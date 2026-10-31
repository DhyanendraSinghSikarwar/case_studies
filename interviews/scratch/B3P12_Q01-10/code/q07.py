# Q7: currency conversion at the rate valid on the payment day (latest rate on or before paid_on).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE fx_rates(currency TEXT, valid_from TEXT, rate_to_inr REAL);
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, currency TEXT, paid_on TEXT, amount REAL);
INSERT INTO fx_rates VALUES
 ('USD','2025-01-01',83.0),('USD','2025-02-01',84.5),('USD','2025-03-01',85.25),
 ('EUR','2025-01-15',90.0),('EUR','2025-02-15',91.5),('EUR','2025-03-15',93.0);
INSERT INTO payments VALUES
 (1,'USD','2025-01-10',100),   -- inside the first USD range
 (2,'USD','2025-02-01',200),   -- exactly on a valid_from: the new rate applies
 (3,'USD','2025-02-28',50),    -- day before the next change: still 84.5
 (4,'USD','2025-04-10',10),    -- after the last row: last rate carries on
 (5,'EUR','2025-01-10',100),   -- before the first EUR rate: NULL
 (6,'EUR','2025-03-15',40),    -- exactly on the last valid_from
 (7,'GBP','2025-02-01',10);    -- currency with no rate rows at all: NULL
""")

corr = """
SELECT p.payment_id, p.currency, p.paid_on, p.amount,
       (SELECT r.rate_to_inr FROM fx_rates r
        WHERE r.currency = p.currency AND r.valid_from <= p.paid_on
        ORDER BY r.valid_from DESC LIMIT 1) AS rate,
       ROUND(p.amount * (SELECT r.rate_to_inr FROM fx_rates r
        WHERE r.currency = p.currency AND r.valid_from <= p.paid_on
        ORDER BY r.valid_from DESC LIMIT 1), 2) AS amount_inr
FROM payments p ORDER BY p.payment_id
"""
rng = """
WITH r AS (
  SELECT currency, valid_from, rate_to_inr,
         LEAD(valid_from) OVER (PARTITION BY currency ORDER BY valid_from) AS valid_to   -- exclusive end
  FROM fx_rates
)
SELECT p.payment_id, p.currency, p.paid_on, p.amount, r.rate_to_inr AS rate,
       ROUND(p.amount * r.rate_to_inr, 2) AS amount_inr
FROM payments p
LEFT JOIN r ON r.currency = p.currency AND p.paid_on >= r.valid_from
           AND (r.valid_to IS NULL OR p.paid_on < r.valid_to)
ORDER BY p.payment_id
"""
a = pd.read_sql(corr, con); b = pd.read_sql(rng, con)
print("SQL correlated subquery:"); print(a.to_string(index=False)); print()
pd.testing.assert_frame_equal(a, b, check_dtype=False)
print("range join with LEAD gives the same rows")

# pandas merge_asof: both sides sorted on the date key, matched within currency
pay = pd.read_sql("SELECT * FROM payments", con, parse_dates=["paid_on"])
fx = pd.read_sql("SELECT * FROM fx_rates", con, parse_dates=["valid_from"])
m = pd.merge_asof(pay.sort_values("paid_on"), fx.sort_values("valid_from"),
                  left_on="paid_on", right_on="valid_from", by="currency",
                  direction="backward", allow_exact_matches=True)
m["amount_inr"] = (m["amount"] * m["rate_to_inr"]).round(2)
p = (m.rename(columns={"rate_to_inr": "rate"}).sort_values("payment_id").reset_index(drop=True))
p["paid_on"] = p["paid_on"].dt.strftime("%Y-%m-%d")
p = p[["payment_id", "currency", "paid_on", "amount", "rate", "amount_inr"]]
print(); print("pandas merge_asof:"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("asserts passed (compared in payment_id order)")

# what goes wrong without allow_exact_matches
m2 = pd.merge_asof(pay.sort_values("paid_on"), fx.sort_values("valid_from"), left_on="paid_on",
                   right_on="valid_from", by="currency", allow_exact_matches=False).sort_values("payment_id")
print("with allow_exact_matches=False payment 2 gets rate", m2.loc[m2.payment_id == 2, "rate_to_inr"].iloc[0], "(should be 84.5)")
