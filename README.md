# How Do LLMs Perceive Color in Graph Drawings?

Code and data for the bachelor's thesis of the same name.

Two multimodal models answer simple questions about generated graph drawings whose nodes fall
into three color groups. Each drawing is recolored, which should change no answer, and edited, so
that one node moves to another group and the answer of a color task should change. A control task
asks about an edge, which no color can change. The colors step from 52 down to 3 CIEDE2000 units
apart, past the design recommendation of 10 units. The question: down to which color distance do a
model's answers hold, and is 10 units enough?

## Results

- **Claude Opus 5.5** holds down to 7 units, so the 10-unit recommendation is enough for it.
- **Qwen3.8-27B** holds down to 20 units. The formal tests stopped inconclusive at 14, so its
  verdict on 10 units is undetermined; at 10 units it gets about one color-task answer in five wrong.
- **The control:** both models answer at least 99% of the control questions correctly at every
  distance, so the failures concern the colors: the models still read the edges.

The main run's numbers are in `data/main/results.md`.

## Contents

| Path | What it is |
| --- | --- |
| `study/generate.py` | Builds the items: graph, groups, question, answer and 15 images each |
| `study/query.py` | Sends every query to one model and logs every request and reply |
| `study/analyze.py` | Scores the replies and computes the validity check, H1 and H2 |
| `study/simulate.py` | Runs the analysis on simulated models to check the decision rule |
| `study/test_*.py` | Tests |
| `data/` | Items, queries, replies and results: `main/` and the final `pilot/` (see `data/README.md`) |
| `checks/` | Checks behind numbers in the thesis: the stimuli (`stimuli.py`) and Qwen's reasoning effort (`qwen-effort.py`) |

## Reproducing

Everything runs from the repository root with [uv](https://docs.astral.sh/uv/).

1. Tests: `uv run pytest study`.
2. Images: `uv run study/generate.py main`. The images are not in git; the same code and seed draw
   them again, after checking that the committed manifest is the one the code generates. Their
   SHA-256 hashes are in `data/main/queries.jsonl`.
3. Queries: `uv run --env-file .env study/query.py main claude` (or `qwen`; the pilot also used
   `gpt` and `gemini`). API keys go in `.env`: `ANTHROPIC_API_KEY`, `OPENROUTER_API_KEY`,
   `OPENAI_API_KEY`, `GEMINI_API_KEY`. A stopped run resumes when started again.
4. Analysis: `uv run study/analyze.py main` writes `data/main/results.md`.

Replace `main` with `pilot` for the final pilot.

## Settings

The request settings are in `study/query.py`. The thesis's appendix (Implementation details)
explains them, and how we checked that each model received the image unresized and that Qwen
honored its reasoning effort.

## License

The code is under the MIT license (`LICENSE`), and the data under CC BY 4.0 (`data/README.md`,
which also carries the canary string that keeps the data out of training sets).
