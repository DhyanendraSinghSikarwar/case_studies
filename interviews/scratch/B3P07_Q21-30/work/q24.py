# Q24: cumulative sum that resets at flagged rows (running SUM of is_reset as group key)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE txns(acct_id INTEGER, txn_id INTEGER, amount INTEGER, is_reset INTEGER);
INSERT INTO txns VALUES
 (1,3,30,0),(1,1,10,0),(1,2,20,0),(1,4,5,1),(1,5,7,0),(1,6,8,1),(1,7,1,0),
 (2,1,50,1),
 (3,1,9,0),(3,2,NULL,0),(3,3,4,NULL),(3,4,6,1),(3,5,NULL,0);
"""
SQL_MAIN = """
WITH k AS (
  SELECT acct_id, txn_id, amount, is_reset,
         SUM(COALESCE(is_reset, 0)) OVER (
           PARTITION BY acct_id ORDER BY txn_id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS grp
  FROM txns
)
SELECT acct_id, txn_id, amount, is_reset, grp,
       SUM(COALESCE(amount, 0)) OVER (
         PARTITION BY acct_id, grp ORDER BY txn_id
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_since_reset
FROM k
ORDER BY acct_id, txn_id
"""
SQL_RAWNULL = """
WITH k AS (
  SELECT acct_id, txn_id, amount, SUM(COALESCE(is_reset, 0)) OVER (PARTITION BY acct_id ORDER BY txn_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS grp
  FROM txns
)
SELECT acct_id, txn_id, SUM(amount) OVER (PARTITION BY acct_id, grp ORDER BY txn_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS raw_running
FROM k WHERE acct_id = 3 ORDER BY txn_id
"""
SQL_NOGROUP = """
SELECT acct_id, txn_id, SUM(COALESCE(amount, 0)) OVER (PARTITION BY acct_id ORDER BY txn_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS plain_running
FROM txns WHERE acct_id = 1 ORDER BY txn_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL answer:")
print(sql_df.to_string(index=False))
print("raw SUM(amount), NULL amounts, account 3:")
print(pd.read_sql_query(SQL_RAWNULL, con).to_string(index=False))
print("no reset (plain running total), account 1:")
print(pd.read_sql_query(SQL_NOGROUP, con).to_string(index=False))

txns = pd.read_sql_query("SELECT * FROM txns", con)
# pd:main
t = txns.sort_values(["acct_id", "txn_id"]).reset_index(drop=True)
t["grp"] = t["is_reset"].fillna(0).astype(int).groupby(t["acct_id"]).cumsum()
t["running_since_reset"] = t["amount"].fillna(0).groupby([t["acct_id"], t["grp"]]).cumsum().astype(int)
# pd:end
print("pandas answer:")
print(t.to_string(index=False))
cols = ["acct_id", "txn_id", "grp", "running_since_reset"]
pd.testing.assert_frame_equal(sql_df[cols].reset_index(drop=True), t[cols].reset_index(drop=True), check_dtype=False)  # sorted by acct_id, txn_id

# the honest difference: groupby cumsum on raw NaN keeps NaN on that row, SQL SUM skips the NULL
raw = txns.sort_values(["acct_id", "txn_id"]).reset_index(drop=True)
raw["grp"] = raw["is_reset"].fillna(0).astype(int).groupby(raw["acct_id"]).cumsum()
raw["raw_cumsum"] = raw["amount"].groupby([raw["acct_id"], raw["grp"]]).cumsum()
print("pandas raw cumsum, account 3:")
print(raw[raw["acct_id"] == 3][["txn_id", "amount", "raw_cumsum"]].to_string(index=False))

# the harder variant: reset when the running total EXCEEDS a threshold (state-dependent), plain loop as oracle
def reset_over(amounts, limit):
    out, tot = [], 0
    for a in amounts:
        tot += a
        out.append(tot)
        if tot > limit:
            tot = 0
    return out
amts = [40, 30, 50, 10, 60, 20, 90]
print("threshold 100 loop, running total after each row (resets after exceeding):", reset_over(amts, 100))
print("plain running total of the same rows:", list(pd.Series(amts).cumsum()))
print("SUM over only NULLs in SQLite:", con.execute("SELECT SUM(x) FROM (SELECT NULL AS x UNION ALL SELECT NULL)").fetchone()[0])
print("asserts passed")
