import pendulum
from airflow.sdk import dag, task


@dag(dag_id="ml_pipe", schedule="@daily", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False)
def ml_pipe():
    @task
    def extract() -> str:
        return "s3://b/raw"

    @task(retries=2)
    def train(p: str) -> str:
        return "model"

    @task
    def evaluate(m: str) -> float:
        return 0.9

    evaluate(train(extract()))


ml_pipe()
