# Q25: search metrics: searches, CTR (searches with a click), zero-result rate, clicked position distribution
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE searches(search_id INTEGER PRIMARY KEY, user_id INTEGER, search_ts TEXT, query TEXT, result_count INTEGER);
CREATE TABLE clicks(click_id INTEGER PRIMARY KEY, search_id INTEGER, click_ts TEXT, position INTEGER);
INSERT INTO searches VALUES
 (1,1,'2024-03-01 09:00:00','shoes',   5),
 (2,2,'2024-03-01 09:05:00','shooes',  0),
 (3,3,'2024-03-01 10:00:00','bag',    10),
 (4,4,'2024-03-01 11:00:00','watch',   4),
 (5,1,'2024-03-02 09:00:00','phone',  20),
 (6,2,'2024-03-02 09:30:00','case',    3),
 (7,3,'2024-03-02 10:00:00','charger',NULL),
 (8,4,'2024-03-03 08:00:00','lamp',    6);
INSERT INTO clicks VALUES
 (1,1,'2024-03-01 09:00:10',1),(2,1,'2024-03-01 09:00:40',3),
 (3,4,'2024-03-01 11:00:05',2),
 (4,5,'2024-03-02 09:00:07',1),(5,5,'2024-03-02 09:00:30',12),
 (6,6,'2024-03-02 09:30:09',5);
"""

SQL_MAIN = """
WITH s AS (
  SELECT search_id, date(search_ts) AS d, result_count,
         EXISTS (SELECT 1 FROM clicks c WHERE c.search_id = searches.search_id) AS clicked
  FROM searches
)
SELECT d AS day,
       COUNT(*) AS searches,
       SUM(clicked) AS searches_with_click,
       ROUND(SUM(clicked) * 1.0 / COUNT(*), 2) AS ctr,
       SUM(result_count = 0) AS zero_result,
       ROUND(SUM(result_count = 0) * 1.0 / COUNT(*), 2) AS zero_result_rate
FROM s
GROUP BY d
ORDER BY d
"""
SQL_WRONG = """
SELECT date(s.search_ts) AS day,
       COUNT(*) AS searches_after_join,
       COUNT(DISTINCT s.search_id) AS searches_true,
       ROUND(COUNT(c.click_id) * 1.0 / COUNT(DISTINCT s.search_id), 2) AS clicks_over_searches,
       ROUND(COUNT(c.click_id) * 1.0 / COUNT(*), 2) AS click_rows_over_joined_rows
FROM searches s LEFT JOIN clicks c ON c.search_id = s.search_id
GROUP BY date(s.search_ts)
ORDER BY day
"""
SQL_POS = """
WITH b(bucket, ord) AS (VALUES ('1',1),('2',2),('3',3),('4-10',4),('11+',5)),
d AS (SELECT DISTINCT date(search_ts) AS day FROM searches),
k AS (
  SELECT date(s.search_ts) AS day,
         CASE WHEN c.position = 1 THEN '1' WHEN c.position = 2 THEN '2' WHEN c.position = 3 THEN '3'
              WHEN c.position BETWEEN 4 AND 10 THEN '4-10' ELSE '11+' END AS bucket
  FROM clicks c JOIN searches s ON s.search_id = c.search_id
)
SELECT d.day, b.bucket,
       (SELECT COUNT(*) FROM k WHERE k.day = d.day AND k.bucket = b.bucket) AS clicks,
       ROUND((SELECT COUNT(*) FROM k WHERE k.day = d.day AND k.bucket = b.bucket) * 100.0 /
             NULLIF((SELECT COUNT(*) FROM k WHERE k.day = d.day), 0), 2) AS pct_of_clicks
FROM d CROSS JOIN b
ORDER BY d.day, b.ord
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
sql_pos = pd.read_sql_query(SQL_POS, con)
print("SQL daily metrics:")
print(sql_main.to_string(index=False))
print("SQL wrong CTR (join first, count rows):")
print(pd.read_sql_query(SQL_WRONG, con).to_string(index=False))
print("SQL click position distribution:")
print(sql_pos.to_string(index=False))

searches = pd.read_sql_query("SELECT * FROM searches", con)
clicks = pd.read_sql_query("SELECT * FROM clicks", con)

# pd:main
def search_metrics(searches, clicks):
    s = searches.assign(day=searches["search_ts"].str[:10],
                        clicked=searches["search_id"].isin(clicks["search_id"]),
                        zero=searches["result_count"] == 0)
    daily = (s.groupby("day").agg(searches=("search_id", "size"), searches_with_click=("clicked", "sum"),
                                  zero_result=("zero", "sum")).reset_index())
    daily["ctr"] = (daily["searches_with_click"] / daily["searches"]).round(2)
    daily["zero_result_rate"] = (daily["zero_result"] / daily["searches"]).round(2)
    daily = daily[["day", "searches", "searches_with_click", "ctr", "zero_result", "zero_result_rate"]]

    k = clicks.merge(s[["search_id", "day"]], on="search_id")
    k["bucket"] = pd.cut(k["position"], bins=[0, 1, 2, 3, 10, 10**9],
                         labels=["1", "2", "3", "4-10", "11+"]).astype(str)
    grid = pd.MultiIndex.from_product([sorted(s["day"].unique()), ["1", "2", "3", "4-10", "11+"]],
                                      names=["day", "bucket"]).to_frame(index=False)
    cnt = k.groupby(["day", "bucket"]).size().rename("clicks").reset_index()
    pos = grid.merge(cnt, on=["day", "bucket"], how="left").fillna({"clicks": 0})
    pos["clicks"] = pos["clicks"].astype(int)
    total = pos.groupby("day")["clicks"].transform("sum")
    pos["pct_of_clicks"] = (pos["clicks"] * 100.0 / total.where(total != 0)).round(2)
    return daily, pos
# pd:end

pd_main, pd_pos = search_metrics(searches, clicks)
# both results are already in (day, bucket order) order, which matches the SQL ORDER BY
pd.testing.assert_frame_equal(pd_main, sql_main, check_dtype=False)
pd.testing.assert_frame_equal(pd_pos, sql_pos, check_dtype=False)
print("pandas daily:")
print(pd_main.to_string(index=False))
print("asserts passed")
