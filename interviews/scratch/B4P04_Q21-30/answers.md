# Book 4 Part 4, answers Q21-Q30 (Wave B agent output)

### Q21 ⭐⭐ 🟡 MLflow Projects and mlflow run. Explain the MLproject file (name, entry points, parameters with types and defaults, environment as conda, virtualenv or Docker), how mlflow run executes an entry point and logs it as a run with the source and git commit, and why many teams now prefer plain scripts, DVC or an orchestrator over MLflow Projects (hedge). Write an MLproject for a train.py with two parameters and run it with the local environment manager if it works here; say exactly what ran.
**Asked at:** MLflow official docs and tutorials (mlflow.org tracking, autolog and model registry pages, MLflow 3.1.3 autolog docs, MLflow 2.11 model signature docs, DataTalksClub MLOps Zoomcamp experiment-tracking module, Azure ML MLflow training pages; search snippets only, not opened); docs and course material, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** An MLproject file is a small YAML recipe: a name, entry points with typed parameters, and an environment. `mlflow run` reads it, creates a run, and executes the command with the parameters filled in.
**Then explain:**
- The file has `name`, `entry_points` (each with `parameters` that have a type and a default, and a `command`), and one environment key: `python_env`, `conda_env` or `docker_env`.
- `mlflow run . -P C=0.5` builds the command line, starts a run that is tagged `source.type = PROJECT`, and runs the command. Your script then logs into that same run (inside `mlflow run`, `start_run()` attaches to the run the CLI made, because the CLI sets the run id in an environment variable).
- `--env-manager local` skips building an environment and uses the Python you already have. The other choices are `virtualenv`, `uv` and `conda` (check `mlflow run --help` for your version). Only local is fast and also the least reproducible.
- If the folder is a Git repo, MLflow records the commit as a tag, and it can run straight from a Git URL. In my run the folder was not a Git repo, so no commit tag was written. I did not run the Git case.
- Why many teams skip it now (my view, hedge): a plain script plus a `dvc.yaml` or an orchestrator already gives the command, the parameters and the data lineage. MLproject adds a second place to declare the same things, and the environment build can be slow. It is still fine for small teams that want one command to rerun a tracked run.
- Failure modes: a parameter with the wrong type fails before the command starts; a missing default with no `-P` fails; `docker_env` needs a running Docker daemon (not available here, not executed).
**Example:** `C` is declared `float, default 1.0`. `mlflow run . -P C=0.5` runs `python train.py --C 0.5 --max_iter 100`. Hand check: one new run, `params.C = 0.5`, `params.max_iter = 100` (default used), and `test_acc` on the iris test split.
**Code:** MLproject (YAML), `train.py` (Python), and the shell driver that ran everything in a fresh temp directory with a sqlite tracker. MLflow 3.17.2 here.
```yaml
name: iris_demo
entry_points:
  main:
    parameters:
      C: {type: float, default: 1.0}
      max_iter: {type: int, default: 100}
    command: "python train.py --C {C} --max_iter {max_iter}"
```
```python
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
```
```bash
set -e
source "$(dirname "$0")/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q21.XXXX); cp "$(dirname "$0")"/{MLproject,train.py} $W/; cd $W
export MLFLOW_TRACKING_URI=sqlite:///mlflow.db
mlflow --version
mlflow run . --env-manager local --experiment-name proj -P C=0.5 2>&1 | grep -v '^$' | tail -8
python3 -I - <<'P'
import mlflow
mlflow.set_tracking_uri("sqlite:///mlflow.db")
df = mlflow.search_runs(experiment_names=["proj"])
r = df.iloc[0]
print(df.shape[0], "run;", "status", r["status"])
print({k: r[k] for k in ["params.C","params.max_iter","metrics.test_acc"]})
print(sorted(c for c in df.columns if c.startswith("tags.mlflow")))
print("source.name:", r["tags.mlflow.source.name"], "| source.type:", r["tags.mlflow.source.type"])
P
```
**Output (my run):** Real run, `--env-manager local`, MLflow 3.17.2, Python 3.13. The `source.name` line is a temp folder, so it will differ on your machine.
```text
mlflow, version 3.17.2
2026/10/26 14:04:55 INFO mlflow.store.db.utils: Creating initial MLflow database tables...
2026/10/26 14:04:55 INFO mlflow.store.db.utils: Updating database tables
2026/10/26 14:04:56 INFO mlflow.projects: 'proj' does not exist. Creating a new experiment
2026/10/26 14:04:57 INFO mlflow.projects.utils: === Created directory /tmp/tmphd8_4623 for downloading remote URIs passed to arguments of type 'path' ===
2026/10/26 14:04:57 INFO mlflow.projects.backend.local: === Running command 'python train.py --C 0.5 --max_iter 100' in run with ID '6a339424d9384e18a3522ffe9215c585' === 
2026/10/26 14:05:00 INFO mlflow.projects: === Run (ID '6a339424d9384e18a3522ffe9215c585') succeeded ===
1 run; status FINISHED
{'params.C': '0.5', 'params.max_iter': '100', 'metrics.test_acc': np.float64(0.9778)}
['tags.mlflow.project.backend', 'tags.mlflow.project.entryPoint', 'tags.mlflow.runName', 'tags.mlflow.source.name', 'tags.mlflow.source.type', 'tags.mlflow.user']
source.name: /tmp/claude-0/b4q21.Kn4c | source.type: PROJECT
```

**Follow-ups:**
- *Can I run it from GitHub?* Yes: `mlflow run https://github.com/org/repo -P C=0.5` clones and runs. Not executed here (no repo to point at).
- *How do I run it on a cluster?* `--backend` options exist (for example Kubernetes or Databricks). Not executed here; check current docs.
- *What replaces it?* A `dvc.yaml` stage, an Airflow or Prefect task, or a plain CLI. All of them can still log to MLflow.
**Common mistakes:**
- Believing `mlflow run` makes the run reproducible. With `--env-manager local` it only records the command and parameters, not your installed libraries.
- Forgetting that `train.py` must call `mlflow.log_*` itself (or autolog). The CLI creates the run but does not know your metrics.
- Hard-coding the tracking URI in `train.py`, so the CLI and the script write to different places.

