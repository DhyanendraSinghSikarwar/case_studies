import json, yaml
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
p = yaml.safe_load(open("params.yaml"))["train"]
X, y = make_classification(n_samples=120, n_features=40, n_informative=3, flip_y=0.15, random_state=0)
acc = cross_val_score(LogisticRegression(C=p["C"], max_iter=300), X, y, cv=5).mean()
json.dump({"cv_acc": round(float(acc), 4)}, open("metrics.json", "w"))
