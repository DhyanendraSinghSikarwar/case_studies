# Q6: ledger vs bank settlement file: one status per txn_id.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE ledger(txn_id TEXT, amount_paise INTEGER, txn_date TEXT);
CREATE TABLE bank_file(bank_ref TEXT, txn_id TEXT, amount_paise INTEGER, settled_date TEXT);
INSERT INTO ledger VALUES
 ('T1',10000,'2025-06-01'),('T2',25000,'2025-06-01'),('T3',5000,'2025-06-02'),('T4',7500,'2025-06-02'),
 ('T5',12000,'2025-06-03'),('T6',3000,'2025-06-03'),('T7',9900,'2025-06-04'),('T8',4000,'2025-06-04');
INSERT INTO bank_file VALUES
 ('B1','T1',10000,'2025-06-02'),('B2','T2',24500,'2025-06-02'),('B3','T3',5000,'2025-06-03'),
 ('B4','T4',7500,'2025-06-03'),('B5','T5',12000,'2025-06-04'),('B6','T5',12000,'2025-06-04'),
 ('B7','T6',3000,'2025-06-04'),('B8','T8',4000,'2025-06-05'),('B9','T9',1500,'2025-06-05');
""")

full_sql = """
WITH b AS (                                    -- one row per txn_id: dedupe BEFORE comparing
  SELECT txn_id, COUNT(*) AS n_bank, MIN(amount_paise) AS bank_min, MAX(amount_paise) AS bank_max
  FROM bank_file GROUP BY txn_id
)
SELECT COALESCE(l.txn_id, b.txn_id) AS txn_id,
       l.amount_paise AS ledger_paise, b.bank_min AS bank_paise,
       CASE WHEN b.txn_id IS NULL THEN 'MISSING_IN_BANK'
            WHEN l.txn_id IS NULL THEN 'MISSING_IN_LEDGER'
            WHEN b.n_bank > 1 THEN 'DUPLICATE_IN_BANK'
            WHEN l.amount_paise <> b.bank_min THEN 'AMOUNT_MISMATCH'
            ELSE 'MATCHED' END AS status
FROM ledger l FULL OUTER JOIN b ON b.txn_id = l.txn_id
ORDER BY txn_id
"""
emul_sql = """
WITH b AS (
  SELECT txn_id, COUNT(*) AS n_bank, MIN(amount_paise) AS bank_min FROM bank_file GROUP BY txn_id
), j AS (
  SELECT l.txn_id AS lid, b.txn_id AS bid, l.amount_paise AS lp, b.bank_min AS bp, b.n_bank AS n
  FROM ledger l LEFT JOIN b ON b.txn_id = l.txn_id
  UNION ALL
  SELECT NULL, b.txn_id, NULL, b.bank_min, b.n_bank FROM b WHERE NOT EXISTS (SELECT 1 FROM ledger l WHERE l.txn_id = b.txn_id)
)
SELECT COALESCE(lid, bid) AS txn_id, lp AS ledger_paise, bp AS bank_paise,
       CASE WHEN bid IS NULL THEN 'MISSING_IN_BANK'
            WHEN lid IS NULL THEN 'MISSING_IN_LEDGER'
            WHEN n > 1 THEN 'DUPLICATE_IN_BANK'
            WHEN lp <> bp THEN 'AMOUNT_MISMATCH'
            ELSE 'MATCHED' END AS status
FROM j ORDER BY txn_id
"""
naive_sql = "SELECT l.txn_id, COUNT(*) AS rows_out FROM ledger l JOIN bank_file b ON b.txn_id = l.txn_id GROUP BY l.txn_id HAVING COUNT(*) > 1"

s = pd.read_sql(full_sql, con)
e = pd.read_sql(emul_sql, con)
print("SQL FULL OUTER JOIN (SQLite 3.45):"); print(s.to_string(index=False)); print()
print("naive join without deduping bank_file, txn_ids that fan out:"); print(pd.read_sql(naive_sql, con).to_string(index=False)); print()
pd.testing.assert_frame_equal(s, e, check_dtype=False)

print("NULL trap in the compare:", con.execute("SELECT CASE WHEN 5 <> NULL THEN 'AMOUNT_MISMATCH' ELSE 'MATCHED' END, "
      "CASE WHEN 5 IS NOT NULL THEN 'AMOUNT_MISMATCH' ELSE 'MATCHED' END").fetchone(), "(<> vs IS NOT)"); print()

# pandas
ledger = pd.read_sql("SELECT * FROM ledger", con); bank = pd.read_sql("SELECT * FROM bank_file", con)
b = bank.groupby("txn_id", as_index=False).agg(n_bank=("bank_ref", "size"), bank_paise=("amount_paise", "min"))
m = ledger.merge(b, on="txn_id", how="outer", indicator=True)
m = m.rename(columns={"amount_paise": "ledger_paise"})
m["status"] = np.select(
    [m["_merge"] == "left_only", m["_merge"] == "right_only", m["n_bank"] > 1, m["ledger_paise"] != m["bank_paise"]],
    ["MISSING_IN_BANK", "MISSING_IN_LEDGER", "DUPLICATE_IN_BANK", "AMOUNT_MISMATCH"], default="MATCHED")
p = m[["txn_id", "ledger_paise", "bank_paise", "status"]].sort_values("txn_id").reset_index(drop=True)
print("pandas outer merge with indicator:"); print(p.to_string(index=False)); print()
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("status counts:", s["status"].value_counts().sort_index().to_dict())
print("asserts passed (FULL JOIN = UNION ALL emulation = pandas; compared after ordering by txn_id)")
