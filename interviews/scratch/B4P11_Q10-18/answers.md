# Book 4 Part 11 answers Q10-Q18

### Q10 ⭐⭐⭐ 🟡 Vertex AI endpoints and batch prediction: upload a model to the Model Registry, deploy to an endpoint (machine type, min and max replicas, traffic split between deployed models, dedicated versus shared public endpoint, private endpoint), versus a batch prediction job reading from Cloud Storage or BigQuery. Compare with Azure managed online and batch endpoints and with SageMaker by concept. Build Endpoint and BatchPredictionJob references offline and say what cannot be shown without a project.
**Asked at:** GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs') | Cross-cloud comparison articles (TechTarget 'Compare Google Vertex AI vs Amazon SageMaker vs Azure ML', cloudoptimo, gmicloud, superwise, a redresscompliance licensing piece; search snippets only, not opened; several authors sell competing services or advice, so conclusions treated as opinion)
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
```python
"""Q10: Vertex endpoint + batch prediction as proto objects, offline. No network, no aiplatform.init."""
import warnings; warnings.filterwarnings("ignore")
import google.cloud.aiplatform as ai
from google.cloud.aiplatform_v1.types import (DeployedModel, DedicatedResources, MachineSpec, Endpoint,
    BatchPredictionJob, BatchDedicatedResources, GcsSource, GcsDestination, BigQuerySource, BigQueryDestination)

print("google-cloud-aiplatform", ai.__version__)
MODEL = "projects/demo-proj/locations/asia-south1/models/111"

def dm(id_, version, min_r, max_r):
    return DeployedModel(
        id=id_, model=MODEL, model_version_id=version, display_name=f"churn-v{version}",
        dedicated_resources=DedicatedResources(
            machine_spec=MachineSpec(machine_type="n1-standard-4"),
            min_replica_count=min_r, max_replica_count=max_r))

ep = Endpoint(
    display_name="churn-ep",
    deployed_models=[dm("a", "1", 1, 3), dm("b", "2", 1, 3)],
    traffic_split={"a": 90, "b": 10},        # keys are deployed-model ids
    dedicated_endpoint_enabled=True)         # dedicated endpoint flag; check current docs
print(Endpoint.to_json(ep, indent=None, including_default_value_fields=False))

def check_split(split, deployed_ids):
    """Traffic must name only deployed models and sum to 100 (check current docs)."""
    unknown = set(split) - set(deployed_ids)
    if unknown:
        return f"BAD unknown deployed model id(s): {sorted(unknown)}"
    if sum(split.values()) != 100:
        return f"BAD sum is {sum(split.values())}, need 100"
    return "ok"

ids = [d.id for d in ep.deployed_models]
for s in [{"a": 90, "b": 10}, {"a": 90, "b": 20}, {"a": 50, "c": 50}]:
    print(s, "->", check_split(s, ids))

res = BatchDedicatedResources(machine_spec=MachineSpec(machine_type="n1-standard-4"),
                              starting_replica_count=2, max_replica_count=4)
gcs_job = BatchPredictionJob(
    display_name="nightly-gcs", model=MODEL,
    input_config=BatchPredictionJob.InputConfig(instances_format="jsonl",
        gcs_source=GcsSource(uris=["gs://demo-bkt/in/part-*.jsonl"])),
    output_config=BatchPredictionJob.OutputConfig(predictions_format="jsonl",
        gcs_destination=GcsDestination(output_uri_prefix="gs://demo-bkt/out/")),
    dedicated_resources=res)
bq_job = BatchPredictionJob(
    display_name="nightly-bq", model=MODEL,
    input_config=BatchPredictionJob.InputConfig(instances_format="bigquery",
        bigquery_source=BigQuerySource(input_uri="bq://demo-proj.sales.to_score")),
    output_config=BatchPredictionJob.OutputConfig(predictions_format="bigquery",
        bigquery_destination=BigQueryDestination(output_uri="bq://demo-proj.sales_out")),
    dedicated_resources=res)
for j in (gcs_job, bq_job):
    print(j.display_name, "| in:", BatchPredictionJob.InputConfig.to_dict(j.input_config),
          "| out:", BatchPredictionJob.OutputConfig.to_dict(j.output_config))
print("replicas:", res.starting_replica_count, "->", res.max_replica_count)

# ai.Endpoint("projects/.../endpoints/1") fetches the resource in its constructor, so it is NOT called here.
print("SDK classes present:", ai.Endpoint.__name__, ai.BatchPredictionJob.__name__, ai.Model.__name__,
      "| Model.deploy and Model.batch_predict exist:", hasattr(ai.Model, "deploy"), hasattr(ai.Model, "batch_predict"))
```

