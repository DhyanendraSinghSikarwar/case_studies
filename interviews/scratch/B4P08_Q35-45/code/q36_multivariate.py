import numpy as np
from scipy.stats import ks_2samp
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_auc_score
from sklearn.decomposition import PCA

rng = np.random.default_rng(36)
n = 2000
def make(rho):
    cov = [[1, rho], [rho, 1]]
    return rng.multivariate_normal([0, 0], cov, n)
ref, cur = make(0.8), make(-0.8)   # marginals identical N(0,1), correlation flips
for j in range(2):
    D, p = ks_2samp(ref[:, j], cur[:, j])
    print(f"per-feature KS x{j}: D={D:.3f} p={p:.2f}")
# domain classifier (non-linear, so it can see the correlation)
X = np.vstack([ref, cur]); y = np.r_[np.zeros(n), np.ones(n)]
pr = cross_val_predict(RandomForestClassifier(100, min_samples_leaf=20, random_state=0), X, y, cv=5, method="predict_proba")[:, 1]
print("domain classifier AUC: %.3f" % roc_auc_score(y, pr))
# correlation diff
c0, c1 = np.corrcoef(ref.T)[0, 1], np.corrcoef(cur.T)[0, 1]
print(f"corr ref={c0:.3f} cur={c1:.3f} abs diff={abs(c1-c0):.3f}")
# PCA reconstruction error: fit on ref, 1 component
pca = PCA(1).fit(ref)
def rec_err(x): return float(np.mean(np.sum((x - pca.inverse_transform(pca.transform(x)))**2, axis=1)))
print(f"PCA(1) recon error ref={rec_err(ref):.3f} cur={rec_err(cur):.3f}")
# control: no change at all
ref2, cur2 = make(0.8), make(0.8)
pr2 = cross_val_predict(RandomForestClassifier(100, min_samples_leaf=20, random_state=0), np.vstack([ref2, cur2]), y, cv=5, method="predict_proba")[:, 1]
print("control (no change) domain AUC: %.3f  corr diff %.3f  recon %.3f vs %.3f" % (
    roc_auc_score(y, pr2), abs(np.corrcoef(cur2.T)[0,1]-np.corrcoef(ref2.T)[0,1]), rec_err(ref2), rec_err(cur2)))
