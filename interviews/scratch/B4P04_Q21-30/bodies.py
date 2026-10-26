B = {}

B[21] = dict(
 say="An MLproject file is a small YAML recipe: a name, entry points with typed parameters, and an environment. `mlflow run` reads it, creates a run, and executes the command with the parameters filled in.",
 explain="""
- The file has `name`, `entry_points` (each with `parameters` that have a type and a default, and a `command`), and one environment key: `python_env`, `conda_env` or `docker_env`.
- `mlflow run . -P C=0.5` builds the command line, starts a run that is tagged `source.type = PROJECT`, and runs the command. Your script then logs into that same run (inside `mlflow run`, `start_run()` attaches to the run the CLI made, because the CLI sets the run id in an environment variable).
- `--env-manager local` skips building an environment and uses the Python you already have. The other choices are `virtualenv`, `uv` and `conda` (check `mlflow run --help` for your version). Only local is fast and also the least reproducible.
- If the folder is a Git repo, MLflow records the commit as a tag, and it can run straight from a Git URL. In my run the folder was not a Git repo, so no commit tag was written. I did not run the Git case.
- Why many teams skip it now (my view, hedge): a plain script plus a `dvc.yaml` or an orchestrator already gives the command, the parameters and the data lineage. MLproject adds a second place to declare the same things, and the environment build can be slow. It is still fine for small teams that want one command to rerun a tracked run.
- Failure modes: a parameter with the wrong type fails before the command starts; a missing default with no `-P` fails; `docker_env` needs a running Docker daemon (not available here, not executed).
""",
 example="`C` is declared `float, default 1.0`. `mlflow run . -P C=0.5` runs `python train.py --C 0.5 --max_iter 100`. Hand check: one new run, `params.C = 0.5`, `params.max_iter = 100` (default used), and `test_acc` on the iris test split.",
 codeintro="MLproject (YAML), `train.py` (Python), and the shell driver that ran everything in a fresh temp directory with a sqlite tracker. MLflow 3.17.2 here.",
 code=[("yaml", ["q21/MLproject"]), ("python", ["q21/train.py"]), ("bash", ["q21/run.sh"])],
 outintro="Real run, `--env-manager local`, MLflow 3.17.2, Python 3.13. The `source.name` line is a temp folder, so it will differ on your machine.",
 out=["q21/output.txt"],
 follow="""
- *Can I run it from GitHub?* Yes: `mlflow run https://github.com/org/repo -P C=0.5` clones and runs. Not executed here (no repo to point at).
- *How do I run it on a cluster?* `--backend` options exist (for example Kubernetes or Databricks). Not executed here; check current docs.
- *What replaces it?* A `dvc.yaml` stage, an Airflow or Prefect task, or a plain CLI. All of them can still log to MLflow.
""",
 mistakes="""
- Believing `mlflow run` makes the run reproducible. With `--env-manager local` it only records the command and parameters, not your installed libraries.
- Forgetting that `train.py` must call `mlflow.log_*` itself (or autolog). The CLI creates the run but does not know your metrics.
- Hard-coding the tracking URI in `train.py`, so the CLI and the script write to different places.
""")

