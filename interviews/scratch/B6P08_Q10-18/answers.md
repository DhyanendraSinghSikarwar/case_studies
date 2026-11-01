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

