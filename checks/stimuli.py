"""Reproduces the stimulus numbers in the thesis: palette distances and their CIEDE2000 implementation
against published reference data, the closest pairs of matplotlib's qualitative palettes (Table 2.1),
acceptance rates, crossings, answer balance, how far apart T4's node pairs sit, pilot error directions,
how much of a node the label covers, and the JPEG re-encoding check.

Run from the repository root: uv run checks/stimuli.py

Reads manifests, main images and parsed pilot replies. Sends no queries and writes no files.
The JPEG experiment runs entirely in memory and does not claim to reproduce provider processing.
"""

import csv
import io
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np
from PIL import Image

Root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Root / "study"))
import generate
import colour


def main():
    main_items = read_jsonl(Root / "data/main/manifest.jsonl")
    rejections = read_jsonl(Root / "data/main/rejections.jsonl")
    pilot_items = read_jsonl(Root / "data/pilot/manifest.jsonl")
    validate_items(main_items)
    palette_measurements()
    common_palettes()
    sampling_measurements(main_items, rejections)
    drawing_measurements(main_items)
    error_labels(pilot_items)
    label_coverage(main_items)
    jpeg_measurements(main_items)


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def validate_items(items):
    violations = []
    for item in items:
        u, v = item["u"], item["v"]
        for distance in generate.Distances:
            palette = generate.LadderPalettes[item["hue_center"], distance]
            expected = [palette[position] for position in item["palette_position"]]
            if item["palettes"][f"d{distance}"] != expected:
                violations.append((item["id"], distance, "manifest palette differs from code"))
        neighbors = {b if a == u else a for a, b in item["edge_list"] if u in (a, b)}
        for condition in generate.ImageConditions:
            colors = generate.node_colors(item, condition)
            if item["task"] == "T1":
                answer = "yes" if colors[u] == colors[v] else "no"
            elif item["task"] == "T2":
                answer = sum(color == colors[u] for color in colors.values())
            elif item["task"] == "T3":
                answer = "yes" if any(colors[node] == colors[u] for node in neighbors) else "no"
            else:
                answer = "yes" if v in neighbors else "no"
            edited = condition.endswith("edited")
            truth = item["edited_answer"] if edited else item["answer"]
            if answer != truth:
                violations.append((item["id"], condition, "incorrect truth"))
            if edited:
                base = "original" if condition == "edited" else condition.removesuffix("-edited")
                before = generate.node_colors(item, base)
                if sum(colors[node] != before[node] for node in colors) != 1:
                    violations.append((item["id"], condition, "edit changes other than one node"))
                if min(Counter(colors.values()).values()) < 2:
                    violations.append((item["id"], condition, "group below two nodes"))
        positions = item["positions"]
        for a, b in combinations(positions, 2):
            if math.dist(positions[a], positions[b]) < 3 * generate.NodeRadius:
                violations.append((item["id"], "nodes too close"))
        for a, b in item["edge_list"]:
            for node in positions:
                if node not in (a, b) and generate.segment_distance(
                    positions[node], positions[a], positions[b]
                ) < 2 * generate.NodeRadius:
                    violations.append((item["id"], "edge too close"))
    print("Main items:", len(items), "violations:", violations)
    for task in generate.Tasks:
        subset = [item for item in items if item["task"] == task]
        print(task, "answer cells", set(Counter(
            (item["nodes"], item["band"], item["answer"]) for item in subset
        ).values()), "hues", dict(Counter(item["hue_center"] for item in subset)))


