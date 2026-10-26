import mlflow, pandas as pd
from mlflow.models import infer_signature
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
mlflow.set_tracking_uri("sqlite:///mlflow.db")
X, y = load_iris(return_X_y=True, as_frame=True)
m = LogisticRegression(max_iter=200).fit(X, y)
with mlflow.start_run():
    mlflow.sklearn.log_model(m, name="model", signature=infer_signature(X, m.predict(X)), registered_model_name="iris_clf")
mlflow.MlflowClient().set_registered_model_alias("iris_clf", "champion", 1)
X.head(2).to_json("in_split.json", orient="split", index=False)
print("registered iris_clf v1, alias champion")
