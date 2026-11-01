from build_b import *

A[36] = f"""**Say this first (1 line):** Do not fail on the raw number; fail when a paired bootstrap says the drop is plausibly bigger than the allowed margin, warn when it is inside noise, and keep a logged override for humans.

**Then explain:**
- A 0.005 AUC drop on 5,000 rows may be noise. Both models score the same rows, so compare them as a pair: resample rows with replacement, compute AUC of both models on the SAME resample, take the difference, repeat 2,000 times, read the 95 percent interval.
- Pairing matters: the two scores share row difficulty, so the difference has much less noise than two separate AUCs. How much it helps depends on how correlated the models are (here 0.86 for the small case, 0.97 for the big one).
- Decision rule I would write down: PASS if the interval lower end is above minus margin; FAIL if the whole interval is below zero and the lower end is past the margin; otherwise WARN (a human decides). The margin (here 0.01 AUC) is a business decision stored in the baseline file.
- Baseline file in git (`baseline.json`: metric, value, row count, margin, data version). It only changes through a reviewed PR, so a gate cannot be quietly loosened. Use a fixed validation set and fixed seed for the bootstrap.
- Slice checks: run the same comparison per important slice (new vs old customers, region). A flat overall AUC can hide a slice that got worse; use a looser or count-aware rule on small slices.
- Override: a label or a PR comment with a reason, a named approver, and a ticket, logged in CI. Never an edit of the threshold in the same PR.
- Failure modes: peeking at the same validation set so often that it is overfit; a baseline that is itself stale; many slices giving false alarms (multiple comparisons).

**Example:** In the run, the candidate AUC is 0.869 versus 0.874: delta minus 0.005, interval minus 0.0124 to plus 0.0026, which includes 0. We cannot call it a regression, but it might exceed 0.01, so WARN. A real degradation to 0.845 has an interval of minus 0.033 to minus 0.025, entirely below zero and past the margin: FAIL.

**Code:**
{block("python", "q36/gate.py")}

**Output (my run):** ({ENV}; seed 36, 2000 resamples). The data is synthetic.
{out("q36/out.txt")}

**Follow-ups:**
- *Why not a DeLong test?* It is a valid analytic alternative for paired AUCs; the bootstrap also works for any metric and is easy to explain.
- *What if the metric is not AUC?* The same loop works for F1 or log loss; for rare positives use stratified resampling.
- *Is 0.005 ever worth blocking?* If the model's profit or risk is very sensitive to it, set a tighter margin and a bigger validation set; the margin comes from the business cost, not from the stats.

**Common mistakes:**
- Failing the build on any drop (noise causes constant red) or passing anything within a loose fixed margin (a slow decline gets through).
- Bootstrapping the two models on different resamples (loses the pairing).
- Letting the threshold be edited in the same PR as the model change.
- Ignoring slices.
"""

