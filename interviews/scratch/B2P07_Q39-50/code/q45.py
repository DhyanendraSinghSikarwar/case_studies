# Standalone, numpy only. SYNTHETIC scores drawn from assumed distributions; shows the analysis method, not real rerankers.
import numpy as np
rng = np.random.default_rng(7)
SLICES = {            # slice: (n queries, first-stage gold shift, reranker gold shift, P(gold evidence truncated away))  -- all ASSUMED
    "general":      (500, 1.6, 3.2, 0.00),
    "domain_jargon": (300, 1.6, 0.9, 0.00),     # reranker trained on general data misjudges the domain
    "long_docs":    (200, 1.6, 3.2, 0.60)}      # max length cuts the evidence out of the text the reranker sees
C = 20                                          # candidates per query, 1 gold at index 0

def simulate():
    rows = []
    for name, (n, mu_fs, mu_rr, p_trunc) in SLICES.items():
        for _ in range(n):
            fs = rng.normal(0, 1, C); fs[0] += mu_fs
            rr = rng.normal(0, 1, C); rr[0] += 0 if rng.random() < p_trunc else mu_rr
            rr = rr * rng.lognormal(0, 0.5) + rng.normal(0, 2)          # per-query scale and offset: scores are NOT comparable across queries
            rows.append((name, fs, rr))
    return rows
Q = simulate()
z = lambda x: (x - x.mean()) / x.std()
top1_gold = lambda s: int(np.argmax(s)) == 0

def policy(kind, fs, rr):
    if kind == "baseline": return top1_gold(fs)
    if kind == "rerank": return top1_gold(rr)
    if kind == "blend": return top1_gold(0.5 * z(fs) + 0.5 * z(rr))
    if kind == "gated":                                         # rerank only when first stage is unsure (small gap between its top two scores)
        s = np.sort(fs)[::-1]; return top1_gold(rr) if (s[0] - s[1]) < 0.8 else top1_gold(fs)
    if kind == "blend_gated":
        s = np.sort(fs)[::-1]; return top1_gold(0.5 * z(fs) + 0.5 * z(rr)) if (s[0] - s[1]) < 0.8 else top1_gold(fs)
KINDS = ["baseline", "rerank", "blend", "gated", "blend_gated"]

print("PAIRED win/loss/tie of rerank vs baseline on top-1 correctness (win = baseline wrong, rerank right; loss = baseline right, rerank wrong)")
print(f"{'slice':15s}{'n':>5s}{'win':>6s}{'loss':>6s}{'tie':>6s}{'net':>6s}{'base acc':>10s}{'rerank acc':>12s}")
for name in list(SLICES) + ["ALL"]:
    sel = [(fs, rr) for nm, fs, rr in Q if name == "ALL" or nm == name]
    b = np.array([policy("baseline", *x) for x in sel]); r = np.array([policy("rerank", *x) for x in sel])
    w, l = int((~b & r).sum()), int((b & ~r).sum()); t = len(sel) - w - l
    print(f"{name:15s}{len(sel):>5d}{w:>6d}{l:>6d}{t:>6d}{w - l:>6d}{b.mean():>10.2f}{r.mean():>12.2f}")

print("\nTop-1 accuracy by policy and slice (synthetic):")
print(f"{'policy':13s}" + "".join(f"{n:>15s}" for n in list(SLICES) + ["ALL"]))
acc = {}
for k in KINDS:
    out = []
    for name in list(SLICES) + ["ALL"]:
        v = [policy(k, fs, rr) for nm, fs, rr in Q if name == "ALL" or nm == name]; out.append(np.mean(v))
    acc[k] = out; print(f"{k:13s}" + "".join(f"{x:>15.3f}" for x in out))

# Fixed threshold on the RAW reranker score: the same cut-off accepts very different shares of queries
cut = 3.0
print("\nshare of queries whose top reranker raw score exceeds a fixed cut-off of", cut, "(a score is not comparable across queries):")
for name in SLICES:
    sc = np.array([rr.max() for nm, fs, rr in Q if nm == name]); print(f"  {name:15s} {np.mean(sc > cut):.2f}   (raw top-score mean {sc.mean():.2f}, std {sc.std():.2f})")

# Checks used as tests
assert acc["rerank"][1] < acc["baseline"][1] and acc["rerank"][2] < acc["baseline"][2]       # reranking hurts on the two stressed slices
assert acc["rerank"][0] > acc["baseline"][0]                                                  # and helps on general
assert acc["blend_gated"][3] >= acc["rerank"][3] - 0.02
