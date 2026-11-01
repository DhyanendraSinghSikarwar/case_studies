@@HEAD 1@@
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
@@CODE q01.py python@@
@@CODE q01_cli.sh sh@@

**Output (my run):** moto 5.2.4, boto3 1.43.118, fake keys, decorator mode (moto's in-process mock).
@@OUT q01.py@@
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

@@HEAD 2@@
**Say this first (1 line):** S3 is a flat key-value object store with strong read-after-write consistency per object, but no rename, no locks and no multi-object transactions, so a reader of a dataset must not trust "it exists, so it is complete".

**Then explain:**
- Flat key space: `data/part-0.csv` is one key string. "Folders" are a convention: listing with a prefix and a delimiter gives you the folder view. Empty-folder markers are just zero-byte keys.
- Strong consistency (since December 2020): after a successful PUT or DELETE, any later GET or LIST sees it. Before that, list-after-put and overwrite reads could be stale.
- What it does not give: atomic commit of many objects, rename (it is copy plus delete, two calls), locking, or protection from lost updates. Two writers to one key: last writer wins.
- Training job reading while another writes: the job can list a half-written dataset and train on partial data. Fix with a commit marker: write all parts, then write a manifest or `_SUCCESS` last, and readers only trust prefixes that have it. Or write to a new versioned prefix and never overwrite.
- Conditional writes: `If-None-Match: *` on PUT gives "create only if absent", enough for a simple lock or leader claim. Real S3 support and its edge cases: check current docs.

**Example:** writer makes 4 parts, crashes after 2, never writes the manifest. The reader sees 2 parts in a listing but no manifest, so it skips the run. Without the manifest rule it would train on half the data and nobody would notice.

**Code:**
@@CODE q02.py python@@

**Output (my run):** moto 5.2.4, API shape and logic only.
@@OUT q02.py@@
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

@@HEAD 3@@
**Say this first (1 line):** A role has two documents: the trust policy says who may assume it, the permissions policy says what it can do once assumed, and ML systems use roles because credentials are short-lived and nothing long-lived can leak.

**Then explain:**
- User: a long-term identity with a password or access keys. Group: a bag of users for attaching policies; a group is not a principal. Role: an identity with no password or keys of its own; you assume it and get temporary credentials.
- Policies: managed (standalone, reusable, attach by ARN; AWS-managed or customer-managed) or inline (embedded in one identity, deleted with it). Identity-based policies attach to users, groups, roles. Resource-based policies attach to the resource (bucket policy, KMS key policy, role trust policy) and name a Principal.
- Trust policy is a resource-based policy on the role. Permissions policies are identity-based. A call needs both: caller allowed to assume, then the assumed role allowed to do the action.
- Why roles for ML: training jobs, Lambdas and EC2 get credentials automatically, they expire (hours), rotate by themselves, and leave no key in code, a notebook or a repo. Long-lived keys leak into Git (Q50).
- Failure modes: a wildcard Principal in a trust policy, a role that is assumable by any user in the account, inline policies nobody can find, and a long-lived key kept "just for CI".

**Example:** `train-role` trusts `sagemaker.amazonaws.com` (trust) and may read `s3://ml-data/train/*` (permissions). A teammate cannot assume it, because the trust names only the service. SageMaker can, but cannot write anywhere because the permissions say read-only.

**Code:**
@@CODE q03.py python@@

**Output (my run):** moto 5.2.4.
@@OUT q03.py@@
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

@@HEAD 4@@
**Say this first (1 line):** The execution role is the IAM role SageMaker assumes to act for your job: trusted by `sagemaker.amazonaws.com`, with just enough permission to read inputs, write outputs, pull the image and write logs, and the launcher needs `iam:PassRole` to hand it over.

**Then explain:**
- Trust policy: Principal `{"Service": "sagemaker.amazonaws.com"}`, action `sts:AssumeRole`. Without it SageMaker cannot use the role and job creation fails.
- Minimum permissions: S3 read on the input prefix (plus ListBucket with a prefix condition), S3 write on the output prefix, ECR pull actions for the image (and `ecr:GetAuthorizationToken` on `*`), CloudWatch Logs create stream and put events. Add KMS if encrypted (Q8).
- `iam:PassRole`: when you call CreateTrainingJob with a RoleArn, IAM checks that *you* may pass that role. Without that check anyone who can create jobs could pass an admin role and escalate. Scope it to the one role ARN and add `iam:PassedToService`.
- Human vs role: the human launches the job with their own permissions; the code in the container uses the role's. They are different identities. The role does not need `PassRole` or `CreateTrainingJob`; the human does.
- Failure modes: AccessDenied at job start (PassRole or trust), job starts but cannot read data (role policy), ECR pull failure, and an over-broad role such as AmazonSageMakerFullAccess plus S3 full access.

**Example:** Training role can GetObject on `ml-data/train/a.csv` (allow) but not PutObject there (deny). The launcher can pass `sm-exec` to SageMaker but not to EC2 and not an `admin` role.

**Code:** (the evaluator is a copy of `scratch/B4P10_wavea/iam_eval_sketch.py`, saved here as `code/iam_eval.py`, simplified)
@@CODE q04.py python@@

**Output (my run):** pure Python, no AWS.
@@OUT q04.py@@
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

@@HEAD 5@@
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
@@CODE q05.py python@@

**Output (my run):** moto 5.2.4. API shape only.
@@OUT q05.py@@
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

@@HEAD 6@@
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
@@CODE q06.py python@@

**Output (my run):** moto 5.2.4. API shape only.
@@OUT q06.py@@
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

@@HEAD 7@@
**Say this first (1 line):** IAM decides in this order in spirit: any explicit Deny wins, then every ceiling (SCP, boundary, session) must allow, and then something must actually grant, otherwise it is an implicit deny.

**Then explain:**
- Default is deny. An allow must exist. An explicit Deny anywhere (identity, resource, SCP, boundary, session) beats every Allow.
- Ceilings, not grants: SCPs (organisation), permissions boundaries (on a user or role) and session policies (on an assumed session) only limit. The effective permission is the intersection. They never grant anything.
- Same account: an identity policy allow or a resource policy allow is enough (with the boundary and session caveats). Cross-account: both the caller's identity policy and the resource policy must allow.
- Exceptions to "one allow is enough": role trust policies (the trust policy must name the caller), and KMS key policies (the key policy must allow, directly or by enabling IAM). SCPs do not apply to the management account. Check current docs for the full flowchart.
- Failure modes: forgetting the SCP ceiling, expecting a boundary to grant, and debugging only the identity policy when a bucket policy denies.

**Example:** boundary allows only `ec2:*`, identity policy allows `s3:*`, so `s3:GetObject` is denied. Add `s3:*` to the boundary and it is allowed.

**Code:** (evaluator in `code/iam_eval.py` is a copy of the Wave A sketch)
@@CODE q07.py python@@

**Output (my run):** pure Python, thirteen cases (I ran more than ten).
@@OUT q07.py@@
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

@@HEAD 8@@
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
@@CODE q08.py python@@

**Output (my run):** pure-Python evaluator, then moto 5.2.4 with and without auth enforcement.
@@OUT q08.py@@
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

@@HEAD 9@@
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
@@CODE q09.py python@@

**Output (my run):** moto 5.2.4 (caller is the fixed moto user in account 123456789012).
@@OUT q09.py@@
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

@@HEAD 10@@
**Say this first (1 line):** A presigned URL is a normal S3 request signed in advance with the signer's credentials, carrying the signature and expiry in the query string, so a client with no AWS credentials can do exactly that one request until it expires.

**Then explain:**
- GET or PUT presign: the URL pins method, bucket, key, expiry. Whoever holds it can do it. The permission used is the signer's at request time.
- Lifetime with an assumed role: the URL stops working when the signing credentials expire, even if you asked for a longer expiry. Long-lived presigns need an IAM user key (not recommended) or regenerate on demand.
- Restricting uploads: presigned POST with a signed policy: `content-length-range`, key prefix, content type. Presigned PUT cannot do a size range.
- Pitfalls: URLs end up in logs, referrers and chat; long expiry; signer loses the permission or is deleted, so the URL fails; no per-user identity in the access log.
- Failure mode: assuming "expired" is enforced by the mock. It was not.

**Example:** a web app hands a data scientist a 5-minute presigned POST limited to `uploads/` and 1 MiB. The browser uploads straight to S3; the server never touches the bytes.

**Code:**
@@CODE q10.py python@@

**Output (my run):** moto 5.2.4, requests against the mock.
@@OUT q10.py@@
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
