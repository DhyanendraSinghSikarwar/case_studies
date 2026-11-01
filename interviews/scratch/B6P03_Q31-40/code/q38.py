import math
import numpy as np
from scipy.stats import beta

# 1) the audit arithmetic
audit, true_fraud, labelled = 2000, 25, 20
print("true fraud rate in audit:", true_fraud / audit, "  labelled fraud rate in audit:", labelled / audit)
sens = labelled / true_fraud
lo, hi = beta.ppf(0.025, labelled, true_fraud - labelled + 1), beta.ppf(0.975, labelled + 1, true_fraud - labelled)
print("label sensitivity P(label=fraud | fraud):", sens, " 95% CI", round(float(lo), 3), "-", round(float(hi), 3))
assert sens == 0.8 and true_fraud / audit == 0.0125 and labelled / audit == 0.01
# 2) simulate the consequences. Frauds come in two kinds: 'seen' (the old rules catch them, so they get labelled)
#    and 'hidden' (nobody notices them, so they are mostly unlabelled): noise is NOT random.
rng = np.random.default_rng(38)
n = 400_000
X = rng.normal(size=(n, 3))
fraud = rng.random(n) < 0.0125
hidden = fraud & (rng.random(n) < 0.25)
seen = fraud & ~hidden
X[seen, 0] += 2.5; X[seen, 1] += 1.0                  # seen frauds look like the old rules' targets
X[hidden, 2] += 2.5; X[hidden, 1] += 1.0              # hidden frauds look different
lab = np.where(seen, rng.random(n) < 0.96, np.where(hidden, rng.random(n) < 0.28, False))
print("true fraud rate:", round(float(fraud.mean()), 4), " labelled rate:", round(float(lab.mean()), 4), " label sensitivity:", round(float(lab[fraud].mean()), 3))
assert 0.76 < lab[fraud].mean() / 1 < 0.84
tr = np.arange(n) < 250_000; te = ~tr
def fit(F, t, iters=25, l2=1e-3):
    b = np.zeros(F.shape[1])
    for _ in range(iters):
        q = 1 / (1 + np.exp(-F @ b)); g = F.T @ (q - t) + l2 * b
        H = (F * (q * (1 - q))[:, None]).T @ F + l2 * np.eye(len(b)); b -= np.linalg.solve(H, g)
    return b
F = np.c_[X, X ** 2, np.ones(n)]
b = fit(F[tr], lab[tr].astype(float))
s = F[te] @ b
k = 600                                     # review capacity: flag the top 600 test rows
top = np.argsort(-s)[:k]
flag = np.zeros(te.sum(), bool); flag[top] = True
lab_te, fr_te = lab[te], fraud[te]
tp_lab = (flag & lab_te).sum(); tp_true = (flag & fr_te).sum()
print(f"flagged {k}: label-precision {tp_lab/k:.3f}  true-precision {tp_true/k:.3f}")
print(f"label-recall {tp_lab/lab_te.sum():.3f}  true-recall {tp_true/fr_te.sum():.3f}")
print("recall of hidden frauds:", round(float((flag & hidden[te]).sum() / hidden[te].sum()), 3), " recall of seen frauds:", round(float((flag & seen[te]).sum() / seen[te].sum()), 3))
assert tp_true / k > tp_lab / k                     # precision understated
assert tp_lab / lab_te.sum() > tp_true / fr_te.sum()  # recall overstated
# 3) correct the headline with the audit: recall_true = TP_true / fraud_total. Needs an audited estimate of how many are missed
# audit-based estimate on the test slice: investigate a random 2,000 of the test rows
aud = rng.choice(te.sum(), 2000, replace=False)
est_fraud_rate = fr_te[aud].mean(); est_sens = lab_te[aud][fr_te[aud]].mean() if fr_te[aud].any() else float('nan')
print("audit sample: true frauds", int(fr_te[aud].sum()), " labelled", int(lab_te[aud][fr_te[aud]].sum()), " est. sensitivity", round(float(est_sens), 2))
sens_flagged = tp_lab / tp_true
print("label sensitivity among frauds the model flagged:", round(float(sens_flagged), 3), " among all frauds:", round(float(lab_te[fr_te].mean()), 3))
assert sens_flagged > lab_te[fr_te].mean() + 0.1     # the model's catches are the easy-to-label ones, so one global factor misleads
