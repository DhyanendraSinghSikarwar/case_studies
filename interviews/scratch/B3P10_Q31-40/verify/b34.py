# Parse log lines and key=value text with SUBSTR/INSTR, a recursive CTE, then the pandas version.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE logs(id INTEGER PRIMARY KEY, raw_line TEXT);
INSERT INTO logs VALUES
 (1,'2024-03-05 12:01:33 ERROR user=42 action=login ip=10.0.0.7'),
 (2,'2024-03-05 12:02:10 INFO user=7 action=view ip=10.0.0.8'),
 (3,'2024-03-05 12:03:00 ERROR action=login ip=10.0.0.9'),
 (4,'2024-03-05  12:04:05   ERROR  user=42   action=pay'),
 (5,NULL),
 (6,'2024-03-05 12:05:00 WARN user=9'),
 (7,'garbage line'),
 (8,'2024-03-05 12:06:00 ERROR user=abc action=x');
""")

parse_sql = """
WITH norm AS (                      -- collapse runs of spaces (3 passes handle runs up to 8) and trim
  SELECT id, raw_line,
         trim(replace(replace(replace(raw_line,'  ',' '),'  ',' '),'  ',' ')) AS s
  FROM logs
), p1 AS (
  SELECT id, raw_line, s,
         CASE WHEN substr(s,1,19) GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
              THEN substr(s,21) END AS after_ts                       -- NULL when the prefix is not a timestamp
  FROM norm
), p2 AS (
  SELECT id, raw_line, s, after_ts,
         substr(after_ts, 1, instr(after_ts || ' ', ' ') - 1) AS level,
         CASE WHEN instr(s, ' user=') > 0 THEN substr(s, instr(s, ' user=') + 6) END AS user_rest,
         CASE WHEN instr(s, ' action=') > 0 THEN substr(s, instr(s, ' action=') + 8) END AS action_rest
  FROM p1
)
SELECT id,
       level,
       substr(user_rest, 1, instr(user_rest || ' ', ' ') - 1)       AS user_txt,
       substr(action_rest, 1, instr(action_rest || ' ', ' ') - 1)   AS action,
       CASE WHEN raw_line IS NULL THEN 'null line'
            WHEN after_ts IS NULL OR level NOT IN ('ERROR','WARN','INFO') THEN 'unreadable'
            WHEN user_rest IS NOT NULL AND (substr(user_rest, 1, instr(user_rest || ' ', ' ') - 1) = ''
                 OR substr(user_rest, 1, instr(user_rest || ' ', ' ') - 1) GLOB '*[^0-9]*') THEN 'bad user'
            ELSE 'ok' END AS status
FROM p2 ORDER BY id"""
sql_parsed = pd.read_sql(parse_sql, con)
print(sql_parsed.to_string(index=False))

con.execute("CREATE TEMP TABLE parsed AS " + parse_sql)
print(con.execute("SELECT level, COUNT(*) FROM parsed WHERE status IN ('ok','bad user') GROUP BY level ORDER BY level").fetchall())
print("distinct users with an ERROR line:", con.execute(
    "SELECT COUNT(DISTINCT user_txt) FROM parsed WHERE level='ERROR' AND status='ok' AND user_txt IS NOT NULL").fetchone()[0])
print("lines the parser could not read:", con.execute(
    "SELECT id, status FROM parsed WHERE status <> 'ok' ORDER BY id").fetchall())
print("rows in = rows out:", con.execute("SELECT (SELECT COUNT(*) FROM logs), (SELECT COUNT(*) FROM parsed)").fetchone())

# ---- pandas: extract with named groups
logs = pd.read_sql("SELECT * FROM logs", con)
raw = logs["raw_line"]
head = raw.str.extract(r"^(?P<ts>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(?P<level>[A-Z]+)\b")
user = raw.str.extract(r"\buser=(?P<user_txt>\S*)")
act = raw.str.extract(r"\baction=(?P<action>\S+)")
p = pd.concat([logs["id"], head["level"], user, act], axis=1)
p["level"] = p["level"].where(p["level"].isin(["ERROR", "WARN", "INFO"]))
ok = p["level"].notna()
bad_user = p["user_txt"].notna() & ~p["user_txt"].fillna("").str.fullmatch(r"\d+")
p["status"] = np.select([raw.isna(), ~ok, bad_user], ["null line", "unreadable", "bad user"], default="ok")
print(p.to_string(index=False))
a = sql_parsed.fillna("<NA>").astype(str).reset_index(drop=True)
b = p[["id", "level", "user_txt", "action", "status"]].fillna("<NA>").astype(str).reset_index(drop=True)
# SQL gives NULL level for the null line; the unreadable row 7 has level 'garbage' in SQL only if after_ts passed (it did not)
a["id"] = a["id"].astype(int); b["id"] = b["id"].astype(int)
pd.testing.assert_frame_equal(a, b)           # compared in id order

# ---- generalise: key=value;key=value text -> (key, value) rows -> columns
con.executescript("""
CREATE TABLE attrs(id INTEGER PRIMARY KEY, txt TEXT);
INSERT INTO attrs VALUES (1,'user=42;action=login;ip=10.0.0.7'),(2,'user=7;action=view'),
                         (3,'action=pay;note=a=b;'),(4,NULL),(5,'');
