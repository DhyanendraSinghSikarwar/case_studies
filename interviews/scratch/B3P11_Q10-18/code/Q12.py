# Q12
import sqlite3, random, tempfile
import numpy as np
import pandas as pd

WORK = tempfile.mkdtemp()          # file databases: every plan and step count uses a FRESH connection

def plan(path, sql, params=()):
    """EXPLAIN QUERY PLAN detail lines, read on a fresh connection (a reused connection can show a stale plan)."""
    c = sqlite3.connect(path)
    try:
        return [r[3] for r in c.execute("EXPLAIN QUERY PLAN " + sql, params)]
    finally:
        c.close()

def steps(path, sql, params=()):
    """(VM steps, rows) for one statement: set_progress_handler(cb, 1) fires once per VM opcode."""
    c = sqlite3.connect(path)
    n = [0]
    def tick():
        n[0] += 1
        return 0
    c.set_progress_handler(tick, 1)
    rows = c.execute(sql, params).fetchall()
    c.set_progress_handler(None, 0)
    c.close()
    return n[0], rows

rng = random.Random(31)
N = 200000
base = pd.Timestamp("2024-01-01")
# 20,000 distinct timestamps, about 10 posts each, so created_at is NOT unique
stamps = [(base + pd.Timedelta(minutes=5 * rng.randint(0, 19999))).strftime("%Y-%m-%d %H:%M") for _ in range(N)]
feed_rows = [(i, stamps[i - 1], rng.randint(1, 5000), "post %d" % i) for i in range(1, N + 1)]
path = WORK + "/feed.db"
c = sqlite3.connect(path)
c.execute("CREATE TABLE feed(post_id INTEGER PRIMARY KEY, created_at TEXT, user_id INT, title TEXT)")
c.executemany("INSERT INTO feed VALUES(?,?,?,?)", feed_rows)
c.execute("CREATE INDEX ix_feed ON feed(created_at, post_id)")
c.commit(); c.close()
df = pd.DataFrame(feed_rows, columns=["post_id", "created_at", "user_id", "title"])
ordered = df.sort_values(["created_at", "post_id"], ascending=False).reset_index(drop=True)
print("distinct created_at:", df.created_at.nunique(), "of", N, "rows")

OFF = "SELECT post_id, created_at FROM feed ORDER BY created_at DESC, post_id DESC LIMIT 20 OFFSET ?"
KEY = ("SELECT post_id, created_at FROM feed WHERE (created_at, post_id) < (?, ?) "
       "ORDER BY created_at DESC, post_id DESC LIMIT 20")
print(f"{'page':>5} {'OFFSET steps':>13} {'keyset steps':>13}")
for page in (1, 5000, 9000):
    off = (page - 1) * 20
    so, ro = steps(path, OFF, (off,))
    if page == 1:
        sk, rk = steps(path, "SELECT post_id, created_at FROM feed ORDER BY created_at DESC, post_id DESC LIMIT 20")
    else:                                   # cursor = last row of the previous page
        last = ordered.iloc[off - 1]
        sk, rk = steps(path, KEY, (last.created_at, int(last.post_id)))
    assert ro == rk == list(zip(ordered.post_id[off:off + 20], ordered.created_at[off:off + 20]))
    print(f"{page:>5} {so:>13,} {sk:>13,}")
last = ordered.iloc[5000 * 20 - 21]
print("OFFSET plan:", plan(path, OFF, (99980,)))
print("keyset plan:", plan(path, KEY, (last.created_at, int(last.post_id))))

print("--- keyset with a NON-unique key only (created_at) ---")
def walk(sql_first, sql_next, key_of):
    seen, cur, pages = [], None, 0
    while True:
        rows = sqlite3.connect(path).execute(sql_first if cur is None else sql_next, () if cur is None else (cur,)).fetchall()
        if not rows: break
        seen += [r[0] for r in rows]; cur = key_of(rows[-1]); pages += 1
        if pages > 20000: break
    return seen, pages
seen, pages = walk("SELECT post_id, created_at FROM feed ORDER BY created_at DESC LIMIT 20",
                   "SELECT post_id, created_at FROM feed WHERE created_at < ? ORDER BY created_at DESC LIMIT 20", lambda r: r[1])
print(f"created_at < ?  : fetched {len(seen):,} rows in {pages:,} pages, {N - len(set(seen)):,} rows never returned")
# one page boundary with ties
page1 = sqlite3.connect(path).execute("SELECT post_id, created_at FROM feed ORDER BY created_at DESC, post_id DESC LIMIT 20").fetchall()
seen2 = [r[0] for r in page1]
nxt_lt = sqlite3.connect(path).execute("SELECT post_id FROM feed WHERE created_at < ? ORDER BY created_at DESC, post_id DESC LIMIT 20", (page1[-1][1],)).fetchall()
nxt_le = sqlite3.connect(path).execute("SELECT post_id FROM feed WHERE created_at <= ? ORDER BY created_at DESC, post_id DESC LIMIT 20", (page1[-1][1],)).fetchall()
nxt_ok = sqlite3.connect(path).execute(KEY, (page1[-1][1], page1[-1][0])).fetchall()
print("page 1 last row:", page1[-1], "| ties with that timestamp in the table:", int((df.created_at == page1[-1][1]).sum()))
true2 = set(ordered.post_id[20:40])
print("page 2 via '<'  : repeats", len(set(seen2) & {r[0] for r in nxt_lt}), "| true page-2 rows missing:", len(true2 - {r[0] for r in nxt_lt}))
print("page 2 via '<=' : repeats", len(set(seen2) & {r[0] for r in nxt_le}), "| true page-2 rows missing:", len(true2 - {r[0] for r in nxt_le}))
assert [r[0] for r in nxt_ok] == list(ordered.post_id[20:40])

print("--- stable under inserts ---")
c = sqlite3.connect(path)
before = c.execute(OFF, (20,)).fetchall()
c.executemany("INSERT INTO feed VALUES(?,?,?,?)", [(N + k, "2025-01-01 00:%02d" % k, 1, "new %d" % k) for k in range(1, 6)])
c.commit()
after = c.execute(OFF, (20,)).fetchall()
print("OFFSET 20 page 2: rows shifted by 5 new posts; overlap with the old page 2:", len({r[0] for r in before} & {r[0] for r in after}), "of 20")
cursor = (page1[-1][1], page1[-1][0])
print("keyset page 2 after the inserts equals the old page 2:", [r[0] for r in c.execute(KEY, cursor).fetchall()] == [r[0] for r in before])
c.close()
