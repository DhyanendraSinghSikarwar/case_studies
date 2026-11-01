import pendulum
from airflow.sdk import dag, task

@dag(dag_id="good", schedule="@daily", start_date=pendulum.datetime(2026, 1, 1), catchup=False,
     tags=["ml", "team-ranking"], default_args={"owner": "ranking-team", "retries": 2})
def good():
    @task
    def fetch():
        import requests            # network call is inside the task: fine
        return requests.get("https://example.com").status_code
    fetch()
good()
