import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

def kmeans(X, k, n_iter=100, tol=1e-6, seed=0):
    rng = np.random.default_rng(seed)
    # k-means++ init
    C = [X[rng.integers(len(X))]]
    for _ in range(k - 1):
        d2 = np.min(((X[:, None] - np.array(C)[None]) ** 2).sum(-1), axis=1)
        C.append(X[rng.choice(len(X), p=d2 / d2.sum())])
    C = np.array(C)
    for _ in range(n_iter):
        d = ((X[:, None, :] - C[None, :, :]) ** 2).sum(-1)   # (n,k)
        labels = d.argmin(1)
        newC = C.copy()
        for j in range(k):
            pts = X[labels == j]
            if len(pts):
                newC[j] = pts.mean(0)
            else:                                            # empty cluster: re-seed at farthest point
                newC[j] = X[d.min(1).argmax()]
        shift = np.abs(newC - C).max(); C = newC
        if shift < tol: break
    inertia = ((X - C[labels]) ** 2).sum()
    return C, labels, inertia

X, _ = make_blobs(600, centers=4, cluster_std=0.8, random_state=1)
C, lab, inertia = kmeans(X, 4)
print("scratch inertia:", round(inertia, 1))
print("sklearn inertia:", round(KMeans(4, n_init=10, random_state=0).fit(X).inertia_, 1))