**Output (my run):** google-cloud-aiplatform 1.165.1, Python 3.13, run with `python3 -I`, offline.
```text
google-cloud-aiplatform 1.165.1
{"displayName": "churn-ep", "deployedModels": [{"id": "a", "model": "projects/demo-proj/locations/asia-south1/models/111", "displayName": "churn-v1", "dedicatedResources": {"machineSpec": {"machineType": "n1-standard-4"}, "minReplicaCount": 1, "maxReplicaCount": 3}, "modelVersionId": "1"}, {"id": "b", "model": "projects/demo-proj/locations/asia-south1/models/111", "displayName": "churn-v2", "dedicatedResources": {"machineSpec": {"machineType": "n1-standard-4"}, "minReplicaCount": 1, "maxReplicaCount": 3}, "modelVersionId": "2"}], "trafficSplit": {"b": 10, "a": 90}, "dedicatedEndpointEnabled": true}
{'a': 90, 'b': 10} -> ok
{'a': 90, 'b': 20} -> BAD sum is 110, need 100
{'a': 50, 'c': 50} -> BAD unknown deployed model id(s): ['c']
nightly-gcs | in: {'instances_format': 'jsonl', 'gcs_source': {'uris': ['gs://demo-bkt/in/part-*.jsonl']}} | out: {'predictions_format': 'jsonl', 'gcs_destination': {'output_uri_prefix': 'gs://demo-bkt/out/'}}
nightly-bq | in: {'instances_format': 'bigquery', 'bigquery_source': {'input_uri': 'bq://demo-proj.sales.to_score'}} | out: {'predictions_format': 'bigquery', 'bigquery_destination': {'output_uri': 'bq://demo-proj.sales_out'}}
replicas: 2 -> 4
SDK classes present: Endpoint BatchPredictionJob Model | Model.deploy and Model.batch_predict exist: True True
```
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

### Q11 ⭐⭐⭐ 🟡 Model registry in each cloud: Azure ML model registry (workspace and shared registries, versions, tags, MLflow and custom model types, no built-in stage field) versus Vertex AI Model Registry (models, versions, aliases, labels, deploy and batch actions) versus MLflow registry aliases. Design a promotion convention for dev, staging and prod in each, and write a small function that validates a registry entry (name, version, alias or tag, source run, approver) and run it on good and bad examples. Part 4 and Part 7 own registry and gate basics.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs')
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
```python
"""Q11: registry entry validator + a promotion convention per cloud. Pure Python; runs in any venv."""
import re

# Convention (mine, not a vendor rule): stage lives in an alias (Vertex, MLflow) or a tag (Azure ML),
# never in the model name, and a prod entry needs an approver and a source run.
CONVENTION = {
    "azure_ml": {"stage_carrier": "tag  stage=dev|staging|prod", "immutable": "name:version", "pointer": "azureml:churn:7"},
    "vertex":   {"stage_carrier": "version alias dev|staging|prod (moves)", "immutable": "model id + version id", "pointer": "projects/P/locations/R/models/ID@prod"},
    "mlflow":   {"stage_carrier": "registered-model alias (moves)", "immutable": "name + version", "pointer": "models:/churn@prod"},
}
STAGES = {"dev", "staging", "prod"}
NAME_RE = re.compile(r"^[a-z][a-z0-9-]{2,40}$")

def validate(e):
    errs = []
    if not NAME_RE.match(str(e.get("name", ""))):
        errs.append("name must be lowercase-hyphen, no stage in it")
    elif any(s in e["name"].split("-") for s in STAGES):
        errs.append("stage word in model name (use alias/tag instead)")
    if not isinstance(e.get("version"), int) or e["version"] < 1:
        errs.append("version must be an integer >= 1")
    if e.get("stage") not in STAGES:
        errs.append("stage must be one of dev|staging|prod")
    if not e.get("source_run"):
        errs.append("source_run missing (no lineage)")
    if e.get("stage") == "prod" and not e.get("approver"):
        errs.append("prod needs an approver")
    if e.get("stage") == "prod" and e.get("approver") == e.get("registered_by"):
        errs.append("approver must differ from registered_by")
    return errs

samples = {
 "good_staging": dict(name="churn", version=7, stage="staging", source_run="run-8841", registered_by="asha"),
 "good_prod":    dict(name="churn", version=7, stage="prod", source_run="run-8841", registered_by="asha", approver="ravi"),
 "bad_prod_self_approved": dict(name="churn", version=8, stage="prod", source_run="run-9", registered_by="asha", approver="asha"),
 "bad_stage_in_name": dict(name="churn-prod", version=3, stage="prod", source_run="run-5", registered_by="asha", approver="ravi"),
 "bad_name_and_run": dict(name="Churn-Prod", version=0, stage="prod", registered_by="asha", approver="ravi"),
}
for k, v in samples.items():
    errs = validate(v)
    print(f"{k:24s}", "OK" if not errs else "FAIL " + "; ".join(errs))
```

**Output (my run):** `python3 -I`, pure Python, no cloud.
```text
good_staging             OK
good_prod                OK
bad_prod_self_approved   FAIL approver must differ from registered_by
bad_stage_in_name        FAIL stage word in model name (use alias/tag instead)
bad_name_and_run         FAIL name must be lowercase-hyphen, no stage in it; version must be an integer >= 1; source_run missing (no lineage)
```
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

