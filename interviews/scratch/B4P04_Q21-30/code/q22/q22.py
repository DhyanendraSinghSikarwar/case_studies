# Q22: MLmodel file, flavors, and a custom pyfunc that bundles preprocessing + model.
import os, mlflow, mlflow.pyfunc, pandas as pd, numpy as np
from mlflow.models import infer_signature
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("flavors")
X, y = load_iris(return_X_y=True, as_frame=True)
sc = StandardScaler().fit(X)
clf = LogisticRegression(max_iter=200).fit(sc.transform(X), y)

class ScaledClf(mlflow.pyfunc.PythonModel):
    def load_context(self, context):                    # runs once at load; read bundled files here
        self.sc = joblib.load(context.artifacts["scaler"])
        self.clf = joblib.load(context.artifacts["clf"])
    def predict(self, context, model_input, params=None):
        return self.clf.predict(self.sc.transform(model_input))   # scaling can never be skipped

joblib.dump(sc, "scaler.pkl"); joblib.dump(clf, "clf.pkl")
sig = infer_signature(X.head(3), clf.predict(sc.transform(X.head(3))))
with mlflow.start_run() as run:
    info = mlflow.pyfunc.log_model(name="model", python_model=ScaledClf(),
                                   artifacts={"scaler": "scaler.pkl", "clf": "clf.pkl"},
                                   signature=sig, input_example=X.head(2),
                                   pip_requirements=["scikit-learn", "joblib"])
    mlflow.sklearn.log_model(clf, name="plain_sklearn", signature=sig)
    rid = run.info.run_id
local = mlflow.artifacts.download_artifacts(run_id=rid, artifact_path="model", dst_path="dl")
print("files in the pyfunc model folder:")
for root, _, fs in sorted(os.walk(local)):
    for f in sorted(fs):
        print("  ", os.path.relpath(os.path.join(root, f), local))
print("\n--- MLmodel (custom pyfunc), trimmed ---")
for line in open(os.path.join(local, "MLmodel")).read().splitlines():
    if not line.startswith(("artifact_path", "utc_time_created", "mlflow_version", "model_uuid", "model_id", "run_id")):
        print(line)
plain = mlflow.artifacts.download_artifacts(run_id=rid, artifact_path="plain_sklearn", dst_path="dl2")
print("\n--- flavors in the plain sklearn model ---")
import yaml
print(list(yaml.safe_load(open(os.path.join(plain, "MLmodel")))["flavors"]))

loaded = mlflow.pyfunc.load_model(f"runs:/{rid}/model")
raw = X.iloc[[0, 60, 120]]
print("\ncustom pyfunc on RAW (unscaled) rows:", loaded.predict(raw).tolist(), "| truth:", y.iloc[[0, 60, 120]].tolist())
print("plain sklearn pyfunc on the same raw rows:", mlflow.pyfunc.load_model(f"runs:/{rid}/plain_sklearn").predict(raw).tolist(), "(no scaler inside, so skew risk)")