### Q22 ⭐⭐ 🟡 MLflow model flavors and pyfunc. Explain the MLmodel file (flavors, signature, run_id, environment files such as requirements.txt and conda.yaml), why the python_function flavor gives one predict interface over sklearn, xgboost, pytorch and custom code, and how to write a custom pyfunc model (PythonModel with load_context and predict) that bundles preprocessing and the model so serving cannot skew. Show the folder a logged model produces, and a custom pyfunc that is loaded and called locally.
**Asked at:** MLflow official docs and tutorials (mlflow.org tracking, autolog and model registry pages, MLflow 3.1.3 autolog docs, MLflow 2.11 model signature docs, DataTalksClub MLOps Zoomcamp experiment-tracking module, Azure ML MLflow training pages; search snippets only, not opened); docs and course material, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** The MLmodel file is the model's manifest. It lists the flavors (ways to load the model), the signature and the environment files. The `python_function` flavor gives every model one `predict` call, and a custom PythonModel lets me ship the preprocessing together with the model.
**Then explain:**
- A logged model is a folder: `MLmodel`, `requirements.txt`, `conda.yaml`, `python_env.yaml`, plus the model files and, for custom pyfunc, an `artifacts/` folder (see the run output below).
- `MLmodel` lists `flavors`. An sklearn model has two: `sklearn` (load back as an sklearn object) and `python_function` (generic). A custom model has only `python_function`.
- Serving tools only need the pyfunc flavor, so one server can run sklearn, xgboost, pytorch or custom code behind `predict(DataFrame)`.
- Custom `PythonModel`: `load_context` runs once at load and reads the bundled files; `predict` runs per request. Put the scaler and the model inside, and callers cannot forget the scaling.
- Failure modes: the pickled class is serialised with cloudpickle, so loading needs a compatible Python and library set (the `python_version` and `requirements.txt` in the folder tell you which). Only load models you trust: pickle can run code on load. MLflow also warns that a Python object as `python_model` uses CloudPickle and suggests models-from-code (check current docs).
**Example:** Iris rows 0, 60, 120 are classes 0, 1, 2. The custom model scales inside `predict`, so raw rows give `[0, 1, 2]`. A plain sklearn model that was trained on scaled data, loaded as pyfunc and fed the same raw rows, gives `[1, 2, 2]`: that is training-serving skew in one line.
**Code:** One script. It trains a scaler and a logistic regression, wraps both in `ScaledClf`, logs it, lists the folder, prints the `MLmodel` file and calls the loaded model.
```python
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
```
```bash
set -e
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q22.XXXX); cd $W
python3 -I "$D/q22.py" 2>&1 | sed "s/\x1b\[[0-9;]*m//g" | grep -v "INFO\|Downloading\|color_warning"
```
**Output (my run):** Real run (MLflow 3.17.2, sqlite tracker in a temp dir; warnings kept as printed, the per-line INFO logs were filtered out).
```text
/tmp/claude-0/ven/v/lib/python3.13/site-packages/mlflow/pyfunc/utils/data_validation.py:187: UserWarning: Add type hints to the `predict` method to enable data validation and automatic signature inference during model logging. Che ...[line cut for the book]
2026/10/26 14:05:37 WARNING mlflow.pyfunc: Passing a Python object as `python_model` causes it to be serialized using CloudPickle, it requires exercising caution as Python object serialization mechanisms may execute arbitrary code ...[line cut for the book]
files in the pyfunc model folder:
   MLmodel
   conda.yaml
   input_example.json
   python_env.yaml
   python_model.pkl
   registered_model_meta
   requirements.txt
   serving_input_example.json
   artifacts/clf.pkl
   artifacts/scaler.pkl

--- MLmodel (custom pyfunc), trimmed ---
flavors:
  python_function:
    artifacts:
      clf:
        path: artifacts/clf.pkl
        uri: clf.pkl
      scaler:
        path: artifacts/scaler.pkl
        uri: scaler.pkl
    cloudpickle_version: 3.1.2
    code: null
    env:
      conda: conda.yaml
      virtualenv: python_env.yaml
    loader_module: mlflow.pyfunc.model
    python_model: python_model.pkl
    python_version: 3.13.17
    streamable: false
is_signature_from_type_hint: false
model_size_bytes: 4619
prompts: null
saved_input_example_info:
  artifact_path: input_example.json
  pandas_orient: split
  serving_input_path: serving_input_example.json
  type: dataframe
signature:
  inputs: '[{"type": "double", "name": "sepal length (cm)", "required": true}, {"type":
    "double", "name": "sepal width (cm)", "required": true}, {"type": "double", "name":
    "petal length (cm)", "required": true}, {"type": "double", "name": "petal width
    (cm)", "required": true}]'
  outputs: '[{"type": "tensor", "tensor-spec": {"dtype": "int64", "shape": [-1]}}]'
  params: null
type_hint_from_example: false

--- flavors in the plain sklearn model ---
['python_function', 'sklearn']

custom pyfunc on RAW (unscaled) rows: [0, 1, 2] | truth: [0, 1, 2]
/tmp/claude-0/ven/v/lib/python3.13/site-packages/sklearn/utils/validation.py:2823: UserWarning: X has feature names, but LogisticRegression was fitted without feature names
  warnings.warn(
plain sklearn pyfunc on the same raw rows: [1, 2, 2] (no scaler inside, so skew risk)
```

**Follow-ups:**
- *Why not just pickle a sklearn Pipeline?* A Pipeline already bundles scaler and model. Custom pyfunc is for things a Pipeline cannot hold: rules, lookups, multiple models, post-processing.
- *What does `signature` in MLmodel do?* It lets pyfunc check input columns and types at predict time (see Q9).
- *Can I avoid pickle?* Yes, models-from-code logs a Python file instead of a pickled object. Not run here; check current docs.
**Common mistakes:**
- Doing preprocessing in a notebook and logging only the bare model, so the server receives raw data and quietly gives wrong answers.
- Loading bundled files in `predict` instead of `load_context`, so they are read on every request.
- Ignoring `requirements.txt` in the model folder and then being surprised that load fails on a different Python.

### Q23 ⭐⭐ 🟡 Serving an MLflow model locally. Explain mlflow models serve, mlflow models predict and the REST /invocations request formats (dataframe_split, dataframe_records, inputs; check the docs for the version), environment managers (local, virtualenv, uv or conda), and what mlflow models build-docker produces (Docker is not available here). Run mlflow models predict on a registered model locally and, if feasible, serve it on localhost and post one request. Part 6 owns serving frameworks and production design; keep this to what MLflow itself provides. Docker builds are not executed.
**Asked at:** MLflow official docs and tutorials (mlflow.org tracking, autolog and model registry pages, MLflow 3.1.3 autolog docs, MLflow 2.11 model signature docs, DataTalksClub MLOps Zoomcamp experiment-tracking module, Azure ML MLflow training pages; search snippets only, not opened); docs and course material, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** MLflow itself gives me `mlflow models predict` for a batch file and `mlflow models serve` for a small REST server with `/ping` and `/invocations`. For real production serving I would use a proper serving stack (Part 6).
**Then explain:**
- Both commands take a model URI like `models:/iris_clf@champion`, which is the registry alias from Q8. Moving the alias changes what `serve` loads on its next start.
- The request body must have exactly one top-level key: `dataframe_split`, `dataframe_records`, `instances` or `inputs` (the MLflow 3.17.2 error text lists these four; check the docs for your version). The same rule applies to the input file of `predict -t json`.
- `--env-manager` chooses where the model runs: `local` (current Python), `virtualenv`, `uv`, or `conda` (conda needs conda installed). A fresh environment is safer and slower.
- `mlflow models build-docker` builds an image whose default entrypoint serves the model on port 8080 (from `--help`). Not executed here: no Docker daemon. Part 2 and Part 6 cover images and serving.
- Failure modes: a bare `{columns, data}` file without the wrapper key fails; a missing column is rejected by the signature check with an `INVALID_PARAMETER_VALUE` error JSON (real text below); `serve` with `local` uses whatever versions are installed, which may differ from the training environment.
**Example:** Two iris rows are sent as `dataframe_split`. Both are setosa (class 0), so `{"predictions": [0, 0]}` is the hand-checkable answer. A single row with petal length 5.2 and petal width 2.3 should be virginica (class 2).
**Code:** `make_model.py` registers `iris_clf` v1 with alias `champion` in a sqlite registry; the shell script then runs `predict`, starts `serve` on 127.0.0.1:5088, sends three requests with curl, and stops the server.
```python
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
```
```bash
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q23.XXXX); cd $W
export MLFLOW_TRACKING_URI=sqlite:///mlflow.db
python3 -I "$D/make_model.py" 2>&1 | grep -v "INFO\|Downloading\|WARNING"
echo "--- mlflow models predict (batch, CLI) ---"
python3 -I -c "import json;d=json.load(open('in_split.json'));print(json.dumps({'dataframe_split':d}))" > in_req.json
cat in_split.json; echo
echo "bare split file (no wrapper key):"
mlflow models predict -m models:/iris_clf@champion -i in_split.json -t json --env-manager local 2>&1 | grep "^mlflow.exceptions" | cut -c1-200
echo "wrapped file {\"dataframe_split\": ...}:"
mlflow models predict -m models:/iris_clf@champion -i in_req.json -t json --env-manager local 2>&1 | grep -v "INFO\|WARNING\|Downloading"
echo "--- mlflow models serve (localhost:5088) ---"
mlflow models serve -m models:/iris_clf@champion -p 5088 -h 127.0.0.1 --env-manager local > serve.log 2>&1 &
PID=$!
for i in $(seq 1 40); do curl -s http://127.0.0.1:5088/ping -o /dev/null -w "%{http_code}" 2>/dev/null | grep -q 200 && break; sleep 1; done
echo "GET /ping -> $(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:5088/ping)"
echo "dataframe_split:"; curl -s -X POST http://127.0.0.1:5088/invocations -H 'Content-Type: application/json' -d @in_req.json; echo
echo "dataframe_records:"; curl -s -X POST http://127.0.0.1:5088/invocations -H 'Content-Type: application/json' -d '{"dataframe_records":[{"sepal length (cm)":6.7,"sepal width (cm)":3.0,"petal length (cm)":5.2,"petal width (cm)":2.3}]}'; echo
echo "missing column:"; curl -s -X POST http://127.0.0.1:5088/invocations -H 'Content-Type: application/json' -d '{"dataframe_records":[{"sepal length (cm)":6.7}]}' | cut -c1-260; echo
kill $PID; wait $PID 2>/dev/null
```
**Output (my run):** Real run on localhost, MLflow 3.17.2. The last error line is cut for length. The `pip`/INFO startup noise was filtered out.
```text
Successfully registered model 'iris_clf'.
Created version '1' of model 'iris_clf'.
registered iris_clf v1, alias champion
--- mlflow models predict (batch, CLI) ---
{"columns":["sepal length (cm)","sepal width (cm)","petal length (cm)","petal width (cm)"],"data":[[5.1,3.5,1.4,0.2],[4.9,3.0,1.4,0.2]]}
bare split file (no wrapper key):
mlflow.exceptions.MlflowException: The input must be a JSON dictionary with exactly one of the input fields {'instances', 'inputs', 'dataframe_records', 'dataframe_split'}. Received dictionary with in
wrapped file {"dataframe_split": ...}:
{"predictions": [0, 0]}
--- mlflow models serve (localhost:5088) ---
GET /ping -> 200
dataframe_split:
{"predictions": [0, 0]}
dataframe_records:
{"predictions": [2]}
missing column:
{"error_code": "INVALID_PARAMETER_VALUE", "message": "Failed to predict data '   sepal length (cm)\n0                6.7'. \nError: Failed to enforce schema of data '   sepal length (cm)\n0                6.7' with schema '['sepal ...[line cut for the book]
```

