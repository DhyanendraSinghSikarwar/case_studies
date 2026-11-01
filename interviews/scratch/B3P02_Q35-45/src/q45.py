# Q45: revenue by promo code when customers hold several codes: dedupe, then three allocation policies, with tie-out
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE promo_codes(code TEXT, customer_id INTEGER);          -- duplicates possible
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO promo_codes VALUES ('SAVE10',1),('SAVE10',1),('VIP',1),('SAVE10',2),('VIP',3),('FEST',3);
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,2,80),(4,3,60),(5,3,40),(6,4,30);
"""
DEDUP = "(SELECT DISTINCT code, customer_id FROM promo_codes)"
SQL_NAIVE = """
SELECT p.code, SUM(o.amount) AS revenue
FROM promo_codes p JOIN orders o ON o.customer_id = p.customer_id
GROUP BY p.code ORDER BY p.code
"""
SQL_ONCE = f"""
SELECT p.code, SUM(o.amount) AS revenue
FROM {DEDUP} p JOIN orders o ON o.customer_id = p.customer_id
GROUP BY p.code ORDER BY p.code
"""
SQL_SPLIT = f"""
SELECT p.code, SUM(o.amount * 1.0 / n.n_codes) AS revenue
FROM {DEDUP} p
JOIN (SELECT customer_id, COUNT(*) AS n_codes FROM {DEDUP} GROUP BY customer_id) n ON n.customer_id = p.customer_id
JOIN orders o ON o.customer_id = p.customer_id
GROUP BY p.code ORDER BY p.code
"""
SQL_PICK = """
SELECT p.code, SUM(o.amount) AS revenue
FROM (SELECT customer_id, MIN(code) AS code FROM promo_codes GROUP BY customer_id) p
JOIN orders o ON o.customer_id = p.customer_id
GROUP BY p.code ORDER BY p.code
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
total_orders = con.execute("SELECT SUM(amount) FROM orders").fetchone()[0]
with_code = con.execute("SELECT SUM(amount) FROM orders WHERE customer_id IN (SELECT customer_id FROM promo_codes)").fetchone()[0]
print("order total:", total_orders, "| orders of customers holding at least one code:", with_code)
sql = {k: dict(con.execute(q).fetchall()) for k, q in
       [("naive", SQL_NAIVE), ("once per code", SQL_ONCE), ("split equally", SQL_SPLIT), ("pick one (MIN code)", SQL_PICK)]}
for k, v in sql.items():
    print(f"{k:>20}: {v}  sum = {sum(v.values())}")

# pandas
promo = pd.read_sql_query("SELECT * FROM promo_codes", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
print("\nduplicate promo rows:", int(promo.duplicated().sum()))
try:
    orders.merge(promo, on="customer_id", validate="many_to_one")
except pd.errors.MergeError as e:
    print("validate='many_to_one' on the promo table ->", type(e).__name__ + ":", e)
pd_dedup = promo.drop_duplicates()
once = orders.merge(pd_dedup, on="customer_id", validate="many_to_many")          # many-to-many on purpose, after de-duplication
p_once = once.groupby("code")["amount"].sum()
n_codes = pd_dedup.groupby("customer_id").size().rename("n_codes").reset_index()
sp = once.merge(n_codes, on="customer_id", validate="many_to_one")
p_split = (sp["amount"] / sp["n_codes"]).groupby(sp["code"]).sum()
pick = promo.groupby("customer_id", as_index=False).agg(code=("code", "min"))
pk = orders.merge(pick, on="customer_id", validate="many_to_one")
p_pick = pk.groupby("code")["amount"].sum()
for k, s in [("once per code", p_once), ("split equally", p_split), ("pick one (MIN code)", p_pick)]:
    assert {c: float(v) for c, v in s.items()} == {c: float(v) for c, v in sql[k].items()}, k
print("pandas == SQL for all three policies (compared as code -> revenue)")

# tie-out checks
assert sum(sql["once per code"].values()) > with_code               # overlap by design
assert sum(sql["split equally"].values()) == with_code
assert sum(sql["pick one (MIN code)"].values()) == with_code
assert sum(sql["split equally"].values()) + (total_orders - with_code) == total_orders
print("tie-out: split and pick sum to", with_code, "(+", total_orders - with_code, "with no code =", total_orders,
      "); once-per-code sums to", sum(sql["once per code"].values()), "by design, so it must not be added up")
con.close()
