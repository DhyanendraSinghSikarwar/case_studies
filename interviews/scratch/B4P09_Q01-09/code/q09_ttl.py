# Q9: TTL offline and online in Feast 0.67 (local provider, file offline store, SQLite online store). ttl = 2 days.
import sys, warnings, io, contextlib; warnings.filterwarnings("ignore")
sys.path.insert(0, __import__("pathlib").Path(__file__).parent.as_posix())
from datetime import datetime, timedelta, timezone
import pandas as pd
from feast import FeatureStore
from feast_common import make_repo
pd.set_option("display.width", 200)
F = ["user_stats:txn_count_7d"]

# ---- offline: label time 2026-01-10 00:00; feature ages: 1 day, exactly 2 days, 2 days + 1 min, none at all
T = pd.Timestamp("2026-01-10", tz="UTC")
ages = {1: timedelta(days=1), 2: timedelta(days=2), 3: timedelta(days=2, minutes=1)}
feat = pd.DataFrame({"user_id": list(ages), "event_ts": [(T - a).tz_localize(None) for a in ages.values()],
                     "txn_count_7d": [10, 20, 30], "avg_amount_7d": [1.0] * 3})
repo = make_repo(sys.argv[1] + "/offline", feat, ttl_days=2, project="q09off")
fs = FeatureStore(repo_path=str(repo))
ent = pd.DataFrame({"user_id": [1, 2, 3, 4], "event_timestamp": [T] * 4})
out = fs.get_historical_features(entity_df=ent, features=F).to_df()
print("OFFLINE: asked for 4 users, got", len(out), "rows back")
print(out.sort_values("user_id").to_string(index=False))
print("users with no row in the output:", sorted(set(ent.user_id) - set(out.user_id)))

# ---- online: timestamps relative to the real clock so 'now' matters
now = datetime.now(timezone.utc).replace(tzinfo=None)
ages2 = {1: timedelta(hours=1), 2: timedelta(days=1), 3: timedelta(days=3)}
feat2 = pd.DataFrame({"user_id": list(ages2), "event_ts": [now - a for a in ages2.values()],
                      "txn_count_7d": [10, 20, 30], "avg_amount_7d": [1.0] * 3})
repo2 = make_repo(sys.argv[1] + "/online", feat2, ttl_days=2, project="q09on")
fs2 = FeatureStore(repo_path=str(repo2))
with contextlib.redirect_stdout(io.StringIO()):
    fs2.materialize(start_date=datetime.now(timezone.utc) - timedelta(days=10), end_date=datetime.now(timezone.utc) + timedelta(hours=1))
d = fs2.get_online_features(features=F, entity_rows=[{"user_id": u} for u in (1, 2, 3, 4)]).to_dict()
print("\nONLINE (ttl 2 days; value ages 1 hour, 1 day, 3 days, no row)")
print(pd.DataFrame(d).to_string(index=False))

# ---- freshness SLO check done by us (the online read did not enforce ttl): age of the newest source row per user
SLO = timedelta(hours=26)          # example SLO for a daily-refreshed feature: 24 h + 2 h slack
newest = feat2.groupby("user_id").event_ts.max()
age = (now - newest)
rep = pd.DataFrame({"user_id": newest.index, "age_hours": (age.dt.total_seconds() / 3600).round(1).values,
                    "within_slo": (age <= SLO).values})
print("\nFRESHNESS CHECK (SLO 26 h)"); print(rep.to_string(index=False))
