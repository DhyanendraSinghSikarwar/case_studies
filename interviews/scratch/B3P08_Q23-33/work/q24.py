# Q24: marketplace supply and demand metrics per city: fill rate, cancellation share, rides per driver, take rate
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE ride_requests(request_id INTEGER PRIMARY KEY, rider_id INTEGER, driver_id INTEGER, city TEXT,
                           request_ts TEXT, status TEXT, fare REAL, commission REAL);
INSERT INTO ride_requests VALUES
 (1, 1, 10,  'Mumbai','2024-03-01 08:00:00','completed',          200, 40),
 (2, 2, 10,  'Mumbai','2024-03-01 09:00:00','completed',          100, 20),
 (3, 3, 11,  'Mumbai','2024-03-01 09:30:00','cancelled_by_driver',NULL,NULL),
 (4, 4, NULL,'Mumbai','2024-03-01 10:00:00','cancelled_by_rider', NULL,NULL),
 (5, 5, NULL,'Mumbai','2024-03-01 10:30:00','no_driver_found',    NULL,NULL),
 (6, 6, 11,  'Mumbai','2024-03-01 11:00:00','completed',          300, 48),
 (7, 7, 12,  'Mumbai','2024-03-01 12:00:00','cancelled_by_rider', NULL,NULL),
 (8, 8, NULL,'Pune',  '2024-03-01 08:00:00','no_driver_found',    NULL,NULL),
 (9, 9, NULL,'Pune',  '2024-03-01 09:00:00','cancelled_by_rider', NULL,NULL),
 (10,10,20,  'Pune',  '2024-03-01 10:00:00','completed',          150, 30),
 (11,11,20,  'Pune',  '2024-03-01 11:00:00','completed',          250, 50),
 (12,12,NULL,'Delhi', '2024-03-01 08:00:00','no_driver_found',    NULL,NULL),
 (13,13,NULL,'Delhi', '2024-03-01 09:00:00','no_driver_found',    NULL,NULL);
"""

SQL_MAIN = """
SELECT city,
       COUNT(*) AS requests,
       SUM(status = 'completed') AS completed,
       ROUND(SUM(status = 'completed') * 1.0 / COUNT(*), 2) AS fill_rate,
       SUM(status IN ('cancelled_by_rider', 'cancelled_by_driver')) AS cancelled,
       ROUND(SUM(status = 'cancelled_by_rider') * 1.0 /
             NULLIF(SUM(status IN ('cancelled_by_rider', 'cancelled_by_driver')), 0), 2) AS rider_share,
       ROUND(SUM(status = 'cancelled_by_driver') * 1.0 /
             NULLIF(SUM(status IN ('cancelled_by_rider', 'cancelled_by_driver')), 0), 2) AS driver_share,
       COUNT(DISTINCT driver_id) AS active_drivers,
       ROUND(SUM(status = 'completed') * 1.0 / NULLIF(COUNT(DISTINCT driver_id), 0), 2) AS rides_per_driver,
       ROUND(SUM(CASE WHEN status = 'completed' THEN commission END) * 1.0 /
             NULLIF(SUM(CASE WHEN status = 'completed' THEN fare END), 0), 2) AS take_rate
FROM ride_requests
GROUP BY city
ORDER BY city
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_res = pd.read_sql_query(SQL_MAIN, con)
print("SQL:")
print(sql_res.to_string(index=False))

rr = pd.read_sql_query("SELECT * FROM ride_requests", con)

# pd:main
def city_metrics(rr):
    done = rr["status"] == "completed"
    canc = rr["status"].isin(["cancelled_by_rider", "cancelled_by_driver"])
    t = rr.assign(completed=done, cancelled=canc,
                  by_rider=rr["status"] == "cancelled_by_rider",
                  by_driver=rr["status"] == "cancelled_by_driver",
                  fare_done=rr["fare"].where(done), comm_done=rr["commission"].where(done))
    g = t.groupby("city")
    out = g.agg(requests=("request_id", "size"), completed=("completed", "sum"),
                cancelled=("cancelled", "sum"), by_rider=("by_rider", "sum"),
                by_driver=("by_driver", "sum"), active_drivers=("driver_id", "nunique"),
                fare=("fare_done", "sum"), comm=("comm_done", "sum")).reset_index()
    nz = lambda s: s.where(s != 0)          # zero denominator -> NaN (SQL NULLIF)
    out["fill_rate"] = (out["completed"] / out["requests"]).round(2)
    out["rider_share"] = (out["by_rider"] / nz(out["cancelled"])).round(2)
    out["driver_share"] = (out["by_driver"] / nz(out["cancelled"])).round(2)
    out["rides_per_driver"] = (out["completed"] / nz(out["active_drivers"])).round(2)
    out["take_rate"] = (out["comm"] / nz(out["fare"])).round(2)
    return out[["city", "requests", "completed", "fill_rate", "cancelled", "rider_share",
                "driver_share", "active_drivers", "rides_per_driver", "take_rate"]]
# pd:end

pd_res = city_metrics(rr)
# compare after sorting by city; NaN in pandas equals NULL in SQL for this comparison
pd.testing.assert_frame_equal(pd_res.sort_values("city").reset_index(drop=True), sql_res, check_dtype=False)
print("pandas:")
print(pd_res.to_string(index=False))

# Mumbai alternatives for the rides-per-driver denominator
m = rr[rr["city"] == "Mumbai"]
print("Mumbai drivers with an assigned request:", m["driver_id"].nunique(),
      "; drivers with a completed ride:", m.loc[m["status"] == "completed", "driver_id"].nunique(),
      "; rows with a NULL driver:", int(m["driver_id"].isna().sum()))
print("asserts passed")
