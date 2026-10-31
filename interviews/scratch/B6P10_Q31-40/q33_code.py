import math
from statistics import NormalDist
budget, price, rare_share, target = 6000, 3, 0.03, 200
labels = budget // price
exp_rare = labels * rare_share
sd = math.sqrt(labels * rare_share * (1 - rare_share))
print("labels", labels, "expected rare", exp_rare, "sd", round(sd, 2))
assert labels == 2000 and round(exp_rare) == 60 and round(sd, 2) == 7.63
random_needed = math.ceil(target / rare_share)
print("random labels for 200 rare:", random_needed, "cost", random_needed * price, "x budget", round(random_needed * price / budget, 2))
assert random_needed == 6667 and random_needed * price == 20_001
# 5th-95th percentile band if the true share is only 2% or 4% (the 3% is a sample)
for s in (0.02, 0.03, 0.04):
    print("true share", s, "expected rare", labels * s)
assert labels * 0.02 == 40 and labels * 0.04 == 80
# targeted sampling: labels needed if a search/model-assisted pool has precision p for the rare intent
spend_rare = 1200  # labels from the enriched pool (illustrative split)
for p in (0.15, 0.30, 0.50):
    need = math.ceil(target / p)
    print("pool precision", p, "labels for 200 rare", need, "fits 2000:", need <= labels)
assert math.ceil(200 / 0.15) == 1334 and math.ceil(200 / 0.30) == 667 and math.ceil(200 / 0.50) == 400
# split plan: 800 random labels (unbiased share + base rates) + 1,200 enriched
rand_part, enr_part = 800, 1200
rare_random = rand_part * rare_share
rare_enriched = enr_part * 0.30
print("rare from random", rare_random, "from enriched at 30%", rare_enriched, "total", rare_random + rare_enriched)
assert rare_random == 24 and round(rare_enriched) == 360 and rand_part + enr_part == labels
# even at 15% precision: 1,200 * 0.15 + 24 = 204 >= 200
assert round(enr_part * 0.15 + rare_random) == 204
# weights: enriched examples must be down-weighted (or kept out) when estimating real prevalence
