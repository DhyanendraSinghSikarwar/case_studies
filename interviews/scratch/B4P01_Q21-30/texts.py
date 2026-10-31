T = {}

T[21] = r"""
**Say this first (1 line):** I write one `validate(df)` function in plain pandas that checks every rule, collects the problems in a list and returns them all, so the team fixes the data once instead of five times.

**Then explain:**
- Why plain pandas: no extra dependency, I control the messages, and it is easy to explain. pandera is the better pick when many people share schemas (declare once, `lazy=True` collects all failures, I cross-check it below). pydantic validates row by row, which is slow and clumsy for a big frame, so I keep it for configs and API payloads.
- Rules, in order: columns exist, dtype family is right, key not null, key unique, value in range, category in the allowed set. If a column is missing, I report it and skip the other checks on that column.
- Where it runs: at ingest (reject or quarantine the file), before training (hard stop, do not train on bad data), before serving (cheap schema check on each batch or request). Same function, different strictness.
- On failure: the job exits non-zero, an alert goes out with the violation list, and the pipeline keeps using the last good dataset or model. I never silently fill or drop rows in the validator.
- Two traps from my own run: one null turns an integer id column into float, so I use nullable `Int64` and check dtype families; and pandas 3 shows text as `str`, not `object`, so exact string dtype checks break across versions.

**Example:** The bad frame has 4 rows. `loan_id = [1, 1, NA, 4]` gives a null key and a duplicate id 1. `age = [25, 17, 130, 40]` puts rows 1 and 2 out of range. `segment` has `vip`, which is not allowed. That is four planted problems and the function reports exactly four lines. The good frame returns an empty list.

**Code:** `python3 -I q21.py`
{{PY:q21/q21.py}}

**Output (my run):** pandas 3.0.5, pandera 0.35.0 (pandera also reports 6 failure cases because it lists duplicates and each bad age separately).
{{OUT:q21/q21.out}}

**Follow-ups:**
- *Hard rule or warning?* Keys, schema and categories are hard rules. Distribution checks (mean shifted) are warnings with thresholds, and they belong to monitoring, not to this function.
- *Why not Great Expectations?* It is fine for big teams, but it is heavier. For a small pipeline a 30-line function plus tests is easier to own (check current docs if the team already uses it).
- *How do you test the validator?* With the good frame and one frame per rule, each asserting the exact message. A validator without tests is itself untested code.

**Common mistakes:**
- Raising on the first problem, so the data team fixes one issue per run.
- Checking `dtype == "object"` or `"int64"` as strings and breaking after a pandas upgrade or after one null appears.
- Validating after `fillna`, which hides the nulls.
- Forgetting uniqueness of the id, then joining and silently duplicating rows.
"""

T[22] = r"""
**Say this first (1 line):** Leakage tests check the split and the preprocessing, not just the score: no shared ids between train and test, scaler statistics equal to train-only statistics, and an alarm when the score is too good.

**Then explain:**
- Three classic leaks: fit a scaler or imputer on all rows before splitting; the same entity in both train and test (duplicates, or several rows per customer); a feature built from the target or from the future.
- Test 1, id overlap: `set(train.id) & set(test.id)` must be empty. If rows from one customer can appear twice, split by customer group, not by row.
- Test 2, scaler stats: after fitting, `scaler.mean_` must equal the train mean. Scale-before-split leaks only a little, so the score barely moves (my run shows 0.708 vs 0.708). The stats test still catches it. A score alarm would not.
- Test 3, score alarm: if AUC is far above what this problem allows, stop and look for leakage. The ceiling is a judgement per problem; mine is 0.90 for a weak-signal task.
- Best fix is structural: put the scaler inside a `Pipeline` and use `GroupKFold` or a split by id, so the leak cannot be written by accident.

**Example:** Seed 0, 400 rows, `x1` weakly predicts `y`. I duplicate 100 rows before the split, so 41 ids land in both train and test; a RandomForest memorises them and reports AUC 0.841 against an honest 0.576. A feature `leak = 5*y + noise` gives AUC 1.000 against an honest 0.708. All of this is in the output below.

**Code:** `python3 -I q22.py`
{{PY:q22/q22.py}}

**Output (my run):** Python 3.13, scikit-learn 1.9.1, numpy 2.5.3, pandas 3.0.5, seed 0.
{{OUT:q22/q22.out}}

**Follow-ups:**
- *Time series?* Split by time (train on past, test on future) and add a test that `max(train.date) < min(test.date)`.
- *Cross-validation?* Put preprocessing inside the `Pipeline` passed to `cross_val_score`, so each fold refits it on its own training part.
- *Is a high score always a leak?* No. It is a reason to investigate. Some tasks are easy. The alarm triggers a human, not an automatic failure of the model.

**Common mistakes:**
- Fitting `StandardScaler`, `SimpleImputer` or target encoding on the whole dataset first.
- Random row split when the same customer has many rows.
- Tuning hyperparameters on the test set and then calling it unbiased.
- Trusting a good score without a baseline to compare against.
"""

