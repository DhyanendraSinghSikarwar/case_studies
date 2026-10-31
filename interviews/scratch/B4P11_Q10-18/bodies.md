@@Q10@@
**Say this first (1 line):** Upload the model once to the Model Registry, then either deploy it to an endpoint for live traffic (replicas always on, traffic split between versions) or run a batch prediction job that reads files or a table, writes results, and shuts the machines down.

**Then explain:**
- **Registry then deploy.** The Vertex Model is the registry entry. Deploying puts a model version on an endpoint as a "deployed model" with an id, a machine type, and min and max replicas. The endpoint's `traffic_split` maps deployed-model ids to percentages that must add up to 100 (check current docs for the exact rule).
- **Canary.** Deploy v2 next to v1 and give it a small share, say 90 / 10. Rollback is setting the split back to 100 / 0 and undeploying v2. Keep min replicas at 1 or more if you cannot afford a cold start.
- **Public or private.** Options are a shared public endpoint, a dedicated endpoint, or a private endpoint (VPC peering or Private Service Connect). Which of these exist for your Region and model type: check current docs. Q24 covers the network side.
- **Batch is a different product.** A `BatchPredictionJob` takes Cloud Storage files (jsonl, csv and so on) or a BigQuery table, and writes to a bucket prefix or a BigQuery dataset. It uses dedicated replicas for the job only. There is no endpoint, no traffic split, and no latency promise.
- **Map to the others (concept only).** Azure: managed online endpoint (endpoint holds deployments, blue and green, traffic map) and batch endpoint (default deployment, `invoke` returns a job). SageMaker: real-time endpoint with weighted production variants, and batch transform. Part 10 owns the AWS depth, Part 6 owns rollout mechanics.
- **Failure modes.** Split does not sum to 100 or names an unknown id. Endpoint and model in different Regions. Machine type or GPU quota not available in the Region. Batch job service account cannot read the input bucket (Q29 walks that). Output prefix already holds old files.

**Example:** v1 and v2 deployed, split 90 / 10. Of 1,000 requests about 900 reach v1 and about 100 reach v2 (random routing, so not exact). A split of 90 / 20 sums to 110 and is rejected. Nightly scoring of a table is batch: no one waits on a reply.

**Code:** the proto objects below are what the SDK builds and sends. Nothing here calls Google.
@@CODE q10_vertex_endpoint.py py@@

**Output (my run):** google-cloud-aiplatform 1.165.1, Python 3.13, run with `python3 -I`, offline.
@@OUT q10.out@@
Not executed: `Model.upload`, `Model.deploy`, `Endpoint.predict`, `Model.batch_predict`, and even `ai.Endpoint("projects/.../endpoints/1")`, because the SDK constructor fetches the resource from the API. Those need a project, billing, credentials and quota. The split check function is my own helper; the service does its own validation.

**Follow-ups:**
- *How do you roll back a bad v2?* Set the split to `{a: 100}`, confirm errors drop, then undeploy `b`. Do not delete the model version.
- *Online or batch?* If nobody waits and the input is already in a bucket or table, batch. If a user or service waits on the answer, online. Part 6 has the full reasoning.
- *What does an endpoint need that batch does not?* Always-on replicas, so you pay for idle capacity (no figures here), autoscaling limits, and a latency alert.

**Common mistakes:**
- Treating the split as relative weights instead of percentages that sum to 100.
- Deploying with min replicas 0 or 1 and then being surprised by cold starts or a single point of failure (check current docs for what your mode allows).
- Using an online endpoint for a nightly job and leaving it running.
- Saying "it works" from objects built offline. Building a proto proves the shape, not that the service accepts it.

@@Q11@@
**Say this first (1 line):** None of the three has a universal stage field you can trust, so I put the stage in a tag (Azure ML) or an alias (Vertex, MLflow), keep the version number immutable, and let a small validator refuse a prod entry without a source run and a second-person approver.

