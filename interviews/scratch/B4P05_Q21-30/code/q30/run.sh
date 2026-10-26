#!/bin/bash
# Q30 driver: decision function, DagBag parse of both DAGs, dags test with --conf (3 runs).
D=/tmp/claude-0/b5p05_q21_30/q30; HERE=$(cd "$(dirname "$0")" && pwd); A=/tmp/claude-0/b5p05/af/bin
export AIRFLOW_HOME=$D/home AIRFLOW__CORE__LOAD_EXAMPLES=False AIRFLOW__CORE__DAGS_FOLDER=$D/dags
rm -rf $D; mkdir -p $D/dags $D/home; cp $HERE/retrain_dag.py $HERE/trigger_dag.py $D/dags
echo "--- decide()"; python3 -I $HERE/triggers.py
$A/airflow db migrate >/dev/null 2>&1
echo "--- DagBag"
$A/python -I -c "
from airflow.dag_processing.dagbag import DagBag
b = DagBag(dag_folder='$D/dags'); print('import_errors:', b.import_errors); print(sorted(b.dags))" 2>&1 | grep -v "Z \["
run() { echo "--- dags test retrain $*"; $A/airflow dags test retrain 2026-10-26 "$@" 2>&1 | grep -E "^(PLAN|TRAIN)|DagRun Finished|Invalid|ValueError|ParamValidationError|rror:" | sed -E 's/.*DagRun Finished: (dag_id=[a-z0-9_]+).*(state=[a-z]+), run_type.*/DagRun Finished: \1 \2/' | cut -c1-200 | head -6; }
run
run --conf '{"reason":"drift: PSI 0.31","lookback_days":14,"data_end":"2026-10-25","dry_run":true}'
run --conf '{"lookback_days":9999}'