T[23] = r"""
**Say this first (1 line):** Property-based testing states a rule that must hold for all inputs (output in [0, 1], sizes add up, no row lost), and Hypothesis generates many inputs, finds one that breaks the rule and shrinks it to the smallest example.

**Then explain:**
- Properties for a min-max scaler: same length out, every value in [0, 1] for finite input, bigger input never gives smaller output, and a defined behaviour for constant columns and NaN or inf (raise or return zeros, but never silent NaN).
- Properties for a splitter: train plus test sizes equal n, every index appears exactly once (no loss, no duplicate), both sides non-empty when n >= 2, same seed gives the same split.
- In my run the naive scaler failed on `[0.0]` (a single row is also a constant column: 0/0 gives NaN) and on `[nan]`. The naive splitter sampled with replacement and truncated with `int()`, so it failed on `n=15` (9 + 7 rows is not 15, and index 4 is duplicated) and on `n=2` (empty test set).
- The monotone property passed for both, which is a useful result too: it tells me that part is safe.
- Worth it for pure functions with clear rules: scalers, splitters, encoders, metric code, parsers. Not worth it for plumbing, IO, or model training. Example tests stay for known regression cases.

**Example:** Hand-check the shrunk case: `minmax([0.0])` computes `(0 - 0) / (0 - 0) = 0/0 = nan`, and `nan >= 0` is False, so the property fails. For the splitter, `n=2, frac=0.25`: `int(2 * 0.25) = 0`, so the test set is empty.

**Code:** `IMPL=impl_naive` or `IMPL=impl_fixed` picks which implementation the same tests run against. `derandomize=True` makes the run repeatable.
{{PY:q23/impl_naive.py|q23/impl_fixed.py|q23/test_props.py}}
```bash
IMPL=impl_naive python3 -I -m pytest -q -p no:cacheprovider --tb=short test_props.py
IMPL=impl_fixed python3 -I -m pytest -q -p no:cacheprovider --tb=short test_props.py
```

**Output (my run):** naive output is trimmed (warnings and long assertion helpers removed); hypothesis 6.170.11, pytest 9.1.1, numpy 2.5.3. The `n=15` split case did not shrink further because that failure depends on the random draw.
{{OUT:q23/naive_short.out|q23/fixed.out}}

**Follow-ups:**
- *Why does Hypothesis try NaN and inf?* Because real data has them. That is the point: it explores the places I forgot.
- *How do I replay a failure?* Hypothesis keeps a database of failing examples locally and prints a reproduce hint. I also turn a found case into a normal example test so the regression stays pinned.
- *Float roundoff?* Compare with `pytest.approx` or `np.isclose`. Also note that tiny differences can collapse into the same scaled value, so I test "non-decreasing", not "strictly increasing".

**Common mistakes:**
- Writing a property that just re-implements the function, so it can never fail.
- Unbounded floats, which find overflow in every function and bury the real rules (I bounded floats to +/- 1e6 on purpose).
- Leaving the test random in CI with no seed policy, then being unable to reproduce.
- Using Hypothesis everywhere. It costs run time and thinking time.
"""

