from build_helpers import code, out
B = {}

B[15] = f"""**Say this first (1 line):** I move the notebook into a package in small steps (functions, a config object, a pipeline with the scaler inside it, tests, a CLI, a pinned environment), and doing it shows the bug: the scaler was fitted on all rows before the split.

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
{code("python", ["q15/notebook_before.py", "q15/src/churn/config.py", "q15/src/churn/pipeline.py", "q15/src/churn/cli.py", "q15/make_data.py", "q15/bug_demo.py", "q15/tests/test_pipeline.py"])}
{code("toml", ["q15/pyproject.toml"])}
{code("shell", ["q15/run_demo.sh"])}

**Output (my run):** Python 3.13.17, scikit-learn 1.9.1, pandas 3.0.5, pytest 9.1.1, uv 0.11.32; a throwaway venv with an editable install. Data is synthetic and seeded (`default_rng(7)`). `notebook_before.py` was not run (it points to a path that does not exist, which is the point). The numbers below were produced by the run.
{out("q15/out_demo.txt")}
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
"""

B[16] = f"""**Say this first (1 line):** For six people shipping every two weeks I would pick trunk-based development: short-lived branches into main, unfinished work behind flags, releases as tags, and experiments archived as tags instead of long-lived branches.

**Then explain:**
- Trunk-based: branches live a day or two and merge to main often. Main is always releasable. Releases are tags; hotfixes are a fix on main (or a short release branch only if main has moved too far). Less merge pain, easier CI.
- Gitflow: long-lived `develop` and `release/*` branches, feature branches, hotfix branches. It suits versioned products with many supported releases. For a team of six on a two-week cadence it adds merge overhead and drift between branches.
- ML twist: experiments are cheap to start and rarely merge. Long-lived experiment branches rot: they fall behind main, conflict with everything, and nobody can reproduce them. Cost is real: weeks of divergence turn one merge into a mini-project.
- Keep the experiment without cluttering main: tag the last commit (`exp/2026-10-wide-features`), write the result in the tag message or a short doc, then delete the branch. The commit stays reachable through the tag. A shared `archive/` branch namespace is the other common option.
- Unfinished model code merges behind a flag (config value, off by default) so main always builds; turn it on when metrics and tests are ready.
- Failure modes: flags that never get removed (set a cleanup date); a flag changes behaviour in tests only when on (test both); hotfix on main that cannot ship because main holds half-done work (the flag is why this does not happen).

**Example:** Team of six, release every second Friday. Monday: `feat/new-ranker` branch, merged to main behind `USE_NEW_RANKER=false` on Tuesday. A wide-features experiment fails: tag it and delete the branch. Release Friday: tag `release-1.1`. A bug appears Monday: fix on main, tag `release-1.1.1`. In the demo below the history is one straight line plus one merge bubble, and `git branch` lists only `main`.

**Code:** a throwaway-repo walk-through (git 2.43.0).
{code("shell", ["q16/demo.sh"])}

**Output (my run):** commit hashes differ on every run because timestamps differ.
{out("q16/out_demo.txt")}

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
"""

B[17] = f"""**Say this first (1 line):** My ML review checklist starts with data and evaluation, not style: could the test set influence training, is the metric on the right split, is it reproducible, and what changed in the data version and shapes.

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
{code("python", ["q17/review_target.py", "q17/fixed.py", "q17/harness.py"])}
{code("shell", ["q17/run.sh"])}

**Output (my run):** Python 3.13.17, scikit-learn 1.9.1, ruff 0.16.9.
{out("q17/out_run.txt")}
ruff on the target (this ruff default set; rule set may differ by version):
{out("q17/out_ruff.txt")}
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
"""

B[18] = f"""**Say this first (1 line):** To backport a fix I switch to `release/2.3`, run `git cherry-pick -x <hash>`, resolve any conflict by hand and continue; it makes a new commit with a new hash that has the same change.

**Then explain:**
- Why a new hash: a commit's hash includes its parent. The same change on a different parent is a different commit, so the copy on the release branch has a new hash. `-x` appends "(cherry picked from commit ...)" so you can trace it.
- Conflict: the release branch has older or different code around the line. Git stops with `UU` status and conflict markers. Edit the file, `git add` it, then `git cherry-pick --continue` (or `--abort` to back out). Always re-run tests on the release branch afterwards, because a clean pick can still be wrong in older code.
- Tracking: `git cherry -v release/2.3 main` marks `-` for commits whose patch is already on release and `+` for those that are not. Also keep a backport label or a changelog line; tools that tag the PR are a team choice.
- Alternatives: fix on the release branch first and merge forward to main, so there is only one change and history stays connected. Cherry-pick is for when the fix was already made on main.
- Failure modes: forgetting to backport to a second supported release; picking a commit that depends on earlier unpicked commits (code compiles, behaves differently); cherry-picking a merge commit (needs `-m`).

**Example:** In the run: `release/2.3` and a 2.4 feature-set commit on main. The null fix on main is `17a9415`; backporting it creates `e6a0f4c` on release. Searching both branches by message shows two commits with different hashes. `git cherry` shows `-` against the null fix (already applied) and `+` against the 2.4 feature-set commit (not on release, correctly). Part B: a second fix ("score never negative") conflicts with a local release tweak ("round score"), so git stops; the resolved line keeps both ideas.

**Code:** run in a throwaway repo (git 2.43.0).
{code("shell", ["q18/demo.sh"])}

**Output (my run):** hashes differ each run.
{out("q18/out_demo.txt")}

**Follow-ups:**
- *What if the commit touches many files?* Cherry-pick a range (`A..B`), or merge a fix branch that was cut from an old enough base.
- *Rebase instead?* No; rebasing release onto main would pull in 2.4 work.
- *How do you avoid doing the fix twice?* Branch the fix from the oldest supported release and merge it into the newer ones.

**Common mistakes:**
- Forgetting `-x`, so the origin is lost.
- Assuming a clean pick is a correct pick, with no tests on the release branch.
- Cherry-picking one commit of a dependent series.
- Backporting to release but never recording it, then shipping 2.3.2 without it.
"""

