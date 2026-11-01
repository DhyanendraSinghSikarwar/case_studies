import numpy as np, pandas as pd
rng = np.random.default_rng(23)
days = pd.date_range("2026-08-01", "2026-10-25", freq="D")
base = np.where(days.dayofweek >= 5, 6000, 10000)          # weekends are lower
cnt = (base * rng.normal(1, 0.03, len(days))).round().astype(int)
df = pd.DataFrame({"event_date": days, "rows": cnt})
# load time per partition: normally 02:00 next day
df["loaded_at"] = df.event_date + pd.Timedelta(days=1, hours=2)
# inject problems in the last days
now = pd.Timestamp("2026-10-26 12:00")
df = df[df.event_date != "2026-10-22"]                           # missing partition
df.loc[df.event_date == "2026-10-23", "rows"] //= 2              # half-size partition (a Friday)
df.loc[df.event_date == "2026-10-24", "loaded_at"] += pd.Timedelta(hours=30)   # late but complete
df["dow"] = df.event_date.dt.dayofweek
hist = df[df.event_date < "2026-10-15"]
# seasonal band: same weekday, median and MAD-based band
stats = hist.groupby("dow")["rows"].agg(med="median", mad=lambda s: (s - s.median()).abs().median())
def checks(df, now, expected_cadence=pd.Timedelta(days=1), sla=pd.Timedelta(hours=6), k=8):
    out = []
    # freshness: newest event_date vs now; allow cadence + SLA slack
    newest = df.event_date.max()
    lag = now - (newest + pd.Timedelta(days=1))          # how old is the newest data
    if lag > expected_cadence + sla: out.append(f"STALE: newest partition {newest.date()}, data is {lag} old (allowed {expected_cadence + sla})")
    # missing partitions in the recent window
    want = pd.date_range("2026-10-15", "2026-10-25")
    for d in want.difference(df.event_date): out.append(f"MISSING partition {d.date()}")
    for _, r in df[df.event_date >= "2026-10-15"].iterrows():
        s = stats.loc[r.dow]; lo, hi = s.med - k * max(s.mad, 1), s.med + k * max(s.mad, 1)
        if not lo <= r.rows <= hi:
            out.append(f"VOLUME {r.event_date.date()} rows={r.rows} outside [{lo:.0f}, {hi:.0f}] for weekday {r.dow}")
        delay = r.loaded_at - (r.event_date + pd.Timedelta(days=1, hours=2))
        if delay > sla: out.append(f"LATE-LOAD {r.event_date.date()} loaded {delay} after due time (rows look complete: {r.rows})")
    return out
print("history weekday bands (median, MAD):"); print(stats.round(0).to_string())
print("--- run at", now)
for a in checks(df, now): print(a)
now2 = pd.Timestamp("2026-10-28 12:00")
print("--- same table, run at", now2, "(no new partition arrived)")
for a in checks(df, now2): print(a)
# a naive global band would flag every weekend:
g = hist.rows; lo, hi = g.median() - 3 * g.std(), g.median() + 3 * g.std()
wk = df[(df.event_date >= "2026-10-15") & (df.dow >= 5)]
print(f"\nnaive global band [{lo:.0f}, {hi:.0f}]; weekend rows in recent window: {wk.rows.tolist()} (all inside? {bool(wk.rows.between(lo, hi).all())})")
print("half-size Friday rows", int(df[df.event_date=='2026-10-23'].rows.iloc[0]), "inside the naive global band?", bool(lo <= df[df.event_date=='2026-10-23'].rows.iloc[0] <= hi))
