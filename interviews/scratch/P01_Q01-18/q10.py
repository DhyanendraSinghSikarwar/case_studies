import numpy as np
rng = np.random.default_rng(0)
n, d = 500, 3
X = rng.normal(size=(n, d))
true_w, true_b = np.array([2.0, -1.0, 0.5]), 4.0
y = X @ true_w + true_b + rng.normal(0, 0.1, n)

def fit_normal_eq(X, y):
    Xb = np.c_[np.ones(len(X)), X]                    # add bias column
    return np.linalg.solve(Xb.T @ Xb, Xb.T @ y)       # solve, never inv()

def fit_gd(X, y, lr=0.1, epochs=500):
    Xb = np.c_[np.ones(len(X)), X]
    w = np.zeros(Xb.shape[1])
    for _ in range(epochs):
        grad = 2 / len(y) * Xb.T @ (Xb @ w - y)       # d(MSE)/dw
        w -= lr * grad
    return w

print("normal eq:", np.round(fit_normal_eq(X, y), 3))
print("grad desc:", np.round(fit_gd(X, y), 3))
