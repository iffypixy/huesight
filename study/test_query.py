import json
import shutil

import anthropic
import httpx
import pytest

import generate
import query


@pytest.fixture
def providers(monkeypatch):
    for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "OPENROUTER_API_KEY"):
        monkeypatch.setenv(key, "test-key")
    return {name: cls() for name, cls in query.Models.items()}


Question = {"id": "pilot-T1-000-original", "prompt": "In this graph drawing, do nodes A and B have the same color?"}


def test_requests_put_the_image_before_the_question_and_use_the_agreed_settings(providers):
    gpt = providers["gpt"].request(Question, "IMG")
    assert gpt["model"] == "gpt-6.1-sol" and gpt["reasoning"] == {"effort": "medium"}
    assert gpt["max_output_tokens"] == 32_000 and "temperature" not in gpt and gpt["service_tier"] == "flex"
    assert [part["type"] for part in gpt["input"][0]["content"]] == ["input_image", "input_text"]
    assert gpt["input"][0]["content"][0]["detail"] == "original"

    claude = providers["claude"].request(Question, "IMG")
    assert claude["model"] == "claude-opus-5-5" and claude["output_config"] == {"effort": "medium"}
    assert claude["max_tokens"] == 32_000 and "temperature" not in claude and "thinking" not in claude
    assert [part["type"] for part in claude["messages"][0]["content"]] == ["image", "text"]

    gemini = providers["gemini"].request(Question, "IMG")
    config = gemini["generation_config"]
    assert config == {"thinking_config": {"thinking_level": "MEDIUM"}, "max_output_tokens": 32_000}
    parts = gemini["contents"][0]["parts"]
    assert parts[0]["media_resolution"] == {"level": "MEDIA_RESOLUTION_ULTRA_HIGH"} and "text" in parts[1]

    qwen = providers["qwen"].request(Question, "IMG")
    assert qwen["model"] == "qwen/qwen3.8-27b" and qwen["max_tokens"] == 32_000
    assert qwen["extra_body"]["provider"] == {"order": ["deepinfra/bf16"], "allow_fallbacks": False,
                                               "require_parameters": True}
    assert qwen["extra_body"]["reasoning"] == {"effort": "medium"}
    assert [part["type"] for part in qwen["messages"][0]["content"]] == ["image_url", "text"]


def test_a_no_image_query_sends_only_the_question(providers):
    assert [p["type"] for p in providers["claude"].request(Question, None)["messages"][0]["content"]] == ["text"]
    assert [list(p) for p in providers["gemini"].request(Question, None)["contents"][0]["parts"]] == [["text"]]


def test_openai_responses(providers):
    done = {"status": "completed", "incomplete_details": None, "usage": {"input_tokens": 900, "output_tokens": 300},
            "output": [{"type": "reasoning", "summary": []},
                       {"type": "message", "content": [{"type": "output_text", "text": "Yes"}]}]}
    cut = {"status": "incomplete", "incomplete_details": {"reason": "max_output_tokens"}, "usage": {}, "output": []}
    refused = {"status": "completed", "incomplete_details": None, "usage": {},
               "output": [{"type": "message", "content": [{"type": "refusal", "refusal": "I can't help with that."}]}]}
    failed = {"status": "failed", "incomplete_details": None, "usage": {}, "output": []}
    parse = providers["gpt"].parse_response
    assert (parse(done)["text"], parse(done)["stop"]) == ("Yes", "done")
    assert parse(cut)["stop"] == "truncated"
    assert parse(refused)["stop"] == "blocked"
    assert parse(failed)["ok"] is False and not parse(failed)["permanent"]


def test_anthropic_result_lines(providers):
    done = {"custom_id": "q1", "result": {"type": "succeeded", "message": {
        "stop_reason": "end_turn", "usage": {"input_tokens": 800, "output_tokens": 200},
        "content": [{"type": "thinking", "thinking": ""}, {"type": "text", "text": "No"}]}}}
    refused = {"custom_id": "q2", "result": {"type": "succeeded", "message": {
        "stop_reason": "refusal", "usage": {"input_tokens": 800, "output_tokens": 5}, "content": []}}}
    errored = {"custom_id": "q3", "result": {"type": "errored", "error": {"type": "error", "error": {"type": "api_error"}}}}
    invalid = {"custom_id": "q4", "result": {"type": "errored",
                                             "error": {"type": "error", "error": {"type": "invalid_request_error"}}}}
    paused = {"custom_id": "q5", "result": {"type": "succeeded", "message": {
        "stop_reason": "pause_turn", "usage": {"input_tokens": 800, "output_tokens": 5}, "content": []}}}
    parse = providers["claude"].parse_line
    assert (parse(done)[1]["text"], parse(done)[1]["stop"]) == ("No", "done")
    assert parse(refused)[1]["stop"] == "blocked"
    assert parse(errored)[1]["ok"] is False and not parse(errored)[1]["permanent"]
    assert parse(invalid)[1]["permanent"]
    assert parse(paused)[1]["ok"] is False


