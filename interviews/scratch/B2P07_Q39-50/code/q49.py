# Standalone, stdlib only. EVERY number is an ASSUMPTION (not a benchmark, not a finding from any paper). It shows HOW to decide, using your own measured numbers.
OPTIONS = {   # name: (recall@10 on YOUR golden set, p95 latency ms, one-time index cost units, storage GB, monthly update cost units, robustness 0-1 (paraphrase/typo/stress set))
 "BM25 only":                         (0.62,  40,   1,   2, 0.1, 0.60),
 "dense only (small encoder)":        (0.68,  60,   8,  30, 0.8, 0.70),
 "hybrid (BM25+dense, RRF)":          (0.74,  90,   9,  32, 0.9, 0.78),
 "hybrid + cross-encoder rerank":     (0.81, 260,   9,  32, 0.9, 0.84),   # <- the tuned baseline
 "hybrid + LLM reranker (top 20)":    (0.83, 1400,  9,  32, 0.9, 0.86),
 "LLM-embedding retriever":           (0.80, 180,  60, 120, 6.0, 0.82),
 "contextual index (LLM per chunk)+hybrid+rerank": (0.85, 270, 45, 40, 4.0, 0.88),
}
BASE = "hybrid + cross-encoder rerank"
LAT_SLO, INDEX_BUDGET, MONTHLY_BUDGET, STORAGE_CAP = 600, 50, 3.0, 100       # ASSUMED constraints
print(f"{'option':48s}{'R@10':>6s}{'ms':>6s}{'index':>7s}{'GB':>5s}{'upd/mo':>8s}{'robust':>8s}")
for n, (r, l, ix, gb, up, rb) in OPTIONS.items(): print(f"{n:48s}{r:>6.2f}{l:>6d}{ix:>7d}{gb:>5d}{up:>8.1f}{rb:>8.2f}")

# 1) Pareto frontier on (quality up, latency down, index cost down, storage down, update cost down)
def dominates(a, b):
    ka = (a[0], -a[1], -a[2], -a[3], -a[4]); kb = (b[0], -b[1], -b[2], -b[3], -b[4])
    return all(x >= y for x, y in zip(ka, kb)) and ka != kb
frontier = [n for n, v in OPTIONS.items() if not any(dominates(OPTIONS[m], v) for m in OPTIONS if m != n)]
print("\nnot dominated on all five axes:", frontier)

# 2) incremental value over the tuned baseline: quality gain per added cost
b = OPTIONS[BASE]
print(f"\nvs baseline '{BASE}':")
print(f"{'option':48s}{'dR@10':>7s}{'+ms':>7s}{'R@10 pts per +100ms':>21s}{'+index':>8s}{'+GB':>6s}")
for n, v in OPTIONS.items():
    if n == BASE: continue
    d_r, d_ms = v[0] - b[0], v[1] - b[1]
    per100 = f"{d_r * 100 / (d_ms / 100):.2f}" if d_ms > 0 else "n/a (faster)"
    print(f"{n:48s}{d_r:>+7.2f}{d_ms:>+7d}{per100:>21s}{v[2] - b[2]:>+8d}{v[3] - b[3]:>+6d}")

# 3) choose under constraints: maximise a quality score subject to the SLO and budgets
def feasible(v): return v[1] <= LAT_SLO and v[2] <= INDEX_BUDGET and v[4] <= MONTHLY_BUDGET and v[3] <= STORAGE_CAP
cands = {n: v for n, v in OPTIONS.items() if feasible(v)}
best = max(cands, key=lambda n: (0.7 * cands[n][0] + 0.3 * cands[n][5]))             # ASSUMED weighting: 70% quality, 30% robustness
print(f"\nconstraints: latency<={LAT_SLO}ms, index<={INDEX_BUDGET}, update/mo<={MONTHLY_BUDGET}, storage<={STORAGE_CAP}GB")
print("feasible:", list(cands)); print("choice (0.7*recall + 0.3*robustness):", best)
assert "hybrid + LLM reranker (top 20)" not in cands and "LLM-embedding retriever" not in cands
assert best == "hybrid + cross-encoder rerank", best
# sensitivity: how big must the LLM-retriever's gain be to justify its cost? (break-even recall for the same score)
needed = (0.7 * b[0] + 0.3 * b[5] - 0.3 * OPTIONS["LLM-embedding retriever"][5]) / 0.7
print("LLM-embedding retriever would need R@10 >= %.3f to tie the baseline under this scoring (assumed numbers say %.2f)" % (needed, OPTIONS["LLM-embedding retriever"][0]))
