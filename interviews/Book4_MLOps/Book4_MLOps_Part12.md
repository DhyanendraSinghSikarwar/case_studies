# Book 4 — Part 12: Cost, scaling, security and MLOps system design (with timed mock sets)

**Topic:** cost control without price figures (FinOps tagging and attribution, showback and chargeback, right-sizing, idle GPUs, spot and preemptible capacity, batching, quantisation, caching, scale-to-zero, storage tiering, egress, unit economics and budgeting), scaling and capacity arithmetic (queues, backpressure, autoscaling, load shedding), security (secrets, least-privilege IAM, model and image supply chain, network isolation, PII and India data residency, model theft and extraction, policy as code, the agent and prompt-injection boundary at platform level), reliability (SLOs, rollback, disaster recovery, multi-Region, incident response), organisation (build versus buy, platform versus embedded teams, maturity, ML technical debt) and six timed end-to-end MLOps system-design sets (fraud detection, recommender, demand forecasting, regulated credit risk, LLM-serving boundary, edge and on-device)

**Target:** 45  |  **Actual:** 45 (⭐⭐⭐ 13, ⭐⭐ 19, ⭐ 13)  |  **Date:** 2026-10-26  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

How the sets work: there are 6 sets of 4 questions (24 of the 45 questions); the other 21 questions are standalone. Each set question is tagged `[Set F, Q1 of 4, 6 min, 10 pts]`. Questions are listed by star rating (⭐⭐⭐ first) as the book requires, so the four questions of a set are scattered through the file; to run a set as a mock, collect its tag. Inside a set, Q1 is the clarify-and-requirements warm-up (10 pts), Q2 the core design or capacity step (20 pts), Q3 the data, operations or governance step (30 pts) and Q4 the hard integrative step with failure, cost and security (40 pts): 100 points per set, 40 to 45 minutes. Suggested scoring per question: 30 percent for clarifying questions and stated assumptions, 30 percent for a design that meets the stated numbers (check the arithmetic), 20 percent for naming the failure modes, security and cost consequences, 10 percent for the runnable check (a short Python simulation, validator or table with assertions), 10 percent for a crisp spoken summary in under 60 seconds. Bands: 85 to 100 strong hire-style answer, 70 to 84 solid with gaps, 50 to 69 needs the weak parts reviewed, below 50 redo the linked earlier parts. Time budgets and bands are practice targets set by this book, not any company's published rules.

| Set | Theme | Questions | Time | Points |
|---|---|---|---|---|
| C | Regulated credit-risk platform (bank-owned GCC, India) | 4 | 45 min | 100 |
| D | Demand forecasting platform (retail replenishment) | 4 | 40 min | 100 |
| E | Edge and on-device inference (field app) | 4 | 40 min | 100 |
| F | Fraud detection platform (card and UPI-style payments) | 4 | 40 min | 100 |
| L | LLM-serving boundary (internal assistant, hosted model) | 4 | 40 min | 100 |
| R | Recommender platform (video home feed) | 4 | 40 min | 100 |

Scope note: this part integrates, it does not reteach. Part 1 owns Git and pytest; Part 2 Docker; Part 3 Kubernetes and Helm; Part 4 DVC, MLflow and registry; Part 5 pipelines and orchestration; Part 6 serving mechanics, latency, shadow, canary and rollout; Part 7 CI/CD and promotion gates; Part 8 monitoring, drift and alerting; Part 9 feature stores, Kafka and Spark; Part 10 AWS and SageMaker depth; Part 11 Azure ML, Vertex AI and cross-cloud comparison; Book 1 owns ML theory; Book 2 owns LLM and RAG internals and prompt-injection technique; Book 3 SQL; Book 6 product and business metrics. This part owns cost, scaling, security, reliability and organisation decisions across the stack and end-to-end design. Every prompt names the earlier question it builds on (cited as Part N Qn) and all 87 distinct references were checked by script against the headings of Book4_MLOps_Part01 to Part11. Part 12 is the last part of Book 4.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book4_Part12_sources.md). No page was found that reports exact system-design or FinOps questions asked by a named company, so 'Asked at' tags name source types (ML system-design guides and courses, FinOps prep lists, regulator and law-firm explainers, OWASP summaries, maturity-model posts, job-posting patterns), not verified company reports; set contents are expert designs. All numbers in the prompts are invented, no prices or salary figures are used, and Indian regulatory statements (RBI FREE-AI of 13 Aug 2025, DPDP Act and Rules, RBI payment-data direction, SEBI cloud framework) come from adviser snippets and are hedged 'check the regulator's site and current law'. Wave B may run only: Python cost and capacity arithmetic in abstract units, queue, autoscaling, spot and failover simulations with seeds, the simplified IAM evaluator sketch scratch/B4P10_wavea/iam_eval_sketch.py (it does not model all IAM rules), secret and pickle scanners, policy YAML validators (pyyaml and pydantic), hash-chained logs, signature checks, threat-model and controls tables, and a small ONNX export and quantisation. No cloud calls, no credentials, no prices.

---

### Q1 ⭐⭐⭐ 🟢 [Set F, Q1 of 4, 6 min, 10 pts] Fraud detection platform, clarify first. A payments company with 20 million card and UPI-style transactions a day (invented) wants real-time fraud scoring. Before drawing anything, list the questions you ask (decision at authorisation time or after, latency budget, who owns false positives, label delay, regulator and data-residency limits), the three numbers you want (peak transactions per second, fraud rate, cost of a missed fraud versus a blocked good customer) and the success metrics at model, service and business level. Turn the stated numbers into a one-page requirements table in Python and compute average and peak TPS for a 6x peak-to-average ratio.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Job-posting and community patterns for MLOps, platform and ML-engineering roles at Indian GCCs, product companies and IT-services firms and at global product companies; inferred from search snippets about system-design and FinOps rounds, not from a verified company report
**Say this first (1 line):** Before I draw anything I ask what the decision is, how fast, who owns false positives and how late the labels come, then I turn the numbers into a table: 20 million a day is about 231 TPS on average and about 1,389 TPS at a 6x peak.

**Then explain:**
- Questions I ask: is the score used at authorisation time (blocking) or after the fact? What is the latency budget for the model hop? Who owns a wrongly blocked good customer? How late do chargebacks arrive? Which regulator and data-residency limits apply (check current rules and the company policy)? What happens if the model is down: fail open or fail closed?
- Three numbers I want: peak TPS, fraud rate, and the cost of a missed fraud versus a blocked good customer. Without the cost ratio I cannot choose a threshold.
- Success metrics at three levels. Model: recall at a fixed review budget, precision, PR-AUC. Service: p99 latency, error rate, availability. Business: fraud loss, false-decline rate, analyst load.
- Failure modes: peak assumed too low (ratio is a guess, ask for the real busiest minute), labels delayed so recall looks worse than it is, nobody owns false positives.
- Scoring note (10 pts, Set F Q1, 6 min): full points for asking at least four of the clarifying questions, stating assumptions out loud, and getting 231 and 1,389 right with the 6x ratio shown. Partial (5-7) for good questions but arithmetic or metrics missing. Little credit for jumping to an architecture.

**Example:** 20,000,000 / 86,400 = 231.5 TPS average. Times 6 = 1,388.9 peak. If the interviewer later says "700 TPS peak", that means either a different daily volume (about 10 million) or a different ratio. Say so and ask, do not silently switch. (Note: Set F Q2 starts from 700 TPS; at 20 million a day and 6x the arithmetic gives about 1,389, so state which input you changed.)

**Code:**
```python
# Set F Q1: requirements table and TPS (invented inputs)
daily = 20_000_000
avg = daily / 86_400
peak = avg * 6
req = [
 ("daily transactions", daily),
 ("average TPS", round(avg, 1)),
 ("peak/avg ratio", 6),
 ("peak TPS", round(peak, 1)),
 ("p99 model-hop budget ms", 60),
 ("fraud rate", "0.1% (assumed)"),
]
for k, v in req: print(f"{k:28} {v}")
assert round(avg) == 231 and round(peak) == 1389
print("note: Q5 uses 700 TPS peak; that is the book's later figure, not this arithmetic")
```

**Output (my run):**
```text
daily transactions           20000000
average TPS                  231.5
peak/avg ratio               6
peak TPS                     1388.9
p99 model-hop budget ms      60
fraud rate                   0.1% (assumed)
note: Q5 uses 700 TPS peak; that is the book's later figure, not this arithmetic
```

**Follow-ups:**
- Why ask about label delay in a requirements round? Because it sets the retraining cadence and how you evaluate (Q8 of this set covers it).
- Why a peak ratio and not the average? Capacity is paid for at the peak and the p99 budget is broken at the peak.

**Common mistakes:** Starting with Kafka and boxes. Using average TPS for sizing. Giving only a model metric and no business metric. Not asking what happens when the scorer is down.

### Q2 ⭐⭐⭐ 🟢 [Set R, Q1 of 4, 6 min, 10 pts] Recommender platform, clarify first. A video app with 8 million daily users (invented) wants a home-feed recommender. Ask about the objective (watch time versus satisfaction versus creator fairness), cold-start share, freshness needs, candidate-generation then ranking stages, the latency budget and what a bad recommendation costs. Write the requirements as a table and compute daily feed requests and catalogue size from stated inputs (6 feed loads per user per day, 2 million items). Say which parts are Book 1 modelling and which are platform work.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Job-posting and community patterns for MLOps, platform and ML-engineering roles at Indian GCCs, product companies and IT-services firms and at global product companies; inferred from search snippets about system-design and FinOps rounds, not from a verified company report
**Say this first (1 line):** I clarify the objective first, because watch time, satisfaction and creator fairness pull in different directions; then 8 million users times 6 loads is 48 million feed requests a day, about 556 per second on average, over a 2 million item catalogue.

**Then explain:**
- Ask: what is the objective (watch time can reward clickbait; satisfaction needs surveys or proxies; creator fairness needs exposure rules)? What share of users and items are cold-start? How fresh must new items be (minutes or a day)? What is the latency budget? What does a bad recommendation cost (a skipped video versus an unsafe one)?
- Shape: candidate generation narrows 2 million items to hundreds, then ranking scores them, then re-ranking applies business rules and diversity. Stages exist because you cannot score 2 million items per request.
- Book 1 owns: model choice (two-tower, ranker loss, cold-start methods), offline metrics. Platform owns: feature stores, embedding index refresh, serving latency, A/B plumbing, rollback, logging for training.
- Failure modes: feedback loops (you only learn about what you showed), stale embeddings, peak at evening hours far above the average.
- Scoring note (10 pts, Set R Q1, 6 min): full for explicit objective trade-off, cold-start and freshness questions, correct 48M and about 556 rps, and a clear modelling-versus-platform split. Partial for a table without questions. Low if you only describe a model.

**Example:** 8,000,000 x 6 = 48,000,000 requests/day; /86,400 = 555.6 rps. If 70 percent of traffic lands in 4 evening hours (invented), the busy-hour rate is 2,333 rps, about 4x the average. Size for the busy hour.

**Code:**
```python
users=8_000_000; loads=6; items=2_000_000
daily=users*loads
avg=daily/86400
print("daily feed requests",daily)
print("avg feed rps",round(avg,1))
print("catalogue items",items)
# invented: 70% of daily requests in 4 busy hours
busy=daily*0.7/(4*3600)
print("busy-hour rps (70% in 4h, invented)",round(busy,1))
assert daily==48_000_000
```

**Output (my run):**
```text
daily feed requests 48000000
avg feed rps 555.6
catalogue items 2000000
busy-hour rps (70% in 4h, invented) 2333.3
```

**Follow-ups:**
- Which metric do you launch on? A guardrail set plus the main metric in an A/B test, not offline AUC alone.
- Where do you put exposure logs? In the training pipeline with the served position, so you can correct position bias later.

**Common mistakes:** Treating it as only a modelling question. Forgetting cold-start. One objective with no guardrails. Sizing on the average.

### Q3 ⭐⭐⭐ 🟢 [Set C, Q1 of 4, 8 min, 10 pts] Regulated credit-risk platform, clarify first. A bank-owned GCC in India (invented) will build a retail credit-scoring model used for loan decisions. List the constraints you ask about before design: who approves a model, explainability and adverse-action reasons, fairness review, audit trail and retention, data residency, where customer data may be processed, third-party and cloud outsourcing rules (hedge: check the RBI site and the bank's own policy), and independent validation. Write them as a requirements and controls table in YAML and validate it with pyyaml and a pydantic model.
**Asked at:** Coverage of the RBI FREE-AI framework of 13 Aug 2025 (law.asia, storyboard18, cxodigitalpulse, securiti, mitsloanme; search snippets only, not opened): seven principles, 26 recommendations in six pillars, board-approved AI policy, AI-specific audit, disclosures; no snippet gave model-risk or localisation text, so those parts are hedged 'check the RBI site'; regulated BFSI and GCC credit and fraud roles | ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports
**Say this first (1 line):** For a bank credit model I ask who approves, how declines are explained, how fairness is checked, what is logged and for how long, where data may live and who validates independently, and I keep these as a requirements and controls file that a script can validate.

**Then explain:**
- Controls to ask about: approval authority (model risk committee), explainability and reasons for a decline, fairness review, audit trail and retention, data residency and where processing is allowed, third-party and cloud outsourcing rules, independent validation.
- Hedge the regulation: RBI and bank policy rules change. Say "check the RBI site and the bank's own policy"; I do not quote circular text from memory.
- Put it in YAML with an owner and an evidence artefact per control, so every row answers "who" and "show me". A pydantic model plus a coverage check turns a forgotten control into a failed validation.
- Failure modes: a control with no owner, no evidence, or a whole area missing; requirements kept in a slide deck that nobody checks.
- Scoring note (10 pts, Set C Q1, 8 min): full for covering all seven areas, giving owners and evidence, hedging regulation and running a validator that rejects an incomplete file. Partial for a list without owners. Do not invent legal text.

**Example:** The sample file has 7 controls, one per area. Removing the validation row makes the validator fail with "missing areas ['validation']".

**Code:**
```python
import yaml
from pydantic import BaseModel, field_validator
from typing import List
DOC = """
model: retail_credit_score_v1
requirements:
  - {id: R1, area: approval, control: "Model risk committee approves before go-live", owner: model_risk, evidence: approval_minutes}
  - {id: R2, area: explainability, control: "Top reasons per decline stored with each decision", owner: ml_team, evidence: reason_code_log}
  - {id: R3, area: fairness, control: "Fairness review across agreed groups before approval", owner: model_risk, evidence: fairness_report}
  - {id: R4, area: audit, control: "Decision log kept for retention period set by bank policy", owner: compliance, evidence: log_retention_policy}
  - {id: R5, area: residency, control: "Customer data processed only in approved locations (check RBI site and bank policy)", owner: security, evidence: architecture_review}
  - {id: R6, area: outsourcing, control: "Cloud and third-party use follows bank outsourcing policy (check current rules)", owner: vendor_risk, evidence: vendor_assessment}
  - {id: R7, area: validation, control: "Independent team validates, not the builders", owner: validation_team, evidence: validation_report}
"""
AREAS={"approval","explainability","fairness","audit","residency","outsourcing","validation"}
class Req(BaseModel):
    id:str; area:str; control:str; owner:str; evidence:str
    @field_validator("area")
    @classmethod
    def ok(cls,v):
        if v not in AREAS: raise ValueError("unknown area "+v)
        return v
class Doc(BaseModel):
    model:str; requirements:List[Req]
    @field_validator("requirements")
    @classmethod
    def cover(cls,v):
        miss=AREAS-{r.area for r in v}
        if miss: raise ValueError(f"missing areas {sorted(miss)}")
        return v
d=Doc(**yaml.safe_load(DOC))
print("valid; requirements:",len(d.requirements))
for r in d.requirements: print(r.id,r.area,"->",r.owner,"/",r.evidence)
bad=yaml.safe_load(DOC); bad["requirements"]=bad["requirements"][:-1]
try: Doc(**bad)
except Exception as e: print("rejected incomplete doc:", e.errors()[0]["msg"])
```

**Output (my run):**
```text
valid; requirements: 7
R1 approval -> model_risk / approval_minutes
R2 explainability -> ml_team / reason_code_log
R3 fairness -> model_risk / fairness_report
R4 audit -> compliance / log_retention_policy
R5 residency -> security / architecture_review
R6 outsourcing -> vendor_risk / vendor_assessment
R7 validation -> validation_team / validation_report
rejected incomplete doc: Value error, missing areas ['validation']
```

**Follow-ups:**
- Why a pydantic model? It gives typed fields and clear error messages; the coverage rule is plain Python.
- Is this compliance? No. It is a checklist structure; legal review decides what is required.

**Common mistakes:** Quoting regulations from memory. Controls with no owner. Treating the builders as the independent validators.

### Q4 ⭐⭐⭐ 🟢 Cost visibility first. A shared ML platform has one cloud bill and four teams (invented) and nobody can say which model costs what. Design the tagging and attribution scheme (mandatory tags, allocation of shared costs such as the cluster, registry and feature store by usage or by fixed split, untagged residue), explain showback versus chargeback and when to move from one to the other, and write a Python allocator that takes an invented usage table plus a shared-cost pool and prints per-team cost with an assertion that allocations sum to the bill. No prices; use abstract cost units.
**Asked at:** FinOps interview-prep material (TechTarget 'Prepare for your FinOps interview' 12-question tip, hirevire FinOps and cloud-cost prescreening lists, a devopsboys FinOps roadmap; search snippets only, not opened, WebFetch of techtarget.com failed with getaddrinfo ENOTFOUND); generic cloud-cost question families (tagging, showback and chargeback, spot, idle resources, budgeting), none GPU-specific, not verified company reports | Job-posting and community patterns for MLOps, platform and ML-engineering roles at Indian GCCs, product companies and IT-services firms and at global product companies; inferred from search snippets about system-design and FinOps rounds, not from a verified company report
**Say this first (1 line):** Tag everything with team, model and environment, allocate shared costs by usage where you can measure it and by fixed split where you cannot, show the untagged residue openly, and prove the allocations sum to the bill.

