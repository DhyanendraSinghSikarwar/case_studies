# Book 4 Part 1, Q11-Q20 answers (Wave B)

### Q11 ⭐⭐⭐ 🟡 Dependency management in an ML repo. Compare a loose requirements.txt, a pinned requirements file produced by pip-compile or uv, and a full lockfile; say what you pin directly versus transitively, how you handle separate dev, test and GPU dependencies, and why a model pickled with one scikit-learn version can fail or silently misbehave under another. Demonstrate the pickle version warning or a safer export idea, and show the commands to produce a lock.
**Asked at:** Python packaging references (PEP 660, Xebia setuptools and pyproject guide, editables docs; snippets only) plus Bangalore job postings that list Git, CI/CD, Docker and Python (Cognizant, CommBank, JPMorgan Chase; snippets); postings show required skills, not interview questions; MLOps and ML platform roles
**Say this first (1 line):** Loose files say what I want, a compiled pin file says exactly what I got, and a lockfile says it for every platform with hashes; I write only direct dependencies by hand, compile the rest, and never trust a pickle across scikit-learn versions.

**Then explain:**
- Three levels. Loose `requirements.txt` (`pandas>=2`): easy to write, but two installs a month apart give two different environments. Pinned file from `pip-compile` or `uv pip compile`: every package, direct and transitive, at an exact version. Lockfile (`uv.lock`, poetry.lock): the same idea, resolved for all platforms and Python versions at once, usually with hashes.
- What I pin by hand: only direct dependencies, as ranges in `pyproject.toml` or a small `requirements.in` (pin exactly only when a bug forces it). Transitive ones (numpy, scipy, joblib) are the tool's job. I commit the compiled output and update it on purpose, in a PR, with tests.
- Dev, test and GPU: keep them out of the runtime list. Use extras or dependency groups (`dev`, `test`) and a separate compiled file per environment (`requirements.txt` for serving, `requirements-dev.txt` for CI). For GPU, the torch wheel comes from a different index and CUDA version, so I keep a separate GPU requirements file or group and build a separate image. Check current docs for how your tool handles extra indexes.
- Pickle problem: a pickle stores the object's internal attributes, not a stable format. A different scikit-learn version can have renamed or added attributes, so loading may raise, or load fine and give different numbers because a default changed. Newer versions emit `InconsistentVersionWarning`; many people never read it. Pickle also runs code on load, so never load one you do not trust.
- Safer ideas: serve in the same locked image the model was trained in; store a sidecar file with library versions and fail closed on a mismatch; or export to a portable format (ONNX for supported models, or `skops` for scikit-learn, check current docs; not run here); or keep the training code and data version so you can retrain.
- Edge cases: the minor-version jump is the dangerous one (1.6 to 1.9 below); an unpinned `latest` in a Docker build makes the same Dockerfile produce different images; a lockfile made on Linux can miss a Windows-only wheel unless it is multi-platform.

**Example:** `requirements.in` has two lines (scikit-learn pinned, pandas as a range). `uv pip compile` turned them into 11 exact pins. Count them by hand in the output below: pandas pulls numpy, python-dateutil, six, tzdata; scikit-learn pulls numpy, scipy, joblib, threadpoolctl (plus narwhals and cloudpickle in these versions). Then I trained a LogisticRegression under scikit-learn 1.6.1, pickled it, and loaded it under 1.9.1: it loaded, and only a warning told me the versions differ.

**Code:** the commands first, then `pyproject.toml`, then the two Python scripts (the first run in an old venv, the second in the current environment).
```sh
# 1. loose: hand-written, direct dependencies only
cat requirements.in            # scikit-learn==1.9.1 / pandas>=2.0
# 2. pinned file (pick one tool; pip-tools line not run here)
pip-compile requirements.in -o requirements.txt          # pip-tools
uv pip compile requirements.in -o requirements.txt       # ran; uv 0.11.32
uv pip sync requirements.txt                             # install exactly the pinned set
# 3. lockfile from pyproject.toml (ran)
uv lock
uv sync --frozen                                         # CI/Docker: fail if the lock is out of date
# old environment for the pickle demo (ran)
uv venv old && uv pip install --python old/bin/python scikit-learn==1.6.1
old/bin/python -I make_pickle.py && python3 -I load_pickle.py
```
```toml
# pyproject.toml
[project]
name = "demo"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["scikit-learn>=1.5", "pandas>=2.0"]

[dependency-groups]
dev = ["pytest>=8", "ruff"]
```
```python
# ===== make_pickle.py =====
# run under the OLD environment (scikit-learn 1.6.1)
import json, pickle, sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
X, y = make_classification(n_samples=100, random_state=0)
m = LogisticRegression().fit(X, y)
with open("model_old.pkl", "wb") as f:
    pickle.dump(m, f)
with open("model_old.meta.json", "w") as f:        # sidecar: what built this artifact
    json.dump({"sklearn": sklearn.__version__, "python": "3.13"}, f)
print("wrote model_old.pkl with scikit-learn", sklearn.__version__)

# ===== load_pickle.py =====
# run under the NEW environment (system python, scikit-learn 1.9.1)
import json, pickle, warnings, sklearn
from sklearn.exceptions import InconsistentVersionWarning
print("loading with scikit-learn", sklearn.__version__)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always", InconsistentVersionWarning)
    with open("model_old.pkl", "rb") as f:
        m = pickle.load(f)
for x in w:
    print("warning:", x.category.__name__, "|", str(x.message).split(" This")[0])
print("loaded:", type(m).__name__, "| version warnings:", len(w))

# safer: fail closed using the sidecar, instead of trusting a warning
meta = json.load(open("model_old.meta.json"))
if meta["sklearn"] != sklearn.__version__:
    print(f"GUARD: artifact built with {meta['sklearn']}, runtime has {sklearn.__version__} -> refuse to serve, retrain or re-export")
```

**Output (my run):** uv 0.11.32, Python 3.13.17; the `.in` was pinned to scikit-learn 1.9.1, the old venv had 1.6.1. `pip-compile` itself was not run (pip-tools not installed); `uv pip compile` gives the same kind of file. The versions below will differ when you run it later.
```text
$ cat requirements.in
scikit-learn==1.9.1
pandas>=2.0

$ uv pip compile requirements.in -o requirements.txt --no-header   # then:
direct lines in .in: 2, pinned lines in requirements.txt: 11
$ cat requirements.txt (first 12 lines)
cloudpickle==3.1.2
    # via joblib
joblib==1.6.0
    # via scikit-learn
narwhals==2.27.1
    # via scikit-learn
numpy==2.5.4
    # via
    #   pandas
    #   scikit-learn
    #   scipy
pandas==3.1.0
$ uv lock  ->  packages in uv.lock (all platforms, incl. dev group): 29
```
```text
loading with scikit-learn 1.9.1
warning: InconsistentVersionWarning | Trying to unpickle estimator LogisticRegression from version 1.6.1 when using version 1.9.1.
loaded: LogisticRegression | version warnings: 1
GUARD: artifact built with 1.6.1, runtime has 1.9.1 -> refuse to serve, retrain or re-export
```
`uv lock` printed `Resolved 29 packages`; the lockfile covers all platforms and the dev group, so it is bigger than the single-platform pin file.

