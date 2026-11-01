# Q22: type affinity and text-versus-number traps in SQLite, STRICT tables, and the pandas equivalents.
import io
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE items(item_id INTEGER PRIMARY KEY, price_text TEXT, qty INTEGER, code);   -- code: no declared type
""")
csv_text = "item_id,price_text,qty,code\n1,9,3,9\n2,10,12,10\n3,100,7,100\n4,2.5,5,2.5\n"
rows = [tuple(line.split(",")) for line in csv_text.strip().split("\n")[1:]]   # every field arrives as a str, like a CSV
con.executemany("INSERT INTO items VALUES (?,?,?,?)", rows)
print("typeof:", con.execute("SELECT typeof(price_text), typeof(qty), typeof(code) FROM items WHERE item_id = 1").fetchone())

sql_text_order = "SELECT price_text FROM items ORDER BY price_text"
sql_cast_order = "SELECT price_text FROM items ORDER BY CAST(price_text AS REAL)"
sql_len_order  = "SELECT price_text FROM items ORDER BY LENGTH(price_text), price_text"
col = lambda q: [r[0] for r in con.execute(q).fetchall()]
print("ORDER BY price_text            :", col(sql_text_order))
print("ORDER BY CAST(.. AS REAL)      :", col(sql_cast_order))
print("ORDER BY LENGTH(x), x (breaks) :", col(sql_len_order))

print("literals  '10'<'9':", con.execute("SELECT '10' < '9'").fetchone()[0],
      "| 10<'9':", con.execute("SELECT 10 < '9'").fetchone()[0],
      "| '1'=1:", con.execute("SELECT '1' = 1").fetchone()[0])
cmp = lambda q: con.execute(q).fetchone()[0]
print("TEXT col  price_text < 9 (rows true):", cmp("SELECT COUNT(*) FROM items WHERE price_text < 9"))
print("no-type   code < 9       (rows true):", cmp("SELECT COUNT(*) FROM items WHERE code < 9"))
print("INTEGER   qty < '9'      (rows true):", cmp("SELECT COUNT(*) FROM items WHERE qty < '9'"))
print("TEXT col  price_text = 9 (rows true):", cmp("SELECT COUNT(*) FROM items WHERE price_text = 9"))
print("no-type   code = 9       (rows true):", cmp("SELECT COUNT(*) FROM items WHERE code = 9"))

# what each declared affinity does to the same input strings
con.executescript("CREATE TABLE aff(i INTEGER, n NUMERIC, r REAL, t TEXT, a);")
for v in ("12", " 12", "12 ", "1e3", "2.50", "007", "0x10", "abc"):
    con.execute("INSERT INTO aff VALUES (?,?,?,?,?)", (v,) * 5)
print("raw value | INTEGER | NUMERIC | REAL | TEXT | no type")
for r in con.execute("SELECT quote(t), typeof(i)||':'||quote(i), typeof(n)||':'||quote(n), typeof(r)||':'||quote(r), typeof(t), typeof(a) FROM aff"):
    print("  ", " | ".join(r))

# STRICT tables (SQLite 3.37+)
con.executescript("CREATE TABLE s(a INTEGER, b TEXT, c ANY) STRICT;")
for label, args in [("'12' into INTEGER", ("12", "x", 1)), ("' 12' into INTEGER", (" 12", "x", 1)),
                    ("'abc' into INTEGER", ("abc", "x", 1)), ("2.5 into INTEGER", (2.5, "x", 1)),
                    ("3.0 into INTEGER", (3.0, "x", 1)), ("5 into TEXT", (1, 5, 1)), ("'z' into ANY", (1, "x", "z"))]:
    try:
        con.execute("INSERT INTO s VALUES (?,?,?)", args); print("  STRICT ok  :", label)
    except sqlite3.Error as e:
        print("  STRICT FAIL:", label, "->", e)
print("  stored:", con.execute("SELECT a, typeof(a), b, typeof(b), c, typeof(c) FROM s").fetchall())

# natural sort of codes with a text prefix
con.executescript("CREATE TABLE codes(c TEXT); INSERT INTO codes VALUES ('A9'),('A10'),('A100'),('A2');")
sql_nat = "SELECT c FROM codes ORDER BY CAST(SUBSTR(c, 2) AS INTEGER)"
print("plain order:", col("SELECT c FROM codes ORDER BY c"), "| natural order:", col(sql_nat))

# pandas
df = pd.read_sql("SELECT * FROM items ORDER BY item_id", con)
print("pandas dtypes from SQL:", dict(df.dtypes.astype(str)))   # price_text stays str, qty int64
as_text = pd.read_csv(io.StringIO(csv_text), dtype=str)
as_num = pd.read_csv(io.StringIO(csv_text))
print("read_csv default dtypes:", dict(as_num.dtypes.astype(str)))
print("string sort :", as_text["price_text"].sort_values().tolist())
print("numeric sort:", as_num["price_text"].sort_values().tolist())
nat = pd.Series(["A9", "A10", "A100", "A2"])
nat_sorted = nat.sort_values(key=lambda s: s.str.extract(r"(\d+)", expand=False).astype(int)).tolist()
print("natural key :", nat_sorted)
na_csv = pd.read_csv(io.StringIO("code,n\nNA,1\nnull,2\nNone,3\nN/A,4\nnan,5\nxyz,6\n"))
print("read_csv NA markers -> NaN:", na_csv["code"].isna().tolist(), "| keep_default_na=False:",
      pd.read_csv(io.StringIO("code,n\nNA,1\nnull,2\nxyz,3\n"), keep_default_na=False)["code"].tolist())

assert col(sql_text_order) == sorted(as_text["price_text"]) == ["10", "100", "2.5", "9"]
assert col(sql_cast_order) == as_text.sort_values("price_text", key=lambda s: s.astype(float))["price_text"].tolist() == ["2.5", "9", "10", "100"]
assert col(sql_nat) == nat_sorted == ["A2", "A9", "A10", "A100"]
print("asserts passed (SQL == pandas for the three orderings)")
