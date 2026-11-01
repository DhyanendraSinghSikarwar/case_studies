from build_head import *
A = {}

A[41] = (r"""
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
@@CODE@@

**Output (my run):** the handler test and the Dockerfile text check ran for real with Python 3.13. No Lambda runtime, no image build (no Docker daemon), and no ECR push was executed, so cold-start timings are not measured and none are claimed.
@@OUT@@

**Follow-ups:**
- *How would you measure the real cold start?* In real AWS, log the init duration and compare first and later invocations; check current docs for the log fields. Not executed here.
- *Handler returns 200 even when the model fails to load?* No. Let init errors fail loudly, and return 4xx for bad input only.
- *Why not read the model from S3 on every call?* Network and parse cost on each call; cache it in the environment (and still handle model version changes by redeploying or by a version key).

**Common mistakes:** loading in the handler; putting the model in `/tmp` and assuming it is always there; testing only through the Lambda console; a heavy `import` list you do not use; claiming layers fix cold start; no input validation.
""", ["q41_lambda_handler.py", "q41_dockerfile_check.py"], {"python": ["q41_lambda_handler.py"], "dockerfile": ["Dockerfile.lambda"]})

A[42] = (r"""
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
@@CODE@@

**Output (my run):** ran against moto with fake keys. The mock returned an empty `{}` body for `invoke_model`: it proves only that the request shape was accepted. It does not call a model, check model access, check IAM, or route through the endpoint. `create_guardrail` and `list_foundation_models` are not implemented in this moto version; invocation-logging config round-trips. Real Bedrock behaviour is not executed.
@@OUT@@

**Follow-ups:**
- *Where do Bedrock calls show up for audit?* CloudTrail records API calls (check current docs for which events); the mock has no CloudTrail lookup (Q19, Q50).
- *Who needs permission, the user or the app role?* The calling principal: usually the application's role. Developers get a narrower set in non-prod.
- *Bedrock or self-hosted model on SageMaker?* A trade-off on control, ops and cost; the LLM-serving side is Book 2.

**Common mistakes:** `bedrock:*` on `*`; forgetting the Region condition or the inference-profile ARN; logging full prompts into an open log group; assuming the mock tested guardrails; mixing Book 2 topics (prompt design) into a platform answer.
""", ["q42_bedrock.py"], {"python": ["q42_bedrock.py"]})

A[43] = (r"""
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
@@CODE@@

**Output (my run):** pyyaml parsing and the hand-written checks ran for real. In moto, `create_placement_group` raised `NotImplementedError`; a launch template with EFA and placement fields was created and read back; `describe_instance_types` returned canned GPU info. A mock cannot show real GPUs, EFA performance, quotas, capacity, or whether a placement group can be satisfied: not executed. The instance type is an example; check current docs.
@@OUT@@

**Follow-ups:**
- *Why not just more nodes?* Communication cost grows and the scaling stops being linear; measure scaling efficiency on a small run first.
- *Capacity reservation or on-demand?* Reservation guarantees capacity for the cost of paying while idle; on-demand can fail at launch. Check current docs for the exact reservation types.
- *Where do checkpoints go?* S3 or a shared file system; write them from a few ranks, sharded, and test restore.

**Common mistakes:** multi-AZ for a tightly coupled job; spot for multi-node without restart logic; ignoring quota until launch day; slow data loading hidden behind GPU purchase; claiming benchmark numbers.
""", ["q43_validate.py"], {"python": ["q43_validate.py"], "yaml": ["q43_cluster_spec.yaml"]})

A[44] = (r"""
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
@@CODE@@

**Output (my run):** the moto calls and the functions ran for real. In moto, the tagging API returned only resources that carry tags; the untagged bucket appeared only through `list_buckets`, so a real audit must start from a resource inventory, not only the tagging API (real behaviour: check current docs). Endpoint metrics here are sample data, not CloudWatch. No prices and no real bill were involved.
@@OUT@@

**Follow-ups:**
- *Why did the bill rise with no new training?* Look at idle endpoints, logging volume, NAT traffic, and storage growth first.
- *Tag enforcement?* Require tags on creation with an SCP or IAM condition (Q48, Q47), then audit.
- *Scheduled shutdown for notebooks?* Lifecycle config or a scheduled function; the exact mechanism is in current docs.

**Common mistakes:** tags that are not activated for cost reports; auditing only tagged resources; treating dev endpoints as free; ignoring data transfer; optimising instance price before utilisation.
""", ["q44_cost_tags.py"], {"python": ["q44_cost_tags.py"]})

