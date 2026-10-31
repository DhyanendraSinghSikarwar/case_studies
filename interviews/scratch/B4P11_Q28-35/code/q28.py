# q28.py - v2 command job as target state, loaded and validated offline (no workspace, no network)
import sys, os, tempfile, warnings, logging
warnings.filterwarnings("ignore"); logging.disable(logging.CRITICAL)
import azure.ai.ml as m
from azure.ai.ml import load_job
print("azure-ai-ml", m.__version__)
root = sys.argv[1]; os.makedirs(os.path.join(root, "src"), exist_ok=True)
open(os.path.join(root, "src", "train.py"), "w").write("print('train')\n")
JOB = """\
$schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
display_name: train-churn
experiment_name: churn
code: ./src
command: python train.py --data ${{inputs.training_data}} --lr ${{inputs.lr}}
inputs:
  training_data:
    type: uri_folder
    path: azureml:churn-data:1
  lr: 0.1
environment: azureml:sklearn-env:3
compute: azureml:cpu-cluster
"""
p = os.path.join(root, "job.yml"); open(p, "w").write(JOB)
job = load_job(p)
print("loaded:", type(job).__name__, "| compute:", job.compute, "| env:", job.environment)
print("input keys:", sorted(job.inputs))
job._validate()
print("validate: OK")
bad = JOB.replace("inputs:", "inptus:", 1)
open(os.path.join(root, "bad.yml"), "w").write(bad)
try:
    load_job(os.path.join(root, "bad.yml"))._validate()
    print("bad: no error")
except Exception as e:
    print("bad job ->", type(e).__name__, "|", str(e).replace("\n", " ")[:160])
