# Answer bodies for Q1-Q10. {{SH:file}} {{PY:file[,file...]}} {{OUT:name}} are filled by build.py from files that really ran.
B = {}

B[1] = r'''**Say this first (1 line):** Git holds code, small configs and the lockfile; data and models go to a data store, secrets never go in, and a pushed key is treated as leaked, so I rotate it first and clean history second.

**Then explain:**
- **Commit:** source, tests, `params.yaml`, `requirements.txt` or a lockfile, `.gitignore`, `.env.example` (names only, no values), pointer files from DVC or LFS, and notebooks with outputs stripped.
- **Ignore:** `.env`, the 400 MB parquet, the 1.2 GB `model.pkl`, `__pycache__`, `.ipynb_checkpoints`, virtualenvs.
- **Big files, one line each:** Git LFS keeps a tiny pointer in Git and the real file on an LFS server (simple, but it versions files, not pipelines). A data versioning tool such as DVC keeps a small `.dvc` file in Git and the bytes in object storage, and also links data to the pipeline and params.
- **Why not just commit them:** every version of a big binary stays in history forever, clones get slow, and binaries do not diff or merge.
- **Key already pushed:** (1) revoke and rotate it now, because anyone who cloned has it; (2) then remove it from history with `git filter-repo --invert-paths --path <file>` (needs a fresh clone, rewrites all hashes, so the team must re-clone); (3) check the provider's access logs; (4) add a secret scanner (pre-commit or CI). Failure mode: deleting the file in a new commit does nothing, the old commit still has it.

**Example:** The team has `src/`, `params.yaml`, `data/train.parquet`, `models/model.pkl`, `.env`, `notebooks/eda.ipynb`. After the `.gitignore` below, `git ls-files` shows only code, params, requirements, the notebook, `.gitignore` and `.env.example`. `git check-ignore -v` prints the exact rule that hides each big file.

**Code:** the script runs in a temp repo with small stand-in files (400 KB and 1.2 MB, same names). The LFS step only writes `.gitattributes`; there is no LFS server here, so nothing was uploaded.
{{SH:q01_repo_hygiene.sh}}

**Output (my run):** git 2.43.0, git-lfs 3.4.1, git-filter-repo 2.47.0. The key in the demo is a fake string.
{{OUT:q01}}

**Follow-ups:**
- *Git LFS or DVC?* LFS if you only need big files to behave inside Git hosting; DVC if you want data tied to pipelines, remotes you choose, and params. Check your Git host's LFS storage limits (they change).
- *Can I just `git rm` the file?* No. It stays in earlier commits. Rotate, then rewrite history.
- *What stops this next time?* A pre-commit secret scan, a CI scan, and short-lived credentials (roles, not long-lived keys).

**Common mistakes:**
- Cleaning history but never rotating the key.
- Adding `.gitignore` after the file was already committed (ignore rules do not affect tracked files; run `git rm --cached`).
- Committing model files "just this once" and then needing `filter-repo` to shrink the repo.
- Putting the real key in `.env.example`.
'''

