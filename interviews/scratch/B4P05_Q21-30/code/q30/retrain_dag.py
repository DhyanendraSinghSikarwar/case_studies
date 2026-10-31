import pendulum
from airflow.sdk import Param, dag, get_current_context, task


@dag(
    schedule=None,  # started by a trigger, never by the clock
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False,
    params={
        "data_end": Param("2026-10-01", type="string", pattern=r"^\d{4}-\d{2}-\d{2}$"),
        "lookback_days": Param(30, type="integer", minimum=1, maximum=365),
        "model_version": Param("auto", type="string"),
        "dry_run": Param(False, type="boolean"),
        "reason": Param("manual", type="string"),
    },
)
def retrain():
    @task
    def plan():
        p = get_current_context()["params"]
        print(f"PLAN reason={p['reason']!r} window={p['lookback_days']}d ending {p['data_end']} version={p['model_version']} dry_run={p['dry_run']}")
        return dict(p)

    @task
    def train(p: dict):
        if p["dry_run"]:
            print("TRAIN skipped (dry_run=True): would train and register nothing")
            return "skipped"
        print(f"TRAIN fit on {p['lookback_days']} days ending {p['data_end']}")
        return "trained"

    train(plan())


retrain()
