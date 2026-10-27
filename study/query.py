"""Sends every query of a set to one model and logs every request and reply (Method, Models and settings).

Run: uv run study/query.py <set> <model>     (model: gpt, claude, gemini or qwen)
Needs OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY or OPENROUTER_API_KEY. It can be stopped
and rerun at any time: it resumes where it left off.

Each item is asked in 17 conditions: its 15 images, the original image again (repeat) and no
image. Queries go out in shuffled order, BatchSize at a time: as batches for Claude and Gemini,
one by one for GPT and Qwen, whose batch APIs do not accept them. The provider's SDK retries each
API call SdkRetries times; a query that still gets no reply is sent once more after the first
pass, and then counts as missing. The run stops, without using up any
attempt, when the provider rejects a request as invalid or when so much of a first-pass batch fails
that the provider looks unavailable; rerun it once the cause is fixed. Writes:
  data/<set>/queries.jsonl          every query: prompt, image file and its SHA-256
  data/<set>/replies/<model>.jsonl  one line per attempt: answer text, how it stopped, usage, the request sent
  data/<set>/replies/raw/           the providers' raw batch results
"""

import base64
import fcntl
import hashlib
import json
import os
import random
import sys
import tempfile
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import anthropic
import openai
from google import genai
from google.genai import errors, types

from analyze import Conditions

Data = Path(__file__).resolve().parent.parent / "data"
MaxOutputTokens = 32_000  # includes reasoning for every provider; the longest pilot reply (Gemini) used 14,904
Effort = "medium"
SdkRetries = 3
# About 50 MB of images (80 MB at most) and 2.3M input tokens: under Anthropic's 256 MB per
# batch, and under the 3M tokens Gemini's Tier 1 queues at once.
BatchSize = 1_000
# When more of a first-pass batch than this fails, the provider is probably down: the run stops
# instead of using up the queries' attempts.
OutageShare = 0.1
PollSeconds = 60
# Errors the provider sent back, so the request surely created nothing. A timeout is not among them:
# the batch may exist, and the open-batch file stays to say so.
Rejected = (openai.APIStatusError, anthropic.APIStatusError, errors.APIError)


