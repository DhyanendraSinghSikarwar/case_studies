Q = {}
NE = "Not executed here: a real GitHub runner, so none of these workflows ran on GitHub. "

Q[1] = dict(
code=[("yaml", ["q01_stage_map.yml"]), ("python", ["q01_order.py"]), ("shell", ["cmds.sh"])],
say="CI tests every change to code, data and pipeline, CD ships a tested model and its serving image behind a gate, and CT retrains on a trigger; the ML twist is that a model can change with no code change, and a data change can break a green build.",
explain="""
- **CI (continuous integration):** on every pull request, check the things you own: code (lint, unit tests), data (schema, nulls, ranges on a sample), the pipeline (a tiny smoke train that runs end to end). Fast, cheap, blocks the merge.
- **CD (continuous delivery or deployment):** take a model that passed evaluation and move it toward users: register it, pass the gate, deploy the serving image or move a pointer. Delivery means a human approves the last step. Deployment means no human.
- **CT (continuous training):** the extra ML loop. Retrain on a schedule, on new data, or on a drift alert, then evaluate, register, gate. It runs with no commit at all.
- **Why ML differs:** three things change, not one: code, data and model. Same commit plus new data gives a different model. A bad upstream column breaks the model while every unit test is still green. So CI needs data tests, and CD needs a metric gate, not only "tests pass".
- **What ships:** CI ships nothing, it gives a yes or no. CD ships a model artifact plus a serving image. CT ships a new model version into the registry.
- **Hand-off:** Part 5 (orchestration) takes over the scheduled, long, multi-step training run (the `full-train` to `register` stages). Part 8 (monitoring) takes over after `deploy`: the monitor stage is not a CI job, it watches live traffic and fires CT.
- **Failure modes:** green CI with silently shifted data; a retrain that is worse than the champion but gets deployed because nothing compared them; training and serving use different preprocessing.
""",
example="""A churn model repo. A developer edits a feature function: CI runs lint, unit and data tests, then a smoke train, and blocks the PR if any fail. Two weeks later, with no commit, the nightly CT job retrains on fresh data, evaluates, registers version 7 and runs the gate. The gate fails (AUC dropped 0.02 against the champion), so nothing is deployed. The stage map below puts both loops on one needs graph; `lint` is the only root and `deploy` the only leaf, and `unit` and `data-tests` can run in parallel.""",
outnote=NE + "The validation that did run is below: PyYAML parsed the file (note the top-level key `on` shows up as `True`, see Q2), `graphlib` ordered the `needs` graph, and actionlint accepted it (exit 0). The `monitor` stage is deliberately not in the YAML: it is not a CI job (Part 8).",
follow="""
- *Is CT the same as a nightly CI run?* No. A nightly CI re-runs tests on the same code. CT produces a new model from new data and ends in the registry.
- *Where does CT start?* On a time trigger, a data-arrival trigger or a drift alert (Part 8). Pick the simplest one that fits how fast your data goes stale.
- *Do you need all stages from day one?* No. Start with lint, unit, smoke train and a gate; add the rest as pain shows up.
""",
mistakes="""
- Saying CI/CD for ML is "just DevOps". The data and model axes are the whole point.
- Testing code only, with no data tests, so a schema change goes to production.
- Full training on every PR. That is slow and costly; use a smoke train on PRs and full training on schedule.
- Confusing delivery (human approves) with deployment (automatic).
- Claiming a maturity "level number" for CT. Sources disagree on numbering; just say what each stage does.
""")

