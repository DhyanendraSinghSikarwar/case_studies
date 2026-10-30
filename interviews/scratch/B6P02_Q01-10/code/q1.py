# Q1 fraud AUC 0.86 -> 0.79: is the drop noise, a mix shift, or real decay? (illustrative numbers)
import numpy as np
from scipy.stats import rankdata, norm

def auc(y, s):
    r = rankdata(s)
    n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def hanley_se(a, n1, n0):
    q1 = a / (2 - a); q2 = 2 * a * a / (1 + a)
    v = (a * (1 - a) + (n1 - 1) * (q1 - a * a) + (n0 - 1) * (q2 - a * a)) / (n1 * n0)
    return v ** 0.5

# Step 1: is a 0.07 drop on 30,000 rows just noise? Assume 2% fraud -> 600 positives.
n, pos = 30_000, 600
se = hanley_se(0.79, pos, n - pos)
print(f"SE of AUC 0.79 with {pos} positives: {se:.4f}; 95% CI [{0.79-1.96*se:.3f}, {0.79+1.96*se:.3f}]")
assert 0.010 < se < 0.014
assert 0.79 + 1.96 * se < 0.86          # 0.86 is far outside the interval

# Step 2: a pure mix shift. Two segments with FIXED within-segment quality.
rng = np.random.default_rng(7)
def seg(n_rows, rate, d):                # binormal: positives shifted by d; AUC = Phi(d/sqrt2)
    y = (rng.random(n_rows) < rate).astype(int)
    s = rng.normal(size=n_rows) + d * y
    return y, s
d_dom, d_xb = norm.ppf(0.92) * 2**0.5, norm.ppf(0.68) * 2**0.5     # segment AUCs 0.92 and 0.68
def pooled(share_xb, total=400_000):
    nx = int(total * share_xb); nd = total - nx
    y1, s1 = seg(nd, 0.01, d_dom); y2, s2 = seg(nx, 0.04, d_xb)
    return (auc(y1, s1), auc(y2, s2),
            auc(np.r_[y1, y2], np.r_[s1, s2]))
res = {}
for label, share in [("launch mix (10% cross-border)", 0.10), ("now (30% cross-border)", 0.30)]:
    res[share] = pooled(share)
    a1, a2, ap = res[share]
    print(f"{label:30s} domestic {a1:.3f}  cross-border {a2:.3f}  pooled {ap:.3f}")
drop = res[0.10][2] - res[0.30][2]
print(f"pooled AUC drop from mix alone: {drop:.3f}")
assert 0.05 < drop < 0.10               # same size as the reported 0.07 drop, with no model change
# Segment AUCs did not move, only the mix did, so the model is not the first suspect
assert abs(res[0.10][0] - res[0.30][0]) < 0.01 and abs(res[0.10][1] - res[0.30][1]) < 0.02
