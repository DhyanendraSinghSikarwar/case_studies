A = {}
A[31] = dict(
 say="Code never hard-codes keys: the SDK walks a fixed chain (env vars, profile, web identity, container endpoint, instance metadata) and the first source that gives keys wins, so on AWS compute you attach a role and the SDK picks up short-lived credentials by itself.",
 explain=[
 "**The chain (botocore, printed from the run):** env, assume-role, assume-role-with-web-identity, sso, shared-credentials-file, login, custom-process, config-file, ec2-credentials-file, boto-config, container-role, iam-role. Order differs by SDK and version, so say 'check current docs' for other languages.",
 "**Env vars beat the shared file.** Case 3 in the run: both set, `env` won. Classic bug: a stale `AWS_ACCESS_KEY_ID` on a CI box silently overrides the role you thought you had.",
 "**Role versus instance profile.** A role is the identity with a trust policy and permissions. An instance profile is the container that lets EC2 attach one role to an instance. The console hides this; the API does not.",
 "**IMDSv2** (instance metadata, concept): the code first does a PUT to get a session token, then GETs credentials with that token header. It blocks simple SSRF tricks that worked on IMDSv1. A hop limit of 1 can stop containers on the host from reaching it (check current docs). Credentials rotate; the SDK refreshes them.",
 "**Containers and pods:** ECS tasks use a container-credentials endpoint (the `container-role` row; I ran it against a local fake). On EKS, IRSA projects an OIDC token file and the SDK calls AssumeRoleWithWebIdentity with it; EKS Pod Identity (newer) uses an agent on the node and the container-credentials route. Both give each pod its own role instead of the node role. Concept only here.",
 "**Failure modes:** no source found gives `NoCredentialsError` (case 5: `None`); a job on EC2 with IMDS blocked falls through and fails after a timeout; the node role leaks to every pod if you skip IRSA/Pod Identity."],
 example="Laptop: you run `aws sso login`, the SDK takes the `sso` source. Training container on SageMaker or ECS: no keys in the image; the container endpoint hands out the task or execution role's keys, which expire. Hand-check from the run: with only the credentials file set, method is `shared-credentials-file` and key `AKIAFAKEFILEKEY0000`; add env vars as well and the key becomes `AKIAFAKEENVKEY00000`.",
 codenote="The script spawns a clean child process per case with a temp HOME, `AWS_EC2_METADATA_DISABLED=true` and a loopback HTTP server pretending to be the container-credentials endpoint.",
 outnote="real run. IMDS (disabled on purpose), web identity, IRSA and Pod Identity were not executed: they need a real STS endpoint, an OIDC issuer or a node agent. The container case ran against my fake local endpoint, so it proves the SDK's lookup, not AWS's endpoint.",
 follow=["Where would you see which role your code actually runs as? `sts get-caller-identity`; here moto would only return its fixed dummy identity, so do it on real AWS.",
         "IRSA versus Pod Identity in one line? IRSA wires an OIDC provider and trust policy per cluster; Pod Identity uses an EKS association and agent, so less trust-policy editing (check current docs).",
         "Why not access keys for a pipeline? Long-lived, easy to leak, no expiry; prefer role plus short-lived credentials (GitHub OIDC is Part 7)."],
 mistakes=["Leaving old `AWS_*` env vars in a shell and wondering why the wrong account answers.","Baking keys into an image or notebook.","Assuming the SDK order is the same in Java, Go and Python.","Forgetting IMDS hop limit and token requirement for containers on EC2."])

