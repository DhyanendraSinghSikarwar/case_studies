### Q1 ⭐⭐⭐ 🟢 Service-mapping question that opens most cross-cloud rounds: map the ML lifecycle pieces across Azure Machine Learning, Google Vertex AI and (by concept only, Part 10 owns depth) AWS SageMaker: workspace or project, notebooks, compute, data access, environments, training jobs, pipelines, hyperparameter tuning, AutoML, model registry, real-time and batch inference, monitoring, feature store, experiment tracking. Say where the mapping is not one-to-one. Write the table as YAML, load it with pyyaml and assert every concept has an entry for all three clouds.
**Asked at:** Cross-cloud comparison articles (TechTarget 'Compare Google Vertex AI vs Amazon SageMaker vs Azure ML', cloudoptimo, gmicloud, superwise, a redresscompliance licensing piece; search snippets only, not opened; several authors sell competing services or advice, so conclusions treated as opinion) | Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Certification-style question families (Microsoft DP-100 study guide and its replacement AI-300 as reported by third-party sites, Google Cloud Professional Machine Learning Engineer exam-prep listings; mentioned as a source type only, no exam questions reproduced; skills lists conflicted between sources, so verify on the vendor pages)
**Say this first (1 line):** The ideas map almost one to one across Azure ML, Vertex AI and SageMaker, but the containers differ: Azure has a workspace that owns assets, Vertex has a project plus region and resources hang off it, and the names for compute, data and environments do not line up cleanly.

**Then explain:**
- Start from the lifecycle, not the product names: data, environment, train, tune, register, deploy, monitor. Every cloud has a managed piece for each step. Say the table, then say where it bends.
- Where it is not one to one: (1) Azure ML has a workspace object that owns data, models, environments and endpoints; Vertex has no workspace, the project and region are the boundary; (2) Azure has standing compute objects (cluster, instance), Vertex training takes a machine spec per job; (3) Azure has datastores and data assets, Vertex mostly takes Cloud Storage or BigQuery paths; (4) an Azure environment is a versioned asset, Vertex and SageMaker use a container image.
- Names that sound alike but are not the same: "Pipelines" on Vertex is a KFP spec; on Azure ML it is a pipeline job of components in Azure's own YAML. "Model Monitoring" differs in what it watches and how you configure it.
- Failure mode: answering with a marketing table and no caveats. Interviewers then ask "so what breaks if I move from one to the other?" and the honest answer is the SDK objects, registry metadata and IAM, not the model file.
- SageMaker is by concept only here. Part 10 owns its depth. Cells marked "check current docs" in the table may have changed; product names move often.

**Example:** "Train, then deploy". Azure: command job on a compute cluster, model asset registered, managed online endpoint with a deployment. Vertex: CustomJob with a machine spec, Model uploaded to Model Registry, Endpoint with a deployed model. SageMaker: TrainingJob, model package, real-time endpoint.

**Code:** the table is YAML inside Python. It is loaded and asserted: every concept has a non-empty entry for all three clouds, and a broken copy is rejected. The mapping content is my own summary from general knowledge, not checked against live docs.
```python
# q01.py
import yaml
TABLE = """
workspace_or_project:
  azure_ml: Workspace (inside a resource group and subscription)
  vertex_ai: Google Cloud project plus a region (no workspace object)
  sagemaker: AWS account plus Region; SageMaker Domain for Studio users
notebooks:
  azure_ml: Compute instance with Jupyter/VS Code
  vertex_ai: Workbench instances and Colab Enterprise
  sagemaker: Studio notebooks / notebook instances
compute:
  azure_ml: Compute cluster (AmlCompute), serverless compute, attached Kubernetes
  vertex_ai: Machine specs inside each job (no standing cluster object for training)
  sagemaker: Instance type and count inside each training job
data_access:
  azure_ml: Datastores and data assets (uri_file, uri_folder, mltable)
  vertex_ai: Cloud Storage paths, BigQuery tables, managed datasets
  sagemaker: S3 URIs as channels
environments:
  azure_ml: Environment asset (image plus conda or Dockerfile), versioned
  vertex_ai: Prebuilt or custom container in Artifact Registry
  sagemaker: Prebuilt or custom container in ECR
training_jobs:
  azure_ml: command job
  vertex_ai: CustomJob / CustomTrainingJob
  sagemaker: TrainingJob
pipelines:
  azure_ml: Pipeline job made of components
  vertex_ai: Vertex AI Pipelines (KFP v2 spec)
  sagemaker: SageMaker Pipelines
hyperparameter_tuning:
  azure_ml: sweep job
  vertex_ai: HyperparameterTuningJob (Vizier)
  sagemaker: Automatic Model Tuning job
automl:
  azure_ml: Automated ML jobs (automl.classification etc.)
  vertex_ai: Vertex AI AutoML training
  sagemaker: Autopilot / Canvas
model_registry:
  azure_ml: Model asset in workspace or shared registry
  vertex_ai: Model Registry (versions and aliases)
  sagemaker: Model Registry (model package groups)
realtime_inference:
  azure_ml: Managed online endpoint plus deployments
  vertex_ai: Endpoint plus deployed models
  sagemaker: Real-time endpoint
batch_inference:
  azure_ml: Batch endpoint plus batch deployments
  vertex_ai: BatchPredictionJob
  sagemaker: Batch Transform job
monitoring:
  azure_ml: Model monitoring (signals and schedules)
  vertex_ai: Model Monitoring
  sagemaker: Model Monitor
feature_store:
  azure_ml: Managed feature store (check current docs)
  vertex_ai: Vertex AI Feature Store (BigQuery based; legacy store deprecated)
  sagemaker: SageMaker Feature Store
experiment_tracking:
  azure_ml: Jobs and runs with MLflow tracking
  vertex_ai: Vertex AI Experiments (and ML Metadata)
  sagemaker: SageMaker Experiments or managed MLflow
"""
t = yaml.safe_load(TABLE)
CLOUDS = {"azure_ml", "vertex_ai", "sagemaker"}
for concept, row in t.items():
    assert set(row) == CLOUDS, (concept, set(row) ^ CLOUDS)
    assert all(isinstance(v, str) and v.strip() for v in row.values()), concept
print("concepts:", len(t), "all have", sorted(CLOUDS))
# one-to-one check: where do the three clouds NOT line up as a single named object?
NOT_ONE_TO_ONE = ["workspace_or_project", "compute", "data_access", "environments"]
for c in NOT_ONE_TO_ONE:
    print(f"{c:22} azure={t[c]['azure_ml']!r:.45}  vertex={t[c]['vertex_ai']!r:.45}")
# negative test: a missing cell must fail
broken = yaml.safe_load(TABLE); del broken["monitoring"]["vertex_ai"]
try:
    for concept, row in broken.items():
        assert set(row) == CLOUDS, (concept, sorted(CLOUDS - set(row)))
except AssertionError as e:
    print("broken table rejected:", e)
```

**Output (my run):** (azure-ai-ml venv, Python 3.13; pyyaml only; no cloud call.)
```
concepts: 15 all have ['azure_ml', 'sagemaker', 'vertex_ai']
workspace_or_project   azure='Workspace (inside a resource group and subsc  vertex='Google Cloud project plus a region (no works
compute                azure='Compute cluster (AmlCompute), serverless com  vertex='Machine specs inside each job (no standing c
data_access            azure='Datastores and data assets (uri_file, uri_fo  vertex='Cloud Storage paths, BigQuery tables, manage
environments           azure='Environment asset (image plus conda or Docke  vertex='Prebuilt or custom container in Artifact Reg
broken table rejected: ('monitoring', ['vertex_ai'])
```
Real services, quotas, Regions and product names were not executed; check current docs for the cells marked so.

