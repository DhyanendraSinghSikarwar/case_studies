# Q17: one 'winning' segment out of 40 after a flat overall test (simulation, illustrative numbers)
import numpy as np
from scipy.stats import norm

rng = np.random.default_rng(17)
m, alpha1 = 40, 0.01
print(f"P(at least one of {m} null segments has p <= {alpha1}) = 1 - 0.99^{m} = {1 - 0.99**m:.3f}")
assert abs((1 - 0.99**m) - 0.331) < 0.001

# Simulate: every segment has a true effect of exactly 0; z ~ N(0,1) in each segment
reps = 200_000
z = rng.standard_normal((reps, m))
p = 2 * norm.sf(np.abs(z))
any_001 = np.mean((p <= alpha1).any(axis=1))
print(f"simulated: {any_001:.3f} of null experiments show at least one segment with p <= 0.01")
assert abs(any_001 - 0.331) < 0.005

# What corrections say about p = 0.01 when it is the smallest of 40
bonf = 0.05 / m
print(f"Bonferroni threshold 0.05/{m} = {bonf:.5f}; p = 0.01 passes? {0.01 <= bonf}")
# Benjamini-Hochberg: smallest p is compared with 0.05 * 1/40
bh = 0.05 * 1 / m
print(f"BH threshold for rank 1 = {bh:.5f}; p = 0.01 passes? {0.01 <= bh}")
assert 0.01 > bonf and 0.01 > bh

# A segment with +9% and p = 0.01 has an SE of about 9% / 2.576
se = 0.09 / norm.isf(0.005)
print(f"SE implied for the segment = {se:.1%} relative; its 95% CI is {0.09 - 1.96*se:+.1%} to {0.09 + 1.96*se:+.1%}")
assert 0.034 < se < 0.036

# Winner's curse: 5 of 40 segments have a real +2%, others 0, SE 3.5%. Pick the segment with the best estimate.
se_seg, true = 0.035, np.zeros(m); true[:5] = 0.02
est = true + se_seg * rng.standard_normal((reps, m))
best = est.argmax(axis=1)
sel_est = est[np.arange(reps), best]
sel_true = true[best]
print(f"best segment: mean estimate {sel_est.mean():+.1%}, mean true effect {sel_true.mean():+.2%}, picked a truly null segment {np.mean(sel_true == 0):.0%} of the time")
assert sel_est.mean() > 0.07 and sel_true.mean() < 0.01 and 0.6 < np.mean(sel_true == 0) < 0.75

# Replication on fresh data for the chosen segment (a confirmatory test with a new sample)
new = true[best] + se_seg * rng.standard_normal(reps)
print(f"replication estimate of the chosen segments: {new.mean():+.2%} (the first-look estimate was {sel_est.mean():+.1%})")
assert new.mean() < 0.01
# Chance that a truly null chosen segment passes a one-sided replication at 5%
print("pass rate of a replication at one-sided 5% for chosen segments:", f"{np.mean(new / se_seg > norm.isf(0.05)):.1%}")
print("all asserts passed")
