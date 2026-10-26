import re, pathlib
ROOT = pathlib.Path("/home/user/case_studies/interviews")
part = (ROOT/"Book4_MLOps/Book4_MLOps_Part10.md").read_text().split("\n")
OUT = pathlib.Path("/tmp/claude-0/b10_q21_30/out")
CODE = ROOT/"scratch/B4P10_Q21-30/code"
def head(n):
    for i, l in enumerate(part):
        if l.startswith(f"### Q{n} "):
            assert part[i+1].startswith("**Asked at:**"), n
            return l, part[i+1]
    raise KeyError(n)
def code(f): return (CODE/f).read_text().rstrip()
def out(f): return (OUT/f).read_text().rstrip()
HDR = 'import os\nos.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")\nimport boto3\nfrom moto import mock_aws\n'
def tidy(f):
    c = code(f)
    return c.replace(HDR.strip()+"\n", HDR.strip()+"\n")
RUN = "Ran with `python3 -I` from an empty temp dir, Python 3.13.17, boto3 1.43.118, moto 5.2.4, fake keys, in-process `mock_aws()` (no moto server needed, no network to AWS). "
A = {}

A[21] = dict(
say="Multipart upload splits one big object into parts that upload in parallel and retry on their own, then Complete stitches them together. Use it for big files, and add a lifecycle rule so abandoned uploads do not sit there costing storage.",
bul=[
"**Why:** a 20 GB model archive as one PUT means one failure restarts everything. With parts you upload in parallel, retry only the failed part, and can resume later.",
"**When:** AWS docs recommend multipart for large objects (a size threshold is suggested, and a single PUT has an upper limit). The exact thresholds, part-size minimum and maximum, and max part count: check current docs. boto3's `upload_file` switches to multipart for you above a configurable threshold.",
"**Complete and Abort:** Complete takes the list of (PartNumber, ETag) and makes the object appear. Abort throws away the uploaded parts. Until one of them happens, the parts exist but there is no object.",
"**Hidden cost:** unfinished uploads are not visible in a normal `ls` but, per AWS docs, their stored parts are billed storage. Fix: a lifecycle rule `AbortIncompleteMultipartUpload` with `DaysAfterInitiation`.",
"**ETag trap:** the multipart ETag is not the MD5 of the file. It is a hash built from the part hashes plus `-<number of parts>`. So you cannot compare it with `md5sum`. Use a checksum feature or your own stored hash for integrity.",
"**Failure modes:** non-final part under the minimum size gives `EntityTooSmall` at Complete time; wrong ETag or missing part gives `InvalidPart`; same part number uploaded twice, last one wins.",
],
ex="Two 5 MiB parts. Complete returns an ETag ending in `-2`. A whole-file MD5 of the same 10 MiB looks completely different. Two 4-byte parts: Complete fails with EntityTooSmall because part 1 is not the last part and is below the minimum.",
codef="q21_multipart.py", outf="q21_multipart.txt",
notes="Moto note: moto enforces the small-part rule (the real limit value is AWS's; check current docs). Moto does not model real parallel throughput, storage billing, or lifecycle execution (the rule is stored and read back, nothing is ever aborted by it). Real S3 timing and limits: not executed.",
fu=[("How do you make a failed upload resumable?","Persist the UploadId and the list of finished part numbers; on restart call ListParts and upload only the missing ones."),("Why not just use bigger single PUTs?","There is a single-PUT size cap (check current docs) and one failure restarts everything."),],
mm="Calling Complete with the ETags in the wrong order; assuming the ETag equals MD5; forgetting the lifecycle abort rule so failed uploads pile up; claiming a threshold number as fixed without checking current docs.")

