# Q26 cold-start exploration cost (illustrative rates, from a sample)
import random
explore, ctr_explore, ctr_policy = 0.10, 0.015, 0.03
with_exp = 100 * (explore * ctr_explore + (1 - explore) * ctr_policy)
without = 100 * ctr_policy
loss = (without - with_exp) / without
assert abs(with_exp - 2.85) < 1e-9 and abs(without - 3.0) < 1e-9 and abs(loss - 0.05) < 1e-9
print(f"clicks per 100 impressions: with exploration={with_exp:.2f}, without={without:.2f}, relative loss={loss:.1%}")

# What the learned policy must gain for exploration to pay back (rates held as assumptions)
needed = (ctr_policy - explore * ctr_explore) / (1 - explore)
assert abs(needed - 0.031667) < 1e-5
print(f"policy CTR must rise from 3.00% to {needed:.3%} ({needed/ctr_policy-1:.2%} relative) to break even")

# Simulation check with a fixed seed
random.seed(11)
n = 1_000_000
clicks = 0
for _ in range(n):
    p = ctr_explore if random.random() < explore else ctr_policy
    clicks += random.random() < p
sim = clicks / n * 100
assert abs(sim - with_exp) < 0.05
print(f"simulated clicks per 100 impressions={sim:.2f}")

# Noise in the measured rates: a 1.5% rate from 2,000 impressions (invented) has a wide interval
imp = 2_000
se = (ctr_explore * (1 - ctr_explore) / imp) ** 0.5
lo, hi = ctr_explore - 1.96 * se, ctr_explore + 1.96 * se
assert abs(lo - 0.00961) < 1e-4 and abs(hi - 0.02039) < 1e-4
print(f"1.5% from {imp} impressions: 95% interval {lo:.2%} to {hi:.2%}")
# Example: 60,000 new users x 20 impressions (invented)
imps = 60_000 * 20
assert imps == 1_200_000 and round(imps * (ctr_policy - (with_exp / 100))) == 1_800
print(f"daily clicks lost at {imps:,} impressions: {imps*(ctr_policy-with_exp/100):,.0f}")
