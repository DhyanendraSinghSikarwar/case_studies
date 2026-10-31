# Book 4 — Part 11: Azure Machine Learning and Google Cloud Vertex AI (with a cross-cloud comparison)

**Topic:** Azure ML (workspace, compute instances and clusters, datastores and data assets, environments, jobs, components and pipelines in YAML v2 and SDK v2, managed online and batch endpoints, model registry, MLflow integration, AutoML, sweep jobs, Responsible AI dashboard, managed identity and RBAC, managed virtual network and private endpoints, Azure DevOps and GitHub integration, SDK v1 to v2 migration, Azure OpenAI at the boundary only), Google Vertex AI (Workbench, custom training, Vertex Pipelines and KFP, online and batch prediction, Model Registry, Feature Store, Experiments, Model Monitoring, Vizier tuning, AutoML, BigQuery ML at the boundary, IAM and service accounts, VPC Service Controls and Private Service Connect, Gemini at the boundary only), and the cross-cloud layer (service mapping with AWS SageMaker by concept only, vendor lock-in, multi-cloud, portability through containers, MLflow and KFP, identity models, networking, governance, India Region and data-residency concerns, choosing a platform, migration)

**Target:** 35  |  **Actual:** 35 (⭐⭐⭐ 14, ⭐⭐ 15, ⭐ 6)  |  **Date:** 2026-10-26  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 1 owns Git and pytest for ML code; Part 2 owns Docker; Part 3 owns Kubernetes and Helm; Part 4 owns DVC, MLflow and registry basics; Part 5 owns pipelines and orchestration concepts including KFP; Part 6 owns serving mechanics, latency, shadow, canary and rollout; Part 7 owns CI workflows and promotion gates; Part 8 owns monitoring, drift detection and alerting; Part 9 owns feature-store concepts, Kafka and Spark; Part 10 owns AWS and SageMaker depth (compared here by concept only); Part 12 owns cost, security and system design in depth; Book 1 owns ML theory; Book 2 owns LLM serving, RAG and the use of Azure OpenAI or Gemini; Book 3 owns SQL; Book 6 owns product and business. This part owns the managed Azure ML and Vertex AI services as used to train, register, deploy and govern models, and how to compare, choose between and move across clouds; where a question touches another part it says so and stays at service level.

Evidence limits: WebFetch of learn.microsoft.com failed (getaddrinfo ENOTFOUND), so no vendor page was opened and every external source is a WebSearch snippet only (see research_notes/Book4_Part11_sources.md). No page was found that reports exact Azure ML or Vertex AI questions asked by a named company, so 'Asked at' tags name source types (prep-site question lists, vendor docs, comparison articles, job-posting patterns, certification-style families), not verified company reports. Execution limit: no Azure or Google credentials exist and none were used. In fresh venvs under /tmp/claude-0/b11p11 (Python 3.13.17) pip installed azure-ai-ml 1.35.2, azure-identity 1.26.0 (azure-storage-blob 12.31.0, later downgraded to 12.19.0 when mlflow 3.17.2 and azureml-mlflow 1.60.0 were added), google-cloud-aiplatform 1.165.1, google-cloud-storage 3.17.1, kfp 2.17.3, kfp-pipeline-spec 2.17.3 and google-cloud-pipeline-components 2.22.0, gcp-storage-emulator 2026.7.19 (own venv), and npm installed azurite 3.37.0 (node v22.22.0, npm 10.9.4). Ran offline and for real: Azure SDK v2 object construction (Environment, command job, dsl.pipeline, ManagedOnlineEndpoint, ManagedOnlineDeployment, AmlCompute, Data, Model, BatchEndpoint, Workspace entity, automl.classification, sweep with Bandit policy), load_job, load_component, load_online_endpoint, load_online_deployment and load_environment on YAML with the SDK's offline _validate() (a misspelt key raised ValidationError 'Unknown field'; endpoint, deployment and environment entities have no _validate); DefaultAzureCredential constructs but get_token fails with no credentials; MLClient(credential=None) raises ValueError; mlflow with the azureml:// tracking URI scheme accepted and a real run logged to a local sqlite store (the plain file store is gated behind MLFLOW_ALLOW_FILE_STORE in mlflow 3.17.2); Azurite blob emulator upload and download with the public development account key through azure-storage-blob; KFP compile to JSON and YAML for a two-component pipeline and for google-cloud-pipeline-components CustomTrainingJobOp and EndpointCreateOp, the KFP local SubprocessRunner (add(1,2) gave 3), Vertex CustomJobSpec proto built and printed with to_json, gcp-storage-emulator accepting google-cloud-storage writes and reads through STORAGE_EMULATOR_HOST, and gcloud 570.0.0 help text. Findings: constructing aiplatform.PipelineJob, CustomJob or Endpoint without init and credentials fails (GoogleAuthError for project, then DefaultCredentialsError); with init plus google.auth AnonymousCredentials the objects build offline, CustomJob and HyperparameterTuningJob build, but PipelineJob.submit tried a real Cloud Storage call and returned 400 for a too-short bucket name and 401 for the API, so anonymous calls reached public Google endpoints and were refused; CustomJob takes service_account and network at run or submit, not in the constructor; azure hosts were refused by the sandbox proxy (management.azure.com connect_rejected). NOT executed: every real Azure or Google call, workspaces, projects, jobs, pipelines, endpoints, quotas, Regions, networking, IAM and RBAC enforcement, AutoML, Responsible AI dashboard, monitoring, Feature Store, BigQuery ML, Azure OpenAI and Gemini, the az CLI and az ml extension (not installed), and all prices. Azurite and gcp-storage-emulator mock storage APIs only: they do not model Entra, IAM, private networking or consistency. Write cloud behaviour from official docs, hedge as 'check current docs', give no prices, and label what ran against what.

---

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

### Q19 ⭐⭐ 🟡 Vertex AI Feature Store versus feature management in Azure ML: the current Vertex design (BigQuery as the offline source, feature groups and feature views, online serving through Bigtable or optimized online serving), the deprecation dates published for the legacy store and optimized online serving, and what a migration means. Part 9 owns feature-store concepts: cover only the managed-service choices, sync modes and the risk of building on a deprecated service. Check the docs-deprecations page the snippets point to and state that nothing was run.
**Asked at:** GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs')
**Say this first (1 line):** Vertex AI Feature Store today means BigQuery as the offline source plus feature groups and feature views synced to online serving (Bigtable-backed is the recommended path), the legacy store and optimized online serving carry published deprecation dates, and Azure ML has a separate managed feature store workspace, so I never start new work on a deprecated service.

**Then explain:**
- **Vertex current design:** features live in BigQuery tables or views. A feature group points at the BigQuery source. A feature view picks features from groups and syncs them to an online store on a schedule (cron) or manually. Check current docs for exact class names, they have changed.
- **Legacy store:** the old Feature Store (Legacy) and "optimized" online serving were announced as deprecated. From the search snippets of the deprecations page (page not opened, check current docs): deprecated 17 Feb 2026, no new features from 17 May 2026, sunset 17 Feb 2027. The pattern matters more than the dates: managed services get retired, so you keep an exit path.
- **Migration means:** new feature groups and views over the BigQuery source, re-sync to the new online store, switch the serving client to the new read API, dual-read to compare values, then retire the old store. Old online values are not copied for you, you rebuild them from the offline source.
- **Azure side:** a managed feature store is its own workspace type. You define a feature store entity, a feature set (with a transformation spec) and materialise to offline and online stores. SDK shape: `FeatureStore`, `FeatureStoreEntity`, `FeatureSet`. Not one-to-one with Vertex, check current docs for status.
- **Failure modes:** online and offline values drift if sync is slow, a sync schedule that is too rare serves stale features, a point-in-time-wrong join leaks the future (Part 9 owns that), and building on a deprecated service means a forced migration on someone else's calendar.

**Example:** a fraud team has features in BigQuery and online serving on the legacy store. Today is 2026-10-26. By the snippet dates the store is past its "no new features" mark, so the checker below says HIGH: plan the migration this quarter. A design on Bigtable-backed serving says ok. Hand check: 26 Oct 2026 is after 17 May 2026 and before 17 Feb 2027, so HIGH, not BLOCKER.

**Code:** two scripts, run with two different venvs (gcp and az). Nothing was created in any cloud.
```python
# ---- q19_gcp_featurestore.py ----
"""Q19 Vertex side: FeatureView proto offline + deprecation-clock checker. No network."""
import warnings; warnings.filterwarnings("ignore")
from datetime import date
import importlib.metadata as md
from google.cloud.aiplatform_v1beta1.types import FeatureView
print("google-cloud-aiplatform", md.version("google-cloud-aiplatform"))

# Current design: a FeatureView syncs from a BigQuery source on a cron schedule.
fv = FeatureView(
    big_query_source=FeatureView.BigQuerySource(
        uri="bq://my-proj.fs_demo.user_features", entity_id_columns=["user_id"]),
    sync_config=FeatureView.SyncConfig(cron="0 */6 * * *"),
)
print(FeatureView.to_json(fv, indent=None))

# Deprecation clock. Dates are from search snippets of the docs-deprecations page, NOT opened.
SNIPPET_DATES = {"deprecated": date(2026, 2, 17), "no_new_features": date(2026, 5, 17), "sunset": date(2027, 2, 17)}
LEGACY = {"legacy_featurestore", "optimized_online_serving"}

def risk(design: dict, today: date) -> str:
    uses = design.get("online_serving")
    if uses not in LEGACY:
        return "ok: not on the legacy services (still check current docs)"
    if today >= SNIPPET_DATES["sunset"]:
        return "BLOCKER: past the snippet sunset date, migrate now"
    if today >= SNIPPET_DATES["no_new_features"]:
        return "HIGH: no new features expected, plan the migration this quarter"
    if today >= SNIPPET_DATES["deprecated"]:
        return "MEDIUM: deprecated, do not start new work on it"
    return "LOW: not deprecated yet by the snippet dates"

for d in [{"online_serving": "legacy_featurestore"}, {"online_serving": "bigtable"},
          {"online_serving": "optimized_online_serving"}]:
    for t in (date(2026, 1, 1), date(2026, 10, 26), date(2027, 3, 1)):
        print(t, d["online_serving"], "->", risk(d, t))

# ---- q19_azure_featurestore.py ----
"""Q19 Azure side: managed feature store entities built offline (nothing is created)."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from azure.ai.ml.entities import FeatureStore, FeatureStoreEntity, FeatureSet, FeatureSetSpecification, DataColumn
print("azure-ai-ml", md.version("azure-ai-ml"))
fs = FeatureStore(name="fs-demo", location="centralindia")
print(type(fs).__name__, fs.name, fs.location)
ent = FeatureStoreEntity(name="account", version="1", index_columns=[DataColumn(name="accountID", type="string")], stage="Development")
print(type(ent).__name__, ent.name, ent.version, [c.name for c in ent.index_columns])
fset = FeatureSet(name="txn_agg", version="1", entities=["azureml:account:1"],
                  specification=FeatureSetSpecification(path="./featureset_spec"), stage="Development")
print(type(fset).__name__, fset.name, fset.version, fset.entities)
```

**Output (my run):** `python -I` in venvs with google-cloud-aiplatform 1.165.1 and azure-ai-ml 1.35.2. Proto and entity objects were built offline. Not executed: the docs-deprecations page (the snippets were the only source, WebFetch failed earlier), any real Feature Store, BigQuery, Bigtable, sync job or Azure materialisation. Dates are from snippets and hedged.
```text
$ python -I q19_gcp_featurestore.py
google-cloud-aiplatform 1.165.1
{"bigQuerySource": {"uri": "bq://my-proj.fs_demo.user_features", "entityIdColumns": ["user_id"]}, "syncConfig": {"cron": "0 */6 * * *"}, "name": "", "etag": "", "labels": {}, "serviceAgentType": 0, "serviceAccountEmail": "", "satisfiesPzs": false, "satisfiesPzi": false}
2026-01-01 legacy_featurestore -> LOW: not deprecated yet by the snippet dates
2026-10-26 legacy_featurestore -> HIGH: no new features expected, plan the migration this quarter
2027-03-01 legacy_featurestore -> BLOCKER: past the snippet sunset date, migrate now
2026-01-01 bigtable -> ok: not on the legacy services (still check current docs)
2026-10-26 bigtable -> ok: not on the legacy services (still check current docs)
2027-03-01 bigtable -> ok: not on the legacy services (still check current docs)
2026-01-01 optimized_online_serving -> LOW: not deprecated yet by the snippet dates
2026-10-26 optimized_online_serving -> HIGH: no new features expected, plan the migration this quarter
2027-03-01 optimized_online_serving -> BLOCKER: past the snippet sunset date, migrate now

$ python -I q19_azure_featurestore.py
azure-ai-ml 1.35.2
FeatureStore fs-demo centralindia
FeatureStoreEntity account 1 ['accountID']
FeatureSet txn_agg 1 ['azureml:account:1']
```

**Follow-ups:**
- *Why not just wait until the sunset date?* The cost is migration under deadline plus no new features. Start with a dual-read pilot now.
- *Where do features come from if not the store?* From the BigQuery tables or views, the store is a serving copy. Keep the transformation in version-controlled SQL or code.
- *Do I even need a managed store?* Only if online low-latency lookups need shared, consistent features. Otherwise a batch table is enough (Part 9).

**Common mistakes:**
- Starting a new project on a service whose docs page says deprecated.
- Quoting deprecation dates from memory or a blog instead of the vendor page on the day.
- Forgetting that online values must be re-synced after migration.
- Treating the Azure feature store as a drop-in for Vertex.

### Q20 ⭐⭐ 🟡 Model monitoring services: Vertex AI Model Monitoring (training-serving skew and prediction drift, baseline, sampling rate, schedule, alert channels) and Azure ML model monitoring (signals, thresholds, a monitor schedule), at the configuration level only. Part 8 owns drift maths and alerting design. Build the Azure monitor entities offline if the import works, write a config checker for a monitoring spec (baseline set, sample rate in range, alert target present), and list what each service does not do for you (labels, business metrics, retraining).
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs') | Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs')
**Say this first (1 line):** Both services compare production data to a baseline on a schedule, on a sample, against thresholds, and send an alert; neither one gives you labels, business metrics or retraining, so those stay your job.

**Then explain:**
- **Vertex Model Monitoring (v1 objects):** baseline is the training dataset (BigQuery, Cloud Storage) for skew, or the previous window for drift. You set per-feature thresholds, a sampling rate for logged requests, a schedule interval, and an alert config (email, Cloud Monitoring channels). There is also a newer monitoring design; check current docs which one your project should use, I could not confirm its status.
- **Azure ML model monitoring:** a monitor schedule runs a monitor definition on Spark compute. The definition has a target (endpoint deployment), signals (data drift, data quality, prediction drift, feature attribution drift, model performance) with metric thresholds, and an alert notification. Production data comes from collected inference data.
- **Not done for you:** collecting ground truth, computing business KPIs, deciding the retrain trigger, running the retrain, rollback. Delayed labels mean model performance signals lag (Part 8).
- **Failure modes:** no baseline means nothing to compare, a sample rate that is too low misses rare classes, thresholds copied from a blog fire daily and get muted, alerts to a mailbox nobody reads, schema change in logged data breaks the job silently.

**Example:** daily Azure monitor with drift, quality and prediction-drift signals and one alert email: built offline below. The checker flags a spec with an empty baseline, sample rate 1.5, no alert target and no thresholds, and passes the good spec. Hand check: 4 problems in the bad spec (the schedule is present).

