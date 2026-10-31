# Illustrative: flat A/B after 3 weeks. 200,000 users per arm, baseline conversion 5.0%.
from statistics import NormalDist
N = NormalDist()
n, p = 200_000, 0.050
se = (2 * p * (1 - p) / n) ** 0.5
z = N.inv_cdf(0.975) + N.inv_cdf(0.80)
mde = z * se
print(f"se of difference {100*se:.3f} pts; MDE (80% power) {100*mde:.2f} pts = {mde/p:.1%} relative")
assert round(100 * se, 3) == 0.069 and round(100 * mde, 2) == 0.19
# Observed: +0.03 pts (illustrative). CI:
obs = 0.0003
lo, hi = obs - 1.96 * se, obs + 1.96 * se
print(f"observed +{100*obs:.2f} pts, 95% CI [{100*lo:.2f}, {100*hi:.2f}] pts")
assert lo < 0 < hi and round(100 * hi, 2) == 0.17
# The test cannot rule out a +0.17 pt gain, nor a -0.11 pt loss. Value of each: 1M orders-able users, 400 per conversion (illustrative)
users, value = 1_000_000, 400
print("value of +0.17 pts on 1M users/month:", f"{hi*users*value:,.0f}", "; of -0.11 pts:", f"{lo*users*value:,.0f}")
assert round(hi * users * value, -3) == 660_000 and round(lo * users * value, -3) == -420_000
# How long to halve the CI? Quadruple the sample.
n2 = 4 * n
se2 = (2 * p * (1 - p) / n2) ** 0.5
print(f"4x sample ({n2:,}/arm) -> CI half-width {100*1.96*se2:.2f} pts (was {100*1.96*se:.2f})")
assert round(1.96 * se2 * 100, 2) == 0.07
# Ship cost vs run-on cost, expected value with a prior belief. P(real +0.1 pt)=0.3, else 0; ship cost 20,000/month.
gain_if_real = 0.001 * users * value
ev = 0.3 * gain_if_real
print(f"gain if real {gain_if_real:,.0f}/month; EV {ev:,.0f}/month vs maintenance 20,000")
assert gain_if_real == 400_000 and ev == 120_000
