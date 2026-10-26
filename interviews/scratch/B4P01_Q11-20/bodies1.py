from build_helpers import code, out

B = {}

B[11] = f"""**Say this first (1 line):** Loose files say what I want, a compiled pin file says exactly what I got, and a lockfile says it for every platform with hashes; I write only direct dependencies by hand, compile the rest, and never trust a pickle across scikit-learn versions.

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
{code("toml", ["q11/pyproject.toml"])}
{code("python", ["q11/make_pickle.py", "q11/load_pickle.py"])}

**Output (my run):** uv 0.11.32, Python 3.13.17; the `.in` was pinned to scikit-learn 1.9.1, the old venv had 1.6.1. `pip-compile` itself was not run (pip-tools not installed); `uv pip compile` gives the same kind of file. The versions below will differ when you run it later.
{out("q11/out_compile.txt")}
{out("q11/out_load.txt")}
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
"""

B[12] = f"""**Say this first (1 line):** I run ruff, mypy and fast tests in pre-commit for quick feedback, then run the same commands in CI as the real gate, because a local hook can be skipped with `--no-verify`.

**Then explain:**
- Hard gates (fail the build): ruff lint, ruff format check, mypy on the `src` package, fast unit tests, a coverage floor that is modest and never lowered silently. Soft (warn, do not block): stricter mypy on old modules, complexity, docstring rules, slow tests, notebook lint. I tighten a soft check to hard only after the existing violations are fixed.
- Why pre-commit alone is not enough: `git commit --no-verify` skips it, a new contributor may not have run `pre-commit install`, and local tool versions drift. CI runs the same commands from the same pinned dev requirements, and branch protection makes that job required (a hosted setting; check your platform's docs).
- Speed rules so people do not skip: pre-commit only checks changed files; ruff is fast; mypy runs only on `src`; the slow tests are marked and run in CI or on pre-push, not on every commit. If a commit hook takes more than a few seconds, people find the bypass.
- Failure modes: pinned hook versions differ from CI versions (so "passes locally, fails in CI"); `types: [python]` hooks miss notebooks (use `nbstripout` or jupytext, not covered here); auto-fixing hooks edit files and the commit fails once, which confuses newcomers (tell them to re-add and commit again).
- I used `repo: local` hooks because this sandbox cannot clone hook repositories. On a real team I would pin the official hook repos with a `rev`, and let `pre-commit autoupdate` raise PRs (check current docs for the repos and revisions).

**Example:** The bad file `src/train.py` has an unused import and a multi-import line, a mutable default argument `mean=[]`, an unused variable, a function with no type hints and a function that returns a `str` when annotated `int`. By hand: ruff should flag the imports, `B006` (mutable default) and `F841` (unused variable); `ruff format` flags `x/ 2`; mypy flags the missing annotation and the bad return. That is exactly what the run printed. Normal commit blocked (exit 1); with `--no-verify` the same file went into history, and only the CI-style run caught it.

**Code:** `.pre-commit-config.yaml` plus the CI job (both parse as YAML, validated below), tool settings, the bad file and the demo script that runs in a throwaway repo.
{code("yaml", ["q12/.pre-commit-config.yaml", "q12/.github-ci.yml"])}
{code("toml", ["q12/pyproject.toml"])}
{code("python", ["q12/src/train.py"])}
{code("shell", ["q12/run_demo.sh"])}

**Output (my run):** pre-commit 4.7.0, ruff 0.16.9, mypy 2.3.1, git 2.43.0, in a temp repo. The CI workflow was not executed (needs the hosted platform; the action versions in it should be checked against current docs). I did validate that both YAML files parse with pyyaml: `.pre-commit-config.yaml parses ['repos']`, and the CI file parses with keys `name`, `on` and `jobs` (YAML reads the bare word `on` as `True`, which is a known gotcha; GitHub reads it as `on`).
{out("q12/out_demo.txt")}
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
"""

