# Standalone, standard library only. SYNTHETIC logs (generated here), not real traffic.
import random, statistics
from dataclasses import dataclass, field

@dataclass
class RagLog:
    request_id: str
    query: str
    chunk_ids: list           # retrieved chunk ids, in rank order
    scores: list              # similarity scores, same order
    prompt_tokens: int
    answer: str
    citations: list           # chunk ids the answer cites
    latency_ms: dict          # per stage: embed, search, rerank, generate
    index_version: str = "v1"
    feedback: str = None      # "up", "down" or None

random.seed(7)
def make_logs(n, search_scale=1.0):
    logs = []
    for i in range(n):
        lat = {"embed": random.lognormvariate(3.0, 0.25),
               "search": random.lognormvariate(3.2, 0.35) * search_scale,
               "rerank": random.lognormvariate(4.2, 0.30),
               "generate": random.lognormvariate(6.3, 0.40)}
        logs.append(RagLog(f"r{i}", "toy query", [f"c{i}a", f"c{i}b"], [0.8, 0.6],
                           900, "toy answer", [f"c{i}a"], lat))
    return logs

def pct(vals, q):                       # nearest-rank percentile
    s = sorted(vals); return s[min(len(s) - 1, max(0, int(round(q / 100 * len(s) + 0.5)) - 1))]

def stage_table(logs):
    return {st: (pct([l.latency_ms[st] for l in logs], 50), pct([l.latency_ms[st] for l in logs], 95))
            for st in logs[0].latency_ms}

def regressions(base, cur, tol=1.25):
    out = []
    for st in base:
        b95, c95 = base[st][1], cur[st][1]
        if c95 > tol * b95: out.append((st, b95, c95, c95 / b95))
    return out

base = stage_table(make_logs(5000))                      # last week (synthetic)
cur = stage_table(make_logs(5000, search_scale=1.8))     # today: search stage made 1.8x slower on purpose
print("stage      base p50/p95 (ms)   today p50/p95 (ms)")
for st in base:
    print(f"{st:9s}  {base[st][0]:7.1f} /{base[st][1]:7.1f}   {cur[st][0]:7.1f} /{cur[st][1]:7.1f}")
for st, b, c, r in regressions(base, cur):
    print(f"ALERT: {st} p95 {b:.1f} -> {c:.1f} ms ({r:.2f}x, threshold 1.25x)")

# thumbs-down -> eval case (cross-ref Q40): keep query, retrieved ids, and a slot for a human label
logs = make_logs(3); logs[1].feedback = "down"
cases = [{"query": l.query, "retrieved": l.chunk_ids, "expected_chunk_ids": None, "note": "label me"}
         for l in logs if l.feedback == "down"]
print("eval cases from thumbs-down:", cases)
