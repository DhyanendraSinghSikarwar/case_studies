# SELECT DISTINCT vs GROUP BY, NULLs, COUNT(DISTINCT) variants (Q19).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, city TEXT);
INSERT INTO orders VALUES
 (1,10,'paid','Pune'),(2,10,'paid','Pune'),(3,10,'paid','Delhi'),
 (4,20,'refunded','Pune'),(5,20,NULL,'Pune'),(6,30,NULL,NULL),
 (7,NULL,'paid','Delhi'),(8,NULL,'paid','Delhi');
""")
def rows(q): return con.execute(q).fetchall()

d1 = "SELECT DISTINCT status FROM orders ORDER BY status"
d2 = "SELECT DISTINCT customer_id, city FROM orders ORDER BY customer_id, city"
g1 = "SELECT status FROM orders GROUP BY status ORDER BY status"
print("DISTINCT status:", rows(d1))
print("GROUP BY status:", rows(g1), "(same rows)")
print("DISTINCT customer_id, city:", rows(d2))
assert rows(d1) == rows(g1)

print("COUNT(DISTINCT customer_id):", rows("SELECT COUNT(DISTINCT customer_id) FROM orders")[0][0], "(NULL not counted)")
print("COUNT(*) over DISTINCT customer_id subquery:", rows("SELECT COUNT(*) FROM (SELECT DISTINCT customer_id FROM orders)")[0][0], "(NULL counted as a value)")
try:
    con.execute("SELECT COUNT(DISTINCT customer_id, city) FROM orders")
except sqlite3.Error as e:
    print("COUNT(DISTINCT a, b) in SQLite ->", type(e).__name__, e)
portable = "SELECT COUNT(*) FROM (SELECT DISTINCT customer_id, city FROM orders)"
print("pairs via subquery (NULL pairs kept):", rows(portable)[0][0])
only_complete = "SELECT COUNT(*) FROM (SELECT DISTINCT customer_id, city FROM orders WHERE customer_id IS NOT NULL AND city IS NOT NULL)"
print("pairs with no NULLs (what a multi-column COUNT(DISTINCT) would give where supported):", rows(only_complete)[0][0])

# GROUP BY is needed when you also aggregate
agg = "SELECT customer_id, COUNT(*) AS n_orders, COUNT(DISTINCT city) AS n_cities FROM orders GROUP BY customer_id ORDER BY customer_id"
print("GROUP BY with aggregates:", rows(agg))

# pandas
df = pd.read_sql("SELECT * FROM orders", con)
p1 = df[["status"]].drop_duplicates().sort_values("status", na_position="first").reset_index(drop=True)
print("pandas drop_duplicates on status:", p1["status"].tolist())
print("unique():", df["status"].unique().tolist())
print("nunique() default dropna=True:", df["customer_id"].nunique(), "| dropna=False:", df["customer_id"].nunique(dropna=False))
p2 = df[["customer_id", "city"]].drop_duplicates()
print("pairs via drop_duplicates:", len(p2), "| NULL-free pairs:", len(p2.dropna()))
sql_d2 = pd.read_sql(d2, con)
p2s = p2.sort_values(["customer_id", "city"], na_position="first").reset_index(drop=True)
assert list(map(tuple, sql_d2.astype(object).where(sql_d2.notna(), None).values.tolist())) == \
       list(map(tuple, p2s.astype(object).where(p2s.notna(), None).values.tolist()))
sql_agg = pd.read_sql(agg, con)
p_agg = (df.groupby("customer_id", dropna=False).agg(n_orders=("order_id", "size"), n_cities=("city", "nunique"))
         .reset_index().sort_values("customer_id", na_position="first").reset_index(drop=True))
pd.testing.assert_frame_equal(sql_agg, p_agg, check_dtype=False)
assert rows("SELECT COUNT(DISTINCT customer_id) FROM orders")[0][0] == df["customer_id"].nunique()
assert rows(portable)[0][0] == len(p2) and rows(only_complete)[0][0] == len(p2.dropna())
print("asserts passed (sorted with NULL first, as SQLite does)")
