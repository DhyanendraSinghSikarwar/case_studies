# Q12: sample size, MDE and duration for a 5.0% -> 5.25% test (illustrative numbers)
import numpy as np
from scipy.stats import norm

alpha, power = 0.05, 0.80
p1, lift_rel = 0.05, 0.05
p2 = p1 * (1 + lift_rel)
daily_visitors = 20_000
per_arm_per_day = daily_visitors // 2
za, zb = norm.ppf(1 - alpha / 2), norm.ppf(power)

def n_per_arm(p1, p2):
    pbar = (p1 + p2) / 2
    num = (za * np.sqrt(2 * pbar * (1 - pbar)) + zb * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return num / (p2 - p1) ** 2

n = n_per_arm(p1, p2)
days = n / per_arm_per_day
print(f"p2 = {p2:.4f}, delta = {p2 - p1:.4f}")
print(f"n per arm = {n:,.0f}  ->  {days:.1f} days at {per_arm_per_day:,} per arm per day")

n3 = 3 * per_arm_per_day
se3 = np.sqrt(p1 * (1 - p1) / n3 * 2)
mde3 = (za + zb) * se3
print(f"3 days: {n3:,} per arm, MDE = {mde3:.4f} abs = {mde3 / p1:.1%} relative")
# power at 3 days for the planned +0.25 points
se_alt = np.sqrt(p1 * (1 - p1) / n3 + p2 * (1 - p2) / n3)
pw3 = norm.cdf(abs(p2 - p1) / se_alt - za)
print(f"power at 3 days for +0.25 points = {pw3:.2f}")

# simulation check of power at 3 days and at 14 days
rng = np.random.default_rng(12)
def sim_power(n, reps=4000):
    c = rng.binomial(n, p1, reps); t = rng.binomial(n, p2, reps)
    pc, pt = c / n, t / n
    pp = (c + t) / (2 * n)
    z = (pt - pc) / np.sqrt(2 * pp * (1 - pp) / n)
    return np.mean(np.abs(z) > za)
s3, s14 = sim_power(n3), sim_power(14 * per_arm_per_day)
print(f"simulated power: 3 days {s3:.2f}, 14 days {s14:.2f}")
# false positive rate when there is no effect (A/A) at 14 days
c = rng.binomial(140_000, p1, 4000); t = rng.binomial(140_000, p1, 4000)
pp = (c + t) / 280_000
z = (t - c) / 140_000 / np.sqrt(2 * pp * (1 - pp) / 140_000)
print(f"simulated A/A rejection rate = {np.mean(np.abs(z) > za):.3f}")

assert 121_000 < n < 123_500 and 12.0 < days < 12.5
assert abs(mde3 / p1 - 0.10) < 0.005
assert 0.25 < pw3 < 0.32 and abs(s3 - pw3) < 0.04
assert s14 > 0.80 and abs(np.mean(np.abs(z) > za) - 0.05) < 0.015
assert abs((1 - 0.5**2) - 0.75) < 1e-12  # CUPED rho=0.5 keeps 75% of variance
print("all asserts passed")