**Then explain:**
- **Azure ML.** Models are versioned assets in a workspace, or in a shared registry that several workspaces can use. Types include MLflow models and custom models. There is no built-in dev, staging, prod stage, so use tags (`stage=prod`) and promote by copying the same version to the next workspace or registry. Check current docs for how registry-to-workspace copy works.
- **Vertex AI Model Registry.** A model has numbered versions. Versions carry aliases (a movable pointer such as `prod`) and models carry labels. Deploy and batch-predict actions work from a version. I checked that the Vertex Model proto has `version_id`, `version_aliases` and `labels` fields (one-off listing of the proto fields, not part of the script below).
- **MLflow registry.** Aliases (`models:/churn@prod`) replaced the older stage idea in recent MLflow versions (check current docs for your version). Portable across clouds, but you run and secure it yourself.
- **Convention that works on all three.** Immutable identity = name plus version. Movable pointer = alias or tag. Never put the stage in the name (`churn-prod` makes a second model, not a promotion). Promotion = move the pointer after tests pass, with the approval recorded.
- **Failure modes.** Alias moved with no record of who did it. Same name used in two stages so lineage splits. Source run missing, so nobody can reproduce it. Approver equals the person who registered it.

**Example:** `churn` v7 is trained by run-8841 by asha. It gets `stage=staging` after the tests. For prod, ravi approves; the entry is `{name: churn, version: 7, stage: prod, source_run: run-8841, approver: ravi}`. Hand check: `churn-prod` v3 fails because the name contains a stage word.

| | Azure ML | Vertex AI | MLflow |
|---|---|---|---|
| Immutable id | name:version | model id + version id | name + version |
| Stage carrier | tag | version alias | alias |
| Shared across envs | shared registry | same project, or copy across projects | one server |
| Pointer example | `azureml:churn:7` | `.../models/ID@prod` | `models:/churn@prod` |

**Code:**
@@CODE q11_registry_check.py py@@

**Output (my run):** `python3 -I`, pure Python, no cloud.
@@OUT q11.out@@
Not executed: any real registry call (register, copy, alias change). The table is my convention, not a vendor rule.

**Follow-ups:**
- *Where does approval live?* In the pipeline (a protected environment or manual gate) and in the entry's `approver` field. The registry is the record, not the gate. Part 7 covers gates.
- *Alias or tag, which is safer?* Both can be moved by anyone with write rights, so restrict who can write and log the change.
- *Can I use one registry for three environments?* Yes with aliases or tags, but many teams keep a separate prod registry or project for access control.

**Common mistakes:**
- Encoding the stage in the model name.
- Using "latest" as the production pointer.
- Registering a model with no source run or data version.
- Assuming an Azure registry has a stage field because the older MLflow docs show one.

@@Q12@@
**Say this first (1 line):** On both clouds three different identities do three different jobs: one creates the job, one runs as the job and reads the data, one pulls the image, and I give each the smallest role at the smallest scope.

**Then explain:**
- **Azure side.** Entra ID gives users, service principals and managed identities. A managed identity is system-assigned (tied to the resource) or user-assigned (a standalone object you attach). The workspace has its own identity for plumbing (storage, registry, Key Vault). A compute cluster can have its own identity, and a job can run as that identity or, with user identity passthrough, as the submitting user. Access is Azure RBAC: roles like Storage Blob Data Reader on the storage scope. Check current docs for built-in role names.
- **Google side.** Principals are users, groups and service accounts. A custom training job runs as a service account you attach, otherwise a Google-managed default is used (check current docs). Vertex has service agents, Google-managed accounts that do plumbing such as image pulls. IAM roles are bound on the project, bucket or repository. The caller who attaches a service account to a job needs permission to act as it (`roles/iam.serviceAccountUser`). Impersonation uses a token-creator role so a CI identity can borrow a service account without a key.
- **Who does what.** Creates the job: the CI service principal or deployer service account. Reads data: the compute or job identity. Pulls the image: the registry-reading identity (workspace or compute identity on Azure; job service account or service agent on Google). Writes outputs: the job identity, scoped to the output container or bucket.
- **Failure modes.** Role granted to the wrong identity. Role granted at a scope that does not cover the path. New role assignment not effective yet (propagation delay). Owner or Contributor handed out "to make it work".
- **Not like for like.** Azure RBAC data-plane roles are separate from management roles; on Google a single IAM role can cover both. AWS equivalent is IAM roles, covered in Part 10.

**Example:** Azure training job: CI service principal has a workspace role to create jobs. The cluster's user-assigned identity has Storage Blob Data Reader on the input container and Storage Blob Data Contributor on the output container. Google: the deployer service account has `roles/aiplatform.user` and act-as on the job service account; the job service account has `objectViewer` on the input bucket and `objectAdmin` on the output bucket.

**Code:** the role matrix and a validator. Role names are examples (check current docs for exact built-in roles).
@@CODE q12_role_matrix.yaml yaml@@
@@CODE q12_check.py py@@

