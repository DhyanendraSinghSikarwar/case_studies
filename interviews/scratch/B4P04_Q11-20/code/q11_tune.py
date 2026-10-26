# Q11: tuning loop, parent + child runs, search_runs, held-out test once
import warnings; warnings.filterwarnings("ignore")
import itertools, mlflow
from mlflow import MlflowClient
from sklearn.datasets import make_classification
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("tune-demo")
X, y = make_classification(n_samples=1500, n_features=20, n_informative=6, flip_y=0.1, random_state=0)
Xtv, Xte, ytv, yte = train_test_split(X, y, test_size=0.25, random_state=1)   # test: touch ONCE
Xtr, Xva, ytr, yva = train_test_split(Xtv, ytv, test_size=0.3, random_state=2) # same split for all runs
feature_sets = {"first5": list(range(5)), "first10": list(range(10)), "all20": list(range(20))}
lrs = [0.0001, 0.001, 0.01, 0.1, 1.0]
with mlflow.start_run(run_name="tuning-job") as parent:
    mlflow.set_tag("data_version", "synthetic-v1")
    for (fs, cols), lr in itertools.product(feature_sets.items(), lrs):
        with mlflow.start_run(run_name=f"{fs}-lr{lr}", nested=True):
            mlflow.set_tags({"data_version": "synthetic-v1", "metric_def": "val_auc"})
            mlflow.log_params({"lr": lr, "features": fs})
            m = SGDClassifier(loss="log_loss", learning_rate="constant", eta0=lr, random_state=0, max_iter=50)
            m.fit(Xtr[:, cols], ytr)
            mlflow.log_metric("val_auc", roc_auc_score(yva, m.decision_function(Xva[:, cols])))

exp = mlflow.get_experiment_by_name("tune-demo")
pid = parent.info.run_id
df = mlflow.search_runs([exp.experiment_id],
        filter_string=f"tags.mlflow.parentRunId = '{pid}' and tags.data_version = 'synthetic-v1' and metrics.val_auc > 0.5",
        order_by=["metrics.val_auc DESC"], max_results=3)
print(df[["tags.mlflow.runName", "params.lr", "params.features", "metrics.val_auc"]].to_string(index=False))

kids = MlflowClient().search_runs([exp.experiment_id], f"tags.mlflow.parentRunId = '{pid}'",
                                  order_by=["metrics.val_auc DESC"])
best = kids[0]
print("child runs:", len(kids))
print("best params:", best.data.params, "val_auc=%.4f" % best.data.metrics["val_auc"])
cols = feature_sets[best.data.params["features"]]
m = SGDClassifier(loss="log_loss", learning_rate="constant", eta0=float(best.data.params["lr"]), random_state=0, max_iter=50).fit(Xtr[:, cols], ytr)
print("test_auc (used once) = %.4f" % roc_auc_score(yte, m.decision_function(Xte[:, cols])))
