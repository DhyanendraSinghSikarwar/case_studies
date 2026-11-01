# Q6: mean-fill in training (48,000) vs zero-fill in serving. Illustrative; seeded.
import math
import numpy as np

# prompt arithmetic + sampling uncertainty of "6% null"
n_live, n_null = 5000, 300
assert n_null / n_live == 0.06
p = n_null / n_live
z = 1.96
wilson_lo = (p + z*z/(2*n_live) - z*math.sqrt(p*(1-p)/n_live + z*z/(4*n_live**2))) / (1 + z*z/n_live)
wilson_hi = (p + z*z/(2*n_live) + z*math.sqrt(p*(1-p)/n_live + z*z/(4*n_live**2))) / (1 + z*z/n_live)
print(f"null share in sample = {p:.1%}; 95% Wilson interval = [{wilson_lo:.1%}, {wilson_hi:.1%}]  (a sample, not the whole traffic)")
assert 0.053 < wilson_lo < 0.054 and 0.066 < wilson_hi < 0.067

# toy model: default risk falls with income. Train WITH mean fill (48,000).
rng = np.random.default_rng(66)
def make(m):
    income = rng.lognormal(math.log(42_000), 0.45, m)
    x2 = rng.normal(size=m)
    logit = -1.2 - 1.0 * (income - 48_000) / 20_000 + 0.6 * x2
    y = (rng.random(m) < 1 / (1 + np.exp(-logit))).astype(float)
    return income, x2, y
inc, x2, y = make(100_000)
is_null = rng.random(100_000) < 0.06
mean_income = inc[~is_null].mean()
print("training mean of non-null income:", round(mean_income))
assert 45_000 < mean_income < 51_000                  # about 48,000 as in the prompt (this toy uses its own draw)
FILL = 48_000                                         # the prompt's value; use it for both sides of the comparison
inc_tr = np.where(is_null, FILL, inc)
def feats(income, x2): return np.column_stack([np.ones(len(income)), (income - FILL) / 20_000, x2])
D = feats(inc_tr, x2); w = np.zeros(3)
for _ in range(15):
    pr = 1 / (1 + np.exp(-D @ w)); w -= np.linalg.solve((D * (pr * (1 - pr))[:, None]).T @ D, D.T @ (pr - y))
print("fitted weights (bias, income, x2):", w.round(2))

# 5,000 live requests, 300 with null income. Score with both fills.
inc_l, x2_l, _ = make(n_live)
null_l = np.zeros(n_live, bool); null_l[rng.choice(n_live, n_null, replace=False)] = True
def score(fill_value):
    inc_f = np.where(null_l, fill_value, inc_l)
    return 1 / (1 + np.exp(-(feats(inc_f, x2_l) @ w)))
s_train_fill, s_zero_fill = score(48_000), score(0)
diff = s_zero_fill - s_train_fill
print(f"non-null rows changed: {int((np.abs(diff[~null_l]) > 0).sum())}; null rows mean score {s_train_fill[null_l].mean():.3f} (right fill) vs {s_zero_fill[null_l].mean():.3f} (zero fill)")
assert (np.abs(diff[~null_l]) == 0).all()
shift_null = diff[null_l].mean(); shift_all = diff.mean()
print(f"mean shift on null rows = {shift_null:+.3f}; mean shift over all 5,000 = {shift_all:+.4f}")
assert abs(shift_all - 0.06 * shift_null) < 1e-12 and shift_null > 0.2

# decisions flipped at an illustrative cut-off of 0.35 (decline above it)
thr = 0.35
flipped = ((s_train_fill > thr) != (s_zero_fill > thr))
print("null rows whose decision flips:", int(flipped.sum()), "of", n_null, "| as share of all requests:", f"{flipped.sum()/n_live:.2%}")
assert flipped.sum() > 0.2 * n_null and flipped.sum() == int(flipped[null_l].sum())

# the control: a parity test that replays the SAME raw rows through the train path and the serve path
def train_impute(v): return FILL if v is None else v
def serve_impute(v): return 0 if v is None else v
raw = [None if k < n_null else 40_000 + k for k in range(n_live)]
mism = sum(train_impute(v) != serve_impute(v) for v in raw)
print("parity test mismatches:", mism)
assert mism == 300                                    # catches exactly the null rows, in CI, before any deploy

# and the fix: ONE shared function shipped inside the model artifact
def impute(v, fill=FILL): return fill if v is None else v
assert sum(impute(v) != impute(v) for v in raw) == 0
