import numpy as np, yaml, joblib
from sklearn.linear_model import LogisticRegression
p = yaml.safe_load(open("params.yaml"))["train"]
d = np.load("prepared.npz")
m = LogisticRegression(C=p["C"], max_iter=200).fit(d["Xtr"], d["ytr"])
joblib.dump(m, "model.joblib")
print("trained with C =", p["C"])
