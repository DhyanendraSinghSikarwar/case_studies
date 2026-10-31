### Q34 ⭐ 🟡 [Maturity assessment] Using the three Google-style levels and a Microsoft-style five-level view (as reported secondhand, hedged), assess a team where training is a notebook, deploys are manual, monitoring is a weekly spreadsheet and the model registry is a shared folder (invented). Give a 6-month roadmap with the smallest next step per quarter, the leading indicators of progress and the trap of over-engineering. Cross-reference Part 4, Part 5, Part 7 and Part 8 by question number where they apply (Part 7 Q9, Part 8 Q2). Score the team on an invented rubric in Python and print the roadmap.
**Asked at:** MLOps maturity and tech-debt sources (ZenML maturity-models post, NannyML '5 levels of MLOps maturity', Towards Data Science, arXiv 2503.15577; search snippets only, not opened): Google levels 0 to 2 (manual, pipeline automation, full CI/CD) and Microsoft's five levels as reported secondhand; the Sculley et al. 2015 'Hidden technical debt' paper itself was not found, so only the commonly cited ideas are used | Job-posting and community patterns for MLOps, platform and ML-engineering roles at Indian GCCs, product companies and IT-services firms and at global product companies; inferred from search snippets about system-design and FinOps rounds, not from a verified company report
**Say this first (1 line):** This team is at level 0 on every dimension; I would not buy a platform, I would fix one gap per quarter, starting with the registry because nothing else can be audited without it.

**Then explain:**
- Google-style levels (as widely described, check the original): level 0 manual, level 1 pipeline automation and continuous training, level 2 CI/CD for the pipeline itself. The Microsoft-style five-level view is only known to me secondhand, so I use it as a vocabulary (ad hoc, repeatable, automated, measured, optimised), not as a standard.
- Assessment: notebook training = level 0, manual deploys = level 0, spreadsheet monitoring = level 0, shared-folder registry = level 0. Roadmap: Q1 registry plus a reproducible training script plus a first test (Part 4, Part 1), Q2 one CI deploy job (Part 7 Q9) plus three automated monitoring checks (Part 8 Q2) plus data versioning. Pipelines (Part 5) come after, when the script already works from one command.
- Leading indicators beat lagging ones: share of prod models with a registered version, minutes to reproduce last month's model, manual deploys per month, time to detect a bad input.
- Failure modes: scoring the team once and never again; buying Kubeflow or a feature store at level 0; metrics that people game (counting registered models that nobody deploys from).
- Scoring note [Not a timed set]: full marks need a concrete smallest step per quarter with an indicator; partial for a list of tools with no order.

**Example:** My invented rubric scores six dimensions 0 to 2, so the maximum is 12. Level 1 starts at half the points (6 of 12). Each roadmap step lifts one dimension from 0 to 1. After six steps the score is 6/12 and the level flips from 0 to 1, as the output shows. No step needs new infrastructure beyond a tracker and one CI job.

**Code:** run with `python3 -I q34.py`. Rubric weights and thresholds are invented for the interview.
```python
# Q34: invented maturity rubric (0-2 per dimension) and a 6-month roadmap. Abstract, hand-checkable.
dims = ["training", "deploy", "monitoring", "registry", "tests", "data_versioning"]
team = {"training": 0, "deploy": 0, "monitoring": 0, "registry": 0, "tests": 0, "data_versioning": 0}
# 0 = manual, 1 = automated pipeline, 2 = automated + gated (Google-style levels 0/1/2, simplified)
def level(score, n):
    pct = score / (2 * n)
    return 0 if pct < 0.34 else 1 if pct < 0.75 else 2
roadmap = [
    ("Q1", "registry", "Part 4 Q25 style: log runs and register models in a tracker; stop the shared folder",
     "100% of prod models have a registered version id"),
    ("Q1", "training", "move notebook to a script with fixed seed and pinned deps (Part 1)",
     "one command reproduces last model"),
    ("Q2", "deploy", "one CI job: tests + build + deploy to staging (Part 7 Q9)",
     "manual deploys per month falls to 0 for staging"),
    ("Q1", "tests", "add 5 unit tests for feature code and one data-schema check (Part 1)", "CI red on a deliberately broken column"),
    ("Q2", "data_versioning", "pin training data by hash or snapshot id (Part 4)", "every model record names its data version"),
    ("Q2", "monitoring", "replace spreadsheet with 3 automated checks and one alert (Part 8 Q2)",
     "time-to-detect drops from days to hours"),
]
def run(state):
    s = sum(state.values()); return s, level(s, len(dims))
s, l = run(team); print(f"start: score {s}/12, level {l}")
for q, d, step, ind in roadmap:
    team[d] = 1
    s, l = run(team)
    print(f"{q} step on {d}: score {s}/12, level {l}\n    do: {step}\n    indicator: {ind}")
assert run(team) == (6, 1), run(team)
print("trap: no feature store or Kubeflow until every dimension is at 1 and the pain is named")
print("final:", run(team))
```

**Output (my run):**
```
start: score 0/12, level 0
Q1 step on registry: score 1/12, level 0
    do: Part 4 Q25 style: log runs and register models in a tracker; stop the shared folder
    indicator: 100% of prod models have a registered version id
Q1 step on training: score 2/12, level 0
    do: move notebook to a script with fixed seed and pinned deps (Part 1)
    indicator: one command reproduces last model
Q2 step on deploy: score 3/12, level 0
    do: one CI job: tests + build + deploy to staging (Part 7 Q9)
    indicator: manual deploys per month falls to 0 for staging
Q1 step on tests: score 4/12, level 0
    do: add 5 unit tests for feature code and one data-schema check (Part 1)
    indicator: CI red on a deliberately broken column
Q2 step on data_versioning: score 5/12, level 1
    do: pin training data by hash or snapshot id (Part 4)
    indicator: every model record names its data version
Q2 step on monitoring: score 6/12, level 1
    do: replace spreadsheet with 3 automated checks and one alert (Part 8 Q2)
    indicator: time-to-detect drops from days to hours
trap: no feature store or Kubeflow until every dimension is at 1 and the pain is named
final: (6, 1)
```

**Follow-ups:**
- *When do you stop?* When the next gap costs more than the incidents it prevents; maturity is a means, not a goal.
- *Is level 2 needed everywhere?* No. A quarterly batch model rarely needs continuous training.
- *How do you get buy-in?* Tie each step to a named pain (late detection, unreproducible model) with its indicator.

**Common mistakes:**
- Treating a maturity level as a target for all models.
- Starting with tools rather than the pain.
- No indicator, so nobody can say the quarter worked.

### Q35 ⭐ 🔴 [Set F, Q4 of 4, 12 min, 40 pts] Fraud platform incident and resilience. At 02:10 the false-positive rate triples after a nightly feature job change (invented). Walk the incident: detect (Part 8 Q43), contain (rollback or fallback rule set, Part 7 Q12), diagnose (skew, late data, schema change; Part 9 Q7 and Part 9 Q31), decide fail-open versus fail-closed per transaction class, communicate, and write the blameless follow-ups. Then add the cost angle: which controls are worth their spend. Build a fallback decision function in Python with a rules-only mode and a test that the switch is exercised monthly.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** First stop the bleeding with a rollback or a rules-only fallback, then diagnose; decide fail-open or fail-closed per transaction class ahead of time, and prove the switch works by drilling it every month.

**Then explain:**
- Detect (Part 8 Q43): an alert on the false-positive proxy (block rate, step-up rate, complaint calls) against a baseline for that hour; a tripled block rate should page, not wait for the morning report.
- Contain (Part 7 Q12): roll back the nightly feature job or flip to the rules-only mode. Prefer the one that is already tested; a mode never drilled is a gamble at 02:10.
- Diagnose: compare feature distributions before and after the job change, check schema and late-arriving data, and training-serving skew (Part 9 Q7, Part 9 Q31). Look first at what changed, not at what looks odd.
- Fail-open versus fail-closed per class: low-value card-present may fail open (allow), high-value or card-not-present should fail to step-up authentication. State the loss trade-off and who signed it off.
- Communicate: one incident channel, an owner, a status line every 30 minutes, a note to the fraud-ops and customer-support leads. Blameless follow-ups: add a canary on the feature job, a schema contract, a drill calendar.
- Cost angle (abstract units): cheap controls with a big avoided loss win (rollback, drill, shadow rules); a second region for this one failure is poor value.
- Scoring note [Set F, Q4 of 4, 12 min, 40 pts] per the part rubric: about 12 pts for clarifying and stated assumptions (what is the fraud and block baseline, who owns false positives), 12 for a timeline that actually contains and fixes it, 8 for failure modes and cost, 4 for the runnable check, 4 for the 60-second summary. Partial: a diagnosis list with no containment order.

