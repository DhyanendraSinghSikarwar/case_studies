# Book 4 — Part 4: Data and model versioning: DVC, MLflow, W&B

**Topic:** data and model versioning and experiment tracking: DVC (remotes, dvc.yaml stages, params, metrics, cache, pipelines, experiments, reproducibility), MLflow (tracking, autolog, artifacts, model registry, aliases versus stages, signatures, projects, local serving), Weights & Biases (runs, sweeps, artifacts, offline mode), data versioning alternatives (lakeFS, Delta and Iceberg time travel at concept level, Git LFS), dataset and model lineage, reproducible experiments, comparing runs, model cards
**Target:** 40  |  **Actual:** 40 (⭐⭐⭐ 15, ⭐⭐ 17, ⭐ 8)  |  **Date:** 2026-10-26  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 1 owns Git and the general reproducibility checklist; Part 2 owns Docker and the MLflow compose stack; Part 5 owns pipeline orchestration (Airflow, Kubeflow, Prefect); Part 6 owns serving frameworks; Part 7 owns CI/CD and promotion gates; Part 8 owns model monitoring; Parts 10 and 11 own AWS, Azure and GCP services; Part 12 owns cost and system design in depth; Book 2 owns LLM internals; Book 3 owns SQL; Book 6 owns product and business.

Evidence limits: the pages found could not be opened (WebFetch failed with getaddrinfo ENOTFOUND for dvc.org), so every source is a search snippet only (see research_notes/Book4_Part04_sources.md). No page was found that reports exact DVC, MLflow or W&B questions asked by a named company at an India or global ML role; 'Asked at' tags therefore name source types (editorial guides, docs, job postings), not verified company reports. Execution limit: pip install worked through the proxy, so Wave B can really run DVC 3.67.1 (local repo, local-directory remote, repro, params and metrics diff, exp run), MLflow 3.17.2 (sqlite backend, autolog, registry aliases, signatures, mlflow models predict, a local mlflow server on localhost) and W&B 0.31.0 in offline mode, with scikit-learn 1.9.1 on Python 3.13. Everything needing cloud buckets, remote servers, SSO, hosted W&B, Docker builds, Spark or lakeFS must be labelled 'not executed'.

---

### Q1 ⭐⭐⭐ 🟢 Why version data and models, and why Git alone is not enough. A team has a 2 GB training CSV, a model file and code. Explain what goes wrong when data lives in a shared folder (silent edits, no link between model and data), what DVC puts in Git (small .dvc pointer files with an md5 hash, plus dvc.lock) versus where the bytes go (the DVC cache and a remote), and what dvc add, git add and git commit each do in order. Show a real dvc add in a throwaway repo and the contents of the .dvc file. Remote servers and cloud buckets are not executed here.
**Asked at:** DVC official docs and tutorials (dvc.org 'Metrics, Plots, and Parameters' get-started page, OneUptime 'How to Configure DVC for Data Versioning' 2026, UCL data version control lecture, DAGsHub pipelines tutorial; search snippets only, not opened); docs and tutorials, not interview reports; MLOps and data science roles
**Say this first (1 line):** Git stores code well but chokes on big binary files and has no idea which data produced which model, so DVC keeps a tiny pointer file with a hash in Git and keeps the real bytes in a cache and a remote.

**Then explain:**
- A shared folder fails in three ways: someone edits `train.csv` silently, nobody can say which file version trained model X, and you cannot go back to last month's data.
- Git alone fails because it keeps every version of a 2 GB file in history, clones get slow, and hosts cap file sizes. Git does not know the data changed unless the bytes are inside the repo.
- DVC puts the small `train.csv.dvc` file in Git. It holds the md5 hash, the size and the path. The data goes into `.dvc/cache` (content-addressed, folder name is the first two hash characters) and later to a remote.
- Order of events: `dvc add` hashes the file, copies it into the cache, writes the `.dvc` file and adds the data file to `.gitignore`. `git add` stages the pointer and the `.gitignore`. `git commit` freezes "this commit uses this data hash".
- Failure modes: if you edit the file after `dvc add` and forget to re-add, `dvc status` shows it as modified, but Git sees nothing. If you forget `dvc push`, a teammate clones the pointer and cannot get the bytes.
- In a pipeline (Q3), the same idea lives in `dvc.lock` for stage outputs.

**Example:** I add a 1000-row CSV. The `.dvc` file says md5 `d9b13d6b...`. The cache holds the file under `files/md5/d9/b13d6b...`. I append one row. The md5 of the file is now `8de6e62d...`, so `dvc status` says "modified". Hash changed means a different data version. Same logic holds for a 2 GB file, only the size differs.

**Code:**
```bash
set -e
export PATH=/tmp/claude-0/ven/v/bin:$PATH
W=$(mktemp -d); cd $W
git init -q; git config user.email a@b.c; git config user.name demo
python3 -I - <<'PY'
import random
random.seed(0)
with open("train.csv","w") as f:
    f.write("x,y\n")
    for i in range(1000): f.write(f"{random.random():.4f},{i%2}\n")
PY
dvc init -q
git commit -qm "dvc init"
dvc add train.csv
echo "--- train.csv.dvc"; cat train.csv.dvc
echo "--- .gitignore"; cat .gitignore
echo "--- git status"; git status --short
git add train.csv.dvc .gitignore
git commit -qm "track train.csv"
echo "--- cache layout"; find .dvc/cache -type f | sed 's#.dvc/cache/##'
echo "--- silent edit"; echo "0.5,1" >> train.csv
dvc status
echo "--- md5 now"; md5sum train.csv
```

**Output (my run):** dvc 3.67.1, Python 3.13, a throwaway repo and a local directory (no remote needed for this question).
```text

To track the changes with git, run:

	git add .gitignore train.csv.dvc

To enable auto staging, run:

	dvc config core.autostage true
--- train.csv.dvc
outs:
- md5: d9b13d6b1aa717f38c852afe582875a0
  size: 9004
  hash: md5
  path: train.csv
--- .gitignore
/train.csv
--- git status
?? .gitignore
?? train.csv.dvc
--- cache layout
files/md5/d9/b13d6b1aa717f38c852afe582875a0
--- silent edit
train.csv.dvc:
	changed outs:
		modified:           train.csv
--- md5 now
8de6e62d730cb364e8d282c830f7ce2b  train.csv
```
Remote servers and cloud buckets: not executed (covered in Q2 with a local-directory remote).

**Follow-ups:**
- *Why not Git LFS?* LFS also keeps pointers, but it has no pipelines, no stage hashes, and hosts meter storage and bandwidth (check current terms). See Q13.
- *Is the md5 a security feature?* No. It is a content address for identifying versions. Do not treat it as tamper protection.
- *What if I never use Git?* `dvc init --no-scm` works, you lose the commit link, so you lose most of the value.

**Common mistakes:**
- Committing the data file and the `.dvc` file both. The `.gitignore` entry exists to stop this.
- Running `dvc add` and thinking the data is backed up. It is only in the local cache until you `dvc push`.
- Saying "DVC stores the data in Git". It stores a pointer in Git.

### Q2 ⭐⭐⭐ 🟢 DVC remotes: dvc remote add, dvc push and dvc pull. Explain what a remote is (S3, GCS, Azure, SSH, a plain local directory), the default remote, how push uploads only missing hashes, how pull restores files for the checked-out Git commit, and what lives in .dvc/config (shared, committed) versus .dvc/config.local (secrets, ignored). Run the full cycle against a local-directory remote, delete the workspace file and cache, and restore it with dvc pull. Cloud remotes and credentials are not executed; show the S3 config lines hedged.
**Asked at:** DVC official docs and tutorials (dvc.org 'Metrics, Plots, and Parameters' get-started page, OneUptime 'How to Configure DVC for Data Versioning' 2026, UCL data version control lecture, DAGsHub pipelines tutorial; search snippets only, not opened); docs and tutorials, not interview reports; MLOps and data science roles
**Say this first (1 line):** A DVC remote is shared storage for the cached files (S3, GCS, Azure, SSH or even a folder); `dvc push` uploads what the remote is missing, `dvc pull` downloads exactly what the checked-out Git commit points to.

**Then explain:**
- `dvc remote add -d name url` writes to `.dvc/config`. The `-d` flag makes it the default remote. This file is committed, so the team shares the URL.
- Secrets go in `.dvc/config.local` with `--local`. DVC puts that file in `.dvc/.gitignore`, so it is never committed. Never put keys in the shared config.
- Push works by hash: the remote already has an object with that md5, so it is skipped. A second push says "Everything is up to date".
- Pull reads the `.dvc` files and `dvc.lock` at the current commit, finds their hashes, fetches missing objects into the cache, then links or copies them into the workspace.
- Failure modes: forgot `dvc push` (teammate sees missing files), wrong credentials, a plugin is not installed (S3 needs the S3 extra, check current docs), or someone ran `dvc gc` against the remote (see Q5).

**Example:** One 501-line `data.csv`. After `dvc push` the remote folder holds one object `files/md5/c5/3f3d80...`. I delete `data.csv` and `.dvc/cache`. `dvc status -c` says "deleted: data.csv". `dvc pull` fetches one file and the CSV is back with 501 lines.

**Code:**
```bash
set -e
export PATH=/tmp/claude-0/ven/v/bin:$PATH
W=$(mktemp -d); R=$(mktemp -d); cd $W
git init -q; git config user.email a@b.c; git config user.name demo
python3 -I -c "
open('data.csv','w').write('x,y\n'+''.join(f'{i},{i%2}\n' for i in range(500)))"
dvc init -q; dvc add -q data.csv
dvc remote add -d localstore $R/store
dvc remote add -q s3demo s3://my-bucket/dvcstore
git add -A; git commit -qm init
echo "--- .dvc/config"; cat .dvc/config
echo "--- push 1"; dvc push
echo "--- push 2"; dvc push
echo "--- remote layout"; (cd $R/store; find . -type f | sort)
echo "--- add a secret-ish setting to local config"
dvc remote modify s3demo region us-east-1
dvc remote modify --local s3demo access_key_id FAKE_KEY_FOR_DEMO
echo "--- .dvc/config after region edit"; cat .dvc/config
echo "--- .dvc/config.local"; cat .dvc/config.local
echo "--- gitignore in .dvc"; cat .dvc/.gitignore
echo "--- delete workspace file and cache"
rm data.csv; rm -rf .dvc/cache
ls
echo "--- dvc status -c"; dvc status -c || true
echo "--- pull"; dvc pull
ls; wc -l data.csv
```

**Output (my run):** dvc 3.67.1, local directory as the remote. Temp paths vary per run.
```text
Setting 'localstore' as a default remote.
--- .dvc/config
[core]
    remote = localstore
['remote "localstore"']
    url = /tmp/tmp.FsmPbO2God/store
['remote "s3demo"']
    url = s3://my-bucket/dvcstore
--- push 1
1 file pushed
--- push 2
Everything is up to date.
--- remote layout
./files/md5/c5/3f3d80faae72f979df2dd3730349c2
--- add a secret-ish setting to local config
--- .dvc/config after region edit
[core]
    remote = localstore
['remote "localstore"']
    url = /tmp/tmp.FsmPbO2God/store
['remote "s3demo"']
    url = s3://my-bucket/dvcstore
    region = us-east-1
--- .dvc/config.local
['remote "s3demo"']
    access_key_id = FAKE_KEY_FOR_DEMO
--- gitignore in .dvc
/config.local
/tmp
/cache
--- delete workspace file and cache
data.csv.dvc
--- dvc status -c
	deleted:            data.csv
--- pull
A       data.csv
1 file fetched and 1 file added
data.csv
data.csv.dvc
501 data.csv
```
S3 remote: only the config lines were written (`s3demo` with a fake key in `config.local`). Upload to S3/GCS/Azure and real credentials: not executed here. Validation that did run: the config files were generated and read back by DVC, and the full push/delete/pull cycle ran against the local-directory remote.

**Follow-ups:**
- *Several remotes?* Yes. `-r name` picks one. Only one is default.
- *Does push upload everything each time?* No. Only hashes the remote lacks.
- *CI credentials?* Use environment variables or the CI secret store, not the repo. Check current docs for the variable names of your cloud.

**Common mistakes:**
- Committing credentials into `.dvc/config` instead of `config.local` (or CI secrets).
- Assuming `git push` also sends the data.
- Pulling on a commit whose data was never pushed. Result: "missing files" error.

### Q3 ⭐⭐⭐ 🟡 Write a DVC pipeline in dvc.yaml with prepare, train and evaluate stages. Explain cmd, deps, outs, params, metrics and plots, how dvc.lock records the exact hashes that were run, and how dvc repro decides which stages to re-run (changed dep, param or command) and which to skip. Show the DAG with dvc dag and what happens when you edit only the evaluate script. Run it for real on a tiny numpy or sklearn dataset and show the repro output.
**Asked at:** DVC official docs and tutorials (dvc.org 'Metrics, Plots, and Parameters' get-started page, OneUptime 'How to Configure DVC for Data Versioning' 2026, UCL data version control lecture, DAGsHub pipelines tutorial; search snippets only, not opened); docs and tutorials, not interview reports; MLOps and data science roles
**Say this first (1 line):** `dvc.yaml` declares stages as commands with their inputs and outputs, `dvc.lock` records the exact hashes of the last run, and `dvc repro` re-runs only the stages whose inputs, params or command changed.

**Then explain:**
- Stage fields: `cmd` (what to run), `deps` (files that make the stage stale), `params` (keys from `params.yaml`), `outs` (files DVC caches), `metrics` (small JSON or YAML numbers), `plots` (data for charts).
- `dvc.lock` stores, per stage, the command, the md5 of each dep, the value of each param and the md5 of each output. Commit it to Git. It is the "what was actually run" record. `dvc.yaml` is the "what should run" recipe.
- `dvc repro` walks the graph in order. If a stage's deps, params or `cmd` match `dvc.lock`, it prints "didn't change, skipping". Otherwise it runs and updates the lock. Downstream stages rerun when their dep (the upstream output) hash changes.
- Edit only `evaluate.py`: prepare and train are skipped, only evaluate runs. Change `train.C`: prepare skipped, train and evaluate run.
- Failure modes: a file used by the script but not listed in `deps` (DVC will not notice changes), outputs written to places not listed in `outs`, a non-deterministic script that changes the output hash on every run, two stages writing the same output.
- `metrics` and `plots` use `cache: false` in my file so small files stay in Git for easy diffs. That is a choice, not a rule.

**Example:** Three stages: prepare makes `prepared.npz`, train makes `model.joblib`, evaluate writes `metrics.json` and `roc.csv`. After an edit to `evaluate.py`, I expect exactly one stage to run. The output shows that: two "skipping" lines, one "Running stage 'evaluate'".

**Code:** The three scripts are small numpy/sklearn files (in `code/proj/`: `prepare.py`, `train.py`, `evaluate.py`, each reads its keys from `params.yaml`).
```yaml
stages:
  prepare:
    cmd: python prepare.py
    deps:
      - prepare.py
    params:
      - prepare.seed
      - prepare.test_frac
    outs:
      - prepared.npz
  train:
    cmd: python train.py
    deps:
      - train.py
      - prepared.npz
    params:
      - train.C
    outs:
      - model.joblib
  evaluate:
    cmd: python evaluate.py
    deps:
      - evaluate.py
      - prepared.npz
      - model.joblib
    metrics:
      - metrics.json:
          cache: false
    plots:
      - roc.csv:
          x: fpr
          y: tpr
          cache: false

prepare:
  seed: 7
  test_frac: 0.25
train:
  C: 1.0
```
```bash
set -e
export PATH=/tmp/claude-0/ven/v/bin:$PATH
W=$(mktemp -d); cp proj/* $W/; cd $W
git init -q; git config user.email a@b.c; git config user.name demo
dvc init -q; git add -A; git commit -qm init
echo "--- repro #1"; dvc repro 2>&1 | grep -v -i 'warn'
echo "--- dvc.lock (train stage)"; sed -n '/^  train:/,/^  evaluate:/p' dvc.lock | head -30
echo "--- dag"; dvc dag
echo "--- repro #2 (nothing changed)"; dvc repro
echo "--- edit only evaluate.py (comment)"; echo "# tweak" >> evaluate.py
dvc repro
echo "--- change train.C only"; sed -i 's/C: 1.0/C: 0.1/' params.yaml
dvc repro
echo "--- dvc status after changing prepare.seed"; sed -i "s/seed: 7/seed: 8/" params.yaml
dvc status
cat metrics.json
```

**Output (my run):** dvc 3.67.1, scikit-learn 1.9.1. DVC's trailing "To track the changes with git..." and "Use `dvc push`" hint lines are trimmed.
```text
--- repro #1
Running stage 'prepare':
> python prepare.py
prepared 300 train rows
Generating lock file 'dvc.lock'
Updating lock file 'dvc.lock'

Running stage 'train':
> python train.py
trained with C = 1.0
Updating lock file 'dvc.lock'

Running stage 'evaluate':
> python evaluate.py
evaluated
Updating lock file 'dvc.lock'

--- dvc.lock (train stage)
  train:
    cmd: python train.py
    deps:
    - path: prepared.npz
      hash: md5
      md5: 6b7a979dc958f90ce05da26c9e7ffe53
      size: 13774
    - path: train.py
      hash: md5
      md5: a8ce490d01045ca694769ab036e917aa
      size: 298
    params:
      params.yaml:
        train.C: 1.0
    outs:
    - path: model.joblib
      hash: md5
      md5: 8ceac560346ba3243217c578149a59d5
      size: 879
  evaluate:
--- dag
        +---------+      
        | prepare |      
        +---------+      
         *         **    
       **            *   
      *               ** 
+-------+               *
| train |             ** 
+-------+            *   
         *         **    
          **     **      
            *   *        
        +----------+     
        | evaluate |     
        +----------+     
--- repro #2 (nothing changed)
Stage 'prepare' didn't change, skipping
Stage 'train' didn't change, skipping
Stage 'evaluate' didn't change, skipping
Data and pipelines are up to date.
--- edit only evaluate.py (comment)
Stage 'prepare' didn't change, skipping
Stage 'train' didn't change, skipping
Running stage 'evaluate':
> python evaluate.py
evaluated
Updating lock file 'dvc.lock'

--- change train.C only
Stage 'prepare' didn't change, skipping
Running stage 'train':
> python train.py
trained with C = 0.1
Updating lock file 'dvc.lock'

Running stage 'evaluate':
> python evaluate.py
evaluated
Updating lock file 'dvc.lock'

--- dvc status after changing prepare.seed
prepare:
	changed deps:
		params.yaml:
			modified:           prepare.seed
{
  "accuracy": 0.81,
  "auc": 0.907
}
```
No remote was used.

**Follow-ups:**
- *`dvc repro --dry`?* Prints what would run without running. It is shallow for downstream stages, so I use `dvc status` to see what changed.
- *Force a rerun?* `dvc repro -f` or `dvc repro --force`.
- *Why not a Makefile?* Make tracks timestamps; DVC tracks content hashes, caches outputs and ties them to Git.

**Common mistakes:**
- Forgetting to list a script or config file in `deps`, so edits silently do nothing.
- Declaring whole `params.yaml` instead of keys, so any edit triggers a rerun (see Q4).
- Not committing `dvc.lock`. Then nobody can reproduce the run.

### Q4 ⭐⭐⭐ 🟡 Parameters and metrics in DVC. Explain params.yaml, how a stage declares only the keys it uses (train.lr) so that unrelated edits do not trigger a re-run, metrics files (JSON or YAML) versus plots, and dvc params diff and dvc metrics diff between the workspace and HEAD or between two Git revisions. Run a pipeline, change one parameter, re-run, and show both diffs. Say what a skeptical interviewer will ask: what if the metric file is not tracked, or the param key is misspelled (a missing key is an error)?
**Asked at:** DVC official docs and tutorials (dvc.org 'Metrics, Plots, and Parameters' get-started page, OneUptime 'How to Configure DVC for Data Versioning' 2026, UCL data version control lecture, DAGsHub pipelines tutorial; search snippets only, not opened); docs and tutorials, not interview reports; MLOps and data science roles
**Say this first (1 line):** `params.yaml` holds the knobs, a stage lists only the keys it uses, and `dvc params diff` and `dvc metrics diff` show what changed in knobs and results between the workspace and a Git revision.

**Then explain:**
- A stage with `params: [train.C]` reruns only when `train.C` changes. Edit another section or add a new key and DVC says "up to date" (my run shows this).
- Metrics are small files (JSON or YAML) that you list under `metrics:`. Plots are tabular data (CSV, JSON) for charts. Metrics are for numbers you compare, plots are curves.
- `dvc params diff` compares params, `dvc metrics diff` compares metric values and shows the change. With no arguments it compares workspace against HEAD. `dvc metrics diff HEAD~1 HEAD` compares two commits.
- Note: in my run `params diff` also listed the new `notes.owner` key because it reads the whole file, but `dvc status` ignored it. Diff is a report. Staleness is by declared keys only.
- Failure modes: a misspelled key in `dvc.yaml` is a hard error, not a silent skip (shown). A metrics file that is missing or not tracked gives a "failed to load some metrics" message and an empty row. A metric not committed to Git has nothing to diff against HEAD.

**Example:** `train.C` goes 1.0 to 0.01. Accuracy goes 0.81 to 0.76 (change -0.05) while auc barely moves, 0.9066 to 0.9078. Two lines of diff tell the story, no notebook needed.

**Code:** Same project as Q3 (`code/proj`), shell steps below.
```bash
set -e
export PATH=/tmp/claude-0/ven/v/bin:$PATH
W=$(mktemp -d); cp proj/* $W/; cd $W
git init -q; git config user.email a@b.c; git config user.name demo
dvc init -q; git add -A; git commit -qm init
dvc repro -q; git add -A; git commit -qm "baseline C=1.0"
echo "--- unrelated edit: add an unused key to params.yaml"
printf "notes:\n  owner: team-a\n" >> params.yaml
dvc status
echo "--- change train.C"
sed -i 's/C: 1.0/C: 0.01/' params.yaml
dvc repro -q
echo "--- params diff (workspace vs HEAD)"; dvc params diff
echo "--- metrics diff (workspace vs HEAD)"; dvc metrics diff
echo "--- metrics show"; dvc metrics show
git add -A; git commit -qm "C=0.01"
echo "--- metrics diff HEAD~1 HEAD"; dvc metrics diff HEAD~1 HEAD
echo "--- plots diff --json (head)"; dvc plots diff HEAD~1 HEAD -o plots_out >/dev/null 2>&1 && ls plots_out || echo "plots diff failed"
echo "--- misspelled param key"
sed -i 's/- train.C$/- train.Cc/' dvc.yaml
dvc repro 2>&1 | tail -4 || true
sed -i 's/- train.Cc$/- train.C/' dvc.yaml
echo "--- metrics file missing"
rm metrics.json
dvc metrics show 2>&1 | tail -3 || true
```

**Output (my run):** dvc 3.67.1. Stage prints from the scripts are shown once.
```text
prepared 300 train rows
trained with C = 1.0
evaluated
--- unrelated edit: add an unused key to params.yaml
Data and pipelines are up to date.
--- change train.C
trained with C = 0.01
evaluated
--- params diff (workspace vs HEAD)
Path         Param        HEAD    workspace
params.yaml  notes.owner  -       team-a
params.yaml  train.C      1.0     0.01
--- metrics diff (workspace vs HEAD)
Path          Metric    HEAD    workspace    Change
metrics.json  accuracy  0.81    0.76         -0.05
metrics.json  auc       0.9066  0.9078       0.0012
--- metrics show
Path          accuracy    auc
metrics.json  0.76        0.9078
--- metrics diff HEAD~1 HEAD
Path          Metric    HEAD~1    HEAD    Change
metrics.json  accuracy  0.81      0.76    -0.05
metrics.json  auc       0.9066    0.9078  0.0012
--- plots diff --json (head)
index.html
--- misspelled param key
Stage 'prepare' didn't change, skipping
ERROR: failed to reproduce 'train': Parameters 'train.Cc' are missing from 'params.yaml'.
--- metrics file missing
DVC failed to load some metrics for following revisions: ''.
Path
metrics.json
```
`dvc plots diff` produced an `index.html` (not shown or viewed). No remote used.

**Follow-ups:**
- *Params without a file?* `dvc exp run -S train.C=0.1` overrides one value for an experiment (see the `dvc exp` docs; I only ran it in setup checks, not for this answer).
- *Metrics vs MLflow?* DVC metrics live in Git and are great for diffs on a commit. MLflow is for many runs. See Q14.
- *Lists and nested keys?* Dotted names for nested keys (`train.C`). Check the docs for lists.

**Common mistakes:**
- Listing the whole params file as a dep, so every edit retrains.
- Metrics file in `.gitignore` or `cache: true` unthinkingly, then Git history has no numbers to diff.
- Typo in a key and assuming DVC will skip it.

### Q5 ⭐⭐⭐ 🟡 Reproduce a model trained six months ago. You have a Git tag, a dvc.lock and a remote. Give the exact sequence (git checkout tag, dvc checkout or dvc pull, dvc repro or dvc repro --dry) and what makes it fail in real life: the remote was garbage-collected, the Python or library versions drifted, a data source outside DVC changed, random seeds, GPU nondeterminism. Show a local demo that checks out an old commit and restores the data and the model hash. This extends Part 1's reproducibility checklist with the DVC mechanics.
**Asked at:** DVC official docs and tutorials (dvc.org 'Metrics, Plots, and Parameters' get-started page, OneUptime 'How to Configure DVC for Data Versioning' 2026, UCL data version control lecture, DAGsHub pipelines tutorial; search snippets only, not opened); docs and tutorials, not interview reports; MLOps and data science roles
**Say this first (1 line):** Check out the Git tag, then `dvc pull` (or `dvc checkout` if the cache has it) to get the exact data and model for that commit, then `dvc status` or `dvc repro` to prove it matches `dvc.lock`.

**Then explain:**
- Steps: `git checkout v1`, `dvc pull` (fresh machine) or `dvc checkout` (cache already has it), then `dvc status` (clean means workspace matches the lock), then `dvc repro` only if you need to retrain.
- Git gives you code, `dvc.yaml`, `params.yaml`, `dvc.lock`. DVC gives you the bytes for the hashes in those files. Both are needed.
- What breaks in real life: the remote was garbage-collected (shown below), Python or library versions drifted (DVC does not pin your environment), a data source outside DVC changed (a SQL table, an API), random seeds not set, GPU nondeterminism, or a pickle that no longer loads on a newer library.
- Retraining the "same" model is not guaranteed to give the same hash. Pulling the stored model is. So for an audit, pull first, retrain only if you must.
- Part 1 covers the reproducibility checklist (seeds, pinned deps, lock files). This answer adds the DVC mechanics.

**Example:** Tag `v1` has model md5 `8ceac560...`. I move on to `v2` with a different `C`. Going back to `v1`, `dvc checkout` restores the file and `md5sum` on disk gives `8ceac560...` again. In a fresh clone, `dvc pull` fetches 2 files and the md5 matches. After `dvc gc -w -c` on the remote, a fresh clone of `v1` fails with "Checkout failed ... Is your cache up to date?".

**Code:** Same project as Q3.
```bash
set -e
export PATH=/tmp/claude-0/ven/v/bin:$PATH
W=$(mktemp -d); R=$(mktemp -d); cp proj/* $W/; cd $W
git init -q -b main; git config user.email a@b.c; git config user.name demo
dvc init -q; dvc remote add -d store $R/store -q; git add -A; git commit -qm init
dvc repro -q >/dev/null; dvc push -q
git add -A; git commit -qm "model v1"; git tag v1
echo "v1 model md5 from dvc.lock:"; grep -A3 'path: model.joblib' dvc.lock | grep md5: | head -1
echo "--- experiment moves on: C=0.01 -> model v2"
sed -i 's/C: 1.0/C: 0.01/' params.yaml; dvc repro -q >/dev/null; dvc push -q
git add -A; git commit -qm "model v2"
echo "v2 model md5:"; md5sum model.joblib | cut -c1-32
echo "--- go back to v1"
git -c advice.detachedHead=false checkout -q v1
dvc status
dvc checkout
echo "md5 of model.joblib on disk now:"; md5sum model.joblib | cut -c1-32
echo "--- repro dry-run check (is v1 reproducible without retraining?)"
dvc status
echo "--- fresh clone, pull from remote"
cd $(mktemp -d); git -c advice.detachedHead=false clone -q $W fresh; cd fresh; git -c advice.detachedHead=false checkout -q v1
cp $W/.dvc/config.local .dvc/ 2>/dev/null || true
ls
dvc pull
md5sum model.joblib | cut -c1-32
echo "--- remote garbage collected (gc keeps only workspace=v2)"
cd $W; git checkout -q main
dvc gc -w -c -f
cd $(mktemp -d); git -c advice.detachedHead=false clone -q $W fresh2; cd fresh2; git -c advice.detachedHead=false checkout -q v1
dvc pull 2>&1 | tail -6 || true
```

**Output (my run):** dvc 3.67.1, git, local-directory remote. Git's detached-HEAD advice is suppressed in the script.
```text
v1 model md5 from dvc.lock:
      md5: 8ceac560346ba3243217c578149a59d5
--- experiment moves on: C=0.01 -> model v2
v2 model md5:
6c4b20cf712cd280633ed13c86254e62
--- go back to v1
train:
	changed outs:
		modified:           model.joblib
evaluate:
	changed deps:
		modified:           model.joblib
M       model.joblib
md5 of model.joblib on disk now:
8ceac560346ba3243217c578149a59d5
--- repro dry-run check (is v1 reproducible without retraining?)
Data and pipelines are up to date.
--- fresh clone, pull from remote
dvc.lock
dvc.yaml
evaluate.py
metrics.json
params.yaml
prepare.py
roc.csv
train.py
A       model.joblib
A       prepared.npz
2 files fetched and 2 files added
8ceac560346ba3243217c578149a59d5
--- remote garbage collected (gc keeps only workspace=v2)
WARNING: This will remove all cache except items used in the workspace of the current repo.
Removed 5 objects from repo cache.
No unused 'legacy' cache to remove.
Removed 1 objects from remote.
No unused cache to remove from remote.
A       prepared.npz
1 file fetched and 1 file added
ERROR: failed to pull data from the cloud - Checkout failed for following targets:
model.joblib
Is your cache up to date?
<https://error.dvc.org/missing-files>
```
The same model md5 `8ceac560...` appeared in an earlier run of the Q3 pipeline. That is luck of a deterministic tiny sklearn fit on one machine, not a promise across machines or library versions.

**Follow-ups:**
- *How to stop GC from deleting old tags?* Use `dvc gc` with `--all-tags` or `--all-commits` (check current docs) and run it carefully, ideally only with a team agreement.
- *Retrain gives a different hash, is that a bug?* Not necessarily. Compare metrics, not file hashes, and fix seeds and library versions.
- *Environment?* Pin it separately (lock file, Docker image tag) and record it next to the run.

**Common mistakes:**
- Assuming Git tag equals reproducible. The data bytes must also still exist on the remote.
- Running `dvc gc -w -c` on a shared remote without checking what other branches and tags need.
- Forgetting the environment: same DVC files, different scikit-learn, different model.

### Q6 ⭐⭐⭐ 🟡 MLflow Tracking basics. Explain experiments, runs, parameters, metrics (with steps), tags, artifacts, the difference between the backend store (runs, params, metrics) and the artifact store (files), and the run_id. Write a script that logs params, a metric history, a text file and a matplotlib or JSON artifact to a local sqlite backend, then reads them back with MlflowClient and search_runs. Say what happens if you call log_param twice with a different value for the same key in one run (it raises an error). Hosted tracking servers are not executed.
**Asked at:** MLflow official docs and tutorials (mlflow.org tracking, autolog and model registry pages, MLflow 3.1.3 autolog docs, MLflow 2.11 model signature docs, DataTalksClub MLOps Zoomcamp experiment-tracking module, Azure ML MLflow training pages; search snippets only, not opened); docs and course material, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** MLflow Tracking records runs inside experiments: params (inputs, set once), metrics (numbers, can have steps), tags (labels), and artifacts (files); the backend store keeps the structured data and the artifact store keeps the files.

**Then explain:**
- Experiment = a named group of runs. Run = one execution, with a unique `run_id` (32 hex characters).
- Params are strings and immutable per key in one run. Metrics can be logged many times with a `step`, so you get a history (loss curve). Tags are free labels like `data_version`.
- Backend store: a database (SQLite, Postgres, MySQL) with runs, params, metrics, tags. Artifact store: a folder or object store with files (models, plots, text). A run only holds the artifact location.
- With `sqlite:///mlflow.db` and no server, the DB is the backend and `./mlruns/...` becomes the artifact folder (shown below).
- Failure modes: `log_param` twice with a different value raises an error (shown); forgetting `set_experiment` puts runs in "Default"; forgetting to end runs when not using `with`; logging a param that changes each step (use a metric).

