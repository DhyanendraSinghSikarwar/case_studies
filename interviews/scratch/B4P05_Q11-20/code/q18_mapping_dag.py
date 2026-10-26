import pendulum
from airflow.sdk import dag, task, get_current_context

START = pendulum.datetime(2026, 1, 1, tz="UTC")


@dag(dag_id="map_train", schedule=None, start_date=START, catchup=False)
def map_train():
    @task
    def list_params() -> list[dict]:
        # small, JSON-able list (it goes through XCom). No network call at PARSE time.
        return [{"region": r, "lr": lr} for r, lr in [("north", 0.1), ("south", 0.1), ("east", 0.01), ("west", 0.01)]]

    @task(max_active_tis_per_dag=2)          # at most 2 mapped copies at once
    def train(cfg: dict, epochs: int) -> dict:
        idx = get_current_context()["ti"].map_index
        print(f"MAP_INDEX={idx} region={cfg['region']} lr={cfg['lr']} epochs={epochs}")
        return {"region": cfg["region"], "score": round(0.9 - cfg["lr"], 2)}

    @task
    def pick_best(results: list[dict]):
        best = max(results, key=lambda r: r["score"])
        print("RESULTS_COUNT=", len(results), "BEST=", best)

    pick_best(train.partial(epochs=3).expand(cfg=list_params()))


map_train()


@dag(dag_id="map_empty", schedule=None, start_date=START, catchup=False)
def map_empty():
    @task
    def nothing() -> list[int]:
        return []

    @task
    def work(x: int):
        print("never printed", x)

    @task(trigger_rule="all_done")
    def after():
        print("AFTER_RAN")

    work.expand(x=nothing()) >> after()


map_empty()
