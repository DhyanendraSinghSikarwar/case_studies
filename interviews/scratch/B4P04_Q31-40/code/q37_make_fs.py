import mlflow, os
mlflow.set_tracking_uri("file:./mlruns"); mlflow.set_experiment("legacy-exp")
for i, acc in enumerate([0.80, 0.85, 0.90]):
    with mlflow.start_run(run_name=f"r{i}"):
        mlflow.log_param("depth", i + 2); mlflow.log_metric("acc", acc); mlflow.log_text("x", "n.txt")
