# Q10: UNION vs UNION ALL vs JOIN, and pandas concat vs merge.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE web_orders(order_id INTEGER, customer_id INTEGER, amount INTEGER);
CREATE TABLE store_orders(order_id INTEGER, customer_id INTEGER, amount INTEGER);
INSERT INTO web_orders   VALUES (1,10,100),(2,11,50),(3,12,75);
INSERT INTO store_orders VALUES (3,12,75),(4,10,100),(5,13,20);   -- order 3 is loaded in both channels
""")
run = lambda q: con.execute(q).fetchall()
sql_all = "SELECT * FROM web_orders UNION ALL SELECT * FROM store_orders"
sql_union = "SELECT * FROM web_orders UNION SELECT * FROM store_orders"
sql_chan = """SELECT 'web' AS channel, order_id, customer_id, amount FROM web_orders
UNION ALL SELECT 'store', order_id, customer_id, amount FROM store_orders"""
sql_proj_all = "SELECT customer_id, amount FROM web_orders UNION ALL SELECT customer_id, amount FROM store_orders"
sql_proj_union = "SELECT customer_id, amount FROM web_orders UNION SELECT customer_id, amount FROM store_orders"
sql_join = """SELECT w.order_id, w.amount AS web_amount, s.amount AS store_amount
FROM web_orders w JOIN store_orders s ON s.order_id = w.order_id"""
print("UNION ALL rows:", len(run(sql_all)), "| UNION rows:", len(run(sql_union)),
      "| with channel column:", len(run(sql_chan)))
print("UNION with the channel column:", len(run("SELECT 'web' AS channel, * FROM web_orders UNION SELECT 'store', * FROM store_orders")), "rows")
print("projected to (customer_id, amount): UNION ALL", len(run(sql_proj_all)), "rows, UNION", len(run(sql_proj_union)),
      "rows (orders 1 and 4 look identical and one vanished)")
print("JOIN side by side:", run(sql_join))
try:
    con.execute("SELECT order_id, amount FROM web_orders UNION ALL SELECT * FROM store_orders")
except sqlite3.OperationalError as e:
    print("column-count mismatch ->", e)

web = pd.read_sql("SELECT * FROM web_orders", con)
store = pd.read_sql("SELECT * FROM store_orders", con)
cat = pd.concat([web.assign(channel="web"), store.assign(channel="store")], ignore_index=True)
rows = lambda df: sorted(df.itertuples(index=False, name=None))
assert rows(pd.concat([web, store], ignore_index=True)) == sorted(run(sql_all))
assert rows(pd.concat([web, store], ignore_index=True).drop_duplicates()) == sorted(run(sql_union))
assert rows(cat[["channel", "order_id", "customer_id", "amount"]]) == sorted(run(sql_chan))
proj = pd.concat([web, store])[["customer_id", "amount"]]
assert len(proj) == 6 and len(proj.drop_duplicates()) == len(run(sql_proj_union)) == 4
j = web.merge(store, on="order_id", suffixes=("_web", "_store"))
assert rows(j[["order_id", "amount_web", "amount_store"]]) == sorted(run(sql_join))
print("pandas concat:", len(cat), "rows | concat+drop_duplicates (UNION):",
      len(pd.concat([web, store]).drop_duplicates()), "| merge on order_id:", len(j), "row")
print("asserts passed (all compared after sorting rows)")