""")
kv_sql = """
WITH RECURSIVE split(id, key_val, rest) AS (
  SELECT id, NULL, txt || ';' FROM attrs WHERE txt IS NOT NULL          -- NULL txt produces no rows
  UNION ALL
  SELECT id, substr(rest, 1, instr(rest, ';') - 1), substr(rest, instr(rest, ';') + 1)
  FROM split WHERE rest <> ''
), kv AS (
  SELECT id, substr(key_val, 1, instr(key_val, '=') - 1) AS k, substr(key_val, instr(key_val, '=') + 1) AS v
  FROM split WHERE key_val IS NOT NULL AND instr(key_val, '=') > 0     -- empty pieces and pieces without '=' dropped
)
SELECT id, k, v FROM kv ORDER BY id, k"""
sql_kv = pd.read_sql(kv_sql, con)
print(sql_kv.to_string(index=False))
wide_sql = f"""
WITH RECURSIVE split(id, key_val, rest) AS (
  SELECT id, NULL, txt || ';' FROM attrs WHERE txt IS NOT NULL
  UNION ALL
  SELECT id, substr(rest, 1, instr(rest, ';') - 1), substr(rest, instr(rest, ';') + 1) FROM split WHERE rest <> ''
), kv AS (
  SELECT id, substr(key_val, 1, instr(key_val, '=') - 1) AS k, substr(key_val, instr(key_val, '=') + 1) AS v
  FROM split WHERE key_val IS NOT NULL AND instr(key_val, '=') > 0
)
SELECT a.id,
       MAX(CASE WHEN k = 'user'   THEN v END) AS user,
       MAX(CASE WHEN k = 'action' THEN v END) AS action,
       MAX(CASE WHEN k = 'ip'     THEN v END) AS ip,
       MAX(CASE WHEN k = 'note'   THEN v END) AS note
FROM attrs a LEFT JOIN kv ON kv.id = a.id
GROUP BY a.id ORDER BY a.id"""
sql_wide = pd.read_sql(wide_sql, con)
print(sql_wide.to_string(index=False))

at = pd.read_sql("SELECT * FROM attrs", con)
long = (at.assign(pair=at["txt"].str.split(";")).explode("pair")
          .dropna(subset=["pair"]))
long = long[long["pair"].str.contains("=", regex=False)]
long[["k", "v"]] = long["pair"].str.split("=", n=1, expand=True)
p_kv = long[["id", "k", "v"]].sort_values(["id", "k"]).reset_index(drop=True)
pd.testing.assert_frame_equal(p_kv, sql_kv.sort_values(["id", "k"]).reset_index(drop=True), check_dtype=False)
p_wide = (long.pivot(index="id", columns="k", values="v")
              .reindex(index=at["id"], columns=["user", "action", "ip", "note"]).reset_index().rename_axis(columns=None))
pd.testing.assert_frame_equal(p_wide.astype(object).where(p_wide.notna(), None),
                              sql_wide.astype(object).where(sql_wide.notna(), None), check_dtype=False)
print(p_wide.to_string(index=False))

# counting a substring: SQL length/replace trick versus str.count (regex, non-overlapping)
print("SQL count of 'aa' in 'aaa':", con.execute("SELECT (length('aaa') - length(replace('aaa','aa',''))) / length('aa')").fetchone()[0],
      "| pandas str.count:", pd.Series(["aaa"]).str.count("aa")[0],
      "| '=' per attrs line (pandas):", at["txt"].str.count("=").tolist())
con.close()
print("asserts passed")