B[22] = dict(
 say="The MLmodel file is the model's manifest. It lists the flavors (ways to load the model), the signature and the environment files. The `python_function` flavor gives every model one `predict` call, and a custom PythonModel lets me ship the preprocessing together with the model.",
 explain="""
- A logged model is a folder: `MLmodel`, `requirements.txt`, `conda.yaml`, `python_env.yaml`, plus the model files and, for custom pyfunc, an `artifacts/` folder (see the run output below).
- `MLmodel` lists `flavors`. An sklearn model has two: `sklearn` (load back as an sklearn object) and `python_function` (generic). A custom model has only `python_function`.
- Serving tools only need the pyfunc flavor, so one server can run sklearn, xgboost, pytorch or custom code behind `predict(DataFrame)`.
- Custom `PythonModel`: `load_context` runs once at load and reads the bundled files; `predict` runs per request. Put the scaler and the model inside, and callers cannot forget the scaling.
- Failure modes: the pickled class is serialised with cloudpickle, so loading needs a compatible Python and library set (the `python_version` and `requirements.txt` in the folder tell you which). Only load models you trust: pickle can run code on load. MLflow also warns that a Python object as `python_model` uses CloudPickle and suggests models-from-code (check current docs).
""",
 example="Iris rows 0, 60, 120 are classes 0, 1, 2. The custom model scales inside `predict`, so raw rows give `[0, 1, 2]`. A plain sklearn model that was trained on scaled data, loaded as pyfunc and fed the same raw rows, gives `[1, 2, 2]`: that is training-serving skew in one line.",
 codeintro="One script. It trains a scaler and a logistic regression, wraps both in `ScaledClf`, logs it, lists the folder, prints the `MLmodel` file and calls the loaded model.",
 code=[("python", ["q22/q22.py"]), ("bash", ["q22/run.sh"])],
 outintro="Real run (MLflow 3.17.2, sqlite tracker in a temp dir; warnings kept as printed, the per-line INFO logs were filtered out).",
 out=["q22/output.txt"],
 follow="""
- *Why not just pickle a sklearn Pipeline?* A Pipeline already bundles scaler and model. Custom pyfunc is for things a Pipeline cannot hold: rules, lookups, multiple models, post-processing.
- *What does `signature` in MLmodel do?* It lets pyfunc check input columns and types at predict time (see Q9).
- *Can I avoid pickle?* Yes, models-from-code logs a Python file instead of a pickled object. Not run here; check current docs.
""",
 mistakes="""
- Doing preprocessing in a notebook and logging only the bare model, so the server receives raw data and quietly gives wrong answers.
- Loading bundled files in `predict` instead of `load_context`, so they are read on every request.
- Ignoring `requirements.txt` in the model folder and then being surprised that load fails on a different Python.
""")

B[23] = dict(
 say="MLflow itself gives me `mlflow models predict` for a batch file and `mlflow models serve` for a small REST server with `/ping` and `/invocations`. For real production serving I would use a proper serving stack (Part 6).",
 explain="""
- Both commands take a model URI like `models:/iris_clf@champion`, which is the registry alias from Q8. Moving the alias changes what `serve` loads on its next start.
- The request body must have exactly one top-level key: `dataframe_split`, `dataframe_records`, `instances` or `inputs` (the MLflow 3.17.2 error text lists these four; check the docs for your version). The same rule applies to the input file of `predict -t json`.
- `--env-manager` chooses where the model runs: `local` (current Python), `virtualenv`, `uv`, or `conda` (conda needs conda installed). A fresh environment is safer and slower.
- `mlflow models build-docker` builds an image whose default entrypoint serves the model on port 8080 (from `--help`). Not executed here: no Docker daemon. Part 2 and Part 6 cover images and serving.
- Failure modes: a bare `{columns, data}` file without the wrapper key fails; a missing column is rejected by the signature check with an `INVALID_PARAMETER_VALUE` error JSON (real text below); `serve` with `local` uses whatever versions are installed, which may differ from the training environment.
""",
 example="Two iris rows are sent as `dataframe_split`. Both are setosa (class 0), so `{\"predictions\": [0, 0]}` is the hand-checkable answer. A single row with petal length 5.2 and petal width 2.3 should be virginica (class 2).",
 codeintro="`make_model.py` registers `iris_clf` v1 with alias `champion` in a sqlite registry; the shell script then runs `predict`, starts `serve` on 127.0.0.1:5088, sends three requests with curl, and stops the server.",
 code=[("python", ["q23/make_model.py"]), ("bash", ["q23/run.sh"])],
 outintro="Real run on localhost, MLflow 3.17.2. The last error line is cut for length. The `pip`/INFO startup noise was filtered out.",
 out=["q23/output.txt"],
 follow="""
- *Is `mlflow models serve` production ready?* It is fine for a demo or a simple internal tool. Autoscaling, auth, batching and rollout control come from the platform around it (Part 6, Part 3).
- *What is `/ping` for?* A health check; it returned 200 here.
- *How do I send a tensor?* Use `inputs` (check the docs for your version). Not run here.
""",
 mistakes="""
- Sending the DataFrame JSON without the `dataframe_split` wrapper key.
- Serving with `--env-manager local` and assuming the libraries match training.
- Pointing a service at `models:/name/latest` or a version number and then not knowing which model is live. Use an alias.
""")

