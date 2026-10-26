import json, numpy as np
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(36)
N = 5000
y = (rng.random(N) < 0.3).astype(int)
shared = rng.normal(size=N)            # row difficulty both models see
own_new = rng.normal(size=N)           # what only the NEW model's changed feature adds

def make(strength, own_weight):
    return strength * y + shared + own_weight * own_new

def tune(target, own_weight):
    lo, hi = 0.05, 4.0
    for _ in range(50):
        mid = (lo + hi) / 2
        if roc_auc_score(y, make(mid, own_weight)) < target: lo = mid
        else: hi = mid
    return mid

base  = make(tune(0.874, 0.0), 0.0)
small = make(tune(0.869, 0.8), 0.8)    # changed feature adds its own noise -> models only partly correlated
real  = make(tune(0.845, 0.3), 0.3)

baseline = {"metric": "roc_auc", "auc": round(float(roc_auc_score(y, base)), 3), "n_rows": N, "allowed_drop": 0.01}
json.dump(baseline, open("baseline.json", "w"))   # in CI: committed file, changed only through a reviewed PR
print("baseline.json:", baseline)

def gate(new, name, reps=2000, margin=baseline["allowed_drop"]):
    r = np.random.default_rng(1)
    diffs = np.empty(reps)
    for b in range(reps):
        i = r.integers(0, N, N)        # the SAME resampled rows for both models = paired bootstrap
        diffs[b] = roc_auc_score(y[i], new[i]) - roc_auc_score(y[i], base[i])
    d = roc_auc_score(y, new) - roc_auc_score(y, base)
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    if lo > -margin and d > -margin:   verdict, why = "PASS", f"drop is not provably worse than {margin}"
    elif hi < 0 and lo < -margin:      verdict, why = "FAIL", f"drop plausibly bigger than {margin}"
    else:                              verdict, why = "WARN", "drop not shown to exceed margin; flag for review"
    zero = "includes 0" if lo <= 0 <= hi else "excludes 0"
    print(f"{name:11} AUC {roc_auc_score(y,new):.3f} vs {roc_auc_score(y,base):.3f} delta {d:+.4f}  95% CI [{lo:+.4f}, {hi:+.4f}] ({zero})  -> {verdict}: {why}")
gate(small, "small drop")
gate(real,  "real drop")
print("Pearson corr of scores, base vs small:", round(float(np.corrcoef(base, small)[0,1]), 3), " base vs real:", round(float(np.corrcoef(base, real)[0,1]), 3))
