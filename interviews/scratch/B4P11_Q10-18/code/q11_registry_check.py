"""Q11: registry entry validator + a promotion convention per cloud. Pure Python; runs in any venv."""
import re

# Convention (mine, not a vendor rule): stage lives in an alias (Vertex, MLflow) or a tag (Azure ML),
# never in the model name, and a prod entry needs an approver and a source run.
CONVENTION = {
    "azure_ml": {"stage_carrier": "tag  stage=dev|staging|prod", "immutable": "name:version", "pointer": "azureml:churn:7"},
    "vertex":   {"stage_carrier": "version alias dev|staging|prod (moves)", "immutable": "model id + version id", "pointer": "projects/P/locations/R/models/ID@prod"},
    "mlflow":   {"stage_carrier": "registered-model alias (moves)", "immutable": "name + version", "pointer": "models:/churn@prod"},
}
STAGES = {"dev", "staging", "prod"}
NAME_RE = re.compile(r"^[a-z][a-z0-9-]{2,40}$")

def validate(e):
    errs = []
    if not NAME_RE.match(str(e.get("name", ""))):
        errs.append("name must be lowercase-hyphen, no stage in it")
    elif any(s in e["name"].split("-") for s in STAGES):
        errs.append("stage word in model name (use alias/tag instead)")
    if not isinstance(e.get("version"), int) or e["version"] < 1:
        errs.append("version must be an integer >= 1")
    if e.get("stage") not in STAGES:
        errs.append("stage must be one of dev|staging|prod")
    if not e.get("source_run"):
        errs.append("source_run missing (no lineage)")
    if e.get("stage") == "prod" and not e.get("approver"):
        errs.append("prod needs an approver")
    if e.get("stage") == "prod" and e.get("approver") == e.get("registered_by"):
        errs.append("approver must differ from registered_by")
    return errs

samples = {
 "good_staging": dict(name="churn", version=7, stage="staging", source_run="run-8841", registered_by="asha"),
 "good_prod":    dict(name="churn", version=7, stage="prod", source_run="run-8841", registered_by="asha", approver="ravi"),
 "bad_prod_self_approved": dict(name="churn", version=8, stage="prod", source_run="run-9", registered_by="asha", approver="asha"),
 "bad_stage_in_name": dict(name="churn-prod", version=3, stage="prod", source_run="run-5", registered_by="asha", approver="ravi"),
 "bad_name_and_run": dict(name="Churn-Prod", version=0, stage="prod", registered_by="asha", approver="ravi"),
}
for k, v in samples.items():
    errs = validate(v)
    print(f"{k:24s}", "OK" if not errs else "FAIL " + "; ".join(errs))
