import numpy as np
rng = np.random.default_rng(23)
D, N, Q, NEW_FRAC, K = 32, 2000, 400, 0.15, 5

def unit(m): return m / np.linalg.norm(m, axis=1, keepdims=True)
latent = unit(rng.normal(size=(N, D)))
def rot():
    q, _ = np.linalg.qr(rng.normal(size=(D, D))); return q
RA, RB = rot(), rot()
common = unit(rng.normal(size=(1, D)))[0]             # model B shares a big common direction (higher cosines)
def embA(x): return unit(x @ RA + 0.05 * rng.normal(size=x.shape))
def embB(x): return unit(unit(x @ RB + 0.05 * rng.normal(size=x.shape)) + 1.5 * common)

is_new = rng.random(N) < NEW_FRAC
docA = embA(latent); docB = embB(latent)
target = rng.integers(0, N, Q)
qlat = unit(latent[target] + 0.12 * rng.normal(size=(Q, D)))
qA, qB = embA(qlat), embB(qlat)
docs_mixed = np.where(is_new[:, None], docB, docA)      # index: old docs in A, new docs in B
docs_allA = docA

def hit(scores):
    top = np.argsort(-scores, axis=1)[:, :K]
    return (top == target[:, None]).any(axis=1)

h_clean = hit(qA @ docs_allA.T)                                    # all docs and queries in model A
h_Aq = hit(qA @ docs_mixed.T)                                      # mixed index, query embedded by A
h_Bq = hit(qB @ docs_mixed.T)                                      # mixed index, query embedded by B
# dual query: score old docs with qA, new docs with qB, merge on raw cosine
s_dual = np.where(is_new[None, :], qB @ docB.T, qA @ docA.T)
h_dual = hit(s_dual)
# fix: re-embed everything with B and query with B
h_fix = hit(qB @ docB.T)
print(f"new-model share of index: {is_new.mean():.0%}")
for name, h in [("all old, A query (baseline)", h_clean), ("mixed, A query", h_Aq), ("mixed, B query", h_Bq),
                ("mixed, dual query merged by raw score", h_dual), ("all re-embedded with B", h_fix)]:
    print(f"{name:40s} hit@{K} = {h.mean():.2f}  | target old docs {h[~is_new[target]].mean():.2f}  target new docs {h[is_new[target]].mean():.2f}")
assert h_clean.mean() > 0.7
assert h_Aq.mean() < h_clean.mean() - 0.05
assert h_Bq.mean() < h_clean.mean() - 0.3
assert h_dual.mean() < h_clean.mean() - 0.03
assert abs(h_fix.mean() - h_clean.mean()) < 0.08
# the cosine between a doc and its own query is on a different scale in each space
print("mean top-1 cosine A:", round(float((qA @ docA.T).max(1).mean()), 2), " B:", round(float((qB @ docB.T).max(1).mean()), 2))
print("asserts passed")
