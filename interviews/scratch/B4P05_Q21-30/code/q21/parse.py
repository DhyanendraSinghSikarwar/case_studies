import sys, warnings, os
from airflow.dag_processing.dagbag import DagBag
folder = sys.argv[1]
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    bag = DagBag(dag_folder=folder)
print("file:", os.path.basename(folder))
print("dags:", sorted(bag.dags))
print("import_errors:", {os.path.basename(k): v.strip().splitlines()[-1] for k, v in bag.import_errors.items()})
print("warnings:", sorted({f"{x.category.__name__}: {str(x.message)[:110]}" for x in w if "airflow" in str(x.message).lower() or "Deprec" in x.category.__name__}))
