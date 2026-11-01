# Q22: ANY / SOME / ALL when SQLite has none: MAX / MIN and EXISTS / NOT EXISTS equivalents
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER);
INSERT INTO products VALUES
 (1,'Atlas','Books',10),(2,'Novel','Books',20),(3,'Cookbook','Books',30),
 (4,'Digest','Mags',15),(5,'Zine','Mags',NULL),
 (6,'Pen','Stationery',5),(7,'Lamp','Home',25),(8,'Chair','Home',40),(9,'Desk','Home',35),
 (10,'Bag','Travel',NULL);
"""
# native syntax (PostgreSQL / MySQL), NOT executed on SQLite
NATIVE_ALL = "SELECT name FROM products WHERE price > ALL (SELECT price FROM products WHERE category = ?)"
NATIVE_ANY = "SELECT name FROM products WHERE price > ANY (SELECT price FROM products WHERE category = ?)"

SQL_ALL_MAX = """
SELECT product_id FROM products
WHERE price > (SELECT MAX(price) FROM products WHERE category = ?)
ORDER BY product_id
"""
SQL_ALL_NOT_EXISTS = """
SELECT p.product_id FROM products p
WHERE NOT EXISTS (SELECT 1 FROM products b
                  WHERE b.category = ?
                    AND NOT COALESCE(p.price > b.price, 0))
ORDER BY p.product_id
"""
SQL_ANY_MIN = """
SELECT product_id FROM products
WHERE price > (SELECT MIN(price) FROM products WHERE category = ?)
ORDER BY product_id
"""
SQL_ANY_EXISTS = """
SELECT p.product_id FROM products p
WHERE EXISTS (SELECT 1 FROM products b
              WHERE b.category = ?
                AND p.price > b.price)
ORDER BY p.product_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)

for label, sql in [("price > ALL", NATIVE_ALL), ("price > ANY", NATIVE_ANY), ("price > SOME", NATIVE_ANY.replace("ANY", "SOME"))]:
    try:
        con.execute(sql, ("Books",)).fetchall()
        print(label, "-> ran")
    except sqlite3.Error as e:
        print(f"{label} on SQLite -> {type(e).__name__}: {e}")

prices = pd.read_sql_query("SELECT * FROM products", con)
def ids(sql, cat):
    return [r[0] for r in con.execute(sql, (cat,))]

# pd:main
def pd_all(df, cat):
    sub = df.loc[df["category"] == cat, "price"].to_numpy(dtype=float)
    cmp = df["price"].to_numpy(dtype=float)[:, None] > sub[None, :]   # NaN compares False
    return df.loc[cmp.all(axis=1), "product_id"].tolist()            # all() of an empty row is True

def pd_any(df, cat):
    sub = df.loc[df["category"] == cat, "price"].to_numpy(dtype=float)
    cmp = df["price"].to_numpy(dtype=float)[:, None] > sub[None, :]
    return df.loc[cmp.any(axis=1), "product_id"].tolist()            # any() of an empty row is False
# pd:end

print()
res = {}
for cat, what in [("Books", "clean prices"), ("Mags", "one NULL price"), ("Toys", "empty subquery")]:
    r = (ids(SQL_ALL_MAX, cat), ids(SQL_ALL_NOT_EXISTS, cat), pd_all(prices, cat),
         ids(SQL_ANY_MIN, cat), ids(SQL_ANY_EXISTS, cat), pd_any(prices, cat))
    res[cat] = r
    print(f"{cat:5s} ({what})")
    for name, v in zip(["ALL MAX", "ALL NOT EXISTS", "pandas all", "ANY MIN", "ANY EXISTS", "pandas any"], r):
        print(f"   {name:15s}{v}")

for cat in res:
    mx, ne, pa, mn, ex, pn = res[cat]
    assert ne == pa and ex == pn and mn == ex       # NOT EXISTS / EXISTS forms equal pandas; ANY via MIN always equal
assert res["Books"][0] == res["Books"][1] == [8, 9]
assert res["Mags"][0] != res["Mags"][1] and res["Toys"][0] != res["Toys"][1]
print("\nasserts passed: NOT EXISTS == pandas all, EXISTS == MIN == pandas any; MAX differs from ALL on NULL and empty sets")
