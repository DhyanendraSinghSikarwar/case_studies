import pendulum
from airflow.sdk import dag, task


def clean_rows(rows):
    """Plain function: unit-testable without Airflow."""
    return [r for r in rows if r is not None and r >= 0]


@dag(dag_id="good_train", schedule="@daily", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
     catchup=False, tags=["ml"], default_args={"owner": "ml-team", "retries": 2})
def good_train():
    @task
    def extract() -> str:
        return "s3://bucket/raw"

    @task
    def train(path: str):
        print("train on", path)

    train(extract())


good_train()
