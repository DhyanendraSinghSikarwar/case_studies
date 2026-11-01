@@Q25
**Say this first (1 line):** In Prefect I give the flow typed parameters, fan out training with `.submit()` on a thread-pool task runner, put retries on the flaky fetch, cache the data task with a `cache_key_fn` and an expiry, and fail fast on a bad parameter before any work starts.

**Then explain:**
- Parameters: type hints are validated, and my own guard (`lr <= 0` raises) stops the flow before the fetch. Cheap failures first.
- Concurrency: `ThreadPoolTaskRunner(max_workers=3)` plus `task.submit(...)` returns futures; `.result()` waits. Threads suit I/O and libraries that release the GIL. For heavy CPU or GPU training, use separate processes or infrastructure per run (check docs for a process-based runner or Dask/Ray integrations).
- Retries: `retries=2, retry_delay_seconds=...` re-runs only the task. In my run the first fetch raised `ConnectionError`, Prefect logged "Retry 1/2", and the second try passed. Retry only what is safe to repeat (idempotent).
- Caching: `cache_key_fn` returns a string; same key inside `cache_expiration` means the task is skipped and the stored result is reused (state `Cached`). With `persist_result=True` the result is stored on disk under the Prefect home, so it also works across flow runs. The key here is the day, so a new day is a miss. Failure mode: a key that ignores something that matters (for example the query version) serves stale data.
- Failure hooks: `on_failure=[fn]` on the flow gets `(flow, flow_run, state)`. It ran once, after the bad-parameter failure. Notifications to Slack, email or Cloud automations are not executed here.
- Result storage defaults and cleanup differ between versions; check current docs before relying on them in production.

**Example:** Fetch returns `[1, 2, 3, 4]`, mean 2.5. Score = mean x lr, doubled for `gbm`: logreg 2.5 x 0.5 = 1.25, gbm = 2.5, mlp = 1.25. Best is gbm, score 2.5, as in the output. Call 1 fetches (one failure plus one retry, so the body ran twice). Call 2, same day, hits the cache (body not run). Call 3, a new day, runs the body again: 3 body executions in total. Call 4 with `lr=0` fails before any task.

**Code:** one file; the driver `code/q25/run.sh` runs it with its own `PREFECT_HOME`.
{{CODE python q25/ml_flow.py}}

**Output (my run):** Prefect 3.9.0 with the in-process temporary server. Lines were filtered (the `train` task lines, "Beginning" lines, the stack trace and the telemetry 403 noise from the sandbox proxy were removed).
{{OUT q25/output.txt}}

**Follow-ups:**
1. *submit versus map?* `map` fans one task over an iterable; `submit` is for different calls, like three models. Not tested: `map` here.
2. *Does cache survive a restart?* Only if the result is persisted and the storage is still there.
3. *What if one training task fails?* `.result()` raises in the flow; use `return_state=True` or `wait_for` if you want the others to finish and decide yourself (not tested).

**Common mistakes:** Caching on a key that leaves out the data version. Retrying a non-idempotent step. Threads for CPU-bound training. Putting the guard after the expensive fetch. Assuming hooks run for task failures when I wrote a flow hook.

@@Q26
**Say this first (1 line):** In KFP v2 I write the control flow with `dsl.ParallelFor`, `dsl.Collected`, `dsl.If` and `dsl.ExitHandler`, set resources and scheduling per task, and compile to YAML where each of those shows up as a sub-DAG component and a policy field.

