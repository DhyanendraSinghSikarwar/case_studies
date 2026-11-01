import numpy as np

def probs_from_logits(logits, temperature=1.0, top_k=0, top_p=1.0):
    z = np.asarray(logits, dtype=np.float64) / temperature      # 1) temperature (new array, no mutation)
    p = np.exp(z - z.max()); p /= p.sum()                       # 2) stable softmax
    order = np.argsort(-p, kind="stable")                       # sort desc; stable => ties by lower index
    keep = np.zeros(len(p), dtype=bool)
    k = len(p) if top_k <= 0 else min(top_k, len(p))
    keep[order[:k]] = True                                      # 3) top-k
    csum = np.cumsum(p[order])
    # top-p: smallest prefix whose mass >= top_p (token that crosses the line is kept)
    n_p = int(np.searchsorted(csum, top_p - 1e-12) + 1)
    mask_p = np.zeros(len(p), dtype=bool); mask_p[order[:max(n_p, 1)]] = True
    keep &= mask_p                                              # at least the top token survives both
    q = np.where(keep, p, 0.0)
    return q / q.sum()                                          # 4) renormalise

def sample(logits, rng, **kw):
    return rng.choice(len(logits), p=probs_from_logits(logits, **kw))

logits = np.array([2.0, 1.0, 1.0, 0.5, 0.0, -1.0])
for kw in [dict(), dict(temperature=0.5), dict(top_k=3), dict(top_p=0.8), dict(temperature=0.7, top_k=4, top_p=0.9), dict(top_p=0.0), dict(top_k=1)]:
    print(kw, np.round(probs_from_logits(logits, **kw), 4))

rng = np.random.default_rng(0)
N = 100_000
for kw in [dict(temperature=0.7, top_k=4, top_p=0.9), dict(top_p=0.8)]:
    expected = probs_from_logits(logits, **kw)
    draws = rng.choice(len(logits), size=N, p=expected)   # same call sample() makes, vectorised
    emp = np.bincount(draws, minlength=len(logits)) / N
    print(kw, "max abs err", round(np.abs(emp-expected).max(), 4), "never-sampled-masked:", (emp[expected==0]==0).all())
# also check the real single-draw function
cnt = np.zeros(6)
for _ in range(20000): cnt[sample(logits, rng, temperature=0.7, top_k=4, top_p=0.9)] += 1
print(np.round(cnt/20000,3))
