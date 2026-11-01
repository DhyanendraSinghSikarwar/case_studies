import os, sys, tempfile
sys.path.insert(0, os.getcwd())
from mlflow import MlflowClient
from envpromo import promote, PromotionError

d = tempfile.mkdtemp()
uri = f"sqlite:///{d}/m.db"; led = f"{d}/ledger.jsonl"
c = MlflowClient(tracking_uri=uri, registry_uri=uri)
c.create_registered_model("churn")
for _ in range(2):
    c.create_model_version("churn", source=d)
def alias(a):
    try: return c.get_model_version_by_alias("churn", a).version
    except Exception: return None
def show(tag): print(f"{tag:<28} staging={alias('staging')} champion={alias('champion')}")
show("start")
try: promote(c, "churn", 2, "champion", "dhyan", led)
except PromotionError as e: print("refused:", e)
print(promote(c, "churn", 1, "staging", "ci", led)); print(promote(c, "churn", 1, "champion", "ci", led)); show("v1 staging then champion")
print(promote(c, "churn", 2, "staging", "ci", led)); show("v2 in staging")
print(promote(c, "churn", 2, "champion", "ci", led)); show("v2 champion")
print(open(led).read().replace(d, "<tmp>"), end="")
