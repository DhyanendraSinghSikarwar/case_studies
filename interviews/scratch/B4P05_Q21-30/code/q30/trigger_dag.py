import pendulum
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sdk import dag


@dag(schedule="@daily", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False)
def retrain_gate():
    TriggerDagRunOperator(
        task_id="start_retrain", trigger_dag_id="retrain",
        conf={"reason": "gate says yes", "dry_run": True, "data_end": "{{ ds }}"},
        wait_for_completion=False,
    )


retrain_gate()
