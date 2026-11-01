def T(s):
    def r(m):
        k = m.group(1).split()
        if k[0] == "OUT": return out(k[1], int(k[2]) if len(k) > 2 else None)
        if k[0] == "CODE": return code(k[1])
    return re.sub(r"<<(.+?)>>", r, s)

V = "Versions that ran: Python 3.13, dvc 3.67.1, mlflow 3.17.2, wandb 0.31.0, scikit-learn 1.9.1, tracked in a sqlite backend. Check current docs for newer behaviour."

A[31] = T("""**Say this first (1 line):** Same seed does not mean same result once the environment, the hardware, the thread order or the data order changes, so I log all of those to the run, repeat the run with several seeds, and compare means and spread before I believe a 0.002 gap.

**Then explain:**
- Sources of drift: floating point addition is not associative, so a multithreaded or GPU reduction that adds in a different order gives a slightly different sum. Python string hashing is randomised per process, so set and dict-of-set order can change (`PYTHONHASHSEED`). A data loader with workers can change batch order. A library upgrade can change a default or an algorithm.
- Log the environment on every run: Python and library versions, `pip freeze` (or its hash), CPU or GPU type, OS, data hash, git SHA, seed. Without that you cannot tell a real change from an environment change.
- Repeat, do not trust one run: run each config with 5 or more seeds and report mean, standard deviation, min and max. If the gap between two configs is smaller than the spread between seeds, you have not shown a difference.
- Use a test when the gap is small: a Welch t-test (or a paired test on the same folds, or a bootstrap) tells you if the gap is likely noise. With 5 runs the test is weak, so say so. A p-value is not proof either way.
- Failure modes: seeding only numpy and not the framework; comparing runs on different data splits; picking the best of N seeds and reporting it; calling a result reproducible when only the seed was the same.
- GPU determinism (cuDNN algorithm choice, atomics, framework deterministic flags) is **not executed** here, no GPU. Check the framework docs for its deterministic mode and its speed cost.

**Example:** Two configs A and B score 0.8578 and 0.8500 on the same test set (5 seeds each). The gap is 0.0078. The seed-to-seed std is about 0.01 for A. The gap is smaller than one std, and the Welch p-value is 0.18. I would say: no evidence that A beats B. I would not ship on this.

**Code:**
```python
<<CODE q31.py>>
```

**Output (my run):** run in a temp dir with `python -I`, MLflow on `sqlite:///mlflow.db`. Scores can differ a little on other machines or library versions. """ + V + """
```text
<<OUT q31.clean>>
```
Reading it: the float sum shows the order effect (2.0 versus 2.0000000000000004). The set order changed with `PYTHONHASHSEED`. The same seed twice, and `n_jobs` 1 versus 4, gave the same score here, because scikit-learn's forest is built to be deterministic given a seed. Do not assume that for every library. GPU determinism: not executed.

**Follow-ups:**
- *How many repeats?* Enough that the spread is stable; 5 is a floor, 10 to 30 is better for small gaps. If runs are expensive, use cross-validation folds as the repeats and a paired test.
- *Is a p-value enough?* No. Also report the size of the gap and the interval, and ask if the gap matters for the product.
- *What would you pin for a repeatable build?* Lock file, Python version, container image digest, data hash, seed, and the deterministic flags of the framework.

**Common mistakes:**
- Reading a 0.002 difference from one run.
- Fixing one seed and calling that reproducibility.
- Not logging the environment, so a later "regression" cannot be traced.
- Reporting the best seed.
- Testing many configs and quoting an uncorrected p-value.
""")

