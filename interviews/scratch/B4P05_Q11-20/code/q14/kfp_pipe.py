from kfp import dsl


@dsl.component(base_image="python:3.12")
def extract() -> str:
    return "s3://b/raw"


@dsl.component(base_image="python:3.12")
def train(p: str) -> str:
    return "model"


@dsl.component(base_image="python:3.12")
def evaluate(m: str) -> float:
    return 0.9


@dsl.pipeline
def ml_pipe():
    e = extract()
    t = train(p=e.output).set_retry(num_retries=2)
    evaluate(m=t.output)
