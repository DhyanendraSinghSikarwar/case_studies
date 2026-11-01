"""Extended pure-Python IAM evaluator, derived from scratch/B4P10_wavea/iam_eval_sketch.py (copied, not modified).
Adds: NotAction, NotResource, policy variables (${aws:PrincipalTag/team}), negated and IfExists condition
operators, Null, Date operators, principal-aware resource-policy Deny, management-account SCP exemption.
STILL SIMPLIFIED. Not modelled: KMS key-policy rules, trust-policy exception, VPC endpoint policies, Block Public Access,
resource-control policies, service-linked roles, most condition operators and keys, case rules. Check current AWS docs."""
import fnmatch
from datetime import datetime

def L(x): return x if isinstance(x, list) else [x]

def _sub(s, ctx):
    s = str(s)
    for k, v in ctx.items():
        s = s.replace("${" + k + "}", str(v))
    return s

def _pmatch(pats, val, ctx):
    return any(fnmatch.fnmatchcase(val, _sub(p, ctx)) for p in L(pats))

def _dt(x): return datetime.fromisoformat(str(x).replace("Z", "+00:00"))

def _cond_ok(cond, ctx):
    for op, kv in (cond or {}).items():
        if_exists = op.endswith("IfExists"); base = op[:-8] if if_exists else op
        for k, vals in kv.items():
            have = ctx.get(k)
            vals = [_sub(v, ctx) for v in L(vals)]
            if base == "Null":
                ok = (have is None) == (vals[0].lower() == "true")
            elif have is None:
                ok = if_exists or base in ("StringNotEquals", "StringNotLike", "ArnNotLike", "ArnNotEquals")
            elif base in ("StringEquals", "ArnEquals"): ok = have in vals
            elif base in ("StringLike", "ArnLike"): ok = any(fnmatch.fnmatchcase(have, v) for v in vals)
            elif base in ("StringNotEquals", "ArnNotEquals"): ok = have not in vals
            elif base in ("StringNotLike", "ArnNotLike"): ok = not any(fnmatch.fnmatchcase(have, v) for v in vals)
            elif base == "Bool": ok = str(have).lower() in [v.lower() for v in vals]
            elif base == "DateLessThan": ok = _dt(have) < _dt(vals[0])
            elif base == "DateGreaterThan": ok = _dt(have) > _dt(vals[0])
            else: raise NotImplementedError(op)
            if not ok: return False
    return True

def _principal_ok(s, principal_arn):
    pr = s.get("Principal")
    if pr is None: return True              # identity-based or SCP statement: no Principal element
    if pr == "*": return True
    if not isinstance(pr, dict) or not principal_arn: return False
    acct = principal_arn.split(":")[4] if principal_arn.count(":") >= 4 else ""
    for p in L(pr.get("AWS", [])):
        if p == "*" or p == principal_arn or p == f"arn:aws:iam::{acct}:root": return True
    return False

def _hit(policy, action, resource, ctx, effect, principal_arn=None):
    for s in L(policy.get("Statement", [])):
        if s["Effect"] != effect: continue
        a_ok = (not _pmatch(s["NotAction"], action, ctx)) if "NotAction" in s else _pmatch(s["Action"], action, ctx)
        r_ok = (not _pmatch(s["NotResource"], resource, ctx)) if "NotResource" in s else _pmatch(s.get("Resource", "*"), resource, ctx)
        if a_ok and r_ok and _principal_ok(s, principal_arn) and _cond_ok(s.get("Condition"), ctx):
            return True
    return False

def _names_arn(rp, arn):
    return any(isinstance(s.get("Principal"), dict) and arn in L(s["Principal"].get("AWS", []))
               for s in L(rp["Statement"]) if s["Effect"] == "Allow")

def evaluate(action, resource, ctx=None, identity=(), boundary=None, scps=(), session=None, resource_policy=None,
             same_account=True, principal_arn=None, management_account=False):
    ctx = dict(ctx or {})
    if principal_arn: ctx.setdefault("aws:PrincipalArn", principal_arn)
    scps = [] if management_account else list(scps)      # SCPs do not affect the management account
    pols = list(identity) + scps + ([boundary] if boundary else []) + ([session] if session else [])
    if any(_hit(p, action, resource, ctx, "Deny") for p in pols) or \
       (resource_policy and _hit(resource_policy, action, resource, ctx, "Deny", principal_arn)):
        return "Deny", "explicit deny"
    for i, scp in enumerate(scps):
        if not _hit(scp, action, resource, ctx, "Allow"): return "Deny", f"implicit deny: SCP level {i} has no allow"
    rp_allow = bool(resource_policy) and _hit(resource_policy, action, resource, ctx, "Allow", principal_arn)
    ident_allow = any(_hit(p, action, resource, ctx, "Allow") for p in identity)
    if boundary is not None and not _hit(boundary, action, resource, ctx, "Allow") and not (rp_allow and same_account and _names_arn(resource_policy, principal_arn)):
        return "Deny", "implicit deny: outside permissions boundary"
    if session is not None and not _hit(session, action, resource, ctx, "Allow"):
        return "Deny", "implicit deny: outside session policy"
    if same_account:
        return ("Allow", "identity or resource policy allows (same account)") if (ident_allow or rp_allow) else ("Deny", "implicit deny: nothing allows")
    if ident_allow and rp_allow: return "Allow", "cross-account: identity AND resource policy allow"
    return "Deny", "implicit deny: cross-account needs both sides" + ("" if ident_allow or rp_allow else " (neither present)")

if __name__ == "__main__":
    P = lambda **s: {"Version": "2012-10-17", "Statement": [s]}
    obj = "arn:aws:s3:::b/k"
    t = [
     ("allow", dict(identity=[P(Effect="Allow", Action="s3:*", Resource="*")]), "Allow"),
     ("NotAction deny, other action", dict(identity=[P(Effect="Allow", Action="*", Resource="*"), P(Effect="Deny", NotAction="iam:*", Resource="*")]), "Deny"),
     ("variable ${aws:PrincipalTag/team}", dict(ctx={"aws:PrincipalTag/team": "a"}, identity=[P(Effect="Allow", Action="s3:*", Resource="*", Condition={"StringEquals": {"aws:ResourceTag/team": "${aws:PrincipalTag/team}"}})]), "Deny"),
     ("management account skips SCP", dict(identity=[P(Effect="Allow", Action="*", Resource="*")], scps=[P(Effect="Deny", Action="*", Resource="*")], management_account=True), "Allow"),
    ]
    for n, kw, want in t:
        got = evaluate("s3:GetObject", obj, **kw); assert got[0] == want, (n, got); print(f"{n:40s} {got}")
    print("ext self-test ok")
