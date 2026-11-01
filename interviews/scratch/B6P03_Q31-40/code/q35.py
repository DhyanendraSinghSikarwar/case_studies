import numpy as np
from scipy.stats import beta


# 12 classes, 100,000 tickets; sizes as in the prompt (invented split of the rest)
sizes = np.array([40000, 15000, 13000, 11000, 9000, 5000, 3500, 900, 800, 700, 600, 500])
assert sizes.sum() == 100_000 and sizes[0] / sizes.sum() == 0.40 and (sizes[7:] < 1000).all() and len(sizes) == 12
recall = np.array([0.945, 0.935, 0.925, 0.915, 0.905, 0.885, 0.83, 0.55, 0.50, 0.45, 0.40, 0.35])
rng = np.random.default_rng(35)
K = 12
C = np.zeros((K, K), int)                                   # confusion matrix: rows true, cols predicted
for i in range(K):
    C[i, i] = round(sizes[i] * recall[i])
    miss = sizes[i] - C[i, i]
    w = np.array([0.5 if j == 0 else 0.5 / (K - 2) for j in range(K)]); w[i] = 0
    w = w / w.sum()
    add = np.floor(miss * w).astype(int); add[0 if i else 1] += miss - add.sum()
    C[i] += add
    assert C[i].sum() == sizes[i]
tp = np.diag(C); support = C.sum(1); predicted = C.sum(0)
prec = tp / predicted; rec = tp / support; f1 = 2 * prec * rec / (prec + rec)
acc = tp.sum() / C.sum()
print("accuracy (= micro-F1):", round(float(acc), 4))
print("macro-F1 over all 12:", round(float(f1.mean()), 3), "  weighted-F1:", round(float((f1 * support).sum() / support.sum()), 3))
print("macro recall over the 5 rare classes:", round(float(rec[7:].mean()), 3), "  rare-class share of tickets:", round(support[7:].sum() / C.sum(), 3))
for i in range(K):
    print(f"class {i+1:2d} n={support[i]:6d} precision={prec[i]:.2f} recall={rec[i]:.2f} F1={f1[i]:.2f}")
assert abs(acc - 0.91) < 0.01
assert f1.mean() < acc - 0.05
# a 'predict the biggest class' baseline
print("baseline accuracy, always predict class 1:", sizes[0] / sizes.sum())
# rare classes: how well can recall be measured? Clopper-Pearson for class 12 if the test set holds 25% of it
n12 = int(support[11] * 0.25); k12 = round(n12 * rec[11])
lo, hi = beta.ppf(0.025, k12, n12 - k12 + 1), beta.ppf(0.975, k12 + 1, n12 - k12)
print(f"class 12 test positives {n12}, recall {k12/n12:.2f}, 95% CI {lo:.2f}-{hi:.2f}")
