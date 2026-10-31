# Q12: leaderboard with a full tie-breaker
import sqlite3
import pandas as pd

ROWS = [(1,'Asha',90,'2026-03-01'),(2,'Ben',90,'2026-02-01'),(3,'Chitra',90,'2026-02-01'),
        (4,'Dev',80,'2026-01-20'),(5,'Esha',80,'2026-01-05'),(6,'Farid',100,'2026-04-01')]
SCHEMA = "CREATE TABLE players(player_id INTEGER PRIMARY KEY, name TEXT, score INTEGER, last_updated TEXT);"
# score DESC, earlier last_updated first, then lower player_id
SQL_MAIN = """
SELECT player_id, name, score, last_updated,
       ROW_NUMBER() OVER (ORDER BY score DESC, last_updated, player_id) AS position
FROM players
ORDER BY position
"""
SQL_PARTIAL = """
SELECT player_id, ROW_NUMBER() OVER (ORDER BY score DESC) AS position
FROM players ORDER BY player_id
"""
SQL_RANK = """
SELECT player_id, RANK() OVER (ORDER BY score DESC) AS shared_pos
FROM players ORDER BY player_id
"""
def load(rows):
    con = sqlite3.connect(":memory:")
    con.execute(SCHEMA)
    con.executemany("INSERT INTO players VALUES (?,?,?,?)", rows)
    return con
con = load(ROWS)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\nscore-only ORDER BY, positions by player_id:", [r[1] for r in con.execute(SQL_PARTIAL)])
print("same query, rows inserted in reverse order:   ", [r[1] for r in load(ROWS[::-1]).execute(SQL_PARTIAL)])
print("RANK on score only, shared positions:         ", [r[1] for r in con.execute(SQL_RANK)])

players = pd.read_sql_query("SELECT * FROM players", con)
# pd:main
board = players.sort_values(["score", "last_updated", "player_id"], ascending=[False, True, True])
board = board.assign(position=range(1, len(board) + 1))
# pd:end
# pd:rank
alt = players.sort_values(["last_updated", "player_id"]).copy()
alt["position"] = alt["score"].rank(method="first", ascending=False).astype(int)
# pd:end
# compared in leaderboard order (position)
pd.testing.assert_frame_equal(sql_df, board.sort_values("position").reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(sql_df, alt.sort_values("position").reset_index(drop=True)[sql_df.columns], check_dtype=False)
print("\nasserts passed: SQL ROW_NUMBER == pandas sort_values + position == rank(method='first') after pre-sorting by the tie-breakers")
