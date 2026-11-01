# Q25: days-past-due buckets as of 2025-06-30.
import sqlite3
import numpy as np
import pandas as pd

AS_OF = "2025-06-30"
DDL = """
CREATE TABLE loans(loan_id INTEGER PRIMARY KEY, due_date TEXT, paid_date TEXT);
INSERT INTO loans VALUES
 (1,'2025-06-30',NULL),
 (2,'2025-07-15',NULL),
 (3,'2025-06-29',NULL),
 (4,'2025-05-31',NULL),
 (5,'2025-05-30',NULL),
 (6,'2025-05-01',NULL),
 (7,'2025-04-30',NULL),
 (8,'2025-05-10','2025-05-10'),
 (9,'2025-05-10','2025-05-11');
"""
SQL = """
SELECT loan_id, due_date, paid_date,
       CASE WHEN paid_date IS NULL
            THEN CAST(julianday(:as_of) - julianday(due_date) AS INTEGER) END AS dpd,
       CASE
         WHEN paid_date IS NOT NULL AND paid_date <= due_date THEN 'PAID_ON_TIME'
         WHEN paid_date IS NOT NULL THEN 'PAID_LATE'
         WHEN julianday(:as_of) - julianday(due_date) <= 0 THEN 'CURRENT'
         WHEN julianday(:as_of) - julianday(due_date) <= 30 THEN 'DPD_1_30'
         WHEN julianday(:as_of) - julianday(due_date) <= 60 THEN 'DPD_31_60'
         ELSE 'DPD_61_PLUS'
       END AS bucket
FROM loans
ORDER BY loan_id
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con, params={"as_of": AS_OF})
print(s.to_string(index=False))

loans = pd.read_sql("SELECT * FROM loans", con)
# PANDAS START
as_of = pd.Timestamp("2025-06-30")
due = pd.to_datetime(loans["due_date"])
paid = pd.to_datetime(loans["paid_date"])
dpd = (as_of - due).dt.days
cut = pd.cut(dpd, bins=[-10**6, 0, 30, 60, 10**6],
             labels=["CURRENT", "DPD_1_30", "DPD_31_60", "DPD_61_PLUS"]).astype(object)
bucket = np.select([paid.notna() & (paid <= due), paid.notna()],
                   ["PAID_ON_TIME", "PAID_LATE"], default=cut)
p = loans[["loan_id", "due_date", "paid_date"]].copy()
p["dpd"] = dpd.where(paid.isna())
p["bucket"] = bucket
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (ordered by loan_id; dpd NULL equals NaN for paid loans)")
print("pd.cut default is right-closed: 30 falls in (0, 30], 31 in (30, 60]; counts by bucket:")
print(p["bucket"].value_counts().sort_index().to_string())
