# Results: pilot

60 items. Intervals are 95%; margin 5 pp.

## Claude Opus 5.5

Output tokens per reply, reasoning included: mean 87, median 68.

### Validity check

| Task | Accuracy, original | Bar | Gain over no image | Invalid without image | Passes |
| --- | --- | --- | --- | --- | --- |
| T1 | 100.0% [83.9%, 100.0%], n = 20 | 50.0% | 100.0% [67.8%, 100.0%], n = 20 | 20 of 20 | yes |
| T2 | 100.0% [83.9%, 100.0%], n = 20 | 20.0% | 100.0% [67.8%, 100.0%], n = 20 | 20 of 20 | yes |
| T3 | 100.0% [83.9%, 100.0%], n = 20 | 55.0% | 100.0% [67.8%, 100.0%], n = 20 | 20 of 20 | yes |

Invalid includes refusals: without the image, some models decline to answer, and that counts as wrong.

### H1: inconclusive at reassigned

### H2: inconclusive at reassigned

### The 10-unit recommendation: undetermined

The published design recommendation keeps categorical colors at least 10 CIEDE2000 units apart.

### By color distance

Means of the T1 to T3 values, for description; the verdicts use the intervals per task, below.

| Recoloring | Excess flips | Edit loss | Accuracy, recolored | Accuracy, edited | n, H1 / H2 |
| --- | --- | --- | --- | --- | --- |
| reassigned (52) | 0.0% | 0.0% | 100.0% | 100.0% | 60 / 60 |
| d20 | 0.0% | 0.0% | 100.0% | 100.0% | 60 / 60 |
| d14 | 0.0% | 0.0% | 100.0% | 100.0% | 60 / 60 |
| d10 | 0.0% | 0.0% | 100.0% | 100.0% | 60 / 60 |
| d7 | 0.0% | 0.0% | 100.0% | 100.0% | 60 / 60 |
| d5 | 6.7% | 6.7% | 93.3% | 93.3% | 60 / 60 |
| d3 | 41.7% | 45.0% | 58.3% | 55.0% | 60 / 60 |

Answers changed on the repeat, mean over all tasks: 0.0%. n counts the T1 to T3 items with every reply the comparison needs.

### Per task

95% intervals; these decide the verdicts. A hypothesis is supported at a distance only if every task's interval lies below the margin.

| Excess flips | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d14 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d10 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d7 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d5 | 5.0% [-11.9%, 23.6%], n = 20 | 15.0% [-3.5%, 36.0%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d3 | 30.0% [9.1%, 51.9%], n = 20 | 70.0% [42.6%, 85.5%], n = 20 | 25.0% [4.9%, 46.9%], n = 20 |

| Edit loss | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d14 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d10 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d7 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d5 | 5.0% [-11.9%, 23.6%], n = 20 | 10.0% [-7.7%, 30.1%], n = 20 | 5.0% [-11.9%, 23.6%], n = 20 |
| d3 | 20.0% [0.7%, 41.6%], n = 20 | 75.0% [46.8%, 88.8%], n = 20 | 40.0% [17.4%, 61.3%], n = 20 |

### Each task alone (descriptive)

| Task | H1 alone | H2 alone |
| --- | --- | --- |
| T1 | inconclusive at reassigned | inconclusive at reassigned |
| T2 | inconclusive at reassigned | inconclusive at reassigned |
| T3 | inconclusive at reassigned | inconclusive at reassigned |

The verdicts above need every task.

### The sequences under other margins (descriptive)

| Margin | H1 | H2 |
| --- | --- | --- |
| 2.5 pp | inconclusive at reassigned | inconclusive at reassigned |
| 5 pp | inconclusive at reassigned | inconclusive at reassigned |
| 10 pp | inconclusive at reassigned | inconclusive at reassigned |

### Intervals with a Bonferroni correction over all 42 tests (descriptive)

Each interval at one-sided 0.060% (z = 3.24) instead of 2.5%.

| Excess flips | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d20 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d14 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d10 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d7 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d5 | 5.0% [-31.2%, 40.6%] | 15.0% [-24.6%, 51.2%] | 0.0% [-34.4%, 34.4%] |
| d3 | 30.0% [-14.8%, 64.6%] | 70.0% [11.5%, 90.9%] | 25.0% [-18.0%, 60.4%] |

| Edit loss | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d20 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d14 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d10 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d7 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d5 | 5.0% [-31.2%, 40.6%] | 10.0% [-27.9%, 46.1%] | 5.0% [-31.2%, 40.6%] |
| d3 | 20.0% [-21.3%, 56.0%] | 75.0% [14.7%, 93.2%] | 40.0% [-8.2%, 72.4%] |

### Answers without the image (descriptive)

| Task | Valid replies | Yes, or mean count |
| --- | --- | --- |
| T1 | 0 | - |
| T2 | 0 | - |
| T3 | 0 | - |

### Invalid replies by kind (descriptive)

| Drawing | No answer line | Truncated | Blocked |
| --- | --- | --- | --- |
| with image | 0 | 0 | 0 |
| without image | 60 | 0 | 0 |

### Yes answers by correct answer on the ladder (descriptive)

| Recoloring | T1, answer yes | T1, answer no | T3, answer yes | T3, answer no |
| --- | --- | --- | --- | --- |
| d20 | 100.0% | 0.0% | 100.0% | 0.0% |
| d14 | 100.0% | 0.0% | 100.0% | 0.0% |
| d10 | 100.0% | 0.0% | 100.0% | 0.0% |
| d7 | 100.0% | 0.0% | 100.0% | 0.0% |
| d5 | 95.0% | 5.0% | 95.0% | 0.0% |
| d3 | 85.0% | 35.0% | 100.0% | 65.0% |

Cells: share of valid answers that are yes.

### Correct on both drawings of a same-palette pair (descriptive)

95% Wilson intervals.

| Palette | T1 | T2 | T3 |
| --- | --- | --- | --- |
| tab10 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 |
| d20 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 |
| d14 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 |
| d10 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 |
| d7 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 |
| d5 | 90.0% [69.9%, 97.2%], n = 20 | 80.0% [58.4%, 91.9%], n = 20 | 95.0% [76.4%, 99.1%], n = 20 |
| d3 | 55.0% [34.2%, 74.2%], n = 20 | 15.0% [5.2%, 36.0%], n = 20 | 35.0% [18.1%, 56.7%], n = 20 |

### H1 excess flips on the items at risk, where reading two colors as one changes the answer (descriptive)

T1 and T3: no items only; T2: all items.

| Recoloring | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-27.8%, 27.8%], n = 10 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-27.8%, 27.8%], n = 10 |
| d20 | 0.0% [-27.8%, 27.8%], n = 10 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-27.8%, 27.8%], n = 10 |
| d14 | 0.0% [-27.8%, 27.8%], n = 10 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-27.8%, 27.8%], n = 10 |
| d10 | 0.0% [-27.8%, 27.8%], n = 10 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-27.8%, 27.8%], n = 10 |
| d7 | 0.0% [-27.8%, 27.8%], n = 10 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-27.8%, 27.8%], n = 10 |
| d5 | 10.0% [-20.5%, 40.4%], n = 10 | 15.0% [-3.5%, 36.0%], n = 20 | 0.0% [-27.8%, 27.8%], n = 10 |
| d3 | 50.0% [8.4%, 76.3%], n = 10 | 70.0% [42.6%, 85.5%], n = 20 | 50.0% [8.4%, 76.3%], n = 10 |

