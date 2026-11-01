# Q11: split a comma-separated column into rows (recursive CTE) and count orders per tag
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders_tags(order_id INTEGER PRIMARY KEY, tags TEXT);
INSERT INTO orders_tags VALUES
 (1,'red,blue,sale'),
 (2,'red, sale'),
 (3,NULL),
 (4,''),
 (5,'a,,b'),
 (6,'sale,sale');
""")

# <<sql_split
SQL_SPLIT = """
WITH RECURSIVE s(order_id, pos, tag, rest) AS (
  SELECT order_id, 0, NULL, tags || ','          -- append a delimiter so the last element is cut like the others
  FROM orders_tags WHERE tags IS NOT NULL
  UNION ALL
  SELECT order_id, pos + 1,
         TRIM(SUBSTR(rest, 1, INSTR(rest, ',') - 1)),
         SUBSTR(rest, INSTR(rest, ',') + 1)
  FROM s WHERE rest <> ''
)
SELECT o.order_id, s.tag, s.pos AS position
FROM orders_tags o LEFT JOIN s ON s.order_id = o.order_id AND s.pos > 0
ORDER BY o.order_id, s.pos
"""
# >>
# <<sql_drop
SQL_SPLIT_CLEAN = """
WITH RECURSIVE s(order_id, pos, tag, rest) AS (
  SELECT order_id, 0, NULL, tags || ',' FROM orders_tags WHERE tags IS NOT NULL
  UNION ALL
  SELECT order_id, pos + 1, TRIM(SUBSTR(rest, 1, INSTR(rest, ',') - 1)), SUBSTR(rest, INSTR(rest, ',') + 1)
  FROM s WHERE rest <> ''
)
SELECT order_id, tag, pos AS position FROM s WHERE pos > 0 AND tag <> '' ORDER BY order_id, pos
"""
# >>
# <<sql_count
SQL_COUNT = """
WITH RECURSIVE s(order_id, pos, tag, rest) AS (
  SELECT order_id, 0, NULL, tags || ',' FROM orders_tags WHERE tags IS NOT NULL
  UNION ALL
  SELECT order_id, pos + 1, TRIM(SUBSTR(rest, 1, INSTR(rest, ',') - 1)), SUBSTR(rest, INSTR(rest, ',') + 1)
  FROM s WHERE rest <> ''
)
SELECT tag, COUNT(DISTINCT order_id) AS orders, COUNT(*) AS mentions
FROM s WHERE pos > 0 AND tag <> ''
GROUP BY tag ORDER BY orders DESC, tag
"""
# >>

sql_all = pd.read_sql_query(SQL_SPLIT, con)
print("SQL, every order kept (NULL tag = NULL or missing list; '' = empty element):")
print(sql_all.to_string(index=False))
sql_clean = pd.read_sql_query(SQL_SPLIT_CLEAN, con)
print("\nSQL, empty and NULL dropped deliberately:")
print(sql_clean.to_string(index=False))
sql_cnt = pd.read_sql_query(SQL_COUNT, con)
print("\nSQL, orders per tag:")
print(sql_cnt.to_string(index=False))

# <<pd_split
def split_tags(df):
    t = df.assign(tag=df["tags"].str.split(",")).explode("tag")     # one row per element; NaN and '' survive
    t["tag"] = t["tag"].str.strip()
    t["position"] = t.groupby("order_id").cumcount() + 1
    return t[["order_id", "tag", "position"]]
# >>
raw = pd.read_sql_query("SELECT * FROM orders_tags", con)
p_all = split_tags(raw)
print("\npandas str.split + explode (raw):")
print(p_all.to_string(index=False))
print("tags dtype:", raw["tags"].dtype, "| NaN row after explode:", p_all.loc[p_all["order_id"] == 3, "tag"].tolist())

# <<pd_clean
p_clean = p_all[p_all["tag"].notna() & (p_all["tag"] != "")].reset_index(drop=True)
p_cnt = (p_clean.groupby("tag")
         .agg(orders=("order_id", "nunique"), mentions=("order_id", "size"))
         .reset_index().sort_values(["orders", "tag"], ascending=[False, True]).reset_index(drop=True))
# >>

# Comparison rows: order_id, position (both sorted by order_id, position).
# SQL keeps NULL for order 3; pandas keeps NaN. Map NaN -> None to compare the all-rows version.
a = sql_all.copy()
b = p_all.copy()
b["position"] = b["position"].astype("float")
a["position"] = a["position"].astype("float")
# SQL gives NULL position for the NULL-tags order; pandas numbers it 1. Align by design: set both to NaN there.
b.loc[b["tag"].isna(), "position"] = np.nan
pd.testing.assert_frame_equal(a.reset_index(drop=True), b.reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(sql_clean, p_clean, check_dtype=False)
pd.testing.assert_frame_equal(sql_cnt, p_cnt, check_dtype=False)
print("\nasserts passed: all-rows, cleaned rows and per-tag counts match (sorted by order_id, position / orders desc, tag)")

# trap: no trailing delimiter appended -> the last element is lost
bad = con.execute("""
WITH RECURSIVE s(order_id, pos, tag, rest) AS (
  SELECT order_id, 0, NULL, tags FROM orders_tags WHERE order_id = 1
  UNION ALL
  SELECT order_id, pos + 1, SUBSTR(rest, 1, INSTR(rest, ',') - 1), SUBSTR(rest, INSTR(rest, ',') + 1)
  FROM s WHERE INSTR(rest, ',') > 0
) SELECT tag FROM s WHERE pos > 0""").fetchall()
print("without appending ',' (order 1):", [r[0] for r in bad], "-> 'sale' is lost")
print("explode on NaN/'':", pd.Series([np.nan, "", "a,b"]).str.split(",").explode().tolist())
