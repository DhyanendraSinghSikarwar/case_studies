# Q20: delete a subtree, move a subtree with a rebuilt materialised path, and refuse a move that creates a cycle
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE categories(category_id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT, path TEXT);
INSERT INTO categories VALUES
 (1,NULL,'Store','/1/'),(2,1,'Home','/1/2/'),(5,1,'Electronics','/1/5/'),(6,5,'Phones','/1/5/6/'),
 (7,5,'Laptops','/1/5/7/'),(9,6,'Android','/1/5/6/9/'),(8,1,'Garden','/1/8/'),(10,8,'Tools','/1/8/10/'),
 (11,8,'Lawn','/1/8/11/'),(12,10,'Spades','/1/8/10/12/');
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER);
INSERT INTO employees VALUES (1,NULL),(2,1),(3,1),(4,3),(5,3),(6,4),(7,2);
"""
SQL_MAIN = """
DELETE FROM categories
WHERE category_id IN (
  WITH RECURSIVE sub(id) AS (
    SELECT category_id FROM categories WHERE category_id = 5
    UNION ALL
    SELECT c.category_id FROM categories c JOIN sub s ON c.parent_id = s.id
  )
  SELECT id FROM sub
)
"""
SQL_CYCLE_CHECK = """
WITH RECURSIVE sub(id) AS (
  SELECT :moved
  UNION
  SELECT c.category_id FROM categories c JOIN sub s ON c.parent_id = s.id
)
SELECT COUNT(*) FROM sub WHERE id = :newparent
"""
SQL_MOVE_PARENT = """
UPDATE categories SET parent_id = :newparent WHERE category_id = :moved
"""
SQL_MOVE_PATHS = """
WITH RECURSIVE t(id, newpath) AS (
  SELECT c.category_id, p.path || c.category_id || '/'
  FROM categories c JOIN categories p ON p.category_id = c.parent_id
  WHERE c.category_id = :moved
  UNION ALL
  SELECT c.category_id, t.newpath || c.category_id || '/'
  FROM categories c JOIN t ON c.parent_id = t.id
)
UPDATE categories SET path = (SELECT newpath FROM t WHERE t.id = categories.category_id)
WHERE category_id IN (SELECT id FROM t)
"""
SQL_DELETE_EMP = """
DELETE FROM employees
WHERE emp_id IN (
  WITH RECURSIVE team(id) AS (
    SELECT emp_id FROM employees WHERE emp_id = 3
    UNION ALL SELECT e.emp_id FROM employees e JOIN team t ON e.manager_id = t.id
  )
  SELECT id FROM team
)
"""

def load():
    con = sqlite3.connect(":memory:")
    con.executescript(SCHEMA)
    return con

def table(con, name="categories"):
    return pd.read_sql_query(f"SELECT * FROM {name} ORDER BY 1", con)

def move(con, moved, newparent):
    # refuse a move into the moved node's own subtree (that includes the node itself)
    if con.execute(SQL_CYCLE_CHECK, {"moved": moved, "newparent": newparent}).fetchone()[0] > 0:
        return False
    with con:
        con.execute(SQL_MOVE_PARENT, {"moved": moved, "newparent": newparent})
        con.execute(SQL_MOVE_PATHS, {"moved": moved})
    return True

con = load()
before = table(con)
print("categories before:")
print(before.to_string(index=False))
cur = con.execute(SQL_MAIN)
print("DELETE category 5 and everything under it: rows deleted =", cur.rowcount)
after_del = table(con)
print(after_del.to_string(index=False))
cur = con.execute(SQL_DELETE_EMP)
print("DELETE employee 3 and the whole team below: rows deleted =", cur.rowcount, "| employees left:", [r[0] for r in con.execute("SELECT emp_id FROM employees ORDER BY 1")])

ok = move(con, 8, 2)
after_move = table(con)
print("move subtree 8 under 2 (moved =", ok, "):")
print(after_move.to_string(index=False))
print("move 2 under 12 (a descendant of 2 after the move) accepted?", move(con, 2, 12), "| move 8 under itself accepted?", move(con, 8, 8))
assert table(con).equals(after_move), "refused moves must not change anything"

cats = before.copy()

def pandas_side(cats):
    # pd:main
    c = cats.set_index("category_id")
    kids = {p: list(g.index) for p, g in c.dropna(subset=["parent_id"]).groupby("parent_id")}
    def subtree(root):
        out, stack = [], [root]
        while stack:
            n = stack.pop()
            out.append(n)
            stack.extend(kids.get(n, []))
        return out
    deleted = c.drop(subtree(5))
    moved = deleted.copy()
    moved.loc[8, "parent_id"] = 2
    for n in subtree(8):   # pre-order: a parent is always handled before its children
        p = moved.loc[n, "parent_id"]
        moved.loc[n, "path"] = moved.loc[int(p), "path"] + f"{n}/"
    return deleted.reset_index(), moved.reset_index()
    # pd:end

pd_del, pd_move = pandas_side(cats)
pd.testing.assert_frame_equal(pd_del, after_del, check_dtype=False)   # compared after sorting by category_id
pd.testing.assert_frame_equal(pd_move, after_move, check_dtype=False)
print("pandas results equal SQL after the delete and after the move")
assert table(con, "categories")["category_id"].tolist() == [1, 2, 8, 10, 11, 12]
n_sub = con.execute("SELECT COUNT(*) FROM categories WHERE path LIKE '/1/2/8/%'").fetchone()[0]
print("rows whose path starts with /1/2/8/ after the move:", n_sub, "(Garden and its three descendants)")

# what the cycle check protects: a move into the own subtree, forced without the check
c2 = load()
c2.execute("UPDATE categories SET parent_id = 9 WHERE category_id = 5")
reach = c2.execute("""WITH RECURSIVE d(id) AS (SELECT category_id FROM categories WHERE parent_id IS NULL
                      UNION SELECT c.category_id FROM categories c JOIN d ON c.parent_id = d.id) SELECT COUNT(*) FROM d""").fetchone()[0]
print("forced move 5 under 9 without the check: rows reachable from the root drop from 10 to", reach, "(Electronics, Phones, Laptops, Android are now a detached cycle)")
# a naive delete without recursion
c3 = load()
c3.execute("DELETE FROM categories WHERE category_id = 5")
print("plain DELETE of category 5 leaves orphans:", [r[0] for r in c3.execute("SELECT category_id FROM categories WHERE parent_id IS NOT NULL AND parent_id NOT IN (SELECT category_id FROM categories) ORDER BY 1")])

# foreign key with ON DELETE CASCADE does the same without a recursive query, but only with the pragma on
def fk_run(pragma):
    c = sqlite3.connect(":memory:")
    c.execute(f"PRAGMA foreign_keys = {pragma}")
    c.executescript("""
    CREATE TABLE cat(category_id INTEGER PRIMARY KEY, parent_id INTEGER REFERENCES cat(category_id) ON DELETE CASCADE, name TEXT);
    INSERT INTO cat VALUES (1,NULL,'Store'),(5,1,'Electronics'),(6,5,'Phones'),(7,5,'Laptops'),(9,6,'Android'),(8,1,'Garden');""")
    c.execute("DELETE FROM cat WHERE category_id = 5")
    return [r[0] for r in c.execute("SELECT category_id FROM cat ORDER BY 1")]
print("ON DELETE CASCADE with foreign_keys = ON leaves", fk_run("ON"), "| with the default (OFF) leaves", fk_run("OFF"))
empty = sqlite3.connect(":memory:")
empty.execute("CREATE TABLE categories(category_id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT, path TEXT)")
print("delete a missing id:", load().execute(SQL_MAIN.replace("= 5", "= 999")).rowcount, "rows | empty table:", empty.execute(SQL_MAIN).rowcount, "rows")
print("asserts passed")
