H=/tmp/claude-0/b5p05_q11_20/q16; rm -rf $H; mkdir -p $H
export AIRFLOW_HOME=$H AIRFLOW__CORE__LOAD_EXAMPLES=False
AF=/tmp/claude-0/b5p05/af/bin/airflow
echo "# 1. env-var form: get-value echoes the env var (it does NOT prove the key exists)"
AIRFLOW__CORE__EXECUTOR=CeleryExecutor AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0 $AF config get-value celery broker_url 2>&1 | tail -1
AIRFLOW__CELERY__BROKR_URL=oops $AF config get-value celery brokr_url 2>&1 | tail -1
echo "# 2. validate key names in a CLEAN env (no AIRFLOW__ vars): a 'not found' warning means unknown key"
check() { out=$($AF config get-value "$1" "$2" 2>&1); if echo "$out" | grep -q "not found in config"; then echo "UNKNOWN  $1/$2"; else echo "known    $1/$2 = $(echo "$out" | tail -1 | cut -c1-60)"; fi; }
check core executor
check core parallelism
check core max_active_tasks_per_dag
check celery broker_url
check celery worker_concurrency
check kubernetes_executor namespace
check kubernetes_executor pod_template_file
check core executr
check scheduler min_file_process_interval
check dag_processor min_file_process_interval
echo "# 3. executor classes importable in this venv?"
/tmp/claude-0/b5p05/af/bin/python -I - <<'PY' 2>&1 | grep -v -i warn
import importlib
for m in ["airflow.executors.local_executor", "airflow.providers.celery.executors.celery_executor", "airflow.providers.cncf.kubernetes.executors.kubernetes_executor"]:
    try: importlib.import_module(m); print("importable:", m)
    except Exception as e: print("NOT installed:", m, "-", type(e).__name__)
PY