**Example:** One run logs `lr=0.1`, loss `0.9, 0.6, 0.45` at steps 0-2, `val_acc=0.81`, tag `data_version=v1`, and two text/JSON artifacts. Reading back gives the same values. A search `params.model = 'logreg' and metrics.val_acc > 0.5` returns that one run.

**Code:**
```python
import json, os, mlflow
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("q6-demo")
with mlflow.start_run(run_name="baseline") as run:
    mlflow.log_param("lr", 0.1)
    mlflow.log_params({"epochs": 3, "model": "logreg"})
    for step, loss in enumerate([0.9, 0.6, 0.45]):
        mlflow.log_metric("loss", loss, step=step)
    mlflow.log_metric("val_acc", 0.81)
    mlflow.set_tag("data_version", "v1")
    mlflow.log_text("hello from run\n", "notes/readme.txt")
    mlflow.log_dict({"classes": [0, 1]}, "meta.json")
    try:
        mlflow.log_param("lr", 0.5)
    except MlflowException as e:
        print("second log_param error:", str(e)[:150])
    run_id = run.info.run_id
    print("artifact_uri:", run.info.artifact_uri.replace(os.getcwd(), "<cwd>"))

c = MlflowClient()
r = c.get_run(run_id)
print("params:", r.data.params)
print("metrics (latest):", r.data.metrics)
print("tags data_version:", r.data.tags["data_version"])
print("loss history:", [(m.step, m.value) for m in c.get_metric_history(run_id, "loss")])
print("artifacts:", [a.path for a in c.list_artifacts(run_id)])
df = mlflow.search_runs(experiment_names=["q6-demo"], filter_string="params.model = 'logreg' and metrics.val_acc > 0.5")
print(df[["run_id", "status", "params.lr", "metrics.val_acc", "tags.data_version"]].assign(run_id=lambda d: d.run_id.str[:8]).to_string(index=False))
print("files:", sorted(f for f in os.listdir(".") if f.startswith("mlflow") or f in ("mlruns",)))
```

**Output (my run):** mlflow 3.17.2, Python 3.13, `python3 -I` in a temp dir, telemetry off. Run id shortened by the script for the table. No tracking server involved, hosted servers: not executed.
```text
2026/10/26 14:07:07 INFO mlflow.store.db.utils: Creating initial MLflow database tables...
2026/10/26 14:07:07 INFO mlflow.store.db.utils: Updating database tables
2026/10/26 14:07:08 INFO mlflow.tracking.fluent: Experiment with name 'q6-demo' does not exist. Creating a new experiment.
second log_param error: Changing param values is not allowed. Param with key='lr' was already logged with value='0.1' for run ID='9daa6370edd54baa8be7bf9a4777cd2d'. Attempted
artifact_uri: <cwd>/mlruns/1/9daa6370edd54baa8be7bf9a4777cd2d/artifacts
params: {'lr': '0.1', 'epochs': '3', 'model': 'logreg'}
metrics (latest): {'loss': 0.45, 'val_acc': 0.81}
tags data_version: v1
loss history: [(0, 0.9), (1, 0.6), (2, 0.45)]
artifacts: ['meta.json', 'notes']
  run_id   status params.lr  metrics.val_acc tags.data_version
9daa6370 FINISHED       0.1             0.81                v1
files: ['mlflow.db', 'mlruns']
```

**Follow-ups:**
- *How do I overwrite a param?* You cannot within a run. Start a new run, or use a metric or tag if it really changes.
- *Where do I see the UI?* `mlflow ui --backend-store-uri sqlite:///mlflow.db` (not run for this answer; Q10 ran the server).
- *Metric vs param?* Param is an input you choose. Metric is an output you measure.

**Common mistakes:**
- Using the file store by habit (Q10) and then wanting the registry.
- Logging a number as a param so you cannot sort or chart it.
- Different metric names between runs (`val_acc` vs `valid_acc`), so comparison breaks.

### Q7 ⭐⭐⭐ 🟡 MLflow autolog with scikit-learn. Explain what mlflow.sklearn.autolog() records (estimator params, training metrics, the score, optionally the model and signature, input example, tags), what it does not (your custom metric on a test set, data version, git commit), how it behaves with cross-validation or GridSearchCV (child runs), and the pitfalls: several fit() calls in one run, forgetting the autolog call before fit, and logging huge models by default. Run it on a small dataset, list what ended up in the run, and say which flags you would set (log_models, log_datasets). Version-specific behaviour: state the MLflow version that ran.
**Asked at:** MLflow official docs and tutorials (mlflow.org tracking, autolog and model registry pages, MLflow 3.1.3 autolog docs, MLflow 2.11 model signature docs, DataTalksClub MLOps Zoomcamp experiment-tracking module, Azure ML MLflow training pages; search snippets only, not opened); docs and course material, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** `mlflow.sklearn.autolog()` logs the estimator's params, training metrics and some artifacts automatically on `fit`, but it does not know your test set, your data version or your git state unless you log them.

**Then explain:**
- Call it before `fit()`. It patches sklearn, so a `fit` that ran earlier is not logged.
- In my run it recorded estimator params (`C`, `max_iter`, ...), training metrics (accuracy, f1, log loss, roc auc, `training_score`), tags `estimator_name` and `estimator_class`, plus artifacts `estimator.html`, `metric_info.json` and a training confusion matrix.
- It did not record the git commit (my temp dir was not a git repo, so that tag was absent) or any data version. Log those yourself with tags.
- A call to `model.score(Xte, yte)` inside an active run was also logged as `LogisticRegression_score_Xte`. That is a post-training metric hook. Handy, but name your own metrics (`test_accuracy`) so it is clear.
- `GridSearchCV` creates a parent run with `best_cv_score` and `cv_results.csv`, plus child runs. Here that gave 2 child runs, one per value of C.
- Pitfalls: two `fit` calls in one run: the second fit's `C=5.0` did not replace the first value (params are immutable per run), so use one run per fit. By default autolog logs the model, which can be large. I set `log_models=False` and `log_datasets=False`, then log the final model on purpose (Q8).

**Example:** `LogisticRegression(C=0.5)` on iris. Training accuracy `0.943`, test accuracy `1.0` (30% stratified split, 45 rows). The run lists 3 artifacts. The grid search of 2 values of C gives 2 child runs under one parent.

**Code:**
```python
import mlflow, mlflow.sklearn, sklearn
from mlflow import MlflowClient
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split

print("mlflow", mlflow.__version__, "sklearn", sklearn.__version__)
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("q7-autolog")
mlflow.sklearn.autolog(log_models=False, log_datasets=False)   # autolog BEFORE fit

X, y = load_iris(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
c = MlflowClient()
exp = c.get_experiment_by_name("q7-autolog").experiment_id

with mlflow.start_run(run_name="single-fit") as r:
    m = LogisticRegression(C=0.5, max_iter=200).fit(Xtr, ytr)
    mlflow.log_metric("test_accuracy", m.score(Xte, yte))   # manual: autolog does not know the test set
run = c.get_run(r.info.run_id)
print("PARAMS (first 4):", dict(list(run.data.params.items())[:4]))
print("METRICS:", {k: round(v, 3) for k, v in run.data.metrics.items()})
print("TAGS (custom ones):", {k: v for k, v in run.data.tags.items() if not k.startswith("mlflow.log-model")and k.startswith(("estimator", "mlflow.runName"))})
print("artifacts:", [a.path for a in c.list_artifacts(r.info.run_id)])
print("git commit tag present:", "mlflow.source.git.commit" in run.data.tags, "(temp dir, not a git repo); data_version tag present:", "data_version" in run.data.tags)

# two fits in one run: the second overwrites the same param keys? -> error or new run?
with mlflow.start_run(run_name="two-fits") as r2:
    LogisticRegression(C=0.5, max_iter=200).fit(Xtr, ytr)
    LogisticRegression(C=5.0, max_iter=200).fit(Xtr, ytr)
print("two fits in one run, C kept:", c.get_run(r2.info.run_id).data.params["C"], "(still the first fit value)")

# GridSearchCV: child runs
gs = GridSearchCV(LogisticRegression(max_iter=200), {"C": [0.1, 1.0]}, cv=3)
with mlflow.start_run(run_name="grid-parent") as r3:
    gs.fit(Xtr, ytr)
runs = mlflow.search_runs(experiment_ids=[exp], output_format="list")
print("runs total:", len(runs))
kids = [x for x in runs if x.data.tags.get("mlflow.parentRunId") == r3.info.run_id]
print("child runs of grid-parent:", len(kids))
print("parent metrics:", {k: round(v, 3) for k, v in c.get_run(r3.info.run_id).data.metrics.items()})
print("parent artifacts:", [a.path for a in c.list_artifacts(r3.info.run_id)])
```

**Output (my run):** mlflow 3.17.2, scikit-learn 1.9.1. Flags and defaults can change between MLflow versions, so check current docs.
```text
2026/10/26 14:07:56 INFO mlflow.store.db.utils: Creating initial MLflow database tables...
2026/10/26 14:07:56 INFO mlflow.store.db.utils: Updating database tables
2026/10/26 14:07:57 INFO mlflow.tracking.fluent: Experiment with name 'q7-autolog' does not exist. Creating a new experiment.
2026/10/26 14:08:01 INFO mlflow.sklearn.utils: Logging the 2 best runs, no runs will be omitted.
mlflow 3.17.2 sklearn 1.9.1
PARAMS (first 4): {'C': '0.5', 'class_weight': 'None', 'dual': 'False', 'fit_intercept': 'True'}
METRICS: {'training_precision_score': 0.943, 'training_recall_score': 0.943, 'training_f1_score': 0.943, 'training_accuracy_score': 0.943, 'training_log_loss': 0.19, 'training_roc_auc': 0.995, 'training_score': 0.943, 'LogisticRegression_score_Xte': 1.0, 'test_accuracy': 1.0}
TAGS (custom ones): {'mlflow.runName': 'single-fit', 'estimator_name': 'LogisticRegression', 'estimator_class': 'sklearn.linear_model._logistic.LogisticRegression'}
artifacts: ['estimator.html', 'metric_info.json', 'training_confusion_matrix.png']
git commit tag present: False (temp dir, not a git repo); data_version tag present: False
two fits in one run, C kept: 0.5 (still the first fit value)
runs total: 5
child runs of grid-parent: 2
parent metrics: {'training_precision_score': 0.935, 'training_recall_score': 0.933, 'training_f1_score': 0.933, 'training_accuracy_score': 0.933, 'training_log_loss': 0.336, 'training_roc_auc': 0.988, 'training_score': 0.933, 'best_cv_score': 0.924}
parent artifacts: ['cv_results.csv', 'estimator.html', 'training_confusion_matrix.png']
```

**Follow-ups:**
- *Which flags would I set?* `log_models=False` while exploring, then log the chosen model explicitly with a signature. `log_datasets=False` unless I want dataset metadata. Check the flags of your version.
- *Autolog or manual?* Autolog for a fast baseline and consistent training metrics, manual for business metrics and test results.
- *Other libraries?* `mlflow.autolog()` also exists for several frameworks. Behaviour differs per flavor.

**Common mistakes:**
- Calling autolog after `fit` and wondering why nothing was logged.
- Trusting `training_score` as model quality. It is training data.
- Fitting several models in one run and reading the params as if they described the last one.

### Q8 ⭐⭐⭐ 🟡 MLflow Model Registry: registered models, versions, aliases and the deprecated stages. Explain how log_model with registered_model_name creates versions, why the old Staging/Production stages are deprecated in favour of aliases such as champion and challenger and tags, how serving code loads models:/name@champion so that promotion means moving an alias (and rollback means moving it back), and what the older models:/name/Production URI did. Show it with a local sqlite registry. The registry needs a database backend, so say why a plain file store is not enough. CI promotion workflows belong to Part 7.
**Asked at:** MLflow Model Registry sources (mlflow.org registry docs, MLflow GitHub issue on stage deprecation, ZenML MLflow registry page, Databricks community and knowledge-base posts; search snippets only, not opened); docs and community posts, not interview reports; MLOps roles using MLflow or Databricks
**Say this first (1 line):** The registry gives each model name numbered versions, and today you promote by moving an alias like `champion` to a version, not by moving it through the deprecated Staging and Production stages.

**Then explain:**
- `log_model(..., registered_model_name="clf")` creates registered model `clf` and version 1. Logging again makes version 2.
- Alias = a movable name pointing to one version, e.g. `champion`, `challenger`. Tags = free key/value notes on a version (`validated=true`).
- Serving code loads `models:/clf@champion` once and never changes. Promote = `set_registered_model_alias("clf","champion",2)`. Rollback = set it back to 1. My run shows predictions flip to the other model and back (`[0]`, `[1]`, `[0]`).
- Stages (`None/Staging/Production/Archived`) are deprecated since MLflow 2.9. In 3.17.2 the old call still ran here and printed a deprecation note, and `models:/clf/Production` still loaded. Treat that as legacy: new code should use aliases, and a later version may remove it (check current docs).
- The registry needs a database backend (SQLite, Postgres...). The plain file store is in maintenance mode and the registry is meant for DB backends (see Q10).
- Failure modes: moving an alias with no gate (any script can swap production), serving code pinned to a version number so rollbacks need a deploy, deleting a version that an alias still points at. Promotion gates and CI belong to Part 7.

**Example:** Version 1 trained with C=0.01, version 2 with C=100. For `x=1.5`, v1 predicts 0 and v2 predicts 1. `champion` points to 1, then to 2, then back to 1. The serving script is the same all three times.

**Code:**
```python
import warnings, mlflow, mlflow.sklearn, numpy as np
from mlflow import MlflowClient
from mlflow.models import infer_signature
from sklearn.linear_model import LogisticRegression

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("q8-registry")
X = np.array([[0.0], [1.0], [2.0], [3.0]]); y = np.array([0, 0, 1, 1])

def train(C):
    with mlflow.start_run():
        m = LogisticRegression(C=C).fit(X, y)
        mlflow.sklearn.log_model(m, name="model", signature=infer_signature(X, m.predict(X)),
                                 registered_model_name="clf")

train(0.01); train(100.0)          # creates version 1 and version 2
c = MlflowClient()
print("versions:", sorted(v.version for v in c.search_model_versions("name='clf'")))

c.set_registered_model_alias("clf", "champion", 1)
c.set_registered_model_alias("clf", "challenger", 2)
c.set_model_version_tag("clf", "2", "validated", "true")
def serve_once(label):
    m = mlflow.pyfunc.load_model("models:/clf@champion")      # serving code never changes
    print(label, "champion -> version", c.get_model_version_by_alias("clf", "champion").version,
          "| predict x=1.5:", m.predict(np.array([[1.5]])).tolist())
serve_once("before:")
c.set_registered_model_alias("clf", "champion", 2)             # promote
serve_once("promoted:")
c.set_registered_model_alias("clf", "champion", 1)             # rollback
serve_once("rolled back:")
print("aliases now:", {v: sorted(c.get_model_version("clf", v).aliases) for v in ("1", "2")})
print("tags on v2:", c.get_model_version("clf", "2").tags)

print("--- old stage API in this version")
try:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        c.transition_model_version_stage("clf", 2, "Production")
    print("transition_model_version_stage: worked; note:", str(w[0].message)[:110] if w else None)
except Exception as e:
    print("transition_model_version_stage:", type(e).__name__, str(e)[:120])
try:
    mlflow.pyfunc.load_model("models:/clf/Production")
    print("models:/clf/Production loaded")
except Exception as e:
    print("models:/clf/Production ->", type(e).__name__, str(e)[:140])
```

**Output (my run):** mlflow 3.17.2 with a local `sqlite:///mlflow.db`. Hosted registries (Databricks, Azure ML, SageMaker): not executed.
```text
2026/10/26 14:08:52 INFO mlflow.store.db.utils: Creating initial MLflow database tables...
2026/10/26 14:08:52 INFO mlflow.store.db.utils: Updating database tables
2026/10/26 14:08:57 INFO mlflow.tracking.fluent: Experiment with name 'q8-registry' does not exist. Creating a new experiment.
Successfully registered model 'clf'.
Created version '1' of model 'clf'.
Registered model 'clf' already exists. Creating a new version of this model...
Created version '2' of model 'clf'.
versions: [1, 2]
before: champion -> version 1 | predict x=1.5: [0]
promoted: champion -> version 2 | predict x=1.5: [1]
rolled back: champion -> version 1 | predict x=1.5: [0]
aliases now: {'1': ['champion'], '2': ['challenger']}
tags on v2: {'validated': 'true'}
--- old stage API in this version
transition_model_version_stage: worked; note: ``mlflow.tracking.client.MlflowClient.transition_model_version_stage`` is deprecated since 2.9.0. Model regist
models:/clf/Production loaded
```

**Follow-ups:**
- *Why aliases over stages?* One name per environment limited you to a fixed set of stages. Aliases are free names and a version can hold several. Tags carry approval status.
- *How do I know who promoted?* Use the platform's audit or access controls. The open-source registry alone is thin here.
- *Can an alias point to two versions?* No. One alias, one version. A version can have many aliases.

**Common mistakes:**
- Building new automation on `transition_model_version_stage`.
- Loading `models:/clf/2` in the app, so every promotion needs a code change.
- Registering without a signature (Q9).

### Q9 ⭐⭐⭐ 🟡 MLflow model signatures and input examples. Explain what a signature is (input and output schema, column-based or tensor-based, optional params), infer_signature, how pyfunc enforces the schema at predict time (missing column, wrong type, safe type casting such as int to float), why a model with no signature can be registered but is harder to serve safely, and what autolog infers. Show a model logged with a signature, a call with a missing column that fails with a clear error, and a call that is auto-cast. Run it locally.
**Asked at:** MLflow official docs and tutorials (mlflow.org tracking, autolog and model registry pages, MLflow 3.1.3 autolog docs, MLflow 2.11 model signature docs, DataTalksClub MLOps Zoomcamp experiment-tracking module, Azure ML MLflow training pages; search snippets only, not opened); docs and course material, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** A signature is the model's input and output schema stored with it, and the pyfunc wrapper checks incoming data against it at predict time, so a missing column or a bad type fails with a clear error instead of a wrong answer.

