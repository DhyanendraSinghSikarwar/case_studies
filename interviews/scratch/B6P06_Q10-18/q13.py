import math
# headline: approval rates and impact ratio
ra, rb = 0.60, 0.42
print("impact ratio", round(rb / ra, 2))
assert round(rb / ra, 2) == 0.70 and rb / ra < 0.8
# is the gap beyond noise? invented n = 10,000 applicants per group
n = 10_000
se = math.sqrt(ra * (1 - ra) / n + rb * (1 - rb) / n)
z = (ra - rb) / se
print("gap 18 pts, z =", round(z, 1))
assert z > 25
# Test of the business head's claim: compare approval WITHIN risk bands (invented).
# policy approves 90% / 50% / 10% of low / mid / high risk bands, same for both groups
rate = {"low": 0.9, "mid": 0.5, "high": 0.1}
mixA = {"low": 0.50, "mid": 0.25, "high": 0.25}
mixB = {"low": 0.25, "mid": 0.30, "high": 0.45}
def overall(mix, adj=1.0):
    return sum(mix[b] * rate[b] * adj for b in mix)
oA, oB = overall(mixA), overall(mixB)
print("World 1 (explained by mix): A", round(oA, 3), "B", round(oB, 3), "ratio", round(oB / oA, 2))
assert round(oA, 3) == 0.60 and round(oB, 3) == 0.42
# standardise B to A's mix: if equal within bands, ratio is 1.0
std = overall(mixA)
print("World 1 mix-standardised ratio:", round(std / oA, 2))
assert std / oA == 1.0
# World 2: B gets only 70% of the approval rate A gets in EVERY band, same risk mix as A
oB2 = overall(mixA, 0.70)
print("World 2 (not explained): B with A's own mix:", round(oB2, 3), "ratio", round(oB2 / oA, 2))
assert round(oB2 / oA, 2) == 0.70
# Same 0.70 headline from two different worlds: only the within-band comparison tells them apart.
# If risk is real, defaults should match the score: observed default per band should be equal across groups.
