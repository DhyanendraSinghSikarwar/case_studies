from kfp import dsl, compiler
from kfp.dsl import Input, Output, Dataset, Model, Metrics


@dsl.component(base_image="python:3.12", packages_to_install=["pandas==2.2.3"])
def make_data(out: Output[Dataset], n: int = 100):
    import pandas as pd  # imports INSIDE the function: only the body is shipped
    pd.DataFrame({"x": range(n)}).to_csv(out.path, index=False)


@dsl.component(base_image="python:3.12")
def train(data: Input[Dataset], model: Output[Model], metrics: Output[Metrics], lr: float = 0.1):
    with open(data.path) as f:
        rows = sum(1 for _ in f) - 1
    with open(model.path, "w") as f:
        f.write(f"model trained on {rows} rows")
    metrics.log_metric("rows", rows)


@dsl.container_component
def notify(msg: str):
    return dsl.ContainerSpec(image="alpine:3.20", command=["echo"], args=[msg])


@dsl.pipeline(name="three-kinds")
def p(n: int = 100):
    d = make_data(n=n)
    t = train(data=d.outputs["out"])
    notify(msg="done")


if __name__ == "__main__":
    compiler.Compiler().compile(p, "q11.yaml")
    import yaml
    spec = list(yaml.safe_load_all(open("q11.yaml")))[0]
    print("components:", list(spec["components"]))
    for name, ex in spec["deploymentSpec"]["executors"].items():
        c = ex["container"]
        print(f"\n== {name}: image={c['image']}")
        print("command[:2]:", c["command"][:2])
        print("args-tail:", " ".join(c.get("args", []))[-120:] if name!="exec-notify" else c.get("args"))
        if name == "exec-notify": print("command:", c["command"])
    t = spec["components"]["comp-train"]["inputDefinitions"]["artifacts"]
    print("\ntrain input artifacts:", t)
    print("train output artifacts:", spec["components"]["comp-train"]["outputDefinitions"]["artifacts"])
    print("train params:", spec["components"]["comp-train"]["inputDefinitions"]["parameters"])

    # packages_to_install shows up as pip installs inside the step command
    import re
    for n in ("exec-make-data", "exec-train"):
        cmd = " ".join(spec["deploymentSpec"]["executors"][n]["container"]["command"])
        print(n, "pip installs:", re.findall(r"install\s+--quiet\s+--no-warn-script-location\s+'([^']+)'", cmd))
    # component from YAML: compile the component alone, load it back
    from kfp import components
    compiler.Compiler().compile(notify, "notify.yaml")
    loaded = components.load_component_from_file("notify.yaml")
    print("loaded from YAML:", type(loaded).__name__, "inputs:", list(loaded.component_spec.inputs))
