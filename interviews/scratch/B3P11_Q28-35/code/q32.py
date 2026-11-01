# Q32: emulate partition pruning with monthly tables and a UNION ALL view in SQLite.
import sqlite3
import numpy as np
import pandas as pd

rng = np.random.default_rng(32)
months = [f"2024_{m:02d}" for m in range(1, 7)]
N = 60_000
t0 = pd.Timestamp("2024-01-01")
secs = rng.integers(0, 182 * 86400, N)           # Jan 1 to Jun 30
ev = pd.DataFrame({"event_id": np.arange(1, N + 1), "user_id": rng.integers(1, 5001, N),
                   "event_time": (t0 + pd.to_timedelta(secs, unit="s")).strftime("%Y-%m-%d %H:%M:%S"),
                   "event_type": np.array(["view", "click", "buy"])[rng.integers(0, 3, N)]})
ev["mon"] = ev["event_time"].str[:7].str.replace("-", "_")

def build(with_check):
    con = sqlite3.connect(":memory:")
    for m in months:
        lo, hi = m.replace("_", "-") + "-01", None
        nxt = (pd.Timestamp(lo) + pd.offsets.MonthBegin(1)).strftime("%Y-%m-%d")
        chk = f", CHECK (event_time >= '{lo}' AND event_time < '{nxt}')" if with_check else ""
        con.execute(f"CREATE TABLE ev_{m}(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_time TEXT, event_type TEXT{chk})")
        con.execute(f"CREATE INDEX ix_{m}_time ON ev_{m}(event_time)")
        con.execute(f"CREATE INDEX ix_{m}_user ON ev_{m}(user_id)")
        part = ev[ev.mon == m]
        con.executemany(f"INSERT INTO ev_{m} VALUES (?,?,?,?)", part.iloc[:, :4].itertuples(index=False, name=None))
    con.execute("CREATE VIEW ev AS " + " UNION ALL ".join(f"SELECT * FROM ev_{m}" for m in months))
    con.commit()
    return con

def plan(con, sql): return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql)]

def steps(con, sql):
    c = [0]
    def cb(): c[0] += 1; return 0
    con.set_progress_handler(cb, 1); r = con.execute(sql).fetchall(); con.set_progress_handler(None, 0)
    return c[0], r

one_view = "SELECT COUNT(event_type) FROM ev WHERE event_time >= '2024-03-01' AND event_time < '2024-04-01'"
cross_view = "SELECT COUNT(event_type) FROM ev WHERE event_time >= '2024-03-15' AND event_time < '2024-04-15'"
direct = "SELECT COUNT(event_type) FROM ev_2024_03 WHERE event_time >= '2024-03-01' AND event_time < '2024-04-01'"
by_user = "SELECT COUNT(*) FROM ev WHERE user_id = 42"

exp_one = int(((ev.event_time >= "2024-03-01") & (ev.event_time < "2024-04-01")).sum())
exp_cross = int(((ev.event_time >= "2024-03-15") & (ev.event_time < "2024-04-15")).sum())
exp_user = int((ev.user_id == 42).sum())
for label, with_check in (("no CHECK constraints", False), ("with CHECK constraints on event_time", True)):
    con = build(with_check)
    print(f"\n=== {label}")
    for name, q, exp in (("one month via view", one_view, exp_one), ("cross-month via view", cross_view, exp_cross),
                         ("one month, table named directly", direct, exp_one), ("user_id=42 via view", by_user, exp_user)):
        n_steps, r = steps(con, q)
        assert r[0][0] == exp
        print(f"-- {name}: count {r[0][0]} (pandas {exp}), VM steps {n_steps:,}")
        print("      plan:", " / ".join(p.replace("USING ", "").replace("INDEX ", "") for p in plan(con, q)))
    if not with_check:
        con.execute("CREATE VIEW ev_one AS SELECT * FROM ev_2024_03")
        q = one_view.replace("FROM ev WHERE", "FROM ev_one WHERE")
        n_steps, r = steps(con, q)
        assert r[0][0] == exp_one
        print(f"-- one month via a ONE-branch view (isolates the view overhead): VM steps {n_steps:,}")
    con.close()
print("rows per monthly table:", {m: int((ev.mon == m).sum()) for m in months}, "total", len(ev))
print("\nall counts equal pandas")
