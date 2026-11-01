from prefect import flow, task, get_run_logger

calls = {"n": 0}


@task(retries=2, retry_delay_seconds=0)
def flaky_fetch(day: str) -> str:
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError(f"try {calls['n']} failed")
    return f"data-{day}"


@flow(name="train-flow")
def train_flow(day: str = "2026-10-01", epochs: int = 3) -> str:
    log = get_run_logger()
    data = flaky_fetch(day)
    log.info("training %s for %d epochs", data, epochs)
    return "ok"


if __name__ == "__main__":
    print("RETURN:", train_flow(day="2026-10-02", epochs=5), "calls:", calls["n"])
    try:
        train_flow(day="x", epochs="many")       # bad type: validated before running
    except Exception as e:
        print("VALIDATION:", type(e).__name__, str(e).splitlines()[0][:120])
    # .fn runs the raw Python function with no orchestration (no retries, no states)
    calls["n"] = 5
    print("PLAIN TASK .fn:", flaky_fetch.fn("2026-10-03"))
    try:
        train_flow.fn()                      # get_run_logger() needs a run context
    except Exception as e:
        print("PLAIN FLOW .fn:", type(e).__name__, "-", e)
