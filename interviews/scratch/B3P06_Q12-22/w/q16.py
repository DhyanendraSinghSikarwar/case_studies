# Q16: UTC vs IST day boundaries; localtime modifier depends on host TZ; pandas tz_convert
import os
import sqlite3
import time
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts_utc TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-03-05 08:00:00',100),
 (2,'2024-03-05 18:29:59',200),
 (3,'2024-03-05 18:30:00',300),
 (4,'2024-03-05 20:00:00',400),
 (5,'2024-03-06 10:00:00',500),
 (6,'2024-03-31 19:00:00',600);
"""
SQL_UTC = """
SELECT date(order_ts_utc) AS day, COUNT(*) AS orders
FROM orders GROUP BY day ORDER BY day
"""
SQL_IST = """
SELECT date(datetime(order_ts_utc, '+5 hours', '+30 minutes')) AS day, COUNT(*) AS orders
FROM orders GROUP BY day ORDER BY day
"""
SQL_MOVED = """
SELECT order_id, order_ts_utc,
       datetime(order_ts_utc, '+5 hours', '+30 minutes') AS ist_ts,
       date(order_ts_utc) AS utc_day,
       date(datetime(order_ts_utc, '+5 hours', '+30 minutes')) AS ist_day
FROM orders
WHERE date(order_ts_utc) <> date(datetime(order_ts_utc, '+5 hours', '+30 minutes'))
ORDER BY order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
utc_sql = pd.read_sql_query(SQL_UTC, con)
ist_sql = pd.read_sql_query(SQL_IST, con)
print("UTC daily counts:"); print(utc_sql.to_string(index=False))
print("IST daily counts:"); print(ist_sql.to_string(index=False))
print("orders that change day:"); print(pd.read_sql_query(SQL_MOVED, con).to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
ts = pd.to_datetime(orders["order_ts_utc"], utc=True)
ist = ts.dt.tz_convert("Asia/Kolkata")
utc_pd = ts.dt.date.astype(str).value_counts().sort_index().rename_axis("day").reset_index(name="orders")
ist_pd = ist.dt.date.astype(str).value_counts().sort_index().rename_axis("day").reset_index(name="orders")
# pd:end
# compared in ascending day order
pd.testing.assert_frame_equal(utc_pd, utc_sql, check_dtype=False)
pd.testing.assert_frame_equal(ist_pd, ist_sql, check_dtype=False)
print("pandas equals SQL for UTC and IST")
print("pandas IST timestamps:", [str(x) for x in ist])

# the 'localtime' modifier depends on the process time zone, not on a stated business zone
probe = "SELECT datetime('2024-03-05 20:00:00', 'localtime')"
print("host TZ env:", os.environ.get("TZ"), "| tzname:", time.tzname)
print("localtime on this host:", con.execute(probe).fetchone()[0])
for tz in ("Asia/Kolkata", "America/New_York"):
    os.environ["TZ"] = tz
    time.tzset()
    print("with TZ =", tz, "->", con.execute(probe).fetchone()[0])
print("asserts passed")
