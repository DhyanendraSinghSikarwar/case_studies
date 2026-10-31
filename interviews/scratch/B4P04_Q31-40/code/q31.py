import os, sys, platform, subprocess, hashlib, json
import numpy as np, sklearn, mlflow
from mlflow.tracking import MlflowClient
from scipy import stats
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# 1. tiny nondeterminism demos (no ML needed)
xs = [0.1] * 10 + [1e16, -1e16] + [0.1] * 10
print("float sum, order A :", sum(xs))
print("float sum, order B :", sum(sorted(xs)))
out = subprocess.run([sys.executable, "-I", "-c", "print(sorted({'a','b','c','d'}))\nprint(list({'a','b','c','d'}))"],
                     env={**os.environ, "PYTHONHASHSEED": "1"}, capture_output=True, text=True).stdout
out2 = subprocess.run([sys.executable, "-I", "-c", "print(list({'a','b','c','d'}))"],
                     env={**os.environ, "PYTHONHASHSEED": "2"}, capture_output=True, text=True).stdout
print("set order, hashseed=1:", out.splitlines()[1], "| hashseed=2:", out2.strip())

# 2. experiment
X, y = make_classification(n_samples=600, n_features=20, n_informative=5, flip_y=0.1, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)

def one(seed, n_jobs=1):
    m = RandomForestClassifier(n_estimators=30, max_depth=6, random_state=seed, n_jobs=n_jobs).fit(Xtr, ytr)
    return m.score(Xte, yte)

print("same seed twice:", one(1), one(1))
print("n_jobs 1 vs 4 same seed:", one(1, 1), one(1, 4))

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("q31-seeds")
env = {"python": platform.python_version(), "sklearn": sklearn.__version__, "numpy": np.__version__,
       "machine": platform.machine(), "os": platform.system(), "cpus": os.cpu_count()}
freeze = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True).stdout
fhash = hashlib.sha256(freeze.encode()).hexdigest()[:12]
dhash = hashlib.sha256(Xtr.tobytes() + ytr.tobytes()).hexdigest()[:12]

scores = {}
for cfg, seeds in {"A_seed_0_to_4": range(0, 5), "B_seed_10_to_14": range(10, 15)}.items():
    scores[cfg] = []
    for s in seeds:
        with mlflow.start_run(run_name=f"{cfg}-{s}"):
            mlflow.set_tags({"config": cfg, "data_hash": dhash, "freeze_hash": fhash})
            mlflow.log_params({"seed": s, "n_estimators": 30, "max_depth": 6, **env})
            mlflow.log_text(freeze, "pip_freeze.txt")
            acc = one(s)
            mlflow.log_metric("accuracy", acc)
            scores[cfg].append(acc)
for k, v in scores.items():
    print(f"{k}: mean={np.mean(v):.4f} std={np.std(v, ddof=1):.4f} min={min(v):.4f} max={max(v):.4f}")
a, b = np.array(scores["A_seed_0_to_4"]), np.array(scores["B_seed_10_to_14"])
print("mean gap A-B: %.4f" % (a.mean() - b.mean()))
t = stats.ttest_ind(a, b, equal_var=False)
print("Welch t-test p = %.3f" % t.pvalue)

df = mlflow.search_runs(experiment_names=["q31-seeds"], order_by=["metrics.accuracy DESC"])
print(df[["tags.config", "params.seed", "metrics.accuracy", "tags.data_hash", "tags.freeze_hash"]].to_string(index=False))
