from datetime import datetime, timedelta, timezone
import pendulum
from airflow.sdk import dag, task
from airflow.sdk.definitions.deadline import AsyncCallback, DeadlineAlert, DeadlineReference
from checks import freshness_problem, on_failure, row_count_problem


@dag(
    schedule="@daily", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False,
    default_args={"retries": 1, "retry_delay": timedelta(seconds=1), "on_failure_callback": on_failure},
    # Airflow 3 replacement for SLAs (check current docs for the exact API in your version)
    deadline=DeadlineAlert(
        reference=DeadlineReference.DAGRUN_QUEUED_AT,
        interval=timedelta(hours=2),
        callback=AsyncCallback("checks.notify_async", kwargs={"context_like": "run queued over 2h ago and not finished"}),
    ),
)
def health_demo():
    @task
    def load():
        return {"rows": 0, "last_update": datetime(2026, 10, 24, tzinfo=timezone.utc).isoformat()}

    @task
    def check(stats: dict):
        now = datetime(2026, 10, 26, 12, tzinfo=timezone.utc)
        problems = [p for p in (
            row_count_problem(stats["rows"]),
            freshness_problem(datetime.fromisoformat(stats["last_update"]), now, timedelta(hours=26)),
        ) if p]
        if problems:
            raise ValueError("data check failed: " + "; ".join(problems))

    check(load())


health_demo()
