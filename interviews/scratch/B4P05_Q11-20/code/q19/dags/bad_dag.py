import pendulum
from airflow.sdk import dag, task


@dag(dag_id="bad_no_retries", schedule="@daily", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
     catchup=False, tags=["ml"], default_args={"owner": "ml-team"})   # retries missing on purpose
def bad_no_retries():
    @task
    def only():
        pass

    only()


bad_no_retries()
