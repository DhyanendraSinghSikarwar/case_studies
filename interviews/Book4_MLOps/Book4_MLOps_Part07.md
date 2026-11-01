# Book 4 — Part 7: CI/CD for ML, GitHub Actions, model registry

**Topic:** CI/CD for ML: CI for ML code (lint, unit tests, data tests, training smoke tests), CD for models versus code, GitHub Actions (workflows, triggers, matrix, caching, secrets, OIDC to cloud, environments and approvals, reusable workflows, self-hosted and GPU runners, artifacts, concurrency), pipeline-as-code, continuous training triggers, model registry promotion (aliases, approvals, lineage, rollback), promotion gates (metric thresholds, fairness checks, shadow and canary tie-in), GitOps with Argo CD and Flux at concept level, Jenkins and GitLab CI comparison, Docker image build, scan and push in CI, semantic versioning of models and data, release notes and model cards, rollback and blue-green for models, CI cost and time optimisation, and security (secrets, supply chain, SBOM at concept level)
**Target:** 40  |  **Actual:** 40 (⭐⭐⭐ 15, ⭐⭐ 15, ⭐ 10)  |  **Date:** 2026-10-26  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 1 owns Git, pre-commit and pytest for ML code; Part 2 owns Docker (images, tags, scanning concepts); Part 3 owns Kubernetes, Helm and cluster rollouts; Part 4 owns DVC, MLflow and registry basics and governance; Part 5 owns pipelines and orchestration; Part 6 owns serving and rollout mechanics (shadow, canary, blue-green); Part 8 owns model monitoring, drift and data-quality monitoring; Part 9 owns feature stores, Kafka and Spark; Parts 10 and 11 own AWS, Azure and GCP services (IAM depth); Part 12 owns cost and system design in depth; Book 2 owns LLM internals; Book 3 owns SQL; Book 6 owns product and business. This part owns the automation around them: CI workflows, promotion gates, CD and rollback.

Evidence limits: the pages found could not be opened (WebFetch failed with getaddrinfo ENOTFOUND for docs.github.com), so every source is a search snippet only (see research_notes/Book4_Part07_sources.md). No page was found that reports exact CI/CD questions asked by a named company at an India or global ML role; 'Asked at' tags therefore name source types (question banks, docs, security write-ups), not verified company reports. Execution limit: pip install worked through the proxy in a fresh venv (/tmp/claude-0/b7p07/v), so Wave B can really run on Python 3.13.17: PyYAML 6.0.3, actionlint-py 1.7.12.25 (actionlint 1.7.12), check-jsonschema 0.38.2 (its built-in GitHub workflow schema works offline), MLflow 3.17.2 (sqlite registry with aliases), pytest 9.1.1, ruff 0.17.2, scikit-learn 1.9.1, numpy 2.5.4, pandas 3.1.0, git 2.43.0, and the docker CLI 29.9.2 with buildx v0.38.1 and compose v5.6.1 (no daemon: docker build fails with 'failed to connect to the docker API'). Everything needing a real GitHub runner or environment, OIDC token exchange, a cloud account, Argo CD, Flux, Jenkins, GitLab runners, a GPU, a Docker daemon, Trivy, Syft or cosign, a Kubernetes cluster or an authenticated MLflow server must be labelled 'not executed'. Note for Wave B: actionlint flags unknown custom runner labels such as gpu unless an actionlint.yaml config lists them, and PyYAML parses the workflow key on as the boolean True.

---

### Q1 ⭐⭐⭐ 🟢 CI, CD and CT for machine learning. Define continuous integration, continuous delivery (or deployment) and continuous training, say what each one tests or ships in an ML system (code, data, model, pipeline, serving image), and explain how ML differs from ordinary software CI/CD because a model can change without a code change and a data change can break a green build. Draw the stage map (lint, unit tests, data tests, smoke train, full train, evaluate, register, gate, deploy, monitor) as a workflow-style YAML with a needs graph, parse it with pyyaml and print the jobs in dependency order. Say where Part 5 (orchestration) and Part 8 (monitoring) take over.
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Continuous training and maturity-level write-ups (open-exam-prep.com MLOps CI/CD retraining guide, nerdleveltech.com MLOps maturity levels, resumelens.org, nicheelab.com Vertex AI pipelines, a Google Cloud 'MLOps: continuous delivery and automation pipelines' page named by the search tool but not shown; search snippets only, not opened; level numbering differs between secondary sources); study guides, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** CI tests every change to code, data and pipeline, CD ships a tested model and its serving image behind a gate, and CT retrains on a trigger; the ML twist is that a model can change with no code change, and a data change can break a green build.

**Then explain:**
- **CI (continuous integration):** on every pull request, check the things you own: code (lint, unit tests), data (schema, nulls, ranges on a sample), the pipeline (a tiny smoke train that runs end to end). Fast, cheap, blocks the merge.
- **CD (continuous delivery or deployment):** take a model that passed evaluation and move it toward users: register it, pass the gate, deploy the serving image or move a pointer. Delivery means a human approves the last step. Deployment means no human.
- **CT (continuous training):** the extra ML loop. Retrain on a schedule, on new data, or on a drift alert, then evaluate, register, gate. It runs with no commit at all.
- **Why ML differs:** three things change, not one: code, data and model. Same commit plus new data gives a different model. A bad upstream column breaks the model while every unit test is still green. So CI needs data tests, and CD needs a metric gate, not only "tests pass".
- **What ships:** CI ships nothing, it gives a yes or no. CD ships a model artifact plus a serving image. CT ships a new model version into the registry.
- **Hand-off:** Part 5 (orchestration) takes over the scheduled, long, multi-step training run (the `full-train` to `register` stages). Part 8 (monitoring) takes over after `deploy`: the monitor stage is not a CI job, it watches live traffic and fires CT.
- **Failure modes:** green CI with silently shifted data; a retrain that is worse than the champion but gets deployed because nothing compared them; training and serving use different preprocessing.

**Example:** A churn model repo. A developer edits a feature function: CI runs lint, unit and data tests, then a smoke train, and blocks the PR if any fail. Two weeks later, with no commit, the nightly CT job retrains on fresh data, evaluates, registers version 7 and runs the gate. The gate fails (AUC dropped 0.02 against the champion), so nothing is deployed. The stage map below puts both loops on one needs graph; `lint` is the only root and `deploy` the only leaf, and `unit` and `data-tests` can run in parallel.

**Code:**
Workflow YAML:
```yaml
name: ml-stage-map
on: [pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [{run: ruff check .}]
  unit:
    needs: lint
    runs-on: ubuntu-latest
    steps: [{run: pytest tests/unit}]
  data-tests:
    needs: lint
    runs-on: ubuntu-latest
    steps: [{run: pytest tests/data}]
  smoke-train:
    needs: [unit, data-tests]
    runs-on: ubuntu-latest
    steps: [{run: python train.py --smoke}]
  full-train:
    needs: smoke-train
    runs-on: ubuntu-latest
    steps: [{run: python train.py --full}]
  evaluate:
    needs: full-train
    runs-on: ubuntu-latest
    steps: [{run: python evaluate.py}]
  register:
    needs: evaluate
    runs-on: ubuntu-latest
    steps: [{run: python register.py}]
  gate:
    needs: register
    runs-on: ubuntu-latest
    steps: [{run: python gate.py}]
  deploy:
    needs: gate
    runs-on: ubuntu-latest
    steps: [{run: python deploy.py}]
```

Python:
```python
import sys, graphlib, yaml
wf = yaml.safe_load(open(sys.argv[1]))
print("top-level keys:", list(wf))            # note: 'on' is parsed as True
jobs = wf["jobs"]
deps = {}
for name, j in jobs.items():
    n = j.get("needs", [])
    deps[name] = [n] if isinstance(n, str) else list(n)
order = list(graphlib.TopologicalSorter(deps).static_order())
for i, j in enumerate(order, 1):
    print(i, j, "<-", deps[j] or "-")
ts = graphlib.TopologicalSorter(deps); ts.prepare()
wave = 0
while ts.is_active():
    ready = sorted(ts.get_ready()); wave += 1
    print("wave", wave, "runs in parallel:", ready)
    ts.done(*ready)
```

Shell (venv with actionlint-py, check-jsonschema, pytest, PyYAML on PATH):
```shell
python -I q01_order.py q01_stage_map.yml
actionlint q01_stage_map.yml; echo "actionlint exit=$?"
```

**Output (my run):** Not executed here: a real GitHub runner, so none of these workflows ran on GitHub. The validation that did run is below: PyYAML parsed the file (note the top-level key `on` shows up as `True`, see Q2), `graphlib` ordered the `needs` graph, and actionlint accepted it (exit 0). The `monitor` stage is deliberately not in the YAML: it is not a CI job (Part 8).
```text
$ python -I q01_order.py q01_stage_map.yml
top-level keys: ['name', True, 'jobs']
1 lint <- -
2 unit <- ['lint']
3 data-tests <- ['lint']
4 smoke-train <- ['unit', 'data-tests']
5 full-train <- ['smoke-train']
6 evaluate <- ['full-train']
7 register <- ['evaluate']
8 gate <- ['register']
9 deploy <- ['gate']
wave 1 runs in parallel: ['lint']
wave 2 runs in parallel: ['data-tests', 'unit']
wave 3 runs in parallel: ['smoke-train']
wave 4 runs in parallel: ['full-train']
wave 5 runs in parallel: ['evaluate']
wave 6 runs in parallel: ['register']
wave 7 runs in parallel: ['gate']
wave 8 runs in parallel: ['deploy']
$ actionlint q01_stage_map.yml
actionlint exit=0
```

**Follow-ups:**
- *Is CT the same as a nightly CI run?* No. A nightly CI re-runs tests on the same code. CT produces a new model from new data and ends in the registry.
- *Where does CT start?* On a time trigger, a data-arrival trigger or a drift alert (Part 8). Pick the simplest one that fits how fast your data goes stale.
- *Do you need all stages from day one?* No. Start with lint, unit, smoke train and a gate; add the rest as pain shows up.

**Common mistakes:**
- Saying CI/CD for ML is "just DevOps". The data and model axes are the whole point.
- Testing code only, with no data tests, so a schema change goes to production.
- Full training on every PR. That is slow and costly; use a smoke train on PRs and full training on schedule.
- Confusing delivery (human approves) with deployment (automatic).
- Claiming a maturity "level number" for CT. Sources disagree on numbering; just say what each stage does.

### Q2 ⭐⭐⭐ 🟢 Anatomy of a GitHub Actions workflow for an ML repository. Explain on, jobs, runs-on, steps, uses versus run, with, env, needs, permissions, and where the file lives (.github/workflows). Write a pull-request workflow that runs ruff and pytest on a Python matrix with pip caching, then check it two ways without any GitHub runner: actionlint (actionlint-py) and check-jsonschema with the built-in GitHub workflow schema (no network needed). Show the real output for a good file and for a file with a typo'd event name, a missing needs target and an untrusted-input expression, and explain the YAML 1.1 trap where the key on becomes the boolean True under pyyaml.
**Asked at:** GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD | MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** A workflow is a YAML file in `.github/workflows/` with a trigger (`on`), one or more `jobs` that each pick a runner (`runs-on`) and run `steps`, where a step either calls an action (`uses`) or runs a shell command (`run`); you can lint it offline with actionlint and check-jsonschema.

**Then explain:**
- **Where:** `.github/workflows/*.yml` on the default branch of the repo. One file, one workflow.
- **`on`:** what starts it (`pull_request`, `schedule`, ...; Q4). **`jobs`:** a map of jobs. Jobs run in parallel unless one has **`needs`** pointing at another.
- **`runs-on`:** the runner label (`ubuntu-latest`, or a self-hosted label). **`steps`:** run in order on the same machine. A **step** is `uses: owner/action@ref` (reuse) or `run:` (a shell command). **`with`** passes inputs to an action, **`env`** sets environment variables.
- **`permissions`:** what the `GITHUB_TOKEN` may do. Set `contents: read` at the top and widen per job only.
- **`matrix`:** one job definition fanned out over values (here Python 3.11 and 3.12). `fail-fast: false` lets the other cells finish when one fails.
- **YAML 1.1 trap:** PyYAML reads the bare key `on` as the boolean `True`, so `wf["on"]` raises KeyError or `.get("on")` is `None`. GitHub itself handles it fine. Fix in your own tooling: look up `True` as well, or use a parser with YAML 1.2 rules.
- **Limit of linting:** actionlint and the schema check syntax and expressions. They cannot tell you the job will pass on a real runner, or that a secret exists.

**Example:** Good file: a PR triggers `test`, which runs on two Python versions, restores the pip cache keyed on `requirements.txt`, runs `ruff` then `pytest`. Bad file: three planted mistakes. `pull_requests` (extra s) is not an event, `needs: tests` points at a job called `test`, and the PR title is pasted straight into a `run` script, which lets a PR author inject shell commands. actionlint reports all three; the schema check reports the event only (it checks structure, not expression safety or job names).

**Code:**
Workflow YAML:
```yaml
# ===== q02_good.yml =====
name: ci
on:
  pull_request:
    paths: ["src/**", "tests/**", "requirements*.txt"]
permissions:
  contents: read
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    strategy:
      fail-fast: false
      matrix:
        python: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
          cache: pip
          cache-dependency-path: requirements.txt
      - run: pip install -r requirements.txt
      - run: ruff check src tests
      - run: pytest -q

# ===== q02_bad.yml =====
name: ci-bad
on:
  pull_requests:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "title is ${{ github.event.pull_request.title }}"
  report:
    needs: tests
    runs-on: ubuntu-latest
    steps:
      - run: echo done
```

Python:
```python
import yaml
print(yaml.safe_load("on: push"))
wf = yaml.safe_load(open("q02_good.yml"))
print("keys:", list(wf))
print("wf.get('on'):", wf.get("on"))
print("wf.get(True):", wf.get(True))
def trigger(wf):                      # safe reader: accept both spellings
    return wf.get("on", wf.get(True))
print("safe reader:", trigger(wf))
print("quoted key:", list(yaml.safe_load('"on": push')))
```

Shell (venv with actionlint-py, check-jsonschema, pytest, PyYAML on PATH):
```shell
actionlint q02_good.yml; echo "exit=$?"
check-jsonschema --builtin-schema vendor.github-workflows q02_good.yml; echo "exit=$?"
actionlint q02_bad.yml; echo "exit=$?"
check-jsonschema --builtin-schema vendor.github-workflows q02_bad.yml; echo "exit=$?"
python -I q02_on_trap.py
```

**Output (my run):** Not executed here: a real GitHub runner, so none of these workflows ran on GitHub. Everything below really ran offline: actionlint 1.7.12 (from actionlint-py), check-jsonschema 0.38.2 with the built-in `vendor.github-workflows` schema, and PyYAML 6.0.3.
```text
$ actionlint q02_good.yml
exit=0
$ check-jsonschema --builtin-schema vendor.github-workflows q02_good.yml
ok -- validation done
exit=0
$ actionlint q02_bad.yml
q02_bad.yml:3:3: unknown Webhook event "pull_requests". see https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#webhook-events for list of all Webhook event names [events]
  |
3 |   pull_requests:
  |   ^~~~~~~~~~~~~~
q02_bad.yml:9:33: "github.event.pull_request.title" is potentially untrusted. avoid using it directly in inline scripts. instead, pass it through an environment variable. see https://docs.github.com/en/actions/reference/security/secure-use#good-practices-for-mitigating-script-injection-attacks for more details [expression]
  |
9 |       - run: echo "title is ${{ github.event.pull_request.title }}"
  |                                 ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
q02_bad.yml:10:3: job "report" needs job "tests" which does not exist in this workflow [job-needs]
   |
10 |   report:
   |   ^~~~~~~
exit=1
$ check-jsonschema --builtin-schema vendor.github-workflows q02_bad.yml
Schema validation errors were encountered.
  q02_bad.yml::$.on: {'pull_requests': {'branches': ['main']}} is not valid under any of the given schemas
  Underlying errors caused this.

  Best Match:
    $.on: {'pull_requests': {'branches': ['main']}} is not of type 'string'

  3 other errors were produced. Use '--verbose' to see all errors.
exit=1
$ python -I q02_on_trap.py
{True: 'push'}
keys: ['name', True, 'permissions', 'concurrency', 'jobs']
wf.get('on'): None
wf.get(True): {'pull_request': {'paths': ['src/**', 'tests/**', 'requirements*.txt']}}
safe reader: {'pull_request': {'paths': ['src/**', 'tests/**', 'requirements*.txt']}}
quoted key: ['on']
```

**Follow-ups:**
- *`uses` or `run`?* `uses` for a maintained action (checkout, setup-python); `run` for your own commands. Pin third-party actions to a full commit SHA (Q5).
- *Does actionlint check OIDC permissions?* No. In my testing it does not flag a missing `id-token: write`; test that on a real run (Q6).
- *Can I run it locally?* `act` is a separate tool and was not available here, so I only linted.

**Common mistakes:**
- Putting the file anywhere except `.github/workflows/`; it will not run.
- Forgetting `needs`, then wondering why jobs run in parallel and one reads an artifact the other has not made yet.
- Reading workflow YAML in Python with `wf["on"]` and getting a KeyError.
- Treating a green `check-jsonschema` as proof the workflow is safe or correct.
- Leaving `permissions` unset, so the token gets the repo default, which may be broader than needed (check current docs for the default).

### Q3 ⭐⭐⭐ 🟡 A layered CI test suite for an ML repo and what runs when. Explain the pyramid: lint and type checks, fast unit tests on small arrays, data tests on a sample (schema, nulls, ranges), a training smoke test (a few hundred rows, two epochs, assert the loss is finite and falls, the artifact is written and reloads, finish in under a minute or two) and a nightly full training. Say what fails the PR versus what only warns, and the time budget. Part 1 owns pytest and pre-commit basics, so do not repeat them; focus on the smoke test and the PR versus nightly split. Write the smoke test with scikit-learn and pytest and run it, then show the workflow with a pytest marker split (pytest -m 'not slow' on PRs, slow on schedule).
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Run a fast pyramid on every PR (lint, unit, data tests on a sample, a one-minute smoke train) and push the full training and quality checks to a nightly job, using a pytest marker to split them.

**Then explain:**
- **The pyramid, cheapest first:** lint and types, unit tests on tiny arrays, data tests on a sample (schema, nulls, ranges), training smoke test, nightly full training. Each layer catches a different bug; run the cheap ones first so a typo fails in seconds.
- **Smoke test:** a few hundred rows, two epochs. Assert: loss is finite, loss goes down, the artifact is written, the artifact reloads and predicts. It proves the pipeline wires together, not that the model is good. Aim for about a minute or two.
- **Fails the PR:** lint, unit, data schema, smoke test. **Only warns or alerts:** slow quality checks on the full dataset, soft metric drift, a flaky external dependency. Decide this once, write it down.
- **Time budget:** PR checks should finish in minutes, or people stop waiting and merge anyway. Full training goes on `schedule` with a long `timeout-minutes`.
- **Failure modes:** a smoke test that checks nothing (only "it ran"); a full test marked `slow` that nobody reads when it fails; test data that is so clean the data tests never fail; an unseeded run that makes "loss falls" flaky.
- Part 1 owns pytest and pre-commit basics; this answer is only the smoke test and the PR versus nightly split.

**Example:** A fixture builds 300 synthetic rows. `SGDClassifier` trains for 2 `partial_fit` epochs; the log loss after epoch 1 must be higher than after epoch 2, and the saved joblib file must reload and predict 5 rows. The nightly test trains on 20,000 rows for 50 epochs and requires accuracy above 0.75 (a threshold I chose for this synthetic data, not a benchmark). `pytest -m "not slow"` runs the first only; `pytest -m slow` the second.

**Code:**
Python:
```python
# ===== train_lib.py =====
import numpy as np, joblib
from sklearn.datasets import make_classification
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import log_loss

def make_data(n, seed=0):
    return make_classification(n_samples=n, n_features=10, n_informative=5, random_state=seed)

def train(X, y, epochs, out_path):
    clf = SGDClassifier(loss="log_loss", random_state=0, learning_rate="constant", eta0=0.05)
    losses = []
    for _ in range(epochs):
        clf.partial_fit(X, y, classes=[0, 1])
        losses.append(log_loss(y, clf.predict_proba(X)))
    joblib.dump(clf, out_path)
    return losses

# ===== test_train.py =====
import math, pytest, joblib, numpy as np
from train_lib import make_data, train

def test_smoke_train(tmp_path):
    X, y = make_data(300)                       # a few hundred rows
    out = tmp_path / "model.joblib"
    losses = train(X, y, epochs=2, out_path=out)
    assert all(math.isfinite(v) for v in losses)     # no NaN / inf
    assert losses[-1] < losses[0]                    # loss falls
    assert out.exists() and out.stat().st_size > 0   # artifact written
    clf = joblib.load(out)                           # artifact reloads
    assert clf.predict(X[:5]).shape == (5,)

@pytest.mark.slow
def test_full_train_quality(tmp_path):
    X, y = make_data(20000, seed=1)
    losses = train(X, y, epochs=50, out_path=tmp_path / "m.joblib")
    clf = joblib.load(tmp_path / "m.joblib")
    assert (clf.predict(X) == y).mean() > 0.75       # nightly quality floor
```

pytest.ini:
```ini
[pytest]
markers =
    slow: full training, nightly only
```

Workflow YAML:
```yaml
name: ci-layers
on:
  pull_request:
  schedule:
    - cron: "30 20 * * *"      # UTC, default branch only
permissions:
  contents: read
jobs:
  pr-checks:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12", cache: pip}
      - run: pip install -r requirements.txt
      - run: ruff check .
      - run: pytest -m "not slow" -q        # lint + unit + data + smoke: blocks the PR
  nightly-full:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    timeout-minutes: 120
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12", cache: pip}
      - run: pip install -r requirements.txt
      - run: pytest -m slow -q              # full training: alerts, does not block PRs
```

Shell (venv with actionlint-py, check-jsonschema, pytest, PyYAML on PATH):
```shell
pytest -m "not slow" -q -p no:cacheprovider
pytest -m slow -q -p no:cacheprovider
actionlint ci.yml; echo "actionlint exit=$?"
check-jsonschema --builtin-schema vendor.github-workflows ci.yml
```

**Output (my run):** Not executed here: a real GitHub runner, so none of these workflows ran on GitHub. The tests and the marker split below really ran with scikit-learn 1.9.1 and pytest 9.1.1; the workflow was only linted (actionlint and check-jsonschema). Timings are sandbox-only.
```text
$ pytest -m 'not slow' -q -p no:cacheprovider
.                                                                        [100%]
1 passed, 1 deselected in 1.35s
$ pytest -m slow -q -p no:cacheprovider
.                                                                        [100%]
1 passed, 1 deselected in 1.75s
$ actionlint ci.yml
actionlint exit=0
$ check-jsonschema --builtin-schema vendor.github-workflows ci.yml
ok -- validation done
```

**Follow-ups:**
- *Why a marker and not two folders?* Either works. A marker keeps the tests next to the code; register it in `pytest.ini` so a typo in the marker name is caught with `--strict-markers`.
- *How do you stop flakiness?* Seed everything and assert on a direction (loss falls), not an exact number.
- *Nightly fails, what then?* It alerts the team and opens a ticket; it does not block unrelated PRs.

**Common mistakes:**
- Running the full training on every PR.
- A smoke test with no artifact reload step, so a broken save/load ships.
- Exact-number assertions on loss, which break on a library upgrade.
- Unregistered markers: pytest only warns by default, and `-m "not slow"` still runs a mistyped one.
- Letting the nightly job fail for weeks with nobody owning it.

### Q4 ⭐⭐⭐ 🟡 Workflow triggers for an ML repository. Explain push, pull_request, paths and branches filters, schedule (cron is UTC and only runs from the default branch), workflow_dispatch with inputs, workflow_run, repository_dispatch, release and workflow_call, and choose triggers for a repo that has code CI on every PR, a nightly training, a manual 'retrain now' button and a retrain when new data lands. Explain pull_request versus pull_request_target (why the second is dangerous with untrusted fork code) and why a schedule trigger may silently stop on an inactive repository (check current docs). Validate every trigger block with actionlint and check-jsonschema and show the output.
**Asked at:** GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Use `pull_request` with `paths` for code CI, `schedule` for nightly training, `workflow_dispatch` for the manual button and `repository_dispatch` for new data; avoid `pull_request_target` with fork code.

**Then explain:**
- **`push` / `pull_request`:** the code CI triggers. `branches` filters by branch, `paths` by changed files, so a docs edit does not train a model. If a required check is skipped by a `paths` filter, check current docs for how branch protection treats it.
- **`schedule`:** cron, in **UTC**, and only runs from the **default branch**. On an inactive repository GitHub may disable scheduled workflows after a period of no activity (check current docs), so a "nightly" job can silently stop.
- **`workflow_dispatch`:** a manual button with typed `inputs` (string, boolean, choice). **`repository_dispatch`:** an API call from outside (a data pipeline says "new data landed") with a `client_payload`. **`workflow_run`:** start after another workflow finishes. **`release`:** on publish. **`workflow_call`:** makes the workflow callable from other workflows (reusable workflows).
- **`pull_request` vs `pull_request_target`:** the first runs the merge result with a read-only token and no secrets for fork PRs. The second runs in the context of the **base** repo, with secrets and a write-capable token. If it checks out and runs the fork's code, an outsider runs code with your secrets. Use it only for things like labelling, and never run untrusted code in it.
- **Failure modes:** `branch:` instead of `branches:`, a bad cron, a boolean input with a string default, a `schedule` that never runs because the file is not on the default branch.

**Example:** Repo needs: (1) code CI on every PR touching code: `ci.yml` (`pull_request`, `paths`). (2) Nightly training at 20:30 UTC (02:00 IST): `schedule` in `train.yml`. (3) A "retrain now" button: `workflow_dispatch` with `data_version` and `full` inputs. (4) Retrain when new data lands: the data job calls `repository_dispatch` with type `new-data`. All three training triggers share one `train.yml`, which can also be called by other workflows via `workflow_call`. `after_ci.yml` shows `workflow_run` and `release`. `risky_target.yml` is the pattern to avoid: lint accepts it.

**Code:**
Workflow YAML:
```yaml
# ===== ci.yml =====
name: code-ci
on:
  push:
    branches: [main]
    paths: ["src/**", "tests/**", "requirements*.txt"]
  pull_request:
    branches: [main]
    paths: ["src/**", "tests/**", "requirements*.txt"]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt && pytest -m "not slow" -q

# ===== train.yml =====
name: train
on:
  workflow_call:
    inputs:
      data_version:
        type: string
        required: true
  workflow_dispatch:
    inputs:
      data_version:
        description: "Data tag to train on"
        type: string
        default: "latest"
      full:
        description: "Full training (not smoke)"
        type: boolean
        default: false
  schedule:
    - cron: "30 20 * * *"
  repository_dispatch:
    types: [new-data]
permissions:
  contents: read
jobs:
  train:
    runs-on: ubuntu-latest
    env:
      DATA_VERSION: ${{ inputs.data_version || github.event.client_payload.data_version || 'latest' }}
      FULL: ${{ inputs.full || github.event_name == 'schedule' }}
    steps:
      - uses: actions/checkout@v4
      - run: python train.py --data "$DATA_VERSION" --full "$FULL"

# ===== after_ci.yml =====
name: after-ci
on:
  workflow_run:
    workflows: ["code-ci"]
    types: [completed]
    branches: [main]
  release:
    types: [published]
permissions:
  contents: read
jobs:
  follow-up:
    if: github.event_name == 'release' || github.event.workflow_run.conclusion == 'success'
    runs-on: ubuntu-latest
    steps:
      - run: echo "CI passed on main or a release was published"

# ===== risky_target.yml =====
name: risky
on:
  pull_request_target:
    types: [opened, synchronize]
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}   # untrusted fork code
      - run: pip install -r requirements.txt && pytest

# ===== bad_triggers.yml =====
name: bad
on:
  push:
    branch: [main]
  schedule:
    - cron: "61 25 * * *"
  workflow_dispatch:
    inputs:
      full:
        type: boolean
        default: "yes"
jobs:
  x:
    runs-on: ubuntu-latest
    steps: [{run: "echo hi"}]
```

Shell (venv with actionlint-py, check-jsonschema, pytest, PyYAML on PATH):
```shell
for f in ci train after_ci risky_target bad_triggers; do
  echo "== $f.yml"
  actionlint $f.yml; echo "actionlint exit=$?"
  check-jsonschema --builtin-schema vendor.github-workflows $f.yml; echo "schema exit=$?"
done
```

**Output (my run):** Not executed here: a real GitHub runner, so none of these workflows ran on GitHub. Real runs below: actionlint and check-jsonschema on all five files. Four are clean; the broken one (wrong key `branch`, cron `61 25 * * *`, a boolean input with default `yes`) is rejected by both. Note that `risky_target.yml` passes both checkers: they do not detect the unsafe checkout, so review that by reading.
```text
== ci.yml
$ actionlint ci.yml
actionlint exit=0
$ check-jsonschema --builtin-schema vendor.github-workflows ci.yml
ok -- validation done
schema exit=0
== train.yml
$ actionlint train.yml
actionlint exit=0
$ check-jsonschema --builtin-schema vendor.github-workflows train.yml
ok -- validation done
schema exit=0
== after_ci.yml
$ actionlint after_ci.yml
actionlint exit=0
$ check-jsonschema --builtin-schema vendor.github-workflows after_ci.yml
ok -- validation done
schema exit=0
== risky_target.yml
$ actionlint risky_target.yml
actionlint exit=0
$ check-jsonschema --builtin-schema vendor.github-workflows risky_target.yml
ok -- validation done
schema exit=0
== bad_triggers.yml
$ actionlint bad_triggers.yml
bad_triggers.yml:4:5: unexpected key "branch" for "push" section. expected one of "branches", "branches-ignore", "paths", "paths-ignore", "tags", "tags-ignore", "types", "workflows" [syntax-check]
  |
4 |     branch: [main]
  |     ^~~~~~~
bad_triggers.yml:6:13: invalid CRON format "61 25 * * *" in schedule event: end of range (61) above maximum (59): 61 [events]
  |
6 |     - cron: "61 25 * * *"
  |             ^~~
bad_triggers.yml:11:18: type of "full" input is "boolean". its default value "yes" must be "true" or "false" [events]
   |
11 |         default: "yes"
   |                  ^~~~~
actionlint exit=1
$ check-jsonschema --builtin-schema vendor.github-workflows bad_triggers.yml
Schema validation errors were encountered.
  bad_triggers.yml::$.on: {'push': {'branch': ['main']}, 'schedule': [{'cron': '61 25 * * *'}], 'workflow_dispatch': {'inputs': {'full': {'type': 'boolean', 'default': 'yes'}}}} is not valid under any of the given schemas
  Underlying errors caused this.

  Best Match:
    $.on: {'push': {'branch': ['main']}, 'schedule': [{'cron': '61 25 * * *'}], 'workflow_dispatch': {'inputs': {'full': {'type': 'boolean', 'default': 'yes'}}}} is not of type 'string'
  Best Deep Match:
    $.on.push: {'branch': ['main']} is not of type 'null'

  4 other errors were produced. Use '--verbose' to see all errors.
schema exit=1
```

**Follow-ups:**
- *IST night run?* Cron has no time zone; convert (IST is UTC+5:30).
- *Can I trigger one workflow from another?* `workflow_run`, `workflow_call` or `repository_dispatch`. `workflow_call` is the clearest.
- *Why does GITHUB_TOKEN not trigger new runs?* Events created with the default token generally do not start new workflow runs (check current docs); use a GitHub App or PAT if you need chaining.

**Common mistakes:**
- Expecting `schedule` to run from a feature branch.
- Using `pull_request_target` to "get secrets in fork PR tests" and then running the fork's code.
- Treating cron time as local time.
- No `paths` filter, so a README edit burns CI minutes.
- Passing a boolean input and comparing it as a string (`inputs.full == 'true'` versus `inputs.full`).

### Q5 ⭐⭐⭐ 🟡 Secrets, variables and GITHUB_TOKEN in GitHub Actions for ML teams. Explain repository, environment and organisation secrets versus variables, why secrets are not passed to workflows from forks, log masking and its limits (a secret that is base64-encoded or split is not masked), setting permissions to least privilege (contents: read by default), script injection through expressions like github.event.pull_request.title, and what to do after a secret leaks (rotate, do not just delete the log). Show a workflow that passes a secret through env instead of inlining it, run actionlint on an unsafe version and a safe version, and say Part 2 owns secrets inside Docker builds.
**Asked at:** GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD | Actions supply-chain incident reports (orca.security, wiz.io, infoworld.com, phoenix.security, securityboulevard.com on the March 2025 tj-actions/changed-files compromise CVE-2025-30066; search snippets only, not opened; nothing found on SBOM or provenance attestations); security vendor posts, not interview reports; DevSecOps, platform and MLOps roles
**Say this first (1 line):** Keep secrets in the secret store, pass them to a step through `env` (never pasted into a script or a log), give the token the least permission, and treat any text from a PR as hostile input.

**Then explain:**
- **Scopes:** repository, environment and organisation **secrets** (encrypted, masked in logs) versus **variables** (plain text, for non-sensitive config such as a region or model name). Environment secrets only load after the environment's protection rules pass (Q7).
- **Forks:** secrets are not passed to workflows triggered by fork pull requests (except via risky triggers, Q4), and the token there is read-only.
- **Masking is exact-string match:** a secret that is base64-encoded, transformed or split across lines is not masked (see the demo). Masking is a safety net, not a plan. Do not `echo` secrets or use `set -x` around them.
- **`GITHUB_TOKEN`:** a short-lived, per-run token. Set `permissions: contents: read` at the top and add `id-token: write`, `pull-requests: write` only on the job that needs it.
- **Script injection:** `${{ github.event.pull_request.title }}` is replaced by text **before** the shell runs. A title with `"; curl ... ;` becomes code. Fix: put the value in `env:` and use `"$PR_TITLE"` in the script. Branch names (`github.head_ref`), issue titles and commit messages are attacker-controlled too.
- **After a leak:** rotate the secret first. Deleting the log or the run does not un-leak it, because copies and caches exist. Then find the cause and review what the credential could access.
- **Supply chain:** the March 2025 `tj-actions/changed-files` incident (CVE-2025-30066, from security vendor write-ups; I did not open them) involved tags being re-pointed to malicious code. Pin third-party actions to a full commit SHA, not a tag.

**Example:** A PR titled `x"; echo INJECTED; "` hits the unsafe workflow. The runner builds the script text `echo "PR title is x"; echo INJECTED; ""`, so the second `echo` is a command. In the safe version the title only ever lives in `$PR_TITLE`, so it is printed as plain text. The demo script reproduces exactly this with a harmless `echo` (no real secrets anywhere).

**Code:**
Workflow YAML:
```yaml
# ===== unsafe.yml =====
name: report-unsafe
on:
  pull_request:
    types: [opened, edited]
jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - run: echo "PR title is ${{ github.event.pull_request.title }}"
      - run: |
          curl -H "Authorization: Bearer ${{ secrets.REGISTRY_TOKEN }}" https://registry.example.com/ping
      - run: echo "branch is ${{ github.head_ref }}"

# ===== safe.yml =====
name: report-safe
on:
  pull_request:
    types: [opened, edited]
permissions:
  contents: read
jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - name: Print title safely
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}
        run: echo "PR title is $PR_TITLE"
      - name: Call registry
        env:
          REGISTRY_TOKEN: ${{ secrets.REGISTRY_TOKEN }}
        run: |
          curl -H "Authorization: Bearer $REGISTRY_TOKEN" https://registry.example.com/ping
```

Python:
```python
import base64
secret = "s3cr3t-token-123"
masked = lambda line: line.replace(secret, "***")      # what log masking does: exact-string match
for label, line in [("exact", f"token={secret}"),
                    ("base64", "token=" + base64.b64encode(secret.encode()).decode()),
                    ("split", "token=" + secret[:6] + " " + secret[6:])]:
    print(f"{label:7}-> {masked(line)}")
```

Shell (venv with actionlint-py, check-jsonschema, pytest, PyYAML on PATH):
```shell
# ===== cmds.sh =====
actionlint unsafe.yml; echo "unsafe exit=$?"
actionlint safe.yml; echo "safe exit=$?"
bash inject_demo.sh
python -I mask_demo.py

# ===== inject_demo.sh =====
#!/usr/bin/env bash
# Simulates what the runner does: the unsafe form pastes the title INTO the script text first.
TITLE='x"; echo INJECTED-COMMAND-RAN; echo "'
echo "--- unsafe: expression pasted into the script text"
printf 'echo "PR title is %s"\n' "$TITLE" > /tmp/claude-0/b7_q01_10/unsafe_step.sh
cat /tmp/claude-0/b7_q01_10/unsafe_step.sh
bash /tmp/claude-0/b7_q01_10/unsafe_step.sh
echo "--- safe: value passed as an environment variable"
PR_TITLE="$TITLE" bash -c 'echo "PR title is $PR_TITLE"'
```

