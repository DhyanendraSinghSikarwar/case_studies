# Book 4 Part 5, Q11-Q20 answers (Wave B)

### Q11 ⭐⭐⭐ 🟡 Kubeflow Pipelines components in depth. Compare lightweight Python components (@dsl.component with base_image and packages_to_install), container components (@dsl.container_component), and loading a component from YAML. Explain Input[Dataset], Output[Model], Output[Metrics], artifact paths, why the function must be self-contained (imports inside), and how packages_to_install slows each step. Compile a pipeline with one of each type and show the generated executor containers. Not run on a cluster.
**Asked at:** Kubeflow Pipelines docs and prep pages (kubeflow.org KFP v2 caching docs, climbtheladder Kubeflow interview questions; search snippets only, not opened); docs and generic prep page, not interview reports; Kubernetes-heavy MLOps and ML platform roles
**Say this first (1 line):** There are three ways to build a Kubeflow step, a Python function that KFP wraps in a container, a container you build yourself, or a ready-made YAML spec, and all three compile into the same pipeline YAML.

**Then explain:**
- **Lightweight Python component** (`@dsl.component`): KFP copies the function source into the step command and runs it inside `base_image`. Only the function body travels. So imports must be inside the function, and module-level helpers or globals are not there at run time (the usual `NameError` in the pod).
- **Container component** (`@dsl.container_component`): you return a `ContainerSpec(image, command, args)`. KFP does not touch your image, so it can be any language and needs no kfp library. Inputs reach it only as placeholders in `args`; outputs must be written to the paths you were given.
- **From YAML** (`components.load_component_from_file`): reuse a component another team published as a spec file. Good for sharing, bad for reading, because the logic is hidden in an image.
- **Parameters versus artifacts:** small values (str, int, float, bool, list, dict) are parameters. Files are artifacts: `Input[Dataset]`, `Output[Model]`, `Output[Metrics]`. In the function you use `.path` for the local file and `.metadata` for extra info; `Output[Metrics]` has `log_metric`. Where the bytes live is the backend's job (object storage); check your deployment.
- **Startup cost:** `packages_to_install` becomes a pip install at the start of every run of that step. In my compile, even `train` (no packages asked) carries a `kfp==2.17.3` install, because the lightweight runtime needs kfp inside the image. So bake heavy dependencies into the image and keep the list short.
- Failure modes: import at file top then used in the function (NameError in the pod); pip install fails in an air-gapped cluster; a parameter without a type annotation (I ran it: `TypeError: Missing type annotation for argument: x` as soon as the decorator runs, because KFP builds the interface from the annotations).

**Example:** `make_data(n=100)` writes a CSV with a header and 100 rows. `train` counts lines minus the header, so `rows = 100`, writes `model trained on 100 rows` to the Model path and logs metric `rows=100`. This arithmetic is from reading the code; the step bodies were not run on a cluster. What I did run is the compile, and I read the executor containers in the YAML.

**Code:**
```python
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
```

**Output (my run):** kfp 2.17.3, Python 3.13, compile only (no cluster, so the steps themselves are **not executed**).
```text
components: ['comp-make-data', 'comp-notify', 'comp-train']

== exec-make-data: image=python:3.12
command[:2]: ['sh', '-c']
args-tail: --executor_input {{$}} --function_to_execute make_data

== exec-notify: image=alpine:3.20
command[:2]: ['echo']
args-tail: ["{{$.inputs.parameters['msg']}}"]
command: ['echo']

== exec-train: image=python:3.12
command[:2]: ['sh', '-c']
args-tail: --executor_input {{$}} --function_to_execute train

train input artifacts: {'data': {'artifactType': {'schemaTitle': 'system.Dataset', 'schemaVersion': '0.0.1'}}}
train output artifacts: {'metrics': {'artifactType': {'schemaTitle': 'system.Metrics', 'schemaVersion': '0.0.1'}}, 'model': {'artifactType': {'schemaTitle': 'system.Model', 'schemaVersion': '0.0.1'}}}
train params: {'lr': {'defaultValue': 0.1, 'isOptional': True, 'parameterType': 'NUMBER_DOUBLE'}}
exec-make-data pip installs: ['pandas==2.2.3', 'kfp==2.17.3']
exec-train pip installs: ['kfp==2.17.3']
loaded from YAML: YamlComponent inputs: ['msg']
```

**Follow-ups:**
1. *Why is kfp installed in every step?* The function runs through a small kfp launcher in the image, so kfp must be importable. You can point to your own kfp package or bake it in (check current docs).
2. *Can I return a model object?* No. Write it to the `Output[Model]` path. Return values are for small parameters.
3. *Which type when?* Pure Python logic: lightweight. Existing image or non-Python tool: container component. Shared team library: YAML or a versioned image.

**Common mistakes:**
- Importing at the top of the file and using it inside the function.
- Returning a DataFrame instead of writing a `Dataset` file.
- Putting 15 pip packages in `packages_to_install` and wondering why each step starts slowly.
- Not setting `base_image`: I saw a `FutureWarning` that the SDK default (python:3.11) will change to python:3.12 on 2027-10-01. Pin it explicitly, and never use `:latest`.

### Q12 ⭐⭐⭐ 🟡 Kubeflow Pipelines caching and re-runs. Explain how step-level caching works (same component spec, same inputs and parameters give a reused output), enable_caching at submit, set_caching_options(False) per task, what breaks it (a changing timestamp input, external data that changed behind the same path), and why cache hits can serve stale data. Show a pipeline that disables caching on a data-fetch step and compile it, pointing at the cache setting in the YAML. Whether a cache hit occurs on a live cluster is not executed.
**Asked at:** Kubeflow Pipelines docs and prep pages (kubeflow.org KFP v2 caching docs, climbtheladder Kubeflow interview questions; search snippets only, not opened); docs and generic prep page, not interview reports; Kubernetes-heavy MLOps and ML platform roles
**Say this first (1 line):** KFP reuses a step's old output when the step's definition and its inputs are the same, which saves time, but it can hand you stale data when the data changed behind an unchanged path, so I switch caching off on fetch steps.

**Then explain:**
- Caching is per step. If the component spec (image, command) and the input values match an earlier run that has a stored output, the backend reuses that output and skips the container. The exact key is backend-defined; check current docs.
- On the compiled YAML the per-task setting is visible: `cachingOptions: {enableCache: true}` or an empty `{}` when you called `set_caching_options(False)`. I confirmed that below.
- Run-level switch: `enable_caching` is an argument when you submit a run (`Client.create_run_from_pipeline_func`). In the installed SDK its default is `None`, so I read that as "do not override"; confirm in docs.
- What breaks a cache: an input that changes every run (a `datetime.now()` string) means no step downstream ever hits. The opposite danger is worse: a fixed path like `s3://bucket/raw/latest.parquet` with new content inside gives a hit and old results.
- Subtle trap (reasoning, not run on a cluster): if the fetch step is uncached but returns the same path string, the next step sees identical inputs and can still hit its cache. Fix by passing a snapshot id or content hash as an input.
- Failure modes: stale model after a data fix; cache hit hides a flaky component; a cache that is never invalidated after you change code but not the image tag.

