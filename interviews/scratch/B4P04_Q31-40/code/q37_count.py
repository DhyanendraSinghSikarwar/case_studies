import mlflow, sys
mlflow.set_tracking_uri(sys.argv[1])
df = mlflow.search_runs(experiment_names=["legacy-exp"], order_by=["metrics.acc"])
print(sys.argv[1], "runs:", len(df), "acc:", list(df["metrics.acc"]), "depth:", list(df["params.depth"]))
print("artifact uri of first run:", df["artifact_uri"].iloc[0].replace(sys.argv[2], "<CWD>"))
