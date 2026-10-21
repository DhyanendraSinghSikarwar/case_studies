import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
rng = np.random.default_rng(0)
z = rng.normal(size=(500, 2))
X = z @ rng.normal(size=(2, 6)) + 0.1 * rng.normal(size=(500, 6))   # 6 features, ~2 true dims
Xs = StandardScaler().fit_transform(X)
p = PCA().fit(Xs)
print(p.explained_variance_ratio_.round(3), p.explained_variance_ratio_.cumsum().round(3))