A[22] = dict(
say="An Auto Scaling group keeps a fleet of EC2 instances between a min and a max, built from a launch template, and a scaling policy moves desired capacity. It is for self-managed workers; SageMaker endpoints have their own autoscaling.",
bul=[
"**Launch template vs launch configuration:** the template is versioned and the current choice; launch configurations are legacy (check current docs for current status). Pin a version or use `$Latest` knowingly.",
"**Capacity:** min is the floor, max is the ceiling, desired is what the group tries to run now. Scaling policies only change desired inside min and max.",
"**Health checks:** EC2 status checks by default; ELB checks if behind a load balancer. The grace period stops the group killing a GPU node that is still loading a model. Too short a grace period gives a replace-loop.",
"**Policies:** target tracking (hold a metric near a value, simplest), step (different actions per alarm size), scheduled (known peaks, like a nightly batch). Queue depth per worker is often a better metric for batch workers than CPU.",
"**Extras:** scale-in protection stops chosen instances being terminated (for example one mid-job). Warm pools keep pre-initialised instances so slow GPU boots do not hurt scale-out. Mixed instances policy blends spot and on-demand, with several instance types to reduce spot capacity risk.",
"**One-line contrast:** SageMaker endpoint autoscaling is Application Auto Scaling on a variant's instance count (and scaling metrics like invocations per instance); here you manage the AMI, patching, and load balancer yourself.",
],
ex="min 1, max 6, desired 2, target-tracking at 50 percent average CPU. If CPU is high, desired rises toward 6; when quiet, back toward 1. A scheduled action raises capacity to 4 at 20:00 for a nightly job.",
codef="q22_asg.py", outf="q22_asg.txt",
notes="Moto stores the group, template, policy and scheduled action and returns them; it does not boot instances for real, run health checks, evaluate CloudWatch metrics, or ever scale. Warm pools, mixed-instances policy and spot behaviour: not executed. Real scaling: not executed.",
fu=[("Why a warm pool for GPUs?","Boot plus driver plus model load is slow; pre-initialised stopped or running instances cut scale-out latency. Check current docs for pool states and their costs."),("CPU target for a GPU inference fleet?","Often a bad signal; use requests per instance, queue depth or GPU utilisation as a custom metric.")],
mm="Using CPU for GPU or queue-bound workers; no health-check grace period; setting min=0 for a latency-sensitive service; forgetting scale-in protection for long batch jobs.")

A[23] = dict(
say="Lambda has three invocation styles: synchronous, where the caller gets the error; asynchronous, where Lambda retries and then uses a DLQ or destination; and poll-based, where Lambda polls the source. In all three delivery can repeat, so handlers must be idempotent.",
bul=[
"**Synchronous** (API Gateway, direct invoke): the caller waits and sees the error. Retries are the caller's job. Throttling shows up as a 429 to the caller.",
"**Asynchronous** (S3, EventBridge, SNS): Lambda queues the event and retries on failure (default retry count and event age are configurable; check current docs). After that, send it to a DLQ or an on-failure destination so it is not lost.",
"**Poll-based** (SQS, Kinesis, DynamoDB streams): the Lambda service polls. For SQS, a failed batch returns to the queue after the visibility timeout; after `maxReceiveCount` receives it moves to the queue's DLQ. For streams, a bad record can block a shard unless you configure bisect, retry limits and an on-failure destination.",
"**Idempotency:** SQS standard is at-least-once and retries re-run your code. Use an idempotency key (job id) and a conditional write or a dedupe table.",
"**Visibility timeout rule of thumb:** set it longer than the function timeout (AWS docs suggest a multiple; check current docs), or a slow run gets its message delivered again while still running.",
"**ML use:** S3 upload triggers feature extraction (async); a queue feeds embedding jobs (poll). A DLQ with an alarm on depth is the safety net.",
],
ex="Receive a message: it is invisible. Receive again straight away: nothing. If the worker dies and the visibility timeout ends, the same message comes back with ReceiveCount 2. That is a duplicate. With maxReceiveCount 2, a third failure would send it to the DLQ.",
codef="q23_sqs.py", outf="q23_sqs.txt",
notes="Moto's SQS visibility works, and I shortened visibility to 0 to simulate expiry instead of waiting 30 s. Lambda event source mappings, retries, destinations and DLQ delivery on failure are not executed (Lambda invoke needs Docker, which is unavailable). The moto redrive config is stored and read back; I did not show a message actually moving to the DLQ.",
fu=[("FIFO or standard?","FIFO gives ordering and dedup within limits (check current docs) but lower throughput; the handler should still be idempotent."),("Partial batch failure?","Report only failed message ids (batch item failures) so successes are not retried; check current docs for the response shape.")],
mm="Visibility timeout shorter than the function runtime; no DLQ; assuming exactly-once; DLQ with no alarm so failures sit silent.")

