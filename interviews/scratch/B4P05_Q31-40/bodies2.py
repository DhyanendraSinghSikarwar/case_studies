B = {}
B[36] = r'''**Say this first (1 line):** In Dagster you declare the data things you want to exist (assets, such as a table or a model) and what each depends on, and the tool works out the graph; Airflow asks you to declare the steps. For ML this gives lineage and "what is stale" almost for free.

**Then explain:**
- Software-defined asset: a Python function that produces one named thing, like `training_table` or `churn_model`. Its function arguments name its upstream assets, so the dependency graph and lineage come from the code.
- Jobs select which assets to run. Schedules run them on time. Sensors run them when something happens (a new file, an upstream event). Partitions slice an asset by date or other key, which gives backfills per partition and per-partition status.
- IO managers decide where an asset's value is stored and loaded (local pickle, file, warehouse, object store). The asset code stays free of storage code.
- A model as an asset: `churn_model` depends on `training_table`. When the table is rematerialised, the model shows as stale, and you can see which data version produced which model.
- Versus Airflow: Airflow is task-centric (run this, then that). It has a larger ecosystem, more people who know it and more hiring demand. Dagster has a smaller ecosystem and a new mental model (assets, definitions, resources), so a team used to Airflow needs time. Newer Airflow also has asset-style features; check current docs before saying one lacks something.
- Failure modes: forgetting that an asset's value is persisted by the IO manager (large values need a real store, not the default pickle); partition definitions that do not match the upstream's.

**Example:** Two assets: `training_table` yields 5 rows of `y = 2x`; `churn_model` fits `w` by least squares through the origin. Hand check: sum(x*y) = 2*(0+1+4+9+16) = 60 and sum(x^2) = 30, so w = 2.0.

**Code:**
@@code:python:q36_assets.py@@

**Output (my run):** dagster 1.13.26 installed with pip in a fresh venv, Python 3.13, `DAGSTER_HOME` set to a temp folder; `materialize()` runs in-process. The framework's own debug log lines are dropped here; these are the lines my script printed:
@@out:q36_out.txt@@
Not executed: the Dagster webserver and UI, daemon (schedules and sensors), partitions and Dagster Cloud. Schedules, sensors, partitions and IO managers above are described from general knowledge; check the current Dagster docs for exact APIs, which have changed between versions.

**Follow-ups:**
- *When would you pick Dagster?* A data and ML team that cares about lineage, partitions and asset freshness, and has no big Airflow investment.
- *When stay on Airflow?* Existing DAGs, many provider integrations, hiring pool.
- *Is it either/or?* No. Some teams run both and trigger one from the other; that adds ops cost.

**Common mistakes:**
- Calling assets "just DAGs with new names". The unit of design is the data, not the step.
- Keeping huge values in the default IO manager.
- Claiming Dagster is better without naming the migration cost.
'''

B[37] = r'''**Say this first (1 line):** For an AWS-only team, Step Functions is a good glue layer for service-to-service flows with Lambda and SageMaker jobs, SageMaker Pipelines is built for the ML DAG itself, and Airflow (MWAA) wins when you already have Airflow skills or many non-AWS systems. Check current docs for features and limits.

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
@@code:json:q37_ml_state_machine.json@@
@@code:python:q37_asl_check.py@@

**Output (my run):** `python3 -I q37_asl_check.py` on the file, then on a copy where I deliberately misspelled the Choice default as `RejectModell`:
@@out:q37_out.txt@@
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
'''

B[38] = r'''**Say this first (1 line):** I check the data before training reads it: wait for a completeness signal from upstream, then run a validation task for schema, null rate and row count, and make it fail the run so the training task never starts.

**Then explain:**
- How a DAG learns an upstream table is complete: a success marker file (like `_SUCCESS`) written last; an asset or dataset event from the producer; a row-count check against an expected range; a watermark ("data is complete up to time T"). Marker or event is best, because it is explicit. Row counts alone cannot tell "complete" from "plausibly sized".
- Wait versus check-and-fail. Wait (a sensor, ideally in reschedule or deferrable mode so it does not hold a worker slot; check docs) when late data is normal. Check-and-fail when late or bad data is a bug you want to see. Use both: wait with a timeout, then check, then fail loudly.
- Schema checks: pandera or Great Expectations let you declare columns, types, ranges and nullability. I did not run either here. The plain-Python check below shows the idea.
- Stop bad data: the validation task raises, so downstream tasks do not run by default dependency rules. Failure mode: a gate that only logs a warning, a threshold so loose it never fires, or validating a different copy of the data than training reads.
- Scope: this is the pipeline-level gate. Continuous production data-quality and drift monitoring is a separate topic (Part 8).

**Example:** Rules: columns `user_id` int, `amount` float, `country` text; null rate at most 10% for `amount`; 5 to 1000 rows. A frame with 3 of 8 amounts missing has a 38% null rate and is blocked. A frame with `amount` stored as text is blocked. A frame with 3 rows is blocked.

**Code:** the pandas validator, and an Airflow DAG with a failing gate. (The DAG uses hard-coded stats to stay dependency free.)
@@code:python:q38_validate.py,q38_dags/gate_dag.py@@

**Output (my run):** plain Python with pandas 3.0.5, `python3 -I q38_validate.py`:
@@out:q38_out.txt@@
Then `airflow dags test gate 2026-10-01` with apache-airflow 3.3.2 (own temp AIRFLOW_HOME, no scheduler):
@@out:q38_af_out.txt@@
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
'''

B[39] = r'''**Say this first (1 line):** A run should be a pure function of a manifest: run date, data snapshot id, git SHA, parameters and an image digest, all recorded and none of them "latest".

**Then explain:**
- Pin what moves: image by digest (a tag can be re-pushed), library versions in a lock file, data by snapshot id or version, code by git SHA. Refuse "latest" in code, as the function below does.
- Pass the run date as a parameter instead of calling `now()` inside the task. A rerun for 2026-10-01 next month must read the same partitions.
- Record the manifest with every run (as JSON next to the output, or as tags in the tracking tool). MLflow and DVC own the experiment and data versioning side (Part 4); here the point is that the orchestrator hands them the same manifest.
- Cost: ephemeral compute per run (create, run, delete), scale to zero when idle, cache or skip unchanged steps (KFP has step caching keyed on inputs and parameters; Airflow has no built-in result cache, so you implement "skip if output exists for this manifest id"), and tag each run with team and pipeline so a cloud cost report can group by tag.
- Failure modes: caching a step whose hidden input changed (a file read by path, not passed as input), and a manifest that omits a parameter that matters.

**Example:** Two runs with the same date, snapshot and parameters get the same `manifest_id` and the same three input paths. Changing only the snapshot from `snap-0042` to `snap-0043` changes both.

**Code:** a manifest builder and the determinism check (the demo makes a temporary git repo only to have a real SHA).
@@code:python:q39_manifest.py@@

**Output (my run):** `python3 -I q39_manifest.py`, Python 3.13, git in a temp repo. The git SHA differs on every run because the commit has a timestamp, so the id changes between runs of this demo, but within one run it is consistent:
@@out:q39_out.txt@@
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
'''

B[40] = r'''**Say this first (1 line):** Inventory first, wrap the existing scripts as they are, run old and new side by side and compare outputs, fix idempotency, then cut over one job at a time with a rollback ready.

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
@@code:python:q40_compare.py@@

**Output (my run):** `python3 -I q40_compare.py` (built-in demo data: the new run has an extra row, a changed score `0.70` vs `0.71`, a missing file and an extra file; a score off by 1e-10 is correctly not flagged):
@@out:q40_out.txt@@
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
'''
