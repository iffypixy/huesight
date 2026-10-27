"""Generates the study items: graph drawings with known answers, drawn in every image condition.

Implements the Stimuli, Tasks and Conditions of the thesis's Method chapter. Everything follows
from the set's seed, so the same code and seed give the same items.

Run: uv run study/generate.py pilot   (then: main)
Writes data/<set>/manifest.jsonl (one item per line), data/<set>/rejections.jsonl (every
rejected draw) and data/<set>/images/<item id>/<condition>.png. The manifests are committed and
the images are not, so on a clone it draws the images again, after checking that the manifests
are the ones the code generates.
"""

import json
import math
import random
import sys
import warnings
from itertools import combinations
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import Circle

with warnings.catch_warnings():
    warnings.simplefilter("ignore")  # colour-science warns that SciPy is missing; CIEDE2000 does not need it
    import colour

Data = Path(__file__).resolve().parent.parent / "data"
# T1 to T3 ask about the colors; T4, the control, asks about an edge, so no drawing of an item changes its
# answer. The pilot calibrated the colors and so asked only T1 to T3.
Tasks = ("T1", "T2", "T3", "T4")
Sets = {"pilot": {"seed": 3, "items_per_task": 20, "tasks": Tasks[:3]},
        "main": {"seed": 2, "items_per_task": 300, "tasks": Tasks}}

Prompts = {
    "T1": "In this graph drawing, do nodes {u} and {v} have the same color? Answer with yes or no only.",
    "T2": "In this graph drawing, how many nodes have the same color as node {u}, including {u} itself? "
          "Answer with a single number only.",
    "T3": "In this graph drawing, is node {u} connected by an edge to any node of the same color? "
          "Answer with yes or no only.",
    "T4": "In this graph drawing, is there an edge between nodes {u} and {v}? Answer with yes or no only.",
}
Answers = {"T1": ["yes", "no"], "T2": [2, 3, 4, 5, 6], "T3": ["yes", "no"], "T4": ["yes", "no"]}
NodeCounts = (10, 11, 12)
Bands = ("sparse", "dense")
Groups = 3

Tab10 = ("#1f77b4", "#ff7f0e", "#2ca02c")  # matplotlib tab:blue, tab:orange, tab:green
Derangements = ((1, 2, 0), (2, 0, 1))  # the two ways to move every group to another tab10 hue
# The distance ladder (Method, Palettes): three colors of equal lightness and chroma around one hue center,
# each outer color this many CIEDE2000 units from the middle one, up to 0.4 more after 8-bit rounding.
# Only hue differs.
Distances = (20, 14, 10, 7, 5, 3)
HueCenters = (235, 295, 355, 55, 115, 175)  # six centers 60 degrees apart, balanced over items
Lightness, Chroma = 65, 35
ImageConditions = ("original", "reassigned", "edited") + tuple(
    condition for d in Distances for condition in (f"d{d}", f"d{d}-edited"))

ImagePx = 768
Dpi = 100
Limit = 1.15  # axis limits in layout units; spring_layout keeps positions within [-1, 1]
NodeRadius = 24 / ImagePx * 2 * Limit  # 24 px, in layout units
EdgeColor = "#888888"


def main():
    name = sys.argv[1] if len(sys.argv) == 2 else None
    if name not in Sets:
        sys.exit("usage: uv run study/generate.py pilot|main")
    out = Data / name
    items, rejections = make_items(name, **Sets[name])
    if name == "main":
        check_disjoint(items, sorted(Data.glob("pilot*/manifest.jsonl")))
    write_set(out, items, rejections)
    print(f"wrote {len(items)} items and {len(rejections)} rejected draws to {out}")


def make_items(name, seed, items_per_task, tasks=Tasks):
    """Returns the items of one set and the log of rejected draws. Tasks are drawn in order from one
    random stream, so a task added at the end leaves the items of the tasks before it unchanged."""
    rng = random.Random(seed)
    items = []
    rejections = []
    t2_directions = {"up": 0, "down": 0}
    for task in tasks:
        chosen = targets(task, items_per_task, rng)
        shared = shared_colors(chosen, rng) if task == "T4" else [None] * len(chosen)
        for index, ((n, band, answer, hue_center), same) in enumerate(zip(chosen, shared)):
            item = make_item(task, n, band, answer, hue_center, same, rng, rejections, t2_directions)
            items.append({"id": f"{name}-{task}-{index:03d}", **item})
    return items, rejections


