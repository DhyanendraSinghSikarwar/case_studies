# Q28: chargeback rate by merchant category without fan-out.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE merchants(merchant_id INTEGER PRIMARY KEY, category TEXT);
CREATE TABLE card_payments(payment_id INTEGER PRIMARY KEY, merchant_id INTEGER, amount INTEGER);
CREATE TABLE chargebacks(chargeback_id INTEGER PRIMARY KEY, payment_id INTEGER, amount INTEGER);
INSERT INTO merchants VALUES (1,'travel'),(2,'travel'),(3,'grocery'),(4,'gaming');
INSERT INTO card_payments VALUES
 (1,1,1000),(2,1,2000),(3,2,500),(4,2,700),(5,3,300),(6,3,400),(7,3,350),(8,3,250),(9,4,900);
INSERT INTO chargebacks VALUES (1,1,600),(2,1,400),(3,3,500),(4,5,300);
"""
SQL_NAIVE = """
SELECT m.category, COUNT(*) AS payments, SUM(c.amount) AS chargeback_amount
FROM card_payments p
JOIN merchants m ON m.merchant_id = p.merchant_id
LEFT JOIN chargebacks c ON c.payment_id = p.payment_id
GROUP BY m.category
ORDER BY m.category
"""
SQL = """
WITH cb AS (
  SELECT payment_id, SUM(amount) AS cb_amount
  FROM chargebacks
  GROUP BY payment_id
)
SELECT m.category,
       COUNT(*) AS payments,
       COUNT(cb.payment_id) AS payments_with_cb,
       ROUND(1.0 * COUNT(cb.payment_id) / COUNT(*), 4) AS cb_rate,
       COALESCE(SUM(cb.cb_amount), 0) AS chargeback_amount
FROM card_payments p
JOIN merchants m ON m.merchant_id = p.merchant_id
LEFT JOIN cb ON cb.payment_id = p.payment_id
GROUP BY m.category
ORDER BY m.category
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
naive = pd.read_sql(SQL_NAIVE, con)
print("naive join (payment 1 has two chargebacks):")
print(naive.to_string(index=False))
s = pd.read_sql(SQL, con)
print("\npre-aggregated:")
print(s.to_string(index=False))

pay = pd.read_sql("SELECT * FROM card_payments", con)
mer = pd.read_sql("SELECT * FROM merchants", con)
cbs = pd.read_sql("SELECT * FROM chargebacks", con)
# PANDAS START
cb = cbs.groupby("payment_id", as_index=False)["amount"].sum().rename(columns={"amount": "cb_amount"})
d = pay.merge(mer, on="merchant_id").merge(cb, on="payment_id", how="left")
p = (d.groupby("category")
       .agg(payments=("payment_id", "size"),
            payments_with_cb=("cb_amount", "count"),
            chargeback_amount=("cb_amount", "sum"))
       .reset_index())
p["cb_rate"] = (p["payments_with_cb"] / p["payments"]).round(4)
p = p[["category", "payments", "payments_with_cb", "cb_rate", "chargeback_amount"]].sort_values("category").reset_index(drop=True)
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (ordered by category)")

nv = pay.merge(mer, on="merchant_id").merge(cbs, on="payment_id", how="left")
print("pandas naive merge rows:", len(nv), "vs payments:", len(pay))
