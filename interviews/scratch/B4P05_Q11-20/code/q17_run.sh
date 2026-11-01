set -e
H=/tmp/claude-0/b5p05_q11_20/q17; rm -rf $H; mkdir -p $H/dags; cp q17_pool_dag.py $H/dags/
export AIRFLOW_HOME=$H AIRFLOW__CORE__DAGS_FOLDER=$H/dags AIRFLOW__CORE__LOAD_EXAMPLES=False
AF=/tmp/claude-0/b5p05/af/bin/airflow
$AF db migrate >/dev/null 2>&1
$AF pools list 2>&1 | grep -v -i warn
$AF pools set gpu 4 "4 GPUs on the training cluster" 2>&1 | tail -4
$AF pools list 2>&1 | grep -v -i warn
$AF dags test gpu_sweep 2026-10-01 2>&1 | grep -oE "Returned value was: trial-[0-9]-done" | sort | uniq -c
