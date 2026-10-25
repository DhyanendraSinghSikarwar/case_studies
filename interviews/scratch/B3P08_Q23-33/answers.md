### Q23 ⭐⭐ 🟡 LeetCode 262 Trips and Users style cancellation by side: trips(trip_id, client_id, driver_id, city, status, request_date) with status in ('completed', 'cancelled_by_driver', 'cancelled_by_client') and users(user_id, banned, role). Return per request_date the cancellation rate (any cancellation over all requests, rounded to 2 decimals) counting only trips where both client and driver are unbanned, and show the rate split by who cancelled. Join users twice (once for the client, once for the driver), explain why filtering only the client is wrong, and handle days with zero qualifying trips (the row should not appear).
**Asked at:** LeetCode 262 Trips and Users (search snippets of doocs, tencent and velog mirrors; not opened; statement: daily cancellation rate, both client and driver unbanned) plus the marketplace framing (fill rate, cancellation by side) as an expert extension; public problem bank, not a candidate report; ride-hailing, food-delivery and marketplace analyst rounds
**Say this first (1 line):** Join `users` twice, once as client and once as driver, keep only trips where both are unbanned, then per `request_date` divide cancelled trips (any status other than completed) by all qualifying trips, using `* 1.0` so SQLite does not do integer division; a day with no qualifying trip has no group, so it simply does not appear.

**Schema and sample data:** twelve trips, seven users, `banned` stored as 'Yes' or 'No' (the LeetCode 262 convention; I state that as an assumption). Trip 3 has a banned client, trip 4 a banned driver, trip 9 is the only trip on 2024-03-03 and it involves two banned users, trip 12 has a client id (99) that is not in `users`. The `city` column is carried but not used.
```sql
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
```

**SQL answer:** `SQL_MAIN` in the Code block (two joins to `users`, the ban test inside each join so it is applied to the right side):
```sql
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
```
The wrong version (`SQL_WRONG` in the Code block) joins `users` once, for the client only. It is printed in the output so you can see the number move.

**pandas answer:** the same logic, shown once here and identical to the Code block. Two merges against the unbanned users, one renamed to `client_id` and one to `driver_id`:
```py
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
```

**Example:** walk through the sample data by hand.
- Day 2024-03-01 has five trips. Trip 3 (banned client 3) and trip 4 (banned driver 6) drop out, leaving trips 1, 2 and 5: one completed, one cancelled by the driver, one completed. 3 requests, 1 cancellation, rate 1/3 = 0.33, all of it driver-side (0.33 by driver, 0.00 by client).
- Day 2024-03-02 has three qualifying trips (6, 7, 8): two are cancelled by the client, so 2/3 = 0.67 and the split is 0.00 driver, 0.67 client.
- Day 2024-03-03 has one trip and both of its users are banned, so zero qualifying trips and no output row. Trip 12 on 2024-03-04 has a client id that is not in `users`; an inner join drops it, so that day has 2 qualifying trips and rate 0.00.
- Wrong version (client filter only): on 2024-03-01 the banned-driver trip 4 stays in, giving 4 requests and 2 cancellations, 0.50 instead of 0.33. Days where only a driver is banned are the ones that move.

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
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
```

**Output (my run):**
```text
SQL, both client and driver unbanned:
request_date  requests  cancelled  cancel_rate  by_driver_rate  by_client_rate
  2024-03-01         3          1         0.33            0.33            0.00
  2024-03-02         3          2         0.67            0.00            0.67
  2024-03-04         2          0         0.00            0.00            0.00
SQL, wrong (client filtered only):
request_date  requests  cancel_rate
  2024-03-01         4         0.50
  2024-03-02         3         0.67
  2024-03-04         2         0.00
pandas:
request_date  requests  cancelled  cancel_rate  by_driver_rate  by_client_rate
  2024-03-01         3          1         0.33            0.33            0.00
  2024-03-02         3          2         0.67            0.00            0.67
  2024-03-04         2          0         0.00            0.00            0.00
days in trips: 4 ; days in result: 3
asserts passed
```

**Edge cases:**
- A day with zero qualifying trips has no group, so no row and no division by zero. If the report must show every day with 0 or NULL, start from a date list and LEFT JOIN, and say which you want.
- A user id missing from `users` (trip 12): with inner joins the trip is dropped; with a LEFT JOIN plus `banned = 'No'` in the WHERE it is also dropped; with `banned <> 'Yes'` it would be kept. Pick and state the rule.
- `banned` NULL: `banned = 'No'` is not true for NULL, so the user is treated as not provably unbanned and the trip is dropped; the opposite rule is `COALESCE(banned,'No') = 'No'`.
- Rounding: values here are 1/3 and 2/3, no exact half; for a value like 0.125 SQLite ROUND and pandas round disagree (see Q31).

**Then explain:**
- Both parties must be unbanned: banning is a property of a user, a trip has two users, and the question's rule needs both. Filtering only the client leaves trips with a banned driver in the numerator and denominator.
- The denominator is all qualifying requests (completed plus both cancel types), not only completed trips.
- `SUM(status <> 'completed')` works in SQLite because a comparison is 0 or 1; in Postgres you would write `COUNT(*) FILTER (WHERE ...)` or `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`, in BigQuery `COUNTIF(...)` (not executed here). The CASE form is portable.
- Put the ban condition in the join (`ON ... AND c.banned = 'No'`) for an inner join; it is equivalent to a WHERE there. With a LEFT JOIN it must stay in the WHERE or the row survives with NULLs.
- Round the final ratio only; do not round counts first.

**Follow-ups:**
- Also show the days with zero qualifying trips? Generate a date spine (recursive CTE, see Q33) and LEFT JOIN the daily result, returning NULL or 0 as agreed.
- Cancellation rate by city as well? Add `t.city` to the GROUP BY; the double join is unchanged.
- Split by who cancelled but over cancellations only? Use `NULLIF(SUM(status <> 'completed'), 0)` as the denominator; Q24 does this for a marketplace.

**Common mistakes:**
- Filtering only the client side (shown in the output).
- Joining `users` once and checking `client_id` and `driver_id` against the same alias.
- Integer division: `SUM(...) / COUNT(*)` gives 0 in SQLite when the ratio is below 1; multiply by 1.0 first.
- Putting the ban filter in WHERE after a LEFT JOIN and then wondering why unmatched trips vanish (or the reverse).
- Counting only 'cancelled_by_client' as cancellations.


### Q24 ⭐⭐ 🟡 Supply and demand marketplace metrics: ride_requests(request_id, rider_id, driver_id, city, request_ts, status, fare, commission) with status in ('completed', 'cancelled_by_rider', 'cancelled_by_driver', 'no_driver_found') and driver_id NULL when no driver was assigned. Return per city the fill rate (requests that ended completed over all requests), the cancellation share by side, completed rides per active driver (drivers with at least one assigned request), and the take rate (commission over fare on completed rides). Say why 'no_driver_found' belongs in the fill-rate denominator and not in the cancellation numerator, and which denominator rides per driver should use.
**Asked at:** LeetCode 262 Trips and Users (search snippets of doocs, tencent and velog mirrors; not opened; statement: daily cancellation rate, both client and driver unbanned) plus the marketplace framing (fill rate, cancellation by side) as an expert extension; public problem bank, not a candidate report; ride-hailing, food-delivery and marketplace analyst rounds
**Say this first (1 line):** Per city: fill rate is completed over all requests (including no_driver_found), cancellation share is rider-cancelled and driver-cancelled over cancellations, rides per active driver is completed rides over distinct drivers with an assigned request, and take rate is summed commission over summed fare on completed rides only; every ratio gets `NULLIF` so an empty denominator is NULL, not an error.

**Schema and sample data:** thirteen requests in three cities. Mumbai has all four statuses and one rider cancellation after a driver was assigned (driver 12). Pune has two completed rides by the same driver. Delhi has only `no_driver_found`, so cancellations, active drivers and fare are all zero there. `fare` and `commission` are NULL on rows that did not complete. All fares and commissions are made-up toy values.
```sql
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
```

**SQL answer:** `SQL_MAIN` in the Code block:
```sql
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
```

**pandas answer:** the same logic as one function (`nz` turns a zero denominator into NaN, the counterpart of `NULLIF`):
```py
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
```

**Example:** walk through the sample data by hand.
- Mumbai: 7 requests, 3 completed (requests 1, 2, 6) so fill rate 3/7 = 0.43. Cancellations are requests 3 (driver), 4 (rider) and 7 (rider): 3 in all, rider share 2/3 = 0.67, driver share 1/3 = 0.33. The request with `no_driver_found` is in the fill-rate denominator but not among the cancellations.
- Active drivers in Mumbai are the distinct non-NULL driver ids: 10, 11, 12, so 3. Rides per active driver is 3 completed / 3 = 1.0. `COUNT(DISTINCT driver_id)` ignores the two NULL rows by itself.
- Take rate: commissions 40 + 20 + 48 = 108 over fares 200 + 100 + 300 = 600, 0.18.
- Pune: fill 2/4 = 0.50, one cancellation (rider), so shares 1.00 and 0.00, one active driver (20), 2.0 rides per driver, take rate 80/400 = 0.20.
- Delhi: fill 0.00, no cancellations, no drivers, no fare: the four ratios are NULL (NaN in pandas), not 0 and not an error.

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
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
```

**Output (my run):**
```text
SQL:
  city  requests  completed  fill_rate  cancelled  rider_share  driver_share  active_drivers  rides_per_driver  take_rate
 Delhi         2          0       0.00          0          NaN           NaN               0               NaN        NaN
Mumbai         7          3       0.43          3         0.67          0.33               3               1.0       0.18
  Pune         4          2       0.50          1         1.00          0.00               1               2.0       0.20
pandas:
  city  requests  completed  fill_rate  cancelled  rider_share  driver_share  active_drivers  rides_per_driver  take_rate
 Delhi         2          0       0.00          0          NaN           NaN               0               NaN        NaN
Mumbai         7          3       0.43          3         0.67          0.33               3               1.0       0.18
  Pune         4          2       0.50          1         1.00          0.00               1               2.0       0.20
Mumbai drivers with an assigned request: 3 ; drivers with a completed ride: 2 ; rows with a NULL driver: 2
asserts passed
```

**Edge cases:**
- Zero denominators give NULL here. In SQLite `x / 0` also returns NULL rather than raising (Q31 runs it), but PostgreSQL and others raise a division error (not executed here), so `NULLIF` is the portable habit.
- Driver NULL on a cancelled_by_rider row (rider left before assignment, request 4) versus a driver assigned (request 7): the first does not count toward active drivers, the second does. That is a business rule to confirm.
- A driver with one completed ride and one driver-cancelled request is one active driver; counting rows instead of distinct ids would double count.
- Drivers who were online but never got a request are not in this table at all, so they cannot be in the denominator; that needs a supply table.

**Then explain:**
- no_driver_found belongs in the fill-rate denominator because fill rate measures how much of the demand you served; a request nobody could serve is the clearest failure of supply. It is not a cancellation: nobody cancelled, the platform failed to match.
- Cancellation share by side is a share of cancellations here (rider plus driver = 1). If the interviewer means each side's cancellations over all requests, change the denominator to `COUNT(*)`; say which you used.
- Rides per active driver uses distinct drivers with at least one assigned request (3 in Mumbai). The alternatives are drivers with a completed ride (2 in Mumbai, which would give 1.5) or drivers logged in from a supply table. All are defensible; the choice changes the number, so name it.
- Take rate is a ratio of sums over completed rides, not an average of per-ride ratios; the average of ratios weights a 100 fare ride like a 1000 fare ride.
- Metric design (is fill rate the right goal?) belongs to Book 6; this answer stays on the SQL.

**Follow-ups:**
- Per day or per hour instead of per city? Add the truncated `request_ts` to the GROUP BY; with few rows per bucket the ratios get noisy.
- Why not average per-ride commission rates? Because that is a different, unweighted number (see above).
- How would you split cancellations before and after driver assignment? Use `driver_id IS NULL` on cancelled_by_rider rows as the proxy and say it is a proxy.

**Common mistakes:**
- Putting `no_driver_found` in the cancellation numerator.
- Dividing rides by all drivers in the company instead of drivers active in that city and period.
- Summing fares over all rows (including cancelled) for the take-rate denominator.
- Averaging per-ride take rates.
- Dividing by zero instead of `NULLIF` for a city with no completed rides.


### Q25 ⭐⭐ 🟡 Search metrics: searches(search_id, user_id, search_ts, query, result_count) and clicks(click_id, search_id, click_ts, position). Return per day the search count, the click-through rate (searches with at least one click over searches, not clicks over searches), the zero-result rate, and the distribution of clicked positions (1, 2, 3, 4 to 10, 11 and above) as a percentage of clicks. Show why joining searches to clicks first and counting rows inflates CTR (fan-out) and use EXISTS or a distinct count instead, and what you do with searches that have zero results and therefore cannot get a click.
**Asked at:** search-analytics guides (Elastic ES|QL click-tracking post, oneuptime ClickHouse search analytics, Algolia and SearchStax metric definitions; search snippets only, not opened: CTR = searches with at least one click over searches, zero-result rate, average click position, MRR); vendor guides, not candidate reports; search and marketplace analyst rounds
**Say this first (1 line):** Decide the grain first: CTR is searches that got at least one click over searches, so mark each search with `EXISTS` on `clicks` (one row per search, no fan-out) and average that flag per day; clicks per search is a different number and joining first inflates it.

**Schema and sample data:** eight searches over three days and six clicks. Search 1 gets two clicks (positions 1 and 3), search 2 has zero results so it cannot be clicked, search 7 has `result_count` NULL (a logging gap, not the same as zero), search 8 is the only search on 2024-03-03 and has no click at all.
```sql
CREATE TABLE searches(search_id INTEGER PRIMARY KEY, user_id INTEGER, search_ts TEXT, query TEXT, result_count INTEGER);
CREATE TABLE clicks(click_id INTEGER PRIMARY KEY, search_id INTEGER, click_ts TEXT, position INTEGER);
INSERT INTO searches VALUES
 (1,1,'2024-03-01 09:00:00','shoes',   5),
 (2,2,'2024-03-01 09:05:00','shooes',  0),
 (3,3,'2024-03-01 10:00:00','bag',    10),
 (4,4,'2024-03-01 11:00:00','watch',   4),
 (5,1,'2024-03-02 09:00:00','phone',  20),
 (6,2,'2024-03-02 09:30:00','case',    3),
 (7,3,'2024-03-02 10:00:00','charger',NULL),
 (8,4,'2024-03-03 08:00:00','lamp',    6);
INSERT INTO clicks VALUES
 (1,1,'2024-03-01 09:00:10',1),(2,1,'2024-03-01 09:00:40',3),
 (3,4,'2024-03-01 11:00:05',2),
 (4,5,'2024-03-02 09:00:07',1),(5,5,'2024-03-02 09:00:30',12),
 (6,6,'2024-03-02 09:30:09',5);
```

**SQL answer:** `SQL_MAIN` (daily metrics) and `SQL_POS` (click-position distribution) in the Code block. `SQL_MAIN`:
```sql
WITH s AS (
  SELECT search_id, date(search_ts) AS d, result_count,
         EXISTS (SELECT 1 FROM clicks c WHERE c.search_id = searches.search_id) AS clicked
  FROM searches
)
SELECT d AS day,
       COUNT(*) AS searches,
       SUM(clicked) AS searches_with_click,
       ROUND(SUM(clicked) * 1.0 / COUNT(*), 2) AS ctr,
       SUM(result_count = 0) AS zero_result,
       ROUND(SUM(result_count = 0) * 1.0 / COUNT(*), 2) AS zero_result_rate
FROM s
GROUP BY d
ORDER BY d
```
```sql
WITH b(bucket, ord) AS (VALUES ('1',1),('2',2),('3',3),('4-10',4),('11+',5)),
d AS (SELECT DISTINCT date(search_ts) AS day FROM searches),
k AS (
  SELECT date(s.search_ts) AS day,
         CASE WHEN c.position = 1 THEN '1' WHEN c.position = 2 THEN '2' WHEN c.position = 3 THEN '3'
              WHEN c.position BETWEEN 4 AND 10 THEN '4-10' ELSE '11+' END AS bucket
  FROM clicks c JOIN searches s ON s.search_id = c.search_id
)
SELECT d.day, b.bucket,
       (SELECT COUNT(*) FROM k WHERE k.day = d.day AND k.bucket = b.bucket) AS clicks,
       ROUND((SELECT COUNT(*) FROM k WHERE k.day = d.day AND k.bucket = b.bucket) * 100.0 /
             NULLIF((SELECT COUNT(*) FROM k WHERE k.day = d.day), 0), 2) AS pct_of_clicks
FROM d CROSS JOIN b
ORDER BY d.day, b.ord
```
`SQL_WRONG` in the Code block is the join-first version, printed in the output for comparison.

**pandas answer:** both results come from one function, identical to the Code block (`isin` is the `EXISTS`; `pd.cut` makes the position buckets):
```py
def search_metrics(searches, clicks):
    s = searches.assign(day=searches["search_ts"].str[:10],
                        clicked=searches["search_id"].isin(clicks["search_id"]),
                        zero=searches["result_count"] == 0)
    daily = (s.groupby("day").agg(searches=("search_id", "size"), searches_with_click=("clicked", "sum"),
                                  zero_result=("zero", "sum")).reset_index())
    daily["ctr"] = (daily["searches_with_click"] / daily["searches"]).round(2)
    daily["zero_result_rate"] = (daily["zero_result"] / daily["searches"]).round(2)
    daily = daily[["day", "searches", "searches_with_click", "ctr", "zero_result", "zero_result_rate"]]

    k = clicks.merge(s[["search_id", "day"]], on="search_id")
    k["bucket"] = pd.cut(k["position"], bins=[0, 1, 2, 3, 10, 10**9],
                         labels=["1", "2", "3", "4-10", "11+"]).astype(str)
    grid = pd.MultiIndex.from_product([sorted(s["day"].unique()), ["1", "2", "3", "4-10", "11+"]],
                                      names=["day", "bucket"]).to_frame(index=False)
    cnt = k.groupby(["day", "bucket"]).size().rename("clicks").reset_index()
    pos = grid.merge(cnt, on=["day", "bucket"], how="left").fillna({"clicks": 0})
    pos["clicks"] = pos["clicks"].astype(int)
    total = pos.groupby("day")["clicks"].transform("sum")
    pos["pct_of_clicks"] = (pos["clicks"] * 100.0 / total.where(total != 0)).round(2)
    return daily, pos
```

