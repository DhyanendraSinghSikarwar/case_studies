import numpy as np
from scipy.stats import ks_2samp
rng = np.random.default_rng(44)
n = 20000
THRESH = 0.80                                    # model blocks at score >= 0.80
def score(x): return 1 / (1 + np.exp(-(x - 1.0) * 2.5))   # monotone score from a risk feature
organic = rng.normal(0, 1, n)                     # week 0 traffic
score0 = score(organic)
# week 8: 15% of traffic is an adaptive attacker who tunes the feature to land just under the block line
atk = int(0.15 * n)
x_cur = rng.normal(0, 1, n)
x_cur[:atk] = rng.uniform(1.25, 1.50, atk)       # score about 0.65 to 0.76 (just below 0.80) , i.e. x < ~1.55
score1 = score(x_cur)
print("block threshold on score: %.2f (feature x=%.2f)" % (THRESH, 1 + np.log(THRESH/(1-THRESH))/2.5))
print("feature KS D=%.3f  score KS D=%.3f  block rate %.4f -> %.4f" % (
    ks_2samp(organic, x_cur).statistic, ks_2samp(score0, score1).statistic, (score0 >= THRESH).mean(), (score1 >= THRESH).mean()))

def pileup_detector(ref_scores, cur_scores, thr, width=0.10, min_ratio=2.0, min_count=30):
    """Compare the mass in the band just BELOW the threshold with the mass in the same band at reference, and with the band just ABOVE."""
    lo, hi = thr - width, thr
    ref_b = np.mean((ref_scores >= lo) & (ref_scores < hi)); cur_b = np.mean((cur_scores >= lo) & (cur_scores < hi))
    above = np.mean((cur_scores >= thr) & (cur_scores < thr + width))
    cnt = int(np.sum((cur_scores >= lo) & (cur_scores < hi)))
    return {"below_band_ref": round(float(ref_b), 4), "below_band_cur": round(float(cur_b), 4),
            "band_ratio": round(float(cur_b / ref_b), 2), "below_over_above": round(float(cur_b / max(above, 1e-9)), 2),
            "alert": bool(cnt >= min_count and cur_b / ref_b >= min_ratio)}
print("week 8 vs week 0:", pileup_detector(score0, score1, THRESH))
print("control (no attacker):", pileup_detector(score0, score(rng.normal(0, 1, n)), THRESH))
