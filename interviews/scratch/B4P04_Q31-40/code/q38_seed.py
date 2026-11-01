import mlflow, sys
mlflow.set_tracking_uri(sys.argv[1])
def run(exp, tags):
    mlflow.set_experiment(exp)
    with mlflow.start_run(): mlflow.set_tags(tags); mlflow.log_metric("auc", 0.9)
good = {"git_sha": "a1b2c3d", "data_hash": "0f9e8d7c6b5a", "owner": "asha", "project": "churn"}
run("risk/churn/baseline", good)
run("risk/churn/baseline", {k: v for k, v in good.items() if k != "data_hash"})
run("Quick Test", {**good, "git_sha": "latest"})