**Then explain:**
- `infer_signature(X, preds)` builds it from sample data. Column-based schema has names and types (`age: long`, `income: double`). Tensor-based has shapes and dtypes. There can also be optional `params`.
- `input_example` stores a few real rows next to the model, so a person can see the expected format.
- Enforcement in my run (pandas input): missing column raises "Model is missing inputs ['income']"; a string for a number raises "Can not safely convert str to int64"; an extra column is accepted and ignored.
- Type casting is only for safe widening. `int32` into `long` and `int32` or `float32` into `double` worked. `float64` into `int64` failed, and so did `int64` into `float64` (could lose precision for large values). That second one surprised me, so test your own dtypes.
- A model with no signature can be registered and loaded, but nothing checks the input. In my run the sklearn error for the missing column came from sklearn's feature-name check (clear here, but only because sklearn does it). Many models would give a cryptic error or silently wrong output.
- Autolog infers a signature on a best-effort basis (check your version's flags). Some managed registries, such as Unity Catalog, expect signatures (check current docs).
- Failure modes: signature learned from a sample that has no NaNs, so a nullable column breaks later; signature drifts from the real training pipeline; integer columns that sometimes arrive as floats from JSON (a classic production failure).

**Example:** Trained on `age` (int64) and `income` (float64). A JSON request with `{"age": 25.0, "income": 1.5}` fails because 25.0 arrives as float64. The fix is in the caller or an explicit cast in a wrapper, not turning off the check.

**Code:**
```python
import mlflow, mlflow.sklearn, pandas as pd
from mlflow.models import infer_signature
from sklearn.linear_model import LinearRegression

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("q9-signature")
train = pd.DataFrame({"age": [20, 30, 40, 50], "income": [1.0, 2.0, 3.0, 4.0]})   # age int64, income float64
y = [10.0, 20.0, 30.0, 40.0]
model = LinearRegression().fit(train, y)
sig = infer_signature(train, model.predict(train))
print("signature:", sig)

with mlflow.start_run():
    info = mlflow.sklearn.log_model(model, name="with_sig", signature=sig, input_example=train.head(2))
    info2 = mlflow.sklearn.log_model(model, name="no_sig")
print("no_sig model signature:", mlflow.models.get_model_info(info2.model_uri).signature)

m = mlflow.pyfunc.load_model(info.model_uri)
print("input schema:", m.metadata.get_input_schema())

def attempt(label, df):
    try:
        print(label, "->", m.predict(df).round(2).tolist())
    except Exception as e:
        print(label, "-> ERROR:", type(e).__name__, str(e).split("Error: ")[-1].replace("\n", " ")[:150])

attempt("exact types        ", pd.DataFrame({"age": [25], "income": [1.5]}))
attempt("age as float64     ", pd.DataFrame({"age": [25.0], "income": [1.5]}))   # float -> int is NOT safe
attempt("income as int64    ", pd.DataFrame({"age": [25], "income": [2]}))      # int64 -> float64 may lose precision
attempt("age int32 (widens) ", pd.DataFrame({"age": pd.array([25], dtype="int32"), "income": [1.5]}))
attempt("income int32       ", pd.DataFrame({"age": [25], "income": pd.array([2], dtype="int32")}))
attempt("income float32     ", pd.DataFrame({"age": [25], "income": pd.array([1.5], dtype="float32")}))
attempt("missing column     ", pd.DataFrame({"age": [25]}))
attempt("string value       ", pd.DataFrame({"age": ["old"], "income": [1.5]}))
attempt("extra column       ", pd.DataFrame({"age": [25], "income": [1.5], "zip": [1]}))
m2 = mlflow.pyfunc.load_model(info2.model_uri)
print("no-signature model, missing column ->", end=" ")
try: print(m2.predict(pd.DataFrame({"age": [25]})))
except Exception as e: print("ERROR:", type(e).__name__, str(e).replace("\n", " ")[:110])
```

**Output (my run):** mlflow 3.17.2, scikit-learn 1.9.1, pandas 3.0.5. The error text is shortened by the script.
```text
2026/10/26 14:09:40 INFO mlflow.store.db.utils: Creating initial MLflow database tables...
2026/10/26 14:09:40 INFO mlflow.store.db.utils: Updating database tables
2026/10/26 14:09:42 INFO mlflow.tracking.fluent: Experiment with name 'q9-signature' does not exist. Creating a new experiment.
signature: inputs: 
  ['age': long (required), 'income': double (required)]
outputs: 
  [Tensor('float64', (-1,))]
params: 
  None

no_sig model signature: None
input schema: ['age': long (required), 'income': double (required)]
exact types         -> [15.0]
age as float64      -> ERROR: MlflowException Incompatible input types for column age. Can not safely convert float64 to int64.
income as int64     -> ERROR: MlflowException Incompatible input types for column income. Can not safely convert int64 to float64.
age int32 (widens)  -> [15.0]
income int32        -> [15.05]
income float32      -> [15.0]
missing column      -> ERROR: MlflowException Model is missing inputs ['income'].
string value        -> ERROR: MlflowException Incompatible input types for column age. Can not safely convert str to int64.
extra column        -> [15.0]
no-signature model, missing column -> ERROR: ValueError The feature names should match those that were passed during fit. Feature names seen at fit time, yet now miss
```

**Follow-ups:**
- *Does the signature validate value ranges?* No, only names, types and shapes. Range and quality checks need your own validation.
- *Optional columns?* Mark them optional in the schema (check current docs for the syntax).
- *Where do I see the signature?* In the model's `MLmodel` file and the UI.

**Common mistakes:**
- Inferring the signature from a DataFrame with the wrong dtypes (all float after a join).
- Believing "no signature = no problem".
- Disabling schema enforcement when it throws errors instead of fixing the caller.

### Q10 ⭐⭐⭐ 🟡 Where does MLflow keep its data? Compare the local file store (./mlruns), a sqlite or Postgres backend store, an artifact root on local disk or S3-compatible object storage, and a tracking server in between (mlflow server with --backend-store-uri and --default-artifact-root, and proxied artifact access). Explain why the registry needs a database, why recent MLflow 3.x versions treat the file store as maintenance mode and raise an error unless an environment variable allows it (check current docs), and what a team that starts with ./mlruns has to migrate. Show a local sqlite run and a local mlflow server on localhost; S3 and remote servers are not executed.
**Asked at:** MLflow official docs and tutorials (mlflow.org tracking, autolog and model registry pages, MLflow 3.1.3 autolog docs, MLflow 2.11 model signature docs, DataTalksClub MLOps Zoomcamp experiment-tracking module, Azure ML MLflow training pages; search snippets only, not opened); docs and course material, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** MLflow keeps structured run data in a backend store and files in an artifact store; the old `./mlruns` file store is in maintenance mode, so start with SQLite (or Postgres) and put a tracking server in front when a team shares it.

**Then explain:**
- File store: folders and `meta.yaml` files under `./mlruns`. Simple, but no registry, weak search, and in 3.17.2 it raises an error unless `MLFLOW_ALLOW_FILE_STORE=true` (shown). Check current docs for how this changes.
- SQL backend (`sqlite:///mlflow.db`, Postgres, MySQL): one DB with about 65 tables here (runs, params, metrics, registry, and more). Needed for the registry, transactions and safe concurrent writers. SQLite is fine for one person, Postgres for a team.
- Artifact root: a local folder, or S3-compatible and other cloud object storage. Only the location is in the DB.
- Tracking server: `mlflow server --backend-store-uri ... --default-artifact-root ...`. Clients point at `http://host:port`. With proxied artifact access (the server relays artifact uploads), clients do not need cloud credentials. Needs auth in front for real use (reverse proxy, SSO); not shown here.
- Migrating from `./mlruns`: the error names `mlflow migrate-filestore`. I did not run it, so test it on a copy first.
- Failure modes: SQLite on a network share (locks), two teams writing one file store, artifact root on a laptop path that other users cannot reach, a server with no auth on a public IP.

**Example:** The same tiny run went to four places: file store (ok only with the env var), SQLite (`mlflow.db`, 1 run in the `runs` table), local folder artifacts, and a server on `127.0.0.1:5081` whose `/health` said OK and which wrote `a.txt` under its own `art/` folder.

**Code:** The client is the same file for every URI. The server runs in a shell script.
```python
import os, re, sys, mlflow
from mlflow import MlflowClient
uri = sys.argv[1]
mlflow.set_tracking_uri(uri)
mlflow.set_experiment("q10")
with mlflow.start_run() as r:
    mlflow.log_param("where", uri.split(":")[0])
    mlflow.log_metric("m", 1.0)
    mlflow.log_text("hi\n", "a.txt")
    rid = r.info.run_id
c = MlflowClient()
print("ok: runs =", len(mlflow.search_runs(experiment_names=["q10"])), "| artifacts:", [a.path for a in c.list_artifacts(rid)])
u = c.get_run(rid).info.artifact_uri
print("artifact_uri:", re.sub(r"[0-9a-f]{32}", "<run_id>", u.replace(os.getcwd(), "<cwd>")))
```
```bash
export PATH=/tmp/claude-0/ven/v/bin:$PATH MLFLOW_DISABLE_TELEMETRY=true MLFLOW_DISABLE_AGENT_HINT=1
HERE=$PWD
W=$(mktemp -d); cd $W
echo "=== A. plain file store, default settings"
python3 -I $HERE/q10_client.py file:./fs 2>&1 | grep -v -E 'WARN|warn' | tail -1 | cut -c1-330
echo "=== B. file store with MLFLOW_ALLOW_FILE_STORE=true"
MLFLOW_ALLOW_FILE_STORE=true python3 -I $HERE/q10_client.py file:./fs2 2>&1 | grep -v -E 'INFO|WARN|warn'
echo "    layout:"; (cd fs2; find . -maxdepth 2 | sed 's#/[0-9]\{10,\}#/<exp_id>#' | sort | head -6)
echo "=== C. sqlite backend"
python3 -I $HERE/q10_client.py sqlite:///mlflow.db 2>&1 | grep -v -E 'INFO|WARN|warn'
echo "    tables (sample):"; python3 -I -c "
import sqlite3; c=sqlite3.connect('mlflow.db')
t=[r[0] for r in c.execute(\"select name from sqlite_master where type='table'\")]
print(sorted(t)[:9], '... total', len(t))
print('runs in db:', c.execute('select count(*) from runs').fetchone()[0])"
echo "=== D. local tracking server on localhost:5081"
mlflow server --backend-store-uri sqlite:///srv.db --default-artifact-root ./art --host 127.0.0.1 --port 5081 > server.log 2>&1 &
SP=$!
for i in $(seq 1 40); do curl -s http://127.0.0.1:5081/health >/dev/null && break; sleep 1; done
echo -n "    /health -> "; curl -s http://127.0.0.1:5081/health; echo
python3 -I $HERE/q10_client.py http://127.0.0.1:5081 2>&1 | grep -v -E 'INFO|WARN|warn|View'
echo "    artifact files on server disk:"; find art -type f | sed 's#^#    #'
kill $SP; wait $SP 2>/dev/null
```

**Output (my run):** mlflow 3.17.2. Case A shows the real exception (shortened). `<cwd>` stands for a temp dir.
```text
=== A. plain file store, default settings
mlflow.exceptions.MlflowException: The filesystem tracking backend (e.g., './mlruns') is in maintenance mode and will not receive further updates. Please migrate to a database backend (e.g., 'sqlite:///mlflow.db') to access the latest MLflow features. The `mlflow migrate-filestore` tool migrates your existing data losslessly. Se
=== B. file store with MLFLOW_ALLOW_FILE_STORE=true
ok: runs = 1 | artifacts: ['a.txt']
artifact_uri: file://<cwd>/fs2/713620244018705718/<run_id>/artifacts
    layout:
.
./.trash
./0
./0/meta.yaml
./<exp_id>
./<exp_id>/fc9d10d4e598427f9f2439725e9ca0ec
=== C. sqlite backend
ok: runs = 1 | artifacts: ['a.txt']
artifact_uri: <cwd>/mlruns/1/<run_id>/artifacts
    tables (sample):
['alembic_version', 'assessments', 'budget_policies', 'datasets', 'endpoint_bindings', 'endpoint_model_mappings', 'endpoint_tags', 'endpoints', 'entity_associations'] ... total 65
runs in db: 1
=== D. local tracking server on localhost:5081
    /health -> OK
ok: runs = 1 | artifacts: ['a.txt']
artifact_uri: <cwd>/art/1/<run_id>/artifacts
    artifact files on server disk:
    art/1/26a13aecd49645eeba86e757b8e9d1b1/artifacts/a.txt
```
Not executed: S3 or other cloud artifact roots, Postgres, remote servers, authentication, and `mlflow migrate-filestore`. Validation that did run: SQLite backend, file store, and a localhost server with an uploaded artifact.

**Follow-ups:**
- *Why not just share the SQLite file?* Concurrent writers and network file systems break it. Use Postgres behind a server.
- *Where do large models go?* The artifact store, not the DB.
- *Managed MLflow?* Databricks, Azure ML and SageMaker offer hosted MLflow. Not executed here, check each vendor's docs.

**Common mistakes:**
- Treating the artifact store and backend store as one thing.
- Starting a server without `--default-artifact-root` and then finding artifacts in a path clients cannot read.
- Setting `MLFLOW_ALLOW_FILE_STORE=true` forever instead of migrating.

### Q11 ⭐⭐⭐ 🟡 Compare experiments and pick the best run. You ran 30 training runs with different learning rates and feature sets. Show how to query them (mlflow.search_runs with a filter string and order_by, MlflowClient.search_runs), how to use parent and child runs for a tuning job, what makes runs comparable (same data split, same metric definition, tags for data version), how the UI compare view helps, and why picking the highest validation score of 30 tries is optimistic (selection bias, use a held-out test set once). Run a small tuning loop locally and print the best run's params.
**Asked at:** MLflow official docs and tutorials (mlflow.org tracking, autolog and model registry pages, MLflow 3.1.3 autolog docs, MLflow 2.11 model signature docs, DataTalksClub MLOps Zoomcamp experiment-tracking module, Azure ML MLflow training pages; search snippets only, not opened); docs and course material, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** I log every trial as a child run under one parent run, query them with a filter and order_by, and pick the best on validation. Then I score that one winner on a held-out test set, once, because the best of 30 is an optimistic number.

**Then explain:**
- **Structure:** one parent run for the tuning job (`start_run`), one nested child run per trial (`nested=True`). In the UI the parent expands to its children. Child runs carry the tag `mlflow.parentRunId`, so I can filter on it.
- **Query:** `mlflow.search_runs(filter_string=..., order_by=[...])` returns a pandas DataFrame. `MlflowClient().search_runs(...)` returns `Run` objects. Filter syntax is SQL-like: `metrics.val_auc > 0.5 and tags.data_version = 'v1'`. Params are stored as strings, so compare them as strings.
- **Comparable means:** same train/validation split, same metric definition (AUC on the same rows), same data version, same code. I enforce this with a fixed split seed and tags (`data_version`, `metric_def`). If any of these differ, a column in the compare table is not comparing like with like.
- **UI compare view:** select runs, click Compare. You get a parallel-coordinates plot, a scatter of param vs metric, and a table of diffs. It is good for spotting that "lr above 0.1 always hurts". It does not fix a bad experiment design.
- **Selection bias:** the max of 30 noisy scores is biased upward. Some of the lead is luck. So the validation score of the winner is not my estimate of production performance. The estimate comes from a test set I touch once, after the choice is made. Failure mode: peeking at test for every trial turns the test set into a second validation set.

**Example:** 3 feature sets x 5 learning rates = 15 child runs (I cap at 15 here to keep it small; 30 works the same). The best child is `all20`, lr 0.001. Its validation AUC is the biggest of 15 numbers. In the second script, 30 models with NO skill (random scores) still give a best validation AUC well above 0.5 just from picking the max. A fresh test set shows no skill.

**Code:**
```python
# ---- q11_tune.py ----
# Q11: tuning loop, parent + child runs, search_runs, held-out test once
import warnings; warnings.filterwarnings("ignore")
import itertools, mlflow
from mlflow import MlflowClient
from sklearn.datasets import make_classification
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("tune-demo")
X, y = make_classification(n_samples=1500, n_features=20, n_informative=6, flip_y=0.1, random_state=0)
Xtv, Xte, ytv, yte = train_test_split(X, y, test_size=0.25, random_state=1)   # test: touch ONCE
Xtr, Xva, ytr, yva = train_test_split(Xtv, ytv, test_size=0.3, random_state=2) # same split for all runs
feature_sets = {"first5": list(range(5)), "first10": list(range(10)), "all20": list(range(20))}
lrs = [0.0001, 0.001, 0.01, 0.1, 1.0]
with mlflow.start_run(run_name="tuning-job") as parent:
    mlflow.set_tag("data_version", "synthetic-v1")
    for (fs, cols), lr in itertools.product(feature_sets.items(), lrs):
        with mlflow.start_run(run_name=f"{fs}-lr{lr}", nested=True):
            mlflow.set_tags({"data_version": "synthetic-v1", "metric_def": "val_auc"})
            mlflow.log_params({"lr": lr, "features": fs})
            m = SGDClassifier(loss="log_loss", learning_rate="constant", eta0=lr, random_state=0, max_iter=50)
            m.fit(Xtr[:, cols], ytr)
            mlflow.log_metric("val_auc", roc_auc_score(yva, m.decision_function(Xva[:, cols])))

exp = mlflow.get_experiment_by_name("tune-demo")
pid = parent.info.run_id
df = mlflow.search_runs([exp.experiment_id],
        filter_string=f"tags.mlflow.parentRunId = '{pid}' and tags.data_version = 'synthetic-v1' and metrics.val_auc > 0.5",
        order_by=["metrics.val_auc DESC"], max_results=3)
print(df[["tags.mlflow.runName", "params.lr", "params.features", "metrics.val_auc"]].to_string(index=False))

kids = MlflowClient().search_runs([exp.experiment_id], f"tags.mlflow.parentRunId = '{pid}'",
                                  order_by=["metrics.val_auc DESC"])
best = kids[0]
print("child runs:", len(kids))
print("best params:", best.data.params, "val_auc=%.4f" % best.data.metrics["val_auc"])
cols = feature_sets[best.data.params["features"]]
m = SGDClassifier(loss="log_loss", learning_rate="constant", eta0=float(best.data.params["lr"]), random_state=0, max_iter=50).fit(Xtr[:, cols], ytr)
print("test_auc (used once) = %.4f" % roc_auc_score(yte, m.decision_function(Xte[:, cols])))

# ---- q11_bias.py (separate script) ----
# 30 useless "models" (random scores): best validation AUC of 30 looks good, test AUC stays ~0.5
import numpy as np
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0)
yva, yte = rng.integers(0, 2, 200), rng.integers(0, 2, 200)
val = [roc_auc_score(yva, rng.normal(size=200)) for _ in range(30)]
best = int(np.argmax(val))
print("best of 30 val AUC: %.3f" % max(val))
print("same pick on fresh test AUC: %.3f" % roc_auc_score(yte, rng.normal(size=200)))
```

**Output (my run):** MLflow 3.17.2, sklearn 1.9.1, sqlite store. First script, then the second script.
```
tags.mlflow.runName params.lr params.features  metrics.val_auc
      all20-lr0.001     0.001           all20         0.852303
     all20-lr0.0001    0.0001           all20         0.851813
        all20-lr1.0       1.0           all20         0.844176
child runs: 15
best params: {'lr': '0.001', 'features': 'all20'} val_auc=0.8523
test_auc (used once) = 0.8716
best of 30 val AUC: 0.576
same pick on fresh test AUC: 0.440
```
In this run test AUC (0.8716) happened to come out above validation (0.8523). That is luck of a small split and does not disprove the bias. The second script shows the bias without any model luck. A 15-run grid has a smaller bias than a 300-run one, so more trials means more caution.

**Follow-ups:**
- *Do I need a parent run?* No, tags work. But a parent gives a clean UI grouping and one place for job-level tags and the final test metric.
- *How do I reduce selection bias?* Cross-validation inside the search, a final untouched test set, and fewer, smarter trials. For close scores, say they are tied, and prefer the simpler or cheaper model.
- *Optuna or Hyperopt?* They suggest the trials. MLflow still logs them. The logging pattern is the same.

**Common mistakes:**
- Comparing runs trained on different splits or data versions.
- Reporting the best validation score as the expected production score.
- Evaluating on the test set inside the loop.
- Filtering params as numbers (`params.lr > 0.01`). Params are strings.
- Forgetting `nested=True`, so child runs fail or replace the parent.

### Q12 ⭐⭐⭐ 🟡 Weights & Biases basics for an ML engineer: wandb.init, config, wandb.log, run, project, entity, artifacts and the dashboard. Compare with MLflow (hosted SaaS first, rich dashboards, sweeps built in, closed source with self-host options; MLflow open source and self-hosted first; check current plans). Show the same training loop instrumented with wandb in offline mode (WANDB_MODE=offline), what files appear locally, and how wandb sync uploads them later. Live logging to wandb.ai needs an account and network and is not executed here.
**Asked at:** Weights & Biases sources (techinterview.org 'Weights & Biases Interview Guide', KDnuggets 'Weights & Biases crash course', TWIML podcast on managing ML artifacts, wandb.ai articles; search snippets only, not opened); guide and docs, not verified candidate reports; ML engineer and MLOps roles at AI-lab and product companies
**Say this first (1 line):** W&B is a hosted experiment tracker: `wandb.init` starts a run inside a project, `wandb.log` streams metrics, `config` holds hyperparameters, and artifacts version datasets and models. Same job as MLflow tracking, with a stronger dashboard and built-in sweeps.

**Then explain:**
- **Vocabulary:** *entity* is the user or team that owns the data. *Project* groups runs. *Run* is one execution. *config* is the inputs (lr, epochs). *summary* is the final value per metric. *Artifact* is a versioned file or folder with lineage (which run produced it, which run used it).
- **Versus MLflow:** W&B is SaaS first with rich dashboards, reports, sweeps (`wandb sweep`, `wandb agent`) and team features. It is closed source, and self-hosting exists (check current plans and terms). MLflow is open source and self-hosted first, with a model registry that is a core feature. Many teams use MLflow for the registry and one of the two for dashboards. Check current docs for pricing and limits.
- **Offline mode:** `WANDB_MODE=offline` or `mode="offline"` writes everything to a local `wandb/offline-run-...` folder and uploads nothing. Later `wandb sync <run dir>` uploads it. Good for clusters with no internet.
- **Failure modes:** no `wandb.finish()` leaves the run open (in scripts it closes on exit, in notebooks do it yourself). Offline runs never appear online until synced. Logging every step of a big job floods storage, so log every N steps. Never commit the API key.

**Example:** the same loop as the MLflow one in Q11: one config, five epochs, one metric per epoch, then a small dataset artifact. In MLflow the equivalents are `log_params`, `log_metric(step=)`, and `log_artifact`.

| W&B | MLflow |
|---|---|
| `wandb.init(project=, config=)` | `set_experiment`, `start_run`, `log_params` |
| `wandb.log({"loss": x})` | `mlflow.log_metric("loss", x, step=i)` |
| `run.summary[...]` | last metric value or a final `log_metric` |
| `wandb.Artifact` + `log_artifact` | `log_artifact`, `log_input`, model registry |
| sweeps | external (Optuna, Hyperopt) + MLflow logging |

**Code:**
```python
import warnings; warnings.filterwarnings("ignore")
import wandb
from sklearn.datasets import make_classification
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
X, y = make_classification(n_samples=800, n_features=10, random_state=0)
Xtr, Xva, ytr, yva = train_test_split(X, y, random_state=1)
run = wandb.init(project="demo-proj", config={"lr": 0.01, "epochs": 5}, dir=".", mode="offline", name="sgd-1")
cfg = run.config
m = SGDClassifier(loss="log_loss", learning_rate="constant", eta0=cfg.lr, random_state=0)
for epoch in range(cfg.epochs):
    m.partial_fit(Xtr, ytr, classes=[0, 1])
    wandb.log({"epoch": epoch, "val_auc": roc_auc_score(yva, m.decision_function(Xva))})
run.summary["final_val_auc"] = roc_auc_score(yva, m.decision_function(Xva))
art = wandb.Artifact("train-data", type="dataset", metadata={"rows": len(Xtr)})
with art.new_file("note.txt") as f: f.write("synthetic data, seed 0\n")
run.log_artifact(art)
print("mode:", run.settings.mode, "| project:", run.project, "| entity:", run.entity, "| run id:", run.id)
run.finish()
```
```bash
# upload later, from a machine with network and a login (NOT executed here)
wandb login            # or set WANDB_API_KEY
wandb sync wandb/offline-run-*   # uploads one or more offline run dirs
```

**Output (my run):** wandb 0.31.0, offline mode, python 3.13. The first script ran; the folder listing is `find` plus `ls wandb` afterwards. `wandb sync`, live logging, hosted artifacts and sweeps were not executed: they need an account and network. I only confirmed `wandb sync --help` works offline.
```
mode: offline | project: demo-proj | entity:  | run id: g7jqtbto
./wandb/offline-run-20261026_141334-g7jqtbto/files/output.log
./wandb/offline-run-20261026_141334-g7jqtbto/files/requirements.txt
./wandb/offline-run-20261026_141334-g7jqtbto/logs/debug-internal.log
./wandb/offline-run-20261026_141334-g7jqtbto/logs/debug.log
./wandb/offline-run-20261026_141334-g7jqtbto/run-g7jqtbto.wandb
debug-internal.log
debug.log
latest-run
offline-run-20261026_141334-g7jqtbto
```
The `.wandb` file is the binary log that `wandb sync` reads. Entity is empty offline because no login exists, so the run has no owner until you sync.

**Follow-ups:**
- *How do sweeps work?* A sweep config (method grid/random/bayes, parameter ranges) is registered with the server. One or more `wandb agent` processes pull the next parameter set and call your training function. Needs the server, so not executed here.
- *Is my data uploaded?* Metrics, config and logged files are. Artifact reference mode can point at your own bucket instead of copying (check current docs).
- *Would you pick W&B or MLflow?* Depends on constraints: data must stay on-prem or you want a free registry, MLflow. Team wants fast dashboards and sweeps with no ops, W&B.

**Common mistakes:**
- Saying "W&B replaces MLflow" with no mention of registry, hosting, or cost.
- Putting the API key in code or Git.
- Expecting offline runs to show online without `wandb sync`.
- Logging each batch for a multi-day job.

### Q13 ⭐⭐⭐ 🟡 DVC versus Git LFS versus MLflow artifacts: which one for what. Compare where the bytes live, how a version is pinned (pointer file, LFS pointer, run artifact URI), pipelines and reproducibility, storage backends, cost and quota behaviour (Git LFS bandwidth and storage limits on hosts, check current terms), and team workflow. Give a decision table for a 5 GB dataset, a 300 MB model checkpoint, a nightly metrics file and a plot. Show the .gitattributes line for LFS and a dvc add for the same file; LFS push to a host is not executed.
**Asked at:** DVC official docs and tutorials (dvc.org 'Metrics, Plots, and Parameters' get-started page, OneUptime 'How to Configure DVC for Data Versioning' 2026, UCL data version control lecture, DAGsHub pipelines tutorial; search snippets only, not opened); docs and tutorials, not interview reports; MLOps and data science roles
**Say this first (1 line):** Git LFS swaps big files for small pointers inside Git and keeps the bytes on the Git host. DVC keeps its own pointer file and cache and stores the bytes in storage you choose, and it adds pipelines. MLflow artifacts store files per run and are for outputs of runs, not for versioning inputs.

**Then explain:**
- **Where the bytes live:** LFS uses the Git host's LFS store. DVC uses a remote you pick (S3, GCS, Azure, SSH, local or NFS path; check current docs for the list). MLflow uses the artifact root of the tracking server (a folder or bucket).
- **How a version is pinned:** LFS has a pointer (oid sha256 plus size) committed in the file's place. DVC has a `.dvc` file or `dvc.lock` with an md5 per output. MLflow has a run's artifact URI, pinned only if you record the run id.
- **Pipelines and reproducibility:** only DVC defines stages (`dvc.yaml`), tracks deps and outputs, and re-runs what changed. LFS and MLflow do not.
- **Cost and quota:** LFS hosts commonly cap storage and bandwidth, and every clone or CI checkout downloads through LFS. Check the current terms of your host. With DVC the cost is your own storage bill, and you control egress. MLflow artifact cost is the same as DVC remote cost.
- **Team workflow:** LFS is nearly invisible after `git lfs install`. DVC needs `dvc push` and `dvc pull` besides Git, which is more steps and a classic "forgot to push" failure. MLflow is for sharing and comparing results, not for `git checkout` of a data version.

**Example:** decision table.

| Asset | Pick | Why |
|---|---|---|
| 5 GB dataset, changes monthly, feeds a pipeline | DVC | Needs pinned versions, dedup, your own bucket, and stage tracking. Likely too large or too costly for host LFS quotas. |
| 300 MB model checkpoint from a training run | MLflow artifact (or registry), with run id and data hash recorded | It is an output of a run, linked to params and metrics. DVC `-o` also works if the pipeline is the source of truth. |
| Nightly metrics file (tiny JSON) | Plain Git, or DVC `-M` with `cache: false` | Small text diffs well in Git. Metrics in Git make `dvc metrics diff` work. |
| A plot (PNG/HTML) | MLflow `log_figure`, or a DVC plot output | Artifact of a run. If it is in a report in Git, track it in Git when small. |
| A few 20 MB sample images for tests | LFS or plain Git | Few, small, no pipeline. LFS is simple. |

**Code:**
```bash
set -e
head -c 2000000 /dev/zero | tr '\0' 'a' > /tmp/big.bin      # stand-in for a big file
echo "=== Git LFS (local only, no host, no push)"
mkdir lfs && cd lfs && git init -q . && git lfs install --local >/dev/null
git lfs track "*.bin"
cp /tmp/big.bin . && git add .gitattributes big.bin && git commit -qm lfs
echo "--- .gitattributes"; cat .gitattributes
echo "--- what Git stores (the pointer)"; git cat-file -p HEAD:big.bin
git lfs ls-files
cd ..
echo "=== DVC"
mkdir dvc && cd dvc && git init -q . && dvc init -q
cp /tmp/big.bin . && dvc add big.bin 2>&1 | grep -v -e '^$' -e 'track' -e 'git add' -e autostage
echo "--- big.bin.dvc"; cat big.bin.dvc
echo "--- cache"; find .dvc/cache -type f
```

**Output (my run):** git-lfs 3.4.1 and dvc 3.67.1. The LFS part ran fully local: track, add, commit, and look at the pointer. `git push` of LFS objects to a host and quota behaviour were not executed (no host). DVC printed its autostage hint, which I filtered.
```
=== Git LFS (local only, no host, no push)
Tracking "*.bin"
--- .gitattributes
*.bin filter=lfs diff=lfs merge=lfs -text
--- what Git stores (the pointer)
version https://git-lfs.github.com/spec/v1
oid sha256:bcf7f9d1b4311c3352e60502255ce09a6744df84e8f2c89f79c4b5d74933a95a
size 2000000
bcf7f9d1b4 * big.bin
=== DVC
To enable auto staging, run:
--- big.bin.dvc
outs:
- md5: 2a915e52d86d42e58e580f4073120a6b
  size: 2000000
  hash: md5
  path: big.bin
--- cache
.dvc/cache/files/md5/2a/915e52d86d42e58e580f4073120a6b
```
The 2 MB file in LFS is a 3-line pointer in Git. In DVC it is a 6-line `.dvc` file, and `.gitignore` keeps the data itself out of Git.

**Follow-ups:**
- *Can they be combined?* Yes, but avoid both on one file. LFS for a few binary assets in the repo, DVC for datasets and pipelines.
- *What if I have no cloud?* A DVC remote can be a shared path or SSH host. Local path remotes work for this (Q19, Q20).
- *Why not store datasets in Git directly?* Git stores every version forever in history, clones get slow, and diffs are meaningless for binaries.

**Common mistakes:**
- Choosing LFS for multi-GB data and hitting host quotas.
- Treating MLflow artifacts as dataset versions with no record of which run holds which data.
- Putting the same file under both LFS and DVC.
- Forgetting `dvc push`, so teammates get a pointer with no bytes.

### Q14 ⭐⭐⭐ 🟡 DVC and MLflow together: who owns what? A teammate says 'we do not need both'. Explain the split (DVC versions data and defines the reproducible pipeline through Git; MLflow records runs, compares them and registers models; W&B overlaps with the MLflow side), where they overlap (metrics, params, experiments, model files), and a clean repo layout where dvc.yaml runs train.py, train.py logs to MLflow, and the MLflow run stores the Git SHA and DVC data hash. Build this tiny setup, run dvc repro, and show one MLflow run plus the dvc.lock entry. Remote servers are not executed.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** We need both, because they do different jobs. DVC versions data and defines the reproducible pipeline through Git. MLflow records each run, compares runs, and registers models. The glue is two tags on every MLflow run: the Git SHA and the DVC data hash.

**Then explain:**
- **DVC owns:** `data.csv.dvc` (data pointer), `dvc.yaml` (stages), `dvc.lock` (exact hashes of deps and outs), `params.yaml`. Everything is in Git, bytes go to a DVC remote. Question it answers: "can I rebuild this exactly?"
- **MLflow owns:** run history (params, metrics over time, artifacts), compare UI, model registry with versions and aliases. Question it answers: "which of my 200 runs was best, and which model is in production?"
- **Overlap:** both can store params, metrics and model files. W&B overlaps with the MLflow side. Pick one place as the system of record for each: pipeline definition and data in DVC, run comparison and registry in MLflow. Duplicated metrics are fine (`metrics.json` for `dvc metrics diff` in a PR, MLflow for long-term comparison), as long as both come from the same `train.py`.
- **The link:** `dvc.yaml` runs `train.py`. `train.py` reads `params.yaml`, reads the hash from `data.csv.dvc`, calls `git rev-parse HEAD`, and logs both as MLflow tags. Now from any run you can get back to the exact data and code.
- **Failure mode:** the SHA logged is HEAD, not "the commit of this result". If you run `dvc repro` with uncommitted changes, HEAD is the old commit. I log `git_dirty` too. The run is only fully traceable when the tree is clean. Also, DVC does not know about MLflow. Re-running `dvc repro` with no changes skips the stage, so no new MLflow run appears (that is correct).

**Example:** layout.
```
repo/
  data.csv.dvc     # pointer, in Git
  dvc.yaml         # stage: train -> python train.py
  dvc.lock         # hashes of what the last repro used
  params.yaml      # train.C
  train.py         # logs to MLflow + writes metrics.json
  mlflow.db        # local tracking store, NOT in Git (.gitignore)
```
Flow: change `params.yaml` -> `dvc repro` -> `train.py` runs -> new MLflow run with tag `dvc_data_md5` and `git_sha` -> `dvc.lock` changes -> commit.

**Code:** `train.py` (also used in Q15) and the setup script that builds the repo and runs `dvc repro`.
```python
import json, subprocess, warnings, yaml
warnings.filterwarnings("ignore")
import mlflow, pandas as pd
from mlflow import MlflowClient
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

def sh(*a): return subprocess.run(a, capture_output=True, text=True).stdout.strip()

params = yaml.safe_load(open("params.yaml"))["train"]
df = pd.read_csv("data.csv")
data_md5 = yaml.safe_load(open("data.csv.dvc"))["outs"][0]["md5"]   # DVC hash of the input
sha, dirty = sh("git", "rev-parse", "HEAD"), bool(sh("git", "status", "--porcelain", "--", "train.py", "params.yaml", "data.csv.dvc"))

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("dvc-plus-mlflow")
with mlflow.start_run() as run:
    mlflow.set_tags({"git_sha": sha, "git_dirty": str(dirty), "dvc_data_md5": data_md5})
    mlflow.log_params(params)
    mlflow.log_input(mlflow.data.from_pandas(df, source="data.csv", name="train-data"), context="training")
    model = LogisticRegression(C=params["C"], max_iter=200)
    acc = cross_val_score(model, df[["x1", "x2"]], df["y"], cv=5).mean()
    mlflow.log_metric("cv_acc", acc)
    model.fit(df[["x1", "x2"]], df["y"])
    mlflow.sklearn.log_model(model, name="model", registered_model_name="churn")
    v = max(int(m.version) for m in MlflowClient().search_model_versions("name='churn'"))
    for k, val in {"git_sha": sha, "dvc_data_md5": data_md5}.items():
        MlflowClient().set_model_version_tag("churn", str(v), k, val)
json.dump({"cv_acc": round(acc, 4)}, open("metrics.json", "w"))
print("run", run.info.run_id, "-> churn v%d" % v)
```
```bash
set -e
P=/home/user/case_studies/interviews/scratch/B4P04_Q11-20/code/q14_proj
git init -q . && dvc init -q && cp $P/train.py $P/lineage.py .
python -I -c "
import numpy as np, pandas as pd
r = np.random.default_rng(0); x = r.normal(size=(300, 2))
y = (x[:,0] + 0.5*x[:,1] + r.normal(scale=0.7, size=300) > 0).astype(int)
pd.DataFrame({'x1': x[:,0], 'x2': x[:,1], 'y': y}).to_csv('data.csv', index=False)"
printf 'train:\n  C: 1.0\n' > params.yaml
dvc add data.csv >/dev/null 2>&1
dvc stage add -q -n train -d train.py -d data.csv -p train.C -M metrics.json python train.py
cat dvc.yaml
printf 'mlflow.db\nmlruns/\n' >> .gitignore
git add -A && git commit -qm "data v1 + pipeline"
echo "=== dvc repro"; dvc repro 2>&1 | grep -v -e '^$' -e 'git add' -e autostage -e 'To track' | tail -8
echo "=== dvc.lock"; cat dvc.lock
git add -A && git commit -qm "first model"
echo "=== mlflow run (search_runs)"
python -I -c "
import mlflow; mlflow.set_tracking_uri('sqlite:///mlflow.db')
df = mlflow.search_runs(experiment_names=['dvc-plus-mlflow'])
r = df.iloc[0]
for k in ['params.C','metrics.cv_acc','tags.git_sha','tags.git_dirty','tags.dvc_data_md5']: print(k, '=', r[k])"
echo "=== lineage for churn v1"
python -I lineage.py churn 1
echo "=== change params -> new model version"
sed -i 's/C: 1.0/C: 0.1/' params.yaml; dvc repro 2>&1 | grep -e Running -e Updating; git add -A; git commit -qm "C=0.1"
python -I lineage.py churn 2
```

**Output (my run):** dvc 3.67.1, mlflow 3.17.2 (sqlite store), local only. No DVC remote was configured here; no remote server was used. I filtered MLflow INFO lines and DVC hints.
```
stages:
  train:
    cmd: python train.py
    deps:
    - data.csv
    - train.py
    params:
    - train.C
    metrics:
    - metrics.json:
        cache: false
=== dvc repro
Successfully registered model 'churn'.
Created version '1' of model 'churn'.
run f66c32dd3324418eb28e3d986c1eee0f -> churn v1
Generating lock file 'dvc.lock'
Updating lock file 'dvc.lock'
To enable auto staging, run:
Use `dvc push` to send your updates to remote storage.
=== dvc.lock
schema: '2.0'
stages:
  train:
    cmd: python train.py
    deps:
    - path: data.csv
      hash: md5
      md5: bd1cba7e3a139900c201e9cbd437e476
      size: 12390
    - path: train.py
      hash: md5
      md5: c9ec64cf03ab10b677bfb27a5cf3e7d6
      size: 1618
    params:
      params.yaml:
        train.C: 1.0
    outs:
    - path: metrics.json
      hash: md5
      md5: fa2191aa5a98b12125eea68d9ebea253
      size: 18
=== mlflow run (search_runs)
params.C = 1.0
metrics.cv_acc = 0.8666666666666666
tags.git_sha = a745da060a18ab1edddb3c0267f4d1de52f1862f
tags.git_dirty = False
tags.dvc_data_md5 = bd1cba7e3a139900c201e9cbd437e476
=== lineage for churn v1
model        : churn v1  (run f66c32dd)
git commit   : a745da060a  dirty=False
data md5 tag : bd1cba7e3a139900c201e9cbd437e476
data md5 git : bd1cba7e3a139900c201e9cbd437e476   match=True
params       : {'C': '1.0'}
logged input : [('train-data', '987c1572')]
=== change params -> new model version
Running stage 'train':
Updating lock file 'dvc.lock'
model        : churn v2  (run ea4fafd0)
git commit   : 77a413c584  dirty=True
data md5 tag : bd1cba7e3a139900c201e9cbd437e476
data md5 git : bd1cba7e3a139900c201e9cbd437e476   match=True
params       : {'C': '0.1'}
logged input : [('train-data', '987c1572')]
```
Read the `dvc.lock` entry: it pins the md5 of `data.csv`, `train.py`, the param, and the output. Read the MLflow run: same data md5 as a tag. The SHA in the run is the commit before the result was committed, which is normal. Output of the second part shows `dirty=True` for version 2, since I had changed `params.yaml` without committing before `dvc repro`.

**Follow-ups:**
- *Can DVC alone do everything?* It has `dvc exp` and metrics diff (Q17). It has no registry and a basic UI. MLflow alone cannot define a stage graph or pin data hashes by itself.
- *Can MLflow log the DVC data directly?* `mlflow.log_input` with a dataset, and tags for the hash. MLflow does not replace the data store.
- *Where does CI fit?* CI runs `dvc pull` and `dvc repro`, or tests only. Part 7 owns that.

**Common mistakes:**
- Committing `mlflow.db` or `mlruns/` to Git.
- Logging only the Git SHA and forgetting the data hash.
- Ignoring the dirty flag, then trusting a SHA that does not match the code that ran.
- Two systems of record for the same thing (model registered in both).

### Q15 ⭐⭐⭐ 🔴 Dataset and model lineage: for any production model, answer 'which data, which code, which parameters?'. Explain how you wire Git commit, DVC data hash, params and MLflow run together (log the commit SHA and the .dvc or dvc.lock hash as MLflow tags, mlflow.log_input with a dataset, set tags on the registered version), how W&B artifacts record lineage automatically, and what lineage still misses (upstream raw tables, feature code outside Git). Build a small script that records the tags in a run and then, given a model version, prints the dataset hash and commit. Run it locally with DVC and MLflow.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** I write three facts onto every training run and every registered model version: the Git commit, the DVC data hash, and the params. Then a model version answers "which data, code, params?" in one lookup, and I can re-check it against Git.

**Then explain:**
- **What to record:** `git_sha` (+ `git_dirty`), `dvc_data_md5` (from the `.dvc` file or `dvc.lock`), params, and the dataset via `mlflow.log_input(mlflow.data.from_pandas(...))`. Put the same tags on the **model version** (`set_model_version_tag`), since people look at the registry, not at runs.
- **Look-up path:** model version -> run id -> tags and params -> `git show <sha>:data.csv.dvc` -> md5. If the md5 in Git equals the tag, the lineage holds. Then `git checkout <sha>`, `dvc pull`, `dvc repro` rebuilds it.
- **W&B way:** artifacts record lineage automatically. A run `use_artifact` on a dataset and `log_artifact` on a model, and the artifact graph shows both sides. It only knows what went through artifacts (not run here, needs the hosted service).
- **What lineage still misses:** the upstream raw tables the CSV came from (the query or the warehouse snapshot), feature code that lives outside Git, library versions and hardware unless logged, random seeds, and dirty trees. Say so out loud in an interview.
- **Failure mode:** tags are free text, nobody checks them. Without a check (like the script below that compares the tag with Git), lineage can be quietly wrong.

**Example:** model `churn` v1 was trained at commit `a745da060a` on data md5 `bd1cba7e...`. Tomorrow someone asks "what data?". The script prints the md5 from the tag and from Git at that commit, and they match.

**Code:** `train.py` is in Q14. This is the lookup script.
```python
# usage: python lineage.py <registered-model> <version>
import subprocess, sys, yaml
import mlflow
from mlflow import MlflowClient
mlflow.set_tracking_uri("sqlite:///mlflow.db")
name, ver = sys.argv[1], sys.argv[2]
c = MlflowClient()
mv = c.get_model_version(name, ver)
run = c.get_run(mv.run_id)
sha = mv.tags["git_sha"]
# ask Git what data.csv.dvc said AT THAT COMMIT, and compare with the tag
blob = subprocess.run(["git", "show", f"{sha}:data.csv.dvc"], capture_output=True, text=True).stdout
git_md5 = yaml.safe_load(blob)["outs"][0]["md5"]
print(f"model        : {name} v{ver}  (run {mv.run_id[:8]})")
print(f"git commit   : {sha[:10]}  dirty={run.data.tags['git_dirty']}")
print(f"data md5 tag : {mv.tags['dvc_data_md5']}")
print(f"data md5 git : {git_md5}   match={git_md5 == mv.tags['dvc_data_md5']}")
print(f"params       : {run.data.params}")
print(f"logged input : {[ (d.dataset.name, d.dataset.digest) for d in run.inputs.dataset_inputs ]}")
```
```bash
python -I lineage.py churn 1
```

**Output (my run):** same project as Q14, same run. The first block is `churn` v1 (lines before "change params"). The second is v2 after a param change, run with an uncommitted params file.
```
=== lineage for churn v1
model        : churn v1  (run f66c32dd)
git commit   : a745da060a  dirty=False
data md5 tag : bd1cba7e3a139900c201e9cbd437e476
data md5 git : bd1cba7e3a139900c201e9cbd437e476   match=True
params       : {'C': '1.0'}
logged input : [('train-data', '987c1572')]
=== change params -> new model version
Running stage 'train':
Updating lock file 'dvc.lock'
model        : churn v2  (run ea4fafd0)
git commit   : 77a413c584  dirty=True
data md5 tag : bd1cba7e3a139900c201e9cbd437e476
data md5 git : bd1cba7e3a139900c201e9cbd437e476   match=True
params       : {'C': '0.1'}
logged input : [('train-data', '987c1572')]
```
Version 2 shows `dirty=True` and the commit of the previous state. That is the honest answer: the tag says the code and params were not fully committed. In a real pipeline, CI should refuse to register a model from a dirty tree.

**Follow-ups:**
- *What if the data is in a warehouse, not a CSV?* Record a snapshot id or query timestamp, and the SQL, as tags. Delta time travel and lakeFS are alternatives (not run here).
- *Standards?* OpenLineage is a standard for lineage events (not run here; check current docs).
- *Why also use log_input?* It gives a dataset digest in the MLflow UI and a link from run to dataset.

**Common mistakes:**
- Tagging the run but not the registered version.
- Logging the SHA but not the data hash.
- Not checking the dirty flag.
- Claiming "full lineage" when raw upstream tables and feature code are not covered.

### Q16 ⭐⭐ 🟡 How the DVC cache works. Explain content-addressable storage (files stored under .dvc/cache by md5 hash), why identical files are stored once, link types (reflink, hardlink, symlink, copy) and the trade-off between disk use and safety when you edit a linked file, what dvc checkout does, dvc status versus dvc status -c, and dvc gc and what it deletes (workspace-referenced hashes are kept; check flags). Show the cache layout after dvc add and a dvc gc dry demonstration. Run it locally.
**Asked at:** DVC official docs and tutorials (dvc.org 'Metrics, Plots, and Parameters' get-started page, OneUptime 'How to Configure DVC for Data Versioning' 2026, UCL data version control lecture, DAGsHub pipelines tutorial; search snippets only, not opened); docs and tutorials, not interview reports; MLOps and data science roles
**Say this first (1 line):** DVC's cache is a content-addressable store: each file is stored once under `.dvc/cache` at a path made from its md5, and the workspace file is a link or a copy of that object. Same content, same hash, one stored copy.

**Then explain:**
- **Layout:** `.dvc/cache/files/md5/<first 2 hex>/<remaining 30 hex>`. The `.dvc` file just stores the md5. Directories get a `.dir` manifest listing the md5 of each file (Q19).
- **Dedup:** two files with identical bytes share one cache object. In the run below 3 files made 2 objects.
- **Link types:** `cache.type` is a list in order of preference, default `reflink,copy`. *reflink* is copy-on-write: no extra space and safe, but only on filesystems that support it. *hardlink* and *symlink* use no extra space, but editing the workspace file edits the cache object, which can corrupt every file that shares it. *copy* is safest and uses double the disk. DVC makes cache files read-only to guard the linked types, but that did not stop writes in my run, since I ran as root.
- **Commands:** `dvc checkout` makes the workspace match the `.dvc` files and `dvc.lock` from the cache (restores deleted files, switches versions after `git checkout`). `dvc status` compares workspace to the `.dvc` files and cache. `dvc status -c` compares cache to the remote (what still needs `dvc push`).
- **gc:** `dvc gc` removes cache objects that are not referenced. It needs a scope flag. `-w` keeps only what the current workspace uses and deletes the rest of the local cache, including versions used by old commits and other branches (`-a` all branches, `-T` tags, `-c` also cleans the remote, check `dvc gc --help`). Use `--dry` first. Danger: if old versions were never pushed, gc deletes the only copy.

**Example:** `a.txt` and `b.txt` are both `hello\n`. Both `.dvc` files carry md5 `b1946ac9...`. The cache holds one object `b1/946ac9...`. Edit `c.txt` and `dvc add` again: new object, old `c.txt` object is now garbage that `dvc gc -w` removes from local cache. The remote still has it, so `git checkout` of the old `.dvc` plus `dvc pull` brings it back.

**Code:**
```bash
R=$(mktemp -d /tmp/q16remote.XXXX)
mkdir part1 && cd part1 && git init -q . && dvc init -q && dvc remote add -d loc $R -q
printf 'hello\n' > a.txt; cp a.txt b.txt; printf 'other\n' > c.txt
dvc add a.txt b.txt c.txt >/dev/null 2>&1
echo "--- cache after dvc add (a.txt and b.txt are identical): 2 objects for 3 files"; find .dvc/cache -type f | sort
echo "--- a.txt.dvc"; cat a.txt.dvc
echo "--- inode of a.txt vs its cache object (same inode = link, different = copy)"; stat -c '%i %n' a.txt .dvc/cache/files/md5/b1/946ac92492d2347c6235b4d2611184
git add -A >/dev/null; git commit -qm v1
echo "--- dvc status -c BEFORE push (cache vs remote)"; dvc status -c 2>&1 | grep -v '^$'
dvc push 2>&1 | tail -1
echo "--- dvc status -c AFTER push"; dvc status -c 2>&1
echo "--- delete a.txt from workspace; dvc status; dvc checkout"
rm a.txt; dvc status 2>&1 | grep -v '^$'; dvc checkout 2>&1 | grep -v '^$'; cat a.txt
echo "--- change c.txt, add, commit: old c.txt object is now unreferenced"
printf 'other v2\n' > c.txt; dvc add c.txt >/dev/null 2>&1; git add -A >/dev/null; git commit -qm v2
echo "cache objects: $(find .dvc/cache -type f | wc -l)"
echo "--- dvc gc -w --dry (dry run)"; dvc gc -w --dry 2>&1 | grep -v '^$'
echo "cache objects after dry run: $(find .dvc/cache -type f | wc -l)"
echo "--- dvc gc -w -f (workspace only: keeps only what the current workspace uses)"; dvc gc -w -f 2>&1 | grep -v '^$'
echo "cache objects after gc: $(find .dvc/cache -type f | wc -l)"
echo "--- but the old c.txt is still in the remote, so it can come back"
git checkout -q HEAD~1 -- c.txt.dvc; dvc pull 2>&1 | grep -v '^$' | tail -2; cat c.txt
cd ..
echo "=== part 2: symlink cache type, edit through the link"
mkdir part2 && cd part2 && git init -q . && dvc init -q && dvc config cache.type symlink
printf 'hello\n' > a.txt; cp a.txt b.txt; dvc add a.txt b.txt >/dev/null 2>&1
ls -l a.txt | awk '{print $1, $9, $10, $11}' | sed "s#$PWD/##"
echo "oops" >> a.txt        # as root the read-only bit does not stop this; as a normal user it usually does
echo "--- dvc status after the edit:"; dvc status 2>&1 | grep -v '^$'
```

**Output (my run):** dvc 3.67.1, local filesystem and a local-directory remote. With the default link type the inodes differ, so this sandbox filesystem fell back to copy (reflink was not available). Part 1 uses defaults and part 2 uses `cache.type symlink`.
```
--- cache after dvc add (a.txt and b.txt are identical): 2 objects for 3 files
.dvc/cache/files/md5/b1/946ac92492d2347c6235b4d2611184
.dvc/cache/files/md5/ba/7790b1708b71cb2b61b1a30d824712
--- a.txt.dvc
outs:
- md5: b1946ac92492d2347c6235b4d2611184
  size: 6
  hash: md5
  path: a.txt
--- inode of a.txt vs its cache object (same inode = link, different = copy)
1130612 a.txt
1131781 .dvc/cache/files/md5/b1/946ac92492d2347c6235b4d2611184
--- dvc status -c BEFORE push (cache vs remote)
	new:                c.txt
	new:                b.txt
2 files pushed
--- dvc status -c AFTER push
Cache and remote 'loc' are in sync.
--- delete a.txt from workspace; dvc status; dvc checkout
a.txt.dvc:
	changed outs:
		deleted:            a.txt
A       a.txt
hello
--- change c.txt, add, commit: old c.txt object is now unreferenced
cache objects: 3
--- dvc gc -w --dry (dry run)
WARNING: This will remove all cache except items used in the workspace of the current repo.
Removing /tmp/wr.zI7J/part1/.dvc/cache/files/md5/ba/7790b1708b71cb2b61b1a30d824712
Removed 1 objects from repo cache.
No unused 'legacy' cache to remove.
cache objects after dry run: 3
--- dvc gc -w -f (workspace only: keeps only what the current workspace uses)
WARNING: This will remove all cache except items used in the workspace of the current repo.
Removed 1 objects from repo cache.
No unused 'legacy' cache to remove.
cache objects after gc: 2
--- but the old c.txt is still in the remote, so it can come back
M       c.txt
1 file fetched and 1 file modified
other
=== part 2: symlink cache type, edit through the link
lrwxrwxrwx a.txt -> .dvc/cache/files/md5/b1/946ac92492d2347c6235b4d2611184
--- dvc status after the edit:
b.txt.dvc:
	changed outs:
		modified:           b.txt
a.txt.dvc:
	changed outs:
		modified:           a.txt
```
Note: the dry run prints "Removing ..." and "Removed 1 objects" wording, but the cache still had 3 objects afterwards. The real `-f` run took it to 2. Part 2: I edited `a.txt` through the symlink and `dvc status` reports both `a.txt` and `b.txt` as modified, since they point at one cache object. The cache is damaged until it is restored by `dvc pull` or the file is re-added.

**Follow-ups:**
- *Shared cache for a team?* A shared `cache.dir` on one machine saves space, with the link-type risks above.
- *Why md5, not sha256?* DVC 3 stores md5 (`hash: md5` in `.dvc`). Fine for dedup and change detection, not for security.
- *Does `dvc gc -c` delete the remote?* It deletes unreferenced objects on the remote. Be careful with shared remotes.

**Common mistakes:**
- Running `dvc gc -w` before `dvc push`, and losing the only copy of other branches' data.
- Using symlink/hardlink and editing the file in place.
- Confusing `dvc status` with `dvc status -c`.
- Thinking `.dvc/cache` goes into Git. It is git-ignored; only `.dvc` files go in.

### Q17 ⭐⭐ 🟡 DVC experiments: dvc exp run, dvc exp show, dvc exp diff, dvc exp apply and dvc exp branch. Explain how experiments are stored as hidden Git refs rather than commits, how -S train.lr=0.1 overrides a parameter, queueing several runs, and when to promote an experiment to a normal commit. Contrast with logging runs to MLflow or W&B. Run two experiments with different parameters locally and show the experiment table. Hedge: experiment UI features changed across DVC versions; state the version that ran.
**Asked at:** DVC official docs and tutorials (dvc.org 'Metrics, Plots, and Parameters' get-started page, OneUptime 'How to Configure DVC for Data Versioning' 2026, UCL data version control lecture, DAGsHub pipelines tutorial; search snippets only, not opened); docs and tutorials, not interview reports; MLOps and data science roles
**Say this first (1 line):** `dvc exp run` runs the pipeline with changed params, records the result as an experiment kept in hidden Git refs, not as a commit on my branch. I compare with `dvc exp show` and `dvc exp diff`, then promote the winner with `dvc exp apply` and a normal commit, or `dvc exp branch`.

**Then explain:**
- **Storage:** each experiment is a Git commit stored under `refs/exps/...`. `git branch` and `git log` do not show them, so I can try 50 ideas with no branch clutter. Data outputs go to the DVC cache like normal.
- **Override params:** `dvc exp run -S train.C=0.01` changes `params.yaml` for that run only. `-n name` names it. `--queue` stores runs and `dvc exp run --run-all` executes them (`-j` for parallel; check current docs).
- **Compare:** `dvc exp show` prints a table (params and metrics, one row per experiment under its base commit). `dvc exp diff a b` compares two. Output format and options changed between DVC versions, so treat this as DVC 3.67.1 behaviour and check current docs.
- **Promote:** `dvc exp apply <name>` writes that experiment's params, lock and outputs into the workspace, then I `git commit` normally. `dvc exp branch <name> <branch>` creates a Git branch from it. Share with `dvc exp push` and `dvc exp pull` (needs a Git remote, not run here).
- **Versus MLflow or W&B:** DVC experiments are tied to the Git-plus-pipeline state and reproduce exactly. They are local-first and Git-shaped, with a basic table. MLflow and W&B give a server, dashboards, many users, step-by-step metric curves and a registry. Many teams use both. Failure mode: `dvc exp run` leaves the result in your workspace (dirty), and if you forget to apply or commit, the "winner" lives only in a hidden ref (which `git gc` or a lost laptop can take).

**Example:** baseline `C=1.0` gives cv_acc 0.6 on a small noisy synthetic dataset. Experiments: `C=0.01` gives 0.7, `C=100` gives 0.55, and queued `0.1` gives 0.6583 and `10` gives 0.5667. Winner is `C=0.01`, apply it and commit `params.yaml`, `dvc.lock`, `metrics.json`. Small data, so the gaps are within noise; do not read much into them.

**Code:**
```bash
git init -q . && dvc init -q
cp /home/user/case_studies/interviews/scratch/B4P04_Q11-20/code/q17_train.py train.py
printf 'train:\n  C: 1.0\n' > params.yaml
dvc stage add -q -n train -d train.py -p train.C -M metrics.json python train.py
git add -A; git commit -qm base
dvc repro >/dev/null 2>&1; git add -A; git commit -qm "baseline run"
echo "=== two experiments with -S"
dvc exp run -S train.C=0.01 -n c-small 2>&1 | grep -e Experiment -e "exp-" | head -3
dvc exp run -S train.C=100 -n c-big 2>&1 | grep -e Experiment | head -3
echo "=== queue two more, then run them"
dvc exp run --queue -S train.C=0.1 -n q-01 2>&1 | grep -i queued
dvc exp run --queue -S train.C=10 -n q-10 2>&1 | grep -i queued
dvc exp run --run-all 2>&1 | grep -ie "experiment results" -e error | head
echo "=== dvc exp show"; dvc exp show --no-pager --md 2>&1
echo "=== dvc exp diff c-small c-big"; dvc exp diff c-small c-big 2>&1
echo "=== workspace holds the last run (dirty); experiments live in hidden refs, no new branches"; git status --short; git branch; git for-each-ref | awk '{print $3}' | head -5
echo "=== promote: apply c-small, then commit"
dvc exp apply c-small 2>&1 | tail -1; git diff --stat; git commit -qam "adopt C=0.01"; git log --oneline | head -3
echo "=== or branch from another experiment"
dvc exp branch c-big try-big 2>&1; git branch
```
```python
import json, yaml
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
p = yaml.safe_load(open("params.yaml"))["train"]
X, y = make_classification(n_samples=120, n_features=40, n_informative=3, flip_y=0.15, random_state=0)
acc = cross_val_score(LogisticRegression(C=p["C"], max_iter=300), X, y, cv=5).mean()
json.dump({"cv_acc": round(float(acc), 4)}, open("metrics.json", "w"))
```

**Output (my run):** dvc 3.67.1, sklearn 1.9.1, local only (no remote, no `dvc exp push`). I used `--md` for the table so it is not clipped by the terminal. Timestamps are in local time of the sandbox.
```
=== two experiments with -S
Experiment results have been applied to your workspace.
Experiment results have been applied to your workspace.
=== queue two more, then run them
Queued experiment 'q-01' for future execution.
Queued experiment 'q-10' for future execution.
=== dvc exp show
| Experiment            | Created   | State   | Executor   | cv_acc   | train.C   | train.py                         |
|-----------------------|-----------|---------|------------|----------|-----------|----------------------------------|
| workspace             | -         | -       | -          | 0.55     | 100       | e432cd949a5aabf26917012707d00db0 |
| master                | 02:13 PM  | -       | -          | 0.6      | 1         | e432cd949a5aabf26917012707d00db0 |
| ├── 9838557 [q-10]    | 02:14 PM  | Success | Dvc-task   | 0.5667   | 10        | e432cd949a5aabf26917012707d00db0 |
| ├── 37f5b71 [q-01]    | 02:14 PM  | Success | Dvc-task   | 0.6583   | 0.1       | e432cd949a5aabf26917012707d00db0 |
| ├── b201e58 [c-big]   | 02:13 PM  | -       | -          | 0.55     | 100       | e432cd949a5aabf26917012707d00db0 |
| └── aac3f78 [c-small] | 02:13 PM  | -       | -          | 0.7      | 0.01      | e432cd949a5aabf26917012707d00db0 |

=== dvc exp diff c-small c-big
Path          Metric    c-small    c-big    Change
metrics.json  cv_acc    0.7        0.55     -0.15

Path         Param    c-small    c-big    Change
params.yaml  train.C  0.01       100      99.99
=== workspace holds the last run (dirty); experiments live in hidden refs, no new branches
 M dvc.lock
 M metrics.json
 M params.yaml
* master
refs/exps/15/f9217004002bc91fe4994074ee3cbad64a0006/c-big
refs/exps/15/f9217004002bc91fe4994074ee3cbad64a0006/c-small
refs/exps/15/f9217004002bc91fe4994074ee3cbad64a0006/q-01
refs/exps/15/f9217004002bc91fe4994074ee3cbad64a0006/q-10
refs/exps/exec/EXEC_HEAD
=== promote: apply c-small, then commit
Changes for experiment 'c-small' have been applied to your current workspace.
 dvc.lock     | 4 ++--
 metrics.json | 2 +-
 params.yaml  | 2 +-
 3 files changed, 4 insertions(+), 4 deletions(-)
6db050b adopt C=0.01
15f9217 baseline run
85078d0 base
=== or branch from another experiment
Git branch 'try-big' has been created from experiment 'c-big'.
To switch to the new branch run:

	git checkout try-big
* master
  try-big
```

**Follow-ups:**
- *Can I run in parallel?* The queue supports workers (`-j`, check docs). Unique temp workspaces are used so runs do not clash.
- *Is the `git status` dirty after exp run?* Yes, the last run is applied to the workspace. Note it in the output above.
- *When not to use dvc exp?* When teammates need a shared live dashboard, use MLflow or W&B.

**Common mistakes:**
- Thinking experiments are branches and looking for them in `git log`.
- Forgetting to apply and commit the winner.
- Reading tiny metric differences as real wins (see Q11).
- Using the experiment table as a long-term record: refs get cleaned with `dvc exp gc` (check flags).

### Q18 ⭐⭐ 🟡 DVC pipeline pitfalls. Explain what goes wrong with undeclared dependencies (the stage never re-runs), outputs that are not tracked, stages that read a file the stage did not declare, always_changed, frozen stages, cache: false outputs for metrics, foreach and matrix stages for per-fold or per-model runs, and a non-deterministic stage that makes repro look different every time. Show a deliberately broken dvc.yaml with a missing dependency and prove the stale result with a real run, then fix it.
**Asked at:** DVC official docs and tutorials (dvc.org 'Metrics, Plots, and Parameters' get-started page, OneUptime 'How to Configure DVC for Data Versioning' 2026, UCL data version control lecture, DAGsHub pipelines tutorial; search snippets only, not opened); docs and tutorials, not interview reports; MLOps and data science roles
**Say this first (1 line):** DVC only re-runs a stage when something it declared has changed, so any file the code reads but the stage did not list is invisible to DVC and the result goes stale with no warning.

**Then explain:**
- **Undeclared dependency:** stage reads `config.json` but `deps` omits it. Change the file, `dvc repro` says "didn't change, skipping". Fix: list every file read in `deps` (or `params` for keys in `params.yaml`). Test: delete outputs, or run `dvc repro -f` and see whether results differ.
- **Untracked outputs:** an output the stage writes but does not list in `outs` is not cached, not versioned, and not restored by `dvc checkout`. List every file you want to keep.
- **Flags:** `always_changed: true` re-runs the stage every time (for stages that depend on the outside world; it makes everything downstream re-run too). `dvc freeze <stage>` makes repro skip a stage even if its deps changed, useful for an expensive step, risky if forgotten. `cache: false` on an output keeps it out of the DVC cache, used for small files you want in Git (metrics, `-M` does this).
- **foreach and matrix:** `foreach` makes one stage per item (`fold@0`, `fold@1`). `matrix` makes a stage per combination (model x seed). Good for per-fold and per-model runs. Mistake: too many generated stages make the DAG and `dvc.lock` huge.
- **Non-determinism:** an unseeded stage produces different bytes each run. `dvc repro -f` then changes the output hash and `dvc.lock` every time, so every PR shows a diff and caching never helps downstream. Seed everything and pin library versions.

**Example:** `make.py` sums `data.txt` times `scale` from `config.json`. With scale 2 the sum is 12. I change scale to 10 and run `dvc repro`: DVC says skipping and `out.txt` still says 12. Running by hand gives 60. After adding `config.json` to `deps`, repro re-runs and gives 60, and changing scale to 3 gives 18.

**Code:**
```bash
git init -q . && dvc init -q
printf '{"scale": 2}\n' > config.json
printf '1\n2\n3\n' > data.txt
cat > make.py <<'P'
import json
cfg = json.load(open("config.json"))          # <- reads a file the stage did not declare
vals = [int(v) * cfg["scale"] for v in open("data.txt")]
open("out.txt", "w").write(f"sum={sum(vals)}\n")
P
cat > dvc.yaml <<'Y'
stages:
  make:
    cmd: python make.py
    deps:
      - make.py
      - data.txt          # config.json is MISSING here
    outs:
      - out.txt
Y
echo "=== 1. broken pipeline"; dvc repro 2>&1 | grep -v -e '^$' -e autostage -e 'git add' -e 'To track' -e 'To enable'; cat out.txt
echo '{"scale": 10}' > config.json
echo "--- changed config.json to scale=10, ran dvc repro:"; dvc repro 2>&1 | grep -v '^$'; cat out.txt
echo "--- truth (run by hand):"; python make.py; cat out.txt
echo "=== 2. fix: declare config.json"
sed -i 's/      - data.txt          # config.json is MISSING here/      - data.txt\n      - config.json/' dvc.yaml
dvc repro 2>&1 | grep -e Running -e Updating; cat out.txt
echo '{"scale": 3}' > config.json; dvc repro 2>&1 | grep -e Running; cat out.txt
echo "=== 3. always_changed, frozen, cache:false metrics"
cat > dvc.yaml <<'Y'
stages:
  make:
    cmd: python make.py
    deps: [make.py, data.txt, config.json]
    outs: [out.txt]
  stamp:
    cmd: date +%s%N > stamp.txt
    always_changed: true
    outs:
      - stamp.txt:
          cache: false
Y
dvc repro 2>&1 | grep -e Running -e "didn't change"
dvc repro 2>&1 | grep -e Running -e "didn't change"
echo "--- freeze make, change data, repro"; dvc freeze make >/dev/null; echo 4 >> data.txt; dvc repro 2>&1 | grep -e Running -e "didn't change" -e frozen; cat out.txt
dvc unfreeze make > /dev/null; dvc repro make 2>&1 | grep -e Running; cat out.txt
echo "=== 4. foreach and matrix"
cat > dvc.yaml <<'Y'
stages:
  make:
    cmd: python make.py
    deps: [make.py, data.txt, config.json]
    outs: [out.txt]
  fold:
    foreach: [0, 1, 2]
    do:
      cmd: echo fold ${item} > fold_${item}.txt
      outs:
        - fold_${item}.txt
  grid:
    matrix:
      model: [svm, rf]
      seed: [1, 2]
    cmd: echo ${item.model} ${item.seed} > g_${item.model}_${item.seed}.txt
    outs:
      - g_${item.model}_${item.seed}.txt
Y
dvc stage list 2>&1 | grep -v '^$'
echo "=== 5. non-deterministic stage"
cat > dvc.yaml <<'Y'
stages:
  noisy:
    cmd: python -c "import random; print(random.random())" > noisy.txt
    outs:
      - noisy.txt
Y
dvc repro 2>&1 | grep Running; python -I -c "import yaml;print('noisy.txt md5 in dvc.lock:', yaml.safe_load(open('dvc.lock'))['stages']['noisy']['outs'][0]['md5'])"
dvc repro -f 2>&1 | grep Running; python -I -c "import yaml;print('noisy.txt md5 in dvc.lock:', yaml.safe_load(open('dvc.lock'))['stages']['noisy']['outs'][0]['md5'])"
```

**Output (my run):** dvc 3.67.1, local, git repo in a temp dir. Sections: 1 broken pipeline, 2 fix, 3 always_changed/frozen, 4 foreach/matrix list, 5 non-deterministic md5 changes.
```
=== 1. broken pipeline
Running stage 'make':
> python make.py
Generating lock file 'dvc.lock'
Updating lock file 'dvc.lock'
Use `dvc push` to send your updates to remote storage.
sum=12
--- changed config.json to scale=10, ran dvc repro:
Stage 'make' didn't change, skipping
Data and pipelines are up to date.
sum=12
--- truth (run by hand):
sum=60
=== 2. fix: declare config.json
Running stage 'make':
Updating lock file 'dvc.lock'
sum=60
Running stage 'make':
sum=18
=== 3. always_changed, frozen, cache:false metrics
Stage 'make' didn't change, skipping
Running stage 'stamp':
Stage 'make' didn't change, skipping
Running stage 'stamp':
--- freeze make, change data, repro
WARNING: stage: 'make' is frozen. Its dependencies are not going to be reproduced.
Stage 'make' didn't change, skipping
Running stage 'stamp':
sum=18
Running stage 'make':
sum=30
=== 4. foreach and matrix
make        Outputs out.txt
fold@0      Outputs fold_0.txt
fold@1      Outputs fold_1.txt
fold@2      Outputs fold_2.txt
grid@svm-1  Outputs g_svm_1.txt
grid@svm-2  Outputs g_svm_2.txt
grid@rf-1   Outputs g_rf_1.txt
grid@rf-2   Outputs g_rf_2.txt
=== 5. non-deterministic stage
Running stage 'noisy':
noisy.txt md5 in dvc.lock: 4b112c2d5921e1d280efe82bf4f08948
Running stage 'noisy':
noisy.txt md5 in dvc.lock: 3667f00915aa9a9e1f7f0c1f5bc27379
```
In section 3 the frozen stage did not re-run after `data.txt` changed (still 18, though the truth is 30 for scale 3 and 4 values). After `unfreeze` it ran and gave 30. Section 5: two forced runs produce two different md5 values in `dvc.lock`.

**Follow-ups:**
- *How do I find undeclared deps?* Run in a clean checkout or container with only declared files. A forgotten file then fails loudly. Also `dvc repro -f` and compare.
- *What about the run cache?* DVC remembers results by input hashes, so reverting an input can restore an old result without running; the message is "Stage is cached - skipping run".
- *Params versus deps?* Use `params` for specific keys: only changes to that key trigger a re-run, not other keys in the file.

**Common mistakes:**
- Reading hard-coded paths or env vars inside the stage with no declaration.
- Seeing "Data and pipelines are up to date" and trusting it.
- Leaving a stage frozen after debugging.
- `always_changed` on an early stage, which re-runs the whole pipeline.

### Q19 ⭐⭐ 🟡 Versioning a folder of many files with DVC: dvc add on a directory, the .dir manifest, why adding a directory with 100,000 small files is slow, options to keep it manageable (archive shards, parquet, WebDataset style tar files), what happens to the version when one file changes, and how dvc get, dvc import and dvc.api.open let another repo read a pinned version of the data. Show it with a tiny local dataset and a local remote. Large scale behaviour is not executed; do not quote speed numbers.
**Asked at:** DVC official docs and tutorials (dvc.org 'Metrics, Plots, and Parameters' get-started page, OneUptime 'How to Configure DVC for Data Versioning' 2026, UCL data version control lecture, DAGsHub pipelines tutorial; search snippets only, not opened); docs and tutorials, not interview reports; MLOps and data science roles
**Say this first (1 line):** `dvc add folder` stores each file as its own cache object and writes a `.dir` manifest that lists every file's hash. The folder's version is the hash of that manifest, so one changed file gives a new manifest and a new folder hash, but only the changed file is stored again.

**Then explain:**
- **What gets tracked:** `images.dvc` holds `md5: <hash>.dir`, `nfiles`, `size`. The `.dir` object in the cache is JSON: a list of `{relpath, md5}`.
- **One file changes:** new object for that file, new manifest, new folder md5. The other files are reused. `git diff` of the `.dvc` file shows just the new folder hash.
- **Why 100,000 small files is slow:** DVC hashes, links and transfers each file separately. Many tiny files mean many stat calls, many cache objects, many remote requests. No speed numbers here, I did not run it at scale. Options: pack into shards (tar or zip files of a few thousand samples, WebDataset style), use columnar files (parquet) when samples are tabular, or split into a few folders and version them separately.
- **Sharing a pinned version:** `dvc get <repo> <path> --rev <tag>` copies once and leaves no link. `dvc import` copies and writes a `.dvc` that records repo, rev and the exact commit (`rev_lock`), so `dvc update` can move it later. `dvc.api.open(path, repo=, rev=)` streams one file with no checkout. All three read bytes from the source repo's DVC remote, so the producer must have pushed.
- **Failure modes:** a file added to the folder after `dvc add` shows as modified until you `dvc add` again. `dvc import` of a moving branch is not pinned unless you read `rev_lock`. Tag or use a commit when you need stability.

**Example:** 4 files, `images/img1..img4.txt`. The folder md5 ends in `.dir`. The manifest has 4 entries. After editing `img3.txt` the cache has 7 objects: 4 originals, 1 new file, 1 old manifest, 1 new manifest. `dvc.api.open('images/img3.txt', rev='v1')` returns `image-3` and with `v2` returns `image-3 edited`.

**Code:**
```bash
R=$(mktemp -d /tmp/q19remote.XXXX)
mkdir producer consumer
cd producer && git init -q . && dvc init -q && dvc remote add -d loc $R -q
mkdir -p images && for i in 1 2 3 4; do echo "image-$i" > images/img$i.txt; done
dvc add images >/dev/null 2>&1
echo "--- images.dvc"; cat images.dvc
echo "--- cache: one .dir manifest + one object per file"; find .dvc/cache -type f | sed 's#.dvc/cache/files/md5/##' | sort
M=$(grep md5 images.dvc | head -1 | awk '{print $3}'); echo "--- manifest content ($M)"; cat .dvc/cache/files/md5/${M:0:2}/${M:2}; echo
git add -A >/dev/null; git commit -qm v1; git tag v1; dvc push 2>&1 | tail -1
echo "=== change ONE file, add again"
echo "image-3 edited" > images/img3.txt; dvc add images >/dev/null 2>&1
echo "new dir hash:"; grep md5 images.dvc | head -1
echo "cache objects: $(find .dvc/cache -type f | wc -l)  (3 unchanged files reused, +1 file, +1 manifest)"
git add -A >/dev/null; git commit -qm v2; git tag v2; dvc push 2>&1 | tail -1
P=$PWD; cd ../consumer && git init -q . && dvc init -q
echo "=== dvc get (plain copy, no link to the source repo)"
dvc get $P images --rev v1 -o got_v1 2>&1 | tail -1; ls got_v1; cat got_v1/img3.txt
echo "=== dvc import (copy + a .dvc file that pins repo and rev)"
dvc import $P images --rev v1 -o imported 2>&1 | tail -1; cat imported.dvc
echo "=== dvc.api.open: stream one file of a pinned version, no checkout"
python -I -c "
import dvc.api
for rev in ('v1', 'v2'):
    with dvc.api.open('images/img3.txt', repo='$P', rev=rev) as f: print(rev, '->', f.read().strip())
"
echo "=== dvc update to v2"
dvc update imported.dvc --rev v2 2>&1 | tail -1; cat imported/img3.txt
```

**Output (my run):** dvc 3.67.1, local Git repos and a local-directory remote (no cloud). Scale behaviour was not executed and I give no speed numbers.
```
--- images.dvc
outs:
- md5: f6cbd8086608ea283fa2b571d1eda43f.dir
  size: 32
  nfiles: 4
  hash: md5
  path: images
--- cache: one .dir manifest + one object per file
72/bee980634a9a1520150196659c531a
af/02dda0190040f03b85066c4119aa7e
d1/494b65f1a872b59ffd2c5e50887c62
dc/234b94ae02e9da1d061a83aa4f7ac8
f6/cbd8086608ea283fa2b571d1eda43f.dir
--- manifest content (f6cbd8086608ea283fa2b571d1eda43f.dir)
[{"md5": "d1494b65f1a872b59ffd2c5e50887c62", "relpath": "img1.txt"}, {"md5": "dc234b94ae02e9da1d061a83aa4f7ac8", "relpath": "img2.txt"}, {"md5": "af02dda0190040f03b85066c4119aa7e", "relpath": "img3.txt"}, {"md5": "72bee980634a9a1520150196659c531a", "relpath": "img4.txt"}]
5 files pushed
=== change ONE file, add again
new dir hash:
- md5: aa9c77b9e249efbc01974b4efec0ec22.dir
cache objects: 7  (3 unchanged files reused, +1 file, +1 manifest)
2 files pushed
=== dvc get (plain copy, no link to the source repo)
img1.txt
img2.txt
img3.txt
img4.txt
image-3
=== dvc import (copy + a .dvc file that pins repo and rev)
	dvc config core.autostage true
md5: b86c734301d2a487420f10773812902a
frozen: true
deps:
- path: images
  repo:
    url: /tmp/wr.TQ3I/producer
    rev: v1
    rev_lock: dd0dbc692f3bb8efa54361117928241bca7e9a47
outs:
- md5: f6cbd8086608ea283fa2b571d1eda43f.dir
  size: 32
  nfiles: 4
  hash: md5
  path: imported
=== dvc.api.open: stream one file of a pinned version, no checkout
v1 -> image-3
v2 -> image-3 edited
=== dvc update to v2
Importing 'images (/tmp/wr.TQ3I/producer)' -> 'imported'
image-3 edited
```

**Follow-ups:**
- *Does import copy data?* Yes, into your workspace and cache. The `.dvc` file records where it came from. A plain `dvc get` does not record it.
- *How do I read a folder without downloading everything?* `dvc.api.open` streams individual files, and `dvc.api.get_url` gives the remote URL (check current docs).
- *What breaks the 'one file changes' story?* A tar shard: change one sample, the whole shard is a new object. Pick shard size accordingly.

**Common mistakes:**
- Adding a huge folder of tiny files and being surprised at the time.
- Importing from a branch name and expecting a frozen version.
- Forgetting `dvc push` on the producer, so consumers cannot fetch.
- Hand-editing the folder after `dvc add` and not re-adding.

### Q20 ⭐⭐ 🟡 A team workflow with DVC and Git. Two people change the training data and the params on different branches. Explain what shows up in the pull request (the .dvc file or dvc.lock hash change, never the data), how merge conflicts in dvc.lock or .dvc files are resolved (re-run dvc repro, do not hand-merge hashes), who must dvc push before the PR is reviewed, a CI step that checks dvc status -c, and what a reviewer can and cannot see in the diff. Reproduce a dvc.lock conflict in a throwaway repo. CI platforms are not executed here; Part 7 owns CI design.
**Asked at:** DVC official docs and tutorials (dvc.org 'Metrics, Plots, and Parameters' get-started page, OneUptime 'How to Configure DVC for Data Versioning' 2026, UCL data version control lecture, DAGsHub pipelines tutorial; search snippets only, not opened); docs and tutorials, not interview reports; MLOps and data science roles
**Say this first (1 line):** In the PR you only see small text changes: the new hash in the `.dvc` file or `dvc.lock`, plus params and metrics. The data never appears in the diff, so the author must `dvc push` before review, and a conflict in `dvc.lock` is fixed by re-running `dvc repro`, never by hand-merging hashes.

**Then explain:**
- **In the PR:** `data.csv.dvc` (md5 and size change), `params.yaml`, `dvc.lock` (hashes of deps and outs), `metrics.json` if tracked in Git. A reviewer can see what changed and how big, and compare metrics. A reviewer cannot see the data rows, cannot tell if the new hash is a good dataset, and cannot trust the hash unless the data is in the remote.
- **Before review:** author runs `dvc push` so the reviewer or CI can `dvc pull`. Without the push, the `.dvc` file points to bytes that exist only on the author's laptop.
- **Conflicts:** two branches that both ran `dvc repro` each rewrote `dvc.lock` and `metrics.json`. The merge conflicts there. Do not pick hashes by hand. Fix real inputs first (merge `params.yaml` and the `.dvc` files, which are the sources), take one side of the generated files, run `dvc repro`, commit. DVC recomputes `dvc.lock` for the merged inputs. If both changed the same data file, you need to decide how to combine the data: that is a data question, not a Git question.
- **CI check:** `dvc status -c` (cache vs remote) catches "forgot to push". In my run it exits 0 even when something is missing, so the CI step must read the output (`--json` gives `{"data.csv": "new"}`), not just the exit code. Check current docs for flags that fail on diff. CI design belongs to Part 7, and CI was not executed here.
- **Failure modes:** forgetting `dvc checkout` after `git checkout`, so the workspace data is from another branch. A hash that "matches" but is not pushed. Merge picks the wrong `dvc.lock`, then CI green on stale outputs. Both branches add different rows to the same file.

**Example:** `main` has `C=1.0` and `data.csv`. Branch `data-v2` appends a row (new md5 `4437d833...`). Branch `params-c01` sets `C=0.1`. Merge both: `params.yaml` and `data.csv.dvc` merge cleanly, `dvc.lock` and `metrics.json` conflict. After taking one side and `dvc repro`, `dvc.lock` shows `C: 0.1` and the data md5 `4437d833...`: both changes are in.

**Code:**
```bash
R=$(mktemp -d /tmp/q20remote.XXXX)
git init -q -b main . && dvc init -q && dvc remote add -d loc $R -q
python -I -c "
import numpy as np; r=np.random.default_rng(0); x=r.normal(size=(200,2)); y=(x[:,0]+r.normal(scale=.8,size=200)>0).astype(int)
open('data.csv','w').write('x1,x2,y\n'+'\n'.join(f'{a:.4f},{b:.4f},{c}' for (a,b),c in zip(x,y))+'\n')"
printf 'train:\n  C: 1.0\n' > params.yaml
cat > train.py <<'P'
import json, yaml, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
C = yaml.safe_load(open("params.yaml"))["train"]["C"]; d = pd.read_csv("data.csv")
json.dump({"acc": round(float(cross_val_score(LogisticRegression(C=C), d[["x1","x2"]], d.y, cv=5).mean()), 4)}, open("metrics.json", "w"))
P
dvc add data.csv >/dev/null 2>&1
dvc stage add -q -n train -d train.py -d data.csv -p train.C -M metrics.json python train.py
dvc repro >/dev/null 2>&1; git add -A; git commit -qm base; dvc push 2>&1 | tail -1
echo "=== branch data-v2: new rows in data.csv"
git checkout -q -b data-v2; echo "0.1000,0.2000,1" >> data.csv; dvc repro 2>&1 | grep Running; git add -A; git commit -qm "more data"; dvc push 2>&1 | tail -1
echo "--- what the PR shows (git diff main..data-v2, hashes only):"; git diff main..data-v2 --stat; git diff main..data-v2 -U0 -- data.csv.dvc | grep -v -e '^diff' -e '^index'
git checkout -q main; dvc checkout >/dev/null 2>&1; git checkout -q -b params-c01; sed -i 's/C: 1.0/C: 0.1/' params.yaml; dvc repro 2>&1 | grep Running; git add -A; git commit -qm "C=0.1"
git checkout -q main; dvc checkout >/dev/null 2>&1; git merge -q data-v2 -m "merge data-v2" 2>&1 | tail -1; dvc checkout >/dev/null 2>&1
echo "=== merge params-c01 into main"
git merge params-c01 2>&1 | grep -i conflict
echo "--- conflict markers in dvc.lock:"; git diff --name-only --diff-filter=U; grep -n -e '<<<<<<<' -e '=======' -e '>>>>>>>' dvc.lock
echo "=== resolve: take one side of the generated files, let DVC recompute them"
git checkout --ours dvc.lock metrics.json; dvc repro 2>&1 | grep -v -e "^$" -e autostage -e "git add" -e "To track" -e "To enable" -e "dvc push"
git add dvc.lock metrics.json; git commit -qm "merge params-c01; dvc repro"
python -I -c "
import yaml; l=yaml.safe_load(open('dvc.lock'))['stages']['train']
print('lock params:', l['params']['params.yaml'], '| data md5:', [d['md5'] for d in l['deps'] if d['path']=='data.csv'][0])"
grep md5 data.csv.dvc; tail -1 data.csv
echo "=== CI check: someone commits a data change but forgets dvc push"
echo "0.3,0.3,0" >> data.csv; dvc add data.csv >/dev/null 2>&1; git add -A; git commit -qm "forgot to push"
dvc status -c; echo "exit=$?"
dvc status -c --json; echo "exit=$?"
dvc push 2>&1 | tail -1
dvc status -c; echo "exit=$?"
```

**Output (my run):** dvc 3.67.1, git 2.43, local-directory remote, throwaway repo in a temp dir. No CI platform was run. After every `git checkout` I ran `dvc checkout`, because Git does not restore DVC-tracked data (a classic mistake: you train on the wrong branch's data). After taking one side of the generated files, `dvc repro` really re-ran the stage, and `dvc.lock` now has the merged inputs.
```
1 file pushed
=== branch data-v2: new rows in data.csv
Running stage 'train':
1 file pushed
--- what the PR shows (git diff main..data-v2, hashes only):
 data.csv.dvc | 4 ++--
 dvc.lock     | 6 +++---
 metrics.json | 2 +-
 3 files changed, 6 insertions(+), 6 deletions(-)
--- a/data.csv.dvc
+++ b/data.csv.dvc
@@ -2,2 +2,2 @@ outs:
-- md5: 868bbdf0aa96a4077dc358bd5668340a
-  size: 3419
+- md5: 4437d833347b0d9630b06fa43c7424f6
+  size: 3435
Running stage 'train':
=== merge params-c01 into main
CONFLICT (content): Merge conflict in dvc.lock
CONFLICT (content): Merge conflict in metrics.json
Automatic merge failed; fix conflicts and then commit the result.
--- conflict markers in dvc.lock:
dvc.lock
metrics.json
20:<<<<<<< HEAD
23:=======
26:>>>>>>> params-c01
=== resolve: take one side of the generated files, let DVC recompute them
Updated 2 paths from the index
'data.csv.dvc' didn't change, skipping
Running stage 'train':
> python train.py
Updating lock file 'dvc.lock'
lock params: {'train.C': 0.1} | data md5: 4437d833347b0d9630b06fa43c7424f6
- md5: 4437d833347b0d9630b06fa43c7424f6
  hash: md5
0.1000,0.2000,1
=== CI check: someone commits a data change but forgets dvc push
	new:                data.csv
exit=0
{"data.csv": "new"}
exit=0
1 file pushed
Cache and remote 'loc' are in sync.
exit=0
```

**Follow-ups:**
- *Should `dvc.lock` be in Git?* Yes. It is the exact record. The conflicts come with it, so the standard fix is to regenerate.
- *Review checklist?* Params change makes sense, metric diff (`dvc metrics diff`, `dvc params diff`) is plausible, data hash was pushed, no unrelated files.
- *Protect main?* Use CI to run `dvc status -c` and a reproduce-or-compare check. Details in Part 7.

**Common mistakes:**
- Opening the PR without `dvc push`.
- Hand-picking one side of `dvc.lock` and committing without running `dvc repro`.
- Trusting the exit code of `dvc status -c` in CI.
- Reviewing only code and ignoring the `.dvc` and `dvc.lock` diff.

### Q21 ⭐⭐ 🟡 MLflow Projects and mlflow run. Explain the MLproject file (name, entry points, parameters with types and defaults, environment as conda, virtualenv or Docker), how mlflow run executes an entry point and logs it as a run with the source and git commit, and why many teams now prefer plain scripts, DVC or an orchestrator over MLflow Projects (hedge). Write an MLproject for a train.py with two parameters and run it with the local environment manager if it works here; say exactly what ran.
**Asked at:** MLflow official docs and tutorials (mlflow.org tracking, autolog and model registry pages, MLflow 3.1.3 autolog docs, MLflow 2.11 model signature docs, DataTalksClub MLOps Zoomcamp experiment-tracking module, Azure ML MLflow training pages; search snippets only, not opened); docs and course material, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** An MLproject file is a small YAML recipe: a name, entry points with typed parameters, and an environment. `mlflow run` reads it, creates a run, and executes the command with the parameters filled in.
**Then explain:**
- The file has `name`, `entry_points` (each with `parameters` that have a type and a default, and a `command`), and one environment key: `python_env`, `conda_env` or `docker_env`.
- `mlflow run . -P C=0.5` builds the command line, starts a run that is tagged `source.type = PROJECT`, and runs the command. Your script then logs into that same run (inside `mlflow run`, `start_run()` attaches to the run the CLI made, because the CLI sets the run id in an environment variable).
- `--env-manager local` skips building an environment and uses the Python you already have. The other choices are `virtualenv`, `uv` and `conda` (check `mlflow run --help` for your version). Only local is fast and also the least reproducible.
- If the folder is a Git repo, MLflow records the commit as a tag, and it can run straight from a Git URL. In my run the folder was not a Git repo, so no commit tag was written. I did not run the Git case.
- Why many teams skip it now (my view, hedge): a plain script plus a `dvc.yaml` or an orchestrator already gives the command, the parameters and the data lineage. MLproject adds a second place to declare the same things, and the environment build can be slow. It is still fine for small teams that want one command to rerun a tracked run.
- Failure modes: a parameter with the wrong type fails before the command starts; a missing default with no `-P` fails; `docker_env` needs a running Docker daemon (not available here, not executed).
**Example:** `C` is declared `float, default 1.0`. `mlflow run . -P C=0.5` runs `python train.py --C 0.5 --max_iter 100`. Hand check: one new run, `params.C = 0.5`, `params.max_iter = 100` (default used), and `test_acc` on the iris test split.
**Code:** MLproject (YAML), `train.py` (Python), and the shell driver that ran everything in a fresh temp directory with a sqlite tracker. MLflow 3.17.2 here.
```yaml
name: iris_demo
entry_points:
  main:
    parameters:
      C: {type: float, default: 1.0}
      max_iter: {type: int, default: 100}
    command: "python train.py --C {C} --max_iter {max_iter}"
```
```python
import argparse, mlflow
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
p = argparse.ArgumentParser()
p.add_argument("--C", type=float, default=1.0)
p.add_argument("--max_iter", type=int, default=100)
a = p.parse_args()
X, y = load_iris(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
m = LogisticRegression(C=a.C, max_iter=a.max_iter).fit(Xtr, ytr)
with mlflow.start_run():          # under `mlflow run` this attaches to the run the CLI created
    mlflow.log_param("C", a.C)
    mlflow.log_param("max_iter", a.max_iter)
    mlflow.log_metric("test_acc", round(m.score(Xte, yte), 4))
```
```bash
set -e
source "$(dirname "$0")/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q21.XXXX); cp "$(dirname "$0")"/{MLproject,train.py} $W/; cd $W
export MLFLOW_TRACKING_URI=sqlite:///mlflow.db
mlflow --version
mlflow run . --env-manager local --experiment-name proj -P C=0.5 2>&1 | grep -v '^$' | tail -8
python3 -I - <<'P'
import mlflow
mlflow.set_tracking_uri("sqlite:///mlflow.db")
df = mlflow.search_runs(experiment_names=["proj"])
r = df.iloc[0]
print(df.shape[0], "run;", "status", r["status"])
print({k: r[k] for k in ["params.C","params.max_iter","metrics.test_acc"]})
print(sorted(c for c in df.columns if c.startswith("tags.mlflow")))
print("source.name:", r["tags.mlflow.source.name"], "| source.type:", r["tags.mlflow.source.type"])
P
```
**Output (my run):** Real run, `--env-manager local`, MLflow 3.17.2, Python 3.13. The `source.name` line is a temp folder, so it will differ on your machine.
```text
mlflow, version 3.17.2
2026/10/26 14:04:55 INFO mlflow.store.db.utils: Creating initial MLflow database tables...
2026/10/26 14:04:55 INFO mlflow.store.db.utils: Updating database tables
2026/10/26 14:04:56 INFO mlflow.projects: 'proj' does not exist. Creating a new experiment
2026/10/26 14:04:57 INFO mlflow.projects.utils: === Created directory /tmp/tmphd8_4623 for downloading remote URIs passed to arguments of type 'path' ===
2026/10/26 14:04:57 INFO mlflow.projects.backend.local: === Running command 'python train.py --C 0.5 --max_iter 100' in run with ID '6a339424d9384e18a3522ffe9215c585' === 
2026/10/26 14:05:00 INFO mlflow.projects: === Run (ID '6a339424d9384e18a3522ffe9215c585') succeeded ===
1 run; status FINISHED
{'params.C': '0.5', 'params.max_iter': '100', 'metrics.test_acc': np.float64(0.9778)}
['tags.mlflow.project.backend', 'tags.mlflow.project.entryPoint', 'tags.mlflow.runName', 'tags.mlflow.source.name', 'tags.mlflow.source.type', 'tags.mlflow.user']
source.name: /tmp/claude-0/b4q21.Kn4c | source.type: PROJECT
```

**Follow-ups:**
- *Can I run it from GitHub?* Yes: `mlflow run https://github.com/org/repo -P C=0.5` clones and runs. Not executed here (no repo to point at).
- *How do I run it on a cluster?* `--backend` options exist (for example Kubernetes or Databricks). Not executed here; check current docs.
- *What replaces it?* A `dvc.yaml` stage, an Airflow or Prefect task, or a plain CLI. All of them can still log to MLflow.
**Common mistakes:**
- Believing `mlflow run` makes the run reproducible. With `--env-manager local` it only records the command and parameters, not your installed libraries.
- Forgetting that `train.py` must call `mlflow.log_*` itself (or autolog). The CLI creates the run but does not know your metrics.
- Hard-coding the tracking URI in `train.py`, so the CLI and the script write to different places.

### Q22 ⭐⭐ 🟡 MLflow model flavors and pyfunc. Explain the MLmodel file (flavors, signature, run_id, environment files such as requirements.txt and conda.yaml), why the python_function flavor gives one predict interface over sklearn, xgboost, pytorch and custom code, and how to write a custom pyfunc model (PythonModel with load_context and predict) that bundles preprocessing and the model so serving cannot skew. Show the folder a logged model produces, and a custom pyfunc that is loaded and called locally.
**Asked at:** MLflow official docs and tutorials (mlflow.org tracking, autolog and model registry pages, MLflow 3.1.3 autolog docs, MLflow 2.11 model signature docs, DataTalksClub MLOps Zoomcamp experiment-tracking module, Azure ML MLflow training pages; search snippets only, not opened); docs and course material, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** The MLmodel file is the model's manifest. It lists the flavors (ways to load the model), the signature and the environment files. The `python_function` flavor gives every model one `predict` call, and a custom PythonModel lets me ship the preprocessing together with the model.
**Then explain:**
- A logged model is a folder: `MLmodel`, `requirements.txt`, `conda.yaml`, `python_env.yaml`, plus the model files and, for custom pyfunc, an `artifacts/` folder (see the run output below).
- `MLmodel` lists `flavors`. An sklearn model has two: `sklearn` (load back as an sklearn object) and `python_function` (generic). A custom model has only `python_function`.
- Serving tools only need the pyfunc flavor, so one server can run sklearn, xgboost, pytorch or custom code behind `predict(DataFrame)`.
- Custom `PythonModel`: `load_context` runs once at load and reads the bundled files; `predict` runs per request. Put the scaler and the model inside, and callers cannot forget the scaling.
- Failure modes: the pickled class is serialised with cloudpickle, so loading needs a compatible Python and library set (the `python_version` and `requirements.txt` in the folder tell you which). Only load models you trust: pickle can run code on load. MLflow also warns that a Python object as `python_model` uses CloudPickle and suggests models-from-code (check current docs).
**Example:** Iris rows 0, 60, 120 are classes 0, 1, 2. The custom model scales inside `predict`, so raw rows give `[0, 1, 2]`. A plain sklearn model that was trained on scaled data, loaded as pyfunc and fed the same raw rows, gives `[1, 2, 2]`: that is training-serving skew in one line.
**Code:** One script. It trains a scaler and a logistic regression, wraps both in `ScaledClf`, logs it, lists the folder, prints the `MLmodel` file and calls the loaded model.
```python
# Q22: MLmodel file, flavors, and a custom pyfunc that bundles preprocessing + model.
import os, mlflow, mlflow.pyfunc, pandas as pd, numpy as np
from mlflow.models import infer_signature
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("flavors")
X, y = load_iris(return_X_y=True, as_frame=True)
sc = StandardScaler().fit(X)
clf = LogisticRegression(max_iter=200).fit(sc.transform(X), y)

class ScaledClf(mlflow.pyfunc.PythonModel):
    def load_context(self, context):                    # runs once at load; read bundled files here
        self.sc = joblib.load(context.artifacts["scaler"])
        self.clf = joblib.load(context.artifacts["clf"])
    def predict(self, context, model_input, params=None):
        return self.clf.predict(self.sc.transform(model_input))   # scaling can never be skipped

joblib.dump(sc, "scaler.pkl"); joblib.dump(clf, "clf.pkl")
sig = infer_signature(X.head(3), clf.predict(sc.transform(X.head(3))))
with mlflow.start_run() as run:
    info = mlflow.pyfunc.log_model(name="model", python_model=ScaledClf(),
                                   artifacts={"scaler": "scaler.pkl", "clf": "clf.pkl"},
                                   signature=sig, input_example=X.head(2),
                                   pip_requirements=["scikit-learn", "joblib"])
    mlflow.sklearn.log_model(clf, name="plain_sklearn", signature=sig)
    rid = run.info.run_id
local = mlflow.artifacts.download_artifacts(run_id=rid, artifact_path="model", dst_path="dl")
print("files in the pyfunc model folder:")
for root, _, fs in sorted(os.walk(local)):
    for f in sorted(fs):
        print("  ", os.path.relpath(os.path.join(root, f), local))
print("\n--- MLmodel (custom pyfunc), trimmed ---")
for line in open(os.path.join(local, "MLmodel")).read().splitlines():
    if not line.startswith(("artifact_path", "utc_time_created", "mlflow_version", "model_uuid", "model_id", "run_id")):
        print(line)
plain = mlflow.artifacts.download_artifacts(run_id=rid, artifact_path="plain_sklearn", dst_path="dl2")
print("\n--- flavors in the plain sklearn model ---")
import yaml
print(list(yaml.safe_load(open(os.path.join(plain, "MLmodel")))["flavors"]))

loaded = mlflow.pyfunc.load_model(f"runs:/{rid}/model")
raw = X.iloc[[0, 60, 120]]
print("\ncustom pyfunc on RAW (unscaled) rows:", loaded.predict(raw).tolist(), "| truth:", y.iloc[[0, 60, 120]].tolist())
print("plain sklearn pyfunc on the same raw rows:", mlflow.pyfunc.load_model(f"runs:/{rid}/plain_sklearn").predict(raw).tolist(), "(no scaler inside, so skew risk)")
```
```bash
set -e
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q22.XXXX); cd $W
python3 -I "$D/q22.py" 2>&1 | sed "s/\x1b\[[0-9;]*m//g" | grep -v "INFO\|Downloading\|color_warning"
```
**Output (my run):** Real run (MLflow 3.17.2, sqlite tracker in a temp dir; warnings kept as printed, the per-line INFO logs were filtered out).
```text
/tmp/claude-0/ven/v/lib/python3.13/site-packages/mlflow/pyfunc/utils/data_validation.py:187: UserWarning: Add type hints to the `predict` method to enable data validation and automatic signature inference during model logging. Che ...[line cut for the book]
2026/10/26 14:05:37 WARNING mlflow.pyfunc: Passing a Python object as `python_model` causes it to be serialized using CloudPickle, it requires exercising caution as Python object serialization mechanisms may execute arbitrary code ...[line cut for the book]
files in the pyfunc model folder:
   MLmodel
   conda.yaml
   input_example.json
   python_env.yaml
   python_model.pkl
   registered_model_meta
   requirements.txt
   serving_input_example.json
   artifacts/clf.pkl
   artifacts/scaler.pkl

--- MLmodel (custom pyfunc), trimmed ---
flavors:
  python_function:
    artifacts:
      clf:
        path: artifacts/clf.pkl
        uri: clf.pkl
      scaler:
        path: artifacts/scaler.pkl
        uri: scaler.pkl
    cloudpickle_version: 3.1.2
    code: null
    env:
      conda: conda.yaml
      virtualenv: python_env.yaml
    loader_module: mlflow.pyfunc.model
    python_model: python_model.pkl
    python_version: 3.13.17
    streamable: false
is_signature_from_type_hint: false
model_size_bytes: 4619
prompts: null
saved_input_example_info:
  artifact_path: input_example.json
  pandas_orient: split
  serving_input_path: serving_input_example.json
  type: dataframe
signature:
  inputs: '[{"type": "double", "name": "sepal length (cm)", "required": true}, {"type":
    "double", "name": "sepal width (cm)", "required": true}, {"type": "double", "name":
    "petal length (cm)", "required": true}, {"type": "double", "name": "petal width
    (cm)", "required": true}]'
  outputs: '[{"type": "tensor", "tensor-spec": {"dtype": "int64", "shape": [-1]}}]'
  params: null
type_hint_from_example: false

--- flavors in the plain sklearn model ---
['python_function', 'sklearn']

custom pyfunc on RAW (unscaled) rows: [0, 1, 2] | truth: [0, 1, 2]
/tmp/claude-0/ven/v/lib/python3.13/site-packages/sklearn/utils/validation.py:2823: UserWarning: X has feature names, but LogisticRegression was fitted without feature names
  warnings.warn(
plain sklearn pyfunc on the same raw rows: [1, 2, 2] (no scaler inside, so skew risk)
```

**Follow-ups:**
- *Why not just pickle a sklearn Pipeline?* A Pipeline already bundles scaler and model. Custom pyfunc is for things a Pipeline cannot hold: rules, lookups, multiple models, post-processing.
- *What does `signature` in MLmodel do?* It lets pyfunc check input columns and types at predict time (see Q9).
- *Can I avoid pickle?* Yes, models-from-code logs a Python file instead of a pickled object. Not run here; check current docs.
**Common mistakes:**
- Doing preprocessing in a notebook and logging only the bare model, so the server receives raw data and quietly gives wrong answers.
- Loading bundled files in `predict` instead of `load_context`, so they are read on every request.
- Ignoring `requirements.txt` in the model folder and then being surprised that load fails on a different Python.

### Q23 ⭐⭐ 🟡 Serving an MLflow model locally. Explain mlflow models serve, mlflow models predict and the REST /invocations request formats (dataframe_split, dataframe_records, inputs; check the docs for the version), environment managers (local, virtualenv, uv or conda), and what mlflow models build-docker produces (Docker is not available here). Run mlflow models predict on a registered model locally and, if feasible, serve it on localhost and post one request. Part 6 owns serving frameworks and production design; keep this to what MLflow itself provides. Docker builds are not executed.
**Asked at:** MLflow official docs and tutorials (mlflow.org tracking, autolog and model registry pages, MLflow 3.1.3 autolog docs, MLflow 2.11 model signature docs, DataTalksClub MLOps Zoomcamp experiment-tracking module, Azure ML MLflow training pages; search snippets only, not opened); docs and course material, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** MLflow itself gives me `mlflow models predict` for a batch file and `mlflow models serve` for a small REST server with `/ping` and `/invocations`. For real production serving I would use a proper serving stack (Part 6).
**Then explain:**
- Both commands take a model URI like `models:/iris_clf@champion`, which is the registry alias from Q8. Moving the alias changes what `serve` loads on its next start.
- The request body must have exactly one top-level key: `dataframe_split`, `dataframe_records`, `instances` or `inputs` (the MLflow 3.17.2 error text lists these four; check the docs for your version). The same rule applies to the input file of `predict -t json`.
- `--env-manager` chooses where the model runs: `local` (current Python), `virtualenv`, `uv`, or `conda` (conda needs conda installed). A fresh environment is safer and slower.
- `mlflow models build-docker` builds an image whose default entrypoint serves the model on port 8080 (from `--help`). Not executed here: no Docker daemon. Part 2 and Part 6 cover images and serving.
- Failure modes: a bare `{columns, data}` file without the wrapper key fails; a missing column is rejected by the signature check with an `INVALID_PARAMETER_VALUE` error JSON (real text below); `serve` with `local` uses whatever versions are installed, which may differ from the training environment.
**Example:** Two iris rows are sent as `dataframe_split`. Both are setosa (class 0), so `{"predictions": [0, 0]}` is the hand-checkable answer. A single row with petal length 5.2 and petal width 2.3 should be virginica (class 2).
**Code:** `make_model.py` registers `iris_clf` v1 with alias `champion` in a sqlite registry; the shell script then runs `predict`, starts `serve` on 127.0.0.1:5088, sends three requests with curl, and stops the server.
```python
import mlflow, pandas as pd
from mlflow.models import infer_signature
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
mlflow.set_tracking_uri("sqlite:///mlflow.db")
X, y = load_iris(return_X_y=True, as_frame=True)
m = LogisticRegression(max_iter=200).fit(X, y)
with mlflow.start_run():
    mlflow.sklearn.log_model(m, name="model", signature=infer_signature(X, m.predict(X)), registered_model_name="iris_clf")
mlflow.MlflowClient().set_registered_model_alias("iris_clf", "champion", 1)
X.head(2).to_json("in_split.json", orient="split", index=False)
print("registered iris_clf v1, alias champion")
```
```bash
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q23.XXXX); cd $W
export MLFLOW_TRACKING_URI=sqlite:///mlflow.db
python3 -I "$D/make_model.py" 2>&1 | grep -v "INFO\|Downloading\|WARNING"
echo "--- mlflow models predict (batch, CLI) ---"
python3 -I -c "import json;d=json.load(open('in_split.json'));print(json.dumps({'dataframe_split':d}))" > in_req.json
cat in_split.json; echo
echo "bare split file (no wrapper key):"
mlflow models predict -m models:/iris_clf@champion -i in_split.json -t json --env-manager local 2>&1 | grep "^mlflow.exceptions" | cut -c1-200
echo "wrapped file {\"dataframe_split\": ...}:"
mlflow models predict -m models:/iris_clf@champion -i in_req.json -t json --env-manager local 2>&1 | grep -v "INFO\|WARNING\|Downloading"
echo "--- mlflow models serve (localhost:5088) ---"
mlflow models serve -m models:/iris_clf@champion -p 5088 -h 127.0.0.1 --env-manager local > serve.log 2>&1 &
PID=$!
for i in $(seq 1 40); do curl -s http://127.0.0.1:5088/ping -o /dev/null -w "%{http_code}" 2>/dev/null | grep -q 200 && break; sleep 1; done
echo "GET /ping -> $(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:5088/ping)"
echo "dataframe_split:"; curl -s -X POST http://127.0.0.1:5088/invocations -H 'Content-Type: application/json' -d @in_req.json; echo
echo "dataframe_records:"; curl -s -X POST http://127.0.0.1:5088/invocations -H 'Content-Type: application/json' -d '{"dataframe_records":[{"sepal length (cm)":6.7,"sepal width (cm)":3.0,"petal length (cm)":5.2,"petal width (cm)":2.3}]}'; echo
echo "missing column:"; curl -s -X POST http://127.0.0.1:5088/invocations -H 'Content-Type: application/json' -d '{"dataframe_records":[{"sepal length (cm)":6.7}]}' | cut -c1-260; echo
kill $PID; wait $PID 2>/dev/null
```
**Output (my run):** Real run on localhost, MLflow 3.17.2. The last error line is cut for length. The `pip`/INFO startup noise was filtered out.
```text
Successfully registered model 'iris_clf'.
Created version '1' of model 'iris_clf'.
registered iris_clf v1, alias champion
--- mlflow models predict (batch, CLI) ---
{"columns":["sepal length (cm)","sepal width (cm)","petal length (cm)","petal width (cm)"],"data":[[5.1,3.5,1.4,0.2],[4.9,3.0,1.4,0.2]]}
bare split file (no wrapper key):
mlflow.exceptions.MlflowException: The input must be a JSON dictionary with exactly one of the input fields {'instances', 'inputs', 'dataframe_records', 'dataframe_split'}. Received dictionary with in
wrapped file {"dataframe_split": ...}:
{"predictions": [0, 0]}
--- mlflow models serve (localhost:5088) ---
GET /ping -> 200
dataframe_split:
{"predictions": [0, 0]}
dataframe_records:
{"predictions": [2]}
missing column:
{"error_code": "INVALID_PARAMETER_VALUE", "message": "Failed to predict data '   sepal length (cm)\n0                6.7'. \nError: Failed to enforce schema of data '   sepal length (cm)\n0                6.7' with schema '['sepal ...[line cut for the book]
```

**Follow-ups:**
- *Is `mlflow models serve` production ready?* It is fine for a demo or a simple internal tool. Autoscaling, auth, batching and rollout control come from the platform around it (Part 6, Part 3).
- *What is `/ping` for?* A health check; it returned 200 here.
- *How do I send a tensor?* Use `inputs` (check the docs for your version). Not run here.
**Common mistakes:**
- Sending the DataFrame JSON without the `dataframe_split` wrapper key.
- Serving with `--env-manager local` and assuming the libraries match training.
- Pointing a service at `models:/name/latest` or a version number and then not knowing which model is live. Use an alias.

### Q24 ⭐⭐ 🟡 MLflow artifacts in depth: log_artifact, log_artifacts, log_figure, log_text, log_dict, log_table, artifact URIs, how artifact_location is fixed when an experiment is created, proxied artifact serving (--serve-artifacts) versus clients holding their own S3 credentials, and the problem of artifacts written by a client that cannot reach the server's path. Show a local run that logs a figure, a dict and a CSV and then downloads them with mlflow.artifacts.download_artifacts. S3 and proxy mode against a remote server are not executed.
**Asked at:** MLflow official docs and tutorials (mlflow.org tracking, autolog and model registry pages, MLflow 3.1.3 autolog docs, MLflow 2.11 model signature docs, DataTalksClub MLOps Zoomcamp experiment-tracking module, Azure ML MLflow training pages; search snippets only, not opened); docs and course material, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** An artifact is any file attached to a run. The tracking store keeps the run row; the artifact store keeps the bytes, at a location fixed when the experiment is created.
**Then explain:**
- APIs: `log_artifact` (one file), `log_artifacts` (a folder), `log_figure`, `log_text`, `log_dict`, `log_table`. All write under `<artifact_location>/<run_id>/artifacts/...`. `download_artifacts` and `load_text` read them back.
- `artifact_location` is set at experiment creation (a default under `./mlruns`, or `--default-artifact-root` on a server, or the `artifact_location` argument as I did). Changing the server flag later does not move old experiments.
- With a remote server there are two modes. Direct access: the client writes to S3 itself and needs its own credentials. Proxied access (`--serve-artifacts`): the client talks only to the server, which holds the credentials. Check current docs for flags and defaults. Not executed here (needs S3 and a remote server).
- Classic failure: the client logs to a path that only the server can see, for example a server folder `/srv/art`. The client then tries to create `/srv/art` on its own machine and gets a permission or missing-path error. Proxied mode avoids this.
- Do not put huge files or secrets in artifacts. Artifacts are as widely readable as the store.
**Example:** After the run, the listing should show six folders: `cfg`, `notes`, `outputs`, `plots`, `shards` (two files from `log_artifacts`) and `tables`. Hand check: `shards/part0.txt` and `part1.txt` exist because the loop wrote two files.
**Code:** A run that logs a figure, a dict, a text note, a CSV, a folder and a table to a custom `artifact_location`, lists them, then downloads three of them. Needs matplotlib (it was installed here).
```python
# Q24: artifact logging APIs, artifact_location fixed at experiment creation, download back.
import os, json, mlflow, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
mlflow.set_tracking_uri("sqlite:///mlflow.db")
exp_id = mlflow.create_experiment("art", artifact_location="file:///tmp/claude-0/b4q24_art_root")
exp = mlflow.get_experiment(exp_id)
print("artifact_location fixed at creation:", exp.artifact_location)
with mlflow.start_run(experiment_id=exp_id) as run:
    fig, ax = plt.subplots(); ax.plot([1, 2, 3], [1, 4, 9]); ax.set_title("demo")
    mlflow.log_figure(fig, "plots/curve.png")
    mlflow.log_dict({"lr": 0.1, "features": ["a", "b"]}, "cfg/config.json")
    mlflow.log_text("hello run", "notes/readme.txt")
    pd.DataFrame({"id": [1, 2], "pred": [0.2, 0.9]}).to_csv("preds.csv", index=False)
    mlflow.log_artifact("preds.csv", artifact_path="outputs")           # one file
    os.makedirs("many", exist_ok=True)
    for i in range(2): open(f"many/part{i}.txt", "w").write(str(i))
    mlflow.log_artifacts("many", artifact_path="shards")                 # a whole folder
    mlflow.log_table(pd.DataFrame({"q": ["a", "b"], "score": [1, 2]}), "tables/eval.json")
    print("run artifact_uri:", run.info.artifact_uri)
    rid = run.info.run_id
c = mlflow.MlflowClient()
def walk(p=None, ind=""):
    for f in c.list_artifacts(rid, p):
        print(ind + f.path + ("/" if f.is_dir else ""))
        if f.is_dir: walk(f.path, ind + "  ")
print("listing:"); walk()
d = mlflow.artifacts.download_artifacts(run_id=rid, artifact_path="cfg/config.json", dst_path="dl")
print("downloaded ->", os.path.relpath(d), json.load(open(d)))
d2 = mlflow.artifacts.download_artifacts(run_id=rid, artifact_path="outputs/preds.csv", dst_path="dl")
print("csv back:", pd.read_csv(d2).to_dict("list"))
print("text back:", mlflow.artifacts.load_text(f"runs:/{rid}/notes/readme.txt"))
```
```bash
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
rm -rf /tmp/claude-0/b4q24_art_root
W=$(mktemp -d /tmp/claude-0/b4q24.XXXX); cd $W
python3 -I "$D/q24.py" 2>&1 | grep -v "INFO\|Downloading"
```
**Output (my run):** Real run, MLflow 3.17.2, local file artifact root.
```text
artifact_location fixed at creation: file:///tmp/claude-0/b4q24_art_root
run artifact_uri: file:///tmp/claude-0/b4q24_art_root/09ab9c5dedff4590a99061ca4384dda8/artifacts
listing:
cfg/
  cfg/config.json
notes/
  notes/readme.txt
outputs/
  outputs/preds.csv
plots/
  plots/curve.png
shards/
  shards/part0.txt
  shards/part1.txt
tables/
  tables/eval.json
downloaded -> dl/config.json {'lr': 0.1, 'features': ['a', 'b']}
csv back: {'id': [1, 2], 'pred': [0.2, 0.9]}
text back: hello run
```
Not executed: S3 or other object stores, `--serve-artifacts` against a remote server, and cross-machine path problems. Validation that did run: the artifact location is a plain path that I fixed at experiment creation and every file came back with the right content.
**Follow-ups:**
- *Can I move artifacts to another bucket?* You copy the files and update the stored location. Plan this early; check current docs.
- *Where does the model go?* `log_model` is an artifact folder plus a registered model entry (Q8, Q22).
- *Large files?* Log a pointer and a hash (a DVC hash from Q15) instead of copying a dataset into every run.
**Common mistakes:**
- Creating the experiment before the server's artifact root is right, then discovering it is stuck.
- Giving every laptop its own S3 keys instead of using proxied access.
- Logging a 5 GB dataset into every run.

### Q25 ⭐⭐ 🟡 Governing the model registry beyond aliases: descriptions, tags (validation_status, data_version, owner), model version tags, who can register or move an alias (permissions need an authenticated server or a managed platform; check current docs), the audit question 'who moved champion to version 7 and when', and rollback by moving the alias back. Show a script that registers two versions, tags them, moves the alias and prints the version history with timestamps from the client API. Automated promotion gates belong to Part 7; authentication on a server is not executed.
**Asked at:** MLflow Model Registry sources (mlflow.org registry docs, MLflow GitHub issue on stage deprecation, ZenML MLflow registry page, Databricks community and knowledge-base posts; search snippets only, not opened); docs and community posts, not interview reports; MLOps roles using MLflow or Databricks
**Say this first (1 line):** Aliases say which version is live, but governance needs more: tags for status and owner, a note for every move, and permissions on who may move an alias. The audit trail is mostly something I add myself.
**Then explain:**
- Model versions carry tags (for example `validation_status`, `data_version`, `owner`) and a registered model has a description. The client API also returns a creation time for each version.
- Moving an alias is one call, `set_registered_model_alias`. Rollback is the same call pointed at the old version.
- What the client API did NOT give me in this run: who moved the alias and when. The alias map shows only the current target. So I wrap the move in a helper that writes `promoted_by`, `promoted_at` and a note as tags, ideally also to an append-only log outside MLflow.
- Tags keep only the last value per key. My rollback overwrote the first release note on v1 (see the output): history in tags is lossy. Use an external log, or one tag key per event.
- Who may move an alias: a plain local or open server has no per-user permission. An authenticated server, or a managed platform (Databricks, Azure ML, SageMaker), adds that. Check current docs. Not executed here.
- Edge case: `search_model_versions` returned an empty `aliases` list for a version that does hold an alias, while `get_model_version` showed it. Use `get_model_version` or the model's alias map when you need aliases.
**Example:** Two versions. v1 is `pending`, v2 is `approved`. Alias goes v1 (first release), then v2, then back to v1. Hand check: after the rollback the alias map must read `{'champion': 1}`, and the v1 note must say `v2 -> v1`.
**Code:** Registers `iris_gov` twice (C=0.1, then C=5.0), tags the versions, moves the alias with an audit helper, rolls back and prints the history.
```python
# Q25: register two versions, tag them, move the alias, print history from the client API.
import time, datetime as dt, mlflow
from mlflow import MlflowClient
from mlflow.models import infer_signature
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
mlflow.set_tracking_uri("sqlite:///mlflow.db")
c = MlflowClient(); NAME = "iris_gov"
X, y = load_iris(return_X_y=True, as_frame=True)
for C in (0.1, 5.0):
    m = LogisticRegression(C=C, max_iter=300).fit(X, y)
    with mlflow.start_run() as r:
        mlflow.log_param("C", C)
        mlflow.sklearn.log_model(m, name="model", signature=infer_signature(X, m.predict(X)), registered_model_name=NAME)
    v = c.search_model_versions(f"name='{NAME}'")[0].version      # newest first
    c.set_model_version_tag(NAME, v, "validation_status", "approved" if C == 5.0 else "pending")
    c.set_model_version_tag(NAME, v, "data_version", "md5:abc123")
    c.set_model_version_tag(NAME, v, "owner", "team-risk")
    time.sleep(1.1)
c.update_registered_model(NAME, description="Iris classifier (demo). Owner: team-risk.")

def move_alias(alias, to_version, who, why):
    """Audit trail is OUR job: the server stores the alias but not who moved it."""
    old = None
    try: old = c.get_model_version_by_alias(NAME, alias).version
    except Exception: pass
    c.set_registered_model_alias(NAME, alias, to_version)
    c.set_model_version_tag(NAME, to_version, "promoted_by", who)
    c.set_model_version_tag(NAME, to_version, "promoted_at", dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"))
    c.set_model_version_tag(NAME, to_version, "promotion_note", f"{alias}: v{old or '-'} -> v{to_version}; {why}")

move_alias("champion", "1", "asha", "first release")
move_alias("champion", "2", "dev", "better CV score")
print("champion now v", c.get_model_version_by_alias(NAME, "champion").version, "| rollback = move it back:")
move_alias("champion", "1", "asha", "rollback, v2 latency regression")
print("champion after rollback: v", c.get_model_version_by_alias(NAME, "champion").version)

print("\nversion history")
for mv in [c.get_model_version(NAME, v) for v in ("1", "2")]:
    t = dt.datetime.fromtimestamp(mv.creation_timestamp / 1000, dt.timezone.utc).strftime("%H:%M:%S")
    print(f"v{mv.version} created {t}Z aliases={mv.aliases} run={mv.run_id[:8]}")
    for k in sorted(mv.tags): print(f"    {k} = {mv.tags[k]}")
rm = c.get_registered_model(NAME)
print("\nmodel description:", rm.description, "| aliases map:", rm.aliases)
```
```bash
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q25.XXXX); cd $W
python3 -I "$D/q25.py" 2>&1 | grep -v "INFO\|Downloading\|WARNING\|Registered model\|Created version\|^$"
```
**Output (my run):** Real run, MLflow 3.17.2, sqlite registry. Timestamps are from my run.
```text
Successfully registered model 'iris_gov'.
champion now v 2 | rollback = move it back:
champion after rollback: v 1
version history
v1 created 14:07:56Z aliases=['champion'] run=b03d93f0
    data_version = md5:abc123
    owner = team-risk
    promoted_at = 2026-10-26T14:08:02+00:00
    promoted_by = asha
    promotion_note = champion: v2 -> v1; rollback, v2 latency regression
    validation_status = pending
v2 created 14:08:01Z aliases=[] run=9c75ad41
    data_version = md5:abc123
    owner = team-risk
    promoted_at = 2026-10-26T14:08:02+00:00
    promoted_by = dev
    promotion_note = champion: v1 -> v2; better CV score
    validation_status = approved
model description: Iris classifier (demo). Owner: team-risk. | aliases map: {'champion': 1}
```
Not executed: authentication, permissions and any server that records who made a change. The tags above are written by my helper, not by MLflow.
**Follow-ups:**
- *Who moved champion to v7?* Only what my helper and the server's own logs recorded. A managed platform may keep an audit log; check current docs.
- *Should CI move the alias?* Yes, with a service account and a gate. Part 7 owns that.
- *Tags or aliases for status?* Aliases for pointers (one version holds it); tags for facts about a version.
**Common mistakes:**
- Treating the alias map as an audit log.
- Putting status only in the model name (`iris_prod_v2`).
- Letting every data scientist move `champion` from a notebook.

### Q26 ⭐⭐ 🟡 Weights & Biases sweeps. Explain a sweep config (method grid, random or bayes, metric goal, parameter ranges and distributions), wandb.sweep, wandb.agent and running agents on several machines, early termination (Hyperband), and cost control (max runs). Compare with Optuna and with MLflow plus Optuna. Write a sweep configuration and validate it with a Python script (parse YAML, check ranges and the metric name); wandb.sweep and agents need an account and network and are not executed.
**Asked at:** Weights & Biases sources (techinterview.org 'Weights & Biases Interview Guide', KDnuggets 'Weights & Biases crash course', TWIML podcast on managing ML artifacts, wandb.ai articles; search snippets only, not opened); guide and docs, not verified candidate reports; ML engineer and MLOps roles at AI-lab and product companies
**Say this first (1 line):** A W&B sweep is a hyperparameter search run by W&B. I write a config (method, metric, parameters), call `wandb.sweep`, then run one or more `wandb.agent` processes that pull the next set of parameters.
**Then explain:**
- Config: `method` is `grid`, `random` or `bayes`; `metric` has a name and a goal; `parameters` are either `values` (a list) or a distribution with min and max.
- The metric name must match what the script logs with `wandb.log`. A typo means bayes and early termination have nothing to optimise. My validator catches this against a list of logged names.
- Agents can run on many machines against the same sweep id. Cost control: cap runs with the `count` argument of `wandb.agent` (and a stop rule on the sweep; check current docs for the exact option). Early termination (`hyperband`) stops weak runs early.
- Grid with ranges does not make sense; grid needs discrete values and multiplies fast (5 x 5 x 3 x 2 = 150 runs).
- Versus Optuna: Optuna is a library that runs in your own process with pruning and storage you choose; W&B sweeps give a hosted controller and a dashboard. Optuna plus MLflow logging gives a fully self-hosted setup. Both are fine; the choice is about where you want the controller and the UI.
**Example:** `lr` log-uniform from 1e-4 to 1e-1, `batch_size` from [16, 32, 64], `dropout` uniform from 0 to 0.5, `optimizer` adam or sgd, bayes on `val_auc` (maximise) with hyperband. Hand check: `min < max`, `lr` min above 0 (log), metric is one that `train.py` logs.
**Code:** `sweep.yaml`, the offline validator (pyyaml only), the helper that tries `wandb.sweep` without an account, and the driver.
```yaml
program: train.py
method: bayes
metric:
  name: val_auc
  goal: maximize
parameters:
  lr:
    distribution: log_uniform_values
    min: 0.0001
    max: 0.1
  batch_size:
    values: [16, 32, 64]
  dropout:
    distribution: uniform
    min: 0.0
    max: 0.5
  optimizer:
    values: [adam, sgd]
early_terminate:
  type: hyperband
  min_iter: 3
  eta: 3
```
```python
# --- q26/validate_sweep.py ---
# Q26: validate a W&B sweep config offline (pyyaml only; no wandb import, no network).
import sys, yaml
METHODS = {"grid", "random", "bayes"}
DISTS_RANGE = {"uniform", "int_uniform", "log_uniform_values", "q_uniform", "q_log_uniform_values"}
def check(cfg, logged_metrics):
    errs = []
    if cfg.get("method") not in METHODS: errs.append(f"method must be one of {sorted(METHODS)}, got {cfg.get('method')!r}")
    m = cfg.get("metric", {})
    if cfg.get("method") == "bayes" and not m: errs.append("bayes needs a metric block")
    if m and m.get("goal") not in {"minimize", "maximize"}: errs.append(f"metric.goal invalid: {m.get('goal')!r}")
    if m and m.get("name") not in logged_metrics: errs.append(f"metric.name {m.get('name')!r} is never logged by train.py (known: {sorted(logged_metrics)})")
    params = cfg.get("parameters") or {}
    if not params: errs.append("no parameters")
    for k, p in params.items():
        if "values" in p:
            if not p["values"]: errs.append(f"{k}: empty values")
        elif "value" in p: pass
        else:
            d = p.get("distribution", "uniform")
            if d in DISTS_RANGE:
                lo, hi = p.get("min"), p.get("max")
                if lo is None or hi is None: errs.append(f"{k}: {d} needs min and max")
                elif lo >= hi: errs.append(f"{k}: min {lo} must be < max {hi}")
                elif d.startswith(("log", "q_log")) and lo <= 0: errs.append(f"{k}: log distribution needs min > 0")
            else: errs.append(f"{k}: unknown distribution {d!r}")
        if cfg.get("method") == "grid" and "values" not in p and "value" not in p:
            errs.append(f"{k}: grid search needs discrete values, not a range")
    if "early_terminate" in cfg and cfg["early_terminate"].get("type") != "hyperband":
        errs.append("early_terminate.type should be hyperband")
    return errs

cfg = yaml.safe_load(open("sweep.yaml"))
logged = {"val_auc", "val_loss", "train_loss"}
print("good config  ->", check(cfg, logged) or "OK")
bad = yaml.safe_load(open("sweep.yaml"))
bad["method"] = "grid"; bad["metric"]["name"] = "val_acc"
bad["parameters"]["lr"]["min"] = 0.5
bad["parameters"]["dropout"]["distribution"] = "normalish"
print("broken config ->")
for e in check(bad, logged): print("   -", e)
print("grid blow-up check: 5 lr values * 5 dropout values * 3 batch sizes * 2 optimizers =", 5*5*3*2, "runs")

# --- q26/try_sweep.py ---
# Shows what happens when you call wandb.sweep with no account/network (offline mode).
import wandb, yaml
cfg = yaml.safe_load(open("sweep.yaml"))
try:
    sid = wandb.sweep(cfg, project="demo")
    print("sweep id:", sid)
except Exception as e:
    print(type(e).__name__ + ":", str(e).splitlines()[0][:200])
```
```bash
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q26.XXXX); cd $W; cp $D/sweep.yaml .
python3 -I "$D/validate_sweep.py"
echo "--- wandb.sweep with no account (WANDB_MODE=offline) ---"
timeout 60 python3 -I "$D/try_sweep.py" 2>&1 | tail -3
```
**Output (my run):** The validator is my own checker (not a W&B tool) and covers only the rules in the code. The last line is the real `wandb.sweep` failure without an account (wandb 0.31.0).
```text
good config  -> OK
broken config ->
   - metric.name 'val_acc' is never logged by train.py (known: ['train_loss', 'val_auc', 'val_loss'])
   - lr: min 0.5 must be < max 0.1
   - lr: grid search needs discrete values, not a range
   - dropout: unknown distribution 'normalish'
   - dropout: grid search needs discrete values, not a range
grid blow-up check: 5 lr values * 5 dropout values * 3 batch sizes * 2 optimizers = 150 runs
--- wandb.sweep with no account (WANDB_MODE=offline) ---
UsageError: No API key configured. Use `wandb login` to log in.
```
Not executed: `wandb.sweep` and `wandb.agent` for real (they need an account and network), hyperband behaviour, multi-machine agents. Validation that did run: the YAML parses and passes my checks; the broken copy produces five errors.
**Follow-ups:**
- *Random or bayes?* Random is a safe start and parallelises easily; bayes helps when each run is costly and the space is smooth.
- *How do I stop a runaway sweep?* Cap the count per agent and stop the sweep from the UI or CLI; check current docs.
- *Selection bias?* The best of N runs on validation is optimistic. Use a held-out test set once (Q11).
**Common mistakes:**
- Metric name in the config differs from the logged key.
- A grid sweep over continuous ranges.
- Leaving agents running overnight with no run cap.

### Q27 ⭐⭐ 🟡 W&B Artifacts and lineage. Explain Artifact(type, name), add_file, add_dir, log_artifact, use_artifact, the automatic versions v0, v1 and aliases such as latest, the lineage graph between runs and artifacts, references to files in S3 without copying, and how this compares to DVC (pointers in Git) and MLflow (artifacts attached to a run). Show the code and test what can be done offline (building an Artifact object locally and checking its digest or file manifest, if the library allows); logging to the service is not executed.
**Asked at:** Weights & Biases sources (techinterview.org 'Weights & Biases Interview Guide', KDnuggets 'Weights & Biases crash course', TWIML podcast on managing ML artifacts, wandb.ai articles; search snippets only, not opened); guide and docs, not verified candidate reports; ML engineer and MLOps roles at AI-lab and product companies
**Say this first (1 line):** A W&B Artifact is a versioned bundle of files. `log_artifact` creates a version (v0, v1, ...), `use_artifact` consumes one, and W&B draws the lineage graph between runs and artifacts for you.
**Then explain:**
- Build: `wandb.Artifact(name, type)`, then `add_file`, `add_dir`, or `add_reference` (a pointer to a file in a bucket or URL; the bytes are not copied).
- The versions `v0`, `v1` and aliases like `latest` are assigned by the server when you log. Offline I could build the artifact and read its manifest and digest, but not see a version number.
- Same content gives the same digest; one more row in the CSV gives a different digest (output below). That is the same content-addressing idea as DVC hashes.
- Compare: DVC keeps pointers in Git and the bytes in a remote you own. MLflow attaches artifacts to a run. W&B keeps versions and lineage in its service (cloud or self-hosted).
- Failure modes: an `s3://` reference needs boto3 and credentials; here it failed with a clear error. A reference artifact points at data that someone else can change or delete, so a checksum matters.
**Example:** A dataset artifact with `train.csv`, an image folder and a reference to a remote parquet file has 3 manifest entries. After appending one row to `train.csv`, the artifact digest must change. Both hold in the output.
**Code:** Builds the artifact locally with `wandb 0.31.0`, prints the manifest and digests, and shows the S3 reference error. The two lines at the end are the real service calls that I did not run.
```python
# Q27: W&B Artifact built locally. Nothing is uploaded; we inspect the manifest/digest.
import os, wandb
os.makedirs("data/imgs", exist_ok=True)
open("data/train.csv", "w").write("x,y\n1,2\n3,4\n")
open("data/imgs/a.txt", "w").write("img-a")

def build(extra=None):
    art = wandb.Artifact("train-data", type="dataset", description="tiny demo", metadata={"rows": 2})
    art.add_file("data/train.csv")
    art.add_dir("data/imgs", name="imgs")
    art.add_reference("https://example.com/raw/events.parquet", name="raw_events", checksum=False)   # pointer, nothing copied (s3:// works the same but needs boto3 + credentials)
    if extra: art.add_file(extra)
    return art

a1 = build()
print("name:", a1.name, "| type:", a1.type, "| size entries:", len(a1.manifest.entries))
for path, e in sorted(a1.manifest.entries.items()):
    print(f"  {path:16} digest={e.digest[:12]}... ref={e.ref}")
print("artifact digest v1:", a1.digest)
a1b = build()
print("same content, rebuilt -> same digest?", a1b.digest == a1.digest)
open("data/train.csv", "a").write("5,6\n")
a2 = build()
print("one row appended -> new digest?", a2.digest != a1.digest)
print("version/aliases before upload:", getattr(a1, "version", None), "| (v0/v1/latest are assigned by the server on log_artifact)")
try:
    a1.add_reference("s3://my-bucket/raw/events.parquet", name="s3ref")   # needs boto3 (and creds to checksum)
except Exception as e:
    print("s3:// reference here ->", type(e).__name__ + ":", str(e)[:90])
# the real lineage calls, shown but NOT run:
print("\nnot run: run.log_artifact(a2, aliases=['latest']) / run.use_artifact('train-data:v0') need an account")
```
```bash
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q27.XXXX); cd $W
timeout 90 python3 -I "$D/q27.py" 2>&1 | tail -30
```
**Output (my run):** Real offline run. Nothing was uploaded. The first line is wandb's own progress message.
```text
wandb: Adding directory to artifact (data/imgs)... Done. 0.0s
name: train-data | type: dataset | size entries: 3
  imgs/a.txt       digest=BkMMzP4kwnLZ... ref=None
  raw_events       digest=https://exam... ref=https://example.com/raw/events.parquet
  train.csv        digest=F4uoVwdHDEHP... ref=None
artifact digest v1: f6fe2d8e2ac987a649f41e7d1fe2b6fc
same content, rebuilt -> same digest? True
one row appended -> new digest? True
version/aliases before upload: None | (v0/v1/latest are assigned by the server on log_artifact)
s3:// reference here -> Error: s3:// references requires the boto3 library, run pip install wandb[aws]

not run: run.log_artifact(a2, aliases=['latest']) / run.use_artifact('train-data:v0') need an account
```
Not executed: `run.log_artifact`, `run.use_artifact`, version numbers and aliases, the lineage graph, S3 references. They need an account and network. Validation that did run: artifact manifests and digests built locally.
**Follow-ups:**
- *Can I use W&B Artifacts without W&B runs?* There are API calls for it; not tested here, check current docs.
- *How do I pin a version?* `use_artifact('train-data:v3')`. An alias like `latest` moves, so pin a version in training code.
- *Lineage gap?* Only objects logged through W&B are in the graph. Raw tables upstream are not.
**Common mistakes:**
- Using `latest` in a training script and losing reproducibility.
- Using references for data that can change, with no checksum.
- Assuming offline mode gives versions; they appear after sync or log.

### Q28 ⭐⭐ 🟡 Choosing an experiment tracker: MLflow, Weights & Biases, Neptune, Comet, TensorBoard, or a cloud-native one (SageMaker Experiments, Vertex AI Experiments, Azure ML). Give a decision table: self-hosting effort, cost model, collaboration and dashboards, registry features, access control, data residency, lock-in and portability (MLflow format as common ground). Add the India angle: data protection obligations under the Digital Personal Data Protection Act and company rules on sending metadata to a foreign SaaS (hedge, not legal advice) and the common use of MLflow on Databricks, Azure ML or SageMaker in IT-services and GCC teams. Pure comparison; nothing is executed.
**Asked at:** Bengaluru and India MLOps job postings that list DVC, MLflow and experiment tracking (weekday.works, builtinbengaluru, GrabJobs listings seen while researching Parts 2 and 3; snippets only) plus editorial MLOps guides; postings show required skills, not interview questions; IT-services firms, GCCs and AI product companies in India
**Say this first (1 line):** I choose the tracker by who runs it and who may see the data. MLflow is the open, self-hosted default. W&B is the polished hosted one. Cloud-native trackers fit if the whole stack is on one cloud.
**Then explain:**
- Decision table (my summary, hedged; check each vendor's current plans and terms; no prices here):

| Criterion | MLflow | W&B | Neptune / Comet | TensorBoard | Cloud-native (SageMaker, Vertex, Azure ML) |
|---|---|---|---|---|---|
| Hosting | You host it, or a managed one | Hosted first; self-host option | Hosted first | Local files | Inside the cloud account |
| Setup effort | Server, database, artifact store, auth | Almost none | Almost none | None | Low, but cloud lock-in |
| Dashboards, sweeps | Basic UI, no built-in sweeps | Strong UI, sweeps built in | Strong UI | Good for curves | Varies |
| Registry | Yes (aliases, tags) | Yes (artifact-based) | Varies | No | Yes, platform's own |
| Access control | Needs plugin, proxy or managed platform | Teams and roles in the service | Same | OS file permissions | Cloud IAM |
| Data residency | Wherever you deploy | Depends on plan and region; check | Same | Local | Region of the cloud account |
| Portability | MLflow model format is a common ground | Export APIs exist | Export APIs exist | Event files | Often MLflow-compatible; check |

- Questions that decide it: can metadata (run names, params, sometimes sample data) leave our network? who patches and backs up the server? do we need a registry and approvals? how many users?
- India angle (hedge, not legal advice): the Digital Personal Data Protection Act means that if run metadata or logged samples contain personal data, sending it to a foreign SaaS needs a review with the privacy or legal team. Many IT-services and GCC teams use MLflow on Databricks, Azure ML or SageMaker because it sits inside an approved cloud account (this is my observation of the market, not sourced).
- Failure mode: picking a tracker because the demo looked nice, then finding that logged samples contain customer data.
**Example:** A bank team with strict data rules and 15 data scientists on Azure: managed MLflow in Azure ML, no SaaS egress. A three-person startup with GPUs on rented machines: W&B hosted free tier (check current terms) for speed.
**Code:** No code. This is a pure comparison.
**Output (my run):** not executed. Nothing to run; this is a comparison written from general knowledge, not from opened vendor pages. Check current docs and terms for every row.

**Follow-ups:**
- *Can I switch later?* Params and metrics export easily; dashboards and reports do not. Keep the model in MLflow format and the data in DVC.
- *Do I need both MLflow and W&B?* Usually not (Q14). Some teams use W&B for experiments and MLflow for the registry; that doubles the logging code.
- *Self-host W&B?* An option exists on some plans; check current terms.
**Common mistakes:**
- Comparing price lists from memory.
- Ignoring data residency until a security review.
- Treating the tracker as the system of record for data versions.

### Q29 ⭐⭐ 🟡 Model cards and documentation for a registered model. Explain what a model card contains (intended use, training data and version, metrics overall and per slice, limitations, ethical considerations, owner, how to retrain), why it should be generated from the run and registry data rather than written by hand, and how to attach it as an MLflow artifact or tag and as a markdown file in the repo. Write a script that builds a model card from an MLflow run and registered version (params, metrics, tags, signature) and run it. Hedge the template source (Mitchell et al. model cards; check current docs).
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** A model card is a short, standard document about a model: what it is for, what data it was trained on, how well it works (overall and on slices), its limits and its owner. I generate the factual parts from MLflow so it cannot drift from the run.
**Then explain:**
- Contents (from the Mitchell et al. model card idea; check current docs for template variants): intended use, training data and version, parameters, metrics overall and per slice, inputs and outputs, limitations and ethics, owner, how to retrain.
- Facts come from the run and registry: params, metrics, tags, signature, run id. Judgement parts (intended use, limits) stay human-written and are marked as such in my script.
- Attach it two ways: as an artifact on the training run (`MODEL_CARD.md`) and as a pointer tag on the registered version; also commit the markdown in the repo for review.
- Failure modes: a stale card (written once, never regenerated); a missing tag silently becoming an empty field (my script prints `MISSING` and reports it); slice metrics on very few rows look precise but mean little (the demo test set has 15 and 30 rows).
- A card does not replace tests. It documents what was tested.
**Example:** Iris model v1: tags carry the data version and git SHA (demo values), three accuracy metrics, four double inputs. All appear in the card; a tag removed from the run would show as `MISSING`. Test accuracy is 1.000 on only 45 test rows, so I would say so.
**Code:** Trains, registers, and builds the markdown from the stored run and signature, logs it back to the run and sets a pointer tag.
```python
# Q29: generate a model card (markdown) from MLflow run + registry data, log it back as an artifact.
import json, mlflow
from mlflow import MlflowClient
from mlflow.models import infer_signature
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
mlflow.set_tracking_uri("sqlite:///mlflow.db"); c = MlflowClient(); NAME = "iris_card"

# --- train + log (slice = petal length bucket) ---
X, y = load_iris(return_X_y=True, as_frame=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
m = LogisticRegression(C=1.0, max_iter=300).fit(Xtr, ytr)
pred = m.predict(Xte)
with mlflow.start_run() as run:
    mlflow.log_params({"C": 1.0, "max_iter": 300, "test_size": 0.3, "seed": 0})
    mlflow.log_metric("test_acc", accuracy_score(yte, pred))
    short = Xte["petal length (cm)"] < 3
    mlflow.log_metric("acc_slice_short_petal", accuracy_score(yte[short], pred[short]))
    mlflow.log_metric("acc_slice_long_petal", accuracy_score(yte[~short], pred[~short]))
    mlflow.set_tags({"data_version": "md5:abc123 (demo)", "git_sha": "deadbeef (demo)", "owner": "team-risk"})
    mlflow.sklearn.log_model(m, name="model", signature=infer_signature(Xtr, m.predict(Xtr)), registered_model_name=NAME)
c.set_registered_model_alias(NAME, "champion", 1)

# --- build the card from stored facts, never from memory ---
def card(name, alias):
    mv = c.get_model_version_by_alias(name, alias)
    r = c.get_run(mv.run_id)
    sig = mlflow.models.get_model_info(f"models:/{name}@{alias}").signature.to_dict()
    L = [f"# Model card: {name} (v{mv.version}, alias {alias})", "",
         "## Intended use", "- Classify iris species from 4 measurements. Demo only, not for botanical decisions. (hand-written field)", "",
         "## Training data", f"- data_version: {r.data.tags.get('data_version', 'MISSING')}", f"- code: git {r.data.tags.get('git_sha', 'MISSING')}", "",
         "## Parameters"] + [f"- {k}: {v}" for k, v in sorted(r.data.params.items())] + ["", "## Metrics", "| metric | value |", "|---|---|"]
    L += [f"| {k} | {v:.3f} |" for k, v in sorted(r.data.metrics.items())]
    L += ["", "## Inputs", "| name | type |", "|---|---|"] + [f"| {i['name']} | {i['type']} |" for i in json.loads(sig["inputs"])]
    L += ["", "## Limitations", "- Only 150 rows; slice metrics rest on few test rows, check the counts before trusting them. (hand-written field)",
          f"- Owner: {r.data.tags.get('owner', 'MISSING')}", f"- Run: {mv.run_id}", ""]
    missing = [l for l in L if "MISSING" in l]
    return "\n".join(L), missing

text, missing = card(NAME, "champion")
print(text); print("fields missing:", missing or "none")
with mlflow.start_run(run_id=c.get_model_version_by_alias(NAME, "champion").run_id):
    mlflow.log_text(text, "MODEL_CARD.md")
open("MODEL_CARD.md", "w").write(text)
c.set_model_version_tag(NAME, "1", "model_card", "artifact: MODEL_CARD.md on the training run")
print("slice sizes in the test set: short petal =", int(short.sum()), ", long petal =", int((~short).sum()))
```
```bash
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q29.XXXX); cd $W
python3 -I "$D/q29.py" 2>&1 | grep -v "INFO\|Downloading\|WARNING\|Registered model\|Created version"
```
**Output (my run):** Real run, MLflow 3.17.2. The git SHA and data version are made-up demo strings.
```text
Successfully registered model 'iris_card'.
# Model card: iris_card (v1, alias champion)

## Intended use
- Classify iris species from 4 measurements. Demo only, not for botanical decisions. (hand-written field)

## Training data
- data_version: md5:abc123 (demo)
- code: git deadbeef (demo)

## Parameters
- C: 1.0
- max_iter: 300
- seed: 0
- test_size: 0.3

## Metrics
| metric | value |
|---|---|
| acc_slice_long_petal | 1.000 |
| acc_slice_short_petal | 1.000 |
| test_acc | 1.000 |

## Inputs
| name | type |
|---|---|
| sepal length (cm) | double |
| sepal width (cm) | double |
| petal length (cm) | double |
| petal width (cm) | double |

## Limitations
- Only 150 rows; slice metrics rest on few test rows, check the counts before trusting them. (hand-written field)
- Owner: team-risk
- Run: f616288f7b38446391fa08fba2e99e41

fields missing: none
slice sizes in the test set: short petal = 15 , long petal = 30
```

**Follow-ups:**
- *Who owns the card?* The model owner, with review in the PR. The facts are generated.
- *Per-slice metrics?* Pick slices in advance (region, device, age band) and log them as metrics, as the demo does with petal length.
- *Regulated settings?* The card feeds the audit file (Q40), it is not the audit file.
**Common mistakes:**
- Hand-typing metrics into a Word file.
- One overall number and no slices.
- No owner and no retrain instructions.

### Q30 ⭐⭐ 🔴 Table-format time travel versus ML data versioning: Delta Lake and Apache Iceberg time travel (query a table as of a version or timestamp, snapshots, retention and vacuum or expire-snapshots limits) versus DVC (file-level pointers) and lakeFS (branches over an object store). Explain which you use for an analytics table that feeds a feature pipeline, which for an image dataset, which for a training snapshot that must exist for years, and what happens when old snapshots are vacuumed. Concept level only: no Spark, Delta or Iceberg cluster is available here; a pure-Python toy snapshot table can be run to show the idea.
**Asked at:** Data-versioning comparison write-ups (lakeFS blog 'scalable data version control', kanerika data versioning tools, pdpspectra 'DVC vs lakeFS', jisaku glossary; search snippets only, not opened); vendor-written or low-quality blogs, treat specifics with caution; data and ML platform roles
**Say this first (1 line):** Delta and Iceberg give time travel over one table, inside the table format, until old snapshots are vacuumed. DVC pins whole files by hash in Git. lakeFS branches a whole object store. I pick by the data shape and by how long the snapshot must live.
**Then explain:**
- Delta Lake and Iceberg: every commit writes a new snapshot (a manifest listing immutable data files). You query a version or a timestamp (`VERSION AS OF`, `TIMESTAMP AS OF` in Delta; Iceberg has the same idea; check current docs for syntax). Concept level here: no cluster available.
- Retention: `VACUUM` (Delta) and `expire_snapshots` (Iceberg) delete files no kept snapshot needs. After that, time travel to the older version fails. Defaults and safe minimums exist; check current docs.
- DVC: file or folder level, content-hash pointers in Git, bytes in a cache and remote. It lasts as long as the remote keeps the hash and Git keeps the tag. It does not understand rows.
- lakeFS: branches, commits and merges over an object store, zero-copy; good for ingest-validate-merge on lots of files. Some sources report a changed stewardship of DVC (unverified; check news).
- Choice: analytics table feeding features: Delta or Iceberg (rows, schema evolution, SQL). Image dataset: DVC or lakeFS (files). Training snapshot that must live for years: copy that snapshot out to a protected, immutable location and pin it by hash (DVC tag, or a table version that is explicitly excluded from vacuum); never rely on the default retention.
- Failure mode (shown below): the snapshot a model was trained on shares files with other versions; one vacuum removes them and the model can no longer be reproduced.
**Example:** Version 0 has ids 1 and 2. Version 1 adds id 3. Version 2 rewrites the first file (id 2 changes from 20 to 25). Training used version 1. Vacuum keeping only the latest version deletes `data-v0-0.json`, which v1 also needs. Hand check: both v0 and v1 now fail.
**Code:** A pure-Python toy snapshot table (about 40 lines): immutable data files, one manifest per version, `read(version)`, `read(ts=...)` and `vacuum`. It teaches the idea only; it is not Delta or Iceberg code.
```python
# Q30: toy snapshot table (Delta/Iceberg idea in 60 lines): immutable data files + a manifest per version.
import json, os, tempfile, time
class ToyTable:
    def __init__(self, root): self.root = root; os.makedirs(root, exist_ok=True); self.log = []   # log[i] = manifest of version i
    def _write(self, name, rows):
        with open(os.path.join(self.root, name), "w") as f: json.dump(rows, f)
    def commit(self, add=(), remove=()):
        files = list(self.log[-1]["files"]) if self.log else []
        files = [f for f in files if f not in remove]
        for i, rows in enumerate(add):
            n = f"data-v{len(self.log)}-{i}.json"; self._write(n, rows); files.append(n)
        self.log.append({"version": len(self.log), "ts": time.time(), "files": files})   # files never edited in place
        return len(self.log) - 1
    def read(self, version=None, ts=None):
        if ts is not None: version = max(m["version"] for m in self.log if m["ts"] <= ts)
        m = self.log[-1 if version is None else version]
        rows = []
        for f in m["files"]:
            p = os.path.join(self.root, f)
            if not os.path.exists(p): raise FileNotFoundError(f"version {m['version']} needs {f}, which was vacuumed")
            rows += json.load(open(p))
        return rows
    def vacuum(self, keep_last_n):
        """Delete data files that no kept version references (like VACUUM / expire_snapshots)."""
        keep = {f for m in self.log[-keep_last_n:] for f in m["files"]}
        gone = [f for f in os.listdir(self.root) if f not in keep]
        for f in gone: os.remove(os.path.join(self.root, f))
        return sorted(gone)

t = ToyTable(tempfile.mkdtemp(prefix="toy_", dir="/tmp/claude-0"))
v0 = t.commit(add=[[{"id": 1, "amt": 10}, {"id": 2, "amt": 20}]]); time.sleep(0.05); mid = time.time(); time.sleep(0.05)
v1 = t.commit(add=[[{"id": 3, "amt": 30}]])
v2 = t.commit(add=[[{"id": 1, "amt": 10}, {"id": 2, "amt": 25}]], remove=["data-v0-0.json"])   # rewrite file: id 2 amt 20 -> 25
print("v0 rows:", len(t.read(0)), "| v1 rows:", len(t.read(1)), "| v2 rows:", len(t.read(2)))
print("as of timestamp 'mid' ->", [r["id"] for r in t.read(ts=mid)], "(version", max(m["version"] for m in t.log if m["ts"] <= mid), ")")
print("train snapshot = version 1 ids/amt:", [(r["id"], r["amt"]) for r in t.read(1)])
print("vacuum keeping only the latest version deletes:", t.vacuum(keep_last_n=1))
print("latest still fine:", [(r["id"], r["amt"]) for r in t.read()])
for v in (1, 0):
    try: t.read(v)
    except FileNotFoundError as e: print(f"time travel to v{v} ->", e)
```
```bash
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
python3 -I "$D/toy_table.py"
```
**Output (my run):** Real run of the toy. It shows retention behaviour, not any real table format.
```text
v0 rows: 2 | v1 rows: 3 | v2 rows: 3
as of timestamp 'mid' -> [1, 2] (version 0 )
train snapshot = version 1 ids/amt: [(1, 10), (2, 20), (3, 30)]
vacuum keeping only the latest version deletes: ['data-v0-0.json']
latest still fine: [(3, 30), (1, 10), (2, 25)]
time travel to v1 -> version 1 needs data-v0-0.json, which was vacuumed
time travel to v0 -> version 0 needs data-v0-0.json, which was vacuumed
```
Not executed: Delta Lake, Iceberg, lakeFS, Spark. Validation that did run: the toy table reproduces the snapshot, timestamp lookup and vacuum failure logic.
**Follow-ups:**
- *Can I combine them?* Yes: Delta table for features, and a DVC pointer to an exported Parquet snapshot for each training run.
- *Why not keep everything forever?* Storage cost and deletion duties (for example a data-protection request). Plan retention and deletion together.
- *Timestamp or version?* Version number is exact; a timestamp depends on clocks and commit times.
**Common mistakes:**
- Assuming time travel is a backup. It stops at the retention window.
- Pinning only the table name and not the version or snapshot id in the training record.
- Running vacuum with a very short retention to save space, with a long-running job still reading.

### Q31 ⭐⭐ 🔴 Why can the same code, seed and data give a different metric, and how do you prove it with run comparison? Explain nondeterminism sources (multithreaded reductions, GPU kernels, hash ordering, data loader order, library versions), how to log the environment (pip freeze, python version, hardware) to the run, how to repeat a run five times and report mean and spread, and when to use a statistical test instead of reading a 0.002 difference. Run a small sklearn experiment with two seeds and a repeat loop, log everything to MLflow and compare. GPU determinism is not executed.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** Same seed does not mean same result once the environment, the hardware, the thread order or the data order changes, so I log all of those to the run, repeat the run with several seeds, and compare means and spread before I believe a 0.002 gap.

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
import os, sys, platform, subprocess, hashlib, json
import numpy as np, sklearn, mlflow
from mlflow.tracking import MlflowClient
from scipy import stats
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# 1. tiny nondeterminism demos (no ML needed)
xs = [0.1] * 10 + [1e16, -1e16] + [0.1] * 10
print("float sum, order A :", sum(xs))
print("float sum, order B :", sum(sorted(xs)))
out = subprocess.run([sys.executable, "-I", "-c", "print(sorted({'a','b','c','d'}))\nprint(list({'a','b','c','d'}))"],
                     env={**os.environ, "PYTHONHASHSEED": "1"}, capture_output=True, text=True).stdout
out2 = subprocess.run([sys.executable, "-I", "-c", "print(list({'a','b','c','d'}))"],
                     env={**os.environ, "PYTHONHASHSEED": "2"}, capture_output=True, text=True).stdout
print("set order, hashseed=1:", out.splitlines()[1], "| hashseed=2:", out2.strip())

# 2. experiment
X, y = make_classification(n_samples=600, n_features=20, n_informative=5, flip_y=0.1, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)

def one(seed, n_jobs=1):
    m = RandomForestClassifier(n_estimators=30, max_depth=6, random_state=seed, n_jobs=n_jobs).fit(Xtr, ytr)
    return m.score(Xte, yte)

print("same seed twice:", one(1), one(1))
print("n_jobs 1 vs 4 same seed:", one(1, 1), one(1, 4))

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("q31-seeds")
env = {"python": platform.python_version(), "sklearn": sklearn.__version__, "numpy": np.__version__,
       "machine": platform.machine(), "os": platform.system(), "cpus": os.cpu_count()}
freeze = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True).stdout
fhash = hashlib.sha256(freeze.encode()).hexdigest()[:12]
dhash = hashlib.sha256(Xtr.tobytes() + ytr.tobytes()).hexdigest()[:12]

scores = {}
for cfg, seeds in {"A_seed_0_to_4": range(0, 5), "B_seed_10_to_14": range(10, 15)}.items():
    scores[cfg] = []
    for s in seeds:
        with mlflow.start_run(run_name=f"{cfg}-{s}"):
            mlflow.set_tags({"config": cfg, "data_hash": dhash, "freeze_hash": fhash})
            mlflow.log_params({"seed": s, "n_estimators": 30, "max_depth": 6, **env})
            mlflow.log_text(freeze, "pip_freeze.txt")
            acc = one(s)
            mlflow.log_metric("accuracy", acc)
            scores[cfg].append(acc)
for k, v in scores.items():
    print(f"{k}: mean={np.mean(v):.4f} std={np.std(v, ddof=1):.4f} min={min(v):.4f} max={max(v):.4f}")
a, b = np.array(scores["A_seed_0_to_4"]), np.array(scores["B_seed_10_to_14"])
print("mean gap A-B: %.4f" % (a.mean() - b.mean()))
t = stats.ttest_ind(a, b, equal_var=False)
print("Welch t-test p = %.3f" % t.pvalue)

df = mlflow.search_runs(experiment_names=["q31-seeds"], order_by=["metrics.accuracy DESC"])
print(df[["tags.config", "params.seed", "metrics.accuracy", "tags.data_hash", "tags.freeze_hash"]].to_string(index=False))
```

**Output (my run):** run in a temp dir with `python -I`, MLflow on `sqlite:///mlflow.db`. Scores can differ a little on other machines or library versions. Versions that ran: Python 3.13, dvc 3.67.1, mlflow 3.17.2, wandb 0.31.0, scikit-learn 1.9.1, tracked in a sqlite backend. Check current docs for newer behaviour.
```text
float sum, order A : 2.0
float sum, order B : 2.0000000000000004
set order, hashseed=1: ['c', 'b', 'a', 'd'] | hashseed=2: ['a', 'b', 'd', 'c']
same seed twice: 0.8555555555555555 0.8555555555555555
n_jobs 1 vs 4 same seed: 0.8555555555555555 0.8555555555555555
A_seed_0_to_4: mean=0.8578 std=0.0101 min=0.8444 max=0.8722
B_seed_10_to_14: mean=0.8500 std=0.0056 min=0.8444 max=0.8556
mean gap A-B: 0.0078
Welch t-test p = 0.180
    tags.config params.seed  metrics.accuracy tags.data_hash tags.freeze_hash
  A_seed_0_to_4           0          0.872222   1087158f6276     b2bcacd332b7
  A_seed_0_to_4           3          0.861111   1087158f6276     b2bcacd332b7
B_seed_10_to_14          14          0.855556   1087158f6276     b2bcacd332b7
B_seed_10_to_14          10          0.855556   1087158f6276     b2bcacd332b7
  A_seed_0_to_4           2          0.855556   1087158f6276     b2bcacd332b7
  A_seed_0_to_4           1          0.855556   1087158f6276     b2bcacd332b7
B_seed_10_to_14          13          0.850000   1087158f6276     b2bcacd332b7
B_seed_10_to_14          12          0.844444   1087158f6276     b2bcacd332b7
B_seed_10_to_14          11          0.844444   1087158f6276     b2bcacd332b7
  A_seed_0_to_4           4          0.844444   1087158f6276     b2bcacd332b7
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

### Q32 ⭐⭐ 🟡 Debugging scenarios for versioning tools, in the order you would check. (1) dvc pull says files are missing from the remote. (2) dvc repro re-runs everything although nothing changed. (3) dvc.lock shows a conflict. (4) MLflow UI shows runs but artifacts are missing or cannot be opened. (5) registering a model fails with a backend error. (6) a run logs to ./mlruns instead of the tracking server. Give a table symptom, likely cause, command to confirm, fix. Reproduce at least three of these locally and show the real error text.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** I go from the cheapest check to the dearest: read the exact error, confirm with one command (`dvc status -c`, `dvc status`, `mlflow.get_tracking_uri()`), then fix the cause, not the symptom.

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
#!/bin/bash
# Reproduce DVC debugging cases 1, 2, 3 in a temp repo. Usage: q32_dvc.sh WORKDIR
set -u
W=$1; rm -rf "$W"; mkdir -p "$W/repo" "$W/remote"; cd "$W/repo"
git init -q -b main; git config user.email a@b.c; git config user.name t
dvc init -q; git commit -qm init
printf 'a,b\n1,2\n3,4\n' > data.csv
dvc remote add -d loc "$W/remote" >/dev/null
dvc add data.csv >/dev/null
git add -A; git commit -qm "data"
echo "=== CASE 1: dvc pull when the remote never received the data (forgot dvc push)"
rm -rf data.csv .dvc/cache
dvc pull 2>&1 | tail -6
echo "--- confirm: what does the remote hold?"; find "$W/remote" -type f | wc -l
echo "--- fix: push from a machine that has the cache"
printf 'a,b\n1,2\n3,4\n' > data.csv; dvc add data.csv >/dev/null; dvc push 2>&1 | tail -1
rm -rf data.csv .dvc/cache; dvc pull 2>&1 | tail -1

echo; echo "=== CASE 2: dvc repro re-runs although nothing changed"
mkdir -p feats; echo x > feats/f1.txt
printf 'lr: 0.1\nnoise: 1\n' > params.yaml
printf 'import yaml\nlr = yaml.safe_load(open("params.yaml"))["lr"]\nopen("out.txt", "w").write(str(lr))\n' > prep.py
echo "--- cause A: whole params.yaml listed as a plain dependency"
dvc stage add -q -n prep -d prep.py -d params.yaml -o out.txt python prep.py
dvc repro 2>&1 | grep -E "Running|up to date"
sed -i 's/noise: 1/noise: 2/' params.yaml         # change a key the script never reads
dvc repro 2>&1 | grep -E "Running|up to date"
echo "--- fix: depend on the keys the stage reads (-p lr)"
dvc stage add -q -f -n prep -d prep.py -p lr -o out.txt python prep.py
dvc repro 2>&1 | grep -E "Running|up to date"
sed -i 's/noise: 2/noise: 3/' params.yaml
dvc repro 2>&1 | grep -E "Running|up to date"
echo "--- cause B: dvc.lock was not committed or was deleted"
cp dvc.lock /tmp/lock.bak; rm dvc.lock
dvc status 2>&1 | head -3
dvc repro 2>&1 | head -3
echo "--- cause C: --always-changed on the stage"
dvc stage add -q -f -n prep -d prep.py -p lr -o out.txt --always-changed python prep.py
dvc repro 2>&1 | grep -E "Running"; dvc repro 2>&1 | grep -E "Running"
dvc stage add -q -f -n prep -d prep.py -p lr -o out.txt python prep.py; dvc repro 2>&1 | grep -E "Running|up to date"; dvc repro 2>&1 | grep -E "Running|up to date"
git add -A; git commit -qm pipeline

echo; echo "=== CASE 3: conflict in dvc.lock"
git checkout -qb exp1; sed -i 's/lr: 0.1/lr: 0.2/' params.yaml; dvc repro >/dev/null 2>&1; git add -A; git commit -qm exp1
git checkout -q main; git checkout -qb exp2; sed -i 's/lr: 0.1/lr: 0.3/' params.yaml; dvc repro >/dev/null 2>&1; git add -A; git commit -qm exp2
git merge exp1 2>&1 | tail -3
echo "--- markers in dvc.lock:"; grep -nE '^(<<<<<<<|=======|>>>>>>>)' dvc.lock
echo "--- dvc status:"; dvc status 2>&1 | tail -4
echo "--- fix: abort, merge again, take either lock, re-run, commit"
git merge --abort
git merge exp1 -q -X theirs -m "merge exp1" 2>&1 | tail -1
dvc repro 2>&1 | grep -E "Running|up to date"; dvc status 2>&1 | head -2
```
```python
import os, shutil, sys, traceback, tempfile
import mlflow
from mlflow.tracking import MlflowClient
import warnings; warnings.filterwarnings("ignore")

def short(e): return f"{type(e).__name__}: {str(e).strip().splitlines()[0][:230]}"

print("=== CASE 6: the run goes somewhere you did not expect")
print("default tracking uri (MLFLOW_TRACKING_URI unset):", mlflow.get_tracking_uri().replace(os.getcwd(), "<cwd>"))
with mlflow.start_run(): mlflow.log_metric("m", 1)
print("files created in cwd:", sorted(os.listdir(".")))
mlflow.set_tracking_uri("file:./mlruns")
try:
    with mlflow.start_run(): mlflow.log_metric("m", 1)
except Exception as e: print("plain file store:", short(e))
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
with mlflow.start_run(): mlflow.log_metric("m", 1)
print("after opting in, ./mlruns exists:", os.path.isdir("mlruns"))
print("fix: set MLFLOW_TRACKING_URI (or set_tracking_uri) BEFORE the first run, and print mlflow.get_tracking_uri() in the log")

print("\n=== CASE 4: UI shows the run but the artifact is gone")
mlflow.set_tracking_uri("sqlite:///t.db")
art = os.path.abspath("art_root"); os.makedirs(art, exist_ok=True)
exp = mlflow.create_experiment("e4", artifact_location=art)
with mlflow.start_run(experiment_id=exp) as r:
    mlflow.log_metric("acc", 0.9); mlflow.log_text("hello", "notes.txt")
    rid = r.info.run_id
print("artifact uri :", mlflow.get_run(rid).info.artifact_uri)
print("list before  :", [f.path for f in MlflowClient().list_artifacts(rid)])
shutil.rmtree(art)                                    # bucket cleaned, disk moved, wrong mount ...
print("list after   :", [f.path for f in MlflowClient().list_artifacts(rid)])
print("metrics still:", mlflow.get_run(rid).data.metrics)
try: mlflow.artifacts.download_artifacts(run_id=rid, artifact_path="notes.txt", dst_path=tempfile.mkdtemp())
except Exception as e: print(short(e))

print("\n=== CASE 5: registering a model fails with a backend error")
from sklearn.dummy import DummyClassifier
m = DummyClassifier().fit([[0], [1]], [0, 1])
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
mlflow.set_tracking_uri("file:./fs_only")
try:
    with mlflow.start_run():
        mlflow.sklearn.log_model(m, name="model", registered_model_name="clf")
    print("file store registered OK (this version allows it)")
except Exception as e: print("file store:", short(e))
mlflow.set_tracking_uri("sqlite:////dev/null/x/mlflow.db")
try:
    with mlflow.start_run(): mlflow.sklearn.log_model(m, name="model", registered_model_name="clf")
except Exception as e: print("bad db path:", short(e))
mlflow.set_tracking_uri("http://127.0.0.1:9")
os.environ["MLFLOW_HTTP_REQUEST_MAX_RETRIES"] = "0"; os.environ["MLFLOW_HTTP_REQUEST_TIMEOUT"] = "3"
try: MlflowClient().create_registered_model("clf")
except Exception as e: print("server down:", short(e))
```

**Output (my run):** DVC script (cases 1 to 3), temp git repo with a local-folder remote. Versions that ran: Python 3.13, dvc 3.67.1, mlflow 3.17.2, wandb 0.31.0, scikit-learn 1.9.1, tracked in a sqlite backend. Check current docs for newer behaviour.
```text
=== CASE 1: dvc pull when the remote never received the data (forgot dvc push)
md5: c3c6bc2ae8ece4bd2510dca21225c041
Everything is up to date.
ERROR: failed to pull data from the cloud - Checkout failed for following targets:
data.csv
Is your cache up to date?
<https://error.dvc.org/missing-files>
--- confirm: what does the remote hold?
0
--- fix: push from a machine that has the cache
1 file pushed
1 file fetched and 1 file added

=== CASE 2: dvc repro re-runs although nothing changed
--- cause A: whole params.yaml listed as a plain dependency
Running stage 'prep':
Running stage 'prep':
--- fix: depend on the keys the stage reads (-p lr)
Running stage 'prep':
Data and pipelines are up to date.
--- cause B: dvc.lock was not committed or was deleted
prep:
	changed deps:
		modified:           prep.py
Stage 'prep' is cached - skipping run, checking out outputs
Generating lock file 'dvc.lock'
Updating lock file 'dvc.lock'
--- cause C: --always-changed on the stage
Running stage 'prep':
Running stage 'prep':
Data and pipelines are up to date.
Data and pipelines are up to date.

=== CASE 3: conflict in dvc.lock
Auto-merging params.yaml
CONFLICT (content): Merge conflict in params.yaml
Automatic merge failed; fix conflicts and then commit the result.
--- markers in dvc.lock:
12:<<<<<<< HEAD
18:=======
24:>>>>>>> exp1
--- dvc status:
  12 <<<<<<< HEAD                                                               

Could not find expected ':', in line 13, column 11
  13 │   │   lr: 0.3                                                            
--- fix: abort, merge again, take either lock, re-run, commit
Auto-merging params.yaml
Data and pipelines are up to date.
```
MLflow script (cases 6, 4, 5), run from an empty folder:
```text
=== CASE 6: the run goes somewhere you did not expect
default tracking uri (MLFLOW_TRACKING_URI unset): sqlite:///<cwd>/mlflow.db
files created in cwd: ['mlflow.db']
plain file store: MlflowException: The filesystem tracking backend (e.g., './mlruns') is in maintenance mode and will not receive further updates. Please migrate to a database backend (e.g., 'sqlite:///mlflow.db') to access the latest MLflow features. The `mlflow m
after opting in, ./mlruns exists: True
fix: set MLFLOW_TRACKING_URI (or set_tracking_uri) BEFORE the first run, and print mlflow.get_tracking_uri() in the log

=== CASE 4: UI shows the run but the artifact is gone
artifact uri : /tmp/claude-0/b4p04/q32m/art_root/cb2d2e51606449879024b1ea71475d11/artifacts
list before  : ['notes.txt']
list after   : []
metrics still: {'acc': 0.9}
MlflowException: Failed to download artifacts from path 'notes.txt', please ensure that the path is correct.

=== CASE 5: registering a model fails with a backend error
file store registered OK (this version allows it)
bad db path: NotADirectoryError: [Errno 20] Not a directory: '/dev/null/x'
server down: MlflowException: API request to http://127.0.0.1:9/api/2.0/mlflow/registered-models/create failed with exception HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /api/2.0/mlflow/registered-models/create (Caused by NewCo
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

### Q33 ⭐ 🔴 lakeFS and branch-based data versioning at concept level: repositories, branches, commits, merges over an object store, zero-copy branching, hooks that run quality checks before merge, and how it differs from DVC (a Git-side pointer file per dataset). Some sources say lakeFS has taken over DVC stewardship (reported in late 2025 snippets, unverified; check current news). Draw the flow for 'ingest to a branch, validate, merge to main' and write a toy in-memory branch and merge simulation in Python and run it. lakeFS itself is not installed here and nothing is executed against it.
**Asked at:** Data-versioning comparison write-ups (lakeFS blog 'scalable data version control', kanerika data versioning tools, pdpspectra 'DVC vs lakeFS', jisaku glossary; search snippets only, not opened); vendor-written or low-quality blogs, treat specifics with caution; data and ML platform roles
**Say this first (1 line):** lakeFS puts Git-style branches, commits and merges on top of an object store, so a whole data lake is versioned without copying files; DVC instead keeps one small pointer file in Git per dataset or pipeline output.

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
                                                      \-> fail: branch kept for debugging, main untouched
```

**Code:**
```python
"""Toy lakeFS-style branching: objects are immutable blobs; a commit is a path->blob-id map.
Branching copies only the map (zero-copy); merge is a 3-way merge on paths."""
import hashlib

class Repo:
    def __init__(self):
        self.blobs = {}            # blob_id -> bytes  (the "object store")
        self.commits = {}          # commit_id -> (parent, {path: blob_id}, msg)
        self.branches = {}         # name -> commit_id
        self.hooks = []            # pre-merge hooks: fn(files: dict[path, bytes]) -> None or raises
        c = self._commit(None, {}, "init"); self.branches["main"] = c
        self.staged = {}           # branch -> {path: blob_id or None}

    def _commit(self, parent, tree, msg):
        cid = hashlib.sha1(f"{parent}{sorted(tree.items())}{msg}".encode()).hexdigest()[:8]
        self.commits[cid] = (parent, dict(tree), msg); return cid
    def branch(self, name, source="main"):
        self.branches[name] = self.branches[source]            # copies a pointer, no data
    def put(self, branch, path, data: bytes):
        bid = hashlib.sha1(data).hexdigest()[:8]; self.blobs.setdefault(bid, data)
        self.staged.setdefault(branch, {})[path] = bid
    def delete(self, branch, path): self.staged.setdefault(branch, {})[path] = None
    def tree(self, cid): return self.commits[cid][1]
    def commit(self, branch, msg):
        tree = dict(self.tree(self.branches[branch]))
        for p, b in self.staged.pop(branch, {}).items():
            tree.pop(p, None) if b is None else tree.__setitem__(p, b)
        self.branches[branch] = self._commit(self.branches[branch], tree, msg)
    def files(self, branch): return {p: self.blobs[b] for p, b in self.tree(self.branches[branch]).items()}
    def base(self, a, b):
        anc = set(); c = a
        while c: anc.add(c); c = self.commits[c][0]
        c = b
        while c not in anc: c = self.commits[c][0]
        return c
    def merge(self, src, dst):
        for h in self.hooks: h(self.files(src))               # pre-merge quality gate
        ca, cb = self.branches[src], self.branches[dst]; base = self.tree(self.base(ca, cb))
        s, d = self.tree(ca), self.tree(cb); out = dict(d)
        for p in set(s) | set(d) | set(base):
            if s.get(p) == d.get(p): continue
            if s.get(p) == base.get(p): continue                   # only dst changed
            if d.get(p) == base.get(p):                            # only src changed
                out.pop(p, None) if p not in s else out.__setitem__(p, s[p]); continue
            raise RuntimeError(f"conflict on {p}")
        self.branches[dst] = self._commit(cb, out, f"merge {src}")

def no_null_ids(files):
    for p, data in files.items():
        if p.endswith(".csv") and any(l.startswith(b",") for l in data.splitlines()): raise ValueError(f"quality gate failed: empty id in {p}")

r = Repo(); r.hooks.append(no_null_ids)
r.put("main", "users/part-0.csv", b"1,a\n2,b\n"); r.commit("main", "load v1")
print("main files:", sorted(r.files("main")))

r.branch("ingest-2026-10-26")
print("blobs before branch write:", len(r.blobs))
r.put("ingest-2026-10-26", "users/part-1.csv", b"3,c\n,d\n")      # bad row: empty id
r.commit("ingest-2026-10-26", "new batch")
print("blobs after one new file :", len(r.blobs), "(old file not copied)")
try: r.merge("ingest-2026-10-26", "main")
except ValueError as e: print("merge blocked:", e)
print("main still:", sorted(r.files("main")))

r.put("ingest-2026-10-26", "users/part-1.csv", b"3,c\n4,d\n"); r.commit("ingest-2026-10-26", "fix batch")
r.merge("ingest-2026-10-26", "main")
print("merged main:", sorted(r.files("main")))

# conflict: two branches edit the same path
r.branch("a"); r.branch("b")
r.put("a", "users/part-0.csv", b"1,A\n"); r.commit("a", "edit a")
r.put("b", "users/part-0.csv", b"1,B\n"); r.commit("b", "edit b")
r.merge("a", "main")
try: r.merge("b", "main")
except RuntimeError as e: print("second merge:", e)
```

**Output (my run):** pure Python, `python -I`. This is a simulation, not lakeFS. lakeFS itself: not executed.
```text
main files: ['users/part-0.csv']
blobs before branch write: 1
blobs after one new file : 2 (old file not copied)
merge blocked: quality gate failed: empty id in users/part-1.csv
main still: ['users/part-0.csv']
merged main: ['users/part-0.csv', 'users/part-1.csv']
second merge: conflict on users/part-0.csv
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

### Q34 ⭐ 🔴 Cost, retention and safety of the data and artifact store behind DVC and MLflow: bucket versioning, lifecycle rules, what dvc gc -c does to a shared remote (it can delete data another branch still needs), who is allowed to delete, backups, and tracking-server retention for old runs. Give a policy table for a 20-person team and a script that lists which cache hashes are referenced by a list of Git revisions and which are unreferenced. Run it against a local DVC repo; cloud lifecycle features are not executed (check current docs, no prices).
**Asked at:** DVC official docs and tutorials (dvc.org 'Metrics, Plots, and Parameters' get-started page, OneUptime 'How to Configure DVC for Data Versioning' 2026, UCL data version control lecture, DAGsHub pipelines tutorial; search snippets only, not opened); docs and tutorials, not interview reports; MLOps and data science roles
**Say this first (1 line):** `dvc gc` deletes whatever your chosen Git revisions do not reference, so on a shared remote I never run it with the default scope; I list what each revision needs first, and I run it dry.

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
"""List which DVC cache objects are referenced by given Git revisions, and which are not.
usage: python -I q34_gc_report.py REPO REV [REV ...]"""
import json, subprocess, sys, pathlib, yaml

repo = pathlib.Path(sys.argv[1]); revs = sys.argv[2:]
cache = repo / ".dvc" / "cache" / "files" / "md5"

def git(*a): return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, check=True).stdout

def obj_path(h): return cache / h[:2] / h[2:]

def expand(h):                      # a '.dir' hash points to a manifest listing member hashes
    if not h.endswith(".dir"): return {h}
    out = {h}; p = obj_path(h)
    if p.exists():
        out |= {e["md5"] for e in json.loads(p.read_text())}
    return out

def hashes_at(rev):
    found = {}
    for f in git("ls-tree", "-r", "--name-only", rev).split():
        if f.endswith(".dvc") or f.endswith("dvc.lock"):
            doc = yaml.safe_load(git("show", f"{rev}:{f}")) or {}
            outs = doc.get("outs", []) if f.endswith(".dvc") else \
                   [o for s in doc.get("stages", {}).values() for o in s.get("outs", [])]
            for o in outs:
                for h in expand(o["md5"]): found[h] = f"{f}:{o['path']}"
    return found

ref = {}
for r in revs:
    for h, why in hashes_at(r).items(): ref.setdefault(h, []).append(f"{r}:{why}")
on_disk = {p.parent.name + p.name for p in cache.rglob("*") if p.is_file()}
print(f"revisions scanned : {revs}")
print(f"objects in cache  : {len(on_disk)}")
print(f"referenced        : {len(set(ref) & on_disk)}")
for h in sorted(set(ref) & on_disk): print(f"  KEEP   {h[:10]}  <- {ref[h][0]}")
unref = on_disk - set(ref)
print(f"unreferenced      : {len(unref)}  (a 'dvc gc' candidate, but ONLY for these revisions)")
for h in sorted(unref): print(f"  UNREF  {h[:10]}  {obj_path(h).stat().st_size} bytes")
missing = set(ref) - on_disk
print(f"referenced but not in cache: {len(missing)}")
```
```bash
set -u; W=$1; rm -rf $W; mkdir -p $W/repo $W/remote; cd $W/repo
git init -q -b main; git config user.email a@b.c; git config user.name t; dvc init -q; git commit -qm init
dvc remote add -d loc $W/remote >/dev/null
echo v1 > data.csv; dvc add data.csv >/dev/null; git add -A; git commit -qm v1; git tag v1
git checkout -qb feature; echo v2-feature > data.csv; dvc add data.csv >/dev/null; git add -A; git commit -qm feature; git tag feat
git checkout -q main; echo v3 > data.csv; dvc add data.csv >/dev/null; git add -A; git commit -qm v3
dvc push 2>&1 | tail -1; git checkout -q feature; dvc push 2>&1 | tail -1; git checkout -q main
echo "--- report: main only"; python -I $2 . main
echo; echo "--- report: main + feature branch"; python -I $2 . main feature
echo; echo "--- dvc gc dry run, workspace only (keeps just what main HEAD needs), cloud remote"
dvc gc -w -c -f --dry 2>&1 | tail -6
echo "--- dvc gc dry run, all branches and tags"
dvc gc -A -c -f --dry 2>&1 | tail -4
```

**Output (my run):** local repo, local-folder remote; `dvc gc` runs were `--dry`. Versions that ran: Python 3.13, dvc 3.67.1, mlflow 3.17.2, wandb 0.31.0, scikit-learn 1.9.1, tracked in a sqlite backend. Check current docs for newer behaviour.
```text
1 file pushed
1 file pushed
--- report: main only
revisions scanned : ['main']
objects in cache  : 3
referenced        : 1
  KEEP   cc255a285b  <- main:data.csv.dvc:data.csv
unreferenced      : 2  (a 'dvc gc' candidate, but ONLY for these revisions)
  UNREF  4f98f59e87  3 bytes
  UNREF  955b491ba0  11 bytes
referenced but not in cache: 0

--- report: main + feature branch
revisions scanned : ['main', 'feature']
objects in cache  : 3
referenced        : 2
  KEEP   955b491ba0  <- feature:data.csv.dvc:data.csv
  KEEP   cc255a285b  <- main:data.csv.dvc:data.csv
unreferenced      : 1  (a 'dvc gc' candidate, but ONLY for these revisions)
  UNREF  4f98f59e87  3 bytes
referenced but not in cache: 0

--- dvc gc dry run, workspace only (keeps just what main HEAD needs), cloud remote
Removing /tmp/claude-0/b4p04/q34/repo/.dvc/cache/files/md5/95/5b491ba0e40766a98a6593293fc922
Removed 2 objects from repo cache.
No unused 'legacy' cache to remove.
Removing /tmp/claude-0/b4p04/q34/remote/files/md5/95/5b491ba0e40766a98a6593293fc922
Removed 1 objects from remote.
No unused cache to remove from remote.
--- dvc gc dry run, all branches and tags
No unused 'repo' cache to remove.
No unused 'legacy' cache to remove.
No unused cache to remove from remote.
No unused cache to remove from remote.
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

### Q35 ⭐ 🔴 Versioning in the GenAI era: datasets, prompts and evaluation sets for LLM fine-tuning and RAG. Explain what you version (the fine-tuning JSONL, the prompt template, the eval set, the embedding model and index build), Hugging Face dataset revisions and commit hashes, DVC for the JSONL, MLflow or W&B for prompts and eval results (prompt registry and tracing features exist; hedge by version), and how to tie an answer-quality regression to a prompt or data change. Show a small script that hashes a prompt file and eval set and logs both to an MLflow run. Hosted LLM calls are not executed. Book 2 owns LLM internals.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** In GenAI work the model is only one input, so I version the data, the prompt, the eval set and the retrieval build as separate things, and I put a hash of each on every eval run so a quality drop points to a changed input.

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
import hashlib, json, pathlib, sys, tempfile, mlflow
from mlflow.tracking import MlflowClient

def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:12]