Q[2] = dict(
code=[("yaml", ["q02_good.yml", "q02_bad.yml"]), ("python", ["q02_on_trap.py"]), ("shell", ["cmds.sh"])],
say="A workflow is a YAML file in `.github/workflows/` with a trigger (`on`), one or more `jobs` that each pick a runner (`runs-on`) and run `steps`, where a step either calls an action (`uses`) or runs a shell command (`run`); you can lint it offline with actionlint and check-jsonschema.",
explain="""
- **Where:** `.github/workflows/*.yml` on the default branch of the repo. One file, one workflow.
- **`on`:** what starts it (`pull_request`, `schedule`, ...; Q4). **`jobs`:** a map of jobs. Jobs run in parallel unless one has **`needs`** pointing at another.
- **`runs-on`:** the runner label (`ubuntu-latest`, or a self-hosted label). **`steps`:** run in order on the same machine. A **step** is `uses: owner/action@ref` (reuse) or `run:` (a shell command). **`with`** passes inputs to an action, **`env`** sets environment variables.
- **`permissions`:** what the `GITHUB_TOKEN` may do. Set `contents: read` at the top and widen per job only.
- **`matrix`:** one job definition fanned out over values (here Python 3.11 and 3.12). `fail-fast: false` lets the other cells finish when one fails.
- **YAML 1.1 trap:** PyYAML reads the bare key `on` as the boolean `True`, so `wf["on"]` raises KeyError or `.get("on")` is `None`. GitHub itself handles it fine. Fix in your own tooling: look up `True` as well, or use a parser with YAML 1.2 rules.
- **Limit of linting:** actionlint and the schema check syntax and expressions. They cannot tell you the job will pass on a real runner, or that a secret exists.
""",
example="""Good file: a PR triggers `test`, which runs on two Python versions, restores the pip cache keyed on `requirements.txt`, runs `ruff` then `pytest`. Bad file: three planted mistakes. `pull_requests` (extra s) is not an event, `needs: tests` points at a job called `test`, and the PR title is pasted straight into a `run` script, which lets a PR author inject shell commands. actionlint reports all three; the schema check reports the event only (it checks structure, not expression safety or job names).""",
outnote=NE + "Everything below really ran offline: actionlint 1.7.12 (from actionlint-py), check-jsonschema 0.38.2 with the built-in `vendor.github-workflows` schema, and PyYAML 6.0.3.",
follow="""
- *`uses` or `run`?* `uses` for a maintained action (checkout, setup-python); `run` for your own commands. Pin third-party actions to a full commit SHA (Q5).
- *Does actionlint check OIDC permissions?* No. In my testing it does not flag a missing `id-token: write`; test that on a real run (Q6).
- *Can I run it locally?* `act` is a separate tool and was not available here, so I only linted.
""",
mistakes="""
- Putting the file anywhere except `.github/workflows/`; it will not run.
- Forgetting `needs`, then wondering why jobs run in parallel and one reads an artifact the other has not made yet.
- Reading workflow YAML in Python with `wf["on"]` and getting a KeyError.
- Treating a green `check-jsonschema` as proof the workflow is safe or correct.
- Leaving `permissions` unset, so the token gets the repo default, which may be broader than needed (check current docs for the default).
""")

Q[3] = dict(
code=[("python", ["train_lib.py", "test_train.py"]), ("ini", ["pytest.ini"]), ("yaml", ["ci.yml"]), ("shell", ["cmds.sh"])],
say="Run a fast pyramid on every PR (lint, unit, data tests on a sample, a one-minute smoke train) and push the full training and quality checks to a nightly job, using a pytest marker to split them.",
explain="""
- **The pyramid, cheapest first:** lint and types, unit tests on tiny arrays, data tests on a sample (schema, nulls, ranges), training smoke test, nightly full training. Each layer catches a different bug; run the cheap ones first so a typo fails in seconds.
- **Smoke test:** a few hundred rows, two epochs. Assert: loss is finite, loss goes down, the artifact is written, the artifact reloads and predicts. It proves the pipeline wires together, not that the model is good. Aim for about a minute or two.
- **Fails the PR:** lint, unit, data schema, smoke test. **Only warns or alerts:** slow quality checks on the full dataset, soft metric drift, a flaky external dependency. Decide this once, write it down.
- **Time budget:** PR checks should finish in minutes, or people stop waiting and merge anyway. Full training goes on `schedule` with a long `timeout-minutes`.
- **Failure modes:** a smoke test that checks nothing (only "it ran"); a full test marked `slow` that nobody reads when it fails; test data that is so clean the data tests never fail; an unseeded run that makes "loss falls" flaky.
- Part 1 owns pytest and pre-commit basics; this answer is only the smoke test and the PR versus nightly split.
""",
example="""A fixture builds 300 synthetic rows. `SGDClassifier` trains for 2 `partial_fit` epochs; the log loss after epoch 1 must be higher than after epoch 2, and the saved joblib file must reload and predict 5 rows. The nightly test trains on 20,000 rows for 50 epochs and requires accuracy above 0.75 (a threshold I chose for this synthetic data, not a benchmark). `pytest -m "not slow"` runs the first only; `pytest -m slow` the second.""",
outnote=NE + "The tests and the marker split below really ran with scikit-learn 1.9.1 and pytest 9.1.1; the workflow was only linted (actionlint and check-jsonschema). Timings are sandbox-only.",
follow="""
- *Why a marker and not two folders?* Either works. A marker keeps the tests next to the code; register it in `pytest.ini` so a typo in the marker name is caught with `--strict-markers`.
- *How do you stop flakiness?* Seed everything and assert on a direction (loss falls), not an exact number.
- *Nightly fails, what then?* It alerts the team and opens a ticket; it does not block unrelated PRs.
""",
mistakes="""
- Running the full training on every PR.
- A smoke test with no artifact reload step, so a broken save/load ships.
- Exact-number assertions on loss, which break on a library upgrade.
- Unregistered markers: pytest only warns by default, and `-m "not slow"` still runs a mistyped one.
- Letting the nightly job fail for weeks with nobody owning it.
""")

