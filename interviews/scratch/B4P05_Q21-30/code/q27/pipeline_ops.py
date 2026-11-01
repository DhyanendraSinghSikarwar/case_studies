import inspect
import yaml
from kfp import Client, compiler, dsl


@dsl.component(base_image="python:3.12")
def step(x: int) -> int:
    return x + 1


@dsl.pipeline(name="ops-demo")
def ops_demo(x: int = 1):
    t = step(x=x)
    t.set_retry(num_retries=2, backoff_duration="60s", backoff_factor=2)   # transient node or network failures
    t.set_caching_options(False)                                           # always recompute this step
    t.set_memory_limit("2G")
    t.set_display_name("add-one")


compiler.Compiler().compile(ops_demo, "ops_demo.yaml")
doc = next(yaml.safe_load_all(open("ops_demo.yaml")))
task = doc["root"]["dag"]["tasks"]["step"]
print("retryPolicy:", task["retryPolicy"])
print("cachingOptions:", task["cachingOptions"], "| displayName:", task["taskInfo"]["name"])
for m in ("create_experiment", "run_pipeline", "create_run_from_pipeline_package", "create_recurring_run", "list_runs", "get_run"):
    print(f"Client.{m}:", "exists" if hasattr(Client, m) else "MISSING")
print("create_recurring_run args:", [p for p in inspect.signature(Client.create_recurring_run).parameters][:12])
