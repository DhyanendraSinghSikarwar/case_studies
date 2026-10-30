from math import sqrt
from scipy.stats import norm
# Illustrative A/B: 100,000 users per arm
n = 100_000
ctr0, ctr1 = 0.100, 0.107                      # clicks / impressions
print(f"CTR lift {ctr1 / ctr0 - 1:+.1%}")
assert round(ctr1 / ctr0 - 1, 3) == 0.070
opu0 = 0.800
opu1 = opu0 * (1 - 0.015)                      # orders placed per user, -1.5%
cancel0, cancel1 = 0.050, 0.065                # share of placed orders cancelled
done0 = opu0 * (1 - cancel0)
done1 = opu1 * (1 - cancel1)
print(f"placed per user {opu0:.3f} -> {opu1:.3f}")
print(f"completed per user {done0:.4f} -> {done1:.4f} ({done1 / done0 - 1:+.1%})")
assert round(opu1, 3) == 0.788 and round(done0, 3) == 0.760 and round(done1 / done0 - 1, 3) == -0.031
# is the placed-orders gap noise? Poisson assumption: variance = mean (assumption, not data)
def z(m0, m1):
    se = sqrt(m0 / n + m1 / n)
    return (m1 - m0) / se
for name, a, b in [("placed", opu0, opu1), ("completed", done0, done1)]:
    zz = z(a, b); p = 2 * (1 - norm.cdf(abs(zz)))
    print(f"{name:10} z={zz:+.2f} p={p:.4f}")
assert round(z(opu0, opu1), 1) == -3.0 and round(z(done0, done1), 1) == -6.0
# what a click-based metric hides: orders per 1,000 impressions-led clicks (illustrative clicks per user)
imp = 50  # impressions per user
c0, c1 = ctr0 * imp, ctr1 * imp
print(f"clicks per user {c0:.2f} -> {c1:.2f}; completed orders per 100 clicks {100 * done0 / c0:.1f} -> {100 * done1 / c1:.1f}")
assert round(100 * done0 / c0, 1) == 15.2 and round(100 * done1 / c1, 1) == 13.8
