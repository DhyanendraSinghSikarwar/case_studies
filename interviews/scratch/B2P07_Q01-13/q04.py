# SYNTHETIC scores (not real retrievers): BM25-like scores on a ~0-30 scale, dense cosine-like on ~0-1.
# Shows (1) raw sums let the big-scale ranker dominate, (2) normalised fusion + an alpha sweep with CIs.
import numpy as np
rng = np.random.default_rng(0)
N_Q, N_D = 400, 30            # queries, candidates per query; candidate 0 is the relevant one

def make():
    bm = np.zeros((N_Q, N_D)); de = np.zeros((N_Q, N_D))
    for q in range(N_Q):
        lexical = rng.random() < 0.5          # half the queries favour BM25, half favour dense
        bm[q] = rng.gamma(2.0, 2.0, N_D)                      # scale ~ 0-25
        de[q] = np.clip(rng.normal(0.45, 0.08, N_D), 0, 1)    # scale ~ 0-1
        if lexical: bm[q, 0] += rng.normal(9, 3);  de[q, 0] += rng.normal(0.04, 0.05)
        else:       bm[q, 0] += rng.normal(1, 2);  de[q, 0] += rng.normal(0.22, 0.06)
    return bm, de
bm, de = make()

def hit_at(score, k):          # recall@k with exactly one relevant doc (index 0)
    top = np.argsort(-score, axis=1)[:, :k]
    return (top == 0).any(axis=1).astype(float)
def minmax(x): lo, hi = x.min(1, keepdims=True), x.max(1, keepdims=True); return (x - lo) / (hi - lo + 1e-12)
def zscore(x): return (x - x.mean(1, keepdims=True)) / (x.std(1, keepdims=True) + 1e-12)
K = 3
print(f"recall@{K}  BM25 only: {hit_at(bm, K).mean():.3f}   dense only: {hit_at(de, K).mean():.3f}")
print(f"raw sum bm+dense   : {hit_at(bm + de, K).mean():.3f}   (BM25 scale swamps dense; ~= BM25 only)")
for name, f in (("min-max", minmax), ("z-score", zscore)):
    print(f"{name:8} 0.5/0.5    : {hit_at(0.5 * f(de) + 0.5 * f(bm), K).mean():.3f}")

# tune alpha on a dev split, report on a held-out test split with bootstrap CI
dev, test = np.arange(N_Q) < 200, np.arange(N_Q) >= 200
alphas = np.round(np.linspace(0, 1, 11), 1)
fused = lambda a: a * zscore(de) + (1 - a) * zscore(bm)
dev_scores = {a: hit_at(fused(a), K)[dev].mean() for a in alphas}
best = max(dev_scores, key=dev_scores.get)
print("alpha sweep (dev recall@3):", {float(a): round(float(v), 3) for a, v in dev_scores.items()})
best = float(best); print("best alpha on dev:", best)
def boot_ci(x, n=2000):
    m = [rng.choice(x, len(x)).mean() for _ in range(n)]; return np.percentile(m, [2.5, 97.5])
for label, a in (("dense only", 1.0), ("bm25 only", 0.0), (f"alpha={best}", best)):
    x = hit_at(fused(a), K)[test]
    lo, hi = boot_ci(x)
    print(f"TEST {label:12} recall@{K} = {x.mean():.3f}  95% CI [{lo:.3f}, {hi:.3f}]  (n={len(x)})")
