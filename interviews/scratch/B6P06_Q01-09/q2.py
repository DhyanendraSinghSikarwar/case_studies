import math
from scipy import stats
# holdout (illustrative): 10,000 leads, overall conversion 6%, top decile 18%
n, top_n = 10_000, 1_000
conv_all, conv_top = 0.06 * n, 0.18 * top_n
lift = 0.18 / 0.06
share = conv_top / conv_all
print(f"lift {lift:.1f}x; top decile holds {share:.0%} of all conversions")
assert lift == 3.0 and round(conv_all) == 600 and round(conv_top) == 180 and round(share, 2) == 0.30

# is 18% vs 6% noise? 180 of 1,000 vs the other 420 of 9,000
p_rest = (600 - 180) / 9000
z = (0.18 - p_rest) / math.sqrt(0.18*0.82/1000 + p_rest*(1-p_rest)/9000)
print(f"rest-of-leads rate {p_rest:.3%}, z = {z:.1f}")
assert round(p_rest, 4) == 0.0467 and z > 10

# his ten leads: assume (illustrative) 15% of truly strong leads sit in the bottom half
miss = 0.15
known = 200                       # strong leads he can name over a year
print(f"expected misses among {known} strong leads: {known*miss:.0f}")
assert known * miss == 30
# chance that ten random strong leads are ALL in bottom half if model is decent
p10 = miss ** 10
print(f"P(10 random strong leads all in bottom half) = {p10:.2e}")
assert p10 < 1e-8
# but he can pick the 10 worst of 200: expected bottom-half count is 30, so ten is easy
assert stats.binom.sf(9, known, miss) > 0.999
print("P(at least 10 bottom-half leads among 200) > 0.999")
