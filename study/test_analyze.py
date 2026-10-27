import json
import math

import numpy as np
import pytest

import analyze
import generate
from analyze import Invalid, Missing


def test_parse_accepts_only_the_requested_form():
    assert analyze.parse("T1", " Yes.\n") == 1.0
    assert analyze.parse("T3", "**no**") == 0.0
    assert analyze.parse("T2", "4") == 4.0
    assert analyze.parse("T2", "7.") == 7.0
    assert analyze.parse("T1", "**yes**.") == analyze.parse("T1", "**yes.**") == analyze.parse("T1", "**yes**") == 1.0
    assert analyze.parse("T1", "Yes, they do.") == Invalid


def test_parse_reads_an_answer_that_stands_alone_on_the_first_or_last_line():
    assert analyze.parse("T1", "B is blue and D is green, so they differ.\n\nNo") == 0.0
    assert analyze.parse("T2", "Orange nodes: D and C.\n\n**2**") == 2.0
    assert analyze.parse("T3", "No\n\nNode H is connected to E, G and A, none of which share its color.") == 0.0
    assert analyze.parse("T3", "Yes\n\nNode K is green, and so is G.\n\n**Yes**") == 1.0
    assert analyze.parse("T1", "Yes\n\nOn second thought:\n\nNo") == Invalid
    assert analyze.parse("T2", "Let me count.\n5\nThat is my answer.") == Invalid
    assert analyze.parse("T2", "four") == Invalid
    assert analyze.parse("T2", "yes") == Invalid
    assert analyze.parse("T1", "") == Invalid


def test_a_truncated_or_blocked_reply_is_invalid_whatever_its_text():
    assert analyze.score("T1", {"text": "yes", "stop": "done"}) == 1.0
    assert analyze.score("T1", {"text": "yes", "stop": "truncated"}) == Invalid
    assert analyze.score("T1", {"text": "yes", "stop": "blocked"}) == Invalid


def table(original, repeat, reassigned, edited, truth, truth_edited, **other):
    """Every recoloring answers like `reassigned` and every edited twin like `edited`, unless a condition
    is given by name in `other` (for example d10=[...])."""
    answers = {"original": original, "repeat": repeat, "no_image": [Missing] * len(truth)}
    for r in analyze.Recolorings:
        answers[r] = reassigned
        answers[analyze.edited_twin(r)] = edited
    answers.update({name.replace("_edited", "-edited"): values for name, values in other.items()})
    return {"truth": np.array(truth, float), "truth_edited": np.array(truth_edited, float),
            "answers": {c: np.array(v, float) for c, v in answers.items()}}


def test_an_invalid_reply_counts_as_a_flip_even_against_another_invalid_reply():
    t = table(original=[Invalid, 1], repeat=[Invalid, 1], reassigned=[1, 1],
              edited=[0, 0], truth=[1, 1], truth_edited=[0, 0])
    stats = analyze.item_statistics(t)
    assert [x.tolist() for x in stats["excess flips, reassigned"]] == [[1.0, 0.0], [1.0, 0.0]]  # flipped, and flipped on the repeat
    assert stats["gain over no image"][0].tolist() == [0.0, 1.0]


def test_a_missing_reply_drops_the_item_from_comparisons_that_need_it():
    t = table(original=[1, 1], repeat=[1, 1], reassigned=[1, 1], d20=[Missing, 1],
              edited=[0, 0], truth=[1, 1], truth_edited=[0, 0])
    stats = analyze.item_statistics(t)
    assert math.isnan(stats["excess flips, d20"][0][0])
    assert stats["excess flips, d14"][0].tolist() == [0.0, 0.0]


def test_h2_counts_items_correct_on_both_drawings():
    # Item 1 misses the edit, item 2 is wrong on the original, so only item 1 counts against H2.
    t = table(original=[1, 0], repeat=[1, 0], reassigned=[1, 0],
              edited=[1, 0], truth=[1, 1], truth_edited=[0, 0])
    both_repeat, both_edited = analyze.item_statistics(t)["edit loss, reassigned"]
    assert (both_repeat - both_edited).tolist() == [1.0, 0.0]


def test_h2_fails_a_model_that_merges_colors_although_its_recolored_and_edited_errors_balance():
    # At d3 a model merges the adjacent colors, so it answers "yes" to every T1 item. Recolored and edited
    # drawings are then equally wrong; against the repeat, the edit loss is plain.
    n = 100
    truth = [1] * 50 + [0] * 50
    edited_truth = [0] * 50 + [1] * 50
    merged = table(original=truth, repeat=truth, reassigned=truth, edited=edited_truth, truth=truth,
                   truth_edited=edited_truth, d3=[1] * n, d3_edited=[1] * n)
    stats = analyze.item_statistics(merged)
    assert np.mean(np.subtract(*stats["edit loss, d3"])) == 0.5 and np.mean(np.subtract(*stats["excess flips, d3"])) == 0.5


