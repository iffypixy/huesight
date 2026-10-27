"""Scores the replies and computes the validity check, H1, H2 and the verdicts of the thesis's Method chapter.

Run: uv run study/analyze.py <set>
Reads data/<set>/manifest.jsonl and data/<set>/replies/<model>.jsonl, and writes
data/<set>/results.md, data/<set>/parsed.csv (every reply with its parsed answer) and
data/<set>/replies_to_code.csv (every distinct reply text once, with how often it occurred).

For the pilot's parser check (Appendix, Pilots), copy replies_to_code.csv to hand_coding.csv and fill its
hand_coded column with yes, no, a number or invalid. Identical texts always get the same code, so
coding each distinct text once checks every reply. The script only reads hand_coding.csv, so
rerunning it never loses the hand coding, and results.md lists every disagreement with the parser.
"""

import csv
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from statistics import NormalDist

import numpy as np

from generate import Bands, Distances, ImagePx, Limit, Tasks

Data = Path(__file__).resolve().parent.parent / "data"
# The tasks whose answer turns on the colors. T4, the control, asks about an edge, so the analyses of how
# colors are confused, and the values pooled over tasks, use these three; T4 is reported on its own.
ColorTasks = ("T1", "T2", "T3")
# Each recoloring comes with an edited twin in the same palette: the reassigned tab10 palette (52
# CIEDE2000 units between its closest colors) pairs with the original palette edited, and every
# ladder palette "d<distance>" with "d<distance>-edited" (Method, Conditions). Both hypotheses are tested
# along this order, from easy to hard (Method, Decision rule).
Recolorings = ("reassigned",) + tuple(f"d{d}" for d in Distances)
Ladder = Recolorings[1:]
# A published design recommendation: categorical palettes keep their colors at least this many CIEDE2000
# units apart (Background, Measuring color difference). Each model's result is read against it; the tests run past it.
PaletteThreshold = 10
Conditions = ("original", "repeat") + tuple(c for r in Recolorings for c in (r, "edited" if r == "reassigned" else f"{r}-edited")) + ("no_image",)
Invalid = -1.0  # a reply without a valid answer line, or truncated: counts as wrong, and as a flip in H1
Missing = math.nan  # no reply after all retries: the item drops out of comparisons that need it
Margin = 0.05
# A bound this close to the margin counts as touching it, so floating-point noise (0.0499999...) cannot
# decide a tie.
Tie = 1e-9
# The two losses, H1's and H2's, by the names every comparison and table uses.
Kinds = ("excess flips", "edit loss")
# The names of the models in the report, by the name of their replies file.
ModelNames = {"claude": "Claude Opus 5.5", "qwen": "Qwen3.8-27B", "gpt": "GPT-6.1 Sol", "gemini": "Gemini 3.8 Flash"}
Z = 1.959964  # two-sided 95%


def main():
    name = sys.argv[1] if len(sys.argv) == 2 else None
    folder = Data / str(name)
    if name is None or not (folder / "manifest.jsonl").exists():
        sys.exit("usage: uv run study/analyze.py pilot|main")
    items = [json.loads(line) for line in (folder / "manifest.jsonl").read_text().splitlines()]
    reply_files = sorted((folder / "replies").glob("*.jsonl"))
    if not reply_files:
        sys.exit(f"no replies in {folder / 'replies'}")
    report = [f"# Results: {name}", "", f"{len(items)} items. Intervals are 95%; margin {Margin * 100:g} pp.", ""]
    rows = []
    for path in reply_files:
        replies = first_replies(path)
        tables = answer_tables(items, replies)
        report += model_report(path.stem, tables, items, replies)
        rows += parsed_rows(path.stem, items, replies)
    distinct = distinct_replies(rows)
    report += hand_coding_report(distinct, sum(r["reply"] is None for r in rows), folder / "hand_coding.csv")
    (folder / "results.md").write_text("\n".join(report) + "\n")
    write_csv(folder / "parsed.csv", rows)
    write_csv(folder / "replies_to_code.csv", distinct)
    print(f"wrote results.md, parsed.csv and replies_to_code.csv in {folder}")


def write_csv(path, rows):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def score(task, reply):
    """The answer in a reply, or Invalid when the model did not finish normally (truncated or blocked)."""
    return parse(task, reply["text"]) if reply["stop"] == "done" else Invalid


def parse(task, text):
    """The answer in a reply's text, or Invalid. The answer must stand alone on the first or the last
    non-empty line, because models sometimes explain before or after it (seen in the pilot). If both
    lines hold answers that differ, or neither holds one, the reply is invalid."""
    lines = [line for line in text.strip().splitlines() if line.strip()]
    if not lines:
        return Invalid
    answers = {parse_line(task, lines[0]), parse_line(task, lines[-1])} - {Invalid}
    return answers.pop() if len(answers) == 1 else Invalid


def parse_line(task, line):
    """Accepts only the requested form: "yes" or "no" for T1, T3 and T4, a whole number for T2. Ignores case,
    surrounding whitespace, asterisks on either side (markdown bold or italics, paired or not) and a
    final period inside and/or outside them."""
    answer = line.strip().removesuffix(".").strip().strip("*").strip().removesuffix(".").strip().lower()
    if task == "T2":
        return float(answer) if re.fullmatch(r"[0-9]+", answer) else Invalid
    return {"yes": 1.0, "no": 0.0}.get(answer, Invalid)