**Output (my run):** `python3 -I q12_check.py q12_role_matrix.yaml`, pyyaml only.
@@OUT q12.out@@
Not executed: no role assignment, IAM binding or token exchange happened on either cloud. The validator only checks that my matrix is complete and not lazy.

**Follow-ups:**
- *Why not give the job the creator's rights?* A job that can create jobs can spread. Keep runtime narrow.
- *Key file or identity?* Identity. Federation and managed identities mean no long-lived secret (Q25).
- *User or system-assigned managed identity?* User-assigned when several resources share one set of rights or you want to pre-grant roles before creation.

**Common mistakes:**
- Granting a role to the user and wondering why the job fails (the job runs as a different identity).
- Granting at subscription or project scope for convenience.
- Forgetting the image-pull permission and blaming the code.
- Forgetting that a role change can take a few minutes to take effect.

@@Q13@@
**Say this first (1 line):** The training script stays the same and only the tracking URI and auth change, so I read the URI from an environment variable, run it against a local sqlite MLflow, and let the platform inject the real one.

**Then explain:**
- **Same:** `mlflow.set_experiment`, `start_run`, `log_param`, `log_metric`, tags. Your code does not care where the server is.
- **Local:** a sqlite URI (`sqlite:///ml.db`) works for development. I used the sqlite backend with MLflow 3.17.2. The Wave A run found the plain file store refused unless opted in (not re-run here; check current docs for your version).
- **Azure ML:** with the `azureml-mlflow` plugin the tracking URI starts with `azureml://` and points at the workspace. Auth is an Entra token (for example from `DefaultAzureCredential`). Inside an Azure ML job the URI is normally set for you (check current docs). Artifacts go to the workspace's default storage.
- **Vertex AI Experiments:** not MLflow by default. You call `aiplatform.init(experiment=...)` then the SDK's run and logging calls, which use Vertex ML Metadata. So a script that is portable keeps logging behind a thin function, or uses MLflow on both sides with a server you run.
- **Do not hard-code:** the tracking URI, experiment name per environment, artifact path, any key or token, the workspace id.
- **Failure modes.** No plugin installed, so the `azureml` scheme is unknown at first use. Token expired in a long job. Artifact store unreachable from compute (network or role). Experiment names colliding between dev and prod.

**Example:** the same script logs `lr=0.1`, `auc=0.85`, `loss=0.3` locally. Hand check: `auc = 0.80 + 0.5 * 0.1 = 0.85`, `loss = 0.4 - 0.1 = 0.3`.

**Code:**
@@CODE q13_train_portable.py py@@
```bash
# local: sqlite backend in a temp dir
MLFLOW_TRACKING_URI="sqlite:///$PWD/ml.db" python3 -I q13_train_portable.py
# Azure ML URI (fake subscription id): only proves the client takes the scheme; the script returns before any call
MLFLOW_TRACKING_URI="azureml://centralindia.api.azureml.ms/mlflow/v1.0/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg/providers/Microsoft.MachineLearningServices/workspaces/ws" python3 -I q13_train_portable.py
```

**Output (my run):** mlflow 3.17.2 with azureml-mlflow 1.60.0 installed, Python 3.13 (one MLflow hint log line removed).
@@OUT q13.out@@
Not executed: no call to a real Azure ML workspace, and no Vertex AI Experiments call (the `azureml` branch returns before any request). `set_tracking_uri` accepting the scheme does not prove the plugin resolves it or that auth works; that happens at the first real call.

**Follow-ups:**
- *Why not just use the cloud's native tracker?* You can. The cost is code that does not move. A thin wrapper keeps the choice cheap to change.
- *Where do artifacts go?* Azure ML: workspace blob storage. Local sqlite: the local `./mlruns` path or the artifact root you set. Check current docs for your setup.
- *How do you stop dev runs polluting prod experiments?* Different experiment names or different workspaces, set by environment variable.

**Common mistakes:**
- Hard-coding the workspace URI in the script.
- Testing only locally and discovering auth on the first cloud run.
- Logging secrets as params.
- Assuming MLflow code runs unchanged on Vertex.

@@Q14@@
**Say this first (1 line):** There is no best platform; the winner follows data gravity and identity, so I give each org a weighted score, show that the weights decide the answer, and pilot one real pipeline before standardising.

