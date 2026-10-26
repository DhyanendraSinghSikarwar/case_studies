from prefect import flow, task
calls = {"n": 0}

@task(retries=2, retry_delay_seconds=0)
def flaky_load():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ValueError("transient")
    return "loaded"

@flow(name="lab-flow")
def lab_flow():
    return flaky_load()

if __name__ == "__main__":
    print("result:", lab_flow(), "calls:", calls["n"])