A[37] = f"""**Say this first (1 line):** A pure-Python wheel (`py3-none-any`) works anywhere; a platform wheel contains compiled code and is tagged for an OS and CPU; heavy or optional dependencies go in extras (`pkg[gpu]`) so a small utility does not drag in torch.

**Then explain:**
- Wheel tag format: name-version-python tag-ABI tag-platform tag. `py3-none-any` means no compiled code, any OS. A compiled wheel looks like `cp313-cp313-manylinux_x_y_x86_64`: the `manylinux` tag says it was built to run on most Linux distributions with a baseline glibc (check the current manylinux policy for the exact versions).
- A source distribution (sdist) is the source; installing it runs the build on the user's machine, so it needs a compiler for C extensions. Wheels install with no build.
- Extras: `[project.optional-dependencies] gpu = ["torch>=2.1"]`. `pip install mlutil` stays light; `pip install "mlutil[gpu]"` adds torch. Import the heavy module lazily and raise a clear error that names the extra.
- Why not put torch or CUDA in the core `dependencies`: it forces a huge download and a specific build on everyone (CPU-only users, edge devices), and the right torch build depends on the CUDA and index setup, which a utility library should not decide. Also it makes version conflicts with the user's own torch likely.
- Inspect a built wheel: it is a zip. List the files, read `METADATA` for `Requires-Dist` (with `extra == 'gpu'` markers) and `Provides-Extra`, read `WHEEL` for the tag.
- Failure modes: forgetting that extras are not installed in CI (the GPU path is untested), extras names with typos silently ignored by pip (it warns), and tests that import the optional module at top level.

**Example:** `mlutil` 0.3.0 has `numpy>=1.24` as core and `torch>=2.1` under `gpu`. The built wheel is `mlutil-0.3.0-py3-none-any.whl`; installing it in a clean venv and calling `mlutil.gpu` without torch gives the friendly error that tells you to install `mlutil[gpu]`.

**Code:**
{block("toml", "q37/pkg/pyproject.toml")}

{block("python", "q37/pkg/src/mlutil/__init__.py", "q37/pkg/src/mlutil/gpu.py")}

{block("bash", "q37/run.sh")}

**Output (my run):** ({ENV}). Built with `--no-isolation` using the already installed hatchling. The `[gpu]` install itself was not run (it would download torch); only the metadata and the error message were checked.
{out("q37/out.txt")}

**Follow-ups:**
- *How do you ship a platform wheel for several OSes?* Build in CI per platform (a tool such as cibuildwheel, check current docs) and upload all wheels plus the sdist.
- *Extras versus a separate package?* If the optional part is big or has its own release cycle, a separate package (`mlutil-gpu`) is cleaner.
- *Should `torch` be a dev dependency?* Put it in the `dev` or `test` extra for CI jobs that need it.

**Common mistakes:**
- Listing torch in core dependencies of a small library.
- Importing the optional module at the top of `__init__.py`.
- Not testing the install without the extra.
- Calling a wheel with C code "pure" and uploading only one platform.
"""

A[38] = f"""**Say this first (1 line):** For 30 people use a private package index with versioned releases (it gives auth, yanking and a normal `pip install`); a git URL with a tag is a good small-team shortcut; a shared mounted directory is the weakest option.

**Then explain:**
| Option | Auth | Versioning | Good for | Weak point |
|---|---|---|---|---|
| Private index (Artifact Registry, CodeArtifact, Nexus, Artifactory; check current docs) | tokens or cloud identity | real releases, ranges like `>=1.2,<2` | 30 users and many projects | someone must run it and manage tokens |
| `pip install "lib @ git+https://host/org/lib.git@v1.2.0"` | the git host's SSH key or token | a tag or commit | tiny teams, quick start | builds from source each time; needs git and build tools; no yank |
| Shared directory of wheels with `--no-index --find-links` | file permissions | file names | air-gapped or very small | no history, no access control per project, stale copies |
- Authentication: never put tokens in `requirements.txt`; use keyring helpers or environment variables injected by CI, and read-only tokens for installs (check the docs of the chosen registry).
- Versioning: semantic versions, release only from tags, one changelog. Pin consumers with ranges.
- Yanking a bad release: a yanked release stays installable only if someone pins it exactly, so new resolutions skip it. Index support varies, so check your registry's docs; on a private index you can often delete it. Then ship a fixed patch version.
- Deprecation: warn first with `warnings.warn(..., DeprecationWarning, stacklevel=2)`, keep the old name for at least one minor series, then remove in the next major. Write the policy down (for example: warn for 2 minor releases or 3 months).
- Test the shim with `pytest.warns`, and check that the new API is silent.

**Example:** `build_features()` is renamed `make_features()` in 1.2.0. The old name still works but warns, with a message pointing to the new one and the version where it disappears. Users see the warning at their own call site because of `stacklevel=2`.

**Code:**
{block("toml", "q38/pkg/pyproject.toml")}

{block("python", "q38/pkg/src/teamlib/__init__.py", "q38/tests/test_shim.py")}

{block("bash", "q38/run.sh")}

Pip forms against a hosted index, shown but NOT executed here (replace names and URLs; check your registry's docs):
```text
pip install teamlib==1.2.0 --index-url https://<private-index>/simple/ --extra-index-url https://pypi.org/simple/
pip install "teamlib @ git+https://<host>/<org>/teamlib.git@v1.2.0"
pip install --no-index --find-links /mnt/shared/wheels teamlib==1.2.0
```
Note: `--extra-index-url` mixes indexes, which allows dependency confusion if an attacker publishes the same name publicly; prefer one index that mirrors public packages.

**Output (my run):** ({ENV}). Forms 1 (local git repo, tag v1.2.0) and 3 (directory of wheels) were really run; hosted index forms were not.
{out("q38/out.txt")}

**Follow-ups:**
- *What is dependency confusion?* Pip picks the highest version across all indexes, so an attacker can publish your internal package name publicly with a higher number. Use a single index, or pin hashes.
- *How long do you keep deprecated names?* Write a policy; my default is at least one minor release and a few weeks, longer when many teams use it.
- *Who tests that consumers still work?* The library's CI runs a few consumer test suites against each release candidate.

**Common mistakes:**
- Tokens in committed requirements files.
- Installing from `main` instead of a tag.
- Deprecating with a `print` or a silent change instead of a warning.
- Forgetting `stacklevel=2`, so the warning points inside the library.
"""