work = pathlib.Path(tempfile.mkdtemp())
(work / "prompt.txt").write_text("Answer using only the context.\nContext: {context}\nQuestion: {question}\n")
(work / "eval.jsonl").write_text("\n".join(json.dumps(x) for x in [
    {"q": "Refund window?", "gold": "30 days"}, {"q": "Support hours?", "gold": "9 to 6"}]) + "\n")

def fake_answer(prompt_text, question):          # stand-in for an LLM call: NOT a model, not executed
    return {"Refund window?": "30 days", "Support hours?": "9 to 6" if "only the context" in prompt_text else "24x7"}[question]

def run(tag):
    prompt = (work / "prompt.txt").read_text()
    rows = [json.loads(l) for l in (work / "eval.jsonl").read_text().splitlines()]
    acc = sum(fake_answer(prompt, r["q"]) == r["gold"] for r in rows) / len(rows)
    with mlflow.start_run(run_name=tag):
        mlflow.set_tags({"prompt_sha": sha(work / "prompt.txt"), "evalset_sha": sha(work / "eval.jsonl"),
                         "embedding_model": "example-embedder@rev-abc (placeholder)", "index_build": "idx-2026-10-26 (placeholder)"})
        mlflow.log_artifact(str(work / "prompt.txt")); mlflow.log_artifact(str(work / "eval.jsonl"))
        mlflow.log_metric("exact_match", acc)

