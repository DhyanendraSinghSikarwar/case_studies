# One feature, "spend_today per user", written twice (batch team and streaming team).
from datetime import datetime, timezone, timedelta
from collections import defaultdict

IST = timezone(timedelta(hours=5, minutes=30))
def ts(s): return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)

events = [  # (user, utc timestamp, amount, kind)
    ("u1", ts("2025-03-01T10:00:00"), 100.0, "purchase"),
    ("u1", ts("2025-03-01T20:00:00"),  50.0, "purchase"),   # 01:30 IST next day
    ("u1", ts("2025-03-01T21:00:00"),  30.0, "refund"),     # refund, stored as positive amount
    ("u2", ts("2025-03-01T09:00:00"),  None, "purchase"),   # missing amount
    ("u2", ts("2025-03-01T11:00:00"),  70.0, "purchase"),
    ("u3", ts("2025-03-02T00:30:00"),  20.0, "purchase"),
]

# --- Codebase 1: batch (analyst SQL-style): business day in IST, refunds subtract, nulls skipped
def batch_spend(events):
    out = defaultdict(float)
    for u, t, amt, kind in events:
        if amt is None: continue
        sign = -1 if kind == "refund" else 1
        out[(u, t.astimezone(IST).date().isoformat())] += sign * amt
    return dict(out)

# --- Codebase 2: streaming (engineer, per-key state): UTC day, refunds ignored, null -> 0
def stream_spend(events):
    out = defaultdict(float)
    for u, t, amt, kind in events:
        if kind == "refund": continue
        out[(u, t.date().isoformat())] += (amt or 0.0)
    return dict(out)

b, s = batch_spend(events), stream_spend(events)
print("key               batch  stream  agree")
for k in sorted(set(b) | set(s)):
    print(f"{str(k):28s} {b.get(k, 0):6.1f} {s.get(k, 0):6.1f}  {b.get(k, 0) == s.get(k, 0)}")

# --- Fix: one shared definition, imported by BOTH the batch job and the stream job
def contribution(user, t, amt, kind):
    """The single definition: (key, signed amount). IST business day, refunds subtract, null skipped."""
    if amt is None: return None
    return (user, t.astimezone(IST).date().isoformat()), (-amt if kind == "refund" else amt)

def run_batch_shared(evts):       # batch calls it over a full list
    out = defaultdict(float)
    for e in evts:
        c = contribution(*e)
        if c: out[c[0]] += c[1]
    return dict(out)

class StreamState:                # stream calls the SAME function one event at a time
    def __init__(self): self.s = defaultdict(float)
    def on_event(self, e):
        c = contribution(*e)
        if c: self.s[c[0]] += c[1]

st = StreamState()
for e in events: st.on_event(e)
print("after fix, batch == stream:", run_batch_shared(events) == dict(st.s))
print("values:", dict(sorted(st.s.items())))
