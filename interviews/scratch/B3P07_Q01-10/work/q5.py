# Q5: pandas run grouping, (s != s.shift()).cumsum(), vs the SQL LAG-flag version
import itertools
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE seq(pos INTEGER, status TEXT);
INSERT INTO seq VALUES (1,'up'),(2,'up'),(3,'down'),(4,'down'),(5,'down'),(6,'up');
CREATE TABLE ev(entity TEXT, ts INTEGER, status TEXT);
INSERT INTO ev VALUES
 ('A',1,'up'),('A',2,'up'),('A',3,'down'),('A',4,'down'),('A',5,'down'),('A',6,'up'),
 ('B',1,'up'),('B',2,'up'),('B',3,'down');
"""
SQL_MAIN = """
WITH x AS (
  SELECT pos, status,
         CASE WHEN status IS NOT LAG(status) OVER (ORDER BY pos) THEN 1 ELSE 0 END AS new_run
  FROM seq
),
y AS (
  SELECT pos, status, SUM(new_run) OVER (ORDER BY pos) AS run_id
  FROM x
)
SELECT run_id,
       MIN(status) AS status,
       MIN(pos)    AS first_pos,
       MAX(pos)    AS last_pos,
       COUNT(*)    AS run_len
FROM y
GROUP BY run_id
ORDER BY run_id
"""
SQL_ENTITY = """
WITH x AS (
  SELECT entity, ts, status,
         CASE WHEN status IS NOT LAG(status) OVER (PARTITION BY entity ORDER BY ts) THEN 1 ELSE 0 END AS new_run
  FROM ev
),
y AS (
  SELECT entity, ts, status,
         SUM(new_run) OVER (PARTITION BY entity ORDER BY ts) AS run_id
  FROM x
)
SELECT entity, run_id, MIN(status) AS status, MIN(ts) AS first_ts, MAX(ts) AS last_ts, COUNT(*) AS run_len
FROM y
GROUP BY entity, run_id
ORDER BY entity, run_id
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL LAG flag + running SUM:")
print(sql_df.to_string(index=False))

seq = pd.read_sql_query("SELECT * FROM seq", con)
# pd:main
s = seq.sort_values("pos")
run = (s["status"] != s["status"].shift()).cumsum()
pd_df = (s.groupby(run)
          .agg(status=("status", "first"), first_pos=("pos", "min"), last_pos=("pos", "max"), run_len=("pos", "size"))
          .rename_axis("run_id").reset_index())
# pd:end
print("\npandas run key:", run.tolist())
# compared in run_id order; run_id starts at 1 in pandas (cumsum of a True first flag) and at 1 in SQL
pd.testing.assert_frame_equal(pd_df, sql_df)
print("pandas equals SQL: True")
print("\ngroupby on the value itself:", seq.groupby("status").size().to_dict(), "(two separate up runs merged into one group of 3)")
print("itertools.groupby run lengths:", [(k, len(list(g))) for k, g in itertools.groupby(seq.sort_values("pos")["status"])])

# the first comparison is True because shift() puts NaN in front
print("first flag:", (s["status"] != s["status"].shift()).iloc[0], "| shift()[0]:", s["status"].shift().iloc[0])

# per entity
ev = pd.read_sql_query("SELECT * FROM ev", con)
sql_e = pd.read_sql_query(SQL_ENTITY, con)
e = ev.sort_values(["entity", "ts"])
wrong_run = (e["status"] != e["status"].shift()).cumsum()
print("\nwrong, global shift: runs by run key only ->", e.groupby(wrong_run).agg(n_rows=("ts", "size"), n_entities=("entity", "nunique")).to_dict("records"))
new_run = e["status"] != e.groupby("entity")["status"].shift()
e_run = new_run.groupby(e["entity"]).cumsum()
pd_e = (e.groupby(["entity", e_run])
         .agg(status=("status", "first"), first_ts=("ts", "min"), last_ts=("ts", "max"), run_len=("ts", "size"))
         .rename_axis(["entity", "run_id"]).reset_index())
pd.testing.assert_frame_equal(pd_e, sql_e)
print("per-entity pandas equals SQL (sorted by entity, run_id): True")
print(sql_e.to_string(index=False))

# NULL status: SQL IS NOT merges consecutive NULLs, pandas != does not
con.executescript("CREATE TABLE seqn(pos INTEGER, status TEXT); INSERT INTO seqn VALUES (1,'up'),(2,NULL),(3,NULL),(4,'up');")
sn = pd.read_sql_query("SELECT * FROM seqn", con)
sql_n = pd.read_sql_query(SQL_MAIN.replace("FROM seq", "FROM seqn"), con)
naive = (sn["status"] != sn["status"].shift()).cumsum()
both_na = sn["status"].isna() & sn["status"].shift().isna()
fixed = ((sn["status"] != sn["status"].shift()) & ~both_na).cumsum()
print("\nNULL,NULL in the middle: SQL run lengths", sql_n["run_len"].tolist(),
      "| pandas naive", sn.groupby(naive).size().tolist(),
      "| pandas fixed", sn.groupby(fixed).size().tolist())
assert sn.groupby(fixed).size().tolist() == sql_n["run_len"].tolist()
print("NaN != NaN:", bool(np.nan != np.nan), "| pandas Series:", (pd.Series([np.nan]) != pd.Series([np.nan])).tolist())

# integer states: shift upcasts to float64
st = pd.Series([1, 1, 0, 0, 1])
print("int Series shift dtype:", st.shift().dtype, "| shift(fill_value=-1) dtype:", st.shift(fill_value=-1).dtype,
      "| runs:", (st != st.shift()).cumsum().tolist())

# groupby drops NaN keys unless dropna=False
ev_nan = pd.concat([ev, pd.DataFrame({"entity": [None], "ts": [1], "status": ["up"]})], ignore_index=True)
print("groupby rows with a NULL entity: default", ev_nan.groupby("entity")["ts"].size().sum(),
      "| dropna=False", ev_nan.groupby("entity", dropna=False)["ts"].size().sum(), "| total rows", len(ev_nan))

# unsorted input, ties on the sort key, stability
rng = np.random.default_rng(0)
big = pd.DataFrame({"k": rng.integers(0, 5, 20000), "orig": np.arange(20000)})
default_order = big.sort_values("k")["orig"].to_numpy()
stable_order = big.sort_values("k", kind="stable")["orig"].to_numpy()
print("sort_values single column, default kind equals stable order on 20000 tied rows:", bool((default_order == stable_order).all()))
print("empty and single-row:", (pd.Series([], dtype=object) != pd.Series([], dtype=object).shift()).cumsum().tolist(),
      (pd.Series(["up"]) != pd.Series(["up"]).shift()).cumsum().tolist())
print("asserts passed")
