import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import json, boto3
from moto import mock_aws

RULES = {"Rules": [
  {"ID": "raw-tiering", "Status": "Enabled", "Filter": {"Prefix": "raw/"},
   "Transitions": [{"Days": 30, "StorageClass": "STANDARD_IA"}, {"Days": 90, "StorageClass": "GLACIER"}],
   "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7}},
  {"ID": "tmp-expire", "Status": "Enabled", "Filter": {"Prefix": "tmp/"},
   "Expiration": {"Days": 14},
   "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 3}},
]}
with mock_aws():
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="ml-lake-demo")
    s3.put_bucket_lifecycle_configuration(Bucket="ml-lake-demo", LifecycleConfiguration=RULES)
    got = s3.get_bucket_lifecycle_configuration(Bucket="ml-lake-demo")["Rules"]
    for r in got:
        print(r["ID"], r["Status"], r["Filter"],
              [(t["Days"], t["StorageClass"]) for t in r.get("Transitions", [])],
              "expire", r.get("Expiration"), "abort-mpu", r["AbortIncompleteMultipartUpload"])
    # a PUT with an explicit class is accepted; moto does not move objects over time
    s3.put_object(Bucket="ml-lake-demo", Key="raw/a.csv", Body=b"x", StorageClass="STANDARD_IA")
    print("class on put:", s3.head_object(Bucket="ml-lake-demo", Key="raw/a.csv").get("StorageClass"))
    # expiry before transition is a rejected config? try a bad one: Days below the 30-day minimum for STANDARD_IA
    bad = {"Rules": [{"ID": "bad", "Status": "Enabled", "Filter": {"Prefix": "x/"},
                      "Transitions": [{"Days": 5, "StorageClass": "STANDARD_IA"}]}]}
    try:
        s3.put_bucket_lifecycle_configuration(Bucket="ml-lake-demo", LifecycleConfiguration=bad)
        print("moto accepted a 5-day STANDARD_IA transition (real S3 enforces a 30-day minimum; check current docs)")
    except Exception as e:
        print("rejected:", type(e).__name__)
