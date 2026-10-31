# Illustrative. Relative vs absolute CTR cost and the sample size needed to see it.
from statistics import NormalDist
N = NormalDist()
p0, rel = 0.040, 0.008
p1 = p0 * (1 - rel)
print(f"CTR {p0:.4%} -> {p1:.4%}; absolute drop {100*(p0-p1):.3f} points")
assert round(p1, 5) == 0.03968 and round(100 * (p0 - p1), 3) == 0.032
def n_per_arm(p, delta, alpha=0.05, power=0.80):
    z = N.inv_cdf(1 - alpha / 2) + N.inv_cdf(power)
    return 2 * p * (1 - p) * z * z / delta ** 2
n = n_per_arm(p0, p0 - p1)
print(f"impressions per arm to detect a 0.8% relative CTR change: {n:,.0f}")
assert 5.5e6 < n < 6.3e6
# at 20 impressions per user per week, one arm of 100,000 users per week
users_week = 100_000 * 20
print(f"weeks of 100k users/arm at 20 impressions/user/week: {n/users_week:.1f}")
assert 2.5 < n / users_week < 3.5
# Small-creator share (illustrative 12% -> 15% of impressions): what does a creator-side gain look like?
share0, share1 = 0.12, 0.15
print(f"small-creator impression share {share0:.0%} -> {share1:.0%}, +{(share1/share0-1):.0%} relative")
assert round(share1 / share0 - 1, 2) == 0.25
# Clicks cost per 1,000,000 impressions
print("clicks lost per 1M impressions:", round(1e6 * (p0 - p1)))
assert round(1e6 * (p0 - p1)) == 320
