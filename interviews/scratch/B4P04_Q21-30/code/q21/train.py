import argparse, mlflow
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
p = argparse.ArgumentParser()
p.add_argument("--C", type=float, default=1.0)
p.add_argument("--max_iter", type=int, default=100)
a = p.parse_args()
X, y = load_iris(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
m = LogisticRegression(C=a.C, max_iter=a.max_iter).fit(Xtr, ytr)
with mlflow.start_run():          # under `mlflow run` this attaches to the run the CLI created
    mlflow.log_param("C", a.C)
    mlflow.log_param("max_iter", a.max_iter)
    mlflow.log_metric("test_acc", round(m.score(Xte, yte), 4))
