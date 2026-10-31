# q32_mlflow.py - same tracking + model-packaging script runs on any MLflow backend; here: local sqlite.
import os, sys, warnings; warnings.filterwarnings("ignore")
os.environ["MLFLOW_DISABLE_TELEMETRY"] = "true"; os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"
import logging; logging.disable(logging.CRITICAL)
import mlflow, mlflow.pyfunc
root = sys.argv[1]; os.makedirs(root, exist_ok=True)
mlflow.set_tracking_uri(f"sqlite:///{root}/ml.db")   # swap this one line for azureml://... or a Vertex-hosted server
mlflow.set_experiment("portable")
class Doubler(mlflow.pyfunc.PythonModel):
    def predict(self, context, model_input, params=None): return [x * 2 for x in model_input]
with mlflow.start_run() as r:
    mlflow.log_param("lr", 0.1); mlflow.log_metric("auc", 0.9)
    mlflow.pyfunc.save_model(path=f"{root}/model", python_model=Doubler())
run = mlflow.get_run(r.info.run_id)
print("mlflow", mlflow.__version__, "| tracking:", mlflow.get_tracking_uri().split(":")[0])
print("params:", run.data.params, "metrics:", run.data.metrics)
print("model dir:", sorted(os.listdir(f"{root}/model")))
print(open(f"{root}/model/MLmodel").read().split("\n")[0:4])
print("reload+predict:", mlflow.pyfunc.load_model(f"{root}/model").predict([1, 2, 3]))
