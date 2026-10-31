### Q21 ⭐⭐ 🟡 Healthcare triage assist: A tele-clinic network handles 30,000 consultations a day, and 2% are urgent (an estimate from an audit sample). A triage tool must flag at least 95% of urgent cases for clinician review, and clinicians can review at most 3,000 flagged cases a day. Design the assistive tool, and compute the urgent cases a day, the true urgent cases the flags must contain and the minimum precision of the flagged queue, and say what you would ask compliance.
**Asked at:** Healthcare and vision design material (a Dataford prompt on end-to-end ML for medical signal or image data, behind a sign-up wall, and an arXiv technology-readiness paper noting trust as a barrier in regulated fields; no triage-specific interview page was found); commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** 30,000 x 2% = 600 urgent cases a day, 95% of them is 570, and with 3,000 review slots the queue only needs 570 / 3,000 = 19% precision at its floor, so I would design an assistive ranker that never closes a case, only moves risky ones to a clinician first.

**Clarifying questions:**
- What does "urgent" mean and who labelled it in the audit sample (clinician consensus, one reviewer, outcome after 48 hours)? The label sets the ceiling for everything, including the 2%.
- How big was the audit sample behind the 2%? A 2% from 1,000 consults could be anywhere from about 1.1% to 2.9%, which moves the workload and the precision floor.
- Is the tool ranking, flagging or deciding? I assume it only reorders and flags, and a clinician makes every decision. If it can auto-close cases the whole risk profile changes.
- What does a missed urgent case cost, and how fast must a flagged case be seen? That decides whether recall 95% is the right target and what the review delay budget is.
- What data arrives at triage (free text, vitals, history, audio)? That decides the model family and the privacy questions I take to compliance.
- Does the tool count as regulated software in our market? I do not assume an answer; I ask compliance and legal.

**Approach:** (about 7 steps; pacing for a 45-minute round: 5 / 5 / 8 / 6 / 8 / 8 / 5)
1. Clarify and frame (5 min). Assistive, human in the loop, never auto-dismiss. Say the numbers out loud: 600 urgent, 570 must be in the queue, 3,000 slots, so a 10% flag rate.
2. Metrics and guardrails (5 min). Primary: recall of urgent cases in the flagged queue (target 95%). Capacity: queue size at most 3,000. Guardrails: recall for each subgroup (age band, language, hospital, channel), time from flag to clinician review, and clinician override rate.
3. Data and labels (8 min). Labels from clinician outcomes, but the audit sample is a sample: get an interval on the 2%. Beware that past triage decisions shaped which cases got outcomes (label bias). Add a small random slice of "not flagged" cases for clinician audit so recall is measured and not assumed.
4. Baseline first (6 min). Keyword and vital-sign rules plus the current manual triage order. The model must beat that at the same 3,000 slots, in recall, not accuracy.
5. Model and trade-offs (8 min). Calibrated gradient boosting on structured fields plus a text encoder if free text matters. The queue is a rank cut: take the top 3,000, or fewer if the score falls below a threshold. Trade-off: a bigger queue raises recall but costs clinician time (the 19% floor rises as the queue shrinks). Binormal rough guide: a 95% recall at a 10% flag rate needs an AUC near 0.98, which is high, so say it may not be reachable and plan the fallback (higher cap, more reviewers, or a lower target).
6. Evaluate offline, then online (8 min). Offline: recall at the 3,000 cap on a time-split holdout, by subgroup, with intervals. Then shadow mode (the tool scores, nobody sees it), then clinician-visible on one hospital, then stage up. Online metric: urgent cases reviewed within the time target, measured on the random audit slice.
7. Monitoring, retraining, risks and cost (5 min). Daily: flag rate, queue age, score drift, subgroup recall on the audit slice, override rate. Retrain on a schedule with clinician-confirmed labels. Risks: automation bias, drift when a season or disease pattern changes, hidden subgroup misses. Cost: reviewer hours (3,000 reviews a day) against the harm of missed cases. Ask compliance and legal about approval, consent, retention and liability; I do not state rules as facts.

**Metrics:**
- Recall of the queue = urgent cases inside the flagged queue / all urgent cases that day (570 / 600 at target). Measure it on clinician-confirmed outcomes plus the random audit slice.
- Precision of the queue = urgent cases in the queue / queue size. At a full 3,000 queue the floor is 570 / 3,000 = 19%.
- Flag rate = flagged consults / all consults (10% at the cap).
- Time to first review = minutes from flag to a clinician opening the case, 95th percentile.
- Guardrails: recall for each subgroup (denominator: urgent cases in that subgroup), override rate, and the share of urgent cases found only after the patient came back.

**Risks:**
- The 19% is a floor only at a full queue. A smaller queue needs higher precision for the same 570 hits.
- The 2% is an estimate from a sample; if urgency is 3% the 95% target means 855 hits, not 570, and the precision floor becomes 28.5%.
- Recall measured only on flagged cases looks perfect. Measure it on an unflagged random slice.
- Clinicians trust the queue and stop looking at unflagged cases (automation bias).
- Subgroups with weak data (rare language, children) can have much lower recall than the average.

**What the interviewer scores:**
- Strong: derives 600, 570 and 19% in seconds and says what each means. Weak: starts with a model name.
- Strong: assistive framing, shadow mode, an audit slice of unflagged cases. Weak: "accuracy of 95%" and an autonomous decision.
- Strong: notices the 2% is a sample and the 19% is a floor. Weak: treats every number as exact.
- Strong: asks compliance and legal and states no rules as facts. Weak: invents regulations, or ignores them.
- Strong: gives a pacing plan and a fallback if the target is not reachable.

**Example:** Illustrative numbers. If the audit sample had 1,000 consults, the 2% has an interval of about plus or minus 0.9 points, so urgent cases are 340 to 860 a day and the precision floor is 10.8% to 27.2%.
- Weak: "I would train a classifier with 95% accuracy on urgent cases."
- Strong: "There are about 600 urgent cases a day. To catch 95% I need 570 of them in the queue. Clinicians can read 3,000, so the queue must be at least 19% urgent at the cap. I would ship it as an assistive ranker, run it in shadow first, and measure recall on a random audit slice, because the 2% is only an estimate. What counts as regulated here is a question for compliance and legal."

**Code:**
```python
# Q21 triage sizing (all numbers illustrative; the 2% is a sample estimate)
from statistics import NormalDist
N = NormalDist()
consults, urgent_rate, recall_target, cap = 30_000, 0.02, 0.95, 3_000
urgent = round(consults * urgent_rate)
must_catch = round(urgent * recall_target)
min_precision = must_catch / cap
assert urgent == 600 and must_catch == 570 and min_precision == 0.19
print(f"urgent/day={urgent}, true urgent in flags >= {must_catch}, min precision at a full queue = {min_precision:.0%}")

# Flag rate and the false-positive room inside the queue
flag_rate = cap / consults
fp_room = cap - must_catch
non_urgent = consults - urgent
max_fpr = fp_room / non_urgent
assert flag_rate == 0.10 and fp_room == 2_430 and abs(max_fpr - 0.08265) < 1e-4
print(f"flag rate={flag_rate:.0%}, false flags allowed={fp_room}, max false-positive rate={max_fpr:.2%}")

# Model assumption (equal-variance binormal scores): what separation does that need?
d = N.inv_cdf(recall_target) + N.inv_cdf(1 - max_fpr)
auc = N.cdf(d / 2 ** 0.5)
assert abs(d - 3.03) < 0.01 and abs(auc - 0.984) < 0.002
print(f"needed d'={d:.2f}, implied AUC={auc:.3f} (binormal assumption, a rough guide only)")

# The 2% is a sample. Suppose (invented) the audit had 1,000 consults.
n_audit = 1_000
se = (urgent_rate * (1 - urgent_rate) / n_audit) ** 0.5
lo, hi = urgent_rate - 1.96 * se, urgent_rate + 1.96 * se
u_lo, u_hi = consults * lo, consults * hi
p_lo, p_hi = recall_target * u_lo / cap, recall_target * u_hi / cap
assert abs(se - 0.004427) < 1e-5 and round(u_lo) == 340 and round(u_hi) == 860
assert abs(p_lo - 0.1077) < 1e-3 and abs(p_hi - 0.2724) < 1e-3
print(f"2% +/- {1.96*se:.2%} -> urgent {u_lo:.0f}..{u_hi:.0f}/day -> min precision {p_lo:.1%}..{p_hi:.1%}")
# If urgency were 3% instead of 2%
hits3 = consults * 0.03 * recall_target
assert round(hits3) == 855 and abs(hits3 / cap - 0.285) < 1e-9
print(f"if urgency is 3%: hits needed={hits3:.0f}, precision floor={hits3/cap:.1%}")
```

**Output (my run):**
```text
urgent/day=600, true urgent in flags >= 570, min precision at a full queue = 19%
flag rate=10%, false flags allowed=2430, max false-positive rate=8.27%
needed d'=3.03, implied AUC=0.984 (binormal assumption, a rough guide only)
2% +/- 0.87% -> urgent 340..860/day -> min precision 10.8%..27.2%
if urgency is 3%: hits needed=855, precision floor=28.5%
```

**Follow-ups:**
- What if the model only reaches 80% recall at the 3,000 cap? Say so, then offer options: a bigger cap with more reviewers, a two-stage queue (fast nurse check on the second tier), or a lower target agreed with clinical leads.
- How do you measure recall if unflagged cases are never reviewed? A small random audit slice of unflagged cases reviewed by a clinician each day, with an interval.
- Would you use an LLM here? Possibly to extract fields from free text, with the ranker doing the scoring, and with the same audit slice; free text from an LLM is not a decision.

**Common mistakes:** Quoting accuracy instead of recall at a fixed review capacity. Treating 19% as the required precision at any queue size. Forgetting the 2% is a sample. No unflagged audit slice. Letting the tool close cases. Stating legal rules as facts.

### Q22 ⭐⭐ 🟡 Experimentation platform: 40 product teams will run 120 concurrent experiments on an app with 12,000,000 daily users, organised in 10 layers where every user is in every layer and the 12 experiments inside a layer split its users evenly. Assignment lookups must answer in 5 ms at the 99th percentile at 20,000 requests per second. Design the platform, and compute the daily users each experiment sees if all users are eligible and compare it with a need of 800,000 users across two arms.
**Asked at:** Operations and platform design material (a Codemia anomaly-detection pipeline prompt attributed to ServiceNow, Codemia A/B-testing platform prompts attributed to a DoorDash onsite, a PracHub feature-store data-quality and backfill prompt attributed to a Faire onsite, datadriven.io and techinterview.org MLOps guides); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** 12,000,000 users split 12 ways in each layer gives 1,000,000 users per experiment, which covers the 800,000 needed with 200,000 (25%) to spare, but only if every user is eligible and the 800,000 means distinct users over the run, so I would design for eligibility rules and a layer-by-layer capacity check.