def first_replies(path):
    """query id -> the first successful reply; failed attempts are skipped."""
    replies = {}
    for line in path.read_text().splitlines():
        reply = json.loads(line)
        if reply["ok"] and reply["query_id"] not in replies:
            replies[reply["query_id"]] = reply
    return replies


def answer_tables(items, replies):
    """Per task of the set: the correct answers and each condition's parsed answers, one entry per item."""
    tables = {}
    for task in [t for t in Tasks if any(item["task"] == t for item in items)]:
        task_items = [item for item in items if item["task"] == task]
        answers = {}
        for condition in Conditions:
            values = []
            for item in task_items:
                reply = replies.get(f"{item['id']}-{condition}")
                values.append(Missing if reply is None else score(task, reply))
            answers[condition] = np.array(values)
        tables[task] = {
            "truth": np.array([encode(item["answer"]) for item in task_items]),
            "truth_edited": np.array([encode(item["edited_answer"]) for item in task_items]),
            "answers": answers,
        }
    return tables


def encode(answer):
    return {"yes": 1.0, "no": 0.0}.get(answer, answer) * 1.0


def edited_twin(recoloring):
    return "edited" if recoloring == "reassigned" else f"{recoloring}-edited"


def is_edited(condition):
    return condition == "edited" or condition.endswith("-edited")


def item_statistics(table):
    """Per comparison, the two paired indicators (x, y) whose difference in means it estimates, one
    entry per item; NaN where a needed reply is missing.

    Excess flips, r: whether the answer changed from original to recolored, against whether it
    changed on the repeat. Edit loss, r: correct on both original and repeat, against correct on both
    original and edited twin. Both are measured against the repeat, the noise floor. Gain over no
    image: correct on the original, against correct with no image."""
    a = table["answers"]
    truth = table["truth"]

    def correct(condition, target):
        return np.where(np.isnan(a[condition]), np.nan, (a[condition] == target) * 1.0)

    def flip(x, y):
        changed = (a[x] != a[y]) | (a[x] == Invalid) | (a[y] == Invalid)
        return np.where(np.isnan(a[x]) | np.isnan(a[y]), np.nan, changed * 1.0)

    original = correct("original", truth)
    statistics = {"gain over no image": (original, correct("no_image", truth))}
    both_repeat = original * correct("repeat", truth)
    for r in Recolorings:
        statistics[f"excess flips, {r}"] = (flip("original", r), flip("original", "repeat"))
        statistics[f"edit loss, {r}"] = (both_repeat, original * correct(edited_twin(r), table["truth_edited"]))
    return statistics


def hypotheses(tables, margin=Margin):
    """H1 and H2 for one model (Method, Hypotheses), each tested along Recolorings in a fixed sequence: a
    distance is tested only if every easier one was supported, so each claim "supported down to this
    distance" is an intersection-union test and needs no multiplicity correction (Westfall and Krishen,
    2001). Returns the two sequences of (recoloring, verdict) and, per comparison and task, the
    estimate and its 95% interval. Another margin than the 5 points is for description only."""
    statistics = {task: item_statistics(table) for task, table in tables.items()}
    names = [f"{kind}, {r}" for kind in Kinds for r in Recolorings]
    intervals = {name: {task: difference(*statistics[task][name]) for task in tables} for name in names}
    h1, h2 = [fixed_sequence((r, level_verdict(intervals[f"{kind}, {r}"], margin)) for r in Recolorings) for kind in Kinds]
    return h1, h2, intervals


def fixed_sequence(verdicts):
    """The (recoloring, verdict) pairs, from easy to hard, up to and including the first that is not
    supported. The verdicts are computed lazily, so nothing past that first one is tested."""
    sequence = []
    for r, outcome in verdicts:
        sequence.append((r, outcome))
        if outcome != "supported":
            break
    return sequence


def level_verdict(interval, margin=Margin):
    """The verdict at one distance; a rejection names the tasks whose interval lies above the margin,
    since each of them is a claim of its own."""
    outcome = verdict([bounds[1:] for bounds in interval.values()], margin)
    if outcome == "rejected":
        outcome += " in " + ", ".join(task for task, bounds in interval.items() if bounds[1] > margin + Tie)
    return outcome


def ten_unit_verdict(h1, h2):
    """What the two sequences say about the 10-unit recommendation (Method, Decision rule): enough if both hypotheses
    are supported at 10 units; not enough if either sequence stops with a rejection on a ladder palette at
    20, 14 or 10 units, which assumes that a closer ladder palette is no easier than one that already
    failed; undetermined otherwise. A rejection at 52 units does not count: that step also changes lightness and
    chroma, not only the distance."""
    reached = [[r for r, v in sequence if v == "supported"] for sequence in (h1, h2)]
    if all(f"d{PaletteThreshold}" in supported for supported in reached):
        return "enough"
    ladder_at_or_above = Ladder[:Ladder.index(f"d{PaletteThreshold}") + 1]
    if any(v.startswith("rejected") and r in ladder_at_or_above for sequence in (h1, h2) for r, v in sequence):
        return "not enough"
    return "undetermined"


def summary(sequence):
    """One line for a fixed-sequence result, for example "supported down to d14; d10 inconclusive"."""
    supported = [r for r, v in sequence if v == "supported"]
    if len(supported) == len(Recolorings):
        return f"supported at every distance, down to {Recolorings[-1]}"
    stop, why = sequence[-1]
    return f"supported down to {supported[-1]}; {stop} {why}" if supported else f"{why} at {stop}"


def completed(x, y):
    """The number of items behind a paired comparison: those with every reply it needs."""
    return int((~np.isnan(x) & ~np.isnan(y)).sum())