**Follow-ups:**
- *Is `mlflow models serve` production ready?* It is fine for a demo or a simple internal tool. Autoscaling, auth, batching and rollout control come from the platform around it (Part 6, Part 3).
- *What is `/ping` for?* A health check; it returned 200 here.
- *How do I send a tensor?* Use `inputs` (check the docs for your version). Not run here.
**Common mistakes:**
- Sending the DataFrame JSON without the `dataframe_split` wrapper key.
- Serving with `--env-manager local` and assuming the libraries match training.
- Pointing a service at `models:/name/latest` or a version number and then not knowing which model is live. Use an alias.

### Q24 ⭐⭐ 🟡 MLflow artifacts in depth: log_artifact, log_artifacts, log_figure, log_text, log_dict, log_table, artifact URIs, how artifact_location is fixed when an experiment is created, proxied artifact serving (--serve-artifacts) versus clients holding their own S3 credentials, and the problem of artifacts written by a client that cannot reach the server's path. Show a local run that logs a figure, a dict and a CSV and then downloads them with mlflow.artifacts.download_artifacts. S3 and proxy mode against a remote server are not executed.
**Asked at:** MLflow official docs and tutorials (mlflow.org tracking, autolog and model registry pages, MLflow 3.1.3 autolog docs, MLflow 2.11 model signature docs, DataTalksClub MLOps Zoomcamp experiment-tracking module, Azure ML MLflow training pages; search snippets only, not opened); docs and course material, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** An artifact is any file attached to a run. The tracking store keeps the run row; the artifact store keeps the bytes, at a location fixed when the experiment is created.
**Then explain:**
- APIs: `log_artifact` (one file), `log_artifacts` (a folder), `log_figure`, `log_text`, `log_dict`, `log_table`. All write under `<artifact_location>/<run_id>/artifacts/...`. `download_artifacts` and `load_text` read them back.
- `artifact_location` is set at experiment creation (a default under `./mlruns`, or `--default-artifact-root` on a server, or the `artifact_location` argument as I did). Changing the server flag later does not move old experiments.
- With a remote server there are two modes. Direct access: the client writes to S3 itself and needs its own credentials. Proxied access (`--serve-artifacts`): the client talks only to the server, which holds the credentials. Check current docs for flags and defaults. Not executed here (needs S3 and a remote server).
- Classic failure: the client logs to a path that only the server can see, for example a server folder `/srv/art`. The client then tries to create `/srv/art` on its own machine and gets a permission or missing-path error. Proxied mode avoids this.
- Do not put huge files or secrets in artifacts. Artifacts are as widely readable as the store.
**Example:** After the run, the listing should show six folders: `cfg`, `notes`, `outputs`, `plots`, `shards` (two files from `log_artifacts`) and `tables`. Hand check: `shards/part0.txt` and `part1.txt` exist because the loop wrote two files.
**Code:** A run that logs a figure, a dict, a text note, a CSV, a folder and a table to a custom `artifact_location`, lists them, then downloads three of them. Needs matplotlib (it was installed here).
```python
# Q24: artifact logging APIs, artifact_location fixed at experiment creation, download back.
import os, json, mlflow, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
mlflow.set_tracking_uri("sqlite:///mlflow.db")
exp_id = mlflow.create_experiment("art", artifact_location="file:///tmp/claude-0/b4q24_art_root")
exp = mlflow.get_experiment(exp_id)
print("artifact_location fixed at creation:", exp.artifact_location)
with mlflow.start_run(experiment_id=exp_id) as run:
    fig, ax = plt.subplots(); ax.plot([1, 2, 3], [1, 4, 9]); ax.set_title("demo")
    mlflow.log_figure(fig, "plots/curve.png")
    mlflow.log_dict({"lr": 0.1, "features": ["a", "b"]}, "cfg/config.json")
    mlflow.log_text("hello run", "notes/readme.txt")
    pd.DataFrame({"id": [1, 2], "pred": [0.2, 0.9]}).to_csv("preds.csv", index=False)
    mlflow.log_artifact("preds.csv", artifact_path="outputs")           # one file
    os.makedirs("many", exist_ok=True)
    for i in range(2): open(f"many/part{i}.txt", "w").write(str(i))
    mlflow.log_artifacts("many", artifact_path="shards")                 # a whole folder
    mlflow.log_table(pd.DataFrame({"q": ["a", "b"], "score": [1, 2]}), "tables/eval.json")
    print("run artifact_uri:", run.info.artifact_uri)
    rid = run.info.run_id
c = mlflow.MlflowClient()
def walk(p=None, ind=""):
    for f in c.list_artifacts(rid, p):
        print(ind + f.path + ("/" if f.is_dir else ""))
        if f.is_dir: walk(f.path, ind + "  ")
print("listing:"); walk()
d = mlflow.artifacts.download_artifacts(run_id=rid, artifact_path="cfg/config.json", dst_path="dl")
print("downloaded ->", os.path.relpath(d), json.load(open(d)))
d2 = mlflow.artifacts.download_artifacts(run_id=rid, artifact_path="outputs/preds.csv", dst_path="dl")
print("csv back:", pd.read_csv(d2).to_dict("list"))
print("text back:", mlflow.artifacts.load_text(f"runs:/{rid}/notes/readme.txt"))
```
```bash
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
rm -rf /tmp/claude-0/b4q24_art_root
W=$(mktemp -d /tmp/claude-0/b4q24.XXXX); cd $W
python3 -I "$D/q24.py" 2>&1 | grep -v "INFO\|Downloading"
```
**Output (my run):** Real run, MLflow 3.17.2, local file artifact root.
```text
artifact_location fixed at creation: file:///tmp/claude-0/b4q24_art_root
run artifact_uri: file:///tmp/claude-0/b4q24_art_root/09ab9c5dedff4590a99061ca4384dda8/artifacts
listing:
cfg/
  cfg/config.json
notes/
  notes/readme.txt
outputs/
  outputs/preds.csv
plots/
  plots/curve.png
shards/
  shards/part0.txt
  shards/part1.txt
tables/
  tables/eval.json
downloaded -> dl/config.json {'lr': 0.1, 'features': ['a', 'b']}
csv back: {'id': [1, 2], 'pred': [0.2, 0.9]}
text back: hello run
```
Not executed: S3 or other object stores, `--serve-artifacts` against a remote server, and cross-machine path problems. Validation that did run: the artifact location is a plain path that I fixed at experiment creation and every file came back with the right content.
**Follow-ups:**
- *Can I move artifacts to another bucket?* You copy the files and update the stored location. Plan this early; check current docs.
- *Where does the model go?* `log_model` is an artifact folder plus a registered model entry (Q8, Q22).
- *Large files?* Log a pointer and a hash (a DVC hash from Q15) instead of copying a dataset into every run.
**Common mistakes:**
- Creating the experiment before the server's artifact root is right, then discovering it is stuck.
- Giving every laptop its own S3 keys instead of using proxied access.
- Logging a 5 GB dataset into every run.