A[24] = dict(
say="The SageMaker Model Registry is a group of versioned model packages. Each package carries the inference container and model data location, metadata and an approval status, and a status change emits an event that can start deployment.",
bul=[
"**Model package group:** a named collection (one per model line, for example churn-model). Each registered version is a model package with an auto-incremented version number.",
"**Package contents:** `InferenceSpecification` (container image, model data S3 URL, supported content types), optional model metrics, customer metadata, and the approval status.",
"**Approval status:** `PendingManualApproval`, `Approved`, `Rejected`. Status alone does not deploy anything; it is a gate that a pipeline or event rule reads.",
"**Trigger:** SageMaker emits an EventBridge event on model package state change. A rule filtered on `Approved` can start CodePipeline or Step Functions. Event details: check current docs.",
"**Scope:** promotion policy and gates live in Parts 4 and 7; here it is just the service objects.",
"**Failure modes:** deploying a package whose S3 artifact was deleted; approving without recording the metrics that justified it; two groups for the same model.",
],
ex="Create group churn-model, create package version 1 as PendingManualApproval, update it to Approved. Listing Approved packages in the group returns 1.",
codef="q24_registry.py", outf="q24_registry.txt",
notes="Moto stores and returns group, package and status changes (API shape only). It did not echo my CustomerMetadataProperties back (printed None) so do not rely on that here. No EventBridge event is delivered on approval; the rule I created is only stored. Real events and downstream deployments: not executed.",
fu=[("Who should approve?","A human or an automated check, recorded with an approval description; keep a separate role for approval than for registering."),("Registry vs MLflow registry?","Different service; both hold versions and stages. Choose by where the rest of your stack lives.")],
mm="Treating approval as deployment; no metadata on the package (git SHA, data version); letting the training role also approve.")

A[25] = dict(
say="A multi-model endpoint hosts many models behind one endpoint and loads each from S3 on first request, evicting cold ones. It suits thousands of small per-tenant models, not big GPU models with strict p99.",
bul=[
"**Multi-model endpoint (MME):** one container image serves many artifacts from an S3 prefix; the caller passes `TargetModel`. The container lazy-loads a model into memory/disk and evicts when memory is short.",
"**Cold-load penalty:** the first call for a model pays the S3 download and load. Later calls are warm until eviction. Latency is therefore uneven; check current docs for hosting details and instance support (GPU support rules differ).",
"**Multi-container endpoint:** different containers on one endpoint, either invoked directly or chained as a serial inference pipeline (for example preprocess then model).",
"**Inference components:** a newer way to place several models on one endpoint with per-model compute settings and scaling; check current docs for the current feature set.",
"**Good fit:** many small, similar, rarely-hit models (per-customer forecasters). **Bad fit:** large GPU models, strict latency SLO, models that all stay hot (eviction thrash).",
"**Versus many small endpoints:** simpler isolation and per-model scaling, but each endpoint has a minimum instance cost and management overhead. MME shares one fleet and cuts idle cost, at the price of cold loads and noisy neighbours.",
],
ex="10,000 tenant models, each hit a few times a day. One MME with 2 instances beats 10,000 endpoints. A fraud model needing p99 under 50 ms should have its own endpoint.",
codef="q25_mme.py", outf="q25_mme.txt",
notes="NOT emulated: no S3 load, no eviction, no cold-load latency, no model memory limits. Moto accepted `Mode: MultiModel`, and invoke returned a canned body regardless of TargetModel. It also did not echo InferenceExecutionConfig for the multi-container model (printed None). Everything about real hosting behaviour: not executed.",
fu=[("How do you handle a noisy neighbour?","Split into several MMEs by tier, or give heavy tenants their own endpoint."),("What do you monitor?","Per-model load time and invocation count, memory and disk use, eviction rate; metric names: check current docs.")],
mm="Putting large GPU models in an MME; ignoring cold-load latency; no per-tenant isolation plan; assuming TargetModel needs no S3 permissions on the execution role.")