B[24] = dict(
 say="An artifact is any file attached to a run. The tracking store keeps the run row; the artifact store keeps the bytes, at a location fixed when the experiment is created.",
 explain="""
- APIs: `log_artifact` (one file), `log_artifacts` (a folder), `log_figure`, `log_text`, `log_dict`, `log_table`. All write under `<artifact_location>/<run_id>/artifacts/...`. `download_artifacts` and `load_text` read them back.
- `artifact_location` is set at experiment creation (a default under `./mlruns`, or `--default-artifact-root` on a server, or the `artifact_location` argument as I did). Changing the server flag later does not move old experiments.
- With a remote server there are two modes. Direct access: the client writes to S3 itself and needs its own credentials. Proxied access (`--serve-artifacts`): the client talks only to the server, which holds the credentials. Check current docs for flags and defaults. Not executed here (needs S3 and a remote server).
- Classic failure: the client logs to a path that only the server can see, for example a server folder `/srv/art`. The client then tries to create `/srv/art` on its own machine and gets a permission or missing-path error. Proxied mode avoids this.
- Do not put huge files or secrets in artifacts. Artifacts are as widely readable as the store.
""",
 example="After the run, the listing should show six folders: `cfg`, `notes`, `outputs`, `plots`, `shards` (two files from `log_artifacts`) and `tables`. Hand check: `shards/part0.txt` and `part1.txt` exist because the loop wrote two files.",
 codeintro="A run that logs a figure, a dict, a text note, a CSV, a folder and a table to a custom `artifact_location`, lists them, then downloads three of them. Needs matplotlib (it was installed here).",
 code=[("python", ["q24/q24.py"]), ("bash", ["q24/run.sh"])],
 outintro="Real run, MLflow 3.17.2, local file artifact root.",
 out=["q24/output.txt"],
 notexec="Not executed: S3 or other object stores, `--serve-artifacts` against a remote server, and cross-machine path problems. Validation that did run: the artifact location is a plain path that I fixed at experiment creation and every file came back with the right content.",
 follow="""
- *Can I move artifacts to another bucket?* You copy the files and update the stored location. Plan this early; check current docs.
- *Where does the model go?* `log_model` is an artifact folder plus a registered model entry (Q8, Q22).
- *Large files?* Log a pointer and a hash (a DVC hash from Q15) instead of copying a dataset into every run.
""",
 mistakes="""
- Creating the experiment before the server's artifact root is right, then discovering it is stuck.
- Giving every laptop its own S3 keys instead of using proxied access.
- Logging a 5 GB dataset into every run.
""")

B[25] = dict(
 say="Aliases say which version is live, but governance needs more: tags for status and owner, a note for every move, and permissions on who may move an alias. The audit trail is mostly something I add myself.",
 explain="""
- Model versions carry tags (for example `validation_status`, `data_version`, `owner`) and a registered model has a description. The client API also returns a creation time for each version.
- Moving an alias is one call, `set_registered_model_alias`. Rollback is the same call pointed at the old version.
- What the client API did NOT give me in this run: who moved the alias and when. The alias map shows only the current target. So I wrap the move in a helper that writes `promoted_by`, `promoted_at` and a note as tags, ideally also to an append-only log outside MLflow.
- Tags keep only the last value per key. My rollback overwrote the first release note on v1 (see the output): history in tags is lossy. Use an external log, or one tag key per event.
- Who may move an alias: a plain local or open server has no per-user permission. An authenticated server, or a managed platform (Databricks, Azure ML, SageMaker), adds that. Check current docs. Not executed here.
- Edge case: `search_model_versions` returned an empty `aliases` list for a version that does hold an alias, while `get_model_version` showed it. Use `get_model_version` or the model's alias map when you need aliases.
""",
 example="Two versions. v1 is `pending`, v2 is `approved`. Alias goes v1 (first release), then v2, then back to v1. Hand check: after the rollback the alias map must read `{'champion': 1}`, and the v1 note must say `v2 -> v1`.",
 codeintro="Registers `iris_gov` twice (C=0.1, then C=5.0), tags the versions, moves the alias with an audit helper, rolls back and prints the history.",
 code=[("python", ["q25/q25.py"]), ("bash", ["q25/run.sh"])],
 outintro="Real run, MLflow 3.17.2, sqlite registry. Timestamps are from my run.",
 out=["q25/output.txt"],
 notexec="Not executed: authentication, permissions and any server that records who made a change. The tags above are written by my helper, not by MLflow.",
 follow="""
- *Who moved champion to v7?* Only what my helper and the server's own logs recorded. A managed platform may keep an audit log; check current docs.
- *Should CI move the alias?* Yes, with a service account and a gate. Part 7 owns that.
- *Tags or aliases for status?* Aliases for pointers (one version holds it); tags for facts about a version.
""",
 mistakes="""
- Treating the alias map as an audit log.
- Putting status only in the model name (`iris_prod_v2`).
- Letting every data scientist move `champion` from a notebook.
""")