### Q25 ⭐⭐ 🟡 Governing the model registry beyond aliases: descriptions, tags (validation_status, data_version, owner), model version tags, who can register or move an alias (permissions need an authenticated server or a managed platform; check current docs), the audit question 'who moved champion to version 7 and when', and rollback by moving the alias back. Show a script that registers two versions, tags them, moves the alias and prints the version history with timestamps from the client API. Automated promotion gates belong to Part 7; authentication on a server is not executed.
**Asked at:** MLflow Model Registry sources (mlflow.org registry docs, MLflow GitHub issue on stage deprecation, ZenML MLflow registry page, Databricks community and knowledge-base posts; search snippets only, not opened); docs and community posts, not interview reports; MLOps roles using MLflow or Databricks
**Say this first (1 line):** Aliases say which version is live, but governance needs more: tags for status and owner, a note for every move, and permissions on who may move an alias. The audit trail is mostly something I add myself.
**Then explain:**
- Model versions carry tags (for example `validation_status`, `data_version`, `owner`) and a registered model has a description. The client API also returns a creation time for each version.
- Moving an alias is one call, `set_registered_model_alias`. Rollback is the same call pointed at the old version.
- What the client API did NOT give me in this run: who moved the alias and when. The alias map shows only the current target. So I wrap the move in a helper that writes `promoted_by`, `promoted_at` and a note as tags, ideally also to an append-only log outside MLflow.
- Tags keep only the last value per key. My rollback overwrote the first release note on v1 (see the output): history in tags is lossy. Use an external log, or one tag key per event.
- Who may move an alias: a plain local or open server has no per-user permission. An authenticated server, or a managed platform (Databricks, Azure ML, SageMaker), adds that. Check current docs. Not executed here.
- Edge case: `search_model_versions` returned an empty `aliases` list for a version that does hold an alias, while `get_model_version` showed it. Use `get_model_version` or the model's alias map when you need aliases.
**Example:** Two versions. v1 is `pending`, v2 is `approved`. Alias goes v1 (first release), then v2, then back to v1. Hand check: after the rollback the alias map must read `{'champion': 1}`, and the v1 note must say `v2 -> v1`.
**Code:** Registers `iris_gov` twice (C=0.1, then C=5.0), tags the versions, moves the alias with an audit helper, rolls back and prints the history.
```python
# Q25: register two versions, tag them, move the alias, print history from the client API.
import time, datetime as dt, mlflow
from mlflow import MlflowClient
from mlflow.models import infer_signature
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
mlflow.set_tracking_uri("sqlite:///mlflow.db")
c = MlflowClient(); NAME = "iris_gov"
X, y = load_iris(return_X_y=True, as_frame=True)
for C in (0.1, 5.0):
    m = LogisticRegression(C=C, max_iter=300).fit(X, y)
    with mlflow.start_run() as r:
        mlflow.log_param("C", C)
        mlflow.sklearn.log_model(m, name="model", signature=infer_signature(X, m.predict(X)), registered_model_name=NAME)
    v = c.search_model_versions(f"name='{NAME}'")[0].version      # newest first
    c.set_model_version_tag(NAME, v, "validation_status", "approved" if C == 5.0 else "pending")
    c.set_model_version_tag(NAME, v, "data_version", "md5:abc123")
    c.set_model_version_tag(NAME, v, "owner", "team-risk")
    time.sleep(1.1)
c.update_registered_model(NAME, description="Iris classifier (demo). Owner: team-risk.")

def move_alias(alias, to_version, who, why):
    """Audit trail is OUR job: the server stores the alias but not who moved it."""
    old = None
    try: old = c.get_model_version_by_alias(NAME, alias).version
    except Exception: pass
    c.set_registered_model_alias(NAME, alias, to_version)
    c.set_model_version_tag(NAME, to_version, "promoted_by", who)
    c.set_model_version_tag(NAME, to_version, "promoted_at", dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"))
    c.set_model_version_tag(NAME, to_version, "promotion_note", f"{alias}: v{old or '-'} -> v{to_version}; {why}")

move_alias("champion", "1", "asha", "first release")
move_alias("champion", "2", "dev", "better CV score")
print("champion now v", c.get_model_version_by_alias(NAME, "champion").version, "| rollback = move it back:")
move_alias("champion", "1", "asha", "rollback, v2 latency regression")
print("champion after rollback: v", c.get_model_version_by_alias(NAME, "champion").version)

print("\nversion history")
for mv in [c.get_model_version(NAME, v) for v in ("1", "2")]:
    t = dt.datetime.fromtimestamp(mv.creation_timestamp / 1000, dt.timezone.utc).strftime("%H:%M:%S")
    print(f"v{mv.version} created {t}Z aliases={mv.aliases} run={mv.run_id[:8]}")
    for k in sorted(mv.tags): print(f"    {k} = {mv.tags[k]}")
rm = c.get_registered_model(NAME)
print("\nmodel description:", rm.description, "| aliases map:", rm.aliases)
```
```bash
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q25.XXXX); cd $W
python3 -I "$D/q25.py" 2>&1 | grep -v "INFO\|Downloading\|WARNING\|Registered model\|Created version\|^$"
```
**Output (my run):** Real run, MLflow 3.17.2, sqlite registry. Timestamps are from my run.
```text
Successfully registered model 'iris_gov'.
champion now v 2 | rollback = move it back:
champion after rollback: v 1
version history
v1 created 14:07:56Z aliases=['champion'] run=b03d93f0
    data_version = md5:abc123
    owner = team-risk
    promoted_at = 2026-10-26T14:08:02+00:00
    promoted_by = asha
    promotion_note = champion: v2 -> v1; rollback, v2 latency regression
    validation_status = pending
v2 created 14:08:01Z aliases=[] run=9c75ad41
    data_version = md5:abc123
    owner = team-risk
    promoted_at = 2026-10-26T14:08:02+00:00
    promoted_by = dev
    promotion_note = champion: v1 -> v2; better CV score
    validation_status = approved
model description: Iris classifier (demo). Owner: team-risk. | aliases map: {'champion': 1}
```
Not executed: authentication, permissions and any server that records who made a change. The tags above are written by my helper, not by MLflow.
**Follow-ups:**
- *Who moved champion to v7?* Only what my helper and the server's own logs recorded. A managed platform may keep an audit log; check current docs.
- *Should CI move the alias?* Yes, with a service account and a gate. Part 7 owns that.
- *Tags or aliases for status?* Aliases for pointers (one version holds it); tags for facts about a version.
**Common mistakes:**
- Treating the alias map as an audit log.
- Putting status only in the model name (`iris_prod_v2`).
- Letting every data scientist move `champion` from a notebook.

