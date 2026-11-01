# Q46: keep all conversions, 1% of non-conversions. Illustrative numbers + a scaled simulation.
import numpy as np
imps, conv, r = 50_000_000, 500, 0.01
neg = imps - conv
print(f"base rate: 1 in {imps/conv:,.0f}")
assert imps // conv == 100_000
kept_neg = neg * r
rate_s = conv / (conv + kept_neg)
print(f"kept rows: {conv + kept_neg:,.0f}, sampled positive rate = {rate_s:.6f} (about 1 in {1/rate_s:,.0f})")
assert 1000 < 1 / rate_s < 1002

# prior correction: p = r*ps / (1 - ps + r*ps)
def correct(ps, r): return r * ps / (1 - ps + r * ps)
print(f"sampled p 0.001 -> corrected {correct(0.001, r):.8f}")
assert abs(correct(rate_s, r) - conv / imps) / (conv / imps) < 1e-6      # recovers 1e-5 exactly
print(f"uncorrected / true inflation at base rate: {rate_s/(conv/imps):.2f}x")
assert round(rate_s / (conv / imps), 1) == 99.9

# variance of a log-odds estimate ~ 1/positives + 1/negatives
v_full = 1 / conv + 1 / neg; v_samp = 1 / conv + 1 / kept_neg
print(f"variance ratio sampled/full = {v_samp/v_full:.4f}")
assert 1.0 < v_samp / v_full < 1.01

# scaled simulation: 2,000,000 rows, one feature, logistic truth (invented)
rng = np.random.default_rng(46)
n = 2_000_000
x = rng.normal(size=n)
true_b0, true_b1 = -7.0, 1.0
p = 1 / (1 + np.exp(-(true_b0 + true_b1 * x)))
y = rng.random(n) < p
print(f"simulated positives: {y.sum()}  rate {y.mean():.5f}")
keep = y | (rng.random(n) < r)
xs, ys = x[keep], y[keep].astype(float)
print(f"kept {keep.sum()} rows")

def fit(X, t, w=None, iters=25):
    A = np.column_stack([np.ones(len(X)), X]); b = np.zeros(2)
    w = np.ones(len(t)) if w is None else w
    for _ in range(iters):
        q = 1 / (1 + np.exp(-A @ b))
        g = A.T @ (w * (q - t)); H = (A * (w * q * (1 - q))[:, None]).T @ A
        b -= np.linalg.solve(H, g)
    return b
b = fit(xs, ys)
print(f"fitted on sample: intercept {b[0]:.3f}, slope {b[1]:.3f}   (truth {true_b0}, {true_b1})")
shift = b[0] - true_b0
print(f"intercept shift = {shift:.3f}, -ln(r) = {-np.log(r):.3f}")
assert abs(b[1] - 1.0) < 0.1 and abs(shift - (-np.log(r))) < 0.5

# calibration on the FULL data: raw vs corrected vs inverse-weight evaluation
ps = 1 / (1 + np.exp(-(b[0] + b[1] * x)))
pc = correct(ps, r)
print(f"mean predicted: raw {ps.mean():.5f}  corrected {pc.mean():.5f}  actual {y.mean():.5f}")
assert ps.mean() > 50 * y.mean() and abs(pc.mean() / y.mean() - 1) < 0.15

# offline evaluation on the sampled rows with weights: negatives weigh 1/r = 100
wts = np.where(ys == 1, 1.0, 1 / r)
def wlogloss(pp, yy, ww): return -(ww * (yy * np.log(pp) + (1 - yy) * np.log(1 - pp))).sum() / ww.sum()
pc_s = correct(1 / (1 + np.exp(-(b[0] + b[1] * xs))), r)
ll_w = wlogloss(pc_s, ys, wts)
ll_full = wlogloss(pc, y.astype(float), np.ones(n))
print(f"weighted log loss on sample {ll_w:.5f} vs full-data log loss {ll_full:.5f}")
assert abs(ll_w - ll_full) / ll_full < 0.1
