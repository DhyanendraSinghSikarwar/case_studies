@@Q21
**Say this first (1 line):** Airflow 3 moves DAG authoring to `airflow.sdk`, puts an API server in front, renames datasets to assets and drops `execution_date` and `schedule_interval`, so I migrate a fleet by linting with ruff, fixing imports, parsing every DAG with DagBag in CI, then upgrading a canary first.

**Then explain:**
- What I verified by running Airflow 3.3.2 here: `schedule_interval` is gone (TypeError at parse), `execution_date` is not in the task context but `logical_date` is, `airflow.datasets` does not exist any more, and `from airflow.operators.python import PythonOperator` still imports but warns that it moved to the standard provider.
- What I know from release notes but did NOT run here (check current docs): the API server replaces the old web server; tasks talk to the API server through the Task SDK instead of opening the metadata DB directly (so a task that queries the Airflow DB breaks); DAG versioning; backfills are run by the scheduler; SLAs and SubDAGs are removed. For ML teams the two that bite are the direct-DB access and the removed SLAs.
- Migration plan for many DAGs: (1) inventory and owners, (2) `ruff check --preview --select AIR3` on the repo and apply the safe fixes, (3) a CI job that loads every file with DagBag on Airflow 3 and fails on any `import_errors`, (4) install the standard provider and any provider the DAGs need, (5) canary environment with a copy of the metadata DB backup, compare run counts and task states for a week, (6) cut over with a rollback plan.
- Failure mode: a DAG that fails to import does not crash anything. It just disappears from the UI. So alert on the import-error count.
- Trust the DagBag test over the linter. Here ruff said `airflow.datasets.Dataset` "still works", but on 3.3.2 the module was already gone. Linter notes are written against one release, your install may be newer.

**Example:** `old_dag.py` below has three problems that a reader can count: the `Dataset` import (line 5), `schedule_interval` (line 12) and `execution_date` used in the callable. On 3.3.2 the first one stops the parse. `old2_dag.py` has no Dataset import, so the next one shows up: `schedule_interval`. `old3_dag.py` (only in the code folder) uses `schedule=` and `PythonOperator` and does parse, with a deprecation warning, and its context has `logical_date` but no `execution_date`. The new style file parses clean.

**Code:** the driver `code/q21/run.sh` builds its own AIRFLOW_HOME in a temp dir. Python block: the old DAGs, the new DAG and the parse script. Bash block: the commands.
{{CODE python q21/old_dag.py q21/old2_dag.py q21/new_dag.py q21/parse.py}}

```bash
export AIRFLOW_HOME=/tmp/some_own_dir AIRFLOW__CORE__LOAD_EXAMPLES=False   # never share this with another run
airflow db migrate
python -I parse.py ./old            # DagBag(dag_folder=...) -> import_errors
AIRFLOW__CORE__DAGS_FOLDER=./new airflow dags test new_train 2026-10-01
ruff check --preview --select AIR3 --output-format concise ./old   # migration lint (ruff 0.16.9)
```

**Output (my run):** Airflow 3.3.2, Python 3.13, SQLite, no scheduler or API server started (only `dags test`). Log lines were filtered with grep/sed.
{{OUT q21/output.txt}}

**Follow-ups:**
1. *Why is it called logical_date?* It is the point on the timeline the run is about, not the wall-clock time it ran. In `dags test` the data interval start and end both equalled the date I passed (seen in the log), so do not assume a neat interval for manual runs; check current docs.
2. *Can old and new run together?* Run two separate deployments, one per major version, and move DAGs across in batches. I did not test a mixed fleet.
3. *What about custom operators?* Same lint and parse test, plus a real task run in the canary, because import errors are only half of it.

**Common mistakes:** Upgrading everything in one go. Trusting the linter and skipping the parse test. Leaving `from airflow.models import ...` DB queries inside tasks. Forgetting the standard provider. Not alerting on import errors.

@@Q22
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
{{CODE python q22/ml_dags.py q22/check.py}}

```bash
export AIRFLOW_HOME=/tmp/own_dir AIRFLOW__CORE__LOAD_EXAMPLES=False AIRFLOW__CORE__DAGS_FOLDER=/tmp/own_dir/dags
airflow db migrate
python -I check.py /tmp/own_dir/dags                 # DagBag parse, print schedules
airflow dags test build_features 2026-10-01          # producer only; consumer needs a running scheduler
```

**Output (my run):** Airflow 3.3.2. Scheduler, triggerer and API server were not started.
{{OUT q22/output.txt}}

**Follow-ups:**
1. *Asset versus sensor?* An asset needs the producer to be in Airflow (or to call the API); a sensor can watch anything, but it polls and costs a slot or a triggerer.
2. *What if the producer reruns?* It emits another event and the consumer runs again, so the consumer must be idempotent (same output path per input version).
3. *Backfill with assets?* Not tested; check current docs.

**Common mistakes:** Emitting the event before the data is complete. Forgetting that the consumer has no calendar interval (do not use `data_interval_start` as the data date; pass the date in the asset event extra or read it from the data). Using a sensor in poke mode that holds a worker for hours. Creating two assets with slightly different URIs.

@@Q23
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
{{CODE python q23/checks.py q23/health_dag.py}}

```bash
python3 -I checks.py                                  # pure checks, no Airflow
AIRFLOW__CORE__DAGS_FOLDER=./dags airflow dags test health_demo 2026-10-01   # failing check task + callback
```

**Output (my run):** Airflow 3.3.2, `dags test` only (no scheduler, so no deadline fired). The `check` task is meant to fail.
{{OUT q23/output.txt}}

**Follow-ups:**
1. *Alert on every failure?* No: after retries, and group by DAG, or people mute the channel.
2. *Late versus slow?* Late is against a clock (deadline from queued time), slow is against history (runtime much above the usual); I use both.
3. *Who watches the watcher?* The outside probe; keep it simple and on different infrastructure.

**Common mistakes:** Alerting only inside Airflow. Alert storms from per-try callbacks. A success status with an empty output table. Callback code that needs a connection that is itself broken. Treating an SLA example from an Airflow 2 blog as valid on 3.

@@Q24
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
{{CODE python q24/train_flow.py q24/serve_it.py q24/check_yaml.py}}

{{CODE yaml q24/prefect.yaml}}

```bash
export PREFECT_HOME=/tmp/own_dir PREFECT_API_URL=http://127.0.0.1:4299/api PREFECT_SERVER_ANALYTICS_ENABLED=false
prefect server start --port 4299 &          # local server
python serve_it.py &                        # registers train/nightly and polls
prefect deployment run train/nightly --param rows=7 --param dry_run=true
prefect deployment inspect train/nightly
```

**Output (my run):** Prefect 3.9.0. Part 1 used the in-process temporary API; part 2 used a real local server and a served deployment; part 3 parsed the `prefect.yaml` sketch only (nothing was deployed). Both processes were stopped at the end.
{{OUT q24/output.txt}}

**Follow-ups:**
1. *serve or deploy?* serve for one machine or a simple team box; deploy with a work pool when you want isolation, images and autoscaled infrastructure.
2. *Where do secrets go?* Prefect blocks or variables, or the environment of the worker; not in `prefect.yaml`.
3. *Does Prefect backfill?* Not tested here; check current docs.

**Common mistakes:** Running `serve` in a terminal and closing it. Assuming a Prefect run sees your laptop's code when a worker runs it elsewhere. Putting secrets in parameters (they are visible in the UI). Forgetting the timezone on a cron.