### Q12 ⭐⭐⭐ 🟡 Identity on Azure ML versus Vertex AI: Azure Entra ID users, service principals, system-assigned and user-assigned managed identities, the workspace identity, compute identity, and RBAC roles on workspace and storage (for example Storage Blob Data roles) versus Google IAM principals, service accounts attached to jobs, Vertex service agents, roles on the project and bucket, and impersonation. Which identity reads data, which pulls the image, which creates the job? Write a role matrix for one training job in each cloud as YAML and validate it with pyyaml. AWS IAM depth is Part 10.
**Asked at:** Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs') | Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms
**Say this first (1 line):** On both clouds three different identities do three different jobs: one creates the job, one runs as the job and reads the data, one pulls the image, and I give each the smallest role at the smallest scope.

**Then explain:**
- **Azure side.** Entra ID gives users, service principals and managed identities. A managed identity is system-assigned (tied to the resource) or user-assigned (a standalone object you attach). The workspace has its own identity for plumbing (storage, registry, Key Vault). A compute cluster can have its own identity, and a job can run as that identity or, with user identity passthrough, as the submitting user. Access is Azure RBAC: roles like Storage Blob Data Reader on the storage scope. Check current docs for built-in role names.
- **Google side.** Principals are users, groups and service accounts. A custom training job runs as a service account you attach, otherwise a Google-managed default is used (check current docs). Vertex has service agents, Google-managed accounts that do plumbing such as image pulls. IAM roles are bound on the project, bucket or repository. The caller who attaches a service account to a job needs permission to act as it (`roles/iam.serviceAccountUser`). Impersonation uses a token-creator role so a CI identity can borrow a service account without a key.
- **Who does what.** Creates the job: the CI service principal or deployer service account. Reads data: the compute or job identity. Pulls the image: the registry-reading identity (workspace or compute identity on Azure; job service account or service agent on Google). Writes outputs: the job identity, scoped to the output container or bucket.
- **Failure modes.** Role granted to the wrong identity. Role granted at a scope that does not cover the path. New role assignment not effective yet (propagation delay). Owner or Contributor handed out "to make it work".
- **Not like for like.** Azure RBAC data-plane roles are separate from management roles; on Google a single IAM role can cover both. AWS equivalent is IAM roles, covered in Part 10.

**Example:** Azure training job: CI service principal has a workspace role to create jobs. The cluster's user-assigned identity has Storage Blob Data Reader on the input container and Storage Blob Data Contributor on the output container. Google: the deployer service account has `roles/aiplatform.user` and act-as on the job service account; the job service account has `objectViewer` on the input bucket and `objectAdmin` on the output bucket.

**Code:** the role matrix and a validator. Role names are examples (check current docs for exact built-in roles).
```yaml
# One training job per cloud. Role names are examples; check current docs for exact built-in roles.
azure_ml:
  job_creator:        {identity: "service principal (CI) or user, Entra ID", role: "AzureML Data Scientist", scope: workspace}
  job_runs_as:        {identity: "compute cluster user-assigned managed identity", role: "Storage Blob Data Reader", scope: "storage account or container"}
  image_pull:         {identity: "workspace or compute managed identity", role: "AcrPull", scope: container registry}
  output_write:       {identity: "compute cluster user-assigned managed identity", role: "Storage Blob Data Contributor", scope: "output container"}
google_vertex:
  job_creator:        {identity: "deployer service account", role: "roles/aiplatform.user", scope: project, extra: "roles/iam.serviceAccountUser on the job service account"}
  job_runs_as:        {identity: "job service account (custom)", role: "roles/storage.objectViewer", scope: "input bucket"}
  image_pull:         {identity: "job service account or Vertex service agent", role: "roles/artifactregistry.reader", scope: "repository"}
  output_write:       {identity: "job service account (custom)", role: "roles/storage.objectAdmin", scope: "output bucket"}
```
```python
import yaml, sys
m = yaml.safe_load(open(sys.argv[1]))
BROAD = {"Owner", "Contributor", "roles/owner", "roles/editor"}
need = {"job_creator", "job_runs_as", "image_pull", "output_write"}
for cloud, rows in m.items():
    assert set(rows) == need, (cloud, set(rows) ^ need)
    for k, r in rows.items():
        assert {"identity", "role", "scope"} <= set(r), (cloud, k)
        assert r["role"] not in BROAD, (cloud, k, "too broad", r["role"])
    # the identity that reads data must not be the human/CI creator
    assert rows["job_creator"]["identity"] != rows["job_runs_as"]["identity"], cloud
    print(cloud, "ok:", len(rows), "duties,",
          "creator != runtime identity:", rows["job_creator"]["identity"] != rows["job_runs_as"]["identity"])
# negative test: a lazy matrix must fail
bad = {"azure_ml": {k: {"identity": "me", "role": "Contributor", "scope": "subscription"} for k in need}}
try:
    for k, r in bad["azure_ml"].items():
        assert r["role"] not in BROAD, f"{k}: broad role {r['role']}"
    assert bad["azure_ml"]["job_creator"]["identity"] != bad["azure_ml"]["job_runs_as"]["identity"], "creator == runtime identity"
except AssertionError as e:
    print("lazy matrix rejected:", e)
```