B[26] = dict(
 say="A W&B sweep is a hyperparameter search run by W&B. I write a config (method, metric, parameters), call `wandb.sweep`, then run one or more `wandb.agent` processes that pull the next set of parameters.",
 explain="""
- Config: `method` is `grid`, `random` or `bayes`; `metric` has a name and a goal; `parameters` are either `values` (a list) or a distribution with min and max.
- The metric name must match what the script logs with `wandb.log`. A typo means bayes and early termination have nothing to optimise. My validator catches this against a list of logged names.
- Agents can run on many machines against the same sweep id. Cost control: cap runs with the `count` argument of `wandb.agent` (and a stop rule on the sweep; check current docs for the exact option). Early termination (`hyperband`) stops weak runs early.
- Grid with ranges does not make sense; grid needs discrete values and multiplies fast (5 x 5 x 3 x 2 = 150 runs).
- Versus Optuna: Optuna is a library that runs in your own process with pruning and storage you choose; W&B sweeps give a hosted controller and a dashboard. Optuna plus MLflow logging gives a fully self-hosted setup. Both are fine; the choice is about where you want the controller and the UI.
""",
 example="`lr` log-uniform from 1e-4 to 1e-1, `batch_size` from [16, 32, 64], `dropout` uniform from 0 to 0.5, `optimizer` adam or sgd, bayes on `val_auc` (maximise) with hyperband. Hand check: `min < max`, `lr` min above 0 (log), metric is one that `train.py` logs.",
 codeintro="`sweep.yaml`, the offline validator (pyyaml only), the helper that tries `wandb.sweep` without an account, and the driver.",
 code=[("yaml", ["q26/sweep.yaml"]), ("python", ["q26/validate_sweep.py", "q26/try_sweep.py"]), ("bash", ["q26/run.sh"])],
 outintro="The validator is my own checker (not a W&B tool) and covers only the rules in the code. The last line is the real `wandb.sweep` failure without an account (wandb 0.31.0).",
 out=["q26/output.txt"],
 notexec="Not executed: `wandb.sweep` and `wandb.agent` for real (they need an account and network), hyperband behaviour, multi-machine agents. Validation that did run: the YAML parses and passes my checks; the broken copy produces five errors.",
 follow="""
- *Random or bayes?* Random is a safe start and parallelises easily; bayes helps when each run is costly and the space is smooth.
- *How do I stop a runaway sweep?* Cap the count per agent and stop the sweep from the UI or CLI; check current docs.
- *Selection bias?* The best of N runs on validation is optimistic. Use a held-out test set once (Q11).
""",
 mistakes="""
- Metric name in the config differs from the logged key.
- A grid sweep over continuous ranges.
- Leaving agents running overnight with no run cap.
""")

