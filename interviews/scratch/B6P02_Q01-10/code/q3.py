# Q3 offline AUC 0.91 but flat online conversion (illustrative numbers)
import numpy as np
from scipy.stats import rankdata, norm
rng = np.random.default_rng(3)

def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

# (1) Leakage: a feature that is only known after the click lifts offline AUC but is missing online
n = 200_000
true_signal = rng.normal(size=n)
y = (rng.random(n) < 1 / (1 + np.exp(-(true_signal * 1.1 - 3)))).astype(int)
leak = y * 2.5 + rng.normal(size=n)                 # e.g. 'dwell time after click'
honest = true_signal + rng.normal(scale=1.0, size=n)
auc_honest = auc(y, honest)
auc_leaky = auc(y, honest + leak)
print(f"AUC without leak {auc_honest:.3f}; with post-click feature {auc_leaky:.3f}")
assert auc_leaky - auc_honest > 0.10
assert 0.90 < auc_leaky < 0.97

# (2) Power: could this A/B test even see a lift?
base = 0.04                                       # 4% conversion
n_arm = 50_000
rel = 0.02                                       # a 2% relative lift
d = base * rel
se = (2 * base * (1 - base) / n_arm) ** 0.5
power = 1 - norm.cdf(1.96 - d / se)
print(f"power to detect +2% relative with {n_arm} users/arm: {power:.2f}")
assert power < 0.15
# users per arm for 80% power
need = 2 * (1.96 + 0.8416) ** 2 * base * (1 - base) / d ** 2
print(f"users per arm for 80% power at +2% relative: {int(np.ceil(need)):,}")
assert 900_000 < need < 1_000_000
# smallest relative lift that 50,000/arm can detect at 80% power
mde = (1.96 + 0.8416) * se / base
print(f"minimum detectable relative lift at 50,000/arm: {mde:.1%}")
assert 0.08 < mde < 0.09

# (3) SRM check: does the split look like 50/50?
a, b = 50_000, 50_900
chi = (a - (a + b) / 2) ** 2 / ((a + b) / 2) + (b - (a + b) / 2) ** 2 / ((a + b) / 2)
print(f"SRM chi-square for {a} vs {b}: {chi:.2f} (3.84 is the 5% cut-off for 1 df)")
assert 8 < chi < 10