### Error directions on the ladder (exploratory)

| Recoloring | False yes or overcount | False no or undercount | Invalid |
| --- | --- | --- | --- |
| d20 | 0 | 0 | 0 |
| d14 | 0 | 0 | 0 |
| d10 | 0 | 0 | 0 |
| d7 | 0 | 0 | 0 |
| d5 | 5 | 3 | 0 |
| d3 | 48 | 4 | 0 |

### Accuracy per condition and task

| Condition | T1 | T2 | T3 |
| --- | --- | --- | --- |
| original | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| repeat | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| reassigned | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d20 | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d20-edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d14 | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d14-edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d10 | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d10-edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d7 | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d7-edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d5 | 95.0% (0 inv, 0 miss) | 85.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d5-edited | 95.0% (0 inv, 0 miss) | 90.0% (0 inv, 0 miss) | 95.0% (0 inv, 0 miss) |
| d3 | 70.0% (0 inv, 0 miss) | 30.0% (0 inv, 0 miss) | 75.0% (0 inv, 0 miss) |
| d3-edited | 80.0% (0 inv, 0 miss) | 25.0% (0 inv, 0 miss) | 60.0% (0 inv, 0 miss) |
| no_image | 0.0% (20 inv, 0 miss) | 0.0% (20 inv, 0 miss) | 0.0% (20 inv, 0 miss) |

Cells: accuracy, then invalid and missing replies.

### Accuracy by hue center (exploratory)

| Hue center | d20 | d14 | d10 | d7 | d5 | d3 |
| --- | --- | --- | --- | --- | --- | --- |
| 55 | 100.0% | 100.0% | 100.0% | 100.0% | 77.8% | 38.9% |
| 115 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 66.7% |
| 175 | 100.0% | 100.0% | 100.0% | 100.0% | 94.4% | 61.1% |
| 235 | 100.0% | 100.0% | 100.0% | 100.0% | 91.7% | 50.0% |
| 295 | 100.0% | 100.0% | 100.0% | 100.0% | 95.8% | 62.5% |
| 355 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 61.1% |

### T2 accuracy by the position of u's color on the ladder (exploratory)

| u's color | d20 | d14 | d10 | d7 | d5 | d3 | Items |
| --- | --- | --- | --- | --- | --- | --- | --- |
| middle | 100.0% | 100.0% | 100.0% | 100.0% | 77.8% | 11.1% | 9 |
| outer | 100.0% | 100.0% | 100.0% | 100.0% | 95.5% | 40.9% | 11 |

Each cell pools the recolored and the edited drawing.

### T1 accuracy by the spatial separation of u and v in the drawing (exploratory)

Drawings where u and v have adjacent, different ladder colors.

| Distance between u and v | d20 | d14 | d10 | d7 | d5 | d3 | Items |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 127 to 310 px | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 57.1% | 7 |
| 328 to 431 px | 100.0% | 100.0% | 100.0% | 100.0% | 83.3% | 83.3% | 6 |
| 462 to 677 px | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 57.1% | 7 |

### Error analysis on the ladder (exploratory)

| nodes | Accuracy | Items |
| --- | --- | --- |
| 10 | 92.4% | 24 |
| 11 | 92.6% | 18 |
| 12 | 89.8% | 18 |

| edge band | Accuracy | Items |
| --- | --- | --- |
| sparse | 91.1% | 30 |
| dense | 92.2% | 30 |

| crossings | Accuracy | Items |
| --- | --- | --- |
| 0 | 91.7% | 31 |
| 1-2 | 92.0% | 27 |
| 3-5 | 87.5% | 2 |

| edited node degree | Accuracy | Items |
| --- | --- | --- |
| 1 | 85.4% | 8 |
| 2 | 91.7% | 17 |
| 3 | 92.9% | 21 |
| 4 | 94.8% | 8 |
| 5 | 91.7% | 6 |

### Accuracy on the ladder by output tokens (exploratory)

| Output tokens | Accuracy | Replies |
| --- | --- | --- |
| 5 to 49 | 98.3% | 177 |
| 50 to 79 | 96.7% | 181 |
| 80 to 123 | 95.6% | 180 |
| 124 to 616 | 76.4% | 182 |

Rows are quartiles of this model's ladder replies; tied token counts share a row.

## Gemini 3.8 Flash

Output tokens per reply, reasoning included: mean 668, median 322.

### Validity check

| Task | Accuracy, original | Bar | Gain over no image | Invalid without image | Passes |
| --- | --- | --- | --- | --- | --- |
| T1 | 100.0% [83.9%, 100.0%], n = 20 | 50.0% | 35.0% [13.2%, 56.7%], n = 20 | 2 of 20 | yes |
| T2 | 100.0% [83.9%, 100.0%], n = 20 | 20.0% | 90.0% [59.4%, 97.2%], n = 20 | 0 of 20 | yes |
| T3 | 100.0% [83.9%, 100.0%], n = 20 | 55.0% | 50.0% [25.8%, 70.1%], n = 20 | 0 of 20 | yes |

Invalid includes refusals: without the image, some models decline to answer, and that counts as wrong.

### H1: inconclusive at reassigned

### H2: inconclusive at reassigned

### The 10-unit recommendation: undetermined

The published design recommendation keeps categorical colors at least 10 CIEDE2000 units apart.

### By color distance

Means of the T1 to T3 values, for description; the verdicts use the intervals per task, below.

| Recoloring | Excess flips | Edit loss | Accuracy, recolored | Accuracy, edited | n, H1 / H2 |
| --- | --- | --- | --- | --- | --- |
| reassigned (52) | 0.0% | 0.0% | 100.0% | 100.0% | 60 / 60 |
| d20 | 0.0% | 0.0% | 100.0% | 100.0% | 60 / 60 |
| d14 | 1.7% | 0.0% | 98.3% | 100.0% | 60 / 60 |
| d10 | 6.7% | 6.7% | 93.3% | 93.3% | 60 / 60 |
| d7 | 30.0% | 23.3% | 70.0% | 76.7% | 60 / 60 |
| d5 | 41.7% | 41.7% | 58.3% | 58.3% | 60 / 60 |
| d3 | 66.7% | 66.7% | 33.3% | 33.3% | 60 / 60 |

Answers changed on the repeat, mean over all tasks: 0.0%. n counts the T1 to T3 items with every reply the comparison needs.

### Per task

95% intervals; these decide the verdicts. A hypothesis is supported at a distance only if every task's interval lies below the margin.

