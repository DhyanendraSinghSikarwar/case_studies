# Illustrative numbers only. Is the thumbs-down rise noise, what to do, and how fast could we have seen it.
import math
from statistics import NormalDist
Z = NormalDist()
x1, n1, x2, n2 = 248, 8000, 375, 7500
p1, p2 = x1 / n1, x2 / n2
assert round(p1, 3) == 0.031 and round(p2, 3) == 0.05 and round((p2 - p1) * 100, 1) == 1.9
rel = p2 / p1 - 1
print('relative rise', round(rel, 3))
assert round(rel, 2) == 0.61
pool = (x1 + x2) / (n1 + n2)
se0 = math.sqrt(pool * (1 - pool) * (1 / n1 + 1 / n2))
z = (p2 - p1) / se0
pval = 2 * (1 - Z.cdf(abs(z)))
print('z', round(z, 2), 'two-sided p', f'{pval:.1e}')
assert 5.5 < z < 6.5 and pval < 1e-8
se1 = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
lo, hi = (p2 - p1) - 1.96 * se1, (p2 - p1) + 1.96 * se1
print('95% CI for the rise (points)', round(lo * 100, 2), round(hi * 100, 2))
assert 1.2 < lo * 100 < 1.3 and 2.4 < hi * 100 < 2.6
# Sampling noise is not the issue. Bias is: only a small share is rated, and raters choose to rate.
# Pre-agreed rollback rule (illustrative): rise >= 1.0 pt absolute AND lower CI bound > 0 with >= 1,000 ratings in each period.
rule = (p2 - p1) >= 0.010 and lo > 0 and min(n1, n2) >= 1000
assert rule
# Speed: how many rated answers per arm to see 3.1% -> 5.0% at 80% power, 5% two-sided?
za, zb = Z.inv_cdf(0.975), Z.inv_cdf(0.80)
n_arm = math.ceil((za + zb) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p2 - p1) ** 2)
print('rated answers needed per arm', n_arm)
assert 1600 < n_arm < 1800
# Invented volume: 200,000 answers a week, 4% rated -> 8,000 rated a week (matches the prompt), 1,143 a day.
weekly_answers, rate_share = 200_000, 0.04
rated_week = weekly_answers * rate_share
assert rated_week == 8000
rated_day = rated_week / 7
for split in (0.10, 0.50):
    per_day_arm = rated_day * split
    print(f'canary {int(split*100)}%: rated/day in canary {per_day_arm:.0f}, days to {n_arm} ratings {n_arm/per_day_arm:.1f}')
assert round(1700 / (rated_day * 0.10)) > 10 and round(n_arm / (rated_day * 0.5)) <= 3
# Days of post-ship data against the prior week baseline before |z| > 2.58 (expected values, not a simulation).
def days_to_z(target):
    for d in range(1, 15):
        n = rated_day * d
        pl = (p1 * n1 + p2 * n) / (n1 + n)
        s = math.sqrt(pl * (1 - pl) * (1 / n1 + 1 / n))
        if (p2 - p1) / s > target: return d
d99 = days_to_z(2.58)
print('days of post-ship ratings before z>2.58 against last week:', d99)
assert d99 == 1
# Faster signals that do not need ratings: a 300-prompt golden set run BEFORE the release.
golden_n, old_pass, new_pass = 300, 0.90, 0.84
se_g = math.sqrt(old_pass * (1 - old_pass) / golden_n + new_pass * (1 - new_pass) / golden_n)
drop_pts = (old_pass - new_pass) * 100
print('golden-set drop', round(drop_pts, 1), 'pts, 1.96 se =', round(1.96 * se_g * 100, 1), 'pts')
assert round(drop_pts) == 6 and 1.96 * se_g * 100 < 6
