# Q8: materialize vs materialize-incremental, idempotency, late rows. Feast 0.67 local, SQLite online store.
import sys, warnings, logging, os, io, contextlib; warnings.filterwarnings("ignore")
sys.path.insert(0, __import__("pathlib").Path(__file__).parent.as_posix())
from datetime import datetime, timezone
import pandas as pd
from feast import FeatureStore
from feast_common import make_repo, write_rows
U = lambda *a: datetime(*a, tzinfo=timezone.utc)
base = pd.DataFrame({"user_id": [1, 1, 2], "event_ts": pd.to_datetime(["2026-01-01", "2026-01-03", "2026-01-02"]),
                     "txn_count_7d": [3, 8, 1], "avg_amount_7d": [1.0, 1.0, 1.0]})
repo = make_repo(sys.argv[1], base, ttl_days=30, project="q08")
fs = FeatureStore(repo_path=str(repo))
F = ["user_stats:txn_count_7d"]
def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): fn(*a, **k)
def online(*users):
    d = fs.get_online_features(features=F, entity_rows=[{"user_id": u} for u in users]).to_dict()
    return dict(zip(d["user_id"], d["txn_count_7d"]))
def intervals():
    return [(a.date().isoformat(), b.date().isoformat()) for a, b in fs.get_feature_view("user_stats").materialization_intervals]

print("1. materialize 2026-01-01 .. 2026-01-04   ->", end=" "); quiet(fs.materialize, U(2026,1,1), U(2026,1,4)); print(online(1, 2, 3))
print("2. same command again (idempotent)       ->", end=" "); quiet(fs.materialize, U(2026,1,1), U(2026,1,4)); print(online(1, 2, 3))
print("   registry intervals after plain materialize:", intervals())

print("3. replay an OLD window 01-01..01-02 after newer data is online ->", end=" ")
quiet(fs.materialize, U(2026,1,1), U(2026,1,2)); print(online(1, 2, 3))

# late row: user 3, event time Jan 2 (inside the window we already ran), arrives after the run
late = pd.concat([base, pd.DataFrame({"user_id": [3], "event_ts": pd.to_datetime(["2026-01-02"]), "txn_count_7d": [7], "avg_amount_7d": [1.0]})])
write_rows(repo, late)
print("4. late row for user 3 (event 01-02) lands")
quiet(fs.materialize_incremental, end_date=U(2026,1,6))
print("   materialize-incremental to 01-06      ->", online(3))
print("   registry intervals now:", intervals())
quiet(fs.materialize, U(2026,1,1), U(2026,1,6))
print("   explicit overlapping window 01-01..06 ->", online(1, 2, 3))
