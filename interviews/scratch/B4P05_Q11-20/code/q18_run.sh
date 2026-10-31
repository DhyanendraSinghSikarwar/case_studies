set -e
H=/tmp/claude-0/b5p05_q11_20/q18; rm -rf $H; mkdir -p $H/dags; cp q18_mapping_dag.py $H/dags/
export AIRFLOW_HOME=$H AIRFLOW__CORE__DAGS_FOLDER=$H/dags AIRFLOW__CORE__LOAD_EXAMPLES=False
AF=/tmp/claude-0/b5p05/af/bin/airflow
$AF db migrate >/dev/null 2>&1
for d in map_train map_empty; do
  echo "=== dags test $d"
  $AF dags test $d 2026-10-01 > $H/$d.log 2>&1 || echo "exit $?"
  grep -E "MAP_INDEX|RESULTS_COUNT|AFTER_RAN|never printed" $H/$d.log | sed -E 's/.*(MAP_INDEX|RESULTS_COUNT|AFTER_RAN|never printed)/\1/' | cut -c1-120
  grep -E "DagRun Finished" $H/$d.log | sed -E 's/.*(state=[a-z]+).*/\1/' | head -1
  grep -iE "skipped|error" $H/$d.log | cut -c1-200 | head -3
done
