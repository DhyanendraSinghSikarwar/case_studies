# usage: python lineage.py <registered-model> <version>
import subprocess, sys, yaml
import mlflow
from mlflow import MlflowClient
mlflow.set_tracking_uri("sqlite:///mlflow.db")
name, ver = sys.argv[1], sys.argv[2]
c = MlflowClient()
mv = c.get_model_version(name, ver)
run = c.get_run(mv.run_id)
sha = mv.tags["git_sha"]
# ask Git what data.csv.dvc said AT THAT COMMIT, and compare with the tag
blob = subprocess.run(["git", "show", f"{sha}:data.csv.dvc"], capture_output=True, text=True).stdout
git_md5 = yaml.safe_load(blob)["outs"][0]["md5"]
print(f"model        : {name} v{ver}  (run {mv.run_id[:8]})")
print(f"git commit   : {sha[:10]}  dirty={run.data.tags['git_dirty']}")
print(f"data md5 tag : {mv.tags['dvc_data_md5']}")
print(f"data md5 git : {git_md5}   match={git_md5 == mv.tags['dvc_data_md5']}")
print(f"params       : {run.data.params}")
print(f"logged input : {[ (d.dataset.name, d.dataset.digest) for d in run.inputs.dataset_inputs ]}")
