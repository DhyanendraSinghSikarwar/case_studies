# Q3: sargability: which predicate shapes can use an index on event_time
import os, sqlite3, tempfile
import numpy as np
import pandas as pd

rng = np.random.default_rng(3)
N = 300_000
secs = rng.integers(0, 366 * 86_400, N)
ts = (pd.Timestamp("2024-01-01") + pd.to_timedelta(secs, unit="s")).strftime("%Y-%m-%d %H:%M:%S").to_numpy()
events = pd.DataFrame({"event_id": np.arange(1, N + 1), "user_id": rng.integers(1, 5_001, N),
                       "event_time": ts, "event_type": rng.choice(["view", "click", "buy"], N, p=[.7, .25, .05]),
                       "payload": "x"})
path = os.path.join(tempfile.mkdtemp(), "q3.db")
con = sqlite3.connect(path)
con.execute("CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INT, event_time TEXT, event_type TEXT, payload TEXT)")
con.executemany("INSERT INTO events VALUES (?,?,?,?,?)", events.itertuples(index=False, name=None))
con.execute("CREATE INDEX ix_time ON events(event_time)")
con.execute("CREATE INDEX ix_user ON events(user_id)")
con.commit(); con.close()
print("sqlite", sqlite3.sqlite_version)

def plan(sql):
    c = sqlite3.connect(path)          # fresh connection per plan
    try:
        return [r[3] for r in c.execute("EXPLAIN QUERY PLAN " + sql)]
    finally:
        c.close()

def steps(sql):
    c = sqlite3.connect(path); n = [0]
    def cb():
        n[0] += 1
        return 0
    c.set_progress_handler(cb, 1)
    out = c.execute(sql).fetchall()
    c.close()
    return n[0], out

CASES = [
 ("strftime on column",  "strftime('%Y-%m', event_time) = '2024-03'", False),
 ("substr on column",    "substr(event_time,1,7) = '2024-03'", False),
 ("date() on column",    "date(event_time) = '2024-03-05'", False),
 ("LIKE prefix",         "event_time LIKE '2024-03%'", False),
 ("COALESCE on column",  "COALESCE(event_time,'x') = '2024-03-05 10:00:00'", False),
 ("user_id + 0",         "user_id + 0 = 5", False),
 ("half-open range",     "event_time >= '2024-03-01' AND event_time < '2024-04-01'", True),
]
print("\nplans (query: SELECT event_id, payload FROM events WHERE <predicate>; payload is not in any index)")
counts = {}
for name, pred, expect in CASES:
    sql = f"SELECT event_id, payload FROM events WHERE {pred}"
    p = plan(sql)
    used = p[0].startswith("SEARCH")
    s, out = steps(sql)
    counts[name] = len(out)
    print(f"- {name:20s} {pred}\n    {p[0]}\n    index used: {used}; VM steps {s:,}; rows {len(out)}")
    if name != "user_id + 0":
        assert used == expect, (name, p)
    else:
        assert p == ["SCAN events"], p

# same answer from every form of the month filter
assert counts["strftime on column"] == counts["substr on column"] == counts["LIKE prefix"] == counts["half-open range"]
m = events["event_time"]
pd_march = int(((m >= "2024-03-01") & (m < "2024-04-01")).sum())
assert pd_march == counts["half-open range"]
pd_march_fn = int((pd.to_datetime(m).dt.strftime("%Y-%m") == "2024-03").sum())
assert pd_march_fn == pd_march
print("\nMarch 2024 rows:", pd_march, "(SQL range, SQL strftime and pandas agree)")

# a plain index on user_id is fine for equality
print("user_id = 5 plan:", plan("SELECT event_id, payload FROM events WHERE user_id = 5")[0])
print("COUNT(*) with strftime plan (covering index, still a full index SCAN):", plan("SELECT COUNT(*) FROM events WHERE strftime('%Y-%m', event_time) = '2024-03'")[0])

# expression indexes: usable only for the exact same expression
c = sqlite3.connect(path)
c.execute("CREATE INDEX ix_month ON events(strftime('%Y-%m', event_time))")
c.execute("CREATE INDEX ix_sub7 ON events(substr(event_time,1,7))")
c.commit(); c.close()
print("\nafter expression indexes:")
for label, pred, expect in [
    ("strftime, exact expression", "strftime('%Y-%m', event_time) = '2024-03'", "ix_month"),
    ("substr(...,1,7), exact",     "substr(event_time,1,7) = '2024-03'", "ix_sub7"),
    ("substr(...,1,6), different", "substr(event_time,1,6) = '2024-0'", None),
    ("strftime, other format",     "strftime('%Y', event_time) = '2024'", None),
]:
    p = plan(f"SELECT event_id, payload FROM events WHERE {pred}")
    print(f"- {label:28s} {p[0]}")
    if expect:
        assert expect in p[0] and p[0].startswith("SEARCH")
    else:
        assert p[0].startswith("SCAN")
s, out = steps("SELECT event_id, payload FROM events WHERE strftime('%Y-%m', event_time) = '2024-03'")
assert len(out) == pd_march
print("strftime filter with expression index: VM steps", f"{s:,}", "rows", len(out))
s, out = steps("SELECT event_id, payload FROM events WHERE event_time >= '2024-03-01' AND event_time < '2024-04-01'")
print("half-open range with ix_time:           VM steps", f"{s:,}", "rows", len(out))
