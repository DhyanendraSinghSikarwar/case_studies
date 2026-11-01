import re, pathlib, sys
ROOT = pathlib.Path("/home/user/case_studies/interviews")
part = (ROOT / "Book4_MLOps/Book4_MLOps_Part10.md").read_text().splitlines()
CODE = ROOT / "scratch/B4P10_Q11-20/code"
OUT = pathlib.Path("/tmp/claude-0/b10_q11_20/out")

def head(n):
    for i, l in enumerate(part):
        if l.startswith(f"### Q{n} "):
            ask = next(x for x in part[i:i + 4] if x.startswith("**Asked at:**"))
            return l, ask
    raise SystemExit(f"Q{n} missing")

def code(*names):
    return "\n\n".join(f"# --- file: code/{n} ---\n" + (CODE / n).read_text().rstrip() for n in names)

def out(*names):
    return "\n".join((OUT / n).read_text().rstrip() for n in names)

ENV = "Sandbox: Python 3.13.17, boto3 1.43.118, moto 5.2.4 (decorator mode `mock_aws`, fake keys, no real AWS contact, no moto server needed for these), run with `python3 -I`. "
A = {}

A[11] = dict(
say="With versioning on, an overwrite adds a new version and a delete adds a delete marker; nothing is lost until someone deletes a specific version id. For training, I pin the dataset to a version id so the run is reproducible.",
explain="""- **Versioning enabled:** every PUT to a key makes a new version with its own VersionId. A plain DELETE does not remove data; it adds a delete marker as the newest version, so a plain GET says NoSuchKey.
- **Restore:** delete the delete marker (by its VersionId). The previous version becomes current again. Or copy an old version over the key. Both are cheap and need no backup system.
- **Suspended:** new writes get the version id `null` and overwrite the previous null version. Old versions made earlier stay. Suspending does not turn the clock back.
- **Lifecycle:** keeps the current version and the old (noncurrent) ones are handled by their own rules: `NoncurrentVersionExpiration`, transitions of noncurrent versions, and cleanup of expired delete markers. Without it, versions pile up quietly. Check current docs for exact rule fields.
- **MFA delete and Object Lock:** MFA delete asks for an MFA code to permanently delete a version or change versioning state. Object Lock (needs versioning, set up at bucket creation as the docs describe) gives WORM retention: governance mode can be bypassed by users with special permission, compliance mode cannot be shortened by anyone. Both protect against mistakes and bad actors, not against a wrong dataset.
- **Reproducibility:** a key name is not a dataset. Record `bucket + key + VersionId` (or a manifest listing them) in the run metadata, and read with `VersionId=`. Failure mode: deleting that old version by id, or a lifecycle rule expiring it, breaks reproduction. Pair with Object Lock or a retention rule when you must keep it.""",
example="Key `train.csv` gets v1, then v2. Delete it: 2 versions plus 1 delete marker, plain GET fails, v2 still readable by id. Remove the marker and the GET returns v2 again. Permanently delete v2 by id and v1 becomes current. (Numbers are in the output below.)",
lang="python", code=code("q11_versioning.py"),
output=ENV + "Real output (S3 behaviour is moto's emulation):\n```\n" + out("q11_versioning.out") + "\n```\nWhat moto differs on or does not show: an unversioned object has no VersionId here (real S3 reports `null` in some APIs; check current docs); the lifecycle read-back kept `NoncurrentDays` but dropped `NewerNoncurrentVersions` in this version; Object Lock denied the permanent delete in moto, but real retention modes, bypass permissions, MFA delete and lifecycle timing were **not executed**. Real S3 durability and consistency are not proven by a mock.",
fu="""- *Can I roll back a whole prefix?* No single call. You list versions and copy or delete markers per key, usually with a script or S3 Batch Operations (check current docs). Or use dataset snapshot prefixes.
- *Is versioning a backup?* Partly. It protects against overwrite and delete in the same bucket and Region. It does not protect against the whole account being compromised or a Region loss. Add replication or a separate backup account if that matters.
- *Why not just copy the data per run?* It works but costs storage and hides lineage. A version id or manifest is a light pointer. Part 4 (DVC, MLflow) covers dataset versioning tools.""",
mist="""- Logging only the S3 key in the experiment tracker and calling the run reproducible.
- Thinking a DELETE frees space on a versioned bucket. It adds a marker; storage stays until versions are deleted.
- Forgetting a noncurrent-version lifecycle rule and being surprised by growth.
- Believing suspended versioning removes old versions.
- Treating a moto result as proof of how real S3 lifecycle, MFA delete or Object Lock behave.""")

