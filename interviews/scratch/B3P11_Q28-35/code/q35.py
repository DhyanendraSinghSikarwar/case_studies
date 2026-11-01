# Q35: locking in a file-backed SQLite database: rollback journal vs WAL (executed); other engines in prose only.
import os, sqlite3, tempfile
import pandas as pd

def open_db(path, timeout=0.1):
    return sqlite3.connect(path, timeout=timeout, isolation_level=None)   # isolation_level=None: we send BEGIN/COMMIT ourselves

def run(mode):
    d = tempfile.mkdtemp(); path = os.path.join(d, "t.db")
    setup = open_db(path)
    setup.execute(f"PRAGMA journal_mode={mode}")
    setup.execute("CREATE TABLE acct(id INTEGER PRIMARY KEY, bal INTEGER)")
    setup.execute("INSERT INTO acct VALUES (1, 100)")
    print(f"\n===== journal_mode = {setup.execute('PRAGMA journal_mode').fetchone()[0]}  (busy_timeout = "
          f"{setup.execute('PRAGMA busy_timeout').fetchone()[0]} ms, from timeout=0.1)")
    reader, writer = open_db(path), open_db(path)
    reader.execute("BEGIN"); n0 = reader.execute("SELECT bal FROM acct WHERE id = 1").fetchone()[0]
    print("reader: BEGIN + SELECT sees bal =", n0, "and keeps the transaction open")
    writer.execute("BEGIN"); writer.execute("UPDATE acct SET bal = 150 WHERE id = 1")
    print("writer: BEGIN + UPDATE succeeded (change is uncommitted)")
    try:
        writer.execute("COMMIT"); print("writer: COMMIT succeeded")
        committed = True
    except sqlite3.OperationalError as e:
        print("writer: COMMIT failed ->", e); committed = False
    print("reader (same transaction) sees bal =", reader.execute("SELECT bal FROM acct WHERE id = 1").fetchone()[0])
    print("files in the directory:", sorted(os.listdir(d)))
    if not committed:
        writer.execute("ROLLBACK")
    reader.execute("COMMIT")
    print("reader after COMMIT sees bal =", reader.execute("SELECT bal FROM acct WHERE id = 1").fetchone()[0])
    if not committed:
        writer.execute("BEGIN"); writer.execute("UPDATE acct SET bal = 150 WHERE id = 1"); writer.execute("COMMIT")
        print("writer retried after the reader finished: committed; bal =", reader.execute("SELECT bal FROM acct WHERE id = 1").fetchone()[0])
    # second writer while the first holds the write lock
    w1, w2 = open_db(path), open_db(path)
    w1.execute("BEGIN IMMEDIATE")
    try:
        w2.execute("BEGIN IMMEDIATE"); print("second writer got the lock")
    except sqlite3.OperationalError as e:
        print("second BEGIN IMMEDIATE while a writer is open ->", e)
    w1.execute("ROLLBACK")
    if mode == "wal":
        # read-then-write on a snapshot that went stale
        r, w = open_db(path), open_db(path)
        r.execute("BEGIN"); r.execute("SELECT bal FROM acct").fetchall()
        w.execute("UPDATE acct SET bal = bal + 1 WHERE id = 1")           # autocommit write
        try:
            r.execute("UPDATE acct SET bal = bal + 10 WHERE id = 1"); print("reader upgraded to a writer fine")
        except sqlite3.OperationalError as e:
            print("reader with an old snapshot tries to write ->", e)
        r.execute("ROLLBACK"); r.close(); w.close()
    out = pd.read_sql("SELECT * FROM acct", setup)
    for c in (setup, reader, writer, w1, w2): c.close()
    return out

res = {m: run(m) for m in ("delete", "wal")}
expected = {"delete": 150, "wal": 151}   # wal run has one extra +1 update from the stale-snapshot demo
for m, o in res.items():
    pd.testing.assert_frame_equal(o, pd.DataFrame({"id": [1], "bal": [expected[m]]}), check_dtype=False)
print("\nfinal tables equal the expected pandas frames:", {m: o["bal"].tolist() for m, o in res.items()})

# autocommit reads see each other's commits (a non-repeatable read at the SQL level); a WAL snapshot does not
d = tempfile.mkdtemp(); p = os.path.join(d, "n.db")
a, b = open_db(p), open_db(p)
a.execute("PRAGMA journal_mode=WAL"); a.execute("CREATE TABLE x(v INTEGER)"); a.execute("INSERT INTO x VALUES (1)")
first = b.execute("SELECT v FROM x").fetchone()[0]; a.execute("UPDATE x SET v = 2")
second = b.execute("SELECT v FROM x").fetchone()[0]
print("\nautocommit reader, two SELECTs with a commit between:", first, "then", second)
b.execute("BEGIN"); f = b.execute("SELECT v FROM x").fetchone()[0]; a.execute("UPDATE x SET v = 3")
s = b.execute("SELECT v FROM x").fetchone()[0]; b.execute("COMMIT")
print("reader inside BEGIN (WAL snapshot), same two SELECTs:", f, "then", s)
a.close(); b.close()