| Excess flips | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d14 | 0.0% [-16.1%, 16.1%], n = 20 | 5.0% [-11.9%, 23.6%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d10 | 0.0% [-16.1%, 16.1%], n = 20 | 10.0% [-7.7%, 30.1%], n = 20 | 10.0% [-7.7%, 30.1%], n = 20 |
| d7 | 15.0% [-3.5%, 36.0%], n = 20 | 45.0% [21.6%, 65.8%], n = 20 | 30.0% [9.1%, 51.9%], n = 20 |
| d5 | 15.0% [-3.5%, 36.0%], n = 20 | 80.0% [51.0%, 91.9%], n = 20 | 30.0% [9.1%, 51.9%], n = 20 |
| d3 | 50.0% [25.8%, 70.1%], n = 20 | 100.0% [67.8%, 100.0%], n = 20 | 50.0% [25.8%, 70.1%], n = 20 |

| Edit loss | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d14 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d10 | 5.0% [-11.9%, 23.6%], n = 20 | 10.0% [-7.7%, 30.1%], n = 20 | 5.0% [-11.9%, 23.6%], n = 20 |
| d7 | 10.0% [-7.7%, 30.1%], n = 20 | 45.0% [21.6%, 65.8%], n = 20 | 15.0% [-3.5%, 36.0%], n = 20 |
| d5 | 30.0% [9.1%, 51.9%], n = 20 | 60.0% [34.2%, 78.1%], n = 20 | 35.0% [13.2%, 56.7%], n = 20 |
| d3 | 50.0% [25.8%, 70.1%], n = 20 | 100.0% [67.8%, 100.0%], n = 20 | 50.0% [25.8%, 70.1%], n = 20 |

### Each task alone (descriptive)

| Task | H1 alone | H2 alone |
| --- | --- | --- |
| T1 | inconclusive at reassigned | inconclusive at reassigned |
| T2 | inconclusive at reassigned | inconclusive at reassigned |
| T3 | inconclusive at reassigned | inconclusive at reassigned |

The verdicts above need every task.

### The sequences under other margins (descriptive)

| Margin | H1 | H2 |
| --- | --- | --- |
| 2.5 pp | inconclusive at reassigned | inconclusive at reassigned |
| 5 pp | inconclusive at reassigned | inconclusive at reassigned |
| 10 pp | inconclusive at reassigned | inconclusive at reassigned |

### Intervals with a Bonferroni correction over all 42 tests (descriptive)

Each interval at one-sided 0.060% (z = 3.24) instead of 2.5%.

| Excess flips | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d20 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d14 | 0.0% [-34.4%, 34.4%] | 5.0% [-31.2%, 40.6%] | 0.0% [-34.4%, 34.4%] |
| d10 | 0.0% [-34.4%, 34.4%] | 10.0% [-27.9%, 46.1%] | 10.0% [-27.9%, 46.1%] |
| d7 | 15.0% [-24.6%, 51.2%] | 45.0% [-4.9%, 76.0%] | 30.0% [-14.8%, 64.6%] |
| d5 | 15.0% [-24.6%, 51.2%] | 80.0% [18.0%, 95.3%] | 30.0% [-14.8%, 64.6%] |
| d3 | 50.0% [-1.7%, 79.3%] | 100.0% [31.1%, 100.0%] | 50.0% [-1.7%, 79.3%] |

| Edit loss | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d20 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d14 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d10 | 5.0% [-31.2%, 40.6%] | 10.0% [-27.9%, 46.1%] | 5.0% [-31.2%, 40.6%] |
| d7 | 10.0% [-27.9%, 46.1%] | 45.0% [-4.9%, 76.0%] | 15.0% [-24.6%, 51.2%] |
| d5 | 30.0% [-14.8%, 64.6%] | 60.0% [4.9%, 85.5%] | 35.0% [-11.5%, 68.6%] |
| d3 | 50.0% [-1.7%, 79.3%] | 100.0% [31.1%, 100.0%] | 50.0% [-1.7%, 79.3%] |

### Answers without the image (descriptive)

| Task | Valid replies | Yes, or mean count |
| --- | --- | --- |
| T1 | 18 | 22.2% |
| T2 | 20 | 3.7 |
| T3 | 20 | 50.0% |

### Invalid replies by kind (descriptive)

| Drawing | No answer line | Truncated | Blocked |
| --- | --- | --- | --- |
| with image | 2 | 0 | 0 |
| without image | 2 | 0 | 0 |

### Yes answers by correct answer on the ladder (descriptive)

| Recoloring | T1, answer yes | T1, answer no | T3, answer yes | T3, answer no |
| --- | --- | --- | --- | --- |
| d20 | 100.0% | 0.0% | 100.0% | 0.0% |
| d14 | 100.0% | 0.0% | 100.0% | 0.0% |
| d10 | 100.0% | 5.0% | 100.0% | 15.0% |
| d7 | 95.0% | 20.0% | 100.0% | 45.0% |
| d5 | 90.0% | 35.0% | 90.0% | 55.0% |
| d3 | 100.0% | 100.0% | 100.0% | 100.0% |

Cells: share of valid answers that are yes.

### Correct on both drawings of a same-palette pair (descriptive)

95% Wilson intervals.

| Palette | T1 | T2 | T3 |
| --- | --- | --- | --- |
| tab10 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 |
| d20 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 |
| d14 | 100.0% [83.9%, 100.0%], n = 20 | 95.0% [76.4%, 99.1%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 |
| d10 | 95.0% [76.4%, 99.1%], n = 20 | 90.0% [69.9%, 97.2%], n = 20 | 85.0% [64.0%, 94.8%], n = 20 |
| d7 | 75.0% [53.1%, 88.8%], n = 20 | 50.0% [29.9%, 70.1%], n = 20 | 55.0% [34.2%, 74.2%], n = 20 |
| d5 | 60.0% [38.7%, 78.1%], n = 20 | 15.0% [5.2%, 36.0%], n = 20 | 45.0% [25.8%, 65.8%], n = 20 |
| d3 | 0.0% [-0.0%, 16.1%], n = 20 | 0.0% [-0.0%, 16.1%], n = 20 | 0.0% [-0.0%, 16.1%], n = 20 |

### H1 excess flips on the items at risk, where reading two colors as one changes the answer (descriptive)

T1 and T3: no items only; T2: all items.

| Recoloring | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-27.8%, 27.8%], n = 10 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-27.8%, 27.8%], n = 10 |
| d20 | 0.0% [-27.8%, 27.8%], n = 10 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-27.8%, 27.8%], n = 10 |
| d14 | 0.0% [-27.8%, 27.8%], n = 10 | 5.0% [-11.9%, 23.6%], n = 20 | 0.0% [-27.8%, 27.8%], n = 10 |
| d10 | 0.0% [-27.8%, 27.8%], n = 10 | 10.0% [-7.7%, 30.1%], n = 20 | 20.0% [-13.3%, 51.0%], n = 10 |
| d7 | 30.0% [-6.1%, 60.3%], n = 10 | 45.0% [21.6%, 65.8%], n = 20 | 60.0% [15.6%, 83.2%], n = 10 |
| d5 | 30.0% [-6.1%, 60.3%], n = 10 | 80.0% [51.0%, 91.9%], n = 20 | 60.0% [15.6%, 83.2%], n = 10 |
| d3 | 100.0% [44.5%, 100.0%], n = 10 | 100.0% [67.8%, 100.0%], n = 20 | 100.0% [44.5%, 100.0%], n = 10 |

