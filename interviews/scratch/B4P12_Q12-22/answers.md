### Q12 ⭐⭐⭐ 🟡 [Least privilege review] An ML platform role is allowed s3:*, sagemaker:*, kms:* and iam:PassRole on * (invented). Write the tightened policy set for a training job role, a serving role and a CI deploy role, and explain how you find what is really used (access-advisor style reports, CloudTrail-style logs, policy simulation) without breaking jobs. Reuse the IAM evaluator sketch in scratch/B4P10_wavea/iam_eval_sketch.py to show allow, explicit-deny and missing-allow cases, reference Part 10 Q7, Part 10 Q8 and Part 10 Q30, and list what the sketch does not model.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | OWASP Top 10 for LLM Applications 2025 summaries (opensourcesecurity substack, Trend Micro, HackerOne, Bright Security, Coralogix; search snippets only, not opened): supply chain moved to LLM03, data and model poisoning LLM04, model theft folded out of the standalone list; no source on classic ML model-extraction attacks surfaced, so extraction questions rest on general knowledge, hedged | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Give each role only the actions and resource ARNs its job needs, pin `iam:PassRole` to one named role and one service, and find the real usage from access reports and logs, then replay that usage against the new policy before you remove the old one.

**Then explain:**
- Three roles, three small policies. Training reads `train/` and writes `models/`. Serving only reads `models/`. The CI deploy role creates and updates endpoints and may pass only the serving role to SageMaker (Part 10 Q8 has the training policy in full).
- `iam:PassRole` on `*` is the dangerous one. Whoever can pass any role can hand a job a more powerful role. Pin the Resource to the serving role ARN and add `iam:PassedToService` as a condition. The evaluator below shows the old role passing an admin role and the new CI role failing to.
- Finding real usage without breaking jobs: pull the last-accessed or access-advisor style report, read CloudTrail-style logs for the role, then run policy simulation. Do it over a full cycle (a monthly job, a quarterly retrain), otherwise you cut a rarely used action. Check current docs for how long these reports look back and which services they cover.
- Roll out in steps: add the new policy next to the old one, add alarms on AccessDenied events, then detach the wildcard. Keep a break-glass path. Evaluation order and the three guard rails (boundary, SCP, session policy) are Part 10 Q7 and Part 10 Q30.
- Failure modes: a missing `kms:Decrypt` shows up as an S3 access error; `ListBucket` needs the bucket ARN, not the object ARN; a wildcard `Resource` copied from an example silently re-opens everything.
- What the sketch does NOT model: NotAction and NotResource, policy variables, resource policies beyond the simple cases, KMS grants and key policies, VPC endpoint policies, service-linked roles, real condition operators beyond StringEquals, StringLike and Bool, and the exact cross-account rules. It is a teaching sketch, not the real evaluator; use the provider's simulator for sign-off.

**Example:** The old role allows `s3:*`, `sagemaker:*`, `kms:*` and PassRole on `*`. Logs show the training role used 5 actions, serving 2, CI 3. The new policies cover exactly those. A serving job trying to read `train/` is now an implicit deny (missing allow). Any delete on `models/` is an explicit deny, and an explicit deny wins even over an allow-everything policy.

**Code:** (the evaluator is a copy of `scratch/B4P10_wavea/iam_eval_sketch.py`, unmodified; policies and names are invented)
```python
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
```

**Output (my run):** (python3 -I, Python in the b10p10 venv; no cloud, no credentials)
```
train reads train data                           Allow identity or resource policy allows (same account)
train writes model                               Allow identity or resource policy allows (same account)
train reads models (missing allow)               Deny  implicit deny: nothing allows
train deletes model (explicit deny)              Deny  explicit deny
train over plain http (explicit deny)            Deny  explicit deny
serve reads model                                Allow identity or resource policy allows (same account)
serve reads train data (missing allow)           Deny  implicit deny: nothing allows
CI passes serving role to SageMaker              Allow identity or resource policy allows (same account)
CI passes admin role (missing allow)             Deny  implicit deny: nothing allows
CI passes serving role to ec2 (condition fails)  Deny  implicit deny: nothing allows
OLD role passes admin role                       Allow identity or resource policy allows (same account)
11 cases pass
old grant families: s3:*, sagemaker:*, kms:*, iam:PassRole on * (every action in each family)
ci-role: used 3 distinct actions -> ['iam:PassRole', 'sagemaker:CreateModel', 'sagemaker:UpdateEndpoint']
serve-role: used 2 distinct actions -> ['kms:Decrypt', 's3:GetObject']
train-role: used 5 distinct actions -> ['kms:Decrypt', 'kms:GenerateDataKey', 's3:GetObject', 's3:ListBucket', 's3:PutObject']
replay: every observed action is still allowed by the candidate policies
```

**Follow-ups:**
- *A job fails after tightening. First move?* Read the AccessDenied event: it names the action and resource. Add exactly that, not a wildcard. Check KMS and the bucket-versus-object ARN first.
- *Why not just use a permissions boundary?* A boundary only caps. It grants nothing. It is a guard rail for delegated role creation, not a substitute for a tight identity policy.
- *How do you keep it tight over time?* Policy as code in git, review, a scheduled access-report job that flags unused actions, and a CI check that fails on `Action: *` or `PassRole` on `*`.

**Common mistakes:**
- Cutting actions based on a one-week log when a job runs monthly.
- Writing `"Resource": "*"` for PassRole "just for CI".
- Forgetting the KMS permission and blaming S3.
- Trusting the sketch for sign-off instead of the real simulator.

---

### Q13 ⭐⭐⭐ 🔴 [Reliability and DR] Define RTO and RPO for four ML assets (feature store, model registry, serving endpoint, training pipeline) and choose backup and recovery for each at a payments-style business (invented: serving must recover in 15 minutes, registry in 4 hours, training in 2 days). Cover backups versus replication, what is hard to rebuild (labels, feature history, signed models), restore drills and what a region failure does to dependencies. Reference Part 7 Q12 (rollback), Part 6 Q38 (graceful shutdown) and Part 11 Q33. Compute availability of a three-dependency serial chain versus one with a cached fallback from invented figures.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Job-posting and community patterns for MLOps, platform and ML-engineering roles at Indian GCCs, product companies and IT-services firms and at global product companies; inferred from search snippets about system-design and FinOps rounds, not from a verified company report | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Set RTO and RPO per asset from the business impact, pick the cheapest recovery that meets each (warm replica for serving, backup for the registry, rebuild for training), and prove it with restore drills, because an untested backup is a hope.

**Then explain:**
- Definitions: RTO is how long you can be down. RPO is how much data you can lose. Invented targets: serving 15 min, registry 4 h, training 2 days.
- Backup versus replication: replication copies mistakes too (a bad delete or a corrupt model replicates in seconds). Backups give you point-in-time. Use both for the registry: versioned artefact bucket plus a metadata DB backup.
- Per asset: *serving endpoint*: warm capacity in a second Region, image by digest, model artefact replicated; rollback as in Part 7 Q12, graceful shutdown as in Part 6 Q38. *Feature store*: online store can be rebuilt from the stream or replicated; offline tables versioned. *Registry*: backups, replicated artefact store, signed models with keys held outside the Region. *Training*: code and configs in git, rebuild elsewhere, restore the data snapshot.
- Hard to rebuild: labels (chargebacks, human reviews), feature history with point-in-time correctness, signing keys and the trust root, and the exact training data snapshot. Protect these first.
- A region failure takes down the dependencies together: the identity service, the registry, the container registry, the secret store, the DNS. Independence in the availability maths is a best case. Cross-cloud sits in Part 11 Q33.
- Restore drills: a scheduled game day that restores the registry and one model to a clean account and serves one request. Record the real time against the RTO. Failure mode: restore works but the signing key or secrets are missing.

**Example:** Three serial dependencies at 0.999, 0.995, 0.999 give 0.993011, about 302 minutes down in 30 days. If the weakest (0.995) has a cache fallback that covers 90 percent of its outages, its effective value is 0.995 + 0.005 x 0.9 = 0.9995 and the chain is 0.997502, about 108 minutes.

**Code:**
```python
"""Q13: RTO/RPO table checks and serial-chain availability (invented figures)."""
assets = {  # asset: (RTO min, RPO min, target RTO min, strategy)
 "serving endpoint":   (15, 5, 15, "second Region warm, image digest + model artefact replicated"),
 "feature store":      (60, 5, 60, "online store replicated or rebuilt from stream; offline from versioned tables"),
 "model registry":     (240, 60, 240, "metadata DB backup + artefact bucket versioning/replication"),
 "training pipeline":  (2880, 1440, 2880, "code in git, configs as code, rebuild in other Region; data snapshot restore"),
}
print(f"{'asset':18s}{'RTO(min)':>9s}{'RPO(min)':>9s}  meets target")
for k, (rto, rpo, tgt, s) in assets.items():
    assert rto <= tgt
    print(f"{k:18s}{rto:9d}{rpo:9d}  {rto <= tgt}")

MIN_MONTH = 30 * 24 * 60
def down(a): return (1 - a) * MIN_MONTH
feature, registry_cfg, model_store = 0.999, 0.995, 0.999  # invented dependency availabilities
serial = feature * registry_cfg * model_store
print(f"\nserial chain A*B*C = {feature}*{registry_cfg}*{model_store} = {serial:.6f}  (~{down(serial):.0f} min down per 30 days)")
# dependency B (the weakest) gets a cached fallback that works 90% of the time B is down
cov = 0.90
b_eff = registry_cfg + (1 - registry_cfg) * cov
with_fb = feature * b_eff * model_store
print(f"B with cached fallback covering {cov:.0%} of its outages: {b_eff:.5f}")
print(f"chain with fallback = {with_fb:.6f}  (~{down(with_fb):.0f} min down per 30 days)")
assert with_fb > serial
# hand check: B down 0.5% of time -> 0.005*0.1 = 0.0005 left uncovered
assert abs((1 - b_eff) - 0.0005) < 1e-12
# a region failure takes out everything in that region at once: independence assumption breaks
print("\nIf all three share one Region and it fails, they fail together: the product above is a best case.")
```

