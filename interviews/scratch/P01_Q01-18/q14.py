import numpy as np
rng = np.random.default_rng(0)
n = 2000
X = np.c_[np.ones(n), rng.normal(size=(n, 2))]
y = X @ np.array([1., 2., -3.]) + rng.normal(0, .5, n)
def run(bs, lr, epochs=20):
    w = np.zeros(3)
    for _ in range(epochs):
        idx = rng.permutation(n)
        for i in range(0, n, bs):
            b = idx[i:i+bs]
            w -= lr * 2 / len(b) * X[b].T @ (X[b] @ w - y[b])
    return w
for name, bs, lr in [("batch", n, .1), ("SGD", 1, .005), ("mini-32", 32, .05)]:
    w = run(bs, lr); print(name, np.round(w, 2), "mse=%.3f" % np.mean((X@w-y)**2))
print("lr too high:", np.round(run(32, 1.5, 3), 2))