def targets(task, count, rng):
    """(node count, band, correct answer, hue center) for each item of a task, in random order.

    Answers are balanced within each node count and band. When the count does not allow that
    (the pilot's 20 items), the remaining items go to the cells in turn, with answers balanced overall.
    Hue centers are balanced over the task's items, independently of the rest.
    """
    cells = [(n, band) for n in NodeCounts for band in Bands]
    answers = Answers[task]
    full, rest = divmod(count, len(cells) * len(answers))
    chosen = [(n, band, answer) for n, band in cells for answer in answers] * full
    rest_answers = [answers[i % len(answers)] for i in range(rest)]
    rng.shuffle(rest_answers)
    chosen += [(*cells[i % len(cells)], answer) for i, answer in enumerate(rest_answers)]
    rng.shuffle(chosen)
    centers = [HueCenters[i % len(HueCenters)] for i in range(count)]
    rng.shuffle(centers)
    return [(*target, center) for target, center in zip(chosen, centers)]


def shared_colors(chosen, rng):
    """T4: whether u and v share a color, in exactly half the items with an edge and half without, so
    that sharing a color and having an edge are independent."""
    shared = [False] * len(chosen)
    for answer in Answers["T4"]:
        indices = [i for i, target in enumerate(chosen) if target[2] == answer]
        rng.shuffle(indices)
        for i in indices[:len(indices) // 2]:
            shared[i] = True
    return shared


def make_item(task, n, band, answer, hue_center, shared, rng, rejections, t2_directions):
    """Draws graphs until one has an unambiguous drawing and a valid question with the target answer."""
    low, high = edge_range(n, band)
    while True:
        m = rng.randint(low, high)
        g = random_connected_graph(n, m, rng)
        layout_seed = rng.randrange(2**32)
        pos = {node: (float(x), float(y)) for node, (x, y) in nx.spring_layout(g, seed=layout_seed).items()}
        problem = drawing_problem(g, pos)
        question = None
        if problem is None:
            # Which ladder color each group gets: the middle color's group is adjacent to both others.
            position = rng.sample(range(Groups), Groups)
            if task == "T1":
                question = same_color_question(g, answer, rng, position)
            elif task == "T2":
                question = group_size_question(g, answer, rng, t2_directions, position)
            elif task == "T3":
                question = neighbor_question(g, answer, rng, position)
            else:
                question = edge_question(g, answer, shared, rng, position)
            if question is None:
                problem = "no valid question for the target answer"
        if problem:
            rejections.append({"task": task, "nodes": n, "band": band, "edges": m,
                               "layout_seed": layout_seed, "reason": problem})
            continue
        return record(task, g, pos, band, layout_seed, answer, hue_center, position, rng, **question)


def edge_range(n, band):
    """Sparse graphs have n to 1.3n edges, dense ones 1.4n to 1.8n, rounded inward."""
    if band == "sparse":
        return n, 13 * n // 10
    return -(-14 * n // 10), 18 * n // 10


def random_connected_graph(n, m, rng):
    """Uniform over connected graphs with n nodes and m edges, by rejection."""
    while True:
        g = nx.gnm_random_graph(n, m, seed=rng.randrange(2**32))
        if nx.is_connected(g):
            return g


def drawing_problem(g, pos):
    """Why the drawing is ambiguous, or None: node centers at least 3 radii apart, and no edge
    within 2 radii of a node it does not join (Method, Layout)."""
    for a, b in combinations(g, 2):
        if math.dist(pos[a], pos[b]) < 3 * NodeRadius:
            return "nodes too close"
    for a, b in g.edges:
        for w in g:
            if w not in (a, b) and segment_distance(pos[w], pos[a], pos[b]) < 2 * NodeRadius:
                return "edge too close to a node"
    return None


def segment_distance(p, a, b):
    ab = (b[0] - a[0], b[1] - a[1])
    t = ((p[0] - a[0]) * ab[0] + (p[1] - a[1]) * ab[1]) / (ab[0] ** 2 + ab[1] ** 2)
    t = min(1.0, max(0.0, t))
    return math.dist(p, (a[0] + t * ab[0], a[1] + t * ab[1]))


# Every question and edit involves adjacent groups, so on a ladder palette the colors an answer
# turns on are the ladder distance apart. The outer pair (1.56 to 2.16 times as far) can still matter
# for a T2 count and for a T3 no item where u and one of its neighbors have the two outer colors.

def same_color_question(g, answer, rng, position):
    """T1. A no item asks about adjacent groups. The edit gives v the color of u, or a color adjacent
    to u's; v's group must keep two nodes."""
    groups = random_groups(len(g), rng)
    size = group_sizes(groups)
    if answer == "yes":
        partners = {u: [v for v in g if v != u and groups[v] == groups[u] and size[groups[v]] >= 3] for u in g}
    else:
        partners = {u: [v for v in g if adjacent(groups[u], groups[v], position) and size[groups[v]] >= 3]
                    for u in g}
    u, v = pick(partners, rng)
    if u is None:
        return None
    new = rng.choice(adjacent_groups(groups[u], position)) if answer == "yes" else groups[u]
    return {"groups": groups, "u": u, "v": v, "edited_node": v, "edited_group": new}


def group_size_question(g, answer, rng, directions, position):
    """T2. Node u's group gets exactly `answer` nodes; the edit moves one other node into it from an
    adjacent group, or out of it into an adjacent group."""
    n = len(g)
    u = rng.randrange(n)
    home = rng.randrange(Groups)
    others = [w for w in range(n) if w != u]
    mates = set(rng.sample(others, answer - 1))
    rest = [w for w in others if w not in mates]
    while True:
        split = [rng.choice(other_groups(home)) for _ in rest]
        if all(split.count(k) >= 2 for k in other_groups(home)):
            break
    groups = [home] * n
    for w, k in zip(rest, split):
        groups[w] = k
    size = group_sizes(groups)
    candidates = {
        "up": [w for w in range(n) if adjacent(groups[w], home, position) and size[groups[w]] >= 3],
        "down": [w for w in range(n) if w != u and groups[w] == home] if size[home] >= 3 else [],
    }
    allowed = [d for d in candidates if candidates[d]]
    if not allowed:
        return None
    if len(allowed) == 2:
        # Where group sizes allow both, take the direction used less so far, so both occur equally often.
        tied = directions["up"] == directions["down"]
        direction = rng.choice(allowed) if tied else min(allowed, key=directions.get)
        directions[direction] += 1
    else:
        direction = allowed[0]
    w = rng.choice(candidates[direction])
    new = home if direction == "up" else rng.choice(adjacent_groups(home, position))
    return {"groups": groups, "u": u, "v": None, "edited_node": w, "edited_group": new}


def neighbor_question(g, answer, rng, position):
    """T3. A yes item has exactly one neighbor x in u's color; the edit recolors x to an adjacent
    color. A no item's edited neighbor x comes from an adjacent group and takes u's color. x's
    group must keep two nodes."""
    groups = random_groups(len(g), rng)
    size = group_sizes(groups)
    same = {u: [x for x in g[u] if groups[x] == groups[u]] for u in g}
    if answer == "yes":
        partners = {u: same[u] if len(same[u]) == 1 and size[groups[u]] >= 3 else [] for u in g}
    else:
        partners = {u: [x for x in g[u] if adjacent(groups[x], groups[u], position) and size[groups[x]] >= 3]
                    if not same[u] else [] for u in g}
    u, x = pick(partners, rng)
    if u is None:
        return None
    new = rng.choice(adjacent_groups(groups[u], position)) if answer == "yes" else groups[u]
    return {"groups": groups, "u": u, "v": None, "edited_node": x, "edited_group": new}


def edge_question(g, answer, shared, rng, position):
    """T4, the control. u and v are joined by an edge or not, and share a color or have adjacent
    colors. The edit recolors v as in T1, so it switches whether u and v share a color but never the
    edge; v's group must keep two nodes."""
    groups = random_groups(len(g), rng)
    size = group_sizes(groups)

    def fits(u, v):
        colors = groups[u] == groups[v] if shared else adjacent(groups[u], groups[v], position)
        return g.has_edge(u, v) == (answer == "yes") and colors and size[groups[v]] >= 3

    partners = {u: [v for v in g if v != u and fits(u, v)] for u in g}
    u, v = pick(partners, rng)
    if u is None:
        return None
    new = rng.choice(adjacent_groups(groups[u], position)) if shared else groups[u]
    return {"groups": groups, "u": u, "v": v, "edited_node": v, "edited_group": new}


def adjacent(a, b, position):
    """Whether two groups sit next to each other on the ladder palette (the middle color touches both)."""
    return abs(position[a] - position[b]) == 1


def adjacent_groups(k, position):
    return [j for j in range(Groups) if adjacent(k, j, position)]


def random_groups(n, rng):
    """Uniform assignment of n nodes to three groups, each with at least two nodes."""
    while True:
        groups = [rng.randrange(Groups) for _ in range(n)]
        if min(group_sizes(groups)) >= 2:
            return groups


def group_sizes(groups):
    return [groups.count(k) for k in range(Groups)]


def other_groups(k):
    return [j for j in range(Groups) if j != k]


def pick(partners, rng):
    """A random node with at least one valid partner, then a random partner, or (None, None)."""
    nodes = [u for u in partners if partners[u]]
    if not nodes:
        return None, None
    u = rng.choice(nodes)
    return u, rng.choice(partners[u])


def record(task, g, pos, band, layout_seed, answer, hue_center, position, rng, groups, u, v, edited_node, edited_group):
    """The manifest entry: everything needed to redraw the item and score every condition."""
    edited = list(groups)
    edited[edited_node] = edited_group
    assert correct_answer(task, g, groups, u, v) == answer
    # Every edit changes the answer, except in T4, whose answer depends on the edges only.
    assert (correct_answer(task, g, edited, u, v) == answer) == (task == "T4")
    assert min(group_sizes(edited)) >= 2
    reassignment = rng.choice(Derangements)
    palettes = {"original": list(Tab10), "reassigned": [Tab10[k] for k in reassignment]}
    for d in Distances:
        ladder = LadderPalettes[(hue_center, d)]
        palettes[f"d{d}"] = [ladder[position[k]] for k in range(Groups)]
    return {
        "task": task,
        "question": Prompts[task].format(u=label(u), v=label(v) if v is not None else ""),
        "u": label(u),
        "v": label(v) if v is not None else None,
        "answer": answer,
        "edited_answer": correct_answer(task, g, edited, u, v),
        "nodes": len(g),
        "edges": g.number_of_edges(),
        "band": band,
        "layout_seed": layout_seed,
        "edge_list": [[label(a), label(b)] for a, b in g.edges],
        "positions": {label(node): list(pos[node]) for node in g},
        "groups": {label(node): groups[node] for node in g},
        "edited_node": label(edited_node),
        "edited_group": edited_group,
        "edited_node_degree": g.degree(edited_node),
        "crossings": crossings(g, pos),
        "hue_center": hue_center,
        "palette_position": position,  # ladder position (0, 1 = middle, 2) of each group
        "palettes": palettes,  # one color per group
        "images": {},  # filled in by write_set
    }


def ladder_palette(hue_center, distance):
    """Three colors at CIE lightness 65 and chroma 35: the hue center, and one color on each side
    at least `distance` CIEDE2000 units from it, as close to that as 8-bit sRGB allows. Distances are
    measured between the rounded colors, since those are what gets drawn."""
    middle = lab_to_hex(lch_to_lab(hue_center))
    sides = []
    for sign in (-1, 1):
        low, high = 0.0, 120.0
        for _ in range(60):
            step = (low + high) / 2
            if ciede2000(hex_to_lab(lab_to_hex(lch_to_lab(hue_center + sign * step))), hex_to_lab(middle)) < distance:
                low = step
            else:
                high = step
        sides.append(lab_to_hex(lch_to_lab(hue_center + sign * high)))
    return (sides[0], middle, sides[1])


def lch_to_lab(hue):
    return np.array([Lightness, Chroma * math.cos(math.radians(hue)), Chroma * math.sin(math.radians(hue))])


def lab_to_hex(lab):
    rgb = colour.XYZ_to_sRGB(colour.Lab_to_XYZ(lab))
    assert (rgb >= -1e-6).all() and (rgb <= 1 + 1e-6).all(), f"outside sRGB: {lab}"
    return "#" + "".join(f"{round(float(min(max(c, 0.0), 1.0)) * 255):02x}" for c in rgb)


def hex_to_lab(color):
    rgb = np.array([int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)])
    return colour.XYZ_to_Lab(colour.sRGB_to_XYZ(rgb))


def ciede2000(a, b):
    return float(colour.delta_E(a, b, method="CIE 2000"))


LadderPalettes = {(center, d): ladder_palette(center, d) for center in HueCenters for d in Distances}


def correct_answer(task, g, groups, u, v):
    if task == "T1":
        return "yes" if groups[u] == groups[v] else "no"
    if task == "T2":
        return groups.count(groups[u])
    if task == "T3":
        return "yes" if any(groups[x] == groups[u] for x in g[u]) else "no"
    return "yes" if g.has_edge(u, v) else "no"


def label(node):
    return chr(ord("A") + node)


def crossings(g, pos):
    """Pairs of edges without a shared end whose segments cross."""
    count = 0
    for (a, b), (c, d) in combinations(g.edges, 2):
        if len({a, b, c, d}) == 4 and segments_cross(pos[a], pos[b], pos[c], pos[d]):
            count += 1
    return count


def segments_cross(p, q, r, s):
    def side(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return side(p, q, r) * side(p, q, s) < 0 and side(r, s, p) * side(r, s, q) < 0


def check_disjoint(items, pilot_manifests):
    """Pilot items are never reused (Appendix, Pilots), so no main item may equal an item of any pilot."""
    if not pilot_manifests:
        sys.exit("no pilot manifest found; generate the pilot first")
    def key(item):  # edge order and direction do not matter
        edges = sorted(sorted(edge) for edge in item["edge_list"])
        return (json.dumps(edges), json.dumps(item["groups"], sort_keys=True))
    pilot = {key(json.loads(line)) for path in pilot_manifests for line in path.read_text().splitlines()}
    shared = [item["id"] for item in items if key(item) in pilot]
    if shared:
        sys.exit(f"main items equal to pilot items: {shared}")


def write_set(out, items, rejections):
    for item in items:
        item["images"] = {condition: f"images/{item['id']}/{condition}.png" for condition in ImageConditions}
    texts = {name: "".join(json.dumps(row) + "\n" for row in rows)
             for name, rows in (("manifest.jsonl", items), ("rejections.jsonl", rejections))}
    for name, text in texts.items():
        if (out / name).exists() and (out / name).read_text() != text:
            sys.exit(f"{out / name} differs from what the code generates: restore it with git, or delete {out} to regenerate")
    for item in items:
        (out / "images" / item["id"]).mkdir(parents=True, exist_ok=True)
        for condition, path in item["images"].items():
            render(out / path, item, node_colors(item, condition))
    for name, text in texts.items():
        (out / name).write_text(text)


def node_colors(item, condition):
    """Fill color of every node in one image condition. "edited" is the original palette with the one
    node recolored; "d10-edited" is the d10 palette with the same node recolored."""
    is_edited = condition == "edited" or condition.endswith("-edited")
    palette = item["palettes"]["original" if condition == "edited" else condition.removesuffix("-edited")]
    groups = dict(item["groups"])
    if is_edited:
        groups[item["edited_node"]] = item["edited_group"]
    return {node: palette[k] for node, k in groups.items()}


def render(path, item, colors):
    """768 x 768 px PNG: white background, gray edges, black outlines, black labels with a white halo."""
    pos = item["positions"]
    fig = plt.figure(figsize=(ImagePx / Dpi, ImagePx / Dpi), dpi=Dpi)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(-Limit, Limit)
    ax.set_ylim(-Limit, Limit)
    ax.set_aspect("equal")
    ax.set_axis_off()
    for a, b in item["edge_list"]:
        ax.plot(*zip(pos[a], pos[b]), color=EdgeColor, linewidth=1.5, zorder=1)
    for node, color in colors.items():
        ax.add_patch(Circle(pos[node], NodeRadius, facecolor=color, edgecolor="black", linewidth=1, zorder=2))
        ax.text(*pos[node], node, ha="center", va="center", fontsize=13, fontweight="bold", zorder=3,
                path_effects=[pe.withStroke(linewidth=3, foreground="white")])
    fig.savefig(path, dpi=Dpi, facecolor="white", metadata={"Software": None})
    plt.close(fig)


if __name__ == "__main__":
    main()