A[26] = dict(
say="SageMaker Pipelines is SageMaker's own DAG service: typed steps, parameters and a JSON definition, with step caching. Pick it when the work is mostly SageMaker jobs; pick Step Functions or Airflow for broader, cross-service orchestration.",
bul=[
"**Steps:** Processing, Training, Tuning, Condition (branch), RegisterModel, Lambda, Callback and others (check current docs for the list). Dependencies come from data references or explicit `DependsOn`.",
"**Parameters:** typed pipeline inputs (for example the input S3 path), referenced as `{\"Get\": \"Parameters.Name\"}`. Change them per execution without editing the definition.",
"**Caching:** a step with `CacheConfig` and an `ExpireAfter` can reuse an earlier result if its arguments match. Good for expensive preprocessing; the cache key rules and what counts as a match: check current docs.",
"**Definition is JSON:** the SDK builds it, and `create_pipeline` accepts the JSON string. Validating structure early (names unique, parameters declared, DependsOn resolved) catches typos before a long run.",
"**When to prefer:** native ML lineage, Studio UI and registry integration favour Pipelines. Prefer Step Functions for non-SageMaker work, or Airflow when the platform already runs it (design is Part 5).",
"**Failure modes:** a Condition referencing a property that does not exist; cache hiding a changed upstream data file because the path stayed the same.",
],
ex="Prep (processing) -> Train (training, cached) -> AucCheck (condition) -> Register. A checker flags a step that depends on a name that does not exist and a parameter that was never declared.",
codef="q26_pipeline.py", outf="q26_pipeline.txt",
notes="No step ran. Moto stores the definition and `start_pipeline_execution` returns an execution that moto itself reports as Succeeded with nothing executed; `list_pipeline_execution_steps` is NotImplementedError in moto. My checker is a small structural check, not the SageMaker validator; real validation rules: check current docs. Pipeline execution on AWS: not executed.",
fu=[("Pipelines or Step Functions for a train-evaluate-deploy flow?","If everything is SageMaker jobs and you want registry lineage, Pipelines; if it also calls many other services with retries, Step Functions."),("How do you trigger it?","EventBridge schedule or event, or an API call from CI.")],
mm="Trusting the caching on changed data at the same S3 path; hard-coding paths instead of parameters; believing a moto 'Succeeded' means anything ran.")

A[27] = dict(
say="Step Functions is a state-machine service defined in Amazon States Language. Standard is for long, auditable workflows; Express is for high-volume short ones. For ML you chain Task states with Retry, Catch and a Choice gate.",
bul=[
"**Standard vs Express:** Standard runs for a long time, with durable execution history you can inspect. Express is for short, high-rate runs, with history through logging rather than the execution-history API. Duration limits and delivery semantics: check current docs.",
"**State types:** Task (do work), Choice (branch), Map (loop over items), Parallel (fixed branches), Wait, Pass, Succeed, Fail.",
"**Retry and Catch:** Retry on named errors with interval, backoff rate and max attempts (use it for throttling). Catch routes to a fallback state after retries run out.",
"**Integrations:** request-response (start and move on), run-a-job `.sync` (wait until the job finishes), and wait-for-callback with a task token for human or external steps. Exact ARNs and supported services: check current docs.",
"**History model:** each execution is an event history of state entries and exits; that is what you debug from.",
"**Design:** Train (retry on throttling) -> Evaluate -> Gate on metric -> Deploy, else Fail. Common failure modes: a Next that points nowhere, a state with no Next or End, retrying non-idempotent steps.",
],
ex="Train retries ThrottlingException up to 4 times with doubling intervals starting at 10 s. If AUC from Evaluate is at least 0.9, Deploy; else Fail. The checker catches a Choice default pointing to a missing state.",
codef="q27_sfn.py", outf="q27_sfn.txt",
notes="The checker is mine and simplified (Next/Default/Catch targets, StartAt, terminal states; not Map/Parallel inner graphs, not JSONPath validity). Moto stores the definition and starts an execution, but it does not run SageMaker or Lambda integrations; the RUNNING status shown is moto's, not a real run. Real state engine, retries and `.sync` waits: not executed.",
fu=[("Express or Standard for an inference pre-processing fan-out?","Express if short and high-rate; Standard if you need durable history or human callback."),("Where does a timeout belong?","On the Task (`TimeoutSeconds`), plus HeartbeatSeconds for long jobs.")],
mm="No Catch so a failure leaves a vague error; retrying a non-idempotent deploy; polling loops instead of `.sync`; hard-coding ARNs.")

