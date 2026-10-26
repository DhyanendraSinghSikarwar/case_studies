# Book 4 — Part 5: Pipelines and orchestration: Airflow, Kubeflow, Prefect

**Topic:** pipelines and orchestration for ML: Apache Airflow (DAGs, operators, sensors, XCom, scheduling and catchup, retries, idempotency, backfills, TaskFlow API, executors, pools, testing, secrets), Kubeflow Pipelines (components, kfp DSL, compile to YAML, caching), Prefect (flows, tasks, deployments, retries), comparisons (Dagster, Argo Workflows, Step Functions, Vertex and SageMaker Pipelines at concept level), and ML pipeline design (training and inference DAGs, data dependencies, failure handling, parametrisation, SLAs, alerting, retraining triggers)
**Target:** 40  |  **Actual:** 40 (⭐⭐⭐ 15, ⭐⭐ 17, ⭐ 8)  |  **Date:** 2026-10-26  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 1 owns Git and testing basics; Part 2 owns Docker; Part 3 owns Kubernetes and the Kubeflow platform overview; Part 4 owns DVC, MLflow and W&B (and OpenLineage); Part 6 owns serving frameworks; Part 7 owns CI/CD and promotion gates; Part 8 owns model monitoring, drift and data-quality monitoring; Part 9 owns feature stores and streaming; Parts 10 and 11 own AWS, Azure and GCP services; Part 12 owns cost and system design in depth; Book 2 owns LLM internals; Book 3 owns SQL; Book 6 owns product and business.

Evidence limits: the pages found could not be opened (WebFetch failed with getaddrinfo ENOTFOUND for airflow.apache.org), so every source is a search snippet only (see research_notes/Book4_Part05_sources.md). No page was found that reports exact Airflow, Kubeflow or Prefect questions asked by a named company at an India or global ML role; 'Asked at' tags therefore name source types (editorial guides, docs, job postings), not verified company reports. Execution limit: pip install worked through the proxy in fresh venvs, so Wave B can really run Apache Airflow 3.3.2 (DagBag parsing, airflow db migrate and airflow dags test on SQLite, no scheduler or web server), Prefect 3.9.0 (local flow runs with a temporary server) and kfp 2.17.3 (compile to YAML, no cluster) on Python 3.13. Everything needing a scheduler, API server, Celery or Kubernetes executor, Kubeflow or Argo cluster, Prefect Cloud, or any cloud service must be labelled 'not executed'.

---

### Q1 ⭐⭐⭐ 🟢 What is Apache Airflow, and what is a DAG, a task, an operator and a task instance? Explain how a DAG file is just Python that declares structure, the scheduler, the DAG processor, the executor, workers, the metadata database and the web UI or API server, and what 'directed acyclic' rules out. Show a three-task ML DAG (extract, train, evaluate) written with the TaskFlow API. Parse it with DagBag and run it with airflow dags test on SQLite; no scheduler or web server is started.
**Asked at:** Airflow interview guides (hyring.com Airflow Interview Questions 2026, datavidhya.com Airflow interview pages, prachub.com 'Airflow Interview Questions for Data Engineers', datadriven.io, hirist.tech top 20 Airflow questions; search snippets only, not opened); editorial guides, not verified candidate reports; data engineering, MLOps and ML platform roles, including IT-services firms and GCCs
**Say this first (1 line):** Airflow is a scheduler for workflows written as Python: a DAG is the graph of tasks and their order, the scheduler decides when each task runs, and workers do the work.

**Then explain:**
- A **DAG** is a directed acyclic graph: arrows have a direction (A before B) and you can never walk a loop back to where you started. "Acyclic" rules out train -> evaluate -> train. A loop would never finish, so the scheduler could not order the tasks.
- A **task** is one node. An **operator** is the template for a task (`BashOperator`, `PythonOperator`, a cloud operator). With the TaskFlow API, a function with `@task` becomes a task. A **task instance** is one task in one DAG run (one date), with its own state, try number and logs.
- A DAG file is just Python that declares structure. The **DAG processor** parses the files and stores the result. The **scheduler** creates runs and queues task instances. The **executor** hands them to **workers**. The **metadata database** holds all state (runs, task states, XComs). The **API server** (Airflow 3) serves the UI and the REST API; check current docs for the exact process list in your version.
- Orchestrator rule: Airflow decides what runs when. Heavy work (Spark, a GPU job) belongs in other systems that the task only calls or waits on.
- Failure modes: a syntax error or a failing import shows up as a DAG import error and the DAG disappears from the UI. Network or database calls at the top level of the file run every parse and slow the whole scheduler. A cycle makes the DAG fail to load.

**Example:** `extract -> train -> evaluate`. For one daily run there are three task instances. If `train` fails, `evaluate` is not run (state `upstream_failed`), and you can retry just `train` for that date.

**Code:**
```python
# dags/ml_train.py  (Airflow 3: note airflow.sdk imports)
from pendulum import datetime
from airflow.sdk import dag, task

@dag(schedule="@daily", start_date=datetime(2026, 1, 1, tz="UTC"), catchup=False,
     default_args={"retries": 2}, tags=["ml"])
def ml_train():
    @task
    def extract(ds=None):
        return f"s3://bucket/raw/{ds}.parquet"

    @task
    def train(uri: str):
        print(f"training on {uri}")
        return "model-v1"

    @task
    def evaluate(model: str):
        print(f"evaluating {model}")
        return {"auc": 0.91}

    evaluate(train(extract()))

ml_train()

# check.py: parse with DagBag (Airflow 3 DagBag has no include_examples argument)
#   from airflow.models import DagBag
#   bag = DagBag(dag_folder=sys.argv[1])
#   print("import_errors:", bag.import_errors)
#   for d in bag.dags.values(): print(d.dag_id, "tasks:", [t.task_id for t in d.tasks])
```

```bash
export AIRFLOW_HOME=/tmp/af_home AIRFLOW__CORE__DAGS_FOLDER=/tmp/af_dags AIRFLOW__CORE__LOAD_EXAMPLES=False
mkdir -p $AIRFLOW_HOME $AIRFLOW__CORE__DAGS_FOLDER && cp ml_train.py $AIRFLOW__CORE__DAGS_FOLDER/
airflow db migrate                      # creates the SQLite metadata DB
python3 -I check.py $AIRFLOW__CORE__DAGS_FOLDER
airflow dags test ml_train 2026-10-01   # runs all tasks in-process: no scheduler, no web server
airflow tasks list ml_train
```

**Output (my run):** apache-airflow 3.3.2, Python 3.13, SQLite, own temp AIRFLOW_HOME. The `dags test` log is verbose (structlog lines); I kept the lines that matter.
```
import_errors: {}
ml_train tasks: ['extract', 'train', 'evaluate']
info: [DAG TEST] starting task_id=extract map_index=-1
info: Pushing xcom
info: [DAG TEST] starting task_id=train map_index=-1
training on s3://bucket/raw/2026-10-01.parquet
info: Pushing xcom
info: [DAG TEST] starting task_id=evaluate map_index=-1
evaluating model-v1
info: Marking run <DagRun ml_train @ 2026-10-01 00:00:00+00:00 ... run_type: manual> successful
(airflow tasks list ml_train prints: evaluate, extract, train)
```
Not executed: scheduler, DAG processor, API server, triggerer, any executor other than the in-process one used by `dags test`.

**Follow-ups:**
- *Is a DAG file run on every task?* The file is parsed repeatedly by the DAG processor, and again by the task runner when a task starts. So keep top-level code cheap.
- *Task vs task instance?* The task is the definition. The instance is that definition for one run, with state.
- *Why not cron?* No dependencies, retries, history or backfill (see Q15).

**Common mistakes:**
- Putting heavy imports or API calls at the top of the DAG file.
- Thinking `airflow dags test` equals a real scheduled run. It runs in one process, with no queueing or worker limits.
- Using Airflow 2 import paths (`from airflow.decorators import dag`) in new code; in Airflow 3 use `airflow.sdk` (the old path may still work with a warning; check current docs).

### Q2 ⭐⭐⭐ 🟡 Airflow scheduling: schedule, start_date, data interval, logical date and catchup. Explain why a daily run for 2026-01-01 starts only after that interval ends, what logical date and data_interval_start and data_interval_end mean, cron strings versus presets versus timetables, why a dynamic start_date such as datetime.now() is a bug, time zones (pendulum) and daylight saving, and what catchup=True does the first time a DAG is unpaused. Show a DAG with a fixed start_date and print its data interval from a test run. Check the Airflow 3 docs for renamed fields.
**Asked at:** Airflow interview guides (hyring.com Airflow Interview Questions 2026, datavidhya.com Airflow interview pages, prachub.com 'Airflow Interview Questions for Data Engineers', datadriven.io, hirist.tech top 20 Airflow questions; search snippets only, not opened); editorial guides, not verified candidate reports; data engineering, MLOps and ML platform roles, including IT-services firms and GCCs
**Say this first (1 line):** A schedule is a rule for making runs, each run covers a data interval, and the logical date names that run; with the classic interval timetables a run for Jan 1 starts only after Jan 1 has ended, because the data is not complete before that.

**Then explain:**
- `start_date` is the earliest point the DAG may produce runs. It must be a fixed date. `datetime.now()` moves every parse, so the first interval never completes and you get confusing or missing runs. Use a fixed value with a time zone (pendulum).
- **Interval timetable** (the Airflow 2 default for cron strings and presets): the daily run for 2026-01-01 has data interval Jan 1 00:00 to Jan 2 00:00 and starts at Jan 2 00:00. **Trigger timetable** (`CronTriggerTimetable`): the run starts at the cron time and the interval is a point.
- In my install (3.3.2) a plain `"@daily"` or `"0 2 * * *"` string became `CronTriggerTimetable`, and the config key `create_cron_data_intervals` was `False`. So do not assume Airflow 2 behaviour; check current docs for your version. If you want "run after the day ends" semantics, use `CronDataIntervalTimetable` explicitly.
- A manual run (and `dags test`) has `data_interval_start = data_interval_end = logical_date`. In Airflow 3 the field is `logical_date`; `execution_date` was removed from the context.
- `catchup=True` the first time you unpause creates a run for every missed interval since `start_date`. That can mean hundreds of runs and a flood on your warehouse. In 3.3.2 `catchup_by_default` is `False`. Time zones: store in UTC, and remember a local day around daylight saving is 23 or 25 hours, so "daily" in local time can shift against UTC.

**Example:** `@daily`, start 2026-01-01 UTC, interval timetable. First run: interval Jan 1 -> Jan 2, starts Jan 2 00:00. Trigger timetable, same cron: first run starts Jan 1 00:00 with an empty interval. The first reading is what you want when the job reads "all of Jan 1".

**Code:**
```python
# dags/daily_features.py
from pendulum import datetime
from airflow.sdk import dag, task

@dag(schedule="@daily", start_date=datetime(2026, 1, 1, tz="Asia/Kolkata"), catchup=False)
def daily_features():
    @task
    def show(logical_date=None, data_interval_start=None, data_interval_end=None, run_id=None):
        print("logical_date        :", logical_date)
        print("data_interval_start :", data_interval_start)
        print("data_interval_end   :", data_interval_end)
    show()

daily_features()

# timetable_types.py: what do the timetables do for the first run?
import pendulum
from airflow.timetables.interval import CronDataIntervalTimetable
from airflow.timetables.trigger import CronTriggerTimetable
from airflow.timetables.base import TimeRestriction
from airflow.sdk import DAG

for s in ["@daily", "0 2 * * *"]:
    d = DAG(f"d{len(s)}", schedule=s, start_date=pendulum.datetime(2026, 1, 1, tz="UTC"))
    print(repr(s), "->", type(d.timetable).__name__)

restr = TimeRestriction(earliest=pendulum.datetime(2026, 1, 1, tz="UTC"), latest=None, catchup=True)
i = CronDataIntervalTimetable("@daily", timezone="UTC").next_dagrun_info(last_automated_data_interval=None, restriction=restr)
print("CronDataIntervalTimetable:", i.data_interval.start, "->", i.data_interval.end, "| run_after", i.run_after)
j = CronTriggerTimetable("0 0 * * *", timezone="UTC").next_dagrun_info(last_automated_data_interval=None, restriction=restr)
print("CronTriggerTimetable     :", j.data_interval.start, "->", j.data_interval.end, "| run_after", j.run_after)
```

```bash
airflow dags test daily_features 2026-10-01
airflow dags test daily_features 2026-10-01T10:30:00
airflow config get-value scheduler create_cron_data_intervals
airflow config get-value scheduler catchup_by_default
```

**Output (my run):** apache-airflow 3.3.2, own AIRFLOW_HOME.
```
logical_date        : 2026-10-01 00:00:00+00:00
data_interval_start : 2026-10-01 00:00:00+00:00
data_interval_end   : 2026-10-01 00:00:00+00:00
(second test, T10:30)  logical_date : 2026-10-01 10:30:00+00:00 (start = end = same)
'@daily' -> CronTriggerTimetable
'0 2 * * *' -> CronTriggerTimetable
CronDataIntervalTimetable: 2026-01-01 00:00:00+00:00 -> 2026-01-02 00:00:00+00:00 | run_after 2026-01-02 00:00:00+00:00
CronTriggerTimetable     : 2026-01-01 00:00:00+00:00 -> 2026-01-01 00:00:00+00:00 | run_after 2026-01-01 00:00:00+00:00
create_cron_data_intervals = False ; catchup_by_default = False
```
Note: the DAG has an Asia/Kolkata start_date, but the manual run shows UTC because the install default time zone is `utc`. Not executed: a live scheduler creating scheduled runs.

**Follow-ups:**
- *Why is a dynamic start_date a bug?* The first interval never closes; behaviour changes every parse.
- *Cron vs preset vs timetable?* Cron and presets are shortcuts. A custom timetable handles rules cron cannot (business days, holidays).
- *What does catchup do on first unpause?* Creates a run per missed interval, up to `max_active_runs` at a time.

**Common mistakes:**
- Reading `{{ ds }}` as "today". It is the logical date.
- Assuming Airflow 2 and 3 treat `"@daily"` the same. I saw `CronTriggerTimetable` in 3.3.2; hedge and verify on your version.
- Scheduling in local time with no thought for daylight saving.

### Q3 ⭐⭐⭐ 🟡 Idempotency in pipeline tasks. Define it, explain why retries, reruns and backfills make it mandatory, and show three patterns: write to a partition keyed by the data interval and overwrite it, upsert on a business key, and write to a temp location then atomically rename. Show a bad task (append to a table on every run) and the fixed one, in Python with a local directory standing in for storage, and prove that running both twice gives different and identical results. Cover non-idempotent side effects such as emails, model registrations and external API calls.
**Asked at:** Airflow interview guides (hyring.com Airflow Interview Questions 2026, datavidhya.com Airflow interview pages, prachub.com 'Airflow Interview Questions for Data Engineers', datadriven.io, hirist.tech top 20 Airflow questions; search snippets only, not opened); editorial guides, not verified candidate reports; data engineering, MLOps and ML platform roles, including IT-services firms and GCCs
**Say this first (1 line):** A task is idempotent if running it twice for the same input leaves the world in the same state as running it once; retries, reruns and backfills all run tasks again, so without idempotency every one of them corrupts data.

**Then explain:**
- Tasks run more than once on purpose: a retry after a crash, a manual clear, a backfill, or two workers racing after a timeout. Design for "at least once".
- Pattern 1, **partition overwrite**: the output location is a function of the data interval (`dt=2026-10-01`). A rerun replaces the same partition. Write to a temp file and `os.replace` it, so readers never see half a file.
- Pattern 2, **upsert on a business key**: `MERGE` or `INSERT ... ON CONFLICT UPDATE` in a database. Same key, same row.
- Pattern 3, **temp then atomic rename**: build the output off to the side, then move it in one step. On object stores a rename is not always atomic (check your store); use a manifest or a "latest" pointer written last.
- Non-idempotent side effects (emails, model registrations, calls to a paid API, Slack messages) need a guard: a ledger of "already done" keys, an idempotency key sent to the API, or a registry that rejects the same version twice. Failure mode: a crash after the side effect but before the task is marked successful means the retry repeats it, so the key must be checked or stored atomically.
- Never use `datetime.now()` or "latest" inside the task for the output name; use the run's date.

**Example:** Raw rows for 2026-10-01 are u1:10 and u2:20. A bad append task run twice gives 4 rows. The partition overwrite run twice gives 2 rows. Count by hand: 2 rows per run, append adds, overwrite replaces.

**Code:**
```python
import csv, json, os, tempfile, pathlib

root = pathlib.Path(tempfile.mkdtemp())
rows = {"2026-10-01": [("u1", 10), ("u2", 20)]}

def bad(day, path):                       # appends every run
    with open(path, "a", newline="") as f:
        w = csv.writer(f)
        for u, v in rows[day]:
            w.writerow([day, u, v])

def good_partition(day, base):            # overwrite partition, temp file + atomic rename
    part = base / f"dt={day}"
    part.mkdir(parents=True, exist_ok=True)
    tmp = part / "data.csv.tmp"
    with open(tmp, "w", newline="") as f:
        csv.writer(f).writerows([[day, u, v] for u, v in rows[day]])
    os.replace(tmp, part / "data.csv")

def good_upsert(day, path):               # same key -> same slot
    state = json.loads(path.read_text()) if path.exists() else {}
    for u, v in rows[day]:
        state[f"{day}|{u}"] = v
    path.write_text(json.dumps(state, sort_keys=True))

def count_lines(p): return sum(1 for _ in open(p))

bad_path = root / "bad.csv"
for _ in range(2): bad("2026-10-01", bad_path)
print("BAD   rows after 2 runs:", count_lines(bad_path))
for _ in range(2): good_partition("2026-10-01", root / "tbl")
print("GOOD1 rows after 2 runs:", count_lines(root / "tbl/dt=2026-10-01/data.csv"),
      "| leftover tmp files:", [p.name for p in (root/"tbl/dt=2026-10-01").glob("*.tmp")])
up = root / "up.json"
for _ in range(2): good_upsert("2026-10-01", up)
print("GOOD2 keys after 2 runs:", len(json.loads(up.read_text())), json.loads(up.read_text()))

sent = root / "sent.txt"                  # guard for a side effect
def notify(run_key):
    done = sent.read_text().split() if sent.exists() else []
    if run_key in done:
        return "skipped (already sent)"
    sent.write_text(" ".join(done + [run_key]))
    return "sent"
print("email run 1:", notify("train|2026-10-01"))
print("email run 2:", notify("train|2026-10-01"))
```

**Output (my run):** `python3 -I`, Python 3.13, temp directory, pure standard library.
```
BAD   rows after 2 runs: 4
GOOD1 rows after 2 runs: 2 | leftover tmp files: []
GOOD2 keys after 2 runs: 2 {'2026-10-01|u1': 10, '2026-10-01|u2': 20}
email run 1: sent
email run 2: skipped (already sent)
```

