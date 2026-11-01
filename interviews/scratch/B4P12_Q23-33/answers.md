# Book 4 Part 12, Q23-Q33 answers (Wave B)

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