A[32] = T("""**Say this first (1 line):** I go from the cheapest check to the dearest: read the exact error, confirm with one command (`dvc status -c`, `dvc status`, `mlflow.get_tracking_uri()`), then fix the cause, not the symptom.

**Then explain:**
- Order for any tool: (1) read the error text fully, (2) check where the tool is pointing (remote, tracking URI, artifact root), (3) check what is committed to Git (`dvc.lock`, `.dvc` files), (4) only then change things.
- Failure modes are mostly "forgot to push", "pointing at the wrong place", "something changed that I did not know I depended on".
- Cases 1 to 4 and 6 were reproduced below. Case 5 (backend error on register) was reproduced in two forms only (a bad database path, and a tracking server that is down). A real out-of-date database schema was NOT reproduced here; for that, the usual fix is `mlflow db upgrade <uri>` after backing up the database (check current docs).

| # | Symptom | Likely cause | Confirm with | Fix |
|---|---|---|---|---|
| 1 | `dvc pull`: files missing, "Is your cache up to date?" | Nobody ran `dvc push`, or the remote path or credentials differ | `dvc status -c`; look at the remote folder or bucket | Push from a machine that has the cache; check `dvc remote list` |
| 2 | `dvc repro` re-runs a stage with no edits | Stage depends on a whole `params.yaml` instead of keys; `dvc.lock` missing or not committed; `always_changed: true`; a dependency folder that changes | `dvc status` (shows which dep changed); `dvc repro --dry` | Use `-p key`; commit `dvc.lock`; remove `always_changed`; move temp files out of the dep |
| 3 | `dvc.lock` conflict | Two branches ran the same stage with different inputs and Git merged text | `grep -n '<<<<<<<' dvc.lock`; `dvc status` fails to parse | Resolve the real input first (params, data), take one side, `dvc repro` to regenerate the lock, commit |
| 4 | MLflow UI lists runs, artifacts missing or will not open | Artifact root was deleted, moved, or is a path the client or server cannot reach | `run.info.artifact_uri`; `list_artifacts`; check the bucket or folder | Restore the location, or use a proxied artifact setup (`--serve-artifacts`, check docs); keep artifact root stable |
| 5 | Registering a model fails with a backend error | Registry needs a database backend; bad DB path or permission; server down; old schema | `mlflow.get_tracking_uri()`, `curl <server>/health`, DB file path and permissions | Point at a database store or a running server; run `mlflow db upgrade` after a version bump |
| 6 | Run logs to a local store, not the team server | `MLFLOW_TRACKING_URI` not set, so the default store was used | `print(mlflow.get_tracking_uri())` | Set the env var in the job; fail fast if it is unset |

**Example:** Case 2 in my run. With `-d params.yaml` the stage re-ran after I changed a key (`noise`) that the script never reads. With `-p lr` it stayed up to date after the same edit. One flag, no more false re-runs.

**Code:**
```bash
<<CODE q32_dvc.sh>>
```
```python
<<CODE q32_mlflow.py>>
```

**Output (my run):** DVC script (cases 1 to 3), temp git repo with a local-folder remote. """ + V + """
```text
<<OUT q32_dvc.out>>
```
MLflow script (cases 6, 4, 5), run from an empty folder:
```text
<<OUT q32_mlflow.out>>
```
What the output shows, and honest notes:
- Case 2: cause B (deleted `dvc.lock`) did not re-run the training in my run. DVC's run cache found the old result ("cached - skipping run") and restored it. So a missing lock may be silent. Cause C (`--always-changed`) re-runs every time, as designed.
- Case 3: in my run the `dvc.lock` markers were real, and `dvc status` failed with a YAML parse error. My "fix" used `git merge -X theirs`, which took one side of both files; in real work, decide the correct params first.
- Case 6: in mlflow 3.17.2 the default tracking URI was a local `mlflow.db` in the current folder (older versions used `./mlruns`). A plain `file:./mlruns` store raised an error unless `MLFLOW_ALLOW_FILE_STORE=true`. Check the docs for your version.
- Case 5: the file store accepted registration here once the opt-in was set. Different versions differ, so I do not claim it fails everywhere.
- Case 4: after I deleted the artifact folder, the metrics stayed but `list_artifacts` returned nothing and download failed. The tracking DB and the artifact store are separate things.

**Follow-ups:**
- *Why does `dvc pull` say files are missing when the .dvc file is in Git?* Git holds only the pointer. The data lives in the cache and remote, and must be pushed separately.
- *How do you stop case 6 in a team?* Set the URI in the job template or CI env and add a startup check that fails if it is a local path.
- *Is deleting dvc.lock a fix for conflicts?* It can work because of the run cache, but you lose the recorded hashes. Regenerate it with `dvc repro`, do not hand-edit.

**Common mistakes:**
- Re-running `dvc repro --force` to hide a bad dependency.
- Hand-editing `dvc.lock`.
- Cleaning the artifact bucket while the tracking DB still lists the runs.
- Debugging the UI before checking which tracking URI the code used.
""")

