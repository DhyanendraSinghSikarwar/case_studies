import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from botocore.exceptions import ClientError
from moto import mock_aws

with mock_aws():
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="consist-demo")
    s3.put_object(Bucket="consist-demo", Key="data/v1.txt", Body=b"first")
    s3.put_object(Bucket="consist-demo", Key="data/v1.txt", Body=b"second")
    print("overwrite then read:", s3.get_object(Bucket="consist-demo", Key="data/v1.txt")["Body"].read())
    for i in range(3):
        s3.put_object(Bucket="consist-demo", Key=f"data/part-{i}.csv", Body=b"r")
    keys = [o["Key"] for o in s3.list_objects_v2(Bucket="consist-demo", Prefix="data/")["Contents"]]
    print("list after put:", keys)
    # prefixes are just string prefixes: Delimiter makes the 'folder' view
    r = s3.list_objects_v2(Bucket="consist-demo", Delimiter="/")
    print("common prefixes:", [p["Prefix"] for p in r["CommonPrefixes"]])
    # no rename: copy + delete = two calls, not atomic
    s3.copy_object(Bucket="consist-demo", Key="data/renamed.txt", CopySource={"Bucket": "consist-demo", "Key": "data/v1.txt"})
    s3.delete_object(Bucket="consist-demo", Key="data/v1.txt")
    print("after copy+delete:", sorted(o["Key"] for o in s3.list_objects_v2(Bucket="consist-demo", Prefix="data/")["Contents"]))
    # conditional put
    s3.put_object(Bucket="consist-demo", Key="lock/owner", Body=b"job-A", IfNoneMatch="*")
    print("first conditional put: ok")
    try:
        s3.put_object(Bucket="consist-demo", Key="lock/owner", Body=b"job-B", IfNoneMatch="*")
    except ClientError as e:
        print("second conditional put:", e.response["Error"]["Code"], e.response["ResponseMetadata"]["HTTPStatusCode"])
    print("owner is still:", s3.get_object(Bucket="consist-demo", Key="lock/owner")["Body"].read())

# reader/writer: a manifest makes a dataset 'commit' without multi-object atomicity
def writer(s3, n_parts, crash_after=None):
    for i in range(n_parts):
        if crash_after is not None and i == crash_after: return
        s3.put_object(Bucket="consist-demo", Key=f"ds/run1/part-{i}", Body=b"p")
    s3.put_object(Bucket="consist-demo", Key="ds/run1/_MANIFEST.json", Body=b'{"parts": %d}' % n_parts)
def reader(s3):
    try:
        s3.head_object(Bucket="consist-demo", Key="ds/run1/_MANIFEST.json")
    except ClientError:
        return "not committed: skip"
    n = len(s3.list_objects_v2(Bucket="consist-demo", Prefix="ds/run1/part-").get("Contents", []))
    return f"read {n} parts"
with mock_aws():
    s3 = boto3.client("s3"); s3.create_bucket(Bucket="consist-demo")
    writer(s3, 4, crash_after=2)
    print("writer crashed -> reader says:", reader(s3))
    writer(s3, 4)
    print("writer finished -> reader says:", reader(s3))
