# Airflow 2 style: provider-less PythonOperator import and 'schedule' fine; execution_date only used at run time
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def train(**ctx):
    print("keys has execution_date:", "execution_date" in ctx, "| has logical_date:", "logical_date" in ctx)

with DAG("old3_train", schedule="@daily", start_date=datetime(2026, 1, 1), catchup=False) as dag:
    PythonOperator(task_id="train", python_callable=train)
