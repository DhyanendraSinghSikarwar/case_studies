from pendulum import datetime
from airflow.sdk import dag, task

@dag(schedule="@daily", start_date=datetime(2026, 1, 1, tz="Asia/Kolkata"), catchup=False)
def daily_features():
    @task
    def show(logical_date=None, data_interval_start=None, data_interval_end=None, run_id=None):
        print("run_id              :", run_id)
        print("logical_date        :", logical_date)
        print("data_interval_start :", data_interval_start)
        print("data_interval_end   :", data_interval_end)
        print("tz of start_date    :", data_interval_start.tzinfo)

    show()

daily_features()
