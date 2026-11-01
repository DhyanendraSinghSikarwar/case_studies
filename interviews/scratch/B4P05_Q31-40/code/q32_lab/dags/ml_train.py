from __future__ import annotations
import pendulum
from airflow.sdk import dag, task

@dag(dag_id="ml_train", schedule="@daily", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
     catchup=False, default_args={"retries": 2}, tags=["ml", "lab"])
def ml_train():
    @task
    def extract(ds=None):
        return {"path": f"s3://bucket/raw/{ds}.parquet"}
    @task
    def train(meta: dict):
        print("training on", meta["path"]); return "model-v1"
    @task
    def evaluate(model: str):
        print("evaluating", model); return 0.91
    evaluate(train(extract()))
ml_train()
