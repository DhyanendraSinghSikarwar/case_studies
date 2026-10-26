#!/bin/bash
# Q21 driver: parse old and new style DAGs, then run the two that parse. Own AIRFLOW_HOME in /tmp.
D=/tmp/claude-0/b5p05_q21_30/q21; HERE=$(cd "$(dirname "$0")" && pwd)
A=/tmp/claude-0/b5p05/af/bin
export AIRFLOW_HOME=$D/home AIRFLOW__CORE__LOAD_EXAMPLES=False
rm -rf $D; mkdir -p $D/home
for n in old:old_dag old2:old2_dag old3:old3_dag new:new_dag; do mkdir -p $D/${n%%:*}; cp $HERE/${n##*:}.py $D/${n%%:*}/; done
$A/airflow db migrate >/dev/null 2>&1
echo "airflow $($A/airflow version)"
for d in old old2 old3 new; do $A/python -I $HERE/parse.py $D/$d 2>&1 | grep -E "^(file|dags|import_errors|warnings)"; done
echo "--- dags test"
for p in old3:old3_train new:new_train; do
  AIRFLOW__CORE__DAGS_FOLDER=$D/${p%%:*} $A/airflow dags test ${p##*:} 2026-10-01 2>&1 | grep -E "^(keys has|run for)|DagRun Finished" | sed -E 's/.*DagRun Finished: (dag_id=[a-z0-9_]+).*(state=[a-z]+), run_type.*/DagRun Finished: \1 \2/' 
done
