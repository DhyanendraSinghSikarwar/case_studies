B = {}
B[31] = r'''**Say this first (1 line):** Make every stage safe to rerun: checkpoint inside long steps, gate on validation and evaluation before anything touches production, publish with one atomic rename, and guard against duplicate runs with a lock.

**Then explain:**
- Crash in the middle of training (spot loss, OOM): write a checkpoint after each epoch to durable storage and resume from it on rerun. Failure mode: a checkpoint written half-way. Write to a temp file, then `os.replace`.
- Poisoned or late upstream data: a validation gate runs before training and fails fast. Bad input goes to a dead-letter folder with the reason, so someone can look at it. For a late partition, wait with a timeout, then fail with a clear message. Do not train on yesterday's data silently.
- Model trains but is worse: an evaluation gate compares to a threshold or to the current production model. If it fails, the run ends "gate failed", production is untouched, and that is not a pager event by itself.
- Atomic publish: write the model to a staging path, then promote with one rename (or one registry alias change). Readers see the old model or the new one, never a half-written one.
- Duplicate runs (a retry plus a manual trigger): use a lock keyed on the run id, or an idempotent run id, so the second run skips. Failure mode: a hard kill leaves a stale lock, so add a lock timeout or owner check.
- Circuit breaker: after N consecutive failures, stop auto-retrying and page a human. Runbook for on-call: where the logs are, which stage failed, is it safe to rerun (yes, because stages are idempotent), who owns the upstream table, how to roll back (point the alias at the previous model).

**Example:** A 4-epoch training crashes after epoch 2. Rerun starts at "epoch 2" and finishes epochs 3 and 4 only. A table with a label value of 7 never reaches training and lands in `dead_letter/`. A model scoring 0.9 against a 0.95 gate is not published, and `prod_model.json` still names run `r1`.

**Code:** the runner below uses fake scores on purpose, so you can hand-check the flow.
@@code:python:q31_runner.py@@

**Output (my run):** `python3 -I q31_runner.py`, Python 3.13, temp directory, real output:
@@out:q31_out.txt@@
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
'''

B[32] = r'''**Say this first (1 line):** Postings pair Airflow or Kubeflow with Python, Docker, Kubernetes, MLflow and a cloud, so I build a small public lab that proves each of those: an Airflow DAG tested locally, a Prefect flow with retries, a kfp pipeline compiled to YAML, and a README with a diagram.

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
@@code:python:q32_lab/dags/ml_train.py,q32_lab/pf_flow.py,q32_lab/kfp_pipe.py@@
@@code:bash:q32_lab/run_lab.sh@@

**Output (my run):** `run_lab.sh` with apache-airflow 3.3.2, prefect 3.9.0, kfp 2.17.3, each with its own temp home. The Airflow log is verbose, so the script filters it. Real output:
@@out:q32_out.txt@@
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
'''

B[33] = r'''**Say this first (1 line):** For about 30 pipelines I would start with one shared Airflow deployment run by a platform team, one repo with CODEOWNERS per team folder, per-task containers for heavy code, and a linter in CI that rejects DAGs without owner, tags and retries.

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
@@code:python:q33_dag_lint.py@@

**Output (my run):** `python3 -I q33_dag_lint.py q33_dags` on three sample files (`good_dag.py`, `bad_dag.py` with a top-level `requests.get`, `bad2_dag.py` with a top-level `boto3.client`), real output:
@@out:q33_out.txt@@
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
'''

