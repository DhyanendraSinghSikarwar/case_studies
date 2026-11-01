# Q10: bill of materials explosion with quantity multiplication (a DAG, not a tree)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE parts(part_id TEXT, sub_part_id TEXT, qty INTEGER);
INSERT INTO parts VALUES
 ('BIKE','FRAME',1), ('BIKE','FRONT_ASSY',1), ('BIKE','REAR_ASSY',1), ('BIKE','SEAT',1),
 ('FRONT_ASSY','WHEEL',1), ('FRONT_ASSY','FORK',1), ('FRONT_ASSY','BRAKE',1),
 ('REAR_ASSY','WHEEL',1),  ('REAR_ASSY','CHAIN',1), ('REAR_ASSY','BRAKE',1),
 ('WHEEL','SPOKE',36), ('WHEEL','RIM',1), ('WHEEL','TYRE',1);
"""
SQL_PATHS = """
WITH RECURSIVE bom(part, mult, path) AS (
  SELECT sub_part_id, qty, :product || '>' || sub_part_id FROM parts WHERE part_id = :product
  UNION ALL
  SELECT p.sub_part_id, b.mult * p.qty, b.path || '>' || p.sub_part_id
  FROM parts p JOIN bom b ON p.part_id = b.part
  WHERE instr('>' || b.path || '>', '>' || p.sub_part_id || '>') = 0     -- cycle guard: no part inside itself
)
SELECT part, mult, path FROM bom ORDER BY path
"""
SQL_MAIN = """
WITH RECURSIVE bom(part, mult, path) AS (
  SELECT sub_part_id, qty, :product || '>' || sub_part_id FROM parts WHERE part_id = :product
  UNION ALL
  SELECT p.sub_part_id, b.mult * p.qty, b.path || '>' || p.sub_part_id
  FROM parts p JOIN bom b ON p.part_id = b.part
  WHERE instr('>' || b.path || '>', '>' || p.sub_part_id || '>') = 0
)
SELECT part, SUM(mult) AS total_qty, COUNT(*) AS paths
FROM bom
WHERE NOT EXISTS (SELECT 1 FROM parts x WHERE x.part_id = bom.part)      -- raw component: never used as a parent
GROUP BY part
ORDER BY part
"""
SQL_UNION_BAD = """
WITH RECURSIVE bom(part, mult) AS (
  SELECT sub_part_id, qty FROM parts WHERE part_id = :product
  UNION                                                                  -- collapses equal (part, mult) rows from different paths
  SELECT p.sub_part_id, b.mult * p.qty FROM parts p JOIN bom b ON p.part_id = b.part
)
SELECT part, SUM(mult) AS total_qty FROM bom
WHERE NOT EXISTS (SELECT 1 FROM parts x WHERE x.part_id = bom.part)
GROUP BY part ORDER BY part
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
P = {"product": "BIKE"}
paths = pd.read_sql_query(SQL_PATHS, con, params=P)
print(paths.to_string(index=False))
sql_df = pd.read_sql_query(SQL_MAIN, con, params=P)
print(sql_df.to_string(index=False))
bad = pd.read_sql_query(SQL_UNION_BAD, con, params=P)
print("UNION version (wrong):", dict(zip(bad.part, bad.total_qty)))

parts = pd.read_sql_query("SELECT * FROM parts", con)
# pd:main
def explode(parts, product):
    frontier = (parts[parts["part_id"] == product]
                .assign(path=lambda d: product + ">" + d["sub_part_id"])
                .rename(columns={"sub_part_id": "part", "qty": "mult"})[["part", "mult", "path"]])
    out = [frontier]
    for _ in range(len(parts)):                                  # depth cap: a path cannot be longer than the table
        if frontier.empty:
            break
        nxt = frontier.merge(parts, left_on="part", right_on="part_id")
        ok = pd.Series([(">" + d + ">") not in (">" + p + ">") for d, p in zip(nxt["sub_part_id"], nxt["path"])], index=nxt.index, dtype=bool)
        nxt = nxt[ok]                                            # visited check (an explicit bool Series: an empty list would select no columns)
        frontier = pd.DataFrame({"part": nxt["sub_part_id"], "mult": nxt["mult"] * nxt["qty"], "path": nxt["path"] + ">" + nxt["sub_part_id"]})
        out.append(frontier)
    return pd.concat(out, ignore_index=True)
pd_paths = explode(parts, "BIKE").sort_values("path").reset_index(drop=True)
raw = pd_paths[~pd_paths["part"].isin(parts["part_id"])]
pd_df = (raw.groupby("part", as_index=False).agg(total_qty=("mult", "sum"), paths=("mult", "size")))
# pd:end
pd.testing.assert_frame_equal(pd_paths, paths, check_dtype=False)            # ordered by path
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)              # ordered by part
assert dict(zip(sql_df.part, sql_df.total_qty)) == {"BRAKE": 2, "CHAIN": 1, "FORK": 1, "FRAME": 1, "RIM": 2, "SEAT": 1, "SPOKE": 72, "TYRE": 2}
print("pandas equals SQL (paths ordered by path, totals by part)")
print("pandas drop_duplicates on (part, mult) as the UNION analogue:",
      pd_paths[["part", "mult"]].drop_duplicates().pipe(lambda d: d[~d.part.isin(parts.part_id)]).groupby("part")["mult"].sum().to_dict())

# Edge cases
print("unknown product:", con.execute(SQL_MAIN, {"product": "UNICYCLE"}).fetchall(), "| raw part as product:", con.execute(SQL_MAIN, {"product": "SEAT"}).fetchall())
print("sub-assembly WHEEL on its own:", con.execute(SQL_MAIN, {"product": "WHEEL"}).fetchall())
con.execute("INSERT INTO parts VALUES ('BIKE','SEAT',1)")
print("duplicate BIKE-SEAT row: SEAT total =", {r[0]: r[1] for r in con.execute(SQL_MAIN, P)}["SEAT"])
con.execute("DELETE FROM parts WHERE rowid = (SELECT max(rowid) FROM parts)")
con.execute("UPDATE parts SET qty = NULL WHERE part_id = 'REAR_ASSY' AND sub_part_id = 'CHAIN'")
print("NULL qty on REAR_ASSY-CHAIN: CHAIN total =", [r for r in con.execute(SQL_MAIN, P) if r[0] == "CHAIN"])
con.execute("UPDATE parts SET qty = 1 WHERE part_id = 'REAR_ASSY' AND sub_part_id = 'CHAIN'")
con.execute("INSERT INTO parts VALUES ('WHEEL','BIKE',1)")      # a data error: a wheel contains a bike
print("cyclic BOM with the path guard:", [(r[0], r[1]) for r in con.execute(SQL_MAIN, P)])
unguarded = SQL_PATHS.replace("  WHERE instr('>' || b.path || '>', '>' || p.sub_part_id || '>') = 0     -- cycle guard: no part inside itself\n", "").replace("ORDER BY path", "LIMIT 40")
print("cyclic BOM, no guard, LIMIT 40: rows =", len(con.execute(unguarded, P).fetchall()), "| longest path:", max(len(r[2]) for r in con.execute(unguarded, P)), "characters")
print("asserts passed")
