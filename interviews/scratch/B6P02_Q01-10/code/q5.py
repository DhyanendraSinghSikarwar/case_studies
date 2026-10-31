# Q5 null-rate jump in merchant_category: confirm the cause (illustrative numbers)
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(5)

def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

n = 300_000
mcc_risk = rng.normal(size=n)                    # merchant-category risk (known to the model)
other = rng.normal(size=n)                       # everything else the model uses
logit = -3.2 + 1.5 * mcc_risk + 1.0 * other
y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
def score(m, o): return 1.5 * m + 1.0 * o        # the model's score (null filled by 0 = 'average')

def with_nulls(rate):
    is_null = rng.random(n) < rate
    m = np.where(is_null, 0.0, mcc_risk)         # default fill after the deploy
    return is_null, score(m, other)

res = {}
for rate in (0.005, 0.18):
    is_null, s = with_nulls(rate)
    res[rate] = (is_null, s, auc(y, s))
    print(f"null rate {rate:.1%}: AUC {res[rate][2]:.3f}")
is_null, s18, a18 = res[0.18]
a_null = auc(y[is_null], s18[is_null]); a_ok = auc(y[~is_null], s18[~is_null])
print(f"at 18% nulls: AUC on null rows {a_null:.3f}, on non-null rows {a_ok:.3f}")
assert 0.84 < res[0.005][2] < 0.89 and a18 < res[0.005][2] - 0.02
assert a_null < a_ok - 0.04                      # the damage sits in the null rows
# Confirm: replay the 18% nulls with the true value restored -> AUC recovers
s_fixed = score(mcc_risk, other)
print(f"replay with feature restored: AUC {auc(y, s_fixed):.3f}")
assert abs(auc(y, s_fixed) - res[0.005][2]) < 0.01
# Why a threshold alert catches it on day one: 3-sigma upper bound for an hourly batch
base, nh = 0.005, 10_000
ub = base + 3 * (base * (1 - base) / nh) ** 0.5
print(f"3-sigma null-rate bound for {nh:,} rows/hour: {ub:.2%}; 18% is {0.18/ub:.0f}x that")
assert 0.0069 < ub < 0.0072