A[12] = dict(
say="Lambda is great for small glue around ML: triggers, light pre or post processing, calling an endpoint. It is usually the wrong place to host a heavy model because of cold starts, memory and package limits, and no GPU. I would check the current limits page before quoting any number.",
explain="""- **Limits to know (all: check current docs):** memory range, timeout cap, deployment size for zip versus container image, `/tmp` size, request and response payload size, and account concurrency. They have changed over the years and sources I looked at disagree on wording, so I do not quote them from memory.
- **Cold start:** a new execution environment must start, load the runtime and your code, then run init code. Later calls on a warm environment skip that. For ML it gets worse with big dependencies and loading a model file in init.
- **Levers:** load the model once outside the handler (warm calls reuse it), keep dependencies small, use a container image when libraries are large, put shared libraries in layers, and use provisioned concurrency to keep environments initialised (you pay for readiness; check the docs on the cost model).
- **Wrong tool when:** the model needs a GPU, is large, needs sustained throughput with tight p99, or needs long runs beyond the timeout cap. Then use SageMaker endpoints or containers on ECS/EKS. Lambda is fine for a tiny model with spiky traffic.
- **Failure modes:** throttling when concurrency is exhausted, timeouts on first request after a deploy, memory too low so CPU is also low (CPU scales with memory; check docs).""",
example="A Lambda reads an S3 event and calls a SageMaker endpoint: good glue. A Lambda that loads a large model file in init: the first request after idle pays that load time, so it is a poor fit for a strict latency target.",
lang="python", code=code("q12_lambda.py"),
output=ENV + "Real output:\n```\n" + out("q12_lambda.out") + "\n```\nmoto stores the function configuration (memory, timeout, env, reserved concurrency, layer) and returns it. **Invoke needs Docker to run the code; no Docker daemon here, so nothing executed.** The invoke response still shows StatusCode 200 with the Docker error text as the payload: a 200 from the mock is not proof the code ran. Provisioned concurrency was not implemented in this moto version (404). Cold starts, real limits and throttling are **not executed**.",
fu="""- *Zip or container image?* Zip is simple and quick for small code. Container image when dependencies are big or you already build images; it lands in ECR. Check current docs for size caps.
- *Reserved versus provisioned concurrency?* Reserved guarantees a slice and also caps the function (Q32 goes deeper). Provisioned pre-warms environments.
- *How do I test the handler?* Keep it a plain function and call it with a fake event locally (Part 10 Q41).""",
mist="""- Loading the model inside the handler on every call.
- Quoting limits from memory in an interview. Say "check the current limits page".
- Reading a 200 from an invoke as proof it ran.
- Putting a GPU or large-model workload in Lambda.""")

