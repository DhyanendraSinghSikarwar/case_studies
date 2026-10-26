"""Q48: SCP documents, structural validation, moto organizations, evaluator runs. Real SCP enforcement NOT executed."""
import os, sys, json
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
import boto3
from moto import mock_aws
from iam_eval_ext import evaluate

scp = json.load(open(os.path.join(here, "scp_ml_org.json")))

def validate_scp(doc):
    errs = []
    if doc.get("Version") != "2012-10-17": errs.append("Version")
    for s in doc["Statement"]:
        if "Principal" in s or "NotPrincipal" in s: errs.append(f"{s.get('Sid')}: SCPs have no Principal element")
        if s["Effect"] not in ("Allow", "Deny"): errs.append(f"{s.get('Sid')}: Effect")
        if ("Action" in s) == ("NotAction" in s): errs.append(f"{s.get('Sid')}: need exactly one of Action/NotAction")
        if "Resource" not in s: errs.append(f"{s.get('Sid')}: Resource")
    sids = [s.get("Sid") for s in doc["Statement"]]
    if len(sids) != len(set(sids)): errs.append("duplicate Sid")
    return errs
print("SCP structural errors:", validate_scp(scp) or "none", "| statements:", len(scp["Statement"]))
bad = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": "*", "Action": "*", "Resource": "*"}]}
print("deliberately bad SCP:", validate_scp(bad))

with mock_aws():
    org = boto3.client("organizations")
    org.create_organization(FeatureSet="ALL")
    p = org.create_policy(Content=json.dumps(scp), Description="ml guardrails", Name="ml-guardrails", Type="SERVICE_CONTROL_POLICY")["Policy"]["PolicySummary"]
    print("created:", p["Name"], p["Type"], "| listed:", [x["Name"] for x in org.list_policies(Filter="SERVICE_CONTROL_POLICY")["Policies"]])
    root = org.list_roots()["Roots"][0]["Id"]
    org.attach_policy(PolicyId=p["Id"], TargetId=root)
    print("attached to root; targets:", [t["Name"] if "Name" in t else t["TargetId"] for t in org.list_targets_for_policy(PolicyId=p["Id"])["Targets"]])

print("\n== evaluator (identity policy is AdministratorAccess-like in every case) ==")
admin = {"Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"}]}
dev = "arn:aws:iam::111111111111:role/ml-engineer"; bg = "arn:aws:iam::111111111111:role/BreakGlass"
rows = [
 ("train in ap-south-1",              "sagemaker:CreateTrainingJob", {"aws:RequestedRegion": "ap-south-1", "aws:RequestTag/project": "pd"}, dev, False),
 ("train in us-east-1",               "sagemaker:CreateTrainingJob", {"aws:RequestedRegion": "us-east-1", "aws:RequestTag/project": "pd"}, dev, False),
 ("train in us-east-1 as BreakGlass", "sagemaker:CreateTrainingJob", {"aws:RequestedRegion": "us-east-1", "aws:RequestTag/project": "pd"}, bg, False),
 ("iam call from us-east-1 (global)", "iam:ListRoles",               {"aws:RequestedRegion": "us-east-1"}, dev, False),
 ("train without project tag",        "sagemaker:CreateTrainingJob", {"aws:RequestedRegion": "ap-south-1"}, dev, False),
 ("stop CloudTrail",                  "cloudtrail:StopLogging",      {"aws:RequestedRegion": "ap-south-1"}, dev, False),
 ("stop CloudTrail as BreakGlass",    "cloudtrail:StopLogging",      {"aws:RequestedRegion": "ap-south-1"}, bg, False),
 ("leave organisation",               "organizations:LeaveOrganization", {"aws:RequestedRegion": "ap-south-1"}, dev, False),
 ("leave organisation, mgmt account", "organizations:LeaveOrganization", {"aws:RequestedRegion": "ap-south-1"}, "arn:aws:iam::999999999999:role/admin", True),
]
for name, act, ctx, who, mgmt in rows:
    d = evaluate(act, "*", ctx=ctx, identity=[admin], scps=[scp], principal_arn=who, management_account=mgmt)
    print(f"{name:36s} {d[0]:5s} {d[1]}")
print("\nSimplified: no Organizations hierarchy (root -> OU -> account all need an allow), no service-linked-role exemption, no condition-key availability per action.")