Q[4] = dict(
code=[("yaml", ["ci.yml", "train.yml", "after_ci.yml", "risky_target.yml", "bad_triggers.yml"]), ("shell", ["cmds.sh"])],
say="Use `pull_request` with `paths` for code CI, `schedule` for nightly training, `workflow_dispatch` for the manual button and `repository_dispatch` for new data; avoid `pull_request_target` with fork code.",
explain="""
- **`push` / `pull_request`:** the code CI triggers. `branches` filters by branch, `paths` by changed files, so a docs edit does not train a model. If a required check is skipped by a `paths` filter, check current docs for how branch protection treats it.
- **`schedule`:** cron, in **UTC**, and only runs from the **default branch**. On an inactive repository GitHub may disable scheduled workflows after a period of no activity (check current docs), so a "nightly" job can silently stop.
- **`workflow_dispatch`:** a manual button with typed `inputs` (string, boolean, choice). **`repository_dispatch`:** an API call from outside (a data pipeline says "new data landed") with a `client_payload`. **`workflow_run`:** start after another workflow finishes. **`release`:** on publish. **`workflow_call`:** makes the workflow callable from other workflows (reusable workflows).
- **`pull_request` vs `pull_request_target`:** the first runs the merge result with a read-only token and no secrets for fork PRs. The second runs in the context of the **base** repo, with secrets and a write-capable token. If it checks out and runs the fork's code, an outsider runs code with your secrets. Use it only for things like labelling, and never run untrusted code in it.
- **Failure modes:** `branch:` instead of `branches:`, a bad cron, a boolean input with a string default, a `schedule` that never runs because the file is not on the default branch.
""",
example="""Repo needs: (1) code CI on every PR touching code: `ci.yml` (`pull_request`, `paths`). (2) Nightly training at 20:30 UTC (02:00 IST): `schedule` in `train.yml`. (3) A "retrain now" button: `workflow_dispatch` with `data_version` and `full` inputs. (4) Retrain when new data lands: the data job calls `repository_dispatch` with type `new-data`. All three training triggers share one `train.yml`, which can also be called by other workflows via `workflow_call`. `after_ci.yml` shows `workflow_run` and `release`. `risky_target.yml` is the pattern to avoid: lint accepts it.""",
outnote=NE + "Real runs below: actionlint and check-jsonschema on all five files. Four are clean; the broken one (wrong key `branch`, cron `61 25 * * *`, a boolean input with default `yes`) is rejected by both. Note that `risky_target.yml` passes both checkers: they do not detect the unsafe checkout, so review that by reading.",
follow="""
- *IST night run?* Cron has no time zone; convert (IST is UTC+5:30).
- *Can I trigger one workflow from another?* `workflow_run`, `workflow_call` or `repository_dispatch`. `workflow_call` is the clearest.
- *Why does GITHUB_TOKEN not trigger new runs?* Events created with the default token generally do not start new workflow runs (check current docs); use a GitHub App or PAT if you need chaining.
""",
mistakes="""
- Expecting `schedule` to run from a feature branch.
- Using `pull_request_target` to "get secrets in fork PR tests" and then running the fork's code.
- Treating cron time as local time.
- No `paths` filter, so a README edit burns CI minutes.
- Passing a boolean input and comparing it as a string (`inputs.full == 'true'` versus `inputs.full`).
""")

