from pendulum import datetime
from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator

@dag(schedule=None, start_date=datetime(2026, 1, 1, tz="UTC"), catchup=False)
def xcom_demo():
    @task
    def extract(ds=None):
        # heavy data stays in object storage; only the address travels
        return f"s3://ml-bucket/features/dt={ds}/part-0.parquet"

    @task
    def train(uri: str):
        print("reading", uri)
        return {"model_uri": uri.replace("features", "models").replace("part-0.parquet", "model.pkl"), "rows": 1000}

    uri = extract()
    meta = train(uri)
    # classic operator reading the same XCom through Jinja
    BashOperator(task_id="announce",
                 bash_command="echo model at {{ ti.xcom_pull(task_ids='train')['model_uri'] }}") .set_upstream(meta)

xcom_demo()
