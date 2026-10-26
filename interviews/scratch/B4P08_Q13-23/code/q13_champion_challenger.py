import numpy as np
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(13)
n = 5000
y = (rng.random(n) < 0.2).astype(int)
# both models see the same cases; part of their error is shared (common features), part is their own
shared = rng.normal(0, 1, n)
champ = shared + 1.0 * y + 0.8 * rng.normal(0, 1, n)
chall_small = shared + 1.1 * y + 0.8 * rng.normal(0, 1, n)   # small real gain
chall_noise = shared + 1.0 * y + 0.8 * rng.normal(0, 1, n)   # no real gain, different noise
def auc_diff(chall, idx):
    return roc_auc_score(y[idx], chall[idx]) - roc_auc_score(y[idx], champ[idx])
MIN_GAIN = 0.005   # business floor chosen by the team, an assumption here
B = 1000
print(f"AUC champion {roc_auc_score(y, champ):.4f}")
for name, chall in [("challenger_small_gain", chall_small), ("challenger_noise_only", chall_noise)]:
    obs = auc_diff(chall, np.arange(n))
    diffs = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n, n)          # paired: same resampled rows for both models
        diffs[b] = auc_diff(chall, idx)
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    if lo > 0 and obs >= MIN_GAIN:
        decision = "PROMOTE (CI above zero and gain above the floor)"
    elif hi < 0:
        decision = "REJECT (challenger is worse)"
    else:
        decision = "HOLD (CI includes zero or gain below floor; collect more labels)"
    print(f"{name}: AUC {roc_auc_score(y, chall):.4f} diff {obs:+.4f} 95% CI [{lo:+.4f}, {hi:+.4f}] -> {decision}")
