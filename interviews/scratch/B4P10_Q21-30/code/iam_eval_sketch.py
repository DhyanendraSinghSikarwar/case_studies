"""Pure-Python sketch of AWS IAM policy evaluation (same-account and cross-account), for Wave B reuse.
Simplified: Action/Resource wildcards (* and ?), Condition ops StringEquals/StringLike/Bool/IpAddress-less only,
NotAction/NotResource/variables not handled. Real IAM has more rules; check current docs."""
import fnmatch

def _list(x): return x if isinstance(x, list) else [x]
def _match(pats, val): return any(fnmatch.fnmatchcase(val.lower() if False else val, p) for p in _list(pats))
def _cond_ok(cond, ctx):
    for op, kv in (cond or {}).items():
        for k, vals in kv.items():
            have = ctx.get(k)
            vals = [str(v) for v in _list(vals)]
            if op == "StringEquals": ok = have in vals
            elif op == "StringLike": ok = have is not None and any(fnmatch.fnmatchcase(have, v) for v in vals)
            elif op == "StringNotEquals": ok = have not in vals  # added in this copy; missing key counts as not-equal
            elif op == "Bool": ok = str(have).lower() in [v.lower() for v in vals]
            else: raise NotImplementedError(op)
            if not ok: return False
    return True
def _stmt_hits(policy, action, resource, ctx, effect):
    for s in _list(policy.get("Statement", [])):
        if s["Effect"] == effect and _match(s["Action"], action) and _match(s["Resource"], resource) and _cond_ok(s.get("Condition"), ctx):
            return True
    return False

def evaluate(action, resource, ctx=None, identity=(), boundary=None, scps=(), session=None, resource_policy=None, same_account=True, principal_arn=None):
    """Return (decision, reason). Order: explicit deny anywhere -> SCPs -> boundary/session -> allow."""
    ctx = ctx or {}
    all_pols = list(identity) + list(scps) + ([boundary] if boundary else []) + ([session] if session else []) + ([resource_policy] if resource_policy else [])
    if any(_stmt_hits(p, action, resource, ctx, "Deny") for p in all_pols):
        return "Deny", "explicit deny"
    for i, scp in enumerate(scps):
        if not _stmt_hits(scp, action, resource, ctx, "Allow"):
            return "Deny", f"implicit deny: SCP level {i} does not allow"
    rp_allow = bool(resource_policy) and _stmt_hits_principal(resource_policy, action, resource, ctx, principal_arn)
    ident_allow = any(_stmt_hits(p, action, resource, ctx, "Allow") for p in identity)
    if boundary is not None and not _stmt_hits(boundary, action, resource, ctx, "Allow") and not (rp_allow and same_account and _rp_names_principal_arn(resource_policy, principal_arn)):
        return "Deny", "implicit deny: outside permissions boundary"
    if session is not None and not _stmt_hits(session, action, resource, ctx, "Allow"):
        return "Deny", "implicit deny: outside session policy"
    if same_account:
        if ident_allow or rp_allow: return "Allow", "identity or resource policy allows (same account)"
        return "Deny", "implicit deny: nothing allows"
    # cross account: both sides must allow
    if ident_allow and rp_allow: return "Allow", "cross-account: identity AND resource policy allow"
    return "Deny", "implicit deny: cross-account needs both sides"

def _stmt_hits_principal(rp, action, resource, ctx, principal_arn):
    for s in _list(rp.get("Statement", [])):
        pr = s.get("Principal")
        pr_ok = pr == "*" or (isinstance(pr, dict) and principal_arn in _list(pr.get("AWS", [])) or (isinstance(pr, dict) and "*" in _list(pr.get("AWS", []))))
        if s["Effect"] == "Allow" and pr_ok and _match(s["Action"], action) and _match(s["Resource"], resource) and _cond_ok(s.get("Condition"), ctx):
            return True
    return False
def _rp_names_principal_arn(rp, arn):
    # resource policy naming the exact role/user ARN is not limited by the boundary; naming the account root IS limited
    return any(isinstance(s.get("Principal"), dict) and arn in _list(s["Principal"].get("AWS", [])) for s in _list(rp["Statement"]) if s["Effect"] == "Allow")

if __name__ == "__main__":
    A = lambda a, r="*", e="Allow", c=None: {"Version": "2012-10-17", "Statement": [{"Effect": e, "Action": a, "Resource": r, **({"Condition": c} if c else {})}]}
    obj = "arn:aws:s3:::ml-data/train/x.csv"
    cases = [
        ("allow via identity", dict(identity=[A("s3:GetObject", "arn:aws:s3:::ml-data/*")]), "Allow"),
        ("no policy -> implicit deny", dict(identity=[]), "Deny"),
        ("explicit deny beats allow", dict(identity=[A("s3:*"), A("s3:GetObject", e="Deny")]), "Deny"),
        ("boundary narrows", dict(identity=[A("s3:*")], boundary=A("ec2:*")), "Deny"),
        ("SCP without allow", dict(identity=[A("s3:*")], scps=[A("ec2:*")]), "Deny"),
        ("SCP allows + identity allows", dict(identity=[A("s3:*")], scps=[A("*")]), "Allow"),
        ("SCP deny", dict(identity=[A("s3:*")], scps=[A("*"), A("s3:GetObject", e="Deny")]), "Deny"),
        ("session policy narrows", dict(identity=[A("s3:*")], session=A("s3:PutObject")), "Deny"),
        ("cond: deny unless MFA", dict(identity=[A("s3:*"), A("s3:*", e="Deny", c={"Bool": {"aws:MultiFactorAuthPresent": "false"}})], ctx={"aws:MultiFactorAuthPresent": "false"}), "Deny"),
        ("cond: MFA present -> allow", dict(identity=[A("s3:*"), A("s3:*", e="Deny", c={"Bool": {"aws:MultiFactorAuthPresent": "false"}})], ctx={"aws:MultiFactorAuthPresent": "true"}), "Allow"),
        ("same-account resource policy alone allows", dict(identity=[], resource_policy={"Statement": [{"Effect": "Allow", "Principal": {"AWS": "arn:aws:iam::111:role/r"}, "Action": "s3:GetObject", "Resource": "*"}]}, principal_arn="arn:aws:iam::111:role/r"), "Allow"),
        ("cross-account: resource policy only", dict(identity=[], same_account=False, resource_policy={"Statement": [{"Effect": "Allow", "Principal": {"AWS": "arn:aws:iam::111:role/r"}, "Action": "s3:GetObject", "Resource": "*"}]}, principal_arn="arn:aws:iam::111:role/r"), "Deny"),
        ("cross-account: both", dict(identity=[A("s3:GetObject")], same_account=False, resource_policy={"Statement": [{"Effect": "Allow", "Principal": {"AWS": "arn:aws:iam::111:role/r"}, "Action": "s3:GetObject", "Resource": "*"}]}, principal_arn="arn:aws:iam::111:role/r"), "Allow"),
    ]
    for name, kw, want in cases:
        got = evaluate("s3:GetObject", obj, **kw)
        assert got[0] == want, (name, got)
        print(f"{name:45s} {got[0]:5s} ({got[1]})")
    print("all", len(cases), "cases pass")
