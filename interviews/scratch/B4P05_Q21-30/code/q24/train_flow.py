from prefect import flow, task, get_run_logger


@task
def load(rows: int) -> list[int]:
    return list(range(rows))


@flow(name="train", log_prints=True)
def train(rows: int = 5, lr: float = 0.1, dry_run: bool = False):
    data = load(rows)
    print(f"rows={len(data)} lr={lr} dry_run={dry_run}")
    return "skipped" if dry_run else f"trained on {len(data)} rows"


if __name__ == "__main__":
    # run once, locally, with different parameters (no server needed)
    print(train())
    print(train(rows=12, lr=0.01))
    print(train(rows=3, dry_run=True))
    try:
        train(rows="many")
    except Exception as e:
        print("bad parameter ->", type(e).__name__, str(e).splitlines()[0][:100])