A[28] = dict(
say="Batch queues containerised jobs on compute it manages (EC2, spot or Fargate), which is good for many CPU jobs and array sweeps; SageMaker Training or Processing is better for ML-aware jobs; plain ECS tasks are for simple one-offs.",
bul=[
"**Batch objects:** compute environment (what machines, min/max vCPUs, spot or on-demand), job queue (priority, ordered environments), job definition (image, resources, command). Array jobs run N copies with an index. Fair priority comes from queue priority; check current docs for scheduling policies.",
"**Spot:** cheaper but interruptible; use retry strategy so interrupted jobs rerun. Jobs must be restartable.",
"**Decision:** many independent jobs, queueing, priorities and arrays: Batch. GPU training with metrics, experiments, managed spot checkpoints, tuning: SageMaker. A single scheduled container, or already on ECS: ECS task (maybe via EventBridge).",
"**Not Batch when:** you need ML job lineage and tuning built in, tiny infrequent jobs (a simple ECS task or Lambda is easier), or hard real-time.",
"**Failure modes:** min vCPU above zero leaves idle machines; job stuck RUNNABLE because the compute environment cannot satisfy the resource ask; non-idempotent jobs retried on spot interruption.",
],
ex="Nightly embedding generation over 1,000 shards: an array job of size 1,000 on a spot compute environment with retry 2. A one-off GPU fine-tune with checkpointing: SageMaker Training.",
codef="q28_batch.py", outf="q28_batch.txt",
notes="Moto accepted the compute environments, queue and job definition in this run (it needed a service role, instance profile, subnet and security group). I did not submit a job; nothing would run. Moto does not provision instances, schedule, or model spot. Real Batch behaviour: not executed.",
decision=True,
fu=[("How do you size an array job?","One child per shard, each idempotent; cap concurrency via the environment's max vCPUs."),("Fargate or EC2 for Batch?","Fargate for no node management and small jobs; EC2 when you need GPUs or specific instance types (check current docs).")],
mm="Using Batch for one tiny job; min vCPUs above zero; no retry strategy on spot; forgetting job idempotency.")

A[29] = dict(
say="S3 access is the union of identity policy, bucket policy and other layers, with one rule on top: any explicit Deny wins. In the same account either side can allow; across accounts both sides must allow.",
bul=[
"**Layers:** IAM identity policy (what the caller may do), bucket policy (resource policy, can name other accounts), access points (per-use-case names with their own policy), VPC endpoint policy (limits what goes through the endpoint), Block Public Access (a guard against public grants).",
"**ACLs:** legacy. New buckets default to ACLs disabled via Object Ownership 'bucket owner enforced' (check current docs). Use policies, not ACLs.",
"**Non-TLS deny:** a Deny with `Bool aws:SecureTransport = false` forces HTTPS.",
"**Cross-account read on one prefix:** the bucket policy names the other account's role and a prefix in `Resource`; the other account's role must also have an identity allow. Both are needed.",
"**Failure modes:** a wildcard Principal with an Allow (public); forgetting the identity side in the partner account; a deny without scoping that breaks your own pipelines; KMS-encrypted objects also need key permissions.",
"**What real AWS adds:** full IAM evaluation for every caller (moto enforces little by default), SCPs and boundaries, KMS key policy checks, VPC endpoint routing, Access Analyzer, CloudTrail and Block Public Access enforcement. Moto's S3 did enforce this bucket-policy Deny in this run; the rest I did not test.",
],
ex="Bucket ml-secure-data: partner account 222222222222 may read `train/*` only. With a Deny on `train/*` the GET returns 403 but `other/` still returns 200.",
codef="q29_s3_access.py", outf="q29_s3_access.txt",
json_block='''{
  "Version": "2012-10-17",
  "Statement": [
    {"Sid": "DenyNonTLS", "Effect": "Deny", "Principal": "*", "Action": "s3:*",
     "Resource": ["arn:aws:s3:::ml-secure-data", "arn:aws:s3:::ml-secure-data/*"],
     "Condition": {"Bool": {"aws:SecureTransport": "false"}}},
    {"Sid": "PartnerReadTrain", "Effect": "Allow",
     "Principal": {"AWS": "arn:aws:iam::222222222222:role/partner-reader"},
     "Action": "s3:GetObject", "Resource": "arn:aws:s3:::ml-secure-data/train/*"}
  ]
}''',
notes="Moto enforced the explicit-Deny bucket policy on GET (403) in this run. The evaluator (copied from the Wave A sketch, simplified: no NotAction, policy variables, KMS, access points, endpoint policies, Block Public Access) gave the cross-account decisions. The Deny and Allow statements above are shown in one JSON document for reading; in the Python run they are separate objects (the evaluator in the last two lines took the TLS deny as a policy and a context of http vs https). Real AWS enforcement: not executed.",
fu=[("Where does the partner's side go?","An identity policy on partner-reader allowing s3:GetObject on that prefix (in their account)."),("Access points?","Give each team its own name and policy; delegate details to the access point policy; check current docs for how they combine with the bucket policy.")],
mm="Only editing the bucket policy for cross-account; Principal `*` with Allow; mixing ACLs and policies; forgetting `s3:ListBucket` on the bucket ARN (not the object ARN) for listing.")

