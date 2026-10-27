# Results: main

1200 items. Intervals are 95%; margin 5 pp.

## Claude Opus 5.5

Output tokens per reply, reasoning included: mean 70, median 58.

### Validity check

| Task | Accuracy, original | Bar | Gain over no image | Invalid without image | Passes |
| --- | --- | --- | --- | --- | --- |
| T1 | 100.0% [98.7%, 100.0%], n = 300 | 50.0% | 100.0% [97.5%, 100.0%], n = 300 | 300 of 300 | yes |
| T2 | 100.0% [98.7%, 100.0%], n = 300 | 20.0% | 100.0% [97.5%, 100.0%], n = 300 | 300 of 300 | yes |
| T3 | 100.0% [98.7%, 100.0%], n = 300 | 57.7% | 100.0% [97.5%, 100.0%], n = 300 | 300 of 300 | yes |
| T4 | 100.0% [98.7%, 100.0%], n = 300 | 89.3% | 100.0% [97.5%, 100.0%], n = 300 | 300 of 300 | yes |

Invalid includes refusals: without the image, some models decline to answer, and that counts as wrong.

### H1: supported down to d7; d5 rejected in T2

### H2: supported down to d7; d5 rejected in T2

### The 10-unit recommendation: enough

The published design recommendation keeps categorical colors at least 10 CIEDE2000 units apart.

### By color distance

Means of the T1 to T3 values, for description; the verdicts use the intervals per task, below.

| Recoloring | Excess flips | Edit loss | Accuracy, recolored | Accuracy, edited | n, H1 / H2 |
| --- | --- | --- | --- | --- | --- |
| reassigned (52) | 0.0% | -0.1% | 99.9% | 100.0% | 900 / 900 |
| d20 | -0.1% | 0.0% | 100.0% | 99.9% | 900 / 900 |
| d14 | -0.1% | -0.1% | 100.0% | 100.0% | 900 / 900 |
| d10 | -0.1% | -0.1% | 100.0% | 100.0% | 900 / 900 |
| d7 | 0.3% | 0.9% | 99.6% | 99.0% | 900 / 900 |
| d5 | 5.7% | 6.6% | 94.2% | 93.3% | 900 / 900 |
| d3 | 41.3% | 38.6% | 58.6% | 61.3% | 900 / 900 |

Answers changed on the repeat, mean over all tasks: 0.1%. n counts the T1 to T3 items with every reply the comparison needs.

### Per task

95% intervals; these decide the verdicts. A hypothesis is supported at a distance only if every task's interval lies below the margin.

