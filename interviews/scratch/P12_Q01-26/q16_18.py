import numpy as np, pandas as pd, time
rng = np.random.default_rng(0)

print("=== Q16 ===")
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted, check_array
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import make_classification

class QuantileClipper(BaseEstimator, TransformerMixin):
    def __init__(self, lower=0.01, upper=0.99):
        self.lower = lower; self.upper = upper          # only store params, no logic
    def fit(self, X, y=None):
        X = check_array(X, dtype=float, ensure_all_finite=False)
        self.lo_ = np.nanquantile(X, self.lower, axis=0)  # learned from TRAIN only
        self.hi_ = np.nanquantile(X, self.upper, axis=0)
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self, X):
        check_is_fitted(self, ["lo_", "hi_"])
        X = check_array(X, dtype=float, ensure_all_finite=False)
        return np.clip(X, self.lo_, self.hi_)           # no refit, no mutation of input
    def get_feature_names_out(self, input_features=None):
        return np.asarray(input_features, dtype=object)

X, y = make_classification(500, 5, random_state=0)
X[::50, 0] *= 30                                         # outliers
pipe = make_pipeline(QuantileClipper(), LogisticRegression(max_iter=1000))
gs = GridSearchCV(pipe, {"quantileclipper__upper": [0.9, 0.99, 0.999],
                         "quantileclipper__lower": [0.001, 0.1]}, cv=3).fit(X, y)
print(gs.best_params_, round(gs.best_score_, 3))
t = QuantileClipper(0.05, 0.95).fit(X[:400])
print(t.lo_[:2].round(2), t.hi_[:2].round(2), t.transform(X[400:]).max(0)[:2].round(2))

print("=== Q17 ===")
n, d = 10_000, 50
Xtr = rng.normal(size=(n, d)); ytr = (Xtr[:, 0] > 0).astype(int)
Xq = rng.normal(size=(1000, d))
def sqdist(A, B):
    d2 = (A**2).sum(1)[:, None] - 2 * A @ B.T + (B**2).sum(1)[None, :]
    return np.maximum(d2, 0)                    # clip tiny negatives from rounding
t = time.perf_counter()
D = sqdist(Xq, Xtr)                             # (1000, 10000) float64 = 80 MB
k = 5
idx = np.argpartition(D, k, axis=1)[:, :k]      # O(n) per row, no full sort
pred = (ytr[idx].mean(1) > 0.5).astype(int)
print("time", round(time.perf_counter() - t, 3), "s; D MB:", D.nbytes / 1e6)
from sklearn.neighbors import KNeighborsClassifier
sk = KNeighborsClassifier(5, algorithm="brute").fit(Xtr, ytr).predict(Xq)
print("agree with sklearn:", (pred == sk).mean())
# naive broadcasting memory
print("naive (a-b) tensor for 1000x10000x50 float64 GB:", 1000 * 10000 * 50 * 8 / 1e9)
# numerical issue: large offset
A = rng.normal(size=(3, 3)) + 1e8
Dexp = sqdist(A, A)
Dtrue = ((A[:, None] - A[None]) ** 2).sum(-1)
print("offset 1e8 expansion diag (should be 0):", np.diag(Dexp), "off-diag rel err:", np.abs(Dexp - Dtrue).max() / Dtrue.max())
# chunking
def knn_chunked(Q, T, yT, k=5, bs=250):
    out = []
    for i in range(0, len(Q), bs):
        Dc = sqdist(Q[i:i + bs], T)
        out.append(np.argpartition(Dc, k, axis=1)[:, :k])
    return np.vstack(out)
print((knn_chunked(Xq, Xtr, ytr).shape))

print("=== Q18 ===")
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold, cross_val_score, KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
X, y = make_classification(300, 30, n_informative=3, flip_y=0.3, random_state=0)
pipe = make_pipeline(StandardScaler(), SVC())
grid = {"svc__C": [0.01, 0.1, 1, 10, 100], "svc__gamma": [1e-4, 1e-3, 1e-2, 0.1, 1]}
inner = StratifiedKFold(5, shuffle=True, random_state=1)
outer = StratifiedKFold(5, shuffle=True, random_state=2)
gs = GridSearchCV(pipe, grid, cv=inner, scoring="roc_auc")
gs.fit(X, y)
print("non-nested (best inner CV score):", round(gs.best_score_, 3), gs.best_params_)
nested = cross_val_score(gs, X, y, cv=outer, scoring="roc_auc")
print("nested outer scores:", nested.round(3), "mean", nested.mean().round(3))