Q[5] = dict(
code=[("yaml", ["unsafe.yml", "safe.yml"]), ("python", ["mask_demo.py"]), ("shell", ["cmds.sh", "inject_demo.sh"])],
say="Keep secrets in the secret store, pass them to a step through `env` (never pasted into a script or a log), give the token the least permission, and treat any text from a PR as hostile input.",
explain="""
- **Scopes:** repository, environment and organisation **secrets** (encrypted, masked in logs) versus **variables** (plain text, for non-sensitive config such as a region or model name). Environment secrets only load after the environment's protection rules pass (Q7).
- **Forks:** secrets are not passed to workflows triggered by fork pull requests (except via risky triggers, Q4), and the token there is read-only.
- **Masking is exact-string match:** a secret that is base64-encoded, transformed or split across lines is not masked (see the demo). Masking is a safety net, not a plan. Do not `echo` secrets or use `set -x` around them.
- **`GITHUB_TOKEN`:** a short-lived, per-run token. Set `permissions: contents: read` at the top and add `id-token: write`, `pull-requests: write` only on the job that needs it.
- **Script injection:** `${{ github.event.pull_request.title }}` is replaced by text **before** the shell runs. A title with `"; curl ... ;` becomes code. Fix: put the value in `env:` and use `"$PR_TITLE"` in the script. Branch names (`github.head_ref`), issue titles and commit messages are attacker-controlled too.
- **After a leak:** rotate the secret first. Deleting the log or the run does not un-leak it, because copies and caches exist. Then find the cause and review what the credential could access.
- **Supply chain:** the March 2025 `tj-actions/changed-files` incident (CVE-2025-30066, from security vendor write-ups; I did not open them) involved tags being re-pointed to malicious code. Pin third-party actions to a full commit SHA, not a tag.
""",
example="""A PR titled `x"; echo INJECTED; "` hits the unsafe workflow. The runner builds the script text `echo "PR title is x"; echo INJECTED; ""`, so the second `echo` is a command. In the safe version the title only ever lives in `$PR_TITLE`, so it is printed as plain text. The demo script reproduces exactly this with a harmless `echo` (no real secrets anywhere).""",
outnote=NE + "Real runs below: actionlint flags two untrusted expressions in the unsafe file and passes the safe file; the shell demo shows the injection; the Python demo shows masking missing base64 and split secrets. actionlint did not flag `${{ secrets.REGISTRY_TOKEN }}` pasted into the `run` line (line 10), so it does not replace review. The secret in the demo is a made-up string.",
follow="""
- *Where do Docker build secrets go?* Part 2 owns that (build secrets, not `ARG`).
- *Secrets or OIDC?* Prefer OIDC for cloud access (Q6): there is no long-lived key to leak.
- *Self-hosted runners and secrets?* A job on a shared runner can leave files behind; use ephemeral runners that are thrown away after one job.
""",
mistakes="""
- Inlining `${{ secrets.X }}` in `run:`; it can land in the process list or logs.
- Believing masking protects encoded or partial secrets.
- Deleting the workflow run log after a leak and not rotating.
- Using tags (`@v3`) for third-party actions and trusting them forever.
- Default-wide token permissions on every workflow.
""")