A[32] = dict(
 say="Reserved concurrency is both a guarantee and a cap for one function; for a SQS-fed scorer that overloads a database, set reserved concurrency at or below what the database can take and let the backlog wait in the queue.",
 explain=[
 "**Account limit:** a pool shared by all functions in a Region (a default of about a thousand is commonly cited; it can be raised, check current docs). One noisy function can starve the rest.",
 "**Reserved:** carves a slice out of the pool for one function. Guarantee (others cannot take it) and cap (the function cannot exceed it). Setting it to 0 effectively switches the function off. It costs nothing extra by itself.",
 "**Provisioned:** keeps pre-initialised environments warm to dodge cold starts; it is billed while provisioned, applies to a version or alias, and is separate from reserved (check current docs).",
 "**Throttling differs by source:** synchronous caller gets a 429 and must retry; asynchronous events are queued and retried by Lambda for a while, then go to a DLQ or on-failure destination; SQS pollers back off and the messages reappear after the visibility timeout, and can land in the queue's DLQ after the max receive count even though the code never ran. So set visibility timeout above function timeout and a sensible max receive count.",
 "**Scaling speed** is bounded too (burst then steady increase; check current docs), so reserved is not the only brake. For SQS there is also a per-mapping maximum concurrency setting; moto accepted that shape (see run)."],
 example="Hand-check the simulation: 20 messages per second for 20 s is 400 messages; each takes 3 s and holds one database connection. Unlimited-ish (100): peak 60 running (20 x 3), database limit 10 is exceeded. Reserved 10: running never passes 10, 400 messages drain at about 10/3 per second, so about 120 s (run says 121). The cost of protection is a 330-message peak backlog and a longer drain, which is the right place for waiting.",
 codenote="Part 1 sets and reads reserved concurrency plus an SQS mapping shape in moto; part 2 is a tick-by-tick simulation (1 tick = 1 second), not Lambda's real scaler.",
 outnote="real run. Moto stores the setting but never invoked or throttled anything; the table is my simulation with made-up rates (database limit 10, duration 3 s), so it shows the reasoning, not AWS numbers.",
 follow=["Reserved set to 5 on an SQS function with a 10-way database: what breaks? Messages can be throttled repeatedly and move to the DLQ untouched; raise max receive count or reserved.",
         "Better fix than a cap? Pool connections with RDS Proxy or a pooler, plus the cap (check current docs for your engine).",
         "When provisioned instead? When cold-start latency hurts a sync path, not for protecting a database."],
 mistakes=["Thinking reserved concurrency only guarantees capacity and forgetting it also caps.","Setting reserved above the database limit and calling it protected.","Visibility timeout shorter than the function timeout, causing duplicates.","Reserving so much that the rest of the account has too little."])

A[33] = dict(
 say="SageMaker gives you the plumbing (data capture, baseline jobs, schedules, reports, Clarify, Ground Truth) but you still own the thresholds, alert routing and the decision to retrain.",
 explain=[
 "**Data capture:** an endpoint-config setting that writes a sample of requests and responses to S3 (sampling percentage, capture Input and/or Output). It is the raw material for everything else.",
 "**Baseline then monitor:** a baselining job computes statistics and constraints from training or a reference set; a monitoring schedule runs a job on the captured data on a cron and writes a violations report to S3 and metrics to CloudWatch. Drift maths belongs to Part 8.",
 "**Clarify** runs bias and explainability jobs (pre-training, post-training, SHAP-style attributions) as processing jobs. **Ground Truth** manages labelling jobs with a workforce (private, vendor, public) and can bring ground truth back for quality monitoring.",
 "**You still own:** which constraints to trust, alarms on the CloudWatch metrics, who is paged, the join of late-arriving labels to predictions, and the retrain trigger. A report in S3 that nobody reads is not monitoring.",
 "**Failure modes:** capture off or sampling too low, schedule on an empty window (job fails or passes meaninglessly), baseline taken from a different feature pipeline than serving."],
 example="Config check by hand: `InitialSamplingPercentage: 150` is invalid (must be 0 to 100), `DestinationS3Uri` without `s3://` is invalid and capture mode `Both` is not a mode. The validator flags exactly these three; the good config returns an empty error list.",
 codenote="A required-keys validator for the `DataCaptureConfig` dict (key names as in the CreateEndpointConfig API), plus moto calls to see what the mock does and does not do.",
 outnote="real run. Moto accepted and echoed the data-capture config (API shape only) but raised NotImplementedError for `create_monitoring_schedule` and `list_labeling_jobs`; no monitoring or labelling ran. My validator is a simplified check, not the service's own validation.",
 follow=["Which part is the real ML judgement? Choosing constraints and thresholds and deciding when drift justifies retraining.",
         "Why sample instead of capturing everything? Storage and privacy; but low sampling can miss rare drift (rates are your choice, check docs).",
         "Alert path? Schedule metrics to CloudWatch alarms to SNS or EventBridge; design is Part 8."],
 mistakes=["Treating 'Model Monitor enabled' as 'we monitor the model'.","Baseline from clean training data while production features come through a different path.","Forgetting the S3 and KMS permissions for the capture destination.","Expecting Ground Truth to remove the need for label-quality review."])

