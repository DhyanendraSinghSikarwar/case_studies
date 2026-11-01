"""Q12: tightened role policies checked with the IAM evaluator sketch. Invented names, no cloud."""
import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iam_eval_sketch import evaluate

def pol(*stmts): return {"Version": "2012-10-17", "Statement": list(stmts)}
def S(effect, action, resource, cond=None):
    d = {"Effect": effect, "Action": action, "Resource": resource}
    if cond: d["Condition"] = cond
    return d
DATA, B = "arn:aws:s3:::ml-data", "arn:aws:iam::111122223333"
OLD = pol(S("Allow", ["s3:*", "sagemaker:*", "kms:*"], "*"), S("Allow", "iam:PassRole", "*"))
TRAIN = pol(S("Allow", "s3:GetObject", f"{DATA}/train/*"),
            S("Allow", "s3:PutObject", f"{DATA}/models/*"),
            S("Allow", "s3:ListBucket", DATA, {"StringLike": {"s3:prefix": "train/*"}}),
            S("Allow", ["kms:Decrypt", "kms:GenerateDataKey"], f"{B}:key/data-key"))
SERVE = pol(S("Allow", "s3:GetObject", f"{DATA}/models/*"),
            S("Allow", "kms:Decrypt", f"{B}:key/data-key"))
CI = pol(S("Allow", ["sagemaker:CreateModel", "sagemaker:CreateEndpointConfig", "sagemaker:UpdateEndpoint"], "*"),
         S("Allow", "iam:PassRole", f"{B}:role/serving-role", {"StringEquals": {"iam:PassedToService": "sagemaker.amazonaws.com"}}))
GUARD = pol(S("Deny", "s3:*", "*", {"Bool": {"aws:SecureTransport": "false"}}),
            S("Deny", "s3:DeleteObject", f"{DATA}/models/*"))
ANYS3 = pol(S("Allow", "*", "*"))

cases = [  # name, role policies, action, resource, ctx, expected
 ("train reads train data", [TRAIN, GUARD], "s3:GetObject", f"{DATA}/train/a.csv", {"aws:SecureTransport": "true"}, "Allow"),
 ("train writes model", [TRAIN, GUARD], "s3:PutObject", f"{DATA}/models/m1/model.tar.gz", {"aws:SecureTransport": "true"}, "Allow"),
 ("train reads models (missing allow)", [TRAIN, GUARD], "s3:GetObject", f"{DATA}/models/m1/model.tar.gz", {"aws:SecureTransport": "true"}, "Deny"),
 ("train deletes model (explicit deny)", [TRAIN, ANYS3, GUARD], "s3:DeleteObject", f"{DATA}/models/m1/model.tar.gz", {"aws:SecureTransport": "true"}, "Deny"),
 ("train over plain http (explicit deny)", [TRAIN, GUARD], "s3:GetObject", f"{DATA}/train/a.csv", {"aws:SecureTransport": "false"}, "Deny"),
 ("serve reads model", [SERVE, GUARD], "s3:GetObject", f"{DATA}/models/m1/model.tar.gz", {"aws:SecureTransport": "true"}, "Allow"),
 ("serve reads train data (missing allow)", [SERVE, GUARD], "s3:GetObject", f"{DATA}/train/a.csv", {"aws:SecureTransport": "true"}, "Deny"),
 ("CI passes serving role to SageMaker", [CI], "iam:PassRole", f"{B}:role/serving-role", {"iam:PassedToService": "sagemaker.amazonaws.com"}, "Allow"),
 ("CI passes admin role (missing allow)", [CI], "iam:PassRole", f"{B}:role/admin", {"iam:PassedToService": "sagemaker.amazonaws.com"}, "Deny"),
 ("CI passes serving role to ec2 (condition fails)", [CI], "iam:PassRole", f"{B}:role/serving-role", {"iam:PassedToService": "ec2.amazonaws.com"}, "Deny"),
 ("OLD role passes admin role", [OLD], "iam:PassRole", f"{B}:role/admin", {}, "Allow"),
]
for name, pols, act, res, ctx, want in cases:
    d, why = evaluate(act, res, ctx, identity=pols)
    assert d == want, (name, d, why)
    print(f"{name:48s} {d:5s} {why}")
print(len(cases), "cases pass")

# usage report: CloudTrail-style events (invented, seeded by hand) vs what the old policy granted
events = [("train-role", "s3:GetObject"), ("train-role", "s3:PutObject"), ("train-role", "s3:ListBucket"),
          ("train-role", "kms:Decrypt"), ("train-role", "kms:GenerateDataKey")] * 40 + \
         [("serve-role", "s3:GetObject"), ("serve-role", "kms:Decrypt")] * 90 + \
         [("ci-role", "sagemaker:CreateModel"), ("ci-role", "sagemaker:UpdateEndpoint"), ("ci-role", "iam:PassRole")] * 5
used = collections.defaultdict(set)
for r, a in events: used[r].add(a)
print("old grant families: s3:*, sagemaker:*, kms:*, iam:PassRole on * (every action in each family)")
for r in sorted(used): print(f"{r}: used {len(used[r])} distinct actions -> {sorted(used[r])}")
# rule: a candidate policy must cover every observed action (else a job breaks)
cand = {"train-role": TRAIN, "serve-role": SERVE, "ci-role": CI}
probe = {"s3:GetObject": f"{DATA}/train/x", "s3:PutObject": f"{DATA}/models/x", "s3:ListBucket": DATA, "kms:Decrypt": f"{B}:key/data-key",
         "kms:GenerateDataKey": f"{B}:key/data-key", "sagemaker:CreateModel": "*", "sagemaker:UpdateEndpoint": "*", "iam:PassRole": f"{B}:role/serving-role"}
for r, acts in used.items():
    for a in acts:
        res = probe[a]
        if r == "serve-role" and a == "s3:GetObject": res = f"{DATA}/models/x"
        ctx = {"s3:prefix": "train/", "iam:PassedToService": "sagemaker.amazonaws.com"}
        d, why = evaluate(a, res, ctx, identity=[cand[r]])
        assert d == "Allow", (r, a, why)
print("replay: every observed action is still allowed by the candidate policies")
