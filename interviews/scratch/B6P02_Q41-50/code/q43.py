# Q43: gaming of a published scorecard. Illustrative simulation.
import numpy as np
from scipy.optimize import minimize
from scipy.stats import rankdata
rng = np.random.default_rng(43)
n = 40_000
risk = rng.normal(size=n)                       # latent creditworthiness
default = rng.random(n) < 1/(1+np.exp(2.0 + 1.5*risk))   # higher risk value -> fewer defaults
# features: x_hard is costly to fake (repayment history), x_easy is cheap to fake (declared balance)
x_hard = risk + rng.normal(0, 1.0, n)
x_easy = risk + rng.normal(0, 0.5, n)
def feats(xh, xe): return np.column_stack([np.ones(len(xh)), xh, xe])

def fit(X, y):
    def nll(b):
        z = X@b
        return np.mean(np.logaddexp(0, z) - y*z)
    return minimize(nll, np.zeros(X.shape[1]), method="BFGS").x
def auc(score, y):   # AUC for predicting y=1
    r = rankdata(score); n1 = y.sum(); n0 = len(y)-n1
    return (r[y == 1].sum() - n1*(n1+1)/2)/(n1*n0)

b_full = fit(feats(x_hard, x_easy), default.astype(float))
b_hard = fit(feats(x_hard, np.zeros(n))[:, :2], default.astype(float))
print("weights full model (const, hard, easy):", np.round(b_full, 2))

# after publication: 60% of applicants inflate the easy feature (the model reads them as safer)
m = 40_000
risk2 = rng.normal(size=m)
d2 = rng.random(m) < 1/(1+np.exp(2.0 + 1.5*risk2))
xh2 = risk2 + rng.normal(0, 1.0, m)
xe2 = risk2 + rng.normal(0, 0.5, m)
gamers = rng.random(m) < 0.6
xe2_g = xe2 + gamers*rng.uniform(1.5, 3.5, m)    # inflation unrelated to true risk
before = auc(feats(x_hard, x_easy)@b_full, default.astype(int))
after = auc(feats(xh2, xe2_g)@b_full, d2.astype(int))
hard_only_after = auc(feats(xh2, xe2_g)[:, :2]@b_hard[:2], d2.astype(int))
hard_only_before = auc(feats(x_hard, x_easy)[:, :2]@b_hard[:2], default.astype(int))
print(f"full model AUC before {before:.3f} after gaming {after:.3f}")
print(f"hard-feature-only model AUC before {hard_only_before:.3f} after {hard_only_after:.3f}")
assert after < before - 0.03
assert hard_only_before < before        # robustness costs some power today
assert abs(hard_only_after - hard_only_before) < 0.01   # but it does not decay
assert hard_only_after > after            # and wins once gaming starts

# detection: the easy feature's distribution moves and its link to the outcome weakens
print(f"mean easy feature before {x_easy.mean():.2f}, after {xe2_g.mean():.2f}")
corr_b = np.corrcoef(x_easy, default)[0, 1]; corr_a = np.corrcoef(xe2_g, d2)[0, 1]
print(f"corr(easy, default) before {corr_b:.3f}, after {corr_a:.3f}")
assert xe2_g.mean() > x_easy.mean() + 0.5 and abs(corr_a) < abs(corr_b)
# gap between easy and hard features: gamers show easy >> hard
gap_b = (x_easy - x_hard).mean(); gap_a = (xe2_g - xh2).mean()
print(f"mean(easy - hard) before {gap_b:.2f}, after {gap_a:.2f}")
assert gap_a > gap_b + 0.5
