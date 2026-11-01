from airflow.dag_processing.dagbag import DagBag
import sys
bag = DagBag(dag_folder=sys.argv[1])
print("import_errors:", bag.import_errors)
for d in sorted(bag.dags.values(), key=lambda d: d.dag_id):
    s = d.schedule
    if isinstance(s, str): shown = repr(s)
    elif isinstance(s, list): shown = "assets " + str([a.uri for a in s])
    else: shown = type(s).__name__
    print(f"{d.dag_id:18} timetable={type(d.timetable).__name__:22} schedule={shown}")
    outs = sorted(a.uri for t in d.tasks for a in getattr(t, "outlets", []) if hasattr(a, "uri"))
    if outs: print("                   task outlets:", outs)