def palette_measurements():
    print("colour version", colour.__version__)
    # Sharma/Wu/Dalal's published numerical reference data, downloaded 2026-10-08:
    # https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/dataNprograms/ciede2000testdata.txt
    reference = np.loadtxt(Root / "checks/ciede2000-reference.txt")
    error = max(abs(generate.ciede2000(row[:3], row[3:6]) - row[6]) for row in reference)
    print("Published CIEDE2000 reference cases", len(reference), "max error", error,
          "within published rounding", error < 0.00005)
    for a, b in combinations(generate.Tab10, 2):
        print("tab10 pair", a, b, generate.ciede2000(generate.hex_to_lab(a), generate.hex_to_lab(b)))
    for color in generate.Tab10:
        lab = generate.hex_to_lab(color)
        print("tab10 L,C", color, lab[0], np.hypot(*lab[1:]))
    labs = []
    for distance in generate.Distances:
        adjacent, outer = [], []
        for center in generate.HueCenters:
            palette = generate.LadderPalettes[center, distance]
            values = [generate.hex_to_lab(color) for color in palette]
            labs.extend(values)
            adjacent.extend(generate.ciede2000(values[k], values[1]) for k in (0, 2))
            outer.append(generate.ciede2000(values[0], values[2]))
        print("ladder", distance, "adjacent", min(adjacent), max(adjacent),
              "outer", min(outer), max(outer))
    print("actual ladder L", min(lab[0] for lab in labs), max(lab[0] for lab in labs))
    print("actual ladder C", min(np.hypot(*lab[1:]) for lab in labs),
          max(np.hypot(*lab[1:]) for lab in labs))
    hues = np.radians(np.linspace(0, 360, 36001))
    circle = np.stack((np.full_like(hues, generate.Lightness),
                       generate.Chroma * np.cos(hues), generate.Chroma * np.sin(hues)), axis=1)
    rgb = colour.XYZ_to_sRGB(colour.Lab_to_XYZ(circle))
    print("fixed LCh circle RGB channel extrema", rgb.min(axis=0), rgb.max(axis=0))


def common_palettes():
    """The closest pair of colors in each of matplotlib's qualitative palettes, with all colors in use."""
    from matplotlib import colormaps
    from matplotlib.colors import ListedColormap, to_hex
    names = sorted(name for name, cmap in colormaps.items()
                   if isinstance(cmap, ListedColormap) and cmap.N <= 20 and not name.endswith("_r"))
    for name in names:
        colors = [to_hex(c) for c in colormaps[name].colors]
        distance, a, b = min((generate.ciede2000(generate.hex_to_lab(a), generate.hex_to_lab(b)), a, b)
                             for a, b in combinations(colors, 2))
        print("palette", name, len(colors), "closest pair", round(distance, 1), a, b)


def sampling_measurements(items, rejections):
    print("Main accepted", len(items), "rejected", len(rejections),
          "reasons", dict(Counter(item["reason"] for item in rejections)))
    for n in generate.NodeCounts:
        for band in generate.Bands:
            accepted = Counter(item["edges"] for item in items
                               if item["nodes"] == n and item["band"] == band)
            rejected = Counter(item["edges"] for item in rejections
                               if item["nodes"] == n and item["band"] == band)
            low, high = generate.edge_range(n, band)
            print("edge cell", n, band, [(m, accepted[m], accepted[m] + rejected[m],
                  round(accepted[m] / (accepted[m] + rejected[m]), 3)) for m in range(low, high + 1)])
    flexible, forced = Counter(), Counter()
    for item in items:
        if item["task"] != "T2":
            continue
        groups, positions = item["groups"], item["palette_position"]
        home = groups[item["u"]]
        sizes = Counter(groups.values())
        up = any(generate.adjacent(group, home, positions) and sizes[group] >= 3 for group in sizes)
        down = sizes[home] >= 3
        direction = "up" if item["edited_answer"] > item["answer"] else "down"
        (flexible if up and down else forced)[direction] += 1
    print("T2 flexible directions", dict(flexible), "forced", dict(forced))
    t2 = [item for item in items if item["task"] == "T2"]
    print("T2 edited answer distribution", dict(Counter(item["edited_answer"] for item in t2)))
    no_items = [item for item in items if item["task"] == "T3" and item["answer"] == "no"]
    outer_neighbors = 0
    for item in no_items:
        u = item["u"]
        home = item["groups"][u]
        positions = item["palette_position"]
        neighbors = {b if a == u else a for a, b in item["edge_list"] if u in (a, b)}
        outer_neighbors += any(abs(positions[home] - positions[item["groups"][node]]) == 2
                               for node in neighbors)
    print("T3 original no items with outer-color neighbors", outer_neighbors, "of", len(no_items))


def drawing_measurements(items):
    crossings = Counter(item["crossings"] for item in items)
    print("crossing-free drawings", crossings[0], "of", len(items),
          "six or more crossings", sum(n for count, n in crossings.items() if count >= 6))
    to_px = generate.ImagePx / (2 * generate.Limit)  # layout units to pixels
    for answer in ("yes", "no"):
        distances = [math.dist(item["positions"][item["u"]], item["positions"][item["v"]]) * to_px
                     for item in items if item["task"] == "T4" and item["answer"] == answer]
        print("T4 pairs with answer", answer, "median distance in px", round(statistics.median(distances)))