T[24] = r"""
**Say this first (1 line):** Coverage only tells me which lines ran during tests, not whether the tests checked anything or used the right data, so 92 percent coverage can still ship a scaling bug.

**Then explain:**
- Line coverage: was this line executed. Branch coverage: was each side of every `if` taken. Branch is stricter and I turn it on (`--cov-branch`).
- What it cannot see: missing assertions, wrong expected values, and data coverage. A scaler tested only with `lo = 0` runs every line and never notices a wrong formula.
- Sensible target: a floor around the team's current level (often 70-85 percent; no magic number), a fail-under so it never drops, and a diff-coverage rule: new or changed lines in a PR must be covered (for example 80 percent or more). Diff coverage punishes new untested code and does not force teams to chase old code.
- Honest use: coverage finds untested code. It does not prove tested code is right. Pair it with property tests, regression tests on real examples, and review.
- In ML repos watch for the big blind spots: data issues, training loops marked `# pragma: no cover`, and notebooks that are not measured at all.

**Example:** `scale(x, lo, hi)` returns `(x - lo) / hi`; it should divide by `hi - lo`. One test, `scale(5, 0, 10, clip=True) == 0.5`, passes because `lo = 0` hides the bug. Line coverage is 100 percent, branch coverage is 86 percent (the `clip=False` path was never taken), and the bug is still there. A second test with `lo = 10` fails: expected 0.5, got 0.25. The bug was found by a better test, not by any coverage number.

**Code:** the function and tests, the commands, and the diff-coverage demo (temp git repo).
{{PY:q24/scaling.py|q24/test_scaling.py|q24/test_scaling_more.py}}
```bash
# line coverage, then branch coverage, both failing under 100
python3 -I -m pytest -q -p no:cacheprovider --cov=scaling --cov-report=term-missing --cov-fail-under=100 test_scaling.py
python3 -I -m pytest -q -p no:cacheprovider --cov=scaling --cov-branch --cov-report=term-missing --cov-fail-under=100 test_scaling.py
# diff coverage in a throwaway git repo (needs: pip install diff-cover)
python3 -I -m pytest -q --cov=lib --cov-report=xml test_lib.py
diff-cover coverage.xml --compare-branch=main~1 --fail-under=80
```

**Output (my run):** coverage 7.17.0, pytest-cov 7.1.0, diff-cover 10.6.0. First the three runs, then the diff-coverage run: the PR added a 4-line function with no test, so 1 of 4 new lines is covered (25 percent) and the gate fails.
{{OUT:q24/q24.out|q24/diffcov.out}}

**Follow-ups:**
- *Is 100 percent a good target?* No. It pushes people to write assertion-free tests. A fail-under floor plus a diff rule works better.
- *How do you measure test quality instead?* Mutation testing (tools like mutmut; concept, not run here) changes the code and checks that a test fails. That catches the `/ hi` bug.
- *Where does the threshold live?* In `pyproject.toml` or CI config, so it is the same on every laptop and in CI.

**Common mistakes:**
- Treating the coverage percent as a quality score.
- Counting tests that call the function but assert nothing.
- Only using the easy input (`lo = 0`, no NaN, balanced classes).
- Excluding hard code with `# pragma: no cover` until the number looks good.
"""

T[25] = r"""
**Say this first (1 line):** I give Git one good commit and one bad commit plus a script that exits 0 for good and 1 for bad, and `git bisect run` finds the first bad commit by binary search in about log2 of N steps.

**Then explain:**
- Setup: `git bisect start HEAD v1.0`. The first commit is bad, the second is good. Git checks out the middle commit, runs my script, reads the exit code, and halves the range.
- Exit codes: 0 means good, 1 to 127 (except 125) means bad, 125 means "cannot test this commit, skip it". A commit that does not compile or install is a skip, not a bad.
- Steps: 12 commits after the tag means about 4 tests instead of 12. My run tested 5 commits because one of them was a skip.
- The script must be deterministic: seeded data, fixed threshold on the metric, no network. A threshold like "accuracy >= 0.85" is better than "accuracy equals 0.885".
- A flaky test breaks bisect, because one wrong answer sends Git into the wrong half and it names a confident, wrong commit. My demo makes the check lie once and Git blames c8 instead of c9. Fix: make it deterministic, or run it several times in the script and only exit 1 when it fails every time.

**Example:** A tag `v1.0` has accuracy 0.885. Twelve commits later HEAD has 0.615. Commit c6 does not compile (syntax error), c7 fixes it, and c9 changes `scale` from 1.0 to 0.6 in `cfg.json`. Bisect skips c6 and returns `c9` as the first bad commit. Hand-check: with scale 0.6 a class-1 point needs x >= 0.833 to pass the 0.5 threshold, so most class-1 rows are wrong and accuracy falls from 0.885 to 0.615 (the HEAD line in the output).

**Code:** the whole demo, run in a temp repo with fixed commit dates, so the hashes and the bisect path are the same every run.
{{SH:q25/bisect_demo.sh}}

**Output (my run):** git 2.43.0. Five commits tested (c6 skipped, c3 good, c8 good, c10 bad, c9 bad), culprit c9. Short hashes are replaced with `<sha>`.
{{OUT:q25/bisect.out}}

**Follow-ups:**
- *What if the tag is not good?* Bisect only works if the good commit is really good. Check it first by running the script on it.
- *Can I bisect a metric, not a pass/fail?* Yes: the script computes the metric and exits 1 below a threshold. Pick the threshold with margin so noise cannot flip it.
- *How do I finish?* `git bisect reset` returns to where I started. Then I write a regression test so the fix stays.

**Common mistakes:**
- Using an unseeded training run as the check, so results flip between runs.
- Marking a broken build as bad instead of skipping it, so Git blames the build break.
- Forgetting `git bisect reset` and committing on a detached HEAD.
- Not saving the real culprit: after bisect, add a regression test, or the bug can return.
"""

