# Q19: EWMA and declining-balance depreciation with recursive CTEs, checked against pandas ewm and closed forms
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE daily_prices(day TEXT, close REAL);
INSERT INTO daily_prices VALUES
 ('2024-03-01',100),('2024-03-02',102),('2024-03-03',101),('2024-03-04',105),('2024-03-05',103),
 ('2024-03-06',108),('2024-03-07',110),('2024-03-08',107),('2024-03-11',111),('2024-03-12',115);
CREATE TABLE assets(asset_id INTEGER PRIMARY KEY, cost REAL, life_years INTEGER, rate REAL, salvage REAL);
INSERT INTO assets VALUES (1,10000,6,0.40,1000),(2,5000,3,0.25,500),(3,800,4,0.50,100);
"""
SQL_MAIN = """
WITH RECURSIVE p AS (
  SELECT day, close, ROW_NUMBER() OVER (ORDER BY day) AS rn FROM daily_prices
), s(rn, day, close, ewma) AS (
  SELECT rn, day, close, close FROM p WHERE rn = 1
  UNION ALL
  SELECT p.rn, p.day, p.close, 0.3 * p.close + (1 - 0.3) * s.ewma
  FROM s JOIN p ON p.rn = s.rn + 1
)
SELECT day, close, ewma FROM s ORDER BY rn
"""
SQL_DEPR = """
WITH RECURSIVE b(asset_id, year, book) AS (
  SELECT asset_id, 0, cost FROM assets
  UNION ALL
  SELECT b.asset_id, b.year + 1, MAX(a.salvage, b.book * (1 - a.rate))
  FROM b JOIN assets a ON a.asset_id = b.asset_id
  WHERE b.year < a.life_years
)
SELECT asset_id, year, ROUND(LAG(book) OVER (PARTITION BY asset_id ORDER BY year), 2) AS opening,
       ROUND(LAG(book) OVER (PARTITION BY asset_id ORDER BY year) - book, 2) AS depreciation,
       ROUND(book, 2) AS closing
FROM b
ORDER BY asset_id, year
"""
# closed forms: no recursion needed for either, shown to prove the recursion is not the only way
SQL_EWMA_CLOSED = """
WITH p AS (SELECT day, close, ROW_NUMBER() OVER (ORDER BY day) AS rn FROM daily_prices)
SELECT day, close,
       SUM(CASE WHEN rn = 1 THEN close / 0.7 ELSE 0.3 * close * power(0.7, -rn) END)
         OVER (ORDER BY rn ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) * power(0.7, rn) AS ewma
FROM p ORDER BY rn
"""
SQL_DEPR_CLOSED = """
WITH RECURSIVE y(asset_id, year) AS (
  SELECT asset_id, 0 FROM assets
  UNION ALL SELECT y.asset_id, y.year + 1 FROM y JOIN assets a ON a.asset_id = y.asset_id WHERE y.year < a.life_years
)
SELECT y.asset_id, y.year, ROUND(MAX(a.salvage, a.cost * power(1 - a.rate, y.year)), 2) AS closing
FROM y JOIN assets a ON a.asset_id = y.asset_id
WHERE y.year >= 1 ORDER BY y.asset_id, y.year
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
ew = pd.read_sql_query(SQL_MAIN, con)
dep = pd.read_sql_query(SQL_DEPR, con)
print("(a) EWMA, alpha 0.3, seed s_1 = x_1:")
print(ew.round(4).to_string(index=False))
print("(b) declining balance with a salvage floor (year 0 rows have no depreciation):")
print(dep.to_string(index=False))

prices = pd.read_sql_query("SELECT * FROM daily_prices", con)
assets = pd.read_sql_query("SELECT * FROM assets", con)

def pandas_side(prices, assets):
    # pd:main
    ewma = prices.sort_values("day")["close"].ewm(alpha=0.3, adjust=False).mean()
    rows = []
    for a in assets.itertuples():
        book = a.cost
        rows.append((a.asset_id, 0, np.nan, np.nan, book))
        for y in range(1, a.life_years + 1):
            new = max(a.salvage, book * (1 - a.rate))
            rows.append((a.asset_id, y, book, book - new, new))
            book = new
    depr = pd.DataFrame(rows, columns=["asset_id", "year", "opening", "depreciation", "closing"])
    return ewma, depr
    # pd:end

