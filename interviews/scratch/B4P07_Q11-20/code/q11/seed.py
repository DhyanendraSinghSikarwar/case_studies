"""Seed a local sqlite registry with two versions of 'churn' (stand-in for the training job)."""
import sys, mlflow
from mlflow import MlflowClient
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression

uri = sys.argv[1]
mlflow.set_tracking_uri(uri)
mlflow.set_registry_uri(uri)
mlflow.set_experiment("churn-train")
X, y = make_classification(n_samples=200, n_features=5, random_state=0)
c = MlflowClient(uri)
for i, C in enumerate([0.1, 1.0], start=1):
    with mlflow.start_run():
        m = LogisticRegression(C=C, max_iter=200).fit(X, y)
        mlflow.sklearn.log_model(m, name="model", registered_model_name="churn")
# the gate marked version 2 as passed; version 1 was never gated
c.set_model_version_tag("churn", "2", "gate", "passed")
print("seeded", [(v.version, v.tags) for v in c.search_model_versions("name='churn'")])
