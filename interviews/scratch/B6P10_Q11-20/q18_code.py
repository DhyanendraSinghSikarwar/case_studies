import math
from statistics import NormalDist
import numpy as np

# Prompt arithmetic
metrics, per_day, budget = 20_000, 24 * 60, 15
points = metrics * per_day
p_max = budget / points
assert points == 28_800_000 and abs(p_max - 5.2083e-7) < 1e-10
print("data points a day:", points, "| max false-alert probability per point:", f"{p_max:.4e}")

# What threshold does that imply for a Gaussian residual? one-sided z
z = NormalDist().inv_cdf(1 - p_max)
print("one-sided z threshold for a Gaussian residual:", round(z, 2))
assert 4.8 < z < 5.0

# Check by simulation (chunked): count exceedances of z over one simulated day of independent Gaussian points
rng = np.random.default_rng(18)
hits = 0
for _ in range(29):
    hits += int((rng.standard_normal(1_000_000)[:] > z).sum())
print("simulated false alerts over 29,000,000 independent points (expected about 15):", hits)
assert 3 <= hits <= 35

# Persistence rule: alert only if k consecutive points exceed a looser per-point threshold (independence assumed, so optimistic)
q = 1e-3
for k in (1, 2, 3):
    print(f"per-point tail {q} needed k={k} in a row -> false chance per point {q ** k:.1e}; alerts/day {points * q ** k:.3g}")
assert points * q ** 3 < budget < points * q ** 2
# Grouping: if correlated metrics fire together and count as one alert
groups_of = 20
print("if 20 metrics fail together as one alert, budget per group-event:", budget, "alerts -> point-level budget can be up to", budget * groups_of / points)
assert abs(budget * groups_of / points - 1.0417e-5) < 1e-8
