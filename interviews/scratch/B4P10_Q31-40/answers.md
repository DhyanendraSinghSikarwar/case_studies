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

