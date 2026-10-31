# Q27 rural subgroup gap in a credit model (illustrative simulation)
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(27)

def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def make(n, rate, d):
    y = (rng.random(n) < rate).astype(int)
    s = rng.normal(size=n) + d * y            # score = signal + noise; AUC = Phi(d/sqrt2)
    return y, s
# 97,000 urban rows (default rate 5%), 3,000 rural rows (default rate 6%, weaker signal)
yu, su = make(97_000, 0.05, 1.45)
yr, sr = make(3_000, 0.06, 0.62)
y = np.concatenate([yu, yr]); s = np.concatenate([su, sr]); rural = np.r_[np.zeros(97_000, bool), np.ones(3_000, bool)]
a_all, a_u, a_r = auc(y, s), auc(yu, su), auc(yr, sr)
print(f"AUC overall {a_all:.3f}, urban {a_u:.3f}, rural {a_r:.3f}; rural defaults {yr.sum()}")
assert 0.80 < a_all < 0.86 and 0.68 < a_r < 0.75 and a_u - a_r > 0.1

# Bootstrap CI for the rural AUC, and for the gap
B = 400; gaps = []; rurals = []
for _ in range(B):
    i = rng.integers(0, 3_000, 3_000); j = rng.integers(0, 97_000, 97_000)
    ar = auc(yr[i], sr[i]); rurals.append(ar); gaps.append(auc(yu[j], su[j]) - ar)
print(f"rural AUC 95% CI {np.percentile(rurals,2.5):.3f} to {np.percentile(rurals,97.5):.3f}; gap CI {np.percentile(gaps,2.5):.3f} to {np.percentile(gaps,97.5):.3f}")
assert np.percentile(gaps, 2.5) > 0.05                      # the gap is real, not noise

# Re-weight to the launch mix (8% rural) by resampling rows
n_launch = 100_000
iu = rng.integers(0, 97_000, int(n_launch * 0.92)); ir = rng.integers(0, 3_000, int(n_launch * 0.08))
yl = np.concatenate([yu[iu], yr[ir]]); sl = np.concatenate([su[iu], sr[ir]])
print(f"overall AUC at training mix (3% rural) {a_all:.3f}; at launch mix (8% rural) {auc(yl, sl):.3f}")
assert auc(yl, sl) < a_all

# What a rural-only AUC of 0.71 on this many defaults means: Hanley-McNeil standard error
def hm_se(A, n1, n0):
    Q1 = A / (2 - A); Q2 = 2 * A * A / (1 + A)
    return np.sqrt((A*(1-A) + (n1-1)*(Q1-A*A) + (n0-1)*(Q2-A*A)) / (n1 * n0))
print(f"Hanley-McNeil SE for rural AUC with {yr.sum()} defaults: {hm_se(a_r, yr.sum(), len(yr)-yr.sum()):.3f}")
print(f"defaults needed in rural for SE about 0.01: {int(next(n for n in range(100,5000,25) if hm_se(0.71, n, 16*n) < 0.01))}")
assert 0.015 < hm_se(a_r, yr.sum(), len(yr) - yr.sum()) < 0.03
assert next(n for n in range(100, 5000, 25) if hm_se(0.71, n, 16 * n) < 0.01) == 900 and 900 / 0.06 == 15_000