def test_support_needs_every_task_below_the_margin_and_one_clearly_failing_task_rejects():
    assert analyze.verdict([(-0.02, 0.02), (-0.02, 0.02), (0.07, 0.17)]) == "rejected"
    assert analyze.verdict([(-0.02, 0.02), (-0.02, 0.02), (0.0, 0.06)]) == "inconclusive"
    assert analyze.verdict([(-0.02, 0.02), (-0.02, 0.02), (0.0, 0.04)]) == "supported"


def test_a_bound_exactly_at_the_margin_is_not_below_it_even_after_floating_point_rounding():
    upper = float(np.mean([0.0, 0.15, 0.0]))  # 0.049999999999999996
    assert upper < analyze.Margin
    assert analyze.verdict([(0.0, upper), (0.0, 0.0), (0.0, 0.0)]) == "inconclusive"


def test_pair_correctness_does_not_let_two_poor_answers_cancel():
    # At d3 the plain drawing is right only on item 1 and the edited one only on item 2: each is 50%
    # accurate, but no item is right on both.
    t = table(original=[1, 0], repeat=[1, 0], reassigned=[1, 0], edited=[0, 1], truth=[1, 0], truth_edited=[0, 1],
              d3=[1, 1], d3_edited=[1, 1])
    lines = analyze.pair_correctness({task: t for task in analyze.Tasks})
    assert next(line for line in lines if line.startswith("| d3 |")).startswith("| d3 | 0.0% [")


def test_the_report_shows_a_missing_edited_reply_in_the_h2_denominator_only():
    items, _ = generate.make_items("pilot", seed=3, items_per_task=20)
    replies = {}
    for item in items:
        for condition in analyze.Conditions:
            answer = item["edited_answer"] if analyze.is_edited(condition) else item["answer"]
            replies[f"{item['id']}-{condition}"] = {"text": str(answer), "stop": "done", "ok": True}
    del replies[next(f"{i['id']}-d10-edited" for i in items if i["task"] == "T1")]
    report = "\n".join(analyze.model_report("m", analyze.answer_tables(items, replies), items, replies))
    assert "| d10 | " in report and "| 60 / 59 |" in report


def test_flips_at_risk_count_only_items_where_reading_two_colors_as_one_changes_the_answer():
    # At d3 the two no items flip to yes; the two yes items cannot be hurt by confusing colors.
    t = table(original=[1, 1, 0, 0], repeat=[1, 1, 0, 0], reassigned=[1, 1, 0, 0], edited=[0, 0, 1, 1],
              truth=[1, 1, 0, 0], truth_edited=[0, 0, 1, 1], d3=[1, 1, 1, 1])
    lines = analyze.flips_at_risk({task: t for task in analyze.Tasks})
    row = next(line for line in lines if line.startswith("| d3 |"))
    assert row.split(" | ")[1].startswith("100.0% [") and "n = 2" in row.split(" | ")[1]


def test_wilson_interval_for_5_of_10():
    p, low, high = analyze.wilson(5, 10)
    assert (p, low, high) == pytest.approx((0.5, 0.2366, 0.7634), abs=1e-4)


def test_wilson_interval_contains_an_estimate_of_one_despite_rounding():
    p, low, high = analyze.wilson(3, 3)
    assert low <= p <= high


def test_wilson_without_data_is_undefined_rather_than_a_crash():
    assert all(math.isnan(x) for x in analyze.wilson(0, 0))


def test_hand_coding_is_compared_with_the_parser_text_by_text(tmp_path):
    rows = [{"task": "T1", "stop": "done", "reply": "Yes", "parsed": 1.0},
            {"task": "T1", "stop": "done", "reply": "Yes", "parsed": 1.0},
            {"task": "T1", "stop": "done", "reply": "No, they differ.", "parsed": Invalid},
            {"task": "T2", "stop": "done", "reply": "4", "parsed": 4.0}]
    distinct = analyze.distinct_replies(rows)
    assert [r["count"] for r in distinct] == [2, 1, 1]
    (tmp_path / "hand_coding.csv").write_text("task,stop,reply,hand_coded\nT1,done,Yes,yes\nT1,done,\"No, they differ.\",no\nT2,done,4,4\n")
    report = "\n".join(analyze.hand_coding_report(distinct, 0, tmp_path / "hand_coding.csv"))
    assert "3 of 3 distinct replies hand coded" in report and "1 disagree" in report and "they differ" in report


