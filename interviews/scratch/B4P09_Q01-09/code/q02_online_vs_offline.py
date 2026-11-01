# Q2: same entity read from the offline store (history, as-of) and the online store (latest row only).
import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, __import__("pathlib").Path(__file__).parent.as_posix())
from datetime import datetime
import pandas as pd
from feast import FeatureStore
from feast_common import make_repo, write_rows

rows = pd.DataFrame({
    "user_id": [1, 1, 1, 2],
    "event_ts": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-01"]),
    "txn_count_7d": [3, 5, 8, 1],
    "avg_amount_7d": [200.0, 220.0, 260.0, 90.0],
})
repo = make_repo(sys.argv[1], rows, ttl_days=30, project="q02")
fs = FeatureStore(repo_path=str(repo))
F = ["user_stats:txn_count_7d", "user_stats:avg_amount_7d"]

print("== offline: raw history for user 1 (3 rows) ==")
print(rows[rows.user_id == 1][["user_id", "event_ts", "txn_count_7d"]].to_string(index=False))

print("\n== offline: get_historical_features, one row per (entity, label time) ==")
ent = pd.DataFrame({"user_id": [1, 1, 1], "event_timestamp": pd.to_datetime(["2026-01-01 12:00", "2026-01-02 12:00", "2026-01-03 12:00"])})
h = fs.get_historical_features(entity_df=ent, features=F).to_df().sort_values("event_timestamp")
print(h.to_string(index=False))

fs.materialize(start_date=datetime(2025, 12, 31), end_date=datetime(2026, 1, 4))
print("\n== online: get_online_features for user 1 and 2 (latest row only) ==")
o = fs.get_online_features(features=F, entity_rows=[{"user_id": 1}, {"user_id": 2}]).to_dict()
print(pd.DataFrame(o).to_string(index=False))

print("\n== disagreement: a new row lands offline on Jan 4, nobody re-materialises ==")
new = pd.concat([rows, pd.DataFrame({"user_id": [1], "event_ts": pd.to_datetime(["2026-01-04"]), "txn_count_7d": [13], "avg_amount_7d": [300.0]})])
write_rows(repo, new)
off = fs.get_historical_features(entity_df=pd.DataFrame({"user_id": [1], "event_timestamp": pd.to_datetime(["2026-01-04 12:00"])}), features=F).to_df()
on = fs.get_online_features(features=F, entity_rows=[{"user_id": 1}]).to_dict()
print("offline says txn_count_7d =", int(off.txn_count_7d.iloc[0]), "| online says txn_count_7d =", on["txn_count_7d"][0])
