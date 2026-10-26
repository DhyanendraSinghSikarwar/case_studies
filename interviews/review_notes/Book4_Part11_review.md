# Book 4 Part 11 review (Wave C)

Date: 2026-10-26. Reviewer: lead session (independent of the four answer agents). Scope: 35 questions, Q1-Q35 (Azure ML and GCP Vertex AI, with comparison to AWS SageMaker). Band per plan.md: Rs 30-80 LPA; no salary figures; no prices.

## Process
Four agents answered Q1-9, Q10-18, Q19-27, Q28-35; merged by heading: 35 of 35 merged, 0 skipped, 0 pending. No spend-limit stops. Only fake credentials were used. The answer agents were told not to call any real Azure or Google endpoint; the Wave A agent had made one real unauthenticated `PipelineJob.submit` call (400 then 401 from Google's public endpoint, no credentials), which is recorded in the sources note and was not repeated. No emulator servers were left running.

## Structure checks (scripted by the lead)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q35; star order and counts 14 / 15 / 6 | pass |
| All 7 template labels present and in order; code fences balanced | pass for all 35 |

The lead did not re-run the scripts (they depend on the shared Azure and GCP venvs and local emulators); pasted outputs come from each agent's real runs (`python3 -I`, azure-ai-ml 1.35.2, azure-identity 1.26.0, google-cloud-aiplatform 1.165.1, kfp 2.17.3, google-cloud-pipeline-components 2.22.0, mlflow 3.17.2, azureml-mlflow 1.60.0, Azurite 3.37.0, gcp-storage-emulator), with code and outputs in each agent's `code/` and `out/` folders.

## What really ran (all offline)
Azure SDK v2: Workspace, command job, dsl.pipeline, components, environments, AmlCompute and ComputeInstance, ManagedOnlineEndpoint and deployments, BatchEndpoint and ModelBatchDeployment, Data and datastores, automl.classification, sweep jobs (Bayesian and random with Bandit), MonitorSchedule, FeatureStore entities, managed-network workspace; YAML jobs, components and pipelines loaded and `_validate()`d (a misspelt key raised "Unknown field"). Vertex: CustomJob, HyperparameterTuningJob, PipelineJob, AutoMLTabularTrainingJob, Endpoint and BatchPredictionJob protos built with `AnonymousCredentials`; KFP compile to JSON and YAML; `kfp.local` SubprocessRunner. MLflow on local sqlite and with an `azureml://` URI (the client only accepts the scheme). Azurite and gcp-storage-emulator round trips of the same artifact (identical SHA-256; storage API shape only). Pure-Python checkers and decision functions (traffic splits, role matrix, region and data-class rules, network and notebook-config lints, scoring and exit-cost functions, a regex scanner, a pydantic metadata schema).

## Findings kept in the text (observed)
- Without `init` and credentials, Vertex `PipelineJob`/`CustomJob` fail (missing project, then DefaultCredentialsError); with `init` plus `AnonymousCredentials` they build offline. `CustomJob` takes `service_account` and `network` at run or submit, not in the constructor.
- Offline entities accept things real services would reject (AmlCompute min greater than max, a command that refers to an undefined input, a misspelt step-output binding); `PredictionDriftSignal` needed explicit metric thresholds; the Azure environment loader failed on a missing docker build-context folder.
- The same weighted-scoring inputs with two client weightings flip the winner from Azure ML to Vertex (weights are the argument); a regex migration scanner missed `import os, boto3` and `boto3.client(...)`.
- mlflow 3.17.2 plain file store raises unless `MLFLOW_ALLOW_FILE_STORE` is set; installing azureml-mlflow downgraded azure-storage-blob (pip conflict warning).

## Not executed
All real Azure and Google services, the `az` CLI and `az ml` (not installed), gcloud beyond `--help`, endpoints, training, AutoML, Responsible AI dashboard, monitoring, Feature Store, BigQuery ML, Azure OpenAI and Gemini, RBAC and IAM enforcement, private networking and VPC-SC perimeters, quotas, Regions, MLflow against a real workspace, and all prices. Cloud log sources (Azure Activity Log, Purview, Cloud Audit Logs, ML Metadata) are named only.

## Hedged ("check current docs")
Dates from search snippets (Azure SDK v1 and Vertex Feature Store legacy deprecation and sunset dates, page not opened), Region availability, India DPDP cross-border rules (not legal advice), Azure `mirror_traffic` syntax, Bayesian sweep and early termination, Vertex service accounts inside VPC-SC, `AIP_*` variable names, `mini_batch_size` semantics, `gcloud` canary flags (left out). The Q1 service mapping is the writer's own summary.

## Evidence limits
No candidate-reported questions found; the one WebFetch failed, so every source is a snippet (one editorial question list, comparison articles, vendor docs, job-posting patterns; DP-100/AI-300 and Google PMLE only as source types). See research_notes/Book4_Part11_sources.md.
