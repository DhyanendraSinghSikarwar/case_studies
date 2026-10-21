#@@ q08
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score, adjusted_rand_score
X, _ = make_blobs(1000, centers=4, random_state=1)
a = KMeans(4, n_init=10, random_state=0).fit(X)
print("sil", round(silhouette_score(X, a.labels_), 3), "DB", round(davies_bouldin_score(X, a.labels_), 3),
      "CH", round(calinski_harabasz_score(X, a.labels_)))
# stability: refit on two bootstrap samples, compare labels on the full data
rng = np.random.default_rng(0)
labs = []
for _ in range(2):
    idx = rng.choice(len(X), len(X))
    labs.append(KMeans(4, n_init=10, random_state=0).fit(X[idx]).predict(X))
print("bootstrap ARI", round(adjusted_rand_score(*labs), 3))
#@@ q10
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score as ari
rng = np.random.default_rng(0)
grp = rng.integers(0, 2, 600)
orders = rng.normal(5 + 3 * grp, 1.5)              # informative, small scale
income = rng.normal(60000, 20000, 600)             # noise, huge scale
X = np.c_[orders, income]
raw = KMeans(2, n_init=10, random_state=0).fit_predict(X)
sc = KMeans(2, n_init=10, random_state=0).fit_predict(StandardScaler().fit_transform(X))
print("ARI vs true group  raw:", round(ari(grp, raw), 2), " scaled:", round(ari(grp, sc), 2))
#@@ q11
import numpy as np
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
X, y = load_digits(return_X_y=True)
p = PCA().fit(StandardScaler().fit_transform(X))
cum = p.explained_variance_ratio_.cumsum()
print("components for 90% / 95%:", (cum < .90).sum() + 1, (cum < .95).sum() + 1)
for k in (5, 15, 30, 45):
    pipe = make_pipeline(StandardScaler(), PCA(k), LogisticRegression(max_iter=2000))
    print(k, cross_val_score(pipe, X, y, cv=5).mean().round(3))
#@@ q12
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import average_precision_score
rng = np.random.default_rng(0)
Xn = rng.normal(0, 1, (5000, 5)); Xa = rng.normal(3, 1.5, (50, 5))
X = np.vstack([Xn, Xa]); y = np.r_[np.zeros(5000), np.ones(50)]
s = -IsolationForest(random_state=0).fit(X).score_samples(X)
print("PR-AUC", round(average_precision_score(y, s), 3), "base rate", round(y.mean(), 4))
thr = np.quantile(s, 0.99)               # alert on top 1% (review budget)
flag = s >= thr
print("flagged", flag.sum(), "precision", round(y[flag].mean(), 2), "recall", round(y[flag].sum() / y.sum(), 2))
#@@ q13
import numpy as np
from sklearn.datasets import make_blobs
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.metrics import adjusted_rand_score as ari
X, y = make_blobs(300, centers=3, random_state=0)
for m in ("single", "complete", "average", "ward"):
    Z = linkage(X, method=m)
    lab = fcluster(Z, t=3, criterion="maxclust")
    print(m, "ARI", round(ari(y, lab), 2))
print("last 3 ward merge heights:", Z[-3:, 2].round(1))   # big jump => natural cut
#@@ q14
import numpy as np
rng = np.random.default_rng(0)
for d in (2, 10, 100, 1000):
    X = rng.uniform(size=(1000, d))
    q = rng.uniform(size=d)
    dist = np.linalg.norm(X - q, axis=1)
    print(d, "max/min distance ratio:", round(dist.max() / dist.min(), 2))
#@@ q15
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score as ari
rng = np.random.default_rng(0)
A = rng.multivariate_normal([0, 0], [[4, 3.6], [3.6, 4]], 500)   # elongated, tilted
B = rng.multivariate_normal([4, -2], [[1, 0], [0, 1]], 500)
X = np.vstack([A, B]); y = np.r_[np.zeros(500), np.ones(500)]
g = GaussianMixture(2, covariance_type="full", n_init=5, random_state=0).fit(X)
km = KMeans(2, n_init=10, random_state=0).fit_predict(X)
print("GMM ARI", round(ari(y, g.predict(X)), 2), " KMeans ARI", round(ari(y, km), 2))
print("soft probs, 3 points:", g.predict_proba(X[[0, 600, 400]]).round(2).tolist())
#@@ q16
import numpy as np
from sklearn.datasets import make_blobs, make_moons
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, silhouette_samples
X, _ = make_blobs(500, centers=3, random_state=0)
lab = KMeans(3, n_init=10, random_state=0).fit_predict(X)
print("blobs sil", round(silhouette_score(X, lab), 3))
M, _ = make_moons(500, noise=0.06, random_state=0)
print("moons: kmeans sil", round(silhouette_score(M, KMeans(2, n_init=10, random_state=0).fit_predict(M)), 3),
      " DBSCAN (correct shape) sil", round(silhouette_score(M, DBSCAN(eps=0.15).fit_predict(M)), 3))