**Then explain:**
- **Criteria.** Data gravity (where the data already lives), identity (Entra or Google identity already in use), skills in the team, compliance and audit needs, existing contracts, GPU availability in your Region (check current docs), and exit cost.
- **Bank-owned GCC on Microsoft 365 and Entra:** lean Azure ML. Identity and compliance reporting are already there. Pilot: one batch scoring pipeline with managed identities and a private workspace.
- **Consumer product company with data in BigQuery:** lean Vertex AI. Data stays where it is, and the warehouse team already knows Google IAM. Pilot: train from a BigQuery table, register, batch predict back into BigQuery.
- **Services firm serving clients on all three clouds:** do not standardise on one. Standardise on containers, MLflow and Terraform, and use each client's cloud. Pilot: the same pipeline template on two clouds.
- **Opinion, not fact.** The comparison articles I found are commercial and I did not open them. Region and GPU availability: check current docs.
- **Failure modes.** Picking by a demo. Ignoring where the data is and paying to move it. Treating "we have a contract" as a technical reason.

**Example:** Hand check for the bank on Azure ML: weights `[2,4,2,5,3,2,1]` sum to 19; scores `[3,5,4,5,5,3,3]` give `(6+20+8+25+15+6+3) / 19 = 83 / 19 = 4.37`.

**Code:** the scores and weights are my judgement inputs, not measurements.
@@CODE q14_platform_score.py py@@

**Output (my run):** `python3 -I`, pure Python.
@@OUT q14.out@@
Same scores, different weights: the services firm's winner flips from Azure ML (client A, identity heavy) to Vertex (client B, data heavy). That flip is why the weights are the real argument. Not executed: no pilot, no benchmark, no price data.

**Follow-ups:**
- *Who sets the weights?* The platform owner with security, data and finance in the room. Write them down before scoring.
- *What if the scores are wrong?* The pilot tests the top two scores that mattered most, not everything.
- *Where does SageMaker fit?* Same method: add a column. Part 10 owns AWS depth.

**Common mistakes:**
- Scoring first and choosing weights afterwards to fit a preferred answer.
- Ignoring exit cost until the contract renews.
- Quoting a price or benchmark from a vendor blog.
- Standardising a services firm on one cloud its clients do not use.

@@Q15@@
**Say this first (1 line):** A datastore is a named pointer to storage (Blob, Data Lake or Files) with identity-based or credential-based access; a data asset is a versioned reference to a path inside it, and a job gets it mounted or downloaded.

**Then explain:**
- **Datastore types.** Azure Blob, Azure Data Lake Gen2, Azure Files (check current docs for others). Access is identity-based (the user or compute identity needs a storage role, such as Storage Blob Data Reader) or credential-based (an account key or SAS token stored with the datastore).
- **Path forms.** `azureml://datastores/<name>/paths/<path>`, a registered asset `azureml:<name>:<version>`, and direct URLs such as `https://` or `abfss://` (check current docs for the full list).
- **Data asset types.** `uri_file` (one file), `uri_folder` (a folder), `mltable` (a table definition with a schema and loading steps). An asset is versioned, so a job can say which data it used.
- **How a job gets it.** `ro_mount` mounts read-only, `download` copies to the node, `direct` passes the path (check current docs for modes per type).
- **Failure modes.** Identity-based datastore but the compute identity has no storage role (a 403 at job start). Asset points at a path that moved. Account key rotated while a datastore still holds the old one.
- **What Azurite is.** It speaks the Blob storage API on my laptop. It is not Azure ML, not Entra auth, and it does not check RBAC. It proves the storage API shape only.

**Example:** upload `churn/2026-10/part-0.csv` (3 lines) to a container, then define `churn-raw` v1 as the `churn/2026-10/` folder. A second version, `uri_file`, points at the single file.

**Code:** a documented public Azurite development account is used (the key is the published Azurite one, not a secret). Start Azurite on my own port, run the script, stop it.
@@CODE q15_azurite_data.py py@@
```bash
azurite-blob --blobPort 8611 --location /tmp/claude-0/b11_q10_18/q15 --skipApiVersionCheck --silent &
python3 -I q15_azurite_data.py 8611
kill %1        # stop the emulator
```

**Output (my run):** azurite 3.37.0 (npm), azure-ai-ml 1.35.2, azure-storage-blob 12.19.0, Python 3.13. Azurite stopped afterwards (port 8611 closed).
@@OUT q15.out@@
`credentials: NoneCredentialConfiguration` means the offline datastore object carries no stored secret, which is how an identity-based datastore looks (my reading; check current docs). Not executed: registering the datastore or data asset, Entra auth, RBAC, a job mounting it.

