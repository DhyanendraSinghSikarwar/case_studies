# Q35: hot streaks (>= 3 consecutive games with >= 30 points) per player, SQL + pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE games(player_id TEXT, game_no INTEGER, points INTEGER);
INSERT INTO games VALUES
 ('P1',8,36),('P1',1,35),('P1',2,30),('P1',3,41),('P1',4,10),('P1',5,32),('P1',6,33),('P1',7,34),
 ('P2',1,40),('P2',2,40),('P2',3,40),('P2',5,40),('P2',6,40),
 ('P3',1,40),
 ('P4',1,29),('P4',2,30),('P4',3,31),
 ('P5',1,30),('P5',2,30),('P5',3,30),
 ('P6',1,31),('P6',2,NULL),('P6',3,32),('P6',4,33),('P6',5,34),
 ('P7',1,35),('P7',2,35),('P7',2,35),('P7',3,35),
 ('P8',1,31),('P8',2,32),('P8',3,33),('P8',4,34);
"""
SQL_MAIN = """
WITH hot AS (
  SELECT DISTINCT player_id, game_no, points FROM games WHERE points >= 30
),
r AS (
  SELECT *, game_no - ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY game_no) AS k FROM hot
)
SELECT player_id, MIN(game_no) AS start_game, MAX(game_no) AS end_game,
       COUNT(*) AS length, ROUND(AVG(points), 2) AS avg_points
FROM r
GROUP BY player_id, k
HAVING COUNT(*) >= 3
ORDER BY player_id, start_game
"""
SQL_LONGEST = """
WITH s AS (""" + SQL_MAIN.replace("ORDER BY player_id, start_game", "") + """)
SELECT player_id, start_game, end_game, length FROM s
WHERE length = (SELECT MAX(length) FROM s)
ORDER BY player_id
"""
SQL_ROWORDER = """
WITH t AS (
  SELECT DISTINCT player_id, game_no, points FROM games
),
n AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY game_no) AS rn_all FROM t
),
h AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY game_no) AS rn_hot
  FROM n WHERE points >= 30
)
SELECT player_id, MIN(game_no) AS start_game, MAX(game_no) AS end_game, COUNT(*) AS length
FROM h
GROUP BY player_id, rn_all - rn_hot
HAVING COUNT(*) >= 3
ORDER BY player_id, start_game
"""
SQL_NODEDUP = SQL_MAIN.replace("SELECT DISTINCT player_id, game_no, points FROM games", "SELECT player_id, game_no, points FROM games")
SQL_GT30 = SQL_MAIN.replace("points >= 30", "points > 30")

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL hot streaks:"); print(sql_df.to_string(index=False))
longest = pd.read_sql_query(SQL_LONGEST, con)
print("longest hot streak (ties kept):"); print(longest.to_string(index=False))
print("wrong, row order instead of game_no (P2 merges across missing game 4):")
print(pd.read_sql_query(SQL_ROWORDER, con).to_string(index=False))
print("wrong, no DISTINCT (P7 duplicate game 2 splits the run):")
print(pd.read_sql_query(SQL_NODEDUP, con).to_string(index=False))
print("wrong, points > 30 (P5 with exactly 30 disappears):")
print(pd.read_sql_query(SQL_GT30, con)["player_id"].tolist())

games = pd.read_sql_query("SELECT * FROM games", con)
# pd:main
h = games[games["points"] >= 30].drop_duplicates()       # NaN >= 30 is False, so NULL points drop out
h = h.sort_values(["player_id", "game_no"])
h["k"] = h["game_no"] - (h.groupby("player_id").cumcount() + 1)
pd_df = (h.groupby(["player_id", "k"])
          .agg(start_game=("game_no", "min"), end_game=("game_no", "max"),
               length=("game_no", "size"), avg_points=("points", "mean")).reset_index())
pd_df = pd_df[pd_df["length"] >= 3].drop(columns="k")
pd_df["avg_points"] = pd_df["avg_points"].round(2)
pd_df = pd_df.sort_values(["player_id", "start_game"]).reset_index(drop=True)
pd_longest = pd_df[pd_df["length"] == pd_df["length"].max()][["player_id", "start_game", "end_game", "length"]]
# pd:end
print("pandas:"); print(pd_df.to_string(index=False))
# compare after sorting by player_id, start_game
assert pd_df.astype(sql_df.dtypes.to_dict()).equals(sql_df)
assert pd_longest.reset_index(drop=True).astype(longest.dtypes.to_dict()).equals(longest)
print("asserts passed")
