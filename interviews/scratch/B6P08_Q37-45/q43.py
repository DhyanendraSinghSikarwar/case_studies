# Q43: reproduce training data of model v9 (11 months ago) when the table is overwritten nightly
import hashlib, sqlite3

def digest(rows):
    h = hashlib.sha256()
    for r in sorted(rows):
        h.update(repr(r).encode())
    return h.hexdigest()[:12]

db = sqlite3.connect(":memory:")
db.execute("create table events (id int, cust int, amount real, event_day int, loaded_day int)")
# append-only raw events; some arrive late (loaded_day > event_day) and one is corrected later
raw = [(1, 10, 50.0, 1, 1), (2, 11, 20.0, 1, 1), (3, 10, 70.0, 2, 2), (4, 12, 10.0, 2, 4),   # id 4 arrives 2 days late
       (5, 11, 30.0, 3, 3), (6, 13, 90.0, 3, 3)]
db.executemany("insert into events values (?,?,?,?,?)", raw)

SQL = "select cust, sum(amount) from events where event_day<=? and loaded_day<=? group by cust"
TRAIN_DAY = 3

# Day 3: training run reads the table that is overwritten nightly (the problem)
train_rows = db.execute(SQL, (TRAIN_DAY, TRAIN_DAY)).fetchall()
v9_digest = digest(train_rows)
print("v9 training rows:", len(train_rows), "digest:", v9_digest)

# Today (day 400): only the SQL is in git. Re-run it with 'now' as the cutoff
rows_now = db.execute(SQL, (TRAIN_DAY, 400)).fetchall()
print("re-run with today's data: rows", len(rows_now), "digest", digest(rows_now), "| matches v9:", digest(rows_now) == v9_digest)
assert digest(rows_now) != v9_digest        # the late event changes the answer

# What CAN be recovered: if raw events are append-only and carry load time, filter by load time too
rows_asof = db.execute(SQL, (TRAIN_DAY, TRAIN_DAY)).fetchall()
print("as-of reconstruction (event_day and loaded_day <= 3): digest", digest(rows_asof), "| matches v9:", digest(rows_asof) == v9_digest)
assert digest(rows_asof) == v9_digest       # only possible because loaded_day was kept

# What would have made it a one-hour task: manifest tying model version to an immutable snapshot
db.execute("create table snapshot_9 as select * from events where loaded_day <= 3")   # written once, never updated
manifest = {"model": "v9", "snapshot": "snapshot_9", "sql_git_sha": "abc1234 (invented)",
            "row_count": len(train_rows), "digest": v9_digest}
snap_rows = db.execute("select cust, sum(amount) from snapshot_9 where event_day<=3 group by cust").fetchall()
check = digest(snap_rows) == manifest["digest"] and len(snap_rows) == manifest["row_count"]
print("manifest check from snapshot:", check)
assert check

# Cost of snapshotting every night vs only per training run (invented sizes)
nights = 11 * 30
per_run = 11        # e.g. one retrain a month (invented)
print("nightly snapshots over 11 months:", nights, "| per-run snapshots:", per_run)
assert nights == 330 and per_run == 11
