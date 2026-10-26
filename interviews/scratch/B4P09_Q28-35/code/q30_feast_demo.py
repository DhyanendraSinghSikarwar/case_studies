"""Q30: tiny local Feast run (file offline store + SQLite online store). Own repo dir passed as argv[1]."""
import sys, os, shutil, warnings
from datetime import datetime, timedelta
import pandas as pd
warnings.filterwarnings("ignore")

repo = sys.argv[1]
shutil.rmtree(repo, ignore_errors=True)
os.makedirs(repo + "/data")

with open(repo + "/feature_store.yaml", "w") as f:
    f.write(f"""project: q30demo
provider: local
registry: {repo}/data/registry.db
online_store:
  type: sqlite
  path: {repo}/data/online.db
offline_store:
  type: file
entity_key_serialization_version: 3
""")

pd.DataFrame({
    "user_id": [1, 1, 1, 2],
    "event_timestamp": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-04", "2026-01-01"], utc=True),
    "txn_count_7d": [3, 5, 9, 1],
}).to_parquet(repo + "/data/stats.parquet")

from feast import FeatureStore, Entity, FeatureView, Field, FileSource
from feast.types import Int64
from feast.value_type import ValueType

user = Entity(name="user", join_keys=["user_id"], value_type=ValueType.INT64)
src = FileSource(path=repo + "/data/stats.parquet", timestamp_field="event_timestamp")
fv = FeatureView(name="user_stats", entities=[user], ttl=timedelta(days=3),
                 schema=[Field(name="txn_count_7d", dtype=Int64)], source=src)

store = FeatureStore(repo_path=repo)
store.apply([user, fv])
print("registry has:", [v.name for v in store.list_feature_views()])

req = pd.DataFrame({"user_id": [1, 1, 2],
                    "event_timestamp": pd.to_datetime(["2026-01-03", "2026-01-10", "2026-01-02"], utc=True)})
hist = store.get_historical_features(entity_df=req, features=["user_stats:txn_count_7d"]).to_df()
print("historical (offline, as-of, ttl=3d):")
print(hist.sort_values(["user_id", "event_timestamp"]).to_string(index=False))

store.materialize(start_date=datetime(2025, 12, 1), end_date=datetime(2026, 1, 5))
online = store.get_online_features(features=["user_stats:txn_count_7d"],
                                   entity_rows=[{"user_id": 1}, {"user_id": 2}, {"user_id": 99}]).to_dict()
print("online (latest value materialised):", online)
