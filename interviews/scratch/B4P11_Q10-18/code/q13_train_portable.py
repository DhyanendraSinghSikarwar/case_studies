"""Same training script, tracking target chosen by env var. Only the local sqlite target is actually exercised."""
import os, sys, tempfile, warnings
warnings.filterwarnings("ignore")
os.environ.setdefault("MLFLOW_DISABLE_TELEMETRY", "true")
import mlflow

def train(lr):                      # stand-in for real training
    return {"auc": round(0.80 + 0.5 * lr, 3), "loss": round(0.4 - lr, 3)}

def main():
    uri = os.environ["MLFLOW_TRACKING_URI"]      # never hard-code; CI/job injects it
    mlflow.set_tracking_uri(uri)
    print("mlflow", mlflow.__version__, "| tracking uri scheme:", uri.split(":", 1)[0])
    if uri.startswith("azureml"):
        print("azureml URI accepted by the client; NO experiment/run call made (would reach management.azure.com)")
        return
    mlflow.set_experiment("churn-demo")
    with mlflow.start_run(run_name="lr-0.1") as r:
        mlflow.log_param("lr", 0.1)
        for k, v in train(0.1).items():
            mlflow.log_metric(k, v)
        mlflow.set_tag("git_sha", "abc1234")
    run = mlflow.get_run(r.info.run_id)
    print("params:", run.data.params, "| metrics:", run.data.metrics, "| tags(git_sha):", run.data.tags["git_sha"])

if __name__ == "__main__":
    main()