**Then explain:**
- Mandatory tags: team, model or service, environment, cost-centre. Enforce at creation time with policy (no tag, no resource).
- Shared costs (cluster, registry, feature store): by measured usage (cluster-hours, lookups) when meters exist; fixed even split for small flat things like the registry. Say which rule you used so teams can argue with it.
- Untagged residue: do not hide it. Report it as its own line, then either spread in proportion to direct cost or assign to the platform team; track it as a metric that should fall.
- Showback means report the cost, no money moves. Chargeback means the team's budget is actually debited. Start with showback until tags are above a high coverage level and teams trust the numbers, then move to chargeback.
- Failure modes: allocations that do not sum to the bill, teams gaming tags, usage meters missing for shared services.

**Example:** Abstract units. Bill 2,000 = compute 1,000 + storage 300 + shared cluster 400 + registry 50 + feature store 150 + untagged 100. Tagged direct is 1,230 of the 1,300 compute+storage, so the residue is 70 + 100 = 170, spread by direct cost. Fraud ends at 782.5, reco 709.7, forecast 281.0, credit 226.8; total 2,000.

**Code:**
```python
# abstract cost units, invented usage
bill = {"compute":1000,"storage":300,"shared_cluster":400,"registry":50,"feature_store":150,"untagged":100}
direct = {  # tagged direct cost per team
 "fraud":{"compute":380,"storage":90},
 "reco":{"compute":330,"storage":120},
 "forecast":{"compute":120,"storage":50},
 "credit":{"compute":110,"storage":30},
}
usage = {"fraud":40,"reco":35,"forecast":15,"credit":10}   # share of cluster-hours
fs_use = {"fraud":50,"reco":30,"forecast":10,"credit":10}
pool_cluster=bill["shared_cluster"]; pool_reg=bill["registry"]; pool_fs=bill["feature_store"]
tagged_direct=sum(sum(v.values()) for v in direct.values())
untagged=bill["compute"]+bill["storage"]-tagged_direct+bill["untagged"]
print("tagged direct",tagged_direct,"untagged residue",untagged)
out={}
for t in direct:
    d=sum(direct[t].values())
    c=pool_cluster*usage[t]/sum(usage.values())
    r=pool_reg/len(direct)                      # fixed even split
    f=pool_fs*fs_use[t]/sum(fs_use.values())
    # untagged residue spread in proportion to direct cost
    u=untagged*d/tagged_direct
    out[t]=d+c+r+f+u
    print(f"{t:9} direct {d:5} cluster {c:6.1f} registry {r:5.1f} fs {f:6.1f} untagged {u:6.1f} total {out[t]:7.1f}")
total=sum(bill.values())
print("sum",round(sum(out.values()),6),"bill",total)
assert abs(sum(out.values())-total)<1e-9
```

**Output (my run):**
```text
tagged direct 1230 untagged residue 170
fraud     direct   470 cluster  160.0 registry  12.5 fs   75.0 untagged   65.0 total   782.5
reco      direct   450 cluster  140.0 registry  12.5 fs   45.0 untagged   62.2 total   709.7
forecast  direct   170 cluster   60.0 registry  12.5 fs   15.0 untagged   23.5 total   281.0
credit    direct   140 cluster   40.0 registry  12.5 fs   15.0 untagged   19.3 total   226.8
sum 2000.0 bill 2000
```

**Follow-ups:**
- When does chargeback hurt? When numbers are disputed or teams cut safety spend such as monitoring to save their budget. Keep a shared floor.
- Usage or fixed split? Usage if measured and stable; fixed when metering costs more than the item.

**Common mistakes:** No assertion that the split adds up. Ignoring untagged cost. Starting with chargeback on bad data. Quoting prices instead of units.

### Q5 ⭐⭐⭐ 🟡 [Set F, Q2 of 4, 10 min, 20 pts] Fraud platform capacity. Using your Set F Q1 numbers (peak 700 TPS after the 6x ratio, invented per-replica service time 12 ms with 4 worker threads, p99 budget 60 ms for the model hop, 30 percent headroom, two availability zones), compute replicas, show that losing one zone still meets the budget, and run a small M/M/c-style queue simulation that shows p99 wait rising near saturation. Reference Part 6 Q15 for the capacity method and Part 6 Q31 for timeouts, retries and load shedding; say what you shed first and what you never shed (the decision must fail closed or open by policy).
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** One replica handles 333 requests a second, peak with headroom is 910, so each zone needs 3 replicas (6 in total) so that either zone alone carries the peak at 70 percent utilisation; a split of 2 per zone would run at 105 percent after a zone loss.

**Then explain:**
- Method (see Part 6 Q15): replica capacity = threads / service time = 4 / 0.012 = 333 rps. Required capacity = peak x (1 + headroom) = 700 x 1.3 = 910. Sizing is per zone because the survivor must carry everything.
- Queue sim (M/M/c style, exponential arrivals and service, sandbox numbers only): p99 wait is nearly zero at 50 percent utilisation and climbs steeply past 85 percent. With one zone lost at 700 rps, utilisation is 0.70, simulated p99 wait is about 8 ms. Add the 12 ms service time and a typical request is near 20 ms, inside the 60 ms budget. The sim's exponential service time is pessimistic (its p99 service alone would be about 55 ms, total about 64 ms), so confirm with a real load test.
- Timeouts, retries and load shedding (Part 6 Q31): shed first low-value work such as batch re-scoring, enrichment calls and non-critical features. Never silently drop the authorisation decision: fail closed or fail open is a written policy per merchant risk tier (for example, small amounts fail open to a rules fallback; high risk fails closed). Retries need budgets or they multiply load during an outage.
- Failure modes: assuming N/2 capacity is enough, retry storms, a shared dependency (feature store) that fails both zones at once.
- Scoring note (20 pts, Set F Q2, 10 min): full for the replica arithmetic including the zone-loss check (6 pts each for per-replica capacity and zone survival), the saturation curve (5 pts), shed/never-shed policy (3 pts). Partial for sizing on the total only.

**Example:** 3 replicas x 333 = 1,000 rps per zone. Peak 700 / 1,000 = 0.70 after losing a zone. 2 per zone gives 700/667 = 1.05, saturated, queue grows without bound.

**Code:**
```python
import math, random, heapq
peak=700; svc=0.012; threads=4; headroom=0.30; budget=0.060
per_rep=threads/svc                      # req/s at 100% busy
need=peak*(1+headroom)
reps=math.ceil(need/per_rep)             # one zone must carry the whole peak plus headroom
per_az=reps; reps_az=2*per_az
print("per-replica capacity rps",round(per_rep,1),"needed with headroom",need,"replicas per AZ",per_az,"-> deploy",reps_az)
surv=per_az
print("after losing one AZ: replicas",surv,"util at peak",round(peak/(surv*per_rep),3))
assert peak/(surv*per_rep)<1
print("naive N/2 split (2 per AZ) would give util",round(peak/(2*per_rep),3),"-> saturated")
def sim(lam,c,n=60000,seed=1):
    rnd=random.Random(seed); free=[0.0]*c; heapq.heapify(free); t=0; waits=[]
    for _ in range(n):
        t+=rnd.expovariate(lam); s=rnd.expovariate(1/svc)
        f=heapq.heappop(free); st=max(t,f); waits.append(st-t); heapq.heappush(free,st+s)
    waits.sort(); return waits[int(.99*n)]*1000, sum(waits)/n*1000
c=reps_az*threads
print("servers (threads) in sim:",c,"full cap",round(c/svc))
print("util  p99_wait_ms  mean_wait_ms   (full fleet, then one AZ lost)")
for u in (0.5,0.7,0.85,0.95,0.99):
    p,m=sim(u*c/svc,c); print(f"{u:.2f}  {p:8.2f}  {m:8.2f}")
c2=surv*threads
p,m=sim(peak,c2); print("one AZ lost at 700 rps: util",round(peak*svc/c2,2),"p99 wait ms",round(p,2),"p99 total ~",round(p+12*4.6,1),"(service p99 for exp ~4.6x mean, sandbox model)")
```

**Output (my run):**
```text
per-replica capacity rps 333.3 needed with headroom 910.0 replicas per AZ 3 -> deploy 6
after losing one AZ: replicas 3 util at peak 0.7
naive N/2 split (2 per AZ) would give util 1.05 -> saturated
servers (threads) in sim: 24 full cap 2000
util  p99_wait_ms  mean_wait_ms   (full fleet, then one AZ lost)
0.50      0.00      0.00
0.70      2.53      0.08
0.85      8.20      0.89
0.95     37.21      6.51
0.99    105.56     24.23
one AZ lost at 700 rps: util 0.7 p99 wait ms 8.46 p99 total ~ 63.7 (service p99 for exp ~4.6x mean, sandbox model)
```

**Follow-ups:**
- Why not autoscale? Autoscaling lags fraud bursts; keep a floor sized for the survivor case and autoscale above it.
- Is the sim exact? No: exponential service is a rough model; real service times are less variable, so measure with a load test.

**Common mistakes:** Dividing capacity across zones without checking survival. Using mean latency for the p99 budget. Retrying without limits. Dropping decisions with no policy.

### Q6 ⭐⭐⭐ 🟡 [Set R, Q2 of 4, 10 min, 20 pts] Recommender serving path and features. Sketch the two-stage path (candidate retrieval, ranking) with a 120 ms feed budget split across feature lookup, retrieval, ranking and re-ranking, and place the online and offline feature stores. Reference Part 9 Q35 for recommender features and Part 9 Q27 for the real-time feature latency budget. Compute, with invented numbers, how many ranking-model calls per second a 400 candidates per request design needs at 900 requests per second, and show one lever that cuts it (two-tower pre-filter, caching, smaller candidate set) with the quality risk.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Two stages: retrieve a few hundred candidates cheaply, then rank them with a heavier model; at 400 candidates and 900 requests a second that is 360,000 ranking calls a second, and a two-tower pre-filter down to 150 cuts it to 135,000.

**Then explain:**
- Budget (120 ms, invented): feature lookup 15, retrieval 25, ranking 55, re-ranking 15, overhead 10 = 120. Ranking gets the biggest slice, retrieval and lookups run in parallel where possible (see Part 9 Q27 for the real-time feature budget).
- Feature stores: online store (low-latency key-value) serves user and item features at request time; the offline store holds history for training and backfills; both must compute features the same way (Part 9 Q35 for recommender features).
- Levers: two-tower pre-filter (cheap dot-product to shrink candidates), caching rankings for repeat users, smaller candidate set. Batch the 400 candidates into one model call; ranking calls are batched rows, not 400 network calls.
- Quality risk: a tighter pre-filter can drop the item the ranker would have put first (recall loss at the retrieval stage cannot be recovered later). Caching serves stale results, which hurts freshness and new-item exposure. Check with an A/B test and a retrieval-recall metric.
- Scoring note (20 pts, Set R Q2, 10 min): full for a budget that sums to 120, correct 360,000, one lever with its quality risk and online/offline store placement. Partial if the arithmetic is right but the risk is missing.

**Example:** 900 x 400 = 360,000 candidate scores/s. Prefilter to 150: 135,000 (-62.5 percent). 30 percent cache hit (invented) on top: 94,500.

**Code:**
```python
rps=900; cand=400
calls=rps*cand
print("ranking calls/s, 400 cands:",calls)
budget={"feature lookup":15,"retrieval":25,"ranking":55,"re-ranking":15,"overhead":10}
print(budget,"sum",sum(budget.values())); assert sum(budget.values())==120
for name,n in [("two-tower prefilter to 150",150),("smaller set 200",200)]:
    print(name,"calls/s",rps*n,"cut",round(1-n/cand,3))
hit=0.30
print("cache 30% of requests (invented):",int(rps*(1-hit))*cand)
print("combined prefilter 150 + cache 30%:",int(rps*(1-hit))*150)
```

**Output (my run):**
```text
ranking calls/s, 400 cands: 360000
{'feature lookup': 15, 'retrieval': 25, 'ranking': 55, 're-ranking': 15, 'overhead': 10} sum 120
two-tower prefilter to 150 calls/s 135000 cut 0.625
smaller set 200 calls/s 180000 cut 0.5
cache 30% of requests (invented): 252000
combined prefilter 150 + cache 30%: 94500
```

**Follow-ups:**
- Where does re-ranking sit? After ranking: diversity, freshness boosts, creator-fairness rules, safety filters.
- How do you protect cold-start items? Reserve exploration slots in re-ranking.

**Common mistakes:** Treating candidates as 400 separate calls. Cutting candidates with no retrieval-recall check. Budget that does not sum.

### Q7 ⭐⭐⭐ 🟡 [Set C, Q2 of 4, 10 min, 20 pts] Credit-risk lifecycle controls. Lay out the model lifecycle with its gates: data lineage, development, independent validation, approval, champion-challenger or shadow period, deployment, monitoring and retirement. Reference Part 7 Q38 (CI/CD for a regulated credit model), Part 7 Q24 (separation of duties), Part 4 Q15 (lineage) and Part 8 Q41 (model risk governance and monitoring); say what evidence artefact each gate produces and who signs. Implement the gate checklist as a small Python state machine that refuses a promotion if any evidence field is missing, with tests.
**Asked at:** Coverage of the RBI FREE-AI framework of 13 Aug 2025 (law.asia, storyboard18, cxodigitalpulse, securiti, mitsloanme; search snippets only, not opened): seven principles, 26 recommendations in six pillars, board-approved AI policy, AI-specific audit, disclosures; no snippet gave model-risk or localisation text, so those parts are hedged 'check the RBI site'; regulated BFSI and GCC credit and fraud roles | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** A regulated credit model moves through fixed gates, each gate needs named evidence and a named signer, and the pipeline refuses to move forward if any evidence is missing or the same person signed twice.

**Then explain:**
- Gates and evidence: lineage (lineage id, data snapshot; Part 4 Q15) then development (dev report, signed by the model owner), independent validation (validation report, signed by the validator), approval (approval record from the committee; Part 8 Q41 for governance), shadow or champion-challenger period (shadow report), deployment (deploy record, release approver separate from model owner; Part 7 Q38 and Q24), monitoring (drift and performance reports) and retirement (reason and sign-off).
- Separation of duties (Part 7 Q24): the approver must not be the validator or builder; the deployer must not be the approver. The state machine enforces this in code.
- Refusal is the point: a missing field, a skipped gate or a duplicate signer returns an error and the state does not change. Tests prove each refusal.
- Failure modes: evidence stored as free text that nobody checks, a gate bypassed under delivery pressure, retirement forgotten so old models keep scoring.
- Scoring note (20 pts, Set C Q2, 10 min): full for all gates with an evidence artefact and signer each (10 pts), working refusal logic with tests (6 pts), monitoring and retirement (4 pts). Partial if the gates are listed without evidence.

**Example:** Promoting to approval with approver = validator raises "approver must differ from validator/builder" and the model stays at validation.

**Code:**
```python
import unittest
GATES=["lineage","development","validation","approval","shadow","deployment","monitoring","retired"]
EVID={"development":["lineage_id"],"validation":["dev_report","lineage_id"],
 "approval":["validation_report","validator","approver"],
 "shadow":["approval_id","approver"],
 "deployment":["shadow_report","deployer"],
 "monitoring":["deploy_id"],"retired":["retire_reason","approver"]}
class Refused(Exception): pass
class Model:
    def __init__(s): s.state="lineage"; s.log=[]; s.ev={}
    def promote(s,to,**ev):
        i=GATES.index(s.state)
        if to!=GATES[i+1] if i+1<len(GATES) else True: raise Refused(f"cannot skip {s.state}->{to}")
        for k in EVID.get(to,[]):
            if not ev.get(k): raise Refused(f"missing evidence '{k}' for {to}")
        # separation of duties
        if to=="approval" and ev["approver"] in (ev["validator"],ev.get("builder")): raise Refused("approver must differ from validator/builder")
        if to=="deployment" and ev["deployer"]==s.ev.get("approver"): raise Refused("deployer must differ from approver")
        s.state=to; s.ev.update(ev); s.log.append((to,dict(ev)))
class T(unittest.TestCase):
    def full(s):
        m=Model()
        m.promote("development",lineage_id="L1"); m.promote("validation",dev_report="D",lineage_id="L1")
        m.promote("approval",validation_report="V",validator="vera",approver="al",builder="bo")
        return m
    def test_happy(s):
        m=s.full(); m.promote("shadow",approval_id="A1",approver="al")
        m.promote("deployment",shadow_report="S",deployer="dee"); m.promote("monitoring",deploy_id="X"); s.assertEqual(m.state,"monitoring")
    def test_missing(s):
        m=Model()
        with s.assertRaises(Refused): m.promote("development")
    def test_skip(s):
        m=Model()
        with s.assertRaises(Refused): m.promote("approval",validation_report="V",validator="v",approver="a")
    def test_sod_approver(s):
        m=Model(); m.promote("development",lineage_id="L"); m.promote("validation",dev_report="D",lineage_id="L")
        with s.assertRaises(Refused): m.promote("approval",validation_report="V",validator="vera",approver="vera")
    def test_sod_deployer(s):
        m=s.full(); m.promote("shadow",approval_id="A",approver="al")
        with s.assertRaises(Refused): m.promote("deployment",shadow_report="S",deployer="al")
    def test_state_unchanged_on_refusal(s):
        m=Model()
        try: m.promote("development")
        except Refused: pass
        s.assertEqual(m.state,"lineage")
if __name__=="__main__": unittest.main(verbosity=2)
```