def test_gemini_result_lines_skip_thought_parts(providers):
    done = {"key": "q1", "response": {"usageMetadata": {"promptTokenCount": 2300, "candidatesTokenCount": 1,
                                                        "thoughtsTokenCount": 400},
        "candidates": [{"finishReason": "STOP", "content": {"parts": [
            {"text": "Counting the orange nodes...", "thought": True}, {"text": "4"}]}}]}}
    cut = {"key": "q2", "response": {"candidates": [{"finishReason": "MAX_TOKENS", "content": {"parts": []}}]}}
    failed = {"key": "q3", "error": {"code": 500, "message": "internal"}}
    other = {"key": "q4", "response": {"candidates": [{"finishReason": "OTHER", "content": {"parts": []}}]}}
    safety = {"key": "q5", "request": {"contents": "<image data>"},
              "response": {"candidates": [{"finishReason": "SAFETY", "content": {"parts": []}}]}}
    parse = providers["gemini"].parse_line
    reply = parse(done)[1]
    assert (reply["text"], reply["stop"], reply["output_tokens"]) == ("4", "done", 401)
    assert parse(cut)[1]["stop"] == "truncated"
    assert parse(failed)[1]["ok"] is False and not parse(failed)[1]["permanent"]
    assert parse(other)[1]["ok"] is False
    assert parse(safety)[1]["stop"] == "blocked" and "request" not in parse(safety)[1]["raw"]


def test_openrouter_responses(providers):
    parse = providers["qwen"].parse_response
    done = {"choices": [{"finish_reason": "stop", "message": {"content": "yes", "reasoning": "..."}}],
            "usage": {"prompt_tokens": 900, "completion_tokens": 700}}
    error_in_body = {"choices": [{"finish_reason": "error", "error": {"code": 502}, "message": {"content": ""}}]}
    assert (parse(done)["text"], parse(done)["stop"]) == ("yes", "done")
    assert parse(error_in_body)["ok"] is False


class FakeProvider:
    """Answers "yes" to everything, except that it fails the `failing` queries on every attempt and
    rejects the `rejected` queries as invalid."""

    def __init__(self, failing=(), rejected=()):
        self.failing = set(failing)
        self.rejected = set(rejected)
        self.batches = {}

    def request(self, query, image):
        return {"prompt": query["prompt"], "image": image}

    def submit(self, queries):
        batch_id = f"batch-{len(self.batches)}"
        self.batches[batch_id] = [q["id"] for q in queries]
        return batch_id

    def done(self, batch_id):
        return True

    def download(self, batch_id):
        return "\n".join(json.dumps({"id": i}) for i in self.batches[batch_id] if i not in self.failing)

    def parse_line(self, line):
        if line["id"] in self.rejected:
            return line["id"], query.failure("invalid_request_error", line, permanent=True)
        return line["id"], query.answered("yes", "done", "stop", 1, 1, line)


@pytest.fixture(scope="module")
def drawn(tmp_path_factory):
    """A generated set of 3 items (51 queries), drawn once for the module."""
    folder = tmp_path_factory.mktemp("drawn") / "pilot"
    items, rejections = generate.make_items("pilot", seed=3, items_per_task=1, tasks=generate.Sets["pilot"]["tasks"])
    generate.write_set(folder, items, rejections)
    return folder


@pytest.fixture
def pilot(drawn, tmp_path, monkeypatch):
    """A fresh copy of the drawn set, with query.py pointed at it."""
    shutil.copytree(drawn, tmp_path / "pilot")
    items = [json.loads(line) for line in (tmp_path / "pilot" / "manifest.jsonl").read_text().splitlines()]
    monkeypatch.setattr(query, "Data", tmp_path)
    monkeypatch.setattr("sys.argv", ["query.py", "pilot", "fake"])
    return {"items": items, "log": tmp_path / "pilot" / "replies" / "fake.jsonl", "folder": tmp_path / "pilot"}


def use(monkeypatch, fake, batch_size):
    monkeypatch.setattr(query, "Models", {"fake": lambda: fake})
    monkeypatch.setattr(query, "BatchSize", batch_size)