**Follow-ups:**
- *Is the ledger itself safe?* Not under two racing workers: the check and the write must be one atomic step (a database unique key, or the API's own idempotency key).
- *Can append ever be idempotent?* Yes, if you delete the interval's rows first, or dedupe on a key afterwards; a partition overwrite is simpler.
- *Does Airflow give idempotency for free?* No. It only reruns your code; the code must be safe to rerun.

**Common mistakes:**
- Using "now" or an auto-increment ID as the output key.
- Overwriting in place: a crash mid-write leaves a half file.
- Registering a model on every retry and ending with duplicate versions.

### Q4 ⭐⭐⭐ 🟡 XCom and passing data between tasks. Explain what XCom is (small values in the metadata database, keyed by dag, run, task and key), push and pull, the automatic return-value XCom of TaskFlow, size limits and why a DataFrame or model must never go through XCom, the 'pass a path or ID and keep data in object storage' rule, custom XCom backends at concept level, and templating with Jinja. Show a task that passes an S3-style URI to the next task. Run it with airflow dags test and show what was pushed.
**Asked at:** Airflow interview guides (hyring.com Airflow Interview Questions 2026, datavidhya.com Airflow interview pages, prachub.com 'Airflow Interview Questions for Data Engineers', datadriven.io, hirist.tech top 20 Airflow questions; search snippets only, not opened); editorial guides, not verified candidate reports; data engineering, MLOps and ML platform roles, including IT-services firms and GCCs
**Say this first (1 line):** XCom is Airflow's small message box between tasks: values are stored in the metadata database keyed by DAG, run, task and key, so pass a path or an ID and keep the real data in object storage.

**Then explain:**
- A task pushes a value with `ti.xcom_push` or just by returning it (TaskFlow: the return value is pushed under key `return_value`). A downstream task pulls it with `xcom_pull`, or receives it as a function argument in TaskFlow. Wiring a return value into an argument also sets the dependency.
- XComs live in the `xcom` table of the metadata database (columns include dag_id, run_id, task_id, key, value). Size limits depend on the database and backend; check current docs. A DataFrame or a model in there bloats the database, slows the UI and the scheduler, and can fail on serialisation.
- Rule: **pass the address, not the data**. `s3://bucket/features/dt=2026-10-01/part-0.parquet`, a run ID, a model URI. Heavy data stays in object storage.
- A **custom XCom backend** (concept) stores big values in object storage and keeps only a reference in the database. It hides the rule, so it is easy to abuse; use deliberately.
- Jinja: `{{ ti.xcom_pull(task_ids='train') }}` in templated fields of classic operators. Note that `BashOperator` also pushes its last stdout line as `return_value`, which I saw in the table.
- Failure modes: a value that cannot be serialised to JSON fails the task. XComs are tied to a run, so a cleared task re-pushes; and a secret returned from a task sits in plain text in the database.

**Example:** `extract` returns the feature-file URI. `train` receives it, reads from storage and returns a small dict with the model URI and a row count. A `BashOperator` echoes the model URI via a Jinja pull. Three rows land in the `xcom` table; no big data is in them.

**Code:**
```python
# dags/xcom_demo.py
from pendulum import datetime
from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator

@dag(schedule=None, start_date=datetime(2026, 1, 1, tz="UTC"), catchup=False)
def xcom_demo():
    @task
    def extract(ds=None):
        return f"s3://ml-bucket/features/dt={ds}/part-0.parquet"   # address only

    @task
    def train(uri: str):
        print("reading", uri)
        return {"model_uri": uri.replace("features", "models").replace("part-0.parquet", "model.pkl"), "rows": 1000}

    meta = train(extract())
    BashOperator(task_id="announce",
                 bash_command="echo model at {{ ti.xcom_pull(task_ids='train')['model_uri'] }}").set_upstream(meta)

xcom_demo()

# after `airflow dags test`, read what was pushed straight from SQLite
import sqlite3, os
c = sqlite3.connect(os.environ["AIRFLOW_HOME"] + "/airflow.db")
for r in c.execute("select task_id, key, value from xcom order by task_id"): print(r)
```

```bash
airflow dags test xcom_demo 2026-10-01
```

**Output (my run):** apache-airflow 3.3.2, SQLite, own AIRFLOW_HOME.
```
reading s3://ml-bucket/features/dt=2026-10-01/part-0.parquet
info: model at s3://ml-bucket/models/dt=2026-10-01/model.pkl
('announce', 'return_value', '"model at s3://ml-bucket/models/dt=2026-10-01/model.pkl"')
('extract', 'return_value', '"s3://ml-bucket/features/dt=2026-10-01/part-0.parquet"')
('train', 'return_value', '{"model_uri": "s3://ml-bucket/models/dt=2026-10-01/model.pkl", "rows": 1000}')
```
Not executed: a custom XCom backend or real S3. I did not test the size limit, so I give none.

**Follow-ups:**
- *Why not pass a DataFrame?* Database bloat and serialisation limits; pass a path and read it in the next task.
- *Can two DAGs share XCom?* Not by default; use assets, or an explicit store. XCom is scoped to a run.
- *Mapped tasks?* Each mapped instance pushes under its own map index (Q18).

**Common mistakes:**
- Returning a large list "just this once".
- Returning credentials or tokens from a task.
- Pulling from the wrong `task_ids` (returns None and fails later).

### Q5 ⭐⭐⭐ 🟡 Retries, timeouts and failure handling in Airflow. Explain retries, retry_delay, retry_exponential_backoff, max_retry_delay, execution_timeout, on_failure_callback, trigger rules (all_success, all_done, one_failed, none_failed), default_args versus task-level settings, and the difference between a failed and an up_for_retry or skipped state. Show a DAG with a task that fails twice then succeeds, and a cleanup task that runs with trigger_rule all_done. Run it with airflow dags test and show the retry log lines. Alerting channels are not executed.
**Asked at:** Airflow interview guides (hyring.com Airflow Interview Questions 2026, datavidhya.com Airflow interview pages, prachub.com 'Airflow Interview Questions for Data Engineers', datadriven.io, hirist.tech top 20 Airflow questions; search snippets only, not opened); editorial guides, not verified candidate reports; data engineering, MLOps and ML platform roles, including IT-services firms and GCCs
**Say this first (1 line):** Retries handle flaky tasks, timeouts stop hung ones, callbacks tell you about final failures, and trigger rules decide whether a downstream task still runs when an upstream one failed.

**Then explain:**
- Settings: `retries`, `retry_delay`, `retry_exponential_backoff` with `max_retry_delay`, and `execution_timeout` (kills a single try that runs too long; the task then fails and may retry). Put shared values in `default_args`; a task-level argument overrides it.
- States: `failed` is final. `up_for_retry` means it failed but has tries left. `skipped` means it was deliberately not run (branching, a trigger rule). `upstream_failed` means a parent failed so it never started.
- `on_failure_callback` fires when the task finally fails, not on every retry. In my run it fired once for the task with `retries=0` and never for the task that recovered. `on_retry_callback` is the one for retries.
- Trigger rules: `all_success` (default), `all_done` (run whatever happened: good for cleanup), `one_failed` (alerting task), `none_failed` (skipped is fine, failed is not).
- Gotcha I observed: the DAG run is marked **success** when the leaf task succeeds. My cleanup task is the only leaf and ran with `all_done`, so the run showed success even though `always_fails` failed. Make sure a failure cannot be masked: end with a check task, or use `setup`/`teardown` tasks (check current docs), or alert on task failure rather than run state.
- Retries only help if the task is idempotent (Q3). Retrying a non-idempotent task duplicates side effects.

**Example:** `flaky_fetch` fails on tries 1 and 2 and works on 3 (`retries=2`, delay 1 s). `always_fails` has `retries=0`, so it fails at once and the callback fires. `cleanup` (`all_done`) waits for both; it ran after `flaky_fetch` finished its third try.

**Code:**
```python
# dags/retry_demo.py
from datetime import timedelta
from pendulum import datetime
from airflow.sdk import dag, task

def alert(context):
    ti = context["ti"]
    print(f"ALERT callback: {ti.task_id} failed on try {ti.try_number}")   # swap for Slack/email

@dag(schedule=None, start_date=datetime(2026, 1, 1, tz="UTC"), catchup=False,
     default_args={"retries": 2, "retry_delay": timedelta(seconds=1), "on_failure_callback": alert})
def retry_demo():
    @task(execution_timeout=timedelta(minutes=5))
    def flaky_fetch(ti=None):
        print("attempt number", ti.try_number)
        if ti.try_number < 3:
            raise RuntimeError(f"upstream 503 on try {ti.try_number}")
        return "rows=100"

    @task(retries=0)
    def always_fails():
        raise ValueError("bad schema")

    @task(trigger_rule="all_done")
    def cleanup():
        print("cleanup runs even though a sibling failed")

    done = cleanup()
    [flaky_fetch(), always_fails()] >> done

retry_demo()
```

```bash
airflow dags test retry_demo 2026-10-01
```

**Output (my run):** apache-airflow 3.3.2, SQLite. Log trimmed (tracebacks cut to the last line).
```
ValueError: bad schema
ALERT callback: always_fails failed on try 1
attempt number 1
RuntimeError: upstream 503 on try 1
warning: No tasks to run. unrunnable tasks: {<TaskInstance: retry_demo.cleanup ...
attempt number 2
RuntimeError: upstream 503 on try 2
warning: No tasks to run. unrunnable tasks: {<TaskInstance: retry_demo.cleanup ...
attempt number 3
cleanup runs even though a sibling failed
info: Marking run <DagRun retry_demo @ 2026-10-01 ...> successful
final task_instance rows (task_id, state, try_number, max_tries):
('always_fails', 'failed', 1, 0)
('cleanup', 'success', 1, 2)
('flaky_fetch', 'success', 3, 2)
dag_run state: success
```
Not executed: real alert channels (email, Slack, pager), a real scheduler (the retry delay was honoured by `dags test`; I did not time it).

**Follow-ups:**
- *Why exponential backoff?* A flaky upstream gets breathing room; add `max_retry_delay` to cap it.
- *Timeout vs retries?* `execution_timeout` is per try; a timed-out try counts as a failure and can retry.
- *Skipped vs failed?* Skipped is intentional and not an error; failed needs attention.

**Common mistakes:**
- Retrying non-idempotent tasks.
- Trusting the DAG run state when the last task is a cleanup with `all_done`.
- No timeout, so a hung task holds a worker slot forever.

### Q6 ⭐⭐⭐ 🟡 Backfills and catchup. A feature table was wrong for the last 30 days; you must recompute it. Explain airflow backfill create (Airflow 3) versus the older airflow dags backfill, clearing task instances, catchup versus manual backfill, max_active_runs, why idempotent tasks make backfills safe, how to avoid flooding downstream systems, and what depends_on_past does. Show the command forms (check current docs) and run a short backfill on SQLite if the installed version allows, or show the real error.
**Asked at:** Airflow interview guides (hyring.com Airflow Interview Questions 2026, datavidhya.com Airflow interview pages, prachub.com 'Airflow Interview Questions for Data Engineers', datadriven.io, hirist.tech top 20 Airflow questions; search snippets only, not opened); editorial guides, not verified candidate reports; data engineering, MLOps and ML platform roles, including IT-services firms and GCCs
**Say this first (1 line):** To recompute 30 bad days I use a backfill: a bounded set of runs for past dates, created on demand; it is safe only because each task overwrites its own date's partition.

**Then explain:**
- **Catchup** is automatic and tied to the schedule: when a DAG is unpaused it creates runs for missed intervals since `start_date`. A **backfill** is manual and explicit: you pick the DAG and the date range. For fixing a bug in history, use a backfill, and keep `catchup=False` on the DAG.
- Airflow 3: `airflow backfill create --dag-id X --from-date ... --to-date ...`. The old `airflow dags backfill` is gone: in my install it printed "Command `dags backfill` has been removed. Please use `airflow backfill create`". In Airflow 3 backfills are created in the metadata DB and then executed by the **scheduler**; without one the runs stay `queued`.
- Options I saw in `--help`: `--dry-run`, `--max-active-runs`, `--reprocess-behavior {none,completed,failed}`, `--run-backwards`, `--dag-run-conf`. `reprocess-behavior` decides whether dates that already have a run are skipped, rerun if failed, or all rerun.
- Without the backfill command you can also **clear** task instances for a date range (UI or `airflow tasks clear`) to rerun existing runs; check current docs for flags.
- Flooding: 30 runs at once can hammer the warehouse. Use `--max-active-runs`, a pool for the heavy task, and a rate-limited target. `depends_on_past=True` makes a run wait for the previous date's success: safe for rolling features, but one failed day blocks all later days, and it is not supported with `--run-backwards`.
- Failure mode: non-idempotent tasks (append) will duplicate 30 days of data. Fix Q3 first.

**Example:** Feature table wrong for Oct 1-30. Plan: fix code, deploy, dry-run the range (30 logical dates listed), then create the backfill with `--max-active-runs 3`, watch the first run, check row counts for one date by hand, let the rest go. Each run overwrites `dt=...`, so reruns never double-count.

**Code:**
```python
# dags/rebuild_features.py
from pendulum import datetime
from airflow.sdk import dag, task

@dag(schedule="@daily", start_date=datetime(2026, 9, 1, tz="UTC"), catchup=False, max_active_runs=3)
def rebuild_features():
    @task
    def rebuild(ds=None):
        print(f"overwrite partition dt={ds}")     # idempotent, see Q3
    rebuild()

rebuild_features()
```

```bash
airflow dags reserialize     # put the DAG into the metadata DB first (otherwise: DagNotFound)
airflow backfill create --dag-id rebuild_features --from-date 2026-10-01 --to-date 2026-10-05 --dry-run
airflow backfill create --dag-id rebuild_features --from-date 2026-10-01 --to-date 2026-10-03 \
        --max-active-runs 2 --reprocess-behavior failed
airflow dags backfill rebuild_features      # old Airflow 2 form
```

**Output (my run):** apache-airflow 3.3.2, SQLite. Before `dags reserialize` both create calls raised `DagNotFound: Could not find Dag rebuild_features`: a real error worth knowing.
```
Performing dry run of backfill.
Printing params:
    - dag_id = rebuild_features
    - from_date = 2026-10-01 00:00:00+00:00
    - to_date = 2026-10-03 00:00:00+00:00
(dry run for 10-01..10-05 then printed a table with one row per logical date: 10-01 to 10-05, five rows)
info: Created backfill Dag run. backfill_id=1 dag_id=rebuild_features logical_date=2026-10-01
info: Created backfill Dag run. ... logical_date=2026-10-02
info: Created backfill Dag run. ... logical_date=2026-10-03
backfill row: (1, 'rebuild_features', '2026-10-01', '2026-10-03', 2, 'failed')
dag_run rows: 10-01 backfill queued / 10-02 backfill queued / 10-03 backfill queued
airflow dags command error: argument COMMAND: Command `dags backfill` has been removed. Please use `airflow backfill create`
```
Not executed: the runs themselves (no scheduler was started, so they stay `queued`). `to-date` is inclusive.

**Follow-ups:**
- *Backfill vs rerun failed runs?* Rerun/clear touches existing runs; backfill creates runs that do not exist (and with `reprocess-behavior` can touch old ones).
- *Why `max_active_runs`?* To cap parallel dates and protect downstream systems.
- *Does a backfill use today's code?* Yes, current DAG code by default (there is a `--run-on-latest-version` option; check current docs for DAG versioning behaviour).

**Common mistakes:**
- Backfilling non-idempotent tasks.
- Forgetting that `dags backfill` is removed in Airflow 3.
- Backfilling 30 dates with no concurrency limit.

### Q7 ⭐⭐⭐ 🟡 Airflow sensors versus plain tasks. When do you wait for a file, a partition, an upstream DAG (ExternalTaskSensor or asset events) or an API? Explain poke versus reschedule mode, deferrable operators and the triggerer, timeout, poke_interval and soft_fail, and why many long-poking sensors can exhaust worker slots. Show a file sensor in reschedule mode and a deferrable alternative. Run the sensor DAG against a local file with airflow dags test. Real S3 or cloud sensors are not executed.
**Asked at:** Airflow interview guides (hyring.com Airflow Interview Questions 2026, datavidhya.com Airflow interview pages, prachub.com 'Airflow Interview Questions for Data Engineers', datadriven.io, hirist.tech top 20 Airflow questions; search snippets only, not opened); editorial guides, not verified candidate reports; data engineering, MLOps and ML platform roles, including IT-services firms and GCCs
**Say this first (1 line):** Use a sensor when the thing you need is produced outside Airflow's control and you must wait for it; use reschedule or deferrable mode so waiting does not hold a worker slot.

**Then explain:**
- A **sensor** is a task that polls a condition (a file, an S3 key, a partition, another DAG's run, an API) and succeeds when true. If you already know the data is there, a plain task is simpler and better.
- **poke mode** holds a worker slot the whole time and sleeps between checks. **reschedule mode** frees the slot between pokes: the task goes to `up_for_reschedule` and returns after `poke_interval`. Use poke only for very short waits.
- **Deferrable** operators hand the wait to the **triggerer** (an async process that runs many waits in one event loop), freeing the worker entirely. It needs a triggerer running in real deployments.
- `timeout` is the total time before the sensor fails; `soft_fail=True` marks it skipped instead of failed (downstream is skipped too). Pick it deliberately: a skipped sensor can hide a missing upstream.
- Failure mode: many long poke-mode sensors can fill all worker slots and starve real work (a deadlock if the sensors wait on something that needs a slot). `ExternalTaskSensor` needs the same logical date alignment as the other DAG; for cross-DAG data dependencies, assets (Q22) are usually cleaner. Better still: have the upstream write a success marker file.

**Example:** Upstream writes `_SUCCESS` when its files are complete. The sensor waits for that marker (not for the data files, which could be half written), then `train` runs.

**Code:**
```python
# dags/wait_for_file.py : reschedule mode
from pendulum import datetime
from airflow.sdk import dag, task
from airflow.providers.standard.sensors.filesystem import FileSensor

LANDING = "/tmp/q7/landing/_SUCCESS"

@dag(schedule=None, start_date=datetime(2026, 1, 1, tz="UTC"), catchup=False)
def wait_for_file():
    wait = FileSensor(task_id="wait_for_success_marker", filepath=LANDING,
                      fs_conn_id="fs_default",
                      mode="reschedule", poke_interval=2, timeout=60, soft_fail=False)

    @task
    def train():
        print("marker found, training starts")

    wait >> train()

wait_for_file()

# dags/wait_deferrable.py : same wait, handed to the triggerer
@dag(schedule=None, start_date=datetime(2026, 1, 1, tz="UTC"), catchup=False)
def wait_deferrable():
    wait = FileSensor(task_id="wait_async", filepath=LANDING, fs_conn_id="fs_default",
                      deferrable=True, poke_interval=2)

    @task
    def train():
        print("marker found (deferrable), training starts")

    wait >> train()

wait_deferrable()
```

```bash
export AIRFLOW_CONN_FS_DEFAULT='fs://?path=/'      # without a fs_default connection the sensor has nothing to use
( sleep 8; touch /tmp/q7/landing/_SUCCESS ) &      # the file appears while the sensor waits
airflow dags test wait_for_file 2026-10-01
rm -f /tmp/q7/landing/_SUCCESS
( sleep 14; touch /tmp/q7/landing/_SUCCESS ) &
airflow dags test wait_deferrable 2026-10-01
```

**Output (my run):** apache-airflow 3.3.2, local file, own AIRFLOW_HOME. `connections get fs_default` said "Connection not found." until I set the env var.
```
--- wait_for_file (reschedule)
info: Poking for file /tmp/.../landing/_SUCCESS
info: Poking for file /tmp/.../landing/_SUCCESS
marker found, training starts
info: Marking run <DagRun wait_for_file ...> successful
--- wait_deferrable
info: Poking for file /tmp/.../landing/_SUCCESS
info: [DAG TEST] running trigger in line
info: [DAG TEST] Trigger completed
info: wait_async completed successfully as /tmp/.../landing/_SUCCESS found.
marker found (deferrable), training starts
info: Marking run <DagRun wait_deferrable ...> successful
```
`dags test` ran the trigger in line; no triggerer process was started, so real triggerer behaviour is not executed. Real S3 or cloud sensors: not executed.

**Follow-ups:**
- *Sensor vs asset-triggered DAG?* Assets fit data produced by other Airflow DAGs; sensors fit outside producers.
- *Why a marker file?* Data files may be partially written; the marker means complete.
- *Reschedule vs deferrable?* Reschedule still uses a slot briefly each poke; deferrable uses none but needs the triggerer.

**Common mistakes:**
- Poke mode with a 6-hour timeout across many DAGs.
- Waiting for the data file instead of a completion marker.
- `soft_fail=True` hiding a real outage.

### Q8 ⭐⭐⭐ 🟡 Airflow TaskFlow API versus classic operators. Explain @dag and @task, automatic XCom wiring, type hints, multiple_outputs, mixing with BashOperator and PythonOperator, dynamic task mapping with expand, @task.virtualenv or external Python for isolated dependencies, and when classic operators and provider packages are still the better choice. Show the same two-step ML DAG both ways. Parse and test both with DagBag and show the task lists.
**Asked at:** Airflow interview guides (hyring.com Airflow Interview Questions 2026, datavidhya.com Airflow interview pages, prachub.com 'Airflow Interview Questions for Data Engineers', datadriven.io, hirist.tech top 20 Airflow questions; search snippets only, not opened); editorial guides, not verified candidate reports; data engineering, MLOps and ML platform roles, including IT-services firms and GCCs
**Say this first (1 line):** TaskFlow turns plain Python functions into tasks and wires XCom for you, which is shorter and easier to read; classic operators are still the right tool when a provider operator already does the job or you need an operator's exact features.

**Then explain:**
- `@dag` and `@task` (from `airflow.sdk` in Airflow 3). Calling a task inside the DAG function builds the graph; passing one task's result into another sets the dependency and the XCom in one step. Type hints document what travels.
- `multiple_outputs=True` (or returning a dict with a `dict` type hint) pushes each key as its own XCom, so you can write `out["path"]`. I saw the keys `path`, `rows` and the whole `return_value` pushed.
- Classic `PythonOperator` needs you to write the `xcom_pull` yourself and set `>>` by hand. Both styles mix freely in one DAG (a `BashOperator` next to a `@task`).
- Dynamic task mapping: `task.expand(...)` creates one mapped instance per item at runtime (Q18).
- Isolated dependencies: `@task.virtualenv(requirements=[...])` builds a venv for that task; `@task.external_python` points at an existing interpreter; `@task.docker` or the pod operator for full images (Q35). Heavy ML libraries should not be in the Airflow environment.
- Prefer classic operators for provider integrations (`SQLExecuteQueryOperator`, cloud job operators) that handle auth, polling and deferral for you. Failure modes: top-level code still runs at parse time in both styles; a virtualenv task is slow and needs network at run time.

**Example:** Same two steps. `prepare` returns `{"path", "rows"}`; `train` prints "train on /data/train.parquet with 100 rows". Both DAGs give the same log line; TaskFlow is about half the wiring.

**Code:**
```python
# dag_taskflow.py
from pendulum import datetime
from airflow.sdk import dag, task

@dag(dag_id="two_step_taskflow", schedule=None, start_date=datetime(2026, 1, 1, tz="UTC"), catchup=False)
def two_step():
    @task(multiple_outputs=True)
    def prepare(n_rows: int = 100) -> dict:
        return {"path": "/data/train.parquet", "rows": n_rows}

    @task
    def train(path: str, rows: int) -> str:
        print(f"train on {path} with {rows} rows")
        return "model-v1"

    @task.virtualenv(requirements=["scikit-learn==1.5.2"], system_site_packages=False)
    def isolated_score():
        import sklearn
        return sklearn.__version__

    out = prepare()
    train(out["path"], out["rows"])
    isolated_score()

two_step()

# dag_classic.py
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

def prepare(n_rows=100, **_):
    return {"path": "/data/train.parquet", "rows": n_rows}

def train(ti, **_):
    out = ti.xcom_pull(task_ids="prepare")          # you wire the XCom yourself
    print(f"train on {out['path']} with {out['rows']} rows")
    return "model-v1"

with DAG("two_step_classic", schedule=None, start_date=datetime(2026, 1, 1, tz="UTC"), catchup=False):
    p = PythonOperator(task_id="prepare", python_callable=prepare)
    t = PythonOperator(task_id="train", python_callable=train)
    p >> t
```

```bash
python3 -I check.py $AIRFLOW__CORE__DAGS_FOLDER      # DagBag parse of both files
airflow dags test two_step_classic 2026-10-01
airflow dags test two_step_taskflow 2026-10-01
```

**Output (my run):** apache-airflow 3.3.2, SQLite. Note that `dags test` really ran the virtualenv task: it pip-installed scikit-learn 1.5.2 into a fresh venv through the proxy and returned its version.
```
import_errors: {}
two_step_taskflow tasks: ['prepare', 'train', 'isolated_score']
two_step_classic tasks: ['prepare', 'train']
train on /data/train.parquet with 100 rows     (classic run)
train on /data/train.parquet with 100 rows     (taskflow run)
xcom rows: ('isolated_score', '"1.5.2"'), ('prepare', '"/data/train.parquet"'), ('prepare', 100),
           ('prepare', '{"path": "/data/train.parquet", "rows": 100}'), ('train', '"model-v1"')
```
Not executed: `@task.docker`, `external_python`, mapping (see Q18).

**Follow-ups:**
- *Does TaskFlow hide the DAG?* The graph is still explicit in the calls; check the graph view.
- *Where is classic still better?* Provider operators with deferral and rich args, and teams that want declarative DAGs.
- *Why venv per task?* Dependency isolation, at the cost of build time on every run.

**Common mistakes:**
- Calling a `@task` function twice in the DAG by accident (I did this in Q5 at first and got two copies of the task, `cleanup` and `cleanup__1`).
- Returning big objects (Q4).
- Using `@task.virtualenv` for a task that runs every minute.

### Q9 ⭐⭐⭐ 🟡 Design a daily model-training pipeline as an Airflow DAG: ingest, validate data, build features, train, evaluate, compare with the production model, register, and notify. Draw the task graph (Mermaid), say which steps run in Airflow itself and which are delegated to Spark, a Kubernetes pod or a cloud training job, where artifacts live, the gate between evaluate and register (branching), and what happens on a partial failure. Show the DAG with BranchPythonOperator or @task.branch and run it with airflow dags test. Real training platforms are not executed.
**Asked at:** Airflow interview guides (hyring.com Airflow Interview Questions 2026, datavidhya.com Airflow interview pages, prachub.com 'Airflow Interview Questions for Data Engineers', datadriven.io, hirist.tech top 20 Airflow questions; search snippets only, not opened); editorial guides, not verified candidate reports; data engineering, MLOps and ML platform roles, including IT-services firms and GCCs
**Say this first (1 line):** The Airflow DAG is the control plane: it orders ingest, validate, features, train, evaluate, a gate and register, while the heavy compute runs elsewhere (Spark, a Kubernetes pod, a cloud training job) and Airflow just launches and waits.

**Then explain:**
- Steps: `ingest -> validate -> build_features -> train -> evaluate -> gate -> (register | skip) -> notify`. Validation raises on bad data, so nothing downstream runs on a poisoned table.
- Where work runs: ingest and features in Spark or the warehouse; training as a pod or managed job (Airflow submits it and waits, ideally deferrable). Airflow tasks stay small and pass paths and IDs (Q4). Artifacts (features, model files, metrics) live in object storage under a path with the run date; the model registry (Part 4) holds versions.
- The **gate** is a branch task (`@task.branch`) returning the next task_id: register if the candidate beats production by a margin, else skip. The other branch is `skipped`. The join task needs `trigger_rule="none_failed_min_one_success"`, otherwise skipped upstreams skip it too.
- Partial failure: each stage writes to an idempotent location (Q3), so rerunning from the failed task (clear it) continues without redoing earlier stages. Retries for flaky stages, a timeout on training, and an alert on the final failure. Registration is the one step with a side effect; guard it with the run key.
- Failure modes: comparing to "latest prod" that changed between train and gate; a gate that compares on a different dataset from the production metric; branching on a metric read from a big XCom.

**Example:** Candidate AUC 0.93 vs production 0.90: register runs, skip is `skipped`. Production at 0.95: skip runs, register is `skipped`, nothing is registered, and notify still runs.

```mermaid
flowchart LR
  I[ingest] --> V[validate] --> F[build_features] --> T[train] --> E[evaluate] --> G{gate}
  G -- better --> R[register]
  G -- not better --> S[skip_register]
  R --> N[notify]
  S --> N
```

**Code:**
```python
# dags/daily_train.py
from pendulum import datetime
from airflow.sdk import dag, task

@dag(schedule="@daily", start_date=datetime(2026, 1, 1, tz="UTC"), catchup=False,
     default_args={"retries": 1}, tags=["ml", "training"], params={"prod_auc": 0.90})
def daily_train():
    @task
    def ingest(ds=None):
        return f"s3://lake/raw/dt={ds}"

    @task
    def validate(uri: str):
        print("validated", uri)       # real life: schema, null rate, row count; raise to stop
        return uri

    @task
    def build_features(uri: str):
        return uri.replace("raw", "features")

    @task
    def train(features: str):
        print("submit training job for", features, "(delegated; Airflow only waits)")
        return {"model_uri": features.replace("features", "models") + "/model.pkl", "auc": 0.93}

    @task
    def evaluate(result: dict):
        return result

    @task.branch
    def gate(result: dict, params=None):
        better = result["auc"] > params["prod_auc"]
        print(f"candidate auc {result['auc']} vs prod {params['prod_auc']} -> {'register' if better else 'skip_register'}")
        return "register" if better else "skip_register"

    @task
    def register(result: dict):
        print("registered", result["model_uri"])

    @task
    def skip_register():
        print("kept production model")

    @task(trigger_rule="none_failed_min_one_success")
    def notify():
        print("notify team: run finished")

    r = evaluate(train(build_features(validate(ingest()))))
    g = gate(r)
    g >> [register(r), skip_register()] >> notify()

daily_train()
```

```bash
airflow dags test daily_train 2026-10-01 --conf '{"prod_auc": 0.90}'
airflow dags test daily_train 2026-10-01 --conf '{"prod_auc": 0.95}'
```

**Output (my run):** apache-airflow 3.3.2, SQLite; DagBag showed tasks `['ingest', 'validate', 'build_features', 'train', 'evaluate', 'gate', 'register', 'skip_register', 'notify']`. The training "job" is just a print.
```
=== conf {"prod_auc": 0.90}
candidate auc 0.93 vs prod 0.9 -> register
info: Downstream tasks skipped
registered s3://lake/models/dt=2026-10-01/model.pkl
notify team: run finished
=== conf {"prod_auc": 0.95}
candidate auc 0.93 vs prod 0.95 -> skip_register
info: Downstream tasks skipped
kept production model
notify team: run finished
```
Not executed: any real Spark job, pod, cloud training job, registry or notification channel.

**Follow-ups:**
- *Why not register inside train?* A separate gate task makes the decision visible, testable and rerunnable.
- *What if notify is the leaf and always succeeds?* It can hide failures; see Q5.
- *Where does the production metric come from?* From the registry or a metrics store, read in the gate (Part 4); here it is a param.

**Common mistakes:**
- Forgetting the join trigger rule so notify is skipped.
- Training inside the Airflow worker.
- A gate with no margin, so noise swaps models daily.

### Q10 ⭐⭐⭐ 🟡 Kubeflow Pipelines basics. Explain a pipeline as a graph of components, each running in its own container on Kubernetes, the kfp SDK (@dsl.component, @dsl.pipeline), typed inputs and outputs, Artifacts versus parameters, compile to IR YAML, and the cluster pieces (API server, persistence, workflow engine, UI, metadata). Write a two-component pipeline, compile it with kfp to YAML, and inspect the YAML keys. Submitting to a cluster is not executed; no cluster is available.
**Asked at:** Kubeflow Pipelines docs and prep pages (kubeflow.org KFP v2 caching docs, climbtheladder Kubeflow interview questions; search snippets only, not opened); docs and generic prep page, not interview reports; Kubernetes-heavy MLOps and ML platform roles
**Say this first (1 line):** Kubeflow Pipelines (KFP) describes a pipeline as a graph of components, each one a container step on Kubernetes; you write it in Python with the kfp SDK, compile it to an IR YAML file, and submit that file to a KFP backend.

**Then explain:**
- `@dsl.component` turns a Python function into a component; `@dsl.pipeline` wires components into a graph. Calling a component inside the pipeline function creates a task; data flow between tasks gives the dependency order.
- **Parameters** are small typed values (int, float, str, bool, list, dict) passed by value. **Artifacts** (`Dataset`, `Model`, `Metrics`) are files: the step reads and writes `.path`, and KFP moves them through object storage and records metadata. Never pass a big file as a parameter.
- Compile: `Compiler().compile(pipeline, "x.yaml")`. The YAML is the pipeline definition: pipeline info, components, executors (container image and command), and the DAG of tasks.
- Cluster pieces (concept, check current docs): an API server, a database for runs and metadata, object storage for artifacts, a workflow engine that creates the pods, a UI, and ML Metadata for lineage. The Kubeflow platform overview is Part 3.
- Failure modes: imports must be inside the component function (it is shipped alone to a container); a lightweight component pip-installs `kfp` itself at start (I saw this in the YAML), which costs seconds on every step.

**Example:** `make_data` writes a Dataset file. `train` reads it, writes a Model and a Metrics artifact, and returns a string. In the compiled YAML the `train` task lists `make-data` in `dependentTasks`, and the root has two parameters, `n_rows` (default 100) and `lr` (default 0.1).

**Code:**
```python
# pipe.py
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

# inspect_yaml.py
import yaml
doc = list(yaml.safe_load_all(open("two_step.yaml")))[0]
print("top-level keys        :", sorted(doc))
print("pipelineInfo          :", doc["pipelineInfo"])
print("components            :", sorted(doc["components"]))
print("executors             :", sorted(doc["deploymentSpec"]["executors"]))
for name, t in doc["root"]["dag"]["tasks"].items():
    print("task", name, "-> component", t["componentRef"]["name"], "| depends on", t.get("dependentTasks", []))
print("train inputs          :", {k: list(v) for k, v in doc["components"]["comp-train"]["inputDefinitions"].items()})
print("train outputs         :", {k: list(v) for k, v in doc["components"]["comp-train"]["outputDefinitions"].items()})
print("root params           :", doc["root"]["inputDefinitions"]["parameters"])
print("train image           :", doc["deploymentSpec"]["executors"]["exec-train"]["container"]["image"])
```

```bash
python3 -I pipe.py && head -3 two_step.yaml && python3 -I inspect_yaml.py
```

**Output (my run):** kfp 2.17.3, Python 3.13, in a temp dir, no cluster.
```
compiled
# PIPELINE DEFINITION
# Name: two-step-demo
# Description: make data then train
top-level keys        : ['components', 'deploymentSpec', 'pipelineInfo', 'root', 'schemaVersion', 'sdkVersion']
pipelineInfo          : {'description': 'make data then train', 'name': 'two-step-demo'}
components            : ['comp-make-data', 'comp-train']
executors             : ['exec-make-data', 'exec-train']
task make-data -> component comp-make-data | depends on []
task train -> component comp-train | depends on ['make-data']
train inputs          : {'artifacts': ['data'], 'parameters': ['lr']}
train outputs         : {'artifacts': ['metrics', 'model'], 'parameters': ['Output']}
root params           : {'lr': {'defaultValue': 0.1, 'isOptional': True, 'parameterType': 'NUMBER_DOUBLE'}, 'n_rows': {'defaultValue': 100.0, 'isOptional': True, 'parameterType': 'NUMBER_INTEGER'}}
train image           : python:3.12
schemaVersion: 2.1.0 / sdkVersion: kfp-2.17.3
executor command starts: ['sh', '-c', '... python3 -m pip install --quiet ... kfp==2.17.3 --no-deps ... && "$0" "$@"']
```
Not executed: submitting to a cluster (no cluster is available), so the pods, artifact store and UI are described from docs only; the compile and YAML checks above did run.

**Follow-ups:**
- *Why does the function return type become `parameters: Output`?* A returned value is exposed as the output parameter named `Output`.
- *Where does the YAML run?* On any KFP v2 backend; Vertex AI Pipelines accepts the same file (Q29, check current docs).
- *KFP vs Airflow?* KFP gives container-per-step plus artifact tracking on Kubernetes; Airflow is a general scheduler (Q14).

**Common mistakes:**
- Importing at module top and using the import inside the component.
- Passing a big dataset as a parameter instead of an artifact.
- Forgetting that every lightweight step installs packages on each run (build an image instead).

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

### Q21 ⭐⭐ 🟡 Airflow 2 versus Airflow 3 and what changed that matters to ML teams (check current docs and release notes): the Task SDK and airflow.sdk imports, the API server replacing the web server, assets replacing datasets, DAG versioning, backfills run by the scheduler, and removal of execution_date in favour of logical_date. Say how you would migrate a fleet of old DAGs. Show an old-style DAG and the new-style one; parse the new one with the installed Airflow and show the real result of parsing the old one (an error or a deprecation warning).
**Asked at:** Airflow interview guides (hyring.com Airflow Interview Questions 2026, datavidhya.com Airflow interview pages, prachub.com 'Airflow Interview Questions for Data Engineers', datadriven.io, hirist.tech top 20 Airflow questions; search snippets only, not opened); editorial guides, not verified candidate reports; data engineering, MLOps and ML platform roles, including IT-services firms and GCCs
**Say this first (1 line):** Airflow 3 moves DAG authoring to `airflow.sdk`, puts an API server in front, renames datasets to assets and drops `execution_date` and `schedule_interval`, so I migrate a fleet by linting with ruff, fixing imports, parsing every DAG with DagBag in CI, then upgrading a canary first.

**Then explain:**
- What I verified by running Airflow 3.3.2 here: `schedule_interval` is gone (TypeError at parse), `execution_date` is not in the task context but `logical_date` is, `airflow.datasets` does not exist any more, and `from airflow.operators.python import PythonOperator` still imports but warns that it moved to the standard provider.
- What I know from release notes but did NOT run here (check current docs): the API server replaces the old web server; tasks talk to the API server through the Task SDK instead of opening the metadata DB directly (so a task that queries the Airflow DB breaks); DAG versioning; backfills are run by the scheduler; SLAs and SubDAGs are removed. For ML teams the two that bite are the direct-DB access and the removed SLAs.
- Migration plan for many DAGs: (1) inventory and owners, (2) `ruff check --preview --select AIR3` on the repo and apply the safe fixes, (3) a CI job that loads every file with DagBag on Airflow 3 and fails on any `import_errors`, (4) install the standard provider and any provider the DAGs need, (5) canary environment with a copy of the metadata DB backup, compare run counts and task states for a week, (6) cut over with a rollback plan.
- Failure mode: a DAG that fails to import does not crash anything. It just disappears from the UI. So alert on the import-error count.
- Trust the DagBag test over the linter. Here ruff said `airflow.datasets.Dataset` "still works", but on 3.3.2 the module was already gone. Linter notes are written against one release, your install may be newer.

**Example:** `old_dag.py` below has three problems that a reader can count: the `Dataset` import (line 5), `schedule_interval` (line 12) and `execution_date` used in the callable. On 3.3.2 the first one stops the parse. `old2_dag.py` has no Dataset import, so the next one shows up: `schedule_interval`. `old3_dag.py` (only in the code folder) uses `schedule=` and `PythonOperator` and does parse, with a deprecation warning, and its context has `logical_date` but no `execution_date`. The new style file parses clean.

**Code:** the driver `code/q21/run.sh` builds its own AIRFLOW_HOME in a temp dir. Python block: the old DAGs, the new DAG and the parse script. Bash block: the commands.
```python
# --- old_dag.py ---
# Airflow 2 style DAG (what a legacy fleet looks like)
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.datasets import Dataset

features = Dataset("s3://bucket/features/")

def train(**ctx):
    print("run for", ctx["execution_date"])

with DAG("old_train", schedule_interval="@daily", start_date=datetime(2026, 1, 1), catchup=False) as dag:
    PythonOperator(task_id="train", python_callable=train, outlets=[features])

# --- old2_dag.py ---
# Airflow 2 style, but without the Dataset import: only schedule_interval and execution_date
from datetime import datetime
from airflow import DAG
from airflow.decorators import task

with DAG("old2_train", schedule_interval="@daily", start_date=datetime(2026, 1, 1), catchup=False) as dag:
    @task
    def train(execution_date=None):
        print("run for", execution_date)
    train()

# --- new_dag.py ---
# Airflow 3 style DAG
import pendulum
from airflow.sdk import Asset, dag, task

features = Asset("s3://bucket/features/")

@dag(schedule="@daily", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False)
def new_train():
    @task(outlets=[features])
    def train(**context):
        print("run for", context["logical_date"])
    train()

new_train()

# --- parse.py ---
import sys, warnings, os
from airflow.dag_processing.dagbag import DagBag
folder = sys.argv[1]
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    bag = DagBag(dag_folder=folder)
print("file:", os.path.basename(folder))
print("dags:", sorted(bag.dags))
print("import_errors:", {os.path.basename(k): v.strip().splitlines()[-1] for k, v in bag.import_errors.items()})
print("warnings:", sorted({f"{x.category.__name__}: {str(x.message)[:110]}" for x in w if "airflow" in str(x.message).lower() or "Deprec" in x.category.__name__}))
```

```bash
export AIRFLOW_HOME=/tmp/some_own_dir AIRFLOW__CORE__LOAD_EXAMPLES=False   # never share this with another run
airflow db migrate
python -I parse.py ./old            # DagBag(dag_folder=...) -> import_errors
AIRFLOW__CORE__DAGS_FOLDER=./new airflow dags test new_train 2026-10-01
ruff check --preview --select AIR3 --output-format concise ./old   # migration lint (ruff 0.16.9)
```

**Output (my run):** Airflow 3.3.2, Python 3.13, SQLite, no scheduler or API server started (only `dags test`). Log lines were filtered with grep/sed.
```text
airflow 3.3.2
file: old
dags: []
import_errors: {'old_dag.py': "ModuleNotFoundError: No module named 'airflow.datasets'"}
warnings: ["UserWarning: The `airflow.operators.python.PythonOperator` attribute is deprecated. Please use `'airflow.providers.standard"]
file: old2
dags: []
import_errors: {'old2_dag.py': "TypeError: DAG.__init__() got an unexpected keyword argument 'schedule_interval'"}
warnings: ["UserWarning: The `airflow.decorators.task` attribute is deprecated. Please use `'airflow.sdk.task'`."]
file: old3
dags: ['old3_train']
import_errors: {}
warnings: ["UserWarning: The `airflow.operators.python.PythonOperator` attribute is deprecated. Please use `'airflow.providers.standard"]
file: new
dags: ['new_train']
import_errors: {}
warnings: []
--- dags test
keys has execution_date: False | has logical_date: True
DagRun Finished: dag_id=old3_train state=success
run for 2026-10-01 00:00:00+00:00
DagRun Finished: dag_id=new_train state=success
--- ruff ruff 0.16.9 migration rules (AIR3) on the old files
old/old_dag.py:7:12: airflow3-suggested-update: [*] `airflow.datasets.Dataset` is removed in Airflow 3.0; It still works in Airflow 3.0 but is expected to be removed in a futu
old/old_dag.py:12:6: airflow3-suggested-update: `airflow.DAG` is removed in Airflow 3.0; It still works in Airflow 3.0 but is expected to be removed in a future version.
old/old_dag.py:12:23: airflow3-removal: [*] `schedule_interval` is removed in Airflow 3.0
old/old_dag.py:13:5: airflow3-suggested-to-move-to-provider: `airflow.operators.python.PythonOperator` is deprecated and moved into `standard` provider in Airflow 3.0; It stil
old2/old2_dag.py:6:6: airflow3-suggested-update: `airflow.DAG` is removed in Airflow 3.0; It still works in Airflow 3.0 but is expected to be removed in a future version.
old2/old2_dag.py:6:24: airflow3-removal: [*] `schedule_interval` is removed in Airflow 3.0
old2/old2_dag.py:7:6: airflow3-suggested-update: `airflow.decorators.task` is removed in Airflow 3.0; It still works in Airflow 3.0 but is expected to be removed in a future v
old2/old2_dag.py:8:15: airflow3-removal: `execution_date` is removed in Airflow 3.0
Found 8 errors.
[*] 3 fixable with the `--fix` option (4 hidden fixes can be enabled with the `--unsafe-fixes` option).
```

**Follow-ups:**
1. *Why is it called logical_date?* It is the point on the timeline the run is about, not the wall-clock time it ran. In `dags test` the data interval start and end both equalled the date I passed (seen in the log), so do not assume a neat interval for manual runs; check current docs.
2. *Can old and new run together?* Run two separate deployments, one per major version, and move DAGs across in batches. I did not test a mixed fleet.
3. *What about custom operators?* Same lint and parse test, plus a real task run in the canary, because import errors are only half of it.

**Common mistakes:** Upgrading everything in one go. Trusting the linter and skipping the parse test. Leaving `from airflow.models import ...` DB queries inside tasks. Forgetting the standard provider. Not alerting on import errors.

### Q22 ⭐⭐ 🟡 Event-driven and asset-aware scheduling versus time-based scheduling. Explain Airflow assets (formerly datasets): a producer task updates an asset, a consumer DAG is scheduled on it, plus sensors, external triggers through the REST API, cloud events (S3 event to Lambda to Step Functions or a message queue) at concept level, and why new-data-arrived beats 'every night at 2 a.m.'. Show a producer and consumer DAG pair and parse them with DagBag, showing the schedule of each. Real event triggering is not executed.
**Asked at:** Airflow interview guides (hyring.com Airflow Interview Questions 2026, datavidhya.com Airflow interview pages, prachub.com 'Airflow Interview Questions for Data Engineers', datadriven.io, hirist.tech top 20 Airflow questions; search snippets only, not opened); editorial guides, not verified candidate reports; data engineering, MLOps and ML platform roles, including IT-services firms and GCCs
**Say this first (1 line):** Time-based scheduling says "run at 2 a.m. and hope the data is there"; asset-based scheduling says "run when the producer says the data is ready", and in Airflow 3 that is an `Asset` listed in the producer's `outlets` and in the consumer's `schedule`.

**Then explain:**
- How it works: a producer task with `outlets=[asset]` writes an asset event when it succeeds. The scheduler sees the event and creates a run of every DAG whose `schedule` lists that asset. The consumer run is not tied to a calendar interval.
- Verified here: the consumer parses with timetable `AssetTriggeredTimetable`; running the producer with `dags test` wrote exactly one row in the `asset_event` table; the consumer had zero runs because no scheduler was running (so the actual consumer trigger is NOT executed here).
- Mixed rule: `AssetOrTimeSchedule` means "on new data, or on a weekly cron, whichever comes first". Good as a safety net when a producer may go silent.
- Other ways to start work on new data: sensors (use reschedule or deferrable mode so they do not hold a worker slot), an external call to the REST API (`POST` a DAG run, check the current API reference for the exact path and auth), or a cloud event (S3 event, then Lambda or EventBridge, then Step Functions or a queue, then the API call). The cloud chain is concept only here.
- Failure modes: the producer emits the event before the file is fully written (write to a temp path, then rename, then finish the task); the same asset updated many times in a minute (check how events are batched in your version); a consumer needing two assets waits for both by default (check docs for `&` and `|` expressions); an asset updated by an outside system does not emit an event unless something calls the API or a watcher is set up; URIs are normalised (the trailing slash was dropped in my run), so be consistent.
- When time-based is still right: a report due at 9 a.m. no matter what, or no clear "done" signal from the producer.

**Example:** Producer `build_features` runs `0 2 * * *` and writes `s3://ml-bucket/features/daily/`. Consumer `train_on_features` has `schedule=[features]`, so it runs after the producer finishes: 02:07 on a good day, 04:40 if the producer was slow, and not at all if the producer failed. With a fixed 03:00 cron, the slow day would train on yesterday's features and the failed day would too, silently.

**Code:** the three DAGs and the check script (python block), then the commands (bash block). The driver `code/q22/run.sh` also reads the `asset`, `asset_event` and `dag_run` tables from its own SQLite file.
```python
# --- ml_dags.py ---
import pendulum
from airflow.sdk import Asset, dag, task
from airflow.timetables.assets import AssetOrTimeSchedule
from airflow.timetables.trigger import CronTriggerTimetable

features = Asset("s3://ml-bucket/features/daily/")

@dag(schedule="0 2 * * *", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False, tags=["producer"])
def build_features():
    @task(outlets=[features])
    def write_features():
        print("wrote features/daily/ ; asset event emitted when this task succeeds")
    write_features()

@dag(schedule=[features], start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False, tags=["consumer"])
def train_on_features():
    @task
    def train():
        print("training because the features asset was updated")
    train()

# new data OR a weekly safety net, whichever comes first
@dag(schedule=AssetOrTimeSchedule(timetable=CronTriggerTimetable("0 6 * * 1", timezone="UTC"), assets=[features]),
     start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False)
def train_or_weekly():
    @task
    def train():
        print("run")
    train()

build_features(); train_on_features(); train_or_weekly()

# --- check.py ---
from airflow.dag_processing.dagbag import DagBag
import sys
bag = DagBag(dag_folder=sys.argv[1])
print("import_errors:", bag.import_errors)
for d in sorted(bag.dags.values(), key=lambda d: d.dag_id):
    s = d.schedule
    if isinstance(s, str): shown = repr(s)
    elif isinstance(s, list): shown = "assets " + str([a.uri for a in s])
    else: shown = type(s).__name__
    print(f"{d.dag_id:18} timetable={type(d.timetable).__name__:22} schedule={shown}")
    outs = sorted(a.uri for t in d.tasks for a in getattr(t, "outlets", []) if hasattr(a, "uri"))
    if outs: print("                   task outlets:", outs)
```

```bash
export AIRFLOW_HOME=/tmp/own_dir AIRFLOW__CORE__LOAD_EXAMPLES=False AIRFLOW__CORE__DAGS_FOLDER=/tmp/own_dir/dags
airflow db migrate
python -I check.py /tmp/own_dir/dags                 # DagBag parse, print schedules
airflow dags test build_features 2026-10-01          # producer only; consumer needs a running scheduler
```

**Output (my run):** Airflow 3.3.2. Scheduler, triggerer and API server were not started.
```text
import_errors: {}
build_features     timetable=CronTriggerTimetable   schedule='0 2 * * *'
                   task outlets: ['s3://ml-bucket/features/daily']
train_on_features  timetable=AssetTriggeredTimetable schedule=assets ['s3://ml-bucket/features/daily']
train_or_weekly    timetable=AssetOrTimeSchedule    schedule=AssetOrTimeSchedule
--- dags test build_features (producer only; no scheduler running)
wrote features/daily/ ; asset event emitted when this task succeeds
DagRun Finished: dag_id=build_features state=success
--- asset tables in the metadata DB
asset rows: [('s3://ml-bucket/features/daily/', 's3://ml-bucket/features/daily')]
asset events: 1
consumer dag run rows: 0
```

**Follow-ups:**
1. *Asset versus sensor?* An asset needs the producer to be in Airflow (or to call the API); a sensor can watch anything, but it polls and costs a slot or a triggerer.
2. *What if the producer reruns?* It emits another event and the consumer runs again, so the consumer must be idempotent (same output path per input version).
3. *Backfill with assets?* Not tested; check current docs.

**Common mistakes:** Emitting the event before the data is complete. Forgetting that the consumer has no calendar interval (do not use `data_interval_start` as the data date; pass the date in the asset event extra or read it from the data). Using a sensor in poke mode that holds a worker for hours. Creating two assets with slightly different URIs.

### Q23 ⭐⭐ 🟡 Monitoring and SLAs of a pipeline itself (not the model; Part 8 owns model monitoring). What do you alert on: task failure, a run that did not start, a late run, a run slower than usual, a stuck sensor, a growing queue, scheduler heartbeat, a zero-row output? Explain Airflow callbacks, deadline alerts or SLA replacements in recent versions (SLAs were removed in Airflow 3; check current docs), emails and Slack hooks, and a heartbeat or dead-man's-switch check. Show a failure callback and a custom data-freshness check as code and run it locally. Real paging channels are not executed.
**Asked at:** Airflow interview guides (hyring.com Airflow Interview Questions 2026, datavidhya.com Airflow interview pages, prachub.com 'Airflow Interview Questions for Data Engineers', datadriven.io, hirist.tech top 20 Airflow questions; search snippets only, not opened); editorial guides, not verified candidate reports; data engineering, MLOps and ML platform roles, including IT-services firms and GCCs
**Say this first (1 line):** I alert on the pipeline's health separately from the model's: failed task, run that never started, run that is late or slow, stuck sensor, queue growth, scheduler heartbeat and a zero-row output, and I put one check outside Airflow because a dead scheduler cannot alert about itself.

**Then explain:**
- Table of what to watch and how:

| Symptom | Signal | Where |
|---|---|---|
| Task failed | failure callback after the last retry | Airflow callback |
| Run never started | no run for the expected interval | external check on run history |
| Run late or slow | deadline alert, or run duration over a limit | Airflow 3 deadline alerts (check docs) or external |
| Stuck sensor or queue growing | queued task count and age | metrics system |
| Scheduler down | heartbeat or health endpoint stops | external probe |
| Zero rows or stale data | a data check task that raises | in the DAG |

- Callbacks: `on_failure_callback` gets the task context. Here it fired once, on the final failed try (try 2 with one retry), not on every try. A callback that itself raises means no alert, so keep it tiny and wrap the sender in try/except.
- SLAs were removed in Airflow 3 (per the Airflow 3 release notes; check current docs). The replacement is deadline alerts. In 3.3.2 I found `DeadlineAlert(reference=..., interval=..., callback=AsyncCallback(...))` and it parsed. Findings from running it: the callback target must be an `async` function (a plain function raised "not awaitable" at parse time), and the DAG object stores the alerts as a list. I did NOT run a scheduler, so I did not see a deadline actually fire. `sla_miss_callback` is still in the `DAG` signature, but I did not test it and would not build on it.
- Dead-man's switch: a successful run pings an outside URL (a healthchecks-style service or your monitoring system). If no ping arrives within the window, the outside system pages you. This catches "nothing ran at all", which in-Airflow alerts cannot.
- Data freshness and row count belong in the DAG as a task that raises with a clear message. Keep the check functions pure Python so they can be unit tested.
- Real email, Slack and paging channels are not executed; the `notify` function here is a print.

**Example:** Now is 2026-10-26 12:00 UTC, the last update was 2026-10-24 00:00, the limit is 26 hours (daily job plus 2 hours grace). Age is 60 hours = 2 days 12:00, over the limit, so the check says stale. Rows are 0, so the row check also fires. The task fails with both reasons, retries once, then the callback alerts once.

**Code:** `checks.py` (pure functions plus the callback), the DAG that uses them and a deadline alert (python block). The driver `code/q23/run.sh` runs them.
```python
# --- checks.py ---
"""Pipeline health checks: pure Python, no Airflow import, so they are easy to unit test."""
from datetime import datetime, timedelta, timezone


def freshness_problem(last_update, now, max_age):
    """Return None if fresh, else a short reason string."""
    if last_update is None:
        return "no data at all"
    age = now - last_update
    if age > max_age:
        return f"stale: {age} old, limit {max_age}"
    return None


def row_count_problem(rows, min_rows=1):
    return f"only {rows} rows, need at least {min_rows}" if rows < min_rows else None


def notify(context_like):
    """Stand-in for Slack/PagerDuty/SMTP. A real one would post to a webhook."""
    print("ALERT:", context_like)


async def notify_async(context_like):
    """AsyncCallback targets must be async functions (Airflow 3.3.2 refused a plain function at parse time)."""
    notify(context_like)


def on_failure(context):
    """Airflow failure callback: receives the task context dict."""
    ti = context["ti"]
    notify(f"task {ti.dag_id}.{ti.task_id} failed on try {ti.try_number}: {context.get('exception')!r}")


if __name__ == "__main__":
    now = datetime(2026, 10, 26, 12, 0, tzinfo=timezone.utc)
    limit = timedelta(hours=26)  # daily job plus 2h grace
    for label, last in [("fresh", now - timedelta(hours=5)), ("stale", now - timedelta(hours=40)), ("empty", None)]:
        print(f"{label:6} ->", freshness_problem(last, now, limit))
    for n in (0, 3):
        print(f"rows={n} ->", row_count_problem(n))

# --- health_dag.py ---
from datetime import datetime, timedelta, timezone
import pendulum
from airflow.sdk import dag, task
from airflow.sdk.definitions.deadline import AsyncCallback, DeadlineAlert, DeadlineReference
from checks import freshness_problem, on_failure, row_count_problem


@dag(
    schedule="@daily", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False,
    default_args={"retries": 1, "retry_delay": timedelta(seconds=1), "on_failure_callback": on_failure},
    # Airflow 3 replacement for SLAs (check current docs for the exact API in your version)
    deadline=DeadlineAlert(
        reference=DeadlineReference.DAGRUN_QUEUED_AT,
        interval=timedelta(hours=2),
        callback=AsyncCallback("checks.notify_async", kwargs={"context_like": "run queued over 2h ago and not finished"}),
    ),
)
def health_demo():
    @task
    def load():
        return {"rows": 0, "last_update": datetime(2026, 10, 24, tzinfo=timezone.utc).isoformat()}

    @task
    def check(stats: dict):
        now = datetime(2026, 10, 26, 12, tzinfo=timezone.utc)
        problems = [p for p in (
            row_count_problem(stats["rows"]),
            freshness_problem(datetime.fromisoformat(stats["last_update"]), now, timedelta(hours=26)),
        ) if p]
        if problems:
            raise ValueError("data check failed: " + "; ".join(problems))

    check(load())


health_demo()
```

```bash
python3 -I checks.py                                  # pure checks, no Airflow
AIRFLOW__CORE__DAGS_FOLDER=./dags airflow dags test health_demo 2026-10-01   # failing check task + callback
```

**Output (my run):** Airflow 3.3.2, `dags test` only (no scheduler, so no deadline fired). The `check` task is meant to fail.
```text
--- pure checks
fresh  -> None
stale  -> stale: 1 day, 16:00:00 old, limit 1 day, 2:00:00
empty  -> no data at all
rows=0 -> only 0 rows, need at least 1
rows=3 -> None
--- DagBag parse
import_errors: {} | deadline alerts attached: 1
dag-level on_failure_callback in default_args: on_failure
--- dags test (check task is expected to fail)
ValueError: data check failed: only 0 rows, need at least 1; stale: 2 days, 12:00:00 old, limit 1 day, 2:00:00
ValueError: data check failed: only 0 rows, need at least 1; stale: 2 days, 12:00:00 old, limit 1 day, 2:00:00
ALERT: task health_demo.check failed on try 2: ValueError('data check failed: only 0 rows, need at least 1; stale: 2 days, 12:00:00 old, limit 1 day, 2:00:00')
DagRun Finished: dag_id=health_demo state=failed
```

**Follow-ups:**
1. *Alert on every failure?* No: after retries, and group by DAG, or people mute the channel.
2. *Late versus slow?* Late is against a clock (deadline from queued time), slow is against history (runtime much above the usual); I use both.
3. *Who watches the watcher?* The outside probe; keep it simple and on different infrastructure.

**Common mistakes:** Alerting only inside Airflow. Alert storms from per-try callbacks. A success status with an empty output table. Callback code that needs a connection that is itself broken. Treating an SLA example from an Airflow 2 blog as valid on 3.

### Q24 ⭐⭐ 🟡 Prefect deployments, work pools and workers. Explain how a flow becomes a deployment (flow.serve versus flow.deploy, prefect.yaml), what a work pool and a worker do, schedules (cron, interval), parameters per run, infrastructure types (process, Docker, Kubernetes) at concept level, and how it differs from Airflow where the scheduler loads DAG files. Show a flow.serve or deployment definition and run the flow once with different parameters locally. A hosted work pool and a worker on Kubernetes are not executed.
**Asked at:** Prefect docs and tutorials (docs.prefect.io concepts and deployments tutorials, MotherDuck Prefect glossary, Tessl registry pages; search snippets only, not opened); docs, no interview question bank found; Python-first data and ML teams
**Say this first (1 line):** In Prefect a flow becomes a deployment that is stored on the API with its entrypoint, schedule, parameters and work pool; `flow.serve()` runs it from one long-lived process, while `flow.deploy()` or `prefect.yaml` plus a work pool and a worker launch each run in separate infrastructure.

**Then explain:**
- Flow versus deployment: a flow is just a Python function. A deployment is a server-side record that says how, when and where to run it (entrypoint, schedules, default parameters, tags, work pool).
- `flow.serve(name=..., cron=...)`: starts a process that registers the deployment and then polls for runs and runs them as sub-processes. Easy, but that process must stay up. I ran this for real: local server, one served deployment, one triggered run with `--param rows=7`.
- Work pool and worker: a work pool is a queue of runs plus a template for infrastructure (process, Docker, Kubernetes; types and names change by version, check current docs). A worker polls a pool and starts each run on that infrastructure. Deploy with `flow.deploy(...)` or `prefect deploy` reading `prefect.yaml`. Not executed here: no work pool, no worker, no Docker or Kubernetes.
- Different from Airflow: Airflow's scheduler and DAG processor read DAG files from a folder and keep a parsed copy of every DAG; Prefect never parses your code in the scheduler. A run starts a fresh process that imports the flow. The price: a bad import shows up at run time, not at parse time, so test the flow in CI.
- Parameters per run: schema-checked from the type hints. A bad type fails before any task starts (shown below).
- Failure modes: the serve process died (runs stay Scheduled and nothing runs); a worker is polling the wrong pool; the flow code on the worker is an old version because the pull step points at the wrong branch; cron timezone.

**Example:** `train` has defaults `rows=5, lr=0.1`. `train()` uses 5 rows. `train(rows=12, lr=0.01)` uses 12. `train(rows=3, dry_run=True)` returns "skipped" without training. `train(rows="many")` is refused by validation. The deployment `train/nightly` has a cron of `0 2 * * *` and default parameter `rows=10`; the manual run overrode it with `rows=7, dry_run=true`.

**Code:** flow, serve script, and a `prefect.yaml` sketch (python and yaml blocks); the driver `code/q24/run.sh` runs everything with its own `PREFECT_HOME`.
```python
# --- train_flow.py ---
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

# --- serve_it.py ---
from train_flow import train

if __name__ == "__main__":
    # one deployment, one cron schedule, default parameters; the process stays alive and polls for runs
    train.serve(name="nightly", cron="0 2 * * *", parameters={"rows": 10}, tags=["ml"])

# --- check_yaml.py ---
import yaml
cfg = yaml.safe_load(open("prefect.yaml"))
dep = cfg["deployments"][0]
print("deployment:", dep["name"], "| entrypoint:", dep["entrypoint"], "| pool:", dep["work_pool"]["name"])
print("schedule:", dep["schedules"][0], "| parameters:", dep["parameters"])
file, func = dep["entrypoint"].split(":")
import ast
tree = ast.parse(open(file).read())
print("entrypoint function found in", file, ":", any(isinstance(n, ast.FunctionDef) and n.name == func for n in ast.walk(tree)))
```

```yaml
# prefect.yaml sketch (keys as I know them from Prefect 3 docs; check current docs). Not deployed: needs a server and a work pool.
name: ml-flows
prefect-version: 3.9.0
pull:
  - prefect.deployments.steps.git_clone:
      repository: https://example.com/team/ml-flows.git
      branch: main
deployments:
  - name: train-nightly
    entrypoint: train_flow.py:train
    parameters: {rows: 10, lr: 0.1}
    schedules:
      - cron: "0 2 * * *"
        timezone: Asia/Kolkata
    work_pool:
      name: k8s-pool          # a Kubernetes work pool; created with `prefect work-pool create`
      job_variables: {image: registry.example.com/team/train:1.4.2}
```

```bash
export PREFECT_HOME=/tmp/own_dir PREFECT_API_URL=http://127.0.0.1:4299/api PREFECT_SERVER_ANALYTICS_ENABLED=false
prefect server start --port 4299 &          # local server
python serve_it.py &                        # registers train/nightly and polls
prefect deployment run train/nightly --param rows=7 --param dry_run=true
prefect deployment inspect train/nightly
```

**Output (my run):** Prefect 3.9.0. Part 1 used the in-process temporary API; part 2 used a real local server and a served deployment; part 3 parsed the `prefect.yaml` sketch only (nothing was deployed). Both processes were stopped at the end.
```text
--- (1) local runs, no server configured (ephemeral API inside the process)
14:40:34.483 | INFO    | Flow run 'talkative-toucanet' - rows=5 lr=0.1 dry_run=False
14:40:35.610 | INFO    | Flow run 'overjoyed-puma' - rows=12 lr=0.01 dry_run=False
14:40:36.740 | INFO    | Flow run 'funny-beagle' - rows=3 lr=0.1 dry_run=True
trained on 5 rows
trained on 12 rows
skipped
bad parameter -> ParameterTypeError Flow run received invalid parameters:
--- (2) server + flow.serve
Created flow run 'keen-ara'.
└── Parameters: {'rows': 7, 'dry_run': True}
14:41:06.443 | INFO    | Flow run 'keen-ara' - rows=7 lr=0.1 dry_run=True
14:41:07.542 | INFO    | Flow run 'keen-ara' - Finished in state Completed()
                'cron': '0 2 * * *',
    'parameters': {'rows': 10},
    'tags': ['ml'],
    'work_pool_name': None,
--- (3) prefect.yaml parses and its entrypoint points at a real function (nothing deployed)
deployment: train-nightly | entrypoint: train_flow.py:train | pool: k8s-pool
schedule: {'cron': '0 2 * * *', 'timezone': 'Asia/Kolkata'} | parameters: {'rows': 10, 'lr': 0.1}
entrypoint function found in train_flow.py : True
```

**Follow-ups:**
1. *serve or deploy?* serve for one machine or a simple team box; deploy with a work pool when you want isolation, images and autoscaled infrastructure.
2. *Where do secrets go?* Prefect blocks or variables, or the environment of the worker; not in `prefect.yaml`.
3. *Does Prefect backfill?* Not tested here; check current docs.

**Common mistakes:** Running `serve` in a terminal and closing it. Assuming a Prefect run sees your laptop's code when a worker runs it elsewhere. Putting secrets in parameters (they are visible in the UI). Forgetting the timezone on a cron.

### Q25 ⭐⭐ 🟡 Prefect for an ML training flow: parameters, task runners for concurrency (ThreadPoolTaskRunner, submit and map), retries on a flaky data fetch, task caching with cache_key_fn and expiration, result storage, and failure hooks (on_failure). Show a flow that fans out three training tasks with .submit, caches a data task, and fails fast on a bad parameter. Run it locally and show the log lines. Prefect Cloud automations and notifications are not executed.
**Asked at:** Prefect docs and tutorials (docs.prefect.io concepts and deployments tutorials, MotherDuck Prefect glossary, Tessl registry pages; search snippets only, not opened); docs, no interview question bank found; Python-first data and ML teams
**Say this first (1 line):** In Prefect I give the flow typed parameters, fan out training with `.submit()` on a thread-pool task runner, put retries on the flaky fetch, cache the data task with a `cache_key_fn` and an expiry, and fail fast on a bad parameter before any work starts.

**Then explain:**
- Parameters: type hints are validated, and my own guard (`lr <= 0` raises) stops the flow before the fetch. Cheap failures first.
- Concurrency: `ThreadPoolTaskRunner(max_workers=3)` plus `task.submit(...)` returns futures; `.result()` waits. Threads suit I/O and libraries that release the GIL. For heavy CPU or GPU training, use separate processes or infrastructure per run (check docs for a process-based runner or Dask/Ray integrations).
- Retries: `retries=2, retry_delay_seconds=...` re-runs only the task. In my run the first fetch raised `ConnectionError`, Prefect logged "Retry 1/2", and the second try passed. Retry only what is safe to repeat (idempotent).
- Caching: `cache_key_fn` returns a string; same key inside `cache_expiration` means the task is skipped and the stored result is reused (state `Cached`). With `persist_result=True` the result goes to result storage (local disk by default as far as I know; check current docs), so it can also be reused across flow runs. I only ran the repeat inside one Python process. The key here is the day, so a new day is a miss. Failure mode: a key that ignores something that matters (for example the query version) serves stale data.
- Failure hooks: `on_failure=[fn]` on the flow gets `(flow, flow_run, state)`. It ran once, after the bad-parameter failure. Notifications to Slack, email or Cloud automations are not executed here.
- Result storage defaults and cleanup differ between versions; check current docs before relying on them in production.

**Example:** Fetch returns `[1, 2, 3, 4]`, mean 2.5. Score = mean x lr, doubled for `gbm`: logreg 2.5 x 0.5 = 1.25, gbm = 2.5, mlp = 1.25. Best is gbm, score 2.5, as in the output. Call 1 fetches (one failure plus one retry, so the body ran twice). Call 2, same day, hits the cache (body not run). Call 3, a new day, runs the body again: 3 body executions in total. Call 4 with `lr=0` fails before any task.

**Code:** one file; the driver `code/q25/run.sh` runs it with its own `PREFECT_HOME`.
```python
from datetime import timedelta
from prefect import flow, task
from prefect.cache_policies import NO_CACHE
from prefect.task_runners import ThreadPoolTaskRunner

CALLS = {"fetch": 0}


def fetch_key(context, parameters):
    """Cache on the inputs that decide the data, not on object identity."""
    return f"data-{parameters['day']}"


@task(retries=2, retry_delay_seconds=0, cache_key_fn=fetch_key, cache_expiration=timedelta(hours=1), persist_result=True)
def fetch(day: str) -> list[float]:
    CALLS["fetch"] += 1
    if CALLS["fetch"] == 1:
        raise ConnectionError("flaky source, first call fails")   # retried by Prefect
    return [1.0, 2.0, 3.0, 4.0]


@task(cache_policy=NO_CACHE)
def train(model: str, data: list[float], lr: float) -> dict:
    score = round(sum(data) / len(data) * lr * (2 if model == "gbm" else 1), 4)
    return {"model": model, "score": score}


def alert(flow, flow_run, state):
    print(f"ON_FAILURE hook: flow run {flow_run.name!r} ended in {state.name}: {state.message[:60]}")


@flow(name="train-many", task_runner=ThreadPoolTaskRunner(max_workers=3), on_failure=[alert], log_prints=True)
def train_many(day: str = "2026-10-01", lr: float = 0.5):
    if lr <= 0:                                  # fail fast, before any work
        raise ValueError(f"lr must be > 0, got {lr}")
    data = fetch(day)
    futures = [train.submit(m, data, lr) for m in ("logreg", "gbm", "mlp")]   # three tasks in parallel threads
    results = [f.result() for f in futures]
    best = max(results, key=lambda r: r["score"])
    print("best:", best)
    return best


if __name__ == "__main__":
    print("RESULT 1:", train_many())                       # fetch fails once, retries, succeeds
    print("RESULT 2:", train_many())                       # same day: fetch comes from cache
    print("RESULT 3:", train_many(day="2026-10-02"))       # new day: new cache key, fetch runs again
    print("fetch body ran", CALLS["fetch"], "times in total")
    try:
        train_many(lr=0)
    except ValueError as e:
        print("RESULT 4 (bad param): ValueError:", e)
```

**Output (my run):** Prefect 3.9.0 with the in-process temporary server. Lines were filtered (the `train` task lines, "Beginning" lines, the stack trace and the telemetry 403 noise from the sandbox proxy were removed).
```text
INFO    | Task run 'fetch-541' - Task run failed with exception: ConnectionError('flaky source, first call fails') - Retry 1/2 will start immediately
INFO    | Task run 'fetch-541' - Finished in state Completed()
INFO    | Flow run 'perky-mosquito' - best: {'model': 'gbm', 'score': 2.5}
INFO    | Flow run 'perky-mosquito' - Finished in state Completed()
INFO    | Task run 'fetch-51c' - Finished in state Cached(type=COMPLETED)
INFO    | Flow run 'mighty-echidna' - best: {'model': 'gbm', 'score': 2.5}
INFO    | Flow run 'mighty-echidna' - Finished in state Completed()
INFO    | Task run 'fetch-734' - Finished in state Completed()
INFO    | Flow run 'ultra-mastiff' - best: {'model': 'gbm', 'score': 2.5}
INFO    | Flow run 'ultra-mastiff' - Finished in state Completed()
ERROR   | Flow run 'quaint-scallop' - Encountered exception during execution: ValueError('lr must be > 0, got 0.0')
INFO    | Flow run 'quaint-scallop' - ON_FAILURE hook: flow run 'quaint-scallop' ended in Failed: Flow run encountered an exception: ValueError: lr must be
INFO    | Flow run 'quaint-scallop' - Finished in state Failed('Flow run encountered an exception: ValueError: lr must be > 0, got 0.0')
RESULT 1: {'model': 'gbm', 'score': 2.5}
RESULT 2: {'model': 'gbm', 'score': 2.5}
RESULT 3: {'model': 'gbm', 'score': 2.5}
fetch body ran 3 times in total
RESULT 4 (bad param): ValueError: lr must be > 0, got 0.0
```

**Follow-ups:**
1. *submit versus map?* `map` fans one task over an iterable; `submit` is for different calls, like three models. Not tested: `map` here.
2. *Does cache survive a restart?* Only if the result is persisted and the storage is still there.
3. *What if one training task fails?* `.result()` raises in the flow; use `return_state=True` or `wait_for` if you want the others to finish and decide yourself (not tested).

**Common mistakes:** Caching on a key that leaves out the data version. Retrying a non-idempotent step. Threads for CPU-bound training. Putting the guard after the expensive fetch. Assuming hooks run for task failures when I wrote a flow hook.

### Q26 ⭐⭐ 🟡 Kubeflow Pipelines control flow and data passing: dsl.If or Condition, dsl.ParallelFor, dsl.ExitHandler, dsl.Collected, pipeline parameters, resource requests per task (set_cpu_limit, set_memory_limit, set_accelerator_type), node selectors and tolerations through kfp-kubernetes, and secrets as environment variables. Write a pipeline that trains in a ParallelFor, picks the best with a condition and cleans up in an exit handler. Compile to YAML and show the DAG structure in the YAML; running it is not executed.
**Asked at:** Kubeflow Pipelines docs and prep pages (kubeflow.org KFP v2 caching docs, climbtheladder Kubeflow interview questions; search snippets only, not opened); docs and generic prep page, not interview reports; Kubernetes-heavy MLOps and ML platform roles
**Say this first (1 line):** In KFP v2 I write the control flow with `dsl.ParallelFor`, `dsl.Collected`, `dsl.If` and `dsl.ExitHandler`, set resources and scheduling per task, and compile to YAML where each of those shows up as a sub-DAG component and a policy field.

**Then explain:**
- `ParallelFor(items=lrs, parallelism=2)` runs the body once per item; in the YAML it is a `parameterIterator` plus an `iteratorPolicy: parallelismLimit: 2`. `dsl.Collected(t.output)` gathers all outputs of the loop into a list for a later task (`pick_best`). Without `Collected`, the task after the loop cannot see the per-item results.
- `dsl.If(best.output >= min_score)` (older name `dsl.Condition`) becomes a `condition-3` component with a `triggerPolicy.condition` expression. If false, the deploy step is skipped, not failed (that is how I understand the KFP semantics; I could not run it).
- `dsl.ExitHandler(exit_task)`: the exit task always runs after the group, whether it passed or failed. In the YAML the `cleanup` task depends on the group with the strategy `ALL_UPSTREAM_TASKS_COMPLETED`. Use it for cleanup, not for logic that needs the result.
- Resources per task: `set_cpu_limit("2")`, `set_memory_limit("4G")`, `set_accelerator_type(...)`, `set_accelerator_limit(1)` land in the executor `resources` block. Node selector, tolerations and secrets come from the separate `kfp-kubernetes` package and land in a second YAML document (platform spec): `nodeSelector`, `tolerations`, `secretAsEnv`. Accelerator type names are platform specific; check current docs.
- Secrets as env vars: reference a Kubernetes secret by name; the value never appears in the YAML (the compiled file only has `wandb-key` and the key name).
- Failure modes: loops over big lists create many pods; no limit means the cluster fills; a missing `Collected` means the next step gets one value only; a node selector that matches no node leaves the pod Pending (see Q27).
- Not executed: submitting the pipeline. No cluster here. What ran: compile and inspect the YAML with kfp 2.17.3 and kfp-kubernetes 2.17.3 (kfp-kubernetes was installed in its own venv).

**Example:** `lrs = [0.1, 0.01, 0.001]`, score = `1 - abs(lr - 0.01) * 10`: 0.1 gives 0.1, 0.01 gives 1.0, 0.001 gives 0.91. `pick_best` returns 1.0; with `min_score = 0.8`, 1.0 >= 0.8 so `deploy` runs. If every score were below 0.8, deploy is skipped and `cleanup` still runs.

**Code:** the pipeline and the inspection script (python block). The driver `code/q26/run.sh` compiles in a temp dir and copies `pipeline.yaml` into the code folder.
```python
# --- pipeline.py ---
from typing import List
from kfp import compiler, dsl
from kfp import kubernetes


@dsl.component(base_image="python:3.12")
def train(lr: float) -> float:
    # toy "validation score": best near lr=0.01
    return round(1.0 - abs(lr - 0.01) * 10, 3)


@dsl.component(base_image="python:3.12")
def pick_best(scores: List[float]) -> float:
    return max(scores)


@dsl.component(base_image="python:3.12")
def deploy(score: float):
    print("deploying model with score", score)


@dsl.component(base_image="python:3.12")
def cleanup():
    print("always runs: delete scratch data")


@dsl.pipeline(name="train-select-deploy")
def train_select_deploy(lrs: List[float] = [0.1, 0.01, 0.001], min_score: float = 0.8):
    exit_task = cleanup()
    with dsl.ExitHandler(exit_task):
        with dsl.ParallelFor(items=lrs, parallelism=2) as lr:
            t = train(lr=lr)
            t.set_cpu_limit("2").set_memory_limit("4G")
            t.set_accelerator_type("NVIDIA_TESLA_T4").set_accelerator_limit(1)
            kubernetes.add_node_selector(t, label_key="pool", label_value="gpu")
            kubernetes.add_toleration(t, key="nvidia.com/gpu", operator="Exists", effect="NoSchedule")
            kubernetes.use_secret_as_env(t, secret_name="wandb-key", secret_key_to_env={"api_key": "WANDB_API_KEY"})
        best = pick_best(scores=dsl.Collected(t.output))
        with dsl.If(best.output >= min_score):
            deploy(score=best.output)


if __name__ == "__main__":
    compiler.Compiler().compile(train_select_deploy, "pipeline.yaml")
    print("compiled pipeline.yaml")

# --- inspect_yaml.py ---
import yaml
docs = list(yaml.safe_load_all(open("pipeline.yaml")))
print("yaml documents:", len(docs), "(0 = pipeline spec, 1 = platform spec)" if len(docs) > 1 else "")
spec = docs[0]
print("pipelineInfo.name:", spec["pipelineInfo"]["name"])
print("input parameters:", {k: (v["parameterType"], v.get("defaultValue")) for k, v in spec["root"]["inputDefinitions"]["parameters"].items()})
print("components:", sorted(spec["components"]))
print("root dag tasks:", sorted(spec["root"]["dag"]["tasks"]))
for name, c in sorted(spec["components"].items()):
    if "dag" in c:
        print(f"  {name}: tasks={sorted(c['dag']['tasks'])}")
for name, t in sorted(spec["root"]["dag"]["tasks"].items()):
    print(f"  root.{name}: dependentTasks={t.get('dependentTasks', [])} trigger={t.get('triggerPolicy', {}).get('strategy')}")
def walk(d, path=""):
    for name, t in d["dag"]["tasks"].items():
        if "parameterIterator" in t: print(f"  {path}{name}: parameterIterator items={t['parameterIterator']['items']} iteratorPolicy={t.get('iteratorPolicy')}")
        if name == "pick-best": print(f"  {path}{name}: dependentTasks={t['dependentTasks']} scores<-{t['inputs']['parameters']['scores']['taskOutputParameter']}")
        if "triggerPolicy" in t: print(f"  {path}{name}: triggerPolicy={t['triggerPolicy']}")
        ref = t.get("componentRef", {}).get("name")
        if ref in spec["components"] and "dag" in spec["components"][ref]:
            walk(spec["components"][ref], path + name + "/")
walk(spec["root"])
ex = [e for k, e in spec["deploymentSpec"]["executors"].items() if k.startswith("exec-train")][0]["container"]
print("train executor resources:", ex.get("resources"))
if len(docs) > 1:
    pk = docs[1]["platforms"]["kubernetes"]["deploymentSpec"]["executors"]
    for k, v in pk.items():
        print("platform executor", k, "->", sorted(v))
        print("   nodeSelector:", v.get("nodeSelector"), "| tolerations:", v.get("tolerations"), "| secretAsEnv:", v.get("secretAsEnv"))
```

**Output (my run):** compile only; the output is my script reading the real compiled YAML. The full file is `code/q26/pipeline.yaml`.
```text
kfp                      2.17.3
kfp-kubernetes           2.17.3
compiled pipeline.yaml
yaml documents: 2 (0 = pipeline spec, 1 = platform spec)
pipelineInfo.name: train-select-deploy
input parameters: {'lrs': ('LIST', [0.1, 0.01, 0.001]), 'min_score': ('NUMBER_DOUBLE', 0.8)}
components: ['comp-cleanup', 'comp-condition-3', 'comp-deploy', 'comp-exit-handler-1', 'comp-for-loop-2', 'comp-pick-best', 'comp-train']
root dag tasks: ['cleanup', 'exit-handler-1']
  comp-condition-3: tasks=['deploy']
  comp-exit-handler-1: tasks=['condition-3', 'for-loop-2', 'pick-best']
  comp-for-loop-2: tasks=['train']
  root.cleanup: dependentTasks=['exit-handler-1'] trigger=ALL_UPSTREAM_TASKS_COMPLETED
  root.exit-handler-1: dependentTasks=[] trigger=None
  cleanup: triggerPolicy={'strategy': 'ALL_UPSTREAM_TASKS_COMPLETED'}
  exit-handler-1/condition-3: triggerPolicy={'condition': "inputs.parameter_values['pipelinechannel--pick-best-Output'] >= inputs.parameter_values['pipelinechannel--min_score']"}
  exit-handler-1/for-loop-2: parameterIterator items={'inputParameter': 'pipelinechannel--lrs'} iteratorPolicy={'parallelismLimit': 2}
  exit-handler-1/pick-best: dependentTasks=['for-loop-2'] scores<-{'outputParameterKey': 'pipelinechannel--train-Output', 'producerTask': 'for-loop-2'}
train executor resources: {'accelerator': {'count': '1', 'resourceCount': '1', 'resourceType': 'NVIDIA_TESLA_T4', 'type': 'NVIDIA_TESLA_T4'}, 'cpuLimit': 2.0, 'memoryLimit': 4.0, 'resourceCpuLimit': '2', 'resourceMemoryLimit': '4G'}
platform executor exec-train -> ['nodeSelector', 'secretAsEnv', 'tolerations']
   nodeSelector: {'labels': {'pool': 'gpu'}} | tolerations: [{'effect': 'NoSchedule', 'key': 'nvidia.com/gpu', 'operator': 'Exists'}] | secretAsEnv: [{'keyToEnv': [{'envVar': 'WANDB_API_KEY', 'secretKey': 'api_key'}], 'optional': False, 'secretName': 'wandb-key', 'secretNameParameter': {'runtimeValue': {'constant': 'wandb-key'}}}]
```

**Follow-ups:**
1. *Where is the cache setting?* A `cachingOptions: enableCache: true` field on each task in the YAML (seen on `pick-best`); `set_caching_options(False)` removes it (seen in Q27).
2. *Why two YAML documents?* The second holds platform-specific settings from `kfp-kubernetes`; a backend that does not know it would ignore or reject it, check your backend.
3. *Can I nest `If` in `ParallelFor`?* Yes in principle; not tested here.

**Common mistakes:** Reading `t.output` after a loop without `Collected`. Putting real logic in the exit handler. Memory limit set below what the data needs (OOMKilled). Forgetting that `kfp-kubernetes` is a separate package. Hard-coding secret values into parameters.

### Q27 ⭐⭐ 🟡 Kubeflow Pipelines in operation: recurring runs, experiments and runs, run parameters, artifacts stored in object storage (MinIO or S3 or GCS), ML Metadata lineage, standalone KFP versus full Kubeflow versus managed Vertex AI Pipelines, and common failures (image pull errors, OOMKilled steps, missing service account permission to storage, large artifacts). Give a troubleshooting table for a step stuck in Pending or failing. Concept and YAML only; no cluster is available, nothing is executed against one.
**Asked at:** Kubeflow Pipelines docs and prep pages (kubeflow.org KFP v2 caching docs, climbtheladder Kubeflow interview questions; search snippets only, not opened); docs and generic prep page, not interview reports; Kubernetes-heavy MLOps and ML platform roles
**Say this first (1 line):** In operation I think in four layers: runs and experiments in the KFP backend, artifacts in object storage, lineage in ML Metadata, and each step as a Kubernetes pod, so most failures are pod failures: Pending, ImagePullBackOff, OOMKilled or a storage permission error.

**Then explain:**
- Vocabulary: an experiment groups runs; a run is one execution of a pipeline with parameters; a recurring run is a schedule (cron or interval) that creates runs. Artifacts (datasets, models) go to object storage (MinIO, S3 or GCS, depending on the install); ML Metadata records which run produced which artifact, which is the lineage you read when someone asks "which data made this model".
- Three ways to run it: standalone KFP (just Pipelines), full Kubeflow (Pipelines plus notebooks, Katib, auth, multi-user), or managed Vertex AI Pipelines (no cluster to run; compiled KFP YAML goes in, see Q29). Install details and versions change; check current docs.
- What I ran: kfp 2.17.3 compile with `set_retry`, `set_caching_options(False)` and a memory limit, and checked that the `Client` class has methods for experiments, runs and recurring runs. No cluster, so no real run, no real recurring run and no UI.
- Observed in the YAML: retries became `retryPolicy: maxRetryCount: 2, backoffDuration: 60s, backoffFactor: 2`. With caching off, the `cachingOptions` field was an empty `{}` (compare `enableCache: true` in Q26), so I read empty as "not cached" but treat that as a reading of the file, not a documented rule.
- Failure mode to say out loud: a step that works on a laptop fails on the cluster because of a different image, no GPU node, different service account, or data bigger than the memory limit.

| Symptom (`kubectl describe pod`) | Likely cause | First fix |
|---|---|---|
| Pending, event "Insufficient cpu/memory/nvidia.com/gpu" | requests larger than any node has free | lower requests, add nodes, check quota |
| Pending, "node(s) didn't match Pod's node affinity/selector" | node selector or toleration does not match a real node label or taint | compare with `kubectl get nodes --show-labels` and taints |
| ImagePullBackOff / ErrImagePull | wrong tag, private registry without a pull secret | fix tag, add `imagePullSecrets` |
| OOMKilled (exit code 137) | memory limit too low for the data | raise `set_memory_limit`, stream or chunk data |
| Step fails with 403 or AccessDenied on the bucket | the step's service account lacks storage permission | grant read/write to the bucket for that service account |
| Step slow at start or at end | big artifact upload and download | pass a path or ID, keep only small values as parameters |
| Same result as before, no new work | cache hit | disable cache for that step or change the input |

**Example:** A training step asks for `memory: 4Gi` and loads a 6 GB frame, so it dies with exit 137. The KFP UI shows a failed step; `kubectl describe` shows `OOMKilled`. Fix: raise the limit to fit with headroom or read in chunks. If the same step instead shows Pending with "Insufficient nvidia.com/gpu", nothing is wrong with the code; no node can offer a GPU.

**Code:** a sketch pod manifest with the settings that cause these failures (yaml block), and the SDK check (python block). Driver: `code/q27/run.sh`.
```yaml
# What a KFP step pod roughly asks Kubernetes for (hand-written sketch of the failure-prone settings, not KFP output)
apiVersion: v1
kind: Pod
metadata:
  name: train-step-sketch
spec:
  serviceAccountName: pipeline-runner        # must be allowed to read/write the artifact bucket
  imagePullSecrets:
    - name: registry-cred                    # missing or wrong => ImagePullBackOff
  nodeSelector:
    pool: gpu
  tolerations:
    - key: nvidia.com/gpu
      operator: Exists
      effect: NoSchedule
  containers:
    - name: main
      image: registry.example.com/team/train:1.4.2
      resources:
        requests: {cpu: "2", memory: 4Gi}
        limits: {memory: 4Gi, nvidia.com/gpu: 1}   # data bigger than 4Gi in memory => OOMKilled (exit 137)
```

```python
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
```

**Output (my run):** `kubernetes-validate` (offline schema check, Kubernetes 1.37) on the manifest, then the SDK script. Nothing was submitted anywhere.
```text
INFO step_pod.yaml passed for resource pod/train-step-sketch against version 1.37
kubernetes-validate exit: 0
retryPolicy: {'backoffDuration': '60s', 'backoffFactor': 2.0, 'backoffMaxDuration': '3600s', 'maxRetryCount': 2}
cachingOptions: {} | displayName: add-one
Client.create_experiment: exists
Client.run_pipeline: exists
Client.create_run_from_pipeline_package: exists
Client.create_recurring_run: exists
Client.list_runs: exists
Client.get_run: exists
create_recurring_run args: ['self', 'experiment_id', 'job_name', 'description', 'start_time', 'end_time', 'interval_second', 'cron_expression', 'max_concurrency', 'no_catchup', 'params', 'pipeline_package_path']
```

**Follow-ups:**
1. *How do I find the step's error?* The step pod logs (main container), then `kubectl describe pod` events, then the node and quota.
2. *Where do artifacts live?* In the object store configured for the install; only small values and URIs go through the metadata store. Check your install's docs.
3. *Recurring run missed a day?* Check the schedule's catch-up setting and that the cluster was up; `create_recurring_run` has a `no_catchup` argument in the SDK I ran.

**Common mistakes:** Debugging code when the pod never started. Using the default service account. Requesting a GPU and forgetting the toleration. Passing a big dataframe as a parameter. Not noticing a cache hit and thinking the step "ran".

### Q28 ⭐⭐ 🟡 Argo Workflows and how it relates to Kubeflow Pipelines. Explain Workflow, Template, DAG and steps templates, artifacts and parameters, CronWorkflow, why Kubeflow Pipelines v1 compiled to Argo and what KFP v2 does differently (check current docs), and when a team uses Argo directly. Write a small two-step Argo Workflow YAML and validate that it parses with pyyaml and has the expected keys. Argo is not installed; nothing was submitted to a cluster.
**Asked at:** Orchestrator comparison write-ups (zenml.io 'Orchestration showdown: Dagster vs Prefect vs Airflow', risingwave, dzone, deploybase, hightouch; search snippets only, not opened); vendor-adjacent blogs, treat specifics with caution; data and ML platform roles
**Say this first (1 line):** Argo Workflows is the general Kubernetes workflow engine (a Workflow is a list of templates, usually a DAG or steps of containers); Kubeflow Pipelines v1 compiled your Python to Argo YAML, and KFP v2 compiles to its own pipeline spec that the backend runs, so most ML teams do not write Argo directly.

**Then explain:**
- Argo objects: `Workflow` (one run), `WorkflowTemplate` (reusable, run by reference), `CronWorkflow` (a schedule that creates Workflows). Inside `spec.templates` you have container templates (do work) and `dag` or `steps` templates (wire them). Parameters are strings passed with `{{inputs.parameters.x}}`; artifacts are files moved through an artifact store; `dependencies: [train]` makes the DAG.
- KFP link: v1 SDK compiled to an Argo Workflow YAML. KFP v2 compiles to a platform-neutral IR YAML (header `# PIPELINE DEFINITION`, seen in Q26) and the backend decides how to run it. I am recalling this from docs and release notes, did not open them here; check current docs. In my own run the kfp 2.17.3 output was the IR, not an Argo Workflow.
- When a team uses Argo directly: non-ML or mixed workflows on Kubernetes (builds, ETL, batch), GitOps style, many small steps, need for Argo features like `CronWorkflow` concurrency rules and fine control of retries and templates. ML teams that want Python authoring, an experiment UI and lineage pick KFP or another tool.
- Failure modes: parameters are strings, so a number needs conversion inside the container; a typo in `dependencies` or a template name fails at submit; artifact store not configured means artifact steps fail.
- Not executed: Argo is not installed and nothing was submitted. What ran: a pyyaml check of the structure (kind, entrypoint exists, DAG dependencies exist, parameters used are declared), including a deliberately broken copy that the check caught.

**Example:** `train-eval.yaml` has a DAG `main` with two tasks: `train` (takes `lr` from the workflow parameter, writes `/tmp/model.txt` as an artifact `model`) and `evaluate` (depends on `train`, reads that artifact). A nightly `CronWorkflow` at `0 2 * * *` with `concurrencyPolicy: Forbid` starts a new run only if the previous one finished. The broken copy renames the dependency to `trian` and uses an undeclared `epochs` parameter, and the check reports both.

**Code:** the Argo YAML (yaml block) and the validator (python block).
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: train-eval-
spec:
  entrypoint: main
  arguments:
    parameters:
      - name: lr
        value: "0.01"
  templates:
    - name: main
      dag:
        tasks:
          - name: train
            template: train
            arguments:
              parameters:
                - name: lr
                  value: "{{workflow.parameters.lr}}"
          - name: evaluate
            dependencies: [train]
            template: evaluate
            arguments:
              artifacts:
                - name: model
                  from: "{{tasks.train.outputs.artifacts.model}}"
    - name: train
      inputs:
        parameters:
          - name: lr
      container:
        image: python:3.12-slim
        command: [python, -c]
        args: ["import sys; open('/tmp/model.txt','w').write('lr={{inputs.parameters.lr}}')"]
      outputs:
        artifacts:
          - name: model
            path: /tmp/model.txt
    - name: evaluate
      inputs:
        artifacts:
          - name: model
            path: /tmp/in/model.txt
      container:
        image: python:3.12-slim
        command: [python, -c]
        args: ["print(open('/tmp/in/model.txt').read())"]
---
apiVersion: argoproj.io/v1alpha1
kind: CronWorkflow
metadata:
  name: nightly-train-eval
spec:
  schedule: "0 2 * * *"
  concurrencyPolicy: Forbid
  workflowSpec:                # same shape as a Workflow spec; a workflowTemplateRef is the other option
    entrypoint: train
    arguments:
      parameters:
        - name: lr
          value: "0.01"
    templates:
      - name: train
        inputs:
          parameters:
            - name: lr
        container:
          image: python:3.12-slim
          command: [python, -c]
          args: ["print('training with lr={{inputs.parameters.lr}}')"]
```

```python
import re, sys, yaml

def check_workflow(spec, label):
    errs = []
    templates = {t["name"]: t for t in spec["templates"]}
    if spec["entrypoint"] not in templates:
        errs.append(f"entrypoint {spec['entrypoint']!r} is not a template")
    wf_params = {p["name"] for p in spec.get("arguments", {}).get("parameters", [])}
    for t in spec["templates"]:
        body = t.get("dag", {}).get("tasks", [])
        names = {x["name"] for x in body}
        for x in body:
            if x["template"] not in templates:
                errs.append(f"task {x['name']}: unknown template {x['template']!r}")
            for d in x.get("dependencies", []):
                if d not in names:
                    errs.append(f"task {x['name']}: unknown dependency {d!r}")
        declared = {p["name"] for p in t.get("inputs", {}).get("parameters", [])}
        for ref in re.findall(r"{{inputs\.parameters\.([\w-]+)}}", yaml.dump(t.get("container", {}))):
            if ref not in declared:
                errs.append(f"template {t['name']}: uses inputs.parameters.{ref} but does not declare it")
        for ref in re.findall(r"{{workflow\.parameters\.([\w-]+)}}", yaml.dump(t)):
            if ref not in wf_params:
                errs.append(f"template {t['name']}: workflow.parameters.{ref} not in spec.arguments")
    print(f"{label}: templates={sorted(templates)} errors={errs or 'none'}")
    return not errs

docs = list(yaml.safe_load_all(open(sys.argv[1])))
for d in docs:
    assert d["apiVersion"].startswith("argoproj.io/"), d["apiVersion"]
    print("kind:", d["kind"])
    if d["kind"] == "Workflow":
        check_workflow(d["spec"], "good workflow")
    else:
        print("cron schedule:", d["spec"]["schedule"], "| concurrencyPolicy:", d["spec"]["concurrencyPolicy"])
        check_workflow(d["spec"]["workflowSpec"], "cron workflowSpec")
# negative test: break it on purpose
bad = yaml.safe_load(open(sys.argv[1]).read().split("---")[0])
bad["spec"]["templates"][0]["dag"]["tasks"][1]["dependencies"] = ["trian"]
bad["spec"]["templates"][1]["container"]["args"][0] += " {{inputs.parameters.epochs}}"
check_workflow(bad["spec"], "broken workflow")
```

**Output (my run):** `python3 -I validate.py train-eval.yaml`. This checks structure only; it is not Argo's own validation (that needs the `argo lint` CLI or a cluster, not available here).
```text
kind: Workflow
good workflow: templates=['evaluate', 'main', 'train'] errors=none
kind: CronWorkflow
cron schedule: 0 2 * * * | concurrencyPolicy: Forbid
cron workflowSpec: templates=['train'] errors=none
broken workflow: templates=['evaluate', 'main', 'train'] errors=["task evaluate: unknown dependency 'trian'", 'template train: uses inputs.parameters.epochs but does not declare it']
```

**Follow-ups:**
1. *Argo versus Airflow?* Argo is Kubernetes native with YAML; Airflow is Python with many operators. Argo fits container-only batch; Airflow fits mixed systems.
2. *Argo Events?* A separate project for triggers from webhooks and queues; concept only.
3. *Why not write Argo for ML?* Authoring a lot of YAML for data scientists, and no ML lineage or experiment UI by default.

**Common mistakes:** Treating all parameters as typed. Forgetting the artifact repository config. Assuming KFP v2 still produces Argo YAML. Using `generateName` in a file that a CronWorkflow must reference (use a `WorkflowTemplate`).

### Q29 ⭐⭐ 🟡 Cloud-managed ML pipelines at concept level: SageMaker Pipelines, Vertex AI Pipelines (runs KFP and TFX definitions), Azure ML pipelines, and AWS Step Functions. Compare what each is for, how steps map to managed training jobs, registry and lineage integration, cost and lock-in, and when a team picks Airflow (MWAA or Cloud Composer) instead. Give a comparison table with hedged claims (check current docs). Parts 10 and 11 own the service detail. Nothing cloud is executed; show how a Vertex pipeline reuses the compiled KFP YAML from the local compile.
**Asked at:** Cloud ML orchestration study guides (open-exam-prep AWS ML Engineer guide on SageMaker Pipelines versus Step Functions and EventBridge retraining, insertchat ML pipeline orchestration glossary, wecreateproblems MLOps interview questions; search snippets only, not opened); study guides and glossaries, not interview reports; MLOps roles on AWS, GCP and Azure
**Say this first (1 line):** Managed pipeline services trade control for less ops: SageMaker Pipelines for AWS ML jobs and registry, Vertex AI Pipelines for KFP and TFX definitions on GCP, Azure ML pipelines on Azure, Step Functions for general AWS service orchestration, and I pick Airflow (MWAA or Cloud Composer) when the workflow is bigger than ML or must be portable.

**Then explain:**
- All claims below are concept level and from my memory of vendor docs; I did not open them and nothing cloud ran. Check current docs and the parts on AWS (Part 10) and Azure and GCP (Part 11).
- The shape is the same everywhere: define steps, each step becomes a managed job (training job, processing job, container), the service tracks runs and artifacts, and ties into a model registry.

| Option | What it is for | Step maps to | Registry and lineage | Lock-in |
|---|---|---|---|---|
| SageMaker Pipelines | ML DAGs on AWS | SageMaker processing, training, transform, register steps | SageMaker Model Registry, lineage tracking | high (SageMaker SDK) |
| Vertex AI Pipelines | runs KFP (and TFX) definitions | Vertex custom jobs or container components | Vertex Model Registry, ML Metadata | medium (KFP YAML is portable, components often call GCP services) |
| Azure ML pipelines | ML workflows in an Azure ML workspace | command or component jobs on Azure ML compute | Azure ML registries and lineage | high |
| Step Functions | state machines across AWS services (Lambda, SageMaker, Glue, ...) | service calls via the Task state | none for ML by itself | high, but general |
| Airflow on MWAA or Composer | any workflow, many systems | operators, which can launch any of the above | via providers or MLflow | low, code stays portable |

- Cost and lock-in: you pay for the jobs either way; managed orchestration adds little compared with the training compute, but lock-in is the real cost. Do not quote prices.
- Choose Airflow when: data engineering and ML share one scheduler; several clouds; you already operate it. Choose the vendor tool when: the team is all ML, one cloud, wants registry and lineage out of the box.
- Failure modes: pipeline definitions that call vendor SDKs everywhere become impossible to move; a managed service quota or region limit blocks a job; IAM role missing for a step.
- Vertex reuse of the KFP YAML: the compiled file from the local compile can be submitted as a Vertex pipeline job (`template_path`), so the same `@dsl.pipeline` code that I compile here is what Vertex runs. I checked the compiled file's header and keys locally. I did NOT call Vertex, and I did not install the Google SDK, so the submit call below is from the docs as I remember them.
- I also parsed an Amazon States Language sketch (Step Functions) with plain Python to prove its states and transitions are consistent; that is not AWS's validator.

**Example:** A bank-like team on one cloud with only ML jobs picks the vendor pipeline. A platform team that also runs nightly warehouse loads on Airflow keeps Airflow as the top scheduler and calls the cloud training job from one task (the pipeline in the cloud tool does the ML part only). Both are valid; say why.

**Code:** compile a KFP pipeline for Vertex and inspect it (python block), the Step Functions sketch (json block), and the Vertex submit call as comments in the bash block (not executed).
```python
# --- compile_for_vertex.py ---
from kfp import compiler, dsl


@dsl.component(base_image="python:3.12")
def train(lr: float) -> float:
    return round(1.0 - abs(lr - 0.01) * 10, 3)


@dsl.pipeline(name="vertex-demo", pipeline_root="gs://YOUR_BUCKET/pipeline_root")   # placeholder bucket
def vertex_demo(lr: float = 0.01):
    train(lr=lr).set_cpu_limit("2").set_memory_limit("4G")


compiler.Compiler().compile(vertex_demo, "vertex_demo.yaml")

# --- check_yaml.py ---
import yaml
head = open("vertex_demo.yaml").read().splitlines()[:1]
doc = next(yaml.safe_load_all(open("vertex_demo.yaml")))
print("first line:", head[0])
print("top-level keys:", sorted(doc))
print("schemaVersion:", doc["schemaVersion"], "| sdkVersion:", doc["sdkVersion"])
print("pipelineInfo:", doc["pipelineInfo"], "| default pipeline_root:", doc["defaultPipelineRoot"])

# --- check_asl.py ---
import json
d = json.load(open("states.json")); S = d["States"]
targets = {d["StartAt"]}
for n, s in S.items():
    if "Next" in s: targets.add(s["Next"])
    for c in s.get("Choices", []): targets.add(c["Next"])
    if "Default" in s: targets.add(s["Default"])
    assert s["Type"] in ("Succeed", "Fail", "Choice") or "Next" in s or s.get("End"), f"{n} has no exit"
missing = targets - set(S)
reachable = targets & set(S)
print("states:", list(S), "| missing targets:", sorted(missing) or "none", "| unreachable:", sorted(set(S) - reachable) or "none")
```

```json
{
  "Comment": "retrain then register, concept sketch",
  "StartAt": "Train",
  "States": {
    "Train": {"Type": "Task", "Resource": "arn:aws:states:::sagemaker:createTrainingJob.sync", "Parameters": {"TrainingJobName.$": "$.job_name"}, "Retry": [{"ErrorEquals": ["States.TaskFailed"], "MaxAttempts": 1}], "Next": "Good?"},
    "Good?": {"Type": "Choice", "Choices": [{"Variable": "$.auc", "NumericGreaterThan": 0.8, "Next": "Register"}], "Default": "Stop"},
    "Register": {"Type": "Task", "Resource": "arn:aws:states:::lambda:invoke", "End": true},
    "Stop": {"Type": "Succeed"}
  }
}
```

```bash
# NOT EXECUTED (needs a GCP project, credentials and a bucket; check current docs for the exact calls):
#   from google.cloud import aiplatform
#   aiplatform.init(project="PROJECT", location="REGION")
#   aiplatform.PipelineJob(display_name="vertex-demo", template_path="vertex_demo.yaml",
#                          pipeline_root="gs://YOUR_BUCKET/pipeline_root", parameter_values={"lr": 0.01}).run()
# What did run: python -I compile_for_vertex.py && python -I check_yaml.py && python3 -I check_asl.py
```

**Output (my run):** kfp 2.17.3 compile and my two checks. No cloud call.
```text
first line: # PIPELINE DEFINITION
top-level keys: ['components', 'defaultPipelineRoot', 'deploymentSpec', 'pipelineInfo', 'root', 'schemaVersion', 'sdkVersion']
schemaVersion: 2.1.0 | sdkVersion: kfp-2.17.3
pipelineInfo: {'name': 'vertex-demo'} | default pipeline_root: gs://YOUR_BUCKET/pipeline_root
states: ['Train', 'Good?', 'Register', 'Stop'] | missing targets: none | unreachable: none
```

**Follow-ups:**
1. *Is KFP YAML really portable?* The definition format is, the base images, buckets and service accounts inside it are not.
2. *SageMaker Pipelines or Step Functions?* ML-centric with registry and lineage: SageMaker Pipelines. Many AWS services and non-ML steps: Step Functions.
3. *Cost difference?* I do not quote numbers; compare the orchestration fee (small) against compute and engineering time.

**Common mistakes:** Comparing tools without naming the workload. Claiming a service does lineage without checking. Hard-coding project IDs in the pipeline file. Treating managed Airflow as zero-ops (versions, plugins, networking still need care).

### Q30 ⭐⭐ 🟡 Retraining triggers and pipeline parametrisation. Compare schedule-based, data-volume-based, drift-alert-based and performance-based triggers, how a trigger starts a pipeline (Airflow REST API or TriggerDagRunOperator, Prefect run_deployment, KFP create run, EventBridge to SageMaker), and what parameters a run takes (data date range, model version, dry-run flag, hyperparameters). Part 8 owns drift detection itself. Show a trigger-decision function and a parametrised DAG run with conf, run locally with airflow dags test and its --conf option if available.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** A retraining trigger is one small decision function (performance, then drift, then data volume, then age) that returns yes or no with a reason, and starting the run just means calling the orchestrator with a conf or parameters dict, so the pipeline code is the same whoever pulls the trigger.

**Then explain:**
- Trigger types: schedule (simple, wastes runs when nothing changed, misses a sudden shift); data volume (new rows since last train, good when labels arrive steadily); drift alert (input or prediction distribution moved, early but can fire without any harm to accuracy; Part 8 owns detection); performance (live metric below a floor, the strongest signal but labels are delayed, so it can be late). I order the rules from most to least urgent and also keep an age limit as a safety net.
- How a trigger starts a pipeline: Airflow: `TriggerDagRunOperator` from a gate DAG, or the REST API (check the API reference for path and auth); Prefect: `run_deployment(name, parameters=...)` or `prefect deployment run` (the CLI form ran in Q24); KFP: `Client.create_run_from_pipeline_package(..., arguments={...})`; AWS: EventBridge rule to a SageMaker pipeline start. Only the Airflow `--conf` path and the parameter checks were run here; REST, EventBridge and KFP submit are not executed.
- Run parameters: data end date and lookback window, model version or `auto`, a `dry_run` flag, hyperparameters, and a `reason` for the audit trail. Validate them in the DAG (Airflow `Param` with type and range). I ran a conf with `lookback_days: 9999` and it was refused before any task started.
- Failure modes: a trigger that fires every hour (flapping) because the drift metric hovers near the limit, so add a cooldown or minimum interval; two triggers firing at once (use one run at a time, `max_active_runs=1`, not tested here); retraining on bad data (put data checks first in the pipeline); dry run that still registers a model (my `dry_run` skips training and register).
- A trigger should not auto-promote a model. Retraining produces a candidate; promotion goes through the gate in Part 7.

**Example:** Today is 2026-10-26, last trained 2026-10-01 (25 days). Case "quiet": 5,000 new rows, PSI 0.05, AUC 0.86, so no trigger (25 < 30 days). Case "volume": 250,000 rows >= 100,000, so train. Case "drift": PSI 0.31 > 0.25, so train. Case "perf+drift": AUC 0.74 < 0.80 wins as the first rule, so the reason says performance. "No labels yet": AUC missing, other signals quiet, so no trigger. A model last trained 2026-09-01 is 55 days old, over the limit, so the schedule rule fires.

**Code:** decision function, a parametrised DAG with `Param` validation, and a gate DAG using `TriggerDagRunOperator` (python block); commands (bash block). The driver `code/q30/run.sh` runs everything with its own AIRFLOW_HOME.
```python
# --- triggers.py ---
"""Retraining trigger decision. Pure Python; the inputs come from your monitoring job (Part 8 owns drift detection)."""
from datetime import date


def decide(today, last_trained, new_rows, drift_psi, live_auc, *,
           max_age_days=30, min_new_rows=100_000, psi_limit=0.25, auc_floor=0.80):
    """Return (should_train, reason). First matching rule wins, ordered from most to least urgent."""
    if live_auc is not None and live_auc < auc_floor:
        return True, f"performance: live AUC {live_auc} < floor {auc_floor}"
    if drift_psi is not None and drift_psi > psi_limit:
        return True, f"drift: PSI {drift_psi} > {psi_limit}"
    if new_rows >= min_new_rows:
        return True, f"volume: {new_rows} new rows >= {min_new_rows}"
    age = (today - last_trained).days
    if age >= max_age_days:
        return True, f"schedule: model is {age} days old (limit {max_age_days})"
    return False, f"no trigger: age {age}d, rows {new_rows}, psi {drift_psi}, auc {live_auc}"


def build_conf(today, reason, *, dry_run=False, model_version="auto", lookback_days=30):
    """The parameters a triggered run takes. Same shape for Airflow conf, Prefect parameters and KFP arguments."""
    return {"reason": reason, "data_end": today.isoformat(), "lookback_days": lookback_days,
            "model_version": model_version, "dry_run": dry_run}


if __name__ == "__main__":
    today, last = date(2026, 10, 26), date(2026, 10, 1)
    cases = [
        ("quiet", dict(new_rows=5_000, drift_psi=0.05, live_auc=0.86)),
        ("volume", dict(new_rows=250_000, drift_psi=0.05, live_auc=0.86)),
        ("drift", dict(new_rows=5_000, drift_psi=0.31, live_auc=0.86)),
        ("perf+drift", dict(new_rows=5_000, drift_psi=0.31, live_auc=0.74)),
        ("no labels yet", dict(new_rows=5_000, drift_psi=0.05, live_auc=None)),
    ]
    for name, kw in cases:
        print(f"{name:14}", decide(today, last, **kw))
    print("old model     ", decide(today, date(2026, 9, 1), 5_000, 0.05, 0.86))
    print(build_conf(today, "drift: PSI 0.31 > 0.25", dry_run=True))

# --- retrain_dag.py ---
import pendulum
from airflow.sdk import Param, dag, get_current_context, task


@dag(
    schedule=None,  # started by a trigger, never by the clock
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False,
    params={
        "data_end": Param("2026-10-01", type="string", pattern=r"^\d{4}-\d{2}-\d{2}$"),
        "lookback_days": Param(30, type="integer", minimum=1, maximum=365),
        "model_version": Param("auto", type="string"),
        "dry_run": Param(False, type="boolean"),
        "reason": Param("manual", type="string"),
    },
)
def retrain():
    @task
    def plan():
        p = get_current_context()["params"]
        print(f"PLAN reason={p['reason']!r} window={p['lookback_days']}d ending {p['data_end']} version={p['model_version']} dry_run={p['dry_run']}")
        return dict(p)

    @task
    def train(p: dict):
        if p["dry_run"]:
            print("TRAIN skipped (dry_run=True): would train and register nothing")
            return "skipped"
        print(f"TRAIN fit on {p['lookback_days']} days ending {p['data_end']}")
        return "trained"

    train(plan())


retrain()

# --- trigger_dag.py ---
import pendulum
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sdk import dag


@dag(schedule="@daily", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False)
def retrain_gate():
    TriggerDagRunOperator(
        task_id="start_retrain", trigger_dag_id="retrain",
        conf={"reason": "gate says yes", "dry_run": True, "data_end": "{{ ds }}"},
        wait_for_completion=False,
    )


retrain_gate()
```

```bash
python3 -I triggers.py
export AIRFLOW_HOME=/tmp/own_dir AIRFLOW__CORE__DAGS_FOLDER=/tmp/own_dir/dags AIRFLOW__CORE__LOAD_EXAMPLES=False
airflow db migrate
airflow dags test retrain 2026-10-26                                   # defaults
airflow dags test retrain 2026-10-26 --conf '{"reason":"drift: PSI 0.31","lookback_days":14,"data_end":"2026-10-25","dry_run":true}'
airflow dags test retrain 2026-10-26 --conf '{"lookback_days":9999}'   # refused by Param validation
# NOT EXECUTED (needs a running API server and a token; check the Airflow API reference):
#   curl -X POST "$AIRFLOW/api/v2/dags/retrain/dagRuns" -H "Authorization: Bearer $TOKEN" \
#        -H "Content-Type: application/json" -d '{"logical_date": null, "conf": {"reason": "drift", "dry_run": true}}'
```

**Output (my run):** Airflow 3.3.2, `dags test` with `--conf` (the option exists in this version). The gate DAG with `TriggerDagRunOperator` was parsed only, not run (no scheduler).
```text
--- decide()
quiet          (False, 'no trigger: age 25d, rows 5000, psi 0.05, auc 0.86')
volume         (True, 'volume: 250000 new rows >= 100000')
drift          (True, 'drift: PSI 0.31 > 0.25')
perf+drift     (True, 'performance: live AUC 0.74 < floor 0.8')
no labels yet  (False, 'no trigger: age 25d, rows 5000, psi 0.05, auc None')
old model      (True, 'schedule: model is 55 days old (limit 30)')
{'reason': 'drift: PSI 0.31 > 0.25', 'data_end': '2026-10-26', 'lookback_days': 30, 'model_version': 'auto', 'dry_run': True}
--- DagBag
import_errors: {}
['retrain', 'retrain_gate']
--- dags test retrain 
PLAN reason='manual' window=30d ending 2026-10-01 version=auto dry_run=False
TRAIN fit on 30 days ending 2026-10-01
DagRun Finished: dag_id=retrain state=success
--- dags test retrain --conf {"reason":"drift: PSI 0.31","lookback_days":14,"data_end":"2026-10-25","dry_run":true}
PLAN reason='drift: PSI 0.31' window=14d ending 2026-10-25 version=auto dry_run=True
TRAIN skipped (dry_run=True): would train and register nothing
DagRun Finished: dag_id=retrain state=success
--- dags test retrain --conf {"lookback_days":9999}
    raise ParamValidationError(f"Invalid input for param {k}: {e}") from None
airflow.sdk.exceptions.ParamValidationError: Invalid input for param lookback_days: 9999 is greater than the maximum of 365
```

**Follow-ups:**
1. *Schedule or event?* Start with schedule plus a volume rule. Add drift and performance when you have trusted metrics and a way to avoid flapping.
2. *Who approves a retrain?* Auto-train yes; auto-deploy no, unless there is an automatic gate with a rollback.
3. *How do I stop duplicate runs?* One active run per pipeline and a run key (the date and reason) so the same trigger twice does not train twice; not tested here.

**Common mistakes:** Treating drift as proof the model is bad. No cooldown. Training on the newest window with no check of the data. Letting `dry_run` write to production. Keeping the trigger logic inside the DAG so it cannot be unit tested.

### Q31 ⭐⭐ 🟡 Failure-handling design for ML pipelines: partial failure in the middle of training, a poisoned upstream table, a late upstream partition, a model that trains but fails the evaluation gate, a spot-instance interruption, duplicate runs. Cover checkpoints, atomic publish (write to a staging path then promote), data validation gates, circuit breakers, dead-letter handling, and the human on-call runbook. Simulate three failure modes in a small Python pipeline runner and show the real output of rerunning after each failure.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** Make every stage safe to rerun: checkpoint inside long steps, gate on validation and evaluation before anything touches production, publish with one atomic rename, and guard against duplicate runs with a lock.

**Then explain:**
- Crash in the middle of training (spot loss, OOM): write a checkpoint after each epoch to durable storage and resume from it on rerun. Failure mode: a checkpoint written half-way. Write to a temp file, then `os.replace`.
- Poisoned or late upstream data: a validation gate runs before training and fails fast. Bad input goes to a dead-letter folder with the reason, so someone can look at it. For a late partition, wait with a timeout, then fail with a clear message. Do not train on yesterday's data silently.
- Model trains but is worse: an evaluation gate compares to a threshold or to the current production model. If it fails, the run ends "gate failed", production is untouched, and that is not a pager event by itself.
- Atomic publish: write the model to a staging path, then promote with one rename (or one registry alias change). Readers see the old model or the new one, never a half-written one.
- Duplicate runs (a retry plus a manual trigger): use a lock keyed on the run id, or an idempotent run id, so the second run skips. Failure mode: a hard kill leaves a stale lock, so add a lock timeout or owner check.
- Circuit breaker: after N consecutive failures, stop auto-retrying and page a human. Runbook for on-call: where the logs are, which stage failed, is it safe to rerun (yes, because stages are idempotent), who owns the upstream table, how to roll back (point the alias at the previous model).

**Example:** A 4-epoch training crashes after epoch 2. Rerun starts at "epoch 2" and finishes epochs 3 and 4 only. A table with a label value of 7 never reaches training and lands in `dead_letter/`. A model scoring 0.9 against a 0.95 gate is not published, and `prod_model.json` still names run `r1`.

**Code:** the runner below uses fake scores on purpose, so you can hand-check the flow.
```python
"""Tiny pipeline runner: checkpoints, validation gate, eval gate, atomic publish, run lock."""
import json, os, sys, tempfile, shutil

class Crash(Exception): pass

def atomic_write(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f: json.dump(obj, f)
    os.replace(tmp, path)            # atomic on the same filesystem

def validate(rows):
    bad = [r for r in rows if r["label"] not in (0, 1)]
    if len(rows) < 4 or bad:
        raise ValueError(f"validation failed: rows={len(rows)} bad_labels={len(bad)}")

def train(work, rows, crash_at=None):
    ck = os.path.join(work, "ckpt.json")
    state = json.load(open(ck)) if os.path.exists(ck) else {"epoch": 0, "w": 0.0}
    print(f"  train: start at epoch {state['epoch']}")
    while state["epoch"] < 4:
        state["epoch"] += 1
        state["w"] = round(state["w"] + 0.25, 2)
        atomic_write(ck, state)      # checkpoint after every epoch
        if crash_at == state["epoch"]:
            raise Crash(f"spot instance gone after epoch {state['epoch']}")
    return state["w"]

def run(root, run_id, rows, crash_at=None, gate=0.9):
    work = os.path.join(root, "work", run_id); os.makedirs(work, exist_ok=True)
    lock = os.path.join(work, "LOCK")
    try: fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)   # duplicate-run guard
    except FileExistsError: print("  skip: another run holds the lock"); return "locked"
    try:
        validate(rows)
        w = train(work, rows, crash_at)
        score = w * 0.9 if gate > 0.9 else w          # pretend score; low-quality case below
        score = round(score, 2)
        if score < gate:
            print(f"  eval gate FAILED: score {score} < {gate}; production untouched"); return "gate_failed"
        stage = os.path.join(root, "staging_model.json")
        atomic_write(stage, {"run_id": run_id, "w": w, "score": score})
        os.replace(stage, os.path.join(root, "prod_model.json"))   # promote = one rename
        print(f"  published model from {run_id}, score {score}"); return "ok"
    except ValueError as e:
        os.makedirs(os.path.join(root, "dead_letter"), exist_ok=True)
        atomic_write(os.path.join(root, "dead_letter", run_id + ".json"), {"error": str(e), "rows": len(rows)})
        print(f"  {e} -> sent to dead_letter, no training"); return "poisoned"
    except Crash as e:
        print(f"  CRASH: {e}"); return "crashed"
    finally:
        os.close(fd); os.remove(lock)

def prod(root):
    p = os.path.join(root, "prod_model.json")
    return open(p).read() if os.path.exists(p) else "none"

good = [{"x": i, "label": i % 2} for i in range(8)]
poison = good + [{"x": 99, "label": 7}]
root = tempfile.mkdtemp()
print("A. crash mid-training, then rerun same run_id"); print(" attempt 1:", run(root, "r1", good, crash_at=2))
print(" attempt 2:", run(root, "r1", good)); print(" prod:", prod(root))
print("B. poisoned upstream table"); print(" result:", run(root, "r2", poison)); print(" prod unchanged:", prod(root))
print(" dead_letter:", os.listdir(os.path.join(root, "dead_letter")))
print("C. model fails evaluation gate (gate 0.95)"); print(" result:", run(root, "r3", good, gate=0.95)); print(" prod unchanged:", prod(root))
print("D. duplicate run while one is active")
os.makedirs(os.path.join(root, "work", "r4")); open(os.path.join(root, "work", "r4", "LOCK"), "w").close()
print(" result:", run(root, "r4", good))
shutil.rmtree(root)
```

**Output (my run):** `python3 -I q31_runner.py`, Python 3.13, temp directory, real output:
```text
A. crash mid-training, then rerun same run_id
  train: start at epoch 0
  CRASH: spot instance gone after epoch 2
 attempt 1: crashed
  train: start at epoch 2
  published model from r1, score 1.0
 attempt 2: ok
 prod: {"run_id": "r1", "w": 1.0, "score": 1.0}
B. poisoned upstream table
  validation failed: rows=9 bad_labels=1 -> sent to dead_letter, no training
 result: poisoned
 prod unchanged: {"run_id": "r1", "w": 1.0, "score": 1.0}
 dead_letter: ['r2.json']
C. model fails evaluation gate (gate 0.95)
  train: start at epoch 0
  eval gate FAILED: score 0.9 < 0.95; production untouched
 result: gate_failed
 prod unchanged: {"run_id": "r1", "w": 1.0, "score": 1.0}
D. duplicate run while one is active
  skip: another run holds the lock
 result: locked
```
Nothing here ran on a real orchestrator or spot instance; the crash is a raised exception, not a killed process.

**Follow-ups:**
- *What if the process is killed with no exception?* The checkpoint file and the lock file stay on disk. The checkpoint is fine, but the lock is stale. Give the lock an owner id and a timeout.
- *Why not just retry everything?* Retries fix transient faults. A poisoned table or a failed gate will fail again, so those need a human or a different input.
- *Where does the atomic promote live in real life?* A registry alias, a symlink swap or an object-store "current" pointer. Part 7 covers the registry. Check your storage's rename semantics: on many object stores a rename is copy plus delete, not atomic.

**Common mistakes:**
- Training straight into the production path.
- Retrying a validation failure three times and hiding it.
- Checkpoints that are not atomic, so a crash leaves a corrupt file that the resume then trusts.
- No lock timeout, so one killed run blocks every later run.
- Treating "gate failed" and "pipeline crashed" as the same alert.

### Q32 ⭐⭐ 🟢 Orchestration skills in India MLOps hiring: what do Bengaluru-style postings and screens ask about Airflow, Kubeflow, Prefect, Vertex AI Pipelines and SageMaker Pipelines, and how do you build proof without a company budget? Summarise skills lists from postings (not interview reports), then give a lab plan: an Airflow standalone or dags test project, a Prefect flow, a kfp compile, a README and a diagram. Include a skills-to-lab table and a list of free-tier limits to check. Run the core of the lab locally.
**Asked at:** Bengaluru MLOps job postings that list Airflow, Kubeflow, Vertex AI or SageMaker Pipelines (Infosys via jobs.weekday.works, Deloitte Bengaluru, Stats Perform via foundit, GlobalLogic, Datamatics via metaintro; search snippets only, not opened); postings show required skills, not interview questions; IT-services firms, product companies and GCCs
**Say this first (1 line):** Postings pair Airflow or Kubeflow with Python, Docker, Kubernetes, MLflow and a cloud, so I build a small public lab that proves each of those: an Airflow DAG tested locally, a Prefect flow with retries, a kfp pipeline compiled to YAML, and a README with a diagram.

**Then explain:**
- What postings ask for (from search snippets of Bengaluru-style postings, not interview reports, not opened): Airflow or Kubeflow named together with Python, Docker, Kubernetes, MLflow, CI/CD and one cloud. Some name Vertex AI Pipelines or SageMaker Pipelines. Kubeflow-heavy roles seem to want more years and Kubernetes depth. Treat this as a hint, not a rule.
- Proof without a budget: everything below runs on a laptop. `airflow dags test` runs a DAG without any scheduler. `kfp` compiles a pipeline to YAML without a cluster. A Prefect flow runs locally. For Vertex and SageMaker you can only read docs and explain the shape of a pipeline; I would say so honestly in the interview.
- Show decisions, not tool counts: a README that says why retries are 2, why XCom carries a path and not a dataframe, why caching is off for one step.
- Failure mode of the lab: copying a tutorial. Add one thing of your own, like a validation gate or a failure drill, and write down what broke.
- Free-tier limits to check before relying on any cloud: free credits and their expiry, GPU quota, managed Airflow or pipeline service minimum cost, egress, and whether a card is needed. I give no numbers; check current docs.

**Example (skills-to-lab table):**

| Posting skill | Lab piece | Proof in the repo |
|---|---|---|
| Airflow | TaskFlow DAG, `dags test` | `dags/ml_train.py`, run log |
| Prefect | flow with task retries | `pf_flow.py`, retry log lines |
| Kubeflow Pipelines | `@dsl.component` + compile | `lab_pipeline.yaml` |
| Docker, Kubernetes | image name in the kfp component, pod spec (Q35) | README note, YAML parse |
| MLflow, CI/CD | out of scope here (Parts 4 and 7) | link to those labs |
| Vertex or SageMaker Pipelines | read-only comparison table | README, marked "not run" |

**Code:** three small files plus the runner script.
```python
# ===== q32_lab/dags/ml_train.py =====
from __future__ import annotations
import pendulum
from airflow.sdk import dag, task

@dag(dag_id="ml_train", schedule="@daily", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
     catchup=False, default_args={"retries": 2}, tags=["ml", "lab"])
def ml_train():
    @task
    def extract(ds=None):
        return {"path": f"s3://bucket/raw/{ds}.parquet"}
    @task
    def train(meta: dict):
        print("training on", meta["path"]); return "model-v1"
    @task
    def evaluate(model: str):
        print("evaluating", model); return 0.91
    evaluate(train(extract()))
ml_train()

# ===== q32_lab/pf_flow.py =====
from prefect import flow, task
calls = {"n": 0}

@task(retries=2, retry_delay_seconds=0)
def flaky_load():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ValueError("transient")
    return "loaded"

@flow(name="lab-flow")
def lab_flow():
    return flaky_load()

if __name__ == "__main__":
    print("result:", lab_flow(), "calls:", calls["n"])

# ===== q32_lab/kfp_pipe.py =====
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
```
```bash
#!/bin/bash
# runs the three lab pieces with throwaway homes outside the repo
B=/tmp/claude-0/b5p05; T=$(mktemp -d /tmp/claude-0/b5p05_q31_40/lab.XXXX); D=$(cd "$(dirname "$0")"; pwd)
echo "== Airflow dags test"
AIRFLOW_HOME=$T/af AIRFLOW__CORE__DAGS_FOLDER=$D/dags AIRFLOW__CORE__LOAD_EXAMPLES=False $B/af/bin/airflow db migrate >/dev/null 2>&1
AIRFLOW_HOME=$T/af AIRFLOW__CORE__DAGS_FOLDER=$D/dags AIRFLOW__CORE__LOAD_EXAMPLES=False $B/af/bin/airflow dags test ml_train 2026-10-01 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | grep -E "^training on|^evaluating|Pushing xcom|DagRun Finished|Marking run" | sed -E 's/^[^ ]+ \[info *\] //; s/ ti=.*task_id=.([a-z_]+).*/ task_id=\1/' | cut -c1-170
echo "== Prefect flow"
PREFECT_HOME=$T/pf $B/pf/bin/python -I $D/pf_flow.py 2>&1 | grep -E "Retry|Completed|result:" | sed 's/\x1b\[[0-9;]*m//g' | cut -c1-160
echo "== kfp compile"
(cd $T && $B/kf/bin/python -I $D/kfp_pipe.py && head -3 lab_pipeline.yaml && grep -c "" lab_pipeline.yaml)
rm -rf $T
```

**Output (my run):** `run_lab.sh` with apache-airflow 3.3.2, prefect 3.9.0, kfp 2.17.3, each with its own temp home. The Airflow log is verbose, so the script filters it. Real output:
```text
== Airflow dags test
Pushing xcom                   [task] loc=task_runner.py:2280 task_id=extract
training on s3://bucket/raw/2026-10-01.parquet
Pushing xcom                   [task] loc=task_runner.py:2280 task_id=train
evaluating model-v1
Pushing xcom                   [task] loc=task_runner.py:2280 task_id=evaluate
Marking run <DagRun ml_train @ 2026-10-01 00:00:00+00:00: manual__2026-10-26T14:27:15.046651+00:00, state:running, queued_at: None. run_type: manual> successful [airflow.
DagRun Finished: dag_id=ml_train, logical_date=2026-10-01 00:00:00+00:00, run_id=manual__2026-10-26T14:27:15.046651+00:00, run_start_date=2026-10-01 00:00:00+00:00, run_e
== Prefect flow
14:27:37.697 | INFO    | Task run 'flaky_load-6d0' - Task run failed with exception: ValueError('transient') - Retry 1/2 will start immediately
14:27:37.700 | INFO    | Task run 'flaky_load-6d0' - Task run failed with exception: ValueError('transient') - Retry 2/2 will start immediately
14:27:37.703 | INFO    | Task run 'flaky_load-6d0' - Finished in state Completed()
14:27:38.695 | INFO    | Flow run 'screeching-serval' - Finished in state Completed()
result: loaded calls: 3
== kfp compile
compiled
# PIPELINE DEFINITION
# Name: lab-pipeline
# Inputs:
73
```
The compiled YAML has 73 lines. No Airflow scheduler, no Kubeflow cluster, no cloud service was used.

**Follow-ups:**
- *Which one first?* Airflow, because the most postings name it.
- *No cluster, so how do you show Kubeflow?* Compile, then read the YAML: components, deploymentSpec, parameters. Say it was not run on a cluster.
- *Where do I host the README diagram?* Any image in the repo; keep it to five boxes.

**Common mistakes:**
- Listing every tool in the CV with no repo.
- Screenshots of a managed service you cannot reproduce.
- Claiming cloud pipeline experience from reading docs.
- Leaving an AIRFLOW_HOME, SQLite file or logs in the repo.

### Q33 ⭐ 🔴 Design question: a multi-team ML orchestration platform for 30 pipelines. Cover one shared Airflow versus per-team deployments, DAG repository layout and ownership (CODEOWNERS), a DAG deployment path (git-sync or image bake), executor choice, resource isolation with pools and queues, secrets, the base operator or pod template library, SLAs and on-call, cost, and an onboarding template. Give a component table with owners and a DAG linter script that enforces tags, owner, retries and no top-level network calls. Pure design; the linter runs locally.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** For about 30 pipelines I would start with one shared Airflow deployment run by a platform team, one repo with CODEOWNERS per team folder, per-task containers for heavy code, and a linter in CI that rejects DAGs without owner, tags and retries.

**Then explain:**
- Shared versus per-team: shared is cheaper to run and gives one place to look. Per-team gives isolation and independent upgrades but multiplies ops work. At 30 pipelines I start shared, with pools and queues for isolation, and split a team out only if upgrades or security force it. Failure mode of shared: one team's heavy DAG file slows parsing for everyone.
- Repo layout: `dags/<team>/...`, `CODEOWNERS` maps each folder to its team, shared code in a library package, not copied between DAGs. Deploy by git-sync (fast, no rebuild) or by baking DAGs into the image (strict versioning, slower). Both work; choose by how often DAGs change. Check current docs for how DAG bundles work in Airflow 3.
- Executor: Celery (warm workers) or Kubernetes (a pod per task, better isolation, slower start). Hybrid setups exist; check the docs for what your version still supports.
- Isolation: pools cap concurrent slots for scarce resources (a GPU, a database). Queues route tasks to worker groups. Heavy ML dependencies live in task images (Q35), not in the Airflow image.
- Secrets: a secrets backend or Kubernetes secrets, never in DAG code. SLAs and on-call: an owner per DAG, failure callbacks to the team's channel, and a clear page-or-ticket rule. Cost: tag every DAG with team and cost centre and report per tag.
- Onboarding template: a cookie-cutter DAG with default_args, tags and a test; new teams copy it.

**Example (components):**

| Component | Owner | Notes |
|---|---|---|
| Scheduler, DAG processor, API server | Platform | upgrades, scaling, metadata DB |
| Executor and worker pools | Platform | Celery or Kubernetes; capacity |
| DAG folders `dags/<team>/` | Each team | CODEOWNERS enforced |
| Task images | Each team | pinned tags or digests |
| Shared operator and pod template library | Platform | versioned package |
| Secrets backend | Security and platform | teams request, never read others' |
| Linter and CI checks | Platform | blocks merge |
| Alerts and on-call rota | Each team for its DAGs, platform for the cluster | owner field routes it |

**Code:** an AST-based linter. It never imports the DAG, so a top-level network call cannot run during the lint.
```python
"""Static DAG linter (AST only, never imports the DAG): tags, owner, retries, no top-level network calls."""
import ast, sys, pathlib

NET_MODULES = {"requests", "urllib", "urllib3", "httpx", "boto3", "psycopg2", "pymysql", "socket", "snowflake"}

def kw(call, name):
    for k in call.keywords:
        if k.arg == name: return k.value
    return None

def dag_calls(tree):
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            f = n.func
            nm = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else ""
            if nm == "dag" or nm == "DAG":
                yield n

def default_args_keys(call):
    da = kw(call, "default_args")
    return {k.value for k in da.keys if isinstance(k, ast.Constant)} if isinstance(da, ast.Dict) else set()

def top_level_net(tree):
    hits = []
    class V(ast.NodeVisitor):                        # skip function bodies: they run at task time
        def visit_FunctionDef(self, n): pass
        visit_AsyncFunctionDef = visit_FunctionDef
        def visit_Call(self, n):
            root = n.func
            while isinstance(root, (ast.Attribute, ast.Call)):
                root = root.value if isinstance(root, ast.Attribute) else root.func
            if isinstance(root, ast.Name) and root.id in NET_MODULES:
                hits.append((n.lineno, root.id))
            self.generic_visit(n)
    V().visit(tree)
    return hits

def lint(path):
    tree = ast.parse(pathlib.Path(path).read_text()); errs = []
    calls = list(dag_calls(tree))
    if not calls: return ["no DAG found"]
    for c in calls:
        da = default_args_keys(c)
        tags = kw(c, "tags")
        if not (isinstance(tags, ast.List) and tags.elts): errs.append(f"line {c.lineno}: missing tags")
        if "owner" not in da: errs.append(f"line {c.lineno}: default_args has no owner")
        if "retries" not in da: errs.append(f"line {c.lineno}: default_args has no retries")
    for ln, mod in sorted(set(top_level_net(tree))): errs.append(f"line {ln}: top-level call into {mod}")
    return errs

if __name__ == "__main__":
    bad = 0
    for p in sorted(pathlib.Path(sys.argv[1]).glob("*.py")):
        e = lint(p); bad += bool(e)
        print(f"{p.name}: {'OK' if not e else 'FAIL'}")
        for m in e: print("   ", m)
    sys.exit(1 if bad else 0)
```

**Output (my run):** `python3 -I q33_dag_lint.py q33_dags` on three sample files (`good_dag.py`, `bad_dag.py` with a top-level `requests.get`, `bad2_dag.py` with a top-level `boto3.client`), real output:
```text
bad2_dag.py: FAIL
    line 7: default_args has no retries
    line 6: top-level call into boto3
bad_dag.py: FAIL
    line 6: missing tags
    line 6: default_args has no owner
    line 6: default_args has no retries
    line 4: top-level call into requests
good_dag.py: OK
exit=1
```
Pure design otherwise: no shared deployment, git-sync, Celery or Kubernetes was run. The linter is heuristic: it checks literal `tags=[...]` and a literal `default_args` dict, so a DAG that builds them elsewhere needs a different check.

**Follow-ups:**
- *Why a linter and not just review?* Reviewers miss a `requests.get` at module level. The scheduler would run it on every parse.
- *How do you stop one team starving others?* Pools, per-DAG concurrency limits and separate queues. Check your executor's docs.
- *Multi-tenant security?* Airflow's own docs describe its multi-team story as limited or evolving; check current docs. For hard isolation use separate deployments.

**Common mistakes:**
- One giant DAG folder with no owners.
- Putting torch in the Airflow image.
- Per-team Airflow for every team from day one.
- A linter that imports DAG files, which runs the bad code it is meant to catch.

### Q34 ⭐ 🔴 Airflow scheduler internals and scale. Explain how the scheduler loop works at concept level (DAG processing, creating runs, queueing task instances, heartbeats), what slows it down (heavy top-level code, thousands of tiny DAGs, database load), running multiple schedulers with row-level locking, min_file_process_interval, and measuring DAG parse time. Show a script that times DagBag parsing of generated DAG files (10 versus 500) and show real numbers from this machine. A real multi-scheduler cluster is not executed.
**Asked at:** Airflow guides on executors and operations (datadriven.io executors page, oneuptime.com 'How to Configure Airflow Executors' 2026, datavidhya.com; search snippets only, not opened); generic prep blogs, some inaccurate, check Airflow docs; platform and MLOps roles
**Say this first (1 line):** The scheduler (with the DAG processor) loops: parse DAG files, create runs that are due, queue ready task instances, and heartbeat; most slowness I have seen comes from heavy top-level code, too many files and a busy database, so I measure parse time first.

**Then explain:**
- Concept loop: (1) the DAG processor parses files and stores the DAG structure in the metadata DB (in Airflow 3 it is a separate component; check docs for your version); (2) the scheduler creates DAG runs whose time has come; (3) it finds task instances whose dependencies are met and hands them to the executor; (4) it records heartbeats and state changes, and cleans up tasks that died.
- What slows it: top-level code that imports big libraries or calls a network or database (runs on every parse); thousands of tiny DAG files each paying a fixed cost; DB load from many task state updates; very frequent re-parsing.
- Multiple schedulers: you can run more than one against the same database. They coordinate with row-level locks in the DB (`SELECT ... FOR UPDATE SKIP LOCKED` style), so the DB must support it (PostgreSQL or MySQL 8, not SQLite). More schedulers add throughput and availability but also DB load.
- Knobs I would look up, not trust from memory: in the installed 3.3.2 default config, `min_file_process_interval`, `parsing_processes` and `dag_file_processor_timeout` appear under `[dag_processor]`, and `use_row_level_locking` and `max_dagruns_to_create_per_loop` under `[scheduler]`. Older docs put several of these under `[scheduler]`; check current docs for your version.
- Measure before tuning: time how long the parse takes per file. Put heavy imports inside the task function.

**Example:** 500 files at 2 ms each parse in about a second here. Ten files that each sleep 0.2 s at import time cost two seconds. Ten slow files cost twice as much as 500 light ones, so file count is not the whole story.

**Code:** run with the Airflow venv's Python; it generates the DAG files in temp folders, then times `DagBag`.
```python
"""Time DagBag parsing of N generated DAG files. Run with the Airflow venv python."""
import os, sys, tempfile, time, pathlib
home = tempfile.mkdtemp(prefix="q34home_", dir="/tmp/claude-0/b5p05_q31_40")
os.environ.update(AIRFLOW_HOME=home, AIRFLOW__CORE__LOAD_EXAMPLES="False")
TEMPLATE = '''import pendulum
{heavy}
from airflow.sdk import dag, task

@dag(dag_id="gen_{i}", schedule="@daily", start_date=pendulum.datetime(2026, 1, 1), catchup=False, tags=["gen"])
def gen_{i}():
    @task
    def a(): return 1
    @task
    def b(x): return x
    @task
    def c(x): return x
    c(b(a()))
gen_{i}()
'''
def make(n, heavy=""):
    d = pathlib.Path(tempfile.mkdtemp(prefix="dags_", dir="/tmp/claude-0/b5p05_q31_40"))
    for i in range(n):
        (d / f"gen_{i}.py").write_text(TEMPLATE.format(i=i, heavy=heavy))
    return d
from airflow.models.dagbag import DagBag
DagBag(dag_folder=str(make(1)))            # warm-up: pays the one-off import cost
for label, n, heavy in [("10 light files", 10, ""), ("500 light files", 500, ""),
                        ("10 files, 0.2 s top-level sleep each", 10, "import time; time.sleep(0.2)")]:
    d = make(n, heavy)
    t = time.perf_counter(); bag = DagBag(dag_folder=str(d)); dt = time.perf_counter() - t
    print(f"{label:40s} dags={len(bag.dags):4d} errors={len(bag.import_errors)} total={dt:6.2f}s per_file={dt/n*1000:7.1f}ms")
```

**Output (my run):** apache-airflow 3.3.2, Python 3.13, this sandbox, one in-process run after a one-file warm-up (so the Airflow import cost is excluded):
```text
10 light files                           dags=  10 errors=0 total=  0.03s per_file=    3.1ms
500 light files                          dags= 500 errors=0 total=  0.99s per_file=    2.0ms
10 files, 0.2 s top-level sleep each     dags=  10 errors=0 total=  2.04s per_file=  204.4ms
```
Caveats: one run, no repeats, so treat the numbers as rough; they are specific to this machine. The real processor parses in separate worker processes and adds serialization and DB writes, so `DagBag` time understates the real cost. No scheduler, multi-scheduler cluster or Postgres was run (not executed).

**Follow-ups:**
- *SQLite with two schedulers?* No. Use a DB with proper row locking.
- *How do I find the slow file?* Parse stats per file (Airflow shows parse duration in the UI or CLI; check your version), or time `DagBag` like above.
- *DAG generated from a config file?* Fine if the read is local and cheap. A network call at parse time is the classic bug.

**Common mistakes:**
- `import torch` or a DB query at module level.
- Lowering the parse interval to make DAG changes appear faster, then wondering why CPU is high.
- Adding schedulers when the DB is the bottleneck.
- Quoting parse numbers from another machine.

### Q35 ⭐ 🔴 Containerised and per-task environments for ML in Airflow: KubernetesPodOperator, @task.docker, @task.virtualenv or external Python, and the pod template. Explain why heavy ML dependencies (torch, tensorflow) should not live in the Airflow image, how to pass GPU requests and secrets, how logs and XCom return values come back from a pod, and the cold-start trade-off. Show a KubernetesPodOperator task with resources and a pod spec; validate the YAML parse locally and parse the DAG with DagBag if the provider is installed. No pod is run.
**Asked at:** Airflow guides on executors and operations (datadriven.io executors page, oneuptime.com 'How to Configure Airflow Executors' 2026, datavidhya.com; search snippets only, not opened); generic prep blogs, some inaccurate, check Airflow docs; platform and MLOps roles
**Say this first (1 line):** Keep Airflow's image small and run each ML step in its own container, with KubernetesPodOperator for real isolation and GPUs, and `@task.virtualenv` or `@task.docker` for lighter cases.

**Then explain:**
- Why not put torch in the Airflow image: huge image, slow upgrades, and dependency conflicts between teams and with Airflow's own pins. A task image per project avoids all three.
- KubernetesPodOperator (from the cncf.kubernetes provider): launches a pod per task. You set the image, command, resources, node selector, tolerations, env and secrets. GPUs are requested as a resource limit (for example `nvidia.com/gpu`) and the cluster needs the GPU device plugin; check your cluster docs.
- Secrets: reference a Kubernetes Secret (env or volume) so the value never appears in the DAG or the log. Logs: with `get_logs=True` the operator streams the container's stdout into the task log. XCom: with `do_xcom_push=True` the operator adds a sidecar and reads `/airflow/xcom/return.json` after the main container ends; keep the value small. Check current provider docs for the exact behaviour.
- Pod template: a YAML base pod (service account, node pool, volumes) that tasks start from, so the platform sets defaults once.
- `@task.virtualenv` builds a venv per run (slow install, but no container). `@task.docker` needs a Docker daemon on the worker and the docker provider (not installed here). External Python points at a prebuilt interpreter.
- Cold start trade-off: a pod per task pays image pull and scheduling time (seconds to minutes with big images); warm Celery workers start fast but share dependencies. Failure modes: pod stuck Pending (no GPU node), image pull errors, OOMKilled, and orphan pods if the worker dies.

**Example:** The DAG below asks for 4 CPUs, 16Gi and one GPU, tolerates the GPU node taint and mounts a DB password from the Secret `ml-db`. The YAML is the pod template that gives these defaults to every task.

**Code:** the DAG (python) and the pod template (yaml), then the check script.
```python
# ===== q35_dags/train_gpu.py =====
import pendulum
from airflow.sdk import dag, task
from kubernetes.client import models as k8s
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.providers.cncf.kubernetes.secret import Secret

db_pw = Secret(deploy_type="env", deploy_target="DB_PASSWORD", secret="ml-db", key="password")

@dag(dag_id="train_gpu", schedule=None, start_date=pendulum.datetime(2026, 1, 1), catchup=False,
     tags=["ml", "k8s"], default_args={"owner": "ml-platform", "retries": 1})
def train_gpu():
    train = KubernetesPodOperator(
        task_id="train",
        name="train-pod",
        namespace="ml-jobs",
        image="registry.example.com/ml/train:1.4.2",      # pinned tag (ideally a digest)
        cmds=["python", "-m", "train"],
        arguments=["--run-date", "{{ ds }}", "--out", "/out/result.json"],
        env_vars={"MODEL_NAME": "ranker"},
        secrets=[db_pw],                                    # mounted from a k8s Secret, not in the DAG
        container_resources=k8s.V1ResourceRequirements(
            requests={"cpu": "4", "memory": "16Gi"},
            limits={"memory": "16Gi", "nvidia.com/gpu": "1"}),
        node_selector={"pool": "gpu"},
        tolerations=[k8s.V1Toleration(key="nvidia.com/gpu", operator="Exists", effect="NoSchedule")],
        get_logs=True,                                      # stream container stdout into the task log
        do_xcom_push=True,                                  # reads /airflow/xcom/return.json via a sidecar
        on_finish_action="delete_pod",
        startup_timeout_seconds=600,
    )

    @task.virtualenv(requirements=["numpy==2.1.0"], system_site_packages=False)
    def small_check():
        import numpy as np
        return float(np.arange(3).sum())
    train >> small_check()
train_gpu()

# ===== q35_check.py =====
import os, sys, tempfile, yaml
home = tempfile.mkdtemp(prefix="q35home_", dir="/tmp/claude-0/b5p05_q31_40")
os.environ.update(AIRFLOW_HOME=home, AIRFLOW__CORE__LOAD_EXAMPLES="False")
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.environ["K8S_PROVIDER_DIR"])        # provider unpacked outside the Airflow venv
pod = yaml.safe_load(open(os.path.join(here, "q35_pod_template.yaml")))
c = pod["spec"]["containers"][0]
print("pod yaml parses: kind =", pod["kind"], "| container =", c["name"], "| gpu limit =", c["resources"]["limits"]["nvidia.com/gpu"])
from airflow.models.dagbag import DagBag
bag = DagBag(dag_folder=os.path.join(here, "q35_dags"))
print("import_errors:", bag.import_errors)
d = bag.dags["train_gpu"]
for t in d.tasks: print(" task", t.task_id, type(t).__name__)
k = d.get_task("train")
print(" train gpu limit:", k.container_resources.limits["nvidia.com/gpu"], "| namespace:", k.namespace)
```
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: placeholder
  labels:
    app: ml-train
spec:
  restartPolicy: Never
  serviceAccountName: ml-train
  nodeSelector:
    pool: gpu
  tolerations:
    - key: nvidia.com/gpu
      operator: Exists
      effect: NoSchedule
  containers:
    - name: base
      image: registry.example.com/ml/train:1.4.2
      resources:
        requests: {cpu: "4", memory: 16Gi}
        limits: {memory: 16Gi, nvidia.com/gpu: "1"}
      volumeMounts:
        - {name: out, mountPath: /out}
  volumes:
    - {name: out, emptyDir: {}}
```

**Output (my run):** the provider (apache-airflow-providers-cncf-kubernetes 10.25.0) is NOT in the shared Airflow venv. I unpacked it with `pip install --target` (no deps) plus the `kubernetes` client libraries into a separate folder, and added that folder to `sys.path` in the script. Real output:
```text
pod yaml parses: kind = Pod | container = base | gpu limit = 1
import_errors: {}
 task train KubernetesPodOperator
 task small_check _PythonVirtualenvDecoratedOperator
 train gpu limit: 1 | namespace: ml-jobs
```
Not executed: no pod, cluster, GPU or secret was used, and `@task.virtualenv` was only parsed, not run. The validation is that the YAML parses and the DAG imports and parses with `DagBag` (no import errors). It does not check that the pod spec is valid for a real cluster.

**Follow-ups:**
- *Pod vs Docker operator?* Pod needs a cluster; docker needs a daemon on the worker. Pods scale better.
- *Big outputs?* Write to object storage and return the path through XCom.
- *Reduce cold start?* Smaller images, pre-pulled images on nodes, or keep warm workers for small tasks.

**Common mistakes:**
- `latest` image tags, so a rerun uses different code.
- Returning a large dataframe through XCom.
- No resource requests, so the scheduler packs pods badly.
- Secrets in `env_vars` in plain text.

### Q36 ⭐ 🔴 Dagster and the asset-centric view. Explain software-defined assets, jobs, schedules and sensors, partitions, IO managers, how a model becomes an asset with lineage, and what that gives versus a task-centric DAG in Airflow. Include honest trade-offs (smaller ecosystem, new mental model). If dagster installs, define two assets and materialise them locally and show the output; otherwise state the install error. Dagster Cloud and a webserver are not executed.
**Asked at:** Orchestrator comparison write-ups (zenml.io 'Orchestration showdown: Dagster vs Prefect vs Airflow', risingwave, dzone, deploybase, hightouch; search snippets only, not opened); vendor-adjacent blogs, treat specifics with caution; data and ML platform roles
**Say this first (1 line):** In Dagster you declare the data things you want to exist (assets, such as a table or a model) and what each depends on, and the tool works out the graph; Airflow asks you to declare the steps. For ML this gives lineage and "what is stale" almost for free.

**Then explain:**
- Software-defined asset: a Python function that produces one named thing, like `training_table` or `churn_model`. Its function arguments name its upstream assets, so the dependency graph and lineage come from the code.
- Jobs select which assets to run. Schedules run them on time. Sensors run them when something happens (a new file, an upstream event). Partitions slice an asset by date or other key, which gives backfills per partition and per-partition status.
- IO managers decide where an asset's value is stored and loaded (local pickle, file, warehouse, object store). The asset code stays free of storage code.
- A model as an asset: `churn_model` depends on `training_table`. When the table is rematerialised, the model shows as stale, and you can see which data version produced which model.
- Versus Airflow: Airflow is task-centric (run this, then that). It has a larger ecosystem, more people who know it and more hiring demand. Dagster has a smaller ecosystem and a new mental model (assets, definitions, resources), so a team used to Airflow needs time. Newer Airflow also has asset-style features; check current docs before saying one lacks something.
- Failure modes: forgetting that an asset's value is persisted by the IO manager (large values need a real store, not the default pickle); partition definitions that do not match the upstream's.

**Example:** Two assets: `training_table` yields 5 rows of `y = 2x`; `churn_model` fits `w` by least squares through the origin. Hand check: sum(x*y) = 2*(0+1+4+9+16) = 60 and sum(x^2) = 30, so w = 2.0.

**Code:**
```python
import dagster as dg

@dg.asset
def training_table() -> list[dict]:
    return [{"x": i, "y": 2 * i} for i in range(5)]

@dg.asset
def churn_model(training_table: list[dict]) -> dict:
    # fit y = w * x by least squares through the origin
    w = sum(r["x"] * r["y"] for r in training_table) / sum(r["x"] ** 2 for r in training_table)
    return {"w": w, "rows": len(training_table)}

defs = dg.Definitions(assets=[training_table, churn_model])

if __name__ == "__main__":
    result = dg.materialize([training_table, churn_model])
    print("success:", result.success)
    print("model value:", result.output_for_node("churn_model"))
    for e in result.get_asset_materialization_events():
        print("materialized:", e.asset_key.to_user_string())
```

**Output (my run):** dagster 1.13.26 installed with pip in a fresh venv, Python 3.13, `DAGSTER_HOME` set to a temp folder; `materialize()` runs in-process. The framework's own debug log lines are dropped here; these are the lines my script printed:
```text
success: True
model value: {'w': 2.0, 'rows': 5}
materialized: training_table
materialized: churn_model
```
Not executed: the Dagster webserver and UI, daemon (schedules and sensors), partitions and Dagster Cloud. Schedules, sensors, partitions and IO managers above are described from general knowledge; check the current Dagster docs for exact APIs, which have changed between versions.

**Follow-ups:**
- *When would you pick Dagster?* A data and ML team that cares about lineage, partitions and asset freshness, and has no big Airflow investment.
- *When stay on Airflow?* Existing DAGs, many provider integrations, hiring pool.
- *Is it either/or?* No. Some teams run both and trigger one from the other; that adds ops cost.

**Common mistakes:**
- Calling assets "just DAGs with new names". The unit of design is the data, not the step.
- Keeping huge values in the default IO manager.
- Claiming Dagster is better without naming the migration cost.

### Q37 ⭐ 🔴 Step Functions versus Airflow versus SageMaker Pipelines for an AWS-only team. Explain state machines in Amazon States Language (Task, Choice, Parallel, Map, Retry and Catch), standard versus express workflows at concept level, waiting for a training job with the .sync integration, and when a Lambda glue plus Step Functions beats MWAA. Write a small ASL JSON state machine for train, evaluate and conditionally register, and validate that it parses and every Next target exists, with a script. Nothing is deployed or executed on AWS.
**Asked at:** Cloud ML orchestration study guides (open-exam-prep AWS ML Engineer guide on SageMaker Pipelines versus Step Functions and EventBridge retraining, insertchat ML pipeline orchestration glossary, wecreateproblems MLOps interview questions; search snippets only, not opened); study guides and glossaries, not interview reports; MLOps roles on AWS, GCP and Azure
**Say this first (1 line):** For an AWS-only team, Step Functions is a good glue layer for service-to-service flows with Lambda and SageMaker jobs, SageMaker Pipelines is built for the ML DAG itself, and Airflow (MWAA) wins when you already have Airflow skills or many non-AWS systems. Check current docs for features and limits.

**Then explain:**
- Amazon States Language (ASL) is JSON. A state machine has `StartAt` and `States`. Types: Task (do work), Choice (branch on data), Parallel (run branches together), Map (loop over a list), Wait, Pass, Succeed, Fail.
- Error handling: `Retry` (error names, interval, attempts, backoff) and `Catch` (route to a fallback state). Put them on the Task state.
- Standard versus express workflows (concept): standard is for long-running, auditable, exactly-once style flows; express is for short, high-rate, at-least-once flows. Durations and limits change; check current docs.
- `.sync` integration: appending `.sync` to a service resource (for example a SageMaker training job) makes the state wait until the job finishes, so you do not poll in a Lambda. Which services support it: check current docs.
- Lambda glue plus Step Functions beats MWAA when the flow is event-driven, short, and mostly AWS API calls, and you do not want an always-on Airflow environment to pay for and patch. MWAA beats it when you need Python-defined dynamic DAGs, backfills, or lots of existing DAGs.
- SageMaker Pipelines: ML-specific steps, model registry integration and lineage in SageMaker. Less general than Step Functions.
- Failure modes: a Choice with no `Default` (the execution fails on an unmatched value), a `Next` typo, a Catch that swallows errors silently, and payload size limits between states.

**Example:** The machine trains with `.sync`, retries twice on a task failure, evaluates in a Lambda, then a Choice registers the model only if AUC is at least 0.85, otherwise it ends in `RejectModel` (a Succeed state: the pipeline worked, the model was not good enough). A training failure goes to `NotifyFailure`.

**Code:** the state machine (json) and an offline structure checker (python).
```json
{
  "Comment": "train, evaluate, register if good (sketch, not deployed)",
  "StartAt": "Train",
  "States": {
    "Train": {
      "Type": "Task",
      "Resource": "arn:aws:states:::sagemaker:createTrainingJob.sync",
      "Parameters": {"TrainingJobName.$": "$.job_name", "RoleArn.$": "$.role_arn"},
      "ResultPath": "$.train",
      "Retry": [{"ErrorEquals": ["States.TaskFailed"], "IntervalSeconds": 60, "MaxAttempts": 2, "BackoffRate": 2.0}],
      "Catch": [{"ErrorEquals": ["States.ALL"], "ResultPath": "$.error", "Next": "NotifyFailure"}],
      "Next": "Evaluate"
    },
    "Evaluate": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {"FunctionName": "evaluate-model", "Payload.$": "$"},
      "ResultSelector": {"auc.$": "$.Payload.auc"},
      "ResultPath": "$.eval",
      "Next": "GoodEnough"
    },
    "GoodEnough": {
      "Type": "Choice",
      "Choices": [{"Variable": "$.eval.auc", "NumericGreaterThanEquals": 0.85, "Next": "RegisterModel"}],
      "Default": "RejectModel"
    },
    "RegisterModel": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {"FunctionName": "register-model", "Payload.$": "$"},
      "End": true
    },
    "RejectModel": {"Type": "Succeed", "Comment": "ran fine, model not good enough"},
    "NotifyFailure": {"Type": "Fail", "Error": "TrainingFailed", "Cause": "see $.error"}
  }
}
```
```python
"""Offline structural check of an ASL file: every Next/Default/Catch target exists, no orphan states, a terminal state is reachable."""
import json, sys
sm = json.load(open(sys.argv[1])); S = sm["States"]; errs = []
def targets(name, s):
    t = []
    if "Next" in s: t.append(s["Next"])
    if "Default" in s: t.append(s["Default"])
    t += [c["Next"] for c in s.get("Choices", []) if "Next" in c]
    t += [c["Next"] for c in s.get("Catch", [])]
    return t
if sm["StartAt"] not in S: errs.append(f"StartAt {sm['StartAt']} missing")
for n, s in S.items():
    for t in targets(n, s):
        if t not in S: errs.append(f"{n} -> {t} does not exist")
    if s["Type"] in ("Task", "Pass", "Parallel", "Map", "Wait") and not ("Next" in s or s.get("End")):
        errs.append(f"{n} has neither Next nor End")
seen, stack = set(), [sm["StartAt"]]
while stack:
    n = stack.pop()
    if n in seen or n not in S: continue
    seen.add(n); stack += targets(n, S[n])
for n in S:
    if n not in seen: errs.append(f"{n} is unreachable")
terminal = [n for n in seen if S[n]["Type"] in ("Succeed", "Fail") or S[n].get("End")]
if not terminal: errs.append("no terminal state reachable")
print("states:", len(S), "| reachable:", len(seen), "| terminals:", sorted(terminal))
print("ERRORS:" if errs else "OK: all Next targets exist", *errs, sep="\n  " if errs else " ")
sys.exit(bool(errs))
```

**Output (my run):** `python3 -I q37_asl_check.py` on the file, then on a copy where I deliberately misspelled the Choice default as `RejectModell`:
```text
states: 6 | reachable: 6 | terminals: ['NotifyFailure', 'RegisterModel', 'RejectModel']
OK: all Next targets exist
states: 6 | reachable: 5 | terminals: ['NotifyFailure', 'RegisterModel']
ERRORS:
  GoodEnough -> RejectModell does not exist
  RejectModel is unreachable
```
Not executed: nothing was deployed or run on AWS. The script only checks the JSON structure and that every target state exists and is reachable. It does not validate the ASL schema fully, the ARNs, IAM permissions or JSONPath expressions. The ARNs and field names are written from memory of the docs; check current docs.

**Follow-ups:**
- *Why not poll in Lambda?* You pay for the wait and add a failure point; `.sync` lets the service wait.
- *Big data between states?* Pass S3 paths, not payloads.
- *EventBridge?* Often the trigger: a schedule or an event starts the state machine.

**Common mistakes:**
- No Default on a Choice.
- Using Catch to hide failures.
- Putting training logic inside Lambda (time limit).
- Choosing a tool by brand instead of by who will operate it.

### Q38 ⭐ 🔴 Data dependencies and pipeline-level data contracts: how a training DAG learns that an upstream table is complete (a success marker file, an asset event, a row-count check, a watermark), schema checks with pandera or Great Expectations at concept level, and stopping bad data from reaching training. Compare 'wait for upstream' versus 'check and fail'. Show a validation task that checks schema, null rate and row-count bounds on a small DataFrame and blocks the next step, and run it with airflow dags test or plain Python. Part 8 owns production data-quality monitoring.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** I check the data before training reads it: wait for a completeness signal from upstream, then run a validation task for schema, null rate and row count, and make it fail the run so the training task never starts.

**Then explain:**
- How a DAG learns an upstream table is complete: a success marker file (like `_SUCCESS`) written last; an asset or dataset event from the producer; a row-count check against an expected range; a watermark ("data is complete up to time T"). Marker or event is best, because it is explicit. Row counts alone cannot tell "complete" from "plausibly sized".
- Wait versus check-and-fail. Wait (a sensor, ideally in reschedule or deferrable mode so it does not hold a worker slot; check docs) when late data is normal. Check-and-fail when late or bad data is a bug you want to see. Use both: wait with a timeout, then check, then fail loudly.
- Schema checks: pandera or Great Expectations let you declare columns, types, ranges and nullability. I did not run either here. The plain-Python check below shows the idea.
- Stop bad data: the validation task raises, so downstream tasks do not run by default dependency rules. Failure mode: a gate that only logs a warning, a threshold so loose it never fires, or validating a different copy of the data than training reads.
- Scope: this is the pipeline-level gate. Continuous production data-quality and drift monitoring is a separate topic (Part 8).

**Example:** Rules: columns `user_id` int, `amount` float, `country` text; null rate at most 10% for `amount`; 5 to 1000 rows. A frame with 3 of 8 amounts missing has a 38% null rate and is blocked. A frame with `amount` stored as text is blocked. A frame with 3 rows is blocked.

**Code:** the pandas validator, and an Airflow DAG with a failing gate. (The DAG uses hard-coded stats to stay dependency free.)
```python
# ===== q38_validate.py =====
import pandas as pd

RULES = {"cols": {"user_id": "int", "amount": "float", "country": "text"},
         "max_null_rate": {"amount": 0.10, "country": 0.05},
         "min_rows": 5, "max_rows": 1000}

class DataContractError(Exception): pass

def kind(series):                     # pandas 3 shows text as 'str', older pandas as 'object'
    if pd.api.types.is_integer_dtype(series): return "int"
    if pd.api.types.is_float_dtype(series): return "float"
    if pd.api.types.is_string_dtype(series): return "text"
    return str(series.dtype)

def validate(df, rules=RULES):
    errs = []
    for c, dt in rules["cols"].items():
        if c not in df.columns: errs.append(f"missing column {c}")
        elif kind(df[c]) != dt: errs.append(f"{c} is {kind(df[c])}, expected {dt}")
    for c, mx in rules["max_null_rate"].items():
        if c in df.columns and df[c].isna().mean() > mx:
            errs.append(f"{c} null rate {df[c].isna().mean():.2f} > {mx}")
    if not rules["min_rows"] <= len(df) <= rules["max_rows"]:
        errs.append(f"row count {len(df)} outside [{rules['min_rows']}, {rules['max_rows']}]")
    if errs: raise DataContractError("; ".join(errs))
    return True

def train(df): return f"trained on {len(df)} rows"

def pipeline(df):
    validate(df)                      # raising here means train() never runs
    return train(df)

good = pd.DataFrame({"user_id": range(1, 9), "amount": [10.0, 5.5, 7, 3, 9, 4, 8, 2], "country": list("INUSINUS")})
nulls = good.assign(amount=[None, None, None, 3, 9, 4, 8, 2])
schema = good.assign(amount=good["amount"].astype(str))
small = good.head(3)
for name, df in [("good", good), ("many nulls", nulls), ("schema drift", schema), ("too few rows", small)]:
    try: print(f"{name:13s} -> {pipeline(df)}")
    except DataContractError as e: print(f"{name:13s} -> BLOCKED: {e}")

# ===== q38_dags/gate_dag.py =====
import pendulum
from airflow.sdk import dag, task

@dag(dag_id="gate", schedule=None, start_date=pendulum.datetime(2026, 1, 1), catchup=False,
     default_args={"retries": 0}, tags=["lab"])
def gate():
    @task
    def load():
        return {"rows": 3, "null_rate": 0.4}          # pretend this came from the upstream table
    @task
    def validate(stats: dict):
        if stats["rows"] < 5 or stats["null_rate"] > 0.1:
            raise ValueError(f"data contract broken: {stats}")
        return "ok"
    @task
    def train(flag: str):
        print("TRAINING STARTED")
    train(validate(load()))
gate()
```

**Output (my run):** plain Python with pandas 3.0.5, `python3 -I q38_validate.py`:
```text
good          -> trained on 8 rows
many nulls    -> BLOCKED: amount null rate 0.38 > 0.1
schema drift  -> BLOCKED: amount is text, expected float
too few rows  -> BLOCKED: row count 3 outside [5, 1000]
```
Then `airflow dags test gate 2026-10-01` with apache-airflow 3.3.2 (own temp AIRFLOW_HOME, no scheduler):
```text
airflow dags test gate: exit code 1
ValueError: data contract broken: {'rows': 3, 'null_rate': 0.4}
Marking run <DagRun gate  ... > failed
lines containing 'TRAINING STARTED': 0
```
A real finding while writing this: my first version compared dtype strings to `object`, and pandas 3 reports text columns as `str`, so every frame was blocked. The `kind()` helper fixes that. Pandera and Great Expectations were not installed or run (not executed).

**Follow-ups:**
- *Where do thresholds come from?* From history of the table, reviewed by the data owner; keep them in config, not in code.
- *Should a bad batch stop all pipelines?* Only the ones that read it. Quarantine the batch (Q31).
- *Contracts?* A written agreement with the producer on schema and freshness; validation is how you enforce it.

**Common mistakes:**
- Warn-only checks.
- Sensors in poke mode that hold a worker for hours.
- Checking row count only.
- Comparing dtype names without testing on the pandas version you deploy.

### Q39 ⭐ 🔴 Reproducible and cost-aware pipeline runs: pin the image and library versions, pass a run date and a data snapshot ID instead of 'latest', record git SHA and parameters with the run (Part 4 owns MLflow and DVC), ephemeral compute per run, scale to zero, skip unchanged steps with caching, and tag cost per pipeline. Show a run-manifest function that captures date, snapshot, git SHA, params and image digest into JSON, and a test that two runs with the same manifest pick identical inputs. Runs locally; cloud cost reports are not executed.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** A run should be a pure function of a manifest: run date, data snapshot id, git SHA, parameters and an image digest, all recorded and none of them "latest".

**Then explain:**
- Pin what moves: image by digest (a tag can be re-pushed), library versions in a lock file, data by snapshot id or version, code by git SHA. Refuse "latest" in code, as the function below does.
- Pass the run date as a parameter instead of calling `now()` inside the task. A rerun for 2026-10-01 next month must read the same partitions.
- Record the manifest with every run (as JSON next to the output, or as tags in the tracking tool). MLflow and DVC own the experiment and data versioning side (Part 4); here the point is that the orchestrator hands them the same manifest.
- Cost: ephemeral compute per run (create, run, delete), scale to zero when idle, cache or skip unchanged steps (KFP has step caching keyed on inputs and parameters; Airflow has no built-in result cache, so you implement "skip if output exists for this manifest id"), and tag each run with team and pipeline so a cloud cost report can group by tag.
- Failure modes: caching a step whose hidden input changed (a file read by path, not passed as input), and a manifest that omits a parameter that matters.

**Example:** Two runs with the same date, snapshot and parameters get the same `manifest_id` and the same three input paths. Changing only the snapshot from `snap-0042` to `snap-0043` changes both.

**Code:** a manifest builder and the determinism check (the demo makes a temporary git repo only to have a real SHA).
```python
import hashlib, json, os, subprocess, sys, tempfile

def git_sha(repo):
    return subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()

def make_manifest(run_date, snapshot_id, params, repo, image):
    if snapshot_id == "latest" or "@sha256:" not in image:
        raise ValueError("pin the snapshot id and use an image digest, not 'latest' or a moving tag")
    m = {"run_date": run_date, "snapshot_id": snapshot_id, "git_sha": git_sha(repo),
         "params": params, "image": image}
    m["manifest_id"] = hashlib.sha256(json.dumps(m, sort_keys=True).encode()).hexdigest()[:12]
    return m

def pick_inputs(m):
    """Deterministic: files depend only on the snapshot and the run date, never on 'now'."""
    return [f"s3://lake/{m['snapshot_id']}/dt={m['run_date']}/part-{i:02d}.parquet" for i in range(3)]

if __name__ == "__main__":
    repo = tempfile.mkdtemp()
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    subprocess.run(["git", "init", "-q", repo], check=True)
    subprocess.run(["git", "-C", repo, "commit", "-q", "--allow-empty", "-m", "c1"], check=True, env=env)
    img = "registry.example.com/ml/train@sha256:" + "ab" * 32
    a = make_manifest("2026-10-01", "snap-0042", {"lr": 0.1}, repo, img)
    b = make_manifest("2026-10-01", "snap-0042", {"lr": 0.1}, repo, img)
    c = make_manifest("2026-10-01", "snap-0043", {"lr": 0.1}, repo, img)
    print(json.dumps(a, indent=1))
    print("same manifest, same inputs:", pick_inputs(a) == pick_inputs(b), "| same id:", a["manifest_id"] == b["manifest_id"])
    print("new snapshot, different inputs:", pick_inputs(a) != pick_inputs(c), "| ids:", a["manifest_id"], c["manifest_id"])
    try: make_manifest("2026-10-01", "latest", {}, repo, img)
    except ValueError as e: print("rejected:", e)
    try: make_manifest("2026-10-01", "snap-0042", {}, repo, "registry.example.com/ml/train:latest")
    except ValueError as e: print("rejected:", e)
```

**Output (my run):** `python3 -I q39_manifest.py`, Python 3.13, git in a temp repo. The git SHA differs on every run because the commit has a timestamp, so the id changes between runs of this demo, but within one run it is consistent:
```text
{
 "run_date": "2026-10-01",
 "snapshot_id": "snap-0042",
 "git_sha": "55c44d849e893181416b055ac49f7e91b3c59cc2",
 "params": {
  "lr": 0.1
 },
 "image": "registry.example.com/ml/train@sha256:abababababababababababababababababababababababababababababababab",
 "manifest_id": "5585053da754"
}
same manifest, same inputs: True | same id: True
new snapshot, different inputs: True | ids: 5585053da754 de231616adc5
rejected: pin the snapshot id and use an image digest, not 'latest' or a moving tag
rejected: pin the snapshot id and use an image digest, not 'latest' or a moving tag
```
Not executed: any cloud cost report, tag-based cost allocation, KFP caching on a cluster, or ephemeral cluster creation.

**Follow-ups:**
- *Why a digest, not a tag?* Tags can move; a digest names exact bytes.
- *Two runs, different outputs, same manifest?* Then something is not pinned: a random seed, an unpinned library, a time call. Find it.
- *How do you cost a pipeline?* Tag compute with the pipeline name; check your cloud's cost allocation docs.

**Common mistakes:**
- `FROM python:latest` or `pip install` with no versions.
- Reading "yesterday" from the clock inside the job.
- Recording parameters but not the data snapshot.
- Caching steps that read mutable paths.

### Q40 ⭐ 🔴 Migration scenario: a team has 40 cron jobs and notebooks that retrain models. You move them to an orchestrator over three months. Cover inventory and dependency discovery, picking the tool, wrapping scripts first (lift and shift with BashOperator or a container) before refactoring, running old and new in parallel and comparing outputs, idempotency fixes, cutover and rollback, and what to measure (failure rate, time to recover, on-time rate). Give a migration plan table and a script that compares the outputs of old and new runs and flags diffs. The comparison runs locally; nothing else is executed.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** Inventory first, wrap the existing scripts as they are, run old and new side by side and compare outputs, fix idempotency, then cut over one job at a time with a rollback ready.

**Then explain:**
- Inventory and dependencies: list all 40 jobs with schedule, owner, inputs, outputs, runtime, and who is hurt if it fails. Find hidden dependencies (one job reads another's file, jobs that must run in order by "start at 2am, the other at 3am"). Failure mode: undocumented notebook cells run by hand.
- Pick the tool by team skills and needs (Airflow for breadth and hiring pool, Prefect for light Python-first flows, Kubeflow if you are already on Kubernetes); do not decide on features alone.
- Lift and shift first: a BashOperator or a container task that calls the old script, with retries and alerts. You gain scheduling, history and dependencies in week one. Refactor later, one job at a time.
- Parallel run: old cron and new orchestrated job both run, the new one writes to a shadow location. A comparison script checks the outputs. Failure mode: comparing files byte for byte when they contain timestamps; ignore known-volatile columns and use a numeric tolerance.
- Idempotency fixes: jobs that append on every run, write to fixed paths, or use "today" from the clock need an overwrite-by-partition design and a run date parameter, or a rerun will double count.
- Cutover and rollback: switch consumers to the new output, keep cron disabled but not deleted for a period, and keep the switch reversible (an alias or a config flag).
- Measure: failure rate, time to recover, on-time rate (finished before the consumer needs it), plus manual interventions per month. Compare before and after.

**Example (plan table):**

| Weeks | Step | Exit check |
|---|---|---|
| 1-2 | Inventory 40 jobs, rank by risk and value, draw dependencies | every job has owner and inputs/outputs |
| 3-4 | Pick tool, platform skeleton, linter, alerts | one pilot job wrapped and running |
| 5-8 | Lift and shift in batches of about 8, run parallel | comparison diff clean for N consecutive runs |
| 9-10 | Idempotency fixes, run-date parameters | rerun of any day gives identical output |
| 11-12 | Cutover in order of risk, rollback drill | cron disabled, rollback tested once |
| after | Refactor, retire duplicates, review metrics | failure rate and recovery time better than baseline |

**Code:** a comparison of two output folders. It flags missing and extra files, row count and key differences, and value differences beyond a tolerance, and ignores a `generated_at` column.
```python
"""Compare output folders of the old cron job and the new orchestrated job. Flags: missing/extra files, row-count and key diffs, value diffs beyond tolerance."""
import csv, os, sys, tempfile

IGNORE = {"generated_at"}            # columns that legitimately differ between runs
TOL = 1e-6

def load(path, key):
    with open(path, newline="") as f:
        return {r[key]: {k: v for k, v in r.items() if k not in IGNORE} for r in csv.DictReader(f)}

def same(a, b):
    try: return abs(float(a) - float(b)) <= TOL
    except ValueError: return a == b

def compare_dirs(old, new, key="id"):
    findings = []
    fo, fn = set(os.listdir(old)), set(os.listdir(new))
    findings += [f"MISSING in new: {f}" for f in sorted(fo - fn)] + [f"EXTRA in new: {f}" for f in sorted(fn - fo)]
    for f in sorted(fo & fn):
        o, n = load(os.path.join(old, f), key), load(os.path.join(new, f), key)
        if len(o) != len(n): findings.append(f"{f}: row count old={len(o)} new={len(n)}")
        for k in sorted(set(o) - set(n)): findings.append(f"{f}: key {k} only in old")
        for k in sorted(set(n) - set(o)): findings.append(f"{f}: key {k} only in new")
        for k in sorted(set(o) & set(n)):
            for col, v in o[k].items():
                if not same(v, n[k].get(col, "<absent>")):
                    findings.append(f"{f}: key {k} col {col} old={v} new={n[k].get(col)}")
    return findings

def write(d, name, header, rows):
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, name), "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        res = compare_dirs(sys.argv[1], sys.argv[2])
    else:                                         # demo data
        t = tempfile.mkdtemp(); o, n = os.path.join(t, "old"), os.path.join(t, "new")
        h = ["id", "score", "generated_at"]
        write(o, "scores.csv", h, [(1, 0.50, "09:00"), (2, 0.70, "09:00"), (3, 0.90, "09:00")])
        write(n, "scores.csv", h, [(3, 0.90, "09:05"), (1, 0.5000000001, "09:05"), (2, 0.71, "09:05"), (4, 0.1, "09:05")])
        write(o, "churn.csv", ["id", "p"], [(1, 0.2)]); write(n, "extra.csv", ["id", "p"], [(1, 0.2)])
        res = compare_dirs(o, n)
    print("\n".join(res) if res else "IDENTICAL within tolerance")
    print(f"diffs: {len(res)}")
    sys.exit(1 if res else 0)
```

**Output (my run):** `python3 -I q40_compare.py` (built-in demo data: the new run has an extra row, a changed score `0.70` vs `0.71`, a missing file and an extra file; a score off by 1e-10 is correctly not flagged):
```text
MISSING in new: churn.csv
EXTRA in new: extra.csv
scores.csv: row count old=3 new=4
scores.csv: key 4 only in new
scores.csv: key 2 col score old=0.7 new=0.71
diffs: 5
```
Nothing else was executed: no cron, no orchestrator, no real jobs. The three-month plan is a reasonable template, not a measured schedule; adjust to your team.

**Follow-ups:**
- *What if outputs never match exactly?* Decide per column: exact, tolerance, or ignored. Get the consumer to sign off.
- *Do you migrate everything?* No. Retire jobs nobody reads; the inventory often finds some.
- *What if the new system fails at cutover?* Re-enable cron for that job and fix forward.

**Common mistakes:**
- Rewriting every job before getting any into the orchestrator.
- Cutting over without a parallel run.
- Deleting the cron entry on day one.
- Measuring success by "jobs migrated" rather than by failures and recovery time.