A[13] = dict(
say="I match the instance family to the workload: GPU memory and bandwidth for deep learning, plain CPU instances for a gradient-boosted model. For a 7B fine-tune the first question is GPU memory, then multi-GPU or multi-node, then quota and capacity.",
explain="""- **Families (concept level, check current docs for current generations):** general purpose (M), compute optimised (C), memory optimised (R), GPU training (P series), GPU inference and graphics (G series), AWS Trainium (training) and Inferentia (inference) accelerators which need the Neuron SDK and model compilation.
- **7B fine-tune versus boosted trees:** a full fine-tune of a 7B model needs weights, gradients and optimizer state in GPU memory, so it usually means large-memory GPUs or multiple GPUs, or parameter-efficient methods to shrink the footprint. A gradient-boosted model on tabular data usually runs fine on CPU, so a memory-optimised or compute instance is enough. Training maths is Books 1 and 2.
- **Storage:** EBS is network-attached and persists (can be snapshotted); instance store is local, fast, and lost when the instance stops or terminates. Use instance store or local NVMe for scratch and cache, EBS or S3 for anything you must keep.
- **Deep Learning AMIs:** images with GPU drivers, CUDA and common frameworks preinstalled, so you do not hand-build driver stacks. Check current docs for the available versions.
- **Surprises:** GPU instance vCPU quotas default low or at zero in a new account and need a quota request; capacity can be short in a Region or AZ even with quota; spot GPU capacity is volatile. Plan lead time. None of this is visible in a mock.""",
example="Fraud model on tabular features: boosted trees, a CPU instance, data from S3 to local disk. 7B fine-tune: a GPU-family instance sized by GPU memory; if one GPU cannot hold it, multi-GPU or sharded training (Q43). First action: check the GPU quota in the Region.",
lang="python", code=code("q13_ec2.py"),
output=ENV + "Real output (instance-type metadata is moto's bundled data):\n```\n" + out("q13_ec2.out") + "\n```\nAPI shape only: `run_instances` returns `pending` and the 200 GiB gp3 root volume is recorded. **Not shown by a mock:** a real GPU, drivers, a real AMI boot, vCPU or GPU quotas, capacity errors, EFA, instance store behaviour. The bundled type data may lag real AWS: check current docs.",
fu="""- *Why not always the biggest GPU?* Cost and utilisation. Small jobs waste it. Start from memory needs and data loading speed.
- *Trainium or Inferentia?* Possible cost or availability wins, but you take on compile and framework-compatibility work. Check current docs and test your model first.
- *EBS or instance store for checkpoints?* Write checkpoints to S3 (or EBS you keep); instance store disappears with the instance.""",
mist="""- Picking a GPU by name instead of by memory need.
- Learning about GPU quota on launch day.
- Keeping the only copy of a model on instance store.
- Using moto's instance-type list as a current catalogue.""")

A[14] = dict(
say="Spot is cheap capacity that can be reclaimed with a short warning, so the job must be able to die at any step and resume to the same result. That means checkpoints with model, optimizer, scheduler, RNG and data position, written to S3 atomically, and a resume path that is tested.",
explain="""- **How interruption works:** AWS can reclaim spot capacity and gives a short warning (about two minutes in the sources I saw; check current docs). You cannot rely on that warning to save a big checkpoint, so checkpoint on a schedule.
- **Spot-safe means:** save model weights, optimizer state (momentum), LR scheduler state, RNG states and the data position (epoch and batch, or the sampler state), plus the step counter. Write to a temp name and rename, so a half-written file is never read. Resume must be idempotent.
- **SageMaker managed spot training:** set `EnableManagedSpotTraining`, give a `CheckpointConfig` with an S3 URI (SDK `checkpoint_s3_uri`, local path `/opt/ml/checkpoints` by default) and `MaxWaitTimeInSeconds` at least the run time limit. SageMaker syncs that folder to S3 and restores it on restart. Your code must still load the checkpoint. Check current docs for options.
- **Diversify:** allow several instance types and AZs where the service allows, to lower the chance of losing everything at once.
- **Failure modes:** checkpoint too rare (lost work), checkpoint only weights (results drift, see below), non-atomic writes, a deterministic-looking run that is not reproducible because the sampler restarts from the beginning.""",
example="Train for 200 steps with a checkpoint every 25. Kill at step 130. Resume from step 125 and finish. The final weights equal the uninterrupted run exactly. A sloppy resume (weights only) ends with different weights.",
lang="python", code=code("q14_spot.py", "q14b_sm_spot_shape.py"),
output="Pure-Python loop (no AWS), Python 3.13.17, seeded, run with `python3 -I`:\n```\n" + out("q14_spot.out") + "\n```\nSageMaker request shape in moto 5.2.4 (fake keys):\n```\n" + out("q14b_sm_spot_shape.out") + "\n```\nThe loop is a simulation of the resume logic. **Real spot interruption, the warning notice, SageMaker syncing checkpoints and real GPU training are not executed.** moto marked the training job Completed instantly.",
fu="""- *How often to checkpoint?* A trade-off between lost work and checkpoint cost. Sources I saw disagreed on a fixed number, so measure your checkpoint time and pick an interval you can afford to lose.
- *Is the resumed result always identical?* Here yes, on one CPU with seeded Python. On GPUs with nondeterministic kernels or changed world size it may not be bit-identical; aim for statistically equivalent and test it.
- *When not to use spot?* Tight deadlines, jobs that cannot checkpoint, or the last run before a release.""",
mist="""- Saving weights but not optimizer state or RNG.
- Writing the checkpoint in place so a kill leaves a corrupt file.
- Never testing resume until the first real interruption.
- Setting MaxWaitTime below the run time.""")

