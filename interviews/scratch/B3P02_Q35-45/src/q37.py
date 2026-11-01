# Q37: market-basket pairs with a self join: dedupe lines, a < b, GROUP BY pair, top N
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE order_items(order_id INTEGER, product_id TEXT);
INSERT INTO order_items VALUES
 (1,'A'),(1,'B'),(1,'C'),
 (2,'A'),(2,'B'),
 (3,'A'),(3,'C'),
 (4,'B'),(4,'C'),(4,'A'),
 (5,'A'),(5,'B'),(5,'B'),
 (6,'D');
"""
SQL_MAIN = """
SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS n_orders
FROM (SELECT DISTINCT order_id, product_id FROM order_items) a
JOIN (SELECT DISTINCT order_id, product_id FROM order_items) b ON a.order_id = b.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
ORDER BY n_orders DESC, p1, p2
LIMIT 10
"""
SQL_NAIVE = """
SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS n_orders
FROM order_items a
JOIN order_items b ON a.order_id = b.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
ORDER BY n_orders DESC, p1, p2
LIMIT 10
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL (deduplicated baskets):")
print(sql_df.to_string(index=False))
print("\nSQL naive (duplicate line not removed):")
naive = pd.read_sql_query(SQL_NAIVE, con)
print(naive.to_string(index=False))

# pandas: dedupe lines, self-merge on order_id, keep p1 < p2, count pairs
items = pd.read_sql_query("SELECT * FROM order_items", con)
basket = items.drop_duplicates()
pairs = basket.merge(basket, on="order_id", suffixes=("_1", "_2"))
pairs = pairs[pairs["product_id_1"] < pairs["product_id_2"]]
counts = pairs[["product_id_1", "product_id_2"]].value_counts()      # a Series indexed by the pair
p_df = (counts.rename("n_orders").reset_index()
        .rename(columns={"product_id_1": "p1", "product_id_2": "p2"})
        .sort_values(["n_orders", "p1", "p2"], ascending=[False, True, True])
        .head(10).reset_index(drop=True))
print("\npandas (value_counts after the filtered self-merge):")
print(p_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, p_df, check_dtype=False)
print("SQL == pandas (compared in the order n_orders desc, p1, p2)")

# row growth: a basket of n distinct products produces n(n-1)/2 pair rows
for n in (3, 10, 100):
    con.execute("DELETE FROM order_items WHERE order_id = 99")
    con.executemany("INSERT INTO order_items VALUES (99, ?)", [(f"P{i:03d}",) for i in range(n)])
    rows = con.execute("""SELECT COUNT(*) FROM order_items a JOIN order_items b
                          ON a.order_id = b.order_id AND a.product_id < b.product_id
                          WHERE a.order_id = 99""").fetchone()[0]
    print(f"basket of {n:>3} products -> {rows} pair rows (n(n-1)/2 = {n*(n-1)//2})")
con.close()