### Error directions on the ladder (exploratory)

| Recoloring | False yes or overcount | False no or undercount | Invalid |
| --- | --- | --- | --- |
| d20 | 0 | 0 | 0 |
| d14 | 1 | 0 | 0 |
| d10 | 8 | 0 | 0 |
| d7 | 29 | 3 | 0 |
| d5 | 44 | 4 | 2 |
| d3 | 80 | 0 | 0 |

### Accuracy per condition and task

| Condition | T1 | T2 | T3 |
| --- | --- | --- | --- |
| original | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| repeat | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| reassigned | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d20 | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d20-edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d14 | 100.0% (0 inv, 0 miss) | 95.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d14-edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d10 | 100.0% (0 inv, 0 miss) | 90.0% (0 inv, 0 miss) | 90.0% (0 inv, 0 miss) |
| d10-edited | 95.0% (0 inv, 0 miss) | 90.0% (0 inv, 0 miss) | 95.0% (0 inv, 0 miss) |
| d7 | 85.0% (0 inv, 0 miss) | 55.0% (0 inv, 0 miss) | 70.0% (0 inv, 0 miss) |
| d7-edited | 90.0% (0 inv, 0 miss) | 55.0% (0 inv, 0 miss) | 85.0% (0 inv, 0 miss) |
| d5 | 85.0% (0 inv, 0 miss) | 20.0% (2 inv, 0 miss) | 70.0% (0 inv, 0 miss) |
| d5-edited | 70.0% (0 inv, 0 miss) | 40.0% (0 inv, 0 miss) | 65.0% (0 inv, 0 miss) |
| d3 | 50.0% (0 inv, 0 miss) | 0.0% (0 inv, 0 miss) | 50.0% (0 inv, 0 miss) |
| d3-edited | 50.0% (0 inv, 0 miss) | 0.0% (0 inv, 0 miss) | 50.0% (0 inv, 0 miss) |
| no_image | 65.0% (2 inv, 0 miss) | 10.0% (0 inv, 0 miss) | 50.0% (0 inv, 0 miss) |

Cells: accuracy, then invalid and missing replies.

### Accuracy by hue center (exploratory)

| Hue center | d20 | d14 | d10 | d7 | d5 | d3 |
| --- | --- | --- | --- | --- | --- | --- |
| 55 | 100.0% | 100.0% | 100.0% | 66.7% | 55.6% | 33.3% |
| 115 | 100.0% | 100.0% | 100.0% | 83.3% | 66.7% | 33.3% |
| 175 | 100.0% | 100.0% | 88.9% | 55.6% | 38.9% | 33.3% |
| 235 | 100.0% | 95.8% | 75.0% | 62.5% | 62.5% | 33.3% |
| 295 | 100.0% | 100.0% | 100.0% | 79.2% | 54.2% | 33.3% |
| 355 | 100.0% | 100.0% | 100.0% | 94.4% | 72.2% | 33.3% |

### T2 accuracy by the position of u's color on the ladder (exploratory)

| u's color | d20 | d14 | d10 | d7 | d5 | d3 | Items |
| --- | --- | --- | --- | --- | --- | --- | --- |
| middle | 100.0% | 94.4% | 88.9% | 38.9% | 11.1% | 0.0% | 9 |
| outer | 100.0% | 100.0% | 90.9% | 68.2% | 45.5% | 0.0% | 11 |

Each cell pools the recolored and the edited drawing.

### T1 accuracy by the spatial separation of u and v in the drawing (exploratory)

Drawings where u and v have adjacent, different ladder colors.

| Distance between u and v | d20 | d14 | d10 | d7 | d5 | d3 | Items |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 127 to 310 px | 100.0% | 100.0% | 85.7% | 85.7% | 57.1% | 0.0% | 7 |
| 328 to 431 px | 100.0% | 100.0% | 100.0% | 83.3% | 100.0% | 0.0% | 6 |
| 462 to 677 px | 100.0% | 100.0% | 100.0% | 71.4% | 42.9% | 0.0% | 7 |

### Error analysis on the ladder (exploratory)

| nodes | Accuracy | Items |
| --- | --- | --- |
| 10 | 76.0% | 24 |
| 11 | 78.7% | 18 |
| 12 | 74.1% | 18 |

| edge band | Accuracy | Items |
| --- | --- | --- |
| sparse | 75.6% | 30 |
| dense | 76.9% | 30 |

| crossings | Accuracy | Items |
| --- | --- | --- |
| 0 | 78.0% | 31 |
| 1-2 | 74.1% | 27 |
| 3-5 | 79.2% | 2 |

| edited node degree | Accuracy | Items |
| --- | --- | --- |
| 1 | 62.5% | 8 |
| 2 | 77.5% | 17 |
| 3 | 77.4% | 21 |
| 4 | 79.2% | 8 |
| 5 | 83.3% | 6 |

### Accuracy on the ladder by output tokens (exploratory)

| Output tokens | Accuracy | Replies |
| --- | --- | --- |
| 63 to 236 | 75.0% | 180 |
| 238 to 395 | 78.7% | 178 |
| 396 to 705 | 83.5% | 182 |
| 706 to 9519 | 67.8% | 180 |

Rows are quartiles of this model's ladder replies; tied token counts share a row.

## GPT-6.1 Sol

Output tokens per reply, reasoning included: mean 30, median 22.

### Validity check

| Task | Accuracy, original | Bar | Gain over no image | Invalid without image | Passes |
| --- | --- | --- | --- | --- | --- |
| T1 | 100.0% [83.9%, 100.0%], n = 20 | 50.0% | 35.0% [13.2%, 56.7%], n = 20 | 0 of 20 | yes |
| T2 | 95.0% [76.4%, 99.1%], n = 20 | 20.0% | 95.0% [63.6%, 99.1%], n = 20 | 20 of 20 | yes |
| T3 | 100.0% [83.9%, 100.0%], n = 20 | 55.0% | 45.0% [21.6%, 65.8%], n = 20 | 3 of 20 | yes |

Invalid includes refusals: without the image, some models decline to answer, and that counts as wrong.

### H1: inconclusive at reassigned

### H2: inconclusive at reassigned

### The 10-unit recommendation: undetermined

The published design recommendation keeps categorical colors at least 10 CIEDE2000 units apart.

### By color distance

Means of the T1 to T3 values, for description; the verdicts use the intervals per task, below.

| Recoloring | Excess flips | Edit loss | Accuracy, recolored | Accuracy, edited | n, H1 / H2 |
| --- | --- | --- | --- | --- | --- |
| reassigned (52) | 0.0% | 0.0% | 100.0% | 100.0% | 60 / 60 |
| d20 | 1.7% | 0.0% | 98.3% | 100.0% | 60 / 60 |
| d14 | 0.0% | 0.0% | 100.0% | 100.0% | 60 / 60 |
| d10 | 0.0% | 3.3% | 100.0% | 96.7% | 60 / 60 |
| d7 | 3.3% | 3.3% | 96.7% | 95.0% | 60 / 60 |
| d5 | 11.7% | 15.0% | 88.3% | 83.3% | 60 / 60 |
| d3 | 40.0% | 41.7% | 58.3% | 58.3% | 60 / 60 |