**Example:** walk through the sample data by hand.
- 2024-03-01: four searches (1 to 4). Search 1 has two clicks, search 4 has one, searches 2 and 3 none, so searches with a click = 2 and CTR = 2/4 = 0.50. One of the four has `result_count = 0`, zero-result rate 0.25.
- Joining first: search 1 becomes two rows, so the joined table has 5 rows for 4 searches. Counting clicks over true searches gives 3/4 = 0.75, counting click rows over joined rows gives 3/5 = 0.60. Neither is the CTR. On 2024-03-02 the clicks-over-searches version reaches 1.00 although one search in three got no click.
- Zero-result search 2 stays in the denominator (it is a search that could not succeed); the search with `result_count` NULL is in the denominator and not counted as zero-result, so 2024-03-02 shows zero-result rate 0.00.
- Positions on 2024-03-01: clicked positions 1, 3, 2 give 33.33 percent each for buckets 1, 2 and 3 and 0 for the others. On 2024-03-02 positions 1, 12, 5 land in buckets 1, 11+ and 4-10 at 33.33 each. On 2024-03-03 there are no clicks, so the percentages are NULL (NaN in pandas), not 0.

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q25: search metrics: searches, CTR (searches with a click), zero-result rate, clicked position distribution
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE searches(search_id INTEGER PRIMARY KEY, user_id INTEGER, search_ts TEXT, query TEXT, result_count INTEGER);
CREATE TABLE clicks(click_id INTEGER PRIMARY KEY, search_id INTEGER, click_ts TEXT, position INTEGER);
INSERT INTO searches VALUES
 (1,1,'2024-03-01 09:00:00','shoes',   5),
 (2,2,'2024-03-01 09:05:00','shooes',  0),
 (3,3,'2024-03-01 10:00:00','bag',    10),
 (4,4,'2024-03-01 11:00:00','watch',   4),
 (5,1,'2024-03-02 09:00:00','phone',  20),
 (6,2,'2024-03-02 09:30:00','case',    3),
 (7,3,'2024-03-02 10:00:00','charger',NULL),
 (8,4,'2024-03-03 08:00:00','lamp',    6);
INSERT INTO clicks VALUES
 (1,1,'2024-03-01 09:00:10',1),(2,1,'2024-03-01 09:00:40',3),
 (3,4,'2024-03-01 11:00:05',2),
 (4,5,'2024-03-02 09:00:07',1),(5,5,'2024-03-02 09:00:30',12),
 (6,6,'2024-03-02 09:30:09',5);
"""

SQL_MAIN = """
WITH s AS (
  SELECT search_id, date(search_ts) AS d, result_count,
         EXISTS (SELECT 1 FROM clicks c WHERE c.search_id = searches.search_id) AS clicked
  FROM searches
)
SELECT d AS day,
       COUNT(*) AS searches,
       SUM(clicked) AS searches_with_click,
       ROUND(SUM(clicked) * 1.0 / COUNT(*), 2) AS ctr,
       SUM(result_count = 0) AS zero_result,
       ROUND(SUM(result_count = 0) * 1.0 / COUNT(*), 2) AS zero_result_rate
FROM s
GROUP BY d
ORDER BY d
"""
SQL_WRONG = """
SELECT date(s.search_ts) AS day,
       COUNT(*) AS searches_after_join,
       COUNT(DISTINCT s.search_id) AS searches_true,
       ROUND(COUNT(c.click_id) * 1.0 / COUNT(DISTINCT s.search_id), 2) AS clicks_over_searches,
       ROUND(COUNT(c.click_id) * 1.0 / COUNT(*), 2) AS click_rows_over_joined_rows
FROM searches s LEFT JOIN clicks c ON c.search_id = s.search_id
GROUP BY date(s.search_ts)
ORDER BY day
"""
SQL_POS = """
WITH b(bucket, ord) AS (VALUES ('1',1),('2',2),('3',3),('4-10',4),('11+',5)),
d AS (SELECT DISTINCT date(search_ts) AS day FROM searches),
k AS (
  SELECT date(s.search_ts) AS day,
         CASE WHEN c.position = 1 THEN '1' WHEN c.position = 2 THEN '2' WHEN c.position = 3 THEN '3'
              WHEN c.position BETWEEN 4 AND 10 THEN '4-10' ELSE '11+' END AS bucket
  FROM clicks c JOIN searches s ON s.search_id = c.search_id
)
SELECT d.day, b.bucket,
       (SELECT COUNT(*) FROM k WHERE k.day = d.day AND k.bucket = b.bucket) AS clicks,
       ROUND((SELECT COUNT(*) FROM k WHERE k.day = d.day AND k.bucket = b.bucket) * 100.0 /
             NULLIF((SELECT COUNT(*) FROM k WHERE k.day = d.day), 0), 2) AS pct_of_clicks
FROM d CROSS JOIN b
ORDER BY d.day, b.ord
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
sql_pos = pd.read_sql_query(SQL_POS, con)
print("SQL daily metrics:")
print(sql_main.to_string(index=False))
print("SQL wrong CTR (join first, count rows):")
print(pd.read_sql_query(SQL_WRONG, con).to_string(index=False))
print("SQL click position distribution:")
print(sql_pos.to_string(index=False))

searches = pd.read_sql_query("SELECT * FROM searches", con)
clicks = pd.read_sql_query("SELECT * FROM clicks", con)

# pd:main
def search_metrics(searches, clicks):
    s = searches.assign(day=searches["search_ts"].str[:10],
                        clicked=searches["search_id"].isin(clicks["search_id"]),
                        zero=searches["result_count"] == 0)
    daily = (s.groupby("day").agg(searches=("search_id", "size"), searches_with_click=("clicked", "sum"),
                                  zero_result=("zero", "sum")).reset_index())
    daily["ctr"] = (daily["searches_with_click"] / daily["searches"]).round(2)
    daily["zero_result_rate"] = (daily["zero_result"] / daily["searches"]).round(2)
    daily = daily[["day", "searches", "searches_with_click", "ctr", "zero_result", "zero_result_rate"]]

    k = clicks.merge(s[["search_id", "day"]], on="search_id")
    k["bucket"] = pd.cut(k["position"], bins=[0, 1, 2, 3, 10, 10**9],
                         labels=["1", "2", "3", "4-10", "11+"]).astype(str)
    grid = pd.MultiIndex.from_product([sorted(s["day"].unique()), ["1", "2", "3", "4-10", "11+"]],
                                      names=["day", "bucket"]).to_frame(index=False)
    cnt = k.groupby(["day", "bucket"]).size().rename("clicks").reset_index()
    pos = grid.merge(cnt, on=["day", "bucket"], how="left").fillna({"clicks": 0})
    pos["clicks"] = pos["clicks"].astype(int)
    total = pos.groupby("day")["clicks"].transform("sum")
    pos["pct_of_clicks"] = (pos["clicks"] * 100.0 / total.where(total != 0)).round(2)
    return daily, pos
# pd:end

