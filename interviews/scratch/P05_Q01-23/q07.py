import numpy as np
from sklearn.ensemble import IsolationForest
rng = np.random.default_rng(0)
X = np.vstack([rng.normal(0, 1, (980, 2)), rng.uniform(-6, 6, (20, 2))])
y = np.r_[np.zeros(980), np.ones(20)]
m = IsolationForest(n_estimators=200, contamination=0.02, random_state=0).fit(X)
s = -m.score_samples(X)          # higher = more anomalous
top = np.argsort(-s)[:20]
print("precision@20:", y[top].mean())
print("mean score normal/anom:", s[y == 0].mean().round(3), s[y == 1].mean().round(3))