**Follow-ups:**
- *Identity-based or key-based?* Identity-based by default: no secret to rotate, access follows roles. Key-based only when a store cannot use identity.
- *mount or download?* Mount for big data read once in a streaming way, download when you need fast repeated local access. Test on your data.
- *What goes in `mltable`?* A small YAML describing paths and read steps, so the schema travels with the data.

**Common mistakes:**
- Treating Azurite passing as proof the Azure ML job will read the data.
- Putting an account key in the repo.
- Forgetting data assets are versioned and pointing jobs at "latest".
- Giving the user the storage role but not the compute identity.

@@Q16@@
**Say this first (1 line):** An environment is a versioned recipe for the runtime: a base image plus a conda file, or a Dockerfile build, and I pin every package so the same job tomorrow runs the same code.

**Then explain:**
- **Curated or custom.** Curated environments are maintained by the service with common frameworks (check current docs for what they contain). Custom ones are yours. Use curated for quick starts and custom when you need pinned, reviewed dependencies.
- **Two ways to define.** Base image plus `conda_file`, or a build context with a Dockerfile. The service builds and caches the image, usually on first use (check current docs for when and where).
- **Versioning.** An environment has a name and a version, and a job references `azureml:name:version`. Pin the version in jobs.
- **Reproducibility.** Unpinned pip packages drift. The same YAML builds a different image next month. Pin versions, and pin the base image tag.
- **Vertex comparison.** You build your own container image and push it to Artifact Registry, then reference it as `image_uri` in the job. You own the build, the scan and the tag.
- **Failure modes.** Build context path wrong (the loader failed on a missing folder, see output). Unpinned `pandas`. Image too big, so job start is slow. Base image tag `latest`.

**Example:** `conda.yml` pins `scikit-learn==1.5.2` and `mlflow==2.17.0` but leaves `pandas` unpinned, so the check fails. `conda_good.yml` pins all three.

**Code:** the two environment YAMLs and the conda file, shown together (separate files in practice), then the checker.
@@CODE q16_files.yaml yaml@@
@@CODE q16_env_check.py py@@

**Output (my run):** azure-ai-ml 1.35.2, Python 3.13.
@@OUT q16.out@@
The first run of the loader on the Docker environment failed because the build folder did not exist: the SDK validates the context path at load time. I created `docker-context/Dockerfile` and it loaded. Not executed: any image build, and nothing was registered. Versions in the YAML are examples.

**Follow-ups:**
- *Is pinning enough?* No, transitive dependencies can still move. Use a lock file for strong reproducibility.
- *Curated or custom for production?* Custom, pinned, built in CI, scanned.
- *Where does Docker depth live?* Part 2.

**Common mistakes:**
- `image: ...:latest`.
- Editing an environment in place instead of publishing a new version.
- Mixing conda and pip packages without pinning either.
- Assuming the check passes if the YAML loads.

@@Q17@@
**Say this first (1 line):** A batch endpoint is a stable name with one default deployment; `invoke` starts a job over a folder or data asset, and Vertex batch prediction is the same idea without a named endpoint: you submit a job and read its output.

**Then explain:**
- **Azure shape.** Batch endpoint = name and auth. Batch deployment = model, compute cluster, settings (mini-batch size, instance count, concurrency per instance, retry, error threshold, output action). A model can be an MLflow model (no scoring script) or a custom model with a scoring script.
- **No traffic split on batch.** To roll back or promote you switch the default deployment, not a percentage.
- **Output action.** `append_row` collects results into one file; `summary_only` leaves output to your script (check current docs).
- **Vertex shape.** `BatchPredictionJob`: model, input (Cloud Storage files or BigQuery), output prefix or dataset, dedicated replicas (starting and maximum). No endpoint needed. Q10 has the proto objects.
- **Part 6 owns when to choose batch.** Here: nothing waits on the answer and the volume is large.
- **Failure modes.** Mini-batch too large for memory. Error threshold set so one bad file kills the run, or set so everything silently fails. Output file overwritten between runs. Compute cluster at min nodes 0 and quota missing. Row count of output differs from input.