**Then explain:**
- `ParallelFor(items=lrs, parallelism=2)` runs the body once per item; in the YAML it is a `parameterIterator` plus an `iteratorPolicy: parallelismLimit: 2`. `dsl.Collected(t.output)` gathers all outputs of the loop into a list for a later task (`pick_best`). Without `Collected`, the task after the loop cannot see the per-item results.
- `dsl.If(best.output >= min_score)` (older name `dsl.Condition`) becomes a `condition-3` component with a `triggerPolicy.condition` expression. If false, the deploy step is skipped, not failed.
- `dsl.ExitHandler(exit_task)`: the exit task always runs after the group, whether it passed or failed. In the YAML the `cleanup` task depends on the group with the strategy `ALL_UPSTREAM_TASKS_COMPLETED`. Use it for cleanup, not for logic that needs the result.
- Resources per task: `set_cpu_limit("2")`, `set_memory_limit("4G")`, `set_accelerator_type(...)`, `set_accelerator_limit(1)` land in the executor `resources` block. Node selector, tolerations and secrets come from the separate `kfp-kubernetes` package and land in a second YAML document (platform spec): `nodeSelector`, `tolerations`, `secretAsEnv`. Accelerator type names are platform specific; check current docs.
- Secrets as env vars: reference a Kubernetes secret by name; the value never appears in the YAML (the compiled file only has `wandb-key` and the key name).
- Failure modes: loops over big lists create many pods; no limit means the cluster fills; a missing `Collected` means the next step gets one value only; a node selector that matches no node leaves the pod Pending (see Q27).
- Not executed: submitting the pipeline. No cluster here. What ran: compile and inspect the YAML with kfp 2.17.3 and kfp-kubernetes 2.17.3 (kfp-kubernetes was installed in its own venv).

**Example:** `lrs = [0.1, 0.01, 0.001]`, score = `1 - abs(lr - 0.01) * 10`: 0.1 gives 0.1, 0.01 gives 1.0, 0.001 gives 0.91. `pick_best` returns 1.0; with `min_score = 0.8`, 1.0 >= 0.8 so `deploy` runs. If every score were below 0.8, deploy is skipped and `cleanup` still runs.

**Code:** the pipeline and the inspection script (python block). The driver `code/q26/run.sh` compiles in a temp dir and copies `pipeline.yaml` into the code folder.
{{CODE python q26/pipeline.py q26/inspect_yaml.py}}

**Output (my run):** compile only; the output is my script reading the real compiled YAML. The full file is `code/q26/pipeline.yaml`.
{{OUT q26/output.txt}}

**Follow-ups:**
1. *Where is the cache setting?* A `cachingOptions: enableCache: true` field on each task in the YAML (seen on `pick-best`); `set_caching_options(False)` removes it (seen in Q27).
2. *Why two YAML documents?* The second holds platform-specific settings from `kfp-kubernetes`; a backend that does not know it would ignore or reject it, check your backend.
3. *Can I nest `If` in `ParallelFor`?* Yes in principle; not tested here.

**Common mistakes:** Reading `t.output` after a loop without `Collected`. Putting real logic in the exit handler. Memory limit set below what the data needs (OOMKilled). Forgetting that `kfp-kubernetes` is a separate package. Hard-coding secret values into parameters.

@@Q27
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
{{CODE yaml q27/step_pod.yaml}}

{{CODE python q27/pipeline_ops.py}}

**Output (my run):** `kubernetes-validate` (offline schema check, Kubernetes 1.37) on the manifest, then the SDK script. Nothing was submitted anywhere.
{{OUT q27/output.txt}}

**Follow-ups:**
1. *How do I find the step's error?* The step pod logs (main container), then `kubectl describe pod` events, then the node and quota.
2. *Where do artifacts live?* In the object store configured for the install; only small values and URIs go through the metadata store. Check your install's docs.
3. *Recurring run missed a day?* Check the schedule's catch-up setting and that the cluster was up; `create_recurring_run` has a `no_catchup` argument in the SDK I ran.

**Common mistakes:** Debugging code when the pod never started. Using the default service account. Requesting a GPU and forgetting the toleration. Passing a big dataframe as a parameter. Not noticing a cache hit and thinking the step "ran".

@@Q28
**Say this first (1 line):** Argo Workflows is the general Kubernetes workflow engine (a Workflow is a list of templates, usually a DAG or steps of containers); Kubeflow Pipelines v1 compiled your Python to Argo YAML, and KFP v2 compiles to its own pipeline spec that the backend runs, so most ML teams do not write Argo directly.

