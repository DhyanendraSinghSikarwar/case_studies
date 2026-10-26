import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import json
from iam_eval import evaluate
POLICY = {"Version": "2012-10-17", "Statement": [
 {"Sid": "ListOnlyTrainPrefix", "Effect": "Allow", "Action": "s3:ListBucket", "Resource": "arn:aws:s3:::ml-data",
  "Condition": {"StringLike": {"s3:prefix": ["train/*", "train/"]}}},
 {"Sid": "ReadTrain", "Effect": "Allow", "Action": "s3:GetObject", "Resource": "arn:aws:s3:::ml-data/train/*"},
 {"Sid": "WriteModels", "Effect": "Allow", "Action": "s3:PutObject", "Resource": "arn:aws:s3:::ml-data/models/*"},
 {"Sid": "KmsForSse", "Effect": "Allow", "Action": ["kms:Decrypt", "kms:GenerateDataKey"],
  "Resource": "arn:aws:kms:ap-south-1:123456789012:key/1111-2222"}]}
cases = [
 ("GetObject train/a.csv",       "s3:GetObject",  "arn:aws:s3:::ml-data/train/a.csv", {}),
 ("GetObject models/m.tar.gz",   "s3:GetObject",  "arn:aws:s3:::ml-data/models/m.tar.gz", {}),
 ("PutObject models/j1/model",   "s3:PutObject",  "arn:aws:s3:::ml-data/models/j1/model.tar.gz", {}),
 ("PutObject train/evil.csv",    "s3:PutObject",  "arn:aws:s3:::ml-data/train/evil.csv", {}),
 ("ListBucket on BUCKET arn, prefix train/", "s3:ListBucket", "arn:aws:s3:::ml-data", {"s3:prefix": "train/2026/"}),
 ("ListBucket on BUCKET arn, prefix ''",    "s3:ListBucket", "arn:aws:s3:::ml-data", {"s3:prefix": ""}),
 ("ListBucket with OBJECT arn (wrong ARN)", "s3:ListBucket", "arn:aws:s3:::ml-data/train/*", {"s3:prefix": "train/"}),
 ("DeleteObject models/",        "s3:DeleteObject", "arn:aws:s3:::ml-data/models/x", {}),
 ("kms:Decrypt on the key",      "kms:Decrypt",   "arn:aws:kms:ap-south-1:123456789012:key/1111-2222", {}),
 ("kms:Decrypt on another key",  "kms:Decrypt",   "arn:aws:kms:ap-south-1:123456789012:key/9999", {}),
]
for n, a, r, c in cases:
    d, why = evaluate(a, r, ctx=c, identity=[POLICY]); print(f"{n:42s} {d:5s} ({why})")
# the wildcard trap
BAD = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "arn:aws:s3:::ml-data*"}]}
for n, r in [("trap: s3:*  on ml-data*  vs ml-data-prod/secret", "arn:aws:s3:::ml-data-prod/secret.csv"),
             ("trap: s3:*  on ml-data*  vs ml-data/anything", "arn:aws:s3:::ml-data/anything")]:
    print(f"{n:55s}", evaluate("s3:DeleteObject", r, identity=[BAD])[0])

# --- moto: is policy enforcement on? ---
import json, boto3
from botocore.exceptions import ClientError
from moto import mock_aws
from moto.core import set_initial_no_auth_action_count

POL = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": "s3:ListAllMyBuckets", "Resource": "*"}]}
def run(enforce):
    @mock_aws
    def body():
        iam = boto3.client("iam"); s3 = boto3.client("s3")
        iam.create_user(UserName="u")
        iam.put_user_policy(UserName="u", PolicyName="p", PolicyDocument=json.dumps(POL))
        k = iam.create_access_key(UserName="u")["AccessKey"]
        s3.create_bucket(Bucket="ml-data")
        u = boto3.client("s3", aws_access_key_id=k["AccessKeyId"], aws_secret_access_key=k["SecretAccessKey"])
        print("  ListBuckets:", [b["Name"] for b in u.list_buckets()["Buckets"]])
        try:
            u.create_bucket(Bucket="other-bucket"); print("  CreateBucket: succeeded (no enforcement)")
        except ClientError as e:
            print("  CreateBucket:", e.response["Error"]["Code"])
    if enforce:
        set_initial_no_auth_action_count(4)(body)()   # first 4 calls unauthenticated (user setup), then enforce
    else:
        body()
print("auth enforcement OFF (default):"); run(False)
print("auth enforcement ON (set_initial_no_auth_action_count(4)):"); run(True)
