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
