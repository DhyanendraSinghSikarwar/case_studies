# Feast 0.67.0 (own venv, own repo under /tmp/claude-0/b9_q10_18). Registry is a local file.
import sys, os, shutil, tempfile
from datetime import datetime, timedelta, timezone
import pandas as pd
W = tempfile.mkdtemp(prefix="q15_", dir="/tmp/claude-0/b9_q10_18"); os.makedirs(W + "/data")
shutil.copy("/tmp/claude-0/b9_q10_18/feast_repo/feature_store.yaml", W); shutil.copy("/tmp/claude-0/b9_q10_18/feast_repo/defs.py", W)
os.chdir(W); sys.path.insert(0, W)
t0 = datetime(2026, 3, 1, tzinfo=timezone.utc)
pd.DataFrame({"card_id": [1, 2], "event_ts": [t0, t0], "txn_count_1h": [3, 1], "avg_amt_24h": [20.0, 5.0]}).to_parquet("data/card_stats.parquet")
import defs, feast
from feast import FeatureStore, FeatureView, Field
from feast.types import Float32, Int64
print("feast", feast.__version__)
fs = FeatureStore(".")
fs.apply([defs.card, defs.card_velocity_v1])

print("--- registry contents")
for e in fs.list_entities(): print("entity      ", e.name, "| owner:", e.owner)
for fv in fs.list_feature_views():
    print("feature view", fv.name, "| owner:", fv.owner, "| ttl:", fv.ttl, "| entities:", fv.entities)
    print("   tags:", dict(fv.tags))
    for f in fv.schema: print("   feature:", f.name, f.dtype, "|", f.description)
    print("   source:", fv.batch_source.path if hasattr(fv.batch_source, "path") else fv.batch_source)

print("--- find by tag (client-side filter)")
print([fv.name for fv in fs.list_feature_views() if fv.tags.get("team") == "fraud" and fv.tags.get("pii") == "false"])

print("--- version bump: change window semantics, new name card_velocity_v2, keep v1 for old models")
v2 = FeatureView(name="card_velocity_v2", entities=[defs.card], ttl=timedelta(days=1), source=defs.src,
    schema=[Field(name="txn_count_1h", dtype=Int64, description="Window [t-1h, t) excluding current event"),
            Field(name="avg_amt_24h", dtype=Float32)],
    owner="fraud-ml@example.com", description="Card velocity features, window fixed",
    tags={"team": "fraud", "pii": "false", "freshness_slo": "5m", "transform_version": "2", "status": "active"})
fs.apply([v2])
print([ (fv.name, fv.tags["transform_version"], fv.tags["status"]) for fv in fs.list_feature_views()])
v1 = fs.get_feature_view("card_velocity_v1"); v1.tags["status"] = "deprecated"; v1.tags["replaced_by"] = "card_velocity_v2"
fs.apply([v1])
print("after deprecating v1:", [(fv.name, fv.tags["status"]) for fv in fs.list_feature_views()])
print("(without full_feature_names=True Feast 0.67 raises FeatureNameCollisionError: same short name in two views)")
print("both still servable offline:", fs.get_historical_features(
    pd.DataFrame({"card_id": [1], "event_timestamp": [t0 + timedelta(hours=1)]}),
    features=["card_velocity_v1:txn_count_1h", "card_velocity_v2:txn_count_1h"], full_feature_names=True).to_df().to_dict("records"))
shutil.rmtree(W, ignore_errors=True)