**Output (my run):** (python3 -I; the table values are invented design targets, the code only checks they meet the stated targets)
```
asset              RTO(min) RPO(min)  meets target
serving endpoint         15        5  True
feature store            60        5  True
model registry          240       60  True
training pipeline      2880     1440  True

serial chain A*B*C = 0.999*0.995*0.999 = 0.993011  (~302 min down per 30 days)
B with cached fallback covering 90% of its outages: 0.99950
chain with fallback = 0.997502  (~108 min down per 30 days)

If all three share one Region and it fails, they fail together: the product above is a best case.
```

**Follow-ups:**
- *Why not multi-Region active-active for everything?* Cost and complexity. Only the serving path needs it at 15 minutes; training can wait two days.
- *What does a restore drill prove?* The time, the missing keys, the stale runbook. It is the only evidence for your RTO.
- *Is 0.997502 the real number?* No. It assumes independent failures. A shared Region or shared identity service breaks that.

**Common mistakes:**
- Treating replication as backup.
- Backing up the model but not the labels or the signing key.
- Never running a restore.
- Quoting an availability product without noting the independence assumption.

---

### Q14 ⭐⭐ 🟡 [Set D, Q1 of 4, 6 min, 10 pts] Demand forecasting platform, clarify first. A retailer with 3,000 stores and 40,000 SKUs (invented) wants daily forecasts 14 days ahead for replenishment. Ask about the hierarchy (store, SKU, region), intermittent items, promotions and holidays as known-future inputs, cold-start SKUs, the cost of stock-out versus overstock and how forecasts are consumed. Compute series count and rows per day for a 14-day horizon, and say why one global model, per-group models or per-series models change the platform cost.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Job-posting and community patterns for MLOps, platform and ML-engineering roles at Indian GCCs, product companies and IT-services firms and at global product companies; inferred from search snippets about system-design and FinOps rounds, not from a verified company report
**Say this first (1 line):** Before any design I ask about the hierarchy, intermittent items, known-future inputs, cold start, the cost of stock-out versus overstock and how planners consume forecasts, and then I size it: 120 million store-SKU cells, a share of them actually ranged, 14 rows per series per day.

**Then explain:**
- Clarifying questions: hierarchy (store, SKU, region) and the level where decisions are made; intermittent items with many zero days; promotions and holidays are known-future inputs, so the platform must supply a future calendar; new SKUs with no history; stock-out cost versus overstock cost (decides a quantile target, not just a mean); who consumes the forecast and how (replenishment system, planner screen).
- Sizing: 3,000 x 40,000 = 120,000,000 cells. Not every store carries every SKU. At an invented 10 percent ranged: 12,000,000 series and 168,000,000 forecast rows a day at 14 days. At 25 percent: 30,000,000 series and 420,000,000 rows.
- Platform cost shape: one global model has the fewest things to run, version and monitor; per-group (invented 12 regions x 4 item classes = 48 models) is a middle path; per-series means 12 million models, with per-model overhead (start, load, register, monitor) dominating. It also kills registry and monitoring tooling.
- Failure modes: rows balloon downstream (storage, join, publish time); cold-start items need a fallback from similar items; a feed delay silently forecasts from stale data (Part 8 Q23).
- Scoring note (10 pts, 6 min; rubric from the part header): about 3 points for clarifying questions and stated assumptions, 3 for correct sizing (120M cells, rows per day), 2 for failure modes and the cost shape, 1 for the runnable check, 1 for a clear 60-second summary. Full marks need the ranged-share assumption said out loud; partial if you multiply 120M by 14 and ignore assortment.

**Example:** 3,000 x 40,000 = 120M. At 10 percent ranged that is 12M series. 12M x 14 = 168M rows per day. With 5.0 fixed units per fit and 0.01 units per series of work (invented), the global model costs about 120,005 units and per-series costs about 60,120,000, roughly 500 times more, almost all fixed overhead.

**Code:**
```python
"""Q14: series count, rows per day and platform cost shape for three modelling choices (abstract units)."""
stores, skus, horizon = 3000, 40000, 14
cells = stores * skus
print("store x SKU cells:", f"{cells:,}")
for ranged in (0.10, 0.25):   # invented share of SKUs actually ranged (sold) in a given store
    series = int(cells * ranged)
    rows = series * horizon
    print(f"ranged {ranged:.0%}: series={series:,}  forecast rows/day (14 days)={rows:,}")
assert 3000 * 40000 == 120_000_000
series = int(cells * 0.10)

# platform cost shape, abstract units. Invented: each model fit has a fixed overhead (load data, start, register)
FIXED, PER_SERIES_COMPUTE = 5.0, 0.01           # units per fit; units per series of actual learning work
regions, classes = 12, 4                        # invented: per-group model = region x item class
options = {
  "one global model":      dict(models=1,                  series_fitted=series),
  "per-group models":      dict(models=regions * classes,  series_fitted=series),
  "per-series models":     dict(models=series,             series_fitted=series),
}
print(f"\n{'option':20s}{'models to manage':>18s}{'fit cost (units)':>20s}")
base = None
for k, v in options.items():
    cost = v["models"] * FIXED + v["series_fitted"] * PER_SERIES_COMPUTE
    base = base or cost
    print(f"{k:20s}{v['models']:18,d}{cost:20,.0f}  x{cost/base:.1f} vs global")
```

**Output (my run):** (python3 -I; abstract units, not prices)
```
store x SKU cells: 120,000,000
ranged 10%: series=12,000,000  forecast rows/day (14 days)=168,000,000
ranged 25%: series=30,000,000  forecast rows/day (14 days)=420,000,000

option                models to manage    fit cost (units)
one global model                     1             120,005  x1.0 vs global
per-group models                    48             120,240  x1.0 vs global
per-series models           12,000,000          60,120,000  x501.0 vs global
```

**Follow-ups:**
- *Why a quantile and not just a mean?* If a stock-out costs more than overstock, plan on a higher quantile. That is a business input from Book 6.
- *When would per-series models be justified?* Few, high-value series where a global model is clearly worse on a backtest. Never as the default at this scale.
- *What do you do for a new SKU?* Borrow from a similar item group until history exists, and flag it as low confidence.

**Common mistakes:**
- Assuming every store carries every SKU.
- Ignoring future inputs like promotions.
- Choosing per-series models without counting the models to operate.

---

### Q15 ⭐⭐ 🟡 [Set D, Q2 of 4, 10 min, 20 pts] Forecasting pipeline and cost. Design the nightly batch (data freshness check, feature build, training or rescoring, backtest, publish, override handling) for the Set D Q1 numbers. Reference Part 5 Q9 (training DAG), Part 5 Q39 (cost-aware runs) and Part 6 Q27 (batch inference design). With invented per-series training seconds, compute wall-clock and relative cost for full retrain nightly versus retrain weekly and rescore nightly, and state what accuracy evidence would justify each. Simulate the schedule and find the parallelism that meets a 4-hour window.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Run the nightly batch as freshness check, feature build, score, backtest check, publish with overrides preserved, shard it across workers, and retrain weekly with nightly rescore unless backtests show nightly retraining pays for its compute.

**Then explain:**
- Steps and gates: freshness check (Part 8 Q23 style: stop or flag stale feeds), feature build, train or rescore, backtest on the latest holdout window, publish to a staged table then rename (idempotent, as in Part 6 Q27), apply or carry over planner overrides, notify. The DAG shape is Part 5 Q9. Cost-aware runs (pinned inputs, ephemeral compute, scale down after) are Part 5 Q39.
- Compute trade: with invented 0.02 s per series to train and 0.001 s to score, full nightly retrain costs about 83 core-hours a night versus about 17 to rescore. Weekly retrain plus six rescores is about 183 core-hours a week against 583: relative 0.31.
- Evidence that justifies each: nightly retrain only if a backtest shows rolling-origin error clearly improves with daily refits (fast-moving promo data); weekly retrain if error is flat across the week. Decide on error by item class, not on one average.
- Window: 12 million series cut into 2,400 shards of uneven size. A longest-first scheduler needs 23 workers for full retrain and 5 for rescore to finish inside 4 hours including 0.3 h of fixed steps.
- Failure modes: one giant shard becomes the critical path (skew), a half-written output (use temp then rename), a late feed forecasting from yesterday, overrides lost when a rerun overwrites the table.
- Scoring note (20 pts, 10 min): about 6 for a pipeline that covers the named steps with assumptions, 6 for arithmetic that meets the 4 h window (check the worker count), 4 for failure modes and cost, 2 for the runnable check, 2 for the spoken summary. Partial: a DAG with no window arithmetic, or a worker count that ignores skew.