A[33] = T("""**Say this first (1 line):** lakeFS puts Git-style branches, commits and merges on top of an object store, so a whole data lake is versioned without copying files; DVC instead keeps one small pointer file in Git per dataset or pipeline output.

**Then explain:**
- lakeFS model: a repository over a bucket; branches are cheap pointers (zero-copy), commits are immutable snapshots, merges combine branches; hooks run checks before a merge (data quality, schema, PII scan). Check current docs for the hook mechanism and API.
- Flow: ingest to a branch, validate, then merge to main. Consumers read main, so they never see half-written or failed data. A failed check leaves main untouched.
- Versus DVC: DVC works from the developer's Git repo and a cache and remote; it is file or pipeline oriented and ties data to code commits. lakeFS is a service for the shared lake; it ties versions to the repository, not to your Git repo. They can be combined.
- Delta or Iceberg time travel versions one table, lakeFS versions the repository across tables and formats. Check current docs for what each supports.
- A claim that lakeFS took over DVC stewardship appeared in late-2025 search snippets from vendor-written sources. I could NOT verify it. Say "I have seen it reported, please check current news" if asked.
- Failure modes: concurrent writers to one branch; a merge conflict on the same path; hooks that are too slow; forgetting that a rollback of data does not roll back the model trained on it.
- lakeFS is not installed here and nothing was run against it. The toy below only shows the idea.

**Example (flow):**
```text
ingest job --> branch ingest-<date> --> quality hook --> pass: merge to main
                                                      \\-> fail: branch kept for debugging, main untouched
```

**Code:**
```python
<<CODE q33_branch_sim.py>>
```

**Output (my run):** pure Python, `python -I`. This is a simulation, not lakeFS. lakeFS itself: not executed.
```text
<<OUT q33.out>>
```
Reading it: branching added no blobs; one new file added exactly one blob; the bad batch was blocked before it reached main; after the fix, merge succeeded; two branches editing the same path produced a conflict on the second merge.

**Follow-ups:**
- *When would you pick DVC over lakeFS?* Small team, files tied to a Git repo, pipelines. lakeFS fits a shared lake with many writers.
- *Where do hooks run?* At lakeFS events such as pre-merge; check current docs for how they are configured.
- *Does data versioning give reproducible training?* Only if the training run records the commit or branch id it read.

**Common mistakes:**
- Treating the vendor blog claims as fact.
- Thinking a branch copies the data.
- Merging without a validation gate.
- Not recording the data commit in the model run.
""")

