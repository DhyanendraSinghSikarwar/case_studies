import warnings, os, tempfile, json; warnings.filterwarnings("ignore")
import azure.ai.ml as m
from azure.ai.ml import command, Input, Output, load_job, load_component
from azure.ai.ml.dsl import pipeline
print("azure-ai-ml", m.__version__)
d = tempfile.mkdtemp(); os.makedirs(f"{d}/src"); os.chdir(d)
for n in ("prep", "train"):
    open(f"src/{n}.py", "w").write("pass\n")
open("prep.yml", "w").write("""\
$schema: https://azuremlschemas.azureedge.net/latest/commandComponent.schema.json
type: command
name: prep
version: "1"
code: ./src
command: python prep.py --raw ${{inputs.raw}} --out ${{outputs.clean}}
inputs:
  raw: {type: uri_folder}
outputs:
  clean: {type: uri_folder}
environment: azureml:sklearn-env:1
""")
open("train.yml", "w").write("""\
$schema: https://azuremlschemas.azureedge.net/latest/commandComponent.schema.json
type: command
name: train
version: "1"
code: ./src
command: python train.py --data ${{inputs.data}} --lr ${{inputs.lr}} --model ${{outputs.model}}
inputs:
  data: {type: uri_folder}
  lr: {type: number, default: 0.1}
outputs:
  model: {type: uri_folder}
environment: azureml:sklearn-env:1
is_deterministic: true
""")
PIPE = """\
$schema: https://azuremlschemas.azureedge.net/latest/pipelineJob.schema.json
type: pipeline
display_name: churn-pipe
settings:
  default_compute: azureml:cpu-cluster
inputs:
  raw_data: {type: uri_folder, path: azureml://datastores/workspaceblobstore/paths/raw/}
  lr: 0.05
jobs:
  prep_step:
    type: command
    component: ./prep.yml
    inputs:
      raw: ${{parent.inputs.raw_data}}
  train_step:
    type: command
    component: ./train.yml
    inputs:
      data: ${{parent.jobs.prep_step.outputs.clean}}
      lr: ${{parent.inputs.lr}}
    outputs:
      model: ${{parent.outputs.final_model}}
outputs:
  final_model: {type: uri_folder}
"""
open("pipe.yml", "w").write(PIPE)
p = load_job("pipe.yml")
print("YAML pipeline:", type(p).__name__, "steps:", list(p.jobs), "validate passed:", p._validate().passed)

prep, train = load_component("prep.yml"), load_component("train.yml")
@pipeline(default_compute="cpu-cluster")
def churn(raw_data, lr: float = 0.05):
    a = prep(raw=raw_data)
    b = train(data=a.outputs.clean, lr=lr)
    return {"final_model": b.outputs.model}
sp = churn(raw_data=Input(type="uri_folder", path="azureml://datastores/workspaceblobstore/paths/raw/"))
print("SDK pipeline steps:", list(sp.jobs), "| validate passed:", sp._validate().passed)
print("train component is_deterministic (reuse allowed):", train.is_deterministic)

# What validation catches
open("bad_pipe.yml", "w").write(PIPE.replace("${{parent.jobs.prep_step.outputs.clean}}", "${{parent.jobs.prep_step.outputs.cleen}}"))
r = load_job("bad_pipe.yml")._validate()
print("misspelt step output -> passed:", r.passed, "|", [" ".join(str(x).split())[:110] for x in (r.error_messages.values() if isinstance(getattr(r, 'error_messages', None), dict) else [])][:2])
open("bad_pipe2.yml", "w").write(PIPE.replace("./train.yml", "./missing.yml"))
try:
    r = load_job("bad_pipe2.yml")._validate(); print("missing component file -> passed:", r.passed)
except Exception as e:
    print("missing component file ->", type(e).__name__, "|", " ".join(str(e).split())[:140])
print("NOT caught offline: compute 'cpu-cluster' exists, environment azureml:sklearn-env:1 exists, quota, data path readable, script runs.")
