import os, sys
os.environ["MLFLOW_DISABLE_TELEMETRY"] = "true"
sys.path.insert(0, ".")
import mlflow
from mlflow import MlflowClient
from approve import PromotionRefused, approve, promote
uri = "sqlite:////tmp/claude-0/b7_q21_30/q24/m.db"
mlflow.set_tracking_uri(uri); mlflow.set_registry_uri(uri)
c = MlflowClient(uri, uri)
c.create_registered_model("churn")
mv = c.create_model_version("churn", source="file:///tmp/none", tags={"author": "asha"})
print("registered churn v%s author=asha" % mv.version)
try:
    approve(c, "churn", mv.version, "asha", "https://ci.example/gate-report/55", 9001)
except PromotionRefused as e:
    print("REFUSED:", e)
t = approve(c, "churn", mv.version, "ravi", "https://ci.example/gate-report/55", 9001)
promote(c, "churn", mv.version)
tags = c.get_model_version("churn", mv.version).tags
for k in sorted(tags):
    print(f"  {k} = {tags[k] if k != 'approved_at' else '<utc timestamp>'}")
print("champion ->", c.get_model_version_by_alias("churn", "champion").version)
