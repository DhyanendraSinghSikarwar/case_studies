# Q36 two MAU numbers: simulate raw events, show each definition choice moves the count
import numpy as np, pandas as pd
rng = np.random.default_rng(36)
N = 20_000
users = pd.DataFrame({"user_id": np.arange(N)})
users["n_dev"] = rng.choice([1, 2, 3], N, p=[0.75, 0.2, 0.05])
rows = []
for u, nd in zip(users.user_id, users.n_dev):
    for dv in range(nd):
        k = rng.integers(1, 6)
        # event times across March 2026 UTC, plus some at the edges
        t = pd.Timestamp("2026-03-01") + pd.to_timedelta(rng.uniform(-0.3, 31.3, k), unit="D")
        for tt in t:
            rows.append((u, f"{u}-{dv}", tt, 0, rng.random() < 0.9))
ev = pd.DataFrame(rows, columns=["user_id", "device_id", "ts_utc", "is_bot", "logged_in"])
bots = pd.DataFrame({"user_id": np.arange(N, N + 600)})
brow = []
for u in bots.user_id:
    for tt in pd.Timestamp("2026-03-01") + pd.to_timedelta(rng.uniform(0, 31, 3), unit="D"):
        brow.append((u, f"b-{u}", tt, 1, False))
ev = pd.concat([ev, pd.DataFrame(brow, columns=ev.columns)], ignore_index=True)
ev["ts_ist"] = ev.ts_utc + pd.Timedelta(hours=5, minutes=30)

def in_month(ts):
    return (ts >= "2026-03-01") & (ts < "2026-04-01")
A = ev[in_month(ev.ts_utc)].device_id.nunique()                          # team A: devices, UTC, bots in
B = ev[in_month(ev.ts_ist) & (ev.is_bot == 0)].user_id.nunique()        # team B: people, IST, bots out
print("A (devices, UTC, bots in):", A, " B (people, IST, bots out):", B, " gap:", A - B)

# waterfall, fixed order; each step changes one definition
s0 = ev[in_month(ev.ts_utc)].device_id.nunique()
s1 = ev[in_month(ev.ts_utc)].user_id.nunique()                                   # dedupe devices to user_id (bots count as users)
s2 = ev[in_month(ev.ts_utc) & (ev.is_bot == 0)].user_id.nunique()                # drop bots
s3 = ev[in_month(ev.ts_ist) & (ev.is_bot == 0)].user_id.nunique()                # month boundary in IST
steps = [("devices in UTC month", s0), ("-> distinct user_id", s1), ("-> drop bots", s2), ("-> IST month", s3)]
prev = None
for name, v in steps:
    print(f"{name:24}{v:8d}" + ("" if prev is None else f"  step {v-prev:+d}"))
    prev = v
assert s0 == A and s3 == B
assert (s0 - s1) + (s1 - s2) + (s2 - s3) == A - B
print('note: state the order of the waterfall steps when you present it')
