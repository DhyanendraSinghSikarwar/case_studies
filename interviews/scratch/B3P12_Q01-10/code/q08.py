# Q8: double-entry audit: unbalanced entries, first negative WALLET balance, and why not RANGE.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE account(account TEXT PRIMARY KEY, kind TEXT);
CREATE TABLE journal_lines(entry_id INTEGER, line_no INTEGER, account TEXT, debit_paise INTEGER, credit_paise INTEGER, posted_at TEXT);
INSERT INTO account VALUES ('WALLET','LIABILITY'),('CASH','ASSET'),('REVENUE','INCOME'),('BANK','ASSET');
INSERT INTO journal_lines VALUES
 (1,1,'CASH',   500,0,  '2025-06-01 09:00:00'),(1,2,'WALLET',0,500,'2025-06-01 09:00:00'),   -- wallet +500 = 500
 (2,1,'WALLET', 200,0,  '2025-06-01 10:00:00'),(2,2,'CASH',  0,200,'2025-06-01 10:00:00'),   -- wallet -200 = 300
 (3,1,'WALLET', 400,0,  '2025-06-01 11:00:00'),(3,2,'REVENUE',0,400,'2025-06-01 11:00:00'),  -- tie at 11:00:00, wallet -400
 (4,1,'BANK',   300,0,  '2025-06-01 11:00:00'),(4,2,'WALLET',0,300,'2025-06-01 11:00:00'),   -- tie at 11:00:00, wallet +300
 (5,1,'CASH',   100,0,  '2025-06-01 12:00:00'),(5,2,'REVENUE',0, 90,'2025-06-01 12:00:00'),  -- UNBALANCED by 10
 (6,1,'CASH',    50,0,  '2025-06-01 13:00:00'),(6,2,'WALLET',0, 50,'2025-06-01 13:00:00');
""")

unbal_sql = """
SELECT entry_id, SUM(debit_paise) AS debits, SUM(credit_paise) AS credits,
       SUM(debit_paise) - SUM(credit_paise) AS diff
FROM journal_lines GROUP BY entry_id
HAVING SUM(debit_paise) <> SUM(credit_paise) ORDER BY entry_id
"""
run_sql = """
SELECT j.entry_id, j.line_no, j.posted_at,
       SUM(j.credit_paise - j.debit_paise) OVER (ORDER BY j.posted_at, j.entry_id, j.line_no
                                                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance
FROM journal_lines j JOIN account a ON a.account = j.account
WHERE j.account = 'WALLET' ORDER BY j.posted_at, j.entry_id, j.line_no
"""
first_neg_sql = """
WITH r AS (%s)
SELECT entry_id, line_no, posted_at, balance FROM r WHERE balance < 0 ORDER BY posted_at, entry_id, line_no LIMIT 1
""" % run_sql
range_sql = """
SELECT entry_id, line_no, posted_at,
       SUM(credit_paise - debit_paise) OVER (ORDER BY posted_at) AS balance_default_range
FROM journal_lines WHERE account = 'WALLET' ORDER BY posted_at, entry_id, line_no
"""
u = pd.read_sql(unbal_sql, con); r = pd.read_sql(run_sql, con); f = pd.read_sql(first_neg_sql, con)
rg = pd.read_sql(range_sql, con)
print("(a) unbalanced entries:"); print(u.to_string(index=False)); print()
print("(b) WALLET running balance, ROWS frame, tie broken by entry_id, line_no:"); print(r.to_string(index=False)); print()
print("first negative posting:"); print(f.to_string(index=False)); print()
print("same data with ORDER BY posted_at only (default RANGE frame):"); print(rg.to_string(index=False))
print("min balance with RANGE:", rg["balance_default_range"].min(), "-> the dip is invisible"); print()

# pandas
jl = pd.read_sql("SELECT * FROM journal_lines", con)
g = jl.groupby("entry_id").agg(debits=("debit_paise", "sum"), credits=("credit_paise", "sum")).reset_index()
g["diff"] = g["debits"] - g["credits"]
pu = g[g["diff"] != 0].reset_index(drop=True)
w = jl[jl["account"] == "WALLET"].sort_values(["posted_at", "entry_id", "line_no"]).copy()
w["balance"] = (w["credit_paise"] - w["debit_paise"]).cumsum()
pr = w[["entry_id", "line_no", "posted_at", "balance"]].reset_index(drop=True)
pf = pr[pr["balance"] < 0].head(1).reset_index(drop=True)
print("pandas unbalanced:"); print(pu.to_string(index=False))
print("pandas first negative:"); print(pf.to_string(index=False))
pd.testing.assert_frame_equal(u, pu, check_dtype=False)
pd.testing.assert_frame_equal(r, pr, check_dtype=False)
pd.testing.assert_frame_equal(f, pf, check_dtype=False)
print("asserts passed (order posted_at, entry_id, line_no)")
