import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
import joblib

def train(X, y, out_path, seed=0):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=seed)   # split FIRST, seeded
    model = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression(max_iter=1000))  # selector fitted on train only
    model.fit(X_tr, y_tr)
    joblib.dump(model, out_path)         # let a failed save raise
    return model, model.score(X_te, y_te)

def make_data(seed=0):
    rng = np.random.default_rng(seed)
    return rng.normal(size=(100, 2000)), rng.integers(0, 2, size=100)