def test_a_blank_hand_coding_sheet_does_not_pass(tmp_path):
    distinct = analyze.distinct_replies([{"task": "T1", "stop": "done", "reply": "Yes", "parsed": 1.0}])
    (tmp_path / "hand_coding.csv").write_text("task,stop,reply,hand_coded\nT1,done,Yes,\n")
    report = "\n".join(analyze.hand_coding_report(distinct, 0, tmp_path / "hand_coding.csv"))
    assert "0 of 1 distinct replies hand coded" in report and "does not pass yet" in report


def test_a_model_that_reads_everything_right_is_supported_at_every_distance():
    n = 300
    right = table(original=[1] * n, repeat=[1] * n, reassigned=[1] * n, edited=[0] * n, truth=[1] * n, truth_edited=[0] * n)
    h1, h2, _ = analyze.hypotheses({task: right for task in analyze.Tasks})
    assert analyze.summary(h1) == analyze.summary(h2) == "supported at every distance, down to d3"


def test_each_sequence_stops_at_the_first_distance_that_fails():
    n = 300
    wrong_at_d10 = [0] * 30 + [1] * (n - 30)
    t = table(original=[1] * n, repeat=[1] * n, reassigned=[1] * n, edited=[0] * n, truth=[1] * n,
              truth_edited=[0] * n, d10=wrong_at_d10, d5_edited=[1] * 30 + [0] * (n - 30))
    h1, h2, _ = analyze.hypotheses({task: t for task in analyze.Tasks})
    assert analyze.summary(h1) == "supported down to d14; d10 rejected in T1, T2, T3, T4"
    assert analyze.summary(h2) == "supported down to d7; d5 rejected in T1, T2, T3, T4"


def test_one_task_that_clearly_fails_rejects_both_hypotheses_in_that_task():
    # On T1 the reassigned answer is wrong on 32 of 300 items, and the edits on exactly those items are
    # missed. The mean over tasks is 3.6%, below the margin; T1's interval lies above it.
    n, bad = 300, 32
    perfect = table(original=[1] * n, repeat=[1] * n, reassigned=[1] * n, edited=[0] * n, truth=[1] * n, truth_edited=[0] * n)
    t1 = table(original=[1] * n, repeat=[1] * n, reassigned=[1] * n, edited=[0] * n, truth=[1] * n, truth_edited=[0] * n)
    t1["answers"]["reassigned"] = np.array([0] * bad + [1] * (n - bad), float)
    t1["answers"]["edited"] = np.array([1] * bad + [0] * (n - bad), float)
    h1, h2, intervals = analyze.hypotheses({"T1": t1, "T2": perfect, "T3": perfect})
    assert intervals["excess flips, reassigned"]["T1"][1] > analyze.Margin
    assert (analyze.summary(h1), analyze.summary(h2)) == ("rejected in T1 at reassigned", "rejected in T1 at reassigned")


def test_tango_interval_matches_the_contingencytables_package():
    # Cavo et al. (2012), table [[59, 6], [16, 80]]; the package's tests expect -0.0621 (-0.1240 to -0.0054).
    x = np.array([1] * 59 + [1] * 6 + [0] * 16 + [0] * 80, bool)
    y = np.array([1] * 59 + [0] * 6 + [1] * 16 + [0] * 80, bool)
    estimate, low, high = analyze.tango(x, y)
    assert (round(estimate, 4), round(low, 4), round(high, 4)) == (-0.0621, -0.124, -0.0054)


def test_tango_interval_when_every_item_differs_one_way_matches_the_package():
    # The package's tests: three discordant items, all one way, give 1.0000 (-0.1230 to 1.0000).
    estimate, low, high = analyze.tango(np.array([True] * 3), np.array([False] * 3))
    assert (round(estimate, 4), round(low, 4), round(high, 4)) == (1.0, -0.123, 1.0)


def test_no_flips_at_all_still_leave_an_interval_of_about_1_percent_above_zero():
    zeros = np.zeros(300, bool)
    _, low, high = analyze.tango(zeros, zeros)
    assert -0.013 < low < -0.012 and 0.012 < high < 0.013


def test_the_report_runs_end_to_end_on_a_generated_set(tmp_path, monkeypatch):
    items, _ = generate.make_items("pilot", seed=3, items_per_task=10)
    (tmp_path / "pilot" / "replies").mkdir(parents=True)
    (tmp_path / "pilot" / "manifest.jsonl").write_text("".join(json.dumps(item) + "\n" for item in items))  # analyze reads no images
    with open(tmp_path / "pilot" / "replies" / "perfect.jsonl", "w") as f:
        for item in items:
            for condition in analyze.Conditions:
                answer = item["edited_answer"] if analyze.is_edited(condition) else item["answer"]
                f.write(json.dumps({"query_id": f"{item['id']}-{condition}", "ok": True,
                                    "text": str(answer), "stop": "done"}) + "\n")
    monkeypatch.setattr(analyze, "Data", tmp_path)
    monkeypatch.setattr("sys.argv", ["analyze.py", "pilot"])

    analyze.main()

    report = (tmp_path / "pilot" / "results.md").read_text()
    # 10 items per task are too few to bound even a perfect model's flips below the margin.
    assert "### H1: inconclusive at reassigned" in report and "### H2: inconclusive at reassigned" in report
    assert "| T1 | 100.0% [" in report


