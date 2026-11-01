#!/bin/bash
# Q23 driver: run the pure checks, parse the DAG (callback + deadline), then dags test with a task that fails.
D=/tmp/claude-0/b5p05_q21_30/q23; HERE=$(cd "$(dirname "$0")" && pwd); A=/tmp/claude-0/b5p05/af/bin
export AIRFLOW_HOME=$D/home AIRFLOW__CORE__LOAD_EXAMPLES=False AIRFLOW__CORE__DAGS_FOLDER=$D/dags
rm -rf $D; mkdir -p $D/dags $D/home; cp $HERE/checks.py $HERE/health_dag.py $D/dags
echo "--- pure checks"; python3 -I $HERE/checks.py
$A/airflow db migrate >/dev/null 2>&1
echo "--- DagBag parse"
$A/python -I - <<PY 2>&1 | grep -v "Z \["
import sys; sys.path.insert(0, "'$D/dags'")  # -I drops the DAGs folder from sys.path; the real DAG processor adds it
import sys; sys.path.insert(0, "$D/dags")  # python -I drops the DAGs folder from sys.path; Airflow adds it itself
from airflow.dag_processing.dagbag import DagBag
b = DagBag(dag_folder="$D/dags"); d = b.dags["health_demo"]
print("import_errors:", b.import_errors, "| deadline alerts attached:", len(d.deadline or []))
print("dag-level on_failure_callback in default_args:", d.default_args["on_failure_callback"].__name__)
PY
echo "--- dags test (check task is expected to fail)"
$A/airflow dags test health_demo 2026-10-01 2>&1 | grep -E "^ALERT|^ValueError: data check|DagRun Finished" | sed -E 's/.*DagRun Finished: (dag_id=[a-z0-9_]+).*(state=[a-z]+), run_type.*/DagRun Finished: \1 \2/' | cut -c1-220