**Code:** Azure and Vertex configuration objects plus a config checker. Nothing was sent.
```python
# ---- q20_monitoring.py ----
"""Q20: monitoring configs offline. Azure MonitorDefinition/MonitorSchedule built (not created);
Vertex ModelMonitoringObjectiveConfig proto printed by the gcp venv separately (q20_vertex.py)."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from azure.ai.ml.entities import (MonitorDefinition, MonitorSchedule, MonitoringTarget, DataDriftSignal,
    DataQualitySignal, PredictionDriftSignal, AlertNotification, ServerlessSparkCompute, RecurrenceTrigger,
    RecurrencePattern, PredictionDriftMetricThreshold)
print("azure-ai-ml", md.version("azure-ai-ml"))
md_ = MonitorDefinition(
    compute=ServerlessSparkCompute(instance_type="standard_e4s_v3", runtime_version="3.4"),
    monitoring_target=MonitoringTarget(ml_task="classification", endpoint_deployment_id="azureml:my-ep:blue"),
    monitoring_signals={"drift": DataDriftSignal(), "quality": DataQualitySignal(), "pred": PredictionDriftSignal(metric_thresholds=PredictionDriftMetricThreshold())},
    alert_notification=AlertNotification(emails=["mlops@example.com"]),
)
sched = MonitorSchedule(name="daily-monitor", trigger=RecurrenceTrigger(frequency="day", interval=1,
        schedule=RecurrencePattern(hours=3, minutes=0)), create_monitor=md_)
print(type(sched).__name__, sched.name, sorted(md_.monitoring_signals), md_.alert_notification.emails)

# ---- config checker (works on a plain dict so it also fits a Vertex-style spec) ----
def check_monitor(spec: dict) -> list[str]:
    errs = []
    if not spec.get("baseline"): errs.append("no baseline set (training data or reference window)")
    r = spec.get("sample_rate")
    if r is None or not (0 < r <= 1): errs.append(f"sample_rate {r!r} not in (0, 1]")
    if not spec.get("alert_targets"): errs.append("no alert target (email, channel, webhook)")
    if not spec.get("schedule"): errs.append("no schedule")
    if not spec.get("thresholds"): errs.append("no thresholds: signals would never fire")
    return errs

good = {"baseline": "train_v7", "sample_rate": 0.1, "alert_targets": ["mlops@example.com"],
        "schedule": "daily", "thresholds": {"psi": 0.2}}
bad = {"baseline": "", "sample_rate": 1.5, "alert_targets": [], "schedule": "daily", "thresholds": {}}
for name, s in [("good", good), ("bad", bad)]:
    print(name, "->", check_monitor(s) or "OK")

# ---- q20_vertex.py ----
"""Q20 Vertex side: ModelMonitoringObjectiveConfig proto built offline (v1beta1 types); nothing sent."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from google.cloud.aiplatform_v1.types import (ModelDeploymentMonitoringObjectiveConfig, ModelMonitoringObjectiveConfig,
    ModelMonitoringAlertConfig, SamplingStrategy, ThresholdConfig)
print("google-cloud-aiplatform", md.version("google-cloud-aiplatform"))
obj = ModelMonitoringObjectiveConfig(
    training_dataset=ModelMonitoringObjectiveConfig.TrainingDataset(
        bigquery_source={"input_uri": "bq://my-proj.ds.train"}, target_field="label"),
    training_prediction_skew_detection_config=ModelMonitoringObjectiveConfig.TrainingPredictionSkewDetectionConfig(
        skew_thresholds={"age": ThresholdConfig(value=0.3)}),
    prediction_drift_detection_config=ModelMonitoringObjectiveConfig.PredictionDriftDetectionConfig(
        drift_thresholds={"age": ThresholdConfig(value=0.3)}))
dep = ModelDeploymentMonitoringObjectiveConfig(deployed_model_id="1234", objective_config=obj)
sampling = SamplingStrategy(random_sample_config=SamplingStrategy.RandomSampleConfig(sample_rate=0.2))
alert = ModelMonitoringAlertConfig(email_alert_config=ModelMonitoringAlertConfig.EmailAlertConfig(user_emails=["mlops@example.com"]))
print("sample_rate", sampling.random_sample_config.sample_rate, "| emails", list(alert.email_alert_config.user_emails))
print("skew thresholds:", {k: v.value for k, v in obj.training_prediction_skew_detection_config.skew_thresholds.items()})
print("types:", type(dep).__name__, type(obj).__name__)
```

**Output (my run):** azure-ai-ml 1.35.2 (az venv) and google-cloud-aiplatform 1.165.1 (gcp venv), `python -I`. Entities and protos built offline; no monitor was created. Not executed: any scheduled monitor run, Spark compute, Cloud Monitoring alerts. The Azure `PredictionDriftSignal` needed explicit `metric_thresholds` (my first run raised a TypeError), which shows constructor shapes change between versions.
```text
$ python -I q20_monitoring.py
azure-ai-ml 1.35.2
MonitorSchedule daily-monitor ['drift', 'pred', 'quality'] ['mlops@example.com']
good -> OK
bad -> ['no baseline set (training data or reference window)', 'sample_rate 1.5 not in (0, 1]', 'no alert target (email, channel, webhook)', 'no thresholds: signals would never fire']

$ python -I q20_vertex.py
google-cloud-aiplatform 1.165.1
sample_rate 0.2 | emails ['mlops@example.com']
skew thresholds: {'age': 0.3}
types: ModelDeploymentMonitoringObjectiveConfig ModelMonitoringObjectiveConfig
```

**Follow-ups:**
- *Who decides the threshold?* Start from history of normal days, review after a month. The drift maths is in Part 8.
- *Skew versus drift?* Skew is training versus serving now, drift is serving now versus serving earlier.
- *What triggers retraining?* A policy you write; the service only alerts.

**Common mistakes:**
- Turning on monitoring with no baseline or no owner for the alert.
- Sampling 100 percent on a busy endpoint and being surprised by log volume (cost depth: Part 12).
- Calling drift an accuracy drop. It is a warning, not proof.

### Q21 ⭐⭐ 🟡 AutoML in Azure ML versus Vertex AI AutoML: supported task types, what you give it (an MLTable or a managed dataset), limits and timeouts, primary metric, explainability and guardrails, and when you refuse to use it (leakage, tiny data, strict latency, need for custom features). Build an Azure automl.classification job offline with limits set, print its settings, and say what a trained AutoML model gives you for registry and deployment. Book 1 owns ML theory.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Certification-style question families (Microsoft DP-100 study guide and its replacement AI-300 as reported by third-party sites, Google Cloud Professional Machine Learning Engineer exam-prep listings; mentioned as a source type only, no exam questions reproduced; skills lists conflicted between sources, so verify on the vendor pages)
**Say this first (1 line):** AutoML tries many models and preprocessing for you under a time and trial budget, which is a fast baseline for tabular data, but I refuse it when leakage risk, tiny data, strict latency or custom features matter more than speed.

**Then explain:**
- **Azure ML AutoML:** SDK v2 `automl.classification`, `regression`, `forecasting`, plus image and text tasks (check current docs for the exact list). You give it an MLTable data input, a target column, a primary metric, validation (for example cross-validation folds) and limits (total timeout, per-trial timeout, max trials, concurrency, early termination). You can allow or block algorithms and ask for ONNX-compatible models.
- **Vertex AI AutoML:** a managed dataset or BigQuery table in, an optimization objective (for example `maximize-au-roc`) and a node-hour budget out. Supported data types and task names move between releases, check current docs.
- **What you get back:** a trained model with the best run, explainability and a model object you register and deploy like any other. Check the generated model's inputs: AutoML does its own featurization, so serving must apply the same one.
- **Refuse it when:** the target leaks (a column that is only known after the outcome), you have a few hundred rows, latency budget is tight and the winner is a big ensemble, regulators need a model you can fully describe, or the value is in hand-built features.
- **Failure modes:** leaky column wins by a huge margin (a warning sign, not a success), time budget too short to finish, a random split on time-ordered data, and treating the leaderboard as the final test.

**Example:** churn data with 3-fold cross-validation, primary metric AUC weighted, 60 minutes total, 10 per trial, 20 trials, 2 in parallel. Hand check: 20 trials at 2 in parallel is about 10 rounds, so up to roughly 100 minutes if every trial used its full 10 minutes, which is more than the 60-minute cap. The cap wins, so not every trial may run. Raise the timeout or cut the trials.

**Code:** both jobs built offline, nothing submitted.
```python
# ---- q21_automl_azure.py ----
"""Q21 Azure: automl.classification built offline. Nothing submitted."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from azure.ai.ml import automl, Input
print("azure-ai-ml", md.version("azure-ai-ml"))
j = automl.classification(compute="cpu-cluster", experiment_name="churn-automl",
        training_data=Input(type="mltable", path="./train_mltable"), target_column_name="churned",
        primary_metric="AUC_weighted", n_cross_validations=3, enable_model_explainability=True)
j.set_limits(timeout_minutes=60, trial_timeout_minutes=10, max_trials=20, max_concurrent_trials=2, enable_early_termination=True)
j.set_training(allowed_training_algorithms=["LightGBM", "LogisticRegression"], enable_onnx_compatible_models=True)
print("task:", j.task_type, "| metric:", j.primary_metric, "| target:", j.target_column_name)
L = j.limits
print("limits:", dict(timeout_minutes=L.timeout_minutes, trial_timeout_minutes=L.trial_timeout_minutes,
      max_trials=L.max_trials, max_concurrent_trials=L.max_concurrent_trials, early=L.enable_early_termination))
print("allowed algos:", j.training.allowed_training_algorithms, "| onnx:", j.training.enable_onnx_compatible_models)

# ---- q21_automl_vertex.py ----
"""Q21 Vertex: AutoMLTabularTrainingJob constructed offline with anonymous credentials. run() NOT called."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from google.auth.credentials import AnonymousCredentials
import google.cloud.aiplatform as aip
print("google-cloud-aiplatform", md.version("google-cloud-aiplatform"))
aip.init(project="demo-proj", location="asia-south1", credentials=AnonymousCredentials())
job = aip.AutoMLTabularTrainingJob(display_name="churn-automl", optimization_prediction_type="classification",
        optimization_objective="maximize-au-roc")
print(type(job).__name__, "| objective:", job._optimization_objective, "| type:", job._optimization_prediction_type)
print("run() signature has budget arg:", "budget_milli_node_hours" in job.run.__code__.co_varnames)
```

**Output (my run):** azure-ai-ml 1.35.2 and google-cloud-aiplatform 1.165.1, `python -I`. Objects constructed offline; the Vertex training job was not run and the Azure job was not submitted. Not executed: any AutoML training, explainability output, registry or deployment of an AutoML model. I did not run the SDK featurization or validation printing beyond what is shown.
```text
$ python -I q21_automl_azure.py
azure-ai-ml 1.35.2
task: TaskType.CLASSIFICATION | metric: ClassificationPrimaryMetrics.AUC_WEIGHTED | target: churned
limits: {'timeout_minutes': 60, 'trial_timeout_minutes': 10, 'max_trials': 20, 'max_concurrent_trials': 2, 'early': True}
allowed algos: [<ClassificationModels.LIGHT_GBM: 'LightGBM'>, <ClassificationModels.LOGISTIC_REGRESSION: 'LogisticRegression'>] | onnx: True

$ python -I q21_automl_vertex.py
google-cloud-aiplatform 1.165.1
AutoMLTabularTrainingJob | objective: maximize-au-roc | type: classification
run() signature has budget arg: True
```

**Follow-ups:**
- *How do you stop leakage?* Split by time or by group first, drop post-outcome columns, check feature importance for suspicious winners.
- *Is AutoML a replacement for a data scientist?* No. It is a baseline and a time saver.
- *Where does it fit in the registry?* The output is a model like another: register it, tag the data version and the job id.

**Common mistakes:**
- Trusting the leaderboard without a final holdout.
- Letting AutoML pick features from an ID or timestamp column.
- Forgetting that the deployed model needs the same featurization.

### Q22 ⭐⭐ 🟡 Hyperparameter tuning as a service: Azure ML sweep jobs (search space, sampling algorithm, primary metric and goal, early termination such as Bandit, trial limits) versus Vertex AI HyperparameterTuningJob and Vizier (metric spec, parameter spec, trial counts, parallel trials, Bayesian search). Build a sweep job and a HyperparameterTuningJob offline, show both specs, and explain why parallel trials and Bayesian search pull against each other. Book 1 owns tuning theory.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs')
**Say this first (1 line):** Both clouds run a hyperparameter search as a managed job of trials over your training code, with a metric, a search space and trial limits; and more parallel trials means faster wall-clock but a Bayesian search learns from fewer finished results.

**Then explain:**
- **Azure ML sweep job:** you take a command job, replace inputs with a search space (`Uniform`, `Choice` and so on), call `.sweep()` with sampling algorithm (random, grid, bayesian), primary metric and goal, then set limits (total trials, concurrent trials, timeout). Early termination (Bandit, median stopping, truncation) is an optional policy. The docs say Bayesian sampling does not support early termination policies (check current docs), so I paired Bandit with random sampling.
- **Vertex AI HyperparameterTuningJob (Vizier):** a `custom_job` is the trial template, `metric_spec` has the metric and goal, `parameter_spec` has Double, Integer, Discrete or Categorical parameters with a scale, and `max_trial_count` and `parallel_trial_count` set the budget. If the algorithm is unset the service picks its default, which is Bayesian-style optimization, check current docs.
- **Your script must report the metric:** in Azure, log the metric the sweep names (MLflow); in Vertex, report through the hypertune helper library or the documented mechanism, otherwise trials finish with no value.
- **Why parallel and Bayesian fight:** a Bayesian method proposes the next point from finished trials. If P trials run at once, a new trial is proposed with up to P-1 results still missing. With P equal to the trial count it is just random search.
- **Failure modes:** metric name mismatch (all trials look failed), too-wide log-scale ranges, each trial paying cold start, tuning on the test set, and quota limiting real concurrency below what you set.

**Example:** 20 trials. Parallel 1: trial 10 sees 9 finished results. Parallel 4: trial 10 sees 6. Parallel 20: trial 10 sees 0. Hand check: trial i sees about i minus P finished results, never below 0. With parallel 4 the first 4 trials are proposed blind.

**Code:** Azure sweep, Vertex tuning job, plus the small count of what each trial can see.
```python
# ---- q22_tuning.py ----
"""Q22 Azure sweep job offline + the parallel-vs-Bayesian arithmetic (pure Python)."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from azure.ai.ml import command
from azure.ai.ml.sweep import Uniform, Choice, BanditPolicy
print("azure-ai-ml", md.version("azure-ai-ml"))
base = command(code=".", command="python train.py --lr ${{inputs.lr}} --depth ${{inputs.depth}}",
               inputs={"lr": 0.1, "depth": 4}, environment="azureml:train-env:1", compute="cpu-cluster")
sw = base(lr=Uniform(min_value=0.001, max_value=0.1), depth=Choice(values=[3, 4, 6])).sweep(
        sampling_algorithm="bayesian", primary_metric="auc", goal="maximize")
sw.set_limits(max_total_trials=20, max_concurrent_trials=4, timeout=3600)
print(type(sw).__name__, "| sampling:", sw.sampling_algorithm, "| goal:", sw.objective.goal, "| metric:", sw.objective.primary_metric)
print("limits: total", sw.limits.max_total_trials, "concurrent", sw.limits.max_concurrent_trials)
print("search space:", {k: type(v).__name__ for k, v in sw.search_space.items()})

# Bandit early termination goes on a random-sampling sweep (docs say Bayesian does not support
# early-termination policies: check current docs).
sw2 = base(lr=Uniform(min_value=0.001, max_value=0.1), depth=Choice(values=[3, 4, 6])).sweep(
        sampling_algorithm="random", primary_metric="auc", goal="maximize")
sw2.set_limits(max_total_trials=20, max_concurrent_trials=4)
sw2.early_termination = BanditPolicy(slack_factor=0.1, evaluation_interval=1, delay_evaluation=2)
print("sweep2:", sw2.sampling_algorithm, "+", type(sw2.early_termination).__name__, "slack", sw2.early_termination.slack_factor)

# Why parallel trials and Bayesian search pull against each other: a Bayesian suggester only learns from
# FINISHED trials. With P trials running at once, trial i (1-based) starts after at most i-P finished.
def informed_trials(total, parallel):
    return [max(0, i - parallel) for i in range(1, total + 1)]   # finished results visible when trial i is proposed
for p in (1, 4, 20):
    seen = informed_trials(20, p)
    print(f"parallel={p:2d}: results seen by trial 5={seen[4]}, trial 10={seen[9]}, trial 20={seen[19]}, trials proposed blind={sum(1 for x in seen if x==0)}")

# ---- q22_vertex_hpt.py ----
"""Q22 Vertex HyperparameterTuningJob built offline (anonymous creds). run() NOT called."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from google.auth.credentials import AnonymousCredentials
import google.cloud.aiplatform as aip
from google.cloud.aiplatform import hyperparameter_tuning as hpt
print("google-cloud-aiplatform", md.version("google-cloud-aiplatform"))
aip.init(project="demo-proj", location="asia-south1", staging_bucket="gs://demo-stage-bkt", credentials=AnonymousCredentials())
cj = aip.CustomJob(display_name="trial-template", worker_pool_specs=[{"machine_spec": {"machine_type": "n1-standard-4"},
        "replica_count": 1, "container_spec": {"image_uri": "asia-south1-docker.pkg.dev/demo-proj/repo/train:1"}}])
h = aip.HyperparameterTuningJob(display_name="hpt", custom_job=cj, metric_spec={"auc": "maximize"},
        parameter_spec={"lr": hpt.DoubleParameterSpec(min=0.001, max=0.1, scale="log"),
                        "depth": hpt.DiscreteParameterSpec(values=[3, 4, 6], scale=None)},
        max_trial_count=20, parallel_trial_count=4, search_algorithm=None)
spec = h._gca_resource.trial_job_spec
print(type(h).__name__, "| max_trials", h._gca_resource.max_trial_count, "| parallel", h._gca_resource.parallel_trial_count)
print("metrics:", [(m.metric_id, m.goal.name) for m in h._gca_resource.study_spec.metrics])
print("params:", [(p.parameter_id, p.scale_type.name) for p in h._gca_resource.study_spec.parameters])
print("algorithm (unset = service default):", h._gca_resource.study_spec.algorithm.name)
```

