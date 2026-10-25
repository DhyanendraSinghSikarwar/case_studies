# Q13: category tree: breadcrumb, depth, product count including descendants, leaf flag
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE categories(category_id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT);
INSERT INTO categories VALUES
 (1,NULL,'Electronics'),(2,1,'Phones'),(3,2,'Android'),(4,2,'iOS'),(5,1,'Laptops'),
 (6,NULL,'Books'),(7,6,'Fiction'),(8,1,'Tablets');
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category_id INTEGER);
INSERT INTO products VALUES
 (101,3),(102,3),(103,3),(104,4),(105,4),(106,5),(107,5),(108,2),
 (109,7),(110,7),(111,7),(112,7),(113,NULL),(114,99);
"""
SQL_MAIN = """
WITH RECURSIVE tree(category_id, depth, breadcrumb) AS (
  SELECT category_id, 0, name FROM categories WHERE parent_id IS NULL
  UNION ALL
  SELECT c.category_id, t.depth + 1, t.breadcrumb || ' > ' || c.name
  FROM categories c JOIN tree t ON c.parent_id = t.category_id
), closure(ancestor, descendant) AS (
  SELECT category_id, category_id FROM categories
  UNION ALL
  SELECT cl.ancestor, c.category_id
  FROM closure cl JOIN categories c ON c.parent_id = cl.descendant
), rollup AS (
  SELECT cl.ancestor AS category_id, COUNT(p.product_id) AS products_incl_descendants
  FROM closure cl LEFT JOIN products p ON p.category_id = cl.descendant
  GROUP BY cl.ancestor
)
SELECT t.category_id, t.breadcrumb, t.depth,
       COALESCE(r.products_incl_descendants, 0) AS products_incl_descendants,
       CASE WHEN EXISTS (SELECT 1 FROM categories k WHERE k.parent_id = t.category_id) THEN 0 ELSE 1 END AS is_leaf
FROM tree t LEFT JOIN rollup r ON r.category_id = t.category_id
ORDER BY t.category_id
"""
SQL_DIRECT = """
SELECT c.category_id, COUNT(p.product_id) AS direct_products
FROM categories c LEFT JOIN products p ON p.category_id = c.category_id
GROUP BY c.category_id ORDER BY c.category_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("direct count only (GROUP BY category_id):", dict(con.execute(SQL_DIRECT).fetchall()))

cats = pd.read_sql_query("SELECT * FROM categories", con)
prods = pd.read_sql_query("SELECT * FROM products", con)

def category_report(cats, prods):
    # pd:main
    name = dict(zip(cats["category_id"], cats["name"]))
    parent = dict(zip(cats["category_id"], cats["parent_id"].astype("Int64")))
    rows = []
    for cid in cats["category_id"]:
        crumbs, cur, depth = [name[cid]], cid, 0
        while pd.notna(parent[cur]):
            cur = int(parent[cur])
            crumbs.append(name[cur])
            depth += 1
        rows.append((cid, " > ".join(reversed(crumbs)), depth))
    rep = pd.DataFrame(rows, columns=["category_id", "breadcrumb", "depth"])
    pairs = pd.DataFrame({"ancestor": cats["category_id"], "descendant": cats["category_id"]})
    edges = cats.dropna(subset=["parent_id"]).astype({"parent_id": int})
    frontier = pairs
    while not frontier.empty:
        frontier = (frontier.merge(edges, left_on="descendant", right_on="parent_id")
                            [["ancestor", "category_id"]].rename(columns={"category_id": "descendant"}))
        pairs = pd.concat([pairs, frontier], ignore_index=True)
    counts = (pairs.merge(prods, left_on="descendant", right_on="category_id", how="left")
                   .groupby("ancestor")["product_id"].count().rename("products_incl_descendants"))
    rep = rep.merge(counts, left_on="category_id", right_index=True, how="left")
    rep["is_leaf"] = (~rep["category_id"].isin(edges["parent_id"])).astype(int)
    return rep.sort_values("category_id").reset_index(drop=True)
    # pd:end

pd_df = category_report(cats, prods)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)   # compared after sorting by category_id
print("pandas equal to SQL; leaf categories:", list(pd_df.loc[pd_df.is_leaf == 1, "breadcrumb"]))
print("products not counted anywhere (NULL category or unknown category):",
      con.execute("SELECT product_id FROM products WHERE category_id IS NULL OR category_id NOT IN (SELECT category_id FROM categories)").fetchall())
# a leaf can be filtered with NOT IN only if parent_id has no NULLs: it has (roots), so show the trap
print("NOT IN version of the leaf filter returns:", con.execute("SELECT COUNT(*) FROM categories WHERE category_id NOT IN (SELECT parent_id FROM categories)").fetchone()[0], "rows (NULL parent_id of the roots poisons it)")
print("total rollup of roots:", int(pd_df.loc[pd_df.depth == 0, "products_incl_descendants"].sum()), "= products with a valid category:", int(prods["category_id"].isin(cats["category_id"]).sum()))
print("no root rows (anchor returns nothing) ->", pd.read_sql_query(SQL_MAIN.replace("FROM categories WHERE parent_id IS NULL", "FROM categories WHERE 1 = 0"), con).shape[0], "rows")
print("asserts passed")
