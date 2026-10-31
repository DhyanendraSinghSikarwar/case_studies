# Q26: running balance per account with a same-timestamp tie.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE acct_txns(txn_id INTEGER PRIMARY KEY, account_id INTEGER, txn_ts TEXT, amount_paise INTEGER);
INSERT INTO acct_txns VALUES
 (1,1,'2025-06-01 09:00:00',10000),
 (2,1,'2025-06-01 10:00:00',-2500),
 (3,1,'2025-06-01 10:00:00',-4000),
 (4,1,'2025-06-02 09:00:00',700),
 (5,2,'2025-06-01 11:00:00',3000),
 (6,2,'2025-06-01 12:00:00',-500);
"""
SQL = """
SELECT txn_id, account_id, txn_ts, amount_paise,
       SUM(amount_paise) OVER (PARTITION BY account_id ORDER BY txn_ts, txn_id
                               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance_rows,
       SUM(amount_paise) OVER (PARTITION BY account_id ORDER BY txn_ts) AS balance_default_range
FROM acct_txns
ORDER BY account_id, txn_ts, txn_id
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

t = pd.read_sql("SELECT * FROM acct_txns", con)
# PANDAS START
p = t.sort_values(["account_id", "txn_ts", "txn_id"]).reset_index(drop=True)
p["balance_rows"] = p.groupby("account_id")["amount_paise"].cumsum()
# RANGE-like: every row of a tied timestamp shows the balance after the whole tie group
p["balance_default_range"] = p.groupby(["account_id", "txn_ts"])["balance_rows"].transform("last")
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (ordered by account_id, txn_ts, txn_id; both balance columns equal)")

# reversing txn_id inside the tie changes the intermediate balance but not the final one
alt = con.execute("""SELECT txn_id, SUM(amount_paise) OVER (PARTITION BY account_id ORDER BY txn_ts, txn_id DESC
                     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) FROM acct_txns
                     WHERE account_id = 1 ORDER BY txn_id""").fetchall()
print("account 1 with the tie broken by txn_id DESC (txn_id, balance):", alt)
