# Q2: islands of consecutive integers (LeetCode 1285 pattern): log_id - ROW_NUMBER, plus pandas twins
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logs(log_id INTEGER);
INSERT INTO logs VALUES (8),(1),(10),(3),(7),(2);
"""
SQL_MAIN = """
WITH x AS (
  SELECT log_id,
         log_id - ROW_NUMBER() OVER (ORDER BY log_id) AS grp
  FROM logs
  WHERE log_id IS NOT NULL
)
SELECT MIN(log_id) AS start_id,
       MAX(log_id) AS end_id,
       COUNT(*) AS cnt
FROM x
GROUP BY grp
ORDER BY start_id
"""
SQL_NO_FILTER = SQL_MAIN.replace("  WHERE log_id IS NOT NULL\n", "")
SQL_DISTINCT = SQL_MAIN.replace("FROM logs", "FROM (SELECT DISTINCT log_id FROM logs)")

def sql_islands(con, sql=SQL_MAIN):
    return pd.read_sql_query(sql, con)

def pd_islands(logs):
    # pd:main
    s = logs["log_id"].dropna().astype("int64").sort_values().reset_index(drop=True)
    grp = s - (s.index + 1)
    pd_df = (s.groupby(grp)
              .agg(start_id="min", end_id="max", cnt="size")
              .sort_values("start_id").reset_index(drop=True))
    # pd:end
    return pd_df

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = sql_islands(con)
print("SQL islands:")
print(sql_df.to_string(index=False))
logs = pd.read_sql_query("SELECT * FROM logs", con)
pd_df = pd_islands(logs)
# compared after sorting by start_id
pd.testing.assert_frame_equal(pd_df, sql_df)
print("pandas islands equal SQL islands: True")

# second pandas idiom: diff().ne(1).cumsum() as run key (diff is float64 because the first value is NaN)
s = logs["log_id"].sort_values().reset_index(drop=True)
print("diff dtype:", s.diff().dtype, "| first diff:", s.diff().iloc[0], "| first diff != 1:", bool(s.diff().iloc[0] != 1))
run = s.diff().ne(1).cumsum()
alt = s.groupby(run).agg(start_id="min", end_id="max", cnt="size").reset_index(drop=True)
pd.testing.assert_frame_equal(alt, sql_df)
print("diff().ne(1).cumsum() version equals SQL: True")

# edge: single row, empty table, NULL, duplicate id
con.execute("CREATE TABLE one(log_id INTEGER)")
con.execute("INSERT INTO one VALUES (42)")
print("single row:", con.execute(SQL_MAIN.replace("FROM logs", "FROM one")).fetchall())
con.execute("INSERT INTO logs VALUES (NULL)")
print("NULL row, filtered:", len(sql_islands(con)), "islands")
print("NULL row, no filter:")
print(sql_islands(con, SQL_NO_FILTER).to_string(index=False))
logs_n = pd.read_sql_query("SELECT * FROM logs", con)
print("pandas column dtype with a NULL:", logs_n["log_id"].dtype)
pd.testing.assert_frame_equal(pd_islands(logs_n), sql_df)
con.execute("INSERT INTO logs VALUES (2)")
print("duplicate id 2, no DISTINCT:")
print(sql_islands(con).to_string(index=False))
dist = sql_islands(con, SQL_DISTINCT)
pd.testing.assert_frame_equal(dist, sql_df)
print("with SELECT DISTINCT: equals the clean result")
con.execute("DELETE FROM logs")
print("empty table, SQL rows:", len(sql_islands(con)))
empty = pd_islands(pd.read_sql_query("SELECT * FROM logs", con))
print("empty table, pandas rows:", len(empty), "| columns:", list(empty.columns))
print("asserts passed")