**Output (my run):** azure-ai-ml 1.35.2 and google-cloud-aiplatform 1.165.1, `python -I`; objects built offline (Vertex with anonymous credentials, `run()` not called). The informed-trials count is my simplified model of a sequential suggester, not a measurement of Vizier or Azure internals. Not executed: any trial, quota check or search result.
```text
$ python -I q22_tuning.py
azure-ai-ml 1.35.2
Sweep | sampling: bayesian | goal: maximize | metric: auc
limits: total 20 concurrent 4
search space: {'lr': 'Uniform', 'depth': 'Choice'}
sweep2: random + BanditPolicy slack 0.1
parallel= 1: results seen by trial 5=4, trial 10=9, trial 20=19, trials proposed blind=1
parallel= 4: results seen by trial 5=1, trial 10=6, trial 20=16, trials proposed blind=4
parallel=20: results seen by trial 5=0, trial 10=0, trial 20=0, trials proposed blind=20

$ python -I q22_vertex_hpt.py
google-cloud-aiplatform 1.165.1
HyperparameterTuningJob | max_trials 20 | parallel 4
metrics: [('auc', 'MAXIMIZE')]
params: [('lr', 'UNIT_LOG_SCALE'), ('depth', 'SCALE_TYPE_UNSPECIFIED')]
algorithm (unset = service default): ALGORITHM_UNSPECIFIED
```

**Follow-ups:**
- *What parallelism would you pick?* A small share of the trial budget (for example 4 of 20), then check results. Do not pick it from a rule of thumb alone.
- *When is random search enough?* Few parameters, cheap trials, or when you run many in parallel.
- *Why log scale for learning rate?* Good values span orders of magnitude.

**Common mistakes:**
- Setting concurrency above the cluster's real node count so trials queue.
- Reporting the metric under a different name than the spec.
- Reading a best-trial score as the expected production score.

### Q23 ⭐⭐ 🟡 Azure ML network isolation: workspace public_network_access, a private endpoint for inbound access, the managed virtual network for outbound control (allow internet outbound versus allow only approved outbound, outbound rules, private endpoints to Storage, Key Vault and Container Registry), and securing a managed online endpoint. Build a Workspace entity with public access disabled offline, write a checker for a network config, and name the deployment-time RBAC that managed-network creation needs. Part 12 owns security design in depth.
**Asked at:** Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs
**Say this first (1 line):** Close the front door with public_network_access disabled plus a private endpoint, control the back door with the managed virtual network (allow only approved outbound, private endpoints to Storage, Key Vault and Container Registry), and make sure whoever creates it has the RBAC to build private endpoints.

**Then explain:**
- **Inbound:** set the workspace `public_network_access` to Disabled and add a private endpoint in your own VNet. Users and CI then reach the workspace only through that network (VPN, ExpressRoute or a jump host).
- **Outbound:** the managed virtual network is created and run by the service for compute. Isolation modes as named in the SDK: disabled, allow internet outbound, allow only approved outbound (check current docs for names). In the strict mode you add outbound rules: FQDN rules (for example a package mirror) and private endpoint rules to the workspace's Storage, Key Vault and Container Registry.
- **Online endpoints:** a managed online endpoint has its own public network access setting; set it to disabled so scoring is private as well (check current docs for the current property and for the workspace-level interplay).
- **RBAC for creating it:** the identity that provisions the managed network needs permission to create private endpoints and to read the target resources (from snippets: rights on the Storage account and others, Reader on storage private endpoints; the exact role list is version-specific, check current docs).
- **Failure modes:** a Docker image pull or `pip install` fails because outbound is closed and no rule exists, workspace is private but the CI runner is on the public internet, DNS for private endpoints not resolved from your network, and "allow internet outbound" left on forever "for now".

**Example:** a bank GCC sets Disabled public access, strict outbound, three private endpoint rules and one FQDN rule for an internal package mirror. The checker passes it, and fails a sample with public access Enabled, internet outbound and only a storage rule. Hand check: the bad sample has 7 findings (public access, no inbound private endpoint, internet outbound, key vault and registry rules missing, public endpoint, missing deployer RBAC).

**Code:** Workspace entity with a managed network built offline, and a checker.
```python
# ---- q23_azure_network.py ----
"""Q23: Workspace with managed network + checker, offline. Nothing is created."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from azure.ai.ml.entities import Workspace, ManagedNetwork, IsolationMode, FqdnDestination, PrivateEndpointDestination
print("azure-ai-ml", md.version("azure-ai-ml"))
mn = ManagedNetwork(isolation_mode=IsolationMode.ALLOW_ONLY_APPROVED_OUTBOUND, outbound_rules=[
    FqdnDestination(name="pypi", destination="pypi.org"),
    PrivateEndpointDestination(name="pe-storage", service_resource_id="/subscriptions/0000/resourceGroups/rg/providers/Microsoft.Storage/storageAccounts/stdemo", subresource_target="blob", spark_enabled=False)])
ws = Workspace(name="ws-secure", location="centralindia", public_network_access="Disabled", managed_network=mn)
print(type(ws).__name__, ws.location, "public:", ws.public_network_access, "| mode:", ws.managed_network.isolation_mode,
      "| rules:", [(r.name, type(r).__name__) for r in ws.managed_network.outbound_rules])

def check_network(cfg: dict) -> list[str]:
    f = []
    if cfg.get("public_network_access") != "Disabled": f.append("workspace public_network_access is not Disabled")
    if not cfg.get("private_endpoint_inbound"): f.append("no private endpoint for inbound access to the workspace")
    mode = cfg.get("isolation_mode")
    if mode == "disabled": f.append("managed network off: outbound is uncontrolled")
    if mode == "allow_internet_outbound": f.append("internet outbound allowed: exfiltration path open (ok only with a written reason)")
    for dep in ("storage", "key_vault", "container_registry"):
        if dep not in cfg.get("private_endpoint_outbound", []): f.append(f"no outbound private endpoint rule for {dep}")
    for ep in cfg.get("online_endpoints", []):
        if ep.get("public_network_access") != "disabled": f.append(f"endpoint {ep['name']} is public")
    if not cfg.get("deployer_can_create_private_endpoints"): f.append("deployer lacks RBAC to create private endpoints (managed network creation fails)")
    return f

good = {"public_network_access": "Disabled", "private_endpoint_inbound": True, "isolation_mode": "allow_only_approved_outbound",
        "private_endpoint_outbound": ["storage", "key_vault", "container_registry"],
        "online_endpoints": [{"name": "fraud-ep", "public_network_access": "disabled"}], "deployer_can_create_private_endpoints": True}
bad = {"public_network_access": "Enabled", "isolation_mode": "allow_internet_outbound", "private_endpoint_outbound": ["storage"],
       "online_endpoints": [{"name": "fraud-ep", "public_network_access": "enabled"}]}
for n, c in (("good", good), ("bad", bad)):
    r = check_network(c); print(n, "->", "OK" if not r else ""); [print("   -", x) for x in r]
```

**Output (my run):** azure-ai-ml 1.35.2, `python -I`. The Workspace entity was constructed in memory only. Not executed: workspace creation, private endpoints, DNS, outbound rule provisioning, RBAC evaluation. The checker reads a dict I wrote, it does not read Azure. Security design depth is Part 12.
```text
$ python -I q23_azure_network.py
azure-ai-ml 1.35.2
Workspace centralindia public: Disabled | mode: AllowOnlyApprovedOutbound | rules: [('pypi', 'FqdnDestination'), ('pe-storage', 'PrivateEndpointDestination')]
good -> OK
bad -> 
   - workspace public_network_access is not Disabled
   - no private endpoint for inbound access to the workspace
   - internet outbound allowed: exfiltration path open (ok only with a written reason)
   - no outbound private endpoint rule for key_vault
   - no outbound private endpoint rule for container_registry
   - endpoint fraud-ep is public
   - deployer lacks RBAC to create private endpoints (managed network creation fails)
```

**Follow-ups:**
- *Why not allow internet outbound?* It is an exfiltration path. Use it only for a short, written reason.
- *Where do packages come from then?* A mirror reachable via FQDN or private endpoint rules.
- *How do you test it?* A job that tries `pip install` and a blob read from inside the network.

**Common mistakes:**
- Disabling public access and forgetting the build and CI path.
- Forgetting that Storage, Key Vault and registry each need their own rule.
- Assuming a private workspace means a private endpoint for scoring.

### Q24 ⭐⭐ 🟡 Vertex AI network and perimeter controls: VPC Service Controls perimeters (what they protect against, exfiltration, ingress and egress rules), Private Service Connect interface for custom training and pipelines (network attachment, subnet sizing as documented, default internet access blocked inside a perimeter), private endpoints for online prediction, and restricted Google APIs access. A training job works in a dev project and fails in the perimeter: list what you check in order. Write the checklist as a function over a config dict and run it on two samples. No Google call was made.
**Asked at:** Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs') | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms
**Say this first (1 line):** A job that works in dev and fails in the perimeter is almost always a blocked path, not a bad model: so I check identity first, then perimeter membership, then network attachment, DNS, internet use, data location and rules, and I read the denial in the audit logs.

**Then explain:**
- **VPC Service Controls:** a perimeter around projects and services (such as Vertex AI and Cloud Storage) that blocks calls crossing its edge unless an ingress or egress rule allows them. It protects against data exfiltration with stolen credentials. It does not replace IAM: both must allow.
- **Custom training in a perimeter:** from the snippets, the job's data plane needs extra networking. A Private Service Connect interface (network attachment in your VPC, subnet around /28 is the documented size, check current docs) gives the job a path. Default internet access is blocked inside the perimeter.
- **Restricted Google APIs:** DNS for `*.googleapis.com` should resolve to the restricted VIP so API calls stay inside.
- **Online prediction:** private endpoints (a private network path to the endpoint) instead of the shared public one.
- **Service accounts inside a perimeter** are not covered by my sources: check current docs for how service agents and your job account are treated.
- **Failure modes:** `pip install` and `git clone` silently need the internet, the container image sits in a repository outside the perimeter, the bucket project is outside, a dry-run perimeter hides what an enforced one breaks.

**Example:** the dev project is outside any perimeter, so only API and IAM checks matter and it passes. The prod project is inside: its attachment subnet is a /29, DNS is not on the restricted VIP, the job pip installs from the internet and nothing allows the bucket project. The ordered checklist stops at check 6, and four more fail after it. Hand check: /29 has 8 addresses, a /28 has 16, so "prefix length at most 28" is the test.

**Code:** the checklist as a function over a dict.
```python
# ---- q24_vertex_perimeter.py ----
"""Q24: ordered checklist over a config dict. Pure Python, no Google call. Facts hedged: check current docs."""
import ipaddress

def checklist(c: dict) -> list[tuple[int, str, str]]:
    out = []
    def chk(name, ok, hint): out.append((len(out) + 1, name, "PASS" if ok else "FAIL: " + hint))
    chk("Vertex AI API and Storage API enabled in the project", c["apis_enabled"], "enable the APIs")
    chk("job service account has roles on bucket, image repo, project", c["sa_roles_ok"], "fix IAM first: perimeter is the second wall, not the first")
    chk("project perimeter membership matches the intent", c["project_in_perimeter"] == c["perimeter_expected"], "add project to perimeter (or confirm it is meant to be outside)")
    chk("restricted services include aiplatform and storage consistently", c["services_restricted"], "check the restricted-services list")
    chk("job has a network attachment (PSC interface) when data-plane egress is needed", c["network_attachment"], "create attachment, pass it in the job spec")
    ok_subnet = False
    if c["network_attachment"]:
        ok_subnet = ipaddress.ip_network(c["attachment_subnet"]).prefixlen <= 28   # docs recommend /28 or larger, check current docs
    chk("attachment subnet has room (docs recommend /28; check current docs)", ok_subnet or not c["network_attachment"], "subnet too small")
    chk("DNS resolves googleapis.com names to the restricted VIP", c["restricted_vip_dns"], "add private DNS zone for restricted.googleapis.com")
    chk("no step needs the public internet (pip install, git clone, external API)", not c["needs_internet"], "mirror packages in Artifact Registry or allow egress through a controlled proxy")
    chk("images and data live in-perimeter, or an ingress/egress rule names this identity", c["data_in_perimeter"] or c["egress_rule_for_sa"], "add an egress rule for the job service account and the bucket project")
    chk("denials checked in audit logs (dry-run mode first)", c["audit_logs_read"], "read the VPC-SC violation entries")
    return out

dev = dict(apis_enabled=True, sa_roles_ok=True, project_in_perimeter=False, services_restricted=False, network_attachment=False,
           attachment_subnet="10.0.0.0/24", restricted_vip_dns=False, needs_internet=True, data_in_perimeter=True,
           egress_rule_for_sa=False, audit_logs_read=False, perimeter_expected=False)
prod = dict(dev, perimeter_expected=True, project_in_perimeter=True, services_restricted=True, network_attachment=True, attachment_subnet="10.9.0.0/29",
            restricted_vip_dns=False, data_in_perimeter=False)

def run(cfg):
    rows = checklist(cfg)
    if not cfg["project_in_perimeter"]:       # outside a perimeter, checks 4-10 are not enforced
        rows = rows[:3]
    return rows

for name, cfg in (("dev project (outside perimeter)", dev), ("prod project (inside perimeter)", prod)):
    rows = run(cfg)
    print("==", name, "->", "first failure: #%d" % next((r[0] for r in rows if r[2] != "PASS"), 0) if any(r[2] != "PASS" for r in rows) else "all checks pass")
    for n, what, res in rows: print(f" {n:2d}. {what}: {res}")
```

**Output (my run):** Python 3.13 `python -I`, no Google libraries needed. No Google call was made and no perimeter existed; the checks encode my reading of the doc snippets and a real denial is found in the audit logs (not executed).
```text
$ python -I q24_vertex_perimeter.py
== dev project (outside perimeter) -> all checks pass
  1. Vertex AI API and Storage API enabled in the project: PASS
  2. job service account has roles on bucket, image repo, project: PASS
  3. project perimeter membership matches the intent: PASS
== prod project (inside perimeter) -> first failure: #6
  1. Vertex AI API and Storage API enabled in the project: PASS
  2. job service account has roles on bucket, image repo, project: PASS
  3. project perimeter membership matches the intent: PASS
  4. restricted services include aiplatform and storage consistently: PASS
  5. job has a network attachment (PSC interface) when data-plane egress is needed: PASS
  6. attachment subnet has room (docs recommend /28; check current docs): FAIL: subnet too small
  7. DNS resolves googleapis.com names to the restricted VIP: FAIL: add private DNS zone for restricted.googleapis.com
  8. no step needs the public internet (pip install, git clone, external API): FAIL: mirror packages in Artifact Registry or allow egress through a controlled proxy
  9. images and data live in-perimeter, or an ingress/egress rule names this identity: FAIL: add an egress rule for the job service account and the bucket project
 10. denials checked in audit logs (dry-run mode first): FAIL: read the VPC-SC violation entries
```

