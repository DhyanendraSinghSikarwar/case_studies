"""Feature: number of events per user in the window (now - W, now]. Two code paths: batch and online."""
import os
from bisect import bisect_right, insort
from collections import defaultdict, deque

W = 3600  # seconds
BUG = os.environ.get("FEATURE_BUG", "none")   # "none" | "boundary" | "unsorted"  (seeded bugs for the demo)

def batch_count(events, user, now):
    """Offline path: recompute from the raw log. Slow but obviously right. Oracle for tests."""
    return sum(1 for e in events if e["user"] == user and now - W < e["ts"] <= now)

class OnlineCounter:
    """Online path: incremental state per user."""
    def __init__(self):
        self.ts = defaultdict(list) if BUG != "unsorted" else defaultdict(deque)

    def update(self, e):
        if BUG == "unsorted":
            self.ts[e["user"]].append(e["ts"])      # assumes events arrive in time order
        else:
            insort(self.ts[e["user"]], e["ts"])     # tolerates out-of-order arrival

    def get(self, user, now):
        if BUG == "unsorted":
            d = self.ts[user]
            while d and d[0] <= now - W:            # evict from the left, assumes sorted
                d.popleft()
            return sum(1 for t in d if t <= now)
        lst = self.ts[user]
        lo = bisect_right(lst, now - W - (1 if BUG == "boundary" else 0))   # boundary bug: keeps t == now-W
        hi = bisect_right(lst, now)
        return hi - lo

REQUIRED = {"user": str, "ts": int, "amount": float}

def schema_errors(e):
    errs = [f"missing {k}" for k in REQUIRED if k not in e]
    errs += [f"bad type {k}" for k, t in REQUIRED.items() if k in e and not isinstance(e[k], t)]
    if isinstance(e.get("user"), str) and not e["user"]:
        errs.append("empty user")
    return errs

def freshness_ok(last_event_ts, now, max_lag=900):
    return now - last_event_ts <= max_lag
