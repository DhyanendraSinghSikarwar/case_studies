# Question data for Book 6 Part 8. Tuple: (stars, difficulty, scenario text, asked-key). All numbers are invented illustrative numbers.
import math
NS = "; commonly reported in public guides for ML engineer, MLOps and data scientist loops; search snippets only, not opened"
AS = {
 'T': "MLOps interview guides (startup.jobs, Hyring, kore1, refresh.cv, wecreateproblems and Yardstick pages list rollback, canary versus blue/green versus shadow, and 'tell me about an urgent production incident' prompts, and one 2026 guide says the strongest questions test custody of a live model); practitioner and prep-site material rather than a confirmed employer round" + NS,
 'S': "Feature-store and skew material (techinterview.org pages on point-in-time joins, drift and feature stores and MLOps pipelines, DesignGurus and barkingiguana pages on training-serving skew; one snippet gives a mean-imputation versus zero-fill skew incident as a template); prep and course material rather than a documented real incident" + NS,
 'D': "Data-pipeline pages (luminousmen on avoidable backfills and non-idempotent jobs, DZone on silent upstream schema change, HackerNoon and Seattle Data Guy on silent pipeline failures, DataExpert on schema drift and idempotent replays, DataVidhya on measuring detection latency in postmortems); practitioner blogs rather than an interview bank" + NS,
 'A': "Alerting and drift-monitor material (an ICLR 2026 listing on false-alarm rates of drift detectors, an MLflow alerts playbook, GeoSurge, LeadDev and Rootly pages on thresholds, monitoring debt and alert fatigue); research and practitioner pages rather than an interview bank" + NS,
 'L': "LLM-serving resilience pages (getmaxim, TrueFoundry, tianpan and Statsig pages on retries, 429 handling, fallbacks, circuit breakers and cost during failover; one snippet notes that silent quality degradation is invisible to HTTP success rates); practitioner material, no confirmed interview bank" + NS,
 'R': "Model-registry and rollback pages (oneuptime and mljar rollback runbooks that move a 'champion' alias or demote a Production stage, a Towards AI piece on registries as the source of truth); secondary practitioner material, no located public incident" + NS,
 'G': "GPU-serving and autoscaling pages (apxml and system-design.space on autoscaling and serving architecture; vendor pages from regolo.ai and lyceum.technology on cold starts and capacity, treated as vendor claims); no public postmortem located" + NS,
 'X': "Leakage and reproducibility material (arXiv 2207.07048 and 2311.04179 on leakage, an Omdena post on silent ML failures and label timing, an arXiv 2025 paper on reproducible ML infrastructure); research and practitioner pages rather than an interview bank" + NS,
}
ED = "No public page found for this exact scenario, editor-designed; the theme is adjacent to "
def add(s, d, t, a):
    if a.startswith('ED:'):
        AS.setdefault(a, ED + a[3:] + "; related topics appear in public MLOps guides; no page for the exact framing; search snippets only, not opened")
    Q.append((s, d, t, a))
Q = []
def z2(x1, n1, x2, n2):
    p = (x1+x2)/(n1+n2); se = math.sqrt(p*(1-p)*(1/n1+1/n2)); return (x1/n1-x2/n2)/se