A[34] = T("""**Say this first (1 line):** `dvc gc` deletes whatever your chosen Git revisions do not reference, so on a shared remote I never run it with the default scope; I list what each revision needs first, and I run it dry.

**Then explain:**
- Defaults are dangerous: `dvc gc -w` keeps only what the current workspace (checked-out commit) needs. With `-c` it also deletes from the remote. Other branches, tags and teammates lose data they still need. Use `-A` (all branches and tags) or `--rev` lists, and run `--dry` first. Check `dvc gc --help` for your version.
- Cloud bucket features (versioning, lifecycle rules, replication, object lock) are the safety net. They differ by provider. **Not executed here**; check current docs. I give no prices.
- Who may delete: nobody in a team deletes by hand; one scheduled job with a reviewed scope does. Write access for many, delete access for few.
- Backups: back up the tracking database and the artifact store separately. Losing either one breaks the link between runs and files.
- MLflow retention: runs and artifacts are separate. Deleting a run marks it deleted; removing the data needs a garbage-collect step (check current docs for `mlflow gc` options in your version).
- Failure modes: gc on a stale checkout; a branch that was never pushed; tags missing so old releases lose data; a lifecycle rule that expires "old" versions of an object that a release still needs.

| Item | Policy for a 20-person team | Owner |
|---|---|---|
| DVC remote bucket | Versioning on; no human delete rights; gc by one job only | Platform |
| gc scope | `-A` plus protected release tags, always `--dry` first, review the list | Platform + lead DS |
| Lifecycle rules | Move cold data to cheaper class after N days (check provider docs); never expire versions tagged as release | Platform |
| MLflow DB | Daily backup, restore drill each quarter | Platform |
| MLflow artifacts | Same bucket policy; delete runs only via a retention job | Platform |
| Old runs | Keep registered-model runs forever; others for a set window, agreed with the team | Team leads |
| Access | Read for all; write by CI and owners; delete for the job role only | Security |

**Example:** In my run, main pointed at v3 and a feature branch at v2; a tag pointed at v1. `dvc gc -w -c --dry` listed the v1 and v2 objects for removal from the local cache and the feature branch's v2 object for removal from the remote. `dvc gc -A -c --dry` listed nothing. Same repo, opposite answers, because of scope.

**Code:**
```python
<<CODE q34_gc_report.py>>
```
```bash
<<CODE q34_run.sh>>
```

**Output (my run):** local repo, local-folder remote; `dvc gc` runs were `--dry`. """ + V + """
```text
<<OUT q34.out>>
```
Notes: my report only scanned the revisions I named, so with `main` and `feature` it called the v1 tag's object unreferenced, while `dvc gc -A` kept it. The lesson is to name every revision that matters. In dry mode the DVC message said "Removed N objects"; I checked and the files were still there (5 files before and after). Cloud lifecycle and bucket versioning: not executed.

**Follow-ups:**
- *Safest gc?* A scheduled job, `-A` plus a protected tag list, dry run reviewed first.
- *Do I need gc?* Storage grows with every data version; gc plus a retention policy keeps it bounded.
- *Can bucket versioning save a bad gc?* Often yes, if enabled before the delete and not expired. Check provider docs.

**Common mistakes:**
- Running `dvc gc -w -c` on a shared remote.
- Giving everyone delete rights.
- Forgetting that unpushed branches hold the only copy of some data.
- Backing up the MLflow database but not the artifacts.
""")