def logged(path):
    tries = {}
    for line in path.read_text().splitlines():
        line = json.loads(line)
        tries.setdefault(line["query_id"], []).append(line["ok"])
    return tries


def test_a_failed_query_is_sent_once_more_then_counts_as_missing(pilot, monkeypatch):
    failing = f"{pilot['items'][0]['id']}-edited"
    use(monkeypatch, FakeProvider(failing=[failing]), batch_size=51)

    query.main()

    tries = logged(pilot["log"])
    assert len(tries) == 51
    assert tries[failing] == [False, False]
    assert all(oks == [True] for query_id, oks in tries.items() if query_id != failing)
    first = json.loads(pilot["log"].read_text().splitlines()[0])
    assert first["request"]["image"] is None or first["request"]["image"].startswith("<images/")


def test_a_rejected_request_stops_the_run_unlogged_and_is_sent_again_on_rerun(pilot, monkeypatch):
    rejected = f"{pilot['items'][0]['id']}-original"
    use(monkeypatch, FakeProvider(rejected=[rejected]), batch_size=51)

    with pytest.raises(SystemExit, match="rejected"):
        query.main()
    assert rejected not in logged(pilot["log"])

    use(monkeypatch, FakeProvider(), batch_size=51)
    query.main()
    assert logged(pilot["log"])[rejected] == [True]


def test_a_first_pass_outage_stops_the_run_without_using_up_attempts(pilot, monkeypatch):
    ids = [f"{item['id']}-{c}" for item in pilot["items"] for c in ("original", "repeat", "edited")]
    use(monkeypatch, FakeProvider(failing=ids), batch_size=51)

    with pytest.raises(SystemExit, match="unavailable"):
        query.main()

    tries = logged(pilot["log"])
    assert len(tries) == 51 - len(ids) and all(oks == [True] for oks in tries.values())


def test_collecting_a_batch_again_after_a_crash_logs_nothing_twice(pilot, monkeypatch):
    fake = FakeProvider()
    use(monkeypatch, fake, batch_size=51)
    query.main()
    before = pilot["log"].read_text()
    # A crash between logging the replies and closing the batch leaves the batch open.
    open_batch = pilot["folder"] / "replies" / "fake.open-batch.json"
    open_batch.write_text(json.dumps({"id": "batch-0", "queries": fake.batches["batch-0"], "attempt": 1}))

    query.main()

    assert pilot["log"].read_text() == before


def test_qwen_replies_are_logged_as_they_arrive_so_a_crash_loses_none(pilot, monkeypatch):
    class Crashing(query.OpenRouterCalls):
        Workers = 1

        def __init__(self):
            self.calls = 0

        def call(self, q):
            self.calls += 1
            if self.calls == 5:
                raise RuntimeError("crash")
            return query.answered("yes", "done", "stop", 1, 1, {})
    use(monkeypatch, Crashing(), batch_size=51)

    with pytest.raises(RuntimeError):
        query.main()

    assert len(logged(pilot["log"])) == 4


def test_a_changed_image_is_never_sent(pilot, monkeypatch):
    use(monkeypatch, FakeProvider(), batch_size=51)
    queries = query.load_queries(pilot["folder"])
    image = next(q for q in queries if q["file"] is not None)
    image["file"].write_bytes(image["file"].read_bytes() + b"changed")

    with pytest.raises(SystemExit, match="changed"):
        query.image_base64(image)
    with pytest.raises(SystemExit, match="no longer matches"):
        query.load_queries(pilot["folder"])


def test_a_batch_the_provider_refuses_to_create_leaves_no_open_batch_behind(pilot, monkeypatch):
    class Refusing(FakeProvider):
        def submit(self, queries):
            request = httpx.Request("POST", "https://api.example.com/batches")
            raise anthropic.BadRequestError("credit balance too low", response=httpx.Response(400, request=request), body=None)
    use(monkeypatch, Refusing(), batch_size=51)

    with pytest.raises(anthropic.BadRequestError):
        query.main()

    assert not (pilot["folder"] / "replies" / "fake.open-batch.json").exists()


def test_a_run_that_stopped_while_submitting_asks_for_a_check_instead_of_submitting_again(pilot, monkeypatch):
    use(monkeypatch, FakeProvider(), batch_size=51)
    open_batch = pilot["folder"] / "replies" / "fake.open-batch.json"
    open_batch.parent.mkdir(parents=True)
    open_batch.write_text(json.dumps({"id": None, "queries": [], "attempt": 1}))

    with pytest.raises(SystemExit, match="console"):
        query.main()
