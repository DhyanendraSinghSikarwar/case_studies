# Q20: 12 automated accounts create half of a +6% lift (illustrative simulation built to match the prompt)
import numpy as np
from scipy.stats import ttest_ind, binom

rng = np.random.default_rng(20)
n = 100_000
# normal users: heavy-tailed revenue, rescaled so control total is exactly 1,000,000
ctrl = rng.lognormal(0, 1.2, n); ctrl *= 1_000_000 / ctrl.sum()
base = rng.lognormal(0, 1.2, n)
treat_real = base * (1_030_000 / base.sum())         # genuine users: +3% in total
bots = np.full(12, 2_500.0)                          # 12 accounts, 30,000 in total
treat = np.concatenate([treat_real, bots])           # 100,012 accounts in the treatment arm
is_bot = np.r_[np.zeros(n, bool), np.ones(12, bool)]

print(f"control total {ctrl.sum():,.0f}; treatment total {treat.sum():,.0f}; bots {bots.sum():,.0f}")
print(f"lift with bots    : {treat.sum() / ctrl.sum() - 1:+.1%}")
print(f"lift without bots : {treat[~is_bot].sum() / ctrl.sum() - 1:+.1%}")
assert round(treat.sum()) == 1_060_000 and abs(treat.sum() / ctrl.sum() - 1.06) < 1e-9
assert abs(treat[~is_bot].sum() / ctrl.sum() - 1.03) < 1e-9

def report(label, t, c):
    r = ttest_ind(t, c, equal_var=False)
    print(f"{label:28} lift {t.mean() / c.mean() - 1:+.2%}  Welch p = {r.pvalue:.4f}")
    return r.pvalue
p_all = report("all accounts", treat, ctrl)
p_clean = report("bots removed", treat[~is_bot], ctrl)

# Winsorize at the 99.9th percentile of the pooled data (no bot labels needed)
cap = np.quantile(np.r_[ctrl, treat], 0.999)
report("winsorized at p99.9", np.minimum(treat, cap), np.minimum(ctrl, cap))
print(f"cap = {cap:.1f} vs a bot's revenue 2,500 and a normal mean of 10")

# a behaviour rule: page views per day (bots: thousands; normal users: a few dozen at most)
views_normal = rng.poisson(8, 2 * n)
views_bots = rng.integers(2_000, 5_000, 12)
rule = 1_000
print(f"rule 'page views/day > {rule}': flags {np.sum(views_bots > rule)} of 12 bots and {np.sum(views_normal > rule)} of {2*n:,} normal accounts")
assert np.sum(views_bots > rule) == 12 and np.sum(views_normal > rule) == 0

# if 12 bots had landed at random in the arms, how likely are all 12 in treatment?
print(f"P(all 12 bots land in treatment by chance) = {binom.pmf(12, 12, 0.5):.5f}")
assert abs(binom.pmf(12, 12, 0.5) - 0.5**12) < 1e-12
print("all asserts passed")
