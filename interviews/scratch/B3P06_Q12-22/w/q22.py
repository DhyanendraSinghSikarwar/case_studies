# Q22: Rising Temperature (LeetCode 197 pattern) with date gaps: self join, LAG, pandas asfreq / merge
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE weather(id INTEGER PRIMARY KEY, record_date TEXT, temperature INTEGER);
INSERT INTO weather VALUES
 (1,'2015-01-01',10),(2,'2015-01-02',25),(3,'2015-01-03',20),(4,'2015-01-04',30),
 (5,'2015-01-06',35),(6,'2015-01-07',40),
 (7,'2015-01-31',20),(8,'2015-02-01',25),
 (9,'2016-02-28',15),(10,'2016-02-29',18),(11,'2016-03-01',20);
"""
SQL_JOIN = """
SELECT w1.id
FROM weather w1
JOIN weather w2 ON w2.record_date = date(w1.record_date, '-1 day')
WHERE w1.temperature > w2.temperature
ORDER BY w1.id
"""
SQL_LAG_NAIVE = """
SELECT id FROM (
  SELECT id, temperature, LAG(temperature) OVER (ORDER BY record_date) AS prev_temp FROM weather
) WHERE temperature > prev_temp ORDER BY id
"""
SQL_LAG_CHECKED = """
SELECT id FROM (
  SELECT id, temperature, record_date,
         LAG(temperature) OVER (ORDER BY record_date) AS prev_temp,
         LAG(record_date) OVER (ORDER BY record_date) AS prev_date
  FROM weather
) WHERE temperature > prev_temp AND julianday(record_date) - julianday(prev_date) = 1
ORDER BY id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
join_ids = [r[0] for r in con.execute(SQL_JOIN)]
naive_ids = [r[0] for r in con.execute(SQL_LAG_NAIVE)]
checked_ids = [r[0] for r in con.execute(SQL_LAG_CHECKED)]
print("self join:", join_ids)
print("naive LAG:", naive_ids)
print("LAG + gap check:", checked_ids)
assert join_ids == checked_ids

weather = pd.read_sql_query("SELECT * FROM weather", con)
# pd:main
w = weather.assign(record_date=pd.to_datetime(weather["record_date"])).set_index("record_date").sort_index()
daily = w.asfreq("D")                                   # inserts NaN rows for missing calendar days
rising = daily["temperature"] > daily["temperature"].shift(1)
ids_asfreq = sorted(daily.loc[rising, "id"].astype(int).tolist())
prev = weather.assign(record_date=pd.to_datetime(weather["record_date"]) + pd.Timedelta(days=1))
ids_merge = sorted(weather.assign(record_date=pd.to_datetime(weather["record_date"]))
                   .merge(prev[["record_date", "temperature"]], on="record_date", suffixes=("", "_prev"))
                   .query("temperature > temperature_prev")["id"].tolist())
# pd:end
# compared as sorted id lists
assert ids_asfreq == join_ids and ids_merge == join_ids
print("pandas asfreq('D') + shift:", ids_asfreq)
print("pandas merge on date + 1 day:", ids_merge)
print("pandas naive shift on the raw sorted rows:",
      sorted(w.loc[w["temperature"] > w["temperature"].shift(1), "id"].tolist()))
print("asfreq rows:", len(daily), "of which missing days:", int(daily["id"].isna().sum()))
print("asserts passed")
