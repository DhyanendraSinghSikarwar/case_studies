# Q18: day-1 retention by signup date, 0.00 kept
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT);
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO users VALUES (1,'2025-03-01'),(2,'2025-03-01'),(3,'2025-03-01'),
                         (4,'2025-03-02'),(5,'2025-03-02'),(6,'2025-03-02'),
                         (7,'2025-03-03'),(8,'2025-03-03'),(9,'2025-03-03');
INSERT INTO logins VALUES (1,'2025-03-02'),(1,'2025-03-02'),(2,'2025-03-03'),(3,'2025-03-02'),
                          (4,'2025-03-03'),(6,'2025-03-09'),
                          (7,'2025-03-05'),(9,'2025-03-03');
""")
sql = """
SELECT u.signup_date,
       COUNT(DISTINCT u.user_id) AS signups,
       COUNT(DISTINCT CASE WHEN l.login_date = date(u.signup_date, '+1 day') THEN u.user_id END) AS retained,
       ROUND(1.0 * COUNT(DISTINCT CASE WHEN l.login_date = date(u.signup_date, '+1 day') THEN u.user_id END)
             / COUNT(DISTINCT u.user_id), 2) AS rate
FROM users u LEFT JOIN logins l ON l.user_id = u.user_id
GROUP BY u.signup_date ORDER BY u.signup_date
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.assign(rate=a.rate.map("{:.2f}".format)).to_string(index=False))
print("\nwithout DISTINCT, COUNT(*) of the joined rows for 2025-03-01 gives:",
      con.execute("SELECT COUNT(*) FROM users u JOIN logins l ON l.user_id=u.user_id AND l.login_date=date(u.signup_date,'+1 day') WHERE u.signup_date='2025-03-01'").fetchone()[0],
      "retained (user 1 has two login rows)")

u = pd.read_sql("SELECT * FROM users", con); lg = pd.read_sql("SELECT * FROM logins", con)
u["next_day"] = (pd.to_datetime(u.signup_date) + pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d")
hit = u.merge(lg.drop_duplicates(), left_on=["user_id", "next_day"], right_on=["user_id", "login_date"])
u["retained"] = u.user_id.isin(hit.user_id)
p = u.groupby("signup_date").agg(signups=("user_id", "nunique"), retained=("retained", "sum")).reset_index()
p["rate"] = (p.retained / p.signups).round(2)
print("\npandas"); print(p.assign(rate=p.rate.map("{:.2f}".format)).to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: equal, rows ordered by signup_date")