B[27] = dict(
 say="A W&B Artifact is a versioned bundle of files. `log_artifact` creates a version (v0, v1, ...), `use_artifact` consumes one, and W&B draws the lineage graph between runs and artifacts for you.",
 explain="""
- Build: `wandb.Artifact(name, type)`, then `add_file`, `add_dir`, or `add_reference` (a pointer to a file in a bucket or URL; the bytes are not copied).
- The versions `v0`, `v1` and aliases like `latest` are assigned by the server when you log. Offline I could build the artifact and read its manifest and digest, but not see a version number.
- Same content gives the same digest; one more row in the CSV gives a different digest (output below). That is the same content-addressing idea as DVC hashes.
- Compare: DVC keeps pointers in Git and the bytes in a remote you own. MLflow attaches artifacts to a run. W&B keeps versions and lineage in its service (cloud or self-hosted).
- Failure modes: an `s3://` reference needs boto3 and credentials; here it failed with a clear error. A reference artifact points at data that someone else can change or delete, so a checksum matters.
""",
 example="A dataset artifact with `train.csv`, an image folder and a reference to a remote parquet file has 3 manifest entries. After appending one row to `train.csv`, the artifact digest must change. Both hold in the output.",
 codeintro="Builds the artifact locally with `wandb 0.31.0`, prints the manifest and digests, and shows the S3 reference error. The two lines at the end are the real service calls that I did not run.",
 code=[("python", ["q27/q27.py"]), ("bash", ["q27/run.sh"])],
 outintro="Real offline run. Nothing was uploaded. The first line is wandb's own progress message.",
 out=["q27/output.txt"],
 notexec="Not executed: `run.log_artifact`, `run.use_artifact`, version numbers and aliases, the lineage graph, S3 references. They need an account and network. Validation that did run: artifact manifests and digests built locally.",
 follow="""
- *Can I use W&B Artifacts without W&B runs?* There are API calls for it; not tested here, check current docs.
- *How do I pin a version?* `use_artifact('train-data:v3')`. An alias like `latest` moves, so pin a version in training code.
- *Lineage gap?* Only objects logged through W&B are in the graph. Raw tables upstream are not.
""",
 mistakes="""
- Using `latest` in a training script and losing reproducibility.
- Using references for data that can change, with no checksum.
- Assuming offline mode gives versions; they appear after sync or log.
""")

B[28] = dict(
 say="I choose the tracker by who runs it and who may see the data. MLflow is the open, self-hosted default. W&B is the polished hosted one. Cloud-native trackers fit if the whole stack is on one cloud.",
 explain="""
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
""",
 example="A bank team with strict data rules and 15 data scientists on Azure: managed MLflow in Azure ML, no SaaS egress. A three-person startup with GPUs on rented machines: W&B hosted free tier (check current terms) for speed.",
 codeintro="No code. This is a pure comparison.",
 code=None,
 outintro="not executed. Nothing to run; this is a comparison written from general knowledge, not from opened vendor pages. Check current docs and terms for every row.",
 out=[],
 follow="""
- *Can I switch later?* Params and metrics export easily; dashboards and reports do not. Keep the model in MLflow format and the data in DVC.
- *Do I need both MLflow and W&B?* Usually not (Q14). Some teams use W&B for experiments and MLflow for the registry; that doubles the logging code.
- *Self-host W&B?* An option exists on some plans; check current terms.
""",
 mistakes="""
- Comparing price lists from memory.
- Ignoring data residency until a security review.
- Treating the tracker as the system of record for data versions.
""")

