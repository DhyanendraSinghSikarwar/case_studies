"""Q31: event-time vs ingestion-time as-of joins on a late row and a correction. No randomness."""
import pandas as pd

T = pd.Timestamp
# feature log: one row per (entity, event_time, ingest_time); value = last_txn_amount
log = pd.DataFrame([
    # user 1: normal row, then a row that happened at 12:00 but arrived 6 hours late (18:00)
    (1, T("2026-01-01 10:00"), T("2026-01-01 10:05"), 100),
    (1, T("2026-01-01 12:00"), T("2026-01-01 18:00"), 500),   # LATE ROW
    # user 2: row, then a correction of the SAME event, ingested a week later
    (2, T("2026-01-01 09:00"), T("2026-01-01 09:01"), 10),
    (2, T("2026-01-01 09:00"), T("2026-01-08 08:00"), 12),    # CORRECTION (new version)
], columns=["user", "event_time", "ingest_time", "value"])

# prediction moments (what the model was asked, and when)
asks = pd.DataFrame([
    (1, T("2026-01-01 13:00")),   # 1h after the late row happened, 5h before it arrived
    (1, T("2026-01-02 09:00")),   # next day: late row is known by now
    (2, T("2026-01-02 09:00")),   # before the correction was ingested
], columns=["user", "ask_time"])

def as_of(user, ask_time, use_ingest):
    r = log[(log.user == user) & (log.event_time <= ask_time)]
    if use_ingest:                       # only rows the system KNEW at ask_time
        r = r[r.ingest_time <= ask_time]
    if r.empty:
        return None
    # latest event wins; for same event the latest ingested version wins
    return r.sort_values(["event_time", "ingest_time"]).iloc[-1].value

out = asks.copy()
out["A_event_time_only(today)"] = [as_of(u, t, False) for u, t in zip(asks.user, asks.ask_time)]
out["B_event+ingest(knowledge)"] = [as_of(u, t, True) for u, t in zip(asks.user, asks.ask_time)]
def served_in_prod(user, ask_time):
    """Replay the online store: apply rows in arrival order, keep the newest event, read at ask_time."""
    store = {}
    for r in log.sort_values("ingest_time").itertuples():
        if r.ingest_time > ask_time:
            break
        if r.user not in store or r.event_time >= store[r.user][0]:
            store[r.user] = (r.event_time, r.value)
    return store[user][1]

out["served_in_prod"] = [served_in_prod(u, t) for u, t in zip(asks.user, asks.ask_time)]
out["A_leaks"] = out["A_event_time_only(today)"] != out["served_in_prod"]
out["B_matches_prod"] = out["B_event+ingest(knowledge)"] == out["served_in_prod"]
pd.set_option("display.width", 200)
print(out.to_string(index=False))
