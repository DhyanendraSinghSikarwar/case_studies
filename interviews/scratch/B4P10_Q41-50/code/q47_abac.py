"""Q47: ABAC with the extended evaluator + moto session-tag shape. Simplified evaluator; see 'not modelled' list at the end."""
import os, sys, json
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iam_eval_ext import evaluate

# ONE policy for every team. Access follows the tag match, not a per-team policy.
ABAC = {"Version": "2012-10-17", "Statement": [
  {"Sid": "ReadOwnTeamData", "Effect": "Allow", "Action": ["s3:GetObject"], "Resource": "*",
   "Condition": {"StringEquals": {"aws:ResourceTag/team": "${aws:PrincipalTag/team}"}}},
  {"Sid": "CreateOnlyWithOwnTeamTag", "Effect": "Allow", "Action": ["sagemaker:CreateTrainingJob"], "Resource": "*",
   "Condition": {"StringEquals": {"aws:RequestTag/team": "${aws:PrincipalTag/team}"}}},
  {"Sid": "DenyTagTampering", "Effect": "Deny", "Action": ["s3:PutObjectTagging", "s3:PutBucketTagging"], "Resource": "*"},
]}
obj = "arn:aws:s3:::lake/curated/x.parquet"
cases = [
 ("team-a reads team-a data",  "s3:GetObject", {"aws:PrincipalTag/team": "team-a", "aws:ResourceTag/team": "team-a"}, "Allow"),
 ("team-b reads team-a data",  "s3:GetObject", {"aws:PrincipalTag/team": "team-b", "aws:ResourceTag/team": "team-a"}, "Deny"),
 ("principal has NO team tag", "s3:GetObject", {"aws:ResourceTag/team": "team-a"}, "Deny"),
 ("resource has NO team tag",  "s3:GetObject", {"aws:PrincipalTag/team": "team-a"}, "Deny"),
 ("team-a creates job tagged team-a", "sagemaker:CreateTrainingJob", {"aws:PrincipalTag/team": "team-a", "aws:RequestTag/team": "team-a"}, "Allow"),
 ("team-a creates job tagged team-b", "sagemaker:CreateTrainingJob", {"aws:PrincipalTag/team": "team-a", "aws:RequestTag/team": "team-b"}, "Deny"),
 ("team-a creates job, NO tag (tag-on-create missing)", "sagemaker:CreateTrainingJob", {"aws:PrincipalTag/team": "team-a"}, "Deny"),
 ("team-b retags team-a object (trap, blocked by explicit deny)", "s3:PutObjectTagging", {"aws:PrincipalTag/team": "team-b"}, "Deny"),
]
for name, act, ctx, want in cases:
    got = evaluate(act, obj, ctx=ctx, identity=[ABAC]); assert got[0] == want, (name, got)
    print(f"{name:58s} {got[0]:5s} {got[1]}")

# The trap: if the same role may change tags, ABAC collapses. Remove the tag-deny and let team-b re-tag the data first.
no_guard = {"Version": "2012-10-17", "Statement": [s for s in ABAC["Statement"] if s["Sid"] != "DenyTagTampering"] +
            [{"Effect": "Allow", "Action": "s3:PutObjectTagging", "Resource": "*"}]}
print("\n== trap: tag-editing allowed ==")
print("step 1 team-b retags object   ->", evaluate("s3:PutObjectTagging", obj, ctx={"aws:PrincipalTag/team": "team-b"}, identity=[no_guard]))
print("step 2 team-b now reads it    ->", evaluate("s3:GetObject", obj, ctx={"aws:PrincipalTag/team": "team-b", "aws:ResourceTag/team": "team-b"}, identity=[no_guard]))

import boto3
from moto import mock_aws
with mock_aws():
    sts = boto3.client("sts"); iam = boto3.client("iam")
    iam.create_role(RoleName="ml-eng", AssumeRolePolicyDocument=json.dumps({"Version": "2012-10-17", "Statement": [
        {"Effect": "Allow", "Principal": {"AWS": "arn:aws:iam::123456789012:root"}, "Action": ["sts:AssumeRole", "sts:TagSession"]}]}))
    r = sts.assume_role(RoleArn="arn:aws:iam::123456789012:role/ml-eng", RoleSessionName="alice",
                        Tags=[{"Key": "team", "Value": "team-a"}], TransitiveTagKeys=["team"])
    print("\nmoto assume_role with session tags accepted; keys returned:", sorted(k for k in r["Credentials"]))
    print("(moto IAM enforcement is off by default, so these session tags drove no policy decision here)")

print("\nSTILL NOT MODELLED: multi-value tag operators (ForAllValues/ForAnyValue), case rules for tag keys, services that ignore tag conditions,\n"
      "tag-on-create vs tag-after-create API differences per service, whether aws:RequestTag applies to a given action, session-tag transitivity,\n"
      "tags on the role vs on the session precedence, tag policies, and anything in a real account's Organization.")