def difference(x, y, z=None):
    """Estimate and 95% interval (or the interval for normal quantile z) for mean(x) - mean(y), two 0/1
    indicators on the same items; items where either is NaN drop out. Returns (estimate, low, high), all
    NaN without items."""
    known = ~np.isnan(x) & ~np.isnan(y)
    return tango(x[known] == 1, y[known] == 1, z)


def tango(x, y, z=None):
    """Tango's asymptotic score interval for the difference of two paired proportions (Tango, 1998), as
    given by Fagerland, Lydersen and Laake (2017) and their contingencytables package: the limits are the
    differences at which the score statistic, with the restricted maximum-likelihood estimate of the
    discordant cell, equals the normal quantile. It uses how many items differ in each direction and the
    total, not how the agreeing items split into both right and both wrong, and keeps a one-sided
    false-support rate near the nominal 2.5% at the margin, where Newcombe's square-and-add interval
    (Newcombe, 1998) reached 3% to 4% in simulation (Appendix, Design choices)."""
    n = len(x)
    if n == 0:
        return math.nan, math.nan, math.nan
    only_x, only_y = int((x & ~y).sum()), int((~x & y).sum())
    estimate = (only_x - only_y) / n

    def score(delta):
        a = 2 * n
        b = -only_x - only_y + (2 * n - only_x + only_y) * delta
        c = -only_y * delta * (1 - delta)
        p_only_y = (math.sqrt(b * b - 4 * a * c) - b) / (2 * a)
        variance = n * (2 * p_only_y + delta * (1 - delta))
        if variance <= 0:  # no discordant items and delta = 0: the statistic's limit there is 0
            return 0.0
        return (only_x - only_y - n * delta) / math.sqrt(variance)

    def root(target):
        """The delta in (-1, 1) where score(delta) = target; score falls as delta grows."""
        low, high = -1 + 1e-12, 1 - 1e-12
        for _ in range(200):
            middle = (low + high) / 2
            if score(middle) > target:
                low = middle
            else:
                high = middle
        return (low + high) / 2

    z = Z if z is None else z
    lower = -1.0 if estimate == -1 else root(z)
    upper = 1.0 if estimate == 1 else root(-z)
    return estimate, lower, upper


def verdict(per_task, margin=Margin):
    """Supported if every task's interval lies below the margin (an intersection-union test over the
    tasks), rejected if any task's interval lies entirely above it, inconclusive otherwise. A bound
    exactly at the margin counts as touching it (Tie)."""
    if any(low > margin + Tie for low, _ in per_task):
        return "rejected"
    if all(high < margin - Tie for _, high in per_task):
        return "supported"
    return "inconclusive"



def validity_check(tables, items):
    """Per task: accuracy on the original above chance (Wilson), and gain over no image above zero (Tango).
    Chance is the share of the most common correct answer; for T3 it is at least the accuracy of answering
    from the drawing's structure alone, yes when u has two or more neighbors (structure_only_accuracy), and
    for T4 at least that of answering from proximity alone (proximity_only_accuracy)."""
    rows = {}
    for task in tables:
        original, no_image = item_statistics(tables[task])["gain over no image"]
        correct = original[~np.isnan(original)]
        truth = tables[task]["truth"]
        chance = max(Counter(truth.tolist()).values()) / len(truth)
        if task == "T3":
            chance = max(chance, structure_only_accuracy([item for item in items if item["task"] == "T3"]))
        if task == "T4":
            chance = max(chance, proximity_only_accuracy([item for item in items if item["task"] == "T4"]))
        accuracy = wilson(int(correct.sum()), len(correct))
        gain = difference(original, no_image)
        blind = tables[task]["answers"]["no_image"]
        blind = blind[~np.isnan(blind)]
        rows[task] = {"accuracy": accuracy, "chance": chance, "gain": gain, "n": len(correct),
                      "gain n": completed(original, no_image), "invalid without image": (int((blind == Invalid).sum()), len(blind)),
                      "passes": accuracy[1] > chance and gain[1] > 0}
    return rows


def structure_only_accuracy(t3_items):
    """The share of T3 items a reader blind to color answers correctly by saying yes exactly when u has two
    or more neighbors: in the generated items, u's degree is not independent of the answer."""
    hits = 0
    for item in t3_items:
        degree = sum(item["u"] in edge for edge in item["edge_list"])
        hits += (degree >= 2) == (item["answer"] == "yes")
    return hits / len(t3_items)


def proximity_only_accuracy(t4_items):
    """The share of T4 items a reader blind to edges answers correctly by saying yes exactly when u and v
    are closer than some cutoff, with the best cutoff for these items: nodes joined by an edge sit closer."""
    distances = [(math.dist(item["positions"][item["u"]], item["positions"][item["v"]]), item["answer"] == "yes")
                 for item in t4_items]
    return max(sum((d <= cutoff) == joined for d, joined in distances) for cutoff, _ in distances) / len(distances)


def wilson(successes, n):
    """Point estimate and 95% Wilson interval for a proportion (NIST handbook, section 7.2.4.1)."""
    if n == 0:
        return math.nan, math.nan, math.nan
    p = successes / n
    center = (p + Z**2 / (2 * n)) / (1 + Z**2 / n)
    half = Z / (1 + Z**2 / n) * math.sqrt(p * (1 - p) / n + Z**2 / (4 * n**2))
    # The interval contains p exactly; at p = 0 or 1, rounding can leave a bound a hair on the wrong side.
    return p, min(center - half, p), max(center + half, p)


