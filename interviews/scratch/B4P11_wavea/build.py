import os, sys
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0,'scratch/B4P11_wavea')
from qs import QS
order={'🟢':0,'🟡':1,'🔴':2}
QS=sorted(QS,key=lambda q:(-q[0],order[q[1]]))   # stable: stars 3,2,1; easy to hard inside a star
n=len(QS)
c=[sum(1 for q in QS if q[0]==s) for s in (3,2,1)]
print(n,c)
assert n==35, n
assert [q[0] for q in QS]==sorted([q[0] for q in QS],reverse=True)
assert sum(c)==35
assert all(q[1] in order for q in QS)
assert len({q[2] for q in QS})==35
for s in (3,2,1):
    d=[order[q[1]] for q in QS if q[0]==s]
    assert d==sorted(d),(s,d)
hdr=f"""# Book 4 — Part 11: Azure Machine Learning and Google Cloud Vertex AI (with a cross-cloud comparison)

**Topic:** Azure ML (workspace, compute instances and clusters, datastores and data assets, environments, jobs, components and pipelines in YAML v2 and SDK v2, managed online and batch endpoints, model registry, MLflow integration, AutoML, sweep jobs, Responsible AI dashboard, managed identity and RBAC, managed virtual network and private endpoints, Azure DevOps and GitHub integration, SDK v1 to v2 migration, Azure OpenAI at the boundary only), Google Vertex AI (Workbench, custom training, Vertex Pipelines and KFP, online and batch prediction, Model Registry, Feature Store, Experiments, Model Monitoring, Vizier tuning, AutoML, BigQuery ML at the boundary, IAM and service accounts, VPC Service Controls and Private Service Connect, Gemini at the boundary only), and the cross-cloud layer (service mapping with AWS SageMaker by concept only, vendor lock-in, multi-cloud, portability through containers, MLflow and KFP, identity models, networking, governance, India Region and data-residency concerns, choosing a platform, migration)

**Target:** 35  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-26  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 1 owns Git and pytest for ML code; Part 2 owns Docker; Part 3 owns Kubernetes and Helm; Part 4 owns DVC, MLflow and registry basics; Part 5 owns pipelines and orchestration concepts including KFP; Part 6 owns serving mechanics, latency, shadow, canary and rollout; Part 7 owns CI workflows and promotion gates; Part 8 owns monitoring, drift detection and alerting; Part 9 owns feature-store concepts, Kafka and Spark; Part 10 owns AWS and SageMaker depth (compared here by concept only); Part 12 owns cost, security and system design in depth; Book 1 owns ML theory; Book 2 owns LLM serving, RAG and the use of Azure OpenAI or Gemini; Book 3 owns SQL; Book 6 owns product and business. This part owns the managed Azure ML and Vertex AI services as used to train, register, deploy and govern models, and how to compare, choose between and move across clouds; where a question touches another part it says so and stays at service level.

Evidence limits: WebFetch of learn.microsoft.com failed (getaddrinfo ENOTFOUND), so no vendor page was opened and every external source is a WebSearch snippet only (see research_notes/Book4_Part11_sources.md). No page was found that reports exact Azure ML or Vertex AI questions asked by a named company, so 'Asked at' tags name source types (prep-site question lists, vendor docs, comparison articles, job-posting patterns, certification-style families), not verified company reports. Execution limit: no Azure or Google credentials exist and none were used. In fresh venvs under /tmp/claude-0/b11p11 (Python 3.13.17) pip installed azure-ai-ml 1.35.2, azure-identity 1.26.0 (azure-storage-blob 12.31.0, later downgraded to 12.19.0 when mlflow 3.17.2 and azureml-mlflow 1.60.0 were added), google-cloud-aiplatform 1.165.1, google-cloud-storage 3.17.1, kfp 2.17.3, kfp-pipeline-spec 2.17.3 and google-cloud-pipeline-components 2.22.0, gcp-storage-emulator 2026.7.19 (own venv), and npm installed azurite 3.37.0 (node v22.22.0, npm 10.9.4). Ran offline and for real: Azure SDK v2 object construction (Environment, command job, dsl.pipeline, ManagedOnlineEndpoint, ManagedOnlineDeployment, AmlCompute, Data, Model, BatchEndpoint, Workspace entity, automl.classification, sweep with Bandit policy), load_job, load_component, load_online_endpoint, load_online_deployment and load_environment on YAML with the SDK's offline _validate() (a misspelt key raised ValidationError 'Unknown field'; endpoint, deployment and environment entities have no _validate); DefaultAzureCredential constructs but get_token fails with no credentials; MLClient(credential=None) raises ValueError; mlflow with the azureml:// tracking URI scheme accepted and a real run logged to a local sqlite store (the plain file store is gated behind MLFLOW_ALLOW_FILE_STORE in mlflow 3.17.2); Azurite blob emulator upload and download with the public development account key through azure-storage-blob; KFP compile to JSON and YAML for a two-component pipeline and for google-cloud-pipeline-components CustomTrainingJobOp and EndpointCreateOp, the KFP local SubprocessRunner (add(1,2) gave 3), Vertex CustomJobSpec proto built and printed with to_json, gcp-storage-emulator accepting google-cloud-storage writes and reads through STORAGE_EMULATOR_HOST, and gcloud 570.0.0 help text. Findings: constructing aiplatform.PipelineJob, CustomJob or Endpoint without init and credentials fails (GoogleAuthError for project, then DefaultCredentialsError); with init plus google.auth AnonymousCredentials the objects build offline, CustomJob and HyperparameterTuningJob build, but PipelineJob.submit tried a real Cloud Storage call and returned 400 for a too-short bucket name and 401 for the API, so anonymous calls reached public Google endpoints and were refused; CustomJob takes service_account and network at run or submit, not in the constructor; azure hosts were refused by the sandbox proxy (management.azure.com connect_rejected). NOT executed: every real Azure or Google call, workspaces, projects, jobs, pipelines, endpoints, quotas, Regions, networking, IAM and RBAC enforcement, AutoML, Responsible AI dashboard, monitoring, Feature Store, BigQuery ML, Azure OpenAI and Gemini, the az CLI and az ml extension (not installed), and all prices. Azurite and gcp-storage-emulator mock storage APIs only: they do not model Entra, IAM, private networking or consistency. Write cloud behaviour from official docs, hedge as 'check current docs', give no prices, and label what ran against what.

---
"""
out=[hdr]
for i,(s,d,q,a) in enumerate(QS,1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q.strip()}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
txt=''.join(out)
assert txt.count('<!-- ANSWER_PENDING -->')==35 and txt.count('**Asked at:**')==35
assert f"(⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})" in txt
assert txt.count('\n### Q')==35
open('Book4_MLOps/Book4_MLOps_Part11.md','w',encoding='utf-8',newline='\n').write(txt)
rows=''.join(f"| B4P11-Q{i} | 11 | {q.strip()} |\n" for i,(s,d,q,a) in enumerate(QS,1))
open('scratch/B4P11_wavea/index_rows.txt','w',encoding='utf-8',newline='\n').write(rows)
print(n,c)
