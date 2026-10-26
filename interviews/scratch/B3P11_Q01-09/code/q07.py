# Q7: implicit type conversion in SQLite (column affinity) and what it does to index use and join order.
import random
import sqlite3
import pandas as pd

random.seed(7)
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE a(id INTEGER PRIMARY KEY, k TEXT, v INT);
CREATE TABLE b(id INTEGER PRIMARY KEY, k INTEGER, w INT);
""")
con.executemany("INSERT INTO a VALUES (?,?,?)", [(i, str(i), i % 7) for i in range(1, 5001)])
con.executemany("INSERT INTO b VALUES (?,?,?)", [(i, random.randint(1, 5000), i % 11) for i in range(1, 50001)])
con.execute("CREATE INDEX ia ON a(k)")
con.execute("CREATE INDEX ib ON b(k)")
con.commit()
print("declared affinities:", con.execute("SELECT name, type FROM pragma_table_info('a') UNION ALL SELECT name, type FROM pragma_table_info('b')").fetchall())
print("typeof stored:", con.execute("SELECT typeof(k) FROM a LIMIT 1").fetchone(), con.execute("SELECT typeof(k) FROM b LIMIT 1").fetchone())

_n = [0]
def plan(sql):
    _n[0] += 1
    return " | ".join(r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _n[0]))
def run(sql):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    out = con.execute(sql).fetchall()
    con.set_progress_handler(None, 0)
    return c[0], out

pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 110)
qs = [
    ("a.k = 42 (TEXT col, int literal)",  "SELECT * FROM a WHERE a.k = 42"),
    ("a.k = '42'",                        "SELECT * FROM a WHERE a.k = '42'"),
    ("b.k = 42",                          "SELECT * FROM b WHERE b.k = 42"),
    ("b.k = '42' (INT col, text literal)", "SELECT * FROM b WHERE b.k = '42'"),
    ("join a.k = b.k (TEXT vs INTEGER)",  "SELECT COUNT(*) FROM a JOIN b ON a.k = b.k"),
    ("join a.k = b.k + 0",                "SELECT COUNT(*) FROM a JOIN b ON a.k = b.k + 0"),
    ("join a.k = b.k || ''",              "SELECT COUNT(*) FROM a JOIN b ON a.k = b.k || ''"),
    ("join CAST(b.k AS TEXT) = a.k",      "SELECT COUNT(*) FROM a JOIN b ON CAST(b.k AS TEXT) = a.k"),
]
res = []
for name, q in qs:
    s, r = run(q)
    res.append((name, plan(q), s, r[0][0] if len(r) == 1 and len(r[0]) == 1 else len(r)))
print(pd.DataFrame(res, columns=["query", "plan", "vm_steps", "count_or_rows"]).to_string(index=False))

# the sneaky part: affinity changes which rows match, not just the plan
con.execute("INSERT INTO a VALUES (9001, '042', 0)")
print("\nrow k='042' in TEXT column a:")
print("  a.k = 42   ->", con.execute("SELECT COUNT(*) FROM a WHERE a.k = 42").fetchone()[0], "(42 is converted to text '42', which is not '042')")
print("  a.k = '42' ->", con.execute("SELECT COUNT(*) FROM a WHERE a.k = '42'").fetchone()[0])
print("  join a.k = b.k, rows with a.id=9001:", con.execute("SELECT COUNT(*) FROM a JOIN b ON a.k = b.k WHERE a.id = 9001").fetchone()[0],
      "(column vs column: numeric affinity is applied to the TEXT side, so '042' = 42)")
print("  join on a.k = CAST(b.k AS TEXT), rows with a.id=9001:", con.execute("SELECT COUNT(*) FROM a JOIN b ON a.k = CAST(b.k AS TEXT) WHERE a.id = 9001").fetchone()[0])
con.execute("DELETE FROM a WHERE id = 9001")

# pandas: merging a str key with an int key does not silently convert
da = pd.read_sql("SELECT * FROM a", con)
db = pd.read_sql("SELECT * FROM b", con)
print("\npandas dtypes:", da.k.dtype, db.k.dtype)
try:
    da.merge(db, on="k")
except ValueError as e:
    print("pandas merge on mismatched dtypes ->", type(e).__name__ + ":", str(e)[:100])
m = da.assign(k=da.k.astype("int64")).merge(db, on="k")
sql_n = con.execute("SELECT COUNT(*) FROM a JOIN b ON a.k = b.k").fetchone()[0]
assert len(m) == sql_n
print("after astype(int64): merge rows", len(m), "= SQL join count", sql_n)