B[13] = f"""**Say this first (1 line):** Put every feature calculation in one module that both training and the service import, add a golden-file parity test that runs both paths on the same 20 rows, and validate inputs with a schema, so a re-implementation cannot drift without a red test.

**Then explain:**
- Why it happens: notebook pandas code is copied into the API as hand-written Python. Small differences (fill value, rounding, category order, timezone) give different numbers, and the model sees inputs it was never trained on. Offline metrics stay good; online quality drops with no error.
- Repo fix: `features.py` is the only place with feature logic. Training calls `build_features(df)`. The service calls the same function (a thin wrapper, no maths). Constants such as the fill value live there too, or in a config both read.
- Golden-file parity test: save 20 raw rows and the features training produced (`golden_features.csv`). The test pushes the raw rows through the real serving function and compares with a tolerance. Include rows with missing values on purpose, since edge cases are where paths differ.
- Schema contract: a pydantic model (or pandera for frames) at the service boundary rejects wrong types early and documents what the model expects.
- Limits: the parity test only covers the sample rows, so choose them to include nulls, zeros and extremes. If a feature uses a fitted statistic (a median), store it as an artefact with the model, not as a number typed in two places. Features computed in a warehouse or feature store are a different setup; this covers the in-repo case.

**Example:** The seeded golden set has 20 rows, rows 3, 11 and 17 with missing income. Training fills missing income with 50,000. The buggy service fills 0 and rounds `income_per_head` to 1 decimal instead of 2. Hand check: row 3's income column should be 50000.0 and the buggy service gives 0.0. The 3 missing-income rows (3, 11, 17) differ on several columns. Three more rows (6, 13, 14, all household size 3) differ only because of rounding: row 6 is 92000/3 = 30666.67 in training and 30666.7 in the buggy service. The test reports 6 of 20 rows differ and names the first one.

**Code:** run with `python3 -I`. `SERVICE=buggy` points the same test at the re-implementation; `SERVICE=shared` points it at the fixed service.
{code("python", ["q13/features.py", "q13/service_buggy.py", "q13/service_shared.py", "q13/make_golden.py", "q13/tests/test_parity.py"])}
{code("ini", ["q13/pytest.ini"])}
{code("shell", ["q13/run.sh"])}

**Output (my run):** Python 3.13.17, pandas 3.0.5, numpy 2.5.3, pytest 9.1.1, pydantic 2.13.5.
{out("q13/out_run.txt")}
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
"""

B[14] = f"""**Say this first (1 line):** I test a model in two groups: pre-train checks that the machinery is sane (shapes, probabilities, can overfit a tiny set), and post-train checks of behaviour (minimum score on a slice, invariance, directional expectation, no leakage), all as ordinary pytest tests on seeded data.

**Then explain:**
- Pre-train tests need no quality bar: output shape, probabilities in [0, 1] and summing to 1, loss goes down on a batch, and the model can memorise 10 rows. If it cannot overfit 10 rows, something in the pipeline is broken.
- Post-train tests check behaviour: a minimum accuracy on an important slice (not only overall), invariance (changing an irrelevant feature should not flip predictions), directional expectation (more of a positively-linked feature should not lower the probability), and no train/test overlap or leaky feature.
- Thresholds: set them from observed spread with a margin, not from one lucky run; otherwise the test is flaky. Record seeds.
- These tests catch pipeline bugs and regressions, not "is the model good enough for the business"; that is evaluation and monitoring.
- Failure modes: a test that passes on a tiny sample for the wrong reason, a threshold too tight, and tests that retrain a big model on every run (use a small fixture trained once per module).

**Example:** Data: 600 rows, x0 pushes class 1 up, x1 pushes it down, a third column is pure noise, split 70/30 stratified, seed 0. Hand expectation: shifting the noise column by 0.5 should flip almost no predictions (limit 2%). Then I inject a bug: the noise column secretly equals the label plus small noise (a leak). The model now leans on it, and shifting it flips 5.6% of predictions, so the invariance test fails and names the number.

**Code:** `test_model.py`, six tests. Set `LEAK=1` to inject the leaky column.
{code("python", ["q14/test_model.py"])}
{code("shell", ["q14/run.sh"])}

**Output (my run):** Python 3.13.17, scikit-learn 1.9.1, pytest 9.1.1.
{out("q14/out_all.txt")}

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
"""
