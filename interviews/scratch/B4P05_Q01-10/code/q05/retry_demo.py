from datetime import timedelta
from pendulum import datetime
from airflow.sdk import dag, task

def alert(context):
    ti = context["ti"]
    print(f"ALERT callback: {ti.task_id} failed on try {ti.try_number}")

@dag(schedule=None, start_date=datetime(2026, 1, 1, tz="UTC"), catchup=False,
     default_args={"retries": 2, "retry_delay": timedelta(seconds=1), "on_failure_callback": alert})
def retry_demo():
    @task(execution_timeout=timedelta(minutes=5))
    def flaky_fetch(ti=None):
        print("attempt number", ti.try_number)
        if ti.try_number < 3:
            raise RuntimeError(f"upstream 503 on try {ti.try_number}")
        return "rows=100"

    @task(retries=0)
    def always_fails():
        raise ValueError("bad schema")

    @task(trigger_rule="all_done")
    def cleanup():
        print("cleanup runs even though a sibling failed")

    done = cleanup()
    [flaky_fetch(), always_fails()] >> done

retry_demo()
