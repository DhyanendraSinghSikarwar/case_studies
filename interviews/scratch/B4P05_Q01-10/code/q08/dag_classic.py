from pendulum import datetime
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

def prepare(n_rows=100, **_):
    return {"path": "/data/train.parquet", "rows": n_rows}

def train(ti, **_):
    out = ti.xcom_pull(task_ids="prepare")          # you wire the XCom yourself
    print(f"train on {out['path']} with {out['rows']} rows")
    return "model-v1"

with DAG("two_step_classic", schedule=None, start_date=datetime(2026, 1, 1, tz="UTC"), catchup=False):
    p = PythonOperator(task_id="prepare", python_callable=prepare)
    t = PythonOperator(task_id="train", python_callable=train)
    p >> t