A[35] = T("""**Say this first (1 line):** In GenAI work the model is only one input, so I version the data, the prompt, the eval set and the retrieval build as separate things, and I put a hash of each on every eval run so a quality drop points to a changed input.

**Then explain:**
- What to version: fine-tuning JSONL (DVC or a dataset hub revision), prompt templates (Git, plus a hash on the run), eval set (frozen, with a version id), embedding model name and revision, chunking settings and the index build id, base model id or revision.
- Hugging Face datasets and models have Git-style revisions (commit hash); pin the commit, not "main". Hub calls were **not executed** here.
- Tools: MLflow and W&B both have newer features for prompts, tracing and LLM evaluation; they differ by version, so check current docs. The simple way that works anywhere: file hash as a tag plus the file as an artifact.
- Tie a regression to a cause: two runs with the same eval-set hash and different prompt hashes means the prompt did it. Different eval hashes means the comparison is invalid.
- Failure modes: editing the eval set in place; a prompt living only in a notebook; an index rebuilt silently when the embedding model changed; judge-model drift when an LLM judge is itself updated.
- Hosted LLM calls were not run. My script uses a fake function in place of the model so the logging logic is what is tested. Book 2 owns LLM internals.

**Example:** Baseline prompt scored 1.0 exact match on a 2-question eval set. After someone edited the prompt, it scored 0.5. The eval-set hash was the same and the prompt hash differed, so the change is traceable to the prompt in one query.

**Code:**
```python
<<CODE q35_prompt_versioning.py>>
```

**Output (my run):** `python -I`, MLflow on local sqlite. The "model" is a stub, not an LLM. Hosted LLM calls: not executed.
```text
<<OUT q35.out>>
```

**Follow-ups:**
- *Prompt in Git or in a registry?* Git is the base. A registry helps when non-engineers edit prompts; either way log the hash on each run.
- *How do you handle LLM-judge drift?* Pin the judge version, keep a small human-labelled set, re-check it on a schedule.
- *DVC for JSONL?* Yes, same as any dataset: `dvc add`, push, and record the md5.

**Common mistakes:**
- Not versioning the eval set.
- Comparing runs with different eval sets.
- Pointing at a model or dataset "main" instead of a pinned revision.
- Forgetting the chunking and index settings.
""")

A[36] = T("""**Say this first (1 line):** For a team I run a tracking server on a database (Postgres) with an object store for artifacts behind an authenticating reverse proxy, back up both, and upgrade the schema deliberately; or I buy it managed.

**Then explain:**
- Architecture: clients -> reverse proxy (TLS, auth) -> MLflow server -> database (runs, params, metrics, registry) and object store (artifacts, models). Clients can upload artifacts through the server (proxied artifacts) or straight to the bucket; check current docs for the trade-off.
- Auth: MLflow has a basic-auth app and plugins in recent versions; many teams put SSO in the proxy. Check current docs for what your version supports.
- Upgrades: back up the database first, then `mlflow db upgrade <uri>`, then start the new server. Test on a copy.
- Managed MLflow (Databricks, Azure ML, SageMaker) removes the server work; you trade control and portability. Check each vendor's current terms.
- Failure modes: SQLite on a shared disk (locking); artifacts on the server's local disk (lost with the container); no auth on an internet-facing port; upgrading code and DB out of step; no backup of the bucket.
- Part 2 owns the Docker Compose stack for this.

| Layer | Choice | Why | Failure to watch |
|---|---|---|---|
| Entry | Reverse proxy with TLS and SSO | One place for auth | Open port without auth |
| Server | `mlflow server`, stateless, 2+ copies | Easy to replace | Version skew with DB |
| Backend DB | Postgres (managed if possible) | Concurrent writers | No backups |
| Artifacts | S3 or compatible bucket | Durable, cheap | Local disk by mistake |
| Registry | Same DB, aliases | One source of truth | Hard-coded stage URIs |
| Managed option | Databricks, Azure ML, SageMaker | Less ops | Lock-in, per-vendor limits |

**Example:** A run logged through a local server on port 5081 stored its metrics in the database and its text file under the server's artifact folder; the client only saw a `mlflow-artifacts:/` URI. That is the proxied artifact pattern in miniature.

**Code:**
```bash
<<CODE q36_run.sh>>
```
```python
<<CODE q36_client.py>>
```
Production-shaped start command (**not executed**; Postgres and S3 not available here, hostnames are placeholders):
```text
mlflow server --backend-store-uri postgresql://USER:PASS@db-host:5432/mlflow --artifacts-destination s3://my-bucket/mlflow --host 0.0.0.0 --port 5000
```

**Output (my run):** local server on 127.0.0.1 with SQLite and a local artifact folder, then a client run. """ + V + """
```text
<<OUT q36.out>>
```
Postgres, S3, SSO, TLS and anything remote: not executed.

**Follow-ups:**
- *Why not SQLite in production?* Poor fit for many concurrent writers and shared storage.
- *How do you add auth?* Basic-auth app in newer versions, or SSO in the proxy; check current docs.
- *Managed or self-hosted?* Small team with a cloud already: managed. Strict control or portability: self-host.

**Common mistakes:**
- Artifacts left on a container disk.
- No database backup.
- Running the server with no auth on a public IP.
- Upgrading the image without `db upgrade`.
""")

