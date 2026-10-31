# Q9: pandas-first risk table: 30-day amount per customer, share of city total, rank within city. Then the SQL.
import sqlite3
import pandas as pd

customers = pd.DataFrame({"customer_id": [1, 2, 3, 4, 5, 6],
                          "city": ["Pune", "Pune", "Pune", "Delhi", "Delhi", "Delhi"]})
txns = pd.DataFrame({
    "txn_id": range(1, 12),
    "customer_id": [1, 1, 2, 3, 4, 4, 5, 2, 1, 99, 4],
    "txn_date": ["2025-06-05", "2025-06-30", "2025-06-10", "2025-06-12", "2025-06-01", "2025-06-20",
                 "2025-06-15", "2025-05-31", "2025-07-01", "2025-06-18", "2025-06-02"],
    "amount": [100, 50, 150, 100, 60, 40, 50, 999, 777, 300, 0]})
# customer 6 has no transactions; customer 99 (txn 10) is not in customers; txns 8 and 9 fall outside the window

con = sqlite3.connect(":memory:")
customers.to_sql("customers", con, index=False)
txns.to_sql("txns", con, index=False)

# pandas first. Window = 2025-06-01 .. 2025-06-30 inclusive (30 days ending on the as-of date)
asof = pd.Timestamp("2025-06-30"); start = asof - pd.Timedelta(days=29)
t = txns.assign(txn_date=pd.to_datetime(txns["txn_date"]))
w = t[(t["txn_date"] >= start) & (t["txn_date"] <= asof)]
amt = w.groupby("customer_id")["amount"].sum()
risk = customers.assign(amount_30d=customers["customer_id"].map(amt).fillna(0).astype("int64"))
city_tot = risk.groupby("city")["amount_30d"].transform("sum")
risk["city_share"] = (risk["amount_30d"] / city_tot.where(city_tot != 0)).round(4)
risk["city_rank"] = risk.groupby("city")["amount_30d"].rank(method="min", ascending=False).astype("int64")
p = risk.sort_values(["city", "city_rank", "customer_id"]).reset_index(drop=True)
orphan_p = w[~w["customer_id"].isin(customers["customer_id"])].groupby("customer_id", as_index=False).agg(
    txns=("txn_id", "size"), amount_30d=("amount", "sum"))
print("window:", start.date(), "to", asof.date(), "(", (asof - start).days + 1, "days )")
print("pandas risk table:"); print(p.to_string(index=False)); print()
print("pandas orphan transactions (customer not in customers), reported separately:"); print(orphan_p.to_string(index=False)); print()

sql = """
WITH a AS (
  SELECT customer_id, SUM(amount) AS amt FROM txns
  WHERE txn_date BETWEEN date('2025-06-30', '-29 days') AND '2025-06-30' GROUP BY customer_id
), r AS (
  SELECT c.customer_id, c.city, COALESCE(a.amt, 0) AS amount_30d
  FROM customers c LEFT JOIN a ON a.customer_id = c.customer_id
)
SELECT customer_id, city, amount_30d,
       ROUND(1.0 * amount_30d / NULLIF(SUM(amount_30d) OVER (PARTITION BY city), 0), 4) AS city_share,
       RANK() OVER (PARTITION BY city ORDER BY amount_30d DESC) AS city_rank
FROM r ORDER BY city, city_rank, customer_id
"""
orphan_sql = """
SELECT t.customer_id, COUNT(*) AS txns, SUM(t.amount) AS amount_30d FROM txns t
WHERE t.txn_date BETWEEN date('2025-06-30', '-29 days') AND '2025-06-30'
  AND NOT EXISTS (SELECT 1 FROM customers c WHERE c.customer_id = t.customer_id)
GROUP BY t.customer_id
"""
off = pd.read_sql(sql.replace("'-29 days'", "'-30 days'"), con)
print("off-by-one check, window start minus 30 days (31 days): customer 2 amount =",
      int(off.loc[off.customer_id == 2, "amount_30d"].iloc[0]), "instead of 150"); print()
s = pd.read_sql(sql, con); so = pd.read_sql(orphan_sql, con)
print("SQL risk table:"); print(s.to_string(index=False)); print()
pd.testing.assert_frame_equal(s, p[s.columns], check_dtype=False)
pd.testing.assert_frame_equal(so, orphan_p, check_dtype=False)
print("asserts passed (order: city, city_rank, customer_id)")
