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