A[15] = dict(
say="Fargate is a way to run containers without managing servers, under ECS or EKS. It is not a rival to them. For one model and a small team I would pick SageMaker endpoints or ECS on Fargate; for 40 models with GPUs a platform team might choose EKS or SageMaker with a managed fleet. ECR just holds the images.",
explain="""- **Where each fits:** SageMaker endpoint gives managed hosting, autoscaling hooks, model monitoring and the registry link. ECS is simpler AWS-native container orchestration. EKS is Kubernetes: more power, portability and GPU scheduling, more to operate. Lambda is for small models and spiky traffic. (Opinion pieces I read agree on this shape; check current docs for GPU support per mode.)
- **Small team, one model:** least ops wins. SageMaker real-time endpoint or ECS Fargate with an autoscaling service if the model is CPU-sized.
- **Platform team, 40 models, GPUs:** Kubernetes tooling and bin-packing GPUs, or SageMaker features such as multi-model or inference components (Q25). It depends on how much platform work the team wants to own.
- **Spiky traffic:** serverless options (Lambda, SageMaker serverless or async) or autoscaling with a minimum of one; watch cold starts.
- **ECR:** private image registry. Task definitions and endpoint models reference an image URI, ideally by digest. Kubernetes internals are Part 3 and serving mechanics Part 6.""",
example="Task definition `fraud-scorer` (Fargate, 1 vCPU, 2 GB in moto's units of cpu and memory) points at `<account>.dkr.ecr.us-east-1.amazonaws.com/fraud-scorer:1.4.0`. The task role is what the container's code uses; the execution role is what ECS uses to pull the image and write logs.",
lang="python", code=code("q15_ecs_ecr.py"),
output=ENV + "Real output (API shape only):\n```\n" + out("q15_ecs_ecr.out") + "\n```\nNothing ran: no image was pushed, no service or task started, no networking. Cost, GPU support on Fargate and per-service limits are **not executed**; check current docs.",
fu="""- *Is Fargate cheaper than EC2?* Depends on utilisation and workload; I do not quote prices. Measure with your own traffic.
- *Why SageMaker over ECS?* Built-in endpoint autoscaling, data capture, Model Monitor and registry integration, at the cost of its own conventions.
- *Task role versus execution role?* Task role is the app's permissions; execution role pulls images and ships logs.""",
mist="""- Calling Fargate an alternative to ECS or EKS.
- Choosing EKS for one model with no Kubernetes skills on the team.
- Deploying by mutable tag instead of digest.
- Mixing up task role and execution role.""")

A[16] = dict(
say="A VPC is my private network with a CIDR block. Subnets are public if their route table sends 0.0.0.0/0 to an internet gateway, private if not. A private SageMaker job reaches S3 and ECR through VPC endpoints, not the internet. Security groups are stateful and allow-only; NACLs are stateless, ordered, and can deny.",
explain="""- **Basics:** CIDR (for example /16 for the VPC, /24 per subnet), route tables per subnet, internet gateway for public routes, NAT gateway so private subnets can start outbound connections.
- **Endpoints:** a gateway endpoint (S3, and DynamoDB) adds a route in your route table. An interface endpoint puts an ENI with a private IP in your subnet for services such as ECR (`ecr.api`, `ecr.dkr`), CloudWatch Logs and STS. Compared with NAT, endpoints avoid internet egress and often cut NAT traffic cost; check current docs for pricing.
- **Security group:** attached to ENIs, allow-only, stateful: if a request was allowed in, the reply is allowed out without an egress rule.
- **NACL:** per subnet, numbered rules evaluated in order, first match wins, allow and deny, stateless: you must allow return traffic on ephemeral ports yourself.
- **Failure modes:** missing endpoint means a hang or timeout (no route), NACL forgetting ephemeral ports, SG on the endpoint ENI not allowing 443 from the job.""",
example="Job in a private subnet pulls its image from ECR and reads S3: it needs `ecr.api` and `ecr.dkr` interface endpoints, an S3 gateway endpoint (ECR layers are stored in S3), and CloudWatch Logs access. No NAT needed.",
lang="python", code=code("q16_vpc.py"),
output=ENV + "Real output:\n```\n" + out("q16_vpc.out") + "\n```\nPart 1 is moto API shape only. Part 2 is my own small model of filtering, not AWS's implementation. **Real routing, DNS, ENIs, endpoint policies and connection tracking limits are not executed.**",
fu="""- *Gateway or interface endpoint for S3?* A gateway endpoint is the common default (route-based); interface endpoints for S3 exist for other cases such as on-premises access. Check current docs.
- *Why no clear error when an endpoint is missing?* Packets have no route, so they time out instead of being refused.
- *Where do SGs attach?* To ENIs (instances, endpoints, tasks), not to subnets.""",
mist="""- Saying security groups can deny.
- Forgetting ephemeral ports in a NACL.
- Putting a training job in a private subnet with no S3 or ECR path.
- Assuming a NAT gateway is free of cost; check current docs.""")

