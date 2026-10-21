import numpy as np
from sklearn.linear_model import Ridge, LinearRegression
rng = np.random.default_rng(0)
X = rng.normal(size=(50, 4)); X = np.c_[X, X[:, 0]]
y = 2*X[:, 0] + rng.normal(size=50); lam = 1.0
w = np.linalg.solve(X.T @ X + lam*np.eye(5), X.T @ y)
print(w.round(3), Ridge(alpha=lam, fit_intercept=False).fit(X, y).coef_.round(3), LinearRegression(fit_intercept=False).fit(X,y).coef_.round(3))
