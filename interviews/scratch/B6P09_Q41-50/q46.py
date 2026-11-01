# Q46: where does a 0.05 AUC lift apply when features exist for 70%? Synthetic (binormal scores, invented).
import numpy as np
from scipy.stats import norm, rankdata
rng = np.random.default_rng(3)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
sep = lambda a: np.sqrt(2) * norm.ppf(a)        # binormal separation for a target AUC, unit variances
d0, d1 = sep(0.66), sep(0.71)
n, bad_rate, cover = 400_000, 0.10, 0.70
y = (rng.random(n) < bad_rate).astype(int)
has = rng.random(n) < cover
base = d0 * y + rng.normal(size=n)
new = np.where(has, d1 * y + rng.normal(size=n), base)       # uncovered applicants keep the old score
print("AUC base overall      :", round(auc(y, base), 3))
print("AUC new, covered only :", round(auc(y[has], new[has]), 3), " (base on same group:", round(auc(y[has], base[has]), 3), ")")
print("AUC new, overall      :", round(auc(y, new), 3))
lift_overall = auc(y, new) - auc(y, base)
print("overall lift:", round(lift_overall, 3), "vs 0.05 on the covered group")
assert abs(auc(y[has], new[has]) - 0.71) < 0.01 and abs(auc(y, base) - 0.66) < 0.01
assert 0.015 < lift_overall < 0.045      # diluted: well under 0.05

# stability: population stability index of one feature between build month and a later month (invented shift)
def psi(a, b, bins=10):
    edges = np.quantile(a, np.linspace(0, 1, bins + 1)); edges[0], edges[-1] = -np.inf, np.inf
    pa = np.histogram(a, edges)[0] / len(a); pb = np.histogram(b, edges)[0] / len(b)
    pa, pb = np.clip(pa, 1e-6, None), np.clip(pb, 1e-6, None)
    return float(((pb - pa) * np.log(pb / pa)).sum())
f0 = rng.normal(0, 1, 50_000); f_same = rng.normal(0, 1, 50_000); f_shift = rng.normal(0.4, 1.2, 50_000)
print("PSI same:", round(psi(f0, f_same), 4), " PSI shifted:", round(psi(f0, f_shift), 3))
assert psi(f0, f_same) < 0.01 and psi(f0, f_shift) > 0.1
