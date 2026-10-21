import numpy as np
from collections import Counter
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

class KNN:
    def __init__(self, k=5): self.k = k
    def fit(self, X, y): self.X, self.y = X, y; return self
    def predict(self, Q):
        d2 = (Q**2).sum(1)[:, None] - 2 * Q @ self.X.T + (self.X**2).sum(1)[None]
        idx = np.argpartition(d2, self.k, axis=1)[:, :self.k]       # O(n) per query, no full sort
        return np.array([Counter(self.y[r]).most_common(1)[0][0] for r in idx])

X, y = load_iris(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.3, random_state=0, stratify=y)
print("scratch:", (KNN(5).fit(Xtr, ytr).predict(Xte) == yte).mean().round(3))
print("sklearn:", KNeighborsClassifier(5).fit(Xtr, ytr).score(Xte, yte))
for k in [1, 5, 25, 90]:
    m = KNN(k).fit(Xtr, ytr)
    print(k, "train", (m.predict(Xtr)==ytr).mean().round(3), "test", (m.predict(Xte)==yte).mean().round(3))