# ================= 3 stars =================
# 1 silent worse model
assert round(0.812-0.771, 3) == 0.041 and 5000000-4200000 == 800000 and 800000/5000000 == 0.16
add(3, '🟢', "A nightly retrain job finished green, but the new model scores an AUC of 0.771 on the fixed 20,000-row holdout against 0.812 for the production model, an absolute drop of 0.041. The job read 4,200,000 rows against a usual 5,000,000, which is 16% fewer relative to the usual count, and the deploy step is automatic whenever the job succeeds. What do you do tonight, and which gates would have stopped this?", 'T')
# 2 rollback decision, noise
z = z2(504, 12000, 516, 12000)
assert 504/12000 == 0.042 and 516/12000 == 0.043 and 240/180 > 1.33 and 240/180 < 1.34 and abs(z) < 1
add(3, '🟢', "A new model went to 100% of traffic 40 minutes ago. The 95th-percentile latency rose from 180 ms to 240 ms, which is 33% higher relative to 180 ms, and conversion over the 12,000 sessions since release is 4.2% against 4.3% for the 12,000 sessions in the same weekday hour last week (a 0.1 point absolute gap, measured samples). Do you roll back now, and what pre-agreed rollback rule would have made this a non-debate?", 'T')
# 3 on-call first minutes
assert 2000*0.71 == 1420 and 2000*0.92 == 1840 and 1840-1420 == 420
add(3, '🟢', "At 02:10 you are paged because the fraud model's approval rate in the latest 5-minute window fell from 92% to 71% (absolute, of about 2,000 requests per window, so roughly 420 fewer approvals than usual). Nothing was deployed today according to the release calendar. What do you do in the first 15 minutes, in order, and when do you wake someone else?", 'T')
# 4 alert fatigue arithmetic
chk = 24*40; fa = chk*0.05; ph = 1-0.95**40
assert chk == 960 and fa == 48 and 0.87 < ph < 0.88
add(3, '🟢', "A drift monitor runs a per-feature test on 40 features every hour at a 5% false-positive level, and the on-call engineer is paged several times a day, nearly every hour, without a real incident. Assuming independent features and no real change, compute the expected false alerts per day and the probability that at least one feature alerts in a given hour. What would you change so the page means something?", 'A')
# 5 CI mocked store outage
assert 600*12*60 == 432000 and 12+6 == 18
add(3, '🟢', "A model deploy passed every CI test, but the integration test used a mocked feature store, and in production the new model returned errors for 100% of requests for 12 minutes before an engineer rolled back, taking 6 further minutes to finish. At 600 requests per second, compute the failed requests in the first 12 minutes and name which tests and gates were missing. Which of them would you add first?", 'T')
# 6 skew imputation
assert 300/5000 == 0.06
add(3, '🟡', "The training pipeline switched to filling a null income with the training mean of 48,000, while the serving service still fills it with 0. In a sample of 5,000 live requests, 300 (6% of the sample) have a null income. How do you confirm the skew, estimate its damage, and fix it, and which control makes this class of change impossible to ship unnoticed?", 'S')
# 7 wrong version served
assert 4/10 == 0.4
add(3, '🟡', "At 10:00 the registry alias 'champion' was moved from version 17 to version 18, but 4 of the 10 serving pods (40%) cached version 17 at startup and never re-resolved the alias. The two versions differ by a mean absolute difference of 0.08 in score per request, and the logs show only the alias name. How do you detect this today, fix it, and change the design so the served version is always provable?", 'R')
# 8 late pipeline
assert (9*60+30)-(6*60) == 210 and 1000000*1 == 1000000
add(3, '🟡', "A feature table due at 06:00 landed at 09:30, which is 210 minutes late, and the 07:00 scoring job quietly read the previous day's partition, so 1,000,000 customers were scored on features one day old. The job exited with success. What do you do now for the 1,000,000 scores, and what checks make a stale input fail loudly next time?", 'D')
# 9 double run
assert 1000000+1000000 == 2000000
add(3, '🟡', "A daily scoring job that appends to its output table was retried by the scheduler after a timeout at minute 55, but the first run was still alive and also finished. The table now holds 2,000,000 rows for 1,000,000 customers for that date, and a downstream campaign job has already read it. How do you clean up, and how do you redesign the job so a duplicate run is harmless?", 'D')
# 10 units change
assert 850*100 == 85000 and 2/90 > 0.022 and 2/90 < 0.0223
add(3, '🟡', "An upstream team changed order_value from rupees to paise, a factor of 100, so a typical value of 850 became 85,000, and nobody told the ML team. The change ran for 2 days before it was caught, and the training table keeps 90 days, so those 2 days are about 2.2% of its days (about 2.2% of rows if volume per day is equal). What do you do about served predictions and the training table, and what contract would have caught it?", 'D')
# 11 error budget
bud = 0.005*30*24*60
assert round(bud) == 216 and 70+95+40 == 205 and round(bud)-205 == 11
add(3, '🟡', "A model API has a 99.5% availability objective over a 30-day month, which is 216 minutes of allowed downtime. Two outages have used 70 and 95 minutes, and the current one has run for 40 minutes so far and is still going. Counting the current outage, how much budget is left, and what do you decide about the release schedule and about the fix you are about to ship?", 'ED:error budgets and SLOs in SRE and MLOps material')
# 12 LLM provider outage
assert 40*0.25 == 10 and 1000*0.25 == 250
add(3, '🟡', "Your LLM provider starts returning rate-limit or server errors on 25% of calls at a traffic of 40 original requests per second, which is 10 failed calls per second. The client retries immediately up to 3 times, and a second provider is wired as a fallback but has never been used in production. What do you do in the first 30 minutes, and what could go wrong with the fallback itself?", 'L')
# 13 feedback loop
add(3, '🔴', "A recommender retrains weekly on clicks from its own recommendations. Over six weeks the share of impressions going to the top 1% of items rose from 35% to 52% (absolute points, of all impressions), while click-through on the whole page is flat. Explain the loop, how you would prove it with the data you have, and what you would change in logging and training. Which metric would you track from now on?", 'ED:feedback loops and exposure bias in ML system design material')
# 14 canary stats
zc = z2(9, 2000, 76, 38000)
assert 2000+38000 == 40000 and abs(9/2000-0.0045) < 1e-12 and 76/38000 == 0.002 and 2.0 < zc < 2.5, zc
add(3, '🔴', "A canary takes 5% of 40,000 requests in its first hour, which is 2,000 requests, with only 9 errors (0.45%), while the control's 38,000 requests had 76 errors (0.2%). Compute whether the gap is bigger than sampling noise, and say what you do at this point and what you would have wanted written down before the canary started. How does the answer change if the errors are all in one customer segment?", 'T')
# 15 reproducibility
assert round(0.842-0.829, 3) == 0.013
add(3, '🔴', "Retraining the same commit on the same table gave an AUC of 0.842 on the 10,000-row holdout (10% positives, 1,000 rows) in March and 0.829 in September, an absolute gap of 0.013, and an auditor asks you to reproduce the March model. Nobody pinned the library versions, the table is refreshed in place, and seeds were not logged. How do you find out how much of the gap is noise, what changed and what is unrecoverable, and what do you record from now on?", 'X')

