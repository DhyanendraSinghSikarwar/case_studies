from sklearn.datasets import make_moons
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import adjusted_rand_score as ari
X, y = make_moons(500, noise=0.06, random_state=0)
print("kmeans ARI", round(ari(y, KMeans(2, n_init=10, random_state=0).fit_predict(X)), 2))
print("dbscan ARI", round(ari(y, DBSCAN(eps=0.15, min_samples=5).fit_predict(X)), 2))
