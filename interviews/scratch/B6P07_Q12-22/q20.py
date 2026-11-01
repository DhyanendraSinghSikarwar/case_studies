import math
weekly, share, price = 700_000, 0.10, 0.0153
shadow = weekly * share
cost = shadow * price
print(f"shadow calls {shadow:,.0f}; weekly cost {cost:,.0f}; full-traffic equivalent {weekly*price:,.0f}")
assert shadow == 70_000 and round(cost) == 1071 and round(weekly * price) == 10_710
rule3 = 3 / shadow
print(f"0 failures in {shadow:,.0f} shadow calls -> 95% upper bound ~{rule3:.4%} per call (rule of three)")
assert round(rule3 * 100, 4) == 0.0043
# What an A/B test needs to see a 1-point change in a 60% resolution rate (80% power, 5% two-sided).
za, zb = 1.96, 0.84
p = 0.60
n_arm = 2 * p * (1 - p) * (za + zb) ** 2 / 0.01 ** 2
print(f"A/B needs ~{n_arm:,.0f} conversations per arm for +1 point at 60%")
assert round(n_arm) == 37_632
# Disagreement review: if models differ on 12% of shadow calls, how many are there to read?
dis = shadow * 0.12
print(f"if 12% disagree: {dis:,.0f} pairs; reviewing a random 400 gives a margin of about +-{1.96*math.sqrt(0.25/400)*100:.1f} pts on 'candidate better'")
assert dis == 8400 and round(1.96 * math.sqrt(0.25 / 400) * 100, 1) == 4.9
