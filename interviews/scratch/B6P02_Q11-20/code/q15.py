# Q15: how much can offline, shadow, canary and A/B each show about a "1.2% better" model? (illustrative, seeded)
import numpy as np
from scipy.stats import rankdata, norm
rng = np.random.default_rng(15)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

# (1) Offline: is a 1.2% relative AUC gain (0.800 -> about 0.81) distinguishable from noise on a 30,000-row test set?
n = 30_000
z = rng.normal(size=n)
y = (rng.random(n) < 1 / (1 + np.exp(-(-1.5 + 2.4 * z)))).astype(int)
old = z + rng.normal(0, 0.75, n)                    # old model's score
new = old + 0.10 * (z - old) + rng.normal(0, 0.12, n)   # correlated, slightly better
a_old, a_new = auc(y, old), auc(y, new)
print(f"offline AUC old {a_old:.4f}, new {a_new:.4f}, relative gain {100*(a_new/a_old-1):.2f}%")
diffs = []
for _ in range(300):
    i = rng.integers(0, n, n)
    diffs.append(auc(y[i], new[i]) - auc(y[i], old[i]))
lo, hi = np.percentile(diffs, [2.5, 97.5])
print(f"paired bootstrap 95% CI for AUC difference: [{lo:.4f}, {hi:.4f}]")
assert lo > 0 and a_new > a_old

# (2) Online A/B: sample size to see a 1.2% RELATIVE lift in a 4.0% conversion rate
p0, rel = 0.04, 0.012
p1 = p0 * (1 + rel); d = p1 - p0
za, zb = norm.ppf(0.975), norm.ppf(0.80)
n_arm = 2 * (za + zb) ** 2 * (p0 * (1 - p0) + p1 * (1 - p1)) / 2 / d ** 2
print(f"A/B: lift {100*d:.3f} points; users needed per arm = {n_arm:,.0f}")
assert 2.5e6 < n_arm < 2.8e6
for per_day in (100_000, 500_000):
    print(f"  at {per_day:,} users/day split 50/50: {np.ceil(n_arm / (per_day / 2)):.0f} days")
assert np.ceil(n_arm / 50_000) > 50

# (3) Canary: 5% of traffic for a day cannot see 1.2% but should catch a breakage. Detect a 10% relative drop in approval?
base = 0.60                       # approval rate of the old model (illustrative)
n_can = 20_000                    # canary decisions in the first hours
se = np.sqrt(base * (1 - base) / n_can)
mde = (za + zb) * se * np.sqrt(2)
print(f"canary of {n_can:,} decisions: smallest approval-rate change detectable ~ {100*mde:.2f} points (80% power)")
broken = 0.60 * 0.90
power = 1 - norm.cdf((za * np.sqrt(2) * se - (base - broken)) / (np.sqrt(2) * se))
print(f"chance to flag a 10% relative approval drop: {power:.3f}")
assert power > 0.99 and mde > 0.01      # catches breakage, cannot see 1.2% relative of 4% conversion

# (4) Shadow: both models score the same requests; compare decisions. No effect on users, no outcome for the new model's own choices.
thr_old = np.quantile(old, 0.9); thr_new = np.quantile(new, 0.9)
flip = ((old >= thr_old) != (new >= thr_new)).mean()
print(f"shadow: top-10% decisions differ on {100*flip:.2f}% of requests")
# (5) Label delay: with 45-day label delay, outcome metrics for a canary started day 0 are first mature on day 45
print("label delay 45 days: use proxy guardrails (approval rate, score shift, latency) until day 45; outcome A/B read at day 45+window")