A[17] = dict(
say="At rest means encrypted on disk, in transit means encrypted on the wire with TLS. On S3 I would set default SSE-KMS so I control the key and get an audit trail. A job needs both S3 permission and KMS permission, which is why it can fail on KMS even when S3 looks fine.",
explain="""- **S3 options:** SSE-S3 (S3-managed keys), SSE-KMS (key in KMS, policy and audit control), SSE-C (you supply the key on each request), client-side (you encrypt before upload). Default bucket encryption applies when a request does not specify one. Check current docs for what is applied by default today.
- **EBS and SageMaker:** volumes and outputs can use a KMS key you name (volume KMS key, output KMS key on the job). The role needs to use that key.
- **Envelope encryption:** KMS gives you a data key; you encrypt the big file locally with it and store the wrapped (encrypted) key next to the data. KMS only handles the small key, never the bulk data.
- **KMS access has three doors:** key policy (the main one, must allow or delegate to IAM), IAM policy, and grants (temporary, scoped). Unlike most AWS resources, IAM alone is not enough unless the key policy delegates to IAM.
- **Why S3 allowed but KMS denied:** SSE-KMS reads call `kms:Decrypt`; the role lacks it or the key policy does not name the role (or account) so the read fails with AccessDenied that mentions KMS. Also a key in another account or Region.""",
example="Bucket default is SSE-KMS. A PUT with no encryption arguments gets `ServerSideEncryption: aws:kms` and the key id on `head_object`. For envelope encryption: ask KMS for a 256-bit data key, encrypt locally with AES-GCM, store ciphertext plus wrapped key, decrypt by asking KMS to unwrap.",
lang="python", code=code("q17_encryption.py"),
output=ENV + "`cryptography` 50.0.2 for AES-GCM. Real output:\n```\n" + out("q17_encryption.out") + "\n```\nmoto applies the default encryption and does the data-key and grant API calls. **Real KMS key-policy, IAM and grant enforcement, bucket keys' request savings, Region scoping and rotation are not executed.**",
fu="""- *SSE-KMS or SSE-S3?* SSE-KMS when you need key-level access control, audit and revocation; it adds KMS calls and quotas to think about (check current docs). SSE-S3 is simpler.
- *What is encryption context for?* Extra authenticated data: binding a key use to a context (for example dataset name), visible in logs. Decrypt must supply the same context.
- *Does encryption stop an over-permissioned role?* No. It adds a second gate only if the key policy is tight.""",
mist="""- Giving the role s3:GetObject but no kms:Decrypt.
- Believing KMS encrypts the bulk data directly.
- Logging or persisting the plaintext data key.
- Assuming moto proves the key policy would allow the call.""")

