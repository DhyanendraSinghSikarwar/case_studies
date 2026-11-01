from kfp import dsl, compiler

@dsl.component(base_image="python:3.12")
def add(a: int, b: int) -> int:
    return a + b

@dsl.pipeline(name="lab-pipeline")
def lab_pipeline(x: int = 1):
    t = add(a=x, b=2)
    t.set_caching_options(False)

compiler.Compiler().compile(lab_pipeline, "lab_pipeline.yaml")
print("compiled")
