"""AccessDenied checklist as code. Reuses the simplified evaluator (iam_eval_sketch.py, copied unmodified).
Layers are checked in the order an on-call engineer would look. Simplified: see notes printed at the end."""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iam_eval_sketch import evaluate

ROLE = "arn:aws:iam::111111111111:role/sm-exec"
OBJ = "arn:aws:s3:::ml-data/train/part-0.csv"
KEY_ARN = "arn:aws:kms:us-east-1:111111111111:key/abc"

def A(action, res="*", eff="Allow"):
    return {"Version": "2012-10-17", "Statement": [{"Effect": eff, "Action": action, "Resource": res}]}

def rp(principal, action, res="*"):
    return {"Statement": [{"Effect": "Allow", "Principal": {"AWS": principal}, "Action": action, "Resource": res}]}

GOOD = {
    "caller_arn": ROLE,                        # who CloudTrail says made the call
    "expected_role": ROLE,                     # who we THINK the job runs as
    "job_region": "us-east-1", "bucket_region": "us-east-1",
    "bucket_account_same": True,
    "role_policy": [A(["s3:GetObject", "s3:ListBucket"], ["arn:aws:s3:::ml-data", "arn:aws:s3:::ml-data/train/*"]),
                    A(["kms:Decrypt", "kms:GenerateDataKey"], KEY_ARN)],
    "boundary": None, "scps": [], "bucket_policy": None,
    "bucket_sse_kms": True,
    "key_policy": rp(ROLE, ["kms:Decrypt", "kms:GenerateDataKey"], "*"),
    "vpc_endpoint_policy": None,               # None = default full-access endpoint policy
    "bpa_blocks_public_policy_only": True,     # informational: BPA does not deny a named-principal grant
    "objects_owned_by_other_account_with_acl": False,
}

def check(cfg):
    """Return (layer, detail) of the first layer that denies, or None."""
    if cfg["caller_arn"] != cfg["expected_role"]:
        return ("real caller", f"caller is {cfg['caller_arn']}, not {cfg['expected_role']}")
    if cfg["job_region"] != cfg["bucket_region"] and cfg.get("strict_region"):
        return ("region", "bucket in another Region than the job config expects")
    d, why = evaluate("s3:GetObject", OBJ, identity=cfg["role_policy"], boundary=cfg["boundary"], scps=cfg["scps"],
                      resource_policy=cfg["bucket_policy"], same_account=cfg["bucket_account_same"], principal_arn=cfg["caller_arn"])
    if d == "Deny":
        layer = ("policy stack (explicit deny, SCP, boundary, role or bucket policy)")
        if "explicit deny" in why: layer = "explicit deny somewhere (role, bucket, SCP or boundary)"
        elif "SCP" in why: layer = "SCP"
        elif "boundary" in why: layer = "permissions boundary"
        elif "cross-account" in why: layer = "bucket policy (cross-account needs both sides)"
        else: layer = "role policy (or bucket policy) gives no allow"
        return (layer, why)
    if cfg["bucket_sse_kms"]:
        d, why = evaluate("kms:Decrypt", KEY_ARN, identity=cfg["role_policy"], resource_policy=cfg["key_policy"], same_account=True, principal_arn=cfg["caller_arn"])
        # KMS is an exception: the KEY POLICY must allow (directly or by delegating to IAM); role policy alone is not enough
        key_ok = cfg["key_policy"] is not None and any(
            s["Effect"] == "Allow" and s.get("Principal", {}).get("AWS") in (cfg["caller_arn"], "arn:aws:iam::111111111111:root")
            for s in cfg["key_policy"]["Statement"])
        if not key_ok:
            return ("kms key policy", "key policy neither names the role nor delegates to IAM (role policy alone is not enough)")
        if d == "Deny":
            return ("kms role permission", why)
    if cfg["vpc_endpoint_policy"] is not None:
        d, why = evaluate("s3:GetObject", OBJ, identity=[cfg["vpc_endpoint_policy"]])
        if d == "Deny":
            return ("vpc endpoint policy", why)
    if cfg["objects_owned_by_other_account_with_acl"]:
        return ("object ownership", "objects owned by another account and bucket owner enforced is off")
    return None

def variant(**kw):
    c = copy.deepcopy(GOOD); c.update(kw); return c

SCEN = [
    ("fixed / healthy config", GOOD),
    ("job really runs as a different role", variant(caller_arn="arn:aws:iam::111111111111:role/notebook-user")),
    ("role policy missing the train/ prefix", variant(role_policy=[A("s3:GetObject", "arn:aws:s3:::ml-data/other/*")])),
    ("boundary does not include s3", variant(boundary=A("ec2:*"))),
    ("SCP allows only ec2", variant(scps=[A("ec2:*")])),
    ("explicit deny in bucket policy", variant(bucket_policy={"Statement": [{"Effect": "Deny", "Principal": "*", "Action": "s3:GetObject", "Resource": "*"}]})),
    ("bucket in other account, no bucket policy", variant(bucket_account_same=False)),
    ("SSE-KMS key policy does not name the role", variant(key_policy=rp("arn:aws:iam::111111111111:role/other", ["kms:Decrypt"], "*"))),
    ("VPC endpoint policy only allows another bucket", variant(vpc_endpoint_policy=A("s3:GetObject", "arn:aws:s3:::other-bucket/*"))),
    ("objects owned by another account", variant(objects_owned_by_other_account_with_acl=True)),
]
for name, cfg in SCEN:
    r = check(cfg)
    print(f"{name:48s} -> {('PASS (no layer denies)' if r is None else 'DENY at ' + r[0])}")
    if r: print(f"{'':51s}evidence: {r[1]}")
print("\nSimplified: Block Public Access, Region redirects and ACLs are modelled as flags, not real evaluation.")
