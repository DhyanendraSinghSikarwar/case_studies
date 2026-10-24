# Q27: multi-column ranking with mixed directions (score DESC, attempts ASC, submitted_at ASC)
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE candidates(candidate_id INTEGER PRIMARY KEY, name TEXT, score INTEGER,
                        attempts INTEGER, submitted_at TEXT);
INSERT INTO candidates VALUES
 (1,'Asha',90,2,'2026-01-05'),(2,'Ben',90,1,'2026-01-06'),(3,'Chitra',90,1,'2026-01-04'),
 (4,'Dev',85,3,'2026-01-02'),(5,'Esha',85,3,'2026-01-02'),(6,'Farid',70,1,'2026-01-01');
"""
SQL_MAIN = """
SELECT candidate_id, name, score, attempts, submitted_at,
       DENSE_RANK() OVER (ORDER BY score DESC, attempts ASC, submitted_at ASC)               AS dense_pos,
       RANK()       OVER (ORDER BY score DESC, attempts ASC, submitted_at ASC)               AS rank_pos,
       ROW_NUMBER() OVER (ORDER BY score DESC, attempts ASC, submitted_at ASC, candidate_id) AS row_pos
FROM candidates
ORDER BY row_pos
"""
SQL_SCORE_ONLY = """
SELECT candidate_id, RANK() OVER (ORDER BY score DESC) AS rank_score_only
FROM candidates ORDER BY candidate_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL (ties broken for ROW_NUMBER by candidate_id):")
print(sql_df.to_string(index=False))
print("\nRANK on score only, for contrast:")
print(pd.read_sql_query(SQL_SCORE_ONLY, con).to_string(index=False))

# named window: a window that already has ORDER BY cannot be given another one
for label, q in [
    ("OVER (w ORDER BY candidate_id) where w has ORDER BY",
     "SELECT RANK() OVER (w ORDER BY candidate_id) FROM candidates WINDOW w AS (ORDER BY score DESC)"),
    ("OVER (w ORDER BY ...) where w has only PARTITION BY",
     "SELECT candidate_id, RANK() OVER (w ORDER BY score DESC) FROM candidates WINDOW w AS (PARTITION BY attempts)"),
]:
    try:
        n = len(con.execute(q).fetchall())
        print("named window OK  :", label, "->", n, "rows")
    except sqlite3.Error as ex:
        print("named window FAIL:", label, "->", ex)

cand = pd.read_sql_query("SELECT * FROM candidates", con)
# pd:main
keys = ["score", "attempts", "submitted_at"]
ordered = cand.sort_values(by=keys + ["candidate_id"], ascending=[False, True, True, True]).reset_index(drop=True)
ordered["row_pos"] = ordered.index + 1
ordered["dense_pos"] = ordered.groupby(keys, sort=False).ngroup() + 1
ordered["rank_pos"] = ordered.groupby(keys, sort=False)["row_pos"].transform("min")
# pd:end
# rank(method='first') on score alone is right only if the frame is first sorted by the other keys
by_rest = cand.sort_values(["attempts", "submitted_at", "candidate_id"])
first_pos = by_rest["score"].rank(method="first", ascending=False).astype(int)
print("\npandas:")
print(ordered.to_string(index=False))
# compared after sorting both by candidate_id
cols = ["candidate_id", "dense_pos", "rank_pos", "row_pos"]
a = sql_df[cols].sort_values("candidate_id").reset_index(drop=True)
b = ordered[cols].sort_values("candidate_id").reset_index(drop=True).astype("int64")
pd.testing.assert_frame_equal(a, b, check_dtype=False)
# the 'first' route: its ranks are by score only, so it differs where score ties exist
by_rest_df = pd.DataFrame({"candidate_id": by_rest["candidate_id"], "first_on_score_only": first_pos}).sort_values("candidate_id")
print("\nrank(method='first') on score alone after sorting by the other keys ascending:")
print(by_rest_df.to_string(index=False))
assert by_rest_df["first_on_score_only"].tolist() == a["row_pos"].tolist()
print("asserts passed: SQL == pandas for dense_pos, rank_pos, row_pos; 'first' route == row_pos")