**Clarifying questions:**
- Is the 800,000 a total of distinct users over the whole run, or per day? One million "daily users" are mostly the same people tomorrow, so a multi-day run adds few new users.
- What share of users is eligible for a typical experiment (new users only, one country, one platform)? At 30% eligible, each experiment sees 300,000 and the plan breaks.
- What metrics, and what effect size must be detectable? The 800,000 is only a need if someone derived it; I would re-derive it (for a 5% baseline, 400,000 per arm detects about 0.14 points).
- Which experiments must be mutually exclusive (same screen, same ranking model) and which can overlap? That decides what goes into one layer.
- Do the 5 ms at 20,000 requests per second apply to the assignment call only, and is it from cache or from a service? It sets whether we assign by hash or look up a table.
- Who is allowed to launch, and who reviews a bad result? Governance decides the platform scope as much as the maths does.

**Approach:** (about 7 steps; pacing for a 45-minute round: 5 / 6 / 5 / 6 / 8 / 8 / 7)
1. Clarify and frame (5 min). Platform users are 40 teams; the product is trustworthy decisions at low cost. Do the arithmetic aloud: 120 / 10 = 12 per layer, 12,000,000 / 12 = 1,000,000 each.
2. Metrics and guardrails (6 min). Platform metrics: experiments launched per week, share of experiments reaching their needed sample, time to a decision, and a guardrail of sample ratio mismatch (assigned split against the planned split). Product metrics are owned by each team, with a shared guardrail set (crashes, latency, retention).
3. Data and labels (5 min). Exposure logs (user, experiment, arm, time), assignment configuration with versions, and metric tables. The key rule: log exposure at the moment the user actually sees the change, not at assignment.
4. Baseline first (6 min). Start with one layer, hash assignment, a basic z-test or t-test report and a sample-ratio check. Do not build sequential testing or variance reduction before that works.
5. Model and trade-offs (8 min). Assignment is a pure function: hash(salt per layer, user id) mod 12, no database lookup, so 5 ms at 20,000 per second is easy (about 100 in flight at most by Little's law). Trade-off: more layers give more concurrent tests but more interaction risk; fewer layers give clean results but a queue. Reserve a holdout. Capacity planner: refuse or queue an experiment whose eligible users cannot reach its needed sample.
6. Evaluate offline, then online (8 min). Offline: A/A tests on every layer should show about 5% false positives at 0.05 and a balanced split. Replay old experiments through the pipeline. Online: roll the platform out to two teams first.
7. Monitoring, retraining and cost (7 min). Alert on sample-ratio mismatch, logging gaps, and exposure drift. No model retraining here, but metric definitions are versioned. Cost: the logging and metric computation, not the assignment. Risks: peeking, interaction between layers, novelty effects, and teams reading many metrics without correction.

**Metrics:**
- Users per experiment per day = users in the layer / experiments in the layer = 12,000,000 / 12 = 1,000,000.
- Sample coverage = users the experiment sees over its run / users needed (target at least 1.0; here 1,000,000 / 800,000 = 1.25 if the need is per day-cohort).
- Sample-ratio mismatch rate = experiments whose observed arm split differs from plan by a chi-square test at a strict threshold / all running experiments.
- Assignment latency p99 in ms (target 5) and error rate of the lookup.
- Guardrail: the false-positive rate of A/A tests, which should be near the chosen alpha.

**Risks:**
- "Daily users" and "distinct users over the run" are different bases. Say which one 800,000 is.
- Eligibility filters cut each experiment's sample sharply.
- Layers are independent only if each has its own salt; shared salts correlate assignments (the code checks this).
- Many experiments on one user can interact (two ranking changes in different layers).
- Peeking at results daily inflates false positives.

**What the interviewer scores:**
- Strong: 120 / 10 = 12 and 1,000,000 immediately, then immediately asks about eligibility and the base of the 800,000. Weak: stops at "enough users".
- Strong: hash-based assignment, so lookups are computation, not a database. Weak: a table lookup per call with no capacity thought.
- Strong: sample-ratio mismatch and A/A tests as platform health checks. Weak: only the dashboard.
- Strong: a baseline first plan, one layer then more. Weak: builds everything at once.

**Example:** Illustrative numbers. One experiment limited to 30% eligible users sees 300,000 users, so it needs about 2.7 times the share of users (or a longer run, which helps only as new users arrive), while another that is open to everyone sees 1,000,000.
- Weak: "We have 12 million users and the test needs 800,000, so we are fine."
- Strong: "Each layer splits 12 million users 12 ways, so every experiment gets 1 million. That clears 800,000 by 25%, but only if all users are eligible and the 800,000 means distinct users over the run. With 30% eligibility it falls to 300,000, so the platform should check eligible users against the needed sample before an experiment is allowed to launch."

**Code:**
```python
# Q22 experimentation platform sizing (illustrative)
import hashlib, math
users, layers, exps_total, per_layer = 12_000_000, 10, 120, 12
assert per_layer * layers == exps_total and exps_total // 40 == 3
users_per_exp = users // per_layer
need = 800_000
assert users_per_exp == 1_000_000 and users_per_exp >= need
headroom = users_per_exp - need
assert headroom == 200_000 and headroom / need == 0.25
print(f"users per experiment per day={users_per_exp:,}, need={need:,}, headroom={headroom:,} ({headroom/need:.0%} of need)")

# If only 30% of users are eligible (invented), each experiment sees fewer
elig = round(users_per_exp * 0.30)
assert elig == 300_000 and elig < need
print(f"with 30% eligibility: {elig:,} < {need:,}")

# What 800,000 (400,000 per arm) can detect: baseline 5%, alpha 0.05 two-sided, power 80%
z = 1.96 + 0.8416
p, n_arm = 0.05, 400_000
mde = z * math.sqrt(2 * p * (1 - p) / n_arm)
assert abs(mde - 0.001366) < 2e-5
print(f"minimum detectable absolute lift ~ {mde*100:.3f} points ({mde/p:.1%} relative)")

# Assignment load: Little's law on the lookup service (upper bound uses the 5 ms p99 for every call)
rps, lat = 20_000, 0.005
inflight = rps * lat
assert inflight == 100
print(f"requests in flight at most ~ {inflight:.0f}; each request resolves {layers} layers")

# Deterministic hash bucketing: each layer has its own salt, so layers are independent
def bucket(uid, layer, k):
    h = hashlib.sha256(f"layer{layer}:{uid}".encode()).digest()
    return int.from_bytes(h[:8], 'big') % k
N = 120_000
counts = [0] * per_layer
cross = [[0] * per_layer for _ in range(per_layer)]
for u in range(N):
    a, b = bucket(u, 0, per_layer), bucket(u, 1, per_layer)
    counts[a] += 1
    cross[a][b] += 1
expected = N / per_layer
assert all(abs(c - expected) / expected < 0.05 for c in counts)
# users in experiment 0 of layer 0 spread evenly over layer 1 buckets (independence)
row = cross[0]
assert all(abs(c - sum(row) / per_layer) / (sum(row) / per_layer) < 0.15 for c in row)
print("bucket counts layer0:", counts)
print("layer-0 experiment 0 across layer-1 buckets:", row)
```

**Output (my run):**
```text
users per experiment per day=1,000,000, need=800,000, headroom=200,000 (25% of need)
with 30% eligibility: 300,000 < 800,000
minimum detectable absolute lift ~ 0.137 points (2.7% relative)
requests in flight at most ~ 100; each request resolves 10 layers
bucket counts layer0: [9949, 9857, 9987, 9869, 9869, 10142, 9993, 10107, 10222, 9969, 10060, 9976]
layer-0 experiment 0 across layer-1 buckets: [827, 844, 822, 859, 840, 802, 806, 819, 845, 876, 790, 819]
```

**Follow-ups:**
- How do you run more than 12 experiments in a layer? Shrink each arm's share, run longer, or use more layers; every option trades speed for power or interaction risk.
- What if two experiments touch the same screen in different layers? Put them in the same layer so they are mutually exclusive, or analyse the interaction explicitly.
- How do you know the platform is trustworthy? A/A tests, sample-ratio checks, and replaying a past experiment. The detailed metric reading is covered in Book 6 Part 1 (see its question on a ranking change that lifts click-through while orders fall).

**Common mistakes:** Confusing daily users with distinct users over the run. Ignoring eligibility. Using one hash salt for all layers. Logging exposure at assignment time. Building sequential testing before the basics work. Giving no capacity check before launch.

### Q23 ⭐⭐ 🟡 Data-quality platform: A data team owns 1,500 tables with 6 automated checks each, run daily, and each check scans 40 GB on average at an illustrative 0.5 rupees per GB, with a budget of 100,000 rupees a day. Design the data-quality platform, and compute the daily scan cost with full scans and with a 50% row sample, and say which checks should not be sampled.
**Asked at:** Operations and platform design material (a Codemia anomaly-detection pipeline prompt attributed to ServiceNow, Codemia A/B-testing platform prompts attributed to a DoorDash onsite, a PracHub feature-store data-quality and backfill prompt attributed to a Faire onsite, datadriven.io and techinterview.org MLOps guides); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** 1,500 tables x 6 checks is 9,000 scans, 360,000 GB, so 180,000 rupees a day with full scans (1.8 times the 100,000 budget) and 90,000 with a 50% sample, but a sample only helps if the engine really reads half the data and it must not touch checks that look for rare or exact defects.

**Clarifying questions:**
- Does a 50% row sample really halve the bytes scanned? In many columnar layouts a row sample still reads most of the data, and only partition or file-level sampling saves cost. This decides if the 90,000 is real.
- What are the six checks per table today (freshness, row count, schema, null rate, uniqueness, distribution)? Some can be answered from metadata at almost no cost.
- Which tables feed models or finance reports, and which are scratch? Criticality sets check depth and who gets paged.
- Are tables partitioned by date, so a daily check can scan only the new partition? That is usually a bigger saving than sampling.
- Who owns a failed check, and what is the expected response time? A check with no owner is a cost with no value.
- Is 100,000 rupees a hard cap or a target, and does it include storage and alert tooling?

**Approach:** (about 7 steps; pacing for a 45-minute round: 5 / 6 / 5 / 6 / 8 / 8 / 7)
1. Clarify and frame (5 min). Goal: catch bad data before models and dashboards use it, within a cost cap. State the arithmetic: 9,000 checks, 360,000 GB, 180,000 rupees full, 90,000 sampled.
2. Metrics and guardrails (6 min). Detection: bad-data incidents caught by a check before a user noticed / all bad-data incidents. Cost: rupees per day against the 100,000 cap. Noise: alerts per week and the share that were real. Guardrail: time from a bad load to an alert.
3. Data and labels (5 min). Labels are past incidents (which table, which defect, how found). Start by listing the last 20 data incidents and asking which check would have caught each.
4. Baseline first (6 min). Metadata checks for every table (freshness, row count versus recent days, schema, partition present). These cost almost nothing and catch many failures.
5. Model and trade-offs (8 min). Tier the tables (critical, normal, scratch). Content checks run only on the new partition. Sample where an estimate is good enough (null rate, mean, distribution shift); scan fully where exactness matters (uniqueness of keys, orphan keys, value ranges that must never break, rare segments). Learned anomaly thresholds on top of row counts instead of fixed numbers, as a later step.
6. Evaluate offline, then online (8 min). Offline: replay the 20 past incidents and count which are caught, and at what cost. Online: shadow mode for two weeks (alerts to a channel nobody is paged by), then page for the critical tier only.
7. Monitoring, retraining and cost (7 min). Weekly report of cost per tier, alerts, false-alert share and incidents missed. Retune thresholds monthly. Risks: alert fatigue, a sample hiding a rare defect, checks drifting as schemas change, cost rising as tables grow. Build-versus-buy: an open or vendor tool can cover standard checks; the custom part is tiering and ownership.

**Metrics:**
- Daily scan cost = checks run x GB per check x rupees per GB (9,000 x 40 x 0.5 = 180,000).
- Detection rate = incidents caught by a check before a consumer reported them / all incidents in the period.
- False-alert share = alerts judged not real after triage / all alerts.
- Time to detect = hours from a bad load to its first alert.
- Guardrail: cost as a share of the cap (target below 100%), and incidents missed that a sampled check could have caught.

**Risks:**
- A row sample may not reduce bytes read; check the engine before promising savings.
- A sampled uniqueness check catches one duplicate pair only 25% of the time at a 50% sample.
- Rare bad segments disappear in samples (one bad row survives with probability 0.5).
- Checks run without an owner create alert noise.
- Table growth silently pushes the cost back over the cap.

**What the interviewer scores:**
- Strong: 9,000, 360,000 GB, 180,000 and 90,000 quickly, then notices full scans are over budget. Weak: designs checks with no cost figure.
- Strong: says which checks must not be sampled and why (uniqueness, referential integrity, hard ranges, rare segments). Weak: "sample everything".
- Strong: cheaper levers first (metadata, new partition only, tiering). Weak: only sampling.
- Strong: ownership, shadow mode and alert-noise tracking. Weak: dashboards no one reads.

**Example:** Illustrative numbers. If 3 of the 6 checks are metadata-only and the other 3 scan, full scans cost 90,000 a day, and scanning only the new partition (taken as 1/30 of the table) costs 3,000.
- Weak: "I would sample 50% of every table and that fits the budget."
- Strong: "Full scans cost 180,000 a day, 1.8 times the budget. A 50% sample gives 90,000 only if the engine really reads half the data. Before that I would answer freshness, volume and schema from metadata, scan only new partitions, and keep uniqueness and key-integrity checks unsampled because a sample catches one duplicate pair only a quarter of the time."

**Code:**
```python
# Q23 data-quality scan cost (illustrative)
import random
tables, checks, gb, price, budget = 1_500, 6, 40, 0.5, 100_000
runs = tables * checks
assert runs == 9_000
full = runs * gb * price
half = full * 0.5
assert full == 180_000 and half == 90_000
print(f"checks/day={runs}, full scan cost={full:,.0f} rupees ({full/budget:.2f}x budget), 50% sample={half:,.0f} ({half/budget:.0%} of budget)")

# Illustrative split of the 6 checks: 3 answered from metadata (almost free), 3 scan data
meta, scanning = 3, 3
mix_full = tables * scanning * gb * price
mix_half = mix_full * 0.5
assert mix_full == 90_000 and mix_half == 45_000
print(f"3 metadata + 3 scanning checks: full={mix_full:,.0f}, sampled={mix_half:,.0f}")

# Incremental scan: only the new daily partition (invented: 1/30 of the table) for the scanning checks
inc = mix_full / 30
assert inc == 3_000
print(f"incremental (new partition only, 1/30 of table): {inc:,.0f} rupees")

# Why uniqueness should not be sampled: one duplicated pair survives a 50% row sample with prob 0.25
random.seed(7)
trials, caught = 100_000, 0
for _ in range(trials):
    a, b = random.random() < 0.5, random.random() < 0.5
    caught += a and b
rate = caught / trials
assert abs(rate - 0.25) < 0.01
print(f"single duplicate pair caught by a 50% row sample: {rate:.3f} (theory 0.25)")

# A rare bad segment: 40 bad rows among 1,000,000; chance the sample contains none of them
p_none = 0.5 ** 40
assert p_none < 1e-12
# ... but chance of seeing zero of 1 bad row is 0.5, so tiny defects often vanish
print(f"sample sees none of 1 bad row: {0.5:.2f}; none of 40: {p_none:.1e}")
```

**Output (my run):**
```text
checks/day=9000, full scan cost=180,000 rupees (1.80x budget), 50% sample=90,000 (90% of budget)
3 metadata + 3 scanning checks: full=90,000, sampled=45,000
incremental (new partition only, 1/30 of table): 3,000 rupees
single duplicate pair caught by a 50% row sample: 0.250 (theory 0.25)
sample sees none of 1 bad row: 0.50; none of 40: 9.1e-13
```

**Follow-ups:**
- How do you set thresholds without hand tuning 9,000 checks? Start with rolling-window bounds from recent history per table, review the noisiest 5% by hand, and tier by criticality.
- What would you do if cost grows past the cap? Re-tier, widen sampling on non-critical tables only, reduce frequency for slow-changing tables, and show the trade-off to the data owners.
- How does this connect to model monitoring? Data checks protect inputs; model monitoring (Book 6 Part 2, see its question on a feature null rate jumping after an upstream deploy) sees the effect on predictions.

**Common mistakes:** Assuming a row sample halves the scan cost. Sampling uniqueness or key checks. Ignoring metadata checks. No owner per table. Pasting one threshold for every table. Forgetting the cost grows with table size.

### Q24 ⭐⭐ 🟡 MLOps platform: Four platform engineers have 6 months (take it as 26 weeks) to build a deployment and retraining platform for 25 models owned by 6 teams, of which 10 are real-time and 15 are batch. The real-time services target 99.9% availability over a 30-day month. Design the platform and its roadmap, and compute the monthly error budget in minutes and the engineer-weeks available.
**Asked at:** Operations and platform design material (a Codemia anomaly-detection pipeline prompt attributed to ServiceNow, Codemia A/B-testing platform prompts attributed to a DoorDash onsite, a PracHub feature-store data-quality and backfill prompt attributed to a Faire onsite, datadriven.io and techinterview.org MLOps guides); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** 99.9% over a 30-day month is 0.001 x 43,200 = 43.2 minutes of allowed downtime per real-time service, and 4 engineers x 26 weeks is 104 engineer-weeks gross (about 73 at 70% focus), so I will build the thinnest platform that makes the 10 real-time models safe first and onboard the 15 batch models on the same pieces.

**Clarifying questions:**
- How do the 6 teams deploy and retrain today (scripts, notebooks, a scheduler)? The platform must replace pain, not add a new process.
- Is 99.9% per service measured at the user-facing endpoint, and what counts as a failure (errors, timeouts, stale model)? Without that, the 43.2 minutes is not measurable.
- Which of the 10 real-time models are revenue- or safety-critical? They go first.
- Which cloud, cluster and tools are already approved? Build-versus-buy depends on this.
- Who is on call, and is there a platform on-call or does each team page itself? That drives the effort needed for runbooks and alerts.
- What does "retraining" mean for each model (scheduled, triggered by drift, manual)? It sets the pipeline design.

**Approach:** (about 8 steps; pacing for a 45-minute round: 4 / 5 / 5 / 6 / 8 / 7 / 5 / 5)
1. Clarify and frame (4 min). Users are 6 teams and 25 models. Success is that a team can ship and retrain a model without the platform team in the loop.
2. Metrics and guardrails (5 min). Platform: deploy lead time, share of models on the platform, failed-deploy rate, rollback time. Reliability: error budget burn per service. Guardrail: team satisfaction and number of platform tickets per week.
3. Data and labels (5 min). The "data" here is an inventory: every model, its owner, its input data, how it serves (real-time or batch), how often it retrains and what it costs. Build that table in week 1.
4. Baseline first (6 min). A model registry plus a standard container and CI pipeline, a one-command deploy and a rollback. This alone removes the biggest risk and fits in the first 14 engineer-weeks.
5. Model and trade-offs (8 min). Real-time serving: canary or blue-green, health checks, autoscaling and an SLO dashboard. Batch: a templated scheduled pipeline with retraining, validation gates and promotion. Trade-off: buy or adopt existing tools for standard parts, build only the glue and the golden path. Resist a feature store or a UI in the first half.
6. Evaluate offline, then online (7 min). Pilot with two teams, one real-time and one batch. Measure deploy lead time before and after. Chaos-style test: kill a pod and a bad model version and time the rollback.
7. Launch, monitoring and retraining (5 min). Onboard the 10 real-time models in order of criticality, then the 15 batch ones. Monitor latency, errors, saturation and a model-quality proxy. A failed retrain must never replace the live model.
8. Risks and cost (5 min). Scope creep, adoption (teams keep their scripts), a single point of failure in the platform itself (three serial 99.9% parts give 99.7%, so the platform must not sit in the request path), key-person risk. Cost: effort first, cloud second.

**Metrics:**
- Monthly error budget (minutes) = (1 - 0.999) x 30 x 24 x 60 = 43.2 per service.
- Error-budget burn = bad minutes so far / 43.2 (alert at 50% and 100% of the monthly budget).
- Deploy lead time = hours from merge to serving traffic, median.
- Adoption = models deployed through the platform / 25.
- Guardrail: rollback time (target minutes) and failed retrains that reached production (target zero).

**Risks:**
- 104 engineer-weeks is gross; leave, support and on-call cut it to about 73 (at an invented 70%).
- A platform in the serving path adds its own downtime to every service.
- Teams do not migrate if the golden path is harder than their scripts.
- 43.2 minutes is per service per month; one bad 30-minute deploy uses 70% of it.
- Scope grows (feature store, UI, A/B tooling) before the basics work.

**What the interviewer scores:**
- Strong: 43.2 and 104 immediately, then the net capacity after overhead. Weak: stops at 104 or treats it as fully usable.
- Strong: a phased roadmap with engineer-weeks per phase that sums to capacity. Weak: a wish list.
- Strong: buy or adopt the standard parts, own the golden path and the SLO. Weak: build everything.
- Strong: reliability thinking (error budget, canary, rollback, platform not in the request path). Weak: "use Kubernetes".

**Example:** Illustrative split of about 73 net engineer-weeks: foundation 14, real-time serving 18, batch retraining 14, monitoring 10, onboarding 12 (about 0.5 each for 25 models), buffer 4.8.
- Weak: "We will build a full MLOps platform with a feature store and a model registry in six months."
- Strong: "Four people for 26 weeks is 104 engineer-weeks, about 73 after overhead. Real-time services get 43.2 minutes of downtime a month, so I would first ship registry, standard container, canary and one-command rollback for the 10 real-time models, then the templated batch pipeline, then monitoring. A feature store waits until the first teams are live."

**Code:**
```python
# Q24 MLOps platform sizing (illustrative)
minutes_month = 30 * 24 * 60
budget_min = (1 - 0.999) * minutes_month
assert minutes_month == 43_200 and abs(budget_min - 43.2) < 1e-9
print(f"monthly error budget at 99.9% = {budget_min:.1f} minutes per real-time service")
print(f"across 10 real-time services = {10*budget_min:.0f} service-minutes in total")

# Chained dependencies: serial availability multiplies
chain = 0.999 ** 3
assert abs(chain - 0.997003) < 1e-6
assert abs((1-chain)*minutes_month - 129.5) < 0.1
print(f"three serial 99.9% parts give {chain:.4%} -> {(1-chain)*minutes_month:.1f} min/month of downtime (3x the single budget)")

# Capacity
engineers, weeks = 4, 26
gross = engineers * weeks
focus = 0.70                     # invented: leave, meetings, on-call, support
net = gross * focus
assert gross == 104 and abs(net - 72.8) < 1e-9
print(f"gross engineer-weeks={gross}, at 70% focus={net:.1f}, per model (25) gross={gross/25:.2f}")

# Illustrative roadmap that sums to the net capacity
plan = {"foundation: registry, packaging, CI": 14,
        "real-time serving, canary, rollback": 18,
        "batch retraining pipelines": 14,
        "monitoring and SLO alerts": 10,
        "onboard 25 models (about 0.5 each)": 12,
        "buffer": 4.8}
tot = sum(plan.values())
assert abs(tot - net) < 1e-9
for k, v in plan.items():
    print(f"  {k}: {v} eng-weeks")
print(f"planned total={tot:.1f}")

# One bad deploy: how many full-outage minutes exhaust one service's budget
assert int(budget_min // 10) == 4
print(f"4 outages of 10 minutes use {40} of {budget_min:.1f} minutes")
assert round(30 / budget_min, 3) == 0.694
print(f"one 30-minute outage uses {30/budget_min:.1%} of the monthly budget")
```

**Output (my run):**
```text
monthly error budget at 99.9% = 43.2 minutes per real-time service
across 10 real-time services = 432 service-minutes in total
three serial 99.9% parts give 99.7003% -> 129.5 min/month of downtime (3x the single budget)
gross engineer-weeks=104, at 70% focus=72.8, per model (25) gross=4.16
  foundation: registry, packaging, CI: 14 eng-weeks
  real-time serving, canary, rollback: 18 eng-weeks
  batch retraining pipelines: 14 eng-weeks
  monitoring and SLO alerts: 10 eng-weeks
  onboard 25 models (about 0.5 each): 12 eng-weeks
  buffer: 4.8 eng-weeks
planned total=72.8
4 outages of 10 minutes use 40 of 43.2 minutes
one 30-minute outage uses 69.4% of the monthly budget
```

**Follow-ups:**
- What would you cut if the team loses one engineer? Drop the batch retraining templates to a later quarter and keep serving, rollback and monitoring; the 10 real-time models carry the availability risk.
- How do you set an SLO for a model, not only a service? Add a quality proxy (prediction distribution, a delayed-label metric) next to availability, and agree what a breach triggers.
- How do you measure that the platform helps? Compare deploy lead time and incident counts for onboarded versus not-yet-onboarded models. Detail on monitoring is in Book 6 Part 2 (e.g. the question on a feature null rate jumping after an upstream deploy).

**Common mistakes:** Using 104 as fully available. Forgetting the error budget is per service. Building a feature store first. Putting the platform in the request path. No pilot team. Skipping rollback.

### Q25 ⭐⭐ 🟡 Vision for insurance claims: An insurer receives 20,000 vehicle-damage photos a day through a mobile app, with 70% arriving in a 4-hour window (assume evenly spread). A raw photo is 1.2 MB and a compressed one is 250 KB (take 1 MB as 1,000,000 bytes), uplinks give about 500 kilobits per second, and one GPU scores 40 photos per second. Design the claims-photo triage system, and compute the upload time for each size, the peak photos per second and the GPUs needed, then say where the bottleneck is.
**Asked at:** Healthcare and vision design material (a Dataford prompt on end-to-end ML for medical signal or image data, behind a sign-up wall, and an arXiv technology-readiness paper noting trust as a barrier in regulated fields; no triage-specific interview page was found); commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The peak is only 14,000 / 14,400 s = 0.97 photos a second, so one GPU at 40 a second is 2.4% busy; the real bottleneck is the customer's 500 kilobit uplink, where a raw photo takes 19.2 seconds and a compressed one 4.0 seconds, so I would compress on the phone and spend my design effort on upload and review.

**Clarifying questions:**
- What decision does the photo feed (fast-track payout, route to an adjuster, flag for fraud review)? The action decides which errors cost the most.
- How many photos per claim and is the customer waiting on screen for the result? That sets the latency target and whether upload time is the user's pain.
- Who owns the final claim decision? I assume a human adjuster for anything above a threshold; the tool triages and never denies a claim alone.
- Is the "evenly spread" 4-hour window realistic, or do claims spike after a weather event? Bursts matter more than the average.
- What labels exist (adjuster estimates, repair invoices, fraud outcomes), and how late do they arrive? Repair invoices can take weeks.
- What may be stored and for how long (photos contain locations, plates, people)? I ask compliance and legal; I do not assume.

**Approach:** (about 7 steps; pacing for a 45-minute round: 5 / 5 / 7 / 6 / 8 / 8 / 6)
1. Clarify and frame (5 min). Goal: faster, more consistent claim triage with fewer manual touches, without wrongly rejecting honest claims. Do the numbers aloud: 19.2 s versus 4 s upload, 0.97 per second, one GPU.
2. Metrics and guardrails (5 min). Primary: share of claims routed correctly (fast-track, adjuster, fraud review) compared with the final adjuster outcome. Operational: time from first photo to decision, upload failure rate. Guardrails: wrongly delayed honest claims, and error rate by phone type and region.
3. Data and labels (7 min). Past claims with photos and adjuster outcome (severity band, repair cost band, fraud flag). Labels are noisy and late, so use severity bands rather than exact cost, and check agreement between adjusters. Photo quality labels (blurred, wrong angle) are cheap to add and very useful.
4. Baseline first (6 min). Quality checks on the phone (blur, glare, vehicle present), a simple severity classifier, and the current adjuster queue order. Compare against it.
5. Model and trade-offs (8 min). On-device: resize and compress to about 250 KB, check quality, resumable uploads, upload in the background. Server: a pretrained vision backbone fine-tuned for damage severity and part location, plus a duplicate-photo and metadata check for fraud. Trade-off: compression too hard hurts damage detail; test accuracy at the compressed size, not at the original. Scoring is cheap, so the model can be larger.
6. Evaluate offline, then online (8 min). Offline: severity-band accuracy and the confusion cost matrix on a time-split holdout, by phone type and lighting. Online: shadow mode (score, route nothing), then recommend-only to adjusters, then fast-track low-risk bands for a small share.
7. Launch, monitoring and risks (6 min). Monitor upload failures, photo-quality rejects, score drift, override rate by adjusters and complaint rate. Retrain on adjuster outcomes. Risks: new phone cameras, staged fraud, fairness across regions and vehicle types, a weather-event burst. Cost: GPU is small; storage and adjuster time dominate.

**Metrics:**
- Upload time = bytes x 8 / uplink bits per second (1,200,000 x 8 / 500,000 = 19.2 s; 250,000 x 8 / 500,000 = 4.0 s).
- Peak rate = photos in the window / window seconds = 14,000 / 14,400 = 0.97 per second.
- GPU utilisation = peak rate / 40 = 2.4%.
- Routing accuracy = claims routed to the band the adjuster later confirmed / all routed claims.
- Guardrails: share of honest claims delayed beyond the target, and the fast-track error rate (fast-tracked claims later overturned / fast-tracked claims).

**Risks:**
- Evenly spread is an assumption; a storm can multiply the rate, though even 10 times is 9.7 per second.
- Compression that hides damage detail lowers accuracy; test it.
- Adjuster outcomes are late and noisy labels.
- Staged or reused photos need a separate fraud check.
- Customers on slow links abandon uploads; measure drop-off.

**What the interviewer scores:**
- Strong: finds that upload, not the GPU, is the bottleneck, with the numbers. Weak: sizes GPUs and stops.
- Strong: compress and resume on the phone, test accuracy at the compressed size. Weak: "send the raw photo".
- Strong: human adjuster decides, shadow mode first. Weak: automatic denial.
- Strong: labels and their lateness handled. Weak: assumes clean labels.

**Example:** Illustrative numbers. A claim of 6 photos sent one after another takes 115 seconds raw and 24 seconds compressed on that uplink, while the GPU needs 0.025 seconds a photo.
- Weak: "20,000 photos a day, so I need a GPU cluster."
- Strong: "The peak is under one photo a second, so one GPU, or two for redundancy, is plenty. The 500 kilobit uplink is the problem: 19.2 seconds raw versus 4 seconds compressed. So I compress on the phone, upload in the background and resume on failure, check accuracy at the compressed size, and keep an adjuster in the loop."

**Code:**
```python
# Q25 claims-photo triage sizing (illustrative)
import math
photos, share, window_h = 20_000, 0.70, 4
raw_B, comp_B, uplink_bps = 1_200_000, 250_000, 500_000
t_raw, t_comp = raw_B * 8 / uplink_bps, comp_B * 8 / uplink_bps
assert t_raw == 19.2 and t_comp == 4.0 and abs(t_raw / t_comp - 4.8) < 1e-9
print(f"upload time: raw {t_raw:.1f} s, compressed {t_comp:.1f} s ({t_raw/t_comp:.1f}x faster)")

peak_photos = photos * share
peak_rate = peak_photos / (window_h * 3600)
assert peak_photos == 14_000 and abs(peak_rate - 0.9722) < 1e-3
gpu_rate = 40
gpus = math.ceil(peak_rate / gpu_rate)
util = peak_rate / gpu_rate
assert gpus == 1 and abs(util - 0.0243) < 1e-3
print(f"peak rate={peak_rate:.3f} photos/s, GPUs needed={gpus}, utilisation={util:.1%}")

# Burst check: even a 10x burst over the even-spread rate
burst = 10 * peak_rate
assert math.ceil(burst / gpu_rate) == 1 and burst < gpu_rate
print(f"10x burst={burst:.2f} photos/s still fits one GPU (use 2 for redundancy)")

# Ingest bandwidth at the server for compressed photos
ingest_bps = peak_rate * comp_B * 8
assert abs(ingest_bps - 1_944_444) < 10
print(f"server ingest at peak ~ {ingest_bps/1e6:.2f} Mbit/s")

# Per claim with 6 photos (invented): customer waits
per_claim_raw, per_claim_comp = 6 * t_raw, 6 * t_comp
assert abs(per_claim_raw - 115.2) < 1e-9 and per_claim_comp == 24.0
print(f"6 photos one after another: raw {per_claim_raw:.1f} s, compressed {per_claim_comp:.1f} s")
# Scoring time per photo on a GPU is 1/40 s
assert 1 / 40 == 0.025
print("GPU scoring time per photo = 0.025 s versus 4.0 s upload: upload is 160x longer")
assert 4.0 / 0.025 == 160
```

**Output (my run):**
```text
upload time: raw 19.2 s, compressed 4.0 s (4.8x faster)
peak rate=0.972 photos/s, GPUs needed=1, utilisation=2.4%
10x burst=9.72 photos/s still fits one GPU (use 2 for redundancy)
server ingest at peak ~ 1.94 Mbit/s
6 photos one after another: raw 115.2 s, compressed 24.0 s
GPU scoring time per photo = 0.025 s versus 4.0 s upload: upload is 160x longer
```

**Follow-ups:**
- What if photos arrive in a storm at 50 times the rate? 50 x 0.97 is about 49 per second, so 2 GPUs; queue the rest and tell customers the expected wait.
- Do you score on the phone instead of the server? A small quality-check model on the phone, yes; the damage model stays on the server so it can be updated and audited.
- How would you catch fraud? Duplicate and near-duplicate photo search, metadata consistency, and routing to a specialist, never an automatic denial.

**Common mistakes:** Sizing the GPU and ignoring upload time. Sending raw photos over slow links. Testing accuracy only on uncompressed photos. Treating late adjuster labels as instant. Auto-denying on a model score.

### Q26 ⭐⭐ 🟡 Cold-start personalisation: A grocery app gets 60,000 new users a day with no history and plans to give 10% of recommendation slots to exploration, where the click rate is 1.5% per impression, against 3% for slots chosen by the best current policy (both rates measured in an earlier test, a sample). Design the new-user recommender, and compute the expected clicks per 100 impressions with that exploration and without it, and the relative loss against the no-exploration figure.
**Asked at:** General ML system-design prep material (Educative's 6-step ML design framework and fraud-detection mock interview, DesignGurus, techinterview.org, PracHub's 2026 ML system design bank and a DEV Community guide describe open prompts such as feed or recommendation, search ranking and ad prediction, and one guide quotes a search prompt with 1,000 queries per second and 200 ms); commercial prep sites, so example numbers are treated as examples only; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** With 10% exploration at 1.5% and 90% at 3%, I expect 0.10 x 1.5 + 0.90 x 3 = 2.85 clicks per 100 impressions against 3.00 without it, a 5% relative loss, and I would accept that price only because exploration is how a new user's profile gets learned.

**Clarifying questions:**
- Were the 1.5% and 3% measured on new users or on existing users? The sample may not transfer to people with no history, so I treat both as starting guesses.
- What is the goal for a new user (first order, second-week return, basket size)? Clicks are only a proxy, and exploration pays off in later sessions, not in the first click.
- What can be used before any history (city, device, time of day, install source, popular items)? That is the baseline policy for the cold start.
- How many items and categories exist, and how fast does the catalogue change? That decides how much exploration is needed.
- Are there items we must never show (out of stock, age-restricted, local rules)? Exploration must stay inside safe limits.
- How long does a user stay "new"? An exit rule from cold start sets how much of the traffic explores.

**Approach:** (about 7 steps; pacing for a 45-minute round: 5 / 5 / 6 / 6 / 9 / 8 / 6)
1. Clarify and frame (5 min). Goal: get a new user to a good first basket and a return visit, while learning fast. Say the arithmetic: 2.85 versus 3.00, 5% cost per slot.
2. Metrics and guardrails (5 min). Primary: clicks per 100 impressions in the first session, plus the real goal (orders in the first 7 days per new user). Guardrails: add-to-cart and order rate, return-visit rate on day 7, share of slots on out-of-stock or poor items, latency.
3. Data and labels (6 min). Impressions with clicks and orders, logged with the policy and the probability of showing each item (propensity). Without logged propensities, later learning from exploration data is biased.
4. Baseline first (6 min). Popularity by city and time of day, with a few hand-made category slots. That is the policy that gets 3%.
5. Model and trade-offs (9 min). A contextual bandit or a simple epsilon-greedy over popular items with a decaying exploration share; as a user's history builds, a personalised ranker takes over. Trade-off: exploration cost is 5% of clicks at 10%; the policy must improve by more than 5.56% relative (3.00% to 3.17%) for exploration to break even on clicks alone. Use smarter exploration (explore among decent items, not random ones) to cut the cost.
6. Evaluate offline, then online (8 min). Offline: replay logged data with propensities (inverse-propensity weighting) as a rough check only. Online: randomise users to exploration shares (0%, 5%, 10%) and measure 7-day orders per new user, not first-session clicks.
7. Monitoring, retraining and risks (6 min). Watch exploration share, popularity feedback loops (popular items get more clicks only because they are shown), catalogue coverage and per-city results. Retrain daily for new items. Cost is small compared with the learning value; the trade-off is a few percent of first-session clicks.

**Metrics:**
- Expected clicks per 100 impressions = 100 x (explore share x explore CTR + (1 - explore share) x policy CTR) = 2.85.
- Relative loss = (3.00 - 2.85) / 3.00 = 5%, base is the no-exploration figure.
- 7-day orders per new user = orders in 7 days from new users / new users in the arm.
- Catalogue coverage = distinct items shown to new users in a day / items in stock.
- Guardrails: out-of-stock impression share, day-7 return rate, latency.

**Risks:**
- The 1.5% and 3% are sample estimates (a 1.5% from 2,000 impressions could be 1.0% to 2.0%).
- The 5% is a first-session cost; the learning benefit is not in the figure.
- Rates are assumed constant; exploring on low-quality items may hurt the experience more than clicks show.
- Popularity bias: the algorithm shows popular items, they get clicks, they stay popular.
- Without logged propensities the exploration data cannot be used fairly.

**What the interviewer scores:**
- Strong: computes 2.85 and 5% quickly and frames it as the price of learning. Weak: "exploration is wasteful" or "explore a lot".
- Strong: a baseline first, then bandit, with a break-even condition. Weak: jumps to a deep model with no history.
- Strong: measures the long-run outcome, not first-click CTR. Weak: only clicks.
- Strong: says the rates are samples and may not transfer to new users. Weak: treats them as exact.

**Example:** Illustrative numbers. On 60,000 new users with 20 impressions each (1,200,000 impressions, an invented figure), the 5% relative loss is 0.15 clicks per 100, which is 1,800 clicks a day.
- Weak: "I would use 10% exploration because that is standard."
- Strong: "Ten percent exploration costs 0.15 clicks per 100 impressions, 2.85 against 3.00, a 5% loss. It is worth it only if it lifts the learned policy by about 5.6% relative or raises 7-day orders. I would test 0, 5 and 10 percent on new users and judge them by 7-day orders, with propensities logged."

**Code:**
```python
# Q26 cold-start exploration cost (illustrative rates, from a sample)
import random
explore, ctr_explore, ctr_policy = 0.10, 0.015, 0.03
with_exp = 100 * (explore * ctr_explore + (1 - explore) * ctr_policy)
without = 100 * ctr_policy
loss = (without - with_exp) / without
assert abs(with_exp - 2.85) < 1e-9 and abs(without - 3.0) < 1e-9 and abs(loss - 0.05) < 1e-9
print(f"clicks per 100 impressions: with exploration={with_exp:.2f}, without={without:.2f}, relative loss={loss:.1%}")

# What the learned policy must gain for exploration to pay back (rates held as assumptions)
needed = (ctr_policy - explore * ctr_explore) / (1 - explore)
assert abs(needed - 0.031667) < 1e-5
print(f"policy CTR must rise from 3.00% to {needed:.3%} ({needed/ctr_policy-1:.2%} relative) to break even")

# Simulation check with a fixed seed
random.seed(11)
n = 1_000_000
clicks = 0
for _ in range(n):
    p = ctr_explore if random.random() < explore else ctr_policy
    clicks += random.random() < p
sim = clicks / n * 100
assert abs(sim - with_exp) < 0.05
print(f"simulated clicks per 100 impressions={sim:.2f}")

# Noise in the measured rates: a 1.5% rate from 2,000 impressions (invented) has a wide interval
imp = 2_000
se = (ctr_explore * (1 - ctr_explore) / imp) ** 0.5
lo, hi = ctr_explore - 1.96 * se, ctr_explore + 1.96 * se
assert abs(lo - 0.00961) < 1e-4 and abs(hi - 0.02039) < 1e-4
print(f"1.5% from {imp} impressions: 95% interval {lo:.2%} to {hi:.2%}")
# Example: 60,000 new users x 20 impressions (invented)
imps = 60_000 * 20
assert imps == 1_200_000 and round(imps * (ctr_policy - (with_exp / 100))) == 1_800
print(f"daily clicks lost at {imps:,} impressions: {imps*(ctr_policy-with_exp/100):,.0f}")
```

**Output (my run):**
```text
clicks per 100 impressions: with exploration=2.85, without=3.00, relative loss=5.0%
policy CTR must rise from 3.00% to 3.167% (5.56% relative) to break even
simulated clicks per 100 impressions=2.81
1.5% from 2000 impressions: 95% interval 0.97% to 2.03%
daily clicks lost at 1,200,000 impressions: 1,800
```

**Follow-ups:**
- How would you cut the cost of exploration? Explore only among items already above a quality bar, shrink the share as history builds, and explore more where the model is uncertain.
- What if the catalogue is tiny? Then little exploration is needed, a few percent, because popular items already cover it.
- Why does popularity feedback matter? The items shown get clicks, so popularity looks self-confirming; logged propensities and some random slots keep the data honest.

**Common mistakes:** Judging exploration by first-session clicks only. Treating sample rates as exact. Not logging propensities. Using random items rather than decent ones. Using the same exploration share forever.

### Q27 ⭐⭐ 🟡 Vernacular search evaluation: A shopping app serves 3,000,000 queries a day in 8 languages and has a labelling budget of 120,000 rupees at 4 rupees per human relevance judgement. You want each language measured to within plus or minus 2.5 percentage points at 95% confidence for a proportion near 50%, using n = (1.96 times 0.5 over 0.025) squared, rounded up. Design the evaluation and labelling plan, and compute the judgements bought, the judgements per language for that precision, the total for 8 languages and what remains.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to multilingual search relevance evaluation (no page found in these searches); search snippets only, not opened
**Say this first (1 line):** The budget buys 120,000 / 4 = 30,000 judgements, precision of plus or minus 2.5 points needs 1,537 per language (1,536.64 rounded up), 8 languages cost 12,296, leaving 17,704, which I would spend on a harder question than one headline number per language.

**Clarifying questions:**
- What is being measured: the share of queries with a relevant result in the top results, NDCG, or a side-by-side preference? The 1,537 formula is for one proportion; other metrics need their own sizing.
- Is the goal to describe each language, or to compare two search systems in each language? A comparison needs more labels (about 3,074 per language per system at the same precision if samples are separate).
- How many judges per item, and how well do they agree? Two judges per item double the cost and give an agreement estimate; Hinglish and mixed script are the hard cases.
- Are queries drawn at random from traffic, or by popularity? Random draws describe users; head-heavy draws miss the long tail where search fails.
- Who are the judges (native speakers per language)? Quality and the cost of 4 rupees depend on it.
- Does the 8-language split reflect traffic? Small languages may need a different precision target.

**Approach:** (about 7 steps; pacing for a 45-minute round: 5 / 5 / 8 / 5 / 7 / 8 / 7)
1. Clarify and frame (5 min). The goal is a trustworthy relevance number per language, so that regressions are visible. Say the budget arithmetic: 30,000 judgements.
2. Metrics and guardrails (5 min). Primary: share of judged query-result pairs rated relevant (at top 5) per language. Guardrails: judge agreement per language and the share of queries with no result.
3. Data and labels (8 min). Sample queries at random per language (stratify by head, torso, tail), gold questions to check judges, written guidelines for mixed-script queries, two judges on a 10% slice to measure agreement.
4. Baseline first (5 min). One fixed judged set per language, scored once on the current system. That is the yardstick before any new model.
5. Model and trade-offs (7 min). The "model" here is the sampling plan: 1,537 per language gives about plus or minus 2.5 points for a proportion near 50%. Trade-off: eight separate 95% intervals all cover their truths only about 66% of the time; making them hold jointly needs 2,991 per language (23,928 total), still inside the 30,000.
6. Evaluate offline, then online (8 min). Offline: judged sets for regression checks on every ranker change. Online: compare click and reformulation metrics per language as a cross-check, since judgements and clicks can disagree.
7. Monitoring, retraining, risks and cost (7 min). Refresh a fraction of the set monthly as queries drift, keep a frozen core, track judge drift with gold items. Use leftover budget for tail queries or double judging. Risks: judge bias, stale sets, an LLM judge not validated against humans.

**Metrics:**
- Relevant share per language = pairs judged relevant / pairs judged, in that language.
- Margin = 1.96 x sqrt(p(1-p)/n), with p = 0.5 and n = 1,537 gives about 0.025.
- Agreement = pairs where both judges agree / pairs double-judged (or a chance-corrected kappa).
- Budget used = judgements x 4 rupees (12,296 x 4 = 49,184).
- Guardrail: the share of the budget on gold and double-judged items (target a stated small share).

**Risks:**
- The formula assumes a simple random sample of independent items; several judgements on one query are correlated, so the real margin is wider.
- p near 50% is the worst case; if p is 80% the same n gives a narrower margin.
- 8 intervals at 95% each are not 95% jointly.
- Tail queries drive complaints but rarely appear in a random sample.
- Judges may disagree on code-mixed queries; a noisy label limits what any sample size shows.

**What the interviewer scores:**
- Strong: 30,000, 1,537, 12,296 and 17,704 quickly and in the right units (judgements, then rupees). Weak: mixes rupees and judgements.
- Strong: knows what the margin applies to (one proportion) and the multiple-intervals point. Weak: quotes 2.5 points for everything.
- Strong: judge quality, guidelines, gold items. Weak: "buy labels" with no quality plan.
- Strong: spends the remainder on a stated purpose (tail, comparison, agreement). Weak: leaves it unspent.

**Example:** Illustrative numbers. After the 12,296 judgements, 17,704 remain (70,816 rupees); 1,600 tail queries x 8 languages = 12,800 more would leave 4,904.
- Weak: "I would label 30,000 queries and see how it goes."
- Strong: "1,537 judgements per language gives plus or minus 2.5 points, 12,296 in total, 17,704 left. I would keep the rest for tail queries and a second judge on a slice, and if we need all eight intervals to hold together I would go to 2,991 per language, 23,928 in all."

**Code:**
```python
# Q27 vernacular search evaluation labelling plan (illustrative)
import math
from statistics import NormalDist
budget, price, langs, moe = 120_000, 4, 8, 0.025
bought = budget // price
n_raw = (1.96 * 0.5 / moe) ** 2
n = math.ceil(n_raw)
total = langs * n
left = bought - total
assert bought == 30_000 and abs(n_raw - 1536.64) < 1e-9 and n == 1537
assert total == 12_296 and left == 17_704
print(f"bought={bought}, n per language={n} (raw {n_raw:.2f}), total={total}, remaining={left} judgements = {left*price} rupees")

# Joint coverage of 8 separate 95% intervals
joint = 0.95 ** langs
assert abs(joint - 0.6634) < 1e-3
print(f"chance all 8 intervals cover their truth ~ {joint:.1%} (independent)")

# Bonferroni: 8 intervals jointly at 95%
z = NormalDist().inv_cdf(1 - 0.05 / (2 * langs))
nb = math.ceil((z * 0.5 / moe) ** 2)
assert abs(z - 2.734) < 0.001 and nb == 2991 and langs * nb == 23_928 and bought - langs * nb == 6_072
print(f"Bonferroni z={z:.3f}, n per language={nb}, total={langs*nb}, remaining={bought-langs*nb}")

# Comparing two rankers on separate samples needs more (a paired design on shared queries can need less)
# Unpaired two-sample on proportions near 50%: n per arm = 2*(1.96*0.5/0.025)^2
nu = math.ceil(2 * (1.96 * 0.5 / 0.025) ** 2)
assert nu == 3074
print(f"unpaired comparison of two systems at same precision: {nu} per language per system")
assert langs * n * price == 49_184 and left - 1_600 * langs == 4_904 and left * price == 70_816
```

**Output (my run):**
```text
bought=30000, n per language=1537 (raw 1536.64), total=12296, remaining=17704 judgements = 70816 rupees
chance all 8 intervals cover their truth ~ 66.3% (independent)
Bonferroni z=2.734, n per language=2991, total=23928, remaining=6072
unpaired comparison of two systems at same precision: 3074 per language per system
```

**Follow-ups:**
- Can an LLM judge replace humans? It can cut cost, but validate it against a human-labelled slice per language and do not let it grade its own system alone. See Book 6 Part 3 (the question on using one LLM for labels and as the judge).
- How do you compare two rankers? Judge both on the same queries and analyse the paired difference; unpaired samples need about double the n at the same precision.
- What if a language has few queries? The sample is capped by what exists; report a wider interval honestly.

**Common mistakes:** Confusing rupees with judgements. Using p = 0.5 and ignoring that it is the worst case. Forgetting the margin applies to one proportion. Not rounding up. No judge-quality checks. Ignoring correlation within queries.

### Q28 ⭐⭐ 🔴 LLM analytics assistant: An internal assistant for 800 employees answers 5,000 questions a day, each using an average of 2.4 LLM calls of 6,000 tokens, at an illustrative blended 0.25 rupees per 1,000 tokens against a monthly budget of 60,000 rupees (30 days). Design the assistant with its data-access limits and evaluation, and compute the monthly cost as designed, the factor by which cost must fall and two levers that could deliver it.
**Asked at:** Agentic and GenAI design material (Dataford agentic AI engineer guides listing multi-step customer-service workflows, techinterview.org and aiforanything.io pages on AI agent infrastructure and system design, and a post-LLM-era ML engineer interview guide saying 'design an LLM-based system for X' is now the most common prompt); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** As described the assistant uses 5,000 x 2.4 x 6,000 = 72 million tokens a day, 18,000 rupees a day, 540,000 a month, which is 9 times the 60,000 budget, so I design for a 9x cost cut first (route most calls to a small model and shrink the context) and treat quality and data access as the other two fixed constraints.

**Clarifying questions:**
- Is 6,000 tokens per call or per question? I read it per call (14,400 per question); if it is per question, the cost is 225,000 a month, 3.75 times over. It changes how hard the cut is.
- What kinds of questions arrive (look up a number, build a chart, explain a trend)? Simple look-ups can use a cheap path.
- Which data may each employee see? Row-level and column-level access must follow the user, not the assistant. I ask the data-governance owner; I assume nothing.
- How wrong may an answer be? A wrong number in a board deck is worse than a refusal, so I set a wrong-answer ceiling before choosing models.
- Is the 0.25 blended price input plus output, and does it hold for a small model? I use it as given and treat a cheaper model price as an assumption to check.
- Is the budget a hard cap or a target? That sets whether we throttle or only alert.

**Approach:** (about 8 steps; pacing for a 45-minute round: 4 / 5 / 5 / 6 / 8 / 7 / 5 / 5)
1. Clarify and frame (4 min). Users are 800 employees asking about internal data. Success is a correct, traceable answer at a cost within 60,000 rupees a month. Say the gap aloud: 540,000 versus 60,000.
2. Metrics and guardrails (5 min). Primary: share of questions answered correctly (checked against a reference or a reviewer). Cost per question against 0.40 rupees allowed (60,000 / 30 / 5,000). Guardrails: wrong-answer rate, refusal rate, access violations (target zero), latency.
3. Data and labels (5 min). Collect 200 to 300 real questions with correct answers from analysts, split by type and difficulty. This is the test set and the source of routing labels.
4. Baseline first (6 min). Retrieval over a small governed set of tables and metric definitions, one strong model, one call per question. Measure accuracy and cost per question before adding agents.
5. Model and trade-offs (8 min). Generate queries against a semantic layer or approved views, run them under the asking user's permissions, and have the model explain the result. Cost levers: route about 80% of calls to a small model (a 3.57x cut if it is priced at a tenth, an assumption), cut tokens per call from 6,000 to 2,000 by sending only the relevant schema (3x), cache repeated questions. Together the first two give 10.7x, about 50,400 a month. Trade-off: cheaper paths lose accuracy on hard questions, so route by difficulty and escalate on low confidence.
6. Evaluate offline, then online (7 min). Offline: accuracy on the test set per route, and cost per question. Online: pilot with one team, thumbs and analyst spot checks, compare with a human analyst on a sample.
7. Launch, monitoring and retraining (5 min). Daily spend alert at 50% and 100% of the budget pace, per-user quota, logs of every query and the data touched, weekly review of failures, refresh the test set monthly.
8. Risks and cost (5 min). Wrong but confident numbers, data leakage across teams, prompt injection through table contents, costs creeping with usage. Build versus buy: buying a vendor tool shifts cost and data-access questions, which I would raise with security.

**Metrics:**
- Monthly cost = questions x calls x tokens per call / 1,000 x price x 30 = 540,000.
- Cost per question = 2.4 x 6,000 / 1,000 x 0.25 = 3.60 rupees; the allowed figure is 0.40.
- Answer accuracy = correct answers / questions in the test set (and in the audited live sample).
- Escalation rate = calls sent to the strong model / all calls.
- Guardrails: wrong-answer rate on audited live answers, access violations (zero), p95 latency.

**Risks:**
- Prices and the small-model share are assumptions; measure them.
- A 9x cut with no quality check just moves the cost into wrong answers.
- Caching can serve stale numbers; key it on data version and user permissions.
- Users who ask more because it is cheap raise the volume; a quota is needed.
- The assistant runs queries as a service account and exposes data a user may not see.

**What the interviewer scores:**
- Strong: 72 million, 540,000 and 9x in seconds, then levers with numbers. Weak: "use a cheaper model" with no figure.
- Strong: access follows the user, queries run under the user's rights. Weak: one shared database login.
- Strong: accuracy measured on a real question set before and after cost cuts. Weak: only cost.
- Strong: spots the ambiguity in 6,000 tokens per call. Weak: silently picks one.

**Example:** Illustrative numbers. Routing 80% of calls to a model at one tenth of the price gives 0.2 + 0.08 = 0.28 of the cost (3.57x cheaper); cutting 6,000 tokens to 2,000 gives 3x; together 10.7x, so 540,000 becomes about 50,400.
- Weak: "That is expensive, so I would switch to a smaller model."
- Strong: "As designed it costs 540,000 a month, 9 times the budget, or 3.60 rupees a question against 0.40 allowed. Routing most calls to a small model gives about 3.6x, pruning the context from 6,000 to 2,000 tokens gives 3x, together 10.7x, about 50,000. I would check accuracy on 250 real questions at every step, and run every query under the asker's own permissions."

**Code:**
```python
# Q28 LLM analytics assistant cost (illustrative prices)
qpd, calls, tok, price_k, budget, days = 5_000, 2.4, 6_000, 0.25, 60_000, 30
tokens_day = qpd * calls * tok
cost_day = tokens_day / 1000 * price_k
cost_month = cost_day * days
factor = cost_month / budget
assert tokens_day == 72_000_000 and cost_day == 18_000 and cost_month == 540_000 and factor == 9
print(f"tokens/day={tokens_day:,.0f}, cost/day={cost_day:,.0f}, cost/month={cost_month:,.0f}, factor over budget={factor:.0f}x")
per_q = calls * tok / 1000 * price_k
allowed = budget / days / qpd
assert abs(per_q - 3.6) < 1e-9 and abs(allowed - 0.4) < 1e-9
print(f"cost per question={per_q:.2f} rupees, allowed={allowed:.2f}")

# Lever A: route 80% of calls to a small model priced at 0.1x (assumed)
price_factor = 0.2 + 0.8 * 0.1
a = 1 / price_factor
# Lever B: cut tokens per call 6,000 -> 2,000 (schema pruning, short context)
b = 6_000 / 2_000
assert abs(a - 3.5714) < 1e-3 and b == 3
both = a * b
new_month = cost_month / both
assert abs(both - 10.714) < 1e-2 and new_month < budget and abs(new_month - 50_400) < 1
print(f"routing alone {a:.2f}x, token cut alone {b:.1f}x (neither reaches 9x), both {both:.2f}x -> {new_month:,.0f} per month")
# Lever C: answer cache with 30% hit rate adds headroom
c = 1 / 0.7
assert abs(both * c - 15.31) < 0.01
print(f"adding a 30% cache hit rate: {both*c:.2f}x -> {cost_month/(both*c):,.0f} per month")

# Alternative reading: 6,000 tokens per question in total
alt = qpd * 6_000 / 1000 * price_k * days
assert alt == 225_000 and abs(alt / budget - 3.75) < 1e-9
print(f"if 6,000 tokens were per question: {alt:,.0f} per month, {alt/budget:.2f}x over")
```

**Output (my run):**
```text
tokens/day=72,000,000, cost/day=18,000, cost/month=540,000, factor over budget=9x
cost per question=3.60 rupees, allowed=0.40
routing alone 3.57x, token cut alone 3.0x (neither reaches 9x), both 10.71x -> 50,400 per month
adding a 30% cache hit rate: 15.31x -> 35,280 per month
if 6,000 tokens were per question: 225,000 per month, 3.75x over
```

**Follow-ups:**
- What if the small model fails on hard questions? Escalate on low confidence or failed validation of the generated query; accept a small rise in cost on the hard tail.
- How do you stop a user from seeing data they should not? Run queries with the user's identity and the database's row and column permissions, log every query. I ask security and data governance how access is defined.
- How would you keep cost from creeping? Per-user and per-team quotas, a daily spend alert, and a monthly review of the top query types.

**Common mistakes:** Quoting cost per token and not per question. Cutting cost without an accuracy check. One shared service account. Forgetting caches need permission-aware keys. Not stating the per-call versus per-question reading.

### Q29 ⭐⭐ 🔴 Vision identity verification: A lender's app runs 40,000 selfie-and-ID checks a day, and 0.1% are spoof attempts (a projection from last quarter's investigations). A liveness model catches 95% of spoofs on a test set of known attack types (a sample), and new attack types are expected. Design the verification flow end to end with fallback and human review, compute the spoofs a day and how many pass liveness, and say what you would ask compliance.
**Asked at:** Healthcare and vision design material (a Dataford prompt on end-to-end ML for medical signal or image data, behind a sign-up wall, and an arXiv technology-readiness paper noting trust as a barrier in regulated fields; no triage-specific interview page was found); commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** 40,000 x 0.1% is 40 spoof attempts a day, a 95% catch rate stops 38 and lets 2 through, but that 2 is a best case because the 95% was measured on known attack types and new ones are expected, so I design layers, a human fallback and a fast retraining loop rather than trusting one liveness score.

**Clarifying questions:**
- What do spoofs cost (a fraudulent loan disbursed) compared with a genuine customer turned away? That sets the threshold and how much human review we can afford.
- Is the 0.1% the share of attempts or of customers, and how was it found (confirmed investigations only)? Undetected spoofs mean it is likely an underestimate.
- How big was the test set behind 95%, and which attack types did it contain (printed photo, screen replay, mask, deepfake)? A small set gives a wide interval and says nothing about new types.
- What is the false-reject rate on genuine users today, and for which phones, lighting and skin tones? Failure for honest users is the main cost of strictness.
- What other signals exist (device, location, behaviour, document checks, a second factor)? Layers reduce dependence on one model.
- Which checks and data retention does the lender need from compliance and legal? I ask; I do not assume rules.

**Approach:** (about 7 steps; pacing for a 45-minute round: 5 / 5 / 6 / 5 / 9 / 8 / 7)
1. Clarify and frame (5 min). Goal: stop impersonation without turning honest customers away. Say the numbers aloud: 40 spoofs, 38 caught, 2 passing as a best case.
2. Metrics and guardrails (5 min). Primary: spoofs reaching approval per day (confirmed later), and attack catch rate by attack type. Guardrails: genuine users falsely rejected, share sent to human review, completion time, subgroup false-reject rates.
3. Data and labels (6 min). Confirmed spoofs from investigations, red-team attacks built in-house for each new type, genuine sessions across phones and lighting. Keep the test set split by attack type so "new attack" is tested honestly.
4. Baseline first (5 min). The current liveness check plus document checks and device signals, a simple score threshold, and a human fallback. Measure its false-reject and catch rates by type.
5. Model and trade-offs (9 min). Layered flow: capture quality check, active liveness challenge, passive liveness model, face match to the ID, device and behaviour risk score. Three routes: pass, step-up (retry or another factor), human review. Trade-off: a stricter threshold catches more spoofs and rejects more genuine users; use two thresholds so the middle band goes to step-up, not to rejection.
6. Evaluate offline, then online (8 min). Offline: catch rate per attack type on a held-out attack type set (leave-one-attack-out), false-reject rate by subgroup, with intervals. Online: shadow mode first, then a small share of traffic, with confirmed spoofs tracked to the loan outcome.
7. Monitoring, retraining, risks and cost (7 min). Weekly red-team of new attack types, alert on score distribution drift, track review queue age, retrain when a new attack is confirmed. Risks: deepfakes, bias across skin tones and phones, adversaries probing the thresholds, privacy of biometric data (ask compliance and legal about consent, storage and retention).

**Metrics:**
- Spoofs per day = checks x spoof share = 40,000 x 0.001 = 40.
- Spoof pass rate = spoofs that pass liveness / spoofs (5% on known attacks; unknown on new ones).
- False reject rate = genuine users rejected or stepped up / genuine users (denominator 39,960).
- Review queue = users sent to a human per day, and its share that are real spoofs.
- Guardrails: false-reject rate per subgroup, review time, time to onboard.

**Risks:**
- 2 passing spoofs a day is a floor; at an assumed 50% catch on a new attack it is 20 a day.
- The 95% comes from a test of invented size 200 (190 caught); the interval is 91.0% to 97.3%.
- A 1% false-reject on 39,960 genuine users sends about 400 people a day to fallback, more than the spoofs.
- Adversaries adapt to a published threshold.
- Biometric data creates privacy and storage obligations; ask compliance and legal.

**What the interviewer scores:**
- Strong: 40, 38, 2 immediately, then says why 2 is optimistic. Weak: stops at "95% is good".
- Strong: layers, step-up, human review and a plan for new attacks. Weak: a single model.
- Strong: measures false rejects on honest users and by subgroup. Weak: only the catch rate.
- Strong: defers legal and biometric rules to compliance. Weak: invents them.

**Example:** Illustrative numbers. If the catch rate on a new attack type is 50%, 20 spoofs a day pass; with a 1% false-reject rate about 400 genuine users go to fallback, so about 8.7% of a 438-case review queue are real spoofs.
- Weak: "Liveness catches 95%, so only 2 spoofs get through."
- Strong: "40 attempts a day, 38 caught, 2 pass, but only against known attack types, so I treat 2 as a best case. I would add a step-up route, a human review band, a weekly red-team for new attacks and shadow mode before launch, and measure false rejects by phone and lighting. Biometric rules are a question for compliance and legal."

**Code:**
```python
# Q29 identity verification (illustrative; 0.1% is a projection, 95% is a sample on known attacks)
from math import sqrt
checks, spoof_rate, catch = 40_000, 0.001, 0.95
spoofs = round(checks * spoof_rate)
caught = spoofs * catch
passed = spoofs - caught
assert spoofs == 40 and caught == 38 and abs(passed - 2) < 1e-9
print(f"spoofs/day={spoofs}, caught={caught:.0f}, pass liveness={passed:.0f} (best case: known attacks only)")

# Sensitivity to the catch rate on new attack types
for r in (0.95, 0.80, 0.50, 0.20):
    print(f"  catch {r:.0%}: {spoofs*(1-r):.0f} spoofs pass a day")
assert abs(spoofs * (1 - 0.2) - 32) < 1e-9
assert spoofs * (1 - 0.5) == 20 and abs(spoofs * (1 - 0.8) - 8) < 1e-9

# The 95% is from a test set; invented size 200 attacks, 190 caught -> Wilson interval
n, k, z = 200, 190, 1.96
p = k / n
den = 1 + z * z / n
centre = (p + z * z / (2 * n)) / den
half = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
lo, hi = centre - half, centre + half
assert abs(lo - 0.9104) < 0.002 and abs(hi - 0.9727) < 0.002
print(f"95% from 190/200: interval {lo:.1%} to {hi:.1%} -> {spoofs*(1-hi):.1f} to {spoofs*(1-lo):.1f} pass")

# Cost on genuine users: invented 1% fall back to human review
genuine = checks - spoofs
fallback = genuine * 0.01
assert genuine == 39_960 and abs(fallback - 399.6) < 1e-9
print(f"genuine users sent to fallback at 1%: {fallback:.1f} a day")
# Queue that a review team must handle: fallback plus caught spoofs
queue = fallback + caught
assert abs(queue - 437.6) < 1e-9
print(f"daily human-review queue ~ {queue:.1f} cases")
# Precision of the fallback queue
prec = caught / queue
assert abs(prec - 0.0868) < 1e-3
print(f"share of that queue that are real spoofs ~ {prec:.1%}")
```

**Output (my run):**
```text
spoofs/day=40, caught=38, pass liveness=2 (best case: known attacks only)
  catch 95%: 2 spoofs pass a day
  catch 80%: 8 spoofs pass a day
  catch 50%: 20 spoofs pass a day
  catch 20%: 32 spoofs pass a day
95% from 190/200: interval 91.0% to 97.3% -> 1.1 to 3.6 pass
genuine users sent to fallback at 1%: 399.6 a day
daily human-review queue ~ 437.6 cases
share of that queue that are real spoofs ~ 8.7%
```

**Follow-ups:**
- What if a deepfake attack appears? Block the pattern with a quick rule, add it to the red-team set, retrain, and use step-up for the risky band while it is fixed.
- How do you handle a rejected honest customer? A clear retry route and a human review path, because a hard rejection with no recourse is a harm in itself.
- How many human reviewers? Compute the queue (about 438 a day at the assumed 1% false-reject) times minutes per case; the review time is an input I would measure.

**Common mistakes:** Treating the known-attack catch rate as the real one. Ignoring false rejects of genuine users. One threshold with no middle band. No plan for new attack types. Storing biometrics without asking compliance. Using no subgroup checks.

### Q30 ⭐⭐ 🔴 Clinical note summarisation: An LLM tool will summarise 8,000 clinical notes a day across 12 hospitals, and you want to detect an unsupported-claim rate of 2% or more with 95% confidence by auditing a random daily sample of independent notes. The audit should miss a true 2% rate with probability at most 5%. Design the rollout, safeguards and monitoring, compute the smallest daily audit size n with 1 minus 0.98 to the power n at least 0.95 and its share of the day's notes, and say what you would ask compliance.
**Asked at:** Healthcare and vision design material (a Dataford prompt on end-to-end ML for medical signal or image data, behind a sign-up wall, and an arXiv technology-readiness paper noting trust as a barrier in regulated fields; no triage-specific interview page was found); commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** ln 0.05 / ln 0.98 is 148.28, so the smallest daily audit is 149 notes, 1.86% of 8,000, which gives a 95% chance of seeing at least one unsupported note if the true rate is exactly 2%, and I would roll out in stages with every summary linked to its source note and a clinician in control.

**Clarifying questions:**
- What counts as an "unsupported claim" (a statement not in the note, a wrong drug or dose, an omission), and is the rate counted per note or per sentence? The 2% and the 149 are per note with at least one unsupported claim; I would define severity grades too.
- Who audits, and how good are they? An auditor who misses errors lowers the real detection chance; two auditors on a slice measure that.
- Are the 8,000 notes spread evenly across the 12 hospitals, and is the risk the same everywhere (specialty, language, note style)? A pooled sample can hide one bad hospital.
- Does the summary replace reading the note, or sit beside it? A clinician reading the summary instead of the note raises the stakes.
- Which errors are unacceptable regardless of rate (wrong allergy, wrong dose)? A rate target is not enough for those; they need hard checks.
- What does compliance and legal require for patient data, model use, audit records and sign-off? I ask; I do not state rules.

**Approach:** (about 8 steps; pacing for a 45-minute round: 4 / 5 / 5 / 5 / 8 / 8 / 5 / 5)
1. Clarify and frame (4 min). Goal: save clinician time without adding unsupported statements to the record. Define the error and say the sample-size maths aloud: 0.98 to the power 149 is 0.0493, below 5%.
2. Metrics and guardrails (5 min). Primary: unsupported-note rate (notes with at least one unsupported claim / notes audited), by severity. Guardrails: omission rate for key items (allergies, doses, diagnoses), clinician edit rate, time saved, complaints.
3. Data and labels (5 min). A gold set of notes with clinician-written summaries and error annotations. Audit labels need written guidelines and double review on a slice.
4. Baseline first (5 min). Extractive summary (selected sentences from the note) or a template of key fields, plus the clinician's current workflow. The LLM must beat it on errors, not on style.
5. Model and trade-offs (8 min). An LLM that must cite the source sentence for every claim, a check that each cited sentence supports the claim, and a block on high-risk fields unless they match the note exactly. Trade-off: stricter grounding reduces fabrication and also drops useful inference; accept shorter summaries. Human edits the summary before it enters the record at first.
6. Evaluate offline, then online (8 min). Offline: unsupported-note rate and omission rate on the gold set and on notes from each hospital, with intervals. Online: shadow mode, then one department, then hospitals in stages, with the daily random audit of 149 notes pooled and a stricter schedule at launch.
7. Monitoring, retraining and risks (5 min). The daily audit has limits: 149 notes detect a 2% rate with 95% probability, but a 1% true rate is caught only 77.6% of days, and 0.5% only 52.6%. Zero found in 149 means the rate is below about 1.99% with 95% confidence. Add automatic checks on every summary (citation present, high-risk fields match) and trend the weekly pooled audit.
8. Risks and cost (5 min). A pooled audit has about 12 notes per hospital, so a bad hospital hides; auditing 149 per hospital costs 1,788 notes a day (22.35%), so rotate hospitals or audit extra at launch. Cost is auditor time; ask compliance and legal about records, consent and who signs off.

**Metrics:**
- Unsupported-note rate = audited notes with at least one unsupported claim / audited notes.
- Detection probability = 1 - (1 - 0.02)^n, equal to 0.9507 at n = 149 (0.9497 at 148).
- Audit share = 149 / 8,000 = 1.86%.
- Omission rate = notes missing a required item (allergy, dose, diagnosis) / notes audited.
- Guardrails: clinician edit rate, per-hospital rate with intervals, time saved per note.

**Risks:**
- The audit is a detection rule for a 2% rate, not an estimate of the rate; one error in 149 gives a very wide interval.
- Independence matters: notes from one clinician or one hospital are correlated, so the real power is lower.
- Auditors miss errors; the true unsupported rate is higher than the audited one.
- A 2% rate may be too high for severe errors, which need their own zero-tolerance checks.
- Pooled sampling hides a bad hospital.

**What the interviewer scores:**
- Strong: derives 149 and 1.86%, and states what it guarantees and does not (95% chance of at least one at a 2% rate; weaker at lower rates). Weak: says "95% confident the rate is below 2%" with no condition.
- Strong: staged rollout with human review, citation grounding, hard checks on high-risk fields. Weak: "ship and monitor".
- Strong: notices the per-hospital hiding problem and its cost. Weak: ignores the 12 hospitals.
- Strong: asks compliance and legal and states no rules. Weak: invents them.

**Example:** Illustrative numbers. If the true rate is 1%, 149 notes catch at least one error on 77.6% of days; auditing each of 12 hospitals at 149 notes takes 1,788 notes a day, so I would rotate: one hospital a day at 149, each hospital every 12 days.
- Weak: "I would audit 5% of notes and see if the error rate is low."
- Strong: "149 notes a day, 1.86%, gives at least a 95% chance of catching at least one unsupported note if the rate is 2%. That is a tripwire, not a measurement, and at 1% it works 78% of the time. The sample is pooled over 12 hospitals, so I would add per-hospital rotation, automatic grounding checks on every summary, a clinician who edits before filing, and a staged launch. Legal and records questions go to compliance and legal."

**Code:**
```python
# Q30 audit sample size for unsupported-claim rate (illustrative)
import math
import numpy as np
p, notes, target = 0.02, 8_000, 0.95
n = math.ceil(math.log(1 - target) / math.log(1 - p))
assert n == 149 and 1 - (1 - p) ** n >= target > 1 - (1 - p) ** (n - 1)
share = n / notes
assert round(share * 100, 2) == 1.86
print(f"smallest n={n}, share of the day's notes={share:.2%}, detection prob at n: {1-(1-p)**n:.4f} (n-1: {1-(1-p)**(n-1):.4f})")

# Power at other true rates with n = 149
for r in (0.005, 0.01, 0.02, 0.03):
    print(f"  true rate {r:.1%}: P(at least one unsupported note in sample) = {1-(1-r)**n:.3f}")
assert abs((1 - 0.995 ** n) - 0.526) < 0.002 and abs((1 - 0.99 ** n) - 0.776) < 0.002

# If zero are found in 149: one-sided 95% upper bound for the rate
upper = 1 - 0.05 ** (1 / n)
assert abs(upper - 0.01987) < 1e-4
print(f"zero found in {n}: upper 95% bound on the rate = {upper:.2%}")

# Seeded simulation of the daily audit when the true rate is exactly 2%
rng = np.random.default_rng(5)
days = 200_000
hits = rng.binomial(n, p, size=days)
detect = (hits >= 1).mean()
assert abs(detect - 0.9506) < 0.005
print(f"simulated detection rate at 2% = {detect:.4f}")

# Per hospital: 12 hospitals, same guarantee for each
per_h_total = 12 * n
assert per_h_total == 1_788 and round(per_h_total / notes * 100, 2) == 22.35
print(f"same guarantee per hospital: {per_h_total} notes a day = {per_h_total/notes:.2%} of notes")
print(f"pooled sample gives {n/12:.1f} notes per hospital on average")
assert round(n / 12, 1) == 12.4
# Rotation alternative: each hospital gets the full 149 on one day of every 12-day cycle (invented schedule)
print(f"rotation: one hospital per day gets {n}; each hospital audited every 12 days")
```

**Output (my run):**
```text
smallest n=149, share of the day's notes=1.86%, detection prob at n: 0.9507 (n-1: 0.9497)
  true rate 0.5%: P(at least one unsupported note in sample) = 0.526
  true rate 1.0%: P(at least one unsupported note in sample) = 0.776
  true rate 2.0%: P(at least one unsupported note in sample) = 0.951
  true rate 3.0%: P(at least one unsupported note in sample) = 0.989
zero found in 149: upper 95% bound on the rate = 1.99%
simulated detection rate at 2% = 0.9504
same guarantee per hospital: 1788 notes a day = 22.35% of notes
pooled sample gives 12.4 notes per hospital on average
rotation: one hospital per day gets 149; each hospital audited every 12 days
```

**Follow-ups:**
- What do you do on the first unsupported note found? Review it, classify severity, check for a pattern (hospital, prompt, note type); one hit at a 2% rate is expected about twice per 100, so escalate on severity or a repeated pattern, not on a single mild case.
- How do you estimate the actual rate, not just trip on 2%? A larger weekly pooled sample with an interval: 1,000 notes at a 2% rate gives about plus or minus 0.9 points.
- Could an LLM do the audit? As a first-pass filter that picks notes for human review, yes, but humans must label the random sample, because an LLM judge shares blind spots with the summariser (see Book 6 Part 3, the question on one LLM labelling and judging).

**Common mistakes:** Calling the audit a 95% confidence that the rate is below 2% without the zero-found condition. Forgetting 149 is a minimum for a single pooled rate. Ignoring per-hospital differences. Assuming notes are independent. Treating audit rate as true rate when auditors miss errors. Stating legal rules as facts.