mlflow.set_tracking_uri("sqlite:///genai.db"); mlflow.set_experiment("rag-eval")
run("baseline")
(work / "prompt.txt").write_text("Be brief.\nContext: {context}\nQuestion: {question}\n")   # someone edits the prompt
run("after-prompt-edit")
df = mlflow.search_runs(experiment_names=["rag-eval"], order_by=["start_time ASC"])
print(df[["tags.mlflow.runName", "metrics.exact_match", "tags.prompt_sha", "tags.evalset_sha"]].to_string(index=False))
a, b = df.iloc[0], df.iloc[1]
print("\nprompt changed :", a["tags.prompt_sha"] != b["tags.prompt_sha"])
print("eval set same  :", a["tags.evalset_sha"] == b["tags.evalset_sha"])
print("metric delta   :", b["metrics.exact_match"] - a["metrics.exact_match"])
```

**Output (my run):** `python -I`, MLflow on local sqlite. The "model" is a stub, not an LLM. Hosted LLM calls: not executed.
```text
tags.mlflow.runName  metrics.exact_match tags.prompt_sha tags.evalset_sha
           baseline                  1.0    40d40b632afa     27cd69ab1e36
  after-prompt-edit                  0.5    f68baffa851f     27cd69ab1e36

prompt changed : True
eval set same  : True
metric delta   : -0.5
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

