import numpy as np
from sklearn.linear_model import LogisticRegression
rng = np.random.default_rng(20)
def make(n, prev, shift=0.0):
    y = (rng.random(n) < prev).astype(int)
    x = rng.normal(0, 1, (n, 2)) + 1.5 * y[:, None] + shift * y[:, None]
    return x, y
xt, yt = make(20000, 0.05)                    # training prevalence 5%
xv, yv = make(20000, 0.05)                    # validation, same prevalence
clf = LogisticRegression(class_weight=None).fit(xt, yt)
thr = 0.5
# confusion rates on validation: TPR = P(pred=1|y=1), FPR = P(pred=1|y=0)
pv = clf.predict_proba(xv)[:, 1] >= thr
tpr, fpr = pv[yv == 1].mean(), pv[yv == 0].mean()
# live: prevalence 12%, no labels
xl, yl = make(20000, 0.12)
pl = clf.predict_proba(xl)[:, 1] >= thr
q = pl.mean()                                  # live positive rate
# q = pi*TPR + (1-pi)*FPR  ->  pi = (q - FPR)/(TPR - FPR)
pi_hat = (q - fpr) / (tpr - fpr)
print(f"validation positive rate {pv.mean():.3f}")
print(f"validation TPR {tpr:.3f} FPR {fpr:.3f}")
print(f"live positive rate {q:.3f} | true live prevalence {yl.mean():.3f} | estimated {pi_hat:.3f}")
# threshold correction: Bayes rule with new prior, posterior odds scale by (pi_new/(1-pi_new)) / (pi_old/(1-pi_old))
old, new = 0.05, pi_hat
p = clf.predict_proba(xl)[:, 1]
odds = p / (1 - p) * (new / (1 - new)) / (old / (1 - old))
p_adj = odds / (1 + odds)
print(f"mean score before {p.mean():.3f} after prior correction {p_adj.mean():.3f} (true prevalence {yl.mean():.3f})")
# if we want the same cost trade-off as before, the old 0.5 threshold on adjusted probabilities
print(f"positives flagged at 0.5: raw {np.mean(p >= .5):.3f}, adjusted {np.mean(p_adj >= .5):.3f}")
# where it breaks: P(x|y) also changes (covariate shift inside the positive class)
xs, ys = make(20000, 0.12, shift=-0.8)         # positives look weaker now
qs = (clf.predict_proba(xs)[:, 1] >= thr).mean()
print(f"BROKEN case: true prevalence {ys.mean():.3f}, estimate {(qs - fpr) / (tpr - fpr):.3f}  (P(x|y) moved, method assumes it did not)")