A[18] = dict(
say="For a database password I use Secrets Manager because it has rotation, versions and audit. For plain config and a simple API key Parameter Store SecureString is fine. Environment variables are only a delivery method, and secrets must never be baked into an image or printed in logs.",
explain="""- **Secrets Manager:** purpose-built for secrets; versions with staging labels (AWSCURRENT, AWSPREVIOUS), built-in rotation support (usually through a Lambda), IAM and optional resource policies, CloudTrail audit. Priced per secret and per call (check current docs).
- **SSM Parameter Store:** hierarchical config; SecureString uses KMS; versions; no built-in rotation; standard tier is generally cheaper (check current docs). Good for non-rotating values.
- **Env vars:** how the process gets the value at runtime. Fine if injected at start by the platform (ECS secrets, SageMaker job environment from a fetched secret). Not fine when they are hard-coded in a Dockerfile `ENV`: layers keep them forever and `docker history` shows them.
- **KMS-encrypted files in S3:** workable but you build rotation and access control yourself.
- **Rules:** fetch at start with least-privilege role, never in image or git, never log values, rotate and have a revocation plan. CI secrets are Part 7.""",
example="Dockerfile line `ENV DB_PASSWORD=...` is a leak: anyone with the image has it. Correct: `ENV DB_PASSWORD_FILE=/run/secrets/db_password` or fetch from Secrets Manager at start using the task role.",
lang="python", code=code("q18_secrets.py", "secret_scan.py"),
output=ENV + "Secrets and SSM calls, then the scanner on two demo files in `code/demo_inputs/` (all values are fake; the scanner is a heuristic and misses obfuscated or high-entropy secrets):\n```\n" + out("q18_secrets.out", "scan.out") + "\n```\nCommands run: `python3 -I q18_secrets.py` style (venv python) and `python3 -I secret_scan.py <Dockerfile> <train.env>` (exit code 1 when findings). Note the scanner ignored `DB_PASSWORD_FILE` (a path pointer) and the `${DB_PASSWORD}` reference. moto does not enforce IAM or KMS on these reads; the `kms:alias/...` value for the undecrypted parameter is moto's representation. **Real rotation, KMS enforcement and audit are not executed.**",
fu="""- *How do I rotate without downtime?* Staging labels: new version is AWSPENDING, tested, then promoted; clients read AWSCURRENT. Both old and new credentials need to work during the switch.
- *Parameter Store or Secrets Manager?* Rotation and cross-account sharing need push you to Secrets Manager. Otherwise cost and simplicity decide; check current docs.
- *Already leaked?* Rotate first, then clean the history. Q50 covers the response order.""",
mist="""- `ENV` or `ARG` secrets in Dockerfiles (ARG values also show in history).
- Committing `.env` files.
- Logging the full config dict at startup.
- Trusting a regex scanner as the only control; use real secret scanning too.""")

A[19] = dict(
say="CloudWatch is for metrics, logs and alarms: how the system is behaving now. CloudTrail is the audit log of API calls: who did what. AWS Config records resource configuration over time: what it looked like and when it changed.",
explain="""- **CloudWatch:** metrics (service and custom), Logs with filters, alarms with period, evaluation periods and datapoints to alarm. First stop for 'why is the endpoint slow': latency, invocation and error metrics, CPU, GPU, memory, plus container logs.
- **CloudTrail:** records management API events (and optionally data events) with caller identity, time, source IP and error message. 'Who deleted the model bucket' is a CloudTrail question: look up `DeleteBucket`. Retention and lookup window: check current docs; for long retention, deliver a trail to S3.
- **AWS Config:** tracks configuration items and compliance rules. 'Was this bucket public last week' is a Config history question.
- **Failure modes:** no trail set up before the incident, no Config recorder enabled, logs not retained, alarms with missing-data treatment hiding outages.
- Drift monitoring is Part 8; endpoint metrics in depth is Q37.""",
example="Custom metric `FraudScoreLatencyMs`; alarm: Average over 60 s period, 3 evaluation periods, 2 datapoints needed, threshold 100, GreaterThanThreshold. A log line `ERROR AccessDenied ...` found with filter `ERROR`.",
lang="python", code=code("q19_cloudwatch.py"),
output=ENV + "Real output:\n```\n" + out("q19_cloudwatch.out") + "\n```\nmoto implements metrics, alarms and log filtering. **CloudTrail `lookup_events` raised NotImplementedError in this moto version**, so no audit lookup was shown. The Config recorder call was accepted but I did not test further. The alarm reads `OK` in moto right after creation; real CloudWatch typically starts at `INSUFFICIENT_DATA` until data arrives (check current docs). Real alarm evaluation, log delivery delays and CloudTrail contents are **not executed**.",
fu="""- *Which for 'AccessDenied on S3'?* CloudTrail event with errorMessage, then the policy layers (Q20).
- *Does CloudTrail show everything?* Management events by default; object-level S3 and some data events need to be enabled (check current docs).
- *Alarm on what?* Alert design is Part 8; here pick symptoms (5XX, latency) not just CPU.""",
mist="""- Opening CloudWatch for a 'who did it' question.
- Enabling CloudTrail after the incident.
- Treating alarm state OK as 'healthy' when data is missing.
- Assuming moto's CloudTrail or Config behaviour matches AWS.""")