A[45] = (r"""
**Say this first (1 line):** Separate by environment, keep an immutable raw zone, curate to partitioned Parquet, freeze training sets as versioned snapshot prefixes, and enforce names with a checker so the layout does not drift.

**Then explain:**
- Buckets: one per environment (dev, stage, prod) keeps IAM, KMS and lifecycle simple; per domain is an option when teams own data. Bucket names are global and have format rules.
- Zones: `raw` is append-only; `curated` is cleaned Parquet partitioned by date so Athena and Spark prune partitions; `snapshots/<dataset>/vNNN/` holds frozen training inputs; `models/` holds artifacts; `tmp/` expires fast.
- Governance: versioning plus Object Lock where compliance demands write-once (check current docs on modes); replication for DR or cross-account copies needs versioning on both buckets; access points give each team its own scoped door.
- Old snapshots may go to archive classes; restore from Glacier Flexible or Deep Archive has a delay, so plan retrains (Q1).
- Failure modes: replication does not copy what existed before the rule unless you backfill (check current docs); deletes and existing objects have special rules; prefix typos create parallel "zones".

**Example:** `raw/upi/ingest_date=2026-10-01/part-0.parquet` passes. `raw/upi/2026-10-01/part-0.parquet` fails (no `ingest_date=`). `snapshots/pd_train/v3/x` fails (`v003` is the convention).

**Code:** tree, regex checks and a moto bucket pair for replication.
@@CODE@@

**Output (my run):** the tree and regex checks ran for real. In moto the versioned buckets and a replication rule were accepted, and replication without source versioning was rejected. Note the mock dropped the prefix filter on read-back (`Filter` came back as an empty prefix), so a mock read-back is not proof of what real S3 stores. Real replication, Object Lock retention and Glacier restore were not executed.
@@OUT@@

**Follow-ups:**
- *Single bucket or many?* Fewer buckets are easier to manage; more buckets give hard isolation. Pick per blast radius and policy needs.
- *Why partition by date?* Query engines skip whole prefixes; but too-fine partitions create many small files (Q36).
- *Dataset version in training?* Record the snapshot prefix (or version id) in the run metadata (Part 4).

**Common mistakes:** editing raw in place; mixing environments in one bucket; no naming validation; thinking replication covers old objects automatically; assuming the mock matches real replication.
""", ["q45_datalake.py"], {"python": ["q45_datalake.py"]})

A[46] = (r"""
**Say this first (1 line):** Deploy by digest, not by tag: a digest names exact bytes, a tag can be moved; set immutable tags, scan on push, expire old images with a lifecycle policy, and grant cross-account pull explicitly.

**Then explain:**
- Repository holds images; a tag is a movable label, a digest (`sha256:...`) is the content hash. `:latest` or an unpinned tag can change under a running deployment and break reproducibility.
- Immutable tags make re-pushing an existing tag fail, which protects against silent overwrites. It does not replace pinning by digest in the manifest.
- Scan on push gives basic vulnerability findings (enhanced scanning is a separate option; check current docs). Treat findings as input to a gate, not a guarantee.
- Lifecycle policy: expire untagged or old images by rule so storage does not grow forever; test the rule so it cannot delete the tag you deploy.
- Cross-account pull: repository policy allows the other account's role, and that role also needs `ecr:GetAuthorizationToken` in its own identity policy (check current docs). Replication copies images to other Regions or accounts. In a private VPC, pulls need the ECR endpoints plus S3 for layers (Q16, Q39).

**Example:** Reference `.../ml/pd-model@sha256:<64 hex>` passes. `...:v1` fails: resolve to a digest. `...:latest` fails. `python:3.12` is not an ECR reference and fails.

**Code:** moto repo with immutable tags and lifecycle rules, then the validator.
@@CODE@@

**Output (my run):** ran against moto. The mock rejected a second push of tag `v1` with different content (`ImageAlreadyExistsException`), accepted the lifecycle and repository policy, and read them back. The digest moto stored is moto's own; the real digest comes from the registry. The validator is my own regex over the reference format, not an official parser. No image was built, scanned or pulled; scanning, lifecycle expiry timing and replication are not executed.
@@OUT@@

**Follow-ups:**
- *Why not only immutable tags?* Tags in other registries or older repos may be mutable, and humans reuse tag names; digest in the manifest is the stronger guarantee.
- *How do you get the digest in CI?* Read it from the push result or describe the image, then write it into the deploy manifest (Part 7).
- *Lifecycle deleted my prod image?* Keep a rule that protects deployed tags, or tag by environment and exclude it.

**Common mistakes:** deploying `:latest`; lifecycle rule too aggressive; forgetting the pull role's own token permission; no VPC endpoints for a private subnet; trusting "scan passed" as security sign-off.
""", ["q46_ecr.py"], {"python": ["q46_ecr.py"]})
