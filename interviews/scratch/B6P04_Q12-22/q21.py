# Q21: a test that needs 75 months: what can this traffic detect? (illustrative numbers)
import numpy as np
from scipy.stats import norm

za, zb = norm.ppf(0.975), norm.ppf(0.80)
def n_per_arm(p1, rel_lift, alpha_z=za, power_z=zb):
    p2 = p1 * (1 + rel_lift); pbar = (p1 + p2) / 2
    return (alpha_z * np.sqrt(2 * pbar * (1 - pbar)) + power_z * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2

n = n_per_arm(0.02, 0.05)
monthly = 4_000
print(f"n per arm for 2.0% -> 2.1%: {n:,.0f}; months at {monthly:,}/arm/month = {n / monthly:.0f}")
print(f"the prompt's round figures: 300,000 / 4,000 = {300_000 / monthly:.0f} months")
assert 310_000 < n < 320_000 and 77 < n / monthly < 80 and 300_000 / monthly == 75

def mde_rel(p1, n):
    se = np.sqrt(2 * p1 * (1 - p1) / n)
    return (za + zb) * se / p1
print("\nwhat the traffic can detect (relative MDE at baseline 2.0%):")
for months in (1, 3, 6, 12, 24):
    print(f"  {months:>2} months ({months * monthly:>6,} per arm): MDE = {mde_rel(0.02, months * monthly):.0%}")
assert 0.40 < mde_rel(0.02, 4_000) < 0.46 and 0.12 < mde_rel(0.02, 48_000) < 0.14

# Option A: CUPED with a pre-period covariate (variance x (1 - rho^2)); sample size scales with variance
for rho in (0.3, 0.5, 0.7):
    print(f"CUPED rho {rho}: n = {n * (1 - rho**2):,.0f} per arm, {n * (1 - rho**2) / monthly:.0f} months")
assert abs(n * (1 - 0.7**2) / monthly - 0.51 * n / monthly) < 1e-9

# Option B: a more frequent upstream metric, for example click on the offer at 20% baseline with the same 5% lift
n_up = n_per_arm(0.20, 0.05)
print(f"upstream metric, 20% baseline, 5% lift: n = {n_up:,.0f} per arm, {n_up / monthly:.1f} months")
assert 24_000 < n_up < 27_000

# Option C: accept a larger lift as the target, or a one-sided 10% test
n_big = n_per_arm(0.02, 0.20)
print(f"target 20% relative lift: n = {n_big:,.0f} per arm, {n_big / monthly:.1f} months")
n_one = n_per_arm(0.02, 0.05, alpha_z=norm.ppf(0.90), power_z=norm.ppf(0.80))
print(f"one-sided alpha 0.10 (z = 1.28), 5% lift: n = {n_one:,.0f} per arm, {n_one / monthly:.0f} months")
assert 20_000 < n_big < 22_000 and n_one < n
# Option D: pooling more pages (same change on 10 similar pages) multiplies traffic
print(f"same change on 10 similar pages: {n / (10 * monthly):.1f} months")
print("all asserts passed")
