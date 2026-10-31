# Q7: offline pandas rolling feature vs online incremental feature; the parity test that catches a window-boundary bug.
from collections import deque
import numpy as np, pandas as pd

def make_events(seed=3, n=60):
    rng = np.random.default_rng(seed)
    ts = pd.Timestamp("2026-01-01") + pd.to_timedelta(np.sort(rng.integers(0, 20 * 24, n)), unit="h")   # whole hours -> exact 7-day gaps happen
    return pd.DataFrame({"user_id": 1, "ts": ts})

def offline_count_7d(ev):
    """Training path: pandas time-based rolling, window (t-7d, t], current event included (closed='right')."""
    s = ev.set_index("ts").assign(one=1)["one"]
    return s.rolling("7D").sum().astype(int).to_numpy()

class OnlineCounter:
    """Serving path: incremental deque. BUGGY keeps an event exactly 7 days old (window [t-7d, t])."""
    def __init__(self, buggy): self.q, self.buggy = deque(), buggy
    def update(self, t):
        self.q.append(t); cut = t - pd.Timedelta(days=7)
        while self.q and (self.q[0] < cut if self.buggy else self.q[0] <= cut): self.q.popleft()
        return len(self.q)

def online_series(ev, buggy):
    c = OnlineCounter(buggy); return np.array([c.update(t) for t in ev.ts])

def parity_report(ev, buggy):
    off, on = offline_count_7d(ev), online_series(ev, buggy)
    bad = np.flatnonzero(off != on)
    return off, on, bad

def test_online_matches_offline():              # run with pytest or call directly
    ev = make_events(); off, on, bad = parity_report(ev, buggy=False)
    assert len(bad) == 0, f"{len(bad)} of {len(ev)} rows disagree, first at {ev.ts.iloc[bad[0]]}"

if __name__ == "__main__":
    ev = make_events()
    for buggy in (True, False):
        off, on, bad = parity_report(ev, buggy)
        print(f"online variant = {'inclusive boundary (buggy)' if buggy else 'exclusive boundary (fixed)'}: {len(bad)} of {len(ev)} rows disagree")
        for i in bad[:3]:
            print(f"   ts={ev.ts.iloc[i]}  offline={off[i]}  online={on[i]}")
    try: test_online_matches_offline(); print("parity test with fixed online code: PASS")
    except AssertionError as e: print("parity test FAIL:", e)
    OnlineBug = lambda: parity_report(ev, True)
    try:
        off, on, bad = OnlineBug(); assert len(bad) == 0, f"{len(bad)} rows disagree"
    except AssertionError as e: print("parity test with buggy online code: FAIL ->", e)
