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
