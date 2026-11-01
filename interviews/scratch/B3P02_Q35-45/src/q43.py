# Q43: join dialect map: run each feature on SQLite 3.45 and record what happens (other engines are NOT executed)
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE l(id INTEGER, v TEXT);
CREATE TABLE r(id INTEGER, w TEXT);
INSERT INTO l VALUES (1,'l1'),(2,'l2'),(3,'l3');
INSERT INTO r VALUES (2,'r2'),(3,'r3'),(4,'r4');
""")
print("SQLite version:", sqlite3.sqlite_version)

def attempt(q):
    try:
        cur = con.execute(q)
        rows = cur.fetchall()
        return [d[0] for d in cur.description], rows
    except sqlite3.Error as e:
        return None, f"{type(e).__name__}: {e}"

l = pd.read_sql_query("SELECT * FROM l", con)
r = pd.read_sql_query("SELECT * FROM r", con)

# 1. join types: row counts, compared with pandas how=
checks = {
    "INNER JOIN":      ("SELECT * FROM l INNER JOIN r ON l.id = r.id", l.merge(r, on="id", how="inner")),
    "LEFT JOIN":       ("SELECT * FROM l LEFT JOIN r ON l.id = r.id", l.merge(r, on="id", how="left")),
    "RIGHT JOIN":      ("SELECT * FROM l RIGHT JOIN r ON l.id = r.id", l.merge(r, on="id", how="right")),
    "FULL OUTER JOIN": ("SELECT * FROM l FULL OUTER JOIN r ON l.id = r.id", l.merge(r, on="id", how="outer")),
    "CROSS JOIN":      ("SELECT * FROM l CROSS JOIN r", l.merge(r, how="cross")),
    "comma join":      ("SELECT * FROM l, r", l.merge(r, how="cross")),
}
print("\njoin type: SQLite rows | pandas rows")
for name, (q, pdf) in checks.items():
    cols, rows = attempt(q)
    assert isinstance(rows, list) and len(rows) == len(pdf), name
    print(f"{name:>16}: {len(rows)} | {len(pdf)}")
# RIGHT JOIN is the LEFT JOIN with the tables swapped (same rows, columns in a different order)
a = sorted(map(tuple, con.execute("SELECT r.id, r.w, l.v FROM l RIGHT JOIN r ON l.id = r.id").fetchall()), key=str)
b = sorted(map(tuple, con.execute("SELECT r.id, r.w, l.v FROM r LEFT JOIN l ON l.id = r.id").fetchall()), key=str)
assert a == b
print("RIGHT JOIN == swapped LEFT JOIN: True")

# 2. set operators
for name, q in [("INTERSECT", "SELECT id FROM l INTERSECT SELECT id FROM r"),
                ("EXCEPT", "SELECT id FROM l EXCEPT SELECT id FROM r"),
                ("MINUS", "SELECT id FROM l MINUS SELECT id FROM r")]:
    cols, rows = attempt(q)
    print(f"{name:>9}: {rows}")
assert [x[0] for x in con.execute("SELECT id FROM l INTERSECT SELECT id FROM r ORDER BY id")] == sorted(set(l.id) & set(r.id))
assert [x[0] for x in con.execute("SELECT id FROM l EXCEPT SELECT id FROM r ORDER BY id")] == sorted(set(l.id) - set(r.id))

# 3. USING / NATURAL / ON: which columns does SELECT * return, and in what order
print("\nSELECT * column lists:")
for name, q in [("ON", "SELECT * FROM l JOIN r ON l.id = r.id"),
                ("USING (id)", "SELECT * FROM l JOIN r USING (id)"),
                ("NATURAL JOIN", "SELECT * FROM l NATURAL JOIN r"),
                ("RIGHT JOIN USING", "SELECT * FROM l RIGHT JOIN r USING (id)"),
                ("FULL JOIN USING", "SELECT * FROM l FULL JOIN r USING (id)")]:
    cols, rows = attempt(q)
    print(f"{name:>17}: {cols}")
print("FULL JOIN USING rows:", attempt("SELECT * FROM l FULL JOIN r USING (id) ORDER BY id")[1])
print("qualified l.id with USING in a FULL JOIN:", attempt("SELECT l.id, r.id FROM l FULL JOIN r USING (id) ORDER BY 1, 2")[1])
print("pandas merge on='id' columns:", list(l.merge(r, on="id").columns),
      "| left_on/right_on columns:", list(l.merge(r.rename(columns={"id": "rid"}), left_on="id", right_on="rid").columns))

# 4. null-safe equality spellings and LATERAL
print("\nnull-safe equality in SQLite: NULL IS NULL ->", con.execute("SELECT NULL IS NULL").fetchone()[0],
      "| NULL IS NOT DISTINCT FROM NULL ->", con.execute("SELECT NULL IS NOT DISTINCT FROM NULL").fetchone()[0],
      "| NULL <=> NULL ->", attempt("SELECT NULL <=> NULL")[1])
print("LATERAL:", attempt("SELECT * FROM l, LATERAL (SELECT * FROM r WHERE r.id = l.id)")[1])
con.close()