**Output (my run):** Not executed here: a real GitHub runner, so none of these workflows ran on GitHub. Real runs below: actionlint flags two untrusted expressions in the unsafe file and passes the safe file; the shell demo shows the injection; the Python demo shows masking missing base64 and split secrets. actionlint did not flag `${{ secrets.REGISTRY_TOKEN }}` pasted into the `run` line (line 10), so it does not replace review. The secret in the demo is a made-up string.
```text
$ actionlint unsafe.yml
unsafe.yml:9:36: "github.event.pull_request.title" is potentially untrusted. avoid using it directly in inline scripts. instead, pass it through an environment variable. see https://docs.github.com/en/actions/reference/security/secure-use#good-practices-for-mitigating-script-injection-attacks for more details [expression]
  |
9 |       - run: echo "PR title is ${{ github.event.pull_request.title }}"
  |                                    ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
unsafe.yml:12:34: "github.head_ref" is potentially untrusted. avoid using it directly in inline scripts. instead, pass it through an environment variable. see https://docs.github.com/en/actions/reference/security/secure-use#good-practices-for-mitigating-script-injection-attacks for more details [expression]
   |
12 |       - run: echo "branch is ${{ github.head_ref }}"
   |                                  ^~~~~~~~~~~~~~~
unsafe exit=1
$ actionlint safe.yml
safe exit=0
$ bash inject_demo.sh
--- unsafe: expression pasted into the script text
echo "PR title is x"; echo INJECTED-COMMAND-RAN; echo ""
PR title is x
INJECTED-COMMAND-RAN

--- safe: value passed as an environment variable
PR title is x"; echo INJECTED-COMMAND-RAN; echo "
$ python -I mask_demo.py
exact  -> token=***
base64 -> token=czNjcjN0LXRva2VuLTEyMw==
split  -> token=s3cr3t -token-123
```

**Follow-ups:**
- *Where do Docker build secrets go?* Part 2 owns that (build secrets, not `ARG`).
- *Secrets or OIDC?* Prefer OIDC for cloud access (Q6): there is no long-lived key to leak.
- *Self-hosted runners and secrets?* A job on a shared runner can leave files behind; use ephemeral runners that are thrown away after one job.

**Common mistakes:**
- Inlining `${{ secrets.X }}` in `run:`; it can land in the process list or logs.
- Believing masking protects encoded or partial secrets.
- Deleting the workflow run log after a leak and not rotating.
- Using tags (`@v3`) for third-party actions and trusting them forever.
- Default-wide token permissions on every workflow.

### Q6 ⭐⭐⭐ 🟡 OIDC from GitHub Actions to a cloud account instead of long-lived keys. Explain the flow (the job asks GitHub's OIDC provider for a short-lived JWT, which needs permissions id-token: write; the cloud validates the token and issues short-lived credentials), the claims that matter (iss, aud, sub such as repo:org/repo:environment:production, ref), why the trust policy must pin sub (an unpinned trust lets any repo assume the role), and the AWS example with aws-actions/configure-aws-credentials and role-to-assume, with Azure and GCP equivalents named at concept level. Write the workflow and a trust-policy JSON, validate the workflow with actionlint, and write a small Python matcher that tests sub patterns against sample claims (production, a feature branch, a fork). The real token exchange is not executed; Part 10 owns IAM depth.
**Asked at:** GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD | MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** With OIDC the job asks GitHub for a short-lived signed token, the cloud checks its claims against a trust policy and hands back short-lived credentials, so there is no stored cloud key; the trust policy must pin `sub` or any repo could assume your role.

**Then explain:**
- **Flow:** (1) job has `permissions: id-token: write`; (2) the action requests a JWT from GitHub's OIDC provider; (3) it calls the cloud's token service (on AWS, `AssumeRoleWithWebIdentity`) with that JWT; (4) the cloud verifies the signature and claims against the trust policy; (5) it returns credentials that expire. `id-token: write` only lets the job fetch a token. It grants no cloud access by itself.
- **Claims that matter:** `iss` (GitHub's token issuer), `aud` (the audience, e.g. `sts.amazonaws.com`), `sub` (who: `repo:ORG/REPO:environment:production`, or `...:ref:refs/heads/main`, or `...:pull_request`), plus `ref`, `repository`.
- **Pin `sub`:** if the trust policy only checks `aud`, or uses `repo:*`, any repository on GitHub can get a token that satisfies it. Pin the org, repo and, best, the **environment**, because environment protection rules (Q7) then gate who can assume the role.
- **Equivalents (concept level, check current docs):** Azure uses a federated identity credential on an app registration; GCP uses workload identity federation with a provider condition on the repository claim.
- **Failure modes:** missing `id-token: write` (the action cannot get a token); `sub` pattern too wide; role policy too wide even with a good trust policy; wrong `aud`; a reusable workflow changing the `sub` you expected (check current docs).
- Part 10 owns IAM depth.

**Example:** Trust policy pins `repo:acme/churn-model:environment:production`. The table below (from the matcher) shows who can assume the role under three policies. Only the production environment job passes the pinned policy. The repo-wide pattern lets feature branches and PR jobs in, and `repo:*` also lets another repo in.

**Code:**
Workflow YAML:
```yaml
name: deploy-prod
on:
  workflow_dispatch:
permissions:
  id-token: write       # lets the job REQUEST an OIDC token; grants no cloud access by itself
  contents: read
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/gha-model-deploy
          aws-region: ap-south-1
      - run: aws sts get-caller-identity
```

JSON:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"},
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {"token.actions.githubusercontent.com:aud": "sts.amazonaws.com"},
      "StringLike":   {"token.actions.githubusercontent.com:sub": "repo:acme/churn-model:environment:production"}
    }
  }]
}
```

Python:
```python
import json, fnmatch
policy = json.load(open("trust_policy.json"))
cond = policy["Statement"][0]["Condition"]
PIN = cond["StringLike"]["token.actions.githubusercontent.com:sub"]
AUD = cond["StringEquals"]["token.actions.githubusercontent.com:aud"]

def allowed(claims, sub_pattern, aud=AUD):
    # StringLike semantics: * and ? wildcards, case-sensitive
    return claims["aud"] == aud and fnmatch.fnmatchcase(claims["sub"], sub_pattern)

samples = {
  "prod deploy job":      {"aud": "sts.amazonaws.com", "sub": "repo:acme/churn-model:environment:production"},
  "feature branch job":   {"aud": "sts.amazonaws.com", "sub": "repo:acme/churn-model:ref:refs/heads/feature/x"},
  "PR job":               {"aud": "sts.amazonaws.com", "sub": "repo:acme/churn-model:pull_request"},
  "staging env job":      {"aud": "sts.amazonaws.com", "sub": "repo:acme/churn-model:environment:staging"},
  "other repo job":   {"aud": "sts.amazonaws.com", "sub": "repo:attacker/churn-model:environment:production"},
  "wrong audience":       {"aud": "sts.example.com",   "sub": "repo:acme/churn-model:environment:production"},
}
policies = {"pinned": PIN, "repo-wide": "repo:acme/churn-model:*", "unpinned": "repo:*"}
print(f"{'claims':22}" + "".join(f"{k:>10}" for k in policies))
for name, c in samples.items():
    print(f"{name:22}" + "".join(f"{('ALLOW' if allowed(c, p) else 'deny'):>10}" for p in policies.values()))
