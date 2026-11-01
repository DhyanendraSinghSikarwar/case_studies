import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import json, boto3
from moto import mock_aws

TRUST = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow",
        "Principal": {"Service": "sagemaker.amazonaws.com"}, "Action": "sts:AssumeRole"}]}
PERMS = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow",
        "Action": ["s3:GetObject"], "Resource": "arn:aws:s3:::ml-data/train/*"}]}
with mock_aws():
    iam = boto3.client("iam")
    iam.create_role(RoleName="train-role", AssumeRolePolicyDocument=json.dumps(TRUST))
    iam.put_role_policy(RoleName="train-role", PolicyName="read-train", PolicyDocument=json.dumps(PERMS))
    role = iam.get_role(RoleName="train-role")["Role"]
    print("ARN:", role["Arn"])
    print("TRUST (who can assume):", json.dumps(role["AssumeRolePolicyDocument"]))
    inl = iam.get_role_policy(RoleName="train-role", PolicyName="read-train")
    print("PERMISSIONS (what it can do):", json.dumps(inl["PolicyDocument"]))
    print("inline policy names:", iam.list_role_policies(RoleName="train-role")["PolicyNames"])
    # managed policy: standalone object, attach by ARN
    mp = iam.create_policy(PolicyName="read-train-managed", PolicyDocument=json.dumps(PERMS))["Policy"]
    iam.attach_role_policy(RoleName="train-role", PolicyArn=mp["Arn"])
    print("attached managed:", [p["PolicyName"] for p in iam.list_attached_role_policies(RoleName="train-role")["AttachedPolicies"]])
    # group and user
    iam.create_group(GroupName="ml-eng"); iam.create_user(UserName="asha")
    iam.add_user_to_group(GroupName="ml-eng", UserName="asha")
    print("groups of asha:", [g["GroupName"] for g in iam.list_groups_for_user(UserName="asha")["Groups"]])
    # a role has no password and no access key of its own
    print("role has access keys API? no: list_access_keys is for users; user keys:", iam.list_access_keys(UserName="asha")["AccessKeyMetadata"])
