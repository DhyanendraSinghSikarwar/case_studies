# Standalone, numpy only. SYNTHETIC clustered vectors and a random metadata flag; recall is vs exact filtered search.
import numpy as np
rng = np.random.default_rng(0)
N, D, NLIST, K = 20000, 32, 64, 10
centers = rng.normal(size=(NLIST, D)) * 2
X = centers[rng.integers(0, NLIST, N)] + rng.normal(size=(N, D))
X /= np.linalg.norm(X, axis=1, keepdims=True)
# tiny k-means for an IVF index
C = X[rng.choice(N, NLIST, replace=False)].copy()
for _ in range(8):
    a = np.argmax(X @ C.T, 1)
    for j in range(NLIST):
        m = X[a == j]
        if len(m): C[j] = m.mean(0)
    C /= np.linalg.norm(C, axis=1, keepdims=True)
assign = np.argmax(X @ C.T, 1); cells = [np.where(assign == j)[0] for j in range(NLIST)]
Q = X[rng.choice(N, 200, replace=False)] + 0.1 * rng.normal(size=(200, D)); Q /= np.linalg.norm(Q, axis=1, keepdims=True)

def top(ids, q, k): s = X[ids] @ q; return ids[np.argsort(-s)[:k]]
def ivf_candidates(q, nprobe): return np.concatenate([cells[j] for j in np.argsort(-(C @ q))[:nprobe]])

def run(sel, nprobe=4):
    flag = rng.random(N) < sel                                    # metadata predicate passes for fraction `sel`
    res = {m: [] for m in ["post-filter ANN, k=10", "post-filter, over-fetch k/sel (cap 200)", "pre-filter inside IVF cells", "pre-filter, nprobe x4"]}
    rec = {m: [] for m in res}
    for q in Q:
        truth = set(top(np.where(flag)[0], q, K))                 # exact search on the filtered subset
        cand = ivf_candidates(q, nprobe)
        outs = {"post-filter ANN, k=10": [i for i in top(cand, q, K) if flag[i]],
                "post-filter, over-fetch k/sel (cap 200)": [i for i in top(cand, q, min(200, int(K / sel))) if flag[i]][:K],
                "pre-filter inside IVF cells": list(top(cand[flag[cand]], q, K)),
                "pre-filter, nprobe x4": list(top((c4 := ivf_candidates(q, nprobe * 4))[flag[c4]], q, K))}
        for m, o in outs.items(): res[m].append(len(o)); rec[m].append(len(set(o) & truth) / K)
    print(f"selectivity {sel:.0%} (about {int(N*sel)} eligible vectors), nprobe={nprobe} of {NLIST}")
    for m in res: print(f"  {m:42s} results/query={np.mean(res[m]):5.2f}  recall@10 vs exact-filtered={np.mean(rec[m]):.2f}")
run(0.20); run(0.01)
