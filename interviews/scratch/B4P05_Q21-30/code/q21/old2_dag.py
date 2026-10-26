# Airflow 2 style, but without the Dataset import: only schedule_interval and execution_date
from datetime import datetime
from airflow import DAG
from airflow.decorators import task

with DAG("old2_train", schedule_interval="@daily", start_date=datetime(2026, 1, 1), catchup=False) as dag:
    @task
    def train(execution_date=None):
        print("run for", execution_date)
    train()
