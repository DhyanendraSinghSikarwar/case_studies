# Q25: NULL in DISTINCT, GROUP BY, UNION, INTERSECT, EXCEPT, COUNT(DISTINCT), joins and IN, with pandas equivalents.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE contacts_a(email TEXT);
CREATE TABLE contacts_b(email TEXT);
INSERT INTO contacts_a VALUES ('a@x.com'),('a@x.com'),(NULL),(NULL),('b@x.com');
INSERT INTO contacts_b VALUES ('a@x.com'),(NULL),('c@x.com'),(NULL);
""")
def run(q): return [r[0] for r in con.execute(q).fetchall()]
def one(q): return con.execute(q).fetchone()[0]

queries = {
 "distinct":     "SELECT DISTINCT email FROM contacts_a ORDER BY email",
 "group_by":     "SELECT email, COUNT(*) FROM contacts_a GROUP BY email ORDER BY email",
 "union":        "SELECT email FROM contacts_a UNION SELECT email FROM contacts_b ORDER BY 1",
 "union_all":    "SELECT email FROM contacts_a UNION ALL SELECT email FROM contacts_b ORDER BY 1",
 "intersect":    "SELECT email FROM contacts_a INTERSECT SELECT email FROM contacts_b ORDER BY 1",
 "except":       "SELECT email FROM contacts_a EXCEPT SELECT email FROM contacts_b ORDER BY 1",
 "not_in":       "SELECT DISTINCT email FROM contacts_a WHERE email NOT IN (SELECT email FROM contacts_b) ORDER BY 1",
 "join_eq":      "SELECT a.email FROM contacts_a a JOIN contacts_b b ON a.email = b.email ORDER BY 1",
 "join_isnd":    "SELECT a.email FROM contacts_a a JOIN contacts_b b ON a.email IS b.email ORDER BY 1",
 "in_subquery":  "SELECT email FROM contacts_a WHERE email IN (SELECT email FROM contacts_b) ORDER BY 1",
}
sql_res = {k: run(q) for k, q in queries.items()}
for k, v in sql_res.items(): print(f"{k:12}", v)
print("COUNT(*), COUNT(email), COUNT(DISTINCT email), DISTINCT rows:",
      con.execute("SELECT COUNT(*), COUNT(email), COUNT(DISTINCT email) FROM contacts_a").fetchone(), len(sql_res["distinct"]))
print("NULL = NULL:", one("SELECT NULL = NULL"), "| NULL IS NULL:", one("SELECT NULL IS NULL"),
      "| NULL IS DISTINCT FROM NULL:", one("SELECT NULL IS DISTINCT FROM NULL"))

# pandas (str dtype: missing is NaN)
a = pd.read_sql("SELECT email FROM contacts_a", con)["email"]
b = pd.read_sql("SELECT email FROM contacts_b", con)["email"]
def sort_nulls_first(s): return s.sort_values(na_position="first").tolist()
def lst(x): return [None if pd.isna(v) else v for v in x]
p_res = {
 "distinct":  lst(sort_nulls_first(a.drop_duplicates())),
 "union":     lst(sort_nulls_first(pd.concat([a, b]).drop_duplicates())),
 "union_all": lst(sort_nulls_first(pd.concat([a, b]))),
 "intersect": lst(sort_nulls_first(a.drop_duplicates()[a.drop_duplicates().isin(b)])),
 "except":    lst(sort_nulls_first(a.drop_duplicates()[~a.drop_duplicates().isin(b)])),
}
g = a.groupby(a, dropna=False).size()
p_res["group_by"] = sorted([(None if pd.isna(k) else k, int(v)) for k, v in g.items()], key=lambda t: (t[0] is not None, t[0] or ""))  # NULL group first, like SQLite
merged = a.to_frame().merge(b.to_frame(), on="email")                 # inner merge on the email key
p_res["join_eq"] = lst(sort_nulls_first(merged["email"]))
print("pandas merge on email returns", len(merged), "rows:", p_res["join_eq"], "(NaN keys matched each other)")
print("nunique default:", a.nunique(), "| nunique(dropna=False):", a.nunique(dropna=False),
      "| groupby groups: default", len(a.groupby(a).size()), "vs dropna=False", len(g))
print("isin NaN:", pd.Series([float("nan"), 1.0]).isin([float("nan")]).tolist(), "| ==:", (pd.Series([float("nan")]) == float("nan")).tolist())

sql_cmp = {k: ([(r[0], r[1]) for r in con.execute(queries[k]).fetchall()] if k == "group_by" else v) for k, v in sql_res.items()}
for k in p_res:
    if k == "join_eq": continue
    assert sql_cmp[k] == p_res[k], (k, sql_cmp[k], p_res[k])
assert one("SELECT COUNT(DISTINCT email) FROM contacts_a") == a.nunique() == 2
assert a.nunique(dropna=False) == len(sql_res["distinct"]) == 3
assert sql_res["join_eq"] == ["a@x.com", "a@x.com"] and p_res["join_eq"] != sql_res["join_eq"]   # pandas merge differs from SQL ON a.email = b.email
assert p_res["join_eq"] == sql_res["join_isnd"]                                                    # ...but matches the null-safe join (IS)
print("asserts passed (set operations and group counts equal; pandas merge equals the null-safe SQL join, not the = join; NULLs sorted first in both)")
