# Book 4 Part 4, Q1-Q10 answers (Wave B)

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