B[2] = r'''**Say this first (1 line):** A commit is a snapshot, a branch is a movable name for a commit, HEAD is "where I am now", and the staging area is the draft of the next commit; on a detached HEAD I make a branch with `git switch -c name` before leaving.

**Then explain:**
- **Staging area (index):** what the next commit will contain. `git add` copies changes into it.
- **`git fetch` vs `git pull`:** fetch only downloads and moves `origin/main`; my `main` does not move. `pull` is fetch plus merge (or rebase with `--rebase`). I fetch first when I want to look before I merge.
- **Detached HEAD:** HEAD points at a commit, not a branch (for example after `git checkout v1.0`). New commits there belong to no branch, so switching away leaves them reachable only through the reflog. Fix: `git switch -c hotfix-1.0` while still on them.
- **Status and diffs:** `git status` lists the state of files; `git diff` = working tree vs staging; `git diff --staged` = staging vs last commit. A file edited after `git add` shows as `MM` and appears in both diffs.
- Failure mode: committing on a detached HEAD, switching away, and "losing" the work (recoverable with `git reflog`, but only until it expires).

**Example:** Tag `v1.0` is the first model version. I check out the tag, fix something, commit, then run `git switch -c hotfix-1.0`. The graph shows `hotfix-1.0` hanging off v1 and `main` unchanged.

**Code:** temp repo, a second clone as "origin" side, fixed commit dates.
{{SH:q02_detached_head.sh}}

**Output (my run):** git 2.43.0.
{{OUT:q02}}

**Follow-ups:**
- *I already switched away from the detached commit. Now what?* `git reflog`, find the hash, `git branch rescue <hash>`.
- *Why fetch before pull?* To see incoming commits (`git log main..origin/main`) and avoid a surprise merge.
- *`switch` vs `checkout`?* `switch` moves between branches, `restore` fixes files; `checkout` did both, so it was split. Both still work.

**Common mistakes:**
- Ignoring the "detached HEAD" message and carrying on.
- Thinking `git diff` shows staged changes (it does not; use `--staged`).
- Running `git pull` on a dirty tree and getting a conflict mid-merge.
'''

B[3] = r'''**Say this first (1 line):** Merge keeps history as it happened, rebase replays my commits on top of main for a straight line, squash merge collapses the branch into one commit; I rebase private branches, merge or squash shared ones, and I never rebase what others have pulled.

**Then explain:**
- **Merge (`--no-ff`):** adds a merge commit with two parents. Nothing is rewritten, so it is safe on shared branches. History has side branches.
- **Rebase:** copies my commits onto the new tip of main. Commits get new hashes; the old ones become unreachable. History is linear. Conflicts may appear commit by commit.
- **Squash merge:** all feature commits become one new commit on main. Clean main log, but the individual steps and their authors are not on main, and the feature branch is no longer "merged" in Git's eyes (do not reuse it).
- **Why not rebase shared branches:** rebase rewrites hashes. A teammate who pulled the old commits now has history that disagrees with yours. Pushing needs `--force`, they get duplicate commits or conflicts. If you must, use `--force-with-lease` and tell them.
- **Practical rule:** before opening a PR I rebase my private branch on the latest main; the team's PR button uses merge or squash (a team policy, check your repo settings).

**Example:** `A` is the base. Main gets `M1`. My branch has `F1 F2 F3`. Merge gives a diamond with a merge commit; rebase gives `A M1 F1' F2' F3'`; squash gives `A M1 S`, where `S` has all three changes.

**Code:** one setup function, run three times in a temp repo.
{{SH:q03_merge_rebase_squash.sh}}

**Output (my run):** git 2.43.0, fixed dates so hashes repeat on a rerun with this git version.
{{OUT:q03}}

**Follow-ups:**
- *When do you prefer squash?* Noisy WIP commits ("fix typo", "oops"); one PR = one commit makes `git revert` of the whole feature a single command.
- *When do you avoid it?* When individual commits matter for `git bisect` or attribution.
- *What does `git pull --rebase` do?* Fetches, then rebases my local commits on top of the remote branch instead of making a merge commit.

**Common mistakes:**
- Rebasing a branch someone else branched from.
- Squashing and then continuing work on the same feature branch (it re-conflicts with itself).
- Resolving rebase conflicts with `--skip` and silently dropping a commit.
'''