def model_report(model, tables, items, replies):
    check = validity_check(tables, items)
    h1, h2, intervals = hypotheses(tables)
    passes = all(row["passes"] for row in check.values())
    tokens = [r["output_tokens"] for r in replies.values() if r.get("output_tokens") is not None]
    lines = [f"## {ModelNames.get(model, model)}", ""]
    if tokens:
        lines += [f"Output tokens per reply, reasoning included: mean {np.mean(tokens):.0f}, median {np.median(tokens):.0f}.", ""]
    lines += ["### Validity check", "",
             "| Task | Accuracy, original | Bar | Gain over no image | Invalid without image | Passes |",
             "| --- | --- | --- | --- | --- | --- |"]
    for task, row in check.items():
        p, low, high = row["accuracy"]
        invalid, asked = row["invalid without image"]
        lines.append(f"| {task} | {pct(p)} [{pct(low)}, {pct(high)}], n = {row['n']} | {pct(row['chance'])} "
                     f"| {pct(row['gain'][0])} [{pct(row['gain'][1])}, {pct(row['gain'][2])}], n = {row['gain n']} "
                     f"| {invalid} of {asked} | {'yes' if row['passes'] else 'no'} |")
    lines += ["", "Invalid includes refusals: without the image, some models decline to answer, and that counts as wrong."]
    note = "" if passes else " (not interpreted: the validity check failed)"
    lines += ["", f"### H1: {summary(h1)}{note}", "", f"### H2: {summary(h2)}{note}", "",
              f"### The {PaletteThreshold}-unit recommendation: {ten_unit_verdict(h1, h2)}{note}", "",
              f"The published design recommendation keeps categorical colors at least {PaletteThreshold} CIEDE2000 units apart.",
              "", "### By color distance", "",
              "Means of the T1 to T3 values, for description; the verdicts use the intervals per task, below.", "",
              "| Recoloring | Excess flips | Edit loss | Accuracy, recolored | Accuracy, edited | n, H1 / H2 |",
              "| --- | --- | --- | --- | --- | --- |"]
    statistics = {task: item_statistics(table) for task, table in tables.items()}
    for r in Recolorings:
        cells = [pct(float(np.mean([intervals[f"{kind}, {r}"][task][0] for task in ColorTasks])))
                 for kind in Kinds]
        n = [sum(completed(*statistics[task][f"{kind}, {r}"]) for task in ColorTasks) for kind in Kinds]
        name = "reassigned (52)" if r == "reassigned" else r
        lines.append(f"| {name} | {cells[0]} | {cells[1]} | {pooled_accuracy(tables, r)} "
                     f"| {pooled_accuracy(tables, edited_twin(r))} | {n[0]} / {n[1]} |")
    lines += ["", f"Answers changed on the repeat, mean over all tasks: {pct(float(np.mean([repeat_flips(t) for t in tables.values()])))}. "
              "n counts the T1 to T3 items with every reply the comparison needs.", "",
              "### Per task", "",
              "95% intervals; these decide the verdicts. A hypothesis is supported at a distance only if every task's interval lies below the margin.", ""]
    for kind in Kinds:
        lines += [f"| {kind.capitalize()} | " + " | ".join(tables) + " |", "| --- |" + " --- |" * len(tables)]
        for r in Recolorings:
            cells = [f"{pct(e)} [{pct(low)}, {pct(high)}], n = {completed(*statistics[task][f'{kind}, {r}'])}"
                     for task, (e, low, high) in ((task, intervals[f"{kind}, {r}"][task]) for task in tables)]
            lines.append(f"| {r} | " + " | ".join(cells) + " |")
        lines.append("")
    lines += per_task_stops(intervals) + margin_stops(tables) + bonferroni_intervals(tables) + missing_sensitivity(tables)
    lines += default_answers(tables) + invalid_kinds(items, replies) + yes_rates(tables) + pair_correctness(tables)
    lines += flips_at_risk(tables) + error_directions(tables) + ["### Accuracy per condition and task", "",
              "| Condition | " + " | ".join(tables) + " |", "| --- |" + " --- |" * len(tables)]
    for condition in Conditions:
        lines.append(f"| {condition} | " + " | ".join(accuracy_cell(table, condition) for table in tables.values()) + " |")
    lines += ["", "Cells: accuracy, then invalid and missing replies.", ""]
    lines += hue_analysis(tables, items) + middle_color_analysis(tables, items)
    lines += spatial_analysis(tables, items) + error_analysis(tables, items) + token_analysis(items, replies)
    return lines + (shared_color_analysis(tables, items) if "T4" in tables else [])


def bonferroni_intervals(tables):
    """Descriptive: every task's interval with a Bonferroni correction over all of a model's tests, both
    hypotheses at every distance and task, so that a result past where a fixed sequence stopped can be read
    on its own: an interval entirely above the margin even then holds at 2.5% for the model as a whole."""
    tests = 2 * len(Recolorings) * len(tables)
    z = NormalDist().inv_cdf(1 - 0.025 / tests)
    statistics = {task: item_statistics(table) for task, table in tables.items()}
    lines = [f"### Intervals with a Bonferroni correction over all {tests} tests (descriptive)", "",
             f"Each interval at one-sided {0.025 / tests:.3%} (z = {z:.2f}) instead of 2.5%.", ""]
    for kind in Kinds:
        lines += [f"| {kind.capitalize()} | " + " | ".join(tables) + " |", "| --- |" + " --- |" * len(tables)]
        for r in Recolorings:
            cells = [f"{pct(e)} [{pct(low)}, {pct(high)}]"
                     for e, low, high in (difference(*statistics[task][f"{kind}, {r}"], z) for task in tables)]
            lines.append(f"| {r} | " + " | ".join(cells) + " |")
        lines.append("")
    return lines


