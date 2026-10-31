# Q18: compound interest and loan amortisation with recursive CTEs, checked against the closed form and a Python loop
import sqlite3
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd

SCHEMA = """
CREATE TABLE accounts(acct_id INTEGER PRIMARY KEY, balance REAL, annual_rate REAL);
INSERT INTO accounts VALUES (1,1000,0.12),(2,2500,0.075),(3,100.55,0.06),(4,800,0.0),(5,500,NULL);
CREATE TABLE loans(loan_id INTEGER PRIMARY KEY, principal REAL, annual_rate REAL, months INTEGER);
INSERT INTO loans VALUES (1,10000,0.12,6),(2,5000,0.0,4),(3,1200,0.18,1);
"""
SQL_GROWTH = """
WITH RECURSIVE g(acct_id, month, bal) AS (
  SELECT acct_id, 0, balance FROM accounts
  UNION ALL
  SELECT g.acct_id, g.month + 1, ROUND(g.bal * (1 + a.annual_rate / 12.0), 2)
  FROM g JOIN accounts a ON a.acct_id = g.acct_id
  WHERE g.month < 12
)
SELECT g.acct_id, g.bal AS monthly_rounded,
       ROUND(a.balance * power(1 + a.annual_rate / 12.0, 12), 2) AS closed_form,
       ROUND(g.bal - a.balance * power(1 + a.annual_rate / 12.0, 12), 4) AS difference
FROM g JOIN accounts a ON a.acct_id = g.acct_id
WHERE g.month = 12
ORDER BY g.acct_id
"""
SQL_MAIN = """
WITH RECURSIVE l AS (
  SELECT loan_id, principal, months, annual_rate / 12.0 AS r,
         CASE WHEN annual_rate = 0 THEN ROUND(principal / months, 2)
              ELSE ROUND(principal * (annual_rate / 12.0) * power(1 + annual_rate / 12.0, months)
                         / (power(1 + annual_rate / 12.0, months) - 1), 2) END AS emi
  FROM loans
), s(loan_id, month, opening) AS (
  SELECT loan_id, 1, principal FROM l
  UNION ALL
  SELECT s.loan_id, s.month + 1,
         ROUND(s.opening - CASE WHEN s.month = l.months THEN s.opening
                                ELSE l.emi - ROUND(s.opening * l.r, 2) END, 2)
  FROM s JOIN l ON l.loan_id = s.loan_id
  WHERE s.month < l.months
), x AS (
  SELECT s.loan_id, s.month, s.opening, l.emi,
         ROUND(s.opening * l.r, 2) AS interest,
         CASE WHEN s.month = l.months THEN s.opening ELSE l.emi - ROUND(s.opening * l.r, 2) END AS principal_paid
  FROM s JOIN l ON l.loan_id = s.loan_id
)
SELECT loan_id, month, opening, interest, ROUND(principal_paid, 2) AS principal_paid,
       ROUND(interest + principal_paid, 2) AS payment,
       ROUND(opening - principal_paid, 2) AS closing
FROM x
ORDER BY loan_id, month
"""
SQL_NOFIX = SQL_MAIN.replace("CASE WHEN s.month = l.months THEN s.opening ELSE l.emi - ROUND(s.opening * l.r, 2) END", "l.emi - ROUND(s.opening * l.r, 2)")
assert SQL_NOFIX != SQL_MAIN
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
g = pd.read_sql_query(SQL_GROWTH, con)
print("(a) 12 months of monthly compounding, rounded to 2 decimals each month, versus the closed form:")
print(g.to_string(index=False))
sched = pd.read_sql_query(SQL_MAIN, con)
print("(b) amortisation schedules (loan 1 is 10000 at 12 percent for 6 months):")
print(sched.to_string(index=False))
print("EMI per loan:", dict(con.execute("SELECT loan_id, ROUND(principal*(annual_rate/12.0)*power(1+annual_rate/12.0,months)/(power(1+annual_rate/12.0,months)-1),2) FROM loans WHERE annual_rate > 0").fetchall()))
nofix = pd.read_sql_query(SQL_NOFIX, con)
print("without the last-row fix, closing balance after the last month:", nofix.groupby("loan_id")["closing"].last().to_dict())
print("with the fix:", sched.groupby("loan_id")["closing"].last().to_dict())

accounts = pd.read_sql_query("SELECT * FROM accounts", con)
loans = pd.read_sql_query("SELECT * FROM loans", con)

def r2(x):
    return float(Decimal(repr(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

def pandas_side(accounts, loans):
    # pd:main
    grow = accounts.assign(bal=accounts["balance"])
    for _ in range(12):
        grow["bal"] = [None if pd.isna(rt) else r2(b * (1 + rt / 12.0)) for b, rt in zip(grow["bal"], grow["annual_rate"])]
    grow["closed_form"] = [None if pd.isna(rt) else r2(b * (1 + rt / 12.0) ** 12) for b, rt in zip(grow["balance"], grow["annual_rate"])]
    rows = []
    for ln in loans.itertuples():
        r = ln.annual_rate / 12.0
        emi = r2(ln.principal / ln.months) if ln.annual_rate == 0 else r2(ln.principal * r * (1 + r) ** ln.months / ((1 + r) ** ln.months - 1))
        opening = ln.principal
        for m in range(1, ln.months + 1):
            interest = r2(opening * r)
            paid = opening if m == ln.months else emi - interest
            rows.append((ln.loan_id, m, opening, interest, r2(paid), r2(interest + paid), r2(opening - paid)))
            opening = r2(opening - paid)
    sch = pd.DataFrame(rows, columns=["loan_id", "month", "opening", "interest", "principal_paid", "payment", "closing"])
    return grow, sch
    # pd:end

grow, sch = pandas_side(accounts, loans)
cmp_g = grow[grow["annual_rate"].notna()][["acct_id", "bal", "closed_form"]].reset_index(drop=True)
g_ok = g[g["monthly_rounded"].notna()].reset_index(drop=True)
assert (cmp_g["bal"].round(2).to_numpy() == g_ok["monthly_rounded"].round(2).to_numpy()).all()
assert (cmp_g["closed_form"].round(2).to_numpy() == g_ok["closed_form"].round(2).to_numpy()).all()
print("pandas/Python growth loop equals SQL (rounded balance and closed form) for the 4 accounts with a rate; account 5 (NULL rate) stays NULL in SQL:", g.loc[g.acct_id == 5, "monthly_rounded"].isna().all())
pd.testing.assert_frame_equal(sch.round(2), sched.round(2), check_dtype=False)   # compared after sorting by loan_id, month
assert abs(sched.groupby("loan_id")["principal_paid"].sum().round(2) - loans.set_index("loan_id")["principal"]).max() < 1e-6
assert (sched.groupby("loan_id")["closing"].last() == 0).all()
print("pandas schedule equal to SQL; principal paid sums to the loan amount; last closing balance is 0")
print("total interest on loan 1:", round(sched[sched.loan_id == 1]["interest"].sum(), 2), "| total paid:", round(sched[sched.loan_id == 1]["payment"].sum(), 2))
print("zero-rate formula without the CASE:", con.execute("SELECT 5000 * 0 * power(1, 4) / (power(1, 4) - 1)").fetchone(), "(division by zero gives NULL in SQLite)")
print("exp/ln check of power(): ", con.execute("SELECT ROUND(power(1.01, 12), 10), ROUND(exp(12 * ln(1.01)), 10)").fetchone())
print("asserts passed")
