# Q27 vernacular search evaluation labelling plan (illustrative)
import math
from statistics import NormalDist
budget, price, langs, moe = 120_000, 4, 8, 0.025
bought = budget // price
n_raw = (1.96 * 0.5 / moe) ** 2
n = math.ceil(n_raw)
total = langs * n
left = bought - total
assert bought == 30_000 and abs(n_raw - 1536.64) < 1e-9 and n == 1537
assert total == 12_296 and left == 17_704
print(f"bought={bought}, n per language={n} (raw {n_raw:.2f}), total={total}, remaining={left} judgements = {left*price} rupees")

# Joint coverage of 8 separate 95% intervals
joint = 0.95 ** langs
assert abs(joint - 0.6634) < 1e-3
print(f"chance all 8 intervals cover their truth ~ {joint:.1%} (independent)")

# Bonferroni: 8 intervals jointly at 95%
z = NormalDist().inv_cdf(1 - 0.05 / (2 * langs))
nb = math.ceil((z * 0.5 / moe) ** 2)
assert abs(z - 2.734) < 0.001 and nb == 2991 and langs * nb == 23_928 and bought - langs * nb == 6_072
print(f"Bonferroni z={z:.3f}, n per language={nb}, total={langs*nb}, remaining={bought-langs*nb}")

# Comparing two rankers on separate samples needs more (a paired design on shared queries can need less)
# Unpaired two-sample on proportions near 50%: n per arm = 2*(1.96*0.5/0.025)^2
nu = math.ceil(2 * (1.96 * 0.5 / 0.025) ** 2)
assert nu == 3074
print(f"unpaired comparison of two systems at same precision: {nu} per language per system")
assert langs * n * price == 49_184 and left - 1_600 * langs == 4_904 and left * price == 70_816
