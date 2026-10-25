# Q5: unpivot survey columns: UNION ALL, CROSS JOIN over VALUES, pandas melt.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE survey(user_id INTEGER PRIMARY KEY, q1 INTEGER, q2 INTEGER, q3 INTEGER);
INSERT INTO survey VALUES (1,5,3,NULL),(2,NULL,NULL,NULL),(3,4,4,4),(4,2,NULL,5);
""")

sql_union_all = """
SELECT user_id, 'q1' AS question, q1 AS rating FROM survey WHERE q1 IS NOT NULL
UNION ALL
SELECT user_id, 'q2', q2 FROM survey WHERE q2 IS NOT NULL
UNION ALL
SELECT user_id, 'q3', q3 FROM survey WHERE q3 IS NOT NULL
ORDER BY question, user_id
"""
sql_cross = """
WITH qs(question) AS (VALUES ('q1'), ('q2'), ('q3')),
long AS (
  SELECT s.user_id, qs.question,
         CASE qs.question WHEN 'q1' THEN s.q1 WHEN 'q2' THEN s.q2 WHEN 'q3' THEN s.q3 END AS rating
  FROM survey s CROSS JOIN qs
)
SELECT user_id, question, rating FROM long WHERE rating IS NOT NULL
ORDER BY question, user_id
"""
# UNION (not ALL) over (user_id, rating) only: legitimate duplicates vanish
sql_union_bad = """
SELECT user_id, q1 AS rating FROM survey WHERE q1 IS NOT NULL
UNION SELECT user_id, q2 FROM survey WHERE q2 IS NOT NULL
UNION SELECT user_id, q3 FROM survey WHERE q3 IS NOT NULL
"""
sql_union_all_bad = sql_union_bad.replace("UNION SELECT", "UNION ALL SELECT")

a = pd.read_sql(sql_union_all, con)
b = pd.read_sql(sql_cross, con)
print(a.to_string(index=False)); print()
assert a.equals(b)
print("rows kept: UNION ALL %d, CROSS JOIN %d" % (len(a), len(b)))
print("UNION on (user_id, rating): %d rows; UNION ALL on the same: %d rows (user 3 gave 4,4,4)" % (
    len(con.execute(sql_union_bad).fetchall()), len(con.execute(sql_union_all_bad).fetchall())))
print("keeping unanswered rows: %d rows when the IS NOT NULL filter is dropped" % len(con.execute(
    sql_cross.replace("WHERE rating IS NOT NULL", "")).fetchall()))

for label, sql in (("UNION ALL", sql_union_all), ("CROSS JOIN", sql_cross)):
    plan = [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql)]
    print(label, "plan:", plan)

# pandas
survey = pd.read_sql("SELECT * FROM survey", con)
melted = survey.melt(id_vars="user_id", value_vars=["q1", "q2", "q3"], var_name="question", value_name="rating")
print("\nmelt keeps NaN rows:", len(melted), "rows; after dropna:", end=" ")
p = melted.dropna(subset=["rating"]).reset_index(drop=True)
print(len(p))
print("melt row order (before sorting): question blocks in column order, users inside each block")
print(melted.head(5).to_string(index=False))
p["rating"] = p["rating"].astype(int)
# compare after sorting by (question, user_id)
p = p.sort_values(["question", "user_id"]).reset_index(drop=True)
pd.testing.assert_frame_equal(a, p[["user_id", "question", "rating"]], check_dtype=False)
print("asserts passed (compared after sorting by question, user_id)")