**Example:** Total work is 12M series x 0.021 s = 252,000 core-seconds = 70 core-hours, plus 2,400 shards x 20 s start-up = 13.3 core-hours: about 83 core-hours. Divided by 23 workers is 3.6 h, plus 0.3 h fixed steps, inside the 4 h window.

**Code:**
```python
"""Q15: nightly batch window simulation: full retrain nightly vs weekly retrain + nightly rescore (abstract units, seeded)."""
import random, heapq
random.seed(15)
SERIES = 12_000_000          # from Q14: 10 percent of 120M cells (invented)
TRAIN_S, SCORE_S = 0.02, 0.001   # invented seconds of one core per series
SHARDS = 2400
WINDOW_H = 4.0
FIXED_S = 20                 # per-shard startup: load data, model, write output (invented)
# shard sizes vary (big stores / SKU groups): seeded lognormal, rescaled to total
raw = [random.lognormvariate(0, 0.5) for _ in range(SHARDS)]
sizes = [int(SERIES * r / sum(raw)) for r in raw]

def makespan(per_series_s, workers):
    """Longest-processing-time-first onto `workers` identical cores. Returns hours."""
    jobs = sorted((FIXED_S + s * per_series_s for s in sizes), reverse=True)
    heap = [0.0] * workers
    for j in jobs:
        t = heapq.heappop(heap); heapq.heappush(heap, t + j)
    return max(heap) / 3600
def core_hours(per_series_s): return sum(FIXED_S + s * per_series_s for s in sizes) / 3600

pre = 0.30   # invented: freshness check + feature build + backtest + publish take 0.30 h of the window
print("shards:", SHARDS, " largest/smallest shard ratio:", round(max(sizes) / min(sizes), 1))
for name, per in (("full retrain + score nightly", TRAIN_S + SCORE_S), ("rescore only (weekly retrain)", SCORE_S)):
    ch = core_hours(per)
    need = None
    for w in range(1, 5000):
        if makespan(per, w) + pre <= WINDOW_H: need = w; break
    print(f"{name:32s} core-hours={ch:8.1f}  min workers for {WINDOW_H}h window (incl {pre}h fixed steps)={need}  makespan={makespan(per, need) + pre:.2f}h")
    if per == TRAIN_S + SCORE_S: full_ch = ch
    else: resc_ch = ch
week_full = 7 * full_ch
week_mix = 1 * (full_ch) + 6 * resc_ch
print(f"\nweekly core-hours: nightly full={week_full:.1f}  weekly retrain + nightly rescore={week_mix:.1f}  relative={week_mix/week_full:.2f}")
assert week_mix < week_full
```

**Output (my run):** (python3 -I, seeded; the times and unit costs are invented inputs, not measurements)
```
shards: 2400  largest/smallest shard ratio: 31.8
full retrain + score nightly     core-hours=    83.3  min workers for 4.0h window (incl 0.3h fixed steps)=23  makespan=3.93h
rescore only (weekly retrain)    core-hours=    16.7  min workers for 4.0h window (incl 0.3h fixed steps)=5  makespan=3.63h

weekly core-hours: nightly full=583.3  weekly retrain + nightly rescore=183.3  relative=0.31
```

**Follow-ups:**
- *Why not just add workers?* Past a point the biggest shard and fixed steps set the floor. Split big shards.
- *Rescore uses a week-old model: is that safe?* Only if the backtest shows error stays flat. Monitor error by class (Q22) and trigger an early retrain when it drifts.
- *What if the feed is late?* Do not silently forecast. Flag, use the last good features with a stale marker, tell planners.

**Common mistakes:**
- One huge job with no shards or retry.
- Overwriting outputs in place with no temp table.
- Retraining nightly because it feels safer.
- Dropping planner overrides on rerun.

---

