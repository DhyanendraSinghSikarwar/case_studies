import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, sys
from iam_eval import evaluate

ROLE_ARN = "arn:aws:iam::123456789012:role/sm-exec"
TRUST = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow",
        "Principal": {"Service": "sagemaker.amazonaws.com"}, "Action": "sts:AssumeRole"}]}
PERMS = {"Version": "2012-10-17", "Statement": [
 {"Sid": "ReadInput", "Effect": "Allow", "Action": "s3:GetObject", "Resource": "arn:aws:s3:::ml-data/train/*"},
 {"Sid": "ListInput", "Effect": "Allow", "Action": "s3:ListBucket", "Resource": "arn:aws:s3:::ml-data",
  "Condition": {"StringLike": {"s3:prefix": "train/*"}}},
 {"Sid": "WriteOutput", "Effect": "Allow", "Action": "s3:PutObject", "Resource": "arn:aws:s3:::ml-data/models/*"},
 {"Sid": "PullImage", "Effect": "Allow", "Action": ["ecr:GetDownloadUrlForLayer", "ecr:BatchGetImage", "ecr:BatchCheckLayerAvailability"],
  "Resource": "arn:aws:ecr:ap-south-1:123456789012:repository/train-img"},
 {"Sid": "EcrToken", "Effect": "Allow", "Action": "ecr:GetAuthorizationToken", "Resource": "*"},
 {"Sid": "Logs", "Effect": "Allow", "Action": ["logs:CreateLogStream", "logs:PutLogEvents", "logs:CreateLogGroup"],
  "Resource": "arn:aws:logs:ap-south-1:123456789012:log-group:/aws/sagemaker/TrainingJobs*"}]}
# what the human/pipeline needs to launch the job
LAUNCHER = {"Version": "2012-10-17", "Statement": [
 {"Effect": "Allow", "Action": "sagemaker:CreateTrainingJob", "Resource": "*"},
 {"Effect": "Allow", "Action": "iam:PassRole", "Resource": ROLE_ARN,
  "Condition": {"StringEquals": {"iam:PassedToService": "sagemaker.amazonaws.com"}}}]}

def check(doc, kind):
    errs = []
    if doc.get("Version") != "2012-10-17": errs.append("Version must be 2012-10-17")
    st = doc.get("Statement")
    if not isinstance(st, list) or not st: return ["Statement must be a non-empty list"]
    for i, s in enumerate(st):
        if s.get("Effect") not in ("Allow", "Deny"): errs.append(f"stmt {i}: bad Effect")
        if "Action" not in s: errs.append(f"stmt {i}: no Action")
        if kind == "trust":
            if "Principal" not in s: errs.append(f"stmt {i}: trust policy needs Principal")
            if s.get("Action") != "sts:AssumeRole" and "sts:AssumeRole" not in s.get("Action", []):
                errs.append(f"stmt {i}: trust action is not sts:AssumeRole")
        else:
            if "Principal" in s: errs.append(f"stmt {i}: identity policy must not have Principal")
            if "Resource" not in s: errs.append(f"stmt {i}: no Resource")
            if s.get("Action") == "*" or s.get("Resource") == "*" and s.get("Action") not in ("ecr:GetAuthorizationToken",):
                errs.append(f"stmt {i}: wildcard Action or Resource, review")
    return errs
print("trust check:", check(TRUST, "trust") or "ok")
print("perms check:", check(PERMS, "perms") or "ok")
bad = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}]}
print("bad doc check:", check(bad, "perms"))
print("trust-as-perms check:", check(TRUST, "perms"))

ident = [PERMS]
cases = [
 ("read train object",        "s3:GetObject",    "arn:aws:s3:::ml-data/train/a.csv", {}, True),
 ("read from models prefix",  "s3:GetObject",    "arn:aws:s3:::ml-data/models/m.tar.gz", {}, False),
 ("write model output",       "s3:PutObject",    "arn:aws:s3:::ml-data/models/job1/model.tar.gz", {}, True),
 ("write into train prefix",  "s3:PutObject",    "arn:aws:s3:::ml-data/train/a.csv", {}, False),
 ("list bucket, prefix train/","s3:ListBucket",  "arn:aws:s3:::ml-data", {"s3:prefix": "train/x"}, True),
 ("list bucket, prefix models/","s3:ListBucket", "arn:aws:s3:::ml-data", {"s3:prefix": "models/"}, False),
 ("pull own image",          "ecr:BatchGetImage","arn:aws:ecr:ap-south-1:123456789012:repository/train-img", {}, True),
 ("pull other image",        "ecr:BatchGetImage","arn:aws:ecr:ap-south-1:123456789012:repository/other", {}, False),
 ("delete a bucket",         "s3:DeleteBucket",  "arn:aws:s3:::ml-data", {}, False),
]
for name, a, r, c, want in cases:
    d, why = evaluate(a, r, ctx=c, identity=ident)
    assert (d == "Allow") == want, (name, d, why)
    print(f"role    {name:28s} {d:5s} ({why})")
# launcher: PassRole to the right role vs another role
for name, rarn, c in [("PassRole sm-exec to sagemaker", ROLE_ARN, {"iam:PassedToService": "sagemaker.amazonaws.com"}),
                      ("PassRole sm-exec to ec2", ROLE_ARN, {"iam:PassedToService": "ec2.amazonaws.com"}),
                      ("PassRole admin-role", "arn:aws:iam::123456789012:role/admin", {"iam:PassedToService": "sagemaker.amazonaws.com"})]:
    d, why = evaluate("iam:PassRole", rarn, ctx=c, identity=[LAUNCHER])
    print(f"launcher {name:30s} {d:5s} ({why})")
d, why = evaluate("iam:PassRole", ROLE_ARN, ctx={"iam:PassedToService": "sagemaker.amazonaws.com"}, identity=[PERMS])
print("training role itself (no PassRole)  ", d, f"({why})")
