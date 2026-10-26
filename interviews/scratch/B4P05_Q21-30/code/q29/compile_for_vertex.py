from kfp import compiler, dsl


@dsl.component(base_image="python:3.12")
def train(lr: float) -> float:
    return round(1.0 - abs(lr - 0.01) * 10, 3)


@dsl.pipeline(name="vertex-demo", pipeline_root="gs://YOUR_BUCKET/pipeline_root")   # placeholder bucket
def vertex_demo(lr: float = 0.01):
    train(lr=lr).set_cpu_limit("2").set_memory_limit("4G")


compiler.Compiler().compile(vertex_demo, "vertex_demo.yaml")