T[26] = r"""
**Say this first (1 line):** I put the checks in `.pre-commit-config.yaml` so they run on every `git commit` (strip notebook outputs, block big files, block obvious secrets, lint with ruff), and I run the same config in CI because anyone can skip local hooks.

**Then explain:**
- pre-commit runs each hook on the staged files only, so it is fast. If a hook modifies files (nbstripout, ruff `--fix`) the commit fails once, and I `git add` and commit again.
- My four hooks: `nbstripout` cleans notebooks (small diffs, no leaked data in outputs); a 5 MB size check points to DVC or Git LFS; a regex secrets check; `ruff check`.
- The regex secrets hook is a tripwire, not a scanner. It misses many leaks and gives false alarms. Real teams use a maintained secret scanner (for example detect-secrets or gitleaks; check current docs) and also rotate any key that ever reached a commit.
- Hooks can be bypassed (`git commit --no-verify`) or never installed. So CI runs `pre-commit run --all-files`, and branch protection (hosted-service setting, check current docs) makes that check required.
- For a demo that runs offline I used `repo: local` hooks. In a real repo most teams pin published hook repos with `rev:` and keep the versions updated.

**Example:** My first commit adds a notebook with an output, a 6 MB file, `API_KEY = "sk_live_abcdef123456"` and a script with an unused import. All four hooks fail: nbstripout rewrites the notebook, the size check names `big.bin` (6.0 MB), the secrets check flags `config.py:1`, and ruff reports F401 for `train.py`. After removing the big file, reading the key from the environment, deleting the import and re-adding the cleaned notebook, the second commit passes all four.

**Code:** config, the two hook scripts, and the demo run in a temp git repo.
{{YAML:q26/pre-commit-config.yaml}}
{{PY:q26/tools/check_big_files.py|q26/tools/check_secrets.py}}
{{SH:q26/demo.sh}}

**Output (my run):** pre-commit 4.7.0, ruff 0.16.9, nbstripout 0.9.1. The config also parses with pyyaml (4 hooks). Warnings from nbstripout about missing cell ids are filtered out. The commit hash is from this run.
{{OUT:q26/demo.out}}

**Follow-ups:**
- *Hook too slow?* Run only fast checks locally (format, lint, size, secrets) and move tests to CI.
- *What about a key already committed?* Rotate it first. Removing it from history (git filter-repo) comes second, because clones and forks may still have it.
- *Big files that are really needed?* Version them with DVC or Git LFS (Part 4 covers DVC), not plain Git.

**Common mistakes:**
- Relying on local hooks only, with no CI check.
- Believing a regex hook catches all secrets.
- Committing notebooks with outputs, so a customer table sits in Git history.
- Not telling new team members to run `pre-commit install`.
"""

