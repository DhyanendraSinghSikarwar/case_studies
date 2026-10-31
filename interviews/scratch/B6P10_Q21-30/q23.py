# Q23 data-quality scan cost (illustrative)
import random
tables, checks, gb, price, budget = 1_500, 6, 40, 0.5, 100_000
runs = tables * checks
assert runs == 9_000
full = runs * gb * price
half = full * 0.5
assert full == 180_000 and half == 90_000
print(f"checks/day={runs}, full scan cost={full:,.0f} rupees ({full/budget:.2f}x budget), 50% sample={half:,.0f} ({half/budget:.0%} of budget)")

# Illustrative split of the 6 checks: 3 answered from metadata (almost free), 3 scan data
meta, scanning = 3, 3
mix_full = tables * scanning * gb * price
mix_half = mix_full * 0.5
assert mix_full == 90_000 and mix_half == 45_000
print(f"3 metadata + 3 scanning checks: full={mix_full:,.0f}, sampled={mix_half:,.0f}")

# Incremental scan: only the new daily partition (invented: 1/30 of the table) for the scanning checks
inc = mix_full / 30
assert inc == 3_000
print(f"incremental (new partition only, 1/30 of table): {inc:,.0f} rupees")

# Why uniqueness should not be sampled: one duplicated pair survives a 50% row sample with prob 0.25
random.seed(7)
trials, caught = 100_000, 0
for _ in range(trials):
    a, b = random.random() < 0.5, random.random() < 0.5
    caught += a and b
rate = caught / trials
assert abs(rate - 0.25) < 0.01
print(f"single duplicate pair caught by a 50% row sample: {rate:.3f} (theory 0.25)")

# A rare bad segment: 40 bad rows among 1,000,000; chance the sample contains none of them
p_none = 0.5 ** 40
assert p_none < 1e-12
# ... but chance of seeing zero of 1 bad row is 0.5, so tiny defects often vanish
print(f"sample sees none of 1 bad row: {0.5:.2f}; none of 40: {p_none:.1e}")
