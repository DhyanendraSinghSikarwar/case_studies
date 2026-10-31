# Q44: reconcile orders with partial payments: aggregate payments first, status per order, orphan payments, tie-out
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, amount INTEGER);
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, order_id INTEGER, paid_amount INTEGER);
INSERT INTO orders VALUES (1,100),(2,200),(3,50),(4,80),(5,120);
INSERT INTO payments VALUES
 (1,1,100),            -- order 1 paid in full
 (2,2,120),(3,2,50),   -- order 2 partial (170 of 200)
 (4,3,60),             -- order 3 overpaid
 (5,5,70),(6,5,50),    -- order 5 paid in full with two payments
 (7,99,40),            -- orphan: unknown order
 (8,NULL,25);          -- orphan: no order id at all
"""
SQL_MAIN = """
SELECT o.order_id, o.amount, COALESCE(p.paid, 0) AS paid,
       CASE WHEN p.paid IS NULL THEN 'unpaid'
            WHEN p.paid < o.amount THEN 'partial'
            WHEN p.paid = o.amount THEN 'paid'
            ELSE 'overpaid' END AS status
FROM orders o
LEFT JOIN (SELECT order_id, SUM(paid_amount) AS paid FROM payments GROUP BY order_id) p
       ON p.order_id = o.order_id
ORDER BY o.order_id
"""
SQL_ORPHANS = """
SELECT pm.payment_id, pm.order_id, pm.paid_amount
FROM payments pm LEFT JOIN orders o ON o.order_id = pm.order_id
WHERE o.order_id IS NULL
ORDER BY pm.payment_id
"""
SQL_WRONG = """
SELECT SUM(o.amount) AS inflated_order_total
FROM orders o JOIN payments pm ON pm.order_id = o.order_id
"""
# the single-pass FULL JOIN structure: one row per order, plus one row per orphan order_id group
SQL_FULL = """
SELECT COALESCE(o.order_id, p.order_id) AS order_id, o.amount, p.paid,
       CASE WHEN o.order_id IS NULL THEN 'orphan' WHEN p.paid IS NULL THEN 'unpaid'
            WHEN p.paid < o.amount THEN 'partial' WHEN p.paid = o.amount THEN 'paid' ELSE 'overpaid' END AS status
FROM orders o
FULL JOIN (SELECT order_id, SUM(paid_amount) AS paid FROM payments GROUP BY order_id) p ON p.order_id = o.order_id
ORDER BY order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_orph = pd.read_sql_query(SQL_ORPHANS, con)
print("status per order:"); print(sql_df.to_string(index=False))
print("\norphan payments:"); print(sql_orph.to_string(index=False))
print("\nFULL JOIN version (NULL order_id group sorts first):"); print(pd.read_sql_query(SQL_FULL, con).to_string(index=False))
print("\ntrue order total:", con.execute("SELECT SUM(amount) FROM orders").fetchone()[0],
      "| joined straight to payments:", con.execute(SQL_WRONG).fetchone()[0])

# pandas
orders = pd.read_sql_query("SELECT * FROM orders", con)
payments = pd.read_sql_query("SELECT * FROM payments", con)
print("\npayments.order_id dtype:", payments["order_id"].dtype, "(NULL became NaN)")
paid = payments.groupby("order_id", as_index=False).agg(paid=("paid_amount", "sum"))     # NaN order_id group is dropped by default
m = orders.merge(paid, on="order_id", how="left", validate="one_to_one")
m["paid"] = m["paid"].fillna(0).astype("int64")
m["status"] = "overpaid"
m.loc[m["paid"] == m["amount"], "status"] = "paid"
m.loc[m["paid"] < m["amount"], "status"] = "partial"
m.loc[m["paid"] == 0, "status"] = "unpaid"
p_df = m[["order_id", "amount", "paid", "status"]].sort_values("order_id").reset_index(drop=True)
chk = payments.merge(orders[["order_id"]], on="order_id", how="left", indicator=True)
p_orph = (chk[chk["_merge"] == "left_only"][["payment_id", "order_id", "paid_amount"]]
          .sort_values("payment_id").reset_index(drop=True))
pd.testing.assert_frame_equal(sql_df, p_df, check_dtype=False)
pd.testing.assert_frame_equal(sql_orph, p_orph, check_dtype=False)
print("asserts passed: status table and orphan list equal SQL (sorted by order_id / payment_id)")

# tie-out: every payment is either on a known order or an orphan
total_paid = int(payments["paid_amount"].sum())
matched = int(p_df["paid"].sum())
orph = int(p_orph["paid_amount"].sum())
print(f"tie-out: total payments {total_paid} = matched {matched} + orphan {orph}")
assert total_paid == matched + orph
g_total = int(paid["paid"].sum())
print("sum of the groupby result (default dropna=True):", g_total, "vs total payments", total_paid,
      "-> the NaN-order_id payment of", total_paid - g_total, "is silently missing from it")
assert total_paid - g_total == 25
sql_tie = con.execute("SELECT (SELECT SUM(paid_amount) FROM payments), "
                      "(SELECT SUM(pm.paid_amount) FROM payments pm JOIN orders o ON o.order_id = pm.order_id), "
                      "(SELECT SUM(paid_amount) FROM payments pm WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.order_id = pm.order_id))").fetchone()
print("SQL tie-out (all, matched, orphan):", sql_tie)
assert sql_tie == (total_paid, matched, orph)
con.close()
