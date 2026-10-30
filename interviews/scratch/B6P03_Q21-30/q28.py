# Q28 400 rows, 40 positives: how noisy is 5-fold AUC? (illustrative; fixed scores isolate the evaluation noise)
import numpy as np
from scipy.stats import rankdata, norm
rng = np.random.default_rng(28)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
d = 1.0                              # binormal shift: AUC = Phi(d/sqrt(2))
true_auc = norm.cdf(d / np.sqrt(2))
print(f"true AUC of the scoring rule: {true_auc:.3f}")

def one_dataset():
    y = np.r_[np.ones(40, int), np.zeros(360, int)]
    s = rng.normal(size=400) + d * y
    return y, s
def stratified_folds(y):
    pos = rng.permutation(np.where(y == 1)[0]); neg = rng.permutation(np.where(y == 0)[0])
    return [np.r_[pos[k::5], neg[k::5]] for k in range(5)]

# Part 1: spread of the 5 fold AUCs on one dataset, repeated over many datasets
ranges = []; pooled = []
for _ in range(2000):
    y, s = one_dataset()
    f = [auc(y[i], s[i]) for i in stratified_folds(y)]
    ranges.append(max(f) - min(f)); pooled.append(auc(y, s))
ranges = np.array(ranges); pooled = np.array(pooled)
print(f"fold size 80 with 8 positives; median (max-min) of 5 fold AUCs {np.median(ranges):.2f}; share of datasets with a spread >= 0.29: {np.mean(ranges >= 0.29):.1%}")
print(f"pooled AUC over all 400 rows: mean {pooled.mean():.3f}, sd across datasets {pooled.std():.3f}")
assert np.median(ranges) > 0.18
assert 0.03 < pooled.std() < 0.05
# Part 2: repeating the CV many times removes split noise but not the noise of having 400 rows
y, s = one_dataset()
rep = [np.mean([auc(y[i], s[i]) for i in stratified_folds(y)]) for _ in range(50)]
print(f"one dataset, 50 repeats of 5-fold: mean-of-folds AUC varies only {np.std(rep):.4f}; pooled AUC {auc(y,s):.3f}")
# Part 3: bootstrap CI for the pooled AUC on that dataset
bs = []
for _ in range(2000):
    i = rng.integers(0, 400, 400)
    if y[i].sum() in (0, 400): continue
    bs.append(auc(y[i], s[i]))
lo, hi = np.percentile(bs, [2.5, 97.5])
print(f"bootstrap 95% CI for the pooled AUC: {lo:.2f} to {hi:.2f} (width {hi-lo:.2f})")
assert hi - lo > 0.1
assert np.std(rep) < 0.02