Q[6] = dict(
code=[("yaml", ["deploy.yml"]), ("json", ["trust_policy.json"]), ("python", ["sub_matcher.py"]), ("shell", ["cmds.sh"])],
say="With OIDC the job asks GitHub for a short-lived signed token, the cloud checks its claims against a trust policy and hands back short-lived credentials, so there is no stored cloud key; the trust policy must pin `sub` or any repo could assume your role.",
explain="""
- **Flow:** (1) job has `permissions: id-token: write`; (2) the action requests a JWT from GitHub's OIDC provider; (3) it calls the cloud's token service (on AWS, `AssumeRoleWithWebIdentity`) with that JWT; (4) the cloud verifies the signature and claims against the trust policy; (5) it returns credentials that expire. `id-token: write` only lets the job fetch a token. It grants no cloud access by itself.
- **Claims that matter:** `iss` (GitHub's token issuer), `aud` (the audience, e.g. `sts.amazonaws.com`), `sub` (who: `repo:ORG/REPO:environment:production`, or `...:ref:refs/heads/main`, or `...:pull_request`), plus `ref`, `repository`.
- **Pin `sub`:** if the trust policy only checks `aud`, or uses `repo:*`, any repository on GitHub can get a token that satisfies it. Pin the org, repo and, best, the **environment**, because environment protection rules (Q7) then gate who can assume the role.
- **Equivalents (concept level, check current docs):** Azure uses a federated identity credential on an app registration; GCP uses workload identity federation with a provider condition on the repository claim.
- **Failure modes:** missing `id-token: write` (the action cannot get a token); `sub` pattern too wide; role policy too wide even with a good trust policy; wrong `aud`; a reusable workflow changing the `sub` you expected (check current docs).
- Part 10 owns IAM depth.
""",
example="""Trust policy pins `repo:acme/churn-model:environment:production`. The table below (from the matcher) shows who can assume the role under three policies. Only the production environment job passes the pinned policy. The repo-wide pattern lets feature branches and PR jobs in, and `repo:*` also lets another repo in.""",
outnote="Not executed: the real token exchange with GitHub and a cloud account (no cloud account, no runner). Real runs below: actionlint and check-jsonschema on the workflow, a JSON parse of the trust policy, and the Python matcher over sample claims (my own `fnmatch` imitation of StringLike wildcard matching, not the cloud's engine).",
follow="""
- *Why environment in `sub` instead of branch?* An environment can require approval, so the credential is only minted after a human says yes.
- *Is the token a secret?* It is short-lived and only useful with a matching policy, but do not log it.
- *Fork PRs?* They do not get an id-token to your cloud under normal rules; do not weaken that.
""",
mistakes="""
- Trust policy with only an `aud` condition.
- `repo:org/*` because "it is our org": any repo in it, including a throwaway one, can deploy to production.
- Forgetting `id-token: write`, then adding `write-all` to "fix" it.
- Long-lived keys kept "as a backup".
- Giving the assumed role admin rights.
""")

Q[7] = dict(
code=[("yaml", ["release.yml", "bad_env.yml"]), ("python", ["list_envs.py"]), ("shell", ["cmds.sh"])],
say="Put `environment: production` on the deploy job and configure required reviewers in the repo settings; GitHub then pauses the job for approval before it starts, and only then releases that environment's secrets.",
explain="""
- **Environment:** a named target (`staging`, `production`) with its own protection rules, secrets and variables. A job opts in with `environment:`.
- **Rules:** required reviewers, a wait timer, and a restriction on which branches may deploy. They are evaluated **before** the job starts; until they pass, the job's environment secrets are not available. Availability of rules on private repos depends on the plan (check current docs).
- **Scoped secrets:** a production credential lives only in the `production` environment, so staging jobs and PR jobs cannot read it.
- **Pipeline shape:** train, evaluate (gate), deploy-staging, deploy-production with `needs` chaining them. Use `concurrency` so two releases do not overlap.
- **What approval does not prove:** the reviewer clicked, not that the model is good. Put the gate report in the job summary (`$GITHUB_STEP_SUMMARY`) and upload it as an artifact so the reviewer sees metrics, champion versus candidate, and the data version before approving. Record who approved (the deployment history shows it).
- **Failure modes:** the self-reviewer problem (the person who triggered the run approves it; check the "prevent self-review" setting in current docs); a typo in the environment name silently creates a new, unprotected environment (check current docs); approvals that expire while a run waits.
""",
example="""Release run: `train` and `evaluate` run unattended and `evaluate` writes the gate table to the summary. `deploy-staging` runs with the staging environment. `deploy-production` waits; the reviewer reads the gate table, then approves; the job starts, gets production secrets, and moves the `champion` alias. If the reviewer rejects, the run stops and no production credential was ever exposed.""",
outnote=NE + "The approval pause itself is a GitHub server feature and was not run. Real runs below: actionlint and check-jsonschema accept the release workflow; a PyYAML script lists which jobs carry an environment; a bad `environment` block (`nme:`) is rejected by actionlint.",
follow="""
- *Staging automatically, production manually?* Yes: no reviewers on staging, reviewers on production.
- *Can the approval be bypassed?* Admins and workflow edits can change settings; limit who can edit workflows and use branch protection and code owners on `.github/workflows/` so the workflow file itself is protected.
- *Where does the alias move happen?* In the deploy step (registry, Q9, Q10), not by rebuilding the image.
""",
mistakes="""
- Approval with no evidence shown.
- Putting production secrets at repository level, so every job can read them.
- Environment name typos.
- Letting the same person trigger and approve.
- Assuming a `wait timer` is a security control; it is only a delay.
""")

