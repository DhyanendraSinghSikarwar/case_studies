# Illustrative: five metrics, no true effect. Multiple-comparison arithmetic plus a seeded simulation.
import numpy as np
m, alpha = 5, 0.05
fwer = 1 - (1 - alpha) ** m
print(f"P(at least one p<0.05 | 5 independent nulls) = {fwer:.4f}")
assert round(fwer, 3) == 0.226
bonf = alpha / m
sidak = 1 - (1 - alpha) ** (1 / m)
print(f"Bonferroni per-metric level {bonf:.4f}, Sidak {sidak:.5f}")
assert bonf == 0.01 and round(sidak, 5) == 0.01021
print(f"FWER with Bonferroni 0.01 each: {1-(1-bonf)**m:.4f}")
assert 1 - (1 - bonf) ** m < alpha
rng = np.random.default_rng(28)
sims = rng.uniform(size=(200_000, m))          # p-values are uniform under the null
any_sig = (sims < alpha).any(axis=1).mean()
any_bonf = (sims < bonf).any(axis=1).mean()
print(f"simulated: raw {any_sig:.3f}, Bonferroni {any_bonf:.3f}")
assert abs(any_sig - 0.226) < 0.005 and abs(any_bonf - 0.049) < 0.004
# What the team saw: smallest of five p-values. Its median under the null:
minp = sims.min(axis=1)
print(f"median of the smallest p-value under the null: {np.median(minp):.3f}")
assert abs(np.median(minp) - (1 - 0.5 ** (1 / 5))) < 0.003
# Holm on an example: p = 0.030, 0.20, 0.45, 0.60, 0.80 (one 'win' at 0.03)
p = np.array([0.030, 0.20, 0.45, 0.60, 0.80])
order = np.argsort(p)
holm_ok = [p[i] <= alpha / (m - k) for k, i in enumerate(order)]
holm_ok = [bool(x) for x in holm_ok]
print("Holm rejects:", holm_ok)
assert not any(holm_ok)