A[30] = dict(
say="None of the three grants anything. A permissions boundary and a session policy cap one identity; an SCP caps a whole account or OU. Effective access is what the identity policy allows and every cap also allows, and any explicit deny wins.",
bul=[
"**Permissions boundary:** set by an IAM admin on a user or role; maximum permissions that role can ever have. Does not grant. Does not limit resource policies naming the exact principal ARN (check current docs).",
"**SCP:** set in AWS Organizations on accounts or OUs; a ceiling over all principals there. It does not apply to the management account, and does not grant. Service-linked roles are exempt (check current docs).",
"**Session policy:** passed when assuming a role or federating; narrows that session only, as an intersection with the role's permissions.",
"**Delegation:** let ML engineers create roles `ml-*`, but only with the boundary attached, and deny changing or removing the boundary. Then a role they create with AdministratorAccess is still capped to S3, SageMaker, logs and ECR reads.",
"**Guardrail:** a Deny on `iam:CreateRole` when `iam:PermissionsBoundary` is not the approved ARN (as an SCP or identity-policy deny). Also protect the boundary policy itself from edits, which this sketch does not show.",
"**Failure modes:** boundary missing `iam:PassRole` where the job needs it; forgetting that SCP and boundary only cut, so a role with an empty identity policy still has nothing.",
],
ex="Engineer creates `ml-trainer` with the boundary: allowed. Without it: denied. Attaching AdministratorAccess to ml-trainer is allowed as an action, but its iam:CreateUser and ec2:RunInstances are outside the boundary, so denied.",
codef="q30_boundary.py", outf="q30_boundary.txt",
notes="Simplified evaluator (copied from the Wave A sketch; I added only `StringNotEquals` in my copy). Not handled: NotAction/NotResource, policy variables, most condition operators and set operators, the boundary-vs-resource-policy rules beyond the principal-ARN case, session-policy details for role chaining, service-linked roles, SCPs at several OU levels beyond a simple list, implicit-deny nuances for iam:PassRole. Real IAM: not executed.",
fu=[("Boundary vs SCP, who uses which?","SCP for org-wide guardrails by a platform team; boundary for delegating role creation inside an account."),("Can a boundary alone give access?","No. Identity policy must also allow, except for the resource-policy exception noted in docs.")],
mm="Thinking a boundary grants access; leaving boundary removal permitted; applying an SCP expecting it to affect the management account; forgetting the identity side.")

def build():
    lines = []
    for n in range(21, 31):
        h, asked = head(n); a = A[n]
        lines += [h, asked, "", "**Say this first (1 line):** " + a["say"], "", "**Then explain:**"]
        lines += ["- " + b for b in a["bul"]]
        lines += ["", "**Example:** " + a["ex"], ""]
        if a.get("decision"):
            lines += ["Decision table:", "", "| Need | Batch | SageMaker Training/Processing | ECS task |", "|---|---|---|---|",
                      "| Many independent CPU jobs, arrays, queue priorities | good fit | possible, more per-job overhead | manual scheduling |",
                      "| GPU training with checkpoints, tuning, lineage | possible | good fit | manual |",
                      "| One scheduled container | overkill | possible | good fit |",
                      "| Spot with retries | supported (check current docs) | managed spot (check current docs) | self-managed |", ""]
        lines += ["**Code:**", ""]
        if a.get("json_block"):
            lines += ["```json", a["json_block"], "```", ""]
        lines += ["```python", code(a["codef"]), "```", ""]
        lines += ["**Output (my run):** " + RUN + "Moto is API shape only: " + a["notes"], "", "```text", out(a["outf"]), "```", ""]
        lines += ["**Follow-ups:**"] + [f"- {q} {r}" for q, r in a["fu"]]
        lines += ["", "**Common mistakes:** " + a["mm"], "", "---", ""]
    pathlib.Path(ROOT/"scratch/B4P10_Q21-30/answers.md").write_text("\n".join(lines))
build()
