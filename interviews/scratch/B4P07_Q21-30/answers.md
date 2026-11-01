# Book 4 Part 7, Q21-Q30 answers (Wave B)

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
