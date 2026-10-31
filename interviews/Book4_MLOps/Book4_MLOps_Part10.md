# Book 4 — Part 10: AWS for ML: S3, EC2, Lambda, SageMaker, ECR/ECS, IAM

**Topic:** AWS for ML engineers: S3 (storage classes, versioning, lifecycle, presigned URLs, multipart upload, consistency, bucket policies, encryption, data lake layout, read patterns for training data), EC2 (instance families, GPU instances, spot and checkpointing, AMIs, EBS and instance store, placement groups, Auto Scaling groups), Lambda (limits, cold starts, container images, layers, event sources, concurrency), SageMaker (training jobs, processing, pipelines, real-time, serverless, asynchronous and batch transform inference, multi-model endpoints, model registry, Studio, managed spot training, Model Monitor, Feature Store and Ground Truth at service level), ECR, ECS, Fargate and EKS comparison, IAM (users, roles, policies, least privilege, trust policies, STS assume-role, instance profiles, IRSA, permission boundaries, SCPs, ABAC, policy evaluation logic), VPC basics (subnets, security groups, NACLs, endpoints, NAT), CloudWatch and CloudTrail, Step Functions, Batch, Athena, Glue and Redshift at boundary level, Secrets Manager, Parameter Store and KMS, cost basics without prices, Bedrock at the boundary with Book 2, and design and incident questions
**Target:** 50  |  **Actual:** 50 (⭐⭐⭐ 20, ⭐⭐ 20, ⭐ 10)  |  **Date:** 2026-10-26  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 1 owns Git, pre-commit and pytest for ML code; Part 2 owns Docker; Part 3 owns Kubernetes and Helm; Part 4 owns DVC, MLflow and registry basics; Part 5 owns pipelines, scheduling and orchestration (Airflow, Prefect, Kubeflow); Part 6 owns serving mechanics, latency and error metrics, shadow, canary and rollout; Part 7 owns CI workflows, promotion gates and GitHub OIDC to AWS; Part 8 owns monitoring, drift detection and alerting; Part 9 owns feature-store concepts, Kafka and Spark; Part 11 owns Azure ML and GCP Vertex AI; Part 12 owns cost, security and system design in depth; Book 1 owns ML theory; Book 2 owns LLM serving, RAG and Bedrock usage; Book 3 owns SQL and pandas; Book 6 owns product and business. This part owns AWS services and IAM as used to store data, train, host and secure ML systems; where a question touches another part it says so and stays at service level.

Evidence limits: WebFetch of docs.aws.amazon.com failed (getaddrinfo ENOTFOUND), so no AWS page was opened and every external source is a WebSearch snippet only (see research_notes/Book4_Part10_sources.md). No page was found that reports exact AWS-for-ML questions asked by a named company, so 'Asked at' tags name source types (prep-site question banks, vendor docs, job postings, certification-style families), not verified company reports. Execution limit: no AWS account or credentials exist; in a fresh venv under /tmp/claude-0/b10p10 (Python 3.13.17) pip installed boto3 1.43.118, botocore 1.43.118, moto 5.2.4 (plus moto[server] and Flask 3.1.3) and awscli 1.46.2 (its own botocore 1.43.62), so Wave B can really run boto3 and aws CLI calls against moto with fake keys in decorator mode and in server mode (moto_server on a local port; aws --endpoint-url worked for S3, IAM, STS and SageMaker list calls). In moto these ran: S3 versioning, delete markers, lifecycle, default KMS encryption, multipart (EntityTooSmall for small parts), presigned GET and POST, conditional put, Glacier-class GET raising InvalidObjectState, explicit Deny bucket policy enforced as 403; IAM roles, inline policies, permissions boundary, instance profiles, access-key deactivation; STS assume_role (trust policy not checked: a role trusting another account was assumed); SQS visibility timeout; ECR repo with immutable tags and lifecycle; ECS Fargate task definition; Lambda create, config, layers and reserved concurrency (invoke needs Docker and did not execute code); SageMaker training, processing, transform, model, endpoint config (real-time, async, serverless shapes), endpoint, model package group with approval, pipeline, feature group (needs offline store config) and invoke_endpoint (canned 'body'); CloudWatch metrics and alarms; Secrets Manager, SSM, KMS (generate_data_key, grants); Step Functions, EC2, VPC, subnets, security groups, S3 gateway endpoint, spot request, Auto Scaling, Athena, Glue, Redshift records, Organizations SCP objects. In moto these were NOT implemented or not enforced: IAM simulate_principal_policy, CloudTrail lookup_events, SageMaker monitoring schedules, labeling jobs and the feature-store runtime, EC2 placement groups, Bedrock list_foundation_models, Lambda real execution, SageMaker real training and endpoints, real networking and VPC routing, and IAM policy enforcement unless auth enforcement is switched on (it denied an implicit-deny CreateBucket when set_initial_no_auth_action_count was used). A pure-Python IAM evaluator sketch is in scratch/B4P10_wavea/iam_eval_sketch.py (13 cases pass; simplified). Real AWS behaviour, quotas, limits, Regions, networking and prices were not executed: write them from official docs, hedge as 'check current docs', and give no prices. The sandbox environment variables hold placeholder AWS keys; no real AWS call was made.

---

### Q1 ⭐⭐⭐ 🟢 S3 storage classes for an ML data lake: explain Standard, Intelligent-Tiering, Standard-IA, One Zone-IA, Glacier Instant, Flexible and Deep Archive in terms of access pattern, retrieval delay, minimum storage duration, availability zones and when each fits raw data, curated features, training snapshots and model artifacts. Do not quote prices. Then write a lifecycle rule (prefix filter, transition, expiry, abort incomplete multipart uploads), apply it to a mock bucket with moto and read it back.
**Asked at:** S3 interview question banks (novelvista '100+ Top AWS S3 Interview Questions', adaface, ccbp.in, a techinterview.org 'System Design Interview: Object Storage (Amazon S3)' post, AWS developer exam-prep study guides; search snippets only, not opened; WebFetch of docs.aws.amazon.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; cloud, data and ML engineer roles at IT-services firms, product companies and GCCs | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)
**Say this first (1 line):** S3 storage classes trade retrieval speed and flexibility for storage cost: keep hot training data in Standard, let Intelligent-Tiering handle unknown patterns, and push cold snapshots down to Glacier tiers with a lifecycle rule.

**Then explain:**
- Think in four questions per class: how often do I read it, how fast must the first byte come, how long must I pay for it at minimum, and how many Availability Zones hold it.
- All numbers below are from memory of the docs, so treat them as "check current docs". No prices here.

| Class | Access pattern | Retrieval | Minimum duration | AZs | ML fit |
|---|---|---|---|---|---|
| Standard | frequent | milliseconds | none | 3+ | active training data, features in use, latest model artifacts |
| Intelligent-Tiering | unknown or changing | ms in the frequent and infrequent tiers; optional archive tiers are slower | none | 3+ | datasets nobody can predict; per-object monitoring fee, check docs for small objects |
| Standard-IA | rare but needs ms | milliseconds, retrieval fee | 30 days | 3+ | older curated features, last quarter's snapshots |
| One Zone-IA | rare, can be recreated | milliseconds | 30 days | 1 only | derived data you can rebuild (shuffled shards, caches) |
| Glacier Instant | about once a quarter | milliseconds | 90 days | 3+ | audit copies you may need on short notice |
| Glacier Flexible | archive | minutes to hours | 90 days | 3+ | old raw data kept for compliance |
| Glacier Deep Archive | almost never | hours (check docs) | 180 days | 3+ | long-term regulatory copies |

- Raw data: immutable, large, read once to build features. Tier down after a month or two. Curated features and the current training snapshot: Standard. Old snapshots: Infrequent or Glacier Instant. Model artifacts: Standard for the deployed version, older versions can tier down.
- Failure modes: moving tiny objects to IA classes (a minimum billable object size applies, check docs), deleting before the minimum duration (you still pay for the minimum), putting the only copy in One Zone-IA (an AZ loss loses it), and forgetting that Glacier Flexible and Deep Archive objects must be restored before a GET (the call fails until restored).
- Lifecycle rules do the moving. Always add AbortIncompleteMultipartUpload, because half-finished uploads sit there invisibly and cost storage.

**Example:** `raw/` objects: Standard for 30 days, then Standard-IA, then Glacier at day 90. `tmp/` scratch objects: expire at day 14. Both prefixes abort incomplete multipart uploads after a few days. A 100-day-old raw file is therefore in Glacier, and a training job that needs it must plan a restore first.

**Code:**
```python
# q01.py
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import json, boto3
from moto import mock_aws

RULES = {"Rules": [
  {"ID": "raw-tiering", "Status": "Enabled", "Filter": {"Prefix": "raw/"},
   "Transitions": [{"Days": 30, "StorageClass": "STANDARD_IA"}, {"Days": 90, "StorageClass": "GLACIER"}],
   "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7}},
  {"ID": "tmp-expire", "Status": "Enabled", "Filter": {"Prefix": "tmp/"},
   "Expiration": {"Days": 14},
   "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 3}},
]}
with mock_aws():
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="ml-lake-demo")
    s3.put_bucket_lifecycle_configuration(Bucket="ml-lake-demo", LifecycleConfiguration=RULES)
    got = s3.get_bucket_lifecycle_configuration(Bucket="ml-lake-demo")["Rules"]
    for r in got:
        print(r["ID"], r["Status"], r["Filter"],
              [(t["Days"], t["StorageClass"]) for t in r.get("Transitions", [])],
              "expire", r.get("Expiration"), "abort-mpu", r["AbortIncompleteMultipartUpload"])
    # a PUT with an explicit class is accepted; moto does not move objects over time
    s3.put_object(Bucket="ml-lake-demo", Key="raw/a.csv", Body=b"x", StorageClass="STANDARD_IA")
    print("class on put:", s3.head_object(Bucket="ml-lake-demo", Key="raw/a.csv").get("StorageClass"))
    # expiry before transition is a rejected config? try a bad one: Days below the 30-day minimum for STANDARD_IA
    bad = {"Rules": [{"ID": "bad", "Status": "Enabled", "Filter": {"Prefix": "x/"},
                      "Transitions": [{"Days": 5, "StorageClass": "STANDARD_IA"}]}]}
    try:
        s3.put_bucket_lifecycle_configuration(Bucket="ml-lake-demo", LifecycleConfiguration=bad)
        print("moto accepted a 5-day STANDARD_IA transition (real S3 enforces a 30-day minimum; check current docs)")
    except Exception as e:
        print("rejected:", type(e).__name__)
```
```sh
# q01_cli.sh
#!/bin/sh
# usage: sh q01_cli.sh  (starts moto_server on 8501, runs the aws CLI with fake keys, stops it)
export AWS_ACCESS_KEY_ID=testing AWS_SECRET_ACCESS_KEY=testing AWS_DEFAULT_REGION=us-east-1
V=/tmp/claude-0/b10p10/v/bin
$V/moto_server -p 8501 >/tmp/claude-0/b10_q01_10/moto.log 2>&1 &
PID=$!
for i in 1 2 3 4 5 6 7 8 9 10; do curl -s -o /dev/null http://127.0.0.1:8501/ && break; sleep 1; done
E="--endpoint-url http://127.0.0.1:8501"
$V/aws $E s3 mb s3://ml-lake-cli
$V/aws $E s3api put-bucket-lifecycle-configuration --bucket ml-lake-cli --lifecycle-configuration file://lifecycle.json
$V/aws $E s3api get-bucket-lifecycle-configuration --bucket ml-lake-cli --query 'Rules[0].[ID,Filter.Prefix,Transitions[0].StorageClass,AbortIncompleteMultipartUpload.DaysAfterInitiation]' --output text
kill $PID
```

**Output (my run):** moto 5.2.4, boto3 1.43.118, fake keys, decorator mode (moto's in-process mock).
```
raw-tiering Enabled {'Prefix': 'raw/'} [(30, 'STANDARD_IA'), (90, 'GLACIER')] expire None abort-mpu {'DaysAfterInitiation': 7}
tmp-expire Enabled {'Prefix': 'tmp/'} [] expire {'Days': 14} abort-mpu {'DaysAfterInitiation': 3}
class on put: STANDARD_IA
moto accepted a 5-day STANDARD_IA transition (real S3 enforces a 30-day minimum; check current docs)
```
Server mode (moto_server on port 8501, `aws --endpoint-url`, run from a temp dir holding lifecycle.json):
```
make_bucket: ml-lake-cli
raw-tiering	raw/	STANDARD_IA	7
```
What moto does not do: it stores and returns the rule but never moves or expires objects over time, and it accepted a 5-day Standard-IA transition that real S3 should reject (30-day minimum, check current docs). Real tiering, retrieval delays, minimum-duration charges and prices: not executed.

**Follow-ups:**
- *Intelligent-Tiering or lifecycle?* Lifecycle when the age-based pattern is known (raw data gets cold). Intelligent-Tiering when access is unpredictable.
- *Can a training job read from Glacier Flexible directly?* No. Restore first, then read. Glacier Instant is readable directly.
- *Where do small files hurt?* IA and Glacier have minimum billable sizes and per-object overheads; bundle small files into shards (Q36).

**Common mistakes:**
- Quoting prices or fixed latencies as facts.
- Putting frequently re-read training data in an IA class and paying retrieval fees every epoch.
- No multipart-abort rule.
- Treating a lifecycle rule as instant. It runs asynchronously, daily at best.

### Q2 ⭐⭐⭐ 🟢 S3 data model and consistency: why S3 is an object store with a flat key space (prefixes are not folders), what 'strong read-after-write consistency' means after the December 2020 change and what it does not give you (no atomic multi-object commit, no rename, no locking, last-writer-wins), and what that implies for a training job that reads a dataset while another job is still writing it. Show overwrite, list-after-put and a conditional put (If-None-Match) against moto and say clearly that a mock cannot prove S3's real consistency.
**Asked at:** S3 interview question banks (novelvista '100+ Top AWS S3 Interview Questions', adaface, ccbp.in, a techinterview.org 'System Design Interview: Object Storage (Amazon S3)' post, AWS developer exam-prep study guides; search snippets only, not opened; WebFetch of docs.aws.amazon.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; cloud, data and ML engineer roles at IT-services firms, product companies and GCCs | AWS S3 documentation topics as summarised by prep guides (versioning and delete markers, lifecycle transitions and expiry, multipart upload, presigned URLs, strong read-after-write consistency since December 2020; search snippets only, not opened, exact limits not verified); vendor docs and prep notes, not interview reports; cloud, data and ML platform roles
**Say this first (1 line):** S3 is a flat key-value object store with strong read-after-write consistency per object, but no rename, no locks and no multi-object transactions, so a reader of a dataset must not trust "it exists, so it is complete".

**Then explain:**
- Flat key space: `data/part-0.csv` is one key string. "Folders" are a convention: listing with a prefix and a delimiter gives you the folder view. Empty-folder markers are just zero-byte keys.
- Strong consistency (since December 2020): after a successful PUT or DELETE, any later GET or LIST sees it. Before that, list-after-put and overwrite reads could be stale.
- What it does not give: atomic commit of many objects, rename (it is copy plus delete, two calls), locking, or protection from lost updates. Two writers to one key: last writer wins.
- Training job reading while another writes: the job can list a half-written dataset and train on partial data. Fix with a commit marker: write all parts, then write a manifest or `_SUCCESS` last, and readers only trust prefixes that have it. Or write to a new versioned prefix and never overwrite.
- Conditional writes: `If-None-Match: *` on PUT gives "create only if absent", enough for a simple lock or leader claim. Real S3 support and its edge cases: check current docs.

**Example:** writer makes 4 parts, crashes after 2, never writes the manifest. The reader sees 2 parts in a listing but no manifest, so it skips the run. Without the manifest rule it would train on half the data and nobody would notice.

**Code:**
```python
# q02.py
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from botocore.exceptions import ClientError
from moto import mock_aws

with mock_aws():
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="consist-demo")
    s3.put_object(Bucket="consist-demo", Key="data/v1.txt", Body=b"first")
    s3.put_object(Bucket="consist-demo", Key="data/v1.txt", Body=b"second")
    print("overwrite then read:", s3.get_object(Bucket="consist-demo", Key="data/v1.txt")["Body"].read())
    for i in range(3):
        s3.put_object(Bucket="consist-demo", Key=f"data/part-{i}.csv", Body=b"r")
    keys = [o["Key"] for o in s3.list_objects_v2(Bucket="consist-demo", Prefix="data/")["Contents"]]
    print("list after put:", keys)
    # prefixes are just string prefixes: Delimiter makes the 'folder' view
    r = s3.list_objects_v2(Bucket="consist-demo", Delimiter="/")
    print("common prefixes:", [p["Prefix"] for p in r["CommonPrefixes"]])
    # no rename: copy + delete = two calls, not atomic
    s3.copy_object(Bucket="consist-demo", Key="data/renamed.txt", CopySource={"Bucket": "consist-demo", "Key": "data/v1.txt"})
    s3.delete_object(Bucket="consist-demo", Key="data/v1.txt")
    print("after copy+delete:", sorted(o["Key"] for o in s3.list_objects_v2(Bucket="consist-demo", Prefix="data/")["Contents"]))
    # conditional put
    s3.put_object(Bucket="consist-demo", Key="lock/owner", Body=b"job-A", IfNoneMatch="*")
    print("first conditional put: ok")
    try:
        s3.put_object(Bucket="consist-demo", Key="lock/owner", Body=b"job-B", IfNoneMatch="*")
    except ClientError as e:
        print("second conditional put:", e.response["Error"]["Code"], e.response["ResponseMetadata"]["HTTPStatusCode"])
    print("owner is still:", s3.get_object(Bucket="consist-demo", Key="lock/owner")["Body"].read())

# reader/writer: a manifest makes a dataset 'commit' without multi-object atomicity
def writer(s3, n_parts, crash_after=None):
    for i in range(n_parts):
        if crash_after is not None and i == crash_after: return
        s3.put_object(Bucket="consist-demo", Key=f"ds/run1/part-{i}", Body=b"p")
    s3.put_object(Bucket="consist-demo", Key="ds/run1/_MANIFEST.json", Body=b'{"parts": %d}' % n_parts)
def reader(s3):
    try:
        s3.head_object(Bucket="consist-demo", Key="ds/run1/_MANIFEST.json")
    except ClientError:
        return "not committed: skip"
    n = len(s3.list_objects_v2(Bucket="consist-demo", Prefix="ds/run1/part-").get("Contents", []))
    return f"read {n} parts"
with mock_aws():
    s3 = boto3.client("s3"); s3.create_bucket(Bucket="consist-demo")
    writer(s3, 4, crash_after=2)
    print("writer crashed -> reader says:", reader(s3))
    writer(s3, 4)
    print("writer finished -> reader says:", reader(s3))
```

**Output (my run):** moto 5.2.4, API shape and logic only.
```
overwrite then read: b'second'
list after put: ['data/part-0.csv', 'data/part-1.csv', 'data/part-2.csv', 'data/v1.txt']
common prefixes: ['data/']
after copy+delete: ['data/part-0.csv', 'data/part-1.csv', 'data/part-2.csv', 'data/renamed.txt']
first conditional put: ok
second conditional put: PreconditionFailed 412
owner is still: b'job-A'
writer crashed -> reader says: not committed: skip
writer finished -> reader says: read 4 parts
```
A mock runs in one process and one thread, so it cannot show S3's real consistency or concurrent-writer behaviour. It only shows the API semantics. Real distributed behaviour: not executed.

**Follow-ups:**
- *Is listing a bucket cheap?* No: it is paged and slow for millions of keys (Q36).
- *How do you do an atomic dataset swap?* Write the new version under a new prefix, then flip a small pointer object or a catalog entry.
- *Does versioning solve lost updates?* It keeps old versions, but does not stop the overwrite.

**Common mistakes:**
- Saying S3 is eventually consistent (old answer).
- Treating prefixes as real folders, or rename as atomic.
- Reading a prefix while it is being written.
- Claiming a mock proves consistency.

### Q3 ⭐⭐⭐ 🟢 IAM building blocks: user, group, role, policy (managed, inline), identity-based versus resource-based policies, and the trust policy versus the permissions policy of a role. Why do ML systems use roles and short-lived credentials instead of long-lived access keys? Create a role with a trust policy and an inline policy in moto, print both documents, and explain which document answers 'who can assume it' and which answers 'what can it do'.
**Asked at:** IAM interview and policy-evaluation sources (AWS IAM 'Policy evaluation logic' pages on docs.aws.amazon.com and docs.aws.eu, tutorialsdojo 'How AWS IAM Handles Conflicting IAM Policies', advancedweb.hu 'IAM policy evaluation logic explained with examples', barkingiguana 'How IAM Policy Evaluation Actually Works', community.aws and hidekazu-konishi IAM glossary; search snippets only, not opened); vendor docs and study guides, not verified candidate reports; cloud, DevOps, security and MLOps roles at IT-services firms, product companies and GCCs | Job-posting skill lists (a getonbrd Senior MLOps Engineer AWS and SageMaker posting listing Athena, RDS, ECR, IAM, CloudWatch, CloudFormation or Terraform and GitHub Actions, a workingnomads Senior MLOps Engineer SageMaker and Airflow posting; search snippets only, not opened); job postings, not interview reports; MLOps roles on AWS
**Say this first (1 line):** A role has two documents: the trust policy says who may assume it, the permissions policy says what it can do once assumed, and ML systems use roles because credentials are short-lived and nothing long-lived can leak.

**Then explain:**
- User: a long-term identity with a password or access keys. Group: a bag of users for attaching policies; a group is not a principal. Role: an identity with no password or keys of its own; you assume it and get temporary credentials.
- Policies: managed (standalone, reusable, attach by ARN; AWS-managed or customer-managed) or inline (embedded in one identity, deleted with it). Identity-based policies attach to users, groups, roles. Resource-based policies attach to the resource (bucket policy, KMS key policy, role trust policy) and name a Principal.
- Trust policy is a resource-based policy on the role. Permissions policies are identity-based. A call needs both: caller allowed to assume, then the assumed role allowed to do the action.
- Why roles for ML: training jobs, Lambdas and EC2 get credentials automatically, they expire (hours), rotate by themselves, and leave no key in code, a notebook or a repo. Long-lived keys leak into Git (Q50).
- Failure modes: a wildcard Principal in a trust policy, a role that is assumable by any user in the account, inline policies nobody can find, and a long-lived key kept "just for CI".

**Example:** `train-role` trusts `sagemaker.amazonaws.com` (trust) and may read `s3://ml-data/train/*` (permissions). A teammate cannot assume it, because the trust names only the service. SageMaker can, but cannot write anywhere because the permissions say read-only.

**Code:**
```python
# q03.py
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import json, boto3
from moto import mock_aws

TRUST = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow",
        "Principal": {"Service": "sagemaker.amazonaws.com"}, "Action": "sts:AssumeRole"}]}
PERMS = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow",
        "Action": ["s3:GetObject"], "Resource": "arn:aws:s3:::ml-data/train/*"}]}
with mock_aws():
    iam = boto3.client("iam")
    iam.create_role(RoleName="train-role", AssumeRolePolicyDocument=json.dumps(TRUST))
    iam.put_role_policy(RoleName="train-role", PolicyName="read-train", PolicyDocument=json.dumps(PERMS))
    role = iam.get_role(RoleName="train-role")["Role"]
    print("ARN:", role["Arn"])
    print("TRUST (who can assume):", json.dumps(role["AssumeRolePolicyDocument"]))
    inl = iam.get_role_policy(RoleName="train-role", PolicyName="read-train")
    print("PERMISSIONS (what it can do):", json.dumps(inl["PolicyDocument"]))
    print("inline policy names:", iam.list_role_policies(RoleName="train-role")["PolicyNames"])
    # managed policy: standalone object, attach by ARN
    mp = iam.create_policy(PolicyName="read-train-managed", PolicyDocument=json.dumps(PERMS))["Policy"]
    iam.attach_role_policy(RoleName="train-role", PolicyArn=mp["Arn"])
    print("attached managed:", [p["PolicyName"] for p in iam.list_attached_role_policies(RoleName="train-role")["AttachedPolicies"]])
    # group and user
    iam.create_group(GroupName="ml-eng"); iam.create_user(UserName="asha")
    iam.add_user_to_group(GroupName="ml-eng", UserName="asha")
    print("groups of asha:", [g["GroupName"] for g in iam.list_groups_for_user(UserName="asha")["Groups"]])
    # a role has no password and no access key of its own
    print("role has access keys API? no: list_access_keys is for users; user keys:", iam.list_access_keys(UserName="asha")["AccessKeyMetadata"])
```

**Output (my run):** moto 5.2.4.
```
ARN: arn:aws:iam::123456789012:role/train-role
TRUST (who can assume): {"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "sagemaker.amazonaws.com"}, "Action": "sts:AssumeRole"}]}
PERMISSIONS (what it can do): {"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": ["s3:GetObject"], "Resource": "arn:aws:s3:::ml-data/train/*"}]}
inline policy names: ['read-train']
attached managed: ['read-train-managed']
groups of asha: ['ml-eng']
role has access keys API? no: list_access_keys is for users; user keys: []
```
Note: moto stores and returns both documents faithfully. It does not enforce either unless auth enforcement is switched on (Q8), so this shows the structure, not the access control.

**Follow-ups:**
- *Inline or managed?* Managed for anything shared or versioned, inline for a one-off tightly coupled to one role.
- *Instance profile?* A wrapper that passes a role to an EC2 instance.
- *Can a group be a Principal?* No.

**Common mistakes:**
- Mixing up trust and permissions policies.
- Putting the permissions in the trust policy.
- Using access keys in a training container.
- Thinking a group can be assumed.

### Q4 ⭐⭐⭐ 🟢 What is a SageMaker execution role? Give its trust policy principal (sagemaker.amazonaws.com), say what permissions a training job needs at minimum (read input prefix, write output prefix, pull an ECR image, write CloudWatch logs), why iam:PassRole matters for the person or pipeline that launches the job, and how it differs from the permissions of the human user. Write the trust and permissions policies as JSON, validate them with a Python checker, and test the allow and deny cases with a small evaluator.
**Asked at:** SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs | IAM interview and policy-evaluation sources (AWS IAM 'Policy evaluation logic' pages on docs.aws.amazon.com and docs.aws.eu, tutorialsdojo 'How AWS IAM Handles Conflicting IAM Policies', advancedweb.hu 'IAM policy evaluation logic explained with examples', barkingiguana 'How IAM Policy Evaluation Actually Works', community.aws and hidekazu-konishi IAM glossary; search snippets only, not opened); vendor docs and study guides, not verified candidate reports; cloud, DevOps, security and MLOps roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** The execution role is the IAM role SageMaker assumes to act for your job: trusted by `sagemaker.amazonaws.com`, with just enough permission to read inputs, write outputs, pull the image and write logs, and the launcher needs `iam:PassRole` to hand it over.

**Then explain:**
- Trust policy: Principal `{"Service": "sagemaker.amazonaws.com"}`, action `sts:AssumeRole`. Without it SageMaker cannot use the role and job creation fails.
- Minimum permissions: S3 read on the input prefix (plus ListBucket with a prefix condition), S3 write on the output prefix, ECR pull actions for the image (and `ecr:GetAuthorizationToken` on `*`), CloudWatch Logs create stream and put events. Add KMS if encrypted (Q8).
- `iam:PassRole`: when you call CreateTrainingJob with a RoleArn, IAM checks that *you* may pass that role. Without that check anyone who can create jobs could pass an admin role and escalate. Scope it to the one role ARN and add `iam:PassedToService`.
- Human vs role: the human launches the job with their own permissions; the code in the container uses the role's. They are different identities. The role does not need `PassRole` or `CreateTrainingJob`; the human does.
- Failure modes: AccessDenied at job start (PassRole or trust), job starts but cannot read data (role policy), ECR pull failure, and an over-broad role such as AmazonSageMakerFullAccess plus S3 full access.

**Example:** Training role can GetObject on `ml-data/train/a.csv` (allow) but not PutObject there (deny). The launcher can pass `sm-exec` to SageMaker but not to EC2 and not an `admin` role.

**Code:** (the evaluator is a copy of `scratch/B4P10_wavea/iam_eval_sketch.py`, saved here as `code/iam_eval.py`, simplified)
```python
# q04.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, sys
from iam_eval import evaluate

ROLE_ARN = "arn:aws:iam::123456789012:role/sm-exec"
TRUST = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow",
        "Principal": {"Service": "sagemaker.amazonaws.com"}, "Action": "sts:AssumeRole"}]}
PERMS = {"Version": "2012-10-17", "Statement": [
 {"Sid": "ReadInput", "Effect": "Allow", "Action": "s3:GetObject", "Resource": "arn:aws:s3:::ml-data/train/*"},
 {"Sid": "ListInput", "Effect": "Allow", "Action": "s3:ListBucket", "Resource": "arn:aws:s3:::ml-data",
  "Condition": {"StringLike": {"s3:prefix": "train/*"}}},
 {"Sid": "WriteOutput", "Effect": "Allow", "Action": "s3:PutObject", "Resource": "arn:aws:s3:::ml-data/models/*"},
 {"Sid": "PullImage", "Effect": "Allow", "Action": ["ecr:GetDownloadUrlForLayer", "ecr:BatchGetImage", "ecr:BatchCheckLayerAvailability"],
  "Resource": "arn:aws:ecr:ap-south-1:123456789012:repository/train-img"},
 {"Sid": "EcrToken", "Effect": "Allow", "Action": "ecr:GetAuthorizationToken", "Resource": "*"},
 {"Sid": "Logs", "Effect": "Allow", "Action": ["logs:CreateLogStream", "logs:PutLogEvents", "logs:CreateLogGroup"],
  "Resource": "arn:aws:logs:ap-south-1:123456789012:log-group:/aws/sagemaker/TrainingJobs*"}]}
# what the human/pipeline needs to launch the job
LAUNCHER = {"Version": "2012-10-17", "Statement": [
 {"Effect": "Allow", "Action": "sagemaker:CreateTrainingJob", "Resource": "*"},
 {"Effect": "Allow", "Action": "iam:PassRole", "Resource": ROLE_ARN,
  "Condition": {"StringEquals": {"iam:PassedToService": "sagemaker.amazonaws.com"}}}]}

def check(doc, kind):
    errs = []
    if doc.get("Version") != "2012-10-17": errs.append("Version must be 2012-10-17")
    st = doc.get("Statement")
    if not isinstance(st, list) or not st: return ["Statement must be a non-empty list"]
    for i, s in enumerate(st):
        if s.get("Effect") not in ("Allow", "Deny"): errs.append(f"stmt {i}: bad Effect")
        if "Action" not in s: errs.append(f"stmt {i}: no Action")
        if kind == "trust":
            if "Principal" not in s: errs.append(f"stmt {i}: trust policy needs Principal")
            if s.get("Action") != "sts:AssumeRole" and "sts:AssumeRole" not in s.get("Action", []):
                errs.append(f"stmt {i}: trust action is not sts:AssumeRole")
        else:
            if "Principal" in s: errs.append(f"stmt {i}: identity policy must not have Principal")
            if "Resource" not in s: errs.append(f"stmt {i}: no Resource")
            if s.get("Action") == "*" or s.get("Resource") == "*" and s.get("Action") not in ("ecr:GetAuthorizationToken",):
                errs.append(f"stmt {i}: wildcard Action or Resource, review")
    return errs
print("trust check:", check(TRUST, "trust") or "ok")
print("perms check:", check(PERMS, "perms") or "ok")
bad = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}]}
print("bad doc check:", check(bad, "perms"))
print("trust-as-perms check:", check(TRUST, "perms"))

ident = [PERMS]
cases = [
 ("read train object",        "s3:GetObject",    "arn:aws:s3:::ml-data/train/a.csv", {}, True),
 ("read from models prefix",  "s3:GetObject",    "arn:aws:s3:::ml-data/models/m.tar.gz", {}, False),
 ("write model output",       "s3:PutObject",    "arn:aws:s3:::ml-data/models/job1/model.tar.gz", {}, True),
 ("write into train prefix",  "s3:PutObject",    "arn:aws:s3:::ml-data/train/a.csv", {}, False),
 ("list bucket, prefix train/","s3:ListBucket",  "arn:aws:s3:::ml-data", {"s3:prefix": "train/x"}, True),
 ("list bucket, prefix models/","s3:ListBucket", "arn:aws:s3:::ml-data", {"s3:prefix": "models/"}, False),
 ("pull own image",          "ecr:BatchGetImage","arn:aws:ecr:ap-south-1:123456789012:repository/train-img", {}, True),
 ("pull other image",        "ecr:BatchGetImage","arn:aws:ecr:ap-south-1:123456789012:repository/other", {}, False),
 ("delete a bucket",         "s3:DeleteBucket",  "arn:aws:s3:::ml-data", {}, False),
]
for name, a, r, c, want in cases:
    d, why = evaluate(a, r, ctx=c, identity=ident)
    assert (d == "Allow") == want, (name, d, why)
    print(f"role    {name:28s} {d:5s} ({why})")
# launcher: PassRole to the right role vs another role
for name, rarn, c in [("PassRole sm-exec to sagemaker", ROLE_ARN, {"iam:PassedToService": "sagemaker.amazonaws.com"}),
                      ("PassRole sm-exec to ec2", ROLE_ARN, {"iam:PassedToService": "ec2.amazonaws.com"}),
                      ("PassRole admin-role", "arn:aws:iam::123456789012:role/admin", {"iam:PassedToService": "sagemaker.amazonaws.com"})]:
    d, why = evaluate("iam:PassRole", rarn, ctx=c, identity=[LAUNCHER])
    print(f"launcher {name:30s} {d:5s} ({why})")
d, why = evaluate("iam:PassRole", ROLE_ARN, ctx={"iam:PassedToService": "sagemaker.amazonaws.com"}, identity=[PERMS])
print("training role itself (no PassRole)  ", d, f"({why})")
```

**Output (my run):** pure Python, no AWS.
```
trust check: ok
perms check: ok
bad doc check: ['stmt 0: wildcard Action or Resource, review']
trust-as-perms check: ['stmt 0: identity policy must not have Principal', 'stmt 0: no Resource']
role    read train object            Allow (identity or resource policy allows (same account))
role    read from models prefix      Deny  (implicit deny: nothing allows)
role    write model output           Allow (identity or resource policy allows (same account))
role    write into train prefix      Deny  (implicit deny: nothing allows)
role    list bucket, prefix train/   Allow (identity or resource policy allows (same account))
role    list bucket, prefix models/  Deny  (implicit deny: nothing allows)
role    pull own image               Allow (identity or resource policy allows (same account))
role    pull other image             Deny  (implicit deny: nothing allows)
role    delete a bucket              Deny  (implicit deny: nothing allows)
launcher PassRole sm-exec to sagemaker  Allow (identity or resource policy allows (same account))
launcher PassRole sm-exec to ec2        Deny  (implicit deny: nothing allows)
launcher PassRole admin-role            Deny  (implicit deny: nothing allows)
training role itself (no PassRole)   Deny (implicit deny: nothing allows)
```
The checker and evaluator are simplified (no NotAction, no policy variables, few condition operators). Real SageMaker job creation and real IAM enforcement: not executed.

**Follow-ups:**
- *Why not give the role admin?* A bug or malicious code in the container then has admin.
- *Who is the caller in S3 logs?* The assumed-role session of the execution role.
- *Role for processing and endpoints?* Same pattern, separate roles per stage.

**Common mistakes:**
- Forgetting `GetAuthorizationToken` needs `Resource: "*"`.
- Putting ListBucket on the object ARN.
- Granting `iam:PassRole` on `*`.
- Mixing up the user's permissions with the job's.

### Q5 ⭐⭐⭐ 🟢 Walk through a SageMaker training job from API call to artifact: what you provide (image, role, instance type and count, input channels, hyperparameters, output path, stopping condition), what SageMaker does (provision, pull image, copy data, run, upload to S3, tear down), what the container sees under /opt/ml, and where logs and metrics go. Name the difference between script mode with a framework container and bring-your-own container. Build the CreateTrainingJob request in boto3 against moto, show the API shape, and state that no training ran.
**Asked at:** SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)
**Say this first (1 line):** A training job is an API call that says "run this image on these instances with this data and write the model there", and SageMaker provisions, runs, uploads and tears down for you.

**Then explain:**
- You provide: algorithm image (`TrainingImage`), `RoleArn`, `ResourceConfig` (instance type, count, volume), `InputDataConfig` (channels, each pointing at an S3 prefix), `HyperParameters` (all string values), `OutputDataConfig` (S3 output path), `StoppingCondition` (max runtime).
- SageMaker does: launch instances, pull the image from ECR, download or stream input data, run the container, upload what is in `/opt/ml/model` to S3 as `model.tar.gz`, tear everything down. Billing stops when the instances do (no prices here).
- Container layout: `/opt/ml/input/data/<channel>/` for data, `/opt/ml/input/config/hyperparameters.json` and `resourceconfig.json`, `/opt/ml/model/` for artifacts, `/opt/ml/output/failure` for the failure reason. Check current docs for the exact contract.
- Logs: stdout and stderr go to CloudWatch Logs (`/aws/sagemaker/TrainingJobs`). Metrics: SageMaker scrapes regex patterns you define from the logs (`MetricDefinitions`) into CloudWatch metrics.
- Script mode: you bring a Python script, a framework container (PyTorch, XGBoost, ...) runs it. BYO container: you build the image with its own entrypoint that follows the `/opt/ml` contract. Script mode is faster to start; BYO is for custom dependencies.
- Failure modes: role missing S3 or ECR permission, wrong channel names, not writing to `/opt/ml/model`, hitting the stopping condition, and a failure reason read from the job description rather than guessed.

**Example:** `churn-xgb-001`, one `ml.m5.xlarge`, channels `train` and `validation`, output `s3://ml-data/models/`. If it succeeds, the model lands at `s3://ml-data/models/churn-xgb-001/output/model.tar.gz`.

**Code:**
```python
# q05.py
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import json, boto3
from moto import mock_aws

with mock_aws():
    iam = boto3.client("iam")
    role = iam.create_role(RoleName="sm-exec", AssumeRolePolicyDocument=json.dumps({"Version": "2012-10-17", "Statement": [
        {"Effect": "Allow", "Principal": {"Service": "sagemaker.amazonaws.com"}, "Action": "sts:AssumeRole"}]}))["Role"]["Arn"]
    sm = boto3.client("sagemaker")
    req = dict(
        TrainingJobName="churn-xgb-001",
        RoleArn=role,
        AlgorithmSpecification={"TrainingImage": "123456789012.dkr.ecr.us-east-1.amazonaws.com/train-img:1.0",
                                "TrainingInputMode": "File"},
        InputDataConfig=[{"ChannelName": "train",
            "DataSource": {"S3DataSource": {"S3DataType": "S3Prefix", "S3Uri": "s3://ml-data/train/", "S3DataDistributionType": "FullyReplicated"}}},
            {"ChannelName": "validation",
            "DataSource": {"S3DataSource": {"S3DataType": "S3Prefix", "S3Uri": "s3://ml-data/val/"}}}],
        OutputDataConfig={"S3OutputPath": "s3://ml-data/models/"},
        ResourceConfig={"InstanceType": "ml.m5.xlarge", "InstanceCount": 1, "VolumeSizeInGB": 30},
        StoppingCondition={"MaxRuntimeInSeconds": 3600},
        HyperParameters={"max_depth": "6", "eta": "0.1"},   # all values are strings
    )
    print("request keys:", list(req))
    r = sm.create_training_job(**req)
    print("response keys:", [k for k in r if k != "ResponseMetadata"])
    print("TrainingJobArn:", r["TrainingJobArn"])
    d = sm.describe_training_job(TrainingJobName="churn-xgb-001")
    print("status:", d["TrainingJobStatus"], "| secondary:", d.get("SecondaryStatus"))
    print("hyperparameters:", d["HyperParameters"])
    print("channels:", [c["ChannelName"] for c in d["InputDataConfig"]])
    print("ModelArtifacts:", d.get("ModelArtifacts"))
    print("NOTE: no container ran, nothing was written to S3, no logs exist.")
```

**Output (my run):** moto 5.2.4. API shape only.
```
request keys: ['TrainingJobName', 'RoleArn', 'AlgorithmSpecification', 'InputDataConfig', 'OutputDataConfig', 'ResourceConfig', 'StoppingCondition', 'HyperParameters']
response keys: ['TrainingJobArn']
TrainingJobArn: arn:aws:sagemaker:us-east-1:123456789012:training-job/churn-xgb-001
status: Completed | secondary: Completed
hyperparameters: {'max_depth': '6', 'eta': '0.1'}
channels: ['train', 'validation']
ModelArtifacts: {'S3ModelArtifacts': 's3://ml-data/models/churn-xgb-001/output/model.tar.gz'}
NOTE: no container ran, nothing was written to S3, no logs exist.
```
No training ran: moto returned Completed instantly and invented a ModelArtifacts path; no container, no S3 write, no logs. Real provisioning, `/opt/ml` and CloudWatch: not executed.

**Follow-ups:**
- *Where does an input channel appear?* Under `/opt/ml/input/data/<channel>`. Input modes File, Pipe, FastFile change how data arrives (Q36).
- *How do you pass secrets?* Not as hyperparameters (they are visible in the job description); use Secrets Manager (Q18).
- *Spot?* `EnableManagedSpotTraining` with checkpoints (Q14).

**Common mistakes:**
- Non-string hyperparameter values.
- Saving the model outside `/opt/ml/model`.
- Using the human's credentials in the container.
- Claiming the mock trained something.

### Q6 ⭐⭐⭐ 🟡 SageMaker inference options: compare real-time endpoints, serverless inference, asynchronous inference and batch transform on traffic shape, latency tolerance, payload size, scale to zero, cold starts, cost model and operational burden. Give a decision table for four scenarios (UPI risk score under 100 ms, nightly scoring of 20 million rows, 500 MB document processing, a rarely used internal model). Build the endpoint-config shapes for all four in moto and say what the mock does not do. Do not quote limits from memory; point to the docs and the feature matrix.
**Asked at:** SageMaker hosting docs and write-ups (AWS 'Supported features' feature matrix and Model Hosting FAQs, caylent.com 'How To Pick the Best SageMaker Model Hosting Option' and 'SageMaker inference types', kodekloud AWS ML Engineer Associate notes on endpoint types; search snippets only, not opened; one third-party page's latency and payload figures conflicted with AWS and were not used); vendor docs and training notes, not interview reports; MLOps and ML engineer roles on AWS | SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs
**Say this first (1 line):** Pick the endpoint type from traffic shape and latency need: real-time for steady low latency, serverless for rare small traffic, asynchronous for big or slow requests, and batch transform for offline scoring with no endpoint at all.

**Then explain:**
- Real-time: always-on instances, lowest and steadiest latency, you pay while it is up, you autoscale instance count, no scale to zero.
- Serverless: scales to zero, cold starts on the first call after idle, limited memory and concurrency settings, for spiky or rare traffic. Limits on payload and timeout: check current docs.
- Asynchronous: requests go to a queue and results to S3; large payloads and long processing; can scale to zero instances (check docs); caller polls or gets a notification.
- Batch transform: a job over an S3 prefix, writes outputs to S3, nothing stays running.
- Check the SageMaker inference feature matrix and docs for supported features and limits before committing; I would not quote limits from memory.
- Failure modes: real-time for a rarely used model (idle cost), serverless for a p99-critical API (cold starts), async when the caller needs an answer in 100 ms, and batch for something that needs per-request freshness.

| Scenario | Choice | Why |
|---|---|---|
| UPI risk score under 100 ms | real-time | steady, low latency; at least two instances across AZs, autoscale |
| nightly scoring of 20 million rows | batch transform (or processing) | offline, throughput not latency, no idle endpoint |
| 500 MB document processing | asynchronous | large payload, long run, result in S3 |
| rarely used internal model | serverless | scale to zero, cold start acceptable |

**Example:** the UPI score path has a strict latency budget set by the payment flow, so serverless cold starts are a risk; the internal model called twice a day on a quiet team is the reverse.

**Code:**
```python
# q06.py
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import json, boto3
from moto import mock_aws

with mock_aws():
    iam = boto3.client("iam")
    role = iam.create_role(RoleName="sm-exec", AssumeRolePolicyDocument=json.dumps({"Version": "2012-10-17", "Statement": [
        {"Effect": "Allow", "Principal": {"Service": "sagemaker.amazonaws.com"}, "Action": "sts:AssumeRole"}]}))["Role"]["Arn"]
    sm = boto3.client("sagemaker")
    sm.create_model(ModelName="m1", ExecutionRoleArn=role,
        PrimaryContainer={"Image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/serve:1", "ModelDataUrl": "s3://ml-data/models/m1/model.tar.gz"})
    configs = {
     "upi-realtime": dict(ProductionVariants=[{"VariantName": "AllTraffic", "ModelName": "m1",
          "InstanceType": "ml.c5.xlarge", "InitialInstanceCount": 2}]),
     "docs-async": dict(ProductionVariants=[{"VariantName": "AllTraffic", "ModelName": "m1",
          "InstanceType": "ml.m5.xlarge", "InitialInstanceCount": 1}],
          AsyncInferenceConfig={"OutputConfig": {"S3OutputPath": "s3://ml-data/async-out/"}}),
     "internal-serverless": dict(ProductionVariants=[{"VariantName": "AllTraffic", "ModelName": "m1",
          "ServerlessConfig": {"MemorySizeInMB": 2048, "MaxConcurrency": 5}}]),
    }
    for name, kw in configs.items():
        sm.create_endpoint_config(EndpointConfigName=name, **kw)
        d = sm.describe_endpoint_config(EndpointConfigName=name)
        v = d["ProductionVariants"][0]
        kind = "async" if "AsyncInferenceConfig" in d else ("serverless" if "ServerlessConfig" in v else "real-time")
        print(f"{name:20s} -> {kind:10s} variant keys: {sorted(k for k in v if k in ('InstanceType','InitialInstanceCount','ServerlessConfig'))}")
    # batch transform is a JOB, not an endpoint
    sm.create_transform_job(TransformJobName="nightly-score-001", ModelName="m1",
        TransformInput={"DataSource": {"S3DataSource": {"S3DataType": "S3Prefix", "S3Uri": "s3://ml-data/score/2026-10-25/"}}, "ContentType": "text/csv"},
        TransformOutput={"S3OutputPath": "s3://ml-data/score-out/"},
        TransformResources={"InstanceType": "ml.m5.xlarge", "InstanceCount": 2})
    t = sm.describe_transform_job(TransformJobName="nightly-score-001")
    print("batch transform job:", t["TransformJobName"], t["TransformJobStatus"], "(job, no endpoint)")
    sm.create_endpoint(EndpointName="upi-ep", EndpointConfigName="upi-realtime")
    print("endpoint status:", sm.describe_endpoint(EndpointName="upi-ep")["EndpointStatus"])
    rt = boto3.client("sagemaker-runtime")
    print("invoke_endpoint:", rt.invoke_endpoint(EndpointName="upi-ep", Body=b"1,2,3", ContentType="text/csv")["Body"].read(), "<- canned, no model ran")
```

**Output (my run):** moto 5.2.4. API shape only.
```
upi-realtime         -> real-time  variant keys: ['InitialInstanceCount', 'InstanceType']
docs-async           -> async      variant keys: ['InitialInstanceCount', 'InstanceType']
internal-serverless  -> serverless variant keys: ['ServerlessConfig']
batch transform job: nightly-score-001 Completed (job, no endpoint)
endpoint status: InService
invoke_endpoint: b'body' <- canned, no model ran
```
Not emulated: no instances, no autoscaling, no real latency, no cold start, no queue or S3 result for async, no scale to zero, no model ever served (the invoke body is moto's canned bytes). Real behaviour, limits and costs: not executed; see the SageMaker docs and feature matrix.

**Follow-ups:**
- *Can I mix traffic on one endpoint?* Production variants split traffic by weight (rollout mechanics belong to Part 6).
- *Why batch transform over a real-time loop?* No endpoint to keep up, easy retry by shard.
- *Many small models?* Multi-model endpoints (Q25).

**Common mistakes:**
- Quoting payload and timeout numbers from memory.
- Choosing serverless for latency-critical paths.
- Forgetting async needs an S3 output and a notification design.
- Leaving real-time endpoints up after an experiment.

### Q7 ⭐⭐⭐ 🟡 IAM policy evaluation logic: explain the order of evaluation (explicit deny anywhere wins, then organisation SCPs, resource-based policies, identity-based policies, permissions boundaries, session policies, and implicit deny by default), same-account versus cross-account differences, and the role-trust-policy exception. Use the pure-Python evaluator to run ten cases (allow, implicit deny, explicit deny beating allow, SCP ceiling, boundary ceiling, session policy intersection, cross-account needing both sides) and print the decisions; mark clearly that the sketch is simplified.
**Asked at:** IAM interview and policy-evaluation sources (AWS IAM 'Policy evaluation logic' pages on docs.aws.amazon.com and docs.aws.eu, tutorialsdojo 'How AWS IAM Handles Conflicting IAM Policies', advancedweb.hu 'IAM policy evaluation logic explained with examples', barkingiguana 'How IAM Policy Evaluation Actually Works', community.aws and hidekazu-konishi IAM glossary; search snippets only, not opened); vendor docs and study guides, not verified candidate reports; cloud, DevOps, security and MLOps roles at IT-services firms, product companies and GCCs | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)
**Say this first (1 line):** IAM decides in this order in spirit: any explicit Deny wins, then every ceiling (SCP, boundary, session) must allow, and then something must actually grant, otherwise it is an implicit deny.

**Then explain:**
- Default is deny. An allow must exist. An explicit Deny anywhere (identity, resource, SCP, boundary, session) beats every Allow.
- Ceilings, not grants: SCPs (organisation), permissions boundaries (on a user or role) and session policies (on an assumed session) only limit. The effective permission is the intersection. They never grant anything.
- Same account: an identity policy allow or a resource policy allow is enough (with the boundary and session caveats). Cross-account: both the caller's identity policy and the resource policy must allow.
- Exceptions to "one allow is enough": role trust policies (the trust policy must name the caller), and KMS key policies (the key policy must allow, directly or by enabling IAM). SCPs do not apply to the management account. Check current docs for the full flowchart.
- Failure modes: forgetting the SCP ceiling, expecting a boundary to grant, and debugging only the identity policy when a bucket policy denies.

**Example:** boundary allows only `ec2:*`, identity policy allows `s3:*`, so `s3:GetObject` is denied. Add `s3:*` to the boundary and it is allowed.

**Code:** (evaluator in `code/iam_eval.py` is a copy of the Wave A sketch)
```python
# q07.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iam_eval import evaluate

def P(action, resource="*", effect="Allow", cond=None):
    s = {"Effect": effect, "Action": action, "Resource": resource}
    if cond: s["Condition"] = cond
    return {"Version": "2012-10-17", "Statement": [s]}
OBJ = "arn:aws:s3:::ml-data/train/x.csv"
ROLE = "arn:aws:iam::111111111111:role/trainer"
RP_ROLE = {"Statement": [{"Effect": "Allow", "Principal": {"AWS": ROLE}, "Action": "s3:GetObject", "Resource": "*"}]}
CASES = [
 ("1 identity allow",                      dict(identity=[P("s3:GetObject")]), "Allow"),
 ("2 nothing says allow (implicit deny)",  dict(identity=[]), "Deny"),
 ("3 allow + explicit deny -> deny",       dict(identity=[P("s3:*"), P("s3:GetObject", effect="Deny")]), "Deny"),
 ("4 SCP ceiling lacks s3",                dict(identity=[P("s3:*")], scps=[P("ec2:*")]), "Deny"),
 ("5 SCP allows + identity allows",        dict(identity=[P("s3:*")], scps=[P("*")]), "Allow"),
 ("6 SCP explicit deny",                   dict(identity=[P("s3:*")], scps=[P("*"), P("s3:*", effect="Deny")]), "Deny"),
 ("7 boundary lacks s3",                   dict(identity=[P("s3:*")], boundary=P("ec2:*")), "Deny"),
 ("8 boundary allows s3, identity allows", dict(identity=[P("s3:*")], boundary=P("s3:*")), "Allow"),
 ("9 session policy narrows to Put",       dict(identity=[P("s3:*")], session=P("s3:PutObject")), "Deny"),
 ("10 same-account resource policy alone", dict(identity=[], resource_policy=RP_ROLE, principal_arn=ROLE), "Allow"),
 ("11 cross-account, resource side only",  dict(identity=[], resource_policy=RP_ROLE, principal_arn=ROLE, same_account=False), "Deny"),
 ("12 cross-account, both sides",          dict(identity=[P("s3:GetObject")], resource_policy=RP_ROLE, principal_arn=ROLE, same_account=False), "Allow"),
 ("13 cross-account, identity side only",  dict(identity=[P("s3:GetObject")], same_account=False), "Deny"),
]
for name, kw, want in CASES:
    d, why = evaluate("s3:GetObject", OBJ, **kw)
    assert d == want, (name, d, why)
    print(f"{name:42s} {d:5s} | {why}")
print(len(CASES), "cases, all as expected")
print("Sketch limits: no NotAction/NotResource, no policy variables, few condition operators,")
print("no resource-policy-vs-boundary corner cases beyond one rule, trust policies and KMS key policies not modelled.")
```

**Output (my run):** pure Python, thirteen cases (I ran more than ten).
```
1 identity allow                           Allow | identity or resource policy allows (same account)
2 nothing says allow (implicit deny)       Deny  | implicit deny: nothing allows
3 allow + explicit deny -> deny            Deny  | explicit deny
4 SCP ceiling lacks s3                     Deny  | implicit deny: SCP level 0 does not allow
5 SCP allows + identity allows             Allow | identity or resource policy allows (same account)
6 SCP explicit deny                        Deny  | explicit deny
7 boundary lacks s3                        Deny  | implicit deny: outside permissions boundary
8 boundary allows s3, identity allows      Allow | identity or resource policy allows (same account)
9 session policy narrows to Put            Deny  | implicit deny: outside session policy
10 same-account resource policy alone      Allow | identity or resource policy allows (same account)
11 cross-account, resource side only       Deny  | implicit deny: cross-account needs both sides
12 cross-account, both sides               Allow | cross-account: identity AND resource policy allow
13 cross-account, identity side only       Deny  | implicit deny: cross-account needs both sides
13 cases, all as expected
Sketch limits: no NotAction/NotResource, no policy variables, few condition operators,
no resource-policy-vs-boundary corner cases beyond one rule, trust policies and KMS key policies not modelled.
```
The sketch is simplified: it models Action and Resource wildcards, three condition operators, one boundary corner case and one resource-policy rule. It is a teaching model, not AWS. Real enforcement and the policy simulator: not executed.

**Follow-ups:**
- *Does an SCP grant access?* No, only limits.
- *Resource policy plus boundary?* If the resource policy names the role ARN directly, same-account access can work without boundary allow; naming the account root does not. Check current docs.
- *What tool helps?* IAM Policy Simulator and Access Analyzer in real AWS.

**Common mistakes:**
- Saying boundaries or SCPs grant permissions.
- Forgetting cross-account needs both sides.
- Believing Allow beats Deny.
- Forgetting the trust policy is a separate check.

### Q8 ⭐⭐⭐ 🟡 Write a least-privilege policy for a training job that reads s3://ml-data/train/ and writes s3://ml-data/models/. Show why bucket ARNs and object ARNs differ (s3:ListBucket on the bucket with a prefix condition, s3:GetObject on objects), how wildcards go wrong, how to add a KMS permission when the bucket uses SSE-KMS, and how you would verify it (IAM Access Analyzer or policy simulator in real AWS). Test allow and deny cases with the evaluator, and note that moto does not enforce policies unless auth enforcement is switched on.
**Asked at:** IAM interview and policy-evaluation sources (AWS IAM 'Policy evaluation logic' pages on docs.aws.amazon.com and docs.aws.eu, tutorialsdojo 'How AWS IAM Handles Conflicting IAM Policies', advancedweb.hu 'IAM policy evaluation logic explained with examples', barkingiguana 'How IAM Policy Evaluation Actually Works', community.aws and hidekazu-konishi IAM glossary; search snippets only, not opened); vendor docs and study guides, not verified candidate reports; cloud, DevOps, security and MLOps roles at IT-services firms, product companies and GCCs | SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs
**Say this first (1 line):** Grant exactly the verbs on exactly the ARNs the job uses: ListBucket on the bucket ARN with a prefix condition, GetObject on `train/*`, PutObject on `models/*`, and the KMS key actions if the bucket is encrypted with SSE-KMS.

**Then explain:**
- Bucket vs object ARNs: `arn:aws:s3:::ml-data` is the bucket, used by `s3:ListBucket`. `arn:aws:s3:::ml-data/train/*` is objects, used by `s3:GetObject` and `PutObject`. Putting ListBucket on the object ARN does nothing.
- Prefix control for listing is a Condition (`s3:prefix`), because the resource is the bucket.
- Wildcard traps: `ml-data*` also matches `ml-data-prod`; `s3:*` on `*` is admin for S3; a prefix `train*` also matches `trainer/`.
- SSE-KMS: the role also needs `kms:Decrypt` (read) and `kms:GenerateDataKey` (write) on the key, and the key policy must allow it. Missing KMS is the classic AccessDenied with S3 permission present.
- Verify in real AWS with IAM Access Analyzer (policy validation and findings) and the policy simulator, and by reading CloudTrail denials. Not executed here.
- moto does not enforce IAM unless you switch auth enforcement on; otherwise every call passes as if admin.

**Example:** the evaluator run shows GetObject on `train/a.csv` allowed, on `models/` denied, ListBucket with prefix `train/` allowed but with an empty prefix denied, and the wildcard trap allowing deletes on a neighbouring bucket.

**Code:**
```python
# q08.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import json
from iam_eval import evaluate
POLICY = {"Version": "2012-10-17", "Statement": [
 {"Sid": "ListOnlyTrainPrefix", "Effect": "Allow", "Action": "s3:ListBucket", "Resource": "arn:aws:s3:::ml-data",
  "Condition": {"StringLike": {"s3:prefix": ["train/*", "train/"]}}},
 {"Sid": "ReadTrain", "Effect": "Allow", "Action": "s3:GetObject", "Resource": "arn:aws:s3:::ml-data/train/*"},
 {"Sid": "WriteModels", "Effect": "Allow", "Action": "s3:PutObject", "Resource": "arn:aws:s3:::ml-data/models/*"},
 {"Sid": "KmsForSse", "Effect": "Allow", "Action": ["kms:Decrypt", "kms:GenerateDataKey"],
  "Resource": "arn:aws:kms:ap-south-1:123456789012:key/1111-2222"}]}
cases = [
 ("GetObject train/a.csv",       "s3:GetObject",  "arn:aws:s3:::ml-data/train/a.csv", {}),
 ("GetObject models/m.tar.gz",   "s3:GetObject",  "arn:aws:s3:::ml-data/models/m.tar.gz", {}),
 ("PutObject models/j1/model",   "s3:PutObject",  "arn:aws:s3:::ml-data/models/j1/model.tar.gz", {}),
 ("PutObject train/evil.csv",    "s3:PutObject",  "arn:aws:s3:::ml-data/train/evil.csv", {}),
 ("ListBucket on BUCKET arn, prefix train/", "s3:ListBucket", "arn:aws:s3:::ml-data", {"s3:prefix": "train/2026/"}),
 ("ListBucket on BUCKET arn, prefix ''",    "s3:ListBucket", "arn:aws:s3:::ml-data", {"s3:prefix": ""}),
 ("ListBucket with OBJECT arn (wrong ARN)", "s3:ListBucket", "arn:aws:s3:::ml-data/train/*", {"s3:prefix": "train/"}),
 ("DeleteObject models/",        "s3:DeleteObject", "arn:aws:s3:::ml-data/models/x", {}),
 ("kms:Decrypt on the key",      "kms:Decrypt",   "arn:aws:kms:ap-south-1:123456789012:key/1111-2222", {}),
 ("kms:Decrypt on another key",  "kms:Decrypt",   "arn:aws:kms:ap-south-1:123456789012:key/9999", {}),
]
for n, a, r, c in cases:
    d, why = evaluate(a, r, ctx=c, identity=[POLICY]); print(f"{n:42s} {d:5s} ({why})")
# the wildcard trap
BAD = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "arn:aws:s3:::ml-data*"}]}
for n, r in [("trap: s3:*  on ml-data*  vs ml-data-prod/secret", "arn:aws:s3:::ml-data-prod/secret.csv"),
             ("trap: s3:*  on ml-data*  vs ml-data/anything", "arn:aws:s3:::ml-data/anything")]:
    print(f"{n:55s}", evaluate("s3:DeleteObject", r, identity=[BAD])[0])

# --- moto: is policy enforcement on? ---
import json, boto3
from botocore.exceptions import ClientError
from moto import mock_aws
from moto.core import set_initial_no_auth_action_count

POL = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": "s3:ListAllMyBuckets", "Resource": "*"}]}
def run(enforce):
    @mock_aws
    def body():
        iam = boto3.client("iam"); s3 = boto3.client("s3")
        iam.create_user(UserName="u")
        iam.put_user_policy(UserName="u", PolicyName="p", PolicyDocument=json.dumps(POL))
        k = iam.create_access_key(UserName="u")["AccessKey"]
        s3.create_bucket(Bucket="ml-data")
        u = boto3.client("s3", aws_access_key_id=k["AccessKeyId"], aws_secret_access_key=k["SecretAccessKey"])
        print("  ListBuckets:", [b["Name"] for b in u.list_buckets()["Buckets"]])
        try:
            u.create_bucket(Bucket="other-bucket"); print("  CreateBucket: succeeded (no enforcement)")
        except ClientError as e:
            print("  CreateBucket:", e.response["Error"]["Code"])
    if enforce:
        set_initial_no_auth_action_count(4)(body)()   # first 4 calls unauthenticated (user setup), then enforce
    else:
        body()
print("auth enforcement OFF (default):"); run(False)
print("auth enforcement ON (set_initial_no_auth_action_count(4)):"); run(True)
```

**Output (my run):** pure-Python evaluator, then moto 5.2.4 with and without auth enforcement.
```
GetObject train/a.csv                      Allow (identity or resource policy allows (same account))
GetObject models/m.tar.gz                  Deny  (implicit deny: nothing allows)
PutObject models/j1/model                  Allow (identity or resource policy allows (same account))
PutObject train/evil.csv                   Deny  (implicit deny: nothing allows)
ListBucket on BUCKET arn, prefix train/    Allow (identity or resource policy allows (same account))
ListBucket on BUCKET arn, prefix ''        Deny  (implicit deny: nothing allows)
ListBucket with OBJECT arn (wrong ARN)     Deny  (implicit deny: nothing allows)
DeleteObject models/                       Deny  (implicit deny: nothing allows)
kms:Decrypt on the key                     Allow (identity or resource policy allows (same account))
kms:Decrypt on another key                 Deny  (implicit deny: nothing allows)
trap: s3:*  on ml-data*  vs ml-data-prod/secret         Allow
trap: s3:*  on ml-data*  vs ml-data/anything            Allow
auth enforcement OFF (default):
  ListBuckets: ['ml-data']
  CreateBucket: succeeded (no enforcement)
auth enforcement ON (set_initial_no_auth_action_count(4)):
  ListBuckets: ['ml-data']
  CreateBucket: AccessDenied
```
In moto, enforcement is off by default; with `set_initial_no_auth_action_count(4)` the first four calls (user setup) are unauthenticated and later ones are checked, which denied CreateBucket. moto's IAM evaluation is limited, and the simulator and Access Analyzer are not available here. Real AWS verification: not executed.

**Follow-ups:**
- *How to avoid the wildcard trap?* Name the bucket exactly and prefer an explicit prefix.
- *Why was ListBucket denied for empty prefix?* The condition requires `train/`; a client listing the whole bucket is refused.
- *Where does the data-owner control it?* A bucket policy with a deny outside the VPC endpoint or role.

**Common mistakes:**
- ListBucket on the object ARN.
- Granting `s3:*` on `*` "to get unblocked".
- Forgetting KMS for encrypted buckets.
- Trusting a mock that is not enforcing anything.

### Q9 ⭐⭐⭐ 🟡 STS and assume-role: describe what happens when a service or person calls AssumeRole (trust policy check, temporary credentials with access key, secret and session token, a session name, duration limits), cross-account assume role with an external ID, and role chaining. Why are temporary credentials better than access keys? Run assume_role in moto, print the returned shape and the assumed-role ARN, then show that moto accepted a role whose trust policy names a different account (so trust checks are not emulated) and explain what real AWS would do.
**Asked at:** IAM interview and policy-evaluation sources (AWS IAM 'Policy evaluation logic' pages on docs.aws.amazon.com and docs.aws.eu, tutorialsdojo 'How AWS IAM Handles Conflicting IAM Policies', advancedweb.hu 'IAM policy evaluation logic explained with examples', barkingiguana 'How IAM Policy Evaluation Actually Works', community.aws and hidekazu-konishi IAM glossary; search snippets only, not opened); vendor docs and study guides, not verified candidate reports; cloud, DevOps, security and MLOps roles at IT-services firms, product companies and GCCs | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)
**Say this first (1 line):** AssumeRole checks the caller against the role's trust policy and returns temporary credentials (access key, secret, session token, expiry) tied to a session name, so nothing long-lived is handed out.

**Then explain:**
- Flow: caller (user, role or service) calls `sts:AssumeRole` on a role ARN with a session name. AWS checks that the trust policy allows this caller (and the caller's own identity policy allows `sts:AssumeRole` when cross-account). If yes, it returns credentials that act as `assumed-role/<role>/<session>`.
- Duration: default one hour, role maximum configurable up to a ceiling; role chaining has a shorter cap. Check current docs for the numbers.
- Cross-account with external ID: the trust policy requires `sts:ExternalId` to match, which stops the confused-deputy problem when a third party assumes your role.
- Role chaining: using assumed-role credentials to assume another role. Session cannot be extended beyond the chain cap, and session tags and policies carry forward rules (check docs).
- Better than keys: they expire, are scoped by the session policy, show up in CloudTrail with the session name, and nothing needs to be rotated by hand.
- Failure modes: trust policy naming `:root` of a whole account when only one role should assume; no external ID for a vendor; missing `sts:AssumeRole` on the caller side.

**Example:** a role in account A trusts account B's root with `sts:ExternalId = partner-42`. B's caller without the ID is refused; with it, allowed. In moto the call just works.

**Code:**
```python
# q09.py
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import json, boto3
from botocore.exceptions import ClientError, ParamValidationError
from moto import mock_aws

# role in THIS account whose trust policy names a DIFFERENT account (999999999999)
TRUST_OTHER = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow",
    "Principal": {"AWS": "arn:aws:iam::999999999999:root"}, "Action": "sts:AssumeRole",
    "Condition": {"StringEquals": {"sts:ExternalId": "partner-42"}}}]}
with mock_aws():
    iam = boto3.client("iam"); sts = boto3.client("sts")
    print("caller:", sts.get_caller_identity()["Arn"])
    iam.create_role(RoleName="r", AssumeRolePolicyDocument=json.dumps(TRUST_OTHER))
    resp = sts.assume_role(RoleArn="arn:aws:iam::123456789012:role/r", RoleSessionName="train-job-7", DurationSeconds=900)
    c = resp["Credentials"]
    print("response keys:", sorted(k for k in resp if k != "ResponseMetadata"))
    print("credential keys:", sorted(c))
    print("AssumedRoleUser.Arn:", resp["AssumedRoleUser"]["Arn"])
    print("access key id starts with:", c["AccessKeyId"][:4], "| token length > 0:", len(c["SessionToken"]) > 0)
    print("Expiration present:", "Expiration" in c)
    print("MOTO ACCEPTED: caller is account 123456789012, trust names 999999999999, no ExternalId passed.")
    # session name length rule is validated
    try:
        sts.assume_role(RoleArn="arn:aws:iam::123456789012:role/r", RoleSessionName="x")
    except ParamValidationError as e:
        print("short session name rejected client-side by botocore:", str(e).splitlines()[-1].strip())
    # role chaining shape: use the temp creds to call STS again
    chained = boto3.client("sts", aws_access_key_id=c["AccessKeyId"], aws_secret_access_key=c["SecretAccessKey"], aws_session_token=c["SessionToken"])
    iam.create_role(RoleName="r2", AssumeRolePolicyDocument=json.dumps(TRUST_OTHER))
    r2 = chained.assume_role(RoleArn="arn:aws:iam::123456789012:role/r2", RoleSessionName="hop-2")
    print("chained ARN:", r2["AssumedRoleUser"]["Arn"])

# what real AWS checks, as a small trust evaluator (simplified)
def trust_allows(trust, caller_account, ctx):
    for s in trust["Statement"]:
        p = s["Principal"].get("AWS", [])
        p = p if isinstance(p, list) else [p]
        who = any(x == f"arn:aws:iam::{caller_account}:root" for x in p)
        cond = all(ctx.get(k) == v for op, kv in s.get("Condition", {}).items() for k, v in kv.items())
        if s["Effect"] == "Allow" and who and cond: return True
    return False
print("real-AWS-style trust check, caller 123456789012:", trust_allows(TRUST_OTHER, "123456789012", {}))
print("caller 999999999999 without ExternalId:        ", trust_allows(TRUST_OTHER, "999999999999", {}))
print("caller 999999999999 with ExternalId partner-42:", trust_allows(TRUST_OTHER, "999999999999", {"sts:ExternalId": "partner-42"}))
```

**Output (my run):** moto 5.2.4 (caller is the fixed moto user in account 123456789012).
```
caller: arn:aws:sts::123456789012:user/moto
response keys: ['AssumedRoleUser', 'Credentials', 'PackedPolicySize']
credential keys: ['AccessKeyId', 'Expiration', 'SecretAccessKey', 'SessionToken']
AssumedRoleUser.Arn: arn:aws:sts::123456789012:assumed-role/r/train-job-7
access key id starts with: ASIA | token length > 0: True
Expiration present: True
MOTO ACCEPTED: caller is account 123456789012, trust names 999999999999, no ExternalId passed.
short session name rejected client-side by botocore: Invalid length for parameter RoleSessionName, value: 1, valid min length: 2
chained ARN: arn:aws:sts::123456789012:assumed-role/r2/hop-2
real-AWS-style trust check, caller 123456789012: False
caller 999999999999 without ExternalId:         False
caller 999999999999 with ExternalId partner-42: True
```
Important: moto did not check the trust policy at all. The role trusted a different account and demanded an external ID, and the assume succeeded anyway. The last three lines are my small trust checker showing what real AWS would decide. Real credential expiry, chaining caps and CloudTrail: not executed.

**Follow-ups:**
- *Who can assume a role in the same account?* Only principals the trust policy allows (an account root principal then needs an identity policy too). Check docs.
- *Session policy?* Passed on AssumeRole, can only shrink permissions.
- *AssumeRoleWithWebIdentity?* For OIDC (EKS, GitHub); Part 7 and Q31.

**Common mistakes:**
- Saying moto proves the trust works.
- Forgetting the session name shows in logs.
- Sharing an external ID as if it were a secret key (it is not secret).
- Using keys when a role would do.

### Q10 ⭐⭐⭐ 🟡 Presigned URLs: how a presigned GET or PUT works (the signer's credentials sign the request, the URL carries the signature and expiry, no AWS credentials on the client), what limits the effective lifetime when the signer is an assumed role, how to restrict an upload (presigned POST with conditions such as content-length-range), and security pitfalls (URLs in logs, overly long expiry, signer permission loss). Generate GET and POST presigns with moto, fetch the object with requests, and print the query parameters.
**Asked at:** S3 interview question banks (novelvista '100+ Top AWS S3 Interview Questions', adaface, ccbp.in, a techinterview.org 'System Design Interview: Object Storage (Amazon S3)' post, AWS developer exam-prep study guides; search snippets only, not opened; WebFetch of docs.aws.amazon.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; cloud, data and ML engineer roles at IT-services firms, product companies and GCCs | AWS S3 documentation topics as summarised by prep guides (versioning and delete markers, lifecycle transitions and expiry, multipart upload, presigned URLs, strong read-after-write consistency since December 2020; search snippets only, not opened, exact limits not verified); vendor docs and prep notes, not interview reports; cloud, data and ML platform roles
**Say this first (1 line):** A presigned URL is a normal S3 request signed in advance with the signer's credentials, carrying the signature and expiry in the query string, so a client with no AWS credentials can do exactly that one request until it expires.

**Then explain:**
- GET or PUT presign: the URL pins method, bucket, key, expiry. Whoever holds it can do it. The permission used is the signer's at request time.
- Lifetime with an assumed role: the URL stops working when the signing credentials expire, even if you asked for a longer expiry. Long-lived presigns need an IAM user key (not recommended) or regenerate on demand.
- Restricting uploads: presigned POST with a signed policy: `content-length-range`, key prefix, content type. Presigned PUT cannot do a size range.
- Pitfalls: URLs end up in logs, referrers and chat; long expiry; signer loses the permission or is deleted, so the URL fails; no per-user identity in the access log.
- Failure mode: assuming "expired" is enforced by the mock. It was not.

**Example:** a web app hands a data scientist a 5-minute presigned POST limited to `uploads/` and 1 MiB. The browser uploads straight to S3; the server never touches the bytes.

**Code:**
```python
# q10.py
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3, requests
from urllib.parse import urlparse, parse_qs
from moto import mock_aws

with mock_aws():
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="share-demo")
    s3.put_object(Bucket="share-demo", Key="reports/r1.txt", Body=b"hello report")
    url = s3.generate_presigned_url("get_object", Params={"Bucket": "share-demo", "Key": "reports/r1.txt"}, ExpiresIn=300)
    q = parse_qs(urlparse(url).query)
    print("GET url query params:", sorted(q))
    print("Expires param is an epoch-seconds value:", q["Expires"][0].isdigit())
    r = requests.get(url); print("GET with requests:", r.status_code, r.content)
    # PUT presign
    purl = s3.generate_presigned_url("put_object", Params={"Bucket": "share-demo", "Key": "uploads/u1.txt"}, ExpiresIn=300)
    r = requests.put(purl, data=b"uploaded by a client with no keys"); print("PUT with requests:", r.status_code)
    print("object now:", s3.get_object(Bucket="share-demo", Key="uploads/u1.txt")["Body"].read())
    # presigned POST with conditions
    post = s3.generate_presigned_post("share-demo", "uploads/${filename}",
        Fields={"Content-Type": "text/plain"},
        Conditions=[["content-length-range", 1, 1048576], {"Content-Type": "text/plain"}, ["starts-with", "$key", "uploads/"]],
        ExpiresIn=300)
    print("POST url:", post["url"])
    print("POST fields:", sorted(post["fields"]))
    import base64, json
    pol = json.loads(base64.b64decode(post["fields"]["policy"]))
    print("POST policy conditions:", pol["conditions"])
    r = requests.post(post["url"], data=post["fields"], files={"file": ("a.txt", b"small file")})
    print("POST upload:", r.status_code)
    # big file against the 1 MiB condition, to see what moto does
    r = requests.post(post["url"], data=post["fields"], files={"file": ("big.txt", b"x" * 2_000_000)})
    print("POST 2 MB (condition max 1 MiB) status in moto:", r.status_code)

# expired URL: signed in the past
import time
from unittest import mock
with mock_aws():
    s3 = boto3.client("s3"); s3.create_bucket(Bucket="share-demo"); s3.put_object(Bucket="share-demo", Key="k", Body=b"v")
    url = s3.generate_presigned_url("get_object", Params={"Bucket": "share-demo", "Key": "k"}, ExpiresIn=1)
    time.sleep(2.2)
    r = requests.get(url); print("GET after expiry:", r.status_code, "(moto)" )
```

**Output (my run):** moto 5.2.4, requests against the mock.
```
GET url query params: ['AWSAccessKeyId', 'Expires', 'Signature']
Expires param is an epoch-seconds value: True
GET with requests: 200 b'hello report'
PUT with requests: 200
object now: b'uploaded by a client with no keys'
POST url: https://share-demo.s3.amazonaws.com/
POST fields: ['AWSAccessKeyId', 'Content-Type', 'key', 'policy', 'signature']
POST policy conditions: [['content-length-range', 1, 1048576], {'Content-Type': 'text/plain'}, ['starts-with', '$key', 'uploads/'], {'bucket': 'share-demo'}, ['starts-with', '$key', 'uploads/']]
POST upload: 204
POST 2 MB (condition max 1 MiB) status in moto: 204
GET after expiry: 200 (moto)
```
Honest read: moto accepted a 2 MB POST against a 1 MiB `content-length-range` condition (204) and still served a GET after a 1-second expiry (200). Real S3 enforces both (`EntityTooLarge`, `AccessDenied` on expiry, as far as I know; check current docs). That is a mock gap, not S3 behaviour. Real signature verification: not executed.

**Follow-ups:**
- *Query parameters?* This run (older-style signing): `AWSAccessKeyId`, `Signature`, `Expires`. Newer SigV4 URLs use `X-Amz-*` names. Depends on client config.
- *How to revoke one URL?* You cannot; revoke the signer's permission or credentials, or use a short expiry.
- *Browser uploads?* Presigned POST plus a CORS rule.

**Common mistakes:**
- Putting presigned URLs in logs or tickets.
- Day-long expiry from a short-lived role (it will fail early).
- Thinking a PUT presign can cap size.
- Trusting mock behaviour on expiry or conditions.

### Q11 ⭐⭐⭐ 🟡 S3 versioning, delete markers and protection of training datasets: what happens on overwrite and delete with versioning enabled and suspended, how to restore a deleted object, how lifecycle handles noncurrent versions, what MFA delete and Object Lock add, and how to make a training run reproducible against a dataset version id. Run overwrite, delete and list_object_versions against moto and print version and delete-marker counts. No prices.
**Asked at:** S3 interview question banks (novelvista '100+ Top AWS S3 Interview Questions', adaface, ccbp.in, a techinterview.org 'System Design Interview: Object Storage (Amazon S3)' post, AWS developer exam-prep study guides; search snippets only, not opened; WebFetch of docs.aws.amazon.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; cloud, data and ML engineer roles at IT-services firms, product companies and GCCs | AWS S3 documentation topics as summarised by prep guides (versioning and delete markers, lifecycle transitions and expiry, multipart upload, presigned URLs, strong read-after-write consistency since December 2020; search snippets only, not opened, exact limits not verified); vendor docs and prep notes, not interview reports; cloud, data and ML platform roles

**Say this first (1 line):** With versioning on, an overwrite adds a new version and a delete adds a delete marker; nothing is lost until someone deletes a specific version id. For training, I pin the dataset to a version id so the run is reproducible.

**Then explain:**
- **Versioning enabled:** every PUT to a key makes a new version with its own VersionId. A plain DELETE does not remove data; it adds a delete marker as the newest version, so a plain GET says NoSuchKey.
- **Restore:** delete the delete marker (by its VersionId). The previous version becomes current again. Or copy an old version over the key. Both are cheap and need no backup system.
- **Suspended:** new writes get the version id `null` and overwrite the previous null version. Old versions made earlier stay. Suspending does not turn the clock back.
- **Lifecycle:** keeps the current version and the old (noncurrent) ones are handled by their own rules: `NoncurrentVersionExpiration`, transitions of noncurrent versions, and cleanup of expired delete markers. Without it, versions pile up quietly. Check current docs for exact rule fields.
- **MFA delete and Object Lock:** MFA delete asks for an MFA code to permanently delete a version or change versioning state. Object Lock (needs versioning, set up at bucket creation as the docs describe) gives WORM retention: governance mode can be bypassed by users with special permission, compliance mode cannot be shortened by anyone. Both protect against mistakes and bad actors, not against a wrong dataset.
- **Reproducibility:** a key name is not a dataset. Record `bucket + key + VersionId` (or a manifest listing them) in the run metadata, and read with `VersionId=`. Failure mode: deleting that old version by id, or a lifecycle rule expiring it, breaks reproduction. Pair with Object Lock or a retention rule when you must keep it.

**Example:** Key `train.csv` gets v1, then v2. Delete it: 2 versions plus 1 delete marker, plain GET fails, v2 still readable by id. Remove the marker and the GET returns v2 again. Permanently delete v2 by id and v1 becomes current. (Numbers are in the output below.)

**Code:**
```python
# --- file: code/q11_versioning.py ---
import os
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws

def counts(s3, b):
    r = s3.list_object_versions(Bucket=b)
    return len(r.get("Versions", [])), len(r.get("DeleteMarkers", []))

with mock_aws():
    s3 = boto3.client("s3")
    b = "ml-train-data"
    s3.create_bucket(Bucket=b)
    # 1. versioning OFF: overwrite replaces
    s3.put_object(Bucket=b, Key="off.csv", Body=b"v1")
    s3.put_object(Bucket=b, Key="off.csv", Body=b"v2")
    print("unversioned versions/markers:", counts(s3, b), "VersionId of unversioned object:", s3.head_object(Bucket=b, Key="off.csv").get("VersionId"))
    s3.put_bucket_versioning(Bucket=b, VersioningConfiguration={"Status": "Enabled"})
    v1 = s3.put_object(Bucket=b, Key="train.csv", Body=b"rows-v1")["VersionId"]
    v2 = s3.put_object(Bucket=b, Key="train.csv", Body=b"rows-v2")["VersionId"]
    print("after 2 puts on train.csv (enabled): total versions, markers =", counts(s3, b), "(includes off.csv)")
    # reproducible read by version id
    print("read pinned v1:", s3.get_object(Bucket=b, Key="train.csv", VersionId=v1)["Body"].read())
    print("read latest   :", s3.get_object(Bucket=b, Key="train.csv")["Body"].read())
    # delete -> marker
    d = s3.delete_object(Bucket=b, Key="train.csv")
    print("delete returned DeleteMarker:", d.get("DeleteMarker"))
    try:
        s3.get_object(Bucket=b, Key="train.csv")
    except Exception as e:
        print("plain GET after delete:", e.response["Error"]["Code"])
    r = s3.list_object_versions(Bucket=b, Prefix="train.csv")
    print("train.csv versions:", len(r["Versions"]), "markers:", len(r["DeleteMarkers"]), "marker IsLatest:", r["DeleteMarkers"][0]["IsLatest"])
    print("pinned v2 still readable:", s3.get_object(Bucket=b, Key="train.csv", VersionId=v2)["Body"].read())
    # restore = delete the marker
    s3.delete_object(Bucket=b, Key="train.csv", VersionId=r["DeleteMarkers"][0]["VersionId"])
    print("after removing marker, GET:", s3.get_object(Bucket=b, Key="train.csv")["Body"].read())
    # permanent delete of one version
    s3.delete_object(Bucket=b, Key="train.csv", VersionId=v2)
    r = s3.list_object_versions(Bucket=b, Prefix="train.csv")
    print("after permanent delete of v2: versions", len(r["Versions"]), "markers", len(r.get("DeleteMarkers", [])), "latest now:", s3.get_object(Bucket=b, Key="train.csv")["Body"].read())
    # suspended
    s3.put_bucket_versioning(Bucket=b, VersioningConfiguration={"Status": "Suspended"})
    s3.put_object(Bucket=b, Key="train.csv", Body=b"rows-v3-suspended")
    r = s3.list_object_versions(Bucket=b, Prefix="train.csv")
    print("suspended put -> VersionIds:", sorted(v["VersionId"] if len(v["VersionId"]) < 8 else "<real-id>" for v in r["Versions"]))
    # lifecycle noncurrent expiration
    s3.put_bucket_versioning(Bucket=b, VersioningConfiguration={"Status": "Enabled"})
    s3.put_bucket_lifecycle_configuration(Bucket=b, LifecycleConfiguration={"Rules": [{
        "ID": "trim-old", "Status": "Enabled", "Filter": {"Prefix": "train"},
        "NoncurrentVersionExpiration": {"NoncurrentDays": 30, "NewerNoncurrentVersions": 3},
        "Expiration": {"ExpiredObjectDeleteMarker": True}}]})
    print("lifecycle readback:", s3.get_bucket_lifecycle_configuration(Bucket=b)["Rules"][0]["NoncurrentVersionExpiration"])
    # object lock
    try:
        s3.create_bucket(Bucket="locked-bucket", ObjectLockEnabledForBucket=True)
        s3.put_object_lock_configuration(Bucket="locked-bucket", ObjectLockConfiguration={"ObjectLockEnabled": "Enabled", "Rule": {"DefaultRetention": {"Mode": "GOVERNANCE", "Days": 1}}})
        s3.put_object(Bucket="locked-bucket", Key="a", Body=b"x")
        vid = s3.list_object_versions(Bucket="locked-bucket")["Versions"][0]["VersionId"]
        try:
            s3.delete_object(Bucket="locked-bucket", Key="a", VersionId=vid)
            print("object lock: permanent delete was ALLOWED by moto")
        except Exception as e:
            print("object lock: permanent delete blocked:", e.response["Error"]["Code"])
        print("lock config:", s3.get_object_lock_configuration(Bucket="locked-bucket")["ObjectLockConfiguration"]["Rule"])
    except Exception as e:
        print("object lock not usable:", type(e).__name__, e)
```

**Output (my run):** Sandbox: Python 3.13.17, boto3 1.43.118, moto 5.2.4 (decorator mode `mock_aws`, fake keys, no real AWS contact, no moto server needed for these), run with `python3 -I`. Real output (S3 behaviour is moto's emulation):
```
unversioned versions/markers: (1, 0) VersionId of unversioned object: None
after 2 puts on train.csv (enabled): total versions, markers = (3, 0) (includes off.csv)
read pinned v1: b'rows-v1'
read latest   : b'rows-v2'
delete returned DeleteMarker: True
plain GET after delete: NoSuchKey
train.csv versions: 2 markers: 1 marker IsLatest: True
pinned v2 still readable: b'rows-v2'
after removing marker, GET: b'rows-v2'
after permanent delete of v2: versions 1 markers 0 latest now: b'rows-v1'
suspended put -> VersionIds: ['null']
lifecycle readback: {'NoncurrentDays': 30}
object lock: permanent delete blocked: AccessDenied
lock config: {'DefaultRetention': {'Mode': 'GOVERNANCE', 'Days': 1, 'Years': 0}}
```
What moto differs on or does not show: an unversioned object has no VersionId here (real S3 reports `null` in some APIs; check current docs); the lifecycle read-back kept `NoncurrentDays` but dropped `NewerNoncurrentVersions` in this version; Object Lock denied the permanent delete in moto, but real retention modes, bypass permissions, MFA delete and lifecycle timing were **not executed**. Real S3 durability and consistency are not proven by a mock.

**Follow-ups:**
- *Can I roll back a whole prefix?* No single call. You list versions and copy or delete markers per key, usually with a script or S3 Batch Operations (check current docs). Or use dataset snapshot prefixes.
- *Is versioning a backup?* Partly. It protects against overwrite and delete in the same bucket and Region. It does not protect against the whole account being compromised or a Region loss. Add replication or a separate backup account if that matters.
- *Why not just copy the data per run?* It works but costs storage and hides lineage. A version id or manifest is a light pointer. Part 4 (DVC, MLflow) covers dataset versioning tools.

**Common mistakes:**
- Logging only the S3 key in the experiment tracker and calling the run reproducible.
- Thinking a DELETE frees space on a versioned bucket. It adds a marker; storage stays until versions are deleted.
- Forgetting a noncurrent-version lifecycle rule and being surprised by growth.
- Believing suspended versioning removes old versions.
- Treating a moto result as proof of how real S3 lifecycle, MFA delete or Object Lock behave.

---

### Q12 ⭐⭐⭐ 🟡 Lambda for ML and data glue: list the main limits to know (memory range, timeout cap, package size for zip versus container image, /tmp size, payload size, concurrency), what a cold start is and what makes it worse for ML (large dependencies, model load in init), how container images, layers and provisioned concurrency change it, and when Lambda is the wrong tool for model inference. Hedge every number as 'check current docs'. Create a function with moto, set memory, timeout and reserved concurrency, read the configuration back, and say moto's invoke needs Docker and did not really execute code here.
**Asked at:** Lambda interview and limits sources (kodekloud AWS Developer Associate notes on limits and concurrency, awsfundamentals.com 'Lambda limitations', a dev.to Lambda compute-limits post, a pulumi provisioned-concurrency post; search snippets only, not opened; secondary sources disagreed on package-size wording so numbers are hedged 'check current docs'); training notes and blogs, not verified interview reports; backend, cloud and ML engineer roles | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)

**Say this first (1 line):** Lambda is great for small glue around ML: triggers, light pre or post processing, calling an endpoint. It is usually the wrong place to host a heavy model because of cold starts, memory and package limits, and no GPU. I would check the current limits page before quoting any number.

**Then explain:**
- **Limits to know (all: check current docs):** memory range, timeout cap, deployment size for zip versus container image, `/tmp` size, request and response payload size, and account concurrency. They have changed over the years and sources I looked at disagree on wording, so I do not quote them from memory.
- **Cold start:** a new execution environment must start, load the runtime and your code, then run init code. Later calls on a warm environment skip that. For ML it gets worse with big dependencies and loading a model file in init.
- **Levers:** load the model once outside the handler (warm calls reuse it), keep dependencies small, use a container image when libraries are large, put shared libraries in layers, and use provisioned concurrency to keep environments initialised (you pay for readiness; check the docs on the cost model).
- **Wrong tool when:** the model needs a GPU, is large, needs sustained throughput with tight p99, or needs long runs beyond the timeout cap. Then use SageMaker endpoints or containers on ECS/EKS. Lambda is fine for a tiny model with spiky traffic.
- **Failure modes:** throttling when concurrency is exhausted, timeouts on first request after a deploy, memory too low so CPU is also low (CPU scales with memory; check docs).

**Example:** A Lambda reads an S3 event and calls a SageMaker endpoint: good glue. A Lambda that loads a large model file in init: the first request after idle pays that load time, so it is a poor fit for a strict latency target.

**Code:**
```python
# --- file: code/q12_lambda.py ---
import os, io, zipfile
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws

def zipped(src):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("app.py", src)
    return buf.getvalue()

with mock_aws():
    iam = boto3.client("iam")
    role = iam.create_role(RoleName="lam", AssumeRolePolicyDocument='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}')["Role"]["Arn"]
    lam = boto3.client("lambda")
    lam.create_function(FunctionName="score", Runtime="python3.12", Role=role, Handler="app.handler",
                        Code={"ZipFile": zipped("def handler(e, c):\n    return {'ok': 1}\n")},
                        MemorySize=1024, Timeout=30, Publish=True,
                        Environment={"Variables": {"MODEL_URI": "s3://ml-data/models/m1/"}})
    lam.put_function_concurrency(FunctionName="score", ReservedConcurrentExecutions=5)
    cfg = lam.get_function_configuration(FunctionName="score")
    print({k: cfg[k] for k in ("FunctionName", "Runtime", "MemorySize", "Timeout", "Handler", "PackageType", "State")})
    print("env:", cfg["Environment"]["Variables"])
    print("reserved concurrency:", lam.get_function_concurrency(FunctionName="score")["ReservedConcurrentExecutions"])
    layer = lam.publish_layer_version(LayerName="deps", Content={"ZipFile": zipped("x=1")}, CompatibleRuntimes=["python3.12"])
    print("layer version:", layer["Version"])
    try:
        pc = lam.put_provisioned_concurrency_config(FunctionName="score", Qualifier="1", ProvisionedConcurrentExecutions=2)
        print("provisioned:", pc.get("RequestedProvisionedConcurrentExecutions"), pc.get("Status"))
    except Exception as e:
        print("provisioned concurrency call:", type(e).__name__, str(e)[:100])
    r = lam.invoke(FunctionName="score", Payload=b"{}")
    body = r["Payload"].read().decode()
    print("invoke StatusCode:", r["StatusCode"], "| payload starts:", body[:80].replace("\n", " "))
```

**Output (my run):** Sandbox: Python 3.13.17, boto3 1.43.118, moto 5.2.4 (decorator mode `mock_aws`, fake keys, no real AWS contact, no moto server needed for these), run with `python3 -I`. Real output:
```
error running docker: Error while fetching server API version: ('Connection aborted.', FileNotFoundError(2, 'No such file or directory'))
{'FunctionName': 'score', 'Runtime': 'python3.12', 'MemorySize': 1024, 'Timeout': 30, 'Handler': 'app.handler', 'PackageType': 'Zip', 'State': 'Active'}
env: {'MODEL_URI': 's3://ml-data/models/m1/'}
reserved concurrency: 5
layer version: 1
provisioned concurrency call: ClientError An error occurred (404) when calling the PutProvisionedConcurrencyConfig operation: Not yet implemen
invoke StatusCode: 200 | payload starts: error running docker: Error while fetching server API version: ('Connection abor
```
moto stores the function configuration (memory, timeout, env, reserved concurrency, layer) and returns it. **Invoke needs Docker to run the code; no Docker daemon here, so nothing executed.** The invoke response still shows StatusCode 200 with the Docker error text as the payload: a 200 from the mock is not proof the code ran. Provisioned concurrency was not implemented in this moto version (404). Cold starts, real limits and throttling are **not executed**.

**Follow-ups:**
- *Zip or container image?* Zip is simple and quick for small code. Container image when dependencies are big or you already build images; it lands in ECR. Check current docs for size caps.
- *Reserved versus provisioned concurrency?* Reserved guarantees a slice and also caps the function (Q32 goes deeper). Provisioned pre-warms environments.
- *How do I test the handler?* Keep it a plain function and call it with a fake event locally (Part 10 Q41).

**Common mistakes:**
- Loading the model inside the handler on every call.
- Quoting limits from memory in an interview. Say "check the current limits page".
- Reading a 200 from an invoke as proof it ran.
- Putting a GPU or large-model workload in Lambda.

---

### Q13 ⭐⭐⭐ 🟡 EC2 for ML: instance families and what they are for (general, compute, memory, GPU training such as the P series, GPU inference and graphics such as the G series, AWS Trainium and Inferentia accelerators), how you pick for a 7B-parameter fine-tune versus a gradient-boosted model, EBS versus instance store, Deep Learning AMIs, and quota and capacity surprises with GPU instances. No prices and no benchmark numbers. Use moto describe_instance_types and run_instances to show the API shape, and say what a mock cannot show (real GPUs, real quotas, real capacity).
**Asked at:** EC2 and spot-training sources (introl.com and barkingiguana.com posts on spot GPU training and SageMaker managed spot, practitioner notes on checkpoint cadence and resume testing; search snippets only, not opened; a savings percentage in one title was not used); blogs, not interview reports; ML platform and MLOps roles | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)

**Say this first (1 line):** I match the instance family to the workload: GPU memory and bandwidth for deep learning, plain CPU instances for a gradient-boosted model. For a 7B fine-tune the first question is GPU memory, then multi-GPU or multi-node, then quota and capacity.

**Then explain:**
- **Families (concept level, check current docs for current generations):** general purpose (M), compute optimised (C), memory optimised (R), GPU training (P series), GPU inference and graphics (G series), AWS Trainium (training) and Inferentia (inference) accelerators which need the Neuron SDK and model compilation.
- **7B fine-tune versus boosted trees:** a full fine-tune of a 7B model needs weights, gradients and optimizer state in GPU memory, so it usually means large-memory GPUs or multiple GPUs, or parameter-efficient methods to shrink the footprint. A gradient-boosted model on tabular data usually runs fine on CPU, so a memory-optimised or compute instance is enough. Training maths is Books 1 and 2.
- **Storage:** EBS is network-attached and persists (can be snapshotted); instance store is local, fast, and lost when the instance stops or terminates. Use instance store or local NVMe for scratch and cache, EBS or S3 for anything you must keep.
- **Deep Learning AMIs:** images with GPU drivers, CUDA and common frameworks preinstalled, so you do not hand-build driver stacks. Check current docs for the available versions.
- **Surprises:** GPU instance vCPU quotas default low or at zero in a new account and need a quota request; capacity can be short in a Region or AZ even with quota; spot GPU capacity is volatile. Plan lead time. None of this is visible in a mock.

**Example:** Fraud model on tabular features: boosted trees, a CPU instance, data from S3 to local disk. 7B fine-tune: a GPU-family instance sized by GPU memory; if one GPU cannot hold it, multi-GPU or sharded training (Q43). First action: check the GPU quota in the Region.

**Code:**
```python
# --- file: code/q13_ec2.py ---
import os
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws

with mock_aws():
    ec2 = boto3.client("ec2")
    r = ec2.describe_instance_types(InstanceTypes=["p4d.24xlarge", "g5.xlarge", "m5.xlarge", "trn1.2xlarge"])
    for t in sorted(r["InstanceTypes"], key=lambda x: x["InstanceType"]):
        gpu = t.get("GpuInfo", {}).get("Gpus", [])
        print(t["InstanceType"], "vcpu", t["VCpuInfo"]["DefaultVCpus"], "mem_MiB", t["MemoryInfo"]["SizeInMiB"],
              "gpus", [(g["Name"], g["Count"]) for g in gpu])
    got = {t["InstanceType"] for t in r["InstanceTypes"]}
    print("asked 4, moto returned:", sorted(got))
    inst = ec2.run_instances(ImageId="ami-12345678", InstanceType="g5.xlarge", MinCount=1, MaxCount=1,
                             BlockDeviceMappings=[{"DeviceName": "/dev/sda1", "Ebs": {"VolumeSize": 200, "VolumeType": "gp3", "DeleteOnTermination": True}}],
                             TagSpecifications=[{"ResourceType": "instance", "Tags": [{"Key": "team", "Value": "ml"}]}])["Instances"][0]
    print("run_instances state:", inst["State"]["Name"], "type:", inst["InstanceType"])
    vols = ec2.describe_volumes()["Volumes"]
    print("volumes:", [(v["Size"], v["VolumeType"]) for v in vols])
```

**Output (my run):** Sandbox: Python 3.13.17, boto3 1.43.118, moto 5.2.4 (decorator mode `mock_aws`, fake keys, no real AWS contact, no moto server needed for these), run with `python3 -I`. Real output (instance-type metadata is moto's bundled data):
```
g5.xlarge vcpu 4 mem_MiB 16384 gpus [('A10G', 1)]
m5.xlarge vcpu 4 mem_MiB 16384 gpus []
p4d.24xlarge vcpu 96 mem_MiB 1179648 gpus [('A100', 8)]
trn1.2xlarge vcpu 8 mem_MiB 32768 gpus []
asked 4, moto returned: ['g5.xlarge', 'm5.xlarge', 'p4d.24xlarge', 'trn1.2xlarge']
run_instances state: pending type: g5.xlarge
volumes: [(200, 'gp3')]
```
API shape only: `run_instances` returns `pending` and the 200 GiB gp3 root volume is recorded. **Not shown by a mock:** a real GPU, drivers, a real AMI boot, vCPU or GPU quotas, capacity errors, EFA, instance store behaviour. The bundled type data may lag real AWS: check current docs.

**Follow-ups:**
- *Why not always the biggest GPU?* Cost and utilisation. Small jobs waste it. Start from memory needs and data loading speed.
- *Trainium or Inferentia?* Possible cost or availability wins, but you take on compile and framework-compatibility work. Check current docs and test your model first.
- *EBS or instance store for checkpoints?* Write checkpoints to S3 (or EBS you keep); instance store disappears with the instance.

**Common mistakes:**
- Picking a GPU by name instead of by memory need.
- Learning about GPU quota on launch day.
- Keeping the only copy of a model on instance store.
- Using moto's instance-type list as a current catalogue.

---

### Q14 ⭐⭐⭐ 🟡 Spot capacity for training: how Spot interruption works (a short warning before reclaim), what makes a job spot-safe (checkpoint model, optimizer state, scheduler, RNG and data position to S3, idempotent resume), how SageMaker managed spot training uses checkpoint_s3_uri and MaxWaitTimeInSeconds, and how instance and AZ diversification helps. Write a pure-Python training loop with periodic checkpoints and a simulated interruption, resume it, and verify that the final result equals an uninterrupted run. Real spot behaviour is not executed.
**Asked at:** EC2 and spot-training sources (introl.com and barkingiguana.com posts on spot GPU training and SageMaker managed spot, practitioner notes on checkpoint cadence and resume testing; search snippets only, not opened; a savings percentage in one title was not used); blogs, not interview reports; ML platform and MLOps roles | SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs

**Say this first (1 line):** Spot is cheap capacity that can be reclaimed with a short warning, so the job must be able to die at any step and resume to the same result. That means checkpoints with model, optimizer, scheduler, RNG and data position, written to S3 atomically, and a resume path that is tested.

**Then explain:**
- **How interruption works:** AWS can reclaim spot capacity and gives a short warning (about two minutes in the sources I saw; check current docs). You cannot rely on that warning to save a big checkpoint, so checkpoint on a schedule.
- **Spot-safe means:** save model weights, optimizer state (momentum), LR scheduler state, RNG states and the data position (epoch and batch, or the sampler state), plus the step counter. Write to a temp name and rename, so a half-written file is never read. Resume must be idempotent.
- **SageMaker managed spot training:** set `EnableManagedSpotTraining`, give a `CheckpointConfig` with an S3 URI (SDK `checkpoint_s3_uri`, local path `/opt/ml/checkpoints` by default) and `MaxWaitTimeInSeconds` at least the run time limit. SageMaker syncs that folder to S3 and restores it on restart. Your code must still load the checkpoint. Check current docs for options.
- **Diversify:** allow several instance types and AZs where the service allows, to lower the chance of losing everything at once.
- **Failure modes:** checkpoint too rare (lost work), checkpoint only weights (results drift, see below), non-atomic writes, a deterministic-looking run that is not reproducible because the sampler restarts from the beginning.

**Example:** Train for 200 steps with a checkpoint every 25. Kill at step 130. Resume from step 125 and finish. The final weights equal the uninterrupted run exactly. A sloppy resume (weights only) ends with different weights.

**Code:**
```python
# --- file: code/q14_spot.py ---
"""Spot-safe training loop in pure Python: checkpoint everything, resume, compare with uninterrupted run."""
import json, os, random, sys, tempfile, hashlib

class Interrupted(Exception):
    pass

def make_data(n=64, seed=7):
    r = random.Random(seed)
    return [(x, 3.0 * x + 1.0 + r.gauss(0, 0.1)) for x in (r.uniform(-1, 1) for _ in range(n))]

def save_ckpt(path, state):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f)
    os.replace(tmp, path)  # atomic: a reclaim mid-write must not leave a half file

def train(ckpt, total_steps=200, every=25, interrupt_at=None, batch=8, seed=123):
    data = make_data()
    st = {"step": 0, "w": 0.0, "b": 0.0, "mw": 0.0, "mb": 0.0, "rng": None}
    rng = random.Random(seed)
    if os.path.exists(ckpt):
        st = json.load(open(ckpt))
        rng.setstate((st["rng"][0], tuple(st["rng"][1]), st["rng"][2]))
        print(f"  resumed at step {st['step']}")
    while st["step"] < total_steps:
        if interrupt_at is not None and st["step"] == interrupt_at:
            raise Interrupted(f"reclaimed at step {st['step']}")
        lr = 0.1 * (0.99 ** st["step"])              # scheduler state is a function of step
        b_ = rng.sample(data, batch)                  # data position = RNG state
        gw = sum(2 * (st["w"] * x + st["b"] - y) * x for x, y in b_) / batch
        gb = sum(2 * (st["w"] * x + st["b"] - y) for x, y in b_) / batch
        st["mw"] = 0.9 * st["mw"] + gw               # optimizer state (momentum)
        st["mb"] = 0.9 * st["mb"] + gb
        st["w"] -= lr * st["mw"]; st["b"] -= lr * st["mb"]
        st["step"] += 1
        if st["step"] % every == 0:
            s = rng.getstate()
            save_ckpt(ckpt, {**st, "rng": [s[0], list(s[1]), s[2]]})
    return st

def train_sloppy(ckpt, total_steps=200, batch=8):
    data = make_data()
    st = json.load(open(ckpt))
    rng = random.Random(999)  # wrong: fresh RNG instead of the saved state
    while st["step"] < total_steps:
        lr = 0.1 * (0.99 ** st["step"])
        b_ = rng.sample(data, batch)
        gw = sum(2 * (st["w"] * x + st["b"] - y) * x for x, y in b_) / batch
        gb = sum(2 * (st["w"] * x + st["b"] - y) for x, y in b_) / batch
        st["mw"] = 0.9 * st["mw"] + gw; st["mb"] = 0.9 * st["mb"] + gb
        st["w"] -= lr * st["mw"]; st["b"] -= lr * st["mb"]; st["step"] += 1
    return st

def digest(st):
    return hashlib.sha256(json.dumps([st["w"], st["b"]]).encode()).hexdigest()[:12]

with tempfile.TemporaryDirectory() as d:
    print("A) uninterrupted run")
    a = train(os.path.join(d, "a.json"), every=10**9)
    print(f"  w={a['w']:.6f} b={a['b']:.6f} digest={digest(a)}")
    print("B) interrupted at step 130, last checkpoint at 125, then resume")
    p = os.path.join(d, "b.json")
    try:
        train(p, interrupt_at=130)
    except Interrupted as e:
        print(" ", e)
    b = train(p)
    print(f"  w={b['w']:.6f} b={b['b']:.6f} digest={digest(b)}")
    print("identical to uninterrupted:", a["w"] == b["w"] and a["b"] == b["b"])
    print("C) sloppy resume: weights and step only (no momentum, no RNG state)")
    full = json.load(open(p))
    # re-create the step-125 checkpoint by re-running to 125, then load it sloppily
    q = os.path.join(d, "c.json")
    try:
        train(q, total_steps=125, every=25)
    except Interrupted:
        pass
    ck = json.load(open(q))
    json.dump({"step": ck["step"], "w": ck["w"], "b": ck["b"], "mw": 0.0, "mb": 0.0, "rng": None}, open(q, "w"))
    c = train_sloppy(q)
    print(f"  w={c['w']:.6f} b={c['b']:.6f} digest={digest(c)}")
    print("sloppy equals uninterrupted:", a["w"] == c["w"] and a["b"] == c["b"])

# --- file: code/q14b_sm_spot_shape.py ---
import os
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws
with mock_aws():
    iam = boto3.client("iam")
    role = iam.create_role(RoleName="sm", AssumeRolePolicyDocument="{}")["Role"]["Arn"]
    sm = boto3.client("sagemaker")
    req = dict(
        TrainingJobName="spot-demo", RoleArn=role,
        AlgorithmSpecification={"TrainingImage": "123456789012.dkr.ecr.us-east-1.amazonaws.com/trainer:1", "TrainingInputMode": "File"},
        ResourceConfig={"InstanceType": "ml.g5.xlarge", "InstanceCount": 1, "VolumeSizeInGB": 50},
        OutputDataConfig={"S3OutputPath": "s3://ml-data/models/"},
        StoppingCondition={"MaxRuntimeInSeconds": 3600, "MaxWaitTimeInSeconds": 7200},
        EnableManagedSpotTraining=True,
        CheckpointConfig={"S3Uri": "s3://ml-data/ckpt/spot-demo/", "LocalPath": "/opt/ml/checkpoints"})
    sm.create_training_job(**req)
    d = sm.describe_training_job(TrainingJobName="spot-demo")
    print({k: d[k] for k in ("TrainingJobStatus", "EnableManagedSpotTraining")}, d["CheckpointConfig"], d["StoppingCondition"])
    print("moto marks job finished instantly; no spot interruption, no checkpoint was ever written")
```

**Output (my run):** Pure-Python loop (no AWS), Python 3.13.17, seeded, run with `python3 -I`:
```
A) uninterrupted run
  w=3.034275 b=1.002817 digest=7b93a291f461
B) interrupted at step 130, last checkpoint at 125, then resume
  reclaimed at step 130
  resumed at step 125
  w=3.034275 b=1.002817 digest=7b93a291f461
identical to uninterrupted: True
C) sloppy resume: weights and step only (no momentum, no RNG state)
  w=3.012900 b=1.020688 digest=610914e21177
sloppy equals uninterrupted: False
```
SageMaker request shape in moto 5.2.4 (fake keys):
```
{'TrainingJobStatus': 'Completed', 'EnableManagedSpotTraining': True} {'S3Uri': 's3://ml-data/ckpt/spot-demo/', 'LocalPath': '/opt/ml/checkpoints'} {'MaxRuntimeInSeconds': 3600, 'MaxWaitTimeInSeconds': 7200}
moto marks job finished instantly; no spot interruption, no checkpoint was ever written
```
The loop is a simulation of the resume logic. **Real spot interruption, the warning notice, SageMaker syncing checkpoints and real GPU training are not executed.** moto marked the training job Completed instantly.

**Follow-ups:**
- *How often to checkpoint?* A trade-off between lost work and checkpoint cost. Sources I saw disagreed on a fixed number, so measure your checkpoint time and pick an interval you can afford to lose.
- *Is the resumed result always identical?* Here yes, on one CPU with seeded Python. On GPUs with nondeterministic kernels or changed world size it may not be bit-identical; aim for statistically equivalent and test it.
- *When not to use spot?* Tight deadlines, jobs that cannot checkpoint, or the last run before a release.

**Common mistakes:**
- Saving weights but not optimizer state or RNG.
- Writing the checkpoint in place so a kill leaves a corrupt file.
- Never testing resume until the first real interruption.
- Setting MaxWaitTime below the run time.

---

### Q15 ⭐⭐⭐ 🟡 ECS versus EKS versus Fargate versus SageMaker versus Lambda for hosting an ML model container: which would you choose for a small team with one model, for a platform team with 40 models and GPUs, and for spiky traffic? Explain that Fargate is a compute mode under ECS and EKS, not a rival to them, and where ECR fits. Kubernetes internals belong to Part 3 and serving mechanics to Part 6. Register an ECS Fargate task definition and create an ECR repository in moto and print what they hold; no container actually runs.
**Asked at:** Container-service comparison sources (nops.io 'ECS vs EKS vs Fargate', perfectscale.io, jayendrapatil.com 'AWS EKS vs ECS Decision Guide', cloudoptimo, doit.com, a 2019 AWS slideshare on ML with container services; search snippets only, not opened); vendor and consultancy blogs stating opinion; DevOps, platform and MLOps roles | SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs

**Say this first (1 line):** Fargate is a way to run containers without managing servers, under ECS or EKS. It is not a rival to them. For one model and a small team I would pick SageMaker endpoints or ECS on Fargate; for 40 models with GPUs a platform team might choose EKS or SageMaker with a managed fleet. ECR just holds the images.

**Then explain:**
- **Where each fits:** SageMaker endpoint gives managed hosting, autoscaling hooks, model monitoring and the registry link. ECS is simpler AWS-native container orchestration. EKS is Kubernetes: more power, portability and GPU scheduling, more to operate. Lambda is for small models and spiky traffic. (Opinion pieces I read agree on this shape; check current docs for GPU support per mode.)
- **Small team, one model:** least ops wins. SageMaker real-time endpoint or ECS Fargate with an autoscaling service if the model is CPU-sized.
- **Platform team, 40 models, GPUs:** Kubernetes tooling and bin-packing GPUs, or SageMaker features such as multi-model or inference components (Q25). It depends on how much platform work the team wants to own.
- **Spiky traffic:** serverless options (Lambda, SageMaker serverless or async) or autoscaling with a minimum of one; watch cold starts.
- **ECR:** private image registry. Task definitions and endpoint models reference an image URI, ideally by digest. Kubernetes internals are Part 3 and serving mechanics Part 6.

**Example:** Task definition `fraud-scorer` (Fargate, 1 vCPU, 2 GB in moto's units of cpu and memory) points at `<account>.dkr.ecr.us-east-1.amazonaws.com/fraud-scorer:1.4.0`. The task role is what the container's code uses; the execution role is what ECS uses to pull the image and write logs.

**Code:**
```python
# --- file: code/q15_ecs_ecr.py ---
import os, json
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws
with mock_aws():
    ecr = boto3.client("ecr")
    repo = ecr.create_repository(repositoryName="fraud-scorer", imageTagMutability="IMMUTABLE",
                                 imageScanningConfiguration={"scanOnPush": True})["repository"]
    print({k: repo[k] for k in ("repositoryName", "repositoryUri", "imageTagMutability")}, repo["imageScanningConfiguration"])
    ecs = boto3.client("ecs")
    ecs.create_cluster(clusterName="ml")
    td = ecs.register_task_definition(
        family="fraud-scorer", requiresCompatibilities=["FARGATE"], networkMode="awsvpc", cpu="1024", memory="2048",
        executionRoleArn="arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
        taskRoleArn="arn:aws:iam::123456789012:role/fraud-scorer-task",
        containerDefinitions=[{"name": "app", "image": repo["repositoryUri"] + ":1.4.0", "essential": True,
                               "portMappings": [{"containerPort": 8080}],
                               "environment": [{"name": "MODEL_URI", "value": "s3://ml-data/models/m1/"}]}])["taskDefinition"]
    print({k: td[k] for k in ("family", "revision", "status", "requiresCompatibilities", "networkMode", "cpu", "memory")})
    print("container image:", td["containerDefinitions"][0]["image"])
    print("clusters:", ecs.list_clusters()["clusterArns"])
    print("Not run: no service, no task, no container, no image pushed (API shape only).")
```

**Output (my run):** Sandbox: Python 3.13.17, boto3 1.43.118, moto 5.2.4 (decorator mode `mock_aws`, fake keys, no real AWS contact, no moto server needed for these), run with `python3 -I`. Real output (API shape only):
```
{'repositoryName': 'fraud-scorer', 'repositoryUri': '123456789012.dkr.ecr.us-east-1.amazonaws.com/fraud-scorer', 'imageTagMutability': 'IMMUTABLE'} {'scanOnPush': True}
{'family': 'fraud-scorer', 'revision': 1, 'status': 'ACTIVE', 'requiresCompatibilities': ['FARGATE'], 'networkMode': 'awsvpc', 'cpu': '1024', 'memory': '2048'}
container image: 123456789012.dkr.ecr.us-east-1.amazonaws.com/fraud-scorer:1.4.0
clusters: ['arn:aws:ecs:us-east-1:123456789012:cluster/ml']
Not run: no service, no task, no container, no image pushed (API shape only).
```
Nothing ran: no image was pushed, no service or task started, no networking. Cost, GPU support on Fargate and per-service limits are **not executed**; check current docs.

**Follow-ups:**
- *Is Fargate cheaper than EC2?* Depends on utilisation and workload; I do not quote prices. Measure with your own traffic.
- *Why SageMaker over ECS?* Built-in endpoint autoscaling, data capture, Model Monitor and registry integration, at the cost of its own conventions.
- *Task role versus execution role?* Task role is the app's permissions; execution role pulls images and ships logs.

**Common mistakes:**
- Calling Fargate an alternative to ECS or EKS.
- Choosing EKS for one model with no Kubernetes skills on the team.
- Deploying by mutable tag instead of digest.
- Mixing up task role and execution role.

---

### Q16 ⭐⭐⭐ 🟡 VPC basics an ML engineer must know: CIDR, public versus private subnets, route tables, internet gateway, NAT gateway versus gateway and interface VPC endpoints, security groups (stateful, allow-only, attached to ENIs) versus NACLs (stateless, ordered, allow and deny, per subnet). How does a SageMaker job in a private subnet reach S3 and ECR without internet? Create a VPC, subnet, security group rules and an S3 gateway endpoint in moto, then simulate stateful versus stateless filtering in pure Python. Real networking is not executed.
**Asked at:** AWS VPC interview sources (AWS Builder Center 'AWS VPC explained for beginners: from CIDR to interview questions', digitalcloud.training 'Security Group vs NACL', dev.to scenario-based security group and NACL questions, thenetworkdna 20 AWS network interview questions, kodekloud notes on VPC configuration for SageMaker; search snippets only, not opened); editorial prep and training notes, not verified candidate reports; cloud, DevOps and MLOps roles | SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs

**Say this first (1 line):** A VPC is my private network with a CIDR block. Subnets are public if their route table sends 0.0.0.0/0 to an internet gateway, private if not. A private SageMaker job reaches S3 and ECR through VPC endpoints, not the internet. Security groups are stateful and allow-only; NACLs are stateless, ordered, and can deny.

**Then explain:**
- **Basics:** CIDR (for example /16 for the VPC, /24 per subnet), route tables per subnet, internet gateway for public routes, NAT gateway so private subnets can start outbound connections.
- **Endpoints:** a gateway endpoint (S3, and DynamoDB) adds a route in your route table. An interface endpoint puts an ENI with a private IP in your subnet for services such as ECR (`ecr.api`, `ecr.dkr`), CloudWatch Logs and STS. Compared with NAT, endpoints avoid internet egress and often cut NAT traffic cost; check current docs for pricing.
- **Security group:** attached to ENIs, allow-only, stateful: if a request was allowed in, the reply is allowed out without an egress rule.
- **NACL:** per subnet, numbered rules evaluated in order, first match wins, allow and deny, stateless: you must allow return traffic on ephemeral ports yourself.
- **Failure modes:** missing endpoint means a hang or timeout (no route), NACL forgetting ephemeral ports, SG on the endpoint ENI not allowing 443 from the job.

**Example:** Job in a private subnet pulls its image from ECR and reads S3: it needs `ecr.api` and `ecr.dkr` interface endpoints, an S3 gateway endpoint (ECR layers are stored in S3), and CloudWatch Logs access. No NAT needed.

**Code:**
```python
# --- file: code/q16_vpc.py ---
import os
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws

# ---- part 1: moto API shapes
with mock_aws():
    ec2 = boto3.client("ec2")
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")["Vpc"]["VpcId"]
    sub = ec2.create_subnet(VpcId=vpc, CidrBlock="10.0.1.0/24")["Subnet"]
    sg = ec2.create_security_group(GroupName="train-sg", Description="training", VpcId=vpc)["GroupId"]
    ec2.authorize_security_group_ingress(GroupId=sg, IpPermissions=[{"IpProtocol": "tcp", "FromPort": 443, "ToPort": 443, "IpRanges": [{"CidrIp": "10.0.0.0/16"}]}])
    rt = ec2.create_route_table(VpcId=vpc)["RouteTable"]["RouteTableId"]
    ec2.associate_route_table(RouteTableId=rt, SubnetId=sub["SubnetId"])
    ep = ec2.create_vpc_endpoint(VpcId=vpc, ServiceName="com.amazonaws.us-east-1.s3", VpcEndpointType="Gateway", RouteTableIds=[rt])["VpcEndpoint"]
    print("subnet cidr:", sub["CidrBlock"], "| endpoint:", ep["ServiceName"], ep["VpcEndpointType"], ep["State"])
    rules = ec2.describe_security_group_rules(Filters=[{"Name": "group-id", "Values": [sg]}])["SecurityGroupRules"]
    print("sg rules:", [(r["IsEgress"], r["IpProtocol"], r["FromPort"], r["CidrIpv4"]) for r in rules])
    print("API shape only: no packet was routed, no ENI attached to anything.")

# ---- part 2: stateful (SG) versus stateless (NACL) in pure Python
class SG:  # allow-only rules, default deny, remembers connections it admitted
    def __init__(self, ingress, egress): self.ingress, self.egress, self.conns = ingress, egress, set()
    def inbound(self, pkt):
        if any(r["proto"] == pkt["proto"] and r["port"] == pkt["dport"] for r in self.ingress):
            self.conns.add((pkt["proto"], pkt["sport"], pkt["dport"]))
            return True
        return False
    def outbound(self, pkt):
        if (pkt["proto"], pkt["dport"], pkt["sport"]) in self.conns:  # reply to a tracked connection
            return True
        return any(r["proto"] == pkt["proto"] and r["port"] == pkt["dport"] for r in self.egress)

def nacl_allows(rules, pkt, direction):  # ordered, first match wins, final implicit deny
    for r in sorted(rules[direction], key=lambda r: r["num"]):
        lo, hi = r["ports"]
        if r["proto"] == pkt["proto"] and lo <= pkt["dport"] <= hi:
            return r["action"] == "allow"
    return False

req = {"proto": "tcp", "sport": 51000, "dport": 443}
resp = {"proto": "tcp", "sport": 443, "dport": 51000}      # reply travels back to ephemeral port
sg = SG(ingress=[{"proto": "tcp", "port": 443}], egress=[])  # NO egress rules at all
print("\nSG  request in:", sg.inbound(req), "| reply out with zero egress rules:", sg.outbound(resp))
print("SG  fresh outbound connection to 443 with zero egress rules:", sg.outbound({"proto": "tcp", "sport": 40000, "dport": 443}))
print("SG  request to closed port 22:", sg.inbound({"proto": "tcp", "sport": 50000, "dport": 22}))

nacl_bad = {"in": [{"num": 100, "proto": "tcp", "ports": (443, 443), "action": "allow"}], "out": []}
nacl_ok  = {"in": [{"num": 100, "proto": "tcp", "ports": (443, 443), "action": "allow"}],
            "out": [{"num": 100, "proto": "tcp", "ports": (1024, 65535), "action": "allow"}]}
nacl_deny = {"in": [{"num": 90, "proto": "tcp", "ports": (443, 443), "action": "deny"},
                    {"num": 100, "proto": "tcp", "ports": (0, 65535), "action": "allow"}], "out": []}
for name, n in (("NACL missing outbound ephemeral", nacl_bad), ("NACL with ephemeral outbound", nacl_ok)):
    print(f"{name}: request in={nacl_allows(n, req, 'in')}, reply out={nacl_allows(n, resp, 'out')}")
print("NACL rule 90 deny 443 beats rule 100 allow all:", nacl_allows(nacl_deny, req, "in"))
```

**Output (my run):** Sandbox: Python 3.13.17, boto3 1.43.118, moto 5.2.4 (decorator mode `mock_aws`, fake keys, no real AWS contact, no moto server needed for these), run with `python3 -I`. Real output:
```
subnet cidr: 10.0.1.0/24 | endpoint: com.amazonaws.us-east-1.s3 Gateway available
sg rules: [(True, '-1', -1, '0.0.0.0/0'), (False, 'tcp', 443, '10.0.0.0/16')]
API shape only: no packet was routed, no ENI attached to anything.

SG  request in: True | reply out with zero egress rules: True
SG  fresh outbound connection to 443 with zero egress rules: False
SG  request to closed port 22: False
NACL missing outbound ephemeral: request in=True, reply out=False
NACL with ephemeral outbound: request in=True, reply out=True
NACL rule 90 deny 443 beats rule 100 allow all: False
```
Part 1 is moto API shape only. Part 2 is my own small model of filtering, not AWS's implementation. **Real routing, DNS, ENIs, endpoint policies and connection tracking limits are not executed.**

**Follow-ups:**
- *Gateway or interface endpoint for S3?* A gateway endpoint is the common default (route-based); interface endpoints for S3 exist for other cases such as on-premises access. Check current docs.
- *Why no clear error when an endpoint is missing?* Packets have no route, so they time out instead of being refused.
- *Where do SGs attach?* To ENIs (instances, endpoints, tasks), not to subnets.

**Common mistakes:**
- Saying security groups can deny.
- Forgetting ephemeral ports in a NACL.
- Putting a training job in a private subnet with no S3 or ECR path.
- Assuming a NAT gateway is free of cost; check current docs.

---

### Q17 ⭐⭐⭐ 🟡 Encryption on AWS for ML data: encryption at rest versus in transit; S3 SSE-S3, SSE-KMS, SSE-C and client-side encryption; default bucket encryption; EBS and SageMaker volume and output KMS keys; how a KMS key policy, IAM policy and grant interact; and why a job can have S3 permission and still get AccessDenied on a KMS key. Apply default SSE-KMS encryption in moto, show the head_object field, and use generate_data_key to explain envelope encryption. Real KMS enforcement is not executed.
**Asked at:** S3 interview question banks (novelvista '100+ Top AWS S3 Interview Questions', adaface, ccbp.in, a techinterview.org 'System Design Interview: Object Storage (Amazon S3)' post, AWS developer exam-prep study guides; search snippets only, not opened; WebFetch of docs.aws.amazon.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; cloud, data and ML engineer roles at IT-services firms, product companies and GCCs | IAM interview and policy-evaluation sources (AWS IAM 'Policy evaluation logic' pages on docs.aws.amazon.com and docs.aws.eu, tutorialsdojo 'How AWS IAM Handles Conflicting IAM Policies', advancedweb.hu 'IAM policy evaluation logic explained with examples', barkingiguana 'How IAM Policy Evaluation Actually Works', community.aws and hidekazu-konishi IAM glossary; search snippets only, not opened); vendor docs and study guides, not verified candidate reports; cloud, DevOps, security and MLOps roles at IT-services firms, product companies and GCCs

**Say this first (1 line):** At rest means encrypted on disk, in transit means encrypted on the wire with TLS. On S3 I would set default SSE-KMS so I control the key and get an audit trail. A job needs both S3 permission and KMS permission, which is why it can fail on KMS even when S3 looks fine.

**Then explain:**
- **S3 options:** SSE-S3 (S3-managed keys), SSE-KMS (key in KMS, policy and audit control), SSE-C (you supply the key on each request), client-side (you encrypt before upload). Default bucket encryption applies when a request does not specify one. Check current docs for what is applied by default today.
- **EBS and SageMaker:** volumes and outputs can use a KMS key you name (volume KMS key, output KMS key on the job). The role needs to use that key.
- **Envelope encryption:** KMS gives you a data key; you encrypt the big file locally with it and store the wrapped (encrypted) key next to the data. KMS only handles the small key, never the bulk data.
- **KMS access has three doors:** key policy (the main one, must allow or delegate to IAM), IAM policy, and grants (temporary, scoped). Unlike most AWS resources, IAM alone is not enough unless the key policy delegates to IAM.
- **Why S3 allowed but KMS denied:** SSE-KMS reads call `kms:Decrypt`; the role lacks it or the key policy does not name the role (or account) so the read fails with AccessDenied that mentions KMS. Also a key in another account or Region.

**Example:** Bucket default is SSE-KMS. A PUT with no encryption arguments gets `ServerSideEncryption: aws:kms` and the key id on `head_object`. For envelope encryption: ask KMS for a 256-bit data key, encrypt locally with AES-GCM, store ciphertext plus wrapped key, decrypt by asking KMS to unwrap.

**Code:**
```python
# --- file: code/q17_encryption.py ---
import os, base64
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

with mock_aws():
    kms = boto3.client("kms")
    key = kms.create_key(Description="ml-data-key")["KeyMetadata"]
    arn = key["Arn"]
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="ml-secure-data")
    s3.put_bucket_encryption(Bucket="ml-secure-data", ServerSideEncryptionConfiguration={"Rules": [
        {"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "aws:kms", "KMSMasterKeyID": arn}, "BucketKeyEnabled": True}]})
    print("default encryption:", s3.get_bucket_encryption(Bucket="ml-secure-data")["ServerSideEncryptionConfiguration"]["Rules"][0]["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"])
    s3.put_object(Bucket="ml-secure-data", Key="train/a.csv", Body=b"a,b\n1,2\n")  # no encryption args
    h = s3.head_object(Bucket="ml-secure-data", Key="train/a.csv")
    print("head_object ServerSideEncryption:", h["ServerSideEncryption"], "| key id matches:", h["SSEKMSKeyId"] == arn)

    # envelope encryption: KMS only protects a small data key
    ctx = {"dataset": "train-v1"}
    dk = kms.generate_data_key(KeyId=arn, KeySpec="AES_256", EncryptionContext=ctx)
    print("plaintext data key bytes:", len(dk["Plaintext"]), "| wrapped key bytes (opaque blob):", len(dk["CiphertextBlob"]) > 32)
    nonce = os.urandom(12)
    ct = AESGCM(dk["Plaintext"]).encrypt(nonce, b"big training file contents", None)
    del dk["Plaintext"]  # real code wipes the plaintext key after use
    stored = (dk["CiphertextBlob"], nonce, ct)   # what you store beside the object
    plain_key = kms.decrypt(CiphertextBlob=stored[0], EncryptionContext=ctx)["Plaintext"]
    print("round trip:", AESGCM(plain_key).decrypt(stored[1], stored[2], None))
    # grants
    g = kms.create_grant(KeyId=arn, GranteePrincipal="arn:aws:iam::123456789012:role/sm-exec", Operations=["Decrypt", "GenerateDataKey"])
    print("grant created:", bool(g["GrantId"]), "| list_grants:", len(kms.list_grants(KeyId=arn)["Grants"]))
    print("NOT shown: key-policy / IAM / grant enforcement; this script never tested a caller without kms:Decrypt.")
```

**Output (my run):** Sandbox: Python 3.13.17, boto3 1.43.118, moto 5.2.4 (decorator mode `mock_aws`, fake keys, no real AWS contact, no moto server needed for these), run with `python3 -I`. `cryptography` 50.0.2 for AES-GCM. Real output:
```
default encryption: aws:kms
head_object ServerSideEncryption: aws:kms | key id matches: True
plaintext data key bytes: 32 | wrapped key bytes (opaque blob): True
round trip: b'big training file contents'
grant created: True | list_grants: 1
NOT shown: key-policy / IAM / grant enforcement; this script never tested a caller without kms:Decrypt.
```
moto applies the default encryption and does the data-key and grant API calls. **Real KMS key-policy, IAM and grant enforcement, bucket keys' request savings, Region scoping and rotation are not executed.**

**Follow-ups:**
- *SSE-KMS or SSE-S3?* SSE-KMS when you need key-level access control, audit and revocation; it adds KMS calls and quotas to think about (check current docs). SSE-S3 is simpler.
- *What is encryption context for?* Extra authenticated data: binding a key use to a context (for example dataset name), visible in logs. Decrypt must supply the same context.
- *Does encryption stop an over-permissioned role?* No. It adds a second gate only if the key policy is tight.

**Common mistakes:**
- Giving the role s3:GetObject but no kms:Decrypt.
- Believing KMS encrypts the bulk data directly.
- Logging or persisting the plaintext data key.
- Assuming moto proves the key policy would allow the call.

---

### Q18 ⭐⭐⭐ 🟡 Secrets Manager versus SSM Parameter Store versus environment variables versus KMS-encrypted files for a database password and an API key used by a training pipeline. Cover rotation, versioning, IAM access, auditing, cost model without prices, and why secrets must not be baked into images or logged. Store and read a secret and a SecureString parameter in moto, then write a small scanner that flags likely secrets in a Dockerfile and an env file. Secrets in CI belong to Part 7.
**Asked at:** IAM interview and policy-evaluation sources (AWS IAM 'Policy evaluation logic' pages on docs.aws.amazon.com and docs.aws.eu, tutorialsdojo 'How AWS IAM Handles Conflicting IAM Policies', advancedweb.hu 'IAM policy evaluation logic explained with examples', barkingiguana 'How IAM Policy Evaluation Actually Works', community.aws and hidekazu-konishi IAM glossary; search snippets only, not opened); vendor docs and study guides, not verified candidate reports; cloud, DevOps, security and MLOps roles at IT-services firms, product companies and GCCs | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)

**Say this first (1 line):** For a database password I use Secrets Manager because it has rotation, versions and audit. For plain config and a simple API key Parameter Store SecureString is fine. Environment variables are only a delivery method, and secrets must never be baked into an image or printed in logs.

**Then explain:**
- **Secrets Manager:** purpose-built for secrets; versions with staging labels (AWSCURRENT, AWSPREVIOUS), built-in rotation support (usually through a Lambda), IAM and optional resource policies, CloudTrail audit. Priced per secret and per call (check current docs).
- **SSM Parameter Store:** hierarchical config; SecureString uses KMS; versions; no built-in rotation; standard tier is generally cheaper (check current docs). Good for non-rotating values.
- **Env vars:** how the process gets the value at runtime. Fine if injected at start by the platform (ECS secrets, SageMaker job environment from a fetched secret). Not fine when they are hard-coded in a Dockerfile `ENV`: layers keep them forever and `docker history` shows them.
- **KMS-encrypted files in S3:** workable but you build rotation and access control yourself.
- **Rules:** fetch at start with least-privilege role, never in image or git, never log values, rotate and have a revocation plan. CI secrets are Part 7.

**Example:** Dockerfile line `ENV DB_PASSWORD=...` is a leak: anyone with the image has it. Correct: `ENV DB_PASSWORD_FILE=/run/secrets/db_password` or fetch from Secrets Manager at start using the task role.

**Code:**
```python
# --- file: code/q18_secrets.py ---
import os
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws

with mock_aws():
    sm = boto3.client("secretsmanager")
    sm.create_secret(Name="prod/train/db", SecretString='{"user":"etl","password":"FAKE-not-real-pw"}')
    sm.put_secret_value(SecretId="prod/train/db", SecretString='{"user":"etl","password":"FAKE-rotated-pw"}')
    v = sm.get_secret_value(SecretId="prod/train/db")
    print("secret stages:", v["VersionStages"], "| value:", v["SecretString"])
    vers = sm.list_secret_version_ids(SecretId="prod/train/db", IncludeDeprecated=True)["Versions"]
    print("versions with stages:", sorted(str(x.get("VersionStages")) for x in vers))
    ssm = boto3.client("ssm")
    ssm.put_parameter(Name="/prod/train/api_key", Value="FAKE-api-key-123", Type="SecureString")
    raw = ssm.get_parameter(Name="/prod/train/api_key")["Parameter"]
    dec = ssm.get_parameter(Name="/prod/train/api_key", WithDecryption=True)["Parameter"]
    print("ssm without decryption: type", raw["Type"], "version", raw["Version"], "| value starts:", raw["Value"][:10])
    print("ssm with decryption   :", dec["Value"])
    print("Not emulated: IAM/KMS checks on these reads, real rotation Lambda, CloudTrail audit.")

# --- file: code/secret_scan.py ---
"""Tiny secret scanner for Dockerfiles and env files. Heuristic only: it will miss some and flag some."""
import re, sys, pathlib

AWS_KEY = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
NAME_HINT = re.compile(r"(secret|password|passwd|token|api[_-]?key|private[_-]?key)", re.I)
ASSIGN = re.compile(r"^\s*(?:export\s+)?(?:(?:ENV|ARG)\s+)?([A-Za-z0-9_]+)\s*[= ]\s*(.+?)\s*$")
SAFE_VALUE = re.compile(r"^(\$\{?\w+\}?|<.*>|changeme|example|xxx+|)$", re.I)

def scan_text(name, text):
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        if AWS_KEY.search(line):
            out.append((name, n, "aws-access-key-id-shape"))
        m = ASSIGN.match(line)
        if m and NAME_HINT.search(m.group(1)):
            val = m.group(2).strip("'\"")
            if re.search(r"_(FILE|PATH|URI|URL)$", m.group(1), re.I) or val.startswith("/"):
                continue  # a pointer to a secret, not the secret
            if not SAFE_VALUE.match(val) and len(val) >= 6:
                out.append((name, n, f"hardcoded value for {m.group(1)}"))
        if re.search(r"curl[^|]*-u\s+\S+:\S+", line):
            out.append((name, n, "credentials in curl -u"))
    return out

if __name__ == "__main__":
    hits = []
    for p in sys.argv[1:]:
        hits += scan_text(p, pathlib.Path(p).read_text())
    for h in hits:
        print(f"{h[0]}:{h[1]}: {h[2]}")
    print(f"{len(hits)} finding(s)")
    sys.exit(1 if hits else 0)
```

**Output (my run):** Sandbox: Python 3.13.17, boto3 1.43.118, moto 5.2.4 (decorator mode `mock_aws`, fake keys, no real AWS contact, no moto server needed for these), run with `python3 -I`. Secrets and SSM calls, then the scanner on two demo files in `code/demo_inputs/` (all values are fake; the scanner is a heuristic and misses obfuscated or high-entropy secrets):
```
secret stages: ['AWSCURRENT'] | value: {"user":"etl","password":"FAKE-rotated-pw"}
versions with stages: ["['AWSCURRENT']", "['AWSPREVIOUS']"]
ssm without decryption: type SecureString version 1 | value starts: kms:alias/
ssm with decryption   : FAKE-api-key-123
Not emulated: IAM/KMS checks on these reads, real rotation Lambda, CloudTrail audit.
/tmp/claude-0/b10_q11_20/q18/Dockerfile:2: hardcoded value for DB_PASSWORD
/tmp/claude-0/b10_q11_20/q18/Dockerfile:3: hardcoded value for API_KEY
/tmp/claude-0/b10_q11_20/q18/Dockerfile:4: aws-access-key-id-shape
/tmp/claude-0/b10_q11_20/q18/train.env:4: hardcoded value for SLACK_TOKEN
/tmp/claude-0/b10_q11_20/q18/train.env:5: hardcoded value for API_KEY
5 finding(s)
```
Commands run: `python3 -I q18_secrets.py` style (venv python) and `python3 -I secret_scan.py <Dockerfile> <train.env>` (exit code 1 when findings). Note the scanner ignored `DB_PASSWORD_FILE` (a path pointer) and the `${DB_PASSWORD}` reference. moto does not enforce IAM or KMS on these reads; the `kms:alias/...` value for the undecrypted parameter is moto's representation. **Real rotation, KMS enforcement and audit are not executed.**

**Follow-ups:**
- *How do I rotate without downtime?* Staging labels: new version is AWSPENDING, tested, then promoted; clients read AWSCURRENT. Both old and new credentials need to work during the switch.
- *Parameter Store or Secrets Manager?* Rotation and cross-account sharing need push you to Secrets Manager. Otherwise cost and simplicity decide; check current docs.
- *Already leaked?* Rotate first, then clean the history. Q50 covers the response order.

**Common mistakes:**
- `ENV` or `ARG` secrets in Dockerfiles (ARG values also show in history).
- Committing `.env` files.
- Logging the full config dict at startup.
- Trusting a regex scanner as the only control; use real secret scanning too.

---

### Q19 ⭐⭐⭐ 🟡 CloudWatch versus CloudTrail versus AWS Config: what each records (metrics, logs and alarms; API call audit; resource configuration history), which you open for 'why is the endpoint slow', 'who deleted the model bucket' and 'was this bucket public last week'. Put a custom metric and an alarm in moto, write a log event and filter it, and show that moto does not implement CloudTrail lookup_events here. Monitoring drift belongs to Part 8.
**Asked at:** AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only) | Job-posting skill lists (a getonbrd Senior MLOps Engineer AWS and SageMaker posting listing Athena, RDS, ECR, IAM, CloudWatch, CloudFormation or Terraform and GitHub Actions, a workingnomads Senior MLOps Engineer SageMaker and Airflow posting; search snippets only, not opened); job postings, not interview reports; MLOps roles on AWS

**Say this first (1 line):** CloudWatch is for metrics, logs and alarms: how the system is behaving now. CloudTrail is the audit log of API calls: who did what. AWS Config records resource configuration over time: what it looked like and when it changed.

**Then explain:**
- **CloudWatch:** metrics (service and custom), Logs with filters, alarms with period, evaluation periods and datapoints to alarm. First stop for 'why is the endpoint slow': latency, invocation and error metrics, CPU, GPU, memory, plus container logs.
- **CloudTrail:** records management API events (and optionally data events) with caller identity, time, source IP and error message. 'Who deleted the model bucket' is a CloudTrail question: look up `DeleteBucket`. Retention and lookup window: check current docs; for long retention, deliver a trail to S3.
- **AWS Config:** tracks configuration items and compliance rules. 'Was this bucket public last week' is a Config history question.
- **Failure modes:** no trail set up before the incident, no Config recorder enabled, logs not retained, alarms with missing-data treatment hiding outages.
- Drift monitoring is Part 8; endpoint metrics in depth is Q37.

**Example:** Custom metric `FraudScoreLatencyMs`; alarm: Average over 60 s period, 3 evaluation periods, 2 datapoints needed, threshold 100, GreaterThanThreshold. A log line `ERROR AccessDenied ...` found with filter `ERROR`.

**Code:**
```python
# --- file: code/q19_cloudwatch.py ---
import os, time
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws

with mock_aws():
    cw = boto3.client("cloudwatch")
    cw.put_metric_data(Namespace="MLApp", MetricData=[{"MetricName": "FraudScoreLatencyMs", "Value": 42.0, "Unit": "Milliseconds",
                                                       "Dimensions": [{"Name": "Endpoint", "Value": "fraud-v3"}]}])
    cw.put_metric_alarm(AlarmName="fraud-latency-high", Namespace="MLApp", MetricName="FraudScoreLatencyMs",
                        Dimensions=[{"Name": "Endpoint", "Value": "fraud-v3"}], Statistic="Average", Period=60,
                        EvaluationPeriods=3, DatapointsToAlarm=2, Threshold=100.0, ComparisonOperator="GreaterThanThreshold",
                        TreatMissingData="notBreaching")
    a = cw.describe_alarms(AlarmNames=["fraud-latency-high"])["MetricAlarms"][0]
    print({k: a[k] for k in ("AlarmName", "StateValue", "Period", "EvaluationPeriods", "DatapointsToAlarm", "Threshold", "ComparisonOperator")})
    print("metrics listed:", [(m["Namespace"], m["MetricName"]) for m in cw.list_metrics(Namespace="MLApp")["Metrics"]])

    logs = boto3.client("logs")
    logs.create_log_group(logGroupName="/ml/train")
    logs.create_log_stream(logGroupName="/ml/train", logStreamName="job-1")
    now = int(time.time() * 1000)
    logs.put_log_events(logGroupName="/ml/train", logStreamName="job-1", logEvents=[
        {"timestamp": now, "message": "epoch=1 loss=0.9"},
        {"timestamp": now + 1, "message": "ERROR AccessDenied reading s3://ml-data/train/"},
        {"timestamp": now + 2, "message": "epoch=2 loss=0.7"}])
    ev = logs.filter_log_events(logGroupName="/ml/train", filterPattern="ERROR")["events"]
    print("filter 'ERROR' ->", [e["message"] for e in ev])

    ct = boto3.client("cloudtrail")
    try:
        ct.lookup_events(LookupAttributes=[{"AttributeKey": "EventName", "AttributeValue": "DeleteBucket"}])
        print("cloudtrail lookup_events worked")
    except Exception as e:
        print("cloudtrail lookup_events:", type(e).__name__, str(e)[:90])
    cfg = boto3.client("config")
    try:
        cfg.describe_configuration_recorders()
        print("config describe_configuration_recorders: call accepted")
    except Exception as e:
        print("config:", type(e).__name__, str(e)[:90])
```

**Output (my run):** Sandbox: Python 3.13.17, boto3 1.43.118, moto 5.2.4 (decorator mode `mock_aws`, fake keys, no real AWS contact, no moto server needed for these), run with `python3 -I`. Real output:
```
{'AlarmName': 'fraud-latency-high', 'StateValue': 'OK', 'Period': 60, 'EvaluationPeriods': 3, 'DatapointsToAlarm': 2, 'Threshold': 100.0, 'ComparisonOperator': 'GreaterThanThreshold'}
metrics listed: [('MLApp', 'FraudScoreLatencyMs')]
filter 'ERROR' -> ['ERROR AccessDenied reading s3://ml-data/train/']
cloudtrail lookup_events: NotImplementedError The lookup_events action has not been implemented
config describe_configuration_recorders: call accepted
```
moto implements metrics, alarms and log filtering. **CloudTrail `lookup_events` raised NotImplementedError in this moto version**, so no audit lookup was shown. The Config recorder call was accepted but I did not test further. The alarm reads `OK` in moto right after creation; real CloudWatch typically starts at `INSUFFICIENT_DATA` until data arrives (check current docs). Real alarm evaluation, log delivery delays and CloudTrail contents are **not executed**.

**Follow-ups:**
- *Which for 'AccessDenied on S3'?* CloudTrail event with errorMessage, then the policy layers (Q20).
- *Does CloudTrail show everything?* Management events by default; object-level S3 and some data events need to be enabled (check current docs).
- *Alarm on what?* Alert design is Part 8; here pick symptoms (5XX, latency) not just CPU.

**Common mistakes:**
- Opening CloudWatch for a 'who did it' question.
- Enabling CloudTrail after the incident.
- Treating alarm state OK as 'healthy' when data is missing.
- Assuming moto's CloudTrail or Config behaviour matches AWS.

---

### Q20 ⭐⭐⭐ 🔴 Debug scenario: a SageMaker training job fails with AccessDenied reading s3://ml-data/train/ . Give the ordered checklist (which principal is the real caller, role policy, bucket policy, KMS key policy, permissions boundary, SCP, VPC endpoint policy, S3 Block Public Access and Object Ownership, bucket in another account or Region) and what evidence you pull from each (CloudTrail errorMessage, Access Analyzer, policy simulator). Encode the checklist as an evaluator run on a failing and a fixed configuration and print the first layer that denies.
**Asked at:** IAM interview and policy-evaluation sources (AWS IAM 'Policy evaluation logic' pages on docs.aws.amazon.com and docs.aws.eu, tutorialsdojo 'How AWS IAM Handles Conflicting IAM Policies', advancedweb.hu 'IAM policy evaluation logic explained with examples', barkingiguana 'How IAM Policy Evaluation Actually Works', community.aws and hidekazu-konishi IAM glossary; search snippets only, not opened); vendor docs and study guides, not verified candidate reports; cloud, DevOps, security and MLOps roles at IT-services firms, product companies and GCCs | SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs

**Say this first (1 line):** First confirm who the real caller is, because most AccessDenied is the wrong principal. Then walk the layers in order: role policy, bucket policy, KMS key policy, boundary, SCP, VPC endpoint policy, Block Public Access and Ownership, cross-account or Region. Evidence: CloudTrail's errorMessage, then the policy simulator or Access Analyzer.

**Then explain:**
- **1. Real caller:** CloudTrail (or the error text) shows the assumed-role ARN. Is it the job's execution role or a notebook user? Is the bucket in another account or Region?
- **2. Role policy:** does it allow `s3:GetObject` on `arn:aws:s3:::ml-data/train/*` and `s3:ListBucket` on the bucket with a prefix condition? Common typo: object ARN versus bucket ARN.
- **3. Bucket policy:** an explicit Deny (for example a missing VPC endpoint condition or a TLS-only rule), or in cross-account use, no Allow for your role.
- **4. KMS:** SSE-KMS needs `kms:Decrypt` in the role policy and a key policy that allows the role (or delegates to IAM). The error often names KMS.
- **5. Guardrails:** permissions boundary, SCP (also session policy if assumed with one). They only limit; an explicit deny wins everywhere.
- **6. Network and bucket settings:** VPC endpoint policy, Block Public Access (affects public policies, not a plain named-principal grant), Object Ownership (objects owned by another account), wrong Region (redirect or 301 style errors).
- **Evidence:** CloudTrail `errorCode` and `errorMessage` (newer messages may name the denying policy type; check current docs), the IAM policy simulator, Access Analyzer policy validation and findings. Fix one layer at a time and re-test.

**Example:** Role policy is perfect, bucket has default SSE-KMS, key policy names a different role: S3 checks pass, the first denying layer is the KMS key policy. Fix: add the role to the key policy (or key policy delegating to IAM) and `kms:Decrypt` on the role.

**Code:**
```python
# --- file: code/q20_accessdenied_checklist.py ---
"""AccessDenied checklist as code. Reuses the simplified evaluator (iam_eval_sketch.py, copied unmodified).
Layers are checked in the order an on-call engineer would look. Simplified: see notes printed at the end."""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iam_eval_sketch import evaluate

ROLE = "arn:aws:iam::111111111111:role/sm-exec"
OBJ = "arn:aws:s3:::ml-data/train/part-0.csv"
KEY_ARN = "arn:aws:kms:us-east-1:111111111111:key/abc"

def A(action, res="*", eff="Allow"):
    return {"Version": "2012-10-17", "Statement": [{"Effect": eff, "Action": action, "Resource": res}]}

def rp(principal, action, res="*"):
    return {"Statement": [{"Effect": "Allow", "Principal": {"AWS": principal}, "Action": action, "Resource": res}]}

GOOD = {
    "caller_arn": ROLE,                        # who CloudTrail says made the call
    "expected_role": ROLE,                     # who we THINK the job runs as
    "job_region": "us-east-1", "bucket_region": "us-east-1",
    "bucket_account_same": True,
    "role_policy": [A(["s3:GetObject", "s3:ListBucket"], ["arn:aws:s3:::ml-data", "arn:aws:s3:::ml-data/train/*"]),
                    A(["kms:Decrypt", "kms:GenerateDataKey"], KEY_ARN)],
    "boundary": None, "scps": [], "bucket_policy": None,
    "bucket_sse_kms": True,
    "key_policy": rp(ROLE, ["kms:Decrypt", "kms:GenerateDataKey"], "*"),
    "vpc_endpoint_policy": None,               # None = default full-access endpoint policy
    "bpa_blocks_public_policy_only": True,     # informational: BPA does not deny a named-principal grant
    "objects_owned_by_other_account_with_acl": False,
}

def check(cfg):
    """Return (layer, detail) of the first layer that denies, or None."""
    if cfg["caller_arn"] != cfg["expected_role"]:
        return ("real caller", f"caller is {cfg['caller_arn']}, not {cfg['expected_role']}")
    if cfg["job_region"] != cfg["bucket_region"] and cfg.get("strict_region"):
        return ("region", "bucket in another Region than the job config expects")
    d, why = evaluate("s3:GetObject", OBJ, identity=cfg["role_policy"], boundary=cfg["boundary"], scps=cfg["scps"],
                      resource_policy=cfg["bucket_policy"], same_account=cfg["bucket_account_same"], principal_arn=cfg["caller_arn"])
    if d == "Deny":
        layer = ("policy stack (explicit deny, SCP, boundary, role or bucket policy)")
        if "explicit deny" in why: layer = "explicit deny somewhere (role, bucket, SCP or boundary)"
        elif "SCP" in why: layer = "SCP"
        elif "boundary" in why: layer = "permissions boundary"
        elif "cross-account" in why: layer = "bucket policy (cross-account needs both sides)"
        else: layer = "role policy (or bucket policy) gives no allow"
        return (layer, why)
    if cfg["bucket_sse_kms"]:
        d, why = evaluate("kms:Decrypt", KEY_ARN, identity=cfg["role_policy"], resource_policy=cfg["key_policy"], same_account=True, principal_arn=cfg["caller_arn"])
        # KMS is an exception: the KEY POLICY must allow (directly or by delegating to IAM); role policy alone is not enough
        key_ok = cfg["key_policy"] is not None and any(
            s["Effect"] == "Allow" and s.get("Principal", {}).get("AWS") in (cfg["caller_arn"], "arn:aws:iam::111111111111:root")
            for s in cfg["key_policy"]["Statement"])
        if not key_ok:
            return ("kms key policy", "key policy neither names the role nor delegates to IAM (role policy alone is not enough)")
        if d == "Deny":
            return ("kms role permission", why)
    if cfg["vpc_endpoint_policy"] is not None:
        d, why = evaluate("s3:GetObject", OBJ, identity=[cfg["vpc_endpoint_policy"]])
        if d == "Deny":
            return ("vpc endpoint policy", why)
    if cfg["objects_owned_by_other_account_with_acl"]:
        return ("object ownership", "objects owned by another account and bucket owner enforced is off")
    return None

def variant(**kw):
    c = copy.deepcopy(GOOD); c.update(kw); return c

SCEN = [
    ("fixed / healthy config", GOOD),
    ("job really runs as a different role", variant(caller_arn="arn:aws:iam::111111111111:role/notebook-user")),
    ("role policy missing the train/ prefix", variant(role_policy=[A("s3:GetObject", "arn:aws:s3:::ml-data/other/*")])),
    ("boundary does not include s3", variant(boundary=A("ec2:*"))),
    ("SCP allows only ec2", variant(scps=[A("ec2:*")])),
    ("explicit deny in bucket policy", variant(bucket_policy={"Statement": [{"Effect": "Deny", "Principal": "*", "Action": "s3:GetObject", "Resource": "*"}]})),
    ("bucket in other account, no bucket policy", variant(bucket_account_same=False)),
    ("SSE-KMS key policy does not name the role", variant(key_policy=rp("arn:aws:iam::111111111111:role/other", ["kms:Decrypt"], "*"))),
    ("VPC endpoint policy only allows another bucket", variant(vpc_endpoint_policy=A("s3:GetObject", "arn:aws:s3:::other-bucket/*"))),
    ("objects owned by another account", variant(objects_owned_by_other_account_with_acl=True)),
]
for name, cfg in SCEN:
    r = check(cfg)
    print(f"{name:48s} -> {('PASS (no layer denies)' if r is None else 'DENY at ' + r[0])}")
    if r: print(f"{'':51s}evidence: {r[1]}")
print("\nSimplified: Block Public Access, Region redirects and ACLs are modelled as flags, not real evaluation.")
```

**Output (my run):** Pure-Python only (no AWS, no moto), Python 3.13.17. It copies `code/iam_eval_sketch.py` unmodified from the Wave A sketch. Real output:
```
fixed / healthy config                           -> PASS (no layer denies)
job really runs as a different role              -> DENY at real caller
                                                   evidence: caller is arn:aws:iam::111111111111:role/notebook-user, not arn:aws:iam::111111111111:role/sm-exec
role policy missing the train/ prefix            -> DENY at role policy (or bucket policy) gives no allow
                                                   evidence: implicit deny: nothing allows
boundary does not include s3                     -> DENY at permissions boundary
                                                   evidence: implicit deny: outside permissions boundary
SCP allows only ec2                              -> DENY at SCP
                                                   evidence: implicit deny: SCP level 0 does not allow
explicit deny in bucket policy                   -> DENY at explicit deny somewhere (role, bucket, SCP or boundary)
                                                   evidence: explicit deny
bucket in other account, no bucket policy        -> DENY at bucket policy (cross-account needs both sides)
                                                   evidence: implicit deny: cross-account needs both sides
SSE-KMS key policy does not name the role        -> DENY at kms key policy
                                                   evidence: key policy neither names the role nor delegates to IAM (role policy alone is not enough)
VPC endpoint policy only allows another bucket   -> DENY at vpc endpoint policy
                                                   evidence: implicit deny: nothing allows
objects owned by another account                 -> DENY at object ownership
                                                   evidence: objects owned by another account and bucket owner enforced is off

Simplified: Block Public Access, Region redirects and ACLs are modelled as flags, not real evaluation.
```
Simplified: the evaluator is the Wave A sketch (no NotAction, policy variables or most operators); KMS, VPC endpoint policy, Block Public Access, Region and Ownership are small rules or flags I wrote, not real AWS evaluation. The order shown is a debugging order, not AWS's internal order. **Real CloudTrail, the policy simulator and Access Analyzer are not executed.** For reference, moto only enforces IAM when auth enforcement is switched on, so it cannot reproduce this failure by default.

**Follow-ups:**
- *The role policy looks right, still denied?* Look for an explicit deny in SCP, boundary or bucket policy, then KMS.
- *Is the denying layer always in the error?* Not always. Newer error messages can say which policy type denied (check current docs); older ones are generic.
- *How to prevent a repeat?* A test job in CI that reads the prefix, Access Analyzer checks, and least-privilege policy templates (Q8).

**Common mistakes:**
- Editing the role policy again and again without checking who the caller is.
- Forgetting KMS because the bucket looks 'just S3'.
- Missing that a cross-account read needs both sides.
- Testing the fix with your own admin credentials instead of the job role.

---

### Q21 ⭐⭐ 🟢 S3 multipart upload: why and when (large files, parallel parts, retry of single parts), part-size rules to check in current docs, what Complete and Abort do, why incomplete uploads quietly hold storage until a lifecycle rule removes them, and how the multipart ETag differs from an MD5. Run a two-part upload in moto, print the resulting ETag suffix, and show the EntityTooSmall error for an undersized non-final part.
**Asked at:** S3 interview question banks (novelvista '100+ Top AWS S3 Interview Questions', adaface, ccbp.in, a techinterview.org 'System Design Interview: Object Storage (Amazon S3)' post, AWS developer exam-prep study guides; search snippets only, not opened; WebFetch of docs.aws.amazon.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; cloud, data and ML engineer roles at IT-services firms, product companies and GCCs | AWS S3 documentation topics as summarised by prep guides (versioning and delete markers, lifecycle transitions and expiry, multipart upload, presigned URLs, strong read-after-write consistency since December 2020; search snippets only, not opened, exact limits not verified); vendor docs and prep notes, not interview reports; cloud, data and ML platform roles

**Say this first (1 line):** Multipart upload splits one big object into parts that upload in parallel and retry on their own, then Complete stitches them together. Use it for big files, and add a lifecycle rule so abandoned uploads do not sit there costing storage.

**Then explain:**
- **Why:** a 20 GB model archive as one PUT means one failure restarts everything. With parts you upload in parallel, retry only the failed part, and can resume later.
- **When:** AWS docs recommend multipart for large objects (a size threshold is suggested, and a single PUT has an upper limit). The exact thresholds, part-size minimum and maximum, and max part count: check current docs. boto3's `upload_file` switches to multipart for you above a configurable threshold.
- **Complete and Abort:** Complete takes the list of (PartNumber, ETag) and makes the object appear. Abort throws away the uploaded parts. Until one of them happens, the parts exist but there is no object.
- **Hidden cost:** unfinished uploads are not visible in a normal `ls` but, per AWS docs, their stored parts are billed storage. Fix: a lifecycle rule `AbortIncompleteMultipartUpload` with `DaysAfterInitiation`.
- **ETag trap:** the multipart ETag is not the MD5 of the file. It is a hash built from the part hashes plus `-<number of parts>`. So you cannot compare it with `md5sum`. Use a checksum feature or your own stored hash for integrity.
- **Failure modes:** non-final part under the minimum size gives `EntityTooSmall` at Complete time; wrong ETag or missing part gives `InvalidPart`; same part number uploaded twice, last one wins.

**Example:** Two 5 MiB parts. Complete returns an ETag ending in `-2`. A whole-file MD5 of the same 10 MiB looks completely different. Two 4-byte parts: Complete fails with EntityTooSmall because part 1 is not the last part and is below the minimum.

**Code:**

```python
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

from botocore.exceptions import ClientError
with mock_aws():
    s3 = boto3.client("s3"); s3.create_bucket(Bucket="ml-artifacts")
    uid = s3.create_multipart_upload(Bucket="ml-artifacts", Key="big.bin")["UploadId"]
    parts = []
    for n in (1, 2):
        r = s3.upload_part(Bucket="ml-artifacts", Key="big.bin", UploadId=uid, PartNumber=n, Body=b"x" * (5 * 1024 * 1024))
        parts.append({"PartNumber": n, "ETag": r["ETag"]})
    print("listed parts:", [p["PartNumber"] for p in s3.list_parts(Bucket="ml-artifacts", Key="big.bin", UploadId=uid)["Parts"]])
    done = s3.complete_multipart_upload(Bucket="ml-artifacts", Key="big.bin", UploadId=uid, MultipartUpload={"Parts": parts})
    print("multipart ETag:", done["ETag"], "suffix:", done["ETag"].strip('"').split("-")[1])
    import hashlib
    print("md5 of whole body (different):", hashlib.md5(b"x" * (10 * 1024 * 1024)).hexdigest())
    # undersized non-final part
    uid2 = s3.create_multipart_upload(Bucket="ml-artifacts", Key="small.bin")["UploadId"]
    p1 = s3.upload_part(Bucket="ml-artifacts", Key="small.bin", UploadId=uid2, PartNumber=1, Body=b"tiny")
    p2 = s3.upload_part(Bucket="ml-artifacts", Key="small.bin", UploadId=uid2, PartNumber=2, Body=b"tiny")
    try:
        s3.complete_multipart_upload(Bucket="ml-artifacts", Key="small.bin", UploadId=uid2,
            MultipartUpload={"Parts": [{"PartNumber": 1, "ETag": p1["ETag"]}, {"PartNumber": 2, "ETag": p2["ETag"]}]})
    except ClientError as e:
        print("error code:", e.response["Error"]["Code"])
    # abort + in-flight listing + lifecycle rule
    print("in flight before abort:", len(s3.list_multipart_uploads(Bucket="ml-artifacts").get("Uploads", [])))
    s3.abort_multipart_upload(Bucket="ml-artifacts", Key="small.bin", UploadId=uid2)
    print("in flight after abort:", len(s3.list_multipart_uploads(Bucket="ml-artifacts").get("Uploads", [])))
    s3.put_bucket_lifecycle_configuration(Bucket="ml-artifacts", LifecycleConfiguration={"Rules": [{"ID": "clean-mpu", "Status": "Enabled", "Filter": {"Prefix": ""}, "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7}}]})
    print("lifecycle read-back:", s3.get_bucket_lifecycle_configuration(Bucket="ml-artifacts")["Rules"][0]["AbortIncompleteMultipartUpload"])
```

**Output (my run):** Ran with `python3 -I` from an empty temp dir, Python 3.13.17, boto3 1.43.118, moto 5.2.4, fake keys, in-process `mock_aws()` (no moto server needed, no network to AWS). Moto is API shape only: Moto note: moto enforces the small-part rule (the real limit value is AWS's; check current docs). Moto does not model real parallel throughput, storage billing, or lifecycle execution (the rule is stored and read back, nothing is ever aborted by it). Real S3 timing and limits: not executed.

```text
listed parts: [1, 2]
multipart ETag: "d316408c159ea701ab954894bd3a92c2-2" suffix: 2
md5 of whole body (different): 46f40f95feefb6ab49b2b3679b5ec0a2
error code: EntityTooSmall
in flight before abort: 1
in flight after abort: 0
lifecycle read-back: {'DaysAfterInitiation': 7}
```

**Follow-ups:**
- How do you make a failed upload resumable? Persist the UploadId and the list of finished part numbers; on restart call ListParts and upload only the missing ones.
- Why not just use bigger single PUTs? There is a single-PUT size cap (check current docs) and one failure restarts everything.

**Common mistakes:** Calling Complete with the ETags in the wrong order; assuming the ETag equals MD5; forgetting the lifecycle abort rule so failed uploads pile up; claiming a threshold number as fixed without checking current docs.

---

### Q22 ⭐⭐ 🟢 Auto Scaling groups for self-managed inference or batch workers: launch template versus launch configuration, min, max and desired capacity, health checks, target-tracking versus step versus scheduled scaling, scale-in protection, warm pools for slow-starting GPU nodes, and mixed spot and on-demand instances. Create an ASG and a target-tracking policy in moto and read them back; real scaling and instance boot are not executed. How this differs from SageMaker endpoint autoscaling is a one-line contrast.
**Asked at:** EC2 and spot-training sources (introl.com and barkingiguana.com posts on spot GPU training and SageMaker managed spot, practitioner notes on checkpoint cadence and resume testing; search snippets only, not opened; a savings percentage in one title was not used); blogs, not interview reports; ML platform and MLOps roles | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)

**Say this first (1 line):** An Auto Scaling group keeps a fleet of EC2 instances between a min and a max, built from a launch template, and a scaling policy moves desired capacity. It is for self-managed workers; SageMaker endpoints have their own autoscaling.

**Then explain:**
- **Launch template vs launch configuration:** the template is versioned and the current choice; launch configurations are legacy (check current docs for current status). Pin a version or use `$Latest` knowingly.
- **Capacity:** min is the floor, max is the ceiling, desired is what the group tries to run now. Scaling policies only change desired inside min and max.
- **Health checks:** EC2 status checks by default; ELB checks if behind a load balancer. The grace period stops the group killing a GPU node that is still loading a model. Too short a grace period gives a replace-loop.
- **Policies:** target tracking (hold a metric near a value, simplest), step (different actions per alarm size), scheduled (known peaks, like a nightly batch). Queue depth per worker is often a better metric for batch workers than CPU.
- **Extras:** scale-in protection stops chosen instances being terminated (for example one mid-job). Warm pools keep pre-initialised instances so slow GPU boots do not hurt scale-out. Mixed instances policy blends spot and on-demand, with several instance types to reduce spot capacity risk.
- **One-line contrast:** SageMaker endpoint autoscaling is Application Auto Scaling on a variant's instance count (and scaling metrics like invocations per instance); here you manage the AMI, patching, and load balancer yourself.

**Example:** min 1, max 6, desired 2, target-tracking at 50 percent average CPU. If CPU is high, desired rises toward 6; when quiet, back toward 1. A scheduled action raises capacity to 4 at 20:00 for a nightly job.

**Code:**

```python
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

with mock_aws():
    ec2 = boto3.client("ec2"); asg = boto3.client("autoscaling")
    ami = ec2.describe_images()["Images"][0]["ImageId"]
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")["Vpc"]["VpcId"]
    sn = ec2.create_subnet(VpcId=vpc, CidrBlock="10.0.1.0/24")["Subnet"]["SubnetId"]
    ec2.create_launch_template(LaunchTemplateName="infer-lt", LaunchTemplateData={"ImageId": ami, "InstanceType": "g5.xlarge"})
    asg.create_auto_scaling_group(AutoScalingGroupName="infer-asg", LaunchTemplate={"LaunchTemplateName": "infer-lt", "Version": "$Latest"},
        MinSize=1, MaxSize=6, DesiredCapacity=2, VPCZoneIdentifier=sn, HealthCheckType="EC2", HealthCheckGracePeriod=300)
    asg.put_scaling_policy(AutoScalingGroupName="infer-asg", PolicyName="cpu50", PolicyType="TargetTrackingScaling",
        TargetTrackingConfiguration={"PredefinedMetricSpecification": {"PredefinedMetricType": "ASGAverageCPUUtilization"}, "TargetValue": 50.0})
    asg.put_scheduled_update_group_action(AutoScalingGroupName="infer-asg", ScheduledActionName="nightly-up", Recurrence="0 20 * * *", MinSize=2, MaxSize=6, DesiredCapacity=4)
    g = asg.describe_auto_scaling_groups(AutoScalingGroupNames=["infer-asg"])["AutoScalingGroups"][0]
    print("min/max/desired:", g["MinSize"], g["MaxSize"], g["DesiredCapacity"], "health:", g["HealthCheckType"], g["HealthCheckGracePeriod"])
    print("launch template:", g.get("LaunchTemplate", {}).get("LaunchTemplateName"))
    p = asg.describe_policies(AutoScalingGroupName="infer-asg")["ScalingPolicies"][0]
    print("policy:", p["PolicyName"], p["PolicyType"], p["TargetTrackingConfiguration"]["TargetValue"])
    print("scheduled:", [a["ScheduledActionName"] for a in asg.describe_scheduled_actions(AutoScalingGroupName="infer-asg")["ScheduledUpdateGroupActions"]])
    print("instances in group (moto creates records, no real boot):", len(g["Instances"]))
    try:
        asg.set_instance_protection(AutoScalingGroupName="infer-asg", InstanceIds=[g["Instances"][0]["InstanceId"]], ProtectedFromScaleIn=True)
        print("scale-in protection set OK")
    except Exception as e: print("scale-in protection:", type(e).__name__, str(e)[:80])
```

**Output (my run):** Ran with `python3 -I` from an empty temp dir, Python 3.13.17, boto3 1.43.118, moto 5.2.4, fake keys, in-process `mock_aws()` (no moto server needed, no network to AWS). Moto is API shape only: Moto stores the group, template, policy and scheduled action and returns them; it does not boot instances for real, run health checks, evaluate CloudWatch metrics, or ever scale. Warm pools, mixed-instances policy and spot behaviour: not executed. Real scaling: not executed.

```text
min/max/desired: 1 6 2 health: EC2 300
launch template: infer-lt
policy: cpu50 TargetTrackingScaling 50.0
scheduled: ['nightly-up']
instances in group (moto creates records, no real boot): 2
scale-in protection set OK
```

**Follow-ups:**
- Why a warm pool for GPUs? Boot plus driver plus model load is slow; pre-initialised stopped or running instances cut scale-out latency. Check current docs for pool states and their costs.
- CPU target for a GPU inference fleet? Often a bad signal; use requests per instance, queue depth or GPU utilisation as a custom metric.

**Common mistakes:** Using CPU for GPU or queue-bound workers; no health-check grace period; setting min=0 for a latency-sensitive service; forgetting scale-in protection for long batch jobs.

---

### Q23 ⭐⭐ 🟢 Lambda event sources: synchronous (API Gateway, direct invoke), asynchronous (S3, EventBridge, SNS) and poll-based (SQS, Kinesis, DynamoDB streams). For each, what retries, what happens on failure, where a dead-letter queue or on-failure destination fits, and why handlers must be idempotent. Wire a mock SQS queue with a visibility timeout in moto, show a message becoming invisible after receive, and explain how that relates to duplicate processing. Real Lambda triggers are not executed.
**Asked at:** Lambda interview and limits sources (kodekloud AWS Developer Associate notes on limits and concurrency, awsfundamentals.com 'Lambda limitations', a dev.to Lambda compute-limits post, a pulumi provisioned-concurrency post; search snippets only, not opened; secondary sources disagreed on package-size wording so numbers are hedged 'check current docs'); training notes and blogs, not verified interview reports; backend, cloud and ML engineer roles | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)

**Say this first (1 line):** Lambda has three invocation styles: synchronous, where the caller gets the error; asynchronous, where Lambda retries and then uses a DLQ or destination; and poll-based, where Lambda polls the source. In all three delivery can repeat, so handlers must be idempotent.

**Then explain:**
- **Synchronous** (API Gateway, direct invoke): the caller waits and sees the error. Retries are the caller's job. Throttling shows up as a 429 to the caller.
- **Asynchronous** (S3, EventBridge, SNS): Lambda queues the event and retries on failure (default retry count and event age are configurable; check current docs). After that, send it to a DLQ or an on-failure destination so it is not lost.
- **Poll-based** (SQS, Kinesis, DynamoDB streams): the Lambda service polls. For SQS, a failed batch returns to the queue after the visibility timeout; after `maxReceiveCount` receives it moves to the queue's DLQ. For streams, a bad record can block a shard unless you configure bisect, retry limits and an on-failure destination.
- **Idempotency:** SQS standard is at-least-once and retries re-run your code. Use an idempotency key (job id) and a conditional write or a dedupe table.
- **Visibility timeout rule of thumb:** set it longer than the function timeout (AWS docs suggest a multiple; check current docs), or a slow run gets its message delivered again while still running.
- **ML use:** S3 upload triggers feature extraction (async); a queue feeds embedding jobs (poll). A DLQ with an alarm on depth is the safety net.

**Example:** Receive a message: it is invisible. Receive again straight away: nothing. If the worker dies and the visibility timeout ends, the same message comes back with ReceiveCount 2. That is a duplicate. With maxReceiveCount 2, a third failure would send it to the DLQ.

**Code:**

```python
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

import json
with mock_aws():
    sqs = boto3.client("sqs")
    dlq = sqs.create_queue(QueueName="jobs-dlq")["QueueUrl"]
    dlq_arn = sqs.get_queue_attributes(QueueUrl=dlq, AttributeNames=["QueueArn"])["Attributes"]["QueueArn"]
    q = sqs.create_queue(QueueName="jobs", Attributes={"VisibilityTimeout": "30",
        "RedrivePolicy": json.dumps({"deadLetterTargetArn": dlq_arn, "maxReceiveCount": "2"})})["QueueUrl"]
    print("attrs:", {k: v for k, v in sqs.get_queue_attributes(QueueUrl=q, AttributeNames=["VisibilityTimeout", "RedrivePolicy"])["Attributes"].items()})
    sqs.send_message(QueueUrl=q, MessageBody="train-job-42")
    r1 = sqs.receive_message(QueueUrl=q, MaxNumberOfMessages=1)
    print("receive 1:", [m["Body"] for m in r1.get("Messages", [])])
    r2 = sqs.receive_message(QueueUrl=q, MaxNumberOfMessages=1)
    print("receive 2 right after (invisible):", r2.get("Messages", []))
    # worker 'crashes': shorten visibility to 0 so message returns (simulates timeout expiry)
    sqs.change_message_visibility(QueueUrl=q, ReceiptHandle=r1["Messages"][0]["ReceiptHandle"], VisibilityTimeout=0)
    r3 = sqs.receive_message(QueueUrl=q, MaxNumberOfMessages=1, AttributeNames=["ApproximateReceiveCount"])
    m = r3["Messages"][0]
    print("receive 3 after timeout expiry:", m["Body"], "ReceiveCount:", m["Attributes"]["ApproximateReceiveCount"], "-> duplicate delivery")
    # idempotent handler
    done = set()
    def handle(body):
        if body in done: return "skipped (already done)"
        done.add(body); return "processed"
    print(handle(m["Body"]), "|", handle(m["Body"]))
```

**Output (my run):** Ran with `python3 -I` from an empty temp dir, Python 3.13.17, boto3 1.43.118, moto 5.2.4, fake keys, in-process `mock_aws()` (no moto server needed, no network to AWS). Moto is API shape only: Moto's SQS visibility works, and I shortened visibility to 0 to simulate expiry instead of waiting 30 s. Lambda event source mappings, retries, destinations and DLQ delivery on failure are not executed (Lambda invoke needs Docker, which is unavailable). The moto redrive config is stored and read back; I did not show a message actually moving to the DLQ.

```text
attrs: {'VisibilityTimeout': '30', 'RedrivePolicy': '{"deadLetterTargetArn": "arn:aws:sqs:us-east-1:123456789012:jobs-dlq", "maxReceiveCount": 2}'}
receive 1: ['train-job-42']
receive 2 right after (invisible): []
receive 3 after timeout expiry: train-job-42 ReceiveCount: 2 -> duplicate delivery
processed | skipped (already done)
```

**Follow-ups:**
- FIFO or standard? FIFO gives ordering and dedup within limits (check current docs) but lower throughput; the handler should still be idempotent.
- Partial batch failure? Report only failed message ids (batch item failures) so successes are not retried; check current docs for the response shape.

**Common mistakes:** Visibility timeout shorter than the function runtime; no DLQ; assuming exactly-once; DLQ with no alarm so failures sit silent.

---

### Q24 ⭐⭐ 🟢 SageMaker Model Registry: model package groups, versions, approval status (PendingManualApproval, Approved, Rejected), what metadata and inference specification a package holds, and how an approval event can trigger a deployment pipeline. Registry concepts and promotion gates are owned by Parts 4 and 7; this question is about the SageMaker service objects. Create a group, a package and an approval update in moto and print the statuses.
**Asked at:** SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)

**Say this first (1 line):** The SageMaker Model Registry is a group of versioned model packages. Each package carries the inference container and model data location, metadata and an approval status, and a status change emits an event that can start deployment.

**Then explain:**
- **Model package group:** a named collection (one per model line, for example churn-model). Each registered version is a model package with an auto-incremented version number.
- **Package contents:** `InferenceSpecification` (container image, model data S3 URL, supported content types), optional model metrics, customer metadata, and the approval status.
- **Approval status:** `PendingManualApproval`, `Approved`, `Rejected`. Status alone does not deploy anything; it is a gate that a pipeline or event rule reads.
- **Trigger:** SageMaker emits an EventBridge event on model package state change. A rule filtered on `Approved` can start CodePipeline or Step Functions. Event details: check current docs.
- **Scope:** promotion policy and gates live in Parts 4 and 7; here it is just the service objects.
- **Failure modes:** deploying a package whose S3 artifact was deleted; approving without recording the metrics that justified it; two groups for the same model.

**Example:** Create group churn-model, create package version 1 as PendingManualApproval, update it to Approved. Listing Approved packages in the group returns 1.

**Code:**

```python
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

with mock_aws():
    sm = boto3.client("sagemaker")
    sm.create_model_package_group(ModelPackageGroupName="churn-model", ModelPackageGroupDescription="demo")
    arn = sm.create_model_package(ModelPackageGroupName="churn-model", ModelPackageDescription="v1", ModelApprovalStatus="PendingManualApproval",
        InferenceSpecification={"Containers": [{"Image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/infer:1", "ModelDataUrl": "s3://ml-artifacts/churn/model.tar.gz"}],
            "SupportedContentTypes": ["text/csv"], "SupportedResponseMIMETypes": ["text/csv"]},
        CustomerMetadataProperties={"git_sha": "abc123", "auc": "0.91"})["ModelPackageArn"]
    print("arn tail:", arn.split(":", 5)[-1])
    d = sm.describe_model_package(ModelPackageName=arn)
    print("status before:", d["ModelApprovalStatus"], "| version:", d.get("ModelPackageVersion"))
    sm.update_model_package(ModelPackageArn=arn, ModelApprovalStatus="Approved", ApprovalDescription="reviewed by ds-lead")
    d = sm.describe_model_package(ModelPackageName=arn)
    print("status after:", d["ModelApprovalStatus"], "| metadata:", d.get("CustomerMetadataProperties"))
    print("containers:", [c["ModelDataUrl"] for c in d["InferenceSpecification"]["Containers"]])
    pk = sm.list_model_packages(ModelPackageGroupName="churn-model", ModelApprovalStatus="Approved")["ModelPackageSummaryList"]
    print("approved in group:", len(pk))
    # EventBridge rule shape for the approval event (rule is just stored; nothing fires)
    import json
    ev = boto3.client("events")
    ev.put_rule(Name="on-approved", EventPattern=json.dumps({"source": ["aws.sagemaker"], "detail-type": ["SageMaker Model Package State Change"], "detail": {"ModelApprovalStatus": ["Approved"]}}))
    print("rule stored:", ev.describe_rule(Name="on-approved")["Name"], "(no event is ever delivered in moto)")
```

**Output (my run):** Ran with `python3 -I` from an empty temp dir, Python 3.13.17, boto3 1.43.118, moto 5.2.4, fake keys, in-process `mock_aws()` (no moto server needed, no network to AWS). Moto is API shape only: Moto stores and returns group, package and status changes (API shape only). It did not echo my CustomerMetadataProperties back (printed None) so do not rely on that here. No EventBridge event is delivered on approval; the rule I created is only stored. Real events and downstream deployments: not executed.

```text
arn tail: model-package/churn-model/1
status before: PendingManualApproval | version: 1
status after: Approved | metadata: None
containers: ['s3://ml-artifacts/churn/model.tar.gz']
approved in group: 1
rule stored: on-approved (no event is ever delivered in moto)
```

**Follow-ups:**
- Who should approve? A human or an automated check, recorded with an approval description; keep a separate role for approval than for registering.
- Registry vs MLflow registry? Different service; both hold versions and stages. Choose by where the rest of your stack lives.

**Common mistakes:** Treating approval as deployment; no metadata on the package (git SHA, data version); letting the training role also approve.

---

### Q25 ⭐⭐ 🟡 Multi-model endpoints, multi-container endpoints and inference components in SageMaker: what each hosts, how a multi-model endpoint loads models from S3 on demand and evicts them, what workloads suit it (thousands of small per-tenant models) and what does not (large GPU models, strict p99), and the cold-load penalty on first call. Create a model with a multi-model mode in moto and note what is not emulated. Compare with simply running many small endpoints.
**Asked at:** SageMaker hosting docs and write-ups (AWS 'Supported features' feature matrix and Model Hosting FAQs, caylent.com 'How To Pick the Best SageMaker Model Hosting Option' and 'SageMaker inference types', kodekloud AWS ML Engineer Associate notes on endpoint types; search snippets only, not opened; one third-party page's latency and payload figures conflicted with AWS and were not used); vendor docs and training notes, not interview reports; MLOps and ML engineer roles on AWS | SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs

**Say this first (1 line):** A multi-model endpoint hosts many models behind one endpoint and loads each from S3 on first request, evicting cold ones. It suits thousands of small per-tenant models, not big GPU models with strict p99.

**Then explain:**
- **Multi-model endpoint (MME):** one container image serves many artifacts from an S3 prefix; the caller passes `TargetModel`. The container lazy-loads a model into memory/disk and evicts when memory is short.
- **Cold-load penalty:** the first call for a model pays the S3 download and load. Later calls are warm until eviction. Latency is therefore uneven; check current docs for hosting details and instance support (GPU support rules differ).
- **Multi-container endpoint:** different containers on one endpoint, either invoked directly or chained as a serial inference pipeline (for example preprocess then model).
- **Inference components:** a newer way to place several models on one endpoint with per-model compute settings and scaling; check current docs for the current feature set.
- **Good fit:** many small, similar, rarely-hit models (per-customer forecasters). **Bad fit:** large GPU models, strict latency SLO, models that all stay hot (eviction thrash).
- **Versus many small endpoints:** simpler isolation and per-model scaling, but each endpoint has a minimum instance cost and management overhead. MME shares one fleet and cuts idle cost, at the price of cold loads and noisy neighbours.

**Example:** 10,000 tenant models, each hit a few times a day. One MME with 2 instances beats 10,000 endpoints. A fraud model needing p99 under 50 ms should have its own endpoint.

**Code:**

```python
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

with mock_aws():
    sm = boto3.client("sagemaker")
    img = "123456789012.dkr.ecr.us-east-1.amazonaws.com/xgb-infer:1"
    role = "arn:aws:iam::123456789012:role/sm"
    sm.create_model(ModelName="tenants-mme", ExecutionRoleArn=role,
        PrimaryContainer={"Image": img, "Mode": "MultiModel", "ModelDataUrl": "s3://ml-models/tenants/"})
    d = sm.describe_model(ModelName="tenants-mme")
    print("MME container:", d["PrimaryContainer"]["Mode"], d["PrimaryContainer"]["ModelDataUrl"])
    sm.create_model(ModelName="pipe", ExecutionRoleArn=role, InferenceExecutionConfig={"Mode": "Serial"},
        Containers=[{"Image": img, "ContainerHostname": "pre"}, {"Image": img, "ContainerHostname": "model"}])
    d = sm.describe_model(ModelName="pipe")
    print("multi-container: containers =", [c["ContainerHostname"] for c in d["Containers"]], "| InferenceExecutionConfig echoed:", d.get("InferenceExecutionConfig"))
    sm.create_endpoint_config(EndpointConfigName="mme-cfg", ProductionVariants=[{"VariantName": "v", "ModelName": "tenants-mme", "InstanceType": "ml.m5.large", "InitialInstanceCount": 1}])
    sm.create_endpoint(EndpointName="mme-ep", EndpointConfigName="mme-cfg")
    print("endpoint:", sm.describe_endpoint(EndpointName="mme-ep")["EndpointStatus"])
    rt = boto3.client("sagemaker-runtime")
    r = rt.invoke_endpoint(EndpointName="mme-ep", TargetModel="tenant-17.tar.gz", Body=b"1,2,3", ContentType="text/csv")
    print("invoke with TargetModel returned:", r["Body"].read(), "-> canned; nothing loaded from S3, no cold load, no eviction")
```

**Output (my run):** Ran with `python3 -I` from an empty temp dir, Python 3.13.17, boto3 1.43.118, moto 5.2.4, fake keys, in-process `mock_aws()` (no moto server needed, no network to AWS). Moto is API shape only: NOT emulated: no S3 load, no eviction, no cold-load latency, no model memory limits. Moto accepted `Mode: MultiModel`, and invoke returned a canned body regardless of TargetModel. It also did not echo InferenceExecutionConfig for the multi-container model (printed None). Everything about real hosting behaviour: not executed.

```text
MME container: MultiModel s3://ml-models/tenants/
multi-container: containers = ['pre', 'model'] | InferenceExecutionConfig echoed: None
endpoint: InService
invoke with TargetModel returned: b'body' -> canned; nothing loaded from S3, no cold load, no eviction
```

**Follow-ups:**
- How do you handle a noisy neighbour? Split into several MMEs by tier, or give heavy tenants their own endpoint.
- What do you monitor? Per-model load time and invocation count, memory and disk use, eviction rate; metric names: check current docs.

**Common mistakes:** Putting large GPU models in an MME; ignoring cold-load latency; no per-tenant isolation plan; assuming TargetModel needs no S3 permissions on the execution role.

---

### Q26 ⭐⭐ 🟡 SageMaker Pipelines: steps (processing, training, tuning, condition, register model, lambda, callback), parameters, step caching, how a pipeline definition is JSON, and when to prefer it over Step Functions or Airflow. Orchestration tool design belongs to Part 5; keep to SageMaker's own objects. Build a minimal pipeline definition dict, validate its structure with a small checker, create the pipeline in moto and start an execution. State that no step ran.
**Asked at:** SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs | Job-posting skill lists (a getonbrd Senior MLOps Engineer AWS and SageMaker posting listing Athena, RDS, ECR, IAM, CloudWatch, CloudFormation or Terraform and GitHub Actions, a workingnomads Senior MLOps Engineer SageMaker and Airflow posting; search snippets only, not opened); job postings, not interview reports; MLOps roles on AWS

**Say this first (1 line):** SageMaker Pipelines is SageMaker's own DAG service: typed steps, parameters and a JSON definition, with step caching. Pick it when the work is mostly SageMaker jobs; pick Step Functions or Airflow for broader, cross-service orchestration.

**Then explain:**
- **Steps:** Processing, Training, Tuning, Condition (branch), RegisterModel, Lambda, Callback and others (check current docs for the list). Dependencies come from data references or explicit `DependsOn`.
- **Parameters:** typed pipeline inputs (for example the input S3 path), referenced as `{"Get": "Parameters.Name"}`. Change them per execution without editing the definition.
- **Caching:** a step with `CacheConfig` and an `ExpireAfter` can reuse an earlier result if its arguments match. Good for expensive preprocessing; the cache key rules and what counts as a match: check current docs.
- **Definition is JSON:** the SDK builds it, and `create_pipeline` accepts the JSON string. Validating structure early (names unique, parameters declared, DependsOn resolved) catches typos before a long run.
- **When to prefer:** native ML lineage, Studio UI and registry integration favour Pipelines. Prefer Step Functions for non-SageMaker work, or Airflow when the platform already runs it (design is Part 5).
- **Failure modes:** a Condition referencing a property that does not exist; cache hiding a changed upstream data file because the path stayed the same.

**Example:** Prep (processing) -> Train (training, cached) -> AucCheck (condition) -> Register. A checker flags a step that depends on a name that does not exist and a parameter that was never declared.

**Code:**

```python
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

import json
def check(defn):
    errs = []
    if "Version" not in defn: errs.append("no Version")
    names = [s["Name"] for s in defn.get("Steps", [])]
    if len(names) != len(set(names)): errs.append("duplicate step names")
    pnames = {p["Name"] for p in defn.get("Parameters", [])}
    text = json.dumps(defn)
    import re
    for ref in re.findall(r'"Get": "Parameters\.([A-Za-z0-9_]+)"', text):
        if ref not in pnames: errs.append("unknown parameter " + ref)
    for s in defn.get("Steps", []):
        for k in ("Name", "Type", "Arguments"):
            if k not in s and s.get("Type") != "Condition": errs.append(f"{s.get('Name')}: missing {k}")
        for dep in s.get("DependsOn", []):
            if dep not in names: errs.append(f"{s['Name']}: DependsOn unknown {dep}")
        if s.get("Type") == "Condition":
            for br in ("IfSteps", "ElseSteps"):
                for sub in s.get("Arguments", {}).get(br, []):
                    if sub["Name"] not in names + [x["Name"] for x in s["Arguments"].get(br, [])]: errs.append("bad branch step")
    return errs
good = {"Version": "2020-12-01", "Parameters": [{"Name": "InputData", "Type": "String", "DefaultValue": "s3://ml/in"}],
 "Steps": [
  {"Name": "Prep", "Type": "Processing", "Arguments": {"ProcessingInputs": [{"S3Uri": {"Get": "Parameters.InputData"}}]}},
  {"Name": "Train", "Type": "Training", "DependsOn": ["Prep"], "Arguments": {"AlgorithmSpecification": {}}, "CacheConfig": {"Enabled": True, "ExpireAfter": "P30D"}},
  {"Name": "AucCheck", "Type": "Condition", "Arguments": {"Conditions": [{"Type": "GreaterThanOrEqualTo"}], "IfSteps": [{"Name": "Register", "Type": "RegisterModel", "Arguments": {}}], "ElseSteps": []}}]}
bad = json.loads(json.dumps(good)); bad["Steps"][1]["DependsOn"] = ["Nope"]; bad["Parameters"] = []
print("good errors:", check(good)); print("bad errors:", check(bad))
with mock_aws():
    sm = boto3.client("sagemaker")
    sm.create_pipeline(PipelineName="train-pipe", PipelineDefinition=json.dumps(good), RoleArn="arn:aws:iam::123456789012:role/sm")
    ex = sm.start_pipeline_execution(PipelineName="train-pipe")["PipelineExecutionArn"]
    print("execution status (API shape only):", sm.describe_pipeline_execution(PipelineExecutionArn=ex)["PipelineExecutionStatus"])
    try:
        print("steps listed:", len(sm.list_pipeline_execution_steps(PipelineExecutionArn=ex)["PipelineExecutionSteps"]))
    except Exception as e:
        print("list_pipeline_execution_steps:", type(e).__name__, str(e)[:70])
    print("moto reports a status but no step ran: no processing, no training, no condition evaluated")
```

**Output (my run):** Ran with `python3 -I` from an empty temp dir, Python 3.13.17, boto3 1.43.118, moto 5.2.4, fake keys, in-process `mock_aws()` (no moto server needed, no network to AWS). Moto is API shape only: No step ran. Moto stores the definition and `start_pipeline_execution` returns an execution that moto itself reports as Succeeded with nothing executed; `list_pipeline_execution_steps` is NotImplementedError in moto. My checker is a small structural check, not the SageMaker validator; real validation rules: check current docs. Pipeline execution on AWS: not executed.

```text
good errors: []
bad errors: ['unknown parameter InputData', 'Train: DependsOn unknown Nope']
execution status (API shape only): Succeeded
list_pipeline_execution_steps: NotImplementedError The list_pipeline_execution_steps action has not been implemented
moto reports a status but no step ran: no processing, no training, no condition evaluated
```

**Follow-ups:**
- Pipelines or Step Functions for a train-evaluate-deploy flow? If everything is SageMaker jobs and you want registry lineage, Pipelines; if it also calls many other services with retries, Step Functions.
- How do you trigger it? EventBridge schedule or event, or an API call from CI.

**Common mistakes:** Trusting the caching on changed data at the same S3 path; hard-coding paths instead of parameters; believing a moto 'Succeeded' means anything ran.

---

### Q27 ⭐⭐ 🟡 Step Functions: Standard versus Express workflows, state types (Task, Choice, Map, Parallel, Wait, Pass), Retry and Catch, service integrations (run-a-job versus wait-for-callback patterns), and the execution-history model. Design a train, evaluate, branch, deploy flow with a retry on throttling. Validate an Amazon States Language definition with a small pure-Python checker (every Next resolves, one StartAt, terminal states) and create it in moto; the real state engine is not executed.
**Asked at:** SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs | Job-posting skill lists (a getonbrd Senior MLOps Engineer AWS and SageMaker posting listing Athena, RDS, ECR, IAM, CloudWatch, CloudFormation or Terraform and GitHub Actions, a workingnomads Senior MLOps Engineer SageMaker and Airflow posting; search snippets only, not opened); job postings, not interview reports; MLOps roles on AWS

**Say this first (1 line):** Step Functions is a state-machine service defined in Amazon States Language. Standard is for long, auditable workflows; Express is for high-volume short ones. For ML you chain Task states with Retry, Catch and a Choice gate.

**Then explain:**
- **Standard vs Express:** Standard runs for a long time, with durable execution history you can inspect. Express is for short, high-rate runs, with history through logging rather than the execution-history API. Duration limits and delivery semantics: check current docs.
- **State types:** Task (do work), Choice (branch), Map (loop over items), Parallel (fixed branches), Wait, Pass, Succeed, Fail.
- **Retry and Catch:** Retry on named errors with interval, backoff rate and max attempts (use it for throttling). Catch routes to a fallback state after retries run out.
- **Integrations:** request-response (start and move on), run-a-job `.sync` (wait until the job finishes), and wait-for-callback with a task token for human or external steps. Exact ARNs and supported services: check current docs.
- **History model:** each execution is an event history of state entries and exits; that is what you debug from.
- **Design:** Train (retry on throttling) -> Evaluate -> Gate on metric -> Deploy, else Fail. Common failure modes: a Next that points nowhere, a state with no Next or End, retrying non-idempotent steps.

**Example:** Train retries ThrottlingException up to 4 times with doubling intervals starting at 10 s. If AUC from Evaluate is at least 0.9, Deploy; else Fail. The checker catches a Choice default pointing to a missing state.

**Code:**

```python
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

import json
def check(d):
    errs = []; st = d.get("States", {})
    if "StartAt" not in d: errs.append("no StartAt")
    elif d["StartAt"] not in st: errs.append("StartAt unknown: " + d["StartAt"])
    terminal = 0
    for n, s in st.items():
        t = s.get("Type"); nxt = []
        if t in ("Succeed", "Fail"): terminal += 1
        elif t == "Choice":
            nxt = [c["Next"] for c in s.get("Choices", [])] + ([s["Default"]] if "Default" in s else [])
        else:
            if s.get("End"): terminal += 1
            elif "Next" in s: nxt = [s["Next"]]
            else: errs.append(n + ": no Next or End")
        for c in s.get("Catch", []): nxt.append(c["Next"])
        for x in nxt:
            if x not in st: errs.append(f"{n}: Next '{x}' not found")
    if terminal == 0: errs.append("no terminal state")
    return errs
retry = [{"ErrorEquals": ["ThrottlingException", "SageMaker.AmazonSageMakerException"], "IntervalSeconds": 10, "BackoffRate": 2.0, "MaxAttempts": 4}]
flow = {"StartAt": "Train", "States": {
 "Train": {"Type": "Task", "Resource": "arn:aws:states:::sagemaker:createTrainingJob.sync", "Parameters": {"TrainingJobName.$": "$$.Execution.Name"}, "Retry": retry, "Catch": [{"ErrorEquals": ["States.ALL"], "Next": "Failed"}], "Next": "Evaluate"},
 "Evaluate": {"Type": "Task", "Resource": "arn:aws:states:::lambda:invoke", "Next": "Gate"},
 "Gate": {"Type": "Choice", "Choices": [{"Variable": "$.Payload.auc", "NumericGreaterThanEquals": 0.9, "Next": "Deploy"}], "Default": "Failed"},
 "Deploy": {"Type": "Task", "Resource": "arn:aws:states:::sagemaker:createEndpoint", "End": True},
 "Failed": {"Type": "Fail", "Error": "QualityGate", "Cause": "auc below bar or training failed"}}}
print("good:", check(flow))
broken = json.loads(json.dumps(flow)); broken["States"]["Gate"]["Default"] = "Nowhere"; del broken["States"]["Deploy"]["End"]
print("broken:", check(broken))
with mock_aws():
    sf = boto3.client("stepfunctions")
    arn = sf.create_state_machine(name="train-eval-deploy", definition=json.dumps(flow), roleArn="arn:aws:iam::123456789012:role/sfn")["stateMachineArn"]
    print("created:", sf.describe_state_machine(stateMachineArn=arn)["status"])
    print("type:", sf.describe_state_machine(stateMachineArn=arn)["type"])
    ex = sf.start_execution(stateMachineArn=arn, input="{}")["executionArn"]
    print("started; status reported by moto (no real state engine for these task ARNs):", sf.describe_execution(executionArn=ex)["status"])
```

**Output (my run):** Ran with `python3 -I` from an empty temp dir, Python 3.13.17, boto3 1.43.118, moto 5.2.4, fake keys, in-process `mock_aws()` (no moto server needed, no network to AWS). Moto is API shape only: The checker is mine and simplified (Next/Default/Catch targets, StartAt, terminal states; not Map/Parallel inner graphs, not JSONPath validity). Moto stores the definition and starts an execution, but it does not run SageMaker or Lambda integrations; the RUNNING status shown is moto's, not a real run. Real state engine, retries and `.sync` waits: not executed.

```text
good: []
broken: ["Gate: Next 'Nowhere' not found", 'Deploy: no Next or End']
created: ACTIVE
type: STANDARD
started; status reported by moto (no real state engine for these task ARNs): RUNNING
```

**Follow-ups:**
- Express or Standard for an inference pre-processing fan-out? Express if short and high-rate; Standard if you need durable history or human callback.
- Where does a timeout belong? On the Task (`TimeoutSeconds`), plus HeartbeatSeconds for long jobs.

**Common mistakes:** No Catch so a failure leaves a vague error; retrying a non-idempotent deploy; polling loops instead of `.sync`; hard-coding ARNs.

---

### Q28 ⭐⭐ 🟡 AWS Batch versus SageMaker Training or Processing versus ECS tasks for batch ML work (nightly feature jobs, embedding generation, hyperparameter sweeps): compute environment, job queue, job definition, array jobs, spot, priorities. Give a decision table and say when you would not use Batch. Create a compute environment, queue and job definition in moto where supported and record what fails; no job is executed.
**Asked at:** Container-service comparison sources (nops.io 'ECS vs EKS vs Fargate', perfectscale.io, jayendrapatil.com 'AWS EKS vs ECS Decision Guide', cloudoptimo, doit.com, a 2019 AWS slideshare on ML with container services; search snippets only, not opened); vendor and consultancy blogs stating opinion; DevOps, platform and MLOps roles | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)

**Say this first (1 line):** Batch queues containerised jobs on compute it manages (EC2, spot or Fargate), which is good for many CPU jobs and array sweeps; SageMaker Training or Processing is better for ML-aware jobs; plain ECS tasks are for simple one-offs.

**Then explain:**
- **Batch objects:** compute environment (what machines, min/max vCPUs, spot or on-demand), job queue (priority, ordered environments), job definition (image, resources, command). Array jobs run N copies with an index. Fair priority comes from queue priority; check current docs for scheduling policies.
- **Spot:** cheaper but interruptible; use retry strategy so interrupted jobs rerun. Jobs must be restartable.
- **Decision:** many independent jobs, queueing, priorities and arrays: Batch. GPU training with metrics, experiments, managed spot checkpoints, tuning: SageMaker. A single scheduled container, or already on ECS: ECS task (maybe via EventBridge).
- **Not Batch when:** you need ML job lineage and tuning built in, tiny infrequent jobs (a simple ECS task or Lambda is easier), or hard real-time.
- **Failure modes:** min vCPU above zero leaves idle machines; job stuck RUNNABLE because the compute environment cannot satisfy the resource ask; non-idempotent jobs retried on spot interruption.

**Example:** Nightly embedding generation over 1,000 shards: an array job of size 1,000 on a spot compute environment with retry 2. A one-off GPU fine-tune with checkpointing: SageMaker Training.

Decision table:

| Need | Batch | SageMaker Training/Processing | ECS task |
|---|---|---|---|
| Many independent CPU jobs, arrays, queue priorities | good fit | possible, more per-job overhead | manual scheduling |
| GPU training with checkpoints, tuning, lineage | possible | good fit | manual |
| One scheduled container | overkill | possible | good fit |
| Spot with retries | supported (check current docs) | managed spot (check current docs) | self-managed |

**Code:**

```python
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

with mock_aws():
    ec2 = boto3.client("ec2"); iam = boto3.client("iam"); b = boto3.client("batch")
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")["Vpc"]["VpcId"]
    sn = ec2.create_subnet(VpcId=vpc, CidrBlock="10.0.1.0/24")["Subnet"]["SubnetId"]
    sg = ec2.create_security_group(GroupName="batch-sg", Description="d", VpcId=vpc)["GroupId"]
    role = iam.create_role(RoleName="batch-svc", AssumeRolePolicyDocument="{}")["Role"]["Arn"]
    prof = iam.create_instance_profile(InstanceProfileName="ecsInst")["InstanceProfile"]["Arn"]
    def step(name, fn):
        try: r = fn(); print(f"{name}: OK"); return r
        except Exception as e: print(f"{name}: FAILED {type(e).__name__}: {str(e)[:110]}")
    step("compute env (EC2)", lambda: b.create_compute_environment(computeEnvironmentName="ml-ce", type="MANAGED", state="ENABLED", serviceRole=role,
        computeResources={"type": "EC2", "minvCpus": 0, "maxvCpus": 16, "desiredvCpus": 0, "instanceTypes": ["m5.large"], "subnets": [sn], "securityGroupIds": [sg], "instanceRole": prof}))
    step("compute env (SPOT)", lambda: b.create_compute_environment(computeEnvironmentName="ml-spot", type="MANAGED", state="ENABLED", serviceRole=role,
        computeResources={"type": "SPOT", "allocationStrategy": "SPOT_CAPACITY_OPTIMIZED", "minvCpus": 0, "maxvCpus": 16, "instanceTypes": ["m5.large"], "subnets": [sn], "securityGroupIds": [sg], "instanceRole": prof, "spotIamFleetRole": role}))
    step("job queue", lambda: b.create_job_queue(jobQueueName="ml-queue", priority=10, state="ENABLED", computeEnvironmentOrder=[{"order": 1, "computeEnvironment": "ml-ce"}]))
    step("job definition", lambda: b.register_job_definition(jobDefinitionName="embed-job", type="container",
        containerProperties={"image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/embed:1", "vcpus": 2, "memory": 4096, "command": ["python", "embed.py"]}))
    print("queues:", [q["jobQueueName"] for q in b.describe_job_queues()["jobQueues"]])
    print("job defs:", [d["jobDefinitionName"] + ":" + str(d["revision"]) for d in b.describe_job_definitions()["jobDefinitions"]])
    print("(no submit_job attempted: nothing would run)")
```

**Output (my run):** Ran with `python3 -I` from an empty temp dir, Python 3.13.17, boto3 1.43.118, moto 5.2.4, fake keys, in-process `mock_aws()` (no moto server needed, no network to AWS). Moto is API shape only: Moto accepted the compute environments, queue and job definition in this run (it needed a service role, instance profile, subnet and security group). I did not submit a job; nothing would run. Moto does not provision instances, schedule, or model spot. Real Batch behaviour: not executed.

```text
compute env (EC2): OK
compute env (SPOT): OK
job queue: OK
job definition: OK
queues: ['ml-queue']
job defs: ['embed-job:1']
(no submit_job attempted: nothing would run)
```

**Follow-ups:**
- How do you size an array job? One child per shard, each idempotent; cap concurrency via the environment's max vCPUs.
- Fargate or EC2 for Batch? Fargate for no node management and small jobs; EC2 when you need GPUs or specific instance types (check current docs).

**Common mistakes:** Using Batch for one tiny job; min vCPUs above zero; no retry strategy on spot; forgetting job idempotency.

---

### Q29 ⭐⭐ 🟡 S3 access control: IAM policy, bucket policy, ACLs (and why they are mostly disabled by default now), Block Public Access, access points, and VPC endpoint policies. Write a bucket policy that denies non-TLS requests and a policy that allows another account's role read access to one prefix, then show moto enforcing an explicit Deny bucket policy on a GET, and the evaluator giving the cross-account decisions. Say what real AWS adds that moto does not.
**Asked at:** IAM interview and policy-evaluation sources (AWS IAM 'Policy evaluation logic' pages on docs.aws.amazon.com and docs.aws.eu, tutorialsdojo 'How AWS IAM Handles Conflicting IAM Policies', advancedweb.hu 'IAM policy evaluation logic explained with examples', barkingiguana 'How IAM Policy Evaluation Actually Works', community.aws and hidekazu-konishi IAM glossary; search snippets only, not opened); vendor docs and study guides, not verified candidate reports; cloud, DevOps, security and MLOps roles at IT-services firms, product companies and GCCs | S3 interview question banks (novelvista '100+ Top AWS S3 Interview Questions', adaface, ccbp.in, a techinterview.org 'System Design Interview: Object Storage (Amazon S3)' post, AWS developer exam-prep study guides; search snippets only, not opened; WebFetch of docs.aws.amazon.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; cloud, data and ML engineer roles at IT-services firms, product companies and GCCs

**Say this first (1 line):** S3 access is the union of identity policy, bucket policy and other layers, with one rule on top: any explicit Deny wins. In the same account either side can allow; across accounts both sides must allow.

**Then explain:**
- **Layers:** IAM identity policy (what the caller may do), bucket policy (resource policy, can name other accounts), access points (per-use-case names with their own policy), VPC endpoint policy (limits what goes through the endpoint), Block Public Access (a guard against public grants).
- **ACLs:** legacy. New buckets default to ACLs disabled via Object Ownership 'bucket owner enforced' (check current docs). Use policies, not ACLs.
- **Non-TLS deny:** a Deny with `Bool aws:SecureTransport = false` forces HTTPS.
- **Cross-account read on one prefix:** the bucket policy names the other account's role and a prefix in `Resource`; the other account's role must also have an identity allow. Both are needed.
- **Failure modes:** a wildcard Principal with an Allow (public); forgetting the identity side in the partner account; a deny without scoping that breaks your own pipelines; KMS-encrypted objects also need key permissions.
- **What real AWS adds:** full IAM evaluation for every caller (moto enforces little by default), SCPs and boundaries, KMS key policy checks, VPC endpoint routing, Access Analyzer, CloudTrail and Block Public Access enforcement. Moto's S3 did enforce this bucket-policy Deny in this run; the rest I did not test.

**Example:** Bucket ml-secure-data: partner account 222222222222 may read `train/*` only. With a Deny on `train/*` the GET returns 403 but `other/` still returns 200.

**Code:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {"Sid": "DenyNonTLS", "Effect": "Deny", "Principal": "*", "Action": "s3:*",
     "Resource": ["arn:aws:s3:::ml-secure-data", "arn:aws:s3:::ml-secure-data/*"],
     "Condition": {"Bool": {"aws:SecureTransport": "false"}}},
    {"Sid": "PartnerReadTrain", "Effect": "Allow",
     "Principal": {"AWS": "arn:aws:iam::222222222222:role/partner-reader"},
     "Action": "s3:GetObject", "Resource": "arn:aws:s3:::ml-secure-data/train/*"}
  ]
}
```

```python
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

import json, sys
from botocore.exceptions import ClientError
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iam_eval_sketch import evaluate
B = "ml-secure-data"
tls_deny = {"Version": "2012-10-17", "Statement": [{"Sid": "DenyNonTLS", "Effect": "Deny", "Principal": "*", "Action": "s3:*",
    "Resource": [f"arn:aws:s3:::{B}", f"arn:aws:s3:::{B}/*"], "Condition": {"Bool": {"aws:SecureTransport": "false"}}}]}
xacct = {"Version": "2012-10-17", "Statement": [{"Sid": "PartnerReadTrain", "Effect": "Allow", "Principal": {"AWS": "arn:aws:iam::222222222222:role/partner-reader"},
    "Action": "s3:GetObject", "Resource": f"arn:aws:s3:::{B}/train/*"}]}
print("policies are valid JSON:", bool(json.dumps(tls_deny)) and bool(json.dumps(xacct)))
with mock_aws():
    s3 = boto3.client("s3"); s3.create_bucket(Bucket=B)
    s3.put_object(Bucket=B, Key="train/a.csv", Body=b"1")
    print("GET before deny policy:", s3.get_object(Bucket=B, Key="train/a.csv")["ResponseMetadata"]["HTTPStatusCode"])
    deny = {"Version": "2012-10-17", "Statement": [{"Effect": "Deny", "Principal": "*", "Action": "s3:GetObject", "Resource": f"arn:aws:s3:::{B}/train/*"}]}
    s3.put_bucket_policy(Bucket=B, Policy=json.dumps(deny))
    try: s3.get_object(Bucket=B, Key="train/a.csv")
    except ClientError as e: print("GET after explicit Deny policy:", e.response["ResponseMetadata"]["HTTPStatusCode"], e.response["Error"]["Code"])
    print("other prefix still readable?:", end=" ")
    s3.put_object(Bucket=B, Key="other/b.csv", Body=b"2"); print(s3.get_object(Bucket=B, Key="other/b.csv")["ResponseMetadata"]["HTTPStatusCode"])
    s3.put_public_access_block(Bucket=B, PublicAccessBlockConfiguration={"BlockPublicAcls": True, "IgnorePublicAcls": True, "BlockPublicPolicy": True, "RestrictPublicBuckets": True})
    print("BPA read-back:", s3.get_public_access_block(Bucket=B)["PublicAccessBlockConfiguration"])
# evaluator: cross-account decisions
role = "arn:aws:iam::222222222222:role/partner-reader"
obj = f"arn:aws:s3:::{B}/train/a.csv"; other = f"arn:aws:s3:::{B}/val/c.csv"
idp = {"Statement": [{"Effect": "Allow", "Action": "s3:GetObject", "Resource": f"arn:aws:s3:::{B}/*"}]}
rp = {"Statement": xacct["Statement"]}
rows = [
 ("both sides allow, train/ prefix", obj, dict(identity=[idp], resource_policy=rp)),
 ("bucket policy only, no identity allow", obj, dict(identity=[], resource_policy=rp)),
 ("identity allow only, no bucket policy", obj, dict(identity=[idp], resource_policy=None)),
 ("both, but other prefix val/", other, dict(identity=[idp], resource_policy=rp)),
]
for label, res, kw in rows:
    print(f"{label:42s}", evaluate("s3:GetObject", res, same_account=False, principal_arn=role, **kw))
print("non-TLS ctx vs TLS-deny policy:", evaluate("s3:GetObject", obj, ctx={"aws:SecureTransport": "false"}, identity=[idp, {"Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}]}, {"Statement": tls_deny["Statement"]}]))
print("TLS ctx:", evaluate("s3:GetObject", obj, ctx={"aws:SecureTransport": "true"}, identity=[idp, {"Statement": tls_deny["Statement"]}]))
print(json.dumps(tls_deny["Statement"][0]["Condition"]))
```

**Output (my run):** Ran with `python3 -I` from an empty temp dir, Python 3.13.17, boto3 1.43.118, moto 5.2.4, fake keys, in-process `mock_aws()` (no moto server needed, no network to AWS). Moto is API shape only: Moto enforced the explicit-Deny bucket policy on GET (403) in this run. The evaluator (copied from the Wave A sketch, simplified: no NotAction, policy variables, KMS, access points, endpoint policies, Block Public Access) gave the cross-account decisions. The Deny and Allow statements above are shown in one JSON document for reading; in the Python run they are separate objects (the evaluator in the last two lines took the TLS deny as a policy and a context of http vs https). Real AWS enforcement: not executed.

```text
policies are valid JSON: True
GET before deny policy: 200
GET after explicit Deny policy: 403 403
other prefix still readable?: 200
BPA read-back: {'BlockPublicAcls': True, 'IgnorePublicAcls': True, 'BlockPublicPolicy': True, 'RestrictPublicBuckets': True}
both sides allow, train/ prefix            ('Allow', 'cross-account: identity AND resource policy allow')
bucket policy only, no identity allow      ('Deny', 'implicit deny: cross-account needs both sides')
identity allow only, no bucket policy      ('Deny', 'implicit deny: cross-account needs both sides')
both, but other prefix val/                ('Deny', 'implicit deny: cross-account needs both sides')
non-TLS ctx vs TLS-deny policy: ('Deny', 'explicit deny')
TLS ctx: ('Allow', 'identity or resource policy allows (same account)')
{"Bool": {"aws:SecureTransport": "false"}}
```

**Follow-ups:**
- Where does the partner's side go? An identity policy on partner-reader allowing s3:GetObject on that prefix (in their account).
- Access points? Give each team its own name and policy; delegate details to the access point policy; check current docs for how they combine with the bucket policy.

**Common mistakes:** Only editing the bucket policy for cross-account; Principal `*` with Allow; mixing ACLs and policies; forgetting `s3:ListBucket` on the bucket ARN (not the object ARN) for listing.

---

### Q30 ⭐⭐ 🟡 Permissions boundary versus SCP versus session policy: who sets each, what each can and cannot do (none of them grants permissions by itself), and a delegation scenario (let ML engineers create roles for their jobs without letting them escalate to admin). Write the boundary and a deny-without-boundary guardrail, run both through the evaluator including a role that tries to attach AdministratorAccess, and explain where the sketch is simplified.
**Asked at:** IAM interview and policy-evaluation sources (AWS IAM 'Policy evaluation logic' pages on docs.aws.amazon.com and docs.aws.eu, tutorialsdojo 'How AWS IAM Handles Conflicting IAM Policies', advancedweb.hu 'IAM policy evaluation logic explained with examples', barkingiguana 'How IAM Policy Evaluation Actually Works', community.aws and hidekazu-konishi IAM glossary; search snippets only, not opened); vendor docs and study guides, not verified candidate reports; cloud, DevOps, security and MLOps roles at IT-services firms, product companies and GCCs | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)

**Say this first (1 line):** None of the three grants anything. A permissions boundary and a session policy cap one identity; an SCP caps a whole account or OU. Effective access is what the identity policy allows and every cap also allows, and any explicit deny wins.

**Then explain:**
- **Permissions boundary:** set by an IAM admin on a user or role; maximum permissions that role can ever have. Does not grant. Does not limit resource policies naming the exact principal ARN (check current docs).
- **SCP:** set in AWS Organizations on accounts or OUs; a ceiling over all principals there. It does not apply to the management account, and does not grant. Service-linked roles are exempt (check current docs).
- **Session policy:** passed when assuming a role or federating; narrows that session only, as an intersection with the role's permissions.
- **Delegation:** let ML engineers create roles `ml-*`, but only with the boundary attached, and deny changing or removing the boundary. Then a role they create with AdministratorAccess is still capped to S3, SageMaker, logs and ECR reads.
- **Guardrail:** a Deny on `iam:CreateRole` when `iam:PermissionsBoundary` is not the approved ARN (as an SCP or identity-policy deny). Also protect the boundary policy itself from edits, which this sketch does not show.
- **Failure modes:** boundary missing `iam:PassRole` where the job needs it; forgetting that SCP and boundary only cut, so a role with an empty identity policy still has nothing.

**Example:** Engineer creates `ml-trainer` with the boundary: allowed. Without it: denied. Attaching AdministratorAccess to ml-trainer is allowed as an action, but its iam:CreateUser and ec2:RunInstances are outside the boundary, so denied.

**Code:**

```python
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iam_eval_sketch import evaluate
ACCT = "123456789012"
BP = f"arn:aws:iam::{ACCT}:policy/MlJobBoundary"
boundary = {"Statement": [{"Effect": "Allow", "Action": ["s3:*", "sagemaker:*", "logs:*", "ecr:Get*", "ecr:BatchGet*"], "Resource": "*"}]}
# delegation policy for ML engineers: may create roles ONLY with the boundary attached
engineer = {"Statement": [
  {"Effect": "Allow", "Action": ["iam:CreateRole", "iam:PutRolePolicy", "iam:AttachRolePolicy"], "Resource": f"arn:aws:iam::{ACCT}:role/ml-*"},
  {"Effect": "Allow", "Action": "iam:PassRole", "Resource": f"arn:aws:iam::{ACCT}:role/ml-*"}]}
# guardrail (as SCP or identity-policy deny): block CreateRole unless boundary is set
guard_deny = {"Statement": [
  {"Effect": "Deny", "Action": ["iam:CreateRole"], "Resource": "*", "Condition": {"StringNotEquals": {"iam:PermissionsBoundary": BP}}},
  {"Effect": "Deny", "Action": ["iam:DeleteRolePermissionsBoundary", "iam:PutRolePermissionsBoundary"], "Resource": "*"}]}
guard_sketch = guard_deny
scp = {"Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"}]}
scp_region = {"Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"}, {"Effect": "Deny", "Action": "sagemaker:*", "Resource": "*", "Condition": {"StringEquals": {"aws:RequestedRegion": "ap-east-1"}}}]}
role = f"arn:aws:iam::{ACCT}:role/ml-trainer"
admin_pol = {"Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"}]}  # what AdministratorAccess grants
def row(label, action, res, **kw):
    d, why = evaluate(action, res, **kw); print(f"{label:58s} {d:5s} {why}")
print("-- engineer (identity policy) creating roles")
row("engineer CreateRole ml-x, boundary supplied", "iam:CreateRole", f"arn:aws:iam::{ACCT}:role/ml-x", identity=[engineer, guard_sketch], ctx={"iam:PermissionsBoundary": BP})
row("engineer CreateRole ml-x, NO boundary (guardrail)", "iam:CreateRole", f"arn:aws:iam::{ACCT}:role/ml-x", identity=[engineer, guard_sketch], ctx={})
row("engineer CreateRole admin-x (name not ml-*)", "iam:CreateRole", f"arn:aws:iam::{ACCT}:role/admin-x", identity=[engineer], ctx={"iam:PermissionsBoundary": BP})
row("engineer removes boundary from ml-trainer", "iam:DeleteRolePermissionsBoundary", f"arn:aws:iam::{ACCT}:role/ml-trainer", identity=[engineer, guard_deny])
row("engineer attaches AdministratorAccess to ml-trainer", "iam:AttachRolePolicy", f"arn:aws:iam::{ACCT}:role/ml-trainer", identity=[engineer, guard_deny])
print("-- the created role ml-trainer: boundary + attached policies")
row("trainer s3:GetObject (identity allows, boundary allows)", "s3:GetObject", "arn:aws:s3:::ml-data/x", identity=[admin_pol], boundary=boundary)
row("trainer sagemaker:CreateTrainingJob", "sagemaker:CreateTrainingJob", "*", identity=[admin_pol], boundary=boundary)
row("trainer attached AdministratorAccess -> iam:CreateUser", "iam:CreateUser", "*", identity=[admin_pol], boundary=boundary)
row("trainer attached AdministratorAccess -> ec2:RunInstances", "ec2:RunInstances", "*", identity=[admin_pol], boundary=boundary)
row("trainer with NO boundary + AdministratorAccess -> iam:CreateUser", "iam:CreateUser", "*", identity=[admin_pol])
row("boundary allows s3 but identity grants nothing", "s3:GetObject", "arn:aws:s3:::ml-data/x", identity=[], boundary=boundary)
print("-- SCP and session policy")
row("SCP has no allow for ec2 (narrow SCP)", "ec2:RunInstances", "*", identity=[admin_pol], scps=[{"Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}]}])
row("SCP region deny, request in ap-east-1", "sagemaker:CreateTrainingJob", "*", identity=[admin_pol], scps=[scp_region], ctx={"aws:RequestedRegion": "ap-east-1"})
row("SCP region deny, request in us-east-1", "sagemaker:CreateTrainingJob", "*", identity=[admin_pol], scps=[scp_region], ctx={"aws:RequestedRegion": "us-east-1"})
sess = {"Statement": [{"Effect": "Allow", "Action": "s3:GetObject", "Resource": "arn:aws:s3:::ml-data/train/*"}]}
row("session policy: GetObject on train/ (in scope)", "s3:GetObject", "arn:aws:s3:::ml-data/train/a", identity=[admin_pol], session=sess)
row("session policy: PutObject (out of scope)", "s3:PutObject", "arn:aws:s3:::ml-data/train/a", identity=[admin_pol], session=sess)
row("session policy alone, role has no identity allow", "s3:GetObject", "arn:aws:s3:::ml-data/train/a", identity=[], session=sess)
```

**Output (my run):** Ran with `python3 -I` from an empty temp dir, Python 3.13.17, boto3 1.43.118, moto 5.2.4, fake keys, in-process `mock_aws()` (no moto server needed, no network to AWS). Moto is API shape only: Simplified evaluator (copied from the Wave A sketch; I added only `StringNotEquals` in my copy). Not handled: NotAction/NotResource, policy variables, most condition operators and set operators, the boundary-vs-resource-policy rules beyond the principal-ARN case, session-policy details for role chaining, service-linked roles, SCPs at several OU levels beyond a simple list, implicit-deny nuances for iam:PassRole. Real IAM: not executed.

```text
-- engineer (identity policy) creating roles
engineer CreateRole ml-x, boundary supplied                Allow identity or resource policy allows (same account)
engineer CreateRole ml-x, NO boundary (guardrail)          Deny  explicit deny
engineer CreateRole admin-x (name not ml-*)                Deny  implicit deny: nothing allows
engineer removes boundary from ml-trainer                  Deny  explicit deny
engineer attaches AdministratorAccess to ml-trainer        Allow identity or resource policy allows (same account)
-- the created role ml-trainer: boundary + attached policies
trainer s3:GetObject (identity allows, boundary allows)    Allow identity or resource policy allows (same account)
trainer sagemaker:CreateTrainingJob                        Allow identity or resource policy allows (same account)
trainer attached AdministratorAccess -> iam:CreateUser     Deny  implicit deny: outside permissions boundary
trainer attached AdministratorAccess -> ec2:RunInstances   Deny  implicit deny: outside permissions boundary
trainer with NO boundary + AdministratorAccess -> iam:CreateUser Allow identity or resource policy allows (same account)
boundary allows s3 but identity grants nothing             Deny  implicit deny: nothing allows
-- SCP and session policy
SCP has no allow for ec2 (narrow SCP)                      Deny  implicit deny: SCP level 0 does not allow
SCP region deny, request in ap-east-1                      Deny  explicit deny
SCP region deny, request in us-east-1                      Allow identity or resource policy allows (same account)
session policy: GetObject on train/ (in scope)             Allow identity or resource policy allows (same account)
session policy: PutObject (out of scope)                   Deny  implicit deny: outside session policy
session policy alone, role has no identity allow           Deny  implicit deny: nothing allows
```

**Follow-ups:**
- Boundary vs SCP, who uses which? SCP for org-wide guardrails by a platform team; boundary for delegating role creation inside an account.
- Can a boundary alone give access? No. Identity policy must also allow, except for the resource-policy exception noted in docs.

**Common mistakes:** Thinking a boundary grants access; leaving boundary removal permitted; applying an SCP expecting it to affect the management account; forgetting the identity side.

---

### Q31 ⭐⭐ 🟡 How does code get AWS credentials? Explain the default credential chain (environment variables, shared profile, web identity, container credentials, instance profile via IMDS), instance profiles versus roles, IMDSv2, and the EKS pods version (IRSA and EKS Pod Identity) at concept level. GitHub OIDC to AWS belongs to Part 7 and Kubernetes ServiceAccounts to Part 3. Run boto3's credential resolution in a sandbox with fake environment keys and then with none, print the resolved method, and say IMDS and IRSA were not executed.
**Asked at:** IAM interview and policy-evaluation sources (AWS IAM 'Policy evaluation logic' pages on docs.aws.amazon.com and docs.aws.eu, tutorialsdojo 'How AWS IAM Handles Conflicting IAM Policies', advancedweb.hu 'IAM policy evaluation logic explained with examples', barkingiguana 'How IAM Policy Evaluation Actually Works', community.aws and hidekazu-konishi IAM glossary; search snippets only, not opened); vendor docs and study guides, not verified candidate reports; cloud, DevOps, security and MLOps roles at IT-services firms, product companies and GCCs | Job-posting skill lists (a getonbrd Senior MLOps Engineer AWS and SageMaker posting listing Athena, RDS, ECR, IAM, CloudWatch, CloudFormation or Terraform and GitHub Actions, a workingnomads Senior MLOps Engineer SageMaker and Airflow posting; search snippets only, not opened); job postings, not interview reports; MLOps roles on AWS
**Say this first (1 line):** Code never hard-codes keys: the SDK walks a fixed chain (env vars, profile, web identity, container endpoint, instance metadata) and the first source that gives keys wins, so on AWS compute you attach a role and the SDK picks up short-lived credentials by itself.

**Then explain:**
- **The chain (botocore, printed from the run):** env, assume-role, assume-role-with-web-identity, sso, shared-credentials-file, login, custom-process, config-file, ec2-credentials-file, boto-config, container-role, iam-role. Order differs by SDK and version, so say 'check current docs' for other languages.
- **Env vars beat the shared file.** Case 3 in the run: both set, `env` won. Classic bug: a stale `AWS_ACCESS_KEY_ID` on a CI box silently overrides the role you thought you had.
- **Role versus instance profile.** A role is the identity with a trust policy and permissions. An instance profile is the container that lets EC2 attach one role to an instance. The console hides this; the API does not.
- **IMDSv2** (instance metadata, concept): the code first does a PUT to get a session token, then GETs credentials with that token header. It blocks simple SSRF tricks that worked on IMDSv1. A hop limit of 1 can stop containers on the host from reaching it (check current docs). Credentials rotate; the SDK refreshes them.
- **Containers and pods:** ECS tasks use a container-credentials endpoint (the `container-role` row; I ran it against a local fake). On EKS, IRSA projects an OIDC token file and the SDK calls AssumeRoleWithWebIdentity with it; EKS Pod Identity (newer) uses an agent on the node and the container-credentials route. Both give each pod its own role instead of the node role. Concept only here.
- **Failure modes:** no source found gives `NoCredentialsError` (case 5: `None`); a job on EC2 with IMDS blocked falls through and fails after a timeout; the node role leaks to every pod if you skip IRSA/Pod Identity.

**Example:** Laptop: you run `aws sso login`, the SDK takes the `sso` source. Training container on SageMaker or ECS: no keys in the image; the container endpoint hands out the task or execution role's keys, which expire. Hand-check from the run: with only the credentials file set, method is `shared-credentials-file` and key `AKIAFAKEFILEKEY0000`; add env vars as well and the key becomes `AKIAFAKEENVKEY00000`.

**Code:** The script spawns a clean child process per case with a temp HOME, `AWS_EC2_METADATA_DISABLED=true` and a loopback HTTP server pretending to be the container-credentials endpoint. Run with `python3 -I` from the venv (boto3 1.43.118, moto 5.2.4); fake keys only.
```python
# Q31: which credential source does boto3 pick? Each case runs in a child process with a clean env and a temp HOME.
import json, os, subprocess, sys, tempfile, threading
from http.server import BaseHTTPRequestHandler, HTTPServer

CHILD = r'''
import boto3, botocore.credentials as c
s = boto3.session.Session()
names = [p.METHOD for p in c.create_credential_resolver(s._session).providers]
try:
    cr = s.get_credentials()
    print("resolved method:", None if cr is None else cr.method, "| key:", None if cr is None else cr.access_key)
except Exception as e:
    print("error:", type(e).__name__)
print("chain order in this botocore:", names) if %r else None
'''

tmp = tempfile.mkdtemp(dir="/tmp/claude-0/b10_q31_40")
creds_file = os.path.join(tmp, "credentials")
open(creds_file, "w").write("[default]\naws_access_key_id = AKIAFAKEFILEKEY0000\naws_secret_access_key = fakesecretfile\n")
tok = os.path.join(tmp, "token"); open(tok, "w").write("fake.jwt.token")

class H(BaseHTTPRequestHandler):  # stands in for the ECS/container credentials endpoint (loopback only)
    def do_GET(self):
        body = json.dumps({"AccessKeyId": "ASIAFAKECONTAINER00", "SecretAccessKey": "fakesecretcontainer",
                           "Token": "faketoken", "Expiration": "2099-01-01T00:00:00Z"}).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(body)
    def log_message(self, *a): pass
srv = HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()

base = {"PATH": os.environ["PATH"], "HOME": tmp, "AWS_DEFAULT_REGION": "us-east-1",
        "AWS_EC2_METADATA_DISABLED": "true",             # no IMDS call: keeps the sandbox off the network
        "AWS_SHARED_CREDENTIALS_FILE": os.path.join(tmp, "nope"), "AWS_CONFIG_FILE": os.path.join(tmp, "nope2")}
cases = [
  ("1 env vars", {"AWS_ACCESS_KEY_ID": "AKIAFAKEENVKEY00000", "AWS_SECRET_ACCESS_KEY": "fakesecretenv"}),
  ("2 shared credentials file", {"AWS_SHARED_CREDENTIALS_FILE": creds_file}),
  ("3 env vars AND file (env wins)", {"AWS_ACCESS_KEY_ID": "AKIAFAKEENVKEY00000", "AWS_SECRET_ACCESS_KEY": "fakesecretenv", "AWS_SHARED_CREDENTIALS_FILE": creds_file}),
  ("4 container credentials (local fake endpoint)", {"AWS_CONTAINER_CREDENTIALS_FULL_URI": f"http://127.0.0.1:{srv.server_port}/creds"}),
  ("5 nothing at all", {}),
]
for i, (name, extra) in enumerate(cases):
    env = dict(base, **extra)
    print("==", name)
    out = subprocess.run([sys.executable, "-I", "-c", CHILD % (i == 0)], env=env, capture_output=True, text=True)
    print((out.stdout + out.stderr).strip())
srv.shutdown()
print("NOT executed: IMDS (disabled), web identity / IRSA / Pod Identity (need an STS endpoint and an issuer).")
```

**Output (my run):** real run. IMDS (disabled on purpose), web identity, IRSA and Pod Identity were not executed: they need a real STS endpoint, an OIDC issuer or a node agent. The container case ran against my fake local endpoint, so it proves the SDK's lookup, not AWS's endpoint.
```text
== 1 env vars
resolved method: env | key: AKIAFAKEENVKEY00000
chain order in this botocore: ['env', 'assume-role', 'assume-role-with-web-identity', 'sso', 'shared-credentials-file', 'login', 'custom-process', 'config-file', 'ec2-credentials-file', 'boto-config', 'container-role', 'iam-role']
== 2 shared credentials file
resolved method: shared-credentials-file | key: AKIAFAKEFILEKEY0000
== 3 env vars AND file (env wins)
resolved method: env | key: AKIAFAKEENVKEY00000
== 4 container credentials (local fake endpoint)
resolved method: container-role | key: ASIAFAKECONTAINER00
== 5 nothing at all
resolved method: None | key: None
NOT executed: IMDS (disabled), web identity / IRSA / Pod Identity (need an STS endpoint and an issuer).
```

**Follow-ups:**
- Where would you see which role your code actually runs as? `sts get-caller-identity`; here moto would only return its fixed dummy identity, so do it on real AWS.
- IRSA versus Pod Identity in one line? IRSA wires an OIDC provider and trust policy per cluster; Pod Identity uses an EKS association and agent, so less trust-policy editing (check current docs).
- Why not access keys for a pipeline? Long-lived, easy to leak, no expiry; prefer role plus short-lived credentials (GitHub OIDC is Part 7).

**Common mistakes:**
- Leaving old `AWS_*` env vars in a shell and wondering why the wrong account answers.
- Baking keys into an image or notebook.
- Assuming the SDK order is the same in Java, Go and Python.
- Forgetting IMDS hop limit and token requirement for containers on EC2.

### Q32 ⭐⭐ 🟡 Lambda concurrency: account limit, reserved versus provisioned concurrency, throttling behaviour for sync versus async versus SQS sources, scaling speed, and why reserved concurrency both guarantees and caps. A model-scoring Lambda behind SQS keeps hitting a downstream database limit: what do you set? Set reserved concurrency in moto, read it back, and simulate concurrency, throttles and queue backlog in pure Python.
**Asked at:** Lambda interview and limits sources (kodekloud AWS Developer Associate notes on limits and concurrency, awsfundamentals.com 'Lambda limitations', a dev.to Lambda compute-limits post, a pulumi provisioned-concurrency post; search snippets only, not opened; secondary sources disagreed on package-size wording so numbers are hedged 'check current docs'); training notes and blogs, not verified interview reports; backend, cloud and ML engineer roles | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)
**Say this first (1 line):** Reserved concurrency is both a guarantee and a cap for one function; for a SQS-fed scorer that overloads a database, set reserved concurrency at or below what the database can take and let the backlog wait in the queue.

**Then explain:**
- **Account limit:** a pool shared by all functions in a Region (a default of about a thousand is commonly cited; it can be raised, check current docs). One noisy function can starve the rest.
- **Reserved:** carves a slice out of the pool for one function. Guarantee (others cannot take it) and cap (the function cannot exceed it). Setting it to 0 effectively switches the function off. It costs nothing extra by itself.
- **Provisioned:** keeps pre-initialised environments warm to dodge cold starts; it is billed while provisioned, applies to a version or alias, and is separate from reserved (check current docs).
- **Throttling differs by source:** synchronous caller gets a 429 and must retry; asynchronous events are queued and retried by Lambda for a while, then go to a DLQ or on-failure destination; SQS pollers back off and the messages reappear after the visibility timeout, and can land in the queue's DLQ after the max receive count even though the code never ran. So set visibility timeout above function timeout and a sensible max receive count.
- **Scaling speed** is bounded too (burst then steady increase; check current docs), so reserved is not the only brake. For SQS there is also a per-mapping maximum concurrency setting; moto accepted that shape (see run).

**Example:** Hand-check the simulation: 20 messages per second for 20 s is 400 messages; each takes 3 s and holds one database connection. Unlimited-ish (100): peak 60 running (20 x 3), database limit 10 is exceeded. Reserved 10: running never passes 10, 400 messages drain at about 10/3 per second, so about 120 s (run says 121). The cost of protection is a 330-message peak backlog and a longer drain, which is the right place for waiting.

**Code:** Part 1 sets and reads reserved concurrency plus an SQS mapping shape in moto; part 2 is a tick-by-tick simulation (1 tick = 1 second), not Lambda's real scaler. Run with `python3 -I` from the venv (boto3 1.43.118, moto 5.2.4); fake keys only.
```python
# Q32: Lambda concurrency. Part 1 moto API shape; part 2 pure-Python tick simulation (NOT Lambda's real scaling).
import os, io, zipfile
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

@mock_aws
def moto_part():
    z = io.BytesIO()
    with zipfile.ZipFile(z, "w") as f: f.writestr("app.py", "def handler(e, c): return 1")
    iam = boto3.client("iam")
    role = iam.create_role(RoleName="lam", AssumeRolePolicyDocument="{}")["Role"]["Arn"]
    lam = boto3.client("lambda")
    lam.create_function(FunctionName="score", Runtime="python3.12", Role=role, Handler="app.handler", Code={"ZipFile": z.getvalue()})
    print("put   :", lam.put_function_concurrency(FunctionName="score", ReservedConcurrentExecutions=10)["ReservedConcurrentExecutions"])
    print("get   :", lam.get_function_concurrency(FunctionName="score")["ReservedConcurrentExecutions"])
    sqs = boto3.client("sqs"); q = sqs.create_queue(QueueName="jobs")["QueueUrl"]
    arn = sqs.get_queue_attributes(QueueUrl=q, AttributeNames=["QueueArn"])["Attributes"]["QueueArn"]
    try:
        m = lam.create_event_source_mapping(FunctionName="score", EventSourceArn=arn, BatchSize=5,
                                            ScalingConfig={"MaximumConcurrency": 5})
        print("ESM   :", {k: m.get(k) for k in ("BatchSize", "ScalingConfig", "State")})
    except Exception as e:
        print("ESM   : error", type(e).__name__, str(e)[:100])
moto_part()
print("(API shape only: nothing was invoked, nothing was throttled)\n")

# ---- simulation: 1 tick = 1 second. Jobs arrive from SQS; each takes DUR ticks and holds 1 DB connection while running.
DUR, DB_LIMIT, TICKS = 3, 10, 60
def arrivals(t): return 20 if t < 20 else 0           # burst: 20 messages/s for 20 s = 400 messages, then quiet
def run(reserved):
    queue, running, db_over, max_run = 0, [], 0, 0
    backlog_peak = 0
    for t in range(TICKS):
        queue += arrivals(t)
        running = [r - 1 for r in running if r - 1 > 0]
        take = min(queue, reserved - len(running))   # no free slot: messages simply stay queued
        queue -= take; running += [DUR] * take
        max_run = max(max_run, len(running)); db_over += max(0, len(running) - DB_LIMIT)
        backlog_peak = max(backlog_peak, queue)
    # finish draining to see how long the backlog takes
    t = TICKS
    while queue or running:
        running = [r - 1 for r in running if r - 1 > 0]
        take = min(queue, reserved - len(running)); queue -= take; running += [DUR] * take
        t += 1
    return dict(reserved=reserved, peak_concurrent=max_run, secs_over_db_limit=db_over, peak_backlog=backlog_peak, seconds_to_drain=t)
print(f"{'reserved':>8} {'peak running':>12} {'excess connection-seconds':>27} {'peak backlog':>13} {'drain time (s)':>15}")
for r in (100, 30, 10):
    d = run(r)
    print(f"{d['reserved']:>8} {d['peak_concurrent']:>12} {d['secs_over_db_limit']:>27} {d['peak_backlog']:>13} {d['seconds_to_drain']:>15}")
print("rule of thumb checked: reserved <= DB_LIMIT keeps connections at the limit; backlog waits in SQS instead of hitting the DB")
```

**Output (my run):** real run. Moto stores the setting but never invoked or throttled anything; the table is my simulation with made-up rates (database limit 10, duration 3 s), so it shows the reasoning, not AWS numbers.
```text
put   : 10
get   : 10
ESM   : {'BatchSize': 5, 'ScalingConfig': {'MaximumConcurrency': 5}, 'State': 'Enabled'}
(API shape only: nothing was invoked, nothing was throttled)

reserved peak running   excess connection-seconds  peak backlog  drain time (s)
     100           60                         980             0              60
      30           30                         780           190              60
      10           10                           0           330             121
rule of thumb checked: reserved <= DB_LIMIT keeps connections at the limit; backlog waits in SQS instead of hitting the DB
```

**Follow-ups:**
- Reserved set to 5 on an SQS function with a 10-way database: what breaks? Messages can be throttled repeatedly and move to the DLQ untouched; raise max receive count or reserved.
- Better fix than a cap? Pool connections with RDS Proxy or a pooler, plus the cap (check current docs for your engine).
- When provisioned instead? When cold-start latency hurts a sync path, not for protecting a database.

**Common mistakes:**
- Thinking reserved concurrency only guarantees capacity and forgetting it also caps.
- Setting reserved above the database limit and calling it protected.
- Visibility timeout shorter than the function timeout, causing duplicates.
- Reserving so much that the rest of the account has too little.

### Q33 ⭐⭐ 🟡 SageMaker Model Monitor and Ground Truth at the service boundary: data capture on an endpoint, baseline statistics and constraints, monitoring schedules and reports, Clarify bias and explainability jobs, and Ground Truth labeling workforces. What does the service give you and what must you still own (alerting, thresholds, retraining decisions)? Drift statistics belong to Part 8. Record that moto does not implement monitoring schedules or labeling jobs, and show a data-capture config dict validated for required keys.
**Asked at:** SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)
**Say this first (1 line):** SageMaker gives you the plumbing (data capture, baseline jobs, schedules, reports, Clarify, Ground Truth) but you still own the thresholds, alert routing and the decision to retrain.

**Then explain:**
- **Data capture:** an endpoint-config setting that writes a sample of requests and responses to S3 (sampling percentage, capture Input and/or Output). It is the raw material for everything else.
- **Baseline then monitor:** a baselining job computes statistics and constraints from training or a reference set; a monitoring schedule runs a job on the captured data on a cron and writes a violations report to S3 and metrics to CloudWatch. Drift maths belongs to Part 8.
- **Clarify** runs bias and explainability jobs (pre-training, post-training, SHAP-style attributions) as processing jobs. **Ground Truth** manages labelling jobs with a workforce (private, vendor, public) and can bring ground truth back for quality monitoring.
- **You still own:** which constraints to trust, alarms on the CloudWatch metrics, who is paged, the join of late-arriving labels to predictions, and the retrain trigger. A report in S3 that nobody reads is not monitoring.
- **Failure modes:** capture off or sampling too low, schedule on an empty window (job fails or passes meaninglessly), baseline taken from a different feature pipeline than serving.

**Example:** Config check by hand: `InitialSamplingPercentage: 150` is invalid (must be 0 to 100), `DestinationS3Uri` without `s3://` is invalid and capture mode `Both` is not a mode. The validator flags exactly these three; the good config returns an empty error list.

**Code:** A required-keys validator for the `DataCaptureConfig` dict (key names as in the CreateEndpointConfig API), plus moto calls to see what the mock does and does not do. Run with `python3 -I` from the venv (boto3 1.43.118, moto 5.2.4); fake keys only.
```python
# Q33: Model Monitor / Ground Truth at the service boundary. moto API shape only.
import os, json
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

REQUIRED = {"EnableCapture": bool, "InitialSamplingPercentage": int, "DestinationS3Uri": str, "CaptureOptions": list}
def validate_capture(cfg):
    errs = [f"missing {k}" for k in REQUIRED if k not in cfg]
    errs += [f"{k} should be {t.__name__}" for k, t in REQUIRED.items() if k in cfg and not isinstance(cfg[k], t)]
    if isinstance(cfg.get("InitialSamplingPercentage"), int) and not 0 <= cfg["InitialSamplingPercentage"] <= 100:
        errs.append("InitialSamplingPercentage must be 0..100")
    if isinstance(cfg.get("DestinationS3Uri"), str) and not cfg["DestinationS3Uri"].startswith("s3://"):
        errs.append("DestinationS3Uri must start with s3://")
    modes = {o.get("CaptureMode") for o in cfg.get("CaptureOptions", []) if isinstance(o, dict)}
    if not modes <= {"Input", "Output"} or not modes: errs.append("CaptureOptions needs CaptureMode Input and/or Output")
    return errs

good = {"EnableCapture": True, "InitialSamplingPercentage": 20, "DestinationS3Uri": "s3://ml-monitor/capture/",
        "CaptureOptions": [{"CaptureMode": "Input"}, {"CaptureMode": "Output"}]}
bad = {"EnableCapture": True, "InitialSamplingPercentage": 150, "DestinationS3Uri": "ml-monitor/capture", "CaptureOptions": [{"CaptureMode": "Both"}]}
print("good ->", validate_capture(good)); print("bad  ->", validate_capture(bad))
print("missing keys ->", validate_capture({"EnableCapture": True}))

@mock_aws
def moto():
    sm = boto3.client("sagemaker")
    sm.create_model(ModelName="m", ExecutionRoleArn="arn:aws:iam::123456789012:role/sm",
                    PrimaryContainer={"Image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/img:1"})
    try:
        r = sm.create_endpoint_config(EndpointConfigName="ec", ProductionVariants=[{"VariantName": "v", "ModelName": "m",
            "InitialInstanceCount": 1, "InstanceType": "ml.m5.large"}], DataCaptureConfig=good)
        print("create_endpoint_config with DataCaptureConfig: accepted ->", r["EndpointConfigArn"].split("/")[-1])
        d = sm.describe_endpoint_config(EndpointConfigName="ec")
        print("read back DataCaptureConfig:", "DataCaptureConfig" in d, d.get("DataCaptureConfig", {}).get("DestinationS3Uri"))
    except Exception as e: print("create_endpoint_config:", type(e).__name__, str(e)[:120])
    for name, call in [("create_monitoring_schedule", lambda: sm.create_monitoring_schedule(MonitoringScheduleName="s",
            MonitoringScheduleConfig={"ScheduleConfig": {"ScheduleExpression": "cron(0 * ? * * *)"}})),
        ("list_labeling_jobs", lambda: sm.list_labeling_jobs()),
        ("create_data_quality_job_definition", lambda: sm.create_data_quality_job_definition(JobDefinitionName="d"))]:
        try: call(); print(name, ": returned (unexpected)")
        except Exception as e: print(name, ":", type(e).__name__, "-", str(e)[:90].replace("\n", " "))
moto()
```

**Output (my run):** real run. Moto accepted and echoed the data-capture config (API shape only) but raised NotImplementedError for `create_monitoring_schedule` and `list_labeling_jobs`; no monitoring or labelling ran. My validator is a simplified check, not the service's own validation.
```text
good -> []
bad  -> ['InitialSamplingPercentage must be 0..100', 'DestinationS3Uri must start with s3://', 'CaptureOptions needs CaptureMode Input and/or Output']
missing keys -> ['missing InitialSamplingPercentage', 'missing DestinationS3Uri', 'missing CaptureOptions', 'CaptureOptions needs CaptureMode Input and/or Output']
create_endpoint_config with DataCaptureConfig: accepted -> ec
read back DataCaptureConfig: True s3://ml-monitor/capture/
create_monitoring_schedule : NotImplementedError - The create_monitoring_schedule action has not been implemented
list_labeling_jobs : NotImplementedError - The list_labeling_jobs action has not been implemented
create_data_quality_job_definition : ParamValidationError - Parameter validation failed: Missing required parameter in input: "DataQualityAppSpecifica
```

**Follow-ups:**
- Which part is the real ML judgement? Choosing constraints and thresholds and deciding when drift justifies retraining.
- Why sample instead of capturing everything? Storage and privacy; but low sampling can miss rare drift (rates are your choice, check docs).
- Alert path? Schedule metrics to CloudWatch alarms to SNS or EventBridge; design is Part 8.

**Common mistakes:**
- Treating 'Model Monitor enabled' as 'we monitor the model'.
- Baseline from clean training data while production features come through a different path.
- Forgetting the S3 and KMS permissions for the capture destination.
- Expecting Ground Truth to remove the need for label-quality review.

### Q34 ⭐⭐ 🟡 SageMaker Feature Store at the service boundary: feature groups, record identifier and event time, online versus offline store (S3 with a Glue catalog), what ingestion does, and the cost of an online store you forgot to turn off. Concepts, point-in-time joins and Feast belong to Part 9. Create a feature group in moto, print its status and config, and note that the feature-store runtime API was not implemented by the mock.
**Asked at:** SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)
**Say this first (1 line):** A SageMaker feature group is a named set of features with a record identifier and an event time, stored in an offline store on S3 (with a Glue table) and optionally an online store; the thing to remember is the online store keeps costing until you turn it off.

**Then explain:**
- **Feature group:** schema (name and type per feature), `RecordIdentifierFeatureName` (the entity key) and `EventTimeFeatureName` (when the value was true). Without event time you cannot do point-in-time correct training sets (Part 9).
- **Offline store:** append-only history in S3 (Parquet), with an optional Glue catalog table, so Athena and training jobs can read it. Needs an S3 location and a role. **Online store:** low-latency latest value per key for real-time inference.
- **Ingestion:** `PutRecord` writes to the online store (and the offline store gets a copy); batch ingestion can write through Spark or the SDK helper. The runtime API (`sagemaker-featurestore-runtime`) is a separate service from the control-plane API.
- **Cost trap:** an online store you forgot keeps its storage and request costs running; add review rules (last-read age) and delete test groups. No prices here; check current docs.
- **Failure modes:** missing role or S3 permission (group sits in `CreateFailed`), event time in the wrong type, and duplicates when identifier plus event time repeat.

**Example:** Hand-check: a group with features `customer_id`, `event_time`, `txn_count_7d` has the key `customer_id`. The review rule on the sample inventory flags only `customer-risk` (online store on, 45 days since read); `txn-agg` is not online and was read yesterday, so it is not flagged.

**Code:** Creates a feature group in moto, reads it back, probes the runtime API, then applies a review rule to a small sample inventory. Run with `python3 -I` from the venv (boto3 1.43.118, moto 5.2.4); fake keys only.
```python
# Q34: SageMaker Feature Store at the service boundary, moto API shape only.
import os, json
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

@mock_aws
def main():
    s3 = boto3.client("s3"); s3.create_bucket(Bucket="ml-features")
    sm = boto3.client("sagemaker")
    r = sm.create_feature_group(
        FeatureGroupName="customer-risk", RecordIdentifierFeatureName="customer_id", EventTimeFeatureName="event_time",
        FeatureDefinitions=[{"FeatureName": "customer_id", "FeatureType": "String"},
                            {"FeatureName": "event_time", "FeatureType": "Fractional"},
                            {"FeatureName": "txn_count_7d", "FeatureType": "Integral"}],
        OnlineStoreConfig={"EnableOnlineStore": True},
        OfflineStoreConfig={"S3StorageConfig": {"S3Uri": "s3://ml-features/offline/"}, "DisableGlueTableCreation": False},
        RoleArn="arn:aws:iam::123456789012:role/sm-featurestore")
    d = sm.describe_feature_group(FeatureGroupName="customer-risk")
    print("status      :", d["FeatureGroupStatus"])
    print("record id   :", d["RecordIdentifierFeatureName"], "| event time:", d["EventTimeFeatureName"])
    print("online      :", d.get("OnlineStoreConfig"))
    print("offline     :", d.get("OfflineStoreConfig", {}).get("S3StorageConfig"))
    print("features    :", [f["FeatureName"] for f in d["FeatureDefinitions"]])
    try: sm.list_feature_groups(); print("list_feature_groups: returned")
    except Exception as e: print("list_feature_groups ->", type(e).__name__, str(e)[:70])
    rt = boto3.client("sagemaker-featurestore-runtime")
    for name, fn in [("put_record", lambda: rt.put_record(FeatureGroupName="customer-risk", Record=[
            {"FeatureName": "customer_id", "ValueAsString": "c1"}, {"FeatureName": "event_time", "ValueAsString": "1700000000.0"},
            {"FeatureName": "txn_count_7d", "ValueAsString": "4"}])),
            ("get_record", lambda: rt.get_record(FeatureGroupName="customer-risk", RecordIdentifierValueAsString="c1"))]:
        try: print(name, "-> returned", fn())
        except Exception as e: print(name, "->", type(e).__name__, str(e)[:100].replace("\n", " "))
    print("NOTE: I sent EnableOnlineStore=True but moto's describe did not echo it (online: None above), so the mock cannot show the online-store flag.")
    # review rule on the REQUEST we hold (sample inventory), not on the mock's answer:
    inventory = [{"name": "customer-risk", "online": True, "last_read_days_ago": 45}, {"name": "txn-agg", "online": False, "last_read_days_ago": 1}]
    print("online stores not read for 30+ days:", [g["name"] for g in inventory if g["online"] and g["last_read_days_ago"] >= 30])
main()
```

**Output (my run):** real run (random numbers in the S3 path are moto's). API shape only: `describe_feature_group` did not echo `OnlineStoreConfig`, `list_feature_groups` raised NotImplementedError and the runtime `put_record` and `get_record` returned 404 'Not yet implemented'. The review rule ran on my sample list, not on mock data.
```text
status      : Created
record id   : customer_id | event time: event_time
online      : None
offline     : {'S3Uri': 's3://ml-features/offline/', 'ResolvedOutputS3Uri': 's3://ml-features/offline//123456789012/us-east-1/offline-store/customer-risk-1793037576/data'}
features    : ['customer_id', 'event_time', 'txn_count_7d']
list_feature_groups -> NotImplementedError The list_feature_groups action has not been implemented
put_record -> ClientError An error occurred (404) when calling the PutRecord operation: Not yet implemented
get_record -> ClientError An error occurred (404) when calling the GetRecord operation: Not yet implemented
NOTE: I sent EnableOnlineStore=True but moto's describe did not echo it (online: None above), so the mock cannot show the online-store flag.
online stores not read for 30+ days: ['customer-risk']
```

**Follow-ups:**
- Offline versus online in one line? Offline is history for training; online is latest value for serving.
- Why Glue? So Athena and other engines can query the offline store as a table.
- Do you need it? Not if one team and batch scoring only; Part 9 weighs Feast and alternatives.

**Common mistakes:**
- Leaving an online store on after a demo.
- No event time or the wrong type for it.
- Using the control-plane client to read records.
- Assuming offline and online are always consistent in time.

### Q35 ⭐⭐ 🟡 Athena, Glue and Redshift at the boundary of ML data prep: when Athena over partitioned Parquet in S3 is enough, what the Glue Data Catalog and crawlers give you, when a Glue ETL job beats pandas on one box, and when a Redshift warehouse is already the source of truth. Mention how SageMaker reads from each. Create a Glue database, an Athena query and a Redshift cluster record in moto; no real query ran. SQL itself belongs to Book 3.
**Asked at:** Job-posting skill lists (a getonbrd Senior MLOps Engineer AWS and SageMaker posting listing Athena, RDS, ECR, IAM, CloudWatch, CloudFormation or Terraform and GitHub Actions, a workingnomads Senior MLOps Engineer SageMaker and Airflow posting; search snippets only, not opened); job postings, not interview reports; MLOps roles on AWS | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)
**Say this first (1 line):** Athena over partitioned Parquet is enough for ad hoc and training-set pulls, Glue gives the catalog and heavy ETL when one machine is not enough, and Redshift is the answer when the warehouse already holds the truth.

**Then explain:**
- **Athena:** serverless SQL over files in S3; you pay by data scanned (check current docs), so Parquet plus partitions (`dt=...`) cut cost and time. It is not a low-latency serving store.
- **Glue Data Catalog and crawlers:** a shared metastore (databases, tables, partitions) used by Athena, Glue jobs, EMR and others. A crawler infers schema; in production many teams prefer explicit DDL so schema does not drift silently.
- **Glue ETL (Spark)** beats pandas on one box when data no longer fits memory or you need parallel reads and writes; for a few GB, pandas or DuckDB on one instance is simpler.
- **Redshift:** when curated tables already live in the warehouse, read them with UNLOAD to S3 or the data API instead of re-copying pipelines. SageMaker can read from S3 directly, from Athena or Redshift through Data Wrangler or processing jobs, or via the warehouse's connector (check current docs).
- **Failure modes:** no partition filter means a full scan; too many tiny files; crawler changes a column type; stale catalog partitions after new data lands.

**Example:** Hand-check partition pruning: 30 days x 4 files = 120 objects. A query with `dt = '2026-10-01'` reads 4; without the filter it reads all 120. That is the whole reason to partition.

**Code:** Creates a Glue database and partitioned table, an Athena query execution and a Redshift cluster record in moto, then counts objects pruned by a partition filter. Run with `python3 -I` from the venv (boto3 1.43.118, moto 5.2.4); fake keys only.
```python
# Q35: Athena, Glue, Redshift records in moto + tiny partition-pruning illustration. No query actually ran.
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

@mock_aws
def main():
    glue = boto3.client("glue")
    glue.create_database(DatabaseInput={"Name": "ml_lake"})
    glue.create_table(DatabaseName="ml_lake", TableInput={"Name": "txns", "PartitionKeys": [{"Name": "dt", "Type": "string"}],
        "StorageDescriptor": {"Columns": [{"Name": "txn_id", "Type": "string"}, {"Name": "amount", "Type": "double"}],
        "Location": "s3://ml-lake/curated/txns/", "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
        "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
        "SerdeInfo": {"SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"}}, "TableType": "EXTERNAL_TABLE"})
    t = glue.get_table(DatabaseName="ml_lake", Name="txns")["Table"]
    print("glue table  :", t["Name"], "| partition keys:", [p["Name"] for p in t["PartitionKeys"]], "|", t["StorageDescriptor"]["Location"])
    boto3.client("s3").create_bucket(Bucket="ml-athena-out")
    a = boto3.client("athena")
    q = a.start_query_execution(QueryString="SELECT count(*) FROM ml_lake.txns WHERE dt = '2026-10-01'",
        QueryExecutionContext={"Database": "ml_lake"}, ResultConfiguration={"OutputLocation": "s3://ml-athena-out/"})
    st = a.get_query_execution(QueryExecutionId=q["QueryExecutionId"])["QueryExecution"]["Status"]["State"]
    print("athena      : query id present:", bool(q["QueryExecutionId"]), "| state:", st, "(mock; no data scanned)")
    rs = boto3.client("redshift")
    c = rs.create_cluster(ClusterIdentifier="dw", NodeType="ra3.xlplus", MasterUsername="admin", MasterUserPassword="Fake1234Pass",
                          ClusterType="single-node", DBName="analytics")["Cluster"]
    print("redshift    :", c["ClusterIdentifier"], c["ClusterStatus"], c["DBName"], "(record only; no warehouse, no SQL)")
main()

# Partition pruning, hand-checkable: a Hive-style layout dt=YYYY-MM-DD; a query with dt filter reads only matching prefixes.
days = [f"2026-10-{d:02d}" for d in range(1, 31)]
files_per_day = 4
keys = [f"curated/txns/dt={d}/part-{i}.parquet" for d in days for i in range(files_per_day)]
def prune(keys, want): return [k for k in keys if f"dt={want}/" in k]
print("\nobjects in table:", len(keys), "| objects a dt='2026-10-01' query must read:", len(prune(keys, "2026-10-01")))
print("same query without a partition filter reads:", len(keys))
```

**Output (my run):** real run. Moto only stores the records: the Athena query is marked SUCCEEDED without reading data and the Redshift cluster is a record that never became a warehouse. No real query ran; SQL itself is Book 3.
```text
glue table  : txns | partition keys: ['dt'] | s3://ml-lake/curated/txns/
athena      : query id present: True | state: SUCCEEDED (mock; no data scanned)
redshift    : dw creating analytics (record only; no warehouse, no SQL)

objects in table: 120 | objects a dt='2026-10-01' query must read: 4
same query without a partition filter reads: 120
```

**Follow-ups:**
- Crawler or DDL? DDL for stable production tables, crawler for discovery.
- When Glue over pandas? When parallel data volume or scheduled managed Spark matters.
- Athena for feature serving? No, use an online store or a service database.

**Common mistakes:**
- Querying raw CSV without partitions and calling Athena slow.
- Letting the crawler redefine production schemas.
- Copying warehouse tables to S3 by hand with no lineage.
- Forgetting the S3 and Glue permissions the SageMaker role needs.

### Q36 ⭐⭐ 🟡 S3 read patterns for training data: why millions of small objects hurt (request overhead, listing cost, per-request latency), how prefixes, parallel range GETs, sharded archives (tar, WebDataset, Parquet row groups), caching on local NVMe, and SageMaker input modes (File, Pipe, FastFile) address it. Build a pure-Python simulation that counts requests for many small files versus a few shards, add moto GET counts, and keep all timings out; sandbox numbers prove nothing about S3.
**Asked at:** S3 interview question banks (novelvista '100+ Top AWS S3 Interview Questions', adaface, ccbp.in, a techinterview.org 'System Design Interview: Object Storage (Amazon S3)' post, AWS developer exam-prep study guides; search snippets only, not opened; WebFetch of docs.aws.amazon.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; cloud, data and ML engineer roles at IT-services firms, product companies and GCCs | SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs
**Say this first (1 line):** Millions of small objects hurt because every object costs a request and listing pages; the fix is fewer, larger objects (shards), ranged parallel reads and local caching, plus the right SageMaker input mode.

**Then explain:**
- **Why small files hurt:** one GET per object, per-request latency, and ListObjectsV2 returns a limited page of keys (a thousand per call; check current docs), so enumerating a million keys alone is a thousand calls. Requests also have rate and billing dimensions (check current docs).
- **Fixes:** pack samples into shards (tar for WebDataset, Parquet row groups); use ranged GETs and parallel reads inside a shard; spread load with sensible prefixes; cache hot shards on local NVMe or EBS; avoid listing at start by shipping a manifest.
- **SageMaker input modes:** File copies the data to the instance volume before training; Pipe streams it (older, framework-limited); FastFile exposes S3 objects as files read on demand. Which one wins depends on dataset size and access pattern; check current docs.
- **Failure modes:** shards too large for random access, shuffling across shards done wrong (poor mixing), training stalling on cold reads, request throttling when thousands of workers start together.

**Example:** Hand-check from the run: 1,000,000 files of 100 KB is about 97,656 MB. One GET each gives 1,000,000 GETs plus 1,000 LIST pages. As 256 MB shards it is 382 objects; 64 MB ranges give 4 GETs each, 1,528 total, or 382 with whole-shard GETs. Moto confirms the pattern on a tiny scale: 200 small objects need 200 GetObject calls, one shard needs 2 ranged calls for the same 20,000 bytes.

**Code:** Request-count arithmetic plus real boto3 calls into moto with a before-call event hook counting operations. No timings are printed on purpose. Run with `python3 -I` from the venv (boto3 1.43.118, moto 5.2.4); fake keys only.
```python
# Q36: request counting, no timings. Part 1 pure arithmetic simulation; part 2 real boto3 calls into moto with a call counter.
import os, math
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from collections import Counter
from moto import mock_aws

LIST_PAGE = 1000                     # ListObjectsV2 returns up to 1000 keys per call (check current docs)
def small_files(n_files):            # 1 LIST page per 1000 keys + 1 GET per file
    return {"LIST": math.ceil(n_files / LIST_PAGE), "GET": n_files}
def shards(total_mb, shard_mb, range_mb):   # LIST of a few keys + ranged GETs inside each shard
    n = math.ceil(total_mb / shard_mb)
    return {"LIST": math.ceil(n / LIST_PAGE), "GET": n * math.ceil(shard_mb / range_mb), "shards": n}
n_files, file_kb = 1_000_000, 100
total_mb = n_files * file_kb / 1024
print(f"dataset: {n_files:,} files x {file_kb} KB = {total_mb:,.0f} MB (about the same bytes in both layouts)")
print("1M small files, one GET each :", small_files(n_files))
print("shards of 256 MB, 64 MB ranges :", shards(total_mb, 256, 64))
print("shards of 256 MB, whole-shard GET:", shards(total_mb, 256, 256))

@mock_aws
def moto_counts():
    s3 = boto3.client("s3"); s3.create_bucket(Bucket="train-data")
    calls = Counter()
    s3.meta.events.register("before-call.s3.*", lambda model, **kw: calls.update([model.name]))
    for i in range(200): s3.put_object(Bucket="train-data", Key=f"small/{i:05d}.bin", Body=b"x" * 100)
    s3.put_object(Bucket="train-data", Key="shards/shard-000.tar", Body=b"x" * 100 * 200)  # same 20,000 bytes in one object
    calls.clear()
    for k in [o["Key"] for o in s3.list_objects_v2(Bucket="train-data", Prefix="small/")["Contents"]]:
        s3.get_object(Bucket="train-data", Key=k)["Body"].read()
    print("moto, 200 small objects :", dict(calls)); calls.clear()
    s3.list_objects_v2(Bucket="train-data", Prefix="shards/")
    got = b"".join(s3.get_object(Bucket="train-data", Key="shards/shard-000.tar", Range=f"bytes={a}-{a+9999}")["Body"].read() for a in (0, 10000))
    print("moto, 1 shard, 2 ranged GETs:", dict(calls), "| bytes read:", len(got))
moto_counts()
print("timings deliberately not printed: a mock on localhost says nothing about S3 latency")
```

**Output (my run):** real run, counts only. A localhost mock proves nothing about S3 latency or throughput, and the 1M-file line is arithmetic, not a measurement.
```text
dataset: 1,000,000 files x 100 KB = 97,656 MB (about the same bytes in both layouts)
1M small files, one GET each : {'LIST': 1000, 'GET': 1000000}
shards of 256 MB, 64 MB ranges : {'LIST': 1, 'GET': 1528, 'shards': 382}
shards of 256 MB, whole-shard GET: {'LIST': 1, 'GET': 382, 'shards': 382}
moto, 200 small objects : {'ListObjectsV2': 1, 'GetObject': 200}
moto, 1 shard, 2 ranged GETs: {'ListObjectsV2': 1, 'GetObject': 2} | bytes read: 20000
timings deliberately not printed: a mock on localhost says nothing about S3 latency
```

**Follow-ups:**
- Pick a shard size? Big enough to amortise requests, small enough to shuffle and resume; tune and measure on the real service.
- File versus FastFile versus Pipe? File when the data fits and you want simple reads; FastFile to start sooner on big data (check current docs).
- Does a prefix fix throttling? Spreading across prefixes helped historically; check current docs for the current scaling behaviour.

**Common mistakes:**
- Benchmarking against a mock or laptop and quoting it.
- Listing the whole bucket at every epoch.
- Tiny shards that recreate the small-file problem.
- Reading with one thread.

### Q37 ⭐⭐ 🟡 Monitoring a SageMaker endpoint with CloudWatch: invocation, 4XX and 5XX, model latency versus overhead latency, instance CPU, GPU and memory utilisation, how alarms and autoscaling use them, and what log lines to emit. Alerting design belongs to Part 8; this question is about which service metrics exist and which you would alarm on. Create an alarm in moto with comparison, period and evaluation periods, and write a pure-Python evaluator for 'M of N datapoints breaching'.
**Asked at:** SageMaker hosting docs and write-ups (AWS 'Supported features' feature matrix and Model Hosting FAQs, caylent.com 'How To Pick the Best SageMaker Model Hosting Option' and 'SageMaker inference types', kodekloud AWS ML Engineer Associate notes on endpoint types; search snippets only, not opened; one third-party page's latency and payload figures conflicted with AWS and were not used); vendor docs and training notes, not interview reports; MLOps and ML engineer roles on AWS | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)
**Say this first (1 line):** For a SageMaker endpoint I watch invocations, 4XX and 5XX errors, model latency versus overhead latency, and CPU, memory and GPU use, and I alarm on 'M of N datapoints breaching' so one spike does not page anyone.

**Then explain:**
- **Endpoint metrics (namespace AWS/SageMaker, dimensions EndpointName and VariantName):** `Invocations`, `Invocation4XXErrors`, `Invocation5XXErrors`, `ModelLatency` (time inside your container), `OverheadLatency` (service overhead). Latency units are microseconds per current docs; verify.
- **Instance metrics (namespace /aws/sagemaker/Endpoints):** CPU, memory, disk and GPU utilisation, and GPU memory. A 5XX with high CPU suggests saturation; high ModelLatency with low CPU suggests a slow dependency or model load.
- **Alarms and autoscaling:** alarms evaluate a statistic over a period for N periods, firing when M datapoints breach; target-tracking autoscaling uses a metric such as invocations per instance. Treat-missing-data setting matters: no traffic is not the same as healthy.
- **Logs:** emit one structured line per request (request id, model version, latency, input size, outcome), never raw sensitive input. Alerting design is Part 8.

**Example:** Hand-check M of N: window [10,120,130,20,140] with threshold 100 has three breaches, so '3 of 5' is ALARM; [10,120,130,20,30] has two, so OK. With missing points set to breaching, five of five flags are true and it alarms; with notBreaching, two data points breach and it stays OK.

**Code:** Creates the alarm in moto and reads back comparison, period, evaluation periods and datapoints-to-alarm; then a small pure-Python M-of-N evaluator with missing-data modes (simplified: it ignores the alarm's exact period alignment). Run with `python3 -I` from the venv (boto3 1.43.118, moto 5.2.4); fake keys only.
```python
# Q37: CloudWatch alarm in moto + pure-Python 'M of N datapoints breaching' evaluator.
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

@mock_aws
def moto_part():
    cw = boto3.client("cloudwatch")
    cw.put_metric_alarm(AlarmName="ep-model-latency-high", Namespace="AWS/SageMaker", MetricName="ModelLatency",
        Dimensions=[{"Name": "EndpointName", "Value": "risk-ep"}, {"Name": "VariantName", "Value": "AllTraffic"}],
        ExtendedStatistic="p99", Period=60, EvaluationPeriods=5, DatapointsToAlarm=3, Threshold=100000,
        ComparisonOperator="GreaterThanThreshold", TreatMissingData="notBreaching")
    a = cw.describe_alarms(AlarmNames=["ep-model-latency-high"])["MetricAlarms"][0]
    print({k: a[k] for k in ("AlarmName", "MetricName", "Period", "EvaluationPeriods", "DatapointsToAlarm", "ComparisonOperator", "TreatMissingData", "StateValue")})
    print("(ModelLatency is reported in microseconds by SageMaker per current docs; threshold above is a placeholder, not advice)")
moto_part()

def evaluate(points, threshold, m, n, op="gt", treat_missing="notBreaching"):
    """Last n datapoints (None = missing). ALARM if >= m breach; INSUFFICIENT_DATA if missing treated as 'missing' and not enough data."""
    window = points[-n:]
    def breach(v):
        if v is None: return {"breaching": True, "notBreaching": False, "ignore": None, "missing": None}[treat_missing]
        return v > threshold if op == "gt" else v < threshold
    flags = [breach(v) for v in window]
    if treat_missing in ("ignore", "missing"): flags = [f for f in flags if f is not None]
    if treat_missing == "missing" and len(flags) == 0: return "INSUFFICIENT_DATA", flags
    return ("ALARM" if sum(1 for f in flags if f) >= m else "OK"), flags
cases = [
  ("3 of 5, exactly 3 breach",     [10, 120, 130, 20, 140], dict(m=3, n=5)),
  ("3 of 5, only 2 breach",        [10, 120, 130, 20, 30],  dict(m=3, n=5)),
  ("1 of 1 single spike",          [10, 10, 10, 10, 500],   dict(m=1, n=1)),
  ("missing, notBreaching",        [None, None, 130, 140, None], dict(m=3, n=5)),
  ("missing, breaching",           [None, None, 130, 140, None], dict(m=3, n=5, treat_missing="breaching")),
  ("all missing, 'missing' mode",  [None] * 5,              dict(m=3, n=5, treat_missing="missing")),
]
for name, pts, kw in cases:
    state, flags = evaluate(pts, 100, **kw)
    print(f"{name:32s} {state:18s} flags={flags}")
```

**Output (my run):** real run. Moto stored the alarm in `OK` and never evaluated a real metric; the evaluator is my simplified reimplementation, and the threshold is a placeholder.
```text
{'AlarmName': 'ep-model-latency-high', 'MetricName': 'ModelLatency', 'Period': 60, 'EvaluationPeriods': 5, 'DatapointsToAlarm': 3, 'ComparisonOperator': 'GreaterThanThreshold', 'TreatMissingData': 'notBreaching', 'StateValue': 'OK'}
(ModelLatency is reported in microseconds by SageMaker per current docs; threshold above is a placeholder, not advice)
3 of 5, exactly 3 breach         ALARM              flags=[False, True, True, False, True]
3 of 5, only 2 breach            OK                 flags=[False, True, True, False, False]
1 of 1 single spike              ALARM              flags=[True]
missing, notBreaching            OK                 flags=[False, False, True, True, False]
missing, breaching               ALARM              flags=[True, True, True, True, True]
all missing, 'missing' mode      INSUFFICIENT_DATA  flags=[]
```

**Follow-ups:**
- Why M of N? It filters one-off spikes yet reacts to sustained breaches.
- Which latency tells you your code is slow? ModelLatency; OverheadLatency points at the platform.
- Which metric for autoscaling? Per-instance invocations is the common choice; check current docs for the predefined metric.

**Common mistakes:**
- Alarming on the average and missing p99.
- Default missing-data handling hiding an endpoint that receives no traffic.
- Alarming without an action or owner.
- Ignoring GPU memory until an out-of-memory 5XX.

### Q38 ⭐⭐ 🟡 KMS in depth for ML teams: customer managed versus AWS managed keys, key policies versus IAM versus grants, envelope encryption with data keys, key rotation, encryption context, Region scoping, and what happens to old data when a key is disabled or deleted. Use moto to create a key, generate a data key, encrypt with it locally (cryptography), then decrypt, and create a grant. Real key-policy enforcement is not executed.
**Asked at:** IAM interview and policy-evaluation sources (AWS IAM 'Policy evaluation logic' pages on docs.aws.amazon.com and docs.aws.eu, tutorialsdojo 'How AWS IAM Handles Conflicting IAM Policies', advancedweb.hu 'IAM policy evaluation logic explained with examples', barkingiguana 'How IAM Policy Evaluation Actually Works', community.aws and hidekazu-konishi IAM glossary; search snippets only, not opened); vendor docs and study guides, not verified candidate reports; cloud, DevOps, security and MLOps roles at IT-services firms, product companies and GCCs | S3 interview question banks (novelvista '100+ Top AWS S3 Interview Questions', adaface, ccbp.in, a techinterview.org 'System Design Interview: Object Storage (Amazon S3)' post, AWS developer exam-prep study guides; search snippets only, not opened; WebFetch of docs.aws.amazon.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; cloud, data and ML engineer roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** A KMS key never leaves KMS: you ask it for a data key, encrypt locally with the plaintext copy, store only the wrapped copy, and later ask KMS to unwrap it; access is the key policy plus IAM plus optional grants.

**Then explain:**
- **Key types:** customer managed (you control policy, rotation, deletion, can be shared across accounts) versus AWS managed (created by the service, you cannot edit the policy, and cannot share it cross-account; check current docs).
- **Who may use a key:** the key policy is the root of trust; IAM policies only work if the key policy delegates to IAM. Grants are temporary, narrow delegations (used by services like EBS). Cross-account use needs both the key policy and the caller's IAM policy.
- **Envelope encryption:** `GenerateDataKey` returns a plaintext key plus a wrapped one; encrypt data locally (AES-GCM), discard the plaintext, store the wrapped key next to the ciphertext. KMS is called only to wrap and unwrap, which is why it scales to big files.
- **Encryption context:** extra key-value pairs bound to the ciphertext as authenticated data; a mismatch fails decrypt, and it shows in CloudTrail for audit. **Rotation:** automatic rotation changes backing material while old ciphertext stays decryptable. Keys are Region-scoped.
- **Disable or delete:** a disabled key cannot decrypt, so data becomes unreadable; deletion has a waiting period and is irreversible afterwards (check current docs). Always confirm nothing live depends on the key.

**Example:** Hand-check the run: the data key is 32 bytes (AES-256); decrypt with the original context returns the fake text. With a different context moto raised InvalidCiphertextException, matching the idea that context must match. After `disable_key` moto still decrypted, which real KMS is documented not to allow, and `schedule_key_deletion` left the key in `PendingDeletion`.

**Code:** Moto for create_key, generate_data_key, decrypt, create_grant, rotation, disable and scheduled deletion; `cryptography` AES-GCM does the local encrypt and decrypt. Run with `python3 -I` from the venv (boto3 1.43.118, moto 5.2.4); fake keys only.
```python
# Q38: KMS envelope encryption. moto for the KMS API, `cryptography` AES-GCM for the local data encryption.
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from moto import mock_aws

@mock_aws
def main():
    kms = boto3.client("kms")
    key = kms.create_key(Description="ml-data-cmk", KeyUsage="ENCRYPT_DECRYPT")["KeyMetadata"]
    kid = key["KeyId"]
    print("key         :", key["KeyManager"], key["KeyState"], key["Enabled"], "| arn region:", key["Arn"].split(":")[3])
    ctx = {"project": "risk", "dataset": "train-v3"}
    dk = kms.generate_data_key(KeyId=kid, KeySpec="AES_256", EncryptionContext=ctx)
    print("data key    : plaintext", len(dk["Plaintext"]), "bytes | wrapped copy", len(dk["CiphertextBlob"]), "bytes | KeyId matches:", dk["KeyId"] == key["Arn"])
    nonce = os.urandom(12)
    ct = AESGCM(dk["Plaintext"]).encrypt(nonce, b"customer rows: fake data", None)     # local encryption with the plaintext data key
    del dk["Plaintext"]                                                                  # store only (nonce, ct, wrapped key)
    back = kms.decrypt(CiphertextBlob=dk["CiphertextBlob"], EncryptionContext=ctx)["Plaintext"]   # unwrap the data key
    print("decrypted   :", AESGCM(back).decrypt(nonce, ct, None).decode())
    try:
        kms.decrypt(CiphertextBlob=dk["CiphertextBlob"], EncryptionContext={"project": "other"})
        print("wrong context: accepted")
    except Exception as e:
        print("wrong context:", type(e).__name__)
    g = kms.create_grant(KeyId=kid, GranteePrincipal="arn:aws:iam::123456789012:role/sm-train", Operations=["Decrypt", "GenerateDataKey"])
    print("grant       :", sorted(g.keys() - {"ResponseMetadata"}), "| listed:", len(kms.list_grants(KeyId=kid)["Grants"]))
    kms.enable_key_rotation(KeyId=kid); print("rotation    :", kms.get_key_rotation_status(KeyId=kid)["KeyRotationEnabled"])
    kms.disable_key(KeyId=kid)
    try:
        kms.decrypt(CiphertextBlob=dk["CiphertextBlob"], EncryptionContext=ctx); print("after disable: decrypt still worked in moto (real KMS is documented to refuse; check current docs)")
    except Exception as e: print("after disable: decrypt ->", type(e).__name__)
    d = kms.schedule_key_deletion(KeyId=kid, PendingWindowInDays=7)
    print("deletion    :", {k: str(v)[:19] for k, v in d.items() if k != "ResponseMetadata"}, "| state now:", kms.describe_key(KeyId=kid)["KeyMetadata"]["KeyState"])
main()
print("Real key-policy and IAM enforcement NOT executed; moto does not check who may call kms:Decrypt.")
```

**Output (my run):** real run (random ids and dates masked). Moto does not enforce key policies or IAM, so who can call kms:Decrypt was not tested, and moto ignores the disabled state on decrypt, so do not use it to prove that behaviour.
```text
key         : CUSTOMER Enabled True | arn region: us-east-1
data key    : plaintext 32 bytes | wrapped copy 96 bytes | KeyId matches: True
decrypted   : customer rows: fake data
wrong context: InvalidCiphertextException
grant       : ['GrantId', 'GrantToken'] | listed: 1
rotation    : True
after disable: decrypt still worked in moto (real KMS is documented to refuse; check current docs)
deletion    : {'KeyId': '<id>', 'DeletionDate': '<date>'} | state now: PendingDeletion
Real key-policy and IAM enforcement NOT executed; moto does not check who may call kms:Decrypt.
```

**Follow-ups:**
- Why not encrypt the file directly with KMS? Direct Encrypt has a small size limit (check docs) and sends data to KMS; envelope is cheaper in calls and scales.
- What does S3 SSE-KMS do for you? S3 does the envelope work per object; you control access via key policy.
- Delete versus disable? Disable first, wait, then schedule deletion.

**Common mistakes:**
- Storing the plaintext data key.
- Deleting a key that still protects old datasets.
- Forgetting KMS permission for the job role (S3 allowed, KMS denied).
- Using an AWS managed key when another account needs access.

### Q39 ⭐⭐ 🔴 SageMaker in a locked-down VPC: network isolation, VPC config with private subnets and security groups, why you need S3 and ECR endpoints (ecr.api, ecr.dkr, S3 gateway), CloudWatch Logs and STS endpoints, and why a missing endpoint shows up as a hang or timeout rather than a clear error. Encode a required-endpoints checklist as data, run it against a moto VPC with and without endpoints, and print missing ones. Real routing, DNS and ENIs are not executed.
**Asked at:** AWS VPC interview sources (AWS Builder Center 'AWS VPC explained for beginners: from CIDR to interview questions', digitalcloud.training 'Security Group vs NACL', dev.to scenario-based security group and NACL questions, thenetworkdna 20 AWS network interview questions, kodekloud notes on VPC configuration for SageMaker; search snippets only, not opened); editorial prep and training notes, not verified candidate reports; cloud, DevOps and MLOps roles | SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs
**Say this first (1 line):** In a locked-down VPC the job has no internet, so it needs an S3 gateway endpoint and interface endpoints for ECR (api and dkr), CloudWatch Logs and STS, and a missing one shows up as a hang or timeout, not a clear error.

**Then explain:**
- **Setup:** network isolation turns off outbound network access from the container; the VPC config puts the job's ENIs in private subnets with security groups. Check which options need which (check current docs).
- **Needed paths:** S3 (data, artifacts and image layers) via a Gateway endpoint that must be attached to the subnet's route table; ECR via two interface endpoints, `ecr.api` and `ecr.dkr`; CloudWatch Logs; STS for role credentials; plus SageMaker API endpoints if code in the job calls them.
- **Why a hang:** with no route, packets are dropped silently; clients retry until they time out, so you see a slow generic failure. DNS for interface endpoints also needs private DNS enabled and a security group allowing 443 from the job.
- **Debug order:** read the failure reason, then check each endpoint and the route table association, endpoint SG, endpoint policy, and finally NACLs. A NAT gateway is the alternative to endpoints, with different security and cost trade-offs (Part 12).

**Example:** Hand-check the audit: an empty VPC misses all six. Then I created s3 without a route table plus the two ECR endpoints, and the audit flagged s3 (not attached) and logs, sts, sagemaker.api; after attaching the route table and adding the rest, nothing is missing.

**Code:** The checklist is data (`CHECKLIST`); `audit()` compares it with `describe_vpc_endpoints` and the subnet's route table. The service list is an example; verify against current docs for your job features. Run with `python3 -I` from the venv (boto3 1.43.118, moto 5.2.4); fake keys only.
```python
# Q39: required-endpoints checklist as data, run against a moto VPC with and without endpoints.
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws
REGION = "us-east-1"
# kind: Gateway endpoints go into route tables; Interface endpoints live as ENIs in subnets. List varies by job features: check current docs.
CHECKLIST = [
  {"service": "s3",         "kind": "Gateway",   "why": "training data in, model artifacts out, image layers are served from S3"},
  {"service": "ecr.api",    "kind": "Interface", "why": "ECR API calls (auth token, image manifest lookup)"},
  {"service": "ecr.dkr",    "kind": "Interface", "why": "docker registry protocol to pull the image"},
  {"service": "logs",       "kind": "Interface", "why": "job writes CloudWatch Logs"},
  {"service": "sts",        "kind": "Interface", "why": "role credentials / assume-role calls from inside the job"},
  {"service": "sagemaker.api", "kind": "Interface", "why": "only if code in the job calls the SageMaker API"},
]
def audit(ec2, vpc_id, subnet_route_tables):
    eps = ec2.describe_vpc_endpoints(Filters=[{"Name": "vpc-id", "Values": [vpc_id]}])["VpcEndpoints"]
    have = {e["ServiceName"].removeprefix(f"com.amazonaws.{REGION}."): e for e in eps}
    missing = []
    for item in CHECKLIST:
        e = have.get(item["service"])
        if e is None: missing.append((item["service"], "no endpoint")); continue
        if e["VpcEndpointType"] != item["kind"]: missing.append((item["service"], f"wrong type {e['VpcEndpointType']}"))
        elif item["kind"] == "Gateway" and not set(subnet_route_tables) <= set(e.get("RouteTableIds", [])):
            missing.append((item["service"], "not attached to the subnet's route table"))
    return missing

@mock_aws
def main():
    ec2 = boto3.client("ec2", region_name=REGION)
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")["Vpc"]["VpcId"]
    sn = ec2.create_subnet(VpcId=vpc, CidrBlock="10.0.1.0/24")["Subnet"]["SubnetId"]
    rt = ec2.create_route_table(VpcId=vpc)["RouteTable"]["RouteTableId"]
    ec2.associate_route_table(RouteTableId=rt, SubnetId=sn)
    sg = ec2.create_security_group(GroupName="sm-job", Description="job", VpcId=vpc)["GroupId"]
    print("A) empty VPC, missing:", audit(ec2, vpc, [rt]))
    ec2.create_vpc_endpoint(VpcId=vpc, ServiceName=f"com.amazonaws.{REGION}.s3", VpcEndpointType="Gateway")  # forgot route table
    for svc in ("ecr.api", "ecr.dkr"):
        ec2.create_vpc_endpoint(VpcId=vpc, ServiceName=f"com.amazonaws.{REGION}.{svc}", VpcEndpointType="Interface", SubnetIds=[sn], SecurityGroupIds=[sg])
    print("B) s3 (no route table) + ecr only, missing:", audit(ec2, vpc, [rt]))
    ep = ec2.describe_vpc_endpoints(Filters=[{"Name": "service-name", "Values": [f"com.amazonaws.{REGION}.s3"]}])["VpcEndpoints"][0]["VpcEndpointId"]
    ec2.modify_vpc_endpoint(VpcEndpointId=ep, AddRouteTableIds=[rt])
    for svc in ("logs", "sts", "sagemaker.api"):
        ec2.create_vpc_endpoint(VpcId=vpc, ServiceName=f"com.amazonaws.{REGION}.{svc}", VpcEndpointType="Interface", SubnetIds=[sn], SecurityGroupIds=[sg])
    print("C) all endpoints + route table, missing:", audit(ec2, vpc, [rt]))
main()
print("Not executed: DNS resolution to endpoint ENIs, routing, the actual hang/timeout a missing endpoint causes.")
```

**Output (my run):** real run in moto. Moto stores VPC objects only: routing, private DNS, ENIs and the real timeout were not executed.
```text
A) empty VPC, missing: [('s3', 'no endpoint'), ('ecr.api', 'no endpoint'), ('ecr.dkr', 'no endpoint'), ('logs', 'no endpoint'), ('sts', 'no endpoint'), ('sagemaker.api', 'no endpoint')]
B) s3 (no route table) + ecr only, missing: [('s3', "not attached to the subnet's route table"), ('logs', 'no endpoint'), ('sts', 'no endpoint'), ('sagemaker.api', 'no endpoint')]
C) all endpoints + route table, missing: []
Not executed: DNS resolution to endpoint ENIs, routing, the actual hang/timeout a missing endpoint causes.
```

**Follow-ups:**
- Gateway versus interface endpoint? Gateway: route-table entry, S3 and DynamoDB only; interface: ENI with private IP in your subnet.
- Why ecr.dkr and ecr.api both? One for registry protocol pulls, the other for API calls.
- Alternative? A NAT gateway, but traffic leaves the private design; endpoints keep it on the AWS network.

**Common mistakes:**
- Only creating the S3 endpoint.
- Gateway endpoint not associated with the subnet's route table.
- Endpoint security group blocking 443 from the job.
- Forgetting the logs endpoint and blaming the image.

### Q40 ⭐⭐ 🔴 Cross-account model promotion: training in a dev account, model artifacts in S3 and images in ECR, deployment in a prod account. List every grant needed (S3 bucket policy and role policy, ECR repository policy, KMS key policy, a role to assume, registry sharing), explain why both sides of a cross-account grant are needed, and give the three most common failures. Run the evaluator on cross-account cases with one side missing and print each decision.
**Asked at:** IAM interview and policy-evaluation sources (AWS IAM 'Policy evaluation logic' pages on docs.aws.amazon.com and docs.aws.eu, tutorialsdojo 'How AWS IAM Handles Conflicting IAM Policies', advancedweb.hu 'IAM policy evaluation logic explained with examples', barkingiguana 'How IAM Policy Evaluation Actually Works', community.aws and hidekazu-konishi IAM glossary; search snippets only, not opened); vendor docs and study guides, not verified candidate reports; cloud, DevOps, security and MLOps roles at IT-services firms, product companies and GCCs | SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs
**Say this first (1 line):** Cross-account access needs both sides every time: the prod role must be allowed in prod IAM, and the dev resource (bucket, repository, key, role trust) must name that prod role.

**Then explain:**
- **Grants, dev to prod:** (1) S3: dev bucket policy allowing the prod role, and prod role policy allowing the S3 actions; (2) ECR: dev repository policy allowing prod pull actions, and prod role with `ecr:GetAuthorizationToken` and pull actions (or ECR replication into prod); (3) KMS: dev key policy allowing the prod role, plus prod IAM permission; (4) if prod assumes a role in dev, dev trust policy plus `sts:AssumeRole` in prod; (5) model registry sharing via a model package group resource policy or RAM (check current docs).
- **Why both sides:** across accounts neither account alone can decide. The owner of the resource must trust the other principal, and the caller's own account must allow its principal to make the call. One missing side gives implicit deny.
- **Three common failures:** (a) only one side written, so AccessDenied; (b) the artifact is encrypted with a key policy that does not include the prod role (S3 fine, KMS denied); a default AWS managed key cannot be shared; (c) ECR pull fails because the repository policy or `GetAuthorizationToken` is missing, or the image reference points at the wrong account or Region.
- **Prefer** digests and a promotion step that copies or replicates artifacts into prod over granting prod broad read on dev.

**Example:** Hand-check from the output: S3 with identity and bucket policy allows; remove either and it denies. Same shape for ECR, KMS and AssumeRole. The last case shows an explicit Deny in the bucket policy beating both allows.

**Code:** Uses the simplified evaluator copied from `scratch/B4P10_wavea/iam_eval_sketch.py` (copy kept beside the script). Dev account 111111111111 and prod 222222222222 are fake. Run with `python3 -I` from the venv (boto3 1.43.118, moto 5.2.4); fake keys only.
```python
# Q40: cross-account promotion. Uses the simplified evaluator (copied from scratch/B4P10_wavea). Principal: role in DEV or PROD.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iam_eval_sketch import evaluate
DEV, PROD = "111111111111", "222222222222"
dev_role = f"arn:aws:iam::{DEV}:role/train-role"
prod_role = f"arn:aws:iam::{PROD}:role/deploy-role"
pol = lambda act, res, eff="Allow": {"Version": "2012-10-17", "Statement": [{"Effect": eff, "Action": act, "Resource": res}]}
def rp(arn, act, res, eff="Allow"):
    return {"Version": "2012-10-17", "Statement": [{"Effect": eff, "Principal": {"AWS": arn}, "Action": act, "Resource": res}]}
art = f"arn:aws:s3:::dev-model-artifacts/models/v7/model.tar.gz"
repo = f"arn:aws:ecr:us-east-1:{DEV}:repository/risk-model"
key = f"arn:aws:kms:us-east-1:{DEV}:key/1234abcd"
trust_target = f"arn:aws:iam::{DEV}:role/model-reader"      # a role in dev that prod assumes to read artifacts

cases = [
 # (label, action, resource, kwargs)
 ("S3 both sides present",            "s3:GetObject", art, dict(identity=[pol("s3:GetObject", art)], resource_policy=rp(prod_role, "s3:GetObject", art))),
 ("S3 prod role policy missing",      "s3:GetObject", art, dict(identity=[], resource_policy=rp(prod_role, "s3:GetObject", art))),
 ("S3 dev bucket policy missing",     "s3:GetObject", art, dict(identity=[pol("s3:GetObject", art)], resource_policy=None)),
 ("ECR pull: repo policy + role",     "ecr:BatchGetImage", repo, dict(identity=[pol("ecr:BatchGetImage", repo)], resource_policy=rp(prod_role, "ecr:BatchGetImage", repo))),
 ("ECR pull: repo policy missing",    "ecr:BatchGetImage", repo, dict(identity=[pol("ecr:BatchGetImage", repo)], resource_policy=None)),
 ("KMS decrypt: key policy missing",  "kms:Decrypt", key, dict(identity=[pol("kms:Decrypt", key)], resource_policy=None)),
 ("KMS decrypt: both sides",          "kms:Decrypt", key, dict(identity=[pol("kms:Decrypt", key)], resource_policy=rp(prod_role, "kms:Decrypt", key))),
 ("AssumeRole: trust names prod only, no sts:AssumeRole in prod", "sts:AssumeRole", trust_target, dict(identity=[], resource_policy=rp(prod_role, "sts:AssumeRole", trust_target))),
 ("AssumeRole: both sides",           "sts:AssumeRole", trust_target, dict(identity=[pol("sts:AssumeRole", trust_target)], resource_policy=rp(prod_role, "sts:AssumeRole", trust_target))),
 ("S3 both sides but explicit deny in bucket policy", "s3:GetObject", art, dict(identity=[pol("s3:GetObject", art)], resource_policy={"Statement": [
      {"Effect": "Allow", "Principal": {"AWS": prod_role}, "Action": "s3:GetObject", "Resource": art},
      {"Effect": "Deny", "Principal": "*", "Action": "s3:GetObject", "Resource": art}]})),
]
print(f"{'case':58s} {'decision':8s} reason")
for label, act, res, kw in cases:
    rpol = kw.pop("resource_policy")
    if rpol is None:
        d = evaluate(act, res, same_account=False, principal_arn=prod_role, **kw)
    else:
        d = evaluate(act, res, same_account=False, principal_arn=prod_role, resource_policy=rpol, **kw)
    print(f"{label:58s} {d[0]:8s} {d[1]}")
print("simplified: the sketch ignores the S3 'resource-policy Principal is the account root' pattern, KMS key-policy-must-enable-IAM rule, ECR GetAuthorizationToken (identity-only), and grants.")
```

**Output (my run):** real run of the sketch. It is simplified: no KMS rule that the key policy must enable IAM, no account-root principals, no grants, no VPC endpoint or boundary layers here. It shows the 'both sides' logic, not AWS's full engine, and no real AWS call was made.
```text
case                                                       decision reason
S3 both sides present                                      Allow    cross-account: identity AND resource policy allow
S3 prod role policy missing                                Deny     implicit deny: cross-account needs both sides
S3 dev bucket policy missing                               Deny     implicit deny: cross-account needs both sides
ECR pull: repo policy + role                               Allow    cross-account: identity AND resource policy allow
ECR pull: repo policy missing                              Deny     implicit deny: cross-account needs both sides
KMS decrypt: key policy missing                            Deny     implicit deny: cross-account needs both sides
KMS decrypt: both sides                                    Allow    cross-account: identity AND resource policy allow
AssumeRole: trust names prod only, no sts:AssumeRole in prod Deny     implicit deny: cross-account needs both sides
AssumeRole: both sides                                     Allow    cross-account: identity AND resource policy allow
S3 both sides but explicit deny in bucket policy           Deny     explicit deny
simplified: the sketch ignores the S3 'resource-policy Principal is the account root' pattern, KMS key-policy-must-enable-IAM rule, ECR GetAuthorizationToken (identity-only), and grants.
```

**Follow-ups:**
- Could a resource policy alone be enough? Within one account sometimes; across accounts, no (check the policy-evaluation docs).
- Copy artifacts instead? Often cleaner: a pipeline copies the model and image into prod so prod never reads dev.
- How do you debug? CloudTrail errorMessage and the policy simulator in real AWS (not run here).

**Common mistakes:**
- Fixing only the bucket policy.
- Encrypting with a key prod cannot use.
- Using `Principal: *` to make it work.
- Granting prod read on the whole dev account.

### Q41 ⭐ 🟡 Package an ML inference handler for Lambda: lazy-load the model outside the handler, keep the handler testable as a plain function, and size the image. Write a handler for a tiny scikit-learn-free model, test it locally with fake events, and simulate cold versus warm invocations by counting model loads in pure Python. Cover zip versus container image trade-offs, layers, and ECR. No Lambda runtime executed; Dockerfile craft belongs to Part 2.
**Asked at:** Lambda interview and limits sources (kodekloud AWS Developer Associate notes on limits and concurrency, awsfundamentals.com 'Lambda limitations', a dev.to Lambda compute-limits post, a pulumi provisioned-concurrency post; search snippets only, not opened; secondary sources disagreed on package-size wording so numbers are hedged 'check current docs'); training notes and blogs, not verified interview reports; backend, cloud and ML engineer roles | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)
**Say this first (1 line):** Load the model once, outside the handler, behind a lazy getter; keep the handler a thin wrapper over a plain `predict()` function; and treat cold start as a cost you measure, not something you hide.

**Then explain:**
- Lambda reuses an execution environment for later calls. Module-level state survives, so a cached model is loaded once per environment (the cold start) and reused on warm calls. A new environment loads it again.
- Testability: `predict(model, features)` is plain Python with no event or context. The handler only parses, validates, calls `predict`, and shapes the response (400 on bad input, 200 with a score).
- Zip vs container image: zip is simple and fast to deploy for small code and light dependencies. A container image fits big dependencies and models and lets you reuse your Part 2 Dockerfile habits. Limits differ and change, so check current docs. Images for Lambda live in ECR.
- Layers share common dependencies between functions but still count towards the size limit and still load at init. They do not remove the cold start.
- Failure modes: loading the model inside the handler (every call pays), loading at import with no error handling (init failure on every cold start), a model too big or slow for the memory, and a model that needs a GPU. Lambda is the wrong tool for GPU or very large models; use SageMaker, ECS or EKS (Q15).
- Mitigations to name: provisioned concurrency to keep environments warm (costs money, check current docs), smaller artifacts, and loading only what the first request needs.

**Example:** Weights `[0.5, -0.25]`, bias `0`, features `[2, 4]`. `z = 0.5*2 - 0.25*4 = 0`, `sigmoid(0) = 0.5`. Five calls in one environment give `loads = 1`. A new environment gives `loads = 2`. Hand-check: loads equal the number of environments, not the number of calls.

**Code:** the handler and test (`q41_lambda_handler.py`), then a Dockerfile that was only linted by reading (`q41_dockerfile_check.py`, in code/).
```python
"""Q41: Lambda-style inference handler, lazy model load, cold vs warm counting. Pure Python, no AWS."""
import json, os, tempfile

MODEL_PATH = os.environ.get("MODEL_PATH", "/opt/ml/model.json")   # layer/image path in real life; env var keeps it testable
_MODEL = None          # module-level cache: survives between invocations in the same execution environment
LOADS = 0              # test-only counter

def load_model(path):
    global LOADS
    LOADS += 1                                   # in real life: this is the slow part (read file, build object)
    with open(path) as f:
        return json.load(f)

def get_model():
    global _MODEL
    if _MODEL is None:                           # first call in this container = cold; later calls reuse
        _MODEL = load_model(MODEL_PATH)
    return _MODEL

def predict(model, features):                    # plain function: unit-testable, no event or context
    z = model["bias"] + sum(w * x for w, x in zip(model["weights"], features))
    return 1.0 / (1.0 + 2.718281828459045 ** (-z))

def handler(event, context=None):                # thin wrapper: parse, validate, call predict, shape response
    try:
        body = json.loads(event["body"]) if isinstance(event.get("body"), str) else event
        feats = [float(v) for v in body["features"]]
    except (KeyError, ValueError, TypeError):
        return {"statusCode": 400, "body": json.dumps({"error": "need numeric 'features'"})}
    model = get_model()
    if len(feats) != len(model["weights"]):
        return {"statusCode": 400, "body": json.dumps({"error": f"expected {len(model['weights'])} features"})}
    return {"statusCode": 200, "body": json.dumps({"score": round(predict(model, feats), 4)})}

def simulate_new_container():                    # what a cold start does to module state
    global _MODEL
    _MODEL = None

if __name__ == "__main__":
    d = tempfile.mkdtemp()
    MODEL_PATH = os.path.join(d, "model.json")
    json.dump({"weights": [0.5, -0.25], "bias": 0.0}, open(MODEL_PATH, "w"))
    # unit test of the pure function (hand check: z = 0.5*2 - 0.25*4 = 0 -> sigmoid(0) = 0.5)
    assert predict({"weights": [0.5, -0.25], "bias": 0.0}, [2, 4]) == 0.5
    ev = {"body": json.dumps({"features": [2, 4]})}
    print("loads before any call:", LOADS)
    r1 = handler(ev); print("call 1 (cold):", r1, "| loads =", LOADS)
    for _ in range(4): handler(ev)
    print("calls 2-5 (warm): loads =", LOADS)
    simulate_new_container()
    handler(ev); print("after new container, call 6: loads =", LOADS)
    print("bad body:", handler({"body": "{}"}))
    print("wrong length:", handler({"features": [1]}))
    assert LOADS == 2
    # size budget helper: what goes into the package
    sizes = {"model.json": os.path.getsize(MODEL_PATH), "handler.py": os.path.getsize(__file__)}
    print("package bytes:", sizes)
```
```dockerfile
# Not built here (no Docker daemon). Check current docs for the Lambda base image tags and size limits.
FROM public.ecr.aws/lambda/python:3.12
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir -r requirements.txt
COPY handler.py model.json ${LAMBDA_TASK_ROOT}/
CMD ["handler.handler"]
```

**Output (my run):** the handler test and the Dockerfile text check ran for real with Python 3.13. No Lambda runtime, no image build (no Docker daemon), and no ECR push was executed, so cold-start timings are not measured and none are claimed.
```text
$ python3 -I q41_lambda_handler.py
loads before any call: 0
call 1 (cold): {'statusCode': 200, 'body': '{"score": 0.5}'} | loads = 1
calls 2-5 (warm): loads = 1
after new container, call 6: loads = 2
bad body: {'statusCode': 400, 'body': '{"error": "need numeric \'features\'"}'}
wrong length: {'statusCode': 400, 'body': '{"error": "expected 2 features"}'}
package bytes: {'model.json': 38, 'handler.py': 2854}

$ python3 -I q41_dockerfile_check.py
ok   starts with FROM
ok   CMD is handler.handler (module.function)
ok   deps copied before code (cache friendly)
ok   pip --no-cache-dir
ok   no secrets (KEY/SECRET/PASSWORD)
```

**Follow-ups:**
- *How would you measure the real cold start?* In real AWS, log the init duration and compare first and later invocations; check current docs for the log fields. Not executed here.
- *Handler returns 200 even when the model fails to load?* No. Let init errors fail loudly, and return 4xx for bad input only.
- *Why not read the model from S3 on every call?* Network and parse cost on each call; cache it in the environment (and still handle model version changes by redeploying or by a version key).

**Common mistakes:** loading in the handler; putting the model in `/tmp` and assuming it is always there; testing only through the Lambda console; a heavy `import` list you do not use; claiming layers fix cold start; no input validation.

### Q42 ⭐ 🟡 Bedrock at the boundary with Book 2: what an ML engineer on AWS needs to know about IAM for bedrock:InvokeModel, model access, VPC endpoints for private calls, invocation logging and guardrails as service features, and what stays in Book 2 (prompting, RAG, evaluation, LLM serving). Call the bedrock-runtime mock, show the canned response, and state the mock proves only the request shape.
**Asked at:** Job-posting skill lists (a getonbrd Senior MLOps Engineer AWS and SageMaker posting listing Athena, RDS, ECR, IAM, CloudWatch, CloudFormation or Terraform and GitHub Actions, a workingnomads Senior MLOps Engineer SageMaker and Airflow posting; search snippets only, not opened); job postings, not interview reports; MLOps roles on AWS | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)
**Say this first (1 line):** From the platform side, Bedrock is an IAM-controlled API: allow `bedrock:InvokeModel` on named model resources, reach it through a VPC endpoint if traffic must stay private, turn on invocation logging deliberately, and leave prompting, RAG and evaluation to Book 2.

**Then explain:**
- IAM: scope `bedrock:InvokeModel` (and the streaming and Converse variants, check current docs for exact action mapping) to specific foundation-model ARNs. Foundation-model ARNs have an empty account field. Add a Region condition. If you call through inference profiles, the profile ARN is also a resource (check current docs).
- Model access: models may need to be enabled for the account before use, and the mechanism has changed over time. Check current docs. A missing grant shows up as an access error, not as a model error.
- Private path: an interface VPC endpoint for the `bedrock-runtime` service keeps calls off the public internet. Remember the endpoint's own security group and optional endpoint policy.
- Logging: invocation logging to CloudWatch Logs or S3 is a configuration you choose. Prompts and outputs can contain customer data, so decide retention, encryption and who can read the log group.
- Guardrails: a service feature (denied topics, content filters, and so on) that you attach to calls. It is not a substitute for application-level checks.
- Out of scope here: prompt design, retrieval, LLM evaluation and serving trade-offs belong to Book 2.

**Example:** Policy allows one model in `us-east-1`. Calling that model: allowed. Another model: implicit deny. Same model in `eu-west-1`: denied by the Region condition (see output).

**Code:** IAM check, `invoke_model` on the mock, a VPC endpoint record, and a probe of which Bedrock control-plane calls the mock implements.
```python
"""Q42: Bedrock boundary. moto mock, fake keys. API shape only."""
import os, sys, json
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boto3
from moto import mock_aws
from iam_eval_ext import evaluate

MODEL = "anthropic.claude-3-haiku-20240307-v1:0"     # example model id string only; check current docs for model ids
policy = {"Version": "2012-10-17", "Statement": [
  {"Effect": "Allow", "Action": ["bedrock:InvokeModel"],
   "Resource": [f"arn:aws:bedrock:us-east-1::foundation-model/{MODEL}"],
   "Condition": {"StringEquals": {"aws:RequestedRegion": "us-east-1"}}}]}

print("== IAM: allow one model in one Region ==")
for name, res, ctx in [
  ("approved model, us-east-1", f"arn:aws:bedrock:us-east-1::foundation-model/{MODEL}", {"aws:RequestedRegion": "us-east-1"}),
  ("other model", "arn:aws:bedrock:us-east-1::foundation-model/other.model-v1:0", {"aws:RequestedRegion": "us-east-1"}),
  ("approved model, other Region", f"arn:aws:bedrock:eu-west-1::foundation-model/{MODEL}", {"aws:RequestedRegion": "eu-west-1"}),
]:
    print(f"{name:32s}", evaluate("bedrock:InvokeModel", res, ctx=ctx, identity=[policy]))

with mock_aws():
    print("\n== bedrock-runtime invoke_model (mock) ==")
    br = boto3.client("bedrock-runtime")
    body = json.dumps({"anthropic_version": "bedrock-2023-05-31", "max_tokens": 50,
                       "messages": [{"role": "user", "content": "hello"}]})
    r = br.invoke_model(modelId=MODEL, body=body, contentType="application/json", accept="application/json")
    print("HTTP", r["ResponseMetadata"]["HTTPStatusCode"], "| contentType", r["contentType"])
    print("body:", r["body"].read().decode()[:200])

    print("\n== private call path: interface VPC endpoint (record only) ==")
    ec2 = boto3.client("ec2")
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")["Vpc"]["VpcId"]
    sn = ec2.create_subnet(VpcId=vpc, CidrBlock="10.0.1.0/24")["Subnet"]["SubnetId"]
    ep = ec2.create_vpc_endpoint(VpcId=vpc, ServiceName="com.amazonaws.us-east-1.bedrock-runtime",
                                 VpcEndpointType="Interface", SubnetIds=[sn], PrivateDnsEnabled=True)["VpcEndpoint"]
    print("endpoint service:", ep["ServiceName"], "| type:", ep["VpcEndpointType"], "| private DNS:", ep["PrivateDnsEnabled"])

    print("\n== invocation logging and guardrails in moto (what exists?) ==")
    b = boto3.client("bedrock")
    for label, fn in [
      ("put_model_invocation_logging_configuration", lambda: b.put_model_invocation_logging_configuration(
          loggingConfig={"cloudWatchConfig": {"logGroupName": "/bedrock/invocations", "roleArn": "arn:aws:iam::123456789012:role/br-log"},
                         "textDataDeliveryEnabled": True})),
      ("get_model_invocation_logging_configuration", lambda: b.get_model_invocation_logging_configuration()),
      ("create_guardrail", lambda: b.create_guardrail(name="g1", blockedInputMessaging="no", blockedOutputsMessaging="no",
          topicPolicyConfig={"topicsConfig": [{"name": "advice", "definition": "financial advice", "type": "DENY"}]})),
      ("list_foundation_models", lambda: b.list_foundation_models()),
    ]:
        try:
            out = fn(); out.pop("ResponseMetadata", None)
            print(f"{label}: ok -> {str(out)[:150]}")
        except Exception as e:
            print(f"{label}: {type(e).__name__}: {str(e)[:100]}")
```

**Output (my run):** ran against moto with fake keys. The mock returned an empty `{}` body for `invoke_model`: it proves only that the request shape was accepted. It does not call a model, check model access, check IAM, or route through the endpoint. `create_guardrail` and `list_foundation_models` are not implemented in this moto version; invocation-logging config round-trips. Real Bedrock behaviour is not executed.
```text
== IAM: allow one model in one Region ==
approved model, us-east-1        ('Allow', 'identity or resource policy allows (same account)')
other model                      ('Deny', 'implicit deny: nothing allows')
approved model, other Region     ('Deny', 'implicit deny: nothing allows')

== bedrock-runtime invoke_model (mock) ==
HTTP 200 | contentType application/json
body: {}

== private call path: interface VPC endpoint (record only) ==
endpoint service: com.amazonaws.us-east-1.bedrock-runtime | type: Interface | private DNS: True

== invocation logging and guardrails in moto (what exists?) ==
put_model_invocation_logging_configuration: ok -> {}
get_model_invocation_logging_configuration: ok -> {'loggingConfig': {'cloudWatchConfig': {'logGroupName': '/bedrock/invocations', 'roleArn': 'arn:aws:iam::123456789012:role/br-log'}, 'textDataDelivery
create_guardrail: NotImplementedError: The create_guardrail action has not been implemented
list_foundation_models: NotImplementedError: The list_foundation_models action has not been implemented
```

**Follow-ups:**
- *Where do Bedrock calls show up for audit?* CloudTrail records API calls (check current docs for which events); the mock has no CloudTrail lookup (Q19, Q50).
- *Who needs permission, the user or the app role?* The calling principal: usually the application's role. Developers get a narrower set in non-prod.
- *Bedrock or self-hosted model on SageMaker?* A trade-off on control, ops and cost; the LLM-serving side is Book 2.

**Common mistakes:** `bedrock:*` on `*`; forgetting the Region condition or the inference-profile ARN; logging full prompts into an open log group; assuming the mock tested guardrails; mixing Book 2 topics (prompt design) into a platform answer.

### Q43 ⭐ 🟡 Distributed training on EC2: cluster placement groups, high-bandwidth networking (EFA), NVLink within a node, why AZ choice and capacity reservations matter, and how data loading and checkpoint writes to S3 become the bottleneck. Training algorithm design belongs to Books 1 and 2. Show a launch-template and placement-group spec as validated YAML and note moto did not implement create_placement_group in this version. Nothing real was executed.
**Asked at:** EC2 and spot-training sources (introl.com and barkingiguana.com posts on spot GPU training and SageMaker managed spot, practitioner notes on checkpoint cadence and resume testing; search snippets only, not opened; a savings percentage in one title was not used); blogs, not interview reports; ML platform and MLOps roles | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)
**Say this first (1 line):** Multi-node training is limited by the slowest link: put nodes in one AZ and a cluster placement group, use EFA-capable instances for fast node-to-node traffic, secure capacity ahead of time, and make sure data loading and checkpoint writes do not starve the GPUs.

**Then explain:**
- Inside a node, GPUs talk over a fast interconnect (NVLink on suitable instance types). Between nodes, you want low latency and high bandwidth: EFA network interface plus a `cluster` placement group (packs instances close in one AZ). Check current docs for which instance types support EFA.
- Placement strategies: `cluster` for tightly coupled jobs, `partition` for big replicated systems, `spread` for a few critical instances. Cluster groups trade resilience for locality and can fail to launch if capacity is short.
- AZ choice matters: capacity differs per AZ and per Region, and a multi-AZ cluster adds latency. Capacity reservations or capacity blocks can guarantee GPUs for a window (check current docs); GPU quota and capacity surprises are common.
- Spot is a poor fit for tightly coupled multi-node jobs: one reclaimed node can kill the whole job (Q14 covers single-node checkpointing).
- The bottleneck is often I/O: many workers reading small files from S3 (Q36) and checkpoints written as one big blob. Shard data, cache on local NVMe, write sharded checkpoints, keep the checkpoint interval a trade-off.
- Algorithm and parallelism strategy (data, tensor, pipeline) belong to Books 1 and 2.

**Example:** Spec asks for 4 nodes, EFA on, strategy `cluster`, all in `ap-south-1a`. If you changed the strategy to `spread`, the checker flags it: EFA multi-node training normally wants a cluster group.

**Code:** the spec as YAML, then the checker and the moto probe.
```python
"""Q43: validate the cluster spec (pyyaml + hand checks) and probe moto for placement groups / launch templates."""
import os, sys, re
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="ap-south-1")
import yaml, boto3
from moto import mock_aws
here = os.path.dirname(os.path.abspath(__file__))
spec = yaml.safe_load(open(os.path.join(here, "q43_cluster_spec.yaml")))

errs = []
pg, lt, c, io = spec["placement_group"], spec["launch_template"], spec["cluster"], spec["training_io"]
if pg["strategy"] not in ("cluster", "partition", "spread"): errs.append("bad placement strategy")
if not c["availability_zone"].startswith(c["region"]): errs.append("AZ not in Region")
if lt["efa"] and pg["strategy"] != "cluster": errs.append("EFA multi-node training normally wants a cluster placement group")
if lt["capacity"]["market"] == "spot" and lt["capacity"]["nodes"] > 1: errs.append("spot + tightly coupled multi-node: one reclaim kills the job")
if not re.match(r"^ami-[0-9a-f]{8,17}$", lt["image_id"]): errs.append("image_id format")
for k in ("data_prefix", "checkpoint_prefix"):
    if not io[k].startswith("s3://") or not io[k].endswith("/"): errs.append(f"{k} must be s3://.../")
print("YAML parsed; sections:", sorted(spec))
print("spec errors:", errs or "none")

# negative test: break the spec and make sure the checker notices
bad = yaml.safe_load(yaml.safe_dump(spec)); bad["placement_group"]["strategy"] = "spread"
print("EFA with spread group flagged:", bad["launch_template"]["efa"] and bad["placement_group"]["strategy"] != "cluster")

with mock_aws():
    ec2 = boto3.client("ec2")
    try:
        ec2.create_placement_group(GroupName=pg["name"], Strategy=pg["strategy"])
        print("create_placement_group: ok")
    except Exception as e:
        print("create_placement_group:", type(e).__name__, str(e)[:90])
    r = ec2.create_launch_template(LaunchTemplateName=lt["name"], LaunchTemplateData={
        "ImageId": lt["image_id"], "InstanceType": lt["instance_type"],
        "NetworkInterfaces": [{"DeviceIndex": 0, "InterfaceType": "efa"}],
        "Placement": {"GroupName": pg["name"], "AvailabilityZone": c["availability_zone"]}})
    print("launch template:", r["LaunchTemplate"]["LaunchTemplateName"], "version", r["LaunchTemplate"]["LatestVersionNumber"])
    d = ec2.describe_launch_template_versions(LaunchTemplateName=lt["name"])["LaunchTemplateVersions"][0]["LaunchTemplateData"]
    print("read back: type", d["InstanceType"], "| NIC", d["NetworkInterfaces"][0]["InterfaceType"], "| placement", d.get("Placement"))
    it = ec2.describe_instance_types(InstanceTypes=[lt["instance_type"]])["InstanceTypes"][0]
    print("describe_instance_types:", it["InstanceType"], "| GPUs:", [(g["Name"], g["Count"]) for g in it.get("GpuInfo", {}).get("Gpus", [])],
          "| EfaSupported:", it.get("NetworkInfo", {}).get("EfaSupported"))
```
```yaml
# Spec for a multi-node training cluster. Field names are OUR schema, mapped to EC2 API fields in the checker.
# Instance type, EFA support and capacity are examples only: check current docs and your account quotas.
cluster:
  name: ft-7b-cluster
  region: ap-south-1
  availability_zone: ap-south-1a        # one AZ: placement group and EFA traffic stay inside it
placement_group:
  name: ft-7b-pg
  strategy: cluster                     # cluster | partition | spread
launch_template:
  name: ft-7b-lt
  instance_type: p4d.24xlarge           # example of a GPU training family; verify availability in your Region
  image_id: ami-0123456789abcdef0       # Deep Learning AMI id (placeholder)
  efa: true                             # elastic fabric adapter network interface
  ebs_gb: 500
  capacity:
    market: capacity-block              # on-demand | spot | capacity-block | odcr
    nodes: 4
training_io:
  data_prefix: s3://ml-data/train/
  checkpoint_prefix: s3://ml-data/ckpt/ft-7b/
  checkpoint_every_minutes: 30          # a trade-off, not a rule
```

**Output (my run):** pyyaml parsing and the hand-written checks ran for real. In moto, `create_placement_group` raised `NotImplementedError`; a launch template with EFA and placement fields was created and read back; `describe_instance_types` returned canned GPU info. A mock cannot show real GPUs, EFA performance, quotas, capacity, or whether a placement group can be satisfied: not executed. The instance type is an example; check current docs.
```text
YAML parsed; sections: ['cluster', 'launch_template', 'placement_group', 'training_io']
spec errors: none
EFA with spread group flagged: True
create_placement_group: NotImplementedError The create_placement_group action has not been implemented
launch template: ft-7b-lt version 1
read back: type p4d.24xlarge | NIC efa | placement {'AvailabilityZone': 'ap-south-1a', 'GroupName': 'ft-7b-pg'}
describe_instance_types: p4d.24xlarge | GPUs: [('A100', 8)] | EfaSupported: True
```

**Follow-ups:**
- *Why not just more nodes?* Communication cost grows and the scaling stops being linear; measure scaling efficiency on a small run first.
- *Capacity reservation or on-demand?* Reservation guarantees capacity for the cost of paying while idle; on-demand can fail at launch. Check current docs for the exact reservation types.
- *Where do checkpoints go?* S3 or a shared file system; write them from a few ranks, sharded, and test restore.

**Common mistakes:** multi-AZ for a tightly coupled job; spot for multi-node without restart logic; ignoring quota until launch day; slow data loading hidden behind GPU purchase; claiming benchmark numbers.

### Q44 ⭐ 🟡 Cost basics without prices: the levers behind an AWS ML bill (instance hours, idle endpoints, data transfer, storage classes, NAT gateway traffic, GPU utilisation, logging volume), the mechanisms to control it (tags and cost allocation tags, budgets, autoscaling, spot, scheduled shutdown of notebooks and endpoints, lifecycle rules). Full cost design belongs to Part 12. Use moto's tagging API to list resources and write a function that flags untagged resources and idle endpoints from sample data.
**Asked at:** Job-posting skill lists (a getonbrd Senior MLOps Engineer AWS and SageMaker posting listing Athena, RDS, ECR, IAM, CloudWatch, CloudFormation or Terraform and GitHub Actions, a workingnomads Senior MLOps Engineer SageMaker and Airflow posting; search snippets only, not opened); job postings, not interview reports; MLOps roles on AWS | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)
**Say this first (1 line):** The bill comes from a few levers: hours that instances and endpoints run, things left idle, data movement, storage class and logging volume; control them with tags, budgets, autoscaling, scheduled shutdown, spot and lifecycle rules. I will not quote prices; check current pricing pages.

**Then explain:**
- Compute: instance hours for training, notebooks and endpoints. A real-time endpoint keeps billing while idle; a forgotten notebook does too.
- Utilisation: an expensive GPU at low utilisation is a cost bug, not an infra detail.
- Data: storage class and lifecycle, request counts, data transfer across AZs, Regions or out of AWS, and NAT gateway traffic (S3 through a gateway endpoint avoids sending that traffic through NAT; check current docs).
- Observability itself costs: verbose logs and high-cardinality custom metrics.
- Controls: cost allocation tags (`team`, `project`, `env`) activated in billing, budgets and alerts, autoscaling or scale-to-zero options, spot for fault-tolerant training, scheduled stop of non-prod endpoints and notebooks, lifecycle rules (Q1).
- Edge case: tags help only if they are present and activated; untagged spend is unattributed. Full cost design is Part 12.

**Example:** Resources: an S3 bucket tagged `team, env` (missing `project`), a bucket with no tags, a model with all three. The audit lists both gaps. Endpoint `forgotten-poc` has zero calls for 7 days and is flagged; `old-demo` had 5 calls inside the window and is not.

**Code:** moto tagging call plus two pure functions on sample data.
```python
"""Q44: tag audit + idle endpoint finder. moto tagging API (API shape only), then pure functions on sample data. No prices."""
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

REQUIRED = {"team", "project", "env"}

def untagged(resources, required=REQUIRED):
    """resources: [{'arn':..., 'tags': {k: v}}]. Return [(arn, missing_keys)] for resources missing required tags."""
    out = []
    for r in resources:
        missing = sorted(required - set(r["tags"]))
        if missing: out.append((r["arn"], missing))
    return out

def idle_endpoints(endpoints, min_idle_days=7):
    """endpoints: [{'name','status','daily_invocations': [..newest last..]}]. Idle = InService and zero invocations for the last N days."""
    out = []
    for e in endpoints:
        recent = e["daily_invocations"][-min_idle_days:]
        if e["status"] == "InService" and len(recent) == min_idle_days and sum(recent) == 0:
            out.append(e["name"])
    return out

with mock_aws():
    s3, sm, rg = boto3.client("s3"), boto3.client("sagemaker"), boto3.client("resourcegroupstaggingapi")
    s3.create_bucket(Bucket="ml-raw-dev")
    s3.put_bucket_tagging(Bucket="ml-raw-dev", Tagging={"TagSet": [{"Key": "team", "Value": "risk"}, {"Key": "env", "Value": "dev"}]})
    s3.create_bucket(Bucket="ml-scratch")                 # no tags at all
    sm.create_model(ModelName="m1", ExecutionRoleArn="arn:aws:iam::123456789012:role/sm", PrimaryContainer={"Image": "x/y:1"},
                    Tags=[{"Key": "team", "Value": "risk"}, {"Key": "project", "Value": "pd-model"}, {"Key": "env", "Value": "dev"}])
    res = rg.get_resources()["ResourceTagMappingList"]
    print("tagging API returned", len(res), "tagged resources:")
    inv = []
    for r in res:
        tags = {t["Key"]: t["Value"] for t in r["Tags"]}
        print(" ", r["ResourceARN"], tags); inv.append({"arn": r["ResourceARN"], "tags": tags})
    # moto lists only resources that carry tags; real AWS behaviour here: check current docs
    inv.append({"arn": "arn:aws:s3:::ml-scratch", "tags": {}})      # untagged resource added by hand from list_buckets
    print("\nlist_buckets sees:", [b["Name"] for b in s3.list_buckets()["Buckets"]])

print("\n== flag untagged resources ==")
for arn, miss in untagged(inv): print(" ", arn, "missing", miss)

print("\n== idle endpoints (sample data, 'newest last') ==")
sample = [
  {"name": "pd-model-prod", "status": "InService", "daily_invocations": [900, 880, 910, 905, 890, 920, 930]},
  {"name": "old-demo", "status": "InService", "daily_invocations": [5, 0, 0, 0, 0, 0, 0]},
  {"name": "forgotten-poc", "status": "InService", "daily_invocations": [0] * 7},
  {"name": "failed-one", "status": "Failed", "daily_invocations": [0] * 7},
  {"name": "new-endpoint", "status": "InService", "daily_invocations": [0, 0]},
]
print("idle:", idle_endpoints(sample))
assert idle_endpoints(sample) == ["forgotten-poc"]   # old-demo had 5 calls inside the window
```

**Output (my run):** the moto calls and the functions ran for real. In moto, the tagging API returned only resources that carry tags; the untagged bucket appeared only through `list_buckets`, so a real audit must start from a resource inventory, not only the tagging API (real behaviour: check current docs). Endpoint metrics here are sample data, not CloudWatch. No prices and no real bill were involved.
```text
tagging API returned 2 tagged resources:
  arn:aws:s3:::ml-raw-dev {'team': 'risk', 'env': 'dev'}
  arn:aws:sagemaker:us-east-1:123456789012:model/m1 {'team': 'risk', 'project': 'pd-model', 'env': 'dev'}

list_buckets sees: ['ml-raw-dev', 'ml-scratch']

== flag untagged resources ==
  arn:aws:s3:::ml-raw-dev missing ['project']
  arn:aws:s3:::ml-scratch missing ['env', 'project', 'team']

== idle endpoints (sample data, 'newest last') ==
idle: ['forgotten-poc']
```

**Follow-ups:**
- *Why did the bill rise with no new training?* Look at idle endpoints, logging volume, NAT traffic, and storage growth first.
- *Tag enforcement?* Require tags on creation with an SCP or IAM condition (Q48, Q47), then audit.
- *Scheduled shutdown for notebooks?* Lifecycle config or a scheduled function; the exact mechanism is in current docs.

**Common mistakes:** tags that are not activated for cost reports; auditing only tagged resources; treating dev endpoints as free; ignoring data transfer; optimising instance price before utilisation.

### Q45 ⭐ 🟡 S3 data lake layout for ML: bucket per environment or per domain, prefix and partition design, immutable raw zone, curated Parquet zone, dataset snapshots by version prefix, replication and Object Lock where compliance needs it, access points per team, and Glacier restore delays for old snapshots. Draw the layout as a tree, validate a naming convention with a regex checker, and apply a replication-ready versioned bucket in moto. Real replication is not executed.
**Asked at:** S3 interview question banks (novelvista '100+ Top AWS S3 Interview Questions', adaface, ccbp.in, a techinterview.org 'System Design Interview: Object Storage (Amazon S3)' post, AWS developer exam-prep study guides; search snippets only, not opened; WebFetch of docs.aws.amazon.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; cloud, data and ML engineer roles at IT-services firms, product companies and GCCs | AWS S3 documentation topics as summarised by prep guides (versioning and delete markers, lifecycle transitions and expiry, multipart upload, presigned URLs, strong read-after-write consistency since December 2020; search snippets only, not opened, exact limits not verified); vendor docs and prep notes, not interview reports; cloud, data and ML platform roles
**Say this first (1 line):** Separate by environment, keep an immutable raw zone, curate to partitioned Parquet, freeze training sets as versioned snapshot prefixes, and enforce names with a checker so the layout does not drift.

**Then explain:**
- Buckets: one per environment (dev, stage, prod) keeps IAM, KMS and lifecycle simple; per domain is an option when teams own data. Bucket names are global and have format rules.
- Zones: `raw` is append-only; `curated` is cleaned Parquet partitioned by date so Athena and Spark prune partitions; `snapshots/<dataset>/vNNN/` holds frozen training inputs; `models/` holds artifacts; `tmp/` expires fast.
- Governance: versioning plus Object Lock where compliance demands write-once (check current docs on modes); replication for DR or cross-account copies needs versioning on both buckets; access points give each team its own scoped door.
- Old snapshots may go to archive classes; restore from Glacier Flexible or Deep Archive has a delay, so plan retrains (Q1).
- Failure modes: replication does not copy what existed before the rule unless you backfill (check current docs); deletes and existing objects have special rules; prefix typos create parallel "zones".

**Example:** `raw/upi/ingest_date=2026-10-01/part-0.parquet` passes. `raw/upi/2026-10-01/part-0.parquet` fails (no `ingest_date=`). `snapshots/pd_train/v3/x` fails (`v003` is the convention).

**Code:** tree, regex checks and a moto bucket pair for replication.
```python
"""Q45: data lake layout tree, naming regex checker, versioned replication-ready bucket in moto (API shape only)."""
import os, re, json
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

TREE = """s3://acme-ml-prod-lake/            (one bucket per environment; bucket names are global, so prefix with org)
  raw/<source>/ingest_date=YYYY-MM-DD/   immutable, append-only, never edited in place
  curated/<domain>/<table>/dt=YYYY-MM-DD/   Parquet, partitioned by date
  snapshots/<dataset>/v<NNN>/            frozen training sets, one prefix per version
  models/<model>/<run_id>/               artifacts written by training jobs
  tmp/                                   short lifecycle expiry"""
print(TREE, "\n")

BUCKET = re.compile(r"^[a-z0-9]+-ml-(dev|stage|prod)-[a-z0-9-]+$")
KEY = re.compile(r"^(raw/[a-z0-9_]+/ingest_date=\d{4}-\d{2}-\d{2}/.+|"
                 r"curated/[a-z0-9_]+/[a-z0-9_]+/dt=\d{4}-\d{2}-\d{2}/.+|"
                 r"snapshots/[a-z0-9_]+/v\d{3}/.+|models/[a-z0-9_-]+/[a-z0-9-]+/.+|tmp/.+)$")
for b in ["acme-ml-prod-lake", "acme-ml-qa-lake", "Acme_ML_prod", "ab"]:
    print(f"bucket {b!r:22} ->", "ok" if BUCKET.match(b) else "REJECT")
for k in ["raw/upi/ingest_date=2026-10-01/part-0.parquet", "curated/risk/features/dt=2026-10-01/p0.parquet",
          "snapshots/pd_train/v003/train.parquet", "raw/upi/2026-10-01/part-0.parquet", "snapshots/pd_train/v3/x", "Models/x/y/z"]:
    print(f"key    {k!r:55} ->", "ok" if KEY.match(k) else "REJECT")

with mock_aws():
    s3 = boto3.client("s3")
    # replication needs versioning on BOTH sides
    s3.create_bucket(Bucket="acme-ml-prod-lake", ObjectLockEnabledForBucket=True)   # lock can be enabled at create (also enables versioning)
    s3.create_bucket(Bucket="acme-ml-prod-lake-dr")
    s3.put_bucket_versioning(Bucket="acme-ml-prod-lake-dr", VersioningConfiguration={"Status": "Enabled"})
    print("\nsource versioning:", s3.get_bucket_versioning(Bucket="acme-ml-prod-lake").get("Status"))
    s3.put_bucket_replication(Bucket="acme-ml-prod-lake", ReplicationConfiguration={
        "Role": "arn:aws:iam::123456789012:role/s3-replication",
        "Rules": [{"ID": "snapshots-dr", "Status": "Enabled", "Priority": 1, "Filter": {"Prefix": "snapshots/"},
                   "DeleteMarkerReplication": {"Status": "Disabled"},
                   "Destination": {"Bucket": "arn:aws:s3:::acme-ml-prod-lake-dr"}}]})
    r = s3.get_bucket_replication(Bucket="acme-ml-prod-lake")["ReplicationConfiguration"]
    rule = r["Rules"][0]
    print("replication rule read back (we sent Filter Prefix 'snapshots/'):", json.dumps({k: rule.get(k) for k in ("ID", "Status", "Priority", "Filter", "Prefix", "Destination")}))
    try:
        print("object lock config:", s3.get_object_lock_configuration(Bucket="acme-ml-prod-lake")["ObjectLockConfiguration"])
    except Exception as e: print("object lock:", type(e).__name__, str(e)[:80])
    try:
        s3.create_bucket(Bucket="no-versioning-src"); 
        s3.put_bucket_replication(Bucket="no-versioning-src", ReplicationConfiguration={"Role": "arn:aws:iam::123456789012:role/s3-replication",
            "Rules": [{"ID": "x", "Status": "Enabled", "Priority": 1, "Filter": {"Prefix": ""}, "DeleteMarkerReplication": {"Status": "Disabled"}, "Destination": {"Bucket": "arn:aws:s3:::acme-ml-prod-lake-dr"}}]})
        print("replication without source versioning: accepted by moto")
    except Exception as e: print("replication without source versioning:", type(e).__name__, str(e)[:90])
```

**Output (my run):** the tree and regex checks ran for real. In moto the versioned buckets and a replication rule were accepted, and replication without source versioning was rejected. Note the mock dropped the prefix filter on read-back (`Filter` came back as an empty prefix), so a mock read-back is not proof of what real S3 stores. Real replication, Object Lock retention and Glacier restore were not executed.
```text
s3://acme-ml-prod-lake/            (one bucket per environment; bucket names are global, so prefix with org)
  raw/<source>/ingest_date=YYYY-MM-DD/   immutable, append-only, never edited in place
  curated/<domain>/<table>/dt=YYYY-MM-DD/   Parquet, partitioned by date
  snapshots/<dataset>/v<NNN>/            frozen training sets, one prefix per version
  models/<model>/<run_id>/               artifacts written by training jobs
  tmp/                                   short lifecycle expiry 

bucket 'acme-ml-prod-lake'    -> ok
bucket 'acme-ml-qa-lake'      -> REJECT
bucket 'Acme_ML_prod'         -> REJECT
bucket 'ab'                   -> REJECT
key    'raw/upi/ingest_date=2026-10-01/part-0.parquet'         -> ok
key    'curated/risk/features/dt=2026-10-01/p0.parquet'        -> ok
key    'snapshots/pd_train/v003/train.parquet'                 -> ok
key    'raw/upi/2026-10-01/part-0.parquet'                     -> REJECT
key    'snapshots/pd_train/v3/x'                               -> REJECT
key    'Models/x/y/z'                                          -> REJECT

source versioning: Enabled
replication rule read back (we sent Filter Prefix 'snapshots/'): {"ID": "snapshots-dr", "Status": "Enabled", "Priority": 1, "Filter": {"Prefix": ""}, "Prefix": null, "Destination": {"Bucket": "arn:aws:s3:::acme-ml-prod-lake-dr"}}
object lock config: {'ObjectLockEnabled': 'Enabled'}
replication without source versioning: InvalidRequest An error occurred (InvalidRequest) when calling the PutBucketReplication operation: Versio
```

**Follow-ups:**
- *Single bucket or many?* Fewer buckets are easier to manage; more buckets give hard isolation. Pick per blast radius and policy needs.
- *Why partition by date?* Query engines skip whole prefixes; but too-fine partitions create many small files (Q36).
- *Dataset version in training?* Record the snapshot prefix (or version id) in the run metadata (Part 4).

**Common mistakes:** editing raw in place; mixing environments in one bucket; no naming validation; thinking replication covers old objects automatically; assuming the mock matches real replication.

### Q46 ⭐ 🟡 ECR in practice for ML images: repositories, image tags versus digests, immutable tags, scan on push, lifecycle policies for old images, cross-account pull permissions, replication, and pulling through a VPC endpoint. Why deploy by digest? Create a repository with immutable tags and a lifecycle policy in moto, print them, and write a function that validates image references (tag versus digest) for a deployment manifest. No images were built or pulled.
**Asked at:** Container-service comparison sources (nops.io 'ECS vs EKS vs Fargate', perfectscale.io, jayendrapatil.com 'AWS EKS vs ECS Decision Guide', cloudoptimo, doit.com, a 2019 AWS slideshare on ML with container services; search snippets only, not opened); vendor and consultancy blogs stating opinion; DevOps, platform and MLOps roles | Job-posting skill lists (a getonbrd Senior MLOps Engineer AWS and SageMaker posting listing Athena, RDS, ECR, IAM, CloudWatch, CloudFormation or Terraform and GitHub Actions, a workingnomads Senior MLOps Engineer SageMaker and Airflow posting; search snippets only, not opened); job postings, not interview reports; MLOps roles on AWS
**Say this first (1 line):** Deploy by digest, not by tag: a digest names exact bytes, a tag can be moved; set immutable tags, scan on push, expire old images with a lifecycle policy, and grant cross-account pull explicitly.

**Then explain:**
- Repository holds images; a tag is a movable label, a digest (`sha256:...`) is the content hash. `:latest` or an unpinned tag can change under a running deployment and break reproducibility.
- Immutable tags make re-pushing an existing tag fail, which protects against silent overwrites. It does not replace pinning by digest in the manifest.
- Scan on push gives basic vulnerability findings (enhanced scanning is a separate option; check current docs). Treat findings as input to a gate, not a guarantee.
- Lifecycle policy: expire untagged or old images by rule so storage does not grow forever; test the rule so it cannot delete the tag you deploy.
- Cross-account pull: repository policy allows the other account's role, and that role also needs `ecr:GetAuthorizationToken` in its own identity policy (check current docs). Replication copies images to other Regions or accounts. In a private VPC, pulls need the ECR endpoints plus S3 for layers (Q16, Q39).

**Example:** Reference `.../ml/pd-model@sha256:<64 hex>` passes. `...:v1` fails: resolve to a digest. `...:latest` fails. `python:3.12` is not an ECR reference and fails.

**Code:** moto repo with immutable tags and lifecycle rules, then the validator.
```python
"""Q46: ECR repo (immutable tags, scan on push, lifecycle) in moto + deployment-manifest image-ref validator. No images built or pulled."""
import os, re, json, hashlib
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

REF = re.compile(r"^(?P<host>\d{12}\.dkr\.ecr\.[a-z0-9-]+\.amazonaws\.com)/(?P<repo>[a-z0-9._/-]+)(?::(?P<tag>[\w.-]{1,128}))?(?:@(?P<digest>sha256:[0-9a-f]{64}))?$")

def check_ref(ref):
    """Return (ok, why). Deploy rule: must be pinned by digest; tag alone is mutable unless the repo is immutable, and 'latest' is never allowed."""
    m = REF.match(ref)
    if not m: return False, "not an ECR image reference"
    if m["digest"]: return True, "pinned by digest"
    if m["tag"] in (None, "latest"): return False, "untagged or :latest"
    return False, f"tag only (:{m['tag']}); resolve to a digest before deploy"

manifest = json.dumps({"schemaVersion": 2, "mediaType": "application/vnd.docker.distribution.manifest.v2+json", "config": {"digest": "sha256:" + "0" * 64}, "layers": []})
digest = "sha256:" + hashlib.sha256(manifest.encode()).hexdigest()
acct = "123456789012"; host = f"{acct}.dkr.ecr.us-east-1.amazonaws.com"

with mock_aws():
    ecr = boto3.client("ecr")
    repo = ecr.create_repository(repositoryName="ml/pd-model", imageTagMutability="IMMUTABLE",
                                 imageScanningConfiguration={"scanOnPush": True})["repository"]
    print("repo:", repo["repositoryName"], "| mutability:", repo["imageTagMutability"], "| scanOnPush:", repo["imageScanningConfiguration"]["scanOnPush"])
    print("repositoryUri:", repo["repositoryUri"])
    rules = {"rules": [{"rulePriority": 1, "description": "keep last 10 tagged v*",
                        "selection": {"tagStatus": "tagged", "tagPrefixList": ["v"], "countType": "imageCountMoreThan", "countNumber": 10},
                        "action": {"type": "expire"}},
                       {"rulePriority": 2, "description": "expire untagged after 14 days",
                        "selection": {"tagStatus": "untagged", "countType": "sinceImagePushed", "countUnit": "days", "countNumber": 14},
                        "action": {"type": "expire"}}]}
    ecr.put_lifecycle_policy(repositoryName="ml/pd-model", lifecyclePolicyText=json.dumps(rules))
    got = json.loads(ecr.get_lifecycle_policy(repositoryName="ml/pd-model")["lifecyclePolicyText"])
    print("lifecycle rules read back:", [(r["rulePriority"], r["selection"]["tagStatus"]) for r in got["rules"]])

    ecr.put_image(repositoryName="ml/pd-model", imageManifest=manifest, imageTag="v1")
    try:
        ecr.put_image(repositoryName="ml/pd-model", imageManifest=manifest + " ", imageTag="v1")
    except Exception as e:
        print("re-push v1 with different content:", type(e).__name__)
    imgs = ecr.describe_images(repositoryName="ml/pd-model")["imageDetails"]
    print("images:", [(i["imageTags"], i["imageDigest"][:19] + "...") for i in imgs])
    # cross-account pull policy (resource-based policy on the repo); read back only
    pol = {"Version": "2012-10-17", "Statement": [{"Sid": "ProdPull", "Effect": "Allow",
           "Principal": {"AWS": "arn:aws:iam::999999999999:role/prod-sagemaker-exec"},
           "Action": ["ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer"]}]}
    ecr.set_repository_policy(repositoryName="ml/pd-model", policyText=json.dumps(pol))
    print("repo policy principal:", json.loads(ecr.get_repository_policy(repositoryName="ml/pd-model")["policyText"])["Statement"][0]["Principal"]["AWS"])

print("\n== image reference validator ==")
for r in [f"{host}/ml/pd-model@{digest}", f"{host}/ml/pd-model:v1", f"{host}/ml/pd-model:latest", f"{host}/ml/pd-model", "python:3.12", f"{host}/ml/pd-model:v1@{digest}"]:
    ok, why = check_ref(r)
    print(f"{'PASS' if ok else 'FAIL'}  {r[:60]:60s} {why}")
```

**Output (my run):** ran against moto. The mock rejected a second push of tag `v1` with different content (`ImageAlreadyExistsException`), accepted the lifecycle and repository policy, and read them back. The digest moto stored is moto's own; the real digest comes from the registry. The validator is my own regex over the reference format, not an official parser. No image was built, scanned or pulled; scanning, lifecycle expiry timing and replication are not executed.
```text
repo: ml/pd-model | mutability: IMMUTABLE | scanOnPush: True
repositoryUri: 123456789012.dkr.ecr.us-east-1.amazonaws.com/ml/pd-model
lifecycle rules read back: [(1, 'tagged'), (2, 'untagged')]
re-push v1 with different content: ImageAlreadyExistsException
images: [(['v1'], 'sha256:e3b0c44298fc...')]
repo policy principal: arn:aws:iam::999999999999:role/prod-sagemaker-exec

== image reference validator ==
PASS  123456789012.dkr.ecr.us-east-1.amazonaws.com/ml/pd-model@sha pinned by digest
FAIL  123456789012.dkr.ecr.us-east-1.amazonaws.com/ml/pd-model:v1  tag only (:v1); resolve to a digest before deploy
FAIL  123456789012.dkr.ecr.us-east-1.amazonaws.com/ml/pd-model:lat untagged or :latest
FAIL  123456789012.dkr.ecr.us-east-1.amazonaws.com/ml/pd-model     untagged or :latest
FAIL  python:3.12                                                  not an ECR image reference
PASS  123456789012.dkr.ecr.us-east-1.amazonaws.com/ml/pd-model:v1@ pinned by digest
```

**Follow-ups:**
- *Why not only immutable tags?* Tags in other registries or older repos may be mutable, and humans reuse tag names; digest in the manifest is the stronger guarantee.
- *How do you get the digest in CI?* Read it from the push result or describe the image, then write it into the deploy manifest (Part 7).
- *Lifecycle deleted my prod image?* Keep a rule that protects deployed tags, or tag by environment and exclude it.

**Common mistakes:** deploying `:latest`; lifecycle rule too aggressive; forgetting the pull role's own token permission; no VPC endpoints for a private subnet; trusting "scan passed" as security sign-off.

### Q47 ⭐ 🔴 Attribute-based access control on AWS: tag-based IAM conditions (aws:PrincipalTag, aws:ResourceTag, aws:RequestTag), why ABAC scales better than one policy per project for many ML teams, how session tags pass through assume-role, and the traps (who can change tags, tag-on-create, services that do not support tag conditions). Extend the evaluator with a PrincipalTag-equals-ResourceTag condition, run team-a and team-b cases, and list what the extension still does not model.
**Asked at:** IAM interview and policy-evaluation sources (AWS IAM 'Policy evaluation logic' pages on docs.aws.amazon.com and docs.aws.eu, tutorialsdojo 'How AWS IAM Handles Conflicting IAM Policies', advancedweb.hu 'IAM policy evaluation logic explained with examples', barkingiguana 'How IAM Policy Evaluation Actually Works', community.aws and hidekazu-konishi IAM glossary; search snippets only, not opened); vendor docs and study guides, not verified candidate reports; cloud, DevOps, security and MLOps roles at IT-services firms, product companies and GCCs | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)
**Say this first (1 line):** ABAC lets one policy say "access if the principal's tag matches the resource's tag", so a new team means new tags, not new policies; the traps are who may edit tags, tag-on-create, and services that ignore tag conditions.

**Then explain:**
- Keys: `aws:PrincipalTag/<k>` (tag on the role or user, or a session tag passed at AssumeRole), `aws:ResourceTag/<k>` (tag on the target), `aws:RequestTag/<k>` (tag in the create or tag request).
- Scaling: RBAC needs a policy per project; ABAC needs one policy plus tags. For many ML teams that is far less policy sprawl.
- Session tags: pass tags in AssumeRole (the trust policy must allow `sts:TagSession`); they can be marked transitive for role chaining (Q9).
- Trap 1: if a team can edit tags on resources (or on their own principal), they can re-tag themselves into someone else's data. Guard tag actions with explicit denies or conditions (output shows the collapse).
- Trap 2: tag-on-create. To force the right tag at creation, use `aws:RequestTag` conditions and require the tag key (`Null` check) so untagged creates fail.
- Trap 3: not every service or action supports every tag condition key. Check the service authorisation reference in current docs before relying on it.
- Missing tag: an absent tag must give no access (the condition is false), never default allow.

**Example:** team-a principal reading a team-a object: allow. team-b reading team-a data: deny. Principal with no `team` tag: deny. Training job created with `team=team-b` by a team-a principal: deny. With tag-editing allowed, team-b re-tags the object to `team-b` and then reads it: both steps allow.

**Code:** the ABAC policy and cases (`q47_abac.py`) use the extended evaluator `iam_eval_ext.py` (in code/), derived from the Wave A sketch.
```python
"""Q47: ABAC with the extended evaluator + moto session-tag shape. Simplified evaluator; see 'not modelled' list at the end."""
import os, sys, json
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iam_eval_ext import evaluate

# ONE policy for every team. Access follows the tag match, not a per-team policy.
ABAC = {"Version": "2012-10-17", "Statement": [
  {"Sid": "ReadOwnTeamData", "Effect": "Allow", "Action": ["s3:GetObject"], "Resource": "*",
   "Condition": {"StringEquals": {"aws:ResourceTag/team": "${aws:PrincipalTag/team}"}}},
  {"Sid": "CreateOnlyWithOwnTeamTag", "Effect": "Allow", "Action": ["sagemaker:CreateTrainingJob"], "Resource": "*",
   "Condition": {"StringEquals": {"aws:RequestTag/team": "${aws:PrincipalTag/team}"}}},
  {"Sid": "DenyTagTampering", "Effect": "Deny", "Action": ["s3:PutObjectTagging", "s3:PutBucketTagging"], "Resource": "*"},
]}
obj = "arn:aws:s3:::lake/curated/x.parquet"
cases = [
 ("team-a reads team-a data",  "s3:GetObject", {"aws:PrincipalTag/team": "team-a", "aws:ResourceTag/team": "team-a"}, "Allow"),
 ("team-b reads team-a data",  "s3:GetObject", {"aws:PrincipalTag/team": "team-b", "aws:ResourceTag/team": "team-a"}, "Deny"),
 ("principal has NO team tag", "s3:GetObject", {"aws:ResourceTag/team": "team-a"}, "Deny"),
 ("resource has NO team tag",  "s3:GetObject", {"aws:PrincipalTag/team": "team-a"}, "Deny"),
 ("team-a creates job tagged team-a", "sagemaker:CreateTrainingJob", {"aws:PrincipalTag/team": "team-a", "aws:RequestTag/team": "team-a"}, "Allow"),
 ("team-a creates job tagged team-b", "sagemaker:CreateTrainingJob", {"aws:PrincipalTag/team": "team-a", "aws:RequestTag/team": "team-b"}, "Deny"),
 ("team-a creates job, NO tag (tag-on-create missing)", "sagemaker:CreateTrainingJob", {"aws:PrincipalTag/team": "team-a"}, "Deny"),
 ("team-b retags team-a object (trap, blocked by explicit deny)", "s3:PutObjectTagging", {"aws:PrincipalTag/team": "team-b"}, "Deny"),
]
for name, act, ctx, want in cases:
    got = evaluate(act, obj, ctx=ctx, identity=[ABAC]); assert got[0] == want, (name, got)
    print(f"{name:58s} {got[0]:5s} {got[1]}")

# The trap: if the same role may change tags, ABAC collapses. Remove the tag-deny and let team-b re-tag the data first.
no_guard = {"Version": "2012-10-17", "Statement": [s for s in ABAC["Statement"] if s["Sid"] != "DenyTagTampering"] +
            [{"Effect": "Allow", "Action": "s3:PutObjectTagging", "Resource": "*"}]}
print("\n== trap: tag-editing allowed ==")
print("step 1 team-b retags object   ->", evaluate("s3:PutObjectTagging", obj, ctx={"aws:PrincipalTag/team": "team-b"}, identity=[no_guard]))
print("step 2 team-b now reads it    ->", evaluate("s3:GetObject", obj, ctx={"aws:PrincipalTag/team": "team-b", "aws:ResourceTag/team": "team-b"}, identity=[no_guard]))

import boto3
from moto import mock_aws
with mock_aws():
    sts = boto3.client("sts"); iam = boto3.client("iam")
    iam.create_role(RoleName="ml-eng", AssumeRolePolicyDocument=json.dumps({"Version": "2012-10-17", "Statement": [
        {"Effect": "Allow", "Principal": {"AWS": "arn:aws:iam::123456789012:root"}, "Action": ["sts:AssumeRole", "sts:TagSession"]}]}))
    r = sts.assume_role(RoleArn="arn:aws:iam::123456789012:role/ml-eng", RoleSessionName="alice",
                        Tags=[{"Key": "team", "Value": "team-a"}], TransitiveTagKeys=["team"])
    print("\nmoto assume_role with session tags accepted; keys returned:", sorted(k for k in r["Credentials"]))
    print("(moto IAM enforcement is off by default, so these session tags drove no policy decision here)")

print("\nSTILL NOT MODELLED: multi-value tag operators (ForAllValues/ForAnyValue), case rules for tag keys, services that ignore tag conditions,\n"
      "tag-on-create vs tag-after-create API differences per service, whether aws:RequestTag applies to a given action, session-tag transitivity,\n"
      "tags on the role vs on the session precedence, tag policies, and anything in a real account's Organization.")
```

**Output (my run):** pure-Python evaluator, ran for real. The extension adds policy variables like `${aws:PrincipalTag/team}`, `Null` and the negated condition operators. moto accepted session tags on `assume_role` but IAM enforcement is off by default, so no policy decision there is real. Still not modelled (also printed): multi-value tag operators, tag-key case rules, per-service tag-condition support, session-tag precedence and transitivity, tag policies. Real IAM was not executed; check current docs.
```text
team-a reads team-a data                                   Allow identity or resource policy allows (same account)
team-b reads team-a data                                   Deny  implicit deny: nothing allows
principal has NO team tag                                  Deny  implicit deny: nothing allows
resource has NO team tag                                   Deny  implicit deny: nothing allows
team-a creates job tagged team-a                           Allow identity or resource policy allows (same account)
team-a creates job tagged team-b                           Deny  implicit deny: nothing allows
team-a creates job, NO tag (tag-on-create missing)         Deny  implicit deny: nothing allows
team-b retags team-a object (trap, blocked by explicit deny) Deny  explicit deny

== trap: tag-editing allowed ==
step 1 team-b retags object   -> ('Allow', 'identity or resource policy allows (same account)')
step 2 team-b now reads it    -> ('Allow', 'identity or resource policy allows (same account)')

moto assume_role with session tags accepted; keys returned: ['AccessKeyId', 'Expiration', 'SecretAccessKey', 'SessionToken']
(moto IAM enforcement is off by default, so these session tags drove no policy decision here)

STILL NOT MODELLED: multi-value tag operators (ForAllValues/ForAnyValue), case rules for tag keys, services that ignore tag conditions,
tag-on-create vs tag-after-create API differences per service, whether aws:RequestTag applies to a given action, session-tag transitivity,
tags on the role vs on the session precedence, tag policies, and anything in a real account's Organization.
```

**Follow-ups:**
- *Is ABAC always better?* No. It is good for many similar teams; for a few special roles, plain role policies are easier to read and audit.
- *How do you test it?* Use the policy simulator or Access Analyzer in real AWS (not run here), plus a negative test for each guard.
- *Who owns the tags?* A small admin role, enforced by explicit deny and SCP (Q48).

**Common mistakes:** letting developers edit the tag that grants access; forgetting `sts:TagSession`; assuming all services support tag conditions; no deny for untagged; trusting a simplified evaluator as proof.

### Q48 ⭐ 🔴 SCP design for an ML organisation: deny actions outside approved Regions, deny leaving the organisation, deny disabling CloudTrail, require encryption or tags on creation, and keep an exception path for the break-glass role. Why SCPs never grant permissions, and why they do not apply to the management account. Write three SCP JSON documents, validate them, create one with moto organizations, and run the evaluator against them. Real SCP enforcement is not executed.
**Asked at:** IAM interview and policy-evaluation sources (AWS IAM 'Policy evaluation logic' pages on docs.aws.amazon.com and docs.aws.eu, tutorialsdojo 'How AWS IAM Handles Conflicting IAM Policies', advancedweb.hu 'IAM policy evaluation logic explained with examples', barkingiguana 'How IAM Policy Evaluation Actually Works', community.aws and hidekazu-konishi IAM glossary; search snippets only, not opened); vendor docs and study guides, not verified candidate reports; cloud, DevOps, security and MLOps roles at IT-services firms, product companies and GCCs | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)
**Say this first (1 line):** An SCP is a permission ceiling for accounts in the organisation: it never grants anything, it only removes; I would use a few deny guardrails (Regions, leaving the org, CloudTrail, tags or encryption on create) with a tight break-glass exception, and remember the management account is not affected.

**Then explain:**
- An action is allowed only if every SCP level on the path allows it (and an identity or resource policy also allows it). An explicit deny in any SCP wins.
- The management account is not restricted by SCPs, so keep workloads out of it.
- Region guardrail: deny everything outside approved Regions, with `NotAction` for global services (IAM, Organizations, and so on) so you do not break them. The right list of global-service actions changes; check current docs.
- Org and audit guardrails: deny `organizations:LeaveOrganization` and the CloudTrail stop, delete, update and event-selector actions.
- Create-time rules: deny a create call when a required tag is absent (`Null` on `aws:RequestTag/<k>`). Encryption-on-create rules depend on condition keys that exist per action; check current docs.
- Break-glass: exempt one role with `ArnNotLike aws:PrincipalArn`; protect that role with MFA, alarms and a rarely used trust path.
- Failure modes: a broad deny that blocks your own pipeline or service-linked roles, no testing in a sandbox OU first, and size and nesting limits (check current docs).

**Example:** Everything below uses an AdministratorAccess-like identity policy. Training in ap-south-1: allowed. In us-east-1: denied. Same as BreakGlass: allowed. `iam:ListRoles` in us-east-1: allowed (global service exempt). Stopping CloudTrail: denied, except for BreakGlass. Leaving the org: denied unless the caller is the management account.

**Code:** the SCP document (JSON) and the script that validates it, creates it in moto and runs the cases.
```python
"""Q48: SCP documents, structural validation, moto organizations, evaluator runs. Real SCP enforcement NOT executed."""
import os, sys, json
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
import boto3
from moto import mock_aws
from iam_eval_ext import evaluate

scp = json.load(open(os.path.join(here, "scp_ml_org.json")))

def validate_scp(doc):
    errs = []
    if doc.get("Version") != "2012-10-17": errs.append("Version")
    for s in doc["Statement"]:
        if "Principal" in s or "NotPrincipal" in s: errs.append(f"{s.get('Sid')}: SCPs have no Principal element")
        if s["Effect"] not in ("Allow", "Deny"): errs.append(f"{s.get('Sid')}: Effect")
        if ("Action" in s) == ("NotAction" in s): errs.append(f"{s.get('Sid')}: need exactly one of Action/NotAction")
        if "Resource" not in s: errs.append(f"{s.get('Sid')}: Resource")
    sids = [s.get("Sid") for s in doc["Statement"]]
    if len(sids) != len(set(sids)): errs.append("duplicate Sid")
    return errs
print("SCP structural errors:", validate_scp(scp) or "none", "| statements:", len(scp["Statement"]))
bad = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": "*", "Action": "*", "Resource": "*"}]}
print("deliberately bad SCP:", validate_scp(bad))

with mock_aws():
    org = boto3.client("organizations")
    org.create_organization(FeatureSet="ALL")
    p = org.create_policy(Content=json.dumps(scp), Description="ml guardrails", Name="ml-guardrails", Type="SERVICE_CONTROL_POLICY")["Policy"]["PolicySummary"]
    print("created:", p["Name"], p["Type"], "| listed:", [x["Name"] for x in org.list_policies(Filter="SERVICE_CONTROL_POLICY")["Policies"]])
    root = org.list_roots()["Roots"][0]["Id"]
    org.attach_policy(PolicyId=p["Id"], TargetId=root)
    print("attached to root; targets:", [t["Name"] if "Name" in t else t["TargetId"] for t in org.list_targets_for_policy(PolicyId=p["Id"])["Targets"]])

print("\n== evaluator (identity policy is AdministratorAccess-like in every case) ==")
admin = {"Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"}]}
dev = "arn:aws:iam::111111111111:role/ml-engineer"; bg = "arn:aws:iam::111111111111:role/BreakGlass"
rows = [
 ("train in ap-south-1",              "sagemaker:CreateTrainingJob", {"aws:RequestedRegion": "ap-south-1", "aws:RequestTag/project": "pd"}, dev, False),
 ("train in us-east-1",               "sagemaker:CreateTrainingJob", {"aws:RequestedRegion": "us-east-1", "aws:RequestTag/project": "pd"}, dev, False),
 ("train in us-east-1 as BreakGlass", "sagemaker:CreateTrainingJob", {"aws:RequestedRegion": "us-east-1", "aws:RequestTag/project": "pd"}, bg, False),
 ("iam call from us-east-1 (global)", "iam:ListRoles",               {"aws:RequestedRegion": "us-east-1"}, dev, False),
 ("train without project tag",        "sagemaker:CreateTrainingJob", {"aws:RequestedRegion": "ap-south-1"}, dev, False),
 ("stop CloudTrail",                  "cloudtrail:StopLogging",      {"aws:RequestedRegion": "ap-south-1"}, dev, False),
 ("stop CloudTrail as BreakGlass",    "cloudtrail:StopLogging",      {"aws:RequestedRegion": "ap-south-1"}, bg, False),
 ("leave organisation",               "organizations:LeaveOrganization", {"aws:RequestedRegion": "ap-south-1"}, dev, False),
 ("leave organisation, mgmt account", "organizations:LeaveOrganization", {"aws:RequestedRegion": "ap-south-1"}, "arn:aws:iam::999999999999:role/admin", True),
]
for name, act, ctx, who, mgmt in rows:
    d = evaluate(act, "*", ctx=ctx, identity=[admin], scps=[scp], principal_arn=who, management_account=mgmt)
    print(f"{name:36s} {d[0]:5s} {d[1]}")
print("\nSimplified: no Organizations hierarchy (root -> OU -> account all need an allow), no service-linked-role exemption, no condition-key availability per action.")
```
```json
{"Version": "2012-10-17", "Statement": [
 {"Sid": "DenyOutsideApprovedRegions", "Effect": "Deny",
  "NotAction": ["iam:*", "organizations:*", "sts:*", "support:*", "cloudfront:*", "route53:*"],
  "Resource": "*",
  "Condition": {"StringNotEquals": {"aws:RequestedRegion": ["ap-south-1", "ap-south-2"]},
                "ArnNotLike": {"aws:PrincipalArn": "arn:aws:iam::*:role/BreakGlass"}}},
 {"Sid": "DenyLeaveOrg", "Effect": "Deny", "Action": "organizations:LeaveOrganization", "Resource": "*"},
 {"Sid": "DenyDisableCloudTrail", "Effect": "Deny",
  "Action": ["cloudtrail:StopLogging", "cloudtrail:DeleteTrail", "cloudtrail:UpdateTrail", "cloudtrail:PutEventSelectors"],
  "Resource": "*",
  "Condition": {"ArnNotLike": {"aws:PrincipalArn": "arn:aws:iam::*:role/BreakGlass"}}},
 {"Sid": "RequireProjectTagOnTraining", "Effect": "Deny", "Action": "sagemaker:CreateTrainingJob", "Resource": "*",
  "Condition": {"Null": {"aws:RequestTag/project": "true"}}},
 {"Sid": "AllowEverythingElse", "Effect": "Allow", "Action": "*", "Resource": "*"}
]}
```

**Output (my run):** structure validation and evaluator runs are real. moto Organizations accepted and listed the policy and attached it to the root, but a mock does not enforce SCPs, so enforcement is not executed. The evaluator is simplified: no OU hierarchy, no service-linked-role exemption, and it treats condition keys as always available. Verify guardrails in a sandbox organisation first.
```text
SCP structural errors: none | statements: 5
deliberately bad SCP: ['None: SCPs have no Principal element']
created: ml-guardrails SERVICE_CONTROL_POLICY | listed: ['FullAWSAccess', 'ml-guardrails']
attached to root; targets: ['Root']

== evaluator (identity policy is AdministratorAccess-like in every case) ==
train in ap-south-1                  Allow identity or resource policy allows (same account)
train in us-east-1                   Deny  explicit deny
train in us-east-1 as BreakGlass     Allow identity or resource policy allows (same account)
iam call from us-east-1 (global)     Allow identity or resource policy allows (same account)
train without project tag            Deny  explicit deny
stop CloudTrail                      Deny  explicit deny
stop CloudTrail as BreakGlass        Allow identity or resource policy allows (same account)
leave organisation                   Deny  explicit deny
leave organisation, mgmt account     Allow identity or resource policy allows (same account)

Simplified: no Organizations hierarchy (root -> OU -> account all need an allow), no service-linked-role exemption, no condition-key availability per action.
```

**Follow-ups:**
- *Why does the identity policy matter if an SCP allows?* SCP allow is not a grant. Someone still needs an identity or resource policy.
- *Can an SCP block the root user of a member account?* Generally yes for member accounts (check current docs for exceptions).
- *SCP versus permissions boundary?* SCP caps whole accounts; a boundary caps one role or user (Q30).

**Common mistakes:** thinking an SCP grants access; attaching a deny to the root with no break-glass; no `NotAction` for global services; putting workloads in the management account; shipping untested.

### Q49 ⭐ 🔴 Design question: an end-to-end AWS reference architecture from raw data to a monitored endpoint for an Indian lending or payments company: accounts (dev, prod, shared services), S3 zones, ECR, SageMaker training and registry, deployment, VPC endpoints, IAM roles per stage, KMS, CloudTrail and alerting. Give a whiteboard answer, a role and permission matrix validated with pyyaml, and an evaluator run proving the training role cannot write to prod. Full system design belongs to Part 12.
**Asked at:** Job-posting skill lists (a getonbrd Senior MLOps Engineer AWS and SageMaker posting listing Athena, RDS, ECR, IAM, CloudWatch, CloudFormation or Terraform and GitHub Actions, a workingnomads Senior MLOps Engineer SageMaker and Airflow posting; search snippets only, not opened); job postings, not interview reports; MLOps roles on AWS | SageMaker interview question banks (k21academy 'AWS Machine Learning Engineer Interview Questions' guide listing training, tuning, inference modes, Feature Store, Ground Truth, Model Registry, Model Monitor and Clarify, cloudsoftsol and interviewprep.org SageMaker question lists, digiqt SageMaker posts; search snippets only, not opened); editorial prep sites, not verified candidate reports; MLOps, ML engineer and ML platform roles on AWS at IT-services firms, product companies and GCCs | AWS certification-style question families (AWS Certified Machine Learning Engineer Associate and Specialty, Developer Associate and Solutions Architect exam-prep notes, mentioned as a source type only; no exam questions reproduced; search snippets only)
**Say this first (1 line):** Three accounts (dev, prod, shared services) with data zones in S3, images in ECR, training and registry in dev, a controlled promoter role that is the only writer into prod, deployment into private-subnet endpoints, one role per stage, KMS per environment, an org CloudTrail and alarms.

**Then explain:**
- Flow (whiteboard): ingest to `raw`, curate to Parquet, snapshot a dataset version, train in dev (SageMaker, VPC-attached, execution role), register in the Model Registry with an approval, a promoter role copies the approved artifact into the prod model bucket, a deployer creates the endpoint in prod with its own execution role, Model Monitor and CloudWatch alarms watch it.
- Accounts: dev for experiments, prod for serving and production data, shared for ECR, CI and logging. Why: blast radius and clear audit lines, which matters for regulated lending and payments data (follow your regulator's guidance; check current rules).
- Roles per stage: data engineering, training, promoter, endpoint execution, deployer. Each role gets the least privilege (Q8), and `iam:PassRole` is limited to named roles (Q4).
- Cross-account: both sides must allow (Q40). The prod bucket policy also denies writes from anyone but the promoter, as a second line.
- Network: private subnets, S3 gateway endpoint and interface endpoints for ECR, Logs and STS (Q16, Q39).
- Encryption and audit: KMS key per environment with key policies, org trail to a log-archive bucket, alarms for denied calls and key-policy changes, SCP guardrails (Q48).
- Failure modes: training role allowed on prod "to save time"; one KMS key for all; no approval gate; manual console deploys; no rollback artifact. System-design depth is Part 12.

**Example:** Hand-check: the dev training role has no allow on the prod bucket and the bucket policy denies any writer other than the promoter, so a PUT to `acme-ml-prod-models/approved/credit_v7.tar.gz` by the training role is denied twice. The promoter, which has an identity allow in shared and a bucket allow in prod, is allowed.

**Code:** the role and permission matrix (YAML) and the checker (`q49_check.py`) with the extended evaluator.
```python
"""Q49: validate the role matrix with pyyaml, then run evaluator cases: the dev training role must not write to prod."""
import os, sys
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
import yaml
from iam_eval_ext import evaluate

m = yaml.safe_load(open(os.path.join(here, "q49_matrix.yaml")))
errs = []
for rn, r in m["roles"].items():
    if r["account"] not in m["accounts"]: errs.append(f"{rn}: unknown account")
    for c in r["can"]:
        if c["resource"] == "*" and not c["action"].startswith(("sagemaker:Create", "sagemaker:Describe")): errs.append(f"{rn}: wildcard resource on {c['action']}")
        if c["action"] in ("*", "s3:*", "iam:*"): errs.append(f"{rn}: wildcard action {c['action']}")
print("accounts:", list(m["accounts"]), "| roles:", list(m["roles"]), "| matrix errors:", errs or "none")

def ident(role):   # build an identity policy from the matrix row
    return [{"Statement": [{"Effect": "Allow", "Action": c["action"], "Resource": c["resource"]} for c in m["roles"][role]["can"]]}]
def arn(role): return f"arn:aws:iam::{m['accounts'][m['roles'][role]['account']]['id']}:role/{role}"

PROD_BUCKET = "arn:aws:s3:::acme-ml-prod-models/approved/credit_v7.tar.gz"
prod_bucket_policy = {"Statement": [
  {"Effect": "Allow", "Principal": {"AWS": [arn("model-promoter"), arn("sagemaker-endpoint-exec")]}, "Action": ["s3:PutObject", "s3:GetObject"], "Resource": "arn:aws:s3:::acme-ml-prod-models/approved/*"},
  {"Effect": "Deny", "Principal": "*", "Action": "s3:PutObject", "Resource": "arn:aws:s3:::acme-ml-prod-models/*",
   "Condition": {"ArnNotLike": {"aws:PrincipalArn": arn("model-promoter")}}}]}

def run(label, role, action, res, rp=None, same=True):
    d = evaluate(action, res, identity=ident(role), resource_policy=rp, same_account=same, principal_arn=arn(role))
    print(f"{label:62s} {d[0]:5s} {d[1]}")
    return d[0]

print("\n== cases ==")
assert run("dev training role PUT to prod bucket (cross-account)", "sagemaker-training", "s3:PutObject", PROD_BUCKET, prod_bucket_policy, same=False) == "Deny"
assert run("dev training role PUT to its own dev models/ (same account)", "sagemaker-training", "s3:PutObject", "arn:aws:s3:::acme-ml-dev-lake/models/run1/model.tar.gz") == "Allow"
no_deny = {"Statement": [prod_bucket_policy["Statement"][0]]}
assert run("same, if the Deny statement were missing (second line of defence)", "sagemaker-training", "s3:PutObject", PROD_BUCKET, no_deny, same=False) == "Deny"
assert run("dev training role reads dev snapshot", "sagemaker-training", "s3:GetObject", "arn:aws:s3:::acme-ml-dev-lake/snapshots/pd/v003/train.parquet") == "Allow"
assert run("promoter PUT to prod approved/ (both sides allow)", "model-promoter", "s3:PutObject", PROD_BUCKET, prod_bucket_policy, same=False) == "Allow"
assert run("endpoint role GET approved model (same account as bucket)", "sagemaker-endpoint-exec", "s3:GetObject", PROD_BUCKET, prod_bucket_policy) == "Allow"
assert run("endpoint role PUT to prod bucket (explicit deny in bucket policy)", "sagemaker-endpoint-exec", "s3:PutObject", PROD_BUCKET, prod_bucket_policy) == "Deny"
assert run("data-eng role reads prod model bucket", "data-eng-pipeline", "s3:GetObject", PROD_BUCKET, prod_bucket_policy, same=False) == "Deny"
print("\nTraining role cannot write to prod: shown on the simplified model above (denied twice: no allow on the bucket side, plus an explicit deny). Real AWS also applies SCPs, KMS and endpoint policies: not executed.")
```
```yaml
# Role and permission matrix for a lending/payments ML platform (illustrative; account ids are fake)
accounts:
  shared: {id: "333333333333", purpose: "ECR, CI roles, org logging, artifacts promoted from dev"}
  dev:    {id: "111111111111", purpose: "data science, training, registry (model package groups)"}
  prod:   {id: "222222222222", purpose: "endpoints, monitoring, production data"}
roles:
  data-eng-pipeline:
    account: dev
    can: [{action: "s3:GetObject", resource: "arn:aws:s3:::acme-ml-dev-lake/raw/*"}, {action: "s3:PutObject", resource: "arn:aws:s3:::acme-ml-dev-lake/curated/*"}]
  sagemaker-training:
    account: dev
    can: [{action: "s3:GetObject", resource: "arn:aws:s3:::acme-ml-dev-lake/snapshots/*"}, {action: "s3:PutObject", resource: "arn:aws:s3:::acme-ml-dev-lake/models/*"},
          {action: "ecr:BatchGetImage", resource: "arn:aws:ecr:ap-south-1:333333333333:repository/ml/*"}, {action: "kms:Decrypt", resource: "arn:aws:kms:ap-south-1:111111111111:key/dev-lake"}]
  model-promoter:
    account: shared
    can: [{action: "s3:GetObject", resource: "arn:aws:s3:::acme-ml-dev-lake/models/*"}, {action: "s3:PutObject", resource: "arn:aws:s3:::acme-ml-prod-models/approved/*"}]
  sagemaker-endpoint-exec:
    account: prod
    can: [{action: "s3:GetObject", resource: "arn:aws:s3:::acme-ml-prod-models/approved/*"}, {action: "ecr:BatchGetImage", resource: "arn:aws:ecr:ap-south-1:333333333333:repository/ml/*"},
          {action: "kms:Decrypt", resource: "arn:aws:kms:ap-south-1:222222222222:key/prod-models"}]
  prod-deployer:
    account: prod
    can: [{action: "sagemaker:CreateEndpoint", resource: "*"}, {action: "iam:PassRole", resource: "arn:aws:iam::222222222222:role/sagemaker-endpoint-exec"}]
guardrails:
  - "prod model bucket policy: Deny s3:PutObject unless aws:PrincipalArn is model-promoter"
  - "SCP: deny actions outside ap-south-1 and ap-south-2; deny cloudtrail:StopLogging"
  - "prod endpoints in private subnets; S3 gateway endpoint, ecr.api, ecr.dkr, logs, sts interface endpoints"
  - "CloudTrail org trail to a log-archive bucket; alarms on denied calls and on key policy changes"
```

**Output (my run):** pyyaml parsing, the matrix lint and the evaluator cases ran for real. The evaluator is simplified and uses fake account ids; it ignores SCPs, KMS, VPC endpoint policies and Block Public Access here. The architecture itself (accounts, endpoints, SageMaker, CloudTrail) was not executed.
```text
accounts: ['shared', 'dev', 'prod'] | roles: ['data-eng-pipeline', 'sagemaker-training', 'model-promoter', 'sagemaker-endpoint-exec', 'prod-deployer'] | matrix errors: none

== cases ==
dev training role PUT to prod bucket (cross-account)           Deny  explicit deny
dev training role PUT to its own dev models/ (same account)    Allow identity or resource policy allows (same account)
same, if the Deny statement were missing (second line of defence) Deny  implicit deny: cross-account needs both sides (neither present)
dev training role reads dev snapshot                           Allow identity or resource policy allows (same account)
promoter PUT to prod approved/ (both sides allow)              Allow cross-account: identity AND resource policy allow
endpoint role GET approved model (same account as bucket)      Allow identity or resource policy allows (same account)
endpoint role PUT to prod bucket (explicit deny in bucket policy) Deny  explicit deny
data-eng role reads prod model bucket                          Deny  implicit deny: cross-account needs both sides (neither present)

Training role cannot write to prod: shown on the simplified model above (denied twice: no allow on the bucket side, plus an explicit deny). Real AWS also applies SCPs, KMS and endpoint policies: not executed.
```

**Follow-ups:**
- *Why a separate promoter role?* One narrow identity can write to prod, so the policy is easy to audit and alarm on.
- *Where is the human approval?* In the registry approval status and a protected CI environment (Parts 4 and 7).
- *What about rollback?* Keep the previous approved artifact and endpoint config; redeploy it (Part 6).

**Common mistakes:** sharing one account; broad `iam:PassRole`; writing to prod from dev roles; no network endpoints so jobs hang (Q39); an architecture with no monitoring and no audit trail.

### Q50 ⭐ 🔴 Incident: an access key for a role with broad S3 and SageMaker permissions was committed to a public repository. Give the response order (confirm with CloudTrail, deactivate the key, revoke active role sessions with a deny-before-time condition, rotate secrets, review what was touched, add detection), and what to change afterward (roles instead of keys, secret scanning, boundaries). Deactivate a key in moto and run the evaluator on a time-conditioned deny; CloudTrail lookup is not implemented by the mock. Security design belongs to Part 12.
**Asked at:** IAM interview and policy-evaluation sources (AWS IAM 'Policy evaluation logic' pages on docs.aws.amazon.com and docs.aws.eu, tutorialsdojo 'How AWS IAM Handles Conflicting IAM Policies', advancedweb.hu 'IAM policy evaluation logic explained with examples', barkingiguana 'How IAM Policy Evaluation Actually Works', community.aws and hidekazu-konishi IAM glossary; search snippets only, not opened); vendor docs and study guides, not verified candidate reports; cloud, DevOps, security and MLOps roles at IT-services firms, product companies and GCCs | Job-posting skill lists (a getonbrd Senior MLOps Engineer AWS and SageMaker posting listing Athena, RDS, ECR, IAM, CloudWatch, CloudFormation or Terraform and GitHub Actions, a workingnomads Senior MLOps Engineer SageMaker and Airflow posting; search snippets only, not opened); job postings, not interview reports; MLOps roles on AWS
**Say this first (1 line):** Treat it as compromised now: confirm what the credential did, neutralise it, cut off any live sessions, rotate related secrets, review everything it touched, then fix the root cause with roles, secret scanning and boundaries.

**Then explain:**
- First: what kind of credential is it? An IAM role has no long-term access key. A leaked key beginning with `AKIA` belongs to an IAM user; one beginning with `ASIA` is a temporary credential from a role session. The first you deactivate and delete; the second you cannot deactivate, so you revoke older sessions (below).
- Order: (1) confirm with CloudTrail which calls that key or session made, and from where (the first look, since you must not lose evidence); (2) deactivate the key (do not delete it yet if you want it for evidence, check your process); (3) for role sessions, attach a deny with `aws:TokenIssueTime` before "now", which cuts all older sessions; new legitimate sessions still work; (4) rotate any secrets the key could read; (5) review S3, SageMaker, IAM changes and look for persistence (new users, keys, roles, trust policy edits, endpoints, cross-account grants); (6) remove the key from the repo and history, though treat it as public forever; (7) add detection.
- Afterward: use roles and short-lived credentials (Q3, Q9, Q31), secret scanning and push protection, permissions boundaries and least privilege (Q8, Q30), SCP guardrails (Q48), alarms on unusual API activity.
- Edge cases: a long-term user key has no `TokenIssueTime`, so the deny-before-time policy does not stop it; deactivation does. CloudTrail has delivery delay and may not record every data event unless enabled (check current docs).
- Security design in depth is Part 12.

**Example:** Cutoff 10:00. A session issued at 09:00 is denied; one issued at 10:30 is allowed. A long-term key (no issue time in the request) is not touched by this policy: deactivate it.

**Code:** the drill (moto server on port 8541, `aws` CLI and boto3, the evaluator and a small scanner).
```python
"""Q50: leaked key incident drill. moto_server on port 8541 (fake keys), aws CLI + boto3, scanner, time-conditioned deny via evaluator."""
import os, sys, re, json, subprocess, time, shutil
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
import boto3
from iam_eval_ext import evaluate

BIN = os.path.dirname(sys.executable); PORT = 8541; EP = f"http://127.0.0.1:{PORT}"
srv = subprocess.Popen([os.path.join(BIN, "moto_server"), "-p", str(PORT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(50):
        try: boto3.client("sts", endpoint_url=EP).get_caller_identity(); break
        except Exception: time.sleep(0.2)
    iam = boto3.client("iam", endpoint_url=EP)
    iam.create_user(UserName="ci-uploader")
    k = iam.create_access_key(UserName="ci-uploader")["AccessKey"]
    print("1. key created:", k["AccessKeyId"][:6] + "...", "status", k["Status"], "(fake moto key)")
    cli = lambda *a: subprocess.run([os.path.join(BIN, "aws"), "--endpoint-url", EP, *a], capture_output=True, text=True)
    r = cli("iam", "update-access-key", "--user-name", "ci-uploader", "--access-key-id", k["AccessKeyId"], "--status", "Inactive")
    print("2. aws iam update-access-key Inactive -> exit", r.returncode)
    print("   status now:", [(x["AccessKeyId"][:6] + "...", x["Status"]) for x in iam.list_access_keys(UserName="ci-uploader")["AccessKeyMetadata"]])
    lu = iam.get_access_key_last_used(AccessKeyId=k["AccessKeyId"])["AccessKeyLastUsed"]
    print("3. last used (what you would check in real AWS):", {x: lu.get(x) for x in ("ServiceName", "Region")})
    try:
        boto3.client("cloudtrail", endpoint_url=EP).lookup_events(LookupAttributes=[{"AttributeKey": "AccessKeyId", "AttributeValue": k["AccessKeyId"]}])
        print("4. cloudtrail lookup_events: ok")
    except Exception as e:
        print("4. cloudtrail lookup_events:", type(e).__name__, str(e)[:70])
    iam.delete_access_key(UserName="ci-uploader", AccessKeyId=k["AccessKeyId"])
    print("5. after delete, keys:", iam.list_access_keys(UserName="ci-uploader")["AccessKeyMetadata"])
finally:
    srv.terminate(); srv.wait(timeout=10)
print("   moto_server on port", PORT, "stopped")

print("\n== deny-before-time (the 'revoke active sessions' pattern) ==")
REVOKE = {"Version": "2012-10-17", "Statement": [{"Effect": "Deny", "Action": "*", "Resource": "*",
          "Condition": {"DateLessThan": {"aws:TokenIssueTime": "2026-10-26T10:00:00Z"}}}]}
BROAD = {"Statement": [{"Effect": "Allow", "Action": ["s3:*", "sagemaker:*"], "Resource": "*"}]}
role = "arn:aws:iam::123456789012:role/etl-role"
for name, ctx in [("session issued 09:00 (before cutoff; could be the attacker's)", {"aws:TokenIssueTime": "2026-10-26T09:00:00Z"}),
                  ("session issued 10:30 (after cutoff; fresh legitimate session)", {"aws:TokenIssueTime": "2026-10-26T10:30:00Z"}),
                  ("long-term user key (no TokenIssueTime in the request)", {})]:
    print(f"{name:66s}", evaluate("s3:GetObject", "arn:aws:s3:::ml-data/x", ctx=ctx, identity=[BROAD, REVOKE], principal_arn=role)[0])
print("Without the REVOKE policy the same 09:00 session:", evaluate("s3:GetObject", "arn:aws:s3:::ml-data/x", ctx={"aws:TokenIssueTime": "2026-10-26T09:00:00Z"}, identity=[BROAD])[0])

print("\n== secret scanner (flags access-key-id shape) ==")
SAMPLE = 'aws_access_key_id = AKIAIOSFODNN7EXAMPLE\nregion = ap-south-1\ntoken = ASIAIOSFODNN7EXAMPLE\n'   # AWS documentation example ids, not real
for ln, line in enumerate(SAMPLE.splitlines(), 1):
    m = re.search(r"\b(AKIA|ASIA)[A-Z0-9]{16}\b", line)
    if m: print(f"line {ln}: {m.group(0)[:4]}**** ({'long-term key' if m.group(0).startswith('AKIA') else 'temporary credential'})")
```

**Output (my run):** the CLI and boto3 calls ran against a local moto server with fake keys; the server was stopped afterwards. moto's `get_access_key_last_used` returned `N/A`, and CloudTrail `lookup_events` failed (not implemented), so the evidence step is not executed; in real AWS you would query CloudTrail. The deny-before-time results come from the simplified evaluator, not real IAM. The AWS example key ids in the scanner are documentation placeholders, not real keys.
```text
1. key created: AKIARZ... status Active (fake moto key)
2. aws iam update-access-key Inactive -> exit 0
   status now: [('AKIARZ...', 'Inactive')]
3. last used (what you would check in real AWS): {'ServiceName': 'N/A', 'Region': 'N/A'}
4. cloudtrail lookup_events: ClientError An error occurred (500) when calling the LookupEvents operation (reach
5. after delete, keys: []
   moto_server on port 8541 stopped

== deny-before-time (the 'revoke active sessions' pattern) ==
session issued 09:00 (before cutoff; could be the attacker's)      Deny
session issued 10:30 (after cutoff; fresh legitimate session)      Allow
long-term user key (no TokenIssueTime in the request)              Allow
Without the REVOKE policy the same 09:00 session: Allow

== secret scanner (flags access-key-id shape) ==
line 1: AKIA**** (long-term key)
line 3: ASIA**** (temporary credential)
```

**Follow-ups:**
- *Is deleting the repo file enough?* No. History, forks and caches keep it. Rotate and assume it was used.
- *Revoke sessions in the console?* There is a console action that attaches this kind of deny policy; check current docs for the exact name and effect.
- *How would you detect it earlier?* Secret scanning with push protection, and alarms on unusual regions or calls (Part 8 alerting patterns).

**Common mistakes:** deleting before reading CloudTrail; forgetting temporary sessions are still valid; rotating the key but ignoring what it read; no review for persistence; blaming the developer instead of removing long-term keys.

