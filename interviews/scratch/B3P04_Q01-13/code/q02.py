# Q2: ROW_NUMBER vs RANK vs DENSE_RANK on ties
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE scores(player_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO scores VALUES (1,100),(2,100),(3,90),(4,80);
"""
# tie-break for ROW_NUMBER stated: player_id ascending
SQL_MAIN = """
SELECT player_id, score,
       ROW_NUMBER() OVER (ORDER BY score DESC, player_id) AS row_num,
       RANK()       OVER (ORDER BY score DESC)            AS rnk,
       DENSE_RANK() OVER (ORDER BY score DESC)            AS dense_rnk
FROM scores
ORDER BY score DESC, player_id
"""
SQL_NOTIE = """
SELECT player_id, score, ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num
FROM scores
ORDER BY score DESC, player_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

scores = pd.read_sql_query("SELECT * FROM scores ORDER BY player_id", con)
# pd:main
pd_df = scores.assign(
    row_num=scores["score"].rank(method="first", ascending=False).astype(int),
    rnk=scores["score"].rank(method="min", ascending=False).astype(int),
    dense_rnk=scores["score"].rank(method="dense", ascending=False).astype(int),
)
# pd:end
# compared after sorting by score desc, player_id
pd_sorted = pd_df.sort_values(["score", "player_id"], ascending=[False, True]).reset_index(drop=True)
pd.testing.assert_frame_equal(sql_df, pd_sorted, check_dtype=False)

# without a tie-breaker: only the SET of numbers given to the tied pair is guaranteed
nt = pd.read_sql_query(SQL_NOTIE, con)
print("\nROW_NUMBER with ORDER BY score DESC only (which tied player gets 1 is not guaranteed):")
print(nt.to_string(index=False))
assert sorted(nt.loc[nt["score"] == 100, "row_num"]) == [1, 2]

# pandas 'first' follows row order, so it is deterministic only because the frame is in player_id order
rev = scores.iloc[::-1]
print("\npandas method='first' on the reversed frame gives the tied pair:",
      dict(zip(rev["player_id"], rev["score"].rank(method="first", ascending=False).astype(int)))
      | {})
print("asserts passed: SQL row_num/rnk/dense_rnk == pandas first/min/dense")
