# Q10: Human Traffic of Stadium (LeetCode 601 pattern): island, three-way self join, LAG/LEAD
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE stadium(id INTEGER PRIMARY KEY, visit_date TEXT, people INTEGER);
INSERT INTO stadium VALUES
 (5,'2017-01-05',145),(1,'2017-01-01',10),(2,'2017-01-02',109),(3,'2017-01-03',150),(4,'2017-01-04',99),
 (6,'2017-01-06',1455),(7,'2017-01-07',199),(8,'2017-01-09',188),(9,'2017-01-10',99),
 (10,'2017-01-11',100),(11,'2017-01-12',100),(12,'2017-01-13',100),(13,'2017-01-14',99);
"""
SQL_ISLAND = """
WITH q AS (
  SELECT id, visit_date, people,
         id - ROW_NUMBER() OVER (ORDER BY id) AS grp
  FROM stadium
  WHERE people >= 100
),
r AS (
  SELECT id, visit_date, people,
         COUNT(*) OVER (PARTITION BY grp) AS run_len
  FROM q
)
SELECT id, visit_date, people
FROM r
WHERE run_len >= 3
ORDER BY visit_date, id
"""
SQL_FILTER_AFTER = """
WITH q AS (
  SELECT id, visit_date, people,
         id - ROW_NUMBER() OVER (ORDER BY id) AS grp
  FROM stadium
),
r AS (
  SELECT id, visit_date, people,
         COUNT(*) OVER (PARTITION BY grp) AS run_len
  FROM q
  WHERE people >= 100
)
SELECT id, visit_date, people
FROM r
WHERE run_len >= 3
ORDER BY visit_date, id
"""
SQL_JOIN = """
SELECT DISTINCT t.id, t.visit_date, t.people
FROM stadium a
JOIN stadium b ON b.id = a.id + 1
JOIN stadium c ON c.id = a.id + 2
JOIN stadium t ON t.id IN (a.id, b.id, c.id)
WHERE a.people >= 100 AND b.people >= 100 AND c.people >= 100
ORDER BY t.visit_date, t.id
"""
SQL_JOIN_NO_DISTINCT = SQL_JOIN.replace("SELECT DISTINCT", "SELECT")
SQL_WINDOW = """
WITH x AS (
  SELECT id, visit_date, people,
         LAG(people, 2)  OVER (ORDER BY id) AS b2,
         LAG(people, 1)  OVER (ORDER BY id) AS b1,
         LEAD(people, 1) OVER (ORDER BY id) AS f1,
         LEAD(people, 2) OVER (ORDER BY id) AS f2
  FROM stadium
)
SELECT id, visit_date, people
FROM x
WHERE people >= 100
  AND ( (b1 >= 100 AND b2 >= 100)
     OR (b1 >= 100 AND f1 >= 100)
     OR (f1 >= 100 AND f2 >= 100) )
ORDER BY visit_date, id
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda sql: pd.read_sql_query(sql, con)
isl = q(SQL_ISLAND)
print("island method:"); print(isl.to_string(index=False))
jn, win = q(SQL_JOIN), q(SQL_WINDOW)
pd.testing.assert_frame_equal(jn, isl)
pd.testing.assert_frame_equal(win, isl)
print("\nself join and LAG/LEAD equal the island result: True")
print("join rows with DISTINCT:", len(jn), "| without DISTINCT:", len(q(SQL_JOIN_NO_DISTINCT)),
      "(ids 5-8 are a run of four: two triples share rows)")
print("island with the filter AFTER ROW_NUMBER (wrong):", q(SQL_FILTER_AFTER)["id"].tolist())

stadium = pd.read_sql_query("SELECT * FROM stadium", con)
def pd_traffic(stadium, respect_ids=False):
    # pd:main
    s = stadium.sort_values("id")
    ok = s["people"] >= 100
    key = (ok != ok.shift()).cumsum()
    if respect_ids:
        key = key + (s["id"].diff() != 1).cumsum()
    run_len = ok.groupby(key).transform("size")
    out = s[ok & (run_len >= 3)].sort_values(["visit_date", "id"]).reset_index(drop=True)
    # pd:end
    return out
# compared after sorting by visit_date, id
pd.testing.assert_frame_equal(pd_traffic(stadium), isl)
print("pandas equals SQL: True | ids:", pd_traffic(stadium)["id"].tolist())

# NULL people inside a run: unknown is not >= 100, so the run breaks
con.execute("CREATE TABLE s2 AS SELECT * FROM stadium")
con.execute("UPDATE s2 SET people = NULL WHERE id = 6")
sub = lambda sql: sql.replace("FROM stadium", "FROM s2").replace("JOIN stadium", "JOIN s2")
nul = q(sub(SQL_ISLAND))
print("\nNULL people at id 6, island:", nul["id"].tolist())
pd.testing.assert_frame_equal(q(sub(SQL_JOIN)), nul)
pd.testing.assert_frame_equal(q(sub(SQL_WINDOW)), nul)
s2 = pd.read_sql_query("SELECT * FROM s2", con)
print("pandas people dtype with a NULL:", s2["people"].dtype)
pd.testing.assert_frame_equal(pd_traffic(s2).astype({"people": "int64"}), nul)
print("NULL case: join, window and pandas agree with island: True (ids 5,7,8 do not form a run of 3)")

# gap in ids: delete id 6, so 5,7,8 are positionally adjacent but ids 5,7,8 are not consecutive
con.execute("CREATE TABLE s3 AS SELECT * FROM stadium WHERE id <> 6")
sub3 = lambda sql: sql.replace("FROM stadium", "FROM s3").replace("JOIN stadium", "JOIN s3")
s3 = pd.read_sql_query("SELECT * FROM s3", con)
print("\nid 6 deleted:")
print("  island (id arithmetic):", q(sub3(SQL_ISLAND))["id"].tolist(), "| self join:", q(sub3(SQL_JOIN))["id"].tolist())
print("  LAG/LEAD (positional):", q(sub3(SQL_WINDOW))["id"].tolist(), "| pandas positional:", pd_traffic(s3)["id"].tolist(),
      "| pandas respecting ids:", pd_traffic(s3, respect_ids=True)["id"].tolist())
assert q(sub3(SQL_ISLAND))["id"].tolist() == q(sub3(SQL_JOIN))["id"].tolist() == pd_traffic(s3, respect_ids=True)["id"].tolist()
assert q(sub3(SQL_WINDOW))["id"].tolist() == pd_traffic(s3)["id"].tolist()

# duplicate visit_date: ordering by visit_date alone would tie, so id is the tie-breaker
con.execute("CREATE TABLE s4 AS SELECT * FROM stadium")
con.execute("UPDATE s4 SET visit_date = '2017-01-06' WHERE id IN (5, 6, 7)")
sub4 = lambda sql: sql.replace("FROM stadium", "FROM s4").replace("JOIN stadium", "JOIN s4")
print("\nsame date 2017-01-06 on ids 5, 6, 7, ordered by visit_date, id:", q(sub4(SQL_ISLAND))["id"].tolist())

# single row and empty
con.execute("DELETE FROM s3")
con.execute("INSERT INTO s3 VALUES (1, '2017-01-01', 500)")
print("single qualifying row:", q(sub3(SQL_ISLAND))["id"].tolist())
con.execute("DELETE FROM s3")
print("empty table:", q(sub3(SQL_ISLAND))["id"].tolist())
print("asserts passed")
