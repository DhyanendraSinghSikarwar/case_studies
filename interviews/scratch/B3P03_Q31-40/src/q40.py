# Q40: dialect map for subqueries and CTEs: every SQLite row below is executed, nothing else is claimed as run
import sqlite3
import pandas as pd

print("SQLite version:", sqlite3.sqlite_version)

SCHEMA = """
CREATE TABLE prices(id INTEGER PRIMARY KEY, price INTEGER);
CREATE TABLE new_prices(id INTEGER, new_price INTEGER);
CREATE TABLE archive(id INTEGER, price INTEGER);
INSERT INTO prices VALUES (1,10),(2,20),(3,30);
INSERT INTO new_prices VALUES (1,11),(3,33);
"""
# UPDATE ... FROM: the one statement that also has a pandas twin
SQL_MAIN = """
UPDATE prices SET price = n.new_price FROM new_prices n WHERE prices.id = n.id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
con.execute(SQL_MAIN)
sql_df = pd.read_sql_query("SELECT id, price FROM prices ORDER BY id", con)
base = pd.DataFrame({"id": [1, 2, 3], "price": [10, 20, 30]})
newp = pd.DataFrame({"id": [1, 3], "new_price": [11, 33]})
# pd:main
pd_df = base.assign(price=base["id"].map(newp.set_index("id")["new_price"]).fillna(base["price"]).astype("int64"))
# pd:end
print("\nUPDATE ... FROM result (SQLite):")
print(sql_df.to_string(index=False))
print("pandas map + fillna:")
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, pd_df)
print("assert: SQL UPDATE ... FROM == pandas map/fillna (compared by id)")

def fresh():
    c = sqlite3.connect(":memory:")
    c.executescript(SCHEMA)
    return c

def probe(label, sql, after=None):
    c = fresh()
    try:
        cur = c.execute(sql)
        rows = cur.fetchall() if cur.description else "ok"
        if after:
            rows = "%s; then %s" % (rows, c.execute(after).fetchall())
        print("%-46s -> %s" % (label, rows))
    except sqlite3.Error as e:
        print("%-46s -> ERROR: %s" % (label, e))

print("\n--- scalar subquery returning many rows ---")
probe("SELECT (SELECT price FROM prices)", "SELECT (SELECT price FROM prices)")
probe("SELECT (... ORDER BY price DESC)", "SELECT (SELECT price FROM prices ORDER BY price DESC)")
probe("SELECT ... WHERE price = (SELECT price FROM prices)", "SELECT id FROM prices WHERE price = (SELECT price FROM prices)")
print("pandas twin: Series([10, 20, 30]).item() ->", end=" ")
try:
    pd.Series([10, 20, 30]).item()
except ValueError as e:
    print("ValueError:", e)

print("\n--- alias on a derived table ---")
probe("SELECT * FROM (SELECT 1 AS a)", "SELECT * FROM (SELECT 1 AS a)")
probe("SELECT t.a FROM (SELECT 1 AS a) t", "SELECT t.a FROM (SELECT 1 AS a) t")
probe("join of two un-aliased derived tables", "SELECT * FROM (SELECT 1 AS a) JOIN (SELECT 1 AS b) ON a = b")
probe("two un-aliased derived tables, same column name", "SELECT a FROM (SELECT 1 AS a) JOIN (SELECT 1 AS a)")

print("\n--- ANY / SOME / ALL ---")
probe("price > ANY (SELECT ...)", "SELECT id FROM prices WHERE price > ANY (SELECT price FROM prices)")
probe("price > ALL (SELECT ...)", "SELECT id FROM prices WHERE price > ALL (SELECT price FROM prices)")
probe("price = SOME (SELECT ...)", "SELECT id FROM prices WHERE price = SOME (SELECT price FROM prices)")
probe("emulation: price > (SELECT MIN(price) ...)", "SELECT id FROM prices WHERE price > (SELECT MIN(price) FROM prices)")
probe("emulation: price >= (SELECT MAX(price) ...)", "SELECT id FROM prices WHERE price >= (SELECT MAX(price) FROM prices)")

print("\n--- LIMIT inside IN, LIMIT / OFFSET forms ---")
probe("IN (SELECT ... ORDER BY ... LIMIT 2)", "SELECT id FROM prices WHERE id IN (SELECT id FROM prices ORDER BY price DESC LIMIT 2) ORDER BY id")
probe("LIMIT 1 + 1", "SELECT id FROM prices ORDER BY id LIMIT 1 + 1")
probe("LIMIT (SELECT COUNT(*) - 1 ...)", "SELECT id FROM prices ORDER BY id LIMIT (SELECT COUNT(*) - 1 FROM prices)")
probe("LIMIT -1 OFFSET 1", "SELECT id FROM prices ORDER BY id LIMIT -1 OFFSET 1")
probe("OFFSET alone", "SELECT id FROM prices ORDER BY id OFFSET 1")

print("\n--- UPDATE / DELETE reading the table they change ---")
probe("UPDATE ... WHERE price > (SELECT AVG(price) same table)", "UPDATE prices SET price = price + 1 WHERE price > (SELECT AVG(price) FROM prices)", after="SELECT id, price FROM prices ORDER BY id")
probe("DELETE ... WHERE price < (SELECT AVG(price) same table)", "DELETE FROM prices WHERE price < (SELECT AVG(price) FROM prices)", after="SELECT id, price FROM prices ORDER BY id")
probe("DELETE ... WHERE id IN (SELECT id FROM same table)", "DELETE FROM prices WHERE id IN (SELECT id FROM prices WHERE price > 15)", after="SELECT id, price FROM prices ORDER BY id")

print("\n--- WITH before UPDATE, DELETE, INSERT ---")
probe("WITH ... UPDATE", "WITH hi AS (SELECT id FROM prices WHERE price > 15) UPDATE prices SET price = 0 WHERE id IN (SELECT id FROM hi)", after="SELECT id, price FROM prices ORDER BY id")
probe("WITH ... DELETE", "WITH hi AS (SELECT id FROM prices WHERE price > 15) DELETE FROM prices WHERE id IN (SELECT id FROM hi)", after="SELECT id, price FROM prices ORDER BY id")
probe("WITH ... INSERT INTO ... SELECT", "WITH hi AS (SELECT id, price FROM prices WHERE price > 15) INSERT INTO archive SELECT id, price FROM hi", after="SELECT id, price FROM archive ORDER BY id")
probe("INSERT INTO ... WITH ... SELECT", "INSERT INTO archive WITH hi AS (SELECT id, price FROM prices WHERE price > 15) SELECT id, price FROM hi", after="SELECT id, price FROM archive ORDER BY id")
probe("INSERT ... SELECT ... RETURNING", "INSERT INTO archive SELECT id, price FROM prices WHERE price > 15 RETURNING id")

print("\n--- UPDATE ... FROM (shown above), row values ---")
probe("(a, b) < (c, d)", "SELECT (1, 2) < (1, 3), (1, 2) = (1, 2), (1, NULL) = (1, 2)")
probe("(id, price) IN (SELECT id, price ...)", "SELECT id FROM prices WHERE (id, price) IN (SELECT id, price FROM prices WHERE price > 15) ORDER BY id")
probe("(id, price) IN (VALUES (1, 10), (3, 30))", "SELECT id FROM prices WHERE (id, price) IN (VALUES (1, 10), (3, 30)) ORDER BY id")

print("\n--- CTE rules ---")
probe("CTE used twice", "WITH t AS (SELECT price FROM prices) SELECT (SELECT MAX(price) FROM t), (SELECT MIN(price) FROM t)")
probe("MATERIALIZED / NOT MATERIALIZED", "WITH a AS MATERIALIZED (SELECT 1 AS x), b AS NOT MATERIALIZED (SELECT 2 AS y) SELECT x, y FROM a, b")
probe("CTE with column list", "WITH t(a, b) AS (SELECT id, price FROM prices) SELECT a, b FROM t ORDER BY a LIMIT 1")
probe("later CTE referenced by an earlier one", "WITH a AS (SELECT * FROM b), b AS (SELECT 1 AS x) SELECT * FROM a")
probe("earlier CTE referenced by a later one", "WITH b AS (SELECT 1 AS x), a AS (SELECT * FROM b) SELECT * FROM a")
probe("derived table name reused outside its scope", "SELECT * FROM (SELECT 1 AS x) d, d")
probe("WITH inside a subquery", "SELECT * FROM (WITH t AS (SELECT 5 AS v) SELECT v FROM t)")
probe("two WITH keywords in a row", "WITH a AS (SELECT 1 AS x) WITH b AS (SELECT 2 AS y) SELECT * FROM a, b")

print("\n--- LATERAL ---")
probe("LATERAL (SELECT ...)", "SELECT * FROM prices p, LATERAL (SELECT 1 AS x WHERE p.id > 0)")
