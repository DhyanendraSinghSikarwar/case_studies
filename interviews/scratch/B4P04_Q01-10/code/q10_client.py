import os, re, sys, mlflow
from mlflow import MlflowClient
uri = sys.argv[1]
mlflow.set_tracking_uri(uri)
mlflow.set_experiment("q10")
with mlflow.start_run() as r:
    mlflow.log_param("where", uri.split(":")[0])
    mlflow.log_metric("m", 1.0)
    mlflow.log_text("hi\n", "a.txt")
    rid = r.info.run_id
c = MlflowClient()
print("ok: runs =", len(mlflow.search_runs(experiment_names=["q10"])), "| artifacts:", [a.path for a in c.list_artifacts(rid)])
u = c.get_run(rid).info.artifact_uri
print("artifact_uri:", re.sub(r"[0-9a-f]{32}", "<run_id>", u.replace(os.getcwd(), "<cwd>")))