A[34] = dict(
 say="A SageMaker feature group is a named set of features with a record identifier and an event time, stored in an offline store on S3 (with a Glue table) and optionally an online store; the thing to remember is the online store keeps costing until you turn it off.",
 explain=[
 "**Feature group:** schema (name and type per feature), `RecordIdentifierFeatureName` (the entity key) and `EventTimeFeatureName` (when the value was true). Without event time you cannot do point-in-time correct training sets (Part 9).",
 "**Offline store:** append-only history in S3 (Parquet), with an optional Glue catalog table, so Athena and training jobs can read it. Needs an S3 location and a role. **Online store:** low-latency latest value per key for real-time inference.",
 "**Ingestion:** `PutRecord` writes to the online store (and the offline store gets a copy); batch ingestion can write through Spark or the SDK helper. The runtime API (`sagemaker-featurestore-runtime`) is a separate service from the control-plane API.",
 "**Cost trap:** an online store you forgot keeps its storage and request costs running; add review rules (last-read age) and delete test groups. No prices here; check current docs.",
 "**Failure modes:** missing role or S3 permission (group sits in `CreateFailed`), event time in the wrong type, and duplicates when identifier plus event time repeat."],
 example="Hand-check: a group with features `customer_id`, `event_time`, `txn_count_7d` has the key `customer_id`. The review rule on the sample inventory flags only `customer-risk` (online store on, 45 days since read); `txn-agg` is not online and was read yesterday, so it is not flagged.",
 codenote="Creates a feature group in moto, reads it back, probes the runtime API, then applies a review rule to a small sample inventory.",
 outnote="real run (random numbers in the S3 path are moto's). API shape only: `describe_feature_group` did not echo `OnlineStoreConfig`, `list_feature_groups` raised NotImplementedError and the runtime `put_record` and `get_record` returned 404 'Not yet implemented'. The review rule ran on my sample list, not on mock data.",
 follow=["Offline versus online in one line? Offline is history for training; online is latest value for serving.",
         "Why Glue? So Athena and other engines can query the offline store as a table.",
         "Do you need it? Not if one team and batch scoring only; Part 9 weighs Feast and alternatives."],
 mistakes=["Leaving an online store on after a demo.","No event time or the wrong type for it.","Using the control-plane client to read records.","Assuming offline and online are always consistent in time."])

A[35] = dict(
 say="Athena over partitioned Parquet is enough for ad hoc and training-set pulls, Glue gives the catalog and heavy ETL when one machine is not enough, and Redshift is the answer when the warehouse already holds the truth.",
 explain=[
 "**Athena:** serverless SQL over files in S3; you pay by data scanned (check current docs), so Parquet plus partitions (`dt=...`) cut cost and time. It is not a low-latency serving store.",
 "**Glue Data Catalog and crawlers:** a shared metastore (databases, tables, partitions) used by Athena, Glue jobs, EMR and others. A crawler infers schema; in production many teams prefer explicit DDL so schema does not drift silently.",
 "**Glue ETL (Spark)** beats pandas on one box when data no longer fits memory or you need parallel reads and writes; for a few GB, pandas or DuckDB on one instance is simpler.",
 "**Redshift:** when curated tables already live in the warehouse, read them with UNLOAD to S3 or the data API instead of re-copying pipelines. SageMaker can read from S3 directly, from Athena or Redshift through Data Wrangler or processing jobs, or via the warehouse's connector (check current docs).",
 "**Failure modes:** no partition filter means a full scan; too many tiny files; crawler changes a column type; stale catalog partitions after new data lands."],
 example="Hand-check partition pruning: 30 days x 4 files = 120 objects. A query with `dt = '2026-10-01'` reads 4; without the filter it reads all 120. That is the whole reason to partition.",
 codenote="Creates a Glue database and partitioned table, an Athena query execution and a Redshift cluster record in moto, then counts objects pruned by a partition filter.",
 outnote="real run. Moto only stores the records: the Athena query is marked SUCCEEDED without reading data and the Redshift cluster is a record that never became a warehouse. No real query ran; SQL itself is Book 3.",
 follow=["Crawler or DDL? DDL for stable production tables, crawler for discovery.","When Glue over pandas? When parallel data volume or scheduled managed Spark matters.","Athena for feature serving? No, use an online store or a service database."],
 mistakes=["Querying raw CSV without partitions and calling Athena slow.","Letting the crawler redefine production schemas.","Copying warehouse tables to S3 by hand with no lineage.","Forgetting the S3 and Glue permissions the SageMaker role needs."])

