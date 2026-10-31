# Q7: LIKE, wildcards, ESCAPE, GLOB, case_sensitive_like; pandas str.contains.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO products VALUES
 (1,'100% Cotton'),(2,'cotton_blend'),(3,'Cotton Shirt'),(4,'COTTON'),(5,'pure cotton'),
 (6,'cotton blend'),(7,'cottonwood table'),(8,'1000 Cotton');
""")

def ids(where, params=()):
    return [r[0] for r in con.execute(f"SELECT product_id FROM products WHERE {where} ORDER BY product_id", params)]

sql = {
 "a_literal_percent":      r"name LIKE '%100\%%' ESCAPE '\'",
 "a_unescaped_percent":    "name LIKE '%100%%'",
 "a_backslash_no_escape":  r"name LIKE '%100\%%'",
 "b_literal_underscore":   r"name LIKE '%cotton\_blend%' ESCAPE '\'",
 "b_unescaped_underscore": "name LIKE '%cotton_blend%'",
 "c_like_default":         "name LIKE '%cotton%'",
 "c_glob":                 "name GLOB '*cotton*'",
 "d_prefix_or_word":       "name LIKE 'cotton%' OR name LIKE '% cotton%'",
 "d_whole_word":           "name LIKE 'cotton' OR name LIKE 'cotton %' OR name LIKE '% cotton' OR name LIKE '% cotton %'",
}
res = {k: ids(v) for k, v in sql.items()}
for k, v in res.items():
    print(f"{k:24s} {v}")

# PRAGMA case_sensitive_like is deprecated but works on 3.45.1: it changes LIKE for the whole connection
con.execute("PRAGMA case_sensitive_like = ON")
csl = ids("name LIKE '%cotton%'")
print("\nwith PRAGMA case_sensitive_like = ON, LIKE '%cotton%':", csl)
con.execute("PRAGMA case_sensitive_like = OFF")
print("after turning it OFF again:                       ", ids("name LIKE '%cotton%'"))

# an index on name is not used for a leading wildcard
con.execute("CREATE INDEX ix_name ON products(name)")
for label, where in (("name = 'COTTON'", "name = 'COTTON'"), ("LIKE '%cotton%'", "name LIKE '%cotton%'")):
    plan = [r[3] for r in con.execute(f"EXPLAIN QUERY PLAN SELECT * FROM products WHERE {where}")]
    print(f"plan for {label:16s}", plan)

# pandas: str.contains is regex and case-sensitive by default; regex=False for a literal
df = pd.read_sql("SELECT * FROM products ORDER BY product_id", con)
n = df["name"]
def pid(mask): return df.loc[mask, "product_id"].tolist()
p = {
 "a_literal_percent":    pid(n.str.contains("100%", regex=False)),
 "b_literal_underscore": pid(n.str.contains("cotton_blend", regex=False)),
 "b_unescaped_underscore": pid(n.str.contains("cotton.blend", regex=True)),
 "c_like_default":       pid(n.str.contains("cotton", case=False)),
 "c_glob":               pid(n.str.contains("cotton")),            # default: case-sensitive
 "d_prefix_or_word":     pid(n.str.contains(r"^cotton|\scotton", case=False)),
 "d_whole_word":         pid(n.str.contains(r"(?:^|\s)cotton(?:\s|$)", case=False)),
}
print("\npandas str.contains('100%') regex=True also works because % is not special:",
      pid(n.str.contains("100%")) == res["a_literal_percent"])
for k, v in p.items():
    print(f"pandas {k:24s} {v}")
for k, v in p.items():
    assert v == res[k], k
assert csl == res["c_glob"]            # case-sensitive LIKE equals GLOB here
assert res["a_unescaped_percent"] == [1, 8] and res["a_backslash_no_escape"] == []
assert 7 in res["c_like_default"] and 7 not in res["d_whole_word"]
print("asserts passed (id lists compared in product_id order)")
