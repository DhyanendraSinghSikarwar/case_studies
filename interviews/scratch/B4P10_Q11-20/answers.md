# Book 4 Part 10: answers Q11-Q20 (Wave B agent, scratch)

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