def margin_stops(tables):
    """Descriptive: where each sequence stops under other margins than the 5 points, read
    off the same intervals, so a reader can apply another tolerance."""
    lines = ["### The sequences under other margins (descriptive)", "",
             "| Margin | H1 | H2 |", "| --- | --- | --- |"]
    for margin in (0.025, 0.05, 0.10):
        h1, h2, _ = hypotheses(tables, margin)
        lines.append(f"| {margin * 100:g} pp | {summary(h1)} | {summary(h2)} |")
    return lines + [""]


def missing_sensitivity(tables):
    """If more than 2% of a condition's replies are missing, H1 and H2 again with every missing reply
    counted as invalid, so as wrong and as a flip (Method, Missing data); otherwise nothing."""
    shares = [float(np.isnan(table["answers"][c]).mean()) for table in tables.values() for c in Conditions]
    if max(shares) <= 0.02:
        return []
    worst = {task: {**table, "answers": {c: np.where(np.isnan(a), Invalid, a) for c, a in table["answers"].items()}}
             for task, table in tables.items()}
    h1, h2, _ = hypotheses(worst)
    return ["### Missing replies counted as wrong and as flips (sensitivity)", "",
            f"Up to {max(shares):.1%} of a condition's replies are missing.", "",
            f"- H1: {summary(h1)}", f"- H2: {summary(h2)}", ""]


def invalid_kinds(items, replies):
    """Descriptive: invalid replies by kind, with and without the image: truncated, blocked, or a finished
    reply with no answer line (which, without the image, is mostly a request for the image)."""
    counts = {"with image": Counter(), "without image": Counter()}
    for item in items:
        for condition in Conditions:
            reply = replies.get(f"{item['id']}-{condition}")
            if reply is None or score(item["task"], reply) != Invalid:
                continue
            kind = {"truncated": "truncated", "blocked": "blocked"}.get(reply["stop"], "no answer line")
            counts["without image" if condition == "no_image" else "with image"][kind] += 1
    lines = ["### Invalid replies by kind (descriptive)", "",
             "| Drawing | No answer line | Truncated | Blocked |", "| --- | --- | --- | --- |"]
    for where, c in counts.items():
        lines.append(f"| {where} | {c['no answer line']} | {c['truncated']} | {c['blocked']} |")
    return lines + [""]


def yes_rates(tables):
    """Descriptive: in T1 and T3, on the ladder palettes, how often the model says yes when the correct
    answer is yes (hits) and when it is no (false alarms), recolored and edited drawings together. Reading
    two colors as one raises false alarms only; a general tendency to say yes raises both."""
    lines = ["### Yes answers by correct answer on the ladder (descriptive)", "",
             "| Recoloring | T1, answer yes | T1, answer no | T3, answer yes | T3, answer no |", "| --- | --- | --- | --- | --- |"]
    for r in Ladder:
        cells = []
        for task in ("T1", "T3"):
            answers = np.concatenate([tables[task]["answers"][r], tables[task]["answers"][edited_twin(r)]])
            truths = np.concatenate([tables[task]["truth"], tables[task]["truth_edited"]])
            valid = ~np.isnan(answers) & (answers != Invalid)
            for target in (1.0, 0.0):
                chosen = valid & (truths == target)
                cells.append(pct(float((answers[chosen] == 1.0).mean())) if chosen.any() else "-")
        lines.append(f"| {r} | " + " | ".join(cells) + " |")
    return lines + ["", "Cells: share of valid answers that are yes.", ""]


def default_answers(tables):
    """Descriptive: the answers a model gives without the image, its default when it cannot see; a model
    that says yes by default could make false yes answers look like colors read as one."""
    lines = ["### Answers without the image (descriptive)", "",
             "| Task | Valid replies | Yes, or mean count |", "| --- | --- | --- |"]
    for task in tables:
        a = tables[task]["answers"]["no_image"]
        valid = a[~np.isnan(a) & (a != Invalid)]
        if len(valid) == 0:
            value = "-"
        elif task == "T2":
            value = f"{np.mean(valid):.1f}"
        else:
            value = pct(float(np.mean(valid)))
        lines.append(f"| {task} | {len(valid)} | {value} |")
    return lines + [""]


def pair_correctness(tables):
    """Descriptive: the share of items answered correctly on both the plain and the edited drawing in
    the same palette, so that two poor answers cannot cancel out (H2 compares the edited drawing with
    the original tab10 drawing instead). In tab10, the pair is the original and its edited twin."""
    lines = ["### Correct on both drawings of a same-palette pair (descriptive)", "",
             "95% Wilson intervals.", "", "| Palette | " + " | ".join(tables) + " |", "| --- |" + " --- |" * len(tables)]
    for plain, edited in (("original", "edited"),) + tuple((r, edited_twin(r)) for r in Ladder):
        cells = []
        for task in tables:
            both = accuracy_values(tables[task], plain) * accuracy_values(tables[task], edited)
            both = both[~np.isnan(both)]
            p, low, high = wilson(int(both.sum()), len(both))
            cells.append(f"{pct(p)} [{pct(low)}, {pct(high)}], n = {len(both)}")
        lines.append(f"| {'tab10' if plain == 'original' else plain} | " + " | ".join(cells) + " |")
    return lines + [""]


