# Q12: running total that resets after it reaches a threshold (100): recursive CTE versus pandas loop
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE txns(acct_id TEXT, txn_id INTEGER, amount INTEGER);
INSERT INTO txns VALUES
 ('A',1,40),('A',2,30),('A',3,50),('A',4,20),('A',5,90),('A',6,10),('A',7,100),('A',8,5),
 ('B',1,100),('B',2,100),('B',3,60),('B',4,30),('B',5,10),
 ('C',1,150),
 ('D',1,50),('D',2,NULL),('D',3,60);
"""
SQL_MAIN = """
WITH RECURSIVE t AS (
  SELECT acct_id, txn_id, COALESCE(amount, 0) AS amount,
         ROW_NUMBER() OVER (PARTITION BY acct_id ORDER BY txn_id) AS rn
  FROM txns
), r(acct_id, rn, txn_id, amount, running, reset_flag) AS (
  SELECT acct_id, rn, txn_id, amount, amount, CASE WHEN amount >= 100 THEN 1 ELSE 0 END
  FROM t WHERE rn = 1
  UNION ALL
  SELECT t.acct_id, t.rn, t.txn_id, t.amount,
         CASE WHEN r.reset_flag = 1 THEN t.amount ELSE r.running + t.amount END,
         CASE WHEN (CASE WHEN r.reset_flag = 1 THEN t.amount ELSE r.running + t.amount END) >= 100 THEN 1 ELSE 0 END
  FROM r JOIN t ON t.acct_id = r.acct_id AND t.rn = r.rn + 1
)
SELECT acct_id, txn_id, amount, running, reset_flag
FROM r
ORDER BY acct_id, rn
"""
# a window function once the flags are known: the group key is the number of resets strictly before the row
SQL_WINDOW_GIVEN_FLAGS = """
WITH RECURSIVE t AS (
  SELECT acct_id, txn_id, COALESCE(amount, 0) AS amount,
         ROW_NUMBER() OVER (PARTITION BY acct_id ORDER BY txn_id) AS rn
  FROM txns
), r(acct_id, rn, running, reset_flag) AS (
  SELECT acct_id, rn, amount, CASE WHEN amount >= 100 THEN 1 ELSE 0 END FROM t WHERE rn = 1
  UNION ALL
  SELECT t.acct_id, t.rn,
         CASE WHEN r.reset_flag = 1 THEN t.amount ELSE r.running + t.amount END,
         CASE WHEN (CASE WHEN r.reset_flag = 1 THEN t.amount ELSE r.running + t.amount END) >= 100 THEN 1 ELSE 0 END
  FROM r JOIN t ON t.acct_id = r.acct_id AND t.rn = r.rn + 1
), g AS (
  SELECT t.acct_id, t.rn, t.txn_id, t.amount, r.reset_flag,
         COALESCE(SUM(r.reset_flag) OVER (PARTITION BY t.acct_id ORDER BY t.rn
                  ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING), 0) AS grp
  FROM t JOIN r ON r.acct_id = t.acct_id AND r.rn = t.rn
)
SELECT acct_id, txn_id, amount,
       SUM(amount) OVER (PARTITION BY acct_id, grp ORDER BY rn) AS running, reset_flag
FROM g ORDER BY acct_id, rn
"""
# the tempting window-only answer: cut the plain running total into buckets of 100
SQL_NAIVE = """
WITH c AS (
  SELECT acct_id, txn_id, COALESCE(amount, 0) AS amount,
         SUM(COALESCE(amount, 0)) OVER (PARTITION BY acct_id ORDER BY txn_id) AS cum
  FROM txns
)
SELECT acct_id, txn_id, amount, cum, cum % 100 AS naive_running, CASE WHEN cum / 100 > LAG(cum / 100, 1, 0) OVER (PARTITION BY acct_id ORDER BY txn_id) THEN 1 ELSE 0 END AS naive_flag
FROM c ORDER BY acct_id, txn_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("recursive CTE result:")
print(sql_df.to_string(index=False))

txns = pd.read_sql_query("SELECT * FROM txns", con)

def reset_running(txns, limit=100):
    # pd:main
    t = txns.assign(amount=txns["amount"].fillna(0).astype(int)).sort_values(["acct_id", "txn_id"])
    rows = []
    for acct, g in t.groupby("acct_id", sort=True):
        running, flag = 0, 0
        for txn_id, amount in zip(g["txn_id"], g["amount"]):
            running = amount if flag == 1 else running + amount
            flag = 1 if running >= limit else 0
            rows.append((acct, txn_id, amount, running, flag))
    return pd.DataFrame(rows, columns=["acct_id", "txn_id", "amount", "running", "reset_flag"])
    # pd:end

pd_df = reset_running(txns)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)   # compared after sorting by acct_id, txn_id
print("pandas loop equal to recursive CTE")

win = pd.read_sql_query(SQL_WINDOW_GIVEN_FLAGS, con)
pd.testing.assert_frame_equal(win, sql_df, check_dtype=False)
print("window function with the flags supplied: equal (the flags still came from the recursion)")

naive = pd.read_sql_query(SQL_NAIVE, con)
m = naive.merge(sql_df[["acct_id", "txn_id", "running", "reset_flag"]], on=["acct_id", "txn_id"])
print("window-only buckets of 100, rows that disagree with the true result:")
print(m[(m.naive_running != m.running) | (m.naive_flag != m.reset_flag)][["acct_id", "txn_id", "amount", "running", "naive_running", "reset_flag", "naive_flag"]].to_string(index=False))

# long account: SQLite has no default depth limit like MySQL (1000) or SQL Server (100)
con.execute("CREATE TABLE big(acct_id TEXT, txn_id INTEGER, amount INTEGER)")
con.executemany("INSERT INTO big VALUES ('Z', ?, ?)", [(i, 7) for i in range(1, 5001)])
n = con.execute(SQL_MAIN.replace("FROM txns", "FROM big").replace("ORDER BY acct_id, rn", "ORDER BY acct_id, rn DESC LIMIT 1")).fetchone()
print("5000-row single account, last row:", n, "(5000 recursion levels ran in SQLite)")
bigdf = pd.read_sql_query("SELECT * FROM big", con)
assert reset_running(bigdf).iloc[-1].tolist() == list(n)
print("empty table:", con.execute(SQL_MAIN.replace("FROM txns", "FROM txns WHERE 1 = 0")).fetchall())
print("asserts passed")
