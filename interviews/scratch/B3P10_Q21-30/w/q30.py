# Q30: pivot with subtotals and a grand total without ROLLUP/CUBE (UNION ALL), and the NULL-label trap; pandas margins.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales(region TEXT, product TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('East','A',10),('East','A',5),('East','B',20),('East','C',30),
 ('West','A',40),('West','B',15);                                   -- West has no C row
""")

# long layout: detail + region subtotal + product subtotal + grand total, with a sort key so totals come last
sql_long = """
SELECT region, product, SUM(amount) AS amount, 0 AS k FROM sales GROUP BY region, product
UNION ALL SELECT region, 'ALL', SUM(amount), 1 FROM sales GROUP BY region
UNION ALL SELECT 'ALL', product, SUM(amount), 2 FROM sales GROUP BY product
UNION ALL SELECT 'ALL', 'ALL', SUM(amount), 3 FROM sales
ORDER BY k, region, product"""
long_df = pd.read_sql(sql_long, con)
print(long_df.to_string(index=False))

# pivoted layout: one row per region, one row 'ALL', a Total column
sql_wide = """
SELECT region,
       SUM(CASE WHEN product = 'A' THEN amount END) AS a,
       SUM(CASE WHEN product = 'B' THEN amount END) AS b,
       SUM(CASE WHEN product = 'C' THEN amount END) AS c,
       SUM(amount) AS total, 0 AS k
FROM sales GROUP BY region
UNION ALL
SELECT 'ALL',
       SUM(CASE WHEN product = 'A' THEN amount END),
       SUM(CASE WHEN product = 'B' THEN amount END),
       SUM(CASE WHEN product = 'C' THEN amount END),
       SUM(amount), 1
FROM sales
ORDER BY k, region"""
wide_df = pd.read_sql(sql_wide, con).drop(columns="k")
print(wide_df.to_string(index=False))
plain = con.execute("SELECT SUM(amount) FROM sales").fetchone()[0]
print("plain SUM:", plain, "| ALL row total:", int(wide_df.loc[wide_df.region == "ALL", "total"].iloc[0]),
      "| sum of region totals:", int(wide_df.loc[wide_df.region != "ALL", "total"].sum()),
      "| sum of A,B,C in ALL row:", int(wide_df.loc[wide_df.region == "ALL", ["a", "b", "c"]].sum(axis=1).iloc[0]))

# the NULL-label trap: a real NULL product plus subtotals that use NULL as the label (what ROLLUP prints)
con.executescript("""
CREATE TABLE sales_n(region TEXT, product TEXT, amount INTEGER);
INSERT INTO sales_n VALUES ('East','A',10),('East',NULL,7),('West','A',5);
""")
sql_null_label = """
SELECT region, product, SUM(amount) AS amount FROM sales_n GROUP BY region, product
UNION ALL SELECT region, NULL, SUM(amount) FROM sales_n GROUP BY region
ORDER BY region, product"""
print("NULL used as the subtotal label (ROLLUP style):")
for r in con.execute(sql_null_label): print("  ", r)
print("  East rows where product IS NULL:", con.execute(f"SELECT COUNT(*) FROM ({sql_null_label.replace('ORDER BY region, product','')}) WHERE region='East' AND product IS NULL").fetchone()[0], "(real NULL product and subtotal are indistinguishable)")
sql_safe = """
SELECT region, COALESCE(product, '(no product)') AS product, SUM(amount) AS amount, 0 AS k FROM sales_n GROUP BY region, product
UNION ALL SELECT region, 'ALL', SUM(amount), 1 FROM sales_n GROUP BY region
ORDER BY region, k, product"""
print("explicit labels:"); 
for r in con.execute(sql_safe): print("  ", r)

# pandas
s = pd.read_sql("SELECT * FROM sales", con)
pt = s.pivot_table(index="region", columns="product", values="amount", aggfunc="sum", margins=True, margins_name="ALL")
pt.columns.name = None
print(pt.to_string())
p_wide = pt.reset_index().rename(columns={"A": "a", "B": "b", "C": "c", "ALL": "total"})

# groupby version: detail rows, then the ALL row
g = s.groupby(["region", "product"])["amount"].sum().unstack("product")
g["total"] = s.groupby("region")["amount"].sum()
all_row = g.sum(); all_row.name = "ALL"                      # column sums (NaN skipped) incl. total
g2 = pd.concat([g, all_row.to_frame().T]).reset_index().rename(columns={"index": "region", "product": "region"})
g2.columns.name = None
g2 = g2.rename(columns={"A": "a", "B": "b", "C": "c"})

def rows(df):
    return [tuple(None if pd.isna(v) else (int(v) if not isinstance(v, str) else v) for v in r) for r in df[["region", "a", "b", "c", "total"]].itertuples(index=False)]
assert rows(wide_df) == rows(p_wide) == rows(g2), (rows(wide_df), rows(p_wide), rows(g2))
assert plain == 120 == int(wide_df.loc[wide_df.region == "ALL", "total"].iloc[0])

# pandas drops a NaN product from pivot_table, so its margins lose the NULL-product amount
n = pd.read_sql("SELECT * FROM sales_n", con)
ptn = n.pivot_table(index="region", columns="product", values="amount", aggfunc="sum", margins=True, margins_name="ALL")
print("pandas margins grand total with a NaN product:", int(ptn.loc["ALL", "ALL"]), "| plain SUM:", int(n["amount"].sum()))
assert int(ptn.loc["ALL", "ALL"]) == 15 and int(n["amount"].sum()) == 22
print("asserts passed (UNION ALL pivot == pivot_table(margins=True) == groupby version; rows: regions sorted, then ALL)")
con.close()
