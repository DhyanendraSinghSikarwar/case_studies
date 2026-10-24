# Q21: IN / NOT IN subqueries translated to pandas (isin, map, merge), with NaN customer_id in orders
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Pune'),(4,'Dev','Goa');
INSERT INTO orders VALUES (1,1,300),(2,1,250),(3,2,200),(4,2,100),(5,NULL,900),(6,3,50);
"""
SQL_MAIN = """
SELECT customer_id, name, city
FROM customers
WHERE customer_id IN (SELECT customer_id
                      FROM orders
                      GROUP BY customer_id
                      HAVING SUM(amount) > 500)
ORDER BY customer_id
"""
SQL_NOT_IN = """
SELECT customer_id, name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id
                          FROM orders
                          GROUP BY customer_id
                          HAVING SUM(amount) > 500)
ORDER BY customer_id
"""
SQL_NOT_EXISTS = """
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1
                  FROM orders o
                  WHERE o.customer_id = c.customer_id
                  GROUP BY o.customer_id
                  HAVING SUM(o.amount) > 500)
ORDER BY c.customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
print("orders customer_id dtype in pandas:", orders["customer_id"].dtype, "| NaN count:", int(orders["customer_id"].isna().sum()))

sql_df = pd.read_sql_query(SQL_MAIN, con)
print("\nSQL IN subquery (customers with total spend > 500):")
print(sql_df.to_string(index=False))
print("SQL group totals incl. the NULL group:", con.execute(
    "SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id ORDER BY customer_id").fetchall())

# pd:main
agg = orders.groupby("customer_id")["amount"].sum()          # NaN group dropped (dropna=True default)
big = agg[agg > 500]
form_isin = customers[customers["customer_id"].isin(big.index)]
form_map = (customers.assign(total=customers["customer_id"].map(agg))
            .loc[lambda d: d["total"] > 500, ["customer_id", "name", "city"]])
form_merge = (customers.merge(agg.rename("total").reset_index(), on="customer_id", how="left")
              .loc[lambda d: d["total"] > 500, ["customer_id", "name", "city"]])
# pd:end
for label, f in [("isin", form_isin), ("map", form_map), ("merge(left)", form_merge)]:
    f = f.sort_values("customer_id").reset_index(drop=True)
    pd.testing.assert_frame_equal(sql_df, f, check_dtype=False)
    print(f"pandas form {label}: rows {f['customer_id'].tolist()} == SQL")

print("\nWhich form keeps customers without orders (before filtering)?")
print("  isin: only filters customers, it produces no total column")
print("  map keeps every customer, total is NaN for Dev:", customers.assign(total=customers["customer_id"].map(agg))["total"].tolist())
print("  merge how='left' rows:", len(customers.merge(agg.rename('total').reset_index(), on='customer_id', how='left')),
      "| how='inner' rows:", len(customers.merge(agg.rename('total').reset_index(), on='customer_id', how='inner')))

print("\nNaN handling:")
s = pd.Series([1.0, np.nan, 3.0])
print("  pandas  s.isin([nan]) ->", s.isin([np.nan]).tolist(), "  (NaN matches NaN)")
print("  SQLite  NULL IN (NULL)         ->", con.execute("SELECT NULL IN (NULL)").fetchone()[0])
print("  SQLite  1 NOT IN (2, NULL)     ->", con.execute("SELECT 1 NOT IN (2, NULL)").fetchone()[0])
print("  pandas  ~isin([2, nan]) on [1,nan,3] ->", (~s.isin([2.0, np.nan])).tolist())

print("  empty list: pandas ~isin([]) ->", (~s.isin([])).tolist(), "| SQLite 1 NOT IN (SELECT 1 WHERE 0) ->", con.execute("SELECT 1 NOT IN (SELECT 1 WHERE 0)").fetchone()[0])

not_in = pd.read_sql_query(SQL_NOT_IN, con)
not_ex = pd.read_sql_query(SQL_NOT_EXISTS, con)
print("\nSQL NOT IN over a list that contains the NULL group, rows:", len(not_in))
print("SQL NOT EXISTS, ids:", not_ex["customer_id"].tolist())
pd_not = customers[~customers["customer_id"].isin(big.index)]
print("pandas ~isin, ids:", pd_not["customer_id"].tolist())
# the SQL list was (1, NULL); the pandas list is [1] because groupby dropped NaN, so give pandas the NULL too:
big_with_nan = orders.groupby("customer_id", dropna=False)["amount"].sum()
big_with_nan = big_with_nan[big_with_nan > 500]
print("pandas groupby(dropna=False) list:", big_with_nan.index.tolist(),
      "-> ~isin ids:", customers[~customers["customer_id"].isin(big_with_nan.index)]["customer_id"].tolist())
assert len(not_in) == 0
assert not_ex["customer_id"].tolist() == pd_not["customer_id"].tolist() == [2, 3, 4]
print("\nasserts passed: SQL IN == pandas isin == map == merge (compared after sorting by customer_id)")