pd_main, pd_pos = search_metrics(searches, clicks)
# both results are already in (day, bucket order) order, which matches the SQL ORDER BY
pd.testing.assert_frame_equal(pd_main, sql_main, check_dtype=False)
pd.testing.assert_frame_equal(pd_pos, sql_pos, check_dtype=False)
print("pandas daily:")
print(pd_main.to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
SQL daily metrics:
       day  searches  searches_with_click  ctr  zero_result  zero_result_rate
2024-03-01         4                    2 0.50            1              0.25
2024-03-02         3                    2 0.67            0              0.00
2024-03-03         1                    0 0.00            0              0.00
SQL wrong CTR (join first, count rows):
       day  searches_after_join  searches_true  clicks_over_searches  click_rows_over_joined_rows
2024-03-01                    5              4                  0.75                         0.60
2024-03-02                    4              3                  1.00                         0.75
2024-03-03                    1              1                  0.00                         0.00
SQL click position distribution:
       day bucket  clicks  pct_of_clicks
2024-03-01      1       1          33.33
2024-03-01      2       1          33.33
2024-03-01      3       1          33.33
2024-03-01   4-10       0           0.00
2024-03-01    11+       0           0.00
2024-03-02      1       1          33.33
2024-03-02      2       0           0.00
2024-03-02      3       0           0.00
2024-03-02   4-10       1          33.33
2024-03-02    11+       1          33.33
2024-03-03      1       0            NaN
2024-03-03      2       0            NaN
2024-03-03      3       0            NaN
2024-03-03   4-10       0            NaN
2024-03-03    11+       0            NaN
pandas daily:
       day  searches  searches_with_click  ctr  zero_result  zero_result_rate
2024-03-01         4                    2 0.50            1              0.25
2024-03-02         3                    2 0.67            0              0.00
2024-03-03         1                    0 0.00            0              0.00
asserts passed
```

**Edge cases:**
- Zero-result searches cannot get a click, so they pull CTR down. Many teams also report CTR over searches that returned results; that is `WHERE result_count > 0` on the denominator and numerator, stated explicitly.
- NULL `result_count` is unknown; `result_count = 0` is false for it, so it is not zero-result.
- A day with searches but no clicks: CTR 0.00 (the flag is 0), positions NaN.
- Click rows whose `search_id` is not in `searches` are ignored by the `EXISTS` form and by the inner merge in the position table.
- Buckets with no clicks need the `CROSS JOIN` against the bucket list, otherwise the row is absent rather than 0.

**Then explain:**
- Two different grains: CTR is per search, position distribution is per click. Do not put them in one join.
- `EXISTS` (or `COUNT(DISTINCT search_id)` after a join) keeps one row per search. `EXISTS` is cheaper because it can stop at the first click.
- Percent of clicks uses clicks as the denominator, so a search with three clicks weighs three times in that table; that is intended and worth saying.
- Click-position metrics such as mean click position or MRR need a decision on searches with no click; not computed here.
- Dialect: the same shape works in Postgres and MySQL; BigQuery would use `COUNTIF` and `DATE(search_ts)` (not executed here).

**Follow-ups:**
- CTR by query? Group by `query`; low volume per query makes it noisy, so show the search count next to it.
- First-click position only? Take `MIN(position)` per search first, then bucket.
- Abandonment (no click and no refinement)? Needs a session notion, see Part 7.

**Common mistakes:**
- Joining searches to clicks and counting rows (shown in the output).
- Using `COUNT(DISTINCT click_id) / COUNT(DISTINCT search_id)`, which is clicks per search, not CTR.
- Treating NULL `result_count` as zero results.
- Dropping the zero-result searches from the denominator without saying so.
- Leaving out zero-count buckets so the distribution does not show them.


### Q26 ⭐⭐ 🟡 Notification and email funnel: sends(send_id, user_id, channel, sent_ts) with channel in ('push', 'email'), opens(send_id, open_ts) and clicks(send_id, click_ts), where opens and clicks can repeat per send. Return per channel sent, unique opens, unique clicks, open rate, click-to-open rate (CTOR) and click-through rate over sent, counting each send once. Explain why raw event counts overstate rates, why a click without an open row can occur (image blocking, Apple mail privacy prefetch inflating opens) and how that makes click-to-open above 100 percent possible, and what a send-level versus user-level rate means.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and product analytics rounds at product companies and GCCs
**Say this first (1 line):** Collapse opens and clicks to one flag per send with `EXISTS`, then count sends: open rate is opened sends over sent, click-to-open is clicked sends over opened sends, and click-through is clicked sends over sent; raw event counts overstate every rate when a send is opened or clicked several times.

**Schema and sample data:** eight sends over two channels (`push` and `email`) to three users. Send 1 has two open rows, send 5 has three open rows and two click rows, so event counts exceed send counts. Sends 3, 6 and 8 have a click and no open row. Send 4 has no open and no click. All data is made up.
```sql
CREATE TABLE sends(send_id INTEGER PRIMARY KEY, user_id INTEGER, channel TEXT, sent_ts TEXT);
CREATE TABLE opens(send_id INTEGER, open_ts TEXT);
CREATE TABLE clicks(send_id INTEGER, click_ts TEXT);
INSERT INTO sends VALUES
 (1,1,'push', '2024-03-01 09:00:00'),(2,1,'push', '2024-03-02 09:00:00'),
 (3,2,'push', '2024-03-01 09:00:00'),(4,3,'push', '2024-03-01 09:00:00'),
 (5,1,'email','2024-03-01 08:00:00'),(6,2,'email','2024-03-01 08:00:00'),
 (7,2,'email','2024-03-02 08:00:00'),(8,3,'email','2024-03-01 08:00:00');
INSERT INTO opens VALUES
 (1,'2024-03-01 09:01:00'),(1,'2024-03-01 20:00:00'),(2,'2024-03-02 09:02:00'),
 (5,'2024-03-01 08:05:00'),(5,'2024-03-01 08:06:00'),(5,'2024-03-02 07:00:00'),
 (7,'2024-03-02 08:10:00');
INSERT INTO clicks VALUES
 (1,'2024-03-01 09:01:30'),
 (3,'2024-03-01 09:30:00'),
 (5,'2024-03-01 08:05:30'),(5,'2024-03-01 08:07:00'),
 (6,'2024-03-01 12:00:00'),
 (8,'2024-03-01 13:00:00');
```

**SQL answer:** `SQL_MAIN` in the Code block (`SQL_RAW` for the wrong raw-count rates and `SQL_USER` for the user-level open rate are in the Code block too):
```sql
WITH f AS (
  SELECT s.send_id, s.user_id, s.channel,
         EXISTS (SELECT 1 FROM opens  o WHERE o.send_id = s.send_id) AS opened,
         EXISTS (SELECT 1 FROM clicks c WHERE c.send_id = s.send_id) AS clicked
  FROM sends s
)
SELECT channel,
       COUNT(*) AS sent,
       SUM(opened) AS unique_opens,
       SUM(clicked) AS unique_clicks,
       ROUND(SUM(opened) * 1.0 / COUNT(*), 2) AS open_rate,
       ROUND(SUM(clicked) * 1.0 / NULLIF(SUM(opened), 0), 2) AS ctor,
       ROUND(SUM(clicked) * 1.0 / COUNT(*), 2) AS ctr,
       SUM(clicked AND NOT opened) AS click_without_open,
       ROUND(SUM(opened AND clicked) * 1.0 / NULLIF(SUM(opened), 0), 2) AS ctor_clicked_and_opened
FROM f
GROUP BY channel
ORDER BY channel
```
```sql
WITH f AS (
  SELECT s.user_id, s.channel,
         EXISTS (SELECT 1 FROM opens o WHERE o.send_id = s.send_id) AS opened
  FROM sends s
)
SELECT channel, COUNT(DISTINCT user_id) AS users_sent,
       COUNT(DISTINCT CASE WHEN opened THEN user_id END) AS users_opened,
       ROUND(COUNT(DISTINCT CASE WHEN opened THEN user_id END) * 1.0 / COUNT(DISTINCT user_id), 2) AS user_open_rate
FROM f GROUP BY channel ORDER BY channel
```

**pandas answer:** the send-level function, identical to the Code block:
```py
def notification_funnel(sends, opens, clicks):
    f = sends.assign(opened=sends["send_id"].isin(opens["send_id"]),
                     clicked=sends["send_id"].isin(clicks["send_id"]))
    f["both"] = f["opened"] & f["clicked"]
    f["click_no_open"] = f["clicked"] & ~f["opened"]
    out = f.groupby("channel").agg(sent=("send_id", "size"), unique_opens=("opened", "sum"),
                                   unique_clicks=("clicked", "sum"),
                                   click_without_open=("click_no_open", "sum"),
                                   both=("both", "sum")).reset_index()
    opened = out["unique_opens"].where(out["unique_opens"] != 0)
    out["open_rate"] = (out["unique_opens"] / out["sent"]).round(2)
    out["ctor"] = (out["unique_clicks"] / opened).round(2)
    out["ctr"] = (out["unique_clicks"] / out["sent"]).round(2)
    out["ctor_clicked_and_opened"] = (out["both"] / opened).round(2)
    return out[["channel", "sent", "unique_opens", "unique_clicks", "open_rate", "ctor", "ctr",
                "click_without_open", "ctor_clicked_and_opened"]]
```

**Example:** walk through the sample data by hand.
- Push has sends 1 to 4. Opened: sends 1 (two open rows) and 2, so unique opens 2. Clicked: sends 1 and 3, unique clicks 2. Open rate 2/4 = 0.50, CTOR 2/2 = 1.00, CTR over sent 2/4 = 0.50. Send 3 is a click with no open row.
- Email has sends 5 to 8. Opened: sends 5 (three open rows) and 7, so 2. Clicked: sends 5, 6 and 8, so 3. Open rate 2/4 = 0.50, CTR 3/4 = 0.75, CTOR 3/2 = 1.50, which is above 100 percent because two of the three clicked sends (6 and 8) have no open row.
- Restricting CTOR to clicks on sends that were also opened gives 1/2 = 0.50 for email and 1/2 = 0.50 for push; that is the alternative "clean" definition.
- Raw event counts: email has 4 open events and 4 click events for 4 sends, so a raw open rate of 1.00 and a raw click-over-open of 1.00 instead of 0.50 and 1.50; the unit is wrong.
- User level: push went to users 1, 2 and 3; only user 1 opened (both of their sends), so 1/3 = 0.33 users opened against a send-level 0.50. Email is 2/3 = 0.67 at user level against 0.50 at send level.

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q26: notification and email funnel: unique opens, unique clicks, open rate, CTOR, CTR over sent
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sends(send_id INTEGER PRIMARY KEY, user_id INTEGER, channel TEXT, sent_ts TEXT);
CREATE TABLE opens(send_id INTEGER, open_ts TEXT);
CREATE TABLE clicks(send_id INTEGER, click_ts TEXT);
INSERT INTO sends VALUES
 (1,1,'push', '2024-03-01 09:00:00'),(2,1,'push', '2024-03-02 09:00:00'),
 (3,2,'push', '2024-03-01 09:00:00'),(4,3,'push', '2024-03-01 09:00:00'),
 (5,1,'email','2024-03-01 08:00:00'),(6,2,'email','2024-03-01 08:00:00'),
 (7,2,'email','2024-03-02 08:00:00'),(8,3,'email','2024-03-01 08:00:00');
INSERT INTO opens VALUES
 (1,'2024-03-01 09:01:00'),(1,'2024-03-01 20:00:00'),(2,'2024-03-02 09:02:00'),
 (5,'2024-03-01 08:05:00'),(5,'2024-03-01 08:06:00'),(5,'2024-03-02 07:00:00'),
 (7,'2024-03-02 08:10:00');
INSERT INTO clicks VALUES
 (1,'2024-03-01 09:01:30'),
 (3,'2024-03-01 09:30:00'),
 (5,'2024-03-01 08:05:30'),(5,'2024-03-01 08:07:00'),
 (6,'2024-03-01 12:00:00'),
 (8,'2024-03-01 13:00:00');
"""

SQL_MAIN = """
WITH f AS (
  SELECT s.send_id, s.user_id, s.channel,
         EXISTS (SELECT 1 FROM opens  o WHERE o.send_id = s.send_id) AS opened,
         EXISTS (SELECT 1 FROM clicks c WHERE c.send_id = s.send_id) AS clicked
  FROM sends s
)
SELECT channel,
       COUNT(*) AS sent,
       SUM(opened) AS unique_opens,
       SUM(clicked) AS unique_clicks,
       ROUND(SUM(opened) * 1.0 / COUNT(*), 2) AS open_rate,
       ROUND(SUM(clicked) * 1.0 / NULLIF(SUM(opened), 0), 2) AS ctor,
       ROUND(SUM(clicked) * 1.0 / COUNT(*), 2) AS ctr,
       SUM(clicked AND NOT opened) AS click_without_open,
       ROUND(SUM(opened AND clicked) * 1.0 / NULLIF(SUM(opened), 0), 2) AS ctor_clicked_and_opened
FROM f
GROUP BY channel
ORDER BY channel
"""
SQL_RAW = """
SELECT s.channel,
       (SELECT COUNT(*) FROM opens  o JOIN sends x ON x.send_id = o.send_id WHERE x.channel = s.channel) AS open_events,
       (SELECT COUNT(*) FROM clicks c JOIN sends x ON x.send_id = c.send_id WHERE x.channel = s.channel) AS click_events,
       COUNT(*) AS sent
FROM sends s GROUP BY s.channel ORDER BY s.channel
"""
SQL_USER = """
WITH f AS (
  SELECT s.user_id, s.channel,
         EXISTS (SELECT 1 FROM opens o WHERE o.send_id = s.send_id) AS opened
  FROM sends s
)
SELECT channel, COUNT(DISTINCT user_id) AS users_sent,
       COUNT(DISTINCT CASE WHEN opened THEN user_id END) AS users_opened,
       ROUND(COUNT(DISTINCT CASE WHEN opened THEN user_id END) * 1.0 / COUNT(DISTINCT user_id), 2) AS user_open_rate
FROM f GROUP BY channel ORDER BY channel
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
print("SQL, each send counted once:")
print(sql_main.to_string(index=False))
raw = pd.read_sql_query(SQL_RAW, con)
raw["raw_open_rate"] = (raw["open_events"] / raw["sent"]).round(2)
raw["raw_click_over_open_events"] = (raw["click_events"] / raw["open_events"]).round(2)
print("SQL, raw event counts (wrong rates):")
print(raw.to_string(index=False))
sql_user = pd.read_sql_query(SQL_USER, con)
print("SQL, user-level open rate:")
print(sql_user.to_string(index=False))

sends = pd.read_sql_query("SELECT * FROM sends", con)
opens = pd.read_sql_query("SELECT * FROM opens", con)
clicks = pd.read_sql_query("SELECT * FROM clicks", con)

# pd:main
def notification_funnel(sends, opens, clicks):
    f = sends.assign(opened=sends["send_id"].isin(opens["send_id"]),
                     clicked=sends["send_id"].isin(clicks["send_id"]))
    f["both"] = f["opened"] & f["clicked"]
    f["click_no_open"] = f["clicked"] & ~f["opened"]
    out = f.groupby("channel").agg(sent=("send_id", "size"), unique_opens=("opened", "sum"),
                                   unique_clicks=("clicked", "sum"),
                                   click_without_open=("click_no_open", "sum"),
                                   both=("both", "sum")).reset_index()
    opened = out["unique_opens"].where(out["unique_opens"] != 0)
    out["open_rate"] = (out["unique_opens"] / out["sent"]).round(2)
    out["ctor"] = (out["unique_clicks"] / opened).round(2)
    out["ctr"] = (out["unique_clicks"] / out["sent"]).round(2)
    out["ctor_clicked_and_opened"] = (out["both"] / opened).round(2)
    return out[["channel", "sent", "unique_opens", "unique_clicks", "open_rate", "ctor", "ctr",
                "click_without_open", "ctor_clicked_and_opened"]]
# pd:end

pd_main = notification_funnel(sends, opens, clicks)
# compare after sorting by channel (SQL result is already in that order)
pd.testing.assert_frame_equal(pd_main.sort_values("channel").reset_index(drop=True), sql_main, check_dtype=False)
u = sends.assign(opened=sends["send_id"].isin(opens["send_id"]))
pd_user = (u.groupby("channel").apply(lambda g: pd.Series({
    "users_sent": g["user_id"].nunique(), "users_opened": g.loc[g["opened"], "user_id"].nunique()}),
    include_groups=False).reset_index())
pd_user["user_open_rate"] = (pd_user["users_opened"] / pd_user["users_sent"]).round(2)
pd.testing.assert_frame_equal(pd_user, sql_user, check_dtype=False)
print("pandas:")
print(pd_main.to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
SQL, each send counted once:
channel  sent  unique_opens  unique_clicks  open_rate  ctor  ctr  click_without_open  ctor_clicked_and_opened
  email     4             2              3        0.5   1.5 0.75                   2                      0.5
   push     4             2              2        0.5   1.0 0.50                   1                      0.5
SQL, raw event counts (wrong rates):
channel  open_events  click_events  sent  raw_open_rate  raw_click_over_open_events
  email            4             4     4           1.00                        1.00
   push            3             2     4           0.75                        0.67
SQL, user-level open rate:
channel  users_sent  users_opened  user_open_rate
  email           3             2            0.67
   push           3             1            0.33
pandas:
channel  sent  unique_opens  unique_clicks  open_rate  ctor  ctr  click_without_open  ctor_clicked_and_opened
  email     4             2              3        0.5   1.5 0.75                   2                      0.5
   push     4             2              2        0.5   1.0 0.50                   1                      0.5
asserts passed
```

**Edge cases:**
- A click with no open row: possible when images are blocked (the open pixel never loads), when the open tracking fails, or in push when the app records the tap without an open event. The result is CTOR above 1.
- Apple Mail Privacy Protection: general knowledge, not sourced here and not tested, is that it can preload email content on behalf of the user, which is widely reported to inflate email open counts; treat email open rate as an upper bound and lean on clicks.
- Opens and clicks that arrive before `sent_ts` or for unknown send ids point to a data problem; here they would be ignored by the `EXISTS` form.
- Zero opened sends gives CTOR NULL through `NULLIF`.
- Repeated rows per send (re-opens) are why distinct sends, not rows, are counted.

**Then explain:**
- Unit: one send is one chance to open. Open rate, CTOR and CTR all count sends, so each send is counted once no matter how many open or click rows it has.
- `EXISTS` per send avoids joining opens and clicks to sends together, which would multiply rows (opens times clicks per send).
- CTOR above 100 percent is a symptom, not a bug in the SQL: the click numerator and the open denominator are measured by different tracking.
- Send-level versus user-level: a user who got two pushes and opened both is two sends opened but one user opened. User-level rates answer 'how many people engaged'; send-level rates answer 'how well does a message perform'.
- Dialect: `EXISTS` and `COUNT(DISTINCT ...)` are portable; BigQuery or Postgres users might prefer `COUNTIF` or `FILTER` (not executed here).

**Follow-ups:**
- Which rate do you trust for email? Clicks over sent, because opens may be prefetched; say it is a judgement.
- Per campaign? Group by campaign id; keep the per-send flag CTE.
- Unsubscribes or bounces in the denominator? Define delivered sends and use that as the denominator; bounces are not in this table.

**Common mistakes:**
- Dividing event counts (open rows, click rows) by sends.
- Joining sends to opens and to clicks in one query without pre-aggregating.
- Computing CTOR as clicks over sends or opens over clicks.
- Treating CTOR above 1 as a bug and clipping it without explaining.
- Mixing user-level numerators with send-level denominators.


### Q27 ⭐⭐ 🟡 Cart abandonment and bounce rate: events(session_id, user_id, event_ts, event_name) with event_name in ('page_view', 'add_to_cart', 'purchase'). Return the cart abandonment rate (sessions with an add_to_cart and no purchase over sessions with an add_to_cart) and the bounce rate (sessions with exactly one event over all sessions), per day of the first event. Show a session with a purchase before the add_to_cart, the effect of a purchase in a later session (a different session id, so the first session still counts as abandoned) and why bounce depends on the event definition (one page_view only versus one event of any kind).
**Asked at:** e-commerce and marketplace metric lists: letsdatascience e-commerce SQL list (opened; repeat purchase rate, cart abandonment, top products by category, fan-out and grain pitfalls) and LearnSQL 'SQL metrics in real interviews' (opened; metric patterns breakdown, ratio, KPI, with joins that inflate results and division by zero as pitfalls; one author's own 11 interviews, no questions published); guides, not candidate reports; e-commerce, fintech and marketplace analyst rounds
**Say this first (1 line):** Collapse events to one row per session with flags (`MAX(event_name = ...)`), take the day from the session's first event, then abandonment is cart sessions without a purchase over cart sessions and bounce is sessions with exactly one event over all sessions; the definitions of 'no purchase' and of 'one event' are the two things to state out loud.

**Schema and sample data:** fifteen events in nine sessions. Session D has the purchase before the add_to_cart. User 6 adds to cart in session F and buys in a different session G. Session E is a single add_to_cart. Session H has two page views. Session I (2024-03-03) is a single page view and there is no cart session that day.
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, session_id TEXT, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1, 'A',1,'2024-03-01 09:00:00','page_view'),
 (2, 'A',1,'2024-03-01 09:01:00','add_to_cart'),
 (3, 'A',1,'2024-03-01 09:02:00','purchase'),
 (4, 'B',2,'2024-03-01 10:00:00','page_view'),
 (5, 'B',2,'2024-03-01 10:01:00','add_to_cart'),
 (6, 'C',3,'2024-03-01 11:00:00','page_view'),
 (7, 'D',4,'2024-03-01 12:00:00','purchase'),
 (8, 'D',4,'2024-03-01 12:01:00','add_to_cart'),
 (9, 'E',5,'2024-03-01 13:00:00','add_to_cart'),
 (10,'F',6,'2024-03-02 09:00:00','page_view'),
 (11,'F',6,'2024-03-02 09:01:00','add_to_cart'),
 (12,'G',6,'2024-03-02 18:00:00','purchase'),
 (13,'H',7,'2024-03-02 10:00:00','page_view'),
 (14,'H',7,'2024-03-02 10:01:00','page_view'),
 (15,'I',8,'2024-03-03 10:00:00','page_view');
```

**SQL answer:** `SQL_MAIN` in the Code block (literal definition: a cart session is abandoned when it has no purchase anywhere in the session), and `SQL_ORDERED` for the variant where the purchase must come at or after the first add_to_cart:
```sql
WITH s AS (
  SELECT session_id,
         date(MIN(event_ts)) AS day,
         COUNT(*) AS n_events,
         MAX(event_name = 'add_to_cart') AS has_cart,
         MAX(event_name = 'purchase') AS has_purchase,
         MAX(event_name = 'page_view') AS has_view
  FROM events
  GROUP BY session_id
)
SELECT day,
       COUNT(*) AS sessions,
       SUM(has_cart) AS cart_sessions,
       SUM(has_cart = 1 AND has_purchase = 0) AS abandoned,
       ROUND(SUM(has_cart = 1 AND has_purchase = 0) * 1.0 / NULLIF(SUM(has_cart), 0), 2) AS abandonment_rate,
       SUM(n_events = 1) AS bounce_any_event,
       ROUND(SUM(n_events = 1) * 1.0 / COUNT(*), 2) AS bounce_rate_any,
       SUM(n_events = 1 AND has_view = 1) AS bounce_one_page_view,
       ROUND(SUM(n_events = 1 AND has_view = 1) * 1.0 / COUNT(*), 2) AS bounce_rate_pv
FROM s
GROUP BY day
ORDER BY day
```
```sql
WITH s AS (
  SELECT session_id, date(MIN(event_ts)) AS day,
         MIN(CASE WHEN event_name = 'add_to_cart' THEN event_ts END) AS first_cart,
         MAX(CASE WHEN event_name = 'purchase' THEN event_ts END) AS last_purchase
  FROM events GROUP BY session_id
)
SELECT day,
       SUM(first_cart IS NOT NULL) AS cart_sessions,
       SUM(first_cart IS NOT NULL AND (last_purchase IS NULL OR last_purchase < first_cart)) AS abandoned,
       ROUND(SUM(first_cart IS NOT NULL AND (last_purchase IS NULL OR last_purchase < first_cart)) * 1.0 /
             NULLIF(SUM(first_cart IS NOT NULL), 0), 2) AS abandonment_rate_ordered
FROM s GROUP BY day ORDER BY day
```

**pandas answer:** the same logic for the main definition, identical to the Code block:
```py
def session_metrics(events):
    e = events.assign(cart=events["event_name"] == "add_to_cart",
                      buy=events["event_name"] == "purchase",
                      view=events["event_name"] == "page_view")
    s = e.groupby("session_id").agg(first_ts=("event_ts", "min"), n_events=("event_id", "size"),
                                    has_cart=("cart", "max"), has_purchase=("buy", "max"),
                                    has_view=("view", "max")).reset_index()
    s["day"] = s["first_ts"].str[:10]
    s["abandon"] = s["has_cart"] & ~s["has_purchase"]
    s["bounce_any"] = s["n_events"] == 1
    s["bounce_pv"] = s["bounce_any"] & s["has_view"]
    out = s.groupby("day").agg(sessions=("session_id", "size"), cart_sessions=("has_cart", "sum"),
                               abandoned=("abandon", "sum"), bounce_any_event=("bounce_any", "sum"),
                               bounce_one_page_view=("bounce_pv", "sum")).reset_index()
    out["abandonment_rate"] = (out["abandoned"] / out["cart_sessions"].where(out["cart_sessions"] != 0)).round(2)
    out["bounce_rate_any"] = (out["bounce_any_event"] / out["sessions"]).round(2)
    out["bounce_rate_pv"] = (out["bounce_one_page_view"] / out["sessions"]).round(2)
    return out[["day", "sessions", "cart_sessions", "abandoned", "abandonment_rate",
                "bounce_any_event", "bounce_rate_any", "bounce_one_page_view", "bounce_rate_pv"]]
```

**Example:** walk through the sample data by hand.
- 2024-03-01 has sessions A to E. Cart sessions: A, B, D, E (4). With the literal definition A (bought) and D (bought, earlier) are not abandoned; B and E are, so 2/4 = 0.50.
- With the ordered variant D counts as abandoned (its purchase came before the cart), so 3/4 = 0.75. One session moves the rate by 25 points.
- 2024-03-02: F has a cart and no purchase in F; the purchase is in session G (a different id), so F is abandoned: 1/1 = 1.00. If you stitched sessions per user within a day the answer would differ, but the question says sessions stay separate.
- Bounce on 2024-03-01: session C (one page_view) and session E (one add_to_cart) have exactly one event, so 2/5 = 0.40 under 'one event of any kind'; only C is a single page view, so 1/5 = 0.20 under 'one page_view only'.
- 2024-03-02: G (one purchase) is the only single-event session, 1/3 = 0.33 under the any-event rule and 0 under the page_view rule. H has two page views so it is not a bounce here.
- 2024-03-03: no cart session, so abandonment is NULL (not 0); the one session is a bounce, 1.00.

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q27: cart abandonment rate and bounce rate per day of the session's first event
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, session_id TEXT, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1, 'A',1,'2024-03-01 09:00:00','page_view'),
 (2, 'A',1,'2024-03-01 09:01:00','add_to_cart'),
 (3, 'A',1,'2024-03-01 09:02:00','purchase'),
 (4, 'B',2,'2024-03-01 10:00:00','page_view'),
 (5, 'B',2,'2024-03-01 10:01:00','add_to_cart'),
 (6, 'C',3,'2024-03-01 11:00:00','page_view'),
 (7, 'D',4,'2024-03-01 12:00:00','purchase'),
 (8, 'D',4,'2024-03-01 12:01:00','add_to_cart'),
 (9, 'E',5,'2024-03-01 13:00:00','add_to_cart'),
 (10,'F',6,'2024-03-02 09:00:00','page_view'),
 (11,'F',6,'2024-03-02 09:01:00','add_to_cart'),
 (12,'G',6,'2024-03-02 18:00:00','purchase'),
 (13,'H',7,'2024-03-02 10:00:00','page_view'),
 (14,'H',7,'2024-03-02 10:01:00','page_view'),
 (15,'I',8,'2024-03-03 10:00:00','page_view');
"""

SQL_MAIN = """
WITH s AS (
  SELECT session_id,
         date(MIN(event_ts)) AS day,
         COUNT(*) AS n_events,
         MAX(event_name = 'add_to_cart') AS has_cart,
         MAX(event_name = 'purchase') AS has_purchase,
         MAX(event_name = 'page_view') AS has_view
  FROM events
  GROUP BY session_id
)
SELECT day,
       COUNT(*) AS sessions,
       SUM(has_cart) AS cart_sessions,
       SUM(has_cart = 1 AND has_purchase = 0) AS abandoned,
       ROUND(SUM(has_cart = 1 AND has_purchase = 0) * 1.0 / NULLIF(SUM(has_cart), 0), 2) AS abandonment_rate,
       SUM(n_events = 1) AS bounce_any_event,
       ROUND(SUM(n_events = 1) * 1.0 / COUNT(*), 2) AS bounce_rate_any,
       SUM(n_events = 1 AND has_view = 1) AS bounce_one_page_view,
       ROUND(SUM(n_events = 1 AND has_view = 1) * 1.0 / COUNT(*), 2) AS bounce_rate_pv
FROM s
GROUP BY day
ORDER BY day
"""
# variant: a purchase only completes the cart if it happens at or after the first add_to_cart
SQL_ORDERED = """
WITH s AS (
  SELECT session_id, date(MIN(event_ts)) AS day,
         MIN(CASE WHEN event_name = 'add_to_cart' THEN event_ts END) AS first_cart,
         MAX(CASE WHEN event_name = 'purchase' THEN event_ts END) AS last_purchase
  FROM events GROUP BY session_id
)
SELECT day,
       SUM(first_cart IS NOT NULL) AS cart_sessions,
       SUM(first_cart IS NOT NULL AND (last_purchase IS NULL OR last_purchase < first_cart)) AS abandoned,
       ROUND(SUM(first_cart IS NOT NULL AND (last_purchase IS NULL OR last_purchase < first_cart)) * 1.0 /
             NULLIF(SUM(first_cart IS NOT NULL), 0), 2) AS abandonment_rate_ordered
FROM s GROUP BY day ORDER BY day
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
sql_ord = pd.read_sql_query(SQL_ORDERED, con)
print("SQL (abandoned = cart and no purchase anywhere in the session):")
print(sql_main.to_string(index=False))
print("SQL variant (purchase must be at or after the first add_to_cart):")
print(sql_ord.to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)

# pd:main
def session_metrics(events):
    e = events.assign(cart=events["event_name"] == "add_to_cart",
                      buy=events["event_name"] == "purchase",
                      view=events["event_name"] == "page_view")
    s = e.groupby("session_id").agg(first_ts=("event_ts", "min"), n_events=("event_id", "size"),
                                    has_cart=("cart", "max"), has_purchase=("buy", "max"),
                                    has_view=("view", "max")).reset_index()
    s["day"] = s["first_ts"].str[:10]
    s["abandon"] = s["has_cart"] & ~s["has_purchase"]
    s["bounce_any"] = s["n_events"] == 1
    s["bounce_pv"] = s["bounce_any"] & s["has_view"]
    out = s.groupby("day").agg(sessions=("session_id", "size"), cart_sessions=("has_cart", "sum"),
                               abandoned=("abandon", "sum"), bounce_any_event=("bounce_any", "sum"),
                               bounce_one_page_view=("bounce_pv", "sum")).reset_index()
    out["abandonment_rate"] = (out["abandoned"] / out["cart_sessions"].where(out["cart_sessions"] != 0)).round(2)
    out["bounce_rate_any"] = (out["bounce_any_event"] / out["sessions"]).round(2)
    out["bounce_rate_pv"] = (out["bounce_one_page_view"] / out["sessions"]).round(2)
    return out[["day", "sessions", "cart_sessions", "abandoned", "abandonment_rate",
                "bounce_any_event", "bounce_rate_any", "bounce_one_page_view", "bounce_rate_pv"]]
# pd:end

pd_main = session_metrics(events)
# compare after sorting by day (SQL result is already in that order)
pd.testing.assert_frame_equal(pd_main.sort_values("day").reset_index(drop=True), sql_main, check_dtype=False)
print("pandas:")
print(pd_main.to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
SQL (abandoned = cart and no purchase anywhere in the session):
       day  sessions  cart_sessions  abandoned  abandonment_rate  bounce_any_event  bounce_rate_any  bounce_one_page_view  bounce_rate_pv
2024-03-01         5              4          2               0.5                 2             0.40                     1             0.2
2024-03-02         3              1          1               1.0                 1             0.33                     0             0.0
2024-03-03         1              0          0               NaN                 1             1.00                     1             1.0
SQL variant (purchase must be at or after the first add_to_cart):
       day  cart_sessions  abandoned  abandonment_rate_ordered
2024-03-01              4          3                      0.75
2024-03-02              1          1                      1.00
2024-03-03              0          0                       NaN
pandas:
       day  sessions  cart_sessions  abandoned  abandonment_rate  bounce_any_event  bounce_rate_any  bounce_one_page_view  bounce_rate_pv
2024-03-01         5              4          2               0.5                 2             0.40                     1             0.2
2024-03-02         3              1          1               1.0                 1             0.33                     0             0.0
2024-03-03         1              0          0               NaN                 1             1.00                     1             1.0
asserts passed
```

**Edge cases:**
- No cart sessions on a day: `NULLIF(SUM(has_cart), 0)` returns NULL; reporting 0 would suggest nobody abandoned.
- Sessions that cross midnight belong to the day of their first event (`date(MIN(event_ts))`), not split by day.
- Session id reuse across users or days would merge unrelated rows; assume the id is unique and, if it is not, group by (user_id, session_id).
- Ties on `event_ts` do not matter for these flags except in the ordered variant, where a purchase and a cart at the same timestamp counts as completed (`<` test).
- Bounce is also sometimes defined with time on page; not available here.

**Then explain:**
- Grain: the rate is a ratio of sessions, so build one row per session first and aggregate that. Counting events gives different, wrong, numbers.
- 'Abandoned' must be defined: literal (no purchase in the session) versus ordered (no purchase after the cart). They differ when purchases can precede carts (for example a re-order flow).
- A purchase in a later session does not rescue the earlier session in this metric; a user-level or time-windowed cart abandonment would, and is a different metric.
- Bounce depends on the event definition: with 'one page_view only' a single `add_to_cart` or `purchase` session is not a bounce; with 'one event of any kind' it is. Many analytics tools define bounce differently again (engagement based); state which one you use.
- Dialect: `MAX(boolean)` as a flag works in SQLite and MySQL; in Postgres use `BOOL_OR(...)` or `MAX(CASE WHEN ... THEN 1 ELSE 0 END)` (not executed here).

**Follow-ups:**
- Cart abandonment at user-day level? Group by user and day first, then apply the flags.
- Add checkout steps? That is a funnel; keep the per-session flags and add one flag per step.
- Abandonment value (cart value lost)? Needs cart contents; not in this table.

**Common mistakes:**
- Computing abandonment over all sessions instead of cart sessions.
- Counting events, not sessions, in numerator or denominator.
- Not saying whether a purchase before the cart counts.
- Defining bounce by `COUNT(*) = 1` and then reporting it as 'single page_view'.
- Reporting 0 when the denominator is empty.


### Q28 ⭐⭐ 🟡 Engagement distribution and power users: events(user_id, event_ts, event_name) and users(user_id, signup_date, country, is_test). For March 2024 return events per active user (mean and median, SQLite has no MEDIAN so use a window or ORDER BY LIMIT approach), the power-user cut using NTILE(10) over users ranked by event count (see Part 4 for NTILE), and the share of all events produced by the top decile. Explain why the mean is misleading for skewed usage, how ties across a decile boundary behave, and how users with zero events in the month are handled (included or excluded changes every number).
**Asked at:** StrataScratch product-analytics blog (opened; lists five questions such as Meta Users By Average Session Time and Salesforce User Growth Rate, none labelled candidate-reported) and DataLemur and Interview Query pages (search snippets only); practice-site material, not candidate reports; product analytics and data scientist rounds
**Say this first (1 line):** Count March events per user, take the mean with `AVG` and the median from `ROW_NUMBER` and `COUNT(*) OVER ()` (SQLite has no MEDIAN), cut `NTILE(10)` over users ordered by event count with a `user_id` tie-breaker, and divide the top decile's events by all events; whether zero-event users are in the population changes every one of these numbers, so say which one you use.

**Schema and sample data:** thirteen users (user 13 is a test user, user 12 and user 11 have no March events). The `events` rows are generated in the Code block: March counts per user are 1, 1, 2, 2, 3, 4, 5, 8, 20, 60 for users 1 to 10 (106 events), plus four rows that must be ignored: a February event for user 1, an April 1st event for user 2 (the upper bound is exclusive), a February event for user 11 and a March event for test user 13. Dates and counts are toy values.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-05','IN',0),(2,'2024-01-06','IN',0),(3,'2024-01-07','IN',0),(4,'2024-01-08','IN',0),
 (5,'2024-01-09','IN',0),(6,'2024-01-10','IN',0),(7,'2024-01-11','IN',0),(8,'2024-01-12','IN',0),
 (9,'2024-01-13','IN',0),(10,'2024-01-14','IN',0),(11,'2024-01-15','IN',0),(12,'2024-01-16','IN',0),
 (13,'2024-01-17','IN',1);
```

**SQL answer:** `SQL_TEMPLATE` in the Code block, with `{JOIN}` replaced by `JOIN` (active users only, `SQL_ACTIVE`) or `LEFT JOIN` (all non-test registered users, `SQL_ALL`). The median is the average of the rows at positions `(cnt + 1) / 2` and `(cnt + 2) / 2` (integer division, see Part 4 Q38 for the median pattern in full). `SQL_TEMPLATE`:
```sql
WITH u AS (
  SELECT us.user_id, COUNT(e.event_id) AS n
  FROM users us
  {JOIN} events e ON e.user_id = us.user_id
       AND e.event_ts >= '2024-03-01' AND e.event_ts < '2024-04-01'
  WHERE us.is_test = 0
  GROUP BY us.user_id
), r AS (
  SELECT user_id, n,
         NTILE(10) OVER (ORDER BY n DESC, user_id) AS decile,
         ROW_NUMBER() OVER (ORDER BY n, user_id) AS rn,
         COUNT(*) OVER () AS cnt
  FROM u
), med AS (
  SELECT AVG(n) AS median FROM r WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
)
SELECT COUNT(*) AS users,
       SUM(n) AS events,
       ROUND(AVG(n), 2) AS mean_events,
       (SELECT median FROM med) AS median_events,
       SUM(decile = 1) AS top_decile_users,
       SUM(CASE WHEN decile = 1 THEN n END) AS top_decile_events,
       ROUND(SUM(CASE WHEN decile = 1 THEN n END) * 100.0 / SUM(n), 2) AS top_decile_share_pct
FROM r
```
NTILE itself is explained in Part 4 Q21 and pandas `qcut` versus NTILE in Part 4 Q33; here pandas needs a hand-written NTILE (`ntile` in the function below), because `qcut` splits by value, not by position.

**pandas answer:** the same logic (`keep_zero` is the INNER versus LEFT join choice; `ntile` reproduces positional NTILE):
```py
def ntile(n_rows, k):
    # NTILE: the first (n_rows % k) buckets get one extra row; assigned by position
    base, extra = divmod(n_rows, k)
    out = []
    for i in range(n_rows):
        if i < extra * (base + 1):
            out.append(i // (base + 1) + 1)
        else:
            out.append(extra + (i - extra * (base + 1)) // base + 1)
    return out

def engagement(users, events, keep_zero):
    m = events[(events["event_ts"] >= "2024-03-01") & (events["event_ts"] < "2024-04-01")]
    cnt = m.groupby("user_id").size().rename("n")
    u = users.loc[users["is_test"] == 0, ["user_id"]].merge(cnt, on="user_id", how="left")
    u["n"] = u["n"].fillna(0).astype(int)
    if not keep_zero:
        u = u[u["n"] > 0]
    u = u.sort_values(["n", "user_id"], ascending=[False, True]).reset_index(drop=True)
    u["decile"] = ntile(len(u), 10) if len(u) >= 10 else range(1, len(u) + 1)
    top = u[u["decile"] == 1]
    return pd.DataFrame({"users": [len(u)], "events": [u["n"].sum()], "mean_events": [round(u["n"].mean(), 2)],
                         "median_events": [float(u["n"].median())], "top_decile_users": [len(top)],
                         "top_decile_events": [top["n"].sum()],
                         "top_decile_share_pct": [round(top["n"].sum() * 100.0 / u["n"].sum(), 2)]}), u
```

**Example:** walk through the sample data by hand.
- Active users only (users 1 to 10; users 11 and 12 and test user 13 excluded): total 106 events, mean 106/10 = 10.6. Sorted counts are 1, 1, 2, 2, 3, 4, 5, 8, 20, 60; the median is the average of the 5th and 6th, (3 + 4)/2 = 3.5. NTILE(10) over 10 rows gives one user per decile, so the top decile is user 10 with 60 events, 60/106 = 56.60 percent.
- All 12 non-test users (zero-event users 11 and 12 kept): same 106 events, mean 106/12 = 8.83, median is the average of the 6th and 7th of 0, 0, 1, 1, 2, 2, 3, 4, 5, 8, 20, 60, that is (2 + 3)/2 = 2.5. NTILE(10) over 12 rows makes the first two buckets hold two users each (12 = 10 x 1 + 2 extra), so the top decile is users 10 and 9 with 80 events, 80/106 = 75.47 percent.
- Decile boundary and ties: users 3 and 4 both have 2 events, yet user 3 is in decile 5 and user 4 in decile 6 because NTILE is positional and the `user_id` tie-breaker decides. Without a tie-breaker the split of tied users would be arbitrary and could change between runs.
- The mean (10.6) is three times the median (3.5): the two heaviest users make most of the volume.

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q28: engagement distribution: mean and median events per user, NTILE(10) power users, top decile share
import sqlite3
import pandas as pd

def build_events():
    # events per March user: u1 1, u2 1, u3 2, u4 2, u5 3, u6 4, u7 5, u8 8, u9 20, u10 60
    counts = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 4, 7: 5, 8: 8, 9: 20, 10: 60}
    rows, i = [], 0
    for u, n in counts.items():
        for k in range(n):
            i += 1
            rows.append((i, u, "2024-03-%02d 10:%02d:00" % (1 + (k % 28), k % 60), "click"))
    rows += [(1001, 1, "2024-02-28 10:00:00", "click"), (1002, 11, "2024-02-29 10:00:00", "click"),
             (1003, 2, "2024-04-01 10:00:00", "click"), (1004, 13, "2024-03-05 10:00:00", "click")]
    return rows

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-05','IN',0),(2,'2024-01-06','IN',0),(3,'2024-01-07','IN',0),(4,'2024-01-08','IN',0),
 (5,'2024-01-09','IN',0),(6,'2024-01-10','IN',0),(7,'2024-01-11','IN',0),(8,'2024-01-12','IN',0),
 (9,'2024-01-13','IN',0),(10,'2024-01-14','IN',0),(11,'2024-01-15','IN',0),(12,'2024-01-16','IN',0),
 (13,'2024-01-17','IN',1);
"""

# {BASE} is replaced: active users only (INNER JOIN) or all non-test registered users (LEFT JOIN, zeros kept)
SQL_TEMPLATE = """
WITH u AS (
  SELECT us.user_id, COUNT(e.event_id) AS n
  FROM users us
  {JOIN} events e ON e.user_id = us.user_id
       AND e.event_ts >= '2024-03-01' AND e.event_ts < '2024-04-01'
  WHERE us.is_test = 0
  GROUP BY us.user_id
), r AS (
  SELECT user_id, n,
         NTILE(10) OVER (ORDER BY n DESC, user_id) AS decile,
         ROW_NUMBER() OVER (ORDER BY n, user_id) AS rn,
         COUNT(*) OVER () AS cnt
  FROM u
), med AS (
  SELECT AVG(n) AS median FROM r WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
)
SELECT COUNT(*) AS users,
       SUM(n) AS events,
       ROUND(AVG(n), 2) AS mean_events,
       (SELECT median FROM med) AS median_events,
       SUM(decile = 1) AS top_decile_users,
       SUM(CASE WHEN decile = 1 THEN n END) AS top_decile_events,
       ROUND(SUM(CASE WHEN decile = 1 THEN n END) * 100.0 / SUM(n), 2) AS top_decile_share_pct
FROM r
"""
SQL_ACTIVE = SQL_TEMPLATE.replace("{JOIN}", "JOIN")
SQL_ALL = SQL_TEMPLATE.replace("{JOIN}", "LEFT JOIN")
SQL_DECILES = """
SELECT us.user_id, COUNT(e.event_id) AS n,
       NTILE(10) OVER (ORDER BY COUNT(e.event_id) DESC, us.user_id) AS decile
FROM users us LEFT JOIN events e ON e.user_id = us.user_id
     AND e.event_ts >= '2024-03-01' AND e.event_ts < '2024-04-01'
WHERE us.is_test = 0
GROUP BY us.user_id
ORDER BY decile, us.user_id
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
con.executemany("INSERT INTO events VALUES (?,?,?,?)", build_events())
print("integer division check, (12 + 1) / 2 and (12 + 2) / 2:", con.execute("SELECT (12+1)/2, (12+2)/2").fetchone())
a = pd.read_sql_query(SQL_ACTIVE, con)
b = pd.read_sql_query(SQL_ALL, con)
print("SQL, active users only (zero-event users excluded):")
print(a.to_string(index=False))
print("SQL, all non-test registered users (zero-event users kept):")
print(b.to_string(index=False))
dec = pd.read_sql_query(SQL_DECILES, con)
print("SQL, deciles over all non-test users (NTILE(10) over 12 rows):")
print(dec.to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)

# pd:main
def ntile(n_rows, k):
    # NTILE: the first (n_rows % k) buckets get one extra row; assigned by position
    base, extra = divmod(n_rows, k)
    out = []
    for i in range(n_rows):
        if i < extra * (base + 1):
            out.append(i // (base + 1) + 1)
        else:
            out.append(extra + (i - extra * (base + 1)) // base + 1)
    return out

def engagement(users, events, keep_zero):
    m = events[(events["event_ts"] >= "2024-03-01") & (events["event_ts"] < "2024-04-01")]
    cnt = m.groupby("user_id").size().rename("n")
    u = users.loc[users["is_test"] == 0, ["user_id"]].merge(cnt, on="user_id", how="left")
    u["n"] = u["n"].fillna(0).astype(int)
    if not keep_zero:
        u = u[u["n"] > 0]
    u = u.sort_values(["n", "user_id"], ascending=[False, True]).reset_index(drop=True)
    u["decile"] = ntile(len(u), 10) if len(u) >= 10 else range(1, len(u) + 1)
    top = u[u["decile"] == 1]
    return pd.DataFrame({"users": [len(u)], "events": [u["n"].sum()], "mean_events": [round(u["n"].mean(), 2)],
                         "median_events": [float(u["n"].median())], "top_decile_users": [len(top)],
                         "top_decile_events": [top["n"].sum()],
                         "top_decile_share_pct": [round(top["n"].sum() * 100.0 / u["n"].sum(), 2)]}), u
# pd:end

pd_a, _ = engagement(users, events, keep_zero=False)
pd_b, pu = engagement(users, events, keep_zero=True)
# one-row results, so no sort is needed
pd.testing.assert_frame_equal(pd_a, a, check_dtype=False)
pd.testing.assert_frame_equal(pd_b, b, check_dtype=False)
pd.testing.assert_frame_equal(pu[["user_id", "n", "decile"]].sort_values(["decile", "user_id"]).reset_index(drop=True),
                              dec, check_dtype=False)
print("pandas, keep_zero=True:")
print(pd_b.to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
integer division check, (12 + 1) / 2 and (12 + 2) / 2: (6, 7)
SQL, active users only (zero-event users excluded):
 users  events  mean_events  median_events  top_decile_users  top_decile_events  top_decile_share_pct
    10     106         10.6            3.5                 1                 60                  56.6
SQL, all non-test registered users (zero-event users kept):
 users  events  mean_events  median_events  top_decile_users  top_decile_events  top_decile_share_pct
    12     106         8.83            2.5                 2                 80                 75.47
SQL, deciles over all non-test users (NTILE(10) over 12 rows):
 user_id  n  decile
       9 20       1
      10 60       1
       7  5       2
       8  8       2
       6  4       3
       5  3       4
       3  2       5
       4  2       6
       1  1       7
       2  1       8
      11  0       9
      12  0      10
pandas, keep_zero=True:
 users  events  mean_events  median_events  top_decile_users  top_decile_events  top_decile_share_pct
    12     106         8.83            2.5                 2                 80                 75.47
asserts passed
```

**Edge cases:**
- Zero-event users: included or excluded changes users, mean, median, the decile sizes and the top share (all four printed). 'Events per active user' by definition excludes them.
- Even count: median averages two middle rows; odd count: both positions point at the same row, so the average is that row.
- Fewer than 10 users: NTILE(10) makes buckets of size 1 or 0 (the pandas helper falls back to `range(1, n+1)` in that case, matching NTILE for 10 or fewer rows).
- Ties at the decile boundary: add a deterministic tie-breaker and state that equal users can land in different deciles; alternatives are `PERCENT_RANK` or rank-based cuts that keep ties together (Part 4 Q36).
- Test users and the date range: the range uses `>= '2024-03-01' AND < '2024-04-01'`, so the whole of March 31 is included whatever the time part.

**Then explain:**
- Mean versus median: usage is skewed (a few heavy users), so the mean is pulled up and says little about a typical user. Report the median and a high percentile, or the share held by the top decile.
- NTILE(10) splits by position, not by value: with 12 rows two buckets get an extra row. Top decile is therefore 'the first 10 percent of users in rank order', not 'users above the 90th percentile value'.
- Power-user share: top-decile events over all events (56.6 percent active-only, 75.47 percent with zero users). This is a concentration measure; the Pareto version with revenue is in Part 4 Q49.
- Median without MEDIAN: `ROW_NUMBER() OVER (ORDER BY n)` and `COUNT(*) OVER ()`; SQLite integer division makes `(cnt + 1) / 2` the lower middle position (12 gives 6 and 7, confirmed in my run). PostgreSQL has `PERCENTILE_CONT(0.5)` and BigQuery `PERCENTILE_CONT` as a window function (not executed here).
- Population choice belongs in the definition: say 'active users in March, non-test'.

**Follow-ups:**
- Show the whole decile table? `SQL_DECILES` in the Code block prints every user's decile.
- Top 1 percent instead? Use `NTILE(100)`, but note small populations make that meaningless.
- Median events per user per day? Compute per user-day first, then the median; the grain changes.

**Common mistakes:**
- Reporting the mean as the typical user.
- NTILE without a tie-breaker, so tied users move between runs.
- Mixing populations: mean over active users and top-decile share over all registered users.
- Forgetting the test-user filter, or using `<= '2024-03-31'` on a timestamp and losing most of March 31.
- Using `qcut` as if it were NTILE (it cuts by value quantiles, can raise on duplicate edges unless told to drop them, and does not break ties by position).


### Q29 ⭐⭐ 🟡 Top products per category metrics: order_items(order_id, product_id, qty, unit_price), products(product_id, category, name) and orders(order_id, user_id, order_ts, status). Return for each category the top 2 products by completed revenue, with units, revenue, share of category revenue and rank (ties kept with DENSE_RANK; ranking mechanics are in Part 4). Compute revenue at line-item grain (qty times unit_price), not by joining an order total onto each item, and say how cancelled orders, a product without a category, and a category with fewer than two products are treated.
**Asked at:** e-commerce and marketplace metric lists: letsdatascience e-commerce SQL list (opened; repeat purchase rate, cart abandonment, top products by category, fan-out and grain pitfalls) and LearnSQL 'SQL metrics in real interviews' (opened; metric patterns breakdown, ratio, KPI, with joins that inflate results and division by zero as pitfalls; one author's own 11 interviews, no questions published); guides, not candidate reports; e-commerce, fintech and marketplace analyst rounds
**Say this first (1 line):** Compute revenue at line-item grain (`qty * unit_price`) from completed orders only, aggregate to product, add `SUM(revenue) OVER (PARTITION BY category)` for the share and `DENSE_RANK` within category, then keep rank 2 or better; with `DENSE_RANK` a tie at second place returns three products, which is the intended 'ties kept' behaviour.

**Schema and sample data:** eight products (product 7 has no category, product 8 is alone in its category), five orders (order 4 is cancelled) and thirteen line items. The last item references product 99, which is not in `products`. Electronics is built so that products 2 and 3 tie at 200.
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, status TEXT);
CREATE TABLE order_items(order_id INTEGER, product_id INTEGER, qty INTEGER, unit_price REAL);
INSERT INTO products VALUES
 (1,'Electronics','Phone'),(2,'Electronics','Case'),(3,'Electronics','Cable'),(4,'Electronics','Charger'),
 (5,'Books','Novel'),(6,'Books','Notebook'),(7,NULL,'Gift card'),(8,'Home','Lamp');
INSERT INTO orders VALUES
 (1,1,'2024-03-01','completed'),(2,2,'2024-03-02','completed'),(3,3,'2024-03-03','completed'),
 (4,4,'2024-03-04','cancelled'),(5,5,'2024-03-05','completed');
INSERT INTO order_items VALUES
 (1,1,1,500),(1,2,2,50),
 (2,1,1,500),(2,3,1,100),(2,5,3,20),
 (3,2,2,50),(3,4,1,50),(3,6,5,10),
 (4,4,10,50),
 (5,3,1,100),(5,7,1,30),(5,8,2,40),
 (5,99,1,10);
```

**SQL answer:** `SQL_MAIN` in the Code block (`SQL_WRONG` is the order-total-on-every-row version):
```sql
WITH p AS (
  SELECT COALESCE(pr.category, 'Uncategorised') AS category, pr.name,
         SUM(oi.qty) AS units, SUM(oi.qty * oi.unit_price) AS revenue
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
  JOIN products pr ON pr.product_id = oi.product_id
  GROUP BY COALESCE(pr.category, 'Uncategorised'), pr.product_id, pr.name
), r AS (
  SELECT category, name, units, revenue,
         ROUND(revenue * 100.0 / SUM(revenue) OVER (PARTITION BY category), 2) AS share_pct,
         DENSE_RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rnk
  FROM p
)
SELECT category, name, units, revenue, share_pct, rnk
FROM r
WHERE rnk <= 2
ORDER BY category, rnk, name
```

**pandas answer:** the same logic, identical to the Code block (`rank(method='dense', ascending=False)` is `DENSE_RANK`):
```py
def top_products(products, orders, items, n=2):
    d = (items.merge(orders.loc[orders["status"] == "completed", ["order_id"]], on="order_id")
              .merge(products, on="product_id"))
    d["category"] = d["category"].fillna("Uncategorised")
    d["revenue"] = d["qty"] * d["unit_price"]
    p = d.groupby(["category", "product_id", "name"], as_index=False).agg(units=("qty", "sum"),
                                                                           revenue=("revenue", "sum"))
    p["share_pct"] = (p["revenue"] * 100.0 / p.groupby("category")["revenue"].transform("sum")).round(2)
    p["rnk"] = p.groupby("category")["revenue"].rank(method="dense", ascending=False).astype(int)
    out = p[p["rnk"] <= n].sort_values(["category", "rnk", "name"]).reset_index(drop=True)
    return out[["category", "name", "units", "revenue", "share_pct", "rnk"]]
```

**Example:** walk through the sample data by hand.
- Completed line items only: order 4 (cancelled) is excluded, which removes 10 units of product 4 (500) and leaves the Charger at 50.
- Electronics: Phone 2 x 500 = 1000, Case 2 + 2 units x 50 = 200 (4 units), Cable 100 + 100 = 200 (2 units), Charger 50. Category total 1450. Dense ranks: Phone 1, Case and Cable 2 (tie), Charger 3. The top-2 filter keeps Phone, Cable and Case: three rows. Shares: 1000/1450 = 68.97, 200/1450 = 13.79 each.
- Books: Novel 3 x 20 = 60, Notebook 5 x 10 = 50, so ranks 1 and 2, shares 54.55 and 45.45.
- Product 7 (Gift card) has no category and goes to an explicit 'Uncategorised' group with share 100; Home has one product (Lamp, 80), so it returns one row, not two.
- The item for product 99 is dropped by the inner join to `products`.
- Wrong version: joining an order total onto every item row makes product revenue 880 for Cable (the whole order 2 and order 5 totals) instead of 200, and 1260 for Phone instead of 1000, because every product in the order is credited with the order's total.

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q29: top 2 products per category by completed revenue at line-item grain, DENSE_RANK keeps ties
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, status TEXT);
CREATE TABLE order_items(order_id INTEGER, product_id INTEGER, qty INTEGER, unit_price REAL);
INSERT INTO products VALUES
 (1,'Electronics','Phone'),(2,'Electronics','Case'),(3,'Electronics','Cable'),(4,'Electronics','Charger'),
 (5,'Books','Novel'),(6,'Books','Notebook'),(7,NULL,'Gift card'),(8,'Home','Lamp');
INSERT INTO orders VALUES
 (1,1,'2024-03-01','completed'),(2,2,'2024-03-02','completed'),(3,3,'2024-03-03','completed'),
 (4,4,'2024-03-04','cancelled'),(5,5,'2024-03-05','completed');
INSERT INTO order_items VALUES
 (1,1,1,500),(1,2,2,50),
 (2,1,1,500),(2,3,1,100),(2,5,3,20),
 (3,2,2,50),(3,4,1,50),(3,6,5,10),
 (4,4,10,50),
 (5,3,1,100),(5,7,1,30),(5,8,2,40),
 (5,99,1,10);
"""

SQL_MAIN = """
WITH p AS (
  SELECT COALESCE(pr.category, 'Uncategorised') AS category, pr.name,
         SUM(oi.qty) AS units, SUM(oi.qty * oi.unit_price) AS revenue
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
  JOIN products pr ON pr.product_id = oi.product_id
  GROUP BY COALESCE(pr.category, 'Uncategorised'), pr.product_id, pr.name
), r AS (
  SELECT category, name, units, revenue,
         ROUND(revenue * 100.0 / SUM(revenue) OVER (PARTITION BY category), 2) AS share_pct,
         DENSE_RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rnk
  FROM p
)
SELECT category, name, units, revenue, share_pct, rnk
FROM r
WHERE rnk <= 2
ORDER BY category, rnk, name
"""
# wrong: an order total joined onto every item row
SQL_WRONG = """
WITH ot AS (SELECT order_id, SUM(qty * unit_price) AS order_total FROM order_items GROUP BY order_id)
SELECT pr.name, SUM(ot.order_total) AS wrong_revenue, SUM(oi.qty * oi.unit_price) AS line_revenue
FROM order_items oi
JOIN ot ON ot.order_id = oi.order_id
JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
JOIN products pr ON pr.product_id = oi.product_id
WHERE pr.category = 'Electronics'
GROUP BY pr.product_id, pr.name ORDER BY pr.name
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
print("SQL:")
print(sql_main.to_string(index=False))
print("SQL wrong (order total on every item row), Electronics:")
print(pd.read_sql_query(SQL_WRONG, con).to_string(index=False))

products = pd.read_sql_query("SELECT * FROM products", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
items = pd.read_sql_query("SELECT * FROM order_items", con)

# pd:main
def top_products(products, orders, items, n=2):
    d = (items.merge(orders.loc[orders["status"] == "completed", ["order_id"]], on="order_id")
              .merge(products, on="product_id"))
    d["category"] = d["category"].fillna("Uncategorised")
    d["revenue"] = d["qty"] * d["unit_price"]
    p = d.groupby(["category", "product_id", "name"], as_index=False).agg(units=("qty", "sum"),
                                                                           revenue=("revenue", "sum"))
    p["share_pct"] = (p["revenue"] * 100.0 / p.groupby("category")["revenue"].transform("sum")).round(2)
    p["rnk"] = p.groupby("category")["revenue"].rank(method="dense", ascending=False).astype(int)
    out = p[p["rnk"] <= n].sort_values(["category", "rnk", "name"]).reset_index(drop=True)
    return out[["category", "name", "units", "revenue", "share_pct", "rnk"]]
# pd:end

pd_res = top_products(products, orders, items)
# compare after sorting by category, rnk, name (the SQL ORDER BY)
pd.testing.assert_frame_equal(pd_res, sql_main, check_dtype=False)
print("pandas rows:", len(pd_res), "; SQL rows:", len(sql_main))
print("asserts passed")
```

**Output (my run):**
```text
SQL:
     category      name  units  revenue  share_pct  rnk
        Books     Novel      3     60.0      54.55    1
        Books  Notebook      5     50.0      45.45    2
  Electronics     Phone      2   1000.0      68.97    1
  Electronics     Cable      2    200.0      13.79    2
  Electronics      Case      4    200.0      13.79    2
         Home      Lamp      2     80.0     100.00    1
Uncategorised Gift card      1     30.0     100.00    1
SQL wrong (order total on every item row), Electronics:
   name  wrong_revenue  line_revenue
  Cable          880.0         200.0
   Case          800.0         200.0
Charger          200.0          50.0
  Phone         1260.0        1000.0
pandas rows: 7 ; SQL rows: 7
asserts passed
```

**Edge cases:**
- Cancelled orders: excluded here (status filter). Returned or partially refunded lines would need a refunds table; not in this question.
- NULL category: `COALESCE(category, 'Uncategorised')` makes it a group; leaving it NULL would still group it (GROUP BY and window PARTITION BY treat NULLs as one group) but print NULL.
- Category with fewer than two products: returns what it has (Home: one row). No padding.
- Ties: `DENSE_RANK` keeps all tied products, so the result can exceed 2 rows per category; `ROW_NUMBER` would pick one arbitrarily unless a tie-breaker is added (Part 4 Q2 and Q12).
- Products with no completed sales are absent (inner join on items); to list them with 0, start from `products` and LEFT JOIN.
- Share uses the category total before the top-2 filter, so shares of the shown rows need not add to 100.

**Then explain:**
- Grain: revenue belongs to the order line, so multiply and sum at that grain. An order-level total joined to lines is repeated once per line.
- Window functions run after GROUP BY, so aggregate to product first, then rank and take shares in the same query (ranking aggregates is Part 4 Q13).
- The rank filter has to be in an outer query or CTE because window results cannot be used in WHERE.
- Units and revenue come from the same filtered rows; do not mix completed-only revenue with all-status units.
- Dialect: Snowflake and BigQuery have `QUALIFY` to filter on the rank directly (not executed here).

**Follow-ups:**
- Top 2 per category with exactly two rows? Use `ROW_NUMBER` with a tie-breaker (`name`), and say which product is dropped.
- Net of discounts? Needs a discount column; subtract at line level.
- Share of total company revenue as well? Add a second window `SUM(revenue) OVER ()`.

**Common mistakes:**
- Joining an order total (or order amount) to each item and summing it.
- Including cancelled orders in revenue or units.
- Using `RANK` and then filtering `<= 2`, which behaves like `DENSE_RANK` only until a tie occurs before the cut (a tie at rank 1 skips rank 2).
- Dropping uncategorised products silently through an inner join on a category table.
- Taking share after the top-2 filter, so shares add to 100 by accident.


### Q30 ⭐⭐ 🟡 pandas pivot_table and crosstab for conversion by channel: orders DataFrame with columns user_id, order_id, channel (some NaN) and status, and a users DataFrame with signup channel. Produce (a) counts of orders by channel and status with pivot_table and fill_value, (b) row-normalised shares with pd.crosstab(..., normalize='index'), (c) value_counts(normalize=True) for the channel mix and say how dropna changes each of them (pivot_table and crosstab drop NaN keys by default, value_counts drops NaN unless dropna=False). Assert the shares equal a SQL GROUP BY result from sqlite3 on the same data and say which one silently loses the NaN-channel rows.
**Asked at:** pandas reference pages for pivot_table and crosstab (both opened: pivot_table dropna=True drops NaN keys and all-NaN columns, observed default True in 3.0.0; crosstab normalize accepts all/index/columns and dropna drops empty categories) plus expert gap-check on groupby, nunique and rounding behaviour; documentation, not candidate reports; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `pivot_table` and `pd.crosstab` both drop NaN keys by default and `value_counts` drops NaN unless `dropna=False`, so a NaN channel silently disappears from all three; a SQL `GROUP BY` keeps a NULL group, which is why I fill the key (`'unknown'`) first and then assert the pandas shares equal the SQL result.

**Schema and sample data:** ten orders for five users. Three orders have a NULL channel (orders 6, 7, 8). `users.signup_channel` is complete and is used for a fallback rule at the end. Everything here is made-up toy data.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_channel TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, channel TEXT, status TEXT);
INSERT INTO users VALUES (1,'ads'),(2,'organic'),(3,'referral'),(4,'ads'),(5,'organic');
INSERT INTO orders VALUES
 (1,1,'ads','completed'),(2,1,'ads','cancelled'),(3,2,'organic','completed'),
 (4,2,'organic','completed'),(5,3,'referral','cancelled'),(6,4,NULL,'completed'),
 (7,4,NULL,'cancelled'),(8,5,NULL,'completed'),(9,3,'referral','completed'),
 (10,1,'ads','completed');
```

**SQL answer:** `SQL_COUNTS` in the Code block (NULL channel shown as 'unknown' with `COALESCE`, which turns the NULL group into a labelled row):
```sql
SELECT COALESCE(channel, 'unknown') AS channel,
       SUM(status = 'cancelled') AS cancelled,
       SUM(status = 'completed') AS completed,
       COUNT(*) AS orders,
       ROUND(SUM(status = 'completed') * 1.0 / COUNT(*), 4) AS completed_share,
       ROUND(COUNT(*) * 1.0 / (SELECT COUNT(*) FROM orders), 4) AS channel_mix
FROM orders
GROUP BY COALESCE(channel, 'unknown')
ORDER BY channel
```

**pandas answer:** there is no single function here; the pandas steps are printed in the Code block. The core calls are `pd.pivot_table(orders, index="channel", columns="status", values="order_id", aggfunc="count", fill_value=0)` for counts, `pd.crosstab(orders["channel_f"], orders["status"], normalize="index")` for row shares and `orders["channel"].value_counts(normalize=True, dropna=False)` for the mix, where `channel_f` is `channel.fillna("unknown")`.

**Example:** walk through the sample data by hand.
- SQL on the ten orders: ads 3 orders (2 completed, 1 cancelled), organic 2 (both completed), referral 2 (1 and 1), NULL 3 (2 completed, 1 cancelled). Completed share is 0.6667, 1.0, 0.5 and 0.6667; channel mix is 0.3, 0.2, 0.2, 0.3.
- pandas `pivot_table` default: the NaN-channel rows are gone, 7 of 10 rows are counted and there is no 'unknown' row.
- `crosstab(..., normalize='index')` default: the same three rows only; normalising by `'all'` makes the shares add to 1.0 but over the 7 kept rows, not over 10.
- `value_counts(normalize=True)` default gives ads 0.4286, organic 0.2857, referral 0.2857: shares of 7, so ads looks like 43 percent of orders instead of 30 percent. With `dropna=False` the NaN row appears with 0.3 and every share matches SQL.
- After `fillna('unknown')` the pivot, the crosstab and the mix all match SQL, which the Code block asserts (compared after sorting by channel).
- Fallback rule: filling the NaN order channel from the user's signup channel (merge, then `fillna`) leaves no NaN: ads 5, organic 3, referral 2. That is a different, defined attribution rule, not the same as 'unknown'.

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q30: pandas pivot_table, crosstab and value_counts with a NaN channel, checked against SQL GROUP BY
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_channel TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, channel TEXT, status TEXT);
INSERT INTO users VALUES (1,'ads'),(2,'organic'),(3,'referral'),(4,'ads'),(5,'organic');
INSERT INTO orders VALUES
 (1,1,'ads','completed'),(2,1,'ads','cancelled'),(3,2,'organic','completed'),
 (4,2,'organic','completed'),(5,3,'referral','cancelled'),(6,4,NULL,'completed'),
 (7,4,NULL,'cancelled'),(8,5,NULL,'completed'),(9,3,'referral','completed'),
 (10,1,'ads','completed');
"""

SQL_COUNTS = """
SELECT COALESCE(channel, 'unknown') AS channel,
       SUM(status = 'cancelled') AS cancelled,
       SUM(status = 'completed') AS completed,
       COUNT(*) AS orders,
       ROUND(SUM(status = 'completed') * 1.0 / COUNT(*), 4) AS completed_share,
       ROUND(COUNT(*) * 1.0 / (SELECT COUNT(*) FROM orders), 4) AS channel_mix
FROM orders
GROUP BY COALESCE(channel, 'unknown')
ORDER BY channel
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_res = pd.read_sql_query(SQL_COUNTS, con)
print("SQL GROUP BY (NULL channel kept as 'unknown'):")
print(sql_res.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
users = pd.read_sql_query("SELECT * FROM users", con)
print("channel dtype:", orders["channel"].dtype, "; NaN rows:", int(orders["channel"].isna().sum()))

# (a) counts: default drops NaN keys
pv = pd.pivot_table(orders, index="channel", columns="status", values="order_id",
                    aggfunc="count", fill_value=0)
print("(a) pivot_table, default dropna=True:")
print(pv)
print("    rows kept:", int(pv.to_numpy().sum()), "of", len(orders))
# the aggfunc='mean' default trap
trap = pd.pivot_table(orders, index="channel", columns="status", values="order_id")
print("(a') pivot_table with the default aggfunc='mean' on order_id (not a count):")
print(trap)
# explicit NaN bucket
orders["channel_f"] = orders["channel"].fillna("unknown")
pv_f = pd.pivot_table(orders, index="channel_f", columns="status", values="order_id",
                      aggfunc="count", fill_value=0)
print("(a'') pivot_table after fillna('unknown'):")
print(pv_f)

# (b) crosstab row shares
ct = pd.crosstab(orders["channel"], orders["status"], normalize="index")
ct_f = pd.crosstab(orders["channel_f"], orders["status"], normalize="index")
print("(b) crosstab normalize='index', NaN channel silently absent:")
print(ct.round(4))
print("(b') crosstab after fillna('unknown'):")
print(ct_f.round(4))
ct_all = pd.crosstab(orders["channel"], orders["status"], normalize="all")
print("(b'') crosstab normalize='all' sums to", round(float(ct_all.to_numpy().sum()), 4),
      "(shares of the 7 kept rows, not of 10)")

# (c) value_counts
vc = orders["channel"].value_counts(normalize=True)
vc_na = orders["channel"].value_counts(normalize=True, dropna=False)
print("(c) value_counts(normalize=True):")
print(vc.round(4).to_string())
print("(c') value_counts(normalize=True, dropna=False):")
print(vc_na.round(4).to_string())

# assertions against SQL
pd_res = pd.DataFrame({"channel": pv_f.index, "cancelled": pv_f["cancelled"].to_numpy(),
                       "completed": pv_f["completed"].to_numpy()})
pd_res["orders"] = pd_res["cancelled"] + pd_res["completed"]
pd_res["completed_share"] = ct_f.loc[pd_res["channel"], "completed"].round(4).to_numpy()
mix = orders["channel_f"].value_counts(normalize=True, dropna=False)
pd_res["channel_mix"] = mix.loc[pd_res["channel"]].round(4).to_numpy()
# compare after sorting by channel (SQL ORDER BY channel)
pd.testing.assert_frame_equal(pd_res.sort_values("channel").reset_index(drop=True), sql_res, check_dtype=False)

# crosstab or pivot on a categorical key: observed / dropna defaults
cat = orders.assign(channel_c=pd.Categorical(orders["channel_f"],
                    categories=["ads", "organic", "referral", "unknown", "affiliate"]))
print("categorical key with an unused category 'affiliate':")
print("  pivot_table default rows:", list(pd.pivot_table(cat, index="channel_c", columns="status",
      values="order_id", aggfunc="count", fill_value=0).index))
print("  pivot_table observed=False rows:", list(pd.pivot_table(cat, index="channel_c", columns="status",
      values="order_id", aggfunc="count", fill_value=0, observed=False).index))
print("  crosstab default rows:", list(pd.crosstab(cat["channel_c"], cat["status"]).index))
print("  crosstab dropna=False rows:", list(pd.crosstab(cat["channel_c"], cat["status"], dropna=False).index))

# fallback to the signup channel through a merge
m = orders.merge(users, on="user_id", how="left")
m["channel_fb"] = m["channel"].fillna(m["signup_channel"])
print("after fallback to signup channel, NaN left:", int(m["channel_fb"].isna().sum()))
print(m["channel_fb"].value_counts().to_string())
print("asserts passed")
```

**Output (my run):**
```text
SQL GROUP BY (NULL channel kept as 'unknown'):
 channel  cancelled  completed  orders  completed_share  channel_mix
     ads          1          2       3           0.6667          0.3
 organic          0          2       2           1.0000          0.2
referral          1          1       2           0.5000          0.2
 unknown          1          2       3           0.6667          0.3
channel dtype: str ; NaN rows: 3
(a) pivot_table, default dropna=True:
status    cancelled  completed
channel                       
ads               1          2
organic           0          2
referral          1          1
    rows kept: 7 of 10
(a') pivot_table with the default aggfunc='mean' on order_id (not a count):
status    cancelled  completed
channel                       
ads             2.0        5.5
organic         NaN        3.5
referral        5.0        9.0
(a'') pivot_table after fillna('unknown'):
status     cancelled  completed
channel_f                      
ads                1          2
organic            0          2
referral           1          1
unknown            1          2
(b) crosstab normalize='index', NaN channel silently absent:
status    cancelled  completed
channel                       
ads          0.3333     0.6667
organic      0.0000     1.0000
referral     0.5000     0.5000
(b') crosstab after fillna('unknown'):
status     cancelled  completed
channel_f                      
ads           0.3333     0.6667
organic       0.0000     1.0000
referral      0.5000     0.5000
unknown       0.3333     0.6667
(b'') crosstab normalize='all' sums to 1.0 (shares of the 7 kept rows, not of 10)
(c) value_counts(normalize=True):
channel
ads         0.4286
organic     0.2857
referral    0.2857
(c') value_counts(normalize=True, dropna=False):
channel
ads         0.3
NaN         0.3
organic     0.2
referral    0.2
categorical key with an unused category 'affiliate':
  pivot_table default rows: ['ads', 'organic', 'referral', 'unknown']
  pivot_table observed=False rows: ['ads', 'organic', 'referral', 'unknown', 'affiliate']
  crosstab default rows: ['ads', 'organic', 'referral', 'unknown']
  crosstab dropna=False rows: ['ads', 'organic', 'referral', 'unknown', 'affiliate']
after fallback to signup channel, NaN left: 0
channel_fb
ads         5
organic     3
referral    2
asserts passed
```

**Edge cases:**
- Default aggfunc: `pivot_table` defaults to `aggfunc='mean'`. On `order_id` it printed means such as 5.5, not counts, and an NaN cell for organic cancelled; always pass `aggfunc='count'` (non-null values) or `'size'`.
- `aggfunc='count'` counts non-null values of `values`; if the values column has NaN the counts are short. Use a never-null column such as the order id.
- Unused categories: with a categorical channel that has an unused category 'affiliate', `pivot_table` omitted it (the `observed=True` default in pandas 3.0, as run here) and `observed=False` showed it; `crosstab` omitted it by default and `dropna=False` showed it. Whether this matches older pandas versions I did not test.
- `fill_value=0` fills empty cells (organic, cancelled) but does not recreate NaN-key rows.
- Dtype: with pandas 3.0 the channel column is the string dtype and missing values are NaN; the behaviours above were run on 3.0.5.

**Then explain:**
- Which one silently loses the NaN-channel rows: all three pandas calls by default (`pivot_table`, `crosstab`, `value_counts`); SQL `GROUP BY` does not, it returns the NULL group, so SQL and pandas disagree by 3 of 10 rows until you fill or set `dropna=False`.
- `crosstab(normalize='index')` rows add to 1 over the kept rows; the dropped rows silently change the denominators of `'all'` and `'columns'` normalisation, but not of `'index'` for the channels kept.
- `value_counts(normalize=True)` divides by the non-null count by default, so shares change when NaN is dropped. This is the one that changes the mix, not only the table.
- Counts versus mean: forgetting `aggfunc` gives averages of an id column and looks like a table of numbers.
- Safer habit: make missing an explicit value (`fillna('unknown')`) before any pivot, or pass `dropna=False` where the function supports it, and assert row totals equal `len(orders)`.

**Follow-ups:**
- Does `groupby` behave the same? It also drops NaN keys unless `dropna=False` (Q31 runs it).
- How do you add row and column totals? `margins=True` on both functions; check the margin label does not clash with a real category.
- Same table in SQL with columns per status? `SUM(status = 'completed')` conditional aggregation, as in `SQL_COUNTS`; SQLite has no PIVOT.

**Common mistakes:**
- Relying on the default `aggfunc='mean'`.
- Not noticing that NaN-key rows vanished (7 of 10).
- Comparing pandas shares to SQL shares computed over a different row set.
- Using `normalize=True` on `crosstab` and reading it as row shares (it is `'all'`).
- Filling with 0 instead of a label, which merges unknown orders with a real channel called 0.


### Q31 ⭐⭐ 🟡 SQL versus pandas differences in metric code, a translation table with each row demonstrated on tiny data: nunique skips NaN while COUNT(DISTINCT) skips NULL (same) but len(set()) does not, groupby drops NaN keys while SQL GROUP BY keeps a NULL group, integer division (SQLite 3 / 2 gives 1; pandas / gives 1.5), rounding (SQLite ROUND half away from zero; Python round and numpy round half to even), division by an empty denominator (NULL or error in SQL; NaN or inf in pandas), and merge on keys with NaN. Say which rows were run.
**Asked at:** pandas reference pages for pivot_table and crosstab (both opened: pivot_table dropna=True drops NaN keys and all-NaN columns, observed default True in 3.0.0; crosstab normalize accepts all/index/columns and dropna drops empty categories) plus expert gap-check on groupby, nunique and rounding behaviour; documentation, not candidate reports; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** Most differences are NULL versus NaN handling and number types: `nunique` and `COUNT(DISTINCT)` skip missing values but `len(set(series))` does not, `groupby` drops NaN keys while `GROUP BY` keeps a NULL group, SQLite `3/2` is 1 while pandas gives 1.5, SQLite rounds halves away from zero while Python and numpy round halves to even (and numpy and Python can still disagree), SQLite returns NULL for division by zero while pandas gives inf or NaN, and pandas `merge` matches NaN keys to each other while SQL joins never match NULLs. I ran every row below.

**Schema and sample data:** a five-row table `t(id, k, u, v)` with a NULL in each of `k`, `u` and `v` (k is a, a, NULL, NULL, b; u is 10, NULL, 10, NULL, 20), and two two-row tables `l` and `r` that each have a NULL key. There is no single query and pandas function pair here; every row is a small printed demonstration, so the SQL and pandas answers are the statements in the Code block.
```sql
CREATE TABLE t(id INTEGER, k TEXT, u INTEGER, v REAL);
INSERT INTO t VALUES (1,'a',10,1.0),(2,'a',NULL,2.0),(3,NULL,10,3.0),(4,NULL,NULL,NULL),(5,'b',20,4.0);
CREATE TABLE l(k TEXT, lv INTEGER);
CREATE TABLE r(k TEXT, rv INTEGER);
INSERT INTO l VALUES ('a',1),(NULL,2);
INSERT INTO r VALUES ('a',10),(NULL,20);
```

**SQL answer:** the statements are in the Code block (for example `SELECT COUNT(DISTINCT u) FROM t`, `SELECT 3/2`, `SELECT ROUND(2.5)`, `SELECT 1/0`, `SELECT l.k, lv, rv FROM l JOIN r ON l.k = r.k`).

**pandas answer:** the pandas calls are in the Code block (`df['u'].nunique()`, `df.groupby('k')`, `pd.Series([3]) / 2`, `pd.Series(vals).round()`, `L.merge(R, on='k')`).

**Example:** walk through the sample data by hand.
Translation table, every cell from my run (SQLite 3.45.1, pandas 3.0.5, numpy 2.5.3):

| Topic | SQL (SQLite) | pandas / Python |
|---|---|---|
| Distinct count of u (10, NULL, 10, NULL, 20) | `COUNT(DISTINCT u)` = 2; `COUNT(u)` = 3; `COUNT(*)` = 5 | `nunique()` = 2; `nunique(dropna=False)` = 3; `len(set(series))` = 4 (each NaN is a separate object); `len(unique())` = 3 |
| Group on k (a, a, NULL, NULL, b) | `GROUP BY k` returns three groups: NULL 2, a 2, b 1 | `groupby('k')` gives a 2, b 1 (NaN group dropped); `dropna=False` adds NaN 2; `value_counts()` drops NaN, `dropna=False` keeps it |
| Integer division | `3/2` = 1, `-3/2` = -1 (truncates toward zero), `3/2.0` = 1.5 | `3/2` = 1.5; `3//2` = 1; `-3//2` = -2 (floors); `int(-3/2)` = -1; Series `/` and `//` match Python |
| Rounding halves | `ROUND(0.5)`, `ROUND(2.5)`, `ROUND(-2.5)` = 1.0, 3.0, -3.0 | Python `round(2.5)` = 2, `round(0.5)` = 0, `round(-2.5)` = -2; numpy and `Series.round()` the same (half to even) |
| Rounding to 2 places | `ROUND(0.125, 2)` = 0.13, `ROUND(2.675, 2)` = 2.67, `ROUND(1.005, 2)` = 1.0 | Python 0.12, 2.67, 1.0; numpy and `Series.round(2)` 0.12, **2.68**, 1.0 |
| Division by zero | `1/0`, `1.0/0`, `0.0/0` all NULL; `1/NULLIF(0,0)` NULL; `SUM` and `AVG` of no rows NULL, `COUNT` 0 | Python `1/0` raises `ZeroDivisionError`; float Series gives inf (1/0) and NaN (0/0); empty `sum()` = 0.0, `mean()` = NaN |
| Join or merge on a NULL key | `INNER JOIN` returns only the 'a' row; `LEFT JOIN` keeps the NULL row with no match; `NULL = NULL` is NULL | `merge(on='k')` **matches NaN to NaN**: the inner merge returned the NaN row with rv 20 |
| Rolling distinct | no window `COUNT(DISTINCT ...)` in SQLite (range join, Q33) | `Series.rolling(n).nunique` exists in pandas 3.0.5 (docstring says added in 3.0.0), see Q33 |

What the run showed that I did not expect:
- `len(set(series))` is 4 and not 3: a float column with two NaN values gives two separate NaN objects, and a Python set treats each NaN as different from every other. `nunique()` and `unique()` handle this properly.
- `ROUND(2.675, 2)` agrees with Python's 2.67 but numpy and pandas give 2.68, so numpy is not the same as Python's `round` either. Neither is 'wrong'; they scale and round differently on binary floats.
- `rolling().nunique` is available in pandas 3.0.5, which contradicts the Wave A premise of its absence (checked here by `hasattr` and by a real call in Q33).

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q31: SQL versus pandas differences in metric code, each row run on tiny data
import sqlite3
import warnings
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE t(id INTEGER, k TEXT, u INTEGER, v REAL);
INSERT INTO t VALUES (1,'a',10,1.0),(2,'a',NULL,2.0),(3,NULL,10,3.0),(4,NULL,NULL,NULL),(5,'b',20,4.0);
CREATE TABLE l(k TEXT, lv INTEGER);
CREATE TABLE r(k TEXT, rv INTEGER);
INSERT INTO l VALUES ('a',1),(NULL,2);
INSERT INTO r VALUES ('a',10),(NULL,20);
""")
df = pd.read_sql_query("SELECT * FROM t", con)
print("sqlite", sqlite3.sqlite_version, "pandas", pd.__version__, "numpy", np.__version__)

def q(sql):
    return con.execute(sql).fetchall()

print("\nRow 1: distinct count with a missing user id (column u: 10, NULL, 10, NULL, 20)")
print("  SQL COUNT(DISTINCT u):", q("SELECT COUNT(DISTINCT u) FROM t")[0][0],
      "| SQL COUNT(*):", q("SELECT COUNT(*) FROM t")[0][0],
      "| SQL COUNT(u):", q("SELECT COUNT(u) FROM t")[0][0])
print("  pandas nunique():", df["u"].nunique(), "| nunique(dropna=False):", df["u"].nunique(dropna=False),
      "| len(set(series)):", len(set(df["u"])), "| len(df['u'].unique()):", len(df["u"].unique()))
print("  SQL DISTINCT rows incl NULL group:", len(q("SELECT DISTINCT u FROM t")))

print("\nRow 2: grouping on a key with a missing value (k: a, a, NULL, NULL, b)")
print("  SQL GROUP BY k:", q("SELECT k, COUNT(*) FROM t GROUP BY k ORDER BY k"))
print("  pandas groupby default:", df.groupby("k").size().to_dict())
print("  pandas groupby dropna=False:", df.groupby("k", dropna=False).size().to_dict())
print("  value_counts default:", df["k"].value_counts().to_dict(), "| dropna=False:",
      df["k"].value_counts(dropna=False).to_dict())

print("\nRow 3: integer division and sign")
print("  SQLite 3 / 2 =", q("SELECT 3/2")[0][0], "| 3 / 2.0 =", q("SELECT 3/2.0")[0][0],
      "| -3 / 2 =", q("SELECT -3/2")[0][0], "| 3 * 1.0 / 2 =", q("SELECT 3*1.0/2")[0][0])
print("  Python 3 / 2 =", 3 / 2, "| 3 // 2 =", 3 // 2, "| -3 // 2 =", -3 // 2, "| int(-3 / 2) =", int(-3 / 2))
print("  pandas Series([3]) / 2 =", float((pd.Series([3]) / 2).iloc[0]), "| // 2 =", int((pd.Series([3]) // 2).iloc[0]),
      "| Series([-3]) // 2 =", int((pd.Series([-3]) // 2).iloc[0]))

print("\nRow 4: rounding (SQLite ROUND versus Python round, numpy and pandas)")
vals = [0.5, 1.5, 2.5, -2.5]
print("  SQLite ROUND(x):", [q(f"SELECT ROUND({x})")[0][0] for x in vals])
print("  Python round(x):", [round(x) for x in vals])
print("  numpy np.round(x):", [float(np.round(x)) for x in vals])
print("  pandas Series.round():", pd.Series(vals).round().tolist())
two = [0.125, 0.375, 2.675, 1.005]
print("  to 2 places:", two)
print("  SQLite ROUND(x, 2):", [q(f"SELECT ROUND({x}, 2)")[0][0] for x in two])
print("  Python round(x, 2):", [round(x, 2) for x in two])
print("  numpy np.round(x, 2):", [float(np.round(x, 2)) for x in two])
print("  pandas Series.round(2):", pd.Series(two).round(2).tolist())

print("\nRow 5: division by an empty or zero denominator")
print("  SQLite 1 / 0 =", q("SELECT 1/0")[0][0], "| 1.0 / 0 =", q("SELECT 1.0/0")[0][0],
      "| 0.0 / 0 =", q("SELECT 0.0/0")[0][0], "| 1 / NULLIF(0, 0) =", q("SELECT 1/NULLIF(0,0)")[0][0])
print("  SQLite SUM over zero rows:", q("SELECT SUM(v) FROM t WHERE id > 99")[0][0],
      "| COUNT over zero rows:", q("SELECT COUNT(*) FROM t WHERE id > 99")[0][0],
      "| AVG over zero rows:", q("SELECT AVG(v) FROM t WHERE id > 99")[0][0])
s = pd.Series([1.0, 0.0, 5.0]); z = pd.Series([0.0, 0.0, 5.0])
print("  pandas float Series 1/0, 0/0, 5/5:", (s / z).tolist())
print("  pandas int Series [1, 0] / [0, 0]:", (pd.Series([1, 0]) / pd.Series([0, 0])).tolist())
try:
    1 / 0
except ZeroDivisionError as e:
    print("  Python 1 / 0 raises ZeroDivisionError:", e)
empty = df[df["id"] > 99]
print("  pandas sum of empty:", empty["v"].sum(), "| mean of empty:", empty["v"].mean(), "| count:", int(empty["v"].count()))

print("\nRow 6: merge / join on keys that contain a missing value")
print("  SQL INNER JOIN on k:", q("SELECT l.k, lv, rv FROM l JOIN r ON l.k = r.k"))
print("  SQL LEFT JOIN on k:", q("SELECT l.k, lv, rv FROM l LEFT JOIN r ON l.k = r.k ORDER BY lv"))
L = pd.read_sql_query("SELECT * FROM l", con); R = pd.read_sql_query("SELECT * FROM r", con)
print("  pandas merge inner on k:")
print(L.merge(R, on="k").to_string(index=False))
print("  SQL NULL = NULL:", q("SELECT NULL = NULL")[0][0], "| NULL IS NULL:", q("SELECT NULL IS NULL")[0][0])

print("\nRow 7: rolling().nunique")
print("  hasattr(Series.rolling(2), 'nunique'):", hasattr(pd.Series([1, 2]).rolling(2), "nunique"))
print("  hasattr(Series.rolling(2), 'count'):", hasattr(pd.Series([1, 2]).rolling(2), "count"))

# assertions behind the table
assert q("SELECT COUNT(DISTINCT u) FROM t")[0][0] == df["u"].nunique() == 2
assert q("SELECT 3/2")[0][0] == 1 and 3 / 2 == 1.5
assert q("SELECT ROUND(2.5)")[0][0] == 3.0 and round(2.5) == 2
print("\nasserts passed")
```

**Output (my run):**
```text
sqlite 3.45.1 pandas 3.0.5 numpy 2.5.3

Row 1: distinct count with a missing user id (column u: 10, NULL, 10, NULL, 20)
  SQL COUNT(DISTINCT u): 2 | SQL COUNT(*): 5 | SQL COUNT(u): 3
  pandas nunique(): 2 | nunique(dropna=False): 3 | len(set(series)): 4 | len(df['u'].unique()): 3
  SQL DISTINCT rows incl NULL group: 3

Row 2: grouping on a key with a missing value (k: a, a, NULL, NULL, b)
  SQL GROUP BY k: [(None, 2), ('a', 2), ('b', 1)]
  pandas groupby default: {'a': 2, 'b': 1}
  pandas groupby dropna=False: {'a': 2, 'b': 1, nan: 2}
  value_counts default: {'a': 2, 'b': 1} | dropna=False: {'a': 2, nan: 2, 'b': 1}

Row 3: integer division and sign
  SQLite 3 / 2 = 1 | 3 / 2.0 = 1.5 | -3 / 2 = -1 | 3 * 1.0 / 2 = 1.5
  Python 3 / 2 = 1.5 | 3 // 2 = 1 | -3 // 2 = -2 | int(-3 / 2) = -1
  pandas Series([3]) / 2 = 1.5 | // 2 = 1 | Series([-3]) // 2 = -2

Row 4: rounding (SQLite ROUND versus Python round, numpy and pandas)
  SQLite ROUND(x): [1.0, 2.0, 3.0, -3.0]
  Python round(x): [0, 2, 2, -2]
  numpy np.round(x): [0.0, 2.0, 2.0, -2.0]
  pandas Series.round(): [0.0, 2.0, 2.0, -2.0]
  to 2 places: [0.125, 0.375, 2.675, 1.005]
  SQLite ROUND(x, 2): [0.13, 0.38, 2.67, 1.0]
  Python round(x, 2): [0.12, 0.38, 2.67, 1.0]
  numpy np.round(x, 2): [0.12, 0.38, 2.68, 1.0]
  pandas Series.round(2): [0.12, 0.38, 2.68, 1.0]

Row 5: division by an empty or zero denominator
  SQLite 1 / 0 = None | 1.0 / 0 = None | 0.0 / 0 = None | 1 / NULLIF(0, 0) = None
  SQLite SUM over zero rows: None | COUNT over zero rows: 0 | AVG over zero rows: None
  pandas float Series 1/0, 0/0, 5/5: [inf, nan, 1.0]
  pandas int Series [1, 0] / [0, 0]: [inf, nan]
  Python 1 / 0 raises ZeroDivisionError: division by zero
  pandas sum of empty: 0.0 | mean of empty: nan | count: 0

Row 6: merge / join on keys that contain a missing value
  SQL INNER JOIN on k: [('a', 1, 10)]
  SQL LEFT JOIN on k: [('a', 1, 10), (None, 2, None)]
  pandas merge inner on k:
  k  lv  rv
  a   1  10
NaN   2  20
  SQL NULL = NULL: None | NULL IS NULL: 1

Row 7: rolling().nunique
  hasattr(Series.rolling(2), 'nunique'): True
  hasattr(Series.rolling(2), 'count'): True

asserts passed
```

**Edge cases:**
- `COUNT(DISTINCT col)`, `AVG(col)`, `SUM(col)` ignore NULL; `COUNT(*)` does not. pandas `size()` counts rows, `count()` counts non-null, like `COUNT(*)` and `COUNT(col)`.
- `SELECT DISTINCT u` returns the NULL as one distinct row (3 rows) while `COUNT(DISTINCT u)` gives 2: the two differ on NULL by design.
- Rounding a percentage like 12.5 percent to a whole number gives 13 in SQLite and 12 in pandas; in a reconciliation this shows as a one-unit mismatch that is not a data bug.
- A pandas integer Series divided by a zero Series gave inf and NaN in my run (no exception); Python integers raise.
- Other engines: PostgreSQL integer division also truncates and division by zero raises an error; MySQL `/` returns a decimal and `DIV` is integer division; BigQuery `/` returns a float and `SAFE_DIVIDE` returns NULL on zero (all from memory, not executed here).

**Then explain:**
- Rule of thumb: SQL treats NULL as unknown (never equal to anything, including NULL), pandas treats NaN as a value that most aggregations skip but that `merge`, `set` and sorting treat in their own way.
- For metric code, make the rule explicit: fill or filter missing keys before grouping, `dropna=False` where a NaN group matters, `* 1.0` or `/` for ratios, and one agreed rounding helper.
- If a pandas result must equal SQL to the cent, do not rely on `round`; round once at the end the same way (half away from zero needs a helper) or compare with a tolerance.
- Rows were run in the Code block; the three asserts at the bottom pin the claims 'COUNT(DISTINCT) equals nunique', '3/2 is 1 versus 1.5' and 'ROUND(2.5) is 3.0 versus Python 2'.

**Follow-ups:**
- How do you make pandas merge behave like SQL on NaN keys? Drop or mask the NaN-key rows before the merge (`dropna(subset=['k'])`); then an inner merge matches SQL.
- How do you round half away from zero in pandas? Use `np.sign(x) * np.floor(np.abs(x) * 100 + 0.5) / 100`, accepting binary float effects; I did not run this helper here.
- Why did the NULL group show in SQL but not in pandas by default? Different design: SQL groups NULLs together, pandas drops them unless `dropna=False`.

**Common mistakes:**
- Assuming `groupby` totals add to the table total when the key has NaN.
- Using `len(set(...))` on a float column for distinct users.
- Expecting `/` to be integer division in SQLite or float division in older engines without checking.
- Rounding in pandas and SQL separately and then 'finding a bug' of 0.01.
- Merging on a key with NaN and getting extra rows that SQL would not return.


### Q32 ⭐⭐ 🟡 Sample ratio mismatch (SRM) check as counts: experiments(user_id, arm, assigned_ts) with a planned 50/50 split, and some users assigned in both arms or twice. Return per arm distinct users, the observed share, the expected count, the difference, and the chi-square statistic computed in plain arithmetic in the query (the p-value and threshold choice belong to Book 1 and Book 6; state a typical strict threshold only as a pointer). Explain the counting unit (distinct users, not rows), how users in both arms are found and reported, and why an SRM invalidates the conversion table from the earlier experiment question.
**Asked at:** experiment-metrics guides (PracHub and Statsig SRM pages and abtestly docs, search snippets only, not opened; SRM is a chi-square goodness-of-fit on distinct-user counts against the planned split, strict thresholds such as p < 0.001 in practice); the statistics belong to Book 1 and Book 6 and this question stays on counts, rates and uplift in SQL; guides, not candidate reports; experimentation and data scientist rounds
**Say this first (1 line):** Count distinct users per arm (not rows), compare each count with the planned share times the total, and the chi-square statistic is the sum of (observed - expected)^2 / expected over the arms, computed in plain arithmetic in the query; users assigned to both arms are found with `HAVING COUNT(DISTINCT arm) > 1` and reported separately, and the p-value and the strictness of the threshold are left to Books 1 and 6 (teams commonly use strict thresholds such as p < 0.001 for SRM, which varies by team and is only a pointer here).

**Schema and sample data:** seventeen assignment rows, fourteen distinct users. User 2 is assigned to control twice, user 11 to treatment twice, and user 14 appears in both arms. The planned split is 50/50. A second, generated table of 10,000 control and 10,600 treatment users is used in the Code block for the arithmetic at scale.
```sql
CREATE TABLE experiments(user_id INTEGER, arm TEXT, assigned_ts TEXT);
INSERT INTO experiments VALUES
 (1,'control','2024-03-01 09:00:00'),(2,'control','2024-03-01 09:01:00'),(2,'control','2024-03-02 09:00:00'),
 (3,'control','2024-03-01 09:02:00'),(4,'control','2024-03-01 09:03:00'),(5,'control','2024-03-01 09:04:00'),
 (6,'control','2024-03-01 09:05:00'),(7,'control','2024-03-01 09:06:00'),(8,'control','2024-03-01 09:07:00'),
 (9,'control','2024-03-01 09:08:00'),
 (10,'treatment','2024-03-01 09:09:00'),(11,'treatment','2024-03-01 09:10:00'),(11,'treatment','2024-03-03 09:00:00'),
 (12,'treatment','2024-03-01 09:11:00'),(13,'treatment','2024-03-01 09:12:00'),
 (14,'control','2024-03-01 09:13:00'),(14,'treatment','2024-03-02 09:13:00');
```

**SQL answer:** `SQL_MAIN` in the Code block (the planned split is a small `plan` table so it can change; `SQL_BOTH`, `SQL_ROWS`, `SQL_DUP` and `SQL_CLEAN` are the supporting queries):
```sql
WITH plan(arm, planned) AS (VALUES ('control', 0.5), ('treatment', 0.5)),
obs AS (
  SELECT arm, COUNT(DISTINCT user_id) AS users FROM experiments GROUP BY arm
), tot AS (SELECT SUM(users) AS n FROM obs),
x AS (
  SELECT p.arm, o.users, o.users * 1.0 / t.n AS observed_share, p.planned * t.n AS expected,
         o.users - p.planned * t.n AS diff,
         (o.users - p.planned * t.n) * (o.users - p.planned * t.n) / (p.planned * t.n) AS chi_part
  FROM plan p JOIN obs o ON o.arm = p.arm CROSS JOIN tot t
)
SELECT arm, users, ROUND(observed_share, 4) AS observed_share, expected, diff,
       ROUND(chi_part, 4) AS chi_part, ROUND((SELECT SUM(chi_part) FROM x), 4) AS chi_square
FROM x ORDER BY arm
```
```sql
SELECT user_id, COUNT(DISTINCT arm) AS arms, COUNT(*) AS rows_
FROM experiments GROUP BY user_id HAVING COUNT(DISTINCT arm) > 1
```

**pandas answer:** the same logic as a function, identical to the Code block (`clean=True` removes users in both arms first):
```py
def srm_counts(exp, planned={"control": 0.5, "treatment": 0.5}, clean=False):
    e = exp
    if clean:
        arms_per_user = e.groupby("user_id")["arm"].nunique()
        e = e[~e["user_id"].isin(arms_per_user[arms_per_user > 1].index)]
    obs = e.groupby("arm")["user_id"].nunique().rename("users").reset_index()
    n = obs["users"].sum()
    obs["planned"] = obs["arm"].map(planned)
    obs["observed_share"] = (obs["users"] / n).round(4)
    obs["expected"] = obs["planned"] * n
    obs["diff"] = obs["users"] - obs["expected"]
    chi_part = obs["diff"] ** 2 / obs["expected"]
    obs["chi_part"] = chi_part.round(4)
    obs["chi_square"] = round(float(chi_part.sum()), 4)
    return obs[["arm", "users", "observed_share", "expected", "diff", "chi_part", "chi_square"]]
```

**Example:** walk through the sample data by hand.
- Rows: control has 11 rows (users 1 to 9 with user 2 twice, plus user 14), treatment has 6 rows (users 10 to 13 with user 11 twice, plus user 14). Distinct users: control 10, treatment 5 (user 14 is in both). The row count of 17 against 14 distinct users shows three users with repeated rows (2, 11, 14).
- Per arm, counting user 14 in each arm: total 15, expected 7.5 each, observed shares 0.6667 and 0.3333, difference +2.5 and -2.5, chi parts 2.5^2/7.5 = 0.8333 each, chi-square 1.6667.
- Counting rows instead (wrong unit): 11 and 6, total 17, expected 8.5, chi-square 1.4706. The statistic changes because duplicates changed both the counts and the total.
- Removing the one user in both arms: 9 versus 4, total 13, expected 6.5, chi-square 1.9231.
- At scale (generated): 10,000 versus 10,600, total 20,600, expected 10,300, difference -300 and +300, chi parts 8.7379 each, chi-square 17.4757. Comparing that statistic with a threshold is out of scope here (Book 1 and Book 6).

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q32: sample ratio mismatch as counts: distinct users per arm, expected, difference, chi-square arithmetic
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE experiments(user_id INTEGER, arm TEXT, assigned_ts TEXT);
INSERT INTO experiments VALUES
 (1,'control','2024-03-01 09:00:00'),(2,'control','2024-03-01 09:01:00'),(2,'control','2024-03-02 09:00:00'),
 (3,'control','2024-03-01 09:02:00'),(4,'control','2024-03-01 09:03:00'),(5,'control','2024-03-01 09:04:00'),
 (6,'control','2024-03-01 09:05:00'),(7,'control','2024-03-01 09:06:00'),(8,'control','2024-03-01 09:07:00'),
 (9,'control','2024-03-01 09:08:00'),
 (10,'treatment','2024-03-01 09:09:00'),(11,'treatment','2024-03-01 09:10:00'),(11,'treatment','2024-03-03 09:00:00'),
 (12,'treatment','2024-03-01 09:11:00'),(13,'treatment','2024-03-01 09:12:00'),
 (14,'control','2024-03-01 09:13:00'),(14,'treatment','2024-03-02 09:13:00');
"""

# planned split is a parameter table; chi-square = sum over arms of (observed - expected)^2 / expected
SQL_MAIN = """
WITH plan(arm, planned) AS (VALUES ('control', 0.5), ('treatment', 0.5)),
obs AS (
  SELECT arm, COUNT(DISTINCT user_id) AS users FROM experiments GROUP BY arm
), tot AS (SELECT SUM(users) AS n FROM obs),
x AS (
  SELECT p.arm, o.users, o.users * 1.0 / t.n AS observed_share, p.planned * t.n AS expected,
         o.users - p.planned * t.n AS diff,
         (o.users - p.planned * t.n) * (o.users - p.planned * t.n) / (p.planned * t.n) AS chi_part
  FROM plan p JOIN obs o ON o.arm = p.arm CROSS JOIN tot t
)
SELECT arm, users, ROUND(observed_share, 4) AS observed_share, expected, diff,
       ROUND(chi_part, 4) AS chi_part, ROUND((SELECT SUM(chi_part) FROM x), 4) AS chi_square
FROM x ORDER BY arm
"""
# the same arithmetic on rows, to show the wrong counting unit
SQL_ROWS = SQL_MAIN.replace("COUNT(DISTINCT user_id)", "COUNT(*)")
assert SQL_ROWS != SQL_MAIN
SQL_BOTH = """
SELECT user_id, COUNT(DISTINCT arm) AS arms, COUNT(*) AS rows_
FROM experiments GROUP BY user_id HAVING COUNT(DISTINCT arm) > 1
"""
SQL_DUP = """
SELECT COUNT(*) AS rows_, COUNT(DISTINCT user_id) AS distinct_users,
       (SELECT COUNT(*) FROM (SELECT user_id FROM experiments GROUP BY user_id HAVING COUNT(*) > 1)) AS users_with_repeat_rows
FROM experiments
"""
# clean: users that appear in exactly one arm
SQL_CLEAN = SQL_MAIN.replace("FROM experiments GROUP BY arm",
    "FROM experiments WHERE user_id NOT IN (SELECT user_id FROM experiments GROUP BY user_id HAVING COUNT(DISTINCT arm) > 1) GROUP BY arm")
assert SQL_CLEAN != SQL_MAIN

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
print("SQL, distinct users per arm (users in both arms counted in each arm):")
print(sql_main.to_string(index=False))
print("SQL, same arithmetic on rows (wrong unit):")
print(pd.read_sql_query(SQL_ROWS, con).to_string(index=False))
print("SQL, after removing users that appear in both arms:")
sql_clean = pd.read_sql_query(SQL_CLEAN, con)
print(sql_clean.to_string(index=False))
print("users in both arms:")
print(pd.read_sql_query(SQL_BOTH, con).to_string(index=False))
print("row versus distinct counts:")
print(pd.read_sql_query(SQL_DUP, con).to_string(index=False))

exp = pd.read_sql_query("SELECT * FROM experiments", con)

# pd:main
def srm_counts(exp, planned={"control": 0.5, "treatment": 0.5}, clean=False):
    e = exp
    if clean:
        arms_per_user = e.groupby("user_id")["arm"].nunique()
        e = e[~e["user_id"].isin(arms_per_user[arms_per_user > 1].index)]
    obs = e.groupby("arm")["user_id"].nunique().rename("users").reset_index()
    n = obs["users"].sum()
    obs["planned"] = obs["arm"].map(planned)
    obs["observed_share"] = (obs["users"] / n).round(4)
    obs["expected"] = obs["planned"] * n
    obs["diff"] = obs["users"] - obs["expected"]
    chi_part = obs["diff"] ** 2 / obs["expected"]
    obs["chi_part"] = chi_part.round(4)
    obs["chi_square"] = round(float(chi_part.sum()), 4)
    return obs[["arm", "users", "observed_share", "expected", "diff", "chi_part", "chi_square"]]
# pd:end

pd_main = srm_counts(exp)
pd_clean = srm_counts(exp, clean=True)
# compare after sorting by arm (SQL ORDER BY arm)
pd.testing.assert_frame_equal(pd_main.sort_values("arm").reset_index(drop=True), sql_main, check_dtype=False)
pd.testing.assert_frame_equal(pd_clean.sort_values("arm").reset_index(drop=True), sql_clean, check_dtype=False)

# the same query on a generated table: 10,000 control and 10,600 treatment users (arithmetic at scale)
con.execute("DELETE FROM experiments")
con.executemany("INSERT INTO experiments VALUES (?, ?, '2024-03-01 00:00:00')",
                [(i, "control") for i in range(1, 10001)] + [(i, "treatment") for i in range(10001, 20601)])
big = pd.read_sql_query(SQL_MAIN, con)
print("generated 10,000 vs 10,600 users:")
print(big.to_string(index=False))
pd.testing.assert_frame_equal(srm_counts(pd.read_sql_query("SELECT * FROM experiments", con))
                              .sort_values("arm").reset_index(drop=True), big, check_dtype=False)
print("asserts passed")
```

**Output (my run):**
```text
SQL, distinct users per arm (users in both arms counted in each arm):
      arm  users  observed_share  expected  diff  chi_part  chi_square
  control     10          0.6667       7.5   2.5    0.8333      1.6667
treatment      5          0.3333       7.5  -2.5    0.8333      1.6667
SQL, same arithmetic on rows (wrong unit):
      arm  users  observed_share  expected  diff  chi_part  chi_square
  control     11          0.6471       8.5   2.5    0.7353      1.4706
treatment      6          0.3529       8.5  -2.5    0.7353      1.4706
SQL, after removing users that appear in both arms:
      arm  users  observed_share  expected  diff  chi_part  chi_square
  control      9          0.6923       6.5   2.5    0.9615      1.9231
treatment      4          0.3077       6.5  -2.5    0.9615      1.9231
users in both arms:
 user_id  arms  rows_
      14     2      2
row versus distinct counts:
 rows_  distinct_users  users_with_repeat_rows
    17              14                       3
generated 10,000 vs 10,600 users:
      arm  users  observed_share  expected   diff  chi_part  chi_square
  control  10000          0.4854   10300.0 -300.0    8.7379     17.4757
treatment  10600          0.5146   10300.0  300.0    8.7379     17.4757
asserts passed
```

**Edge cases:**
- Users in both arms: reported by `SQL_BOTH` (user 14). Whether to count them in each arm, drop them, or keep their first assignment is a decision; the raw and clean versions are both printed.
- Repeat rows for the same user and arm (users 2 and 11) inflate row counts but not distinct counts, which is why distinct users are the unit.
- An arm with zero users would make `plan` and `obs` not join; use a LEFT JOIN from `plan` if an arm can be missing.
- Expected counts below about 5 make a chi-square approximation unreliable (rule of thumb from statistics, not checked here); the toy data is only for arithmetic.
- Assignment time: late assignment or filtering on users who reached a page can itself cause an imbalance; this query only counts.

**Then explain:**
- Counting unit: distinct users, because the randomisation unit is the user. Rows include retries and re-assignments.
- Expected count is the planned share times the total distinct users, not the planned share times the larger arm.
- The chi-square statistic here is just arithmetic on counts; turning it into a p-value (1 degree of freedom for two arms) and choosing a threshold belongs to Books 1 and 6, and thresholds differ between vendors and teams.
- Why an SRM invalidates the conversion table from Q13: if assignment counts are off from the plan, something other than the treatment (a bug, a filter, a redirect) decided who ended up in each arm, so the two arms are no longer comparable populations and uplift in the Q13 table could come from that, not from the treatment. Fix the cause before reading any metric (contamination handling is Q44).
- Dialect: the `VALUES` plan table works in SQLite and Postgres; in BigQuery or Snowflake use a CTE with `SELECT ... UNION ALL` (not executed here).

**Follow-ups:**
- Three arms? Add a row to `plan`; the chi-square sum is unchanged (degrees of freedom change, a Book 1 point).
- Check SRM per day or per segment? Group the observed CTE by day or segment, and compare each to its own total.
- What do you do when SRM is flagged? Stop reading results, find the cause, rerun or exclude the affected segment.

**Common mistakes:**
- Counting rows instead of distinct users.
- Computing expected counts from the larger arm.
- Ignoring users in both arms.
- Reading a small chi-square as proof of no problem on tiny samples.
- Computing the p-value here and skipping the cause analysis.


### Q33 ⭐⭐ 🔴 Rolling 30-day active users per day with a date spine: events(user_id, event_ts, event_name). For every day from 2024-03-01 to 2024-03-31 return the DAU and the rolling MAU (distinct users active in the 30 days ending that day, inclusive), using a date spine (recursive CTE or a calendar table) and a range join on e.event_date between spine_date minus 29 days and spine_date. Return stickiness per day. Explain why ROWS BETWEEN 29 PRECEDING over daily counts is wrong (distinct users cannot be summed across days), why days with no events need the spine, and the cost of the range join on a large table (hedge: not executed beyond SQLite).
**Asked at:** active-user guides: Basedash DAU/WAU/MAU pitfalls article (opened; active definition, bots and internal accounts, time zone drift, incomplete periods, calendar vs rolling MAU, events vs users) plus search snippets of oneuptime ClickHouse DAU/WAU/MAU and stickiness posts and Swace and pmtoolkit pages (not opened); guides, not candidate reports; product analytics and data scientist rounds at social, streaming and SaaS companies
**Say this first (1 line):** Build a 31-row date spine with a recursive CTE, reduce events to distinct (user, date) rows, range-join each spine day to the user-days in `[day - 29, day]`, and take `COUNT(DISTINCT user_id)` for the rolling MAU and the distinct users on the day itself for DAU; stickiness is DAU over rolling MAU per day, and `ROWS BETWEEN 29 PRECEDING` over daily counts is wrong because a user active on five days would be counted five times.

**Schema and sample data:** fourteen events from 2024-01-31 to 2024-03-31 for five users. Conventions: the timestamps are UTC text, the day is the UTC date, and no test-user or bot table exists in this question so none is filtered (a real report would join `users` and filter, as in Q1). Events before March matter because the 30-day window reaches into February (2024 is a leap year). User 4's January 31 event is just outside the window of 2024-03-01; user 3's February 1 event is just inside. User 1 has two events on 2024-03-02, so one user-day.
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1, 4,'2024-01-31 10:00:00','open'),
 (2, 3,'2024-02-01 23:30:00','open'),
 (3, 1,'2024-02-05 09:00:00','open'),
 (4, 2,'2024-02-20 09:00:00','open'),
 (5, 1,'2024-03-01 08:00:00','open'),
 (6, 1,'2024-03-02 08:00:00','open'),
 (7, 1,'2024-03-02 21:00:00','click'),
 (8, 2,'2024-03-02 12:00:00','open'),
 (9, 1,'2024-03-03 08:00:00','open'),
 (10,5,'2024-03-05 08:00:00','open'),
 (11,3,'2024-03-15 08:00:00','open'),
 (12,4,'2024-03-20 08:00:00','open'),
 (13,1,'2024-03-31 08:00:00','open'),
 (14,2,'2024-03-31 09:00:00','open');
```

**SQL answer:** `SQL_MAIN` in the Code block (`SQL_WRONG` is the window-frame version, printed for comparison):
```sql
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-31'
), ud AS (
  SELECT DISTINCT user_id, date(event_ts) AS event_date FROM events
)
SELECT s.d AS day,
       COUNT(DISTINCT CASE WHEN ud.event_date = s.d THEN ud.user_id END) AS dau,
       COUNT(DISTINCT ud.user_id) AS rolling_mau,
       ROUND(COUNT(DISTINCT CASE WHEN ud.event_date = s.d THEN ud.user_id END) * 1.0 /
             NULLIF(COUNT(DISTINCT ud.user_id), 0), 4) AS stickiness
FROM spine s
LEFT JOIN ud ON ud.event_date BETWEEN date(s.d, '-29 days') AND s.d
GROUP BY s.d
ORDER BY s.d
```

**pandas answer:** the same logic as a function, identical to the Code block (cross merge of the spine with user-days, then filter to the window, then `nunique`):
```py
def rolling_active(events, start="2024-03-01", end="2024-03-31", window=30):
    ud = (events.assign(event_date=pd.to_datetime(events["event_ts"]).dt.normalize())
                [["user_id", "event_date"]].drop_duplicates())
    spine = pd.DataFrame({"day": pd.date_range(start, end)})
    m = spine.merge(ud, how="cross")
    lo = m["day"] - pd.Timedelta(days=window - 1)
    m = m[(m["event_date"] >= lo) & (m["event_date"] <= m["day"])]
    out = pd.DataFrame({
        "dau": m[m["event_date"] == m["day"]].groupby("day")["user_id"].nunique(),
        "rolling_mau": m.groupby("day")["user_id"].nunique()}).reindex(spine["day"]).fillna(0).astype(int)
    out["stickiness"] = (out["dau"] / out["rolling_mau"].where(out["rolling_mau"] != 0)).round(4)
    out = out.reset_index()
    out["day"] = out["day"].dt.strftime("%Y-%m-%d")
    return out
```

**Example:** walk through the sample data by hand.
- 2024-03-01: window is 2024-02-01 to 2024-03-01 (30 days: 29 in February because of the leap year, plus 1 March). Active users in it: user 3 (Feb 1, the first day of the window), user 2 (Feb 20), user 1 (Feb 5 and Mar 1). User 4 (Jan 31) is out. Rolling MAU = 3, DAU = 1 (user 1), stickiness 1/3 = 0.3333.
- 2024-03-02: window 2024-02-02 to 2024-03-02. User 3's last event (Feb 1) has dropped out, so users 1 and 2: MAU 2. DAU is 2 (user 1 twice on that day is one, plus user 2), stickiness 1.0.
- 2024-03-04: no events, DAU 0, but the rolling MAU is still 2 (users 1 and 2 are in the window). Without the spine this day would not exist; with it the row shows stickiness 0.0.
- 2024-03-15: user 3 returns; window is Feb 15 to Mar 15 so users 1, 2, 3, 5 give MAU 4, DAU 1, stickiness 0.25. 2024-03-31: window Mar 2 to Mar 31: users 1, 2, 3, 4, 5 are all in, MAU 5, DAU 2 (users 1 and 2), stickiness 0.4.
- Window-frame version: on 2024-03-31 summing daily DAU over 30 rows gives 8, not 5, because users 1 and 2 are counted on several days; on 2024-03-02 it gives 3 against a true 2. (That version also only sees March because the spine starts on March 1, a second flaw.)

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q33: rolling 30-day active users per day with a recursive-CTE date spine and a range join
import sqlite3
import pandas as pd

# Conventions: timestamps are UTC text, the day is the UTC date, no test-user table exists here so none is filtered.
SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1, 4,'2024-01-31 10:00:00','open'),
 (2, 3,'2024-02-01 23:30:00','open'),
 (3, 1,'2024-02-05 09:00:00','open'),
 (4, 2,'2024-02-20 09:00:00','open'),
 (5, 1,'2024-03-01 08:00:00','open'),
 (6, 1,'2024-03-02 08:00:00','open'),
 (7, 1,'2024-03-02 21:00:00','click'),
 (8, 2,'2024-03-02 12:00:00','open'),
 (9, 1,'2024-03-03 08:00:00','open'),
 (10,5,'2024-03-05 08:00:00','open'),
 (11,3,'2024-03-15 08:00:00','open'),
 (12,4,'2024-03-20 08:00:00','open'),
 (13,1,'2024-03-31 08:00:00','open'),
 (14,2,'2024-03-31 09:00:00','open');
"""

SQL_MAIN = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-31'
), ud AS (
  SELECT DISTINCT user_id, date(event_ts) AS event_date FROM events
)
SELECT s.d AS day,
       COUNT(DISTINCT CASE WHEN ud.event_date = s.d THEN ud.user_id END) AS dau,
       COUNT(DISTINCT ud.user_id) AS rolling_mau,
       ROUND(COUNT(DISTINCT CASE WHEN ud.event_date = s.d THEN ud.user_id END) * 1.0 /
             NULLIF(COUNT(DISTINCT ud.user_id), 0), 4) AS stickiness
FROM spine s
LEFT JOIN ud ON ud.event_date BETWEEN date(s.d, '-29 days') AND s.d
GROUP BY s.d
ORDER BY s.d
"""
# wrong: sum the daily distinct counts over 30 rows
SQL_WRONG = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01' UNION ALL SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-31'
), daily AS (
  SELECT date(event_ts) AS d, COUNT(DISTINCT user_id) AS dau FROM events GROUP BY date(event_ts)
)
SELECT s.d AS day, COALESCE(daily.dau, 0) AS dau,
       SUM(COALESCE(daily.dau, 0)) OVER (ORDER BY s.d ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS wrong_sum_of_daus
FROM spine s LEFT JOIN daily ON daily.d = s.d
ORDER BY s.d
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
print("SQL, 31 spine days (first 5 and every day with activity shown below):")
print(sql_main.head(5).to_string(index=False))
print(sql_main[sql_main["dau"] > 0].to_string(index=False))
print("rows returned:", len(sql_main), "; days with rolling_mau = 0:", int((sql_main["rolling_mau"] == 0).sum()))
wrong = pd.read_sql_query(SQL_WRONG, con)
cmp = wrong.merge(sql_main[["day", "rolling_mau"]], on="day")
print("wrong sum of DAUs versus distinct rolling MAU on selected days:")
print(cmp[cmp["day"].isin(["2024-03-02", "2024-03-03", "2024-03-31"])].to_string(index=False))

# date arithmetic: datetime/date modifiers versus unixepoch, across the leap day
chk = con.execute("SELECT date('2024-03-01','-29 days'), date(unixepoch('2024-03-01') - 29*86400,'unixepoch'), "
                  "datetime('2024-03-08 10:00:00','+7 days'), datetime(unixepoch('2024-03-08 10:00:00') + 7*86400,'unixepoch')").fetchone()
print("date arithmetic check:", chk)
assert chk[0] == chk[1] and chk[2] == chk[3]

events = pd.read_sql_query("SELECT * FROM events", con)

# pd:main
def rolling_active(events, start="2024-03-01", end="2024-03-31", window=30):
    ud = (events.assign(event_date=pd.to_datetime(events["event_ts"]).dt.normalize())
                [["user_id", "event_date"]].drop_duplicates())
    spine = pd.DataFrame({"day": pd.date_range(start, end)})
    m = spine.merge(ud, how="cross")
    lo = m["day"] - pd.Timedelta(days=window - 1)
    m = m[(m["event_date"] >= lo) & (m["event_date"] <= m["day"])]
    out = pd.DataFrame({
        "dau": m[m["event_date"] == m["day"]].groupby("day")["user_id"].nunique(),
        "rolling_mau": m.groupby("day")["user_id"].nunique()}).reindex(spine["day"]).fillna(0).astype(int)
    out["stickiness"] = (out["dau"] / out["rolling_mau"].where(out["rolling_mau"] != 0)).round(4)
    out = out.reset_index()
    out["day"] = out["day"].dt.strftime("%Y-%m-%d")
    return out
# pd:end

pd_res = rolling_active(events)
# compare in day order (SQL ORDER BY day); NaN stickiness equals NULL
pd.testing.assert_frame_equal(pd_res, sql_main, check_dtype=False)

# pandas 3.0 has Rolling.nunique: cross-check on days that have a row, using a time-based 30D window
ud = (events.assign(event_date=pd.to_datetime(events["event_ts"]).dt.normalize())
            [["user_id", "event_date"]].drop_duplicates().sort_values("event_date").set_index("event_date"))
rn = ud["user_id"].astype(float).rolling("30D").nunique()
last = rn.groupby(level=0).last()
chk_days = last.loc["2024-03-01":"2024-03-31"]
cmp2 = sql_main.set_index(pd.to_datetime(sql_main["day"])).loc[chk_days.index, "rolling_mau"]
assert (chk_days.astype(int).to_numpy() == cmp2.to_numpy()).all()
print("Rolling('30D').nunique matches rolling_mau on the", len(chk_days), "days that have event rows; spine days without events:",
      31 - len(chk_days))

# SQLite plan for the range join (no index): shows a scan, hedged for other engines
plan = con.execute("EXPLAIN QUERY PLAN " + SQL_MAIN).fetchall()
print("EXPLAIN QUERY PLAN rows:", [p[3] for p in plan])
print("asserts passed")
```

**Output (my run):**
```text
SQL, 31 spine days (first 5 and every day with activity shown below):
       day  dau  rolling_mau  stickiness
2024-03-01    1            3      0.3333
2024-03-02    2            2      1.0000
2024-03-03    1            2      0.5000
2024-03-04    0            2      0.0000
2024-03-05    1            3      0.3333
       day  dau  rolling_mau  stickiness
2024-03-01    1            3      0.3333
2024-03-02    2            2      1.0000
2024-03-03    1            2      0.5000
2024-03-05    1            3      0.3333
2024-03-15    1            4      0.2500
2024-03-20    1            5      0.2000
2024-03-31    2            5      0.4000
rows returned: 31 ; days with rolling_mau = 0: 0
wrong sum of DAUs versus distinct rolling MAU on selected days:
       day  dau  wrong_sum_of_daus  rolling_mau
2024-03-02    2                  3            2
2024-03-03    1                  4            2
2024-03-31    2                  8            5
date arithmetic check: ('2024-02-01', '2024-02-01', '2024-03-15 10:00:00', '2024-03-15 10:00:00')
Rolling('30D').nunique matches rolling_mau on the 7 days that have event rows; spine days without events: 24
EXPLAIN QUERY PLAN rows: ['CO-ROUTINE spine', 'SETUP', 'SCAN CONSTANT ROW', 'RECURSIVE STEP', 'SCAN spine', 'MATERIALIZE ud', 'SCAN events', 'USE TEMP B-TREE FOR DISTINCT', 'SCAN s', 'SCAN ud LEFT-JOIN', 'USE TEMP B-TREE FOR GROUP BY', 'USE TEMP B-TREE FOR count(DISTINCT)', 'USE TEMP B-TREE FOR count(DISTINCT)']
asserts passed
```

**Edge cases:**
- Days with no events: the LEFT JOIN from the spine keeps them (DAU 0). If the window had no users at all, MAU would be 0 and stickiness NULL through `NULLIF`; no such day occurs in this data (days with MAU 0: 0 in the output).
- Window length: a 30-day window ending on the day is `date(day, '-29 days')` to `day` inclusive. A 30-day window with `-30 days` is 31 days and a common off-by-one.
- Date arithmetic: I checked `date('2024-03-01','-29 days')` and `datetime('2024-03-08 10:00:00','+7 days')` against `unixepoch` arithmetic with 86400 seconds; they agree across the leap day (the Code block asserts it). Unlike `julianday` times a constant, this keeps whole days exact.
- Time zone: the day is the UTC date; a user in IST has evening events that fall on the next UTC date, so DAU by IST day differs (Q19, Q36).
- Duplicate events in a day are collapsed by the `DISTINCT` in the `ud` CTE; the range join then sees one row per user-day.
- pandas `Rolling.nunique`: exists in pandas 3.0.5 (the docstring says added in 3.0.0), so the premise that it does not exist is wrong for this version. It works on a time-indexed series with a `'30D'` window, but only produces values at rows that exist, so days without events still need the spine; the Code block checks it on the 7 days that have event rows.

**Then explain:**
- A rolling distinct count cannot be built from daily distinct counts: the same user appears on many days, so summing `DAU` over 30 days is a count of user-days, not users. The only fix is to look at the underlying user-days.
- The spine guarantees one output row per day, including quiet days, and supplies the right edge of each window. Without it you get rows only for days with events and a row-based frame such as `ROWS BETWEEN 29 PRECEDING` would silently span more than 30 calendar days.
- Range join cost: each spine day matches up to 30 days of user-days, so the work is roughly spine days times window rows. On a large table you pre-aggregate to user-days first (done in `ud`), index or sort on date, and limit the spine. SQLite's plan here shows a scan with a temporary B-tree for the distinct counts, which I printed; I did not benchmark anything, and other engines (hedged: not executed) have their own range-join and distinct-count strategies, for example approximate distinct functions.
- An alternative that avoids the range join is to track each user's last active date and compare, or to use first-active-date flags for trailing new-user counts; not run here.
- Stickiness is DAU over the same day's rolling MAU here. The calendar-month version (average DAU over calendar MAU) is Q15; fixed-date DAU/WAU/MAU is Q1.

**Follow-ups:**
- Rolling WAU instead? Change `-29 days` to `-6 days`; the rest is identical.
- Calendar MAU instead of rolling? Fix the window to the month, as in Q15.
- Faster for a big table? Pre-aggregate to user-days (already done), partition by date, and in warehouses consider approximate distinct counts and say it is approximate.

**Common mistakes:**
- `ROWS BETWEEN 29 PRECEDING` over daily distinct counts (shown, wrong).
- No spine, so quiet days vanish and the frame is not 30 calendar days.
- Off-by-one window (`-30 days`).
- Range joining raw events instead of distinct user-days.
- Mixing time zones between the spine and the events.