B[34] = r'''**Say this first (1 line):** The scheduler (with the DAG processor) loops: parse DAG files, create runs that are due, queue ready task instances, and heartbeat; most slowness I have seen comes from heavy top-level code, too many files and a busy database, so I measure parse time first.

**Then explain:**
- Concept loop: (1) the DAG processor parses files and stores the DAG structure in the metadata DB (in Airflow 3 it is a separate component; check docs for your version); (2) the scheduler creates DAG runs whose time has come; (3) it finds task instances whose dependencies are met and hands them to the executor; (4) it records heartbeats and state changes, and cleans up tasks that died.
- What slows it: top-level code that imports big libraries or calls a network or database (runs on every parse); thousands of tiny DAG files each paying a fixed cost; DB load from many task state updates; very frequent re-parsing.
- Multiple schedulers: you can run more than one against the same database. They coordinate with row-level locks in the DB (`SELECT ... FOR UPDATE SKIP LOCKED` style), so the DB must support it (PostgreSQL or MySQL 8, not SQLite). More schedulers add throughput and availability but also DB load.
- Knobs I would look up, not trust from memory: in the installed 3.3.2 default config, `min_file_process_interval`, `parsing_processes` and `dag_file_processor_timeout` appear under `[dag_processor]`, and `use_row_level_locking` and `max_dagruns_to_create_per_loop` under `[scheduler]`. Older docs put several of these under `[scheduler]`; check current docs for your version.
- Measure before tuning: time how long the parse takes per file. Put heavy imports inside the task function.

**Example:** 500 files at 2 ms each parse in about a second here. Ten files that each sleep 0.2 s at import time cost two seconds. Ten slow files cost twice as much as 500 light ones, so file count is not the whole story.

**Code:** run with the Airflow venv's Python; it generates the DAG files in temp folders, then times `DagBag`.
@@code:python:q34_parse_time.py@@

**Output (my run):** apache-airflow 3.3.2, Python 3.13, this sandbox, one in-process run after a one-file warm-up (so the Airflow import cost is excluded):
@@out:q34_out.txt@@
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
'''

B[35] = r'''**Say this first (1 line):** Keep Airflow's image small and run each ML step in its own container, with KubernetesPodOperator for real isolation and GPUs, and `@task.virtualenv` or `@task.docker` for lighter cases.

**Then explain:**
- Why not put torch in the Airflow image: huge image, slow upgrades, and dependency conflicts between teams and with Airflow's own pins. A task image per project avoids all three.
- KubernetesPodOperator (from the cncf.kubernetes provider): launches a pod per task. You set the image, command, resources, node selector, tolerations, env and secrets. GPUs are requested as a resource limit (for example `nvidia.com/gpu`) and the cluster needs the GPU device plugin; check your cluster docs.
- Secrets: reference a Kubernetes Secret (env or volume) so the value never appears in the DAG or the log. Logs: with `get_logs=True` the operator streams the container's stdout into the task log. XCom: with `do_xcom_push=True` the operator adds a sidecar and reads `/airflow/xcom/return.json` after the main container ends; keep the value small. Check current provider docs for the exact behaviour.
- Pod template: a YAML base pod (service account, node pool, volumes) that tasks start from, so the platform sets defaults once.
- `@task.virtualenv` builds a venv per run (slow install, but no container). `@task.docker` needs a Docker daemon on the worker and the docker provider (not installed here). External Python points at a prebuilt interpreter.
- Cold start trade-off: a pod per task pays image pull and scheduling time (seconds to minutes with big images); warm Celery workers start fast but share dependencies. Failure modes: pod stuck Pending (no GPU node), image pull errors, OOMKilled, and orphan pods if the worker dies.

**Example:** The DAG below asks for 4 CPUs, 16Gi and one GPU, tolerates the GPU node taint and mounts a DB password from the Secret `ml-db`. The YAML is the pod template that gives these defaults to every task.

**Code:** the DAG (python) and the pod template (yaml), then the check script.
@@code:python:q35_dags/train_gpu.py,q35_check.py@@
@@code:yaml:q35_pod_template.yaml@@

**Output (my run):** the provider (apache-airflow-providers-cncf-kubernetes 10.25.0) is NOT in the shared Airflow venv. I unpacked it with `pip install --target` (no deps) plus the `kubernetes` client libraries into a separate folder, and added that folder to `sys.path` in the script. Real output:
@@out:q35_out.txt@@
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
'''