**Output (my run):**
```text
test_happy (__main__.T.test_happy) ... ok
test_missing (__main__.T.test_missing) ... ok
test_skip (__main__.T.test_skip) ... ok
test_sod_approver (__main__.T.test_sod_approver) ... ok
test_sod_deployer (__main__.T.test_sod_deployer) ... ok
test_state_unchanged_on_refusal (__main__.T.test_state_unchanged_on_refusal) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.000s

OK
```

**Follow-ups:**
- Is code enough? No. It enforces the checklist; people still decide. Store the evidence in the registry and the audit log.
- How long do you shadow? Long enough for the volume and seasonality to cover the cases; set it in policy, not in this sketch.

**Common mistakes:** Evidence as a checkbox with no artefact. One person playing every role. Forgetting retirement. A pipeline that can be skipped.

### Q8 ⭐⭐⭐ 🟡 [Set F, Q3 of 4, 12 min, 30 pts] Fraud features, labels and retraining. Chargebacks arrive 7 to 45 days after the transaction (invented), fraud is 0.1 percent of traffic, and analysts review only the top-scored 0.5 percent. Explain how this creates a biased, delayed label set, what you train on and when, how point-in-time correct features are built (Part 9 Q6 and Part 9 Q34), what monitoring you can do before labels arrive (Part 8 Q43 and Part 8 Q8) and how retraining is triggered (Part 5 Q30). Simulate delayed labels in Python and show how the apparent recall of a fresh model is understated at day 7.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Fraud labels arrive 7 to 45 days late and come mostly from the cases analysts looked at, so a fresh model looks worse than it is until labels land; train on matured windows with point-in-time features and watch proxies in the meantime.

**Then explain:**
- Bias: only the top 0.5 percent are reviewed, so labels for frauds the model missed arrive only via chargeback; the training set reflects the old model's choices (selection bias). Fraud is 0.1 percent so classes are rare; use weights or sampling and PR metrics.
- Train on matured windows: use transactions old enough that most labels have arrived (for example older than 45 days, or older than a chosen maturity point), plus recent data with a censoring flag or down-weighting. Features are built point-in-time (Part 9 Q6, Q34) so no future leakage.
- Before labels arrive (Part 8 Q43, Q8): watch input drift, score distribution, flag rate, analyst-confirmed rate, and early proxies such as customer complaints.
- Retraining trigger (Part 5 Q30): schedule plus drift or business triggers, and a gate that the new model beats the champion on matured data.
- Sim result: with all labels on a 7-45 day delay, apparent recall (caught and labelled / all eventual frauds) is 0.000 at day 7 and 0.054 at day 14, against a true recall of 0.339. If confirmed flagged cases arrive faster than chargebacks, recall among labelled cases only looks too high (1.000 at day 7), a bias in the other direction.
- Scoring note (30 pts, Set F Q3, 12 min): full for explaining delay and selection bias (8), matured-window training with point-in-time features (8), pre-label monitoring and retrain trigger (6), the simulation and both bias directions (8). Partial for naming delay without a fix.

**Example:** First-week cohort has 56 frauds, 19 caught (0.339). At day 14 only 10 labels exist, so naive recall reads 5.4 percent.

**Code:**
```python
import random
rnd=random.Random(7)
N=400_000; fraud=0.001
y=[rnd.random()<fraud for _ in range(N)]
day=[rnd.randrange(60) for _ in range(N)]
score=[rnd.gauss(2.0 if f else 0.0,1) for f in y]
thr=sorted(score)[int(0.995*N)]          # analysts review top 0.5 percent
flag=[s>=thr for s in score]
cb=[rnd.randrange(7,46) for _ in range(N)]        # chargeback delay 7..45
fast=[rnd.randrange(1,4) for _ in range(N)]       # analyst confirms in 1..3 days (scenario 2)
nf=sum(y); tp=sum(1 for f,v in zip(flag,y) if f and v)
print("frauds",nf,"true recall at top 0.5%:",round(tp/nf,3))
cohort=[i for i in range(N) if day[i]<7 and y[i]]       # first week of the fresh model
caught=[i for i in cohort if flag[i]]
def run(name,lab_delay):
    print(name)
    for ed in (7,14,30,50):
        arrived=[i for i in cohort if day[i]+lab_delay(i)<=ed]
        a=sum(1 for i in arrived if flag[i])
        A=a/len(cohort); B=a/max(1,len(arrived))
        print(f"  eval day {ed:2}: labelled {len(arrived):2}/{len(cohort)}  recall A (caught-labelled / all eventual frauds) {A:.3f}   recall B (among labelled only) {B:.3f}")
run("scenario 1: all labels via 7-45 day process",lambda i:cb[i])
run("scenario 2: flagged frauds confirmed in 1-3 days, missed ones wait for chargeback",lambda i:fast[i] if flag[i] else cb[i])
print("cohort true recall:",round(len(caught)/len(cohort),3))
```

**Output (my run):**
```text
frauds 412 true recall at top 0.5%: 0.272
scenario 1: all labels via 7-45 day process
  eval day  7: labelled  0/56  recall A (caught-labelled / all eventual frauds) 0.000   recall B (among labelled only) 0.000
  eval day 14: labelled 10/56  recall A (caught-labelled / all eventual frauds) 0.054   recall B (among labelled only) 0.300
  eval day 30: labelled 33/56  recall A (caught-labelled / all eventual frauds) 0.179   recall B (among labelled only) 0.303
  eval day 50: labelled 56/56  recall A (caught-labelled / all eventual frauds) 0.339   recall B (among labelled only) 0.339
scenario 2: flagged frauds confirmed in 1-3 days, missed ones wait for chargeback
  eval day  7: labelled 16/56  recall A (caught-labelled / all eventual frauds) 0.286   recall B (among labelled only) 1.000
  eval day 14: labelled 26/56  recall A (caught-labelled / all eventual frauds) 0.339   recall B (among labelled only) 0.731
  eval day 30: labelled 42/56  recall A (caught-labelled / all eventual frauds) 0.339   recall B (among labelled only) 0.452
  eval day 50: labelled 56/56  recall A (caught-labelled / all eventual frauds) 0.339   recall B (among labelled only) 0.339
cohort true recall: 0.339
```

**Follow-ups:**
- How do you fix selection bias? Keep a small random-review holdout so you see frauds the model would miss, and use it for unbiased evaluation.
- Why not train on unlabelled as good? Unlabelled recent rows include real frauds not yet reported; that teaches the model to miss them.

**Common mistakes:** Evaluating on labels that have not matured. Training on analyst-reviewed rows only. Leaking future features. Retraining on a fixed calendar with no maturity rule.

