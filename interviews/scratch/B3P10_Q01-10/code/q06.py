# Q6: long to wide with MAX(CASE) for text answers; duplicates; pandas pivot vs pivot_table.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE answers(user_id INTEGER, question TEXT, answer TEXT);
INSERT INTO answers VALUES
 (1,'q1','Yes'),(1,'q2','No'),(1,'q3','Maybe'),
 (2,'q1','No'),(2,'q3','Yes'),
 (3,'q2','Maybe'),
 (4,'q1','No'),(4,'q1','Yes'),(4,'q2','Yes');   -- user 4 answered q1 twice (a data bug)
""")

sql_wide = """
SELECT user_id,
       MAX(CASE WHEN question = 'q1' THEN answer END) AS q1,
       MAX(CASE WHEN question = 'q2' THEN answer END) AS q2,
       MAX(CASE WHEN question = 'q3' THEN answer END) AS q3
FROM answers
GROUP BY user_id
ORDER BY user_id
"""
sql_dups = """
SELECT user_id, question, COUNT(*) AS n FROM answers GROUP BY user_id, question HAVING COUNT(*) > 1
"""
sql_min = sql_wide.replace("MAX(", "MIN(")

wide = pd.read_sql(sql_wide, con)
print(wide.to_string(index=False)); print()
print("duplicate (user, question) pairs:", con.execute(sql_dups).fetchall())
print("same query with MIN, user 4 q1:", pd.read_sql(sql_min, con).set_index("user_id").loc[4, "q1"],
      "(MAX gave", wide.set_index("user_id").loc[4, "q1"] + ")")

# pandas
answers = pd.read_sql("SELECT * FROM answers", con)
try:
    answers.pivot(index="user_id", columns="question", values="answer")
except ValueError as ex:
    print("\npivot with duplicates -> ValueError:", ex)

clean = answers[answers.user_id != 4]
p_clean = (clean.pivot(index="user_id", columns="question", values="answer")
           .reset_index().rename_axis(columns=None))
print("pivot on the clean rows:"); print(p_clean.to_string(index=False))

def pt(how):
    out = answers.pivot_table(index="user_id", columns="question", values="answer", aggfunc=how)
    return out.reset_index().rename_axis(columns=None)

p_first = pt("first")
p_max = pt("max")
print("\npivot_table aggfunc='first', user 4 q1:", p_first.set_index("user_id").loc[4, "q1"], "(first row in the data: 'No')")
print("pivot_table aggfunc='max',   user 4 q1:", p_max.set_index("user_id").loc[4, "q1"])

# compare after sorting by user_id; NULL in SQL = NaN in pandas
pd.testing.assert_frame_equal(wide, p_max, check_dtype=False)
assert not wide.equals(p_first)                       # 'first' and MAX disagree on user 4
print("columns.name after pivot (before rename_axis):", answers.pivot_table(
    index="user_id", columns="question", values="answer", aggfunc="max").columns.name)
print("user 3 has no q1 and no q3 -> missing cells:", wide.set_index("user_id").loc[3].tolist())
print("asserts passed (compared in user_id order)")