**Example:** At 02:10 the block rate on genuine transactions goes from near zero to all of them because a feature now arrives as a constant. Step one: switch to rules-only. In my toy run, rules-only gives 0.0 false positives on the same genuine traffic, while the broken model gives 1.0. A 100 transaction with the model down is allowed (fail-open); a 15,000 one is stepped-up (fail-closed).

**Code:** run with `python3 -I q35.py`. Toy rules and scores; sandbox only.
```python
# Q35: fallback decision function with rules-only mode, plus a test that the switch is exercised.
import random
random.seed(35)
RULES = lambda t: "block" if t["amount"] > 50_000 or t["country_risk"] else "allow"
def model_score(t): return 0.9 if t["amount"] > 100_000 else 0.05
def decide(t, mode="model", cls="card_present"):
    """mode: model | rules_only | model_unavailable. fail policy per class when no decision is possible."""
    if mode == "rules_only": return RULES(t), "rules"
    try:
        if mode == "model_unavailable": raise TimeoutError
        return ("block" if model_score(t) > 0.5 else "allow"), "model"
    except TimeoutError:
        # fail-open for low-value, fail-closed(step-up) for high-value / risky
        if t["amount"] > 10_000 or cls == "card_not_present": return "step_up", "fail_closed"
        return "allow", "fail_open"
def fp_rate(mode, broken=False, n=2000):
    global model_score
    saved = model_score
    if broken: model_score = lambda t: 0.9          # bad nightly feature job: every txn looks risky
    fp = 0
    for _ in range(n):
        t = {"amount": random.choice([100, 500, 30_000]), "country_risk": False}   # all genuine
        d, _ = decide(t, mode)
        fp += d == "block"
    model_score = saved
    return fp / n
# monthly drill: the switch must be exercised and must work
class Drill:
    last = None
    def run(self, month):
        t = {"amount": 60_000, "country_risk": False}
        assert decide(t, "rules_only") == ("block", "rules")
        assert decide({"amount": 100, "country_risk": False}, "model_unavailable") == ("allow", "fail_open")
        assert decide({"amount": 100, "country_risk": False}, "model_unavailable", "card_not_present") == ("step_up", "fail_closed")
        self.last = month
d = Drill()
def check_drill_freshness(today_month): 
    return d.last is not None and today_month - d.last <= 1
print("freshness before any drill:", check_drill_freshness(10))
d.run(10); print("freshness after drill in month 10:", check_drill_freshness(10))
print("freshness 3 months later:", check_drill_freshness(13), "-> page the owner")
print("false-positive rate on genuine txns: healthy model", fp_rate("model"), "| broken features", fp_rate("model", True), "| rules_only after switch", fp_rate("rules_only", True))
for t, c in [({"amount": 100}, "card_present"), ({"amount": 15_000}, "card_present"), ({"amount": 100}, "card_not_present")]:
    t["country_risk"] = False
    print(t["amount"], c, "->", decide(t, "model_unavailable", c))
# cost angle in abstract units: control cost per month vs expected loss avoided
controls = {"auto-rollback": (2, 40), "monthly drill": (1, 25), "extra region": (30, 20), "shadow rules": (4, 30)}
for k, (cost, avoided) in controls.items(): print(f"{k:14s} cost {cost:3d} avoided {avoided:3d} ratio {avoided/cost:5.1f}")
```

**Output (my run):**
```
freshness before any drill: False
freshness after drill in month 10: True
freshness 3 months later: False -> page the owner
false-positive rate on genuine txns: healthy model 0.0 | broken features 1.0 | rules_only after switch 0.0
100 card_present -> ('allow', 'fail_open')
15000 card_present -> ('step_up', 'fail_closed')
100 card_not_present -> ('step_up', 'fail_closed')
auto-rollback  cost   2 avoided  40 ratio  20.0
monthly drill  cost   1 avoided  25 ratio  25.0
extra region   cost  30 avoided  20 ratio   0.7
shadow rules   cost   4 avoided  30 ratio   7.5
```

**Follow-ups:**
- *Why drill monthly?* Fallback code rots; the drill is the test that it still works, and the freshness check pages the owner when it lapses.
- *Who decides fail-open?* Risk and the business owner, written down in advance, not the on-call engineer at night.
- *Rollback or fallback first?* Whichever is already tested and fastest; both are in the runbook.

**Common mistakes:**
- Debugging the model while the bad decisions continue.
- One global fail policy for all transaction types.
- A fallback nobody has run since it was written.

### Q36 ⭐ 🔴 [Set R, Q4 of 4, 12 min, 40 pts] Recommender cost and scale at 10x. Traffic grows 10x in a year (invented). Identify what breaks first (feature store reads, ranking GPU time, embedding refresh, logging volume), what you cache, precompute or shrink, how you test capacity before launch (Part 6 Q16), how you keep the cost per thousand requests flat and where you would stop optimising and negotiate the product (candidate count, refresh frequency). Reference Part 9 Q35 and Part 3 Q36. Build a cost-per-request model in Python with invented unit costs and a 10x sensitivity table.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | FinOps interview-prep material (TechTarget 'Prepare for your FinOps interview' 12-question tip, hirevire FinOps and cloud-cost prescreening lists, a devopsboys FinOps roadmap; search snippets only, not opened, WebFetch of techtarget.com failed with getaddrinfo ENOTFOUND); generic cloud-cost question families (tagging, showback and chargeback, spot, idle resources, budgeting), none GPU-specific, not verified company reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** At 10x the first things to break are usually feature-store reads and logging volume, so I cache, precompute and shrink before buying more GPUs, and I go back to product for candidate count and refresh frequency when the cost curve stays steep.

**Then explain:**
- What breaks first: hot keys and read throughput on the feature store (Part 9 Q35), then ranking compute per request (candidates times model cost), then embedding refresh time, then log volume and its storage. In my toy model the feature reads dominate.
- Levers: cache popular feature reads, precompute user and item embeddings on a schedule, shrink the candidate set (500 to 200), sample logs but keep full logs for a trace percentage.
- Test before launch (Part 6 Q16): replay a load profile at 10x in staging, watch tail latency and saturation, and repeat the test after each lever. Kubernetes cost controls and limits (Part 3 Q36) must be checked too.
- Keep cost per thousand requests flat: report it as a metric with a target, review per release.
- Stop optimising when the next saving hurts relevance; then negotiate: fewer candidates, slower refresh for cold users, smaller feed page. Numbers in this model are invented abstract units.
- Failure modes: cache hit rate collapsing after a catalogue refresh, stale embeddings after a skipped refresh, logging so heavy it becomes the top cost.
- Scoring note [Set R, Q4 of 4, 12 min, 40 pts]: about 12 for stated assumptions and a bottleneck order, 12 for levers that fit the numbers, 8 for failure and cost trade-offs, 4 for the model, 4 for the summary. Partial: only 'add more GPUs'.

**Example:** My model charges 20 feature reads per request. At 10x with a naive setup the cost per 1k requests is 1.36 times today (extra shard overhead, invented). A 60 percent cache hit rate cuts reads by 60 percent, cutting candidates from 500 to 200 cuts ranking cost by 60 percent. The final line is 0.55 of today's cost per 1k.

