from fractions import Fraction as F
import numpy as np

inc = [F(5, 1000), F(3, 1000), F(15, 10000), F(5, 10000)]   # 0.50%, 0.30%, 0.15%, 0.05%
value, cost = 20, F(5, 100)
net = [p * value - cost for p in inc]
print("net value per impression:", [float(x) for x in net])
assert [float(x) for x in net] == [0.05, 0.01, -0.02, -0.04]
cum, run = [], F(0)
for x in net:
    run += x; cum.append(run)
print("cumulative net per user by cap 1..4:", [float(x) for x in cum])
assert [float(x) for x in cum] == [0.05, 0.06, 0.04, 0.0]
best = max(range(4), key=lambda i: cum[i]) + 1
assert best == 2
breakeven = cost / value
print("break-even incremental probability per impression:", float(breakeven))
assert float(breakeven) == 0.0025
# Margin: impression 2 clears break-even by 0.05 points; how far can its true probability fall?
margin = float(inc[1] - breakeven)
print("impression 2 margin over break-even (probability points):", round(margin * 100, 3))
assert round(margin * 100, 3) == 0.05

# Sample size to tell 0.30% from 0.25% in a two-arm randomised comparison (cap 2 vs cap 1 arms)
# Both arms convert at roughly 1% (illustrative baseline), so the variance per user is ~ p(1-p).
p0 = 0.010
za, zb = 1.96, 0.84
delta = 0.0005
n_per_arm = 2 * (za + zb) ** 2 * p0 * (1 - p0) / delta ** 2
print("users per arm to detect a 0.05-point gap at 1% baseline (80% power):", round(n_per_arm))
assert 600_000 < n_per_arm < 650_000
# And to detect the full 0.30-point effect of the 2nd impression versus zero
n_full = 2 * (za + zb) ** 2 * p0 * (1 - p0) / 0.003 ** 2
print("users per arm to detect the 0.30-point effect:", round(n_full))
assert 15_000 < n_full < 20_000

# Selection check: users who reach 4 impressions are more active. Illustrative simulation.
rng = np.random.default_rng(20)
n = 400_000
activity = rng.gamma(2, 0.5, n)                 # latent intent, mean 1
imps = np.minimum(rng.poisson(1.2 * activity), 4)
base = 0.004 * activity                        # conversion without ads depends on intent
conv = rng.random(n) < base                    # zero true ad effect
r1 = conv[imps == 1].mean(); r4 = conv[imps == 4].mean(); r0 = conv[imps == 0].mean()
print("sim with ZERO ad effect: conversion rate by impressions seen 0/1/4:", round(float(r0), 4), round(float(r1), 4), round(float(r4), 4))
assert r4 > r1 > r0                             # observational 'dose-response' appears without any causal effect
