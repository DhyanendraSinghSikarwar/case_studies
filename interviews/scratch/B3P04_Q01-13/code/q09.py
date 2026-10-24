# Q9: keep the latest row per key, with a tie-breaker
import sqlite3
import pandas as pd

ROWS = [(1,1,'a@x.com','2026-01-01'),(2,1,'a2@x.com','2026-02-01'),(3,1,'a3@x.com','2026-02-01'),
        (4,2,'b@x.com','2026-01-15'),(5,3,'c@x.com','2026-03-05'),(6,3,'c0@x.com','2026-01-01'),
        (7,4,'d@x.com',None),(8,4,'d2@x.com','2026-01-10'),(9,5,'e@x.com',None)]
SCHEMA = "CREATE TABLE customer_updates(update_id INTEGER PRIMARY KEY, customer_id INTEGER, email TEXT, updated_at TEXT);"
# latest updated_at wins; update_id DESC breaks ties
SQL_MAIN = """
WITH ranked AS (
  SELECT update_id, customer_id, email, updated_at,
         ROW_NUMBER() OVER (PARTITION BY customer_id
                            ORDER BY updated_at DESC, update_id DESC) AS rn
  FROM customer_updates
)
SELECT update_id, customer_id, email, updated_at
FROM ranked
WHERE rn = 1
ORDER BY customer_id
"""
SQL_FIRST = """
WITH ranked AS (
  SELECT update_id, customer_id, email, updated_at,
         ROW_NUMBER() OVER (PARTITION BY customer_id
                            ORDER BY updated_at ASC, update_id ASC) AS rn
  FROM customer_updates
)
SELECT update_id, customer_id, email, updated_at FROM ranked WHERE rn = 1 ORDER BY customer_id
"""
SQL_NOTIE = """
WITH ranked AS (
  SELECT update_id, customer_id,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) AS rn
  FROM customer_updates)
SELECT update_id FROM ranked WHERE rn = 1 AND customer_id = 1
"""
def load(rows):
    con = sqlite3.connect(":memory:")
    con.execute(SCHEMA)
    con.executemany("INSERT INTO customer_updates VALUES (?,?,?,?)", rows)
    return con
con = load(ROWS)
sql_df = pd.read_sql_query(SQL_MAIN, con)
first_df = pd.read_sql_query(SQL_FIRST, con)
print("latest per customer:"); print(sql_df.to_string(index=False))
print("\nfirst per customer:"); print(first_df.to_string(index=False))

cu = pd.read_sql_query("SELECT * FROM customer_updates", con)
# pd:main
pd_df = (cu.sort_values(["updated_at", "update_id"], ascending=[False, False])
           .drop_duplicates(subset="customer_id", keep="first"))
# pd:end
# pd:first
pd_first = (cu.sort_values(["updated_at", "update_id"], ascending=[True, True])
              .drop_duplicates(subset="customer_id", keep="first"))
# pd:end
# compared after sorting by customer_id
pd.testing.assert_frame_equal(sql_df, pd_df.sort_values("customer_id").reset_index(drop=True), check_dtype=False)
pf = pd_first.sort_values("customer_id").reset_index(drop=True)
diff = first_df.loc[first_df["update_id"] != pf["update_id"], "customer_id"].tolist()
print("\ncustomers where SQL keep-first (ASC) and pandas keep-first (ASC) pick different rows:", diff)
assert diff == [4]   # NULL date sorts FIRST in SQLite ASC, but pandas sort_values puts NaN LAST

print("\nno tie-breaker, customer 1 pick on SQLite 3.45 (repeatable here, not guaranteed):",
      load(ROWS).execute(SQL_NOTIE).fetchall(), load(ROWS[::-1]).execute(SQL_NOTIE).fetchall())
print("asserts passed: SQL latest == pandas sort_values + drop_duplicates")
