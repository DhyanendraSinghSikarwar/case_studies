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
