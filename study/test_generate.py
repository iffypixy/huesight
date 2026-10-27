import json
import math
from collections import Counter

import matplotlib.image
import pytest

import generate


@pytest.fixture(scope="module")
def items():
    # 60 items per task is the smallest count that balances answers within every cell for all tasks.
    items, _ = generate.make_items("test", seed=5, items_per_task=60)
    return items


def answer_from_colors(item, colors):
    """The correct answer read off the node colors alone, written independently of the generator."""
    u, v = item["u"], item["v"]
    if item["task"] == "T1":
        return "yes" if colors[u] == colors[v] else "no"
    if item["task"] == "T2":
        return sum(color == colors[u] for color in colors.values())
    neighbors = {b for a, b in item["edge_list"] if a == u} | {a for a, b in item["edge_list"] if b == u}
    if item["task"] == "T3":
        return "yes" if any(colors[x] == colors[u] for x in neighbors) else "no"
    return "yes" if v in neighbors else "no"


Recolored = [c for c in generate.ImageConditions if not c.endswith("edited")]
Edited = [c for c in generate.ImageConditions if c.endswith("edited")]


def test_preserving_recolorings_keep_the_answer(items):
    for item in items:
        for condition in Recolored:
            colors = generate.node_colors(item, condition)
            assert answer_from_colors(item, colors) == item["answer"], (item["id"], condition)


def test_every_edit_changes_the_answer_except_in_t4(items):
    for item in items:
        for condition in Edited:
            edited = answer_from_colors(item, generate.node_colors(item, condition))
            assert edited == item["edited_answer"], (item["id"], condition)
            assert (edited == item["answer"]) == (item["task"] == "T4"), (item["id"], condition)


def test_t4_edit_switches_whether_u_and_v_share_a_color(items):
    for item in items:
        if item["task"] != "T4":
            continue
        for condition in Edited:
            base = "original" if condition == "edited" else condition.removesuffix("-edited")
            before, after = generate.node_colors(item, base), generate.node_colors(item, condition)
            u, v = item["u"], item["v"]
            assert (before[u] == before[v]) != (after[u] == after[v]), (item["id"], condition)


def test_t4_shares_a_color_in_half_the_items_with_an_edge_and_half_without(items):
    cells = Counter((i["answer"], i["groups"][i["u"]] == i["groups"][i["v"]]) for i in items if i["task"] == "T4")
    assert len(cells) == 4 and len(set(cells.values())) == 1


def test_edit_recolors_exactly_one_node_to_a_color_already_in_the_drawing(items):
    for item in items:
        for condition in Edited:
            base = "original" if condition == "edited" else condition.removesuffix("-edited")
            before = generate.node_colors(item, base)
            after = generate.node_colors(item, condition)
            changed = [node for node in before if before[node] != after[node]]
            assert changed == [item["edited_node"]], (item["id"], condition)
            assert after[item["edited_node"]] in before.values()


def test_ladder_colors_sit_the_stated_distance_apart_and_never_closer():
    # Items take their palettes from LadderPalettes by ladder position, so checking LadderPalettes checks every item.
    for (center, d), palette in generate.LadderPalettes.items():
        side, middle, other_side = (generate.hex_to_lab(color) for color in palette)
        for outer in (side, other_side):
            assert d <= generate.ciede2000(outer, middle) <= d + 0.5, (center, d)
        assert generate.ciede2000(side, other_side) >= 1.5 * d, (center, d)


def test_every_color_the_answer_depends_on_is_one_ladder_step_away(items):
    # T1 "no" pairs and every edit use adjacent groups, so on a ladder palette a model must resolve
    # exactly the ladder distance, never the wider outer pair.
    for item in items:
        position = item["palette_position"]
        old = item["groups"][item["edited_node"]]
        assert generate.adjacent(old, item["edited_group"], position), item["id"]
        u, v = item["u"], item["v"]
        differ = item["task"] == "T1" and item["answer"] == "no" or item["task"] == "T4" and item["groups"][u] != item["groups"][v]
        if differ:
            assert generate.adjacent(item["groups"][u], item["groups"][v], position), item["id"]


def test_hue_centers_are_balanced_within_each_task(items):
    for task in generate.Tasks:
        centers = Counter(i["hue_center"] for i in items if i["task"] == task)
        assert sorted(centers) == sorted(generate.HueCenters) and len(set(centers.values())) == 1, task


