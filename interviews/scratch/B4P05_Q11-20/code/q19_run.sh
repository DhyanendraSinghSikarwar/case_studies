H=/tmp/claude-0/b5p05_q11_20/q19; rm -rf $H; mkdir -p $H
export AIRFLOW_HOME=$H AIRFLOW__CORE__LOAD_EXAMPLES=False PYTHONDONTWRITEBYTECODE=1
cd q19
/tmp/claude-0/b5p05/af/bin/airflow db migrate >/dev/null 2>&1
/tmp/claude-0/b5p05/af/bin/python -m pytest -q -p no:cacheprovider tests 2>&1 | tail -25