def per_task_stops(intervals):
    """Descriptive: the fixed sequence run on each task alone. The verdict needs every task, so this
    shows which task sets each model's distance."""
    lines = ["### Each task alone (descriptive)", "", "| Task | H1 alone | H2 alone |", "| --- | --- | --- |"]
    for task in intervals["excess flips, reassigned"]:
        cells = [summary(fixed_sequence((r, verdict([intervals[f"{kind}, {r}"][task][1:]])) for r in Recolorings))
                 for kind in Kinds]
        lines.append(f"| {task} | {cells[0]} | {cells[1]} |")
    return lines + ["", "The verdicts above need every task.", ""]


def flips_at_risk(tables):
    """Descriptive: excess flips only on the items at risk, where reading two adjacent colors as one
    changes the answer. In T1 and T3 those are the no items: on a yes item, the colors the answer turns
    on are the same color, so reading two colors as one changes nothing. In T2 every item is at risk, in
    T4 none. The verdicts use all items, so a T1 or T3 rate there is about half the rate at risk."""
    lines = ["### H1 excess flips on the items at risk, where reading two colors as one changes the answer (descriptive)", "",
             "T1 and T3: no items only; T2: all items.", "",
             "| Recoloring | T1 | T2 | T3 |", "| --- | --- | --- | --- |"]
    for r in Recolorings:
        cells = []
        for task in ColorTasks:
            x, y = item_statistics(tables[task])[f"excess flips, {r}"]
            at_risk = np.ones(len(x), bool) if task == "T2" else tables[task]["truth"] == 0.0
            e, low, high = difference(x[at_risk], y[at_risk])
            cells.append(f"{pct(e)} [{pct(low)}, {pct(high)}], n = {completed(x[at_risk], y[at_risk])}")
        lines.append(f"| {r} | " + " | ".join(cells) + " |")
    return lines + [""]


def error_directions(tables):
    """Exploratory: the direction of errors on the ladder, as a table (see error_direction_counts)."""
    lines = ["### Error directions on the ladder (exploratory)", "",
             "| Recoloring | False yes or overcount | False no or undercount | Invalid |", "| --- | --- | --- | --- |"]
    for r, counts in error_direction_counts(tables).items():
        lines.append(f"| {r} | {counts['toward one color']} | {counts['toward two colors']} | {counts['invalid']} |")
    return lines + [""]


def error_direction_counts(tables, tasks=ColorTasks):
    """Per ladder recoloring, wrong answers on the recolored and edited drawings of the given tasks by
    direction. A false
    yes (T1, T3) or an overcount (T2) is consistent with two colors read as one ("toward one color"), a
    false no or an undercount with one color read as two. The direction is observed; the cause is not,
    since counting, label or edge errors can point the same way."""
    directions = {}
    for r in Ladder:
        counts = Counter()
        for task in tasks:
            for condition, target in ((r, tables[task]["truth"]), (edited_twin(r), tables[task]["truth_edited"])):
                a = tables[task]["answers"][condition]
                for answer, truth in zip(a, target):
                    if np.isnan(answer) or answer == truth:
                        continue
                    if answer == Invalid:
                        counts["invalid"] += 1
                    elif (task == "T2" and answer > truth) or (task != "T2" and truth == 0.0):
                        counts["toward one color"] += 1
                    else:
                        counts["toward two colors"] += 1
        directions[r] = counts
    return directions


def pooled_accuracy(tables, condition):
    values = [np.nanmean(accuracy_values(tables[task], condition)) for task in ColorTasks]
    return pct(float(np.mean(values)))


def accuracy_values(table, condition):
    a = table["answers"][condition]
    target = table["truth_edited"] if is_edited(condition) else table["truth"]
    return np.where(np.isnan(a), np.nan, (a == target) * 1.0)


def repeat_flips(table):
    a = table["answers"]
    present = ~np.isnan(a["original"]) & ~np.isnan(a["repeat"])
    changed = (a["original"] != a["repeat"]) | (a["original"] == Invalid) | (a["repeat"] == Invalid)
    return float(changed[present].mean()) if present.any() else math.nan


def accuracy_cell(table, condition):
    values = accuracy_values(table, condition)
    a = table["answers"][condition]
    return f"{pct(float(np.nanmean(values)))} ({int((a == Invalid).sum())} inv, {int(np.isnan(a).sum())} miss)"


def hue_analysis(tables, items):
    """Exploratory: accuracy on each ladder distance by hue center, as a table (see hue_accuracy)."""
    lines = ["### Accuracy by hue center (exploratory)", "",
             "| Hue center | " + " | ".join(Ladder) + " |", "| --- |" + " --- |" * len(Ladder)]
    for center, row in hue_accuracy(tables, items).items():
        lines.append(f"| {center} | " + " | ".join(pct(row[r]) if row[r] is not None else "-" for r in Ladder) + " |")
    return lines + [""]


def hue_accuracy(tables, items):
    """Per hue center and ladder recoloring, accuracy pooling the recolored and the edited drawing (None
    without answers); the edit flips the answer, so each hue center gets yes and no answers equally often."""
    centers = sorted({item["hue_center"] for item in items})
    accuracy = {}
    for center in centers:
        accuracy[center] = {}
        for r in Ladder:
            values = []
            for task in ColorTasks:
                task_items = [item for item in items if item["task"] == task]
                for condition in (r, edited_twin(r)):
                    correct = accuracy_values(tables[task], condition)
                    values += [c for item, c in zip(task_items, correct) if item["hue_center"] == center and not np.isnan(c)]
            accuracy[center][r] = float(np.mean(values)) if values else None
    return accuracy


