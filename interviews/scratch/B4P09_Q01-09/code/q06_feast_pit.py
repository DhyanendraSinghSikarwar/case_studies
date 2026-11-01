# Q6: the same data through Feast get_historical_features. Run in the feast venv.
import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, __import__("pathlib").Path(__file__).parent.as_posix())
import pandas as pd
from feast import FeatureStore
from feast_common import make_repo
feat = pd.DataFrame({
    "user_id": [1, 1, 1, 2, 2],
    "event_ts": pd.to_datetime(["2026-01-01", "2026-01-03", "2026-01-06", "2026-01-02", "2026-01-05"]),
    "txn_count_7d": [3, 5, 9, 1, 4], "avg_amount_7d": [1.0] * 5})
repo = make_repo(sys.argv[1], feat, ttl_days=30, project="q06")
fs = FeatureStore(repo_path=str(repo))
ent = pd.DataFrame({"user_id": [1, 1, 2, 2],
    "event_timestamp": pd.to_datetime(["2026-01-02", "2026-01-04", "2026-01-03", "2026-01-01"], utc=True)})
out = fs.get_historical_features(entity_df=ent, features=["user_stats:txn_count_7d"]).to_df()
print(out.sort_values(["event_timestamp", "user_id"]).to_string(index=False))