B[4] = r'''**Say this first (1 line):** The bad commit is already on main and two people pulled it, so I use `git revert`, which adds a new commit that undoes it and rewrites nothing; `reset` is for my own unpushed work and `restore` is for files.

**Then explain:**
- **`git revert <commit>`:** creates an inverse commit. History stays honest, teammates just pull. Reverting a merge commit needs `-m 1`. If later commits touched the same lines, expect a conflict.
- **`git reset`** moves the branch pointer. `--soft`: move the pointer only (changes stay staged). `--mixed` (default): move the pointer and unstage (changes stay in files). `--hard`: move the pointer and throw the changes away.
- **Why not reset here:** after `reset` plus a force push, the two teammates still hold the bad commit and will push it back.
- **`git restore <file>`:** puts one file back from the index (or `--source=<commit>` from any commit); it does not touch history. `--staged` unstages.
- Failure mode: `reset --hard` on uncommitted work cannot be undone (see reflog question for committed work).

**Example:** Three commits: good scaling, BAD scaling, later work. Revert of the BAD commit gives `scaler=standard` again while the later work (`train.py` v2) stays.

**Code:**
{{SH:q04_reset_revert_restore.sh}}

**Output (my run):** git 2.43.0.
{{OUT:q04}}

**Follow-ups:**
- *Can I get the feature back later?* Yes, revert the revert, or cherry-pick the original.
- *When is `reset` fine on shared history?* Almost never; only on a private branch nobody pulled.
- *How do I find which commit broke scaling?* `git bisect` with a test script.

**Common mistakes:**
- Force-pushing a reset to undo a pushed commit.
- Using `reset --hard` to "unstage".
- Forgetting that `revert` of a merge commit needs `-m`.
'''

B[5] = r'''**Say this first (1 line):** For every run I record the code commit (plus a dirty flag), a content hash of the data, the lockfile, config and seeds, hardware and library versions, metrics and a hash of the model file, so I can rebuild the same model or at least explain why I cannot.

**Then explain:**
- **What to record:** git commit and "dirty?", data version (content hash or DVC/lakeFS id), dependency lockfile hash, config and hyperparameters, seeds, Python/OS/GPU/driver/CUDA, metrics, model artifact hash, run date.
- **Git can hold:** code, config, lockfile, the small manifest itself. **Other tools:** data (DVC, object store with versioning), models (registry or artifact store), metrics and runs (experiment tracker), environment (Docker image digest).
- **What still breaks it:** GPU kernels that are nondeterministic (some CUDA ops add floats in varying order; frameworks have a deterministic mode that is slower or limited, check current docs), floating point differing across CPUs and thread counts, unpinned system libraries (CUDA, BLAS, libc), data edited in place, unseeded libraries (data loader workers), time-dependent features.
- **Honest target:** bit-exact is a bonus. Minimum: same data, code and env give metrics within a stated tolerance.
- Failure mode: a manifest written from a dirty working tree names a commit that does not match what ran. Store the dirty flag, or refuse to train when dirty.

**Example:** `run.json` says commit `760ecc4`, data hash `2a2b86...`, `numpy 2.5.3`, seed 42, `auc 0.91`, model hash. Six months later I check out that commit, fetch the data with that hash, install the pinned versions, rerun, and compare the model hash or metric.

**Code:** `python3 -I`; uses a temp git repo and a stand-in model file (random bytes from a seeded generator).
{{PY:q05_run_manifest.py}}

**Output (my run):** Python 3.13.17, numpy 2.5.3.
{{OUT:q05}}

**Follow-ups:**
- *Is a seed enough?* No. It controls randomness, not the data, code, library versions or GPU kernels.
- *Where is the manifest stored?* Next to the model artifact and in the tracker; also logged in the registry entry.
- *Docker?* It pins the environment (store the image digest), but not data or hardware.

**Common mistakes:**
- Recording a branch name instead of a commit hash.
- "Data v2" as a folder name, not a content hash.
- Pinning direct dependencies only (no lockfile for transitive ones).
- Promising bit-exact results on GPU.
'''

