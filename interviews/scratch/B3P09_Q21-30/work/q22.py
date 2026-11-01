import sqlite3
from graphlib import TopologicalSorter, CycleError
import networkx as nx
import pandas as pd

SCHEMA = """
CREATE TABLE tasks(task_id TEXT, depends_on TEXT);
INSERT INTO tasks VALUES
 ('A',NULL),('F',NULL),('B','A'),('C','A'),('D','B'),('D','C'),('E','D'),('E','A'),('G','F'),('D','B');
-- X and Y wait for each other, Z waits for Y; none of them is reachable from a task without dependencies
CREATE TABLE tasks_cyc(task_id TEXT, depends_on TEXT);
INSERT INTO tasks_cyc VALUES
 ('A',NULL),('B','A'),('X','Y'),('Y','X'),('Z','Y');
-- trap: X also depends on a normal task A, so the loop can be entered from a root
CREATE TABLE tasks_mix(task_id TEXT, depends_on TEXT);
INSERT INTO tasks_mix VALUES
 ('A',NULL),('B','A'),('X','A'),('X','Y'),('Y','X'),('Z','Y');
"""
SQL_MAIN = """
WITH RECURSIVE stage(task_id, depth) AS (
  SELECT task_id, 0 FROM tasks
  GROUP BY task_id
  HAVING COUNT(depends_on) = 0
  UNION ALL
  SELECT t.task_id, s.depth + 1
  FROM tasks t JOIN stage s ON t.depends_on = s.task_id
  WHERE s.depth < 50
)
SELECT task_id, MAX(depth) AS stage, COUNT(*) AS paths_seen
FROM stage
GROUP BY task_id
ORDER BY stage, task_id
"""
SQL_NOSTAGE = """
WITH RECURSIVE stage(task_id, depth) AS (
  SELECT task_id, 0 FROM tasks
  GROUP BY task_id
  HAVING COUNT(depends_on) = 0
  UNION ALL
  SELECT t.task_id, s.depth + 1
  FROM tasks t JOIN stage s ON t.depends_on = s.task_id
  WHERE s.depth < 50
)
SELECT DISTINCT task_id FROM tasks
WHERE task_id NOT IN (SELECT task_id FROM stage)
ORDER BY task_id
"""
SQL_SELF_REACH = """
WITH RECURSIVE w(start, cur) AS (
  SELECT task_id, depends_on FROM tasks WHERE depends_on IS NOT NULL
  UNION
  SELECT w.start, t.depends_on
  FROM w JOIN tasks t ON t.task_id = w.cur
  WHERE t.depends_on IS NOT NULL
)
SELECT DISTINCT start AS task_in_cycle FROM w WHERE cur = start ORDER BY 1
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)

def swap(sql, table):
    return sql.replace("FROM tasks", f"FROM {table}").replace("JOIN tasks", f"JOIN {table}")

sql_dag = pd.read_sql_query(SQL_MAIN, con)
print("DAG: tasks with no stage:", [r[0] for r in con.execute(SQL_NOSTAGE)])
print("DAG, stage = longest chain below the task (paths_seen = rows the CTE produced for it):")
print(sql_dag.to_string(index=False))

# pd:main
def stages_pandas(tasks):
    edges = tasks.dropna(subset=["depends_on"]).drop_duplicates()
    nodes = set(tasks["task_id"])
    ndeps = edges.groupby("task_id").size()
    stage = {t: 0 for t in nodes - set(ndeps.index)}
    r = 0
    while True:
        r += 1
        e = edges[~edges["task_id"].isin(stage)]
        done = e["depends_on"].isin(stage).groupby(e["task_id"]).sum()
        ready = done[done == ndeps.reindex(done.index)].index
        if len(ready) == 0:
            break
        stage.update({t: r for t in ready})
    return pd.DataFrame({"task_id": list(stage), "stage": list(stage.values())})
# pd:end

tasks = pd.read_sql_query("SELECT * FROM tasks", con)
pd_dag = stages_pandas(tasks).sort_values(["stage", "task_id"]).reset_index(drop=True)
# compare after ordering by stage, task_id (the SQL ORDER BY)
pd.testing.assert_frame_equal(pd_dag, sql_dag[["task_id", "stage"]], check_dtype=False)
print("pandas layer loop equals SQL")

# graphlib: dependencies as {task: {what it waits for}}
deps = {}
for t, d in con.execute("SELECT task_id, depends_on FROM tasks").fetchall():
    deps.setdefault(t, set())
    if d is not None:
        deps[t].add(d)
ts = TopologicalSorter(deps)
ts.prepare()
gl, k = {}, 0
while ts.is_active():
    batch = ts.get_ready()
    for t in batch:
        gl[t] = k
    ts.done(*batch)
    k += 1
G = nx.DiGraph()
G.add_nodes_from(deps)
G.add_edges_from((d, t) for t, ds in deps.items() for d in ds)      # edge: prerequisite -> task
nxg = {t: i for i, gen in enumerate(nx.topological_generations(G)) for t in gen}
assert gl == nxg == dict(zip(sql_dag["task_id"], sql_dag["stage"]))
print("graphlib batches and networkx topological_generations equal the SQL stages")

for table in ("tasks_cyc", "tasks_mix"):
    q = swap(SQL_MAIN, table)
    got = pd.read_sql_query(q, con)
    print(f"\n{table}: stages from the recursive CTE (depth cap 50)")
    print(got.to_string(index=False))
    all_tasks = [r[0] for r in con.execute(f"SELECT DISTINCT task_id FROM {table} ORDER BY 1")]
    nostage = [r[0] for r in con.execute(swap(SQL_NOSTAGE, table))]
    assert nostage == sorted(set(all_tasks) - set(got["task_id"]))
    print("  tasks with no stage (SQL_NOSTAGE):", nostage)
    print("  tasks that reach themselves:", [r[0] for r in con.execute(swap(SQL_SELF_REACH, table))])
    t2 = pd.read_sql_query(f"SELECT * FROM {table}", con)
    s2 = stages_pandas(t2)
    print("  pandas layer loop stages:", dict(zip(s2["task_id"], s2["stage"])))
    d2 = {}
    for t, d in con.execute(f"SELECT task_id, depends_on FROM {table}").fetchall():
        d2.setdefault(t, set())
        if d is not None:
            d2[t].add(d)
    try:
        TopologicalSorter(d2).prepare()
    except CycleError as ex:
        print("  graphlib CycleError, cycle found:", ex.args[1])
    G2 = nx.DiGraph([(d, t) for t, ds in d2.items() for d in ds])
    try:
        list(nx.topological_generations(G2))
    except nx.NetworkXUnfeasible as ex:
        print("  networkx NetworkXUnfeasible:", ex)
    print("  networkx find_cycle:", nx.find_cycle(G2))
print("asserts passed")
