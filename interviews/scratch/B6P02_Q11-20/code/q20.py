# Q20: renamed column + silent default 0 for order_value (illustrative simulation, seeded, numpy+scipy)
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(20)
sig = lambda z: 1 / (1 + np.exp(-z))
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

# Fixed model: score uses log(order_value) and one other feature
def model(order_value, other):
    return 1.6 * (np.log1p(order_value) - 6.0) / 0.8 * 0.55 + 1.6 * other
def day_data(n, bad_share):
    ov = rng.lognormal(6.0, 0.8, n)                       # order value in rupees, median about Rs 400
    other = rng.normal(size=n)
    true_logit = -1.0 + 1.6 * (np.log1p(ov) - 6.0) / 0.8 * 0.55 + 1.6 * other
    y = (rng.random(n) < sig(true_logit)).astype(int)
    bad = rng.random(n) < bad_share                        # rows served by the new upstream path
    ov_seen = np.where(bad, 0.0, ov)                       # new column not read -> default 0
    return ov_seen, other, y, bad

DAYS, BREAK, N = 14, 7, 20_000                             # break on day index 7 (day 8)
print("day  zero_share  null_share  median_ov   AUC")
zs, aucs = [], []
for d in range(DAYS):
    share = 0.0 if d < BREAK else 0.06                    # 6% of rows go through the new path
    ov, oth, y, bad = day_data(N, share)
    s = model(ov, oth)
    z = (ov == 0).mean(); zs.append(z); aucs.append(auc(y, s))
    print(f"{d+1:3d}  {z:9.3f}  {0.0:9.3f}  {np.median(ov):9.1f}  {aucs[-1]:.4f}")
pre, post = np.mean(aucs[:BREAK]), np.mean(aucs[BREAK:])
print(f"mean AUC before break {pre:.3f}, after break {post:.3f}")
assert pre - post > 0.015
assert max(zs[:BREAK]) < 0.001 and min(zs[BREAK:]) > 0.04

# Day-one checks, written as code
def checks(ov, expected_cols, cols, dtypes):
    out = {}
    out["schema: column present"] = "order_value" in cols
    out["schema: dtype float"] = dtypes.get("order_value") == "float64"
    out["null rate <= 1%"] = np.isnan(ov).mean() <= 0.01
    out["range: min > 0"] = np.nanmin(ov) > 0
    out["zero share <= 0.5%"] = (ov == 0).mean() <= 0.005
    out["median in [200, 800]"] = 200 <= np.nanmedian(ov) <= 800
    return out
ov_ok, _, _, _ = day_data(N, 0.0)
ov_bad, _, _, _ = day_data(N, 0.06)
good = checks(ov_ok, None, ["order_value"], {"order_value": "float64"})
# renamed column: the model-facing frame has the old name filled by default, so schema check on the new name catches it
bad_res = checks(ov_bad, None, ["order_value"], {"order_value": "float64"})
print("check                       healthy day   break day")
for k in good: print(f"{k:27} {str(good[k]):11}   {bad_res[k]}")
assert all(good.values()) and not bad_res["range: min > 0"] and not bad_res["zero share <= 0.5%"] and bad_res["null rate <= 1%"] and bad_res["median in [200, 800]"]
print("note: the null-rate check PASSES on the break day; range and zero-share checks fail (the median check also passes), because the default 0 is a valid number")

# Bisect to the cause with the logged data: AUC by 'served through new path' flag on day 8
ov, oth, y, bad = day_data(N, 0.06)
s = model(ov, oth)
print(f"day 8 AUC overall {auc(y, s):.3f}; rows via new path {auc(y[bad], s[bad]):.3f}; rows via old path {auc(y[~bad], s[~bad]):.3f}")
assert auc(y[~bad], s[~bad]) - auc(y[bad], s[bad]) > 0.02