B[6] = r'''**Say this first (1 line):** Nothing is gone yet: `git reflog` lists where HEAD has been, so I find the commit I had before the reset and move the branch back to it (or hang a rescue branch on it).

**Then explain:**
- `reset --hard HEAD~2` moves the branch back two commits. The two commits still exist as objects; they are just unreachable from any branch.
- `git reflog` shows each HEAD move with `HEAD@{n}`. I pick the entry from before the reset (`HEAD@{1}` here) and run `git reset --hard <hash>` or, safer, `git branch rescue <hash>`.
- **How long:** reflog entries expire; commonly stated defaults are about 90 days for reachable entries and 30 days for unreachable ones (`gc.reflogExpire`, `gc.reflogExpireUnreachable`). I could not verify the numbers on this machine, so check the current git-config docs. `git gc` can then delete the objects.
- **What reflog cannot recover:** edits never committed (in my run the tracked unstaged edit was gone after `reset --hard`), files that were never staged or committed in the first place, and a different clone's reflog (reflog is local).
- **Stash:** `git stash` parks uncommitted work safely before risky commands; `git stash pop` brings it back.

**Example:** `c0 baseline`, `c1 add cross validation`, `c2 add early stopping`. After the mistaken reset only `c0` shows. The reflog still lists `c2` at `HEAD@{1}`; resetting to that hash brings back both commits and the file says `step2`.

**Code:**
{{SH:q06_reflog.sh}}

**Output (my run):** git 2.43.0.
{{OUT:q06}}

**Follow-ups:**
- *Reflog in a fresh clone?* Empty; recovery only works where the work happened.
- *Dropped stash?* `git fsck --unreachable` can find it; not guaranteed.
- *How do you avoid this?* Make a safety branch (`git branch backup`) before any `reset --hard` or rebase.

**Common mistakes:**
- Running `git gc --prune=now` before checking the reflog.
- Believing untracked files can be recovered by git (never added means never stored).
- Resetting `main` to the rescued hash without first checking `git log` on it.
'''

B[7] = r'''**Say this first (1 line):** Notebooks are JSON with outputs and counters, so I strip outputs before commit (nbstripout), review a paired `.py` (jupytext), and keep real logic in modules, not in notebooks.

**Then explain:**
- **Why diffs explode:** execution counts, embedded images (base64) and outputs change on every re-run, even with no code change. Two people editing means conflicts in JSON that no human wants to resolve.
- **nbstripout:** removes outputs and counts. `nbstripout --install` sets a Git filter in this clone (the `.git/config` part is per clone, so also add it to onboarding or a pre-commit hook; the pre-commit hook needs hook repos from the network, so it was not run here).
- **jupytext:** pairs `eda.ipynb` with `eda.py` in percent format; reviewers read the `.py`, and a conflict in a `.py` file is a normal text conflict.
- **When a notebook should not be in the repo:** throwaway exploration, anything with PII or real customer rows in the outputs, and anything the pipeline depends on (move the code to a module with tests and call it from the notebook).
- Trade-off: stripped notebooks lose the plots. For a report that must show results, commit rendered HTML or outputs deliberately, or publish from CI.
- Failure mode: a hook that is not installed on a teammate's machine, so outputs sneak back in. Add a CI check that fails if a committed notebook has outputs.

**Example:** I committed a notebook with two cells and a fake 13 KB image. A teammate re-ran it with no code change. Plain Git: 40 diff lines, about 28 KB. After stripping both versions: the diff is empty, and the file shrinks from about 14.5 KB to 0.6 KB. The sizes come from this synthetic notebook, not a real project.

**Code:** the script builds a notebook with Python, diffs raw vs stripped, installs the filter, and pairs with jupytext.
{{SH:q07_notebooks.sh}}

**Output (my run):** nbstripout 0.9.1, jupytext 1.19.6, git 2.43.0. `git status` at the end is noisy because the demo keeps helper files in the repo.
{{OUT:q07}}

**Follow-ups:**
- *Why not `.ipynb` diff tools only?* They help reading but do not fix merge conflicts or repo bloat.
- *Reproducibility without outputs?* Re-run in CI (for example with papermill or nbconvert) and publish artefacts.
- *Does jupytext lose outputs?* The `.py` has none; the `.ipynb` keeps them locally.

**Common mistakes:**
- Stripping outputs but still committing notebooks with secrets in code cells.
- Installing nbstripout only on one laptop.
- Keeping training code only in a notebook.
'''

