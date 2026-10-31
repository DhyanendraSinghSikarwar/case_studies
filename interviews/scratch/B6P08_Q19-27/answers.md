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
