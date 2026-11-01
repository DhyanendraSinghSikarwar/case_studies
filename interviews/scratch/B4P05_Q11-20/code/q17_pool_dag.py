import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="gpu_sweep",
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    max_active_tasks=16,   # per-DAG cap on running task instances
    max_active_runs=1,     # per-DAG cap on concurrent runs
    tags=["ml"],
)
def gpu_sweep():
    @task(pool="gpu", pool_slots=1, priority_weight=5)
    def train(trial: int) -> str:
        return f"trial-{trial}-done"

    train.expand(trial=list(range(6)))


gpu_sweep()
