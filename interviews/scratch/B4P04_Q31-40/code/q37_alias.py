import mlflow, warnings, sys
from mlflow.tracking import MlflowClient
from sklearn.dummy import DummyClassifier
mlflow.set_tracking_uri("sqlite:///reg.db"); c = MlflowClient()
m = DummyClassifier(strategy="constant", constant=1).fit([[0], [1]], [0, 1])
with mlflow.start_run(): mlflow.sklearn.log_model(m, name="model", registered_model_name="clf")
print("--- old way: stages")
try:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        c.transition_model_version_stage("clf", 1, "Production")
    print("stage call returned; warning:", str(w[0].message)[:150] if w else None)
except Exception as e: print("stage call failed:", type(e).__name__, str(e)[:150])
try:
    print("models:/clf/Production predicts", mlflow.pyfunc.load_model("models:/clf/Production").predict([[0]]))
except Exception as e: print("stage URI failed:", type(e).__name__, str(e).splitlines()[0][:200])
print("--- new way: alias")
c.set_registered_model_alias("clf", "champion", 1)
print("models:/clf@champion predicts", mlflow.pyfunc.load_model("models:/clf@champion").predict([[0]]))
print("alias lookup ->", c.get_model_version_by_alias("clf", "champion").version)