A[37] = T("""**Say this first (1 line):** Before any migration I count runs and compare metrics, then move, then count and compare again, and I keep the old data until the after-check passes.

**Then explain:**
- ./mlruns to database: use `mlflow migrate-filestore --source ./mlruns --target sqlite:///migrated.db` (it exists in 3.17.2; check current docs). It moved runs, params, tags and metrics. The artifact URIs still pointed at the old `mlruns` folder in my run, so **keep that folder** (or copy artifacts and rewrite, which is its own task). Run IDs stayed the same.
- Stages to aliases: stages are deprecated (warning since 2.9). Replace `transition_model_version_stage` with `set_registered_model_alias` and `models:/name/Production` with `models:/name@alias`. Order: add the alias, point serving to the alias URI, verify, then remove the stage use. Hard-coded stage URIs in serving code and CI are what breaks.
- Git LFS to DVC: stop LFS tracking, `git rm --cached` the file, `dvc add` it, push to the DVC remote, commit the `.dvc` file. Old history still holds the LFS pointer, so old commits still need LFS to check out. Rewriting history is a separate, risky choice.
- What breaks: hard-coded URIs, access control (the new store has its own permissions), anything holding run IDs from the old store, CI paths.
- Verify: run count, a few metrics, one model load, one `dvc pull` into a clean clone.

| Migration | Order | What breaks | Check |
|---|---|---|---|
| file store -> DB | back up -> migrate -> count -> point clients | artifact paths, tooling reading `./mlruns` | runs 3 = 3, metrics equal |
| stage -> alias | alias -> switch URIs -> verify -> retire stage | `models:/name/Production` in code | predict through the alias |
| LFS -> DVC | untrack -> `dvc add` -> push -> clean clone pull | old commits still need LFS | clean clone, file hash equal |

**Example:** Three runs in a file store, accuracies 0.80, 0.85, 0.90, depths 2, 3, 4. After migration the sqlite store showed the same three runs and values. Artifact path was unchanged.

**Code:**
```bash
<<CODE q37_lfs_to_dvc.sh>>
```
```python
<<CODE q37_alias.py>>
```
Helpers `q37_make_fs.py` and `q37_count.py` (create three runs; count and print) are in the code folder.

**Output (my run):** with `MLFLOW_ALLOW_FILE_STORE=true` for the old store. """ + V + """
```text
<<OUT q37.out>>
```
LFS to DVC (local git repo with git-lfs, no LFS server, DVC local remote):
```text
<<OUT q37_lfs.out>>
```
Not executed: migration of a registry from a file store, and anything on a server.

**Follow-ups:**
- *Can I keep the stage name working?* Create an alias with the same meaning and update URIs; stages will be removed in a future version, check the release notes.
- *Why keep old artifacts?* The migrated rows still point at them.
- *Rollback?* Keep the old store untouched; point clients back.

**Common mistakes:**
- Deleting `mlruns` after migrating the metadata.
- Not testing the alias in serving code.
- Moving LFS files without checking a clean clone.
- Migrating without a before and after count.
""")

