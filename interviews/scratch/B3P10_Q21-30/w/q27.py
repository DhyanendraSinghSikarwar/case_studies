# Q27: crosstab percentages (row, column, grand) in SQLite versus pandas.crosstab(normalize=...).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales(region TEXT, product TEXT, amount REAL);
INSERT INTO sales VALUES
 ('East','A',4),('East','A',6),('East','B',10),('East','C',10),      -- East: 10 / 10 / 10
 ('South','A',10),('South','B',10),('South','C',40),                 -- South: 10 / 10 / 40
 ('West','A',10),('West','C',30),                                    -- West has no B row
 ('North','A',0),('North','B',0),('North','C',0);                    -- North totals zero
""")

# one long CTE gives every cell its row total, column total and grand total; the outer query pivots one measure
def pivot_sql(measure):
    cols = ",\n       ".join(
        f"ROUND(SUM(CASE WHEN product = '{p}' THEN {measure} END), 1) AS {p.lower()}" for p in "ABC")
    return f"""
WITH cell AS (SELECT region, product, SUM(amount) AS amt FROM sales GROUP BY region, product),
m AS (
  SELECT region, product, amt,
         100.0 * amt / NULLIF(SUM(amt) OVER (PARTITION BY region), 0)  AS row_pct,
         100.0 * amt / NULLIF(SUM(amt) OVER (PARTITION BY product), 0) AS col_pct,
         100.0 * amt / NULLIF((SELECT SUM(amount) FROM sales), 0)     AS grand_pct
  FROM cell)
SELECT region,
       {cols}
FROM m GROUP BY region ORDER BY region"""

sql = {k: pivot_sql(k) for k in ("row_pct", "col_pct", "grand_pct")}
sql_df = {k: pd.read_sql(q, con).set_index("region") for k, q in sql.items()}
for k, v in sql_df.items():
    print(k); print(v.to_string())
print("row_pct row sums:", sql_df["row_pct"].sum(axis=1).round(2).to_dict())
print("col_pct col sums:", sql_df["col_pct"].sum(axis=0).round(2).to_dict(), "| grand_pct total:", round(float(sql_df["grand_pct"].sum().sum()), 2))
print("without NULLIF, North row_pct in SQLite:", con.execute("SELECT 100.0 * 0 / 0").fetchone()[0], "(division by zero gives NULL in SQLite)")
print("unrounded East row shares:", [round(100 * x / 30, 4) for x in (10, 10, 10)], "-> 33.3 * 3 =", round(33.3 * 3, 1))

# pandas
s = pd.read_sql("SELECT * FROM sales", con)
args = dict(index=s["region"], columns=s["product"], values=s["amount"], aggfunc="sum")
p_df = {
    "row_pct": (pd.crosstab(**args, normalize="index") * 100).round(1),
    "col_pct": (pd.crosstab(**args, normalize="columns") * 100).round(1),
    "grand_pct": (pd.crosstab(**args, normalize=True) * 100).round(1),
}
for k, v in p_df.items():
    v.columns.name = None; v.index.name = "region"
    print("pandas", k); print(v.to_string())

# crosstab fills empty cells and 0/0 with 0.0, SQL keeps NULL: so crosstab equals the SQL result after fillna(0)
# the SQL-faithful pandas version (NaN stays NaN, zero total -> NaN like NULLIF) uses pivot_table and explicit division
nan = float("nan")
tbl = s.pivot_table(index="region", columns="product", values="amount", aggfunc="sum")
faithful = {
    "row_pct": tbl.div(tbl.sum(axis=1).replace(0, nan), axis=0) * 100,
    "col_pct": tbl.div(tbl.sum(axis=0).replace(0, nan), axis=1) * 100,
    "grand_pct": tbl / tbl.sum().sum() * 100,
}
def rows(df):
    return [tuple(None if pd.isna(x) else round(float(x), 1) for x in row) for row in df.itertuples(index=False)]
for k in sql_df:
    assert list(sql_df[k].index) == list(p_df[k].index) == list(faithful[k].index)
    assert rows(sql_df[k].fillna(0)) == rows(p_df[k]), ("crosstab", k)       # crosstab == SQL with NULL shown as 0
    assert rows(sql_df[k]) == rows(faithful[k].round(1)), ("pivot_table", k)  # pivot_table + division == SQL exactly
print("faithful row_pct (NaN kept):"); print(faithful["row_pct"].round(1).to_string())
print("asserts passed (rows sorted by region): crosstab == SQL with NULL->0; pivot_table division == SQL with NULL kept")