B[8] = r'''**Say this first (1 line):** I test `impute_and_scale` with hand-computed numbers plus one test per edge case, and I decide up front what each edge case does: raise on all-NaN and constant columns, return an empty frame for no rows, never mutate the input.

**Then explain:**
- **Known values:** `[1, NaN, 3]`: median 2, so `[1, 2, 3]`, mean 2, population std `sqrt(2/3)`, result `[-1.2247, 0, 1.2247]`. Check by hand, not by copying the function's output.
- **All-NaN column:** no median exists. Raise `ValueError`; silently returning NaN hides a broken upstream feed.
- **Constant column:** std is 0, so dividing gives NaN or inf. Raise (a team could instead return zeros; the point is to choose and test it). Also a column that becomes constant after imputing.
- **Empty DataFrame:** nothing to learn from; return an empty float frame so pipelines do not crash on a quiet day. State it in the docstring.
- **No mutation and dtype:** `df.copy()` first; test with `assert_frame_equal` against a deep copy. Integers come back as `float64`.
- A test that fails on a sample-std bug proves the tests are doing work (see output).

**Example:** For `a = [1, NaN, 3]` the test expects `[-1/s, 0, 1/s]` with `s = sqrt(2/3)`. A version using sample std (`ddof=1`) gives about `±1.0` instead and fails.

**Code:** one file shown here for reading; in the repo it is `prep.py` and `test_prep.py`.
{{PY:q08/prep.py,q08/test_prep.py}}
{{SH:q08_run.sh}}

**Output (my run):** pytest 9.1.1, pandas 3.0.5, numpy 2.5.3, Python 3.13.17 (`python3 -I -m pytest`). Second run is the same code with the sample-std bug injected.
{{OUT:q08}}

**Follow-ups:**
- *Why `approx` and `assert_allclose`?* Floats; exact equality breaks on rounding.
- *How would you add property tests?* Hypothesis: for any non-constant numeric column, output mean is about 0 and std about 1.
- *Why not raise on empty?* A design choice; either is fine if it is documented and tested.

**Common mistakes:**
- Expected values copied from the function's own output.
- Testing only the happy path.
- Forgetting that imputing can create a constant column.
- Mutating the caller's frame (the SettingWithCopy family of bugs).
'''

B[9] = r'''**Say this first (1 line):** Four layers: unit tests for small functions, data tests for schema and ranges, model tests for behaviour after a fit, and integration tests for the whole path; fast layers on every PR, slower ones nightly or before release, because ML fails silently when data changes.

**Then explain:**
- **Unit (every PR):** one function, hand-checkable. Churn: a ratio feature does not divide by zero tenure.
- **Data (every PR on a small sample, and on every new data drop):** schema, nulls, ranges, label balance, units. Churn: `monthly_spend` stays in a plausible band.
- **Model (nightly, or on PR if cheap):** needs a fit. Churn: AUC beats a floor the team chose; more support calls never lowers the churn score; same seed gives the same predictions.
- **Integration (nightly / before release):** raw data to saved model to loaded model to prediction for new rows; later also the serving API and a canary comparison.
- **Rough budgets (team choices, not rules):** unit and data seconds to about a minute per PR; model tests a few minutes; integration up to tens of minutes. Keep PR checks short or people stop waiting for them.
- **Why normal tests are not enough:** a unit test of code passes while the data changes underneath. In my run, monthly spend scaled by 100 raised no exception; only the data tests failed.

**Example:** The unit test of the ratio function still passed after I multiplied spend by 100. The data layer caught the shift, and also showed the label becoming all ones (churn rate 1.0), a second signal that something was off.

**Code:** tests are tagged with markers. Files: `churn.py`, `conftest.py`, `test_pyramid.py`, `q09_run.sh` (shown joined).
{{PY:q09/churn.py,q09/conftest.py,q09/test_pyramid.py}}
{{SH:q09_run.sh}}

**Output (my run):** pytest 9.1.1, scikit-learn 1.9.1, Python 3.13.17. Timings are from this sandbox, only to show the layers differ in cost.
{{OUT:q09}}

**Follow-ups:**
- *What else belongs in a data test?* Freshness, row counts, category sets, null rate per column (tools like pandera or Great Expectations; not run here).
- *How do you stop flaky model tests?* Fixed seeds, fixed data slice, thresholds with margin.
- *Which tests gate release?* Model tests against a held-out set and against the current production model.

**Common mistakes:**
- One huge suite that runs 40 minutes on every PR.
- AUC threshold copied from one lucky run.
- No data tests, only code tests.
- Tests that need production data or the network.
'''

