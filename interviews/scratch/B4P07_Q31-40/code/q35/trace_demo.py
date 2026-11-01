"""Simulate a CI run stamping lineage on a model version, then answer 'who made the model that scored this loan?'."""
import os, tempfile
from mlflow import MlflowClient

LINEAGE_ENV = {"GITHUB_SHA": "git_sha", "GITHUB_RUN_ID": "gha_run_id", "GITHUB_WORKFLOW": "gha_workflow",
               "GITHUB_REPOSITORY": "gha_repo", "DATA_VERSION": "data_version", "IMAGE_DIGEST": "image_digest"}

def stamp(client, name, version):
    missing = [k for k in LINEAGE_ENV if not os.environ.get(k)]
    if missing:                                    # fail loudly: a version without lineage is not releasable
        raise SystemExit(f"missing lineage env vars: {missing}")
    for env_name, tag in LINEAGE_ENV.items():
        client.set_model_version_tag(name, version, tag, os.environ[env_name])

def lineage(client, name, version):
    return dict(client.get_model_version(name, str(version)).tags)

def predict(client, name, features):               # stand-in for the API: always return model_version
    v = client.get_model_version_by_alias(name, "champion").version
    return {"score": 0.37, "model_name": name, "model_version": str(v)}

d = tempfile.mkdtemp()
uri = f"sqlite:///{d}/m.db"
c = MlflowClient(tracking_uri=uri, registry_uri=uri)
c.create_registered_model("credit-risk")
c.create_model_version("credit-risk", source=d)
c.create_model_version("credit-risk", source=d)

# CI run for version 2 (values a workflow would get from the runner / earlier steps)
os.environ.update({"GITHUB_SHA": "ab12cd34ef56ab12cd34ef56ab12cd34ef56ab12", "GITHUB_RUN_ID": "9876543210",
                   "GITHUB_WORKFLOW": "train-and-register", "GITHUB_REPOSITORY": "example-org/credit-risk",
                   "DATA_VERSION": "data.20261001", "IMAGE_DIGEST": "sha256:bbbb2222"})
stamp(c, "credit-risk", 2)
c.set_registered_model_alias("credit-risk", "champion", 2)

resp = predict(c, "credit-risk", {"income": 5})      # the loan scoring response stored with the decision
print("API response:", resp)
print("lineage of that version:")
for k, v in sorted(lineage(c, resp["model_name"], resp["model_version"]).items()):
    print(f"  {k:<14} {v}")

del os.environ["IMAGE_DIGEST"]
try:
    stamp(c, "credit-risk", 1)
except SystemExit as e:
    print("refused:", e)