# ================= 2 stars =================
# 16 drift never fires
assert 26*0.03 == 0.78
add(2, '🟡', "A drift monitor compares each week's feature distribution to the previous week, and its weekly population stability index stayed below 0.03 for 26 straight weeks, so it never fired. Over the same 26 weeks the labelled AUC slid from 0.84 to 0.78. Explain how a monitor can stay quiet while the model decays, and how you would redesign the reference windows and the alert rules.", 'A')
# 17 shadow mismatch
assert 500000*0.032 == 16000
add(2, '🟢', "During a shadow run the candidate's score differs from the production score by more than 0.05 on 3.2% of 500,000 requests, which is 16,000 requests, and the decision threshold is 0.5. The product owner asks whether it is safe to switch. What can a shadow run tell you and what can it not tell you, and how would you look at those 16,000 requests?", 'T')
# 18 blue-green cold start
assert 120 == 120 and 2400/120 == 20
add(2, '🟡', "After a blue/green switch, the 99th-percentile latency went from 120 ms to 2,400 ms (20 times the old value) for about 3 minutes because the green pods loaded a multi-gigabyte model after receiving traffic. Health checks only tested that the process was up. What do you change in the readiness checks and in the switch procedure, and what would you watch during the next switch?", 'G')
# 19 rollback criteria power
se = math.sqrt(0.02*0.98/10000)
assert abs(se-0.0014) < 0.00001 and abs(0.005/se-3.57) < 0.02 and 0.005/0.02 == 0.25
add(2, '🟡', "You must write automatic rollback criteria for a model whose error rate is about 2% at baseline, with 10,000 canary requests available before a ramp. The standard error of an error rate of 2% on 10,000 requests is about 0.14 points, so a rise to 2.5% (0.5 points absolute, 25% relative to 2%) is about 3.6 standard errors if the 2% baseline is treated as exactly known (about 2.4 against a concurrent control of 10,000 requests). What rule do you write, and how do you handle small segments that this volume cannot see?", 'T')
# 20 feature store stale
assert 7+1 == 8
add(2, '🟡', "A streaming job feeding the online store lagged by 7 hours, so the feature clicks_last_hour served to the model actually described the hour that ended 7 hours earlier, while offline training always used the live hour. The lag lasted 5 hours before anyone noticed, and the model returned normal-looking scores throughout. How do you detect this kind of staleness, what do you serve when a feature is stale, and how do you assess the damage?", 'S')
# 21 label leakage retrain
assert round(0.93-0.84, 2) == 0.09
add(2, '🟡', "A retrained refund-risk model scored an offline AUC of 0.93 against 0.81 online, and dropping one feature, ticket_reopened, which is filled in after the refund decision, took the offline AUC to 0.84. The leaky feature was added by a teammate three releases ago. How do you find the same problem in other features, what do you tell the stakeholders about the three earlier releases, and what check would catch it automatically?", 'X')
# 22 backfill planning
import math as m
assert m.ceil(9/4) == 3 and m.ceil(9/4)*40 == 120 and 9*40 == 360
add(2, '🟡', "A feature pipeline was broken for 9 daily partitions. Each partition takes 40 minutes, the cluster can run 4 partitions at once, and a rolling 7-day feature may make each day depend on the stored output of the previous day. Compute the backfill wall-clock time if the days were independent and if they must run in order, and say how you would order the work, protect live jobs and validate the result.", 'D')
# 23 registry mix-up lineage
assert 41-38 == 3
add(2, '🟡', "An engineer promoted version 38 of a model, out of 41 registered versions, believing it came from the full-data experiment, but it was trained on a 5% sample and nobody noticed for two days. The registry only stores a name, a version number and a metric. What metadata and promotion checks would you require, who can promote, and how do you find any other mislabelled versions?", 'R')
# 24 postmortem actions
assert 14-11 == 3 and round(11/14, 3) == 0.786
add(2, '🟡', "A postmortem for a bad model deploy lists 14 action items and 11 of them (79% of the 14) say 'be more careful' or 'add a review'. The manager wants the engineer who merged the change named in the report. How do you run the meeting, what makes an action item good, and how do you turn the 11 into changes that do not rely on people remembering?", 'ED:blameless postmortems and incident-review practice')
# 25 GPU cost incident
assert (40-6)*72*3 == 7344
add(2, '🟢', "A traffic burst made the autoscaler grow the GPU pool from 6 to 40 nodes, and scale-down was disabled during an earlier incident and never re-enabled, so the pool stayed at 40 nodes for 72 hours. A node costs an illustrative 3 per hour. Compute the extra cost and say how you find and prevent this kind of leftover emergency setting, and what a sensible scale-down policy looks like.", 'G')
# 26 autoscaling cold start
assert (900-500)*90 == 36000
add(2, '🟡', "A GPU service handles 400 requests per second against a capacity of 500, and traffic jumps to 900 per second. New pods need 90 seconds to load the model, and the autoscaler reacts to CPU, which stays low because the work is GPU-bound. Compute the backlog that builds in the 90 seconds before new capacity arrives, and say what you scale on instead and how you protect users meanwhile.", 'G')
# 27 fallback
assert 1000000*0.04 == 40000 and round(40000*(0.05-0.035)) == 600 and round((0.05-0.035)/0.05, 2) == 0.30
add(2, '🟡', "A ranking model with a 150 ms timeout falls back to a popularity list on 4% of 1,000,000 hourly requests, which is 40,000 requests. Conversion is 5% on the model and 3.5% on the fallback, so the fallback is 30% lower relative to 5%. Estimate the conversions lost per hour due to fallbacks (and say how reliable that estimate is), and decide whether to raise the timeout, add capacity or improve the fallback.", 'L')
# 28 streaming idempotency
assert 20*50000 == 1000000
add(2, '🟡', "A streaming job restarted and replayed the last 20 minutes from its committed offset at 50,000 events per minute, so 1,000,000 events were counted twice in the orders_last_hour feature. The model has been reading inflated counts for two hours, and the feature is a running counter that does not expire old events. How do you repair the feature values, and how do you make replays safe by design?", 'D')
# 29 secrets leak
assert 14 > 0
add(2, '🔴', "A training notebook containing a cloud access key was pushed to a public repository and a secret scanner flagged it 3 hours later. The key can read a bucket with 2,100,000 customer records, and the access logs show 14 downloads from addresses nobody recognises. What do you do in the first hour, in order, and what do you tell security, legal and the business?", 'ED:secrets and data leakage in ML repositories')
# 30 prompt regression
zp = z2(int(0.050*7500), 7500, int(0.031*8000), 8000)
assert 0.050*7500 == 375 and 0.031*8000 == 248 and zp > 4
add(2, '🟡', "A prompt edit shipped on Tuesday, and HTTP success stayed at 99.9%, but the thumbs-down share of rated answers rose from 3.1% of 8,000 rated answers the week before (248 answers) to 5.0% of 7,500 rated answers after (375), a 1.9 point absolute rise on a measured sample. Only a small share of traffic gets rated. Do you roll back, and how do you detect a prompt regression sooner next time?", 'L')
# 31 monitoring gap defaults
assert 2000000*0.15 == 300000
add(2, '🟢', "Dashboards show normal latency and a 0.1% error rate, but a feature lookup timeout makes the service return the default score 0.5 for 15% of 2,000,000 daily requests, which is 300,000 requests. No alert fired because the service returns success. What monitoring was missing, and how would you detect and count these degraded responses from now on?", 'ED:monitoring gaps in model-serving platforms')
# 32 volume alert
assert round(2/11, 3) == 0.182 and 11-9 == 2
add(2, '🟢', "A static alert fires when hourly prediction volume falls 20% below the mean of the same hour over the previous 7 days, and over one month it paged 11 times, of which 9 were weekends and holidays and only 2 were real outages, a precision of about 18% (2 of 11). The on-call engineer now mutes it. How do you redesign the alert so the 2 real outages still page, and what do you check before re-enabling the page?", 'A')
# 33 blast radius
assert 40+25+15+10+6+4 == 100
add(2, '🟡', "A new pricing-model threshold is about to roll out to 6 regions whose traffic shares are 40%, 25%, 15%, 10%, 6% and 4% of all requests. Order and size the rollout waves, say what you watch at each wave, and explain how you limit the blast radius if the threshold has a bug that only shows at a particular hour or customer type.", 'ED:blast radius and progressive delivery in release engineering')
# 34 overlapping retrain
assert 7.5-6 == 1.5 and 24//6 == 4
add(2, '🟡', "A training job takes 7.5 hours, and after a schedule edit it starts every 6 hours, so the second run starts 1.5 hours before the first finishes. Both write to the same registry name and the same checkpoint folder. How do you find out what has already been overwritten, what can the scheduler do to prevent overlap, and how do you make the training job safe if it does overlap?", 'D')
# 35 KS flags everything
assert 38/40 == 0.95
add(2, '🟡', "A two-sample KS test comparing this week's 2,000,000 rows to a reference of 2,000,000 rows flags 38 of 40 features (95% of them) with p-values below 0.001, while the largest KS statistic is only 0.02 and the model's labelled AUC is unchanged. Explain why the monitor fires constantly, and how you would change the test, the effect-size threshold and the alert rule.", 'A')

