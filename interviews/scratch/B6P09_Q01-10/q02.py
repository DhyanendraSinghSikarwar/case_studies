import numpy as np
# Part A: the prompt's arithmetic (illustrative, measured position averages)
ctr1, ctr5, new_ctr = 0.12, 0.04, 0.11
pm_claim = new_ctr / ctr5                  # product manager's ratio
pos_factor = ctr1 / ctr5                   # what position alone is worth (average)
rel_ratio = pm_claim / pos_factor          # relevance change after removing position
exp_at_1 = ctr5 * pos_factor               # CTR at position 1 if relevance were unchanged
se_n2000 = (new_ctr * (1 - new_ctr) / 2000) ** 0.5
print(f"PM ratio {pm_claim:.2f}x, position alone {pos_factor:.2f}x, relevance ratio {rel_ratio:.3f}")
print(f"expected CTR at position 1 with unchanged relevance {exp_at_1:.1%} vs observed {new_ctr:.0%}")
print(f"SE of an 11% rate on 2,000 impressions {se_n2000:.4f} (about {se_n2000*100:.1f} points)")
assert pm_claim == 2.75 and round(pos_factor, 6) == 3.0 and round(rel_ratio, 4) == 0.9167
assert round(exp_at_1, 6) == 0.12 and round(se_n2000, 4) == 0.007

# Part B: simulate a position-based click model. Click = examined(position) x relevant.
rng = np.random.default_rng(7)
exam = np.array([0.60, 0.45, 0.33, 0.25, 0.20])       # true examination by position (ratio pos1/pos5 = 3)
Q = 200_000
rel = rng.beta(2, 8, size=(Q, 5))                      # true relevance of 5 candidate products per query (mean 0.2)
# production ranker: sorts by a noisy copy of relevance, so good items land on top
order = np.argsort(-(rel + rng.normal(0, 0.05, rel.shape)), axis=1)
rel_sorted = np.take_along_axis(rel, order, axis=1)
clicks = rng.random((Q, 5)) < exam * rel_sorted
ctr_pos = clicks.mean(axis=0)
naive_ratio = ctr_pos[0] / ctr_pos[4]
# randomised experiment: shuffle the order for a small slice of traffic, so position is independent of relevance
perm = rng.permuted(rel, axis=1)
clicks_r = rng.random((Q, 5)) < exam * perm
ctr_r = clicks_r.mean(axis=0)
rand_ratio = ctr_r[0] / ctr_r[4]
print("logged CTR by position   ", np.round(ctr_pos, 4), "ratio pos1/pos5", round(naive_ratio, 2))
print("randomised CTR by position", np.round(ctr_r, 4), "ratio pos1/pos5", round(rand_ratio, 2))
# inverse-propensity-weighted relevance for one product shown only at position 5, using the randomised propensity
prop = ctr_r / ctr_r[0]                                 # examination relative to position 1
clicks_at5, shows = 400, 10_000
ips_rel_vs_pos1 = (clicks_at5 / shows) / prop[4]        # CTR it would get at position 1
print(f"propensity at pos5 relative to pos1 {prop[4]:.2f}; position-1-equivalent CTR {ips_rel_vs_pos1:.3f}")
assert abs(rand_ratio - 3.0) < 0.15          # randomisation recovers the true examination ratio
assert naive_ratio > rand_ratio + 0.5        # logged ratio is inflated because the ranker puts relevant items first
assert abs(ips_rel_vs_pos1 - 0.12) < 0.01
assert round(naive_ratio, 1) == 11.6
