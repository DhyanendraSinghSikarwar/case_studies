# Q21: Monthly Transactions I (LeetCode 1193 pattern)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE transactions(id INTEGER PRIMARY KEY, country TEXT, state TEXT, amount INTEGER, trans_date TEXT);
INSERT INTO transactions VALUES
 (121,'US','approved',1000,'2018-12-18'),
 (122,'US','declined',2000,'2018-12-19'),
 (123,'US','approved',2000,'2019-01-01'),
 (124,'DE','approved',2000,'2019-01-07'),
 (125,NULL,'approved',500,'2019-01-10'),
 (126,NULL,'declined',100,'2019-01-11'),
 (127,'DE','declined',300,'2019-02-03');
"""
SQL_MAIN = """
SELECT strftime('%Y-%m', trans_date) AS month,
       country,
       COUNT(*) AS trans_count,
       SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved_count,
       SUM(amount) AS trans_total_amount,
       SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) AS approved_total_amount
FROM transactions
GROUP BY strftime('%Y-%m', trans_date), country
ORDER BY month, country
"""
SQL_NO_ELSE = """
SELECT strftime('%Y-%m', trans_date) AS month, country,
       SUM(CASE WHEN state = 'approved' THEN amount END) AS approved_total_amount
FROM transactions GROUP BY month, country ORDER BY month, country
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("without ELSE 0:")
print(pd.read_sql_query(SQL_NO_ELSE, con).to_string(index=False))

t = pd.read_sql_query("SELECT * FROM transactions", con)
# pd:main
x = t.assign(trans_date=pd.to_datetime(t["trans_date"]))
x["month"] = x["trans_date"].dt.strftime("%Y-%m")
x["approved_amount"] = x["amount"].where(x["state"] == "approved", 0)
x["is_approved"] = (x["state"] == "approved").astype(int)
pd_df = (x.groupby(["month", "country"], dropna=False)
          .agg(trans_count=("id", "count"), approved_count=("is_approved", "sum"),
               trans_total_amount=("amount", "sum"), approved_total_amount=("approved_amount", "sum"))
          .reset_index())
# pd:end
# compared after sorting by month, country with the NULL country first (as SQLite sorts NULL first)
pd_df = pd_df.sort_values(["month", "country"], na_position="first").reset_index(drop=True)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("pandas equals SQL")
dropped = x.groupby(["month", "country"]).agg(n=("id", "count")).reset_index()
print("pandas default groupby (dropna=True) rows:", len(dropped), "versus SQL rows:", len(sql_df))
print("asserts passed")
