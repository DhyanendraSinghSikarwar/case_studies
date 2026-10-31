import math
import numpy as np
from scipy import stats

# Illustrative numbers from the prompt
p1, p2, alpha, power, n_suite = 0.80, 0.75, 0.05, 0.80, 200
d = p1 - p2
za, zb = stats.norm.ppf(1 - alpha / 2), stats.norm.ppf(power)
var_unpaired = p1 * (1 - p1) + p2 * (1 - p2)          # variance of (x1 - x2) per prompt if independent
n_per = (za + zb) ** 2 * var_unpaired / d ** 2
print(f"z_alpha/2 = {za:.3f}, z_power = {zb:.3f}, variance sum = {var_unpaired:.4f}")
print(f"unpaired n per version = {n_per:.1f} -> {math.ceil(n_per)}; suite of {n_suite} is {n_suite/math.ceil(n_per):.0%} of that")
assert round(var_unpaired, 4) == 0.3475 and math.ceil(n_per) == 1091 and round(n_suite / 1091, 2) == 0.18

# Power of the 200-prompt suite for the same 5-point drop (unpaired, two-sided)
se200 = math.sqrt(var_unpaired / n_suite)
pw200 = stats.norm.sf(za - d / se200) + stats.norm.cdf(-za - d / se200)
print(f"power of a {n_suite}-prompt unpaired comparison: {pw200:.2f}")
assert 0.20 < pw200 < 0.25

# One-sided test (only care about drops) needs fewer
za1 = stats.norm.ppf(1 - alpha)
n_one = (za1 + zb) ** 2 * var_unpaired / d ** 2
print("one-sided n per version:", math.ceil(n_one))
assert math.ceil(n_one) == 860

# Paired: same prompts for both versions. Variance of the per-prompt difference falls with the correlation rho
# between the two versions' pass/fail on a prompt (rho is invented; measure it on a pilot).
def n_paired(rho):
    cov = rho * math.sqrt(p1 * (1 - p1) * p2 * (1 - p2))
    var = var_unpaired - 2 * cov
    return (za + zb) ** 2 * var / d ** 2
for rho in (0.0, 0.5, 0.7, 0.9):
    print(f"rho {rho}: prompts needed (paired) = {math.ceil(n_paired(rho))}")
assert math.ceil(n_paired(0.0)) == 1091 and math.ceil(n_paired(0.5)) == 548 and math.ceil(n_paired(0.7)) == 330 and math.ceil(n_paired(0.9)) == 113

# Check by simulation (seeded): paired design at rho = 0.7 with n = 330 prompts detects the drop about 80% of the time
rng = np.random.default_rng(11)
def sim_power(n, rho, reps=4000):
    cov = rho * math.sqrt(p1 * (1 - p1) * p2 * (1 - p2))
    # joint distribution of (pass_v1, pass_v2)
    p11 = p2 * 0 + (p1 * p2 + cov)
    p10 = p1 - p11; p01 = p2 - p11; p00 = 1 - p11 - p10 - p01
    cells = rng.multinomial(n, [p11, p10, p01, p00], size=reps)
    b, c = cells[:, 1], cells[:, 2]       # discordant counts
    z = (b - c) / np.sqrt(np.maximum(b + c, 1))     # McNemar z
    return float(np.mean(z > za))                    # drop detected, one direction (the other tail is negligible)
pw = sim_power(330, 0.7)
print(f"simulated power, paired, rho 0.7, n 330: {pw:.2f}")
assert 0.75 < pw < 0.86
