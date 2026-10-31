import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3, requests
from urllib.parse import urlparse, parse_qs
from moto import mock_aws

with mock_aws():
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="share-demo")
    s3.put_object(Bucket="share-demo", Key="reports/r1.txt", Body=b"hello report")
    url = s3.generate_presigned_url("get_object", Params={"Bucket": "share-demo", "Key": "reports/r1.txt"}, ExpiresIn=300)
    q = parse_qs(urlparse(url).query)
    print("GET url query params:", sorted(q))
    print("Expires param is an epoch-seconds value:", q["Expires"][0].isdigit())
    r = requests.get(url); print("GET with requests:", r.status_code, r.content)
    # PUT presign
    purl = s3.generate_presigned_url("put_object", Params={"Bucket": "share-demo", "Key": "uploads/u1.txt"}, ExpiresIn=300)
    r = requests.put(purl, data=b"uploaded by a client with no keys"); print("PUT with requests:", r.status_code)
    print("object now:", s3.get_object(Bucket="share-demo", Key="uploads/u1.txt")["Body"].read())
    # presigned POST with conditions
    post = s3.generate_presigned_post("share-demo", "uploads/${filename}",
        Fields={"Content-Type": "text/plain"},
        Conditions=[["content-length-range", 1, 1048576], {"Content-Type": "text/plain"}, ["starts-with", "$key", "uploads/"]],
        ExpiresIn=300)
    print("POST url:", post["url"])
    print("POST fields:", sorted(post["fields"]))
    import base64, json
    pol = json.loads(base64.b64decode(post["fields"]["policy"]))
    print("POST policy conditions:", pol["conditions"])
    r = requests.post(post["url"], data=post["fields"], files={"file": ("a.txt", b"small file")})
    print("POST upload:", r.status_code)
    # big file against the 1 MiB condition, to see what moto does
    r = requests.post(post["url"], data=post["fields"], files={"file": ("big.txt", b"x" * 2_000_000)})
    print("POST 2 MB (condition max 1 MiB) status in moto:", r.status_code)

# expired URL: signed in the past
import time
from unittest import mock
with mock_aws():
    s3 = boto3.client("s3"); s3.create_bucket(Bucket="share-demo"); s3.put_object(Bucket="share-demo", Key="k", Body=b"v")
    url = s3.generate_presigned_url("get_object", Params={"Bucket": "share-demo", "Key": "k"}, ExpiresIn=1)
    time.sleep(2.2)
    r = requests.get(url); print("GET after expiry:", r.status_code, "(moto)" )
