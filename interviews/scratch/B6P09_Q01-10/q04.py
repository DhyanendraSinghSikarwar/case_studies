import numpy as np
from scipy.stats import rankdata
from scipy.optimize import brentq
# Part A: prompt arithmetic (illustrative, measured day)
imps, clicks, v = 1_000_000, 24_000, 10
pred, obs = 0.030, clicks / imps
bid_pred, bid_true = pred * v, obs * v
overbid_vs_correct = bid_pred / bid_true - 1
excess_share_of_bid = (bid_pred - bid_true) / bid_pred
cal_ratio = obs / pred
print(f"observed CTR {obs:.1%}; bid per impression {bid_pred:.2f} (model) vs {bid_true:.2f} (calibrated)")
print(f"overbid {overbid_vs_correct:.0%} of the correct bid; excess is {excess_share_of_bid:.0%} of the bid made; fix factor {cal_ratio:.2f}")
print(f"sum of bids over the day: {bid_pred*imps:,.0f} vs {bid_true*imps:,.0f}, difference {(bid_pred-bid_true)*imps:,.0f} (bid amount, not spend)")
assert obs == 0.024 and round(bid_pred, 6) == 0.30 and round(bid_true, 6) == 0.24
assert round(overbid_vs_correct, 6) == 0.25 and round(excess_share_of_bid, 6) == 0.20 and round(cal_ratio, 6) == 0.8
assert round((bid_pred - bid_true) * imps) == 60_000

# Part B: a miscalibrated model with the same ranking, then a recalibration layer
rng = np.random.default_rng(11)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def sig(x): return 1 / (1 + np.exp(-x))
def logit(p): return np.log(p / (1 - p))
def day(n):
    p = rng.beta(1.2, 48.8, n)                      # true click probabilities, mean 2.4%
    y = (rng.random(n) < p).astype(int)
    return p, y
p1, y1 = day(400_000); p2, y2 = day(400_000)
shift = brentq(lambda d: sig(logit(p1) + d).mean() - 0.030, 0, 2)   # model over-predicts: mean 3.0%
s1, s2 = sig(logit(p1) + shift), sig(logit(p2) + shift)
print(f"day 2: mean prediction {s2.mean():.4f}, observed rate {y2.mean():.4f}, AUC raw {auc(y2, s2):.4f}, AUC of true p {auc(y2, p2):.4f}")
# recalibrate on day 1 with 20 quantile bins (monotone map), score day 2
edges = np.quantile(s1, np.linspace(0, 1, 21)); edges[0], edges[-1] = 0, 1
b1 = np.digitize(s1, edges[1:-1]); rate = np.array([y1[b1 == k].mean() for k in range(20)])
rate = np.maximum.accumulate(rate)                   # keep it monotone
c2 = rate[np.digitize(s2, edges[1:-1])]
def ece(p, y, k=10):
    q = np.quantile(p, np.linspace(0, 1, k + 1)); idx = np.clip(np.digitize(p, q[1:-1]), 0, k - 1)
    return sum(abs(p[idx == i].mean() - y[idx == i].mean()) * (idx == i).mean() for i in range(k))
print(f"mean prediction after recalibration {c2.mean():.4f}; ECE before {ece(s2, y2):.4f}, after {ece(c2, y2):.4f}; AUC after {auc(y2, c2):.4f}")
assert abs(s2.mean() - 0.030) < 0.001 and abs(y2.mean() - 0.024) < 0.001
assert abs(auc(y2, s2) - auc(y2, p2)) < 1e-9           # a monotone shift cannot change AUC
assert ece(c2, y2) < ece(s2, y2) / 5 and abs(c2.mean() - y2.mean()) < 0.001
assert abs(auc(y2, c2) - auc(y2, s2)) < 0.003         # binning adds a few ties, so allow a small change
