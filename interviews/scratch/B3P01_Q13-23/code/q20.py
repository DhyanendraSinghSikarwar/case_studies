# Column expressions, aliases, integer division, rounding, concatenation (Q20).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, qty INTEGER, unit_price REAL, discount_pct INTEGER);
INSERT INTO order_items VALUES
 (1,100,3,199.99,10),(2,100,5,49.50,0),(3,101,1,2.50,0),(4,101,2,15.25,25),(5,102,7,12.00,5);
""")

sql = """
SELECT item_id,
       qty * unit_price * (1 - discount_pct / 100.0)            AS line_total,
       ROUND(qty * unit_price * (1 - discount_pct / 100.0), 2)  AS "Line Total (rounded)",
       'Item ' || item_id || ' x' || qty                        AS label
FROM order_items
ORDER BY item_id
"""
sql_df = pd.read_sql(sql, con)
print(sql_df.to_string(index=False))

# the traps
print("qty / 2 (both integers):", con.execute("SELECT qty, qty / 2, qty / 2.0 FROM order_items ORDER BY item_id").fetchall())
print("discount_pct / 100 (integer):", con.execute("SELECT discount_pct, discount_pct / 100, discount_pct / 100.0 FROM order_items WHERE item_id IN (1,4)").fetchall())
print("alias in ORDER BY works:", con.execute("SELECT qty*unit_price AS gross FROM order_items ORDER BY gross DESC LIMIT 1").fetchall())
try:
    print("alias in WHERE (SQLite accepts it as an extension):", con.execute("SELECT qty*unit_price AS gross FROM order_items WHERE gross > 100 ORDER BY item_id").fetchall())
except sqlite3.Error as e:
    print("alias in WHERE ->", e)
print("'Item ' || NULL ->", con.execute("SELECT 'Item ' || NULL").fetchone()[0])
print("'5' + 3 =", con.execute("SELECT '5' + 3").fetchone()[0], "| typeof('5' + 3) =", con.execute("SELECT typeof('5' + 3)").fetchone()[0])

# pandas
oi = pd.read_sql("SELECT * FROM order_items", con)
p = (oi.assign(line_total=lambda d: d["qty"] * d["unit_price"] * (1 - d["discount_pct"] / 100),
               rounded=lambda d: d["line_total"].round(2),
               label=lambda d: "Item " + d["item_id"].astype(str) + " x" + d["qty"].astype(str))
       [["item_id", "line_total", "rounded", "label"]]
       .rename(columns={"rounded": "Line Total (rounded)"}))
pd.testing.assert_frame_equal(sql_df, p)
print("asserts passed: SQL == pandas (ordered by item_id, round to 2 places; float values agree exactly here)")

# pandas / in Python is TRUE division; SQL integer / is truncating. Match with //.
print("pandas qty / 2:", (oi["qty"] / 2).tolist(), "| qty // 2:", (oi["qty"] // 2).tolist())
assert (oi["qty"] // 2).tolist() == [r[0] for r in con.execute("SELECT qty / 2 FROM order_items ORDER BY item_id")]

# honest surprise: halves round differently. SQLite rounds half away from zero, numpy rounds half to even.
print("ROUND(2.5), ROUND(3.5) in SQLite:", con.execute("SELECT ROUND(2.5), ROUND(3.5)").fetchone())
print("pandas Series([2.5, 3.5]).round():", pd.Series([2.5, 3.5]).round().tolist())
