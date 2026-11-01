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
