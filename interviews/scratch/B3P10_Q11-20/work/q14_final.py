# Q14: pandas pivot, pivot_table, crosstab versus the SQL SUM(CASE ...) pivot
import sqlite3
import numpy as np
import pandas as pd

print("pandas", pd.__version__, "| SQLite", sqlite3.sqlite_version)
rows = [("East", "Pen", "Jan", 100), ("East", "Pen", "Jan", 50), ("East", "Pen", "Feb", None),
        ("East", "Book", "Jan", 200), ("West", "Pen", "Feb", 70), ("West", "Book", "Mar", 30),
        ("West", None, "Jan", 40), ("North", "Pen", "Jan", None)]
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE sales(region TEXT, product TEXT, month TEXT, amount INTEGER)")
con.executemany("INSERT INTO sales VALUES (?,?,?,?)", rows)
df = pd.DataFrame(rows, columns=["region", "product", "month", "amount"])
print("dtypes:", {c: str(t) for c, t in df.dtypes.items()}, "| NaN product:", df["product"].isna().sum(), "| NaN amount:", df["amount"].isna().sum())

SQL_SUM = """
SELECT region,
       SUM(CASE WHEN month = 'Jan' THEN amount END) AS Jan,
       SUM(CASE WHEN month = 'Feb' THEN amount END) AS Feb,
       SUM(CASE WHEN month = 'Mar' THEN amount END) AS Mar,
       SUM(amount) AS Total
FROM sales GROUP BY region ORDER BY region
"""
SQL_AVG = """
SELECT region,
       AVG(CASE WHEN month = 'Jan' THEN amount END) AS Jan,
       AVG(CASE WHEN month = 'Feb' THEN amount END) AS Feb,
       AVG(CASE WHEN month = 'Mar' THEN amount END) AS Mar
FROM sales GROUP BY region ORDER BY region
"""
SQL_COUNT_AMOUNTS = """
SELECT region,
       COUNT(CASE WHEN month = 'Jan' THEN amount END) AS Jan,
       COUNT(CASE WHEN month = 'Feb' THEN amount END) AS Feb,
       COUNT(CASE WHEN month = 'Mar' THEN amount END) AS Mar
FROM sales GROUP BY region ORDER BY region
"""
SQL_COUNT_ROWS = """
SELECT region,
       COUNT(CASE WHEN month = 'Jan' THEN 1 END) AS Jan,
       COUNT(CASE WHEN month = 'Feb' THEN 1 END) AS Feb,
       COUNT(CASE WHEN month = 'Mar' THEN 1 END) AS Mar
FROM sales GROUP BY region ORDER BY region
"""
MONTHS = ["Jan", "Feb", "Mar"]
def q(sql): return pd.read_sql_query(sql, con).set_index("region")
sql_sum, sql_avg, sql_cnt_amt, sql_cnt_rows = q(SQL_SUM), q(SQL_AVG), q(SQL_COUNT_AMOUNTS), q(SQL_COUNT_ROWS)
print("\nSQL SUM(CASE) pivot with Total (NULL = no non-NULL amount):"); print(sql_sum)

# 1. pivot cannot aggregate
try:
    df.pivot(index="region", columns="month", values="amount")
except ValueError as e:
    print("\npivot with duplicates -> ValueError:", e)

# the all-NaN row is dropped by default (dropna=True drops rows and columns that are entirely NaN)
no_keep = df.pivot_table(index="region", columns="month", values="amount", aggfunc=lambda s: s.sum(min_count=1))
print("min_count=1 with default dropna: regions kept =", no_keep.index.tolist(), "(North is gone)")
no_keep_mean = df.pivot_table(index="region", columns="month", values="amount", aggfunc="mean")
print("mean with default dropna: regions kept =", no_keep_mean.index.tolist())

# 2. default pivot_table: sum of an all-NaN group is 0.0, not NaN
p_default = df.pivot_table(index="region", columns="month", values="amount", aggfunc="sum")
print("\npivot_table sum (default), columns come out alphabetical:"); print(p_default)
p_default = p_default.reindex(columns=MONTHS)
diff = ~np.isclose(p_default.to_numpy(float), sql_sum[MONTHS].to_numpy(float), equal_nan=True)
print("cells that differ from SQL after reindexing the months:", [(r, m) for (r, m), d in zip(
    [(r, m) for r in p_default.index for m in MONTHS], diff.ravel()) if d],
    "(pandas 0.0 where SQL has NULL)")

def sum_or_nan(s):                      # like SQL SUM: NaN when there is no non-NaN value
    return s.sum(min_count=1)

p_sum = (df.pivot_table(index="region", columns="month", values="amount", aggfunc=sum_or_nan, dropna=False)
           .reindex(columns=MONTHS))
