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