**Follow-ups:**
1. *Which cell is least stable?* Feature store and monitoring: product designs and names have changed on more than one cloud, check current docs.
2. *Is a registry the same everywhere?* Same job, different fields: Azure has versions and tags, Vertex has versions and aliases, SageMaker has model package groups.
3. *Why show YAML?* A table you can load and assert stays complete when someone edits it.

**Common mistakes:**
- Saying "Vertex is the same as SageMaker" with no caveats.
- Forgetting that a project plus region is the Vertex boundary.
- Quoting price or quota numbers from memory.

### Q2 ⭐⭐⭐ 🟢 Azure Machine Learning workspace anatomy: what a workspace is, the resources around it (storage account, Key Vault, container registry, Application Insights), the resource group and subscription above it, workspace-level assets (data, environments, models, components, endpoints, compute), and how that differs from Vertex AI where the Google Cloud project plus region is the boundary. Build a Workspace entity with the Azure SDK v2 offline (no workspace exists, nothing is created) and say what the MLClient needs to talk to a real one.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs')
**Say this first (1 line):** An Azure ML workspace is the top-level place that owns your ML assets and points at a storage account, Key Vault, container registry and Application Insights; Vertex has no such object, a Google Cloud project plus a region is the boundary.

**Then explain:**
- Hierarchy: subscription, then resource group, then workspace. The workspace holds data assets, environments, models, components, endpoints and compute. RBAC and network settings can be applied at the workspace.
- Companion resources: a storage account (default datastore and job artifacts), Key Vault (secrets), container registry (built environment images), Application Insights (logs and telemetry). Whether they are created for you or you bring your own depends on how you create the workspace; check current docs.
- Vertex difference: a Google Cloud project holds resources with a regional location (jobs, models, endpoints). You pick the region at `aiplatform.init`. There is no workspace to create; you enable the API in the project.
- What an MLClient needs: a credential, subscription id, resource group and workspace name. Without a credential it fails at once; with `DefaultAzureCredential` it still fails when it has nothing to log in with.
- Failure modes: assuming creating the entity creates Azure resources (it does not), forgetting the workspace region is a data-residency choice, public access left on, and mixing up which resource group holds the companion resources.

**Example:** Dev and prod are two workspaces (or two subscriptions). Model assets move between them via a shared registry or a rebuild from the same code. On Vertex you would normally use two projects instead.

**Code:** the entity below is built offline. It has no network call. A fake all-zero subscription id is used.
```python
# q02.py
import warnings; warnings.filterwarnings("ignore")
import azure.ai.ml as m
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace
from azure.identity import DefaultAzureCredential
print("azure-ai-ml", m.__version__)

SUB = "00000000-0000-0000-0000-000000000000"   # fake subscription id
RG = "rg-ml-dev"
ws = Workspace(
    name="mlw-dev-cin",
    location="centralindia",
    display_name="ML dev workspace",
    description="offline entity only; nothing created",
    public_network_access="Disabled",
    tags={"owner": "ml-platform", "env": "dev"},
)
print("entity:", ws.name, ws.location, "public_network_access =", ws.public_network_access)
# Companion resources are NOT created by building the entity; they are None until you set them
for k in ("storage_account", "key_vault", "container_registry", "application_insights"):
    print(f"  {k:22} ->", getattr(ws, k))
# What the workspace asset ID of a real one looks like (built by hand, as a string)
print("ARM id shape:", f"/subscriptions/{SUB}/resourceGroups/{RG}/providers/Microsoft.MachineLearningServices/workspaces/{ws.name}")

# MLClient needs 4 things: a credential, subscription, resource group, workspace name
try:
    MLClient(credential=None, subscription_id=SUB, resource_group_name=RG, workspace_name=ws.name)
except Exception as e:
    print("MLClient(credential=None):", type(e).__name__, "-", str(e)[:110])
# DefaultAzureCredential constructs offline; asking for a token with only local sources fails clearly
cred = DefaultAzureCredential(exclude_managed_identity_credential=True)
print("credential built:", type(cred).__name__)
try:
    cred.get_token("https://management.azure.com/.default")
except Exception as e:
    print("get_token:", type(e).__name__, "-", str(e).splitlines()[0][:100])
```

**Output (my run):** (azure-ai-ml 1.35.2; stdout shown; stderr carried only SDK warnings and the long credential error text, which I cut to its first line.)
```
azure-ai-ml 1.35.2
entity: mlw-dev-cin centralindia public_network_access = Disabled
  storage_account        -> None
  key_vault              -> None
  container_registry     -> None
  application_insights   -> None
ARM id shape: /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-ml-dev/providers/Microsoft.MachineLearningServices/workspaces/mlw-dev-cin
MLClient(credential=None): ValueError - credential can not be None
credential built: DefaultAzureCredential
get_token: ClientAuthenticationError - DefaultAzureCredential failed to retrieve a token from the included credentials.
```
Not executed: creating a workspace, the companion resources, RBAC, any `MLClient` call to a real workspace.

**Follow-ups:**
1. *Where do the companion resources show up?* After creation, in the same resource group unless you supplied your own; check current docs.
2. *Is a workspace a security boundary?* It is a scope for RBAC and network rules, not a magic wall; Part 12 owns design.
3. *Hub and project workspaces?* Newer workspace kinds exist; check current docs. I only built the default kind.

**Common mistakes:**
- "I created the Workspace object so the workspace exists."
- Putting dev and prod in one workspace and relying on naming.
- Forgetting that `MLClient(credential=None)` is a ValueError, not an auth error.

### Q3 ⭐⭐⭐ 🟢 Vertex AI project, region and staging-bucket setup: enabling the API, regional endpoints, aiplatform.init(project, location, staging_bucket), Application Default Credentials, and why jobs and models are regional resources. Show offline what really happens without credentials: constructing a PipelineJob or CustomJob raises a credentials error, while init with anonymous credentials lets objects build but submit returns 401. Explain what you would set in CI instead of a key file.
**Asked at:** GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs') | Certification-style question families (Microsoft DP-100 study guide and its replacement AI-300 as reported by third-party sites, Google Cloud Professional Machine Learning Engineer exam-prep listings; mentioned as a source type only, no exam questions reproduced; skills lists conflicted between sources, so verify on the vendor pages)
**Say this first (1 line):** On Vertex you enable the API in a project, choose a region once with `aiplatform.init(project, location, staging_bucket)`, authenticate with Application Default Credentials, and remember every job, model and endpoint is a regional resource.

