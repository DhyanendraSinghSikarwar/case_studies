import pendulum
from airflow.sdk import dag, task

@dag(dag_id="gate", schedule=None, start_date=pendulum.datetime(2026, 1, 1), catchup=False,
     default_args={"retries": 0}, tags=["lab"])
def gate():
    @task
    def load():
        return {"rows": 3, "null_rate": 0.4}          # pretend this came from the upstream table
    @task
    def validate(stats: dict):
        if stats["rows"] < 5 or stats["null_rate"] > 0.1:
            raise ValueError(f"data contract broken: {stats}")
        return "ok"
    @task
    def train(flag: str):
        print("TRAINING STARTED")
    train(validate(load()))
gate()
