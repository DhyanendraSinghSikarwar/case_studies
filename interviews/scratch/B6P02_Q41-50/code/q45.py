# Q45: LLM-as-judge drift/bias and calibration against human labels. Illustrative simulation.
import numpy as np
from scipy.stats import spearmanr, norm
rng = np.random.default_rng(45)
n = 100  # human spot check per month

# 1) the human check on its own: can 100 ratings see a +0.3 change?
sd = 0.9
se_diff = sd*np.sqrt(2/n)
print(f"SE of a difference of two 100-sample means (sd {sd}) = {se_diff:.3f}; 95% half-width {1.96*se_diff:.3f}")
assert abs(1.96*se_diff - 0.249) < 0.001
power = 1 - norm.cdf(1.96 - 0.3/se_diff) + norm.cdf(-1.96 - 0.3/se_diff)
print(f"power to detect a true +0.3 with 100 vs 100 humans = {power:.2f}")
assert 0.6 < power < 0.7

# 2) simulate: true quality unchanged, outputs got longer, judge likes length
def month(n_out, mean_len):
    quality = np.clip(rng.normal(3.9, 0.8, n_out), 1, 5)           # what humans would say
    length = rng.normal(mean_len, 25, n_out)                          # words
    judge = np.clip(quality + 0.3 + 0.01*(length - 150) + rng.normal(0, 0.4, n_out), 1, 5)
    return quality, length, judge
q1, l1, j1 = month(5000, 150)
q2, l2, j2 = month(5000, 180)      # prompt change made answers 30 words longer
print(f"judge mean {j1.mean():.2f} -> {j2.mean():.2f}; true quality {q1.mean():.2f} -> {q2.mean():.2f}")
assert j2.mean() - j1.mean() > 0.2 and abs(q2.mean() - q1.mean()) < 0.05

# 3) calibrate: on a labelled set from BOTH months, regress human on judge and length
idx1 = rng.choice(5000, 200, replace=False); idx2 = rng.choice(5000, 200, replace=False)
H = np.concatenate([q1[idx1], q2[idx2]]); J = np.concatenate([j1[idx1], j2[idx2]]); L = np.concatenate([l1[idx1], l2[idx2]])
rho = spearmanr(H, J)[0]
print(f"Spearman(human, judge) over labelled 400 = {rho:.2f}")
X = np.column_stack([np.ones(len(H)), J, L - 150])
beta = np.linalg.lstsq(X, H, rcond=None)[0]
print(f"human ~ a + b*judge + c*(length-150): b={beta[1]:.2f}, c={beta[2]:.4f} (negative c = judge over-rewards length)")
assert beta[2] < -0.003
corr_j = X@beta
adj1 = (np.column_stack([np.ones(5000), j1, l1-150])@beta).mean()
adj2 = (np.column_stack([np.ones(5000), j2, l2-150])@beta).mean()
print(f"length-adjusted judge: {adj1:.2f} -> {adj2:.2f} (change {adj2-adj1:+.2f}); human truth change {q2.mean()-q1.mean():+.2f}")
assert abs((adj2 - adj1) - (q2.mean() - q1.mean())) < 0.08
# agreement check by band: judge >= 4.5 vs human >= 4.5 (illustrative threshold)
hi_j = J >= 4.5
print(f"judge >=4.5 share {hi_j.mean():.2f}; of those humans also >=4.5: {(H[hi_j] >= 4.5).mean():.2f}")
