# Q3: sargability. Plans and VM steps for predicates on event_time (indexed) and user_id.
import random
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

random.seed(3)
base = datetime(2024, 1, 1)
rows = []
for i in range(1, 300001):
    t = base + timedelta(seconds=random.randint(0, 365 * 86400 - 1))
    rows.append((i, random.randint(1, 5000), t.strftime("%Y-%m-%d %H:%M:%S"),
                 random.choice(["view", "click", "buy"]), "x"))
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INT, event_time TEXT, event_type TEXT, payload TEXT)")
con.executemany("INSERT INTO events VALUES (?,?,?,?,?)", rows)
con.execute("CREATE INDEX ix_time ON events(event_time)")
con.execute("CREATE INDEX ix_user ON events(user_id)")
con.commit()

_n = [0]
def plan(where, sel="COUNT(*)"):
    _n[0] += 1
    sql = f"SELECT {sel} FROM events WHERE {where}"
    return con.execute("EXPLAIN QUERY PLAN " + sql + " " * _n[0]).fetchall()[0][3]

def steps(where):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    n = con.execute(f"SELECT COUNT(*) FROM events WHERE {where}").fetchone()[0]
    con.set_progress_handler(None, 0)
    return c[0], n

preds = [
    ("strftime",   "strftime('%Y-%m', event_time) = '2024-03'"),
    ("substr",     "substr(event_time,1,7) = '2024-03'"),
    ("date()",     "date(event_time) = '2024-03-05'"),
    ("LIKE",       "event_time LIKE '2024-03%'"),
    ("COALESCE",   "COALESCE(event_time,'x') = '2024-03-05 10:00:00'"),
    ("user_id+0",  "user_id + 0 = 5"),
    ("user_id=5",  "user_id = 5"),
    ("range",      "event_time >= '2024-03-01' AND event_time < '2024-04-01'"),
]
res = []
for name, w in preds:
    s, n = steps(w)
    res.append((name, plan(w), plan(w, "*"), s, n))
pd.set_option("display.width", 250)
print(pd.DataFrame(res, columns=["predicate", "plan COUNT(*)", "plan SELECT *", "vm_steps", "count"]).to_string(index=False))

# the three March predicates must agree on the count
c1 = steps("strftime('%Y-%m', event_time) = '2024-03'")[1]
c2 = steps("event_time >= '2024-03-01' AND event_time < '2024-04-01'")[1]
c3 = steps("event_time LIKE '2024-03%'")[1]
assert c1 == c2 == c3
print("March counts equal:", c1, c2, c3)

# timestamps: date = '2024-03-05' as a half-open range
a = steps("date(event_time) = '2024-03-05'")
b = steps("event_time >= '2024-03-05' AND event_time < '2024-03-06'")
assert a[1] == b[1]
print("one day: function form", a, "range form", b, "plan:", plan("event_time >= '2024-03-05' AND event_time < '2024-03-06'"))
# the closed-range trap: BETWEEN '2024-03-05' AND '2024-03-05' on timestamps returns 0 rows
print("BETWEEN '2024-03-05' AND '2024-03-05' count:", steps("event_time BETWEEN '2024-03-05' AND '2024-03-05'")[1])

# expression index on the exact expression
con.execute("CREATE INDEX ix_month ON events(strftime('%Y-%m', event_time))")
print("with expression index:", plan("strftime('%Y-%m', event_time) = '2024-03'"), steps("strftime('%Y-%m', event_time) = '2024-03'"))
print("same idea, different expression (substr):", plan("substr(event_time,1,7) = '2024-03'"))
print("strftime('%Y', ...) with the month index:", plan("strftime('%Y', event_time) = '2024'"))

# pandas: string compare on a sorted column is a range; the function form touches every row
df = pd.DataFrame(rows, columns=["event_id", "user_id", "event_time", "event_type", "payload"])
m_range = df[(df.event_time >= "2024-03-01") & (df.event_time < "2024-04-01")]
m_func = df[pd.to_datetime(df.event_time).dt.strftime("%Y-%m") == "2024-03"]
assert len(m_range) == len(m_func) == c2
s = df.sort_values("event_time")
lo, hi = s.event_time.searchsorted("2024-03-01", "left"), s.event_time.searchsorted("2024-04-01", "left")
assert hi - lo == c2
print("pandas: mask, to_datetime+strftime and searchsorted all give", c2)