A[39] = f"""**Say this first (1 line):** The paper's point is that the model code is a small part of an ML system and the real debt lives around it: glue code, pipeline jungles, dead experimental paths and configuration, plus undeclared consumers; I pay it down by writing characterisation tests first and then refactoring in small steps.

**Then explain:**
| Debt (Sculley et al., from memory, check the paper for wording) | Code smell in a 20-module repo | What it costs |
|---|---|---|
| Glue code | a module whose only job is converting between two libraries' data types (numpy to pandas to a tool format and back) | every library change touches glue; hard to swap tools |
| Pipeline jungle | `step2_clean_v2.py`, `step3_clean_final.py`, `step4_clean_final2.py`: scripts chained by file names and order, nobody knows which are live | one change breaks a step three files later; no one dares to touch it |
| Dead experimental code paths | a constant flag like `USE_OLD_FEATURES = False` guarding a branch nobody has run for a year | every new change must work around code that never runs |
| Configuration debt | keys in `config.json` that no code reads, and keys read but never documented | wrong runs, hidden defaults, fear of deleting anything |
| Undeclared consumers (related) | other jobs reading your output table or model file with no contract | a harmless change breaks someone you did not know about |
- Detecting is mostly mechanical: the demo below finds all four planted smells with about 40 lines of `ast` and regular expressions. Counting them each sprint gives a trend.
- Plan, 3 sprints, to pay one down (the pipeline jungle): Sprint 1, characterisation tests: run the current pipeline on a frozen sample and store the output as golden files; add a smoke test that runs end to end. Sprint 2, turn the step scripts into named functions with one entry point and a config object, keep outputs identical to the golden files. Sprint 3, delete the dead scripts and flags, write down inputs and outputs per step, add a data contract check on the final table.
- I would refuse to refactor without tests: feature engineering code, anything that writes the table or model other systems read, scaling and encoding, and any rewrite of the training-serving shared code. If the behaviour is not pinned, "cleaner" can silently change predictions.
- Failure modes: a big-bang rewrite, refactoring and changing behaviour in one PR, and golden files that nobody reviews.

**Example:** The detector prints four lines for the toy repo: glue in `glue.py`, 4 jungle-named step files, the dead flag in `features.py`, and 3 unread config keys (`dropout`, `legacy_mode`, `tmp_fix_2022`). Then a characterisation test pins the output of a tangled function (`[3.0, 5.0, 0, -2]`) before anyone edits it.

**Code:**
{block("python", "q39/smells.py", "q39/characterize.py")}

**Output (my run):** ({ENV}). The toy repo is generated by the script in a temp folder.
{out("q39/out.txt")}

**Follow-ups:**
- *Which debt hurts most first?* The one that blocks releases or hides wrong results: undeclared consumers and untested feature code.
- *How do you find undeclared consumers?* Access logs on the table or file, a registry of consumers, and breaking changes announced with a deprecation window.
- *Is deleting dead code safe?* With tests green and version control behind you, yes; delete in its own commit so it can be reverted.

**Common mistakes:**
- Refactoring without a safety net.
- Treating technical debt as a one-off clean-up week instead of a tracked backlog.
- Quoting the paper from memory as if word for word; paraphrase and name the paper.
- Deleting a config key without checking who reads it.
"""