def test_palettes_are_one_to_one_and_reassignment_moves_every_group(items):
    for item in items:
        palettes = item["palettes"]
        assert palettes["original"] == list(generate.Tab10)
        assert sorted(palettes["reassigned"]) == sorted(generate.Tab10)
        assert all(new != old for new, old in zip(palettes["reassigned"], palettes["original"]))
        for d in generate.Distances:
            assert len(set(palettes[f"d{d}"])) == 3, (item["id"], d)


def test_every_group_keeps_at_least_two_nodes(items):
    for item in items:
        for condition in ("original", "edited"):
            sizes = Counter(generate.node_colors(item, condition).values())
            assert len(sizes) == 3 and min(sizes.values()) >= 2, (item["id"], condition)


def test_t3_yes_means_exactly_one_same_colored_neighbor(items):
    for item in items:
        if item["task"] != "T3":
            continue
        u = item["u"]
        neighbors = {b for a, b in item["edge_list"] if a == u} | {a for a, b in item["edge_list"] if b == u}
        for condition, answer in (("original", item["answer"]), ("edited", item["edited_answer"])):
            colors = generate.node_colors(item, condition)
            same = sum(colors[x] == colors[u] for x in neighbors)
            assert same == (1 if answer == "yes" else 0), (item["id"], condition)


def test_every_drawing_passes_the_check(items):
    r = generate.NodeRadius
    for item in items:
        pos = item["positions"]
        for a in pos:
            for b in pos:
                assert a == b or math.dist(pos[a], pos[b]) >= 3 * r, item["id"]
        for a, b in item["edge_list"]:
            for w in pos:
                if w not in (a, b):
                    assert generate.segment_distance(pos[w], pos[a], pos[b]) >= 2 * r, item["id"]


def test_graphs_are_connected_with_edge_counts_in_their_band(items):
    bands = {"sparse": (1.0, 1.3), "dense": (1.4, 1.8)}
    for item in items:
        n, m = item["nodes"], item["edges"]
        low, high = bands[item["band"]]
        assert low * n <= m <= high * n and len(item["edge_list"]) == m, item["id"]
        reached, frontier = {item["u"]}, [item["u"]]
        while frontier:
            node = frontier.pop()
            for a, b in item["edge_list"]:
                for x, y in ((a, b), (b, a)):
                    if x == node and y not in reached:
                        reached.add(y)
                        frontier.append(y)
        assert len(reached) == n, item["id"]


def test_answers_are_balanced_within_every_cell(items):
    for task in generate.Tasks:
        cells = Counter((i["nodes"], i["band"], i["answer"]) for i in items if i["task"] == task)
        assert len(set(cells.values())) == 1, task
        assert len(cells) == 6 * len(generate.Answers[task]), task


def test_t2_edits_stay_between_2_and_7(items):
    edited = {i["edited_answer"] for i in items if i["task"] == "T2"}
    assert edited <= set(range(2, 8))


def test_the_pilot_guard_catches_an_identical_graph_with_edges_in_another_order(tmp_path, items):
    pilot = tmp_path / "manifest.jsonl"
    pilot.write_text(json.dumps(items[0]) + "\n")
    shuffled = dict(items[0], edge_list=[[b, a] for a, b in reversed(items[0]["edge_list"])])
    with pytest.raises(SystemExit, match="equal to pilot items"):
        generate.check_disjoint([shuffled], [pilot])


def test_adding_t4_leaves_the_items_of_t1_to_t3_unchanged():
    three, _ = generate.make_items("again", seed=9, items_per_task=4, tasks=generate.Tasks[:3])
    four, _ = generate.make_items("again", seed=9, items_per_task=4)
    assert four[:len(three)] == three and [i["task"] for i in four[len(three):]] == ["T4"] * 4


def test_the_same_seed_gives_the_same_items():
    first, _ = generate.make_items("again", seed=9, items_per_task=4)
    second, _ = generate.make_items("again", seed=9, items_per_task=4)
    assert first == second


def test_images_show_the_manifest_colors(tmp_path):
    items, rejections = generate.make_items("image", seed=3, items_per_task=1)
    generate.write_set(tmp_path, items[:1], rejections)
    item = items[0]
    for condition in generate.ImageConditions:
        image = matplotlib.image.imread(tmp_path / item["images"][condition])
        assert image.shape[:2] == (generate.ImagePx, generate.ImagePx)
        for node, color in generate.node_colors(item, condition).items():
            x, y = item["positions"][node]
            # Sample inside the node but right of its label.
            column = round((x + 0.6 * generate.NodeRadius + generate.Limit) / (2 * generate.Limit) * generate.ImagePx)
            row = round((generate.Limit - y) / (2 * generate.Limit) * generate.ImagePx)
            expected = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            assert image[row, column, :3] == pytest.approx(expected, abs=2 / 255), (condition, node)
