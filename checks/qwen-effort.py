"""Does DeepInfra honor Qwen's reasoning effort? The same 20 pilot queries at low and high effort.

Run: uv run --env-file .env checks/qwen-effort.py
Output in qwen-effort-output.txt: high reasoned more than low on 17 of 20 (median 286 vs. 181 tokens).
Costs under one cent. Reads the pilot queries; writes nothing."""

import json
import statistics
import sys
from pathlib import Path

Root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Root / "study"))
import query

queries = query.load_queries(Root / "data/pilot")
chosen = [q for q in queries if q["id"].endswith("-d5")][:20]
calls = query.OpenRouterCalls()
results = {}
for effort in ("low", "high"):
    query.Effort = effort
    tokens = []
    for q in chosen:
        reply = calls.call(q)
        raw = reply.get("raw") or {}
        reasoning = (raw.get("usage") or {}).get("completion_tokens_details", {}).get("reasoning_tokens")
        tokens.append(reasoning)
        print(effort, q["id"], "ok" if reply.get("ok") else reply.get("error", "")[:200], "reasoning tokens:", reasoning, "provider:", raw.get("provider"), flush=True)
    results[effort] = tokens
print(json.dumps(results))
for effort, t in results.items():
    t = [x for x in t if x is not None]
    print(effort, "median reasoning tokens:", statistics.median(t) if t else None)
