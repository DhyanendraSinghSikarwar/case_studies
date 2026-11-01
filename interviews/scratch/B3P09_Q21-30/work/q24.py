import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE adj(id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT);
INSERT INTO adj VALUES
 (1,NULL,'Root'),(2,1,'Electronics'),(3,1,'Books'),(4,2,'Phones'),(5,2,'Laptops'),
 (6,3,'Fiction'),(7,4,'iOS'),(9,4,'Android');
"""
BUILD = """
CREATE TABLE mat(id INTEGER PRIMARY KEY, path TEXT);
INSERT INTO mat
WITH RECURSIVE t(id, path) AS (
  SELECT id, '/' || id || '/' FROM adj WHERE parent_id IS NULL
  UNION ALL
  SELECT a.id, t.path || a.id || '/' FROM adj a JOIN t ON a.parent_id = t.id
)
SELECT id, path FROM t;
CREATE TABLE closure(ancestor INTEGER, descendant INTEGER, depth INTEGER, PRIMARY KEY (ancestor, descendant));
INSERT INTO closure
WITH RECURSIVE c(ancestor, descendant, depth) AS (
  SELECT id, id, 0 FROM adj
  UNION ALL
  SELECT c.ancestor, a.id, c.depth + 1 FROM c JOIN adj a ON a.parent_id = c.descendant
)
SELECT ancestor, descendant, depth FROM c;
CREATE INDEX closure_desc ON closure(descendant, ancestor);
"""
Q = {
 "adjacency": {
  "desc": """WITH RECURSIVE d(id) AS (SELECT id FROM adj WHERE parent_id = 4
             UNION ALL SELECT a.id FROM adj a JOIN d ON a.parent_id = d.id) SELECT id FROM d ORDER BY id""",
  "anc": """WITH RECURSIVE u(id, parent_id) AS (SELECT id, parent_id FROM adj WHERE id = 9
            UNION ALL SELECT a.id, a.parent_id FROM adj a JOIN u ON a.id = u.parent_id)
            SELECT id FROM u WHERE id <> 9 ORDER BY id""",
  "depth": """WITH RECURSIVE t(id, depth) AS (SELECT id, 0 FROM adj WHERE parent_id IS NULL
              UNION ALL SELECT a.id, t.depth + 1 FROM adj a JOIN t ON a.parent_id = t.id)
              SELECT id, depth FROM t ORDER BY id"""},
 "materialized path": {
  "desc": "SELECT n.id FROM mat n, mat t WHERE t.id = 4 AND n.path LIKE t.path || '%' AND n.id <> 4 ORDER BY n.id",
  "anc": "SELECT a.id FROM mat a, mat t WHERE t.id = 9 AND t.path LIKE a.path || '%' AND a.id <> 9 ORDER BY a.id",
  "depth": "SELECT id, length(path) - length(replace(path, '/', '')) - 2 AS depth FROM mat ORDER BY id"},
 "nested sets": {
  "desc": "SELECT n.id FROM ns n, ns t WHERE t.id = 4 AND n.lft > t.lft AND n.rgt < t.rgt ORDER BY n.id",
  "anc": "SELECT a.id FROM ns a, ns t WHERE t.id = 9 AND a.lft < t.lft AND a.rgt > t.rgt ORDER BY a.id",
  "depth": "SELECT n.id, (SELECT COUNT(*) FROM ns a WHERE a.lft < n.lft AND a.rgt > n.rgt) AS depth FROM ns n ORDER BY n.id"},
 "closure table": {
  "desc": "SELECT descendant FROM closure WHERE ancestor = 4 AND depth > 0 ORDER BY descendant",
  "anc": "SELECT ancestor FROM closure WHERE descendant = 9 AND depth > 0 ORDER BY ancestor",
  "depth": "SELECT descendant, depth FROM closure WHERE ancestor = 1 ORDER BY descendant"},
}
MOVE_MAT = """
UPDATE mat SET path = '/1/3/' || substr(path, length('/1/2/') + 1)
WHERE path LIKE '/1/2/4/%'
"""
MOVE_CLOSURE_DELETE = """
DELETE FROM closure
WHERE descendant IN (SELECT descendant FROM closure WHERE ancestor = 4)
  AND ancestor IN (SELECT ancestor FROM closure WHERE descendant = 4 AND ancestor <> 4)
