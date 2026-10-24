import numpy as np
rng = np.random.default_rng(0)
# SYNTHETIC: a reward model that gives +0.004 per token of length on top of true quality (a built-in length bias).
n = 4000
quality = rng.normal(0, 1, n)
length = np.clip(rng.normal(200, 80, n) + 20 * quality, 30, None)
reward = quality + 0.012 * (length - 200) + rng.normal(0, 0.3, n)
print("corr(length, reward):", round(np.corrcoef(length, reward)[0, 1], 3), " corr(length, true quality):", round(np.corrcoef(length, quality)[0, 1], 3))
# A/B comparison: model B writes longer answers but is slightly WORSE in true quality
qa = rng.normal(0.00, 1, n); la = rng.normal(200, 50, n)
qb = rng.normal(-0.15, 1, n); lb = rng.normal(320, 50, n)
ra = qa + 0.012 * (la - 200); rb = qb + 0.012 * (lb - 200)
print("raw win rate of B (judge with length bias):", round((rb > ra).mean(), 3))
print("true-quality win rate of B:                 ", round((qb > qa).mean(), 3))
# length-controlled: regress reward on length, compare residual (length-adjusted) scores
X = np.concatenate([la, lb]); Y = np.concatenate([ra, rb])
slope = np.polyfit(X, Y, 1)[0]
ra_adj = ra - slope * la; rb_adj = rb - slope * lb
print("length-adjusted win rate of B:              ", round((rb_adj > ra_adj).mean(), 3), "(slope", round(slope, 4), ")")
