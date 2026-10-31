# Q23: write cost: batching inserts and transactions (file-backed SQLite)
import sqlite3, random, os, tempfile, time
import pandas as pd

random.seed(23)
N = 100_000
types = ["view", "click", "cart", "buy"]
data = [(i, random.randint(1, 5000), random.choice(types), "2024-%02d-%02d" % (random.randint(1, 12), random.randint(1, 28)))
        for i in range(1, N + 1)]
pdf = pd.DataFrame(data, columns=["event_id", "user_id", "event_type", "event_time"])
DDL = "CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_type TEXT, event_time TEXT)"
INS = "INSERT INTO events VALUES (?,?,?,?)"
IDX = ["CREATE INDEX ix_user ON events(user_id)", "CREATE INDEX ix_type ON events(event_type)", "CREATE INDEX ix_time ON events(event_time)"]
tmp = tempfile.TemporaryDirectory()

def fresh(name):
    path = os.path.join(tmp.name, name + ".db")
    con = sqlite3.connect(path)
    con.execute(DDL)
    con.commit()
    return con

def run(label, fn, con, expect_rows):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    t0 = time.perf_counter()
    fn(con)
    ms = (time.perf_counter() - t0) * 1000
    con.set_progress_handler(None, 0)
    cnt, s = con.execute("SELECT COUNT(*), SUM(user_id) FROM events").fetchone()
    assert cnt == expect_rows
    assert s == int(pdf["user_id"].iloc[:expect_rows].sum())       # same rows as the pandas frame
    print("%-52s rows %6d  progress steps %9d  wall %8.1f ms" % (label, cnt, n[0], ms))
    return n[0], ms

con = fresh("probe")
print("journal_mode =", con.execute("PRAGMA journal_mode").fetchone()[0], "| synchronous =", con.execute("PRAGMA synchronous").fetchone()[0], "(2 = FULL)")
con.close()

def per_row(con):
    for r in data[:2000]:
        con.execute(INS, r)
        con.commit()
def loop_one_txn(con):
    for r in data:
        con.execute(INS, r)
    con.commit()
def many(con):
    con.executemany(INS, data)
    con.commit()
def multirow(con, k=500):
    for i in range(0, N, k):
        chunk = data[i:i + k]
        con.execute("INSERT INTO events VALUES " + ",".join(["(?,?,?,?)"] * len(chunk)), [v for r in chunk for v in r])
    con.commit()
def indexes_first(con):
    for s in IDX: con.execute(s)
    con.executemany(INS, data); con.commit()
def indexes_after(con):
    con.executemany(INS, data)
    for s in IDX: con.execute(s)
    con.commit()
def fmt_strings(con):                          # unsafe string formatting, shown only for cost
    for r in data:
        con.execute("INSERT INTO events VALUES (%d,%d,'%s','%s')" % r)
    con.commit()

print("\n-- commit granularity (default journal_mode, synchronous=FULL)")
a = run("1. execute + commit per row, 2,000 rows only", per_row, fresh("a"), 2000)
b = run("2. execute in a loop, one transaction, 100,000 rows", loop_one_txn, fresh("b"), N)
c = run("3. executemany, one transaction, 100,000 rows", many, fresh("c"), N)
d = run("3b. multi-row INSERT VALUES (500 rows per statement)", multirow, fresh("d"), N)
e = run("3c. execute with string formatting (not safe), one txn", fmt_strings, fresh("e"), N)
print("per-row commit costs %.2f ms per row; executemany costs %.4f ms per row (machine-specific)" % (a[1] / 2000, c[1] / N))

print("\n-- three secondary indexes before versus after the load (executemany, one transaction)")
f = run("4a. indexes created BEFORE loading", indexes_first, fresh("f"), N)
g = run("4b. indexes created AFTER loading", indexes_after, fresh("g"), N)

print("\n-- per-row commits under other settings (2,000 rows, machine-specific)")
settings = [("journal_mode=WAL, synchronous=FULL", ["PRAGMA journal_mode=WAL"]),
            ("journal_mode=WAL, synchronous=NORMAL", ["PRAGMA journal_mode=WAL", "PRAGMA synchronous=NORMAL"]),
            ("journal_mode=DELETE, synchronous=OFF", ["PRAGMA synchronous=OFF"])]
for j, (label, pragmas) in enumerate(settings):
    con = fresh("h%d" % j)
    for p in pragmas:
        con.execute(p).fetchall()
    run("5. per-row commit, " + label, per_row, con, 2000)

# the safe path: parameters. A quote in the data breaks the formatted statement
c2 = fresh("q")
try:
    c2.execute("INSERT INTO events VALUES (1,1,'it's','x')")
except sqlite3.OperationalError as ex:
    print("\nformatted SQL with a quote in the value ->", ex)
c2.execute(INS, (1, 1, "it's", "x"))
print("bound parameters store it safely:", c2.execute("SELECT event_type FROM events").fetchone()[0])
print("compile option for the bound-variable limit:", [o for o in sqlite3.connect(":memory:").execute("PRAGMA compile_options") if "MAX_VARIABLE" in o[0]])
print("asserts passed: every load produced the same row count and SUM(user_id) as the pandas frame")
tmp.cleanup()
