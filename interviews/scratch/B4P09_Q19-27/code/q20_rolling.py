# Per-key sliding window count (last 60 minutes) in pure Python vs pandas rolling.
from collections import deque, defaultdict
import pandas as pd

# (card, minute-of-day, arrival order is list order). Event 5 (minute 50) arrives late.
events = [("A", 0), ("A", 20), ("A", 60), ("B", 10), ("A", 70), ("A", 50), ("B", 75), ("A", 120)]

# 1) streaming version: arrival order, state = deque of timestamps per key
state = defaultdict(deque)
def on_event(card, t, window=60):
    dq = state[card]
    dq.append(t)                              # naive: assumes timestamps arrive in order
    while dq and dq[0] <= t - window:         # window is (t-60, t]: an event exactly 60 min old is out
        dq.popleft()
    return len(dq)

stream = [on_event(c, t) for c, t in events]

# 2) offline version: sort by event time, pandas rolling (default closed='right' = (t-60, t])
df = pd.DataFrame(events, columns=["card", "t"])
df["arrival"] = range(len(df))
df["ts"] = pd.Timestamp("2025-01-01") + pd.to_timedelta(df["t"], unit="m")
s = df.sort_values("ts").set_index("ts").groupby("card")["arrival"].rolling("60min").count()
# rolling output is indexed by (card, ts); map back to events by (card, ts)
lookup = {(r.card, r.ts): int(r.offline_count) for r in s.reset_index().rename(columns={"arrival": "offline_count"}).itertuples()}
df["stream_count"] = stream
df["offline_count"] = [lookup[(c, ts)] for c, ts in zip(df.card, df.ts)]
df["match"] = df.stream_count == df.offline_count
print(df[["card", "t", "arrival", "stream_count", "offline_count", "match"]].to_string(index=False))
print("disagreements:", int((~df.match).sum()))

# 3) fix the deque bug: keep a sorted buffer per key (insort) so a late event cannot break eviction.
import bisect
buf = defaultdict(list)
def on_event_sorted(card, t, window=60):
    bisect.insort(buf[card], t)
    return sum(1 for x in buf[card] if t - window < x <= t)   # count as of THIS event's own time
fixed = [on_event_sorted(c, t) for c, t in events]

# reference: offline rule applied only to events that had ARRIVED by then (what a stream can know)
def as_of_arrival(i):
    c, t = events[i]
    return sum(1 for cc, tt in events[:i + 1] if cc == c and t - 60 < tt <= t)
ref = [as_of_arrival(i) for i in range(len(events))]
print("sorted-buffer :", fixed)
print("as-of-arrival :", ref, "equal:", fixed == ref)
print("offline (all) :", list(df.offline_count), "-> differs only where a late event had not arrived yet")
