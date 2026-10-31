import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_auc_score
from scipy.stats import ks_2samp

rng = np.random.default_rng(35)
D, N = 32, 1000
def emb(n, shift=0.0):
    x = rng.normal(0, 1, (n, D))
    x[:, :4] += shift            # shift only 4 of 32 dims
    return x
ref = emb(N)
def centroid_dist(ref, cur):     # distance between mean vectors, scaled by ref spread
    return float(np.linalg.norm(cur.mean(0) - ref.mean(0)) / np.sqrt(D))
def domain_auc(ref, cur):
    X = np.vstack([ref, cur]); y = np.r_[np.zeros(len(ref)), np.ones(len(cur))]
    p = cross_val_predict(LogisticRegression(max_iter=500), X, y, cv=5, method="predict_proba")[:, 1]
    return float(roc_auc_score(y, p))
for name, shift in [("no shift", 0.0), ("small shift 0.3", 0.3), ("shift 1.0", 1.0)]:
    cur = emb(N, shift)
    print(f"{name:16s} centroid_dist={centroid_dist(ref,cur):.3f}  domain_AUC={domain_auc(ref,cur):.3f}")
# metadata drift: text length (tokens), same embeddings
len_ref = rng.poisson(40, N); len_cur = rng.poisson(55, N)
print("text length KS D=%.3f p=%.2g" % ks_2samp(len_ref, len_cur))