pd_ewma, pd_dep = pandas_side(prices, assets)
np.testing.assert_allclose(pd_ewma.to_numpy(), ew["ewma"].to_numpy(), rtol=0, atol=1e-9)
half_up = lambda col: np.floor(col * 100 + 0.5) / 100   # SQLite ROUND rounds halves away from zero (positive values here)
pd.testing.assert_frame_equal(pd_dep.assign(**{c: half_up(pd_dep[c]) for c in ("opening", "depreciation", "closing")}), dep, check_dtype=False)   # compared after sorting by asset_id, year
print("depreciation of asset 2, year 3 is exactly 703.125: SQLite ROUND gives", dep.loc[(dep.asset_id == 2) & (dep.year == 3), "depreciation"].iloc[0], "| pandas .round(2) gives", pd_dep.round(2).loc[(pd_dep.asset_id == 2) & (pd_dep.year == 3), "depreciation"].iloc[0], "(half to even)")
print("pandas ewm(alpha=0.3, adjust=False) equals the recursive CTE (atol 1e-9); depreciation loop equals SQL")

# conventions
adj = prices["close"].ewm(alpha=0.3, adjust=True).mean()
seed0 = [0.0]
for x in prices["close"]:
    seed0.append(0.3 * x + 0.7 * seed0[-1])
cmp = pd.DataFrame({"day": prices["day"], "recursive_seed_x1": ew["ewma"].round(4), "pandas_adjust_False": pd_ewma.round(4),
                    "pandas_adjust_True": adj.round(4), "seed_zero": np.round(seed0[1:], 4)})
print("conventions (first rows):")
print(cmp.head(4).to_string(index=False))
print("max abs difference adjust=True vs adjust=False over 10 rows:", round(float((adj - pd_ewma).abs().max()), 4), "| last row:", round(float((adj - pd_ewma).abs().iloc[-1]), 6))

# closed forms
cf = pd.read_sql_query(SQL_EWMA_CLOSED, con)
np.testing.assert_allclose(cf["ewma"].to_numpy(), ew["ewma"].to_numpy(), rtol=0, atol=1e-9)
dc = pd.read_sql_query(SQL_DEPR_CLOSED, con)
assert dc["closing"].tolist() == dep[dep.year >= 1]["closing"].tolist()
print("closed forms (weighted running SUM for EWMA, MAX(salvage, cost * (1-rate)^year) for depreciation) equal the recursive results")
# numerical limit of the EWMA closed form: power(0.7, -n) overflows
con.execute("CREATE TABLE long_p(day TEXT, close REAL)")
con.executemany("INSERT INTO long_p VALUES (?, ?)", [(f"{i:05d}", 100.0 + (i % 7)) for i in range(1, 2401)])
lp = pd.read_sql_query(SQL_EWMA_CLOSED.replace("daily_prices", "long_p"), con)
lr = pd.read_sql_query(SQL_MAIN.replace("daily_prices", "long_p"), con)
bad = lp["ewma"].isna() | ((lp["ewma"] - lr["ewma"]).abs() > 1e-6)
print("2400-row series: first row where the closed form is wrong or NULL:", int(bad.idxmax()) + 1 if bad.any() else None, "| recursive form fine to the end:", float(lr["ewma"].iloc[-1].round(4)))

# NULL close: SQL recursion carries the previous value; pandas ewm weights by position
con.execute("UPDATE daily_prices SET close = NULL WHERE day = '2024-03-05'")
sn = pd.read_sql_query(SQL_MAIN.replace("0.3 * p.close + (1 - 0.3) * s.ewma", "CASE WHEN p.close IS NULL THEN s.ewma ELSE 0.3 * p.close + (1 - 0.3) * s.ewma END"), con)
pn = pd.read_sql_query("SELECT * FROM daily_prices", con)["close"].ewm(alpha=0.3, adjust=False).mean()
pni = pd.read_sql_query("SELECT * FROM daily_prices", con)["close"].ewm(alpha=0.3, adjust=False, ignore_na=True).mean()
print("NULL close on 2024-03-05, rows 5 to 7: SQL carry-forward", sn["ewma"].round(4).tolist()[4:7], "| pandas default", pn.round(4).tolist()[4:7], "| pandas ignore_na=True", pni.round(4).tolist()[4:7])
print("empty prices ->", con.execute(SQL_MAIN.replace("FROM daily_prices", "FROM daily_prices WHERE 1 = 0")).fetchall())
print("asserts passed")