**Example:** 2,000,000 rows in 200 files of 10,000 rows. `mini_batch_size=1` (one file each), 4 nodes, 2 workers per node = 8 workers. 200 mini-batches / 8 workers = 25 waves. Hand check: 2,000,000 / 10,000 = 200; 200 / 8 = 25.

**Code:** the endpoint and deployment are built offline; the invoke plan is printed, not run. I assume `mini_batch_size` counts files for file input (check current docs).
@@CODE q17_batch_plan.py py@@

**Output (my run):** azure-ai-ml 1.35.2, Python 3.13.
@@OUT q17.out@@
Not executed: create or invoke of the endpoint, and the `az ml batch-endpoint invoke` command in the plan (the CLI is not installed here). The wave arithmetic ignores start-up time and uneven file sizes, so it is a planning number, not a prediction.

**Follow-ups:**
- *How do you know the job did all rows?* Compare the output row count to the input count before publishing.
- *How do you re-run a failed night?* Invoke again with the same input asset version; make writes idempotent or write to a dated path.
- *Azure batch vs Vertex batch?* Azure keeps a named, versioned endpoint with a default deployment; Vertex is a one-off job per run. Pick on where the data lives (Q14).

**Common mistakes:**
- Looking for a traffic split on a batch endpoint.
- Using `append_row` and then having two runs write into the same output.
- Never checking the row count.
- Setting error threshold to ignore every error.

@@Q18@@
**Say this first (1 line):** Notebook VMs are cheap to start and easy to forget, so the controls are the same on both clouds: idle shutdown, a scheduled stop, a dedicated identity, no public IP, an owner label, and a cap on which machine types people may create.

**Then explain:**
- **Vertex AI Workbench** instances are VMs in your project running JupyterLab, with a service account attached and settings for idle shutdown and network (check current docs for no-public-IP options). **Colab Enterprise** runs notebooks on runtimes created from templates, with managed lifecycle (check current docs).
- **Azure ML compute instance** is a VM in your workspace. Knobs: idle time before shutdown, start and stop schedules, assigned user, SSH on or off, node public IP on or off (needs a virtual network), identity.
- **Who owns the VM:** in both clouds the VM sits in your subscription or project, so you pay for it and you secure it. The platform provides images and lifecycle tools.
- **Stopping the 8-GPU leak.** Layered: (1) idle shutdown, (2) a scheduled stop each evening, (3) policy that limits allowed machine types or GPU counts (Azure Policy, Google Organization Policy; check current docs), (4) quota per Region or per project so one person cannot create many, (5) owner label on every instance plus a daily report, (6) budget alerts (Part 12 covers cost).
- **Reproducible and out of production.** Notebooks explore; production runs as jobs from a script in git. Strip outputs before commit, pin the environment, run the notebook in CI with papermill if you must, and never let a notebook identity write to the prod registry.
- **Failure modes.** Idle shutdown never fires because a kernel keeps polling (check current docs for what counts as idle). Broad Owner or Editor role on the notebook identity. Public IP plus open SSH. Data copied to the VM disk and left there.

**Example:** `gpu-bob-forever`: an 8-GPU machine, no idle shutdown, public IP, SSH open, Contributor role, no owner. The lint reports all of that. `wb-carol` has an idle time of 180 min, `roles/editor`, and no scheduled stop.

**Code:** the YAML shape is my own simplified schema (not an Azure or Google file format). The `ComputeInstance` line shows the same knobs on the real Azure entity, built offline.
@@CODE q18_samples.yaml yaml@@
@@CODE q18_notebook_lint.py py@@

**Output (my run):** run in the azure-ai-ml 1.35.2 venv with `python3 -I`; the same script under plain Python skips the `ComputeInstance` line. Exit code 1 because two samples fail.
@@OUT q18.out@@
Not executed: no Workbench instance, Colab Enterprise runtime or compute instance was created; the policies and quotas named above were not tested. The 120-minute limit is my example policy, not a default.

**Follow-ups:**
- *Who gets the GPU notebook?* Few people, via a request, with a stop schedule. Others use CPU notebooks and submit GPU jobs.
- *Why not ban notebooks?* People are faster in them. Control cost and identity instead.
- *How do you catch ones already running?* A scheduled job lists instances and flags the lint failures; alert the owner label.

**Common mistakes:**
- Relying on people to remember to stop the VM.
- Giving the notebook identity the same rights as the deployment identity.
- Running scheduled production work from a notebook.
- Setting idle shutdown but leaving the VM on a shared service account nobody owns.