**Then explain:**
- Argo objects: `Workflow` (one run), `WorkflowTemplate` (reusable, run by reference), `CronWorkflow` (a schedule that creates Workflows). Inside `spec.templates` you have container templates (do work) and `dag` or `steps` templates (wire them). Parameters are strings passed with `{{inputs.parameters.x}}`; artifacts are files moved through an artifact store; `dependencies: [train]` makes the DAG.
- KFP link: v1 SDK compiled to an Argo Workflow YAML. KFP v2 compiles to a platform-neutral IR YAML (header `# PIPELINE DEFINITION`, seen in Q26) and the backend decides how to run it. I am recalling this from docs and release notes, did not open them here; check current docs. In my own run the kfp 2.17.3 output was the IR, not an Argo Workflow.
- When a team uses Argo directly: non-ML or mixed workflows on Kubernetes (builds, ETL, batch), GitOps style, many small steps, need for Argo features like `CronWorkflow` concurrency rules and fine control of retries and templates. ML teams that want Python authoring, an experiment UI and lineage pick KFP or another tool.
- Failure modes: parameters are strings, so a number needs conversion inside the container; a typo in `dependencies` or a template name fails at submit; artifact store not configured means artifact steps fail.
- Not executed: Argo is not installed and nothing was submitted. What ran: a pyyaml check of the structure (kind, entrypoint exists, DAG dependencies exist, parameters used are declared), including a deliberately broken copy that the check caught.

**Example:** `train-eval.yaml` has a DAG `main` with two tasks: `train` (takes `lr` from the workflow parameter, writes `/tmp/model.txt` as an artifact `model`) and `evaluate` (depends on `train`, reads that artifact). A nightly `CronWorkflow` at `0 2 * * *` with `concurrencyPolicy: Forbid` starts a new run only if the previous one finished. The broken copy renames the dependency to `trian` and uses an undeclared `epochs` parameter, and the check reports both.

**Code:** the Argo YAML (yaml block) and the validator (python block).
{{CODE yaml q28/train-eval.yaml}}

{{CODE python q28/validate.py}}

**Output (my run):** `python3 -I validate.py train-eval.yaml`. This checks structure only; it is not Argo's own validation (that needs the `argo lint` CLI or a cluster, not available here).
{{OUT q28/output.txt}}

**Follow-ups:**
1. *Argo versus Airflow?* Argo is Kubernetes native with YAML; Airflow is Python with many operators. Argo fits container-only batch; Airflow fits mixed systems.
2. *Argo Events?* A separate project for triggers from webhooks and queues; concept only.
3. *Why not write Argo for ML?* Authoring a lot of YAML for data scientists, and no ML lineage or experiment UI by default.

**Common mistakes:** Treating all parameters as typed. Forgetting the artifact repository config. Assuming KFP v2 still produces Argo YAML. Using `generateName` in a file that a CronWorkflow must reference (use a `WorkflowTemplate`).

@@Q29
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

**Code:** compile a KFP pipeline for Vertex and inspect it (python block), the Step Functions sketch (json block), and the Vertex submit call as a sketch (second part of the python block is a comment only so it is not run).
{{CODE python q29/compile_for_vertex.py q29/check_yaml.py q29/check_asl.py}}

{{CODE json q29/states.json}}

```bash
# NOT EXECUTED (needs a GCP project, credentials and a bucket; check current docs for the exact calls):
#   from google.cloud import aiplatform
#   aiplatform.init(project="PROJECT", location="REGION")
#   aiplatform.PipelineJob(display_name="vertex-demo", template_path="vertex_demo.yaml",
#                          pipeline_root="gs://YOUR_BUCKET/pipeline_root", parameter_values={"lr": 0.01}).run()
# What did run: python -I compile_for_vertex.py && python -I check_yaml.py && python3 -I check_asl.py
```

**Output (my run):** kfp 2.17.3 compile and my two checks. No cloud call.
{{OUT q29/output.txt}}

