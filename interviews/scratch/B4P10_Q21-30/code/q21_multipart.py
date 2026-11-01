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
