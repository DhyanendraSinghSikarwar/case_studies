# Q37: outstanding balance per loan with pre-aggregated repayments.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE loans(loan_id INTEGER PRIMARY KEY, principal INTEGER);
CREATE TABLE repayments(repayment_id INTEGER, loan_id INTEGER, amount INTEGER);
INSERT INTO loans VALUES (1,1000),(2,500),(3,800),(4,600),(5,300);
INSERT INTO repayments VALUES (1,1,400),(2,1,300),(3,3,800),(4,4,700),(5,5,100),(6,99,50);
""")

sql_answer = """
SELECT l.loan_id, l.principal,
       COALESCE(r.paid, 0) AS paid,
       l.principal - COALESCE(r.paid, 0) AS outstanding,
       CASE WHEN COALESCE(r.paid, 0) > l.principal THEN 1 ELSE 0 END AS overpaid
FROM loans l
LEFT JOIN (SELECT loan_id, SUM(amount) AS paid FROM repayments GROUP BY loan_id) r
       ON r.loan_id = l.loan_id
ORDER BY l.loan_id
"""
sql_fanout = """
SELECT SUM(l.principal) FROM loans l LEFT JOIN repayments r ON r.loan_id = l.loan_id
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False))
print("\ntotal principal, correct:", con.execute("SELECT SUM(principal) FROM loans").fetchone()[0],
      "| after joining raw repayments (fan-out):", con.execute(sql_fanout).fetchone()[0])

# --- pandas
loans = pd.read_sql("SELECT * FROM loans", con)
rep = pd.read_sql("SELECT * FROM repayments", con)
paid = rep.groupby("loan_id").amount.sum().rename("paid").reset_index()
want = loans.merge(paid, on="loan_id", how="left")
want["paid"] = want.paid.fillna(0).astype(int)
want["outstanding"] = want.principal - want.paid
want["overpaid"] = (want.paid > want.principal).astype(int)
want = want.sort_values("loan_id").reset_index(drop=True)
# --- end pandas
print("\npandas"); print(want.to_string(index=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
assert 99 not in want.loan_id.values
print("assert passed: 5 loans, ordered by loan_id; orphan repayment for loan 99 appears in neither")