def middle_color_analysis(tables, items):
    """Exploratory: T2 accuracy on each ladder distance by u's color. The middle color of a ladder
    palette has an adjacent color on both sides, an outer color on one side only, so a model that
    confuses adjacent colors should miscount more often when u's color is the middle one."""
    task_items = [item for item in items if item["task"] == "T2"]
    middle = np.array([item["palette_position"][item["groups"][item["u"]]] == 1 for item in task_items])
    lines = ["### T2 accuracy by the position of u's color on the ladder (exploratory)", "",
             "| u's color | " + " | ".join(Ladder) + " | Items |", "| --- |" + " --- |" * (len(Ladder) + 1)]
    for name, rows in (("middle", middle), ("outer", ~middle)):
        cells = []
        for r in Ladder:
            values = np.concatenate([accuracy_values(tables["T2"], c)[rows] for c in (r, edited_twin(r))])
            cells.append(pct(float(np.nanmean(values))) if (~np.isnan(values)).any() else "-")
        lines.append(f"| {name} | " + " | ".join(cells) + f" | {int(rows.sum())} |")
    return lines + ["", "Each cell pools the recolored and the edited drawing.", ""]


def spatial_analysis(tables, items):
    """Exploratory: T1 accuracy by how far apart u and v sit in the drawing. For people, colors are
    harder to tell apart the farther apart they are (Brychtova and Coltekin, 2017). Counts only the T1
    drawings where u and v have adjacent, different colors: the plain drawing of a no item and the
    edited drawing of a yes item. Distances are in pixels, split into thirds."""
    task_items = [item for item in items if item["task"] == "T1"]
    scale = ImagePx / (2 * Limit)  # pixels per layout unit
    distance = np.array([math.dist(item["positions"][item["u"]], item["positions"][item["v"]]) * scale for item in task_items])
    cuts = np.quantile(distance, [1 / 3, 2 / 3])
    third = np.searchsorted(cuts, distance, side="right")
    no_item = tables["T1"]["truth"] == 0.0
    lines = ["### T1 accuracy by the spatial separation of u and v in the drawing (exploratory)", "",
             "Drawings where u and v have adjacent, different ladder colors.", "",
             "| Distance between u and v | " + " | ".join(Ladder) + " | Items |", "| --- |" + " --- |" * (len(Ladder) + 1)]
    for k in range(3):
        rows = third == k
        cells = []
        for r in Ladder:
            plain = accuracy_values(tables["T1"], r)[rows & no_item]
            edited = accuracy_values(tables["T1"], edited_twin(r))[rows & ~no_item]
            values = np.concatenate([plain, edited])
            cells.append(pct(float(np.nanmean(values))) if (~np.isnan(values)).any() else "-")
        label = f"{distance[rows].min():.0f} to {distance[rows].max():.0f} px"
        lines.append(f"| {label} | " + " | ".join(cells) + f" | {int(rows.sum())} |")
    return lines + [""]


def error_analysis(tables, items):
    """Exploratory: accuracy on the ladder drawings (recolored and edited, every distance) by drawing
    features. On tab10 every model is near 100%, so failures show only on the ladder."""
    rows = []
    for task in ColorTasks:
        task_items = [item for item in items if item["task"] == task]
        ladder = np.array([accuracy_values(tables[task], c) for r in Ladder for c in (r, edited_twin(r))])
        for i, item in enumerate(task_items):
            values = ladder[:, i][~np.isnan(ladder[:, i])]
            rows.append({
                "task": task, "nodes": item["nodes"], "edge band": item["band"],
                "crossings": crossing_bin(item["crossings"]), "edited node degree": min(item["edited_node_degree"], 5),
                "accuracy": float(values.mean()) if len(values) else None,
            })
    lines = ["### Error analysis on the ladder (exploratory)", ""]
    for factor in ("nodes", "edge band", "crossings", "edited node degree"):
        lines += [f"| {factor} | Accuracy | Items |", "| --- | --- | --- |"]
        # Bands in the generator's order; numbers by the leading one, so the crossing bins read 0, 1-2, 3-5, 6+.
        levels = Bands if factor == "edge band" else sorted({row[factor] for row in rows},
                                                            key=lambda level: int(re.match(r"\d+", str(level)).group()))
        for level in levels:
            group = [row["accuracy"] for row in rows if row[factor] == level and row["accuracy"] is not None]
            lines.append(f"| {level} | {pct(float(np.mean(group))) if group else '-'} | {len(group)} |")
        lines.append("")
    return lines


def token_analysis(items, replies):
    """Exploratory and correlational: accuracy on the ladder drawings (recolored and edited) by the
    reply's output tokens, reasoning included, in quartiles of this model's ladder replies. Harder
    drawings may draw longer reasoning, so this cannot show whether reasoning helps."""
    tokens, correct = [], []
    for item in (item for item in items if item["task"] in ColorTasks):
        for r in Ladder:
            for condition in (r, edited_twin(r)):
                reply = replies.get(f"{item['id']}-{condition}")
                if reply is None or reply.get("output_tokens") is None:
                    continue
                truth = encode(item["edited_answer"] if is_edited(condition) else item["answer"])
                tokens.append(reply["output_tokens"])
                correct.append(score(item["task"], reply) == truth)
    if not tokens:
        return []
    tokens, correct = np.array(tokens), np.array(correct)
    edges = np.quantile(tokens, [0, 0.25, 0.5, 0.75, 1])
    quartile = np.minimum(np.searchsorted(edges, tokens, side="right") - 1, 3)
    lines = ["### Accuracy on the ladder by output tokens (exploratory)", "",
             "| Output tokens | Accuracy | Replies |", "| --- | --- | --- |"]
    for q in range(4):
        rows = quartile == q
        if rows.any():
            lines.append(f"| {tokens[rows].min()} to {tokens[rows].max()} | {pct(float(correct[rows].mean()))} | {int(rows.sum())} |")
    return lines + ["", "Rows are quartiles of this model's ladder replies; tied token counts share a row.", ""]