**Follow-ups:**
- *First thing you do on a denial?* Read the violation entry in the audit logs; it names the service, identity and rule that was missing.
- *Dry-run mode?* Logs what would be blocked without blocking: use before enforcing.
- *IAM or perimeter first?* IAM, then perimeter, because the perimeter error can hide a missing role.

**Common mistakes:**
- Opening the perimeter wide "to see if it works" and leaving it.
- Forgetting the image repository and the package source.
- Sizing the attachment subnet too small.

### Q25 ⭐⭐ 🟡 CI/CD authentication and deployment for Azure ML and Vertex AI: GitHub Actions or Azure DevOps to Azure ML with a federated service principal or managed identity and az ml CLI v2 commands, versus GitHub Actions or Cloud Build to Vertex AI with Workload Identity Federation and a deployer service account. Why no long-lived keys, what the deployer identity may and may not do, and where the approval gate sits. Write both workflows as YAML, lint them offline (actionlint or pyyaml), and say nothing was deployed. Part 7 owns CI/CD design and GitHub OIDC to AWS.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Job-posting and community patterns for Azure-heavy IT-services firms and GCCs (Azure ML plus Azure DevOps) versus GCP-using product companies (Vertex plus BigQuery); inferred from search snippets about ecosystem fit, not from a verified company report
**Say this first (1 line):** CI logs in with a short-lived OIDC token exchanged for a cloud identity (federated credential on Azure, Workload Identity Federation on Google), never a stored key, and the deployer identity can ship to one environment but cannot administer IAM, with the approval gate on the prod environment.

**Then explain:**
- **Azure:** the workflow sets `permissions: id-token: write`, and `azure/login` takes a client id, tenant id and subscription id (not a secret). In Entra, the app registration or managed identity has a federated credential that trusts this repo and branch or environment. Then `az ml job create` and `az ml online-deployment create` run with that identity (needs the `ml` CLI extension, check current docs).
- **Google:** `google-github-actions/auth` takes a workload identity provider and a service account. A pool and provider trust GitHub's token with a condition on repository; the pipeline impersonates the deployer service account. Then `gcloud ai custom-jobs create` and `gcloud ai endpoints deploy-model`. Flag spellings change, check current docs.
- **Why no long-lived keys:** a leaked JSON key or client secret works from anywhere until someone finds and rotates it. A federated token lives for minutes and only for matching claims.
- **Deployer may / may not:** may submit jobs, register models, deploy to the one workspace or project. May not grant roles, edit network or perimeter, read unrelated data. Use separate identities for dev and prod (the two files use different ids).
- **Approval gate:** a GitHub `environment: prod` with required reviewers. The prod login job only starts after approval. Azure DevOps has an equivalent with environments and checks.
- **Failure modes:** federated credential subject does not match the branch or environment (login fails with an obscure error), `id-token: write` missing, one identity for all stages, and a train job that deploys without a gate.

**Example:** two workflows, train then deploy-prod behind a gate. Lint rules I run: id-token permission present, a federated login step in every job, no secret-looking key, actions pinned with `@`, deploy jobs have an environment. The bad sample has three findings. Hand check: bad.yml lacks the permission, uses `AZURE_CREDENTIALS`, and has a deploy job with no environment, so 3.

**Code:** a linter (python) and the two workflows (yaml).
```python
# ---- q25_lint_workflows.py ----
"""Q25: offline lint with pyyaml. No deploy, no network. (actionlint is not installed here.)"""
import sys, re, yaml
SECRET_PAT = re.compile(r"(client[-_]secret|credentials_json|AZURE_CREDENTIALS|private_key|\.json)", re.I)

def lint(path):
    doc = yaml.safe_load(open(path))
    trig = doc.get("on", doc.get(True))             # pyyaml (YAML 1.1) reads the key `on` as boolean True
    errs = []
    perms = doc.get("permissions", {})
    if perms.get("id-token") != "write": errs.append("workflow lacks permissions.id-token: write (OIDC login would fail)")
    text = open(path).read()
    for line in text.splitlines():
        code = line.split("#")[0]
        if SECRET_PAT.search(code): errs.append(f"long-lived credential pattern: {code.strip()}")
    for name, job in doc["jobs"].items():
        steps = job["steps"]
        login = [s for s in steps if str(s.get("uses", "")).startswith(("azure/login", "google-github-actions/auth"))]
        if not login: errs.append(f"job {name}: no federated login step")
        for s in steps:
            if "uses" in s and "@" not in s["uses"]: errs.append(f"job {name}: unpinned action {s['uses']}")
        if "deploy" in name and "environment" not in job: errs.append(f"job {name}: deploy job without an environment (no approval gate)")
    return trig, errs

for p in sys.argv[1:]:
    trig, errs = lint(p)
    print(p.split("/")[-1], "| trigger:", trig)
    for e in errs: print("   -", e)
    if not errs: print("   lint: OK")

# negative test: a bad workflow must be caught
bad = """
name: bad
on: push
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    steps:
      - uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
"""
open("bad.yml", "w").write(bad)
trig, errs = lint("bad.yml"); print("bad.yml |", len(errs), "findings"); [print("   -", e) for e in errs]
import os; os.remove("bad.yml")
```

```yaml
# ---- azure_ml_deploy.yml ----
name: azure-ml-train-and-deploy
on:
  push:
    branches: [main]
permissions:
  id-token: write      # lets the job request an OIDC token
  contents: read
jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: azure/login@v2           # federated credential: no client secret stored
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      - run: az extension add -n ml -y
      - run: >
          az ml job create --file jobs/train.yml
          --resource-group rg-ml --workspace-name ws-ml-dev --stream
  deploy-prod:
    needs: train
    runs-on: ubuntu-latest
    environment: prod                  # required reviewers are set on this environment in repo settings
    steps:
      - uses: actions/checkout@v4
      - uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID_PROD }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      - run: az extension add -n ml -y
      - run: >
          az ml online-deployment create --file deploy/green.yml
          --resource-group rg-ml --workspace-name ws-ml-prod
---
# ---- vertex_deploy.yml ----
name: vertex-train-and-deploy
on:
  push:
    branches: [main]
permissions:
  id-token: write
  contents: read
jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/auth@v2     # Workload Identity Federation: no key file
        with:
          workload_identity_provider: projects/123456789/locations/global/workloadIdentityPools/gh-pool/providers/gh-provider
          service_account: vertex-deployer@demo-proj.iam.gserviceaccount.com
      - uses: google-github-actions/setup-gcloud@v2
      - run: >
          gcloud ai custom-jobs create --region=asia-south1 --display-name=train-${{ github.sha }}
          --config=jobs/custom_job.yaml
  deploy-prod:
    needs: train
    runs-on: ubuntu-latest
    environment: prod
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/123456789/locations/global/workloadIdentityPools/gh-pool/providers/gh-provider
          service_account: vertex-prod-deployer@demo-prod.iam.gserviceaccount.com
      - uses: google-github-actions/setup-gcloud@v2
      - run: >
          gcloud ai endpoints deploy-model ENDPOINT_ID --region=asia-south1
          --model=MODEL_ID --display-name=green --machine-type=n1-standard-4
          --min-replica-count=1 --max-replica-count=2
```

**Output (my run):** `python -I` with pyyaml. pyyaml reads `on:` as boolean True, handled in the script. actionlint is not installed here, so this is a small custom lint, not a full GitHub schema check. Nothing was deployed, no OIDC token was issued, no federation was configured. Action versions (`@v2`, `@v4`) are examples; check current docs.
```text
$ python -I q25_lint_workflows.py
azure_ml_deploy.yml | trigger: {'push': {'branches': ['main']}}
   lint: OK
vertex_deploy.yml | trigger: {'push': {'branches': ['main']}}
   lint: OK
bad.yml | 3 findings
   - workflow lacks permissions.id-token: write (OIDC login would fail)
   - long-lived credential pattern: creds: ${{ secrets.AZURE_CREDENTIALS }}
   - job deploy-prod: deploy job without an environment (no approval gate)
```

**Follow-ups:**
- *Subject claim?* Scope the trust to repo plus environment or branch, not the whole organisation.
- *Where do approvals live?* On the prod environment, not in a script.
- *Part 7 difference?* Part 7 owns the pipeline design and the AWS version; here it is only the two clouds.

**Common mistakes:**
- Saving a service principal secret or JSON key in repository secrets.
- Giving the deployer Owner or Contributor on the whole subscription or project.
- Letting pull requests from forks trigger the prod login.

### Q26 ⭐⭐ 🟡 Responsible-AI tooling: Azure ML Responsible AI dashboard (error analysis, interpretability, counterfactuals, causal analysis, fairness) and its pipeline components and scorecard, versus Vertex AI Explainable AI and model evaluation. When does a bank or an insurer in India need these artefacts attached to a model version, and what do they not prove? Show how you would record dashboard output as registry tags or metadata and validate the record schema in Python. Not executed: no dashboard was generated. Book 1 owns fairness and explainability theory.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs') | Certification-style question families (Microsoft DP-100 study guide and its replacement AI-300 as reported by third-party sites, Google Cloud Professional Machine Learning Engineer exam-prep listings; mentioned as a source type only, no exam questions reproduced; skills lists conflicted between sources, so verify on the vendor pages)
**Say this first (1 line):** Azure ML's Responsible AI dashboard (error analysis, interpretability, counterfactuals, causal analysis, fairness) and Vertex Explainable AI plus model evaluation produce evidence; I attach a small, validated summary and a link to the model version and I never say it proves the model is fair.

**Then explain:**
- **Azure ML RAI dashboard:** built by a pipeline of components (a constructor and gather components, as the snippets describe) from a registered model and datasets. Pieces include error analysis, feature importance, counterfactual what-ifs, causal analysis. A scorecard is a shareable summary.
- **Vertex AI:** Explainable AI gives feature attributions for predictions (sampled Shapley, integrated gradients, XRAI depending on model type), and model evaluation gives metrics and, for some tasks, slices. Check current docs for which model types are supported.
- **When a bank or insurer needs it:** model risk reviews for credit, claims or pricing, regulator or internal audit asks for the reason of a decision, and customer-impacting decisions. Which Indian rules apply is a legal question, I do not state them here.
- **What it does not prove:** that the data is unbiased, that the metric you picked is the right one, that fairness holds on groups you did not slice, or that it holds next quarter. Attributions explain the model, not the world.
- **Recording it:** keep the dashboard artefact in storage and put flat summary tags on the registry entry (Azure tags are string key-values): link, metric, value, threshold, method, reviewer, date, limitations. Validate before tagging.
- **Failure modes:** dashboard built on a dev dataset, never rebuilt after retraining, protected attribute not available at all, and tags edited by hand.

**Example:** model `credit-risk` v7, demographic parity difference 0.04 against threshold 0.05: gate passes. The validator rejects fairness 1.7 (out of range), method `none`, a 3-character limitations text and a `file://` link. Hand check: 0.04 is at most 0.05, so passes; it says nothing about intersectional groups, which the limitations text must say.

**Code:** pydantic schema with tags, plus a Vertex explanation parameter proto.
```python
# ---- q26_rai_record.py ----
"""Q26: record RAI evidence as flat string tags on an Azure ML Model (offline) and validate the schema with pydantic.
No dashboard was generated; the numbers in the sample are made up for the schema test."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md, json
from typing import Literal
from pydantic import BaseModel, Field, ValidationError, field_validator
from azure.ai.ml.entities import Model
print("azure-ai-ml", md.version("azure-ai-ml"), "| pydantic", md.version("pydantic"))

class RaiEvidence(BaseModel):
    model_name: str
    model_version: str
    dashboard_uri: str = Field(pattern=r"^(azureml|gs|https)://")   # where the full artefact lives
    protected_attribute: str                                           # e.g. gender (only if legally and ethically usable)
    fairness_metric: Literal["demographic_parity_difference", "equalized_odds_difference"]
    fairness_value: float = Field(ge=0, le=1)
    threshold: float = Field(gt=0, le=1)
    explainability_method: Literal["shap", "mimic", "integrated_gradients", "sampled_shapley", "none"]
    reviewer: str
    reviewed_on: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    limitations: str = Field(min_length=20)                            # what the evidence does NOT prove

    @field_validator("explainability_method")
    @classmethod
    def not_none(cls, v):
        if v == "none": raise ValueError("explainability_method 'none' needs a written exception, not a tag")
        return v
    def to_tags(self) -> dict[str, str]:                               # registry tags are flat strings
        return {f"rai.{k}": str(v) for k, v in self.model_dump().items() if k not in ("model_name", "model_version")}
    @property
    def passed(self): return self.fairness_value <= self.threshold

good = dict(model_name="credit-risk", model_version="7", dashboard_uri="azureml://registries/r/rai/dash1",
            protected_attribute="gender", fairness_metric="demographic_parity_difference", fairness_value=0.04,
            threshold=0.05, explainability_method="shap", reviewer="model-risk@example.com", reviewed_on="2026-10-20",
            limitations="Tested on 2025 applicant data only; no intersectional slices.")
ev = RaiEvidence(**good)
m = Model(name=ev.model_name, version=ev.model_version, path="./model", tags=ev.to_tags())
print("tags on Model entity:", len(m.tags), "e.g.", {k: m.tags[k] for k in list(m.tags)[:3]})
print("gate passed:", ev.passed, "(a pass is a threshold check, not proof of fairness)")
for label, patch in [("fairness out of range", {"fairness_value": 1.7}), ("method none", {"explainability_method": "none"}),
                     ("short limitations", {"limitations": "n/a"}), ("bad uri", {"dashboard_uri": "file:///tmp/x"})]:
    try: RaiEvidence(**{**good, **patch}); print(label, "-> accepted (BUG)")
    except ValidationError as e: print(label, "-> rejected:", e.errors()[0]["loc"][0])

# ---- q26_vertex_explain.py ----
"""Q26 Vertex: ExplanationParameters proto (sampled Shapley) built offline; nothing sent."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from google.cloud.aiplatform_v1.types import ExplanationParameters, SampledShapleyAttribution
print("google-cloud-aiplatform", md.version("google-cloud-aiplatform"))
p = ExplanationParameters(sampled_shapley_attribution=SampledShapleyAttribution(path_count=10), top_k=3)
print(ExplanationParameters.to_json(p, indent=None))
```

**Output (my run):** azure-ai-ml 1.35.2, pydantic 2.14.1 and google-cloud-aiplatform 1.165.1, `python -I`. The Model entity and proto were built in memory. The numbers are made up for the schema test. Not executed: the RAI dashboard pipeline, scorecard, Explainable AI calls and model evaluation; no dashboard was generated. Book 1 owns fairness theory.
```text
$ python -I q26_rai_record.py
azure-ai-ml 1.35.2 | pydantic 2.14.1
tags on Model entity: 9 e.g. {'rai.dashboard_uri': 'azureml://registries/r/rai/dash1', 'rai.protected_attribute': 'gender', 'rai.fairness_metric': 'demographic_parity_difference'}
gate passed: True (a pass is a threshold check, not proof of fairness)
fairness out of range -> rejected: fairness_value
method none -> rejected: explainability_method
short limitations -> rejected: limitations
bad uri -> rejected: dashboard_uri

$ python -I q26_vertex_explain.py
google-cloud-aiplatform 1.165.1
{"sampledShapleyAttribution": {"pathCount": 10}, "topK": 3}
```

**Follow-ups:**
- *Who signs off?* A named reviewer field and date; the gate is a person plus a check.
- *Rebuild when?* On every new model version or data refresh.
- *Is passing a fairness threshold enough?* No: it is one metric on the groups you chose.

**Common mistakes:**
- Treating dashboard output as a certificate.
- Storing evidence in a slide, not next to the model version.
- Running it once and never again after retraining.

