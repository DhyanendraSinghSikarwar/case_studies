import numpy as np
from scipy import stats

n = 40_000
p_c, p_t = 0.100, 0.101
se = np.sqrt(p_t * (1 - p_t) / n + p_c * (1 - p_c) / n)
d = p_t - p_c
lo, hi = d - 1.96 * se, d + 1.96 * se
print(f"diff = {d*100:.2f} pts, se = {se*100:.3f} pts, 95% CI = {lo*100:.2f} to {hi*100:.2f} pts")
assert round(lo * 100, 1) == -0.3 and round(hi * 100, 1) == 0.5
z = d / se
print(f"z = {z:.2f}, p = {2*stats.norm.sf(z):.2f}")

# Smallest effect this test could reliably detect (80% power, 5% two-sided)
mde = (stats.norm.isf(0.025) + stats.norm.isf(0.2)) * np.sqrt(2 * 0.1 * 0.9 / n)
print(f"MDE (80% power) = {mde*100:.2f} pts = {mde/p_c*100:.1f}% relative")
assert 0.0055 < mde < 0.0065

# Users per arm needed to detect +0.3 pt (3% relative) at 80% power
def n_per_arm(p1, p2, alpha=0.05, power=0.8):
    za, zb = stats.norm.isf(alpha / 2), stats.norm.isf(1 - power)
    pb = (p1 + p2) / 2
    num = (za * np.sqrt(2 * pb * (1 - pb)) + zb * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return num / (p2 - p1) ** 2
n3 = n_per_arm(0.100, 0.103)
print(f"users per arm to detect +0.3 pts: {n3:,.0f}")
assert 155_000 < n3 < 165_000

# Simulation: how often would this test see 'significant' if the true lift were +0.3 pts?
rng = np.random.default_rng(5)
sims = 20_000
a = rng.binomial(n, 0.100, sims) / n
b = rng.binomial(n, 0.103, sims) / n
pp = (a + b) / 2
zz = (b - a) / np.sqrt(2 * pp * (1 - pp) / n)
power = (zz > 1.96).mean()
print(f"power at n=40,000 per arm if true lift = +0.3 pts: {power:.2f}")
assert 0.2 < power < 0.4