def shared_color_analysis(tables, items):
    """Exploratory: T4 yes answers by edge and shared color, as a table (see shared_color_rates)."""
    lines = ["### T4 yes answers by edge and shared color (exploratory)", "",
             "| Palette | No edge, shared color | No edge, other colors | Edge, shared color | Edge, other colors |",
             "| --- | --- | --- | --- | --- |"]
    for palette, rates in shared_color_rates(tables, items).items():
        lines.append(f"| {palette} | " + " | ".join("-" if rate is None else pct(rate) for rate in rates.values()) + " |")
    return lines + ["", "Cells: share of valid answers that are yes. tab10 pools the original, reassigned and edited drawings.", ""]


SharedCells = ((False, True), (False, False), (True, True), (True, False))  # (edge, shared color)


def shared_color_rates(tables, items):
    """Per palette, the share of valid T4 answers that are yes in each cell of SharedCells (None
    without answers). The edit switches whether u and v share a color, never the edge, so a model
    whose reading of edges follows the colors says yes more often when they share one."""
    task_items = [item for item in items if item["task"] == "T4"]
    shared = np.array([item["groups"][item["u"]] == item["groups"][item["v"]] for item in task_items])
    edge = tables["T4"]["truth"] == 1.0
    palettes = [("tab10", ("original", "reassigned", "edited"))] + [(r, (r, edited_twin(r))) for r in Ladder]
    rates = {}
    for name, conditions in palettes:
        answers = np.concatenate([tables["T4"]["answers"][c] for c in conditions])
        same = np.concatenate([shared != is_edited(c) for c in conditions])
        joined = np.tile(edge, len(conditions))
        valid = ~np.isnan(answers) & (answers != Invalid)
        rates[name] = {}
        for cell in SharedCells:
            chosen = valid & (joined == cell[0]) & (same == cell[1])
            rates[name][cell] = float((answers[chosen] == 1.0).mean()) if chosen.any() else None
    return rates


def crossing_bin(count):
    return "0" if count == 0 else "1-2" if count <= 2 else "3-5" if count <= 5 else "6+"


def pct(x):
    return "-" if isinstance(x, float) and math.isnan(x) else f"{100 * x:.1f}%"


def distinct_replies(rows):
    """Every distinct (task, stop, reply text) once, most frequent first, for hand coding."""
    counts = Counter((r["task"], r["stop"], r["reply"]) for r in rows if r["reply"] is not None)
    parsed = {(r["task"], r["stop"], r["reply"]): r["parsed"] for r in rows if r["reply"] is not None}
    return [{"task": task, "stop": stop, "reply": reply, "count": n, "parsed": parsed[(task, stop, reply)], "hand_coded": ""}
            for (task, stop, reply), n in sorted(counts.items(), key=lambda kv: (kv[0][0], -kv[1]))]


def hand_coding_report(distinct, missing, path):
    """Compares the hand coding in hand_coding.csv, if it exists, with the parser, text by text."""
    if not path.exists():
        return []
    with open(path, newline="") as f:
        coded = {(r["task"], r["stop"], r["reply"]): r["hand_coded"].strip().lower()
                 for r in csv.DictReader(f) if r["hand_coded"].strip()}
    parsed = {(r["task"], r["stop"], r["reply"]): r["parsed"] for r in distinct}
    uncoded = set(parsed) - set(coded)
    disagree = [key for key, value in coded.items() if key in parsed and hand_answer(value) != parsed[key]]
    passes = not uncoded and not disagree and not missing
    lines = ["## Parser against hand coding", "",
             f"{len(set(parsed) & set(coded))} of {len(parsed)} distinct replies hand coded, {len(uncoded)} not yet; "
             f"{len(disagree)} disagree with the parser; {missing} queries have no reply. "
             f"The parser check {'passes' if passes else 'does not pass yet'}.", ""]
    lines += [f"- {task}, {stop}: {reply[:80]!r}: hand coded {coded[(task, stop, reply)]}, parsed {parsed[(task, stop, reply)]}"
              for task, stop, reply in disagree]
    return lines + [""]


def hand_answer(value):
    """A hand-coded answer in the parser's encoding: yes, no, invalid or a number."""
    words = {"yes": 1.0, "no": 0.0, "invalid": Invalid}
    return words[value] if value in words else float(value)


def parsed_rows(model, items, replies):
    rows = []
    for item in items:
        for condition in Conditions:
            reply = replies.get(f"{item['id']}-{condition}")
            rows.append({
                "model": model, "query_id": f"{item['id']}-{condition}", "task": item["task"],
                "reply": None if reply is None else reply["text"],
                "stop": None if reply is None else reply["stop"],
                "parsed": None if reply is None else score(item["task"], reply),
            })
    return rows


if __name__ == "__main__":
    main()