**Output (my run):** `python3 -I q12_check.py q12_role_matrix.yaml`, pyyaml only.
```text
azure_ml ok: 4 duties, creator != runtime identity: True
google_vertex ok: 4 duties, creator != runtime identity: True
lazy matrix rejected: job_creator: broad role Contributor
```
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

### Q13 ⭐⭐⭐ 🟡 Experiment tracking portability: the same training script logging to MLflow with the tracking URI pointing at a local database, at Azure ML (azureml tracking URI with the azureml-mlflow plugin) and next to Vertex AI Experiments. What stays the same, what changes (URI, auth, artifact store), and what you must not hard-code. Run the script for real against a local sqlite MLflow backend, show that the azureml URI scheme is accepted by the client, and say that no call to a real workspace was made. Part 4 owns MLflow basics.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Cross-cloud comparison articles (TechTarget 'Compare Google Vertex AI vs Amazon SageMaker vs Azure ML', cloudoptimo, gmicloud, superwise, a redresscompliance licensing piece; search snippets only, not opened; several authors sell competing services or advice, so conclusions treated as opinion) | Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs')
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
```python
"""Same training script, tracking target chosen by env var. Only the local sqlite target is actually exercised."""
import os, sys, tempfile, warnings
warnings.filterwarnings("ignore")
os.environ.setdefault("MLFLOW_DISABLE_TELEMETRY", "true")
import mlflow

def train(lr):                      # stand-in for real training
    return {"auc": round(0.80 + 0.5 * lr, 3), "loss": round(0.4 - lr, 3)}

def main():
    uri = os.environ["MLFLOW_TRACKING_URI"]      # never hard-code; CI/job injects it
    mlflow.set_tracking_uri(uri)
    print("mlflow", mlflow.__version__, "| tracking uri scheme:", uri.split(":", 1)[0])
    if uri.startswith("azureml"):
        print("azureml URI accepted by the client; NO experiment/run call made (would reach management.azure.com)")
        return
    mlflow.set_experiment("churn-demo")
    with mlflow.start_run(run_name="lr-0.1") as r:
        mlflow.log_param("lr", 0.1)
        for k, v in train(0.1).items():
            mlflow.log_metric(k, v)
        mlflow.set_tag("git_sha", "abc1234")
    run = mlflow.get_run(r.info.run_id)
    print("params:", run.data.params, "| metrics:", run.data.metrics, "| tags(git_sha):", run.data.tags["git_sha"])

if __name__ == "__main__":
    main()
```
```bash
# local: sqlite backend in a temp dir
MLFLOW_TRACKING_URI="sqlite:///$PWD/ml.db" python3 -I q13_train_portable.py
# Azure ML URI (fake subscription id): only proves the client takes the scheme; the script returns before any call
MLFLOW_TRACKING_URI="azureml://centralindia.api.azureml.ms/mlflow/v1.0/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg/providers/Microsoft.MachineLearningServices/workspaces/ws" python3 -I q13_train_portable.py
```

**Output (my run):** mlflow 3.17.2 with azureml-mlflow 1.60.0 installed, Python 3.13 (one MLflow hint log line removed).
```text
2026/10/26 18:14:09 INFO mlflow.store.db.utils: Creating initial MLflow database tables...
2026/10/26 18:14:09 INFO mlflow.store.db.utils: Updating database tables
2026/10/26 18:14:11 INFO mlflow.tracking.fluent: Experiment with name 'churn-demo' does not exist. Creating a new experiment.
mlflow 3.17.2 | tracking uri scheme: sqlite
params: {'lr': '0.1'} | metrics: {'auc': 0.85, 'loss': 0.3} | tags(git_sha): abc1234
mlflow 3.17.2 | tracking uri scheme: azureml
azureml URI accepted by the client; NO experiment/run call made (would reach management.azure.com)
```
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