**Follow-ups:**
1. *Is KFP YAML really portable?* The definition format is, the base images, buckets and service accounts inside it are not.
2. *SageMaker Pipelines or Step Functions?* ML-centric with registry and lineage: SageMaker Pipelines. Many AWS services and non-ML steps: Step Functions.
3. *Cost difference?* I do not quote numbers; compare the orchestration fee (small) against compute and engineering time.

**Common mistakes:** Comparing tools without naming the workload. Claiming a service does lineage without checking. Hard-coding project IDs in the pipeline file. Treating managed Airflow as zero-ops (versions, plugins, networking still need care).

@@Q30
**Say this first (1 line):** A retraining trigger is one small decision function (performance, then drift, then data volume, then age) that returns yes or no with a reason, and starting the run just means calling the orchestrator with a conf or parameters dict, so the pipeline code is the same whoever pulls the trigger.

**Then explain:**
- Trigger types: schedule (simple, wastes runs when nothing changed, misses a sudden shift); data volume (new rows since last train, good when labels arrive steadily); drift alert (input or prediction distribution moved, early but can fire without any harm to accuracy; Part 8 owns detection); performance (live metric below a floor, the strongest signal but labels are delayed, so it can be late). I order the rules from most to least urgent and also keep an age limit as a safety net.
- How a trigger starts a pipeline: Airflow: `TriggerDagRunOperator` from a gate DAG, or the REST API (check the API reference for path and auth); Prefect: `run_deployment(name, parameters=...)` or `prefect deployment run` (the CLI form ran in Q24); KFP: `Client.create_run_from_pipeline_package(..., arguments={...})`; AWS: EventBridge rule to a SageMaker pipeline start. Only the Airflow `--conf` path and the parameter checks were run here; REST, EventBridge and KFP submit are not executed.
- Run parameters: data end date and lookback window, model version or `auto`, a `dry_run` flag, hyperparameters, and a `reason` for the audit trail. Validate them in the DAG (Airflow `Param` with type and range). I ran a conf with `lookback_days: 9999` and it was refused before any task started.
- Failure modes: a trigger that fires every hour (flapping) because the drift metric hovers near the limit, so add a cooldown or minimum interval; two triggers firing at once (use one run at a time, `max_active_runs=1`, not tested here); retraining on bad data (put data checks first in the pipeline); dry run that still registers a model (my `dry_run` skips training and register).
- A trigger should not auto-promote a model. Retraining produces a candidate; promotion goes through the gate in Part 7.

**Example:** Today is 2026-10-26, last trained 2026-10-01 (25 days). Case "quiet": 5,000 new rows, PSI 0.05, AUC 0.86, so no trigger (25 < 30 days). Case "volume": 250,000 rows >= 100,000, so train. Case "drift": PSI 0.31 > 0.25, so train. Case "perf+drift": AUC 0.74 < 0.80 wins as the first rule, so the reason says performance. "No labels yet": AUC missing, other signals quiet, so no trigger. A model last trained 2026-09-01 is 55 days old, over the limit, so the schedule rule fires.

**Code:** decision function, a parametrised DAG with `Param` validation, and a gate DAG using `TriggerDagRunOperator` (python block); commands (bash block). The driver `code/q30/run.sh` runs everything with its own AIRFLOW_HOME.
{{CODE python q30/triggers.py q30/retrain_dag.py q30/trigger_dag.py}}

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
{{OUT q30/output.txt}}

**Follow-ups:**
1. *Schedule or event?* Start with schedule plus a volume rule. Add drift and performance when you have trusted metrics and a way to avoid flapping.
2. *Who approves a retrain?* Auto-train yes; auto-deploy no, unless there is an automatic gate with a rollback.
3. *How do I stop duplicate runs?* One active run per pipeline and a run key (the date and reason) so the same trigger twice does not train twice; not tested here.

**Common mistakes:** Treating drift as proof the model is bad. No cooldown. Training on the newest window with no check of the data. Letting `dry_run` write to production. Keeping the trigger logic inside the DAG so it cannot be unit tested.
