# Book 6 — Part 8: MLOps Incidents (Pipeline Failures, Rollback, Drift)

**Topic:** Scenario-based "something broke in the ML platform; what do you do" questions for ML Engineer, MLOps and Data Scientist loops: a training pipeline silently producing a worse model, bad deploys and rollback criteria, training-serving skew and feature-store incidents, late or failing data pipelines and backfills, upstream schema and unit changes, model-registry mix-ups, canary, shadow and blue/green problems, drift alerts that fire constantly or never, alert fatigue, GPU cost and autoscaling incidents, retraining loops gone wrong, on-call response, blameless postmortems, CI/CD and reproducibility failures, secrets leaks, serving outages and fallbacks, double-running batch jobs and idempotency, monitoring gaps, error budgets, blast radius and LLM-serving incidents.

**Target:** 45  |  **Actual:** 45 (⭐⭐⭐ 15, ⭐⭐ 20, ⭐ 10)  |  **Date:** 2026-10-31  |  **Status:** Complete (answers merged, checked, reviewed)

**Scope note:** this part is the incident, on-call and judgement angle, with numbers where an error budget, a detection delay, a rollback threshold, a backlog or a cost can be computed. MLOps tooling (CI/CD, containers, versioning, serving, monitoring tools) belongs to Book 4, model degradation in general to Book 6 Part 2, data quality gates to Book 6 Part 3 and GenAI quality and cost to Book 6 Part 7; Wave B answers should cross-reference those only by checked headings. All numbers in the prompts are invented illustrative numbers, not data from any company, and costs are in one unnamed currency unit. Every percentage names its base and says relative or absolute where it matters, rates are labelled as measured samples where it matters, and every arithmetic claim is checked in scratch/B6P08_wavea/qs.py. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part08_sources.md). Searches returned MLOps interview-prep pages, feature-store and skew pages, data-pipeline blogs, alerting and drift-monitor pages, LLM-resilience pages, registry and rollback runbooks and leakage papers. None tied a scenario to a verified employer round, and none located a public ML incident postmortem, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page for the exact framing. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

### Q1 ⭐⭐⭐ 🟢 A nightly retrain job finished green, but the new model scores an AUC of 0.771 on the fixed 20,000-row holdout against 0.812 for the production model, an absolute drop of 0.041. The job read 4,200,000 rows against a usual 5,000,000, which is 16% fewer relative to the usual count, and the deploy step is automatic whenever the job succeeds. What do you do tonight, and which gates would have stopped this?
**Asked at:** MLOps interview guides (startup.jobs, Hyring, kore1, refresh.cv, wecreateproblems and Yardstick pages list rollback, canary versus blue/green versus shadow, and 'tell me about an urgent production incident' prompts, and one 2026 guide says the strongest questions test custody of a live model); practitioner and prep-site material rather than a confirmed employer round; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** I would first check whether the bad model is already serving, roll back to yesterday's version if it is, then find which slice of data went missing, because a green job with 16% fewer rows and a 0.041 AUC drop is a pipeline failure, not a model result.

**Clarifying questions:**
- Did the automatic deploy already push the new model to live traffic, and at what share? It decides whether tonight is a rollback or only a block.
- Is the 20,000-row holdout truly fixed and frozen, and how many positives does it hold? It tells me how much to trust 0.041 (my run assumes 10% positives).
- What is the last known good version and can I switch to it in one command? Rollback must be rehearsed, not invented.
- What dropped the 800,000 rows: a late partition, a join, a filter, a schema change? Random loss and slice loss behave very differently.
- Who consumes the scores, and is there a cost to a wrong score in the next few hours? It sets how loud the escalation is.

**Approach:**
1. First 15 minutes. Stop the line: pause the deploy job and the next scheduled retrain. Check the serving version and traffic share. If the new model is live, roll back to the last good version now (the decision is already made by the rule below). Post one line in the incident channel: what, impact, who owns it.
2. Same night. Confirm the drop is real: the conservative z in my run is 4.9, so it is not holdout noise (assumes 10% positives). Find the missing 800,000 rows by comparing partition counts, segment counts and date ranges with the previous run. Do not rerun and hope.
3. First day. Fix the input (late or truncated partition), rerun the training, and let it pass the gates before it deploys. Write the timeline: when the job ran, when it deployed, when someone noticed (detection delay), when we rolled back.
4. Rollback and escalation criteria. Roll back without debate if a gate fails after a deploy, or live error or latency guardrails break. Escalate to the model owner and the data-platform owner if the cause is not found by the end of the first hour, and to the business owner if scores are being used for decisions in that time.
5. Next quarter. Put the gates in code: row-count gate (+/- 5% of the 7-day median, illustrative), holdout non-inferiority gate (new AUC not below production by more than 0.005, illustrative), segment-count gate, and a canary stage before 100% traffic. Make "deploy" a separate step that needs the gates to pass, not "job succeeded".
6. Blameless postmortem. The question is "why could a green job ship a worse model?", not "who wrote the job". The honest root cause is that success meant "the code ran", and nobody defined success as "the output is good". Each action item must be a gate or an alert, not "be careful".

**Metrics:**
- Absolute AUC drop = 0.812 - 0.771 = 0.041. Relative row shortfall = 800,000 / 5,000,000 = 16%. State which basis each percentage uses.
- Detection delay = time noticed minus time the bad model went live. Bad-model exposure = requests served by it (illustrative 50 requests a second for 7 hours is 1,260,000; with a 5% canary and a 10-minute auto rollback it is 1,500).
- Guardrails for the fixed pipeline: row count versus 7-day median, per-segment row share, null rate of key columns, holdout AUC versus production, calibration error.
- Time to rollback (minutes) and time to root cause are the two numbers I report after the incident.

**Risks:**
- Rolling back to an old model that expects an old feature schema. Check that the last good model still matches the current feature pipeline.
- Treating 16% as "just less data". My simulation shows random 16% loss moved AUC by under 0.005, while loss of a whole slice (about 16% of rows) moved it much more. The size of the loss is not the point, the shape is.
- A single holdout can hide a segment collapse. Add per-segment AUC.
- Sample versus projection: the 20,000-row holdout is a sample; the exposure numbers are invented traffic, not measured.

**What the interviewer scores:**
- Strong: protects users first (rollback), then investigates; separates "job succeeded" from "model is good"; names gates with numbers; proposes a canary. Weak: retrains again and hopes, or blames the author.
- Strong: asks which rows went missing. Weak: says "16% less data explains the drop".
- Strong: gives a first-15-minutes, first-day and next-quarter order. Weak: only "add monitoring".
- Strong: uses blameless language and concrete action items. Weak: "we will be more careful".

**Example:** Illustrative numbers. Last night: 4,200,000 rows, AUC 0.771. Normal: 5,000,000 rows, AUC 0.812. Weak answer: "The job is green and only 16% of the rows are missing, so I would let it run and watch the dashboards tomorrow." Strong answer: "I would not let it serve. The row gap fails a 5% row-count gate and the AUC drop of 0.041 fails a 0.005 non-inferiority margin, so I roll back now, find which partition is missing, and rerun only after both gates pass. Then I make deploy depend on the gates, not on the job's exit code."

**Code:**
```python
# Q1: green job, worse model. All numbers invented / illustrative.
import math
import numpy as np

# 1) the prompt's numbers
auc_prod, auc_new = 0.812, 0.771
drop = round(auc_prod - auc_new, 3)
rows_usual, rows_read = 5_000_000, 4_200_000
missing = rows_usual - rows_read
assert drop == 0.041 and missing == 800_000 and missing / rows_usual == 0.16

# 2) is a 0.041 AUC drop on 20,000 holdout rows more than noise?
# Hanley-McNeil standard error of one AUC; ASSUMPTION: 10% positives (2,000 pos, 18,000 neg).
def hm_se(a, n_pos, n_neg):
    q1, q2 = a / (2 - a), 2 * a * a / (1 + a)
    v = (a*(1-a) + (n_pos-1)*(q1-a*a) + (n_neg-1)*(q2-a*a)) / (n_pos*n_neg)
    return math.sqrt(v)
se = hm_se(0.812, 2000, 18000)
z_conservative = drop / (math.sqrt(2) * se)   # ignores that both models score the SAME rows (paired), so it is conservative
print(f"HM SE of one AUC = {se:.4f}; conservative z for the drop = {z_conservative:.1f}")
assert z_conservative > 4          # a real drop, not holdout noise (under the 10% positives assumption)

# 3) gates, written as code (thresholds are illustrative policy, not a standard)
def gates(rows, usual, auc_new, auc_prod, row_tol=0.05, auc_margin=0.005):
    fails = []
    if abs(rows - usual) / usual > row_tol: fails.append("row_count")
    if auc_new < auc_prod - auc_margin: fails.append("auc_noninferiority")
    return fails
f = gates(rows_read, rows_usual, auc_new, auc_prod)
print("gates failed:", f)
assert f == ["row_count", "auc_noninferiority"]
assert gates(4_900_000, rows_usual, 0.810, auc_prod) == []     # a normal night passes both

# 4) exposure: how many requests the worse model serves (invented traffic 50 req/s)
rps = 50
auto_deploy_noticed_after_h = 7                      # deploy 02:00, human notices 09:00
exposed = rps * auto_deploy_noticed_after_h * 3600
canary_exposed = int(rps * 0.05 * 10 * 60)           # 5% canary, auto rollback after 10 min
print("requests on bad model: no gate =", exposed, "| 5% canary + 10-min auto rollback =", canary_exposed)
assert exposed == 1_260_000 and canary_exposed == 1_500

# 5) does "16% fewer rows" alone explain it? Simulation, seeded. Logistic model by Newton steps.
rng = np.random.default_rng(6)
K, n = 25, 250_000                                    # 25 segments of ~4% each
seg = rng.integers(0, K, n)
base = rng.normal(0, 1.0, K)
X = rng.normal(size=(n, 4))
logit = base[seg] + X @ np.array([0.8, -0.5, 0.3, 0.2]) - 1.5
y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(float)
def design(seg, X): return np.hstack([np.eye(K)[seg], X])
def fit(D, y, it=12):
    w = np.zeros(D.shape[1])
    for _ in range(it):
        p = 1 / (1 + np.exp(-D @ w)); g = D.T @ (p - y) + 1e-3 * w
        H = (D * (p * (1 - p))[:, None]).T @ D + 1e-3 * np.eye(D.shape[1])
        w -= np.linalg.solve(H, g)
    return w
def auc(s, y):
    r = s.argsort().argsort() + 1; n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
hold = np.arange(n) >= 230_000                         # last 20,000 rows are the holdout
tr = ~hold
Dh = design(seg[hold], X[hold])
auc_full = auc(Dh @ fit(design(seg[tr], X[tr]), y[tr]), y[hold])
keep_rand = tr & (rng.random(n) > 0.16)                # drop 16% at random
auc_rand = auc(Dh @ fit(design(seg[keep_rand], X[keep_rand]), y[keep_rand]), y[hold])
gone = np.argsort(-np.abs(base))[:4]                   # drop 4 segments (the 4 most extreme): ~16% of rows, not random
keep_seg = tr & ~np.isin(seg, gone)
auc_seg = auc(Dh @ fit(design(seg[keep_seg], X[keep_seg]), y[keep_seg]), y[hold])
lost = 1 - keep_seg.sum() / tr.sum()
print(f"AUC full={auc_full:.3f} | 16% random rows dropped={auc_rand:.3f} | 4 segments ({lost:.0%} of rows) dropped={auc_seg:.3f}")
assert auc_full - auc_rand < 0.005                     # random loss barely matters
assert auc_full - auc_seg > 5 * (auc_full - auc_rand)  # a missing slice hurts far more
print("lesson: the row-count gap points to a missing slice, so find WHICH slice is missing")
```

**Output (my run):**
```text
HM SE of one AUC = 0.0060; conservative z for the drop = 4.9
gates failed: ['row_count', 'auc_noninferiority']
requests on bad model: no gate = 1260000 | 5% canary + 10-min auto rollback = 1500
AUC full=0.801 | 16% random rows dropped=0.801 | 4 segments (16% of rows) dropped=0.730
lesson: the row-count gap points to a missing slice, so find WHICH slice is missing
```

**Follow-ups:**
- Why not just rerun the job? A rerun of the same broken input gives the same model. Fix the input first, and keep the rollback in place meanwhile.
- Is 0.005 the right margin? It is a policy choice; set it from the holdout noise (SE about 0.006 here) and the business cost of a small drop. If the margin is below the noise, the gate will flap, so use a margin or a bootstrap interval.
- Book 4 link: see "Rolling updates, rollbacks and canary releases for a new model version on Kubernetes" in Book4_MLOps_Part03.md for the rollout mechanics.

**Common mistakes:** Treating the green status as proof of quality. Talking only about the model and not the deploy gate. Saying "16% fewer rows explains 0.041" without finding the slice. Naming a person in the postmortem. No numeric rollback rule.

### Q2 ⭐⭐⭐ 🟢 A new model went to 100% of traffic 40 minutes ago. The 95th-percentile latency rose from 180 ms to 240 ms, which is 33% higher relative to 180 ms, and conversion over the 12,000 sessions since release is 4.2% against 4.3% for the 12,000 sessions in the same weekday hour last week (a 0.1 point absolute gap, measured samples). Do you roll back now, and what pre-agreed rollback rule would have made this a non-debate?
**Asked at:** MLOps interview guides (startup.jobs, Hyring, kore1, refresh.cv, wecreateproblems and Yardstick pages list rollback, canary versus blue/green versus shadow, and 'tell me about an urgent production incident' prompts, and one 2026 guide says the strongest questions test custody of a live model); practitioner and prep-site material rather than a confirmed employer round; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** Not on the conversion number, because 4.2% versus 4.3% on 12,000 sessions each is noise (z about -0.4); the 33% latency rise is real, so I hold, check it against the latency objective, and roll back if it crosses the pre-agreed line.

**Clarifying questions:**
- What is our latency objective and the timeout of the callers? 240 ms may be fine or may be breaking a 250 ms timeout.
- Is the 12,000 sessions in the last 40 minutes a fair comparison with the same hour last week? It is not a concurrent control, so traffic mix, promotions and weekday effects leak in.
- Are errors, timeouts and fallbacks changing too? Slow responses that time out show up as lost conversion later.
- Is there a cheap way back (previous version warm, one command)? If rollback costs 2 minutes, I am more willing to roll back on doubt.
- What does the model owner say changed (larger model, extra feature fetch)? It tells me whether latency is fixable by a quick config change.

**Approach:**
1. First 15 minutes (already past 40 minutes, so now). Look at p95, p99, error rate, timeouts and CPU or GPU saturation by pod. Latency is a direct measurement and moves fast; conversion is a slow, noisy outcome.
2. Decide against the pre-agreed rule (see Metrics). In my illustrative rule, 240 ms is 1.33 times baseline: above the 1.2 times "hold and page" line, below the 1.5 times "roll back after 10 minutes" line. So: hold, freeze other changes, page the model owner, and set a 30-minute decision time.
3. Do not use the conversion gap to justify either action. The 95% interval for the difference is about -0.6 to +0.4 points, and this sample could only detect a drop of about 0.73 points (17% relative). A 0.3-point real loss would be invisible here.
4. Rollback and escalation criteria: roll back at once if errors exceed 1%, or p95 stays above 1.5 times baseline for 10 minutes, or the callers' timeouts start firing. Escalate to the service owner if latency keeps climbing at the 30-minute mark.
5. First day. Keep a 5% share on the old model so there is a concurrent control for conversion; read conversion at 24 to 48 hours with a planned sample size, not at 40 minutes.
6. Next quarter. Ship through a canary stage (5% for a set time) with automatic rollback on latency and error guardrails, and make the conversion test a planned experiment, not a rollback trigger.
7. Blameless postmortem. The release went to 100% with no pre-agreed rule, so the debate happened under pressure. The action is the rule and the canary, not blame for the release owner.

**Metrics:**
- Latency: p95 in ms over a 5-minute window, ratio to baseline (240 / 180 = 1.33, i.e. +33% relative to 180 ms, +60 ms absolute).
- Conversion = converting sessions / sessions, 504 / 12,000 = 4.2% versus 516 / 12,000 = 4.3%. Gap -0.1 points absolute, -12 conversions in the sample.
- Guardrails: error rate, timeout rate, fallback rate, saturation. Minutes over threshold, not a single spike.
- Test statistic: pooled two-proportion z, here -0.38, p about 0.70 (my run). Sample figures, not a projection to all traffic.

**Risks:**
- Calling the latency rise "fine" because conversion did not move; a 33% slower tail often hurts later, in timeouts under peak load.
- Comparing with last week's same hour: seasonal and promo effects can swamp a 0.1 point gap either way.
- Rolling back on noise teaches the team to distrust the release process; not rolling back on a real fault costs users.
- Peeking: reading conversion every few minutes inflates false alarms.

**What the interviewer scores:**
- Strong: separates a direct, fast signal (latency) from a slow noisy one (conversion) and computes the noise. Weak: "conversion fell, roll back" or "it is only 0.1 points, ignore all of it".
- Strong: asks about the objective and timeout. Weak: picks a number from nowhere.
- Strong: writes the rule with thresholds and a decision time. Weak: "we would monitor closely".
- Strong: says a concurrent holdback beats last week's hour. Weak: accepts the comparison as is.

**Example:** Illustrative numbers. p95 is 240 ms, the baseline 180 ms, rule: roll back if p95 above 270 ms for 10 minutes. Weak answer: "Conversion is down 0.1 points and latency is up a third, so I would roll back to be safe, and if it turns out fine we lose nothing." Strong answer: "Conversion is noise: z is about -0.4 and we could only see a 0.7 point drop. Latency is real but under our 270 ms line, so I hold, page the owner and decide in 30 minutes. If p95 passes 270 for 10 minutes, or errors pass 1%, I roll back without another meeting."

**Code:**
```python
# Q2: roll back now? Illustrative numbers; seeded.
import math
import numpy as np
from scipy import stats

# prompt arithmetic
assert round((240 - 180) / 180, 3) == 0.333                 # 33% relative to 180 ms
n = 12_000
x_new, x_old = round(0.042 * n), round(0.043 * n)           # 504 and 516 conversions
assert (x_new, x_old) == (504, 516) and x_old - x_new == 12

# two-proportion z test (pooled), two-sided
p_pool = (x_new + x_old) / (2 * n)
se_pool = math.sqrt(p_pool * (1 - p_pool) * 2 / n)
z = (x_new / n - x_old / n) / se_pool
p_val = 2 * stats.norm.sf(abs(z))
print(f"conversion gap -0.1 pt: z={z:.2f}, p={p_val:.2f}")
assert abs(z) < 1 and p_val > 0.3                            # indistinguishable from noise

# 95% CI of the difference (unpooled)
se = math.sqrt(0.042*0.958/n + 0.043*0.957/n)
lo, hi = (0.042 - 0.043) - 1.96*se, (0.042 - 0.043) + 1.96*se
print(f"95% CI of difference: [{lo*100:.2f}, {hi*100:.2f}] points")
assert lo < -0.004 and hi > 0.002                            # about +/- 0.5 points: a 0.4-point loss is still possible

# smallest drop this sample could detect (80% power, alpha 0.05, two-sided)
mde = (1.96 + 0.8416) * se
print(f"smallest detectable drop at 12,000 vs 12,000 = {mde*100:.2f} points ({mde/0.043:.0%} relative)")
assert 0.006 < mde < 0.008

# is the latency rise real? bootstrap CI of p95 with simulated latencies (lognormal, sigma 0.4)
rng = np.random.default_rng(8)
sigma = 0.4
def sample(p95, m): return rng.lognormal(math.log(p95) - 1.645*sigma, sigma, m)
old, new = sample(180, n), sample(240, n)
def boot_p95(a, B=300): return np.percentile([np.percentile(rng.choice(a, len(a)), 95) for _ in range(B)], [2.5, 97.5])
print("p95 old CI", boot_p95(old).round(1), "| p95 new CI", boot_p95(new).round(1))
assert boot_p95(old)[1] < boot_p95(new)[0]                   # intervals do not overlap: latency rise is real

# the pre-agreed rule, as code (thresholds illustrative)
def decide(p95_ms, base_ms, minutes_over, err_rate):
    if err_rate > 0.01: return "ROLLBACK (errors)"
    if p95_ms > 1.5 * base_ms and minutes_over >= 10: return "ROLLBACK (latency)"
    if p95_ms > 1.2 * base_ms: return "HOLD (freeze other changes), page owner, decide in 30 min"
    return "CONTINUE"
print(decide(240, 180, 40, 0.001))   # 240 is 1.33x: above 1.2x, below 1.5x
print(decide(280, 180, 12, 0.001))   # 280 is 1.56x for 12 min
assert decide(240, 180, 40, 0.001).startswith("HOLD") and decide(280, 180, 12, 0.001).startswith("ROLLBACK")

# follow-up claim: per-arm sample to detect a 0.3-point drop from 4.3% (80% power, alpha 0.05)
n_need = 2 * (1.96 + 0.8416)**2 * 0.043 * 0.957 / 0.003**2
print("per-arm sessions to detect 0.3 points:", round(n_need))
assert 60_000 < n_need < 80_000
```

**Output (my run):**
```text
conversion gap -0.1 pt: z=-0.38, p=0.70
95% CI of difference: [-0.61, 0.41] points
smallest detectable drop at 12,000 vs 12,000 = 0.73 points (17% relative)
p95 old CI [176.5 181.5] | p95 new CI [235.7 243.1]
HOLD (freeze other changes), page owner, decide in 30 min
ROLLBACK (latency)
per-arm sessions to detect 0.3 points: 71776
```

**Follow-ups:**
- What would change your mind about conversion? A concurrent holdback with a planned sample size; at a 4.3% base, detecting a 0.3 point drop takes about 72,000 sessions per arm in my run.
- Why 1.5 times and not 1.2 times to roll back? The first is a hard stop, the second only starts a clock. Both are policy choices; set them from the objective and rehearse the rollback.
- Book 4 link: "Rolling updates, rollbacks and canary releases for a new model version on Kubernetes" in Book4_MLOps_Part03.md.

**Common mistakes:** Treating a 0.1 point gap as a signal or as proof of safety. Ignoring the latency number. Comparing against a non-concurrent baseline without saying so. Having no rollback rule written before the release. Blaming the person who clicked deploy.

### Q3 ⭐⭐⭐ 🟢 At 02:10 you are paged because the fraud model's approval rate in the latest 5-minute window fell from 92% to 71% (absolute, of about 2,000 requests per window, so roughly 420 fewer approvals than usual). Nothing was deployed today according to the release calendar. What do you do in the first 15 minutes, in order, and when do you wake someone else?
**Asked at:** MLOps interview guides (startup.jobs, Hyring, kore1, refresh.cv, wecreateproblems and Yardstick pages list rollback, canary versus blue/green versus shadow, and 'tell me about an urgent production incident' prompts, and one 2026 guide says the strongest questions test custody of a live model); practitioner and prep-site material rather than a confirmed employer round; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** I confirm the drop is real, look for what changed that the release calendar does not list (config, features, upstream data, traffic), break the drop down by segment, mitigate by switching to the last good path if the cause is data, and wake the owner at minute 10 if I still have no cause.

**Clarifying questions:**
- What does a lower approval rate cost us: lost sales, angry customers, or is it a fraud wave that is working as intended? It decides whether tonight is a rollback or a defence.
- What is the normal range of this metric at 02:00 on this weekday? A 5-minute window of 2,000 has a standard error of about 0.6 points, so the drop is about 35 standard errors, but the night-time mix may differ.
- What sits outside the release calendar: feature pipelines, threshold config, feature flags, upstream data feeds, partner outages? "Nothing was deployed" usually means no code deploy.
- Is there a rules-only or last-good-model fallback, and who may switch it at night? Mitigation must be pre-approved.
- Who is the second on-call, and what are the paging rules for a customer-impacting drop?

**Approach:**
1. Minutes 0 to 2. Acknowledge the page, open an incident channel, write the first line: what, since when, who is on it. Roles: I investigate; a second person (when called) communicates.
2. Minutes 2 to 5. Is it real? Check raw request counts, the metric pipeline's own freshness, and whether the same drop shows in logs. A broken metric job looks exactly like a model failure.
3. Minutes 5 to 8. What changed anyway: model version actually served, config and threshold values, feature null rates and freshness, upstream feed status, traffic source mix. Check the release calendar last, not first.
4. Minutes 8 to 12. Break the 420 missing approvals down by segment (device, merchant, country, feature null or not). In my run all 420 sit in one segment (requests where device_score is null), whose approval rate went from 92% to 39.5%. One segment means one broken input, not a changed population.
5. Minutes 12 to 15. Mitigate. If a feature is broken, switch that path to the last good model or to rules, using the pre-approved fallback. Do not loosen the fraud threshold blindly; if the cause is unknown and fraud signals are also up, this may be a real attack and the approvals are correct.
6. When to wake someone. At minute 10 if approval is still under 80% and I have no cause: wake the model owner and the data owner. Wake the business owner if estimated customer harm passes a set line (here 5,000 wrongly declined, illustrative). Wake the owner of a broken dependency as soon as I find it and the drop is still falling.
7. First day. Restore the right input, confirm approval returns to the normal band, list who was declined during the incident and decide on outreach or a manual review, write the timeline with detection delay (here 10 minutes).
8. Next quarter. Alert on feature null rate and freshness, not only on the output rate; add a segment breakdown to the alert page; rehearse the fallback; add the "non-deploy changes" (config, feature flags, pipelines) to the change calendar.
9. Blameless postmortem. Questions: why did a feature outage reach the score silently? Why did the alert fire only on the output? What made the decision at 02:10 hard? Action items are alerts, fallbacks and runbooks, not names.

**Metrics:**
- Approval rate = approved requests / total requests per 5-minute window. Drop = 92% - 71% = 21 points absolute (relative drop is 21 / 92 = 23%); 420 fewer approvals out of 2,000.
- Detection delay = 10 minutes under a "two consecutive 5-minute windows below 85%" rule (illustrative) when the drop starts at 02:00.
- Exposure: 420 fewer approvals per window, 1,260 in the first 15 minutes after the page, 5,040 an hour. These are fewer approvals, not proven wrong declines; the wrong-decline count needs labels or a review sample.
- Guardrails: fraud loss rate, chargeback rate, manual-review queue size, feature null rates by feature.

**Risks:**
- Treating a real fraud wave as a bug and loosening the threshold, which lets fraud through.
- Waking everyone at minute 2 with no facts, or no one at all; both burn trust. Use the minute-10 rule.
- A mitigation with a hidden cost: the fallback model may have a worse fraud catch rate. Say the trade-off aloud.
- Metric pipeline bug mistaken for a model bug, or the reverse.

**What the interviewer scores:**
- Strong: an ordered first-15-minutes list with a reason for each step; confirms the signal before acting. Weak: "check the logs and the model".
- Strong: knows "no deploy" does not mean "no change". Weak: stops at the release calendar.
- Strong: names a wake-up rule with a time and a threshold. Weak: "escalate if serious".
- Strong: protects users with a fallback, then diagnoses. Weak: diagnoses for an hour with customers declined.
- Strong: blameless action items. Weak: "tell the team to be careful".

**Example:** Illustrative numbers. Weak answer: "I would restart the model service and see if it recovers, and tell my manager in the morning." Strong answer: "First I confirm the drop is in raw logs, not the metric job. Then I check config, feature freshness and upstream feeds. A segment cut shows all 420 missing approvals come from requests with a null device score, so a feature feed is broken. I switch that path to the last good fallback, and since I had no cause at minute 10 I already woke the data owner."

**Code:**
```python
# Q3: 02:10 page, fraud approval rate 92% -> 71%. Illustrative numbers.
import math

n, base, now = 2000, 0.92, 0.71
fewer = round(n * base) - round(n * now)
assert round(n * base) == 1840 and round(n * now) == 1420 and fewer == 420

# noise check: how big is normal window-to-window wobble?
se = math.sqrt(base * (1 - base) / n)
z = (base - now) / se
print(f"binomial SE of a {n}-request window = {se*100:.2f} points; the drop is {z:.0f} SE, so this is NOT sampling noise")
assert 0.5 < se * 100 < 0.7 and z > 30

# detection delay: rule = two consecutive 5-minute windows below 85% (illustrative); drop starts 02:00
start_min, window, needed = 0, 5, 2
detect_min = start_min + window * needed        # first time two full bad windows exist
print("detection delay (minutes):", detect_min, "-> page at 02:%02d" % detect_min)
assert detect_min == 10

# exposure while we work: 5-min windows of 420 fewer approvals
per_window = fewer
first_15_after_page = 3 * per_window
per_hour = 12 * per_window
print("fewer approvals: first 15 min after page =", first_15_after_page, "| per hour =", per_hour)
assert first_15_after_page == 1260 and per_hour == 5040

# triage step 3: break the drop down by segment (invented counts). Find where it lives.
seg = {  # name: (requests, approvals_before, approvals_now)
    "device_score present": (1200, 1104, 1104),
    "device_score null":    (800,   736,  316),
}
assert sum(v[0] for v in seg.values()) == 2000 and sum(v[2] for v in seg.values()) == 1420
drop_by = {k: v[1] - v[2] for k, v in seg.items()}
share = drop_by["device_score null"] / sum(drop_by.values())
print("drop by segment:", drop_by, "| share in null-segment =", share)
assert drop_by["device_score null"] == 420 and share == 1.0
print("null segment approval now:", round(316 / 800, 3), "(was", 736 / 800, ")")
assert round(316 / 800, 3) == 0.395

# escalation rule as code (thresholds illustrative)
def escalate(minutes_since_page, cause_found, approval_now, falling, wrong_declines_est):
    if approval_now < 0.80 and not cause_found and minutes_since_page >= 10: return "WAKE model owner + data owner"
    if wrong_declines_est > 5000: return "WAKE business owner (customer harm)"
    if cause_found and falling: return "WAKE owner of the broken dependency"
    return "continue solo, update channel every 10 min"
print(escalate(10, False, 0.71, True, 1260))
print(escalate(5, False, 0.71, True, 600))
assert escalate(10, False, 0.71, True, 1260).startswith("WAKE model owner")
assert escalate(5, False, 0.71, True, 600).startswith("continue")
```

**Output (my run):**
```text
binomial SE of a 2000-request window = 0.61 points; the drop is 35 SE, so this is NOT sampling noise
detection delay (minutes): 10 -> page at 02:10
fewer approvals: first 15 min after page = 1260 | per hour = 5040
drop by segment: {'device_score present': 0, 'device_score null': 420} | share in null-segment = 1.0
null segment approval now: 0.395 (was 0.92 )
WAKE model owner + data owner
continue solo, update channel every 10 min
```

**Follow-ups:**
- What if the segment cut shows nothing concentrated? Then suspect a global cause: a threshold or config change, a model version mix-up, or a real attack across segments; widen the search and wake the owner sooner.
- Should the on-call roll back the model? Only if the model version changed or the old version is known good with the current features. Otherwise the fallback is safer.
- Book 4 link: "Training-serving skew from the code side" in Book4_MLOps_Part01.md covers the feature mismatches that cause this pattern.

**Common mistakes:** Checking only the release calendar. Not confirming the metric is real. Loosening the threshold to make the graph look normal. Waking no one, or everyone. Writing "human error" as the root cause.

### Q4 ⭐⭐⭐ 🟢 A drift monitor runs a per-feature test on 40 features every hour at a 5% false-positive level, and the on-call engineer is paged several times a day, nearly every hour, without a real incident. Assuming independent features and no real change, compute the expected false alerts per day and the probability that at least one feature alerts in a given hour. What would you change so the page means something?
**Asked at:** Alerting and drift-monitor material (an ICLR 2026 listing on false-alarm rates of drift detectors, an MLflow alerts playbook, GeoSurge, LeadDev and Rootly pages on thresholds, monitoring debt and alert fatigue); research and practitioner pages rather than an interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** 40 features times 24 hourly checks is 960 tests a day, so at 5% I expect 48 false alerts a day, and the chance that at least one feature fires in any given hour is 1 - 0.95^40 = 87%; the monitor is built to cry wolf, so I change what pages a human, not just the threshold.

**Clarifying questions:**
- What does one alert page: one feature, or any feature? That sets whether you get 48 pages or about 21 paged hours a day.
- How many rows go into each hourly test? With millions of rows, even a trivial shift is "significant" at 5%.
- What real incidents did this monitor catch in the last year, and how late? It is the only way to price the cost of making it stricter.
- Are the features correlated? Independence is the prompt's assumption; real features move together.
- Who reads the page, and what do they do with it? If nobody has an action, it is a dashboard, not a page.

**Approach:**
1. First hour. Compute the arithmetic above to show the owner that the pages are mathematics, not bad luck: 960 checks, 48 expected false alerts, 87% of hours with at least one.
2. First day. Mute the paging route for this monitor (keep it in a daily report) so on-call is protected, and write down that the mute is temporary with an owner and a date. Do not delete the monitor.
3. First week. Redesign what pages: (a) control the family-wise error with a Bonferroni level of 0.05 / 40 = 0.00125 per feature, which gives 4.9% per hour; (b) require persistence, for example three consecutive hours, which together with (a) gives about 0.012% per hour in my run; (c) add an effect-size floor such as PSI above 0.2 (a common rule of thumb, editor knowledge, not tested here) or a standardised shift above a set size so huge samples do not flag trivia; (d) page on the model-facing signal (score distribution, null rate, output rate) and ticket the per-feature drift.
4. Cost of strictness, honestly. At 2,000 rows per test and a real 0.1 SD shift, per-feature power falls from 0.885 at 5% to 0.474 at the Bonferroni level (my run). Stricter alerts catch big shifts quickly and small ones slowly. That is the right trade for a page and the wrong one for a weekly review, so keep both channels.
5. Next quarter. Tier the alerts: page, ticket, report. Review each alert's precision monthly (alerts that led to action divided by alerts fired) and retire the ones below a set bar. Replay past incidents to check the new rules would still have fired.
6. Rollback or escalation criteria. If after the change a real incident is missed (a labelled AUC drop with no page), loosen the persistence window first, not the level. Escalate to the model owner if two missed incidents happen in a quarter.
7. Blameless postmortem. The root cause is a design that never priced false alarms, so a person ended up acting as the filter. Action items: false-alarm budget per week, owner for the alert, quarterly precision review.

**Metrics:**
- False alerts per day = tests per day x level = (40 x 24) x 0.05 = 48. P(at least one alert in an hour) = 1 - (1 - 0.05)^40 = 0.8715; expected paged hours per day = 24 x 0.8715 = 20.9.
- Alert precision = alerts with a real incident or action / alerts fired. Alert recall = real incidents that fired / real incidents (from labelled replays).
- Detection delay on replayed incidents, and pages per on-call week as a guardrail (set a budget, for example under 5).
- Guardrail on the redesign: no real incident in the replay set may go unalerted.

**Risks:**
- Bonferroni is conservative and loses power on small shifts (shown: 0.474 power on a 0.1 SD shift).
- Persistence adds delay: three hourly windows means at least a 3-hour detection delay for a slow shift.
- Independence is an assumption. With correlation 0.7 across features my simulation gave 37% of hours with an alert instead of 87%, still far too many to page on.
- Sample versus projection: 48 a day is an expectation under "no real change"; a real day has a different count.

**What the interviewer scores:**
- Strong: gets 960, 48 and 87% right and does the second step. Weak: "5% means 5% of alerts are false", or gets only one number.
- Strong: lists several fixes with their price (power, delay). Weak: "raise the threshold".
- Strong: separates paging from reporting. Weak: one channel for everything.
- Strong: blameless, with a precision review. Weak: "ignore it until it is quiet".

**Example:** Illustrative numbers. Weak answer: "A 5% test is wrong 5% of the time, so with 40 features about two will be wrong sometimes. I would raise the alpha to 1%." Strong answer: "We run 960 tests a day, so 48 false alerts are expected, and at least one feature fires in 87% of hours. I would test at 0.05 / 40, require three consecutive hours and an effect-size floor, page only on the score and null-rate signals, and send per-feature drift to a daily report. I would replay last year's incidents to confirm we still catch them, and accept that tiny shifts take longer to show."

**Code:**
```python
# Q4: 40 features x hourly test at 5% -> false alert arithmetic. Illustrative.
import numpy as np
from scipy import stats

F, alpha, hours = 40, 0.05, 24
checks = F * hours
exp_alerts = checks * alpha
p_any_hour = 1 - (1 - alpha) ** F
hours_with_alert = hours * p_any_hour
print(f"checks/day={checks}, expected false feature alerts/day={exp_alerts}")
print(f"P(at least one alert in an hour)={p_any_hour:.4f}; expected hours per day with a page={hours_with_alert:.1f}")
assert checks == 960 and exp_alerts == 48 and 0.871 < p_any_hour < 0.872 and 20.8 < hours_with_alert < 21.0

# verify by simulation (seeded): p-values are uniform when nothing changed
rng = np.random.default_rng(4)
sim = rng.random((100_000, F)) < alpha
print("simulated P(any in hour)=", round(sim.any(axis=1).mean(), 3), "| mean alerts per hour =", round(sim.sum(axis=1).mean(), 3))
assert abs(sim.any(axis=1).mean() - p_any_hour) < 0.005 and abs(sim.sum(axis=1).mean() - 2.0) < 0.02

# fixes, each priced by the same false-alarm arithmetic
bonf = alpha / F
p_bonf = 1 - (1 - bonf) ** F
print(f"Bonferroni per-feature level={bonf}: P(any/hour)={p_bonf:.4f}, hours/day={hours*p_bonf:.2f}")
assert abs(p_bonf - 0.0488) < 0.0005

p_k5 = stats.binom.sf(4, F, alpha)           # P(at least 5 of 40 features alert in one hour)
print(f"page only if >=5 of 40 alert: P(false page/hour)={p_k5:.4f}")
assert 0.047 < p_k5 < 0.049

p_persist3 = p_bonf ** 3                      # Bonferroni AND three consecutive hours (hours independent under no change)
print(f"Bonferroni + 3 consecutive hours: P(false page/hour)={p_persist3:.6f}; per day={hours*p_persist3:.5f}")
assert hours * p_persist3 < 0.003
p_plain3 = p_any_hour ** 3
print(f"plain 5% + 3 consecutive hours: P(false page/hour)={p_plain3:.3f}  (still ~{hours*p_plain3:.0f} a day)")
assert hours * p_plain3 > 15

# the cost of strictness: power on a real shift of 0.1 SD at n=2000 per window, per-feature z test
n, shift = 2000, 0.1
def power(a):
    zc = stats.norm.isf(a / 2); mu = shift * np.sqrt(n / 2)
    return stats.norm.sf(zc - mu) + stats.norm.cdf(-zc - mu)
print(f"per-feature power at 5%: {power(0.05):.3f}; at Bonferroni level {bonf}: {power(bonf):.3f}")
assert power(0.05) > 0.8 and 0.3 < power(bonf) < 0.6   # strictness costs power on small real shifts

# but huge samples flag trivial shifts: with n=2,000,000 a 0.003 SD shift is "significant" at 5%
n2, tiny = 2_000_000, 0.003
mu2 = tiny * np.sqrt(n2 / 2)
print(f"power to flag a 0.003 SD shift at n={n2}: {stats.norm.sf(1.96 - mu2):.2f} -> use an effect-size floor, not p alone")
assert stats.norm.sf(1.96 - mu2) > 0.5

# correlated features: does the independence assumption overstate false pages?
cov = 0.7 * np.ones((F, F)) + 0.3 * np.eye(F)
z = rng.multivariate_normal(np.zeros(F), cov, size=20_000)
pc = (np.abs(z) > 1.96).any(axis=1).mean()
print(f"with feature correlation 0.7: P(any/hour)={pc:.3f} (independence gave {p_any_hour:.3f})")
assert pc < p_any_hour
```

**Output (my run):**
```text
checks/day=960, expected false feature alerts/day=48.0
P(at least one alert in an hour)=0.8715; expected hours per day with a page=20.9
simulated P(any in hour)= 0.872 | mean alerts per hour = 2.004
Bonferroni per-feature level=0.00125: P(any/hour)=0.0488, hours/day=1.17
page only if >=5 of 40 alert: P(false page/hour)=0.0480
Bonferroni + 3 consecutive hours: P(false page/hour)=0.000116; per day=0.00279
plain 5% + 3 consecutive hours: P(false page/hour)=0.662  (still ~16 a day)
per-feature power at 5%: 0.885; at Bonferroni level 0.00125: 0.474
power to flag a 0.003 SD shift at n=2000000: 0.85 -> use an effect-size floor, not p alone
with feature correlation 0.7: P(any/hour)=0.375 (independence gave 0.871)
```

**Follow-ups:**
- Why not Benjamini-Hochberg? It controls the false discovery rate and is less strict than Bonferroni; it suits a ticket queue, but for a page I want a hard cap on false pages per day.
- What about daily instead of hourly checks? That cuts checks to 40 a day and 2 false alerts expected, but multiplies detection delay by up to 24.
- Book 4 link: "Training-serving skew from the code side" in Book4_MLOps_Part01.md separates drift from skew, which matters before you alert on either.

**Common mistakes:** Computing only 40 x 5% = 2 and forgetting the 24 hours. Saying "5% of alerts are false" (the level is per test, not per alert). Raising the threshold with no replay check. Deleting the monitor. Paging on every feature instead of the outcome.

### Q5 ⭐⭐⭐ 🟢 A model deploy passed every CI test, but the integration test used a mocked feature store, and in production the new model returned errors for 100% of requests for 12 minutes before an engineer rolled back, taking 6 further minutes to finish. At 600 requests per second, compute the failed requests in the first 12 minutes and name which tests and gates were missing. Which of them would you add first?
**Asked at:** MLOps interview guides (startup.jobs, Hyring, kore1, refresh.cv, wecreateproblems and Yardstick pages list rollback, canary versus blue/green versus shadow, and 'tell me about an urgent production incident' prompts, and one 2026 guide says the strongest questions test custody of a live model); practitioner and prep-site material rather than a confirmed employer round; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** 600 requests a second for 12 minutes is 432,000 failed requests, 648,000 if the errors lasted until the rollback finished; the gates missing were a test against the real feature store, a readiness smoke test and a canary with automatic rollback, and I would add the canary with automatic rollback first because it limits damage whatever the cause.

**Clarifying questions:**
- Did errors continue at 100% during the 6-minute rollback? If yes the total is 648,000; the prompt's question asks only for the first 12 minutes, so I state both.
- What did the mock hide: a missing feature view, a schema change, a permission, a timeout? It tells me which test would have caught it.
- Why did detection take 12 minutes: no alert, a slow alert, or nobody looking at 100% errors? Detection delay is half of the cost.
- What is our availability objective? It converts failed requests into budget burned.
- Can the deploy tooling roll back automatically, and why did it need 6 minutes?

**Approach:**
1. First 15 minutes of the incident (what a good responder does): treat 100% errors as an outage, roll back first and diagnose after, post one status line, keep the broken version available in staging for the postmortem.
2. Rollback criteria written before deploy: roll back automatically if the error rate exceeds 5% for 60 seconds on the canary, or latency passes the agreed line. Escalate to the platform owner if rollback itself does not complete in 5 minutes.
3. First day. Re-run the failed deploy in staging against the real (staging) feature store to reproduce; list the failed requests by caller so affected teams get a message; compute budget burned.
4. First week. Add, in this order of value: (a) a canary stage (5% of traffic) with automatic rollback on error rate; (b) a post-deploy smoke test that sends a handful of real requests through the real feature store before the pod is marked ready; (c) a contract test that checks every feature the model reads exists in the live feature view with the right type.
5. Which first and why. With a 5% canary and a 60-second automatic rollback, the same bug costs about 12,600 failed requests in my run, 98% fewer than 648,000 (assuming the canary share of traffic, and the same 6-minute rollback). The smoke test would have caught this one bug in seconds, but the canary also catches the next unknown one.
6. Next quarter. Replace mocks in integration tests with a staging store seeded from production-shaped data; run a rollback drill each quarter and measure time to complete; make rollback a one-command, minutes-long action.
7. Blameless postmortem. Why did CI say green when production was broken? Because the test double was always happy. Why 12 minutes to start the rollback? No automatic detection. Action items are gates and alerts with owners, not "review the mocks more carefully".

**Metrics:**
- Failed requests = requests per second x seconds of failure = 600 x 720 = 432,000 (first 12 minutes); 600 x 1,080 = 648,000 through the end of the rollback (upper bound).
- Time to detect, time to start rollback, time to finish rollback (here 12 minutes and 6 minutes).
- Error budget burned = failed requests / (monthly requests x allowed error rate). For an illustrative 99.9% objective at a constant 600 rps over 30 days, the budget is 1,555,200 requests and this incident burned 41.7% (my run).
- Guardrails: error rate, p95 latency, timeouts per version label.

**Risks:**
- The canary share is too small to see a rare error (a 1% error on 5% of 600 rps is 0.3 failed requests a second).
- A smoke test that uses synthetic keys can miss real-key failures.
- A mock-free integration test makes CI slower and flakier; keep it small and run it on release candidates.
- Automatic rollback can flap if thresholds are too tight; add a minimum sample count.
- The 648,000 figure is an upper bound that assumes 100% errors throughout; it is a projection from the prompt, not a measured count.

**What the interviewer scores:**
- Strong: both numbers (432,000 and the full-incident bound) with units shown. Weak: wrong arithmetic (600 x 12 = 7,200 is a common slip) or no second figure.
- Strong: names the missing gates by what they catch. Weak: "more testing".
- Strong: picks one to add first and justifies it by blast radius. Weak: lists ten and no priority.
- Strong: blameless root cause about the test double and the missing automatic rollback. Weak: blames the reviewer.

**Example:** Illustrative numbers. Weak answer: "We should write more unit tests for the new model and have another person review the deploy." Strong answer: "432,000 requests failed in the first 12 minutes, and 648,000 by the time the rollback finished, which is about 42% of a 99.9% monthly budget. The mock hid a missing feature view. First I add a 5% canary with automatic rollback at 5% errors for a minute; the same bug would then cost about 12,600 requests. Next a readiness smoke test on the real store, then a contract test of the feature list."

**Code:**
```python
# Q5: mocked feature store -> 12 minutes of 100% errors. Illustrative.
rps = 600
detect_to_rollback_start_s = 12 * 60          # errors from deploy until the engineer starts the rollback
rollback_s = 6 * 60                           # rollback takes 6 more minutes
failed_first_12 = rps * detect_to_rollback_start_s
assert failed_first_12 == 432_000
# upper bound: errors continue at 100% until the rollback finishes
failed_total_upper = rps * (detect_to_rollback_start_s + rollback_s)
assert failed_total_upper == 648_000 and 12 + 6 == 18
print("failed requests, first 12 min:", failed_first_12, "| through end of rollback (upper bound):", failed_total_upper)

# against an illustrative 99.9% monthly availability objective at constant 600 rps, 30 days
month_req = rps * 86_400 * 30
budget_req = month_req * 0.001
print("monthly requests:", month_req, "| error budget (0.1%):", int(budget_req))
assert month_req == 1_555_200_000 and int(budget_req) == 1_555_200
print("share of monthly budget burned:", round(failed_total_upper / budget_req, 3))
assert round(failed_total_upper / budget_req, 3) == 0.417

# what would a gate have cost? Canary 5% of traffic, auto rollback when error rate > 5% for 60 s,
# rollback takes 6 minutes but only the canary share is exposed
canary_share = 0.05
detect_s = 60
canary_failed = rps * canary_share * (detect_s + rollback_s)
print("canary exposure (failed requests):", int(canary_failed))
assert int(canary_failed) == 12_600
print("reduction vs no canary:", round(1 - canary_failed / failed_total_upper, 3))
assert round(1 - canary_failed / failed_total_upper, 3) == 0.981

# smoke test with a REAL (staging) feature store would have failed the first request
def feature_store_mock(key): return {"f1": 0.0}            # always happy
def feature_store_real(key): raise KeyError("feature view 'f_v2' not found")   # what production did (invented)
def predict(fetch):
    feats = fetch("user42"); return feats["f1"]
assert predict(feature_store_mock) == 0.0                   # CI: green
try:
    predict(feature_store_real); raise SystemExit("should fail")
except KeyError as e:
    print("contract/smoke test against the real store fails at once:", e)
```

**Output (my run):**
```text
failed requests, first 12 min: 432000 | through end of rollback (upper bound): 648000
monthly requests: 1555200000 | error budget (0.1%): 1555200
share of monthly budget burned: 0.417
canary exposure (failed requests): 12600
reduction vs no canary: 0.981
contract/smoke test against the real store fails at once: "feature view 'f_v2' not found"
```

**Follow-ups:**
- Why not rely on the contract test alone? It checks what you thought of; the canary also catches what you did not.
- How do you keep the integration test fast? Seed a small staging feature store and test 20 representative keys; run the heavy suite nightly.
- Book 4 link: "Rolling updates, rollbacks and canary releases for a new model version on Kubernetes" in Book4_MLOps_Part03.md.

**Common mistakes:** Multiplying by 12 instead of 12 x 60. Reporting only the first 12 minutes and ignoring the rollback minutes. Saying "add more tests" without naming the test. Using a mock for the one dependency that failed. Treating the rollback time as someone's fault instead of a missing automation.

### Q6 ⭐⭐⭐ 🟡 The training pipeline switched to filling a null income with the training mean of 48,000, while the serving service still fills it with 0. In a sample of 5,000 live requests, 300 (6% of the sample) have a null income. How do you confirm the skew, estimate its damage, and fix it, and which control makes this class of change impossible to ship unnoticed?
**Asked at:** Feature-store and skew material (techinterview.org pages on point-in-time joins, drift and feature stores and MLOps pipelines, DesignGurus and barkingiguana pages on training-serving skew; one snippet gives a mean-imputation versus zero-fill skew incident as a template); prep and course material rather than a documented real incident; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** I replay the same raw rows through the training path and the serving path to prove the 6% of null-income rows get different features, shadow-score them both ways to size the damage, fix the side that does not match the model (serving, by shipping the imputation inside the model artifact), and make a parity test in CI the control that blocks this.

**Clarifying questions:**
- Which model version is serving and which fill was it trained with? If the old model was trained with zero fill, changing serving to 48,000 would break the old model; fill and model version travel together.
- Is the new training pipeline already live in a deployed model? It decides between rollback and a serving hotfix.
- Is null income random or informative (for example, new customers)? Mean fill hides a signal that zero fill exaggerates.
- What type of model is it? A linear or neural model reacts strongly to 0 versus 48,000; a tree may only care about which side of a split. The replay tells me, not my guess.
- What decisions use the score, and at what cut-off? Damage is measured in flipped decisions, not in score points.

**Approach:**
1. First 15 minutes. Check whether the new model is live. If yes, and nothing yet shows harm, take a sample of live requests (log raw input, imputed value, score) so the evidence is saved before I touch anything.
2. Confirm the skew. Replay the sample's raw rows through the training transform and the serving transform and diff the features. In my run the sample has 300 nulls of 5,000, and the parity test finds exactly those 300 mismatches. The 6% is a sample figure; the 95% interval is 5.4% to 6.7%, so traffic share is about that, not exactly 6%.
3. Estimate the damage. Shadow-score the same sample with both fills. In my toy linear model the 300 null rows had a mean score of 0.249 with the right fill and 0.755 with zero fill, so the mean shift over all 5,000 requests was +0.030 (that is 0.06 x 0.506) and 249 of the 300 decisions flipped at an illustrative 0.35 cut-off, about 5% of all requests. The numbers are from a toy; run the replay on the real model.
4. Rollback criteria. If the new model is live and the replay shows flipped decisions above a set share (for example 2% of all requests, illustrative), roll back to the previous model and its matching fill. If the share is smaller, hotfix serving to the training fill and watch.
5. First day. Ship the fix: one imputation function, fitted at training time and saved inside the model artifact, loaded by serving. Re-score or correct the decisions that flipped if they had customer impact (list them by request id).
6. Next quarter. Put the parity test in CI (same raw rows, train path versus serve path, features must be equal); log the imputed-feature rate in production and alert if the null-fill rate moves; consider a missing-indicator feature so "null" stays visible to the model.
7. Blameless postmortem. The pipeline change was reasonable and the serving service was never told. The gap is that preprocessing lived in two places with no test connecting them. Action items: one shared transform, a parity test and a release checklist line, not "tell both teams".

**Metrics:**
- Null share = null-income requests / sampled requests = 300 / 5,000 = 6.0% (Wilson 95% interval 5.4% to 6.7%).
- Feature mismatch rate = rows where train-path and serve-path features differ / sampled rows (here 300 / 5,000 = 6%).
- Score shift = mean(score with serving fill - score with training fill) on the affected rows and overall; flipped-decision rate at the production cut-off.
- Guardrails: null-fill rate by day, score distribution of null rows, approval or decline rate for null-income customers.

**Risks:**
- Fixing serving when the live model is the old one (trained with zero fill) creates a new skew.
- Mean fill is not neutral; for informative nulls it may be wrong for both train and serve. Check outcome rates for null rows before choosing.
- A parity test on clean data may pass; make sure the replay set contains nulls and edge cases.
- The toy's numbers do not transfer to the real model; treat 0.506 and 249 flips as an illustration of the method.

**What the interviewer scores:**
- Strong: proves the skew with a replay, then sizes it in decisions. Weak: "retrain the model" without evidence.
- Strong: notes fill and model version must match. Weak: "just change serving to 48,000".
- Strong: names a control (parity test, shared transform in the artifact). Weak: "communicate better".
- Strong: separates sample from traffic (interval on 6%). Weak: quotes 6% as exact.

**Example:** Illustrative numbers. Weak answer: "Serving uses zero and training uses the mean, so I would change serving to the mean and redeploy." Strong answer: "First I check which model is live, because the old one may expect zero. I replay 5,000 saved requests through both paths: 300 differ, all the null-income rows. Shadow-scoring says those rows jump from about 0.25 to 0.76 and 249 decisions flip, so if the new model is live I roll back now, then ship one imputation inside the model artifact and add a parity test to CI."

**Code:**
```python
# Q6: mean-fill in training (48,000) vs zero-fill in serving. Illustrative; seeded.
import math
import numpy as np

# prompt arithmetic + sampling uncertainty of "6% null"
n_live, n_null = 5000, 300
assert n_null / n_live == 0.06
p = n_null / n_live
z = 1.96
wilson_lo = (p + z*z/(2*n_live) - z*math.sqrt(p*(1-p)/n_live + z*z/(4*n_live**2))) / (1 + z*z/n_live)
wilson_hi = (p + z*z/(2*n_live) + z*math.sqrt(p*(1-p)/n_live + z*z/(4*n_live**2))) / (1 + z*z/n_live)
print(f"null share in sample = {p:.1%}; 95% Wilson interval = [{wilson_lo:.1%}, {wilson_hi:.1%}]  (a sample, not the whole traffic)")
assert 0.053 < wilson_lo < 0.054 and 0.066 < wilson_hi < 0.067

# toy model: default risk falls with income. Train WITH mean fill (48,000).
rng = np.random.default_rng(66)
def make(m):
    income = rng.lognormal(math.log(42_000), 0.45, m)
    x2 = rng.normal(size=m)
    logit = -1.2 - 1.0 * (income - 48_000) / 20_000 + 0.6 * x2
    y = (rng.random(m) < 1 / (1 + np.exp(-logit))).astype(float)
    return income, x2, y
inc, x2, y = make(100_000)
is_null = rng.random(100_000) < 0.06
mean_income = inc[~is_null].mean()
print("training mean of non-null income:", round(mean_income))
assert 45_000 < mean_income < 51_000                  # about 48,000 as in the prompt (this toy uses its own draw)
FILL = 48_000                                         # the prompt's value; use it for both sides of the comparison
inc_tr = np.where(is_null, FILL, inc)
def feats(income, x2): return np.column_stack([np.ones(len(income)), (income - FILL) / 20_000, x2])
D = feats(inc_tr, x2); w = np.zeros(3)
for _ in range(15):
    pr = 1 / (1 + np.exp(-D @ w)); w -= np.linalg.solve((D * (pr * (1 - pr))[:, None]).T @ D, D.T @ (pr - y))
print("fitted weights (bias, income, x2):", w.round(2))

# 5,000 live requests, 300 with null income. Score with both fills.
inc_l, x2_l, _ = make(n_live)
null_l = np.zeros(n_live, bool); null_l[rng.choice(n_live, n_null, replace=False)] = True
def score(fill_value):
    inc_f = np.where(null_l, fill_value, inc_l)
    return 1 / (1 + np.exp(-(feats(inc_f, x2_l) @ w)))
s_train_fill, s_zero_fill = score(48_000), score(0)
diff = s_zero_fill - s_train_fill
print(f"non-null rows changed: {int((np.abs(diff[~null_l]) > 0).sum())}; null rows mean score {s_train_fill[null_l].mean():.3f} (right fill) vs {s_zero_fill[null_l].mean():.3f} (zero fill)")
assert (np.abs(diff[~null_l]) == 0).all()
shift_null = diff[null_l].mean(); shift_all = diff.mean()
print(f"mean shift on null rows = {shift_null:+.3f}; mean shift over all 5,000 = {shift_all:+.4f}")
assert abs(shift_all - 0.06 * shift_null) < 1e-12 and shift_null > 0.2

# decisions flipped at an illustrative cut-off of 0.35 (decline above it)
thr = 0.35
flipped = ((s_train_fill > thr) != (s_zero_fill > thr))
print("null rows whose decision flips:", int(flipped.sum()), "of", n_null, "| as share of all requests:", f"{flipped.sum()/n_live:.2%}")
assert flipped.sum() > 0.2 * n_null and flipped.sum() == int(flipped[null_l].sum())

# the control: a parity test that replays the SAME raw rows through the train path and the serve path
def train_impute(v): return FILL if v is None else v
def serve_impute(v): return 0 if v is None else v
raw = [None if k < n_null else 40_000 + k for k in range(n_live)]
mism = sum(train_impute(v) != serve_impute(v) for v in raw)
print("parity test mismatches:", mism)
assert mism == 300                                    # catches exactly the null rows, in CI, before any deploy

# and the fix: ONE shared function shipped inside the model artifact
def impute(v, fill=FILL): return fill if v is None else v
assert sum(impute(v) != impute(v) for v in raw) == 0
```

**Output (my run):**
```text
null share in sample = 6.0%; 95% Wilson interval = [5.4%, 6.7%]  (a sample, not the whole traffic)
training mean of non-null income: 46552
fitted weights (bias, income, x2): [-1.18 -1.    0.59]
non-null rows changed: 0; null rows mean score 0.249 (right fill) vs 0.755 (zero fill)
mean shift on null rows = +0.506; mean shift over all 5,000 = +0.0303
null rows whose decision flips: 249 of 300 | as share of all requests: 4.98%
parity test mismatches: 300
```

**Follow-ups:**
- Would a tree model be hit the same way? Not necessarily; zero and 48,000 may fall on the same side of a split. The replay answers it per model, so do not assume.
- Why not just add a null indicator? It helps the model use missingness, but the mismatch between the paths still has to be removed first.
- Book 4 link: "Training-serving skew from the code side" in Book4_MLOps_Part01.md.

**Common mistakes:** Fixing the wrong side. Estimating damage by score points instead of decisions. Treating a 6% sample figure as exact. Trusting that two teams share a convention. Having no test that runs the same raw row through both paths.

### Q7 ⭐⭐⭐ 🟡 At 10:00 the registry alias 'champion' was moved from version 17 to version 18, but 4 of the 10 serving pods (40%) cached version 17 at startup and never re-resolved the alias. The two versions differ by a mean absolute difference of 0.08 in score per request, and the logs show only the alias name. How do you detect this today, fix it, and change the design so the served version is always provable?
**Asked at:** Model-registry and rollback pages (oneuptime and mljar rollback runbooks that move a 'champion' alias or demote a Production stage, a Towards AI piece on registries as the source of truth); secondary practitioner material, no located public incident; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** Today I detect it by reading the model version out of every response and counting versions per pod, fix it with a rolling restart of the 4 stale pods, and change the design so deployments pin a numeric version, the alias is read only by the promotion job, and every response carries a version I can prove.

**Clarifying questions:**
- Is v18 the intended, validated version? If v18 is the suspect one, the right move is the other direction (restart the 6 pods back to v17), so confirm which version is the safe one first.
- Is the 0.08 stable across segments? It is a mean absolute difference per request; the gap may be larger for some customer groups, so I would check the distribution, not only the mean.
- Do users or sessions need consistent scores across requests (credit offers, rankings)? Mixed versions give the same user different answers.
- Can I see which version each pod holds without restarting it (a version endpoint, a log line at startup, a metric label)? Today the logs show only the alias name, so the answer is no, which is the design bug.
- Is any experiment or monitor reading these scores right now? A 60/40 mix quietly contaminates an A/B test and every drift metric.

**Approach:**
1. First 15 minutes. Ask each pod which version it holds (a version endpoint, a model hash in the health check, or the startup logs of each pod). Count the versions: 6 pods on v18, 4 on v17. Post it in the channel. Alias behaviour of registries is editor knowledge here, not tested: an alias is a movable pointer, and a client that resolves it once at startup keeps the version it got.
2. Decide the target. If v18 is the intended and validated version, do a rolling restart of the 4 stale pods one at a time (illustrative 90 seconds each, 6 minutes in total, my run). If v18 is in doubt, roll the 6 back to v17 and investigate.
3. Rollback and escalation criteria. Stop and roll back to the previous version if error rate or p95 latency of any pod rises above the guardrail after the restart. Escalate to the platform owner if pods keep picking up the old version after restart (which would mean the cache lives somewhere other than the pod).
4. Impact. With a 60/40 mix, the expected mean absolute deviation from the intended model is 0.4 x 0.08 = 0.032 per request, and a user making 5 requests has a 91.2% chance of being served by both versions (my run, random load balancing). Find the decisions that crossed a cut-off during the window if the score drives a decision.
5. First day. Add model_version and model_hash as a response header and a log field, and a metric labelled by version per pod. Alert when more than one version is served after a grace period of 10 minutes following a promotion (my run: alias moved at 10:00, alert by 10:15).
6. Next quarter. Deployments resolve the alias once, at deploy time, and write the numeric version into the manifest; pods never resolve aliases themselves. Promotion becomes a pipeline step: move alias, update the manifest, roll the fleet, verify the version count, all in one run. Add a post-promotion check that fails if the versions served differ from the expected one.
7. Blameless postmortem. The system let two valid readings of "champion" exist at once, and the logs could not tell them apart. Action items are the version header, the single-version alert and the pinned manifest, not "remember to restart pods after promotion".

**Metrics:**
- Share of traffic on the wrong version = requests served by v17 / requests = 40% (4 of 10 pods, assuming even load per pod).
- Mean absolute score deviation from intended = share on wrong version x mean absolute difference = 0.4 x 0.08 = 0.032.
- Time to detect = time the alias moved to the first alert (here 15 minutes with the new rule; today it is open-ended); time to converge = rolling restart time.
- Guardrails: number of distinct versions served per service (must be 1 after the grace period), error rate and p95 during the restart.

**Risks:**
- Restarting all pods at once drops capacity; keep max unavailable at 1.
- If the pods re-resolve the alias at startup and someone moves the alias mid-restart, the fleet could split again; pin the version first, then restart.
- A version header proves what was loaded, not that the artifact is the right one; add the model hash from the registry.
- The 0.032 is a projection from the prompt's 0.08 and an even pod share; the simulation in my run gave 0.0308 because clipping scores to [0, 1] slightly shrinks the difference.

**What the interviewer scores:**
- Strong: gets 6 versus 4 visible with a concrete signal (header, label, hash), not just "check the logs". Weak: "restart everything and hope".
- Strong: asks which version is the safe one before acting. Weak: assumes v18 is right.
- Strong: design fix removes the class of bug (pin at deploy, one version proof). Weak: "restart pods after every promotion".
- Strong: quantifies the impact (0.032, user-level 91%) and blameless framing. Weak: no numbers, blames the promoter.

**Example:** Illustrative numbers. Weak answer: "I would restart the pods and tell people to restart after moving the alias in future." Strong answer: "I would ask every pod for its model version: 6 say 18, 4 say 17. Version 18 is the validated one, so I restart the 4 pods one at a time, about 6 minutes. Expected deviation was 0.4 times 0.08, so 0.032 per request, and most users saw both versions. After that I pin the number 18 into the deployment, return the version in every response, and alert if two versions are served 10 minutes after a promotion."

**Code:**
```python
# Q7: alias 'champion' moved 17 -> 18 but 4 of 10 pods cached 17. Illustrative; seeded.
import math
from collections import Counter
import numpy as np

pods = ["v18"] * 6 + ["v17"] * 4
stale = pods.count("v17") / len(pods)
assert stale == 0.4

# The prompt gives 0.08 as the mean ABSOLUTE per-request score difference between versions.
# The fleet-wide expected deviation from the intended model is then 0.4 x 0.08.
fleet_dev = stale * 0.08
print("expected mean |score deviation| over all traffic =", round(fleet_dev, 3))
assert round(fleet_dev, 3) == 0.032

rng = np.random.default_rng(7)
N = 200_000
s18 = rng.beta(2, 5, N)
sd = 0.08 * math.sqrt(math.pi / 2)                       # normal noise with mean absolute value 0.08
s17 = np.clip(s18 + rng.normal(0, sd, N), 0, 1)           # (clipping makes the mean slightly smaller)
pod_idx = rng.integers(0, 10, N)                          # random load balancing
served_v17 = np.array([pods[i] == "v17" for i in pod_idx])
served = np.where(served_v17, s17, s18)
dev = np.abs(served - s18).mean()
print(f"simulated share on v17 = {served_v17.mean():.3f}; mean |deviation| from intended = {dev:.4f}")
assert abs(served_v17.mean() - 0.4) < 0.005 and 0.028 < dev < 0.034

# a user making 5 requests sees both versions with probability:
p_mixed = 1 - 0.6**5 - 0.4**5
print("P(a user sees both versions in 5 requests) =", round(p_mixed, 4))
assert round(p_mixed, 4) == 0.912

# detection TODAY: every response carries model_version (header) and a metric labelled by version.
logs = Counter(pods[i] for i in pod_idx[:5000])
print("version counts in 5,000 logged responses:", dict(logs))
def check_versions(counter, expected, minutes_since_promotion, grace=10):
    extra = [v for v in counter if v != expected]
    if minutes_since_promotion >= grace and extra:
        return f"ALERT: serving {sorted(counter)} but expected {expected}"
    return "ok"
msg = check_versions(logs, "v18", 15); print(msg)
assert msg.startswith("ALERT") and check_versions(Counter({"v18": 10}), "v18", 15) == "ok"
assert check_versions(logs, "v18", 3) == "ok"            # inside the grace period, no alert

# fix: rolling restart one pod at a time; illustrative 90 s to load and pass readiness
stale_pods, per_pod_s, max_unavailable = 4, 90, 1
restart_min = stale_pods * per_pod_s / max_unavailable / 60
print("rolling restart time (minutes):", restart_min)
assert restart_min == 6.0

# design: deployments pin a numeric version; the alias is only read by the promotion job
def resolve_at_deploy(alias_table, alias): return alias_table[alias]    # returns 18, written into the manifest
manifest = {"model": "fraud", "version": resolve_at_deploy({"champion": 18}, "champion")}
assert manifest["version"] == 18
print("manifest pins:", manifest)

# detection delay example: alias moved 10:00, alert rule with 10 min grace + 5 min metric window -> 10:15
detect = 10 + 5
print("detected by 10:%02d" % detect); assert detect == 15
```

**Output (my run):**
```text
expected mean |score deviation| over all traffic = 0.032
simulated share on v17 = 0.400; mean |deviation| from intended = 0.0308
P(a user sees both versions in 5 requests) = 0.912
version counts in 5,000 logged responses: {'v18': 2990, 'v17': 2010}
ALERT: serving ['v17', 'v18'] but expected v18
rolling restart time (minutes): 6.0
manifest pins: {'model': 'fraud', 'version': 18}
detected by 10:15
```

**Follow-ups:**
- Why not make pods re-resolve the alias every minute? It removes the stale cache but replaces "provable" with "eventually consistent"; a pinned version plus a deliberate rollout is easier to prove and to roll back.
- How do you roll back? Move the pinned version in the manifest to the previous number and roll the fleet; the alias follows afterwards, not before.
- Book 4 link: "MLflow Model Registry: registered models, versions, aliases and the deprecated stages" in Book4_MLOps_Part04.md for alias basics.

**Common mistakes:** Only restarting without adding visibility. Assuming one alias move means one version served. Forgetting that mixed versions break per-user consistency and experiments. Not checking that v18 is the right target. Treating 0.08 as a fleet-wide shift instead of a per-request difference on the affected share.

### Q8 ⭐⭐⭐ 🟡 A feature table due at 06:00 landed at 09:30, which is 210 minutes late, and the 07:00 scoring job quietly read the previous day's partition, so 1,000,000 customers were scored on features one day old. The job exited with success. What do you do now for the 1,000,000 scores, and what checks make a stale input fail loudly next time?
**Asked at:** Data-pipeline pages (luminousmen on avoidable backfills and non-idempotent jobs, DZone on silent upstream schema change, HackerNoon and Seattle Data Guy on silent pipeline failures, DataExpert on schema drift and idempotent replays, DataVidhya on measuring detection latency in postmortems); practitioner blogs rather than an interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** I rescore the 1,000,000 customers now from the 09:30 table, mark the stale scores so nothing new reads them, trace who already used them, and change the job so a missing or old input partition fails the run instead of falling back silently.

**Clarifying questions:**
- Who reads the scores, and when? A campaign that already ran at 08:00 is a different problem from a dashboard nobody opened yet.
- How different are yesterday's and today's features for these customers? If I can compute it, I size the damage; if not, I rescore everything.
- How long does a full rescore take and does it hold up the next day's run? Illustrative: 25 minutes.
- Why did the job read the previous partition: an explicit "latest partition" fallback, a default date, a missing dependency? That is the actual defect.
- Is a late table normal (a known SLA slip) or new? It sets how loud the alert is.

**Approach:**
1. First 15 minutes. Stop consumers: pause any downstream job that reads the score table, and label the 07:00 run's output as stale (set a flag or rename the partition). Confirm the 09:30 table is complete (row counts, null rates versus yesterday).
2. Rescore. Run the scoring job against today's partition (illustrative 25 minutes, done at 10:00 in my run), overwriting the same output partition so there is one set of scores. Verify row count equals customers and every row carries today's feature date.
3. Damage trace. List what read the stale scores and when: campaigns, limits, dashboards. For each, decide whether the decision changes enough to redo. Measure it: diff stale versus fresh scores per customer. As a guide, in my simulation with an assumed day-to-day correlation of 0.95, about 43,840 customers (4.4%) change top-10% membership; the real figure comes from the diff, not from my assumed correlation.
4. Rollback and escalation criteria. If the fresh table fails its checks (row count below 99% of customers, null rate far above yesterday), do not rescore; keep yesterday's scores flagged as stale and escalate to the table owner. Escalate to the business owner at once if a decision with customer impact (a credit limit, an offer) used the stale scores.
5. First day. Fix the job: compute the expected partition from the run date; if it is missing, fail with a clear message (my run shows the failure). Add a feature_date column to the output and an assertion that all rows match the run date. Add a sensor with a grace period: if the table has not landed by 06:30, page the data owner.
6. Next quarter. Define data contracts with the table's owner (landing time, completeness, how lateness is signalled); add a freshness metric per input to the dashboard; run a game day where an input is withheld and the job must refuse. Keep an explicit, logged "allow stale up to N days" switch for the cases where staleness is acceptable, so it is a decision, not an accident.
7. Blameless postmortem. The job did what it was written to do: take the latest partition. The failure was that "latest" was treated as "correct". Questions: who knew the table was late at 06:00, and did anything tell the scoring job? Action items are the contract, the sensor and the freshness assertion.

**Metrics:**
- Staleness = scoring date minus feature date, in days (1 here); share of rows with feature_date not equal to run date (100% of the 1,000,000 rows).
- Lateness = landing time minus due time = 09:30 - 06:00 = 210 minutes; scoring ran 150 minutes before the data landed.
- Exposure time of stale scores = from 07:00 to the end of the rescore, 180 minutes in my illustrative timeline.
- Damage = customers whose decision changes between stale and fresh scores / customers (measure with the diff).
- Guardrails: input freshness by table, row count versus customers, null rate versus yesterday.

**Risks:**
- Rescoring from a table that is itself incomplete, replacing bad scores with worse ones. Check the table first.
- Overwriting the output while a consumer is reading it; coordinate or write-then-swap.
- Hiding the staleness by deleting evidence. Keep the stale run's metadata for the postmortem.
- My top-10% simulation assumes a correlation (0.95, invented). A different correlation gives a different count (2.0% at 0.99, 8.7% at 0.80 in my run).

**What the interviewer scores:**
- Strong: stops consumers first, then repairs, then traces impact. Weak: "rerun the job" and nothing else.
- Strong: names the real defect (silent fallback to the latest partition). Weak: blames the late upstream team.
- Strong: checks fail loudly (expected-partition assertion, feature_date column, landing sensor). Weak: "monitor the job".
- Strong: blameless and gives a contract. Weak: "ask the upstream team to be on time".

**Example:** Illustrative numbers. Weak answer: "The table was late, so I would tell the upstream team to deliver on time and rerun the job." Strong answer: "I pause the readers, rescore the 1,000,000 customers from the 09:30 table so the new scores are in place by about 10:00, and check who already read the 07:00 scores. Then the job gets an expected-partition check so it fails with 'partition missing' instead of reading yesterday, a feature_date on every row, and a sensor that pages at 06:30 if the table has not landed."

**Code:**
```python
# Q8: feature table 210 minutes late; the scoring job silently used yesterday's partition. Illustrative; seeded.
from datetime import date, datetime, timedelta
import numpy as np

# prompt arithmetic
due, landed, scored = datetime(2026, 10, 31, 6, 0), datetime(2026, 10, 31, 9, 30), datetime(2026, 10, 31, 7, 0)
late_min = (landed - due) / timedelta(minutes=1)
assert late_min == 210
print("late by", int(late_min), "min; scoring ran", int((due + timedelta(hours=1) - due) / timedelta(minutes=1)), "min after the due time but", int((landed - scored) / timedelta(minutes=1)), "min before the data existed")
assert (landed - scored) / timedelta(minutes=1) == 150

# illustrative recovery timeline: rescoring takes 25 min for 1,000,000 customers; start 5 min after landing
rescore_start = landed + timedelta(minutes=5); rescore_end = rescore_start + timedelta(minutes=25)
exposure_min = (rescore_end - scored) / timedelta(minutes=1)
print("stale scores existed from 07:00 to", rescore_end.strftime("%H:%M"), "=", int(exposure_min), "min")
assert rescore_end.strftime("%H:%M") == "10:00" and exposure_min == 180

# how different are one-day-old features? Simulate scores with day-to-day correlation rho (an ASSUMPTION; measure it for real)
rng = np.random.default_rng(8)
N = 1_000_000
for rho in (0.99, 0.95, 0.80):
    s_old = rng.normal(size=N)
    s_new = rho * s_old + np.sqrt(1 - rho**2) * rng.normal(size=N)
    top_old = s_old >= np.quantile(s_old, 0.90); top_new = s_new >= np.quantile(s_new, 0.90)
    wrong = int((top_old != top_new).sum())          # customers wrongly in or out of the top 10% target list
    print(f"rho={rho}: customers whose top-10% membership differs = {wrong:,} ({wrong/N:.1%})")
    if rho == 0.95: w95 = wrong
assert 20_000 < w95 < 70_000        # a 'small' 1-day lag still misplaces tens of thousands of customers at rho 0.95

# what makes it fail loudly: freshness assertion on the INPUT, and lineage on the OUTPUT
def pick_partition(available, run_date):
    if run_date not in available:
        raise RuntimeError(f"feature partition {run_date} missing (latest is {max(available)}); refusing to score")
    return run_date
today, yday = date(2026, 10, 31), date(2026, 10, 30)
try:
    pick_partition({yday}, today); raise SystemExit("must fail")
except RuntimeError as e:
    print("job now fails:", e)
assert pick_partition({yday, today}, today) == today

def check_output(rows, expected_date, expected_n, tol=0.01):
    bad = [r for r in rows if r["feature_date"] != expected_date]
    assert not bad, f"{len(bad)} rows carry stale feature_date"
    assert abs(len(rows) - expected_n) / expected_n <= tol, "row count off"
    return "ok"
good = [{"customer": i, "feature_date": today} for i in range(1000)]
stale = [{"customer": i, "feature_date": yday} for i in range(1000)]
assert check_output(good, today, 1000) == "ok"
try: check_output(stale, today, 1000); raise SystemExit("must fail")
except AssertionError as e: print("output check:", e)

# sensor alert: table not landed by 06:30 (30 min grace) pages the data owner; shows detection at 06:30 instead of 09:30+
alert_at = due + timedelta(minutes=30)
print("alert time:", alert_at.strftime("%H:%M"), "-> alert fires", int((landed - alert_at) / timedelta(minutes=1)), "min before the table lands")
assert alert_at.strftime("%H:%M") == "06:30"
```

**Output (my run):**
```text
late by 210 min; scoring ran 60 min after the due time but 150 min before the data existed
stale scores existed from 07:00 to 10:00 = 180 min
rho=0.99: customers whose top-10% membership differs = 19,850 (2.0%)
rho=0.95: customers whose top-10% membership differs = 43,840 (4.4%)
rho=0.8: customers whose top-10% membership differs = 87,474 (8.7%)
job now fails: feature partition 2026-10-31 missing (latest is 2026-10-30); refusing to score
output check: 1000 rows carry stale feature_date
alert time: 06:30 -> alert fires 180 min before the table lands
```

**Follow-ups:**
- Should the job wait for the table instead of failing? A bounded wait is fine (poll until a cutoff), then fail; waiting forever hides the problem and delays everything behind it.
- What if yesterday's features are acceptable for some uses? Make that an explicit setting with a logged maximum age, not a default.
- Book 4 link: "Idempotency in pipeline tasks" and "Backfills and catchup" in Book4_MLOps_Part05.md cover safe reruns.

**Common mistakes:** Rerunning without checking the new table. Leaving the stale scores readable. Treating a green exit code as correct output. Having no feature_date in the output. Asking another team to "be on time" as the whole fix.

### Q9 ⭐⭐⭐ 🟡 A daily scoring job that appends to its output table was retried by the scheduler after a timeout at minute 55, but the first run was still alive and also finished. The table now holds 2,000,000 rows for 1,000,000 customers for that date, and a downstream campaign job has already read it. How do you clean up, and how do you redesign the job so a duplicate run is harmless?
**Asked at:** Data-pipeline pages (luminousmen on avoidable backfills and non-idempotent jobs, DZone on silent upstream schema change, HackerNoon and Seattle Data Guy on silent pipeline failures, DataExpert on schema drift and idempotent replays, DataVidhya on measuring detection latency in postmortems); practitioner blogs rather than an interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** I freeze the table for readers, prove the two runs agree, build a clean copy with one row per customer and swap it in, check what the campaign already did with 2,000,000 rows, and redesign the write so a second run replaces the partition instead of appending to it.

**Clarifying questions:**
- Did the two runs use the same model version and the same feature partition? If yes the duplicates are identical and either row is safe; if not, I need a rule for which score is right.
- What did the campaign do with the rows: send, queue, or only read? Duplicate rows could mean duplicate contacts, up to 1,000,000 here.
- Is the output table a plain append table or does it support overwrite by partition or merge by key? That is a platform fact I would check, not assume.
- Why did the scheduler retry while the first run was alive: a timeout that did not kill the process? That is the second defect.
- Who owns the downstream job and can it dedupe on its side?

**Approach:**
1. First 15 minutes. Pause the downstream readers of the table, and snapshot it (so I can undo my own cleanup). Count rows and distinct keys: 2,000,000 rows and 1,000,000 customers, so 50% of the rows are duplicates.
2. Prove the runs agree. Join run A and run B on customer id and compare scores. In my run all 1,000,000 scores match, so keeping either row is safe. If some differ, keep the row from the run that used the intended model and features and log each difference; do not pick "the latest" blindly.
3. Clean on a copy. Build a deduplicated table (one row per customer and run date), validate row count equals customers and keys are unique, and swap it in as one step. Never delete in place before the check passes.
4. Downstream. With the campaign owner, establish what was sent. Worst case, one contact per row read, so up to 1,000,000 customers were contacted twice. Stop pending sends, suppress the second send, and decide on an apology or compensation only if contact policy was breached.
5. Rollback and escalation criteria. If the cleaned table fails validation (row count not equal to customers, keys not unique), restore the snapshot and keep readers paused. Escalate to the campaign owner immediately if any send already went out, and to compliance if contact-frequency rules apply (check the company policy).
6. First day. Make the job idempotent: write by overwriting the date partition from a staged copy, or merge by key (customer id plus date), so a second run replaces the first. Stop the old run when a retry starts: take a lease with a token and let a run commit only if its token is current (my run shows the old run rejected and the retry allowed). Idempotent-write features such as overwrite or merge depend on the table format and are editor knowledge here, not tested.
7. Next quarter. Add a downstream readiness gate (distinct keys equal expected rows) so readers refuse a duplicated table; make the campaign job dedupe on its own key; replay duplicate runs in a test (run twice, assert the same table); set timeouts that kill the process, not just mark it failed.
8. Blameless postmortem. A retry is a normal, designed behaviour of a scheduler, and an append job is not safe under it. The failure sits in the design, not in the person who set the timeout. Action items: idempotent write, lease or lock, downstream gate, kill-on-timeout.

**Metrics:**
- Duplicate rate = (rows - distinct keys) / rows = (2,000,000 - 1,000,000) / 2,000,000 = 50%. Duplicates per customer = rows / distinct keys = 2.0.
- Score disagreement = customers whose two scores differ / customers (0 in my run).
- Downstream impact = customers contacted more than once / customers contacted (from the campaign log).
- Guardrails: rows equal distinct keys on every run, run count per partition per day (must be 1 committed), time from duplicate to detection.

**Risks:**
- Deleting the wrong copy when the runs differ. Prove agreement first.
- Cleanup in place with no snapshot; a mistake then has no undo.
- A lease that expires while the run is still working can still allow two writers; a fencing token on the commit is what blocks the late one.
- Overwrite can briefly show an empty or partial partition to readers; swap atomically or gate readers.
- The 1,000,000 duplicate contacts is a worst case; the campaign log gives the real figure.

**What the interviewer scores:**
- Strong: stops readers, snapshots, proves the runs agree, then cleans. Weak: "delete duplicates" at once.
- Strong: asks what the campaign did and treats it as part of the incident. Weak: fixes the table and forgets the customers.
- Strong: redesign makes a duplicate run harmless (overwrite or merge plus a lease), and states that the detail depends on the platform. Weak: "make sure the job never runs twice".
- Strong: blameless and kill-on-timeout. Weak: blames the scheduler or the engineer.

**Example:** Illustrative numbers. Weak answer: "I would delete the extra rows and ask the scheduler team to stop retrying." Strong answer: "I pause the readers and snapshot the table. The 2,000,000 rows are 1,000,000 customers twice, so I compare both runs; they match, so I keep one row each, validate, and swap. Then I check with the campaign team whether anyone got two messages, which could be up to a million customers. The job becomes a partition overwrite with a lease, so a retry replaces rather than adds, and downstream refuses a table where rows differ from distinct keys."

**Code:**
```python
# Q9: appended twice -> 2,000,000 rows for 1,000,000 customers. Illustrative; seeded.
import numpy as np
import pandas as pd

N = 1_000_000
rng = np.random.default_rng(9)
score = rng.random(N)
run_a = pd.DataFrame({"customer_id": np.arange(N), "run_date": "2026-10-31", "score": score, "run_id": "A"})
# run B is a retry: same model and features -> identical scores here; (a real retry may differ slightly)
run_b = run_a.assign(run_id="B")
table = pd.concat([run_a, run_b], ignore_index=True)

# 1) detect and size the damage
rows, distinct = len(table), table["customer_id"].nunique()
dups = rows - distinct
print(f"rows={rows:,} distinct customers={distinct:,} duplicate rows={dups:,} ({dups/rows:.0%} of the table)")
assert rows == 2_000_000 and distinct == 1_000_000 and dups == 1_000_000 and dups / rows == 0.5

# 2) before deleting anything: do the two runs agree?
m = run_a.merge(run_b, on="customer_id", suffixes=("_a", "_b"))
n_diff = int((m["score_a"] != m["score_b"]).sum())
print("customers whose two scores differ:", n_diff)
assert len(m) == N and n_diff == 0       # identical here, so keeping either row is safe. If not, pick by rule and log it.

# 3) clean up on a COPY, then swap (never delete in place first)
clean = table.sort_values(["customer_id", "run_id"]).drop_duplicates(["customer_id", "run_date"], keep="last")
assert len(clean) == N and clean["customer_id"].is_unique and (clean["run_id"] == "B").all()
print("clean table rows:", len(clean))

# 4) downstream: the campaign read 2,000,000 rows. Worst case each duplicated customer was contacted twice.
contacts_worst = rows                     # one contact per row read, if the campaign has no dedupe of its own
print("worst case contacts:", f"{contacts_worst:,}", "for", f"{N:,}", "customers -> up to", f"{contacts_worst-N:,}", "duplicate contacts")
assert contacts_worst - N == 1_000_000

# 5) redesign A: partition overwrite keyed by run date, staged then swapped (dict stands in for a table)
store = {}
def write_partition(store, run_date, df, run_id):
    staged = df.assign(run_id=run_id).drop_duplicates("customer_id")     # staged copy
    assert staged["customer_id"].is_unique
    store[run_date] = staged                                             # swap in as one step (atomic in a real system)
write_partition(store, "2026-10-31", run_a, "A")
write_partition(store, "2026-10-31", run_b, "B")                         # the duplicate run is harmless
assert len(store["2026-10-31"]) == N
print("after two runs, rows for the date:", len(store["2026-10-31"]))

# 6) redesign B: a lease with a fencing token so the old run cannot write after the retry started
class Lease:
    def __init__(self): self.token = 0
    def acquire(self): self.token += 1; return self.token
    def check(self, t): return t == self.token
lease = Lease(); t1 = lease.acquire(); t2 = lease.acquire()               # retry took the lease at minute 55
assert lease.check(t2) and not lease.check(t1)
print("old run may commit:", lease.check(t1), "| retry may commit:", lease.check(t2))

# 7) final gate: downstream checks distinct keys == expected before reading
def readiness(df, expected): return len(df) == expected and df["customer_id"].is_unique
assert not readiness(table, N) and readiness(clean, N)
print("readiness: duplicated table =", readiness(table, N), "| clean table =", readiness(clean, N))
```

**Output (my run):**
```text
rows=2,000,000 distinct customers=1,000,000 duplicate rows=1,000,000 (50% of the table)
customers whose two scores differ: 0
clean table rows: 1000000
worst case contacts: 2,000,000 for 1,000,000 customers -> up to 1,000,000 duplicate contacts
after two runs, rows for the date: 1000000
old run may commit: False | retry may commit: True
readiness: duplicated table = False | clean table = True
```

**Follow-ups:**
- Why not just add a unique constraint? It turns the second write into a loud failure, which is good, but the job then fails on a retry instead of succeeding quietly; pair it with overwrite or merge so the retry succeeds harmlessly.
- Merge or overwrite? Overwrite of a whole partition is simplest when each run recomputes everything; merge by key suits incremental updates. Both need a stable key.
- Book 4 link: "Idempotency in pipeline tasks" in Book4_MLOps_Part05.md.

**Common mistakes:** Deleting in place without a snapshot. Assuming both runs produced identical scores. Ignoring the downstream campaign. Relying on "the scheduler will not retry". Using append for a job that a scheduler is allowed to rerun.

### Q10 ⭐⭐⭐ 🟡 An upstream team changed order_value from rupees to paise, a factor of 100, so a typical value of 850 became 85,000, and nobody told the ML team. The change ran for 2 days before it was caught, and the training table keeps 90 days, so those 2 days are about 2.2% of its days (about 2.2% of rows if volume per day is equal). What do you do about served predictions and the training table, and what contract would have caught it?
**Asked at:** Data-pipeline pages (luminousmen on avoidable backfills and non-idempotent jobs, DZone on silent upstream schema change, HackerNoon and Seattle Data Guy on silent pipeline failures, DataExpert on schema drift and idempotent replays, DataVidhya on measuring detection latency in postmortems); practitioner blogs rather than an interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** Stop the bleeding first (freeze retraining, fix or quarantine the feed), then repair the 2 bad days in the training table and re-score what matters, and add a unit and range contract at ingestion so this cannot be silent again.

**Clarifying questions:**
- Did the change hit the serving path, the training table, or both? It decides whether users saw wrong predictions or only the next model is at risk.
- Is the bad window exactly known (a deploy timestamp, a schema version field)? An exact window makes repair (divide by 100) safe; a fuzzy window means exclude, not fix.
- Did a retrain or auto-deploy run during those 2 days? A model trained on the bad rows may already be live.
- Do predictions drive money or a regulated decision (credit, fraud)? That sets how loudly we notify and whether affected decisions are re-reviewed.
- Is there a raw immutable copy upstream (or a bronze/raw layer)? It lets us replay instead of patching.

**Approach:**
1. First 15 minutes: confirm with a query (daily median of order_value: about 850 for normal days, about 85,000 for the 2 bad days). Page the owner of the upstream table, pause scheduled retraining and any auto-deploy, and stop new bad rows (ask upstream to roll back the change, or add a divide-by-100 shim at our ingestion keyed on the change timestamp).
2. First 15 minutes, serving: if the model uses order_value as an input, compare score distributions for the bad days. If shifted, clamp or cap the feature at serving, or fall back to the previous model or a rule, until the feed is fixed. Escalate to the incident lead if decisions are money-bearing; roll back or fall back if the score distribution has shifted more than a pre-agreed amount (for example, mean score moved by more than 3 standard errors of a normal day).
3. First day, training table: tag the affected partitions, do not delete them. Repair by dividing by 100 only if the window is exact; otherwise exclude those days from training. Never leave them in: the 2 days are 2.2% of days, but they move the mean of order_value about 3x (see the run).
4. First day, predictions: list which decisions were served from bad inputs, re-score them with the repaired features, and decide with the business owner which need correcting or notifying. Check whether any model trained on the table in the window needs retraining or discarding.
5. Next quarter, contract: write a data contract for the feed. Name the field and unit (`order_value_inr`), type, a valid range, and a schema version. Enforce it in two places: producer CI (breaking change needs a version bump and consumer sign-off) and consumer ingestion (range and distribution checks that quarantine a partition, not just warn).
6. Blameless postmortem: the failure was a missing contract and slow detection, not a person. Timeline, detection delay (48 hours here), why no check existed, and action items with owners and dates (contract, distribution monitor, change-notice channel).

**Metrics:**
- Detection delay = time of first bad row to time of detection. Here 48 hours; target under 24 hours with a daily check, and under 1 hour with a per-batch check.
- Affected-row share = bad rows / all rows in the training table (exactly 2/90 of days = 2.2% only if volume per day is equal; use the real row count).
- Feature drift check: daily median of order_value divided by trailing 14-day median; alarm outside 0.2 to 5.
- Served-impact count = predictions made with bad inputs / all predictions in the window.
- Guardrails: no schema change merges without a consumer sign-off; quarantine, never silent drop.

**Risks:**
- Repairing with a divide when some rows in the window were already correct (a partial rollout) creates a new bug. Check by partition and by source.
- The 2.2% is a share of days, not of rows; busy days weigh more.
- A rules-only range check misses a small unit change (for example, 1.2x). Add a distribution test.
- Models trained during the window may still be serving.

**What the interviewer scores:**
- Strong: separates serving, training table and process; gives an order of actions; repairs without destroying evidence.
- Strong: contract has an owner, enforcement point and a consequence (quarantine), not only a document.
- Strong: measures detection delay and brings a blameless action list.
- Weak: "tell upstream to be careful"; deleting rows silently; only fixing the table and forgetting served predictions.

**Example:** Illustrative: 1,000 orders a day, 90 days. A typical order is 850. For 2 days the field is 85,000. Weak versus strong answer:
- Weak: "I would tell the upstream team to notify us next time and then retrain."
- Strong: "First I pause retraining and cap the feature at serving. Then I tag those two partitions, repair them by dividing by 100 because the window is exact, and re-score the affected decisions. The fix that matters is a contract with the unit in the column name plus a median check at ingestion that quarantines a partition, so detection goes from 48 hours to under a day. I would run a blameless review: nobody did anything unusual, we simply had no gate."

**Code:**
```python
import numpy as np

rng = np.random.default_rng(10)
days, bad_days, per_day = 90, 2, 1000          # illustrative: 1,000 orders a day
share_days = bad_days / days
assert round(share_days * 100, 1) == 2.2

# Training table: lognormal order values around 850 rupees; last 2 days are in paise
day = np.repeat(np.arange(days), per_day)
val = rng.lognormal(mean=np.log(850), sigma=0.4, size=day.size)
raw = val.copy()
bad = day >= days - bad_days
raw[bad] *= 100
share_rows = bad.mean()
assert abs(share_rows - share_days) < 1e-12     # equal volume per day: row share = day share
print("bad share of days/rows:", round(share_days * 100, 2), "%")
print("median clean/raw:", round(float(np.median(val))), round(float(np.median(raw))))
print("mean   clean/raw:", round(float(val.mean())), round(float(raw.mean())))
assert raw.mean() / val.mean() > 3             # 2.2% of rows moves the mean 3x
assert abs(np.median(raw) / np.median(val) - 1) < 0.02   # the median barely moves

# Repair: divide the affected partitions by 100, only because the window is known exactly
fixed = raw.copy()
fixed[bad] /= 100
assert np.allclose(fixed, val)
print("repair restores the table:", bool(np.allclose(fixed, val)))

# Contract check at ingestion: compare each day's median with the trailing 14-day median
def first_alarm(values_by_day, ratio=5.0, k=14):
    meds = [np.median(values_by_day[day == d]) for d in range(days)]
    for d in range(k, days):
        base = np.median(meds[d - k:d])
        if meds[d] > ratio * base or meds[d] < base / ratio:
            return d
    return None
a = first_alarm(raw)
assert a == days - bad_days                    # alarm on the first bad day
delay_hours_daily = 24          # daily batch check: at most one day
delay_hours_caught = bad_days * 24
print("first alarm day index:", a, "| detection delay with the check <= 24 h vs", delay_hours_caught, "h without")
assert delay_hours_caught == 48

# Served predictions: a linear-in-log model sees log(85000)-log(850) = ln(100) extra
ln100 = np.log(100)
print("extra log-value fed to the model:", round(float(ln100), 2))
assert round(float(ln100), 2) == 4.61
# Suppose the model's log-odds weight on log(order_value) is 0.3 (illustrative):
shift = 0.3 * ln100
print("log-odds shift for a typical order:", round(float(shift), 2))
assert round(float(shift), 2) == 1.38
```

**Output (my run):**
```
bad share of days/rows: 2.22 %
median clean/raw: 850 860
mean   clean/raw: 920 2959
repair restores the table: True
first alarm day index: 88 | detection delay with the check <= 24 h vs 48 h without
extra log-value fed to the model: 4.61
log-odds shift for a typical order: 1.38
```

**Follow-ups:**
- What if you cannot tell exactly which rows changed? Exclude the whole window from training, keep the raw rows, and ask upstream for the deploy time.
- How strict should the contract be? Strict on name, unit, type and range at the producer; statistical checks at the consumer. Breaking changes need a version and a consumer sign-off.
- How do you stop a bad model that trained on this? Compare it to the previous model on a fixed holdout built before the window and block promotion if it is worse (see Book 4 Part 1, Q5, "How do you make a trained model reproducible six months later?", on what to record per run).

**Common mistakes:**
- Fixing the table but not the served predictions.
- Deleting bad rows instead of quarantining them.
- Treating "2.2%" as harmless; an outlier 100x large moves a mean far more than its share.
- Writing a contract nobody enforces.

### Q11 ⭐⭐⭐ 🟡 A model API has a 99.5% availability objective over a 30-day month, which is 216 minutes of allowed downtime. Two outages have used 70 and 95 minutes, and the current one has run for 40 minutes so far and is still going. Counting the current outage, how much budget is left, and what do you decide about the release schedule and about the fix you are about to ship?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to error budgets and SLOs in SRE and MLOps material; related topics appear in public MLOps guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** 216 minutes minus 205 used, counting the current outage, leaves 11 minutes (5.1%), and it burns one minute per minute while we are down, so freeze every non-essential release and ship the fix only with a fast rollback and a small first step.

**Clarifying questions:**
- Is the objective measured on a rolling 30 days or the calendar month? On a rolling window the 95-minute outage ages out later; on a calendar month the budget resets on the first.
- Is the outage a full outage or partial (some requests failing)? Partial downtime counts in proportion, so the burn is slower.
- What does the fix change: config, a model version, infrastructure? A risky fix can add a second outage.
- Who owns the budget policy (a freeze rule written down, or only a norm)? It decides whether I can say "no release" or can only advise.
- Is there a contractual SLA with credits behind the 99.5%? The internal objective is a goal; the contract is a promise.

**Approach:**
1. First 15 minutes: mitigate before diagnosing. Roll back the last change, fail over, or serve a fallback. Open an incident channel, name an incident lead and a communicator, and post a first status line.
2. Do the math in the open: budget 216 min, used 70 + 95 + 40 = 205, left 11. At full outage the budget runs out at outage minute 51, in 11 minutes. After that, every minute is over objective.
3. Release policy: freeze feature and model releases until the budget recovers or the leadership explicitly accepts the risk. Only fixes for the outage, security fixes and rollbacks go out.
4. The fix you are about to ship: ship it, because staying down costs 1 minute of budget per minute; but ship it small and reversible. First step to 5 to 10% of traffic or one replica, watch error rate for a pre-agreed time (for example 10 minutes), then widen. Roll back if the error rate is above the pre-outage baseline by more than a set margin, or latency p99 doubles. Escalate to the engineering lead if the first step does not work or the fix needs a risky data or schema change.
5. First day: restore service, write a customer note, and keep the freeze until a review. Confirm the real downtime from monitoring, not from memory.
6. Next quarter: look at what repeats across 3 outages in a month (70, 95, 40+ minutes): bad deploys, a single dependency, or slow detection. Fund the top cause. Add burn-rate alerts (fast and slow) so we get paged at 2% of budget gone in an hour, not at 100%.
7. Blameless postmortem: three outages in a month is a system signal. Ask what made each outage long (detection, diagnosis, rollback time), not who pushed the change.

**Metrics:**
- Error budget = (1 - objective) x window minutes = 0.005 x 43,200 = 216 minutes.
- Budget remaining = budget - downtime so far (70 + 95 + 40) = 11 minutes.
- Burn rate = observed bad-minute rate / allowed rate; a full outage is 200x (1 / 0.005).
- Time to detect and time to mitigate per outage (the two parts we can shorten).
- Guardrail: change-failure rate of releases during a freeze must be zero for non-essential changes.

**Risks:**
- Shipping a rushed fix to "save budget" can create a longer outage.
- The numbers are only as good as the outage clock: when did it start, when did users see it?
- A freeze with no end date makes teams hide risky work. Write the exit rule (budget back above a level, for example 20%).
- An internal objective is not an SLA; do not promise customers more than the contract says.

**What the interviewer scores:**
- Strong: gets 11 minutes, 5.1%, and notices the current outage is still burning budget.
- Strong: balances speed and caution: small, reversible fix with explicit rollback criteria.
- Strong: freeze with owner and exit rule; blameless review of a pattern of three outages.
- Weak: "we have budget left, so keep releasing"; or "fix it immediately for everyone" with no rollback plan.

**Example:** Illustrative. Weak versus strong:
- Weak: "We have used 165 minutes, so we are fine, I will push the fix to everyone."
- Strong: "Counting the live outage we have used 205 of 216, so 11 minutes are left, about 5%. At full outage that is gone in 11 minutes. I would stop all other releases, push the fix to 10% first, and roll back if errors rise above baseline. After this, we hold a blameless review of the three outages together."

**Code:**
```python
slo = 0.995
month_min = 30 * 24 * 60
budget = month_min * (1 - slo)
assert month_min == 43200 and round(budget) == 216
used_done = 70 + 95
current = 40
left = budget - used_done - current
print("budget:", round(budget), "min | used incl. current:", used_done + current, "| left:", round(left))
assert round(left) == 11 and used_done + current == 205
print("share left:", round(left / budget * 100, 1), "%")
assert round(left / budget * 100, 1) == 5.1

# Outage still going at full downtime: 1 budget minute burns per wall minute
print("budget gone at outage minute", current + round(left), "(11 more minutes)")
assert current + round(left) == 51
# Availability if the outage ends at various points (30-day window)
for extra in (0, 11, 30, 60):
    down = used_done + current + extra
    print(f"outage ends after {current + extra} min -> availability {100 * (1 - down / month_min):.3f}% (budget left {budget - down:+.0f})")
assert round(100 * (1 - (205 + 30) / month_min), 3) == 99.456
# Rolling window: the 95-minute outage leaves the window when it is >30 days old (editor reasoning)
# Burn rate of a full outage vs the sustainable rate
burn = 1 / (1 - slo)
print("burn rate of a full outage:", round(burn), "x the sustainable rate")
assert round(burn) == 200
```

**Output (my run):**
```
budget: 216 min | used incl. current: 205 | left: 11
share left: 5.1 %
budget gone at outage minute 51 (11 more minutes)
outage ends after 40 min -> availability 99.525% (budget left +11)
outage ends after 51 min -> availability 99.500% (budget left +0)
outage ends after 70 min -> availability 99.456% (budget left -19)
outage ends after 100 min -> availability 99.387% (budget left -49)
burn rate of a full outage: 200 x the sustainable rate
```

**Follow-ups:**
- The budget is gone; what now? Freeze non-essential releases, spend engineering time on reliability work, and report the breach, until the window recovers.
- Is a partial outage counted? Yes, in proportion to failing requests; use a request-based SLI if you can.
- Should the model be rolled back if only the fix is uncertain? Roll back when the previous version is known good and the outage began after the change; otherwise fix forward in small steps.

**Common mistakes:**
- Forgetting to include the outage still in progress.
- Treating a 30-day budget as resetting weekly.
- Shipping the fix to 100% with no rollback criteria.
- Blaming the engineer who deployed.

### Q12 ⭐⭐⭐ 🟡 Your LLM provider starts returning rate-limit or server errors on 25% of calls at a traffic of 40 original requests per second, which is 10 failed calls per second. The client retries immediately up to 3 times, and a second provider is wired as a fallback but has never been used in production. What do you do in the first 30 minutes, and what could go wrong with the fallback itself?
**Asked at:** LLM-serving resilience pages (getmaxim, TrueFoundry, tianpan and Statsig pages on retries, 429 handling, fallbacks, circuit breakers and cost during failover; one snippet notes that silent quality degradation is invisible to HTTP success rates); practitioner material, no confirmed interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** Stop making it worse (no immediate retries, add backoff with jitter and a retry budget), then shift traffic to the fallback in small steps while checking its limits and its answers, because a fallback never used in production is untested.

**Clarifying questions:**
- Are the errors 429 (rate limit) or 5xx (provider trouble)? A 429 means our own volume matters; a 5xx means the provider is hurt and retries only add load.
- Does the provider status page or our own account dashboard show a quota issue on our side? It decides whether to ask for more quota or leave.
- What is the fallback's quota, prompt compatibility, price and data-handling agreement? Switching can break a contract or a privacy promise.
- How tolerant is the product of a slightly different answer (a support chatbot versus a structured JSON extractor)? It sets how much traffic can move.
- Is there a cached or rule-based degraded mode? It is the safest third option.

**Approach:**
1. First 15 minutes: confirm the error type from logs, post a status line, and cut the retry amplification. Immediate retries add load: with 25% failing and up to 3 retries, 40 calls per second becomes about 53 offered calls per second (+33%). If the cause is a hard rate cap, retries are worse (see the run: a crude model collapses).
2. Replace immediate retries with exponential backoff and jitter, honour `Retry-After` if present, and cap retries at about 10% extra calls (a retry budget). Add a circuit breaker: after a run of failures, stop calling for a short time.
3. First 30 minutes: ramp the fallback: 5% of traffic, then 10%, then 25%, watching its error rate, latency, token cost and a quality check (JSON validity, a small canned evaluation set, thumbs-down rate). Do not flip 100% at once.
4. Escalate to the incident lead and the vendor contact at about minute 15 if error rate is still above 10%. Roll the fallback back if its error rate is above the primary's, its output fails the validity check more than a small margin (for example 2% absolute), or cost per call exceeds the pre-agreed ceiling.
5. Shed or degrade low-value traffic (batch jobs, background summaries) first and keep interactive users.
6. First day: restore the primary slowly (ramp 10, 25, 50, 100%) so we do not trigger the limit again. Confirm customers who got fallback answers were not harmed (a different model, different language, different safety behaviour).
7. Next quarter: run a fallback game day twice a year, keep the fallback warm with 1 to 5% real traffic, write prompts and tests that pass on both providers, negotiate quota in both accounts, and add a per-provider SLO.
8. Blameless postmortem: "the fallback had never been used" is the finding, not a person. Action items: warm traffic, quota check, retry budget in the client library.

**Metrics:**
- Failure rate = failed calls / all calls (here 10 / 40 = 25%).
- Retry amplification = total calls sent / original requests (1.33 under independent failures at 25%).
- Goodput = successful calls per second; compare before and after.
- Final failure rate after retries (user-visible): 0.25^4 = 0.39% if failures were independent, but rate limits are not independent.
- Fallback guardrails: error rate, p95 latency, cost per 1,000 calls, output validity rate.

**Risks:**
- The fallback has its own quota; moving 100% of traffic may just move the outage.
- Different model means different tone, formatting, refusals and cost; silent quality loss does not show in HTTP success.
- A different region or vendor may break a data-residency or privacy commitment.
- Prompt and tool-calling formats may not match (editor knowledge: providers differ in function-call formats).
- Retry storms: many clients retry at the same moment unless jittered.

**What the interviewer scores:**
- Strong: names retry amplification and gives the number; adds backoff, jitter, retry budget and a circuit breaker.
- Strong: ramps the fallback with checks for quota, cost and quality, and has rollback criteria.
- Strong: first 15 minutes, first day and next quarter are separate; blameless action items.
- Weak: "switch to the backup" with no ramp; "increase retries".

**Example:** Illustrative numbers. Weak versus strong:
- Weak: "I would retry more times and, if that fails, point everything to the other provider."
- Strong: "First I stop the immediate retries, because they push 40 calls a second to about 53. Then backoff with jitter and a 10% retry budget. I send 10% of traffic to the second provider and check its quota, cost and answer validity before 25%. If its error rate is worse than the primary's or JSON validity drops by more than 2 points, I send traffic back and shed batch work instead."

**Code:**
```python
import math

rate, f0 = 40, 0.25
failed = rate * f0
assert failed == 10
# Immediate retries (max 3), independent failures at 25%: calls per request
calls_per_req = sum(f0 ** k for k in range(4))
offered = rate * calls_per_req
print("calls per request:", round(calls_per_req, 4), "| offered calls/s:", round(offered, 1))
assert round(calls_per_req, 4) == 1.3281 and round(offered, 1) == 53.1
print("requests failing for good if independent:", round(f0 ** 4 * 100, 2), "%")
assert round(f0 ** 4 * 100, 2) == 0.39

# But a rate limit is not independent. Model: provider accepts L calls/s, rest rejected.
# 25% failing at 40/s means L = 30 (assumption for a 429-style limit).
L = 30
assert L == rate * (1 - f0)
f = f0
for _ in range(200):                      # fixed point of f = 1 - L / offered(f)
    tot = rate * sum(f ** k for k in range(4))
    f = max(0.0, 1 - L / tot)
tot = rate * sum(f ** k for k in range(4))
final_fail = f ** 4
print("with a hard cap of 30/s: attempt failure", round(f * 100, 1), "% | offered", round(tot, 1), "calls/s | requests lost", round(final_fail * 100, 1), "%")
assert 0.70 < f < 0.72 and tot > 100 and abs(final_fail - 0.25) < 0.01

# Retry budget (10% extra calls) + jittered backoff keeps offered load near 40 * 1.1
budget_calls = rate * 1.10
print("with a 10% retry budget: offered at most", budget_calls, "calls/s; the provider still serves only", L, "so goodput is unchanged")
assert budget_calls == 44.0
print("goodput: no retries", min(rate, L), "| 3 immediate retries", L, "| both 30/s, retries only add 62 extra calls/s of load")
assert round(tot - rate) == 62
# Fallback ramp: send 10% of traffic first, check its limit
fb_limit = 20          # illustrative: fallback account allows 20 calls/s (never tested)
print("fallback at 100% would need", rate, "calls/s vs limit", fb_limit, "-> would reject", rate - fb_limit, "/s")
assert rate - fb_limit == 20
print("fallback at 25% needs", rate * 0.25, "calls/s, inside the limit")
assert rate * 0.25 <= fb_limit
```

**Output (my run):**
```
calls per request: 1.3281 | offered calls/s: 53.1
requests failing for good if independent: 0.39 %
with a hard cap of 30/s: attempt failure 70.7 % | offered 102.4 calls/s | requests lost 25.0 %
with a 10% retry budget: offered at most 44.0 calls/s; the provider still serves only 30 so goodput is unchanged
goodput: no retries 30 | 3 immediate retries 30 | both 30/s, retries only add 62 extra calls/s of load
fallback at 100% would need 40 calls/s vs limit 20 -> would reject 20 /s
fallback at 25% needs 10.0 calls/s, inside the limit
```

**Follow-ups:**
- Why does the fallback need a small ramp? It may have a lower limit (here 20 calls per second against 40 needed); a ramp finds that safely.
- How do you detect silent quality loss? Compare output validity and a golden test set on fallback traffic, and sample outputs for review; HTTP 200 does not tell you.
- Should clients retry 429s? Only after the `Retry-After` time and within a budget; otherwise slow down or shed.

**Common mistakes:**
- Increasing retries during a rate-limit incident.
- Switching 100% to a never-tested fallback.
- Ignoring cost and data-handling differences.
- No rollback criteria for the fallback.

### Q13 ⭐⭐⭐ 🔴 A recommender retrains weekly on clicks from its own recommendations. Over six weeks the share of impressions going to the top 1% of items rose from 35% to 52% (absolute points, of all impressions), while click-through on the whole page is flat. Explain the loop, how you would prove it with the data you have, and what you would change in logging and training. Which metric would you track from now on?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to feedback loops and exposure bias in ML system design material; related topics appear in public MLOps guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** The model learns from clicks it caused by showing those items, so popular items get more exposure, more clicks and a higher score next week; I prove it with a small random-exposure slice and fix it with exploration, propensity logging and exposure-aware training.

**Clarifying questions:**
- Is the 52% a share of impressions (as stated, 17 absolute points up from 35%) and of all slots or only the first screen? Position matters because top slots get most attention.
- Did the catalogue change (a new hit release, a seasonal event)? A real hit also raises the top share without any loop.
- Are impressions and positions logged for each click? Without them we cannot separate exposure from appeal.
- Is any traffic shown randomly or with a different ranker today? That slice is the cleanest evidence.
- What is the business goal (clicks now, long-term retention, creator fairness)? A flat page CTR with a narrower catalogue can still hurt long-term.

**Approach:**
1. Explain the loop in two sentences: items shown more get more clicks, and a model trained on clicks scores them higher, so they are shown more. Clicks measure exposure times appeal, but the model reads them as appeal.
2. Prove it with the data you have:
   - Plot top-1% impression share by week against the retrain dates; the rise should follow retrains, not the catalogue.
   - Compare click-through for the same items at the same position, early versus late weeks. If exposure rose and CTR at fixed position did not, the model is not finding better items.
   - Look at items whose exposure rose most: were they already ahead six weeks ago (rich get richer)? Use a rank correlation between last month's clicks and this week's exposure.
   - If any random or exploration traffic exists, compute CTR there. In my simulation the top items had 11,939 impressions each against 81 for the others, yet their CTR in a random slice was 6.0%, the same as the catalogue's 6.05%: exposure rose without appeal rising.
3. Logging fix: log position, the candidate set, the model score and the probability the item was shown (propensity). Keep a 1 to 2% randomised exploration slice as a permanent measuring stick.
4. Training fix: weight clicks by inverse propensity (clipped), or add a position feature trained away at serving; add exploration (epsilon or a bandit); hold out the exploration slice for evaluation. Monitor exposure and quality, not only clicks.
5. Rollback and escalation: if the top-1% share exceeds a ceiling agreed with product (for example 55%) or tail-item coverage drops below a floor, hold the retrain and serve the previous model plus exploration; escalate to the product owner because it trades short-term clicks for long-term health.
6. First 15 minutes does not apply (no outage); first week: logging and the exploration slice. Next quarter: counterfactual evaluation, exposure caps, a creator and catalogue-health dashboard.
7. Blameless angle: the system optimised the metric we gave it; the gap is in what we measured. Action item: add an exposure metric to the retrain gate.

**Metrics:**
- Top-1% exposure share = impressions on the top 1% of items by impressions / all impressions (35% to 52% is 17 absolute points, about 1.49x).
- Catalogue coverage = items with at least N impressions / catalogue size; Gini or entropy of exposure.
- Exploration-slice CTR by item group (unbiased because exposure is random).
- Page CTR (flat) as a guardrail, plus a long-term metric such as 30-day return rate.

**Risks:**
- Top share also rises from genuine quality or a real hit; the exploration slice is what separates them.
- Exploration costs short-term clicks; size it (1 to 2%) and tell the business.
- Inverse-propensity weights have high variance when propensities are tiny; clip them.
- Flat page CTR can hide harm to new creators and cold-start items.

**What the interviewer scores:**
- Strong: states the loop, then proves it with data (fixed position, exploration slice), not only a story.
- Strong: fixes logging first (propensity, position), then training, and picks an exposure metric.
- Strong: considers alternative explanations.
- Weak: "just add diversity" with no measurement; or "the model is fine because CTR is flat".

**Example:** Illustrative simulation: 1,000 items with nearly equal appeal, weekly retrains on last week's clicks. Top-1% share goes from 27% to 53% over six weeks while page CTR stays about 6.0% to 6.2%. Weak versus strong:
- Weak: "CTR is flat, so nothing is wrong."
- Strong: "CTR is flat because appeal did not change; only who gets shown did. In a random slice the top items click at 6.0%, the same as everything else. I would log propensities, keep a 2% random slice, weight training by inverse propensity, and track top-1% share and coverage next to CTR."

**Code:**
```python
import numpy as np

assert 52 - 35 == 17 and round(52 / 35, 2) == 1.49    # absolute points, relative growth
rng = np.random.default_rng(13)
N, weeks, imps = 1000, 6, 200_000                    # 1,000 items, 200k impressions a week
top = N // 100                                       # top 1% = 10 items
quality = rng.beta(400, 6000, N)                         # TRUE click appeal, independent of popularity
quality /= quality.mean() / 0.06                     # average CTR about 6%
pop = rng.gamma(0.1, 1.0, N)                         # initial popularity (clicks last week)
EXPLORE = 0.02                                       # 2% of impressions shown uniformly at random (logged)

def week(pop, power=1.12):
    p = pop ** power; p /= p.sum()
    p = (1 - EXPLORE) * p + EXPLORE / N              # mix random exposure
    shown = rng.multinomial(imps, p)
    clicks = rng.binomial(shown, quality)
    return shown, clicks, p

shares, ctrs = [], []
for w in range(weeks):
    shown, clicks, p = week(pop)
    s = np.sort(shown)[::-1][:top].sum() / imps
    shares.append(s); ctrs.append(clicks.sum() / imps)
    # explore slice only: propensity is 1/N for everyone
    pop = clicks + 1.0                               # retrain: "popularity" = last week's clicks
print("top-1% impression share by week:", [round(float(x) * 100) for x in shares])
print("page CTR by week (%):", [round(float(x) * 100, 2) for x in ctrs])
assert shares[-1] > shares[0] + 0.10                 # concentration rises by >10 points
assert max(ctrs) - min(ctrs) < 0.004                 # page CTR roughly flat (under 0.4 points)

# Proof with the data: naive CTR (clicks/impressions) of top items vs their CTR in the random slice
shown, clicks, p = week(pop)
ids = np.argsort(-shown)[:top]
naive = clicks[ids].sum() / shown[ids].sum()
exp_n = int(imps * EXPLORE)
ex_shown = rng.multinomial(exp_n, np.full(N, 1 / N))     # re-draw the random slice for these items
ex_clicks = rng.binomial(ex_shown, quality)
explore_ctr_top = ex_clicks[ids].sum() / ex_shown[ids].sum()
explore_ctr_all = ex_clicks.sum() / ex_shown.sum()
true_top = quality[ids].mean()
print("top items: naive CTR", round(float(naive) * 100, 2), "% | random-slice CTR", round(float(explore_ctr_top) * 100, 2), "% | all items random-slice", round(float(explore_ctr_all) * 100, 2), "% | true mean quality of those items", round(float(true_top) * 100, 2), "%")
assert abs(explore_ctr_all - quality.mean()) < 0.003   # random slice is an unbiased view of the catalogue
# Exposure per item in the final week: top items vs the rest
print("avg impressions per top item:", int(shown[ids].mean()), "| per other item:", int(np.delete(shown, ids).mean()))
assert shown[ids].mean() > 10 * np.delete(shown, ids).mean()
# Metric to track: top-1% exposure share + Gini of exposure
x = np.sort(shown); g = (2 * np.arange(1, N + 1) - N - 1) @ x / (N * x.sum())
print("final-week exposure Gini:", round(float(g), 2))
assert 0 < g < 1
```

**Output (my run):**
```
top-1% impression share by week: [27, 30, 35, 40, 46, 53]
page CTR by week (%): [6.0, 6.05, 6.02, 6.01, 6.13, 6.2]
top items: naive CTR 6.3 % | random-slice CTR 6.0 % | all items random-slice 6.05 % | true mean quality of those items 6.13 %
avg impressions per top item: 11939 | per other item: 81
final-week exposure Gini: 0.86
```

**Follow-ups:**
- Why not just boost the tail? Boosting without measurement may show worse items; use exploration to learn their real appeal first.
- What if you cannot randomise at all? Use position-debiasing with logged propensities, or natural experiments such as ranker changes; weaker evidence.
- Is the simulation proof? It shows the mechanism is possible; your real proof is the data comparison in step 2.

**Common mistakes:**
- Reading clicks as pure appeal.
- No logging of what was shown, only what was clicked.
- Adding diversity with no metric.
- Treating a flat CTR as success.

### Q14 ⭐⭐⭐ 🔴 A canary takes 5% of 40,000 requests in its first hour, which is 2,000 requests, with only 9 errors (0.45%), while the control's 38,000 requests had 76 errors (0.2%). Compute whether the gap is bigger than sampling noise, and say what you do at this point and what you would have wanted written down before the canary started. How does the answer change if the errors are all in one customer segment?
**Asked at:** MLOps interview guides (startup.jobs, Hyring, kore1, refresh.cv, wecreateproblems and Yardstick pages list rollback, canary versus blue/green versus shadow, and 'tell me about an urgent production incident' prompts, and one 2026 guide says the strongest questions test custody of a live model); practitioner and prep-site material rather than a confirmed employer round; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** The gap is borderline (z = 2.37, Fisher p about 0.04, with a lower interval end barely above zero), so I do not promote and do not panic: I hold the canary at 5%, inspect the errors, and decide by the rollback rule that should have been written before the canary started.

**Clarifying questions:**
- What kind of errors are they (5xx, timeouts, invalid output, wrong predictions)? A crash is a stop; a rare validation error may be a data issue.
- Are errors independent requests or clustered by customer, region or one bad input? Clusters shrink the real sample size.
- Is the control the same hour and traffic mix as the canary? Differences in mix create gaps without any model effect.
- What threshold did we agree before the canary started, and how long should it run? It decides whether this hour is a signal.
- How costly is one error (an annoyed user versus a failed payment)? It sets how tight the limit is.

**Approach:**
1. Compute the gap: canary 9 / 2,000 = 0.45%, control 76 / 38,000 = 0.20%, a difference of 0.25 percentage points, relative risk 2.25. The expected canary errors if it were the same as control: 2,000 x 0.002 = 4.
2. Test it: pooled z = 2.37, two-sided p about 0.018; Fisher exact p about 0.039 (better with small counts). A 95% interval for the gap (Newcombe-style) is 0.03 to 0.66 points: the lower end barely clears zero. So: probably real, imprecise, and 9 errors is a small count.
3. Be careful about looking: one test is at 5% false alarm; six hourly looks give about 26% chance of at least one false alarm if you act on every p below 0.05. Use the pre-agreed rule rather than the first p-value.
4. Action now (first 15 minutes): do not ramp to 25%. Hold at 5%, pull the 9 error logs and see their type, customer and input. Page the model owner. If any error is a crash, wrong-data or safety-relevant, roll back immediately; a statistical test is not needed for that.
5. If the errors look random (timeouts), extend the canary for a pre-agreed time (for example 4 more hours, or until about 20 expected control-rate errors) and decide by the written rule: roll back if the canary error rate is above control by more than 0.3 points absolute with the interval above zero, or if p99 latency worsens by more than 20%.
6. All errors in one segment: test within the segment (the run uses an illustrative segment that is 2% of traffic: 9 of 40 canary requests failed, 22.5%, against 4 of 760 for control, 0.53%, p about 5e-10), while the rest of the traffic shows 0 canary errors against 3.8 expected. This is a segment bug, not a diffuse increase. Action: route that segment to control, keep the canary elsewhere, and fix. If the segment is a key customer or regulated, roll the whole canary back.
7. First day: root-cause the errors and decide fix-and-retry or discard. Next quarter: automatic canary analysis with stratified checks, minimum sample size, and a rule template.
8. Blameless postmortem angle: the issue is not who shipped the model; it is whether the rule existed and was followed. Note what the rule did not say (segment checks, duration).

**Metrics:**
- Error rate = errors / requests per arm; absolute and relative gap with an interval.
- Written before: minimum requests per arm, metrics (error rate, p99, business metric), maximum acceptable absolute gap, segments to check, duration, who decides, and rollback criteria.
- Guardrails: p99 latency, timeout rate, a prediction-distribution check, and a segment breakdown.

**Risks:**
- Significance is not importance: 0.25 points may be tolerable, or may be a failed payment each.
- With 9 events, the pooled z and exact test can disagree; the unpooled Wald interval would include zero. Say so.
- Requests from one user or retry loop are not independent.
- Peeking and many segments produce false alarms; control with a pre-set plan.

**What the interviewer scores:**
- Strong: computes both rates, z and an exact check, and says "borderline, imprecise" instead of over-claiming.
- Strong: says what is written before: thresholds, sample size, segments, duration, owner.
- Strong: handles the segment case by stratifying and routing the segment, not averaging.
- Weak: "p is below 0.05 so roll back" or "0.45% is tiny so ramp up".

**Example:** Illustrative. Weak versus strong:
- Weak: "0.45% versus 0.2% is small, so I would go to 25%."
- Strong: "That is 9 against 4 expected, a gap of 0.25 points, z about 2.4. It is borderline with a tiny count, so I hold at 5% and read the 9 errors. If they are one segment, I route that segment back and fix it; if they look like noise I extend until the written sample size and decide by the pre-agreed rule."

**Code:**
```python
import math
from scipy import stats

xc, nc, xt, nt = 9, 2000, 76, 38000
assert nc == 0.05 * 40000 and nt == 40000 - nc
assert xc / nc == 0.0045 and xt / nt == 0.002
diff = xc / nc - xt / nt
p = (xc + xt) / (nc + nt)
se = math.sqrt(p * (1 - p) * (1 / nc + 1 / nt))
z = diff / se
p2 = 2 * (1 - stats.norm.cdf(z))
print(f"diff {diff*100:.2f} points | pooled z {z:.2f} | two-sided p {p2:.3f}")
assert round(z, 2) == 2.37 and round(p2, 3) == 0.018
odds, pf = stats.fisher_exact([[xc, nc - xc], [xt, nt - xt]])
print(f"Fisher exact p {pf:.3f} | relative risk {(xc/nc)/(xt/nt):.2f}")
assert pf < 0.05 and round((xc / nc) / (xt / nt), 2) == 2.25
# Newcombe-style interval from Wilson intervals for each arm
def wilson(x, n, zc=1.96):
    ph = x / n; d = 1 + zc**2 / n
    c = (ph + zc**2 / (2 * n)) / d; h = zc * math.sqrt(ph * (1 - ph) / n + zc**2 / (4 * n * n)) / d
    return c - h, c + h
l1, u1 = wilson(xc, nc); l2, u2 = wilson(xt, nt)
lo = diff - math.sqrt((xc/nc - l1)**2 + (u2 - xt/nt)**2)
hi = diff + math.sqrt((u1 - xc/nc)**2 + (xt/nt - l2)**2)
print(f"95% interval for the gap: {lo*100:.2f} to {hi*100:.2f} points")
assert 0 < lo < 0.001 and 0.006 < hi < 0.007   # lower end barely clears zero
# Unpooled Wald interval disagrees with the pooled z: it includes zero
se_u = math.sqrt(xc/nc*(1-xc/nc)/nc + xt/nt*(1-xt/nt)/nt)
print(f"Wald interval: {(diff-1.96*se_u)*100:.2f} to {(diff+1.96*se_u)*100:.2f} points")
assert diff - 1.96 * se_u < 0
# Sample per arm to detect 0.2% vs 0.3% (80% power, 5% two-sided)
n_arm = (1.96 + 0.8416) ** 2 * (0.002 * 0.998 + 0.003 * 0.997) / 0.001 ** 2
print("requests per arm for 0.2% vs 0.3%:", round(n_arm))
assert 30_000 < n_arm < 50_000
# Expected canary errors if the canary were no worse: 2000 * 0.002 = 4
assert nc * xt / nt == 4.0
# Peeking: hourly looks for 6 hours inflate false alarms (independent-look approximation)
print("false-alarm chance over 6 looks at 5%:", round((1 - 0.95**6) * 100, 1), "%")
assert round((1 - 0.95**6) * 100, 1) == 26.5

# Segment case (illustrative split): segment A is 2% of traffic
segA_c, segA_t = 40, 760
a_err_c, a_err_t = 9, 4
print("segment A: canary", a_err_c, "/", segA_c, "=", round(a_err_c/segA_c*100, 1), "% vs control", a_err_t, "/", segA_t, "=", round(a_err_t/segA_t*100, 2), "%")
_, pA = stats.fisher_exact([[a_err_c, segA_c - a_err_c], [a_err_t, segA_t - a_err_t]])
rest_c, rest_t = nc - segA_c, nt - segA_t
rest_ec, rest_et = xc - a_err_c, xt - a_err_t
print("rest of traffic: canary", rest_ec, "/", rest_c, "vs control", rest_et, "/", rest_t, "=", round(rest_et/rest_t*100, 3), "%")
exp_rest = rest_c * rest_et / rest_t
print(f"segment A p {pA:.1e} | rest of traffic: canary errors 0 vs {exp_rest:.1f} expected from control rate")
assert pA < 1e-6 and rest_ec == 0 and round(exp_rest, 1) == 3.8
```

**Output (my run):**
```
diff 0.25 points | pooled z 2.37 | two-sided p 0.018
Fisher exact p 0.039 | relative risk 2.25
95% interval for the gap: 0.03 to 0.66 points
Wald interval: -0.05 to 0.55 points
requests per arm for 0.2% vs 0.3%: 39143
false-alarm chance over 6 looks at 5%: 26.5 %
segment A: canary 9 / 40 = 22.5 % vs control 4 / 760 = 0.53 %
rest of traffic: canary 0 / 1960 vs control 72 / 37240 = 0.193 %
segment A p 4.8e-10 | rest of traffic: canary errors 0 vs 3.8 expected from control rate
```

**Follow-ups:**
- Why not just roll back to be safe? You may; the cost of a rollback is low. But you need a rule so you do not roll back on noise every time, and you need the root cause either way.
- How big a sample is needed? Large enough to detect the gap you care about (for 0.2% versus 0.3%, tens of thousands of requests per arm; compute with a power calculation).
- What about a business metric? Errors are a guardrail; the decision also needs the primary metric over a full cycle.

**Common mistakes:**
- Trusting one p-value after one hour.
- Averaging over segments and hiding a localised failure.
- No pre-written rollback criteria.
- Treating requests as independent when one customer causes many.

### Q15 ⭐⭐⭐ 🔴 Retraining the same commit on the same table gave an AUC of 0.842 on the 10,000-row holdout (10% positives, 1,000 rows) in March and 0.829 in September, an absolute gap of 0.013, and an auditor asks you to reproduce the March model. Nobody pinned the library versions, the table is refreshed in place, and seeds were not logged. How do you find out how much of the gap is noise, what changed and what is unrecoverable, and what do you record from now on?
**Asked at:** Leakage and reproducibility material (arXiv 2207.07048 and 2311.04179 on leakage, an Omdena post on silent ML failures and label timing, an arXiv 2025 paper on reproducible ML infrastructure); research and practitioner pages rather than an interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** A 0.013 AUC gap on a 10,000-row holdout is about 1.2 standard errors if the holdouts differ (1,000 positives), so first measure seed and sampling noise; then recover what you can (lockfile history, image digests, warehouse snapshots), say plainly what is unrecoverable, and record everything from now on.

**Clarifying questions:**
- How many positives are in the holdout, and is it the same 10,000 rows in March and September? Standard error depends on positives (1,000 here, a 10% rate), and the same rows allow a paired comparison.
- Does the auditor need the exact model or evidence the process was controlled? These are different deliverables.
- Is there any snapshot: warehouse time travel, backups, exported training files, or a feature log? It decides what is recoverable.
- Do we still have the container image, CI logs, or a `pip freeze` somewhere? Library versions can often be rebuilt from those.
- Which model version is in production, and which one was approved? A reproduction effort for an unused model is lower priority.

**Approach:**
1. Estimate noise. Hanley-McNeil standard error of one AUC at 0.842 with 1,000 positives and 9,000 negatives is about 0.008; for a gap between two independent holdouts the standard error is about 0.011, so 0.013 is about 1.2 standard errors: not strong evidence of any real change. A bootstrap on simulated scores gave a similar scale (0.006 for one AUC). With the same rows and paired scores the noise would be smaller.
2. Measure seed noise: retrain the current code 20 or more times with different seeds on a frozen snapshot and look at the spread. For a stable linear model it is tiny (0.0003 in my run); for deep or boosted models it can be larger. Report the range.
3. Find what changed: diff the lockfile or `pip freeze` history in git, base image digests, CI logs, and the data (row counts, label rates, null rates by month). Run the old code with the oldest plausible library versions in a clean environment.
4. Classify honestly: recoverable (code commit, many library versions, data if the warehouse retains history); partly recoverable (library versions inferred); unrecoverable (in-place table state, unlogged seeds). Do not claim exact reproduction. Offer the auditor: an approximately equivalent model, a confidence interval for its metrics, and the evidence of the gap analysis.
5. Rollback and escalation: if the September model is already serving and its metrics on a frozen shared holdout are within noise of March, no rollback; if they are below the noise band, escalate to the model owner and compliance before the audit response.
6. First 15 minutes of the request: do not retrain over anything; preserve the current table state (copy or snapshot) and logs. First day: snapshot, freeze versions, run the noise study. Next quarter: immutable data snapshots, lockfiles and image digests per run, seed logging, and a run record.
7. Blameless angle: no process required this; the gap is in the platform, not in whoever ran the retrain. Action items: run record, data versioning, and a reproducibility test that retrains monthly and alarms if the metric moves by more than the noise band.

**Metrics:**
- AUC with a confidence interval (Hanley-McNeil or bootstrap), not a point value.
- Seed spread = standard deviation of AUC across seeds on a frozen snapshot.
- Reproducibility gap = metric of the reproduction minus the reference, compared to the noise band.
- Record completeness = share of runs with data id, code commit, lockfile, seed and environment logged.

**Risks:**
- A significant-looking difference between two retrains can be noise; the opposite risk is dismissing a real shift when the data changed.
- In-place refresh may have changed labels or dropped rows; the AUC gap could be a real population change.
- Claiming reproduction without proof is an audit failure.
- Unpinned libraries can change defaults (editor knowledge: a default solver, a tie-breaking rule).

**What the interviewer scores:**
- Strong: quantifies noise with a standard error and a seed study before explaining the gap.
- Strong: separates recoverable from unrecoverable and tells the auditor the truth.
- Strong: concrete record list and a test that would catch the problem.
- Weak: "set the seed and rerun" or "the model degraded"; claiming exact reproduction.

**Example:** Illustrative: AUC 0.842 in March, 0.829 in September, gap 0.013, 1,000 positives. Weak versus strong:
- Weak: "The September model is worse; I will retrain with a fixed seed to get March back."
- Strong: "With 1,000 positives the standard error of the gap is about 0.011, so this is about 1.2 standard errors. I would rerun with 20 seeds on a frozen snapshot to see the seed spread, rebuild the old library versions from CI logs, and tell the auditor which parts I can reproduce and which, like the in-place table and the unlogged seeds, I cannot. From now on each run stores a data snapshot id, lockfile, image digest and seed."

**Code:**
```python
import numpy as np

assert round(0.842 - 0.829, 3) == 0.013
rng = np.random.default_rng(15)
n, pos_rate = 10_000, 0.10                     # 10% positives, as stated
npos = int(n * pos_rate); nneg = n - npos
assert (npos, nneg) == (1000, 9000)

# Hanley-McNeil standard error of one AUC
def hm_se(auc, npos, nneg):
    q1 = auc / (2 - auc); q2 = 2 * auc * auc / (1 + auc)
    v = (auc * (1 - auc) + (npos - 1) * (q1 - auc**2) + (nneg - 1) * (q2 - auc**2)) / (npos * nneg)
    return v ** 0.5
se1 = hm_se(0.842, npos, nneg)
print("Hanley-McNeil SE of one AUC:", round(se1, 4))
assert round(se1, 3) == 0.008
se_diff_indep = (2 * se1 ** 2) ** 0.5
print("SE of the gap if two different holdouts:", round(se_diff_indep, 4), "| gap/SE:", round(0.013 / se_diff_indep, 2))
assert 0.010 < se_diff_indep < 0.013 and 1.0 < 0.013 / se_diff_indep < 1.4

# Simulate: scores with AUC about 0.84, bootstrap SE of AUC and a seed-noise check on a tiny model
def auc(y, s):
    r = s.argsort().argsort() + 1
    return (r[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg)
y = np.r_[np.ones(npos), np.zeros(nneg)].astype(int)
s = np.r_[rng.normal(1.4, 1, npos), rng.normal(0, 1, nneg)]
a0 = auc(y, s)
boots = []
for _ in range(300):
    i = rng.integers(0, n, n); yy, ss = y[i], s[i]
    k1 = yy.sum(); k0 = n - k1
    r = ss.argsort().argsort() + 1
    boots.append((r[yy == 1].sum() - k1 * (k1 + 1) / 2) / (k1 * k0))
print("simulated AUC", round(a0, 3), "| bootstrap SE", round(float(np.std(boots)), 4))
assert 0.005 < np.std(boots) < 0.011

# Seed noise: logistic regression by gradient descent from random starts + row-order shuffles
X = np.c_[s, rng.normal(size=(n, 3))]
def fit(seed, steps=30):
    r = np.random.default_rng(seed); w = r.normal(0, 1, X.shape[1]); idx = r.permutation(n)
    for _ in range(steps):                       # a few SGD-style mini-batch steps, undertrained on purpose
        for b in np.array_split(idx, 20):
            p = 1 / (1 + np.exp(-(X[b] @ w))); w -= 0.05 * X[b].T @ (p - y[b]) / len(b)
    return auc(y, X @ w)
aucs = [fit(sd) for sd in range(10)]
print("seed-only spread over 10 fits: min", round(min(aucs), 4), "max", round(max(aucs), 4), "sd", round(float(np.std(aucs)), 4))
assert np.std(aucs) < 0.02
print("so a 0.013 gap is about", round(0.013 / se_diff_indep, 1), "SE: not strong evidence of real change from the data alone")
```

**Output (my run):**
```
Hanley-McNeil SE of one AUC: 0.0079
SE of the gap if two different holdouts: 0.0112 | gap/SE: 1.16
simulated AUC 0.843 | bootstrap SE 0.0063
seed-only spread over 10 fits: min 0.8411 max 0.842 sd 0.0003
so a 0.013 gap is about 1.2 SE: not strong evidence of real change from the data alone
```

**Follow-ups:**
- Is the gap real? Not provable from these two numbers; test on one shared frozen holdout with a paired bootstrap (see Book 4 Part 1, Q5, "How do you make a trained model reproducible six months later?", for the record list).
- What should the record contain? Data snapshot id or hash, code commit, lockfile and image digest, seeds, hardware, metrics with intervals, and the holdout id.
- Can you get exact reproducibility? Only with fixed data, versions, seeds and deterministic settings; some GPU operations are non-deterministic unless configured (editor knowledge, check your framework).

**Common mistakes:**
- Reading a 0.013 difference as real or as noise without computing the error.
- Updating a table in place without a snapshot.
- Logging seeds but not data or library versions.
- Telling an auditor "reproduced" when it was "similar".

### Q16 ⭐⭐ 🟢 During a shadow run the candidate's score differs from the production score by more than 0.05 on 3.2% of 500,000 requests, which is 16,000 requests, and the decision threshold is 0.5. The product owner asks whether it is safe to switch. What can a shadow run tell you and what can it not tell you, and how would you look at those 16,000 requests?
**Asked at:** MLOps interview guides (startup.jobs, Hyring, kore1, refresh.cv, wecreateproblems and Yardstick pages list rollback, canary versus blue/green versus shadow, and 'tell me about an urgent production incident' prompts, and one 2026 guide says the strongest questions test custody of a live model); practitioner and prep-site material rather than a confirmed employer round; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** A shadow run shows how the candidate behaves on real inputs (errors, latency, score differences, decision flips) but not what happens to outcomes or users, so 3.2% differing is a list to investigate, not a yes or no on the switch.

**Clarifying questions:**
- What is the decision threshold, and what does a score of 0.05 mean in decisions? Scores that differ without crossing the threshold may change nothing (0.5 here).
- Do we have delayed labels for the shadow period? If so we can compare accuracy, not just agreement.
- Is the shadow traffic the full mix (peak hours, all segments, edge cases)? A quiet weekday hides the bad cases.
- What is the cost of a wrong decision in each direction? It tells which flips matter.
- Did the shadow call the same features as production, or did it use a different feature path? Skew would make the comparison unfair.

**Approach:**
1. Say what shadow can tell: input handling on live data, error and timeout rate, latency under load, feature availability, score distribution, and how often the decision changes. It is risk-free for users because the candidate's output is not used.
2. Say what it cannot tell: whether the candidate is more accurate (no labels yet), how users react, effects on downstream systems or feedback loops, or behaviour once its own decisions change the data. It also may not reproduce production load if the candidate runs at lower priority.
3. Look at the 16,000: split by direction (candidate higher or lower), by decision flip at the threshold, and by segment, hour and feature missingness. In my simulation, 10,374 had the candidate higher and 5,626 lower; 3,087 (19% of the 16,000, 0.62% of all requests) flipped the decision at threshold 0.5.
4. Review a stratified sample: 200 from the flips and 200 from the non-flips; a 400-request review has a margin of error of about 4.9 points on a share. Where labels exist later, compare accuracy on the flips only: that is where the two models disagree about the action.
5. Decide with a rule: switch to a canary (not to 100%) if the flip count is explained, the flips are not concentrated in one risky segment, latency and errors are within budget, and the labelled comparison on flips is no worse. Do not switch if flips concentrate in a segment (for example new customers) without a reason, or if feature-missing rows dominate the differences.
6. First week: go to a canary with rollback criteria; next quarter: a standard promotion checklist including shadow metrics.
7. Blameless angle: no incident here, but if a past switch went wrong because shadow was treated as proof, write that down as a process gap.

**Metrics:**
- Difference rate = requests with |candidate - production| > 0.05 / all requests = 16,000 / 500,000 = 3.2%.
- Flip rate = requests whose decision changes at the threshold / all requests (0.62% in the run).
- Agreement on decisions = 1 - flip rate; accuracy on the flips once labels arrive.
- Guardrails: candidate error rate, p95 latency, feature-missing rate.

**Risks:**
- Treating 96.8% close scores as safety: the 3.2% might be the high-risk cases.
- Small score gaps can flip decisions near the threshold; a gap above 0.05 is not the same as a flip, and a gap under 0.05 can flip too. Check both.
- Shadow feeds the candidate from the same logs, so any feedback effect is invisible.
- Without labels, "different" does not mean "worse".

**What the interviewer scores:**
- Strong: separates what shadow shows (behaviour) from what it cannot (outcomes).
- Strong: moves from a count to decision flips and a stratified review.
- Strong: proposes the next step (canary) with criteria.
- Weak: "3.2% is low so it is safe" or "differences mean the new model is bad".

**Example:** Illustrative numbers. Weak versus strong:
- Weak: "Only 3.2% differ, so it is safe to switch."
- Strong: "Shadow tells me the candidate runs on live data. It does not tell me it is better. Of the 16,000, I would count how many cross the decision threshold, split by segment, and review 200 flips. If the flips are not concentrated and the candidate is no worse on labelled outcomes, I go to a 5% canary with rollback rules, not to 100%."

**Code:**
```python
import numpy as np

n, share = 500_000, 0.032
diff_n = round(n * share)
assert diff_n == 16_000
rng = np.random.default_rng(16)
thr = 0.50                                         # decision threshold, as stated
prod = rng.beta(2, 5, n)                           # production scores
cand = prod.copy()
idx = rng.choice(n, diff_n, replace=False)
sign = rng.choice([-1, 1], diff_n); mag = rng.uniform(0.051, 0.30, diff_n)
new = prod[idx] + sign * mag
sign = np.where((new < 0) | (new > 1), -sign, sign)       # flip direction instead of clipping
cand[idx] = prod[idx] + sign * mag
big = np.abs(cand - prod) > 0.05
assert big.sum() == diff_n
print("requests differing by more than 0.05:", int(big.sum()), f"({big.mean()*100:.2f}%)")
flip = (cand >= thr) != (prod >= thr)
print("decision flips at threshold 0.5:", int(flip.sum()), f"= {flip.sum()/n*100:.2f}% of all requests, {flip.sum()/big.sum()*100:.0f}% of the big diffs")
assert flip.sum() < big.sum()
up = (cand - prod)[big] > 0
print("candidate higher on", int(up.sum()), "| lower on", int((~up).sum()))
# Review sample: 400 of the 16,000 gives a margin of error of about 4.9 points at p = 0.5
m = 1.96 * (0.25 / 400) ** 0.5
print("margin of error for a 400-request review:", round(m * 100, 1), "points")
assert round(m * 100, 1) == 4.9
# Stratified plan: review the flips first (these change what the user sees)
print("review plan: 200 from the", int(flip.sum()), "flips + 200 from the", int(big.sum() - flip.sum()), "non-flip big diffs")
assert 200 < flip.sum() and 200 < big.sum() - flip.sum()
```

**Output (my run):**
```
requests differing by more than 0.05: 16000 (3.20%)
decision flips at threshold 0.5: 3087 = 0.62% of all requests, 19% of the big diffs
candidate higher on 10374 | lower on 5626
margin of error for a 400-request review: 4.9 points
review plan: 200 from the 3087 flips + 200 from the 12913 non-flip big diffs
```

**Follow-ups:**
- Can shadow replace a canary? No. Canary shows user and business effects; shadow shows technical behaviour.
- What if the product owner wants a yes today? Give a conditional yes for a 5% canary with a written stop rule.
- How do you evaluate with delayed labels? Join labels when they arrive, compare both models on the same requests, and use a paired comparison on the flips.

**Common mistakes:**
- Using agreement as accuracy.
- Looking only at average score difference.
- Ignoring segments and the decision threshold.
- Going from shadow straight to 100%.

### Q17 ⭐⭐ 🟢 A traffic burst made the autoscaler grow the GPU pool from 6 to 40 nodes, and scale-down was disabled during an earlier incident and never re-enabled, so the pool stayed at 40 nodes for 72 hours. A node costs an illustrative 3 per hour. Compute the extra cost and say how you find and prevent this kind of leftover emergency setting, and what a sensible scale-down policy looks like.
**Asked at:** GPU-serving and autoscaling pages (apxml and system-design.space on autoscaling and serving architecture; vendor pages from regolo.ai and lyceum.technology on cold starts and capacity, treated as vendor claims); no public postmortem located; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** The extra cost is 34 nodes x 72 hours x 3 = 7,344 over the 6-node baseline; I would re-enable scale-down in steps now, then make emergency overrides expire automatically and alert on node-hours so a leftover setting cannot sit for 72 hours.

**Clarifying questions:**
- What traffic does the pool need now? If it needs 8 nodes, scale to about 8 and not to the old 6; the baseline is not necessarily the target.
- Why was scale-down disabled (a thrashing bug, a node-drain problem, a model-load problem)? Re-enabling without fixing that cause repeats the first incident.
- Is "extra cost" measured against the baseline of 6 nodes or against a right-sized pool? I compute against 6 as the prompt says and note the fair-cost alternative.
- Are there reserved or committed nodes, so that the marginal cost is different? Then the extra cost is not a simple price times hours.
- Who can change autoscaler settings, and are changes tracked in code? It decides where the prevention goes.

**Approach:**
1. First 15 minutes: confirm the setting (the config says scale-down disabled), check the load and latency now, and open a short incident or change ticket. Do not drop 40 to 6 in one step.
2. Re-enable scale-down with a safe policy: a stabilisation window (for example 10 to 15 minutes of low utilisation), a maximum step of about 20% or 2 nodes per interval, a floor at the expected steady load, a scale-down trigger on sustained utilisation below a target, and protection for in-flight requests (drain). In the run, going from 40 to 8 nodes in 20% steps with 10-minute waits takes 8 steps, 80 minutes.
3. Watch p95 latency and error rate at each step. Roll back (stop and hold) if p95 rises by more than a set margin (for example 20%) or queue depth grows; escalate to the platform owner if scale-down triggers thrashing again. GPU nodes have slow model loads (editor knowledge), so keep a small warm buffer.
4. First day: compute the overspend with the billing data (7,344 vs baseline, or 6,720 versus the fair cost in my example where load needed 8 nodes after a 2-hour burst), and write the timeline. Revert any other emergency overrides: search config for "disabled", "override", "temporary".
5. Next quarter: make emergency overrides expire (a TTL or an expiry date in the config; the override reverts unless renewed), manage autoscaler config as code with drift detection (the live state differs from git, alert), add a cost alert on node-hours (for example 2x baseline for 4 hours), add an incident-closure checklist item "revert temporary changes", and a weekly pool-size versus request-rate panel.
6. Blameless postmortem: the person who disabled scale-down was acting under pressure to protect users. The gap is that a temporary change had no owner, no expiry and no alert. Detection delay was 72 hours; a 4-hour alert would have limited the extra cost to 408 (5.6% of 7,344).

**Metrics:**
- Extra cost = (nodes held - baseline nodes) x hours x cost per node-hour = 34 x 72 x 3 = 7,344.
- Utilisation = GPU busy time / available time per node; target set by the team.
- Detection delay for a stuck setting (72 hours here); target under 4 hours.
- Guardrails: p95 latency and error rate during scale-down, and a count of temporary overrides older than their expiry (target zero).

**Risks:**
- Scaling down too fast re-creates the original latency incident, since GPU cold starts are slow.
- A fair comparison is against the needed capacity, not always the old baseline.
- A TTL that silently reverts a needed override can cause its own outage; page the owner before expiry.
- Cost alerts that fire on every burst create fatigue; alert on sustained plateaus.

**What the interviewer scores:**
- Strong: correct arithmetic (7,344) and states what it is measured against.
- Strong: gradual scale-down with latency guardrails and a stop rule.
- Strong: expiry on emergency changes, drift detection, cost alert, closure checklist.
- Weak: "just turn autoscaling back on" at once; blaming the person.

**Example:** Illustrative at 3 per node-hour. Weak versus strong:
- Weak: "I would turn scale-down on and remind people to be careful."
- Strong: "The overspend is 34 extra nodes for 72 hours at 3, so 7,344. I turn scale-down back on in 20% steps with a 10-minute wait and watch p95. Then I give every emergency override an expiry, alert when node-hours stay above twice baseline for 4 hours, and add 'revert temporary changes' to the incident checklist. The postmortem is about the missing owner and expiry, not the engineer."

**Code:**
```python
nodes_burst, nodes_base, hours, cost = 40, 6, 72, 3
extra_nodes = nodes_burst - nodes_base
extra = extra_nodes * hours * cost
total = nodes_burst * hours * cost
base = nodes_base * hours * cost
print("extra nodes", extra_nodes, "| extra cost", extra, "| total", total, "| baseline", base)
assert extra_nodes == 34 and extra == 7344 and total == 8640 and base == 1296 and total - base == extra
print("overspend vs baseline:", round(extra / base, 1), "x the baseline cost for those 72 hours")
assert round(extra / base, 1) == 5.7
# Peak need, illustrative: burst needed 40 nodes for 2 hours; after that load needs 8 nodes
need_hours_burst, need_after = 2, 8
fair = nodes_burst * need_hours_burst * cost + need_after * (hours - need_hours_burst) * cost
print("fair cost with working scale-down:", fair, "| waste:", total - fair)
assert fair == 240 + 1680 and total - fair == 6720
# A cost alert at 2x baseline node-hours would have fired after 4 hours of the plateau
alert_after = 4
caught = extra_nodes * alert_after * cost
print("extra cost if the alert fired after 4 h:", caught, f"({caught/extra*100:.1f}% of the real overspend)")
assert caught == 408 and round(caught / extra * 100, 1) == 5.6
# Scale-down policy: stabilisation window and max step
n, steps, wait_min = 40, 0, 0
floor = 8
while n > floor:
    n = max(floor, n - max(2, int(n * 0.2)))   # remove 20% (at least 2) per step
    steps += 1; wait_min += 10                  # 10-minute stabilisation between steps
print("steps to reach", floor, "nodes:", steps, "| minutes:", wait_min)
assert steps == 8 and wait_min == 80
```

**Output (my run):**
```
extra nodes 34 | extra cost 7344 | total 8640 | baseline 1296
overspend vs baseline: 5.7 x the baseline cost for those 72 hours
fair cost with working scale-down: 1920 | waste: 6720
extra cost if the alert fired after 4 h: 408 (5.6% of the real overspend)
steps to reach 8 nodes: 8 | minutes: 80
```

**Follow-ups:**
- Why not scale straight to 6? The load may need more, and GPU nodes are slow to start; go stepwise to the needed level.
- How do you find other leftovers? Search config and the change log for temporary or disabled settings, and compare live state to the repository.
- What is a sensible floor? The steady load plus a small buffer, reviewed from the last weeks of traffic.

**Common mistakes:**
- Computing extra cost against the wrong baseline without saying so.
- Dropping to the floor in one step.
- No expiry or owner on emergency changes.
- Blaming the on-call engineer.

### Q18 ⭐⭐ 🟢 Dashboards show normal latency and a 0.1% error rate, but a feature lookup timeout makes the service return the default score 0.5 for 15% of 2,000,000 daily requests, which is 300,000 requests. No alert fired because the service returns success. What monitoring was missing, and how would you detect and count these degraded responses from now on?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to monitoring gaps in model-serving platforms; related topics appear in public MLOps guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Monitoring counted HTTP success, not useful answers; I would add a degraded-response metric (fallback flag and the share of exact 0.5 scores), alert on that share, and count the 300,000 past requests from logs.

**Clarifying questions:**
- Does the response say the score is a default, or is it indistinguishable from a real 0.5? It decides whether we can count exactly or only estimate.
- What decisions use the score (ranking, fraud, credit)? It sets how serious 15% defaults are and who must be told.
- Which feature lookup times out, and since when? The start time sets the number of affected requests.
- Is the timeout a symptom of load, a slow store, or a bad deploy? It tells whether the fix is capacity or rollback.
- Are there downstream effects, such as the default score being logged as a label or used in retraining? It would contaminate later data.

**Approach:**
1. First 15 minutes: confirm with logs (rows with a timeout and score exactly 0.5), find when it started, and page the owner of the feature store. Mitigate: raise the lookup timeout or fix the slow store, roll back a bad change, or add a cache and a better fallback than 0.5 (for example the last known feature value or a segment average, as a reasoned choice). Escalate to the incident lead if decisions are money-bearing. Roll back the change if the degraded share does not fall under 1% within a set time after the fix.
2. First day: count affected requests (flag or score 0.5 plus timeout log), segment them (which customers, which hours), assess business impact with the owner, decide whether to re-score or notify. Quarantine default-score rows from training data, labels and metrics.
3. Detection: add a counter `degraded_responses_total` with a reason label (feature_timeout, missing_feature, fallback_model) and ship it as a metric. Return a `degraded=true` field in the response so clients can react. Alert on the degraded share above 1% for 5 minutes. Add feature-coverage metrics (share of requests with all features fresh), score-distribution monitoring (a spike at one exact value), and a synthetic canary request every minute.
4. Change the SLI: availability should count a request as good only if it is 200 and not degraded, and latency is measured on good requests. Here the useful share is 84.9%, not 99.9%.
5. Next quarter: set an SLO for degraded share (for example 99% non-degraded), track feature-store latency and timeout budgets, and run a game day that breaks the lookup.
6. Blameless postmortem: the service did what it was coded to do (return 0.5 on timeout). The gap is that nobody defined "healthy" beyond HTTP. Detection delay is unknown (days at 300,000 requests); with the alert it is 5 to 10 minutes. Action items: metric, alert, response flag, SLI change.

**Metrics:**
- Degraded share = degraded responses / all responses = 300,000 / 2,000,000 = 15% (the HTTP error rate is only 0.1%, or 2,000 requests).
- Useful-response SLI = (200 and not degraded) / all = 84.9% in this incident.
- Per 5-minute window: about 6,944 requests; alert at 70 or more degraded (1%), normal is about 7 (0.1%).
- Guardrail: false-alarm rate of the alert and the rate of legitimate 0.5 scores.

**Risks:**
- Counting exact 0.5 as degraded over-counts if real scores can equal 0.5 (illustratively 400 requests a day at 0.02%); use the flag, not the value.
- The default of 0.5 may be fed to downstream rules or logged as a prediction; check consumers.
- A very sensitive alert pages on every blip; use a window and a floor.
- A new fallback (last known value) hides the problem unless the degraded counter still fires.

**What the interviewer scores:**
- Strong: defines healthy as useful answers, not HTTP 200; proposes a flag, a metric and an alert threshold with arithmetic.
- Strong: counts the damage after the fact and cleans training data.
- Strong: first 15 minutes, first day, next quarter; blameless action items.
- Weak: "add more dashboards"; "alert on latency".

**Example:** Illustrative numbers. Weak versus strong:
- Weak: "I would add more dashboards for the feature store."
- Strong: "Our SLI counted 200s, so 15% defaults looked fine; the useful rate was 84.9%. I would add a degraded counter with a reason label, page when it passes 1% for five minutes, which is about 70 requests against a normal 7, and return a degraded flag in the response. Then I would count the 300,000 from logs, keep them out of training, and run a blameless review of what 'healthy' meant."

**Code:**
```python
import math
from scipy import stats

daily, share = 2_000_000, 0.15
degraded = round(daily * share)
assert degraded == 300_000
err = 0.001
print("HTTP errors/day:", round(daily * err), "| degraded (200 OK, score 0.5):", degraded, "| ratio:", round(degraded / (daily * err)))
assert round(daily * err) == 2000 and round(degraded / (daily * err)) == 150
good = 1 - err - share
print("useful responses:", round(good * 100, 1), "% (an SLI that counts only HTTP success says 99.9%)")
assert round(good * 100, 1) == 84.9
# Alert design: degraded share per 5-minute window
per5 = daily / (24 * 12)
print("requests per 5 min:", round(per5))
assert round(per5) == 6944
base_rate = 0.001                                   # normal timeout rate 0.1% (illustrative)
mu = per5 * base_rate
thr_share = 0.01
thr_count = math.ceil(per5 * thr_share)
p_fa = stats.poisson.sf(thr_count - 1, mu)
print(f"normal mean {mu:.1f} per window; alert at >= {thr_count}; false-alarm prob per window {p_fa:.1e}")
assert thr_count == 70 and p_fa < 1e-12
# Time to detect at the incident rate: 15% over the 5-minute window
exp_inc = per5 * share
print("expected degraded in a 5-minute window during the incident:", round(exp_inc), "-> alert fires in the first window")
assert round(exp_inc) == 1042 and exp_inc > thr_count
# Detection delay: unknown (days) vs 5-10 minutes with the alert
print("detection delay with the alert: about 5-10 minutes")
# Cost of delay: degraded requests per hour at the incident rate
per_hour = daily / 24 * share
print("degraded requests per hour:", round(per_hour))
assert round(per_hour) == 12500
# Counting after the fact: log rows with fallback flag; score==0.5 alone over-counts if 0.5 can be legitimate
legit_rate = 0.0002
print("rows with score exactly 0.5 that are legitimate (illustrative 0.02%):", round(daily * legit_rate))
assert round(daily * legit_rate) == 400
```

**Output (my run):**
```
HTTP errors/day: 2000 | degraded (200 OK, score 0.5): 300000 | ratio: 150
useful responses: 84.9 % (an SLI that counts only HTTP success says 99.9%)
requests per 5 min: 6944
normal mean 6.9 per window; alert at >= 70; false-alarm prob per window 7.3e-45
expected degraded in a 5-minute window during the incident: 1042 -> alert fires in the first window
detection delay with the alert: about 5-10 minutes
degraded requests per hour: 12500
rows with score exactly 0.5 that are legitimate (illustrative 0.02%): 400
```

**Follow-ups:**
- Why not alert on exact 0.5? It can be legitimate; flag fallbacks explicitly and use the score spike as a second signal.
- What fallback is better than 0.5? A cached last-known feature or a segment average, chosen with the business, with the degraded flag still set.
- How do you handle past decisions? Re-score those with correct features where possible and decide with the owner whether to correct or notify.

**Common mistakes:**
- Using HTTP status as the only health signal.
- Using the score value instead of an explicit flag.
- Leaving default-score rows in training data.
- Alerting without a window or a baseline.

### Q19 ⭐⭐ 🟢 A static alert fires when hourly prediction volume falls 20% below the mean of the same hour over the previous 7 days, and over one month it paged 11 times, of which 9 were weekends and holidays and only 2 were real outages, a precision of about 18% (2 of 11). The on-call engineer now mutes it. How do you redesign the alert so the 2 real outages still page, and what do you check before re-enabling the page?
**Asked at:** Alerting and drift-monitor material (an ICLR 2026 listing on false-alarm rates of drift detectors, an MLflow alerts playbook, GeoSurge, LeadDev and Rootly pages on thresholds, monitoring debt and alert fatigue); research and practitioner pages rather than an interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** The alert compares a Sunday to a Wednesday, so I give it a seasonal baseline (same hour, same day type, last 4 weeks, with a holiday calendar), a deep tier that pages at once and a mild tier that needs two hours, and I do not re-enable the page until a backtest shows the 2 real outages still fire.

**Clarifying questions:**
- The baseline is the mean of the same hour over the previous 7 days, so it mixes weekdays and weekends. Why it matters: that is exactly why ordinary weekends page (a same-hour-last-week baseline would not); the simulation below uses this baseline.
- Does volume fall because traffic fell, or because our service stopped answering? Why: a quiet Sunday and a broken load balancer look the same on this one chart, so I want an upstream request count or an error rate beside it.
- How fast must a real outage page us, and what did the 2 real ones cost? Why: this sets how much delay I may add for noise filtering.
- Who keeps a holiday calendar, and are there promotions or launches that move volume on purpose? Why: scheduled events are the other big source of false pages.
- What is the page budget per month before people mute? Why: it gives a number to test the redesign against.

**Approach:**
1. First 15 minutes (do not just unmute). Do not silence it for good and do not leave it muted with no cover. Put a crude temporary safety net in place: a page only if volume is below 50% of the usual for the hour for one hour. Weekend and holiday dips of 20-35% will not trip it, a real outage will.
2. First day. Pull 8-12 weeks of hourly history and label the incidents (the 2 real ones; ask on-call about any missed ones). Replay the old rule and the new rule on the same history.
3. First day, the new design. Baseline = median of the same hour and the same day type (work day or off day) over the previous 28 days; day type comes from a calendar that includes holidays. Tier 1: ratio below 0.5 for one evaluation pages. Tier 2: ratio below 0.75 for two evaluations in a row opens a ticket or a low-urgency page. Add a companion signal (error rate or upstream requests) so "volume down, errors up" pages and "volume down, upstream also down" becomes a ticket.
4. Check before re-enabling: (a) backtest catches both known outages with the same delay or one hour more; (b) fewer than 2 non-outage pages in a replayed month, precision target at least 50% with the caveat that 2 events is a tiny sample; (c) a drill: inject a 65% drop into a copy of the series, including one on a Saturday, and watch it fire; (d) a run in shadow (ticket only) for 2 weeks; (e) owner, runbook link, calendar owner and a dead-man check so the alert cannot go quietly stale.
5. Next quarter. Review every page against the postmortem tags (real, false, ignored). Retire or tighten whatever is below target. Fit a seasonal forecast with an interval if the median rule is not enough. Track the share of pages acknowledged within 15 minutes, because a muted alert shows up there first.
6. Escalation and rollback of the alert change itself: if the new rule misses an outage, or pages more than the budget in a week, revert to the temporary 50% rule, not to the old noisy one. Blameless angle: the mute was a rational reaction to a bad alert, so the review asks why 9 false pages in a month did not trigger a redesign, not who muted it.

**Metrics:**
- Page precision = real-incident pages / all pages (old: 2/11 = 18.2% in the prompt). Report the denominator, since 2 events carries wide uncertainty.
- Recall on known incidents = outages that produced a new page / outages in the labelled history. Never judge from precision alone: an alert that never fires has no false pages.
- Detection delay = first page time minus outage start time, in hours at hourly resolution.
- Pages per week per on-call and share of pages acknowledged inside 15 minutes (guardrails for fatigue).
- Guardrail: the new alert must not use a threshold tuned on the 2 outages only; hold out some history.

**Risks:**
- Overfitting a threshold to two events. Say that out loud.
- A median baseline built across an outage can hide the next one; use a median, not a mean, and exclude labelled incidents from the baseline.
- A holiday missing from the calendar gives a false page once a year; a first-ever event has no same-day-type history, so decide up front whether it pages or tickets.
- A gradual fall (for example 5% a day for a week) never crosses a ratio tier. Keep a separate slow-trend check.
- Two-hour tiers add delay; the deep tier exists so a total outage is not delayed.

**What the interviewer scores:**
- Strong: finds the cause (a baseline that ignores day type), keeps the safety net while fixing, tests recall as well as precision, and defines a re-enable gate. Weak: "raise the threshold to 40%" or "just mute weekends", which hides weekend outages.
- Strong: separates a page (act now) from a ticket (look tomorrow). Weak: one threshold, one severity.
- Strong: treats the mute as a signal about the alert, not about the person.
- Strong: gives a replay or drill with numbers. Weak: "we would monitor it".

**Example:** Illustrative numbers. A normal Thursday 12:00 sees 1,000 requests; a normal Sunday 12:00 sees 600 (0.6 of a work day). Old rule: Sunday is compared with a mean of the previous 7 days, about 880, so 600 is 68% of baseline and it pages. New rule: Sunday is compared with the median of the previous Sundays and Saturdays, about 600, ratio 1.0, no page. On a Thursday outage the volume is 350 against 1,000: ratio 0.35, below 0.5, page in the first evaluation.
- Weak answer: "I would lower the sensitivity so it stops paging on weekends."
- Strong answer: "Lowering sensitivity would also hide a Sunday outage. I would compare each hour with the same hour on the same type of day, page at once below half of normal, ticket at three quarters for two hours, and prove on 12 weeks of replay that the 2 real outages still page."

**Code:**
```python
# Q19: static "20% below" volume alert versus a calendar-aware alert. Synthetic, seeded, illustrative.
import numpy as np
rng = np.random.default_rng(19)
WEEKS, H = 9, 168
shape = 1000 * (0.55 + 0.45 * np.sin(np.pi * (np.arange(24) - 4) / 20).clip(0))   # day curve
HOLIDAYS = {37, 45}       # two weekday holidays (day index) inside the eval window
def is_off(d): return d % 7 in (5, 6) or d in HOLIDAYS
vol = np.zeros(WEEKS * H)
for d in range(WEEKS * 7):
    f = 0.6 if is_off(d) else 1.0
    vol[d*24:(d+1)*24] = shape * f * rng.normal(1, 0.03, 24)
OUT1 = (38*24 + 11, 38*24 + 14)      # day 38 is a Friday, 11:00-14:00 (3 hours)
OUT2 = (57*24 + 18, 57*24 + 21)      # day 57 is a Tuesday 18:00-21:00 (3 hours)
for a, b in (OUT1, OUT2): vol[a:b] *= 0.35
START = 5 * H                        # evaluate the last 4 weeks (28 days, 672 hours)
def episodes(fire):
    eps, i = [], START
    while i < len(fire):
        if fire[i]:
            j = i
            while j + 1 < len(fire) and fire[j + 1]: j += 1
            eps.append((i, j)); i = j + 1
        else: i += 1
    return eps
# OLD rule: below 80% of the mean of the same hour over the previous 7 days (all day types mixed)
old = np.zeros(len(vol), bool)
for t in range(START, len(vol)):
    base = np.mean([vol[t - 24*k] for k in range(1, 8)])
    old[t] = vol[t] < 0.8 * base
# NEW rule: baseline = median of same hour, same day type, previous 28 days (needs >=4 samples)
new = np.zeros(len(vol), bool); ratio = np.full(len(vol), np.nan)
for t in range(START, len(vol)):
    d, h = divmod(t, 24)
    same = [vol[(k*24)+h] for k in range(d - 28, d) if k >= 0 and is_off(k) == is_off(d)]
    if len(same) < 4: continue
    ratio[t] = vol[t] / np.median(same)
for t in range(START, len(vol)):
    if np.isnan(ratio[t]): continue
    deep = ratio[t] < 0.5                                   # tier 1: page at once
    mild = ratio[t] < 0.75 and t > 0 and ratio[t-1] < 0.75  # tier 2: two hours in a row
    new[t] = deep or mild
real = [OUT1, OUT2]
def report(name, fire):
    eps = episodes(fire)
    caught = sum(any(s <= a < e + 1 or (a <= s < b) for s, e in eps) for a, b in real)
    new_pages = [e for e in eps if any(a <= e[0] < b for a, b in real)]
    delays = [e[0] - a for e in eps for a, b in real if a <= e[0] < b]
    print(f"{name}: pages={len(eps)} real_caught={len(new_pages)}/2 precision={len(new_pages)/len(eps):.0%} delays_h={delays}")
    return len(eps), len(new_pages), delays
n_old, c_old, d_old = report("OLD static", old)
n_new, c_new, d_new = report("NEW calendar", new)
assert c_old == 2 and c_new == 2          # both rules still page on both outages
assert n_new == 2 and d_new == [0, 0]     # new rule: only the 2 real pages, caught in the first outage hour
assert n_old == 10 and n_old == 5 * n_new   # old rule: 10 pages, 8 of them weekend or holiday noise
# the prompt's own arithmetic
assert round(2 / 11, 3) == 0.182 and 9 + 2 == 11
# weekend outage test for the new rule: inject a 3-hour drop on a Saturday (day 47)
v2 = vol.copy(); v2[47*24+18:47*24+21] *= 0.35
r2 = np.full(len(v2), np.nan)
for t in range(46*24, 48*24):
    d, h = divmod(t, 24)
    same = [v2[k*24+h] for k in range(d - 28, d) if is_off(k) == is_off(d)]
    r2[t] = v2[t] / np.median(same)
assert (r2[47*24+18:47*24+21] < 0.5).all() and (r2[46*24:47*24+18][~np.isnan(r2[46*24:47*24+18])] > 0.75).all()
print("weekend outage ratio:", np.round(r2[47*24+18:47*24+21], 2), "-> pages under NEW rule")
# per-page budget: 4 weeks, tolerate at most 2 noise pages
print("old pages per 28 days:", n_old, "| new pages per 28 days:", n_new)
```

**Output (my run):**
```text
OLD static: pages=10 real_caught=2/2 precision=20% delays_h=[0, 0]
NEW calendar: pages=2 real_caught=2/2 precision=100% delays_h=[0, 0]
weekend outage ratio: [0.35 0.33 0.34] -> pages under NEW rule
old pages per 28 days: 10 | new pages per 28 days: 2
```

The simulation is synthetic and seeded, so the page counts (10 old, 2 new) are illustrative, not the prompt's 11.

**Follow-ups:**
- Why not a z-score on the last hour? A z-score on raw hourly volume still mixes day types; it only works after the seasonal baseline is removed.
- What if a marketing campaign doubles traffic on purpose? Add an annotation or maintenance window that moves the baseline or suppresses the alert, with an expiry date so it cannot stay forever.
- How do you page on an outage that is a slow decline? A separate daily trend rule on the weekly median, ticket severity.

**Common mistakes:** Tuning the percentage until pages stop. Muting weekends. Reporting precision with no recall. Keeping holidays out of a calendar. Skipping the replay before re-enabling. Blaming the engineer who muted it.

### Q20 ⭐⭐ 🟡 A drift monitor compares each week's feature distribution to the previous week, and its weekly population stability index stayed below 0.03 for 26 straight weeks, so it never fired. Over the same 26 weeks the labelled AUC slid from 0.84 to 0.78. Explain how a monitor can stay quiet while the model decays, and how you would redesign the reference windows and the alert rules.
**Asked at:** Alerting and drift-monitor material (an ICLR 2026 listing on false-alarm rates of drift detectors, an MLflow alerts playbook, GeoSurge, LeadDev and Rootly pages on thresholds, monitoring debt and alert fatigue); research and practitioner pages rather than an interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** The monitor compares each week with the week before, so a slow slide never looks big in any single step, and it only watches inputs, so a change in the input-to-label relationship is invisible; I fix both with a fixed reference plus a rolling window, and with a labelled-performance alert.
(Both causes are shown in the simulation below: PSI stays under 0.03 week over week while a fixed reference climbs, and a second case has AUC falling with almost no input movement.)

**Clarifying questions:**
- Which features does the model really rely on, and does the monitor cover them? Why: PSI on 40 unimportant features can be flat while the 3 that matter move.
- How late do labels arrive, and what share is labelled? Why: it sets how soon a performance alert can fire, and what proxy I need while waiting.
- What is the model's score distribution doing? Why: the output is the cheapest summary of all inputs and often moves first.
- Was the 0.06 AUC loss (0.84 to 0.78, absolute) costly, and who was told? Why: it sets the alert level and urgency.
- Do PSI bins come from the previous week or a fixed reference? Why: a moving reference forgets the past, which is the whole bug.

**Approach:**
1. First 15 minutes. Do not retrain on reflex. Confirm the AUC fall is real: a 4-week pooled labelled AUC (one weekly AUC at 20,000 rows has a sampling sd near 0.003, so single weeks are noisy). Check the labels and data pipeline for bugs first.
2. First day. Re-run PSI of every week against a fixed launch reference and against a trailing 8-week reference. If PSI against the fixed reference has been rising, it is slow covariate drift (mechanism A). If it is flat while AUC falls, it is concept drift or a label change (mechanism B).
3. First day. Check score distribution, calibration (predicted rate versus realised rate), per-segment AUC, and the rate of nulls or defaults.
4. Decide action: if AUC is more than 0.03 below launch, retrain on recent data or recalibrate and compare on a held-out recent slice; roll back to the previous model only if it is shown better on the same recent labels. Escalate to the product owner if the loss is already above the agreed tolerance.
5. Next quarter. Redesign the monitor: (a) two references, a fixed launch window and a trailing 8-12 week window, and alert on the fixed one with a lower severity and on the trailing one for sudden breaks; (b) PSI with an effect-size level (0.1 ticket, 0.25 page, illustrative convention, tune it) and a persistence rule; (c) a CUSUM or a rolling slope on the weekly PSI-vs-fixed series so a steady climb is caught; (d) labelled performance alerts on a rolling 4-week window, with proxy signals while labels are late (score distribution, calibration on matured cohorts); (e) a scheduled review of the monitor itself.
6. Rollback or escalation criteria in writing: ticket when PSI vs fixed passes 0.10, page the model owner when it passes 0.25 or rolling AUC is 0.03 below launch, consider a retrain freeze or rollback when 0.05 below launch.
7. Blameless angle: the monitor did what it was configured to do; the review asks why no one owned the question "does the quiet monitor mean the model is fine", and records "no alert is not no problem" as the learning.

**Metrics:**
- PSI = sum over bins of (c_i - r_i) * ln(c_i / r_i), c_i the current share and r_i the reference share, 10 reference-quantile bins. Always state which reference.
- Rolling labelled AUC over 4 weeks pooled (denominator: labelled rows only), with its sampling sd.
- Detection delay in weeks = alert week minus the week the slide started.
- Guardrail: false alerts per quarter, so the redesign does not repeat Q19.

**Risks:**
- A fixed reference goes stale forever; seasonality moves PSI up every December. Compare against the same season or refresh the reference on an approved schedule.
- PSI binning on a small reference is noisy; a pure noise floor is small here (below 0.002 at 50,000 rows).
- Covariate drift that does not hurt the model gets paged; pair PSI with performance.
- Concept drift cannot be seen by any input test; only labels or proxies show it.

**What the interviewer scores:**
- Strong: names both mechanisms (moving reference hides slow drift; input monitors cannot see concept drift) and tests each. Weak: "the threshold was too high".
- Strong: proposes labelled-performance monitoring and a proxy for the label delay. Weak: more drift tests only.
- Strong: gives thresholds with an action attached. Weak: "alert on drift".
- Strong: accepts that a quiet monitor is evidence only about what it watches.

**Example:** Illustrative numbers. A feature drifts by 0.03 standard deviations each week. Week over week the PSI is about 0.001 to 0.002, always below 0.03. After 26 weeks the total shift is 0.78 standard deviations and the PSI against week 0 is about 0.6. Against the fixed reference the PSI passes 0.10 at week 11 and 0.25 at week 18.
- Weak answer: "PSI was below 0.03 every week, so the model is fine and the AUC drop must be noise."
- Strong answer: "A week-to-week reference forgets last week's baseline, so a slow slide never shows. I compare to a fixed launch window as well, I alert on rolling labelled AUC, and I treat a flat PSI plus a falling AUC as concept drift."

**Code:**
```python
# Q20: why week-over-week PSI stays quiet while AUC decays. Synthetic, seeded, illustrative.
import numpy as np
from scipy.stats import norm
rng = np.random.default_rng(20)
N, BINS, WEEKS = 50_000, 10, 26
def psi(ref, cur, edges):
    r = np.histogram(np.clip(ref, edges[0], edges[-1]), edges)[0] / len(ref)
    c = np.histogram(np.clip(cur, edges[0], edges[-1]), edges)[0] / len(cur)
    r, c = np.clip(r, 1e-6, None), np.clip(c, 1e-6, None)
    return float(np.sum((c - r) * np.log(c / r)))
def edges_of(x):
    e = np.quantile(x, np.linspace(0, 1, BINS + 1)); e[0], e[-1] = -np.inf, np.inf
    return e
def auc(y, s):                       # Mann-Whitney with ranks (no ties for continuous scores)
    r = s.argsort().argsort() + 1
    n1 = y.sum(); n0 = len(y) - n1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))
# --- Mechanism A: slow covariate drift, mean +0.03 sd per week
weeks_A = [rng.normal(0.03 * w, 1, N) for w in range(WEEKS + 1)]
wow = [psi(weeks_A[w-1], weeks_A[w], edges_of(weeks_A[w-1])) for w in range(1, WEEKS + 1)]
e0 = edges_of(weeks_A[0])
vs0 = [psi(weeks_A[0], weeks_A[w], e0) for w in range(1, WEEKS + 1)]
first_vs0_01 = next(w for w, v in enumerate(vs0, 1) if v > 0.10)
first_vs0_025 = next(w for w, v in enumerate(vs0, 1) if v > 0.25)
print(f"A: max week-over-week PSI = {max(wow):.4f} (never above 0.03: {max(wow) < 0.03})")
print(f"A: PSI against fixed week-0 reference: week 4 = {vs0[3]:.3f}, week 26 = {vs0[-1]:.3f}; passes 0.10 at week {first_vs0_01}, 0.25 at week {first_vs0_025}")
# --- Mechanism B: concept drift, inputs barely move. x | y ~ N(d_t * y, 1)
d0, d1 = np.sqrt(2) * norm.ppf(0.84), np.sqrt(2) * norm.ppf(0.78)      # binormal separation for AUC 0.84 and 0.78
M = 20_000
def week_B(w):
    d = d0 + (d1 - d0) * w / (WEEKS - 1)
    y = (rng.random(M) < 0.3).astype(int)
    return y, rng.normal(d * y, 1)
data = [week_B(w) for w in range(WEEKS)]
wowB = [psi(data[w-1][1], data[w][1], edges_of(data[w-1][1])) for w in range(1, WEEKS)]
vs0B = [psi(data[0][1], data[w][1], edges_of(data[0][1])) for w in range(1, WEEKS)]
aucs = [auc(y, x) for y, x in data]
print(f"B: max week-over-week PSI = {max(wowB):.4f}; max PSI against fixed week-0 = {max(vs0B):.4f} (both below 0.03)")
print(f"B: labelled AUC week 1 = {aucs[0]:.3f}, week 26 = {aucs[-1]:.3f}")
# noise of one weekly AUC at 20,000 rows, and of a 4-week pooled AUC
reps = [auc(*week_B(0)) for _ in range(40)]
sd = np.std(reps)
pool = []
for _ in range(15):
    ys, xs = zip(*[week_B(0) for _ in range(4)]); pool.append(auc(np.concatenate(ys), np.concatenate(xs)))
sd4 = np.std(pool)
print(f"AUC sampling sd: one week (20,000 rows) = {sd:.4f}; four pooled weeks (80,000 rows) = {sd4:.4f}")
# detection: alert when 4-week rolling labelled AUC is 0.03 below the launch AUC
launch = np.mean(aucs[:4])
roll = [np.mean(aucs[w-3:w+1]) for w in range(3, WEEKS)]
alert_week = next(w + 3 + 1 for w, a in enumerate(roll) if a < launch - 0.03)
print(f"labelled-AUC alert (4-week mean 0.03 below launch {launch:.3f}) fires in week {alert_week} of 26")
# asserts for every number quoted in the text
assert max(wow) < 0.03 and max(wowB) < 0.03 and max(vs0B) < 0.03
assert max(wow) < 0.002 and min(wow) > 0.0003
assert vs0[-1] > 0.25 and first_vs0_01 == 11 and first_vs0_025 == 18
assert abs(aucs[0] - 0.84) < 0.01 and abs(aucs[-1] - 0.78) < 0.01
assert sd < 0.006 and sd4 < sd
assert alert_week == 18 and first_vs0_01 < alert_week
assert round(0.84 - 0.78, 2) == 0.06
```

**Output (my run):**
```text
A: max week-over-week PSI = 0.0018 (never above 0.03: True)
A: PSI against fixed week-0 reference: week 4 = 0.014, week 26 = 0.592; passes 0.10 at week 11, 0.25 at week 18
B: max week-over-week PSI = 0.0018; max PSI against fixed week-0 = 0.0100 (both below 0.03)
B: labelled AUC week 1 = 0.838, week 26 = 0.784
AUC sampling sd: one week (20,000 rows) = 0.0030; four pooled weeks (80,000 rows) = 0.0013
labelled-AUC alert (4-week mean 0.03 below launch 0.835) fires in week 18 of 26
```

All figures are from a seeded synthetic simulation, not real data.

**Follow-ups:**
- Why not just use a lower PSI threshold? The weekly step is about 0.002; the noise floor and the step are too close, so a threshold low enough to catch it would fire on noise. Change the reference, not the threshold.
- Can any feature monitor catch concept drift? No. Use labelled windows, matured cohorts, calibration and proxy metrics.
- How often do you refresh the fixed reference? Only on a model release or an approved review, and log the change.

**Common mistakes:** Comparing only to the previous period. Using one PSI threshold for every feature. Treating the AUC fall as noise without a standard error. Monitoring inputs only. Not asking who owns the monitor.

### Q21 ⭐⭐ 🟡 After a blue/green switch, the 99th-percentile latency went from 120 ms to 2,400 ms (20 times the old value) for about 3 minutes because the green pods loaded a multi-gigabyte model after receiving traffic. Health checks only tested that the process was up. What do you change in the readiness checks and in the switch procedure, and what would you watch during the next switch?
**Asked at:** GPU-serving and autoscaling pages (apxml and system-design.space on autoscaling and serving architecture; vendor pages from regolo.ai and lyceum.technology on cold starts and capacity, treated as vendor claims); no public postmortem located; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** "Process is up" is not "model is ready", so I make readiness mean the model is loaded and has answered warm-up requests inside the latency budget, I move traffic in stages with an automatic abort, and I keep blue alive until green has proved itself.

**Clarifying questions:**
- How long does the model take to load, and does it load at start or on first request? Why: it decides whether a startup gate or a warm-up routine is needed.
- What is our latency objective, and what is the traffic at the switch time? Why: it sets the abort threshold and the number of requests at risk.
- Can blue and green run side by side, and for how long can we pay for both? Why: instant rollback needs blue kept warm.
- How many green pods do we need to carry full traffic? Why: staged shifts need enough warm pods at each stage.
- Is the model file pulled at pod start (cold disk, network)? Why: a slow pull makes the startup window long. (Book 4, Part 2 has the heading "Where do model weights live: baked into the image, mounted as a volume, or downloaded at start?" for the options.)

**Approach:**
1. First 15 minutes (during the incident). If p99 is above 2x baseline (here above 240 ms) for 60 seconds after a switch, send traffic back to blue first and ask questions after. It cost about 3 minutes here; rolling back takes seconds if blue is still warm.
2. First day. Change readiness: the pod reports ready only after (a) the model file is loaded and a version/hash check matches the expected model, and (b) a warm-up routine of synthetic requests ran with the last 5 under 2x baseline. On Kubernetes this is usually a startup probe plus a readiness probe that calls an endpoint testing the loaded model (the probe names are editor knowledge, not tested here; the checking logic is what matters). Book 4, Part 3 has "Rolling updates, rollbacks and canary releases for a new model version on Kubernetes" for the manifest details.
3. First day. Change the switch: 5%, 25%, 50%, 100% with a hold of 60 seconds at each, and an automatic abort rule at every stage. Keep blue running for at least 30 minutes after 100%.
4. Next quarter. Put the switch in a runbook and a CI step; run a game day where green is deliberately cold to prove the gate holds; add a pre-warm job that sends traffic to green before the first user does. Track model-load time as a metric so growth in model size shows up before it hurts.
5. Escalate to the service owner if p99 stays above 2x baseline after rollback (it means blue is also hurt), and page the platform team if green pods cannot reach ready within a set time (say 5 minutes).
6. Blameless angle: the health check passed exactly as written. The review asks why "up" was accepted as "ready", why the switch was all-at-once, and which check would have shown it in staging, not who clicked the button.

**Metrics:**
- Readiness lead time = time from pod start to first ready, and the load time inside it.
- p99 latency by one-minute window, compared with baseline = 120 ms; abort when above 240 ms (2x) for 60 s.
- Exposed requests = traffic rate x stage seconds x stage share.
- Error rate and saturation (queue depth) as guardrails next to latency, because a cold pod can also time out.
- Rollback time = time from abort decision to 100% on blue.

**Risks:**
- Warm-up that uses unrepresentative inputs warms the wrong path. Replay real recent requests.
- Kept-alive blue costs money; set a timer and an owner.
- Staged shifts with sticky sessions can leave some users on green for the whole test.
- Too tight an abort threshold on low traffic stages: at 5% of traffic p99 comes from few requests. Add a minimum request count.
- A passing health check can still hide a wrong model version; check the model hash, not just "loaded".

**What the interviewer scores:**
- Strong: separates liveness (process alive) from readiness (can serve the real latency). Weak: "increase the probe delay".
- Strong: staged traffic plus an automatic abort rule with numbers. Weak: "watch the dashboard".
- Strong: instant rollback path (blue kept warm). Weak: redeploy the old version.
- Strong: blameless review of a check that passed for the wrong reason.

**Example:** Illustrative numbers. Traffic is 500 requests per second. The all-at-once switch exposed 500 x 180 = 90,000 requests to the cold window, and a p99 of 2,400 ms means at least 1% of them (900) were slower than 2.4 seconds. A staged shift with the gate would have exposed the 5% stage for 60 seconds: 25 requests a second x 60 = 1,500 requests, 60 times fewer.
- Weak answer: "I would make the health check wait longer before sending traffic."
- Strong answer: "Ready has to mean the model is loaded and has answered warm-up requests under 240 ms. I shift 5, 25, 50, 100 percent with a 60-second hold, abort on p99 above 240 ms, and keep blue up for 30 minutes. On this incident that is 1,500 exposed requests instead of 90,000."

**Code:**
```python
# Q21: blue/green cold start. Illustrative numbers; simple deterministic model, not a benchmark.
BASE_P99_MS, BAD_P99_MS, BAD_SECONDS = 120, 2400, 180
RPS = 500                                   # illustrative traffic
assert BAD_P99_MS / BASE_P99_MS == 20
exposed_bigbang = RPS * BAD_SECONDS         # all traffic hits the cold pods for 3 minutes
slow_min = exposed_bigbang // 100           # p99 above 2.4 s means at least 1% of requests were slower
print(f"big-bang switch: {exposed_bigbang:,} requests in the 3-minute window, at least {slow_min:,} slower than 2.4 s")
assert exposed_bigbang == 90_000 and slow_min == 900
# --- readiness with warm-up: a cold pod answers the first requests slowly, then settles (decay model)
import math
def cold_latency_ms(i, steady=120, first=2400, tau=6):      # i-th request after start
    return steady + (first - steady) * math.exp(-i / tau)
THRESH = 2 * BASE_P99_MS                                    # ready only when warm latency < 240 ms
def warmup_requests_needed(window=5):
    i = 0
    while True:
        i += 1
        if i >= window and all(cold_latency_ms(j) < THRESH for j in range(i - window, i)):
            return i
n_warm = warmup_requests_needed()
print(f"synthetic warm-up requests before the pod reports ready: {n_warm}")
assert cold_latency_ms(0) == 2400 and cold_latency_ms(n_warm) < THRESH and cold_latency_ms(n_warm - 6) >= THRESH
# --- staged shift with an automatic abort rule: p99 over a 60 s stage window must stay under 2x baseline
stages = [5, 25, 50, 100]                                   # percent of traffic
STAGE_S = 60
def run(pods_warm):
    served_cold = 0
    for pct in stages:
        exposed = RPS * pct // 100 * STAGE_S
        if not pods_warm:                                   # gate trips in the first stage
            served_cold += exposed
            return pct, served_cold
    return 100, 0
stage_hit, cold_requests = run(pods_warm=False)
print(f"staged shift with unwarmed pods: abort in the {stage_hit}% stage, {cold_requests:,} requests exposed")
assert stage_hit == 5 and cold_requests == 1_500
assert exposed_bigbang / cold_requests == 60                # 60 times fewer requests exposed
print(f"exposure ratio big-bang / staged: {exposed_bigbang // cold_requests}x")
print("abort rule: p99 > 240 ms (2 x 120) for 60 s in any stage -> send 100% back to blue, keep blue for >= 30 min")
```

**Output (my run):**
```text
big-bang switch: 90,000 requests in the 3-minute window, at least 900 slower than 2.4 s
synthetic warm-up requests before the pod reports ready: 23
staged shift with unwarmed pods: abort in the 5% stage, 1,500 requests exposed
exposure ratio big-bang / staged: 60x
abort rule: p99 > 240 ms (2 x 120) for 60 s in any stage -> send 100% back to blue, keep blue for >= 30 min
```

The warm-up decay curve is an assumption; the exposure arithmetic is exact for the stated inputs. Probe names for any orchestrator were not tested here.

**Follow-ups:**
- Why not just a longer initial delay? A fixed delay guesses at the load time; when the model grows the guess is wrong again. Test the real condition.
- What do you watch in the next switch? p99 and error rate by stage, queue depth, model hash on each pod, ready count, and GPU or memory use.
- Does a canary replace this? A canary tests model quality on a slice; a readiness gate tests that a pod can serve at all. You want both.

**Common mistakes:** Treating process up as ready. Switching 100% at once with no abort rule. Tearing down blue immediately. Warming with synthetic inputs unlike real traffic. Not checking which model version loaded.

### Q22 ⭐⭐ 🟡 You must write automatic rollback criteria for a model whose error rate is about 2% at baseline, with 10,000 canary requests available before a ramp. The standard error of an error rate of 2% on 10,000 requests is about 0.14 points, so a rise to 2.5% (0.5 points absolute, 25% relative to 2%) is about 3.6 standard errors if the 2% baseline is treated as exactly known (about 2.4 against a concurrent control of 10,000 requests). What rule do you write, and how do you handle small segments that this volume cannot see?
**Asked at:** MLOps interview guides (startup.jobs, Hyring, kore1, refresh.cv, wecreateproblems and Yardstick pages list rollback, canary versus blue/green versus shadow, and 'tell me about an urgent production incident' prompts, and one 2026 guide says the strongest questions test custody of a live model); practitioner and prep-site material rather than a confirmed employer round; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** I write the rule in numbers before the canary starts: compare to a concurrent control, roll back on a z of 3 or more (checked in fixed steps) or on a hard error cap, hold the ramp in a grey zone, and give small segments their own count-based rule plus a longer bake. Note that 3.6 standard errors holds only if the 2% baseline is treated as exactly known.

**Clarifying questions:**
- Is the 2% baseline measured on a control running at the same time, or taken from history? Why: 3.6 treats it as known; against a concurrent control of 10,000 requests the same 0.5-point rise is about 2.4 standard errors.
- What rise in error rate is actually harmful: 0.5 points, 1 point? Why: it sets the effect to detect, and with 10,000 requests a 0.5-point rise is caught only part of the time.
- Which segments matter (customer tier, region, device, language)? Why: a segment with 2% of traffic has only 200 canary requests.
- Is an automatic rollback acceptable, or should it page a human first? Why: some rollbacks have side effects.
- How fast do we ramp (5% to 25% to 100%) and how long do stages last? Why: more time is the only cure for small segments.

**Approach:**
1. First 15 minutes of a canary. Use only hard guards: error rate above 4% after 500 canary requests, or p99 above 2x baseline for 60 seconds, or any crash loop. These need no statistics and catch gross failures.
2. First day of design. Write the statistical rule: pooled two-proportion z of canary against a concurrent control, needs at least 1,000 canary requests and at least 5 errors, evaluated every 1,000 requests; roll back at z of 3.0 or more; hold the ramp and extend the stage at z between 2.0 and 3.0; ramp only below 2.0 and after the minimum bake time. Peeking is the reason for a threshold above the usual 2 (see the simulation).
3. Segments. Per segment with at least 200 canary requests, roll back on an exact count rule (for 200 requests, 12 or more errors, false chance under 0.1% at a true 2% rate). Segments with fewer requests get a ticket, a longer bake, targeted traffic (route internal or test accounts of that segment into the canary) and synthetic probes.
4. Next quarter. Review each rollback and each miss against a blameless template. Replay old incidents against the rule to estimate recall. Put the rule in code with tests and keep the thresholds in version control.
5. Escalation: automatic rollback needs no approval; a hold needs an owner to look within the stage time; if a rollback fails to restore the error rate within 5 minutes, page the service owner.
6. Blameless angle: if a rollback was too late, the review asks what the written rule allowed, not who approved the ramp.

**Metrics:**
- Error rate = failed requests / all requests, per arm, per segment. Say what counts as a failure (5xx, timeouts, fallback responses).
- z = (p_canary - p_control) / sqrt(p_pool x (1 - p_pool) x (1/n_canary + 1/n_control)).
- False rollback rate (probability a good canary is rolled back) and catch rate for the harm size you care about.
- Time to rollback = first breach to 100% on the old version.
- Guardrails: latency, saturation, and the model-quality proxy (score distribution) beside errors.

**Risks:**
- Peeking: checking many times at z of 2 rolls back a healthy canary about 11% of the time in the simulation below.
- Control and canary differ by traffic mix; split randomly or use the same segments.
- Rare, severe segment failures stay invisible at 10,000 requests; small volume cannot be fixed by cleverness, only by time or targeted traffic.
- Error rate misses a wrong-but-successful model; add a score-distribution check.

**What the interviewer scores:**
- Strong: knows that "3.6 standard errors" depends on a known baseline and gives the concurrent-control value. Weak: repeats the number as proof.
- Strong: pre-registered thresholds with a grey zone and a hard guard. Weak: "roll back if it looks bad".
- Strong: explains peeking and gives a tested false-rollback rate. Weak: one threshold at 2 sigma.
- Strong: honest about small segments and what to do about them.

**Example:** Illustrative numbers. Baseline 2%. The canary shows 250 errors in 10,000 (2.5%). Against a known 2%, z is 3.57. Against a control that also had 10,000 requests and 200 errors, z is 2.38, so the rule holds the ramp instead of rolling back. Against a control of 190,000 requests with 3,800 errors (a 5% canary split), z is 3.46. Same numbers, different evidence.
- Weak answer: "The rise is 3.6 standard errors so it is significant, roll back."
- Strong answer: "That 3.6 treats 2% as exact. With a same-size concurrent control it is about 2.4, which is my hold zone, not my rollback line. My written rule rolls back at z of 3 or more, checked every 1,000 requests, with a hard cap at 4% errors."

**Code:**
```python
# Q22: automatic canary rollback criteria. Seeded simulation plus exact binomial; illustrative numbers.
import math
import numpy as np
from scipy.stats import binom
rng = np.random.default_rng(22)
p0, n = 0.02, 10_000
se_known = math.sqrt(p0 * (1 - p0) / n)
print(f"SE of 2% on 10,000 = {se_known*100:.3f} points; z for 2.5% against a KNOWN 2% baseline = {0.005/se_known:.2f}")
assert abs(se_known * 100 - 0.14) < 0.001 and round(0.005 / se_known, 1) == 3.6
def z2(x1, n1, x2, n2):                         # pooled two-proportion z (canary x1/n1 vs control x2/n2)
    p = (x1 + x2) / (n1 + n2)
    return (x1 / n1 - x2 / n2) / math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
for label, nc in [("control also 10,000", 10_000), ("control 190,000 (5% canary split)", 190_000)]:
    z = z2(250, n, round(0.02 * nc), nc)
    print(f"z for 2.5% vs measured 2.0%, {label}: {z:.2f}")
z_eq, z_big = z2(250, n, 200, 10_000), z2(250, n, 3800, 190_000)
assert round(z_eq, 1) == 2.4 and round(z_big, 1) == 3.5
# --- peeking: check every 1,000 canary requests; control is 19x larger; stop if z >= Z
def sim(p_canary, Z, trials=2000, peek=1000, total=10_000, ctrl_factor=19, p_ctrl=0.02, min_err=5):
    hits = 0
    for _ in range(trials):
        c = rng.binomial(peek, p_canary, total // peek).cumsum()
        k = ctrl_factor * peek * np.arange(1, total // peek + 1)
        x = rng.binomial(k, p_ctrl)
        fired = False
        for i in range(total // peek):
            nn = peek * (i + 1)
            if c[i] >= min_err and z2(int(c[i]), nn, int(x[i]), int(k[i])) >= Z: fired = True; break
        hits += fired
    return hits / trials
rows = {}
for Z in (2.0, 3.0, 4.0):
    rows[Z] = (sim(0.02, Z), sim(0.025, Z), sim(0.03, Z))
    print(f"threshold z>={Z}: false rollback {rows[Z][0]:.1%} | catches 2.5% {rows[Z][1]:.0%} | catches 3.0% {rows[Z][2]:.0%} (checked every 1,000 requests)")
assert rows[2.0][0] > 0.10                          # peeking at z=2 rolls back far too often
assert rows[3.0][0] < 0.02                          # z=3 keeps false rollback small
assert rows[3.0][2] > rows[3.0][1] > 0.4            # bigger harm is caught more often
# hard guard: absolute cap, error rate above 4% (2 points above baseline) once 500 requests are in
cap_fp = 1 - binom.cdf(math.floor(0.04 * 500), 500, 0.02)
print(f"hard cap 4% at 500 requests: false trigger at true 2% = {cap_fp:.4f}")
assert cap_fp < 0.005
# --- small segments: a segment with 2% of traffic has 200 canary requests
seg = 200
k = int(binom.isf(0.001, seg, p0)) + 1               # smallest count with false chance below 0.1% at a true 2% rate
print(f"segment of {seg} requests: expect {seg*p0:.0f} errors at 2%; rule 'errors >= {k}' has false chance {binom.sf(k-1, seg, p0):.5f}")
for pt in (0.05, 0.10, 0.20):
    print(f"   chance to catch a segment error rate of {pt:.0%}: {binom.sf(k-1, seg, pt):.2f}")
assert binom.sf(k - 1, seg, 0.02) < 0.001 and binom.sf(k - 1, seg, 0.20) > 0.99 and 0.2 < binom.sf(k - 1, seg, 0.05) < 0.4 and binom.sf(k - 1, seg, 0.10) > 0.9
# volume needed to see a 5% segment rate (vs 2%) with the same 3 sigma idea, one-sided: n = (z*sqrt(p0 q0)+...)^2
z, power_z = 3.0, 0.84
need = ((z * math.sqrt(0.02 * 0.98) + power_z * math.sqrt(0.05 * 0.95)) / 0.03) ** 2
print(f"requests needed in a segment to catch 2% -> 5% (z 3.0, 80% power): about {need:,.0f}")
assert 350 < need < 450
```

**Output (my run):**
```text
SE of 2% on 10,000 = 0.140 points; z for 2.5% against a KNOWN 2% baseline = 3.57
z for 2.5% vs measured 2.0%, control also 10,000: 2.38
z for 2.5% vs measured 2.0%, control 190,000 (5% canary split): 3.46
threshold z>=2.0: false rollback 10.8% | catches 2.5% 95% | catches 3.0% 100% (checked every 1,000 requests)
threshold z>=3.0: false rollback 0.9% | catches 2.5% 76% | catches 3.0% 100% (checked every 1,000 requests)
threshold z>=4.0: false rollback 0.1% | catches 2.5% 40% | catches 3.0% 100% (checked every 1,000 requests)
hard cap 4% at 500 requests: false trigger at true 2% = 0.0014
segment of 200 requests: expect 4 errors at 2%; rule 'errors >= 12' has false chance 0.00079
   chance to catch a segment error rate of 5%: 0.30
   chance to catch a segment error rate of 10%: 0.98
   chance to catch a segment error rate of 20%: 1.00
requests needed in a segment to catch 2% -> 5% (z 3.0, 80% power): about 404
```

All simulation numbers are from a seeded run (2,000 trials per setting) and will move slightly with other seeds.

**Follow-ups:**
- Why not use z of 2? With checks every 1,000 requests it rolled back a healthy canary about 11% of the time (my run). Roll-forward and rollback both cost something.
- Does a 0.5-point rise matter? Only the business can say; if it does, the z of 3 rule catches it about 76% of the time within 10,000 requests, so you need a longer stage or a larger canary.
- What about a segment with 1% of traffic? About 100 canary requests, 2 errors expected; only a collapse is visible. Use targeted traffic or a longer bake.

**Common mistakes:** Quoting z against a "known" baseline when the control is noisy. Checking repeatedly at 2 sigma. Writing "roll back if it looks bad". Ignoring small segments. Judging on error rate only. Blaming whoever approved the ramp.

### Q23 ⭐⭐ 🟡 A streaming job feeding the online store lagged by 7 hours, so the feature clicks_last_hour served to the model actually described the hour that ended 7 hours earlier, while offline training always used the live hour. The lag lasted 5 hours before anyone noticed, and the model returned normal-looking scores throughout. How do you detect this kind of staleness, what do you serve when a feature is stale, and how do you assess the damage?
**Asked at:** Feature-store and skew material (techinterview.org pages on point-in-time joins, drift and feature stores and MLOps pipelines, DesignGurus and barkingiguana pages on training-serving skew; one snippet gives a mean-imputation versus zero-fill skew incident as a template); prep and course material rather than a documented real incident; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** I measure the age of every feature value at serving time, alert on it, give each feature a time-to-live so a stale read becomes an explicit "missing", serve a declared fallback, and then replay the 5 hours with the right values to count the decisions that changed.

**Clarifying questions:**
- How many requests per second, and what decisions does the score drive? Why: it turns "5 hours" into a number of affected decisions and tells me whether a human must review them.
- How sensitive is the model to clicks_last_hour (importance, or a drop-one test)? Why: it decides between a fallback model, a default value or a hard stop.
- Is the online store written by the stream only, or can I recompute the feature from raw events? Why: it decides whether the damage is repairable.
- Did offline training use the live hour, as the prompt says? Why: yes means the model expects fresh values, so stale is a skew, and the training-versus-serving gap is built in.
- Who consumes the scores downstream (campaigns, limits)? Why: they need a correction notice.

**Approach:**
1. First 15 minutes. Confirm the lag (age of the newest event in the stream, offset lag on the consumer, age of the value in the store). If the model is sensitive and the lag persists, switch to the fallback (see step 3); do not wait for the stream to catch up before deciding. Page the stream owner.
2. First day. Get the stream caught up or replay from the committed offset (idempotently). Recompute the feature for the lag window from raw events. Replay the 5 hours of requests with the correct values and compare decisions. Write the incident timeline (blameless).
3. What to serve when stale: a feature carries an expected maximum age (say 30 minutes, a hand-picked illustration). The store or the service returns None when the value is older. The service then applies, in order of preference: (a) a model variant trained with that feature missing (best if clicks_last_hour is not dominant), (b) the last good value plus an "age" flag if the model was trained with age, (c) a population default only if training included default rows, (d) a safe decision rule (queue for review or conservative threshold) when the feature is critical. Never silently serve the old number.
4. Assess the damage: per-hour mean score error and the share of decisions that flip across the threshold (simulation below), then the cost of the flipped decisions; contact downstream owners; decide whether to re-score, reverse or accept.
5. Next quarter. Add freshness SLOs for every online feature (age at serve, 99th percentile), a dead-man check on the pipeline, a skew test that compares online and offline feature values on a sample each day, and a game day where the stream is paused.
6. Escalation: page the feature owner when age passes the limit; escalate to the model owner and business owner when a critical feature is stale for more than 15 minutes; roll back to the previous model only if the old model does not use the feature.
7. Blameless angle: the model returned normal-looking scores because nothing measured freshness; the learning is "we had no signal for time", not a person.

**Metrics:**
- Feature age at serving = request time minus the event time of the value used; report p50 and p99 and the share of requests above the limit.
- Pipeline lag = newest event time in the source minus newest event time in the store.
- Decision flip rate = requests whose decision differs with the true feature / requests in the window.
- Mean absolute score error between true and served scores.
- Detection delay = alert time minus incident start (here the incident ran 300 minutes undetected; a one-minute age check would have alerted in the first check).

**Risks:**
- Model scores look normal because stale values are still plausible numbers.
- A "last known value" fallback hides the problem for as long as it lasts.
- A default fallback shifts the score distribution (a different skew) when the model never saw defaults in training.
- The replay depends on raw events being retained.
- A diurnal feature is wrong by a different amount at each hour, so a single average hides the worst hour.

**What the interviewer scores:**
- Strong: freshness as a first-class signal (age at serve, TTL) and an explicit fallback. Weak: "check the dashboard for lag".
- Strong: a damage estimate with a replay, not a guess. Weak: "scores looked normal so no harm".
- Strong: separates detection, mitigation and repair. Weak: only fixes the stream.
- Strong: notices that offline used the live hour, so the model was never trained for stale values.

**Example:** Illustrative numbers. 100 requests per second for 5 hours is 1,800,000 requests scored with a stale feature. In the simulation the average share of decisions that flip is 0.7%, which would be about 12,000 decisions to review (a projection from synthetic data, not measured data).
- Weak answer: "Scores looked normal, so the model was fine; I would just restart the stream."
- Strong answer: "I alert on the age of every value at serve time, so this would have paged in the first minutes. For the 5 hours, I recompute the feature from raw events, replay the requests and count decisions that cross the threshold, then tell the downstream owners which ones to review."

**Code:**
```python
# Q23: stale clicks_last_hour served for 5 hours with a 7-hour lag. Synthetic, seeded, illustrative.
import numpy as np
rng = np.random.default_rng(23)
LAG_H, DURATION_H, RPS = 7, 5, 100
served_requests = RPS * DURATION_H * 3600
print(f"requests scored with a stale feature: {served_requests:,}")
assert served_requests == 1_800_000
# --- freshness check: age = now - feature event time; page when age > 30 min
def age_minutes(now_min, event_min): return now_min - event_min
FRESH_LIMIT = 30
incident_start = 12 * 60                                  # 12:00; lag appears at once
checks = range(incident_start - 10, incident_start + 60)  # one check a minute
first_alert = next(t for t in checks if age_minutes(t, t - (LAG_H*60 if t >= incident_start else 5)) > FRESH_LIMIT)
detect_delay_min = first_alert - incident_start
print(f"with a per-minute age check the alert fires in the first one-minute check ({detect_delay_min} minutes after the lag starts) (the incident ran undetected for {DURATION_H*60} minutes)")
assert detect_delay_min == 0 and DURATION_H * 60 == 300
# --- damage: replay the 5 hours with true versus served feature values
users = 50_000
level = rng.lognormal(1.0, 0.5, users)                    # user's typical clicks per hour
def diurnal(h): return 1 + 0.8 * np.sin(2 * np.pi * (h - 14) / 24)
def clicks(h): return rng.poisson(level * diurnal(h))
w, b, THR = 0.35, -3.4, 0.5
def score(c, other): return 1 / (1 + np.exp(-(w * np.log1p(c) * 3 + other + b)))
other = rng.normal(0, 0.6, users)                         # all other features
rows = []
for h in range(12, 12 + DURATION_H):                      # incident hours 12..16
    s_true = score(clicks(h), other)
    s_stale = score(clicks(h - LAG_H), other)
    flipped = ((s_true >= THR) != (s_stale >= THR)).mean()
    rows.append((h, np.abs(s_true - s_stale).mean(), flipped))
    print(f"hour {h}: mean |score error| = {rows[-1][1]:.3f}, decisions flipped = {flipped:.1%}")
tot_flip = np.mean([r[2] for r in rows])
exp_flips = tot_flip * served_requests
print(f"average flipped share {tot_flip:.1%} -> about {exp_flips:,.0f} of {served_requests:,} decisions to review (projection from the simulation, not measured)")
assert all(0 < r[2] < 0.5 for r in rows) and 0.002 < tot_flip < 0.05
# --- TTL pattern: a stale read returns None, and the service applies the fallback explicitly
def get_feature(store, key, now, ttl):
    v = store.get(key)
    return None if v is None or now - v["ts"] > ttl else v["value"]
store = {"u1": {"value": 7, "ts": 100}}
assert get_feature(store, "u1", now=110, ttl=30) == 7 and get_feature(store, "u1", now=400, ttl=30) is None
print("TTL read: fresh value returned at age 10, None at age 300 (service then uses the declared fallback)")
```

**Output (my run):**
```text
requests scored with a stale feature: 1,800,000
with a per-minute age check the alert fires in the first one-minute check (0 minutes after the lag starts) (the incident ran undetected for 300 minutes)
hour 12: mean |score error| = 0.044, decisions flipped = 0.1%
hour 13: mean |score error| = 0.058, decisions flipped = 0.3%
hour 14: mean |score error| = 0.078, decisions flipped = 0.5%
hour 15: mean |score error| = 0.096, decisions flipped = 0.9%
hour 16: mean |score error| = 0.108, decisions flipped = 1.5%
average flipped share 0.7% -> about 12,247 of 1,800,000 decisions to review (projection from the simulation, not measured)
TTL read: fresh value returned at age 10, None at age 300 (service then uses the declared fallback)
```

The flip shares and the 12,000 projection come from invented synthetic data; with a different threshold or feature importance they change a lot.

**Follow-ups:**
- Why not just rely on pipeline lag metrics? Lag at the source can look fine while the store is stale (writes failing), so measure age at the point of use.
- Is "last known value" ever right? Yes for slow features with a short expiry and an age flag; not for a fast one like clicks in the last hour.
- How do you stop training and serving using different hours? Define the feature once with its time window and use the same definition and point-in-time join for both; Book 6 Part 8 Q18 shows the "default score counted as success" pattern in the same family.

**Common mistakes:** Serving the old value silently. Alerting on the job instead of the value's age. Not estimating the damage. Choosing a default the model never saw in training. Treating normal-looking scores as proof.

### Q24 ⭐⭐ 🟡 A retrained refund-risk model scored an offline AUC of 0.93 against 0.81 online, and dropping one feature, ticket_reopened, which is filled in after the refund decision, took the offline AUC to 0.84. The leaky feature was added by a teammate three releases ago. How do you find the same problem in other features, what do you tell the stakeholders about the three earlier releases, and what check would catch it automatically?
**Asked at:** Leakage and reproducibility material (arXiv 2207.07048 and 2311.04179 on leakage, an Omdena post on silent ML failures and label timing, an arXiv 2025 paper on reproducible ML infrastructure); research and practitioner pages rather than an interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** I audit every feature for "was this value known at decision time", with a timestamp check as the real test and single-feature AUC and drop-one loss as pointers; I tell stakeholders plainly that the three earlier releases were approved on inflated offline numbers, and I add an automatic availability gate to the release pipeline.

**Clarifying questions:**
- What is the exact decision time, and where is it logged? Why: leakage is defined against that timestamp, so I need it per row.
- Is there online data for the earlier releases (scores plus matured outcomes)? Why: it shows what each release really delivered, independent of the offline claim.
- How was ticket_reopened treated at serving time (missing, default, zero)? Why: if serving fed a default while training saw the real value, the live model was running on a feature it never saw filled.
- Who approved each release and on which offline number? Why: it defines who must be told, and what the approval rule should have required.
- Is a 0.03 gap (0.84 offline after the fix, 0.81 online) expected? Why: it is still unexplained, so more leakage or shift may remain.

**Approach:**
1. First 15 minutes. Stop promoting the current candidate. Keep the live model unchanged unless online metrics are harmful; if they are, move back to the last release from before ticket_reopened was added (check which one that was in the registry).
2. First day, audit. (a) For every feature, document its source table and the time it is written; compute the share of rows where available_at is later than decision_time. (b) Run single-feature AUC to find suspiciously strong features (a pointer only). (c) Run drop-one ablation (retrain without each feature) and look for a feature that carries a lot on its own. (d) Review any feature built from a status, outcome, resolved, closed or "after" field by hand.
3. First day, stakeholders. Message: "In the last three releases, offline AUC was inflated by a feature that is only known after the decision (roughly 0.09 AUC in this release, 0.93 to 0.84). Online performance is what we measured (0.81), not what we reported offline. Here is the effect on decisions, the fix, and the date for the next release." State facts, no names.
4. Estimate impact: compare online AUC (or approval, refund-loss) for each of the three releases with the release before the leak. Quantify the cost of the weaker model, then decide on re-scoring or review.
5. Next quarter. Put the availability gate in CI: each feature must declare source, available_at rule and owner; the training pipeline fails if a feature's timestamp can be after the decision time, or if single-feature AUC is above a set level without a signed-off exception. Use point-in-time joins. Add a daily offline-versus-online score comparison.
6. Escalation: tell the model risk or product owner the same day a leak is confirmed; consider a rollback if the leaky model is live and its online metric is below the agreed floor.
7. Blameless angle: the teammate added a plausible feature that review did not catch because nothing in the process asked "when is this written"; the action item is the gate, not a lecture. Be careful with the same sentence in the postmortem for each of the three releases.

**Metrics:**
- Late share = rows where feature available_at > decision_time / all rows (target: 0 for every training feature).
- Single-feature AUC and drop-one AUC loss (offline, on a time-ordered holdout).
- Offline minus online AUC gap: 0.12 before the fix (0.93 - 0.81), 0.03 after (0.84 - 0.81).
- Online outcome metric for each of the three releases (matured labels only).

**Risks:**
- A high single-feature AUC alone cannot separate leakage from a legitimately strong feature; in the simulation prior_refunds is strong and legitimate.
- The remaining 0.03 gap may be label delay, population shift, a second leak or a sampling difference.
- Fixing the feature but not the process lets the next one in.
- Old releases may have taught downstream users to rely on a score level that is now different.

**What the interviewer scores:**
- Strong: defines leakage by timestamp and builds a gate on it. Weak: "check for correlation with the label".
- Strong: honest message to stakeholders with numbers and no names. Weak: hiding it or blaming the teammate.
- Strong: notices that 0.84 versus 0.81 is still a gap. Weak: declares victory after one feature.
- Strong: estimates harm from online data for each release.

**Example:** Illustrative numbers. Offline AUC 0.93, online 0.81: gap 0.12. After dropping ticket_reopened offline AUC is 0.84, so the feature carried 0.09 AUC. In my synthetic run the all-features AUC is 0.931 and 0.846 without the feature, ticket_reopened has the biggest drop-one loss (0.085, next 0.021) and is the only feature where values arrive after the decision.
- Weak answer: "I would drop features that are too correlated with the target."
- Strong answer: "Correlation would also drop prior_refunds, which is honest. I check when each value is written compared with the decision time, I run drop-one ablation as a pointer, and I make the timestamp check a CI gate so a leak cannot ship again. For the three releases I report the inflated offline number, the real online result and what we fix."

**Code:**
```python
# Q24: finding a leaky feature (ticket_reopened). Synthetic, seeded, illustrative.
import numpy as np
rng = np.random.default_rng(24)
N = 40_000
y = (rng.random(N) < 0.3).astype(int)
def auc(y, s):
    r = s.argsort(kind="stable").argsort() + 1
    n1 = y.sum(); n0 = len(y) - n1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))
# 8 legitimate features known before the decision; one strong but legitimate; one leaky binary
names = [f"f{i}" for i in range(7)] + ["prior_refunds", "ticket_reopened"]
X = np.column_stack([rng.normal(0.42 * y, 1) for _ in range(7)] + [rng.normal(0.9 * y, 1)] +
                    [(rng.random(N) < np.where(y == 1, 0.70, 0.07)).astype(float)])
# when each feature becomes available, relative to the decision (minutes; negative = before the decision)
avail = np.column_stack([np.full(N, -60.0)] * 8 + [rng.uniform(300, 5000, N)])   # reopen happens days later
def fit_auc(cols):
    tr, te = slice(0, 30_000), slice(30_000, N)
    A = np.column_stack([np.ones(N), X[:, cols]])
    w = np.zeros(A.shape[1])
    for _ in range(12):                                      # IRLS for logistic regression
        p = 1 / (1 + np.exp(-A[tr] @ w)); W = p * (1 - p)
        w += np.linalg.solve(A[tr].T @ (A[tr] * W[:, None]) + 1e-6 * np.eye(len(w)), A[tr].T @ (y[tr] - p))
    return auc(y[te], A[te] @ w)
all_cols = list(range(9)); no_leak = list(range(8))
a_all, a_clean = fit_auc(all_cols), fit_auc(no_leak)
print(f"AUC all features = {a_all:.3f}; without ticket_reopened = {a_clean:.3f}; drop = {a_all - a_clean:.3f}")
assert abs(a_all - 0.93) < 0.015 and abs(a_clean - 0.84) < 0.015
# test 1: single-feature AUC (flags suspicious, does not prove leakage)
single = {n: auc(y, X[:, i]) for i, n in enumerate(names)}
for n, v in sorted(single.items(), key=lambda kv: -kv[1])[:3]: print(f"single-feature AUC {n:16} {v:.3f}")
# test 2: drop-one ablation (how much does each feature carry on top of the rest)
drops = {n: a_all - fit_auc([c for c in all_cols if c != i]) for i, n in enumerate(names)}
worst = max(drops, key=drops.get)
print(f"largest drop-one loss: {worst} ({drops[worst]:.3f}); next: {sorted(drops.values())[-2]:.3f}")
assert worst == "ticket_reopened" and drops[worst] > 2.5 * sorted(drops.values())[-2]
# test 3: the definitive check, availability time versus decision time (the automatic gate)
late = {n: float((avail[:, i] > 0).mean()) for i, n in enumerate(names)}
flagged = [n for n, v in late.items() if v > 0.01]
print("features with values arriving after the decision:", flagged)
assert flagged == ["ticket_reopened"]
# prior_refunds is strong on its own but legitimate: test 1 alone would wrongly accuse it too
assert single["prior_refunds"] > 0.68 and "prior_refunds" not in flagged
# arithmetic quoted in the text
assert round(0.93 - 0.81, 2) == 0.12 and round(0.93 - 0.84, 2) == 0.09 and round(0.84 - 0.81, 2) == 0.03
print("offline minus online: 0.12 before the fix; 0.03 remains after the fix and still needs an explanation")
```

**Output (my run):**
```text
AUC all features = 0.931; without ticket_reopened = 0.846; drop = 0.085
single-feature AUC ticket_reopened  0.813
single-feature AUC prior_refunds    0.737
single-feature AUC f2               0.620
largest drop-one loss: ticket_reopened (0.085); next: 0.021
features with values arriving after the decision: ['ticket_reopened']
offline minus online: 0.12 before the fix; 0.03 remains after the fix and still needs an explanation
```

The data are synthetic; the two ablation numbers will differ on real tables.

**Follow-ups:**
- Is ticket_reopened ever fine? Only if it is known at decision time, for example in a later re-decision; then it is a different problem.
- How do you check target leakage inside time-based CV? Use a time-ordered split, so features built from the future cannot cross the cut; see Book 6 Part 2 for the production-degradation angle (Book 6 Part 2 Q1: "A fraud classifier launched with an offline AUC of 0.86...").
- What about features that proxy the label (for example a refund-approved flag)? Same test: not available before the decision means drop.

**Common mistakes:** Checking correlation only. Blaming the teammate. Forgetting the earlier releases. Treating the fix as complete while a 0.03 gap remains. Not building an automated gate.

### Q25 ⭐⭐ 🟡 A feature pipeline was broken for 9 daily partitions. Each partition takes 40 minutes, the cluster can run 4 partitions at once, and a rolling 7-day feature may make each day depend on the stored output of the previous day. Compute the backfill wall-clock time if the days were independent and if they must run in order, and say how you would order the work, protect live jobs and validate the result.
**Asked at:** Data-pipeline pages (luminousmen on avoidable backfills and non-idempotent jobs, DZone on silent upstream schema change, HackerNoon and Seattle Data Guy on silent pipeline failures, DataExpert on schema drift and idempotent replays, DataVidhya on measuring detection latency in postmortems); practitioner blogs rather than an interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** If the 9 days were independent it is 3 waves of 40 minutes, 120 minutes; if each day must wait for the previous one it is 9 x 40 = 360 minutes and extra slots do not help; so I first check whether the rolling feature really reads yesterday's output or can be rebuilt from raw daily data.
(A rolling 7-day feature only forces an order if it reads the stored output of the previous day; a window computed from raw events is independent per day.)

**Clarifying questions:**
- Does day d read raw data for d-6 to d, or the stored feature output of d-1? Why: this is the difference between 120 and 360 minutes.
- Is the raw input for the 9 days healthy, or was the input the thing that broke? Why: if raw data is bad, the backfill must wait for the source to be repaired.
- Who reads this feature now, and what happens to models and scores built on the 9 bad days? Why: it decides whether downstream jobs need to be re-run after the backfill.
- How much of the 4-slot cluster can the backfill use without hurting live jobs? Why: capping at 2 slots turns 120 minutes into 200.
- Is the job idempotent (overwrite a partition, not append)? Why: a backfill that appends doubles rows.

**Approach:**
1. First 15 minutes. Stop the bleeding: freeze or flag the 9 bad partitions so models and dashboards do not read them as good (or make readers fall back to the last good value). Fix the root cause first or the backfill will break again.
2. First day. Establish the dependency: read the job logic. Plan A (independent): compute 9 daily aggregates in parallel in 3 waves (120 minutes), then the 7-day window per day as a cheap second stage (about 138 minutes if each merge takes 2 minutes, which is an assumption). Plan B (incremental): run strictly in date order, 360 minutes, and use the time to shrink what must run (for example start from the last good day).
3. Order the work: oldest broken day first when order matters; when independent, run in date order anyway so a failure leaves a clean prefix of fixed days.
4. Protect live jobs: put the backfill in its own queue or pool, cap at 2 of 4 slots (200 minutes for independent days), lower priority than the daily live run, and run when load is low. Throttle on cluster load, not on a fixed clock.
5. Write to a staging location per partition and swap in only after validation (atomic partition swap), so readers never see half a repair. Make every partition idempotent: overwrite by date.
6. Validate the result: row counts inside a band around healthy neighbours (illustration in the code catches an empty and a tiny partition), null rates and distributions against neighbours, recompute one healthy day and check it matches the stored value exactly, and compare a few known customers by hand.
7. After validation: tell downstream owners which dates changed and re-run anything built on them (training sets, scores, reports).
8. Next quarter: add a freshness and volume check on every partition (the 9 days should have been caught on day 1, not at day 9), a documented backfill runbook with the dependency type, and a periodic backfill drill. Measure detection delay: time from first broken partition to alert.
9. Escalation: if validation fails twice or the live jobs miss their SLO during the backfill, stop, cap lower and page the data platform owner. Blameless angle: record that nothing checked partition volume, not who pushed the change that broke it.

**Metrics:**
- Backfill wall-clock = ceil(partitions / slots) x duration for independent days (ceil(9/4) x 40 = 120), or partitions x duration for a chain (9 x 40 = 360).
- Live job impact: delay of the live run versus its normal finish time while the backfill runs (guardrail).
- Validation pass rate per partition, and the detection delay (days the data was broken before alert).
- Share of downstream consumers re-run.

**Risks:**
- Assuming independence wrongly: a backfill that reads half-fixed outputs gives silently wrong values.
- Appending instead of overwriting duplicates data.
- Backfill saturating the cluster and starving the live run.
- Fixing the pipeline but leaving models trained on the bad 9 days.
- Durations are not constant under contention; 40 minutes may stretch when 4 jobs run at once.

**What the interviewer scores:**
- Strong: both numbers (120 and 360), and challenges whether the dependency is real. Weak: only multiplies 9 by 40.
- Strong: idempotent, staged, validated, swapped in. Weak: "rerun the DAG".
- Strong: protects live work with a cap and shows the cost (200 minutes). Weak: ignores the live jobs.
- Strong: asks why 9 days went unnoticed and adds a check.

**Example:** Illustrative numbers. Independent: 9 partitions on 4 slots finish as waves of 4, 4 and 1 partitions, 3 x 40 = 120 minutes. Strict chain: 9 x 40 = 360 minutes. Capped at 2 slots for the live jobs: waves of 2,2,2,2,1, 5 x 40 = 200 minutes.
- Weak answer: "It is 9 times 40, so 6 hours; I will start the backfill now."
- Strong answer: "That is 6 hours only if each day reads yesterday's output. If the window is computed from raw data it is 120 minutes on 4 slots, or 200 if I leave half the cluster for live jobs. I would check that first, then validate row counts and swap partitions in only when they pass."

**Code:**
```python
# Q25: backfill wall-clock time for 9 partitions. Exact scheduling arithmetic, illustrative durations.
import heapq, math
DUR, N_PART = 40, 9
def makespan(n_parts, slots, deps):
    """List scheduling: deps[i] = set of partitions that must finish before i starts. Returns (finish time, per-partition finish)."""
    done, running, t = {}, [], 0
    pending = list(range(n_parts))
    while pending or running:
        started = True
        while started:
            started = False
            for i in list(pending):
                if len(running) < slots and all(d in done and done[d] <= t for d in deps[i]):
                    heapq.heappush(running, (t + DUR, i)); pending.remove(i); started = True
        fin, i = heapq.heappop(running)
        t = fin; done[i] = fin
        while running and running[0][0] == fin:
            _, j = heapq.heappop(running); done[j] = fin
    return t, done
indep = {i: set() for i in range(N_PART)}
chain = {i: ({i - 1} if i else set()) for i in range(N_PART)}
t_ind4, _ = makespan(N_PART, 4, indep)
t_ord4, _ = makespan(N_PART, 4, chain)
print(f"independent, 4 slots: {t_ind4} min = {t_ind4/60:.1f} h   (waves: {math.ceil(N_PART/4)})")
print(f"strict chain, 4 slots: {t_ord4} min = {t_ord4/60:.1f} h   (extra slots do not help)")
assert t_ind4 == 3 * 40 == 120 and t_ord4 == 9 * 40 == 360
# live jobs need room: cap the backfill at 2 slots (independent case) or 1
t_ind2, _ = makespan(N_PART, 2, indep); t_ind1, _ = makespan(N_PART, 1, indep)
print(f"independent, capped at 2 slots: {t_ind2} min; at 1 slot: {t_ind1} min")
assert t_ind2 == 5 * 40 == 200 and t_ind1 == 360
# a rolling 7-day window computed from RAW daily data does not need the chain: compute 9 daily aggregates in parallel, then window
t_roll_cheap = 3 * DUR + 9 * 2          # 9 cheap window merges of 2 minutes each, run serially after the aggregates
print(f"two-stage plan: 9 daily aggregates (120 min) + 9 window merges of 2 min each = {t_roll_cheap} min (merge cost is an assumption)")
assert t_roll_cheap == 138
# only an INCREMENTAL feature (day d reads the stored output of day d-1) forces the chain
assert t_ord4 / t_ind4 == 3.0
# validation: partition row counts must sit inside a band around the healthy neighbours (illustrative counts)
healthy = [1_000_400, 998_900, 1_001_700, 999_300]
rebuilt = [1_000_900, 999_500, 0, 1_002_000, 7_300]          # 0 and 7,300 are suspicious
lo, hi = 0.95 * min(healthy), 1.05 * max(healthy)
bad = [i for i, n in enumerate(rebuilt) if not lo <= n <= hi]
print("partitions failing the row-count band:", bad)
assert bad == [2, 4]
```

**Output (my run):**
```text
independent, 4 slots: 120 min = 2.0 h   (waves: 3)
strict chain, 4 slots: 360 min = 6.0 h   (extra slots do not help)
independent, capped at 2 slots: 200 min; at 1 slot: 360 min
two-stage plan: 9 daily aggregates (120 min) + 9 window merges of 2 min each = 138 min (merge cost is an assumption)
partitions failing the row-count band: [2, 4]
```

Slot durations are taken as constant 40 minutes, so real runs on a busy cluster can be longer.

**Follow-ups:**
- How do you shorten a true chain? Checkpoint the state at day boundaries, or rewrite the feature so a day is computed from raw data and a cheap merge; only then can days run in parallel.
- What if one partition fails mid-backfill? Because each partition is idempotent and swapped in on its own, you re-run only that date.
- How do you decide the cap for live jobs? Measure the live job's headroom; start at half the slots and watch its delay.

**Common mistakes:** Multiplying 9 by 40 without checking the dependency. Appending rather than overwriting. Using all slots and starving live jobs. Publishing before validation. Forgetting to re-run models built on the bad days.

### Q26 ⭐⭐ 🟡 An engineer promoted version 38 of a model, out of 41 registered versions, believing it came from the full-data experiment, but it was trained on a 5% sample and nobody noticed for two days. The registry only stores a name, a version number and a metric. What metadata and promotion checks would you require, who can promote, and how do you find any other mislabelled versions?
**Asked at:** Model-registry and rollback pages (oneuptime and mljar rollback runbooks that move a 'champion' alias or demote a Production stage, a Towards AI piece on registries as the source of truth); secondary practitioner material, no located public incident; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** First I move the alias back to the last version whose training I can prove, then I require lineage metadata (code, data, rows, sampling fraction, holdout) for every version, let only the pipeline plus a second person promote, and audit the other 40 versions from the experiment-tracking runs.

**Clarifying questions:**
- Is version 38 serving traffic now, and what is the last version with known lineage? Why: it decides whether I roll back this minute.
- Does an experiment-tracking run (logs, parameters, row counts) exist for each version even though the registry does not hold them? Why: that is where the audit gets its facts.
- How was the 5% sample used (a dev shortcut left on)? Why: it shows which control was missing, for example an unreviewed config flag.
- Who can promote today, and is any approval recorded? Why: it defines the access change.
- What decisions were made on version 38's metric during the two days? Why: the harm may be in reports, not only in traffic.

**Approach:**
1. First 15 minutes. Check live metrics for version 38 (error rate, score distribution, business metric). If the model is worse or unverifiable, move the serving alias back to the last version with proven lineage (rollback is moving the alias, so it is quick; Book 4, Part 4 has "MLflow Model Registry: registered models, versions, aliases and the deprecated stages" for the mechanics). Page the model owner. Freeze promotions for the model name.
2. First day. Audit: for all 41 versions pull training row count, data snapshot ID, code commit and config from the experiment-tracking runs; flag any version trained on far fewer rows than the median (the simulation flags versions 12 and 38) and any version with no run attached. Mark flagged versions in the registry (tag, not delete). Estimate exposure: at an illustrative 100 requests per second, 48 hours is 17,280,000 requests.
3. First day. Postmortem, blameless: the registry accepted "name, number, metric" and a human's belief; a sampled config was one flag away from production; promotion needed one person. Timeline, contributing causes, actions.
4. Next quarter. Required metadata on every version: git commit, data version, train_rows, sampling_fraction, evaluation holdout ID and metric, training config hash, trainer, approver, environment. Promotion checks (automated, in CI): all fields present; sampling_fraction equals 1.0 (or a documented exception); train_rows within 80% of the expected size; metric measured on the frozen holdout, not the training set; metric not worse than the current champion by more than a stated tolerance; trainer is not the approver.
5. Who promotes: the pipeline service account moves the alias after the checks pass and one named approver (model owner) signs; engineers cannot move the production alias by hand; every move is logged with who, when, and from which version (Book 4, Part 4 has "Governing the model registry beyond aliases" for tags, permissions and the audit question).
6. Escalation: a version that fails lineage after being promoted is rolled back at once; tell product and risk owners if decisions were made on its output.
7. Find other mislabelled versions: the audit in step 2, then a monthly job that re-verifies lineage for every Production and Staging version.

**Metrics:**
- Lineage completeness = versions with all required fields / all versions (today 0 of 41, target 100%).
- Train-rows ratio = train_rows / expected full rows (version 38: 200,000 / 4,000,000 = 5%).
- Exposure = requests served by an unverified version.
- Time to detect = promotion time to detection (two days here).
- Guardrail: promotions blocked by the gate that were legitimate (so the gate does not become something people bypass).

**Risks:**
- The metric hid the problem: by construction in the simulation, the 5% model's metric sits in the same band as the others.
- Metadata typed by hand can lie; fill it from the pipeline, not from a form.
- A gate with too many manual exceptions becomes noise.
- Flagging by row count misses a mislabelled version trained on stale rather than small data; check data version too.
- Deleting suspect versions destroys evidence; tag them.

**What the interviewer scores:**
- Strong: rolls back first, audits the rest, then fixes process. Weak: only fixes version 38.
- Strong: lists specific fields and checks, ties them to this failure (sampling fraction, row count). Weak: "add more documentation".
- Strong: separation of duties and automated promotion. Weak: "tell people to be careful".
- Strong: blameless language about a registry that stores a number but not a provenance.

**Example:** Illustrative numbers. 41 versions, the full dataset has about 4,000,000 rows. Version 38 trained on 200,000 (5%). The audit flags any version below half the median training size and finds 38, and also a forgotten 1% smoke test, version 12. At 100 requests per second, 48 hours of serving is 17,280,000 requests.
- Weak answer: "I would ask the team to be careful which experiment they promote and add a note to the registry."
- Strong answer: "I roll back to the last version I can prove, then I audit all 41 versions from the run logs, and I make promotion fail unless commit, data version, row count and sampling fraction are recorded and a second person approves."

**Code:**
```python
# Q26: promotion gate and registry audit. Plain Python, illustrative numbers; not tied to any registry product.
import random
random.seed(26)
FULL_ROWS = 4_000_000
# 41 registered versions; row counts come from the experiment-tracking run, not from the registry (the registry only has name, number, metric)
versions = []
for v in range(1, 42):
    rows = int(FULL_ROWS * random.uniform(0.9, 1.05))
    versions.append({"version": v, "metric": round(random.uniform(0.80, 0.84), 3), "rows": rows})
versions[37]["rows"] = int(FULL_ROWS * 0.05)           # version 38: the 5% sample
versions[11]["rows"] = int(FULL_ROWS * 0.01)           # version 12: a 1% smoke-test run nobody else knew about
assert versions[37]["version"] == 38 and versions[37]["rows"] == 200_000
# 1) audit: any version trained on far fewer rows than the median
rows_sorted = sorted(v["rows"] for v in versions)
median = rows_sorted[len(rows_sorted) // 2]
flagged = [v["version"] for v in versions if v["rows"] < 0.5 * median]
print(f"median training rows = {median:,}; flagged versions (below 50% of median): {flagged}")
assert flagged == [12, 38]
# 2) exposure of the mistake: two days at an illustrative 100 requests per second
exposed = 100 * 48 * 3600
print(f"requests served by version 38 in 48 hours at 100 rps: {exposed:,}")
assert exposed == 17_280_000
# 3) the promotion gate: required metadata, sanity bounds, separation of duties
REQUIRED = ["git_commit", "data_version", "train_rows", "sampling_fraction", "holdout_id", "holdout_metric", "trainer", "approver"]
def gate(meta, expected_rows=FULL_ROWS):
    errs = [f"missing {k}" for k in REQUIRED if meta.get(k) in (None, "")]
    if errs: return errs
    if meta["sampling_fraction"] < 1.0: errs.append("trained on a sample")
    if meta["train_rows"] < 0.8 * expected_rows: errs.append("train_rows below 80% of expected")
    if meta["trainer"] == meta["approver"]: errs.append("trainer cannot approve own promotion")
    return errs
good = dict(git_commit="a1b2c3", data_version="d41", train_rows=4_020_000, sampling_fraction=1.0, holdout_id="h7",
            holdout_metric=0.83, trainer="asha", approver="ravi")
v38 = dict(good, train_rows=200_000, sampling_fraction=0.05)
legacy = {"name": "m", "version": 38, "metric": 0.81}            # what the registry stores today
print("good candidate:", gate(good))
print("version 38 as it should have been recorded:", gate(v38))
print("version 38 as the registry stores it:", gate(legacy)[:3], "...", len(gate(legacy)), "missing fields")
assert gate(good) == [] and "trained on a sample" in gate(v38) and len(gate(legacy)) == 8
assert gate(dict(good, approver="asha")) == ["trainer cannot approve own promotion"]
# 4) a green metric on the old holdout is not evidence of the training data: same metric range for both
print("metric alone cannot find it: v38 metric", versions[37]["metric"], "vs median metric", sorted(v["metric"] for v in versions)[20])
assert 0.80 <= versions[37]["metric"] <= 0.84
```

**Output (my run):**
```text
median training rows = 3,913,644; flagged versions (below 50% of median): [12, 38]
requests served by version 38 in 48 hours at 100 rps: 17,280,000
good candidate: []
version 38 as it should have been recorded: ['trained on a sample', 'train_rows below 80% of expected']
version 38 as the registry stores it: ['missing git_commit', 'missing data_version', 'missing train_rows'] ... 8 missing fields
metric alone cannot find it: v38 metric 0.819 vs median metric 0.822
```

Registry products differ; no product-specific feature was run here. All row counts and metrics are invented.

**Follow-ups:**
- Can a model signature or metric hash prove the data? No; it proves the artifact, not what it was trained on. Record the data snapshot ID.
- What about an alias that moves automatically? Gate the move: the pipeline moves it, and only when the checks pass.
- How do you stop a sampled config reaching production? Put sampling behind an explicit flag that the gate reads, and make the default full data.

**Common mistakes:** Trusting a metric as provenance. Deleting the bad version rather than tagging it. Fixing only version 38. Letting the trainer approve their own model. Relying on a wiki page for metadata.

### Q27 ⭐⭐ 🟡 A postmortem for a bad model deploy lists 14 action items and 11 of them (79% of the 14) say 'be more careful' or 'add a review'. The manager wants the engineer who merged the change named in the report. How do you run the meeting, what makes an action item good, and how do you turn the 11 into changes that do not rely on people remembering?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to blameless postmortems and incident-review practice; related topics appear in public MLOps guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** I run it as a blameless review that names the change and the roles, not the person, and I turn each "be more careful" into a check that a machine enforces, with an owner, a date and a test for done.
(Note on the numbers: 11 of 14 is 78.6%, which the prompt rounds to 79%.)

**Clarifying questions:**
- What did the bad deploy cost and how long did it last? Why: it sets the severity and how many action items are justified (the numbers in the Example are illustrative).
- What does the manager actually need: accountability, a performance conversation, or confidence it will not recur? Why: each has a better home than the postmortem report.
- Was the engineer following the documented process? Why: if yes, the process failed, not the person.
- What did the engineer say at the time, and was anyone else in the chain (reviewer, approver)? Why: it tests whether the system relied on one pair of eyes.
- Who owns the action items and has capacity to do them? Why: unowned items do not get done.

**Approach:**
1. Before the meeting (day 1-2). Build the timeline from logs and chat: deploy at 14:00, detected at 14:47 (47 minutes), rollback finished at 15:05 (18 minutes after detection), total harm window 65 minutes (illustrative numbers, computed in the code). Share it in advance. Talk to the engineer first, privately, so there are no surprises.
2. The meeting (60 minutes, a facilitator who is not the manager). Rules said out loud: we describe what happened and what made it seem reasonable at the time; we look at conditions, not character. Walk the timeline, ask "what did we know, what did the tools tell us, what was missing", and list contributing factors (no gate, no canary, alert late). Stop each "why" chain at something we can change.
3. The manager's request. Do not name the engineer in the report as the cause. Name the change (pull request or commit ID) and the roles ("the author", "the reviewer"). Explain why: naming people teaches everyone to hide near-misses; it does not fix the cause, and the next engineer would have merged the same change. Offer what the manager really needs: a clear owner for each fix (accountability for the repair), a separate and private performance route if there was a real conduct issue, and visible progress on the fixes.
4. Action items, what makes one good: it fixes a condition, it names an owner (a role or person who agreed), a due date, a mechanism (a check, a gate, an alert, a limit), and a "done when" test someone can run. Keep to a few high-value items; 14 is too many to finish.
5. Turn the 11: for each "be more careful" ask what check would have stopped it, then build it: CI gates, required checks and code owners, schema and unit contracts, rollout tool with fixed stage sizes, auto-rollback rules, alert thresholds as code with replay tests, a registry of data sources. The code shows the 11 rewritten items, each with a mechanism and a done-when line that contains none of the vague wording. Keep a "review" only where it is cheap and has a checklist and the reviewer sees the evidence (a diff, the gate report).
6. First day after: owners and dates on the tracker. Next quarter: a review of how many items closed, and whether any new incident repeated an old cause. Track it.
7. Rollback and escalation, written down: auto-rollback at the stated error or latency thresholds; the on-call can roll back without asking; escalate to the service owner if not restored within 15 minutes.

**Metrics:**
- Action-item closure rate = closed on time / total, per quarter.
- Share of items with a mechanism, owner, date, done-when test (11 of 14 start with none; target 100%).
- Repeat-cause rate = incidents whose cause matches an earlier postmortem / all incidents.
- Detection delay (47 minutes) and time to mitigate (18 minutes) per incident.
- Guardrail: near-miss reports per quarter; falling to zero after naming someone is a warning sign.

**Risks:**
- A blame-free meeting that ends with "no one was responsible" gives no ownership. Owners for fixes are the accountability.
- Too many items; the team closes the easy ones.
- New gates people bypass because they are slow; measure bypass.
- Naming the engineer anyway because the manager insists; escalate to a senior engineer or director with the reasoning.

**What the interviewer scores:**
- Strong: names the change, not the person, and explains why in terms of what gets fixed. Weak: either gives in to the manager or lectures about blame.
- Strong: turns "be careful" into automated checks with owners and dates. Weak: "assign a reviewer".
- Strong: handles the manager with a better offer (ownership of fixes), not a refusal. Weak: confrontational.
- Strong: timeline and numbers (detection delay, time to mitigate).

**Example:** Illustrative numbers. 14 items; 11 are vague (78.6%). "Add a review for schema changes" becomes "ingest fails when a column type, range or unit changes; owner data engineering; due in 30 days; done when a test changes a column type and the pipeline stops".
- Weak answer: "Fine, I will put the engineer's name in the report and add that everyone should be more careful."
- Strong answer: "I will write that PR 482 shipped without a gate, list the roles involved, and give you an owner and a date for every fix. Naming the person tells everyone to hide the next near-miss. If there is a conduct issue, that is a separate private conversation."

**Code:**
```python
# Q27: classify postmortem action items and rewrite the vague ones. Illustrative items, plain Python.
vague_words = ("be more careful", "add a review", "remind", "double-check", "pay more attention")
items = [
 "Be more careful when changing feature code",
 "Add a review for every model deploy",
 "Remind the team to check the holdout before promoting",
 "Double-check the config before merge",
 "Add a review for schema changes",
 "Be more careful with the canary percentage",
 "Add a review step for rollback decisions",
 "Pay more attention to the dashboard after a deploy",
 "Add a review of alert thresholds",
 "Be more careful to run the replay test",
 "Add a review for data-source changes",
 "Block promotion in CI when holdout AUC is more than 0.02 below the champion (owner: MLOps, due 2026-11-30)",
 "Auto-rollback when the canary error z-score is 3 or more (owner: platform, due 2026-12-15)",
 "Alert when feature null-rate changes by more than 5 points in an hour (owner: data eng, due 2026-11-20)",
]
vague = [i for i in items if any(w in i.lower() for w in vague_words)]
print(f"{len(vague)} of {len(items)} items are vague = {len(vague)/len(items):.1%}")
assert len(items) == 14 and len(vague) == 11 and round(100 * 11 / 14) == 79
# rewrite table: vague item -> mechanism that does not depend on memory
rewrite = {
 0:  ("Contract test on the feature code in CI", "CI blocks merge when feature definitions differ between train and serve"),
 1:  ("Required status check plus CODEOWNERS on deploy config", "merge button disabled without model-owner approval and a green gate"),
 2:  ("Promotion pipeline step compares holdout AUC with champion", "promotion fails if AUC is more than 0.02 below champion"),
 3:  ("Config schema validation in CI", "unknown or out-of-range keys fail the build"),
 4:  ("Schema and unit contract check on upstream tables", "ingest fails loudly on a changed type, range or unit"),
 5:  ("Rollout tool enforces stage sizes", "stages fixed at 5, 25, 50, 100 percent; larger jumps rejected"),
 6:  ("Written rollback rule in the runbook and the deploy tool", "rollback triggers fire automatically on the stated thresholds"),
 7:  ("Post-deploy watch as an automatic 30-minute gate", "deploy marked complete only after dashboards stay green for 30 minutes"),
 8:  ("Alert thresholds stored as code with tests", "a threshold change needs a replay of 8 weeks of history in CI"),
 9:  ("Shadow replay test runs on every release candidate", "release candidate blocked if replay differs by more than a stated tolerance"),
 10: ("Data-source registry with owners and change notices", "unregistered source in a pipeline fails validation"),
}
def good(item):
    """An action item is good when it has an owner, a date, a mechanism and a way to check it is done."""
    return all(k in item for k in ("owner", "due", "mechanism", "done_when"))
rewritten = []
for idx, (mech, done_when) in rewrite.items():
    rewritten.append({"from": items[idx], "owner": "role: platform/MLOps/data eng", "due": "within 90 days", "mechanism": mech, "done_when": done_when})
assert len(rewritten) == 11 and all(good(r) for r in rewritten)
assert not any(w in r["mechanism"].lower() + r["done_when"].lower() for r in rewritten for w in vague_words)
assert not any(good({"item": i}) for i in vague)                  # the vague wording alone fails the test
print(f"after rewrite: {len(rewritten)} items now have an owner role, a date, a mechanism and a done-when test")
# an illustrative timeline: detection delay and time to mitigate
deploy, detect, rollback_start, rollback_done = 14*60, 14*60+47, 14*60+52, 15*60+5     # minutes after midnight
print(f"detection delay {detect-deploy} min, decision to rollback done {rollback_done-detect} min, total harm window {rollback_done-deploy} min")
assert (detect - deploy, rollback_done - detect, rollback_done - deploy) == (47, 18, 65)
```

**Output (my run):**
```text
11 of 14 items are vague = 78.6%
after rewrite: 11 items now have an owner role, a date, a mechanism and a done-when test
detection delay 47 min, decision to rollback done 18 min, total harm window 65 min
```

All items and times are invented for illustration.

**Follow-ups:**
- Is blameless the same as no accountability? No: accountability moves from "who caused it" to "who owns the fix".
- When is a human review right? When the reviewer gets evidence and a checklist, the review is fast, and it backs an automated gate rather than replacing it.
- What if the same engineer repeats mistakes? That is a coaching or performance matter handled privately, after checking the system was not at fault.

**Common mistakes:** Naming the engineer in the report. Closing with "be more careful". Items with no owner or date. Fourteen items and no priority. Adding a slow review instead of an automatic check. Skipping the private conversation with the engineer first.

### Q28 ⭐⭐ 🟡 A GPU service handles 400 requests per second against a capacity of 500, and traffic jumps to 900 per second. New pods need 90 seconds to load the model, and the autoscaler reacts to CPU, which stays low because the work is GPU-bound. Compute the backlog that builds in the 90 seconds before new capacity arrives, and say what you scale on instead and how you protect users meanwhile.
**Asked at:** GPU-serving and autoscaling pages (apxml and system-design.space on autoscaling and serving architecture; vendor pages from regolo.ai and lyceum.technology on cold starts and capacity, treated as vendor claims); no public postmortem located; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** The backlog is (900 - 500) x 90 = 36,000 requests, a 72-second wait for the last one, so CPU is the wrong signal: I scale on queue depth or in-flight requests per pod, shed load past a 2-second wait, and keep warm headroom for a 2.25x jump.

**Clarifying questions:**
- What does one pod serve, and how many pods do we run now? It sets the pod count to ask for (illustrative: 125 req/s per pod, 4 pods = 500).
- Is the 90 seconds only model load, or does it also include scheduling and image pull? Detection lag adds to it, so the real gap is longer.
- What is the client timeout and is the request idempotent? It sets how deep a queue is worth keeping, and whether retries are safe.
- Can the cluster actually get more GPUs right now (quota, spot stock)? If not, scaling is not a plan, shedding is.
- Is there a cheaper fallback (smaller model, cached answer)? It turns a failed request into a degraded one.
- Who owns the page at 3 a.m.? The escalation path decides the first 15 minutes.

**Approach:**
1. First 15 minutes: confirm it is a capacity problem (queue depth up, GPU utilisation near 100%, CPU flat). Turn on load shedding with a bounded queue (about 2 seconds of work). Manually add pods to the target (10 pods, not 8). Tell the owner of the caller what is being degraded.
2. Backlog arithmetic (no shedding): 900 arrive, 500 are served, 400 per second pile up for 90 seconds = 36,000. With 15 seconds of detection lag it is 42,000. The last queued request waits 36,000 / 500 = 72 seconds, so almost all of them would time out anyway.
3. Drain is the part people forget. Once new capacity lands, the surplus is only (new capacity - 900). With 8 pods (1,000/s) the 42,000 backlog takes 420 seconds to drain. With 10 pods (1,250/s) it takes 120 seconds. Overshoot on purpose.
4. Protect users meanwhile: a bounded queue (queue limit = capacity x timeout = 1,000), a fast 429 or 503 with Retry-After, priority classes (paid or interactive first), and a fallback model for the shed share. With the queue bounded, my simulation serves 45,000, queues 1,000 and sheds 35,000 of 81,000 arrivals (43.2%). That is bad, but fast and honest, and it stops the queue from poisoning the next 5 minutes.
5. First day: change the autoscaler signal. Scale on queue depth, in-flight requests per pod, or GPU utilisation, with a target of about 60-70% so a pod is never the last to know (HPA custom-metrics wiring is editor knowledge, not tested here). Raise the minimum replicas, and test pod start time (model load 90 seconds can be cut with a warm image cache or a pre-loaded standby pool).
6. Next quarter: load-test a 2.25x step, schedule known peaks, and add a capacity row to the on-call dashboard. Keep standby cost against loss: 4 extra pods at 10 units per pod-hour = 960 per day, against 1,750 lost per spike (illustrative), so it pays back at about 0.55 spikes per day.
7. Blameless postmortem: the question is not who picked CPU, it is why the default metric looked fine. Timeline, the 90-second gap, what the signal missed, and action items with an owner and a date (signal change, minimum replicas, load test, runbook).

**Escalation and rollback criteria (illustrative, written before the incident):**
- Shed when predicted queue wait is over 2 seconds.
- If no new pod is Ready 120 seconds after the scale-up, add pods by hand.
- If GPU quota blocks the scale-up, page the cloud capacity owner and move to the fallback model.
- Roll back any autoscaler change if p95 latency or the error rate is worse than before the change for 10 minutes.

**Metrics:**
- Backlog = (arrival rate - service rate) x seconds until new capacity serves. Numerator requests, denominator none; report it in requests and in seconds of wait.
- Queue wait p95 = 95th percentile of time between arrival and start of service. Guardrail: under the client timeout.
- Shed share = shed requests / arrivals in the incident window (43.2% in the simulation). Guardrail: below an agreed cap, with fallback share reported next to it.
- Scale lag = time from load step to the first new pod Ready (here 15 + 90 = 105 seconds).
- Drain time = backlog / (new capacity - arrival rate).
- Guardrails: GPU utilisation per pod, error rate, cost per hour.

**Risks:**
- Retry storms: clients retry the 503s and make 900 into 1,500. Use jittered backoff and a retry budget.
- Scaling to exactly the arrival rate: the drain never finishes (new capacity 900 against 900 arrivals).
- A cluster-level GPU shortage turns "scale up" into nothing.
- Autoscaler flapping: scale-down too fast re-creates the problem 5 minutes later.
- The fallback model has its own quality and cost profile.

**What the interviewer scores:**
- Strong: gets 36,000 straight, then notices the drain time and detection lag. Weak: stops at "add more pods".
- Strong: names the wrong signal (CPU) and the right ones (queue depth, in-flight, GPU utilisation). Weak: "tune the CPU threshold lower".
- Strong: protects users with a bounded queue, shedding and a fallback. Weak: lets the queue grow until timeouts.
- Strong: gives the order (15 minutes, day, quarter) and who gets paged. Weak: a bag of tools with no order.
- Strong: blameless, system-focused postmortem. Weak: blames the autoscaler config owner.

**Example:** Illustrative numbers: 4 pods x 125 = 500 req/s, traffic 400 jumps to 900. Weak: "I would scale out when CPU is high; it takes a minute or so for pods to start." Strong: "The gap is 400 requests a second for 90 seconds, so 36,000 requests, and the last waits 72 seconds, which is past any timeout. I cap the queue at 2 seconds, shed the rest with a 503, and ask for 10 pods, not 8, because 8 would take 7 minutes to drain. Then I move the autoscaler to queue depth."

**Code:**
```python
# Illustrative numbers only. Backlog, drain time, shedding and cost for a GPU service during a traffic jump.
import math
base, cap, peak, load_s = 400, 500, 900, 90
per_pod = 125                       # req/s one GPU pod can serve (illustrative)
assert cap // per_pod == 4
# 1. Backlog with no shedding: arrivals minus service for 90 s.
backlog = (peak - cap) * load_s
assert backlog == 36000
wait_last = backlog / cap           # seconds the last queued request waits at t=90
assert wait_last == 72.0
# 2. Real timeline: autoscaler on a queue signal still needs time to notice (scrape + evaluate).
detect_s = 15
backlog_real = (peak - cap) * (detect_s + load_s)
assert backlog_real == 42000
# 3. Drain after new capacity arrives depends on how many pods you ask for.
def drain(new_cap, backlog=backlog_real):
    return backlog / (new_cap - peak)
need_pods = math.ceil(peak * 1.3 / per_pod)       # 30% headroom
assert need_pods == 10
print('drain with 8 pods (1000/s):', round(drain(8 * per_pod)), 's')
print('drain with 10 pods (1250/s):', round(drain(10 * per_pod)), 's')
assert round(drain(1000)) == 420 and round(drain(1250)) == 120
# 4. Bounded queue: a 2 s client timeout means a queue deeper than cap*2 only holds dead requests.
timeout_s = 2
qmax = cap * timeout_s
assert qmax == 1000
q = shed = served = 0
for t in range(load_s):               # per-second simulation, jump at t=0
    arrive = peak
    take = min(cap, arrive + q)        # serve up to capacity
    served += take
    q = q + arrive - take
    if q > qmax:
        shed += q - qmax; q = qmax
assert served == 45000
arrivals = peak * load_s
assert arrivals == 81000 and shed + q + served == arrivals
print('served', served, 'queued', q, 'shed', shed, 'shed share', round(shed / arrivals, 3))
assert shed == 35000 and round(shed / arrivals, 3) == 0.432
# 5. Warm headroom: pods needed to absorb the jump with zero scaling vs the cost of holding them.
hold_pods = math.ceil(peak / per_pod)
extra = hold_pods - cap // per_pod
assert hold_pods == 8 and extra == 4
pod_hour = 10                          # illustrative cost units per pod-hour
standby_day = extra * pod_hour * 24
loss_per_spike = shed * 0.05           # 0.05 units of value per failed request (illustrative)
print('standby cost/day', standby_day, 'loss per spike', loss_per_spike, 'break-even spikes/day', round(standby_day / loss_per_spike, 2))
assert standby_day == 960 and loss_per_spike == 1750.0
# 6. Escalation rules written down (illustrative thresholds)
rules = {'shed_if_queue_wait_s_over': 2, 'manual_scale_if_no_new_pod_after_s': 120, 'page_human_if_quota_blocked': True}
assert rules['manual_scale_if_no_new_pod_after_s'] > detect_s
```

**Output (my run):**
```text
drain with 8 pods (1000/s): 420 s
drain with 10 pods (1250/s): 120 s
served 45000 queued 1000 shed 35000 shed share 0.432
standby cost/day 960 loss per spike 1750.0 break-even spikes/day 0.55
```

**Follow-ups:**
- Why not just scale to zero in quiet hours? Cold start is 90 seconds, so keep a floor of at least the baseline plus a share of the expected jump.
- Why does drain time matter if capacity is higher than arrivals? Because the surplus is small; at 1,000 against 900 arrivals the surplus is 100 per second, not 500.
- Why shed instead of queueing everything? A request that waits 72 seconds is already dead for the user, and it still consumes GPU time.

**Common mistakes:** Using capacity (500) as the drain rate instead of the surplus. Forgetting detection lag. Scaling on CPU for a GPU-bound job. Unbounded queues. Retries without jitter. Blaming a person in the postmortem.

### Q29 ⭐⭐ 🟡 A ranking model with a 150 ms timeout falls back to a popularity list on 4% of 1,000,000 hourly requests, which is 40,000 requests. Conversion is 5% on the model and 3.5% on the fallback, so the fallback is 30% lower relative to 5%. Estimate the conversions lost per hour due to fallbacks (and say how reliable that estimate is), and decide whether to raise the timeout, add capacity or improve the fallback.
**Asked at:** LLM-serving resilience pages (getmaxim, TrueFoundry, tianpan and Statsig pages on retries, 429 handling, fallbacks, circuit breakers and cost during failover; one snippet notes that silent quality degradation is invisible to HTTP success rates); practitioner material, no confirmed interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** The naive loss is 40,000 x (5.0% - 3.5%) = 600 conversions an hour (1.2% of the 50,000 an all-model hour would give); I would first split why requests time out, then fix the biggest cause, usually capacity, before touching the timeout or the fallback list.

**Clarifying questions:**
- Why do the 40,000 requests time out: queue wait, feature fetch, model compute or a slow tail? The right fix depends on the split.
- Is the 4% steady or bursty by hour? A fallback share that spikes at peak points to capacity.
- Are fallback requests a random sample of traffic? If they are heavy users or big candidate sets, the 5% comparison is biased.
- What is the latency budget of the page, and does conversion fall with latency? Raising the timeout is not free.
- What is the value of one conversion and the cost of a pod hour? Without them there is no decision, only arithmetic.

**Approach:**
1. First 15 minutes (if the fallback rate just jumped): check the fallback-rate alert, find the timeout cause from traces (queue wait versus model time), check for a recent deploy or a dependency slowdown. If it began at a deploy, roll back that deploy.
2. The arithmetic. 4% of 1,000,000 is 40,000. (5.0 - 3.5) / 5.0 = 30% relative, 1.5 points absolute. Lost conversions = 40,000 x 0.015 = 600 per hour. Value at 40 units each (illustrative) is 24,000 per hour, 17.28 million over 30 days.
3. Be honest about what 600 is. It is a projection from two measured rates. The 3.5% has a 95% interval of about 3.32% to 3.68% on 40,000 requests, so noise moves the loss only between roughly 528 and 672. The bigger issue is bias: requests that time out are not a random sample. If 60% of them are heavy users who would have converted at 4% (the rest at 6%), the counterfactual is 4.8% and the real loss is 520, not 600. To measure it properly, serve the fallback to a random 0.5% for a day and compare.
4. Choose the fix by what the timeout log says (all splits illustrative):
   - Capacity: if 70% of timeouts are queueing, removing them recovers about 420 conversions per hour. Three extra pods at 10 units each cost 30 per hour against 16,800 of value.
   - Raise the timeout to 200 ms: only recovers the requests that finish between 150 and 200 ms (225 per hour if 37.5% of fallbacks do), and it slows every user in the tail. Only with a p99 guardrail.
   - Improve the fallback: from 3.5% to 4.2% is 280 per hour, steady and low risk, and it also helps during the next outage.
5. First day: do capacity first if queueing dominates, make the fallback better in parallel, and move the timeout only after the first two. Add a fallback-rate alert at 2x its normal level.
6. Next quarter: set an error budget for fallback share (for example 1% of requests), load-test the tail, and report fallback share next to the conversion dashboard.
7. Blameless postmortem: the fallback worked as designed, it was just never tuned or watched. The action items are an alert, a cause breakdown on the dashboard, and a named owner.

**Rollback and escalation criteria (illustrative, set before the change):**
- Roll back a timeout increase if p99 latency goes over 400 ms, or total conversion falls by more than 0.1 point, for 15 minutes.
- Escalate to the platform team if more than half of the timeouts are queue wait and the autoscaler cannot add capacity.
- Roll back a new fallback list if its conversion is below 3.5% in a 1% test for a day.

**Metrics:**
- Fallback rate = fallback responses / all requests in the hour (4%). Guardrail: alert above 2x normal.
- Conversion by path = conversions / sessions served by that path (5.0% model, 3.5% fallback). State that both are measured samples.
- Lost conversions = fallback requests x (model rate - fallback rate), reported as a range, labelled a projection.
- Timeout cause share = timeouts by cause / all timeouts.
- Guardrails: p99 latency, total conversion rate per hour, cost per hour.

**Risks:**
- Treating the comparison as causal (selection bias).
- A longer timeout turns fallbacks into slow pages, which can lose more than it wins.
- More capacity hides a slow model; cost climbs.
- A better fallback that is expensive to compute stops being a fallback.

**What the interviewer scores:**
- Strong: 600 per hour, with the relative versus absolute point made clearly. Weak: says "30% of 40,000" and gets 12,000.
- Strong: says the number is a projection with a range and a bias caveat. Weak: quotes 600 as a fact.
- Strong: diagnoses the timeout cause before choosing. Weak: picks one fix by gut.
- Strong: order of action, rollback criteria and cost versus gain. Weak: no thresholds.
- Strong: a blameless close with an alert and an owner. Weak: "the model team should be faster".

**Example:** Illustrative numbers. Weak: "Conversion drops 30%, so we lose 30% of 40,000 requests, 12,000 conversions an hour; raise the timeout." Strong: "30% is relative. In absolute terms it is 1.5 points on 40,000 requests, so 600 conversions an hour, and that is an upper-end estimate because slow requests are not typical requests. I would look at why they time out first. If it is queueing, three more pods cost 30 units an hour and recover about 420 conversions, worth 16,800."

**Code:**
```python
# Illustrative numbers only. Fallback loss, options, and a sampling check for the 3.5% fallback conversion rate.
import math
N, fb_rate = 1_000_000, 0.04
fb = round(N * fb_rate); model_n = N - fb
assert fb == 40000 and model_n == 960000
c_model, c_fb = 0.05, 0.035
rel_drop = (c_model - c_fb) / c_model
assert round(rel_drop, 2) == 0.30                      # 30% lower, relative to 5%
lost = fb * (c_model - c_fb)                            # conversions lost per hour if fallbacks converted like model traffic
assert round(lost) == 600
actual = model_n * c_model + fb * c_fb
ideal = N * c_model
assert round(actual) == 49400 and round(ideal) == 50000
print('lost/hour', round(lost), 'share of ideal', round(lost / ideal, 4))
assert round(lost / ideal, 3) == 0.012                  # 1.2% of conversions
value = 40                                              # illustrative value per conversion
print('lost value/hour', round(lost * value), 'per 30 days', round(lost * value * 24 * 30))
assert round(lost * value) == 24000
# Sampling noise on the 3.5% (measured on 40,000 hourly fallbacks): small, so the real doubt is bias, not noise.
se = math.sqrt(c_fb * (1 - c_fb) / fb)
lo, hi = c_fb - 1.96 * se, c_fb + 1.96 * se
print('95% interval for fallback rate', round(lo, 4), round(hi, 4))
assert 0.0332 <= round(lo, 4) <= 0.0333 and round(hi, 4) == 0.0368
lost_lo, lost_hi = fb * (c_model - hi), fb * (c_model - lo)
print('lost range', round(lost_lo), round(lost_hi))
assert 525 < lost_lo < 535 and 670 < lost_hi < 675
# Options (every share below is an ILLUSTRATIVE assumption to be replaced by a measured timeout-cause split).
queue_share, slow_tail_share = 0.70, 0.30               # 70% of timeouts are queueing, 30% slow requests
caught_by_200ms = 0.375                                 # share of ALL fallbacks that would finish in 150-200 ms
cap_fix = fb * queue_share * (c_model - c_fb)           # more capacity removes queueing timeouts
tmo_fix = fb * caught_by_200ms * (c_model - c_fb)       # timeout 150 -> 200 ms
fb_fix = fb * (0.042 - c_fb)                            # fallback improved from 3.5% to 4.2%
print('capacity', round(cap_fix), 'timeout', round(tmo_fix), 'better fallback', round(fb_fix))
assert (round(cap_fix), round(tmo_fix), round(fb_fix)) == (420, 225, 280)
# Capacity cost against gain: 3 extra pods at 10 units per pod-hour.
pods_cost = 3 * 10
print('capacity gain value', round(cap_fix * value), 'cost', pods_cost)
assert round(cap_fix * value) == 16800 and pods_cost == 30
# Decision rules written before the change (illustrative)
rollback = {'p99_ms_over': 400, 'total_conversion_drop_pts_over': 0.1, 'for_minutes': 15}
assert rollback['p99_ms_over'] > 150
# Why 5% vs 3.5% is not clean: slow requests are different requests. Tiny example with two request types.
heavy_share = 0.6                                       # share of fallbacks that are heavy users
c_heavy_model, c_light_model = 0.04, 0.06               # what the model would have converted
true_cf = heavy_share * c_heavy_model + (1 - heavy_share) * c_light_model
assert abs(true_cf - 0.048) < 1e-12
true_lost = fb * (true_cf - c_fb)
print('counterfactual lost if fallbacks are heavy users', round(true_lost))
assert round(true_lost) == 520 and true_lost < lost
```

**Output (my run):**
```text
lost/hour 600 share of ideal 0.012
lost value/hour 24000 per 30 days 17280000
95% interval for fallback rate 0.0332 0.0368
lost range 528 672
capacity 420 timeout 225 better fallback 280
capacity gain value 16800 cost 30
counterfactual lost if fallbacks are heavy users 520
```

**Follow-ups:**
- How do you measure the true cost of the fallback? A small random holdout served the fallback on purpose, compared with the model on the same hours.
- When is raising the timeout right? When the tail of model latency just misses the cut and p99 headroom exists; confirm with a canary and the rollback rule above.
- Should the fallback ever be the model itself? A smaller, faster model as the fallback often beats a popularity list.

**Common mistakes:** Applying 30% to the request count. Calling a measured rate a certainty. Ignoring selection bias. Raising the timeout without a latency guardrail. Fixing before measuring why requests time out.

### Q30 ⭐⭐ 🟡 A streaming job restarted and replayed the last 20 minutes from its committed offset at 50,000 events per minute, so 1,000,000 events were counted twice in the orders_last_hour feature. The model has been reading inflated counts for two hours, and the feature is a running counter that does not expire old events. How do you repair the feature values, and how do you make replays safe by design?
**Asked at:** Data-pipeline pages (luminousmen on avoidable backfills and non-idempotent jobs, DZone on silent upstream schema change, HackerNoon and Seattle Data Guy on silent pipeline failures, DataExpert on schema drift and idempotent replays, DataVidhya on measuring detection latency in postmortems); practitioner blogs rather than an interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** 20 minutes at 50,000 a minute is 1,000,000 duplicates, up to +33% on a 3,000,000-event hourly total; I stop the damage first, rebuild the feature from the raw log with a dedupe on event ID, and make the job safe by design so a replay changes nothing.

**Clarifying questions:**
- Is the running counter keyed per customer, and what resets it? It decides the repair scope (a true 60-minute event-time window would have healed itself within an hour, but a counter that never expires old events keeps the duplicates until it is rebuilt).
- Does every event have a stable unique ID? It decides whether dedupe is possible at all.
- Is the raw log (immutable, replayable) still retained for the affected range? It is the source of truth for the repair.
- Does the offline training table read the same stream? If yes, training data is poisoned too.
- How sensitive is the model to this feature, and what decisions were taken on it? It sets whether we turn the feature off, re-score or just fix forward.

**Approach:**
1. First 15 minutes: confirm the diagnosis (stream total versus batch total, 4,000,000 versus 3,000,000). Decide the stop-gap: if the feature carries large weight, serve a last-good snapshot or a default for that one feature rather than inflated values; if not, leave it and fix forward. Page the pipeline owner and tell the consumers of the model.
2. Scope: replay range from the committed offset and restart time, and the keys and windows that contain a duplicated event. In my 1/100-scale simulation, 259 of 2,000 users crossed a flag threshold of 3 orders only because of the duplicates, and inflation only ever pushes counts up.
3. Repair: recompute the affected windows from the immutable raw log with a dedupe on event ID, starting one full window before the replay (here 80 minutes before the restart) through the time the fix is live. Write the corrected values to the online store as a versioned upsert so a late job cannot overwrite them with old values, and clear any cache in front of the store.
4. Training data: recompute the offline partitions for the same range if they came from the same stream; otherwise confirm they are clean and say so in the postmortem.
5. Decisions already made: if the request log stored the feature values, re-score a sample with corrected values to count how many decisions changed, then decide with the business owner whether any need a correction. If feature values were not logged, say that is a gap.
6. First day: add the dedupe and a reconciliation check (see below), and write the replay test.
7. Next quarter: make replay drills routine in staging, with a "replay 20 minutes and compare" check in CI.
8. Blameless postmortem: restarts replay by design; the system should have been safe against it. Timeline, why 2 hours passed unnoticed, what check would have caught it at minute 10, and action items with owners.

**Make replays safe by design:**
- Idempotent aggregation: dedupe on a stable event ID with state retained for at least the longest possible replay (checkpoint interval plus margin).
- Idempotent sink: upsert by key, window and version, not "add 1".
- Recompute windowed features from state, not from a running counter that never forgets.
- Transactional or exactly-once offset and sink handling where the framework offers it (framework behaviour is editor knowledge, not tested here).
- A hard reconciliation: stream total versus batch total every 10 minutes; alert if the gap is above 5%. The 33% gap here would have fired on the first check.

**Rollback and escalation criteria (illustrative):**
- Turn the feature to its default if reconciliation gap exceeds 5% for two checks in a row and the repair is more than 30 minutes away.
- Escalate to the model owner if more than 1% of decisions in the window changed on re-scoring.
- Declare the repair finished only when the online store equals the batch recompute on a sampled set of keys.

**Metrics:**
- Duplicate rate = events whose ID was already seen / all events in the window. Target 0 after the fix; alert on any burst.
- Reconciliation gap = (stream total - batch total) / batch total, 33.3% in the incident.
- Detection delay = time from the restart to the first alert (120 minutes actual versus 10 target).
- Decisions changed = decisions whose outcome flips with corrected feature values / all decisions in the window.
- Guardrails: feature freshness (the repair must not make values stale), store write errors.

**Risks:**
- Repairing the online store while the stream is still writing: a race that overwrites good values. Use versions.
- Dedupe state that expires before the next replay.
- Fixing only the online side; the next retrain learns from duplicates.
- Re-scoring changes decisions people already acted on; the owner decides.

**What the interviewer scores:**
- Strong: gets 1,000,000 and the 33% bound, and sees that a non-expiring counter will not self-heal. Weak: restarts the job and hopes.
- Strong: repair from the raw log with dedupe, versioned write, cache clear. Weak: subtracts a constant from the store.
- Strong: design fix (idempotency, dedupe state, reconciliation). Weak: "do not restart the job".
- Strong: ordered actions with stop-gap criteria. Weak: a flat list.
- Strong: blameless focus on detection delay. Weak: blames the engineer who restarted it.

**Example:** Illustrative numbers. Weak: "I will restart the job from the right offset and the numbers will fix themselves." Strong: "The restart replayed 20 minutes at 50,000 a minute, so 1,000,000 duplicates, up to 33% inflation on a 3,000,000 hour. I recompute the window from the raw log, deduping on event ID, write it back with a version, and check the offline table too. For the future, aggregation dedupes on event ID and a 10-minute reconciliation would have paged us at minute 10, not hour 2."

**Code:**
```python
# Illustrative numbers only. Replay duplicates, window self-healing, flips across a threshold, and a dedupe fix.
import random, collections
rate, replay_min, window_min = 50_000, 20, 60
dupes = rate * replay_min
normal_window = rate * window_min
assert dupes == 1_000_000 and normal_window == 3_000_000
print('peak inflation of the hourly total', round(dupes / normal_window, 4))
assert round(dupes / normal_window, 4) == 0.3333

# 1. Event-time sliding window: when do the duplicates age out? Minute-level sketch at full scale.
# Duplicates carry event times in [T0-20, T0). The window at time t holds event times in (t-60, t].
T0 = 0
def dup_in_window(t):
    lo, hi = max(t - window_min, T0 - replay_min), min(t, T0)
    return max(0, hi - lo) * rate
last_bad = max(t for t in range(0, 200) if dup_in_window(t) > 0)
print('last minute after restart with inflated total:', last_bad)
assert last_bad == 59 and dup_in_window(60) == 0
# So a true 60-minute event-time window heals within an hour of the restart.
# Reading inflated counts 2 hours later means the duplicates sit in a non-expiring state (running counter, or TTL on processing time).

# 2. Mini simulation at 1/100 scale: counter without dedupe versus dedupe by event_id.
rnd = random.Random(7)
users = 2000
events = [(i, rnd.randrange(users)) for i in range(3000)]        # 60 minutes of normal events at 50/min
replayed = events[-1000:]                                        # last 20 minutes replayed (1/100 of 1M)
assert len(replayed) == dupes // 1000
naive = collections.Counter(u for _, u in events + replayed)
seen, dedup = set(), collections.Counter()
for eid, u in events + replayed:
    if eid in seen: continue
    seen.add(eid); dedup[u] += 1
truth = collections.Counter(u for _, u in events)
assert dedup == truth
extra = sum(naive.values()) - sum(truth.values())
assert extra == 1000 and round(extra / sum(truth.values()), 4) == 0.3333
# 3. How many scores flipped? Rule: risk flag if orders_last_hour >= 3 (illustrative threshold).
thr = 3
flips = sum(1 for u in range(users) if (naive[u] >= thr) != (truth[u] >= thr))
print('users flagged correctly', sum(truth[u] >= thr for u in range(users)), 'flagged with inflated counts', sum(naive[u] >= thr for u in range(users)), 'flips', flips)
assert flips > 0 and all(naive[u] >= truth[u] for u in range(users))   # inflation only pushes counts up
# 4. Reconciliation check that would have caught it at the first run.
stream_total, batch_total = 4_000_000, 3_000_000
gap = (stream_total - batch_total) / batch_total
alert_if = 0.05
assert gap > alert_if and round(gap, 4) == 0.3333
check_every_min = 10
print('worst-case detection delay with a', check_every_min, 'minute reconciliation:', check_every_min, 'min vs 120 min actual')
assert check_every_min < 120
# 5. Repair scope: re-aggregate from the raw log for the window that touched duplicates.
repair_from_min = -replay_min - window_min       # first window that could contain any duplicate
repair_to_min = 120                              # until the fix is live (illustrative)
print('recompute event-time range (minutes relative to restart):', repair_from_min, 'to', repair_to_min)
assert repair_to_min - repair_from_min == 200
```

**Output (my run):**
```text
peak inflation of the hourly total 0.3333
last minute after restart with inflated total: 59
users flagged correctly 386 flagged with inflated counts 645 flips 259
worst-case detection delay with a 10 minute reconciliation: 10 min vs 120 min actual
recompute event-time range (minutes relative to restart): -80 to 120
```

**Follow-ups:**
- Why not just subtract 1,000,000? Duplicates are not spread evenly across keys, so a global subtraction corrupts every individual value.
- What if there is no event ID? Build a deterministic one from source, partition, offset (stable across replays), or dedupe on a content key plus time.
- Does this relate to batch reruns? Yes, same principle; see Book 4 Part 5, Q3 "Idempotency in pipeline tasks" and Q6 "Backfills and catchup".

**Common mistakes:** Assuming a restart is harmless. Subtracting a global constant. Repairing the online store but not training data. Writing "increment by 1" sinks. No reconciliation check. Blaming whoever restarted the job.

### Q31 ⭐⭐ 🟡 A prompt edit shipped on Tuesday, and HTTP success stayed at 99.9%, but the thumbs-down share of rated answers rose from 3.1% of 8,000 rated answers the week before (248 answers) to 5.0% of 7,500 rated answers after (375), a 1.9 point absolute rise on a measured sample. Only a small share of traffic gets rated. Do you roll back, and how do you detect a prompt regression sooner next time?
**Asked at:** LLM-serving resilience pages (getmaxim, TrueFoundry, tianpan and Statsig pages on retries, 429 handling, fallbacks, circuit breakers and cost during failover; one snippet notes that silent quality degradation is invisible to HTTP success rates); practitioner material, no confirmed interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** Yes, roll back now: the rise from 3.1% to 5.0% (1.9 points absolute, 61% relative) has z of about 6 and a 95% interval of 1.3 to 2.5 points, rollback of a prompt is cheap and reversible, and then I find out why with a proper split.

**Clarifying questions:**
- Is the prompt behind a flag with a version stamped on every answer log? Without it I cannot separate prompt effects from everything else that changed Tuesday.
- What share of answers is rated and who rates? Raters self-select; the rise may not describe the 96% who did not rate (illustrative: 4% rated).
- Did traffic mix, model version or a UI change land the same day? Before and after is not an experiment.
- What does a thumbs-down cost us (support tickets, churn, regulated content)? It sets the rollback bar.
- Is there a fixed evaluation set for this prompt? It gives a fast signal before rating data exists.

**Approach:**
1. First 15 minutes: flip the prompt flag back to the previous version (a config change, no deploy). Confirm that the thumbs-down share returns toward 3.1% over the next hours, and keep the bad prompt version available for debugging. Tell the product owner in one line.
2. Check the claim before acting on it, in minutes: 248 / 8,000 = 3.1% and 375 / 7,500 = 5.0%. Pooled z is about 6.0, two-sided p is about 2e-9. So it is not sampling noise. The doubts are bias and confounding, not noise.
3. Decide with a pre-agreed rule (illustrative): roll back if the thumbs-down rate is up at least 1.0 point absolute, the lower end of the 95% interval is above zero, and there are at least 1,000 ratings in each period. This case passes with lower bound 1.28 points.
4. First day: run the new prompt against the old on a 50/50 split to find what hurt (tone, refusals, length, a dropped instruction). Read 50 thumbs-down answers by hand, split by prompt version.
5. Detect sooner next time:
   - Stamp prompt version on every answer, ratings included.
   - Run a fixed golden set (for example 300 prompts) before release. A drop from 90% to 84% pass is 6 points, just beyond the noise of about 5.4 on 300 prompts, so use more prompts for a sharper gate.
   - Canary the prompt at 10% to 50%. Thumbs-down alone is slow: about 1,686 ratings per arm are needed for 80% power at this effect size. At 4% rated, a 10% canary gets 114 ratings a day (about 15 days) while 50% takes about 3 days.
   - Add signals that do not need ratings: regenerate rate, abandonment, answer length, refusal rate, format-failure rate, and a sampled model-judge with human spot checks.
   - Alert daily on the same-day comparison against baseline: one day of ratings would already have crossed z of 2.58 here.
6. Next quarter: treat prompts like code (review, version, golden-set CI, staged rollout, rollback drill).
7. Blameless postmortem: HTTP 99.9% only proves the service answered. Timeline, why quality had no monitor, and action items (flag plus version stamp, golden set gate, quality canary, owner).

**Rollback and escalation criteria (illustrative):**
- Roll back: the rule above, or golden-set pass rate down at least 5 points.
- Escalate to the product owner and a human reviewer if answers in a sensitive category (health, money, legal) show any rise.
- Re-ship only after the golden set matches the old prompt and a 50% canary holds for 3 days.

**Metrics:**
- Thumbs-down share = thumbs-down / rated answers in the period, with the denominator shown (8,000 and 7,500). Measured sample, not the whole population.
- Rated share = rated answers / all answers. A change in this share is itself a warning.
- Golden-set pass rate = prompts passing / golden prompts.
- Guardrails: HTTP success, latency, tokens per answer (cost), refusal rate.

**Risks:**
- Confounding: another change on Tuesday (model, UI, traffic mix).
- Selection: unhappy users rate more; the rise may overstate or understate the whole population.
- Reverting to an old prompt that is stale for new policy.
- Alert fatigue if the quality alert is too sensitive.

**What the interviewer scores:**
- Strong: recomputes the numbers, says noise is ruled out and names the bias instead. Weak: "it is significant, done" or "it is only a sample, ignore it".
- Strong: rolls back first because it is cheap, then investigates. Weak: debates for a day.
- Strong: detection design with version stamps, golden set and a canary sized by arithmetic. Weak: "monitor more".
- Strong: ordered actions and a rule written in advance. Weak: no threshold.
- Strong: blameless framing around missing quality monitoring. Weak: blames the prompt author.

**Example:** Illustrative numbers. Weak: "HTTP success is 99.9%, so the service is healthy; I would wait another week of ratings." Strong: "Thumbs-down went from 3.1% to 5.0% of rated answers, 61% relative, z of about 6. The prompt is a flag, so I roll back now and compare versions on a 50/50 split tomorrow. Next time a golden set blocks the release and a 50% canary needs three days of ratings, not fifteen."

**Code:**
```python
# Illustrative numbers only. Is the thumbs-down rise noise, what to do, and how fast could we have seen it.
import math
from statistics import NormalDist
Z = NormalDist()
x1, n1, x2, n2 = 248, 8000, 375, 7500
p1, p2 = x1 / n1, x2 / n2
assert round(p1, 3) == 0.031 and round(p2, 3) == 0.05 and round((p2 - p1) * 100, 1) == 1.9
rel = p2 / p1 - 1
print('relative rise', round(rel, 3))
assert round(rel, 2) == 0.61
pool = (x1 + x2) / (n1 + n2)
se0 = math.sqrt(pool * (1 - pool) * (1 / n1 + 1 / n2))
z = (p2 - p1) / se0
pval = 2 * (1 - Z.cdf(abs(z)))
print('z', round(z, 2), 'two-sided p', f'{pval:.1e}')
assert 5.5 < z < 6.5 and pval < 1e-8
se1 = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
lo, hi = (p2 - p1) - 1.96 * se1, (p2 - p1) + 1.96 * se1
print('95% CI for the rise (points)', round(lo * 100, 2), round(hi * 100, 2))
assert 1.2 < lo * 100 < 1.3 and 2.4 < hi * 100 < 2.6
# Sampling noise is not the issue. Bias is: only a small share is rated, and raters choose to rate.
# Pre-agreed rollback rule (illustrative): rise >= 1.0 pt absolute AND lower CI bound > 0 with >= 1,000 ratings in each period.
rule = (p2 - p1) >= 0.010 and lo > 0 and min(n1, n2) >= 1000
assert rule
# Speed: how many rated answers per arm to see 3.1% -> 5.0% at 80% power, 5% two-sided?
za, zb = Z.inv_cdf(0.975), Z.inv_cdf(0.80)
n_arm = math.ceil((za + zb) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p2 - p1) ** 2)
print('rated answers needed per arm', n_arm)
assert 1600 < n_arm < 1800
# Invented volume: 200,000 answers a week, 4% rated -> 8,000 rated a week (matches the prompt), 1,143 a day.
weekly_answers, rate_share = 200_000, 0.04
rated_week = weekly_answers * rate_share
assert rated_week == 8000
rated_day = rated_week / 7
for split in (0.10, 0.50):
    per_day_arm = rated_day * split
    print(f'canary {int(split*100)}%: rated/day in canary {per_day_arm:.0f}, days to {n_arm} ratings {n_arm/per_day_arm:.1f}')
assert round(1700 / (rated_day * 0.10)) > 10 and round(n_arm / (rated_day * 0.5)) <= 3
# Days of post-ship data against the prior week baseline before |z| > 2.58 (expected values, not a simulation).
def days_to_z(target):
    for d in range(1, 15):
        n = rated_day * d
        pl = (p1 * n1 + p2 * n) / (n1 + n)
        s = math.sqrt(pl * (1 - pl) * (1 / n1 + 1 / n))
        if (p2 - p1) / s > target: return d
d99 = days_to_z(2.58)
print('days of post-ship ratings before z>2.58 against last week:', d99)
assert d99 == 1
# Faster signals that do not need ratings: a 300-prompt golden set run BEFORE the release.
golden_n, old_pass, new_pass = 300, 0.90, 0.84
se_g = math.sqrt(old_pass * (1 - old_pass) / golden_n + new_pass * (1 - new_pass) / golden_n)
drop_pts = (old_pass - new_pass) * 100
print('golden-set drop', round(drop_pts, 1), 'pts, 1.96 se =', round(1.96 * se_g * 100, 1), 'pts')
assert round(drop_pts) == 6 and 1.96 * se_g * 100 < 6
```

**Output (my run):**
```text
relative rise 0.613
z 6.02 two-sided p 1.8e-09
95% CI for the rise (points) 1.28 2.52
rated answers needed per arm 1686
canary 10%: rated/day in canary 114, days to 1686 ratings 14.8
canary 50%: rated/day in canary 571, days to 1686 ratings 3.0
days of post-ship ratings before z>2.58 against last week: 1
golden-set drop 6.0 pts, 1.96 se = 5.4 pts
```

**Follow-ups:**
- What if the rollback does not bring thumbs-down back? Then Tuesday had another cause; look at the other changes and the traffic mix.
- Can an LLM judge replace ratings? It is a useful extra signal, but validate it against human labels before trusting it (see Book 6 Part 2, Q45, the LLM-as-judge versus human spot-check question).
- Why report relative and absolute? 61% relative sounds huge and 1.9 points sounds small; the business cost depends on the base.

**Common mistakes:** Treating HTTP success as quality. Treating a measured rating sample as the full population. Comparing weeks without checking mix. Shipping prompts without a version stamp or a rollback flag. Alerting on thumbs-down alone with a 10% canary.

### Q32 ⭐⭐ 🟡 A new pricing-model threshold is about to roll out to 6 regions whose traffic shares are 40%, 25%, 15%, 10%, 6% and 4% of all requests. Order and size the rollout waves, say what you watch at each wave, and explain how you limit the blast radius if the threshold has a bug that only shows at a particular hour or customer type.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to blast radius and progressive delivery in release engineering; related topics appear in public MLOps guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Go smallest region first, 4%, then cumulative 10%, 20%, 35%, 60%, 80%, 100% (splitting the 40% region), advance only after a full 24-hour cycle and enough requests in each watched segment, and watch segments by hour and customer type, because a bug like that is invisible in global numbers.

**Clarifying questions:**
- Is the threshold changeable by a flag per region, with the old value kept? Without a per-region kill switch there is no staged rollout.
- What does the threshold decide (price shown, offer, block)? It sets how harsh a bad decision is and what we halt on.
- Are the six regions in different time zones with different customer mixes? That tells me whether the early waves can see an hour-specific or customer-specific bug at all.
- Can I shadow the new threshold first (compute, do not apply)? It finds many bugs with zero customer impact.
- What is the cost of one bad decision? It turns blast radius into a number.

**Approach:**
1. Wave 0: shadow in all regions, log what the new threshold would have decided, and compare against the old one by hour and customer type. Nothing is applied.
2. Order and size (shares sum to 100%): W1 smallest region R6 (4%), W2 add R5 (cumulative 10%), W3 add R4 (20%), W4 add R3 (35%), W5 add R2 (60%), W6 half of R1 (80%), W7 the rest (100%). The largest growth factor is 2.5x and the last two steps are 1.33x and 1.25x. A 24-hour dwell per wave makes it 7 days.
3. Smallest first limits exposure, but a small region may not contain the risky segment. Pick the first region for representativeness as well as size, and check coverage before trusting a quiet wave.
4. What I watch at each wave:
   - Global: error rate, decision rate (share approved or priced differently), latency.
   - Segments: decision-changed-versus-old-threshold rate by hour of day and by customer type, judged only with at least 200 requests per segment.
   - Business: revenue per request and complaint volume, against a holdout region.
5. Gate to advance: one full 24-hour cycle (so every hour of the day has occurred once) and every watched segment above the minimum count.
6. First 15 minutes after an alert: halt the ramp (no new regions), flip the flag back for the affected region, keep logs. Do not wait for a root cause.
7. First day: root-cause with the logged shadow data; fix; restart at wave 1.
8. Next quarter: add automated segment slicing to every threshold rollout, and keep a standing holdout region.
9. Blameless postmortem: the bug was in a corner nobody tested; the question is why the process could not see the corner. Action items: segment gates, shadow comparison, coverage check for the first region.

**Why global metrics miss the bug (numbers in the code):** Illustrative: 10,000,000 requests a day. A bug that affects customer type X only during one hour a day hits about 12,800 requests at full rollout and 83 in wave 1. That is 0.128% of all requests, under a 0.5% global alert, so the global monitor never fires. Inside that hour and segment every decision is wrong, so a segment monitor sees 100% bad, but only with enough requests: wave 1 gives 83 per day, so it takes 2.4 days to reach 200; wave 2 gives 333 per day. So the dwell rule must scale with segment sample size, not just the clock.

**Rollback and escalation criteria (illustrative):**
- Halt and roll back a region if any segment with at least 200 requests has a decision-changed rate above 5%, or the global error rate is up 0.2 point for 15 minutes.
- Do not advance if any watched segment is below 200 requests; extend the dwell instead.
- Escalate to the business owner if any wave shows revenue per request down more than 1% against the holdout.
- Blast radius = traffic share x hours to detect x harm per request. Detecting at wave 1 over 72 hours exposes about 250 bad requests; detecting after full rollout over the same time exposes about 38,500.

**Metrics:**
- Cumulative exposure = share of all requests on the new threshold (4, 10, 20, 35, 60, 80, 100).
- Decision-changed rate = requests whose decision differs from the old threshold / requests in that segment.
- Segment coverage = requests in the segment during the wave / minimum count (200).
- Guardrails: global error rate, latency, revenue per request versus holdout, complaints.

**Risks:**
- Region mix: the first region may lack the customer type that triggers the bug.
- Time zones: a daily-hour bug only appears when local time reaches that hour; a 6-hour dwell would miss it.
- Interaction between regions that share a cache or model.
- Pressure to compress waves once early ones look quiet. Quiet with too few requests is not safe.

**What the interviewer scores:**
- Strong: smallest-first with representativeness check, splitting the 40% step. Weak: "10% of everyone, then 100%".
- Strong: 24-hour cycle plus minimum segment counts as the gate. Weak: a timer only.
- Strong: segments by hour and customer type, and a shadow wave first. Weak: global metrics only.
- Strong: halt rules, kill switch and a blast-radius number. Weak: "monitor closely".
- Strong: blameless focus on why the process missed the corner. Weak: blames whoever set the threshold.

**Example:** Illustrative numbers. Weak: "Roll out to the small regions first and watch the dashboard; if it looks fine go to the big ones." Strong: "R6 first, 4% of traffic, shadow before that. I advance after a full 24-hour cycle and only when every watched segment has at least 200 requests. A one-hour, one-customer-type bug is 0.13% of traffic globally, so the global alert never fires, but the segment rate is 100% and the wave-1 sample reaches 200 in about 2.4 days."

**Code:**
```python
# Illustrative numbers only. Wave sizes, exposure, and a hidden hour/segment bug that global metrics cannot see.
shares = {'R1': 40, 'R2': 25, 'R3': 15, 'R4': 10, 'R5': 6, 'R6': 4}   # percent of all requests
assert sum(shares.values()) == 100
# Smallest region first; the 40% region is split so the last step is never a 40% jump.
waves = [('W1 R6', 4), ('W2 +R5', 6), ('W3 +R4', 10), ('W4 +R3', 15), ('W5 +R2', 25), ('W6 +half R1', 20), ('W7 rest of R1', 20)]
cum, tot = [], 0
for name, s in waves:
    tot += s; cum.append(tot)
print('cumulative exposure %:', cum)
assert cum == [4, 10, 20, 35, 60, 80, 100]
steps = [b / a for a, b in zip(cum, cum[1:])]
print('growth factor per wave:', [round(x, 2) for x in steps])
assert max(steps) == 2.5 and cum[0] == shares['R6']
dwell_h = 24
print('days to complete with a 24 h dwell per wave:', len(waves) * dwell_h / 24)
assert len(waves) * dwell_h / 24 == 7
# Hidden bug: only customer type X, only in one hour of the day (e.g. 18:00 local).
daily = 10_000_000                                  # requests per day (illustrative)
x_share = {'R1': 0.04, 'R2': 0.03, 'R3': 0.03, 'R4': 0.02, 'R5': 0.01, 'R6': 0.005}   # share of X inside each region
def affected(regions):                               # requests per day hit by the bug if those regions are live
    return sum(daily * shares[r] / 100 * x_share[r] / 24 for r in regions)
full = affected(shares)
w1 = affected(['R6'])
print('bad requests per day, full rollout:', round(full), 'in wave 1:', round(w1))
assert round(w1) == 83 and 11_000 < full < 14_000
# Global view: bad rate is tiny and cannot be seen against noise.
bad_rate_global = full / daily
print('global bad-request rate at full rollout', round(bad_rate_global * 100, 3), '%')
assert bad_rate_global < 0.0015
alert_global = 0.005                                # 0.5% global error alert (illustrative)
assert bad_rate_global < alert_global               # never fires
# Segment view: inside (type X, hour 18) every request is bad, so the segment rate is 100%.
seg_n_day_w1 = daily * 0.04 * 0.005 / 24            # requests per day in the segment during wave 1
min_n = 200                                         # minimum requests before a segment is judged
days_needed = min_n / seg_n_day_w1
print('segment requests per day in wave 1', round(seg_n_day_w1), 'days to reach', min_n, ':', round(days_needed, 1))
assert round(seg_n_day_w1) == 83 and 2.3 < days_needed < 2.5
# Wave 2 adds R5 and the sample grows.
seg_w2 = seg_n_day_w1 + daily * 0.06 * 0.01 / 24
print('wave 2 segment requests per day', round(seg_w2), 'days to reach', min_n, ':', round(min_n / seg_w2, 2))
assert min_n / seg_w2 < 1
# Rule: advance only when (a) one full 24 h cycle has passed and (b) every watched segment has >= min_n requests.
def can_advance(hours, seg_counts):
    return hours >= 24 and all(c >= min_n for c in seg_counts.values())
assert not can_advance(24, {'X@18': 83}) and can_advance(72, {'X@18': 250}) and not can_advance(10, {'X@18': 900})
# Halt rules (illustrative): per segment, decision changed vs the old threshold above 5% with n >= 200, or global error +0.2 pt.
halt = lambda seg_rate, n: n >= min_n and seg_rate > 0.05
assert halt(1.0, 250) and not halt(1.0, 83)
# Blast radius = exposure share x hours to detect x severity. Compare detecting at wave 1 versus after full rollout.
hours_to_detect = 72
print('requests exposed at wave 1 over 72 h:', round(w1 * hours_to_detect / 24), 'vs full rollout:', round(full * hours_to_detect / 24))
assert round(w1 * 3) == 250 and round(full * 3) > 30_000
```

**Output (my run):**
```text
cumulative exposure %: [4, 10, 20, 35, 60, 80, 100]
growth factor per wave: [2.5, 2.0, 1.75, 1.71, 1.33, 1.25]
days to complete with a 24 h dwell per wave: 7.0
bad requests per day, full rollout: 12833 in wave 1: 83
global bad-request rate at full rollout 0.128 %
segment requests per day in wave 1 83 days to reach 200 : 2.4
wave 2 segment requests per day 333 days to reach 200 : 0.6
requests exposed at wave 1 over 72 h: 250 vs full rollout: 38500
```

**Follow-ups:**
- Why not start with the largest region for the best data? Because the blast radius is highest exactly where you learn most; use shadow for the data and the small region for the live check.
- How do you size a holdout? Keep one region (or 1-5% of traffic) on the old threshold for the whole rollout; its size follows the sample-size arithmetic for the metric you judge.
- Does a per-region flag need a deploy? It should not; a flag flip is the rollback. Related release mechanics are in Book 4 Part 3, Q10 "Rolling updates, rollbacks and canary releases for a new model version on Kubernetes".

**Common mistakes:** Judging a quiet wave with too few requests. A dwell shorter than one daily cycle. Global metrics only. No kill switch or kept old value. Jumping 40% in the last step. Starting in a region that is not representative.

### Q33 ⭐⭐ 🟡 A training job takes 7.5 hours, and after a schedule edit it starts every 6 hours, so the second run starts 1.5 hours before the first finishes. Both write to the same registry name and the same checkpoint folder. How do you find out what has already been overwritten, what can the scheduler do to prevent overlap, and how do you make the training job safe if it does overlap?
**Asked at:** Data-pipeline pages (luminousmen on avoidable backfills and non-idempotent jobs, DZone on silent upstream schema change, HackerNoon and Seattle Data Guy on silent pipeline failures, DataExpert on schema drift and idempotent replays, DataVidhya on measuring detection latency in postmortems); practitioner blogs rather than an interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** The runs overlap for 1.5 hours every 6 hours (25% of the time two jobs are alive), so I first find what was overwritten from versioned storage and run metadata, then stop the overlap with a single-run lease and a sane interval, and make the job write only to its own run folder.

**Clarifying questions:**
- When was the schedule edited, and how many runs have started since? It sets the number of overlap windows to audit (7 windows after 8 starts).
- Is object versioning on for the bucket, and does the registry keep every version? That decides whether overwritten files can be recovered.
- Does the job resume from "latest" at start? If yes, run 2 may have started from run 1's half-trained state.
- Is the registry name an alias that auto-promotes? A bad overlap could have promoted a mixed model.
- What does the scheduler support: max one active run, skip or queue? It sets the prevention.

**Approach:**
1. First 15 minutes: pause the schedule (or set one active run), do not kill running jobs yet (they hold evidence), copy the checkpoint folder listing and the registry history to a safe place.
2. Find what was overwritten:
   - Registry: list versions of that name with creation time, run ID tag and data cutoff. Look for versions created by an overlapped run, and for alias moves.
   - Checkpoint folder: list object versions (if versioning is on) with last-modified times. Any file name written by two run IDs, or any "latest" pointer written in the 6 overlap windows, is suspect. In an overlap, each run writes the shared pointer 3 times (6.5, 7.0, 7.5 hours after the first start), so the pointer interleaves.
   - Logs: for each run, start and end time, resume path, and the checkpoint it loaded. A run that resumed from "latest" at the start of an overlap picked up another run's state, 6 hours into a 7.5-hour job.
   - Decide per version: clean (own folder or no overlap), suspect (overlapped but only wrote its own paths), or corrupt (resumed from another run or shared files). Retrain from a clean commit if the champion is corrupt.
3. Scheduler fixes (editor knowledge about common scheduler options such as one active run, skip-if-running or queue; not tested here):
   - One active run: skipping the overlapped slot moves the effective interval to 12 hours (next free slot on the 6-hour grid). Queueing is worse: the lag grows 1.5 hours per run, 12 hours after 8 runs and 24 after 16.
   - Right-size the interval: at least the duration plus margin (1.2 x 7.5 = 9 hours; use p95 duration in practice), or cut the run time.
   - Alert when a run is still alive when the next one is due.
4. Make the job safe if it overlaps anyway:
   - Run-scoped paths (ckpt/run_id/...), never a shared folder.
   - A lease with a fencing token: only the holder may promote, a stale holder is refused.
   - Registry writes always create a new version tagged with run ID and data cutoff; promotion is a separate gated step that compares against the current champion.
   - Never resume from "latest"; resume by explicit run ID.
5. First day: fix the schedule, add the lease, backfill a clean candidate.
6. Next quarter: add a schedule-lint check in CI (interval versus p95 duration), a "duplicate run" test, and a run-duration dashboard.
7. Blameless postmortem: a one-line schedule edit was allowed to double the job with no check. Timeline, impact on versions, and action items (lint, lease, per-run paths). The editor of the schedule is not the finding.

**Rollback and escalation criteria (illustrative):**
- Roll back the schedule edit immediately (back to the last interval that held).
- If the production champion was registered by an overlapped run, revert the alias to the last version registered with no overlap, and re-validate on the holdout before any new promote.
- Escalate to the model owner if any version served to users is "corrupt" under the audit above.

**Metrics:**
- Overlap share = hours with 2 or more runs alive / total hours (25% steady state here).
- Overlapped runs = runs whose start is before the previous run ended / all runs since the edit.
- Interval headroom = interval / p95 duration (6 / 7.5 = 0.8 here, must be above 1).
- Schedule lag if queued = (duration - interval) x number of runs.
- Guardrails: GPU hours per day, peak concurrent GPUs, registry versions per day.

**Risks:**
- Skipping runs silently makes the model staler (12 hours instead of 6); say so to the business.
- A lease that is never released after a crash blocks all runs; give it a timeout.
- Cleaning up checkpoints too early destroys the evidence.
- A longer-than-average run can finish after its successor, so "latest start" is not "latest finish".

**What the interviewer scores:**
- Strong: states the overlap (1.5 hours, 25%) and the queue-lag trap. Weak: "just delay the schedule".
- Strong: audits with registry history, object versions and run logs and classes each version. Weak: assumes nothing was damaged.
- Strong: lease plus run-scoped paths plus separate promotion. Weak: only a bigger interval.
- Strong: ordered actions and a rollback rule for the champion. Weak: no criteria.
- Strong: blameless framing on missing guardrails. Weak: blames the schedule editor.

**Example:** Illustrative numbers. Weak: "I would check the logs and ask whoever edited the schedule to change it back." Strong: "Eight starts means seven overlap windows, 10.5 hours with two runs alive. I list registry versions and the checkpoint object versions, mark any run that resumed from latest, and revert the alias if the champion came from an overlapped run. Then one active run with a lease, per-run folders, and a lint that fails when interval is under the p95 duration."

**Code:**
```python
# Illustrative numbers only. Overlap timeline, queue lag, skip-if-running cadence, and the shared-latest collision.
import math
dur, every = 7.5, 6.0                                  # hours
overlap = dur - every
assert overlap == 1.5
# 1. Timeline of 8 runs (48 hours of starts), at 1-minute resolution.
starts = [every * k for k in range(8)]
ends = [s + dur for s in starts]
horizon = int(ends[-1] * 60)
conc = [sum(1 for s, e in zip(starts, ends) if s * 60 <= m < e * 60) for m in range(horizon)]
assert max(conc) == 2
two = sum(1 for c in conc if c == 2) / 60
print('hours with 2 runs alive:', two, 'overlap windows:', len(starts) - 1)
assert two == 10.5 == (len(starts) - 1) * overlap
# In steady state the share of time with two runs alive is overlap / every.
assert overlap / every == 0.25
# 2. If the scheduler QUEUES runs one at a time instead, lag grows without bound.
lag = [(dur - every) * n for n in range(1, 17)]
print('queue lag after 8 runs (hours):', lag[7], 'after 16 runs:', lag[15])
assert lag[7] == 12.0 and lag[15] == 24.0
# 3. Skip-if-running keeps no overlap but halves the cadence: next free slot on the 6 h grid.
slot = math.ceil(dur / every) * every
print('effective interval with skip-if-running:', slot, 'h')
assert slot == 12.0
# Better: choose an interval from duration with a margin (here 20% over the 7.5 h average; use p95 in practice).
min_interval = dur * 1.2
assert min_interval == 9.0 and 9.0 > dur
# 4. Shared 'latest' checkpoint pointer: each run writes it every 30 min while alive.
def writes(s, e):
    return [s + 0.5 * i for i in range(1, int((e - s) / 0.5) + 1)]
w0 = [t for t in writes(starts[0], ends[0]) if t > starts[1]]     # run 0 after run 1 started
w1 = [t for t in writes(starts[1], ends[1]) if t <= ends[0]]       # run 1 before run 0 ended
print('latest-pointer writes by run 0 after run 1 started:', w0, 'by run 1 before run 0 ended:', w1)
assert w0 == [6.5, 7.0, 7.5] and w1 == [6.5, 7.0, 7.5]
# A new run that resumes from 'latest' at its start picks up run 0's mid-training state.
resume_state_hours = starts[1] - starts[0]
assert resume_state_hours == 6.0 and resume_state_hours < dur      # run 0 was still only 6 h into a 7.5 h job
# 5. Order of FINISH equals order of START only while durations stay close.
def inverted(d_k, d_next):
    return starts[0] + d_k > starts[1] + d_next
assert not inverted(7.5, 7.5) and inverted(13.0, 6.5)             # a run 6.5 h longer than its successor finishes AFTER it
# 6. Safe design: run-scoped paths + a lease with a fencing token; only the holder may promote.
class Lease:
    def __init__(self): self.token = 0; self.holder = None
    def acquire(self, run):
        if self.holder is None: self.token += 1; self.holder = run; return self.token
        return None
    def release(self, run): self.holder = None
L = Lease()
t0 = L.acquire('run0'); t1 = L.acquire('run1')
assert t0 == 1 and t1 is None                                       # second run refuses to start (or waits) while run0 holds the lease
promote_ok = lambda run, token, current: token == current           # a stale holder cannot promote
assert promote_ok('run0', 1, L.token) and not promote_ok('run0', 1, 2)
paths = [f'ckpt/{r}/step_{i}' for r in ('run0', 'run1') for i in range(3)]
assert len(set(paths)) == 6                                          # no shared file names
print('lease, run-scoped paths and promotion checks passed')
```

**Output (my run):**
```text
hours with 2 runs alive: 10.5 overlap windows: 7
queue lag after 8 runs (hours): 12.0 after 16 runs: 24.0
effective interval with skip-if-running: 12.0 h
latest-pointer writes by run 0 after run 1 started: [6.5, 7.0, 7.5] by run 1 before run 0 ended: [6.5, 7.0, 7.5]
lease, run-scoped paths and promotion checks passed
```

**Follow-ups:**
- Should the interval just be 12 hours? Only if a 12-hour refresh is acceptable; otherwise shorten the job or start the next run from the previous run's end.
- What if overlap is intended (blue and green training)? Then they must write to different paths and promotion picks by validation, not by finish time.
- Related reading: Book 4 Part 5, Q3 "Idempotency in pipeline tasks".

**Common mistakes:** Queueing overlapped runs (lag grows forever). Only fixing the schedule and not the shared paths. Not checking the registry and alias history. Resuming from "latest". Deleting checkpoints before auditing. Blaming the person who edited the schedule.

### Q34 ⭐⭐ 🟡 A two-sample KS test comparing this week's 2,000,000 rows to a reference of 2,000,000 rows flags 38 of 40 features (95% of them) with p-values below 0.001, while the largest KS statistic is only 0.02 and the model's labelled AUC is unchanged. Explain why the monitor fires constantly, and how you would change the test, the effect-size threshold and the alert rule.
**Asked at:** Alerting and drift-monitor material (an ICLR 2026 listing on false-alarm rates of drift detectors, an MLflow alerts playbook, GeoSurge, LeadDev and Rootly pages on thresholds, monitoring debt and alert fatigue); research and practitioner pages rather than an interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** The monitor is not wrong, it is answering the wrong question: with 2,000,000 rows the smallest KS statistic that is "significant" at 0.001 is about 0.002, so a real but tiny shift of 0.02 is 10 times past it; I would alert on effect size, calibrated on history and on feature importance, not on p-values.

**Clarifying questions:**
- Is the reference fixed at 2,000,000 rows, and how often is it refreshed? Critical D depends on both sample sizes (0.00195 at 2,000,000 against 2,000,000, but 0.0063 if the reference were only 100,000 rows), so a smaller or stale reference changes the reading.
- Are the features continuous or discrete or heavy with ties? KS p-values are only exact for continuous data; with ties they are conservative, and the statistic can be driven by one common value.
- How much does week-to-week variation (seasonality, pay cycles, promotions) move D normally? That sets the threshold.
- Which features matter to the model (importance, or a measured effect on the score)? Alerts should weigh by that.
- Who gets paged and for what? That sets the alert rule and who owns it.

**Approach:**
1. First 15 minutes (the page itself): check the AUC and score distribution on recent labelled data, which here is unchanged, then acknowledge, tag as a known false alert, and do not roll anything back. Escalate only if an important feature shows a large effect size or the score distribution moves.
2. Explain why it fires: under no change, 40 features at p below 0.001 would give about 0.04 flags a week. Getting 38 means these are 38 real but small differences (the sample is so large that any real difference is detected). In my simulation a 0.05 standard-deviation shift gives D about 0.02 at 2,000,000 rows, with a p-value that underflows to zero, and a 5,000-row subsample would not flag it (its critical D is 0.039).
3. Change the test: report the statistic (D, or a PSI or Wasserstein distance scaled by the feature spread) with a bootstrap interval, and decide on size, not on p. Optionally subsample to a fixed size so power is comparable across weeks, but the real fix is the threshold below.
4. Calibrate the effect-size threshold: take 26 weeks of week-over-week D under normal conditions. In my illustrative simulation with a seasonal wobble of 0.03 standard deviations, median D is 0.0085 and the 99th percentile is 0.0244, bigger than the 0.02 that fired. So 0.02 is inside natural variation. Pick a threshold several times above that (0.10 here, more than 3 x 0.0244), then check it against past incidents that did hurt the model.
5. Change the alert rule (illustrative): page when D is at least 0.10 on at least 2 of the 10 most important features, two weeks in a row. Everything else goes to a weekly digest, not a page. Add a model-output check (score distribution, and AUC or calibration on labels when they arrive) as the page for "the model is affected".
6. First day: ship the rule, re-send the last 8 weeks through it to count pages (should be near zero) and confirm that known past incidents would still page.
7. Next quarter: review the threshold every quarter against incidents, add a drift-to-impact mapping (how much AUC loss per unit of D, per feature), and delete alerts nobody acts on.
8. Blameless postmortem for alert fatigue: whoever set p<0.001 used the textbook default. Findings: no effect-size threshold, no owner, no review. Action items with owners.

**Rollback and escalation criteria (illustrative):**
- Escalate (page) on D of at least 0.10 on 2 or more important features for two weeks, or any move of the score distribution above its own threshold.
- Roll back the new alert rule if it misses a replayed historical incident, or if it pages more than once a month without a real issue.
- Treat any AUC or calibration drop beyond its own noise (use the labelled sample size) as an incident whatever the drift monitor says.

**Metrics:**
- KS statistic D = largest absolute difference between the two empirical cumulative distributions, on a 0 to 1 scale. Not a p-value.
- Flag share = features with p below 0.001 / features tested (38 / 40 = 95%). Misleading at this sample size.
- Alert precision = pages that were real issues / all pages. Target above 50%.
- Detection delay = time from a real shift to the page.
- Guardrails: AUC or calibration on the labelled sample, score distribution shift, pages per week.

**Risks:**
- A threshold set too high hides a slow decay, so watch cumulative drift over many weeks too.
- Ties and discrete features break the usual KS reading.
- A shift in several features each below threshold can still move the score; check the score itself.
- A constant reference goes stale; refresh it on a schedule with sign-off.

**What the interviewer scores:**
- Strong: explains sample size drives p to zero and quotes the critical D. Weak: "the data is drifting, retrain".
- Strong: separates statistical from practical significance, effect-size threshold calibrated on history. Weak: lowers p to 0.00001.
- Strong: weighs features by importance and checks model outputs. Weak: treats all 40 features alike.
- Strong: alert rule with consecutive weeks, owner and a review. Weak: no owner.
- Strong: blameless alert-fatigue postmortem. Weak: blames the monitoring engineer.

**Example:** Illustrative numbers. Weak: "38 of 40 features drifted, so I would retrain and tighten the p-value." Strong: "At 2,000,000 rows the critical D is 0.002, so D of 0.02 is 10 times critical but only a 0.05 standard-deviation shift. Normal week-to-week D reaches 0.024 in my history. I alert at D of 0.10 on two important features two weeks running, and I page on the score distribution and AUC, which are unchanged."

**Code:**
```python
# Illustrative numbers only. Why KS at 2,000,000 rows flags tiny shifts, and a calibrated effect-size alert rule.
import math, numpy as np
from scipy import stats
rng = np.random.default_rng(34)
n = 2_000_000
shift = 0.05
# 1. Critical KS statistic: smallest D that is "significant" at alpha = 0.001.
def d_crit(n1, n2, alpha=0.001):
    return math.sqrt(-math.log(alpha / 2) / 2) * math.sqrt((n1 + n2) / (n1 * n2))
dc = d_crit(n, n)
print('critical D at n=m=2,000,000, alpha=0.001:', round(dc, 5))
assert round(dc, 5) == 0.00195
print('observed D=0.02 is', round(0.02 / dc, 1), 'x the critical value')
assert 10 < 0.02 / dc < 11
print('critical D if the reference has only 100,000 rows:', round(d_crit(n, 100_000), 4))
assert round(d_crit(n, 100_000), 4) == 0.0063
print('critical D for 5,000 rows each:', round(d_crit(5000, 5000), 4))
assert d_crit(5000, 5000) > 0.02        # a 5,000-row subsample would NOT flag D=0.02
# 2a. One feature at the full 2,000,000 rows: a 0.05 sd shift gives D near 0.02 and a p-value that underflows to zero.
one = stats.ks_2samp(rng.standard_normal(n), rng.standard_normal(n) + 0.05)
print('2,000,000 rows, shift 0.05 sd: D', round(one.statistic, 4), 'p', one.pvalue)
assert 0.018 < one.statistic < 0.022 and one.pvalue < 0.001
# 2b. Scan of 40 features (300,000 rows each to keep the run short): 38 shifted by 0.05 sd, 2 untouched.
k = 300_000
flag, Ds = 0, []
for j in range(40):
    cur = rng.standard_normal(k) + (shift if j < 38 else 0.0)
    r = stats.ks_2samp(rng.standard_normal(k), cur)
    Ds.append(r.statistic); flag += r.pvalue < 0.001
print('flagged', flag, 'of 40 (', flag / 40, '), max D', round(max(Ds), 4))
assert flag == 38 and flag / 40 == 0.95 and max(Ds) < 0.03
# 3. Does a 0.05 sd shift hurt the model? Fixed logistic score on 5 features, labels from the true relation.
m = 200_000
w = np.array([0.8, 0.6, 0.5, 0.4, 0.3])
def auc(score, y):
    r = stats.rankdata(score); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
X0 = rng.standard_normal((m, 5)); X1 = rng.standard_normal((m, 5)) + shift
y0 = (rng.random(m) < 1 / (1 + np.exp(-(X0 @ w)))).astype(int)
y1 = (rng.random(m) < 1 / (1 + np.exp(-(X1 @ w)))).astype(int)
a0, a1 = auc(X0 @ w, y0), auc(X1 @ w, y1)
print('AUC before', round(a0, 4), 'after the shift', round(a1, 4))
assert abs(a1 - a0) < 0.005
# 4. Calibrate the effect-size threshold from history: 26 weeks of week-over-week D with natural wobble.
hist = []
base = rng.standard_normal(200_000)
for wk in range(26):
    mu = rng.normal(0, 0.03)                       # seasonal wobble in standard deviations
    hist.append(stats.ks_2samp(base, rng.standard_normal(200_000) + mu).statistic)
q99 = float(np.quantile(hist, 0.99))
print('week-over-week D: median', round(float(np.median(hist)), 4), '99th percentile', round(q99, 4))
thr = 0.10                                          # chosen effect-size threshold, several times the natural wobble
assert thr > 3 * q99 and max(Ds) < thr
# 5. Alert rule (illustrative): D >= thr on at least 2 of the 10 most important features, two weeks running.
def alert(weekly_D, imp_top10, k=2, weeks=2):
    hits = [sum(weekly_D[f] >= thr for f in imp_top10) >= k for weekly_D in weekly_D_history]
    return len(hits) >= weeks and all(hits[-weeks:])
weekly_D_history = [Ds, Ds]
assert not alert(None, range(10))                    # this week's D=0.02 does not alert
weekly_D_history = [[0.12] * 40, [0.15] * 40]
assert alert(None, range(10))
# 6. These are not chance false positives: under NO change, 40 features at p<0.001 give about 0.04 flags a week.
expected_null_flags = 40 * 0.001
print('expected flags per week under no change at p<0.001:', expected_null_flags, '; P(at least one):', round(1 - 0.999 ** 40, 4))
assert expected_null_flags == 0.04 and round(1 - 0.999 ** 40, 3) == 0.039
# 38 flags therefore mean 38 real but tiny differences; the fix is an effect-size rule, not a smaller p-value.
```

**Output (my run):**
```text
critical D at n=m=2,000,000, alpha=0.001: 0.00195
observed D=0.02 is 10.3 x the critical value
critical D if the reference has only 100,000 rows: 0.0063
critical D for 5,000 rows each: 0.039
2,000,000 rows, shift 0.05 sd: D 0.0207 p 0.0
flagged 38 of 40 ( 0.95 ), max D 0.0235
AUC before 0.7765 after the shift 0.776
week-over-week D: median 0.0085 99th percentile 0.0244
expected flags per week under no change at p<0.001: 0.04 ; P(at least one): 0.0392
```

**Follow-ups:**
- Why not just subsample? It restores a sensible p-value but throws away data and still has no notion of "big enough to matter". Use it with an effect-size threshold.
- How do you map D to impact? Perturb each feature by a known amount on a validation set and measure the AUC or score change, then set per-feature thresholds.
- Is the labelled AUC being unchanged proof of no harm? It means no harm large enough to see with that labelled sample size; compute its noise before relying on it.

**Common mistakes:** Treating p below 0.001 as "important". Using one threshold for all features. No effect-size floor. Ignoring ties in KS. Comparing to a stale or small reference. Paging on a statistic nobody has linked to model quality.

### Q35 ⭐⭐ 🔴 A training notebook containing a cloud access key was pushed to a public repository and a secret scanner flagged it 3 hours later. The key can read a bucket with 2,100,000 customer records, and the access logs show 14 downloads from addresses nobody recognises. What do you do in the first hour, in order, and what do you tell security, legal and the business?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to secrets and data leakage in ML repositories; related topics appear in public MLOps guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Treat it as a confirmed data breach: in the first hour I disable the key, preserve evidence, scope what the logs show, lock the bucket, and bring security and legal in at minute zero, because unknown addresses reading customer data is a SEV1 whatever the cause.

**Clarifying questions:**
- Can the key do anything besides read that bucket (IAM policy, other buckets, create users or keys)? A key that can write or create access is a bigger incident.
- What do the access logs list per download: object, bytes, source address, time? That is what turns "14 downloads" into an exposure number.
- Are the records personal data of regulated people (national IDs, financial data)? It sets the legal clock and who must be told.
- Who is the security on-call and who is the privacy or legal contact? Reaching them in the first minutes is part of the answer.
- Is the repository's host able to purge the commit and cached copies, and is the notebook output also public? Both are exposure paths.

**Approach (first hour, in order, illustrative minute marks):**
1. Minute 0: declare a SEV1, page security on-call and the privacy or legal contact, start a written timeline with names, times and decisions.
2. Minute 5: disable the key (deactivate, do not delete, so the logs and the record of what it did stay). Copy the repo and the notebook before any history rewrite. Rotating the key comes before cleaning the repo, because the key is already in the public history, forks and caches.
3. Minute 15: confirm the key no longer works. Read the key's permissions. Check the logs for anything it did beyond reads: new users, new keys, policy changes, writes or deletes. Any of those means a larger incident.
4. Minute 25: export access logs for the window from the push to now, with who, from where, which objects and how many bytes.
5. Minute 40: lock the bucket (deny by default except named roles) and rotate every other secret that was in the same notebook or repo.
6. Minute 50: make the repo private or take the notebook down, ask the host to purge cached copies, and scan the repo history for other secrets.
7. Minute 60: first written update, even if short: what is known, what is not, and when the next update comes.

**What I tell each audience (one line each, facts only):**
- Security: timeline, key permissions, logs exported, indicators (addresses, user agents), what I need from them (forensics, blocking addresses, review of other keys).
- Legal and privacy: what data, how many records at most (2,100,000), the exposure window (at least 3 hours before the flag plus time to revoke, 200 minutes at a 20-minute response), what the logs show so far. Regulatory and contractual notification clocks may start at awareness, so I ask them to decide now. Which law and which deadline applies is their call, and I do not state it myself.
- Business: customers may be affected, we have stopped the access, we are working out how many, the next update is at a stated time. No speculation and no promise before the numbers.

**First day:**
- Finish the log analysis: which objects each download read. Count unique records exposed as the union of objects read, never downloads times records. 14 x 2,100,000 = 29,400,000 is impossible because only 2,100,000 exist. In my illustrative log the 14 events read 14 of 21 equal objects, so 1,400,000 records at most for that log; if any event read the whole bucket the bound is 2,100,000.
- Work with legal on notification, and with security on blocking and monitoring.
- Review other keys in use by the team; rotate those with the same permissions.

**Next quarter:**
- No long-lived keys in notebooks: use short-lived credentials or a secret manager, and least-privilege roles with a network allowlist.
- Pre-commit and server-side secret scanning that blocks the push (scanners that block at push time exist in some platforms; that is editor knowledge, not tested here), a notebook template that strips outputs and secrets, and access alerts on unusual bulk reads.
- A tabletop exercise for exactly this incident, and a timed target for key revocation after a flag.

**Blameless postmortem:** The question is not who pasted the key. It is why a person could hold a key with that much power, why nothing stopped the push, and why the scanner took 3 hours. Findings: long-lived key, wide permission, scan after the push, no bulk-read alert. Action items each get an owner and a date. The engineer is a source of facts, not the subject.

**Rollback and escalation criteria (illustrative):**
- Treat it as SEV1 at once if logs show unknown addresses reading personal data (the case here).
- Escalate to the cloud account owner if the key cannot be disabled within 15 minutes.
- Raise to an integrity incident if any write, delete or permission change by that key appears.
- Close the incident only when the key is dead, access is locked down, the exposed-record count is final, and legal has recorded its decision.

**Metrics:**
- Exposure window = time from the push to the key being disabled (200 minutes at a 20-minute response).
- Detection delay = push to flag (3 hours here); target under 5 minutes with push-time scanning.
- Time to revoke = flag to key disabled; target under 20 minutes.
- Unique records exposed = records in the union of objects read by unknown addresses / total records (an upper bound until logs are reconciled).
- Guardrails: number of live long-lived keys, share of keys with least-privilege roles.

**Risks:**
- Deleting the key or rewriting history before copying evidence.
- Counting downloads times records, which exaggerates, or counting only one event, which understates.
- Cleaning up the repo and forgetting forks, caches and the notebook output.
- Public statements before legal and security agree.
- Other keys in the same notebook still live.

**What the interviewer scores:**
- Strong: revoke first, evidence preserved, legal and security at minute 0. Weak: starts by deleting the repo.
- Strong: scopes by logs and counts unique records. Weak: "all 2.1 million are gone" or "14 downloads is small".
- Strong: tells each audience facts, unknowns and next update time. Weak: vague or over-confident.
- Strong: prevention (short-lived credentials, least privilege, push-time scan). Weak: "tell people to be careful".
- Strong: blameless on process and tooling. Weak: names and blames the engineer.

**Example:** Illustrative numbers. Weak: "I would remove the notebook from GitHub and tell the team not to do that again." Strong: "First I disable the key and page security and legal, and I save the logs. The key was exposed at least 3 hours, so the unknown downloads are real. I count unique records from the objects the logs show, 2.1 million at most, not 14 times 2.1 million, and I give legal that number and the window so they can decide on notification."

**Code:**
```python
# Illustrative numbers only. Exposure window, record counts (unique, not downloads x records), and the first-hour order.
import random
push_to_flag_min = 3 * 60
flag_to_revoke_min = 20                      # target: key disabled within 20 minutes of the flag
window = push_to_flag_min + flag_to_revoke_min
print('exposure window (push to revoke), minutes:', window)
assert window == 200
downloads, records = 14, 2_100_000
rate = downloads / (push_to_flag_min / 60)   # if all 14 happened before the flag (the log will say)
print('downloads per hour if all before the flag:', round(rate, 2), '; per extra 10 minutes of delay:', round(rate / 6, 2))
assert round(rate, 2) == 4.67
# WRONG way to count: downloads x records. RIGHT way: union of objects actually read.
naive = downloads * records
assert naive == 29_400_000 and naive > records            # impossible: only 2,100,000 records exist
# Illustrative bucket: 21 objects x 100,000 records. 14 download events listing which objects were read.
rnd = random.Random(35)
objects = {f'part-{i:02d}': 100_000 for i in range(21)}
assert sum(objects.values()) == records
events = [rnd.sample(sorted(objects), rnd.choice([1, 2, 3, 4])) for _ in range(downloads)]
touched = set(k for ev in events for k in ev)
unique_records = sum(objects[k] for k in touched)
print('objects touched:', len(touched), 'of', len(objects), '-> unique records exposed (upper bound for this log):', unique_records)
assert unique_records <= records and unique_records >= max(len(ev) for ev in events) * 100_000
# If any one event listed the whole bucket (21 objects), the bound is the whole bucket.
full_copy_events = sum(1 for ev in events if len(ev) == 21)
assert (full_copy_events > 0) == (unique_records == records)
print('events that read the whole bucket:', full_copy_events, '-> exposed records:', unique_records)
# Bytes check: total bytes downloaded divided by bucket size says how many full copies left.
bucket_gb, downloaded_gb = 2.1, 3.15
print('full-copy equivalents downloaded:', downloaded_gb / bucket_gb)
assert downloaded_gb / bucket_gb == 1.5
# First hour, ordered, with minute marks (illustrative). Each step has a deadline and an owner.
plan = [
    (0,  'declare incident (SEV1), page security on-call + privacy/legal contact; start a timeline doc'),
    (5,  'DISABLE the key (do not delete); preserve logs and the repo copy before any history rewrite'),
    (15, 'confirm the key no longer works; list what else the key could reach (IAM policy), check for new users/keys/roles'),
    (25, 'export access logs for the window: who, from where, which objects, how many bytes'),
    (40, 'lock the bucket path (deny by default except named roles); rotate related secrets in the same notebook/repo'),
    (50, 'take the notebook down or make the repo private; ask host to purge cached copies; scan history for other secrets'),
    (60, 'first written update to security, legal and the business: known, unknown, next update time'),
]
mins = [m for m, _ in plan]
assert mins == sorted(mins) and mins[-1] == 60 and mins[1] <= 5
for m, a in plan: print(f'{m:>3} min  {a}')
# Escalation rules (illustrative)
rules = {'unknown_ip_reads_personal_data': 'SEV1 now', 'any_write_or_delete_in_logs': 'SEV1 plus integrity review', 'cannot_disable_key_in_15_min': 'escalate to cloud account owner'}
assert rules['unknown_ip_reads_personal_data'] == 'SEV1 now'
```

**Output (my run):**
```text
exposure window (push to revoke), minutes: 200
downloads per hour if all before the flag: 4.67 ; per extra 10 minutes of delay: 0.78
objects touched: 14 of 21 -> unique records exposed (upper bound for this log): 1400000
events that read the whole bucket: 0 -> exposed records: 1400000
full-copy equivalents downloaded: 1.5
  0 min  declare incident (SEV1), page security on-call + privacy/legal contact; start a timeline doc
  5 min  DISABLE the key (do not delete); preserve logs and the repo copy before any history rewrite
 15 min  confirm the key no longer works; list what else the key could reach (IAM policy), check for new users/keys/roles
 25 min  export access logs for the window: who, from where, which objects, how many bytes
 40 min  lock the bucket path (deny by default except named roles); rotate related secrets in the same notebook/repo
 50 min  take the notebook down or make the repo private; ask host to purge cached copies; scan history for other secrets
 60 min  first written update to security, legal and the business: known, unknown, next update time
```

**Follow-ups:**
- Should we force-push to remove the key from history? Only after copying the evidence, and it is not a fix: the key must already be dead, because forks and caches remain.
- What if the logs are incomplete? Say so, treat the whole bucket as exposed for the unmonitored period, and let legal decide.
- Does the 3-hour delay change the answer? It widens the window and shifts weight to prevention: push-time scanning shrinks it to minutes.

**Common mistakes:** Deleting rather than disabling the key. Cleaning the repo first. Multiplying downloads by records. Telling customers before legal agrees. Not rotating the other secrets in the same file. Blaming the engineer.

### Q36 ⭐ 🟢 The drift job itself failed 12 days ago because of an expired credential, and the dashboard kept showing the last computed values as if they were current. Nobody noticed until a model issue made someone check. How do you monitor the monitor, and what do you do about the 12 days with no coverage?
**Asked at:** Alerting and drift-monitor material (an ICLR 2026 listing on false-alarm rates of drift detectors, an MLflow alerts playbook, GeoSurge, LeadDev and Rootly pages on thresholds, monitoring debt and alert fatigue); research and practitioner pages rather than an interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** I monitor the monitor with a freshness stamp on the dashboard, a dead-man alert that fires when no successful run has landed in 1.5 intervals (36 hours instead of 12 days), and a nightly self-test; then I backfill the 12 missing days from retained logs before they expire.

**Clarifying questions:**
- How long are input and prediction logs retained? If 14 days, the first uncovered day expires in 2 days; if 30, in 18. This sets how fast the backfill must start.
- Did anything else fail with the same credential (other jobs, the model's own data feeds)? One expired credential rarely breaks one thing.
- Is the job idempotent per day partition? It decides whether I can safely re-run 12 days.
- Who owns the drift job and who gets its failure alert? If nobody was paged on failure, that is the root cause.
- What happened to the model in these 12 days (retrain, deploy, upstream change, labels)? It shapes the retroactive review.

**Approach:**
1. First 15 minutes: renew the credential, re-run the latest day, confirm the dashboard updates. Put a visible banner on the dashboard that says "no coverage from day X to day Y". Tell consumers of the dashboard, in one line, that the numbers were stale.
2. Check what else the credential touched, and whether the expiry broke other jobs silently.
3. Backfill, first day: re-run the job for each of the 12 daily partitions (idempotent, one partition at a time), then read the daily results. In my illustrative simulation, drift began on gap day 6 and the KS statistic first passed a 0.10 threshold on day 8, so 5 days of drift were unwatched. Treat this as a retroactive incident if drift shows up: check the model's labelled performance for those days and the decisions made.
4. If the logs are gone, record the gap as unrecoverable, use labels when they arrive to check performance for the period, and say so in the postmortem. Do not fill the gap with the last value.
5. Monitor the monitor (design):
   - Freshness stamp: the dashboard shows "computed at, covering up to" and turns red when the age is over 1.5 intervals (36 hours for a daily job). A dashboard that shows the last value without its age is the failure here.
   - Dead-man alert: pages when no successful run is recorded within 36 hours. Worst-case detection delay is 36 hours, not 288 (8x better), and at most 1 run missed before the first alert.
   - Failure alerts routed to a person, not a log.
   - Credential expiry alert at 14 days: it would have fired 26 days before today.
   - Self-test: inject a known shift (0.5 standard deviations in my test, D of 0.2) and require the alert, and a no-shift case that must stay quiet (D of 0.004). Run nightly and on every deploy of the monitor.
   - An independent watcher: a second, simpler check (or another team's job) that only looks at heartbeat timestamps.
6. First day (continued): add all of the above, put the credential in a rotation system, and write the runbook.
7. Next quarter: a quarterly "break the monitor on purpose" drill (expire a test credential, kill the job), an alert inventory with owners, and a rule that every dashboard shows data age.
8. Blameless postmortem: the monitor was part of the system and had no monitor. Timeline from expiry to discovery (12 days), why a failure produced no page, why a stale chart looked current. Findings and action items with owners; the person who found it by chance is thanked, not questioned.

**Rollback and escalation criteria (illustrative):**
- Page the owner if no successful run in 36 hours; page the platform lead at 72 hours.
- Escalate to the model owner if the backfill shows daily D of at least 0.10 on important features, or labelled performance outside its noise in the gap.
- If the backfill cannot finish before the oldest log expires, escalate to extend retention for the affected range first.
- Roll back the new alert if it pages more than twice a month for non-failures.

**Metrics:**
- Monitor freshness = now - time of last successful run (hours). Target under 36 for a daily job.
- Coverage = days with a successful drift result / days in the period. 12 days missing is a coverage hole.
- Detection delay = time from first missed run to first page (target 36 hours or less; actual 288).
- Self-test pass = injected shifts detected / injected shifts, and quiet cases that stayed quiet / quiet cases.
- Guardrails: alert volume, days to credential expiry.

**Risks:**
- A dead-man alert that depends on the same credential can fail silently too; send heartbeats from a different path.
- Backfilling against a reference that moved in the meantime gives misleading D values; use the reference that was current at the time.
- A noisy new alert gets muted; keep the dead-man alert separate and rare.
- Backfill load on the warehouse; run partitions one at a time.

**What the interviewer scores:**
- Strong: freshness stamp, dead-man alert, expiry alert, self-test with numbers. Weak: "add a failure email".
- Strong: handles the 12-day hole (backfill, retention clock, retroactive check). Weak: ignores the gap.
- Strong: notes the heartbeat must be independent of the thing it watches. Weak: monitors with the same credential.
- Strong: ordered actions and escalation times. Weak: flat list.
- Strong: blameless; thanks the person who noticed. Weak: asks who forgot to renew the credential.

**Example:** Illustrative numbers. Weak: "I would renew the credential and add an alert if the job fails." Strong: "A failure alert only works if the job runs. I add a dead-man alert on the last success timestamp, 36 hours for a daily job instead of 12 days, plus an expiry warning 14 days ahead. For the 12 days, I backfill each partition now, because with 14-day retention the first day expires in 2 days, then look for when drift began."

**Code:**
```python
# Illustrative numbers only. Detection delay for a silent monitor, retention clock for the backfill, and a monitor self-test.
import numpy as np
from scipy import stats
interval_h = 24
gap_days = 12
missed = gap_days                                         # one missed daily run per day
print('missed daily runs:', missed)
assert missed == 12
# Dead-man switch: alert if the newest successful run is older than 1.5 x interval.
threshold_h = 1.5 * interval_h
worst_detect_h = threshold_h                              # failure right after a success; first alert when age passes the threshold
print('worst-case detection delay with a dead-man switch (h):', worst_detect_h, 'vs actual', gap_days * 24)
assert worst_detect_h == 36 and gap_days * 24 == 288 and gap_days * 24 / worst_detect_h == 8.0
missed_with_switch = int(worst_detect_h // interval_h)    # runs missed before the first alert
assert missed_with_switch == 1
# Expiry warning would have fired well before the failure.
warn_days_before = 14
print('days before today that a 14-day expiry warning fires:', gap_days + warn_days_before)
assert gap_days + warn_days_before == 26
# Retention clock: can the gap still be backfilled? Prediction and input logs kept N days (illustrative).
for retention in (30, 14):
    oldest_age = gap_days                                 # age in days of the first uncovered day
    left = retention - oldest_age
    print(f'retention {retention} d: first uncovered day expires in {left} days')
assert 30 - gap_days == 18 and 14 - gap_days == 2
# Self-test of the monitor: inject a known shift, require the alert; run on every deploy and nightly.
def monitor(ref, cur, thr=0.10):
    d = stats.ks_2samp(ref, cur).statistic
    return d >= thr, d
rng = np.random.default_rng(36)
ref = rng.standard_normal(50_000)
fires, d_inj = monitor(ref, rng.standard_normal(50_000) + 0.5)          # synthetic shift of 0.5 sd
quiet, d_null = monitor(ref, rng.standard_normal(50_000))
print('injected shift D', round(d_inj, 3), 'fires', bool(fires), '| no shift D', round(d_null, 4), 'fires', bool(quiet))
assert fires and not quiet
# Backfill: re-run the job per day partition (idempotent), find when drift actually began inside the gap.
days = np.arange(1, gap_days + 1)
shift = np.where(days >= 6, 0.1 * (days - 5), 0.0)                       # drift began on gap day 6 and grew (invented)
Ds = [stats.ks_2samp(ref[:20_000], rng.standard_normal(20_000) + s).statistic for s in shift]
first = int(days[[d >= 0.10 for d in Ds].index(True)])
print('daily D over the gap:', [round(float(d), 2) for d in Ds])
print('first day over the 0.10 threshold:', first, '-> days of unwatched drift:', gap_days - first + 1)
assert first == 8 and gap_days - first + 1 == 5
# Dashboard: show 'as of' and turn red when stale.
def banner(age_h): return 'STALE' if age_h > threshold_h else 'ok'
assert banner(12) == 'ok' and banner(48) == 'STALE' and banner(288) == 'STALE'
```

**Output (my run):**
```text
missed daily runs: 12
worst-case detection delay with a dead-man switch (h): 36.0 vs actual 288
days before today that a 14-day expiry warning fires: 26
retention 30 d: first uncovered day expires in 18 days
retention 14 d: first uncovered day expires in 2 days
injected shift D 0.2 fires True | no shift D 0.0043 fires False
daily D over the gap: [0.01, 0.01, 0.01, 0.01, 0.01, 0.05, 0.08, 0.12, 0.16, 0.2, 0.24, 0.27]
first day over the 0.10 threshold: 8 -> days of unwatched drift: 5
```

**Follow-ups:**
- Why 1.5 intervals and not 1? A run can be a few hours late without being broken; 1.5 avoids a page for normal jitter.
- Who monitors the dead-man alert? A second, simple check owned by a different team, or a managed heartbeat service, with a weekly test page.
- What do you tell stakeholders about the gap? The dates, what was recovered by backfill, what could not be, and what changed.

**Common mistakes:** Showing last-known values with no age. Relying only on job-failure alerts. Using the same credential for the monitor and its watcher. Ignoring the retention clock on the backfill. Filling the gap with the last value. Hunting for the person who missed the renewal.

### Q37 ⭐ 🟡 A provider limits you to 200,000 tokens per minute, and your traffic is 150 requests per minute at 1,500 tokens each, which is 225,000 tokens per minute. That is 25,000 over the limit, about 11% of the demand (relative to the 225,000). Requests get rate-limit errors in bursts. What short-term and structural fixes do you consider, and why do extra API keys in one organisation usually not help?
**Asked at:** LLM-serving resilience pages (getmaxim, TrueFoundry, tianpan and Statsig pages on retries, 429 handling, fallbacks, circuit breakers and cost during failover; one snippet notes that silent quality degradation is invisible to HTTP success rates); practitioner material, no confirmed interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** Demand is 225,000 tokens a minute against a 200,000 limit, so I am 25,000 over (11.1% of demand, 12.5% of the limit); retries and queues cannot fix a sustained gap, so I cut demand or add capacity, and extra keys in one organisation do not add capacity because the limit sits on the organisation, not the key.

**Clarifying questions:**
- Is the 225,000 a steady average or a peak? If it is a peak, a queue and smoothing may be enough; if it is the average, nothing but less demand or more quota works.
- Did anything change recently, such as a longer prompt, a new feature or a retry loop? A change gives me a rollback option and a blameless-postmortem thread.
- Which calls are user-facing and which are batch or background? I shed or delay background first.
- What does the provider's limit apply to (organisation, project, model, tokens in plus out)? Keys, projects and model families can have different buckets. I check the provider's current docs; I do not assume.
- What is the cost and quality of a fallback model? A cheaper model may answer, but output shape and quality can differ.

**Approach:**
1. First 15 minutes (stop the bleeding): check the change log for what raised tokens. Pause or slow background and batch calls. Turn on exponential backoff with jitter and honour the provider's retry-after hint if it sends one (editor knowledge: many providers do; check yours). Cap retries so they do not add to the load.
2. First 15 minutes (decide): if a recent release inflated prompts and a known-good version exists, roll back that release. If not, keep going with shedding and the fallback.
3. First day: put a client-side limiter in front of the provider (token bucket sized a little under the limit) so we queue by priority and fail fast instead of hitting 429s. Trim demand: cache repeated answers, shorten system prompts, cap output length. Compute the target: 11.1% less demand, so 133 requests a minute at 1,500 tokens or 1,333 tokens a request at 150 a minute.
4. First day: ask the provider for a higher quota or tier (it takes time, so start it now). Route low-priority traffic to a second provider or a smaller model only after a quality check; a fallback that returns the wrong shape is its own incident.
5. Next quarter: capacity planning on tokens per minute, not requests; alert at 80% of the limit; load test; a fallback chain with a circuit breaker and a game day; token budgets per feature with owners.
6. Escalation criteria: if user-facing 429s stay above the agreed error budget for 30 minutes after shedding, escalate to the product owner for a quality-degraded mode, and open the quota ticket at the provider.
7. Blameless angle: the question is not who shipped the longer prompt, it is why nothing alerted at 80% of quota and why the retry loop could amplify a limit. Action items are about alerts, limiter and budgets.

**Metrics:**
- Token demand per minute = sum of (prompt plus completion tokens) in the minute, from our own logs, divided by the limit (utilisation); guardrail: alert at 80%.
- 429 rate = rejected calls divided by all calls in the minute (not only user-facing).
- Wait time of queued requests (p95), and share of requests served by the fallback with its own quality score.
- Cost per successful request, because failover and retries raise it.

**Risks:**
- Retries without a cap make a limit incident worse: every rejected call comes back.
- A queue that fills faster than it drains just turns errors into long waits (in my run the wait for a new request reaches 7.5 minutes after an hour).
- A fallback model that "succeeds" with worse output hides the problem from HTTP success rates.
- Treating the rate limit as the root cause when a prompt-size regression is the real change.

**What the interviewer scores:**
- Strong: separates short-term (shed, back off, limiter) from structural (quota, caching, token budget, second provider); computes 25,000 and 11.1%; names the base of the percentage.
- Strong: says why keys in one organisation do not help, and hedges that this depends on the provider's rules.
- Strong: mentions fallback quality and cost, and a blameless follow-up that fixes alerts.
- Weak: "add more keys" or "retry harder"; no arithmetic; blames the team that shipped the change.

**Example:** Illustrative numbers. 150 requests a minute at 1,500 tokens is 225,000. Limit 200,000. Cutting 15% of tokens per request (caching, shorter prompts) gives 191,250 and 8,750 of headroom, and in my run bursts still get about 4% rejected, so I also add a queue with backoff.
- Weak: "add more keys" or "retry harder"; no arithmetic; blames the team that shipped the change.

**Example:** Illustrative numbers. 150 requests a minute at 1,500 tokens is 225,000. Limit 200,000. Caching 10% of requests and trimming 5% of tokens on the rest leaves about 192,000 (see code for a close version), a 4% burst reject rate remains, so I add a queue with backoff.
- Weak: "We are getting 429s, so I will create more API keys and retry until it works."
- Strong: "We are 25,000 tokens a minute over, about 11% of demand. In the next fifteen minutes I slow batch calls and cap retries with jitter. Today I add a token-bucket limiter, cache and trim prompts to get under about 190,000, and ask for more quota. More keys in the same organisation usually share one limit, so they would not help; I would confirm that in the provider's docs. Afterwards we alert at 80% of quota and review without blame why nobody saw this coming."

**Code:**
```python
# Q37: rate limit of 200,000 tokens/min; demand 150 req/min x 1,500 tokens (invented numbers)
import random
from collections import deque

LIMIT = 200_000
RPM, TOK = 150, 1_500
demand = RPM * TOK
over = demand - LIMIT
print("demand", demand, "over", over, "share of demand", round(over / demand, 4),
      "share of limit", round(over / LIMIT, 4))
assert demand == 225_000 and over == 25_000
assert round(over / demand, 3) == 0.111 and round(over / LIMIT, 3) == 0.125

# Sustained overload: a client-side queue only moves the pain into waiting time.
backlog = 0
for minute in range(1, 61):
    backlog += over            # tokens that cannot be sent this minute pile up
wait_min = backlog / LIMIT     # how long a new request waits behind the backlog
print("backlog after 60 min (tokens)", backlog, "wait for a new request (min)", wait_min)
assert backlog == 1_500_000 and wait_min == 7.5

# What it takes to fit: cut demand by 11.1%, i.e. fewer requests or fewer tokens each
max_rpm = LIMIT // TOK                  # 133 requests/min at 1,500 tokens
max_tok = LIMIT // RPM                  # 1,333 tokens per request at 150/min
print("fits at", max_rpm, "req/min or", max_tok, "tokens/request")
assert max_rpm == 133 and max_tok == 1333

# Bursty arrivals: a sliding 60 s window limit, Poisson arrivals, seed fixed.
def run(keys, seed=7, secs=1800, rate_per_s=RPM / 60, tok=TOK):
    """Limit is shared by the whole organisation, whatever key signs the request
    (an ASSUMPTION about the provider; check its docs)."""
    rnd = random.Random(seed)
    win = deque()           # (time, tokens) accepted in the last 60 s, shared
    used = rejected = total = 0
    t = 0.0
    while t < secs:
        t += rnd.expovariate(rate_per_s)
        key = rnd.randrange(keys)           # which key sent it: irrelevant to the limit
        while win and win[0][0] <= t - 60:
            used -= win.popleft()[1]
        total += 1
        if used + tok > LIMIT:
            rejected += 1
        else:
            win.append((t, tok)); used += tok
    return rejected / total

r1, r4 = run(1), run(4)
print("rejected share, 1 key:", round(r1, 3), "| 4 keys, same org limit:", round(r4, 3))
assert r1 == r4                                   # same arrivals, same shared bucket
assert 0.08 < r1 < 0.16                           # near the 11% overload, burstiness adds a bit

# Same traffic, but trimmed 15% by caching + shorter prompts: bursts still hit, far less
TOK2 = int(TOK * 0.85)
r_trim = run(1, tok=TOK2)
print("trimmed demand", RPM * TOK2, "headroom", LIMIT - RPM * TOK2, "rejected share", round(r_trim, 3))
assert r_trim < 0.05 < r1
assert RPM * TOK2 == 191_250 and LIMIT - RPM * TOK2 == 8_750
```

**Output (my run):**
```text
demand 225000 over 25000 share of demand 0.1111 share of limit 0.125
backlog after 60 min (tokens) 1500000 wait for a new request (min) 7.5
fits at 133 req/min or 1333 tokens/request
rejected share, 1 key: 0.151 | 4 keys, same org limit: 0.151
trimmed demand 191250 headroom 8750 rejected share 0.043
```

**Follow-ups:**
- What if the provider says the key limit is per key? Then keys can help, but I treat that as a provider-specific fact I check, and I still have to manage one budget and cost across keys.
- Queue or shed? Queue what can wait (batch), shed what cannot be answered in time (stale user requests), and keep the reject rate visible. See also Book 6 Part 7 Q25 for retries that resend big prompts.

**Common mistakes:** Retry storms. Counting requests instead of tokens. Assuming keys multiply the limit. Declaring a fallback model equal without a quality check. A postmortem that names a person.

### Q38 ⭐ 🟡 A model service handles 1,000 requests per second and has a capacity of 1,500. During a 5-second slowdown every request times out and the clients retry up to 3 times at once, so the offered load can reach 4,000 requests per second, the original plus 3 retries each. How does this turn a short slowdown into an outage, and what do you add on the client and the server side?
**Asked at:** LLM-serving resilience pages (getmaxim, TrueFoundry, tianpan and Statsig pages on retries, 429 handling, fallbacks, circuit breakers and cost during failover; one snippet notes that silent quality degradation is invisible to HTTP success rates); practitioner material, no confirmed interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** The service runs at 67% of capacity (1,000 of 1,500) and a 5-second slowdown makes every call time out, so each client sends up to 3 retries at once and the offered load reaches 4,000 per second, 2.67 times capacity; the retries, not the slowdown, are what keep it down, so I add jittered backoff, a retry budget and a circuit breaker on the client and load shedding and deadline checks on the server.

**Clarifying questions:**
- Do the clients retry immediately, with backoff, or with jitter? Immediate and synchronised retries are the worst case behind the 4,000.
- Does the server queue requests, and does it drop work whose client already timed out? If not, it burns capacity on answers nobody reads.
- Are calls idempotent? Retrying a non-idempotent write can double-charge or double-score.
- Who owns the clients (one team or many)? Fixes on the client need that many owners.
- What was the 5-second trigger (deploy, GC pause, cold node, dependency)? That decides rollback versus fix.

**Approach:**
1. First 15 minutes: see if the load is still above capacity after the trigger is gone. If yes, you are in a retry loop. Shed load at the edge (reject a share of traffic with a fast 503 and a retry-after hint), scale out if autoscaling can respond in minutes, and pause non-urgent callers.
2. First 15 minutes: roll back the change that caused the slowdown if there was a deploy in the last hour and the previous version is known good. Escalate to the dependency owner if a downstream is slow.
3. Why a short slowdown becomes an outage: during the 5 seconds offered load goes 1,000, 2,000, 3,000, 4,000, 4,000 per second. When the server recovers, it still holds the old attempts in its queue and works on them first although their clients gave up, so fresh calls wait behind dead ones and time out too. In my simplified run the naive service never recovers; this is a metastable failure, shown here only in a toy model.
4. First day, client side: exponential backoff with full jitter, a retry budget (retries capped at about 10% of calls), a per-call deadline, and a circuit breaker that stops sending when failures stay high. Only retry idempotent calls or send an idempotency key.
5. First day, server side: a bounded queue, load shedding when queue wait is above the client timeout, drop requests whose deadline has passed, and a concurrency limit per replica.
6. Next quarter: a load test that injects a 5-second stall and checks recovery time, retry-rate dashboards, a game day, and a shared client library so one fix reaches all callers.
7. Rollback and escalation criteria: roll back if the slowdown started within an hour of a change; escalate to the incident commander if shedding does not bring the error rate under the agreed limit within 15 minutes.
8. Blameless angle: nobody wrote "bad code"; the system let a retry policy multiply load by 4 and had no brake. The postmortem asks why there was no retry budget and no alert on retry ratio.

**Metrics:**
- Retry ratio = retry attempts divided by first attempts, per second (alert when above 10%).
- Offered load divided by capacity (utilisation) and queue wait p99.
- Goodput = attempts completed within the client timeout per second (in my sim a successful retry counts too, which is why it can exceed 1,000 for a few seconds).
- Time to recover after the trigger ends; guardrail: it should be seconds, not minutes.

**Risks:**
- Capacity headroom alone (50% over normal) does not protect you if the multiplier is 4.
- A circuit breaker that opens too soon turns a blip into a full stop; one that never opens does nothing.
- Shedding the wrong requests (the paying or latency-critical ones) hurts more than the slowdown.
- Toy model: real servers differ; use the numbers to explain the mechanism, not to predict your service.

**What the interviewer scores:**
- Strong: gets 4,000 and 2.67 times capacity right, says it is a worst case with all clients retrying together, and explains dead work in the queue.
- Strong: names client fixes (backoff with jitter, retry budget, deadline, breaker) and server fixes (shed, bounded queue, drop expired work) and idempotency.
- Strong: gives the 15 minute, one day and quarter order and a blameless action item.
- Weak: "scale up" only; "increase timeouts" (which delays the failure signal and keeps dead work longer).

**Example:** Illustrative. Normal 1,000 per second, capacity 1,500. A 5-second stall with 3 immediate retries gives offered load 1,000, 2,000, 3,000, 4,000, 4,000.
- Weak: "Our capacity is 1,500, so we just need more pods and a longer timeout."
- Strong: "Retries turned a 5-second stall into an outage: offered load went to 4,000, nearly three times capacity, and the server kept working on requests whose clients had gone. I would shed at the edge now, roll back the trigger if it was a deploy, and then ship jittered backoff, a 10% retry budget, a circuit breaker, and server-side dropping of expired requests. The postmortem is blameless: we ask why no retry budget existed."

**Code:**
```python
# Q38: retry amplification; 1,000 rps normal, capacity 1,500 rps, 5 s slowdown (invented numbers)
from collections import deque

NORMAL, CAP, SLOW_S, RETRIES = 1000, 1500, 5, 3
# Simple arithmetic first
peak_offered = NORMAL * (1 + RETRIES)
print("worst-case offered load", peak_offered, "= x", round(peak_offered / CAP, 2), "of capacity")
assert peak_offered == 4000 and round(peak_offered / CAP, 2) == 2.67
assert NORMAL / CAP < 0.67            # normally 67% utilised, 33% headroom
# Amplification: the offered load a request-level retry creates in the 5 s window
offered = [NORMAL * (1 + min(s, RETRIES)) for s in range(SLOW_S)]
print("offered load per second during slowdown", offered)
assert offered == [1000, 2000, 3000, 4000, 4000]

def sim(shed_dead, retry_cap, horizon=40):
    """1-second steps. Server completes up to CAP attempts per second (0 during the slowdown),
    oldest first. An attempt only counts if it is served in the second it arrived
    (client timeout = 1 s). Timed-out requests are retried next second, up to RETRIES.
    shed_dead: server drops attempts whose client already gave up (cheap) instead of working on them.
    retry_cap: max retries admitted per second (None = unlimited)."""
    q = deque()                     # [arrival_second, count]
    retry_in = 0                    # retries arriving next second, by attempt number
    carry = [0] * (RETRIES + 1)     # carry[k] = attempts of number k arriving now
    goodput = []
    peak = 0
    for t in range(horizon):
        arr = [0] * (RETRIES + 1)
        arr[0] = NORMAL
        for k in range(1, RETRIES + 1):
            arr[k] = carry[k]
        if retry_cap is not None:
            extra = sum(arr[1:])
            if extra > retry_cap:                       # client-side retry budget
                scale = retry_cap / extra
                arr = [arr[0]] + [int(x * scale) for x in arr[1:]]
        total = sum(arr); peak = max(peak, total)
        q.append([t, arr])
        cap = 0 if t < SLOW_S else CAP
        served_ok = 0
        newq = deque()
        for ts, a in q:
            n = sum(a)
            if ts < t and shed_dead:
                continue                                # dead work dropped at no cost
            take = min(n, cap)
            cap -= take
            if ts == t:
                served_ok += take
            if take < n:                                # unserved remainder stays queued
                keep = [x * (n - take) // n if n else 0 for x in a]
                newq.append([ts, keep])
        q = newq
        goodput.append(served_ok)
        # attempts not served this second time out; they come back as next attempt number
        fail = [0] * (RETRIES + 1)
        for ts, a in q:
            if ts == t:
                fail = a
        carry = [0] * (RETRIES + 1)
        for k in range(RETRIES):
            carry[k + 1] = fail[k]
    return goodput, peak

def recovery(g):
    for t in range(SLOW_S, len(g)):
        if g[t] >= 0.95 * NORMAL:
            return t - SLOW_S
    return None

for name, shed, cap in [("naive: FIFO, retries unlimited", False, None),
                        ("server drops dead work", True, None),
                        ("drop dead work + retry budget 100/s", True, 100)]:
    g, pk = sim(shed, cap)
    print(f"{name:40} peak offered {pk:5}  secs to recover after slowdown:", recovery(g),
          " goodput t=5..9:", g[5:10])

g_naive, _ = sim(False, None)
g_shed, _ = sim(True, None)
g_best, pk_best = sim(True, 100)
assert recovery(g_naive) is None                    # in this simple model it never recovers
assert recovery(g_shed) is not None
assert recovery(g_best) is not None and recovery(g_best) <= recovery(g_shed)
assert pk_best <= NORMAL + 100
```

**Output (my run):**
```text
worst-case offered load 4000 = x 2.67 of capacity
offered load per second during slowdown [1000, 2000, 3000, 4000, 4000]
naive: FIFO, retries unlimited           peak offered  4000  secs to recover after slowdown: None  goodput t=5..9: [0, 0, 0, 0, 0]
server drops dead work                   peak offered  4000  secs to recover after slowdown: 0  goodput t=5..9: [1500, 1500, 1500, 1490, 1000]
drop dead work + retry budget 100/s      peak offered  1100  secs to recover after slowdown: 0  goodput t=5..9: [1098, 1000, 1000, 1000, 1000]
```

**Follow-ups:**
- Why jitter and not just exponential backoff? Without jitter all clients retry at the same instants and keep the waves synchronised.
- Is a timeout increase a fix? It reduces false timeouts for slow but healthy calls, but it lengthens how long dead work sits in queues; set it from the latency distribution and add deadlines.
- Cross-reference: Book 4 Part 6 Q40 covers where p99 latency comes from (queueing near saturation); Book 6 Part 7 Q25 covers retry cost for LLM calls.

**Common mistakes:** Treating the 4,000 as a prediction rather than an upper bound. Retrying non-idempotent calls. Raising timeouts instead of adding deadlines. Fixing only the server when many clients retry. Blaming the client team.

### Q39 ⭐ 🟡 A team promises that 95% of daily batch scoring runs finish by 07:00. Over 28 days it missed on 3 days, so 25 of 28 runs made it, which is 89.3%. How many whole misses would the objective have allowed over 28 days, what do you do when the budget is gone, and is a lateness objective enough for a model that can also be wrong?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to SLOs and error budgets for batch ML pipelines; related topics appear in public MLOps guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** 5% of 28 runs is 1.4, so the objective allows 1 whole miss (27 of 28 is 96.4%, 26 of 28 is 92.9%, below the 95% target); 3 misses use about 214% of the budget, so the budget is gone and I freeze risky changes, fix the cause, and add a correctness objective, because on time is not the same as right.

**Clarifying questions:**
- Is the objective a rolling 28-day window or a calendar month? It decides when the budget comes back.
- What does "finish by 07:00" cover: the scoring job only, or the delivery to the consumer? A job that finishes at 06:55 but is not published until 07:10 is a miss for the user.
- What were the 3 misses (one cause or three)? One cause repeated is a fix; three different causes is a fragile pipeline.
- Who consumes the scores at 07:00 and what do they do if they are late? That is the cost of a miss and tells me if 95% is the right target.
- Is there a data-quality or accuracy objective today? If not, a pipeline can meet lateness while shipping bad scores.

**Approach:**
1. Compute the budget: 28 x 5% = 1.4, so 1 whole miss. Actual: 25 of 28 on time, which is 89.3% (a sample of 28 runs, not a rate with a tight interval). Misses are 3, so the budget is overspent by 2 whole misses.
2. First 15 minutes (if a run is late right now): check which stage is slow, whether upstream data arrived, and whether a rerun or a partial score is acceptable. Roll back a recent pipeline change if the lateness began with it. Tell consumers the ETA.
3. First day: write down the three misses with cause, detection time and fix. Add an alert on "not finished by 06:30" so a miss is visible while there is still time to act.
4. Policy when the budget is gone: pause non-reliability releases to this pipeline, spend the time on the top cause, resume when the rolling window is back within the objective (in my example that is day 38 with the miss on day 3 and day 10 still counting down).
5. Next quarter: add a data-quality objective (for example, null rate of key features under 5% on 95% of runs) and a model-quality check on a labelled slice, and report all three together.
6. Escalation: if two further misses occur while the freeze is on, escalate to the owning manager and the consuming team to renegotiate the target or fund redundancy.
7. Blameless angle: the objective turns the argument from "who was late" into "how much unreliability we agreed to".

**Metrics:**
- On-time rate = runs published by 07:00 divided by runs scheduled, over the rolling 28 days.
- Budget consumed = misses divided by (28 x 5%) = misses / 1.4.
- Data-quality rate = runs with null rate at or below the limit divided by all runs.
- Guardrail: time to detect a miss (target: before 07:00, not after).

**Risks:**
- 28 runs is small: one extra miss moves the rate by 3.6 points, so do not over-read a single month.
- A lateness objective is gameable: publish an empty or stale file on time.
- Whole misses allowed rounds down; 1.4 means you cannot spend "1.4 misses".
- A freeze can hide the cause if nobody is assigned to the fix.

**What the interviewer scores:**
- Strong: 1 whole miss allowed, 214% consumed, can say which side of 95% one and two misses fall on.
- Strong: a concrete budget policy (freeze, fix, resume rule) and when the budget returns.
- Strong: says lateness is not correctness and adds a quality objective.
- Weak: "89.3% is close to 95%" or "allowed 1.4 misses".

**Example:** Illustrative. 28 runs, 95% target: 1 miss gives 96.4%, 2 give 92.9%. Actual 3 misses give 89.3%.
- Weak: "We were at 89%, close to target, so we carry on and try to do better."
- Strong: "Our budget was one miss in 28 days and we had three, about 214% of it. I would freeze non-essential changes to the pipeline, write up the three causes without blame, add an alert at 06:30, and resume when the rolling window is back to one miss. Also, being on time does not mean the scores are right, so I would add a null-rate and accuracy-slice objective."

**Code:**
```python
# Q39: 95% on-time objective over 28 daily runs (invented numbers)
import math

N, TARGET = 28, 0.95
allowed = math.floor(N * (1 - TARGET) + 1e-9)       # whole misses allowed
exact = N * (1 - TARGET)
print("budget (fractional misses):", round(exact, 2), "-> whole misses allowed:", allowed)
assert round(exact, 2) == 1.4 and allowed == 1
print("1 miss ->", round(27 / 28, 4), "| 2 misses ->", round(26 / 28, 4), "(below 0.95)")
assert 27 / 28 >= TARGET and 26 / 28 < TARGET

misses = 3
on_time = N - misses
print("actual on-time", on_time, "/", N, "=", round(on_time / N, 4))
assert on_time == 25 and round(on_time / N, 3) == 0.893
print("budget used", round(misses / exact, 2), "of the budget (", round(misses / exact * 100), "%)")
assert round(misses / exact, 2) == 2.14
print("overspend: ", misses - allowed, "whole misses over the allowed 1")
assert misses - allowed == 2

# When does the budget come back? Rolling 28-day window; invented miss days.
miss_days = [3, 10, 20]
for today in (28, 31, 38, 48):
    in_win = [d for d in miss_days if today - 27 <= d <= today]
    ok = len(in_win) <= allowed
    print(f"day {today}: misses in window {len(in_win)} -> within objective: {ok}")
assert [len([d for d in miss_days if t - 27 <= d <= t]) for t in (28, 31, 38, 48)] == [3, 2, 1, 0]

# A lateness SLO says nothing about wrongness. Same 28 runs, all on time, one silently bad.
runs = [{"on_time": True, "null_rate": 0.01} for _ in range(N)]
runs[17] = {"on_time": True, "null_rate": 0.31}     # an upstream column went mostly null
lateness_ok = sum(r["on_time"] for r in runs) / N
quality_ok = sum(r["null_rate"] <= 0.05 for r in runs) / N      # a data-quality objective
print("lateness objective:", lateness_ok, "| data-quality objective:", round(quality_ok, 3))
assert lateness_ok == 1.0 and round(quality_ok, 3) == 0.964
assert quality_ok >= 0.95 and (N - 2) / N < 0.95
```

**Output (my run):**
```text
budget (fractional misses): 1.4 -> whole misses allowed: 1
1 miss -> 0.9643 | 2 misses -> 0.9286 (below 0.95)
actual on-time 25 / 28 = 0.8929
budget used 2.14 of the budget ( 214 %)
overspend:  2 whole misses over the allowed 1
day 28: misses in window 3 -> within objective: False
day 31: misses in window 2 -> within objective: False
day 38: misses in window 1 -> within objective: True
day 48: misses in window 0 -> within objective: True
lateness objective: 1.0 | data-quality objective: 0.964
```

**Follow-ups:**
- Why a rolling window and not a calendar month? A calendar reset gives a full budget on day 1 even right after a bad week; a rolling window forgets slowly.
- Should the target be 99%? Only if the cost of a miss justifies the engineering cost; ask the consumers.
- Cross-reference: Book 4 Part 8 Q27 covers runbooks, ownership and on-call for model alerts.

**Common mistakes:** Rounding the budget up. Calling 28 runs a precise rate. Measuring job end instead of when scores are usable. Having only a lateness objective. Using the budget to blame a person.

### Q40 ⭐ 🟡 A 20-hour training run on preemptible nodes is interrupted 4 times, and it checkpoints every 3 hours. On average a preemption loses half a checkpoint interval, which is 1.5 hours, and the worst case loses 3. Compute the expected and the worst-case lost work across the 4 interruptions, and say how you would pick the checkpoint interval and verify that resume gives the same model.
**Asked at:** GPU-serving and autoscaling pages (apxml and system-design.space on autoscaling and serving architecture; vendor pages from regolo.ai and lyceum.technology on cold starts and capacity, treated as vendor claims); no public postmortem located; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** With a 3-hour checkpoint interval, each preemption loses 1.5 hours on average and 3 at worst, so 4 preemptions cost about 6 hours expected and 12 hours worst case (26 and 32 hours of compute for the 20-hour run); I pick the interval from checkpoint cost and interruption rate, and I prove resume by running to the same final weights from a checkpoint.

**Clarifying questions:**
- How long does one checkpoint take and how big is it? That is the cost C in the interval choice.
- What is the real interruption rate (4 in 20 hours is a sample, an average of one per 5 hours)? A different rate changes the interval.
- Is the loss expected to be reproducible bit for bit, or is "statistically equivalent" enough? It decides how much state I must save.
- Does the job restart on a fresh node and how long does the restart (image pull, data load) take? Restart time is lost work too, on top of the replayed 1.5 hours.
- Is there a deadline or a cost cap? It sets how much waste I accept.

**Approach:**
1. Arithmetic: expected lost = 4 x 1.5 = 6 hours, worst = 4 x 3 = 12 hours, assuming preemption is equally likely at any moment (my simulation gives a mean loss of 1.5 hours per preemption). Add restart time to both.
2. First 15 minutes (a run was just preempted): confirm the job resumed from the last checkpoint and not from step 0, check that the checkpoint is complete (checksum or a "done" marker), and watch the loss curve for a jump.
3. First day: choose the interval. A first-order rule (Young) is T = sqrt(2 x C x MTBF): with C = 3 minutes and an interruption every 5 hours that is about 42 minutes, giving overhead of about 2.8 hours against 6.3 hours at 3 hours. This is a computed rule of thumb with invented inputs; measure your own C.
4. First day: save everything that affects the next step: weights, optimizer state (momentum), learning-rate schedule position, step counter, data-loader position or seed and the RNG states. Write to a temp name, then rename, so a half-written file is never read.
5. Verify resume: train N steps straight, versus train to step k, checkpoint, resume to N, and compare final weights. In my toy run they are identical; dropping the RNG state or the optimizer state made them differ.
6. Next quarter: automatic resume in the scheduler, checkpoint retention (keep last few), alerts on repeated preemption, and a fallback to on-demand nodes if preemptions exceed a threshold (editor judgement).
7. Rollback or escalation criteria: if more than two preemptions occur within one checkpoint interval, move to on-demand capacity or escalate to the budget owner; if a resumed run's loss differs sharply from the straight run, stop and treat the checkpoint as corrupt.
8. Blameless angle: preemption is a normal event of cheap capacity; the lesson is "our resume was never tested", not "the engineer lost 6 hours".

**Metrics:**
- Lost work per preemption = time since last complete checkpoint, divided into total training time to get waste share (6 of 26 hours is 23% in the expected case).
- Checkpoint overhead = checkpoint count x checkpoint time divided by run time.
- Resume equality = maximum absolute difference of final weights between straight and resumed runs (0 for bit-exact, or within a tolerance if non-deterministic kernels are used).

**Risks:**
- Bit-exact resume is not guaranteed on GPUs with non-deterministic kernels; test with a tolerance and say so.
- A checkpoint taken during a write can be corrupt; use atomic rename and checksums.
- Too-frequent checkpoints can stall training more than preemptions do.
- 4 interruptions is a small sample; do not tune hard to it.

**What the interviewer scores:**
- Strong: 6 and 12 hours, states the uniform assumption, adds restart cost.
- Strong: a principled interval (cost versus loss), with the formula called a rule of thumb.
- Strong: lists the state to save and a concrete resume-equals-straight test.
- Weak: "checkpoint every epoch" with no reasoning; saves weights only.

**Example:** Illustrative. 20-hour run, 4 preemptions, 3-hour interval.
- Weak: "We lose a few hours, that is fine, spot is cheap."
- Strong: "Expected loss is 4 times 1.5, six hours, worst case twelve. With a 3-minute checkpoint and an interruption every 5 hours, a 40-minute interval cuts the overhead from about 6.3 to 2.8 hours. We save weights, optimizer state, step and RNG state, write atomically, and run a test that resumes from step 120 and matches the straight run."

**Code:**
```python
# Q40: preemptible training, 20 h run, 4 interruptions, checkpoint every 3 h (invented numbers)
import math, random
import numpy as np

RUN_H, N_INT, CK_H = 20, 4, 3.0
exp_loss = N_INT * CK_H / 2
worst_loss = N_INT * CK_H
print("expected lost work", exp_loss, "h | worst case", worst_loss, "h")
assert exp_loss == 6.0 and worst_loss == 12.0
print("expected total compute", RUN_H + exp_loss, "h | worst", RUN_H + worst_loss, "h")
assert RUN_H + exp_loss == 26.0 and RUN_H + worst_loss == 32.0

# Check the 'half an interval' average by simulation: preemption at a uniform random time
rnd = random.Random(3)
losses = [(rnd.uniform(0, 1000) % CK_H) for _ in range(100_000)]
print("simulated mean loss per preemption", round(sum(losses) / len(losses), 3), "max", round(max(losses), 3))
assert abs(sum(losses) / len(losses) - 1.5) < 0.02 and max(losses) < 3.0

# Choosing the interval: Young's first-order rule T = sqrt(2 * C * MTBF), C = cost of one checkpoint
C_h = 3 / 60                       # 3 minutes per checkpoint (invented)
mtbf_h = RUN_H / N_INT             # 5 h between interruptions
t_opt = math.sqrt(2 * C_h * mtbf_h)
print("Young interval (h):", round(t_opt, 2), "=", round(t_opt * 60), "min")
assert round(t_opt, 2) == 0.71

def overhead(T):                   # checkpoint cost + expected re-done work, hours over the run
    return (RUN_H / T) * C_h + N_INT * T / 2
for T in (3.0, 1.0, t_opt, 0.25):
    print(f"interval {T:5.2f} h -> overhead {overhead(T):5.2f} h")
assert overhead(t_opt) < overhead(3.0) and overhead(t_opt) < overhead(0.25)
assert round(overhead(3.0), 2) == 6.33 and round(overhead(t_opt), 2) == 2.83

# Does resume give the same model? Toy logistic regression, minibatch SGD, seeded shuffle.
def make_data():
    g = np.random.default_rng(0)
    X = g.normal(size=(400, 5)); y = (X @ np.array([1, -2, 0.5, 0, 1.5]) + g.normal(size=400) > 0) * 1.0
    return X, y

def train(steps, state=None, stop_at=None, save_rng=True):
    X, y = make_data()
    if state is None:
        w = np.zeros(5); v = np.zeros(5); step = 0; rng = np.random.default_rng(42)
    else:
        w, v, step = state["w"].copy(), state["v"].copy(), state["step"]
        rng = np.random.default_rng(42) if not save_rng else np.random.default_rng()
        if save_rng: rng.bit_generator.state = state["rng"]
    while step < steps:
        idx = rng.choice(len(X), 32, replace=False)
        p = 1 / (1 + np.exp(-X[idx] @ w)); grad = X[idx].T @ (p - y[idx]) / 32
        v = 0.9 * v + grad; w = w - 0.1 * v; step += 1      # momentum = optimizer state
        if stop_at is not None and step == stop_at:
            return {"w": w, "v": v, "step": step, "rng": rng.bit_generator.state}
    return {"w": w, "v": v, "step": step, "rng": rng.bit_generator.state}

full = train(200)
ck = train(200, stop_at=120)                         # preempted: checkpoint at step 120
resumed = train(200, state=ck)                       # weights + momentum + rng + step restored
no_rng = train(200, state=ck, save_rng=False)        # forgot the RNG state
no_mom = dict(ck); no_mom["v"] = np.zeros(5)         # forgot the optimizer state
no_mom = train(200, state=no_mom)
print("resume exact:", np.array_equal(full["w"], resumed["w"]))
print("without rng state exact:", np.array_equal(full["w"], no_rng["w"]))
print("without optimizer state exact:", np.array_equal(full["w"], no_mom["w"]))
assert np.array_equal(full["w"], resumed["w"])
assert not np.array_equal(full["w"], no_rng["w"]) and not np.array_equal(full["w"], no_mom["w"])
```

**Output (my run):**
```text
expected lost work 6.0 h | worst case 12.0 h
expected total compute 26.0 h | worst 32.0 h
simulated mean loss per preemption 1.499 max 3.0
Young interval (h): 0.71 = 42 min
interval  3.00 h -> overhead  6.33 h
interval  1.00 h -> overhead  3.00 h
interval  0.71 h -> overhead  2.83 h
interval  0.25 h -> overhead  4.50 h
resume exact: True
without rng state exact: False
without optimizer state exact: False
```

**Follow-ups:**
- What if the data loader cannot be resumed? Save a seed and the number of batches consumed, or accept a small replay of data and say the run is not bit-exact.
- Cross-reference: Book 4 Part 2 Q27 covers training on spot instances with checkpoints in containers.

**Common mistakes:** Saving only weights. Using the average loss as the worst case. Forgetting restart time. Writing the checkpoint in place. Never testing resume.

### Q41 ⭐ 🟡 After a base-image refresh, 14 of the 60 models (23% of them) fail to load because they were pickled under an older library version, and nobody has the original training code environment for 5 of the 14. How do you recover service quickly, how do you handle the 5, and what artifact format and image policy would you use from now on?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to dependency pinning and model serialization in MLOps guides; related topics appear in public MLOps guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** 14 of 60 models (23.3%) fail to load, so first I roll the serving base image back to the previous digest to restore service in minutes, then I use the old image to export the 14 to a portable format and prove each export matches recorded predictions, and the 5 without a training environment are not special as long as the old image still loads them.

**Clarifying questions:**
- Is the previous image digest still in the registry and can the 14 be served from it? If yes, recovery is a rollback, not a rebuild.
- How many of the 14 are revenue-critical and is there a fallback for each? That sets the order of work.
- Do we have golden inputs and expected outputs per model (recorded at release)? Without them I cannot prove an export is equal.
- For the 5, is the training data and code reference (git SHA, data version) in the registry or run log? That decides retrain versus rescue.
- Who approved the image refresh and was there a load test? The answer shapes the process fix, not blame.

**Approach:**
1. First 15 minutes: stop the damage. Roll the serving image back to the previous digest (not the `latest` tag) for the 14, or route them to the old deployment. Confirm load and a golden-prediction check. Tell consumers what degraded in the meantime.
2. First 15 minutes (decision): if the old image is gone too, escalate: fall back to the previous model version or the rules fallback for those 14 and start the rescue below.
3. First day, the 9 with a known environment: rebuild the old environment, load, export, run golden-prediction parity (my toy export matches to 0.0 maximum difference), then serve the exported artifact on the new image.
4. First day, the 5 without a known environment: do not guess library versions. (a) Load them in the old image if it exists; the pickle only needs the library it was written with. (b) If the version is recoverable from artifact metadata or logs, rebuild it (editor knowledge: some libraries store their version inside the pickle; check yours). (c) Otherwise treat each as lost, keep the previous model version serving, and retrain from the recorded data and code, or rebuild from the last prediction logs as a stopgap.
5. Safety: only load pickles you trust. Loading a pickle can execute code (my demo shows a function running during load).
6. Next quarter: a portable artifact format per model type (editor knowledge: ONNX, safetensors or the library's native text/JSON format; see Book 4 Part 6 Q9), a lockfile and a model-card field for the training environment (Book 4 Part 1 Q5 and Q11), base images pinned by digest, and a CI job that loads every registered model and checks golden predictions before any base-image change ships.
7. Rollback and escalation criteria: roll back the image if more than 5% of models fail the load check in staging or any critical model fails; escalate to the model owners if a model has no reproducible environment after a day.
8. Blameless angle: a refresh without a compatibility test is a process gap. The postmortem asks why "can every registered model still load" was never a pipeline check, and why 5 models had no recorded environment.

**Metrics:**
- Load success rate = models loading and passing the golden check divided by registered models (46 of 60 = 76.7% now, target 100% before any refresh).
- Parity = maximum absolute difference between old and new predictions on golden inputs (0 or within a stated tolerance).
- Time to restore service for the 14, and share of models with a recorded environment (at least 5 of 60 have none; audit the other 55).

**Risks:**
- Exporting can change numerics slightly (different kernels); set a tolerance per model in advance.
- The fallback or the old model may be worse; check its quality and note the date.
- A rollback keeps old vulnerabilities in the image; time-box it.
- Not every model type exports cleanly to a portable format.

**What the interviewer scores:**
- Strong: rollback first, then rescue; golden-prediction parity as the proof; warns about pickle trust.
- Strong: separates the 9 from the 5 and says the old image may already solve the 5.
- Strong: forward policy (portable format, pinned digests, load test in CI) and a blameless angle.
- Weak: "retrain everything" or "pin the library versions" with no recovery plan.

**Example:** Illustrative. 60 models, 14 fail.
- Weak: "I would rebuild the image with the old library versions and hope it loads."
- Strong: "First I roll the base image back to the previous digest, so service is back in minutes. Then in the old image I export the 14 and compare predictions to recorded golden outputs. For the five with no training environment, the old image may load them anyway; if not, I serve the previous version and retrain. Going forward we ship portable formats, pin images by digest and run a load-every-model check in CI. The postmortem asks why that check did not exist."

**Code:**
```python
# Q41: 14 of 60 pickled models fail to load after an image refresh (invented numbers)
import importlib, os, pickle, sys, tempfile
import numpy as np

total, bad, no_env = 60, 14, 5
print("failing share of fleet:", round(bad / total, 3), "| still loading:", total - bad,
      "| failing but env known:", bad - no_env)
assert round(bad / total, 3) == 0.233 and total - bad == 46 and bad - no_env == 9

d = tempfile.mkdtemp()
sys.path.insert(0, d)

# 'Old library' that the model was pickled under.
open(os.path.join(d, "toylib.py"), "w").write(
    "import numpy as np\n"
    "class LinearScorer:\n"
    "    def __init__(self, w, b): self.w = np.asarray(w); self.b = b\n"
    "    def predict(self, X): return X @ self.w + self.b\n")
import toylib
model = toylib.LinearScorer([0.5, -1.0, 2.0], 0.1)
blob = pickle.dumps(model)
X = np.random.default_rng(1).normal(size=(5, 3))
golden = model.predict(X)                       # golden inputs and outputs recorded at release time

# The 'refreshed image': the class was renamed in the new library version.
open(os.path.join(d, "toylib.py"), "w").write(
    "import numpy as np\n"
    "class Estimator:\n"
    "    def __init__(self, coef, intercept): self.coef = np.asarray(coef); self.intercept = intercept\n"
    "    def predict(self, X): return X @ self.coef + self.intercept\n")
del sys.modules["toylib"]; importlib.invalidate_caches()
try:
    pickle.loads(blob)
    failed = False
except Exception as e:
    failed = True; print("load under new library fails with:", type(e).__name__)
assert failed

# Recovery 1: roll the base image back (previous digest) -> same code path as release time.
open(os.path.join(d, "toylib.py"), "w").write(
    "import numpy as np\n"
    "class LinearScorer:\n"
    "    def __init__(self, w, b): self.w = np.asarray(w); self.b = b\n"
    "    def predict(self, X): return X @ self.w + self.b\n")
del sys.modules["toylib"]; importlib.invalidate_caches()
loaded = pickle.loads(blob)                      # trusted artifact only: pickle can run code
assert np.array_equal(loaded.predict(X), golden)
print("old image loads it; predictions equal golden:", True)

# Recovery 2 (inside the old image): export to a plain format with no library classes.
npz = os.path.join(d, "model.npz")
np.savez(npz, w=loaded.w, b=np.array(loaded.b), schema_version=np.array(1))
z = np.load(npz)                                 # allow_pickle is False by default
new_pred = X @ z["w"] + float(z["b"])
parity = float(np.abs(new_pred - golden).max())
print("exported weights parity (max abs diff):", parity)
assert parity < 1e-12

# Pickle can execute code on load: show it harmlessly.
ran = []
def side_effect(msg): ran.append(msg)
class Evil:
    def __reduce__(self): return (side_effect, ("code ran during load",))
pickle.loads(pickle.dumps(Evil()))
print("pickle.loads executed code:", ran == ["code ran during load"])
assert ran == ["code ran during load"]
```

**Output (my run):**
```text
failing share of fleet: 0.233 | still loading: 46 | failing but env known: 9
load under new library fails with: AttributeError
old image loads it; predictions equal golden: True
exported weights parity (max abs diff): 0.0
pickle.loads executed code: True
```

**Follow-ups:**
- Is ONNX always the answer? No. It suits many model types, not all; a library-native format with a version field is acceptable if you pin it. I label specific format claims as editor knowledge.
- How do you stop it recurring? A nightly job that loads all registered models in the candidate image and compares golden predictions.

**Common mistakes:** Rebuilding with guessed versions. Using the `latest` tag. Treating a successful load as a correct model. Loading untrusted pickles. Blaming whoever refreshed the image.

### Q42 ⭐ 🔴 A rules-based fallback for a credit model was written 14 months ago and never exercised in production. When the model service failed last week the fallback itself returned errors for 100% of calls because a config key had been renamed. How do you test and maintain a fallback, and how would you introduce game days without causing an outage?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to fallbacks and game days in reliability engineering; related topics appear in public MLOps guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** A fallback you have never run is a hope, not a control: it sat dormant for 14 months (about 420 days) and failed on 100% of calls the first time it was needed, so I test it in CI against the real config, probe it continuously in production, and run staged game days with an abort rule agreed in advance.

**Clarifying questions:**
- What does the fallback have to decide (approve, refer to a human, decline) and who signed off that policy? For a credit model the policy and compliance owner matter more than the code.
- Fail open or fail closed when both the model and the rules fail? It must be written down, not decided at 2 a.m.
- Who owns the fallback and its config? Nobody owning it is why the key rename went unnoticed.
- Can the fallback run in shadow on live traffic without making decisions? Shadow is the safe way to exercise it.
- What is the volume and the cost of a wrong decision during a game day? It sets the blast radius I accept.

**Approach:**
1. First 15 minutes (the incident just happened): make a human-refer path or a hard stop policy the interim decision (whichever the policy owner pre-approved), restore the key, and verify with one real test call. If a rollback of the config change fixes it, do that first; it is the shortest path.
2. First 15 minutes (escalation): the incident commander escalates to the credit-risk owner because decisions are being made without the usual control; log every decision made in the window for review.
3. First day: add a contract test that loads the real production config (not a hand-written fixture) and fails if a required key is missing. In my code a stale fixture passed while the contract test caught the missing key. Make the fallback read config through one validated loader that fails at start-up, loudly.
4. First day: add a synthetic probe that calls the fallback path every few minutes with a known input and checks the answer, and an alert on any error.
5. Next quarter: a game-day programme with staged blast radius: staging at 100%, then production shadow (fallback runs, its decisions are discarded and compared), then a small canary only if policy allows, then a larger off-peak slice. Define abort criteria before each stage (for example an error rate above 2% or any wrong-direction decision) and a named person with the stop button.
6. Next quarter: review the fallback whenever its config or the model's interface changes; a quarterly exercise with a short report.
7. Blameless angle: the person who renamed the key did what the code allowed. Ask why a config rename had no check, why a control with no test was counted as protection, and why no one had run it in 14 months.

**Metrics:**
- Fallback health = successful probe calls divided by probe calls (target 100%; any failure pages).
- Fallback agreement in shadow = fallback decisions equal to the model's (or to a reference) divided by compared calls; it shows how different the fallback is, not whether it is right.
- Time since last successful exercise (days); guardrail: alert if more than 90 days (editor judgement).
- Error rate during game day against the preset abort limit.

**Risks:**
- A game day on live credit decisions can harm real customers; use shadow first and keep slices small.
- The fallback can pass its tests and still be a worse or biased decision rule; it needs a model-risk review.
- Shadow traffic can differ from production if it skips real dependencies.
- A probe tests the path, not the quality of decisions.

**What the interviewer scores:**
- Strong: real-config contract test, continuous probe, staged blast radius with abort criteria and an owner.
- Strong: says what the fallback decides is a policy decision with a fail-open or fail-closed rule.
- Strong: gives the incident order and a blameless action item.
- Weak: "write more unit tests" only; "run a game day in production on Friday".

**Example:** Illustrative. A threshold key renamed from `rule_threshold` to `rules.score_cutoff`.
- Weak: "We should have tested it more, I would ask the developer to be more careful."
- Strong: "I would make sure applicants are routed to manual review now, restore the key, and log the affected window. Then a contract test that loads the real config, a probe every five minutes, and a shadow run of the fallback on live traffic. Game days go in stages with an abort rule set beforehand. The postmortem asks why a control nobody ran counted as safety."

**Code:**
```python
# Q42: a rules fallback never exercised; a renamed config key made it fail 100% (invented example)
import json, random

# Production config AFTER someone renamed 'rule_threshold' -> 'rules.score_cutoff'
prod_config = {"rules": {"score_cutoff": 620}, "model_url": "svc://credit"}
# The fallback was written against the old name
REQUIRED_KEYS = ["rule_threshold"]

def fallback_decide(app, cfg):
    return "approve" if app["bureau_score"] >= cfg["rule_threshold"] else "refer"

# 1) Unit test with a hand-written fixture passes: false comfort
stale_fixture = {"rule_threshold": 620}
assert fallback_decide({"bureau_score": 700}, stale_fixture) == "approve"

# 2) A contract test that loads the REAL config fails at deploy time, not 14 months later
def contract_test(cfg, required):
    return [k for k in required if k not in cfg]
missing = contract_test(prod_config, REQUIRED_KEYS)
print("contract test, missing keys:", missing)
assert missing == ["rule_threshold"]

# 3) Without any exercise, every call fails: show 100% errors and who notices
errors = 0
for i in range(1000):
    try:
        fallback_decide({"bureau_score": 600 + i % 200}, prod_config)
    except KeyError:
        errors += 1
print("fallback errors on 1000 calls:", errors, "= 100%")
assert errors == 1000

# 4) Detection delay: dormant 14 months vs a synthetic probe every 5 minutes vs 1% live traffic
months_dormant_days = 14 * 30
probe_min = 5
rps, share = 200, 0.01
print("days undetected:", months_dormant_days, "| probe detects within", probe_min, "min")
print("1% live canary of the fallback path:", rps * share, "calls/s -> one call every",
      round(1 / (rps * share), 1), "s on average, so a broken path shows up in seconds")
assert months_dormant_days == 420 and rps * share == 2.0 and round(1 / (rps * share), 1) == 0.5

# 5) Fix: fallback reads config through one validated loader with a schema; test against real file
def load_fallback_cfg(cfg):
    cut = cfg.get("rules", {}).get("score_cutoff")
    if not isinstance(cut, int):
        raise ValueError("fallback config invalid: rules.score_cutoff")
    return {"cutoff": cut}
def fallback_decide_v2(app, fcfg):
    return "approve" if app["bureau_score"] >= fcfg["cutoff"] else "refer"
fcfg = load_fallback_cfg(prod_config)
assert fallback_decide_v2({"bureau_score": 700}, fcfg) == "approve"
try:
    load_fallback_cfg({"rules": {}}); raise SystemExit("should have failed")
except ValueError as e:
    print("loader fails loudly at start-up:", e)

# 6) Game-day gate: staged blast radius, abort rule decided before starting
stages = [("staging, 100%", 1.0), ("prod shadow, 0% decisions", 0.0), ("prod canary 1%", 0.01), ("prod 10% off-peak", 0.10)]
abort_error_rate = 0.02
def stage_ok(observed_error_rate): return observed_error_rate <= abort_error_rate
print("abort if error rate above", abort_error_rate, "->", [stage_ok(x) for x in (0.0, 0.01, 0.05)])
assert [stage_ok(x) for x in (0.0, 0.01, 0.05)] == [True, True, False]
print("stages:", [s for s, _ in stages])
```

**Output (my run):**
```text
contract test, missing keys: ['rule_threshold']
fallback errors on 1000 calls: 1000 = 100%
days undetected: 420 | probe detects within 5 min
1% live canary of the fallback path: 2.0 calls/s -> one call every 0.5 s on average, so a broken path shows up in seconds
loader fails loudly at start-up: fallback config invalid: rules.score_cutoff
abort if error rate above 0.02 -> [True, True, False]
stages: ['staging, 100%', 'prod shadow, 0% decisions', 'prod canary 1%', 'prod 10% off-peak']
```

**Follow-ups:**
- Why not just a canary in production? For credit decisions a canary changes real outcomes, so shadow first, then a small slice only with sign-off.
- How often? After any change to the fallback, its config or the model interface, plus a calendar exercise; the right cadence depends on risk and is a judgement.
- Cross-reference: Book 4 Part 6 Q17 covers a real-time scoring service design with fallbacks.

**Common mistakes:** Testing against a hand-written fixture. No owner. Unscheduled production tests with no abort rule. Treating the fallback as policy-neutral. Blaming the person who renamed the key.

### Q43 ⭐ 🔴 A regulator asks you to reproduce the exact training data of model v9, which went live 11 months ago, but the training table is overwritten in place every night and only the SQL is in git. What can you recover, what do you tell the regulator and what data-versioning design would have made this a one-hour task?
**Asked at:** Leakage and reproducibility material (arXiv 2207.07048 and 2311.04179 on leakage, an Omdena post on silent ML failures and label timing, an arXiv 2025 paper on reproducible ML infrastructure); research and practitioner pages rather than an interview bank; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** I tell the regulator the truth: the exact training table is gone, but I can rebuild an as-of approximation from append-only raw sources with a verified match to what the model artifact and logs show, and I put a snapshot-plus-manifest design in place so the next request is a one-hour job.

**Clarifying questions:**
- What exactly is asked: the exact rows, or evidence that the model was trained on legitimate, documented data? The answer changes what counts as sufficient (check with the compliance and legal teams; I do not assume the regulator's rules).
- Is the raw source (events, application logs, upstream tables) append-only and does it keep load time? That is what lets me reconstruct as-of.
- What was kept for v9: the model artifact, the git SHA of the SQL, training metrics, feature statistics, prediction logs? Each is corroborating evidence.
- What is the retention policy and deadline? It sets how fast and how formally I respond.
- Are there other live models in the same position? The gap is probably not unique to v9.

**Approach:**
1. First 15 minutes (this is a compliance incident, not only an engineering task): tell the compliance lead and open a tracked record; freeze deletion of anything that could help (raw logs, backups) while we assess. Do not run the nightly job's overwrite on anything we might need.
2. First 15 minutes (escalation criteria): escalate to the head of risk and legal the same day if the regulator's deadline is shorter than our recovery estimate, or if the raw sources have already been purged.
3. First day: inventory what exists: the v9 artifact and its recorded metadata, the SQL at the v9 git SHA, backups or warehouse history within retention (editor knowledge: availability and length depend on the platform and settings; check yours), raw append-only sources with load time, prediction logs, and training metrics.
4. First day: reconstruct as-of: run the recorded SQL against raw sources with both event time and load time cut at the v9 training date. In my toy example the naive re-run today gives a different digest because a late event arrived (4 rows versus 3), while the as-of run matches the v9 digest exactly, but only because load time was kept.
5. First day: corroborate: compare row counts, feature distributions and the model's metrics to those recorded at release; report mismatches openly.
6. What I tell the regulator: what we can prove (artifact, code version, as-of reconstruction and how closely it matches, controls since), what we cannot (bit-exact rows, if so), why, and the fix with a date. I do not claim an exact reproduction I cannot show, and I do not blame a person.
7. Next quarter: an immutable snapshot (or table version) per training run, written once, plus a manifest linking model version, snapshot ID, SQL git SHA, row count and content digest; reproduction becomes "read the manifest, verify the digest". Snapshot per training run (11 in 11 months at one retrain a month) is far cheaper than a snapshot per night (330). See Book 4 Part 1 Q5 for the run-record list.
8. Blameless angle: overwriting a table was a design default, not a person's mistake. The postmortem asks why a regulated model could ship without a data-versioning requirement, and the action item is a release gate that refuses a model without a manifest.

**Metrics:**
- Reproduction match = rows in the reconstructed set with the same content hash divided by rows recorded in the manifest (not available for v9, so report row-count and distribution agreement instead).
- Time to reproduce = hours from request to verified dataset (target: 1 hour).
- Coverage = share of live models with a manifest and an immutable snapshot (target 100%).

**Risks:**
- An as-of reconstruction can look right and still differ: late corrections, deletions on request, or upstream changes after the date.
- Overstating certainty to the regulator is worse than admitting a gap.
- Snapshots that contain personal data need access control and a retention rule (check the company's policy).
- Legal and regulatory judgements are not mine to give; I hand them to compliance.

**What the interviewer scores:**
- Strong: separates what is recoverable from what is not, and communicates the gap honestly and early.
- Strong: names append-only raw data with load time, a manifest and an immutable snapshot per run.
- Strong: involves compliance and legal and does not state regulations from memory.
- Weak: "just re-run the SQL" (it changes with late data) or promising an exact reproduction.

**Example:** Illustrative. Six raw events, one arrives two days late.
- Weak: "I will re-run the SQL from git and send it; it should be the same."
- Strong: "I cannot promise the exact table. I can reconstruct as-of from the raw events using load time, and I will show how closely it matches the metrics and row counts we recorded. I will say plainly what we cannot prove. Going forward every training run writes an immutable snapshot and a manifest with a content hash, so this becomes a one-hour check."

**Code:**
```python
# Q43: reproduce training data of model v9 (11 months ago) when the table is overwritten nightly
import hashlib, sqlite3

def digest(rows):
    h = hashlib.sha256()
    for r in sorted(rows):
        h.update(repr(r).encode())
    return h.hexdigest()[:12]

db = sqlite3.connect(":memory:")
db.execute("create table events (id int, cust int, amount real, event_day int, loaded_day int)")
# append-only raw events; some arrive late (loaded_day > event_day) and one is corrected later
raw = [(1, 10, 50.0, 1, 1), (2, 11, 20.0, 1, 1), (3, 10, 70.0, 2, 2), (4, 12, 10.0, 2, 4),   # id 4 arrives 2 days late
       (5, 11, 30.0, 3, 3), (6, 13, 90.0, 3, 3)]
db.executemany("insert into events values (?,?,?,?,?)", raw)

SQL = "select cust, sum(amount) from events where event_day<=? and loaded_day<=? group by cust"
TRAIN_DAY = 3

# Day 3: training run reads the table that is overwritten nightly (the problem)
train_rows = db.execute(SQL, (TRAIN_DAY, TRAIN_DAY)).fetchall()
v9_digest = digest(train_rows)
print("v9 training rows:", len(train_rows), "digest:", v9_digest)

# Today (day 400): only the SQL is in git. Re-run it with 'now' as the cutoff
rows_now = db.execute(SQL, (TRAIN_DAY, 400)).fetchall()
print("re-run with today's data: rows", len(rows_now), "digest", digest(rows_now), "| matches v9:", digest(rows_now) == v9_digest)
assert digest(rows_now) != v9_digest        # the late event changes the answer

# What CAN be recovered: if raw events are append-only and carry load time, filter by load time too
rows_asof = db.execute(SQL, (TRAIN_DAY, TRAIN_DAY)).fetchall()
print("as-of reconstruction (event_day and loaded_day <= 3): digest", digest(rows_asof), "| matches v9:", digest(rows_asof) == v9_digest)
assert digest(rows_asof) == v9_digest       # only possible because loaded_day was kept

# What would have made it a one-hour task: manifest tying model version to an immutable snapshot
db.execute("create table snapshot_9 as select * from events where loaded_day <= 3")   # written once, never updated
manifest = {"model": "v9", "snapshot": "snapshot_9", "sql_git_sha": "abc1234 (invented)",
            "row_count": len(train_rows), "digest": v9_digest}
snap_rows = db.execute("select cust, sum(amount) from snapshot_9 where event_day<=3 group by cust").fetchall()
check = digest(snap_rows) == manifest["digest"] and len(snap_rows) == manifest["row_count"]
print("manifest check from snapshot:", check)
assert check

# Cost of snapshotting every night vs only per training run (invented sizes)
nights = 11 * 30
per_run = 11        # e.g. one retrain a month (invented)
print("nightly snapshots over 11 months:", nights, "| per-run snapshots:", per_run)
assert nights == 330 and per_run == 11
```

**Output (my run):**
```text
v9 training rows: 3 digest: 2a49e45a66bf
re-run with today's data: rows 4 digest fc58d2848e50 | matches v9: False
as-of reconstruction (event_day and loaded_day <= 3): digest 2a49e45a66bf | matches v9: True
manifest check from snapshot: True
nightly snapshots over 11 months: 330 | per-run snapshots: 11
```

**Follow-ups:**
- Why not keep every nightly table? It is possible but costly and noisy; a snapshot per training run captures what the model actually used.
- What if personal data must be deleted on request? Then the snapshot policy and the reproduction promise need to say so; ask the privacy owner.
- Cross-reference: Book 4 Part 1 Q5 (reproducible training records).

**Common mistakes:** Re-running SQL on today's data and calling it the same. Hiding the gap. Quoting regulations without checking. Snapshotting nightly without a purpose. Forgetting to record the SQL commit and a content hash.

### Q44 ⭐ 🔴 A feature view was changed to version 2 by the producer team, and 3 of its 7 consumer models read the new schema while 4 still read version 1. After the change the 3 models are fine but a bug appears in the producer, and rolling the producer back would break those 3. How do you decide the rollback order, and what versioning and deprecation process prevents this deadlock?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to feature-store schema versioning and rollback; related topics appear in public MLOps guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Rollback order is the reverse of deploy order, consumers first and producer last: 3 of 7 consumers read v2, so rolling the producer back alone would break them, and the lasting fix is to publish new feature-view versions side by side, change schemas additively in place, and retire an old version only after every consumer has moved.

**Clarifying questions:**
- Where is the producer bug: only in v2 output, or also in what the 4 v1 consumers read? That decides whether the 4 are part of the incident.
- Is v1 still being published (dual write) or has the producer replaced it? If v1 is still there, repointing consumers is possible.
- Do the 3 v2 consumers have a previous model version, trained on v1, in the registry? Without it there is nothing to roll back to.
- How much revenue or traffic do the 3 carry (illustratively 45%)? It sets the severity and the tolerable wait.
- How long would a forward fix take? If it is hours, fix forward is usually safer than a staged rollback.

**Approach:**
1. First 15 minutes: do not roll the producer back alone. Declare the incident, assign an incident commander, and measure the blast radius: which models read the buggy field, and how wrong are they. Turn on a manual override or fallback for the worst-affected decisions if there is one.
2. First 15 minutes (the decision rule): if the fix is small and fast (within the hours we can tolerate), fix forward as v2.1 and leave the v1 readers alone. If the fix is slow and v1 is still published and prior models exist, roll back consumers first (their model and view back to v1), then the producer. If neither is available, mitigate and fix forward; I never promise a rollback that breaks more than it fixes.
3. Rollback order logic: deployment goes producer then consumers, so rollback goes consumers then producer. In my code the topological order gives deploy producer, A, B, C and rollback C, B, A, producer.
4. First day: verify each step with golden feature values and a model-score comparison before and after, and keep the v1 readers untouched as a control group. Write the timeline while it is fresh.
5. Next quarter: a versioning contract. Additive changes (new columns) are allowed in place; any removal, rename or type change is a new view version published side by side with the old one; a compatibility check in CI classifies each schema diff (in my code v1 to v2 is flagged breaking because `n_orders` was removed or renamed); a deprecation window with named owners and a date; a consumer registry so you can see who reads what; the old version is retired only when no consumer reads it.
6. Rollback and escalation criteria: roll back only when the bug is worse than the rollback risk and the consumer-first path is verified; escalate to the owning managers of the 3 consumers if their sign-off is needed for the model rollback; escalate to the incident commander if the bug also affects the 4 v1 consumers.
7. Blameless angle: the producer team followed a process that had no deprecation rule and no consumer map. The postmortem asks why a breaking change shipped as an in-place update and why no one could list the consumers in a minute.

**Metrics:**
- Consumers on the latest version = consumers reading v2 divided by all consumers (3 of 7 = 42.9%); retirement allowed only at 100%.
- Revenue exposed = revenue share of models reading the buggy field (45% in the invented example).
- Schema-compatibility violations caught in CI divided by breaking changes proposed.
- Time to identify all consumers of a view (target: minutes, from the registry).

**Risks:**
- A rollback of the producer is unsafe for readers that already depend on the new schema.
- Prior model versions may have been trained on features that no longer exist exactly as before; test them.
- Side-by-side versions double compute and storage and can diverge in meaning; keep deprecation dates short and enforced.
- The 4 v1 consumers are not automatically safe if both versions share a pipeline stage.

**What the interviewer scores:**
- Strong: reverse-order rollback, asks where the bug lives, and prefers fix forward when it is fast.
- Strong: names additive-in-place versus new-version-side-by-side, a compatibility check, a consumer map and a deprecation window.
- Strong: blameless action items about process, with an owner and a date.
- Weak: "just roll back the producer" or "tell the three teams to fix their models".

**Example:** Illustrative. 7 consumers, 3 on v2 with 45% of revenue.
- Weak: "Roll back the producer to v1; the three teams can sort it out."
- Strong: "That rollback would break three models that carry about 45% of revenue. I would ask where the bug lives. If a v2.1 patch takes hours, fix forward. If not, and v1 is still published and the old models exist, repoint the consumers first and the producer last. Afterwards, breaking changes become new versions served side by side with a deprecation date, and we retire the old one only when the consumer list is empty."

**Code:**
```python
# Q44: feature view v2; 3 of 7 consumers read v2, 4 read v1; producer bug; rollback deadlock (invented)
from graphlib import TopologicalSorter

consumers = {"A": "v2", "B": "v2", "C": "v2", "D": "v1", "E": "v1", "F": "v1", "G": "v1"}
traffic = {"A": 30, "B": 10, "C": 5, "D": 25, "E": 15, "F": 10, "G": 5}   # share of revenue, invented
assert sum(traffic.values()) == 100
v2 = [m for m, v in consumers.items() if v == "v2"]
assert len(v2) == 3 and len(consumers) - len(v2) == 4
print("v2 readers:", v2, "carry", sum(traffic[m] for m in v2), "% of revenue")
assert sum(traffic[m] for m in v2) == 45

# Naive rollback: producer back to v1-only schema -> the 3 v2 readers break
broken = sum(traffic[m] for m in v2)
print("naive producer rollback breaks", broken, "% of revenue")

# Rollback order is the REVERSE of the deploy order: consumers first, then producer.
deps = {"producer v2": set(), "A": {"producer v2"}, "B": {"producer v2"}, "C": {"producer v2"}}
deploy = list(TopologicalSorter(deps).static_order())
rollback = deploy[::-1]
print("deploy order  :", deploy)
print("rollback order:", rollback)
assert deploy[0] == "producer v2" and rollback[-1] == "producer v2"

# Decision rule (a judgement, written as code so it can be reviewed): ask where the bug lives first
def choose(bug_hits_v1_readers, v1_view_still_published, prior_models_available, patch_hours, tolerable_hours=4):
    if bug_hits_v1_readers:
        return "wider incident: bug also hits v1 readers, fix forward fast and roll back only in the consumers-first order"
    if patch_hours <= tolerable_hours:
        return "fix forward: patch the producer as v2.1, leave v1 readers alone"
    if v1_view_still_published and prior_models_available:
        return "consumers first: repoint A,B,C to v1 view and prior model, then roll the producer back"
    return "no safe rollback: mitigate (manual override or fallback) and fix forward"
cases = [(False, True, True, 2), (False, True, True, 12), (False, False, True, 12), (True, True, True, 2)]
for c in cases:
    print(c, "->", choose(*c))
assert choose(*cases[0]).startswith("fix forward: patch")
assert choose(*cases[1]).startswith("consumers first")
assert choose(*cases[2]).startswith("no safe rollback")
assert choose(*cases[3]).startswith("wider incident")

# Schema compatibility check that would have stopped the deadlock (breaking vs additive)
v1s = {"user_id": "int", "spend_30d": "float", "n_orders": "int"}
v2s = {"user_id": "int", "spend_30d": "float", "orders_count": "int", "region": "str"}
def diff(old, new):
    removed = sorted(set(old) - set(new)); added = sorted(set(new) - set(old))
    retyped = sorted(k for k in set(old) & set(new) if old[k] != new[k])
    return {"removed": removed, "added": added, "retyped": retyped, "breaking": bool(removed or retyped)}
d = diff(v1s, v2s)
print("v1 -> v2:", d)
assert d == {"removed": ["n_orders"], "added": ["orders_count", "region"], "retyped": [], "breaking": True}
# additive-only change is safe to serve in place:
assert diff(v1s, {**v1s, "region": "str"})["breaking"] is False

# Deprecation timeline: serve v1 and v2 side by side until all consumers moved
migrated = {m: 0 for m in consumers}
for m in v2: migrated[m] = 1
remaining = [m for m, x in migrated.items() if not x]
print("consumers still on v1 (block v1 retirement):", remaining)
assert remaining == ["D", "E", "F", "G"]
```

**Output (my run):**
```text
v2 readers: ['A', 'B', 'C'] carry 45 % of revenue
naive producer rollback breaks 45 % of revenue
deploy order  : ['producer v2', 'A', 'B', 'C']
rollback order: ['C', 'B', 'A', 'producer v2']
(False, True, True, 2) -> fix forward: patch the producer as v2.1, leave v1 readers alone
(False, True, True, 12) -> consumers first: repoint A,B,C to v1 view and prior model, then roll the producer back
(False, False, True, 12) -> no safe rollback: mitigate (manual override or fallback) and fix forward
(True, True, True, 2) -> wider incident: bug also hits v1 readers, fix forward fast and roll back only in the consumers-first order
v1 -> v2: {'removed': ['n_orders'], 'added': ['orders_count', 'region'], 'retyped': [], 'breaking': True}
consumers still on v1 (block v1 retirement): ['D', 'E', 'F', 'G']
```

**Follow-ups:**
- How long should v1 stay? As long as any consumer reads it, with a hard date agreed up front; track consumers in a registry.
- What about the feature values themselves changing meaning without a schema change? That is skew; compare distributions, not only names and types. Book 4 Part 8 Q7 covers training-serving skew.

**Common mistakes:** Rolling the producer back first. Breaking changes shipped in place. No consumer list. Retiring v1 on a calendar date. Blaming the producer team.

### Q45 ⭐ 🔴 A model bug hits 3% of requests but those requests carry 20% of revenue, and it started 90 minutes ago. You are the incident commander with a shared on-call rota across 4 teams. How do you set the severity, who do you assign to which role, what cadence do you use for updates, and when do you decide between a fix, a rollback or a manual workaround?
**Asked at:** MLOps interview guides (startup.jobs, Hyring, kore1, refresh.cv, wecreateproblems and Yardstick pages list rollback, canary versus blue/green versus shadow, and 'tell me about an urgent production incident' prompts, and one 2026 guide says the strongest questions test custody of a live model); practitioner and prep-site material rather than a confirmed employer round; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened
**Say this first (1 line):** 3% of requests carrying 20% of revenue is about 6.7 times the average value per request, so I set severity by revenue (SEV1 on my illustrative policy), name an incident commander and role owners from the 4 teams, update every 30 minutes, and default to a verified rollback if there was a recent change, a manual workaround if I can isolate the segment, and a forward fix only when neither exists.

**Clarifying questions:**
- What changed 90 minutes ago (deploy, data, config, upstream)? A change in the window makes rollback the default.
- Is the 90 minutes the age of the bug or of our detection? If we found it late, detection is a separate postmortem topic.
- What does "bug" cost per affected request: a wrong score, no answer, a lost sale? That converts to money (in my invented example half of the affected revenue is lost).
- Can we identify the affected segment in real time? If yes, a workaround is possible.
- Is there a known-good version that is verified, and what is its quality? Rolling back to something untested is a second incident.
- Who owns the model, the data and the platform on the rota right now?

**Approach:**
1. First 15 minutes, declare and assign: I declare the incident, take incident commander (IC) myself or hand off to whoever is free, and assign: ops lead (ML on-call, hands on the fix), comms lead, scribe, and one liaison per team (data, platform, product). The IC does not debug. Write the start time, the known facts and the next update time in one channel.
2. First 15 minutes, severity: by revenue-weighted impact, not request count. 3% of requests would read as minor; 20% of revenue (about 20,000 units an hour in my invented 2.4 million a day) is SEV1 on my illustrative thresholds. Thresholds are the company's policy, not a standard.
3. First 15 minutes, decision: rollback if a deploy fell in the window, a last-good version exists and its rollback has been verified (for example against golden inputs); in my numbers it costs about 3,300 more units against 5,000 for a 30-minute workaround and 30,000 for a 3-hour forward fix.
4. First 15 minutes, otherwise: manual workaround, for example route the affected segment to a rules fallback or the previous model while the fix is written; fix forward with all hands only if neither is possible.
5. Cadence: update every 30 minutes (every 15 while no mitigation exists) with what we know, what we are doing, next update time. Silence is worse than "no change".
6. Escalation criteria: if there is no mitigation 60 minutes after declaration, or the loss rate rises, escalate to the engineering director and open a second IC for hand-off fatigue; wake the data owner if the cause may be upstream.
7. First day: confirm resolution on the revenue-weighted metric, not only an error rate; estimate impact with a clear base (affected requests, revenue and loss assumptions); decide whether to reprocess or compensate affected customers (business and legal decision). Write the postmortem draft within 2 working days.
8. Next quarter: a revenue-weighted and per-segment alert (an overall 5% alert never fires for a 3% bug; the weighted rate of 20% does), a release process with canary and automatic rollback criteria, an on-call rota with a named IC per shift across the 4 teams, and incident drills.
9. Blameless angle: the timeline lists decisions and what people knew at the time. Questions: why did 90 minutes pass, what signal existed, what made rollback slow, and which guard rail would have stopped the release. Action items have owners and dates; no names in blame.

**Metrics:**
- Revenue-weighted error rate = revenue on failed requests divided by total revenue in the window (20% here); also error rate by segment.
- Time to detect, time to mitigate and time to resolve (minutes), from the incident start, not from the page.
- Revenue lost = affected revenue per hour x loss rate x hours (illustrative; state the loss-rate assumption).
- Guardrail: rollback success (quality of the restored version on golden inputs) before declaring recovery.

**Risks:**
- Severity by request share understates the incident (SEV2 on 3% versus SEV1 on 20% of revenue).
- Rolling back to an unverified version creates a second problem.
- Too many responders and no single IC: duplicate work and conflicting changes.
- A workaround that quietly stays in place becomes permanent; give it an owner and an expiry.
- Revenue loss figures are assumptions; present them as ranges.

**What the interviewer scores:**
- Strong: revenue-weighted severity, clear roles and a cadence, a stated decision rule between rollback, workaround and fix.
- Strong: numbers (6.7 times, 20,000 an hour, option costs) with base and assumptions, and a statement of why overall alerts missed it.
- Strong: concrete first-15-minute, first-day and next-quarter actions with escalation triggers.
- Weak: "find the root cause first" while loss continues; no roles; severity from request count; naming a person as the cause.

**Example:** Illustrative. 2.4 million units a day, 3% of requests, 20% of revenue, 90 minutes old.
- Weak: "I would find the root cause and fix it, and keep everyone updated when I know more."
- Strong: "This is SEV1 by revenue: 3% of requests but 20% of revenue, around 20,000 units an hour. I am the commander, ML on-call owns the fix, one person on comms, one scribing, a liaison from each other team. If there was a deploy in the last hour and the last good version is verified I roll back now; if not I route the segment to the fallback while we fix. Updates every 30 minutes. If nothing is mitigated at 60 minutes I escalate. Afterwards we run a blameless review on why no alert fired for 90 minutes."

**Code:**
```python
# Q45: bug on 3% of requests carrying 20% of revenue, started 90 minutes ago (invented numbers)
req_share, rev_share, age_min = 0.03, 0.20, 90
value_ratio = rev_share / req_share
print("revenue per affected request vs average:", round(value_ratio, 2), "x")
assert round(value_ratio, 2) == 6.67

# Money at stake (illustrative revenue: 2,400,000 units per day, flat across the day)
rev_per_day = 2_400_000
rev_per_min = rev_per_day / (24 * 60)
at_risk_per_hour = rev_per_min * 60 * rev_share
print("revenue/hour:", rev_per_min * 60, "| carried by affected requests/hour:", at_risk_per_hour)
assert rev_per_min * 60 == 100_000 and at_risk_per_hour == 20_000
loss_frac = 0.5                    # assume half of the affected revenue is actually lost (invented)
lost_so_far = at_risk_per_hour * (age_min / 60) * loss_frac
print("lost so far at 50% loss rate:", lost_so_far)
assert lost_so_far == 15_000

# Why nobody noticed for 90 minutes: an overall alert on error rate misses a 3% slice
overall_alert = 0.05                   # alert at 5% overall error rate
print("overall error rate from the bug:", req_share, "-> alert fires:", req_share >= overall_alert)
assert not (req_share >= overall_alert)
rev_weighted_alert = 0.05              # same threshold on a revenue-weighted error rate
print("revenue-weighted error rate:", rev_share, "-> alert fires:", rev_share >= rev_weighted_alert)
assert rev_share >= rev_weighted_alert
# detection delay if checked every 5 min on the weighted metric, with a 3-point window: <= 10 min
check_min, consecutive = 5, 2
print("detection delay: hourly dashboard up to 60 min vs 5-min check needing", consecutive, "breaches =", check_min * consecutive, "min")
assert check_min * consecutive == 10

# Option cost, remaining loss at the same 50% loss rate (invented ETAs)
per_min = at_risk_per_hour * loss_frac / 60
options = {"rollback (verified last good)": 20, "manual workaround (route segment to rules)": 30,
           "forward fix (code, test, deploy)": 180}
for name, eta in options.items():
    print(f"{name:45} ETA {eta:3} min  extra loss {per_min * eta:8.0f}")
assert round(per_min * 20) == 3333 and round(per_min * 180) == 30000
assert per_min * 20 < per_min * 30 < per_min * 180

# Decision rule written as code
def decide(deploy_in_window, last_good_exists, rollback_verified, segment_identifiable):
    if deploy_in_window and last_good_exists and rollback_verified:
        return "rollback"
    if segment_identifiable:
        return "manual workaround, then fix forward"
    return "fix forward with all hands; escalate"
assert decide(True, True, True, True) == "rollback"
assert decide(True, True, False, True) == "manual workaround, then fix forward"
assert decide(False, False, False, False).startswith("fix forward")
print("decisions:", decide(True, True, True, True), "|", decide(True, True, False, True))

# Severity by revenue-weighted impact (the thresholds are an illustrative policy, not a standard)
def sev(rev_share_hit):
    return "SEV1" if rev_share_hit >= 0.10 else "SEV2" if rev_share_hit >= 0.02 else "SEV3"
print("severity:", sev(rev_share), "(by revenue) vs", sev(req_share), "(by request share)")
assert sev(rev_share) == "SEV1" and sev(req_share) == "SEV2"

# Update cadence and who runs what (4 teams on one rota)
roles = {"incident commander": "rota A", "ops lead (does the fix/rollback)": "ML on-call",
         "comms lead": "rota B", "scribe": "rota C", "liaison, data/platform": "rota D"}
assert len(roles) == 5
print("update every 30 min; escalate to executive if no mitigation by", 60, "min after declaring")
```

**Output (my run):**
```text
revenue per affected request vs average: 6.67 x
revenue/hour: 100000.0 | carried by affected requests/hour: 20000.0
lost so far at 50% loss rate: 15000.0
overall error rate from the bug: 0.03 -> alert fires: False
revenue-weighted error rate: 0.2 -> alert fires: True
detection delay: hourly dashboard up to 60 min vs 5-min check needing 2 breaches = 10 min
rollback (verified last good)                 ETA  20 min  extra loss     3333
manual workaround (route segment to rules)    ETA  30 min  extra loss     5000
forward fix (code, test, deploy)              ETA 180 min  extra loss    30000
decisions: rollback | manual workaround, then fix forward
severity: SEV1 (by revenue) vs SEV2 (by request share)
update every 30 min; escalate to executive if no mitigation by 60 min after declaring
```

**Follow-ups:**
- What if rollback is not possible? Workaround first, because forward fixes take hours; keep the workaround time-boxed and tracked.
- Who decides to compensate customers? The business and legal owners, with our impact estimate and its assumptions.
- Cross-reference: Book 4 Part 7 Q12 (roll back a bad model release) and Book 4 Part 8 Q27 (runbooks and on-call for model alerts).

**Common mistakes:** Debugging as the commander. Severity from request count. Rolling back to an unverified version. No update cadence. Presenting loss estimates as facts. Blaming the person who shipped it.

