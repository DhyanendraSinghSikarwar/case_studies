from datetime import timedelta
from prefect import flow, task
from prefect.cache_policies import NO_CACHE
from prefect.task_runners import ThreadPoolTaskRunner

CALLS = {"fetch": 0}


def fetch_key(context, parameters):
    """Cache on the inputs that decide the data, not on object identity."""
    return f"data-{parameters['day']}"


@task(retries=2, retry_delay_seconds=0, cache_key_fn=fetch_key, cache_expiration=timedelta(hours=1), persist_result=True)
def fetch(day: str) -> list[float]:
    CALLS["fetch"] += 1
    if CALLS["fetch"] == 1:
        raise ConnectionError("flaky source, first call fails")   # retried by Prefect
    return [1.0, 2.0, 3.0, 4.0]


@task(cache_policy=NO_CACHE)
def train(model: str, data: list[float], lr: float) -> dict:
    score = round(sum(data) / len(data) * lr * (2 if model == "gbm" else 1), 4)
    return {"model": model, "score": score}


def alert(flow, flow_run, state):
    print(f"ON_FAILURE hook: flow run {flow_run.name!r} ended in {state.name}: {state.message[:60]}")


@flow(name="train-many", task_runner=ThreadPoolTaskRunner(max_workers=3), on_failure=[alert], log_prints=True)
def train_many(day: str = "2026-10-01", lr: float = 0.5):
    if lr <= 0:                                  # fail fast, before any work
        raise ValueError(f"lr must be > 0, got {lr}")
    data = fetch(day)
    futures = [train.submit(m, data, lr) for m in ("logreg", "gbm", "mlp")]   # three tasks in parallel threads
    results = [f.result() for f in futures]
    best = max(results, key=lambda r: r["score"])
    print("best:", best)
    return best


if __name__ == "__main__":
    print("RESULT 1:", train_many())                       # fetch fails once, retries, succeeds
    print("RESULT 2:", train_many())                       # same day: fetch comes from cache
    print("RESULT 3:", train_many(day="2026-10-02"))       # new day: new cache key, fetch runs again
    print("fetch body ran", CALLS["fetch"], "times in total")
    try:
        train_many(lr=0)
    except ValueError as e:
        print("RESULT 4 (bad param): ValueError:", e)
