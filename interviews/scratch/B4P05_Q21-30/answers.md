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