**Code:** run with `python3 -I q36.py`. All unit costs are invented abstract units, not prices.
```python
# Q36: cost-per-1000-requests model in abstract units (invented). 10x sensitivity.
base_rps = 100  # requests per second at today's peak
unit = dict(feature_read=0.002, gpu_ms=0.0004, embed_refresh=0.5, log_byte=0.00000002)  # abstract units
def cost_per_1k(mult, cache_hit=0.0, cand=500, rank_ms_per_cand=0.02, refresh_per_day=4, logged_bytes=2000, daily_req=None):
    daily = (daily_req or 86400 * base_rps * 0.3) * mult        # 30% duty cycle, invented
    reads = daily * (1 - cache_hit) * 20 * unit["feature_read"] * mult**0.15   # invented hot-key / extra-shard overhead
    gpu   = daily * cand * rank_ms_per_cand * unit["gpu_ms"]
    emb   = refresh_per_day * unit["embed_refresh"] * 1000 * mult**0.5   # item catalogue grows slower than traffic (invented)
    logs  = daily * logged_bytes * unit["log_byte"]
    total = reads + gpu + emb + logs
    return 1000 * total / daily, dict(reads=reads, gpu=gpu, emb=emb, logs=logs, daily=daily)
print(f"{'case':34s}{'x':>4s}{'cost/1k':>9s}   biggest")
cases = [("today", 1, {}), ("10x naive", 10, {}),
         ("10x + cache 60%", 10, dict(cache_hit=0.6)),
         ("10x + cache + cand 500->200", 10, dict(cache_hit=0.6, cand=200)),
         ("10x + cache + cand + log sample 20%", 10, dict(cache_hit=0.6, cand=200, logged_bytes=400)),
         ("... + refresh 4->2/day (negotiated)", 10, dict(cache_hit=0.6, cand=200, logged_bytes=400, refresh_per_day=2))]
res = {}
for name, m, kw in cases:
    c, parts = cost_per_1k(m, **kw); res[name] = c
    big = max(("reads", "gpu", "emb", "logs"), key=parts.get)
    print(f"{name:34s}{m:>4d}{c:9.4f}   {big}")
assert res["10x + cache + cand + log sample 20%"] <= res["today"]
print("flat vs today?", round(res["10x + cache + cand + log sample 20%"] / res["today"], 2), "x today")
print("sensitivity of 10x naive to unit costs (each +50%):")
b = res["10x naive"]
for k in unit:
    old = unit[k]; unit[k] = old * 1.5; c, _ = cost_per_1k(10); unit[k] = old
    print(f"  {k:14s} -> {c/b:5.3f} x base")
```

**Output (my run):**
```
case                                 x  cost/1k   biggest
today                                1  44.8116   reads
10x naive                           10  60.7855   reads
10x + cache 60%                     10  26.8846   reads
10x + cache + cand 500->200         10  24.4846   reads
10x + cache + cand + log sample 20%  10  24.4526   reads
... + refresh 4->2/day (negotiated)  10  24.3306   reads
flat vs today? 0.55 x today
sensitivity of 10x naive to unit costs (each +50%):
  feature_read   -> 1.465 x base
  gpu_ms         -> 1.033 x base
  embed_refresh  -> 1.002 x base
  log_byte       -> 1.000 x base
```

**Follow-ups:**
- *Which input is the model most sensitive to?* Feature read cost (+50 percent gives 1.465x), so that is where to spend effort first.
- *Why not just scale out?* Cost per request would rise, and some stores have hot-key limits that scale-out does not fix.
- *What do you tell product?* The cost of each extra candidate and each refresh, so they choose.

**Common mistakes:**
- Optimising the model when logs or reads dominate.
- Load-testing only the ranker, not the feature store.
- Quoting a single average cost with no sensitivity.

### Q37 ⭐ 🔴 [Set C, Q4 of 4, 15 min, 40 pts] Credit-risk platform end to end and what an examiner asks. Present the whole design: data zone, feature store, training, validation, registry, deployment, monitoring, audit and decommissioning, with identity, encryption and residency controls. Then answer three examiner-style probes: show me why this applicant was declined, show me who changed the production model last quarter, and show me that the model has been independently validated. Reference Part 4 Q25, Part 4 Q29, Part 10 Q39 and Part 11 Q35. Produce a threat-model and controls table in Python (asset, threat, control, evidence) that fails if any asset lacks evidence.
**Asked at:** Coverage of the RBI FREE-AI framework of 13 Aug 2025 (law.asia, storyboard18, cxodigitalpulse, securiti, mitsloanme; search snippets only, not opened): seven principles, 26 recommendations in six pillars, board-approved AI policy, AI-specific audit, disclosures; no snippet gave model-risk or localisation text, so those parts are hedged 'check the RBI site'; regulated BFSI and GCC credit and fraud roles | ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** I present one governed path from data zone to decommissioning, and I answer the examiner with evidence I can produce on demand: reason codes for a decline, a tamper-evident change log, and a signed independent validation.

**Then explain:**
- Design in order: restricted data zone with residency tags and customer-managed encryption keys; feature store with single definitions (registry governance as in Part 4 Q25); training that records data hash, code commit and seed; independent validation in a separate team; registry with approvals (Part 4 Q29); deployment behind authentication on a private network; monitoring; an append-only audit log; a retirement checklist. Cloud depth is in Part 10 Q39 and Part 11 Q35. Regulatory points (RBI model-risk and localisation expectations) are from adviser summaries: check the regulator's site and current law.
- Probe 1, why declined: store reason codes with each decision and the model and feature versions; I show the top negative contributors. Probe 2, who changed prod last quarter: query the hash-chained promotion log and show the chain verifies. Probe 3, independent validation: show the signed validation memo from a person outside the build team, linked to the model version.
- Failure modes: reasons not stored at decision time, registry edits outside the log, validator who reports to the builder, a retired model still scoring.
- Scoring note [Set C, Q4 of 4, 15 min, 40 pts]: about 12 for scoping assumptions (who the examiner is, which decisions are covered), 12 for a design with the controls, 8 for failures and residency, 4 for the table check, 4 for the summary. Partial: architecture drawn, but no evidence for the probes.

**Example:** Each asset in the table must name a control and the evidence that proves it. The checker fails a row with no evidence, such as 'shadow notebook copy'. The chain probe shows two promotions in my toy log; after I edit one record, verification returns False.

**Code:** run with `python3 -I q37.py`. Rows and logs are invented.
```python
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
```

**Output (my run):**
```
rows ok: 8
- raw bureau + application data  | exfiltration / over-broad access       | evidence: access review export + KMS key policy
- feature store                  | training-serving skew, unauthorised read | evidence: feature registry commit log
- training pipeline              | untracked data or code change          | evidence: run record (Part 4 Q25 style)
- validation report              | self-approval by developer             | evidence: signed validation memo with reviewer id
- model registry                 | unapproved model promoted              | evidence: hash-chained promotion log
- serving endpoint               | stolen model via API, unauthorised caller | evidence: gateway access logs
- decision log                   | tampering, missing reason codes        | evidence: chain verification output
- decommissioned model           | zombie endpoint keeps scoring          | evidence: CMDB retirement ticket
FAIL: assets without control/evidence: shadow notebook copy
probe 2 (who changed prod):  ['ana:promote:pd_v3', 'ana:promote:pd_v4'] chain valid: True
after tamper, chain valid: False
probe 1 (reason codes, top 2 negative): ['bureau_score', 'income_to_emi']
```

**Follow-ups:**
- *Is a hash chain enough for audit?* It shows tampering, not who is trusted; anchor the head hash somewhere the platform team cannot write.
- *How do you explain a complex model?* Reason codes from an approved method plus a documented limitation, agreed with validation.
- *Decommissioning?* Revoke keys, delete endpoints, archive artefacts per retention policy.

**Common mistakes:**
- Evidence assembled after the examiner asks.
- Same person builds and signs off.
- Forgetting the retired model.

### Q38 ⭐ 🔴 [Set D, Q4 of 4, 12 min, 40 pts] Forecasting at scale, cost versus accuracy. Leadership asks to cut forecast compute cost by 40 percent (invented) without hurting service levels. Propose the tiering of series (ABC classes, fast-moving versus long-tail), cheaper models for the long tail, less frequent retraining, reuse of global models, sampling for backtests and warm-start, and the measurement that shows no harm (backtest on stock-out cost, not only error). Reference Part 5 Q39 and Part 6 Q43. Compute from an invented table the compute saved and the expected extra stock-out cost for three policies and pick one.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | FinOps interview-prep material (TechTarget 'Prepare for your FinOps interview' 12-question tip, hirevire FinOps and cloud-cost prescreening lists, a devopsboys FinOps roadmap; search snippets only, not opened, WebFetch of techtarget.com failed with getaddrinfo ENOTFOUND); generic cloud-cost question families (tagging, showback and chargeback, spot, idle resources, budgeting), none GPU-specific, not verified company reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** I tier the series, spend compute where stock-out cost is high, and judge each cost-cut policy on expected extra stock-out cost, not forecast error alone.

