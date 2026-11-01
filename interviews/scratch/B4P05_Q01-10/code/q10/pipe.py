from kfp import dsl, compiler
from kfp.dsl import Input, Output, Dataset, Model, Metrics

@dsl.component(base_image="python:3.12")
def make_data(n_rows: int, out: Output[Dataset]):
    with open(out.path, "w") as f:
        for i in range(n_rows):
            f.write(f"{i},{i % 2}\n")

@dsl.component(base_image="python:3.12")
def train(data: Input[Dataset], lr: float, model: Output[Model], metrics: Output[Metrics]) -> str:
    rows = sum(1 for _ in open(data.path))
    open(model.path, "w").write(f"model trained on {rows} rows, lr={lr}")
    metrics.log_metric("rows", rows)
    return "ok"

@dsl.pipeline(name="two-step-demo", description="make data then train")
def two_step(n_rows: int = 100, lr: float = 0.1):
    d = make_data(n_rows=n_rows)
    train(data=d.outputs["out"], lr=lr)

if __name__ == "__main__":
    compiler.Compiler().compile(two_step, "two_step.yaml")
    print("compiled")