A[38] = T("""**Say this first (1 line):** One shared tracking server with a naming rule and a few mandatory tags, enforced by code, plus per-project DVC remotes and a registry with aliases, so any model can be traced to code, data and owner.

**Then explain:**
- Names: experiments as `team/project/purpose`. Mandatory tags: `git_sha`, `data_hash`, `owner`, `project`. A nightly check flags runs that miss them; CI should fail on the same rule.
- Servers: one shared MLflow server is easier to search and govern; per-team servers give isolation and smaller blast radius. For 50 people in three teams I would start with one, with per-team experiment prefixes and permissions, and split if load or access demands it.
- Data: DVC remote per project (bucket prefix per project). Golden dataset: small, frozen, versioned, used by regression tests on every candidate model.
- Registry: models registered by CI only; aliases such as `candidate` and `champion` replace stages; humans approve alias moves. Part 7 owns the CI/CD detail.
- Retention and cost: keep registered-model runs, expire scratch experiments after a set window, see Q34.
- Access: read for all, write for owners, delete for a job role; SSO at the proxy.
- Onboarding: a project template (repo with DVC, MLflow helper that sets tags, sample CI) so people copy it, not invent.
- Failure modes: free-text names, tags added "later", a golden set that drifts, aliases moved by hand, nobody owning the server.

| Component | Choice | Owner |
|---|---|---|
| Tracking server | Shared MLflow, Postgres, bucket | Platform |
| Naming and tags | Policy plus checker | ML platform lead |
| DVC remotes | One per project, scoped access | Project owner |
| Registry | Aliases, CI registers | Platform + team leads |
| Golden dataset | Frozen, in DVC, tests in CI | Each team |
| Retention | Job with approved scope | Platform |
| Access control | SSO plus role groups | Security |
| Onboarding | Template repo and docs | Platform |

Path: experiment (tagged run) -> candidate evaluated on golden set -> registered version -> alias `candidate` -> approval -> alias `champion` -> deployment reads the alias.

**Example:** My checker over three runs: one fully tagged, one missing `data_hash`, one with experiment name "Quick Test" and `git_sha=latest`. It flagged two of three and returned exit code 1, which a CI job can use.

**Code:**
```python
<<CODE q38_tag_check.py>>
```

**Output (my run):** local sqlite store with the three seeded runs (seed script `q38_seed.py` in the code folder). """ + V + """
```text
<<OUT q38.out>>
```

**Follow-ups:**
- *How do you enforce it for notebooks?* A tiny helper library that sets the tags and fails if inputs are missing, plus the nightly check.
- *Why one server?* One place to search and audit; split only for a clear reason.
- *Who moves `champion`?* A reviewed CI job, not an individual.

**Common mistakes:**
- Rules without enforcement.
- Mutable "latest" data paths.
- One shared remote with write access for everyone.
- No owner for the platform.
""")