**Then explain:**
- Tiering: A items (fast-moving, high value) keep the best model and frequent retraining; B items retrain less often; the long tail uses a cheap or global model. Reference Part 5 Q39 for orchestration at this scale and Part 6 Q43 for batch serving.
- Other levers: reuse a global model across series, sample series for backtests, warm-start instead of training from scratch, skip retraining when drift checks pass.
- Measurement: backtest each policy on stock-out and holding cost, per tier. The 40 percent target is checked on compute, the harm on the cost of misses.
- Failure modes: the long tail sums to a big revenue share, new items with no history, promotions and seasonality breaking a skipped retrain.
- Scoring note [Set D, Q4 of 4, 12 min, 40 pts]: about 12 for assumptions (tier shares, service-level target), 12 for policies that meet the target, 8 for risks, 4 for the table, 4 for the summary. Partial: cost cut with no harm measurement.

**Example:** Invented table: 2,000 A, 8,000 B, 40,000 C series; every series costs 10 units a run, 4 runs a month, so 2,000,000 units. P2 moves only the tail to a cheap model: it saves 68 percent and adds a small stock-out cost (4,000 units, mostly in the tail). P1 saves 50 percent but adds 18,400 because it also slows the A items. P3 saves 82 percent for 8,200 extra. All three clear 40 percent, so I pick the one with the smallest harm: P2. Compute and stock-out units must be converted by finance before comparing them in one currency; here they stay abstract.

**Code:** run with `python3 -I q38.py`. Everything is invented.
```python
# Q38: tiered forecasting compute policies; invented table. Units abstract.
tiers = {  # share of series, cost per series-run (compute units), stock-out cost per series per period at current policy
 "A_fast":  dict(n=2000,  cost=10.0, so=50.0),
 "B_mid":   dict(n=8000,  cost=10.0, so=8.0),
 "C_tail":  dict(n=40000, cost=10.0, so=0.5),
}
runs_per_month = 4
base_cost = sum(t["n"] * t["cost"] * runs_per_month for t in tiers.values())
# policy: (cost multiplier per tier, relative stock-out increase per tier)
policies = {
 "P1 retrain all less often (4->2/mo)": {"A_fast": (0.5, 0.10), "B_mid": (0.5, 0.10), "C_tail": (0.5, 0.10)},
 "P2 tail -> global/cheap model":        {"A_fast": (1.0, 0.0),  "B_mid": (1.0, 0.0),  "C_tail": (0.15, 0.20)},
 "P3 tiered: A as-is, B 2/mo, tail cheap + 1/mo": {"A_fast": (1.0, 0.0), "B_mid": (0.5, 0.05), "C_tail": (0.15 * 0.5, 0.25)},
}
print(f"base compute {base_cost:.0f}; base stock-out cost {sum(t['n']*t['so'] for t in tiers.values()):.0f} per period")
best = None
for name, p in policies.items():
    comp = sum(tiers[k]["n"] * tiers[k]["cost"] * runs_per_month * p[k][0] for k in tiers)
    extra = sum(tiers[k]["n"] * tiers[k]["so"] * p[k][1] for k in tiers)
    saved = base_cost - comp
    print(f"{name:50s} saved {saved/base_cost*100:5.1f}%  extra stock-out {extra:8.0f}  saved per extra {saved/max(extra,1):6.2f}  meets 40%: {saved/base_cost>=0.40}")
    if saved / base_cost >= 0.40 and (best is None or extra < best[1]): best = (name, extra)
print("pick:", best[0])
```

**Output (my run):**
```
base compute 2000000; base stock-out cost 184000 per period
P1 retrain all less often (4->2/mo)                saved  50.0%  extra stock-out    18400  saved per extra  54.35  meets 40%: True
P2 tail -> global/cheap model                      saved  68.0%  extra stock-out     4000  saved per extra 340.00  meets 40%: True
P3 tiered: A as-is, B 2/mo, tail cheap + 1/mo      saved  82.0%  extra stock-out     8200  saved per extra 200.00  meets 40%: True
pick: P2 tail -> global/cheap model
```

**Follow-ups:**
- *What if leadership insists on more than 40 percent?* Show the marginal stock-out cost per extra point saved; P3 is the next step.
- *How do you detect harm after launch?* Track stock-outs per tier with an alert against the backtest.
- *New products?* Keep them in the high tier until they have history.

**Common mistakes:**
- Cutting uniformly across all series.
- Judging by MAPE only.
- No rollback path for the policy.

