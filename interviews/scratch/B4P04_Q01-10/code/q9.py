import mlflow, mlflow.sklearn, pandas as pd
from mlflow.models import infer_signature
from sklearn.linear_model import LinearRegression

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("q9-signature")
train = pd.DataFrame({"age": [20, 30, 40, 50], "income": [1.0, 2.0, 3.0, 4.0]})   # age int64, income float64
y = [10.0, 20.0, 30.0, 40.0]
model = LinearRegression().fit(train, y)
sig = infer_signature(train, model.predict(train))
print("signature:", sig)

with mlflow.start_run():
    info = mlflow.sklearn.log_model(model, name="with_sig", signature=sig, input_example=train.head(2))
    info2 = mlflow.sklearn.log_model(model, name="no_sig")
print("no_sig model signature:", mlflow.models.get_model_info(info2.model_uri).signature)

m = mlflow.pyfunc.load_model(info.model_uri)
print("input schema:", m.metadata.get_input_schema())

def attempt(label, df):
    try:
        print(label, "->", m.predict(df).round(2).tolist())
    except Exception as e:
        print(label, "-> ERROR:", type(e).__name__, str(e).split("Error: ")[-1].replace("\n", " ")[:150])

attempt("exact types        ", pd.DataFrame({"age": [25], "income": [1.5]}))
attempt("age as float64     ", pd.DataFrame({"age": [25.0], "income": [1.5]}))   # float -> int is NOT safe
attempt("income as int64    ", pd.DataFrame({"age": [25], "income": [2]}))      # int64 -> float64 may lose precision
attempt("age int32 (widens) ", pd.DataFrame({"age": pd.array([25], dtype="int32"), "income": [1.5]}))
attempt("income int32       ", pd.DataFrame({"age": [25], "income": pd.array([2], dtype="int32")}))
attempt("income float32     ", pd.DataFrame({"age": [25], "income": pd.array([1.5], dtype="float32")}))
attempt("missing column     ", pd.DataFrame({"age": [25]}))
attempt("string value       ", pd.DataFrame({"age": ["old"], "income": [1.5]}))
attempt("extra column       ", pd.DataFrame({"age": [25], "income": [1.5], "zip": [1]}))
m2 = mlflow.pyfunc.load_model(info2.model_uri)
print("no-signature model, missing column ->", end=" ")
try: print(m2.predict(pd.DataFrame({"age": [25]})))
except Exception as e: print("ERROR:", type(e).__name__, str(e).replace("\n", " ")[:110])
