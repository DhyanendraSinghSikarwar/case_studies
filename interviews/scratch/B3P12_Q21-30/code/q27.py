# Q27: cohort retention counts for months 0 to 2, NULL where the offset month is not finished yet.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE wallet_topups(customer_id INTEGER, topup_date TEXT);
INSERT INTO wallet_topups VALUES
 (1,'2025-01-05'),(1,'2025-02-10'),(1,'2025-03-12'),
 (2,'2025-01-20'),(2,'2025-03-03'),
 (3,'2025-01-15'),(3,'2025-01-25'),
 (4,'2025-01-31'),(4,'2025-02-01'),
 (5,'2025-01-02'),
 (6,'2025-02-03'),(6,'2025-03-04'),(6,'2025-04-05'),
 (7,'2025-02-14'),(7,'2025-04-20'),
 (8,'2025-02-28');
"""
SQL = """
WITH t AS (
  SELECT DISTINCT customer_id, substr(topup_date, 1, 7) AS act_month
  FROM wallet_topups WHERE topup_date <= :as_of
),
first AS (
  SELECT customer_id, MIN(act_month) AS cohort_month FROM t GROUP BY customer_id
),
offs(month_offset) AS (VALUES (0), (1), (2)),
cohorts AS (
  SELECT cohort_month, COUNT(*) AS cohort_size FROM first GROUP BY cohort_month
)
SELECT c.cohort_month, o.month_offset,
       CASE WHEN date(c.cohort_month || '-01', '+' || (o.month_offset + 1) || ' months', '-1 day') <= :as_of
            THEN (SELECT COUNT(*) FROM first f JOIN t
                    ON t.customer_id = f.customer_id
                   AND t.act_month = substr(date(f.cohort_month || '-01', '+' || o.month_offset || ' months'), 1, 7)
                  WHERE f.cohort_month = c.cohort_month)
       END AS active
FROM cohorts c CROSS JOIN offs o
ORDER BY c.cohort_month, o.month_offset
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
raw = pd.read_sql("SELECT * FROM wallet_topups", con)

# PANDAS START
def pandas_version(raw, as_of):
    as_of = pd.Timestamp(as_of)
    d = raw.assign(m=pd.to_datetime(raw["topup_date"]).dt.to_period("M"))
    d = d[pd.to_datetime(raw["topup_date"]) <= as_of][["customer_id", "m"]].drop_duplicates()
    d["cohort"] = d.groupby("customer_id")["m"].transform("min")
    d["off"] = (d["m"] - d["cohort"]).apply(lambda x: x.n)
    counts = d.groupby(["cohort", "off"])["customer_id"].nunique()
    rows = []
    for c in sorted(d["cohort"].unique()):
        for off in range(3):
            done = (c + off).end_time.normalize() <= as_of
            rows.append((str(c), off, int(counts.get((c, off), 0)) if done else None))
    return pd.DataFrame(rows, columns=["cohort_month", "month_offset", "active"])
# PANDAS END

def run(as_of, raw):
    s = pd.read_sql(SQL, con, params={"as_of": as_of})
    p = pandas_version(raw, as_of)
    s["active"] = s["active"].astype("Float64"); p["active"] = p["active"].astype("Float64")
    print(s.to_string(index=False))
    pd.testing.assert_frame_equal(s, p, check_dtype=False)
    print("asserts passed (ordered by cohort_month, month_offset)\n")

print("as of 2025-04-30 (both cohorts fully observable)")
run("2025-04-30", raw)
print("as of 2025-03-31 (February cohort is too young for offset 2)")
run("2025-03-31", raw)
con.execute("DELETE FROM wallet_topups WHERE customer_id IN (1, 4)")
raw2 = pd.read_sql("SELECT * FROM wallet_topups", con)
print("as of 2025-04-30 after deleting customers 1 and 4 (nobody active in February from the January cohort)")
run("2025-04-30", raw2)
