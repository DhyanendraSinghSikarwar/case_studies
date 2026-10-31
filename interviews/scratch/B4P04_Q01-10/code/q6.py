import json, os, mlflow
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("q6-demo")
with mlflow.start_run(run_name="baseline") as run:
    mlflow.log_param("lr", 0.1)
    mlflow.log_params({"epochs": 3, "model": "logreg"})
    for step, loss in enumerate([0.9, 0.6, 0.45]):
        mlflow.log_metric("loss", loss, step=step)
    mlflow.log_metric("val_acc", 0.81)
    mlflow.set_tag("data_version", "v1")
    mlflow.log_text("hello from run\n", "notes/readme.txt")
    mlflow.log_dict({"classes": [0, 1]}, "meta.json")
    try:
        mlflow.log_param("lr", 0.5)
    except MlflowException as e:
        print("second log_param error:", str(e)[:150])
    run_id = run.info.run_id
    print("artifact_uri:", run.info.artifact_uri.replace(os.getcwd(), "<cwd>"))

c = MlflowClient()
r = c.get_run(run_id)
print("params:", r.data.params)
print("metrics (latest):", r.data.metrics)
print("tags data_version:", r.data.tags["data_version"])
print("loss history:", [(m.step, m.value) for m in c.get_metric_history(run_id, "loss")])
print("artifacts:", [a.path for a in c.list_artifacts(run_id)])
df = mlflow.search_runs(experiment_names=["q6-demo"], filter_string="params.model = 'logreg' and metrics.val_acc > 0.5")
print(df[["run_id", "status", "params.lr", "metrics.val_acc", "tags.data_version"]].assign(run_id=lambda d: d.run_id.str[:8]).to_string(index=False))
print("files:", sorted(f for f in os.listdir(".") if f.startswith("mlflow") or f in ("mlruns",)))
