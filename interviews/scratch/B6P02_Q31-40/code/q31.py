# Q31: ads click model over-predicts (ratio 1.12) while AUC is unchanged (illustrative simulation)
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(31)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
logit = lambda p: np.log(p / (1 - p))
sig = lambda z: 1 / (1 + np.exp(-z))

N = 1_200_000
p_true = np.clip(rng.lognormal(np.log(0.02), 0.8, N), 1e-4, 0.5)   # true CTR per impression
y = (rng.random(N) < p_true).astype(int)

# Drift = a constant shift in the log-odds. Find the shift that gives predicted/observed = 1.12.
lo, hi = 0.0, 0.5
for _ in range(60):
    mid = (lo + hi) / 2
    if sig(logit(p_true) + mid).mean() / y.mean() < 1.12: lo = mid
    else: hi = mid
shift = (lo + hi) / 2
p_pred = sig(logit(p_true) + shift)
ratio = p_pred.mean() / y.mean()
print(f"shift in log-odds: {shift:.3f}   predicted/observed: {ratio:.3f}")
assert abs(ratio - 1.12) < 0.01          # observed clicks are random, so allow 0.01

# AUC does not see a monotone shift at all
a0, a1 = auc(y, p_true), auc(y, p_pred)
print(f"AUC before drift {a0:.4f}   after drift {a1:.4f}")
assert abs(a0 - a1) < 1e-12

# Why bidding cares: bid = value_per_click * pCTR. Real value of an impression = value * true CTR.
v = 10.0                                   # Rs per click (illustrative)
rival = rng.lognormal(np.log(v * 0.02), 0.8, N)   # rival bids
rival_fp = rival * 0.6                              # rivals shade too
def second_price(p_used):                  # winner pays the rival bid
    win = v * p_used > rival
    return (v * p_true[win] - rival[win]).sum(), win.sum()
def first_price(p_used):                   # winner pays its own bid
    bid = 0.6 * v * p_used; win = bid > rival_fp   # shade the bid to 60% of value
    return (v * p_true[win] - bid[win]).sum(), win.sum(), bid[win].sum()
sp_ok, w_ok = second_price(p_true); sp_bad, w_bad = second_price(p_pred)
fp_ok, _, spend_ok = first_price(p_true); fp_bad, _, spend_bad = first_price(p_pred)
print(f"second price: won {w_ok} -> {w_bad}; profit Rs {sp_ok:,.0f} -> {sp_bad:,.0f}")
print(f"first price : profit Rs {fp_ok:,.0f} -> {fp_bad:,.0f}; spend Rs {spend_ok:,.0f} -> {spend_bad:,.0f}")
assert w_bad > w_ok and sp_bad < sp_ok     # extra wins are the unprofitable ones
assert fp_bad < 0.9 * fp_ok and 0.8 < sp_bad / sp_ok < 1 and spend_bad > 1.12 * spend_ok   # you pay your own inflated bid

# Recalibrate WITHOUT retraining: fit one intercept on the log-odds of the old score
# using a recent window (first 800k impressions), then test on the rest.
fit, test = slice(0, 800_000), slice(800_000, N)
z = logit(p_pred[fit]); b = 0.0
for _ in range(25):                         # Newton steps on the intercept only
    q = sig(z + b)
    b -= (q - y[fit]).sum() / (q * (1 - q)).sum()
p_fix = sig(logit(p_pred) + b)
r_fix = p_fix[test].mean() / y[test].mean()
print(f"fitted offset {b:.3f}   ratio on holdout after fix {r_fix:.3f}")
assert abs(b + shift) < 0.06 and abs(r_fix - 1) < 0.03
assert abs(auc(y, p_fix) - a1) < 1e-12      # ranking is untouched
fp_fix, _, _ = first_price(p_fix)
print(f"first-price profit after fix (Rs): {fp_fix:,.0f}")
assert fp_fix > fp_bad

# Segment trap: overall 1.12 can hide one bad segment, and one global factor then mis-fixes both.
share = np.array([0.65, 0.35]); seg_ratio = np.array([1.00, 1.45])
pred = np.array([0.020, 0.020]); obs = pred / seg_ratio
overall = (share * pred).sum() / (share * obs).sum()
print(f"overall ratio {overall:.3f}; segment ratios {seg_ratio}")
assert abs(overall - 1.12) < 0.005
after_global = seg_ratio / overall          # divide every prediction by the overall ratio
print("after one global factor, segment ratios:", np.round(after_global, 3))
assert after_global[0] < 0.9 and after_global[1] > 1.25
