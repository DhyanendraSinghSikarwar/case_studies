from pendulum import datetime
from airflow.sdk import dag, task

@dag(schedule="@daily", start_date=datetime(2026, 1, 1, tz="UTC"), catchup=False,
     default_args={"retries": 1}, tags=["ml", "training"], params={"prod_auc": 0.90})
def daily_train():
    @task
    def ingest(ds=None):
        return f"s3://lake/raw/dt={ds}"

    @task
    def validate(uri: str):
        print("validated", uri)       # in real life: schema, null rate, row count; raise to stop
        return uri

    @task
    def build_features(uri: str):
        return uri.replace("raw", "features")

    @task
    def train(features: str):
        print("submit training job for", features, "(delegated; Airflow only waits)")
        return {"model_uri": features.replace("features", "models") + "/model.pkl", "auc": 0.93}

    @task
    def evaluate(result: dict):
        return result

    @task.branch
    def gate(result: dict, params=None):
        better = result["auc"] > params["prod_auc"]
        print(f"candidate auc {result['auc']} vs prod {params['prod_auc']} -> {'register' if better else 'skip_register'}")
        return "register" if better else "skip_register"

    @task
    def register(result: dict):
        print("registered", result["model_uri"])

    @task
    def skip_register():
        print("kept production model")

    @task(trigger_rule="none_failed_min_one_success")
    def notify():
        print("notify team: run finished")

    r = evaluate(train(build_features(validate(ingest()))))
    g = gate(r)
    g >> [register(r), skip_register()] >> notify()

daily_train()
