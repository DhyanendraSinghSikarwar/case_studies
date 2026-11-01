import numpy as np
from scipy.stats import beta

# --- 1) the arithmetic in the prompt
N, flagged, sampled, bad = 28_000, 700, 100, 62
prec = bad / sampled
lo, hi = beta.ppf(0.025, bad, sampled - bad + 1), beta.ppf(0.975, bad + 1, sampled - bad)
print("flag precision:", prec, " 95% CI", round(lo, 3), "-", round(hi, 3))
est_bad_flagged = flagged * prec
print("mislabelled rows among the 700 flagged:", est_bad_flagged, " (CI", round(flagged * lo), "-", round(flagged * hi), ")")
print("lower bound on noise rate from flagged rows alone:", round(est_bad_flagged / N, 4))
assert est_bad_flagged == 434.0 and round(est_bad_flagged / N, 4) == 0.0155
# unflagged rows must be audited too: invented audit of 300 random unflagged rows, 9 mislabelled
unflagged = N - flagged
u_bad, u_n = 9, 300
total_bad = est_bad_flagged + unflagged * u_bad / u_n
print("with an audit of unflagged rows (9 of 300): total noise rate", round(total_bad / N, 4))
assert round(total_bad / N, 3) == round((434 + 27_300 * 0.03) / 28_000, 3)

# --- 2) simulation: why 'flagged at 0.95' misses most of the noise
rng = np.random.default_rng(34)
n = 28_000
X = rng.normal(size=(n, 3)); w_true = np.array([1.5, -1.0, 0.5])
p = 1 / (1 + np.exp(-(X @ w_true)))
y_true = (rng.random(n) < p).astype(int)
flip = np.where(y_true == 1, rng.random(n) < 0.08, rng.random(n) < 0.03)      # asymmetric noise
y_obs = np.where(flip, 1 - y_true, y_true)
print("true noise rate:", round(float(flip.mean()), 4))

def fit(F, t, iters=20, l2=1e-3):
    b = np.zeros(F.shape[1]); w = np.ones(len(t))
    for _ in range(iters):
        q = 1 / (1 + np.exp(-F @ b)); g = F.T @ (w * (q - t)) + l2 * b
        H = (F * (w * q * (1 - q))[:, None]).T @ F + l2 * np.eye(len(b)); b -= np.linalg.solve(H, g)
    return b
F = np.hstack([X, np.ones((n, 1))])
fold = rng.permutation(n) % 5
prob = np.zeros(n)
for k in range(5):                                         # cross-validated probabilities: row never in its own fit
    b = fit(F[fold != k], y_obs[fold != k]); prob[fold == k] = 1 / (1 + np.exp(-F[fold == k] @ b))
conf_other = np.where(y_obs == 1, 1 - prob, prob)          # model's confidence in the OTHER class
flag = conf_other > 0.9
tp = int((flag & flip).sum())
print("flagged:", int(flag.sum()), " flag precision:", round(tp / flag.sum(), 3), " flag recall of the noisy rows:", round(tp / flip.sum(), 3))
assert tp / flip.sum() < 0.2          # most noisy rows are not flagged

# --- 3) drop vs relabel vs down-weight, scored on clean labels of a fresh test set
Xt = rng.normal(size=(20_000, 3)); yt = (rng.random(20_000) < 1 / (1 + np.exp(-(Xt @ w_true)))).astype(int)
Ft = np.hstack([Xt, np.ones((20_000, 1))])
def acc_of(b): return float((((Ft @ b) > 0).astype(int) == yt).mean())
b_all = fit(F, y_obs)
b_drop = fit(F[~flag], y_obs[~flag])
y_rel = np.where(flag, 1 - y_obs, y_obs); b_rel = fit(F, y_rel)
print("test accuracy  noisy:", round(acc_of(b_all), 4), " drop flagged:", round(acc_of(b_drop), 4), " relabel flagged:", round(acc_of(b_rel), 4))
clean_flagged = int((flag & ~flip).sum())
print("clean rows lost by dropping:", clean_flagged, "  clean rows corrupted by relabelling:", clean_flagged)
