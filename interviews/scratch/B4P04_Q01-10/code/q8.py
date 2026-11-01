import warnings, mlflow, mlflow.sklearn, numpy as np
from mlflow import MlflowClient
from mlflow.models import infer_signature
from sklearn.linear_model import LogisticRegression

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("q8-registry")
X = np.array([[0.0], [1.0], [2.0], [3.0]]); y = np.array([0, 0, 1, 1])

def train(C):
    with mlflow.start_run():
        m = LogisticRegression(C=C).fit(X, y)
        mlflow.sklearn.log_model(m, name="model", signature=infer_signature(X, m.predict(X)),
                                 registered_model_name="clf")

train(0.01); train(100.0)          # creates version 1 and version 2
c = MlflowClient()
print("versions:", sorted(v.version for v in c.search_model_versions("name='clf'")))

c.set_registered_model_alias("clf", "champion", 1)
c.set_registered_model_alias("clf", "challenger", 2)
c.set_model_version_tag("clf", "2", "validated", "true")
def serve_once(label):
    m = mlflow.pyfunc.load_model("models:/clf@champion")      # serving code never changes
    print(label, "champion -> version", c.get_model_version_by_alias("clf", "champion").version,
          "| predict x=1.5:", m.predict(np.array([[1.5]])).tolist())
serve_once("before:")
c.set_registered_model_alias("clf", "champion", 2)             # promote
serve_once("promoted:")
c.set_registered_model_alias("clf", "champion", 1)             # rollback
serve_once("rolled back:")
print("aliases now:", {v: sorted(c.get_model_version("clf", v).aliases) for v in ("1", "2")})
print("tags on v2:", c.get_model_version("clf", "2").tags)

print("--- old stage API in this version")
try:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        c.transition_model_version_stage("clf", 2, "Production")
    print("transition_model_version_stage: worked; note:", str(w[0].message)[:110] if w else None)
except Exception as e:
    print("transition_model_version_stage:", type(e).__name__, str(e)[:120])
try:
    mlflow.pyfunc.load_model("models:/clf/Production")
    print("models:/clf/Production loaded")
except Exception as e:
    print("models:/clf/Production ->", type(e).__name__, str(e)[:140])