### Q16 ⭐⭐ 🟡 [Set L, Q1 of 4, 6 min, 10 pts] LLM-serving boundary, clarify first. A support-assistant team wants a hosted foundation model behind an internal API for 5,000 employees (invented). Say what the MLOps platform owns (identity, network path, quota, logging with redaction, versions, cost attribution, fallbacks) and what Book 2 owns (prompting, retrieval, evaluation of answers). Reference Part 11 Q31 and Part 6 Q34. Write the ownership table as YAML and validate that every responsibility has exactly one owner.
**Asked at:** LLM and GPU inference cost guides (Cast AI, Morph, DataCamp, machinelearningatscale.com, an alpeshnakrani.com playbook; search snippets only, not opened; vendor-authored figures such as utilisation percentages are one vendor's data and are NOT reused here); practitioner blogs, not interview reports | ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** The platform owns the plumbing around the model call (who may call it, over which network path, how much, what is logged, which version, who pays, what happens when it fails), and Book 2 owns what is said to the model and how answers are judged.

**Then explain:**
- Platform owns: identity and single sign-on, private network path, quota and rate limits, request logging with redaction (Part 8 Q42 boundary), provider model version pinning, cost attribution by team, timeouts and fallbacks. Part 11 Q31 and Part 6 Q34 cover the cloud boundary and the serving side.
- Book 2 owns: prompt design, retrieval and grounding, answer-quality evaluation, and the in-app prompt-injection defences.
- Clarifying questions: data classes in prompts (customer data?), which provider and Region, latency target, peak requests for 5,000 employees, who approves a model version change, what the logs may keep.
- One owner per item is a rule you can check. Two owners means nobody owns it; zero owners is a gap. Failure mode: "both" for logging, then PII sits in logs for a year.
- Scoring note (10 pts, 6 min): about 3 for clarifying questions and assumptions, 3 for a correct split with every item owned once, 2 for failure modes (an item nobody owns, logs with PII), 1 for the runnable validator, 1 for a 60-second summary. Partial: a good list with shared ownership on logging or cost.

**Example:** `prompt_design` listed twice (once platform, once app) is rejected by the validator. Deleting `identity_and_sso` is rejected as a missing required item. An owner named `vendor` is rejected as unknown.

**Code:** (YAML table, then the validator; pyyaml and pydantic)
```yaml
# Who owns what at the hosted-LLM boundary (invented team names)
owners: [platform, book2_app]
responsibilities:
  - {name: identity_and_sso,         owner: platform}
  - {name: private_network_path,     owner: platform}
  - {name: quota_and_rate_limits,    owner: platform}
  - {name: request_logging_redaction, owner: platform}
  - {name: provider_model_version_pin, owner: platform}
  - {name: cost_attribution_by_team, owner: platform}
  - {name: fallback_and_timeouts,    owner: platform}
  - {name: prompt_design,            owner: book2_app}
  - {name: retrieval_and_grounding,  owner: book2_app}
  - {name: answer_quality_evaluation, owner: book2_app}
  - {name: prompt_injection_defence_in_app, owner: book2_app}
```

```python
"""Q16: validate the ownership table: every responsibility has exactly one owner, from a known set."""
import sys, copy, yaml
from collections import Counter
from pydantic import BaseModel, ValidationError, model_validator
here = sys.argv[1]
class R(BaseModel):
    name: str
    owner: str
class Table(BaseModel):
    owners: list[str]
    responsibilities: list[R]
    @model_validator(mode="after")
    def check(self):
        c = Counter(r.name for r in self.responsibilities)
        dup = [n for n, k in c.items() if k > 1]
        if dup: raise ValueError(f"responsibility listed more than once (two owners?): {dup}")
        bad = [r.name for r in self.responsibilities if r.owner not in self.owners]
        if bad: raise ValueError(f"unknown owner for: {bad}")
        need = {"identity_and_sso", "private_network_path", "quota_and_rate_limits", "request_logging_redaction",
                "provider_model_version_pin", "cost_attribution_by_team", "fallback_and_timeouts", "prompt_design",
                "retrieval_and_grounding", "answer_quality_evaluation"}
        missing = need - set(c)
        if missing: raise ValueError(f"required responsibility has no owner: {sorted(missing)}")
        return self
doc = yaml.safe_load(open(here))
t = Table(**doc)
print("good table OK:", len(t.responsibilities), "responsibilities,", dict(Counter(r.owner for r in t.responsibilities)))
for label, mut in [
    ("two owners for one item", lambda d: d["responsibilities"].append({"name": "prompt_design", "owner": "platform"})),
    ("item nobody owns", lambda d: d["responsibilities"].pop(0)),
    ("unknown owner", lambda d: d["responsibilities"][0].update(owner="vendor")),
]:
    d = copy.deepcopy(doc); mut(d)
    try: Table(**d); print(label, "-> NOT caught"); sys.exit(1)
    except ValidationError as e: print(label, "-> rejected:", e.errors()[0]["msg"].replace("Value error, ", ""))
```

**Output (my run):** (python3 -I q16_validate.py q16_ownership.yaml; pyyaml and pydantic 2.14.1)
```
good table OK: 11 responsibilities, {'platform': 7, 'book2_app': 4}
two owners for one item -> rejected: responsibility listed more than once (two owners?): ['prompt_design']
item nobody owns -> rejected: required responsibility has no owner: ['identity_and_sso']
unknown owner -> rejected: unknown owner for: ['identity_and_sso']
```

**Follow-ups:**
- *Who owns cost?* The platform measures and attributes by team key; each team owns its own usage and prompts.
- *Who owns a bad answer?* The app team (Book 2). The platform owns an outage or a leak.
- *What if the provider changes the model version?* Pin the version, test before moving, and keep a rollback route in the gateway.

**Common mistakes:**
- Blurring platform and app ownership so both skip logging redaction.
- Leaving "who approves a version change" unowned.
- Letting every team hold its own provider key.

---

### Q17 ⭐⭐ 🟡 [Set L, Q2 of 4, 10 min, 20 pts] LLM gateway design at the platform level. Design a gateway in front of one or more model providers: per-team keys and budgets, rate limits, request and response logging with PII redaction, timeouts with provider fallback, caching of exact repeats, and versioned routing. Do not explain model internals (Book 2). With invented token counts per request and request rates, compute daily token volume per team, apply a budget cap in Python and show what the gateway does at 80 and 100 percent. Reference Part 8 Q29 (privacy and prediction logging) and Part 8 Q42.
**Asked at:** LLM and GPU inference cost guides (Cast AI, Morph, DataCamp, machinelearningatscale.com, an alpeshnakrani.com playbook; search snippets only, not opened; vendor-authored figures such as utilisation percentages are one vendor's data and are NOT reused here); practitioner blogs, not interview reports | ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Put one gateway in front of the providers that authenticates teams, gives each a key and a daily token budget, rate-limits, redacts and logs, caches exact repeats, times out and falls back, and routes by version, and let the budget cap warn at 80 percent and block at 100.

**Then explain:**
- Per-team keys and budgets so spend is attributed and one team cannot starve the others. Rate limits protect the provider quota. Budget caps protect money.
- Logging with PII redaction before the log is written (Part 8 Q29 for the privacy tension, Part 8 Q42 for what to monitor). Redact at the gateway, not later.
- Timeouts, then fallback to a second provider or smaller model; caching of exact repeats (same team, same prompt hash); versioned routing so you can pin, canary and roll back a provider model version.
- Not here: prompts, retrieval, model internals (Book 2).
- Daily volume: requests x (input + output tokens). Support: 9,000 x 1,150 = 10.35M tokens against an 11M budget. Analytics runs at 126 percent of its budget.
- Failure modes: a cache that crosses team boundaries leaks data; a retry storm during an outage; a hard block at 100 percent on a critical team with no override path; logs that store raw prompts.
- Scoring note (20 pts, 10 min): about 6 for a gateway design covering keys, budgets, limits, logging, fallback, cache and routing with stated assumptions, 6 for correct token arithmetic and cap behaviour at 80 and 100 percent, 4 for failure modes (cross-team cache, retry storms, PII), 2 for the runnable check, 2 for a 60-second summary.

**Example:** Analytics plans 1,200 requests of 2,100 tokens: 2.52M against a 2.0M budget. In the run it was alerted when it crossed 80 percent (1.6M), then blocked with a 429 near 2.0M, overshooting by one request at most.

**Code:** (invented rates and budgets; no network, no real provider)
```python
"""Q17: gateway budget cap, exact-repeat cache, PII redaction and provider fallback (invented numbers, no network)."""
import random, re, hashlib
random.seed(17)
TEAMS = {  # team: (requests/day, avg input tokens, avg output tokens, daily token budget)
  "support":  (9000, 900, 250, 11_000_000),
  "hr-bot":   (2500, 700, 200, 3_000_000),
  "analytics": (1200, 1500, 600, 2_000_000),
}
print("hand-check daily token volume = requests * (in+out)")
for t, (n, i, o, b) in TEAMS.items():
    vol = n * (i + o)
    print(f"{t:10s} {n:6d} x {i+o:5d} = {vol:>10,d} tokens/day  budget {b:>10,d}  ratio {vol/b:.0%}")
assert 9000 * 1150 == 10_350_000

PII = [(re.compile(r"\b\d{10}\b"), "<PHONE>"), (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "<EMAIL>"), (re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"), "<PAN>")]
def redact(s):
    for rx, tag in PII: s = rx.sub(tag, s)
    return s

class Gateway:
    def __init__(self, budgets, primary_ok=lambda: True):
        self.budget, self.used, self.cache, self.log, self.alerted = dict(budgets), {t: 0 for t in budgets}, {}, [], set()
        self.primary_ok = primary_ok
        self.served = {"primary": 0, "fallback": 0, "cache": 0, "blocked": 0}
    def call(self, team, prompt, in_tok, out_tok):
        key = (team, hashlib.sha256(prompt.encode()).hexdigest())
        if key in self.cache:                       # exact repeat: no provider tokens spent
            self.served["cache"] += 1; return "cache"
        pct = self.used[team] / self.budget[team]
        if pct >= 1.0:
            self.served["blocked"] += 1; return "blocked(429 budget)"
        route = "primary" if self.primary_ok() else "fallback"   # timeout / outage -> smaller model
        self.used[team] += in_tok + out_tok
        if self.used[team] >= 0.8 * self.budget[team] and team not in self.alerted:
            self.alerted.add(team); self.log.append(f"ALERT 80% budget: {team} at request #{sum(self.served.values())+1}")
        self.served[route] += 1
        self.cache[key] = True
        self.log.append(redact(f"{team} {route} {prompt[:40]}"))
        return route

# 1) one day of traffic with the invented rates (analytics runs hot: 1.3x its plan)
gw = Gateway({t: v[3] for t, v in TEAMS.items()})
reqs = []
for t, (n, i, o, b) in TEAMS.items():
    n = int(n * (1.3 if t == "analytics" else 1.0))
    for k in range(n):
        reqs.append((t, f"q{random.randint(0, 40000 if t=='support' else 10**6)} from {t}", int(random.gauss(i, i*0.2)), int(random.gauss(o, o*0.2))))
random.shuffle(reqs)
first100 = {}
for t, p, i, o in reqs:
    r = gw.call(t, p, i, o)
    if r.startswith("blocked") and t not in first100: first100[t] = gw.served["blocked"]
print("\nserved:", gw.served)
for t in TEAMS: print(f"{t:10s} used {gw.used[t]:>11,d} / {gw.budget[t]:>11,d} = {gw.used[t]/gw.budget[t]:.0%}")
print("\n".join(l for l in gw.log if l.startswith("ALERT")))
assert gw.used["analytics"] <= gw.budget["analytics"] + 4000   # cap overshoots by at most one request
assert "analytics" in gw.alerted and "analytics" in first100   # alerted at 80%, blocked at 100%
print("redaction check:", redact("call 9876543210 or a.b@corp.in PAN ABCDE1234F"))
# 2) provider down for part of the day -> fallback route
down = {"on": False}
g2 = Gateway({"support": 10**9}, primary_ok=lambda: not down["on"])
for k in range(100):
    down["on"] = 40 <= k < 70
    g2.call("support", f"unique {k}", 900, 250)
print("outage drill (30 of 100 requests while primary down):", g2.served)
```

**Output (my run):** (python3 -I, seeded)
```
hand-check daily token volume = requests * (in+out)
support      9000 x  1150 = 10,350,000 tokens/day  budget 11,000,000  ratio 94%
hr-bot       2500 x   900 =  2,250,000 tokens/day  budget  3,000,000  ratio 75%
analytics    1200 x  2100 =  2,520,000 tokens/day  budget  2,000,000  ratio 126%

served: {'primary': 11460, 'fallback': 0, 'cache': 996, 'blocked': 604}
support    used   9,203,116 /  11,000,000 = 84%
hr-bot     used   2,252,140 /   3,000,000 = 75%
analytics  used   2,001,064 /   2,000,000 = 100%
ALERT 80% budget: analytics at request #6511
ALERT 80% budget: support at request #12435
redaction check: call <PHONE> or <EMAIL> PAN <PAN>
outage drill (30 of 100 requests while primary down): {'primary': 70, 'fallback': 30, 'cache': 0, 'blocked': 0}
```

**Follow-ups:**
- *What at 100 percent for a critical team?* A documented override with approver and expiry, or route to the cheaper model, not silent unlimited spend.
- *Why cache per team?* Prompts can hold team data; a shared cache is a cross-team leak.
- *Retries during a provider outage?* Bounded, with jitter and a circuit breaker (see Q23).

**Common mistakes:**
- One shared key for all teams.
- Redacting after logging.
- Budget enforced monthly only, so one bad day burns it.
- Caching with no team or version in the key.

---

### Q18 ⭐⭐ 🟡 [Set E, Q1 of 4, 6 min, 10 pts] Edge and on-device inference, clarify first. A field-inspection app must classify images on low-end phones with unreliable connectivity (invented). Ask what must run offline, the model size and latency limits, battery and memory, privacy, update cadence, how you learn about errors without uploading photos, and when a server fallback is allowed. Compare on-device, edge gateway and cloud inference in a table and compute the download time and storage cost of a 60 MB model update to 100,000 devices at an invented 2 Mbps average.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Job-posting and community patterns for MLOps, platform and ML-engineering roles at Indian GCCs, product companies and IT-services firms and at global product companies; inferred from search snippets about system-design and FinOps rounds, not from a verified company report
**Say this first (1 line):** Before choosing on-device, edge gateway or cloud I ask what must work offline, the size, latency, battery and memory limits, privacy, update cadence and how we learn about errors without uploading photos, then I size the update: 60 MB at 2 Mbps is 4 minutes ideal, 6,000 GB for the fleet.

**Then explain:**
- Questions: what must run with no signal; model size and latency limits on the lowest-end phone; battery and memory; are photos allowed to leave the device; how often the model changes; how errors reach us (aggregate counters, user-flagged samples with consent, on-device confidence histograms); when a server fallback is allowed.
- Comparison table below.
- Update arithmetic: 60 MB x 8 = 480 megabits; at 2 Mbps that is 240 s = 4.0 min ideal, 6.7 min at an invented 60 percent link efficiency. 60 MB x 100,000 = 6,000 GB per full rollout. Storage keeps a few versions only; egress dominates, so use delta patches, a CDN, Wi-Fi-only and charging-only downloads, resumable chunks.
- Failure modes: a drop mid-download without resume restarts (toy run: 1.38x bytes versus 1.01x resumable); a bad model reaching every phone at once (staged rollout, Q19); a model that outgrows low-end memory; no telemetry so errors are invisible.
- Scoring note (10 pts, 6 min): about 3 for clarifying questions and assumptions, 3 for the comparison and correct update arithmetic, 2 for failure modes and privacy, 1 for the runnable check, 1 for a 60-second summary.

| Option | Good for | Cost and limits | Privacy |
|---|---|---|---|
| On-device | offline, low latency, no per-call server cost | small model, update logistics, device variety | data stays on phone |
| Edge gateway (site box) | shared site, bigger model, some offline | hardware to run and patch | data stays on site |
| Cloud | biggest model, easy update | needs signal, per-call cost, latency | images leave device |

**Example:** 100,000 devices x 60 MB = 6,000 GB. A 25 percent delta patch is 1,500 GB and 1 minute a device at 2 Mbps. With invented 1 unit per GB sent and 1 per GB-month stored (not real prices), a full rollout is 6,000 units and five stored versions are 0.30 units a month.

**Code:**
```python
"""Q18: model update download time and storage/egress in abstract units (invented inputs)."""
MB, DEVICES, MBPS = 60, 100_000, 2
sec = MB * 8 / MBPS
print(f"one 60 MB update at 2 Mbps: {MB} MB * 8 / {MBPS} = {sec:.0f} s = {sec/60:.1f} min (ideal, no overhead)")
for eff in (1.0, 0.6):
    print(f"  at {eff:.0%} link efficiency: {sec/eff/60:.1f} min")
total_gb = MB * DEVICES / 1000
print(f"fleet transfer: {MB} MB x {DEVICES:,} = {total_gb:,.0f} GB (decimal) per full rollout")
UNIT_STORE, UNIT_EGRESS = 1.0, 1.0   # abstract units per GB-month stored and per GB sent (NOT real prices)
print(f"server storage for 1 copy: {MB/1000:.2f} GB; keep 5 versions: {5*MB/1000:.2f} GB -> {5*MB/1000*UNIT_STORE:.2f} units/month")
print(f"egress per full rollout: {total_gb*UNIT_EGRESS:,.0f} units")
for label, frac in (("delta patch 25% of size", 0.25),):
    print(f"{label}: {total_gb*frac:,.0f} GB, {sec*frac/60:.1f} min per device")
# retries: link drops; with resumable downloads only the lost chunks resend; without, restart
import random; random.seed(18)
def sim(resume, n=3000, drop_p=0.01, chunks=60):
    """Each chunk can drop the connection with probability drop_p. Resume: redo only that chunk. Restart: begin again from chunk 0."""
    sent = 0
    for _ in range(n):
        done = 0
        while done < chunks:
            sent += 1
            if random.random() < drop_p:
                if not resume: done = 0
            else: done += 1
    return sent / (n * chunks)
print(f"bytes sent / model size, restart-on-drop: {sim(False):.2f}x ; resumable chunks: {sim(True):.2f}x  (toy loss model, 1% drop per chunk)")
```

**Output (my run):** (python3 -I, seeded; abstract units; the drop model is a toy)
```
one 60 MB update at 2 Mbps: 60 MB * 8 / 2 = 240 s = 4.0 min (ideal, no overhead)
  at 100% link efficiency: 4.0 min
  at 60% link efficiency: 6.7 min
fleet transfer: 60 MB x 100,000 = 6,000 GB (decimal) per full rollout
server storage for 1 copy: 0.06 GB; keep 5 versions: 0.30 GB -> 0.30 units/month
egress per full rollout: 6,000 units
delta patch 25% of size: 1,500 GB, 1.0 min per device
bytes sent / model size, restart-on-drop: 1.38x ; resumable chunks: 1.01x  (toy loss model, 1% drop per chunk)
```

**Follow-ups:**
- *Server fallback when offline?* Queue the photo with consent and sync later; never block the inspector.
- *How do you see accuracy without photos?* Confidence histograms, user corrections, and a small consented sample.
- *Update cadence?* Only as often as accuracy gain justifies the bytes; staged rollout.

**Common mistakes:**
- Forgetting egress is the cost, not storage.
- Pushing the update over mobile data without a Wi-Fi rule.
- No rollback path on the device.

---

### Q19 ⭐⭐ 🟡 [Set E, Q2 of 4, 10 min, 20 pts] On-device model packaging. Describe the path from a trained model to a shipped one: export to ONNX, quantisation and its accuracy check, size and latency measurement on a reference device profile, signed model artefact, staged rollout and rollback. Reference Part 6 Q10, Part 6 Q29 and Part 6 Q42. Run an ONNX export and dynamic quantisation on a small model in Python and report size and accuracy change on a held-out set; label timings as sandbox-only, not device numbers.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Export to ONNX, quantise, check accuracy on a held-out set against a gate, measure size and latency on a reference device profile, sign the artefact, roll out in stages and keep the previous model for rollback.

**Then explain:**
- Path: train, export with dynamic axes (Part 6 Q10), dynamic int8 quantisation (Part 6 Q29), accuracy gate, device measurement, sign, staged rollout, rollback. Export failures (unsupported operators, tracing issues) are Part 6 Q42.
- My run: a small MLP on synthetic data. int8 file is 0.25 of the fp32 size, accuracy change -0.0005, prediction agreement 0.9985. The gate here is a drop of at most 0.01.
- Latency lesson: sandbox timings are noisy and say little. Two runs of this same script gave fp32 times of 5.8 ms and 20.7 ms, and int8 was slower than fp32 in one and faster in the other. Dynamic quantisation does not always speed things up, and these are sandbox CPU timings, not device numbers; measure repeated runs on the real device profile.
- Signing: a manifest with the file hash and version, signed. The demo uses an HMAC with a fake key; production uses a KMS or HSM-held key or an asymmetric signature and a public key baked into the app. The device verifies before loading. A one-bit change in the file fails verification.
- Failure modes: accuracy fine overall but worse on one slice; unsupported operator on an old runtime; a model that loads but runs out of memory on the low-end phone; unsigned models; rollout to everyone at once.
- Scoring note (20 pts, 10 min): about 6 for the packaging path with assumptions, 6 for correct size, accuracy and latency evidence with a stated gate, 4 for failure modes (slices, runtime, signing), 2 for the runnable check, 2 for the summary.

**Example:** fp32 1,291 KiB, int8 329 KiB. Accuracy 0.9395 versus 0.9390, so the drop is 0.0005, under the 0.01 gate: pass. Ship to 1 percent of devices, watch crash and latency counters, then 10, 50, 100 percent.

**Code:** (torch, onnx, onnxruntime from the b6p06 venv; versions in the output; fake HMAC key)
```python
"""Q19: tiny model -> ONNX -> dynamic int8 quantisation -> size/accuracy check -> HMAC-signed manifest.
Timings are sandbox CPU only, NOT device numbers. Fake signing key."""
import os, sys, json, time, hmac, hashlib, tempfile, warnings
warnings.filterwarnings("ignore")
import numpy as np, torch, onnx, onnxruntime as ort
from onnxruntime.quantization import quantize_dynamic, QuantType
torch.manual_seed(19); np.random.seed(19)
d = tempfile.mkdtemp(prefix="q19_", dir="/tmp/claude-0/b12_q12_22")
# synthetic 3-class "defect" data, 128 features
C = np.random.randn(3, 128) * 0.25
def make(n):
    y = np.random.randint(0, 3, n); c = C
    return (c[y] + np.random.randn(n, 128)).astype("float32"), y
Xtr, ytr = make(6000); Xte, yte = make(2000)
m = torch.nn.Sequential(torch.nn.Linear(128, 512), torch.nn.ReLU(), torch.nn.Linear(512, 512), torch.nn.ReLU(), torch.nn.Linear(512, 3))
opt = torch.optim.Adam(m.parameters(), 1e-3)
for ep in range(15):
    for i in range(0, 6000, 128):
        xb, yb = torch.from_numpy(Xtr[i:i+128]), torch.from_numpy(ytr[i:i+128])
        opt.zero_grad(); torch.nn.functional.cross_entropy(m(xb), yb).backward(); opt.step()
m.eval()
f32 = os.path.join(d, "model_fp32.onnx"); i8 = os.path.join(d, "model_int8.onnx")
torch.onnx.export(m, torch.from_numpy(Xte[:1]), f32, input_names=["x"], output_names=["logits"], dynamic_axes={"x": {0: "batch"}}, dynamo=False)
onnx.checker.check_model(onnx.load(f32))
quantize_dynamic(f32, i8, weight_type=QuantType.QInt8)
def acc_and_time(path):
    s = ort.InferenceSession(path, providers=["CPUExecutionProvider"])
    s.run(None, {"x": Xte[:64]})
    t = time.perf_counter(); out = s.run(None, {"x": Xte})[0]; dt = time.perf_counter() - t
    return (out.argmax(1) == yte).mean(), dt * 1000, out
a32, t32, o32 = acc_and_time(f32); a8, t8, o8 = acc_and_time(i8)
s32, s8 = os.path.getsize(f32), os.path.getsize(i8)
print(f"torch version {torch.__version__}, onnxruntime {ort.__version__}, onnx {onnx.__version__}")
print(f"fp32: {s32/1024:.0f} KiB  acc={a32:.4f}  2000-row run {t32:.1f} ms (sandbox CPU only)")
print(f"int8: {s8/1024:.0f} KiB  acc={a8:.4f}  2000-row run {t8:.1f} ms (sandbox CPU only)")
print(f"size ratio int8/fp32 = {s8/s32:.2f}; accuracy change = {a8-a32:+.4f}; prediction agreement = {(o32.argmax(1)==o8.argmax(1)).mean():.4f}")
GATE_DROP = 0.01
assert a32 - a8 <= GATE_DROP, "quantisation accuracy gate failed"
print(f"gate: accuracy drop <= {GATE_DROP} -> PASS")
# signed manifest (HMAC with a FAKE key; real systems use KMS/HSM-held keys or Ed25519 and a trust root on device)
KEY = b"fake-demo-key-not-secret"
man = {"model": "model_int8.onnx", "sha256": hashlib.sha256(open(i8, "rb").read()).hexdigest(), "version": "2026.10.1", "min_app": "3.2"}
body = json.dumps(man, sort_keys=True).encode(); sig = hmac.new(KEY, body, hashlib.sha256).hexdigest()
def verify(path, man, sig):
    body = json.dumps(man, sort_keys=True).encode()
    return hmac.compare_digest(sig, hmac.new(KEY, body, hashlib.sha256).hexdigest()) and hashlib.sha256(open(path, "rb").read()).hexdigest() == man["sha256"]
print("manifest verifies:", verify(i8, man, sig))
raw = bytearray(open(i8, "rb").read()); raw[100] ^= 1
tam = os.path.join(d, "tampered.onnx"); open(tam, "wb").write(raw)
print("tampered file verifies:", verify(tam, man, sig))
```

**Output (my run):** (python3 -I; the first line is a library warning about pre-processing, harmless here)
```
WARNING:root:Please consider to run pre-processing before quantization. Refer to example: https://github.com/microsoft/onnxruntime-inference-examples/blob/main/quantization/image_classification/cpu/ReadMe.md 
torch version 2.14.1+cu130, onnxruntime 1.31.0, onnx 1.23.2
fp32: 1291 KiB  acc=0.9395  2000-row run 20.7 ms (sandbox CPU only)
int8: 329 KiB  acc=0.9390  2000-row run 10.5 ms (sandbox CPU only)
size ratio int8/fp32 = 0.25; accuracy change = -0.0005; prediction agreement = 0.9985
gate: accuracy drop <= 0.01 -> PASS
manifest verifies: True
tampered file verifies: False
```

**Follow-ups:**
- *Quantisation hurt one class: what now?* Per-slice gate fails; try per-channel or quantisation-aware training (Book 1), or skip it for that layer.
- *Why sign if the app store signs the app?* The model is a separate download; the signature protects that channel.
- *Rollback on a device?* Keep the last good model file and switch back on a crash-loop or health flag.

**Common mistakes:**
- Quoting sandbox timings as device latency.
- Checking only overall accuracy.
- Shipping an unsigned model file.
- Rolling out to 100 percent at once.

---

### Q20 ⭐⭐ 🟡 [Set R, Q3 of 4, 12 min, 30 pts] Recommender feedback loops, experiments and rollback. The home-feed model is retrained daily on clicks it influenced. Explain exposure bias and feedback loops (Part 8 Q33), how an A/B test and a holdout of unpersonalised traffic keep a clean baseline (Part 6 Q13), what a safe daily-retrain pipeline gates on (Part 7 Q10, Part 7 Q26) and how you roll back a model whose offline metric rose and watch time fell (Part 7 Q12). Simulate a popularity feedback loop in Python and show the holdout metric catching the drift.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Retraining daily on clicks the model caused teaches it its own habits, so I keep a small unpersonalised holdout, A/B test every change against it, gate retrains on checks, and roll back on the business metric (watch time) not only the offline one.

**Then explain:**
- Exposure bias and the loop (Part 8 Q33): the model only gets feedback on items it showed, so it keeps showing old winners and never learns about new or unseen items. The in-loop metric can look fine because users do click what you show.
- Clean baseline: a small slice (5 to 10 percent) gets random or non-personalised content, so clicks on it are unbiased. Use it for evaluation and for a fair A/B comparison (Part 6 Q13).
- Safe daily retrain gates (Part 7 Q10 promotion gates, Part 7 Q26 shadow and canary): data checks, an offline floor, a holdout-based check, shadow, then a canary with abort rules on watch time and latency.
- Rollback (Part 7 Q12): if offline AUC rose and watch time fell, trust the online result. Move the registry alias back to the last good model; keep the previous artefact and features available.
- Failure modes: holdout too small to read; holdout contaminated by the personalised model; retraining on a bad week; popularity lock-in; creator unfairness from a rich-get-richer loop.
- Scoring note (30 pts, 12 min): about 9 for clarifying and stated assumptions (what is the objective, how big is the holdout, what labels exist), 9 for a design with gates and rollback that fits the numbers, 6 for failure modes (loop, contamination, drift), 3 for the runnable simulation, 3 for the 60-second summary.

**Example:** In the run the main-traffic CTR stayed between about 0.43 and 0.47 for days 15 to 40, while the model's slate scored only about 0.77 of the best well-measured holdout items, and fresh items were 0 percent of main impressions versus about 25 percent of holdout impressions. The in-loop metric hid the problem; the holdout showed it.

**Code:** (numpy; catalogue churn 4 percent a day, naive model ranks by total clicks)
```python
"""Q20: popularity feedback loop. A daily retrain on clicks the model itself caused locks onto old winners; a 5% unpersonalised
holdout (random items) gives a clean estimate. Sandbox simulation, invented numbers, seeded."""
import numpy as np
rng = np.random.default_rng(20)
N, K, DAYS, IMPR, HOLD, CHURN = 2000, 10, 40, 100_000, 0.10, 0.04
appeal = rng.beta(1.2, 18, N)                      # true click probability per item (hidden from the model)
age = np.zeros(N)
clicks = np.zeros(N); shows = np.zeros(N); hc_ = np.zeros(N); hs_ = np.zeros(N)
for _ in range(20_000):                            # day-0 seed: random exposure
    i = rng.integers(N); shows[i] += 1; clicks[i] += rng.random() < appeal[i]
POS = 1 / np.log2(np.arange(2, K + 2)); POS /= POS.sum()
print(f"{'day':>3s} {'main CTR':>9s} {'holdout CTR of model slate':>27s} {'best well-measured holdout items':>33s} {'ratio':>6s} {'fresh share main/holdout':>26s}")
rows = []
for day in range(DAYS + 1):
    if day:
        new = rng.choice(N, int(N * CHURN), replace=False)       # catalogue churn: new items arrive with fresh appeal
        appeal[new] = rng.beta(1.2, 18, len(new)); age[new] = 0
        for a in (clicks, shows, hc_, hs_): a[new] = 0
        age[np.setdiff1d(np.arange(N), new)] += 1
    top = np.argsort(-clicks)[:K]                                # naive model: rank by total clicks (rich get richer)
    n_h = int(IMPR * HOLD); n_m = IMPR - n_h
    it = top[rng.choice(K, size=n_m, p=POS)]
    c = rng.random(n_m) < np.minimum(appeal[it] * 2, 1)
    np.add.at(shows, it, 1); np.add.at(clicks, it, c)
    hi = rng.integers(N, size=n_h); hc = rng.random(n_h) < appeal[hi]
    np.add.at(hs_, hi, 1); np.add.at(hc_, hi, hc); np.add.at(shows, hi, 1); np.add.at(clicks, hi, hc)
    ok = hs_ >= 30
    hctr = np.where(hs_ > 0, hc_ / np.maximum(hs_, 1), 0)
    slate_est = hctr[top][ok[top]].mean() if ok[top].any() else float("nan")
    best = np.sort(hctr[ok])[-K:].mean() if ok.sum() >= K else float("nan")
    ratio = slate_est / best
    fresh_main = (age[it] < 7).mean(); fresh_hold = (age[hi] < 7).mean()
    rows.append((day, c.mean(), slate_est, best, ratio, fresh_main, fresh_hold))
    if day in (5, 10, 15, 20, 30, 40):
        print(f"{day:3d} {c.mean():9.3f} {slate_est:27.3f} {best:33.3f} {ratio:6.2f} {fresh_main:12.1%} /{fresh_hold:7.1%}")
late = [r for r in rows if r[0] >= 15]
print("\nmain-traffic CTR over days 15-40: min %.3f max %.3f (the in-loop metric looks fine)" % (min(r[1] for r in late), max(r[1] for r in late)))
print("holdout ratio over days 15-40: mean %.2f  -> ALERT rule: ratio < 0.8 for 5 days" % np.mean([r[4] for r in late]))
assert np.mean([r[4] for r in late]) < 0.8 and np.mean([r[5] for r in late]) < 0.1
```

**Output (my run):** (python3 -I in the b6p06 venv with numpy; seeded; day 5 fresh share reads 100 percent only because every item is still under 7 days old at the start)
```
day  main CTR  holdout CTR of model slate  best well-measured holdout items  ratio   fresh share main/holdout
  5     0.437                       0.213                             0.321   0.67       100.0% / 100.0%
 10     0.428                       0.233                             0.332   0.70         0.0% /  25.4%
 15     0.427                       0.228                             0.315   0.72         0.0% /  24.0%
 20     0.465                       0.244                             0.318   0.77         0.0% /  24.9%
 30     0.447                       0.228                             0.298   0.76         0.0% /  25.0%
 40     0.437                       0.232                             0.307   0.76         0.0% /  25.2%

main-traffic CTR over days 15-40: min 0.427 max 0.468 (the in-loop metric looks fine)
holdout ratio over days 15-40: mean 0.77  -> ALERT rule: ratio < 0.8 for 5 days
```

**Follow-ups:**
- *Is the holdout free?* No. It costs a little engagement. Keep it small and rotate users.
- *What alert rule?* Holdout ratio below 0.8 for 5 days, or watch time down in the canary.
- *Fix for the loop itself?* Exploration, new-item boost and debiasing are modelling work in Book 1; the platform supplies the holdout and gates.

**Common mistakes:**
- Evaluating the new model on logs the old model produced.
- Using only the offline metric to promote.
- A holdout so small it cannot be read.
- No way to roll back features along with the model.

---

### Q21 ⭐⭐ 🟡 [Set C, Q3 of 4, 12 min, 30 pts] Credit-risk explainability, fairness and audit logging at platform level. Decide what is logged per decision (inputs, model and feature versions, score, reason codes, overrides, who and when), how long it is kept and how it is protected, how reason codes are generated and tested for stability, and how a fairness slice report is produced each release (Part 7 Q27, Part 8 Q28). Reference Part 8 Q29 for the personal-data tension in logs. Build a tamper-evident hash-chained decision log in Python and a test that detects an edited record.
**Asked at:** Coverage of the RBI FREE-AI framework of 13 Aug 2025 (law.asia, storyboard18, cxodigitalpulse, securiti, mitsloanme; search snippets only, not opened): seven principles, 26 recommendations in six pillars, board-approved AI policy, AI-specific audit, disclosures; no snippet gave model-risk or localisation text, so those parts are hedged 'check the RBI site'; regulated BFSI and GCC credit and fraud roles | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Log every decision with inputs, versions, score, reason codes, overrides, who and when into an append-only hash-chained log, keep personal data minimal and encrypted, test that reason codes are stable, and produce a slice report each release.

**Then explain:**
- Per decision: a hashed applicant reference (not the raw id), model version, feature-set version, score, decision, reason codes, override with who, why and when. Overrides are new appended records, not edits. Part 8 Q29 covers the audit versus minimisation tension: log what an auditor needs, store identifiers hashed or in a separate access-controlled store, and set retention to the rule you were given (check the regulator's current text; the length is a policy decision, not a number I invent).
- Protection: encryption at rest, role-based read access, write-once storage, and the chain head hash anchored somewhere else (a separate account or a signed daily checkpoint).
- Tamper evidence: each record hashes the previous hash plus its own content. Edit, delete or reorder any record and the verifier reports the first bad row. Limit: editing and re-hashing the last row is only caught if the head hash is anchored elsewhere. It is tamper-evident, not tamper-proof.
- Reason codes: here the top points lost against a reference applicant; test stability under small input noise (100 percent unchanged in the run, gate at 95). Check the real method with legal and model-risk teams.
- Fairness slice report each release (Part 7 Q27 gate, Part 8 Q28 monitoring): approval rate by slice and the ratio; run showed 52.2 percent versus 58.5 percent, ratio 0.89. The four-fifths figure is a rule of thumb, not a legal test.
- Regulation: RBI FREE-AI (13 Aug 2025) coverage mentions board-approved policy and AI-specific audit; check the regulator's site for current text. I have not read the primary text.
- Scoring note (30 pts, 12 min): about 9 for clarifying and assumptions (retention rule, who reads logs, what a reason code must satisfy), 9 for a log design that is auditable, minimal and protected, 6 for failure modes (tail rewrite, PII in logs, unstable reasons), 3 for the runnable chain and tamper test, 3 for the summary.

**Example:** Row 7 edited and only that row re-hashed: the verifier flags row 8 (its stored prev no longer matches). Row 100's decision flipped: flagged at 100. Row 50 deleted: flagged at 50. Last row edited: flagged at 399 only because the chain head is known here.

**Code:** (invented scorecard and applicants; stdlib only)
```python
"""Q21: tamper-evident decision log (hash chain), reason-code stability test and a fairness slice report. Invented data, stdlib only."""
import json, hashlib, random, copy
random.seed(21)
GENESIS = "0" * 64
def h(rec_wo_hash, prev): return hashlib.sha256((prev + json.dumps(rec_wo_hash, sort_keys=True, separators=(",", ":"))).encode()).hexdigest()
class Log:
    def __init__(self): self.rows = []
    def append(self, rec):
        prev = self.rows[-1]["hash"] if self.rows else GENESIS
        self.rows.append({**rec, "prev": prev, "hash": h(rec, prev)})
    def verify(self):
        prev = GENESIS
        for i, r in enumerate(self.rows):
            body = {k: v for k, v in r.items() if k not in ("prev", "hash")}
            if r["prev"] != prev or r["hash"] != h(body, prev): return i
            prev = r["hash"]
        return None                                     # None = chain intact

# scorecard (invented): points per feature; reason codes = features that cost the most points vs a reference applicant
W = {"missed_payments": -40, "utilisation": -30, "income_stability": 25, "tenure_years": 8}
REF = {"missed_payments": 0, "utilisation": 0.2, "income_stability": 1.0, "tenure_years": 5}
BASE, CUT = 600, 560
def score(x): return BASE + sum(W[k] * (x[k] - REF[k]) for k in W)
def reasons(x, n=2):
    loss = sorted(((W[k] * (x[k] - REF[k]), k) for k in W))[:n]
    return [k for v, k in loss if v < 0]
MODEL, FEATS = "scorecard-2026.10", "fv-17"
apps = []
for i in range(400):
    g = random.choice(["A", "B"])
    x = {"missed_payments": random.choice([0, 0, 0, 1, 2, 3]), "utilisation": round(random.uniform(0.05, 0.95), 2),
         "income_stability": round(random.uniform(0.3, 1.0), 2), "tenure_years": random.randint(0, 15)}
    apps.append((f"app-{i:04d}", g, x))
log = Log()
for aid, g, x in apps:
    s = score(x)
    log.append({"app_id_hash": hashlib.sha256(("salt-demo" + aid).encode()).hexdigest()[:16],   # no raw id in the log
                "model": MODEL, "feature_set": FEATS, "score": round(s, 1), "decision": "approve" if s >= CUT else "decline",
                "reasons": reasons(x) if s < CUT else [], "override": None, "ts": f"2026-10-26T10:{i//60:02d}:{i%60:02d}Z"})
log.rows[7]["override"] = {"by": "officer-9", "to": "approve", "why": "documented income proof"}   # (legit overrides are NEW appended rows in practice)
log.rows[7]["hash"] = h({k: v for k, v in log.rows[7].items() if k not in ("prev", "hash")}, log.rows[7]["prev"])
# ^ re-hashing one row without re-chaining the next one is exactly what the verifier must catch
print("verify after in-place edit of row 7 with re-hash only that row ->", "first bad row", log.verify())
log.rows[7].pop("override"); log.rows[7]["override"] = None
log.rows[7]["hash"] = h({k: v for k, v in log.rows[7].items() if k not in ("prev", "hash")}, log.rows[7]["prev"])
assert log.verify() is None; print("restored; chain intact:", log.verify() is None, "rows:", len(log.rows))
t = copy.deepcopy(log); t.rows[100]["decision"] = "approve" if t.rows[100]["decision"] == "decline" else "decline"
print("edit decision in row 100 ->", "first bad row", t.verify())
t = copy.deepcopy(log); del t.rows[50]
print("delete row 50 ->", "first bad row", t.verify())
t = copy.deepcopy(log); t.rows[-1]["score"] += 1
print("edit the LAST row ->", "first bad row", t.verify(), "(an attacker who edits the tail and rehashes it is only caught if the head hash is anchored elsewhere)")
assert t.verify() == len(t.rows) - 1

# reason-code stability: tiny input noise should rarely change the top reason
def stable(frac_noise=0.02, trials=300):
    same = tot = 0
    for _, _, x in apps:
        if score(x) >= CUT: continue
        base = reasons(x, 1)
        for _ in range(3):
            y = {k: (v * (1 + random.uniform(-frac_noise, frac_noise)) if k in ("utilisation", "income_stability") else v) for k, v in x.items()}
            tot += 1; same += reasons(y, 1) == base
    return same / tot
print(f"top reason unchanged under +-2% noise on continuous inputs: {stable():.1%}  (release gate: >= 95%)")
# fairness slice report per release (selection rate ratio; four-fifths rule of thumb, NOT a legal test)
sel = {}
for (aid, g, x), r in zip(apps, log.rows): sel.setdefault(g, []).append(r["decision"] == "approve")
rates = {g: sum(v) / len(v) for g, v in sel.items()}
print("approval rate by slice:", {g: f"{r:.1%} (n={len(sel[g])})" for g, r in rates.items()}, " ratio low/high = %.2f" % (min(rates.values()) / max(rates.values())))
```

**Output (my run):** (python3 -I, seeded)
```
verify after in-place edit of row 7 with re-hash only that row -> first bad row 8
restored; chain intact: True rows: 400
edit decision in row 100 -> first bad row 100
delete row 50 -> first bad row 50
edit the LAST row -> first bad row 399 (an attacker who edits the tail and rehashes it is only caught if the head hash is anchored elsewhere)
top reason unchanged under +-2% noise on continuous inputs: 100.0%  (release gate: >= 95%)
approval rate by slice: {'A': '52.2% (n=205)', 'B': '58.5% (n=195)'}  ratio low/high = 0.89
```

**Follow-ups:**
- *Where do you keep the head hash?* In a separate account or a signed periodic checkpoint.
- *Customer asks for erasure?* Log hashed references and keep a legal-hold rule; handle with privacy counsel.
- *Reasons changed after a release?* The stability test should have failed the gate; keep the version in each record to explain old decisions.

**Common mistakes:**
- Logging raw personal data "for audit".
- Editing records in place for an override.
- No head anchoring.
- Reason codes never tested for stability.

---

### Q22 ⭐⭐ 🟡 [Set D, Q3 of 4, 12 min, 30 pts] Forecast monitoring and override governance. Planners override 12 percent of forecasts (invented). Explain how you monitor forecast error by hierarchy level and by item class, detect bias (systematic over- or under-forecast), separate model error from data-feed errors, keep override history, and measure whether overrides help (forecast value added). Reference Part 8 Q8, Part 8 Q23 and Part 8 Q34. Compute WAPE, bias and forecast value added on an invented table in Python and decide which items to automate.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Track WAPE and bias by hierarchy level and item class, separate model error from feed errors with freshness and volume checks, keep override history, and measure forecast value added so you only keep human review where it beats the model.

**Then explain:**
- Error by level and class: item-level WAPE (sum of absolute errors over sum of actuals) hides errors that cancel at the total. In the run the portfolio total was off by 10.1 percent while item-level WAPE by class ranged from 4.8 to 57.8 percent. Report at the level where decisions are made.
- Bias: sum of (forecast minus actual) over actuals. Negative means under-forecast. Promo items were at about -25 percent: a systematic miss, a feature problem, not noise.
- Model error versus data error: check freshness and row counts first (Part 8 Q23), then input drift (Part 8 Q8 for late labels), then model. A flat zero day from a broken feed is not a model failure.
- Override history: store the model forecast, the override, who, when and why, and the actual. Without it you cannot measure whether overrides help. Incident handling for sudden misses is Part 8 Q34.
- Forecast value added: error of the model minus error of the final forecast on the same overridden items. Positive means the human helped. Only judge FVA with enough overrides; 1 override tells you nothing (the table says so).
- Decision: automate classes where overrides do not help or are rare and the model is accurate and unbiased (fast movers); keep review where FVA is positive but fix the model cause (promo bias). Failure modes: planners override because they distrust a biased model; FVA computed after they saw the actual; small samples.
- Scoring note (30 pts, 12 min): about 9 for clarifying and assumptions (what the override rate means, level of decision), 9 for correct WAPE, bias and FVA and a defensible automate decision, 6 for failure modes (cancelling, leakage, small n), 3 for the runnable table, 3 for the summary.

**Example:** For two items with actuals 100 and 120 and forecasts 104 and 112, WAPE is (4 + 8) / 220 = 5.45 percent (an assert in the code). Promo overrides cut error from model to final by 19.5 points on 3 items: positive FVA, but the -25.5 percent bias says fix the model.

**Code:** (invented, seeded table of 50 items, 5 overridden, which is 10 percent of the invented 12 percent)
```python
"""Q22: WAPE, bias and forecast value added (FVA) on an invented, seeded table of 50 items. Stdlib only."""
import random
random.seed(22)
# class: (count, typical level, model noise, model bias, override rate, planner skill: share of error the planner removes; negative = adds error)
SPEC = {"fast": (20, 100, 0.06, 0.00, 0.04, -0.3), "slow": (10, 12, 0.35, 0.05, 0.08, 0.2),
        "promo": (12, 150, 0.20, -0.20, 0.22, 0.7), "intermittent": (8, 3, 0.9, -0.10, 0.10, 0.0)}
rows = []
for cls, (n, lvl, noise, b, orate, skill) in SPEC.items():
    for k in range(n):
        a = max(0, round(random.gauss(lvl, lvl * 0.25)))
        m = max(0.0, a * (1 + b) + random.gauss(0, noise * max(a, 1)))
        ov = None
        if random.random() < orate:
            ov = a + (m - a) * (1 - skill) + random.gauss(0, 0.02 * max(a, 1))   # planner moves the forecast toward (or away from) the truth
        rows.append((f"{cls[:2]}{k}", cls, a, round(m, 1), None if ov is None else round(max(ov, 0), 1)))
def wape(pairs): return sum(abs(a - f) for a, f in pairs) / max(sum(a for a, f in pairs), 1e-9)
def bias(pairs): return sum(f - a for a, f in pairs) / max(sum(a for a, f in pairs), 1e-9)   # + = over-forecast
assert abs(wape([(100, 104), (120, 112)]) - 12 / 220) < 1e-12      # hand check: (4+8)/220
no = sum(r[4] is not None for r in rows)
print(f"items {len(rows)}, overridden {no} = {100*no/len(rows):.0f}%  overall WAPE model {100*wape([(r[2], r[3]) for r in rows]):.1f}%  bias {100*bias([(r[2], r[3]) for r in rows]):+.1f}%")
print(f"\n{'class':14s}{'WAPE':>7s}{'bias':>8s}{'n':>4s}{'ovr':>4s}{'FVA on overridden (pts)':>25s}  decision")
for cls in SPEC:
    rs = [r for r in rows if r[1] == cls]; ov = [r for r in rs if r[4] is not None]
    w, b = wape([(r[2], r[3]) for r in rs]), bias([(r[2], r[3]) for r in rs])
    fva = 100 * (wape([(r[2], r[3]) for r in ov]) - wape([(r[2], r[4]) for r in ov])) if ov else None
    if len(ov) < 3: dec = "too few overrides to judge FVA; " + ("automate" if abs(b) < 0.1 and w < 0.15 else "keep review, fix model")
    elif fva <= 0: dec = "automate: overrides do not help"
    elif abs(b) > 0.1: dec = "overrides help because model is biased: fix the model bias, keep review till then"
    else: dec = "keep review"
    print(f"{cls:14s}{100*w:6.1f}%{100*b:+7.1f}%{len(rs):4d}{len(ov):4d}{'n/a' if fva is None else f'{fva:+.1f}':>25s}  {dec}")
by = {}
for r in rows: by.setdefault(r[1], []).append(r)
tot_a, tot_f = sum(r[2] for r in rows), sum(r[3] for r in rows)
print(f"\nwhole-portfolio total: actual {tot_a}, model {tot_f:.0f} -> total error {100*abs(tot_f-tot_a)/tot_a:.1f}% (cancelling) vs item-level WAPE above")
```

**Output (my run):** (python3 -I)
```
items 50, overridden 5 = 10%  overall WAPE model 16.3%  bias -13.2%

class            WAPE    bias   n ovr  FVA on overridden (pts)  decision
fast             4.8%   -2.1%  20   1                     +0.7  too few overrides to judge FVA; automate
slow            30.6%   -7.9%  10   0                      n/a  too few overrides to judge FVA; keep review, fix model
promo           26.8%  -25.5%  12   3                    +19.5  overrides help because model is biased: fix the model bias, keep review till then
intermittent    57.8%  +31.7%   8   1                     +0.0  too few overrides to judge FVA; keep review, fix model

whole-portfolio total: actual 3932, model 3413 -> total error 13.2% (cancelling) vs item-level WAPE above
```

**Follow-ups:**
- *Why WAPE and not MAPE?* MAPE blows up on zeros and tiny actuals; WAPE weights by volume.
- *Should you ban overrides?* No. Measure them, require a reason, and drop them where FVA is not positive.
- *How do you know it is the feed?* Freshness, row-count and null-rate checks fire before the error metric does.

**Common mistakes:**
- Reporting only the top-level error.
- Judging override value with 1 or 2 overrides.
- Not saving the pre-override model forecast.
- Treating a biased class as noise.
