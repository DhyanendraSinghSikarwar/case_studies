# Standalone, numpy only. SYNTHETIC vectors; recall is ANN vs exact search (index quality, not end-to-end relevance). Timings are machine-specific.
import time, numpy as np
rng = np.random.default_rng(1)
N, D, NLIST, K, NQ = 50000, 32, 128, 10, 200
centers = rng.normal(size=(NLIST, D))
X = (centers[rng.integers(0, NLIST, N)] + 1.2 * rng.normal(size=(N, D))).astype(np.float32)   # overlapping clusters: not trivial
X /= np.linalg.norm(X, axis=1, keepdims=True)
C = X[rng.choice(N, NLIST, replace=False)].copy()
for _ in range(6):
    a = np.argmax(X @ C.T, 1)
    for j in range(NLIST):
        m = X[a == j]
        if len(m): C[j] = m.mean(0)
    C /= np.linalg.norm(C, axis=1, keepdims=True)
a = np.argmax(X @ C.T, 1); cells = [np.where(a == j)[0] for j in range(NLIST)]
Q = X[rng.choice(N, NQ, replace=False)] + 0.5 * rng.normal(size=(NQ, D)).astype(np.float32) / np.sqrt(D); Q = Q.astype(np.float32); Q /= np.linalg.norm(Q, axis=1, keepdims=True)
truth = [set(np.argsort(-(X @ q))[:K]) for q in Q]

def ivf(q, nprobe):
    cand = np.concatenate([cells[j] for j in np.argsort(-(C @ q))[:nprobe]])
    return cand[np.argsort(-(X[cand] @ q))[:K]]
print("IVF nprobe sweep (recall@10 vs exact):")
for nprobe in (1, 2, 4, 8, 16, 32, 64, 128):
    t = time.perf_counter(); res = [ivf(q, nprobe) for q in Q]; ms = (time.perf_counter() - t) / NQ * 1000
    rec = np.mean([len(set(r) & t_) / K for r, t_ in zip(res, truth)])
    print(f"  nprobe={nprobe:3d}  recall@10={rec:.3f}  {ms:6.2f} ms/query (this machine)")
