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

