# Q28: pandas reshaping (melt, wide_to_long, stack/unstack) compared with SQL UNION ALL unpivot and SUM(CASE) pivot.
import sqlite3
import warnings
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE scores_wide(student TEXT, math_2023 INTEGER, math_2024 INTEGER, sci_2023 INTEGER, sci_2024 INTEGER);
INSERT INTO scores_wide VALUES ('Zed',90,92,80,NULL),('Ana',70,NULL,65,66),('Mia',NULL,NULL,NULL,NULL);
""")

# SQL: unpivot with UNION ALL (keeps NULL scores, like melt)
sql_unpivot = """
SELECT student, 'math' AS subject, 2023 AS year, math_2023 AS score FROM scores_wide
UNION ALL SELECT student, 'math', 2024, math_2024 FROM scores_wide
UNION ALL SELECT student, 'sci',  2023, sci_2023  FROM scores_wide
UNION ALL SELECT student, 'sci',  2024, sci_2024  FROM scores_wide
ORDER BY student, subject, year"""
con.execute("CREATE TABLE scores_long AS " + sql_unpivot.replace("ORDER BY student, subject, year", ""))
u_sql = pd.read_sql(sql_unpivot, con)

# SQL: wide-to-long with one column per subject (what wide_to_long returns)
sql_w2l = """
SELECT student, 2023 AS year, math_2023 AS math, sci_2023 AS sci FROM scores_wide
UNION ALL SELECT student, 2024, math_2024, sci_2024 FROM scores_wide ORDER BY student, year"""
w2l_sql = pd.read_sql(sql_w2l, con)

# SQL: long-to-wide with SUM(CASE ...)
sql_pivot = """
SELECT student,
       SUM(CASE WHEN subject = 'math' AND year = 2023 THEN score END) AS math_2023,
       SUM(CASE WHEN subject = 'math' AND year = 2024 THEN score END) AS math_2024,
       SUM(CASE WHEN subject = 'sci'  AND year = 2023 THEN score END) AS sci_2023,
       SUM(CASE WHEN subject = 'sci'  AND year = 2024 THEN score END) AS sci_2024
FROM scores_long GROUP BY student ORDER BY student"""
piv_sql = pd.read_sql(sql_pivot, con)
print("SQL unpivot rows:", len(u_sql), "| NULL scores kept:", int(u_sql["score"].isna().sum()))

# pandas
wide = pd.read_sql("SELECT * FROM scores_wide", con)
long = wide.melt(id_vars="student", var_name="col", value_name="score")          # melt keeps NaN rows
long[["subject", "year"]] = long["col"].str.split("_", expand=True)
long["year"] = long["year"].astype(int)
long = long[["student", "subject", "year", "score"]].sort_values(["student", "subject", "year"]).reset_index(drop=True)
print("melt rows:", len(long), "| after dropna:", len(long.dropna(subset=["score"])))

w2l = (pd.wide_to_long(wide, stubnames=["math", "sci"], i="student", j="year", sep="_", suffix=r"\d+")
         .reset_index().sort_values(["student", "year"]).reset_index(drop=True))

back = long.set_index(["student", "subject", "year"])["score"].unstack(["subject", "year"]).sort_index(axis=1)
back.columns = [f"{s}_{y}" for s, y in back.columns]
print("unstack index order:", back.index.tolist(), "(sorted; input order was Zed, Ana, Mia)")
idx = long.set_index(["student", "subject", "year"])["score"]
print("unstack(fill_value=0), NaN stored in the rows (Mia):", idx.unstack(["subject", "year"], fill_value=0).loc["Mia"].tolist(), "(explicit NaN is not 'missing', so it stays)")
gap = idx.dropna().unstack(["subject", "year"], fill_value=0)
print("unstack(fill_value=0) after dropna: Mia is gone,", "Mia" in gap.index, "| Ana's missing cell becomes 0:"); print(gap.to_string())
print("column order here is order of first appearance, not sorted: add .sort_index(axis=1) ->", gap.sort_index(axis=1).columns.tolist())
back = back.reset_index()

# stack with the pandas 3 behaviour, on a larger frame (1000 rows x 6 columns, 143 NaN)
big = pd.DataFrame(np.arange(6000, dtype=float).reshape(1000, 6), columns=list("abcdef"))
big.iloc[::7, 2] = np.nan
print("NaN cells:", int(big.isna().sum().sum()))
print("stack() default      :", big.stack().shape, "(NaN kept)")
print("stack(future_stack=True):", big.stack(future_stack=True).shape)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    old = big.stack(future_stack=False)
    print("stack(future_stack=False):", old.shape, "(old behaviour drops NaN) | warning:", [x.category.__name__ for x in w])
try:
    big.stack(dropna=True)
except Exception as e:
    print("stack(dropna=True):", type(e).__name__, "-", str(e)[:60])
print("stack(...).dropna() shape:", big.stack().dropna().shape)

def norm(df): return [tuple(None if pd.isna(v) else (int(v) if isinstance(v, float) else v) for v in row) for row in df.itertuples(index=False)]
assert norm(u_sql) == norm(long)                          # ordered by student, subject, year; 12 rows incl. NaN
assert norm(w2l_sql) == norm(w2l[["student", "year", "math", "sci"]])
assert norm(piv_sql) == norm(back)                        # ordered by student
assert big.stack(future_stack=True).shape == big.stack().shape == (6000,) and old.shape == (5857,)
print("asserts passed (UNION ALL == melt, wide_to_long == 2-branch UNION ALL, SUM(CASE) == unstack; all ordered by student[, subject, year])")
con.close()
