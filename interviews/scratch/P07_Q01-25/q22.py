import numpy as np
rng = np.random.default_rng(0)
centers = rng.normal(size=(5, 8))
cl = rng.integers(0, 5, 50)                       # 5 "genres"
E = centers[cl] + .3 * rng.normal(size=(50, 8)); E /= np.linalg.norm(E, axis=1, keepdims=True)
rel = rng.random(50) + 0.4 * (cl == 0)            # genre 0 is most relevant, so top-k piles into it
def mmr(rel, E, k, lam=0.5):
    chosen, cand = [], list(range(len(rel)))
    S = E @ E.T
    while len(chosen) < k:
        best = max(cand, key=lambda i: lam*rel[i] - (1-lam)*(max(S[i, chosen]) if chosen else 0))
        chosen.append(best); cand.remove(best)
    return chosen
def ild(ids): S = E[ids] @ E[ids].T; k=len(ids); return 1 - (S.sum()-k)/(k*(k-1))
top = list(np.argsort(-rel)[:10])
print("top-10 by relevance: mean rel %.2f, ILD %.2f" % (rel[top].mean(), ild(top)))
m = mmr(rel, E, 10)
print("MMR lam=0.5        : mean rel %.2f, ILD %.2f" % (rel[m].mean(), ild(m)))
