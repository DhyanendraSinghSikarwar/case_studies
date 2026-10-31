# Q26 new campaign CTR with a prior worth 200 impressions (illustrative numbers)
import numpy as np
from scipy import stats
imps, clicks = 500, 2
raw = clicks / imps
prior_ctr, prior_n = 0.015, 200
a0, b0 = prior_ctr * prior_n, (1 - prior_ctr) * prior_n      # Beta(3, 197)
assert abs(a0 - 3) < 1e-9 and abs(b0 - 197) < 1e-9
post_mean = (clicks + a0) / (imps + prior_n)
assert abs(raw - 0.004) < 1e-12 and abs(post_mean - 5 / 700) < 1e-12
print(f"raw {raw:.3%}, shrunk {post_mean:.3%}  (= (2+3)/(500+200) = 5/700)")

# Uncertainty: 90% credible intervals
a1, b1 = a0 + clicks, b0 + imps - clicks
lo, hi = stats.beta.ppf([0.05, 0.95], a1, b1)
print(f"posterior 90% interval {lo:.2%} to {hi:.2%}")
assert 0.0027 < lo < 0.0030 and 0.0129 < hi < 0.0132
# raw-only (flat prior) interval is wider
rlo, rhi = stats.beta.ppf([0.05, 0.95], clicks + .5, imps - clicks + .5)
assert rlo < lo and rhi < hi   # raw-only data sit lower and are not narrower
print(f"raw-only (Jeffreys) 90% interval {rlo:.2%} to {rhi:.2%}")
p_below = stats.beta.cdf(0.015, a1, b1)
print(f"P(true CTR < category average 1.5%) = {p_below:.3f}")
assert 0.97 < p_below < 0.99

# Exploration plan: spend cap and stopping rule (invented cost: 20 per 1,000 impressions)
cpm, cap = 20.0, 60.0
max_imps = int(cap / cpm * 1000)
assert max_imps == 3_000
print(f"cap {cap:.0f} buys {max_imps} impressions at CPM {cpm:.0f}")
# Expected course if the true CTR is 0.7% (seeded simulation, batches of 500)
rng = np.random.default_rng(7)
true = 0.007
a, b = a1, b1
n_new = 0
while n_new < max_imps:
    k = rng.binomial(500, true); a += k; b += 500 - k; n_new += 500
    p_low = stats.beta.cdf(0.010, a, b)      # stop (drop) if probably below 1.0%
    if p_low > 0.90 or p_low < 0.05:
        break
print(f"stopped after {n_new} new impressions, posterior mean {a/(a+b):.3%}, P(CTR<1.0%)={p_low:.2f}, spent {n_new*cpm/1000:.0f}")
assert n_new <= max_imps and n_new * cpm / 1000 <= cap
