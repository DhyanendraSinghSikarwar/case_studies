# Q39: FULL OUTER JOIN key columns: a.id and b.key are each NULL on one side; COALESCE, USING, pandas left_on/right_on vs on
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE a(id INTEGER, x TEXT);
CREATE TABLE b(key INTEGER, y INTEGER);
CREATE TABLE b2(id INTEGER, y INTEGER);          -- same data as b, key column renamed to id for USING
INSERT INTO a VALUES (1,'a1'),(2,'a2'),(3,'a3');
INSERT INTO b VALUES (2,20),(3,30),(4,40),(5,50);
INSERT INTO b2 SELECT key, y FROM b;
"""
SQL_RAW = "SELECT a.id, b.key, a.x, b.y FROM a FULL OUTER JOIN b ON a.id = b.key"
SQL_MAIN = """
SELECT COALESCE(a.id, b.key) AS id, a.x, b.y
FROM a FULL OUTER JOIN b ON a.id = b.key
ORDER BY id
"""
SQL_USING = "SELECT id, x, y FROM a FULL OUTER JOIN b2 USING (id) ORDER BY id"
SQL_GROUP_WRONG = """
SELECT a.id AS grp, COUNT(*) AS n_rows, SUM(b.y) AS sum_y
FROM a FULL OUTER JOIN b ON a.id = b.key GROUP BY a.id ORDER BY a.id
"""
SQL_GROUP_RIGHT = """
SELECT COALESCE(a.id, b.key) AS grp, COUNT(*) AS n_rows, SUM(b.y) AS sum_y
FROM a FULL OUTER JOIN b ON a.id = b.key GROUP BY COALESCE(a.id, b.key) ORDER BY grp
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
show = lambda q: print(pd.read_sql_query(q, con).to_string(index=False))
print("raw FULL JOIN, both key columns:"); show(SQL_RAW)
print("\nCOALESCE(a.id, b.key):"); show(SQL_MAIN)
print("\nUSING (id) on b2, SELECT id:"); show(SQL_USING)
print("\nGROUP BY a.id (wrong, right-only keys collapse into one NULL group):"); show(SQL_GROUP_WRONG)
print("\nGROUP BY COALESCE(a.id, b.key):"); show(SQL_GROUP_RIGHT)

# pandas
a = pd.read_sql_query("SELECT * FROM a", con)
b = pd.read_sql_query("SELECT * FROM b", con)
m_lr = a.merge(b, left_on="id", right_on="key", how="outer")
print("\npandas outer, left_on='id' right_on='key' (both columns kept):")
print(m_lr.to_string(index=False)); print("id and key dtypes:", m_lr[["id", "key"]].dtypes.astype(str).to_dict())
m_on = a.merge(b.rename(columns={"key": "id"}), on="id", how="outer")
print("\npandas outer, on='id' after renaming b.key to id (one coalesced column):")
print(m_on.to_string(index=False)); print("id dtype:", str(m_on["id"].dtype))

# the coalesced frame from left_on/right_on, and the group-by
m_lr["id"] = m_lr["id"].fillna(m_lr["key"])
p_main = m_lr[["id", "x", "y"]].sort_values("id").reset_index(drop=True)
sql_main = pd.read_sql_query(SQL_MAIN, con)
pd.testing.assert_frame_equal(sql_main, p_main.astype({"id": "int64", "y": "float64"}), check_dtype=False)
pd.testing.assert_frame_equal(sql_main, m_on[["id", "x", "y"]].sort_values("id").reset_index(drop=True), check_dtype=False)
lr = a.merge(b, left_on="id", right_on="key", how="outer")           # id still has NaN for right-only rows
agg = dict(n_rows=("y", "size"), sum_y=("y", lambda s: s.sum(min_count=1)))
print("\npandas groupby('id') on the uncoalesced column, default dropna=True (right-only rows vanish):")
print(lr.groupby("id").agg(**agg).reset_index().to_string(index=False))
print("pandas groupby('id', dropna=False) (the SQL-like NULL group):")
print(lr.groupby("id", dropna=False).agg(**agg).reset_index().to_string(index=False))
g_right = m_on.groupby("id").agg(**agg).reset_index()
print("\npandas groupby on the coalesced id:"); print(g_right.to_string(index=False))
sql_g = pd.read_sql_query(SQL_GROUP_RIGHT, con)
pd.testing.assert_frame_equal(sql_g.rename(columns={"grp": "id"}), g_right, check_dtype=False)
print("asserts passed: SQL == pandas (sorted by id)")
con.close()
