import warnings, os, json, tempfile; warnings.filterwarnings("ignore")
import azure.ai.ml as m
from azure.ai.ml import command, Input, Output, load_job
from azure.ai.ml.exceptions import ValidationException
print("azure-ai-ml", m.__version__)
d = tempfile.mkdtemp(); os.makedirs(f"{d}/src")
open(f"{d}/src/train.py", "w").write("print('train')\n")
JOB = """\
$schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
display_name: train-demo
experiment_name: churn-exp
code: ./src
command: python train.py --data ${{inputs.data}} --lr ${{inputs.lr}} --out ${{outputs.model_out}}
inputs:
  data:
    type: uri_folder
    path: azureml://datastores/workspaceblobstore/paths/churn/v1/
  lr: 0.1
outputs:
  model_out:
    type: uri_folder
environment: azureml:sklearn-env:1
compute: azureml:cpu-cluster
"""
open(f"{d}/job.yml", "w").write(JOB)
os.chdir(d)
y = load_job("job.yml")
r = y._validate()
print("YAML job:", type(y).__name__, "| validate passed:", r.passed)

s = command(
    display_name="train-demo", experiment_name="churn-exp", code="./src",
    command="python train.py --data ${{inputs.data}} --lr ${{inputs.lr}} --out ${{outputs.model_out}}",
    inputs={"data": Input(type="uri_folder", path="azureml://datastores/workspaceblobstore/paths/churn/v1/"), "lr": 0.1},
    outputs={"model_out": Output(type="uri_folder")},
    environment="azureml:sklearn-env:1", compute="azureml:cpu-cluster")
print("SDK job validate passed:", s._validate().passed)

dy, ds = y._to_dict(), s._to_dict()
for k in ("code", "environment"):          # code is resolved to an absolute temp path
    dy.pop(k, None); ds.pop(k, None)
print("dicts equal (ignoring code and environment):", dy == ds)
print("diff keys:", sorted(k for k in set(dy) | set(ds) if dy.get(k) != ds.get(k)))
print("top-level keys:", sorted(dy))
print(json.dumps({k: dy[k] for k in ("inputs", "outputs") if k in dy}, indent=1))

# misspelt key
open("bad.yml", "w").write(JOB.replace("inputs:", "inptus:", 1))
try:
    load_job("bad.yml")
except Exception as e:
    print("misspelt key ->", type(e).__name__, "|", " ".join(str(e).split())[:230])
# a command that references an input that does not exist
open("bad2.yml", "w").write(JOB.replace("${{inputs.lr}}", "${{inputs.learning_rate}}"))
try:
    r2 = load_job("bad2.yml")._validate()
    print("bad reference validate passed:", r2.passed, "|", getattr(r2, "error_messages", ""))
except Exception as e:
    print("bad reference ->", type(e).__name__, str(e)[:160])
