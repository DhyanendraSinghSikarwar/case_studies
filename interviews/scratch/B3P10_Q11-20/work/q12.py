# Q12: row-wise versus column-wise NULL in a survey (SQL vs pandas)
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE survey(user_id INTEGER PRIMARY KEY, q1 INTEGER, q2 INTEGER, q3 INTEGER);  -- NULL = not answered
INSERT INTO survey VALUES
 (1,4,5,3),
 (2,4,NULL,2),
 (3,NULL,NULL,NULL),
 (4,5,NULL,NULL),
 (5,1,2,NULL);
""")

# <<sql_a
SQL_A = """
SELECT user_id, (q1 + q2 + q3) / 3.0 AS avg_a FROM survey ORDER BY user_id
"""
# >>
# <<sql_b
SQL_B = """
SELECT user_id,
       (COALESCE(q1, 0) + COALESCE(q2, 0) + COALESCE(q3, 0)) * 1.0
         / NULLIF((q1 IS NOT NULL) + (q2 IS NOT NULL) + (q3 IS NOT NULL), 0) AS avg_b
FROM survey ORDER BY user_id
"""
# >>
# <<sql_b2
SQL_B_UNPIVOT = """
SELECT user_id, AVG(score) AS avg_b2
FROM (SELECT user_id, q1 AS score FROM survey
      UNION ALL SELECT user_id, q2 FROM survey
      UNION ALL SELECT user_id, q3 FROM survey)
GROUP BY user_id ORDER BY user_id
"""
# >>
# <<sql_c
SQL_C = """
SELECT AVG(q1) AS q1_avg, AVG(q2) AS q2_avg, AVG(q3) AS q3_avg,
       AVG(COALESCE(q1, 0)) AS q1_avg_zero, AVG(COALESCE(q2, 0)) AS q2_avg_zero, AVG(COALESCE(q3, 0)) AS q3_avg_zero
FROM survey
"""
# >>
a = pd.read_sql_query(SQL_A, con)
b = pd.read_sql_query(SQL_B, con)
b2 = pd.read_sql_query(SQL_B_UNPIVOT, con)
c = pd.read_sql_query(SQL_C, con)
print("(a) (q1+q2+q3)/3.0:"); print(a.to_string(index=False))
print("(b) sum of answers / number of answers:"); print(b.to_string(index=False))
print("(b) via UNION ALL unpivot + AVG:"); print(b2.to_string(index=False))
print("(c) per question, NULLs ignored versus NULL coerced to 0:"); print(c.round(3).to_string(index=False))

# <<pd
survey = pd.read_sql_query("SELECT * FROM survey", con).set_index("user_id")
qs = survey[["q1", "q2", "q3"]]
p_b = qs.mean(axis=1)                          # skipna=True by default: sum of answers / number of answers
p_a = qs.mean(axis=1, skipna=False)            # same as (q1+q2+q3)/3.0: NaN if any answer missing
p_sum = qs.sum(axis=1, min_count=1)            # NaN (not 0) when every answer is missing
p_c = qs.mean()                                # column-wise, NaN ignored
# >>
print("\ndtypes:", dict(qs.dtypes.astype(str)), "(NULL made the integer columns float64)")
print("pandas mean(axis=1):", p_b.tolist())
print("pandas mean(axis=1, skipna=False):", p_a.tolist())
print("pandas sum(axis=1) default (all-NaN row gives 0.0):", qs.sum(axis=1).tolist())
print("pandas sum(axis=1, min_count=1):", p_sum.tolist())
print("pandas q1.fillna(0).mean():", qs["q1"].fillna(0).mean(), "versus q1.mean():", qs["q1"].mean())

# matches: compare rows ordered by user_id; SQL NULL arrives as NaN in pandas
pd.testing.assert_series_equal(p_b.reset_index(drop=True), b["avg_b"], check_names=False)
pd.testing.assert_series_equal(p_b.reset_index(drop=True), b2["avg_b2"], check_names=False)
pd.testing.assert_series_equal(p_a.reset_index(drop=True), a["avg_a"], check_names=False)
assert np.allclose(p_c.to_numpy(), c.loc[0, ["q1_avg", "q2_avg", "q3_avg"]].to_numpy(dtype=float))
assert b.loc[b["user_id"] == 3, "avg_b"].isna().all() and np.isnan(p_b.loc[3])
print("asserts passed (compared in user_id order; NULL in SQL equals NaN in pandas)")

# the all-NULL respondent
print("respondent 3 (all NULL): SQL (b) =", con.execute("SELECT * FROM (" + SQL_B.replace("ORDER BY user_id", "") + ") WHERE user_id = 3").fetchone()[1],
      "| pandas mean =", p_b.loc[3], "| sum(min_count=1) =", p_sum.loc[3])
print("total() and sum on all NULL:", con.execute("SELECT SUM(q1), TOTAL(q1) FROM survey WHERE user_id = 3").fetchone())
