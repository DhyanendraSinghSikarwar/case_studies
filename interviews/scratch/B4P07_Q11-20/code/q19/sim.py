"""Replay the stale-run race on a sqlite registry (own temp db)."""
import sys, tempfile, os
from mlflow import MlflowClient
from cas_promote import promote_forward, current

d = tempfile.mkdtemp()
u = f"sqlite:///{d}/m.db"
c = MlflowClient(u, registry_uri=u)
c.create_registered_model("churn")
for i in range(3):
    c.create_model_version("churn", source=f"{d}/x{i}", run_id=None)
print("run B (newer, v3) finishes first:", promote_forward(c, "churn", 3)[1])
print("run A (older, v2) finishes late :", promote_forward(c, "churn", 2)[1])
print("champion is v%s" % current(c, "churn"))
c.set_registered_model_alias("churn", "champion", "2")      # what a naive script would do
print("naive set_registered_model_alias leaves champion at v%s" % current(c, "churn"))