### Q26 ⭐⭐ 🟡 Weights & Biases sweeps. Explain a sweep config (method grid, random or bayes, metric goal, parameter ranges and distributions), wandb.sweep, wandb.agent and running agents on several machines, early termination (Hyperband), and cost control (max runs). Compare with Optuna and with MLflow plus Optuna. Write a sweep configuration and validate it with a Python script (parse YAML, check ranges and the metric name); wandb.sweep and agents need an account and network and are not executed.
**Asked at:** Weights & Biases sources (techinterview.org 'Weights & Biases Interview Guide', KDnuggets 'Weights & Biases crash course', TWIML podcast on managing ML artifacts, wandb.ai articles; search snippets only, not opened); guide and docs, not verified candidate reports; ML engineer and MLOps roles at AI-lab and product companies
**Say this first (1 line):** A W&B sweep is a hyperparameter search run by W&B. I write a config (method, metric, parameters), call `wandb.sweep`, then run one or more `wandb.agent` processes that pull the next set of parameters.
**Then explain:**
- Config: `method` is `grid`, `random` or `bayes`; `metric` has a name and a goal; `parameters` are either `values` (a list) or a distribution with min and max.
- The metric name must match what the script logs with `wandb.log`. A typo means bayes and early termination have nothing to optimise. My validator catches this against a list of logged names.
- Agents can run on many machines against the same sweep id. Cost control: cap runs with the `count` argument of `wandb.agent` (and a stop rule on the sweep; check current docs for the exact option). Early termination (`hyperband`) stops weak runs early.
- Grid with ranges does not make sense; grid needs discrete values and multiplies fast (5 x 5 x 3 x 2 = 150 runs).
- Versus Optuna: Optuna is a library that runs in your own process with pruning and storage you choose; W&B sweeps give a hosted controller and a dashboard. Optuna plus MLflow logging gives a fully self-hosted setup. Both are fine; the choice is about where you want the controller and the UI.
**Example:** `lr` log-uniform from 1e-4 to 1e-1, `batch_size` from [16, 32, 64], `dropout` uniform from 0 to 0.5, `optimizer` adam or sgd, bayes on `val_auc` (maximise) with hyperband. Hand check: `min < max`, `lr` min above 0 (log), metric is one that `train.py` logs.
**Code:** `sweep.yaml`, the offline validator (pyyaml only), the helper that tries `wandb.sweep` without an account, and the driver.
```yaml
program: train.py
method: bayes
metric:
  name: val_auc
  goal: maximize
parameters:
  lr:
    distribution: log_uniform_values
    min: 0.0001
    max: 0.1
  batch_size:
    values: [16, 32, 64]
  dropout:
    distribution: uniform
    min: 0.0
    max: 0.5
  optimizer:
    values: [adam, sgd]
early_terminate:
  type: hyperband
  min_iter: 3
  eta: 3
```
```python
# --- q26/validate_sweep.py ---
# Q26: validate a W&B sweep config offline (pyyaml only; no wandb import, no network).
import sys, yaml
METHODS = {"grid", "random", "bayes"}
DISTS_RANGE = {"uniform", "int_uniform", "log_uniform_values", "q_uniform", "q_log_uniform_values"}
def check(cfg, logged_metrics):
    errs = []
    if cfg.get("method") not in METHODS: errs.append(f"method must be one of {sorted(METHODS)}, got {cfg.get('method')!r}")
    m = cfg.get("metric", {})
    if cfg.get("method") == "bayes" and not m: errs.append("bayes needs a metric block")
    if m and m.get("goal") not in {"minimize", "maximize"}: errs.append(f"metric.goal invalid: {m.get('goal')!r}")
    if m and m.get("name") not in logged_metrics: errs.append(f"metric.name {m.get('name')!r} is never logged by train.py (known: {sorted(logged_metrics)})")
    params = cfg.get("parameters") or {}
    if not params: errs.append("no parameters")
    for k, p in params.items():
        if "values" in p:
            if not p["values"]: errs.append(f"{k}: empty values")
        elif "value" in p: pass
        else:
            d = p.get("distribution", "uniform")
            if d in DISTS_RANGE:
                lo, hi = p.get("min"), p.get("max")
                if lo is None or hi is None: errs.append(f"{k}: {d} needs min and max")
                elif lo >= hi: errs.append(f"{k}: min {lo} must be < max {hi}")
                elif d.startswith(("log", "q_log")) and lo <= 0: errs.append(f"{k}: log distribution needs min > 0")
            else: errs.append(f"{k}: unknown distribution {d!r}")
        if cfg.get("method") == "grid" and "values" not in p and "value" not in p:
            errs.append(f"{k}: grid search needs discrete values, not a range")
    if "early_terminate" in cfg and cfg["early_terminate"].get("type") != "hyperband":
        errs.append("early_terminate.type should be hyperband")
    return errs

cfg = yaml.safe_load(open("sweep.yaml"))
logged = {"val_auc", "val_loss", "train_loss"}
print("good config  ->", check(cfg, logged) or "OK")
bad = yaml.safe_load(open("sweep.yaml"))
bad["method"] = "grid"; bad["metric"]["name"] = "val_acc"
bad["parameters"]["lr"]["min"] = 0.5
bad["parameters"]["dropout"]["distribution"] = "normalish"
print("broken config ->")
for e in check(bad, logged): print("   -", e)
print("grid blow-up check: 5 lr values * 5 dropout values * 3 batch sizes * 2 optimizers =", 5*5*3*2, "runs")

# --- q26/try_sweep.py ---
# Shows what happens when you call wandb.sweep with no account/network (offline mode).
import wandb, yaml
cfg = yaml.safe_load(open("sweep.yaml"))
try:
    sid = wandb.sweep(cfg, project="demo")
    print("sweep id:", sid)
except Exception as e:
    print(type(e).__name__ + ":", str(e).splitlines()[0][:200])
```
```bash
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q26.XXXX); cd $W; cp $D/sweep.yaml .
python3 -I "$D/validate_sweep.py"
echo "--- wandb.sweep with no account (WANDB_MODE=offline) ---"
timeout 60 python3 -I "$D/try_sweep.py" 2>&1 | tail -3
```
**Output (my run):** The validator is my own checker (not a W&B tool) and covers only the rules in the code. The last line is the real `wandb.sweep` failure without an account (wandb 0.31.0).
```text
good config  -> OK
broken config ->
   - metric.name 'val_acc' is never logged by train.py (known: ['train_loss', 'val_auc', 'val_loss'])
   - lr: min 0.5 must be < max 0.1
   - lr: grid search needs discrete values, not a range
   - dropout: unknown distribution 'normalish'
   - dropout: grid search needs discrete values, not a range
grid blow-up check: 5 lr values * 5 dropout values * 3 batch sizes * 2 optimizers = 150 runs
--- wandb.sweep with no account (WANDB_MODE=offline) ---
UsageError: No API key configured. Use `wandb login` to log in.
```
Not executed: `wandb.sweep` and `wandb.agent` for real (they need an account and network), hyperband behaviour, multi-machine agents. Validation that did run: the YAML parses and passes my checks; the broken copy produces five errors.
**Follow-ups:**
- *Random or bayes?* Random is a safe start and parallelises easily; bayes helps when each run is costly and the space is smooth.
- *How do I stop a runaway sweep?* Cap the count per agent and stop the sweep from the UI or CLI; check current docs.
- *Selection bias?* The best of N runs on validation is optimistic. Use a held-out test set once (Q11).
**Common mistakes:**
- Metric name in the config differs from the logged key.
- A grid sweep over continuous ranges.
- Leaving agents running overnight with no run cap.

