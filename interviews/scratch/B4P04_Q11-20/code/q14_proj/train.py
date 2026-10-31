import json, subprocess, warnings, yaml
warnings.filterwarnings("ignore")
import mlflow, pandas as pd
from mlflow import MlflowClient
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

def sh(*a): return subprocess.run(a, capture_output=True, text=True).stdout.strip()

params = yaml.safe_load(open("params.yaml"))["train"]
df = pd.read_csv("data.csv")
data_md5 = yaml.safe_load(open("data.csv.dvc"))["outs"][0]["md5"]   # DVC hash of the input
sha, dirty = sh("git", "rev-parse", "HEAD"), bool(sh("git", "status", "--porcelain", "--", "train.py", "params.yaml", "data.csv.dvc"))

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("dvc-plus-mlflow")
with mlflow.start_run() as run:
    mlflow.set_tags({"git_sha": sha, "git_dirty": str(dirty), "dvc_data_md5": data_md5})
    mlflow.log_params(params)
    mlflow.log_input(mlflow.data.from_pandas(df, source="data.csv", name="train-data"), context="training")
    model = LogisticRegression(C=params["C"], max_iter=200)
    acc = cross_val_score(model, df[["x1", "x2"]], df["y"], cv=5).mean()
    mlflow.log_metric("cv_acc", acc)
    model.fit(df[["x1", "x2"]], df["y"])
    mlflow.sklearn.log_model(model, name="model", registered_model_name="churn")
    v = max(int(m.version) for m in MlflowClient().search_model_versions("name='churn'"))
    for k, val in {"git_sha": sha, "dvc_data_md5": data_md5}.items():
        MlflowClient().set_model_version_tag("churn", str(v), k, val)
json.dump({"cv_acc": round(acc, 4)}, open("metrics.json", "w"))
print("run", run.info.run_id, "-> churn v%d" % v)
