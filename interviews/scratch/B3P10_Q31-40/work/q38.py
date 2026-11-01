# Transpose a small matrix: unpivot (CROSS JOIN VALUES), then pivot (MAX CASE); pandas .T and stack/unstack.
import sqlite3
import warnings
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE kpis(metric TEXT, q1, q2, q3, q4);          -- no declared types: values keep their own type
INSERT INTO kpis VALUES ('revenue', 100, 120, 130, 150),
                        ('cost',     60,  70, NULL,  90),
                        ('rating',  4.5, 4.0, 4.2, 4.8);
""")

unpivot_sql = """
SELECT k.metric, q.quarter,
       CASE q.quarter WHEN 'q1' THEN k.q1 WHEN 'q2' THEN k.q2 WHEN 'q3' THEN k.q3 WHEN 'q4' THEN k.q4 END AS val
FROM kpis k CROSS JOIN (SELECT column1 AS quarter FROM (VALUES ('q1'),('q2'),('q3'),('q4'))) AS q"""
print(pd.read_sql(unpivot_sql + " ORDER BY k.metric, q.quarter", con).to_string(index=False))

transpose_sql = f"""
WITH long AS ({unpivot_sql})
SELECT quarter,
       MAX(CASE WHEN metric = 'revenue' THEN val END) AS revenue,
       MAX(CASE WHEN metric = 'cost'    THEN val END) AS cost,
       MAX(CASE WHEN metric = 'rating'  THEN val END) AS rating
FROM long GROUP BY quarter ORDER BY quarter"""
sql_t = pd.read_sql(transpose_sql, con)
print(sql_t.to_string(index=False))

# the UNION ALL spelling of the same unpivot gives the same rows
union_sql = ("SELECT metric,'q1' AS quarter,q1 AS val FROM kpis UNION ALL SELECT metric,'q2',q2 FROM kpis "
             "UNION ALL SELECT metric,'q3',q3 FROM kpis UNION ALL SELECT metric,'q4',q4 FROM kpis")
a = sorted(con.execute(unpivot_sql).fetchall(), key=lambda r: (r[0], r[1]))
b = sorted(con.execute(union_sql).fetchall(), key=lambda r: (r[0], r[1]))
assert a == b and len(a) == 12
print("typeof of the revenue/cost/rating cells in the long table:",
      con.execute(f"WITH long AS ({unpivot_sql}) SELECT metric, group_concat(DISTINCT typeof(val)) FROM long GROUP BY metric ORDER BY metric").fetchall())

# mixing types: a text value lands in the same output column as numbers
con.execute("INSERT INTO kpis VALUES ('status','ok','ok','late','ok')")
mixed = pd.read_sql(f"""WITH long AS ({unpivot_sql})
   SELECT quarter, MAX(CASE WHEN metric='revenue' THEN val END) AS revenue,
                   MAX(CASE WHEN metric='status'  THEN val END) AS status FROM long GROUP BY quarter ORDER BY quarter""", con)
print(mixed.to_string(index=False), "| pandas dtypes:", dict(mixed.dtypes.astype(str)))
print("what a single column mixing both gives for MAX:", con.execute(
    f"WITH long AS ({unpivot_sql}) SELECT MAX(val), MIN(val) FROM long WHERE quarter = 'q1'").fetchone(), "(text sorts above numbers)")
con.execute("DELETE FROM kpis WHERE metric = 'status'")

# ---- pandas
k = pd.read_sql("SELECT * FROM kpis", con)
t1 = k.set_index("metric").T.rename_axis(index="quarter", columns=None).reset_index()
with warnings.catch_warnings():
    warnings.simplefilter("error")                         # any deprecation warning would fail the run
    t2 = (k.set_index("metric").stack().unstack("metric")   # new stack keeps NaN rows
            .rename_axis(index="quarter", columns=None).reset_index())
cols = ["quarter", "revenue", "cost", "rating"]
t1, t2 = t1[cols], t2[cols]
print(t1.to_string(index=False))
for p in (t1, t2):
    pd.testing.assert_frame_equal(p.sort_values("quarter").reset_index(drop=True), sql_t, check_dtype=False)   # sorted by quarter
print("df.T dtypes:", dict(t1.dtypes.astype(str)))

# stack on a larger frame: future_stack default, legacy, and how to drop NaN
rng = np.random.default_rng(0)
big = pd.DataFrame(rng.normal(size=(1000, 4)), columns=list("abcd"))
big.iloc[::7, 1] = np.nan
big.iloc[::50, :] = np.nan
print("NaN cells:", int(big.isna().sum().sum()), "of", big.size)
print("stack() default      ->", big.stack().shape[0], "rows")
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    legacy = big.stack(future_stack=False)
print("stack(future_stack=False) ->", legacy.shape[0], "rows;", w[0].category.__name__ if w else "no warning")
print("stack().dropna()     ->", big.stack().dropna().shape[0], "rows (matches legacy:", big.stack().dropna().shape[0] == legacy.shape[0], ")")
try:
    big.stack(dropna=False)
except ValueError as e:
    print("stack(dropna=False) ->", e)
con.close()
print("asserts passed")
