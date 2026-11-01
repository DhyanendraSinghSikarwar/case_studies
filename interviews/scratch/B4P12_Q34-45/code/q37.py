# Q37: threat-model / controls table; fails if any asset lacks evidence.
T = [
 ("raw bureau + application data", "exfiltration / over-broad access", "zone isolation, role-per-job, encryption with customer key, residency tag", "access review export + KMS key policy"),
 ("feature store", "training-serving skew, unauthorised read", "single feature definitions, per-feature ACL", "feature registry commit log"),
 ("training pipeline", "untracked data or code change", "data hash + git sha + seed logged per run", "run record (Part 4 Q25 style)"),
 ("validation report", "self-approval by developer", "independent validator role, separate repo and sign-off", "signed validation memo with reviewer id"),
 ("model registry", "unapproved model promoted", "stage transitions need 2 approvers, immutable versions", "hash-chained promotion log"),
 ("serving endpoint", "stolen model via API, unauthorised caller", "authn, rate limits, private network", "gateway access logs"),
 ("decision log", "tampering, missing reason codes", "append-only, hash chain, reason codes stored", "chain verification output"),
 ("decommissioned model", "zombie endpoint keeps scoring", "retire checklist, endpoint deletion, key revoke", "CMDB retirement ticket"),
]
def check(rows):
    bad = [r[0] for r in rows if not (r[2].strip() and r[3].strip())]
    if bad: raise SystemExit("FAIL: assets without control/evidence: " + ", ".join(bad))
    return len(rows)
print("rows ok:", check(T))
for r in T: print(f"- {r[0]:30s} | {r[1]:38s} | evidence: {r[3]}")
try: check(T + [("shadow notebook copy", "PII on laptop", "", "")])
except SystemExit as e: print(e)
# examiner probes as queries over a tiny invented store
import hashlib, json
def h(prev, rec): return hashlib.sha256((prev + json.dumps(rec, sort_keys=True)).encode()).hexdigest()
log, prev = [], "0"
for rec in [{"who": "ana", "act": "promote", "model": "pd_v3"}, {"who": "ravi", "act": "approve", "model": "pd_v3"}, {"who": "ana", "act": "promote", "model": "pd_v4"}]:
    prev = h(prev, rec); log.append((rec, prev))
def verify(log):
    p = "0"
    for rec, hh in log:
        p = h(p, rec)
        if p != hh: return False
    return True
print("probe 2 (who changed prod): ", [r["who"] + ":" + r["act"] + ":" + r["model"] for r, _ in log if r["act"] == "promote"], "chain valid:", verify(log))
log[0][0]["who"] = "mallory"; print("after tamper, chain valid:", verify(log))
reasons = {"bureau_score": -0.8, "income_to_emi": -0.5, "age_of_credit": 0.1}
print("probe 1 (reason codes, top 2 negative):", sorted(reasons, key=reasons.get)[:2])