A[40] = f"""**Say this first (1 line):** I treat LLM-written code as an untrusted PR from a stranger: I do not accept the metric, I check where the data is split, where fitting happens, what the seed is, whether errors can be swallowed, and whether every imported API and argument really exists in the version we pin.

**Then explain:**
- Leakage: anything fitted (scaler, imputer, feature selector, encoder) must be fitted on training rows only, inside a Pipeline, after the split. Quick test: shuffle the labels or use pure noise; an honest pipeline scores about 0.5.
- Seeds: `train_test_split` without `random_state` gives a different split every run, so results cannot be reproduced or compared. Two runs of the same code must give the same number.
- Metric on the right split: check which array goes to `.score()` or the metric function (train versus test), and which metric is right for the problem (accuracy on imbalanced data is a trap).
- Silent failure: a bare `except Exception: pass` means a failed save or a failed feature step looks like success. Catch specific exceptions or let it raise.
- Invented APIs: LLMs sometimes make up parameters or functions (for example a plural `class_weights`). Check with `inspect.signature` or the docs of the pinned version; in many cases the call just raises `TypeError`, but some wrappers swallow unknown keywords.
- Unpinned imports: confirm every import is in the lockfile with a version, and that there is no import of an unfamiliar package with a similar name to a real one (typosquatting risk).
- Also: the code runs and prints a pleasing number is the weakest evidence there is. Ask for tests, not a screenshot.

**Example:** The 30-line function below looks fine and reports an accuracy of 0.93 on data where the labels are coin flips (the real score is about 0.5). Three planted problems: feature selection fitted on all rows (leakage), no seed in the split, and a swallowed `joblib.dump` error. Three tests catch them (all fail on the pasted code, all pass on the fixed one). A fourth test shows the invented-parameter check: it reads the real signature of the installed library and passes on both versions, because this code has no invented argument.

**Code:**
{block("python", "q40/llm_train.py", "q40/test_review.py", "q40/fixed/llm_train.py")}

**Output (my run):** ({ENV}). The pasted function was run directly, then `pytest` against it, then against the fixed version in `q40/fixed/` (selector inside a Pipeline after a seeded split, no try/except). The reported accuracy changes on every run of the buggy version because it is unseeded (0.70 and 0.73 in two earlier runs, 0.93 in the pasted one).
{out("q40/out.txt")}

**Follow-ups:**
- *Would you ban AI-generated code?* No. I would require the same bar as any code: tests, review, pinned deps, and the author must be able to explain every line.
- *How do you catch invented packages?* Install from the lockfile in CI only, and have a review rule that new dependencies need a justification and a check on the package index page.
- *Is the leakage here that bad with real data?* It depends; with many features and few rows (as here) it is severe, and with large data it is smaller but still wrong.

**Common mistakes:**
- Trusting the printed metric.
- Reviewing only style, not data flow.
- Asking the LLM to confirm its own code is correct.
- Running the code once and calling it verified.
"""