### Q36 ⭐ 🔴 Running MLflow for a team in production: a tracking server behind a reverse proxy, Postgres backend, S3 or compatible artifact store, authentication (basic auth plugin or SSO through a proxy), backups of the database, upgrades with mlflow db upgrade, and the alternatives of managed MLflow (Databricks, Azure ML, SageMaker). Give an architecture table and a server start command; run a local server with sqlite on localhost and log a run to it. Postgres, S3, SSO and anything remote are not executed. Part 2 owns the Docker Compose stack for it.
**Asked at:** MLflow official docs and tutorials (mlflow.org tracking, autolog and model registry pages, MLflow 3.1.3 autolog docs, MLflow 2.11 model signature docs, DataTalksClub MLOps Zoomcamp experiment-tracking module, Azure ML MLflow training pages; search snippets only, not opened); docs and course material, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** For a team I run a tracking server on a database (Postgres) with an object store for artifacts behind an authenticating reverse proxy, back up both, and upgrade the schema deliberately; or I buy it managed.

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
set -u; W=$1; rm -rf $W; mkdir -p $W; cd $W
export MLFLOW_DISABLE_TELEMETRY=true MLFLOW_DISABLE_AGENT_HINT=1
mlflow server --backend-store-uri sqlite:///$W/srv.db --artifacts-destination $W/art --host 127.0.0.1 --port 5081 > server.log 2>&1 &
PID=$!
for i in $(seq 1 40); do curl -s http://127.0.0.1:5081/health >/dev/null && break; sleep 1; done
echo "health: $(curl -s http://127.0.0.1:5081/health)"
python -I $2 http://127.0.0.1:5081 $W 2>&1 | grep -v INFO
echo "--- files on the server side"; find $W/art -type f | sed "s#$W/##" | sed -E 's#[0-9a-f]{32}#<id>#g'
kill $PID; wait $PID 2>/dev/null
echo "--- mlflow db upgrade on the sqlite file (safe to re-run)"
mlflow db upgrade sqlite:///$W/srv.db 2>&1 | grep -v "^$" | tail -3
```
```python
import mlflow, sys
from mlflow.tracking import MlflowClient
mlflow.set_tracking_uri(sys.argv[1]); mlflow.set_experiment("team-demo")
with mlflow.start_run(run_name="via-server") as r:
    mlflow.log_param("owner", "dhyan"); mlflow.log_metric("acc", 0.91); mlflow.log_text("model card draft", "card.txt")
    print("run", r.info.run_id[:8], "artifact_uri:", r.info.artifact_uri.replace(sys.argv[2], "<ROOT>"))