B[29] = dict(
 say="A model card is a short, standard document about a model: what it is for, what data it was trained on, how well it works (overall and on slices), its limits and its owner. I generate the factual parts from MLflow so it cannot drift from the run.",
 explain="""
- Contents (from the Mitchell et al. model card idea; check current docs for template variants): intended use, training data and version, parameters, metrics overall and per slice, inputs and outputs, limitations and ethics, owner, how to retrain.
- Facts come from the run and registry: params, metrics, tags, signature, run id. Judgement parts (intended use, limits) stay human-written and are marked as such in my script.
- Attach it two ways: as an artifact on the training run (`MODEL_CARD.md`) and as a pointer tag on the registered version; also commit the markdown in the repo for review.
- Failure modes: a stale card (written once, never regenerated); a missing tag silently becoming an empty field (my script prints `MISSING` and reports it); slice metrics on very few rows look precise but mean little (the demo test set has 15 and 30 rows).
- A card does not replace tests. It documents what was tested.
""",
 example="Iris model v1: tags carry the data version and git SHA (demo values), three accuracy metrics, four double inputs. All appear in the card; a tag removed from the run would show as `MISSING`. Test accuracy is 1.000 on only 45 test rows, so I would say so.",
 codeintro="Trains, registers, and builds the markdown from the stored run and signature, logs it back to the run and sets a pointer tag.",
 code=[("python", ["q29/q29.py"]), ("bash", ["q29/run.sh"])],
 outintro="Real run, MLflow 3.17.2. The git SHA and data version are made-up demo strings.",
 out=["q29/output.txt"],
 follow="""
- *Who owns the card?* The model owner, with review in the PR. The facts are generated.
- *Per-slice metrics?* Pick slices in advance (region, device, age band) and log them as metrics, as the demo does with petal length.
- *Regulated settings?* The card feeds the audit file (Q40), it is not the audit file.
""",
 mistakes="""
- Hand-typing metrics into a Word file.
- One overall number and no slices.
- No owner and no retrain instructions.
""")

B[30] = dict(
 say="Delta and Iceberg give time travel over one table, inside the table format, until old snapshots are vacuumed. DVC pins whole files by hash in Git. lakeFS branches a whole object store. I pick by the data shape and by how long the snapshot must live.",
 explain="""
- Delta Lake and Iceberg: every commit writes a new snapshot (a manifest listing immutable data files). You query a version or a timestamp (`VERSION AS OF`, `TIMESTAMP AS OF` in Delta; Iceberg has the same idea; check current docs for syntax). Concept level here: no cluster available.
- Retention: `VACUUM` (Delta) and `expire_snapshots` (Iceberg) delete files no kept snapshot needs. After that, time travel to the older version fails. Defaults and safe minimums exist; check current docs.
- DVC: file or folder level, content-hash pointers in Git, bytes in a cache and remote. It lasts as long as the remote keeps the hash and Git keeps the tag. It does not understand rows.
- lakeFS: branches, commits and merges over an object store, zero-copy; good for ingest-validate-merge on lots of files. Some sources report a changed stewardship of DVC (unverified; check news).
- Choice: analytics table feeding features: Delta or Iceberg (rows, schema evolution, SQL). Image dataset: DVC or lakeFS (files). Training snapshot that must live for years: copy that snapshot out to a protected, immutable location and pin it by hash (DVC tag, or a table version that is explicitly excluded from vacuum); never rely on the default retention.
- Failure mode (shown below): the snapshot a model was trained on shares files with other versions; one vacuum removes them and the model can no longer be reproduced.
""",
 example="Version 0 has ids 1 and 2. Version 1 adds id 3. Version 2 rewrites the first file (id 2 changes from 20 to 25). Training used version 1. Vacuum keeping only the latest version deletes `data-v0-0.json`, which v1 also needs. Hand check: both v0 and v1 now fail.",
 codeintro="A pure-Python toy snapshot table (about 40 lines): immutable data files, one manifest per version, `read(version)`, `read(ts=...)` and `vacuum`. It teaches the idea only; it is not Delta or Iceberg code.",
 code=[("python", ["q30/toy_table.py"]), ("bash", ["q30/run.sh"])],
 outintro="Real run of the toy. It shows retention behaviour, not any real table format.",
 out=["q30/output.txt"],
 notexec="Not executed: Delta Lake, Iceberg, lakeFS, Spark. Validation that did run: the toy table reproduces the snapshot, timestamp lookup and vacuum failure logic.",
 follow="""
- *Can I combine them?* Yes: Delta table for features, and a DVC pointer to an exported Parquet snapshot for each training run.
- *Why not keep everything forever?* Storage cost and deletion duties (for example a data-protection request). Plan retention and deletion together.
- *Timestamp or version?* Version number is exact; a timestamp depends on clocks and commit times.
""",
 mistakes="""
- Assuming time travel is a backup. It stops at the retention window.
- Pinning only the table name and not the version or snapshot id in the training record.
- Running vacuum with a very short retention to save space, with a long-running job still reading.
""")