Answers changed on the repeat, mean over all tasks: 1.7%. n counts the T1 to T3 items with every reply the comparison needs.

### Per task

95% intervals; these decide the verdicts. A hypothesis is supported at a distance only if every task's interval lies below the margin.

| Excess flips | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d20 | 0.0% [-16.1%, 16.1%], n = 20 | 5.0% [-11.9%, 23.6%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d14 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d10 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d7 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 10.0% [-7.7%, 30.1%], n = 20 |
| d5 | 5.0% [-11.9%, 23.6%], n = 20 | 15.0% [-3.5%, 36.0%], n = 20 | 15.0% [-3.5%, 36.0%], n = 20 |
| d3 | 30.0% [9.1%, 51.9%], n = 20 | 65.0% [38.4%, 81.9%], n = 20 | 25.0% [4.9%, 46.9%], n = 20 |

| Edit loss | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d14 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d10 | 0.0% [-16.1%, 16.1%], n = 20 | 5.0% [-11.9%, 23.6%], n = 20 | 5.0% [-11.9%, 23.6%], n = 20 |
| d7 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 10.0% [-7.7%, 30.1%], n = 20 |
| d5 | 0.0% [-16.1%, 16.1%], n = 20 | 30.0% [9.1%, 51.9%], n = 20 | 15.0% [-3.5%, 36.0%], n = 20 |
| d3 | 30.0% [9.1%, 51.9%], n = 20 | 55.0% [30.0%, 74.2%], n = 20 | 40.0% [17.4%, 61.3%], n = 20 |

### Each task alone (descriptive)

| Task | H1 alone | H2 alone |
| --- | --- | --- |
| T1 | inconclusive at reassigned | inconclusive at reassigned |
| T2 | inconclusive at reassigned | inconclusive at reassigned |
| T3 | inconclusive at reassigned | inconclusive at reassigned |

The verdicts above need every task.

### The sequences under other margins (descriptive)

| Margin | H1 | H2 |
| --- | --- | --- |
| 2.5 pp | inconclusive at reassigned | inconclusive at reassigned |
| 5 pp | inconclusive at reassigned | inconclusive at reassigned |
| 10 pp | inconclusive at reassigned | inconclusive at reassigned |

### Intervals with a Bonferroni correction over all 42 tests (descriptive)

Each interval at one-sided 0.060% (z = 3.24) instead of 2.5%.

| Excess flips | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d20 | 0.0% [-34.4%, 34.4%] | 5.0% [-31.2%, 40.6%] | 0.0% [-34.4%, 34.4%] |
| d14 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d10 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d7 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 10.0% [-27.9%, 46.1%] |
| d5 | 5.0% [-31.2%, 40.6%] | 15.0% [-24.6%, 51.2%] | 15.0% [-24.6%, 51.2%] |
| d3 | 30.0% [-14.8%, 64.6%] | 65.0% [8.2%, 88.3%] | 25.0% [-18.0%, 60.4%] |

| Edit loss | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d20 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d14 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d10 | 0.0% [-34.4%, 34.4%] | 5.0% [-31.2%, 40.6%] | 5.0% [-31.2%, 40.6%] |
| d7 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 10.0% [-27.9%, 46.1%] |
| d5 | 0.0% [-34.4%, 34.4%] | 30.0% [-14.8%, 64.6%] | 15.0% [-24.6%, 51.2%] |
| d3 | 30.0% [-14.8%, 64.6%] | 55.0% [1.6%, 82.5%] | 40.0% [-8.2%, 72.4%] |

### Answers without the image (descriptive)

| Task | Valid replies | Yes, or mean count |
| --- | --- | --- |
| T1 | 20 | 15.0% |
| T2 | 0 | - |
| T3 | 17 | 70.6% |

### Invalid replies by kind (descriptive)

| Drawing | No answer line | Truncated | Blocked |
| --- | --- | --- | --- |
| with image | 0 | 0 | 0 |
| without image | 23 | 0 | 0 |

### Yes answers by correct answer on the ladder (descriptive)

| Recoloring | T1, answer yes | T1, answer no | T3, answer yes | T3, answer no |
| --- | --- | --- | --- | --- |
| d20 | 100.0% | 0.0% | 100.0% | 0.0% |
| d14 | 100.0% | 0.0% | 100.0% | 0.0% |
| d10 | 100.0% | 0.0% | 100.0% | 5.0% |
| d7 | 100.0% | 0.0% | 100.0% | 20.0% |
| d5 | 100.0% | 5.0% | 100.0% | 30.0% |
| d3 | 100.0% | 60.0% | 100.0% | 65.0% |

Cells: share of valid answers that are yes.

### Correct on both drawings of a same-palette pair (descriptive)

95% Wilson intervals.

| Palette | T1 | T2 | T3 |
| --- | --- | --- | --- |
| tab10 | 100.0% [83.9%, 100.0%], n = 20 | 95.0% [76.4%, 99.1%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 |
| d20 | 100.0% [83.9%, 100.0%], n = 20 | 95.0% [76.4%, 99.1%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 |
| d14 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 |
| d10 | 100.0% [83.9%, 100.0%], n = 20 | 95.0% [76.4%, 99.1%], n = 20 | 95.0% [76.4%, 99.1%], n = 20 |
| d7 | 100.0% [83.9%, 100.0%], n = 20 | 95.0% [76.4%, 99.1%], n = 20 | 80.0% [58.4%, 91.9%], n = 20 |
| d5 | 95.0% [76.4%, 99.1%], n = 20 | 65.0% [43.3%, 81.9%], n = 20 | 70.0% [48.1%, 85.5%], n = 20 |
| d3 | 40.0% [21.9%, 61.3%], n = 20 | 25.0% [11.2%, 46.9%], n = 20 | 35.0% [18.1%, 56.7%], n = 20 |

### H1 excess flips on the items at risk, where reading two colors as one changes the answer (descriptive)

T1 and T3: no items only; T2: all items.

| Recoloring | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-27.8%, 27.8%], n = 10 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-27.8%, 27.8%], n = 10 |
| d20 | 0.0% [-27.8%, 27.8%], n = 10 | 5.0% [-11.9%, 23.6%], n = 20 | 0.0% [-27.8%, 27.8%], n = 10 |
| d14 | 0.0% [-27.8%, 27.8%], n = 10 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-27.8%, 27.8%], n = 10 |
| d10 | 0.0% [-27.8%, 27.8%], n = 10 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-27.8%, 27.8%], n = 10 |
| d7 | 0.0% [-27.8%, 27.8%], n = 10 | 0.0% [-16.1%, 16.1%], n = 20 | 20.0% [-13.3%, 51.0%], n = 10 |
| d5 | 10.0% [-20.5%, 40.4%], n = 10 | 15.0% [-3.5%, 36.0%], n = 20 | 30.0% [-6.1%, 60.3%], n = 10 |
| d3 | 60.0% [15.6%, 83.2%], n = 10 | 65.0% [38.4%, 81.9%], n = 20 | 50.0% [8.4%, 76.3%], n = 10 |

