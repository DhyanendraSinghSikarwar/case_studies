# 30 useless "models" (random scores): best validation AUC of 30 looks good, test AUC stays ~0.5
import numpy as np
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0)
yva, yte = rng.integers(0, 2, 200), rng.integers(0, 2, 200)
val = [roc_auc_score(yva, rng.normal(size=200)) for _ in range(30)]
best = int(np.argmax(val))
print("best of 30 val AUC: %.3f" % max(val))
print("same pick on fresh test AUC: %.3f" % roc_auc_score(yte, rng.normal(size=200)))
