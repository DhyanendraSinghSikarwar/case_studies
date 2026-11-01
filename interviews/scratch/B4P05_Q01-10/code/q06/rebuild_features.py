from pendulum import datetime
from airflow.sdk import dag, task

@dag(schedule="@daily", start_date=datetime(2026, 9, 1, tz="UTC"), catchup=False, max_active_runs=3)
def rebuild_features():
    @task
    def rebuild(ds=None):
        # idempotent: overwrite partition dt=ds (see Q3)
        print(f"overwrite partition dt={ds}")

    rebuild()

rebuild_features()