### Q14 ⭐⭐⭐ 🟡 Choosing a platform: an Indian bank-owned GCC on Microsoft 365 and Entra, a consumer-internet product company with its data in BigQuery, and a services firm serving clients on all three clouds each ask which managed ML platform to standardise on. Give the decision criteria (data gravity, identity, skills, compliance, existing contracts, GPU availability in the Region, exit cost), the recommendation for each, and what you would pilot first. No prices; hedge availability as 'check current docs'. Encode the criteria as a weighted scoring function, run it, and say why the weights are the real argument.
**Asked at:** Cross-cloud comparison articles (TechTarget 'Compare Google Vertex AI vs Amazon SageMaker vs Azure ML', cloudoptimo, gmicloud, superwise, a redresscompliance licensing piece; search snippets only, not opened; several authors sell competing services or advice, so conclusions treated as opinion) | Job-posting and community patterns for Azure-heavy IT-services firms and GCCs (Azure ML plus Azure DevOps) versus GCP-using product companies (Vertex plus BigQuery); inferred from search snippets about ecosystem fit, not from a verified company report | Certification-style question families (Microsoft DP-100 study guide and its replacement AI-300 as reported by third-party sites, Google Cloud Professional Machine Learning Engineer exam-prep listings; mentioned as a source type only, no exam questions reproduced; skills lists conflicted between sources, so verify on the vendor pages)
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
```python
"""Weighted scoring of Azure ML / Vertex AI / SageMaker for three org profiles.
Scores (0-5) and weights are MY judgement inputs for the interview, not measurements. Edit and rerun."""
CRITERIA = ["data_gravity", "identity", "skills", "compliance", "contracts", "gpu_in_region", "exit_cost"]
# 0-5, higher is better for that org. exit_cost: 5 = easy to leave.
SCORES = {
 "bank_gcc_m365": {"azure_ml": [3, 5, 4, 5, 5, 3, 3], "vertex": [2, 2, 2, 3, 2, 3, 3], "sagemaker": [2, 2, 3, 4, 3, 3, 3]},
 "product_bigquery": {"azure_ml": [2, 2, 2, 3, 2, 3, 3], "vertex": [5, 4, 4, 3, 4, 3, 3], "sagemaker": [2, 3, 3, 3, 3, 3, 3]},
 "services_all_clouds": {"azure_ml": [3, 4, 3, 4, 3, 3, 3], "vertex": [4, 3, 3, 3, 3, 3, 3], "sagemaker": [3, 3, 4, 3, 3, 3, 3]},
}
WEIGHTS = {
 "bank_gcc_m365":       [2, 4, 2, 5, 3, 2, 1],
 "product_bigquery":    [5, 2, 3, 2, 2, 3, 2],
 "services_all_clouds": [1, 1, 2, 2, 1, 2, 5],   # exit cost and client choice dominate
}
def score(profile, weights=None):
    w = weights or WEIGHTS[profile]
    assert len(w) == len(CRITERIA)
    tot = sum(w)
    return {p: round(sum(a * b for a, b in zip(w, s)) / tot, 2) for p, s in SCORES[profile].items()}

for prof in SCORES:
    r = score(prof)
    print(f"{prof:22s}", r, "->", max(r, key=r.get) if len(set(r.values())) > 1 else "tie: decide on client")

# Sensitivity: SAME scores for the services firm, two clients with different weights.
# data_gravity, identity, skills, compliance, contracts, gpu_in_region, exit_cost
client_a = [1, 5, 1, 4, 1, 1, 1]   # identity + compliance heavy (Entra shop)
client_b = [5, 1, 1, 1, 1, 1, 1]   # warehouse-heavy
print("services, client A weights:", score("services_all_clouds", client_a))
print("services, client B weights:", score("services_all_clouds", client_b))
# Hand check for bank/azure_ml: (2*3+4*5+2*4+5*5+3*5+2*3+1*3)/19 = 83/19
print("hand check:", round((2*3 + 4*5 + 2*4 + 5*5 + 3*5 + 2*3 + 1*3) / 19, 2))
```

**Output (my run):** `python3 -I`, pure Python.
```text
bank_gcc_m365          {'azure_ml': 4.37, 'vertex': 2.42, 'sagemaker': 2.95} -> azure_ml
product_bigquery       {'azure_ml': 2.37, 'vertex': 3.89, 'sagemaker': 2.74} -> vertex
services_all_clouds    {'azure_ml': 3.21, 'vertex': 3.07, 'sagemaker': 3.14} -> azure_ml
services, client A weights: {'azure_ml': 3.64, 'vertex': 3.07, 'sagemaker': 3.07}
services, client B weights: {'azure_ml': 3.18, 'vertex': 3.45, 'sagemaker': 3.09}
hand check: 4.37
```
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

### Q15 ⭐⭐ 🟢 Azure ML datastores and data assets: datastore types (Blob, Data Lake, Files), identity-based versus credential-based access, the azureml:// path forms, data asset types uri_file, uri_folder and mltable, versioning of assets, and how a job gets an input mounted or downloaded. Run an Azurite blob emulator with its documented public development key, upload a file, build a Data entity pointing at it, and say clearly that Azurite is not Azure ML or Entra auth.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | Job-posting and community patterns for Azure-heavy IT-services firms and GCCs (Azure ML plus Azure DevOps) versus GCP-using product companies (Vertex plus BigQuery); inferred from search snippets about ecosystem fit, not from a verified company report
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
```python
"""Azurite blob emulator + offline Azure ML Datastore/Data entities. Storage API shape only: no Entra, no Azure ML."""
import sys, warnings; warnings.filterwarnings("ignore")
from azure.storage.blob import BlobServiceClient
from azure.ai.ml import Input
from azure.ai.ml.entities import Data, AzureBlobDatastore
import azure.ai.ml as m

PORT = sys.argv[1]
# Documented PUBLIC Azurite dev account; not a secret.
KEY = "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=="
cs = (f"DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey={KEY};"
      f"BlobEndpoint=http://127.0.0.1:{PORT}/devstoreaccount1;")
bsc = BlobServiceClient.from_connection_string(cs)
c = bsc.create_container("train-data")
c.upload_blob("churn/2026-10/part-0.csv", b"id,y\n1,0\n2,1\n", overwrite=True)
print("azure-ai-ml", m.__version__, "| blobs:", [b.name for b in c.list_blobs()])
print("round trip:", c.get_blob_client("churn/2026-10/part-0.csv").download_blob().readall())

# Offline entities: nothing is registered anywhere.
ds = AzureBlobDatastore(name="churn_blob", account_name="devstoreaccount1", container_name="train-data")
print("datastore:", ds.name, ds.type, ds.account_name, ds.container_name, "| credentials:", type(ds.credentials).__name__)
folder = "azureml://datastores/churn_blob/paths/churn/2026-10/"
d1 = Data(name="churn-raw", version="1", type="uri_folder", path=folder)
d2 = Data(name="churn-raw", version="2", type="uri_file", path=folder + "part-0.csv")
for d in (d1, d2):
    print("Data", d.name, "v" + d.version, d.type, d.path)
for mode in ("ro_mount", "download"):
    i = Input(type="uri_folder", path="azureml:churn-raw:1", mode=mode)
    print("Input mode:", i.mode, "->", i.path)
```
```bash
azurite-blob --blobPort 8611 --location /tmp/claude-0/b11_q10_18/q15 --skipApiVersionCheck --silent &
python3 -I q15_azurite_data.py 8611
kill %1        # stop the emulator
```

