import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import json, boto3
from botocore.exceptions import ClientError, ParamValidationError
from moto import mock_aws

# role in THIS account whose trust policy names a DIFFERENT account (999999999999)
TRUST_OTHER = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow",
    "Principal": {"AWS": "arn:aws:iam::999999999999:root"}, "Action": "sts:AssumeRole",
    "Condition": {"StringEquals": {"sts:ExternalId": "partner-42"}}}]}
with mock_aws():
    iam = boto3.client("iam"); sts = boto3.client("sts")
    print("caller:", sts.get_caller_identity()["Arn"])
    iam.create_role(RoleName="r", AssumeRolePolicyDocument=json.dumps(TRUST_OTHER))
    resp = sts.assume_role(RoleArn="arn:aws:iam::123456789012:role/r", RoleSessionName="train-job-7", DurationSeconds=900)
    c = resp["Credentials"]
    print("response keys:", sorted(k for k in resp if k != "ResponseMetadata"))
    print("credential keys:", sorted(c))
    print("AssumedRoleUser.Arn:", resp["AssumedRoleUser"]["Arn"])
    print("access key id starts with:", c["AccessKeyId"][:4], "| token length > 0:", len(c["SessionToken"]) > 0)
    print("Expiration present:", "Expiration" in c)
    print("MOTO ACCEPTED: caller is account 123456789012, trust names 999999999999, no ExternalId passed.")
    # session name length rule is validated
    try:
        sts.assume_role(RoleArn="arn:aws:iam::123456789012:role/r", RoleSessionName="x")
    except ParamValidationError as e:
        print("short session name rejected client-side by botocore:", str(e).splitlines()[-1].strip())
    # role chaining shape: use the temp creds to call STS again
    chained = boto3.client("sts", aws_access_key_id=c["AccessKeyId"], aws_secret_access_key=c["SecretAccessKey"], aws_session_token=c["SessionToken"])
    iam.create_role(RoleName="r2", AssumeRolePolicyDocument=json.dumps(TRUST_OTHER))
    r2 = chained.assume_role(RoleArn="arn:aws:iam::123456789012:role/r2", RoleSessionName="hop-2")
    print("chained ARN:", r2["AssumedRoleUser"]["Arn"])

# what real AWS checks, as a small trust evaluator (simplified)
def trust_allows(trust, caller_account, ctx):
    for s in trust["Statement"]:
        p = s["Principal"].get("AWS", [])
        p = p if isinstance(p, list) else [p]
        who = any(x == f"arn:aws:iam::{caller_account}:root" for x in p)
        cond = all(ctx.get(k) == v for op, kv in s.get("Condition", {}).items() for k, v in kv.items())
        if s["Effect"] == "Allow" and who and cond: return True
    return False
print("real-AWS-style trust check, caller 123456789012:", trust_allows(TRUST_OTHER, "123456789012", {}))
print("caller 999999999999 without ExternalId:        ", trust_allows(TRUST_OTHER, "999999999999", {}))
print("caller 999999999999 with ExternalId partner-42:", trust_allows(TRUST_OTHER, "999999999999", {"sts:ExternalId": "partner-42"}))
