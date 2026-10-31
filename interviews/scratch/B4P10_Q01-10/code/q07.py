import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iam_eval import evaluate

def P(action, resource="*", effect="Allow", cond=None):
    s = {"Effect": effect, "Action": action, "Resource": resource}
    if cond: s["Condition"] = cond
    return {"Version": "2012-10-17", "Statement": [s]}
OBJ = "arn:aws:s3:::ml-data/train/x.csv"
ROLE = "arn:aws:iam::111111111111:role/trainer"
RP_ROLE = {"Statement": [{"Effect": "Allow", "Principal": {"AWS": ROLE}, "Action": "s3:GetObject", "Resource": "*"}]}
CASES = [
 ("1 identity allow",                      dict(identity=[P("s3:GetObject")]), "Allow"),
 ("2 nothing says allow (implicit deny)",  dict(identity=[]), "Deny"),
 ("3 allow + explicit deny -> deny",       dict(identity=[P("s3:*"), P("s3:GetObject", effect="Deny")]), "Deny"),
 ("4 SCP ceiling lacks s3",                dict(identity=[P("s3:*")], scps=[P("ec2:*")]), "Deny"),
 ("5 SCP allows + identity allows",        dict(identity=[P("s3:*")], scps=[P("*")]), "Allow"),
 ("6 SCP explicit deny",                   dict(identity=[P("s3:*")], scps=[P("*"), P("s3:*", effect="Deny")]), "Deny"),
 ("7 boundary lacks s3",                   dict(identity=[P("s3:*")], boundary=P("ec2:*")), "Deny"),
 ("8 boundary allows s3, identity allows", dict(identity=[P("s3:*")], boundary=P("s3:*")), "Allow"),
 ("9 session policy narrows to Put",       dict(identity=[P("s3:*")], session=P("s3:PutObject")), "Deny"),
 ("10 same-account resource policy alone", dict(identity=[], resource_policy=RP_ROLE, principal_arn=ROLE), "Allow"),
 ("11 cross-account, resource side only",  dict(identity=[], resource_policy=RP_ROLE, principal_arn=ROLE, same_account=False), "Deny"),
 ("12 cross-account, both sides",          dict(identity=[P("s3:GetObject")], resource_policy=RP_ROLE, principal_arn=ROLE, same_account=False), "Allow"),
 ("13 cross-account, identity side only",  dict(identity=[P("s3:GetObject")], same_account=False), "Deny"),
]
for name, kw, want in CASES:
    d, why = evaluate("s3:GetObject", OBJ, **kw)
    assert d == want, (name, d, why)
    print(f"{name:42s} {d:5s} | {why}")
print(len(CASES), "cases, all as expected")
print("Sketch limits: no NotAction/NotResource, no policy variables, few condition operators,")
print("no resource-policy-vs-boundary corner cases beyond one rule, trust policies and KMS key policies not modelled.")
