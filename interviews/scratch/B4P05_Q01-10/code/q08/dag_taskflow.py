from pendulum import datetime
from airflow.sdk import dag, task

@dag(dag_id="two_step_taskflow", schedule=None, start_date=datetime(2026, 1, 1, tz="UTC"), catchup=False)
def two_step():
    @task(multiple_outputs=True)
    def prepare(n_rows: int = 100) -> dict:
        return {"path": "/data/train.parquet", "rows": n_rows}

    @task
    def train(path: str, rows: int) -> str:
        print(f"train on {path} with {rows} rows")
        return "model-v1"

    @task.virtualenv(requirements=["scikit-learn==1.5.2"], system_site_packages=False)
    def isolated_score():
        import sklearn
        return sklearn.__version__

    out = prepare()
    train(out["path"], out["rows"])
    isolated_score()   # parsed only; a real run builds a venv and pip-installs

two_step()
