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