### Q27 ⭐⭐ 🟡 W&B Artifacts and lineage. Explain Artifact(type, name), add_file, add_dir, log_artifact, use_artifact, the automatic versions v0, v1 and aliases such as latest, the lineage graph between runs and artifacts, references to files in S3 without copying, and how this compares to DVC (pointers in Git) and MLflow (artifacts attached to a run). Show the code and test what can be done offline (building an Artifact object locally and checking its digest or file manifest, if the library allows); logging to the service is not executed.
**Asked at:** Weights & Biases sources (techinterview.org 'Weights & Biases Interview Guide', KDnuggets 'Weights & Biases crash course', TWIML podcast on managing ML artifacts, wandb.ai articles; search snippets only, not opened); guide and docs, not verified candidate reports; ML engineer and MLOps roles at AI-lab and product companies
**Say this first (1 line):** A W&B Artifact is a versioned bundle of files. `log_artifact` creates a version (v0, v1, ...), `use_artifact` consumes one, and W&B draws the lineage graph between runs and artifacts for you.
**Then explain:**
- Build: `wandb.Artifact(name, type)`, then `add_file`, `add_dir`, or `add_reference` (a pointer to a file in a bucket or URL; the bytes are not copied).
- The versions `v0`, `v1` and aliases like `latest` are assigned by the server when you log. Offline I could build the artifact and read its manifest and digest, but not see a version number.
- Same content gives the same digest; one more row in the CSV gives a different digest (output below). That is the same content-addressing idea as DVC hashes.
- Compare: DVC keeps pointers in Git and the bytes in a remote you own. MLflow attaches artifacts to a run. W&B keeps versions and lineage in its service (cloud or self-hosted).
- Failure modes: an `s3://` reference needs boto3 and credentials; here it failed with a clear error. A reference artifact points at data that someone else can change or delete, so a checksum matters.
**Example:** A dataset artifact with `train.csv`, an image folder and a reference to a remote parquet file has 3 manifest entries. After appending one row to `train.csv`, the artifact digest must change. Both hold in the output.
**Code:** Builds the artifact locally with `wandb 0.31.0`, prints the manifest and digests, and shows the S3 reference error. The two lines at the end are the real service calls that I did not run.
```python
# Q27: W&B Artifact built locally. Nothing is uploaded; we inspect the manifest/digest.
import os, wandb
os.makedirs("data/imgs", exist_ok=True)
open("data/train.csv", "w").write("x,y\n1,2\n3,4\n")
open("data/imgs/a.txt", "w").write("img-a")

def build(extra=None):
    art = wandb.Artifact("train-data", type="dataset", description="tiny demo", metadata={"rows": 2})
    art.add_file("data/train.csv")
    art.add_dir("data/imgs", name="imgs")
    art.add_reference("https://example.com/raw/events.parquet", name="raw_events", checksum=False)   # pointer, nothing copied (s3:// works the same but needs boto3 + credentials)
    if extra: art.add_file(extra)
    return art

a1 = build()
print("name:", a1.name, "| type:", a1.type, "| size entries:", len(a1.manifest.entries))
for path, e in sorted(a1.manifest.entries.items()):
    print(f"  {path:16} digest={e.digest[:12]}... ref={e.ref}")
print("artifact digest v1:", a1.digest)
a1b = build()
print("same content, rebuilt -> same digest?", a1b.digest == a1.digest)
open("data/train.csv", "a").write("5,6\n")
a2 = build()
print("one row appended -> new digest?", a2.digest != a1.digest)
print("version/aliases before upload:", getattr(a1, "version", None), "| (v0/v1/latest are assigned by the server on log_artifact)")
try:
    a1.add_reference("s3://my-bucket/raw/events.parquet", name="s3ref")   # needs boto3 (and creds to checksum)
except Exception as e:
    print("s3:// reference here ->", type(e).__name__ + ":", str(e)[:90])
# the real lineage calls, shown but NOT run:
print("\nnot run: run.log_artifact(a2, aliases=['latest']) / run.use_artifact('train-data:v0') need an account")
```
```bash
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q27.XXXX); cd $W
timeout 90 python3 -I "$D/q27.py" 2>&1 | tail -30
```
**Output (my run):** Real offline run. Nothing was uploaded. The first line is wandb's own progress message.
```text
wandb: Adding directory to artifact (data/imgs)... Done. 0.0s
name: train-data | type: dataset | size entries: 3
  imgs/a.txt       digest=BkMMzP4kwnLZ... ref=None
  raw_events       digest=https://exam... ref=https://example.com/raw/events.parquet
  train.csv        digest=F4uoVwdHDEHP... ref=None
artifact digest v1: f6fe2d8e2ac987a649f41e7d1fe2b6fc
same content, rebuilt -> same digest? True
one row appended -> new digest? True
version/aliases before upload: None | (v0/v1/latest are assigned by the server on log_artifact)
s3:// reference here -> Error: s3:// references requires the boto3 library, run pip install wandb[aws]

not run: run.log_artifact(a2, aliases=['latest']) / run.use_artifact('train-data:v0') need an account
```
Not executed: `run.log_artifact`, `run.use_artifact`, version numbers and aliases, the lineage graph, S3 references. They need an account and network. Validation that did run: artifact manifests and digests built locally.
**Follow-ups:**
- *Can I use W&B Artifacts without W&B runs?* There are API calls for it; not tested here, check current docs.
- *How do I pin a version?* `use_artifact('train-data:v3')`. An alias like `latest` moves, so pin a version in training code.
- *Lineage gap?* Only objects logged through W&B are in the graph. Raw tables upstream are not.
**Common mistakes:**
- Using `latest` in a training script and losing reproducibility.
- Using references for data that can change, with no checksum.
- Assuming offline mode gives versions; they appear after sync or log.