Q[8] = dict(
code=[("yaml", ["cache.yml"]), ("python", ["cache_key.py"]), ("shell", ["cmds.sh"])],
say="Cache dependency downloads with a key built from the lockfile hash and a `restore-keys` fallback, and keep models and datasets out of the Actions cache.",
explain="""
- **`actions/cache`:** `path` (what to save), `key` (exact match), `restore-keys` (prefix fallbacks, restore an older cache and then save a new one under the new key). **`hashFiles('requirements.txt')`** makes the key change exactly when the file changes.
- **Easiest path:** `actions/setup-python` with `cache: pip` and `cache-dependency-path` does this for pip for you.
- **Bad keys:** a constant key (`pip-v1`) serves stale wheels forever, since a hit never re-saves. A key with the run id never hits. A good key changes with the dependency set only.
- **Scope:** as I understand it, a branch can restore caches made on itself or on its base or default branch, but not caches from unrelated sibling branches (check current docs). Repository cache storage is limited and old caches are evicted (check current docs for the size).
- **Do not cache:** models and datasets. They are large, evicted without warning, and a cache hit has no lineage. Use the model registry or a DVC remote (Part 4). Do not cache anything secret.
- **Failure modes:** a poisoned cache (anything that can write to a cache the default branch later restores can plant files, so keep untrusted code away from those caches); a cache restored on a different Python or OS version (put them in the key).
- Docker layer caching is Part 2.
""",
example="""`requirements.txt` has three pins. The key is `pip-Linux-<hash>`. Run 2 reads the same file and gets the same key: cache hit. Bump scikit-learn from 1.5.2 to 1.6.0 and the hash, so the key, changes: a miss, so pip reinstalls, then saves the new cache. `restore-keys: pip-Linux-` could restore the old cache first so only the changed wheel downloads.""",
outnote=NE + "Cache save/restore on GitHub was not run. Real runs below: actionlint and check-jsonschema on the workflow, and a Python script that mimics the hashFiles idea (sha256 per file, then sha256 of the digests). It is not guaranteed to match GitHub's hash byte for byte; the point is only that the key changes when the file changes.",
follow="""
- *Is pip's wheel cache enough?* It saves the download, not the build, so a source build is still slow. Pin wheels where you can.
- *Cache a conda env?* Possible, but key it on the lock file, and check how big it is against the limit.
- *Where do big model files go?* Registry or DVC remote, pulled by version.
""",
mistakes="""
- A constant key.
- Caching `~/.cache` wholesale, which can include tokens or huge model downloads.
- Treating the cache as storage that is always present; a miss must still work.
- Caching test data, then debugging with stale data.
- No OS or Python version in the key.
""")

Q[9] = dict(
code=[("python", ["router.py", "test_router.py"]), ("shell", ["cmds.sh"])],
say="A model release is not a code release: the model can change with no commit, the weights are separate from the serving image, and promotion should move a pointer (an alias or config value) instead of rebuilding the image.",
explain="""
- **Code CD:** commit, build, test, ship an image. The artifact is the image.
- **Model CD:** the artifact is weights plus preprocessing, stored in a registry. The serving image is built once and loads `models:/churn@champion` at start (or on reload). A new model is a new registry version and an alias change, not a new image.
- **Why pointer promotion:** it is fast, it is reversible (point the alias back), it keeps the image tested, and it leaves an audit trail of who moved it and when.
- **Three paths:** see the table in the example.
- **Change router:** a small function maps changed paths to pipelines, so a docs edit runs nothing and a training config change runs CT but not a rebuild. Unknown paths fall back to the cheap code CI (fail safe).
- **Failure modes:** the model needs a new feature column that the image's code does not know about (model and code must be compatible, so test the pair); a dependency bump changes both; an alias move with no gate.
""",
example="""
| Path | Trigger | Built | Tested | Deployed | Approver |
|---|---|---|---|---|---|
| Code-only change | PR to main | image (if serving code changed) | lint, unit, data, smoke | image, via rollout | code reviewer |
| Model-only change (new hyperparameters, config) | PR to the config, or manual dispatch | model version in registry | smoke, full train, gate | alias move, no image build | model owner at the gate or environment |
| Data-triggered retrain | schedule, new-data dispatch, drift alert | model version in registry | gate against champion | alias move if the gate passes | automatic, or owner for risky models |

Router results in the output: `src/training/loss.py` plus a `.dvc` data pointer give `['code_ci', 'model_ct']`; `deploy/alias.yaml` alone gives `['promote_pointer']`.""",
outnote="Real run below: 9 pytest cases for the router and two direct calls. Nothing here needs a GitHub runner; wiring the router into a workflow (a job that outputs the list for `if:` conditions, or `paths` filters) was not executed.",
follow="""
- *Why not bake the model into the image?* Then every retrain is an image build and a rollout, and rollback is slower. Baking it is fine for small, rarely changed models.
- *How does the serving app learn about the new alias?* Reload on a signal or a schedule, or restart the pods (Part 6 and Part 3 own the rollout).
- *Can a data change trigger code CI?* Only if code is affected. Data goes through data tests and CT.
""",
mistakes="""
- One pipeline for everything, so every retrain rebuilds the image.
- Promoting by overwriting a file in object storage with no version or log.
- A router that skips tests for "unknown" paths instead of running the cheap ones.
- Forgetting that dependency changes affect both the image and the model.
- No compatibility test between the new model and the serving code.
""")

