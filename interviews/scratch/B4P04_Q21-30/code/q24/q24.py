# Q24: artifact logging APIs, artifact_location fixed at experiment creation, download back.
import os, json, mlflow, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
mlflow.set_tracking_uri("sqlite:///mlflow.db")
exp_id = mlflow.create_experiment("art", artifact_location="file:///tmp/claude-0/b4q24_art_root")
exp = mlflow.get_experiment(exp_id)
print("artifact_location fixed at creation:", exp.artifact_location)
with mlflow.start_run(experiment_id=exp_id) as run:
    fig, ax = plt.subplots(); ax.plot([1, 2, 3], [1, 4, 9]); ax.set_title("demo")
    mlflow.log_figure(fig, "plots/curve.png")
    mlflow.log_dict({"lr": 0.1, "features": ["a", "b"]}, "cfg/config.json")
    mlflow.log_text("hello run", "notes/readme.txt")
    pd.DataFrame({"id": [1, 2], "pred": [0.2, 0.9]}).to_csv("preds.csv", index=False)
    mlflow.log_artifact("preds.csv", artifact_path="outputs")           # one file
    os.makedirs("many", exist_ok=True)
    for i in range(2): open(f"many/part{i}.txt", "w").write(str(i))
    mlflow.log_artifacts("many", artifact_path="shards")                 # a whole folder
    mlflow.log_table(pd.DataFrame({"q": ["a", "b"], "score": [1, 2]}), "tables/eval.json")
    print("run artifact_uri:", run.info.artifact_uri)
    rid = run.info.run_id
c = mlflow.MlflowClient()
def walk(p=None, ind=""):
    for f in c.list_artifacts(rid, p):
        print(ind + f.path + ("/" if f.is_dir else ""))
        if f.is_dir: walk(f.path, ind + "  ")
print("listing:"); walk()
d = mlflow.artifacts.download_artifacts(run_id=rid, artifact_path="cfg/config.json", dst_path="dl")
print("downloaded ->", os.path.relpath(d), json.load(open(d)))
d2 = mlflow.artifacts.download_artifacts(run_id=rid, artifact_path="outputs/preds.csv", dst_path="dl")
print("csv back:", pd.read_csv(d2).to_dict("list"))
print("text back:", mlflow.artifacts.load_text(f"runs:/{rid}/notes/readme.txt"))
