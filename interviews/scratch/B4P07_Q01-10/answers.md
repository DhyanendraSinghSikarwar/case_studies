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