p_mean = df.pivot_table(index="region", columns="month", values="amount", aggfunc="mean", dropna=False).reindex(columns=MONTHS)
p_cnt_amt = df.pivot_table(index="region", columns="month", values="amount", aggfunc="count", fill_value=0).reindex(columns=MONTHS)
p_cnt_rows = pd.crosstab(df["region"], df["month"]).reindex(columns=MONTHS, fill_value=0)
p_margins = df.pivot_table(index="region", columns="month", values="amount", aggfunc=sum_or_nan,
                           margins=True, margins_name="Total", dropna=False).reindex(columns=MONTHS + ["Total"])
for p in (p_sum, p_mean, p_cnt_amt, p_cnt_rows, p_margins):
    p.columns.name = None
    p.index.name = "region"

print("\nsum with min_count=1 and dropna=False:"); print(p_sum)
print("\nmargins=True, margins_name='Total':"); print(p_margins)
print("\nmean:"); print(p_mean.round(3))
print("\ncount of non-NaN amounts, fill_value=0:"); print(p_cnt_amt)
print("\ncrosstab (row counts):"); print(p_cnt_rows)

# comparisons, rows ordered by region, columns Jan, Feb, Mar
pd.testing.assert_frame_equal(p_sum, sql_sum[MONTHS], check_dtype=False)
pd.testing.assert_frame_equal(p_mean, sql_avg[MONTHS], check_dtype=False)
pd.testing.assert_frame_equal(p_cnt_amt, sql_cnt_amt[MONTHS], check_dtype=False)
pd.testing.assert_frame_equal(p_cnt_rows, sql_cnt_rows[MONTHS], check_dtype=False)
pd.testing.assert_series_equal(p_margins.loc[sql_sum.index, "Total"], sql_sum["Total"], check_dtype=False)
assert p_margins.loc["Total", "Total"] == con.execute("SELECT SUM(amount) FROM sales").fetchone()[0] == 490
print("\nasserts passed: sum, mean, count, crosstab and margins match the SQL pivot (rows by region, columns Jan Feb Mar)")

# list and dict aggfunc, fill_value
gb = (df.groupby(["region", "month"])["amount"].sum(min_count=1).unstack().reindex(columns=MONTHS))
pd.testing.assert_frame_equal(gb, sql_sum[MONTHS], check_dtype=False, check_names=False)
print("groupby(['region','month'])['amount'].sum(min_count=1).unstack() also equals the SQL sum pivot (North kept)")
m1 = df.pivot_table(index="region", columns="month", values="amount", aggfunc="sum", margins=True, margins_name="Total")
m2 = df.pivot_table(index="region", columns="month", values="amount", aggfunc="sum", margins=True, margins_name="Total", dropna=False)
print("default sum margins, North Total: dropna=True ->", m1.loc["North", "Total"], "| dropna=False ->", m2.loc["North", "Total"], "(SQL SUM is NULL)")

print("\naggfunc=['sum','mean'] columns:", df.pivot_table(index="region", columns="month", values="amount", aggfunc=["sum", "mean"]).columns.tolist()[:3], "...")
print("aggfunc={'amount': ['sum','count']} column levels:", df.pivot_table(index="region", columns="month", values="amount",
      aggfunc={"amount": ["sum", "count"]}).columns.nlevels)
print("fill_value=0 on the default sum turns every NaN cell into 0:", df.pivot_table(index="region", columns="month",
      values="amount", aggfunc="sum", fill_value=0).to_numpy().tolist())

# NaN row label
by_prod = df.pivot_table(index="product", columns="month", values="amount", aggfunc="sum")
print("\nindex='product' (default): labels", by_prod.index.tolist(), "| total", by_prod.sum().sum(), "(the NaN-product 40 vanished; region total is 490)")
by_prod2 = df.pivot_table(index="product", columns="month", values="amount", aggfunc="sum", dropna=False)
print("index='product', dropna=False: labels", by_prod2.index.tolist(), "| total", by_prod2.sum().sum())
print("crosstab on product default rows:", pd.crosstab(df["product"], df["month"]).index.tolist(),
      "| dropna=False:", pd.crosstab(df["product"], df["month"], dropna=False).index.tolist())
sql_prod = con.execute("SELECT product, SUM(amount) FROM sales GROUP BY product ORDER BY product").fetchall()
print("SQL GROUP BY product keeps the NULL group:", sql_prod)

# categorical month with an unobserved category
cat = df.assign(month=pd.Categorical(df["month"], categories=MONTHS + ["Apr"]))
a = cat.pivot_table(index="region", columns="month", values="amount", aggfunc="sum")
b = cat.pivot_table(index="region", columns="month", values="amount", aggfunc="sum", observed=False)
print("\ncategorical month with unused 'Apr': default columns", a.columns.tolist(), "| observed=False columns", b.columns.tolist(),
      "| Apr cells:", b["Apr"].tolist())
assert a.columns.tolist() == MONTHS and "Apr" in b.columns
print("asserts passed (categorical)")