A[39] = T("""**Say this first (1 line):** I show the tools working together in one small public repo: a DVC pipeline with a local remote, an MLflow tracker with a registry alias, an offline W&B run, a model card and a README that explains the lineage.

**Then explain:**
- What postings usually list (from skills lists I saw while researching, not interview reports; snippets only): Git, Python, Docker, CI/CD, an experiment tracker such as MLflow or W&B, DVC or similar data versioning, a cloud, sometimes Kubernetes and Airflow. Screens then test whether you understand the idea, not only the commands.
- No budget is needed: DVC with a folder remote, MLflow with sqlite on localhost, W&B offline mode (sync later with a free account). Free-tier limits change; check current terms of each product.
- Proof is a repo a reviewer can run in 5 minutes: one command to reproduce, a README that says what changed between runs and why.
- Be honest about scope: synthetic or public data, a small model, a model card that states limits.
- Failure modes: a lab that only works on your laptop; committing the MLflow database or the data; a model card that overclaims.

| Skill from postings | Lab artifact |
|---|---|
| Data versioning, DVC | `dvc.yaml`, `dvc.lock`, local remote, `dvc push` |
| Experiment tracking | MLflow sqlite runs, tags with git SHA and data hash |
| Model registry | Registered model plus alias `candidate` |
| W&B | Offline run folder; `wandb sync` later (not executed) |
| Reproducibility | `dvc repro` after a param change, `dvc params diff` |
| Documentation | MODEL_CARD.md, README with a lineage sketch |
| Packaging and CI | A short GitHub Actions file running `dvc repro` (Part 7) |

**Example:** In my run, changing `C` from 1.0 to 0.01 in `params.yaml` and running `dvc repro` re-trained only the `train` stage, `dvc params diff` showed the change, and `dvc metrics diff` showed accuracy 0.72 to 0.70. That is one sentence for the README: "lower C hurt accuracy a little on this synthetic data."

**Code:**
```bash
<<CODE q39_lab/lab.sh>>
```
```python
<<CODE q39_lab/train.py>>
```
Also in `code/q39_lab/`: `params.yaml`, `prepare.py`.

**Output (my run):** whole lab in a temp dir. """ + V + """
```text
<<OUT q39.out>>
```
Notes: `search_model_versions` showed an empty alias list but `get_model_version_by_alias` returned version 2, so use the alias lookup call. W&B offline files were created; `wandb sync`, hosted dashboards and sweeps: not executed. I first used a random forest and MLflow 3.17.2 refused to log it with an error about untrusted sklearn types (`sklearn.tree._tree.Tree`) in the skops format, so the lab uses logistic regression; check the MLflow docs for `serialization_format` and trusted types for tree models.

**Follow-ups:**
- *Public data or private?* Public or synthetic; never real customer data in a portfolio repo.
- *What do I say about W&B without an account?* I ran it offline, can sync later, and I know what sweeps and artifacts add.
- *Is a model card required?* It is a good habit and many regulated teams ask; keep it short and honest.

**Common mistakes:**
- Committing `mlflow.db`, data files or the `wandb/` folder.
- Skipping the README lineage explanation.
- Claiming results from one split with no caveat.
- Listing tools you cannot explain.
""")

A[40] = T("""**Say this first (1 line):** OpenLineage records which job read which datasets and wrote which datasets across the whole data stack, while MLflow or W&B records which run produced which model; a regulated team needs both to answer "which models used this table before it was corrected".

**Then explain:**
- OpenLineage is an open spec for lineage events: a job, a run of that job, input and output datasets, and optional "facets" (extra metadata such as schema or row counts). Airflow, Spark and dbt can emit these through integrations; Marquez is a reference server that stores and shows them. Check the current spec and integrations for field names and versions.
- ML-run lineage (MLflow, W&B) is narrower and deeper: parameters, metrics, code version, data hash and the model artifact for one training run.
- Audit question: "which models used customer table X before the fix on date D". Walk from the dataset to downstream jobs, then to model outputs, then filter by event time. The run records then give the exact data hash and who approved the model.
- Gaps: both systems must name datasets the same way; a notebook that reads a CSV emits nothing; lineage tells you what could be affected, not whether the model was actually harmed.
- Failure modes: inconsistent dataset names; missing events from ad hoc jobs; storing events without retention; treating lineage as a proof of correctness.
- No lineage server is available here, so nothing ran against Marquez or any OpenLineage backend. The JSON is hand-written in the spec's style (hedged field names).

**Example:** In my toy graph, `dw.customer` was corrected. The walk found `credit_limit@v3` (directly) and `churn@v7` (through the feature table), and showed `fraud@v12` as not affected, since it reads only transactions.

**Code:**
```python
<<CODE q40_lineage.py>>
```

**Output (my run):** pure Python, `python -I`. No lineage server involved; the event is hand-built.
```text
<<OUT q40.out>>
```

**Follow-ups:**
- *How do you add "before the correction"?* Keep `eventTime` on each edge and keep only events after the old data was read and before the fix.
- *Is MLflow enough?* For one run's inputs, yes if you log the data hash; for tables feeding other tables, no.
- *What do you do with the affected models list?* Re-evaluate or retrain, document the decision, keep the record for audit.

**Common mistakes:**
- Different dataset names in each tool.
- Assuming lineage proves a model is wrong.
- No retention plan for lineage events.
- Believing every job emits events.
""")
