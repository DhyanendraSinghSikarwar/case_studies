# Q20: second highest DISTINCT search count per category and the terms at that rank, NULL if none
import sqlite3
import pandas as pd

def norm(df):
    return df.astype(object).where(df.notna(), None)

con = sqlite3.connect(":memory:")
con.executescript("CREATE TABLE searches(search_id INTEGER PRIMARY KEY, category TEXT, term TEXT);")
rows = []
sid = 0
for cat, term, n in [("shoes", "A", 5), ("shoes", "B", 5), ("shoes", "C", 3), ("shoes", "D", 3), ("shoes", "E", 1),
                     ("phones", "X", 4), ("phones", "Y", 2), ("books", "novel", 3)]:
    for _ in range(n):
        sid += 1
        rows.append((sid, cat, term))
con.executemany("INSERT INTO searches VALUES (?,?,?)", rows)

sql = """
WITH c AS (SELECT category, term, COUNT(*) AS n FROM searches GROUP BY category, term),
r AS (SELECT *, DENSE_RANK() OVER (PARTITION BY category ORDER BY n DESC) AS rk FROM c),
cats AS (SELECT DISTINCT category FROM searches)
SELECT cats.category, r.n AS second_count, r.term
FROM cats LEFT JOIN r ON r.category = cats.category AND r.rk = 2
ORDER BY cats.category, r.term
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))
print("\ninner-join version (drops books):", [r[0] for r in con.execute(sql.replace("LEFT JOIN r ON r.category = cats.category AND r.rk = 2", "JOIN r ON r.category = cats.category AND r.rk = 2"))])

s = pd.read_sql("SELECT * FROM searches", con)
c = s.groupby(["category", "term"]).size().rename("n").reset_index()
c["rk"] = c.groupby("category")["n"].rank(method="dense", ascending=False)
cats = c[["category"]].drop_duplicates()
second = c[c.rk == 2][["category", "n", "term"]].rename(columns={"n": "second_count"})
p = cats.merge(second, on="category", how="left").sort_values(["category", "term"]).reset_index(drop=True)
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(norm(a), norm(p), check_dtype=False)
print("\nassert passed: equal, rows ordered by category, term")
