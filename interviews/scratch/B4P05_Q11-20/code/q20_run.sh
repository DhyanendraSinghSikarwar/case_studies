set -e
H=/tmp/claude-0/b5p05_q11_20/q20; rm -rf $H; mkdir -p $H/dags; cp q20_secrets_dag.py $H/dags/
export AIRFLOW_HOME=$H AIRFLOW__CORE__DAGS_FOLDER=$H/dags AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW_CONN_WAREHOUSE='postgresql://etl_user:S3cretPassw0rd@db.internal:5432/analytics'
export AIRFLOW_VAR_MODEL_API_KEY='sk-demo-123456789'
export AIRFLOW_VAR_REGION='ap-south-1'
AF=/tmp/claude-0/b5p05/af/bin/airflow
$AF db migrate >/dev/null 2>&1
$AF connections get warehouse 2>&1 | tail -3 || true
$AF dags test secrets_demo 2026-10-01 > $H/run.log 2>&1 || echo "exit $?"
grep -E "CONN host|LEAK_TEST" $H/run.log | sed -E 's/.*(CONN host|LEAK_TEST)/\1/' | cut -c1-140
echo "raw secret anywhere in log? $(grep -c -e S3cretPassw0rd -e sk-demo-123456789 $H/run.log)"
