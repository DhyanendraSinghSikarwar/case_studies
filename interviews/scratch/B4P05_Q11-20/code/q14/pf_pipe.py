from prefect import flow, task


@task
def extract() -> str:
    return "s3://b/raw"


@task(retries=2)
def train(p: str) -> str:
    return "model"


@task
def evaluate(m: str) -> float:
    return 0.9


@flow
def ml_pipe():
    return evaluate(train(extract()))
