# Q16: "monthly active buyer rate for last month" with assumptions as parameters (as-of month 2024-03)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2023-11-01','IN',0),(2,'2023-11-05','IN',0),(3,'2023-12-01','US',0),(4,'2023-12-10','UK',0),
 (5,'2024-01-15','IN',0),(6,'2024-02-10','US',0),(7,'2024-03-10','IN',0),(8,'2024-03-20','IN',0),
 (9,'2024-04-05','IN',0),(10,'2023-10-01','IN',1);
INSERT INTO orders VALUES
 (1,1,'2024-03-05 10:00:00',100,'completed'),
 (2,2,'2024-03-31 20:00:00',80,'completed'),
 (3,3,'2024-03-12 09:00:00',60,'cancelled'),
 (4,5,'2024-01-10 09:00:00',90,'completed'),
 (5,7,'2024-03-22 09:00:00',70,'completed'),
 (6,8,'2024-03-25 09:00:00',50,'cancelled'),
 (7,10,'2024-03-08 09:00:00',500,'completed');
"""

# Assumptions are parameters:
#   :m_start / :m_end   local month [start, end) as text; local time = UTC + :tz_min minutes
#   :any_status         0 = buyer needs a completed order, 1 = any order counts
#   :incl_test          0 = drop is_test users (assumption A3)
#   :denom_mode         'registered' = users with signup_date < :signup_before
#                       'orderers'   = users with any order in the month
SQL_MAIN = """
-- A1 buyer: :any_status = 0 means a completed order is needed, 1 means any order counts
-- A2 denominator: :denom_mode = 'registered' means users with signup_date < :signup_before
-- A3 test users: dropped unless :incl_test = 1
-- A4 month: local time = UTC + :tz_min minutes, window [:m_start, :m_end)
-- A5 user level: DISTINCT users, numerator counted only among denominator users
WITH base AS (
  SELECT user_id, signup_date FROM users
  WHERE :incl_test = 1 OR is_test = 0
), o AS (
  SELECT user_id, status
  FROM orders
  WHERE datetime(order_ts, '+' || :tz_min || ' minutes') >= :m_start
    AND datetime(order_ts, '+' || :tz_min || ' minutes') <  :m_end
), buyers AS (
  SELECT DISTINCT user_id FROM o WHERE :any_status = 1 OR status = 'completed'
), denom AS (
  SELECT user_id FROM base WHERE :denom_mode = 'registered' AND signup_date < :signup_before
  UNION
  SELECT user_id FROM base WHERE :denom_mode = 'orderers' AND user_id IN (SELECT user_id FROM o)
)
SELECT COUNT(*) AS denominator,
       SUM(CASE WHEN d.user_id IN (SELECT user_id FROM buyers) THEN 1 ELSE 0 END) AS buyers,
       ROUND(100.0 * SUM(CASE WHEN d.user_id IN (SELECT user_id FROM buyers) THEN 1 ELSE 0 END)
             / NULLIF(COUNT(*), 0), 1) AS rate_pct
FROM denom d
"""

BASE = dict(tz_min=0, any_status=0, incl_test=0, denom_mode="registered",
            m_start="2024-03-01 00:00:00", m_end="2024-04-01 00:00:00", signup_before="2024-04-01")
SCENARIOS = [
    ("base: completed orders, registered by 03-31, no test, UTC", {}),
    ("flip 1: any order status counts", {"any_status": 1}),
    ("flip 2: denominator = registered at the start of March", {"signup_before": "2024-03-01"}),
    ("flip 3: denominator = users who placed any order in March", {"denom_mode": "orderers"}),
    ("flip 4: month in IST (UTC + 330 minutes)", {"tz_min": 330}),
    ("flip 5: test users included", {"incl_test": 1}),
]

# pd:main
def pd_rate(users, orders, tz_min, any_status, incl_test, denom_mode, m_start, m_end, signup_before):
    base = users if incl_test == 1 else users[users["is_test"] == 0]
    o = orders.copy()
    o["local"] = pd.to_datetime(o["order_ts"]) + pd.Timedelta(minutes=tz_min)
    o = o[(o["local"] >= pd.Timestamp(m_start)) & (o["local"] < pd.Timestamp(m_end))]
    buyers = set(o[(o["status"] == "completed") | (any_status == 1)]["user_id"])
    if denom_mode == "registered":
        denom = set(base[base["signup_date"] < signup_before]["user_id"])
    else:
        denom = set(base["user_id"]) & set(o["user_id"])
    n_buy = len(denom & buyers)
    rate = round(100.0 * n_buy / len(denom), 1) if denom else float("nan")
    return len(denom), n_buy, rate
# pd:end

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
users = pd.read_sql_query("SELECT * FROM users", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
rows = []
for name, change in SCENARIOS:
    p = {**BASE, **change}
    den, buy, rate = con.execute(SQL_MAIN, p).fetchone()
    pden, pbuy, prate = pd_rate(users, orders, **p)
    assert (den, buy, rate) == (pden, pbuy, prate), (name, (den, buy, rate), (pden, pbuy, prate))
    rows.append({"scenario": name, "denominator": den, "buyers": buy, "rate_pct": rate})
print(pd.DataFrame(rows).to_string(index=False))

# who is behind the base number and the IST flip
print("base buyers:", sorted(r[0] for r in con.execute(
    "SELECT DISTINCT user_id FROM orders o WHERE status='completed' AND order_ts >= '2024-03-01' AND order_ts < '2024-04-01' "
    "AND user_id IN (SELECT user_id FROM users WHERE is_test = 0)")))
print("IST buyers:", sorted(r[0] for r in con.execute(
    "SELECT DISTINCT user_id FROM orders o WHERE status='completed' "
    "AND datetime(order_ts, '+330 minutes') >= '2024-03-01 00:00:00' AND datetime(order_ts, '+330 minutes') < '2024-04-01 00:00:00' "
    "AND user_id IN (SELECT user_id FROM users WHERE is_test = 0)")))
print("asserts passed")
