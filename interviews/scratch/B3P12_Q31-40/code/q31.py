# Q31: coupon status on the order date (LEFT JOIN with the code match in ON), discounted amount for valid ones.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE coupons(code TEXT PRIMARY KEY, start_date TEXT, end_date TEXT, pct_off INTEGER);
CREATE TABLE orders(order_id INTEGER, order_date TEXT, coupon_code TEXT, amount INTEGER);
INSERT INTO coupons VALUES ('SAVE10', '2025-03-01', '2025-03-31', 10), ('FLASH', '2025-03-10', '2025-03-12', 25);
INSERT INTO orders VALUES
 (1, '2025-03-01', 'SAVE10', 100),
 (2, '2025-03-31', 'SAVE10', 200),
 (3, '2025-02-28', 'SAVE10', 150),
 (4, '2025-04-01', 'SAVE10', 120),
 (5, '2025-03-12', 'FLASH',   80),
 (6, '2025-03-05', 'BOGUS',   90),
 (7, '2025-03-05', NULL,      60);
""")

sql_answer = """
SELECT o.order_id, o.order_date, o.coupon_code,
       CASE WHEN o.coupon_code IS NULL THEN 'NO_COUPON'
            WHEN c.code IS NULL THEN 'UNKNOWN_CODE'
            WHEN o.order_date < c.start_date THEN 'NOT_STARTED'
            WHEN o.order_date > c.end_date THEN 'EXPIRED'
            ELSE 'VALID' END AS status,
       CASE WHEN o.order_date BETWEEN c.start_date AND c.end_date
            THEN ROUND(o.amount * (100 - c.pct_off) / 100.0, 2) END AS discounted
FROM orders o
LEFT JOIN coupons c ON c.code = o.coupon_code
ORDER BY o.order_id
"""
# the two wrong versions, to show what they lose
sql_where = """
SELECT COUNT(*) FROM orders o LEFT JOIN coupons c ON c.code = o.coupon_code
WHERE o.order_date BETWEEN c.start_date AND c.end_date
"""
sql_date_in_on = """
SELECT o.order_id, c.code IS NOT NULL AS matched
FROM orders o LEFT JOIN coupons c
  ON c.code = o.coupon_code AND o.order_date BETWEEN c.start_date AND c.end_date
ORDER BY o.order_id
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False))
print("\nwith the date test in WHERE, rows left:", con.execute(sql_where).fetchone()[0], "of 7")
print("date test in ON, code match flag (cannot tell EXPIRED from UNKNOWN_CODE):",
      pd.read_sql(sql_date_in_on, con).matched.tolist())

# --- pandas
orders = pd.read_sql("SELECT * FROM orders", con)
coupons = pd.read_sql("SELECT * FROM coupons", con)
m = orders.merge(coupons, how="left", left_on="coupon_code", right_on="code")
od, sd, ed = (pd.to_datetime(m[c]) for c in ("order_date", "start_date", "end_date"))
m["status"] = np.select(
    [m.coupon_code.isna(), m.code.isna(), od < sd, od > ed],
    ["NO_COUPON", "UNKNOWN_CODE", "NOT_STARTED", "EXPIRED"], default="VALID")
m["discounted"] = (m.amount * (100 - m.pct_off) / 100).where(m.status == "VALID").round(2)
want = m[["order_id", "order_date", "coupon_code", "status", "discounted"]]
# --- end pandas
print()
print(want.to_string(index=False))
pd.testing.assert_frame_equal(got.sort_values("order_id").reset_index(drop=True),
                              want.sort_values("order_id").reset_index(drop=True), check_dtype=False)
assert len(want) == len(orders) == 7
print("assert passed: SQL equals pandas after sorting by order_id; 7 rows in, 7 rows out")