T[27] = r"""
**Say this first (1 line):** I use semantic versioning MAJOR.MINOR.PATCH for the package, tag each release with `git tag -a vX.Y.Z`, read the version at runtime from package metadata, and store the code tag and data version next to the model artifact so I can roll back by installing the previous tag.

**Then explain:**
- PATCH: bug fix, same contract (clamp negative income). MINOR: new feature that old callers can ignore (an optional `tenure_years` argument). MAJOR: anything that can break a caller, and a change of output scale is exactly that (0-1 to 0-100 breaks every threshold downstream).
- A retrained model with the same features and scale is usually a patch or minor, but I also record a separate model version in the registry. Code version and model version are different things, and both must be traceable.
- Link them: the model card or registry entry stores code tag, data version (a DVC revision, snapshot id or hash) and metrics. From any prediction I can get to code, data and model.
- Single source of truth: the version lives in `pyproject.toml`, and the code reads it with `importlib.metadata.version`, so no second copy can drift.
- Rollback: the previous tag is still installable. Check it out or reinstall that version, and the model card shows the old version and old output scale. The old model artifact stays in the registry, so I do not retrain in an emergency.

**Example:** Releases: 1.0.0 (first), 1.1.0 (optional argument, backward compatible), 1.1.1 (clamp negatives), 2.0.0 (output 0-100, BREAKING). Hand-check the scale: `score(40)` gives 0.4 on 1.1.1 and 40 on 2.0.0, and the output below shows exactly that after the rollback.

**Code:** run in a temp repo with fixed commit dates; installed into a venv with the hatchling build backend (installed locally, no network needed).
{{SH:q27/demo.sh}}

**Output (my run):** git 2.43.0, Python 3.13, hatchling 1.32.4. `git describe` hash replaced with `<sha>`.
{{OUT:q27/demo.out}}

**Follow-ups:**
- *Annotated or lightweight tags?* Annotated (`-a`): they carry author, date and message, and show in `git describe`. I use them for releases.
- *Do I need to bump for a retrain?* My rule: new model artifact always gets a registry version. The package version moves only if the code or contract changed.
- *Calendar versioning?* Some teams use dates for data-heavy projects. Pick one scheme, write it down, and automate the bump.

**Common mistakes:**
- Version number hard-coded in two places (`pyproject.toml` and `__init__.py`).
- Changing the output scale in a patch release.
- Shipping a model file with no record of the code and data that made it.
- Moving or re-using a tag after release instead of making a new one.
"""

T[28] = r"""
**Say this first (1 line):** I move every knob into one YAML file, load it into a pydantic model that forbids unknown keys and checks types and ranges, apply overrides in a fixed order (file, then environment, then CLI), and log the resolved config with the run.

**Then explain:**
- Precedence is easy to explain: defaults, then YAML, then `TRAIN_*` environment variables, then CLI flags. The last one wins. The run output below shows each layer winning.
- Fail fast: `extra="forbid"` turns a typo like `epoch` into an error instead of a silent default, and `Field(gt=0, le=1)` stops `learning_rate: fast` or `epochs: 0` before any compute starts.
- All problems are reported together (pydantic collects them), so one run shows both mistakes.
- Log the resolved config (after all overrides) as JSON plus a short hash with each run, in MLflow params or a file next to the model. The YAML file alone is not enough, because the env and CLI values may differ.
- Secrets do not go in YAML. Read them from the environment or a secret manager.
- Hydra (hedge, not run here) is worth it when I need config composition, sweeps over many parameters, or many experiment variants. For one script with ten keys, YAML plus pydantic is enough.

**Example:** `config.yaml` says `epochs: 5`. With `TRAIN_EPOCHS=20` it becomes 20. With `TRAIN_EPOCHS=20 --epochs 3` it becomes 3. The bad file has `learning_rate: fast` and the typo `epoch: 5`; both are reported and the exit code is 2.

**Code:** `python3 -I train.py --config config.yaml`
{{YAML:q28/config.yaml|q28/bad_config.yaml}}
{{PY:q28/train.py}}

**Output (my run):** pydantic 2.13.5, pyyaml 6.0.1.
{{OUT:q28/q28.out}}

**Follow-ups:**
- *Why not argparse only?* Twenty flags are hard to review and repeat. A file can be committed, diffed and reused.
- *Different environments (dev, prod)?* One base file plus a small override file per environment, or env vars for the few values that change (paths, endpoints).
- *Typed config at runtime?* Pass the `Config` object around, not a dict, so a misspelled attribute fails in the IDE and in mypy.

**Common mistakes:**
- Silently ignoring unknown keys.
- Parsing env vars as strings, so `"False"` is truthy.
- Logging only the YAML, not the final values.
- Putting passwords or API keys in the committed config.
"""

