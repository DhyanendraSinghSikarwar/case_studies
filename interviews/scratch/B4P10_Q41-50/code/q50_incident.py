"""Q50: leaked key incident drill. moto_server on port 8541 (fake keys), aws CLI + boto3, scanner, time-conditioned deny via evaluator."""
import os, sys, re, json, subprocess, time, shutil
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
import boto3
from iam_eval_ext import evaluate

BIN = os.path.dirname(sys.executable); PORT = 8541; EP = f"http://127.0.0.1:{PORT}"
srv = subprocess.Popen([os.path.join(BIN, "moto_server"), "-p", str(PORT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(50):
        try: boto3.client("sts", endpoint_url=EP).get_caller_identity(); break
        except Exception: time.sleep(0.2)
    iam = boto3.client("iam", endpoint_url=EP)
    iam.create_user(UserName="ci-uploader")
    k = iam.create_access_key(UserName="ci-uploader")["AccessKey"]
    print("1. key created:", k["AccessKeyId"][:6] + "...", "status", k["Status"], "(fake moto key)")
    cli = lambda *a: subprocess.run([os.path.join(BIN, "aws"), "--endpoint-url", EP, *a], capture_output=True, text=True)
    r = cli("iam", "update-access-key", "--user-name", "ci-uploader", "--access-key-id", k["AccessKeyId"], "--status", "Inactive")
    print("2. aws iam update-access-key Inactive -> exit", r.returncode)
    print("   status now:", [(x["AccessKeyId"][:6] + "...", x["Status"]) for x in iam.list_access_keys(UserName="ci-uploader")["AccessKeyMetadata"]])
    lu = iam.get_access_key_last_used(AccessKeyId=k["AccessKeyId"])["AccessKeyLastUsed"]
    print("3. last used (what you would check in real AWS):", {x: lu.get(x) for x in ("ServiceName", "Region")})
    try:
        boto3.client("cloudtrail", endpoint_url=EP).lookup_events(LookupAttributes=[{"AttributeKey": "AccessKeyId", "AttributeValue": k["AccessKeyId"]}])
        print("4. cloudtrail lookup_events: ok")
    except Exception as e:
        print("4. cloudtrail lookup_events:", type(e).__name__, str(e)[:70])
    iam.delete_access_key(UserName="ci-uploader", AccessKeyId=k["AccessKeyId"])
    print("5. after delete, keys:", iam.list_access_keys(UserName="ci-uploader")["AccessKeyMetadata"])
finally:
    srv.terminate(); srv.wait(timeout=10)
print("   moto_server on port", PORT, "stopped")

print("\n== deny-before-time (the 'revoke active sessions' pattern) ==")
REVOKE = {"Version": "2012-10-17", "Statement": [{"Effect": "Deny", "Action": "*", "Resource": "*",
          "Condition": {"DateLessThan": {"aws:TokenIssueTime": "2026-10-26T10:00:00Z"}}}]}
BROAD = {"Statement": [{"Effect": "Allow", "Action": ["s3:*", "sagemaker:*"], "Resource": "*"}]}
role = "arn:aws:iam::123456789012:role/etl-role"
for name, ctx in [("session issued 09:00 (before cutoff; could be the attacker's)", {"aws:TokenIssueTime": "2026-10-26T09:00:00Z"}),
                  ("session issued 10:30 (after cutoff; fresh legitimate session)", {"aws:TokenIssueTime": "2026-10-26T10:30:00Z"}),
                  ("long-term user key (no TokenIssueTime in the request)", {})]:
    print(f"{name:66s}", evaluate("s3:GetObject", "arn:aws:s3:::ml-data/x", ctx=ctx, identity=[BROAD, REVOKE], principal_arn=role)[0])
print("Without the REVOKE policy the same 09:00 session:", evaluate("s3:GetObject", "arn:aws:s3:::ml-data/x", ctx={"aws:TokenIssueTime": "2026-10-26T09:00:00Z"}, identity=[BROAD])[0])

print("\n== secret scanner (flags access-key-id shape) ==")
SAMPLE = 'aws_access_key_id = AKIAIOSFODNN7EXAMPLE\nregion = ap-south-1\ntoken = ASIAIOSFODNN7EXAMPLE\n'   # AWS documentation example ids, not real
for ln, line in enumerate(SAMPLE.splitlines(), 1):
    m = re.search(r"\b(AKIA|ASIA)[A-Z0-9]{16}\b", line)
    if m: print(f"line {ln}: {m.group(0)[:4]}**** ({'long-term key' if m.group(0).startswith('AKIA') else 'temporary credential'})")
