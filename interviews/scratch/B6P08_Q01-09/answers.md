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