### Q9 ⭐⭐⭐ 🟡 [Idle GPUs] A 16-GPU cluster (invented) shows 31 percent average GPU utilisation and teams still complain they cannot get GPUs. Explain the usual causes (reserved-by-default notebooks, oversized requests, no queueing or preemption policy, small jobs holding whole GPUs, data-loading stalls), the levers (quotas with borrowing, time-boxed notebook leases, sharing with time-slicing or MIG, bin-packing, scale-to-zero node pools, checkpoint-and-preempt) and how you measure waste. Reference Part 3 Q15, Part 3 Q20 and Part 3 Q21 for the Kubernetes mechanics. Compute from an invented job log the reclaimable GPU-hours and the utilisation after a leasing policy, in Python.
**Asked at:** FinOps interview-prep material (TechTarget 'Prepare for your FinOps interview' 12-question tip, hirevire FinOps and cloud-cost prescreening lists, a devopsboys FinOps roadmap; search snippets only, not opened, WebFetch of techtarget.com failed with getaddrinfo ENOTFOUND); generic cloud-cost question families (tagging, showback and chargeback, spot, idle resources, budgeting), none GPU-specific, not verified company reports | LLM and GPU inference cost guides (Cast AI, Morph, DataCamp, machinelearningatscale.com, an alpeshnakrani.com playbook; search snippets only, not opened; vendor-authored figures such as utilisation percentages are one vendor's data and are NOT reused here); practitioner blogs, not interview reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Low average utilisation with a queue of waiting teams means GPUs are held, not used, so I measure held versus busy hours, then lease notebooks, share small jobs and preempt, not buy more GPUs.

**Then explain:**
- Causes: notebooks reserved by default and left idle, oversized requests (a whole GPU for a small job), no queue or preemption policy, small jobs each holding a full card, data-loading stalls that keep the GPU waiting on the CPU.
- Levers: quotas with borrowing, time-boxed leases, sharing (time-slicing or MIG where the hardware supports it; check current docs), bin-packing, scale-to-zero node pools, checkpoint-and-preempt for long jobs. Kubernetes mechanics: Part 3 Q15, Q20, Q21.
- Measure waste: GPU-hours held minus GPU-hours busy, by team and job kind, from scheduler data and GPU utilisation metrics. Report idle-held hours per team (showback).
- Failure modes: preemption without checkpointing loses work; time-slicing gives no memory isolation, so one job can hurt another; leases that are too short annoy users.
- Honest point: leasing frees capacity; utilisation percent rises only when waiting jobs use the freed hours.

**Example:** Invented 24h log, 16 GPUs: capacity 384 GPU-h, held 262, busy 81.2 (21.1 percent of capacity; 31.0 percent of held hours, the 31 percent in the prompt matches this ratio). A 4h notebook lease for notebooks under 10 percent busy reclaims 76 GPU-h (19.8 percent of capacity). If queued jobs use them at 80 percent busy, utilisation of capacity goes to 37 percent.

**Code:**
```python
# 16 GPUs, 24h window, invented job log: (kind, gpus_held, hours_held, busy_fraction)
jobs=[("notebook",1,24,0.05),("notebook",1,24,0.08),("notebook",1,24,0.04),("notebook",2,24,0.10),
 ("notebook",1,20,0.06),("train",4,10,0.85),("train",2,8,0.70),("train",1,6,0.35),
 ("tune",1,3,0.90),("tune",1,3,0.88),("tune",1,3,0.90),("tune",1,3,0.86),("infer",1,24,0.30),("infer",1,24,0.25)]
cap=16*24
held=sum(g*h for _,g,h,_ in jobs); busy=sum(g*h*b for _,g,h,b in jobs)
print("capacity GPU-h",cap,"held",held,"held share",round(held/cap,3),"busy GPU-h",round(busy,1),"avg util of capacity",round(busy/cap,3))
# lease policy: notebooks get 4h lease unless renewed with activity; idle (<10% busy) notebooks reclaimed after 2h idle grace
LEASE=4
new_held=0; reclaim=0
for k,g,h,b in jobs:
    if k=="notebook" and b<0.10:
        keep=min(h,LEASE); reclaim+=g*(h-keep); new_held+=g*keep
    else: new_held+=g*h
print("reclaimable GPU-h",reclaim,"share of capacity",round(reclaim/cap,3))
print("held after policy",new_held,"free GPU-h now",cap-new_held)
print("busy GPU-h unchanged",round(busy,1),"util of HELD hours before",round(busy/held,3),"after",round(busy/new_held,3))
print("util of capacity unchanged:",round(busy/cap,3),"- the win is freed capacity for waiting jobs, not a higher percentage")
# if queue absorbs freed hours with jobs at 80% busy (invented)
extra=reclaim*0.8
print("if queued jobs use the freed hours at 80% busy: util of capacity",round((busy+extra)/cap,3))
assert reclaim<=held
```

**Output (my run):**
```text
capacity GPU-h 384 held 262 held share 0.682 busy GPU-h 81.2 avg util of capacity 0.211
reclaimable GPU-h 76 share of capacity 0.198
held after policy 186 free GPU-h now 198
busy GPU-h unchanged 81.2 util of HELD hours before 0.31 after 0.437
util of capacity unchanged: 0.211 - the win is freed capacity for waiting jobs, not a higher percentage
if queued jobs use the freed hours at 80% busy: util of capacity 0.37
```

**Follow-ups:**
- Is more utilisation always good? No; leave headroom for latency-sensitive inference and bursts.
- MIG or time-slicing? MIG isolates memory but needs supported hardware and fixed slices; time-slicing is flexible with no isolation. Check current docs.

**Common mistakes:** Buying GPUs before measuring held-versus-busy. Preempting without checkpoints. Reporting one utilisation number with no per-team view.

### Q10 ⭐⭐⭐ 🟡 [Queues and backpressure] A scoring service receives bursts: 200 requests per second for 20 seconds, then 40 for 100 seconds (invented), while workers can do 80 per second. Simulate a bounded queue with three policies (unbounded, bounded with reject, bounded with timeout and drop-oldest) in Python and report queue depth, p99 wait, rejects and wasted work on requests whose callers already timed out. Reference Part 6 Q31 and Part 9 Q19. Say when a message queue and asynchronous replies are the right design instead (Part 6 Q30).
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** An unbounded queue just hides overload: it keeps every request, makes everyone wait about 30 seconds, and burns most work on callers who already gave up; a bounded queue that rejects or drops old requests keeps latency inside the timeout.

**Then explain:**
- Setup: 200 rps for 20 s then 40 rps for 100 s = 8,000 requests; workers do 80 rps, so 9,600 fit in 120 s overall but the burst overfills early. Callers time out after 2 s (invented).
- Unbounded: max depth 2,400, p99 wait 29.6 s, only 2,026 useful, 5,974 wasted on late callers. Bounded with reject (cap 160): depth 160, p99 2.0 s, 2,240 rejected, 5,718 useful, 42 wasted. Bounded with timeout and drop-oldest: p99 1.7 s, 5,760 useful, 0 wasted. Sandbox numbers from my simulation, not benchmarks.
- Choice: reject fast gives callers a clear error to retry elsewhere (Part 6 Q31 on retries and shedding). Drop-oldest favours fresh requests when stale answers are useless.
- Use a message queue and async replies when callers can wait (batch scoring, emails, long jobs) and results can be delivered later (Part 6 Q30; Part 9 Q19 on Kafka consumer lag). Not for authorisation-time decisions.
- Failure modes: retries amplify the burst; the queue limit too high means it delays rather than protects; no metric on rejects.

**Example:** Queue cap 160 at 80 rps equals 2 s of work, the same as the caller timeout, so anything still queued can finish in time.

**Code:**
```python
import random, statistics
def arrivals():
    t=0.0; out=[]
    for rate,dur in ((200,20),(40,100)):
        end=t+dur
        n=int(rate*dur)
        for i in range(n): out.append(t+i/rate)
        t=end
    return out
MU=80; TIMEOUT=2.0   # callers give up after 2s
def run(policy,cap=None):
    arr=arrivals(); q=[]; busy_until=0.0; waits=[]; rej=0; wasted=0; done=0; maxq=0
    # event-free fluid-ish discrete sim: process in arrival order with FIFO server, rate MU
    import heapq
    ev=[(a,'a') for a in arr]; i=0; now=0.0; q=[]; server_free=0.0
    # advance time by arrivals; serve between arrivals
    def serve_until(t):
        nonlocal server_free,done,wasted
        while q and server_free<=t:
            # pick next
            a=q.pop(0)
            start=max(server_free,a)
            if policy=="timeout_drop" and start-a>TIMEOUT:
                continue                    # dropped before work started
            waits.append(start-a)
            server_free=start+1/MU
            if start-a>TIMEOUT: wasted+=1     # caller already gone, work still done
            else: done+=1
    for a in arr:
        serve_until(a)
        if cap is not None and len(q)>=cap:
            if policy=="bounded_reject": rej+=1; continue
            if policy=="timeout_drop": q.pop(0); rej+=1      # drop oldest
        q.append(a); maxq=max(maxq,len(q))
    serve_until(1e9)
    waits.sort(); p99=waits[int(.99*len(waits))] if waits else 0
    return dict(policy=policy,total=len(arr),max_depth=maxq,p99_wait_s=round(p99,2),rejected_or_dropped=rej,useful=done,wasted_late=wasted)
for r in (run("unbounded"),run("bounded_reject",160),run("timeout_drop",160)): print(r)
print("arrivals",len(arrivals()),"= 4000 + 4000; capacity over 120 s =",MU*120)
```

**Output (my run):**
```text
{'policy': 'unbounded', 'total': 8000, 'max_depth': 2400, 'p99_wait_s': 29.63, 'rejected_or_dropped': 0, 'useful': 2026, 'wasted_late': 5974}
{'policy': 'bounded_reject', 'total': 8000, 'max_depth': 160, 'p99_wait_s': 2.0, 'rejected_or_dropped': 2240, 'useful': 5718, 'wasted_late': 42}
{'policy': 'timeout_drop', 'total': 8000, 'max_depth': 160, 'p99_wait_s': 1.73, 'rejected_or_dropped': 2240, 'useful': 5760, 'wasted_late': 0}
arrivals 8000 = 4000 + 4000; capacity over 120 s = 9600
```

**Follow-ups:**
- How to set the bound? Service rate times the longest acceptable wait.
- What do clients see? A fast 429/503 with a retry hint and jittered backoff.

**Common mistakes:** Unbounded queues. Queue limit larger than the caller timeout. Counting throughput without separating useful from wasted work. Retrying without backoff.

### Q11 ⭐⭐⭐ 🟡 [Secrets] A model repo has had an AWS-style key, a database URL with a password and a JWT signing key committed at different times (all fake in your exercise). Build a small secret scanner in Python with regexes and an entropy check, run it over an invented tree and over git-history-style text, and show one false positive and one miss. Then give the remediation order: revoke and rotate first, remove from history second, add pre-commit and CI scanning, move to a secrets manager and short-lived credentials (Part 10 Q18, Part 7 Q5, Part 7 Q6, Part 2 Q9). Explain why deleting the file is not a fix.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | OWASP Top 10 for LLM Applications 2025 summaries (opensourcesecurity substack, Trend Micro, HackerOne, Bright Security, Coralogix; search snippets only, not opened): supply chain moved to LLM03, data and model poisoning LLM04, model theft folded out of the standalone list; no source on classic ML model-extraction attacks surfaced, so extraction questions rest on general knowledge, hedged | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** A scanner finds secrets, but the fix order is: revoke and rotate first, clean history second, then block it from coming back with pre-commit and CI scans and short-lived credentials; deleting the file does nothing because the secret is still in git history and every clone.

**Then explain:**
- Scanner: regex rules for known shapes (AWS key id, URL with password, JWT-shaped tokens, private key headers) plus an entropy check on assigned values. All keys here are fake.
- Run result: it found the fake AWS key, the database URL password and the JWT signing key (by entropy). One false positive: a README placeholder ("your-api-key-goes-here-please", entropy 3.51), and a harmless base64 greeting also flagged. One miss: a password built by concatenating two strings in a history diff, which no regex sees.
- Remediation order: (1) revoke and rotate, assume it leaked; (2) rewrite history and invalidate forks, or accept that rewriting is not enough; (3) pre-commit and CI secret scanning; (4) secrets manager and short-lived credentials via roles (Part 10 Q18, Part 7 Q5, Q6, Part 2 Q9 for Docker build secrets).
- Why deleting is not a fix: the secret lives in old commits, clones, CI logs and image layers.
- Failure modes: rotating only the key but not checking logs for use, secrets baked in image layers.

**Example:** JWT signing key leaked: rotating means all tokens signed with it are invalid or forgeable until rotation, so plan token expiry and key rollover.

**Code:**
```python
import re, math, tempfile, os
FAKE_AWS="AKIA"+"IOSFODNN7EXAMPLE"        # AWS docs example id shape, fake
FAKE_DB="postgres://app:Sup3rS3cretPw@db.internal:5432/prod"
FAKE_JWT_KEY="hs256_signing_key = 'k9Zx3vQ8rLm2PfT7uYb1NcW5eHd0JaGs'"
RULES={"aws_key_id":re.compile(r"\b(AKIA|ASIA)[A-Z0-9]{16}\b"),
 "db_url_password":re.compile(r"\b[a-z+]+://[^\s:/@]+:([^\s@/]{4,})@"),
 "jwt_like_token":re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
 "private_key_header":re.compile(r"-----BEGIN (RSA |EC )?PRIVATE KEY-----")}
ASSIGN=re.compile(r"(?i)(secret|signing_key|api_key|token|password)\w*\s*[=:]\s*['\"]([^'\"]{12,})['\"]")
def entropy(s):
    return -sum(s.count(c)/len(s)*math.log2(s.count(c)/len(s)) for c in set(s))
def scan(text,name):
    hits=[]
    for ln,line in enumerate(text.splitlines(),1):
        for rule,rx in RULES.items():
            if rx.search(line): hits.append((name,ln,rule))
        m=ASSIGN.search(line)
        if m and entropy(m.group(2))>=3.5: hits.append((name,ln,"high_entropy_assignment"))
    return hits
tree={
 "train.py":f"import boto3\nclient = boto3.client('s3', aws_access_key_id='{FAKE_AWS}')\n",
 "config.py":f"DATABASE_URL = '{FAKE_DB}'\n",
 "auth.py":f"{FAKE_JWT_KEY}\n",
 "README.md":"Set api_key = 'your-api-key-goes-here-please' in env\n",   # false positive candidate
 "notes.txt":"token = 'aGVsbG8gd29ybGQgdGhpcyBpcyBiYXNlNjQ='\n",
}
history="""commit 1a2b (removed secret)
- hs256_signing_key = 'k9Zx3vQ8rLm2PfT7uYb1NcW5eHd0JaGs'
+ hs256_signing_key = os.environ['JWT_KEY']
commit 9f9f
+ pwd_in_code = 'p@ss' + 'word123456'
"""
d=tempfile.mkdtemp(prefix="b12q11_",dir="/tmp/claude-0/b12_q01_11")
for n,t in tree.items(): open(os.path.join(d,n),"w").write(t)
hits=[]
for n in sorted(os.listdir(d)): hits+=scan(open(os.path.join(d,n)).read(),n)
print("== working tree"); [print(h) for h in hits]
print("== history-style text"); hh=scan(history,"history.diff"); [print(h) for h in hh]
print("entropy README value",round(entropy("your-api-key-goes-here-please"),2),"; base64 greeting",round(entropy("aGVsbG8gd29ybGQgdGhpcyBpcyBiYXNlNjQ="),2))
```

**Output (my run):**
```text
== working tree
('README.md', 1, 'high_entropy_assignment')
('auth.py', 1, 'high_entropy_assignment')
('config.py', 1, 'db_url_password')
('notes.txt', 1, 'high_entropy_assignment')
('train.py', 2, 'aws_key_id')
== history-style text
('history.diff', 2, 'high_entropy_assignment')
entropy README value 3.51 ; base64 greeting 4.37
```

**Follow-ups:**
- Entropy threshold? Tune it on your own repo; lower finds more, with more noise. Allowlist known placeholders.
- Is a scanner enough? No. Use it as a net; the fix is not having long-lived secrets.

**Common mistakes:** Deleting the file and moving on. Cleaning history before rotating. Trusting a scanner to catch everything. Putting secrets in env files that get committed.

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

### Q23 ⭐⭐ 🟡 [Set L, Q3 of 4, 12 min, 30 pts] LLM serving reliability and cost control at the boundary. The provider degrades for 40 minutes at peak (invented). Describe timeouts, retries with jitter, circuit breaking, fallback to a smaller model or a cached or templated answer, queueing of non-urgent work, and what you tell users. Reference Part 6 Q31, Part 7 Q40 and Part 11 Q33. Simulate a provider outage with and without a circuit breaker in Python and report requests served, requests failed and retry amplification of load on the provider.
**Asked at:** LLM and GPU inference cost guides (Cast AI, Morph, DataCamp, machinelearningatscale.com, an alpeshnakrani.com playbook; search snippets only, not opened; vendor-authored figures such as utilisation percentages are one vendor's data and are NOT reused here); practitioner blogs, not interview reports | ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** I treat the provider as something that will fail: short timeouts, a few retries with jitter and a retry budget, a circuit breaker that stops calling a dead provider, and a fallback (cache, smaller model, template) so users still get an answer.

**Then explain:**
- Timeout first. The client timeout is shorter than the user's patience and shorter than the gateway's, so a slow provider cannot pin all my workers (Part 6 Q31).
- Retries only for transient errors, 2 or 3 attempts, exponential backoff with full jitter. Without jitter all clients retry together. Failure mode: retries triple the load on a provider that is already sick (the run shows 3.0 attempts per request in the outage).
- Circuit breaker: after N failures in a row, stop calling for a cool-down, then send one probe (half-open). In the run it cut provider attempts in the outage from 144,000 to about 80.
- Fallback ladder, chosen per request type: cached answer, smaller or self-hosted model, templated "we are busy, here is the standard answer", or queue it. Non-urgent work (summaries, batch tagging) goes to a queue and drains after recovery with a rate limit, so recovery does not start a second storm. Check quality of the fallback in the CI gate for prompts and configs (Part 7 Q40); a second provider is a multi-cloud style trade-off (Part 11 Q33), so only do it if the outage risk pays for the extra complexity.
- What I tell users: a short banner and honest wording ("answers may be simpler for now"), never a silent downgrade for regulated answers; on-call gets an alert on breaker-open, not on each error.
- Scoring note [Set L, Q3 of 4, 12 min, 30 pts], using the part-header rubric: about 9 points for clarifying and stated assumptions (which requests are urgent, what a degraded answer may say, the budget for a 40-minute outage), 9 for a design that fits the numbers (the 3x retry arithmetic and breaker timings), 6 for failure modes, security and cost (retry storm, cache poisoning or leaking, fallback quality, cost of the smaller model), 3 for the runnable check, 3 for a clear 60-second summary. Partial credit: retries without jitter or a breaker, or a fallback with no quality or privacy thought.

**Example:** traffic is 20 requests a second for an hour; the provider is down for 2,400 seconds. Outage requests = 2,400 x 20 = 48,000. With up to 3 attempts each, the outage alone can send up to 144,000 attempts. The run shows the same: total attempts 167,949 = 24,000 healthy-time attempts plus about 3 x 48,000 in the outage. With the breaker, 23,994 attempts in the whole hour, and all 48,000 outage requests got a fallback answer instead of an error.

**Code:** run with `python3 -I q23.py`. Event simulation, seeded, abstract seconds, no network. Three modes: retries only, retries plus fallback, and breaker plus fallback.
```python
# Q23: provider outage simulation: retries only vs retries + circuit breaker + fallback. Seeded, abstract seconds.
import heapq, random
SEED = 23
DUR, RPS = 3600, 20              # one hour of traffic at 20 requests per second (invented)
OUT_START, OUT_END = 600, 3000   # provider down for 40 minutes (2400 s)
MAX_TRY, BASE, CAP = 3, 1.0, 8.0 # up to 3 attempts, backoff 1s, 2s ... capped, full jitter
TIMEOUT = 2.0                    # an attempt during the outage fails after 2 s

def provider_up(t): return not (OUT_START <= t < OUT_END)

def run(mode):
    rng = random.Random(SEED)
    ev, n = [], 0
    for sec in range(DUR):
        for _ in range(RPS):
            heapq.heappush(ev, (sec + rng.random(), n, 0)); n += 1   # (time, request id, attempts so far)
    total = n
    attempts = served = fb = failed = 0
    fails_in_row, open_until = 0, -1.0
    probing = False
    while ev:
        t, rid, k = heapq.heappop(ev)
        if mode == "breaker" and t < open_until:                      # circuit open: do not touch the provider
            fb += 1; continue
        attempts += 1
        ok = provider_up(t)
        if ok:
            served += 1; fails_in_row = 0
            if mode == "breaker": open_until = -1.0
            continue
        fails_in_row += 1
        if mode == "breaker" and fails_in_row >= 5:                   # trip after 5 failures in a row
            open_until = t + 30.0; fails_in_row = 4                   # half-open: one probe after 30 s, a failed probe re-opens
            fb += 1; continue
        if k + 1 < MAX_TRY:
            delay = rng.uniform(0, min(CAP, BASE * 2 ** k))           # full jitter
            heapq.heappush(ev, (t + TIMEOUT + delay, rid, k + 1))
        elif mode in ("breaker", "retries_fallback"): fb += 1
        else: failed += 1
    return total, served, fb, failed, attempts

print(f"{'mode':<18}{'requests':>9}{'primary_ok':>11}{'fallback':>9}{'failed':>8}{'attempts':>9}{'amplification':>14}")
for mode in ("retries_only", "retries_fallback", "breaker"):
    total, served, fb, failed, attempts = run(mode)
    assert served + fb + failed == total
    print(f"{mode:<18}{total:>9}{served:>11}{fb:>9}{failed:>8}{attempts:>9}{attempts/total:>14.2f}")
# hand check: 2400 s x 20 rps = 48000 requests arrive in the outage; retries_only makes up to 3 attempts for each
print("outage requests:", (OUT_END - OUT_START) * RPS, "-> at most", (OUT_END - OUT_START) * RPS * MAX_TRY, "attempts in the outage")
```

**Output (my run):**
```text
mode               requests primary_ok fallback  failed attempts amplification
retries_only          72000      24109        0   47891   167949          2.33
retries_fallback      72000      24109    47891       0   167949          2.33
breaker               72000      23910    48090       0    23994          0.33
outage requests: 48000 -> at most 144000 attempts in the outage
```
Reading it: `retries_only` fails 47,891 requests; `retries_fallback` serves them from the fallback but still sends 2.33 attempts per request overall (3.0 inside the outage). `breaker` has 0.33 attempts per request because open-circuit requests never reach the provider. About 90 extra requests beyond the 48,000 got the fallback around the end of the outage while the breaker waited for its probe: the cost of a cool-down. This is a toy: no provider capacity, no queue, no partial failures, fixed timings.

**Follow-ups:**
- *Why not just retry more?* Retries help short blips only. In a 40-minute outage they add load and latency and delay recovery.
- *When does the breaker hurt?* If it trips on a few slow requests it removes a healthy provider. Use a rolling error rate with a minimum request count, and alert on trips.
- *Provider says 429?* Obey the retry-after header and shed my own lowest-priority work first.

**Common mistakes:** retries with no cap and no jitter; same timeout at every layer; fallback answers that skip the safety or PII checks; caching responses keyed without user or tenant; queueing non-urgent work with no rate limit on drain; telling nobody the answers got worse.

### Q24 ⭐⭐ 🟡 [Set E, Q3 of 4, 12 min, 30 pts] Edge fleet operations. 100,000 devices run three app versions with two model versions (invented). Explain how you ship model updates (staged cohorts, device capability checks, rollback on crash or accuracy proxy), what telemetry is safe and cheap (aggregate counters, confidence histograms, opt-in samples; Part 8 Q29), how you detect drift without raw data and how you handle devices that never update. Simulate a staged rollout with a bad model in Python and show how many devices are exposed before the gate halts it.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** I ship by cohorts of eligible devices (0.5 percent, 2, 10, 50, 100), gate each step on crash rate plus an accuracy proxy, and keep the old model on the device so rollback is a flag, not a re-download.

**Then explain:**
- Eligibility first: only devices with an app version and hardware that can run the model get it (here 74,969 of 100,000 are eligible). The others stay on the old model, and I keep that group in the plan, because they are the "never update" tail.
- Gate signals that are cheap and safe: crash and error counters, load time, latency histogram, a confidence histogram (aggregate), opt-in sampled inputs only with consent (Part 8 Q29). No raw data leaves by default.
- Drift without raw data: compare on-device confidence histograms and input-feature summaries (counts, means, bins) against the training reference; ship a small set of canary inputs with known answers to check the model on device.
- Failure modes: a crash gate alone misses a silent accuracy loss (the run shows scenario B going to 100 percent); a gate with too few sessions flaps; devices offline for weeks report late. Also kill switch for the model, not only for the app.
- Devices that never update: define a support window, keep the server API tolerant of old model versions, and tell product when a segment is frozen; for a security fix force-update the app, not only the model.
- Scoring note [Set E, Q3 of 4, 12 min, 30 pts], part-header rubric: about 9 points for clarifying (cohort size, update rate, what counts as bad, privacy limits) and assumptions, 9 for a rollout that fits the numbers (exposure arithmetic), 6 for failure modes, security and cost (silent drift, signed model files, bandwidth), 3 for the runnable check, 3 for the 60-second summary. Partial credit: staged rollout with no accuracy proxy, or telemetry that ships raw user data.

**Example:** the stages are 0.5 percent, 2 percent, 10 percent, 50 percent and 100 percent of 74,969 eligible devices, which is 374, 1,499, 7,496, 37,484 and 74,969 devices. A model that triples the crash rate is caught at stage 1, exposing 374 devices (0.37 percent of the fleet). A silent confidence drop of 0.12 is invisible to the crash gate and reaches all 74,969 devices.

**Code:** run with `python3 -I q24.py`. Seeded numpy, invented rates, abstract sessions.
```python
# Q24: staged rollout of a bad model to a 100,000 device fleet. Seeded numpy. Abstract, sandbox-only numbers.
import numpy as np
SEED = 24
N = 100_000
rng = np.random.default_rng(SEED)
app = rng.choice([1, 2, 3], size=N, p=[0.25, 0.45, 0.30])      # three app versions; model v2 needs app >= 2
eligible = np.flatnonzero(app >= 2)                              # capability check: 75,000 devices
order = rng.permutation(eligible)                                # random cohort order
STAGES = [0.005, 0.02, 0.10, 0.50, 1.0]                          # share of eligible devices
SESS = 20                                                        # sessions per device during one soak window
BASE_CRASH, BAD_CRASH = 0.005, 0.03                              # crash per session: old model vs bad model
GATE_CRASH = 0.015                                               # halt when stage crash rate is above this
BASE_CONF, DROP = 0.80, 0.12                                     # mean top-class confidence; silent-bad model drops it
GATE_CONF_DROP = 0.05

def simulate(scenario, proxy_gate):
    exposed = 0
    for i, s in enumerate(STAGES):
        cohort = order[: int(len(order) * s)]
        new = cohort                                             # every device in the cohort runs the new model
        crash_p = BAD_CRASH if scenario == "crashy" else BASE_CRASH
        crashes = rng.binomial(SESS, crash_p, size=len(new)).sum()
        crash_rate = crashes / (SESS * len(new))
        conf = BASE_CONF - (DROP if scenario == "silent" else 0) + rng.normal(0, 0.02)
        exposed = len(cohort)
        halted = crash_rate > GATE_CRASH or (proxy_gate and BASE_CONF - conf > GATE_CONF_DROP)
        print(f"  stage {i+1} ({s:>5.1%}): exposed={exposed:>6} crash_rate={crash_rate:.4f} conf={conf:.3f} -> {'HALT' if halted else 'go'}")
        if halted: return exposed
    return exposed

print("eligible devices:", len(eligible), "of", N)
for name, scen, proxy in [("A crashy model, crash gate only", "crashy", False),
                          ("B silent accuracy loss, crash gate only", "silent", False),
                          ("C silent accuracy loss, crash + confidence-proxy gate", "silent", True)]:
    print(name); e = simulate(scen, proxy)
    print(f"  => devices exposed when it stopped: {e}\n")
```

**Output (my run):**
```text
eligible devices: 74969 of 100000
A crashy model, crash gate only
  stage 1 ( 0.5%): exposed=   374 crash_rate=0.0322 conf=0.820 -> HALT
  => devices exposed when it stopped: 374

B silent accuracy loss, crash gate only
  stage 1 ( 0.5%): exposed=   374 crash_rate=0.0051 conf=0.682 -> go
  stage 2 ( 2.0%): exposed=  1499 crash_rate=0.0049 conf=0.671 -> go
  stage 3 (10.0%): exposed=  7496 crash_rate=0.0049 conf=0.681 -> go
  stage 4 (50.0%): exposed= 37484 crash_rate=0.0050 conf=0.696 -> go
  stage 5 (100.0%): exposed= 74969 crash_rate=0.0050 conf=0.654 -> go
  => devices exposed when it stopped: 74969

C silent accuracy loss, crash + confidence-proxy gate
  stage 1 ( 0.5%): exposed=   374 crash_rate=0.0040 conf=0.671 -> HALT
  => devices exposed when it stopped: 374
```
The numbers are sandbox values from invented rates, not measurements of any real fleet. The crash gate uses 20 sessions per device in each soak window.

**Follow-ups:**
- *How big should the first cohort be?* Big enough to see the failure in one soak window: with a 3 percent crash rate and 374 x 20 sessions the signal is obvious; for a 0.2 percent regression you need many more sessions or a longer soak.
- *Rollback?* Keep the previous model on disk, flip a remote config flag, and make the client fall back by itself after repeated crashes at load.
- *Cohort choice?* Random, but exclude low-end devices at first only if the model is heavy; stratify by app version so one bad app build is not blamed on the model.

**Common mistakes:** gating on crashes only; no kill switch; shipping the model in the app binary so every change needs a store review; collecting raw inputs for "drift"; forgetting devices that stay offline.

### Q25 ⭐⭐ 🟡 [Spot and preemptible capacity] Training takes 10 hours on 8 GPUs (invented) and interruption probability is 15 percent per hour on spot. Work out the expected wasted work with no checkpointing, with hourly checkpoints and with 10-minute checkpoints, include checkpoint overhead and restart delay, and decide when spot is worth it. Reference Part 2 Q27 and Part 10 Q14. Run a Monte Carlo simulation in Python with a seed and report mean and p95 completion time. No prices; use relative cost units with a stated discount parameter.
**Asked at:** FinOps interview-prep material (TechTarget 'Prepare for your FinOps interview' 12-question tip, hirevire FinOps and cloud-cost prescreening lists, a devopsboys FinOps roadmap; search snippets only, not opened, WebFetch of techtarget.com failed with getaddrinfo ENOTFOUND); generic cloud-cost question families (tagging, showback and chargeback, spot, idle resources, budgeting), none GPU-specific, not verified company reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Spot is worth it when checkpoints are cheap, because without checkpoints a long job loses everything on each interruption; with a checkpoint every 10 to 60 minutes the expected waste is small and the discount wins.

**Then explain:**
- Assumption I state out loud: 15 percent per hour is for the whole job (any of the 8 GPUs lost kills it). If it were per GPU the job-level rate would be much higher (1 - 0.85^8 = 73 percent an hour), so I ask which one it is. The model here uses job level.
- No checkpoint: P(10 clean hours) = 0.85^10 = 19.7 percent, so most attempts restart from zero. Closed form for the mean with exponential interruptions and restart delay r: (1/lambda + r) x (e^(lambda T) - 1), lambda = -ln(0.85).
- With checkpoints: expected waste per interruption is about half an interval plus the restart delay, so a shorter interval wastes less but pays more checkpoint overhead. Hourly versus 10-minute is close in the mean; 10 minutes tightens the tail (p95).
- Spot is worth it when mean wall-clock x spot-rate fraction is below the on-demand cost. The run prints the break-even spot rate per policy. The discount is a parameter I assumed (0.35), not a price.
- Failure modes: checkpoint not atomic (half-written file), checkpoint saved to local disk that dies with the node, optimizer state or data-loader position not saved so the resume is not equal (Part 2 Q27, Part 10 Q14), deadline-bound jobs that cannot tolerate a p95 tail, capacity not returning for hours.

**Example:** hand check of no checkpoint: lambda = 0.1625 per hour, e^(1.625) = 5.08, 1/lambda = 6.15 h, plus 0.25 h restart gives 6.40 x 4.08 = 26.1 hours mean (the closed form prints 26.12; the Monte Carlo gives 26.04). On-demand takes 10 hours. At an assumed spot rate of 0.35, no checkpoint costs 26.04 x 8 x 0.35 = 72.9 units against 80 on-demand: barely cheaper and a 63-hour p95. Hourly checkpoints: 11.48 h and 32.2 units, about 40 percent of on-demand.

**Code:** run with `python3 -I q25.py`. Seeded Monte Carlo, 20,000 trials per policy, relative units, 1 minute checkpoint overhead and 15 minutes restart delay (all invented).
```python
# Q25: spot training Monte Carlo. Interruption modelled as one job-level event per hazard (assumption stated). Relative cost units.
import math, random, statistics
SEED = 25
WORK = 10.0                      # hours of work, 8 GPUs (invented)
P_HOUR = 0.15                    # chance of at least one interruption in an hour (job level)
LAM = -math.log(1 - P_HOUR)      # hazard per hour, so that 1 - exp(-LAM) = 0.15
RESTART = 0.25                   # 15 min to get capacity back, reload and resume
GPUS = 8
SPOT_RATE = 0.35                 # spot price as a fraction of on-demand per GPU-hour: an assumed parameter, not a real price
def one(rng, ckpt, ov):
    done = 0.0; clock = 0.0       # done = saved progress
    while done < WORK:
        step = min(ckpt, WORK - done) if ckpt else WORK - done
        cost_step = step + (ov if ckpt and done + step < WORK else 0.0)     # checkpoint write time after each interval
        x = rng.expovariate(LAM)
        if x >= cost_step:
            clock += cost_step; done += step
        else:
            clock += x + RESTART  # lost everything since the last checkpoint
    return clock
def mc(ckpt, ov, n=20000):
    rng = random.Random(SEED)
    t = sorted(one(rng, ckpt, ov) for _ in range(n))
    return statistics.mean(t), t[int(0.95 * n)]
print(f"hazard/hour={LAM:.4f}  P(no interruption in 10h)={math.exp(-LAM*WORK):.3f}  (0.85^10={0.85**10:.3f})")
print(f"on-demand baseline: {WORK:.1f} h, cost {WORK*GPUS:.1f} GPU-hour units at rate 1.0")
print(f"{'policy':<26}{'mean_h':>8}{'p95_h':>8}{'wasted_h(mean)':>15}{'cost_units':>11}{'vs_on_demand':>13}")
for name, ck, ov in [("no checkpoint", None, 0), ("hourly, 1 min overhead", 1.0, 1/60), ("10 min, 1 min overhead", 1/6, 1/60)]:
    m, p95 = mc(ck, ov)
    cost = m * GPUS * SPOT_RATE
    print(f"{name:<26}{m:>8.2f}{p95:>8.2f}{m-WORK:>15.2f}{cost:>11.1f}{cost/(WORK*GPUS):>13.2f}")
# closed form for no checkpoint: E = (1/lam + restart) * (exp(lam*T) - 1)
print(f"closed-form mean, no checkpoint: {(1/LAM + RESTART)*(math.exp(LAM*WORK)-1):.2f} h")
# break-even: spot is worth it while mean wall-clock x SPOT_RATE < 1
for name, ck, ov in [("no checkpoint", None, 0), ("hourly", 1.0, 1/60), ("10 min", 1/6, 1/60)]:
    m, _ = mc(ck, ov); print(f"{name:<14} break-even spot rate = {WORK/m:.2f} of on-demand")
```

**Output (my run):**
```text
hazard/hour=0.1625  P(no interruption in 10h)=0.197  (0.85^10=0.197)
on-demand baseline: 10.0 h, cost 80.0 GPU-hour units at rate 1.0
policy                      mean_h   p95_h wasted_h(mean) cost_units vs_on_demand
no checkpoint                26.04   63.06          16.04       72.9         0.91
hourly, 1 min overhead       11.48   13.63           1.48       32.2         0.40
10 min, 1 min overhead       11.62   12.48           1.62       32.5         0.41
closed-form mean, no checkpoint: 26.12 h
no checkpoint  break-even spot rate = 0.38 of on-demand
hourly         break-even spot rate = 0.87 of on-demand
10 min         break-even spot rate = 0.86 of on-demand
```

**Follow-ups:**
- *Does it change if the interruption warning is two minutes?* A short warning lets a final checkpoint save the last stretch if writes are fast; do not rely on it, the write may not finish.
- *When do I stay on-demand?* Deadline jobs with no slack, jobs that cannot checkpoint, or when the spot-rate fraction is above the break-even printed (0.86 to 0.87 for checkpointed runs here).
- *Mixed fleets?* Keep rank 0 or a small on-demand core and put the elastic workers on spot, if the framework allows elastic membership.

**Common mistakes:** quoting a discount as if it were a measured price; forgetting overhead and restart time in the cost; checkpointing to a local disk; comparing mean only and ignoring p95 against a deadline; assuming per-GPU and per-job interruption are the same.

### Q26 ⭐⭐ 🟡 [Serving cost levers without prices] List the levers that cut serving cost (right-sizing, batching, quantisation, caching, scale-to-zero, model distillation, moving to batch, cheaper hardware, request shaping) and the quality or latency risk each introduces. Reference Part 6 Q43 (cost per 1,000 predictions) and Part 6 Q24 and Part 6 Q7. For an invented service (300 RPS peak, 40 percent repeats) compute capacity before and after batching and caching and rank the levers by cost reduction per unit of engineering effort you estimate. Do not use real prices.
**Asked at:** FinOps interview-prep material (TechTarget 'Prepare for your FinOps interview' 12-question tip, hirevire FinOps and cloud-cost prescreening lists, a devopsboys FinOps roadmap; search snippets only, not opened, WebFetch of techtarget.com failed with getaddrinfo ENOTFOUND); generic cloud-cost question families (tagging, showback and chargeback, spot, idle resources, budgeting), none GPU-specific, not verified company reports | LLM and GPU inference cost guides (Cast AI, Morph, DataCamp, machinelearningatscale.com, an alpeshnakrani.com playbook; search snippets only, not opened; vendor-authored figures such as utilisation percentages are one vendor's data and are NOT reused here); practitioner blogs, not interview reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** I cut cost by removing work first (cache, move to batch), then by getting more from each replica (batching, quantisation, right-sizing), and I rank them by saved replicas per unit of engineering effort, checking the quality or latency risk of each.

**Then explain:**
- Cheapest first: response cache (risk: stale or private answers, so key design and TTL matter, Part 6 Q24), dynamic batching (risk: waiting for the batch to fill raises p99, Part 6 Q7), right-sizing the replica (risk: less burst headroom).
- Heavier levers: quantisation or distillation (accuracy re-validation needed), moving non-urgent traffic to batch (product must accept delay), cheaper hardware (a port and a test).
- Request shaping is a lever too: cap input size, drop duplicate calls, ask clients to call less often.
- Everything is measured in cost per 1,000 predictions at the target utilisation (Part 6 Q43). Idle capacity is usually the largest line, so autoscaling matters more than micro-optimising a kernel.
- Failure modes: cache hit rate falls when traffic changes; batching win disappears at low load; savings counted at peak while the bill is driven by the average; no availability floor (keep at least 2 replicas).

**Example:** 300 RPS peak, one replica serves 30 RPS, target utilisation 70 percent, so 300 / (30 x 0.7) = 14.3, round up to 15 replicas. With 40 percent repeats and an assumed 90 percent of repeats served from cache, load becomes 300 x (1 - 0.36) = 192 RPS and the need is 192 / 21 = 9.1, so 10 replicas. Dynamic batching at an assumed 3x per replica gives 300 / 63 = 4.8, so 5. Both together: 192 / 63 = 3.05, so 4 replicas, a saving of 11 of 15 (the 3x batching factor and the efforts below are my invented estimates).

**Code:** run with `python3 -I q26.py`. Abstract replica counts, no prices.
```python
# Q26: serving cost levers. Abstract units: replicas, not money. All inputs invented.
import math
PEAK, REPEAT, HEAD = 300, 0.40, 0.70           # peak RPS, repeat share, target utilisation
BASE_RPS = 30                                    # one replica, one request at a time (invented)
def need(load, per_rep): return math.ceil(load / (per_rep * HEAD))
base = need(PEAK, BASE_RPS)
HIT = 0.40 * 0.9                                 # repeats only count if still cached: assume 90% of repeats hit
levers = {   # name: (load factor, per-replica factor, effort 1-5 (my estimate), risk)
 "response cache":       (1 - HIT, 1.0, 2, "stale answers; privacy of cached keys"),
 "dynamic batching":     (1.0, 3.0, 2, "adds wait for the batch to fill (p99)"),
 "quantisation":         (1.0, 1.5, 3, "small accuracy loss, needs re-validation"),
 "right-size replica":   (1.0, 1.2, 1, "less headroom for bursts"),
 "move to batch":        (0.25, 1.0, 5, "answers no longer real-time; 25% of traffic assumed movable"),
}
print(f"baseline: {PEAK} RPS / ({BASE_RPS} x {HEAD}) -> {base} replicas")
rows = []
for k, (lf, pf, eff, risk) in levers.items():
    n = need(PEAK * lf, BASE_RPS * pf); red = base - n
    rows.append((red / eff, k, n, red, eff, risk))
print(f"{'lever':<20}{'replicas':>9}{'saved':>6}{'effort':>7}{'saved/effort':>13}  risk")
for r in sorted(rows, reverse=True): print(f"{r[1]:<20}{r[2]:>9}{r[3]:>6}{r[4]:>7}{r[0]:>13.2f}  {r[5]}")
both = need(PEAK * (1 - HIT), BASE_RPS * 3.0)
print(f"cache + batching together: {both} replicas (saved {base-both})")
print("availability floor: never below 2 replicas, so the plan is", max(2, both))
```

**Output (my run):**
```text
baseline: 300 RPS / (30 x 0.7) -> 15 replicas
lever                replicas saved effort saved/effort  risk
dynamic batching            5    10      2         5.00  adds wait for the batch to fill (p99)
right-size replica         12     3      1         3.00  less headroom for bursts
response cache             10     5      2         2.50  stale answers; privacy of cached keys
move to batch               4    11      5         2.20  answers no longer real-time; 25% of traffic assumed movable
quantisation               10     5      3         1.67  small accuracy loss, needs re-validation
cache + batching together: 4 replicas (saved 11)
availability floor: never below 2 replicas, so the plan is 4
```
The ranking is only as good as my effort scores (1 to 5, my estimates). Batching comes first here, then right-sizing, then cache. In a real answer I would say which numbers I would measure to confirm.

**Follow-ups:**
- *Which lever do you try first?* Cache and batching, because they need no model change; check the repeat rate on real logs first, since 40 percent is an invented number.
- *Does quantisation always help?* Not always; check the hardware supports the lower precision and re-run the evaluation gate.
- *How do I report savings?* Cost per 1,000 predictions before and after at equal quality, not total spend.

**Common mistakes:** counting savings at peak only; trusting the hit rate without a TTL and key design; adding batching to a low-traffic service; quantising without a regression test; forgetting the availability floor.

### Q27 ⭐⭐ 🟡 [Storage tiering and egress] A data lake holds 400 TB of raw features, 60 TB of training snapshots and 5 TB of model artefacts (invented). Design lifecycle rules (hot, infrequent, archive, delete), retention for reproducibility versus cost, snapshot deduplication and where cross-Region or cross-cloud egress hides (training in one Region, data in another, multi-cloud as in Part 11 Q33). Reference Part 4 Q34 and Part 10 Q1. Compute with relative cost units and an invented access log which objects to tier and the retrieval penalty of a wrong guess.
**Asked at:** FinOps interview-prep material (TechTarget 'Prepare for your FinOps interview' 12-question tip, hirevire FinOps and cloud-cost prescreening lists, a devopsboys FinOps roadmap; search snippets only, not opened, WebFetch of techtarget.com failed with getaddrinfo ENOTFOUND); generic cloud-cost question families (tagging, showback and chargeback, spot, idle resources, budgeting), none GPU-specific, not verified company reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** I tier by how likely an object is to be read again, keep the artefacts that rollbacks need hot, give snapshots a retention rule tied to reproducibility, and watch for cross-Region reads because that is where cost hides.

**Then explain:**
- Lifecycle by class: raw features (400 TB) go hot to infrequent to archive by last-access age; training snapshots (60 TB) stay warm while they are the reproducible basis of a registered model, then archive; model artefacts (5 TB) stay hot, since a rollback must be fast (Part 4 Q34, Part 10 Q1; check current storage-class rules and minimum durations).
- Retention versus reproducibility: keep what is needed to rebuild a registered model (data version, code, config), delete scratch and failed runs, and deduplicate snapshots (content-addressed, as DVC does) so a small change does not copy 60 TB.
- Egress hides in training in one Region with data in another, in cross-cloud copies (Part 11 Q33), in replication nobody turned off, and in repeated epochs read across a boundary. Fix: move compute to the data or copy once and read local.
- Retrieval penalty: a wrong guess costs retrieval fees and delay. Archive only objects with a low read probability; the break-even for archive over infrequent is the extra storage saving divided by the retrieval cost per read.
- Failure modes: lifecycle rules that delete versions needed by a registered model; archive tier with long retrieval time blocking a retraining; early-deletion minimums (check current docs).

**Example:** with my relative units (hot 1.00, infrequent 0.50, archive 0.15 per TB-month; retrieval 0.10 and 1.00 per TB read), archive beats infrequent only if the monthly read probability is below (0.50 - 0.15) / 1.00 = 0.35. Total 465 TB all hot is 465 units a month. The balanced policy (infrequent after 30 days, archive after 120) costs 159.3; the aggressive one (archive after 30 days) costs 126.9 here, because only about 2 percent of old raw files get re-read; the oracle that knows the future costs 101.0. In the run 28 archived objects (14 TB) were read, a retrieval penalty of 14.0 units. Egress: reading a 60 TB snapshot across Regions at an assumed 0.60 per TB is 36 units per run, 432 for 12 runs; one copy then local reads costs 36.

**Code:** run with `python3 -I q27.py`. Seeded invented access log of 970 objects scaled to the three totals. Relative units only.
```python
# Q27: storage tiering on an invented access log. Relative cost units per TB-month; NOT prices.
import random
rng = random.Random(27)
HOT, IA, ARC = 1.00, 0.50, 0.15            # storage cost per TB-month (relative units, assumed)
RET_IA, RET_ARC = 0.10, 1.00               # retrieval cost per TB read from that tier (assumed)
EGRESS = 0.60                              # cross-Region transfer per TB (assumed)
# 3 groups sized as in the prompt: 400 TB raw features, 60 TB snapshots, 5 TB artefacts
GROUPS = {"raw": (400, 800), "snap": (60, 120), "art": (5, 50)}
objs = []
for g, (tb, n) in GROUPS.items():
    for i in range(n):
        size = tb / n
        age = rng.randint(1, 400)                       # days since last access, from the log
        if g == "raw":   fut = rng.random() < (0.30 if age < 30 else 0.04 if age < 120 else 0.02)  # a few old files get re-read for retraining
        elif g == "snap": fut = rng.random() < (0.50 if age < 60 else 0.10)
        else:             fut = rng.random() < 0.90      # model artefacts: rollback needs them fast
        objs.append((g, size, age, fut))
def cost(policy):
    s = r = pen = 0.0
    for g, size, age, fut in objs:
        tier = policy(g, age)
        rate, ret = {"hot": (HOT, 0), "ia": (IA, RET_IA), "arc": (ARC, RET_ARC)}[tier]
        s += size * rate
        if fut: r += size * ret                         # one read in the next month
    return s, r, s + r
pols = {
 "all hot":                     lambda g, a: "hot",
 "IA>30d, archive>120d":        lambda g, a: "hot" if g == "art" or a <= 30 else "ia" if a <= 120 else "arc",
 "IA>30d only (no archive)":    lambda g, a: "hot" if g == "art" or a <= 30 else "ia",
 "aggressive: archive>30d":     lambda g, a: "hot" if g == "art" or a <= 30 else "arc",
 "oracle (knows future reads)": None,
}
print(f"{'policy':<30}{'storage':>9}{'retrieval':>10}{'total':>8}")
for k, p in pols.items():
    if p is None:
        s = r = 0.0
        for g, size, age, fut in objs:
            s += size * (HOT if fut else ARC)
        print(f"{k:<30}{s:>9.1f}{0:>10.1f}{s:>8.1f}"); continue
    s, r, t = cost(p); print(f"{k:<30}{s:>9.1f}{r:>10.1f}{t:>8.1f}")
# wrong guesses: archived objects that were read
wrong = [(g, size) for g, size, age, fut in objs if fut and pols["IA>30d, archive>120d"](g, age) == "arc"]
print("archived-then-read objects:", len(wrong), "TB:", round(sum(s for _, s in wrong), 1), "retrieval units:", round(sum(s for _, s in wrong) * RET_ARC, 1))
# egress: training Region differs from data Region, one 60 TB snapshot read per run, 12 runs a month
print("cross-Region read of one 60 TB snapshot:", 60 * EGRESS, "units; 12 runs a month:", 12 * 60 * EGRESS, "units; copy once, then read local:", 60 * EGRESS, "units")
print("break-even monthly read probability: archive beats IA only if P(read) <", round((IA - ARC) / RET_ARC, 2), "; IA beats hot if P(read) <", round((HOT - IA) / RET_IA, 1), "(above 1 means always)")
print("total TB:", round(sum(o[1] for o in objs), 1))
```

**Output (my run):**
```text
policy                          storage retrieval   total
all hot                           465.0       0.0   465.0
IA>30d, archive>120d              144.6      14.7   159.3
IA>30d only (no archive)          253.7       2.1   255.8
aggressive: archive>30d           105.9      21.0   126.9
oracle (knows future reads)       101.0       0.0   101.0
archived-then-read objects: 28 TB: 14.0 retrieval units: 14.0
cross-Region read of one 60 TB snapshot: 36.0 units; 12 runs a month: 432.0 units; copy once, then read local: 36.0 units
break-even monthly read probability: archive beats IA only if P(read) < 0.35 ; IA beats hot if P(read) < 5.0 (above 1 means always)
total TB: 465.0
```
The aggressive policy wins on this invented log; with a higher re-read rate (for example frequent retraining over old data) it would lose, so I look at the real access log and measure before copying a policy.

**Follow-ups:**
- *Why not delete old features?* Reproducibility and audits may need them; delete only after the retention decision is recorded.
- *Intelligent tiering instead of rules?* Fine when access is unpredictable; check the monitoring fee and current behaviour in the docs.
- *How do I find egress?* Tag by Region pair and look at the bill by usage type; set an alert on cross-Region bytes.

**Common mistakes:** lifecycle on a bucket that holds live registry artefacts; archiving data a retrain job reads weekly; ignoring minimum storage durations and retrieval fees; one copy per experiment instead of deduplicated snapshots; training in a different Region from the data.

### Q28 ⭐⭐ 🟡 [Autoscaling simulation] A model service takes 90 seconds to start (model load) and traffic is spiky (invented trace). Simulate scale-to-zero, a minimum of two replicas and predictive pre-scaling in Python and compare cold-start hits, p99 wait and replica-hours. Reference Part 6 Q25, Part 3 Q9 and Part 3 Q19. State the stability traps (flapping, scaling on CPU for an I/O-bound model) and the signal you would scale on.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** With a 90-second model load, scale-to-zero means the first requests after a quiet spell wait a minute and a half, so I keep a small floor of warm replicas, pre-scale for known peaks, and scale on queue depth or requests in flight, not on CPU.
 
**Then explain:**
- Scale-to-zero is cheapest and worst for the first user: every cold start hits the 90 s load. Fine for internal or batch endpoints, risky for user-facing ones (Part 6 Q25).
- Minimum replicas remove cold starts for ordinary traffic but cost idle hours. Predictive pre-scaling (schedule or forecast) starts replicas one startup time before the peak, so it removes the spike wait without paying for a high floor.
- Scaling signal: requests in flight per replica or queue depth (KEDA-style on a queue, Part 3 Q19), or GPU utilisation for GPU models. CPU is a bad signal for an I/O-bound or GPU-bound model: CPU stays low while the queue grows (Part 3 Q9 covers the CPU-bound HPA case).
- Stability traps: flapping (scale down then up within the 90 s startup, so each cycle wastes a boot), scaling on a noisy instantaneous signal (use an average and a cool-down), scaling down while requests are queued, a readiness probe that passes before the model is loaded, and a downstream (database, feature store) that falls over when replicas multiply.
- Rule of thumb: the scaler has to look ahead by startup time, so spikes shorter than 90 s cannot be fixed by reactive scaling at all: use a floor, a queue with backpressure, or load shedding.

**Example:** quiet stretch with zero traffic from t=1200 to t=2300, then a 45 RPS spike at t=2400. One replica serves 10 RPS, so the spike needs 45 / (10 x 0.7) = 6.4, so 7 replicas, or 70 RPS. Reactive scaling sees the spike at t=2400 and has capacity at t=2490; in between requests queue. In the run, scale-to-zero shows 3 requests waiting 90 s or more (the first requests when the service starts cold) and the highest p99; min 2 and predictive plus min 1 have none.

**Code:** run with `python3 -I q28.py`. Seeded, 7,200 one-second steps, an invented trace with quiet time, three scheduled peaks, an oscillating section and one surprise spike. Abstract units; not a benchmark.
```python
# Q28: autoscaling simulation, 1-second steps, seeded. Abstract units. Startup 90 s.
import random, math
from collections import deque
SEED = 28
T = 7200; STARTUP = 90; CAP = 10              # one replica serves 10 requests/s
rng = random.Random(SEED)
def rate(t):                                   # invented spiky trace (rps): quiet base plus 4 known daily-style peaks and 1 surprise
    base = 0.0 if 1200 <= t < 2300 else 1.5                   # a quiet stretch with no traffic at all
    for s in (900, 2400, 4500):
        if s <= t < s + 240: base = 45
    if 3200 <= t < 4200: base = 25 if (t // 60) % 2 == 0 else 5   # load that oscillates around a threshold
    if 5800 <= t < 5900: base = 60             # surprise spike nobody scheduled
    return base
arr = [sum(1 for _ in range(int(rate(t) * 3)) if rng.random() < 1/3) for t in range(T)]   # poisson-ish integer arrivals/s
def sim(name, min_rep, idle_to_zero=None, predictive=False, cooldown=180):
    ready = min_rep; booting = []; q = deque(); waits = []; rep_s = 0; last_busy = 0; events = 0; ewma = 0.0; last_down = -999
    for t in range(T):
        done = [b for b in booting if b <= t]; booting = [b for b in booting if b > t]; ready += len(done)
        for _ in range(arr[t]): q.append(t)
        cap = ready * CAP; served = 0
        while q and served < cap: waits.append(t - q.popleft()); served += 1
        ewma = 0.8 * ewma + 0.2 * arr[t]
        if arr[t] or q: last_busy = t
        want = math.ceil((ewma + len(q) / 30) / (CAP * 0.7))
        if predictive:                                       # forecast from the known schedule 120 s ahead
            f = 45 if any(s - 120 <= t + 120 and t < s + 240 for s in (900, 2400, 4500)) else 1.5
            want = max(want, math.ceil(f / (CAP * 0.7)))
        floor = min_rep
        if idle_to_zero is not None and t - last_busy < idle_to_zero: floor = max(floor, 1)
        want = max(want, floor)
        have = ready + len(booting)
        if want > have:
            booting += [t + STARTUP] * (want - have); events += want - have
        elif want < ready and t - last_down >= cooldown and not q:
            ready -= 1; last_down = t
        rep_s += ready + len(booting)
    for _ in q: waits.append(T - 0)
    w = sorted(waits); n = len(w)
    cold = sum(1 for x in w if x >= STARTUP); slow = sum(1 for x in w if x > 10)
    print(f"{name:<34}{n:>7}{cold:>10}{slow:>9}{w[int(0.99*n)]:>8}{max(w):>7}{rep_s/3600:>10.1f}{events:>8}")
print(f"{'strategy':<34}{'reqs':>7}{'wait>=90s':>10}{'wait>10s':>9}{'p99 s':>8}{'max s':>7}{'rep-hours':>10}{'boots':>8}")
sim("scale to zero (idle 300 s)", 0, idle_to_zero=300)
sim("min 2 replicas", 2)
sim("predictive pre-scale, min 0", 0, idle_to_zero=300, predictive=True)
sim("predictive + min 1", 1, predictive=True)
sim("min 2, NO cooldown (flapping)", 2, cooldown=0)
```

**Output (my run):**
```text
strategy                             reqs wait>=90s wait>10s   p99 s  max s rep-hours   boots
scale to zero (idle 300 s)          59055         3     9369      68     90      18.2      37
min 2 replicas                      59055         0     8752      49     52      15.2      34
predictive pre-scale, min 0         59055         3     5986      60     90      17.0      51
predictive + min 1                  59055         0     5846      60     62      17.0      50
min 2, NO cooldown (flapping)       59055         0    22750      60     62       7.4     101
```
Reading it: `wait>10s` counts requests that waited more than 10 s. Predictive pre-scaling cuts slow requests (5,986 against 9,369 for scale to zero) at a cost between the two. The "no cooldown" row looks cheap (7.4 replica-hours) but boots 101 times and has by far the most slow requests (22,750): the cheap number is the flapping trap. The remaining slow requests come from the oscillating section and the unscheduled spike, which no strategy here covers: that is where a queue with limits or shedding is needed.

**Follow-ups:**
- *Why not scale on CPU?* A model waiting on a GPU or a remote call can have a full queue and idle CPU.
- *How do I shorten the 90 s?* Smaller or quantised model, weights on local disk or a warm image, lazy loading, keeping a standby pool. Measure each.
- *Spot nodes in the pool?* Possible for the elastic part only; keep the floor on stable nodes.

**Common mistakes:** scale-to-zero on a latency-sensitive endpoint; no cool-down; readiness before the model is loaded; scaling replicas past what the database or feature store can take; judging a strategy on average latency instead of p99.

### Q29 ⭐⭐ 🟡 [Model supply chain] Teams download pretrained weights and pickles from public hubs and internal buckets. Explain the risk of pickle deserialisation executing code, unsafe model formats versus safetensors or ONNX, dependency confusion, typosquatted packages, unpinned base images and mutable CI action tags. Reference Part 7 Q31, Part 7 Q32, Part 2 Q32 and Part 6 Q9, plus the OWASP supply-chain and poisoning entries (hedged). In Python build a pickle scanner that lists the global opcodes of a harmless test pickle and flags a denylist, and a pinned-hash requirements check.
**Asked at:** OWASP Top 10 for LLM Applications 2025 summaries (opensourcesecurity substack, Trend Micro, HackerOne, Bright Security, Coralogix; search snippets only, not opened): supply chain moved to LLM03, data and model poisoning LLM04, model theft folded out of the standalone list; no source on classic ML model-extraction attacks surfaced, so extraction questions rest on general knowledge, hedged | ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** A pickle is a program, not data: loading it can run code, so I never load pickles from outside my trust boundary, prefer safetensors or ONNX, pin every dependency by hash and digest, and scan before anything is loaded.

**Then explain:**
- Pickle risk: the format can reference any importable callable and call it on load. Joblib and some torch checkpoints use pickle underneath. Check the current docs of each library for safer load options.
- Safer formats: safetensors (weights only, no code) and ONNX (a graph of operators, no Python), but they are not magic: a custom operator, a bad parser or poisoned weights still need review (Part 6 Q9). Signing and provenance of the artefact are separate controls (Part 7 Q32).
- Dependency confusion: a public package with the same name as an internal one wins if the resolver looks at the public index first. Typosquats (`reqests`) work the same way. Defence: private index with explicit priority, exact pins with hashes, an allowlist of names.
- Unpinned base images and mutable CI action tags: a tag can be moved. Pin images by digest and actions by commit SHA (Part 2 Q32, Part 7 Q31).
- OWASP's LLM list (2025 edition, hedged: I only saw summaries) names supply chain and data and model poisoning as separate risks. Poisoned training data is not caught by a pickle scanner: that needs data provenance and evaluation.
- What a scanner cannot do: it uses a denylist, so a novel callable passes. An allowlist of globals is stronger, and the safest rule is not to unpickle untrusted data at all. Treat scan results as a filter, not a guarantee.

**Example:** `pickle.dumps(Harmless())` where `__reduce__` returns `os.getcwd` produces a pickle whose global is `posix.getcwd` (on Linux); the scanner lists it with its byte position and flags it because module `posix` is denied. Nothing is ever unpickled. A plain dict of weights and a name has no global at all, so it is clean. In requirements, `requests>=2.0` and `torch` fail the pin rule, `reqests` is not on the approved list, and `actions/checkout@v4` is a mutable tag.

**Code:** run with `python3 -I q29.py`. Uses `pickletools` to read opcodes (never `pickle.loads`), `re` and `hashlib`. The test pickles are harmless.
```python
# Q29: pickle opcode scanner + pinned-hash requirements check + mutable action tag check. Nothing is ever unpickled.
import pickle, pickletools, hashlib, re
DENY_MODULES = {"os", "posix", "nt", "subprocess", "sys", "socket", "shutil", "builtins", "importlib", "ctypes", "pty", "runpy"}
DENY_BUILTINS = {"eval", "exec", "open", "__import__", "compile", "getattr"}
ALLOW = {("collections", "OrderedDict"), ("numpy", "dtype"), ("numpy.core.multiarray", "_reconstruct"), ("numpy", "ndarray")}
def globals_in(data):
    out, strs = [], []
    for op, arg, pos in pickletools.genops(data):
        if op.name in ("SHORT_BINUNICODE", "BINUNICODE", "UNICODE", "SHORT_BINSTRING", "BINSTRING"): strs.append(arg)
        elif op.name == "GLOBAL": m, n = arg.split(" ", 1); out.append((m, n, pos))
        elif op.name == "STACK_GLOBAL" and len(strs) >= 2: out.append((strs[-2], strs[-1], pos))
    return out
def scan(data):
    findings = []
    for m, n, pos in globals_in(data):
        root = m.split(".")[0]
        bad = root in DENY_MODULES or (m == "builtins" and n in DENY_BUILTINS)
        findings.append((pos, f"{m}.{n}", "DENY" if bad else "ok" if (m, n) in ALLOW else "REVIEW"))
    return findings
class Harmless:                       # when LOADED it would call os.getcwd(): harmless, but it shows the mechanism
    def __reduce__(self):
        import os; return (os.getcwd, ())
good = pickle.dumps({"weights": [0.1, 0.2], "name": "m1"}, protocol=2)
bad2 = pickle.dumps(Harmless(), protocol=2)
bad4 = pickle.dumps(Harmless(), protocol=4)
for label, d in (("plain dict, protocol 2", good), ("reduce->os.getcwd, protocol 2", bad2), ("reduce->os.getcwd, protocol 4", bad4)):
    print(label, "->", scan(d) or "no globals")
# pinned-hash requirements check
REQ = """numpy==1.26.4 --hash=sha256:aaaa
requests>=2.0
torch
internal-lib==1.0 --hash=sha256:bbbb
git+https://example.invalid/x.git
reqests==2.31.0 --hash=sha256:cccc"""
KNOWN = {"numpy", "requests", "torch", "internal-lib"}
for line in REQ.splitlines():
    name = re.split(r"[=<>@ ]", line)[0]; issues = []
    if line.startswith(("git+", "http")): issues.append("URL install, no hash")
    elif "==" not in line: issues.append("not pinned with ==")
    if "--hash=sha256:" not in line and not issues: issues.append("no hash")
    if "==" in line and name not in KNOWN: issues.append("name not in approved index list (typosquat?)")
    print(f"{line[:38]:<40}", "OK" if not issues else "; ".join(issues))
# artefact hash check
blob = b"pretend-weights"; want = hashlib.sha256(blob).hexdigest()
print("hash match:", hashlib.sha256(blob).hexdigest() == want, "| tampered:", hashlib.sha256(blob + b"x").hexdigest() == want)
# mutable CI action tags
WF = ["uses: actions/checkout@v4", "uses: actions/setup-python@" + "a" * 40, "uses: some-org/deploy@main"]
for l in WF: print(l[:50], "->", "pinned SHA" if re.search(r"@[0-9a-f]{40}$", l) else "MUTABLE tag/branch")
```

**Output (my run):**
```text
plain dict, protocol 2 -> no globals
reduce->os.getcwd, protocol 2 -> [(2, 'posix.getcwd', 'DENY')]
reduce->os.getcwd, protocol 4 -> [(28, 'posix.getcwd', 'DENY')]
numpy==1.26.4 --hash=sha256:aaaa         OK
requests>=2.0                            not pinned with ==
torch                                    not pinned with ==
internal-lib==1.0 --hash=sha256:bbbb     OK
git+https://example.invalid/x.git        URL install, no hash
reqests==2.31.0 --hash=sha256:cccc       name not in approved index list (typosquat?)
hash match: True | tampered: False
uses: actions/checkout@v4 -> MUTABLE tag/branch
uses: actions/setup-python@aaaaaaaaaaaaaaaaaaaaaaa -> pinned SHA
uses: some-org/deploy@main -> MUTABLE tag/branch
```
The hash lines in the requirements are made-up placeholders, so this checks the format of the pins, not real package hashes. A real check is `pip install --require-hashes` against a lock file.

**Follow-ups:**
- *Do I need the scanner if I use safetensors?* Keep it for legacy artefacts and for anything a vendor sends in a pickle-based format.
- *Where does it run?* In CI before the artefact is registered and again at load time in a sandbox without network.
- *Is hash pinning enough?* It proves the same bytes, not that the bytes are good: add provenance, review and scanning.

**Common mistakes:** `pickle.load` on a downloaded model; trusting a tag like `latest` or `v4`; one index with both public and private packages and no priority rule; scanning only for `os.system`; treating a model hub's popularity as safety.

### Q30 ⭐⭐ 🟡 [PII and data residency architecture] A fintech GCC in India (invented) must keep customer-identifiable data in India, train models on pseudonymised data, serve from several Regions and use a global vendor's managed ML service. Draw the data-flow, say what is tokenised where, which logs may leave, how keys are controlled and how you prove residency to an auditor. Hedge the law: DPDP defaults, sector rules and what to verify (Part 11 Q30). Reference Part 10 Q38 (KMS), Part 10 Q39 and Part 8 Q29. Write a policy-as-data YAML of allowed flows and a validator that rejects a flow sending a restricted field to a non-India Region.
**Asked at:** India data-protection and data-localisation commentary (treelife, sflc.in, ksandk, an ELP Law note, Grant Thornton guide; search snippets only, not opened): DPDP Act allows cross-border transfer by default subject to Section 16 orders and significant-data-fiduciary limits; sources put commencement of those provisions at 13 May 2027 but this is hedged 'check current law'; sector rules (RBI payment-data direction of 2018, SEBI cloud framework) as reported by advisers; legal explainers, not interview reports | Coverage of the RBI FREE-AI framework of 13 Aug 2025 (law.asia, storyboard18, cxodigitalpulse, securiti, mitsloanme; search snippets only, not opened): seven principles, 26 recommendations in six pillars, board-approved AI policy, AI-specific audit, disclosures; no snippet gave model-risk or localisation text, so those parts are hedged 'check the RBI site'; regulated BFSI and GCC credit and fraud roles | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Customer-identifiable data stays in India; models train on pseudonymised or tokenised data; the token vault and its keys stay in India; and a policy file lists the allowed flows so a check can reject anything else before it ships.

**Then explain:**
- Data flow: source systems and the raw store in an India Region; a tokenisation service in India replaces PAN, account number, phone and name with tokens; the training and feature stores hold tokens and internal fields; serving in several Regions gets only what it needs, and the detokenise call stays in India.
- What leaves: aggregates, tokenised features, model artefacts and metrics. Logs that leave carry only internal-class fields (no names, no raw identifiers; Part 8 Q29).
- Keys: customer-managed keys in an India Region, key policy limiting who can use them, separate keys per data class, rotation and audit logs (Part 10 Q38). A vendor-managed service gets only tokenised data and network isolation (Part 10 Q39).
- Proving residency to an auditor: the policy file in Git with review history, CI output showing every flow validated, resource inventory by Region, key locations, access and transfer logs, and a periodic scan for restricted fields outside India. Evidence, not a diagram.
- Law, hedged: the DPDP Act, as reported by advisers, allows cross-border transfer by default except to countries the government restricts, with possible extra rules for significant data fiduciaries; some provisions were reported to start from 13 May 2027; sector rules (RBI payment-data direction, SEBI cloud framework) can require India storage for their data, and RBI's FREE-AI framework of 13 Aug 2025 adds governance expectations. I only saw adviser summaries, so I would check the regulator's site and current law, and ask legal.
- Failure modes: a "temporary" copy in another Region, backups and replication to a global Region, a vendor sub-processor, debug logs with names, a new field nobody classified (the validator rejects unclassified fields by default).

**Example:** the run checks 7 flows. Allowed: restricted data moved between two India Regions with the key in India, and a tokenised flow to a global ML Region with the vault in India. Rejected: raw PAN to the global Region; tokenised phone where the vault itself is in the EU Region; a log to the US Region carrying `customer_name`; an account-number store with its key in the US Region; and a field `salary_band` that nobody classified.

**Code:** run in a temp dir with `python3 -I q30.py` next to `q30_policy.yaml`. Region names are generic labels. This is an engineering check, not legal advice.
```yaml
# Allowed data flows, policy as data. Region ids are generic labels, not any vendor's names.
regions:
  in-west: {country: IN}
  in-south: {country: IN}
  eu-1: {country: EU}
  us-1: {country: US}
fields:
  pan_number:     restricted
  account_number: restricted
  phone:          restricted
  customer_name:  restricted
  txn_amount:     internal
  merchant_cat:   internal
  device_hash:    internal
rules:
  restricted_stays_in_india: true          # a restricted field may only sit in an IN region ...
  allow_tokenised_abroad: true             # ... unless it is tokenised with the vault and key in India
  keys_must_be_in_country: IN              # KMS key for any restricted store lives in an IN region
  logs_may_leave: [internal]               # only these classes in logs that leave India
```
```python
# Q30: validate invented data flows against policy-as-data. Plain Python + pyyaml. Not legal advice.
import yaml, pathlib
P = yaml.safe_load(pathlib.Path("q30_policy.yaml").read_text())
IN = {r for r, v in P["regions"].items() if v["country"] == "IN"}
def check(f):
    v = []
    for r in (f["from"], f["to"]):
        if r not in P["regions"]: v.append(f"unknown region {r}")
    unknown = [x for x in f["fields"] if x not in P["fields"]]
    if unknown: v.append(f"unclassified fields {unknown} (default deny)")
    restricted = [x for x in f["fields"] if P["fields"].get(x) == "restricted"]
    if f["to"] in P["regions"] and f["to"] not in IN and restricted:
        ok = P["rules"]["allow_tokenised_abroad"] and f.get("transform") == "tokenised" and f.get("vault_region") in IN
        if not ok: v.append(f"restricted {restricted} to non-India region {f['to']} (transform={f.get('transform')})")
    if f.get("kind") == "store" and restricted and f.get("key_region") not in IN:
        v.append(f"restricted store with key in {f.get('key_region')}, rule wants country {P['rules']['keys_must_be_in_country']}")
    if f.get("kind") == "log" and f["to"] not in IN:
        bad = [x for x in f["fields"] if P["fields"].get(x) not in P["rules"]["logs_may_leave"]]
        if bad: v.append(f"log leaving India carries {bad}")
    return v
FLOWS = [
 {"name": "train-data-in-india",        "from": "in-west", "to": "in-south", "fields": ["pan_number", "txn_amount"], "kind": "store", "key_region": "in-west"},
 {"name": "raw-pan-to-global-ml",       "from": "in-west", "to": "us-1", "fields": ["pan_number", "txn_amount"], "transform": "none"},
 {"name": "tokenised-to-global-ml",     "from": "in-west", "to": "us-1", "fields": ["txn_amount", "merchant_cat"], "transform": "tokenised", "vault_region": "in-west"},
 {"name": "tokenised-vault-abroad",     "from": "in-west", "to": "eu-1", "fields": ["phone"], "transform": "tokenised", "vault_region": "eu-1"},
 {"name": "logs-with-name",             "from": "in-south", "to": "us-1", "fields": ["customer_name", "device_hash"], "kind": "log"},
 {"name": "store-key-abroad",           "from": "in-west", "to": "in-south", "fields": ["account_number"], "kind": "store", "key_region": "us-1"},
 {"name": "new-field-nobody-classified","from": "in-west", "to": "in-south", "fields": ["salary_band"]},
]
for f in FLOWS:
    v = check(f); print(f"{f['name']:<30}", "ALLOW" if not v else "REJECT")
    for x in v: print("    -", x)
```

**Output (my run):**
```text
train-data-in-india            ALLOW
raw-pan-to-global-ml           REJECT
    - restricted ['pan_number'] to non-India region us-1 (transform=none)
tokenised-to-global-ml         ALLOW
tokenised-vault-abroad         REJECT
    - restricted ['phone'] to non-India region eu-1 (transform=tokenised)
logs-with-name                 REJECT
    - restricted ['customer_name'] to non-India region us-1 (transform=None)
    - log leaving India carries ['customer_name']
store-key-abroad               REJECT
    - restricted store with key in us-1, rule wants country IN
new-field-nobody-classified    REJECT
    - unclassified fields ['salary_band'] (default deny)
```

**Follow-ups:**
- *Is tokenisation enough for the law?* Not by itself: tokens that can be re-identified with a vault are still personal data in many readings; ask legal.
- *Can I use a global managed ML service?* Often yes with tokenised data, private connectivity and keys in India; check the vendor's data-processing terms and current Region options.
- *What does the policy not catch?* Data copied by hand, or a field mislabelled as internal.

**Common mistakes:** drawing a diagram with no evidence; treating "encrypted" as "in India"; keys in the vendor's global Region; logs and traces forgotten; stating the law as settled instead of saying "check current law".

### Q31 ⭐⭐ 🟡 [Model theft and extraction] An internal fraud-scoring API returns a probability to 300 partner apps (invented). Describe model extraction by repeated queries, membership inference and artefact theft, and defences: authentication and per-key quotas, rounding or bucketing outputs, query-pattern anomaly detection, watermarks, minimal logging of full vectors and artefact encryption and access control. Reference Part 6 Q39 and Part 8 Q44. Build a small extraction demo in Python (query a logistic model, fit a surrogate, report agreement) and show how output rounding and a rate limit reduce surrogate fidelity.
**Asked at:** OWASP Top 10 for LLM Applications 2025 summaries (opensourcesecurity substack, Trend Micro, HackerOne, Bright Security, Coralogix; search snippets only, not opened): supply chain moved to LLM03, data and model poisoning LLM04, model theft folded out of the standalone list; no source on classic ML model-extraction attacks surfaced, so extraction questions rest on general knowledge, hedged | ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** Anyone who can query a model can copy it: attackers fit a surrogate on the answers, so I limit how many answers one key gets, give less precise answers, watch for query patterns, and protect the artefact itself.

**Then explain:**
- Extraction: send many inputs, record the outputs, train a copy. The more precise the output (full probabilities), the fewer queries it takes. For a linear model the sigmoid can be inverted and the weights come out exactly.
- Membership inference: use the confidence on a record to guess whether it was in the training data (overfit models leak more). Artefact theft is a different path: a leaked file or bucket, which is solved by access control and encryption, not by rounding.
- Defences: authentication and per-key quotas (Part 6 Q39), rounding or bucketing outputs, returning a label or a decision instead of a score where the partner does not need a score, anomaly detection on query patterns (many near-uniform random inputs, systematic grid sweeps), watermarking or canary outputs to prove a copy, minimal logging of full vectors, and encrypted artefacts with narrow access.
- Fraud adds a twist: attackers who probe the scorer are also learning how to evade it (Part 8 Q44), so the same controls protect detection quality.
- Failure modes: quotas per IP instead of per account (bypassed by rotating addresses), many keys per attacker, rounding so coarse that honest partners lose value, and false confidence: defences raise cost, they do not make copying impossible. This answer rests on general knowledge, not on a source I could open.

**Example:** the victim is a 20-feature logistic model. With full probabilities, even 25 queries recover the weights (cosine 1.000, agreement 1.000): 21 unknowns, 25 equations. Rounding to one decimal gives 0.957 agreement at 200 queries and 0.753 at 25. A label-only answer with 25 queries gives 0.772. So here the quota (small query counts) does more than rounding.

**Code:** run with `python3 -I q31.py` (needs numpy and scikit-learn). Seeded synthetic data. Agreement is the share of 5,000 test points where the surrogate and the victim give the same label.
```python
# Q31: model extraction demo. Victim = logistic regression on synthetic data. Seeded. Sandbox numbers only.
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
rng = np.random.default_rng(31)
D = 20
w = rng.normal(0, 1, D); b = 0.3
Xtr = rng.normal(0, 1, (5000, D)); ytr = (rng.random(5000) < 1 / (1 + np.exp(-(Xtr @ w + b)))).astype(int)
victim = LogisticRegression(max_iter=1000).fit(Xtr, ytr)
def api(X, mode):                                   # what a partner sees
    p = victim.predict_proba(X)[:, 1]
    if mode == "full": return p
    if mode == "round1": return np.round(p, 1)
    if mode == "bucket3": return np.digitize(p, [0.33, 0.66]) / 2.0          # low / mid / high
    if mode == "label": return (p >= 0.5).astype(float)
Xtest = rng.normal(0, 1, (5000, D)); vlab = victim.predict(Xtest)
def attack(mode, nq):
    X = rng.normal(0, 1, (nq, D)); y = api(X, mode)
    if mode == "full":                              # invert the sigmoid: exact linear system
        z = np.log(np.clip(y, 1e-9, 1 - 1e-9) / np.clip(1 - y, 1e-9, 1)); s = LinearRegression().fit(X, z)
        wh = s.coef_; pred = (Xtest @ wh + s.intercept_ > 0).astype(int)
    else:
        yl = (y >= 0.5).astype(int)
        if yl.min() == yl.max(): return float("nan"), float("nan")
        s = LogisticRegression(max_iter=2000, C=100).fit(X, yl); wh = s.coef_[0]; pred = s.predict(Xtest)
    cos = float(wh @ victim.coef_[0] / (np.linalg.norm(wh) * np.linalg.norm(victim.coef_[0])))
    return float((pred == vlab).mean()), cos
print(f"{'output given to partner':<26}{'queries':>8}{'agreement':>10}{'weight cosine':>14}")
for mode in ("full", "round1", "bucket3", "label"):
    for nq in (20000, 200, 25):
        a, c = attack(mode, nq); print(f"{mode:<26}{nq:>8}{a:>10.3f}{c:>14.3f}")
```

**Output (my run):**
```text
output given to partner    queries agreement weight cosine
full                         20000     1.000         1.000
full                           200     1.000         1.000
full                            25     1.000         1.000
round1                       20000     0.976         1.000
round1                         200     0.957         0.992
round1                          25     0.753         0.692
bucket3                      20000     0.915         1.000
bucket3                        200     0.914         0.994
bucket3                         25     0.752         0.788
label                        20000     1.000         1.000
label                          200     0.962         0.994
label                           25     0.772         0.777
```
Honest limits: a linear victim is the easiest case, one random-input attacker, no anomaly detection, nothing adaptive. The `bucket3` row is also pushed down by how I turned buckets into labels. Real models are not this easy to copy, but the direction of the lesson holds: precision and query volume are what you control.

**Follow-ups:**
- *Rate limit or rounding first?* Both, and a quota per account with identity checks; rounding alone leaves a 200-query attacker at about 0.96 agreement here.
- *Does a watermark stop theft?* No, it helps you prove it later.
- *What do I log?* Who, when, how many queries, an input hash; not full feature vectors, to limit privacy risk (Part 8 Q29).

**Common mistakes:** returning full-precision probabilities to every partner; limits per IP only; logging whole requests forever; believing that hiding the architecture is a defence; forgetting the artefact in the bucket.

### Q32 ⭐⭐ 🟡 [Policy as code for ML deployments] Write a deployment policy in YAML (required tags, owner, data classification, allowed Regions, no public endpoint for restricted data, image from approved registry with digest pinning, max GPU count without approval) and a validator in pydantic plus plain Python that returns all violations for several invented manifests. Reference Part 3 Q35, Part 7 Q29 and Part 10 Q48. Explain where it runs (pre-commit, CI, admission control), how exceptions are granted and expire, and what policy cannot catch.
**Asked at:** ML system-design prep guides and course pages (Educative 'end-to-end examples of ML system design', DataTalks.Club ML system design podcast page, a dev.to 'ML system design interview questions' post, a Maven ML design course page; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); editorial and paid-course material, not verified candidate reports | OWASP Top 10 for LLM Applications 2025 summaries (opensourcesecurity substack, Trend Micro, HackerOne, Bright Security, Coralogix; search snippets only, not opened): supply chain moved to LLM03, data and model poisoning LLM04, model theft folded out of the standalone list; no source on classic ML model-extraction attacks surfaced, so extraction questions rest on general knowledge, hedged | Builds on the question families already recorded for Parts 1 to 11 (see research_notes/Book4_Part12_sources.md for how each earlier part's sources are reused); integrated design question, not a verified company report
**Say this first (1 line):** I write the deployment rules as data in YAML, validate each manifest in a pydantic model plus plain Python rules that return all violations at once, and run it in pre-commit, CI and the cluster admission step, with exceptions that name an owner and expire.

**Then explain:**
- Policy in YAML (required tags, allowed Regions, approved registries, digest pinning, no public endpoint for restricted data, GPU cap) so security and platform can review the rules without reading code. Policy is versioned in Git with required reviewers (Part 7 Q29).
- Pydantic checks the shape and types (a `gpus: many` is a schema error); plain Python checks the rules and collects every violation, so the author fixes everything in one go.
- Where it runs: pre-commit (fast feedback, easy to skip), CI (cannot be skipped for merged code), admission control in the cluster or an organisation-level guardrail (the last line of defence, Part 3 Q35, Part 10 Q48). Same rules in all three, or they drift.
- Exceptions: a named rule, a named manifest, an approver and an expiry date. An expired exception fails again. Review the exception list monthly.
- What policy cannot catch: a wrong label (data marked `public` when it is restricted), a correct manifest running bad code, a compromised approved registry, runtime behaviour, and a rule nobody wrote. Policy stops mistakes, not attackers.

**Example:** with a fixed date of 2026-10-26 the run gives: `fraud-api` allowed; `scratch-notebook` rejected with 6 violations (three missing tags, US Region, unapproved registry, no digest); `big-train-job` allowed because its 16-GPU exception runs until 2026-11-30; `eu-pilot` rejected because its Region exception expired on 2026-09-01; `leaky-scorer` rejected for a tag-only image and a public endpoint on restricted data; `bad-types` stopped at schema level. Note `scratch-notebook` has a public endpoint but no classification tag, so that rule does not fire: it is fixed by making the tag required (which it does).

**Code:** run in a temp dir with `python3 -I q32.py` next to `q32_policy.yaml` (needs pyyaml and pydantic v2). Region and registry names are invented.
```yaml
# Deployment policy (invented). Region ids are generic labels.
required_tags: [owner, cost_center, data_classification, env]
data_classifications: [public, internal, restricted]
allowed_regions: [in-west, in-south]
approved_registries: ["registry.internal.example/"]
require_digest: true                # image must be name@sha256:<64 hex>
restricted_no_public_endpoint: true
max_gpus_without_approval: 4
exceptions:                         # every exception names a rule, a manifest and an expiry
  - {rule: max_gpus, manifest: big-train-job, expires: "2026-11-30", approved_by: platform-lead}
  - {rule: allowed_region, manifest: eu-pilot, expires: "2026-09-01", approved_by: security}
```
```python
# Q32: policy as code. pydantic checks shape and types; plain Python checks the rules; all violations are returned.
import re, yaml, pathlib, datetime
from pydantic import BaseModel, ValidationError
from typing import Optional
TODAY = datetime.date(2026, 10, 26)                   # fixed so the output is repeatable
POL = yaml.safe_load(pathlib.Path("q32_policy.yaml").read_text())
class Manifest(BaseModel):
    name: str
    image: str
    region: str
    gpus: int = 0
    public_endpoint: bool = False
    tags: dict[str, str] = {}
def rules(m: Manifest):
    v = []
    for t in POL["required_tags"]:
        if t not in m.tags: v.append(("required_tag", f"missing tag {t}"))
    dc = m.tags.get("data_classification")
    if dc and dc not in POL["data_classifications"]: v.append(("required_tag", f"bad data_classification {dc}"))
    if m.region not in POL["allowed_regions"]: v.append(("allowed_region", f"region {m.region} not allowed"))
    if not any(m.image.startswith(r) for r in POL["approved_registries"]): v.append(("registry", f"image {m.image.split('@')[0]} not from an approved registry"))
    if POL["require_digest"] and not re.search(r"@sha256:[0-9a-f]{64}$", m.image): v.append(("digest", "image not pinned by digest"))
    if POL["restricted_no_public_endpoint"] and dc == "restricted" and m.public_endpoint: v.append(("public_endpoint", "restricted data behind a public endpoint"))
    if m.gpus > POL["max_gpus_without_approval"]: v.append(("max_gpus", f"{m.gpus} GPUs > {POL['max_gpus_without_approval']}"))
    return v
def apply_exceptions(name, vs):
    out = []
    for rule, msg in vs:
        ex = [e for e in POL["exceptions"] if e["rule"] == rule and e["manifest"] == name]
        if ex and datetime.date.fromisoformat(ex[0]["expires"]) >= TODAY: out.append((rule, msg + f"  [waived by {ex[0]['approved_by']} until {ex[0]['expires']}]", True))
        elif ex: out.append((rule, msg + f"  [exception EXPIRED {ex[0]['expires']}]", False))
        else: out.append((rule, msg, False))
    return out
D = "@sha256:" + "a" * 64; REG = "registry.internal.example/ml/"
MANIFESTS = [
 {"name": "fraud-api", "image": REG + "fraud" + D, "region": "in-west", "gpus": 0, "tags": {"owner": "risk-ml", "cost_center": "cc42", "data_classification": "restricted", "env": "prod"}},
 {"name": "scratch-notebook", "image": "docker.io/library/python:latest", "region": "us-1", "gpus": 1, "public_endpoint": True, "tags": {"owner": "ds-7"}},
 {"name": "big-train-job", "image": REG + "train" + D, "region": "in-south", "gpus": 16, "tags": {"owner": "ds-2", "cost_center": "cc9", "data_classification": "internal", "env": "dev"}},
 {"name": "eu-pilot", "image": REG + "pilot" + D, "region": "eu-1", "gpus": 2, "tags": {"owner": "ds-3", "cost_center": "cc9", "data_classification": "public", "env": "dev"}},
 {"name": "leaky-scorer", "image": REG + "score:v3", "region": "in-west", "gpus": 1, "public_endpoint": True, "tags": {"owner": "ds-4", "cost_center": "cc1", "data_classification": "restricted", "env": "prod"}},
 {"name": "bad-types", "image": REG + "x" + D, "region": "in-west", "gpus": "many", "tags": {}},
]
for raw in MANIFESTS:
    try: m = Manifest(**raw)
    except ValidationError as e:
        print(f"{raw['name']:<17} REJECT (schema)"); [print("    -", er["loc"], er["msg"]) for er in e.errors()]; continue
    res = apply_exceptions(m.name, rules(m)); blocking = [r for r in res if not r[2]]
    print(f"{m.name:<17}", "ALLOW" if not blocking else f"REJECT ({len(blocking)} violations)", "" if not res or blocking else f"(with {len(res)} waived)")
    for rule, msg, waived in res: print("   ", "waived" if waived else "  FAIL", rule, "-", msg)
```

**Output (my run):**
```text
fraud-api         ALLOW 
scratch-notebook  REJECT (6 violations) 
      FAIL required_tag - missing tag cost_center
      FAIL required_tag - missing tag data_classification
      FAIL required_tag - missing tag env
      FAIL allowed_region - region us-1 not allowed
      FAIL registry - image docker.io/library/python:latest not from an approved registry
      FAIL digest - image not pinned by digest
big-train-job     ALLOW (with 1 waived)
    waived max_gpus - 16 GPUs > 4  [waived by platform-lead until 2026-11-30]
eu-pilot          REJECT (1 violations) 
      FAIL allowed_region - region eu-1 not allowed  [exception EXPIRED 2026-09-01]
leaky-scorer      REJECT (2 violations) 
      FAIL digest - image not pinned by digest
      FAIL public_endpoint - restricted data behind a public endpoint
bad-types         REJECT (schema)
    - ('gpus',) Input should be a valid integer, unable to parse string as an integer
```

**Follow-ups:**
- *Why not only admission control?* Late feedback: developers find out at deploy time. Run early too.
- *How do I keep rules and code in sync?* One policy file, one validator package, tests with good and bad manifests.
- *Who grants exceptions?* Not the author: platform or security, recorded and time-limited.

**Common mistakes:** rules that only warn and are ignored; exceptions with no expiry; policy checked in CI but not in the cluster; tags checked for presence but not value; a validator that stops at the first error.

### Q33 ⭐ 🟡 [Platform versus embedded teams] A company has 40 data scientists in five product teams and a two-person platform team (invented). Argue for a central platform team, embedded ML engineers or a hybrid: ownership of pipelines, on-call, standards, golden paths, internal customers, how you measure platform success (adoption, lead time, incident rate, cost per experiment) and the failure modes (ticket queue bottleneck, unused platform). Reference Part 5 Q33 and Part 3 Q39. Produce a RACI table in YAML and validate it.
**Asked at:** Job-posting and community patterns for MLOps, platform and ML-engineering roles at Indian GCCs, product companies and IT-services firms and at global product companies; inferred from search snippets about system-design and FinOps rounds, not from a verified company report | MLOps maturity and tech-debt sources (ZenML maturity-models post, NannyML '5 levels of MLOps maturity', Towards Data Science, arXiv 2503.15577; search snippets only, not opened): Google levels 0 to 2 (manual, pipeline automation, full CI/CD) and Microsoft's five levels as reported secondhand; the Sculley et al. 2015 'Hidden technical debt' paper itself was not found, so only the commonly cited ideas are used
**Say this first (1 line):** For 40 data scientists in five teams and a two-person platform team I would go hybrid: platform builds a thin paved road and standards, embedded ML engineers in each product team own that team's pipelines and on-call, and I measure success by adoption and lead time, not by what the platform ships.

**Then explain:**
- Central only: consistent, but two people become a ticket queue for 40 people (the arithmetic below). Embedded only: fast, but five teams build five slightly different pipelines and nobody owns cost or security standards.
- Hybrid: platform owns the golden path (pipeline template, serving runtime, registry, cost tags, security scans; Part 5 Q33, Part 3 Q39). Embedded ML engineers own team pipelines and model endpoints on call. Platform on-call covers the platform, not each model.
- Self-service over tickets: templates, docs and defaults handle most requests; the platform team handles the hard ones. Product teams are the customers: a roadmap and a feedback loop, not a mandate.
- Success measures: share of teams on the golden path, lead time from idea to production, incident rate per model, cost per experiment, age of open platform tickets.
- Failure modes: ticket-queue bottleneck, a platform nobody uses (built without customers), embedded engineers drifting into pure feature work, on-call load falling on whoever is nearest, and standards without enforcement.

**Example:** 40 data scientists send about 0.4 requests per person per week = 16 tickets a week; two platform engineers clear about 6 each = 12 a week, so utilisation 1.33 and the queue grows without limit. If self-service handles 70 percent, 4.8 tickets a week reach the platform, utilisation 0.40. (All rates invented.)

**Code:** run in a temp dir with `python3 -I q33.py` next to `q33_raci.yaml` (needs pyyaml). The validator checks: one accountable role per activity, at least one responsible role, known roles only, no role twice in one row and no unused role.
```yaml
# Hybrid model: platform team owns paved road; product teams own models; embedded MLEs bridge. R=does, A=one owner, C=consulted, I=informed.
roles: [product_ds, embedded_mle, platform, security, oncall_sre, eng_manager]
activities:
  - {name: feature_and_model_code,        R: [product_ds, embedded_mle], A: product_ds,    C: [platform], I: []}
  - {name: training_pipeline_template,    R: [platform],               A: platform,       C: [embedded_mle], I: [product_ds]}
  - {name: team_pipeline_using_template,  R: [embedded_mle],           A: embedded_mle,   C: [platform], I: [eng_manager]}
  - {name: model_serving_runtime,         R: [platform],               A: platform,       C: [oncall_sre, embedded_mle], I: [product_ds]}
  - {name: model_quality_and_drift,       R: [product_ds],             A: product_ds,     C: [embedded_mle], I: [eng_manager]}
  - {name: model_endpoint_oncall,         R: [embedded_mle],           A: eng_manager,    C: [platform], I: [product_ds]}
  - {name: platform_oncall,               R: [oncall_sre],             A: platform,       C: [], I: [eng_manager]}
  - {name: security_standards_and_scans,  R: [security],               A: security,       C: [platform], I: [product_ds, embedded_mle]}
  - {name: cost_attribution_and_budgets,  R: [platform],               A: eng_manager,    C: [product_ds], I: []}
metrics: [adoption_share_of_teams_on_golden_path, lead_time_idea_to_prod, incident_rate_per_model, cost_per_experiment, platform_ticket_age]
```
```python
# Q33: RACI as YAML, validated: known roles, exactly one A (a single role), at least one R, no role twice in one row, every role used.
import yaml, pathlib, copy
def validate(doc):
    errs = []; roles = set(doc["roles"]); used = set()
    for a in doc["activities"]:
        n = a["name"]
        if isinstance(a.get("A"), list): errs.append(f"{n}: A must be ONE role, got list {a['A']}")
        accountable = a.get("A")
        if not accountable: errs.append(f"{n}: no accountable owner")
        if not a.get("R"): errs.append(f"{n}: nobody is Responsible")
        for k in "RCI":
            for r in a.get(k, []):
                if r not in roles: errs.append(f"{n}: unknown role {r} in {k}")
                used.add(r)
        if isinstance(accountable, str):
            if accountable not in roles: errs.append(f"{n}: unknown role {accountable} in A")
            used.add(accountable)
        names = [x for k in "RCI" for x in a.get(k, [])]
        if len(names) != len(set(names)): errs.append(f"{n}: a role appears in more than one of R, C, I")
    for r in roles - used: errs.append(f"role {r} has no part in any activity")
    if len({a['name'] for a in doc['activities']}) != len(doc['activities']): errs.append("duplicate activity names")
    return errs
doc = yaml.safe_load(pathlib.Path("q33_raci.yaml").read_text())
print("good RACI:", validate(doc) or "no errors", "| activities:", len(doc["activities"]), "| metrics:", len(doc["metrics"]))
bad = copy.deepcopy(doc)
bad["activities"][0]["A"] = ["product_ds", "platform"]
bad["activities"][1]["R"] = []
bad["activities"][2]["C"] = ["data_wizard"]
bad["activities"][6]["A"] = None
bad["activities"][7]["I"] = ["security"]
for e in validate(bad): print("bad RACI:", e)
# queue arithmetic for the ticket-bottleneck failure mode (invented): 40 DS x 0.4 requests/week, platform does 2 people x 6 tickets/week
arr, cap = 40 * 0.4, 2 * 6
print(f"tickets/week in={arr:.1f} out={cap} -> utilisation {arr/cap:.2f}; with self-service handling 70% of requests: in={arr*0.3:.1f}, utilisation {arr*0.3/cap:.2f}")
```

**Output (my run):**
```text
good RACI: no errors | activities: 9 | metrics: 5
bad RACI: feature_and_model_code: A must be ONE role, got list ['product_ds', 'platform']
bad RACI: training_pipeline_template: nobody is Responsible
bad RACI: team_pipeline_using_template: unknown role data_wizard in C
bad RACI: platform_oncall: no accountable owner
bad RACI: security_standards_and_scans: a role appears in more than one of R, C, I
tickets/week in=16.0 out=12 -> utilisation 1.33; with self-service handling 70% of requests: in=4.8, utilisation 0.40
```

**Follow-ups:**
- *When does the platform team grow?* When adoption is high and the ticket age is rising; not before teams use what exists.
- *Who is on call for a model?* The team that owns the model (embedded engineer plus data scientist rota); platform is called only for platform faults.
- *Build or buy?* Buy or reuse commodity parts (orchestrator, registry); build only the glue that encodes your standards.

**Common mistakes:** a platform with no internal customers; metrics that count features shipped; two "Accountable" owners or none; hiding on-call ownership; mandating the platform before it is easier than the alternative.

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