B[10] = r'''**Say this first (1 line):** Put the code under `src/<name>/`, describe it in `pyproject.toml`, install it with `pip install -e .` while developing, and build a wheel (`python -m build`) that I install into a clean venv to prove it works without my source folder.

**Then explain:**
- **Why not `sys.path` hacks:** they depend on where you run from, break in CI and notebooks, and hide missing dependencies. A package works from anywhere once installed.
- **src layout:** code in `src/churnkit/`, tests in `tests/`. With `src/` you cannot import the package by accident from the current folder, so tests exercise the installed code (a common packaging recommendation).
- **Editable install (`pip install -e .`):** links the environment to the source folder, so edits show up with no reinstall. Changes to `pyproject.toml` itself (new dependencies, entry points) need a reinstall.
- **Wheel vs sdist:** the wheel (`.whl`) is a ready-to-unpack built package; the sdist (`.tar.gz`) is the source archive plus metadata that a tool must build. In my run the wheel held only `churnkit/` and metadata; the sdist also held `src/`, `tests/` and `pyproject.toml`.
- **Clean-venv test:** install only the wheel in a new venv and run from another folder; this finds missing files or undeclared dependencies.
- Failure mode: a dependency imported in code but missing from `dependencies` works on your laptop and fails in the clean venv.

**Example:** `utils/features.py` becomes `src/churnkit/features.py`. Everyone does `from churnkit import add_ratio`. After editing the clip value in the source, the editable venv reflected it at once.

**Code:** `pyproject.toml` (also written by the script), then the full demo.
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "churnkit"
version = "0.1.0"
description = "Shared feature helpers for the churn team"
requires-python = ">=3.10"
dependencies = ["pandas>=2.0"]

[project.optional-dependencies]
dev = ["pytest"]

[tool.hatch.build.targets.wheel]
packages = ["src/churnkit"]
```
{{SH:q10_packaging.sh}}

**Output (my run):** Python 3.13.17, build 1.6.1, hatchling pulled by the isolated build from the package index (the sandbox proxy allowed it); pandas 3.1.0 resolved from the index at run time. Nothing was uploaded; `twine` was not run.
{{OUT:q10}}

**Follow-ups:**
- *Where does it get published?* A private index or an internal artifact repo, with CI building the wheel on a tag (hosted-index details vary; check your platform's docs).
- *setuptools or hatchling?* Either works with `pyproject.toml`; pick one and keep the config in that file.
- *How do you pin versions for reproducible training?* The package declares ranges; the application keeps a lockfile.

**Common mistakes:**
- Testing from the repo root, where the source folder hides a broken install.
- Forgetting `__init__.py` or listing the wrong package path (empty wheel).
- Pinning exact versions in a library (it makes installs conflict for users).
- Using `python setup.py install` in new code.
'''
