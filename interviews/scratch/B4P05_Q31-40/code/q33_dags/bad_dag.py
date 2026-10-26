import pendulum, requests
from airflow.sdk import dag, task

CFG = requests.get("https://example.com/config").json()   # top-level network call

@dag(dag_id="bad", schedule="@daily", start_date=pendulum.datetime(2026, 1, 1), catchup=False)
def bad():
    @task
    def t():
        return 1
    t()
bad()