A[20] = dict(
say="First confirm who the real caller is, because most AccessDenied is the wrong principal. Then walk the layers in order: role policy, bucket policy, KMS key policy, boundary, SCP, VPC endpoint policy, Block Public Access and Ownership, cross-account or Region. Evidence: CloudTrail's errorMessage, then the policy simulator or Access Analyzer.",
explain="""- **1. Real caller:** CloudTrail (or the error text) shows the assumed-role ARN. Is it the job's execution role or a notebook user? Is the bucket in another account or Region?
- **2. Role policy:** does it allow `s3:GetObject` on `arn:aws:s3:::ml-data/train/*` and `s3:ListBucket` on the bucket with a prefix condition? Common typo: object ARN versus bucket ARN.
- **3. Bucket policy:** an explicit Deny (for example a missing VPC endpoint condition or a TLS-only rule), or in cross-account use, no Allow for your role.
- **4. KMS:** SSE-KMS needs `kms:Decrypt` in the role policy and a key policy that allows the role (or delegates to IAM). The error often names KMS.
- **5. Guardrails:** permissions boundary, SCP (also session policy if assumed with one). They only limit; an explicit deny wins everywhere.
- **6. Network and bucket settings:** VPC endpoint policy, Block Public Access (affects public policies, not a plain named-principal grant), Object Ownership (objects owned by another account), wrong Region (redirect or 301 style errors).
- **Evidence:** CloudTrail `errorCode` and `errorMessage` (newer messages may name the denying policy type; check current docs), the IAM policy simulator, Access Analyzer policy validation and findings. Fix one layer at a time and re-test.""",
example="Role policy is perfect, bucket has default SSE-KMS, key policy names a different role: S3 checks pass, the first denying layer is the KMS key policy. Fix: add the role to the key policy (or key policy delegating to IAM) and `kms:Decrypt` on the role.",
lang="python", code=code("q20_accessdenied_checklist.py"),
output="Pure-Python only (no AWS, no moto), Python 3.13.17. It copies `code/iam_eval_sketch.py` unmodified from the Wave A sketch. Real output:\n```\n" + out("q20_accessdenied_checklist.out") + "\n```\nSimplified: the evaluator is the Wave A sketch (no NotAction, policy variables or most operators); KMS, VPC endpoint policy, Block Public Access, Region and Ownership are small rules or flags I wrote, not real AWS evaluation. The order shown is a debugging order, not AWS's internal order. **Real CloudTrail, the policy simulator and Access Analyzer are not executed.** For reference, moto only enforces IAM when auth enforcement is switched on, so it cannot reproduce this failure by default.",
fu="""- *The role policy looks right, still denied?* Look for an explicit deny in SCP, boundary or bucket policy, then KMS.
- *Is the denying layer always in the error?* Not always. Newer error messages can say which policy type denied (check current docs); older ones are generic.
- *How to prevent a repeat?* A test job in CI that reads the prefix, Access Analyzer checks, and least-privilege policy templates (Q8).""",
mist="""- Editing the role policy again and again without checking who the caller is.
- Forgetting KMS because the bucket looks 'just S3'.
- Missing that a cross-account read needs both sides.
- Testing the fix with your own admin credentials instead of the job role.""")

lines = ["# Book 4 Part 10: answers Q11-Q20 (Wave B agent, scratch)", ""]
for n in range(11, 21):
    h, ask = head(n)
    d = A[n]
    lines += [h, ask, "",
              "**Say this first (1 line):** " + d["say"], "",
              "**Then explain:**", d["explain"], "",
              "**Example:** " + d["example"], "",
              "**Code:**", f"```{d['lang']}", d["code"], "```", "",
              "**Output (my run):** " + d["output"], "",
              "**Follow-ups:**", d["fu"], "",
              "**Common mistakes:**", d["mist"], "", "---", ""]
(ROOT / "scratch/B4P10_Q11-20/answers.md").write_text("\n".join(lines))
print("ok")