"""
MOVE_CLOSURE_INSERT = """
INSERT INTO closure
SELECT sup.ancestor, sub.descendant, sup.depth + sub.depth + 1
FROM closure sup, closure sub
WHERE sup.descendant = 3 AND sub.ancestor = 4
"""

def build_nested_sets(con):
    kids = {}
    for i, p in con.execute("SELECT id, parent_id FROM adj ORDER BY id"):
        kids.setdefault(p, []).append(i)
    out, counter = [], [0]
    def visit(i):
        counter[0] += 1
        lft = counter[0]
        for c in kids.get(i, []):
            visit(c)
        counter[0] += 1
        out.append((i, lft, counter[0]))
    visit(kids[None][0])
    con.execute("DROP TABLE IF EXISTS ns")
    con.execute("CREATE TABLE ns(id INTEGER PRIMARY KEY, lft INTEGER, rgt INTEGER)")
    con.executemany("INSERT INTO ns VALUES (?, ?, ?)", out)

def run_all(con):
    return {m: {k: con.execute(q).fetchall() for k, q in qs.items()} for m, qs in Q.items()}

def agree(res):
    base = res["adjacency"]
    for m, r in res.items():
        assert r == base, (m, r, base)

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
con.executescript(BUILD)
build_nested_sets(con)
print("nested sets (id, lft, rgt):", con.execute("SELECT * FROM ns ORDER BY lft").fetchall())
print("materialized paths:", con.execute("SELECT id, path FROM mat ORDER BY id").fetchall())
print("closure rows:", con.execute("SELECT COUNT(*) FROM closure").fetchone()[0], "for 8 nodes (8 self rows + one per ancestor-descendant pair)")
before = run_all(con)
agree(before)
print("\nBefore the move, the four models agree. descendants of 4:", [r[0] for r in before["adjacency"]["desc"]],
      "| ancestors of 9:", [r[0] for r in before["adjacency"]["anc"]])
print("depth by id:", dict(before["adjacency"]["depth"]))

# pandas: adjacency walk for paths, then prefix tests on the path column and pair rows for the closure
adj = pd.read_sql_query("SELECT * FROM adj", con)
adj["parent_id"] = adj["parent_id"].astype("Int64")

# pd:main
parent = dict(zip(adj["id"], adj["parent_id"]))
def chain(i):
    out = [i]
    while not pd.isna(parent[out[-1]]):
        out.append(int(parent[out[-1]]))
    return out[::-1]
paths = pd.Series({i: "/" + "/".join(map(str, chain(i))) + "/" for i in adj["id"]}).rename_axis("id").rename("path").reset_index()
p4 = paths.loc[paths["id"] == 4, "path"].item()
p9 = paths.loc[paths["id"] == 9, "path"].item()
pd_desc = paths.loc[paths["path"].str.startswith(p4) & (paths["id"] != 4), "id"].sort_values().tolist()
pd_anc = sorted(int(x) for x in p9.strip("/").split("/") if int(x) != 9)
pd_depth = dict(zip(paths["id"], paths["path"].str.count("/") - 2))
pairs = pd.DataFrame([(a, i, k) for i in adj["id"] for k, a in enumerate(chain(i)[::-1])],
                     columns=["ancestor", "descendant", "depth"])
# pd:end
assert pd_desc == [r[0] for r in before["adjacency"]["desc"]]
assert pd_anc == [r[0] for r in before["adjacency"]["anc"]]
assert pd_depth == dict(before["adjacency"]["depth"])
sql_pairs = pd.read_sql_query("SELECT ancestor, descendant, depth FROM closure ORDER BY ancestor, descendant", con)
pd.testing.assert_frame_equal(pairs.sort_values(["ancestor", "descendant"]).reset_index(drop=True), sql_pairs, check_dtype=False)
print("pandas path, prefix and pair frames equal the SQL results (pairs compared after sorting by ancestor, descendant)")

# the move: subtree 4 goes under 3
changes = {}
con.execute("UPDATE adj SET parent_id = 3 WHERE id = 4")
changes["adjacency"] = con.execute("SELECT changes()").fetchone()[0]
con.execute(MOVE_MAT)
changes["materialized path"] = con.execute("SELECT changes()").fetchone()[0]
old_ns = dict((i, (l, r)) for i, l, r in con.execute("SELECT * FROM ns"))
build_nested_sets(con)
new_ns = dict((i, (l, r)) for i, l, r in con.execute("SELECT * FROM ns"))
changes["nested sets (rebuild)"] = sum(old_ns[i] != new_ns[i] for i in old_ns)
con.execute(MOVE_CLOSURE_DELETE)
deleted = con.execute("SELECT changes()").fetchone()[0]
con.execute(MOVE_CLOSURE_INSERT)
inserted = con.execute("SELECT changes()").fetchone()[0]
changes["closure table"] = f"{deleted} deleted + {inserted} inserted"
after = run_all(con)
agree(after)
print("\nAfter moving 4 under 3 the four models still agree. ancestors of 9 now:", [r[0] for r in after["adjacency"]["anc"]],
      "| depth of 9 now:", dict(after["adjacency"]["depth"])[9])
print("rows changed by the move:", changes)
print("nested sets after:", sorted(new_ns.items()))

print("\nEXPLAIN QUERY PLAN for the materialized-path prefix lookup:")
con.execute("CREATE INDEX mat_path ON mat(path)")
for label, q in [("LIKE on a default-collation index", "SELECT id FROM mat WHERE path LIKE '/1/3/4/%'"),
                 ("range on the same index", "SELECT id FROM mat WHERE path >= '/1/3/4/' AND path < '/1/3/40'")]:
    print(" ", label, "->", [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + q)])
con.execute("DROP INDEX mat_path")
con.execute("CREATE INDEX mat_path ON mat(path COLLATE NOCASE)")
print("  LIKE on a NOCASE index ->", [r[3] for r in con.execute("EXPLAIN QUERY PLAN SELECT id FROM mat WHERE path LIKE '/1/3/4/%'")])
print("asserts passed")
