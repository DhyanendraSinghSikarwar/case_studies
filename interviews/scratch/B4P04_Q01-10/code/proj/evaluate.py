import json, numpy as np, joblib
from sklearn.metrics import accuracy_score, roc_curve, roc_auc_score
d = np.load("prepared.npz"); m = joblib.load("model.joblib")
s = m.predict_proba(d["Xte"])[:, 1]
json.dump({"accuracy": round(float(accuracy_score(d["yte"], s > .5)), 4),
           "auc": round(float(roc_auc_score(d["yte"], s)), 4)}, open("metrics.json", "w"), indent=2)
fpr, tpr, _ = roc_curve(d["yte"], s)
with open("roc.csv", "w") as f:
    f.write("fpr,tpr\n" + "".join(f"{a:.4f},{b:.4f}\n" for a, b in zip(fpr, tpr)))
print("evaluated")
