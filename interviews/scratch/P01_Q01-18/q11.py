import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

def sigmoid(z):
    z = np.clip(z, -500, 500)               # avoid overflow in exp
    return 1 / (1 + np.exp(-z))

def fit_logreg(X, y, lr=0.1, epochs=1000, l2=0.0):
    Xb = np.c_[np.ones(len(X)), X]
    w = np.zeros(Xb.shape[1]); losses = []
    for _ in range(epochs):
        p = sigmoid(Xb @ w)
        grad = Xb.T @ (p - y) / len(y)
        grad[1:] += l2 * w[1:] / len(y)
        w -= lr * grad
        eps = 1e-12
        losses.append(-np.mean(y*np.log(p+eps) + (1-y)*np.log(1-p+eps)))
    return w, losses

X, y = make_classification(1000, 5, n_informative=4, n_redundant=0, class_sep=2.0, random_state=0)
X = StandardScaler().fit_transform(X)
for lr in [0.001, 0.1, 5, 500]:
    w, L = fit_logreg(X, y, lr=lr, epochs=300)
    print(f"lr={lr:<6} final loss={L[-1]:.4f}")
w, L = fit_logreg(X, y, lr=0.5, epochs=2000)
p = sigmoid(np.c_[np.ones(len(X)), X] @ w)
print("acc scratch:", ((p>.5)==y).mean().round(3))
sk = LogisticRegression(C=1e6, max_iter=1000).fit(X, y)
print("coef scratch:", np.round(w[1:],2)); print("coef sklearn:", np.round(sk.coef_[0],2))
