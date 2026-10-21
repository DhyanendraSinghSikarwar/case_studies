import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
X, _ = make_blobs(1000, centers=4, cluster_std=1.0, random_state=1)
for k in range(2, 8):
    km = KMeans(k, n_init=10, random_state=0).fit(X)
    print(k, round(km.inertia_), round(silhouette_score(X, km.labels_), 3))