c = MlflowClient()
print("runs via server API:", [(x.info.run_name, x.data.metrics) for x in c.search_runs([c.get_experiment_by_name("team-demo").experiment_id])])
print("artifacts:", [f.path for f in c.list_artifacts(r.info.run_id)])
```
Production-shaped start command (**not executed**; Postgres and S3 not available here, hostnames are placeholders):
```text
mlflow server --backend-store-uri postgresql://USER:PASS@db-host:5432/mlflow --artifacts-destination s3://my-bucket/mlflow --host 0.0.0.0 --port 5000
```

**Output (my run):** local server on 127.0.0.1 with SQLite and a local artifact folder, then a client run. Versions that ran: Python 3.13, dvc 3.67.1, mlflow 3.17.2, wandb 0.31.0, scikit-learn 1.9.1, tracked in a sqlite backend. Check current docs for newer behaviour.
```text
health: OK
run c70ee442 artifact_uri: mlflow-artifacts:/1/c70ee44219804fe0af3eeb180ab262ff/artifacts
🏃 View run via-server at: http://127.0.0.1:5081/#/experiments/1/runs/c70ee44219804fe0af3eeb180ab262ff
🧪 View experiment at: http://127.0.0.1:5081/#/experiments/1
runs via server API: [('via-server', {'acc': 0.91})]
artifacts: ['card.txt']
--- files on the server side
art/1/<id>/artifacts/card.txt
--- mlflow db upgrade on the sqlite file (safe to re-run)
2026/10/26 14:09:19 INFO mlflow.store.db.utils: Updating database tables
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