A[36] = dict(
 say="Millions of small objects hurt because every object costs a request and listing pages; the fix is fewer, larger objects (shards), ranged parallel reads and local caching, plus the right SageMaker input mode.",
 explain=[
 "**Why small files hurt:** one GET per object, per-request latency, and ListObjectsV2 returns a limited page of keys (a thousand per call; check current docs), so enumerating a million keys alone is a thousand calls. Requests also have rate and billing dimensions (check current docs).",
 "**Fixes:** pack samples into shards (tar for WebDataset, Parquet row groups); use ranged GETs and parallel reads inside a shard; spread load with sensible prefixes; cache hot shards on local NVMe or EBS; avoid listing at start by shipping a manifest.",
 "**SageMaker input modes:** File copies the data to the instance volume before training; Pipe streams it (older, framework-limited); FastFile exposes S3 objects as files read on demand. Which one wins depends on dataset size and access pattern; check current docs.",
 "**Failure modes:** shards too large for random access, shuffling across shards done wrong (poor mixing), training stalling on cold reads, request throttling when thousands of workers start together."],
 example="Hand-check from the run: 1,000,000 files of 100 KB is about 97,656 MB. One GET each gives 1,000,000 GETs plus 1,000 LIST pages. As 256 MB shards it is 382 objects; 64 MB ranges give 4 GETs each, 1,528 total, or 382 with whole-shard GETs. Moto confirms the pattern on a tiny scale: 200 small objects need 200 GetObject calls, one shard needs 2 ranged calls for the same 20,000 bytes.",
 codenote="Request-count arithmetic plus real boto3 calls into moto with a before-call event hook counting operations. No timings are printed on purpose.",
 outnote="real run, counts only. A localhost mock proves nothing about S3 latency or throughput, and the 1M-file line is arithmetic, not a measurement.",
 follow=["Pick a shard size? Big enough to amortise requests, small enough to shuffle and resume; tune and measure on the real service.","File versus FastFile versus Pipe? File when the data fits and you want simple reads; FastFile to start sooner on big data (check current docs).","Does a prefix fix throttling? Spreading across prefixes helped historically; check current docs for the current scaling behaviour."],
 mistakes=["Benchmarking against a mock or laptop and quoting it.","Listing the whole bucket at every epoch.","Tiny shards that recreate the small-file problem.","Reading with one thread."])

A[37] = dict(
 say="For a SageMaker endpoint I watch invocations, 4XX and 5XX errors, model latency versus overhead latency, and CPU, memory and GPU use, and I alarm on 'M of N datapoints breaching' so one spike does not page anyone.",
 explain=[
 "**Endpoint metrics (namespace AWS/SageMaker, dimensions EndpointName and VariantName):** `Invocations`, `Invocation4XXErrors`, `Invocation5XXErrors`, `ModelLatency` (time inside your container), `OverheadLatency` (service overhead). Latency units are microseconds per current docs; verify.",
 "**Instance metrics (namespace /aws/sagemaker/Endpoints):** CPU, memory, disk and GPU utilisation, and GPU memory. A 5XX with high CPU suggests saturation; high ModelLatency with low CPU suggests a slow dependency or model load.",
 "**Alarms and autoscaling:** alarms evaluate a statistic over a period for N periods, firing when M datapoints breach; target-tracking autoscaling uses a metric such as invocations per instance. Treat-missing-data setting matters: no traffic is not the same as healthy.",
 "**Logs:** emit one structured line per request (request id, model version, latency, input size, outcome), never raw sensitive input. Alerting design is Part 8."],
 example="Hand-check M of N: window [10,120,130,20,140] with threshold 100 has three breaches, so '3 of 5' is ALARM; [10,120,130,20,30] has two, so OK. With missing points set to breaching, five of five flags are true and it alarms; with notBreaching, two data points breach and it stays OK.",
 codenote="Creates the alarm in moto and reads back comparison, period, evaluation periods and datapoints-to-alarm; then a small pure-Python M-of-N evaluator with missing-data modes (simplified: it ignores the alarm's exact period alignment).",
 outnote="real run. Moto stored the alarm in `OK` and never evaluated a real metric; the evaluator is my simplified reimplementation, and the threshold is a placeholder.",
 follow=["Why M of N? It filters one-off spikes yet reacts to sustained breaches.","Which latency tells you your code is slow? ModelLatency; OverheadLatency points at the platform.","Which metric for autoscaling? Per-instance invocations is the common choice; check current docs for the predefined metric."],
 mistakes=["Alarming on the average and missing p99.","Default missing-data handling hiding an endpoint that receives no traffic.","Alarming without an action or owner.","Ignoring GPU memory until an out-of-memory 5XX."])