i = 0; d = np.linalg.norm(X - X[i], axis=1)          # one point by hand
a = d[lab == lab[i]].sum() / ((lab == lab[i]).sum() - 1)
b = min(d[lab == c].mean() for c in set(lab) if c != lab[i])
print("manual", round((b - a) / max(a, b), 4), "sklearn", round(silhouette_samples(X, lab)[i], 4))
#@@ q17
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
X, _ = make_blobs(2000, centers=10, cluster_std=0.8, random_state=3)
for init, n in (("random", 1), ("k-means++", 1), ("k-means++", 10)):
    sse = [KMeans(10, init=init, n_init=n, random_state=s).fit(X).inertia_ for s in range(20)]
    print(init, "n_init", n, "median/worst SSE:", round(np.median(sse)), round(max(sse)))
#@@ q18
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0)
dense = rng.normal(0, 0.3, (500, 2)); sparse = rng.normal(8, 3, (500, 2))
local_out = np.array([[1.5, 1.5], [-1.4, 1.2], [0.2, -1.6]])   # far from the dense blob, but not globally rare
X = np.vstack([dense, sparse, local_out]); y = np.r_[np.zeros(1000), np.ones(3)]
s_lof = -LocalOutlierFactor(n_neighbors=20).fit(X).negative_outlier_factor_
s_if = -IsolationForest(random_state=0).fit(X).score_samples(X)
print("AUC  LOF", round(roc_auc_score(y, s_lof), 3), " IsolationForest", round(roc_auc_score(y, s_if), 3))
#@@ q19
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0)
X = rng.normal(size=(3000, 3)) @ rng.normal(size=(3, 10)) + 0.05 * rng.normal(size=(3000, 10))  # normal: ~3-D structure
Xa = rng.normal(size=(60, 10)) * 2                      # anomalies break the structure
tr, val = X[:2000], X[2000:]
sc = StandardScaler().fit(tr)
ae = MLPRegressor(hidden_layer_sizes=(16, 3, 16), max_iter=800, random_state=0).fit(sc.transform(tr), sc.transform(tr))
err = lambda A: ((ae.predict(sc.transform(A)) - sc.transform(A)) ** 2).mean(1)   # per-row reconstruction error
thr = np.quantile(err(tr), 0.99)
y = np.r_[np.zeros(len(val)), np.ones(len(Xa))]
print("AUC", round(roc_auc_score(y, np.r_[err(val), err(Xa)]), 3), "| threshold", round(thr, 3),
      "| anomalies caught", (err(Xa) > thr).mean().round(2), "| false alarms", (err(val) > thr).mean().round(3))
#@@ q20
import numpy as np
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score as ari
X, y = load_digits(return_X_y=True)
a = KMeans(10, n_init=10, random_state=0).fit_predict(X)
b = KMeans(10, n_init=10, random_state=0).fit_predict(PCA(20, random_state=0).fit_transform(X))
print("ARI vs digit labels  full 64-d:", round(ari(y, a), 3), " PCA-20:", round(ari(y, b), 3))
#@@ q21
import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0)
z = rng.normal(size=(2000, 2)); X = z @ rng.normal(size=(2, 8)) + 0.1 * rng.normal(size=(2000, 8))
A1 = X[:20] + rng.normal(0, 1, (20, 8))                 # off-subspace anomalies (big residual)
tr, test_norm = X[200:], X[:200]
p = PCA(2).fit(tr)
# on-subspace but extreme: scale the top PC direction to 6 sigma
A2 = p.mean_ + 6 * np.sqrt(p.explained_variance_[0]) * p.components_[0] + 0.05 * rng.normal(size=(20, 8))
def scores(A):
    Z = p.transform(A)
    recon = ((A - p.inverse_transform(Z)) ** 2).sum(1)
    mahal = (Z ** 2 / p.explained_variance_).sum(1)     # Mahalanobis distance inside PC space
    return recon, mahal
nr, nm = scores(test_norm)
for name, A in (("off-subspace", A1), ("extreme-in-subspace", A2)):
    r, m = scores(A); y = np.r_[np.zeros(200), np.ones(20)]
    print(name, "AUC recon", round(roc_auc_score(y, np.r_[nr, r]), 2), " AUC mahal", round(roc_auc_score(y, np.r_[nm, m]), 2))
#@@ q22
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.manifold import TSNE, trustworthiness
from sklearn.metrics import silhouette_score
X, y = make_blobs(600, n_features=20, centers=4, cluster_std=3.0, random_state=0)
for perp in (2, 30, 150):
    E = TSNE(2, perplexity=perp, init="pca", random_state=0).fit_transform(X)
    print("perplexity", perp, "trustworthiness(k=10):", round(trustworthiness(X, E, n_neighbors=10), 3),
          " silhouette of true labels in 2D:", round(silhouette_score(E, y), 3))
