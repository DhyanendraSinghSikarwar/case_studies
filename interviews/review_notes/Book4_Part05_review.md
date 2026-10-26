# Book 4 Part 5 review (Wave C)

Date: 2026-10-26. Reviewer: lead session (independent of the four answer agents). Scope: 40 questions, Q1-Q40 (pipelines and orchestration: Airflow, Kubeflow Pipelines, Prefect, comparisons). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-10, Q11-20, Q21-30, Q31-40; merged by heading: 40 of 40 merged, 0 skipped, 0 pending. No spend-limit stops. Each agent used its own AIRFLOW_HOME / PREFECT_HOME so no SQLite state was shared.

## Structure checks (scripted by the lead)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q40; star order and counts 15 / 17 / 8 | pass |
| All 7 template labels present and in order; code fences balanced | pass for all 40 |

The lead did not re-run the DAG, flow and compile demos: they need per-question Airflow/Prefect homes and venvs; the pasted outputs come from each agent's real runs (drivers `run.sh`/`output.txt` are in each agent's `code/` folder). Outputs with timestamps, temp paths or timings differ on a re-run.

## What really ran (Airflow 3.3.2, Prefect 3.9.0, kfp 2.17.3, Dagster 1.13.26, Python 3.13)
DagBag parsing and `airflow dags test` on SQLite (TaskFlow and classic DAGs, branching with --conf, retries and callbacks, mapped tasks, sensors, asset producer/consumer DAGs, Param validation, a virtualenv task), `airflow backfill create`, `airflow pools`, `airflow config get-value`, a pytest DAG-test suite, an AST DAG linter, ruff AIR3 rules; local Prefect flows with retries, caching, `.submit`, hooks and a local server with `flow.serve` and a cron deployment; kfp compiles (lightweight, container and YAML components, ParallelFor, If, ExitHandler, resources, caching options, Vertex-style); two Dagster assets materialised locally; Argo, Step Functions and Kubernetes manifests checked with pyyaml/kubernetes-validate and small Python checkers; a pure-Python resumable pipeline runner.

## Findings kept in the text (observed in 3.3.2 unless stated)
- A plain cron string became CronTriggerTimetable; `catchup_by_default` is False; a manual run has data_interval_start = end = logical_date. "The run starts after the interval ends" holds only for the interval timetable.
- A DAG run stays "success" when the only leaf is an `all_done` cleanup task, even if an upstream failed; `on_failure_callback` fires only after the final try.
- `airflow dags backfill` is removed; `airflow backfill create` needs the DAG serialized (`dags reserialize`) and leaves runs queued without a scheduler.
- Airflow 2 patterns fail to parse (`airflow.datasets`, `schedule_interval`); ruff AIR3 said Dataset "still works" while 3.3.2 had removed the module.
- Under `dags test` secrets were not masked in logs or prints, even after `mask_secret`; the masker works when called directly; real worker masking was not run and is hedged. `airflow connections get` prints the password in clear. (All demo credentials are fake.)
- Every kfp lightweight component pip-installs kfp even without packages_to_install; a missing type annotation raises TypeError at once; `.fn` on a Prefect flow raises MissingContextError.
- DeadlineAlert refused a non-async callback target at parse time.
- DagBag timing figures (Q34) are single-run numbers on this machine, labelled so.

## Not executed
Scheduler-driven runs, API server, triggerer, workers, executors other than LocalExecutor, Celery/Kubernetes executors, KubernetesPodOperator pods, any KFP cluster or submission, Prefect work pools and workers, Dagster daemon/webserver, Argo, Step Functions, Vertex, SageMaker, MWAA, secret backends, real alert channels, XCom size limit (no number given). Airflow 3 release-note items (API server, DAG versioning, scheduler-run backfills, SLA removal) are "from release notes, not run, check current docs".

## Evidence limits
No candidate-reported questions found; every WebFetch failed, so sources are snippet-only guides and job postings. Argo, Vertex, Dagster and Airflow 3 questions are expert extensions. See research_notes/Book4_Part05_sources.md. One Q35 sentence about Airflow multi-team support is vague and was left hedged.