# ================= 1 star =================
# 36 rate limits
assert 150*1500 == 225000 and 225000-200000 == 25000 and round(25000/225000, 3) == 0.111
add(1, '🟡', "A provider limits you to 200,000 tokens per minute, and your traffic is 150 requests per minute at 1,500 tokens each, which is 225,000 tokens per minute. That is 25,000 over the limit, about 11% of the demand (relative to the 225,000). Requests get rate-limit errors in bursts. What short-term and structural fixes do you consider, and why do extra API keys in one organisation usually not help?", 'L')
# 37 retry storm
assert 1000*4 == 4000 and 4000 > 1500
add(1, '🟡', "A model service handles 1,000 requests per second and has a capacity of 1,500. During a 5-second slowdown every request times out and the clients retry up to 3 times at once, so the offered load can reach 4,000 requests per second, the original plus 3 retries each. How does this turn a short slowdown into an outage, and what do you add on the client and the server side?", 'L')
# 38 fallback never exercised
add(1, '🔴', "A rules-based fallback for a credit model was written 14 months ago and never exercised in production. When the model service failed last week the fallback itself returned errors for 100% of calls because a config key had been renamed. How do you test and maintain a fallback, and how would you introduce game days without causing an outage?", 'ED:fallbacks and game days in reliability engineering')
# 39 dataset overwritten
add(1, '🔴', "A regulator asks you to reproduce the exact training data of model v9, which went live 11 months ago, but the training table is overwritten in place every night and only the SQL is in git. What can you recover, what do you tell the regulator and what data-versioning design would have made this a one-hour task?", 'X')
# 40 feature view rollback
assert 3 < 7
add(1, '🔴', "A feature view was changed to version 2 by the producer team, and 3 of its 7 consumer models read the new schema while 4 still read version 1. After the change the 3 models are fine but a bug appears in the producer, and rolling the producer back would break those 3. How do you decide the rollback order, and what versioning and deprecation process prevents this deadlock?", 'ED:feature-store schema versioning and rollback')
# 41 monitor failed silently
add(1, '🟢', "The drift job itself failed 12 days ago because of an expired credential, and the dashboard kept showing the last computed values as if they were current. Nobody noticed until a model issue made someone check. How do you monitor the monitor, and what do you do about the 12 days with no coverage?", 'A')
# 42 quality SLO
assert abs(28*0.05-1.4) < 1e-9 and math.floor(28*0.05) == 1 and round(25/28, 3) == 0.893
add(1, '🟡', "A team promises that 95% of daily batch scoring runs finish by 07:00. Over 28 days it missed on 3 days, so 25 of 28 runs made it, which is 89.3%. How many whole misses would the objective have allowed over 28 days, what do you do when the budget is gone, and is a lateness objective enough for a model that can also be wrong?", 'ED:SLOs and error budgets for batch ML pipelines')
# 43 spot preemption
assert 3/2 == 1.5 and 4*1.5 == 6 and 4*3 == 12
add(1, '🟡', "A 20-hour training run on preemptible nodes is interrupted 4 times, and it checkpoints every 3 hours. On average a preemption loses half a checkpoint interval, which is 1.5 hours, and the worst case loses 3. Compute the expected and the worst-case lost work across the 4 interruptions, and say how you would pick the checkpoint interval and verify that resume gives the same model.", 'G')
# 44 library pickle
assert 60-14 == 46 and round(14/60, 3) == 0.233
add(1, '🟡', "After a base-image refresh, 14 of the 60 models (23% of them) fail to load because they were pickled under an older library version, and nobody has the original training code environment for 5 of the 14. How do you recover service quickly, how do you handle the 5, and what artifact format and image policy would you use from now on?", 'ED:dependency pinning and model serialization in MLOps guides')
# 45 severity and comms
assert round(0.03*0.2/0.03, 1) == 0.2
add(1, '🔴', "A model bug hits 3% of requests but those requests carry 20% of revenue, and it started 90 minutes ago. You are the incident commander with a shared on-call rota across 4 teams. How do you set the severity, who do you assign to which role, what cadence do you use for updates, and when do you decide between a fix, a rollback or a manual workaround?", 'T')
