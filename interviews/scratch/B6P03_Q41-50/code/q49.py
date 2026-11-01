# Q49: patient-level folds for 1,200 patients x 6 scans, 25 positive patients. Illustrative.
import numpy as np
from math import sqrt
rng = np.random.default_rng(49)
P, SC, POS, K = 1_200, 6, 25, 5
assert P * SC == 7_200 and P // K == 240 and POS // K == 5
print(f"patients per fold {P//K}, scans per fold {P*SC//K}, positives per fold {POS//K}, prevalence {POS/P:.2%}")

pat_y = np.zeros(P, int); pat_y[rng.choice(P, POS, replace=False)] = 1
# patient-level stratified folds: deal positives and negatives round-robin after shuffling
fold = np.empty(P, int)
for cls in (1, 0):
    ids = rng.permutation(np.where(pat_y == cls)[0])
    fold[ids] = np.arange(len(ids)) % K
for k in range(K):
    m = fold == k
    assert m.sum() == 240 and pat_y[m].sum() == 5
print("every fold: 240 patients, 5 positive patients -> checked")

# Scans: each patient has a fixed 'signature' (no real disease signal at all) plus scan noise.
D = 20
sig = rng.normal(size=(P, D))
Xs = np.repeat(sig, SC, axis=0) + 0.3 * rng.normal(size=(P * SC, D))
pid = np.repeat(np.arange(P), SC); ys = pat_y[pid]

def nn_pred(tr, te):           # 1-nearest-neighbour in numpy
    A, B = Xs[tr], Xs[te]
    d = (B ** 2).sum(1)[:, None] - 2 * B @ A.T + (A ** 2).sum(1)[None]
    return ys[tr][d.argmin(1)]

def cv_recall(scan_fold):
    hit = tot = 0
    for k in range(K):
        te = np.where(scan_fold == k)[0]; tr = np.where(scan_fold != k)[0]
        p = nn_pred(tr, te); pos = ys[te] == 1
        hit += (p[pos] == 1).sum(); tot += pos.sum()
    return hit / tot
# (a) plain stratified split by scan label (leaks patients)
scan_fold = np.empty(P * SC, int)
for cls in (1, 0):
    ids = rng.permutation(np.where(ys == cls)[0]); scan_fold[ids] = np.arange(len(ids)) % K
# (b) split by patient
pat_scan_fold = fold[pid]
ra, rb = cv_recall(scan_fold), cv_recall(pat_scan_fold)
print(f"recall on positive scans, labels are pure patient noise: scan split {ra:.2f}, patient split {rb:.2f}")
assert ra > 0.9 and rb < 0.2
nf_scan = np.mean([len(set(scan_fold[pid == i])) for i in range(P)])
nf_pat = np.mean([len(set(pat_scan_fold[pid == i])) for i in range(P)])
print(f"average number of folds a patient appears in: scan split {nf_scan:.2f}, patient split {nf_pat:.2f}")
assert nf_scan > 3 and nf_pat == 1

# Uncertainty: 25 positive patients. Wilson interval for sensitivity 20/25 (illustrative result).
def wilson(x, n, z=1.96):
    p = x / n; c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h
lo, hi = wilson(20, 25)
print(f"sensitivity 20/25 = 0.80, Wilson 95% interval ({lo:.2f}, {hi:.2f})")
assert (round(lo, 2), round(hi, 2)) == (0.61, 0.91)
# the same 20/25 if the folds were evaluated one by one (5 positives each): per-fold values are just 0..5 / 5
print("per fold with 5 positives, one miss moves sensitivity by", 1 / 5)
# naive scan-level interval pretends 150 independent positive scans
lo2, hi2 = wilson(120, 150)
print(f"naive scan-level interval, 120/150: ({lo2:.2f}, {hi2:.2f})  -> too narrow, scans are not independent")
assert hi2 - lo2 < hi - lo
# patient bootstrap of the 25 positives
rng2 = np.random.default_rng(1)
res = np.array([1] * 20 + [0] * 5)
bs = [rng2.choice(res, 25).mean() for _ in range(5000)]
print("patient bootstrap 95%:", np.round(np.percentile(bs, [2.5, 97.5]), 2))
