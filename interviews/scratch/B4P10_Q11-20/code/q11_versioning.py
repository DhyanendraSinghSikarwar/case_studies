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
