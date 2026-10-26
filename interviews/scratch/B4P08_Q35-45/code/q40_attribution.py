import numpy as np
from scipy.stats import ks_2samp
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(40)
n = 6000
def X(n): return rng.normal(0, 1, (n, 3))          # f0, f1, f2: marginals never change
def y_old(x): return (x[:, 0] + 0.2 * x[:, 2] + rng.normal(0, 0.5, len(x)) > 0).astype(int)  # f0 drives the label
def y_new(x): return (x[:, 1] + 0.2 * x[:, 2] + rng.normal(0, 0.5, len(x)) > 0).astype(int)  # concept change: f1 drives it now
Xtr, Xref, Xcur = X(n), X(n), X(n)
ytr, yref, ycur = y_old(Xtr), y_old(Xref), y_new(Xcur)
m = GradientBoostingClassifier(random_state=0).fit(Xtr, ytr)
print("AUC reference window: %.3f   AUC current window: %.3f" % (roc_auc_score(yref, m.predict_proba(Xref)[:, 1]), roc_auc_score(ycur, m.predict_proba(Xcur)[:, 1])))
print("per-feature KS p-values ref vs cur:", [round(float(ks_2samp(Xref[:, j], Xcur[:, j]).pvalue), 2) for j in range(3)], "(all quiet)")
def perm(Xw, yw):
    return permutation_importance(m, Xw, yw, scoring="roc_auc", n_repeats=5, random_state=0).importances_mean
pr, pc = perm(Xref, yref), perm(Xcur, ycur)
print("perm importance (AUC drop) ref:", np.round(pr, 3), " cur:", np.round(pc, 3))
print("importance change cur-ref     :", np.round(pc - pr, 3))
# Mean |contribution| of the model's own scores per feature is label-free; show prediction distribution stays put
print("mean predicted prob ref %.3f cur %.3f (score drift quiet too)" % (m.predict_proba(Xref)[:, 1].mean(), m.predict_proba(Xcur)[:, 1].mean()))
