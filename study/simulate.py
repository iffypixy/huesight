"""Runs the analysis (analyze.py) on simulated models with known behavior.

It backs the numbers of the thesis's Method (Margin and sample size) and its Simulation appendix:
how often the fixed sequence stops at the distance where a model's answers break down, at 300
items per task; how often a model exactly at the margin is wrongly supported or rejected; and how
often a model with a small real loss inside the margin is supported. A simulated breakdown is
directional, as most pilot errors were: yes where the answer is no (T1, T3), or one node too many
(T2). It never touches T4, whose answer does not depend on the colors. It is an error model, not a
claim about how a model perceives colors.

Run: uv run study/simulate.py   (about ten minutes; the seed is fixed, so the output is too)
"""

import math
from collections import Counter

import numpy as np

import analyze

Items = 300
Runs = 1000
MarginRuns = 5000


def main():
    rng = np.random.default_rng(0)
    exact, calm = error_for_repeat_flips(0.0), error_for_repeat_flips(0.01)
    scenarios = (
        ("reads every distance, no repeat flips", model(exact), Runs),
        ("reads every distance, 1% repeat flips (the pilots had 0% to 1.7%)", model(calm), Runs),
        ("reads every distance, 3% repeat flips", model(error_for_repeat_flips(0.03)), Runs),
        ("reads every distance, 10% repeat flips", model(error_for_repeat_flips(0.10)), Runs),
        ("breaks down from 7 units down (10%, 20%, 40% directional errors)", model(calm, merges={"d7": 0.10, "d5": 0.20, "d3": 0.40}), Runs),
        ("breaks down gradually (0.5%, 1.5%, 4%, 8%, 15%, 30% directional errors from 20 to 3 units)",
         model(calm, merges={"d20": 0.005, "d14": 0.015, "d10": 0.04, "d7": 0.08, "d5": 0.15, "d3": 0.30}), Runs),
        ("T2 exactly at the H1 margin at d10, no repeat flips", model(exact, loss_at="d10", loss_tasks=("T2",)), MarginRuns),
        ("T2 exactly at the H1 margin at d10, 1% repeat flips", model(calm, loss_at="d10", loss_tasks=("T2",)), MarginRuns),
        ("every task exactly at the H1 margin at d10, no repeat flips", model(exact, loss_at="d10"), MarginRuns),
    ) + tuple(
        (f"a real H1 loss of {loss:.0%} in every task at d10, inside the margin, no repeat flips",
         model(exact, loss_at="d10", loss=loss), Runs) for loss in (0.01, 0.02, 0.03, 0.04)
    ) + (
        ("T2 exactly at the H2 margin at d10, no repeat flips", model(exact, loss_at="d10", loss_tasks=("T2",), loss_in="edited"), MarginRuns),
    )
    print(f"{Runs} runs per scenario ({MarginRuns} at the margin), {Items} items per task, margin {analyze.Margin:.0%}")
    for name, simulated, runs in scenarios:
        h1, h2 = Counter(), Counter()
        for _ in range(runs):
            a, b, _ = analyze.hypotheses(simulated_tables(simulated, rng))
            h1[analyze.summary(a)] += 1
            h2[analyze.summary(b)] += 1
        print(name)
        for label, counts in (("H1", h1), ("H2", h2)):
            print(f"  {label}: " + "; ".join(f"{k} {share(v, runs)}" for k, v in counts.most_common()))


def error_for_repeat_flips(rate):
    """Per-query error that makes two answers to the identical drawing differ at this rate on yes/no tasks."""
    return (1 - math.sqrt(1 - 2 * rate)) / 2


def share(count, runs):
    """A Monte Carlo rate with its 95% Wilson interval."""
    p, low, high = analyze.wilson(count, runs)
    return f"{p:.1%} [{low:.1%}, {high:.1%}]"


def simulated_tables(simulated, rng):
    """Answer tables in the format analyze.py reads from real replies; the no-image condition stays missing."""
    tables = {}
    for task in analyze.Tasks:
        if task == "T2":
            truth = rng.integers(2, 7, Items)
            # An edit moves one node into or out of u's group; a group of two cannot lose a node.
            truth_edited = truth + np.where(truth == 2, 1, rng.choice([-1, 1], Items))
        else:
            truth = rng.integers(0, 2, Items)
            truth_edited = truth if task == "T4" else 1 - truth  # T4's edit keeps the answer
        answers = {c: np.full(Items, analyze.Missing) for c in analyze.Conditions}
        answers.update(simulated(task, truth, truth_edited, rng))
        tables[task] = {"truth": truth * 1.0, "truth_edited": truth_edited * 1.0,
                        "answers": {c: answers[c] * 1.0 for c in analyze.Conditions}}
    return tables


def model(error, merges=None, loss_at=None, loss=analyze.Margin, loss_tasks=analyze.Tasks, loss_in="recolored"):
    """A simulated model. Every query is answered on its own and is wrong with probability `error`.
    At a distance in `merges`, that share of the recolored and edited drawings whose answer depends on
    telling the adjacent colors apart gets a directional error. At `loss_at`, in the tasks given,
    the model loses exactly `loss` (by default the margin): as excess flips of the recolored drawing
    (H1), or as wrong answers to the edited drawing (H2)."""
    merges = merges or {}

    def simulated(task, truth, truth_edited, rng):
        a = {"original": answer(task, truth, rng.random(Items) >= error, rng),
             "repeat": answer(task, truth, rng.random(Items) >= error, rng)}
        for r in analyze.Recolorings:
            twin = analyze.edited_twin(r)
            a[r] = answer(task, truth, rng.random(Items) >= error, rng)
            a[twin] = answer(task, truth_edited, rng.random(Items) >= error, rng)
            if r in merges:
                a[r] = merge(task, truth, a[r], merges[r], rng)
                a[twin] = merge(task, truth_edited, a[twin], merges[r], rng)
            if r == loss_at and task in loss_tasks and loss_in == "recolored":
                forced = rng.random(Items) < loss / (1 - repeat_flip_rate(task, error))
                a[r] = np.where(forced, different_answer(task, a["original"], rng), a[r])
            if r == loss_at and task in loss_tasks and loss_in == "edited":
                forced = rng.random(Items) < loss / (1 - error) ** 2
                a[twin] = np.where(forced, different_answer(task, truth_edited, rng), a[twin])
        return a
    return simulated


def merge(task, truth, given, rate, rng):
    """With probability `rate`, a directional error: yes where the answer is no (T1, T3), one node too
    many (T2). Yes items cannot get this error, and neither can T4, whose answer is an edge."""
    if task == "T4":
        return given
    hit = rng.random(len(truth)) < rate
    if task == "T2":
        return np.where(hit, truth + 1, given)
    return np.where(hit & (truth == 0), 1, given)


def answer(task, truth, correct, rng):
    return np.where(correct, truth, different_answer(task, truth, rng))


def different_answer(task, given, rng):
    """Yes/no tasks have one other answer; on T2 a wrong count is off by one."""
    if task == "T2":
        return given + rng.choice([-1, 1], len(given))
    return 1 - given


def repeat_flip_rate(task, error):
    """Chance that two independent answers with this error rate differ."""
    if task == "T2":
        return 1 - (1 - error) ** 2 - error ** 2 / 2  # two wrong counts agree half the time
    return 2 * error * (1 - error)


if __name__ == "__main__":
    main()
