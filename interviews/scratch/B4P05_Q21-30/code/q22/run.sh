#!/bin/bash
# Q22 driver: parse producer/consumer DAGs, run the producer with dags test, read asset tables from SQLite.
D=/tmp/claude-0/b5p05_q21_30/q22; HERE=$(cd "$(dirname "$0")" && pwd); A=/tmp/claude-0/b5p05/af/bin
export AIRFLOW_HOME=$D/home AIRFLOW__CORE__LOAD_EXAMPLES=False AIRFLOW__CORE__DAGS_FOLDER=$D/dags
rm -rf $D; mkdir -p $D/dags $D/home; cp $HERE/ml_dags.py $D/dags
$A/airflow db migrate >/dev/null 2>&1
$A/python -I $HERE/check.py $D/dags 2>&1 | grep -v "Z \["
echo "--- dags test build_features (producer only; no scheduler running)"
$A/airflow dags test build_features 2026-10-01 2>&1 | grep -E "^wrote|DagRun Finished" | sed -E 's/.*DagRun Finished: (dag_id=[a-z0-9_]+).*(state=[a-z]+), run_type.*/DagRun Finished: \1 \2/'
echo "--- asset tables in the metadata DB"
$A/python -I - <<PY
import sqlite3, glob
db = sqlite3.connect("$D/home/airflow.db")
print("asset rows:", db.execute("select name, uri from asset").fetchall())
print("asset events:", db.execute("select count(*) from asset_event").fetchone()[0])
print("consumer dag run rows:", db.execute("select count(*) from dag_run where dag_id='train_on_features'").fetchone()[0])
PY
