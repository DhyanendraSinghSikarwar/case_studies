# Q24: string-to-date casting traps in SQLite and pandas.
import sqlite3
import warnings
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE raw_dates(id INTEGER PRIMARY KEY, d_text TEXT);
INSERT INTO raw_dates VALUES
 (1,'2024-03-05'),(2,'2024-3-5'),(3,'05/03/2024'),(4,'2024-03-05 14:30'),
 (5,'20240305'),(6,'2024-02-30'),(7,''),(8,NULL);
""")

print("DATE() per row:")
for r in con.execute("SELECT id, quote(d_text), DATE(d_text) FROM raw_dates ORDER BY id"): print("  ", r)
print("DATE of 2023-02-29 and 2024-04-31:", con.execute("SELECT DATE('2023-02-29'), DATE('2024-04-31')").fetchone())

print("other invalid shapes:", con.execute("SELECT DATE('2024-13-01'), DATE('2024-00-10'), DATE('2024-02-32')").fetchone())
sql_failed = "SELECT id FROM raw_dates WHERE DATE(d_text) IS NULL AND d_text <> '' ORDER BY id"
print("rows that failed to parse:", [r[0] for r in con.execute(sql_failed)])

# a strict round-trip check catches impossible dates that SQLite normalises (Feb 30 -> Mar 01)
sql_clean = """
SELECT id,
       CASE
         WHEN d_text GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]*'
              AND DATE(SUBSTR(d_text, 1, 10)) = SUBSTR(d_text, 1, 10)            THEN SUBSTR(d_text, 1, 10)
         WHEN d_text GLOB '[0-3][0-9]/[0-1][0-9]/[0-9][0-9][0-9][0-9]'
              AND DATE(SUBSTR(d_text,7,4)||'-'||SUBSTR(d_text,4,2)||'-'||SUBSTR(d_text,1,2))
                  = SUBSTR(d_text,7,4)||'-'||SUBSTR(d_text,4,2)||'-'||SUBSTR(d_text,1,2)
                                                                                THEN SUBSTR(d_text,7,4)||'-'||SUBSTR(d_text,4,2)||'-'||SUBSTR(d_text,1,2)
         WHEN d_text GLOB '[0-9][0-9][0-9][0-9][0-1][0-9][0-3][0-9]'
              AND DATE(SUBSTR(d_text,1,4)||'-'||SUBSTR(d_text,5,2)||'-'||SUBSTR(d_text,7,2))
                  = SUBSTR(d_text,1,4)||'-'||SUBSTR(d_text,5,2)||'-'||SUBSTR(d_text,7,2)
                                                                                THEN SUBSTR(d_text,1,4)||'-'||SUBSTR(d_text,5,2)||'-'||SUBSTR(d_text,7,2)
       END AS iso
FROM raw_dates ORDER BY id"""
sql_df = pd.read_sql(sql_clean, con)
print(sql_df.to_string(index=False))

# pandas
p = pd.read_sql("SELECT * FROM raw_dates ORDER BY id", con)
d = p["d_text"]
print("coerce (format inferred from first value):", pd.to_datetime(d, errors="coerce").dt.strftime("%Y-%m-%d").tolist())
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    mixed = pd.to_datetime(d, format="mixed", errors="coerce")
    print("format='mixed':", mixed.dt.strftime("%Y-%m-%d").tolist(), "| warnings:", [type(x).__name__ for x in w])
dayfirst = pd.to_datetime(d, format="mixed", dayfirst=True, errors="coerce")
print("format='mixed', dayfirst=True:", dayfirst.dt.strftime("%Y-%m-%d").tolist())
print("same string two ways:", pd.to_datetime("05/03/2024", format="%m/%d/%Y").date(), "vs", pd.to_datetime("05/03/2024", format="%d/%m/%Y").date())
try:
    pd.to_datetime(d.dropna(), format="%Y-%m-%d")
except Exception as e:
    print("errors='raise' (default):", type(e).__name__)

# explicit per-shape parsing, the same rules as the SQL CASE
iso = d.str.fullmatch(r"\d{4}-\d{2}-\d{2}( \d{2}:\d{2})?", na=False)
dmy = d.str.fullmatch(r"\d{2}/\d{2}/\d{4}", na=False)
compact = d.str.fullmatch(r"\d{8}", na=False)
parsed = pd.Series(pd.NaT, index=p.index, dtype="datetime64[ns]")
parsed[iso] = pd.to_datetime(d[iso].str[:10], format="%Y-%m-%d", errors="coerce")
parsed[dmy] = pd.to_datetime(d[dmy], format="%d/%m/%Y", errors="coerce")
parsed[compact] = pd.to_datetime(d[compact], format="%Y%m%d", errors="coerce")
pd_df = pd.DataFrame({"id": p["id"], "iso": parsed.dt.strftime("%Y-%m-%d")})
print(pd_df.to_string(index=False))

norm = lambda df: [tuple(None if pd.isna(v) else v for v in row) for row in df.itertuples(index=False)]
assert norm(sql_df) == norm(pd_df), (norm(sql_df), norm(pd_df))
print("asserts passed (SQL CASE parse == pandas per-shape parse, ordered by id)")