**Output (my run):** azurite 3.37.0 (npm), azure-ai-ml 1.35.2, azure-storage-blob 12.19.0, Python 3.13. Azurite stopped afterwards (port 8611 closed).
```text
azure-ai-ml 1.35.2 | blobs: ['churn/2026-10/part-0.csv']
round trip: b'id,y\n1,0\n2,1\n'
datastore: churn_blob DatastoreType.AZURE_BLOB devstoreaccount1 train-data | credentials: NoneCredentialConfiguration
Data churn-raw v1 uri_folder azureml://datastores/churn_blob/paths/churn/2026-10/
Data churn-raw v2 uri_file azureml://datastores/churn_blob/paths/churn/2026-10/part-0.csv
Input mode: ro_mount -> azureml:churn-raw:1
Input mode: download -> azureml:churn-raw:1
```
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

### Q16 ⭐⭐ 🟢 Azure ML environments: curated versus custom, base image plus conda file versus a Dockerfile build context, versioning and image build caching, and why an environment is part of reproducibility. Write an environment YAML and conda file, load them with the SDK, parse the conda file with pyyaml and fail on unpinned packages. Compare with a Vertex custom container in Artifact Registry. Part 2 owns Docker.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs')
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
```yaml
# ---- file: env.yml (Environment from a base image + conda file)
$schema: https://azuremlschemas.azureedge.net/latest/environment.schema.json
name: churn-train
version: "3"
image: mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04
conda_file: conda.yml
description: base image + conda file; image is built and cached by the service on first use
# ---- file: docker_env.yml (Environment from a build context)
name: churn-docker
version: "1"
build:
  path: ./docker-context
  dockerfile_path: Dockerfile
# ---- file: conda.yml (unpinned pandas: the check fails)
name: churn
channels: [conda-forge]
dependencies:
  - python=3.11
  - pip=24.0
  - pip:
      - scikit-learn==1.5.2
      - mlflow==2.17.0
      - pandas
# ---- file: conda_good.yml (all pinned)
name: churn
channels: [conda-forge]
dependencies:
  - python=3.11
  - pip=24.0
  - pip:
      - scikit-learn==1.5.2
      - mlflow==2.17.0
      - pandas==2.2.3
# ---- docker-context/Dockerfile
# FROM python:3.11-slim
# RUN pip install --no-cache-dir scikit-learn==1.5.2
```
```python
import sys, re, warnings, yaml; warnings.filterwarnings("ignore")
from azure.ai.ml import load_environment
import azure.ai.ml as m
print("azure-ai-ml", m.__version__)
e = load_environment("q16/env.yml")
print("loaded:", e.name, e.version, "| image:", e.image, "| conda_file type:", type(e.conda_file).__name__)
d = load_environment("q16/docker_env.yml")
print("docker env:", d.name, "| build context:", d.build.path.name if hasattr(d.build.path, "name") else d.build.path, "| image:", d.image)

PIN = re.compile(r"^[A-Za-z0-9_.\-]+(\[[^\]]+\])?==[^=\s]+$")     # name==version
def unpinned(conda_path):
    c = yaml.safe_load(open(conda_path)); bad = []
    for dep in c["dependencies"]:
        if isinstance(dep, str):
            if not re.search(r"=", dep): bad.append(dep)              # conda: need name=ver
        else:
            for p in dep["pip"]:
                if not PIN.match(p): bad.append("pip:" + p)
    return bad
files = sys.argv[1:] or ["q16/conda.yml", "q16/conda_good.yml"]
rc = 0
for f in files:
    b = unpinned(f)
    print(f, "->", "OK all pinned" if not b else f"FAIL unpinned: {b}")
    rc |= bool(b)
sys.exit(rc)      # non-zero fails the CI step
```

