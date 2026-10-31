import os, shutil, sys, traceback, tempfile
import mlflow
from mlflow.tracking import MlflowClient
import warnings; warnings.filterwarnings("ignore")

def short(e): return f"{type(e).__name__}: {str(e).strip().splitlines()[0][:230]}"

print("=== CASE 6: the run goes somewhere you did not expect")
print("default tracking uri (MLFLOW_TRACKING_URI unset):", mlflow.get_tracking_uri().replace(os.getcwd(), "<cwd>"))
with mlflow.start_run(): mlflow.log_metric("m", 1)
print("files created in cwd:", sorted(os.listdir(".")))
mlflow.set_tracking_uri("file:./mlruns")
try:
    with mlflow.start_run(): mlflow.log_metric("m", 1)
except Exception as e: print("plain file store:", short(e))
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
with mlflow.start_run(): mlflow.log_metric("m", 1)
print("after opting in, ./mlruns exists:", os.path.isdir("mlruns"))
print("fix: set MLFLOW_TRACKING_URI (or set_tracking_uri) BEFORE the first run, and print mlflow.get_tracking_uri() in the log")

print("\n=== CASE 4: UI shows the run but the artifact is gone")
mlflow.set_tracking_uri("sqlite:///t.db")
art = os.path.abspath("art_root"); os.makedirs(art, exist_ok=True)
exp = mlflow.create_experiment("e4", artifact_location=art)
with mlflow.start_run(experiment_id=exp) as r:
    mlflow.log_metric("acc", 0.9); mlflow.log_text("hello", "notes.txt")
    rid = r.info.run_id
print("artifact uri :", mlflow.get_run(rid).info.artifact_uri)
print("list before  :", [f.path for f in MlflowClient().list_artifacts(rid)])
shutil.rmtree(art)                                    # bucket cleaned, disk moved, wrong mount ...
print("list after   :", [f.path for f in MlflowClient().list_artifacts(rid)])
print("metrics still:", mlflow.get_run(rid).data.metrics)
try: mlflow.artifacts.download_artifacts(run_id=rid, artifact_path="notes.txt", dst_path=tempfile.mkdtemp())
except Exception as e: print(short(e))

print("\n=== CASE 5: registering a model fails with a backend error")
from sklearn.dummy import DummyClassifier
m = DummyClassifier().fit([[0], [1]], [0, 1])
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
mlflow.set_tracking_uri("file:./fs_only")
try:
    with mlflow.start_run():
        mlflow.sklearn.log_model(m, name="model", registered_model_name="clf")
    print("file store registered OK (this version allows it)")
except Exception as e: print("file store:", short(e))
mlflow.set_tracking_uri("sqlite:////dev/null/x/mlflow.db")
try:
    with mlflow.start_run(): mlflow.sklearn.log_model(m, name="model", registered_model_name="clf")
except Exception as e: print("bad db path:", short(e))
mlflow.set_tracking_uri("http://127.0.0.1:9")
os.environ["MLFLOW_HTTP_REQUEST_MAX_RETRIES"] = "0"; os.environ["MLFLOW_HTTP_REQUEST_TIMEOUT"] = "3"
try: MlflowClient().create_registered_model("clf")
except Exception as e: print("server down:", short(e))
