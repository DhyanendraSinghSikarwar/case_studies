import boto3
from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
import pendulum

s3 = boto3.client("s3")
with DAG("bad2", schedule=None, start_date=pendulum.datetime(2026, 1, 1), tags=["ml"],
         default_args={"owner": "x"}) as d:
    BashOperator(task_id="b", bash_command="echo hi")