**Output (my run):** azure-ai-ml 1.35.2, Python 3.13.
```text
azure-ai-ml 1.35.2
loaded: churn-train 3 | image: mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04 | conda_file type: dict
docker env: churn-docker | build context: ./docker-context | image: None
q16/conda.yml -> FAIL unpinned: ['pip:pandas']
q16/conda_good.yml -> OK all pinned
exit=1
$ python3 -I q16_env_check.py q16/conda_good.yml
q16/conda_good.yml -> OK all pinned
exit=0
```
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

### Q17 ⭐⭐ 🟡 Azure ML batch endpoints and batch deployments versus Vertex batch prediction: inputs from a data asset or folder, the scoring script or MLflow no-code model, mini-batch size, output action (append or summary), compute cluster, invoke returning a job, and no traffic split on batch (default deployment is switched instead). Build a BatchEndpoint offline and write the invoke-and-collect plan for a nightly scoring of 2 million rows without running it. Part 6 owns batch versus real-time reasoning.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs')
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
```python
"""Azure ML BatchEndpoint/BatchDeployment built offline + a nightly invoke plan with hand-checkable arithmetic."""
import math, warnings; warnings.filterwarnings("ignore")
import azure.ai.ml as m
from azure.ai.ml.entities import BatchEndpoint, ModelBatchDeployment, ModelBatchDeploymentSettings, BatchRetrySettings, Data
from azure.ai.ml.constants import BatchDeploymentOutputAction
print("azure-ai-ml", m.__version__)

ep = BatchEndpoint(name="churn-batch", description="nightly scoring")
dep = ModelBatchDeployment(
    name="v1", endpoint_name="churn-batch", model="azureml:churn:7", compute="cpu-cluster",
    settings=ModelBatchDeploymentSettings(
        mini_batch_size=1, instance_count=4, max_concurrency_per_instance=2,
        output_action=BatchDeploymentOutputAction.APPEND_ROW, output_file_name="predictions.csv",
        retry_settings=BatchRetrySettings(max_retries=3, timeout=300), error_threshold=-1, logging_level="info"))
s = dep.settings
print("endpoint:", ep.name, "| deployment:", dep.name, "->", dep.endpoint_name)
print("settings:", dict(mini_batch_size=s.mini_batch_size, instance_count=s.instance_count,
      max_concurrency=s.max_concurrency_per_instance, output_action=s.output_action,
      retries=s.retry_settings.max_retries, timeout_s=s.retry_settings.timeout))
# NOTE: for an MLflow model the scoring script is not needed (no-code); for a custom model you add code + scoring_script.

ROWS = 2_000_000
# Plan. Assumption (check current docs): mini_batch_size counts FILES for file-based input, so 1 means one file per mini-batch.
# The input is 200 part-files of 10,000 rows each.
FILE_ROWS, FILES_PER_MB = 10_000, s.mini_batch_size
files = math.ceil(ROWS / FILE_ROWS)
mini_batches = math.ceil(files / FILES_PER_MB)
workers = s.instance_count * s.max_concurrency_per_instance
waves = math.ceil(mini_batches / workers)
print(f"files={files} mini_batches={mini_batches} parallel_workers={workers} waves={waves}")
plan = [
 "1. ensure input data asset (uri_folder of part files) is registered/versioned: churn-input:<date>",
 "2. az ml batch-endpoint invoke --name churn-batch --deployment-name v1 --input azureml:churn-input:<date>   (returns a job)",
 "3. poll the returned job until Completed (or Failed/Canceled); alert on Failed",
 "4. read predictions.csv from the job's output location; row count must equal 2,000,000 (APPEND_ROW)",
 "5. publish only after the count check; keep the job name in the run log",
 "6. rollback = set default deployment back (no traffic split on batch)",
]
print("\n".join(plan))
```

**Output (my run):** azure-ai-ml 1.35.2, Python 3.13.
```text
azure-ai-ml 1.35.2
endpoint: churn-batch | deployment: v1 -> churn-batch
settings: {'mini_batch_size': 1, 'instance_count': 4, 'max_concurrency': 2, 'output_action': 'append_row', 'retries': 3, 'timeout_s': 300}
files=200 mini_batches=200 parallel_workers=8 waves=25
1. ensure input data asset (uri_folder of part files) is registered/versioned: churn-input:<date>
2. az ml batch-endpoint invoke --name churn-batch --deployment-name v1 --input azureml:churn-input:<date>   (returns a job)
3. poll the returned job until Completed (or Failed/Canceled); alert on Failed
4. read predictions.csv from the job's output location; row count must equal 2,000,000 (APPEND_ROW)
5. publish only after the count check; keep the job name in the run log
6. rollback = set default deployment back (no traffic split on batch)
```
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

