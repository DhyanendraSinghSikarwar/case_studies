import mlflow, sys
from mlflow.tracking import MlflowClient
mlflow.set_tracking_uri(sys.argv[1]); mlflow.set_experiment("team-demo")
with mlflow.start_run(run_name="via-server") as r:
    mlflow.log_param("owner", "dhyan"); mlflow.log_metric("acc", 0.91); mlflow.log_text("model card draft", "card.txt")
    print("run", r.info.run_id[:8], "artifact_uri:", r.info.artifact_uri.replace(sys.argv[2], "<ROOT>"))
c = MlflowClient()
print("runs via server API:", [(x.info.run_name, x.data.metrics) for x in c.search_runs([c.get_experiment_by_name("team-demo").experiment_id])])
print("artifacts:", [f.path for f in c.list_artifacts(r.info.run_id)])
