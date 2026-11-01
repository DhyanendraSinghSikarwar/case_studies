import mlflow, mlflow.sklearn, sklearn
from mlflow import MlflowClient
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split

print("mlflow", mlflow.__version__, "sklearn", sklearn.__version__)
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("q7-autolog")
mlflow.sklearn.autolog(log_models=False, log_datasets=False)   # autolog BEFORE fit

X, y = load_iris(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
c = MlflowClient()
exp = c.get_experiment_by_name("q7-autolog").experiment_id

with mlflow.start_run(run_name="single-fit") as r:
    m = LogisticRegression(C=0.5, max_iter=200).fit(Xtr, ytr)
    mlflow.log_metric("test_accuracy", m.score(Xte, yte))   # manual: autolog does not know the test set
run = c.get_run(r.info.run_id)
print("PARAMS (first 4):", dict(list(run.data.params.items())[:4]))
print("METRICS:", {k: round(v, 3) for k, v in run.data.metrics.items()})
print("TAGS (custom ones):", {k: v for k, v in run.data.tags.items() if not k.startswith("mlflow.log-model")and k.startswith(("estimator", "mlflow.runName"))})
print("artifacts:", [a.path for a in c.list_artifacts(r.info.run_id)])
print("git commit tag present:", "mlflow.source.git.commit" in run.data.tags, "(temp dir, not a git repo); data_version tag present:", "data_version" in run.data.tags)

# two fits in one run: the second overwrites the same param keys? -> error or new run?
with mlflow.start_run(run_name="two-fits") as r2:
    LogisticRegression(C=0.5, max_iter=200).fit(Xtr, ytr)
    LogisticRegression(C=5.0, max_iter=200).fit(Xtr, ytr)
print("two fits in one run, C kept:", c.get_run(r2.info.run_id).data.params["C"], "(still the first fit value)")

# GridSearchCV: child runs
gs = GridSearchCV(LogisticRegression(max_iter=200), {"C": [0.1, 1.0]}, cv=3)
with mlflow.start_run(run_name="grid-parent") as r3:
    gs.fit(Xtr, ytr)
runs = mlflow.search_runs(experiment_ids=[exp], output_format="list")
print("runs total:", len(runs))
kids = [x for x in runs if x.data.tags.get("mlflow.parentRunId") == r3.info.run_id]
print("child runs of grid-parent:", len(kids))
print("parent metrics:", {k: round(v, 3) for k, v in c.get_run(r3.info.run_id).data.metrics.items()})
print("parent artifacts:", [a.path for a in c.list_artifacts(r3.info.run_id)])
