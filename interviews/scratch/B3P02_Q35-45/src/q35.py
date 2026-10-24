# Q35: merge key dtype mismatch (int64 vs str/object/float64), silent drops, fix, SQLite implicit casting
import io
import sqlite3
import warnings
import pandas as pd

CSV = "order_id,customer_id\n10,1\n11,2 \n12,3\n13,\n14,3\n15,7\n"   # '2 ' has a trailing space, 13 has no key, 15 is unknown
customers = pd.DataFrame({"customer_id": [1, 2, 3, 4], "name": ["Asha", "Ben", "Chitra", "Dev"]})
print("customers key dtype:", customers["customer_id"].dtype)

# 1) every column read as text (what an object/str column looks like): int64 vs text raises
orders_txt = pd.read_csv(io.StringIO(CSV), dtype=str)
print("orders key dtype (dtype=str):", orders_txt["customer_id"].dtype)
try:
    customers.merge(orders_txt, on="customer_id")
except ValueError as e:
    print("int64 vs str ->", type(e).__name__ + ":", e)
orders_obj = pd.read_csv(io.StringIO(CSV), dtype=object)
try:
    customers.merge(orders_obj, on="customer_id")
except ValueError as e:
    print("int64 vs object ->", type(e).__name__ + ":", e)

# 1b) text on BOTH sides: no error at all, the '2 ' row just fails to match
cust_txt = customers.assign(customer_id=customers["customer_id"].astype(str))
t = orders_txt.merge(cust_txt, on="customer_id", how="left", indicator=True)
print("\ntext vs text, no strip: unmatched order_ids:", t.loc[t["_merge"] == "left_only", "order_id"].tolist())

# 2) silent wrong result: an object column holding a mix of ints and strings does NOT raise
mixed = pd.DataFrame({"order_id": [10, 11, 12], "customer_id": pd.Series([1, "2", 3], dtype=object)})
m = mixed.merge(customers, on="customer_id", how="left", indicator=True)
print("\nmixed object key (1, '2', 3), orders LEFT JOIN customers:")
print(m[["order_id", "customer_id", "name", "_merge"]].to_string(index=False))

# 3) float64 key because of the blank (NaN): matches ints, no error, but NaN row can never match
orders_default = pd.read_csv(io.StringIO(CSV.replace("2 ", "2")))
print("\ndefault read_csv key dtype:", orders_default["customer_id"].dtype)
print(orders_default.merge(customers, on="customer_id", how="left", indicator=True)
      [["order_id", "customer_id", "name", "_merge"]].to_string(index=False))

# 4) the fix: strip, convert to numbers (errors -> NaN), nullable Int64, then merge and check unmatched
orders = orders_txt.copy()
orders["order_id"] = orders["order_id"].astype("int64")
orders["customer_id"] = pd.to_numeric(orders["customer_id"].str.strip(), errors="coerce").astype("Int64")
print("\nafter fix, key dtype:", orders["customer_id"].dtype)
p = orders.merge(customers, on="customer_id", how="left", indicator=True)
p = p[["order_id", "customer_id", "name", "_merge"]].sort_values("order_id").reset_index(drop=True)
print(p.to_string())
unmatched = p[p["_merge"] != "both"]
print("unmatched orders:", unmatched["order_id"].tolist())
assert unmatched["order_id"].tolist() == [13, 15]       # blank key and unknown customer 7

# 5) the same in SQL (SQLite): orders loaded as TEXT, as a CSV import would give
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders_raw(order_id INTEGER, customer_id TEXT);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders_raw VALUES (10,'1'),(11,'2 '),(12,'3'),(13,NULL),(14,'3'),(15,'7');
""")
SQL_IMPLICIT = """
SELECT o.order_id, c.name FROM orders_raw o LEFT JOIN customers c ON c.customer_id = o.customer_id
ORDER BY o.order_id
"""
SQL_FIX = """
SELECT o.order_id, CAST(NULLIF(TRIM(o.customer_id), '') AS INTEGER) AS customer_id, c.name,
       CASE WHEN c.customer_id IS NULL THEN 'left_only' ELSE 'both' END AS _merge
FROM orders_raw o
LEFT JOIN customers c ON c.customer_id = CAST(NULLIF(TRIM(o.customer_id), '') AS INTEGER)
ORDER BY o.order_id
"""
print("\nSQLite implicit cast (TEXT vs INTEGER column, no TRIM):", con.execute(SQL_IMPLICIT).fetchall())
print("SQLite literal compare 1 = '1':", con.execute("SELECT 1 = '1'").fetchone()[0],
      "| '2 ' as number:", con.execute("SELECT CAST('2 ' AS INTEGER)").fetchone()[0],
      "| CAST('x' AS INTEGER):", con.execute("SELECT CAST('x' AS INTEGER)").fetchone()[0],
      "| CAST('' AS INTEGER):", con.execute("SELECT CAST('' AS INTEGER)").fetchone()[0])
s = pd.read_sql_query(SQL_FIX, con)
s["customer_id"] = s["customer_id"].astype("Int64")
s["_merge"] = pd.Categorical(s["_merge"], categories=["left_only", "right_only", "both"])  # same categories as indicator=True
print(s.to_string())
pd.testing.assert_frame_equal(s[["order_id", "customer_id", "name", "_merge"]], p, check_dtype=False)
print("SQL fix == pandas fix (sorted by order_id)")

# 6) a bad text value: pandas coerce gives NaN like NULLIF; SQLite CAST silently gives 0
print("\nto_numeric coerce on ['1',' 2','x']:",
      pd.to_numeric(pd.Series(["1", " 2", "x"]).str.strip(), errors="coerce").tolist())
try:
    pd.Series(["1", "x"]).astype("Int64")
except (ValueError, TypeError) as e:
    print("astype('Int64') on 'x' ->", type(e).__name__ + ":", e)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    customers.merge(pd.DataFrame({"customer_id": [1.0, 2.5]}), on="customer_id")
print("int64 vs float64 with a non-integer float:", [str(x.message)[:60] for x in w])
try:
    pd.Series([1.5]).astype("Int64")
except (ValueError, TypeError) as e:
    print("astype('Int64') on 1.5 ->", type(e).__name__ + ":", e)
print("astype('Int64') on ['1', ' 2'] without strip:", pd.Series(["1", " 2"]).astype("Int64").tolist(),
      "| to_numeric without strip:", pd.to_numeric(pd.Series(["1", " 2"])).tolist())
# NaN keys on BOTH sides: pandas matches NaN with NaN (SQL never matches NULL = NULL)
left_nan = pd.DataFrame({"customer_id": [1.0, None], "name": ["Asha", "Unknown"]})
right_nan = pd.DataFrame({"customer_id": [None, 3.0], "order_id": [13, 12]})
both = left_nan.merge(right_nan, on="customer_id", how="inner")
print("NaN key on both sides, inner merge rows:", both[["name", "order_id"]].values.tolist())
sql_nan = sqlite3.connect(":memory:").execute(
    "SELECT COUNT(*) FROM (SELECT NULL AS k) a JOIN (SELECT NULL AS k) b ON a.k = b.k").fetchone()[0]
print("SQL NULL = NULL join rows:", sql_nan)
con.close()
