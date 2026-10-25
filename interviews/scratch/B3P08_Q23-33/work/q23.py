# Q23: Trips and Users style daily cancellation rate, both sides unbanned, split by who cancelled
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, banned TEXT, role TEXT);
CREATE TABLE trips(trip_id INTEGER PRIMARY KEY, client_id INTEGER, driver_id INTEGER, city TEXT,
                   status TEXT, request_date TEXT);
INSERT INTO users VALUES
 (1,'No','client'),(2,'No','client'),(3,'Yes','client'),(7,'No','client'),
 (4,'No','driver'),(5,'No','driver'),(6,'Yes','driver');
INSERT INTO trips VALUES
 (1, 1,4,'Pune','completed',          '2024-03-01'),
 (2, 2,5,'Pune','cancelled_by_driver','2024-03-01'),
 (3, 3,4,'Pune','cancelled_by_client','2024-03-01'),
 (4, 1,6,'Pune','cancelled_by_client','2024-03-01'),
 (5, 2,4,'Pune','completed',          '2024-03-01'),
 (6, 1,4,'Pune','completed',          '2024-03-02'),
 (7, 7,5,'Pune','cancelled_by_client','2024-03-02'),
 (8, 2,4,'Pune','cancelled_by_client','2024-03-02'),
 (9, 3,6,'Pune','cancelled_by_driver','2024-03-03'),
 (10,1,4,'Pune','completed',          '2024-03-04'),
 (11,2,5,'Pune','completed',          '2024-03-04'),
 (12,99,4,'Pune','cancelled_by_client','2024-03-04');
"""

SQL_MAIN = """
SELECT t.request_date,
       COUNT(*) AS requests,
       SUM(t.status <> 'completed') AS cancelled,
       ROUND(SUM(t.status <> 'completed') * 1.0 / COUNT(*), 2) AS cancel_rate,
       ROUND(SUM(t.status = 'cancelled_by_driver') * 1.0 / COUNT(*), 2) AS by_driver_rate,
       ROUND(SUM(t.status = 'cancelled_by_client') * 1.0 / COUNT(*), 2) AS by_client_rate
FROM trips t
JOIN users c ON c.user_id = t.client_id AND c.banned = 'No'
JOIN users d ON d.user_id = t.driver_id AND d.banned = 'No'
GROUP BY t.request_date
ORDER BY t.request_date
"""
# wrong: only the client is checked
SQL_WRONG = """
SELECT t.request_date,
       COUNT(*) AS requests,
       ROUND(SUM(t.status <> 'completed') * 1.0 / COUNT(*), 2) AS cancel_rate
FROM trips t
JOIN users c ON c.user_id = t.client_id AND c.banned = 'No'
GROUP BY t.request_date
ORDER BY t.request_date
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_res = pd.read_sql_query(SQL_MAIN, con)
sql_wrong = pd.read_sql_query(SQL_WRONG, con)
print("SQL, both client and driver unbanned:")
print(sql_res.to_string(index=False))
print("SQL, wrong (client filtered only):")
print(sql_wrong.to_string(index=False))

trips = pd.read_sql_query("SELECT * FROM trips", con)
users = pd.read_sql_query("SELECT * FROM users", con)

# pd:main
def daily_cancellation(trips, users):
    ok = users.loc[users["banned"] == "No", ["user_id"]]
    t = (trips.merge(ok.rename(columns={"user_id": "client_id"}), on="client_id")
              .merge(ok.rename(columns={"user_id": "driver_id"}), on="driver_id"))
    t = t.assign(cancelled=t["status"] != "completed",
                 by_driver=t["status"] == "cancelled_by_driver",
                 by_client=t["status"] == "cancelled_by_client")
    g = t.groupby("request_date")
    out = g.agg(requests=("trip_id", "size"), cancelled=("cancelled", "sum"),
                by_driver=("by_driver", "sum"), by_client=("by_client", "sum")).reset_index()
    out["cancel_rate"] = (out["cancelled"] / out["requests"]).round(2)
    out["by_driver_rate"] = (out["by_driver"] / out["requests"]).round(2)
    out["by_client_rate"] = (out["by_client"] / out["requests"]).round(2)
    return out[["request_date", "requests", "cancelled", "cancel_rate",
                "by_driver_rate", "by_client_rate"]]
# pd:end

pd_res = daily_cancellation(trips, users)
# compare after sorting by request_date (SQL result is already in that order)
pd.testing.assert_frame_equal(pd_res.sort_values("request_date").reset_index(drop=True),
                              sql_res, check_dtype=False)
print("pandas:")
print(pd_res.to_string(index=False))
print("days in trips:", trips["request_date"].nunique(), "; days in result:", len(pd_res))
print("asserts passed")
