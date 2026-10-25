# Q18: title case and initials in SQLite (no INITCAP) versus pandas
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, full_name TEXT);
INSERT INTO customers VALUES
 (1,'RAHUL sharma'),(2,'asha rao'),(3,'ASHA'),(4,'anil kumar singh'),
 (5,'mcDONALD'),(6,'de la cRUZ'),
 (7,'élodie dupont'),(8,'JOSÉ ruiz'),(9,'o''neil'),(10,NULL);
""")
print("SQLite", sqlite3.sqlite_version, "| pandas", pd.__version__)
print("UPPER('é') =", con.execute("SELECT UPPER('é')").fetchone()[0], "| LOWER('É') =", con.execute("SELECT LOWER('É')").fetchone()[0],
      "| UPPER('ß') =", con.execute("SELECT UPPER('ß')").fetchone()[0])
try:
    con.execute("SELECT INITCAP('abc')")
except sqlite3.Error as e:
    print("INITCAP ->", e)

# <<sql_1667
SQL_ONE_WORD = """
SELECT customer_id, UPPER(SUBSTR(full_name, 1, 1)) || LOWER(SUBSTR(full_name, 2)) AS name
FROM customers ORDER BY customer_id
"""
# >>
# <<sql_proper
SQL_PROPER = """
WITH RECURSIVE w(customer_id, rest, proper, initials) AS (
  SELECT customer_id, LTRIM(TRIM(full_name) || ' '), '', ''
  FROM customers WHERE full_name IS NOT NULL
  UNION ALL
  SELECT customer_id,
         LTRIM(SUBSTR(rest, INSTR(rest, ' ') + 1)),
         proper || CASE WHEN proper = '' THEN '' ELSE ' ' END
                || UPPER(SUBSTR(rest, 1, 1)) || LOWER(SUBSTR(rest, 2, INSTR(rest, ' ') - 2)),
         initials || UPPER(SUBSTR(rest, 1, 1)) || '.'
  FROM w WHERE rest <> ''
)
SELECT c.customer_id, c.full_name, w.proper AS proper_name, w.initials
FROM customers c LEFT JOIN w ON w.customer_id = c.customer_id AND w.rest = ''
ORDER BY c.customer_id
"""
# >>
one = pd.read_sql_query(SQL_ONE_WORD, con)
prop = pd.read_sql_query(SQL_PROPER, con)
print("\nLeetCode 1667 formula applied to every row (right only for one-word names):")
print(one.to_string(index=False))
print("\nrecursive CTE: proper case and initials:")
print(prop.to_string(index=False))

# <<pd
cust = pd.read_sql_query("SELECT * FROM customers ORDER BY customer_id", con)
p_one = cust["full_name"].str.capitalize()
p_title = cust["full_name"].str.title()
p_init = cust["full_name"].str.split().map(
    lambda ws: "".join(w[0].upper() + "." for w in ws) if isinstance(ws, list) else None)
# >>
out = pd.DataFrame({"full_name": cust["full_name"], "capitalize": p_one, "title": p_title, "initials": p_init})
print("\npandas str.capitalize, str.title and initials:")
print(out.to_string(index=False))
print("pandas dtype:", cust["full_name"].dtype, "| title of \"o'neil\":", pd.Series(["o'neil"]).str.title().tolist(),
      "| capitalize:", pd.Series(["o'neil"]).str.capitalize().tolist(), "| title of '3rd floor':", pd.Series(["3rd floor"]).str.title().tolist())

# comparisons: rows 1-6 are ASCII without apostrophes: SQL and pandas must agree (ordered by customer_id)
ascii_ids = [1, 2, 3, 4, 5, 6]
sql6 = prop[prop["customer_id"].isin(ascii_ids)].reset_index(drop=True)
pd6 = out.iloc[:6].reset_index(drop=True)
assert sql6["proper_name"].tolist() == pd6["title"].tolist()
assert sql6["initials"].tolist() == pd6["initials"].tolist()
assert one.loc[[2], "name"].tolist() == p_one.iloc[[2]].tolist() == ["Asha"]       # the one-word name
assert prop.loc[prop["customer_id"] == 10, "proper_name"].isna().all() and pd.isna(p_title.iloc[9])
# rows 7-9: they differ, and that is the point
diff = {i: (prop.loc[prop["customer_id"] == i, "proper_name"].iloc[0], p_title.iloc[i - 1]) for i in (7, 8, 9)}
print("\nSQL versus pandas title on the awkward rows (SQL, pandas):", diff)
assert diff[7][0] == "élodie Dupont" and diff[7][1] == "Élodie Dupont"
assert diff[8] == ("JosÉ Ruiz", "José Ruiz")
assert diff[9] == ("O'neil", "O'Neil")
print("asserts passed: rows 1-6 and the NULL row match; rows 7-9 differ as shown")

# extra edge rows: empty string, extra spaces, hyphen, apostrophe-s
con.executescript("CREATE TABLE c2(customer_id INTEGER PRIMARY KEY, full_name TEXT); "
                  "INSERT INTO c2 VALUES (1,''),(2,'  anil   kumar '),(3,'anne-marie'),(4,'it''s ok');")
e_sql = pd.read_sql_query(SQL_PROPER.replace("FROM customers c", "FROM c2 c").replace("FROM customers WHERE", "FROM c2 WHERE"), con)
e_pd = pd.read_sql_query("SELECT * FROM c2 ORDER BY customer_id", con)["full_name"]
print("\nextra rows, SQL proper_name:", e_sql["proper_name"].tolist(), "initials:", e_sql["initials"].tolist())
print("extra rows, pandas title   :", e_pd.str.title().tolist())
assert e_sql["proper_name"].tolist() == ["", "Anil Kumar", "Anne-marie", "It's Ok"]
assert e_pd.str.title().tolist() == ["", "  Anil   Kumar ", "Anne-Marie", "It'S Ok"]
print("asserts passed (extra rows)")