### Error directions on the ladder (exploratory)

| Recoloring | False yes or overcount | False no or undercount | Invalid |
| --- | --- | --- | --- |
| d20 | 1 | 0 | 0 |
| d14 | 0 | 0 | 0 |
| d10 | 2 | 0 | 0 |
| d7 | 5 | 0 | 0 |
| d5 | 13 | 4 | 0 |
| d3 | 50 | 0 | 0 |

### Accuracy per condition and task

| Condition | T1 | T2 | T3 |
| --- | --- | --- | --- |
| original | 100.0% (0 inv, 0 miss) | 95.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| repeat | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| reassigned | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d20 | 100.0% (0 inv, 0 miss) | 95.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d20-edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d14 | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d14-edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d10 | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d10-edited | 100.0% (0 inv, 0 miss) | 95.0% (0 inv, 0 miss) | 95.0% (0 inv, 0 miss) |
| d7 | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 90.0% (0 inv, 0 miss) |
| d7-edited | 100.0% (0 inv, 0 miss) | 95.0% (0 inv, 0 miss) | 90.0% (0 inv, 0 miss) |
| d5 | 95.0% (0 inv, 0 miss) | 85.0% (0 inv, 0 miss) | 85.0% (0 inv, 0 miss) |
| d5-edited | 100.0% (0 inv, 0 miss) | 65.0% (0 inv, 0 miss) | 85.0% (0 inv, 0 miss) |
| d3 | 70.0% (0 inv, 0 miss) | 30.0% (0 inv, 0 miss) | 75.0% (0 inv, 0 miss) |
| d3-edited | 70.0% (0 inv, 0 miss) | 45.0% (0 inv, 0 miss) | 60.0% (0 inv, 0 miss) |
| no_image | 65.0% (0 inv, 0 miss) | 0.0% (20 inv, 0 miss) | 55.0% (3 inv, 0 miss) |

Cells: accuracy, then invalid and missing replies.

### Accuracy by hue center (exploratory)

| Hue center | d20 | d14 | d10 | d7 | d5 | d3 |
| --- | --- | --- | --- | --- | --- | --- |
| 55 | 100.0% | 100.0% | 100.0% | 94.4% | 94.4% | 55.6% |
| 115 | 100.0% | 100.0% | 100.0% | 100.0% | 83.3% | 77.8% |
| 175 | 100.0% | 100.0% | 100.0% | 100.0% | 83.3% | 50.0% |
| 235 | 100.0% | 100.0% | 95.8% | 87.5% | 79.2% | 66.7% |
| 295 | 100.0% | 100.0% | 100.0% | 100.0% | 95.8% | 58.3% |
| 355 | 94.4% | 100.0% | 94.4% | 94.4% | 77.8% | 38.9% |

### T2 accuracy by the position of u's color on the ladder (exploratory)

| u's color | d20 | d14 | d10 | d7 | d5 | d3 | Items |
| --- | --- | --- | --- | --- | --- | --- | --- |
| middle | 100.0% | 100.0% | 94.4% | 94.4% | 61.1% | 16.7% | 9 |
| outer | 95.5% | 100.0% | 100.0% | 100.0% | 86.4% | 54.5% | 11 |

Each cell pools the recolored and the edited drawing.

### T1 accuracy by the spatial separation of u and v in the drawing (exploratory)

Drawings where u and v have adjacent, different ladder colors.

| Distance between u and v | d20 | d14 | d10 | d7 | d5 | d3 | Items |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 127 to 310 px | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 42.9% | 7 |
| 328 to 431 px | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 50.0% | 6 |
| 462 to 677 px | 100.0% | 100.0% | 100.0% | 100.0% | 85.7% | 28.6% | 7 |

### Error analysis on the ladder (exploratory)

| nodes | Accuracy | Items |
| --- | --- | --- |
| 10 | 90.6% | 24 |
| 11 | 90.7% | 18 |
| 12 | 87.0% | 18 |

| edge band | Accuracy | Items |
| --- | --- | --- |
| sparse | 91.7% | 30 |
| dense | 87.5% | 30 |

| crossings | Accuracy | Items |
| --- | --- | --- |
| 0 | 92.5% | 31 |
| 1-2 | 85.8% | 27 |
| 3-5 | 95.8% | 2 |

| edited node degree | Accuracy | Items |
| --- | --- | --- |
| 1 | 84.4% | 8 |
| 2 | 88.7% | 17 |
| 3 | 90.1% | 21 |
| 4 | 92.7% | 8 |
| 5 | 93.1% | 6 |

### Accuracy on the ladder by output tokens (exploratory)

| Output tokens | Accuracy | Replies |
| --- | --- | --- |
| 5 to 22 | 93.6% | 359 |
| 23 to 33 | 89.5% | 171 |
| 34 to 275 | 82.1% | 190 |

Rows are quartiles of this model's ladder replies; tied token counts share a row.

## Qwen3.8-27B

Output tokens per reply, reasoning included: mean 365, median 303.

### Validity check

| Task | Accuracy, original | Bar | Gain over no image | Invalid without image | Passes |
| --- | --- | --- | --- | --- | --- |
| T1 | 100.0% [83.9%, 100.0%], n = 20 | 50.0% | 40.0% [17.4%, 61.3%], n = 20 | 0 of 20 | yes |
| T2 | 100.0% [83.9%, 100.0%], n = 20 | 20.0% | 80.0% [51.0%, 91.9%], n = 20 | 2 of 20 | yes |
| T3 | 100.0% [83.9%, 100.0%], n = 20 | 55.0% | 50.0% [25.8%, 70.1%], n = 20 | 0 of 20 | yes |

Invalid includes refusals: without the image, some models decline to answer, and that counts as wrong.

### H1: inconclusive at reassigned

### H2: inconclusive at reassigned

### The 10-unit recommendation: undetermined

The published design recommendation keeps categorical colors at least 10 CIEDE2000 units apart.

### By color distance

Means of the T1 to T3 values, for description; the verdicts use the intervals per task, below.

| Recoloring | Excess flips | Edit loss | Accuracy, recolored | Accuracy, edited | n, H1 / H2 |
| --- | --- | --- | --- | --- | --- |
| reassigned (52) | 0.0% | 0.0% | 100.0% | 100.0% | 60 / 60 |
| d20 | 1.7% | 1.7% | 98.3% | 98.3% | 60 / 60 |
| d14 | 5.0% | 6.7% | 95.0% | 93.3% | 60 / 60 |
| d10 | 20.0% | 18.3% | 80.0% | 81.7% | 60 / 60 |
| d7 | 36.7% | 28.3% | 63.3% | 71.7% | 60 / 60 |
| d5 | 43.3% | 60.0% | 56.7% | 40.0% | 60 / 60 |
| d3 | 58.3% | 61.7% | 41.7% | 38.3% | 60 / 60 |

Answers changed on the repeat, mean over all tasks: 0.0%. n counts the T1 to T3 items with every reply the comparison needs.

### Per task

95% intervals; these decide the verdicts. A hypothesis is supported at a distance only if every task's interval lies below the margin.

