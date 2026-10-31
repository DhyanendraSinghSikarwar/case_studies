# TOY: what an engineer can produce for governance: a system record with a completeness check, and a subject-request tool.
# The mapping of fields to NIST AI RMF functions below is MY illustrative grouping, not an official crosswalk.
import hashlib, json
REQUIRED = {  # field -> RMF function it mainly serves (illustrative)
 "owner": "Govern", "intended_use": "Map", "out_of_scope_use": "Map", "data_categories": "Map", "model_and_version": "Map",
 "risk_review_date": "Govern", "eval_summary": "Measure", "red_team_result": "Measure", "monitoring_plan": "Manage",
 "incident_contact": "Manage", "retention_days": "Govern", "human_oversight": "Manage"}
record = {"owner": "support-platform", "intended_use": "draft replies to customer emails", "out_of_scope_use": "legal or medical advice",
          "data_categories": ["name", "email", "order history"], "model_and_version": "provider-model-dated-snapshot (placeholder)",
          "eval_summary": "golden set v3, see eval report", "monitoring_plan": "latency, cost, refusal rate, sampled judge",
          "retention_days": 30}
missing = [f for f in REQUIRED if f not in record]
by_fn = {}
for f in REQUIRED: by_fn.setdefault(REQUIRED[f], [0, 0])[1] += 1; by_fn[REQUIRED[f]][0] += f in record
print("missing fields:", missing)
print("completeness by function (present/total):", {k: tuple(v) for k, v in by_fn.items()})

# conversation store: content is deletable, audit metadata is kept without the content
store = [{"id": i, "subject": s, "content": f"text of conversation {i}", "ts": 100 + i} for i, s in enumerate(["u1", "u2", "u1", "u3"])]
audit = []
def log(event, **kw): audit.append({"event": event, **kw})
def export_for(subject):
    rows = [r for r in store if r["subject"] == subject]; log("export", subject_hash=hashlib.sha256(subject.encode()).hexdigest()[:8], n=len(rows)); return rows
def erase_for(subject):
    n = 0
    for r in store:
        if r["subject"] == subject and r["content"] is not None: r["content"] = None; r["erased"] = True; n += 1
    log("erase", subject_hash=hashlib.sha256(subject.encode()).hexdigest()[:8], n=n); return n
print("export u1 returns", len(export_for("u1")), "conversations")
print("erase u1 removed content from", erase_for("u1"), "records; second erase removes", erase_for("u1"))
print("remaining content for u1:", [r["content"] for r in store if r["subject"] == "u1"], "| audit trail:", json.dumps(audit))
print("limit shown: backups, trace stores, provider-side logs and derived data (embeddings, eval sets) are NOT touched by this toy.")
