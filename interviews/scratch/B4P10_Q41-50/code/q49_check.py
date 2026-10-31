"""Q49: validate the role matrix with pyyaml, then run evaluator cases: the dev training role must not write to prod."""
import os, sys
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
import yaml
from iam_eval_ext import evaluate

m = yaml.safe_load(open(os.path.join(here, "q49_matrix.yaml")))
errs = []
for rn, r in m["roles"].items():
    if r["account"] not in m["accounts"]: errs.append(f"{rn}: unknown account")
    for c in r["can"]:
        if c["resource"] == "*" and not c["action"].startswith(("sagemaker:Create", "sagemaker:Describe")): errs.append(f"{rn}: wildcard resource on {c['action']}")
        if c["action"] in ("*", "s3:*", "iam:*"): errs.append(f"{rn}: wildcard action {c['action']}")
print("accounts:", list(m["accounts"]), "| roles:", list(m["roles"]), "| matrix errors:", errs or "none")

def ident(role):   # build an identity policy from the matrix row
    return [{"Statement": [{"Effect": "Allow", "Action": c["action"], "Resource": c["resource"]} for c in m["roles"][role]["can"]]}]
def arn(role): return f"arn:aws:iam::{m['accounts'][m['roles'][role]['account']]['id']}:role/{role}"

PROD_BUCKET = "arn:aws:s3:::acme-ml-prod-models/approved/credit_v7.tar.gz"
prod_bucket_policy = {"Statement": [
  {"Effect": "Allow", "Principal": {"AWS": [arn("model-promoter"), arn("sagemaker-endpoint-exec")]}, "Action": ["s3:PutObject", "s3:GetObject"], "Resource": "arn:aws:s3:::acme-ml-prod-models/approved/*"},
  {"Effect": "Deny", "Principal": "*", "Action": "s3:PutObject", "Resource": "arn:aws:s3:::acme-ml-prod-models/*",
   "Condition": {"ArnNotLike": {"aws:PrincipalArn": arn("model-promoter")}}}]}

def run(label, role, action, res, rp=None, same=True):
    d = evaluate(action, res, identity=ident(role), resource_policy=rp, same_account=same, principal_arn=arn(role))
    print(f"{label:62s} {d[0]:5s} {d[1]}")
    return d[0]

print("\n== cases ==")
assert run("dev training role PUT to prod bucket (cross-account)", "sagemaker-training", "s3:PutObject", PROD_BUCKET, prod_bucket_policy, same=False) == "Deny"
assert run("dev training role PUT to its own dev models/ (same account)", "sagemaker-training", "s3:PutObject", "arn:aws:s3:::acme-ml-dev-lake/models/run1/model.tar.gz") == "Allow"
no_deny = {"Statement": [prod_bucket_policy["Statement"][0]]}
assert run("same, if the Deny statement were missing (second line of defence)", "sagemaker-training", "s3:PutObject", PROD_BUCKET, no_deny, same=False) == "Deny"
assert run("dev training role reads dev snapshot", "sagemaker-training", "s3:GetObject", "arn:aws:s3:::acme-ml-dev-lake/snapshots/pd/v003/train.parquet") == "Allow"
assert run("promoter PUT to prod approved/ (both sides allow)", "model-promoter", "s3:PutObject", PROD_BUCKET, prod_bucket_policy, same=False) == "Allow"
assert run("endpoint role GET approved model (same account as bucket)", "sagemaker-endpoint-exec", "s3:GetObject", PROD_BUCKET, prod_bucket_policy) == "Allow"
assert run("endpoint role PUT to prod bucket (explicit deny in bucket policy)", "sagemaker-endpoint-exec", "s3:PutObject", PROD_BUCKET, prod_bucket_policy) == "Deny"
assert run("data-eng role reads prod model bucket", "data-eng-pipeline", "s3:GetObject", PROD_BUCKET, prod_bucket_policy, same=False) == "Deny"
print("\nTraining role cannot write to prod: shown on the simplified model above (denied twice: no allow on the bucket side, plus an explicit deny). Real AWS also applies SCPs, KMS and endpoint policies: not executed.")
