# Airflow 3 style DAG
import pendulum
from airflow.sdk import Asset, dag, task

features = Asset("s3://bucket/features/")

@dag(schedule="@daily", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False)
def new_train():
    @task(outlets=[features])
    def train(**context):
        print("run for", context["logical_date"])
    train()

new_train()