def test_ten_units_are_enough_only_when_both_hypotheses_are_supported_there():
    reached_d10 = [(r, "supported") for r in analyze.Recolorings[:4]] + [("d7", "inconclusive")]
    assert analyze.ten_unit_verdict(reached_d10, reached_d10) == "enough"


def test_a_rejection_at_ten_units_or_easier_means_ten_units_are_not_enough():
    rejected_d14 = [("reassigned", "supported"), ("d20", "supported"), ("d14", "rejected in T2")]
    reached_d10 = [(r, "supported") for r in analyze.Recolorings[:4]] + [("d7", "inconclusive")]
    assert analyze.ten_unit_verdict(reached_d10, rejected_d14) == "not enough"


def test_a_rejection_below_ten_units_says_nothing_about_ten_units():
    stopped_d14 = [("reassigned", "supported"), ("d20", "supported"), ("d14", "inconclusive")]
    rejected_d5 = [(r, "supported") for r in analyze.Recolorings[:5]] + [("d5", "rejected in T1")]
    assert analyze.ten_unit_verdict(stopped_d14, rejected_d5) == "undetermined"


def test_structure_only_accuracy_answers_yes_exactly_for_nodes_with_two_neighbors():
    hub = {"u": "A", "answer": "yes", "edge_list": [["A", "B"], ["A", "C"]]}
    leaf_no = {"u": "A", "answer": "no", "edge_list": [["A", "B"]]}
    leaf_yes = {"u": "A", "answer": "yes", "edge_list": [["A", "B"]]}
    assert analyze.structure_only_accuracy([hub, leaf_no, leaf_yes]) == 2 / 3


def test_proximity_only_accuracy_uses_the_best_cutoff():
    def item(distance, answer):
        return {"u": "A", "v": "B", "answer": answer, "positions": {"A": [0, 0], "B": [distance, 0]}}
    # A far edge beyond a near non-edge: no cutoff gets all three, the best gets two.
    assert analyze.proximity_only_accuracy([item(1, "yes"), item(2, "no"), item(3, "yes")]) == 2 / 3


def test_a_rejection_at_52_units_says_nothing_about_ten_units():
    rejected_52 = [("reassigned", "rejected in T1")]
    reached_d10 = [(r, "supported") for r in analyze.Recolorings[:4]] + [("d7", "inconclusive")]
    assert analyze.ten_unit_verdict(rejected_52, reached_d10) == "undetermined"


def test_missing_replies_over_two_percent_get_a_rerun_with_missing_counted_as_invalid():
    n = 100
    complete = table(original=[1] * n, repeat=[1] * n, reassigned=[1] * n, edited=[0] * n, truth=[1] * n, truth_edited=[0] * n)
    complete["answers"]["no_image"] = np.zeros(n)
    gappy = table(original=[1] * n, repeat=[1] * n, reassigned=[1] * n, edited=[0] * n, truth=[1] * n, truth_edited=[0] * n,
                  d10=[Missing] * 3 + [1] * (n - 3))
    gappy["answers"]["no_image"] = np.zeros(n)
    assert analyze.missing_sensitivity({"T1": complete, "T2": complete, "T3": complete}) == []
    report = "\n".join(analyze.missing_sensitivity({"T1": gappy, "T2": complete, "T3": complete}))
    assert "Up to 3.0% of a condition's replies are missing." in report


def test_t4_rates_follow_the_shared_color_through_the_edit():
    # A model that sees an edge exactly when u and v share a color. Item 0 shares one on the original,
    # item 1 does not; the edit switches both, so every yes lands in the shared-color cell.
    items = [{"task": "T4", "u": "A", "v": "B", "groups": {"A": 0, "B": 0}},
             {"task": "T4", "u": "A", "v": "B", "groups": {"A": 0, "B": 1}}]
    t = table(original=[1, 0], repeat=[1, 0], reassigned=[1, 0], edited=[0, 1], truth=[0, 0], truth_edited=[0, 0])
    rates = analyze.shared_color_rates({"T4": t}, items)
    assert rates["tab10"] == rates["d3"] == {(False, True): 1.0, (False, False): 0.0, (True, True): None, (True, False): None}