**Then explain:**
- Setup: enable the Vertex AI API in the project, make a Cloud Storage bucket in the same region for staging, call `init`. The client then talks to a regional host (`<region>-aiplatform.googleapis.com`).
- Regional means: a model uploaded in one region cannot be deployed to an endpoint in another. Data in a bucket should sit in the same region (check current docs for exceptions and cost).
- Credentials: ADC looks at an env var for a key file, then the user's `gcloud` login, then the attached service account on Google compute. No credentials: the SDK raises a credentials error.
- What I measured offline: with no `init` the PipelineJob raised a project error; after `init` without credentials it raised `DefaultCredentialsError`; with `AnonymousCredentials` the PipelineJob and CustomJob objects built. Building an object proves nothing about access.
- In CI: use Workload Identity Federation (the CI platform's OIDC token trades for a short-lived credential for a service account), not a downloaded key file. Part 7 owns CI design; Q25 shows the workflow.
- Failure modes: bucket and job in different regions, staging bucket missing, a key file committed to the repo, the job service account lacking bucket access.

**Example:** Project `fake-project`, region `asia-south1`, bucket `gs://fake-bucket-name`. A job created in `asia-south1` with a staging bucket in another region fails or costs extra to cross, check current docs. Which regions have which accelerators: check current docs.

**Code:** the script compiles a tiny pipeline, then tries four situations. Anonymous credentials are used only to show object construction; `submit()` is deliberately not called.
```python
# q03.py
import os, warnings, tempfile, json
os.environ["NO_GCE_CHECK"] = "True"      # do not probe the GCE metadata server
for k in ("GOOGLE_APPLICATION_CREDENTIALS", "GOOGLE_CLOUD_PROJECT"):
    os.environ.pop(k, None)
warnings.filterwarnings("ignore")
import google.cloud.aiplatform as aip, kfp
from kfp import dsl, compiler
from google.auth.credentials import AnonymousCredentials
print("google-cloud-aiplatform", aip.__version__, "| kfp", kfp.__version__)

@dsl.component(base_image="python:3.11")
def hello(x: int) -> int:
    return x + 1
@dsl.pipeline(name="demo", pipeline_root="gs://fake-bucket-name/root")
def pl(x: int = 1):
    hello(x=x)
d = tempfile.mkdtemp()
tpl = os.path.join(d, "demo.json")
compiler.Compiler().compile(pl, tpl)

def attempt(label, fn):
    try:
        fn(); print(label, "-> built")
    except Exception as e:
        print(label, "->", type(e).__name__ + ":", str(e).replace("\n", " ")[:120])

mk_pj = lambda **kw: aip.PipelineJob(display_name="x", template_path=tpl, pipeline_root="gs://fake-bucket-name/r", **kw)
attempt("1. no init, PipelineJob", mk_pj)
aip.init(project="fake-project", location="asia-south1", staging_bucket="gs://fake-bucket-name")
print("2. init(project, location, staging_bucket) ok:", aip.initializer.global_config.project,
      aip.initializer.global_config.location, aip.initializer.global_config.staging_bucket)
attempt("3. init without creds, PipelineJob", mk_pj)
aip.init(project="fake-project", location="asia-south1", staging_bucket="gs://fake-bucket-name",
         credentials=AnonymousCredentials())
attempt("4. init + AnonymousCredentials, PipelineJob", mk_pj)
cj = lambda: aip.CustomJob(display_name="cj", worker_pool_specs=[{"machine_spec": {"machine_type": "n1-standard-4"},
     "replica_count": 1, "container_spec": {"image_uri": "gcr.io/fake/i:1"}}])
attempt("5. init + AnonymousCredentials, CustomJob", cj)
print("6. regional API host the client would call:", f"{aip.initializer.global_config.location}-aiplatform.googleapis.com", "(string only, not contacted)")
print("7. submit(): NOT called here. It would send the job to that host and, with anonymous credentials, be rejected (401).")
```

**Output (my run):** (google-cloud-aiplatform 1.165.1, kfp 2.17.3; `NO_GCE_CHECK=True` set so no metadata server probe.)
```
google-cloud-aiplatform 1.165.1 | kfp 2.17.3
1. no init, PipelineJob -> GoogleAuthError: Unable to find your project. Please provide a project ID by: - Passing a constructor argument - Using vertexai.init() - 
2. init(project, location, staging_bucket) ok: fake-project asia-south1 gs://fake-bucket-name
3. init without creds, PipelineJob -> DefaultCredentialsError: Your default credentials were not found. To set up Application Default Credentials, see https://cloud.google.com/docs/au
4. init + AnonymousCredentials, PipelineJob -> built
5. init + AnonymousCredentials, CustomJob -> built
6. regional API host the client would call: asia-south1-aiplatform.googleapis.com (string only, not contacted)
7. submit(): NOT called here. It would send the job to that host and, with anonymous credentials, be rejected (401).
```
Line 7 is a statement, not a result of this run. The earlier Wave A research run recorded that a real unauthenticated `submit()` returned HTTP 400 and then 401; I did not repeat any call to a Google endpoint. Real project setup, ADC with a real account and Workload Identity Federation: not executed.

**Follow-ups:**
1. *Why is `staging_bucket` needed?* The SDK uploads job artifacts there (code, specs, outputs) unless you give other paths.
2. *Can I use a key file?* It works but it is a long-lived secret. Prefer federation or an attached service account.
3. *Why did step 3 fail differently from step 1?* Step 1 had no project; step 3 had a project but no credentials.

**Common mistakes:**
- Treating "object built" as "job allowed".
- Using a bucket in a different region.
- Committing a service-account JSON.

### Q4 ⭐⭐⭐ 🟡 Azure ML CLI v2 and SDK v2 command job: write the job YAML (code, command, inputs with a datastore path, outputs, environment, compute, experiment name), load it with load_job, run the offline schema validation, build the same job with command() in the SDK, compare the two dictionaries, and show the error a misspelt key produces. Explain what runs on submit (not executed here).
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | Certification-style question families (Microsoft DP-100 study guide and its replacement AI-300 as reported by third-party sites, Google Cloud Professional Machine Learning Engineer exam-prep listings; mentioned as a source type only, no exam questions reproduced; skills lists conflicted between sources, so verify on the vendor pages)
**Say this first (1 line):** A command job is code plus a command line plus inputs, outputs, an environment and a compute target; the YAML and the SDK `command()` produce the same job object, and offline validation catches shape errors, not missing environments or missing data.

**Then explain:**
- YAML fields: `code` (folder uploaded as a snapshot), `command` with `${{inputs.x}}` and `${{outputs.y}}` placeholders, `inputs` (a datastore path or a literal), `outputs`, `environment`, `compute`, `experiment_name`.
- Two ways in: `az ml job create -f job.yml` (CLI v2, not executed) or `ml_client.jobs.create_or_update(job)` (SDK v2, not executed). Both send the same job to the service.
- What happens on submit (from docs, not run): the code folder is uploaded, the environment image is resolved or built, a node is allocated on the compute, the command runs, inputs are mounted or downloaded, outputs and logs are saved to the workspace storage.
- What offline validation does: the schema check says "Unknown field" for a misspelt key. It did not catch a command that refers to `${{inputs.learning_rate}}` when no such input exists, so that error appears only at run time.
- Failure modes: environment name that does not exist, compute name typo, datastore path wrong, identity without access, command refers to an input you never defined.

**Example:** A churn job with an `lr` of 0.1 reading a folder on the default datastore. The YAML job and the SDK job came out equal as dictionaries (after removing the absolute code path and the environment).

**Code:** the Python builds the YAML in a temp dir, loads it, validates, builds the SDK equivalent, compares, and breaks it two ways. The CLI line is shown for reference only.
```python
# q04.py
import warnings, os, json, tempfile; warnings.filterwarnings("ignore")
import azure.ai.ml as m
from azure.ai.ml import command, Input, Output, load_job
from azure.ai.ml.exceptions import ValidationException
print("azure-ai-ml", m.__version__)
d = tempfile.mkdtemp(); os.makedirs(f"{d}/src")
open(f"{d}/src/train.py", "w").write("print('train')\n")
JOB = """\
$schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
display_name: train-demo
experiment_name: churn-exp
code: ./src
command: python train.py --data ${{inputs.data}} --lr ${{inputs.lr}} --out ${{outputs.model_out}}
inputs:
  data:
    type: uri_folder
    path: azureml://datastores/workspaceblobstore/paths/churn/v1/
  lr: 0.1
outputs:
  model_out:
    type: uri_folder
environment: azureml:sklearn-env:1
compute: azureml:cpu-cluster
"""
open(f"{d}/job.yml", "w").write(JOB)
os.chdir(d)
y = load_job("job.yml")
r = y._validate()
print("YAML job:", type(y).__name__, "| validate passed:", r.passed)

s = command(
    display_name="train-demo", experiment_name="churn-exp", code="./src",
    command="python train.py --data ${{inputs.data}} --lr ${{inputs.lr}} --out ${{outputs.model_out}}",
    inputs={"data": Input(type="uri_folder", path="azureml://datastores/workspaceblobstore/paths/churn/v1/"), "lr": 0.1},
    outputs={"model_out": Output(type="uri_folder")},
    environment="azureml:sklearn-env:1", compute="azureml:cpu-cluster")
print("SDK job validate passed:", s._validate().passed)

dy, ds = y._to_dict(), s._to_dict()
for k in ("code", "environment"):          # code is resolved to an absolute temp path
    dy.pop(k, None); ds.pop(k, None)
print("dicts equal (ignoring code and environment):", dy == ds)
print("diff keys:", sorted(k for k in set(dy) | set(ds) if dy.get(k) != ds.get(k)))
print("top-level keys:", sorted(dy))
print(json.dumps({k: dy[k] for k in ("inputs", "outputs") if k in dy}, indent=1))

# misspelt key
open("bad.yml", "w").write(JOB.replace("inputs:", "inptus:", 1))
try:
    load_job("bad.yml")
except Exception as e:
    print("misspelt key ->", type(e).__name__, "|", " ".join(str(e).split())[:230])
# a command that references an input that does not exist
open("bad2.yml", "w").write(JOB.replace("${{inputs.lr}}", "${{inputs.learning_rate}}"))
try:
    r2 = load_job("bad2.yml")._validate()
    print("bad reference validate passed:", r2.passed, "|", getattr(r2, "error_messages", ""))
except Exception as e:
    print("bad reference ->", type(e).__name__, str(e)[:160])
```
```bash
# not executed: needs az CLI with the ml extension and a login
az ml job create -f job.yml --workspace-name mlw-dev-cin --resource-group rg-ml-dev
```

**Output (my run):** (azure-ai-ml 1.35.2; stderr had "experimental class" warnings, not shown; error text shortened by the script.)
```
azure-ai-ml 1.35.2
YAML job: Command | validate passed: True
SDK job validate passed: True
dicts equal (ignoring code and environment): True
diff keys: []
top-level keys: ['component', 'compute', 'inputs', 'outputs', 'type']
{
 "inputs": {
  "data": {
   "type": "uri_folder",
   "path": "azureml://datastores/workspaceblobstore/paths/churn/v1/"
  },
  "lr": 0.1
 },
 "outputs": {
  "model_out": {
   "type": "uri_folder"
  }
 }
}
misspelt key -> ValidationError | Validation for CommandSchema failed: { "result": "Failed", "errors": [ { "message": "Validation for CommandJobSchema failed:\n\n {\n \"inptus\": [\n \"Unknown field.\"\n ]\n} \n\n If you are trying to configure a job that is not o
bad reference validate passed: True | {}
```
Not executed: the `az` CLI (not installed here), submit, compute, the datastore read, the environment build.

**Follow-ups:**
1. *Why does `$schema` matter?* Editors use it for autocompletion. This run did not fetch the URL; validation used the SDK's own schemas.
2. *Are the dicts always equal?* Not across versions; SDK object kwargs drift, check current docs.
3. *Where do I see output?* In the job's run page and the workspace storage; not run here.

**Common mistakes:**
- Treating `_validate()` passing as "the job will run".
- Relying on a private method `_validate()` in production; it is shown only as the offline check here and may change.
- Hard-coding a storage key in `command`.

### Q5 ⭐⭐⭐ 🟡 Azure ML compute choices: compute instance (dev box), compute cluster (AmlCompute with min and max nodes, scale to zero, idle time before scale down), serverless compute, attached Kubernetes, and quota and node-type limits per Region. Pick one for a nightly 4-hour GPU training job and for a notebook user, and say what a min_instances of 0 costs you in start-up delay. Build an AmlCompute entity offline and assert the scale-to-zero settings. No prices.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | Job-posting and community patterns for Azure-heavy IT-services firms and GCCs (Azure ML plus Azure DevOps) versus GCP-using product companies (Vertex plus BigQuery); inferred from search snippets about ecosystem fit, not from a verified company report
**Say this first (1 line):** Use a compute instance for a person at a notebook, a compute cluster that scales to zero for the nightly GPU job, serverless when you do not want to manage a cluster, and attached Kubernetes when platform rules require it; always check the Region quota first.

**Then explain:**
- Compute instance: one VM per user, interactive, should have idle shutdown on. Compute cluster (AmlCompute): `min_instances`, `max_instances`, idle time before scale-down; multi-node training and queued jobs. Serverless: you give instance type and count on the job, no cluster object. Attached Kubernetes: your own cluster, your own ops.
- Nightly 4-hour GPU job: cluster with `min_instances=0` and a sensible `max_instances`. Notebook user: a compute instance with idle shutdown and a schedule. Quota is per VM family per Region; check current docs.
- Cost of min 0: the first job waits for node allocation and image pull. How long depends on the VM family, region capacity and image size, so I would measure it, not quote a number. For a nightly job the wait does not matter. For many short jobs per hour it does; then keep warm nodes (min above 0) and accept idle time.
- Failure modes: quota too low for the GPU family so jobs sit queued, `max_instances` too high with no quota guard, instance left running over a weekend, scale-to-zero cluster used for latency-sensitive work.

**Example:** Nightly 4-hour job at 02:00 on a 2-node cluster with 5 minutes idle time: nodes spin up at job start and release after the idle window. A `Standard_NC6s_v3`-style size is used only as an example name; whether it exists in your Region: check current docs.

**Code:** two entities built offline, assertions on scale-to-zero, and a toy selection rule. The rule is my own simplification, not Microsoft guidance.
```python
# q05.py
import warnings; warnings.filterwarnings("ignore")
import azure.ai.ml as m
from azure.ai.ml.entities import AmlCompute, ComputeInstance
print("azure-ai-ml", m.__version__)

cluster = AmlCompute(name="gpu-nightly", size="Standard_NC6s_v3", min_instances=0, max_instances=2,
                     idle_time_before_scale_down=300, tier="dedicated")
assert cluster.min_instances == 0, "scale to zero needs min 0"
assert cluster.max_instances >= 1
assert cluster.idle_time_before_scale_down == 300
print("cluster:", cluster.name, cluster.type, cluster.size, "min", cluster.min_instances, "max", cluster.max_instances,
      "idle_s", cluster.idle_time_before_scale_down, "tier", cluster.tier)

ci = ComputeInstance(name="dev-asha", size="Standard_DS3_v2", idle_time_before_shutdown_minutes=60)
print("instance:", ci.name, ci.type, ci.size, "idle shutdown min", ci.idle_time_before_shutdown_minutes)

def pick(workload):
    """Toy rule used in the answer; the real inputs are your quota and team habits."""
    if workload["interactive"]:
        return "compute instance (one user, idle shutdown on)"
    if workload["duration_h"] >= 1 and workload["gpu"] and workload["runs_per_day"] <= 1:
        return "compute cluster min=0 (or serverless if quota is pooled and you want no cluster to manage)"
    if workload["runs_per_day"] > 24:
        return "cluster with min>0 (warm nodes) to avoid repeated start-up"
    return "serverless compute"
for w in ({"interactive": True, "gpu": False, "duration_h": 8, "runs_per_day": 1},
          {"interactive": False, "gpu": True, "duration_h": 4, "runs_per_day": 1},
          {"interactive": False, "gpu": False, "duration_h": 0.1, "runs_per_day": 100}):
    print(w, "->", pick(w))

# a bad config is caught only by our own check; the entity itself accepts it offline
bad = AmlCompute(name="oops", size="Standard_NC6s_v3", min_instances=2, max_instances=1)
print("entity accepts min>max offline:", bad.min_instances, bad.max_instances, "| our check:", "min <= max" if bad.min_instances <= bad.max_instances else "REJECT min>max")
```

**Output (my run):** (azure-ai-ml 1.35.2.)
```
azure-ai-ml 1.35.2
cluster: gpu-nightly amlcompute Standard_NC6s_v3 min 0 max 2 idle_s 300 tier dedicated
instance: dev-asha computeinstance Standard_DS3_v2 idle shutdown min 60
{'interactive': True, 'gpu': False, 'duration_h': 8, 'runs_per_day': 1} -> compute instance (one user, idle shutdown on)
{'interactive': False, 'gpu': True, 'duration_h': 4, 'runs_per_day': 1} -> compute cluster min=0 (or serverless if quota is pooled and you want no cluster to manage)
{'interactive': False, 'gpu': False, 'duration_h': 0.1, 'runs_per_day': 100} -> cluster with min>0 (warm nodes) to avoid repeated start-up
entity accepts min>max offline: 2 1 | our check: REJECT min>max
```
Not executed: creating compute, quota, GPU availability, node start-up time. No prices.

**Follow-ups:**
1. *Why did the entity accept min greater than max?* Offline objects do no cross-field checks; the service (or your own CI check) must.
2. *Where does cost depth live?* Part 12.
3. *Serverless vs cluster?* Serverless saves cluster admin; a cluster gives you a fixed pool and shared quota control. Check current docs for what serverless supports.

**Common mistakes:**
- `min_instances` above 0 "just in case", leaving GPUs idle.
- No idle shutdown on instances.
- Assuming the same VM size exists in every Region.

### Q6 ⭐⭐⭐ 🟡 Azure ML pipelines with components: define a command component in YAML, wire two steps with parent inputs and a step output, build the same with the dsl.pipeline decorator, load and validate the pipeline YAML offline, and say what caching, reuse and default compute mean. Show what validation catches and what only a real submit catches. Part 5 owns orchestration concepts; stay on the Azure shape.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | Certification-style question families (Microsoft DP-100 study guide and its replacement AI-300 as reported by third-party sites, Google Cloud Professional Machine Learning Engineer exam-prep listings; mentioned as a source type only, no exam questions reproduced; skills lists conflicted between sources, so verify on the vendor pages)
**Say this first (1 line):** An Azure ML pipeline is a pipeline job whose steps are components; you wire step outputs to step inputs with `${{parent...}}` bindings in YAML or with the `dsl.pipeline` decorator, and offline validation checks structure while only a real submit checks compute, environments and data.

**Then explain:**
- Component: a reusable command with typed inputs and outputs and an environment, versioned. Pipeline job: `jobs:` of steps, each pointing at a component, with `settings.default_compute`.
- Wiring: `${{parent.inputs.raw_data}}` feeds a pipeline input into a step; `${{parent.jobs.prep_step.outputs.clean}}` feeds one step's output to the next; a step output is promoted to a pipeline output with `${{parent.outputs.final_model}}`.
- Caching and reuse: a deterministic component with the same inputs and code can reuse an earlier result instead of running again. Check current docs for the exact reuse conditions; `is_deterministic` is the component-side switch.
- Default compute: a step with no `compute` uses `settings.default_compute`.
- What my offline run showed: the structural check caught a missing component file. It did not catch a misspelt step output name (`cleen`), so that kind of error only appears on submit or in review. I would write a small test that resolves every binding.
- Failure modes: step reuse hiding a data change (data path same, content new), wrong binding name, forgot a type on a Python SDK step, compute name not existing.

**Example:** `prep_step` makes `clean`; `train_step` takes `clean` and `lr` and returns `model`, promoted to `final_model`.

**Code:** components and pipeline YAML written to a temp dir, loaded, validated, rebuilt with `dsl.pipeline`, then two bad variants.
```python
# q06.py
import warnings, os, tempfile, json; warnings.filterwarnings("ignore")
import azure.ai.ml as m
from azure.ai.ml import command, Input, Output, load_job, load_component
from azure.ai.ml.dsl import pipeline
print("azure-ai-ml", m.__version__)
d = tempfile.mkdtemp(); os.makedirs(f"{d}/src"); os.chdir(d)
for n in ("prep", "train"):
    open(f"src/{n}.py", "w").write("pass\n")
open("prep.yml", "w").write("""\
$schema: https://azuremlschemas.azureedge.net/latest/commandComponent.schema.json
type: command
name: prep
version: "1"
code: ./src
command: python prep.py --raw ${{inputs.raw}} --out ${{outputs.clean}}
inputs:
  raw: {type: uri_folder}
outputs:
  clean: {type: uri_folder}
environment: azureml:sklearn-env:1
""")
open("train.yml", "w").write("""\
$schema: https://azuremlschemas.azureedge.net/latest/commandComponent.schema.json
type: command
name: train
version: "1"
code: ./src
command: python train.py --data ${{inputs.data}} --lr ${{inputs.lr}} --model ${{outputs.model}}
inputs:
  data: {type: uri_folder}
  lr: {type: number, default: 0.1}
outputs:
  model: {type: uri_folder}
environment: azureml:sklearn-env:1
is_deterministic: true
""")
PIPE = """\
$schema: https://azuremlschemas.azureedge.net/latest/pipelineJob.schema.json
type: pipeline
display_name: churn-pipe
settings:
  default_compute: azureml:cpu-cluster
inputs:
  raw_data: {type: uri_folder, path: azureml://datastores/workspaceblobstore/paths/raw/}
  lr: 0.05
jobs:
  prep_step:
    type: command
    component: ./prep.yml
    inputs:
      raw: ${{parent.inputs.raw_data}}
  train_step:
    type: command
    component: ./train.yml
    inputs:
      data: ${{parent.jobs.prep_step.outputs.clean}}
      lr: ${{parent.inputs.lr}}
    outputs:
      model: ${{parent.outputs.final_model}}
outputs:
  final_model: {type: uri_folder}
"""
open("pipe.yml", "w").write(PIPE)
p = load_job("pipe.yml")
print("YAML pipeline:", type(p).__name__, "steps:", list(p.jobs), "validate passed:", p._validate().passed)

prep, train = load_component("prep.yml"), load_component("train.yml")
@pipeline(default_compute="cpu-cluster")
def churn(raw_data, lr: float = 0.05):
    a = prep(raw=raw_data)
    b = train(data=a.outputs.clean, lr=lr)
    return {"final_model": b.outputs.model}
sp = churn(raw_data=Input(type="uri_folder", path="azureml://datastores/workspaceblobstore/paths/raw/"))
print("SDK pipeline steps:", list(sp.jobs), "| validate passed:", sp._validate().passed)
print("train component is_deterministic (reuse allowed):", train.is_deterministic)

# What validation catches
open("bad_pipe.yml", "w").write(PIPE.replace("${{parent.jobs.prep_step.outputs.clean}}", "${{parent.jobs.prep_step.outputs.cleen}}"))
r = load_job("bad_pipe.yml")._validate()
print("misspelt step output -> passed:", r.passed, "|", [" ".join(str(x).split())[:110] for x in (r.error_messages.values() if isinstance(getattr(r, 'error_messages', None), dict) else [])][:2])
open("bad_pipe2.yml", "w").write(PIPE.replace("./train.yml", "./missing.yml"))
try:
    r = load_job("bad_pipe2.yml")._validate(); print("missing component file -> passed:", r.passed)
except Exception as e:
    print("missing component file ->", type(e).__name__, "|", " ".join(str(e).split())[:140])
print("NOT caught offline: compute 'cpu-cluster' exists, environment azureml:sklearn-env:1 exists, quota, data path readable, script runs.")
```

**Output (my run):** (azure-ai-ml 1.35.2; load of a pipeline with a misspelt output binding returned a passing validation; error text shortened.)
```
azure-ai-ml 1.35.2
YAML pipeline: PipelineJob steps: ['prep_step', 'train_step'] validate passed: True
SDK pipeline steps: ['a', 'b'] | validate passed: True
train component is_deterministic (reuse allowed): True
misspelt step output -> passed: True | []
missing component file -> ValidationError | Validation for PipelineJobSchema failed: { "result": "Failed", "errors": [ { "message": "In order to specify an existing None, please provid
NOT caught offline: compute 'cpu-cluster' exists, environment azureml:sklearn-env:1 exists, quota, data path readable, script runs.
```
Not executed: submit, caching behaviour, step scheduling, compute and environment existence. Part 5 owns orchestration concepts.

**Follow-ups:**
1. *Can the YAML and SDK pipelines differ?* They gave the same shape here (step names differ because the SDK names steps from variable names).
2. *Why a component, not a script?* Typed interface, versioning and reuse across pipelines.
3. *How do I catch binding typos?* A unit test that parses the YAML and checks each `${{parent.jobs.X.outputs.Y}}` against the component's declared outputs.

**Common mistakes:**
- Assuming validation means the pipeline will run.
- Turning on reuse for a non-deterministic step (timestamps, random seeds, "latest" data).
- Forgetting default compute and hitting a compute error on submit.

### Q7 ⭐⭐⭐ 🟡 Azure ML managed online endpoints: endpoint versus deployment, blue and green deployments with a traffic split (sums to 0 or 100; deployments must exist before traffic is set), scoring script versus MLflow no-code deployment, auth modes (key, aml_token, Microsoft Entra token) and the endpoint identity. Build ManagedOnlineEndpoint and ManagedOnlineDeployment objects offline, write a function that rejects a bad traffic map, and name what a real rollout needs. Part 6 owns rollout mechanics.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | Certification-style question families (Microsoft DP-100 study guide and its replacement AI-300 as reported by third-party sites, Google Cloud Professional Machine Learning Engineer exam-prep listings; mentioned as a source type only, no exam questions reproduced; skills lists conflicted between sources, so verify on the vendor pages)
**Say this first (1 line):** A managed online endpoint is a stable URL and auth setup; deployments (blue, green) sit behind it and traffic percentages move between them, with the rule that the map must sum to 0 or 100 and only name deployments that already exist.

**Then explain:**
- Endpoint versus deployment: the endpoint holds name, auth mode and traffic; a deployment holds model, environment or scoring script, VM size and instance count.
- Scoring script versus MLflow no-code: with a custom model you give `score.py` with `init()` and `run()` plus an environment; for an MLflow model the service can build scoring for you, so no script and no environment on the deployment. Check current docs for supported flavors.
- Auth modes: `key`, `aml_token`, and Microsoft Entra token (I would check current docs for the exact option names in the SDK version you use). The endpoint has an identity (system- or user-assigned) that the container uses to read things like Key Vault; that is separate from the caller's identity.
- Rollout: create green with 0 traffic, test it (a deployment can be called directly with a header, check current docs), then shift 10 percent, then 100, then delete blue. Part 6 owns rollout mechanics.
- Failure modes: setting traffic before the deployment exists, traffic that sums to 95, deleting blue before green is healthy, quota too low for two deployments side by side, scoring script that loads the model in `run()` instead of `init()`.

**Example:** blue 100. Create green at 0. Set `{"blue": 90, "green": 10}`. Check metrics. Set `{"green": 100}`. The function below accepts that and rejects 90 plus 5.

**Code:** objects built offline and a traffic-map validator that I wrote. The service applies its own checks; this one is for CI.
```python
# q07.py
import warnings; warnings.filterwarnings("ignore")
import azure.ai.ml as m
from azure.ai.ml.entities import ManagedOnlineEndpoint, ManagedOnlineDeployment, CodeConfiguration, Environment
print("azure-ai-ml", m.__version__)

ep = ManagedOnlineEndpoint(name="churn-ep", auth_mode="key", description="offline entity")
env = Environment(name="sk", version="1", image="mcr.microsoft.com/azureml/minimal-ubuntu22.04-py311-cpu-inference:latest")
blue = ManagedOnlineDeployment(name="blue", endpoint_name="churn-ep", model="azureml:churn-model:1", environment=env,
        code_configuration=CodeConfiguration(code=".", scoring_script="score.py"), instance_type="Standard_DS3_v2", instance_count=1)
green = ManagedOnlineDeployment(name="green", endpoint_name="churn-ep", model="azureml:churn-model:2",
        instance_type="Standard_DS3_v2", instance_count=1)   # MLflow model: no scoring script, no environment
print("endpoint:", ep.name, "auth_mode =", ep.auth_mode)
print("blue  (custom scoring):", blue.code_configuration.scoring_script, "| env:", blue.environment.name)
print("green (MLflow no-code): scoring script =", green.code_configuration, "| env =", green.environment)

def check_traffic(traffic, existing):
    """Same rules the answer states: only known deployments, 0-100 each, total 0 or 100."""
    unknown = set(traffic) - set(existing)
    if unknown:
        raise ValueError(f"deployments not created yet: {sorted(unknown)}")
    if any(not 0 <= v <= 100 for v in traffic.values()):
        raise ValueError("each share must be 0..100")
    total = sum(traffic.values())
    if total not in (0, 100):
        raise ValueError(f"traffic must sum to 0 or 100, got {total}")
    return True

existing = ["blue"]
cases = [("only blue", {"blue": 100}, existing),
         ("canary before green exists", {"blue": 90, "green": 10}, existing),
         ("canary after green exists", {"blue": 90, "green": 10}, ["blue", "green"]),
         ("sums to 95", {"blue": 85, "green": 10}, ["blue", "green"]),
         ("all zero (pause)", {"blue": 0, "green": 0}, ["blue", "green"])]
for label, t, ex in cases:
    try:
        print(f"{label:28}", t, "->", check_traffic(t, ex))
    except ValueError as e:
        print(f"{label:28}", t, "-> REJECT:", e)
ep.traffic = {"blue": 90, "green": 10}
print("entity holds traffic map:", ep.traffic, "(the service, not the entity, enforces the rule)")
```

**Output (my run):** (azure-ai-ml 1.35.2.)
```
azure-ai-ml 1.35.2
endpoint: churn-ep auth_mode = key
blue  (custom scoring): score.py | env: sk
green (MLflow no-code): scoring script = None | env = None
only blue                    {'blue': 100} -> True
canary before green exists   {'blue': 90, 'green': 10} -> REJECT: deployments not created yet: ['green']
canary after green exists    {'blue': 90, 'green': 10} -> True
sums to 95                   {'blue': 85, 'green': 10} -> REJECT: traffic must sum to 0 or 100, got 95
all zero (pause)             {'blue': 0, 'green': 0} -> True
entity holds traffic map: {'blue': 90, 'green': 10} (the service, not the entity, enforces the rule)
```
Not executed: creating the endpoint or deployments, auth, scoring, traffic shifting, mirrored traffic (third-party sources mention it; the exact syntax was not confirmed; check current docs).

**Follow-ups:**
1. *What needs to be real for a rollout?* Quota for both deployments, a model asset, environment image, identity roles, and a monitoring check before shifting.
2. *Can I skip a canary?* You can, but then a bad model takes all traffic at once.
3. *Batch has traffic split?* No; you switch the default deployment instead (Q17).

**Common mistakes:**
- Setting `traffic` before creating the deployment.
- Giving the endpoint identity broad roles.
- Believing the SDK entity validates the traffic rule offline (it did not here).

### Q8 ⭐⭐⭐ 🟡 Vertex AI custom training: CustomJob worker_pool_specs (machine type, accelerator, replica count, prebuilt versus custom container), the staging bucket, the job service account and network, and what AIP_MODEL_DIR style environment variables are for. Build a CustomJob and the underlying CustomJobSpec proto offline, print it as JSON, and explain what a real run needs (not executed). Compare with an Azure ML command job in two sentences.
**Asked at:** GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs') | Certification-style question families (Microsoft DP-100 study guide and its replacement AI-300 as reported by third-party sites, Google Cloud Professional Machine Learning Engineer exam-prep listings; mentioned as a source type only, no exam questions reproduced; skills lists conflicted between sources, so verify on the vendor pages)
**Say this first (1 line):** A Vertex CustomJob is a list of worker pools, each with a machine spec, replica count and a container (prebuilt or your own), run under a service account, writing to a staging bucket; the `AIP_*` environment variables tell the container where to put the model.

**Then explain:**
- `worker_pool_specs`: pool 0 is the chief (replica count 1); more pools are workers, parameter servers or evaluators for distributed training. Each pool has `machine_spec` (machine type, accelerator type and count), `replica_count`, and `container_spec` (image, args, env) or a Python package spec.
- Prebuilt versus custom container: prebuilt for common frameworks, custom for your own dependencies (image in Artifact Registry). Whether a given framework version is available: check current docs.
- Identity and network: pass a `service_account` for the job; without one it runs as a default service account that may have more rights than you want. `network` attaches the job to a VPC through peering, or use Private Service Connect (see Q24).
- Environment variables: Vertex sets variables like `AIP_MODEL_DIR` (where to save the model), `AIP_CHECKPOINT_DIR` and `AIP_TENSORBOARD_LOG_DIR` when you set a base output directory. My script reads `AIP_MODEL_DIR` with a local fallback, so it also runs on a laptop. Names are from the docs as I remember them; check current docs.
- Azure comparison in two sentences: an Azure command job points at a named compute and an environment asset, and the data is a mounted input. A Vertex CustomJob carries its machine spec and container inline, and the data is whatever path your code reads with the job's service account.
- Failure modes: bucket in another region, job service account missing bucket access, GPU quota or accelerator not in the region, image not pullable by the service agent, timeouts.

**Example:** One T4 on an `n1-standard-8`, one replica, image in Artifact Registry in `asia-south1`, 4-hour timeout, service account `trainer@...`.

**Code:** both the SDK `CustomJob` and the raw proto are built with `AnonymousCredentials`; nothing is sent.
```python
# q08.py
import os, warnings, json
os.environ["NO_GCE_CHECK"] = "True"
warnings.filterwarnings("ignore")
import google.cloud.aiplatform as aip
from google.auth.credentials import AnonymousCredentials
from google.cloud.aiplatform_v1.types import CustomJobSpec, WorkerPoolSpec, MachineSpec, ContainerSpec, Scheduling
print("google-cloud-aiplatform", aip.__version__)
aip.init(project="fake-project", location="asia-south1", staging_bucket="gs://fake-bucket-name", credentials=AnonymousCredentials())

pools = [
  {"machine_spec": {"machine_type": "n1-standard-8", "accelerator_type": "NVIDIA_TESLA_T4", "accelerator_count": 1},
   "replica_count": 1,
   "container_spec": {"image_uri": "asia-south1-docker.pkg.dev/fake-project/ml/train:1.0",
                      "args": ["--epochs", "3"], "env": [{"name": "MODEL_NAME", "value": "churn"}]}},
]
cj = aip.CustomJob(display_name="churn-train", worker_pool_specs=pools,
                   staging_bucket="gs://fake-bucket-name/jobs", base_output_dir="gs://fake-bucket-name/out/run1")
print("CustomJob built:", type(cj).__name__, "| resource name before submit:", getattr(cj._gca_resource, "name", "") or "(empty)")
spec = cj._gca_resource.job_spec
print("service_account on spec (empty unless passed to run/submit):", repr(spec.service_account))
print("base_output_dir:", spec.base_output_directory.output_uri_prefix)

# the underlying proto, built by hand with a service account and a peered network
proto = CustomJobSpec(
    worker_pool_specs=[WorkerPoolSpec(machine_spec=MachineSpec(machine_type="n1-standard-8",
        accelerator_type="NVIDIA_TESLA_T4", accelerator_count=1), replica_count=1,
        container_spec=ContainerSpec(image_uri="asia-south1-docker.pkg.dev/fake-project/ml/train:1.0", args=["--epochs", "3"]))],
    service_account="trainer@fake-project.iam.gserviceaccount.com",
    network="projects/123456789/global/networks/vpc-ml",
    scheduling=Scheduling(timeout={"seconds": 14400}),
)
def prune(x):
    if isinstance(x, dict):
        return {k: prune(v) for k, v in x.items() if v not in ("", [], 0, False, None, {}) or k == "replicaCount"}
    if isinstance(x, list):
        return [prune(i) for i in x]
    return x
print(json.dumps(prune(json.loads(CustomJobSpec.to_json(proto))), indent=1))
print("(empty and zero-valued fields pruned for reading; acceleratorType 5 is the enum number)")

# how a training script should read them, with a local fallback so it also runs on a laptop
model_dir = os.environ.get("AIP_MODEL_DIR", "./model_out")
print("script would write the model to:", model_dir)
```

**Output (my run):** (google-cloud-aiplatform 1.165.1.)
```
google-cloud-aiplatform 1.165.1
CustomJob built: CustomJob | resource name before submit: (empty)
service_account on spec (empty unless passed to run/submit): ''
base_output_dir: gs://fake-bucket-name/out/run1
{
 "workerPoolSpecs": [
  {
   "machineSpec": {
    "machineType": "n1-standard-8",
    "acceleratorType": 5,
    "acceleratorCount": 1
   },
   "replicaCount": "1",
   "containerSpec": {
    "imageUri": "asia-south1-docker.pkg.dev/fake-project/ml/train:1.0",
    "args": [
     "--epochs",
     "3"
    ]
   }
  }
 ],
 "scheduling": {
  "timeout": "14400s"
 },
 "serviceAccount": "trainer@fake-project.iam.gserviceaccount.com",
 "network": "projects/123456789/global/networks/vpc-ml"
}
(empty and zero-valued fields pruned for reading; acceleratorType 5 is the enum number)
script would write the model to: ./model_out
```
Not executed: `run()`/`submit()`, image pull, GPU allocation, service-account or VPC checks, writing to a real bucket.

**Follow-ups:**
1. *Why is the service account empty on the SDK object?* It is passed at run or submit time in this SDK; check current docs for your version.
2. *Chief and workers?* Pool 0 chief, later pools for workers, per Vertex docs.
3. *Where is the model saved?* Under the output directory you set, read through `AIP_MODEL_DIR`.

**Common mistakes:**
- Running as the default service account with broad rights.
- Hard-coding output paths instead of reading `AIP_MODEL_DIR`.
- Assuming an offline object means a valid image or quota.

### Q9 ⭐⭐⭐ 🟡 Vertex AI Pipelines: compile a KFP v2 pipeline to a Vertex-compatible JSON and YAML, inspect the pipelineInfo, root DAG tasks and default pipeline root, construct a PipelineJob and say what submit does (service account, GCS root, caching, ML Metadata lineage). Run the KFP local SubprocessRunner on one component to show logic can be tested without the service. Part 5 owns KFP concepts; this answer is the Vertex service layer.
**Asked at:** GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs') | Certification-style question families (Microsoft DP-100 study guide and its replacement AI-300 as reported by third-party sites, Google Cloud Professional Machine Learning Engineer exam-prep listings; mentioned as a source type only, no exam questions reproduced; skills lists conflicted between sources, so verify on the vendor pages)
**Say this first (1 line):** Vertex Pipelines runs a compiled KFP v2 spec: you compile to JSON or YAML, create a PipelineJob with a GCS pipeline root and parameter values, and the service runs each task as a container under a service account, records artifacts and lineage in ML Metadata, and skips cached steps.

**Then explain:**
- What the compile gives you: `pipelineInfo` (name), `root.dag.tasks` (the steps and their dependencies), `components` and `deploymentSpec.executors` (the containers), `defaultPipelineRoot` and `root.inputDefinitions` (the parameters).
- What `submit` does (docs, not run here): uploads or reads the spec, uses the pipeline root in Cloud Storage for artifacts, runs each task under the pipeline service account you pass, records executions and artifacts in ML Metadata so you can trace lineage, and reuses a cached step when the inputs and component match and caching is on.
- Testing logic without the service: `kfp.local` with `SubprocessRunner` runs one component as a subprocess on your machine. It tests the Python logic, not GCS, IAM or container images.
- Failure modes: service account without bucket access, pipeline root bucket in another region, cache hiding a data change, unpinned `packages_to_install` at run time, forgetting that a lightweight component's imports must be inside the function.
- Part 5 owns KFP concepts; this answer is the Vertex service layer.

**Example:** `prep` then `train`. The compiled root lists both tasks and `train` has `dependentTasks: [prep]`.

**Code:** compile, inspect, build the PipelineJob with anonymous credentials (no submit), and run the local runner on one component. The runner's own log lines are hidden and counted.
```python
# q09.py
import os, warnings, json, tempfile
os.environ["NO_GCE_CHECK"] = "True"
warnings.filterwarnings("ignore")
import kfp, google.cloud.aiplatform as aip
from kfp import dsl, compiler, local
from google.auth.credentials import AnonymousCredentials
print("kfp", kfp.__version__, "| google-cloud-aiplatform", aip.__version__)

@dsl.component(base_image="python:3.11")
def prep(n: int, out: dsl.Output[dsl.Dataset]):
    open(out.path, "w").write(str(n))
@dsl.component(base_image="python:3.11")
def train(d: dsl.Input[dsl.Dataset], m: dsl.Output[dsl.Model], lr: float = 0.1):
    open(m.path, "w").write("model")
@dsl.pipeline(name="churn-pipe", pipeline_root="gs://fake-bucket-name/pipeline-root")
def pl(n: int = 5, lr: float = 0.1):
    p = prep(n=n)
    train(d=p.outputs["out"], lr=lr).set_cpu_limit("2").set_memory_limit("4G")

work = tempfile.mkdtemp()
js, ym = os.path.join(work, "pipe.json"), os.path.join(work, "pipe.yaml")
compiler.Compiler().compile(pl, js); compiler.Compiler().compile(pl, ym)
spec = json.load(open(js))
print("top-level sections:", sorted(spec))
print("pipelineInfo:", spec["pipelineInfo"])
print("defaultPipelineRoot:", spec["defaultPipelineRoot"])
print("root DAG tasks:", list(spec["root"]["dag"]["tasks"]))
print("train depends on:", spec["root"]["dag"]["tasks"]["train"]["dependentTasks"])
print("root input parameters:", spec["root"]["inputDefinitions"]["parameters"])
print("executors:", list(spec["deploymentSpec"]["executors"]))
print("YAML compiled too, first line:", open(ym).read().splitlines()[0])

aip.init(project="fake-project", location="asia-south1", credentials=AnonymousCredentials())
pj = aip.PipelineJob(display_name="churn-pipe", template_path=js, parameter_values={"n": 3, "lr": 0.05},
                     enable_caching=False, labels={"team": "ml"})
print("PipelineJob built offline:", type(pj).__name__, "| pipeline_root:", pj.pipeline_spec["defaultPipelineRoot"])
print("submit(): NOT called (it would go to the regional Vertex API).")

# local run of one component: no service, no GCS, subprocess on this machine
local.init(runner=local.SubprocessRunner(), pipeline_root=os.path.join(work, "local_root"))
@dsl.component
def add(a: int, b: int) -> int:
    return a + b
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    t = add(a=1, b=2)
print("runner log lines hidden:", len(buf.getvalue().splitlines()), "| task status line:", [l.strip() for l in buf.getvalue().splitlines() if "finished with status" in l][0].split(" - ")[-1].replace("\x1b[96m","").replace("\x1b[0m","").replace("\x1b[92m",""))
print("kfp.local SubprocessRunner result:", t.output)
```

**Output (my run):** (kfp 2.17.3, google-cloud-aiplatform 1.165.1.)
```
kfp 2.17.3 | google-cloud-aiplatform 1.165.1
top-level sections: ['components', 'defaultPipelineRoot', 'deploymentSpec', 'pipelineInfo', 'root', 'schemaVersion', 'sdkVersion']
pipelineInfo: {'name': 'churn-pipe'}
defaultPipelineRoot: gs://fake-bucket-name/pipeline-root
root DAG tasks: ['prep', 'train']
train depends on: ['prep']
root input parameters: {'lr': {'defaultValue': 0.1, 'isOptional': True, 'parameterType': 'NUMBER_DOUBLE'}, 'n': {'defaultValue': 5.0, 'isOptional': True, 'parameterType': 'NUMBER_INTEGER'}}
executors: ['exec-prep', 'exec-train']
YAML compiled too, first line: # PIPELINE DEFINITION
PipelineJob built offline: PipelineJob | pipeline_root: gs://fake-bucket-name/pipeline-root
submit(): NOT called (it would go to the regional Vertex API).
runner log lines hidden: 29 | task status line: Task 'add' finished with status SUCCESS
kfp.local SubprocessRunner result: 3
```
Not executed: `submit()`, any use of GCS, service-account checks, caching, ML Metadata lineage. The local runner used the default Python of the venv; the component had no extra packages.

**Follow-ups:**
1. *JSON or YAML?* Both compile; Vertex accepts the compiled spec; check current docs for which formats your SDK version prefers.
2. *Does local run test caching?* No, caching is a service feature.
3. *Which service account?* The one you pass at submit; give it only the bucket, registry and API roles the steps need.

**Common mistakes:**
- Believing `PipelineJob(...)` built offline means the pipeline is valid in the service.
- Using one wide service account for every pipeline.
- Caching steps that read mutable "latest" data.