| Excess flips | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 5.0% [-11.9%, 23.6%], n = 20 |
| d14 | 5.0% [-11.9%, 23.6%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 10.0% [-7.7%, 30.1%], n = 20 |
| d10 | 15.0% [-3.5%, 36.0%], n = 20 | 25.0% [4.9%, 46.9%], n = 20 | 20.0% [0.7%, 41.6%], n = 20 |
| d7 | 20.0% [0.7%, 41.6%], n = 20 | 55.0% [30.0%, 74.2%], n = 20 | 35.0% [13.2%, 56.7%], n = 20 |
| d5 | 10.0% [-7.7%, 30.1%], n = 20 | 65.0% [38.4%, 81.9%], n = 20 | 55.0% [30.0%, 74.2%], n = 20 |
| d3 | 45.0% [21.6%, 65.8%], n = 20 | 85.0% [55.2%, 94.8%], n = 20 | 45.0% [21.6%, 65.8%], n = 20 |

| Edit loss | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 |
| d20 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-16.1%, 16.1%], n = 20 | 5.0% [-11.9%, 23.6%], n = 20 |
| d14 | 5.0% [-11.9%, 23.6%], n = 20 | 10.0% [-7.7%, 30.1%], n = 20 | 5.0% [-11.9%, 23.6%], n = 20 |
| d10 | 15.0% [-3.5%, 36.0%], n = 20 | 25.0% [4.9%, 46.9%], n = 20 | 15.0% [-3.5%, 36.0%], n = 20 |
| d7 | 20.0% [0.7%, 41.6%], n = 20 | 40.0% [17.4%, 61.3%], n = 20 | 25.0% [4.9%, 46.9%], n = 20 |
| d5 | 45.0% [21.6%, 65.8%], n = 20 | 90.0% [59.4%, 97.2%], n = 20 | 45.0% [21.6%, 65.8%], n = 20 |
| d3 | 45.0% [21.6%, 65.8%], n = 20 | 95.0% [63.6%, 99.1%], n = 20 | 45.0% [21.6%, 65.8%], n = 20 |

### Each task alone (descriptive)

| Task | H1 alone | H2 alone |
| --- | --- | --- |
| T1 | inconclusive at reassigned | inconclusive at reassigned |
| T2 | inconclusive at reassigned | inconclusive at reassigned |
| T3 | inconclusive at reassigned | inconclusive at reassigned |

The verdicts above need every task.

### The sequences under other margins (descriptive)

| Margin | H1 | H2 |
| --- | --- | --- |
| 2.5 pp | inconclusive at reassigned | inconclusive at reassigned |
| 5 pp | inconclusive at reassigned | inconclusive at reassigned |
| 10 pp | inconclusive at reassigned | inconclusive at reassigned |

### Intervals with a Bonferroni correction over all 42 tests (descriptive)

Each interval at one-sided 0.060% (z = 3.24) instead of 2.5%.

| Excess flips | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d20 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 5.0% [-31.2%, 40.6%] |
| d14 | 5.0% [-31.2%, 40.6%] | 0.0% [-34.4%, 34.4%] | 10.0% [-27.9%, 46.1%] |
| d10 | 15.0% [-24.6%, 51.2%] | 25.0% [-18.0%, 60.4%] | 20.0% [-21.3%, 56.0%] |
| d7 | 20.0% [-21.3%, 56.0%] | 55.0% [1.6%, 82.5%] | 35.0% [-11.5%, 68.6%] |
| d5 | 10.0% [-27.9%, 46.1%] | 65.0% [8.2%, 88.3%] | 55.0% [1.6%, 82.5%] |
| d3 | 45.0% [-4.9%, 76.0%] | 85.0% [21.3%, 97.1%] | 45.0% [-4.9%, 76.0%] |

| Edit loss | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] |
| d20 | 0.0% [-34.4%, 34.4%] | 0.0% [-34.4%, 34.4%] | 5.0% [-31.2%, 40.6%] |
| d14 | 5.0% [-31.2%, 40.6%] | 10.0% [-27.9%, 46.1%] | 5.0% [-31.2%, 40.6%] |
| d10 | 15.0% [-24.6%, 51.2%] | 25.0% [-18.0%, 60.4%] | 15.0% [-24.6%, 51.2%] |
| d7 | 20.0% [-21.3%, 56.0%] | 40.0% [-8.2%, 72.4%] | 25.0% [-18.0%, 60.4%] |
| d5 | 45.0% [-4.9%, 76.0%] | 90.0% [24.6%, 98.6%] | 45.0% [-4.9%, 76.0%] |
| d3 | 45.0% [-4.9%, 76.0%] | 95.0% [27.8%, 99.6%] | 45.0% [-4.9%, 76.0%] |

### Answers without the image (descriptive)

| Task | Valid replies | Yes, or mean count |
| --- | --- | --- |
| T1 | 20 | 20.0% |
| T2 | 18 | 2.9 |
| T3 | 20 | 10.0% |

### Invalid replies by kind (descriptive)

| Drawing | No answer line | Truncated | Blocked |
| --- | --- | --- | --- |
| with image | 0 | 0 | 0 |
| without image | 2 | 0 | 0 |

### Yes answers by correct answer on the ladder (descriptive)

| Recoloring | T1, answer yes | T1, answer no | T3, answer yes | T3, answer no |
| --- | --- | --- | --- | --- |
| d20 | 100.0% | 0.0% | 95.0% | 5.0% |
| d14 | 100.0% | 10.0% | 100.0% | 15.0% |
| d10 | 85.0% | 15.0% | 100.0% | 35.0% |
| d7 | 100.0% | 40.0% | 95.0% | 55.0% |
| d5 | 85.0% | 40.0% | 85.0% | 85.0% |
| d3 | 95.0% | 85.0% | 100.0% | 90.0% |

Cells: share of valid answers that are yes.

### Correct on both drawings of a same-palette pair (descriptive)

95% Wilson intervals.

| Palette | T1 | T2 | T3 |
| --- | --- | --- | --- |
| tab10 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 |
| d20 | 100.0% [83.9%, 100.0%], n = 20 | 100.0% [83.9%, 100.0%], n = 20 | 90.0% [69.9%, 97.2%], n = 20 |
| d14 | 90.0% [69.9%, 97.2%], n = 20 | 90.0% [69.9%, 97.2%], n = 20 | 85.0% [64.0%, 94.8%], n = 20 |
| d10 | 75.0% [53.1%, 88.8%], n = 20 | 70.0% [48.1%, 85.5%], n = 20 | 65.0% [43.3%, 81.9%], n = 20 |
| d7 | 60.0% [38.7%, 78.1%], n = 20 | 45.0% [25.8%, 65.8%], n = 20 | 45.0% [25.8%, 65.8%], n = 20 |
| d5 | 50.0% [29.9%, 70.1%], n = 20 | 10.0% [2.8%, 30.1%], n = 20 | 15.0% [5.2%, 36.0%], n = 20 |
| d3 | 15.0% [5.2%, 36.0%], n = 20 | 5.0% [0.9%, 23.6%], n = 20 | 10.0% [2.8%, 30.1%], n = 20 |

### H1 excess flips on the items at risk, where reading two colors as one changes the answer (descriptive)

