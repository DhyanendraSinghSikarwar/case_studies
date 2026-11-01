# Book 4 Part 7, Q11-Q20 answers (Wave B)

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