### Q28 ⭐⭐ 🟡 Choosing an experiment tracker: MLflow, Weights & Biases, Neptune, Comet, TensorBoard, or a cloud-native one (SageMaker Experiments, Vertex AI Experiments, Azure ML). Give a decision table: self-hosting effort, cost model, collaboration and dashboards, registry features, access control, data residency, lock-in and portability (MLflow format as common ground). Add the India angle: data protection obligations under the Digital Personal Data Protection Act and company rules on sending metadata to a foreign SaaS (hedge, not legal advice) and the common use of MLflow on Databricks, Azure ML or SageMaker in IT-services and GCC teams. Pure comparison; nothing is executed.
**Asked at:** Bengaluru and India MLOps job postings that list DVC, MLflow and experiment tracking (weekday.works, builtinbengaluru, GrabJobs listings seen while researching Parts 2 and 3; snippets only) plus editorial MLOps guides; postings show required skills, not interview questions; IT-services firms, GCCs and AI product companies in India
**Say this first (1 line):** I choose the tracker by who runs it and who may see the data. MLflow is the open, self-hosted default. W&B is the polished hosted one. Cloud-native trackers fit if the whole stack is on one cloud.
**Then explain:**
- Decision table (my summary, hedged; check each vendor's current plans and terms; no prices here):

| Criterion | MLflow | W&B | Neptune / Comet | TensorBoard | Cloud-native (SageMaker, Vertex, Azure ML) |
|---|---|---|---|---|---|
| Hosting | You host it, or a managed one | Hosted first; self-host option | Hosted first | Local files | Inside the cloud account |
| Setup effort | Server, database, artifact store, auth | Almost none | Almost none | None | Low, but cloud lock-in |
| Dashboards, sweeps | Basic UI, no built-in sweeps | Strong UI, sweeps built in | Strong UI | Good for curves | Varies |
| Registry | Yes (aliases, tags) | Yes (artifact-based) | Varies | No | Yes, platform's own |
| Access control | Needs plugin, proxy or managed platform | Teams and roles in the service | Same | OS file permissions | Cloud IAM |
| Data residency | Wherever you deploy | Depends on plan and region; check | Same | Local | Region of the cloud account |
| Portability | MLflow model format is a common ground | Export APIs exist | Export APIs exist | Event files | Often MLflow-compatible; check |

- Questions that decide it: can metadata (run names, params, sometimes sample data) leave our network? who patches and backs up the server? do we need a registry and approvals? how many users?
- India angle (hedge, not legal advice): the Digital Personal Data Protection Act means that if run metadata or logged samples contain personal data, sending it to a foreign SaaS needs a review with the privacy or legal team. Many IT-services and GCC teams use MLflow on Databricks, Azure ML or SageMaker because it sits inside an approved cloud account (this is my observation of the market, not sourced).
- Failure mode: picking a tracker because the demo looked nice, then finding that logged samples contain customer data.
**Example:** A bank team with strict data rules and 15 data scientists on Azure: managed MLflow in Azure ML, no SaaS egress. A three-person startup with GPUs on rented machines: W&B hosted free tier (check current terms) for speed.
**Code:** No code. This is a pure comparison.
**Output (my run):** not executed. Nothing to run; this is a comparison written from general knowledge, not from opened vendor pages. Check current docs and terms for every row.

**Follow-ups:**
- *Can I switch later?* Params and metrics export easily; dashboards and reports do not. Keep the model in MLflow format and the data in DVC.
- *Do I need both MLflow and W&B?* Usually not (Q14). Some teams use W&B for experiments and MLflow for the registry; that doubles the logging code.
- *Self-host W&B?* An option exists on some plans; check current terms.
**Common mistakes:**
- Comparing price lists from memory.
- Ignoring data residency until a security review.
- Treating the tracker as the system of record for data versions.

### Q29 ⭐⭐ 🟡 Model cards and documentation for a registered model. Explain what a model card contains (intended use, training data and version, metrics overall and per slice, limitations, ethical considerations, owner, how to retrain), why it should be generated from the run and registry data rather than written by hand, and how to attach it as an MLflow artifact or tag and as a markdown file in the repo. Write a script that builds a model card from an MLflow run and registered version (params, metrics, tags, signature) and run it. Hedge the template source (Mitchell et al. model cards; check current docs).
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** A model card is a short, standard document about a model: what it is for, what data it was trained on, how well it works (overall and on slices), its limits and its owner. I generate the factual parts from MLflow so it cannot drift from the run.
**Then explain:**
- Contents (from the Mitchell et al. model card idea; check current docs for template variants): intended use, training data and version, parameters, metrics overall and per slice, inputs and outputs, limitations and ethics, owner, how to retrain.
- Facts come from the run and registry: params, metrics, tags, signature, run id. Judgement parts (intended use, limits) stay human-written and are marked as such in my script.
- Attach it two ways: as an artifact on the training run (`MODEL_CARD.md`) and as a pointer tag on the registered version; also commit the markdown in the repo for review.
- Failure modes: a stale card (written once, never regenerated); a missing tag silently becoming an empty field (my script prints `MISSING` and reports it); slice metrics on very few rows look precise but mean little (the demo test set has 15 and 30 rows).
- A card does not replace tests. It documents what was tested.
**Example:** Iris model v1: tags carry the data version and git SHA (demo values), three accuracy metrics, four double inputs. All appear in the card; a tag removed from the run would show as `MISSING`. Test accuracy is 1.000 on only 45 test rows, so I would say so.
**Code:** Trains, registers, and builds the markdown from the stored run and signature, logs it back to the run and sets a pointer tag.
```python
# Q29: generate a model card (markdown) from MLflow run + registry data, log it back as an artifact.
import json, mlflow
from mlflow import MlflowClient
from mlflow.models import infer_signature
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
mlflow.set_tracking_uri("sqlite:///mlflow.db"); c = MlflowClient(); NAME = "iris_card"

# --- train + log (slice = petal length bucket) ---
X, y = load_iris(return_X_y=True, as_frame=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
m = LogisticRegression(C=1.0, max_iter=300).fit(Xtr, ytr)
pred = m.predict(Xte)
with mlflow.start_run() as run:
    mlflow.log_params({"C": 1.0, "max_iter": 300, "test_size": 0.3, "seed": 0})
    mlflow.log_metric("test_acc", accuracy_score(yte, pred))
    short = Xte["petal length (cm)"] < 3
    mlflow.log_metric("acc_slice_short_petal", accuracy_score(yte[short], pred[short]))
    mlflow.log_metric("acc_slice_long_petal", accuracy_score(yte[~short], pred[~short]))
    mlflow.set_tags({"data_version": "md5:abc123 (demo)", "git_sha": "deadbeef (demo)", "owner": "team-risk"})
    mlflow.sklearn.log_model(m, name="model", signature=infer_signature(Xtr, m.predict(Xtr)), registered_model_name=NAME)
c.set_registered_model_alias(NAME, "champion", 1)

# --- build the card from stored facts, never from memory ---
def card(name, alias):
    mv = c.get_model_version_by_alias(name, alias)
    r = c.get_run(mv.run_id)
    sig = mlflow.models.get_model_info(f"models:/{name}@{alias}").signature.to_dict()
    L = [f"# Model card: {name} (v{mv.version}, alias {alias})", "",
         "## Intended use", "- Classify iris species from 4 measurements. Demo only, not for botanical decisions. (hand-written field)", "",
         "## Training data", f"- data_version: {r.data.tags.get('data_version', 'MISSING')}", f"- code: git {r.data.tags.get('git_sha', 'MISSING')}", "",
         "## Parameters"] + [f"- {k}: {v}" for k, v in sorted(r.data.params.items())] + ["", "## Metrics", "| metric | value |", "|---|---|"]
    L += [f"| {k} | {v:.3f} |" for k, v in sorted(r.data.metrics.items())]
    L += ["", "## Inputs", "| name | type |", "|---|---|"] + [f"| {i['name']} | {i['type']} |" for i in json.loads(sig["inputs"])]
    L += ["", "## Limitations", "- Only 150 rows; slice metrics rest on few test rows, check the counts before trusting them. (hand-written field)",
          f"- Owner: {r.data.tags.get('owner', 'MISSING')}", f"- Run: {mv.run_id}", ""]
    missing = [l for l in L if "MISSING" in l]
    return "\n".join(L), missing

text, missing = card(NAME, "champion")
print(text); print("fields missing:", missing or "none")
with mlflow.start_run(run_id=c.get_model_version_by_alias(NAME, "champion").run_id):
    mlflow.log_text(text, "MODEL_CARD.md")
open("MODEL_CARD.md", "w").write(text)
c.set_model_version_tag(NAME, "1", "model_card", "artifact: MODEL_CARD.md on the training run")
print("slice sizes in the test set: short petal =", int(short.sum()), ", long petal =", int((~short).sum()))
```
```bash
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q29.XXXX); cd $W
python3 -I "$D/q29.py" 2>&1 | grep -v "INFO\|Downloading\|WARNING\|Registered model\|Created version"
```
**Output (my run):** Real run, MLflow 3.17.2. The git SHA and data version are made-up demo strings.
```text
Successfully registered model 'iris_card'.
# Model card: iris_card (v1, alias champion)

## Intended use
- Classify iris species from 4 measurements. Demo only, not for botanical decisions. (hand-written field)

## Training data
- data_version: md5:abc123 (demo)
- code: git deadbeef (demo)

## Parameters
- C: 1.0
- max_iter: 300
- seed: 0
- test_size: 0.3

## Metrics
| metric | value |
|---|---|
| acc_slice_long_petal | 1.000 |
| acc_slice_short_petal | 1.000 |
| test_acc | 1.000 |

## Inputs
| name | type |
|---|---|
| sepal length (cm) | double |
| sepal width (cm) | double |
| petal length (cm) | double |
| petal width (cm) | double |

## Limitations
- Only 150 rows; slice metrics rest on few test rows, check the counts before trusting them. (hand-written field)
- Owner: team-risk
- Run: f616288f7b38446391fa08fba2e99e41

fields missing: none
slice sizes in the test set: short petal = 15 , long petal = 30
```

**Follow-ups:**
- *Who owns the card?* The model owner, with review in the PR. The facts are generated.
- *Per-slice metrics?* Pick slices in advance (region, device, age band) and log them as metrics, as the demo does with petal length.
- *Regulated settings?* The card feeds the audit file (Q40), it is not the audit file.
**Common mistakes:**
- Hand-typing metrics into a Word file.
- One overall number and no slices.
- No owner and no retrain instructions.

### Q30 ⭐⭐ 🔴 Table-format time travel versus ML data versioning: Delta Lake and Apache Iceberg time travel (query a table as of a version or timestamp, snapshots, retention and vacuum or expire-snapshots limits) versus DVC (file-level pointers) and lakeFS (branches over an object store). Explain which you use for an analytics table that feeds a feature pipeline, which for an image dataset, which for a training snapshot that must exist for years, and what happens when old snapshots are vacuumed. Concept level only: no Spark, Delta or Iceberg cluster is available here; a pure-Python toy snapshot table can be run to show the idea.
**Asked at:** Data-versioning comparison write-ups (lakeFS blog 'scalable data version control', kanerika data versioning tools, pdpspectra 'DVC vs lakeFS', jisaku glossary; search snippets only, not opened); vendor-written or low-quality blogs, treat specifics with caution; data and ML platform roles
**Say this first (1 line):** Delta and Iceberg give time travel over one table, inside the table format, until old snapshots are vacuumed. DVC pins whole files by hash in Git. lakeFS branches a whole object store. I pick by the data shape and by how long the snapshot must live.
**Then explain:**
- Delta Lake and Iceberg: every commit writes a new snapshot (a manifest listing immutable data files). You query a version or a timestamp (`VERSION AS OF`, `TIMESTAMP AS OF` in Delta; Iceberg has the same idea; check current docs for syntax). Concept level here: no cluster available.
- Retention: `VACUUM` (Delta) and `expire_snapshots` (Iceberg) delete files no kept snapshot needs. After that, time travel to the older version fails. Defaults and safe minimums exist; check current docs.
- DVC: file or folder level, content-hash pointers in Git, bytes in a cache and remote. It lasts as long as the remote keeps the hash and Git keeps the tag. It does not understand rows.
- lakeFS: branches, commits and merges over an object store, zero-copy; good for ingest-validate-merge on lots of files. Some sources report a changed stewardship of DVC (unverified; check news).
- Choice: analytics table feeding features: Delta or Iceberg (rows, schema evolution, SQL). Image dataset: DVC or lakeFS (files). Training snapshot that must live for years: copy that snapshot out to a protected, immutable location and pin it by hash (DVC tag, or a table version that is explicitly excluded from vacuum); never rely on the default retention.
- Failure mode (shown below): the snapshot a model was trained on shares files with other versions; one vacuum removes them and the model can no longer be reproduced.
**Example:** Version 0 has ids 1 and 2. Version 1 adds id 3. Version 2 rewrites the first file (id 2 changes from 20 to 25). Training used version 1. Vacuum keeping only the latest version deletes `data-v0-0.json`, which v1 also needs. Hand check: both v0 and v1 now fail.
**Code:** A pure-Python toy snapshot table (about 40 lines): immutable data files, one manifest per version, `read(version)`, `read(ts=...)` and `vacuum`. It teaches the idea only; it is not Delta or Iceberg code.
```python
# Q30: toy snapshot table (Delta/Iceberg idea in 60 lines): immutable data files + a manifest per version.
import json, os, tempfile, time
class ToyTable:
    def __init__(self, root): self.root = root; os.makedirs(root, exist_ok=True); self.log = []   # log[i] = manifest of version i
    def _write(self, name, rows):
        with open(os.path.join(self.root, name), "w") as f: json.dump(rows, f)
    def commit(self, add=(), remove=()):
        files = list(self.log[-1]["files"]) if self.log else []
        files = [f for f in files if f not in remove]
        for i, rows in enumerate(add):
            n = f"data-v{len(self.log)}-{i}.json"; self._write(n, rows); files.append(n)
        self.log.append({"version": len(self.log), "ts": time.time(), "files": files})   # files never edited in place
        return len(self.log) - 1
    def read(self, version=None, ts=None):
        if ts is not None: version = max(m["version"] for m in self.log if m["ts"] <= ts)
        m = self.log[-1 if version is None else version]
        rows = []
        for f in m["files"]:
            p = os.path.join(self.root, f)
            if not os.path.exists(p): raise FileNotFoundError(f"version {m['version']} needs {f}, which was vacuumed")
            rows += json.load(open(p))
        return rows
    def vacuum(self, keep_last_n):
        """Delete data files that no kept version references (like VACUUM / expire_snapshots)."""
        keep = {f for m in self.log[-keep_last_n:] for f in m["files"]}
        gone = [f for f in os.listdir(self.root) if f not in keep]
        for f in gone: os.remove(os.path.join(self.root, f))
        return sorted(gone)

t = ToyTable(tempfile.mkdtemp(prefix="toy_", dir="/tmp/claude-0"))
v0 = t.commit(add=[[{"id": 1, "amt": 10}, {"id": 2, "amt": 20}]]); time.sleep(0.05); mid = time.time(); time.sleep(0.05)
v1 = t.commit(add=[[{"id": 3, "amt": 30}]])
v2 = t.commit(add=[[{"id": 1, "amt": 10}, {"id": 2, "amt": 25}]], remove=["data-v0-0.json"])   # rewrite file: id 2 amt 20 -> 25
print("v0 rows:", len(t.read(0)), "| v1 rows:", len(t.read(1)), "| v2 rows:", len(t.read(2)))
print("as of timestamp 'mid' ->", [r["id"] for r in t.read(ts=mid)], "(version", max(m["version"] for m in t.log if m["ts"] <= mid), ")")
print("train snapshot = version 1 ids/amt:", [(r["id"], r["amt"]) for r in t.read(1)])
print("vacuum keeping only the latest version deletes:", t.vacuum(keep_last_n=1))
print("latest still fine:", [(r["id"], r["amt"]) for r in t.read()])
for v in (1, 0):
    try: t.read(v)
    except FileNotFoundError as e: print(f"time travel to v{v} ->", e)
```
```bash
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
python3 -I "$D/toy_table.py"
```
**Output (my run):** Real run of the toy. It shows retention behaviour, not any real table format.
```text
v0 rows: 2 | v1 rows: 3 | v2 rows: 3
as of timestamp 'mid' -> [1, 2] (version 0 )
train snapshot = version 1 ids/amt: [(1, 10), (2, 20), (3, 30)]
vacuum keeping only the latest version deletes: ['data-v0-0.json']
latest still fine: [(3, 30), (1, 10), (2, 25)]
time travel to v1 -> version 1 needs data-v0-0.json, which was vacuumed
time travel to v0 -> version 0 needs data-v0-0.json, which was vacuumed
```
Not executed: Delta Lake, Iceberg, lakeFS, Spark. Validation that did run: the toy table reproduces the snapshot, timestamp lookup and vacuum failure logic.
**Follow-ups:**
- *Can I combine them?* Yes: Delta table for features, and a DVC pointer to an exported Parquet snapshot for each training run.
- *Why not keep everything forever?* Storage cost and deletion duties (for example a data-protection request). Plan retention and deletion together.
- *Timestamp or version?* Version number is exact; a timestamp depends on clocks and commit times.
**Common mistakes:**
- Assuming time travel is a backup. It stops at the retention window.
- Pinning only the table name and not the version or snapshot id in the training record.
- Running vacuum with a very short retention to save space, with a long-running job still reading.