T1 and T3: no items only; T2: all items.

| Recoloring | T1 | T2 | T3 |
| --- | --- | --- | --- |
| reassigned | 0.0% [-27.8%, 27.8%], n = 10 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-27.8%, 27.8%], n = 10 |
| d20 | 0.0% [-27.8%, 27.8%], n = 10 | 0.0% [-16.1%, 16.1%], n = 20 | 0.0% [-27.8%, 27.8%], n = 10 |
| d14 | 10.0% [-20.5%, 40.4%], n = 10 | 0.0% [-16.1%, 16.1%], n = 20 | 20.0% [-13.3%, 51.0%], n = 10 |
| d10 | 20.0% [-13.3%, 51.0%], n = 10 | 25.0% [4.9%, 46.9%], n = 20 | 40.0% [1.1%, 68.7%], n = 10 |
| d7 | 40.0% [1.1%, 68.7%], n = 10 | 55.0% [30.0%, 74.2%], n = 20 | 70.0% [22.8%, 89.2%], n = 10 |
| d5 | 20.0% [-13.3%, 51.0%], n = 10 | 65.0% [38.4%, 81.9%], n = 20 | 100.0% [44.5%, 100.0%], n = 10 |
| d3 | 80.0% [30.0%, 94.3%], n = 10 | 85.0% [55.2%, 94.8%], n = 20 | 90.0% [37.3%, 98.2%], n = 10 |

### Error directions on the ladder (exploratory)

| Recoloring | False yes or overcount | False no or undercount | Invalid |
| --- | --- | --- | --- |
| d20 | 1 | 1 | 0 |
| d14 | 7 | 0 | 0 |
| d10 | 19 | 4 | 0 |
| d7 | 35 | 4 | 0 |
| d5 | 50 | 12 | 0 |
| d3 | 70 | 2 | 0 |

### Accuracy per condition and task

| Condition | T1 | T2 | T3 |
| --- | --- | --- | --- |
| original | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| repeat | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| reassigned | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) |
| d20 | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 95.0% (0 inv, 0 miss) |
| d20-edited | 100.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 95.0% (0 inv, 0 miss) |
| d14 | 95.0% (0 inv, 0 miss) | 100.0% (0 inv, 0 miss) | 90.0% (0 inv, 0 miss) |
| d14-edited | 95.0% (0 inv, 0 miss) | 90.0% (0 inv, 0 miss) | 95.0% (0 inv, 0 miss) |
| d10 | 85.0% (0 inv, 0 miss) | 75.0% (0 inv, 0 miss) | 80.0% (0 inv, 0 miss) |
| d10-edited | 85.0% (0 inv, 0 miss) | 75.0% (0 inv, 0 miss) | 85.0% (0 inv, 0 miss) |
| d7 | 80.0% (0 inv, 0 miss) | 45.0% (0 inv, 0 miss) | 65.0% (0 inv, 0 miss) |
| d7-edited | 80.0% (0 inv, 0 miss) | 60.0% (0 inv, 0 miss) | 75.0% (0 inv, 0 miss) |
| d5 | 90.0% (0 inv, 0 miss) | 35.0% (0 inv, 0 miss) | 45.0% (0 inv, 0 miss) |
| d5-edited | 55.0% (0 inv, 0 miss) | 10.0% (0 inv, 0 miss) | 55.0% (0 inv, 0 miss) |
| d3 | 55.0% (0 inv, 0 miss) | 15.0% (0 inv, 0 miss) | 55.0% (0 inv, 0 miss) |
| d3-edited | 55.0% (0 inv, 0 miss) | 5.0% (0 inv, 0 miss) | 55.0% (0 inv, 0 miss) |
| no_image | 60.0% (0 inv, 0 miss) | 20.0% (2 inv, 0 miss) | 50.0% (0 inv, 0 miss) |

Cells: accuracy, then invalid and missing replies.

### Accuracy by hue center (exploratory)

| Hue center | d20 | d14 | d10 | d7 | d5 | d3 |
| --- | --- | --- | --- | --- | --- | --- |
| 55 | 94.4% | 100.0% | 83.3% | 61.1% | 55.6% | 38.9% |
| 115 | 100.0% | 100.0% | 94.4% | 94.4% | 61.1% | 44.4% |
| 175 | 94.4% | 88.9% | 72.2% | 55.6% | 33.3% | 33.3% |
| 235 | 100.0% | 83.3% | 66.7% | 62.5% | 41.7% | 33.3% |
| 295 | 100.0% | 95.8% | 83.3% | 62.5% | 50.0% | 45.8% |
| 355 | 100.0% | 100.0% | 88.9% | 72.2% | 50.0% | 44.4% |

### T2 accuracy by the position of u's color on the ladder (exploratory)

| u's color | d20 | d14 | d10 | d7 | d5 | d3 | Items |
| --- | --- | --- | --- | --- | --- | --- | --- |
| middle | 100.0% | 94.4% | 61.1% | 44.4% | 16.7% | 0.0% | 9 |
| outer | 100.0% | 95.5% | 86.4% | 59.1% | 27.3% | 18.2% | 11 |

Each cell pools the recolored and the edited drawing.

### T1 accuracy by the spatial separation of u and v in the drawing (exploratory)

Drawings where u and v have adjacent, different ladder colors.

| Distance between u and v | d20 | d14 | d10 | d7 | d5 | d3 | Items |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 127 to 310 px | 100.0% | 100.0% | 85.7% | 57.1% | 71.4% | 14.3% | 7 |
| 328 to 431 px | 100.0% | 66.7% | 83.3% | 33.3% | 66.7% | 16.7% | 6 |
| 462 to 677 px | 100.0% | 100.0% | 85.7% | 85.7% | 42.9% | 14.3% | 7 |

### Error analysis on the ladder (exploratory)

| nodes | Accuracy | Items |
| --- | --- | --- |
| 10 | 71.5% | 24 |
| 11 | 72.2% | 18 |
| 12 | 70.8% | 18 |

| edge band | Accuracy | Items |
| --- | --- | --- |
| sparse | 69.7% | 30 |
| dense | 73.3% | 30 |

| crossings | Accuracy | Items |
| --- | --- | --- |
| 0 | 72.6% | 31 |
| 1-2 | 70.4% | 27 |
| 3-5 | 70.8% | 2 |

| edited node degree | Accuracy | Items |
| --- | --- | --- |
| 1 | 59.4% | 8 |
| 2 | 75.0% | 17 |
| 3 | 71.0% | 21 |
| 4 | 76.0% | 8 |
| 5 | 73.6% | 6 |

### Accuracy on the ladder by output tokens (exploratory)

| Output tokens | Accuracy | Replies |
| --- | --- | --- |
| 55 to 217 | 77.8% | 176 |
| 218 to 324 | 77.2% | 184 |
| 325 to 463 | 69.4% | 180 |
| 466 to 3350 | 61.7% | 180 |

Rows are quartiles of this model's ladder replies; tied token counts share a row.

## Parser against hand coding

172 of 172 distinct replies hand coded, 0 not yet; 0 disagree with the parser; 0 queries have no reply. The parser check passes.