A[38] = dict(
 say="A KMS key never leaves KMS: you ask it for a data key, encrypt locally with the plaintext copy, store only the wrapped copy, and later ask KMS to unwrap it; access is the key policy plus IAM plus optional grants.",
 explain=[
 "**Key types:** customer managed (you control policy, rotation, deletion, can be shared across accounts) versus AWS managed (created by the service, you cannot edit the policy, and cannot share it cross-account; check current docs).",
 "**Who may use a key:** the key policy is the root of trust; IAM policies only work if the key policy delegates to IAM. Grants are temporary, narrow delegations (used by services like EBS). Cross-account use needs both the key policy and the caller's IAM policy.",
 "**Envelope encryption:** `GenerateDataKey` returns a plaintext key plus a wrapped one; encrypt data locally (AES-GCM), discard the plaintext, store the wrapped key next to the ciphertext. KMS is called only to wrap and unwrap, which is why it scales to big files.",
 "**Encryption context:** extra key-value pairs bound to the ciphertext as authenticated data; a mismatch fails decrypt, and it shows in CloudTrail for audit. **Rotation:** automatic rotation changes backing material while old ciphertext stays decryptable. Keys are Region-scoped.",
 "**Disable or delete:** a disabled key cannot decrypt, so data becomes unreadable; deletion has a waiting period and is irreversible afterwards (check current docs). Always confirm nothing live depends on the key."],
 example="Hand-check the run: the data key is 32 bytes (AES-256); decrypt with the original context returns the fake text. With a different context moto raised InvalidCiphertextException, matching the idea that context must match. After `disable_key` moto still decrypted, which real KMS is documented not to allow, and `schedule_key_deletion` left the key in `PendingDeletion`.",
 codenote="Moto for create_key, generate_data_key, decrypt, create_grant, rotation, disable and scheduled deletion; `cryptography` AES-GCM does the local encrypt and decrypt.",
 outnote="real run (random ids and dates masked). Moto does not enforce key policies or IAM, so who can call kms:Decrypt was not tested, and moto ignores the disabled state on decrypt, so do not use it to prove that behaviour.",
 follow=["Why not encrypt the file directly with KMS? Direct Encrypt has a small size limit (check docs) and sends data to KMS; envelope is cheaper in calls and scales.","What does S3 SSE-KMS do for you? S3 does the envelope work per object; you control access via key policy.","Delete versus disable? Disable first, wait, then schedule deletion."],
 mistakes=["Storing the plaintext data key.","Deleting a key that still protects old datasets.","Forgetting KMS permission for the job role (S3 allowed, KMS denied).","Using an AWS managed key when another account needs access."])

