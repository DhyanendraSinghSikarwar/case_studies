import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

def kmeans(X, k, iters=100, seed=0):
    rng = np.random.default_rng(seed)
    C = X[rng.choice(len(X), k, replace=False)]
    for _ in range(iters):
        d = ((X[:, None, :] - C[None]) ** 2).sum(-1)   # n x k squared distances
        lab = d.argmin(1)                              # assignment step
        newC = np.array([X[lab == j].mean(0) if (lab == j).any() else C[j] for j in range(k)])
        if np.allclose(newC, C): break
        C = newC                                       # update step
    return lab, C, d.min(1).sum()

X, _ = make_blobs(600, centers=3, random_state=0)
lab, C, sse = kmeans(X, 3)
km = KMeans(3, n_init=10, random_state=0).fit(X)
print(round(sse, 1), round(km.inertia_, 1))
