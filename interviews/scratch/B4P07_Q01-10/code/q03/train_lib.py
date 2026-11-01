import numpy as np, joblib
from sklearn.datasets import make_classification
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import log_loss

def make_data(n, seed=0):
    return make_classification(n_samples=n, n_features=10, n_informative=5, random_state=seed)

def train(X, y, epochs, out_path):
    clf = SGDClassifier(loss="log_loss", random_state=0, learning_rate="constant", eta0=0.05)
    losses = []
    for _ in range(epochs):
        clf.partial_fit(X, y, classes=[0, 1])
        losses.append(log_loss(y, clf.predict_proba(X)))
    joblib.dump(clf, out_path)
    return losses
