# Q17: is 93.1% -> 92.4% (n=20,000 each) signal or noise, and what monitoring design? (illustrative, seeded)
import numpy as np
from scipy.stats import norm
rng = np.random.default_rng(17)

p1, p2, n = 0.931, 0.924, 20_000
se = np.sqrt(p1 * (1 - p1) / n + p2 * (1 - p2) / n)
z = (p1 - p2) / se
pval = 2 * (1 - norm.cdf(z))
print(f"two-proportion test: SE = {100*se:.3f} points, z = {z:.2f}, two-sided p = {pval:.4f}")
assert abs(se - 0.002593) < 1e-5 and 2.6 < z < 2.8 and 0.005 < pval < 0.009
mde = (norm.ppf(0.975) + norm.ppf(0.8)) * se
print(f"smallest week-over-week change detectable with 80% power at this n: {100*mde:.2f} points")
assert 0.0070 < mde < 0.0077
# Single-sample 95% interval for one week
hw = 1.96 * np.sqrt(p1 * (1 - p1) / n)
print(f"one week 93.1% +/- {100*hw:.2f} points (binomial noise alone)")

# Simulation: stable model at 92.8% for 52 weeks, n=20,000 per week
W, runs, base = 52, 4000, 0.928
wk = rng.binomial(n, base, size=(runs, W)) / n
# Rule A: alert whenever this week differs from last week at p<0.05 (two-proportion z)
zA = (wk[:, 1:] - wk[:, :-1]) / np.sqrt(2 * base * (1 - base) / n)
fa_A = (np.abs(zA) > 1.96).mean()
# Rule B: Shewhart 3-sigma limits around the baseline measured in a 8-week reference window
ref_mu = wk[:, :8].mean(axis=1, keepdims=True)
sd = np.sqrt(ref_mu * (1 - ref_mu) / n)
fa_B = (np.abs(wk[:, 8:] - ref_mu) > 3 * sd).mean()
# Rule C: pooled 4-week window (80,000 cases) against the same baseline, 3-sigma limit on the pooled rate
roll = np.stack([wk[:, t - 3:t + 1].mean(axis=1) for t in range(11, W)], axis=1)   # windows fully after the reference period
sdC = sd / 2
fa_C = (roll < ref_mu - 3 * sdC).mean()
fa_C_runs = (roll < ref_mu - 3 * sdC).any(axis=1).mean()
print(f"stable model, 52 weeks: week-on-week p<0.05 rule false alarms/week = {100*fa_A:.1f}% (about {fa_A*51:.1f} per year)")
print(f"  3-sigma control limit false alarms/week = {100*fa_B:.2f}% ; pooled 4-week rule: false alarms/window = {100*fa_C:.2f}%, chance of any false alarm in the year = {100*fa_C_runs:.1f}%")
assert 0.04 < fa_A < 0.06 and fa_B < 0.01 and fa_C_runs < 0.20

# Slow decline: 0.05 points lost per week starting at week 9 (index 8)
decl = base - 0.0005 * np.maximum(0, np.arange(W) - 8)
wk_d = rng.binomial(n, decl, size=(runs, W)) / n
ref2 = wk_d[:, :8].mean(axis=1, keepdims=True); sd2 = np.sqrt(ref2 * (1 - ref2) / n)
# week-on-week rule: alert if drop vs last week significant; slow decline moves 0.15 pts a week, below its MDE
zD = (wk_d[:, 1:] - wk_d[:, :-1]) / np.sqrt(2 * base * (1 - base) / n)
alerts_A = ((zD < -1.96)[:, 8:]).mean()
first_B = np.full(runs, -1)
for t in range(8, W):
    hit = (wk_d[:, t] < ref2[:, 0] - 3 * sd2[:, 0]) & (first_B < 0); first_B[hit] = t
rollD = np.stack([wk_d[:, t - 3:t + 1].mean(axis=1) for t in range(11, W)], axis=1)
first_C = np.full(runs, -1)
for j, t in enumerate(range(11, W)):
    hit = (rollD[:, j] < ref2[:, 0] - 3 * sd2[:, 0] / 2) & (first_C < 0); first_C[hit] = t
def delay(f):
    ok = f >= 0
    return ok.mean(), (f[ok] - 8).mean()
dB, dC = delay(first_B), delay(first_C)
print(f"slow decline 0.05 pt/week from week 9: weekly drop alert fires in {100*alerts_A:.1f}% of those weeks (looks like noise level {100*fa_A:.1f}%)")
print(f"  3-sigma limit: detected in {100*dB[0]:.0f}% of runs, mean delay {dB[1]:.1f} weeks;  pooled 4-week: detected {100*dC[0]:.0f}%, mean delay {dC[1]:.1f} weeks")
assert dC[0] > 0.95 and dC[1] < dB[1] and alerts_A < 0.08