### Q37 ⭐ 🔴 Migrating: from ./mlruns to a database backend (mlflow migrate-filestore, check current docs), from registry stages to aliases (transition_model_version_stage to set_registered_model_alias, models:/name/Production to models:/name@alias), and from Git LFS to DVC. For each, say what breaks (hard-coded URIs in serving code, run IDs, access control), the order of steps, and how to verify with a before and after comparison of run counts and metrics. Run the file store to sqlite migration locally if the command works in the installed version and show real output or the real error.
**Asked at:** MLflow Model Registry sources (mlflow.org registry docs, MLflow GitHub issue on stage deprecation, ZenML MLflow registry page, Databricks community and knowledge-base posts; search snippets only, not opened); docs and community posts, not interview reports; MLOps roles using MLflow or Databricks
**Say this first (1 line):** Before any migration I count runs and compare metrics, then move, then count and compare again, and I keep the old data until the after-check passes.

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
set -u; W=$1; rm -rf $W; mkdir -p $W/remote; cd $W; export PATH=/tmp/claude-0/ven/v/bin:$PATH
git init -q -b main; git config user.email a@b.c; git config user.name t
git lfs install --local >/dev/null 2>&1
git lfs track "*.csv" >/dev/null; printf 'a,b\n1,2\n' > big.csv
git add -A; git commit -qm "with lfs"
echo "--- before: what git stores in the commit for big.csv"; git show HEAD:big.csv; git lfs ls-files
echo "--- step 1: make sure the real file is in the workspace (git lfs pull); step 2: stop tracking it in LFS"
git lfs untrack "*.csv" >/dev/null; git rm -q --cached big.csv
echo "--- step 3: hand it to DVC"
dvc init -q; dvc remote add -d loc $W/remote >/dev/null; dvc add big.csv 2>&1 | tail -2
git add -A; git commit -qm "move big.csv to DVC"
echo "--- after: what git stores now"; git show HEAD:big.csv.dvc | head -4; git ls-files
dvc push 2>&1 | tail -1
echo "--- old history still holds the LFS pointer:"; git show HEAD~1:big.csv | head -3
```
```python
import mlflow, warnings, sys
from mlflow.tracking import MlflowClient
from sklearn.dummy import DummyClassifier
mlflow.set_tracking_uri("sqlite:///reg.db"); c = MlflowClient()
m = DummyClassifier(strategy="constant", constant=1).fit([[0], [1]], [0, 1])
with mlflow.start_run(): mlflow.sklearn.log_model(m, name="model", registered_model_name="clf")
print("--- old way: stages")
try:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        c.transition_model_version_stage("clf", 1, "Production")
    print("stage call returned; warning:", str(w[0].message)[:150] if w else None)
except Exception as e: print("stage call failed:", type(e).__name__, str(e)[:150])
try:
    print("models:/clf/Production predicts", mlflow.pyfunc.load_model("models:/clf/Production").predict([[0]]))
except Exception as e: print("stage URI failed:", type(e).__name__, str(e).splitlines()[0][:200])
print("--- new way: alias")
c.set_registered_model_alias("clf", "champion", 1)
print("models:/clf@champion predicts", mlflow.pyfunc.load_model("models:/clf@champion").predict([[0]]))
print("alias lookup ->", c.get_model_version_by_alias("clf", "champion").version)
```
Helpers `q37_make_fs.py` and `q37_count.py` (create three runs; count and print) are in the code folder.

**Output (my run):** with `MLFLOW_ALLOW_FILE_STORE=true` for the old store. Versions that ran: Python 3.13, dvc 3.67.1, mlflow 3.17.2, wandb 0.31.0, scikit-learn 1.9.1, tracked in a sqlite backend. Check current docs for newer behaviour.
```text
--- BEFORE (file store)
file:./mlruns runs: 3 acc: [0.8, 0.85, 0.9] depth: ['2', '3', '4']
artifact uri of first run: file://<CWD>/mlruns/757663189457672088/213fa3a0f832469ba12b35e79c66c60c/artifacts
--- mlflow migrate-filestore --source ./mlruns --target sqlite:///migrated.db
  runs                               3          3
  params                             3          3
  tags                              21         21
  metrics                            3          3
  latest_metrics                     3          3
--- AFTER (sqlite)
sqlite:///migrated.db runs: 3 acc: [0.8, 0.85, 0.9] depth: ['2', '3', '4']
artifact uri of first run: file://<CWD>/mlruns/757663189457672088/213fa3a0f832469ba12b35e79c66c60c/artifacts
--- stages to aliases
stage call returned; warning: ``mlflow.tracking.client.MlflowClient.transition_model_version_stage`` is deprecated since 2.9.0. Model registry stages will be removed in a future ma
models:/clf/Production predicts [1]
--- new way: alias
models:/clf@champion predicts [1]
alias lookup -> 1
```
LFS to DVC (local git repo with git-lfs, no LFS server, DVC local remote):
```text
--- before: what git stores in the commit for big.csv
version https://git-lfs.github.com/spec/v1
oid sha256:492d5ea496056f1a6a6592241032fab764c321596317930b4fa0e1e8bc3b7470
size 8
492d5ea496 * big.csv
--- step 1: make sure the real file is in the workspace (git lfs pull); step 2: stop tracking it in LFS
--- step 3: hand it to DVC

	dvc config core.autostage true
--- after: what git stores now
outs:
- md5: e5ebd4c02cefbe7955977c67ada242b7
  size: 8
  hash: md5
.dvc/.gitignore
.dvc/config
.dvcignore
.gitattributes
.gitignore
big.csv.dvc
1 file pushed
--- old history still holds the LFS pointer:
version https://git-lfs.github.com/spec/v1
oid sha256:492d5ea496056f1a6a6592241032fab764c321596317930b4fa0e1e8bc3b7470
size 8
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

### Q38 ⭐ 🔴 Design question: a tracking and versioning platform for 50 data scientists across three teams. Cover naming conventions for experiments, mandatory tags (git SHA, data hash, owner, project), one shared MLflow server or per-team servers, DVC remotes per project, a model registry with aliases, retention and cost, access control, a golden dataset for regression, onboarding docs and templates, and how a model moves from experiment to registered version to deployment (Part 7 owns CI/CD detail). Give a component table with owners and a script that checks that a run has all mandatory tags and flags the ones that do not. Pure design; the script runs locally.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** One shared tracking server with a naming rule and a few mandatory tags, enforced by code, plus per-project DVC remotes and a registry with aliases, so any model can be traced to code, data and owner.

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
"""Flag runs missing mandatory tags / badly formed tags. usage: python -I q38_tag_check.py TRACKING_URI
In production this would run as a nightly job and post to chat; here it just prints."""
import re, sys, mlflow
from mlflow.tracking import MlflowClient

REQUIRED = {                      # tag -> regex it must match
    "git_sha":  r"[0-9a-f]{7,40}",
    "data_hash": r"[0-9a-f]{8,64}",
    "owner":    r"[a-z][a-z0-9._-]+",
    "project":  r"[a-z][a-z0-9-]+",
}
NAME_RULE = r"[a-z0-9-]+/[a-z0-9-]+/[a-z0-9-]+"       # team/project/purpose

def check(run, exp_name):
    problems = []
    if not re.fullmatch(NAME_RULE, exp_name): problems.append(f"experiment name '{exp_name}' is not team/project/purpose")
    for k, pat in REQUIRED.items():
        v = run.data.tags.get(k)
        if v is None: problems.append(f"missing {k}")
        elif not re.fullmatch(pat, v): problems.append(f"bad {k}='{v}'")
    return problems

mlflow.set_tracking_uri(sys.argv[1]); c = MlflowClient(); bad = total = 0
for e in c.search_experiments():
    for r in c.search_runs([e.experiment_id]):
        total += 1; p = check(r, e.name)
        if p: bad += 1; print(f"FAIL run={r.info.run_id[:8]} owner={r.data.tags.get('owner','?')}: " + "; ".join(p))
        else: print(f"ok   run={r.info.run_id[:8]}")
print(f"{bad} of {total} runs fail the policy"); sys.exit(1 if bad else 0)
```

**Output (my run):** local sqlite store with the three seeded runs (seed script `q38_seed.py` in the code folder). Versions that ran: Python 3.13, dvc 3.67.1, mlflow 3.17.2, wandb 0.31.0, scikit-learn 1.9.1, tracked in a sqlite backend. Check current docs for newer behaviour.
```text
FAIL run=64f41fdb owner=asha: experiment name 'Quick Test' is not team/project/purpose; bad git_sha='latest'
FAIL run=42c3b17a owner=asha: missing data_hash
ok   run=ae6d1149
2 of 3 runs fail the policy
exit code of the check: 1
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

### Q39 ⭐ 🟡 MLOps versioning skills in India hiring: what do job postings and screens ask about DVC, MLflow and W&B, and how do you build proof without a company budget? Summarise the skills lists seen in Bengaluru-style postings (not interview reports), then give a lab plan: a repo with a DVC pipeline and local remote, an MLflow sqlite tracker with a registry alias, an offline W&B run, a model card, and a README that explains lineage. Include a skills-to-lab table and what free tiers allow (check current terms). Run the core of the lab locally.
**Asked at:** Bengaluru and India MLOps job postings that list DVC, MLflow and experiment tracking (weekday.works, builtinbengaluru, GrabJobs listings seen while researching Parts 2 and 3; snippets only) plus editorial MLOps guides; postings show required skills, not interview questions; IT-services firms, GCCs and AI product companies in India
**Say this first (1 line):** I show the tools working together in one small public repo: a DVC pipeline with a local remote, an MLflow tracker with a registry alias, an offline W&B run, a model card and a README that explains the lineage.

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
set -u; W=$1; SRC=$(cd "$(dirname "$0")" && pwd); rm -rf $W; mkdir -p $W/repo $W/remote; cd $W/repo
export PATH=/tmp/claude-0/ven/v/bin:$PATH MLFLOW_DISABLE_TELEMETRY=true MLFLOW_DISABLE_AGENT_HINT=1 WANDB_SILENT=true
git init -q -b main; git config user.email a@b.c; git config user.name t
cp $SRC/params.yaml $SRC/prepare.py $SRC/train.py .
dvc init -q; dvc remote add -d loc $W/remote >/dev/null; printf 'mlflow.db\nmlruns/\nwb/\n__pycache__/\n' > .gitignore
dvc stage add -q -n prepare -d prepare.py -o data.csv python prepare.py
dvc stage add -q -n train -d train.py -d data.csv -p train -o model.joblib -O MODEL_CARD.md -M metrics.json python train.py
git add -A; git commit -qm "pipeline"
echo "--- dvc repro (1)"; dvc repro 2>&1 | grep -E "Running|Updating|ERROR|Error" 
git add -A; git commit -qm "first run" ; dvc push 2>&1 | tail -1
echo "--- change a param, repro (2), diff"
sed -i 's/C: 1.0/C: 0.01/' params.yaml; dvc repro 2>&1 | grep -E "Running|ERROR"
dvc params diff 2>&1; dvc metrics diff 2>&1
echo "--- dvc dag"; dvc dag 2>&1 | head -12
echo "--- registry"; python -I -c "
import mlflow; mlflow.set_tracking_uri('sqlite:///mlflow.db'); c = mlflow.tracking.MlflowClient()
for v in c.search_model_versions(\"name='demo-clf'\"): print('demo-clf v'+str(v.version), 'aliases:', v.aliases)
print('alias candidate ->', c.get_model_version_by_alias('demo-clf','candidate').version)" 2>&1 | grep -v INFO
echo "--- wandb offline run dirs"; ls wb/wandb | sed -E 's/offline-run-[0-9_]+-/offline-run-<ts>-/'
echo "--- model card"; cat MODEL_CARD.md
```
```python
import json, os, subprocess, yaml, hashlib, pandas as pd, mlflow, joblib, wandb
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from mlflow.models import infer_signature
p = yaml.safe_load(open("params.yaml"))["train"]
df = pd.read_csv("data.csv"); X, y = df.drop(columns="y"), df["y"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=0)
m = LogisticRegression(C=p["C"], max_iter=p["max_iter"], random_state=p["seed"]).fit(Xtr, ytr)
acc = float(m.score(Xte, yte)); joblib.dump(m, "model.joblib")
json.dump({"accuracy": acc}, open("metrics.json", "w"))
git = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
dhash = hashlib.md5(open("data.csv", "rb").read()).hexdigest()
mlflow.set_tracking_uri("sqlite:///mlflow.db"); mlflow.set_experiment("lab/demo/clf")
with mlflow.start_run() as r:
    mlflow.set_tags({"git_sha": git, "data_hash": dhash, "owner": "me", "project": "demo"})
    mlflow.log_params(p); mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(m, name="model", signature=infer_signature(Xte, m.predict(Xte)), registered_model_name="demo-clf")
v = mlflow.tracking.MlflowClient().search_model_versions("name='demo-clf'")
latest = max(int(x.version) for x in v)
mlflow.tracking.MlflowClient().set_registered_model_alias("demo-clf", "candidate", latest)
w = wandb.init(project="lab", mode="offline", dir="wb", config=p); w.log({"accuracy": acc}); w.finish()
open("MODEL_CARD.md", "w").write(f"""# demo-clf model card (generated)
- Intended use: demo only. Not for real decisions.
- Training data: data.csv, md5 {dhash} (synthetic, make_classification)
- Code: git {git}; params: {p}
- Metric: accuracy {acc:.4f} on a 25 percent hold-out (single split, no confidence interval)
- Registry: demo-clf version {latest}, alias 'candidate'
- Limits: synthetic data; no fairness or drift analysis done.
""")
```
Also in `code/q39_lab/`: `params.yaml`, `prepare.py`.

**Output (my run):** whole lab in a temp dir. Versions that ran: Python 3.13, dvc 3.67.1, mlflow 3.17.2, wandb 0.31.0, scikit-learn 1.9.1, tracked in a sqlite backend. Check current docs for newer behaviour.
```text
--- dvc repro (1)
Running stage 'prepare':
Updating lock file 'dvc.lock'
Running stage 'train':
Updating lock file 'dvc.lock'
2 files pushed
--- change a param, repro (2), diff
Running stage 'train':
Path         Param    HEAD    workspace
params.yaml  train.C  1.0     0.01
Path          Metric    HEAD    workspace    Change
metrics.json  accuracy  0.72    0.7          -0.02
--- dvc dag
+---------+  
| prepare |  
+---------+  
      *      
      *      
      *      
 +-------+   
 | train |   
 +-------+   
--- registry
demo-clf v2 aliases: []
demo-clf v1 aliases: []
alias candidate -> 2
--- wandb offline run dirs
debug-internal.log
debug.log
latest-run
offline-run-<ts>-9jhe8i07
offline-run-<ts>-wcn6c8hw
--- model card
# demo-clf model card (generated)
- Intended use: demo only. Not for real decisions.
- Training data: data.csv, md5 5ac5380ea575357fd9b0184905ce8d43 (synthetic, make_classification)
- Code: git 802a95b; params: {'C': 0.01, 'max_iter': 200, 'seed': 7}
- Metric: accuracy 0.7000 on a 25 percent hold-out (single split, no confidence interval)
- Registry: demo-clf version 2, alias 'candidate'
- Limits: synthetic data; no fairness or drift analysis done.
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

### Q40 ⭐ 🔴 Data lineage beyond one repo: OpenLineage and Marquez at concept level (jobs, runs, datasets, facets emitted by Airflow, Spark and dbt), how that differs from ML-run lineage in MLflow or W&B, and when a regulated team (banking, insurance, health) needs both for audit questions like 'which models used this customer table before it was corrected'. Give a small JSON event in the OpenLineage style (field names hedged, check the spec) and a script that walks a lineage graph from a dataset to every downstream model. No lineage server is available; nothing is executed against one.
**Asked at:** Data-versioning comparison write-ups (lakeFS blog 'scalable data version control', kanerika data versioning tools, pdpspectra 'DVC vs lakeFS', jisaku glossary; search snippets only, not opened); vendor-written or low-quality blogs, treat specifics with caution; data and ML platform roles
**Say this first (1 line):** OpenLineage records which job read which datasets and wrote which datasets across the whole data stack, while MLflow or W&B records which run produced which model; a regulated team needs both to answer "which models used this table before it was corrected".

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
"""OpenLineage-style events (field names follow the public spec as I know it; check the spec for your version)
and a walk from a dataset to every downstream model. Pure Python, no lineage server."""
import json
from collections import defaultdict, deque

def event(job, run_id, inputs, outputs, ts):
    return {"eventType": "COMPLETE", "eventTime": ts,
            "run": {"runId": run_id},
            "job": {"namespace": "prod-airflow", "name": job},
            "inputs": [{"namespace": "wh", "name": n} for n in inputs],
            "outputs": [{"namespace": "wh" if not o.startswith("model:") else "mlflow", "name": o} for o in outputs],
            "producer": "https://example.invalid/my-scheduler", "schemaURL": "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/RunEvent"}

events = [
    event("load_customers",   "r1", ["raw.customer_feed"],                 ["dw.customer"],                "2026-03-01T01:00:00Z"),
    event("build_features",   "r2", ["dw.customer", "dw.txn"],             ["fs.cust_features"],           "2026-03-01T02:00:00Z"),
    event("train_churn",      "r3", ["fs.cust_features"],                  ["model:churn@v7"],             "2026-03-01T03:00:00Z"),
    event("train_limit",      "r4", ["dw.customer"],                       ["model:credit_limit@v3"],      "2026-03-02T03:00:00Z"),
    event("train_fraud",      "r5", ["dw.txn"],                            ["model:fraud@v12"],            "2026-03-02T04:00:00Z"),
    event("report_kpi",       "r6", ["dw.customer"],                       ["bi.kpi_daily"],               "2026-03-02T05:00:00Z"),
]
print("one event, trimmed:"); print(json.dumps(events[2], indent=2)); print()

down = defaultdict(list)                       # dataset -> [(job, output, time)]
for e in events:
    for i in e["inputs"]:
        for o in e["outputs"]: down[i["name"]].append((e["job"]["name"], o["name"], e["eventTime"]))

def downstream(start):
    seen, q, paths = {start}, deque([(start, [start])]), []
    while q:
        node, path = q.popleft()
        for job, out, ts in down.get(node, []):
            if out in seen: continue
            seen.add(out); p = path + [f"--{job}-->", out]; paths.append(p); q.append((out, p))
    return paths

for p in downstream("dw.customer"):
    print(" ".join(p))
models = [p[-1] for p in downstream("dw.customer") if p[-1].startswith("model:")]
print("\nmodels downstream of dw.customer:", models)
print("not affected:", sorted({o["name"] for e in events for o in e["outputs"] if o["name"].startswith("model:")} - set(models)))
```

**Output (my run):** pure Python, `python -I`. No lineage server involved; the event is hand-built.
```text
one event, trimmed:
{
  "eventType": "COMPLETE",
  "eventTime": "2026-03-01T03:00:00Z",
  "run": {
    "runId": "r3"
  },
  "job": {
    "namespace": "prod-airflow",
    "name": "train_churn"
  },
  "inputs": [
    {
      "namespace": "wh",
      "name": "fs.cust_features"
    }
  ],
  "outputs": [
    {
      "namespace": "mlflow",
      "name": "model:churn@v7"
    }
  ],
  "producer": "https://example.invalid/my-scheduler",
  "schemaURL": "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/RunEvent"
}

dw.customer --build_features--> fs.cust_features
dw.customer --train_limit--> model:credit_limit@v3
dw.customer --report_kpi--> bi.kpi_daily
dw.customer --build_features--> fs.cust_features --train_churn--> model:churn@v7

models downstream of dw.customer: ['model:credit_limit@v3', 'model:churn@v7']
not affected: ['model:fraud@v12']
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

