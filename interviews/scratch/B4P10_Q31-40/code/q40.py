# Q40: cross-account promotion. Uses the simplified evaluator (copied from scratch/B4P10_wavea). Principal: role in DEV or PROD.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iam_eval_sketch import evaluate
DEV, PROD = "111111111111", "222222222222"
dev_role = f"arn:aws:iam::{DEV}:role/train-role"
prod_role = f"arn:aws:iam::{PROD}:role/deploy-role"
pol = lambda act, res, eff="Allow": {"Version": "2012-10-17", "Statement": [{"Effect": eff, "Action": act, "Resource": res}]}
def rp(arn, act, res, eff="Allow"):
    return {"Version": "2012-10-17", "Statement": [{"Effect": eff, "Principal": {"AWS": arn}, "Action": act, "Resource": res}]}
art = f"arn:aws:s3:::dev-model-artifacts/models/v7/model.tar.gz"
repo = f"arn:aws:ecr:us-east-1:{DEV}:repository/risk-model"
key = f"arn:aws:kms:us-east-1:{DEV}:key/1234abcd"
trust_target = f"arn:aws:iam::{DEV}:role/model-reader"      # a role in dev that prod assumes to read artifacts

cases = [
 # (label, action, resource, kwargs)
 ("S3 both sides present",            "s3:GetObject", art, dict(identity=[pol("s3:GetObject", art)], resource_policy=rp(prod_role, "s3:GetObject", art))),
 ("S3 prod role policy missing",      "s3:GetObject", art, dict(identity=[], resource_policy=rp(prod_role, "s3:GetObject", art))),
 ("S3 dev bucket policy missing",     "s3:GetObject", art, dict(identity=[pol("s3:GetObject", art)], resource_policy=None)),
 ("ECR pull: repo policy + role",     "ecr:BatchGetImage", repo, dict(identity=[pol("ecr:BatchGetImage", repo)], resource_policy=rp(prod_role, "ecr:BatchGetImage", repo))),
 ("ECR pull: repo policy missing",    "ecr:BatchGetImage", repo, dict(identity=[pol("ecr:BatchGetImage", repo)], resource_policy=None)),
 ("KMS decrypt: key policy missing",  "kms:Decrypt", key, dict(identity=[pol("kms:Decrypt", key)], resource_policy=None)),
 ("KMS decrypt: both sides",          "kms:Decrypt", key, dict(identity=[pol("kms:Decrypt", key)], resource_policy=rp(prod_role, "kms:Decrypt", key))),
 ("AssumeRole: trust names prod only, no sts:AssumeRole in prod", "sts:AssumeRole", trust_target, dict(identity=[], resource_policy=rp(prod_role, "sts:AssumeRole", trust_target))),
 ("AssumeRole: both sides",           "sts:AssumeRole", trust_target, dict(identity=[pol("sts:AssumeRole", trust_target)], resource_policy=rp(prod_role, "sts:AssumeRole", trust_target))),
 ("S3 both sides but explicit deny in bucket policy", "s3:GetObject", art, dict(identity=[pol("s3:GetObject", art)], resource_policy={"Statement": [
      {"Effect": "Allow", "Principal": {"AWS": prod_role}, "Action": "s3:GetObject", "Resource": art},
      {"Effect": "Deny", "Principal": "*", "Action": "s3:GetObject", "Resource": art}]})),
]
print(f"{'case':58s} {'decision':8s} reason")
for label, act, res, kw in cases:
    rpol = kw.pop("resource_policy")
    if rpol is None:
        d = evaluate(act, res, same_account=False, principal_arn=prod_role, **kw)
    else:
        d = evaluate(act, res, same_account=False, principal_arn=prod_role, resource_policy=rpol, **kw)
    print(f"{label:58s} {d[0]:8s} {d[1]}")
print("simplified: the sketch ignores the S3 'resource-policy Principal is the account root' pattern, KMS key-policy-must-enable-IAM rule, ECR GetAuthorizationToken (identity-only), and grants.")
