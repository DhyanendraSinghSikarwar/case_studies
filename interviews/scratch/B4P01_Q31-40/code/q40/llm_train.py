"""LLM-written training function (as pasted). It runs and prints a great number."""
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

def train(X, y, out_path):
    # keep the 20 most predictive features
    X = SelectKBest(f_classif, k=20).fit_transform(X, y)            # PROBLEM 1: selector sees ALL rows, incl. future test rows
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3)  # PROBLEM 2: no random_state, different split every run
    model = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
    try:
        joblib.dump(model, out_path)
    except Exception:                                               # PROBLEM 3: swallowed error, caller thinks it saved
        pass
    return model, model.score(X_te, y_te)

def make_data(seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(100, 2000))      # 100 rows, 2000 features, ALL pure noise
    y = rng.integers(0, 2, size=100)      # labels are coin flips: honest accuracy is about 0.5
    return X, y

if __name__ == "__main__":
    X, y = make_data()
    _, acc = train(X, y, "/no/such/dir/model.joblib")
    print(f"accuracy {acc:.2f}  <- reported (the labels are coin flips)")
