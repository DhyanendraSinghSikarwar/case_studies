from pendulum import datetime
from airflow.sdk import dag, task

@dag(schedule="@daily", start_date=datetime(2026, 1, 1, tz="UTC"), catchup=False,
     default_args={"retries": 2}, tags=["ml"])
def ml_train():
    @task
    def extract(ds=None):
        return f"s3://bucket/raw/{ds}.parquet"

    @task
    def train(uri: str):
        print(f"training on {uri}")
        return "model-v1"

    @task
    def evaluate(model: str):
        print(f"evaluating {model}")
        return {"auc": 0.91}

    evaluate(train(extract()))

ml_train()