Q[10] = dict(
code=[("python", ["gate.py", "test_gate.py"]), ("yaml", ["gate_step.yml"]), ("shell", ["cmds.sh"])],
say="A gate is a policy in code: an absolute floor, a no-regression rule against the champion, budgets, slice checks and a signature check, with missing metrics treated as a failure, and a non-zero exit code that fails the workflow step.",
explain="""
- **Floor:** AUC at least 0.80. Stops a model that is simply bad, even if the champion was also bad.
- **Relative:** candidate AUC may not be worse than the champion by more than 0.005. Stops silent decay of a good model over many small releases. (Part 1 covers the statistical comparison; here the focus is policy.)
- **Budgets:** p95 latency and model size must fit the serving plan. A model that wins on AUC and misses latency is still a fail.
- **Slices:** overall AUC can hide a slice that got worse (new users, a region). Check a floor per slice and a no-big-drop rule against the champion.
- **Signature and schema:** the candidate's input columns and types must match what serving sends.
- **No champion metrics:** decide the policy up front. My choice: fail closed, with an explicit `--allow-no-champion` for a first release, so a lost metrics file cannot wave a model through.
- **Missing candidate metric:** FAIL, never skip.
- **Exit code:** `sys.exit(1)` on any failure; the workflow step fails, later steps (promote) do not run. Print a table so a human can see why.
- The thresholds are example policy values, not benchmarks.
""",
example="""
| Case | Candidate AUC | Champion AUC | Result |
|---|---|---|---|
| good | 0.853 | 0.850 | PASS (drop -0.003, i.e. better) |
| regress | 0.830 | 0.850 | FAIL: drop 0.020 above max 0.005 (floor 0.80 still met) |
| missing | no `p95_ms` | 0.850 | FAIL: metrics present |
| no champion file | 0.853 | none | FAIL closed; PASS only with `--allow-no-champion` |

Hand check for the regress row: 0.850 minus 0.830 is 0.020, and 0.020 is more than 0.005.""",
outnote=NE + "Real runs below: 6 pytest cases, the CLI on four inputs with the exit code printed each time, and actionlint on a workflow step that runs the gate. The workflow itself was not run on GitHub; the exit-code behaviour (non-zero fails a step) is standard Actions behaviour and the script's exit codes were checked locally.",
follow="""
- *Should a failed gate block a hotfix?* Provide a documented override with a named approver, logged, not a quiet bypass.
- *Where do the metrics come from?* The evaluate job writes them next to the run; the champion's come from the registry (Part 4 owns tracking and registry basics).
- *Many slices, multiple tests?* Keep slices few and meaningful, and mind noise on small slices.
""",
mistakes="""
- Treating a missing metric as zero violations.
- Only an absolute floor, so a model decays one release at a time.
- Gate only on the overall metric.
- Exit code always 0 because the script prints "FAIL" but never calls `sys.exit(1)`.
- Gate thresholds living in someone's head instead of in code and review.
""")
