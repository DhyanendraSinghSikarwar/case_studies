import sys
from airflow.models import DagBag
bag = DagBag(dag_folder=sys.argv[1])
print("import_errors:", bag.import_errors)
for d in bag.dags.values():
    print(d.dag_id, "tasks:", [t.task_id for t in d.tasks])
