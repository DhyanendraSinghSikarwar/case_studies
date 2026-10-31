# Q31: rowid table vs WITHOUT ROWID, page counts, DELETE and VACUUM (file databases in a temp dir).
import os, sqlite3, tempfile
import numpy as np
import pandas as pd

rng = np.random.default_rng(31)
N = 100_000
a = np.array([f"key_{i:04d}" for i in range(2000)])[rng.integers(0, 2000, N)]
b = np.arange(N)                     # unique b makes (a, b) unique
c = np.array([f"v{i % 97:02d}" for i in range(N)])
data = pd.DataFrame({"a": a, "b": b, "c": c})
rows = list(data.itertuples(index=False, name=None))
tmp = tempfile.mkdtemp()

def build(kind, big=False):
    path = os.path.join(tmp, f"{kind}{'_big' if big else ''}.db")
    con = sqlite3.connect(path)
    wr = " WITHOUT ROWID" if kind == "norowid" else ""
    con.execute(f"CREATE TABLE kv(a TEXT, b INTEGER, c TEXT, PRIMARY KEY (a, b)){wr}")
    payload = rows if not big else [(x, y, z * 100) for x, y, z in rows[:20_000]]
    con.executemany("INSERT INTO kv VALUES (?,?,?)", payload)
    con.commit()
    return con

def stats(con):
    pc = con.execute("PRAGMA page_count").fetchone()[0]
    ps = con.execute("PRAGMA page_size").fetchone()[0]
    fl = con.execute("PRAGMA freelist_count").fetchone()[0]
    return pc, ps, fl

def dbstat(con):
    return {r[0]: (r[1], r[2]) for r in con.execute(
        "SELECT name, COUNT(*), SUM(pgsize) FROM dbstat WHERE name IN ('kv') OR name LIKE 'sqlite_autoindex%' GROUP BY name")}

def plan(con, sql): return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql)]

cons = {k: build(k) for k in ("rowid", "norowid")}
print("auto_vacuum:", cons["rowid"].execute("PRAGMA auto_vacuum").fetchone()[0], "(0 = NONE, the default)")
Q_AB = "SELECT c FROM kv WHERE a = 'key_0007' AND b = 12345"
Q_B = "SELECT c FROM kv WHERE b = 12345"
for k, con in cons.items():
    print(f"\n[{k}]")
    print("  plan a+b:", plan(con, Q_AB)); print("  plan b only:", plan(con, Q_B))
    pc, ps, fl = stats(con)
    print(f"  page_count {pc}, page_size {ps}, bytes {pc * ps:,}, freelist {fl}")
    print("  dbstat (pages, bytes) per b-tree:", dbstat(con))

# same answers from both layouts and from pandas
for q, mask in ((Q_AB, (data.a == "key_0007") & (data.b == 12345)), (Q_B, data.b == 12345)):
    exp = sorted(data.loc[mask, "c"])
    for k, con in cons.items():
        assert sorted(r[0] for r in con.execute(q)) == exp
print("\nlookups equal pandas on both layouts")

# rows with a big payload: the 1/20 page rule of thumb (4096 / 20 = about 204 bytes)
big = {k: build(k, big=True) for k in ("rowid", "norowid")}
print("\n20,000 rows with a 300-byte c column:", {k: stats(v)[0] for k, v in big.items()}, "pages")

# DELETE half, then VACUUM
print("\nDELETE half the rows (b odd), then VACUUM")
for k, con in cons.items():
    before = stats(con)
    con.execute("DELETE FROM kv WHERE b % 2 = 1"); con.commit()
    mid = stats(con)
    n_left = con.execute("SELECT COUNT(*) FROM kv").fetchone()[0]
    con.execute("VACUUM")
    after = stats(con)
    print(f"  {k}: rows left {n_left}; pages before {before[0]}, after DELETE {mid[0]} (freelist {mid[2]}), after VACUUM {after[0]} (freelist {after[2]});"
          f" file bytes after VACUUM {after[0] * after[1]:,}")
    assert n_left == N // 2
for con in list(cons.values()) + list(big.values()): con.close()