### Q18 ⭐⭐ 🟡 Developer environments: Vertex AI Workbench and Colab Enterprise versus Azure ML compute instances and notebooks: who owns the VM, idle shutdown, attached service account or managed identity, network and no-public-IP options, mounting data, and keeping notebook work reproducible and out of production. A team lead asks how to stop people leaving 8-GPU notebooks running. Give the controls in each cloud and a lint function that flags a notebook-instance config (no idle shutdown, public IP, broad identity) run on sample YAML. Cost depth is Part 12.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Job-posting and community patterns for Azure-heavy IT-services firms and GCCs (Azure ML plus Azure DevOps) versus GCP-using product companies (Vertex plus BigQuery); inferred from search snippets about ecosystem fit, not from a verified company report | Certification-style question families (Microsoft DP-100 study guide and its replacement AI-300 as reported by third-party sites, Google Cloud Professional Machine Learning Engineer exam-prep listings; mentioned as a source type only, no exam questions reproduced; skills lists conflicted between sources, so verify on the vendor pages)
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
```yaml
name: ml-dev-alice
cloud: azure
machine: Standard_NC24ads_A100_v4
gpu_count: 1
idle_shutdown_minutes: 60
public_ip: false
ssh_public_access: false
identity: {principal: "uami-ml-notebooks", roles: ["Storage Blob Data Reader"]}
owner_label: alice
schedule_stop: "20:00"
---
name: gpu-bob-forever
cloud: azure
machine: Standard_ND96asr_v4
gpu_count: 8
public_ip: true
ssh_public_access: true
identity: {roles: ["Contributor"]}
---
name: wb-carol
cloud: gcp
machine: a2-highgpu-8g
gpu_count: 8
idle_shutdown_minutes: 180
public_ip: false
identity: {principal: "nb-sa@demo-proj.iam.gserviceaccount.com", roles: ["roles/editor"]}
owner_label: carol
---
name: wb-dev-ok
cloud: gcp
machine: n1-standard-8
gpu_count: 1
idle_shutdown_minutes: 90
public_ip: false
identity: {principal: "nb-sa@demo-proj.iam.gserviceaccount.com", roles: ["roles/storage.objectViewer"]}
owner_label: dev
schedule_stop: "21:00"
```
```python
"""Lint a notebook-instance config. The YAML shape is MY simplified schema, not an Azure or Google file format.
Azure side maps to ComputeInstance fields; Vertex side maps to Workbench instance settings (check current docs)."""
import sys, yaml
BROAD = {"Owner", "Contributor", "roles/owner", "roles/editor"}
GPU_HINT = ("nc", "nd", "nv", "a100", "t4", "v100", "h100", "l4", "a2-", "g2-", "a3-")

def lint(c):
    f = []
    idle = c.get("idle_shutdown_minutes")
    if not idle:
        f.append("no idle shutdown")
    elif idle > 120:
        f.append(f"idle shutdown {idle} min is long (policy max 120)")
    if c.get("public_ip", False):
        f.append("public IP enabled")
    if c.get("ssh_public_access", False):
        f.append("SSH open to internet")
    ident = c.get("identity", {})
    if not ident.get("principal"):
        f.append("no dedicated identity (falls back to default/user)")
    for r in ident.get("roles", []):
        if r in BROAD:
            f.append(f"broad role {r}")
    shape = str(c.get("machine", "")).lower()
    if any(h in shape for h in GPU_HINT) and c.get("gpu_count", 0) > 1 and c.get("schedule_stop") is None:
        f.append(f"{c['gpu_count']}-GPU machine with no scheduled stop")
    if not c.get("owner_label"):
        f.append("no owner label (cannot tell whose it is)")
    return f

try:   # optional: the real Azure entity carries the same knobs (offline object, nothing created)
    import warnings; warnings.filterwarnings("ignore")
    from azure.ai.ml.entities import ComputeInstance
    ci = ComputeInstance(name="ci-alice", size="Standard_DS3_v2", idle_time_before_shutdown_minutes=60,
                         enable_node_public_ip=False, ssh_public_access_enabled=False)
    print("ComputeInstance:", ci.name, ci.size, "idle_min:", ci.idle_time_before_shutdown_minutes,
          "node_public_ip:", ci.enable_node_public_ip, "ssh_public:", ci.ssh_public_access_enabled)
except ImportError:
    print("azure-ai-ml not installed here: ComputeInstance demo skipped")
bad_rc = 0
for doc in yaml.safe_load_all(open(sys.argv[1])):
    out = lint(doc)
    print(f"{doc['name']:22s} {doc['cloud']:7s}", "PASS" if not out else "FAIL: " + "; ".join(out))
    bad_rc |= bool(out)
sys.exit(bad_rc)
```

**Output (my run):** run in the azure-ai-ml 1.35.2 venv with `python3 -I`; the same script under plain Python skips the `ComputeInstance` line. Exit code 1 because two samples fail.
```text
ComputeInstance: ci-alice Standard_DS3_v2 idle_min: 60 node_public_ip: False ssh_public: False
ml-dev-alice           azure   PASS
gpu-bob-forever        azure   FAIL: no idle shutdown; public IP enabled; SSH open to internet; no dedicated identity (falls back to default/user); broad role Contributor; 8-GPU machine with no scheduled stop; no owner label (cannot tell whose it is)
wb-carol               gcp     FAIL: idle shutdown 180 min is long (policy max 120); broad role roles/editor; 8-GPU machine with no scheduled stop
wb-dev-ok              gcp     PASS
exit=1
```
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
