import pandas as pd
# one shared feature function used by BOTH training and serving
def txn_features(events: pd.DataFrame, now: pd.Timestamp) -> dict:
    w = events[(events.ts > now - pd.Timedelta("1h")) & (events.ts <= now)]
    return {"cnt_1h": len(w), "amt_1h": float(w.amount.sum())}
ev = pd.DataFrame({"ts": pd.to_datetime(["2026-01-01 10:00","2026-01-01 10:20","2026-01-01 10:50","2026-01-01 11:30"]),
                   "amount": [100, 250, 40, 900]})
now = pd.Timestamp("2026-01-01 11:00")
print(txn_features(ev, now))   # training: replay at event time; serving: same call at request time
