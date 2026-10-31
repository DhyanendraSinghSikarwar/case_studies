# Q30 audit sample size for unsupported-claim rate (illustrative)
import math
import numpy as np
p, notes, target = 0.02, 8_000, 0.95
n = math.ceil(math.log(1 - target) / math.log(1 - p))
assert n == 149 and 1 - (1 - p) ** n >= target > 1 - (1 - p) ** (n - 1)
share = n / notes
assert round(share * 100, 2) == 1.86
print(f"smallest n={n}, share of the day's notes={share:.2%}, detection prob at n: {1-(1-p)**n:.4f} (n-1: {1-(1-p)**(n-1):.4f})")

# Power at other true rates with n = 149
for r in (0.005, 0.01, 0.02, 0.03):
    print(f"  true rate {r:.1%}: P(at least one unsupported note in sample) = {1-(1-r)**n:.3f}")
assert abs((1 - 0.995 ** n) - 0.526) < 0.002 and abs((1 - 0.99 ** n) - 0.776) < 0.002

# If zero are found in 149: one-sided 95% upper bound for the rate
upper = 1 - 0.05 ** (1 / n)
assert abs(upper - 0.01987) < 1e-4
print(f"zero found in {n}: upper 95% bound on the rate = {upper:.2%}")

# Seeded simulation of the daily audit when the true rate is exactly 2%
rng = np.random.default_rng(5)
days = 200_000
hits = rng.binomial(n, p, size=days)
detect = (hits >= 1).mean()
assert abs(detect - 0.9506) < 0.005
print(f"simulated detection rate at 2% = {detect:.4f}")

# Per hospital: 12 hospitals, same guarantee for each
per_h_total = 12 * n
assert per_h_total == 1_788 and round(per_h_total / notes * 100, 2) == 22.35
print(f"same guarantee per hospital: {per_h_total} notes a day = {per_h_total/notes:.2%} of notes")
print(f"pooled sample gives {n/12:.1f} notes per hospital on average")
assert round(n / 12, 1) == 12.4
# Rotation alternative: each hospital gets the full 149 on one day of every 12-day cycle (invented schedule)
print(f"rotation: one hospital per day gets {n}; each hospital audited every 12 days")