### Q27 ⭐⭐ 🟡 BigQuery ML boundary on Vertex AI: when to train inside the warehouse (CREATE MODEL, remote models, importing and exporting models, registering to Vertex Model Registry) versus a Vertex custom job; what the Azure counterpart would be (warehouse or Fabric and Synapse features versus Azure ML) at the boundary only. Give a decision rule and the portability cost of SQL-defined models. Book 3 owns SQL. Write a decision function and test it; no BigQuery call was made.
**Asked at:** GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Cross-cloud comparison articles (TechTarget 'Compare Google Vertex AI vs Amazon SageMaker vs Azure ML', cloudoptimo, gmicloud, superwise, a redresscompliance licensing piece; search snippets only, not opened; several authors sell competing services or advice, so conclusions treated as opinion) | Certification-style question families (Microsoft DP-100 study guide and its replacement AI-300 as reported by third-party sites, Google Cloud Professional Machine Learning Engineer exam-prep listings; mentioned as a source type only, no exam questions reproduced; skills lists conflicted between sources, so verify on the vendor pages)
**Say this first (1 line):** If the data is already in the warehouse, the model family is built in and scoring is batch, train with BigQuery ML; if I need custom code, GPUs, custom features or tight online latency, I use a Vertex custom job, and I count the portability cost of a model defined in SQL.

**Then explain:**
- **BigQuery ML:** `CREATE MODEL` trains inside the warehouse, `ML.PREDICT` scores in SQL, no data movement. There are also remote models that call a Vertex endpoint, import of some external model formats, and export of some models (check current docs which types). A BigQuery ML model can be registered to the Vertex Model Registry so governance sits in one place (check current docs).
- **Vertex custom job:** your code in a container, any framework, GPUs, your features, full control, more to operate.
- **Azure counterpart at the boundary only:** train in the warehouse or lakehouse side (Fabric or Synapse features, check current docs) versus Azure ML for custom training. I do not know the exact feature parity, so I say so in an interview.
- **Portability cost:** a SQL-defined model lives in the warehouse. Moving clouds means retraining from the data in another system, the model file may not export, and the SQL dialect differs. Keep the training SQL in git and the feature logic documented.
- **Failure modes:** a model that cannot be explained or exported when audit asks, SQL features that differ from online serving features, a big table scanned on every retrain (cost depth is Part 12), and scoring in SQL for a 50 ms API.

**Example:** weekly churn scores from a BigQuery table with logistic regression: BigQuery ML. An image model needs GPUs: custom job. A 50 ms fraud score with no export plan: custom job. Same fraud case with a plan to export and host: BigQuery ML is possible. Data in Blob storage, not in BigQuery: custom job by default. Hand check: five cases, expected `bqml`, `vertex_custom_job`, `vertex_custom_job`, `bqml`, `vertex_custom_job`, asserted in the script.

**Code:** the decision function with tests. The SQL syntax is shown in prose only, no SQL ran.
```python
# ---- q27_bqml_decision.py ----
"""Q27: decision rule BigQuery ML vs Vertex custom job. Pure Python; no BigQuery call was made."""
def decide(p: dict) -> tuple[str, list[str]]:
    why = []
    # hard blockers for in-warehouse training first
    if p["needs_custom_framework_or_gpu"]: return "vertex_custom_job", ["needs custom code, framework or GPU beyond built-in model types"]
    if p["needs_custom_features_in_python"]: return "vertex_custom_job", ["feature logic does not fit SQL"]
    if p["strict_realtime_latency_ms"] is not None and not p["will_export_model"]:
        return "vertex_custom_job", ["tight online latency: score outside the warehouse (or export and host)"]
    if p["data_in_warehouse"] and p["model_family_supported_in_bqml"]:
        why.append("data already in the warehouse, model family is built in")
        if p["batch_scoring_only"]: why.append("batch scoring in SQL is enough")
        if p["must_register_in_vertex"]: why.append("register to Vertex Model Registry so governance is shared (check current docs)")
        return "bqml", why
    return "vertex_custom_job", ["default: data not in warehouse or model family unsupported"]

base = dict(needs_custom_framework_or_gpu=False, needs_custom_features_in_python=False, strict_realtime_latency_ms=None,
            will_export_model=False, data_in_warehouse=True, model_family_supported_in_bqml=True, batch_scoring_only=True,
            must_register_in_vertex=False)
cases = {
 "weekly churn scores, data in BQ, logistic regression": base,
 "image model on GPUs": {**base, "needs_custom_framework_or_gpu": True},
 "fraud score at 50 ms online, no export plan": {**base, "strict_realtime_latency_ms": 50, "batch_scoring_only": False},
 "same fraud case but plan to export model": {**base, "strict_realtime_latency_ms": 50, "will_export_model": True, "batch_scoring_only": False, "must_register_in_vertex": True},
 "data lives in Blob storage, not BQ": {**base, "data_in_warehouse": False},
}
expected = ["bqml", "vertex_custom_job", "vertex_custom_job", "bqml", "vertex_custom_job"]
for (name, p), exp in zip(cases.items(), expected):
    got, why = decide(p); assert got == exp, (name, got)
    print(f"{got:17s} <- {name}: {'; '.join(why)}")
print("5 cases, all as expected")
```

**Output (my run):** Python 3.13 `python -I`, pure Python. No BigQuery call was made, no `CREATE MODEL` was run and no model was registered; the rule is my judgement, not a vendor rule. Book 3 owns SQL.
```text
$ python -I q27_bqml_decision.py
bqml              <- weekly churn scores, data in BQ, logistic regression: data already in the warehouse, model family is built in; batch scoring in SQL is enough
vertex_custom_job <- image model on GPUs: needs custom code, framework or GPU beyond built-in model types
vertex_custom_job <- fraud score at 50 ms online, no export plan: tight online latency: score outside the warehouse (or export and host)
bqml              <- same fraud case but plan to export model: data already in the warehouse, model family is built in; register to Vertex Model Registry so governance is shared (check current docs)
vertex_custom_job <- data lives in Blob storage, not BQ: default: data not in warehouse or model family unsupported
5 cases, all as expected
```

**Follow-ups:**
- *Why not always BigQuery ML?* Limited model families and control, and SQL models are harder to move.
- *Why not always a custom job?* More engineering and data movement for simple models.
- *How do you serve a BigQuery ML model online?* Export or register and deploy where supported, or call remote models; check current docs.

**Common mistakes:**
- Choosing by habit (always SQL, always Python).
- Ignoring that online features must match the SQL training features.
- Forgetting an exit path for a model that exists only in the warehouse.

### Q28 ⭐⭐ 🟡 Azure ML SDK and CLI v1 to v2 migration: the published support end dates for SDK v1 and CLI v1 as seen in search results (check current docs), what changes in vocabulary (datasets to data assets, estimators and ScriptRunConfig to command jobs, pipelines to components and pipeline jobs), that workspaces serve both API versions and migration is client code, and database datastores having no direct v2 equivalent. Write a rewrite plan, and show one v2 command job loaded and validated offline as the target state.
**Asked at:** Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | Certification-style question families (Microsoft DP-100 study guide and its replacement AI-300 as reported by third-party sites, Google Cloud Professional Machine Learning Engineer exam-prep listings; mentioned as a source type only, no exam questions reproduced; skills lists conflicted between sources, so verify on the vendor pages)
**Say this first (1 line):** Migration is a client-code rewrite, not a data move: the workspace, storage and registered assets stay, and I rewrite v1 scripts (Dataset, Estimator, ScriptRunConfig, Pipeline) as v2 YAML or `azure-ai-ml` objects (data assets, command jobs, components, pipeline jobs), one pipeline at a time.

**Then explain:**
- Dates, as seen in search snippets only (no page opened, check current docs): SDK v1 deprecated 31 Mar 2025 with support ending 30 Jun 2026, CLI v1 ended 30 Sep 2025. If those hold, v1 is already out of support today, so the plan is urgent, not optional.
- Vocabulary map:

| v1 | v2 |
|---|---|
| Dataset (tabular / file) | Data asset (`uri_file`, `uri_folder`, `mltable`) |
| Estimator, ScriptRunConfig | `command` job (YAML `type: command`) |
| Pipeline, PythonScriptStep | Component + pipeline job (`dsl.pipeline` or YAML) |
| Environment | Environment (similar, now versioned asset) |
| Datastore | Datastore (database datastores: no direct v2 equivalent per the snippets) |
| Webservice, AKS/ACI deploy | Managed online endpoint + deployment |
| Experiment, Run | Job in an experiment |

- Workspaces serve both API versions, so old and new jobs run side by side. That is what makes a gradual migration safe: no big-bang, and you can compare outputs of v1 and v2 runs.
- Rewrite plan: (1) inventory every v1 script, pipeline, scheduled run and deploy script; (2) rank by business risk and by how many others depend on them; (3) move data first (register data assets, keep same storage paths); (4) rewrite training as a command job, run it next to the v1 run, compare metrics; (5) rewrite pipelines as components; (6) move deployment to managed online endpoints with traffic split (new deployment at 0 percent, then shift); (7) switch CI/CD and schedules; (8) freeze v1 code, then delete.
- Failure modes: database datastores or dataset features with no v2 twin (redesign, for example export to files or tables first); v1 `Dataset.register` lineage not carried over; CI still calling a retired v1 CLI extension; mixing v1 and v2 `azureml-core` and `azure-ai-ml` in one environment.

**Example:** a v1 `ScriptRunConfig(source_directory="src", script="train.py", arguments=["--lr", 0.1], compute_target="cpu-cluster")` becomes the YAML below: same script, same compute, but code path, inputs and environment are now explicit and versioned. I load it with the SDK's own schema and validate it offline.

**Code:**
```yaml
# job.yml  (v2 command job; written by q28.py)
$schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
display_name: train-churn
experiment_name: churn
code: ./src
command: python train.py --data ${{inputs.training_data}} --lr ${{inputs.lr}}
inputs:
  training_data:
    type: uri_folder
    path: azureml:churn-data:1
  lr: 0.1
environment: azureml:sklearn-env:3
compute: azureml:cpu-cluster
```
```python
# ---- q28.py ----
# q28.py - v2 command job as target state, loaded and validated offline (no workspace, no network)
import sys, os, tempfile, warnings, logging
warnings.filterwarnings("ignore"); logging.disable(logging.CRITICAL)
import azure.ai.ml as m
from azure.ai.ml import load_job
print("azure-ai-ml", m.__version__)
root = sys.argv[1]; os.makedirs(os.path.join(root, "src"), exist_ok=True)
open(os.path.join(root, "src", "train.py"), "w").write("print('train')\n")
JOB = """\
$schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
display_name: train-churn
experiment_name: churn
code: ./src
command: python train.py --data ${{inputs.training_data}} --lr ${{inputs.lr}}
inputs:
  training_data:
    type: uri_folder
    path: azureml:churn-data:1
  lr: 0.1
environment: azureml:sklearn-env:3
compute: azureml:cpu-cluster
"""
p = os.path.join(root, "job.yml"); open(p, "w").write(JOB)
job = load_job(p)
print("loaded:", type(job).__name__, "| compute:", job.compute, "| env:", job.environment)
print("input keys:", sorted(job.inputs))
job._validate()
print("validate: OK")
bad = JOB.replace("inputs:", "inptus:", 1)
open(os.path.join(root, "bad.yml"), "w").write(bad)
try:
    load_job(os.path.join(root, "bad.yml"))._validate()
    print("bad: no error")
except Exception as e:
    print("bad job ->", type(e).__name__, "|", str(e).replace("\n", " ")[:160])
```

**Output (my run):** `/tmp/claude-0/b11p11/az/bin/python -I q28.py <tmpdir>` with azure-ai-ml 1.35.2. Loading and validating used the SDK's own schemas offline; the `$schema` URL is not fetched. `azureml:churn-data:1` and the compute were not resolved (no workspace), so this proves the file is well formed, not that the job would run. Submitting a job, SDK v1 behaviour, and the retirement dates were not executed.
```
azure-ai-ml 1.35.2
loaded: Command | compute: cpu-cluster | env: sklearn-env:3
input keys: ['lr', 'training_data']
validate: OK
bad job -> ValidationError | Validation for CommandSchema failed:   {   "result": "Failed",   "errors": [     {       "message": "Validation for CommandJobSchema failed:\n\n {\n  \"inptus\"
```

**Follow-ups:**
- *Can v1 and v2 jobs share a workspace?* Yes per the migration docs as seen in snippets (check current docs); that is why you migrate pipeline by pipeline.
- *What about the v1 `Dataset` objects?* Register the same storage path as a v2 data asset; use `mltable` when you need schema or transforms.
- *How do you prove the rewrite is equal?* Run both, compare metrics and output hashes on the same seed and data.

**Common mistakes:** Treating migration as a data migration; rewriting everything at once; forgetting CI/CD, schedules and notebooks that still call v1; trusting a date from a blog instead of the current docs; assuming every v1 feature has a v2 twin.

### Q29 ⭐⭐ 🟡 Debugging a permission failure the same way on both clouds: a training job starts but cannot read its dataset (Azure ML job with a managed identity reading Blob; Vertex custom job with a service account reading Cloud Storage). Give the ordered checks: which identity the job really runs as, role or IAM binding at the right scope, private networking, region mismatch, expired credentials, and policy or perimeter denials. Encode the decision tree as a Python function, run it on four scenarios, and say that the logs and role assignments were not inspected live.
**Asked at:** Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs') | Job-posting and community patterns for Azure-heavy IT-services firms and GCCs (Azure ML plus Azure DevOps) versus GCP-using product companies (Vertex plus BigQuery); inferred from search snippets about ecosystem fit, not from a verified company report
**Say this first (1 line):** Check in a fixed order: which identity the job really runs as, then its role or IAM binding at the right scope, then the network path, then Region, then expired credentials, then policy or perimeter denials; stop at the first failure.

