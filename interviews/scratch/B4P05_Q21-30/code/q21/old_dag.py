# Airflow 2 style DAG (what a legacy fleet looks like)
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.datasets import Dataset

features = Dataset("s3://bucket/features/")

def train(**ctx):
    print("run for", ctx["execution_date"])

with DAG("old_train", schedule_interval="@daily", start_date=datetime(2026, 1, 1), catchup=False) as dag:
    PythonOperator(task_id="train", python_callable=train, outlets=[features])