### Q39 ⭐ 🔴 [Set L, Q4 of 4, 12 min, 40 pts] LLM boundary threat model. An internal assistant has retrieval over HR documents, can call a ticketing tool and uses a hosted model (invented). Build the platform-level threat model: prompt injection through retrieved text (Book 2 owns the technique), over-broad tool permissions, data exfiltration through logs and answers, cross-user retrieval leaks, key theft and supply-chain risks (OWASP LLM entries, hedged). Show the platform controls: identity-propagated retrieval, tool scopes, output filtering, network egress limits, redaction, audit. Reference Part 10 Q42 and Part 11 Q31. Encode the table in Python and test that every threat has a control and an owner.
**Asked at:** OWASP Top 10 for LLM Applications 2025 summaries (opensourcesecurity substack, Trend Micro, HackerOne, Bright Security, Coralogix; search snippets only, not opened): supply chain moved to LLM03, data and model poisoning LLM04, model theft folded out of the standalone list; no source on classic ML model-extraction attacks surfaced, so extraction questions rest on general knowledge, hedged | LLM and GPU inference cost guides (Cast AI, Morph, DataCamp, machinelearningatscale.com, an alpeshnakrani.com playbook; search snippets only, not opened; vendor-authored figures such as utilisation percentages are one vendor's data and are NOT reused here); practitioner blogs, not interview reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** I assume the model can be tricked, so the platform limits what a tricked model can reach: user identity on retrieval, narrow tool scopes, redaction and egress limits, and an audit trail with an owner for every threat.

**Then explain:**
- Threats (Book 2 owns injection technique; OWASP LLM Top 10 2025 entries as summarised by commentators, check the current list): prompt injection through retrieved HR text, over-broad tool permission, exfiltration through logs and answers, cross-user retrieval leak, key theft, supply-chain risk in models and libraries.
- Controls: identity-propagated retrieval so the search filters by the caller's groups; the ticket tool can only create tickets, with the user's identity; output filtering and an egress allow-list; redaction before logging; short-lived keys in a secret manager; pinned and scanned dependencies. See Part 10 Q42 and Part 11 Q31 for the cloud mechanics.
- Failure modes: an ACL filter applied after ranking instead of before, logs that keep full prompts, a tool with a write scope 'just in case'.
- Scoring note [Set L, Q4 of 4, 12 min, 40 pts]: about 12 for scoping and assumptions, 12 for a table where each threat has a control, 8 for residual risk and cost, 4 for the check, 4 for the summary. Partial: controls listed with no owner.

**Example:** Documents d1 (HR only), d2 (everyone), d3 (payroll). An HR user should retrieve d1 and d2, never d3; the test asserts exactly that. A row with an empty control and owner is rejected by the validator.

**Code:** run with `python3 -I q39.py`. Table and ACL data are invented.
```python
# Q39: LLM boundary threat model; every threat needs a control and an owner.
M = [
 ("prompt injection via retrieved HR text", "tool call is low-priv; human approval for writes; retrieved text marked untrusted", "platform security"),
 ("over-broad ticketing tool permission", "tool scope = create ticket only, per-user identity", "platform team"),
 ("data exfil via logs", "redact PII before logging; log retention limit", "data protection office"),
 ("data exfil via answers", "output filter + egress allow-list", "platform security"),
 ("cross-user retrieval leak", "identity-propagated retrieval, ACL filter at query time", "search/RAG team"),
 ("API key theft", "secret manager, short-lived creds, rotation", "platform team"),
 ("supply-chain (model/lib)", "pinned hashes, signed artifacts, scan in CI", "platform security"),
]
def validate(rows):
    errs = [r[0] for r in rows if not r[1].strip() or not r[2].strip()]
    assert not errs, errs
    return len(rows)
print("threats with control and owner:", validate(M))
for r in M: print(f"- {r[0]:40s} owner: {r[2]}")
try: validate(M + [("model weights leaked", "", "")])
except AssertionError as e: print("rejected incomplete row:", e)
# tiny retrieval ACL test
docs = [("d1", {"hr"}), ("d2", {"all"}), ("d3", {"payroll"})]
def retrieve(groups): return [d for d, acl in docs if acl & (groups | {"all"})]
assert retrieve({"hr"}) == ["d1", "d2"] and "d3" not in retrieve({"hr"})
print("ACL test ok: hr user sees", retrieve({"hr"}))
```

**Output (my run):**
```
threats with control and owner: 7
- prompt injection via retrieved HR text   owner: platform security
- over-broad ticketing tool permission     owner: platform team
- data exfil via logs                      owner: data protection office
- data exfil via answers                   owner: platform security
- cross-user retrieval leak                owner: search/RAG team
- API key theft                            owner: platform team
- supply-chain (model/lib)                 owner: platform security
rejected incomplete row: ['model weights leaked']
ACL test ok: hr user sees ['d1', 'd2']
```

**Follow-ups:**
- *Can you filter injection out?* Not reliably; design so success of the injection has limited reach.
- *Who owns each row?* One named team, reviewed quarterly.
- *Hosted model data use?* Check the provider's current terms and retention settings.

**Common mistakes:**
- One shared service identity for all users.
- Relying on the system prompt as a security control.
- Threat list without owners.

### Q40 ⭐ 🔴 [Set E, Q4 of 4, 12 min, 40 pts] Edge security and cost. The on-device model file is extractable from the app package and a cloned app can abuse your fallback API (invented). Discuss model protection options and their limits (obfuscation, encryption with hardware key stores, server-side-only for high-value models), update-channel signing, app attestation at concept level, abuse limits on the fallback API, and cost of telemetry and updates across 100,000 devices. Reference Part 7 Q32 and Part 6 Q39. Verify an Ed25519 or HMAC signed model manifest in Python and show a tampered file being rejected.
**Asked at:** OWASP Top 10 for LLM Applications 2025 summaries (opensourcesecurity substack, Trend Micro, HackerOne, Bright Security, Coralogix; search snippets only, not opened): supply chain moved to LLM03, data and model poisoning LLM04, model theft folded out of the standalone list; no source on classic ML model-extraction attacks surfaced, so extraction questions rest on general knowledge, hedged | ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Anything shipped to a device can be extracted, so I protect the update channel with signatures, keep high-value models on the server, and rate-limit the fallback API per attested device.

**Then explain:**
- Model protection and its limits: obfuscation and encryption slow an attacker but the model must be decrypted to run; hardware key stores raise the bar; a model whose theft is costly stays server-side. Be honest: no on-device scheme is unbreakable.
- Update channel: sign a manifest holding the version and the file hash with a private key held in a key service; the app ships only the public key. See Part 7 Q32 for SBOM, signing and provenance and Part 6 Q39 for model API security.
- App attestation (concept only, check platform docs): the platform vouches that the request comes from a genuine app on a genuine device; use it to gate the fallback API with per-device quotas.
- Cost: telemetry and updates across 100,000 devices; delta updates and sampling cut traffic.
- Failure modes: replay of an old valid manifest (rollback attack), key leakage, a cloned app burning the fallback budget.
- Scoring note [Set E, Q4 of 4, 12 min, 40 pts]: about 12 for threat assumptions, 12 for a layered design, 8 for limits and cost, 4 for the signature check, 4 for the summary. Partial: 'encrypt the model' as the only answer.

**Example:** A good manifest is accepted. A model file with one extra byte is rejected by the hash. An edited manifest (version changed) is rejected by the signature. An old valid manifest still verifies, so the app must also require a version above the installed one. The key here is generated in memory for the demo (a fake key, not a real one).

**Code:** run with `python3 -I q40.py` (uses the `cryptography` package, version 50.0.1 here; HMAC from the standard library works if you share a secret, but then devices can forge).
```python
# Q40: Ed25519 signed model manifest; tampered file rejected. Fake demo key generated in memory.
import hashlib, json
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.exceptions import InvalidSignature
sk = Ed25519PrivateKey.generate(); pk = sk.public_key()   # in real life the private key lives in an HSM/KMS, the app ships only pk
model = b"fake-onnx-bytes" * 10
manifest = {"name": "fieldnet", "version": 7, "sha256": hashlib.sha256(model).hexdigest(), "min_app": "3.1"}
payload = json.dumps(manifest, sort_keys=True).encode(); sig = sk.sign(payload)
def verify(manifest, sig, blob):
    p = json.dumps(manifest, sort_keys=True).encode()
    try: pk.verify(sig, p)
    except InvalidSignature: return "REJECT bad signature"
    if hashlib.sha256(blob).hexdigest() != manifest["sha256"]: return "REJECT hash mismatch"
    return "ACCEPT"
print("good:", verify(manifest, sig, model))
print("tampered model:", verify(manifest, sig, model + b"x"))
m2 = dict(manifest, version=6); print("rollback manifest edited:", verify(m2, sig, model))
# note: replay of an old VALID manifest still passes; add a monotonic version check
installed = 7
old = dict(manifest, version=5); old_sig = sk.sign(json.dumps(old, sort_keys=True).encode())
print("old valid manifest signature ok:", verify(old, old_sig, model), "-> app must also require version > installed:", old["version"] > installed)
# telemetry/update cost, abstract
devices = 100_000; model_mb = 8; updates_per_year = 6; delta_ratio = 0.2
full = devices * model_mb * updates_per_year; delta = full * delta_ratio
print(f"update traffic units: full {full} MB-units, delta {delta:.0f} ({delta/full:.0%})")
```

**Output (my run):**
```
good: ACCEPT
tampered model: REJECT hash mismatch
rollback manifest edited: REJECT bad signature
old valid manifest signature ok: ACCEPT -> app must also require version > installed: False
update traffic units: full 4800000 MB-units, delta 960000 (20%)
```

**Follow-ups:**
- *HMAC or Ed25519?* Ed25519: devices hold only the public key, so they cannot forge updates.
- *Can you stop extraction?* No, only raise cost; watermark outputs and monitor API abuse.
- *Telemetry cost?* Sample, batch, compress; send aggregates.

**Common mistakes:**
- Embedding the signing key in the app.
- Verifying the signature but not the version.
- Unlimited fallback API per install.

### Q41 ⭐ 🔴 [Build versus buy] A bank-owned GCC (invented) debates building an in-house ML platform, adopting a managed cloud platform (Part 10, Part 11) or buying a commercial MLOps product. Build the decision framework: capabilities and team size, lock-in (Part 11 Q32), compliance fit, total cost of ownership with ongoing maintenance and on-call, exit plan and the criteria that would change the decision. Compute a three-year relative total cost comparison with invented unit costs and sensitivity to team size, and list what you would pilot first. No real prices.
**Asked at:** Job-posting and community patterns for MLOps, platform and ML-engineering roles at Indian GCCs, product companies and IT-services firms and at global product companies; inferred from search snippets about system-design and FinOps rounds, not from a verified company report | ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | MLOps maturity and tech-debt sources (ZenML maturity-models post, NannyML '5 levels of MLOps maturity', Towards Data Science, arXiv 2503.15577; search snippets only, not opened): Google levels 0 to 2 (manual, pipeline automation, full CI/CD) and Microsoft's five levels as reported secondhand; the Sculley et al. 2015 'Hidden technical debt' paper itself was not found, so only the commonly cited ideas are used
**Say this first (1 line):** I decide by capabilities, team size, compliance fit and exit cost first, then compare three-year relative cost with sensitivity, and pilot the managed option on one real model before committing.

**Then explain:**
- Framework: required capabilities (registry, pipelines, serving, monitoring), team size and skills, lock-in (Part 11 Q32), compliance and residency fit (Part 10, Part 11), total cost including upgrades, on-call and people time, an exit plan, and what would change the decision.
- Cost shape in my toy model: build has low per-model cost but high people cost; managed has higher per-model cost and low people cost; buy adds a licence. With few models and a small team, managed wins; with many models, build overtakes.
- Failure modes: counting build cost without maintenance and on-call, ignoring that the platform team is also a product team, picking a tool the compliance team cannot approve.
- Pilot first: one model end to end on the managed platform, measuring time to first deploy, audit evidence available and team hours.
- Scoring note [Not a timed set]: full marks need criteria plus a computed comparison with sensitivity; partial for a pros-and-cons list.

**Example:** Read the output: at 20 models and 4 people, build is cheapest in the toy numbers (81.0 vs 84.5); at 8 people managed wins. At 400 models build wins at every team size shown. No real prices were used; all values are abstract units.

**Code:** run with `python3 -I q41.py`.
```python
# Q41: 3-year relative TCO, invented units; sensitivity to team size.
def tco(kind, team, models, years=3):
    p = dict(
     build  =dict(upfront=6*team,  run_infra=10+0.05*models, license=0,  eng_per_year=lambda t: t*1.0, oncall=4),
     managed=dict(upfront=2*team,  run_infra=16+0.30*models, license=0,  eng_per_year=lambda t: t*0.5, oncall=1.5),
     buy    =dict(upfront=1.5*team,run_infra=12+0.10*models, license=14+0.30*models, eng_per_year=lambda t: t*0.4, oncall=1.5))[kind]
    per_year = p["run_infra"] + p["license"] + p["eng_per_year"](team) + p["oncall"]
    return p["upfront"] + years * per_year
for models in [20, 100, 400]:
    print(f"--- {models} models in production")
    print(f"{'team':>5s}{'build':>8s}{'managed':>9s}{'buy':>7s}  cheapest")
    for team in [4, 8, 16]:
        r = {k: tco(k, team, models) for k in ("build", "managed", "buy")}
        print(f"{team:>5d}{r['build']:8.1f}{r['managed']:9.1f}{r['buy']:7.1f}  {min(r, key=r.get)}")
# lock-in: exit cost as a share of year-3 run cost
print("exit-cost units: build 0, managed 12, buy 18  (invented; re-platforming effort)")
print("criterion that flips: if compliance forbids the managed service region, managed drops out")
```

**Output (my run):**
```
--- 20 models in production
 team   build  managed    buy  cheapest
    4    81.0     84.5  117.3  build
    8   117.0     98.5  128.1  managed
   16   189.0    126.5  149.7  managed
--- 100 models in production
 team   build  managed    buy  cheapest
    4    93.0    156.5  213.3  build
    8   129.0    170.5  224.1  build
   16   201.0    198.5  245.7  managed
--- 400 models in production
 team   build  managed    buy  cheapest
    4   138.0    426.5  573.3  build
    8   174.0    440.5  584.1  build
   16   246.0    468.5  605.7  build
exit-cost units: build 0, managed 12, buy 18  (invented; re-platforming effort)
criterion that flips: if compliance forbids the managed service region, managed drops out
```

**Follow-ups:**
- *What changes your mind?* A region or compliance restriction, a big jump in model count, or a vendor price change (check current terms).
- *Exit plan?* Keep artefacts and metadata in open formats and test an export.
- *Hybrid?* Managed training and registry with your own serving is common; check lock-in per layer.

**Common mistakes:**
- Comparing licence cost with engineer time only.
- No sensitivity analysis.
- Ignoring on-call.

### Q42 ⭐ 🔴 [ML technical-debt audit] Take a 3-year-old churn pipeline (invented) with glue code, 600 unused features, undeclared consumers, pipeline jungles, config sprawl and a model nobody dares retrain. Using the ideas from Hidden Technical Debt in ML Systems (Part 1 Q39; paper not opened here), propose a debt audit: what you measure, how you prioritise by risk and cost, what you delete first and how you protect against regression. Build a small feature-usage audit in Python on an invented lineage table that finds unused features and undeclared consumers.
**Asked at:** MLOps maturity and tech-debt sources (ZenML maturity-models post, NannyML '5 levels of MLOps maturity', Towards Data Science, arXiv 2503.15577; search snippets only, not opened): Google levels 0 to 2 (manual, pipeline automation, full CI/CD) and Microsoft's five levels as reported secondhand; the Sculley et al. 2015 'Hidden technical debt' paper itself was not found, so only the commonly cited ideas are used | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Measure what is actually read and by whom, delete the unused first, declare the undeclared consumers before touching anything they depend on, and add tests so deletion cannot silently break a model.

**Then explain:**
- Audit measures: feature read counts by consumer, features with no reader, consumers not in the declared list, config files per pipeline, pipeline stages with no owner, last retrain date. Ideas follow Hidden Technical Debt in ML Systems (Part 1 Q39); I did not open the paper here, so I describe them in my own words.
- Prioritise by risk times cost: an undeclared consumer on a critical feature is high risk; 600 unused features are low risk but cost storage and compute.
- Delete order: unused features first (in batches, with a one-release grace period), then duplicate config, then glue code; never delete a feature with an undeclared reader until the reader is declared.
- Protect: golden-set prediction test before and after each deletion, a data contract per feature, a retrain drill so the model is no longer one nobody dares retrain.
- Scoring note [Not a timed set]: full marks need a risk-ordered plan and the regression guard; partial for a general 'clean up' list.

**Example:** 20 invented features: 8 are read by someone, 12 are unused. Feature f003 is read by `promo_svc`, which is not a declared consumer, and f011 is read by two undeclared consumers. Deleting f003 would have broken promo_svc silently.

**Code:** run with `python3 -I q42.py`.
```python
# Q42: feature usage audit on an invented lineage table.
features = [f"f{i:03d}" for i in range(1, 21)]
model_uses = {"churn_v3": {"f001","f002","f003","f004","f005","f006"}}
declared_consumers = {"f001": {"churn_v3"}, "f002": {"churn_v3"}, "f003": {"churn_v3"}, "f004": {"churn_v3"}, "f005": {"churn_v3"}, "f006": {"churn_v3"}, "f010": {"retention_dash"}}
# read log (who actually reads which feature), invented
reads = [("churn_v3", f) for f in model_uses["churn_v3"]] + [("retention_dash", "f010"), ("promo_svc", "f003"), ("promo_svc", "f011"), ("fin_report", "f011")]
actual = {}
for who, f in reads: actual.setdefault(f, set()).add(who)
unused = [f for f in features if f not in actual]
undeclared = {f: sorted(actual[f] - declared_consumers.get(f, set())) for f in actual if actual[f] - declared_consumers.get(f, set())}
print(f"features {len(features)}, read by anyone {len(actual)}, unused {len(unused)}")
print("unused:", unused)
print("undeclared consumers:", undeclared)
assert "f011" in undeclared and "f003" in undeclared and "f020" in unused
# delete order: unused first, then risk by (consumers undeclared) -> do not delete; declare them
print("delete first (no readers):", unused[:5], "...; DO NOT delete f003/f011 until promo_svc/fin_report declared")
```

**Output (my run):**
```
features 20, read by anyone 8, unused 12
unused: ['f007', 'f008', 'f009', 'f012', 'f013', 'f014', 'f015', 'f016', 'f017', 'f018', 'f019', 'f020']
undeclared consumers: {'f003': ['promo_svc'], 'f011': ['fin_report', 'promo_svc']}
delete first (no readers): ['f007', 'f008', 'f009', 'f012', 'f013'] ...; DO NOT delete f003/f011 until promo_svc/fin_report declared
```

**Follow-ups:**
- *How do you find undeclared consumers?* Read logs or access logs on the store, not documentation.
- *Retrain fear?* Retrain in shadow, compare to the golden set, then promote.
- *Where to start?* Where an outage would hurt most.

**Common mistakes:**
- Deleting by name or guess.
- No grace period.
- Fixing code but leaving the lineage table stale.

### Q43 ⭐ 🔴 [Multi-region and active-active serving] A payments-adjacent scoring service must survive the loss of a cloud Region (invented). Compare active-passive, active-active and per-Region independent deployments for the model, features, registry and decision log, including state consistency, data residency, failover testing and the cost of idle capacity. Reference Part 11 Q33, Part 6 Q38 and Part 9 Q32. Simulate failover in Python with replication lag and report the stale-feature window and lost decisions for each design.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Job-posting and community patterns for MLOps, platform and ML-engineering roles at Indian GCCs, product companies and IT-services firms and at global product companies; inferred from search snippets about system-design and FinOps rounds, not from a verified company report | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** I pick the design by the loss I can accept: active-active loses least but costs headroom and needs a residency check, active-passive is cheaper but slower to recover, per-region independent has no stale state but no cover for a region's users.

**Then explain:**
- Active-passive: warm standby, async replication; recovery time includes detection and switch (Part 11 Q33 for multi-cloud architecture trade-offs, Part 6 Q38 for zero-downtime deploys). Stale window equals replication lag.
- Active-active: both Regions serve; the failed Region's half sees errors until health checks react; features replicated asynchronously.
- Per-Region independent: no cross-Region state so no lag, but a Region loss takes its users down unless traffic can move.
- State: feature store replication and its lag (Part 9 Q32 covers pipeline effects end to end), registry artefacts copied ahead of time, decision log per Region with a merge for audit. Residency may forbid replicating some data to another Region; check the law and your policy.
- Test failover on a schedule; a plan never exercised is not a plan. Idle capacity is the cost of the faster designs.
- Scoring note [Not a timed set]: full marks need the three designs, the numbers from the simulation and the residency caveat; partial for a table with no consistency discussion.

**Example:** At 200 decisions per second: with 150 s to detect and switch, active-passive loses 30,000 requests (200 x 150); active-active loses 3,000; per-Region independent loses half the traffic for the assumed 1 hour outage (360,000) because no one covers the failed Region. Stale windows come from lag, with seeded jitter.

**Code:** run with `python3 -I q43.py`. The model is a hand-made simplification with invented timings, sandbox only.
```python
# Q43: failover simulation with replication lag. Seeded. Abstract time in seconds.
import random
random.seed(43)
TPS = 200            # decisions per second
def sim(design, lag_s, detect_s, switch_s, fail_t=1000, horizon=1200):
    lost = stale_until = 0; served_stale = 0
    down = detect_s + switch_s
    if design == "active-passive":   # warm standby, async replication
        lost = int(TPS * down)                       # decisions with no answer while failing over
        stale_window = lag_s                         # feature writes not yet replicated
        decisions_log_lost = int(TPS * lag_s)        # log entries not replicated
    elif design == "active-active":  # both serve; traffic shifts, shared async feature replication
        lost = int(TPS * detect_s * 0.5)             # half of traffic sees errors until health check
        stale_window = lag_s
        decisions_log_lost = int(TPS * lag_s * 0.5)  # only the failed region's share
    else:                            # per-region independent: no cross-region state, no cross-region cover
        lost = int(TPS * 0.5 * 3600)               # failed region's users stay down for an assumed 1 h until it returns
        stale_window = 0                             # each region has its own features, no replica lag
        decisions_log_lost = 0                       # regional log stays; but users pinned there are down w/o failover
    return lost, stale_window, decisions_log_lost
print(f"{'design':26s}{'lost reqs':>10s}{'stale win s':>12s}{'log entries lost':>18s}  idle capacity")
idle = {"active-passive": "high (standby ~100%)", "active-active": "low (headroom ~ 50%)", "per-region independent": "low, but no cross-region cover"}
for d in idle:
    jitter = random.uniform(0.9, 1.1)
    r = sim(d, lag_s=5 * jitter, detect_s=30, switch_s=120 if d == "active-passive" else 10)
    print(f"{d:26s}{r[0]:>10d}{r[1]:>12.1f}{r[2]:>18d}  {idle[d]}")
print("residency: per-region independent keeps data in region; replication across regions needs a residency check")
```

**Output (my run):**
```
design                     lost reqs stale win s  log entries lost  idle capacity
active-passive                 30000         4.5               907  high (standby ~100%)
active-active                   3000         5.2               519  low (headroom ~ 50%)
per-region independent        360000         0.0                 0  low, but no cross-region cover
residency: per-region independent keeps data in region; replication across regions needs a residency check
```

**Follow-ups:**
- *Fail-open during failover?* Same per-class rule as the fraud incident.
- *Why keep decision logs per Region?* Residency and independence; merge later for audit.
- *How often to test?* Per quarter at least; more often for critical services.

**Common mistakes:**
- Assuming replication is instant.
- Forgetting the registry and secrets in the DR Region.
- Never running the failover.

### Q44 ⭐ 🔴 [Agent and prompt-injection boundary] An agent platform lets LLM agents call internal tools with a service identity (invented). Without teaching prompt-injection techniques (Book 2), define the platform security boundary: per-agent identities and scopes, human approval for write actions, sandboxed execution, egress allow-lists, secrets never in context, rate and spend limits and audit logs of tool calls. Reference Part 10 Q3, Part 10 Q8 and Part 11 Q31. Reuse the IAM evaluator sketch in scratch/B4P10_wavea/iam_eval_sketch.py to show an agent role being denied a write action it was not granted.
**Asked at:** OWASP Top 10 for LLM Applications 2025 summaries (opensourcesecurity substack, Trend Micro, HackerOne, Bright Security, Coralogix; search snippets only, not opened): supply chain moved to LLM03, data and model poisoning LLM04, model theft folded out of the standalone list; no source on classic ML model-extraction attacks surfaced, so extraction questions rest on general knowledge, hedged | LLM and GPU inference cost guides (Cast AI, Morph, DataCamp, machinelearningatscale.com, an alpeshnakrani.com playbook; search snippets only, not opened; vendor-authored figures such as utilisation percentages are one vendor's data and are NOT reused here); practitioner blogs, not interview reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** I give each agent its own identity with the smallest scopes, make write actions go through human approval, and enforce those limits in the platform, not in the prompt.

**Then explain:**
- Boundary: per-agent identity and scopes (Part 10 Q3, Part 10 Q8), human approval for write actions, sandboxed code execution, egress allow-lists, secrets never placed in the model context, rate and spend limits, audit logs of every tool call (Part 11 Q31 for the LLM boundary on Azure and GCP).
- Technique of injection is Book 2; here I only assume the agent may be steered, so its credentials cannot do harm.
- Failure modes: one shared service identity for all agents, tools with wildcard actions, a secret pasted into a prompt or a log, approval fatigue (users click yes always).
- Evaluator limits: my sketch handles allow, deny, wildcards, boundaries, SCPs and session policies; it does not model NotAction, policy variables or all cross-account rules. Check current docs and use a real policy simulator for production.
- Scoring note [Not a timed set]: full marks need identities, approval, egress and audit plus a demonstrated denial; partial for 'be careful with prompts'.

**Example:** The read-only agent role can GetItem but PutItem is denied (nothing allows it). After approval a separate role may PutItem. DeleteItem is denied for both because the boundary does not include it; an explicit deny guard beats even a broad allow.

**Code:** run with `cd code && python3 -I q44.py`; it imports an unmodified copy of `scratch/B4P10_wavea/iam_eval_sketch.py` kept next to it. Account id and table are fake.
```python
# Q44: agent role denied a write it was not granted, using a COPY of iam_eval_sketch.py (unmodified).
import sys; sys.path.insert(0, "."); from iam_eval_sketch import evaluate
A = lambda a, r="*", e="Allow": {"Version": "2012-10-17", "Statement": [{"Effect": e, "Action": a, "Resource": r}]}
tickets = "arn:aws:dynamodb:ap-south-1:111122223333:table/tickets"
agent_role = [A(["dynamodb:GetItem", "dynamodb:Query"], tickets)]          # read-only agent
approver_role = [A(["dynamodb:GetItem", "dynamodb:PutItem"], tickets)]     # used only after human approval
boundary = A(["dynamodb:GetItem", "dynamodb:Query", "dynamodb:PutItem"], tickets)
for who, pol in [("agent (read grant)", agent_role), ("approval-flow role", approver_role)]:
    for act in ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:DeleteItem"]:
        print(f"{who:20s} {act:22s} ->", evaluate(act, tickets, identity=pol, boundary=boundary))
assert evaluate("dynamodb:PutItem", tickets, identity=agent_role)[0] == "Deny"
# explicit deny guardrail beats any later allow
guard = A("dynamodb:DeleteItem", "*", "Deny")
print("with explicit deny guard, even an admin-ish allow:", evaluate("dynamodb:DeleteItem", tickets, identity=[A("dynamodb:*"), guard]))
# rate/spend limit and secret-in-context check (platform-level, toy)
import re
ctx = "summarise ticket 42. key=AKIAIOSFODNN7EXAMPLE"
print("secret in context?", bool(re.search(r"AKIA[0-9A-Z]{16}", ctx)), "-> block call")
```

**Output (my run):**
```
agent (read grant)   dynamodb:GetItem       -> ('Allow', 'identity or resource policy allows (same account)')
agent (read grant)   dynamodb:PutItem       -> ('Deny', 'implicit deny: nothing allows')
agent (read grant)   dynamodb:DeleteItem    -> ('Deny', 'implicit deny: outside permissions boundary')
approval-flow role   dynamodb:GetItem       -> ('Allow', 'identity or resource policy allows (same account)')
approval-flow role   dynamodb:PutItem       -> ('Allow', 'identity or resource policy allows (same account)')
approval-flow role   dynamodb:DeleteItem    -> ('Deny', 'implicit deny: outside permissions boundary')
with explicit deny guard, even an admin-ish allow: ('Deny', 'explicit deny')
secret in context? True -> block call
```

**Follow-ups:**
- *Who approves?* The data owner for that action; log approver and request.
- *Spend limit?* A per-agent budget with a hard stop and an alert.
- *Sandbox?* No network except the allow-list, short-lived, no host mounts.

**Common mistakes:**
- Wildcard tool permissions.
- Approval that cannot be audited.
- Putting secrets in context.

### Q45 ⭐ 🔴 [Unit economics and budgeting] Product asks for cost per prediction and a next-year budget for five models (invented usage growth). Build a unit-cost model (compute, storage, data transfer, monitoring, people time, idle capacity share) in abstract units, forecast with growth and a spike scenario, set alert thresholds (anomaly versus budget) and say how you answer 'is this model worth its cost' with Book 6 value metrics rather than the platform inventing them. Reference Part 10 Q44 and Part 8 Q39. Run the model in Python and produce a sensitivity table; no real prices.
**Asked at:** FinOps interview-prep material (TechTarget 'Prepare for your FinOps interview' 12-question tip, hirevire FinOps and cloud-cost prescreening lists, a devopsboys FinOps roadmap; search snippets only, not opened, WebFetch of techtarget.com failed with getaddrinfo ENOTFOUND); generic cloud-cost question families (tagging, showback and chargeback, spot, idle resources, budgeting), none GPU-specific, not verified company reports | Job-posting and community patterns for MLOps, platform and ML-engineering roles at Indian GCCs, product companies and IT-services firms and at global product companies; inferred from search snippets about system-design and FinOps rounds, not from a verified company report | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Cost per prediction is compute (including the idle share) plus storage, transfer, monitoring and people time divided by predictions; I forecast it with growth and a spike, alert on both budget and anomaly, and leave value to the Book 6 owner.

**Then explain:**
- Inputs per model: predictions, compute per thousand, idle share, storage, transfer, monitoring, people. Idle capacity is paid and spread over used predictions (Part 10 Q44 for cost levers on AWS, Part 8 Q39 for the monitoring cost).
- Low-volume models look expensive per prediction because fixed costs dominate (m4 in my run); that is a signal, not an error.
- Alerts: a budget threshold (monthly budget plus a margin) catches slow creep; an anomaly rule (against a trailing mean) catches spikes early.
- 'Is it worth it?': ask the product owner for value per prediction or per outcome (Book 6), then compare. The platform team supplies cost, not value.
- Failure modes: allocating shared platform cost unfairly, forgetting people time, forecasting growth with no spike case.
- Scoring note [Not a timed set]: full marks need the unit-cost build-up, forecast and sensitivity; partial for a single average.

**Example:** Five invented models. Cost per 1k predictions ranges from 0.25 (m3, high volume) to 14.5 (m4, 1 million predictions a month). A 3x spike in month 6 trips both alerts. Sensitivity: compute rate +50 percent gives 1.461x total, idle +20 points gives 1.412x, people +20 percent only 1.015x.

**Code:** run with `python3 -I q45.py`. All figures are invented abstract units, no prices.
```python
# Q45: unit cost model, 5 models, growth and spike, thresholds, sensitivity. Abstract units.
models = {  # monthly predictions, compute/1k, storage, transfer, monitoring, people, idle share
 "m1": dict(preds=50e6, c1k=0.8, stor=20, xfer=10, mon=5, ppl=3000, idle=0.30),
 "m2": dict(preds=5e6,  c1k=2.0, stor=5,  xfer=2,  mon=5, ppl=3000, idle=0.50),
 "m3": dict(preds=200e6,c1k=0.2, stor=40, xfer=30, mon=8, ppl=3000, idle=0.15),
 "m4": dict(preds=1e6,  c1k=5.0, stor=2,  xfer=1,  mon=5, ppl=2000, idle=0.60),
 "m5": dict(preds=20e6, c1k=1.0, stor=10, xfer=5,  mon=5, ppl=2500, idle=0.25),
}
def monthly(m, growth=0.0, mult=1.0):
    p = m["preds"] * (1 + growth) * mult
    comp = p / 1000 * m["c1k"]; comp *= 1 / (1 - m["idle"])       # idle capacity is paid, spread over used
    return comp + m["stor"] + m["xfer"] * (1 + growth) * mult + m["mon"] + m["ppl"], p
print(f"{'model':6s}{'cost/mo':>10s}{'cost per 1k preds':>20s}")
tot = 0
for k, m in models.items():
    c, p = monthly(m); tot += c; print(f"{k:6s}{c:10.1f}{c/p*1000:20.4f}")
print(f"total/month {tot:.1f}")
# forecast: 2%/month growth for 12 months, plus spike (3x for 1 month in month 6)
budget = 0; series = []
for mth in range(1, 13):
    g = 1.02 ** mth - 1; mult = 3.0 if mth == 6 else 1.0
    c = sum(monthly(m, g, mult)[0] for m in models.values()); series.append(c)
budget = sum(sum(monthly(m, 1.02 ** x - 1)[0] for m in models.values()) for x in range(1, 13))
print(f"year budget (no spike) {budget:.0f}; with spike {sum(series):.0f}; spike month {series[5]:.0f}")
alert_budget = budget / 12 * 1.15
print("budget alert threshold per month:", round(alert_budget, 1), "| anomaly rule: month > 1.5 x trailing 3-mo mean")
for mth, c in enumerate(series, 1):
    trail = sum(series[max(0, mth-4):mth-1]) / max(1, len(series[max(0, mth-4):mth-1]))
    if mth > 1 and (c > alert_budget or c > 1.5 * trail): print(f"  month {mth}: ALERT cost {c:.0f} (budget flag {c>alert_budget}, anomaly {c>1.5*trail})")
print("sensitivity of total/month to: idle +20pts / people +20% / compute/1k +50%")
def total(f): return sum(f(dict(m))[0] if False else monthly(f(dict(m)))[0] for m in models.values())
def idle_up(m): m["idle"] = min(0.9, m["idle"] + 0.2); return m
def ppl_up(m): m["ppl"] *= 1.2; return m
def c_up(m): m["c1k"] *= 1.5; return m
for n, f in [("idle", idle_up), ("people", ppl_up), ("compute/1k", c_up)]: print(f"  {n:11s} {total(f)/tot:5.3f} x base")
print("worth-its-cost: ask Book 6 owner for value per prediction, then value_per_pred > cost_per_pred")
```

**Output (my run):**
```
model    cost/mo   cost per 1k preds
m1       60177.9              1.2036
m2       23012.0              4.6024
m3       50136.8              0.2507
m4       14508.0             14.5080
m5       29186.7              1.4593
total/month 177021.3
year budget (no spike) 2398850; with spike 2766917; spike month 565705
budget alert threshold per month: 229889.8 | anomaly rule: month > 1.5 x trailing 3-mo mean
  month 6: ALERT cost 565705 (budget flag True, anomaly True)
sensitivity of total/month to: idle +20pts / people +20% / compute/1k +50%
  idle        1.412 x base
  people      1.015 x base
  compute/1k  1.461 x base
worth-its-cost: ask Book 6 owner for value per prediction, then value_per_pred > cost_per_pred
```

**Follow-ups:**
- *Showback or chargeback?* Start with showback to build trust; chargeback needs agreed tagging.
- *Biggest lever?* Idle share: raising utilisation often beats model tweaks.
- *Budget with uncertainty?* Give a base and a spike case, not one number.

**Common mistakes:**
- Excluding people and idle cost.
- One alert type.
- Platform inventing the value numbers.
