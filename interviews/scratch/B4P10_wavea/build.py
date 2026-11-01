import os, sys
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0,'scratch/B4P10_wavea')
from qs import QS
order={'🟢':0,'🟡':1,'🔴':2}
QS=sorted(QS,key=lambda q:(-q[0],order[q[1]]))   # stable: stars 3,2,1; easy to hard inside a star
n=len(QS)
c=[sum(1 for q in QS if q[0]==s) for s in (3,2,1)]
print(n,c)
assert n==50, n
assert [q[0] for q in QS]==sorted([q[0] for q in QS],reverse=True)
assert sum(c)==50 and c==[20,20,10], c
assert all(q[1] in '🟢🟡🔴' for q in QS)
assert len({q[2] for q in QS})==50
for s in (3,2,1):
    d=[order[q[1]] for q in QS if q[0]==s]
    assert d==sorted(d),(s,d)
assert not any(ch.isdigit() and False for ch in '')
hdr=f"""# Book 4 — Part 10: AWS for ML: S3, EC2, Lambda, SageMaker, ECR/ECS, IAM

**Topic:** AWS for ML engineers: S3 (storage classes, versioning, lifecycle, presigned URLs, multipart upload, consistency, bucket policies, encryption, data lake layout, read patterns for training data), EC2 (instance families, GPU instances, spot and checkpointing, AMIs, EBS and instance store, placement groups, Auto Scaling groups), Lambda (limits, cold starts, container images, layers, event sources, concurrency), SageMaker (training jobs, processing, pipelines, real-time, serverless, asynchronous and batch transform inference, multi-model endpoints, model registry, Studio, managed spot training, Model Monitor, Feature Store and Ground Truth at service level), ECR, ECS, Fargate and EKS comparison, IAM (users, roles, policies, least privilege, trust policies, STS assume-role, instance profiles, IRSA, permission boundaries, SCPs, ABAC, policy evaluation logic), VPC basics (subnets, security groups, NACLs, endpoints, NAT), CloudWatch and CloudTrail, Step Functions, Batch, Athena, Glue and Redshift at boundary level, Secrets Manager, Parameter Store and KMS, cost basics without prices, Bedrock at the boundary with Book 2, and design and incident questions
**Target:** 50  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-26  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 1 owns Git, pre-commit and pytest for ML code; Part 2 owns Docker; Part 3 owns Kubernetes and Helm; Part 4 owns DVC, MLflow and registry basics; Part 5 owns pipelines, scheduling and orchestration (Airflow, Prefect, Kubeflow); Part 6 owns serving mechanics, latency and error metrics, shadow, canary and rollout; Part 7 owns CI workflows, promotion gates and GitHub OIDC to AWS; Part 8 owns monitoring, drift detection and alerting; Part 9 owns feature-store concepts, Kafka and Spark; Part 11 owns Azure ML and GCP Vertex AI; Part 12 owns cost, security and system design in depth; Book 1 owns ML theory; Book 2 owns LLM serving, RAG and Bedrock usage; Book 3 owns SQL and pandas; Book 6 owns product and business. This part owns AWS services and IAM as used to store data, train, host and secure ML systems; where a question touches another part it says so and stays at service level.

Evidence limits: WebFetch of docs.aws.amazon.com failed (getaddrinfo ENOTFOUND), so no AWS page was opened and every external source is a WebSearch snippet only (see research_notes/Book4_Part10_sources.md). No page was found that reports exact AWS-for-ML questions asked by a named company, so 'Asked at' tags name source types (prep-site question banks, vendor docs, job postings, certification-style families), not verified company reports. Execution limit: no AWS account or credentials exist; in a fresh venv under /tmp/claude-0/b10p10 (Python 3.13.17) pip installed boto3 1.43.118, botocore 1.43.118, moto 5.2.4 (plus moto[server] and Flask 3.1.3) and awscli 1.46.2 (its own botocore 1.43.62), so Wave B can really run boto3 and aws CLI calls against moto with fake keys in decorator mode and in server mode (moto_server on a local port; aws --endpoint-url worked for S3, IAM, STS and SageMaker list calls). In moto these ran: S3 versioning, delete markers, lifecycle, default KMS encryption, multipart (EntityTooSmall for small parts), presigned GET and POST, conditional put, Glacier-class GET raising InvalidObjectState, explicit Deny bucket policy enforced as 403; IAM roles, inline policies, permissions boundary, instance profiles, access-key deactivation; STS assume_role (trust policy not checked: a role trusting another account was assumed); SQS visibility timeout; ECR repo with immutable tags and lifecycle; ECS Fargate task definition; Lambda create, config, layers and reserved concurrency (invoke needs Docker and did not execute code); SageMaker training, processing, transform, model, endpoint config (real-time, async, serverless shapes), endpoint, model package group with approval, pipeline, feature group (needs offline store config) and invoke_endpoint (canned 'body'); CloudWatch metrics and alarms; Secrets Manager, SSM, KMS (generate_data_key, grants); Step Functions, EC2, VPC, subnets, security groups, S3 gateway endpoint, spot request, Auto Scaling, Athena, Glue, Redshift records, Organizations SCP objects. In moto these were NOT implemented or not enforced: IAM simulate_principal_policy, CloudTrail lookup_events, SageMaker monitoring schedules, labeling jobs and the feature-store runtime, EC2 placement groups, Bedrock list_foundation_models, Lambda real execution, SageMaker real training and endpoints, real networking and VPC routing, and IAM policy enforcement unless auth enforcement is switched on (it denied an implicit-deny CreateBucket when set_initial_no_auth_action_count was used). A pure-Python IAM evaluator sketch is in scratch/B4P10_wavea/iam_eval_sketch.py (13 cases pass; simplified). Real AWS behaviour, quotas, limits, Regions, networking and prices were not executed: write them from official docs, hedge as 'check current docs', and give no prices. The sandbox environment variables hold placeholder AWS keys; no real AWS call was made.

---
"""
out=[hdr]
for i,(s,d,q,a) in enumerate(QS,1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q.strip()}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
txt=''.join(out)
assert txt.count('<!-- ANSWER_PENDING -->')==50 and txt.count('**Asked at:**')==50
assert f"(⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})" in txt
assert txt.count('\n### Q')==50
open('Book4_MLOps/Book4_MLOps_Part10.md','w',encoding='utf-8',newline='\n').write(txt)
rows=''.join(f"| B4P10-Q{i} | 10 | {q.strip()} |\n" for i,(s,d,q,a) in enumerate(QS,1))
open('scratch/B4P10_wavea/index_rows.txt','w',encoding='utf-8',newline='\n').write(rows)
print(n,c)