B[19] = f"""**Say this first (1 line):** Pass a seed through the function, use a local `np.random.default_rng(seed)` and `random_state`, and assert floats with a tolerance I can justify; seeding is for reproducibility, tolerances are for the leftovers.

**Then explain:**
- Where randomness lives: the train/test split, model initialisation, data generation, shuffling, sampling and dropout. Seed all that you use: `random.seed`, `np.random.seed` (legacy global), a local `np.random.default_rng(seed)` (preferred, no hidden state), and `random_state=seed` in scikit-learn.
- Limits: multi-threaded libraries can sum in a different order, so floats differ in the last digits; GPU kernels and some ops are non-deterministic unless a deterministic mode is on (check the framework's docs); different BLAS builds or CPUs give tiny differences; a different library version can change the algorithm.
- So: same machine, same code, same seed should be exactly equal (assert `==`). Across machines use `pytest.approx(abs=...)` or `np.testing.assert_allclose(rtol=..., atol=...)`. Choose the tolerance from the noise you saw (here a metric is deterministic at 1e-6) and write the reason in a comment.
- For the model quality itself, do not assert one lucky number; assert a floor below the spread seen over many seeds.
- Failure modes: a tolerance so wide it hides bugs (`atol=0.1` on a metric); relying on `np.random.seed` while a library uses its own generator; a seed set once at import so test order changes results.

**Example:** `0.1 + 0.2 == 0.3` is `False` in Python, so exact float equality is the wrong tool for computed values. In the data below, 20 seeds gave a metric spread (min 0.678, max 0.822), so a test that demands `> 0.77` on an unseeded split passes only part of the time. In my run of that flaky test, 6 of 8 runs passed and 2 failed with identical code.

**Code:** `fitmod.py` (with `seed=None` reproducing the original bug), the flaky test and the fixed tests. Run with `python3 -I -m pytest`.
{code("python", ["q19/fitmod.py", "q19/test_flaky.py", "q19/test_fixed.py"])}
{code("ini", ["q19/pytest.ini"])}
{code("shell", ["q19/run.sh"])}

**Output (my run):** Python 3.13.17, scikit-learn 1.9.1, numpy 2.5.3, pytest 9.1.1. Spread printed by a one-off script: seed 1 gives 0.7667; across 20 seeds min 0.678, mean 0.772, max 0.822, std 0.034.
The flaky test, 8 runs (count of results), then the fixed file:
{out("q19/out_run.txt")}

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
"""

B[20] = f"""**Say this first (1 line):** Fixtures build shared inputs (scope controls how often), `parametrize` repeats a test over cases, `tmp_path` gives a clean folder, `monkeypatch` swaps slow or networked code for a stub, and a `slow` marker plus a `--runslow` option keeps heavy tests out of the default run.

**Then explain:**
- Fixture scope: `function` (default, rebuilt per test), `module`, `session` (once for the whole run). A seeded small DataFrame is cheap and read-only, so session scope is fine; a trained model used by many tests is a good `module` fixture. Danger: a session fixture that tests mutate leaks state between tests, so return copies or treat it as read-only.
- `parametrize` turns one test into many named cases (`test_fit_on_subsets[10]`); good for sizes, edge values, and dtype cases.
- `tmp_path`: a unique temp directory per test, cleaned up later by pytest. Use it for save and load round trips instead of writing into the repo.
- `monkeypatch`: replace `download_pretrained` for the test only; it is undone afterwards. Patch the name where it is looked up (the module that calls it).
- Markers: register `slow` in `pytest.ini` (otherwise a warning, and an error with `--strict-markers`). A `conftest.py` hook adds a skip to marked tests unless `--runslow` is passed. Also use `pytest -m "not slow"` for the fast gate in CI.
- Failure modes: autouse fixtures that hide a dependency; an order-dependent test that only passes after another one; patching the wrong import path so the real function runs (here it would sleep and raise).

**Example:** Six tests were collected: a round trip (fit, `joblib.dump` to `tmp_path`, reload, same predictions), one monkeypatched test, three parametrized sizes (10, 25 and 50 rows) and one slow test. Hand count: 1 + 1 + 3 + 1 = 6. Default run: 5 pass and 1 skipped. With `--runslow`, the slow test runs and fails on purpose here because there is no network (and the real function sleeps 5 seconds, which is why the run took about 6 seconds).

**Code:** `pytest.ini`, `conftest.py` (fixtures and the `--runslow` hook), the code under test and the tests.
{code("ini", ["q20/pytest.ini"])}
{code("python", ["q20/modelio.py", "q20/tests/conftest.py", "q20/tests/test_modelio.py"])}
{code("shell", ["q20/run.sh"])}

**Output (my run):** Python 3.13.17, pytest 9.1.1, scikit-learn 1.9.1, joblib 1.6.0.
{out("q20/out_run.txt")}
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
"""
