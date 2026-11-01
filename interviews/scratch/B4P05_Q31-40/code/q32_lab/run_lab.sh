#!/bin/bash
# runs the three lab pieces with throwaway homes outside the repo
B=/tmp/claude-0/b5p05; T=$(mktemp -d /tmp/claude-0/b5p05_q31_40/lab.XXXX); D=$(cd "$(dirname "$0")"; pwd)
echo "== Airflow dags test"
AIRFLOW_HOME=$T/af AIRFLOW__CORE__DAGS_FOLDER=$D/dags AIRFLOW__CORE__LOAD_EXAMPLES=False $B/af/bin/airflow db migrate >/dev/null 2>&1
AIRFLOW_HOME=$T/af AIRFLOW__CORE__DAGS_FOLDER=$D/dags AIRFLOW__CORE__LOAD_EXAMPLES=False $B/af/bin/airflow dags test ml_train 2026-10-01 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | grep -E "^training on|^evaluating|Pushing xcom|DagRun Finished|Marking run" | sed -E 's/^[^ ]+ \[info *\] //; s/ ti=.*task_id=.([a-z_]+).*/ task_id=\1/' | cut -c1-170
echo "== Prefect flow"
PREFECT_HOME=$T/pf $B/pf/bin/python -I $D/pf_flow.py 2>&1 | grep -E "Retry|Completed|result:" | sed 's/\x1b\[[0-9;]*m//g' | cut -c1-160
echo "== kfp compile"
(cd $T && $B/kf/bin/python -I $D/kfp_pipe.py && head -3 lab_pipeline.yaml && grep -c "" lab_pipeline.yaml)
rm -rf $T
