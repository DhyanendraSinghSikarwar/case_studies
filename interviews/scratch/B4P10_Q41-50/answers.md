# Book 4 Part 10, Q41-Q50 answers (Wave B)

Runtime: Python 3.13 venv /tmp/claude-0/b10p10/v; boto3/botocore 1.43.118, moto 5.2.4 (decorator mode, plus one moto_server on port 8541 for Q50), awscli 1.46.2; fake keys only; no real AWS call. Moto does not enforce IAM by default, ignores trust policies in STS assume_role, cannot invoke Lambda without Docker, and runs no SageMaker jobs or endpoints. Real AWS behaviour, limits and prices: not executed; check current docs.

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
