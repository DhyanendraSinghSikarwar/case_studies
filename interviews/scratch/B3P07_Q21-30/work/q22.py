# Q22: longest winning streak (LeetCode 2173 pattern): running count of non-wins vs two ROW_NUMBERs, LEFT JOIN for zero-win players
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE matches(player_id INTEGER, match_day TEXT, result TEXT);
INSERT INTO matches VALUES
 (1,'2022-01-17','Win'),(1,'2022-01-18','Win'),(1,'2022-01-25','Win'),(1,'2022-01-31','Draw'),(1,'2022-02-08','Win'),
 (2,'2022-02-06','Lose'),(2,'2022-02-08','Lose'),
 (3,'2022-03-30','Win'),(3,'2022-03-01','Win'),(3,'2022-03-02','Lose'),(3,'2022-03-04','Win'),(3,'2022-03-05','Win'),(3,'2022-03-06','Win'),
 (4,'2022-04-01','Win'),
 (5,'2022-05-01','Win'),(5,'2022-05-02',NULL),(5,'2022-05-03','Win');
"""
SQL_MAIN = """
WITH players AS (
  SELECT DISTINCT player_id FROM matches
), r AS (
  SELECT player_id, match_day, result,
         SUM(result IS NOT 'Win') OVER (
           PARTITION BY player_id ORDER BY match_day
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS non_wins_so_far
  FROM matches
), streaks AS (
  SELECT player_id, non_wins_so_far, COUNT(*) AS streak_len
  FROM r
  WHERE result = 'Win'
  GROUP BY player_id, non_wins_so_far
)
SELECT p.player_id, COALESCE(MAX(s.streak_len), 0) AS longest_streak
FROM players p
LEFT JOIN streaks s ON s.player_id = p.player_id
GROUP BY p.player_id
ORDER BY p.player_id
"""
SQL_RN = """
WITH players AS (
  SELECT DISTINCT player_id FROM matches
), r AS (
  SELECT player_id, match_day, result,
         ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY match_day) AS rn_all,
         ROW_NUMBER() OVER (PARTITION BY player_id, result ORDER BY match_day) AS rn_res
  FROM matches
), streaks AS (
  SELECT player_id, rn_all - rn_res AS grp, COUNT(*) AS streak_len
  FROM r
  WHERE result = 'Win'
  GROUP BY player_id, rn_all - rn_res
)
SELECT p.player_id, COALESCE(MAX(s.streak_len), 0) AS longest_streak
FROM players p
LEFT JOIN streaks s ON s.player_id = p.player_id
GROUP BY p.player_id
ORDER BY p.player_id
"""
SQL_INNER = """
WITH r AS (
  SELECT player_id, match_day, result,
         SUM(result IS NOT 'Win') OVER (PARTITION BY player_id ORDER BY match_day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS g
  FROM matches
), streaks AS (SELECT player_id, g, COUNT(*) AS streak_len FROM r WHERE result = 'Win' GROUP BY player_id, g)
SELECT player_id, MAX(streak_len) AS longest_streak FROM streaks GROUP BY player_id ORDER BY player_id
"""
SQL_NEQ = """
WITH r AS (
  SELECT player_id, match_day, result,
         SUM(result <> 'Win') OVER (PARTITION BY player_id ORDER BY match_day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS g
  FROM matches
), streaks AS (SELECT player_id, g, COUNT(*) AS streak_len FROM r WHERE result = 'Win' GROUP BY player_id, g)
SELECT player_id, MAX(streak_len) AS longest_streak FROM streaks GROUP BY player_id ORDER BY player_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
m1 = pd.read_sql_query(SQL_MAIN, con)
m2 = pd.read_sql_query(SQL_RN, con)
print("method 1, running count of non-wins:")
print(m1.to_string(index=False))
print("method 2, two ROW_NUMBERs:")
print(m2.to_string(index=False))
assert m1.equals(m2)
print("wrong 1, INNER JOIN style (players 2 has no row):")
print(pd.read_sql_query(SQL_INNER, con).to_string(index=False))
print("wrong 2, result <> 'Win' with a NULL result (player 5 shows 2 instead of 1):")
print(pd.read_sql_query(SQL_NEQ, con).to_string(index=False))

matches = pd.read_sql_query("SELECT * FROM matches", con)
# pd:main
mm = matches.sort_values(["player_id", "match_day"]).reset_index(drop=True)
mm["is_win"] = mm["result"].eq("Win")
mm["non_wins_so_far"] = (~mm["is_win"]).astype(int).groupby(mm["player_id"]).cumsum()
runs = (mm[mm["is_win"]].groupby(["player_id", "non_wins_so_far"]).size()
          .groupby("player_id").max())
pd_df = (runs.reindex(mm["player_id"].unique(), fill_value=0)
             .rename_axis("player_id").rename("longest_streak").reset_index())
# pd:end
print("pandas:")
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(m1.sort_values("player_id").reset_index(drop=True),
                              pd_df.sort_values("player_id").reset_index(drop=True), check_dtype=False)  # sorted by player_id
print("asserts passed")
