# Q36: month-to-date versus same day-of-month window, IST day versus UTC day, as-of 2024-03-18
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts_utc TEXT, amount REAL, status TEXT);
INSERT INTO orders VALUES
 (1,1,'2024-02-03 10:00:00',400,'completed'),
 (2,2,'2024-02-10 20:00:00',500,'completed'),
 (3,3,'2024-02-17 19:30:00',350,'completed'),
 (4,1,'2024-02-18 09:00:00',300,'completed'),
 (5,4,'2024-02-25 12:00:00',600,'completed'),
 (6,2,'2024-02-28 08:00:00',550,'completed'),
 (7,5,'2024-02-29 22:00:00',400,'completed'),
 (8,3,'2024-02-12 11:00:00',90,'cancelled'),
 (9,6,'2024-03-02 10:00:00',500,'completed'),
 (10,7,'2024-03-05 12:00:00',450,'completed'),
 (11,8,'2024-03-10 18:30:00',600,'completed'),
 (12,2,'2024-03-14 09:00:00',350,'completed'),
 (13,9,'2024-03-17 08:00:00',400,'completed'),
 (14,4,'2024-03-17 19:00:00',300,'completed'),
 (15,6,'2024-03-18 03:00:00',200,'completed'),
 (16,10,'2024-02-05 09:00:00',600,'completed'),
 (17,11,'2024-02-08 09:00:00',450,'completed'),
 (18,12,'2024-02-14 09:00:00',500,'completed'),
 (19,13,'2024-02-16 09:00:00',300,'completed');
"""
SQL_MAIN = """
WITH o AS (
  SELECT order_id, amount,
         date(order_ts_utc, '+330 minutes') AS ist_day
  FROM orders
  WHERE status = 'completed'
), p AS (
  SELECT '2024-03-18'                                      AS as_of,
         date('2024-03-18', 'start of month')              AS cur_start,
         date('2024-03-18', 'start of month', '-1 month')  AS prev_start,
         CAST(strftime('%d', '2024-03-18') AS INTEGER) - 1 AS full_days   -- 17 complete days
)
SELECT
  (SELECT SUM(amount) FROM o WHERE ist_day >= p.cur_start AND ist_day < p.as_of) AS mtd_cur,
  (SELECT SUM(amount) FROM o WHERE ist_day >= p.prev_start
                              AND ist_day < date(p.prev_start, '+' || p.full_days || ' days')) AS mtd_prev,
  (SELECT SUM(amount) FROM o WHERE ist_day >= p.prev_start AND ist_day < p.cur_start) AS feb_full_ist
FROM p
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
r = con.execute(SQL_MAIN).fetchone()
mtd_cur, mtd_prev, feb_full = r
naive = con.execute("""SELECT SUM(amount) FROM orders WHERE status='completed'
                       AND order_ts_utc >= '2024-03-01' AND order_ts_utc < '2024-04-01'""").fetchone()[0]
feb_utc = con.execute("""SELECT SUM(amount) FROM orders WHERE status='completed'
                         AND order_ts_utc >= '2024-02-01' AND order_ts_utc < '2024-03-01'""").fetchone()[0]
print("naive (UTC) March so far:", naive, "| February full month:", feb_utc, "| change: %.1f%%" % (100 * (naive / feb_utc - 1)))
u = con.execute("""SELECT SUM(CASE WHEN date(order_ts_utc) BETWEEN '2024-03-01' AND '2024-03-17' THEN amount END),
                          SUM(CASE WHEN date(order_ts_utc) BETWEEN '2024-02-01' AND '2024-02-17' THEN amount END)
                   FROM orders WHERE status='completed'""").fetchone()
print("MTD on UTC days 1-17: March", u[0], "| February 1-17:", u[1], "| change: %.1f%%" % (100 * (u[0] / u[1] - 1)))
print("MTD IST complete days 1-17: March", mtd_cur, "| February 1-17:", mtd_prev, "| change: %.1f%%" % (100 * (mtd_cur / mtd_prev - 1)))

DAILY = """
SELECT date(order_ts_utc) AS utc_day, date(order_ts_utc, '+330 minutes') AS ist_day, order_id, order_ts_utc, amount
FROM orders WHERE status='completed' AND date(order_ts_utc) <> date(order_ts_utc, '+330 minutes')
ORDER BY order_ts_utc
"""
print("orders whose IST day differs from the UTC day:")
print(pd.read_sql_query(DAILY, con).to_string(index=False))
SQL_DAILY = """
WITH RECURSIVE sp(d) AS (SELECT '2024-03-14' UNION ALL SELECT date(d, '+1 day') FROM sp WHERE d < '2024-03-18')
SELECT sp.d,
       COALESCE((SELECT SUM(amount) FROM orders WHERE status='completed' AND date(order_ts_utc) = sp.d), 0) AS utc_revenue,
       COALESCE((SELECT SUM(amount) FROM orders WHERE status='completed'
                   AND date(order_ts_utc, '+330 minutes') = sp.d), 0) AS ist_revenue
FROM sp ORDER BY sp.d
"""
sql_daily = pd.read_sql_query(SQL_DAILY, con)
print(sql_daily.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
o = orders[orders["status"].eq("completed")].copy()
ts = pd.to_datetime(o["order_ts_utc"])
o["ist_day"] = (ts + pd.Timedelta(minutes=330)).dt.normalize()
o["utc_day"] = ts.dt.normalize()
cur = o[(o["ist_day"] >= "2024-03-01") & (o["ist_day"] < "2024-03-18")]["amount"].sum()
prev = o[(o["ist_day"] >= "2024-02-01") & (o["ist_day"] < "2024-02-18")]["amount"].sum()
utc_daily = o.groupby("utc_day")["amount"].sum()
ist_daily = o.groupby("ist_day")["amount"].sum()
days = pd.date_range("2024-03-14", "2024-03-18")
pd_daily = pd.DataFrame({"d": days.strftime("%Y-%m-%d"),
                         "utc_revenue": utc_daily.reindex(days, fill_value=0).to_numpy(),
                         "ist_revenue": ist_daily.reindex(days, fill_value=0).to_numpy()})
# pd:end
assert (cur, prev) == (mtd_cur, mtd_prev)
pd.testing.assert_frame_equal(sql_daily.reset_index(drop=True), pd_daily, check_dtype=False)  # sorted by day
print(pd_daily.to_string(index=False))
# same IST day through a real time zone
tz = pd.to_datetime(o["order_ts_utc"]).dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata").dt.tz_localize(None).dt.normalize()
assert (tz == o["ist_day"]).all()
print("tz_convert('Asia/Kolkata') matches +330 minutes; asserts passed")