```

Shell (venv with actionlint-py, check-jsonschema, pytest, PyYAML on PATH):
```shell
actionlint deploy.yml; echo "actionlint exit=$?"
check-jsonschema --builtin-schema vendor.github-workflows deploy.yml
python -I -c "import json; json.load(open('trust_policy.json')); print('trust policy: valid JSON')"
python -I sub_matcher.py
```

**Output (my run):** Not executed: the real token exchange with GitHub and a cloud account (no cloud account, no runner). Real runs below: actionlint and check-jsonschema on the workflow, a JSON parse of the trust policy, and the Python matcher over sample claims (my own `fnmatch` imitation of StringLike wildcard matching, not the cloud's engine).
```text
$ actionlint deploy.yml
actionlint exit=0
$ check-jsonschema --builtin-schema vendor.github-workflows deploy.yml
ok -- validation done
$ python -I -c 'import json; json.load(open('\''trust_policy.json'\'')); print('\''trust policy: valid JSON'\'')'
trust policy: valid JSON
$ python -I sub_matcher.py
claims                    pinned repo-wide  unpinned
prod deploy job            ALLOW     ALLOW     ALLOW
feature branch job          deny     ALLOW     ALLOW
PR job                      deny     ALLOW     ALLOW
staging env job             deny     ALLOW     ALLOW
other repo job              deny      deny     ALLOW
wrong audience              deny      deny      deny
```

**Follow-ups:**
- *Why environment in `sub` instead of branch?* An environment can require approval, so the credential is only minted after a human says yes.
- *Is the token a secret?* It is short-lived and only useful with a matching policy, but do not log it.
- *Fork PRs?* They do not get an id-token to your cloud under normal rules; do not weaken that.

**Common mistakes:**
- Trust policy with only an `aud` condition.
- `repo:org/*` because "it is our org": any repo in it, including a throwaway one, can deploy to production.
- Forgetting `id-token: write`, then adding `write-all` to "fix" it.
- Long-lived keys kept "as a backup".
- Giving the assumed role admin rights.

### Q7 ⭐⭐⭐ 🟡 GitHub environments, required reviewers and deployment approvals for a model release. Explain environment: staging and production on a job, required reviewers, wait timer, deployment branch restrictions, environment-scoped secrets and variables, the point that protection rules are evaluated before the job starts and its secrets are unavailable until then, and the limits by plan (check current docs). Write a train, evaluate, deploy-to-staging, deploy-to-production workflow where production needs approval, validate it with actionlint, and explain what an approval does not prove (the reviewer must see the gate report, not just click).
**Asked at:** GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD | Continuous training and maturity-level write-ups (open-exam-prep.com MLOps CI/CD retraining guide, nerdleveltech.com MLOps maturity levels, resumelens.org, nicheelab.com Vertex AI pipelines, a Google Cloud 'MLOps: continuous delivery and automation pipelines' page named by the search tool but not shown; search snippets only, not opened; level numbering differs between secondary sources); study guides, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** Put `environment: production` on the deploy job and configure required reviewers in the repo settings; GitHub then pauses the job for approval before it starts, and only then releases that environment's secrets.

**Then explain:**
- **Environment:** a named target (`staging`, `production`) with its own protection rules, secrets and variables. A job opts in with `environment:`.
- **Rules:** required reviewers, a wait timer, and a restriction on which branches may deploy. They are evaluated **before** the job starts; until they pass, the job's environment secrets are not available. Availability of rules on private repos depends on the plan (check current docs).
- **Scoped secrets:** a production credential lives only in the `production` environment, so staging jobs and PR jobs cannot read it.
- **Pipeline shape:** train, evaluate (gate), deploy-staging, deploy-production with `needs` chaining them. Use `concurrency` so two releases do not overlap.
- **What approval does not prove:** the reviewer clicked, not that the model is good. Put the gate report in the job summary (`$GITHUB_STEP_SUMMARY`) and upload it as an artifact so the reviewer sees metrics, champion versus candidate, and the data version before approving. Record who approved (the deployment history shows it).
- **Failure modes:** the self-reviewer problem (the person who triggered the run approves it; check the "prevent self-review" setting in current docs); a typo in the environment name silently creates a new, unprotected environment (check current docs); approvals that expire while a run waits.

**Example:** Release run: `train` and `evaluate` run unattended and `evaluate` writes the gate table to the summary. `deploy-staging` runs with the staging environment. `deploy-production` waits; the reviewer reads the gate table, then approves; the job starts, gets production secrets, and moves the `champion` alias. If the reviewer rejects, the run stops and no production credential was ever exposed.

**Code:**
Workflow YAML:
```yaml
# ===== release.yml =====
name: model-release
on:
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: model-release
  cancel-in-progress: false
jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python train.py --out model.joblib
      - uses: actions/upload-artifact@v4
        with: {name: model, path: model.joblib}
  evaluate:
    needs: train
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with: {name: model}
      - run: python gate.py --candidate metrics.json --champion champion.json | tee gate_report.txt
      - run: cat gate_report.txt >> "$GITHUB_STEP_SUMMARY"     # reviewer sees this
      - uses: actions/upload-artifact@v4
        with: {name: gate-report, path: gate_report.txt}
  deploy-staging:
    needs: evaluate
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - run: python deploy.py --env staging --alias challenger
  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production            # required reviewers + branch rule are set in repo settings
      url: https://ml.example.com/churn
    steps:
      - run: python deploy.py --env production --alias champion

# ===== bad_env.yml =====
name: bad
on: workflow_dispatch
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      nme: production
    steps:
      - run: echo hi
```

Python:
```python
import yaml
wf = yaml.safe_load(open("release.yml"))
for name, job in wf["jobs"].items():
    env = job.get("environment")
    print(f"{name:18} needs={job.get('needs', '-')!s:16} environment={env['name'] if isinstance(env, dict) else env}")
```

Shell (venv with actionlint-py, check-jsonschema, pytest, PyYAML on PATH):
```shell
actionlint release.yml; echo "actionlint exit=$?"
check-jsonschema --builtin-schema vendor.github-workflows release.yml
python -I list_envs.py
actionlint bad_env.yml; echo "bad exit=$?"
```

**Output (my run):** Not executed here: a real GitHub runner, so none of these workflows ran on GitHub. The approval pause itself is a GitHub server feature and was not run. Real runs below: actionlint and check-jsonschema accept the release workflow; a PyYAML script lists which jobs carry an environment; a bad `environment` block (`nme:`) is rejected by actionlint.
```text
$ actionlint release.yml
actionlint exit=0
$ check-jsonschema --builtin-schema vendor.github-workflows release.yml
ok -- validation done
$ python -I list_envs.py
train              needs=-                environment=None
evaluate           needs=train            environment=None
deploy-staging     needs=evaluate         environment=staging
deploy-production  needs=deploy-staging   environment=production
$ actionlint bad_env.yml
bad_env.yml:6:5: name is missing in "environment" section [syntax-check]
  |
6 |     environment:
  |     ^~~~~~~~~~~~
bad_env.yml:7:7: unexpected key "nme" for "environment" section. expected one of "deployment", "name", "url" [syntax-check]
  |
7 |       nme: production
  |       ^~~~
bad exit=1
```

**Follow-ups:**
- *Staging automatically, production manually?* Yes: no reviewers on staging, reviewers on production.
- *Can the approval be bypassed?* Admins and workflow edits can change settings; limit who can edit workflows and use branch protection and code owners on `.github/workflows/` so the workflow file itself is protected.
- *Where does the alias move happen?* In the deploy step (registry, Q9, Q10), not by rebuilding the image.

**Common mistakes:**
- Approval with no evidence shown.
- Putting production secrets at repository level, so every job can read them.
- Environment name typos.
- Letting the same person trigger and approve.
- Assuming a `wait timer` is a security control; it is only a delay.

### Q8 ⭐⭐⭐ 🟡 Caching in GitHub Actions for ML CI: what to cache and what not to. Explain actions/cache with key and restore-keys, hashFiles on requirements or a lock file, the setup-python cache option, why a cache key that never changes serves stale wheels and a key that changes every run never hits, scoping (a cache saved on a PR branch is not visible to unrelated branches; check current docs), the repository cache size limit (check current docs), and why you should not cache models or datasets there (use the registry or DVC remote; Part 4). Write the workflow, then a Python script that computes a hashFiles-style key from a requirements file and show the key changing when a pin changes. Docker layer caching is Part 2; do not repeat it.
**Asked at:** GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Cache dependency downloads with a key built from the lockfile hash and a `restore-keys` fallback, and keep models and datasets out of the Actions cache.

**Then explain:**
- **`actions/cache`:** `path` (what to save), `key` (exact match), `restore-keys` (prefix fallbacks, restore an older cache and then save a new one under the new key). **`hashFiles('requirements.txt')`** makes the key change exactly when the file changes.
- **Easiest path:** `actions/setup-python` with `cache: pip` and `cache-dependency-path` does this for pip for you.
- **Bad keys:** a constant key (`pip-v1`) serves stale wheels forever, since a hit never re-saves. A key with the run id never hits. A good key changes with the dependency set only.
- **Scope:** as I understand it, a branch can restore caches made on itself or on its base or default branch, but not caches from unrelated sibling branches (check current docs). Repository cache storage is limited and old caches are evicted (check current docs for the size).
- **Do not cache:** models and datasets. They are large, evicted without warning, and a cache hit has no lineage. Use the model registry or a DVC remote (Part 4). Do not cache anything secret.
- **Failure modes:** a poisoned cache (anything that can write to a cache the default branch later restores can plant files, so keep untrusted code away from those caches); a cache restored on a different Python or OS version (put them in the key).
- Docker layer caching is Part 2.

**Example:** `requirements.txt` has three pins. The key is `pip-Linux-<hash>`. Run 2 reads the same file and gets the same key: cache hit. Bump scikit-learn from 1.5.2 to 1.6.0 and the hash, so the key, changes: a miss, so pip reinstalls, then saves the new cache. `restore-keys: pip-Linux-` could restore the old cache first so only the changed wheel downloads.

**Code:**
Workflow YAML:
```yaml
name: ci-cache
on: pull_request
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # Option A: let setup-python manage the pip cache (simple, keyed on the requirements file)
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: requirements.txt
      # Option B: explicit cache, for a tool setup-python does not know (here: ruff's cache)
      - uses: actions/cache@v4
        with:
          path: .ruff_cache
          key: ruff-${{ runner.os }}-${{ hashFiles('requirements.txt', 'pyproject.toml') }}
          restore-keys: |
            ruff-${{ runner.os }}-
      - run: pip install -r requirements.txt
      - run: ruff check . && pytest -m "not slow" -q
```

Python:
```python
import hashlib, pathlib, tempfile
def hash_files(paths):
    """hashFiles-style: sha256 of each file, then sha256 of the joined digests (sorted by path)."""
    outer = hashlib.sha256()
    for p in sorted(paths):
        outer.update(hashlib.sha256(pathlib.Path(p).read_bytes()).digest())
    return outer.hexdigest()
def key(os_name, paths):
    return f"pip-{os_name}-{hash_files(paths)[:12]}"

d = pathlib.Path(tempfile.mkdtemp(prefix="b7q08_", dir="/tmp/claude-0/b7_q01_10"))
req = d / "requirements.txt"
req.write_text("scikit-learn==1.5.2\nnumpy==2.0.2\npandas==2.2.3\n")
k1 = key("Linux", [req]); print("run 1      :", k1)
print("run 2 same :", key("Linux", [req]), "(hit)")
req.write_text("scikit-learn==1.5.2\nnumpy==2.0.2\npandas==2.2.3  \n")
print("whitespace :", key("Linux", [req]), "(miss: any byte change is a new key)")
req.write_text("scikit-learn==1.6.0\nnumpy==2.0.2\npandas==2.2.3\n")
k2 = key("Linux", [req]); print("pin bumped :", k2, "(miss -> fresh install)")
print("changed    :", k1 != k2)
print("stale key  : pip-Linux-v1 never changes -> old wheels forever")
print("noisy key  : pip-Linux-<run_id> changes every run -> never hits")
```

Shell (venv with actionlint-py, check-jsonschema, pytest, PyYAML on PATH):
```shell
actionlint cache.yml; echo "actionlint exit=$?"
check-jsonschema --builtin-schema vendor.github-workflows cache.yml
python -I cache_key.py
```

**Output (my run):** Not executed here: a real GitHub runner, so none of these workflows ran on GitHub. Cache save/restore on GitHub was not run. Real runs below: actionlint and check-jsonschema on the workflow, and a Python script that mimics the hashFiles idea (sha256 per file, then sha256 of the digests). It is not guaranteed to match GitHub's hash byte for byte; the point is only that the key changes when the file changes.
```text
$ actionlint cache.yml
actionlint exit=0
$ check-jsonschema --builtin-schema vendor.github-workflows cache.yml
ok -- validation done
$ python -I cache_key.py
run 1      : pip-Linux-8e29c22523e0
run 2 same : pip-Linux-8e29c22523e0 (hit)
whitespace : pip-Linux-886945d98da1 (miss: any byte change is a new key)
pin bumped : pip-Linux-53adf6aa3d16 (miss -> fresh install)
changed    : True
stale key  : pip-Linux-v1 never changes -> old wheels forever
noisy key  : pip-Linux-<run_id> changes every run -> never hits
```

**Follow-ups:**
- *Is pip's wheel cache enough?* It saves the download, not the build, so a source build is still slow. Pin wheels where you can.
- *Cache a conda env?* Possible, but key it on the lock file, and check how big it is against the limit.
- *Where do big model files go?* Registry or DVC remote, pulled by version.

**Common mistakes:**
- A constant key.
- Caching `~/.cache` wholesale, which can include tokens or huge model downloads.
- Treating the cache as storage that is always present; a miss must still work.
- Caching test data, then debugging with stale data.
- No OS or Python version in the key.

### Q9 ⭐⭐⭐ 🟡 CD for code versus CD for models. Explain why a model release has its own lifecycle: it can be retrained with no code change, its artifact (weights plus preprocessing) is separate from the serving image, and promotion should move a pointer (a registry alias or a config value) rather than rebuild the image. Compare three release paths (code-only change, model-only change, data-triggered retrain) in a table with the trigger, what is built, what is tested, what is deployed and who approves. Write a Python change-router that, given a list of changed paths, returns which pipelines to run (code CI, model CT, serving rebuild), with pytest cases, and run it.
**Asked at:** Continuous training and maturity-level write-ups (open-exam-prep.com MLOps CI/CD retraining guide, nerdleveltech.com MLOps maturity levels, resumelens.org, nicheelab.com Vertex AI pipelines, a Google Cloud 'MLOps: continuous delivery and automation pipelines' page named by the search tool but not shown; search snippets only, not opened; level numbering differs between secondary sources); study guides, not interview reports; MLOps and ML platform roles | MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** A model release is not a code release: the model can change with no commit, the weights are separate from the serving image, and promotion should move a pointer (an alias or config value) instead of rebuilding the image.

**Then explain:**
- **Code CD:** commit, build, test, ship an image. The artifact is the image.
- **Model CD:** the artifact is weights plus preprocessing, stored in a registry. The serving image is built once and loads `models:/churn@champion` at start (or on reload). A new model is a new registry version and an alias change, not a new image.
- **Why pointer promotion:** it is fast, it is reversible (point the alias back), it keeps the image tested, and it leaves an audit trail of who moved it and when.
- **Three paths:** see the table in the example.
- **Change router:** a small function maps changed paths to pipelines, so a docs edit runs nothing and a training config change runs CT but not a rebuild. Unknown paths fall back to the cheap code CI (fail safe).
- **Failure modes:** the model needs a new feature column that the image's code does not know about (model and code must be compatible, so test the pair); a dependency bump changes both; an alias move with no gate.

**Example:** | Path | Trigger | Built | Tested | Deployed | Approver |
|---|---|---|---|---|---|
| Code-only change | PR to main | image (if serving code changed) | lint, unit, data, smoke | image, via rollout | code reviewer |
| Model-only change (new hyperparameters, config) | PR to the config, or manual dispatch | model version in registry | smoke, full train, gate | alias move, no image build | model owner at the gate or environment |
| Data-triggered retrain | schedule, new-data dispatch, drift alert | model version in registry | gate against champion | alias move if the gate passes | automatic, or owner for risky models |

Router results in the output: `src/training/loss.py` plus a `.dvc` data pointer give `['code_ci', 'model_ct']`; `deploy/alias.yaml` alone gives `['promote_pointer']`.

**Code:**
Python:
```python
# ===== router.py =====
from fnmatch import fnmatch

# path pattern -> pipelines it triggers (first column of the table in the answer)
RULES = [
    ("docs/*",              set()),                                 # docs only: nothing
    ("*.md",                set()),
    ("src/serving/*",       {"code_ci", "serving_rebuild"}),        # API code: test + rebuild image
    ("Dockerfile",          {"code_ci", "serving_rebuild"}),
    ("requirements*.txt",   {"code_ci", "serving_rebuild", "model_ct"}),  # deps change both
    ("src/training/*",      {"code_ci", "model_ct"}),               # training code: retrain
    ("configs/train*.yaml", {"code_ci", "model_ct"}),
    ("data/*.dvc",          {"model_ct"}),                          # new data pointer: retrain, no code CI
    ("deploy/alias.yaml",   {"promote_pointer"}),                   # pointer move: no build at all
    ("src/*",               {"code_ci"}),
    ("tests/*",             {"code_ci"}),
]

def route(changed_paths):
    out = set()
    for p in changed_paths:
        for pattern, pipes in RULES:
            if fnmatch(p, pattern):
                out |= pipes
                break
        else:
            out.add("code_ci")          # unknown path: fail safe, run the cheap CI
    return sorted(out)

if __name__ == "__main__":
    import sys
    print(route(sys.argv[1:]))

# ===== test_router.py =====
from router import route

def test_docs_only_runs_nothing():
    assert route(["README.md", "docs/setup.md"]) == []

def test_code_only_change():
    assert route(["src/features.py", "tests/test_features.py"]) == ["code_ci"]

def test_serving_change_rebuilds_image():
    assert route(["src/serving/app.py"]) == ["code_ci", "serving_rebuild"]

def test_model_only_change_does_not_rebuild_image():
    r = route(["configs/train_churn.yaml"])
    assert "model_ct" in r and "serving_rebuild" not in r

def test_data_pointer_triggers_training_only():
    assert route(["data/train.csv.dvc"]) == ["model_ct"]

def test_alias_move_is_pointer_only():
    assert route(["deploy/alias.yaml"]) == ["promote_pointer"]

def test_dependency_bump_hits_everything():
    assert route(["requirements.txt"]) == ["code_ci", "model_ct", "serving_rebuild"]

def test_unknown_path_fails_safe():
    assert route(["weird/thing.bin"]) == ["code_ci"]

def test_mixed_change_unions():
    assert route(["src/training/loss.py", "src/serving/app.py"]) == ["code_ci", "model_ct", "serving_rebuild"]
```

Shell (venv with actionlint-py, check-jsonschema, pytest, PyYAML on PATH):
```shell
pytest -v -p no:cacheprovider
python -I router.py src/training/loss.py data/train.csv.dvc
python -I router.py deploy/alias.yaml
```

**Output (my run):** Real run below: 9 pytest cases for the router and two direct calls. Nothing here needs a GitHub runner; wiring the router into a workflow (a job that outputs the list for `if:` conditions, or `paths` filters) was not executed.
```text
$ pytest -v -p no:cacheprovider
============================= test session starts ==============================
platform linux -- Python 3.13.17, pytest-9.1.1, pluggy-1.7.0 -- /tmp/claude-0/b7p07/v/bin/python3
rootdir: /tmp/claude-0/b7_q01_10/work/q09
plugins: anyio-4.15.1
collecting ... collected 9 items

test_router.py::test_docs_only_runs_nothing PASSED                       [ 11%]
test_router.py::test_code_only_change PASSED                             [ 22%]
test_router.py::test_serving_change_rebuilds_image PASSED                [ 33%]
test_router.py::test_model_only_change_does_not_rebuild_image PASSED     [ 44%]
test_router.py::test_data_pointer_triggers_training_only PASSED          [ 55%]
test_router.py::test_alias_move_is_pointer_only PASSED                   [ 66%]
test_router.py::test_dependency_bump_hits_everything PASSED              [ 77%]
test_router.py::test_unknown_path_fails_safe PASSED                      [ 88%]
test_router.py::test_mixed_change_unions PASSED                          [100%]

============================== 9 passed in 0.03s ===============================
$ python -I router.py src/training/loss.py data/train.csv.dvc
['code_ci', 'model_ct']
$ python -I router.py deploy/alias.yaml
['promote_pointer']
```

**Follow-ups:**
- *Why not bake the model into the image?* Then every retrain is an image build and a rollout, and rollback is slower. Baking it is fine for small, rarely changed models.
- *How does the serving app learn about the new alias?* Reload on a signal or a schedule, or restart the pods (Part 6 and Part 3 own the rollout).
- *Can a data change trigger code CI?* Only if code is affected. Data goes through data tests and CT.

**Common mistakes:**
- One pipeline for everything, so every retrain rebuilds the image.
- Promoting by overwriting a file in object storage with no version or log.
- A router that skips tests for "unknown" paths instead of running the cheap ones.
- Forgetting that dependency changes affect both the image and the model.
- No compatibility test between the new model and the serving code.

### Q10 ⭐⭐⭐ 🟡 Promotion gates for a candidate model: design and implement. Explain an absolute floor (AUC at least 0.80), a relative rule against the current champion (no drop worse than 0.005), a latency and model-size budget, slice checks, a schema and signature check, and a rule for what happens when the champion has no metrics. Implement a gate script that reads two metrics JSON files, prints a pass or fail table with reasons, and exits non-zero on failure so a workflow step fails; give pytest cases for pass, regress and missing-metric. Run it. Part 1 covers the statistical bootstrap comparison on a fixed validation set; here the focus is the policy and the exit code in a pipeline.
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Model registry promotion write-ups (dataexpert.io champion-challenger guide, docs.zenml.io MLflow registry, towardsai MLflow series, an unofficial MLflow registry reference; search snippets only, not opened; the official MLflow docs were not opened and sources disagree on how deprecated stages are); editorial guides, not interview reports; MLOps and ML engineer roles
**Say this first (1 line):** A gate is a policy in code: an absolute floor, a no-regression rule against the champion, budgets, slice checks and a signature check, with missing metrics treated as a failure, and a non-zero exit code that fails the workflow step.

**Then explain:**
- **Floor:** AUC at least 0.80. Stops a model that is simply bad, even if the champion was also bad.
- **Relative:** candidate AUC may not be worse than the champion by more than 0.005. Stops silent decay of a good model over many small releases. (Part 1 covers the statistical comparison; here the focus is policy.)
- **Budgets:** p95 latency and model size must fit the serving plan. A model that wins on AUC and misses latency is still a fail.
- **Slices:** overall AUC can hide a slice that got worse (new users, a region). Check a floor per slice and a no-big-drop rule against the champion.
- **Signature and schema:** the candidate's input columns and types must match what serving sends.
- **No champion metrics:** decide the policy up front. My choice: fail closed, with an explicit `--allow-no-champion` for a first release, so a lost metrics file cannot wave a model through.
- **Missing candidate metric:** FAIL, never skip.
- **Exit code:** `sys.exit(1)` on any failure; the workflow step fails, later steps (promote) do not run. Print a table so a human can see why.
- The thresholds are example policy values, not benchmarks.

**Example:** | Case | Candidate AUC | Champion AUC | Result |
|---|---|---|---|
| good | 0.853 | 0.850 | PASS (drop -0.003, i.e. better) |
| regress | 0.830 | 0.850 | FAIL: drop 0.020 above max 0.005 (floor 0.80 still met) |
| missing | no `p95_ms` | 0.850 | FAIL: metrics present |
| no champion file | 0.853 | none | FAIL closed; PASS only with `--allow-no-champion` |

Hand check for the regress row: 0.850 minus 0.830 is 0.020, and 0.020 is more than 0.005.

**Code:**
Python:
```python
# ===== gate.py =====
#!/usr/bin/env python3
"""Promotion gate. Exit 0 = promote allowed, 1 = blocked. Thresholds are example policy values."""
import argparse, json, sys

POLICY = {"auc_floor": 0.80, "max_auc_drop": 0.005, "max_p95_ms": 50.0, "max_size_mb": 200.0,
          "slice_floor": 0.70, "max_slice_drop": 0.02}
REQUIRED = ["auc", "p95_ms", "size_mb", "slices", "signature"]

def load(path):
    try:
        with open(path) as f:
            return json.load(f) or None
    except FileNotFoundError:
        return None

def check(cand, champ, allow_no_champion=False, p=POLICY):
    rows = []                                     # (check, status, reason)
    def add(name, ok, why): rows.append((name, "PASS" if ok else "FAIL", why))
    missing = [k for k in REQUIRED if k not in (cand or {})]
    if missing:                                   # a missing metric is a failure, never a pass
        add("metrics present", False, "candidate missing: " + ", ".join(missing))
        return rows
    add("metrics present", True, "all required keys found")
    add("auc floor", cand["auc"] >= p["auc_floor"], f"{cand['auc']:.3f} vs floor {p['auc_floor']}")
    add("latency budget", cand["p95_ms"] <= p["max_p95_ms"], f"p95 {cand['p95_ms']} ms vs {p['max_p95_ms']}")
    add("size budget", cand["size_mb"] <= p["max_size_mb"], f"{cand['size_mb']} MB vs {p['max_size_mb']}")
    worst = min(cand["slices"].items(), key=lambda kv: kv[1])
    add("slice floor", worst[1] >= p["slice_floor"], f"worst slice {worst[0]}={worst[1]:.3f} vs {p['slice_floor']}")
    if champ is None or "auc" not in champ:
        ok = allow_no_champion
        add("champion metrics", ok, "none found; " + ("first release, relative checks skipped" if ok
                                                    else "fail closed (use --allow-no-champion for the first release)"))
        return rows
    drop = champ["auc"] - cand["auc"]
    add("vs champion auc", drop <= p["max_auc_drop"], f"drop {drop:+.3f} (max {p['max_auc_drop']})")
    for s, v in champ.get("slices", {}).items():
        d = v - cand["slices"].get(s, 0.0)
        if d > p["max_slice_drop"]:
            add(f"slice {s} vs champion", False, f"drop {d:+.3f} (max {p['max_slice_drop']})")
    add("signature", cand["signature"] == champ.get("signature"), "inputs match champion" if
        cand["signature"] == champ.get("signature") else f"{cand['signature']} != {champ.get('signature')}")
    return rows

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True); ap.add_argument("--champion", required=True)
    ap.add_argument("--allow-no-champion", action="store_true")
    a = ap.parse_args(argv)
    rows = check(load(a.candidate), load(a.champion), a.allow_no_champion)
    print(f"{'check':24}{'result':8}reason")
    for n, s, w in rows: print(f"{n:24}{s:8}{w}")
    failed = [r for r in rows if r[1] == "FAIL"]
    print("GATE:", "BLOCKED (%d failed)" % len(failed) if failed else "PASSED")
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())

# ===== test_gate.py =====
import json, subprocess, sys, pytest
from gate import check, main

CHAMP = {"auc": 0.85, "p95_ms": 40, "size_mb": 90, "slices": {"new_users": 0.78, "mobile": 0.82}, "signature": ["age", "tenure"]}
GOOD = {**CHAMP, "auc": 0.853}

def fails(rows): return [r[0] for r in rows if r[1] == "FAIL"]

def test_pass():
    assert fails(check(GOOD, CHAMP)) == []

def test_regress_vs_champion():
    assert fails(check({**GOOD, "auc": 0.83}, CHAMP)) == ["vs champion auc"]

def test_missing_metric_fails_closed():
    bad = {k: v for k, v in GOOD.items() if k != "p95_ms"}
    assert fails(check(bad, CHAMP)) == ["metrics present"]

def test_no_champion_fails_closed_unless_allowed():
    assert fails(check(GOOD, None)) == ["champion metrics"]
    assert fails(check(GOOD, None, allow_no_champion=True)) == []

def test_slice_regression_is_caught_even_if_overall_ok():
    cand = {**GOOD, "slices": {"new_users": 0.70, "mobile": 0.82}}   # overall fine, one slice dropped
    assert "slice new_users vs champion" in fails(check(cand, CHAMP))

def test_exit_code(tmp_path):
    c, h = tmp_path / "c.json", tmp_path / "h.json"
    h.write_text(json.dumps(CHAMP))
    c.write_text(json.dumps({**GOOD, "auc": 0.83}))
    assert main(["--candidate", str(c), "--champion", str(h)]) == 1
    c.write_text(json.dumps(GOOD))
    assert main(["--candidate", str(c), "--champion", str(h)]) == 0
```

Workflow YAML:
```yaml
name: gate-demo
on: workflow_dispatch
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Promotion gate (non-zero exit fails the job)
        run: python gate.py --candidate candidate.json --champion champion.json
      - name: Promote (runs only if the gate step passed)
        run: python promote.py --alias champion
```

Shell (venv with actionlint-py, check-jsonschema, pytest, PyYAML on PATH):
```shell
pytest -q -p no:cacheprovider
python -I gate.py --candidate candidate_pass.json --champion champion.json; echo "exit=$?"
python -I gate.py --candidate candidate_regress.json --champion champion.json; echo "exit=$?"
python -I gate.py --candidate candidate_missing.json --champion champion.json; echo "exit=$?"
python -I gate.py --candidate candidate_pass.json --champion no_such_file.json; echo "exit=$?"
python -I gate.py --candidate candidate_pass.json --champion no_such_file.json --allow-no-champion; echo "exit=$?"
actionlint gate_step.yml; echo "actionlint exit=$?"
```

**Output (my run):** Not executed here: a real GitHub runner, so none of these workflows ran on GitHub. Real runs below: 6 pytest cases, the CLI on four inputs with the exit code printed each time, and actionlint on a workflow step that runs the gate. The workflow itself was not run on GitHub; the exit-code behaviour (non-zero fails a step) is standard Actions behaviour and the script's exit codes were checked locally.
```text
$ pytest -q -p no:cacheprovider
......                                                                   [100%]
6 passed in 0.02s
$ python -I gate.py --candidate candidate_pass.json --champion champion.json
check                   result  reason
metrics present         PASS    all required keys found
auc floor               PASS    0.853 vs floor 0.8
latency budget          PASS    p95 38 ms vs 50.0
size budget             PASS    92 MB vs 200.0
slice floor             PASS    worst slice new_users=0.790 vs 0.7
vs champion auc         PASS    drop -0.003 (max 0.005)
signature               PASS    inputs match champion
GATE: PASSED
exit=0
$ python -I gate.py --candidate candidate_regress.json --champion champion.json
check                   result  reason
metrics present         PASS    all required keys found
auc floor               PASS    0.830 vs floor 0.8
latency budget          PASS    p95 38 ms vs 50.0
size budget             PASS    92 MB vs 200.0
slice floor             PASS    worst slice new_users=0.790 vs 0.7
vs champion auc         FAIL    drop +0.020 (max 0.005)
signature               PASS    inputs match champion
GATE: BLOCKED (1 failed)
exit=1
$ python -I gate.py --candidate candidate_missing.json --champion champion.json
check                   result  reason
metrics present         FAIL    candidate missing: p95_ms
GATE: BLOCKED (1 failed)
exit=1
$ python -I gate.py --candidate candidate_pass.json --champion no_such_file.json
check                   result  reason
metrics present         PASS    all required keys found
auc floor               PASS    0.853 vs floor 0.8
latency budget          PASS    p95 38 ms vs 50.0
size budget             PASS    92 MB vs 200.0
slice floor             PASS    worst slice new_users=0.790 vs 0.7
champion metrics        FAIL    none found; fail closed (use --allow-no-champion for the first release)
GATE: BLOCKED (1 failed)
exit=1
$ python -I gate.py --candidate candidate_pass.json --champion no_such_file.json --allow-no-champion
check                   result  reason
metrics present         PASS    all required keys found
auc floor               PASS    0.853 vs floor 0.8
latency budget          PASS    p95 38 ms vs 50.0
size budget             PASS    92 MB vs 200.0
slice floor             PASS    worst slice new_users=0.790 vs 0.7
champion metrics        PASS    none found; first release, relative checks skipped
GATE: PASSED
exit=0
$ actionlint gate_step.yml
actionlint exit=0
```

**Follow-ups:**
- *Should a failed gate block a hotfix?* Provide a documented override with a named approver, logged, not a quiet bypass.
- *Where do the metrics come from?* The evaluate job writes them next to the run; the champion's come from the registry (Part 4 owns tracking and registry basics).
- *Many slices, multiple tests?* Keep slices few and meaningful, and mind noise on small slices.

**Common mistakes:**
- Treating a missing metric as zero violations.
- Only an absolute floor, so a model decays one release at a time.
- Gate only on the overall metric.
- Exit code always 0 because the script prints "FAIL" but never calls `sys.exit(1)`.
- Gate thresholds living in someone's head instead of in code and review.

### Q11 ⭐⭐⭐ 🟡 Promote a model in CI with MLflow registry aliases. Explain the flow: the training job logs and registers a version, the gate passes, a promotion job moves the champion alias to that version, serving loads models:/name@champion, and the old version stays for rollback. Write the promotion script with MlflowClient on a local sqlite backend (idempotent, checks that the version exists and has the gate-passed tag, records who and which workflow run did it as tags) and show a workflow job that calls it. Run the script for real and print the alias before and after. Part 4 owns registry basics and governance; this question is about the automated promotion step. A real remote tracking server and authentication are not executed.
**Asked at:** Model registry promotion write-ups (dataexpert.io champion-challenger guide, docs.zenml.io MLflow registry, towardsai MLflow series, an unofficial MLflow registry reference; search snippets only, not opened; the official MLflow docs were not opened and sources disagree on how deprecated stages are); editorial guides, not interview reports; MLOps and ML engineer roles | MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** Promotion is just moving the `champion` alias to a version that already passed the gate; the script checks the version exists and carries `gate=passed`, does nothing if the alias is already there, and writes who and which run did it as tags.

**Then explain:**
- Flow: train job logs and registers a version, gate job tags it `gate=passed`, promotion job moves `champion`, serving loads `models:/churn@champion`, the old version is never deleted so rollback is one more alias move.
- Why an alias and not a rebuild: the alias is a pointer. Serving code and image stay the same. Check current MLflow docs for how stages are deprecated; I use aliases and tags only.
- The script refuses in three cases: version does not exist, version has no `gate=passed` tag, or the alias is already on that version (a no-op that exits 0, so a re-run of the workflow is safe).
- Audit: `promoted_by` (the `GITHUB_ACTOR`), `promoted_run` (a URL built from `GITHUB_REPOSITORY` and `GITHUB_RUN_ID`) and a UTC timestamp go on the version as tags. The previous champion gets a `replaced_by` tag.
- Failure modes: a tag is only a convention, so anyone with registry write access can set `gate=passed` by hand (lock down who may write tags). Serving must reload or restart to see a new alias target. Two promotions at once can race (see the concurrency answer).

**Example:** the registry has `churn` v1 (never gated) and v2 (tagged `gate=passed`). Promote v1: refused. Promote v99: refused. Promote v2: `champion` goes from unset to 2. Run it again: no-op. Hand check: only one of the three requests had both an existing version and the tag, so only one moves the alias.

**Code:** (one python block with the seed and promote scripts; one yaml block for the workflow; one bash block for the commands I ran)
```python
# ===== q11/seed.py =====
"""Seed a local sqlite registry with two versions of 'churn' (stand-in for the training job)."""
import sys, mlflow
from mlflow import MlflowClient
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression

uri = sys.argv[1]
mlflow.set_tracking_uri(uri)
mlflow.set_registry_uri(uri)
mlflow.set_experiment("churn-train")
X, y = make_classification(n_samples=200, n_features=5, random_state=0)
c = MlflowClient(uri)
for i, C in enumerate([0.1, 1.0], start=1):
    with mlflow.start_run():
        m = LogisticRegression(C=C, max_iter=200).fit(X, y)
        mlflow.sklearn.log_model(m, name="model", registered_model_name="churn")
# the gate marked version 2 as passed; version 1 was never gated
c.set_model_version_tag("churn", "2", "gate", "passed")
print("seeded", [(v.version, v.tags) for v in c.search_model_versions("name='churn'")])

# ===== q11/promote.py =====
"""Promote a registry version to an alias. Idempotent. Exit 0 ok, 2 refused."""
import argparse, os, sys, datetime
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException


def promote(client, name, version, alias="champion", who="unknown", run_url=""):
    try:
        mv = client.get_model_version(name, str(version))
    except MlflowException as e:
        return 2, f"REFUSED: version {version} of {name} not found ({e.error_code})"
    if mv.tags.get("gate") != "passed":
        return 2, f"REFUSED: version {version} has no gate=passed tag"
    try:
        cur = str(client.get_model_version_by_alias(name, alias).version)
    except MlflowException:
        cur = None
    if cur == str(version):
        return 0, f"NO-OP: {alias} already points at version {version}"
    client.set_registered_model_alias(name, alias, str(version))
    client.set_model_version_tag(name, str(version), "promoted_by", who)
    client.set_model_version_tag(name, str(version), "promoted_run", run_url)
    client.set_model_version_tag(name, str(version), "promoted_at",
                                 datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))
    if cur:
        client.set_model_version_tag(name, cur, "replaced_by", str(version))
    return 0, f"PROMOTED: {alias} {cur} -> {version}"


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--uri", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--version", required=True)
    a = p.parse_args()
    c = MlflowClient(a.uri, registry_uri=a.uri)
    who = os.environ.get("GITHUB_ACTOR", "local-user")
    run = os.environ.get("GITHUB_SERVER_URL", "https://github.com") + "/" + os.environ.get("GITHUB_REPOSITORY", "org/repo") \
        + "/actions/runs/" + os.environ.get("GITHUB_RUN_ID", "0")
    def show(tag):
        try:
            print(f"{tag}: champion -> v{c.get_model_version_by_alias(a.name, 'champion').version}")
        except MlflowException:
            print(f"{tag}: champion -> (unset)")
    show("before")
    code, msg = promote(c, a.name, a.version, who=who, run_url=run)
    print(msg)
    show("after")
    sys.exit(code)
```
```yaml
# ===== q11/promote.yml =====
name: promote-model
on:
  workflow_dispatch:
    inputs:
      version:
        description: Registry version to promote
        required: true
        type: string
concurrency:
  group: promote-churn
  cancel-in-progress: false
permissions:
  contents: read
jobs:
  promote:
    runs-on: ubuntu-latest
    environment: production
    env:
      MLFLOW_TRACKING_URI: ${{ vars.MLFLOW_TRACKING_URI }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install mlflow
      - name: Promote
        env:
          VERSION: ${{ inputs.version }}
        run: python promote.py --uri "$MLFLOW_TRACKING_URI" --name churn --version "$VERSION"
```
```bash
export MLFLOW_DISABLE_TELEMETRY=true
URI=sqlite:////tmp/claude-0/b7_q11_20/q11/m.db        # my own temp db
python3 -I seed.py $URI
python3 -I promote.py --uri $URI --name churn --version 1
python3 -I promote.py --uri $URI --name churn --version 99
GITHUB_ACTOR=asha GITHUB_RUN_ID=4242 GITHUB_REPOSITORY=acme/churn python3 -I promote.py --uri $URI --name churn --version 2
python3 -I promote.py --uri $URI --name churn --version 2
actionlint promote.yml
```

**Output (my run):** (mlflow 3.17.2, local sqlite registry; actionlint 1.7.12 printed nothing and exited 0 for `promote.yml`). The GitHub runner, the `production` environment approval, a remote tracking server and authentication are **not executed**; the workflow was only linted.
```text
$ python3 -I seed.py $URI
seeded [(2, {'gate': 'passed'}), (1, {})]

$ python3 -I promote.py --uri $URI --name churn --version 1   # never gated
before: champion -> (unset)
REFUSED: version 1 has no gate=passed tag
after: champion -> (unset)
exit=2

$ python3 -I promote.py --uri $URI --name churn --version 99
before: champion -> (unset)
REFUSED: version 99 of churn not found (RESOURCE_DOES_NOT_EXIST)
after: champion -> (unset)
exit=2

$ GITHUB_ACTOR=asha GITHUB_RUN_ID=4242 GITHUB_REPOSITORY=acme/churn python3 -I promote.py ... --version 2
before: champion -> (unset)
PROMOTED: champion None -> 2
after: champion -> v2
exit=0

$ same command again (idempotent)
before: champion -> v2
NO-OP: champion already points at version 2
after: champion -> v2
exit=0

$ read tags back
{'gate': 'passed', 'promoted_by': 'asha', 'promoted_run': 'https://github.com/acme/churn/actions/runs/4242', 'promoted_at': '<timestamp>'}
alias champion -> 2
```

**Follow-ups:**
- *Who may run this?* Put the job in a protected `production` environment with required reviewers and give only that environment the registry credential. Environment rules are GitHub settings that I could not run here; check current docs.
- *How do you make serving pick up the change?* Either restart or rollout the pods after promotion, or have the server re-resolve the alias on a timer. Pick one and test it.
- *Why not just a `gate` tag check in the registry itself?* Most registries do not enforce it. Treat the tag as a convention plus access control.

**Common mistakes:**
- Promoting by version number typed into a workflow input with no gate check.
- Deleting the old version "to save space" and losing the rollback target.
- Non-idempotent scripts that re-tag and re-notify on every re-run.
- Putting a long-lived registry token in a repository secret when the platform offers short-lived credentials.

### Q12 ⭐⭐⭐ 🟢 Roll back a bad model release. List the options (move the registry alias back, redeploy the previous image digest, flip blue-green traffic, git revert plus retrain) with the time each takes, what must still exist for rollback to work (the previous model artifact not deleted, a backward-compatible feature schema, the previous serving image), and why rollback must be tested before the incident. Implement an append-only promotion ledger (JSON lines) with a rollback function that restores the previous champion and records why, run it with pytest, and explain how a workflow_dispatch job with a version input would call it. Mechanics of rollout (canary, shadow) are Part 6 and Kubernetes rollbacks are Part 3.
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Model registry promotion write-ups (dataexpert.io champion-challenger guide, docs.zenml.io MLflow registry, towardsai MLflow series, an unofficial MLflow registry reference; search snippets only, not opened; the official MLflow docs were not opened and sources disagree on how deprecated stages are); editorial guides, not interview reports; MLOps and ML engineer roles
**Say this first (1 line):** The fastest rollback is moving the registry alias back, and I only trust it if I have rehearsed it, the old artifact still exists, and the old model still reads today's features.

**Then explain:**
- Options, roughly fastest to slowest (times are relative, they depend on your setup):

| Option | Speed | Needs to still exist |
|---|---|---|
| Move registry alias back | seconds to minutes, plus the time serving takes to reload | previous model version and its artifact |
| Redeploy previous image digest | minutes (rollout time) | previous image in the registry, pinned by digest |
| Flip blue-green traffic | seconds if the old stack is still running | old stack kept warm (costs money) |
| `git revert` plus retrain | hours | code, data version, compute |

- Rollback only works if the previous artifact is not deleted by a retention job, the feature schema is backward compatible (a model that needs a column the pipeline stopped producing cannot come back), and the previous serving image is still pullable.
- Rehearse it. A rollback path that was never run usually fails at the worst time: missing permission, alias name typo, stale cache in serving.
- Write an append-only ledger of every promotion and rollback: from, to, who, why, when. Rollback is then a new row, not an edit. The audit trail survives.
- Edge cases: "previous" is ambiguous after a rollback (my function uses the last different version, so rolling back twice toggles). An explicit target version avoids surprises. A rollback with no reason is refused. If the old artifact is gone, refuse and change nothing.
- Rollout mechanics (canary, shadow) belong to the serving part and Kubernetes rollbacks to the Kubernetes part. Here I only show the model-level step and how a manual workflow calls it.

**Example:** ledger rows say promote v1, v2, v3. Bad news at v3. `rollback --version 1` writes a fourth row (from 3, to 1, reason "v3 and v2 both bad") and `current()` is 1. The first three rows are untouched. Hand check: 3 promote rows plus 1 rollback row is 4 rows; my demo run below also did a second rollback, which is why the final count there is 5.

**Code:** (python block with the ledger and its tests; yaml block for the manual workflow; bash for the commands)
```python
# ===== q12/ledger.py =====
"""Append-only promotion ledger (JSON lines) with rollback. Pure python, no registry needed."""
import json, datetime, pathlib


def _now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def read(path):
    p = pathlib.Path(path)
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def current(path):
    rows = read(path)
    return rows[-1]["to"] if rows else None


def _append(path, row):
    with open(path, "a") as f:            # append only: never rewrite history
        f.write(json.dumps(row, sort_keys=True) + "\n")


def promote(path, version, who, reason="release"):
    row = {"ts": _now(), "action": "promote", "from": current(path), "to": str(version),
           "who": who, "reason": reason}
    _append(path, row)
    return row


def rollback(path, who, reason, exists=lambda v: True, target=None):
    """Restore the previous champion. 'exists' checks the old artifact is still there."""
    if not reason.strip():
        raise ValueError("rollback needs a reason")
    rows = read(path)
    cur = rows[-1]["to"] if rows else None
    # walk back to the last different version
    prev = str(target) if target else None
    for r in (reversed(rows) if prev is None else []):
        if r["to"] != cur:
            prev = r["to"]
            break
    if prev is None:
        raise RuntimeError("nothing to roll back to")
    if not exists(prev):
        raise RuntimeError(f"previous version {prev} no longer exists")
    row = {"ts": _now(), "action": "rollback", "from": cur, "to": prev, "who": who, "reason": reason}
    _append(path, row)
    return row


if __name__ == "__main__":
    import argparse, sys
    p = argparse.ArgumentParser()
    p.add_argument("--ledger", required=True)
    p.add_argument("--who", default="local")
    p.add_argument("--reason", required=True)
    p.add_argument("--version", default="")      # blank = previous champion
    a = p.parse_args()
    print(json.dumps(rollback(a.ledger, a.who, a.reason, target=a.version or None)))

# ===== q12/test_ledger.py =====
import pytest, ledger


def test_promote_then_rollback(tmp_path):
    f = tmp_path / "l.jsonl"
    ledger.promote(f, 1, "ci")
    ledger.promote(f, 2, "ci")
    assert ledger.current(f) == "2"
    r = ledger.rollback(f, "asha", "auc drop in prod")
    assert r["to"] == "1" and r["from"] == "2"
    assert ledger.current(f) == "1"
    assert len(ledger.read(f)) == 3          # history kept, nothing deleted


def test_rollback_needs_reason(tmp_path):
    f = tmp_path / "l.jsonl"
    ledger.promote(f, 1, "ci"); ledger.promote(f, 2, "ci")
    with pytest.raises(ValueError):
        ledger.rollback(f, "asha", "  ")


def test_nothing_to_roll_back(tmp_path):
    f = tmp_path / "l.jsonl"
    ledger.promote(f, 1, "ci")
    with pytest.raises(RuntimeError):
        ledger.rollback(f, "asha", "oops")


def test_missing_artifact_refuses(tmp_path):
    f = tmp_path / "l.jsonl"
    ledger.promote(f, 1, "ci"); ledger.promote(f, 2, "ci")
    with pytest.raises(RuntimeError, match="no longer exists"):
        ledger.rollback(f, "asha", "bad", exists=lambda v: False)
    assert ledger.current(f) == "2"          # failed rollback changes nothing


def test_second_rollback_goes_forward_again(tmp_path):
    # after 1,2 then rollback to 1, a second rollback returns to 2 (last different version)
    f = tmp_path / "l.jsonl"
    ledger.promote(f, 1, "ci"); ledger.promote(f, 2, "ci")
    ledger.rollback(f, "a", "x")
    r = ledger.rollback(f, "a", "undo")
    assert r["to"] == "2"


def test_explicit_target(tmp_path):
    f = tmp_path / "l.jsonl"
    for v in (1, 2, 3):
        ledger.promote(f, v, "ci")
    r = ledger.rollback(f, "a", "skip 2, it is bad too", target=1)
    assert r["to"] == "1" and ledger.current(f) == "1"
```
```yaml
# ===== q12/rollback.yml =====
name: rollback-model
on:
  workflow_dispatch:
    inputs:
      version:
        description: Registry version to restore (blank = previous champion)
        required: false
        type: string
      reason:
        description: Why we are rolling back
        required: true
        type: string
concurrency:
  group: promote-churn
  cancel-in-progress: false
permissions:
  contents: read
jobs:
  rollback:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Roll back
        env:
          VERSION: ${{ inputs.version }}
          REASON: ${{ inputs.reason }}
          ACTOR: ${{ github.actor }}
          MLFLOW_TRACKING_URI: ${{ vars.MLFLOW_TRACKING_URI }}
        run: |
          python ledger.py --ledger ledger.jsonl --who "$ACTOR" --reason "$REASON" --version "$VERSION"
```
```bash
pytest -q
python3 -I ledger.py --ledger l.jsonl --who asha --reason 'v3 and v2 both bad' --version 1
actionlint rollback.yml
```

**Output (my run):** (pytest 9.1.1, Python 3.13; actionlint exited 0). The `workflow_dispatch` run on GitHub and the `production` environment are **not executed**. In real use the same job also moves the registry alias (the promotion script from the previous question) and reloads serving; the ledger alone does not change any model.
```text
$ pytest -q
......                                                                   [100%]
6 passed in 0.03s

$ demo (promote 1,2,3 then CLI rollback with explicit --version 1)
champion now 3
{"ts": "2026-10-26T16:54:09+00:00", "action": "rollback", "from": "3", "to": "1", "who": "asha", "reason": "v3 and v2 both bad"}
{"ts": "2026-10-26T16:54:09+00:00", "action": "rollback", "from": "1", "to": "3", "who": "asha", "reason": "oops back"}
champion now 3 rows 5
```

**Follow-ups:**
- *How does the dispatch job get its input?* `workflow_dispatch` has typed `inputs`. The job passes `inputs.version` and `inputs.reason` through `env:` and the shell uses `"$VERSION"`, so user text never lands inside the script body.
- *Rollback to what if the previous model is also bad?* Pass an explicit older version, or switch to a rules-based fallback if you have one.
- *Does a rollback need approval?* Usually it needs less friction than a promotion, but it is still logged. Many teams allow on-call to roll back without a reviewer.

**Common mistakes:**
- Never testing the rollback.
- Artifact retention that deletes the old model after a few weeks.
- Rolling back the model but not the feature pipeline (or the other way round).
- Rewriting the ledger or the alias history instead of appending.

### Q13 ⭐⭐⭐ 🟡 Continuous training triggers and their guardrails. Compare schedule, new-data-arrival, drift or performance alerts, and code change as triggers, and explain guardrails: a minimum amount of new data, a cooldown so a noisy alert does not retrain hourly, a cost cap, and the rule that CT ends with a registered candidate that still passes the gate, not an automatic production deploy. Show a workflow with schedule and workflow_dispatch plus repository_dispatch for an alert, validate it with actionlint, and implement a trigger-decision function with a cooldown and tests, and run them. Part 8 owns drift detection and Part 5 owns pipeline orchestration.
**Asked at:** Continuous training and maturity-level write-ups (open-exam-prep.com MLOps CI/CD retraining guide, nerdleveltech.com MLOps maturity levels, resumelens.org, nicheelab.com Vertex AI pipelines, a Google Cloud 'MLOps: continuous delivery and automation pipelines' page named by the search tool but not shown; search snippets only, not opened; level numbering differs between secondary sources); study guides, not interview reports; MLOps and ML platform roles | MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** Continuous training should start from a trigger that passes guardrails (enough new data, a cooldown, a cost cap) and should end with a registered candidate that still has to pass the gate, never with an automatic production deploy.

**Then explain:**
- Triggers compared:

| Trigger | Good for | Risk |
|---|---|---|
| Schedule (cron) | simple safety net, predictable cost | retrains when nothing changed |
| New data arrives | data-driven refresh | tiny batches cause constant retrains |
| Drift or performance alert | reacts to real change | noisy alert means retrain storm |
| Code change | new features or fixes | this is normal CI, then training for a new model version |

- Guardrails: minimum new rows, cooldown since the last train, a weekly run budget, a `timeout-minutes` cap on the job. A manual run skips data and cooldown checks but still obeys the budget.
- CT ends at "register a candidate". A separate gated job promotes it. Auto-deploying a retrain removes the human and the gate exactly when the data is odd.
- GitHub details: `schedule` runs only on the default branch and can be delayed (check current docs); `repository_dispatch` lets an outside system (the monitoring tool) start the workflow with an event type; `workflow_dispatch` is the manual button. Keep the decision logic in a script so you can unit test it.
- Failure modes: an alert that fires hourly with no cooldown; a decide step that reads state from a file nobody updates (in real life read last-train time from the registry); a scheduled run that silently stops because the repository was inactive (check current docs on schedule auto-disable).
- Drift detection itself and pipeline orchestration are covered in other parts.

**Example:** the alert fires 2 hours after the last train: `go=false, cooldown: last train 2h ago, need 24h`. Same alert 6 days later with 9000 new rows: `go=true`. Hand check: 2 < 24 hours so blocked; 144 hours and 9000 >= 5000 rows so allowed.

**Code:** (yaml for the workflow; python for the decision function and tests; bash for the commands)
```yaml
# ===== q13/ct.yml =====
name: continuous-training
on:
  schedule:
    - cron: "17 2 * * 1"          # weekly safety net, Monday 02:17 UTC
  workflow_dispatch:
    inputs:
      reason:
        description: Why are we retraining by hand
        required: true
        type: string
  repository_dispatch:
    types: [drift-alert]          # sent by the monitoring system
concurrency:
  group: ct-churn
  cancel-in-progress: false
permissions:
  contents: read
jobs:
  decide:
    runs-on: ubuntu-latest
    outputs:
      go: ${{ steps.d.outputs.go }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - id: d
        env:
          EVENT: ${{ github.event_name }}
        run: python trigger.py --event "$EVENT" --state state.json >> "$GITHUB_OUTPUT"
  train:
    needs: decide
    if: needs.decide.outputs.go == 'true'
    runs-on: ubuntu-latest
    timeout-minutes: 120          # cost cap on one run
    steps:
      - uses: actions/checkout@v4
      - run: echo "train, evaluate, register a CANDIDATE. Promotion is a separate gated job."
```
```python
# ===== q13/trigger.py =====
"""Decide whether a retrain should start. Pure function plus a tiny CLI."""
import argparse, json, datetime as dt

MIN_NEW_ROWS = 5000
COOLDOWN_H = 24
MAX_RUNS_PER_WEEK = 3


def decide(event, new_rows, last_train, now, runs_last_7d, drift_alert=False):
    """Return (go, reason). last_train and now are datetimes."""
    if runs_last_7d >= MAX_RUNS_PER_WEEK:
        return False, "cost cap: weekly retrain budget used"
    if event == "workflow_dispatch":                      # a human decided, only the cost cap applies
        return True, "manual request"
    age_h = (now - last_train).total_seconds() / 3600 if last_train else None
    if age_h is not None and age_h < COOLDOWN_H:
        return False, f"cooldown: last train {age_h:.0f}h ago, need {COOLDOWN_H}h"
    if event == "repository_dispatch":
        if not drift_alert:
            return False, "dispatch without drift flag"
        if new_rows < MIN_NEW_ROWS:
            return False, f"only {new_rows} new rows, need {MIN_NEW_ROWS}"
        return True, "drift alert with enough fresh data"
    if event == "schedule":
        if new_rows < MIN_NEW_ROWS:
            return False, f"only {new_rows} new rows, need {MIN_NEW_ROWS}"
        return True, "scheduled run with enough fresh data"
    return False, f"event {event} does not retrain"


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--event", required=True)
    p.add_argument("--state", required=True)
    a = p.parse_args()
    s = json.load(open(a.state))
    now = dt.datetime.fromisoformat(s.get("now", dt.datetime.now(dt.timezone.utc).isoformat()))
    last = dt.datetime.fromisoformat(s["last_train"]) if s.get("last_train") else None
    go, why = decide(a.event, s["new_rows"], last, now, s["runs_last_7d"], s.get("drift_alert", False))
    print(f"go={'true' if go else 'false'}")
    print(f"why={why}")

# ===== q13/test_trigger.py =====
import datetime as dt
from trigger import decide

NOW = dt.datetime(2026, 10, 26, 12, tzinfo=dt.timezone.utc)
def ago(h): return NOW - dt.timedelta(hours=h)

def test_schedule_with_data():
    assert decide("schedule", 9000, ago(100), NOW, 0)[0] is True

def test_schedule_too_little_data():
    go, why = decide("schedule", 100, ago(100), NOW, 0)
    assert not go and "new rows" in why

def test_cooldown_blocks_noisy_alert():
    go, why = decide("repository_dispatch", 9000, ago(2), NOW, 1, drift_alert=True)
    assert not go and "cooldown" in why

def test_alert_after_cooldown():
    assert decide("repository_dispatch", 9000, ago(30), NOW, 1, drift_alert=True)[0]

def test_cost_cap_beats_manual():
    go, why = decide("workflow_dispatch", 0, ago(1), NOW, 3)
    assert not go and "cost cap" in why

def test_manual_ignores_cooldown():
    assert decide("workflow_dispatch", 0, ago(1), NOW, 0)[0]

def test_push_never_retrains():
    assert not decide("push", 99999, None, NOW, 0)[0]

def test_first_ever_run_has_no_cooldown():
    assert decide("schedule", 9000, None, NOW, 0)[0]
```
```bash
actionlint ct.yml
pytest -q
python3 -I trigger.py --event repository_dispatch --state state_noisy.json
python3 -I trigger.py --event repository_dispatch --state state_ok.json
# the PyYAML note: the key 'on' is parsed as the boolean True (YAML 1.1)
python3 -I -c "import yaml; d=yaml.safe_load(open('ct.yml')); print(list(d.keys()))"
```

**Output (my run):** (actionlint 1.7.12, pytest 9.1.1, PyYAML 6.0.3). Real scheduled and dispatched runs on GitHub are **not executed**. `state.json` in the workflow is a stand-in; the sample state files in my run are hand-written.
```text
$ actionlint ct.yml
exit=0

$ pytest -q
........                                                                 [100%]
8 passed in 0.01s

$ python3 -I trigger.py --event repository_dispatch --state state_noisy.json   # 2h after last train
go=false
why=cooldown: last train 2h ago, need 24h

$ python3 -I trigger.py --event repository_dispatch --state state_ok.json      # 6 days after
go=true
why=drift alert with enough fresh data

$ PyYAML view of the triggers
['name', True, 'concurrency', 'permissions', 'jobs']
dict_keys(['schedule', 'workflow_dispatch', 'repository_dispatch'])
```

**Follow-ups:**
- *How does the monitor send the event?* A POST to the GitHub API `dispatches` endpoint with `event_type: drift-alert` and a token. Check current docs for the exact token permission.
- *Where do you keep thresholds?* In versioned config in the repo, so a pull request changes them.
- *Why a cooldown if there is a data minimum?* A big backlog can satisfy the minimum every hour; the cooldown limits cost.

**Common mistakes:**
- Wiring an alert straight to "train and deploy".
- No cost cap and no `timeout-minutes`.
- Reading the workflow YAML with PyYAML and looking for the key `'on'`; it is `True`.
- Testing the decision logic only by waiting for cron.

### Q14 ⭐⭐⭐ 🟡 Build, scan and push a model-serving Docker image from GitHub Actions. Explain the job: checkout, docker/login-action to GHCR with GITHUB_TOKEN or to a cloud registry with OIDC, docker/metadata-action for tags (git SHA plus a semantic version), docker/build-push-action with push only on main, a vulnerability scan step with a severity policy that fails the build, and recording the image digest as a job output so deploys use the digest and not a mutable tag. Write the workflow, validate it with actionlint, and run what can run: docker CLI and buildx versions and a docker build attempt that fails with no daemon (show the real error). The real build, scan and push are not executed. Part 2 owns the Dockerfile, tags and scanning concepts.
**Asked at:** GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD | Actions supply-chain incident reports (orca.security, wiz.io, infoworld.com, phoenix.security, securityboulevard.com on the March 2025 tj-actions/changed-files compromise CVE-2025-30066; search snippets only, not opened; nothing found on SBOM or provenance attestations); security vendor posts, not interview reports; DevSecOps, platform and MLOps roles
**Say this first (1 line):** The job builds the image, scans it and fails on the severity policy, pushes only from main or a release tag, and passes the pushed image digest to the deploy job so I deploy `image@sha256:...` and not a mutable tag.

**Then explain:**
- Steps: checkout, `docker/setup-buildx-action`, `docker/login-action` (GHCR with `GITHUB_TOKEN` and `packages: write`, or a cloud registry with OIDC), `docker/metadata-action` for tags, `docker/build-push-action`.
- Tags: the git SHA (unique, traceable) plus a semantic version on release tags. `latest` is a moving target and I avoid deploying it.
- Push policy: `push: true` only when the event is not a pull request. PRs build and scan, which also means forks do not get registry credentials.
- Scan: build once with `load: true` into the runner, scan that image, fail with a non-zero exit on HIGH or CRITICAL (I use Trivy as the example; the action version I wrote is a placeholder, pin a version or SHA you have checked). Only then push. `ignore-unfixed` is a policy choice, say it out loud.
- Digest: the push step outputs `digest`; the job re-exports it as a job output; deploy uses `repo/churn-api@${DIGEST}`. A tag can be overwritten, a digest cannot refer to different content.
- Failure modes: scan job passes because the image scanned is not the image pushed (rebuilt differently); `digest` is empty on PRs (no push, so guard the deploy job); the cache (`type=gha`) can serve stale layers if the base image is not refreshed.
- Dockerfile, tag and scanning concepts belong to the Docker part; here it is just the Actions job.

**Example:** push to `main` at commit `ab12cd3`: image `ghcr.io/org/repo/churn-api:sha-ab12cd3` is pushed and the deploy job runs `...churn-api@sha256:<digest>`. A pull request builds and scans but skips login, push and deploy. Hand check: the `if: github.event_name != 'pull_request'` appears on login, push and deploy, three places.

**Code:** (yaml for the workflow; bash for what I could really run)
```yaml
# ===== q14/build-image.yml =====
name: build-serving-image
on:
  push:
    branches: [main]
    tags: ["v*"]
  pull_request:
    branches: [main]
permissions:
  contents: read
jobs:
  image:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write            # push to GHCR with GITHUB_TOKEN
    outputs:
      digest: ${{ steps.push.outputs.digest }}
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        if: github.event_name != 'pull_request'
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}/churn-api
          tags: |
            type=sha
            type=semver,pattern={{version}}
      - name: Build (no push) for scanning
        uses: docker/build-push-action@v6
        with:
          context: .
          load: true
          tags: churn-api:scan
          cache-from: type=gha
          cache-to: type=gha,mode=max
      - name: Scan, fail on HIGH or CRITICAL
        uses: aquasecurity/trivy-action@0.28.0
        with:
          image-ref: churn-api:scan
          severity: HIGH,CRITICAL
          exit-code: "1"
          ignore-unfixed: true
      - id: push
        name: Push (main and tags only)
        if: github.event_name != 'pull_request'
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
  deploy:
    needs: image
    if: github.event_name != 'pull_request'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - env:
          DIGEST: ${{ needs.image.outputs.digest }}
        run: echo "deploy ghcr.io/${{ github.repository }}/churn-api@${DIGEST}"
```
```bash
actionlint build-image.yml
check-jsonschema --builtin-schema vendor.github-workflows build-image.yml
docker --version
docker buildx version
docker build -t churn-api:scan .        # expected to fail here: no daemon
```

**Output (my run):** (actionlint 1.7.12, check-jsonschema 0.38.2, docker CLI 29.9.2 with buildx v0.38.1). The real image build, the Trivy scan, login and push to GHCR, and the digest handoff are **not executed** (no Docker daemon, no registry, no GitHub runner). The validation that did run is the workflow lint and schema check, plus the real daemon error below.
```text
$ actionlint build-image.yml
exit=0

$ check-jsonschema --builtin-schema vendor.github-workflows build-image.yml
ok -- validation done
exit=0

$ docker --version
Docker version 29.9.2, build a82e528
$ docker buildx version
github.com/docker/buildx v0.38.1 0dbe87f36ed472fe36b6796c3f70b4210a731fc5

$ docker build -t churn-api:scan .
ERROR: failed to connect to the docker API at unix:///var/run/docker.sock; check if the path is correct and if the daemon is running: dial unix /var/run/docker.sock: connect: no such file or directory
```

**Follow-ups:**
- *OIDC to a cloud registry instead of a token?* Add `id-token: write` and a cloud login action; the cloud trust policy should check the `sub` claim. Check current docs; not executed here.
- *Sign the image?* Add a signing step such as cosign, keyless, and keep SBOM output. Not executed here; check current docs.
- *Why scan before push?* A failing scan then leaves no vulnerable tag in the registry.

**Common mistakes:**
- Pushing on pull requests from forks.
- Deploying by tag, so a re-push changes what runs.
- Pinning actions by a moving tag (`@v3`) only, when a SHA pin would protect from a rewritten tag.
- Scanning one build and pushing another.

### Q15 ⭐⭐⭐ 🟡 Semantic versioning for models and for data. Explain what MAJOR, MINOR and PATCH mean for a model contract (input schema or output meaning changes is MAJOR, retrain on new data with the same contract is MINOR or PATCH by policy, a bug fix in preprocessing is PATCH), why the data version is a separate identifier (a dataset hash or date) recorded next to the model version, and a composite release identifier such as 2.3.1+data.20261001.git.ab12cd3. Write a script that decides the bump from a list of change labels, tags a temp git repository with git tag -a, and shows git describe and version-sorted tags; run it and show the output. Part 1 covers versioning a Python package; here it is the model and data contract.
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** I version the model contract with MAJOR.MINOR.PATCH (input or output meaning change is MAJOR), keep the data version as a separate id, and join them into one release id so I can trace any prediction back to model, data and code.

**Then explain:**
- MAJOR: input schema changes or output meaning changes (callers must change). MINOR: retrain on new data with the same contract, or a new optional feature or field (my policy, write yours down). PATCH: a preprocessing bug fix or threshold tweak that keeps the contract.
- Data version is its own identifier (a dataset hash or a date like `20261001`). Two models with the same code can differ only by data, so the data id sits next to the model version, not inside the MAJOR.MINOR.PATCH number.
- Composite release id: `2.3.1+data.20261001.git.ab12cd3`. In semver, text after `+` is build metadata and is ignored when comparing versions; that is what I want, since data and commit say where it came from, not which is newer.
- Rule of thumb for the bump: the highest-impact label wins. No label means no release (refuse). An unknown label is an error, not a guess.
- Tag in git with an annotated tag (`git tag -a`) so the message records the release id. `git describe --tags` then gives `model-v2.0.0` at the tag and `model-v2.0.0-1-g<sha>` one commit later.
- Failure modes: sorting tags as strings puts `1.10.0` before `1.2.0` (use `--sort=v:refname`); two teams use different rules for "retrain is MINOR or PATCH"; a schema change shipped as MINOR breaks callers.
- Package versioning for a Python library is in the first part; this is the model and data contract.

**Example:** start at `0.0.0`. Labels `input-schema-change` gives 1.0.0. `retrain-new-data` gives 1.1.0, then 1.2.0. `preprocessing-bugfix` gives 1.2.1. A release with both `input-schema-change` and `retrain-new-data` gives 2.0.0. Hand check: MAJOR resets minor and patch to 0.

**Code:** (python block with the bump script and tests; bash block for the git demo)
```python
# ===== q15/bump.py =====
"""Decide a model version bump from change labels, tag a git repo, build a composite release id."""
import subprocess, sys, re, datetime

MAJOR = {"input-schema-change", "output-meaning-change", "label-set-change"}
MINOR = {"retrain-new-data", "new-optional-feature", "new-output-field"}
PATCH = {"preprocessing-bugfix", "threshold-tweak", "metadata-fix"}


def bump(version, labels):
    unknown = set(labels) - MAJOR - MINOR - PATCH
    if unknown:
        raise ValueError(f"unknown labels: {sorted(unknown)}")
    major, minor, patch = map(int, version.split("."))
    if set(labels) & MAJOR:
        return f"{major + 1}.0.0"
    if set(labels) & MINOR:
        return f"{major}.{minor + 1}.0"
    if set(labels) & PATCH:
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError("no labels: refuse to release")


def release_id(version, data_version, sha):
    return f"{version}+data.{data_version}.git.{sha}"


def git(*a, cwd):
    return subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def latest(cwd):
    tags = git("tag", "--list", "model-v*", "--sort=-v:refname", cwd=cwd).splitlines()
    return re.sub(r"^model-v", "", tags[0]) if tags else "0.0.0"


if __name__ == "__main__":
    repo, data_version = sys.argv[1], sys.argv[2]
    labels = sys.argv[3:]
    cur = latest(repo)
    new = bump(cur, labels)
    sha = git("rev-parse", "--short=7", "HEAD", cwd=repo)
    rid = release_id(new, data_version, sha)
    git("tag", "-a", f"model-v{new}", "-m", f"release {rid}; labels={','.join(labels)}", cwd=repo)
    print(f"{cur} + {labels} -> {new}   id={rid}")

# ===== q15/test_bump.py =====
import pytest
from bump import bump, release_id

def test_major_wins(): assert bump("2.3.1", ["retrain-new-data", "input-schema-change"]) == "3.0.0"
def test_minor():      assert bump("2.3.1", ["retrain-new-data"]) == "2.4.0"
def test_patch():      assert bump("2.3.1", ["preprocessing-bugfix"]) == "2.3.2"
def test_no_labels():
    with pytest.raises(ValueError): bump("1.0.0", [])
def test_unknown_label():
    with pytest.raises(ValueError): bump("1.0.0", ["vibes"])
def test_release_id(): assert release_id("2.3.1", "20261001", "ab12cd3") == "2.3.1+data.20261001.git.ab12cd3"
```
```bash
pytest -q
git init -q -b main repo
# for each release: commit a change, then
python3 -I bump.py repo 20261001 retrain-new-data
git -C repo tag --sort=-v:refname
git -C repo describe --tags
git -C repo tag -n1 model-v1.1.0
git -C repo tag --sort=refname        # string order
git -C repo tag --sort=v:refname      # version order
```

**Output (my run):** (git 2.43.0, pytest 9.1.1; temp repo, the commit shas are real from my run). Only the local git tagging is real; a registry or a GitHub Release carrying these ids is **not executed**.
```text
$ pytest -q
......                                                                   [100%]
6 passed in 0.01s

$ release 1: first model, label input-schema-change
0.0.0 + ['input-schema-change'] -> 1.0.0   id=1.0.0+data.20260901.git.1906d7f
$ release 2: retrain on new data
1.0.0 + ['retrain-new-data'] -> 1.1.0   id=1.1.0+data.20261001.git.ee5f524
$ release 3: retrain again
1.1.0 + ['retrain-new-data'] -> 1.2.0   id=1.2.0+data.20261015.git.7a5d364
$ release 4: preprocessing bug fix
1.2.0 + ['preprocessing-bugfix'] -> 1.2.1   id=1.2.1+data.20261015.git.6d8dcb5
$ release 5: new input column plus retrain
1.2.1 + ['input-schema-change', 'retrain-new-data'] -> 2.0.0   id=2.0.0+data.20261020.git.27cfb98

$ git tag --sort=-v:refname
model-v2.0.0
model-v1.2.1
model-v1.2.0
model-v1.1.0
model-v1.0.0
$ git describe --tags  (at HEAD)
model-v2.0.0
$ git describe --tags  (one commit later)
model-v2.0.0-1-g<sha>
$ git tag -n1 model-v1.1.0
model-v1.1.0    release 1.1.0+data.20261001.git.ee5f524; labels=retrain-new-data

--- why sort by version, not by name: add a throw-away tag model-v1.10.0
$ git tag --sort=refname | head -4
model-v1.0.0
model-v1.1.0
model-v1.10.0
model-v1.2.0
$ git tag --sort=v:refname | head -4
model-v1.0.0
model-v1.1.0
model-v1.2.0
model-v1.2.1
Deleted tag 'model-v1.10.0' (was b86e966)
```

**Follow-ups:**
- *Where does the id go?* In the registry version tags, in the serving response header or log line, and in the image label.
- *Is a retrain MINOR or PATCH?* By policy. I would say MINOR when metrics change and PATCH when only a bug fix. Say which and keep it consistent.
- *Do you use CalVer?* Some teams do for data (date-based ids). It is fine for data; I keep semver for the contract.

**Common mistakes:**
- Using one number for model, data and code.
- Bumping PATCH for an input column change.
- Comparing versions as strings.
- Lightweight tags with no message, so nobody knows why the release happened.

### Q16 ⭐⭐ 🟡 Reusable workflows versus composite actions for sharing ML CI across many repositories. Explain workflow_call with inputs, secrets (and secrets: inherit), outputs, calling with uses: org/repo/.github/workflows/ml-ci.yml@v1, versus a composite action that bundles steps inside one job, the differences (own jobs and runners versus the caller's job; nesting limits and access rules, check current docs), and versioning the shared workflow by tag or SHA so a change does not break 20 repositories at once. Write a reusable workflow and a caller, validate both with actionlint and check-jsonschema, and show the real output.
**Asked at:** GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD | MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** A reusable workflow is a whole job (or jobs) that other repositories call with `uses:` at job level; a composite action is a bundle of steps that runs inside the caller's job; for shared ML CI I use a reusable workflow and pin callers to a tag or SHA.

**Then explain:**
- Reusable workflow: `on: workflow_call` with typed `inputs`, declared `secrets` and `outputs`. Called as `uses: org/repo/.github/workflows/ml-ci.yml@v1`. It gets its own jobs and its own runners. `secrets: inherit` passes the caller's secrets along (fine inside one org, risky across trust boundaries).
- Composite action: `action.yml` with `runs: using: composite` and a list of steps. It runs inside the caller's job, shares the filesystem and runner, and is called with `uses:` as a step. Good for small repeated steps like "set up Python and install".
- Differences to say out loud: reusable = own job and runner, can take secrets and give outputs, shows as a separate job in the UI. Composite = same job, no own runner. Nesting depth limits and access rules for private or cross-repo reuse exist; the numbers differ between sources, so check current docs.
- Versioning: callers use `@v1` (a moving major tag you own) or a full commit SHA. A branch ref like `@main` means one bad merge breaks every repository at once. Cut `v1.2.0`, move `v1` after a canary repo has passed.
- Failure modes: a typo in an input name (actionlint catches it for same-repo callees, see output); a missing required secret; the shared repo not allowing access from callers (a repo setting, check current docs).
- What each tool checked: actionlint read both files, and it resolved the local callee to find the wrong input name. check-jsonschema (vendored GitHub workflow schema) only checks the shape of each file, so it passed the bad caller.

**Example:** twenty repos call `ml-ci.yml@v1`. You fix a bug and move `v1` to the new commit: all twenty get the fix on their next run. If the fix was wrong, you move `v1` back. If they had used `@main`, the bad commit would have hit all twenty immediately.

**Code:** (one yaml block with the three valid files and one deliberately bad caller; bash for the checks)
```yaml
# ===== q16/.github/workflows/ml-ci.yml =====
name: ml-ci (reusable)
on:
  workflow_call:
    inputs:
      python-version:
        description: Python version for the test job
        required: false
        type: string
        default: "3.12"
      test-path:
        required: false
        type: string
        default: tests/
    secrets:
      MLFLOW_TOKEN:
        required: false
    outputs:
      coverage:
        description: Coverage percent from the test job
        value: ${{ jobs.test.outputs.coverage }}
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    outputs:
      coverage: ${{ steps.cov.outputs.pct }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}
          cache: pip
      - run: pip install -r requirements.txt pytest pytest-cov
      - env:
          TEST_PATH: ${{ inputs.test-path }}
        run: pytest "$TEST_PATH" --cov=src --cov-report=term
      - id: cov
        run: echo "pct=87" >> "$GITHUB_OUTPUT"      # placeholder: parse the real report here

# ===== q16/.github/workflows/caller.yml =====
name: churn-ci
on:
  pull_request:
jobs:
  ci:
    uses: acme-ml/shared-workflows/.github/workflows/ml-ci.yml@v1
    with:
      python-version: "3.11"
    secrets: inherit
  report:
    needs: ci
    runs-on: ubuntu-latest
    steps:
      - run: echo "coverage was ${{ needs.ci.outputs.coverage }}"

# ===== q16/.github/workflows/caller-local.yml =====
name: churn-ci-local
on:
  pull_request:
jobs:
  ci:
    uses: ./.github/workflows/ml-ci.yml
    with:
      python-version: "3.11"
    secrets: inherit

# ===== q16/bad-caller.yml =====
name: bad
on: pull_request
jobs:
  ci:
    uses: ./.github/workflows/ml-ci.yml
    with:
      python_version: "3.11"
```
```bash
git init -q .                 # actionlint finds the project root through .git
cp bad-caller.yml .github/workflows/bad-caller.yml
actionlint .github/workflows/ml-ci.yml .github/workflows/caller.yml .github/workflows/caller-local.yml
actionlint .github/workflows/bad-caller.yml
check-jsonschema --builtin-schema vendor.github-workflows .github/workflows/ml-ci.yml .github/workflows/caller.yml .github/workflows/caller-local.yml
check-jsonschema --builtin-schema vendor.github-workflows .github/workflows/bad-caller.yml
```

**Output (my run):** (actionlint 1.7.12, check-jsonschema 0.38.2). The remote `uses: acme-ml/shared-workflows/...@v1` in `caller.yml` cannot be resolved here, and a real call on GitHub is **not executed**. I linted the same shape with the local path form (`caller-local.yml`).
```text
$ actionlint .github/workflows/ml-ci.yml .github/workflows/caller.yml .github/workflows/caller-local.yml
exit=0

$ actionlint .github/workflows/bad-caller.yml   # passes python_version, callee declares python-version
.github/workflows/bad-caller.yml:7:7: input "python_version" is not defined in "./.github/workflows/ml-ci.yml" reusable workflow. defined inputs are "python-version", "test-path" [workflow-call]
  |
7 |       python_version: "3.11"
  |       ^~~~~~~~~~~~~~~
exit=1

$ check-jsonschema --builtin-schema vendor.github-workflows (3 good files)
ok -- validation done
exit=0

$ check-jsonschema on bad-caller.yml
ok -- validation done
exit=0
```

**Follow-ups:**
- *Can a reusable workflow call another?* Yes with a depth limit (check current docs).
- *Matrix with reusable workflows?* A caller job can use `strategy.matrix` and pass values as inputs.
- *Where do secrets go?* Declare only the ones the callee needs, instead of `inherit`, when the callee lives in another team's repo.

**Common mistakes:**
- Pinning callers to `@main`.
- Using `secrets: inherit` across a trust boundary.
- Expecting a composite action to get its own runner or its own `secrets:` input.
- Declaring `inputs` but passing `with:` keys with a different spelling (`python_version` vs `python-version`).

### Q17 ⭐⭐ 🟡 Matrix builds for ML CI: Python versions, library versions and operating systems. Explain strategy.matrix, include and exclude, fail-fast, max-parallel, how a matrix multiplies cost, testing the lowest and highest supported scikit-learn or torch versions, and why a GPU job should not be in the default matrix. Write the workflow, validate it with actionlint, and write a script that expands the matrix with include and exclude rules, prints each job and the total count, and show the count changing when one axis is added. Run it.
**Asked at:** GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** `strategy.matrix` makes one job per combination of axes, so cost multiplies; I test the lowest and highest supported library versions, not every combination, and keep GPU jobs out of the default matrix.

**Then explain:**
- Axes multiply: 2 OS x 2 Python x 2 scikit-learn = 8 jobs. `exclude` removes combinations. `include` adds a combination, or adds extra keys to matching ones (like a `run_slow` flag).
- `fail-fast: true` (default) cancels the other jobs when one fails; for a compatibility matrix I set `false` to see every failure. `max-parallel` caps how many run at once, which helps shared runners.
- Pick the corners: lowest and highest supported versions of scikit-learn or torch, oldest and newest Python. The middle versions rarely find anything new.
- Cost: every extra axis value doubles or triples the minutes. Windows and macOS runners have different billing rules; check current docs.
- GPU jobs: scarce, slow to start and expensive when idle. Run them on a separate workflow or a nightly schedule on a labelled runner (see the self-hosted runner answer), not on every PR in the matrix.
- Failure modes: an `include` entry that does not match any combination becomes its own extra job; a version string like `3.10` written without quotes in YAML becomes the number `3.1`.
- My expander script follows the simple rule: include entries whose axis values match existing combinations add their extra keys, otherwise they become new jobs. GitHub has finer rules for edge cases; check current docs.

**Example:** as written: 2 x 2 x 2 = 8, minus the excluded `windows + 3.10` pair (2 jobs, one per scikit-learn value) = 6 jobs; the `include` only adds `run_slow` to one of them. Add a `numpy: [1.26, 2.1]` axis: 16 - 4 = 12 jobs. Hand check matches the script output.

**Code:** (yaml for the workflow; python for the expander and tests; bash for the commands)
```yaml
# ===== q17/matrix.yml =====
name: ml-matrix
on:
  pull_request:
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      max-parallel: 4
      matrix:
        os: [ubuntu-latest, windows-latest]
        python: ["3.10", "3.12"]
        sklearn: ["1.3.2", "1.6.1"]
        exclude:
          - os: windows-latest
            python: "3.10"
        include:
          - os: ubuntu-latest
            python: "3.12"
            sklearn: "1.6.1"
            run_slow: true
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
          cache: pip
      - run: pip install "scikit-learn==${{ matrix.sklearn }}" pytest
      - run: pytest -q
```
```python
# ===== q17/expand.py =====
"""Expand a GitHub Actions strategy.matrix (axes + exclude + include) and count jobs."""
import itertools, sys, yaml


def expand(matrix):
    m = dict(matrix)
    include = m.pop("include", [])
    exclude = m.pop("exclude", [])
    axes = list(m)
    combos = [dict(zip(axes, vals)) for vals in itertools.product(*[m[a] for a in axes])] if axes else []
    combos = [c for c in combos if not any(all(c.get(k) == v for k, v in e.items()) for e in exclude)]
    for inc in include:
        # simplified include rule: an entry whose axis values match existing combos adds its extra keys to them
        matched = [c for c in combos if all(c[k] == v for k, v in inc.items() if k in axes)]
        if matched:
            for c in matched:
                c.update({k: v for k, v in inc.items() if k not in axes})
        else:
            combos.append(dict(inc))          # no combo matched: becomes its own new job
    return combos


def show(title, matrix):
    jobs = expand(matrix)
    print(f"== {title}: {len(jobs)} jobs")
    for j in jobs:
        print("  ", j)


if __name__ == "__main__":
    wf = yaml.safe_load(open(sys.argv[1]))
    mx = wf["jobs"]["test"]["strategy"]["matrix"]
    show("as written", mx)
    more = dict(mx); more["numpy"] = ["1.26", "2.1"]
    show("add one axis (numpy x2)", more)

# ===== q17/test_expand.py =====
from expand import expand

def test_plain_product():
    assert len(expand({"a": [1, 2], "b": [1, 2, 3]})) == 6

def test_exclude():
    assert len(expand({"a": [1, 2], "b": [1, 2], "exclude": [{"a": 1, "b": 1}]})) == 3

def test_include_extends_existing():
    jobs = expand({"a": [1, 2], "include": [{"a": 1, "extra": "x"}]})
    assert len(jobs) == 2 and jobs[0]["extra"] == "x" and "extra" not in jobs[1]

def test_include_new_combo():
    assert len(expand({"a": [1, 2], "include": [{"a": 3}]})) == 3
```
```bash
actionlint matrix.yml
pytest -q
python3 -I expand.py matrix.yml
```

**Output (my run):** (actionlint 1.7.12, pytest 9.1.1, PyYAML 6.0.3). The workflow on real GitHub runners, the real pip installs and the Windows jobs are **not executed**; the version pins in the YAML are examples and I did not check that each wheel exists for each Python.
```text
$ actionlint matrix.yml
exit=0

$ pytest -q
....                                                                     [100%]
4 passed in 0.02s

$ python3 -I expand.py matrix.yml
== as written: 6 jobs
   {'os': 'ubuntu-latest', 'python': '3.10', 'sklearn': '1.3.2'}
   {'os': 'ubuntu-latest', 'python': '3.10', 'sklearn': '1.6.1'}
   {'os': 'ubuntu-latest', 'python': '3.12', 'sklearn': '1.3.2'}
   {'os': 'ubuntu-latest', 'python': '3.12', 'sklearn': '1.6.1', 'run_slow': True}
   {'os': 'windows-latest', 'python': '3.12', 'sklearn': '1.3.2'}
   {'os': 'windows-latest', 'python': '3.12', 'sklearn': '1.6.1'}
== add one axis (numpy x2): 12 jobs
   {'os': 'ubuntu-latest', 'python': '3.10', 'sklearn': '1.3.2', 'numpy': '1.26'}
   {'os': 'ubuntu-latest', 'python': '3.10', 'sklearn': '1.3.2', 'numpy': '2.1'}
   {'os': 'ubuntu-latest', 'python': '3.10', 'sklearn': '1.6.1', 'numpy': '1.26'}
   {'os': 'ubuntu-latest', 'python': '3.10', 'sklearn': '1.6.1', 'numpy': '2.1'}
   {'os': 'ubuntu-latest', 'python': '3.12', 'sklearn': '1.3.2', 'numpy': '1.26'}
   {'os': 'ubuntu-latest', 'python': '3.12', 'sklearn': '1.3.2', 'numpy': '2.1'}
   {'os': 'ubuntu-latest', 'python': '3.12', 'sklearn': '1.6.1', 'numpy': '1.26', 'run_slow': True}
   {'os': 'ubuntu-latest', 'python': '3.12', 'sklearn': '1.6.1', 'numpy': '2.1', 'run_slow': True}
   {'os': 'windows-latest', 'python': '3.12', 'sklearn': '1.3.2', 'numpy': '1.26'}
   {'os': 'windows-latest', 'python': '3.12', 'sklearn': '1.3.2', 'numpy': '2.1'}
   {'os': 'windows-latest', 'python': '3.12', 'sklearn': '1.6.1', 'numpy': '1.26'}
   {'os': 'windows-latest', 'python': '3.12', 'sklearn': '1.6.1', 'numpy': '2.1'}
```

**Follow-ups:**
- *How do you build the matrix from a file?* A first job prints JSON to `$GITHUB_OUTPUT` and the next job uses `fromJSON(needs.x.outputs.matrix)`.
- *How do you keep cost down?* Matrix on a schedule or on main, a single combination on pull requests.
- *Why `fail-fast: false`?* To see all the broken combinations in one run.

**Common mistakes:**
- Adding axes without counting jobs.
- Putting a GPU job in the default matrix.
- Unquoted `3.10` in YAML.
- Testing every middle version and none of the extremes.

### Q18 ⭐⭐ 🟡 Passing a model between jobs: artifacts, cache, job outputs and the registry. Explain upload-artifact and download-artifact (retention, size limits, check current docs), why artifacts are for handing files between jobs and not a model store, why small values (a run id, a metric, an image digest) go through job outputs, and why the durable model belongs in the registry or object storage. Write a train, evaluate, promote workflow where train uploads the model and metrics and the later jobs download them, validate it with actionlint, and say what is not executed (the real artifact service). Part 4 owns the registry.
**Asked at:** GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Artifacts hand files from one job to the next inside a run, job outputs carry small values, and the durable model goes to the registry or object storage, because artifacts expire.

**Then explain:**
- `actions/upload-artifact` and `actions/download-artifact` share files between jobs of one run (each job has a fresh machine). Artifacts have a retention period and size limits; check current docs for the numbers.
- Job outputs are for small strings: a run id, a metric, an image digest. The train job writes `run_id=...` to `$GITHUB_OUTPUT`, and later jobs read `needs.train.outputs.run_id`.
- Artifacts are not a model store: they expire, they have no versions, no aliases, no lineage, and access is tied to the repository. The final `promote` job registers a durable copy and moves the alias.
- Name artifacts with the run id and attempt so a re-run does not mix files. `if-no-files-found: error` fails the upload if the model was not written.
- Cache is a different tool: it speeds up dependency installs (keyed, may be evicted) and should not carry models between jobs.
- Failure modes: v4 artifacts are scoped to the run, so a download in another workflow run needs extra settings (check current docs); a missing `needs:` means the output expression is undefined, and actionlint says so (see output).

**Example:** `train` writes `out/model.joblib` and `out/metrics.json`, uploads them as `model-<run>-<attempt>`. `evaluate` downloads that name, runs the gate script, and writes `passed=true|false`. `promote` runs only if `passed == 'true'`, downloads the same artifact and registers it. Hand check: three jobs, one artifact name, one output (`run_id`) crossing two job boundaries.

**Code:** (yaml for the workflow; bash for the validation)
```yaml
# ===== q18/train-eval-promote.yml =====
name: train-eval-promote
on:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  train:
    runs-on: ubuntu-latest
    outputs:
      run_id: ${{ steps.t.outputs.run_id }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - id: t
        run: |
          python train.py --out out/
          echo "run_id=${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}" >> "$GITHUB_OUTPUT"
      - uses: actions/upload-artifact@v4
        with:
          name: model-${{ steps.t.outputs.run_id }}
          path: |
            out/model.joblib
            out/metrics.json
          retention-days: 7
          if-no-files-found: error
  evaluate:
    needs: train
    runs-on: ubuntu-latest
    outputs:
      passed: ${{ steps.g.outputs.passed }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: model-${{ needs.train.outputs.run_id }}
          path: in/
      - id: g
        run: |
          if python gate.py --candidate in/metrics.json --champion baseline/metrics.json; then
            echo "passed=true" >> "$GITHUB_OUTPUT"
          else
            echo "passed=false" >> "$GITHUB_OUTPUT"
            exit 1
          fi
  promote:
    needs: [train, evaluate]
    if: needs.evaluate.outputs.passed == 'true'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: model-${{ needs.train.outputs.run_id }}
          path: in/
      - name: Register durable copy and move alias
        env:
          MLFLOW_TRACKING_URI: ${{ vars.MLFLOW_TRACKING_URI }}
        run: python register_and_promote.py --model in/model.joblib --metrics in/metrics.json
```
```bash
actionlint train-eval-promote.yml
check-jsonschema --builtin-schema vendor.github-workflows train-eval-promote.yml
# break it on purpose: remove `needs: train` from evaluate
sed 's/^    needs: train$/    needs: []/' train-eval-promote.yml > bad.yml && actionlint bad.yml
```

**Output (my run):** (actionlint 1.7.12, check-jsonschema 0.38.2). The real artifact service, the scripts `train.py`, `gate.py`, `register_and_promote.py` (names in the workflow are placeholders) and the `production` environment are **not executed**.
```text
$ actionlint train-eval-promote.yml
exit=0
$ check-jsonschema --builtin-schema vendor.github-workflows train-eval-promote.yml
ok -- validation done
exit=0

--- break it: evaluate reads needs.train.outputs.run_id but drops needs: train
bad.yml:30:12: "needs" section should not be empty [syntax-check]
   |
30 |     needs: []
   |            ^~
bad.yml:38:27: property "train" is not defined in object type {} [expression]
   |
38 |           name: model-${{ needs.train.outputs.run_id }}
   |                           ^~~~~~~~~~~~~~~~~~~~~~~~~~
exit=1
```

**Follow-ups:**
- *Why not cache the model?* A cache entry can be evicted or shared across branches; it is a speed-up, not storage.
- *Large models?* Push to object storage or the registry with a credential from OIDC and pass only the URI as an output.
- *Retention too short?* Then you lose the candidate; register it as a candidate version in the registry first.

**Common mistakes:**
- Treating artifacts as the model registry.
- Passing big files through job outputs.
- Same artifact name across matrix jobs (v4 errors on name clashes; check current docs).
- Forgetting `needs:` and getting an empty output.

### Q19 ⭐⭐ 🟡 Concurrency in GitHub Actions and races in model promotion. Explain concurrency groups with cancel-in-progress true for PR CI (a newer push replaces the older run) and false for deployments (never cancel a half-finished promotion), the one-running-one-pending behaviour of a group, that concurrency is separate from environments, and the stale-run problem (an older run finishing after a newer one and moving the alias backwards). Show the workflow, validate with actionlint, then demonstrate a compare-and-set promotion on a local sqlite MLflow registry that refuses to move champion to a version older than the current one, with a pytest, and run it.
**Asked at:** GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD | Model registry promotion write-ups (dataexpert.io champion-challenger guide, docs.zenml.io MLflow registry, towardsai MLflow series, an unofficial MLflow registry reference; search snippets only, not opened; the official MLflow docs were not opened and sources disagree on how deprecated stages are); editorial guides, not interview reports; MLOps and ML engineer roles
**Say this first (1 line):** I cancel superseded PR runs but never cancel a promotion in flight, and I make the promotion itself refuse to move the alias backwards, because an older run can finish after a newer one.

**Then explain:**
- A concurrency group allows one running and at most one pending run per group; a newer pending run replaces the older pending one (details: check current docs). `cancel-in-progress: true` cancels the running one too.
- PR CI: `true`, a new push replaces the old run and saves minutes. Deployment: `false`, killing a half-finished promotion can leave the alias or a rollout in a mixed state.
- Concurrency is separate from environments. An environment gives approvals and secrets scoping; the concurrency group gives mutual exclusion. Use both on a promotion job.
- The stale-run problem: run A starts (v2), run B starts (v3), B finishes first, A finishes late and moves the alias back to v2. Serialising helps but does not fully stop it, because pending runs can still arrive in an unexpected order or be re-run by hand.
- So the promote script does compare-and-set: refuse if the requested version is older than the current champion, and optionally refuse if the champion is not the value I saw earlier (`expected`).
- Honest limit: my check is read then write. MLflow's alias call is a plain set, and I did not find or verify an atomic conditional set. Two promotions in the exact same instant can still interleave; the concurrency group is what removes that window. Check the registry docs for your backend.

**Example:** B (v3) promotes first, then A (v2). Without the check the alias ends on v2 (wrong). With the check A prints `REFUSED: v2 is older than current champion v3`, exits 3, and champion stays v3. Hand check: 2 < 3, so refuse.

**Code:** (yaml for the workflow; python for the script and pytest; bash for the commands)
```yaml
# ===== q19/concurrency.yml =====
name: churn-ci-and-deploy
on:
  pull_request:
  push:
    branches: [main]
concurrency:
  group: ${{ github.workflow }}-${{ github.event_name == 'pull_request' && github.head_ref || 'main' }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "tests"
  promote:
    if: github.event_name == 'push'
    needs: test
    runs-on: ubuntu-latest
    environment: production
    concurrency:
      group: promote-churn           # one promotion at a time, shared across workflows
      cancel-in-progress: false      # never kill a half-finished promotion
    env:
      MLFLOW_TRACKING_URI: ${{ vars.MLFLOW_TRACKING_URI }}
      VERSION: ${{ vars.CANDIDATE_VERSION }}
    steps:
      - uses: actions/checkout@v4
      - run: python cas_promote.py --uri "$MLFLOW_TRACKING_URI" --name churn --version "$VERSION"
```
```python
# ===== q19/cas_promote.py =====
"""Compare-and-set promotion: only move the alias FORWARD, and only if it still points where we think."""
import argparse, sys
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException


def current(client, name, alias="champion"):
    try:
        return int(client.get_model_version_by_alias(name, alias).version)
    except MlflowException:
        return None


def promote_forward(client, name, version, alias="champion", expected=None):
    """expected: the version the caller saw before deciding (None = do not check)."""
    version = int(version)
    cur = current(client, name, alias)
    if expected is not None and cur != expected:
        return False, f"REFUSED: alias moved under us (expected {expected}, found {cur})"
    if cur is not None and version < cur:
        return False, f"REFUSED: v{version} is older than current champion v{cur}"
    if cur == version:
        return True, f"NO-OP: already v{version}"
    client.set_registered_model_alias(name, alias, str(version))
    return True, f"PROMOTED: v{cur} -> v{version}"


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--uri", required=True); p.add_argument("--name", required=True)
    p.add_argument("--version", required=True)
    a = p.parse_args()
    ok, msg = promote_forward(MlflowClient(a.uri, registry_uri=a.uri), a.name, a.version)
    print(msg)
    sys.exit(0 if ok else 3)

# ===== q19/test_cas.py =====
import os, pytest
os.environ["MLFLOW_DISABLE_TELEMETRY"] = "true"
import mlflow
from mlflow import MlflowClient
from cas_promote import promote_forward, current


@pytest.fixture()
def client(tmp_path):
    uri = f"sqlite:///{tmp_path}/m.db"
    c = MlflowClient(uri, registry_uri=uri)
    c.create_registered_model("churn")
    for i in range(3):                                   # three versions, no artifacts needed
        c.create_model_version("churn", source=f"{tmp_path}/fake{i}", run_id=None)
    return c


def test_forward_ok(client):
    assert promote_forward(client, "churn", 1)[0]
    assert promote_forward(client, "churn", 3)[0]
    assert current(client, "churn") == 3


def test_stale_run_cannot_move_backwards(client):
    promote_forward(client, "churn", 3)                  # the newer run finished first
    ok, msg = promote_forward(client, "churn", 2)        # the older run finishes late
    assert not ok and "older" in msg
    assert current(client, "churn") == 3


def test_expected_mismatch_refused(client):
    promote_forward(client, "churn", 1)
    promote_forward(client, "churn", 2)                  # someone else moved it
    ok, msg = promote_forward(client, "churn", 3, expected=1)
    assert not ok and "moved under us" in msg
    assert current(client, "churn") == 2


def test_noop(client):
    promote_forward(client, "churn", 2)
    assert promote_forward(client, "churn", 2)[1].startswith("NO-OP")

# ===== q19/sim.py =====
"""Replay the stale-run race on a sqlite registry (own temp db)."""
import sys, tempfile, os
from mlflow import MlflowClient
from cas_promote import promote_forward, current

d = tempfile.mkdtemp()
u = f"sqlite:///{d}/m.db"
c = MlflowClient(u, registry_uri=u)
c.create_registered_model("churn")
for i in range(3):
    c.create_model_version("churn", source=f"{d}/x{i}", run_id=None)
print("run B (newer, v3) finishes first:", promote_forward(c, "churn", 3)[1])
print("run A (older, v2) finishes late :", promote_forward(c, "churn", 2)[1])
print("champion is v%s" % current(c, "churn"))
c.set_registered_model_alias("churn", "champion", "2")      # what a naive script would do
print("naive set_registered_model_alias leaves champion at v%s" % current(c, "churn"))
```
```bash
export MLFLOW_DISABLE_TELEMETRY=true
actionlint concurrency.yml
pytest -q
PYTHONPATH=. python3 sim.py
```

**Output (my run):** (mlflow 3.17.2 on a local sqlite registry, actionlint 1.7.12, pytest 9.1.1). The GitHub concurrency queue itself (running and pending runs, cancellations) is **not executed**; I only linted the YAML. `sim.py` replays the race with the same functions on a temp database (I ran it with `PYTHONPATH=.` because `-I` would hide the current directory).
```text
$ actionlint concurrency.yml
exit=0

$ pytest -q
....                                                                     [100%]
4 passed in 8.31s

$ PYTHONPATH=. python3 sim.py
run B (newer, v3) finishes first: PROMOTED: vNone -> v3
run A (older, v2) finishes late : REFUSED: v2 is older than current champion v3
champion is v3
naive set_registered_model_alias leaves champion at v2
```

**Follow-ups:**
- *Why a job-level group name as well?* The workflow-level group handles CI cancellation; the job-level `promote-churn` group makes sure two different workflows cannot promote at once.
- *What about a rollback?* A rollback intentionally moves backwards, so it uses its own path or an explicit `--allow-older` flag with a reason in the ledger. I did not build that flag here.
- *Is `github.ref` a good group key?* For PRs use the head ref; on main use a constant so all pushes share one queue.

**Common mistakes:**
- `cancel-in-progress: true` on deployments.
- Assuming environments serialise runs.
- Trusting run order instead of checking versions.
- Using a group key that includes the commit SHA, which makes every run its own group and queues nothing.

### Q20 ⭐⭐ 🟡 Self-hosted and GPU runners for ML CI. Explain when the hosted runner is not enough (GPU smoke tests, large memory, private network access), runner labels and runs-on: [self-hosted, linux, gpu], ephemeral or just-in-time runners, autoscaling at concept level (actions-runner-controller on Kubernetes, check current docs), idle GPU cost, and the security rules (never on public repositories or untrusted fork PRs, because a PR can run code on your machine; a persistent runner keeps files and credentials between jobs). Show a workflow, run actionlint to see that a custom label is flagged until configured in actionlint.yaml, and write a pytest that skips GPU tests when torch.cuda is unavailable. Real GPU runners are not executed.
**Asked at:** Self-hosted runner security sources (Synacktiv 'GitHub Actions exploitation: self hosted runners', appsec.equinor.com runner guidance, Microsoft Learn manage-runners, techzine.eu report on the PyTorch runner finding, dev.to self-hosted runners; search snippets only, not opened; one vendor checklist cited an incident that could not be verified and is not used); security write-ups, not interview reports; ML platform and DevSecOps roles running GPU CI | GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD
**Say this first (1 line):** I use self-hosted or GPU runners only when the hosted runner cannot do the job (GPU smoke tests, big memory, private network), I use labels and ephemeral runners, and I never let untrusted pull requests run on them.

**Then explain:**
- When hosted is not enough: a GPU smoke test (does the model load and run on CUDA), large memory, data behind a private network, special hardware. Everything else stays on hosted runners.
- Labels: `runs-on: [self-hosted, linux, gpu]` picks a runner that has all three labels. actionlint does not know your custom label `gpu` until it is listed in `.github/actionlint.yaml` (see output).
- Ephemeral or just-in-time runners take one job and are removed, so files and credentials do not stay for the next job. A persistent runner keeps its disk, caches and tokens between jobs.
- Autoscaling at concept level: a controller (actions-runner-controller on Kubernetes is one option, check current docs) starts runners when jobs queue and removes them when idle. An idle GPU node still costs money, so scale to zero where you can and keep jobs short with `timeout-minutes`.
- Security: a pull request can change the workflow or the test code and so run code on your machine. Do not attach self-hosted runners to public repositories or to untrusted fork PRs; restrict the GPU workflow to `push` on main and `workflow_dispatch`, and require approval for outside contributors.
- Tests must still pass without a GPU: skip with a reason, do not fail. The pytest below skips when `torch.cuda` is not available (and when torch is not installed).
- Failure modes: a label typo makes the job wait forever in queue; a GPU runner with a full disk from old checkouts; credentials left on a persistent runner.

**Example:** push to main triggers `gpu-smoke`. A runner with labels `self-hosted, linux, gpu` picks it up, runs `nvidia-smi`, then the GPU test. On a laptop or hosted runner the same test shows `SKIPPED ... no CUDA device`. Hand check: the three labels in `runs-on` all must match the runner.

**Code:** (yaml for the workflow and the actionlint config; python for the test; bash for the commands)
```yaml
# ===== q20/.github/workflows/gpu-smoke.yml =====
name: gpu-smoke
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
jobs:
  gpu:
    runs-on: [self-hosted, linux, gpu]
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - run: nvidia-smi
      - run: pytest -q tests/test_gpu.py

# ===== q20/.github/actionlint.yaml =====
self-hosted-runner:
  labels:
    - gpu
```
```python
# ===== q20/tests/test_gpu.py =====
import importlib.util, pytest

HAS_CUDA = False
if importlib.util.find_spec("torch"):
    import torch
    HAS_CUDA = torch.cuda.is_available()

@pytest.mark.skipif(not HAS_CUDA, reason="no CUDA device on this runner")
def test_gpu_only():
    assert HAS_CUDA
```
```bash
git init -q .                       # actionlint finds .github/actionlint.yaml through the repo root
actionlint .github/workflows/gpu-smoke.yml                    # without the config: label error
actionlint .github/workflows/gpu-smoke.yml                    # with the config: clean
pytest -q -rs tests/test_gpu.py
```

**Output (my run):** (actionlint 1.7.12, pytest 9.1.1; this sandbox has no torch and no GPU). Real self-hosted or GPU runners, runner registration, autoscaling, `nvidia-smi` and an actual CUDA test are **not executed**. For the first actionlint command I removed `.github/actionlint.yaml`, for the second I put it back.
```text
$ actionlint .github/workflows/gpu-smoke.yml   # no config yet
.github/workflows/gpu-smoke.yml:10:35: label "gpu" is unknown. available labels are "windows-latest", "windows-latest-8-cores", "windows-2025", "windows-2025-vs2026", "windows-2022", "windows-11-arm", "ubuntu-slim", "ubuntu-latest", "ubuntu-latest-4-cores", "ubuntu-latest-8-cores", "ubuntu-latest-16-cores", "ubuntu-24.04", "ubuntu-24.04-arm", "ubuntu-22.04", "ubuntu-22.04-arm", "macos-latest", "macos-latest-xlarge", "macos-latest-large", "macos-26-intel", "macos-26-xlarge", "macos-26-large", "macos-26", "macos-15-intel", "macos-15-xlarge", "macos-15-large", "macos-15", "macos-14-xlarge", "macos-14-large", "macos-14", "self-hosted", "x64", "arm", "arm64", "linux", "macos", "windows". if it is a custom label for self-hosted runner, set list of labels in actionlint.yaml config file [runner-label]
   |
10 |     runs-on: [self-hosted, linux, gpu]
   |                                   ^~~~
exit=1

$ actionlint with .github/actionlint.yaml declaring label gpu
exit=0

$ python3 -c "import torch"
ModuleNotFoundError: No module named 'torch'

$ pytest -q -rs tests/test_gpu.py   # this sandbox: no torch, no CUDA
s                                                                        [100%]
=========================== short test summary info ============================
SKIPPED [1] tests/test_gpu.py:8: no CUDA device on this runner
1 skipped in 0.01s

$ check-jsonschema --builtin-schema vendor.github-workflows
ok -- validation done
```

**Follow-ups:**
- *Why does a fork PR matter?* The PR can edit the workflow and run its own code on your runner, with whatever access the runner has.
- *How do you keep the GPU bill down?* Short smoke tests, schedule or main-only triggers, scale to zero, and spot or preemptible capacity if your platform has it (check current docs).
- *Runner groups?* Use them to limit which repositories can use a runner (check current docs).

**Common mistakes:**
- Self-hosted runners on a public repository.
- Persistent runners holding cloud credentials.
- GPU tests that fail instead of skip on machines without CUDA.
- GPU job on every PR.

### Q21 ⭐⭐ 🟡 Pipeline-as-code for ML: what lives in Git and why. List what you keep in the repository (workflow files, pipeline definitions, Dockerfiles, serving manifests, gate thresholds, environment config, registry promotion rules), the benefits (review, history, rollback, reproducibility) and the trap of clicking in a UI or editing thresholds outside Git. Explain declarative versus imperative pipelines and the idea that a pull request is the only way to change production behaviour. Write a small repository-linter script that checks required files exist, that gate thresholds live in a versioned YAML, and that no workflow hard-codes a secret-like string, and run it on a good and a bad sample tree.
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | GitOps comparison posts (devtron.ai, codefresh.io, earthly.dev, harness.io, oneuptime.com 2026 Argo CD versus Flux; search snippets only, not opened); vendor and editorial blogs, nothing found on ML-specific GitOps or interview lists; platform and DevOps roles with ML workloads
**Say this first (1 line):** Everything that decides what runs in production, including code, pipeline, image, serving config and gate thresholds, lives in Git, so the only way to change production is a reviewed pull request.

**Then explain:**
- What goes in the repo: workflow files, pipeline definitions, Dockerfiles, serving manifests, gate thresholds in a YAML file, environment config (non-secret), registry promotion rules, CODEOWNERS.
- What stays out: secrets (use the secret store), raw data and model binaries (use DVC or the registry, and keep only a pointer in Git).
- Benefits: review before change, history of who changed a threshold and why, one-command rollback (revert the commit), and reproducibility (a commit identifies the pipeline that built a model).
- Declarative says what the end state is (a manifest, a `gates.yaml`); imperative says how to get there (a shell script of steps). Prefer declarative for config and thresholds. Imperative is fine inside a step, but keep it in a file in the repo.
- The trap: someone lowers `min_auc` in a CI UI variable or edits a pipeline in a web console. Now Git no longer matches production, nobody can review it, and the next deploy silently reverts or keeps the drift.
- Failure modes: a threshold hard-coded in a workflow (a second source of truth), a secret pasted in YAML (it stays in Git history even after you delete it), and a "temporary" manual hotfix in the UI that never lands in Git.

**Example:** `configs/gates.yaml` says `min_auc: 0.80`. A teammate wants 0.78 to ship a model. They open a PR, CODEOWNERS asks the ML lead to review, and the diff shows the change. Three months later the audit question "when did we relax the gate and who agreed" is answered by `git log -p configs/gates.yaml`.

**Code:** a small linter (Python) that checks required files exist, that `configs/gates.yaml` has the required keys, and that workflows contain no secret-like string and no hard-coded threshold. A script builds one good and one bad tree. Workflow lines of the form `${{ secrets.X }}` are references, so they are allowed.

```python
# --- q21/repo_lint.py ---
"""Repository linter: required files, versioned gate thresholds, no secret-like strings in workflows."""
import re
import sys
from pathlib import Path

import yaml

REQUIRED = [
    ".github/workflows/ci.yml",
    "Dockerfile",
    "configs/gates.yaml",
    "serving/deployment.yaml",
    "CODEOWNERS",
]
REQUIRED_GATE_KEYS = {"min_auc", "max_auc_drop", "max_p95_ms"}
SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),                       # AWS access key id shape
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),                   # GitHub token shape
    re.compile(r"(?i)(password|secret|token|api[_-]?key)\s*[:=]\s*['\"]?[A-Za-z0-9/+_\-]{12,}"),
]


def lint(root):
    root = Path(root)
    problems = []
    for rel in REQUIRED:
        if not (root / rel).is_file():
            problems.append(f"missing required file: {rel}")
    gates = root / "configs/gates.yaml"
    if gates.is_file():
        data = yaml.safe_load(gates.read_text()) or {}
        missing = REQUIRED_GATE_KEYS - set(data)
        if missing:
            problems.append(f"configs/gates.yaml missing keys: {sorted(missing)}")
    wf_dir = root / ".github/workflows"
    for wf in sorted(wf_dir.glob("*.yml")) if wf_dir.is_dir() else []:
        text = wf.read_text()
        for n, line in enumerate(text.splitlines(), 1):
            if "${{ secrets." in line:
                continue  # a reference, not a value
            if any(p.search(line) for p in SECRET_PATTERNS):
                problems.append(f"{wf.relative_to(root)}:{n}: secret-like string")
            # thresholds hard-coded in the workflow instead of configs/gates.yaml
            if re.search(r"(?i)(min_auc|max_auc_drop|--threshold)\s*[=: ]\s*0?\.\d+", line):
                problems.append(f"{wf.relative_to(root)}:{n}: gate threshold hard-coded in workflow")
    return problems


if __name__ == "__main__":
    probs = lint(sys.argv[1])
    for p in probs:
        print("FAIL", p)
    print("result:", "FAIL" if probs else "PASS", f"({len(probs)} problem(s))")
    sys.exit(1 if probs else 0)
```
```bash
# --- q21/make_trees.sh ---
set -e
T=$1; rm -rf "$T"; mkdir -p "$T/good/.github/workflows" "$T/good/configs" "$T/good/serving" "$T/bad/.github/workflows"
cd "$T/good"
cat > .github/workflows/ci.yml <<'Y'
name: ci
on: [pull_request]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python gate.py --config configs/gates.yaml
        env:
          REGISTRY_TOKEN: ${{ secrets.REGISTRY_TOKEN }}
Y
printf 'min_auc: 0.80\nmax_auc_drop: 0.005\nmax_p95_ms: 120\n' > configs/gates.yaml
printf 'FROM python:3.12-slim\n' > Dockerfile
printf 'apiVersion: apps/v1\nkind: Deployment\n' > serving/deployment.yaml
printf '/configs/ @ml-leads\n/models/ @ml-leads\n' > CODEOWNERS
cd "$T/bad"
cat > .github/workflows/ci.yml <<'Y'
name: ci
on: [pull_request]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python gate.py --threshold 0.80
        env:
          API_KEY: abcd1234efgh5678ijkl
          AWS_ID: AKIAABCDEFGHIJKLMNOP
Y
printf 'FROM python:3.12-slim\n' > Dockerfile

# --- q21/run.sh ---
PY=/tmp/claude-0/b7p07/v/bin/python
D=$(dirname "$(readlink -f "$0")")
bash $D/make_trees.sh /tmp/claude-0/b7_q21_30/q21
echo '$ python3 -I repo_lint.py good/'; $PY -I $D/repo_lint.py /tmp/claude-0/b7_q21_30/q21/good; echo "exit=$?"
echo '$ python3 -I repo_lint.py bad/'; $PY -I $D/repo_lint.py /tmp/claude-0/b7_q21_30/q21/bad; echo "exit=$?"
```
**Output (my run):** venv Python (pyyaml) with `-I`; ran in `/tmp/claude-0/b7_q21_30/q21`.

```text
$ python3 -I repo_lint.py good/
result: PASS (0 problem(s))
exit=0
$ python3 -I repo_lint.py bad/
FAIL missing required file: configs/gates.yaml
FAIL missing required file: serving/deployment.yaml
FAIL missing required file: CODEOWNERS
FAIL .github/workflows/ci.yml:8: gate threshold hard-coded in workflow
FAIL .github/workflows/ci.yml:10: secret-like string
FAIL .github/workflows/ci.yml:11: secret-like string
result: FAIL (6 problem(s))
exit=1
```
The bad tree fails on three missing files, one hard-coded threshold and two secret-like strings; the good tree passes. The regexes are a teaching sample. In real life add a scanner such as gitleaks or GitHub secret scanning (not executed here).

**Follow-ups:**
- *How do you enforce "PR is the only way"?* Branch protection on main, required checks, CODEOWNERS on `configs/` and `models/`, and no one holding admin bypass for routine work (settings not executed here).
- *Where do secrets go then?* In the CI secret store or a vault, referenced by name in the workflow. Rotate any secret that ever reached Git.
- *Is a UI-built pipeline always wrong?* Not always, but export it as code and keep that file in Git, or you cannot review or roll it back.

**Common mistakes:**
- Keeping thresholds in an env var in the CI UI, so a change leaves no diff.
- Treating "deleted the secret in a later commit" as fixed. History still has it.
- Checking model weights or datasets into Git instead of a pointer.
- One giant imperative `deploy.sh` nobody can review line by line.

### Q22 ⭐⭐ 🟡 Jenkins versus GitLab CI versus GitHub Actions for an ML team. Compare where config lives (Jenkinsfile, .gitlab-ci.yml, .github/workflows), hosting and runners, plugin or marketplace ecosystem, secrets handling, reuse mechanisms, GPU runner support, and when a company with an existing Jenkins estate, a self-managed GitLab or a data-residency rule should stay put; hedge any India-specific claims and check current docs. Write the same train-test-promote pipeline as a GitHub workflow, a .gitlab-ci.yml and a Jenkinsfile, parse the first two with pyyaml and actionlint where it applies, and say the Jenkinsfile and GitLab runners were not executed.
**Asked at:** CI tool comparisons (dev.to 'Jenkins vs GitHub Actions vs GitLab CI', acquaintsoft.com, attractgroup.com, mdssoftware.pl; search snippets only, not opened; nothing found on MLOps-specific or India-enterprise-specific comparison); generic editorial comparisons; DevOps and MLOps roles at enterprises with existing Jenkins or GitLab estates | MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** For a new ML team on GitHub I would pick GitHub Actions; keep Jenkins or self-managed GitLab when you already run them well, or when rules say code and secrets must stay inside your network.

**Then explain:**

| | GitHub Actions | GitLab CI | Jenkins |
|---|---|---|---|
| Config file | `.github/workflows/*.yml` | `.gitlab-ci.yml` | `Jenkinsfile` (Groovy) |
| Hosting | GitHub-hosted runners or your own | GitLab.com runners or self-managed GitLab | You host the controller and agents |
| Ecosystem | Marketplace of actions | Built-in features plus templates | Large plugin ecosystem you must maintain |
| Secrets | Repo, environment and org secrets, OIDC to cloud | CI/CD variables (masked, protected), vault integrations | Credentials plugin, often plus a vault |
| Reuse | Reusable workflows, composite actions | `include`, `extends`, templates | Shared libraries |
| GPU | Self-hosted GPU runner, or larger hosted runners (check current docs) | Self-managed runner with GPU | Agent with GPU, labels |

- Staying put is a good answer when: a Jenkins estate already works and has people to run it; a self-managed GitLab holds code, registry and CI together; or a data-residency or security rule wants everything in your network. In India, some regulated sectors have such rules. I would not state a specific regulation from memory; check the company's policy and current official sources.
- Cost of moving is real: rewrite pipelines, rebuild secrets and permissions, retrain people. The YAML is the easy part; the surrounding practice is the hard part.
- Failure modes: Jenkins plugin upgrades breaking pipelines, a snowflake Jenkins server nobody can rebuild, GitHub Actions marketplace actions pinned to a mutable tag, and GPU runners left idle.
- The ML pipeline is the same on all three: train, test (gate), promote. Only the syntax differs.

**Example:** Same pipeline in three files below: train writes `model.pkl`, test runs a gate script, promote needs a human and uses a credential. In GitHub it is an `environment: production` with required reviewers. In GitLab it is `when: manual`. In Jenkins it is an `input` step.

**Code:** the three files (the scripts `train.py`, `gate.py`, `promote.py` are placeholders).

```yaml
# --- q22/github-workflow.yml ---
name: train-test-promote
on:
  push:
    branches: [main]
jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python train.py --out model.pkl
      - uses: actions/upload-artifact@v4
        with:
          name: model
          path: model.pkl
  test:
    needs: train
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: model
      - run: python gate.py --model model.pkl
  promote:
    needs: test
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - run: python promote.py --alias champion
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}

# --- q22/.gitlab-ci.yml ---
stages: [train, test, promote]
default:
  image: python:3.12-slim
train:
  stage: train
  script:
    - python train.py --out model.pkl
  artifacts:
    paths: [model.pkl]
test:
  stage: test
  needs: [train]
  script:
    - python gate.py --model model.pkl
promote:
  stage: promote
  needs: [test]
  environment: production
  when: manual
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  script:
    - python promote.py --alias champion
```
```groovy
// --- q22/Jenkinsfile ---
pipeline {
  agent { docker { image 'python:3.12-slim' } }
  stages {
    stage('Train') {
      steps {
        sh 'python train.py --out model.pkl'
        stash name: 'model', includes: 'model.pkl'
      }
    }
    stage('Test') {
      steps {
        unstash 'model'
        sh 'python gate.py --model model.pkl'
      }
    }
    stage('Promote') {
      when { branch 'main' }
      steps {
        input message: 'Promote to champion?'
        withCredentials([string(credentialsId: 'mlflow-uri', variable: 'MLFLOW_TRACKING_URI')]) {
          sh 'python promote.py --alias champion'
        }
      }
    }
  }
}
```
```python
# --- q22/check_pipelines.py ---
import sys
import yaml

gh = yaml.safe_load(open(sys.argv[1]))
print("github keys:", list(gh))
print("github 'on' key present as string:", "on" in gh, "| as boolean True:", True in gh)
print("github jobs:", {k: v.get("needs") for k, v in gh["jobs"].items()})

gl = yaml.safe_load(open(sys.argv[2]))
jobs = {k: v for k, v in gl.items() if isinstance(v, dict) and "stage" in v}
print("gitlab stages:", gl["stages"])
for name, j in jobs.items():
    assert j["stage"] in gl["stages"], name
    for dep in j.get("needs", []):
        assert dep in jobs, (name, dep)
    print(f"gitlab job {name}: stage={j['stage']} needs={j.get('needs', [])}")
print("gitlab references all valid")
```
**Output (my run):**

```text
$ python3 -I check_pipelines.py
github keys: ['name', True, 'jobs']
github 'on' key present as string: False | as boolean True: True
github jobs: {'train': None, 'test': 'train', 'promote': 'test'}
gitlab stages: ['train', 'test', 'promote']
gitlab job train: stage=train needs=[]
gitlab job test: stage=test needs=['train']
gitlab job promote: stage=promote needs=['test']
gitlab references all valid
$ actionlint github-workflow.yml
exit=0
$ check-jsonschema --builtin-schema vendor.github-workflows github-workflow.yml
ok -- validation done
exit=0
```
The GitHub workflow passes actionlint and the vendored GitHub workflow schema. Note the PyYAML trap: the key `on` is parsed as boolean `True`, so code that reads `wf["on"]` gets a KeyError; read `wf.get("on", wf.get(True))`. The `.gitlab-ci.yml` was only parsed with PyYAML plus my own check that stages and `needs` point to real jobs. GitLab's own linter (CI Lint) was not available. The Jenkinsfile was not parsed or run at all (Groovy; no Jenkins here). No GitLab runner, Jenkins agent or GitHub runner was executed.

**Follow-ups:**
- *Can one migrate gradually?* Yes. Move the cheap PR checks first, keep the heavy deploy job in the old system, then cut over.
- *How do you keep logic portable?* Put real logic in scripts (`make test`, `python gate.py`) and keep the CI file thin.
- *GPU?* Self-hosted runner with a GPU label on all three; security rules are the same (no untrusted PRs on a persistent runner).

**Common mistakes:**
- Choosing by popularity instead of where code, secrets and data must live.
- Writing business logic in Groovy or YAML, which locks you in.
- Comparing only syntax and ignoring who maintains the servers.
- Quoting a regulation from memory.

### Q23 ⭐⭐ 🟡 Data tests in CI. Explain schema checks (columns, dtypes), ranges, null rates, uniqueness, categorical domains, row-count sanity, and train-serving feature contract checks, on a small sample in PR CI and on every new data batch in the pipeline. Mention Great Expectations and pandera at concept level and write the checks yourself with pandas as a function that returns a list of failures, plus pytest cases for a good frame and a corrupted frame, and run them. Part 1 owns pytest basics and Part 8 owns monitoring data quality in production; keep this to the CI gate.
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** I put a small data-test function in CI that returns a list of failures, run it on a small sample in every PR and on every new data batch before training, and fail the build if the list is not empty.

**Then explain:**
- Checks to write: schema (columns, dtypes), ranges, null rate, uniqueness of the key, categorical domain, row-count sanity, and the train-serving contract (every feature the serving API sends exists in training data with the same type).
- Two places: a tiny committed sample in PR CI (seconds, catches code that breaks the schema) and the real new batch in the pipeline (catches bad data from upstream). Different data, same function.
- Return a list, do not raise on the first problem. The engineer then sees all problems in one run.
- Libraries: Great Expectations and pandera give declarative rules, reports and integrations. At concept level I would use one for a bigger team. Writing the checks by hand shows I understand them and has no dependencies.
- Failure modes: checking dtype by exact name (pandas 3 reads text as `str`, older pandas as `object`, my first version of this test failed on that), thresholds so tight that the gate gets ignored, and a check that passes because the column is all null.
- Scope: pytest basics are Part 1; monitoring data quality in production is Part 8. This is only the CI gate.

**Example:** Corrupted batch: one age is 250, a plan is `gold`, ids repeat, a third of `monthly_spend` is missing. The function returns five messages and CI fails before any training time is spent.

**Code:** the checks and the pytest file.

```python
# --- q23/data_checks.py ---
"""CI data gate: returns a list of failure strings. Empty list = pass."""
import pandas as pd

# dtype families, not exact names: pandas 3 reads text as "str", older pandas as "object"
SCHEMA = {"customer_id": "integer", "age": "integer", "plan": "text", "monthly_spend": "float", "churned": "integer"}
CHECKS = {
    "integer": pd.api.types.is_integer_dtype,
    "float": pd.api.types.is_float_dtype,
    "text": lambda s: pd.api.types.is_string_dtype(s) or pd.api.types.is_object_dtype(s),
}
PLANS = {"basic", "plus", "pro"}
SERVING_FEATURES = ["age", "plan", "monthly_spend"]  # what the serving API sends


def check_frame(df, min_rows=5, feature_contract=SERVING_FEATURES):
    f = []
    # schema: columns and dtypes
    for col, dt in SCHEMA.items():
        if col not in df.columns:
            f.append(f"missing column: {col}")
        elif not CHECKS[dt](df[col]):
            f.append(f"dtype {col}: expected {dt}, got {df[col].dtype}")
    if f:
        return f  # later checks need the right columns
    if len(df) < min_rows:
        f.append(f"row count {len(df)} < {min_rows}")
    if df["customer_id"].duplicated().any():
        f.append("customer_id not unique")
    if not df["age"].between(18, 100).all():
        f.append("age out of range 18-100")
    if (df["monthly_spend"] < 0).any():
        f.append("monthly_spend negative")
    null_rate = df["monthly_spend"].isna().mean()
    if null_rate > 0.1:
        f.append(f"monthly_spend null rate {null_rate:.0%} > 10%")
    bad = set(df["plan"].dropna().unique()) - PLANS
    if bad:
        f.append(f"plan has unknown values: {sorted(bad)}")
    if not set(df["churned"].unique()) <= {0, 1}:
        f.append("churned not in {0,1}")
    for c in feature_contract:  # train-serving contract
        if c not in df.columns:
            f.append(f"serving feature missing from training data: {c}")
    return f

# --- q23/test_data_checks.py ---
import pandas as pd
import pytest

from data_checks import check_frame


@pytest.fixture
def good():
    return pd.DataFrame({
        "customer_id": [1, 2, 3, 4, 5, 6],
        "age": [25, 40, 33, 58, 29, 61],
        "plan": ["basic", "plus", "pro", "basic", "plus", "pro"],
        "monthly_spend": [10.0, 25.5, 40.0, 12.0, 30.0, 55.0],
        "churned": [0, 1, 0, 0, 1, 0],
    })


def test_good_frame_passes(good):
    assert check_frame(good) == []


def test_corrupted_frame_reports_every_problem(good):
    bad = good.copy()
    bad.loc[1, "age"] = 250
    bad.loc[2, "plan"] = "platinum"
    bad.loc[3, "monthly_spend"] = -5.0
    bad.loc[4, "customer_id"] = 1
    bad.loc[[0, 5], "monthly_spend"] = None
    out = check_frame(bad)
    assert "customer_id not unique" in out
    assert "age out of range 18-100" in out
    assert "monthly_spend negative" in out
    assert any("unknown values" in m for m in out)
    assert any("null rate" in m for m in out)


def test_wrong_dtype_and_missing_column(good):
    bad = good.astype({"age": "float64"}).drop(columns=["plan"])
    out = check_frame(bad)
    assert "missing column: plan" in out
    assert any(m.startswith("dtype age") for m in out)


def test_too_few_rows(good):
    assert any("row count" in m for m in check_frame(good.head(2)))
```
```bash
# --- q23/run.sh ---
V=/tmp/claude-0/b7p07/v/bin
D=$(dirname "$(readlink -f "$0")")
cd $D && echo '$ pytest -q -p no:cacheprovider test_data_checks.py' && PYTHONDONTWRITEBYTECODE=1 $V/pytest -q -p no:cacheprovider test_data_checks.py
$V/python -I - <<'PY'
import sys; sys.path.insert(0, ".")
import pandas as pd
from data_checks import check_frame
df = pd.DataFrame({"customer_id":[1,2,2,4,5,6],"age":[25,250,33,58,29,61],"plan":["basic","gold","pro","basic","plus","pro"],
 "monthly_spend":[None,25.5,-1.0,12.0,None,55.0],"churned":[0,1,0,0,1,0]})
print("corrupted frame ->")
for m in check_frame(df): print("  FAIL", m)
PY
```
**Output (my run):** venv Python 3.13, pandas 3.1.0, pytest 9.1.1.

```text
$ pytest -q -p no:cacheprovider test_data_checks.py
....                                                                     [100%]
4 passed in 0.48s
corrupted frame ->
  FAIL customer_id not unique
  FAIL age out of range 18-100
  FAIL monthly_spend negative
  FAIL monthly_spend null rate 33% > 10%
  FAIL plan has unknown values: ['gold']
```
Four tests passed. The first run of this test failed 3 of 4 because I compared dtypes by exact name; I changed to dtype families and reran.

**Follow-ups:**
- *Great Expectations or pandera?* pandera if the team lives in pandas and wants schemas as code; Great Expectations if you want data docs and checkpoints across sources. Check current docs.
- *What about drift?* That is monitoring (Part 8). The CI gate checks validity, not whether the distribution moved.
- *How do you pick the null threshold?* From history of the clean data, then review it in a PR like any other threshold.

**Common mistakes:**
- Testing only the code and never the data.
- Fail-fast on first error, which makes fixing slow.
- Testing on a sample that does not contain the bad cases, so nothing can fail.
- Keeping thresholds in code with no review trail.

### Q24 ⭐⭐ 🟡 Human approval and separation of duties for production model promotion. Explain who may approve (not the person who trained it), a GitHub environment with required reviewers combined with registry tags that record approved_by, gate_report URL and workflow run id, why the approval step should show the gate report, an audit trail for regulated teams, and emergency (break-glass) paths. Write a script that applies the approval tags to a registered version on a local sqlite MLflow registry and refuses promotion when approved_by equals the author, with a pytest, and run it. Real reviewer enforcement on GitHub is not executed.
**Asked at:** Model registry promotion write-ups (dataexpert.io champion-challenger guide, docs.zenml.io MLflow registry, towardsai MLflow series, an unofficial MLflow registry reference; search snippets only, not opened; the official MLflow docs were not opened and sources disagree on how deprecated stages are); editorial guides, not interview reports; MLOps and ML engineer roles | GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD
**Say this first (1 line):** The person who trained the model must not be the one who approves it going to production; approval is recorded as registry tags and enforced by a GitHub environment with required reviewers.

**Then explain:**
- Separation of duties: the author is stored on the model version (a tag set at registration). Approver must be different. Otherwise one compromised or hurried person can ship alone.
- Two layers: GitHub environment `production` with required reviewers blocks the deploy job until someone approves; the registry tags (`approved_by`, `gate_report`, `workflow_run_id`, `approved_at`) record who and on what evidence. The environment is the lock, the tags are the receipt.
- The reviewer must see the gate report (metrics versus champion, slice results, data checks) in the approval screen or a link, not just click approve.
- Audit trail for regulated teams: tags plus the Actions run log plus Git history answer who approved which version, when, with what evidence. Keep them for the retention your policy requires.
- Break-glass: an emergency path (an incident, a broken champion). Still needs a second person, requires a reason or incident id, sets `break_glass=true`, and triggers a review after the fact. It is a documented exception, not a bypass.
- Failure modes: a shared account approving everything, "approved" tags set by anyone with write access (restrict who can write tags), approvals done before the final gate report existed, and a promotion script that does not check the tags at all.

**Example:** Asha registers churn v1 (author tag `asha`). If Asha tries to approve, the script refuses. Ravi approves with a gate report URL and the workflow run id; the script then moves alias `champion` to v1.

**Code:** `approve()` checks author versus approver, writes tags, and `promote()` refuses without them. pytest covers four cases; a demo runs on a local sqlite registry.

```python
# --- q24/approve.py ---
"""Approval tags + separation of duties on an MLflow registry (sqlite)."""
import datetime as dt
import sys

from mlflow import MlflowClient


class PromotionRefused(Exception):
    pass


def approve(client, name, version, approver, gate_report_url, workflow_run_id, break_glass_reason=None):
    mv = client.get_model_version(name, str(version))
    author = mv.tags.get("author")
    if not author:
        raise PromotionRefused("version has no author tag; cannot check separation of duties")
    if approver == author:
        raise PromotionRefused(f"approver '{approver}' is the author; a second person must approve")
    if not gate_report_url and not break_glass_reason:
        raise PromotionRefused("gate_report URL is required (or a break-glass reason)")
    tags = {
        "approved_by": approver,
        "approved_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "gate_report": gate_report_url or "none",
        "workflow_run_id": str(workflow_run_id),
    }
    if break_glass_reason:
        tags["break_glass"] = "true"
        tags["break_glass_reason"] = break_glass_reason
    for k, v in tags.items():
        client.set_model_version_tag(name, str(version), k, v)
    return tags


def promote(client, name, version, alias="champion"):
    mv = client.get_model_version(name, str(version))
    for need in ("approved_by", "gate_report", "workflow_run_id"):
        if need not in mv.tags:
            raise PromotionRefused(f"cannot promote: tag '{need}' missing")
    client.set_registered_model_alias(name, alias, str(version))
    return alias


if __name__ == "__main__":
    # tiny CLI: approve.py <tracking_uri> <name> <version> <approver> <report_url> <run_id>
    uri, name, ver, who, url, run = sys.argv[1:7]
    c = MlflowClient(tracking_uri=uri, registry_uri=uri)
    try:
        approve(c, name, ver, who, url, run)
        promote(c, name, ver)
        print(f"promoted {name} v{ver} to champion, approved by {who}")
    except PromotionRefused as e:
        print("REFUSED:", e)
        sys.exit(1)

# --- q24/test_approve.py ---
import os

import mlflow
import pytest
from mlflow import MlflowClient

from approve import PromotionRefused, approve, promote

os.environ["MLFLOW_DISABLE_TELEMETRY"] = "true"


@pytest.fixture
def reg(tmp_path):
    uri = f"sqlite:///{tmp_path}/m.db"
    mlflow.set_tracking_uri(uri)
    mlflow.set_registry_uri(uri)
    c = MlflowClient(uri, uri)
    c.create_registered_model("churn")
    mv = c.create_model_version("churn", source="file:///tmp/none", tags={"author": "asha"})
    return c, mv.version


def test_author_cannot_approve(reg):
    c, v = reg
    with pytest.raises(PromotionRefused, match="is the author"):
        approve(c, "churn", v, "asha", "https://ci.example/report/1", 101)
    assert "approved_by" not in c.get_model_version("churn", v).tags


def test_other_person_approves_and_promotes(reg):
    c, v = reg
    tags = approve(c, "churn", v, "ravi", "https://ci.example/report/1", 101)
    assert tags["approved_by"] == "ravi"
    promote(c, "churn", v)
    assert c.get_model_version_by_alias("churn", "champion").version == v


def test_promote_without_approval_refused(reg):
    c, v = reg
    with pytest.raises(PromotionRefused, match="approved_by"):
        promote(c, "churn", v)


def test_break_glass_still_needs_second_person_and_leaves_a_mark(reg):
    c, v = reg
    with pytest.raises(PromotionRefused):
        approve(c, "churn", v, "asha", None, 7, break_glass_reason="INC-42")
    tags = approve(c, "churn", v, "ravi", None, 7, break_glass_reason="INC-42")
    assert tags["break_glass"] == "true"

# --- q24/demo.py ---
import os, sys
os.environ["MLFLOW_DISABLE_TELEMETRY"] = "true"
sys.path.insert(0, ".")
import mlflow
from mlflow import MlflowClient
from approve import PromotionRefused, approve, promote
uri = "sqlite:////tmp/claude-0/b7_q21_30/q24/m.db"
mlflow.set_tracking_uri(uri); mlflow.set_registry_uri(uri)
c = MlflowClient(uri, uri)
c.create_registered_model("churn")
mv = c.create_model_version("churn", source="file:///tmp/none", tags={"author": "asha"})
print("registered churn v%s author=asha" % mv.version)
try:
    approve(c, "churn", mv.version, "asha", "https://ci.example/gate-report/55", 9001)
except PromotionRefused as e:
    print("REFUSED:", e)
t = approve(c, "churn", mv.version, "ravi", "https://ci.example/gate-report/55", 9001)
promote(c, "churn", mv.version)
tags = c.get_model_version("churn", mv.version).tags
for k in sorted(tags):
    print(f"  {k} = {tags[k] if k != 'approved_at' else '<utc timestamp>'}")
print("champion ->", c.get_model_version_by_alias("churn", "champion").version)
```
```bash
# --- q24/run.sh ---
V=/tmp/claude-0/b7p07/v/bin
D=$(dirname "$(readlink -f "$0")")
export MLFLOW_DISABLE_TELEMETRY=true MLFLOW_DISABLE_AGENT_HINT=1 PYTHONDONTWRITEBYTECODE=1
rm -rf /tmp/claude-0/b7_q21_30/q24; mkdir -p /tmp/claude-0/b7_q21_30/q24
cd $D
echo '$ pytest -q -p no:cacheprovider test_approve.py'; $V/pytest -q -p no:cacheprovider test_approve.py 2>&1 | tail -5
echo '$ python3 -I demo.py'; $V/python -I demo.py 2>&1 | grep -v -i "alembic\|INFO\|warn"
```
**Output (my run):** MLflow 3.17.2, sqlite registry in `/tmp/claude-0/b7_q21_30/q24`, `MLFLOW_DISABLE_TELEMETRY=true`. I filtered MLflow's log lines from the demo output.

```text
$ pytest -q -p no:cacheprovider test_approve.py
  /tmp/claude-0/b7p07/v/lib/python3.13/site-packages/mlflow/store/tracking/sqlalchemy_store.py:327: SADeprecationWarning: The ``noload`` loader strategy is deprecated and will be removed in a future release.  This option produces incorrect results by returning ``None`` for related items. (deprecated since: 2.1)
    sqlalchemy.orm.configure_mappers()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
4 passed, 1 warning in 8.03s
$ python3 -I demo.py
registered churn v1 author=asha
REFUSED: approver 'asha' is the author; a second person must approve
  approved_at = <utc timestamp>
  approved_by = ravi
  author = asha
  gate_report = https://ci.example/gate-report/55
  workflow_run_id = 9001
champion -> 1
```
Not executed: the GitHub environment with required reviewers, who may approve, and how GitHub shows the approval. Those need a real repository. The environment YAML would just be `environment: production` on the deploy job (the reviewer list is a repository setting, check current docs). Also not executed: MLflow authentication; with plain sqlite anyone with file access can edit tags, so a real setup needs a server with permissions.

**Follow-ups:**
- *Can the approver be the same team?* Same team is fine; same person is not. Some regulated teams require someone outside the team.
- *Can GitHub stop self-approval?* Environments have an option to prevent the person who triggered the run from approving (check current docs). I would still keep the registry tag check.
- *What if the approver is on holiday?* Name a deputy list in advance; do not share credentials.

**Common mistakes:**
- Approving without opening the gate report.
- Storing the approver only in a chat message.
- A break-glass path that skips all checks and leaves no tag.
- Letting the training job write `approved_by`.

### Q25 ⭐⭐ 🟡 Release notes and model cards generated in CI. Explain what a release note for a model should contain (version, data version, git SHA, what changed, metrics versus the previous champion, known limitations, rollback target), generating it from the registry and metrics files instead of writing it by hand, attaching it to a GitHub Release, and the changelog from tags. Write a script that takes two metrics JSON files and tag names and prints markdown release notes with a metric-diff table, run it on sample data and show the output. Part 4 owns what a model card contains; this is the automation.
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD
**Say this first (1 line):** I generate the release note from the registry and metrics files in CI, so it is always consistent with what shipped and nobody types numbers by hand.

**Then explain:**
- A model release note has: model version, data version, git SHA, what changed (commits between tags), metrics versus the previous champion, known limitations, and the rollback target.
- Sources: metrics JSON written by the evaluation step, registry tags (data version, git SHA), `git log old_tag..new_tag` for the changelog. Hand-written notes drift and get skipped.
- Mark each metric better or worse, and know which direction is better (latency and Brier score: lower is better). Show a worse metric clearly; do not hide it.
- Attach it to a GitHub Release created from the model tag, so the note, tag and artifacts sit together (`gh release create` or a release action; not executed here).
- Failure modes: empty limitations (the script should nag), a wrong "previous" version picked, comparing metrics from different eval sets, and tags moved after release.
- Part 4 owns what a model card contains; this is just the automation step.

**Example:** AUC 0.842 to 0.851 is better, p95 latency 38.0 to 41.5 ms is worse. Both show in the table, and the reviewer decides if the trade is acceptable.

**Code:** the script, the two sample metric files (shown in the run via the script), and a throwaway git repo with two tags.

```python
# --- q25/release_notes.py ---
"""Usage: release_notes.py OLD.json NEW.json OLD_TAG NEW_TAG [--commits FILE]"""
import json
import sys

LOWER_IS_BETTER = {"p95_latency_ms", "brier", "log_loss", "rmse"}


def verdict(name, delta):
    if abs(delta) < 1e-12:
        return "same"
    better = delta < 0 if name in LOWER_IS_BETTER else delta > 0
    return "better" if better else "WORSE"


def render(old, new, old_tag, new_tag, commits=()):
    out = [f"# {new['model']} v{new['version']} ({new_tag})", ""]
    out += ["| Field | Value |", "|---|---|",
            f"| Model version | {new['version']} |",
            f"| Data version | {new['data_version']} (was {old['data_version']}) |",
            f"| Git SHA | {new['git_sha']} |",
            f"| Rollback target | {old['model']} v{old['version']} ({old_tag}) |", ""]
    out += ["## Metrics versus previous champion", "",
            "| Metric | Old | New | Change | Verdict |", "|---|---|---|---|---|"]
    for k in sorted(new["metrics"]):
        n = new["metrics"][k]
        o = old["metrics"].get(k)
        if o is None:
            out.append(f"| {k} | n/a | {n:.3f} | n/a | new metric |")
            continue
        d = n - o
        out.append(f"| {k} | {o:.3f} | {n:.3f} | {d:+.3f} | {verdict(k, d)} |")
    out += ["", f"## What changed ({old_tag}..{new_tag})", ""]
    out += [f"- {c}" for c in commits] or ["- (no commit list supplied)"]
    out += ["", "## Known limitations", ""]
    out += [f"- {x}" for x in new.get("limitations", [])] or ["- none recorded (fill this in, do not leave it empty)"]
    return "\n".join(out)


if __name__ == "__main__":
    args = sys.argv[1:]
    commits = []
    if "--commits" in args:
        i = args.index("--commits")
        commits = [l.strip() for l in open(args[i + 1]) if l.strip()]
        del args[i:i + 2]
    old = json.load(open(args[0])); new = json.load(open(args[1]))
    print(render(old, new, args[2], args[3], commits))
```
```bash
# --- q25/run.sh ---
V=/tmp/claude-0/b7p07/v/bin
D=$(dirname "$(readlink -f "$0")")
W=/tmp/claude-0/b7_q21_30/q25; rm -rf $W; mkdir -p $W; cd $W
git init -q . && git config user.email t@example.com && git config user.name t
echo a > f; git add f; git commit -qm "Initial training pipeline"; git tag -a model-v3.0.0 -m v3
echo b > f; git commit -qam "Add tenure feature"; echo c > f; git commit -qam "Retrain on October data"; git tag -a model-v4.0.0 -m v4
echo '$ git log --pretty=format:%s model-v3.0.0..model-v4.0.0 > commits.txt'
git log --pretty=format:%s model-v3.0.0..model-v4.0.0 > commits.txt; cat commits.txt; echo
echo '$ python3 -I release_notes.py old_metrics.json new_metrics.json model-v3.0.0 model-v4.0.0 --commits commits.txt'
$V/python -I $D/release_notes.py $D/old_metrics.json $D/new_metrics.json model-v3.0.0 model-v4.0.0 --commits commits.txt
```
**Output (my run):** the metrics values and git SHAs in the JSON are sample data I made up, not from a real model; the commit messages come from a real temp git repo with tags `model-v3.0.0` and `model-v4.0.0`.

```text
$ git log --pretty=format:%s model-v3.0.0..model-v4.0.0 > commits.txt
Retrain on October data
Add tenure feature
$ python3 -I release_notes.py old_metrics.json new_metrics.json model-v3.0.0 model-v4.0.0 --commits commits.txt
# churn v4 (model-v4.0.0)

| Field | Value |
|---|---|
| Model version | 4 |
| Data version | customers-2026-10 (was customers-2026-09) |
| Git SHA | e4f5a6b |
| Rollback target | churn v3 (model-v3.0.0) |

## Metrics versus previous champion

| Metric | Old | New | Change | Verdict |
|---|---|---|---|---|
| auc | 0.842 | 0.851 | +0.009 | better |
| brier | 0.121 | 0.118 | -0.003 | better |
| p95_latency_ms | 38.000 | 41.500 | +3.500 | WORSE |
| recall_at_10pct | 0.410 | 0.432 | +0.022 | better |

## What changed (model-v3.0.0..model-v4.0.0)

- Retrain on October data
- Add tenure feature

## Known limitations

- Weak on customers under 30 days old
- Not validated for the business plan
```
Not executed: creating a GitHub Release (for example `gh release create model-v4.0.0 --notes-file notes.md`; check current docs) and the permissions it needs (`contents: write`).

**Follow-ups:**
- *Where does the old metrics file come from?* The registry (the champion version's logged metrics) or a stored artifact of the previous release run.
- *Semantic versioning for models?* Often: major for a changed feature contract, minor for retrain with the same contract, patch for fixes. State your convention.
- *Conventional commits?* They make the changelog cleaner, but even plain commit subjects work.

**Common mistakes:**
- Writing notes by hand after the fact.
- Showing only improvements.
- Forgetting the rollback target.
- Using a floating tag such as `latest` as the reference.

### Q26 ⭐⭐ 🟡 Tie shadow and canary stages into the promotion pipeline. Explain the stages staging smoke test, shadow (mirror traffic, compare outputs), canary at 5 percent, then full rollout, automatic abort criteria (error rate, p99, prediction distribution shift), a minimum sample before judging, who moves traffic (an Argo Rollouts, Flagger or KServe canary at concept level, or a router config in Git) and why a canary cannot see a slow quality regression that needs labels. Implement a promotion state machine in Python that advances or aborts from per-stage metrics, with tests, and run it. Rollout mechanics belong to Part 6 and Part 3; real traffic splitting is not executed.
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | GitOps comparison posts (devtron.ai, codefresh.io, earthly.dev, harness.io, oneuptime.com 2026 Argo CD versus Flux; search snippets only, not opened); vendor and editorial blogs, nothing found on ML-specific GitOps or interview lists; platform and DevOps roles with ML workloads
**Say this first (1 line):** Promotion is a staged ladder, staging smoke test, then shadow, then 5 percent canary, then full, and each stage advances only if its metrics pass with enough traffic, otherwise it aborts back to the champion.

**Then explain:**
- Stages: staging smoke test (does it start, answer, match a golden set); shadow (mirror real requests to the candidate, log its outputs, compare with the champion, users never see them); canary at 5 percent (real users see it); full rollout.
- Abort criteria: error rate, p99 latency, and prediction distribution shift against the champion (PSI or similar). Write the numbers in Git, not in someone's head.
- Minimum sample: with 20 requests an error rate means nothing. The state machine says "wait", not "advance" and not "abort".
- Who moves traffic: a rollout tool (Argo Rollouts, Flagger, or a KServe canary, concept level, check current docs) or a router config in Git. The state machine decides; the tool does the traffic split. Rollout mechanics are in Part 6 and Part 3.
- What a canary cannot see: a slow quality regression that needs labels (churn labels arrive weeks later, loan defaults take months). The canary protects against crashes, slowness and wild outputs. Quality needs shadow comparison on proxy metrics plus delayed-label monitoring (Part 8) and a rollback plan.
- Failure modes: judging too early, a metric that is not segmented (the bad segment is 3 percent of traffic), forgetting to roll back traffic on abort, and a shadow path that adds latency or writes to production state.

**Example:** Canary p99 is 480 ms against a 250 ms limit with 5000 requests: abort. The same canary with 400 requests and an error rate of 50 percent: wait, do not judge.

**Code:** `judge()` is a pure function; `Promotion` holds the state. Pytest covers the happy path, each abort rule, too few requests, and stepping after abort.

```python
# --- q26/rollout.py ---
"""Promotion state machine: staging -> shadow -> canary5 -> full. Aborts on bad metrics."""
from dataclasses import dataclass

STAGES = ["staging", "shadow", "canary5", "full"]


@dataclass(frozen=True)
class Criteria:
    max_error_rate: float = 0.01
    max_p99_ms: float = 250.0
    max_psi: float = 0.2          # prediction distribution shift versus champion
    min_requests: int = 1000      # do not judge on fewer


def judge(stage, m, c=Criteria()):
    """Return ('advance'|'wait'|'abort', reason) for one stage's metrics."""
    if stage == "staging":  # smoke test: pass/fail only
        return ("advance", "smoke ok") if m["smoke_passed"] else ("abort", "smoke test failed")
    if m["requests"] < c.min_requests:
        return "wait", f"only {m['requests']} requests (< {c.min_requests})"
    if m["error_rate"] > c.max_error_rate:
        return "abort", f"error rate {m['error_rate']:.3f} > {c.max_error_rate}"
    if m["p99_ms"] > c.max_p99_ms:
        return "abort", f"p99 {m['p99_ms']}ms > {c.max_p99_ms}ms"
    if m["psi"] > c.max_psi:
        return "abort", f"prediction PSI {m['psi']} > {c.max_psi}"
    return "advance", "metrics within limits"


class Promotion:
    def __init__(self):
        self.stage, self.state, self.log = "staging", "running", []

    def step(self, metrics):
        if self.state != "running":
            raise RuntimeError(f"promotion already {self.state}")
        verdict, why = judge(self.stage, metrics)
        self.log.append((self.stage, verdict, why))
        if verdict == "abort":
            self.state = "aborted"  # traffic goes back to champion (done by the router/rollout tool)
        elif verdict == "advance":
            self.stage = STAGES[STAGES.index(self.stage) + 1]
            if self.stage == "full":
                self.state = "done"  # 100% traffic reached; keep watching with normal monitoring
        return verdict

# --- q26/test_rollout.py ---
import pytest

from rollout import Promotion, judge

OK = {"requests": 5000, "error_rate": 0.002, "p99_ms": 120, "psi": 0.05}


def run(seq):
    p = Promotion()
    for m in seq:
        p.step(m)
    return p


def test_happy_path_reaches_full():
    p = run([{"smoke_passed": True}, OK, OK])
    assert (p.stage, p.state) == ("full", "done")


def test_smoke_failure_aborts_at_staging():
    p = run([{"smoke_passed": False}])
    assert (p.stage, p.state) == ("staging", "aborted")


def test_too_few_requests_waits_not_advances():
    p = Promotion(); p.step({"smoke_passed": True})
    assert p.step({**OK, "requests": 50}) == "wait"
    assert p.stage == "shadow" and p.state == "running"


@pytest.mark.parametrize("bad,key", [({"error_rate": 0.05}, "error"), ({"p99_ms": 900}, "p99"), ({"psi": 0.4}, "PSI")])
def test_each_abort_criterion(bad, key):
    v, why = judge("canary5", {**OK, **bad})
    assert v == "abort" and key in why


def test_cannot_step_after_abort():
    p = run([{"smoke_passed": False}])
    with pytest.raises(RuntimeError):
        p.step(OK)


def test_low_volume_bad_metrics_is_not_judged():
    assert judge("canary5", {**OK, "requests": 10, "error_rate": 0.5})[0] == "wait"

# --- q26/demo.py ---
import sys; sys.path.insert(0, ".")
from rollout import Promotion
OK = {"requests": 5000, "error_rate": 0.002, "p99_ms": 120, "psi": 0.05}
for title, seq in [
    ("good candidate", [{"smoke_passed": True}, OK, {**OK, "requests": 400}, OK]),
    ("bad canary", [{"smoke_passed": True}, OK, {**OK, "p99_ms": 480}]),
]:
    p = Promotion()
    print("==", title)
    for m in seq:
        v = p.step(m)
        print(f"  {p.log[-1][0]:8s} {v:8s} {p.log[-1][2]}")
    print("  final:", p.stage, p.state)
```
```bash
# --- q26/run.sh ---
V=/tmp/claude-0/b7p07/v/bin
D=$(dirname "$(readlink -f "$0")")
export PYTHONDONTWRITEBYTECODE=1; cd $D
echo '$ pytest -q -p no:cacheprovider test_rollout.py'; $V/pytest -q -p no:cacheprovider test_rollout.py
echo '$ python3 -I demo.py'; $V/python -I demo.py
```
**Output (my run):**

```text
$ pytest -q -p no:cacheprovider test_rollout.py
........                                                                 [100%]
8 passed in 0.02s
$ python3 -I demo.py
== good candidate
  staging  advance  smoke ok
  shadow   advance  metrics within limits
  canary5  wait     only 400 requests (< 1000)
  canary5  advance  metrics within limits
  final: full done
== bad canary
  staging  advance  smoke ok
  shadow   advance  metrics within limits
  canary5  abort    p99 480ms > 250.0ms
  final: canary5 aborted
```
Not executed: real traffic splitting, Argo Rollouts, Flagger, KServe or a service mesh. This is only the decision logic, with metric values I made up.

**Follow-ups:**
- *Why shadow before canary?* No user risk; you can compare outputs on real traffic.
- *How long should a canary run?* Until the minimum sample is met and across a normal traffic cycle (for example a daily peak). I would not give a fixed number.
- *Automatic or manual advance?* Automatic abort always; advance can need a person for risky models.

**Common mistakes:**
- Aborting or advancing on tiny samples.
- Believing the canary proves model quality.
- No automatic rollback, only an alert.
- Keeping abort thresholds in the rollout tool UI instead of Git.

### Q27 ⭐⭐ 🟡 Fairness and slice checks as a promotion gate. Explain choosing protected or business-relevant groups, per-group metrics (selection rate, true positive rate, false positive rate), a ratio or gap threshold (the four-fifths rule is a common illustrative threshold, not a universal legal standard), small-group sample sizes and confidence, gating on a no-worse-than-champion rule per slice, and what to do when overall AUC improves but one slice regresses. Implement the check on synthetic data with numpy and pandas and a gate that exits non-zero, run it for a fair and an unfair candidate, and note that regulatory expectations for Indian lending or hiring models must be checked in current official sources.
**Asked at:** Continuous Machine Learning (CML) sources (github.com/iterative/cml repository page, dvc.org, medium/towardsdatascience CML tutorial; search snippets only, not opened; nothing found on fairness gates or registry promotion); tool docs and tutorials, not interview reports; ML engineer and MLOps roles using DVC and GitHub | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Before promotion I compute per-group metrics, fail the gate if group gaps or ratios are too wide or a slice is worse than the champion, and exit non-zero so the pipeline stops, even when overall AUC went up.

**Then explain:**
- Choose groups with the business and legal or risk team: protected attributes where you are allowed to hold and use them for testing, plus business slices (new customers, region, device). Write the list in Git.
- Per-group metrics: selection rate (share predicted positive), true positive rate, false positive rate. Which one matters depends on harm: for loans, a low TPR for a group means deserving applicants are rejected.
- Thresholds: ratio of selection rates (the four-fifths or 0.8 rule is a common illustrative threshold, not a universal legal standard) and gaps in TPR and FPR. Pick them with the owners and put them in the gates YAML.
- Small groups: with n too small the metric is noise. Enforce a minimum group size and send small groups to manual review instead of passing silently. Confidence intervals help; here I use a minimum count.
- No-worse-than-champion per slice: the candidate's TPR in each slice may not drop more than a small tolerance against the champion.
- When overall AUC improves but one slice regresses: do not ship automatically. Look for cause (data coverage, a feature that behaves differently), consider retraining with more data for that slice, or ship only with explicit sign-off and a documented reason. Do not average the problem away.
- Regulation: for Indian lending or hiring models, check current official sources (regulator circulars, data protection law). I am not quoting any rule here.
- Failure modes: using a protected attribute as a feature without thinking, proxies (pincode) that still leak, testing on a stale sample, and a gate with so many metrics that everything fails and people disable it.

**Example:** Fair candidate: groups A, B, C all around 35 percent selected and TPR about 0.71, so it passes. Unfair candidate: group C is pushed down; its selection rate is 0.144 against 0.350 for group A (ratio 0.41), so the gate fails on ratio, TPR gap, FPR gap and slice regression.

**Code:** numpy and pandas on synthetic data (the synthetic generator and the group shift are mine, to demonstrate the gate; the data is not real).

```python
# --- q27/fairness_gate.py ---
"""Per-slice gate: selection-rate ratio, TPR gap, FPR gap, no-worse-than-champion. Exit 1 on failure."""
import sys

import numpy as np
import pandas as pd

MIN_GROUP = 200
MIN_RATIO = 0.80      # illustrative four-fifths style threshold, NOT a legal standard
MAX_TPR_GAP = 0.10
MAX_FPR_GAP = 0.10
SLICE_TOL = 0.02      # candidate TPR may be at most this much below champion, per slice


def make_data(seed=0, n=6000):
    rng = np.random.default_rng(seed)
    group = rng.choice(["A", "B", "C"], size=n, p=[0.55, 0.35, 0.10])
    y = rng.binomial(1, 0.30, n)
    signal = y * 1.5 + rng.normal(0, 1, n)
    return pd.DataFrame({"group": group, "y": y, "signal": signal})


def predictions(df, shift_by_group):
    """Decision = signal above 0.9, plus a group-specific shift (the unfairness knob)."""
    s = df["signal"] + df["group"].map(shift_by_group).fillna(0.0)
    return (s > 0.9).astype(int)


def group_metrics(df, pred):
    rows = {}
    for g, d in df.assign(pred=pred).groupby("group"):
        pos, neg = d[d.y == 1], d[d.y == 0]
        rows[g] = {"n": len(d), "sel": d.pred.mean(), "tpr": pos.pred.mean(), "fpr": neg.pred.mean()}
    return pd.DataFrame(rows).T


def gate(df, cand_pred, champ_pred):
    cm, hm = group_metrics(df, cand_pred), group_metrics(df, champ_pred)
    fails = []
    for g, r in cm.iterrows():
        if r.n < MIN_GROUP:
            fails.append(f"group {g}: n={int(r.n)} < {MIN_GROUP}, too small to judge (manual review)")
    ok = cm[cm.n >= MIN_GROUP]
    ratio = ok.sel.min() / ok.sel.max()
    if ratio < MIN_RATIO:
        fails.append(f"selection-rate ratio {ratio:.2f} < {MIN_RATIO} ({ok.sel.idxmin()} vs {ok.sel.idxmax()})")
    if ok.tpr.max() - ok.tpr.min() > MAX_TPR_GAP:
        fails.append(f"TPR gap {ok.tpr.max() - ok.tpr.min():.2f} > {MAX_TPR_GAP}")
    if ok.fpr.max() - ok.fpr.min() > MAX_FPR_GAP:
        fails.append(f"FPR gap {ok.fpr.max() - ok.fpr.min():.2f} > {MAX_FPR_GAP}")
    for g in ok.index:
        if cm.loc[g, "tpr"] < hm.loc[g, "tpr"] - SLICE_TOL:
            fails.append(f"group {g}: TPR {cm.loc[g, 'tpr']:.2f} worse than champion {hm.loc[g, 'tpr']:.2f}")
    return cm, fails


if __name__ == "__main__":
    which = sys.argv[1]  # fair | unfair
    df = make_data()
    champ = predictions(df, {})
    cand = predictions(df, {} if which == "fair" else {"C": -0.9})
    cm, fails = gate(df, cand, champ)
    print(f"candidate = {which}")
    print(cm.round(3).to_string())
    for f in fails:
        print("FAIL", f)
    print("GATE:", "FAIL" if fails else "PASS")
    sys.exit(1 if fails else 0)
```
```bash
# --- q27/run.sh ---
V=/tmp/claude-0/b7p07/v/bin
D=$(dirname "$(readlink -f "$0")")
for w in fair unfair; do echo "\$ python3 -I fairness_gate.py $w"; $V/python -I $D/fairness_gate.py $w; echo "exit=$?"; done
```
**Output (my run):** numpy 2.5.4, pandas 3.1.0.

```text
$ python3 -I fairness_gate.py fair
candidate = fair
        n    sel    tpr    fpr
A  3296.0  0.350  0.715  0.192
B  2135.0  0.348  0.711  0.193
C   569.0  0.351  0.711  0.194
GATE: PASS
exit=0
$ python3 -I fairness_gate.py unfair
candidate = unfair
        n    sel    tpr    fpr
A  3296.0  0.350  0.715  0.192
B  2135.0  0.348  0.711  0.193
C   569.0  0.144  0.376  0.043
FAIL selection-rate ratio 0.41 < 0.8 (C vs A)
FAIL TPR gap 0.34 > 0.1
FAIL FPR gap 0.15 > 0.1
FAIL group C: TPR 0.38 worse than champion 0.71
GATE: FAIL
exit=1
```
Both runs used the same data and the same champion; only the candidate differs. Exit code 1 is what makes CI go red.

**Follow-ups:**
- *Is equal selection rate always the goal?* No. Different base rates can make equal selection rates and equal TPR conflict. Pick the metric that matches the harm, and explain it.
- *What about intersections (gender and region)?* Slices multiply and shrink; start with the key ones and watch sample sizes.
- *Can CI decide fairness alone?* No. It catches regressions against a policy people agreed; the policy itself needs review.

**Common mistakes:**
- Only reporting overall metrics.
- Judging a group with a handful of rows.
- Treating 0.8 as law.
- Dropping the protected column and assuming the model is fair (proxies remain, and you can no longer measure the gap).

### Q28 ⭐⭐ 🟡 How do you test and debug a GitHub Actions workflow you cannot run locally? Explain actionlint and check-jsonschema in pre-commit and CI, the schema check versus semantic check difference, workflow_dispatch for manual runs on a branch, step debug logging, small reproducible workflows, pinning action versions, why act (a local runner) is not a full substitute and was not available here, and the fact that tokens, OIDC and environments cannot be tested locally. Run actionlint and check-jsonschema on three broken workflows (bad event, missing needs, unknown runner label) and show the real messages.
**Asked at:** GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** I cannot fully run GitHub Actions on my laptop, so I lint the workflow with actionlint and check-jsonschema, test logic in scripts I can run locally, and use `workflow_dispatch` on a branch for the real run.

**Then explain:**
- check-jsonschema validates the YAML structure against the GitHub workflow schema (is this a valid shape). actionlint understands workflows: event names, `needs` references, runner labels, expressions, shell scripts, injection risks. They overlap but catch different things.
- Run both locally via pre-commit and again in CI, so a bad workflow cannot reach main. Pin the versions of both tools.
- `workflow_dispatch` gives a manual Run button on a branch with inputs; use a small throwaway workflow to reproduce a problem. Step debug logging: set the secret or variable `ACTIONS_STEP_DEBUG` to `true` and re-run to see `::debug::` lines (check current docs for exact current names).
- Pin third-party actions, ideally to a full commit SHA (a tag can be moved; the tj-actions compromise in March 2025 is the usual example). Pin tool versions too.
- `act` runs workflows locally in Docker, but it is not a full substitute (runner images differ, many contexts and services are missing) and it was not available here, so I did not run it.
- Cannot be tested locally: the `GITHUB_TOKEN`, OIDC token exchange, environments and required reviewers, secrets, and real runner images. Test those in a sandbox repository.
- Failure modes: a green lint with a wrong logic, `on:` typos in a file that GitHub just ignores, and a workflow on a branch that never triggers because the file is not on the default branch for the event.

**Example:** `pull_requests:` (typo for `pull_request`) means the workflow never runs on PRs. No test failed, nothing is red, it just silently does nothing. Linters catch it.

**Code:** three broken workflows (bad event, missing `needs`, unknown runner label) plus a good one with `workflow_dispatch`, and an example pre-commit config (not executed).

```yaml
# --- q28/broken/bad_event.yml ---
name: bad-event
on:
  pull_requests:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest

# --- q28/broken/missing_needs.yml ---
name: missing-needs
on: [push]
jobs:
  deploy:
    needs: [test]
    runs-on: ubuntu-latest
    steps:
      - run: echo deploying
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo building

# --- q28/broken/unknown_label.yml ---
name: unknown-label
on: [push]
jobs:
  smoke:
    runs-on: [self-hosted, gpu]
    steps:
      - run: nvidia-smi

# --- q28/good_dispatch.yml ---
name: debuggable
on:
  workflow_dispatch:
    inputs:
      debug:
        description: "Print extra info"
        type: boolean
        default: false
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Show context
        if: ${{ inputs.debug }}
        run: |
          echo "ref=${{ github.ref }}"
          python --version
      - run: echo "::debug::this line only shows with ACTIONS_STEP_DEBUG=true"

# --- q28/pre-commit-config.yaml ---
# Not executed here (pre-commit not installed in the test venv). Pin rev to a real release tag, check current docs.
repos:
  - repo: https://github.com/rhysd/actionlint
    rev: v1.7.12
    hooks:
      - id: actionlint
  - repo: https://github.com/python-jsonschema/check-jsonschema
    rev: 0.38.2
    hooks:
      - id: check-github-workflows
```
```bash
# --- q28/run.sh ---
V=/tmp/claude-0/b7p07/v/bin
D=$(dirname "$(readlink -f "$0")"); cd $D
for f in broken/bad_event.yml broken/missing_needs.yml broken/unknown_label.yml good_dispatch.yml; do
  echo "=== $f"
  echo "\$ actionlint $f"; $V/actionlint $f; echo "exit=$?"
  echo "\$ check-jsonschema --builtin-schema vendor.github-workflows $f"; $V/check-jsonschema --builtin-schema vendor.github-workflows $f; echo "exit=$?"
done
```
**Output (my run):** actionlint 1.7.12 and check-jsonschema 0.38.2 with the built-in `vendor.github-workflows` schema (works offline).

```text
=== broken/bad_event.yml
$ actionlint broken/bad_event.yml
broken/bad_event.yml:3:3: unknown Webhook event "pull_requests". see https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#webhook-events for list of all Webhook event names [events]
  |
3 |   pull_requests:
  |   ^~~~~~~~~~~~~~
exit=1
$ check-jsonschema --builtin-schema vendor.github-workflows broken/bad_event.yml
Schema validation errors were encountered.
  broken/bad_event.yml::$.on: {'pull_requests': {'branches': ['main']}} is not valid under any of the given schemas
  Underlying errors caused this.

  Best Match:
    $.on: {'pull_requests': {'branches': ['main']}} is not of type 'string'

  3 other errors were produced. Use '--verbose' to see all errors.
exit=1
=== broken/missing_needs.yml
$ actionlint broken/missing_needs.yml
broken/missing_needs.yml:4:3: job "deploy" needs job "test" which does not exist in this workflow [job-needs]
  |
4 |   deploy:
  |   ^~~~~~~
exit=1
$ check-jsonschema --builtin-schema vendor.github-workflows broken/missing_needs.yml
ok -- validation done
exit=0
=== broken/unknown_label.yml
$ actionlint broken/unknown_label.yml
broken/unknown_label.yml:5:28: label "gpu" is unknown. available labels are "windows-latest", "windows-latest-8-cores", "windows-2025", "windows-2025-vs2026", "windows-2022", "windows-11-arm", "ubuntu-slim", "ubuntu-latest", "ubuntu-latest-4-cores", "ubuntu-latest-8-cores", "ubuntu-latest-16-cores", "ubuntu-24.04", "ubuntu-24.04-arm", "ubuntu-22.04", "ubuntu-22.04-arm", "macos-latest", "macos-latest-xlarge", "macos-latest-large", "macos-26-intel", "macos-26-xlarge", "macos-26-large", "macos-26", "macos-15-intel", "macos-15-xlarge", "macos-15-large", "macos-15", "macos-14-xlarge", "macos-14-large", "macos-14", "self-hosted", "x64", "arm", "arm64", "linux", "macos", "windows". if it is a custom label for self-hosted runner, set list of labels in actionlint.yaml config file [runner-label]
  |
5 |     runs-on: [self-hosted, gpu]
  |                            ^~~~
exit=1
$ check-jsonschema --builtin-schema vendor.github-workflows broken/unknown_label.yml
ok -- validation done
exit=0
=== good_dispatch.yml
$ actionlint good_dispatch.yml
exit=0
$ check-jsonschema --builtin-schema vendor.github-workflows good_dispatch.yml
ok -- validation done
exit=0
$ python3 -I -c "import yaml;print(list(yaml.safe_load(open(\"pre-commit-config.yaml\"))))"
['https://github.com/rhysd/actionlint', 'https://github.com/python-jsonschema/check-jsonschema']
```
The key lesson is in the middle: check-jsonschema says `ok` for the missing-`needs` file and the unknown-label file, while actionlint catches both. The schema check cannot know that job `test` does not exist or that `gpu` is not a configured label. For the unknown label the fix is a `.github/actionlint.yaml` with `self-hosted-runner: labels: [gpu]` (see the self-hosted runner question). The pre-commit config was only parsed with PyYAML (last lines of the output file); the hooks were not run. A real run of any workflow was not executed.

**Follow-ups:**
- *Why does GitHub not show an error for a bad `on:`?* Depends on the typo; some invalid files show a red "workflow file issue", others just never trigger. Lint before pushing.
- *How do you debug a failing step?* Re-run with debug logging, add `env | sort` carefully (never print secrets), or reproduce the step as a script.
- *Can you test OIDC locally?* No. Use a sandbox cloud account with a narrow trust policy.

**Common mistakes:**
- Trusting a schema check as if it were a full check.
- Debugging on main by pushing many commits.
- Using `act` results as proof that production CI works.
- Printing secrets during debugging.

### Q29 ⭐⭐ 🟡 Branch protection and required status checks for an ML repository. Explain required checks by job name, requiring a pull request and review, CODEOWNERS on the model, config and gate-threshold directories, dismissing stale approvals, and the trap that a path-filtered workflow that does not run leaves a required check pending forever (and the fix with an always-running summary job or a changed-files step, check current docs). Show the workflow with the summary job and validate it with actionlint. The GitHub settings themselves are not executed.
**Asked at:** GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD | MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** I protect main with required PR review, CODEOWNERS and required status checks, and I make only one always-running summary job the required check, so path filters can never leave a required check stuck.

**Then explain:**
- Required status checks are matched by job name (the check name shown on the PR). Rename a job and the required check silently stops matching, so changes to required names need care.
- Require a pull request and at least one review, and dismiss stale approvals when new commits are pushed, so an approval does not carry over to code nobody reviewed.
- CODEOWNERS: `models/`, `configs/` and the gate-threshold file need the ML lead (or a risk owner). Turn on "require review from code owners" in branch protection. Changing a threshold then needs the owner's approval.
- The trap: a workflow with `paths:` filters does not start for a docs-only PR. If its job is marked required, the check never reports and the PR shows "Expected, waiting for status" forever. A skipped job via `if:` reports as skipped (which counts as passing), but a workflow that never started reports nothing. Check current docs for the exact behaviour.
- The fix: the workflow always runs (no `paths:` on the trigger), a first job computes changed files, heavy jobs use `if:` on that output, and a final job `ci-ok` with `if: always()` and `needs: [...]` fails if any needed job failed or was cancelled. Only `ci-ok` is required.
- Failure modes: `ci-ok` missing `if: always()`. When a needed job fails, a dependent job without it is skipped, and a skipped job reports as success, so the required check goes green on a broken PR (verify in a sandbox repo). Also admins allowed to bypass, and fork PRs having restricted secrets.

**Example:** Docs-only PR: `lint` passes, `model-gate` is skipped by the changes check, `ci-ok` runs and passes, PR is mergeable. A PR that changes `configs/gates.yaml`: `model-gate` runs and if it fails, `ci-ok` fails.

**Code:** the workflow with the summary job, a trap workflow for contrast, and a Python mirror of the summary rule to check the truth table by hand. CODEOWNERS is shown inside the comment of the YAML block as an example.

```yaml
# --- q29/ci.yml ---
name: ci
on:
  pull_request:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      model: ${{ steps.diff.outputs.model }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - id: diff
        run: |
          if git diff --name-only "origin/${{ github.base_ref }}...HEAD" | grep -qE '^(models/|configs/|train/)'; then
            echo "model=true" >> "$GITHUB_OUTPUT"
          else
            echo "model=false" >> "$GITHUB_OUTPUT"
          fi

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff && ruff check .

  model-gate:
    needs: changes
    if: needs.changes.outputs.model == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python gate.py --config configs/gates.yaml

  ci-ok:
    # The ONLY check marked "required" in branch protection.
    if: always()
    needs: [lint, model-gate]
    runs-on: ubuntu-latest
    steps:
      - name: Fail if any needed job failed or was cancelled (skipped is fine)
        if: ${{ contains(needs.*.result, 'failure') || contains(needs.*.result, 'cancelled') }}
        run: |
          echo "a required job did not pass"
          exit 1
      - run: echo "all needed jobs passed or were skipped"

# --- q29/trap.yml ---
name: model-tests
on:
  pull_request:
    paths: ["models/**", "configs/**"]   # docs-only PR: workflow never starts
jobs:
  model-gate:                              # required check name stays "Expected - Waiting"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python gate.py
```
```python
# --- q29/summary_rule.py ---
# A Python mirror of the ci-ok rule, to hand-check the truth table. It is NOT the GitHub evaluator.
def ci_ok(results):
    return not any(r in ("failure", "cancelled") for r in results)

cases = [
    ("docs-only PR: lint success, model-gate skipped", ["success", "skipped"]),
    ("model PR, all green", ["success", "success"]),
    ("model-gate failure", ["success", "failure"]),
    ("lint cancelled", ["cancelled", "success"]),
]
for name, r in cases:
    print(f"{name:50s} -> {'mergeable' if ci_ok(r) else 'blocked'}")
```
```bash
# --- q29/run.sh ---
V=/tmp/claude-0/b7p07/v/bin
D=$(dirname "$(readlink -f "$0")"); cd $D
echo '$ actionlint ci.yml'; $V/actionlint ci.yml; echo "exit=$?"
echo '$ check-jsonschema --builtin-schema vendor.github-workflows ci.yml'; $V/check-jsonschema --builtin-schema vendor.github-workflows ci.yml; echo "exit=$?"
echo "\$ python3 -I summary_rule.py"; $V/python -I summary_rule.py
```
**Output (my run):** actionlint 1.7.12 and the vendored schema.

```text
$ actionlint ci.yml
exit=0
$ check-jsonschema --builtin-schema vendor.github-workflows ci.yml
ok -- validation done
exit=0
$ python3 -I summary_rule.py
docs-only PR: lint success, model-gate skipped     -> mergeable
model PR, all green                                -> mergeable
model-gate failure                                 -> blocked
lint cancelled                                     -> blocked
$ actionlint trap.yml (valid file, but a trap in branch protection)
exit=0
```
Both workflows are syntactically valid; the trap is a behaviour of branch protection, which actionlint cannot see. The truth table comes from my own Python mirror of the rule, not from GitHub's evaluator. Not executed: the branch protection or ruleset settings, CODEOWNERS enforcement, stale-approval dismissal, and the real "pending forever" behaviour. Those need a GitHub repository. A CODEOWNERS file would look like this:

```text
/models/                @ml-leads
/configs/gates.yaml     @ml-leads @risk-owners
/.github/workflows/     @platform-team
```

**Follow-ups:**
- *Branch protection or rulesets?* GitHub now also has rulesets; check current docs for which to use.
- *Why not require each job?* Names change and path-filtered jobs may not exist. One stable summary name is simpler.
- *Do skipped jobs pass?* A job skipped by a job-level condition reports as skipped and does not block merging; a workflow that never started reports nothing and stays pending. Check current docs.

**Common mistakes:**
- Requiring a path-filtered job directly.
- Summary job without `if: always()`.
- No CODEOWNERS on the gate thresholds.
- Letting admins bypass for routine merges.

### Q30 ⭐⭐ 🟡 Reduce CI cost and time for an ML repository whose PR build takes 40 minutes. List the levers: path filters, cache, test splitting and parallelism, a tiny smoke dataset, moving heavy jobs to nightly, cancel-in-progress, smaller runners for lint, fail-fast ordering (lint before tests), and measuring before changing. Without quoting any prices, write a script that models total billed runner-minutes for 50 PRs a week under a matrix (jobs times minutes) before and after the changes and prints the saving, run it, and say real billed minutes depend on runner type (check current docs).
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** First measure which jobs cost the most minutes and time, then cut the biggest ones: skip work that is not needed, cache, shard, shrink the data in PR runs, and move the heavy full-data run to nightly.

**Then explain:**
- Measure first: per-job duration and how often each job runs. Optimise the top one, not the one that annoys you.
- Levers: path filters (docs-only PRs skip heavy jobs), dependency cache, test splitting across shards, a tiny smoke dataset in PR CI, heavy jobs nightly or on merge, `cancel-in-progress` so an old push does not keep burning minutes, a smaller runner for lint, and fail-fast ordering (lint before tests).
- Wall-clock and billed minutes are different. Sharding cuts wall-clock but total billed minutes stay about the same (or rise a bit from setup repeated per shard). Skipping, caching and cancelling cut billed minutes.
- Do not lose coverage: if the full-data run moves to nightly, someone must own the nightly failure, and releases must still run it.
- Failure modes: a cache that never hits (key changes every run), a smoke dataset that no longer catches real bugs, a nightly job nobody watches, and a matrix that grows because someone added another Python version.
- Billing: minutes are rounded per job and depend on runner type (OS, size, hosted or self-hosted). I use no prices; check current docs.

**Example:** Before: 4 jobs, `unit` in a 3-way matrix. One run is 3 + 3x12 + 20 + 8 = 67 billed minutes. With 50 PRs x 3 pushes that is 10050 minutes per week. Changes: smaller lint, cache and sharding, smoke data, cheaper docker build, path filter, cancel-in-progress, full data nightly. Model result below.

**Code:** a model with assumptions I made up (all inputs are labelled and are meant to be replaced with measured values from your own runs), plus a workflow showing the levers.

```python
# --- q30/ci_cost.py ---
"""Model billed runner-minutes per week. ALL inputs are assumptions to replace with measured values."""
import math

PRS_PER_WEEK = 50
PUSHES_PER_PR = 3          # each push starts a run

# (job name, copies in matrix, minutes per copy). Billing rounds each job up to whole minutes.
BEFORE = [("lint", 1, 3.0), ("unit", 3, 12.0), ("integration-full-data", 1, 20.0), ("docker-build", 1, 8.0)]
AFTER = [("lint", 1, 1.5), ("unit", 3, 7.0), ("integration-smoke-data", 1, 5.0), ("docker-build", 1, 4.0)]
NIGHTLY_HEAVY = [("integration-full-data", 1, 20.0)]
NIGHTS = 7

DOCS_ONLY_SHARE = 0.30     # PRs that touch no code (path filter skips the heavy jobs)
CANCELLED_SHARE = 0.40     # pushes superseded by a newer push (cancel-in-progress)
CANCELLED_COST = 0.30      # fraction of a full run a cancelled run still burns


def run_minutes(jobs):
    return sum(n * math.ceil(m) for _, n, m in jobs)


def before():
    return PRS_PER_WEEK * PUSHES_PER_PR * run_minutes(BEFORE)


def after():
    pushes = PRS_PER_WEEK * PUSHES_PER_PR
    full = pushes * (1 - CANCELLED_SHARE)
    cancelled = pushes * CANCELLED_SHARE * CANCELLED_COST
    code_share = 1 - DOCS_ONLY_SHARE
    pr_cost = (full + cancelled) * (code_share * run_minutes(AFTER) + DOCS_ONLY_SHARE * math.ceil(1.0))
    return pr_cost + NIGHTS * run_minutes(NIGHTLY_HEAVY)


if __name__ == "__main__":
    b, a = before(), after()
    print(f"before: {run_minutes(BEFORE)} billed min per run x {PRS_PER_WEEK * PUSHES_PER_PR} runs = {b:.0f} min/week")
    print(f"after : {a:.0f} min/week (PR runs + {NIGHTS} nightly full-data runs)")
    print(f"saving: {b - a:.0f} min/week = {(b - a) / b:.0%}")
    print("wall clock critical path before:", 3 + 12 + 20 + 8, "min if serial (jobs can also run in parallel)")
```
```yaml
# --- q30/ci_fast.yml ---
name: ci-fast
on:
  pull_request:
    paths-ignore: ["docs/**", "**.md"]
  schedule:
    - cron: "17 21 * * *"      # nightly heavy run (UTC)
concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff && ruff check .
  unit:
    needs: lint                       # fail fast: cheap check first
    runs-on: ubuntu-latest
    strategy:
      fail-fast: true
      matrix:
        shard: [1, 2, 3]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r requirements.txt pytest pytest-split
      - run: pytest --splits 3 --group ${{ matrix.shard }}
  integration-smoke:
    needs: unit
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python train.py --data data/smoke.csv --max-rows 2000
  integration-full:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python train.py --data data/full.csv
```
**Output (my run):**

```text
$ python3 -I ci_cost.py
before: 67 billed min per run x 150 runs = 10050 min/week
after : 2592 min/week (PR runs + 7 nightly full-data runs)
saving: 7458 min/week = 74%
wall clock critical path before: 43 min if serial (jobs can also run in parallel)
$ actionlint ci_fast.yml
exit=0
$ check-jsonschema --builtin-schema vendor.github-workflows ci_fast.yml
ok -- validation done
```
The saving percentage comes from my assumptions (30 percent docs-only PRs, 40 percent of pushes superseded, and so on), so it is a method demo, not a benchmark. Real billed minutes depend on runner type and your plan (check current docs). The workflow was only linted: it was not executed on GitHub, and `pytest-split` options and cache behaviour were not run.

**Follow-ups:**
- *Does sharding cut cost?* It cuts waiting time. Cost can go up slightly.
- *How do you keep a smoke dataset honest?* Sample it from real data, include known bad cases, and run the full set nightly.
- *Self-hosted to save money?* Maybe, but you pay in maintenance and security (Part on runners); compare honestly.

**Common mistakes:**
- Optimising before measuring.
- Cutting coverage silently.
- Counting only wall-clock time.
- Forgetting that cancelled runs still burn some minutes.

### Q31 ⭐ 🔴 Supply-chain security for ML CI. Explain why tags are mutable (the March 2025 tj-actions/changed-files compromise rewrote tags, so pinning to a tag did not help while a full commit SHA did), pinning third-party actions to SHAs and updating them with Dependabot or Renovate, least-privilege permissions, pull_request_target, dependency pinning with hashes, and loading pickled models from untrusted places. Write a scanner script that flags uses: lines not pinned to a 40-character SHA and workflows without a permissions block, run it on a good and a bad sample tree and show the output.
**Asked at:** Actions supply-chain incident reports (orca.security, wiz.io, infoworld.com, phoenix.security, securityboulevard.com on the March 2025 tj-actions/changed-files compromise CVE-2025-30066; search snippets only, not opened; nothing found on SBOM or provenance attestations); security vendor posts, not interview reports; DevSecOps, platform and MLOps roles | GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD
**Say this first (1 line):** A tag like `@v4` can be moved by whoever controls that repo, so I pin every third-party action to a full 40-character commit SHA, give each workflow the least permissions it needs, never run untrusted PR code with secrets, and never unpickle a model I did not produce.

**Then explain:**
- **Tags are mutable, SHAs are not.** In the March 2025 tj-actions/changed-files compromise (CVE-2025-30066, per incident write-ups; I read search snippets, not the advisory itself) the attacker repointed existing version tags to malicious code. Anyone on `@v45` pulled it on the next run. People pinned to a SHA were safe unless they updated to a bad SHA during the window.
- **Pinning needs upkeep.** A SHA never updates by itself. Let Dependabot or Renovate open PRs that bump the SHA (keep the version in a trailing comment so humans can read it). Review the diff of the action, not just the number.
- **Permissions and triggers.** Set `permissions: contents: read` at the top, and widen per job only where needed (`id-token: write`, `packages: write`). `pull_request_target` runs with the base repo's secrets and a writable token, so never check out the PR head code in it. If a job needs both, split it into two workflows.
- **Dependencies.** Pin Python deps in a lock file and install with `pip install --require-hashes`, so a swapped package fails the hash check. The same idea applies to base images (use a digest).
- **ML-specific: pickle.** Loading a pickle runs code. A model file from a bucket, a hub or a PR artifact can own the CI runner. Prefer formats that hold only tensors (safetensors, ONNX), verify a SHA-256 against the registry, and for torch check the current `weights_only` behaviour in the docs.
- **Failure modes.** The scanner below is a lint, not a guarantee. It cannot see a SHA that is itself malicious, a compromised dependency inside a pinned action, or a `run:` step that downloads and executes a script. actionlint does not flag any of these either (shown below).

**Example:** `uses: tj-actions/changed-files@v45` means "run whatever that tag points to today". `uses: actions/checkout@<40 hex chars> # v4.2.2` means "run exactly this commit". If the maintainer's account is hijacked tomorrow, the first changes under you and the second does not.

**Code:** scanner (flags non-SHA `uses:`, missing `permissions`, `pull_request_target`, unhashed `pip install`), sample workflows, and a harmless pickle demo. The SHAs in the good sample are examples I recalled from the checkout and setup-python releases, not verified here; always copy a SHA from the action's own releases page.
```python
# --- file: scan_workflows.py ---

"""Flag unpinned third-party actions, missing permissions, risky triggers, unhashed pip installs."""
import pathlib, re, sys
import yaml

SHA = re.compile(r"^[0-9a-f]{40}$")

def triggers(doc):
    on = doc.get("on", doc.get(True))      # YAML 1.1: the key `on` loads as True
    if isinstance(on, str):
        return [on]
    return list(on) if on else []

def scan_file(path):
    problems = []
    doc = yaml.safe_load(path.read_text())
    if "permissions" not in doc:
        jobs_without = [n for n, j in doc["jobs"].items() if "permissions" not in j]
        if jobs_without:
            problems.append(f"no permissions block (top level or job: {', '.join(jobs_without)})")
    if "pull_request_target" in triggers(doc):
        problems.append("trigger pull_request_target: never check out PR head code with it")
    for jname, job in doc["jobs"].items():
        for i, step in enumerate(job.get("steps", []), 1):
            uses = step.get("uses")
            if uses and not uses.startswith("./"):
                ref = uses.split("@", 1)[1] if "@" in uses else ""
                if not SHA.match(ref):
                    problems.append(f"{jname} step {i}: '{uses}' not pinned to a 40-char SHA")
            run = step.get("run", "")
            if "pip install" in run and "--require-hashes" not in run and " -e " not in run:
                problems.append(f"{jname} step {i}: pip install without --require-hashes")
    return problems

def main(root):
    bad = 0
    for f in sorted(pathlib.Path(root).glob(".github/workflows/*.y*ml")):
        problems = scan_file(f)
        print(f"{f.relative_to(root)}: {'OK' if not problems else str(len(problems)) + ' problem(s)'}")
        for p in problems:
            print("  -", p)
        bad += len(problems)
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

# --- file: pickle_demo.py ---

"""Harmless demo: unpickling runs code. Never pickle.load a model you did not produce."""
import pickle

class Evil:
    def __reduce__(self):                 # a real attacker would return (os.system, ("...",))
        return (print, ("code ran during pickle.loads",))

blob = pickle.dumps(Evil())
pickle.loads(blob)
```
```yaml
# --- file: good/.github/workflows/ci.yml ---

name: ci
on:
  pull_request:
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b # v5.3.0
        with:
          python-version: "3.12"
      - run: pip install --require-hashes -r requirements.lock
      - run: pytest -q

# --- file: bad/.github/workflows/ci.yml ---

name: ci
on:
  pull_request_target:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - uses: tj-actions/changed-files@v45
      - uses: some-org/ml-helper@main
      - uses: ./.github/actions/local-setup
      - run: pip install -r requirements.txt
      - run: pytest -q
```
```bash
python -I scan_workflows.py good
python -I scan_workflows.py bad
actionlint bad/.github/workflows/ci.yml
```

**Output (my run):** real run of `run_all.sh` (PyYAML 6.0.3, actionlint 1.7.12 via actionlint-py, Python 3.13). The scanner finds all six problems in the bad tree. actionlint says nothing about the bad file: it checks syntax and expression types, not supply-chain policy. Not executed: Dependabot, Renovate, a real hash-checked install, any action fetch.
```text
== scan good
.github/workflows/ci.yml: OK
exit=0
== scan bad
.github/workflows/ci.yml: 6 problem(s)
  - no permissions block (top level or job: test)
  - trigger pull_request_target: never check out PR head code with it
  - test step 1: 'actions/checkout@v4' not pinned to a 40-char SHA
  - test step 2: 'tj-actions/changed-files@v45' not pinned to a 40-char SHA
  - test step 3: 'some-org/ml-helper@main' not pinned to a 40-char SHA
  - test step 5: pip install without --require-hashes
exit=1
== pickle demo
code ran during pickle.loads
== actionlint on the bad file
exit=0
== actionlint on the good file
exit=0
```

**Follow-ups:**
- *Does SHA pinning solve it?* No. It stops silent tag moves. You still review what you pin, and a pinned action can pull unpinned dependencies.
- *Why Dependabot if you pin?* A pin that is never updated misses security fixes. Bots make the update a reviewed PR.
- *How do you make CI safer for fork PRs?* Plain `pull_request` (no secrets), read-only token, and a maintainer-approved second workflow for anything that needs secrets.

**Common mistakes:**
- Pinning to `@v4` or `@main` and calling it pinned.
- Using `pull_request_target` and checking out `github.event.pull_request.head.sha`.
- No `permissions` block, so the token gets the repository default.
- `pickle.load` or `joblib.load` on a file from an untrusted bucket or PR artifact.

### Q32 ⭐ 🔴 SBOM, signing and provenance for a model image at concept level. Explain what an SBOM is (SPDX or CycloneDX, a list of components), what a signature proves (who built it) versus what provenance proves (how and from which commit), keyless signing with cosign using the OIDC identity, build provenance attestations and SLSA levels (hedge, check current docs), verifying at deploy time with an admission policy, and what changes for models (signing weights, hash of the model file). Generate a minimal CycloneDX-style JSON from pip freeze with Python and compute a SHA-256 of a model file, run them and show the output. cosign, Syft, Trivy and an admission controller are not executed.
**Asked at:** Actions supply-chain incident reports (orca.security, wiz.io, infoworld.com, phoenix.security, securityboulevard.com on the March 2025 tj-actions/changed-files compromise CVE-2025-30066; search snippets only, not opened; nothing found on SBOM or provenance attestations); security vendor posts, not interview reports; DevSecOps, platform and MLOps roles | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** An SBOM lists what is inside the image, a signature proves who produced it, provenance proves how and from which commit it was built, and the cluster should verify all that at deploy time before it runs the image.

**Then explain:**
- **SBOM** (software bill of materials): a machine-readable component list, in SPDX or CycloneDX. It answers "are we affected by this new CVE?" without unpacking images. Tools like Syft generate it from an image (concept here, not run). A list made only from your lock file misses OS packages in the base image.
- **Signature vs provenance.** A signature says "this exact digest was signed by identity X". Provenance (an in-toto or SLSA-style attestation) says "built by workflow W from commit C with these inputs". A signature alone does not tell you the build was clean; provenance alone is useless if nobody checks it.
- **Keyless signing with cosign.** The job uses its GitHub OIDC token (`id-token: write`) to get a short-lived certificate tied to the workflow identity, so there is no long-lived signing key to leak. The signing event goes to a public transparency log. Check current Sigstore docs for details.
- **SLSA levels.** A graded scale for build integrity. Names and requirements change between versions, so I say "we aim for provenance from a hosted, isolated build" and check the current spec for the level.
- **Verify at deploy.** An admission policy (Kyverno, Sigstore policy-controller, Gatekeeper, at concept level) rejects images that lack a valid signature from the expected workflow identity. Verify by digest, never by tag.
- **For models.** Hash the weights file (SHA-256), store the hash in the registry and in the SBOM as a component (CycloneDX has a machine-learning-model component type; check the spec version), and sign the artifact or the image that bundles it. A changed hash means a changed model.
- **Failure modes.** A signature on a bad image still verifies. The identity regexp in the verify step must be tight (org, repo, workflow, tag), or any workflow in your org passes. Signing a mutable tag signs nothing useful.

**Example:** Pin a lock file of three packages and a 16-byte model file `model-weights-v1`. The SBOM has 4 components. `sha256sum model.bin` and the Python hash agree (6903dfbd...). Change one byte and the hash changes, so the deploy check would fail.

**Code:** Python builds the CycloneDX-style JSON from a pinned requirements file (the `pip freeze` format) and hashes the model; the workflow shows signing, attesting and verifying with cosign.
```python
"""Minimal CycloneDX-style SBOM from pinned requirements + SHA-256 of a model file."""
import hashlib, json, pathlib, sys

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()

def sbom(req_file, model_file):
    comps = []
    for line in pathlib.Path(req_file).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, version = line.split("==")
        comps.append({"type": "library", "name": name, "version": version,
                      "purl": f"pkg:pypi/{name}@{version}"})
    comps.append({"type": "machine-learning-model", "name": pathlib.Path(model_file).name,
                  "hashes": [{"alg": "SHA-256", "content": sha256(model_file)}]})
    return {"bomFormat": "CycloneDX", "specVersion": "1.5", "version": 1, "components": comps}

if __name__ == "__main__":
    doc = sbom(sys.argv[1], sys.argv[2])
    print(json.dumps(doc, indent=2))
    print("component count:", len(doc["components"]))
    before = sha256(sys.argv[2])
    pathlib.Path(sys.argv[2]).write_bytes(b"model-weights-v1 TAMPERED")
    after = sha256(sys.argv[2])
    print("hash changed after tamper:", before != after)
```
```yaml
name: sign-model-image
on:
  push:
    tags: ["model-v*"]
permissions:
  contents: read
jobs:
  sign:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      id-token: write        # keyless signing needs the OIDC token
      attestations: write    # build provenance attestation
    env:
      IMAGE: ghcr.io/example-org/churn-serving
      DIGEST: ${{ vars.IMAGE_DIGEST }}   # in a real job: output of the build job
    steps:
      - uses: sigstore/cosign-installer@v3        # pin to a SHA in real use
      - name: Sign image by digest (keyless)
        run: cosign sign --yes "$IMAGE@$DIGEST"
      - name: Attach SBOM as attestation
        run: cosign attest --yes --type cyclonedx --predicate sbom.json "$IMAGE@$DIGEST"
      - name: Verify as the deploy side would
        run: >
          cosign verify "$IMAGE@$DIGEST"
          --certificate-identity-regexp "^https://github.com/example-org/.+/.github/workflows/.+@refs/tags/model-v.+$"
          --certificate-oidc-issuer https://token.actions.githubusercontent.com
```
```bash
printf 'model-weights-v1' > model.bin
python -I make_sbom.py requirements.lock model.bin
sha256sum model.bin
actionlint sign.yml
check-jsonschema --builtin-schema vendor.github-workflows sign.yml
```

**Output (my run):** the SBOM script, `sha256sum` cross-check, actionlint and the schema check ran. I used a small pinned file, not a live `pip freeze` of an environment, so the output stays hand-checkable. Not executed: cosign, Syft, Trivy (none installed, shown in the last lines), Rekor, SLSA verification, any admission controller, any registry push. The cosign flags are from memory of the docs; check current docs.
```text
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "version": 1,
  "components": [
    {
      "type": "library",
      "name": "numpy",
      "version": "2.5.4",
      "purl": "pkg:pypi/numpy@2.5.4"
    },
    {
      "type": "library",
      "name": "scikit-learn",
      "version": "1.9.1",
      "purl": "pkg:pypi/scikit-learn@1.9.1"
    },
    {
      "type": "library",
      "name": "fastapi",
      "version": "0.115.0",
      "purl": "pkg:pypi/fastapi@0.115.0"
    },
    {
      "type": "machine-learning-model",
      "name": "model.bin",
      "hashes": [
        {
          "alg": "SHA-256",
          "content": "6903dfbdfe04273eedd148c9cfd6053c7960caa17d0166ac75fde62c8ea6292d"
        }
      ]
    }
  ]
}
component count: 4
hash changed after tamper: True
== sha256sum on the untouched file
6903dfbdfe04273eedd148c9cfd6053c7960caa17d0166ac75fde62c8ea6292d  model.bin
== actionlint sign.yml
exit=0
== check-jsonschema
ok -- validation done
cosign: not installed
syft: not installed
trivy: not installed
```

**Follow-ups:**
- *Is CycloneDX output from a requirements file a real SBOM?* It is a minimal one. Production SBOMs come from scanning the image, which also catches OS packages.
- *Why digest and not tag?* A tag can point to a different image tomorrow. A digest is the content.
- *Does signing stop a malicious insider?* Not alone. It narrows who can produce a deployable image; review and branch rules still matter.

**Common mistakes:**
- Saying "we scan, so we sign".
- Verifying that an image is signed but not by whom.
- Signing tags, not digests.
- Generating the SBOM once and never attaching it to the release.

### Q33 ⭐ 🔴 GitOps for model deployment with Argo CD or Flux at concept level. Explain the pull model (a controller in the cluster syncs the cluster to a Git repo) versus a CI job that runs kubectl apply, an Argo CD Application manifest (repoURL, path, destination, syncPolicy), automated sync, prune and self-heal, Flux's controllers and Kustomization, a separate config repo, a CI job that opens a PR bumping the image digest or model version in values.yaml, and rollback as git revert. Parse an Application manifest with pyyaml, then in a temp git repository bump a values file by script, show the git diff and revert it as a rollback. Argo CD and Flux were not executed. Part 3 owns Kubernetes and Helm.
**Asked at:** GitOps comparison posts (devtron.ai, codefresh.io, earthly.dev, harness.io, oneuptime.com 2026 Argo CD versus Flux; search snippets only, not opened); vendor and editorial blogs, nothing found on ML-specific GitOps or interview lists; platform and DevOps roles with ML workloads | MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** In GitOps a controller inside the cluster keeps pulling a config repo and makes the cluster match it, so a deploy is a merged PR that bumps an image digest or model version, and a rollback is a `git revert`.

**Then explain:**
- **Pull vs push.** Push: a CI job holds cluster credentials and runs `kubectl apply`. Pull: the controller (Argo CD or Flux) lives in the cluster and reads Git, so CI never holds production cluster credentials, and the repo is the audit log.
- **Argo CD `Application`.** Fields to know: `source.repoURL`, `targetRevision`, `path`, `destination` (cluster and namespace), and `syncPolicy.automated` with `prune` (delete what is no longer in Git) and `selfHeal` (undo manual `kubectl edit` drift). Without `automated`, someone clicks Sync.
- **Flux.** Controllers (source, kustomize, helm, notification) and CRDs: a `GitRepository` source plus a `Kustomization` with `interval`, `path`, `prune`. Lighter, CLI-first, no built-in UI (per the comparison posts I saw; I did not open them, check current docs).
- **Separate config repo.** App code CI builds and pushes the image, then opens a PR to the config repo that edits `values.yaml` (digest, model version). Environments are folders or overlays. Approvals are normal PR reviews.
- **Rollback.** `git revert` the bump commit; the controller syncs the old digest and version. It only works if the old image and old model artifact still exist.
- **Failure modes.** Serving that loads `models:/name@champion` can change without a Git commit, which breaks "Git is the truth". For GitOps, pin a version number in Git. Also: self-heal fighting an autoscaler (ignore replica diffs), prune deleting something you meant to keep, a controller stuck on a bad manifest, and secrets in Git (use sealed or external secrets).

**Example:** values.yaml says digest `aaaa1111`, model 4. CI opens a PR changing it to `bbbb2222`, model 5. Merge, the controller rolls it out. Problem found: revert that one commit, and the file is back to model 4.

**Code:** the Argo CD `Application`, a Flux `Kustomization`, and the CI workflow that edits the config repo are shown as YAML. The Python parses both manifests, then in a temp git repo bumps a values file, prints the diff and reverts the commit.
```yaml
# --- file: application.yaml ---

apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: churn-serving-prod
  namespace: argocd
spec:
  project: ml-serving
  source:
    repoURL: https://github.com/example-org/ml-deploy-config.git
    targetRevision: main
    path: apps/churn-serving/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: churn
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true

# --- file: flux.yaml ---

apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: churn-serving-prod
  namespace: flux-system
spec:
  interval: 5m
  path: ./apps/churn-serving/overlays/prod
  prune: true
  sourceRef:
    kind: GitRepository
    name: ml-deploy-config

# --- file: bump-config.yml ---

name: bump-deploy-config
on:
  workflow_dispatch:
    inputs:
      digest:
        description: image digest, e.g. sha256:...
        required: true
      model_version:
        description: registry model version
        required: true
permissions:
  contents: read
jobs:
  bump:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          repository: example-org/ml-deploy-config
          token: ${{ secrets.CONFIG_REPO_TOKEN }}   # narrow token for the config repo only
      - name: Edit values and open a PR
        env:
          DIGEST: ${{ inputs.digest }}
          MODEL_VERSION: ${{ inputs.model_version }}
          GH_TOKEN: ${{ secrets.CONFIG_REPO_TOKEN }}
        run: |
          python scripts/bump_values.py values.yaml "$DIGEST" "$MODEL_VERSION"
          git switch -c "bump-model-$MODEL_VERSION"
          git commit -am "deploy: churn model $MODEL_VERSION"
          git push origin HEAD
          gh pr create --fill
```
```python
import pathlib, subprocess, sys, tempfile, yaml

def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout

# 1. parse the manifests
app = yaml.safe_load(open(sys.argv[1]))
auto = app["spec"]["syncPolicy"]["automated"]
print("Application:", app["metadata"]["name"], "| path:", app["spec"]["source"]["path"],
      "| prune:", auto["prune"], "| selfHeal:", auto["selfHeal"])
flux = yaml.safe_load(open(sys.argv[2]))
print("Flux Kustomization:", flux["metadata"]["name"], "| interval:", flux["spec"]["interval"])

# 2. the CI "bump PR" step on a temp config repo
def bump(values_path, digest, model_version):
    v = yaml.safe_load(values_path.read_text())
    v["image"]["digest"] = digest
    v["model"]["version"] = model_version
    values_path.write_text(yaml.safe_dump(v, sort_keys=False))

with tempfile.TemporaryDirectory() as d:
    repo = pathlib.Path(d)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "ci@example.com"); git(repo, "config", "user.name", "ci-bot")
    vp = repo / "values.yaml"
    vp.write_text(yaml.safe_dump({"image": {"repository": "ghcr.io/example-org/churn-serving", "digest": "sha256:aaaa1111"},
                                  "model": {"name": "churn", "version": 4}}, sort_keys=False))
    git(repo, "add", "."); git(repo, "commit", "-qm", "initial: model 4")
    bump(vp, "sha256:bbbb2222", 5)
    print("--- git diff after the bump script ---")
    print(git(repo, "diff"))
    git(repo, "commit", "-qam", "deploy: churn model 5")
    git(repo, "revert", "--no-edit", "HEAD")
    print("--- after git revert (the rollback) ---")
    print(vp.read_text())
    print(git(repo, "log", "--oneline"))
```
```bash
python -I gitops_demo.py application.yaml flux.yaml
actionlint bump-config.yml
```

**Output (my run):** manifests parse with PyYAML; the git diff and revert are real (git 2.43). The bump workflow passes actionlint. Argo CD and Flux were not executed (no cluster, no controllers) and I did not validate the manifests against the Argo CD or Flux CRD schemas, only that they parse as YAML. Commit hashes change on every run.
```text
Application: churn-serving-prod | path: apps/churn-serving/overlays/prod | prune: True | selfHeal: True
Flux Kustomization: churn-serving-prod | interval: 5m
--- git diff after the bump script ---
diff --git a/values.yaml b/values.yaml
index 3db1c26..76fa37e 100644
--- a/values.yaml
+++ b/values.yaml
@@ -1,6 +1,6 @@
 image:
   repository: ghcr.io/example-org/churn-serving
-  digest: sha256:aaaa1111
+  digest: sha256:bbbb2222
 model:
   name: churn
-  version: 4
+  version: 5

--- after git revert (the rollback) ---
image:
  repository: ghcr.io/example-org/churn-serving
  digest: sha256:aaaa1111
model:
  name: churn
  version: 4

73bdb75 Revert "deploy: churn model 5"
67c64e6 deploy: churn model 5
ba8a348 initial: model 4

== actionlint bump-config.yml
exit=0
```

**Follow-ups:**
- *Argo CD or Flux?* Argo CD if you want a UI, projects and SSO. Flux if you want a lighter, controller-and-CLI feel. Both work; pick what the platform team already runs.
- *Where does the model file go?* Not in Git. Git holds the version or digest; weights live in the registry or object store.
- *Canary?* Argo Rollouts or Flagger (concept; Part 6 and Part 3 own the mechanics).

**Common mistakes:**
- Keeping app code and cluster config in one repo, so every code commit triggers a deploy.
- Letting the serving layer resolve a mutable alias outside Git.
- `kubectl edit` in production with self-heal off, then wondering why Git and the cluster disagree.
- Rolling back Git but not checking that the old image is still in the registry.

### Q34 ⭐ 🔴 Design multi-environment promotion: dev, staging and production. Explain promoting the same immutable artifact (image digest and model version) through environments instead of rebuilding, per-environment config separate from the artifact, whether to keep one registry with aliases per environment (staging, champion) or a registry per environment with copy-on-promote, what evidence travels with the artifact (gate report, data version), data differences between environments, and drift between environments. Implement a promotion function with a ledger on a local sqlite MLflow registry that moves aliases staging then champion only in order, with pytest, and run it.
**Asked at:** Model registry promotion write-ups (dataexpert.io champion-challenger guide, docs.zenml.io MLflow registry, towardsai MLflow series, an unofficial MLflow registry reference; search snippets only, not opened; the official MLflow docs were not opened and sources disagree on how deprecated stages are); editorial guides, not interview reports; MLOps and ML engineer roles | MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** Build once, then move the same immutable artifact (image digest plus model version) through dev, staging and production in order, change only the per-environment config, and carry the evidence with it.

**Then explain:**
- **Same artifact, different config.** Rebuilding per environment means production runs something nobody tested. Config (endpoints, replicas, secrets, feature-store URL) lives outside the artifact, in per-environment files or overlays.
- **Registry layout, two options.** (1) One registry, aliases per environment (`staging`, `champion`): simple, one lineage, promotion is moving a pointer. (2) A registry per environment with copy-on-promote: stronger isolation and separate access rights (prod registry writable only by the release job), but copies must keep tags, hashes and lineage. MLflow has a copy call for this; check current docs. Regulated teams often choose (2) or (1) plus strict permissions.
- **Order is enforced in code.** `champion` is only reachable from a version that has been through `staging`. Skipping is refused. Re-running the same promotion is a no-op (idempotent), and every move is written to an append-only ledger.
- **Evidence travels.** Gate report URL, data version, git SHA, who approved. Without it, production has an artifact and no reason to trust it.
- **Failure modes.** Staging data is a sample, so staging proves the plumbing, not the quality. Drift between environments (different library version, different feature definition) makes a green staging meaningless. An alias moved by hand, outside the pipeline, breaks the ledger.

**Example:** versions 1 and 2 exist. Promoting 2 straight to `champion` is refused. Promote 1 to `staging`, then to `champion`; promote 2 to `staging` (champion stays 1); then 2 to `champion`. The ledger has four rows, with `previous` showing what each alias held before.

**Code:** `envpromo.py` is the function, then pytest cases, then a demo. (I hit a real bug while writing it: `get_model_version_by_alias(...).version` did not compare equal to my string version, so the "already there" check never fired and a re-run said `moved`. The `str()` in the code is the fix, and the idempotent test catches it.)
```python
# --- file: envpromo.py ---

"""Ordered promotion: a version must hold the staging alias before it can become champion."""
import json, pathlib, time
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException

ORDER = ["staging", "champion"]

class PromotionError(Exception):
    pass

def _ledger(path, **row):
    row["ts"] = round(time.time(), 3)
    with open(path, "a") as f:
        f.write(json.dumps(row) + "\n")

def promote(client, name, version, target, actor, ledger_path):
    version = str(version)
    if target not in ORDER:
        raise PromotionError(f"unknown environment {target!r}")
    try:
        mv = client.get_model_version(name, version)
    except MlflowException:
        raise PromotionError(f"version {version} of {name} does not exist")
    if target == "champion" and mv.tags.get("reached_staging") != "true":
        raise PromotionError(f"v{version} never reached staging; refusing to skip it")
    try:
        current = str(client.get_model_version_by_alias(name, target).version)
    except MlflowException:
        current = None
    if current == version:                      # idempotent re-run
        return "noop"
    client.set_registered_model_alias(name, target, version)
    if target == "staging":
        client.set_model_version_tag(name, version, "reached_staging", "true")
    client.set_model_version_tag(name, version, f"promoted_to_{target}_by", actor)
    _ledger(ledger_path, name=name, version=version, env=target, previous=current, actor=actor)
    return "moved"

# --- file: test_envpromo.py ---

import json, pytest
from mlflow import MlflowClient
from envpromo import promote, PromotionError

@pytest.fixture
def setup(tmp_path):
    uri = f"sqlite:///{tmp_path}/m.db"
    c = MlflowClient(tracking_uri=uri, registry_uri=uri)
    c.create_registered_model("churn")
    for _ in range(2):
        c.create_model_version("churn", source=str(tmp_path))
    return c, str(tmp_path / "ledger.jsonl")

def test_cannot_skip_staging(setup):
    c, led = setup
    with pytest.raises(PromotionError, match="never reached staging"):
        promote(c, "churn", 1, "champion", "ci", led)

def test_in_order_then_idempotent(setup):
    c, led = setup
    assert promote(c, "churn", 1, "staging", "ci", led) == "moved"
    assert promote(c, "churn", 1, "champion", "ci", led) == "moved"
    assert promote(c, "churn", 1, "champion", "ci", led) == "noop"
    rows = [json.loads(l) for l in open(led)]
    assert [(r["env"], r["version"]) for r in rows] == [("staging", "1"), ("champion", "1")]

def test_unknown_version_and_env(setup):
    c, led = setup
    with pytest.raises(PromotionError):
        promote(c, "churn", 9, "staging", "ci", led)
    with pytest.raises(PromotionError):
        promote(c, "churn", 1, "prod", "ci", led)

# --- file: demo.py ---

import os, sys, tempfile
sys.path.insert(0, os.getcwd())
from mlflow import MlflowClient
from envpromo import promote, PromotionError

d = tempfile.mkdtemp()
uri = f"sqlite:///{d}/m.db"; led = f"{d}/ledger.jsonl"
c = MlflowClient(tracking_uri=uri, registry_uri=uri)
c.create_registered_model("churn")
for _ in range(2):
    c.create_model_version("churn", source=d)
def alias(a):
    try: return c.get_model_version_by_alias("churn", a).version
    except Exception: return None
def show(tag): print(f"{tag:<28} staging={alias('staging')} champion={alias('champion')}")
show("start")
try: promote(c, "churn", 2, "champion", "dhyan", led)
except PromotionError as e: print("refused:", e)
print(promote(c, "churn", 1, "staging", "ci", led)); print(promote(c, "churn", 1, "champion", "ci", led)); show("v1 staging then champion")
print(promote(c, "churn", 2, "staging", "ci", led)); show("v2 in staging")
print(promote(c, "churn", 2, "champion", "ci", led)); show("v2 champion")
print(open(led).read().replace(d, "<tmp>"), end="")
```
```bash
export MLFLOW_DISABLE_TELEMETRY=true
python -I -m pytest -q -p no:cacheprovider test_envpromo.py
python -I demo.py
```

**Output (my run):** MLflow 3.17.2, local sqlite registry created in a temp directory, pytest 9.1.1. Timestamps replaced with `<t>`. Not executed: a remote tracking server, authentication, per-environment cloud accounts, a copy between two registries.
```text
== pytest
3 passed, 1 warning in 6.83s
== demo
start                        staging=None champion=None
refused: v2 never reached staging; refusing to skip it
moved
moved
v1 staging then champion     staging=1 champion=1
moved
v2 in staging                staging=2 champion=1
moved
v2 champion                  staging=2 champion=2
{"name": "churn", "version": "1", "env": "staging", "previous": null, "actor": "ci", "ts": <t>}
{"name": "churn", "version": "1", "env": "champion", "previous": null, "actor": "ci", "ts": <t>}
{"name": "churn", "version": "2", "env": "staging", "previous": "1", "actor": "ci", "ts": <t>}
{"name": "churn", "version": "2", "env": "champion", "previous": "1", "actor": "ci", "ts": <t>}
```

**Follow-ups:**
- *One registry or many?* One registry plus aliases is easier; many registries isolate access. Decide on who must be unable to write to production.
- *What about the data differences?* Staging gets a masked or sampled copy, so promote on the artifact's evidence plus a staging smoke test, and monitor in production.
- *Can staging skip for a hotfix?* Only through a documented break-glass path that still writes the ledger.

**Common mistakes:**
- Rebuilding the image in each environment.
- Baking environment config into the image or the model.
- Letting people move aliases by hand in the UI.
- No ledger, so nobody can say what production ran last Tuesday.

### Q35 ⭐ 🔴 Traceability from a GitHub Actions run to a production prediction. Explain recording GITHUB_SHA, GITHUB_RUN_ID, the workflow name, the data version and the image digest as tags on the registered model version, returning model_version in the API response, and answering 'which commit, which data, which run produced the model that scored this loan?' in one query. Write a script that simulates a CI run by setting those environment variables, logs the tags on a local sqlite MLflow registry, then looks the lineage up from a model version, and run it. Part 4 owns lineage mechanics; this is the CI wiring.
**Asked at:** Model registry promotion write-ups (dataexpert.io champion-challenger guide, docs.zenml.io MLflow registry, towardsai MLflow series, an unofficial MLflow registry reference; search snippets only, not opened; the official MLflow docs were not opened and sources disagree on how deprecated stages are); editorial guides, not interview reports; MLOps and ML engineer roles | GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD
**Say this first (1 line):** Stamp the git SHA, run id, workflow name, data version and image digest as tags on the registered model version at registration time, and make the API return `model_version`, so any prediction maps to its commit, data and run with one registry lookup.

**Then explain:**
- **The chain.** prediction log row -> `model_version` -> registry tags -> commit, workflow run URL (`github.com/<repo>/actions/runs/<run id>`), data version, image digest. The weakest link is a prediction store that did not save `model_version`.
- **What GitHub gives you.** The runner sets `GITHUB_SHA`, `GITHUB_RUN_ID`, `GITHUB_WORKFLOW` and `GITHUB_REPOSITORY` as environment variables. The data version and the image digest are not automatic; pass them in as env vars from earlier steps or repository variables.
- **Fail loudly.** If any lineage value is missing, the registration step exits non-zero. A version without lineage is not releasable.
- **MLflow also records source info** on runs it launches (for example a git commit tag when it can find a repo), but I do not rely on it in CI; explicit tags are clearer. Part 4 owns lineage mechanics; this is the wiring.
- **Failure modes.** Tags are mutable, so restrict who can edit them and keep the ledger too. Re-run attempts (`GITHUB_RUN_ATTEMPT`) share a run id, so add the attempt number if re-runs matter. Aliases pointing at the right version do not prove the tags are right.

**Example:** A loan is scored by `credit-risk` version 2. The response had `"model_version": "2"`. One lookup returns commit `ab12cd...`, run `9876543210`, data `data.20261001` and image `sha256:bbbb2222`. That answers the auditor in one query.

**Code:** the script simulates the CI run by setting environment variables, stamps tags on a sqlite registry, resolves lineage from the API response, and shows the refusal when a value is missing. The workflow shows where the values come from.
```python
"""Simulate a CI run stamping lineage on a model version, then answer 'who made the model that scored this loan?'."""
import os, tempfile
from mlflow import MlflowClient

LINEAGE_ENV = {"GITHUB_SHA": "git_sha", "GITHUB_RUN_ID": "gha_run_id", "GITHUB_WORKFLOW": "gha_workflow",
               "GITHUB_REPOSITORY": "gha_repo", "DATA_VERSION": "data_version", "IMAGE_DIGEST": "image_digest"}

def stamp(client, name, version):
    missing = [k for k in LINEAGE_ENV if not os.environ.get(k)]
    if missing:                                    # fail loudly: a version without lineage is not releasable
        raise SystemExit(f"missing lineage env vars: {missing}")
    for env_name, tag in LINEAGE_ENV.items():
        client.set_model_version_tag(name, version, tag, os.environ[env_name])

def lineage(client, name, version):
    return dict(client.get_model_version(name, str(version)).tags)

def predict(client, name, features):               # stand-in for the API: always return model_version
    v = client.get_model_version_by_alias(name, "champion").version
    return {"score": 0.37, "model_name": name, "model_version": str(v)}

d = tempfile.mkdtemp()
uri = f"sqlite:///{d}/m.db"
c = MlflowClient(tracking_uri=uri, registry_uri=uri)
c.create_registered_model("credit-risk")
c.create_model_version("credit-risk", source=d)
c.create_model_version("credit-risk", source=d)

# CI run for version 2 (values a workflow would get from the runner / earlier steps)
os.environ.update({"GITHUB_SHA": "ab12cd34ef56ab12cd34ef56ab12cd34ef56ab12", "GITHUB_RUN_ID": "9876543210",
                   "GITHUB_WORKFLOW": "train-and-register", "GITHUB_REPOSITORY": "example-org/credit-risk",
                   "DATA_VERSION": "data.20261001", "IMAGE_DIGEST": "sha256:bbbb2222"})
stamp(c, "credit-risk", 2)
c.set_registered_model_alias("credit-risk", "champion", 2)

resp = predict(c, "credit-risk", {"income": 5})      # the loan scoring response stored with the decision
print("API response:", resp)
print("lineage of that version:")
for k, v in sorted(lineage(c, resp["model_name"], resp["model_version"]).items()):
    print(f"  {k:<14} {v}")

del os.environ["IMAGE_DIGEST"]
try:
    stamp(c, "credit-risk", 1)
except SystemExit as e:
    print("refused:", e)
```
```yaml
name: train-and-register
on:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      digest: ${{ steps.push.outputs.digest }}
    steps:
      - id: push
        run: echo "digest=sha256:placeholder" >> "$GITHUB_OUTPUT"   # real job: build-push-action output
  register:
    needs: build
    runs-on: ubuntu-latest
    env:
      MLFLOW_TRACKING_URI: ${{ vars.MLFLOW_TRACKING_URI }}
      DATA_VERSION: ${{ vars.DATA_VERSION }}
    steps:
      - uses: actions/checkout@v4
      - name: Train, register, stamp lineage
        env:
          IMAGE_DIGEST: ${{ needs.build.outputs.digest }}
        run: python scripts/register_and_stamp.py   # GITHUB_SHA, GITHUB_RUN_ID, GITHUB_WORKFLOW come from the runner
```
```bash
export MLFLOW_DISABLE_TELEMETRY=true
python -I trace_demo.py
actionlint trace.yml
```

**Output (my run):** real MLflow 3.17.2 on sqlite in a temp directory. The environment variables are set by my script, not by a GitHub runner, so nothing here proves what a real runner provides beyond the documented variable names. (actionlint also caught my first draft: it used `needs.build` without a `build` job.) Not executed: a real workflow run, a real build, a remote server.
```text
API response: {'score': 0.37, 'model_name': 'credit-risk', 'model_version': '2'}
lineage of that version:
  data_version   data.20261001
  gha_repo       example-org/credit-risk
  gha_run_id     9876543210
  gha_workflow   train-and-register
  git_sha        ab12cd34ef56ab12cd34ef56ab12cd34ef56ab12
  image_digest   sha256:bbbb2222
refused: missing lineage env vars: ['IMAGE_DIGEST']
== actionlint trace.yml
exit=0
```

**Follow-ups:**
- *Where is the prediction-to-version link stored?* In the prediction log or response, next to the request id.
- *Can the tag say "approved by"?* Yes, that belongs to the approval-tags answer in this part; keep it in the same tag set.
- *What if the model is retrained with the same code?* Same SHA, different data version and run id, which is why you need all of them.

**Common mistakes:**
- Tagging the registry with only the git SHA, so data changes are invisible.
- Not logging `model_version` with the prediction.
- Relying on the alias name instead of the numeric version in logs (the alias moves).
- Letting registration succeed when lineage is incomplete.

### Q36 ⭐ 🔴 Flaky tests and non-determinism in ML CI. Explain sources (unseeded random state, thread or GPU non-determinism, floating-point order, time and network dependencies, test order), fixing with seeds and tolerances (pytest.approx, assertions on ranges and properties rather than exact values), statistical tests for stochastic behaviour, quarantining versus retrying, and measuring flakiness by repeated runs. Write one flaky test and its fixed version, run each 50 times in a loop and report the failure counts, and show a pytest marker for quarantine.
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** A flaky ML test is almost always unseeded randomness or an exact-value assertion on a stochastic result, so I seed everything I can, assert ranges and properties with tolerances, test averages for truly random behaviour, and quarantine the rest while I fix it.

**Then explain:**
- **Sources.** Unseeded `random_state`, numpy or torch seeds, thread or GPU non-determinism (atomics, parallel reductions), floating-point summation order, tests that depend on the clock, the network, a shared file or test order, and tiny datasets where one sample moves the metric.
- **Fixes.** Seed at the entry point; use `pytest.approx` or `abs=` tolerances; assert properties ("loss falls", "output shape", "probabilities sum to 1", "score is between 0 and 1") instead of magic numbers; for randomness that is the point, average over N seeds and assert on the mean.
- **Quarantine, do not just retry.** A `quarantine` marker keeps the test out of the PR gate (`-m "not quarantine"`) but still runs it nightly, with an issue and an owner. Blind auto-retry hides real intermittent bugs.
- **Measure.** Run the test many times and count failures. A rate, not a feeling.
- **Failure modes.** A seed can hide a real bug that only shows on other data. Tolerances set so wide that nothing can fail are not tests. A quarantine list that only grows is a graveyard.

**Example:** The flaky test trains a logistic regression on freshly generated random data and asserts accuracy of at least 0.85. About a quarter of the time the random data is just harder and it fails. The fixed tests seed the data and assert a band, or average 20 seeds.

**Code:** `test_flaky.py` has the bad test, two fixed versions and a quarantined test; `conftest.py` registers the marker; `repeat.sh` runs one test N times in fresh processes and counts failures.
```python
# --- file: conftest.py ---

def pytest_configure(config):
    config.addinivalue_line("markers", "quarantine: known-flaky test, excluded from the PR gate (run nightly)")

# --- file: test_flaky.py ---

import numpy as np, pytest
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def _accuracy(seed_data, seed_split):
    X, y = make_classification(n_samples=300, n_features=5, n_informative=3, class_sep=1.5,
                               random_state=seed_data)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=seed_split)
    return LogisticRegression().fit(Xtr, ytr).score(Xte, yte)

def test_flaky_exact_threshold():
    # BAD: nothing is seeded (None = fresh randomness each run) and the threshold is tight
    assert _accuracy(None, None) >= 0.85

def test_fixed_seeded_and_range():
    # GOOD 1: seeded, so the result is the same every run; assert a band, not a magic number
    acc = _accuracy(0, 0)
    assert 0.7 <= acc <= 1.0

def test_fixed_statistical():
    # GOOD 2: if randomness is the point, test the average over many seeds against a loose bound
    accs = [_accuracy(s, s) for s in range(20)]
    assert np.mean(accs) == pytest.approx(0.85, abs=0.1)

@pytest.mark.quarantine
def test_quarantined_example():
    assert _accuracy(None, None) >= 0.95   # known flaky, tracked in an issue, runs nightly only
```
```bash
python -I -m pytest -q -p no:cacheprovider test_flaky.py -m "not quarantine"   # the PR gate
python -I -m pytest -q -p no:cacheprovider test_flaky.py -m quarantine         # the nightly job
./repeat.sh test_flaky_exact_threshold 50
./repeat.sh test_fixed_seeded_and_range 50
./repeat.sh test_fixed_statistical 50
```

**Output (my run):** pytest 9.1.1, scikit-learn 1.9.1, each count is 50 fresh `pytest` processes. The 13 of 50 for the flaky test is one sample and will differ on yours (that is the point). The quarantined test failed in my one nightly-style run, which is why it is out of the PR gate. The loop took about five minutes, so I ran it once from a working copy with the same files, not inside `run_all.sh`.
```text
== PR gate: pytest -m "not quarantine"
3 passed, 1 deselected in 1.40s
== nightly: pytest -m quarantine (this run happened to fail; it is the known-flaky test)
FAILED test_flaky.py::test_quarantined_example - assert 0.9333333333333333 >=...
1 failed, 3 deselected in 1.17s
== repeat.sh, 50 fresh pytest processes each (took about 5 minutes)
test_flaky_exact_threshold: 13 failures in 50 runs
test_fixed_seeded_and_range: 0 failures in 50 runs
test_fixed_statistical: 0 failures in 50 runs
```

**Follow-ups:**
- *Why not just set `pytest-rerunfailures` to 3?* It makes the red go away, not the cause. Use it as a short-term bridge with a ticket.
- *GPU non-determinism?* Seed, enable deterministic algorithms where the framework supports it (check current docs), and compare with tolerances.
- *How do you decide a test is flaky and not a real regression?* It fails and passes on the same commit.

**Common mistakes:**
- `assert acc == 0.9137`.
- Seeding the split but not the model, or the reverse.
- Raising the tolerance until the test cannot fail.
- Quarantining with no owner and no deadline.

### Q37 ⭐ 🔴 CI for a monorepo with many models. Explain change detection with paths filters or a changed-files step, building a dynamic matrix from a job output with fromJSON so only changed models are tested, shared library changes that must test every model, and per-model versioning and tags (churn-v1.2.0). Write a script that maps changed file paths to a matrix JSON, show the workflow that consumes it, validate it with actionlint, and run the script on three sample change lists.
**Asked at:** GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** One planning job turns the list of changed files into a matrix of affected models, the test job fans out over it with `fromJSON`, a change in shared code selects every model, and a single always-running summary job is the required check.

**Then explain:**
- **Change detection.** Either workflow `paths:` filters (cheap, but one workflow per model) or a step that runs `git diff --name-only origin/<base>...HEAD` and a script that maps paths to models. The script is testable; YAML filters are not.
- **Dynamic matrix.** The plan job writes `matrix=<json>` to `$GITHUB_OUTPUT`; the test job uses `strategy: matrix: ${{ fromJSON(needs.plan.outputs.matrix) }}`.
- **Shared code.** A change in `libs/`, `ci/`, `pyproject.toml` or a lock file triggers all models. If model B imports model A, the dependency map must say so.
- **Empty change.** A docs-only PR gives an empty `include`, and GitHub rejects an empty matrix (check current docs), so the plan job also outputs `any=true/false` and the test job is skipped when false. Then the required check must still go green: use an `all-green` job with `if: always()`.
- **Per-model versioning.** Tags like `churn-v1.2.0`; a release workflow on `tags: ["churn-v*"]` builds only that model. Needs `fetch-depth: 0` so the diff has history.
- **Failure modes.** Shallow clone makes `git diff` fail; renames show as delete plus add; matrix job names change per PR, so branch protection cannot require them directly (hence the summary job).

**Example:** Three changed-file lists in the run below. `models/churn/*` selects churn only. Mixed `fraud`, `ltv` and `docs/` selects those two. `libs/common/metrics.py` selects all three. `docs/index.md` alone selects none.

**Code:** mapper script (stdin to JSON) and the workflow that consumes it.
```python
"""Map changed file paths to a GitHub Actions matrix JSON for a monorepo of models."""
import json, sys

SHARED_PREFIXES = ("libs/", "ci/", "pyproject.toml", "requirements")   # a change here tests every model
ALL_MODELS = ["churn", "fraud", "ltv"]

def matrix(changed):
    hit = set()
    for p in changed:
        if p.startswith(SHARED_PREFIXES):
            return {"include": [{"model": m, "reason": "shared"} for m in ALL_MODELS]}
        parts = p.split("/")
        if parts[0] == "models" and len(parts) > 2 and parts[1] in ALL_MODELS:
            hit.add(parts[1])
    return {"include": [{"model": m, "reason": "changed"} for m in sorted(hit)]}

if __name__ == "__main__":
    changed = [l.strip() for l in sys.stdin if l.strip()]
    print(json.dumps(matrix(changed), separators=(",", ":")))
```
```yaml
name: monorepo-ci
on:
  pull_request:
permissions:
  contents: read
jobs:
  plan:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.m.outputs.matrix }}
      any: ${{ steps.m.outputs.any }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - id: m
        run: |
          git diff --name-only "origin/${{ github.base_ref }}...HEAD" > changed.txt
          MATRIX=$(python ci/changed_models.py < changed.txt)
          echo "matrix=$MATRIX" >> "$GITHUB_OUTPUT"
          echo "any=$(python -c 'import json,sys;print(str(bool(json.loads(sys.argv[1])["include"])).lower())' "$MATRIX")" >> "$GITHUB_OUTPUT"
  test:
    needs: plan
    if: needs.plan.outputs.any == 'true'
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix: ${{ fromJSON(needs.plan.outputs.matrix) }}
    steps:
      - uses: actions/checkout@v4
      - run: pytest models/${{ matrix.model }} -q
  all-green:                      # one stable required check for branch protection
    needs: [plan, test]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - run: test "${{ needs.test.result }}" != "failure" && test "${{ needs.test.result }}" != "cancelled"
```
```bash
printf 'libs/common/metrics.py\nmodels/ltv/config.yaml\n' | python -I changed_models.py
actionlint monorepo.yml
check-jsonschema --builtin-schema vendor.github-workflows monorepo.yml
```

**Output (my run):** the mapper ran on four change lists with Python 3.13; actionlint and the schema check ran. Not executed: the workflow on GitHub (so `fromJSON`, the empty-matrix behaviour and the `all-green` logic are from docs and memory, not observed).
```text
--- changed files:
    models/churn/train.py
    models/churn/README.md
{"include":[{"model":"churn","reason":"changed"}]}
--- changed files:
    models/fraud/features.py
    models/ltv/config.yaml
    docs/index.md
{"include":[{"model":"fraud","reason":"changed"},{"model":"ltv","reason":"changed"}]}
--- changed files:
    libs/common/metrics.py
    models/ltv/config.yaml
{"include":[{"model":"churn","reason":"shared"},{"model":"fraud","reason":"shared"},{"model":"ltv","reason":"shared"}]}
--- changed files:
    docs/index.md
{"include":[]}
== actionlint monorepo.yml
exit=0
ok -- validation done
```

**Follow-ups:**
- *Why not one workflow per model?* Fine for 3 models; at 30 it is a maintenance burden and a branch-protection mess.
- *Test everything nightly?* Yes, a nightly full run catches missed dependencies in your map.
- *Tools?* Bazel, Nx or Pants do dependency-aware selection; I would mention them, not assume them.

**Common mistakes:**
- Forgetting shared code and shipping a broken model that was "not changed".
- Requiring matrix job names in branch protection.
- `fetch-depth: 1` with a diff-based planner.
- An empty matrix that fails the workflow on docs-only PRs.

### Q38 ⭐ 🔴 Design question: the CI/CD/CT system for a credit-risk model team in a regulated Indian bank or GCC, 30 data scientists, weekly retrains, audit requirements. Cover repositories, PR checks, data tests, scheduled training, registry and aliases, promotion gates with fairness and stability checks, environments with approvals, OIDC to the cloud, GitOps deploy, shadow then canary, rollback, audit trail, secrets, runner strategy and cost. Give a one-page whiteboard answer and a YAML skeleton of the main workflow, validate the YAML with actionlint, and state which parts are concept only. Part 12 owns system design in depth; check current RBI and other regulator guidance rather than quoting rules from memory.
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD
**Say this first (1 line):** PRs run cheap checks on hosted runners, a Friday schedule retrains inside the bank's network, the model must pass a written gate (floor, champion, stability, fairness) before it gets a version alias, humans in the model-risk team approve production, the cloud is reached with OIDC, and the cluster deploys from Git, so every step leaves an audit record.

**Then explain (whiteboard, one page):**

| Area | Decision |
|---|---|
| Repos | One repo per model (code, gate policy YAML, workflows); one config repo for deploy manifests (GitOps); a shared reusable-workflow repo versioned by tag or SHA |
| PR checks | ruff, types, unit tests, data tests on a sample, 2-epoch smoke train, workflow lint, SHA-pinned actions, secret scan; required checks plus CODEOWNERS on gate thresholds and workflows |
| Scheduled training | Weekly cron (UTC) plus manual dispatch with a frozen data snapshot id; training on a runner inside the network, because data cannot leave |
| Registry | One registry, versions immutable, aliases `staging` and `champion`; tags hold git SHA, run id, data snapshot, gate report, approver |
| Gates | Absolute floor, no worse than champion, population-stability (PSI) on score and key features, fairness slices, latency and size budget, signature check; thresholds in Git, changed only by reviewed PR |
| Environments | `staging`, `shadow`, `production` GitHub environments; production needs reviewers from model risk who are not the author; branch restriction to main |
| Cloud access | OIDC with a trust policy pinned to repo and environment; no stored cloud keys |
| Deploy | CI opens a PR to the config repo bumping image digest and model version; Argo CD or Flux syncs (concept) |
| Rollout | Shadow (mirror, compare), canary at a small share, abort rules; labels arrive late so add a slower review after rollout |
| Rollback | Revert the config commit or move the alias back; previous image and artifact retained by policy |
| Audit | Immutable run logs, gate report artifacts, ledger of promotions, approvals from environment history; retention period by policy |
| Secrets | Environment-scoped, short-lived, none for forks; no data in logs |
| Runners | Hosted for PRs (no secrets); ephemeral self-hosted inside the network for training; never self-hosted on public repos |
| Cost | Path filters, smoke on PR and full on schedule, cancel-in-progress on PRs, idle runners scaled to zero |

- **Concept only here:** every cloud, cluster, approval and runner item. What ran is the lint of the skeleton below.
- **Regulation:** RBI and other regulator expectations on model risk, data localisation and audit are not quoted from memory; check current official guidance with the compliance team.
- **Failure modes:** a gate that cannot be edited without review but whose data can (check data tests too); one person holding both author and approver roles; a retrain that silently changes a feature definition.

**Example:** Friday 20:30 UTC the schedule fires. Data tests pass, the model trains, the gate compares it to the champion and checks fairness. It goes to `staging` (alias moves), then shadow and canary checks, then waits for two model-risk reviewers on `production`. After approval the alias moves and a PR to the config repo is opened; the controller deploys the pinned version.

**Code:** the skeleton of the main workflow. Python helper modules named in `run:` lines (`gates`, `promote`, `rollout_check`, `open_gitops_pr`) are placeholders, not written here.
```yaml
# --- file: weekly-retrain.yml ---

name: weekly-retrain-credit-risk
on:
  schedule:
    - cron: "30 20 * * 5"          # UTC; runs from the default branch only
  workflow_dispatch:
    inputs:
      data_version:
        description: frozen data snapshot id
        required: true
concurrency:
  group: credit-risk-release
  cancel-in-progress: false         # never cancel a half-finished promotion
permissions:
  contents: read
jobs:
  data-tests:
    runs-on: [self-hosted, linux, train]     # private runner inside the bank network (concept)
    steps:
      - uses: actions/checkout@v4
      - env:
          SNAPSHOT: ${{ inputs.data_version || vars.LATEST_SNAPSHOT }}
        run: python -m ci.data_tests --snapshot "$SNAPSHOT"
  train:
    needs: data-tests
    runs-on: [self-hosted, linux, train]
    outputs:
      version: ${{ steps.reg.outputs.version }}
    steps:
      - uses: actions/checkout@v4
      - env:
          SNAPSHOT: ${{ inputs.data_version || vars.LATEST_SNAPSHOT }}
        run: python -m train --snapshot "$SNAPSHOT"
      - id: reg
        run: python -m register --name credit-risk >> "$GITHUB_OUTPUT"
  gate:
    needs: train
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Floor, champion regression, stability (PSI), fairness slices
        run: python -m gates --candidate "${{ needs.train.outputs.version }}" --policy policy/gates.yaml
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: gate-report
          path: gate_report.json
  staging:
    needs: [train, gate]
    runs-on: ubuntu-latest
    environment: staging
    permissions:
      contents: read
      id-token: write                # OIDC to the cloud; no stored keys
    steps:
      - run: python -m promote --version "${{ needs.train.outputs.version }}" --alias staging
  shadow-canary:
    needs: [train, staging]
    runs-on: ubuntu-latest
    environment: shadow
    steps:
      - run: python -m rollout_check --version "${{ needs.train.outputs.version }}" --stages shadow,canary5
  production:
    needs: [train, shadow-canary]
    runs-on: ubuntu-latest
    environment: production           # required reviewers: model risk, not the author
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - run: python -m promote --version "${{ needs.train.outputs.version }}" --alias champion --require-approver
      - name: Open the GitOps PR (the cluster controller does the deploy)
        run: python -m open_gitops_pr --version "${{ needs.train.outputs.version }}"

# --- file: actionlint.yaml ---

self-hosted-runner:
  labels:
    - train
```
```bash
actionlint weekly-retrain.yml                              # fails: custom runner label 'train' unknown
actionlint -config-file actionlint.yaml weekly-retrain.yml # passes after declaring the label
check-jsonschema --builtin-schema vendor.github-workflows weekly-retrain.yml
```

**Output (my run):** actionlint 1.7.12 flags the self-hosted label until `actionlint.yaml` declares it (long label list trimmed in the paste); the vendored GitHub schema check passes. PyYAML shows the `on` key loaded as a boolean. Not executed: any job (no runner, no environment, no OIDC, no registry, no cluster).
```text
== actionlint, no config
weekly-retrain.yml:17:35: label "train" is unknown. available labels are "windows-latest", "windows-latest-8-c
   |
17 |     runs-on: [self-hosted, linux, train]     # private runner inside the bank network (concept)
   |                                   ^~~~~~
weekly-retrain.yml:25:35: label "train" is unknown. available labels are "windows-latest", "windows-latest-8-c
   |
25 |     runs-on: [self-hosted, linux, train]
   |                                   ^~~~~~
== actionlint with actionlint.yaml (label train declared)
exit=0
ok -- validation done
jobs: data-tests, train, gate, staging, shadow-canary, production
top-level key types: ['str', 'bool', 'str', 'str', 'str']
```

**Follow-ups:**
- *Why a separate config repo?* Deploy approvals and history stay apart from code churn, and the cluster controller watches only that repo.
- *Why weekly retrain and not drift-triggered?* A schedule is predictable for audit; drift alerts can open a manual dispatch.
- *Where is the human in the loop?* Environment approval on production, plus CODEOWNERS on the gate policy.

**Common mistakes:**
- Describing tools and no gates.
- Auto-deploying a retrain with no human on a credit model.
- Quoting regulator rules from memory.
- Forgetting the audit record (who approved, what evidence, which data).

### Q39 ⭐ 🔴 Scenario round: six CI/CD failures and the order you check them. (1) A scheduled retrain never fired. (2) The OIDC login says it cannot assume the role. (3) A PR from a fork fails because a secret is empty. (4) The required check stays pending after a docs-only change. (5) CI is green but the promoted model is worse in production. (6) Two promotions overlapped and the older model won. For each give the likely causes, the first command or setting to look at, and the fix. Implement the OIDC sub-claim mismatch diagnosis as a small Python function with tests and run it, and run actionlint on a workflow whose job is missing the permissions block that OIDC needs (show what actionlint does and does not catch).
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | GitHub documentation and blog (docs.github.com OIDC in AWS, 'control deployments' on environments and protection rules, github.blog reusable workflows, aws-actions configure-aws-credentials marketplace page; search snippets only, docs.github.com could not be opened because WebFetch failed with getaddrinfo ENOTFOUND); official docs, not interview reports; DevOps, MLOps and ML engineer roles that own CI/CD
**Say this first (1 line):** For each failure I go from the cheapest, most mechanical check to the deepest: did the workflow even start, what does the log or the token actually say, then what does policy do on purpose, and only then the logic.

**Then explain (order of checks):**

| # | Symptom | Check first | Likely causes | Fix |
|---|---|---|---|---|
| 1 | Scheduled retrain never fired | Actions tab: is the workflow listed and enabled? Is the file on the default branch? | Cron is UTC; `schedule` only runs from the default branch; invalid YAML; Actions or the workflow disabled (a schedule can stop on inactive repos, check current docs); delays at busy times | Merge to default branch, re-enable, add `workflow_dispatch` as a manual fallback, alert on "no run in N days" |
| 2 | OIDC: cannot assume role | Workflow `permissions` for `id-token: write`, then the `sub` and `aud` in the token vs the trust policy | Missing `id-token: write`; job uses `environment:` so `sub` has the environment form; wrong repo or renamed repo; `aud` mismatch; wrong role ARN or region | Match the `sub` exactly (function below); fix permissions |
| 3 | Fork PR has an empty secret | Is the PR from a fork? | GitHub does not pass secrets to fork PRs (by design) | Run secret-free checks on forks; maintainers re-run trusted checks on a branch in the main repo; avoid `pull_request_target` with fork code |
| 4 | Required check pending after docs-only change | Does the workflow have a `paths` filter? | A path-filtered workflow never ran, so the required check never reports | Always-running summary job (see the branch-protection answer in this part) or no path filter on the required workflow |
| 5 | CI green, prod model worse | Gate report: which data, which slices; then training-serving skew | Gate set stale or leaked; offline metric is not the business metric; feature skew; no slice check; label delay | Fix the gate, compare shadow output, add monitoring (Part 8), roll back first |
| 6 | Overlapping promotions, older model won | Run timestamps and the promotion ledger | No `concurrency` group; promote step is not compare-and-set | `concurrency` with `cancel-in-progress: false`; refuse to move the alias to an older version |

- **Order inside a scenario:** reproduce or read first, change nothing; then the configuration that is cheapest to verify; then the code.
- **What actionlint does and does not catch:** it checks syntax, event names, `needs`, expression types and some injection patterns. It does **not** know that the OIDC login action needs `id-token: write`, so a deploy job with no `permissions` passes both actionlint and the schema (shown below). That mistake appears only at run time as the "cannot assume role" error.
- **Failure modes:** fixing the cloud trust to `*` to make it pass (an open door); retrying a schedule fix without a manual dispatch to prove it; blaming CI for a gate that was never testing the right thing.

**Example:** `repo:acme/churn:ref:refs/heads/main` against a trust that pins `repo:acme/churn:environment:production` is exactly the case where a job without `environment:` is rejected. The function below prints that reason in one line.

**Code:** `diagnose` compares `iss`, `aud` and `sub` to the trust and explains the likely shape of the mismatch; pytest covers match, ref token, environment form, pull-request token, wrong repo plus wrong audience; two workflows differ only in `permissions`.
```python
# --- file: oidc_diag.py ---

"""Explain why a cloud trust policy rejected a GitHub OIDC token, using sub/aud/iss only."""
from fnmatch import fnmatchcase

def sub_shape(sub):
    parts = sub.split(":")
    return parts[2] if len(parts) > 2 else "unknown"    # ref | environment | pull_request

def diagnose(claims, trust):
    """claims: decoded token claims. trust: {'sub': [patterns], 'aud': str, 'iss': str}. Returns list of findings."""
    findings = []
    if claims.get("iss") != trust["iss"]:
        findings.append(f"iss mismatch: token {claims.get('iss')!r} vs trust {trust['iss']!r}")
    if claims.get("aud") != trust["aud"]:
        findings.append(f"aud mismatch: token {claims.get('aud')!r} vs trust {trust['aud']!r} (check the audience input of the login action)")
    sub = claims["sub"]
    if not any(fnmatchcase(sub, p) for p in trust["sub"]):
        shape = sub_shape(sub)
        want_repo = trust["sub"][0].split(":")[1]
        got_repo = sub.split(":")[1]
        if got_repo != want_repo:
            findings.append(f"sub repo {got_repo!r} is not {want_repo!r} (renamed, moved or forked repo?)")
        elif shape == "environment":
            findings.append(f"sub {sub!r} uses the environment form; a job with `environment:` no longer sends ref:..., "
                            f"so a trust pinned to a branch will not match")
        elif shape == "pull_request":
            findings.append(f"sub {sub!r} is a pull_request token; trust only allows {trust['sub']} (usually correct: PRs should not assume deploy roles)")
        elif shape == "ref":
            findings.append(f"sub {sub!r} is a ref token for another branch or tag than the trust allows {trust['sub']}")
        else:
            findings.append(f"sub {sub!r} matches none of {trust['sub']}")
    return findings

# --- file: test_oidc_diag.py ---

from oidc_diag import diagnose

ISS = "https://token.actions.githubusercontent.com"
TRUST = {"sub": ["repo:acme/churn:environment:production"], "aud": "sts.amazonaws.com", "iss": ISS}

def claims(sub, aud="sts.amazonaws.com", iss=ISS):
    return {"sub": sub, "aud": aud, "iss": iss}

def test_match_gives_no_findings():
    assert diagnose(claims("repo:acme/churn:environment:production"), TRUST) == []

def test_branch_job_without_environment():
    f = diagnose(claims("repo:acme/churn:ref:refs/heads/main"), TRUST)
    assert len(f) == 1 and "ref token" in f[0]

def test_environment_mismatch_when_trust_pins_branch():
    trust = {**TRUST, "sub": ["repo:acme/churn:ref:refs/heads/main"]}
    f = diagnose(claims("repo:acme/churn:environment:production"), trust)
    assert "environment form" in f[0]

def test_pull_request_token():
    f = diagnose(claims("repo:acme/churn:pull_request"), TRUST)
    assert "pull_request token" in f[0]

def test_other_repo_and_wrong_audience():
    f = diagnose(claims("repo:acme/other:environment:production", aud="sts.example.com"), TRUST)
    assert any("aud mismatch" in x for x in f) and any("sub repo" in x for x in f)
```
```yaml
# --- file: no-permissions.yml ---

name: deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/gha-deploy
          aws-region: ap-south-1
      - run: aws sts get-caller-identity

# --- file: with-permissions.yml ---

name: deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/gha-deploy
          aws-region: ap-south-1
      - run: aws sts get-caller-identity
```
```bash
python -I -m pytest -q -p no:cacheprovider test_oidc_diag.py
actionlint no-permissions.yml; actionlint with-permissions.yml
check-jsonschema --builtin-schema vendor.github-workflows no-permissions.yml
```

**Output (my run):** the tests and both lint tools ran. Both workflows pass both tools, which is the point: the missing `id-token: write` is invisible to them. Not executed: a real OIDC token, a cloud trust policy, schedules, forks, branch protection, any real incident. The fork and schedule rows come from GitHub documentation as I know it; check current docs.
```text
== pytest
5 passed in 0.01s
== no-permissions.yml
actionlint exit=0
ok -- validation done
== with-permissions.yml
actionlint exit=0
ok -- validation done
== two live diagnoses
repo:acme/churn:ref:refs/heads/main
  -> sub 'repo:acme/churn:ref:refs/heads/main' is a ref token for another branch or tag than the trust allows ['repo:acme/churn:environment:production']
repo:acme/churn:pull_request
  -> sub 'repo:acme/churn:pull_request' is a pull_request token; trust only allows ['repo:acme/churn:environment:production'] (usually correct: PRs should not assume deploy roles)
```

**Follow-ups:**
- *OIDC works on main but not on a PR?* The PR token has a `pull_request` sub; that is usually correct, PRs should not assume deploy roles.
- *How do you see the real `sub`?* Decode the JWT in a debug step, or read the cloud's error and the token claims it echoes (never print the raw token in shared logs).
- *Scenario 5 first action?* Roll back, then investigate.

**Common mistakes:**
- Widening the trust policy to make it work.
- Debugging code before checking whether the workflow ran.
- Treating a green CI as proof of model quality.
- Believing actionlint verifies cloud permissions.

### Q40 ⭐ 🔴 CI/CD for an LLM application, kept to the CI side (Book 2 owns LLM internals and RAG). Explain versioning prompts and configs in Git, a golden evaluation set run on every PR, deterministic checks (format, schema, banned content) versus LLM-as-judge scores (noisy, cost per run, needs repeated runs and a tolerance), threshold gates on a sampled subset, caching of model calls, and secrets for API keys. Implement the evaluation gate with a stub model function (no real API call, so say the real provider call is not executed), a tolerance for noise, and pytest cases, and run it.
**Asked at:** MLOps interview question banks and guides (goodspace.ai MLOps interview questions, wecreateproblems.com MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, towardsai '101 ML LLM agentic AIOps interview questions', dev.to 'top MLOps interview questions'; search snippets only, not opened); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Expert extension: no source found for the exact question; the topic follows from the GitHub and MLflow behaviour tested in this sandbox and from general CI/CD practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Keep prompts and configs in Git, run a golden evaluation set on every PR, split the checks into cheap deterministic ones (format, schema, banned content) that must pass and noisy LLM-judge scores that are repeated, averaged and compared with a tolerance, and keep the API key out of fork PRs.

**Then explain:**
- **Version everything that changes behaviour.** Prompt templates, model name and parameters, retrieval settings, tool schemas and the golden set are files in Git. A prompt edit is a code change, reviewed like one.
- **Golden set.** A small, curated set of inputs with expectations (must contain, JSON keys, forbidden phrases, or a reference answer). Version it; changes to it are reviewed, otherwise people edit the test until it passes.
- **Deterministic checks first.** Valid JSON, required keys, length, banned content, refusal on unsafe inputs. Free, fast, no key, and they run on forks.
- **LLM-as-judge is noisy and costs money.** Scores vary between runs, so run each case several times, average, and fail only when the mean drops more than a tolerance from a baseline or under a floor. Use a sample of the golden set on PRs and the full set nightly. In my run the per-repeat means ranged over 0.73 across five repeats, more than the 0.3 tolerance, which is why single runs are not gated.
- **Cache model calls** by hash of (model, parameters, prompt, input) so unchanged cases cost nothing on re-runs. Valid only when the setup is effectively deterministic or you accept recorded outputs; refresh the cache on model changes.
- **Secrets.** The API key is a repository or environment secret; fork PRs do not get it, so the judged job is skipped for forks and a maintainer re-runs it. Never print prompts with personal data into logs.
- **Failure modes.** The judge model changes silently under you (pin its version, check current provider docs). Judge and generator are the same model (bias). The golden set leaks into the prompt. A tolerance so loose that regressions pass.

**Example:** four golden cases, five repeats. The stub model answers one case with "Soon." in one repeat (missing "days"). Deterministic pass rate is 0.95, above the 0.90 floor; the judge mean 4.42 is above the 4.0 floor and within 0.3 of the 4.4 baseline: PASS. A model that always says "I cannot help" gets 0.0 and 2.05: FAIL, exit 1.

**Code:** the gate takes a model function and a judge function, so tests inject fakes. Both here are stubs: **no provider API call is made**, and the real provider call is not executed. The workflow shows the real shape.
```python
# --- file: eval_gate.py ---

"""CI gate for an LLM app. The model call is a STUB: no provider API is called here."""
import json, random, statistics, sys

BANNED = ["ignore previous instructions", "as an ai language model"]

def stub_model(prompt, seed):
    """Deterministic stand-in for the real call. Pretends to be a bit noisy on g3 only."""
    rnd = random.Random(f"{prompt}-{seed}")
    answer = {"Refund for order 118?": "You can request a refund within the window.",
              "Reset my password": "Use the reset link on the login page.",
              "Delivery time to Pune?": "Usually 3 to 5 days." if rnd.random() > 0.2 else "Soon.",
              "Cancel subscription": "You can cancel from Settings."}[prompt]
    return json.dumps({"answer": answer, "source": "faq"})

def stub_judge(prompt, output, seed):
    """Stand-in for LLM-as-judge: score 1-5 with noise. A real judge costs money and varies run to run."""
    base = 4.5 if "days" in output or "refund" in output.lower() or "reset" in output or "cancel" in output else 2.0
    return base + random.Random(f"j-{prompt}-{seed}").uniform(-0.4, 0.4)

def deterministic_checks(case, raw):
    fails = []
    try:
        obj = json.loads(raw)
    except ValueError:
        return ["not valid JSON"]
    for k in case["expect_json_keys"]:
        if k not in obj:
            fails.append(f"missing key {k}")
    text = str(obj.get("answer", "")).lower()
    fails += [f"missing '{w}'" for w in case["must_contain"] if w not in text]
    fails += [f"banned phrase '{b}'" for b in BANNED if b in text]
    return fails

def run_gate(cases, model=stub_model, judge=stub_judge, repeats=5,
             min_det_pass=0.9, min_judge_mean=4.0, tolerance=0.3, baseline_judge=4.4):
    problems, notes = [], []
    det_pass = 0
    judge_runs = []
    for r in range(repeats):                       # repeat: single judge scores are noisy
        scores = []
        for c in cases:
            out = model(c["input"], r)
            f = deterministic_checks(c, out)       # cheap, so run on every repeat
            det_pass += not f
            if f:
                notes.append(f"{c['id']} repeat {r}: " + "; ".join(f))
            scores.append(judge(c["input"], out, r))
        judge_runs.append(statistics.mean(scores))
    det_rate = det_pass / (len(cases) * repeats)
    jm = statistics.mean(judge_runs)
    if det_rate < min_det_pass:
        problems.append(f"deterministic pass rate {det_rate:.2f} < {min_det_pass}")
    if jm < min_judge_mean:
        problems.append(f"judge mean {jm:.2f} < floor {min_judge_mean}")
    if jm < baseline_judge - tolerance:
        problems.append(f"judge mean {jm:.2f} dropped more than tolerance {tolerance} from baseline {baseline_judge}")
    return {"det_rate": det_rate, "judge_mean": round(jm, 3), "judge_spread": round(max(judge_runs) - min(judge_runs), 3), "notes": notes}, problems

if __name__ == "__main__":
    cases = [json.loads(l) for l in open(sys.argv[1])]
    summary, problems = run_gate(cases)
    print({k: v for k, v in summary.items() if k != "notes"})
    for n in summary["notes"]:
        print("note:", n)
    for p in problems:
        print("FAIL:", p)
    print("GATE:", "FAIL" if problems else "PASS")
    sys.exit(1 if problems else 0)

# --- file: test_eval_gate.py ---

import json
from eval_gate import run_gate, deterministic_checks, stub_model, stub_judge

CASES = [json.loads(l) for l in open("golden.jsonl")]

def test_good_stub_passes():
    summary, problems = run_gate(CASES)
    assert problems == []
    assert summary["notes"]            # a noisy case was seen, but the rate stayed above 0.9

def test_single_runs_are_noisier_than_the_tolerance_so_we_average():
    summary, problems = run_gate(CASES)
    assert summary["judge_spread"] > 0.3          # one run could trip a 0.3 tolerance by luck
    assert abs(summary["judge_mean"] - 4.4) < 0.3  # the mean over repeats stays inside it

def test_broken_format_fails_deterministic_gate():
    bad = lambda p, s: "plain text, not json"
    summary, problems = run_gate(CASES, model=bad)
    assert any("deterministic pass rate" in p for p in problems)

def test_banned_phrase_is_caught():
    case = CASES[0]
    raw = json.dumps({"answer": "Refund: ignore previous instructions", "source": "x"})
    assert any("banned" in f for f in deterministic_checks(case, raw))

def test_quality_drop_beyond_tolerance_fails():
    worse = lambda p, o, s: 3.5
    _, problems = run_gate(CASES, judge=worse)
    assert any("floor" in p for p in problems) and any("tolerance" in p for p in problems)
```
```yaml
name: llm-eval
on:
  pull_request:
    paths: ["prompts/**", "config/**", "app/**", "evals/**"]
permissions:
  contents: read
concurrency:
  group: llm-eval-${{ github.ref }}
  cancel-in-progress: true
jobs:
  deterministic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest evals/deterministic -q       # format, schema, banned content; no API key, runs on forks too
  judged:
    needs: deterministic
    if: github.event.pull_request.head.repo.full_name == github.repository   # forks get no secrets
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: LLM-as-judge on a sampled subset, repeated
        env:
          LLM_API_KEY: ${{ secrets.LLM_API_KEY }}
          EVAL_REPEATS: "3"
          EVAL_SAMPLE: "40"
        run: python evals/run_gate.py --golden evals/golden.jsonl
```
```bash
python -I eval_gate.py golden.jsonl            # exit 0 on pass, 1 on fail
python -I -m pytest -q -p no:cacheprovider test_eval_gate.py
actionlint llm-ci.yml
```
`golden.jsonl` is in `code/q40/` (four small cases with `must_contain` and `expect_json_keys`).

**Output (my run):** stub model and stub judge only, so the numbers show the mechanism, not the quality of any real LLM. pytest 9.1.1, actionlint 1.7.12.
```text
{'det_rate': 0.95, 'judge_mean': 4.422, 'judge_spread': 0.734}
note: g3 repeat 4: missing 'days'
GATE: PASS
exit=0
5 passed in 0.02s
== a broken model (always 'I cannot help')
{'det_rate': 0.0, 'judge_mean': 2.047, 'judge_spread': 0.147}
FAIL: deterministic pass rate 0.00 < 0.9
FAIL: judge mean 2.05 < floor 4.0
FAIL: judge mean 2.05 dropped more than tolerance 0.3 from baseline 4.4
== actionlint llm-ci.yml
exit=0
```

**Follow-ups:**
- *How many repeats?* Enough that the spread of the mean is well under the tolerance; measure it on your set, do not guess.
- *Why not gate on the judge alone?* It is noisy and gameable. Deterministic checks catch the failures that cost you most.
- *What about prompts changing without code?* Same pipeline: prompt files live in Git, so the PR runs the eval.

**Common mistakes:**
- Gating on one judge run.
- Evaluating on the cases you tuned the prompt on.
- Running the key-holding job on fork PRs.
- Calling a real API in every unit test.