| Excess flips | T1 | T2 | T3 | T4 |
| --- | --- | --- | --- | --- |
| reassigned | 0.0% [-1.6%, 1.6%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 |
| d20 | -0.3% [-1.9%, 0.9%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 |
| d14 | -0.3% [-1.9%, 0.9%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 |
| d10 | -0.3% [-1.9%, 0.9%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 |
| d7 | -0.3% [-1.9%, 0.9%], n = 300 | 1.0% [-0.3%, 2.9%], n = 300 | 0.3% [-0.9%, 1.9%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 |
| d5 | 3.0% [1.0%, 5.7%], n = 300 | 10.0% [7.1%, 13.9%], n = 300 | 4.0% [2.3%, 6.9%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 |
| d3 | 26.0% [21.2%, 31.3%], n = 300 | 68.3% [62.9%, 73.3%], n = 300 | 29.7% [24.8%, 35.1%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 |

| Edit loss | T1 | T2 | T3 | T4 |
| --- | --- | --- | --- | --- |
| reassigned | -0.3% [-1.9%, 0.9%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 |
| d20 | -0.3% [-1.9%, 0.9%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 | 0.3% [-0.9%, 1.9%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 |
| d14 | -0.3% [-1.9%, 0.9%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 |
| d10 | -0.3% [-1.9%, 0.9%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 |
| d7 | 0.3% [-1.3%, 2.1%], n = 300 | 2.0% [0.7%, 4.3%], n = 300 | 0.3% [-0.9%, 1.9%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 |
| d5 | 4.3% [2.1%, 7.4%], n = 300 | 10.3% [7.4%, 14.3%], n = 300 | 5.0% [3.1%, 8.1%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 |
| d3 | 22.7% [18.2%, 27.8%], n = 300 | 64.7% [59.1%, 69.9%], n = 300 | 28.3% [23.5%, 33.7%], n = 300 | 0.0% [-1.3%, 1.3%], n = 300 |

### Each task alone (descriptive)

| Task | H1 alone | H2 alone |
| --- | --- | --- |
| T1 | supported down to d7; d5 inconclusive | supported down to d7; d5 inconclusive |
| T2 | supported down to d7; d5 rejected | supported down to d7; d5 rejected |
| T3 | supported down to d7; d5 inconclusive | supported down to d7; d5 inconclusive |
| T4 | supported at every distance, down to d3 | supported at every distance, down to d3 |

The verdicts above need every task.

### The sequences under other margins (descriptive)

| Margin | H1 | H2 |
| --- | --- | --- |
| 2.5 pp | supported down to d10; d7 inconclusive | supported down to d10; d7 inconclusive |
| 5 pp | supported down to d7; d5 rejected in T2 | supported down to d7; d5 rejected in T2 |
| 10 pp | supported down to d7; d5 inconclusive | supported down to d7; d5 inconclusive |

### Intervals with a Bonferroni correction over all 56 tests (descriptive)

Each interval at one-sided 0.045% (z = 3.32) instead of 2.5%.

| Excess flips | T1 | T2 | T3 | T4 |
| --- | --- | --- | --- | --- |
| reassigned | 0.0% [-3.9%, 3.9%] | 0.0% [-3.5%, 3.5%] | 0.0% [-3.5%, 3.5%] | 0.0% [-3.5%, 3.5%] |
| d20 | -0.3% [-4.2%, 3.2%] | 0.0% [-3.5%, 3.5%] | 0.0% [-3.5%, 3.5%] | 0.0% [-3.5%, 3.5%] |
| d14 | -0.3% [-4.2%, 3.2%] | 0.0% [-3.5%, 3.5%] | 0.0% [-3.5%, 3.5%] | 0.0% [-3.5%, 3.5%] |
| d10 | -0.3% [-4.2%, 3.2%] | 0.0% [-3.5%, 3.5%] | 0.0% [-3.5%, 3.5%] | 0.0% [-3.5%, 3.5%] |
| d7 | -0.3% [-4.2%, 3.2%] | 1.0% [-2.6%, 5.3%] | 0.3% [-3.2%, 4.2%] | 0.0% [-3.5%, 3.5%] |
| d5 | 3.0% [-1.1%, 8.5%] | 10.0% [5.6%, 17.2%] | 4.0% [0.3%, 9.7%] | 0.0% [-3.5%, 3.5%] |
| d3 | 26.0% [18.2%, 35.3%] | 68.3% [58.9%, 76.5%] | 29.7% [21.8%, 39.0%] | 0.0% [-3.5%, 3.5%] |

| Edit loss | T1 | T2 | T3 | T4 |
| --- | --- | --- | --- | --- |
| reassigned | -0.3% [-4.2%, 3.2%] | 0.0% [-3.5%, 3.5%] | 0.0% [-3.5%, 3.5%] | 0.0% [-3.5%, 3.5%] |
| d20 | -0.3% [-4.2%, 3.2%] | 0.0% [-3.5%, 3.5%] | 0.3% [-3.2%, 4.2%] | 0.0% [-3.5%, 3.5%] |
| d14 | -0.3% [-4.2%, 3.2%] | 0.0% [-3.5%, 3.5%] | 0.0% [-3.5%, 3.5%] | 0.0% [-3.5%, 3.5%] |
| d10 | -0.3% [-4.2%, 3.2%] | 0.0% [-3.5%, 3.5%] | 0.0% [-3.5%, 3.5%] | 0.0% [-3.5%, 3.5%] |
| d7 | 0.3% [-3.5%, 4.4%] | 2.0% [-1.6%, 6.8%] | 0.3% [-3.2%, 4.2%] | 0.0% [-3.5%, 3.5%] |
| d5 | 4.3% [0.1%, 10.3%] | 10.3% [5.8%, 17.6%] | 5.0% [1.3%, 11.0%] | 0.0% [-3.5%, 3.5%] |
| d3 | 22.7% [15.3%, 31.7%] | 64.7% [55.1%, 73.2%] | 28.3% [20.6%, 37.6%] | 0.0% [-3.5%, 3.5%] |

### Answers without the image (descriptive)

| Task | Valid replies | Yes, or mean count |
| --- | --- | --- |
| T1 | 0 | - |
| T2 | 0 | - |
| T3 | 0 | - |
| T4 | 0 | - |

### Invalid replies by kind (descriptive)

| Drawing | No answer line | Truncated | Blocked |
| --- | --- | --- | --- |
| with image | 2 | 0 | 0 |
| without image | 1200 | 0 | 0 |

### Yes answers by correct answer on the ladder (descriptive)

| Recoloring | T1, answer yes | T1, answer no | T3, answer yes | T3, answer no |
| --- | --- | --- | --- | --- |
| d20 | 100.0% | 0.0% | 99.7% | 0.0% |
| d14 | 100.0% | 0.0% | 100.0% | 0.0% |
| d10 | 100.0% | 0.0% | 100.0% | 0.0% |
| d7 | 99.3% | 0.0% | 100.0% | 0.7% |
| d5 | 96.3% | 4.3% | 99.3% | 8.0% |
| d3 | 88.3% | 37.7% | 95.3% | 53.3% |

Cells: share of valid answers that are yes.

### Correct on both drawings of a same-palette pair (descriptive)

95% Wilson intervals.

| Palette | T1 | T2 | T3 | T4 |
| --- | --- | --- | --- | --- |
| tab10 | 100.0% [98.7%, 100.0%], n = 300 | 100.0% [98.7%, 100.0%], n = 300 | 100.0% [98.7%, 100.0%], n = 300 | 100.0% [98.7%, 100.0%], n = 300 |
| d20 | 100.0% [98.7%, 100.0%], n = 300 | 100.0% [98.7%, 100.0%], n = 300 | 99.7% [98.1%, 99.9%], n = 300 | 100.0% [98.7%, 100.0%], n = 300 |
| d14 | 100.0% [98.7%, 100.0%], n = 300 | 100.0% [98.7%, 100.0%], n = 300 | 100.0% [98.7%, 100.0%], n = 300 | 100.0% [98.7%, 100.0%], n = 300 |
| d10 | 100.0% [98.7%, 100.0%], n = 300 | 100.0% [98.7%, 100.0%], n = 300 | 100.0% [98.7%, 100.0%], n = 300 | 100.0% [98.7%, 100.0%], n = 300 |
| d7 | 99.3% [97.6%, 99.8%], n = 300 | 97.7% [95.3%, 98.9%], n = 300 | 99.3% [97.6%, 99.8%], n = 300 | 100.0% [98.7%, 100.0%], n = 300 |
| d5 | 92.7% [89.1%, 95.1%], n = 300 | 84.0% [79.4%, 87.7%], n = 300 | 91.3% [87.6%, 94.0%], n = 300 | 100.0% [98.7%, 100.0%], n = 300 |
| d3 | 57.0% [51.3%, 62.5%], n = 300 | 21.3% [17.1%, 26.3%], n = 300 | 44.0% [38.5%, 49.7%], n = 300 | 100.0% [98.7%, 100.0%], n = 300 |

### H1 excess flips on the items at risk, where reading two colors as one changes the answer (descriptive)

T1 and T3: no items only; T2: all items.

| Recoloring | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-2.5%, 2.5%], n = 150 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-2.5%, 2.5%], n = 150 |
| d20 | 0.0% [-2.5%, 2.5%], n = 150 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-2.5%, 2.5%], n = 150 |
| d14 | 0.0% [-2.5%, 2.5%], n = 150 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-2.5%, 2.5%], n = 150 |
| d10 | 0.0% [-2.5%, 2.5%], n = 150 | 0.0% [-1.3%, 1.3%], n = 300 | 0.0% [-2.5%, 2.5%], n = 150 |
| d7 | 0.0% [-2.5%, 2.5%], n = 150 | 1.0% [-0.3%, 2.9%], n = 300 | 0.7% [-1.8%, 3.7%], n = 150 |
| d5 | 3.3% [0.8%, 7.6%], n = 150 | 10.0% [7.1%, 13.9%], n = 300 | 8.0% [4.6%, 13.5%], n = 150 |
| d3 | 41.3% [33.8%, 49.3%], n = 150 | 68.3% [62.9%, 73.3%], n = 300 | 55.3% [47.3%, 63.1%], n = 150 |

### Error directions on the ladder (exploratory)

| Recoloring | False yes or overcount | False no or undercount | Invalid |
| --- | --- | --- | --- |
| d20 | 0 | 1 | 0 |
| d14 | 0 | 0 | 0 |
| d10 | 0 | 0 | 0 |
| d7 | 9 | 4 | 0 |
| d5 | 86 | 25 | 1 |
| d3 | 642 | 79 | 0 |

### Accuracy per condition and task

| Condition | T1 | T2 | T3 | T4 |
| --- | --- | --- | --- | --- |
| original | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| repeat | 99.7% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| reassigned | 99.7% (1 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d20 | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d20-edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 99.7% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d14 | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d14-edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d10 | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d10-edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d7 | 100.0% (0 inv, 0 miss) | 99.0% (0 inv, 0 miss) | 99.7% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d7-edited | 99.3% (0 inv, 0 miss) | 98.0% (0 inv, 0 miss) | 99.7% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d5 | 96.7% (0 inv, 0 miss) | 90.0% (0 inv, 0 miss) | 96.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d5-edited | 95.3% (0 inv, 0 miss) | 89.7% (0 inv, 0 miss) | 95.0% (1 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d3 | 73.7% (0 inv, 0 miss) | 31.7% (0 inv, 0 miss) | 70.3% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d3-edited | 77.0% (0 inv, 0 miss) | 35.3% (0 inv, 0 miss) | 71.7% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| no_image | 0.0% (300 inv, 0 miss) | 0.0% (300 inv, 0 miss) | 0.0% (300 inv, 0 miss) | 0.0% (300 inv, 0 miss) |

Cells: accuracy, then invalid and missing replies.

### Accuracy by hue center (exploratory)

| Hue center | d20 | d14 | d10 | d7 | d5 | d3 |
| --- | --- | --- | --- | --- | --- | --- |
| 55 | 100.0% | 100.0% | 100.0% | 98.0% | 82.0% | 47.0% |
| 115 | 100.0% | 100.0% | 100.0% | 100.0% | 99.3% | 78.0% |
| 175 | 100.0% | 100.0% | 100.0% | 100.0% | 98.7% | 68.3% |
| 235 | 100.0% | 100.0% | 100.0% | 98.0% | 88.7% | 45.3% |
| 295 | 99.7% | 100.0% | 100.0% | 100.0% | 98.7% | 60.3% |
| 355 | 100.0% | 100.0% | 100.0% | 99.7% | 95.3% | 60.7% |

### T2 accuracy by the position of u's color on the ladder (exploratory)

| u's color | d20 | d14 | d10 | d7 | d5 | d3 | Items |
| --- | --- | --- | --- | --- | --- | --- | --- |
| middle | 100.0% | 100.0% | 100.0% | 97.4% | 82.8% | 18.8% | 96 |
| outer | 100.0% | 100.0% | 100.0% | 99.0% | 93.1% | 40.4% | 204 |

Each cell pools the recolored and the edited drawing.

### T1 accuracy by the spatial separation of u and v in the drawing (exploratory)

Drawings where u and v have adjacent, different ladder colors.

| Distance between u and v | d20 | d14 | d10 | d7 | d5 | d3 | Items |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 73 to 223 px | 100.0% | 100.0% | 100.0% | 100.0% | 96.0% | 68.0% | 100 |
| 229 to 376 px | 100.0% | 100.0% | 100.0% | 100.0% | 95.0% | 57.0% | 100 |
| 377 to 694 px | 100.0% | 100.0% | 100.0% | 100.0% | 96.0% | 62.0% | 100 |

### Error analysis on the ladder (exploratory)

| nodes | Accuracy | Items |
| --- | --- | --- |
| 10 | 92.5% | 300 |
| 11 | 92.3% | 300 |
| 12 | 91.6% | 300 |

| edge band | Accuracy | Items |
| --- | --- | --- |
| sparse | 93.0% | 450 |
| dense | 91.3% | 450 |

| crossings | Accuracy | Items |
| --- | --- | --- |
| 0 | 92.8% | 463 |
| 1-2 | 91.8% | 344 |
| 3-5 | 90.2% | 84 |
| 6+ | 91.7% | 9 |

| edited node degree | Accuracy | Items |
| --- | --- | --- |
| 1 | 91.5% | 123 |
| 2 | 91.7% | 249 |
| 3 | 93.1% | 240 |
| 4 | 92.1% | 180 |
| 5 | 92.1% | 108 |

### Accuracy on the ladder by output tokens (exploratory)

| Output tokens | Accuracy | Replies |
| --- | --- | --- |
| 3 to 49 | 99.1% | 2689 |
| 50 to 76 | 97.6% | 2623 |
| 77 to 121 | 94.5% | 2779 |
| 122 to 755 | 77.6% | 2709 |

Rows are quartiles of this model's ladder replies; tied token counts share a row.

### T4 yes answers by edge and shared color (exploratory)

| Palette | No edge, shared color | No edge, other colors | Edge, shared color | Edge, other colors |
| --- | --- | --- | --- | --- |
| tab10 | 0.0% | 0.0% | 100.0% | 100.0% |
| d20 | 0.0% | 0.0% | 100.0% | 100.0% |
| d14 | 0.0% | 0.0% | 100.0% | 100.0% |
| d10 | 0.0% | 0.0% | 100.0% | 100.0% |
| d7 | 0.0% | 0.0% | 100.0% | 100.0% |
| d5 | 0.0% | 0.0% | 100.0% | 100.0% |
| d3 | 0.0% | 0.0% | 100.0% | 100.0% |

Cells: share of valid answers that are yes. tab10 pools the original, reassigned and edited drawings.

## Qwen3.8-27B

Output tokens per reply, reasoning included: mean 330, median 290.

### Validity check

| Task | Accuracy, original | Bar | Gain over no image | Invalid without image | Passes |
| --- | --- | --- | --- | --- | --- |
| T1 | 100.0% [98.7%, 100.0%], n = 300 | 50.0% | 44.3% [38.8%, 50.0%], n = 300 | 0 of 300 | yes |
| T2 | 99.0% [97.1%, 99.7%], n = 299 | 20.0% | 76.7% [71.5%, 81.1%], n = 296 | 15 of 297 | yes |
| T3 | 98.7% [96.6%, 99.5%], n = 298 | 57.7% | 49.2% [43.4%, 54.9%], n = 297 | 0 of 299 | yes |
| T4 | 99.7% [98.1%, 99.9%], n = 300 | 89.3% | 50.0% [44.3%, 55.7%], n = 300 | 1 of 300 | yes |

Invalid includes refusals: without the image, some models decline to answer, and that counts as wrong.

### H1: supported down to d20; d14 inconclusive

### H2: supported down to d20; d14 inconclusive

### The 10-unit recommendation: undetermined

The published design recommendation keeps categorical colors at least 10 CIEDE2000 units apart.

### By color distance

Means of the T1 to T3 values, for description; the verdicts use the intervals per task, below.

| Recoloring | Excess flips | Edit loss | Accuracy, recolored | Accuracy, edited | n, H1 / H2 |
| --- | --- | --- | --- | --- | --- |
| reassigned (52) | 0.1% | 0.4% | 99.7% | 99.2% | 890 / 892 |
| d20 | 0.7% | 0.8% | 99.3% | 99.1% | 893 / 892 |
| d14 | 3.4% | 3.8% | 96.7% | 95.9% | 892 / 892 |
| d10 | 17.9% | 18.1% | 82.0% | 81.1% | 891 / 893 |
| d7 | 36.7% | 37.5% | 63.0% | 61.6% | 891 / 889 |
| d5 | 47.8% | 47.4% | 51.7% | 51.9% | 894 / 887 |
| d3 | 60.2% | 61.1% | 39.5% | 38.3% | 893 / 893 |

Answers changed on the repeat, mean over all tasks: 0.6%. n counts the T1 to T3 items with every reply the comparison needs.

### Per task

95% intervals; these decide the verdicts. A hypothesis is supported at a distance only if every task's interval lies below the margin.

| Excess flips | T1 | T2 | T3 | T4 |
| --- | --- | --- | --- | --- |
| reassigned | 0.0% [-1.3%, 1.3%], n = 298 | -0.3% [-1.9%, 0.9%], n = 296 | 0.7% [-0.6%, 2.4%], n = 296 | 0.3% [-0.9%, 1.9%], n = 300 |
| d20 | 0.3% [-0.9%, 1.9%], n = 298 | -0.3% [-1.9%, 0.9%], n = 298 | 2.0% [0.7%, 4.3%], n = 297 | -0.3% [-1.9%, 0.9%], n = 300 |
| d14 | 1.0% [-0.3%, 2.9%], n = 298 | 3.4% [1.3%, 6.2%], n = 297 | 5.7% [3.6%, 9.0%], n = 297 | -0.3% [-1.9%, 0.9%], n = 300 |
| d10 | 10.4% [7.4%, 14.4%], n = 298 | 25.3% [20.7%, 30.6%], n = 296 | 17.8% [13.9%, 22.6%], n = 297 | 0.0% [-1.3%, 1.3%], n = 300 |
| d7 | 20.2% [16.0%, 25.1%], n = 297 | 60.9% [55.2%, 66.4%], n = 297 | 29.0% [24.1%, 34.4%], n = 297 | 0.3% [-0.9%, 1.9%], n = 300 |
| d5 | 30.5% [25.6%, 36.0%], n = 298 | 75.8% [70.7%, 80.4%], n = 298 | 36.9% [31.5%, 42.6%], n = 298 | 0.7% [-0.6%, 2.4%], n = 300 |
| d3 | 45.6% [40.1%, 51.3%], n = 298 | 89.9% [85.7%, 92.9%], n = 298 | 45.1% [39.6%, 50.8%], n = 297 | 0.0% [-1.3%, 1.3%], n = 300 |

| Edit loss | T1 | T2 | T3 | T4 |
| --- | --- | --- | --- | --- |
| reassigned | 0.0% [-1.3%, 1.3%], n = 296 | -0.3% [-1.9%, 0.9%], n = 298 | 1.7% [0.4%, 3.9%], n = 298 | 0.0% [-1.3%, 1.3%], n = 300 |
| d20 | 0.0% [-1.3%, 1.3%], n = 298 | 0.3% [-1.3%, 2.1%], n = 297 | 2.0% [0.7%, 4.3%], n = 297 | 0.3% [-0.9%, 1.9%], n = 300 |
| d14 | 1.7% [0.4%, 3.9%], n = 297 | 4.4% [2.2%, 7.5%], n = 297 | 5.4% [3.3%, 8.5%], n = 298 | 0.0% [-1.3%, 1.3%], n = 300 |
| d10 | 13.1% [9.7%, 17.4%], n = 298 | 23.2% [18.6%, 28.3%], n = 298 | 18.2% [14.2%, 23.0%], n = 297 | 0.3% [-0.9%, 1.9%], n = 300 |
| d7 | 24.9% [20.3%, 30.1%], n = 297 | 58.6% [52.8%, 64.2%], n = 295 | 29.0% [24.1%, 34.4%], n = 297 | 0.0% [-1.3%, 1.3%], n = 300 |
| d5 | 33.2% [28.1%, 38.8%], n = 295 | 72.6% [67.3%, 77.4%], n = 296 | 36.5% [31.2%, 42.1%], n = 296 | 0.0% [-1.3%, 1.3%], n = 300 |
| d3 | 47.7% [42.0%, 53.3%], n = 298 | 91.2% [87.5%, 94.0%], n = 297 | 44.3% [38.8%, 50.0%], n = 298 | 0.7% [-0.6%, 2.4%], n = 300 |

### Each task alone (descriptive)

| Task | H1 alone | H2 alone |
| --- | --- | --- |
| T1 | supported down to d14; d10 rejected | supported down to d14; d10 rejected |
| T2 | supported down to d20; d14 inconclusive | supported down to d20; d14 inconclusive |
| T3 | supported down to d20; d14 inconclusive | supported down to d20; d14 inconclusive |
| T4 | supported at every distance, down to d3 | supported at every distance, down to d3 |

The verdicts above need every task.

### The sequences under other margins (descriptive)

| Margin | H1 | H2 |
| --- | --- | --- |
| 2.5 pp | supported down to reassigned; d20 inconclusive | inconclusive at reassigned |
| 5 pp | supported down to d20; d14 inconclusive | supported down to d20; d14 inconclusive |
| 10 pp | supported down to d14; d10 rejected in T2, T3 | supported down to d14; d10 rejected in T2, T3 |

### Intervals with a Bonferroni correction over all 56 tests (descriptive)

Each interval at one-sided 0.045% (z = 3.32) instead of 2.5%.

| Excess flips | T1 | T2 | T3 | T4 |
| --- | --- | --- | --- | --- |
| reassigned | 0.0% [-3.6%, 3.6%] | -0.3% [-4.2%, 3.3%] | 0.7% [-2.9%, 4.8%] | 0.3% [-3.2%, 4.2%] |
| d20 | 0.3% [-3.2%, 4.2%] | -0.3% [-4.2%, 3.2%] | 2.0% [-1.6%, 6.9%] | -0.3% [-4.2%, 3.2%] |
| d14 | 1.0% [-2.6%, 5.3%] | 3.4% [-0.8%, 9.0%] | 5.7% [1.9%, 12.0%] | -0.3% [-4.2%, 3.2%] |
| d10 | 10.4% [5.9%, 17.8%] | 25.3% [17.9%, 34.5%] | 17.8% [11.7%, 26.3%] | 0.0% [-3.5%, 3.5%] |
| d7 | 20.2% [13.6%, 28.9%] | 60.9% [51.0%, 69.9%] | 29.0% [21.1%, 38.3%] | 0.3% [-3.2%, 4.2%] |
| d5 | 30.5% [22.5%, 40.0%] | 75.8% [66.8%, 83.1%] | 36.9% [28.0%, 46.6%] | 0.7% [-2.9%, 4.7%] |
| d3 | 45.6% [36.4%, 55.2%] | 89.9% [81.6%, 94.4%] | 45.1% [35.9%, 54.7%] | 0.0% [-3.5%, 3.5%] |

| Edit loss | T1 | T2 | T3 | T4 |
| --- | --- | --- | --- | --- |
| reassigned | 0.0% [-3.6%, 3.6%] | -0.3% [-4.2%, 3.2%] | 1.7% [-2.0%, 6.4%] | 0.0% [-3.5%, 3.5%] |
| d20 | 0.0% [-3.6%, 3.6%] | 0.3% [-3.6%, 4.5%] | 2.0% [-1.6%, 6.9%] | 0.3% [-3.2%, 4.2%] |
| d14 | 1.7% [-2.0%, 6.4%] | 4.4% [0.1%, 10.4%] | 5.4% [1.6%, 11.5%] | 0.0% [-3.5%, 3.5%] |
| d10 | 13.1% [7.9%, 20.9%] | 23.2% [15.7%, 32.2%] | 18.2% [11.9%, 26.7%] | 0.3% [-3.2%, 4.2%] |
| d7 | 24.9% [17.6%, 34.1%] | 58.6% [48.7%, 67.8%] | 29.0% [21.1%, 38.3%] | 0.0% [-3.5%, 3.5%] |
| d5 | 33.2% [24.9%, 42.8%] | 72.6% [63.3%, 80.3%] | 36.5% [27.8%, 46.1%] | 0.0% [-3.5%, 3.5%] |
| d3 | 47.7% [38.3%, 57.2%] | 91.2% [84.2%, 95.3%] | 44.3% [35.1%, 53.9%] | 0.7% [-2.9%, 4.7%] |

### Answers without the image (descriptive)

| Task | Valid replies | Yes, or mean count |
| --- | --- | --- |
| T1 | 300 | 25.7% |
| T2 | 282 | 2.8 |
| T3 | 299 | 6.7% |
| T4 | 299 | 7.7% |

### Invalid replies by kind (descriptive)

| Drawing | No answer line | Truncated | Blocked |
| --- | --- | --- | --- |
| with image | 1 | 0 | 0 |
| without image | 16 | 0 | 0 |

### Yes answers by correct answer on the ladder (descriptive)

| Recoloring | T1, answer yes | T1, answer no | T3, answer yes | T3, answer no |
| --- | --- | --- | --- | --- |
| d20 | 99.7% | 0.0% | 99.0% | 2.7% |
| d14 | 99.0% | 1.7% | 98.3% | 9.7% |
| d10 | 97.7% | 21.7% | 96.3% | 32.8% |
| d7 | 91.3% | 36.3% | 96.0% | 55.7% |
| d5 | 87.2% | 50.8% | 94.0% | 68.9% |
| d3 | 93.0% | 86.3% | 97.3% | 87.3% |

Cells: share of valid answers that are yes.

### Correct on both drawings of a same-palette pair (descriptive)

95% Wilson intervals.

| Palette | T1 | T2 | T3 | T4 |
| --- | --- | --- | --- | --- |
| tab10 | 100.0% [98.7%, 100.0%], n = 298 | 99.0% [97.1%, 99.7%], n = 299 | 97.0% [94.4%, 98.4%], n = 298 | 99.7% [98.1%, 99.9%], n = 300 |
| d20 | 99.7% [98.1%, 99.9%], n = 300 | 99.3% [97.6%, 99.8%], n = 299 | 96.3% [93.5%, 97.9%], n = 298 | 99.3% [97.6%, 99.8%], n = 300 |
| d14 | 97.3% [94.8%, 98.6%], n = 299 | 93.3% [89.9%, 95.6%], n = 298 | 88.6% [84.5%, 91.7%], n = 299 | 99.7% [98.1%, 99.9%], n = 300 |
| d10 | 76.7% [71.6%, 81.1%], n = 300 | 63.8% [58.2%, 69.0%], n = 298 | 64.4% [58.8%, 69.6%], n = 298 | 99.7% [98.1%, 99.9%], n = 300 |
| d7 | 59.7% [54.1%, 65.1%], n = 298 | 24.7% [20.1%, 29.9%], n = 296 | 43.6% [38.1%, 49.3%], n = 298 | 99.7% [98.1%, 99.9%], n = 300 |
| d5 | 41.4% [36.0%, 47.1%], n = 297 | 12.4% [9.1%, 16.6%], n = 298 | 28.9% [24.0%, 34.2%], n = 298 | 99.3% [97.6%, 99.8%], n = 300 |
| d3 | 11.7% [8.5%, 15.8%], n = 300 | 2.7% [1.4%, 5.2%], n = 299 | 12.0% [8.8%, 16.2%], n = 299 | 99.0% [97.1%, 99.7%], n = 300 |

### H1 excess flips on the items at risk, where reading two colors as one changes the answer (descriptive)

T1 and T3: no items only; T2: all items.

| Recoloring | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-2.5%, 2.5%], n = 150 | -0.3% [-1.9%, 0.9%], n = 296 | 0.7% [-1.9%, 3.7%], n = 148 |
| d20 | 0.0% [-2.5%, 2.5%], n = 150 | -0.3% [-1.9%, 0.9%], n = 298 | 2.0% [-0.6%, 5.8%], n = 149 |
| d14 | 0.7% [-1.8%, 3.7%], n = 150 | 3.4% [1.3%, 6.2%], n = 297 | 10.1% [6.2%, 15.9%], n = 149 |
| d10 | 20.0% [14.4%, 27.1%], n = 150 | 25.3% [20.7%, 30.6%], n = 296 | 33.6% [26.5%, 41.5%], n = 149 |
| d7 | 31.3% [24.5%, 39.1%], n = 150 | 60.9% [55.2%, 66.4%], n = 297 | 57.4% [49.4%, 65.1%], n = 148 |
| d5 | 50.0% [42.1%, 57.9%], n = 150 | 75.8% [70.7%, 80.4%], n = 298 | 69.1% [61.3%, 76.0%], n = 149 |
| d3 | 86.0% [79.5%, 90.7%], n = 150 | 89.9% [85.7%, 92.9%], n = 298 | 87.9% [81.7%, 92.2%], n = 149 |

### Error directions on the ladder (exploratory)

| Recoloring | False yes or overcount | False no or undercount | Invalid |
| --- | --- | --- | --- |
| d20 | 8 | 6 | 0 |
| d14 | 53 | 14 | 0 |
| d10 | 299 | 32 | 0 |
| d7 | 610 | 65 | 0 |
| d5 | 774 | 90 | 1 |
| d3 | 1022 | 76 | 0 |

### Accuracy per condition and task

| Condition | T1 | T2 | T3 | T4 |
| --- | --- | --- | --- | --- |
| original | 100.0% (0 inv, 0 miss) | 99.0% (0 inv, 1 miss) | 98.7% (0 inv, 2 miss) | 99.7% (0 inv, 0 miss) |
| repeat | 100.0% (0 inv, 2 miss) | 99.7% (0 inv, 1 miss) | 99.7% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| reassigned | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 2 miss) | 99.0% (0 inv, 2 miss) | 99.7% (0 inv, 0 miss) |
| edited | 100.0% (0 inv, 2 miss) | 99.3% (0 inv, 0 miss) | 98.3% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d20 | 99.7% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 98.3% (0 inv, 1 miss) | 99.7% (0 inv, 0 miss) |
| d20-edited | 100.0% (0 inv, 0 miss) | 99.3% (0 inv, 1 miss) | 98.0% (0 inv, 1 miss) | 99.3% (0 inv, 0 miss) |
| d14 | 99.0% (0 inv, 0 miss) | 96.3% (0 inv, 1 miss) | 94.6% (0 inv, 1 miss) | 99.7% (0 inv, 0 miss) |
| d14-edited | 98.3% (0 inv, 1 miss) | 95.3% (0 inv, 1 miss) | 94.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d10 | 89.7% (0 inv, 0 miss) | 73.8% (0 inv, 2 miss) | 82.6% (0 inv, 1 miss) | 100.0% (0 inv, 0 miss) |
| d10-edited | 86.3% (0 inv, 0 miss) | 76.0% (0 inv, 0 miss) | 80.9% (0 inv, 1 miss) | 99.7% (0 inv, 0 miss) |
| d7 | 79.9% (0 inv, 1 miss) | 38.1% (0 inv, 1 miss) | 70.9% (0 inv, 1 miss) | 99.7% (0 inv, 0 miss) |
| d7-edited | 74.9% (0 inv, 1 miss) | 40.4% (0 inv, 3 miss) | 69.6% (0 inv, 1 miss) | 100.0% (0 inv, 0 miss) |
| d5 | 69.7% (0 inv, 0 miss) | 23.0% (0 inv, 0 miss) | 62.3% (1 inv, 0 miss) | 99.3% (0 inv, 0 miss) |
| d5-edited | 66.7% (0 inv, 3 miss) | 26.5% (0 inv, 2 miss) | 62.4% (0 inv, 2 miss) | 100.0% (0 inv, 0 miss) |
| d3 | 54.7% (0 inv, 0 miss) | 9.0% (0 inv, 0 miss) | 54.8% (0 inv, 1 miss) | 100.0% (0 inv, 0 miss) |
| d3-edited | 52.0% (0 inv, 0 miss) | 8.0% (0 inv, 1 miss) | 55.0% (0 inv, 0 miss) | 99.0% (0 inv, 0 miss) |
| no_image | 55.7% (0 inv, 0 miss) | 22.2% (15 inv, 3 miss) | 49.5% (0 inv, 1 miss) | 49.7% (1 inv, 0 miss) |

Cells: accuracy, then invalid and missing replies.

### Accuracy by hue center (exploratory)

| Hue center | d20 | d14 | d10 | d7 | d5 | d3 |
| --- | --- | --- | --- | --- | --- | --- |
| 55 | 99.7% | 99.3% | 88.0% | 62.0% | 54.2% | 39.8% |
| 115 | 99.3% | 98.7% | 94.6% | 76.5% | 60.1% | 48.0% |
| 175 | 98.3% | 90.9% | 70.7% | 58.0% | 48.8% | 36.7% |
| 235 | 99.3% | 91.3% | 68.3% | 52.0% | 46.3% | 34.8% |
| 295 | 99.0% | 99.3% | 88.0% | 63.9% | 51.5% | 38.7% |
| 355 | 99.7% | 98.0% | 79.9% | 61.5% | 49.7% | 35.7% |

### T2 accuracy by the position of u's color on the ladder (exploratory)

| u's color | d20 | d14 | d10 | d7 | d5 | d3 | Items |
| --- | --- | --- | --- | --- | --- | --- | --- |
| middle | 99.5% | 95.3% | 59.7% | 22.5% | 12.0% | 3.7% | 96 |
| outer | 99.8% | 96.1% | 82.1% | 47.2% | 30.7% | 10.8% | 204 |

Each cell pools the recolored and the edited drawing.

### T1 accuracy by the spatial separation of u and v in the drawing (exploratory)

Drawings where u and v have adjacent, different ladder colors.

| Distance between u and v | d20 | d14 | d10 | d7 | d5 | d3 | Items |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 73 to 223 px | 100.0% | 99.0% | 74.0% | 60.0% | 40.0% | 9.0% | 100 |
| 229 to 376 px | 100.0% | 99.0% | 84.0% | 68.0% | 51.0% | 17.0% | 100 |
| 377 to 694 px | 100.0% | 97.0% | 77.0% | 63.0% | 56.6% | 15.0% | 100 |

### Error analysis on the ladder (exploratory)

| nodes | Accuracy | Items |
| --- | --- | --- |
| 10 | 72.1% | 300 |
| 11 | 72.2% | 300 |
| 12 | 70.7% | 300 |

| edge band | Accuracy | Items |
| --- | --- | --- |
| sparse | 71.6% | 450 |
| dense | 71.7% | 450 |

| crossings | Accuracy | Items |
| --- | --- | --- |
| 0 | 71.4% | 463 |
| 1-2 | 72.1% | 344 |
| 3-5 | 72.0% | 84 |
| 6+ | 65.7% | 9 |

| edited node degree | Accuracy | Items |
| --- | --- | --- |
| 1 | 68.2% | 123 |
| 2 | 70.1% | 249 |
| 3 | 72.6% | 240 |
| 4 | 73.6% | 180 |
| 5 | 74.0% | 108 |

### Accuracy on the ladder by output tokens (exploratory)

| Output tokens | Accuracy | Replies |
| --- | --- | --- |
| 53 to 218 | 79.6% | 2685 |
| 219 to 326 | 79.1% | 2697 |
| 327 to 455 | 71.1% | 2686 |
| 456 to 4644 | 57.0% | 2704 |

Rows are quartiles of this model's ladder replies; tied token counts share a row.

### T4 yes answers by edge and shared color (exploratory)

| Palette | No edge, shared color | No edge, other colors | Edge, shared color | Edge, other colors |
| --- | --- | --- | --- | --- |
| tab10 | 0.0% | 0.4% | 100.0% | 99.6% |
| d20 | 0.7% | 0.7% | 99.3% | 100.0% |
| d14 | 0.0% | 0.7% | 100.0% | 100.0% |
| d10 | 0.0% | 0.0% | 99.3% | 100.0% |
| d7 | 0.0% | 0.0% | 99.3% | 100.0% |
| d5 | 0.0% | 0.7% | 99.3% | 100.0% |
| d3 | 1.3% | 0.0% | 99.3% | 100.0% |

Cells: share of valid answers that are yes. tab10 pools the original, reassigned and edited drawings.