**Then explain:**
- Why this order: each step can hide the next. A wrong identity makes every later role check meaningless; a missing role looks the same as a network block in a bare "403 / authorization failed" message.
- Azure ML: the job may run as the submitting user, the compute's managed identity, or a user-assigned identity, depending on how the job and compute are configured. Storage needs a data-plane role such as Storage Blob Data Reader on the storage account or container (a control-plane role like Contributor does not read blobs). Check current docs for which identity applies to which job type.
- Vertex AI custom job: it runs as a service account (the job's own, or a default one). That account needs a Cloud Storage role such as Storage Object Viewer on the bucket (or project), and the right-scope binding matters (bucket vs project, conditions).
- Network: storage with public access off needs a private endpoint (Azure) or Private Google Access / PSC / a VPC Service Controls-compatible path (GCP). Azure managed VNet and VPC-SC outbound rules are a common hidden block. The snippets did not cover service-account behaviour inside VPC-SC, so verify.
- Region and policy: compute and data in different Regions can break a residency policy or a perimeter rule; Azure Policy or an organisation policy / deny rule beats an allow. Expired SAS tokens, rotated keys, or stale ADC credentials fail the same way as no permission.
- I did not inspect any real logs or role assignments. This is a method plus a function, run on invented facts.

**Example:** Scenario B below: the job runs as the right managed identity, but the only role it holds is Contributor on the resource group. Blob reads need a data role, so the answer is a binding at the storage scope, not a network change.

**Code:**
```python
# ---- q29.py ----
# q29.py - ordered permission-failure checks for a job that cannot read its dataset (both clouds). Pure Python.
# The scenarios are made-up facts a human would collect from logs and the portal; nothing here was read from a real cloud.
ORDER = ["identity", "binding", "network", "region", "credential", "policy"]

def diagnose(s):
    """Return (check, advice) for the FIRST failing check, or ('none', ...)."""
    cloud = s["cloud"]
    # 1. Which identity does the job REALLY run as?
    if s["intended_identity"] != s["effective_identity"]:
        who = ("user-assigned vs system-assigned vs the submitting user's identity" if cloud == "azure"
               else "job service account vs the default compute service account")
        return "identity", f"job runs as {s['effective_identity']!r}, not {s['intended_identity']!r} ({who}); fix the job's identity setting"
    # 2. Role / IAM binding at the right scope (and the right data-plane role)
    need = s["needed_role"]
    if need not in s["roles_on_data_scope"]:
        return "binding", f"{s['effective_identity']!r} lacks {need!r} on {s['data_scope']!r}; a role on the workspace/project or on the control plane does not cover data access"
    # 3. Private networking between the compute and the storage
    if s["storage_public_access"] == "disabled" and not s["private_path_to_storage"]:
        return "network", "storage blocks public access and the job's compute has no private endpoint / PSC / managed-network rule to it"
    # 4. Region mismatch (latency, residency policy, or a service that must be in-region)
    if s["compute_region"] != s["data_region"] and s["same_region_required"]:
        return "region", f"compute in {s['compute_region']} but data in {s['data_region']}; policy or setup needs them together"
    # 5. Expired or missing credential (token, key, SAS, ADC)
    if s["credential_expired"]:
        return "credential", "token / SAS / key expired or was revoked; re-issue and prefer identity-based access to long-lived keys"
    # 6. Policy or perimeter denial that overrides an allow
    if s["policy_denial"]:
        return "policy", f"explicit deny from {s['policy_denial']}; read the denial text, an allow cannot beat it"
    return "none", "all six checks pass; look at the file path, object name, and the training code itself"

SCENARIOS = [
  dict(name="A azure wrong identity", cloud="azure", intended_identity="uami-train", effective_identity="user:dev@corp",
       needed_role="Storage Blob Data Reader", data_scope="storageacct/container", roles_on_data_scope=["Storage Blob Data Reader"],
       storage_public_access="enabled", private_path_to_storage=False, compute_region="centralindia", data_region="centralindia",
       same_region_required=False, credential_expired=False, policy_denial=None),
  dict(name="B azure role on wrong scope", cloud="azure", intended_identity="uami-train", effective_identity="uami-train",
       needed_role="Storage Blob Data Reader", data_scope="storageacct/container", roles_on_data_scope=["Contributor"],
       storage_public_access="enabled", private_path_to_storage=False, compute_region="centralindia", data_region="centralindia",
       same_region_required=False, credential_expired=False, policy_denial=None),
  dict(name="C vertex private storage", cloud="gcp", intended_identity="sa-train@proj", effective_identity="sa-train@proj",
       needed_role="roles/storage.objectViewer", data_scope="bucket", roles_on_data_scope=["roles/storage.objectViewer"],
       storage_public_access="disabled", private_path_to_storage=False, compute_region="asia-south1", data_region="asia-south1",
       same_region_required=False, credential_expired=False, policy_denial=None),
  dict(name="D vertex perimeter deny", cloud="gcp", intended_identity="sa-train@proj", effective_identity="sa-train@proj",
       needed_role="roles/storage.objectViewer", data_scope="bucket", roles_on_data_scope=["roles/storage.objectViewer"],
       storage_public_access="enabled", private_path_to_storage=True, compute_region="asia-south1", data_region="asia-south1",
       same_region_required=False, credential_expired=False, policy_denial="VPC Service Controls perimeter"),
]
if __name__ == "__main__":
    for s in SCENARIOS:
        c, adv = diagnose(s)
        print(f"{s['name']:30s} -> check={c:10s} {adv}")
    # ordering matters: a scenario with two faults reports the earlier one
    both = dict(SCENARIOS[1], credential_expired=True)
    print("two faults (binding + expired) ->", diagnose(both)[0])
    ok = dict(SCENARIOS[0], effective_identity="uami-train")
    print("healthy ->", diagnose(ok)[0])
```

**Output (my run):** `python3 -I q29.py` (pure Python, no cloud calls). The four scenarios are invented inputs; the function is a teaching model, not a replacement for the cloud's own diagnostics (Azure activity logs and role-assignment views, Google Cloud Policy Troubleshooter and audit logs: not executed here).
```
A azure wrong identity         -> check=identity   job runs as 'user:dev@corp', not 'uami-train' (user-assigned vs system-assigned vs the submitting user's identity); fix the job's identity setting
B azure role on wrong scope    -> check=binding    'uami-train' lacks 'Storage Blob Data Reader' on 'storageacct/container'; a role on the workspace/project or on the control plane does not cover data access
C vertex private storage       -> check=network    storage blocks public access and the job's compute has no private endpoint / PSC / managed-network rule to it
D vertex perimeter deny        -> check=policy     explicit deny from VPC Service Controls perimeter; read the denial text, an allow cannot beat it
two faults (binding + expired) -> binding
healthy -> none
```

**Follow-ups:**
- *What if two things are wrong?* The function reports the first; fix, rerun, and expect the next one. The last output line shows it.
- *Why not just grant Owner?* It hides the real cause and breaks least privilege (Part 12 goes deeper).
- *How do you confirm the identity?* Print it from inside a tiny diagnostic job (for example the token's identity or the metadata server's service account), not from the portal's intent.

**Common mistakes:** Granting a role to the user instead of the job's identity; granting at the workspace or project but not at the data scope; waiting for role propagation to be instant (it can take minutes, check docs); forgetting that an explicit deny or perimeter overrides every allow.

### Q30 ⭐ 🟡 India Region and data-residency questions for ML on Azure and GCP: what personal data enters training and serving, the DPDP Act 2023 position on cross-border transfer as reported (transfers allowed unless a country is restricted, sector rules such as RBI still apply, commencement timing differs by source, check current law), choosing in-India Regions, and where logs, backups, model artifacts and monitoring data live. Do not assert which services exist in which Region: say check current docs. Write a Region and data-class policy checker in Python and run it on sample configs. Not legal advice.
**Asked at:** India data-protection sources on the DPDP Act 2023 and Rules 2025 cross-border transfer provisions (legal500, medianama, ksandk, rainmaker, trustarc; search snippets only, not opened; commencement dates differed by source and no region-availability page was found, so region claims are hedged 'check current docs'); legal explainers, not interview reports; BFSI, health and e-commerce data roles in India | Job-posting and community patterns for Azure-heavy IT-services firms and GCCs (Azure ML plus Azure DevOps) versus GCP-using product companies (Vertex plus BigQuery); inferred from search snippets about ecosystem fit, not from a verified company report
**Say this first (1 line):** Treat residency as a data-class by location question: decide which data is personal or regulated, pick in-India Regions where policy needs it, then check every place data lands (training, serving, logs, backups, artifacts, monitoring), not only the main bucket. This is not legal advice.

**Then explain:**
- What personal data enters ML: customer IDs, phone, email, location, device IDs, free text, images, labels from agents. Features can still identify a person even when names are dropped. Serving logs often hold raw request payloads, which is the usual leak.
- DPDP Act 2023 as reported by the search snippets (not opened, check current law): cross-border transfer is allowed unless a country is restricted by notification; stricter sector rules (for example RBI directions for payment data) are preserved; there is no blanket localisation. The commencement date for the transfer provisions differs by source (one reported 13 May 2027), so verify. Ask your legal team before treating any of this as settled.
- Region choice: Azure has Indian Regions (for example Central India, South India) and GCP has asia-south1 and asia-south2. I do not assert that Azure ML, Vertex AI, a GPU type or any feature is available there: check current docs and the service's Region list per feature.
- Easy-to-miss places: log and metric sinks, backup or geo-redundant pairs (a paired Region may be outside India), container registries, model artifacts in multi-region buckets, monitoring or telemetry sent to a global service, support or experiment-tracking SaaS, notebooks on laptops.
- Policy as code: encode org rules (which classes may live where) and run them on every config. Unknown or undeclared location should fail, not pass.

**Example:** `recsys-gcp` below keeps its data in asia-south1 but trains in us-central1 and writes artifacts to a US multi-region bucket. Under our made-up rule "personal data stays in India", that is two findings even though the dataset itself is fine.

**Code:**
```python
# ---- q30.py ----
# q30.py - Region x data-class policy checker. The policy is OUR org's choice, not law and not a list of what a cloud offers.
# Region names are labels used in the sample; whether a service exists in a Region: check current docs. Not legal advice.
import yaml
POLICY = yaml.safe_load("""
allowed_regions:
  public:        ["any"]
  personal:      ["centralindia", "southindia", "asia-south1", "asia-south2"]   # org choice: keep personal data in India
  regulated_fin: ["centralindia", "southindia", "asia-south1", "asia-south2"]   # sector rule (e.g. RBI-type) may be stricter than the Act; check current rules
  restricted_countries: []   # fill from any government notification; empty = none known to us
locations_that_count: [primary_data, training_compute, serving, artifacts, logs, backups, monitoring]
""")
CONFIGS = {
 "churn-azure": {"data_class": "personal", "primary_data": "centralindia", "training_compute": "centralindia",
                 "serving": "centralindia", "artifacts": "centralindia", "logs": "centralindia",
                 "backups": "southindia", "monitoring": "centralindia"},
 "fraud-gcp":   {"data_class": "regulated_fin", "primary_data": "asia-south1", "training_compute": "asia-south1",
                 "serving": "asia-south1", "artifacts": "asia-south1", "logs": "us-central1",
                 "backups": "asia-south2", "monitoring": "asia-south1"},
 "recsys-gcp":  {"data_class": "personal", "primary_data": "asia-south1", "training_compute": "us-central1",
                 "serving": "asia-south1", "artifacts": "multi-region-US", "logs": "asia-south1",
                 "backups": "asia-south1", "monitoring": "asia-south1"},
 "docs-public": {"data_class": "public", "primary_data": "westeurope", "training_compute": "westeurope",
                 "serving": "westeurope", "artifacts": "westeurope", "logs": "westeurope",
                 "backups": "westeurope", "monitoring": "westeurope"},
 "bad-config":  {"data_class": "personal", "primary_data": "centralindia", "serving": "centralindia"},
}
def check(name, cfg, pol=POLICY):
    issues = []
    cls = cfg.get("data_class")
    if cls not in pol["allowed_regions"]:
        return [f"unknown data_class {cls!r}"]
    ok = pol["allowed_regions"][cls]
    for loc in pol["locations_that_count"]:
        r = cfg.get(loc)
        if r is None:
            issues.append(f"{loc}: not declared (unknown is a finding, not a pass)")
        elif r in pol["allowed_regions"]["restricted_countries"]:
            issues.append(f"{loc}: {r} is on the restricted list")
        elif ok != ["any"] and r not in ok:
            issues.append(f"{loc}: {r} not in allowed list for {cls}")
    return issues
for n, c in CONFIGS.items():
    iss = check(n, c)
    print(f"{n:12s} [{c.get('data_class')}] ->", "PASS" if not iss else "FAIL")
    for i in iss: print("    -", i)
```

**Output (my run):** `python3 -I q30.py`. The policy and sample configs are invented; the Region names are labels, not a statement of what each cloud offers. No cloud resource or real configuration was read.
```
churn-azure  [personal] -> PASS
fraud-gcp    [regulated_fin] -> FAIL
    - logs: us-central1 not in allowed list for regulated_fin
recsys-gcp   [personal] -> FAIL
    - training_compute: us-central1 not in allowed list for personal
    - artifacts: multi-region-US not in allowed list for personal
docs-public  [public] -> PASS
bad-config   [personal] -> FAIL
    - training_compute: not declared (unknown is a finding, not a pass)
    - artifacts: not declared (unknown is a finding, not a pass)
    - logs: not declared (unknown is a finding, not a pass)
    - backups: not declared (unknown is a finding, not a pass)
    - monitoring: not declared (unknown is a finding, not a pass)
```

**Follow-ups:**
- *Does the Act force data to stay in India?* As reported, not generally; sector rules may. Legal advice required.
- *Is the in-India Region enough?* Not if the backup pair, logs or support access leave India.
- *Public data?* The rule can be "any"; keep the class explicit anyway.

**Common mistakes:** Checking only the primary storage account; assuming a managed service exists in a Region; treating the cloud vendor's compliance badge as your own compliance; logging full request bodies; copying a rule from a blog without reading the current law and sector circulars.

### Q31 ⭐ 🟡 LLM boundary question: a product team wants a hosted foundation model. Where does the MLOps platform end and Azure OpenAI or Gemini on Vertex AI begin? Cover what MLOps still owns (deployment identity, private networking, quota and Region choice, model-version retirement tracking, evaluation gates, logging and cost attribution) and what Book 2 owns (prompting, RAG, agents, LLM evaluation). Write a pre-launch checklist as YAML, validate it with pyyaml, and say no model endpoint was called.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Cross-cloud comparison articles (TechTarget 'Compare Google Vertex AI vs Amazon SageMaker vs Azure ML', cloudoptimo, gmicloud, superwise, a redresscompliance licensing piece; search snippets only, not opened; several authors sell competing services or advice, so conclusions treated as opinion)
**Say this first (1 line):** The MLOps platform owns everything around the model call (identity, network, quota, Region, version pinning and retirement, release gates, logging, cost tags, fallback), while Book 2 owns what goes into and comes out of the model (prompts, RAG, agents, how to judge answer quality).

**Then explain:**
- Hosted models are another managed dependency with an endpoint, a deployment or model name, and a lifecycle. Treat them like any service you do not control.
- Platform owns: deployment identity (managed identity or service account, no shared keys in code); private networking decisions (private endpoint or PSC) and recorded public-access state; quota and Region (limits and availability change, check current docs; plan a fallback Region); model-version retirement tracking (providers retire versions on published dates; pin the version and alert before the date); an evaluation gate in CI that blocks release when the Book 2 suite fails on the pinned version; request-logging policy and PII handling; cost attribution by tags per team or feature; timeout, retry and degraded-answer path.
- Book 2 owns: prompt design, retrieval and chunking, agent tool use, and the design of LLM evaluation sets and judges.
- Failure modes: version silently retired, quota hit at launch, key pasted into a notebook, logs holding customer data, no per-feature cost split, no fallback when the provider is slow.
- Azure OpenAI and Gemini on Vertex AI differ in model names, quota model and access setup; I did not verify any of that live, check current docs.

**Example:** support-assistant launches on a pinned model version. The CI gate runs the Book 2 eval set and fails the release if the pass rate drops. Three weeks before the provider's published retirement date, a calendar alert fires and the team re-runs the gate on the replacement.

**Code:**
```yaml
# q31_checklist.yaml (full file in code/; first lines shown by the validator)
service: support-assistant
provider: azure_openai          # or gemini_on_vertex
owner: ml-platform-team
mlops_owns:
  - id: model_version
    check: Model name and version pinned; retirement date tracked with an alert before it
    evidence: calendar entry or ticket (dates change; check current docs)
  # ... 7 more items: identity, network, quota_region, eval_gate, logging, cost_attribution, fallback
book2_owns: [prompting, rag, agents, llm_evaluation_design]
called_real_endpoint: false
```
```python
# ---- q31.py ----
# q31.py - validate the launch checklist with pyyaml. No model endpoint is called.
import sys, yaml
d = yaml.safe_load(open(sys.argv[1]))
REQUIRED_IDS = {"identity", "network", "quota_region", "model_version", "eval_gate", "logging", "cost_attribution", "fallback"}
errs = []
for k in ("service", "provider", "owner", "mlops_owns", "book2_owns"):
    if k not in d: errs.append(f"missing top-level key {k}")
if d.get("provider") not in ("azure_openai", "gemini_on_vertex"): errs.append("provider must be azure_openai or gemini_on_vertex")
ids = [i.get("id") for i in d["mlops_owns"]]
if len(ids) != len(set(ids)): errs.append("duplicate ids")
for miss in sorted(REQUIRED_IDS - set(ids)): errs.append(f"missing item {miss}")
for i in d["mlops_owns"]:
    for f in ("id", "check", "evidence"):
        if not i.get(f): errs.append(f"{i.get('id')}: empty {f}")
overlap = set(d["book2_owns"]) & set(ids)
if overlap: errs.append(f"items in both lists: {overlap}")
print("items:", len(ids), "| book2 topics:", d["book2_owns"])
print("called_real_endpoint:", d["called_real_endpoint"])
print("RESULT:", "OK" if not errs else errs)
# negative test
d["mlops_owns"] = [i for i in d["mlops_owns"] if i["id"] != "model_version"]
ids = {i["id"] for i in d["mlops_owns"]}
print("negative test (drop model_version) ->", sorted(REQUIRED_IDS - ids))
```

**Output (my run):** `python3 -I q31.py q31_checklist.yaml` with pyyaml. It checks structure (all eight items present, no duplicates, owner lists not overlapping). It does not check that any control actually exists. No Azure OpenAI or Gemini endpoint was called, and nothing about quotas, Regions or retirement dates was verified.
```
items: 8 | book2 topics: ['prompting', 'rag', 'agents', 'llm_evaluation_design']
called_real_endpoint: False
RESULT: OK
negative test (drop model_version) -> ['model_version']
```

**Follow-ups:**
- *Who owns the eval gate?* Book 2 designs the eval; the platform runs it as a blocking CI step.
- *How do you handle a version retirement?* Pin, track the published date, re-run the gate on the successor, shift traffic gradually.
- *Where does cost go?* Tag or label each call path; token spend is easy to lose in a shared key.

**Common mistakes:** Letting "AI team" mean "nobody owns the platform parts"; floating on "latest" model alias; one shared API key; no quota request before launch; logging raw prompts with personal data.

### Q32 ⭐ 🔴 Vendor lock-in and portability: list what travels between Azure ML, Vertex AI and SageMaker (containers, model files in ONNX or MLflow format, KFP pipeline specs, plain Python and Terraform) and what does not (SDK job objects, registry metadata, managed feature stores, monitoring configs, IAM). Score each asset's exit cost, and say honestly that portable formats do not remove operational lock-in. Show a KFP spec compiled once and inspected, the same MLflow script on a local backend, and a YAML inventory scored by a function. Cost-benefit judgement stays opinion.
**Asked at:** Cross-cloud comparison articles (TechTarget 'Compare Google Vertex AI vs Amazon SageMaker vs Azure ML', cloudoptimo, gmicloud, superwise, a redresscompliance licensing piece; search snippets only, not opened; several authors sell competing services or advice, so conclusions treated as opinion) | Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms
**Say this first (1 line):** Containers, model files in open formats, KFP specs, plain Python and Terraform travel; SDK job objects, registry metadata, managed feature stores, monitoring configs and IAM do not, and even the portable pieces leave you with operational lock-in (on-call habits, quotas, identity design, team skills).

**Then explain:**
- Travels (with rework): a container image (push to another registry, re-auth); model files in ONNX or MLflow format (the MLflow `MLmodel` directory is plain files); a KFP pipeline spec (compiled YAML with no cloud strings, but you still need a runner: Vertex Pipelines or a Kubeflow install); plain Python and SQL; Terraform code (the language ports, the provider resources do not).
- Does not travel: `azure-ai-ml` job objects and Vertex SDK objects (rewrite); registry metadata and lineage (export by script, IDs change); managed feature stores; monitoring and alert configs; IAM roles and policies; endpoint URLs and auth that clients hard-code.
- Exit cost is a judgement. My toy scoring: portable flag, a size guess for rework, and how many other things it is tied to. The numbers are opinion, not measurements; do not quote them as facts.
- Honest point: portable formats lower the cost of moving an asset, not the cost of moving a team. Runbooks, alert routing, cost controls and the identity model are the real lock-in, and they live outside any file format.
- Failure modes: a "portable" pipeline whose components import a cloud SDK inside; MLflow model logged with a cloud-specific flavor or custom code path that is not packaged; ONNX export that loses custom ops.
- Whether lock-in is worth it is a business call (faster delivery vs future flexibility). I give a view, labelled as opinion.

**Example:** I compile one KFP pipeline and grep the YAML for `aiplatform`, `sagemaker`, `azureml`, `googleapis`: none appear, because a plain component is just an image plus args. The portability sits in the component image; the runner is the part you pick per cloud.

**Code:**
```python
# ---- q32_kfp.py ----
# q32_kfp.py - compile a KFP pipeline once, inspect the spec. Offline: no submit.
import sys, warnings; warnings.filterwarnings("ignore")
import kfp, yaml
from kfp import dsl, compiler
@dsl.component(base_image="python:3.11")
def train(lr: float, model: dsl.Output[dsl.Model]):
    open(model.path, "w").write(f"lr={lr}")
@dsl.pipeline(name="portable-train")
def pipe(lr: float = 0.1):
    train(lr=lr)
out = sys.argv[1]
compiler.Compiler().compile(pipe, out)
spec = yaml.safe_load(open(out))
print("kfp", kfp.__version__)
print("top-level keys:", sorted(spec))
print("schemaVersion:", spec["schemaVersion"], "| pipeline:", spec["pipelineInfo"]["name"])
ex = spec["deploymentSpec"]["executors"]["exec-train"]["container"]
print("executor image:", ex["image"], "| args[0..1]:", ex["args"][:2])
print("cloud-specific strings in spec:", [k for k in ("aiplatform", "googleapis", "sagemaker", "azureml") if k in open(out).read()])

# ---- q32_mlflow.py ----
# q32_mlflow.py - same tracking + model-packaging script runs on any MLflow backend; here: local sqlite.
import os, sys, warnings; warnings.filterwarnings("ignore")
os.environ["MLFLOW_DISABLE_TELEMETRY"] = "true"; os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"
import logging; logging.disable(logging.CRITICAL)
import mlflow, mlflow.pyfunc
root = sys.argv[1]; os.makedirs(root, exist_ok=True)
mlflow.set_tracking_uri(f"sqlite:///{root}/ml.db")   # swap this one line for azureml://... or a Vertex-hosted server
mlflow.set_experiment("portable")
class Doubler(mlflow.pyfunc.PythonModel):
    def predict(self, context, model_input, params=None): return [x * 2 for x in model_input]
with mlflow.start_run() as r:
    mlflow.log_param("lr", 0.1); mlflow.log_metric("auc", 0.9)
    mlflow.pyfunc.save_model(path=f"{root}/model", python_model=Doubler())
run = mlflow.get_run(r.info.run_id)
print("mlflow", mlflow.__version__, "| tracking:", mlflow.get_tracking_uri().split(":")[0])
print("params:", run.data.params, "metrics:", run.data.metrics)
print("model dir:", sorted(os.listdir(f"{root}/model")))
print(open(f"{root}/model/MLmodel").read().split("\n")[0:4])
print("reload+predict:", mlflow.pyfunc.load_model(f"{root}/model").predict([1, 2, 3]))

# ---- q32_inventory.py ----
# q32_inventory.py - score exit cost per asset. Scores are OUR judgement (1 easy .. 5 hard), not measurements.
import yaml
INV = yaml.safe_load("""
assets:
  - {name: training container image,   portable: true,  kind: container,  rework: S, coupled_to: [registry auth]}
  - {name: model files (ONNX/MLflow),  portable: true,  kind: format,     rework: S, coupled_to: []}
  - {name: KFP pipeline spec,          portable: true,  kind: spec,       rework: S, coupled_to: [component images, runner]}
  - {name: Terraform modules,          portable: partly, kind: iac,       rework: L, coupled_to: [provider resources]}
  - {name: azure-ai-ml job objects,    portable: false, kind: sdk,        rework: M, coupled_to: [workspace, compute names]}
  - {name: registry metadata/lineage,  portable: false, kind: metadata,   rework: M, coupled_to: [workspace, run ids]}
  - {name: managed feature store,      portable: false, kind: managed,    rework: XL, coupled_to: [online store, offline store, SDK]}
  - {name: monitoring configs,         portable: false, kind: managed,    rework: L, coupled_to: [baseline data, alert routes]}
  - {name: IAM roles and policies,     portable: false, kind: identity,   rework: L, coupled_to: [every service]}
""")
def score(a):
    s = {"true": 1, "partly": 3, "false": 5}[str(a["portable"]).lower()]
    s += {"S": 0, "M": 1, "L": 1, "XL": 2}[a["rework"]] + (1 if len(a["coupled_to"]) >= 3 else 0)
    return min(s, 5)
rows = sorted(((score(a), a["name"], a["rework"]) for a in INV["assets"]), reverse=True)
for s, n, d in rows: print(f"exit cost {s}/5  {n:32s} rework size (our guess) {d}")
print("average:", round(sum(r[0] for r in rows) / len(rows), 2), "| portable formats lower asset cost, not the ops cost of on-call, IAM, quotas")
```

**Output (my run):** KFP 2.17.3 in the gcp venv, MLflow 3.17.2 in the az venv with a local sqlite backend (swapping the tracking URI is the only line that changes per cloud; I did not try azureml:// or a hosted server), and the inventory in plain Python. Nothing was submitted to any cloud. An MLflow type-hint warning was filtered from the pasted output.
```
kfp 2.17.3
top-level keys: ['components', 'deploymentSpec', 'pipelineInfo', 'root', 'schemaVersion', 'sdkVersion']
schemaVersion: 2.1.0 | pipeline: portable-train
executor image: python:3.11 | args[0..1]: ['--executor_input', '{{$}}']
cloud-specific strings in spec: []
mlflow 3.17.2 | tracking: sqlite
params: {'lr': '0.1'} metrics: {'auc': 0.9}
model dir: ['MLmodel', 'conda.yaml', 'python_env.yaml', 'python_model.pkl', 'requirements.txt']
['flavors:', '  python_function:', '    cloudpickle_version: 3.1.2', '    code: null']
reload+predict: [2, 4, 6]
exit cost 5/5  registry metadata/lineage        rework size (our guess) M
exit cost 5/5  monitoring configs               rework size (our guess) L
exit cost 5/5  managed feature store            rework size (our guess) XL
exit cost 5/5  azure-ai-ml job objects          rework size (our guess) M
exit cost 5/5  IAM roles and policies           rework size (our guess) L
exit cost 4/5  Terraform modules                rework size (our guess) L
exit cost 1/5  training container image         rework size (our guess) S
exit cost 1/5  model files (ONNX/MLflow)        rework size (our guess) S
exit cost 1/5  KFP pipeline spec                rework size (our guess) S
average: 3.56 | portable formats lower asset cost, not the ops cost of on-call, IAM, quotas
```

**Follow-ups:**
- *Is KFP the common format across Vertex and Azure ML?* No: KFP runs on Vertex Pipelines and Kubeflow; Azure ML has its own component and pipeline YAML. Check current docs for any KFP support.
- *Is MLflow portable?* The tracking API and model format are widely supported; the backends and registries differ per cloud.
- *So should we avoid lock-in?* Not at all costs: avoid it where it is cheap (containers, formats), accept it where the managed service saves real work.

**Common mistakes:** Saying "we use containers so no lock-in"; scoring by gut without listing coupled pieces; ignoring IAM and monitoring; presenting my cost-benefit view as fact.

### Q33 ⭐ 🔴 Multi-cloud MLOps architecture question: a client insists on running ML on two clouds. Argue when it is sensible (acquired company, regulatory split, data residency, negotiation) and when it is not, then sketch a design with containers, Kubernetes, MLflow, an orchestrator and per-cloud identity, naming the parts that stay cloud-specific. Show the container-first pieces you can run here (an Azurite blob and a local GCS emulator both accepting the same artifact write through two small adapters) and state that nothing ran on a real cloud.
**Asked at:** Cross-cloud comparison articles (TechTarget 'Compare Google Vertex AI vs Amazon SageMaker vs Azure ML', cloudoptimo, gmicloud, superwise, a redresscompliance licensing piece; search snippets only, not opened; several authors sell competing services or advice, so conclusions treated as opinion) | Job-posting and community patterns for Azure-heavy IT-services firms and GCCs (Azure ML plus Azure DevOps) versus GCP-using product companies (Vertex plus BigQuery); inferred from search snippets about ecosystem fit, not from a verified company report | Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms
**Say this first (1 line):** Run ML on two clouds only when there is a real reason (acquired company, regulatory split, data residency, a negotiation lever); otherwise it doubles the work for little gain. If you must, go container-first: Kubernetes, MLflow, one orchestrator, thin adapters, and per-cloud identity, with the cloud-specific parts named and kept small.

**Then explain:**
- Sensible when: an acquired company already runs on the other cloud; a regulator or client requires a specific cloud or Region; data must stay where it is; you need a credible exit for contract talks.
- Not sensible when: "avoid lock-in" is the only reason; the team is small; you would use each cloud's managed services anyway (then you have two lock-ins, not zero).
- Design sketch: training and serving as containers; Kubernetes (AKS and GKE, check current docs) for serving; one MLflow tracking server and registry per environment; one orchestrator (for example Airflow or Kubeflow); artifacts behind a small storage interface; CI that builds once and pushes to both registries.
- Stays cloud-specific: identity (managed identity vs service account, federation), networking (private endpoints, PSC, VPC-SC), secrets, registries, quota and GPU availability, billing and tagging, audit logs, any managed feature store or monitoring.
- Data gravity: moving big datasets across clouds costs time and money (check current docs on egress); put compute near data, not the other way round.
- Failure modes: lowest-common-denominator design that wastes both clouds' strengths; two sets of runbooks; one team drifting to its cloud's native services; identity sprawl.

**Example:** training code calls `store.put("models/churn/1/model.bin", bytes)`. On Azure the adapter writes to Blob; on GCP to Cloud Storage. Same call, same bytes, same SHA-256 read back. Only the adapter and its credentials differ.

**Code:**
```python
# ---- q33_adapter.py ----
# q33_adapter.py - one tiny interface (put/list/get), two adapters. Run by the driver with the right venv.
# usage: q33_adapter.py azure|gcs PORT put|roundtrip KEY FILE
import sys, os, hashlib, json
class ArtifactStore:                      # the interface the training code sees
    def put(self, key, data): raise NotImplementedError
    def get(self, key): raise NotImplementedError
    def list(self): raise NotImplementedError
class AzureBlobStore(ArtifactStore):      # emulator: Azurite with its documented public dev account
    def __init__(self, port):
        from azure.storage.blob import BlobServiceClient
        key = "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=="
        cs = f"DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey={key};BlobEndpoint=http://127.0.0.1:{port}/devstoreaccount1;"
        self.c = BlobServiceClient.from_connection_string(cs).get_container_client("mlartifacts")
        try: self.c.create_container()
        except Exception: pass
    def put(self, key, data): self.c.upload_blob(key, data, overwrite=True)
    def get(self, key): return self.c.get_blob_client(key).download_blob().readall()
    def list(self): return sorted(b.name for b in self.c.list_blobs())
class GcsStore(ArtifactStore):            # emulator: gcp-storage-emulator, anonymous credentials
    def __init__(self, port):
        os.environ["STORAGE_EMULATOR_HOST"] = f"http://127.0.0.1:{port}"
        from google.cloud import storage
        from google.auth.credentials import AnonymousCredentials
        self.b = storage.Client(project="demo", credentials=AnonymousCredentials()).bucket("mlartifacts")
    def put(self, key, data): self.b.blob(key).upload_from_string(data)
    def get(self, key): return self.b.blob(key).download_as_bytes()
    def list(self): return sorted(x.name for x in self.b.client.list_blobs("mlartifacts"))
kind, port, key, path = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
store = {"azure": AzureBlobStore, "gcs": GcsStore}[kind](port)
data = open(path, "rb").read()
store.put(key, data)
back = store.get(key)
print(json.dumps({"adapter": type(store).__name__, "listed": store.list(), "sha256_in": hashlib.sha256(data).hexdigest()[:16],
                  "sha256_back": hashlib.sha256(back).hexdigest()[:16], "same": back == data}))

# ---- q33.py ----
# q33.py - driver (stdlib only): start both emulators on own ports, write the SAME artifact through both adapters, stop them.
import subprocess, time, os, sys, json, socket, tempfile
VENV = "/tmp/claude-0/b11p11"; HERE = os.path.dirname(os.path.abspath(__file__))
W = sys.argv[1]; os.makedirs(W + "/blob", exist_ok=True); os.makedirs(W + "/gcs", exist_ok=True)
AZ_PORT, GCS_PORT = 8631, 8632
art = W + "/model.bin"; open(art, "wb").write(b"fake-model-weights-v1" * 100)
def wait(port):
    for _ in range(60):
        try: socket.create_connection(("127.0.0.1", port), 0.3).close(); return True
        except OSError: time.sleep(0.5)
    return False
procs = []
try:
    procs.append(subprocess.Popen([f"{VENV}/az_npm/node_modules/.bin/azurite-blob", "--blobPort", str(AZ_PORT), "--location", W + "/blob",
        "--skipApiVersionCheck", "--silent"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
    procs.append(subprocess.Popen([f"{VENV}/emu/bin/gcp-storage-emulator", "start", "--port", str(GCS_PORT), "--default-bucket=mlartifacts",
        "--in-memory"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
    print("ports up:", wait(AZ_PORT), wait(GCS_PORT))
    for kind, port, py in (("azure", AZ_PORT, "az"), ("gcs", GCS_PORT, "gcp")):
        r = subprocess.run([f"{VENV}/{py}/bin/python", "-I", HERE + "/q33_adapter.py", kind, str(port), "models/churn/1/model.bin", art],
                           capture_output=True, text=True, timeout=120)
        print(kind, "->", r.stdout.strip() or r.stderr.strip()[-300:])
finally:
    for p in procs: p.terminate()
    for p in procs:
        try: p.wait(10)
        except Exception: p.kill()
    print("stopped; ports free:", all(subprocess.run(["bash","-c",f"! (echo > /dev/tcp/127.0.0.1/{x}) 2>/dev/null"]).returncode == 0 for x in (AZ_PORT, GCS_PORT)))
```

**Output (my run):** Azurite 3.37.0 (blob only, port 8631, its documented public dev account) and gcp-storage-emulator (port 8632, anonymous credentials) were started, used, and stopped. This shows storage API shape only: emulators do not model IAM, networking, consistency edge cases, throttling or latency. Nothing ran on a real cloud, no Kubernetes, MLflow server or orchestrator was started.
```
ports up: True True
azure -> {"adapter": "AzureBlobStore", "listed": ["models/churn/1/model.bin"], "sha256_in": "bf68f0618d63d108", "sha256_back": "bf68f0618d63d108", "same": true}
gcs -> {"adapter": "GcsStore", "listed": ["models/churn/1/model.bin"], "sha256_in": "bf68f0618d63d108", "sha256_back": "bf68f0618d63d108", "same": true}
stopped; ports free: True
```

**Follow-ups:**
- *Do you use one MLflow server for both?* Possibly, hosted near the data; cross-cloud calls add latency and an auth boundary, so decide per team.
- *What about DR across clouds?* It is a separate, expensive goal; usually multi-Region on one cloud is the better first step.
- *Who runs it?* A platform team; without one, do not start.

**Common mistakes:** "Multi-cloud" as a slogan; assuming Kubernetes removes cloud differences (identity and storage still differ); testing only the happy path with emulators and calling it proven; ignoring egress and data gravity.

### Q34 ⭐ 🔴 Migration question: move an existing SageMaker-based training and hosting setup (or on-prem Kubernetes) to Azure ML or Vertex AI. Give the inventory step, the order (data and identity first, training, registry, serving, monitoring last), dual-run and rollback, and the traps (hard-coded S3 paths, SageMaker container contracts, IAM role ARNs, endpoint URLs in clients). Write a scanner that finds provider-specific references in sample code and config and run it, and say that no migration was executed. AWS depth is Part 10.
**Asked at:** Cross-cloud comparison articles (TechTarget 'Compare Google Vertex AI vs Amazon SageMaker vs Azure ML', cloudoptimo, gmicloud, superwise, a redresscompliance licensing piece; search snippets only, not opened; several authors sell competing services or advice, so conclusions treated as opinion) | Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Job-posting and community patterns for Azure-heavy IT-services firms and GCCs (Azure ML plus Azure DevOps) versus GCP-using product companies (Vertex plus BigQuery); inferred from search snippets about ecosystem fit, not from a verified company report
**Say this first (1 line):** Inventory first, then move in this order: data and identity, training, registry, serving, monitoring last; run old and new side by side (dual-run), keep the old path as the rollback, and hunt the traps (hard-coded S3 paths, SageMaker container paths and env vars, IAM role ARNs, endpoint URLs in clients).

**Then explain:**
- Inventory: every training script, pipeline, endpoint, schedule, IAM role, bucket, image, client of each endpoint, and who owns it. A regex scan finds code references; the console and IaC find the rest.
- Order and why: data and identity first (nothing runs without them; set up storage, access, network); training next (offline, easy to compare); registry (re-register model artifacts, keep version mapping); serving (the risky part, with traffic); monitoring last (it needs live traffic and a baseline).
- Dual-run: train on both, compare metrics; serve shadow traffic or a small split; roll back by routing clients back to the old endpoint. Keep the old stack until a stable window passes.
- Traps: `s3://` paths in code and configs; SageMaker container contract (`/opt/ml/...`, `SM_*` variables, `serve` entrypoint) differs from the target's contract, so re-read it for Azure ML or Vertex custom containers (check current docs); IAM role ARNs and policies do not translate; clients with the SageMaker runtime URL and SigV4 auth; instance types have no 1:1 map; AWS region strings in env vars.
- From on-prem Kubernetes it is easier on containers, harder on identity and storage mounts.
- AWS depth is Part 10; this answer stays on the move.

**Example:** the scanner finds 11 hits across 4 files in my sample. The client file's hit is the most dangerous: a hard-coded endpoint URL means every client must be redeployed at cutover, so put it behind config or a gateway first.

**Code:**
```python
# ---- q34_scan.py ----
# q34_scan.py - find AWS/SageMaker-specific references in a code+config tree. Regex scan, so false positives and misses are possible.
import re, sys, os, collections
RULES = [
 ("storage path",      r"s3a?://[\w.\-/]+",                         "use a data-URI variable; Azure: azureml:// or abfss://, GCP: gs://"),
 ("sdk import",        r"^\s*(import|from)\s+(boto3|botocore|sagemaker)\b", "wrap behind an interface; Azure: azure-ai-ml, GCP: google-cloud-aiplatform"),
 ("IAM role ARN",      r"arn:aws:iam::\d{12}:[^\s\"']+",                  "map to managed identity (Azure) or service account (GCP); do not copy the string"),
 ("container contract",r"/opt/ml/[\w/]+|\bSM_[A-Z_]+",              "SageMaker paths and env vars; re-read the target's input/output contract"),
 ("endpoint URL",      r"https://runtime\.sagemaker\.[\w.\-]+/\S+", "clients must call a new URL and auth; put the URL in config or behind a gateway"),
 ("ECR image",         r"\d{12}\.dkr\.ecr\.[\w\-]+\.amazonaws\.com/\S+", "push to ACR (Azure) or Artifact Registry (GCP)"),
 ("instance type",     r"\bml\.[a-z0-9]+\.\w+",                     "no 1:1 mapping; pick the target's machine type from current docs"),
 ("AWS env var",       r"\bAWS_[A-Z_]+",                            "remove; use the target's identity mechanism"),
]
hits = []
for dp, _, fs in os.walk(sys.argv[1]):
    for f in sorted(fs):
        p = os.path.join(dp, f)
        for n, line in enumerate(open(p, errors="ignore"), 1):
            for name, rx, hint in RULES:
                for m in re.finditer(rx, line, re.M):
                    hits.append((os.path.relpath(p, sys.argv[1]), n, name, m.group(0).strip()[:60], hint))
for h in sorted(hits): print(f"{h[0]}:{h[1]:<3} [{h[2]}] {h[3]}")
c = collections.Counter(h[2] for h in hits)
print("\nsummary:", dict(c), "| files with hits:", len({h[0] for h in hits}), "| clean.py hits:", sum(h[0] == "clean.py" for h in hits))
```

**Output (my run):** `python3 -I q34_scan.py q34_sample` over five tiny invented files (fake account id, no real names). It is a regex scan: it missed `import os, boto3` on train.py line 1 and the `boto3.client(...)` call, so false negatives exist; treat the report as a start. No migration, no AWS or Azure or GCP call was made.
```
Dockerfile:1   [ECR image] 123456789012.dkr.ecr.ap-south-1.amazonaws.com/churn-train:la
Dockerfile:2   [container contract] /opt/ml/code/serve
client.py:2   [endpoint URL] https://runtime.sagemaker.ap-south-1.amazonaws.com/endpoints
deploy.yaml:1   [storage path] s3://acme-ml-models/churn/v7/model.tar.gz
deploy.yaml:2   [instance type] ml.m5.xlarge
deploy.yaml:4   [AWS env var] AWS_DEFAULT_REGION
train.py:2   [sdk import] import sagemaker
train.py:3   [storage path] s3://acme-ml-data/churn/train/
train.py:4   [container contract] /opt/ml/model
train.py:4   [container contract] SM_MODEL_DIR
train.py:6   [IAM role ARN] arn:aws:iam::123456789012:role/SageMakerExecRole

summary: {'ECR image': 1, 'container contract': 3, 'endpoint URL': 1, 'storage path': 2, 'instance type': 1, 'AWS env var': 1, 'sdk import': 1, 'IAM role ARN': 1} | files with hits: 4 | clean.py hits: 0
```

**Follow-ups:**
- *How do you cut over?* Dual-run, then a gradual traffic shift or a DNS or gateway switch, with rollback to the old endpoint.
- *What about the model files?* If they are framework formats (ONNX, native) they move; check the new serving container's expected layout.
- *When do you migrate at all?* When there is a business reason (ecosystem, contract, residency); "it is shinier" is not one.

**Common mistakes:** Starting with serving; no rollback; trusting a regex scan as complete; forgetting clients and schedules; copying IAM policies instead of redesigning identity; deleting the old stack on cutover day.

### Q35 ⭐ 🔴 Governance across clouds: model lineage, approvals, audit logs and ownership when Azure ML and Vertex AI are both in use. What each cloud gives you (workspace and registry audit trails, Azure activity logs and Purview boundaries, Google Cloud Audit Logs, Vertex ML Metadata lineage) and what you must add yourself (a model card convention, an owner field, a single catalogue). Design a minimal common metadata schema, validate sample records with pyyaml or pydantic, and mark the cloud-specific log sources as not executed. Part 12 owns security and system design in depth.
**Asked at:** Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs') | Cross-cloud comparison articles (TechTarget 'Compare Google Vertex AI vs Amazon SageMaker vs Azure ML', cloudoptimo, gmicloud, superwise, a redresscompliance licensing piece; search snippets only, not opened; several authors sell competing services or advice, so conclusions treated as opinion) | Job-posting and community patterns for Azure-heavy IT-services firms and GCCs (Azure ML plus Azure DevOps) versus GCP-using product companies (Vertex plus BigQuery); inferred from search snippets about ecosystem fit, not from a verified company report
**Say this first (1 line):** Each cloud gives you pieces (registry versions, run and lineage records, audit logs), but a clean cross-cloud story needs a catalogue you own: one model ID, an owner, an approver, a model card link and lineage refs in one common schema.

**Then explain:**
- Azure side (check current docs, not executed): workspace and registry hold model versions, jobs and some lineage; Azure Activity Log records control-plane changes; Microsoft Purview can catalogue data assets but has its own scope boundaries.
- Google side (check current docs, not executed): Vertex Model Registry and ML Metadata track artifacts and lineage between pipeline steps; Cloud Audit Logs record admin and data access depending on what is enabled.
- Gaps you fill yourself: a common model ID across clouds; a required owner and a different approver for prod; a model card convention (a link per version, not a PDF in someone's drive); one catalogue that both clouds publish into (even a repo of YAML files plus CI).
- Governance rules as code: prod needs an approver who is not the owner, a model card and non-empty lineage. Validate on every promotion.
- Failure modes: two registries that disagree; approvals in chat only; audit logs retained shorter than the model's life; owner who left the company; lineage pointing to deleted data.
- Part 12 covers security and system design in depth; this stays on records.

**Example:** `churn v8` was submitted with the same person as owner and approver; the validator rejects it. `rec v1` claims cloud gcp with an `azureml:` reference and empty lineage; the field checks reject it first (pydantic reports field errors before running the record-level rules, so the cloud/ref mismatch check only runs once fields pass).

**Code:**
```python
# ---- q35.py ----
# q35.py - minimal common model-metadata record for a cross-cloud catalogue; validate sample records with pydantic + pyyaml.
import yaml, pydantic
from typing import Literal, Optional
from pydantic import BaseModel, Field, model_validator
print("pydantic", pydantic.VERSION)
class Lineage(BaseModel):
    training_data: list[str] = Field(min_length=1)      # asset refs (azureml:name:ver / bq or gs URI)
    code_commit: str = Field(pattern=r"^[0-9a-f]{7,40}$")
    pipeline_run: Optional[str] = None
class ModelRecord(BaseModel):
    model_id: str                                       # OUR id, same across clouds
    version: int = Field(ge=1)
    cloud: Literal["azure", "gcp"]
    platform_ref: str                                   # the cloud's own handle
    owner: str = Field(pattern=r"^[^@\s]+@[^@\s]+$")
    approver: Optional[str] = None
    stage: Literal["dev", "staging", "prod"]
    risk_tier: Literal["low", "medium", "high"]
    model_card_url: Optional[str] = None
    lineage: Lineage
    @model_validator(mode="after")
    def rules(self):
        prefix = {"azure": "azureml:", "gcp": "projects/"}[self.cloud]
        if not self.platform_ref.startswith(prefix): raise ValueError(f"platform_ref must start with {prefix!r} for {self.cloud}")
        if self.stage == "prod":
            if not self.approver: raise ValueError("prod needs an approver")
            if self.approver == self.owner: raise ValueError("approver must differ from owner")
            if not self.model_card_url: raise ValueError("prod needs a model card")
        return self
RECORDS = yaml.safe_load("""
- {model_id: churn, version: 7, cloud: azure, platform_ref: "azureml:churn:7", owner: asha@corp.example, approver: ravi@corp.example,
   stage: prod, risk_tier: medium, model_card_url: "https://wiki.example/cards/churn-7",
   lineage: {training_data: ["azureml:churn-data:12"], code_commit: 3fa91bc, pipeline_run: "run-001"}}
- {model_id: fraud, version: 3, cloud: gcp, platform_ref: "projects/p/locations/asia-south1/models/123", owner: dev@corp.example,
   approver: meera@corp.example, stage: prod, risk_tier: high, model_card_url: "https://wiki.example/cards/fraud-3",
   lineage: {training_data: ["bq://p.ds.txns_v5"], code_commit: 9d0c2e4a}}
- {model_id: churn, version: 8, cloud: azure, platform_ref: "azureml:churn:8", owner: asha@corp.example, approver: asha@corp.example,
   stage: prod, risk_tier: medium, model_card_url: "https://wiki.example/cards/churn-8",
   lineage: {training_data: ["azureml:churn-data:13"], code_commit: 77aa12f}}
- {model_id: rec, version: 1, cloud: gcp, platform_ref: "azureml:rec:1", owner: dev@corp.example,
   stage: prod, risk_tier: low, lineage: {training_data: [], code_commit: "xyz"}}
""")
for r in RECORDS:
    try:
        ModelRecord(**r); print(f"OK   {r['model_id']} v{r['version']} ({r['cloud']})")
    except pydantic.ValidationError as e:
        msgs = sorted({f"{'.'.join(map(str, x['loc'])) or 'record'}: {x['msg'].replace('Value error, ', '')}" for x in e.errors()})
        print(f"FAIL {r['model_id']} v{r['version']} ({r['cloud']})"); [print("     -", m) for m in msgs]
```

**Output (my run):** pydantic 2.13.5 and pyyaml under `python3 -I`. Four invented records; two pass, two fail for the reasons printed. The Azure Activity Log, Purview, Google Cloud Audit Logs and Vertex ML Metadata sources were not executed: no workspace, project or log was read.
```
pydantic 2.13.5
OK   churn v7 (azure)
OK   fraud v3 (gcp)
FAIL churn v8 (azure)
     - record: approver must differ from owner
FAIL rec v1 (gcp)
     - lineage.code_commit: String should match pattern '^[0-9a-f]{7,40}$'
     - lineage.training_data: List should have at least 1 item after validation, not 0
```

**Follow-ups:**
- *Single source of truth?* The cloud registry holds artifacts; your catalogue holds the governance facts and points to it.
- *Who approves?* A named role, not the author; the schema enforces a different person for prod.
- *How long to keep audit logs?* Per policy and law; check current retention settings per cloud.

**Common mistakes:** Assuming the cloud's lineage covers the other cloud; no owner field; approval as a chat message; model card written once and never versioned; schema so heavy nobody fills it.

