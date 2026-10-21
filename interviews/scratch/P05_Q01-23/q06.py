import numpy as np
from sklearn.datasets import make_moons
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
X, _ = make_moons(500, noise=0.06, random_state=0)
k = 5
d = np.sort(NearestNeighbors(n_neighbors=k).fit(X).kneighbors(X)[0][:, -1])  # k-distance (includes self)
print("k-dist percentiles 50/90/95/99:", np.percentile(d, [50, 90, 95, 99]).round(3))
lab = DBSCAN(eps=0.12, min_samples=k).fit_predict(X)
print("clusters", len(set(lab)) - (-1 in lab), "noise", (lab == -1).sum())