def error_labels(items):
    by_id = {item["id"]: item for item in items}
    counts = defaultdict(Counter)
    examples = []
    for row in csv.DictReader((Root / "data/pilot/parsed.csv").open()):
        if row["task"] != "T2":
            continue
        parts = row["query_id"].split("-")
        condition = "-".join(parts[3:])
        if not condition.startswith("d"):
            continue
        item = by_id["-".join(parts[:3])]
        groups = dict(item["groups"])
        if condition.endswith("edited"):
            groups[item["edited_node"]] = item["edited_group"]
        home = groups[item["u"]]
        sizes = Counter(groups.values())
        truth, answer = sizes[home], float(row["parsed"])
        if answer <= truth:
            continue
        other = [group for group in sizes if group != home]
        possible = {truth}
        for n in range(1, len(other) + 1):
            possible.update(truth + sum(sizes[group] for group in subset)
                            for subset in combinations(other, n))
        counts[row["model"]]["overcounts"] += 1
        counts[row["model"]]["overcount_by_one"] += answer == truth + 1
        if answer not in possible:
            counts[row["model"]]["incompatible_complete_group_merge"] += 1
            if len(examples) < 5:
                examples.append((row["model"], row["query_id"], truth, answer, dict(sizes)))
    print("T2 overcount classification", {model: dict(count) for model, count in counts.items()})
    print("Examples", examples)


def node_window(item, node):
    """The rows and columns of the image around a node, and its center in pixels."""
    x, y = item["positions"][node]
    cx = (x + generate.Limit) / (2 * generate.Limit) * generate.ImagePx
    cy = (generate.Limit - y) / (2 * generate.Limit) * generate.ImagePx
    return (math.floor(cy - 24), math.floor(cy + 25)), (math.floor(cx - 24), math.floor(cx + 25)), (cx, cy)


def label_coverage(items):
    """The share of a node's interior that the label and its white halo cover. The interior ends at the
    black outline, 1 point (1.39 px) wide around the 24 px radius, so at 23.3 px; the label lies well
    within 22 px, where no outline antialiasing reaches, and covers the pixels there that are not the
    pure fill color."""
    inner = 24 - 0.5 * 100 / 72
    shares = []
    for item in items:
        pixels = np.asarray(Image.open(Root / "data/main" / item["images"]["original"]).convert("RGB"))
        for node, color in generate.node_colors(item, "original").items():
            (r0, r1), (c0, c1), (cx, cy) = node_window(item, node)
            rows, cols = np.mgrid[r0:r1, c0:c1]
            radius = np.hypot(cols + 0.5 - cx, rows + 0.5 - cy)
            fill = np.array([int(color[i:i + 2], 16) for i in (1, 3, 5)])
            covered = ~(pixels[r0:r1, c0:c1] == fill).all(axis=2)
            shares.append((covered[radius <= 22].sum() / (radius <= inner).sum(), node))
    print("label and halo cover", min(shares), "to", max(shares), "of a node's interior")


def jpeg_measurements(items):
    distances = defaultdict(list)
    max_shift = (0, None)
    for item in items:
        for distance in generate.Distances:
            condition = f"d{distance}"
            original = Image.open(Root / "data/main" / item["images"][condition]).convert("RGB")
            encoded = io.BytesIO()
            original.save(encoded, format="JPEG", quality=75, subsampling=2)
            encoded.seek(0)
            compressed, source = np.asarray(Image.open(encoded)), np.asarray(original)
            means = {}
            for node, color in generate.node_colors(item, condition).items():
                (r0, r1), (c0, c1), _ = node_window(item, node)
                fill = np.array([int(color[i:i + 2], 16) for i in (1, 3, 5)])
                mask = (source[r0:r1, c0:c1] == fill).all(axis=2)
                mean = compressed[r0:r1, c0:c1][mask].mean(axis=0) / 255
                means[node] = colour.XYZ_to_Lab(colour.sRGB_to_XYZ(mean))
                shift = generate.ciede2000(means[node], generate.hex_to_lab(color))
                if shift > max_shift[0]:
                    max_shift = shift, (item["id"], condition, node)
            for a, b in combinations(item["groups"], 2):
                if generate.adjacent(item["groups"][a], item["groups"][b], item["palette_position"]):
                    distances[distance].append(generate.ciede2000(means[a], means[b]))
    print("JPEG Q75 4:2:0, average of originally exact fill pixels, max node shift", max_shift)
    for distance, values in distances.items():
        print("JPEG adjacent node-mean distances", distance, min(values), max(values),
              "mean", statistics.mean(values), "n", len(values))


if __name__ == "__main__":
    main()
