import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iam_eval_sketch import evaluate
ACCT = "123456789012"
BP = f"arn:aws:iam::{ACCT}:policy/MlJobBoundary"
boundary = {"Statement": [{"Effect": "Allow", "Action": ["s3:*", "sagemaker:*", "logs:*", "ecr:Get*", "ecr:BatchGet*"], "Resource": "*"}]}
# delegation policy for ML engineers: may create roles ONLY with the boundary attached
engineer = {"Statement": [
  {"Effect": "Allow", "Action": ["iam:CreateRole", "iam:PutRolePolicy", "iam:AttachRolePolicy"], "Resource": f"arn:aws:iam::{ACCT}:role/ml-*"},
  {"Effect": "Allow", "Action": "iam:PassRole", "Resource": f"arn:aws:iam::{ACCT}:role/ml-*"}]}
# guardrail (as SCP or identity-policy deny): block CreateRole unless boundary is set
guard_deny = {"Statement": [
  {"Effect": "Deny", "Action": ["iam:CreateRole"], "Resource": "*", "Condition": {"StringNotEquals": {"iam:PermissionsBoundary": BP}}},
  {"Effect": "Deny", "Action": ["iam:DeleteRolePermissionsBoundary", "iam:PutRolePermissionsBoundary"], "Resource": "*"}]}
guard_sketch = guard_deny
scp = {"Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"}]}
scp_region = {"Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"}, {"Effect": "Deny", "Action": "sagemaker:*", "Resource": "*", "Condition": {"StringEquals": {"aws:RequestedRegion": "ap-east-1"}}}]}
role = f"arn:aws:iam::{ACCT}:role/ml-trainer"
admin_pol = {"Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"}]}  # what AdministratorAccess grants
def row(label, action, res, **kw):
    d, why = evaluate(action, res, **kw); print(f"{label:58s} {d:5s} {why}")
print("-- engineer (identity policy) creating roles")
row("engineer CreateRole ml-x, boundary supplied", "iam:CreateRole", f"arn:aws:iam::{ACCT}:role/ml-x", identity=[engineer, guard_sketch], ctx={"iam:PermissionsBoundary": BP})
row("engineer CreateRole ml-x, NO boundary (guardrail)", "iam:CreateRole", f"arn:aws:iam::{ACCT}:role/ml-x", identity=[engineer, guard_sketch], ctx={})
row("engineer CreateRole admin-x (name not ml-*)", "iam:CreateRole", f"arn:aws:iam::{ACCT}:role/admin-x", identity=[engineer], ctx={"iam:PermissionsBoundary": BP})
row("engineer removes boundary from ml-trainer", "iam:DeleteRolePermissionsBoundary", f"arn:aws:iam::{ACCT}:role/ml-trainer", identity=[engineer, guard_deny])
row("engineer attaches AdministratorAccess to ml-trainer", "iam:AttachRolePolicy", f"arn:aws:iam::{ACCT}:role/ml-trainer", identity=[engineer, guard_deny])
print("-- the created role ml-trainer: boundary + attached policies")
row("trainer s3:GetObject (identity allows, boundary allows)", "s3:GetObject", "arn:aws:s3:::ml-data/x", identity=[admin_pol], boundary=boundary)
row("trainer sagemaker:CreateTrainingJob", "sagemaker:CreateTrainingJob", "*", identity=[admin_pol], boundary=boundary)
row("trainer attached AdministratorAccess -> iam:CreateUser", "iam:CreateUser", "*", identity=[admin_pol], boundary=boundary)
row("trainer attached AdministratorAccess -> ec2:RunInstances", "ec2:RunInstances", "*", identity=[admin_pol], boundary=boundary)
row("trainer with NO boundary + AdministratorAccess -> iam:CreateUser", "iam:CreateUser", "*", identity=[admin_pol])
row("boundary allows s3 but identity grants nothing", "s3:GetObject", "arn:aws:s3:::ml-data/x", identity=[], boundary=boundary)
print("-- SCP and session policy")
row("SCP has no allow for ec2 (narrow SCP)", "ec2:RunInstances", "*", identity=[admin_pol], scps=[{"Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}]}])
row("SCP region deny, request in ap-east-1", "sagemaker:CreateTrainingJob", "*", identity=[admin_pol], scps=[scp_region], ctx={"aws:RequestedRegion": "ap-east-1"})
row("SCP region deny, request in us-east-1", "sagemaker:CreateTrainingJob", "*", identity=[admin_pol], scps=[scp_region], ctx={"aws:RequestedRegion": "us-east-1"})
sess = {"Statement": [{"Effect": "Allow", "Action": "s3:GetObject", "Resource": "arn:aws:s3:::ml-data/train/*"}]}
row("session policy: GetObject on train/ (in scope)", "s3:GetObject", "arn:aws:s3:::ml-data/train/a", identity=[admin_pol], session=sess)
row("session policy: PutObject (out of scope)", "s3:PutObject", "arn:aws:s3:::ml-data/train/a", identity=[admin_pol], session=sess)
row("session policy alone, role has no identity allow", "s3:GetObject", "arn:aws:s3:::ml-data/train/a", identity=[], session=sess)
