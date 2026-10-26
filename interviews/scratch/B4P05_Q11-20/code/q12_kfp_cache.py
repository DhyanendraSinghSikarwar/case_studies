from kfp import dsl, compiler
import yaml


@dsl.component(base_image="python:3.12")
def fetch(day: str) -> str:
    return f"s3://bucket/raw/{day}.parquet"


@dsl.component(base_image="python:3.12")
def train(path: str) -> str:
    return f"model from {path}"


@dsl.pipeline(name="cache-demo")
def p(day: str = "2026-10-01"):
    f = fetch(day=day)
    f.set_caching_options(False)       # always re-fetch: data behind the path may change
    train(path=f.output)               # default: cache allowed


compiler.Compiler().compile(p, "q12.yaml")
spec = list(yaml.safe_load_all(open("q12.yaml")))[0]
for name, t in spec["root"]["dag"]["tasks"].items():
    print(name, "-> cachingOptions:", t.get("cachingOptions", "(absent)"))

# the run-level switch is a submit-time argument; check it exists in the installed SDK
import inspect, kfp
sig = inspect.signature(kfp.Client.create_run_from_pipeline_func)
print("enable_caching in create_run_from_pipeline_func:", "enable_caching" in sig.parameters,
      "default:", sig.parameters["enable_caching"].default)