**Follow-ups:**
- *Why not just `pip freeze`?* It mixes direct and transitive packages with no record of which you asked for, so you cannot tell what is safe to remove or upgrade. Compile from a small input instead.
- *Does the pin protect me from a changed wheel?* Only with hashes (`--require-hashes`, or the lockfile's hashes). Without them a re-uploaded file would go unnoticed. Check current docs for the flag in your tool.
- *Library or application?* An application locks everything. A library declares ranges only, because pinning exactly in a library breaks its users.

**Common mistakes:**
- Committing `pip freeze` output from a dirty laptop environment (extra packages, wrong OS).
- Pinning in `requirements.in` everything by hand, then never updating, so security fixes never arrive.
- One requirements file for training, serving, tests and notebooks; the serving image gets Jupyter.
- Ignoring `InconsistentVersionWarning` in logs, or filtering warnings to silence it.
- Loading a pickle from an untrusted place; it can run arbitrary code.

---

### Q12 ⭐⭐⭐ 🟡 Code quality gates for an ML repository. Set up ruff (lint and format), mypy and pytest in a .pre-commit-config.yaml and the same checks in a CI job, and say what you would enforce hard (failing the build) versus softly. Explain why pre-commit alone is not enough (--no-verify, new contributors) and how you keep checks fast enough that people do not skip them. Show the config and run it against a small bad file.
**Asked at:** Editorial MLOps interview guides (DataCamp MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, wecreateproblems, a DEV Community list; search snippets only, not opened); guides, not verified candidate reports; MLOps and ML engineer rounds at product companies, GCCs and IT-services firms
**Say this first (1 line):** I run ruff, mypy and fast tests in pre-commit for quick feedback, then run the same commands in CI as the real gate, because a local hook can be skipped with `--no-verify`.

**Then explain:**
- Hard gates (fail the build): ruff lint, ruff format check, mypy on the `src` package, fast unit tests, a coverage floor that is modest and never lowered silently. Soft (warn, do not block): stricter mypy on old modules, complexity, docstring rules, slow tests, notebook lint. I tighten a soft check to hard only after the existing violations are fixed.
- Why pre-commit alone is not enough: `git commit --no-verify` skips it, a new contributor may not have run `pre-commit install`, and local tool versions drift. CI runs the same commands from the same pinned dev requirements, and branch protection makes that job required (a hosted setting; check your platform's docs).
- Speed rules so people do not skip: pre-commit only checks changed files; ruff is fast; mypy runs only on `src`; the slow tests are marked and run in CI or on pre-push, not on every commit. If a commit hook takes more than a few seconds, people find the bypass.
- Failure modes: pinned hook versions differ from CI versions (so "passes locally, fails in CI"); `types: [python]` hooks miss notebooks (use `nbstripout` or jupytext, not covered here); auto-fixing hooks edit files and the commit fails once, which confuses newcomers (tell them to re-add and commit again).
- I used `repo: local` hooks because this sandbox cannot clone hook repositories. On a real team I would pin the official hook repos with a `rev`, and let `pre-commit autoupdate` raise PRs (check current docs for the repos and revisions).

**Example:** The bad file `src/train.py` has an unused import and a multi-import line, a mutable default argument `mean=[]`, an unused variable, a function with no type hints and a function that returns a `str` when annotated `int`. By hand: ruff should flag the imports, `B006` (mutable default) and `F841` (unused variable); `ruff format` flags `x/ 2`; mypy flags the missing annotation and the bad return. That is exactly what the run printed. Normal commit blocked (exit 1); with `--no-verify` the same file went into history, and only the CI-style run caught it.

**Code:** `.pre-commit-config.yaml` plus the CI job (both parse as YAML, validated below), tool settings, the bad file and the demo script that runs in a throwaway repo.
```yaml
# ===== .pre-commit-config.yaml =====
# Local hooks use tools already in the env (no network clone). For a real team you can
# pin remote repos instead, e.g. repo: https://github.com/astral-sh/ruff-pre-commit (check current docs for rev).
repos:
  - repo: local
    hooks:
      - id: ruff-lint
        name: ruff lint
        entry: ruff check --output-format=concise
        language: system
        types: [python]
      - id: ruff-format
        name: ruff format --check
        entry: ruff format --check --quiet
        language: system
        types: [python]
      - id: mypy
        name: mypy
        entry: mypy --ignore-missing-imports
        language: system
        types: [python]
        exclude: ^tests/
      - id: pytest-fast
        name: pytest (fast only)
        entry: pytest -q -m "not slow"
        language: system
        pass_filenames: false
        stages: [pre-push]   # heavier check runs on push, not on every commit

# ===== .github-ci.yml =====
# GitHub Actions job (not executed here; check current docs for action versions). File would live at .github/workflows/ci.yml
name: ci
on: [pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12", cache: pip}
      - run: pip install -r requirements-dev.txt
      - run: ruff check . && ruff format --check .
      - run: mypy src
      - run: pytest -q -m "not slow" --cov=src --cov-fail-under=70
```
```toml
# pyproject.toml
[tool.ruff]
line-length = 88
[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]
[tool.mypy]
disallow_untyped_defs = true
[tool.pytest.ini_options]
markers = ["slow: slow tests, skipped in the fast gate"]
```
```python
# src/train.py
import os,sys
import numpy as np

def fit_scale(x, mean=[]):
    mean.append(1)
    unused = 5
    return x/ 2

def load(path: str) -> int:
    return "oops"
```
```sh
# run_demo.sh
#!/bin/sh
# copies this folder to a temp git repo and runs pre-commit there (nothing touches the main repo)
T=$(mktemp -d); cp -r "$(dirname "$0")"/. "$T"/; cd "$T"
git init -q; git config user.email a@b.c; git config user.name demo; git add -A
pre-commit install
echo "== 1. normal commit"; out=$(git commit -q -m "bad file" 2>&1); rc=$?; echo "$out" | grep -E "Failed|Passed|train.py:[0-9]+:[0-9]+: (B006|F841)|error:"; echo "git commit exit code: $rc (blocked)"
echo "== 2. same commit with --no-verify"; git commit -q --no-verify -m "bad file"; echo "git commit exit code: $?  (hooks skipped, bad file is now in history)"
echo "== 3. CI-style run of the same checks"; ruff check -q --output-format=concise . ; echo "ruff exit: $?"
```

**Output (my run):** pre-commit 4.7.0, ruff 0.16.9, mypy 2.3.1, git 2.43.0, in a temp repo. The CI workflow was not executed (needs the hosted platform; the action versions in it should be checked against current docs). I did validate that both YAML files parse with pyyaml: `.pre-commit-config.yaml parses ['repos']`, and the CI file parses with keys `name`, `on` and `jobs` (YAML reads the bare word `on` as `True`, which is a known gotcha; GitHub reads it as `on`).
```text
pre-commit installed at .git/hooks/pre-commit
== 1. normal commit
ruff lint................................................................Failed
src/train.py:4:23: B006 Do not use mutable data structures for argument defaults
src/train.py:6:5: F841 Local variable `unused` is assigned to but never used
ruff format --check......................................................Failed
mypy.....................................................................Failed
src/train.py:4: error: Function is missing a type annotation  [no-untyped-def]
src/train.py:10: error: Incompatible return value type (got "str", expected "int")  [return-value]
git commit exit code: 1 (blocked)
== 2. same commit with --no-verify
git commit exit code: 0  (hooks skipped, bad file is now in history)
== 3. CI-style run of the same checks
src/train.py:1:1: E401 [*] Multiple imports on one line
src/train.py:1:1: I001 [*] Import block is un-sorted or un-formatted
src/train.py:1:8: F401 [*] `os` imported but unused
src/train.py:1:11: F401 [*] `sys` imported but unused
src/train.py:2:17: F401 [*] `numpy` imported but unused
src/train.py:4:23: B006 Do not use mutable data structures for argument defaults
src/train.py:6:5: F841 Local variable `unused` is assigned to but never used
ruff exit: 1
```
The pytest hook is on `pre-push`, so it did not run on commit; the demo repo has a passing test anyway.

**Follow-ups:**
- *Should CI also auto-fix?* No. CI checks and fails; fixing is local (`ruff check --fix`, `ruff format`).
- *Where does the type-check strictness go for a messy legacy repo?* Start with `mypy src/new_package` only, grow the list, and do not turn on `disallow_untyped_defs` globally on day one.
- *How do you stop pre-commit versions drifting from CI?* CI runs `pre-commit run --all-files` itself, or both read the same pinned dev requirements.

**Common mistakes:**
- Treating pre-commit as the only gate.
- Making the hook slow (full test suite on every commit) so everyone uses `--no-verify`.
- Different ruff versions in hooks and CI.
- A gate that nobody can pass on the existing code, so it is switched off for everything.
- Running mypy on tests and notebooks first and drowning in noise.

---

### Q13 ⭐⭐⭐ 🔴 Training-serving skew from the code side. A model scores well offline but badly online because the training notebook computes features with pandas while the service re-implements them. Explain how repository structure prevents this: one shared feature module imported by both paths, a golden-file parity test comparing the two paths on 20 sample rows, and a schema contract. Build the shared module and the parity test with a seeded example in which a deliberate bug (different rounding or a different fill value) is caught by the test.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** Put every feature calculation in one module that both training and the service import, add a golden-file parity test that runs both paths on the same 20 rows, and validate inputs with a schema, so a re-implementation cannot drift without a red test.

**Then explain:**
- Why it happens: notebook pandas code is copied into the API as hand-written Python. Small differences (fill value, rounding, category order, timezone) give different numbers, and the model sees inputs it was never trained on. Offline metrics stay good; online quality drops with no error.
- Repo fix: `features.py` is the only place with feature logic. Training calls `build_features(df)`. The service calls the same function (a thin wrapper, no maths). Constants such as the fill value live there too, or in a config both read.
- Golden-file parity test: save 20 raw rows and the features training produced (`golden_features.csv`). The test pushes the raw rows through the real serving function and compares with a tolerance. Include rows with missing values on purpose, since edge cases are where paths differ.
- Schema contract: a pydantic model (or pandera for frames) at the service boundary rejects wrong types early and documents what the model expects.
- Limits: the parity test only covers the sample rows, so choose them to include nulls, zeros and extremes. If a feature uses a fitted statistic (a median), store it as an artefact with the model, not as a number typed in two places. Features computed in a warehouse or feature store are a different setup; this covers the in-repo case.

**Example:** The seeded golden set has 20 rows, rows 3, 11 and 17 with missing income. Training fills missing income with 50,000. The buggy service fills 0 and rounds `income_per_head` to 1 decimal instead of 2. Hand check: row 3's income column should be 50000.0 and the buggy service gives 0.0. The 3 missing-income rows (3, 11, 17) differ on several columns. Three more rows (6, 13, 14, all household size 3) differ only because of rounding: row 6 is 92000/3 = 30666.67 in training and 30666.7 in the buggy service. The test reports 6 of 20 rows differ and names the first one.

**Code:** run with `python3 -I`. `SERVICE=buggy` points the same test at the re-implementation; `SERVICE=shared` points it at the fixed service.
```python
# ===== features.py =====
"""Single source of truth for features. Training and serving both import this."""
import numpy as np
import pandas as pd
from pydantic import BaseModel

INCOME_FILL = 50_000.0   # constant learned at training time, stored in code/config, not retyped elsewhere
COLUMNS = ["age", "income", "household", "income_per_head", "log_income", "is_senior"]


class RawRow(BaseModel):          # schema contract at the service boundary
    age: int
    income: float | None = None
    household: int


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    out["age"] = df["age"]
    out["income"] = df["income"].fillna(INCOME_FILL)
    out["household"] = df["household"]
    out["income_per_head"] = (out["income"] / out["household"]).round(2)
    out["log_income"] = np.log1p(out["income"]).round(4)
    out["is_senior"] = (out["age"] >= 60).astype(int)
    return out[COLUMNS]

# ===== service_buggy.py =====
"""A re-implementation written by someone else for the API. Looks fine, is not."""
import math
from features import COLUMNS


def predict_features(rows: list[dict]) -> list[list[float]]:
    out = []
    for r in rows:
        income = r["income"] if r["income"] is not None and r["income"] == r["income"] else 0.0  # BUG 1: fills 0
        ph = round(income / r["household"], 1)                                                    # BUG 2: 1 decimal
        out.append([r["age"], income, r["household"], ph, round(math.log1p(income), 4), int(r["age"] >= 60)])
    return out

# ===== service_shared.py =====
"""Service path after the fix: no feature logic here, only a call into the shared module."""
import pandas as pd
from features import RawRow, build_features


def predict_features(rows: list[dict]) -> list[list[float]]:
    rows = [RawRow(**{**r, "income": None if r["income"] != r["income"] else r["income"]}).model_dump() for r in rows]  # schema check
    return build_features(pd.DataFrame(rows)).values.tolist()

# ===== make_golden.py =====
"""Run once at training time: 20 seeded sample rows + the features the training path produced."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np, pandas as pd
from features import build_features

rng = np.random.default_rng(42)
df = pd.DataFrame({
    "age": rng.integers(18, 80, 20),
    "income": rng.integers(20, 200, 20) * 1000.0,
    "household": rng.integers(1, 6, 20),
})
df.loc[[3, 11, 17], "income"] = np.nan          # missing incomes on purpose
df.to_csv("golden_raw.csv", index=False)
build_features(df).to_csv("golden_features.csv", index=False)
print("golden rows:", len(df), "| NaN incomes:", int(df.income.isna().sum()))

# ===== tests/test_parity.py =====
import importlib, os
import numpy as np, pandas as pd, pytest

IMPL = os.environ.get("SERVICE", "shared")


def test_serving_matches_golden_training_features():
    raw = pd.read_csv("golden_raw.csv")
    want = pd.read_csv("golden_features.csv").values
    rows = [{k: (None if v != v else v) for k, v in r.items()} for r in raw.to_dict("records")]
    got = np.array(importlib.import_module(f"service_{IMPL}").predict_features(rows), dtype=float)
    assert got.shape == want.shape
    bad = np.where(~np.isclose(got, want, rtol=0, atol=1e-6))
    assert bad[0].size == 0, f"{len(set(bad[0]))} of {len(want)} rows differ; first: row {bad[0][0]} col {bad[1][0]} got {got[bad[0][0], bad[1][0]]} want {want[bad[0][0], bad[1][0]]}"


def test_schema_contract_rejects_bad_payload():
    from features import RawRow
    with pytest.raises(Exception):
        RawRow(age="old", household=2)
```
```ini
# pytest.ini
[pytest]
pythonpath = .
```
```sh
# run.sh
python3 -I make_golden.py                                   # once, at training time
SERVICE=buggy  python3 -I -m pytest -q -p no:cacheprovider tests   # parity test fails
SERVICE=shared python3 -I -m pytest -q -p no:cacheprovider tests   # passes
```

**Output (my run):** Python 3.13.17, pandas 3.0.5, numpy 2.5.3, pytest 9.1.1, pydantic 2.13.5.
```text
golden rows: 20 | NaN incomes: 3
=== SERVICE=buggy
E       AssertionError: 6 of 20 rows differ; first: row 3 col 1 got 0.0 want 50000.0
E       assert 12 == 0
E        +  where 12 = array([ 3,  3,  3,  6, 11, 11, 11, 13, 14, 17, 17, 17]).size
1 failed, 1 passed in 0.64s
=== SERVICE=shared
..                                                                       [100%]
2 passed in 0.56s
```
The buggy run: 1 failed (parity), 1 passed (schema test). The shared run: both pass.

**Follow-ups:**
- *Why a tolerance and not equality?* Float maths can differ in the last digits across machines. Use `atol=1e-6` for features and say why; exact equality for integers and categories.
- *What if the service must be fast and cannot use pandas?* Then write a pure-Python version and keep the parity test, which is the contract. Better, vectorise the shared function so it handles one row and many rows.
- *How do you catch skew that is not code, such as different data distributions?* That is drift monitoring, not this test.

**Common mistakes:**
- Copy-pasting notebook code into the API "for now".
- Testing the service against hand-written expected values instead of the training path's output.
- Golden rows that are all clean; the bug hides in nulls.
- Typing the fill median in two places.
- Letting a pydantic model coerce silently (`"12"` to 12) when you wanted a rejection; check strict mode.

---

### Q14 ⭐⭐⭐ 🔴 How do you test an ML model itself (not just the code)? Explain pre-train tests (output shape and range, probabilities sum to 1, loss goes down on one batch, the model can overfit a 10-row dataset) and post-train tests (minimum accuracy on a slice, invariance to irrelevant changes, directional expectation, no leakage). Implement five of these as pytest tests for a scikit-learn LogisticRegression on seeded synthetic data and show the passing run and one deliberately failing case.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** I test a model in two groups: pre-train checks that the machinery is sane (shapes, probabilities, can overfit a tiny set), and post-train checks of behaviour (minimum score on a slice, invariance, directional expectation, no leakage), all as ordinary pytest tests on seeded data.

**Then explain:**
- Pre-train tests need no quality bar: output shape, probabilities in [0, 1] and summing to 1, loss goes down on a batch, and the model can memorise 10 rows. If it cannot overfit 10 rows, something in the pipeline is broken.
- Post-train tests check behaviour: a minimum accuracy on an important slice (not only overall), invariance (changing an irrelevant feature should not flip predictions), directional expectation (more of a positively-linked feature should not lower the probability), and no train/test overlap or leaky feature.
- Thresholds: set them from observed spread with a margin, not from one lucky run; otherwise the test is flaky. Record seeds.
- These tests catch pipeline bugs and regressions, not "is the model good enough for the business"; that is evaluation and monitoring.
- Failure modes: a test that passes on a tiny sample for the wrong reason, a threshold too tight, and tests that retrain a big model on every run (use a small fixture trained once per module).

**Example:** Data: 600 rows, x0 pushes class 1 up, x1 pushes it down, a third column is pure noise, split 70/30 stratified, seed 0. Hand expectation: shifting the noise column by 0.5 should flip almost no predictions (limit 2%). Then I inject a bug: the noise column secretly equals the label plus small noise (a leak). The model now leans on it, and shifting it flips 5.6% of predictions, so the invariance test fails and names the number.

**Code:** `test_model.py`, six tests. Set `LEAK=1` to inject the leaky column.
```python
# test_model.py
import os
import numpy as np
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

LEAK = os.environ.get("LEAK") == "1"   # flip to 1 to inject a leaky feature and watch tests fail


def make_data(n=600, seed=0):
    rng = np.random.default_rng(seed)
    x0 = rng.normal(size=n)                      # informative, positive effect
    x1 = rng.normal(size=n)                      # informative, negative effect
    noise = rng.normal(size=n)                   # should be irrelevant
    y = (1.5 * x0 - 1.0 * x1 + rng.normal(scale=0.7, size=n) > 0).astype(int)
    if LEAK:
        noise = y + rng.normal(scale=0.1, size=n)  # the "irrelevant" column secretly encodes the label
    return np.c_[x0, x1, noise], y


@pytest.fixture(scope="module")
def split():
    X, y = make_data()
    idx = np.arange(len(y))
    tr, te = train_test_split(idx, test_size=0.3, random_state=0, stratify=y)
    return X[tr], X[te], y[tr], y[te], tr, te


@pytest.fixture(scope="module")
def model(split):
    Xtr, _, ytr, *_ = split
    return LogisticRegression().fit(Xtr, ytr)


# ---- pre-train style: no quality bar, just "is the machinery sane"
def test_output_shape_range_sum(model, split):
    p = model.predict_proba(split[1])
    assert p.shape == (len(split[1]), 2)
    assert ((p >= 0) & (p <= 1)).all()
    np.testing.assert_allclose(p.sum(axis=1), 1.0, atol=1e-9)


def test_can_overfit_ten_rows():
    X, y = make_data(n=10, seed=1)
    m = LogisticRegression(C=1e6, max_iter=1000).fit(X, y)
    assert (m.predict(X) == y).mean() == 1.0     # if it cannot memorise 10 rows, the pipeline is broken


# ---- post-train behaviour
def test_min_accuracy_on_slice(model, split):
    _, Xte, _, yte, *_ = split
    mask = Xte[:, 0] > 0                         # slice: x0 positive
    acc = (model.predict(Xte[mask]) == yte[mask]).mean()
    assert acc >= 0.80, f"slice accuracy {acc:.3f}"


def test_invariance_to_irrelevant_feature(model, split):
    Xte = split[1]
    shifted = Xte.copy(); shifted[:, 2] += 0.5   # nudge the column that should not matter
    flips = (model.predict(Xte) != model.predict(shifted)).mean()
    assert flips <= 0.02, f"{flips:.1%} predictions flipped"


def test_directional_expectation(model, split):
    Xte = split[1]
    up = Xte.copy(); up[:, 0] += 1.0             # more x0 -> probability of class 1 must not drop
    assert (model.predict_proba(up)[:, 1] >= model.predict_proba(Xte)[:, 1] - 1e-12).all()


def test_no_train_test_overlap(split):
    *_, tr, te = split
    assert set(tr).isdisjoint(te)
```
```sh
# run.sh
python3 -I -m pytest -q -p no:cacheprovider            # all pass
LEAK=1 python3 -I -m pytest -q -p no:cacheprovider     # injected leak: invariance test fails
```

**Output (my run):** Python 3.13.17, scikit-learn 1.9.1, pytest 9.1.1.
```text
$ pytest -q
......                                                                   [100%]
6 passed in 1.65s
$ LEAK=1 pytest -q   # the "irrelevant" column secretly encodes the label
E       AssertionError: 5.6% predictions flipped
E       assert np.float64(0.05555555555555555) <= 0.02
FAILED test_model.py::test_invariance_to_irrelevant_feature - AssertionError:...
1 failed, 5 passed in 1.45s
```

**Follow-ups:**
- *Where does a leakage test come from in real life?* Compare IDs or timestamps across splits, and check that no feature is suspiciously close to the target (very high single-feature score).
- *How do you test fairness or slices?* Same pattern: a parametrized test per slice with a minimum metric, and a clear owner for changing the thresholds.
- *Would you use a metamorphic test for a text model?* Yes: change casing or add a harmless word, expect the same class. Not run here.

**Common mistakes:**
- One accuracy threshold on the whole test set only.
- Thresholds copied from a single run.
- Tests that need the full production data.
- No seed, so the failing case cannot be reproduced.
- Forgetting that these tests do not replace online monitoring.

---

### Q15 ⭐⭐⭐ 🔴 Refactor a messy notebook into production code. The notebook loads data from a hard-coded path, fits a scaler on all rows, trains a model, prints the metric and saves model.pkl, all in global cells. Describe your step-by-step plan (functions, a config object, a train/predict split, tests, a CLI entry point, a pinned environment) and show the refactored layout and key functions, including the bug the refactor exposes (scaler fitted before the split). Run the refactored pipeline on seeded data.
**Asked at:** Editorial MLOps interview guides (DataCamp MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, wecreateproblems, a DEV Community list; search snippets only, not opened); guides, not verified candidate reports; MLOps and ML engineer rounds at product companies, GCCs and IT-services firms
**Say this first (1 line):** I move the notebook into a package in small steps (functions, a config object, a pipeline with the scaler inside it, tests, a CLI, a pinned environment), and doing it shows the bug: the scaler was fitted on all rows before the split.

**Then explain:**
- Plan in order: (1) freeze the current output (metric and a few predictions) so I can tell if the refactor changes behaviour; (2) split cells into functions: `load_data`, `split`, `build_model`, `train`, `predict`; (3) replace hard-coded values with a config object (paths, feature list, seed, test size); (4) put the scaler and model into one `Pipeline` so `fit` only sees training rows; (5) save one artefact (the pipeline plus feature names), not just the model; (6) add a CLI entry point and a few tests; (7) pin the environment with a lockfile.
- The bug the refactor exposes: the notebook did `StandardScaler().fit_transform(X)` on all rows, then split. The test rows influenced the mean and standard deviation. It is mild leakage with a scaler, severe with target encoding or feature selection. It also meant the saved `model.pkl` could not reproduce the inputs at serving time, because the scaler was never saved.
- Also fixed: no seed on the split (different metric every run), metric only printed (now returned as a dict), absolute path on one laptop.
- Edge cases: the metric will change after the fix, and that is correct; say so in the PR. Keep notebooks for exploration, importing the package.

**Example:** Layout after refactor:
```text
churn/
  pyproject.toml          # package, console script "churn", pinned deps via lock
  src/churn/
    config.py             # TrainConfig dataclass: paths, features, seed, test_size
    pipeline.py           # load_data, split, build_model (Pipeline), train, predict
    cli.py                # `churn train --data ... --out ...`
  tests/test_pipeline.py
  notebooks/explore.ipynb # thin, imports churn
```
Hand check of the leak: on 400 rows, the notebook's scaler mean for `tenure` is computed over all 400, the fixed one over the 320 training rows. The two differ (37.415 vs 38.219 in the run below), so the scaled test values changed.

**Code:** the original notebook as a flat script (for reference, not run), then the refactor.
```python
# ===== notebook_before.py =====
# What the notebook looked like, flattened into one script (cells in order). DO NOT ship this.
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle

df = pd.read_csv("C:/Users/me/Downloads/churn_final_v3.csv")     # hard-coded path
X = df[["tenure", "monthly_spend", "support_calls"]]
y = df["churned"]
X = StandardScaler().fit_transform(X)                            # fitted on ALL rows: test statistics leak in
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2)       # no seed
m = LogisticRegression().fit(Xtr, ytr)
print("accuracy", m.score(Xte, yte))                             # metric only printed
pickle.dump(m, open("model.pkl", "wb"))                          # scaler not saved: serving cannot reproduce inputs

# ===== src/churn/config.py =====
from dataclasses import dataclass


@dataclass(frozen=True)
class TrainConfig:
    data_path: str
    out_path: str = "model.joblib"
    features: tuple[str, ...] = ("tenure", "monthly_spend", "support_calls")
    target: str = "churned"
    test_size: float = 0.2
    seed: int = 42

# ===== src/churn/pipeline.py =====
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from churn.config import TrainConfig


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def split(df: pd.DataFrame, cfg: TrainConfig):
    X, y = df[list(cfg.features)], df[cfg.target]
    return train_test_split(X, y, test_size=cfg.test_size, random_state=cfg.seed, stratify=y)


def build_model(seed: int) -> Pipeline:
    # scaler lives INSIDE the pipeline, so fit() only ever sees training rows
    return Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(random_state=seed))])


def train(cfg: TrainConfig) -> dict:
    df = load_data(cfg.data_path)
    Xtr, Xte, ytr, yte = split(df, cfg)
    model = build_model(cfg.seed).fit(Xtr, ytr)
    metrics = {"accuracy": round(float(model.score(Xte, yte)), 4), "n_train": len(Xtr), "n_test": len(Xte)}
    joblib.dump({"model": model, "features": list(cfg.features)}, cfg.out_path)
    return metrics


def predict(model_path: str, rows: pd.DataFrame):
    art = joblib.load(model_path)
    return art["model"].predict(rows[art["features"]])

# ===== src/churn/cli.py =====
import argparse
import json

from churn.config import TrainConfig
from churn.pipeline import predict, train


def main(argv=None) -> None:
    p = argparse.ArgumentParser(prog="churn")
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("train")
    t.add_argument("--data", required=True)
    t.add_argument("--out", default="model.joblib")
    t.add_argument("--seed", type=int, default=42)
    args = p.parse_args(argv)
    if args.cmd == "train":
        print(json.dumps(train(TrainConfig(data_path=args.data, out_path=args.out, seed=args.seed))))


if __name__ == "__main__":
    main()

# ===== make_data.py =====
import sys, numpy as np, pandas as pd
rng = np.random.default_rng(7)
n = 400
df = pd.DataFrame({"tenure": rng.integers(1, 72, n), "monthly_spend": rng.normal(60, 20, n).round(2), "support_calls": rng.poisson(2, n)})
z = -0.04 * df.tenure + 0.02 * df.monthly_spend + 0.4 * df.support_calls - 0.3 + rng.normal(0, 0.8, n)
df["churned"] = (z > 0).astype(int)
df.to_csv(sys.argv[1], index=False)
print("rows", n, "churn rate", round(df.churned.mean(), 3))

# ===== bug_demo.py =====
# shows what the refactor exposes: the notebook's scaler statistics include the test rows
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
df = pd.read_csv("data.csv")
X, y = df[["tenure", "monthly_spend", "support_calls"]], df["churned"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print("mean (all 400 rows, notebook):", X.mean().round(3).tolist())
print("mean (320 train rows, fixed) :", Xtr.mean().round(3).tolist())
print("max abs gap in std units:", float(((X.mean() - Xtr.mean()).abs() / Xtr.std()).max().round(4)))

# ===== tests/test_pipeline.py =====
import numpy as np, pandas as pd
from churn.config import TrainConfig
from churn.pipeline import build_model, split, train, predict


def _df(n=200):
    rng = np.random.default_rng(0)
    df = pd.DataFrame({"tenure": rng.integers(1, 72, n), "monthly_spend": rng.normal(60, 20, n), "support_calls": rng.poisson(2, n)})
    df["churned"] = (df.support_calls + rng.normal(0, 1, n) > 2).astype(int)
    return df


def test_scaler_sees_train_rows_only(tmp_path):
    df = _df(); cfg = TrainConfig(data_path="unused")
    Xtr, Xte, ytr, yte = split(df, cfg)
    m = build_model(cfg.seed).fit(Xtr, ytr)
    np.testing.assert_allclose(m["scale"].mean_, Xtr.mean().values)      # train mean
    assert not np.allclose(m["scale"].mean_, df[list(cfg.features)].mean().values)  # NOT the all-rows mean


def test_train_is_deterministic_and_roundtrips(tmp_path):
    p = tmp_path / "d.csv"; _df().to_csv(p, index=False)
    a = train(TrainConfig(data_path=str(p), out_path=str(tmp_path / "a.joblib")))
    b = train(TrainConfig(data_path=str(p), out_path=str(tmp_path / "b.joblib")))
    assert a == b
    assert len(predict(str(tmp_path / "a.joblib"), _df().head(5))) == 5
```
```toml
# pyproject.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "churn"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["pandas>=2", "scikit-learn>=1.5", "joblib"]

[project.optional-dependencies]
dev = ["pytest"]

[project.scripts]
churn = "churn.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/churn"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```
```sh
# run_demo.sh
#!/bin/sh
# builds a throwaway venv in a temp dir, installs the package, runs tests and the CLI
set -e
SRC=$(cd "$(dirname "$0")" && pwd); T=$(mktemp -d); cd "$T"
cp -r "$SRC"/src "$SRC"/tests "$SRC"/pyproject.toml "$SRC"/make_data.py .
uv venv -q venv; uv pip install -q --python venv/bin/python -e ".[dev]"
venv/bin/python -I make_data.py data.csv
venv/bin/churn train --data data.csv --out model.joblib
venv/bin/churn train --data data.csv --out model2.joblib
venv/bin/python -I -m pytest -q -p no:cacheprovider
cp "$SRC"/bug_demo.py .; venv/bin/python -I bug_demo.py
```

**Output (my run):** Python 3.13.17, scikit-learn 1.9.1, pandas 3.0.5, pytest 9.1.1, uv 0.11.32; a throwaway venv with an editable install. Data is synthetic and seeded (`default_rng(7)`). `notebook_before.py` was not run (it points to a path that does not exist, which is the point). The numbers below were produced by the run.
```text
rows 400 churn rate 0.538
{"accuracy": 0.8375, "n_train": 320, "n_test": 80}
{"accuracy": 0.8375, "n_train": 320, "n_test": 80}
..                                                                       [100%]
2 passed in 1.06s
mean (all 400 rows, notebook): [37.415, 57.454, 1.988]
mean (320 train rows, fixed) : [38.219, 57.492, 2.059]
max abs gap in std units: 0.054
```
The CLI ran twice with the same data and seed and printed the identical metric, and the two pytest tests pass: one checks that the scaler's mean equals the training-rows mean and not the all-rows mean, one checks determinism and a save/load round trip.

**Follow-ups:**
- *Why a Pipeline instead of scaling first and splitting?* A pipeline refits the scaler inside each fit and cross-validation fold automatically, which removes the leak by construction.
- *How do you check you did not break anything?* Compare the metric and predictions on a fixed sample before and after; expect a small honest change from the leak fix only.
- *Where do the pinned deps go?* `pyproject.toml` ranges plus a lockfile, as in a dependency answer.

**Common mistakes:**
- Rewriting everything at once with no behaviour baseline.
- Moving globals into a class but keeping the fit-on-all-rows bug.
- Saving only the model, not the preprocessing.
- Config values as global constants imported everywhere instead of an object passed in.
- Leaving the notebook as the only entry point.

---

### Q16 ⭐⭐ 🟢 Trunk-based development versus Gitflow for an ML team that runs many experiments. Explain short-lived branches, feature flags, long-lived experiment branches and their cost, how releases and hotfixes work in each model, and which you would pick for a team of 6 shipping a model every two weeks. Say how experiment code that never merges is kept (tags or an archive branch) without cluttering main.
**Asked at:** Editorial Git interview lists (GoLinuxCloud, Naukri Code360, Vskills, PhoenixNAP and DataCamp merge-vs-rebase pages; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** For six people shipping every two weeks I would pick trunk-based development: short-lived branches into main, unfinished work behind flags, releases as tags, and experiments archived as tags instead of long-lived branches.

**Then explain:**
- Trunk-based: branches live a day or two and merge to main often. Main is always releasable. Releases are tags; hotfixes are a fix on main (or a short release branch only if main has moved too far). Less merge pain, easier CI.
- Gitflow: long-lived `develop` and `release/*` branches, feature branches, hotfix branches. It suits versioned products with many supported releases. For a team of six on a two-week cadence it adds merge overhead and drift between branches.
- ML twist: experiments are cheap to start and rarely merge. Long-lived experiment branches rot: they fall behind main, conflict with everything, and nobody can reproduce them. Cost is real: weeks of divergence turn one merge into a mini-project.
- Keep the experiment without cluttering main: tag the last commit (`exp/2026-10-wide-features`), write the result in the tag message or a short doc, then delete the branch. The commit stays reachable through the tag. A shared `archive/` branch namespace is the other common option.
- Unfinished model code merges behind a flag (config value, off by default) so main always builds; turn it on when metrics and tests are ready.
- Failure modes: flags that never get removed (set a cleanup date); a flag changes behaviour in tests only when on (test both); hotfix on main that cannot ship because main holds half-done work (the flag is why this does not happen).

**Example:** Team of six, release every second Friday. Monday: `feat/new-ranker` branch, merged to main behind `USE_NEW_RANKER=false` on Tuesday. A wide-features experiment fails: tag it and delete the branch. Release Friday: tag `release-1.1`. A bug appears Monday: fix on main, tag `release-1.1.1`. In the demo below the history is one straight line plus one merge bubble, and `git branch` lists only `main`.

**Code:** a throwaway-repo walk-through (git 2.43.0).
```sh
# demo.sh
#!/bin/sh
# Trunk-based flow in a throwaway repo: short branch, flag-off merge, archive an experiment as a tag, tagged release, hotfix.
set -e
T=$(mktemp -d); cd "$T"; git init -q -b main; git config user.email a@b.c; git config user.name demo
echo 'MODEL=v1' > config.txt; git add .; git commit -qm "model v1"; git tag release-1.0

# 1. short-lived branch; new model code merged but flagged OFF
git switch -qc feat/new-ranker
echo 'USE_NEW_RANKER=false' >> config.txt; echo 'def new_ranker(): ...' > ranker.py
git add .; git commit -qm "add new ranker behind flag (off)"
git switch -q main; git merge -q --no-ff feat/new-ranker -m "merge: ranker behind flag"; git branch -d feat/new-ranker -q

# 2. an experiment that will never merge: keep it as a tag, then delete the branch
git switch -qc exp/wide-features
echo 'WIDE=1' >> config.txt; git commit -qam "experiment: 400 wide features, metric not better"
git tag -a exp/2026-10-wide-features -m "tried; no gain; see notebook link in wiki"
git switch -q main; git branch -D exp/wide-features -q

# 3. release = a tag on main; hotfix = fix on main, tag again (no long-lived release branch)
echo 'USE_NEW_RANKER=true' > flag.txt; git add .; git commit -qm "turn the flag on"
git tag release-1.1
echo 'fix: null guard' > fix.txt; git add .; git commit -qm "hotfix: null guard"; git tag release-1.1.1

echo "--- branches:"; git branch
echo "--- tags:"; git tag -l
echo "--- history:"; git log --oneline --graph --decorate
echo "--- experiment still reachable:"; git show -s --format='%h %s' exp/2026-10-wide-features^{commit}
```

**Output (my run):** commit hashes differ on every run because timestamps differ.
```text
--- branches:
* main
--- tags:
exp/2026-10-wide-features
release-1.0
release-1.1
release-1.1.1
--- history:
* 5e01680 (HEAD -> main, tag: release-1.1.1) hotfix: null guard
* 5cf9ead (tag: release-1.1) turn the flag on
*   08755dc merge: ranker behind flag
|\  
| * 4ea5443 add new ranker behind flag (off)
|/  
* 250572a (tag: release-1.0) model v1
--- experiment still reachable:
0ce7287 experiment: 400 wide features, metric not better
```

**Follow-ups:**
- *When would Gitflow be right?* Several versions supported in the field at once (an on-prem product), or a heavy manual release gate.
- *Experiment tracking?* Tags keep the code; a tracking tool keeps parameters and metrics (a different topic).
- *Squash or merge commits on main?* Team choice; whichever, keep main linear enough to bisect.

**Common mistakes:**
- Calling any branching "trunk-based" while branches live for weeks.
- Merging half-finished model code to main with the flag on.
- Deleting an experiment branch with no tag, losing the commit after garbage collection.
- A `develop` branch with no clear owner that is always broken.
- Hotfixing release without bringing the fix back to main.

---

### Q17 ⭐⭐ 🟢 What goes into a pull request review checklist for ML code? List at least eight items specific to ML (data leakage, fixed seeds, hard-coded paths, metric on the right split, untracked data version, large diffs from notebooks, missing tests, silent shape or dtype changes), say which a linter could catch, and review a 25-line training function with three planted bugs, naming each bug.
**Asked at:** Editorial MLOps interview guides (DataCamp MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, wecreateproblems, a DEV Community list; search snippets only, not opened); guides, not verified candidate reports; MLOps and ML engineer rounds at product companies, GCCs and IT-services firms
**Say this first (1 line):** My ML review checklist starts with data and evaluation, not style: could the test set influence training, is the metric on the right split, is it reproducible, and what changed in the data version and shapes.

**Then explain:** Checklist (the ones a linter can help with are marked):
- Data leakage: any fit (scaler, encoder, feature selection, imputer) before the split. Not catchable by a linter.
- Metric computed on the right split (test or validation, not train). A linter only hints (unused variables, see below).
- Fixed seeds and `random_state` on splits and models. Partly lintable with a custom rule.
- Hard-coded paths and secrets. Lintable (grep rule or a plugin).
- Data version recorded (hash, tag, table snapshot) with the run. Not lintable.
- Large diffs from notebooks (outputs checked in): strip outputs with `nbstripout`; a pre-commit hook catches it.
- Tests for new logic; a new feature has a unit test and the parity or golden test still passes. CI catches missing tests only with a coverage rule.
- Silent shape, dtype or column-order changes (a float turned into an object, a column renamed). Types and schema checks help; mypy catches only some.
- Mutable defaults, unused imports and variables: ruff does these.
- Class imbalance, stratified split, group split for repeated users, time split for time series.
- Does the PR change the model's inputs without changing the serving code?
- The review target below: a short training function (15 lines here, shorter than the 25 in the question; the review method is the same) with three planted bugs.

**Example:** Bug 1: `SelectKBest.fit_transform(X, y)` runs on the whole frame before `train_test_split`, so the test labels choose the features. Bug 2: `train_test_split` has no `random_state`, so the result changes every run. Bug 3: the printed accuracy is `model.score(Xtr, ytr)`, the training split. Plus a smell: hard-coded `/home/me/data.csv`. On pure random labels the honest accuracy should be near 0.5, which gives a hand-check: the leaky pipeline's accuracy is clearly above 0.5, the training score is very high, and a fixed pipeline lands near 0.5.

**Code:** the target function, the fixed version and a harness on seeded noise data (120 rows, 400 random features, random labels).
```python
# ===== review_target.py =====
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def train_and_report(path="/home/me/data.csv"):              # smell: hard-coded path
    df = pd.read_csv(path)
    y = df["y"]
    X = df.drop(columns="y")
    X = SelectKBest(f_classif, k=20).fit_transform(X, y)      # BUG 1: selection sees the test rows
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3)  # BUG 2: no random_state
    model = LogisticRegression(max_iter=200).fit(Xtr, ytr)
    print("accuracy", round(model.score(Xtr, ytr), 3))       # BUG 3: metric on the TRAIN split
    return model

# ===== fixed.py =====
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline


def train_and_report(path, seed=0):
    df = pd.read_csv(path)
    X, y = df.drop(columns="y"), df["y"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)
    model = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression(max_iter=200)).fit(Xtr, ytr)  # selection inside the pipeline
    print("test accuracy", round(model.score(Xte, yte), 3))
    return model

# ===== harness.py =====
import sys, pathlib, tempfile, numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import review_target, fixed

rng = np.random.default_rng(0)                       # PURE NOISE: 120 rows, 400 features, random labels -> honest accuracy is about 0.5
df = pd.DataFrame(rng.normal(size=(120, 400)), columns=[f"f{i}" for i in range(400)])
df["y"] = rng.integers(0, 2, 120)
p = pathlib.Path(tempfile.mkdtemp()) / "data.csv"; df.to_csv(p, index=False)

print("== buggy, run 3 times (note: prints TRAIN accuracy, and it changes each run)")
for _ in range(3):
    review_target.train_and_report(str(p))
print("== buggy but score on its own test split (what bug 3 hides)")
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
X = SelectKBest(f_classif, k=20).fit_transform(df.drop(columns="y"), df["y"])
Xtr, Xte, ytr, yte = train_test_split(X, df["y"], test_size=0.3, random_state=0)
print("leaky test accuracy:", round(LogisticRegression(max_iter=200).fit(Xtr, ytr).score(Xte, yte), 3), "(labels are random, so this should be about 0.5)")
print("== fixed")
fixed.train_and_report(str(p)); fixed.train_and_report(str(p))
```
```sh
# run.sh
python3 -I harness.py
ruff check --output-format=concise review_target.py
```

**Output (my run):** Python 3.13.17, scikit-learn 1.9.1, ruff 0.16.9.
```text
== buggy, run 3 times (note: prints TRAIN accuracy, and it changes each run)
accuracy 0.905
accuracy 0.857
accuracy 0.821
== buggy but score on its own test split (what bug 3 hides)
leaky test accuracy: 0.667 (labels are random, so this should be about 0.5)
== fixed
test accuracy 0.611
test accuracy 0.611
```
ruff on the target (this ruff default set; rule set may differ by version):
```text
q17/review_target.py:12:10: RUF059 Unpacked variable `Xte` is never used
q17/review_target.py:12:20: RUF059 Unpacked variable `yte` is never used
Found 2 errors.
No fixes available (2 hidden fixes can be enabled with the `--unsafe-fixes` option).
```
So the linter flagged the unused test variables, a clue for bug 3, but did not name any of the three bugs. The fixed run reports 0.611 test accuracy on 36 rows, which is within noise of 0.5 for random labels; I do not read it as skill.

**Follow-ups:**
- *Which check is highest value?* Leakage and metric split; they make a good-looking number meaningless.
- *Can a bot do this review?* It can flag patterns, but a human must confirm leakage and data questions.
- *What do you require in the PR description?* Data version, seed, metric on the right split, and what changed in inputs.

**Common mistakes:**
- Reviewing only formatting.
- Approving a metric jump without asking about the split.
- Accepting notebook diffs with outputs.
- Treating a lint pass as a pass on correctness.

---

### Q18 ⭐⭐ 🟡 Cherry-pick and hotfix backports. Version 2.3 of a scoring service is in production, main has moved on to 2.4 work, and a one-line fix to a null-handling bug landed on main. Show how you backport just that commit to a release/2.3 branch with git cherry-pick, what happens when the commit conflicts, why cherry-picking creates a duplicate commit with a new hash, and how to keep track of which fixes went where. Demonstrate in a throwaway repo.
**Asked at:** Editorial Git interview lists (GoLinuxCloud, Naukri Code360, Vskills, PhoenixNAP and DataCamp merge-vs-rebase pages; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** To backport a fix I switch to `release/2.3`, run `git cherry-pick -x <hash>`, resolve any conflict by hand and continue; it makes a new commit with a new hash that has the same change.

**Then explain:**
- Why a new hash: a commit's hash includes its parent. The same change on a different parent is a different commit, so the copy on the release branch has a new hash. `-x` appends "(cherry picked from commit ...)" so you can trace it.
- Conflict: the release branch has older or different code around the line. Git stops with `UU` status and conflict markers. Edit the file, `git add` it, then `git cherry-pick --continue` (or `--abort` to back out). Always re-run tests on the release branch afterwards, because a clean pick can still be wrong in older code.
- Tracking: `git cherry -v release/2.3 main` marks `-` for commits whose patch is already on release and `+` for those that are not. Also keep a backport label or a changelog line; tools that tag the PR are a team choice.
- Alternatives: fix on the release branch first and merge forward to main, so there is only one change and history stays connected. Cherry-pick is for when the fix was already made on main.
- Failure modes: forgetting to backport to a second supported release; picking a commit that depends on earlier unpicked commits (code compiles, behaves differently); cherry-picking a merge commit (needs `-m`).

**Example:** In the run: `release/2.3` and a 2.4 feature-set commit on main. The null fix on main is `17a9415`; backporting it creates `e6a0f4c` on release. Searching both branches by message shows two commits with different hashes. `git cherry` shows `-` against the null fix (already applied) and `+` against the 2.4 feature-set commit (not on release, correctly). Part B: a second fix ("score never negative") conflicts with a local release tweak ("round score"), so git stops; the resolved line keeps both ideas.

**Code:** run in a throwaway repo (git 2.43.0).
```sh
# demo.sh
#!/bin/sh
T=$(mktemp -d); cd "$T"; git init -q -b main; git config user.email a@b.c; git config user.name demo
cat > score.py <<'PY'
def score(row):
    return row["amount"] * 0.1
PY
git add .; git commit -qm "2.3 scoring service"; git branch release/2.3; git tag v2.3.0
# main moves on to 2.4 work (touches the same area later)
cat > other.py <<'PY'
FEATURE_SET = "v24"
PY
git add .; git commit -qm "2.4: new feature set"
# the one-line null fix lands on main
cat > score.py <<'PY'
def score(row):
    return (row["amount"] or 0) * 0.1
PY
git commit -qam "fix: null amount no longer crashes score()"
FIX=$(git rev-parse --short HEAD)
echo "--- A) clean backport"
git switch -q release/2.3
git cherry-pick -x "$FIX" | head -1
git log --oneline --format='%h %s' -2
echo "--- same change, different hash on each branch:"; git log --oneline --all --grep='null amount'
echo "--- -x records where it came from:"; git log -1 --format=%b
echo "--- git cherry: '-' = an equivalent patch is already on release, '+' = not yet:"; git cherry -v release/2.3 main
echo "--- B) conflicting backport: a second fix on main touches the same line that release changed differently"
git switch -q main
printf 'def score(row):\n    return max((row["amount"] or 0) * 0.1, 0.0)\n' > score.py; git commit -qam "fix: score never negative"
FIX2=$(git rev-parse --short HEAD)
git switch -q release/2.3
printf 'def score(row):\n    return round((row["amount"] or 0) * 0.1, 2)\n' > score.py; git commit -qam "2.3.1: round score"
git cherry-pick -x "$FIX2" 2>&1 | grep -E "CONFLICT|error: could not"
git status --short
echo "--- conflict markers in the file:"; cat score.py
echo "--- resolve by hand (keep both ideas), then continue"
printf 'def score(row):\n    return max(round((row["amount"] or 0) * 0.1, 2), 0.0)\n' > score.py; git add score.py
GIT_EDITOR=true git cherry-pick --continue >/dev/null 2>&1
git log --oneline -4
```

**Output (my run):** hashes differ each run.
```text
--- A) clean backport
[release/2.3 e6a0f4c] fix: null amount no longer crashes score()
e6a0f4c fix: null amount no longer crashes score()
d9019fa 2.3 scoring service
--- same change, different hash on each branch:
17a9415 fix: null amount no longer crashes score()
e6a0f4c fix: null amount no longer crashes score()
--- -x records where it came from:
(cherry picked from commit 17a9415780dc094663046937b4612ff5b3347e29)

--- git cherry: '-' = an equivalent patch is already on release, '+' = not yet:
+ e74237da1751b966478b19db4c6dc4dcf4518323 2.4: new feature set
- 17a9415780dc094663046937b4612ff5b3347e29 fix: null amount no longer crashes score()
--- B) conflicting backport: a second fix on main touches the same line that release changed differently
CONFLICT (content): Merge conflict in score.py
error: could not apply 4cb52c9... fix: score never negative
UU score.py
--- conflict markers in the file:
def score(row):
<<<<<<< HEAD
    return round((row["amount"] or 0) * 0.1, 2)
=======
    return max((row["amount"] or 0) * 0.1, 0.0)
>>>>>>> 4cb52c9 (fix: score never negative)
--- resolve by hand (keep both ideas), then continue
accbc72 fix: score never negative
13c6680 2.3.1: round score
e6a0f4c fix: null amount no longer crashes score()
d9019fa 2.3 scoring service
```

**Follow-ups:**
- *What if the commit touches many files?* Cherry-pick a range (`A..B`), or merge a fix branch that was cut from an old enough base.
- *Rebase instead?* No; rebasing release onto main would pull in 2.4 work.
- *How do you avoid doing the fix twice?* Branch the fix from the oldest supported release and merge it into the newer ones.

**Common mistakes:**
- Forgetting `-x`, so the origin is lost.
- Assuming a clean pick is a correct pick, with no tests on the release branch.
- Cherry-picking one commit of a dependent series.
- Backporting to release but never recording it, then shipping 2.3.2 without it.

---

### Q19 ⭐⭐ 🟡 Make randomness testable. A function train_test_split_and_fit(df, seed) gives slightly different metrics on every run. Explain seeding Python, NumPy (np.random.default_rng) and sklearn random_state, the limits of seeding (multi-threaded libraries, GPU kernels), and how to assert on floats with pytest.approx or np.testing.assert_allclose with a justified tolerance. Show a flaky test and the fixed version, both run.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** Pass a seed through the function, use a local `np.random.default_rng(seed)` and `random_state`, and assert floats with a tolerance I can justify; seeding is for reproducibility, tolerances are for the leftovers.

**Then explain:**
- Where randomness lives: the train/test split, model initialisation, data generation, shuffling, sampling and dropout. Seed all that you use: `random.seed`, `np.random.seed` (legacy global), a local `np.random.default_rng(seed)` (preferred, no hidden state), and `random_state=seed` in scikit-learn.
- Limits: multi-threaded libraries can sum in a different order, so floats differ in the last digits; GPU kernels and some ops are non-deterministic unless a deterministic mode is on (check the framework's docs); different BLAS builds or CPUs give tiny differences; a different library version can change the algorithm.
- So: same machine, same code, same seed should be exactly equal (assert `==`). Across machines use `pytest.approx(abs=...)` or `np.testing.assert_allclose(rtol=..., atol=...)`. Choose the tolerance from the noise you saw (here a metric is deterministic at 1e-6) and write the reason in a comment.
- For the model quality itself, do not assert one lucky number; assert a floor below the spread seen over many seeds.
- Failure modes: a tolerance so wide it hides bugs (`atol=0.1` on a metric); relying on `np.random.seed` while a library uses its own generator; a seed set once at import so test order changes results.

**Example:** `0.1 + 0.2 == 0.3` is `False` in Python, so exact float equality is the wrong tool for computed values. In the data below, 20 seeds gave a metric spread (min 0.678, max 0.822), so a test that demands `> 0.77` on an unseeded split passes only part of the time. In my run of that flaky test, 6 of 8 runs passed and 2 failed with identical code.

**Code:** `fitmod.py` (with `seed=None` reproducing the original bug), the flaky test and the fixed tests. Run with `python3 -I -m pytest`.
```python
# ===== fitmod.py =====
import random
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def make_df(n=300, seed=0):
    rng = np.random.default_rng(seed)               # local generator: no hidden global state
    x = rng.normal(size=(n, 3))
    y = (x[:, 0] + 0.5 * x[:, 1] + rng.normal(scale=1.0, size=n) > 0).astype(int)
    return pd.DataFrame(x, columns=["a", "b", "c"]).assign(y=y)


def train_test_split_and_fit(df, seed=None):
    """seed=None reproduces the original problem: the split changes every call."""
    if seed is not None:
        random.seed(seed); np.random.seed(seed)      # only matters for third-party code using the globals
    Xtr, Xte, ytr, yte = train_test_split(df[["a", "b", "c"]], df["y"], test_size=0.3, random_state=seed)
    m = LogisticRegression(random_state=seed).fit(Xtr, ytr)
    return float(m.score(Xte, yte))

# ===== test_flaky.py =====
from fitmod import make_df, train_test_split_and_fit
def test_flaky():
    # unseeded split: the metric moves around, and the threshold sits right in the middle of that spread
    assert train_test_split_and_fit(make_df()) > 0.77

# ===== test_fixed.py =====
import numpy as np, pytest
from fitmod import make_df, train_test_split_and_fit

GOLDEN = 0.7666666666666667      # recorded once with seed=1 (python3 -I run, scikit-learn 1.9.1)


def test_same_seed_same_metric():
    df = make_df()
    assert train_test_split_and_fit(df, seed=1) == train_test_split_and_fit(df, seed=1)   # exact: same machine, same code


def test_golden_metric_with_tolerance():
    # 1e-6 absolute: allows tiny BLAS/platform differences, still catches a changed split or model
    assert train_test_split_and_fit(make_df(), seed=1) == pytest.approx(GOLDEN, abs=1e-6)


def test_metric_is_good_across_seeds():
    # property test: do not depend on one lucky split; assert a floor below the observed spread (min 0.678 over 20 seeds)
    accs = [train_test_split_and_fit(make_df(), seed=s) for s in range(20)]
    assert min(accs) > 0.60


def test_arrays_close():
    np.testing.assert_allclose(np.array([0.1 + 0.2]), [0.3], rtol=1e-9)   # 0.1+0.2 != 0.3 exactly
```
```ini
# pytest.ini
[pytest]
pythonpath = .
```
```sh
# run.sh
for i in 1 2 3 4 5 6 7 8; do python3 -I -m pytest -q -p no:cacheprovider test_flaky.py | tail -1; done   # flaky, then count
python3 -I -m pytest -q -p no:cacheprovider test_fixed.py
```

**Output (my run):** Python 3.13.17, scikit-learn 1.9.1, numpy 2.5.3, pytest 9.1.1. Spread printed by a one-off script: seed 1 gives 0.7667; across 20 seeds min 0.678, mean 0.772, max 0.822, std 0.034.
The flaky test, 8 runs (count of results), then the fixed file:
```text
      2 1 failed
      6 1 passed
4 passed in 1.50s
```

**Follow-ups:**
- *Why `default_rng` and not `np.random.seed`?* The global seed is shared state: another test or library can change it. A local generator passed into the function is explicit.
- *Can I make a GPU run bit-exact?* Often with deterministic flags and fixed library versions, at some speed cost; do not promise it across hardware. Check the framework docs.
- *What tolerance for an ML metric?* Based on repeat runs: a few standard deviations of the seed spread for quality floors; much tighter (1e-6) for the same-seed regression value.

**Common mistakes:**
- Hard-coding a number copied from one run with no seed.
- Seeding only NumPy while scikit-learn uses its own `random_state`.
- `assert a == b` on floats from different code paths.
- Tolerances picked to make the test pass, without a reason.
- Re-seeding inside the function and surprising callers.

---

### Q20 ⭐⭐ 🟡 pytest features used in ML test suites: fixtures (including scope), parametrize, tmp_path, monkeypatch and markers. Write a conftest.py fixture that builds a small seeded DataFrame once per session, a test that uses tmp_path to check a save and load round trip of a model artifact, and a test that monkeypatches a slow model-download function. Say how you mark and skip slow tests (--runslow style) and show the run.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** Fixtures build shared inputs (scope controls how often), `parametrize` repeats a test over cases, `tmp_path` gives a clean folder, `monkeypatch` swaps slow or networked code for a stub, and a `slow` marker plus a `--runslow` option keeps heavy tests out of the default run.

**Then explain:**
- Fixture scope: `function` (default, rebuilt per test), `module`, `session` (once for the whole run). A seeded small DataFrame is cheap and read-only, so session scope is fine; a trained model used by many tests is a good `module` fixture. Danger: a session fixture that tests mutate leaks state between tests, so return copies or treat it as read-only.
- `parametrize` turns one test into many named cases (`test_fit_on_subsets[10]`); good for sizes, edge values, and dtype cases.
- `tmp_path`: a unique temp directory per test, cleaned up later by pytest. Use it for save and load round trips instead of writing into the repo.
- `monkeypatch`: replace `download_pretrained` for the test only; it is undone afterwards. Patch the name where it is looked up (the module that calls it).
- Markers: register `slow` in `pytest.ini` (otherwise a warning, and an error with `--strict-markers`). A `conftest.py` hook adds a skip to marked tests unless `--runslow` is passed. Also use `pytest -m "not slow"` for the fast gate in CI.
- Failure modes: autouse fixtures that hide a dependency; an order-dependent test that only passes after another one; patching the wrong import path so the real function runs (here it would sleep and raise).

**Example:** Six tests were collected: a round trip (fit, `joblib.dump` to `tmp_path`, reload, same predictions), one monkeypatched test, three parametrized sizes (10, 25 and 50 rows) and one slow test. Hand count: 1 + 1 + 3 + 1 = 6. Default run: 5 pass and 1 skipped. With `--runslow`, the slow test runs and fails on purpose here because there is no network (and the real function sleeps 5 seconds, which is why the run took about 6 seconds).

**Code:** `pytest.ini`, `conftest.py` (fixtures and the `--runslow` hook), the code under test and the tests.
```ini
# pytest.ini
[pytest]
pythonpath = .
markers =
    slow: slow tests, skipped unless --runslow is given
```
```python
# ===== modelio.py =====
import time
import joblib
from sklearn.linear_model import LogisticRegression


def download_pretrained(name: str):
    time.sleep(5)                                   # pretend this is a big network download
    raise RuntimeError("no network in tests")


def fit_and_save(df, path):
    m = LogisticRegression().fit(df[["a", "b"]], df["y"])
    joblib.dump(m, path)
    return m


def load_embeddings(name: str):
    weights = download_pretrained(name)
    return weights

# ===== tests/conftest.py =====
import numpy as np
import pandas as pd
import pytest


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", default=False, help="run tests marked slow")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        return
    skip = pytest.mark.skip(reason="slow: use --runslow to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip)


BUILDS = []                                          # counts how often the fixture body really ran


@pytest.fixture(scope="session")
def small_df():
    BUILDS.append(1)                                 # built once per session, shared by every test
    rng = np.random.default_rng(0)
    x = rng.normal(size=(50, 2))
    return pd.DataFrame({"a": x[:, 0], "b": x[:, 1], "y": (x[:, 0] > 0).astype(int)})


@pytest.fixture(scope="session", autouse=True)
def report_builds():
    yield
    print(f"\n[session fixture small_df built {len(BUILDS)} time(s)]")

# ===== tests/test_modelio.py =====
import joblib
import numpy as np
import pytest
import modelio


def test_save_load_roundtrip(small_df, tmp_path):
    path = tmp_path / "m.joblib"                       # fresh temp dir, auto-cleaned later
    m = modelio.fit_and_save(small_df, path)
    loaded = joblib.load(path)
    np.testing.assert_array_equal(m.predict(small_df[["a", "b"]]), loaded.predict(small_df[["a", "b"]]))


def test_load_embeddings_without_network(monkeypatch):
    monkeypatch.setattr(modelio, "download_pretrained", lambda name: {"fake": name})   # replace the slow call
    assert modelio.load_embeddings("tiny") == {"fake": "tiny"}


@pytest.mark.parametrize("n_rows", [10, 25, 50])
def test_fit_on_subsets(small_df, tmp_path, n_rows):
    modelio.fit_and_save(small_df.head(n_rows), tmp_path / "x.joblib")
    assert (tmp_path / "x.joblib").exists()


@pytest.mark.slow
def test_real_download():
    modelio.load_embeddings("big")                      # would hit the network
```
```sh
# run.sh
python3 -I -m pytest -v -s -p no:cacheprovider               # default: slow test skipped
python3 -I -m pytest -q -p no:cacheprovider --runslow        # includes the slow test (fails here: no network)
```

**Output (my run):** Python 3.13.17, pytest 9.1.1, scikit-learn 1.9.1, joblib 1.6.0.
```text
tests/test_modelio.py::test_save_load_roundtrip PASSED
tests/test_modelio.py::test_load_embeddings_without_network PASSED
tests/test_modelio.py::test_fit_on_subsets[10] PASSED
tests/test_modelio.py::test_fit_on_subsets[25] PASSED
tests/test_modelio.py::test_fit_on_subsets[50] PASSED
tests/test_modelio.py::test_real_download SKIPPED (slow: use --runsl...)
[session fixture small_df built 1 time(s)]
========================= 5 passed, 1 skipped in 1.02s =========================
=========================== short test summary info ============================
FAILED tests/test_modelio.py::test_real_download - RuntimeError: no network i...
1 failed, 5 passed in 6.18s
```
The fixture counter shows the session-scoped DataFrame was built once for the four tests that used it.

**Follow-ups:**
- *Fixture or helper function?* Fixture when pytest should manage setup, teardown and sharing; helper when it is a plain pure function.
- *How do I run only a few?* `-k name`, `-m marker`, or `path::test_name`.
- *Can I share conftest across packages?* Yes: a `conftest.py` applies to its folder and below.

**Common mistakes:**
- Session fixtures that tests modify.
- Unregistered markers.
- Patching `modelio.download_pretrained` after `from modelio import download_pretrained` already copied the name elsewhere.
- Writing test artefacts into the repo instead of `tmp_path`.
- Skipping slow tests forever so they rot; run them nightly in CI.

---
