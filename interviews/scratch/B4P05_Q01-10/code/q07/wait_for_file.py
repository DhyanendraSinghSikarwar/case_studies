from datetime import timedelta
from pendulum import datetime
from airflow.sdk import dag, task
from airflow.providers.standard.sensors.filesystem import FileSensor

LANDING = "/tmp/claude-0/b5p05_q1_10/q7/landing/_SUCCESS"

@dag(schedule=None, start_date=datetime(2026, 1, 1, tz="UTC"), catchup=False)
def wait_for_file():
    wait = FileSensor(
        task_id="wait_for_success_marker",
        filepath=LANDING,
        fs_conn_id="fs_default",
        mode="reschedule",          # frees the worker slot between pokes
        poke_interval=2,
        timeout=60,
        soft_fail=False,
    )

    @task
    def train():
        print("marker found, training starts")

    wait >> train()

wait_for_file()