A[39] = dict(
 say="In a locked-down VPC the job has no internet, so it needs an S3 gateway endpoint and interface endpoints for ECR (api and dkr), CloudWatch Logs and STS, and a missing one shows up as a hang or timeout, not a clear error.",
 explain=[
 "**Setup:** network isolation turns off outbound network access from the container; the VPC config puts the job's ENIs in private subnets with security groups. Check which options need which (check current docs).",
 "**Needed paths:** S3 (data, artifacts and image layers) via a Gateway endpoint that must be attached to the subnet's route table; ECR via two interface endpoints, `ecr.api` and `ecr.dkr`; CloudWatch Logs; STS for role credentials; plus SageMaker API endpoints if code in the job calls them.",
 "**Why a hang:** with no route, packets are dropped silently; clients retry until they time out, so you see a slow generic failure. DNS for interface endpoints also needs private DNS enabled and a security group allowing 443 from the job.",
 "**Debug order:** read the failure reason, then check each endpoint and the route table association, endpoint SG, endpoint policy, and finally NACLs. A NAT gateway is the alternative to endpoints, with different security and cost trade-offs (Part 12)."],
 example="Hand-check the audit: an empty VPC misses all six. Then I created s3 without a route table plus the two ECR endpoints, and the audit flagged s3 (not attached) and logs, sts, sagemaker.api; after attaching the route table and adding the rest, nothing is missing.",
 codenote="The checklist is data (`CHECKLIST`); `audit()` compares it with `describe_vpc_endpoints` and the subnet's route table. The service list is an example; verify against current docs for your job features.",
 outnote="real run in moto. Moto stores VPC objects only: routing, private DNS, ENIs and the real timeout were not executed.",
 follow=["Gateway versus interface endpoint? Gateway: route-table entry, S3 and DynamoDB only; interface: ENI with private IP in your subnet.","Why ecr.dkr and ecr.api both? One for registry protocol pulls, the other for API calls.","Alternative? A NAT gateway, but traffic leaves the private design; endpoints keep it on the AWS network."],
 mistakes=["Only creating the S3 endpoint.","Gateway endpoint not associated with the subnet's route table.","Endpoint security group blocking 443 from the job.","Forgetting the logs endpoint and blaming the image."])

A[40] = dict(
 say="Cross-account access needs both sides every time: the prod role must be allowed in prod IAM, and the dev resource (bucket, repository, key, role trust) must name that prod role.",
 explain=[
 "**Grants, dev to prod:** (1) S3: dev bucket policy allowing the prod role, and prod role policy allowing the S3 actions; (2) ECR: dev repository policy allowing prod pull actions, and prod role with `ecr:GetAuthorizationToken` and pull actions (or ECR replication into prod); (3) KMS: dev key policy allowing the prod role, plus prod IAM permission; (4) if prod assumes a role in dev, dev trust policy plus `sts:AssumeRole` in prod; (5) model registry sharing via a model package group resource policy or RAM (check current docs).",
 "**Why both sides:** across accounts neither account alone can decide. The owner of the resource must trust the other principal, and the caller's own account must allow its principal to make the call. One missing side gives implicit deny.",
 "**Three common failures:** (a) only one side written, so AccessDenied; (b) the artifact is encrypted with a key policy that does not include the prod role (S3 fine, KMS denied); a default AWS managed key cannot be shared; (c) ECR pull fails because the repository policy or `GetAuthorizationToken` is missing, or the image reference points at the wrong account or Region.",
 "**Prefer** digests and a promotion step that copies or replicates artifacts into prod over granting prod broad read on dev."],
 example="Hand-check from the output: S3 with identity and bucket policy allows; remove either and it denies. Same shape for ECR, KMS and AssumeRole. The last case shows an explicit Deny in the bucket policy beating both allows.",
 codenote="Uses the simplified evaluator copied from `scratch/B4P10_wavea/iam_eval_sketch.py` (copy kept beside the script). Dev account 111111111111 and prod 222222222222 are fake.",
 outnote="real run of the sketch. It is simplified: no KMS rule that the key policy must enable IAM, no account-root principals, no grants, no VPC endpoint or boundary layers here. It shows the 'both sides' logic, not AWS's full engine, and no real AWS call was made.",
 follow=["Could a resource policy alone be enough? Within one account sometimes; across accounts, no (check the policy-evaluation docs).","Copy artifacts instead? Often cleaner: a pipeline copies the model and image into prod so prod never reads dev.","How do you debug? CloudTrail errorMessage and the policy simulator in real AWS (not run here)."],
 mistakes=["Fixing only the bucket policy.","Encrypting with a key prod cannot use.","Using `Principal: *` to make it work.","Granting prod read on the whole dev account."])