T[29] = r"""
**Say this first (1 line):** I replace `print` with the `logging` module, log JSON lines that carry a run id and row counts, raise a specific exception when the whole batch is unusable, log a warning and continue when only a few rows are bad, and never use a bare `except`.

**Then explain:**
- Levels: DEBUG for detail, INFO for normal milestones (batch received, batch scored), WARNING for something odd but handled (dropped rows), ERROR for a failed batch. Production runs at INFO.
- Structured logs (one JSON object per line) can be searched and counted: filter by `run_id`, plot `rows_bad`. Free text cannot.
- Decision rule: a bad row is a data problem, so warn, drop, count it, and continue until a limit (my rule is 20 percent). A missing column or an empty batch is a pipeline problem, so raise `BadInputError`, which the caller catches by type.
- Never `except: pass` or `except Exception: pass`. It hides real bugs and the job "succeeds" with no output. Catch the specific error, log with `exc_info`, then re-raise or return a non-zero exit code so the scheduler marks the run failed.
- Do not log secrets or raw personal data. Log ids and counts. In real code the run id is generated per run (for example `uuid.uuid4().hex[:8]`); I fixed it here so the output is repeatable.

**Example:** Four batches. Good (5 rows): two INFO lines. Ragged (10 rows, 1 bad, 10 percent): a WARNING with `bad_ids: [2]`, then scored 9 rows. Bad (5 rows, 3 bad, 60 percent): a WARNING, then an ERROR and `BadInputError`. No `income` column: ERROR immediately. Process exit code is 1 because at least one batch was rejected.

**Code:** `python3 -I score_batch.py`
{{PY:q29/score_batch.py}}

**Output (my run):** pandas 3.0.5.
{{OUT:q29/q29.out}}

**Follow-ups:**
- *What do you alert on?* Job failed (exit code or ERROR count above 0), rows_bad fraction above the normal level, rows_out much lower than rows_in, and no `batch scored` line at all in the expected time window (silence is a failure too).
- *print vs logging in containers?* Log to stdout in JSON; the platform collects it. Logging handlers and formats stay in one place.
- *How do you trace one request?* The run id (batch) or request id (online) is on every line.

**Common mistakes:**
- `except Exception: pass` or `except: print("error")`.
- Logging inside a tight loop for each row, which floods the log and slows the job.
- Using ERROR for expected conditions, so the alert is always on and everyone ignores it.
- Logging free text with no ids, so you cannot link a message to a run.
"""

T[30] = r"""
**Say this first (1 line):** Type hints document what a function takes and returns and let mypy catch wrong calls before runtime, but they cannot check DataFrame column names or array shapes, so I add runtime validation (pydantic or schema checks) at the boundaries.

**Then explain:**
- What they buy: a self-checking signature, IDE autocomplete and rename help, and mypy errors for calls like passing a list where an array is needed or a string where a float is needed.
- What they cannot check: which columns a `DataFrame` has, the shape or length of an array, value ranges, or NaN. `NDArray[np.float64]` checks dtype only. My run shows both `add_features(df_without_income)` and a 2-D array going through type checking and failing or misbehaving at runtime.
- Practical setup: install `pandas-stubs` (without it mypy complains about missing stubs for pandas, which my first run showed), and use `numpy.typing.NDArray`.
- Gradual adoption: start with loose settings on the old code (no failures from missing annotations), and use `--strict` or per-module strict overrides only for new modules. Fix errors as files are touched. Do not try to annotate everything in one week.
- Boundaries: validate config, API payloads and incoming data with pydantic or the validation function, then pass trusted typed objects inside the code.

**Example:** `features_bad.py` has four planted errors. mypy reports all four with exit code 1: `floor="1"` to `add_features`, a Python list to `log_income`, `floor="1"` to `log_income`, and assigning an array to an `int` variable. The good file passes, also under `--strict`.

**Code:** the typed module, the module with planted errors, and a script for what the type checker cannot see.
{{PY:q30/features.py|q30/features_bad.py|q30/runtime_traps.py}}
```bash
python3 -I -m mypy features.py
python3 -I -m mypy features_bad.py
python3 -I -m mypy --strict features.py
python3 -I runtime_traps.py
```

**Output (my run):** mypy 2.4.0, numpy 2.5.3, pandas 3.0.5, pandas-stubs 3.0.5.260914. Error message wording and stub coverage change between versions (check current docs).
{{OUT:q30/q30.out}}

**Follow-ups:**
- *Do hints slow code down?* No. Python ignores them at runtime. mypy is a separate step in CI or in pre-commit.
- *How do you type DataFrame columns?* mypy cannot. Options are a pandera schema or a pydantic or dataclass row type at the boundary. Treat them as runtime checks.
- *What about `Any`?* It switches checking off. Use it sparingly and mark it with a comment. A pile of `Any` gives false comfort.

**Common mistakes:**
- Adding hints and not running mypy in CI, so they rot.
- Believing `NDArray[np.float64]` checks shape.
- Forgetting pandas-stubs and ignoring all pandas errors with `ignore_missing_imports`.
- Turning on strict for the whole old codebase at once, then switching mypy off in frustration.
"""
