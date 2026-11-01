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
