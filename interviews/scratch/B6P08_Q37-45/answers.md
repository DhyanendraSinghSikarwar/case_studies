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