def main():
    if len(sys.argv) != 3 or sys.argv[2] not in Models or not (Data / sys.argv[1] / "manifest.jsonl").exists():
        sys.exit("usage: uv run study/query.py pilot|main gpt|claude|gemini|qwen")
    set_name, model = sys.argv[1:]
    folder = Data / set_name
    (folder / "replies").mkdir(exist_ok=True)
    lock = open(folder / "replies" / f"{model}.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        sys.exit(f"another run of {model} on {set_name} is in progress")
    queries = {q["id"]: q for q in load_queries(folder)}
    provider = Models[model]()
    log = ReplyLog(folder / "replies" / f"{model}.jsonl")
    open_batch = folder / "replies" / f"{model}.open-batch.json"
    raw_folder = folder / "replies" / "raw" / model
    if open_batch.exists():
        batch = json.loads(open_batch.read_text())
        if batch["id"] is None:
            sys.exit(f"the last run stopped while submitting a batch: check the provider's console; if a batch "
                     f"was created, write its id into {open_batch}, if not, delete that file, then rerun")
        finish_batch(provider, batch, log, raw_folder, queries, open_batch)
    order = sorted(queries)
    random.Random(f"{set_name} {model}").shuffle(order)
    for attempt in (1, 2):
        while chunk := [queries[i] for i in order if log.attempts[i] == attempt - 1 and i not in log.answered][:BatchSize]:
            if isinstance(provider, OneByOne):
                results = {}
                for query_id, reply in provider.run(chunk):
                    results[query_id] = reply
                    if reply["ok"]:  # logged at once, so an interruption never loses a paid reply
                        log_one(log, query_id, attempt, reply, provider, queries)
                stop_if(log_replies(results, attempt, log, provider, queries))
                continue
            batch = {"id": None, "queries": [q["id"] for q in chunk], "attempt": attempt}
            write_atomic(open_batch, json.dumps(batch))  # recorded first, so a crash cannot hide a paid batch
            try:
                batch["id"] = provider.submit(chunk)
            except Rejected:
                open_batch.unlink()  # the provider answered with an error, so no batch exists
                raise
            write_atomic(open_batch, json.dumps(batch))
            print(f"submitted batch {batch['id']} with {len(chunk)} queries (attempt {attempt})")
            finish_batch(provider, batch, log, raw_folder, queries, open_batch)
    log.print_summary(len(queries))


def load_queries(folder):
    """The queries of a set, written to queries.jsonl on first use so the prompts are logged. Stops if
    the manifest or an image changed since then, so the log always describes what was sent."""
    path = folder / "queries.jsonl"
    items = [json.loads(line) for line in (folder / "manifest.jsonl").read_text().splitlines()]
    lines = []
    for item in items:
        for condition in Conditions:
            image = None if condition == "no_image" else item["images"]["original" if condition == "repeat" else condition]
            lines.append(json.dumps({
                "id": f"{item['id']}-{condition}", "item": item["id"], "task": item["task"],
                "condition": condition, "prompt": item["question"], "image": image,
                "image_sha256": None if image is None else hashlib.sha256((folder / image).read_bytes()).hexdigest(),
            }))
    text = "\n".join(lines) + "\n"
    if not path.exists():
        write_atomic(path, text)
    elif path.read_text() != text:
        sys.exit(f"{path} no longer matches the manifest and images: if the items were regenerated on purpose, "
                 f"start the set's replies afresh, otherwise restore the original items")
    queries = [json.loads(line) for line in path.read_text().splitlines()]
    for q in queries:
        q["file"] = None if q["image"] is None else folder / q["image"]
    return queries


def write_atomic(path, text):
    """Writes the whole file or nothing, so a crash or a parallel run never sees half a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False) as f:
        f.write(text)
    os.replace(f.name, path)


def image_base64(query):
    if query["file"] is None:
        return None
    data = query["file"].read_bytes()
    if hashlib.sha256(data).hexdigest() != query["image_sha256"]:
        sys.exit(f"{query['image']} changed since queries.jsonl was written; not sending it")
    return base64.standard_b64encode(data).decode()


def image_placeholder(query):
    """Stands in for the image data in the request log; the file and hash identify the exact image."""
    return None if query["file"] is None else f"<{query['image']} sha256:{query['image_sha256']}>"


def finish_batch(provider, batch, log, raw_folder, queries, open_batch):
    """Waits for a batch, saves the raw results, logs the replies and closes the batch."""
    while not provider.done(batch["id"]):
        time.sleep(PollSeconds)
    raw = raw_folder / (batch["id"].replace("/", "_") + ".jsonl")
    if not raw.exists():
        write_atomic(raw, provider.download(batch["id"]))
    replies = dict(provider.parse_line(json.loads(line)) for line in raw.read_text().splitlines() if line.strip())
    missing = failure("no result returned for this request")
    results = {i: replies.get(i, missing) for i in batch["queries"]}
    problem = log_replies(results, batch["attempt"], log, provider, queries)
    open_batch.unlink()
    stop_if(problem)


def log_replies(results, attempt, log, provider, queries):
    """Logs one attempt per query and returns why the run must stop, if it must. Rejected requests are
    never logged, and neither are the failures of a first-pass batch that looks like an outage, so a
    rerun sends them again. In the second pass every failure is logged: it was the last try."""
    failed = [i for i, reply in results.items() if not reply["ok"]]
    rejected = [i for i in failed if results[i]["permanent"]]
    outage = attempt == 1 and len(failed) - len(rejected) > OutageShare * len(results)
    for query_id, reply in results.items():
        # A query already logged in this attempt (a batch collected again after a crash, or a reply
        # logged as it arrived) is skipped.
        if log.attempts[query_id] < attempt and (reply["ok"] or not (reply["permanent"] or outage)):
            log_one(log, query_id, attempt, reply, provider, queries)
    if rejected:
        return (f"{len(rejected)} requests were rejected, for example {rejected[0]}: {results[rejected[0]]['error']}; "
                f"fix the cause and rerun, and they will be sent again")
    if outage:
        return (f"{len(failed)} of {len(results)} requests failed, for example {failed[0]}: "
                f"{results[failed[0]]['error']}; the provider looks unavailable, so rerun later")
    return None


def log_one(log, query_id, attempt, reply, provider, queries):
    log.append(query_id, attempt, reply, provider.request(queries[query_id], image_placeholder(queries[query_id])))


def stop_if(problem):
    if problem:
        sys.exit(problem)


def answered(text, stop, stop_reason, input_tokens, output_tokens, raw):
    """A reply from the model. stop is "done" (finished normally), "truncated" (hit the token limit)
    or "blocked" (refused or filtered); only "done" replies are parsed."""
    return {"ok": True, "text": text, "stop": stop, "stop_reason": stop_reason, "input_tokens": input_tokens,
            "output_tokens": output_tokens, "error": None, "permanent": False, "raw": raw}


def failure(error, raw=None, permanent=False):
    """No usable reply: an API error, an expired request, a missing result or an unexpected stop.
    A permanent failure (a bad key, no credits, a rejected request) stops the run instead of being logged."""
    return {"ok": False, "text": None, "stop": None, "stop_reason": None, "input_tokens": None,
            "output_tokens": None, "error": error, "permanent": permanent, "raw": raw}


class ReplyLog:
    """Append-only log of attempts. Knows how often each query was tried and which were answered."""

    def __init__(self, path):
        self.path = path
        self.attempts = Counter()
        self.answered = set()
        self.lines = []
        if path.exists():
            for line in path.read_text().splitlines():
                self._count(json.loads(line))

    def append(self, query_id, attempt, reply, request):
        line = {"query_id": query_id, "attempt": attempt, "time": datetime.now(timezone.utc).isoformat(),
                **reply, "request": request}
        with open(self.path, "a") as f:
            f.write(json.dumps(line) + "\n")
        self._count(line)

    def _count(self, line):
        self.attempts[line["query_id"]] += 1
        if line["ok"]:
            self.answered.add(line["query_id"])
        self.lines.append({k: line[k] for k in ("ok", "stop", "input_tokens", "output_tokens")})

    def print_summary(self, total):
        replies = [line for line in self.lines if line["ok"]]
        print(f"{len(self.answered)} of {total} queries answered, {total - len(self.answered)} missing")
        print(f"stops: {dict(Counter(line['stop'] for line in replies))}")
        print(f"tokens: {sum(r['input_tokens'] or 0 for r in replies):,} input, "
              f"{sum(r['output_tokens'] or 0 for r in replies):,} output (reasoning included)")


class OneByOne:
    """A provider without a usable batch API, reached through the OpenAI SDK: queries go out one by one,
    Workers at a time. A subclass sets the client and says how to send a request and read the reply."""

    def run(self, chunk):
        """Yields (query id, reply) as each call finishes."""
        pool = ThreadPoolExecutor(self.Workers)
        try:
            futures = {pool.submit(self.call, q): q["id"] for q in chunk}
            for future in as_completed(futures):
                yield futures[future], future.result()
        finally:
            pool.shutdown(wait=False, cancel_futures=True)

    def call(self, query):
        try:
            response = self.create(self.request(query, image_base64(query)))
        except (openai.APIConnectionError, openai.RateLimitError, openai.InternalServerError) as error:
            return failure(f"{type(error).__name__}: {error}")
        except openai.APIStatusError as error:  # a bad key, no credits, or a rejected request
            return failure(f"{type(error).__name__}: {error}", permanent=True)
        return self.parse_response(response.model_dump(mode="json"))


class OpenAICalls(OneByOne):
    """GPT-6.1 Sol runs one query at a time on the Flex tier, priced at batch rates: OpenAI's Batch API
    rejected this model ("not supported by the Batch API", pilot on 30 September 2026), although its model
    page lists batch support. Flex answers more slowly and may report a resource as unavailable (429); such
    calls are retried like any rate limit."""
    Model = "gpt-6.1-sol"
    Workers = 8

    def __init__(self):
        self.client = openai.OpenAI(max_retries=SdkRetries, timeout=900)  # Flex can be slow; the default is 600 s

    def request(self, query, image):
        content = []
        if image is not None:
            # "original" is the highest image-detail setting.
            content.append({"type": "input_image", "image_url": f"data:image/png;base64,{image}", "detail": "original"})
        content.append({"type": "input_text", "text": query["prompt"]})
        # Temperature is left out: OpenAI asks to remove it whenever reasoning is on.
        return {"model": self.Model, "service_tier": "flex", "reasoning": {"effort": Effort},
                "max_output_tokens": MaxOutputTokens, "input": [{"role": "user", "content": content}]}

    def create(self, request):
        return self.client.responses.create(**request)

    def parse_response(self, body):
        parts = [part for item in body["output"] if item["type"] == "message" for part in item["content"]]
        text = "".join(part["text"] for part in parts if part["type"] == "output_text")
        reason = (body.get("incomplete_details") or {}).get("reason")
        if body["status"] == "completed":
            stop = "blocked" if any(part["type"] == "refusal" for part in parts) else "done"
        elif body["status"] == "incomplete" and reason in ("max_output_tokens", "content_filter"):
            stop = "truncated" if reason == "max_output_tokens" else "blocked"
        else:
            return failure(f"unexpected status {body['status']} ({reason})", body)
        usage = body.get("usage") or {}
        return answered(text, stop, reason or body["status"], usage.get("input_tokens"), usage.get("output_tokens"), body)


class AnthropicBatch:
    Model = "claude-opus-5-5"
    TransientErrors = ("rate_limit_error", "api_error", "overloaded_error", "timeout_error")

    def __init__(self):
        self.client = anthropic.Anthropic(max_retries=SdkRetries)

    def request(self, query, image):
        content = []
        if image is not None:
            content.append({"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image}})
        content.append({"type": "text", "text": query["prompt"]})
        # Thinking is always on for this model and effort is its only control. Sampling parameters are left out.
        return {"model": self.Model, "max_tokens": MaxOutputTokens, "output_config": {"effort": Effort},
                "messages": [{"role": "user", "content": content}]}

    def submit(self, queries):
        requests = [{"custom_id": q["id"], "params": self.request(q, image_base64(q))} for q in queries]
        # Never retried: a retry after a timeout the server already accepted would create a second paid batch.
        return self.client.with_options(max_retries=0).messages.batches.create(requests=requests).id

    def done(self, batch_id):
        return self.client.messages.batches.retrieve(batch_id).processing_status == "ended"

    def download(self, batch_id):
        return "\n".join(json.dumps(r.model_dump(mode="json")) for r in self.client.messages.batches.results(batch_id))

    def parse_line(self, line):
        query_id = line["custom_id"]
        result = line["result"]
        if result["type"] in ("canceled", "expired"):
            return query_id, failure(result["type"], line)
        if result["type"] == "errored":
            kind = result["error"]["error"]["type"]
            return query_id, failure(json.dumps(result["error"]), line, permanent=kind not in self.TransientErrors)
        message = result["message"]
        stop = {"end_turn": "done", "max_tokens": "truncated", "refusal": "blocked"}.get(message["stop_reason"])
        if stop is None:
            return query_id, failure(f"unexpected stop reason {message['stop_reason']}", line)
        text = "".join(block["text"] for block in message["content"] if block["type"] == "text")
        usage = message["usage"]
        return query_id, answered(text, stop, message["stop_reason"], usage["input_tokens"], usage["output_tokens"], line)


class GeminiBatch:
    Model = "gemini-3.8-flash"
    Blocked = ("SAFETY", "RECITATION", "BLOCKLIST", "PROHIBITED_CONTENT", "SPII",
               "IMAGE_SAFETY", "IMAGE_PROHIBITED_CONTENT", "IMAGE_RECITATION")
    # The docs do not say whether error codes in result files are gRPC or HTTP numbers, so both
    # transient sets are listed: deadline, exhausted, internal, unavailable; 429, 500, 503, 504.
    TransientCodes = (4, 8, 13, 14, 429, 500, 503, 504)

    def __init__(self):
        retries = types.HttpRetryOptions(attempts=SdkRetries + 1)  # attempts include the first request
        self.client = genai.Client(http_options=types.HttpOptions(retry_options=retries))

    def request(self, query, image):
        parts = []
        if image is not None:
            # ULTRA_HIGH is the highest image resolution, and it can only be set per image.
            parts.append({"inline_data": {"mime_type": "image/png", "data": image},
                          "media_resolution": {"level": "MEDIA_RESOLUTION_ULTRA_HIGH"}})
        parts.append({"text": query["prompt"]})
        # Temperature is left out: Google lists it among the deprecated sampling parameters to remove.
        return {"contents": [{"role": "user", "parts": parts}],
                "generation_config": {"thinking_config": {"thinking_level": Effort.upper()},
                                      "max_output_tokens": MaxOutputTokens}}

    def submit(self, queries):
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl") as f:
            for q in queries:
                f.write(json.dumps({"key": q["id"], "request": self.request(q, image_base64(q))}) + "\n")
            f.flush()
            uploaded = self.client.files.upload(file=f.name, config=types.UploadFileConfig(mime_type="jsonl"))
        # Never retried: a retry after a timeout the server already accepted would create a second paid batch.
        once = types.CreateBatchJobConfig(http_options=types.HttpOptions(retry_options=types.HttpRetryOptions(attempts=1)))
        return self.client.batches.create(model=self.Model, src=uploaded.name, config=once).name

    def done(self, batch_id):
        job = self.client.batches.get(name=batch_id)
        if job.state.name == "JOB_STATE_FAILED":
            sys.exit(f"batch {batch_id} failed: {job.error}; fix the request, delete the .open-batch.json file and rerun")
        return job.state.name in ("JOB_STATE_SUCCEEDED", "JOB_STATE_PARTIALLY_SUCCEEDED",
                                  "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED")

    def download(self, batch_id):
        job = self.client.batches.get(name=batch_id)
        if job.dest is None or job.dest.file_name is None:
            return ""
        return self.client.files.download(file=job.dest.file_name).decode()

    def parse_line(self, line):
        query_id = line["key"]
        line = {k: v for k, v in line.items() if k != "request"}  # keeps image data out of the reply log
        if "response" not in line:
            code = (line.get("error") or {}).get("code")
            return query_id, failure(json.dumps(line.get("error")), line, permanent=code not in self.TransientCodes)
        response = line["response"]
        usage = response.get("usageMetadata") or {}
        output_tokens = (usage.get("candidatesTokenCount") or 0) + (usage.get("thoughtsTokenCount") or 0)
        candidates = response.get("candidates") or []
        if not candidates:  # the prompt itself was blocked
            return query_id, answered("", "blocked", json.dumps(response.get("promptFeedback")),
                                      usage.get("promptTokenCount"), output_tokens, line)
        candidate = candidates[0]
        reason = candidate.get("finishReason")
        if reason == "STOP":
            stop = "done"
        elif reason == "MAX_TOKENS":
            stop = "truncated"
        elif reason in self.Blocked:
            stop = "blocked"
        else:
            return query_id, failure(f"unexpected finish reason {reason}", line)
        text = "".join(p.get("text", "") for p in candidate.get("content", {}).get("parts", []) if not p.get("thought"))
        return query_id, answered(text, stop, reason, usage.get("promptTokenCount"), output_tokens, line)


class OpenRouterCalls(OneByOne):
    """Qwen runs through OpenRouter, whose batch mode rejects base64 images, so queries go one by one."""
    Model = "qwen/qwen3.8-27b"
    Endpoint = "deepinfra/bf16"  # unquantized (bf16); the only other unquantized one, Cerebras fp16, caps output at 32,768
    Workers = 16

    def __init__(self):
        self.client = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"],
                                    max_retries=SdkRetries)

    def request(self, query, image):
        content = []
        if image is not None:
            content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image}"}})
        content.append({"type": "text", "text": query["prompt"]})
        return {
            "model": self.Model, "max_tokens": MaxOutputTokens, "messages": [{"role": "user", "content": content}],
            # Sampling as the model card recommends for thinking mode.
            "temperature": 1.0, "top_p": 0.95, "presence_penalty": 0.0,
            "extra_body": {
                # One deployment for every query: no fallback to other providers, and no provider that
                # would silently ignore a parameter.
                "provider": {"order": [self.Endpoint], "allow_fallbacks": False, "require_parameters": True},
                "reasoning": {"effort": Effort},
                "top_k": 20, "min_p": 0.0, "repetition_penalty": 1.0,
            },
        }

    def create(self, request):
        return self.client.chat.completions.create(**request)

    def parse_response(self, raw):
        choice = (raw.get("choices") or [{}])[0]
        stop = {"stop": "done", "length": "truncated", "content_filter": "blocked"}.get(choice.get("finish_reason"))
        if stop is None or choice.get("error"):
            return failure(json.dumps(choice.get("error") or f"unexpected finish reason {choice.get('finish_reason')}"), raw)
        usage = raw.get("usage") or {}
        return answered(choice["message"]["content"] or "", stop, choice["finish_reason"],
                        usage.get("prompt_tokens"), usage.get("completion_tokens"), raw)


Models = {"gpt": OpenAICalls, "claude": AnthropicBatch, "gemini": GeminiBatch, "qwen": OpenRouterCalls}


if __name__ == "__main__":
    main()