**Example:** Run 1 for `2026-10-01` trains on `raw/2026-10-01.parquet`. On Oct 2 someone corrects that file. Run 2 has the same `day`, so `train` gets the same input string and may reuse the old model. If `fetch` also returns a content hash (say the file's md5), the input changes and the cache misses, which is what you want.

**Code:**
```python
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
```

**Output (my run):** kfp 2.17.3, compile only. Whether a live cluster hits the cache is **not executed**.
```text
fetch -> cachingOptions: {}
train -> cachingOptions: {'enableCache': True}
enable_caching in create_run_from_pipeline_func: True default: None
```

**Follow-ups:**
1. *Should I turn caching off globally?* Usually not. Cache pure, expensive steps (feature build on a frozen snapshot), not steps that read "latest".
2. *How do I force one rerun?* Submit with caching disabled for that run, or change an input (a run id parameter).
3. *Where is the cache stored?* In the KFP backend metadata, not in your artifact store alone (check your version).

**Common mistakes:**
- Passing a timestamp as an input "for logging" and killing all cache hits.
- Trusting a cache hit after data was rewritten in place.
- Calling `set_caching_options(False)` and assuming downstream steps also rerun.
- Never recording which steps were cache hits when debugging a bad model.

### Q13 ⭐⭐⭐ 🟡 Prefect basics: @flow and @task, running a flow as a normal Python function, parameters with type validation, task retries and retry_delay_seconds, result persistence and caching at concept level, logging and states (Completed, Failed, Retrying). Write a flow with a task that fails twice then succeeds and run it locally with the temporary server. Show the real log lines and the return value. Prefect Cloud and a persistent server are not executed.
**Asked at:** Prefect docs and tutorials (docs.prefect.io concepts and deployments tutorials, MotherDuck Prefect glossary, Tessl registry pages; search snippets only, not opened); docs, no interview question bank found; Python-first data and ML teams
**Say this first (1 line):** In Prefect a flow is just a decorated Python function and a task is a decorated function inside it, so I get retries, states and logs without changing how I write the code.

**Then explain:**
- `@flow` marks the entry point; `@task` marks a unit that gets its own state, retries and logs. A flow runs like a normal call: `train_flow(day="x")`. Calling it starts a temporary local server for the run (I saw "Starting temporary server"); no deployment is needed.
- Parameters are validated with type hints (pydantic). `epochs="many"` for an `int` made the flow fail with `ParameterTypeError` before any task started.
- `@task(retries=2, retry_delay_seconds=0)` retries only that task. States I saw: the task logged "Retry 1/2", "Retry 2/2", then `Completed`; the flow ended `Completed`. Other states exist (Failed, Cancelled and others; check docs).
- Result persistence and caching are opt-in concepts: by default task results are kept in memory for the run. To reuse results across runs you set persistence and a cache policy or key. I did not run that here; check current docs for your version.
- `.fn` runs the raw function with no orchestration. On a task it worked (`flaky_fetch.fn`). On the flow it failed because `get_run_logger()` needs a run context.
- Failure modes: retrying a non-idempotent task (sends two emails); retries mask a real bug if the exception is not transient; swallowing exceptions inside the task so Prefect sees success.

**Example:** `flaky_fetch` raises on calls 1 and 2 and succeeds on call 3. With `retries=2` that is exactly enough: 3 calls in total. With `retries=1` the flow would fail on call 2. Hand-check: calls counter ends at 3 in the output.

**Code:**
```python
from prefect import flow, task, get_run_logger

calls = {"n": 0}


@task(retries=2, retry_delay_seconds=0)
def flaky_fetch(day: str) -> str:
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError(f"try {calls['n']} failed")
    return f"data-{day}"


@flow(name="train-flow")
def train_flow(day: str = "2026-10-01", epochs: int = 3) -> str:
    log = get_run_logger()
    data = flaky_fetch(day)
    log.info("training %s for %d epochs", data, epochs)
    return "ok"


if __name__ == "__main__":
    print("RETURN:", train_flow(day="2026-10-02", epochs=5), "calls:", calls["n"])
    try:
        train_flow(day="x", epochs="many")       # bad type: validated before running
    except Exception as e:
        print("VALIDATION:", type(e).__name__, str(e).splitlines()[0][:120])
    # .fn runs the raw Python function with no orchestration (no retries, no states)
    calls["n"] = 5
    print("PLAIN TASK .fn:", flaky_fetch.fn("2026-10-03"))
    try:
        train_flow.fn()                      # get_run_logger() needs a run context
    except Exception as e:
        print("PLAIN FLOW .fn:", type(e).__name__, "-", e)
```
```bash
export PREFECT_HOME=$(mktemp -d) PREFECT_SERVER_ANALYTICS_ENABLED=false
/tmp/claude-0/b5p05/pf/bin/python -I q13_prefect_basics.py
```

**Output (my run):** prefect 3.9.0, Python 3.13, temporary local server, `PREFECT_HOME` in a temp dir, `PREFECT_SERVER_ANALYTICS_ENABLED=false`. Timestamps removed and long lines cut for space. Prefect Cloud and a persistent server are **not executed**.
```text
INFO    | Task run 'flaky_fetch-8fd' - Task run failed with exception: ConnectionError('try 1 failed') - Retry 1/2 will start immediately
INFO    | Task run 'flaky_fetch-8fd' - Task run failed with exception: ConnectionError('try 2 failed') - Retry 2/2 will start immediately
INFO    | Task run 'flaky_fetch-8fd' - Finished in state Completed()
INFO    | Flow run 'imperial-griffin' - training data-2026-10-02 for 5 epochs
INFO    | Flow run 'imperial-griffin' - Finished in state Completed()
ERROR   | prefect.flows - Parameter validation failed for flow 'train-flow': [{'type': 'int_parsing', 'loc': ('epochs',), 'msg': 'Input should be a valid integer, unable to pa
ERROR   | prefect.engine - Validation of flow parameters failed with error: Flow run received invalid parameters:
INFO    | prefect.engine - Finished in state Failed('Validation of flow parameters failed with error: ParameterTypeError: Flow run received invalid parameters:\n - epochs: Inp
RETURN: ok calls: 3
VALIDATION: ParameterTypeError Flow run received invalid parameters:
PLAIN TASK .fn: data-2026-10-03
PLAIN FLOW .fn: MissingContextError - There is no active flow or task run context.
```

**Follow-ups:**
1. *Flow retries?* `@flow(retries=...)` exists too; it reruns the whole flow, so tasks should be idempotent or cached.
2. *Task failing in a flow, does the flow fail?* Yes by default, if the exception propagates.
3. *Why a server at all?* It stores run state for the UI and API; check docs for how to point at a dedicated one.

**Common mistakes:**
- Treating `retries` as a fix for a deterministic bug.
- Calling `get_run_logger()` in code that is also called outside a run.
- Passing huge objects between tasks and expecting them to be persisted.
- Skipping type hints on flow parameters and losing validation.

### Q14 ⭐⭐⭐ 🟡 Airflow versus Prefect versus Kubeflow Pipelines versus Dagster for ML, in a table: unit of work, scheduling, dynamic and Python-native workflows, Kubernetes fit, UI and lineage, learning curve, ops burden, and where each shines (Airflow for scheduled data work and a big provider ecosystem, KFP for container-per-step on Kubernetes, Prefect for Python-first flows, Dagster for assets). Say how you would choose for a team of four ML engineers with one Kubernetes cluster. Concept answer, with a small script that counts how the same pipeline is declared in each tool; vendor blogs disagree, hedge claims.
**Asked at:** Orchestrator comparison write-ups (zenml.io 'Orchestration showdown: Dagster vs Prefect vs Airflow', risingwave, dzone, deploybase, hightouch; search snippets only, not opened); vendor-adjacent blogs, treat specifics with caution; data and ML platform roles
**Say this first (1 line):** Airflow is the mature scheduler for data work with a huge provider library, Prefect is the lightest Python-first option, Kubeflow Pipelines is container-per-step on Kubernetes, and Dagster models data assets instead of tasks; I pick by what the team already runs and where the heavy compute lives.

**Then explain:**
- The table below is my summary of how each tool is usually described. Vendor blogs disagree, so treat the cells as starting points and check current docs.
- Same three-step pipeline (extract, train, evaluate) written in each tool is 13 to 15 code lines. The tools differ less in writing than in running: who owns the scheduler, where the code executes, and how you see lineage.
- Failure modes by tool: Airflow, heavy top-level code slows parsing and one shared metadata DB becomes a bottleneck. KFP, every step pays image pull and pip install time, and debugging is `kubectl logs`. Prefect, hosted features can differ from self-hosted (a concern for on-prem; check). Dagster, smaller ecosystem and a new mental model.
- **My pick for four ML engineers and one Kubernetes cluster:** if the company already has Airflow, use it and run heavy steps as pods. If not, and the pipelines are mostly Python and scheduled, Prefect is the cheapest to operate. If the steps are GPU container jobs and the team is happy on Kubernetes, KFP fits. If the pain is "what produced this table or model", look at Dagster. Spend a week on a pilot with one real pipeline before deciding.

| | Airflow 3 | Prefect 3 | Kubeflow Pipelines 2 | Dagster |
|---|---|---|---|---|
| Unit of work | task in a DAG | task in a flow | containerised component | asset (or op in a job) |
| Scheduling | built in scheduler, cron, assets | deployments with schedules | recurring runs on the KFP backend | schedules and sensors |
| Python-native / dynamic | TaskFlow, mapping (`expand`) | plain Python, loops, `.submit` | pipeline DSL compiles to YAML; control flow via `dsl.If`, `ParallelFor` | Python, partitions |
| Kubernetes fit | executor or pod operator | Kubernetes work pool | native (every step a pod) | Kubernetes deployment option |
| UI and lineage | strong UI, assets view | strong run UI | run graph plus ML Metadata | asset graph is the core |
| Learning curve | medium | low | medium to high (K8s) | medium (new model) |
| Ops burden | scheduler, DB, workers | server or cloud plus workers | whole KFP backend on K8s | webserver, daemon, DB |
| Shines at | scheduled data and ML jobs, many integrations | Python-first flows, quick start | container-per-step ML on K8s | asset lineage and testing |

**Example:** Team of four, one cluster, nightly retrain with a GPU step. Option A: Airflow with a small Celery or Local setup, GPU step as a Kubernetes pod. Option B: KFP, every step a pod, the cluster is the platform. A needs the team to run a scheduler and a database; B needs the team to run KFP on the cluster. With four people I would pick the one whose server someone already knows how to fix at 2 a.m.

**Code:** the script loads the three declarations that can run here (Airflow, Prefect, KFP compile) and counts lines; the Dagster file is text only.
```python
# ---- file: q14_compare.py ----
"""Same 3-step pipeline in four tools: load each declaration for real where the tool is installed,
count code lines, and note how dependencies are declared."""
import ast
import pathlib
import subprocess
import sys

BASE = pathlib.Path(__file__).parent / "q14"
VENV = "/tmp/claude-0/b5p05"
rows = [
    ("Airflow 3", "af_pipe.py", f"{VENV}/af/bin/python",
     "import runpy; ns=runpy.run_path('{f}'); print('ok')", "data-flow in function calls (TaskFlow)"),
    ("Prefect 3", "pf_pipe.py", f"{VENV}/pf/bin/python",
     "import runpy; ns=runpy.run_path('{f}'); print('ok, flow =', ns['ml_pipe'].name)", "plain function calls inside a flow"),
    ("KFP 2", "kfp_pipe.py", f"{VENV}/kf/bin/python",
     "import runpy; from kfp import compiler; ns=runpy.run_path('{f}'); compiler.Compiler().compile(ns['ml_pipe'], '/tmp/claude-0/b5p05_q11_20/q14.yaml'); print('compiled')",
     ".output of one step passed into the next"),
    ("Dagster", "dagster_pipe.py.txt", None, None, "asset names as function arguments"),
]
print(f"{'tool':10} {'code lines':>10} {'decorators':>10}  {'loaded/compiled':18} dependency style")
for tool, fname, py, snippet, style in rows:
    src = (BASE / fname).read_text()
    lines = [l for l in src.splitlines() if l.strip() and not l.strip().startswith("#")]
    deco = sum(1 for l in lines if l.lstrip().startswith("@"))
    if py:
        r = subprocess.run([py, "-I", "-c", snippet.format(f=BASE / fname)], capture_output=True, text=True)
        status = r.stdout.strip().splitlines()[-1] if r.returncode == 0 and r.stdout.strip() else f"FAILED rc={r.returncode}"
    else:
        status = "not executed"
    print(f"{tool:10} {len(lines):>10} {deco:>10}  {status[:18]:18} {style}")

# ---- file: q14/af_pipe.py ----
import pendulum
from airflow.sdk import dag, task


@dag(dag_id="ml_pipe", schedule="@daily", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False)
def ml_pipe():
    @task
    def extract() -> str:
        return "s3://b/raw"

    @task(retries=2)
    def train(p: str) -> str:
        return "model"

    @task
    def evaluate(m: str) -> float:
        return 0.9

    evaluate(train(extract()))


ml_pipe()

# ---- file: q14/pf_pipe.py ----
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

# ---- file: q14/kfp_pipe.py ----
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
```

**Output (my run):** counts and load checks are real (airflow 3.3.2, prefect 3.9.0, kfp 2.17.3). Dagster is **not executed** (not installed; its snippet is from memory of the asset API, check current docs). Line counts depend on how I formatted the files, so they show "similar", not "shorter".
```text
tool       code lines decorators  loaded/compiled    dependency style
Airflow 3          15          4  ok                 data-flow in function calls (TaskFlow)
Prefect 3          13          4  ok, flow = ml-pipe plain function calls inside a flow
KFP 2              15          4  compiled           .output of one step passed into the next
Dagster            13          3  not executed       asset names as function arguments
```

**Follow-ups:**
1. *Can they be combined?* Yes, commonly: Airflow or Prefect triggers a KFP run, or runs a pod. Cost is two systems to learn.
2. *What about managed Airflow or Vertex?* Less ops, more lock-in (Q29).
3. *Which has the best retries?* All four have retries; settings and defaults differ, so test the failure you care about.

**Common mistakes:**
- Choosing by a blog's "winner" instead of a pilot.
- Ignoring who will operate it.
- Comparing tools on features you will never use.
- Moving big data through the orchestrator in any of them.

### Q15 ⭐⭐⭐ 🟡 Orchestration for ML: why a cron script or a notebook is not enough, and what an orchestrator gives you (dependency order, retries, backfills, state, logs, alerting, parametrised runs, audit trail), what it must not do (carry big data or heavy compute itself), and how an ML pipeline differs from an ETL pipeline (GPU steps, long training, artifact and model versions, evaluation gates, non-deterministic outputs). Give a before and after example: a cron script that retrains weekly versus the same steps as a DAG. Pure concept; a small simulated failure-and-retry script runs locally.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** A cron script runs steps in order and hopes; an orchestrator adds dependencies, retries, state, backfills, logs and alerts, so a failure in step three is visible, retried and resumable instead of silent.

**Then explain:**
- What it gives you: dependency order, retries with delay, run state per step, rerun from the failed step, backfills for past dates, parametrised runs (date, model version), central logs, alerts, and an audit trail of who ran what.
- What it must not do: carry big data or do heavy compute inside its own workers. It should trigger Spark, a GPU pod or a cloud job and pass paths and IDs. Otherwise the scheduler fleet becomes your training cluster.
- ML differs from ETL: GPU and CPU steps mixed, long training that may be preempted, large artifacts, model and data versions to record, an evaluation gate before registering, and outputs that are not bit-for-bit repeatable, so "same input same output" needs seeds and pinned data.
- Failure modes: a notebook that works only in one person's session; a cron that overlaps with itself; a retry that registers the model twice (needs idempotency, Q3); an orchestrator used as a message bus.
- A trap with orchestrators: "retries fix flakiness" can hide a data problem. Alert on the third failure, not only on the final one.

**Example:** Weekly cron retrain. Week 1 `train` crashes, the script dies, nobody is told, the old model stays for a week. Week 2 it works. With the orchestrated version, `train` fails once, is retried and succeeds in the same run; a rerun skips finished steps; a permanent failure raises an alert after 3 attempts. Hand-check the numbers in the output: cron registered 1 model in 2 weeks, orchestrated run registered 1 in one run and still 1 after the rerun.

**Code:** a simulation, not an orchestrator. The "skip finished steps on rerun" is a simplification of "clear failed tasks and rerun"; real orchestrators rerun idempotent tasks, they do not magically know.
```python
"""Before: cron-style script. After: tiny orchestrator with order, state, retries, skip-done, audit log.
Deterministic simulation: the 'train' step fails on its first attempt only."""
import json
import tempfile
from pathlib import Path

# ---------- BEFORE: weekly cron script ----------
def cron_script(env):
    print("[cron] start")
    steps = ["extract", "build_features", "train", "evaluate", "register"]
    for s in steps:
        if s == "train" and env["train_fail_budget"] > 0:
            env["train_fail_budget"] -= 1
            print("[cron] train crashed -> script dies; next run is next week; nobody is told")
            return False
        if s == "register":
            env["models_registered"] += 1
        print(f"[cron] {s} ok")
    return True


env = {"train_fail_budget": 1, "models_registered": 0}
print("--- cron week 1"); cron_script(env)
print("--- cron week 2"); cron_script(env)
print("models registered after 2 weeks:", env["models_registered"], "(one week of stale model, no alert)\n")


# ---------- AFTER: same steps, as a DAG with state ----------
class Run:
    def __init__(self, state_dir, fail_budget):
        self.state = Path(state_dir) / "state.json"
        self.audit = []
        self.fail_budget = fail_budget
        self.registered = 0

    def done(self):
        return json.loads(self.state.read_text()) if self.state.exists() else {}

    def mark(self, step):
        d = self.done(); d[step] = "success"; self.state.write_text(json.dumps(d))

    def call(self, step):
        if step == "train" and self.fail_budget > 0:
            self.fail_budget -= 1
            raise RuntimeError("GPU node preempted")
        if step == "register":
            self.registered += 1

    def run(self, dag, retries=2):
        for step, deps in dag:                       # list is already in dependency order
            assert all(d in self.done() for d in deps), f"{step}: upstream not done"
            if step in self.done():
                self.audit.append(f"{step}: skipped (already success)"); continue
            for attempt in range(1, retries + 2):
                try:
                    self.call(step); self.mark(step)
                    self.audit.append(f"{step}: success (attempt {attempt})"); break
                except RuntimeError as e:
                    self.audit.append(f"{step}: attempt {attempt} failed: {e}")
            else:
                self.audit.append(f"ALERT: {step} failed after {retries + 1} attempts"); return False
        return True


DAG = [("extract", []), ("build_features", ["extract"]), ("train", ["build_features"]),
       ("evaluate", ["train"]), ("register", ["evaluate"])]
with tempfile.TemporaryDirectory() as d:
    r = Run(d, fail_budget=1)
    print("--- orchestrated run, train fails once"); ok = r.run(DAG)
    print("\n".join(r.audit)); print("run ok:", ok, "| registered:", r.registered)
    r.audit.clear()
    print("--- same run again (rerun / duplicate trigger)"); r.run(DAG)
    print("\n".join(r.audit)); print("registered after rerun:", r.registered)
with tempfile.TemporaryDirectory() as d:
    r = Run(d, fail_budget=5)
    print("--- permanent failure"); ok = r.run(DAG)
    print("\n".join(r.audit[-4:])); print("run ok:", ok, "| registered:", r.registered)
```

**Output (my run):** `python3 -I`, deterministic, no orchestrator involved.
```text
--- cron week 1
[cron] start
[cron] extract ok
[cron] build_features ok
[cron] train crashed -> script dies; next run is next week; nobody is told
--- cron week 2
[cron] start
[cron] extract ok
[cron] build_features ok
[cron] train ok
[cron] evaluate ok
[cron] register ok
models registered after 2 weeks: 1 (one week of stale model, no alert)

--- orchestrated run, train fails once
extract: success (attempt 1)
build_features: success (attempt 1)
train: attempt 1 failed: GPU node preempted
train: success (attempt 2)
evaluate: success (attempt 1)
register: success (attempt 1)
run ok: True | registered: 1
--- same run again (rerun / duplicate trigger)
extract: skipped (already success)
build_features: skipped (already success)
train: skipped (already success)
evaluate: skipped (already success)
register: skipped (already success)
registered after rerun: 1
--- permanent failure
train: attempt 1 failed: GPU node preempted
train: attempt 2 failed: GPU node preempted
train: attempt 3 failed: GPU node preempted
ALERT: train failed after 3 attempts
run ok: False | registered: 0
```

**Follow-ups:**
1. *Is cron ever fine?* One independent, idempotent, low-stakes job. The pain starts with the second dependent step.
2. *Why not just use CI?* CI handles code events; it lacks backfills, per-step state and data-interval thinking (Part 7 covers wiring).
3. *Where do models live?* In a registry or object store; the orchestrator holds only the run and the pointer.

**Common mistakes:**
- Moving the cron command into a `BashOperator` and calling it done, with no idempotency.
- Putting data in XCom or in the scheduler's memory.
- No alert on the final failure, only logs.
- Retrying forever.

### Q16 ⭐⭐ 🟡 Airflow executors: Local, Celery, Kubernetes and the older CeleryKubernetes hybrid (check Airflow 3 docs for current names and multi-executor support). Explain how a task gets from the scheduler to a worker, a message broker such as Redis or RabbitMQ for Celery, pod-per-task for Kubernetes with isolation and cold-start cost, and how to choose for a mix of light SQL tasks and heavy training tasks. Give a configuration snippet for each (airflow.cfg or env vars). Validate the config keys against the installed Airflow with airflow config get-value; no Celery or Kubernetes executor is run.
**Asked at:** Airflow guides on executors and operations (datadriven.io executors page, oneuptime.com 'How to Configure Airflow Executors' 2026, datavidhya.com; search snippets only, not opened); generic prep blogs, some inaccurate, check Airflow docs; platform and MLOps roles
**Say this first (1 line):** The executor decides where a task actually runs: Local runs it next to the scheduler, Celery sends it to warm workers through a broker, Kubernetes starts one pod per task, so I choose by isolation needs versus start-up cost.

**Then explain:**
- Flow: the scheduler decides a task instance is ready, hands it to the executor, the executor runs it (a process, a Celery message, a pod) and reports state back through the metadata database.
- **LocalExecutor:** simplest, same machine, limited by that machine. It was the default in my install (`core/executor = LocalExecutor`); some blogs still say SequentialExecutor is the default, which did not match what I saw.
- **CeleryExecutor:** a broker (Redis or RabbitMQ) holds queued tasks, long-running worker processes pick them up. Fast task start, shared dependencies on the worker image, noisy neighbours.
- **KubernetesExecutor:** one pod per task, from a pod template. Strong isolation and per-task resources, but a cold start for every task.
- **Hybrid:** the older `CeleryKubernetesExecutor` mixed both. In recent Airflow the config accepts a list of executors (I set `LocalExecutor,CeleryExecutor` and the config read it back) and a task picks one; I did not run multi-executor, and I believe the old hybrid classes are deprecated or removed, so check Airflow 3 docs.
- **Light SQL tasks plus heavy training:** keep light tasks on warm workers (or Local for a small setup), push training to a pod (`KubernetesPodOperator` or a Kubernetes executor), so torch is not in the Airflow image (Q35).
- Failure modes: broker down means nothing runs; worker OOM kills neighbouring tasks; pod pending because the cluster is full looks like a hung task; a task stuck "queued" because parallelism or pool slots are exhausted.
- Important gotcha I hit: `airflow config get-value` echoes an environment variable even if the key does not exist (a typo `AIRFLOW__CELERY__BROKR_URL` read back fine). Validate names in a clean environment, where an unknown key prints a "not found in config" warning.

**Example:** 300 small SQL checks a day and one 3-hour GPU training. Celery with 8 workers handles the checks in seconds each. A pod per check would add pod start time to 300 tasks, so training alone goes to a pod with `nvidia.com/gpu: 1` (cluster-specific; check your device plugin).

**Code:** env-var form works for every setting (`AIRFLOW__<SECTION>__<KEY>`); same keys go in `airflow.cfg`.
```bash
H=/tmp/claude-0/b5p05_q11_20/q16; rm -rf $H; mkdir -p $H
export AIRFLOW_HOME=$H AIRFLOW__CORE__LOAD_EXAMPLES=False
AF=/tmp/claude-0/b5p05/af/bin/airflow
echo "# 1. env-var form: get-value echoes the env var (it does NOT prove the key exists)"
AIRFLOW__CORE__EXECUTOR=CeleryExecutor AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0 $AF config get-value celery broker_url 2>&1 | tail -1
AIRFLOW__CELERY__BROKR_URL=oops $AF config get-value celery brokr_url 2>&1 | tail -1
echo "# 2. validate key names in a CLEAN env (no AIRFLOW__ vars): a 'not found' warning means unknown key"
check() { out=$($AF config get-value "$1" "$2" 2>&1); if echo "$out" | grep -q "not found in config"; then echo "UNKNOWN  $1/$2"; else echo "known    $1/$2 = $(echo "$out" | tail -1 | cut -c1-60)"; fi; }
check core executor
check core parallelism
check core max_active_tasks_per_dag
check celery broker_url
check celery worker_concurrency
check kubernetes_executor namespace
check kubernetes_executor pod_template_file
check core executr
check scheduler min_file_process_interval
check dag_processor min_file_process_interval
echo "# 3. executor classes importable in this venv?"
/tmp/claude-0/b5p05/af/bin/python -I - <<'PY' 2>&1 | grep -v -i warn
import importlib
for m in ["airflow.executors.local_executor", "airflow.providers.celery.executors.celery_executor", "airflow.providers.cncf.kubernetes.executors.kubernetes_executor"]:
    try: importlib.import_module(m); print("importable:", m)
    except Exception as e: print("NOT installed:", m, "-", type(e).__name__)
PY
```

**Output (my run):** apache-airflow 3.3.2. Config validation only. The Celery and Kubernetes provider packages are not installed in this venv, and no Celery worker, broker or Kubernetes executor was started: **not executed**.
```text
# 1. env-var form: get-value echoes the env var (it does NOT prove the key exists)
redis://redis:6379/0
oops
# 2. validate key names in a CLEAN env (no AIRFLOW__ vars): a 'not found' warning means unknown key
known    core/executor = LocalExecutor
known    core/parallelism = 32
known    core/max_active_tasks_per_dag = 16
known    celery/broker_url = redis://redis:6379/0
known    celery/worker_concurrency = 16
known    kubernetes_executor/namespace = default
known    kubernetes_executor/pod_template_file = 
UNKNOWN  core/executr
UNKNOWN  scheduler/min_file_process_interval
known    dag_processor/min_file_process_interval = 30
# 3. executor classes importable in this venv?
importable: airflow.executors.local_executor
NOT installed: airflow.providers.celery.executors.celery_executor - ModuleNotFoundError
NOT installed: airflow.providers.cncf.kubernetes.executors.kubernetes_executor - ModuleNotFoundError
```

**Follow-ups:**
1. *Where do I set `airflow.cfg` in Kubernetes?* Usually a ConfigMap or env vars in the Helm chart (Part 3 covers Helm).
2. *How many concurrent tasks?* `parallelism` (32 in my default config) caps the whole installation; pools and `max_active_tasks` cap parts.
3. *Celery versus Kubernetes for GPUs?* Kubernetes: per-task resource requests, scale to zero between runs.

**Common mistakes:**
- Using LocalExecutor in production for a team.
- Trusting a config read-back that came from your own env var.
- Putting heavy ML libraries in the shared worker image.
- Forgetting that the scheduler must reach the broker and database.

### Q17 ⭐⭐ 🟡 Airflow pools, concurrency and priority. Explain parallelism, max_active_tasks, max_active_runs, pools and slots (limit calls to a GPU cluster, a database or an API), pool_slots, priority_weight and weight_rule, and queues with Celery. Scenario: 200 dynamic training tasks must not exceed 4 GPUs. Show a pool being created with the CLI or API and a DAG using it; run on SQLite and show the pool listing. A real parallel run on workers is not executed.
**Asked at:** Airflow guides on executors and operations (datadriven.io executors page, oneuptime.com 'How to Configure Airflow Executors' 2026, datavidhya.com; search snippets only, not opened); generic prep blogs, some inaccurate, check Airflow docs; platform and MLOps roles
**Say this first (1 line):** Pools cap how many task instances may hit one scarce resource at once, so for 200 training tasks and 4 GPUs I create a pool with 4 slots and put every training task in it, and Airflow queues the rest.

**Then explain:**
- Layers of limits: `parallelism` (whole installation), `max_active_tasks` per DAG, `max_active_runs` per DAG, `max_active_tis_per_dag` per task, and **pools** per resource. The strictest one wins.
- A pool has N slots. A task takes `pool_slots` slots (default 1) while running. When the pool is full, further tasks wait in the queued state. My install has `default_pool` with 128 slots.
- `priority_weight` and `weight_rule` decide which waiting task gets a free slot first. `queue` is a different thing: it routes to Celery worker groups.
- Mapped tasks (Q18) are limited by `max_map_length` (1024 in my config); 200 is fine.
- Failure modes: a task pointed at a pool name that does not exist (it will not run; check how your version reports this); deferred or sensor tasks holding slots; pool sized to 4 while the GPU cluster has autoscaled to 8 (wasted capacity); a pool slot leaked by a killed worker until the scheduler cleans it.
- Scenario answer: pool `gpu` = 4, `@task(pool="gpu")` mapped over 200 trials, optionally `max_active_tis_per_dag` as a second guard.

**Example:** 200 tasks, 4 slots, each task 30 minutes. At most 4 run at a time, so 200 / 4 = 50 waves, 50 x 0.5 h = 25 hours of wall time. Raising the pool to 8 halves it, but only if there are 8 GPUs.

**Code:**
```python
import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="gpu_sweep",
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    max_active_tasks=16,   # per-DAG cap on running task instances
    max_active_runs=1,     # per-DAG cap on concurrent runs
    tags=["ml"],
)
def gpu_sweep():
    @task(pool="gpu", pool_slots=1, priority_weight=5)
    def train(trial: int) -> str:
        return f"trial-{trial}-done"

    train.expand(trial=list(range(6)))


gpu_sweep()
```
```bash
set -e
H=/tmp/claude-0/b5p05_q11_20/q17; rm -rf $H; mkdir -p $H/dags; cp q17_pool_dag.py $H/dags/
export AIRFLOW_HOME=$H AIRFLOW__CORE__DAGS_FOLDER=$H/dags AIRFLOW__CORE__LOAD_EXAMPLES=False
AF=/tmp/claude-0/b5p05/af/bin/airflow
$AF db migrate >/dev/null 2>&1
$AF pools list 2>&1 | grep -v -i warn
$AF pools set gpu 4 "4 GPUs on the training cluster" 2>&1 | tail -4
$AF pools list 2>&1 | grep -v -i warn
$AF dags test gpu_sweep 2026-10-01 2>&1 | grep -oE "Returned value was: trial-[0-9]-done" | sort | uniq -c
```

**Output (my run):** apache-airflow 3.3.2, SQLite, `airflow dags test` runs the tasks in one process. I do **not** claim it enforced the pool; it only proves the DAG parses and the pool exists. Real parallel enforcement on workers is **not executed**. (Six mapped tasks finished, shown by the count of returned values.)
```text
pool         | slots | description  | include_deferred | team_name
=============+=======+==============+==================+==========
default_pool | 128   | Default pool | False            | None     
                                                                  
Pool gpu created
pool         | slots | description                    | include_deferred | team_name
=============+=======+================================+==================+==========
default_pool | 128   | Default pool                   | False            | None     
gpu          | 4     | 4 GPUs on the training cluster | False            | None     
                                                                                    
      1 Returned value was: trial-0-done
      1 Returned value was: trial-1-done
      1 Returned value was: trial-2-done
      1 Returned value was: trial-3-done
      1 Returned value was: trial-4-done
      1 Returned value was: trial-5-done
```

**Follow-ups:**
1. *Pool or `max_active_tis_per_dag`?* Pool is shared across DAGs; the per-task limit only covers that task in one DAG.
2. *Can a task use 2 slots?* Yes, `pool_slots=2` for a task that needs two GPUs.
3. *How to create pools as code?* CLI (`airflow pools set`), the REST API, or `airflow pools import` from a JSON file; check current docs.

**Common mistakes:**
- Setting a pool but forgetting to attach it to the tasks.
- Sizing pools by hope, not by the real resource.
- Using `parallelism` as a per-team limit.
- Letting a sensor in `poke` mode eat the slots (Q7).

### Q18 ⭐⭐ 🟡 Dynamic task mapping and dynamic DAGs in Airflow. Train one model per region or per hyperparameter set: .expand and .partial, mapped task limits and what happens when the list is empty, versus generating DAGs from a config file in a loop (and the parse-time cost that causes). Show a mapped training task over four parameter sets and run it with airflow dags test, showing the map indexes. Mention the DAG-file top-level-code rule: no network or database calls at parse time.
**Asked at:** Airflow interview guides (hyring.com Airflow Interview Questions 2026, datavidhya.com Airflow interview pages, prachub.com 'Airflow Interview Questions for Data Engineers', datadriven.io, hirist.tech top 20 Airflow questions; search snippets only, not opened); editorial guides, not verified candidate reports; data engineering, MLOps and ML platform roles, including IT-services firms and GCCs
**Say this first (1 line):** Dynamic task mapping lets one task definition fan out into N task instances at run time with `.expand`, which is how I train one model per region or per hyperparameter set, while generating whole DAGs in a loop is a parse-time trick with a cost.

**Then explain:**
- `train.partial(epochs=3).expand(cfg=list_params())`: `partial` fixes arguments shared by all copies, `expand` gives the list to fan out over. Each copy gets a `map_index` (0, 1, 2 ...). A downstream task that takes the mapped result receives all outputs as one sequence.
- The list must be known by the time the mapped task is scheduled, so it usually comes from an upstream task (small JSON-able list through XCom). Cap in config: `max_map_length` (1024 in my install). Per-task cap on parallel copies: `max_active_tis_per_dag`.
- **Empty list:** the mapped task is marked skipped. I saw "Marking ... as SKIPPED since the map has 0". A downstream task with the default `all_success` rule is skipped too; use `trigger_rule="all_done"` if it must still run (my `after` task did).
- **Dynamic DAGs in a loop** (`for region in regions: create DAG`): the structure is fixed at parse time and the file is re-parsed repeatedly, so any work at top level (network, database, big file read) slows the scheduler (Q34). Use mapping for run-time fan-out and keep top-level code to cheap Python.
- Failure modes: one bad copy fails while others succeed (retry just that map index); huge fan-out floods the UI and DB; mapping over a list produced by a non-deterministic query changes between reruns.
- Execution order is not guaranteed: in my two runs the indexes ran in different orders.

**Example:** four param sets: north and south with lr 0.1, east and west with lr 0.01. Score is `0.9 - lr`, so east and west get 0.89 and the first max is east (ties break to the earlier index). Hand-check matches `BEST= {'region': 'east', 'score': 0.89}`.

**Code:**
```python
import pendulum
from airflow.sdk import dag, task, get_current_context

START = pendulum.datetime(2026, 1, 1, tz="UTC")


@dag(dag_id="map_train", schedule=None, start_date=START, catchup=False)
def map_train():
    @task
    def list_params() -> list[dict]:
        # small, JSON-able list (it goes through XCom). No network call at PARSE time.
        return [{"region": r, "lr": lr} for r, lr in [("north", 0.1), ("south", 0.1), ("east", 0.01), ("west", 0.01)]]

    @task(max_active_tis_per_dag=2)          # at most 2 mapped copies at once
    def train(cfg: dict, epochs: int) -> dict:
        idx = get_current_context()["ti"].map_index
        print(f"MAP_INDEX={idx} region={cfg['region']} lr={cfg['lr']} epochs={epochs}")
        return {"region": cfg["region"], "score": round(0.9 - cfg["lr"], 2)}

    @task
    def pick_best(results: list[dict]):
        best = max(results, key=lambda r: r["score"])
        print("RESULTS_COUNT=", len(results), "BEST=", best)

    pick_best(train.partial(epochs=3).expand(cfg=list_params()))


map_train()


@dag(dag_id="map_empty", schedule=None, start_date=START, catchup=False)
def map_empty():
    @task
    def nothing() -> list[int]:
        return []

    @task
    def work(x: int):
        print("never printed", x)

    @task(trigger_rule="all_done")
    def after():
        print("AFTER_RAN")

    work.expand(x=nothing()) >> after()


map_empty()
```
```bash
set -e
H=/tmp/claude-0/b5p05_q11_20/q18; rm -rf $H; mkdir -p $H/dags; cp q18_mapping_dag.py $H/dags/
export AIRFLOW_HOME=$H AIRFLOW__CORE__DAGS_FOLDER=$H/dags AIRFLOW__CORE__LOAD_EXAMPLES=False
AF=/tmp/claude-0/b5p05/af/bin/airflow
$AF db migrate >/dev/null 2>&1
for d in map_train map_empty; do
  echo "=== dags test $d"
  $AF dags test $d 2026-10-01 > $H/$d.log 2>&1 || echo "exit $?"
  grep -E "MAP_INDEX|RESULTS_COUNT|AFTER_RAN|never printed" $H/$d.log | sed -E 's/.*(MAP_INDEX|RESULTS_COUNT|AFTER_RAN|never printed)/\1/' | cut -c1-120
  grep -E "DagRun Finished" $H/$d.log | sed -E 's/.*(state=[a-z]+).*/\1/' | head -1
  grep -iE "skipped|error" $H/$d.log | cut -c1-200 | head -3
done
```

**Output (my run):** apache-airflow 3.3.2, SQLite, `airflow dags test`. A harmless-looking `XCom not found ... offset=4` line was logged at error level at the end of the reduce step in the `map_train` run (the run still ended in `success`); I read it as the lazy sequence probing past the last item, which I have not confirmed. (Output below has the `map_empty` case after it.)
```text
=== dags test map_train
MAP_INDEX=2 region=east lr=0.01 epochs=3
MAP_INDEX=3 region=west lr=0.01 epochs=3
MAP_INDEX=0 region=north lr=0.1 epochs=3
MAP_INDEX=1 region=south lr=0.1 epochs=3
RESULTS_COUNT= 4 BEST= {'region': 'east', 'score': 0.89}
state=success
2026-10-26T14:32:22.973176Z [error    ] XCom not found                 [airflow.sdk.api.client] dag_id=map_train detail={'reason': 'not_found', 'messa
=== dags test map_empty
AFTER_RAN
state=success
2026-10-26T14:32:31.996853Z [info     ] Marking <TaskInstance: map_empty.work manual__2026-10-26T14:32:27.393284+00:00 [None] ti_id=01a178a0-8231-70e3
```

**Follow-ups:**
1. *Mapping over files in a bucket?* One task lists keys, another maps over them (keep the list small; check limits).
2. *Reduce step?* A normal task taking the mapped output as its input.
3. *Retry one map index?* Clear that mapped task instance only.

**Common mistakes:**
- Calling an API at DAG top level to build the list.
- Mapping over thousands of items without a limit or pool.
- Expecting results in index order of execution.
- Forgetting the empty case.

### Q19 ⭐⭐ 🟡 Testing Airflow DAGs. Show the test layers: a DagBag import test (no import errors, expected dag ids and task counts, tags and owner set, no cycles), unit tests for task logic as plain functions, airflow dags test for a full run on SQLite, and mocking connections. Write a pytest file that fails when a DAG has an import error or a missing retries setting. Run it with pytest and show real output, one passing and one deliberately failing case. CI wiring belongs to Part 7.
**Asked at:** Airflow interview guides (hyring.com Airflow Interview Questions 2026, datavidhya.com Airflow interview pages, prachub.com 'Airflow Interview Questions for Data Engineers', datadriven.io, hirist.tech top 20 Airflow questions; search snippets only, not opened); editorial guides, not verified candidate reports; data engineering, MLOps and ML platform roles, including IT-services firms and GCCs
**Say this first (1 line):** I test DAGs in layers: a DagBag import test that is fast and runs everywhere, plain unit tests for the logic inside tasks, and an `airflow dags test` full run before merge, with a few house rules (owner, tags, retries) enforced by tests.

**Then explain:**
- **Layer 1, DagBag test:** load the dags folder, assert `import_errors == {}`, assert expected dag ids, task ids, tags, owner. A cycle or a bad import ends up in `import_errors`, so the first assertion catches it (I did not test a cycle).
- **Layer 2, unit tests:** keep logic in plain functions (`clean_rows`) and test them with no Airflow. This is the biggest win; thin `@task` wrappers call them.
- **Layer 3, `airflow dags test <dag> <date>`:** runs the whole DAG in one process on SQLite without a scheduler (Q1). Good smoke test; it does not test scheduling, pools or executors.
- **Mocking connections:** set `AIRFLOW_CONN_<ID>` with `monkeypatch.setenv`, or patch the hook method. I did not run that one here.
- **House-rule tests:** the retries test loops over all tasks and fails with the list of offenders. That is cheap policy enforcement.
- Airflow 3 detail I hit: `DagBag` lives at `airflow.dag_processing.dagbag` in my install and takes no `include_examples` argument. Set `AIRFLOW__CORE__LOAD_EXAMPLES=False` and a DB (`airflow db migrate`) in the test environment.
- Failure modes: tests pass locally but CI has no DB; tests import a DAG that makes a network call at top level; a green import test does not prove the task logic is right.

**Example:** two DAG files. `good_train` has `retries: 2` in `default_args`, so its 2 tasks pass. `bad_no_retries` forgets retries, so the parametrised case for it fails and prints `tasks without retries: ['only']`. Expected totals: 5 tests, 4 pass, 1 fails (import errors, expected tasks, retries x2, plain function). Matches the output.

**Code:** one block, three files (a good DAG, a bad DAG, the pytest file); the shell script sets a temp `AIRFLOW_HOME` and runs pytest.
```python
# ---- file: q19/dags/good_dag.py ----
import pendulum
from airflow.sdk import dag, task


def clean_rows(rows):
    """Plain function: unit-testable without Airflow."""
    return [r for r in rows if r is not None and r >= 0]


@dag(dag_id="good_train", schedule="@daily", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
     catchup=False, tags=["ml"], default_args={"owner": "ml-team", "retries": 2})
def good_train():
    @task
    def extract() -> str:
        return "s3://bucket/raw"

    @task
    def train(path: str):
        print("train on", path)

    train(extract())


good_train()

# ---- file: q19/dags/bad_dag.py ----
import pendulum
from airflow.sdk import dag, task


@dag(dag_id="bad_no_retries", schedule="@daily", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
     catchup=False, tags=["ml"], default_args={"owner": "ml-team"})   # retries missing on purpose
def bad_no_retries():
    @task
    def only():
        pass

    only()


bad_no_retries()

# ---- file: q19/tests/test_dags.py ----
import sys
from pathlib import Path

import pytest
from airflow.dag_processing.dagbag import DagBag

DAGS = Path(__file__).resolve().parents[1] / "dags"
sys.path.insert(0, str(DAGS))


@pytest.fixture(scope="session")
def bag():
    return DagBag(dag_folder=str(DAGS))   # Airflow 3: no include_examples argument


def test_no_import_errors(bag):
    assert bag.import_errors == {}


def test_expected_dag_and_tasks(bag):
    dag = bag.get_dag("good_train")
    assert sorted(dag.task_ids) == ["extract", "train"]
    assert dag.tags and "ml" in dag.tags


@pytest.mark.parametrize("dag_id", ["good_train", "bad_no_retries"])
def test_every_task_has_retries(bag, dag_id):
    dag = bag.get_dag(dag_id)
    missing = [t.task_id for t in dag.tasks if (t.retries or 0) < 1]
    assert not missing, f"{dag_id}: tasks without retries: {missing}"


def test_plain_function_logic():
    from good_dag import clean_rows
    assert clean_rows([1, None, -2, 3]) == [1, 3]
```
```bash
H=/tmp/claude-0/b5p05_q11_20/q19; rm -rf $H; mkdir -p $H
export AIRFLOW_HOME=$H AIRFLOW__CORE__LOAD_EXAMPLES=False PYTHONDONTWRITEBYTECODE=1
cd q19
/tmp/claude-0/b5p05/af/bin/airflow db migrate >/dev/null 2>&1
/tmp/claude-0/b5p05/af/bin/python -m pytest -q -p no:cacheprovider tests 2>&1 | tail -25
```

**Output (my run):** apache-airflow 3.3.2, pytest 9.1.1 (installed into the Airflow venv for this run), Python 3.13. The failure is deliberate. CI wiring is Part 7.
```text
...F.                                                                    [100%]
=================================== FAILURES ===================================
_________________ test_every_task_has_retries[bad_no_retries] __________________

bag = <airflow.dag_processing.dagbag.DagBag object at 0x7f9628ddb770>
dag_id = 'bad_no_retries'

    @pytest.mark.parametrize("dag_id", ["good_train", "bad_no_retries"])
    def test_every_task_has_retries(bag, dag_id):
        dag = bag.get_dag(dag_id)
        missing = [t.task_id for t in dag.tasks if (t.retries or 0) < 1]
>       assert not missing, f"{dag_id}: tasks without retries: {missing}"
E       AssertionError: bad_no_retries: tasks without retries: ['only']
E       assert not ['only']

tests/test_dags.py:30: AssertionError
=========================== short test summary info ============================
FAILED tests/test_dags.py::test_every_task_has_retries[bad_no_retries] - Asse...
1 failed, 4 passed in 1.85s
```

**Follow-ups:**
1. *Test speed?* The DagBag is built once per session (fixture scope), which keeps it to seconds.
2. *Test a task's output?* Call the wrapped function directly, or use `dags test` and inspect the run.
3. *Where do these tests run?* In CI before the DAGs are deployed to the scheduler's folder.

**Common mistakes:**
- Only testing in the UI after deploy.
- Leaving import-time side effects (network, DB) in DAG files.
- Putting all logic inside `@task` bodies so nothing is unit-testable.
- Letting a test share the real `AIRFLOW_HOME` and metadata DB.

### Q20 ⭐⭐ 🟡 Secrets, connections and variables in Airflow. Explain Connections and Variables in the metadata database versus environment variables (AIRFLOW_CONN_...) versus a secrets backend (Vault, AWS Secrets Manager, GCP Secret Manager, Kubernetes secrets), why a secret must never be written in the DAG file or an XCom or logged, masking in logs, and Fernet encryption. Show a connection defined by environment variable and read in a task, and show that the secret is masked in the log if it is. Real secret backends are not executed.
**Asked at:** Airflow interview guides (hyring.com Airflow Interview Questions 2026, datavidhya.com Airflow interview pages, prachub.com 'Airflow Interview Questions for Data Engineers', datadriven.io, hirist.tech top 20 Airflow questions; search snippets only, not opened); editorial guides, not verified candidate reports; data engineering, MLOps and ML platform roles, including IT-services firms and GCCs
**Say this first (1 line):** Secrets never go in the DAG file, in XCom or in logs; they live in a secrets backend or environment variables, tasks read them at run time, and I do not rely on log masking as my only protection.

**Then explain:**
- **Connections** hold how to reach a system (host, login, password, extras); **Variables** hold small settings. Both can live in the metadata database (encrypted with the **Fernet** key), in environment variables (`AIRFLOW_CONN_<ID>`, `AIRFLOW_VAR_<NAME>`), or in a **secrets backend** such as Vault, AWS Secrets Manager, GCP Secret Manager or Kubernetes secrets. Per the docs, lookup tries the secrets backend first, then env vars, then the database (not tested here).
- Fernet: with a key set, passwords and variable values are encrypted in the database; lose or change the key and they cannot be decrypted. A key appeared in my generated config; in production set your own, keep it stable and out of git. A key is 44 bytes and I generated and round-tripped one with `cryptography`.
- Reading in a task: `Connection.get("warehouse")` from `airflow.sdk` worked with the connection defined only as an env var.
- **Masking, what I actually saw.** Airflow has a log masker, and a variable whose name contains words such as `api_key` is treated as sensitive by key name (shown in the direct masker check). But under `airflow dags test` in this sandbox, the connection password and the API key were printed in clear by `print`, by the task logger, and even after an explicit `mask_secret(...)`. The masker itself works when called directly. I read the source: the masking processor is attached unless logs go through the task supervisor, so a real worker run likely differs, but I did not run a worker. Do not assume masking; do not print secrets.
- Also seen: `airflow connections get warehouse` printed the password in the CLI table. Limit who has shell and CLI access.
- The masker is substring-based: a lowercased copy of the secret (`s3cretpassw0rd`) was not masked in my check, so transformed copies leak.
- Failure modes: secret in the DAG file (ends up in git and the UI code view); secret in an XCom (stored in the database, visible in the UI); secret in a traceback or a URL like `postgresql://user:pw@host`.

**Example:** `warehouse` is defined as `postgresql://etl_user:...@db.internal:5432/analytics`. The task uses host and login, and returns only `c.host` (safe) to XCom. The password is fake, used only for this test. The right production move is to put the connection in the secrets backend and reference it by id, so the file in git contains only `"warehouse"`.

**Code:**
```python
# ---- file: q20_secrets_dag.py ----
import pendulum
import logging

from airflow.sdk import dag, task, Connection, Variable
from airflow.sdk.log import mask_secret


@dag(dag_id="secrets_demo", schedule=None, start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False)
def secrets_demo():
    @task
    def use_conn():
        c = Connection.get("warehouse")          # resolved: env var first, then secrets backend, then DB
        print("CONN host=", c.host, "login=", c.login, "type=", c.conn_type)
        print("LEAK_TEST password printed:", c.password)         # masked by Airflow's log masker
        print("LEAK_TEST in f-string:", f"postgresql://{c.login}:{c.password}@{c.host}")
        log = logging.getLogger("airflow.task")
        log.info("LEAK_TEST via logger: password=%s", c.password)
        mask_secret(c.password)                                  # explicit masking
        print("LEAK_TEST after mask_secret print:", c.password)
        log.info("LEAK_TEST after mask_secret logger: password=%s", c.password)
        return c.host                                           # safe value for XCom

    @task
    def use_var():
        api_key = Variable.get("model_api_key")      # name contains 'api_key' -> auto-masked
        plain = Variable.get("region")
        print("LEAK_TEST api key:", api_key, "| region:", plain)

    use_conn() >> use_var()


secrets_demo()

# ---- file: q20_masker_check.py ----
# Direct check of Airflow's masker (the component the real worker log path uses).
from airflow.sdk.log import mask_secret
from airflow.sdk._shared.secrets_masker import redact

line = "connecting with password=S3cretPassw0rd to db"
print("before mask_secret:", redact(line))
mask_secret("S3cretPassw0rd")
print("after  mask_secret:", redact(line))
print("by key name       :", redact({"model_api_key": "sk-demo-123456789", "region": "ap-south-1"}))
print("partial/other text:", redact("S3cretPassw0rd!"), "|", redact("s3cretpassw0rd"))
```
```bash
set -e
H=/tmp/claude-0/b5p05_q11_20/q20; rm -rf $H; mkdir -p $H/dags; cp q20_secrets_dag.py $H/dags/
export AIRFLOW_HOME=$H AIRFLOW__CORE__DAGS_FOLDER=$H/dags AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW_CONN_WAREHOUSE='postgresql://etl_user:S3cretPassw0rd@db.internal:5432/analytics'
export AIRFLOW_VAR_MODEL_API_KEY='sk-demo-123456789'
export AIRFLOW_VAR_REGION='ap-south-1'
AF=/tmp/claude-0/b5p05/af/bin/airflow
$AF db migrate >/dev/null 2>&1
$AF connections get warehouse 2>&1 | tail -3 || true
$AF dags test secrets_demo 2026-10-01 > $H/run.log 2>&1 || echo "exit $?"
grep -E "CONN host|LEAK_TEST" $H/run.log | sed -E 's/.*(CONN host|LEAK_TEST)/\1/' | cut -c1-140
echo "raw secret anywhere in log? $(grep -c -e S3cretPassw0rd -e sk-demo-123456789 $H/run.log)"
```

**Output (my run):** apache-airflow 3.3.2, SQLite, `airflow dags test`, fake credentials. First block: the dags test run (leaks are the finding, the count at the end is lines of the log containing the raw secret). Real secrets backends are **not executed**. Lines are cut for width.
```text
None | warehouse | postgres  | None        | db.internal | analytics | etl_user | S3cretPassw0rd | 5432 | True         | True               | {}      
     |           |           |             |             |           |          |                |      |              |                    |         
                                                                                                                                                      
CONN host= db.internal login= etl_user type= postgres
LEAK_TEST password printed: S3cretPassw0rd
LEAK_TEST in f-string: postgresql://etl_user:S3cretPassw0rd@db.internal
LEAK_TEST via logger: password=S3cretPassw0rd [airflow.task] loc=q20_secrets_dag.py:17
LEAK_TEST after mask_secret print: S3cretPassw0rd
LEAK_TEST after mask_secret logger: password=S3cretPassw0rd [airflow.task] loc=q20_secrets_dag.py:20
LEAK_TEST api key: sk-demo-123456789 | region: ap-south-1
raw secret anywhere in log? 6
```

Direct masker check (second script):
```text
before mask_secret: connecting with password=S3cretPassw0rd to db
after  mask_secret: connecting with password=*** to db
by key name       : {'model_api_key': '***', 'region': 'ap-south-1'}
partial/other text: ***! | s3cretpassw0rd
```

**Follow-ups:**
1. *Where do I put the Fernet key in Kubernetes?* In a Kubernetes secret exposed as an env var (`AIRFLOW__CORE__FERNET_KEY`); check your chart.
2. *Rotate a leaked password?* Change it at the source, update the backend, rerun; assume logs and XCom copies are compromised.
3. *Variables or Connections for an API key?* A Connection fits endpoint plus credential; either way store it in the backend.

**Common mistakes:**
- Trusting "masked in logs" without testing your setup.
- Putting a token in `default_args`, an operator argument or a Jinja template result that gets rendered in the UI.
- Using the same credentials for dev and prod.
- Sharing one all-powerful service account across all DAGs.
