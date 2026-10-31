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
