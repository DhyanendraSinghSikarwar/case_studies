from pendulum import datetime
from airflow.sdk import dag, task
from airflow.providers.standard.sensors.filesystem import FileSensor

@dag(schedule=None, start_date=datetime(2026, 1, 1, tz="UTC"), catchup=False)
def wait_deferrable():
    wait = FileSensor(
        task_id="wait_async",
        filepath="/tmp/claude-0/b5p05_q1_10/q7/landing/_SUCCESS",
        fs_conn_id="fs_default",
        deferrable=True,            # hands the wait to the triggerer process
        poke_interval=2,
    )

    @task
    def train():
        print("marker found (deferrable), training starts")

    wait >> train()

wait_deferrable()
