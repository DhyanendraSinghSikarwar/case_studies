import json, os, subprocess, yaml, hashlib, pandas as pd, mlflow, joblib, wandb
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from mlflow.models import infer_signature
p = yaml.safe_load(open("params.yaml"))["train"]
df = pd.read_csv("data.csv"); X, y = df.drop(columns="y"), df["y"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=0)
m = LogisticRegression(C=p["C"], max_iter=p["max_iter"], random_state=p["seed"]).fit(Xtr, ytr)
acc = float(m.score(Xte, yte)); joblib.dump(m, "model.joblib")
json.dump({"accuracy": acc}, open("metrics.json", "w"))
git = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
dhash = hashlib.md5(open("data.csv", "rb").read()).hexdigest()
mlflow.set_tracking_uri("sqlite:///mlflow.db"); mlflow.set_experiment("lab/demo/clf")
with mlflow.start_run() as r:
    mlflow.set_tags({"git_sha": git, "data_hash": dhash, "owner": "me", "project": "demo"})
    mlflow.log_params(p); mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(m, name="model", signature=infer_signature(Xte, m.predict(Xte)), registered_model_name="demo-clf")
v = mlflow.tracking.MlflowClient().search_model_versions("name='demo-clf'")
latest = max(int(x.version) for x in v)
mlflow.tracking.MlflowClient().set_registered_model_alias("demo-clf", "candidate", latest)
w = wandb.init(project="lab", mode="offline", dir="wb", config=p); w.log({"accuracy": acc}); w.finish()
open("MODEL_CARD.md", "w").write(f"""# demo-clf model card (generated)
- Intended use: demo only. Not for real decisions.
- Training data: data.csv, md5 {dhash} (synthetic, make_classification)
- Code: git {git}; params: {p}
- Metric: accuracy {acc:.4f} on a 25 percent hold-out (single split, no confidence interval)
- Registry: demo-clf version {latest}, alias 'candidate'
- Limits: synthetic data; no fairness or drift analysis done.
""")
