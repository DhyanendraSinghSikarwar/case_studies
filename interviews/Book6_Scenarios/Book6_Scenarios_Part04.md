# Book 6 — Part 4: Experiment Design and Ambiguous A/B Results

**Topic:** Scenario-based "the A/B shows X, what do you do" questions for Data Scientist, Product Analyst and ML Engineer loops: sample ratio mismatch, novelty and primacy effects, peeking and sequential testing, multiple metrics, guardrails and multiple comparisons, underpowered or flat tests, minimum detectable effect and sample-size planning, network effects and interference, switchback and geo experiments, two-sided marketplace experiments, ratio metrics and the delta method, CUPED and variance reduction, heterogeneous effects and subgroup claims, Simpson's paradox inside experiments, contradictory metrics, ship or no-ship decisions on partial evidence, long-term holdouts and cumulative effects, bot and outlier contamination, logging and assignment bugs, when you cannot randomize (difference-in-differences, synthetic control, observational comparisons), bandits versus A/B tests, and AI-era twists (LLM feature tests, LLM-as-judge evaluation, non-determinism, silent model updates).

**Target:** 55  |  **Actual:** 55 (⭐⭐⭐ 18, ⭐⭐ 25, ⭐ 12)  |  **Date:** 2026-10-30  |  **Status:** Complete (answers merged, checked, reviewed)

**Scope note:** this part owns the scenario, ambiguous-result and ship-decision angle (the data in front of you is messy, conflicting or suspicious; what do you do, in what order, with what evidence). It does not repeat the theory in Book 1 Part 10 (A/B testing, causal inference and experimentation); Wave B answers should cross-reference that part and Book 6 Parts 1 to 3 only by checked headings. Book 6 Part 2 owns models that degrade after launch and Part 3 owns imbalanced, noisy and missing data, so the object here is the experiment itself. All numbers in the prompts are invented illustrative numbers, not data from any company; every percentage names its base in the prompt and says whether it is a relative or absolute change, and every 'balanced' or 'significant' claim in a prompt is true of the numbers given. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part04_sources.md). Searches returned A/B-testing pitfall lists (Dataford, datainterview.com, PracHub), guardrail and ship-decision pages, marketplace, switchback and interference material (including a DoorDash careers post and an arXiv paper), ratio-metric and CUPED docs, causal-inference interview guides, underpowered-test articles, bot and outlier pages and 2026 practitioner posts on testing LLM features. Several searches returned general guidance rather than interview pages, and none tied a scenario to a verified employer round, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

### Q1 ⭐⭐⭐ 🟢 A test meant to split 100,000 users 50/50 ended with 52,000 in control and 48,000 in treatment. Treatment shows conversion of 5.1% against 4.8% for control (0.3 percentage points absolute, about 6% relative to control's 4.8%) with p = 0.03, and the product manager wants to ship today. Explain what you check first and what you tell the manager.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I do not ship today, because a 52,000 / 48,000 split of a 50/50 test is a sample ratio mismatch (SRM, the arm sizes do not match the design), so the assignment or logging is broken and the 0.3-point gap cannot be trusted.

**Clarifying questions:**
- Was the intended split exactly 50/50, and did it change mid-test? A ramp or a config change makes a ratio mismatch expected, not a bug.
- Are the counts users assigned or users who triggered or loaded the page? Losing users after assignment (crash, slow load, redirect) is the classic SRM cause.
- Is the mismatch the same every day? A constant mismatch points to a code path. A one-day jump points to a deployment or an outage.
- Does the split differ by platform, country or browser? It tells me where the loss happens.
- How was the p-value of 0.03 computed (which test, which counts)? I want to reproduce it (it checks out: z = 2.19) so that the discussion is about validity, not arithmetic.

**Approach:**
1. Say it plainly to the manager: "The test failed a validity check. The result is not readable yet."
2. Run the SRM test: chi-square of observed against the planned split. Here chi-square = 160, p about 1e-36 (see Code). A fair split almost never shows a 4,000 gap on 100,000 users, so this is a bug, not luck. Use a strict alert level such as p < 0.001 for SRM.
3. Locate the loss: split the counts by day, platform, app version, country and assignment path. Find the slice where the ratio breaks.
4. Check the usual causes: bot filtering applied to one arm only, a redirect or heavy treatment page that makes users bounce before logging, a crash in treatment, a stale cache or CDN serving one arm, a hash or bucketing bug, a join that drops users.
5. Fix the cause and re-run (or re-analyse from raw assignment logs if the loss was only in logging). Do not "fix" it by reweighting or by dropping users until the numbers look 50/50, because the missing users are not random.
6. Only then read the conversion result.

**Metrics:**
- SRM: chi-square = sum over arms of (observed - expected)^2 / expected, expected = 50,000 each, 1 degree of freedom. Alert if p < 0.001.
- Primary: conversion = converting users / assigned users, per arm, 95% CI on the difference.
- Guardrail: the SRM check runs before any metric is read, and I repeat it by day and by segment.

**Risks:**
- The users who disappeared are usually different from the ones who stayed (for example, slow-device users in the heavy arm). That biases the lift in an unknown direction.
- "The effect is small, so the bias is small" is wrong. A 2,000-user hole can halve a 0.3-point gap and push it out of significance.
- Fixing the ratio by deleting users from the bigger arm just hides the bug.
- Pressure to ship because the p-value looks good.

**What the interviewer scores:**
- Strong: names SRM first and runs the chi-square before reading any lift. Weak: starts discussing whether a 6% relative lift is big enough.
- Strong: gives a list of causes and a way to localise them (by day, platform, path). Weak: "rerun the test" with no diagnosis.
- Strong: explains why the gap is untrustworthy (differential loss, selection). Weak: "the sample is still big, so it is fine."
- Strong: tells the manager something clear and non-blocking: what I will do and by when. Weak: a lecture on p-values.

**Example:** (illustrative numbers) The design is 50,000 per arm. Observed is 52,000 control and 48,000 treatment: chi-square = 2 x 2,000^2 / 50,000 = 160. Now suppose a bug dropped 2,000 treated users who convert at only 1% (slow-device users). Add them back and treatment is (2,448 + 20) / 50,000 = 4.94%, against control 4.80%: the gap shrinks from 0.30 to about 0.14 points and p rises to about 0.3 (see Code). Weak answer: "p = 0.03, 6% lift, ship it." Strong answer: "SRM fails at p near 1e-36, so I do not read the lift until I find where 4,000 users went."

**Code:**
```python
import numpy as np
from scipy import stats

# Illustrative numbers from the prompt
n_c, n_t = 52_000, 48_000
x_c, x_t = round(0.048 * n_c), round(0.051 * n_t)   # conversions: 2496 and 2448

# 1) SRM check: expected 50/50
exp = 50_000
chi2 = ((n_c - exp) ** 2 + (n_t - exp) ** 2) / exp
p_srm = stats.chi2.sf(chi2, 1)
print("SRM chi2 =", chi2, " p =", p_srm)
assert chi2 == 160.0 and p_srm < 1e-30

# 2) The prompt's conversion test, recomputed from the stated counts
p_c, p_t = x_c / n_c, x_t / n_t
pool = (x_c + x_t) / (n_c + n_t)
se = np.sqrt(pool * (1 - pool) * (1 / n_c + 1 / n_t))
z = (p_t - p_c) / se
p_two = 2 * stats.norm.sf(abs(z))
print(f"conversion control {p_c:.4f}, treatment {p_t:.4f}, diff {p_t-p_c:.4f}")
print(f"z = {z:.2f}, two-sided p = {p_two:.3f}")
assert round(p_two, 2) == 0.03 and abs((p_t / p_c - 1) - 0.0625) < 1e-9   # about 6% relative

# 3) Chance that a fair 50/50 split ever looks like 52,000 / 48,000
print("P(|diff| >= 2000 under fair split) =", 2 * stats.binom.cdf(48_000, 100_000, 0.5))

# 4) Why the SRM matters. The treatment arm is 2,000 short of 50,000. Suppose those 2,000
#    were low converters (illustrative: 1.0%) dropped by a bug. Treatment with them restored:
lost = 2_000
x_full, n_full = x_t + lost * 0.01, n_t + lost
rate_full = x_full / n_full
gap = rate_full - p_c
pool2 = (x_c + x_full) / (n_c + n_full)
z2 = gap / np.sqrt(pool2 * (1 - pool2) * (1 / n_c + 1 / n_full))
print(f"treatment rate with the 2,000 restored: {rate_full:.4f}; gap {gap*100:.2f} points; p = {2*stats.norm.sf(z2):.2f}")
assert 0.0012 < gap < 0.0016 and 2 * stats.norm.sf(z2) > 0.05   # gap halves and is no longer significant
```

**Output (my run):**
```text
SRM chi2 = 160.0  p = 1.1314837902433038e-36
conversion control 0.0480, treatment 0.0510, diff 0.0030
z = 2.19, two-sided p = 0.029
P(|diff| >= 2000 under fair split) = 1.1530938666727834e-36
treatment rate with the 2,000 restored: 0.0494; gap 0.14 points; p = 0.31
```

**Follow-ups:**
- The SRM is small (50.5 / 49.5). Can I ignore it? No, the test is about the p-value, not the size of the gap: at 100,000 users a 1,000 gap (51,000 / 49,000) still gives chi-square 40. Small but significant means a real bug that touches fewer users.
- Can I just reweight to 50/50? No. Reweighting fixes counts, not the fact that the missing users differ. Find and fix the cause.
- Where is this covered in theory? Book 1 Part 10, Q6 ("What is a Sample Ratio Mismatch (SRM)? How do you detect it and what are the common causes?").

**Common mistakes:**
- Reading the lift first and treating the SRM as a footnote.
- Using the usual 0.05 for SRM and ignoring warnings at 0.01 (it is a health check, so a strict threshold is fine).
- Dropping users to rebalance.
- Blaming "randomness" for a 4,000 gap on 100,000 users.

### Q2 ⭐⭐⭐ 🟢 A test was planned for 14 days, and after 4 days the dashboard shows conversion of 6.3% in treatment against 6.0% in control (0.3 points absolute, 5% relative to control) with p = 0.03. The product manager wants to stop now and ship. Explain what is wrong with this and what you would do.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would not stop on day 4, because looking every day and stopping at the first p < 0.05 turns a 5% false-positive rate into about 20%, and four days also miss the weekly cycle; I keep going to day 14 or use a pre-planned sequential rule.

**Clarifying questions:**
- Was a sequential or always-valid method planned, or a fixed-horizon test? If fixed, the p-value is only valid at day 14.
- How many users per arm are in so far? It tells me whether p = 0.03 is believable and how wide the interval is.
- Does the metric have a weekly pattern (weekday versus weekend shoppers)? Four days is half a cycle.
- Are the first-day users heavy or loyal users? Early traffic is not a random sample of the full period.
- What is the cost of waiting 10 more days versus a wrong launch? It decides whether an early-stop rule is worth building.

**Approach:**
1. Explain the problem in one line: "A fixed-horizon p-value assumes one look at the planned end. Daily looks give many chances to cross 0.05 by luck."
2. Show the size of the problem: in an A/A simulation with 14 daily looks, about 22% of tests show at least one p < 0.05 (see Code), against 5% with one look at the end.
3. Offer the honest choices: (a) wait until day 14 and read once; (b) if early stopping is business-critical, use a pre-agreed sequential design (alpha-spending such as O'Brien-Fleming style, or always-valid p-values/mSPRT) planned before the test.
4. Check what the early number is worth: with the interval, not just the p-value. At day 4 the 95% interval is about 0.03 to 0.57 points, so it runs from nearly zero to nearly double the estimate.
5. Protect against the second problem, the weekly cycle: run full weeks, so day-4 averages that over-weight a few weekdays do not mislead.
6. Agree with the PM: ship decision at day 14, with a guardrail check allowed early (stop early only for harm).

**Metrics:**
- Primary: conversion = converting users / assigned users, 95% CI on the absolute difference.
- False-positive rate under peeking = share of null experiments where any daily look has p < 0.05.
- Guardrails: stopping for harm is allowed, so I watch error rate and latency daily with a stricter threshold.

**Risks:**
- Winner's curse: stopping at the first significant look picks an overstated effect (a lucky early peak).
- Novelty effect: day 1-4 behaviour may fade (see the next question).
- Weekday bias: 4 days may be all weekdays.
- The PM learns that peeking "works" because it sometimes does.

**What the interviewer scores:**
- Strong: names peeking and gives a number for the inflated false-positive rate. Weak: "p is under 0.05 so it is significant."
- Strong: offers a practical route (wait, or pre-planned sequential testing), not just "no." Weak: refuses without alternatives.
- Strong: mentions weekly seasonality and the interval, not only the p-value. Weak: only talks about p-values.
- Strong: separates stopping for efficacy (strict) from stopping for harm (allowed). Weak: treats both the same.

**Example:** (illustrative numbers) About 59,000 users per arm by day 4 gives z = 2.14 and p = 0.032 for 6.3% against 6.0%. In an A/A test (no real difference) with 14 daily looks, 22.2% of runs hit p < 0.05 at some look; a single look at day 14 gives 4.7%. A constant boundary that keeps the overall error at 5% across 14 looks is about z = 2.6, and the day-4 z of 2.14 does not cross it. Weak answer: "p = 0.03, ship." Strong answer: "That p is only valid at day 14. Check the boundary or wait."

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(42)

# What sample size makes 6.3% vs 6.0% give p = 0.03? (illustrative: infer n per arm)
p_c, p_t = 0.060, 0.063
z_target = stats.norm.isf(0.03 / 2)
pool = (p_c + p_t) / 2
n_needed = 2 * pool * (1 - pool) * (z_target / (p_t - p_c)) ** 2
print(f"p = 0.03 needs about {n_needed:,.0f} users per arm at day 4")
n4 = 59_000
se = np.sqrt(2 * pool * (1 - pool) / n4)
z4 = (p_t - p_c) / se
print(f"with n = {n4:,} per arm: z = {z4:.2f}, p = {2*stats.norm.sf(z4):.3f}")
assert abs(2 * stats.norm.sf(z4) - 0.03) < 0.005
lo, hi = (p_t - p_c) - 1.96 * se, (p_t - p_c) + 1.96 * se
print(f"95% CI for the difference: {lo*100:.2f} to {hi*100:.2f} points")
assert abs(lo*100 - 0.03) < 0.01 and abs(hi*100 - 0.57) < 0.01
assert abs(p_t / p_c - 1 - 0.05) < 1e-9      # 5% relative

# Peeking: A/A test (no true effect), 14 daily looks, 5,000 users per arm per day
days, per_day, sims, p0 = 14, 5_000, 4_000, 0.06
xa = rng.binomial(per_day, p0, size=(sims, days)).cumsum(axis=1)
xb = rng.binomial(per_day, p0, size=(sims, days)).cumsum(axis=1)
n = per_day * np.arange(1, days + 1)
pp = (xa + xb) / (2 * n)
z = (xb / n - xa / n) / np.sqrt(2 * pp * (1 - pp) / n)
fp_any = (np.abs(z) > 1.96).any(axis=1).mean()
fp_final = (np.abs(z[:, -1]) > 1.96).mean()
print(f"false win rate: stop at first p<0.05 in 14 daily looks = {fp_any:.3f}; one look at day 14 = {fp_final:.3f}")
assert 0.15 < fp_any < 0.27 and 0.03 < fp_final < 0.07

# Pocock-style constant boundary for 14 equally spaced looks (via simulation of the null)
zz = rng.standard_normal((200_000, days)).cumsum(axis=1) / np.sqrt(np.arange(1, days + 1))
bound = np.quantile(np.abs(zz).max(axis=1), 0.95)
print(f"constant z boundary for 14 looks at overall 5%: {bound:.2f}  (day-4 z = {z4:.2f} is below it)")
assert z4 < bound
```

**Output (my run):**
```text
p = 0.03 needs about 60,402 users per arm at day 4
with n = 59,000 per arm: z = 2.14, p = 0.032
95% CI for the difference: 0.03 to 0.57 points
false win rate: stop at first p<0.05 in 14 daily looks = 0.222; one look at day 14 = 0.047
constant z boundary for 14 looks at overall 5%: 2.61  (day-4 z = 2.14 is below it)
```

**Follow-ups:**
- The PM says "but the effect is real, we saw it." The number of looks matters: if the true effect is zero, one in five tests would show it at some look. I need a rule fixed in advance, not a feeling.
- Can we peek if we use Bayesian methods? The posterior is also not immune: stopping when the probability of being better exceeds a threshold still inflates errors unless the stopping rule is accounted for (theory: Book 1 Part 10, Q7 "The A/B test shows a significant lift but the PM wants to stop the test after 3 days. What is wrong with peeking and what do you do?").
- What if the lift is huge on day 4? A sequential boundary lets a huge effect stop early; a small one does not.

**Common mistakes:**
- Stopping at the first significant day.
- Planning a 14-day test and reporting the day-4 snapshot.
- Using a sequential method but picking the boundary after seeing the data.
- Quoting the p-value without the interval.

### Q3 ⭐⭐⭐ 🟢 A new button shows click-through rate of 5.6% in treatment against 5.0% in control in week 1, 5.3% against 5.0% in week 2 and 5.1% against 5.0% in week 3. The week-1 readout was already presented as a 12% relative lift. Explain what you think is happening, how you would confirm it and what number you would quote.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** This looks like a novelty effect (the lift fades as users stop being curious about the new button), so I would quote the latest-week number of about +2% relative with its interval, not the +12% from week 1.
**Clarifying questions:**
- Is the button visible to everyone from day 1, or does exposure ramp? A ramp can fake a fade.
- Are the same users in all three weeks, or is each week a new set? Same users show a fade in behaviour; different users show a change in mix.
- Is click-through rate per user or clicks per impression? A per-impression rate can fall if the button is shown more often to the same people.
- Is the button part of a flow that matters (a purchase step) or a side element? It decides whether a small lasting lift is worth shipping.
- Was the week-1 +12% already promised to anyone? It tells me how hard the correction conversation will be.

**Approach:**
1. Check the shape: relative lift by week is 12%, 6%, 2% (see Code). That is a steady decline, the signature of novelty (a primacy effect would instead rise as users learn).
2. Rule out the boring explanations: weekday mix, a marketing push in week 1, seasonality (the control is flat at 5.0%, which helps), logging changes, and traffic mix.
3. Confirm with cuts: new users versus returning users (new users have no habit to be "novel" against, so their lift is the cleanest estimate of the lasting effect); lift by days since first exposure; lift for users first exposed in week 3 versus week 1.
4. Estimate the steady state: use the latest full week, or the users exposed for several weeks, with its interval. Do not extrapolate from three noisy points.
5. Decide: if the lasting estimate is positive and worth the cost, ship it and say the size honestly. If the interval includes zero, run longer or keep a long-term holdout.
6. Correct the record: tell stakeholders the week-1 number was a launch spike.

**Metrics:**
- Weekly relative lift = (CTR treatment / CTR control - 1) for that week's users.
- Click-through rate (per user) = users who clicked at least once / users who saw the button.
- Guardrails: conversion and orders (a button that gets clicks but no purchases is a bad sign), page load time.

**Risks:**
- Extrapolating a decay curve from three points is fragile.
- New-user versus returning-user cuts are not randomised subgroups of exposure history, so they are descriptive.
- The reverse effect: primacy (users need time to learn) looks like a rising lift, so the trend direction matters.
- The presented 12% sets an expectation that is hard to walk back.

**What the interviewer scores:**
- Strong: names novelty, shows the weekly series, and picks the late-week number. Weak: "the average over three weeks is 6.7%."
- Strong: proposes two checks (new versus returning, time since exposure). Weak: "wait and see."
- Strong: includes the interval and says week 3 is not significant on its own (see Code). Weak: calls the +2% a certain win.
- Strong: addresses the already-presented 12%. Weak: ignores the stakeholder issue.

**Example:** (illustrative numbers) Control is flat at 5.0%. Treatment is 5.6%, 5.3% and 5.1%: gaps of 0.6, 0.3 and 0.1 points, or +12%, +6% and +2% relative. With 100,000 users per arm per week, the week-3 gap of 0.1 points has a 95% interval of about -0.09 to +0.29 points: it includes zero. So the honest statement is "the lift is fading toward a small number, at most about +6% relative and possibly zero; I will keep the test running or keep a holdout." Weak answer: "Lift is 12%, great." Strong answer: "Week 1 was novelty. The lasting effect is about +2% with a wide interval."

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(7)

ctr_c = 0.050
ctr_t = [0.056, 0.053, 0.051]
rel = [(t / ctr_c - 1) * 100 for t in ctr_t]
print("relative lift by week (%):", [round(r, 1) for r in rel])
assert [round(r) for r in rel] == [12, 6, 2]

# Is week 3 still distinguishable from zero? Illustrative: 100,000 users per arm per week
n = 100_000
for wk, t in enumerate(ctr_t, 1):
    pool = (t + ctr_c) / 2
    se = np.sqrt(2 * pool * (1 - pool) / n)
    d = t - ctr_c
    print(f"week {wk}: diff {d*100:.1f} pts, 95% CI {100*(d-1.96*se):.2f} to {100*(d+1.96*se):.2f}")
se3 = np.sqrt(2 * 0.0505 * 0.9495 / n)
assert (0.001 - 1.96 * se3) < 0 < (0.001 + 1.96 * se3)   # week 3 CI includes 0

# Decay shape: the gap roughly halves each week (0.6, 0.3, 0.1 points). Fit log-linear decay.
gap = np.array([0.6, 0.3, 0.1])
slope = np.polyfit([1, 2, 3], np.log(gap), 1)[0]
print(f"fitted weekly decay factor = {np.exp(slope):.2f}")
asymptote_note = "extrapolated gap in week 6 (if pure exponential decay): %.2f pts" % (0.6 * np.exp(slope) ** 5)
print(asymptote_note)

# What to quote: the week-3 estimate with its interval, not week 1
d3 = 0.001
lo, hi = d3 - 1.96 * se3, d3 + 1.96 * se3
print(f"quote: about +{d3*100:.1f} pts (+{d3/ctr_c*100:.0f}% relative), 95% CI {lo*100:.2f} to {hi*100:.2f} pts, still fading")
assert round(d3 / ctr_c * 100) == 2
```

**Output (my run):**
```text
relative lift by week (%): [12.0, 6.0, 2.0]
week 1: diff 0.6 pts, 95% CI 0.40 to 0.80
week 2: diff 0.3 pts, 95% CI 0.11 to 0.49
week 3: diff 0.1 pts, 95% CI -0.09 to 0.29
fitted weekly decay factor = 0.41
extrapolated gap in week 6 (if pure exponential decay): 0.01 pts
quote: about +0.1 pts (+2% relative), 95% CI -0.09 to 0.29 pts, still fading
```

**Follow-ups:**
- How long do I wait for novelty to wear off? Until the lift stabilises over two or more consecutive weeks, or until the new-user lift and the returning-user lift agree.
- Could the fade be a fault, not novelty? Yes: a bug or a traffic change in weeks 2 and 3. The flat control and a check of event volumes help rule that out.
- Where is this covered in theory? Book 1 Part 10, Q8 ("What is the novelty effect and the primacy effect? How do you detect them and what do you do about them?").

**Common mistakes:**
- Quoting the average of all weeks, or the best week.
- Calling the test "significant" because the pooled data is.
- Extrapolating a curve from a few points as if it were a forecast.
- Forgetting new users: they are the cleanest read on the lasting effect.

### Q4 ⭐⭐⭐ 🟢 A team reports 20 metrics for a test whose primary metric (purchases per user) is flat, and one secondary metric, time on page, is significant at p = 0.04, so the team calls the test a win. If none of the 20 metrics had a true effect and each were tested independently at the 5% level, the chance of at least one false positive would be about 64%. Explain how you would read this result and how the metrics should have been set up.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I read this as no win: the pre-declared primary metric is flat, and one of 20 metrics at p = 0.04 is about what chance alone produces, so I would not call it a win and I would fix the metric plan before the next test.

**Clarifying questions:**
- Was purchases per user declared as the primary metric before the test? If yes, the decision rests on it.
- Were the 20 metrics all pre-registered, or picked after looking? Picking afterwards makes the number of "looks" bigger than 20.
- Are the metrics related (clicks, time, pages per session)? Correlated metrics give fewer independent chances than 20.
- Which way did time on page move, and is that good? More time can mean engagement or confusion.
- Are there segment cuts too (new users, mobile)? Each cut multiplies the comparisons again.

**Approach:**
1. Count the looks: 20 metrics at the 5% level gives about a 64% chance of at least one p < 0.05 even with no true effect, and an expected 1.0 false positive (see Code).
2. Apply the rule that was set before the test: the primary metric decides. It is flat, so the test is not a win.
3. Treat time on page as a hypothesis to test next, not a result. Check the direction, the effect size and whether it fits a mechanism (for example, a new layout that makes pages longer to read).
4. If it must be assessed now, adjust: Bonferroni threshold 0.05 / 20 = 0.0025 (p = 0.04 fails; adjusted p = 0.8), or a false-discovery-rate rule such as Benjamini-Hochberg. The smallest of 20 p-values at 0.04 fails both.
5. Fix the design for next time: one primary metric, 2-4 guardrails, secondary metrics labelled as exploratory, a pre-registered analysis plan, and a hierarchy (test secondary metrics only if the primary passes, a gatekeeping rule).
6. If time on page is truly valuable, run a confirmatory test where it is the single primary metric.

**Metrics:**
- Family-wise error rate = P(at least one false positive among the tests). Bonferroni keeps it at or under alpha.
- False discovery rate = expected share of "wins" that are false (Benjamini-Hochberg controls it).
- Primary: purchases per user = purchases / assigned users. Time on page is secondary.
- Guardrails: bounce rate, errors, latency.

**Risks:**
- Reading time on page as engagement when it may be friction.
- Bonferroni is conservative when metrics are correlated (see Code: correlated metrics give about 36%, not 64%), so I report both raw and adjusted values.
- Post-hoc stories: any significant metric can be explained after the fact.
- Over-correcting: an exploratory finding is not worthless, it is a lead.

**What the interviewer scores:**
- Strong: calculates the 64% and says the primary metric decides. Weak: "p = 0.04 so it works."
- Strong: separates primary, guardrail and exploratory metrics and states they are fixed in advance. Weak: lists every metric as equal.
- Strong: knows Bonferroni and Benjamini-Hochberg and what each controls. Weak: names them with no use.
- Strong: proposes a confirmation test. Weak: either ships or discards without a plan.

**Example:** (illustrative numbers) 20 independent null metrics: the chance of at least one p < 0.05 is 1 - 0.95^20 = 64.2%, simulated 64.0%. The one metric with p = 0.04 has a Bonferroni-adjusted p of 0.04 x 20 = 0.8 (min with 1). With correlated metrics (correlation 0.6) the chance of at least one false positive is about 36%, still far above 5%. Weak answer: "Time on page is significant, call it a win." Strong answer: "Primary is flat. One in 20 at p = 0.04 is what chance gives, so this is a lead for a confirmatory test."

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(11)

m, alpha = 20, 0.05
print("P(at least one false positive in 20 independent tests) =", round(1 - (1 - alpha) ** m, 4))
assert round(1 - (1 - alpha) ** m, 2) == 0.64

# Simulate: 20 independent null metrics, 20,000 experiments
sims = 20_000
p = rng.uniform(size=(sims, m))                 # null p-values are uniform
any_fp = (p < alpha).any(axis=1).mean()
mean_fp = (p < alpha).sum(axis=1).mean()
print(f"simulated P(any p<0.05) = {any_fp:.3f}; mean number of false positives = {mean_fp:.2f}")
assert abs(any_fp - 0.64) < 0.01 and abs(mean_fp - 1.0) < 0.03

# Correlated metrics (rho = 0.6 between metrics) -> fewer independent chances
rho = 0.6
cov = np.full((m, m), rho) + (1 - rho) * np.eye(m)
zs = rng.multivariate_normal(np.zeros(m), cov, size=sims)
pc = 2 * stats.norm.sf(np.abs(zs))
any_fp_c = (pc < alpha).any(axis=1).mean()
print(f"correlated metrics (rho=0.6): P(any p<0.05) = {any_fp_c:.3f}")
assert any_fp_c < any_fp

# Corrections: the one p = 0.04 among 20
p_obs = 0.04
print("Bonferroni threshold:", alpha / m, "-> significant?", p_obs < alpha / m)
print("Bonferroni-adjusted p:", min(1.0, p_obs * m))
assert p_obs >= alpha / m and min(1.0, p_obs * m) == 0.8

# Family-wise error with Bonferroni and with a pre-registered single primary metric
fw_bonf = (p < alpha / m).any(axis=1).mean()
fw_primary = (p[:, 0] < alpha).mean()
print(f"family-wise error: Bonferroni = {fw_bonf:.3f}; one pre-registered primary = {fw_primary:.3f}")
assert fw_bonf < 0.06 and abs(fw_primary - 0.05) < 0.01
```

**Output (my run):**
```text
P(at least one false positive in 20 independent tests) = 0.6415
simulated P(any p<0.05) = 0.640; mean number of false positives = 0.99
correlated metrics (rho=0.6): P(any p<0.05) = 0.355
Bonferroni threshold: 0.0025 -> significant? False
Bonferroni-adjusted p: 0.8
family-wise error: Bonferroni = 0.050; one pre-registered primary = 0.048
```

**Follow-ups:**
- What if the secondary metric had been pre-registered as a co-primary? Then split the alpha (for example 0.025 each) or use a gatekeeping order. Pre-registration is what makes it count.
- Should I always use Bonferroni? It controls the strictest error but loses power with many metrics. For exploratory dashboards I use Benjamini-Hochberg and say that the findings are leads.
- Where is this covered in theory? Book 1 Part 10, Q9 ("You track 20 metrics (or 10 variants) in one test and one is significant at p=0.04. What is the multiple-testing problem and how do you handle it (Bonferroni, BH/FDR)?").

**Common mistakes:**
- Treating the best of 20 as if it were the only one tested.
- Adding metrics after the test until something is significant.
- Applying Bonferroni to the secondary metrics but ignoring the number of segments and variants.
- Forgetting that "not significant after correction" is not proof of no effect.

### Q5 ⭐⭐⭐ 🟢 A test with 40,000 users per arm shows conversion of 10.1% in treatment against 10.0% in control, and the 95% confidence interval for the absolute difference runs from about -0.3 to +0.5 percentage points. The product manager says 'no effect, kill it' while the designer says 'it is positive, ship it'. Explain what you conclude and what you recommend.
**Asked at:** Underpowered-test and MDE material (a Towards Data Science 'what to do when an A/B test result is not significant' article, a Dataford 'non significant test PM wants launch' page, a HackerNoon 'running A/B tests you can't measure' post, a Statsig power-analysis page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Neither of them is right: the interval of -0.3 to +0.5 points says the test is inconclusive, because it cannot rule out a small harm or a decent gain, so I recommend a decision based on cost and the interval, not on the word "significant."

**Clarifying questions:**
- What is the smallest lift that would be worth the cost of shipping and maintaining this? That is the bar the interval must clear.
- Was a sample size or minimum detectable effect (MDE) set before the test? If 40,000 per arm was planned for a 0.6-point effect, the test did its job and found nothing that big.
- Is the change cheap to ship, cheap to reverse, or a one-way door? It changes how much evidence I need.
- Are there guardrails or segments that moved? The conversion interval is not the whole picture.
- Can we run longer or pool with a second test? It determines whether "inconclusive" can become "answered."

**Approach:**
1. Read the interval, not the p-value: the estimate is +0.1 points, the 95% interval is -0.32 to +0.52 points, p = 0.64 (see Code). Zero is inside, so "no significant effect." But so are -0.3 and +0.5.
2. Say what the test could detect: with 40,000 per arm at 10% baseline, 80% power needs a true lift of about 0.6 points (5.9% relative). A smaller lift would be missed more often than not. So "not significant" here is weak evidence of no effect.
3. Rule out large effects, both ways: the data are consistent with a harm of up to 0.3 points and a gain of up to 0.5 points, and nothing outside that.
4. Link to the decision: if the change is cheap and a 0.3-point harm is acceptable, shipping for other reasons (design, maintenance) is defensible. If it needs a gain of at least 0.3 points to pay for itself, the test cannot say yes.
5. Get more evidence if the stakes justify it: to detect +0.3 points at 80% power needs about 159,000 users per arm (4 times the current), see Code.
6. Say the sentence to both: "Absence of evidence is not evidence of absence, and the data are not enough for either claim."

**Metrics:**
- Difference in conversion = treatment rate - control rate, with a 95% CI (Wald: difference +/- 1.96 x standard error).
- MDE = (z for alpha/2 + z for power) x sqrt(2 x p x (1 - p) / n), per arm.
- Guardrails: other metrics that might show harm (retention, revenue).

**Risks:**
- Treating a wide interval as proof of zero (kills a possibly good idea).
- Treating a positive point estimate as a win (ships noise).
- Peeking and extending until it turns significant.
- Ignoring the cost of being wrong in each direction.

**What the interviewer scores:**
- Strong: reads the CI, states the range, and computes what the test could detect. Weak: argues over the word "significant."
- Strong: asks what lift is worth shipping and ties the decision to it. Weak: "run it longer" with no number.
- Strong: gives a sample size for a useful effect. Weak: no plan to reduce the uncertainty.
- Strong: sides with neither stakeholder and explains why. Weak: sides with one.

**Example:** (illustrative numbers) 40,000 per arm, 10.0% against 10.1%. Standard error = 0.213 points, so the interval is -0.32 to +0.52. If the true lift were +0.3 points, this test would only reach significance about 30% of the time (simulated). To detect +0.3 points with 80% power I need about 159,000 per arm. Weak answer: "No effect, kill it" or "It is positive, ship it." Strong answer: "Inconclusive: it could be -0.3 or +0.5. Decide on cost, or collect four times the data."

**Code:**
```python
import numpy as np
from scipy import stats

n = 40_000
p_c, p_t = 0.100, 0.101
se = np.sqrt(p_t * (1 - p_t) / n + p_c * (1 - p_c) / n)
d = p_t - p_c
lo, hi = d - 1.96 * se, d + 1.96 * se
print(f"diff = {d*100:.2f} pts, se = {se*100:.3f} pts, 95% CI = {lo*100:.2f} to {hi*100:.2f} pts")
assert round(lo * 100, 1) == -0.3 and round(hi * 100, 1) == 0.5
z = d / se
print(f"z = {z:.2f}, p = {2*stats.norm.sf(z):.2f}")

# Smallest effect this test could reliably detect (80% power, 5% two-sided)
mde = (stats.norm.isf(0.025) + stats.norm.isf(0.2)) * np.sqrt(2 * 0.1 * 0.9 / n)
print(f"MDE (80% power) = {mde*100:.2f} pts = {mde/p_c*100:.1f}% relative")
assert 0.0055 < mde < 0.0065

# Users per arm needed to detect +0.3 pt (3% relative) at 80% power
def n_per_arm(p1, p2, alpha=0.05, power=0.8):
    za, zb = stats.norm.isf(alpha / 2), stats.norm.isf(1 - power)
    pb = (p1 + p2) / 2
    num = (za * np.sqrt(2 * pb * (1 - pb)) + zb * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return num / (p2 - p1) ** 2
n3 = n_per_arm(0.100, 0.103)
print(f"users per arm to detect +0.3 pts: {n3:,.0f}")
assert 155_000 < n3 < 165_000

# Simulation: how often would this test see 'significant' if the true lift were +0.3 pts?
rng = np.random.default_rng(5)
sims = 20_000
a = rng.binomial(n, 0.100, sims) / n
b = rng.binomial(n, 0.103, sims) / n
pp = (a + b) / 2
zz = (b - a) / np.sqrt(2 * pp * (1 - pp) / n)
power = (zz > 1.96).mean()
print(f"power at n=40,000 per arm if true lift = +0.3 pts: {power:.2f}")
assert 0.2 < power < 0.4
```

**Output (my run):**
```text
diff = 0.10 pts, se = 0.213 pts, 95% CI = -0.32 to 0.52 pts
z = 0.47, p = 0.64
MDE (80% power) = 0.59 pts = 5.9% relative
users per arm to detect +0.3 pts: 159,066
power at n=40,000 per arm if true lift = +0.3 pts: 0.29
```

**Follow-ups:**
- The manager says we do not have time. Then I decide on the cost: if it is cheap to reverse, ship with a monitored rollout and a holdout; if not, do not ship on this evidence.
- Can I just combine this with the next test? Only if they are the same design and population, with the pooling plan fixed in advance. Otherwise I am peeking.
- Where is this covered in theory? Book 1 Part 10, Q14 ("What do you do when the A/B test result is statistically insignificant? Can you conclude there is no effect?") and Q15 ("Statistical vs practical significance: how do you read the confidence interval of the lift and make a ship / no-ship call?").

**Common mistakes:**
- Saying "no effect" when the interval is wide.
- Reporting only the p-value.
- Planning the sample size after the test.
- Re-running until it becomes significant.

### Q6 ⭐⭐⭐ 🟢 A checkout redesign lifts conversion from 8.00% to 8.16% of visitors (+2% relative) while average order value among converters falls from 50.00 to 48.50 (-3% relative), and both changes are statistically significant. Explain how you decide whether to ship and which single metric you compute first.
**Asked at:** Guardrail and ship-decision material (a Dataford 'primary vs guardrail metrics' page, a Spotify Confidence guardrail-metric glossary and blog post, PracHub analytics-and-experimentation question pages, a Dataford 'non significant test PM wants launch' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I compute revenue per visitor (conversion x average order value) first, because the two significant moves pull in opposite directions and this one number nets them: here it falls about 1%, so I would not ship on the conversion win alone.

**Clarifying questions:**
- Is the goal revenue, profit or orders? A lower basket with higher conversion can still be good for profit or for lifetime value (more first-time buyers).
- What is the margin by order size, and are discounts or shipping fees part of AOV? Revenue per visitor can mislead if margin differs.
- Did the redesign change who completes checkout (for example, more small orders from marginal buyers)? That explains a falling AOV and is not a pure harm.
- What is the 30-60 day repeat rate for the extra converters? New buyers can be worth more later.
- Is there a pre-registered primary metric? It decides the ship rule.

**Approach:**
1. Combine the two metrics: revenue per visitor (RPV) = conversion x AOV = 8.16% x 48.50 = 3.9576 against 8.00% x 50.00 = 4.0000, so -1.06% (see Code). The +2% and -3% do not cancel: (1.02 x 0.97) - 1 = -1.06%.
2. Test RPV directly. Do not multiply two separate tests: RPV has its own variance, so I use a difference in means over all visitors (zeros included) with a robust or bootstrap interval, or the delta method.
3. Remember that AOV among converters is a post-treatment population: if the redesign changes who converts, the AOV comparison is not apples to apples. RPV, using all visitors, avoids that.
4. Go to profit and lifetime value: gross margin per visitor, and repeat purchase or retention of the extra buyers.
5. Look at the mechanism: did the new design cut high-value baskets (cross-sell removed), or add low-value buyers? Look at the order-value distribution by arm.
6. Decide: if RPV (or margin per visitor) is negative or not clearly positive, do not ship as is. Iterate: keep the conversion gain and restore the basket-building step.

**Metrics:**
- Revenue per visitor = total revenue / visitors assigned (zeros included).
- Conversion = buyers / visitors. AOV = revenue / orders (descriptive, post-treatment).
- Guardrails: refund rate, margin per order, repeat purchase in 30 days.

**Risks:**
- Averaging two significant results into a "mixed" story and picking the one I like.
- Treating AOV among converters as a causal effect when the converter population changed.
- Heavy tails: a few large orders dominate AOV and RPV.
- Revenue per visitor may be the wrong goal if profit or retention is.

**What the interviewer scores:**
- Strong: names one combined metric and computes it, with the correct relative arithmetic. Weak: "conversion is up, AOV is down, it is a trade-off."
- Strong: notes the AOV selection issue. Weak: treats AOV as clean.
- Strong: connects to margin and repeat behaviour before the final call. Weak: decides on revenue alone with no context.
- Strong: proposes a next iteration. Weak: stops at ship or do not ship.

**Example:** (illustrative numbers) 8.00% x 50.00 = 4.0000 per visitor. 8.16% x 48.50 = 3.9576 per visitor. That is -0.0424, or -1.06%. In a simulated test with 2,000,000 visitors per arm, conversion is up (z = 6.3) and AOV is down (z = -10.6), while RPV falls by about 0.9% with an interval that only just reaches zero (-0.069 to -0.000), which is why RPV needs its own test and often more data. Weak answer: "Conversion is significant, ship." Strong answer: "Net revenue per visitor is about -1%, so no ship until I see margin and repeat purchase."

**Code:**
```python
import numpy as np
rng = np.random.default_rng(21)

conv_c, conv_t = 0.0800, 0.0816
aov_c, aov_t = 50.00, 48.50
print("conversion relative change %:", round((conv_t / conv_c - 1) * 100, 2))
print("AOV relative change %:", round((aov_t / aov_c - 1) * 100, 2))
rpv_c, rpv_t = conv_c * aov_c, conv_t * aov_t
print(f"revenue per visitor: control {rpv_c:.4f}, treatment {rpv_t:.4f}, change {(rpv_t/rpv_c-1)*100:.2f}%")
assert round((conv_t / conv_c - 1) * 100, 2) == 2.0
assert round((aov_t / aov_c - 1) * 100, 2) == -3.0
assert round(rpv_t, 4) == 3.9576 and round((rpv_t / rpv_c - 1) * 100, 2) == -1.06

# Simulate a test: 2,000,000 visitors per arm, lognormal order values (sd about 40), with a fixed seed
n = 2_000_000
def arm(conv, aov, n):
    buy = rng.random(n) < conv
    sigma = 0.7
    mu = np.log(aov) - sigma ** 2 / 2
    val = np.where(buy, rng.lognormal(mu, sigma, n), 0.0)
    return buy, val
bc, vc = arm(conv_c, aov_c, n)
bt, vt = arm(conv_t, aov_t, n)

def diff_ci(a, b):
    d = b.mean() - a.mean()
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    return d, d - 1.96 * se, d + 1.96 * se, d / se
d, lo, hi, z = diff_ci(bc.astype(float), bt.astype(float))
print(f"conversion diff {d*100:.3f} pts, z = {z:.2f}")
assert z > 1.96
d, lo, hi, z = diff_ci(vc[bc], vt[bt])
print(f"AOV diff {d:.2f}, z = {z:.2f}")
assert z < -1.96
d, lo, hi, z = diff_ci(vc, vt)
print(f"revenue per visitor diff {d:.3f} (95% CI {lo:.3f} to {hi:.3f}), z = {z:.2f}")
rel = d / vc.mean()
print(f"relative change in revenue per visitor: {rel*100:.2f}%")
assert d < 0 and -0.03 < rel < 0.0
```

**Output (my run):**
```text
conversion relative change %: 2.0
AOV relative change %: -3.0
revenue per visitor: control 4.0000, treatment 3.9576, change -1.06%
conversion diff 0.171 pts, z = 6.28
AOV diff -1.47, z = -10.58
revenue per visitor diff -0.034 (95% CI -0.069 to -0.000), z = -1.96
relative change in revenue per visitor: -0.86%
```

**Follow-ups:**
- What if margin is higher on small baskets? Then margin per visitor, not revenue, is the metric. Compute it and decide on that.
- What if the extra buyers come back more often? Then the 30-60 day value can offset the lower basket. I would hold a long-term holdout and re-read at 60 days.
- Where is this covered in theory? Book 1 Part 10, Q13 ("The test shows the primary metric up but revenue (or a guardrail) down or flat. How do you interpret and decide?").

**Common mistakes:**
- Adding +2% and -3% to get -1% (close, but the product is -1.06% and the correct method is the product).
- Testing AOV among converters and treating it as an unbiased effect.
- Looking at revenue per order instead of per visitor.
- Ignoring margin and repeat purchase.

### Q7 ⭐⭐⭐ 🟡 A feed ranking test raises sessions per user by 1.5% (relative to control) but also raises 95th-percentile page-load time from 1.00 to 1.08 seconds (8% relative), and the latency change is significant. The team's pre-registered rule allows at most a 5% relative degradation on that guardrail. Explain what you recommend and what you look at beyond the rule.
**Asked at:** Guardrail and ship-decision material (a Dataford 'primary vs guardrail metrics' page, a Spotify Confidence guardrail-metric glossary and blog post, PracHub analytics-and-experimentation question pages, a Dataford 'non significant test PM wants launch' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would not ship as it stands, because the 8% p95 slowdown breaks the pre-registered 5% limit and the whole interval is beyond it; the +1.5% sessions is a real gain, so I would send it back to fix latency and then re-test.

**Clarifying questions:**
- Is the 5% rule a hard stop or a trigger for review? The team wrote it as an allowed limit, so I treat a breach as a stop unless a named owner waives it.
- Where does the extra latency come from (model inference, a feature fetch, more items)? If it is fixable, the answer is "fix and retest," not "kill."
- Is the slowdown the same for all users or concentrated on slow devices and networks? Averages hide the users who suffer most.
- Do we have evidence that latency hurts retention or conversion in this product? That turns an engineering number into a business cost.
- Is the +1.5% sessions lift stable across weeks (novelty), and is it in the segments that matter? A fading lift would make the trade worse.

**Approach:**
1. Apply the rule: 1.08 / 1.00 - 1 = +8%, above the 5% limit (see Code). The rule was agreed before the test, so a breach is a no-ship signal, not a negotiation after seeing the win.
2. Check the breach is real, not noise: a bootstrap interval for the relative p95 change (about 8.0% to 9.4% in the illustrative data) lies wholly above 5%. If the interval had straddled 5%, I would say "inconclusive" and collect more data.
3. Look beyond the rule: latency by device class, region, network and page type, and the tail (p99), plus the median. A small median change with a big tail is a different problem than a uniform slowdown.
4. Look at downstream effects the latency might cause: bounce, session length, conversion, and retention in the slowest decile.
5. Estimate the trade: sessions +1.5% is the benefit; the cost is user experience and infrastructure. Ask: does the benefit hold for the users who see slower pages?
6. Recommend: do not launch to everyone. Optimise (cache, smaller model, fewer items, lazy loading) to get back under 5%, then re-run, or ship to a subset with a fast path, with a holdout and a reviewed waiver if the business wants to override.

**Metrics:**
- Guardrail: p95 page-load time, relative change = p95 treatment / p95 control - 1, with a bootstrap 95% CI. Limit +5%.
- Primary: sessions per user = sessions / assigned users, relative lift.
- Secondary: p50 and p99 latency, error rate, bounce, 7-day retention.

**Risks:**
- Waiving the rule because the gain looks good teaches the team that guardrails are optional.
- Percentiles are noisy; the p95 of one arm has its own sampling error, so I use a bootstrap.
- Averages across devices hide a severe slowdown on cheap phones.
- The sessions gain may be partly caused by the slowness (more page loads per task), which would make it a false win.

**What the interviewer scores:**
- Strong: applies the pre-registered rule with the right arithmetic (8% against 5%). Weak: "it is a trade-off, sessions are up."
- Strong: checks the interval, segments and tail rather than only the point estimate. Weak: only reads the p95.
- Strong: proposes a path (fix latency and re-test, or a staged rollout with a holdout). Weak: a flat yes or no.
- Strong: asks if more sessions means more value or more friction. Weak: treats sessions as pure good.

**Example:** (illustrative numbers) p95 goes from 1.00 s to 1.08 s: +8% against a 5% limit. In a simulated sample of 200,000 requests per arm, the bootstrap interval for the relative change is 8.0% to 9.4%, so even the lower end is above 5%. Sessions per user are up 1.5%, but if the slowest tenth of users lose retention, the net can be negative. Weak answer: "1.5% more sessions, ship." Strong answer: "The breach is real. Fix latency, check the slow-device users, re-test."

**Code:**
```python
import numpy as np
rng = np.random.default_rng(31)

base, new = 1.00, 1.08
print("relative p95 degradation (%):", round((new / base - 1) * 100, 1), "vs allowed 5%")
assert round((new / base - 1) * 100, 1) == 8.0

# Illustrative latency data: lognormal, p95 of control = 1.00 s; treatment is 8% slower at every quantile
sigma = 0.5
z95 = 1.6449
mu_c = np.log(1.0) - sigma * z95
n = 200_000
ctrl = rng.lognormal(mu_c, sigma, n)
treat = rng.lognormal(mu_c + np.log(1.08), sigma, n)
p95c, p95t = np.percentile(ctrl, 95), np.percentile(treat, 95)
print(f"sample p95: control {p95c:.3f}, treatment {p95t:.3f}, ratio {p95t/p95c:.3f}")

# Bootstrap CI for the relative p95 degradation (200 resamples)
B = 200
ratios = np.empty(B)
for b in range(B):
    ic = rng.integers(0, n, n); it = rng.integers(0, n, n)
    ratios[b] = np.percentile(treat[it], 95) / np.percentile(ctrl[ic], 95) - 1
lo, hi = np.percentile(ratios, [2.5, 97.5])
print(f"bootstrap 95% CI for relative p95 change: {lo*100:.1f}% to {hi*100:.1f}%")
assert lo > 0.05              # the whole interval is beyond the 5% limit
print("breach of the 5% limit is clear:", lo > 0.05)
```

**Output (my run):**
```text
relative p95 degradation (%): 8.0 vs allowed 5%
sample p95: control 0.999, treatment 1.085, ratio 1.087
bootstrap 95% CI for relative p95 change: 8.0% to 9.4%
breach of the 5% limit is clear: True
```

**Follow-ups:**
- What if the latency increase was 4%? Under the rule, it passes, but I would still check the interval and the slowest segments, because the rule is a floor for my judgement.
- What if the team wants a waiver? A named owner decides in writing, with a rollout plan and a holdout so that the long-term cost is measured.
- Where is this covered in theory? Book 1 Part 10, Q3 ("How do you choose the primary metric, guardrail metrics and secondary metrics for an experiment? Give an example.").

**Common mistakes:**
- Treating a guardrail breach as a failed test instead of a decision with an agreed rule.
- Quoting the mean latency when the rule is on p95.
- Ignoring uncertainty on a percentile.
- Overriding the rule after seeing the win.

### Q8 ⭐⭐⭐ 🟡 A team measures click-through rate as total clicks divided by total impressions and runs a two-proportion z-test over 2,000,000 impressions per arm, getting p = 0.01 for a lift from 4.00% to 4.05%. Those impressions come from only 100,000 users per arm (20 per user on average), and the user-level analysis gives p = 0.12. Explain why the two disagree and how you would analyse the metric properly.
**Asked at:** Ratio-metric, delta-method and variance-reduction material (Spotify Confidence ratio-metric RFP and variance-reduction docs, MetricGate CUPED and delta-method pages, a TechPrep '66 Variance Reduction Interview Questions' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The two tests disagree because the impression-level test treats 2,000,000 correlated impressions as independent, when the real independent units are the 100,000 users; I would analyse at user level (or with the delta method), and trust the p = 0.12.

**Clarifying questions:**
- Was users, not impressions, the randomization unit? If yes, the analysis unit must be users. It is the whole answer.
- Do impressions per user vary a lot (a few heavy users)? Heavy users dominate a pooled ratio and make the variance bigger.
- Is "click-through rate" meant as clicks per impression or the share of users who click? They are different metrics with different decisions.
- Do users see the same item repeatedly (so impressions are even more correlated)? It raises the design effect.
- Is there a pre-registered metric definition? It prevents choosing the test that gives the lower p.

**Approach:**
1. Name the problem: pseudo-replication. The same user's 20 impressions share the user's taste, so they are not 20 independent draws. The effective sample is closer to 100,000 than 2,000,000.
2. Measure the inflation: with intra-user correlation rho and 20 impressions per user, the variance inflates by the design effect 1 + (m - 1) x rho. A user-level p of 0.12 against a pooled p of 0.011 implies a design effect of about 2.7 (rho about 0.09), see Code.
3. Prove it with an A/A simulation: with this correlation, the impression-level test rejects at 5% about 22% of the time on pure noise, while the user-level test rejects about 5%.
4. Do the right analysis. For equal impressions per user, a t-test on per-user CTR is fine. With unequal impressions, the metric is a ratio of sums, so use the delta method (linearise the ratio: residual = clicks - R x impressions, then take the variance across users) or a user-level bootstrap.
5. Report the estimate with an interval at the user level, and call the +0.05-point lift "not distinguishable from zero," not "proven."
6. If a smaller lift matters, plan a bigger or longer test or use variance reduction (CUPED).

**Metrics:**
- Ratio CTR = total clicks / total impressions, compared with the delta method: Var(R) about = Var(click_i - R x imp_i) / (n x mean_imp^2), per arm.
- User-level CTR = mean over users of clicks_i / impressions_i (an alternative metric that weights users equally).
- Design effect = 1 + (m - 1) x rho. Guardrail: A/A false-positive rate near 5%.

**Risks:**
- Picking the pooled test because it gives the smaller p-value.
- Mixing the two definitions (ratio of sums versus mean of ratios) between the planning and the readout.
- Heavy users dominating the ratio.
- Assuming that 2,000,000 observations is power; it is not.

**What the interviewer scores:**
- Strong: names the unit-of-analysis mismatch and the design effect. Weak: "bigger sample, smaller p."
- Strong: gives a fix (user-level test or delta method) with how the variance is built. Weak: "use a different test."
- Strong: checks with an A/A or simulation. Weak: argues from theory only.
- Strong: concludes honestly (not significant). Weak: reports both p-values as equally valid.

**Example:** (illustrative numbers) 100,000 users per arm, 20 impressions each. Control 4.00%, treatment 4.05%: the pooled z-test gives z = 2.54, p = 0.011. A user-level p of 0.12 means z = 1.55, so the variance is (2.54 / 1.55)^2 = 2.7 times larger than the pooled test assumed. With rho = 0.09, that matches 1 + 19 x 0.088. Weak answer: "p = 0.01 on two million rows, ship it." Strong answer: "The pooled test pretends that impressions are independent. At user level, it is not significant."

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(8)

# 1) The prompt's pooled (per-impression) z-test, recomputed
N = 2_000_000
pc, pt = 0.0400, 0.0405
pool = (pc + pt) / 2
se = np.sqrt(pool * (1 - pool) * 2 / N)
z = (pt - pc) / se
p_naive = 2 * stats.norm.sf(z)
print(f"pooled impression-level z = {z:.2f}, p = {p_naive:.4f}")
assert round(p_naive, 2) == 0.01 and round(z, 2) == 2.54 

# 2) Back out the design effect implied by the user-level p = 0.12
z_user = stats.norm.isf(0.12 / 2)
deff = (z / z_user) ** 2
m = 20
rho = (deff - 1) / (m - 1)
print(f"user-level z for p = 0.12: {z_user:.2f}; implied design effect = {deff:.2f}; implied intra-user correlation = {rho:.3f}")

# 3) A/A simulation (no true effect): 20 impressions per user, user CTRs vary (Beta, mean 4%),
#    intra-user correlation as implied above. 20,000 users per arm, 1,000 experiments.
users, m, sims = 20_000, 20, 1_000
ab = 1 / rho - 1                      # Beta(a, b) with icc = 1 / (a + b + 1)
a_, b_ = 0.04 * ab, 0.96 * ab
rej_naive = rej_user = 0
for _ in range(sims):
    cc = rng.binomial(m, rng.beta(a_, b_, users))
    ct = rng.binomial(m, rng.beta(a_, b_, users))
    Nn = users * m
    xc, xt = cc.sum(), ct.sum()
    pl = (xc + xt) / (2 * Nn)
    zn = (xt / Nn - xc / Nn) / np.sqrt(pl * (1 - pl) * 2 / Nn)
    zu = (ct.mean() - cc.mean()) / np.sqrt(ct.var(ddof=1) / users + cc.var(ddof=1) / users)
    rej_naive += abs(zn) > 1.96
    rej_user += abs(zu) > 1.96
print(f"A/A false-positive rate: impression-level z-test = {rej_naive/sims:.3f}; user-level test = {rej_user/sims:.3f}")
assert rej_naive / sims > 0.15 and 0.03 < rej_user / sims < 0.08

# 4) Delta-method test for the ratio when impressions per user differ (one realistic data set)
users = 100_000
def make(mean):
    imp = rng.poisson(20, users).clip(1)
    ctr = rng.beta(mean * ab, (1 - mean) * ab, users)
    return rng.binomial(imp, ctr), imp
clk_c, imp_c = make(0.0400); clk_t, imp_t = make(0.0405)
def ratio_var(clk, imp):
    r = clk.sum() / imp.sum()
    resid = clk - r * imp
    return r, resid.var(ddof=1) / (len(clk) * imp.mean() ** 2)
r_c, v_c = ratio_var(clk_c, imp_c); r_t, v_t = ratio_var(clk_t, imp_t)
zd = (r_t - r_c) / np.sqrt(v_c + v_t)
Nc, Nt = imp_c.sum(), imp_t.sum()
pl = (clk_c.sum() + clk_t.sum()) / (Nc + Nt)
zn = (r_t - r_c) / np.sqrt(pl * (1 - pl) * (1 / Nc + 1 / Nt))
print(f"same data: impression-level z = {zn:.2f}, delta-method z = {zd:.2f}")
assert abs(zn) > abs(zd)
```

**Output (my run):**
```text
pooled impression-level z = 2.54, p = 0.0110
user-level z for p = 0.12: 1.55; implied design effect = 2.68; implied intra-user correlation = 0.088
A/A false-positive rate: impression-level z-test = 0.219; user-level test = 0.053
same data: impression-level z = 1.48, delta-method z = 0.89
```

**Follow-ups:**
- Why not just cluster the standard errors? That is the same idea: cluster-robust standard errors at user level give the same answer as the delta method for a ratio. I use whichever my platform supports.
- Which metric should I use, ratio or mean of user CTRs? Decide before the test. The ratio is closer to "of all impressions, how many were clicked." The mean of ratios treats each user the same. Both are valid when analysed at the user level.
- Where is this covered in theory? Book 1 Part 10, Q27 ("Ratio metrics (CTR, revenue per session) and per-session vs per-user analysis: what goes wrong with the variance and how do you fix it (delta method)?").

**Common mistakes:**
- Using impressions as the sample size when users were randomised.
- Computing a per-user CTR but a ratio-of-sums variance (mixing the two).
- Treating a small p-value on millions of rows as strong evidence.
- Dropping heavy users to make the test pass.

### Q9 ⭐⭐⭐ 🟡 A teammate says that because a user's pre-experiment spend has a correlation of 0.7 with their in-experiment spend, CUPED will cut the required sample size by 70%, and the test currently needs 100,000 users per arm. Explain whether the claim is right, what reduction you expect, and how you would choose and validate the covariate.
**Asked at:** Ratio-metric, delta-method and variance-reduction material (Spotify Confidence ratio-metric RFP and variance-reduction docs, MetricGate CUPED and delta-method pages, a TechPrep '66 Variance Reduction Interview Questions' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The claim is wrong: CUPED (adjusting the metric with a pre-experiment covariate) cuts the variance by the correlation squared, so a correlation of 0.7 cuts variance by 49% and the sample from 100,000 to about 51,000 per arm, not to 30,000.

**Clarifying questions:**
- How long is the pre-period and is it the same metric as the outcome? A longer pre-period of the same metric usually gives the highest correlation.
- What share of users have no pre-period history (new users)? They get no variance reduction, so the real gain is smaller.
- Is the 0.7 correlation measured at the user level on a past period, or a guess? I want to measure it on the same population.
- Is the covariate fixed before assignment? Anything measured after treatment starts can be affected by treatment and bias the result.
- Is the metric heavy-tailed? Heavy tails reduce the usable correlation and may need capping first.

**Approach:**
1. Do the arithmetic: the adjusted variance is Var(Y) x (1 - rho^2) = 0.51 x Var(Y). Sample size is proportional to variance, so 100,000 x 0.51 = 51,000 per arm. The reduction is 49%, not 70% (see Code). The standard error falls by sqrt(0.51) = 0.714, which is a 29% reduction, and this might be where "70%" came from.
2. Choose the covariate: pre-experiment data only, ideally the same metric over a pre-period of similar length; a combination of a few pre-period metrics is fine (regression adjustment).
3. Estimate theta = Cov(X, Y) / Var(X) on the pooled data from both arms (not separately per arm). The adjusted outcome is Y - theta x (X - mean of X).
4. Validate: (a) the covariate is balanced between arms (it should be, since it is pre-assignment); (b) the adjusted effect estimate is close to the raw one (CUPED is unbiased; only the standard error shrinks); (c) an A/A test on past data gives a false-positive rate near 5%; (d) the variance ratio matches 1 - rho^2.
5. Handle users with no history: set X to the mean and add a missing flag, or leave them unadjusted.
6. Plan with the realistic correlation: sample size = raw sample size x (1 - rho^2) for the share of users with history, and keep a buffer.

**Metrics:**
- Variance reduction = 1 - Var(Y_adj) / Var(Y) = rho^2 (for one covariate).
- Required sample (relative) = 1 - rho^2.
- Guardrail: |raw effect - adjusted effect| small compared with the standard error; the A/A false-positive rate near 5%.

**Risks:**
- A post-treatment covariate (for example in-experiment sessions) is affected by treatment and biases the effect (see Code: the estimate is badly wrong).
- Correlation measured on a different population or period than the test.
- New users or a recent change in tracking break the pre-period.
- Stating a sample-size cut as a guarantee before measuring rho.

**What the interviewer scores:**
- Strong: gives 1 - rho^2 and the right number (51,000). Weak: "70%."
- Strong: distinguishes variance, standard error and sample size. Weak: mixes them up.
- Strong: names the pre-experiment rule and a check for a bad covariate. Weak: "just add any correlated variable."
- Strong: notes that the point estimate stays unbiased and only the interval narrows. Weak: expects the effect to change.

**Example:** (illustrative numbers) rho = 0.7, so variance x 0.51, sample size 51,000 per arm instead of 100,000, a 49% cut. In a simulation with 200,000 users, theta = 0.700, the variance ratio is 0.511, the standard error falls from 0.089 to 0.064 (ratio 0.714 = sqrt(0.51)), and the effect estimate stays at about 0.55 either way. A covariate that moves with treatment gave an effect of -9.6 against a true +0.5. Weak answer: "70% smaller." Strong answer: "1 - 0.49 = 0.51, so about half the users, and only for users with history."

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(9)

rho = 0.7
print("variance after CUPED = (1 - rho^2) =", round(1 - rho ** 2, 2), "-> sample size needed:", int(100_000 * (1 - rho ** 2)), "per arm")
assert round(1 - rho ** 2, 2) == 0.51
assert int(100_000 * (1 - rho ** 2)) == 51_000
print("claim '70% fewer users' would mean 30,000 per arm; the formula says 51,000")

# Simulate: pre-period spend X, in-period spend Y with correlation 0.7, treatment effect +0.5
n = 200_000
cov = [[1.0, rho], [rho, 1.0]]
xy = rng.multivariate_normal([0, 0], cov, n)
x = xy[:, 0] * 20 + 100            # pre-experiment spend
y = xy[:, 1] * 20 + 100            # in-experiment spend (control behaviour)
treat = rng.random(n) < 0.5
y = y + 0.5 * treat                # true effect +0.5

# CUPED: theta from pooled data, adjust Y
theta = np.cov(x, y)[0, 1] / x.var(ddof=1)
y_adj = y - theta * (x - x.mean())
print(f"theta = {theta:.3f} (expected {rho:.3f})")
var_ratio = y_adj.var(ddof=1) / y.var(ddof=1)
print(f"variance ratio after / before = {var_ratio:.3f}")
assert abs(var_ratio - 0.51) < 0.02

def effect(v):
    d = v[treat].mean() - v[~treat].mean()
    se = np.sqrt(v[treat].var(ddof=1) / treat.sum() + v[~treat].var(ddof=1) / (~treat).sum())
    return d, se
d0, se0 = effect(y); d1, se1 = effect(y_adj)
print(f"raw: effect {d0:.3f} se {se0:.3f} | CUPED: effect {d1:.3f} se {se1:.3f}")
print(f"se ratio = {se1/se0:.3f} (sqrt of 0.51 = {np.sqrt(0.51):.3f})")
assert abs(se1 / se0 - np.sqrt(0.51)) < 0.02
print(f"sample size ratio (se ratio squared) = {(se1/se0)**2:.3f}")

# Bad covariate: a post-treatment variable (e.g. in-experiment sessions affected by treatment) biases the effect
m = 0.8 * (y - 100) / 20 + 0.6 * treat + rng.standard_normal(n) * 0.5     # moves with treatment
th = np.cov(m, y)[0, 1] / m.var(ddof=1)
y_bad = y - th * (m - m.mean())
db, _ = effect(y_bad)
print(f"post-treatment covariate: estimated effect = {db:.3f} (true 0.5)")
assert abs(db - 0.5) > 0.3
```

**Output (my run):**
```text
variance after CUPED = (1 - rho^2) = 0.51 -> sample size needed: 51000 per arm
claim '70% fewer users' would mean 30,000 per arm; the formula says 51,000
theta = 0.700 (expected 0.700)
variance ratio after / before = 0.511
raw: effect 0.550 se 0.089 | CUPED: effect 0.549 se 0.064
se ratio = 0.714 (sqrt of 0.51 = 0.714)
sample size ratio (se ratio squared) = 0.510
post-treatment covariate: estimated effect = -9.602 (true 0.5)
```

**Follow-ups:**
- Can CUPED ever give more than a 49% cut at rho 0.7? With several covariates, the R-squared of the regression replaces rho squared, so a richer model can do better.
- Does CUPED change what I conclude? Only the width of the interval. If raw and adjusted effects differ a lot, I suspect a bad covariate or an imbalance.
- Where is this covered in theory? Book 1 Part 14, Q15 ("Explain CUPED: what does it do, what is the formula, why is it unbiased, and how much variance does it remove?") and Q33 ("How do you choose a CUPED covariate? Why must it be pre-experiment, what happens with new users who have no history, and does CUPED work with ratio metrics?"). Book 1 Part 10 only points to CUPED in passing.

**Common mistakes:**
- Mixing up rho (correlation) with rho squared.
- Using a covariate measured during the experiment.
- Estimating theta separately in each arm.
- Promising the sample-size cut before looking at the actual correlation.

### Q10 ⭐⭐⭐ 🟡 In a test with 10,000 users per arm, control has 8,000 web users converting at 10% and 2,000 mobile users converting at 4%, while treatment has 2,000 web users converting at 11% and 8,000 mobile users converting at 5%. Overall conversion is 8.8% in control and 6.2% in treatment, so treatment loses overall although it wins in both segments. Explain what happened and what it says about the randomization.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** This is Simpson's paradox caused by a broken randomization: treatment got 20% web users and control got 80%, so the overall numbers compare different mixes, and the randomization failed.

**Clarifying questions:**
- How is platform defined and when is it recorded (at assignment, or after the user acts)? If the experience changes which platform is recorded, the segment is post-treatment.
- Was assignment supposed to be random at user level, or did the feature roll out by platform or app version? A staged rollout would produce this split by design.
- Did users switch platform, or are users counted per device? Cross-device users can be counted in both arms.
- Did the assignment service work on both platforms (a client bug on web)? A one-platform bug gives a mix gap.
- Do the within-platform effects hold across weeks? It tells me if the segment story is stable.

**Approach:**
1. Check the randomization: with fair assignment the platform mix must be the same in both arms (about 50% web in each). Here it is 80% against 20%: chi-square = 7,200 (see Code). That cannot happen by chance, even over 100,000 repeats of a fair draw the web share never moves more than about 2 points from 50%.
2. Explain the paradox: the overall rate is a mix-weighted average. Web converts at about 10% and mobile at 4%, so an arm with more mobile users has a lower overall rate even if each segment improves.
3. Read the segment results as the real signal, with a caveat: within each platform treatment is higher (11% against 10%, 5% against 4%). If the assignment within a platform is still random, this is the valid comparison.
4. Report a standardised result: apply the same platform mix (50/50) to both arms: control 7.0%, treatment 8.0%, a lift of 1.0 point.
5. Find the cause: platform-specific assignment bug, a staged rollout, a redirect or crash that drops users on one platform in one arm, or a sticky-bucket issue. Fix it and re-run.
6. Do not ship on the standardised number alone: if the assignment is not random, even within a platform the comparison can be confounded. The honest outcome is "directionally positive, not trustworthy, re-run."

**Metrics:**
- Conversion = converting users / assigned users, by arm and by platform.
- Randomization check: chi-square of platform mix by arm (expected equal), plus SRM by segment.
- Standardised lift = sum over platforms of (reference share x segment lift).

**Risks:**
- Picking the aggregate (a loss) or the segment (a win) depending on which story one prefers.
- Segment results are also compromised if the cause of the imbalance is related to the outcome.
- Many segment cuts raise false positives. Platform is a natural one to pre-register.
- Standardisation can hide interaction (web and mobile effects differ).

**What the interviewer scores:**
- Strong: checks the arm composition first and calls the randomization broken. Weak: "Simpson's paradox, trust the segments."
- Strong: explains the paradox arithmetically (weighted averages with different weights). Weak: only names it.
- Strong: gives a standardised estimate and a fix plan. Weak: no plan.
- Strong: is clear that a broken assignment limits what we can claim. Weak: ships on either number.

**Example:** (illustrative numbers) Control: 8,000 x 10% + 2,000 x 4% = 880 converters out of 10,000, so 8.8%. Treatment: 2,000 x 11% + 8,000 x 5% = 620 out of 10,000, so 6.2%. Treatment wins in each segment (+1 point on both), but with the same 50/50 mix it would be 7.0% against 8.0%. Weak answer: "Treatment loses overall, do not ship." Strong answer: "The arms have different platform mixes, so the test is broken. Fix assignment and re-run."

**Code:**
```python
import numpy as np
from scipy import stats

web_c, mob_c = 8_000, 2_000
web_t, mob_t = 2_000, 8_000
rc_web, rc_mob = 0.10, 0.04
rt_web, rt_mob = 0.11, 0.05
conv_c = (web_c * rc_web + mob_c * rc_mob) / (web_c + mob_c)
conv_t = (web_t * rt_web + mob_t * rt_mob) / (web_t + mob_t)
print(f"overall conversion: control {conv_c:.3%}, treatment {conv_t:.3%}")
assert round(conv_c * 100, 1) == 8.8 and round(conv_t * 100, 1) == 6.2
assert rt_web > rc_web and rt_mob > rc_mob       # treatment wins in each segment

# Randomization check: platform mix by arm (should be the same under random assignment)
table = np.array([[web_c, mob_c], [web_t, mob_t]])
chi2, p, dof, _ = stats.chi2_contingency(table, correction=False)
print(f"platform-by-arm chi2 = {chi2:.0f}, p = {p:.1e}")
assert p < 1e-100

# Standardised comparison: apply the pooled platform mix (50/50) to both arms
mix_web = (web_c + web_t) / 20_000
std_c = mix_web * rc_web + (1 - mix_web) * rc_mob
std_t = mix_web * rt_web + (1 - mix_web) * rt_mob
print(f"standardised (50/50 mix): control {std_c:.2%}, treatment {std_t:.2%}, lift {(std_t-std_c)*100:.1f} pts")
assert round((std_t - std_c) * 100, 1) == 1.0

# Under proper randomization, how often would the mix differ even a little? (web share 80% vs 20% is impossible)
rng = np.random.default_rng(10)
shares = rng.binomial(10_000, 0.5, 100_000) / 10_000
print("max |web share - 50%| in 100,000 fair randomizations:", round(np.abs(shares - 0.5).max(), 4))
assert np.abs(shares - 0.5).max() < 0.03
print("observed web share: control 80%, treatment 20%")
```

**Output (my run):**
```text
overall conversion: control 8.800%, treatment 6.200%
platform-by-arm chi2 = 7200, p = 0.0e+00
standardised (50/50 mix): control 7.00%, treatment 8.00%, lift 1.0 pts
max |web share - 50%| in 100,000 fair randomizations: 0.0212
observed web share: control 80%, treatment 20%
```

**Follow-ups:**
- Could a legitimate test produce this? Only if the segment is affected by treatment (for example the feature makes users move to mobile) or assignment was stratified differently by design. Then the segment is post-treatment, and the right metric is the overall one.
- Which number would I report if forced? The standardised one, with the warning that it assumes random assignment within platform.
- Where is this covered in theory? Book 1 Part 10, Q10 ("What is Simpson's paradox? Give an A/B-test example where the variant wins overall but loses in every segment.").

**Common mistakes:**
- Choosing between aggregate and segment without checking the mix.
- Treating the mix gap as a coincidence.
- Reweighting and shipping without fixing assignment.
- Confusing this with the normal case where a bigger overall effect is hidden by a mix (no randomization failure).

### Q11 ⭐⭐⭐ 🟡 A messaging app tested a group-invite feature by randomizing 1,000,000 users 50/50, and treated users sent 20.6 invites per user against 20.0 for control (+3% relative to control). Control users who are friends with treated users also joined more groups. Explain what bias this creates, which way it pushes the measured lift, and how you would redesign the test.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** This is interference (users affect each other), and because the spillover into control is positive, the measured +3% lift understates what launching to everyone would deliver, so I would redesign the test with friend-group clusters instead of random users.

**Clarifying questions:**
- How dense is the friend graph, and does it form communities? Dense, clustered graphs make user-level randomization badly contaminated and make clusters possible.
- Is the target the effect of launching to everyone (the global effect) or the effect on one user who gets it? Interference makes these two different numbers.
- Is the spillover positive for the outcome (more invites for friends) or zero-sum (competition for attention)? The sign decides the direction of the bias.
- Which metric moves in control, invites sent or groups joined? The prompt shows control joining more groups, which is an indirect channel.
- How many clusters can we form, and how big are they? It sets the power cost of cluster randomization.

**Approach:**
1. Name the violation: the test assumes one user's outcome does not depend on others' assignments (no interference, SUTVA). Here control users get more invites and join more groups because their friends are treated.
2. Say which way it pushes: with a positive spillover, the control group is lifted by treated friends, so treated minus control understates the gap between a world with the feature and a world without it. In the stylised model below (direct effect +0.6, spillover +0.5 from a fully treated friend group) the user-level test shows +0.61 (3.0%), while launching to everyone would give +1.10 (5.6% of the nobody-treated baseline of 19.75).
3. Note the caveat: if the spillover were competitive (treated users take attention from control), the bias would run the other way and the test would overstate the effect. The sign of the spillover must be measured, not assumed.
4. Redesign: randomize by cluster. Build friend-graph communities (graph clustering), assign whole clusters to treatment or control, and analyse at the cluster level or with cluster-robust errors. In the model, the cluster design measures +1.05 against the global effect of +1.10.
5. Pay for it with power: cluster randomization inflates variance by about 1 + (m - 1) x rho (for 50-user clusters with an intra-cluster correlation of 0.05, 3.45 times), so plan a bigger sample or fewer, larger clusters with less leakage, or geographic or ego-network designs.
6. Measure spillover directly: compare control users by how many treated friends they have (exposure mapping) as a diagnostic, and check that boundary users do not dominate.

**Metrics:**
- Primary: invites per user = invites sent / users in the arm, compared at the cluster level.
- Exposure: share of a user's friends who are treated (0 to 1). Spillover estimate = control outcome at high exposure minus control outcome at low exposure.
- Cluster quality: share of friend ties that stay inside a cluster (leakage = share crossing clusters).
- Guardrails: spam and block rates for invites, notifications per user.

**Risks:**
- Cluster randomization loses power: fewer independent units and a design effect above 1.
- Leakage across cluster borders keeps some contamination.
- The user-level estimate is not "wrong," it answers a different question (direct effect with mixed exposure).
- Network effects can also be long-run (the feature changes how groups form), which a short test misses.

**What the interviewer scores:**
- Strong: states the direction of the bias with a reason and the conditions for the reverse. Weak: "it is biased."
- Strong: separates the direct effect from the total (global) effect. Weak: treats the A/B difference as the launch effect.
- Strong: proposes cluster randomization and prices the power cost. Weak: says "use more users."
- Strong: suggests a way to measure spillover (exposure by friend share). Weak: no diagnostic.

**Example:** (illustrative numbers) A stylised graph: direct effect +0.6 invites per user, spillover +0.5 when all friends are treated, 90% of ties inside a 50-person community. User-level 50/50: control 20.00, treated 20.61, lift +0.61 (+3.0%). The baseline with nobody treated is 19.75, so control is already lifted by 0.25. Launching to all gives +1.10 (+5.6%). Cluster randomization measures +1.05. Weak answer: "3% lift, ship, the rest is noise." Strong answer: "3% understates the launch effect when spillover is positive. Cluster the test and measure exposure."

**Prompt note (Q11):** the prompt gives the lift in invites per user (20.6 against 20.0) but the spillover evidence in control as "joined more groups." Those are different outcomes. The direction argument above needs the spillover to raise the same outcome (control invites), so I state that assumption in the answer. Nothing in the numbers is wrong.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(11)

# Illustrative model: outcome (invites per user) = B + d * own_treated + s * share_of_friends_treated
d, s = 0.6, 0.5                       # direct effect, spillover from fully treated friend group
n_comm, size = 4_000, 50              # 200,000 users in 4,000 friend communities of 50
within = 0.9                          # 90% of friend ties are inside the community
k = 10                                # friends per user

comm = np.repeat(np.arange(n_comm), size)
N = n_comm * size
def friend_share_treated(T):
    # expected share treated among friends = within * (community mean of T, excluding self approx) + (1-within) * overall mean
    cm = T.reshape(n_comm, size).mean(axis=1)
    cm_user = np.repeat(cm, size)
    return within * cm_user + (1 - within) * T.mean()

# Design 1: user-level 50/50
T1 = (rng.random(N) < 0.5).astype(float)
e1 = friend_share_treated(T1)
# Design 2: community-level 50/50 (cluster randomization)
tc = (rng.random(n_comm) < 0.5).astype(float)
T2 = np.repeat(tc, size)
e2 = friend_share_treated(T2)

# Pure baseline B so that the observed control mean is 20.0 under user-level design
B = 20.0 - s * e1[T1 == 0].mean()
def outcome(T, e): return B + d * T + s * e
y1 = outcome(T1, e1); y2 = outcome(T2, e2)
m1 = y1[T1 == 1].mean() - y1[T1 == 0].mean()
m2 = y2[T2 == 1].mean() - y2[T2 == 0].mean()
global_effect = (B + d + s) - B          # everyone treated vs nobody treated
print(f"baseline with nobody treated B = {B:.2f}; control mean in user-level test = {y1[T1==0].mean():.2f}; treated mean = {y1[T1==1].mean():.2f}")
print(f"user-level measured lift = {m1:.2f} ({m1/y1[T1==0].mean()*100:.1f}% of control)")
print(f"cluster-level measured lift = {m2:.2f}")
print(f"true effect of launching to everyone = {global_effect:.2f} ({global_effect/B*100:.1f}% of baseline)")
assert abs(m1 - 0.6) < 0.05
assert m2 > m1 and m2 < global_effect + 0.01
assert abs(y1[T1 == 0].mean() - 20.0) < 1e-9 and abs(y1[T1 == 1].mean() - 20.6) < 0.05

# Variance cost of cluster randomization: design effect = 1 + (m - 1) * icc
for icc in (0.01, 0.05, 0.1):
    print(f"cluster size {size}, intra-cluster correlation {icc}: design effect = {1 + (size - 1) * icc:.2f}")
assert abs((1 + 49 * 0.05) - 3.45) < 1e-9
```

**Output (my run):**
```text
baseline with nobody treated B = 19.75; control mean in user-level test = 20.00; treated mean = 20.61
user-level measured lift = 0.61 (3.0% of control)
cluster-level measured lift = 1.05
true effect of launching to everyone = 1.10 (5.6% of baseline)
cluster size 50, intra-cluster correlation 0.01: design effect = 1.49
cluster size 50, intra-cluster correlation 0.05: design effect = 3.45
cluster size 50, intra-cluster correlation 0.1: design effect = 5.90
```

**Follow-ups:**
- Why not just drop the control users who have treated friends? That selects a different, less connected population and shrinks the sample. Exposure-based analysis is better than deletion.
- When is user-level randomization still fine? When ties are sparse and weak, or when the effect on friends is negligible; I would check with an exposure analysis first.
- Where is this covered in theory? Book 1 Part 10, Q12 ("Explain network effects / interference (SUTVA violation). How do you run experiments on a social product or a two-sided marketplace?") and Q51 ("How do you handle interference with cluster-randomised or graph-cluster experiments? What is the bias-variance tradeoff of cluster size?").

**Common mistakes:**
- Calling the user-level lift the effect of launching.
- Assuming the bias always inflates the lift (it depends on the sign of the spillover).
- Using cluster randomization without correcting standard errors for clustering.
- Dropping boundary users to look clean.

### Q12 ⭐⭐⭐ 🟡 Baseline conversion is 5.0%, and the team wants to detect a 5% relative lift (0.25 percentage points absolute) with 80% power at a two-sided 5% level, with 20,000 eligible visitors a day split evenly between two arms. The product manager wants a readout in 3 days. Explain what this test needs and what you say to the manager.
**Asked at:** Underpowered-test and MDE material (a Towards Data Science 'what to do when an A/B test result is not significant' article, a Dataford 'non significant test PM wants launch' page, a HackerNoon 'running A/B tests you can't measure' post, a Statsig power-analysis page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** This test needs about 122,000 visitors per arm, which is about 12 days of traffic, so I would plan for 14 days (two full weeks); a 3-day readout would only see a lift of about 10 percent or more and would miss the lift we care about about 7 times in 10.
**Clarifying questions:**
- Is 5% relative the smallest lift that is worth shipping, or just a hope? It sets the MDE (minimum detectable effect), and the MDE sets the duration.
- Are the 20,000 a day unique visitors or visits? Repeat visitors mean unique users grow slower than days, so the real wait can be longer.
- Is the conversion event instant or does it lag (checkout, payment, returns)? A lag adds days after the last user enters.
- Is there a hard deadline from the business (a launch date, a sale)? It tells me whether to negotiate a bigger MDE or a different metric instead of a shorter test.
- Is the change cheap and reversible? If yes, the manager may accept a weaker evidence bar; I would still say it out loud.
**Approach:**
1. Fix the inputs: baseline 5.0%, target 5.25%, alpha 0.05 two-sided, power 80%.
2. Compute n per arm (two-proportion formula): about 122,000. Divide by 10,000 per arm per day: about 12.2 days.
3. Round up to full weeks (14 days) so every weekday and weekend day appears equally. Book 1 Part 10, Q5 (How do you decide how long to run an experiment and how many users you need?) has the formula; here I use it.
4. Flip it for the manager: with 3 days (30,000 per arm) the MDE is about 0.5 points absolute, 10% relative. A real 5% lift would be detected only about 28% of the time.
5. Offer options for a faster answer: accept a bigger MDE (10%), use CUPED (variance reduction using pre-test data) to cut the time, or pick a more sensitive upstream metric as the primary one. Do not peek and stop early (see Q16).
6. Pre-register the end date, the metric and the decision rule, and send it to the manager in writing.
**Metrics:**
- Primary: conversion = visitors who convert / visitors assigned, per arm. Numerator and denominator both from the assignment log.
- MDE (relative) = (z_alpha/2 + z_power) x standard error of the difference / baseline. At 3 days: (1.96 + 0.84) x 0.00178 / 0.05, which is about 10%.
- Power = chance of detecting the true lift. 80% is the planning target.
- Guardrails: revenue per visitor, page-load time, error rate. SRM (sample ratio mismatch) check on the 50/50 split.
**Risks:**
- A "significant" 3-day result is more likely to be a noisy overestimate, because only large random swings clear the bar (the winner's curse).
- Weekday-only traffic; the weekend mix may differ (see Q22).
- Visitors versus users: the same person can appear on several days.
- Baseline of 5.0% is an estimate; if the true baseline is 4%, n rises. Re-check with last month's data.
**What the interviewer scores:**
- Strong: gives n (about 122,000 per arm) and days (about 12), then rounds to full weeks. Weak: quotes "30,000 is plenty".
- Strong: turns the question around into "what can 3 days detect" (10% relative). Weak: only says "no".
- Strong: offers options (bigger MDE, CUPED, better metric) and a written plan. Weak: refuses or gives in.
- Strong: names that the manager's real need is a decision date, not a number. Weak: lectures on statistics.
**Example:** Illustrative numbers. Baseline 5.0%, target 5.25%. Per arm n is about 122,100. At 10,000 per arm per day that is 12.2 days, so 14 days. After 3 days each arm has 30,000 visitors. The standard error of the difference is about 0.18 points, so the MDE is about 0.5 points (10% relative) and the power for a 0.25 point lift is about 28%.
- Weak answer: "Fine, we will run for 3 days and see."
- Strong answer: "Three days can only see a 10% lift. For the 5% lift you care about we need 12 days, so two weeks. If you must decide in 3 days, tell me the lift you would still ship at, and I will tell you if 3 days can see it."
**Code:**
```python
# Q12: sample size, MDE and duration for a 5.0% -> 5.25% test (illustrative numbers)
import numpy as np
from scipy.stats import norm

alpha, power = 0.05, 0.80
p1, lift_rel = 0.05, 0.05
p2 = p1 * (1 + lift_rel)
daily_visitors = 20_000
per_arm_per_day = daily_visitors // 2
za, zb = norm.ppf(1 - alpha / 2), norm.ppf(power)

def n_per_arm(p1, p2):
    pbar = (p1 + p2) / 2
    num = (za * np.sqrt(2 * pbar * (1 - pbar)) + zb * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return num / (p2 - p1) ** 2

n = n_per_arm(p1, p2)
days = n / per_arm_per_day
print(f"p2 = {p2:.4f}, delta = {p2 - p1:.4f}")
print(f"n per arm = {n:,.0f}  ->  {days:.1f} days at {per_arm_per_day:,} per arm per day")

n3 = 3 * per_arm_per_day
se3 = np.sqrt(p1 * (1 - p1) / n3 * 2)
mde3 = (za + zb) * se3
print(f"3 days: {n3:,} per arm, MDE = {mde3:.4f} abs = {mde3 / p1:.1%} relative")
# power at 3 days for the planned +0.25 points
se_alt = np.sqrt(p1 * (1 - p1) / n3 + p2 * (1 - p2) / n3)
pw3 = norm.cdf(abs(p2 - p1) / se_alt - za)
print(f"power at 3 days for +0.25 points = {pw3:.2f}")

# simulation check of power at 3 days and at 14 days
rng = np.random.default_rng(12)
def sim_power(n, reps=4000):
    c = rng.binomial(n, p1, reps); t = rng.binomial(n, p2, reps)
    pc, pt = c / n, t / n
    pp = (c + t) / (2 * n)
    z = (pt - pc) / np.sqrt(2 * pp * (1 - pp) / n)
    return np.mean(np.abs(z) > za)
s3, s14 = sim_power(n3), sim_power(14 * per_arm_per_day)
print(f"simulated power: 3 days {s3:.2f}, 14 days {s14:.2f}")
# false positive rate when there is no effect (A/A) at 14 days
c = rng.binomial(140_000, p1, 4000); t = rng.binomial(140_000, p1, 4000)
pp = (c + t) / 280_000
z = (t - c) / 140_000 / np.sqrt(2 * pp * (1 - pp) / 140_000)
print(f"simulated A/A rejection rate = {np.mean(np.abs(z) > za):.3f}")

assert 121_000 < n < 123_500 and 12.0 < days < 12.5
assert abs(mde3 / p1 - 0.10) < 0.005
assert 0.25 < pw3 < 0.32 and abs(s3 - pw3) < 0.04
assert s14 > 0.80 and abs(np.mean(np.abs(z) > za) - 0.05) < 0.015
assert abs((1 - 0.5**2) - 0.75) < 1e-12  # CUPED rho=0.5 keeps 75% of variance
print("all asserts passed")
```
**Output (my run):**
```text
p2 = 0.0525, delta = 0.0025
n per arm = 122,123  ->  12.2 days at 10,000 per arm per day
3 days: 30,000 per arm, MDE = 0.0050 abs = 10.0% relative
power at 3 days for +0.25 points = 0.28
simulated power: 3 days 0.29, 14 days 0.85
simulated A/A rejection rate = 0.050
all asserts passed
```
**Follow-ups:**
- What if the manager insists on 3 days? Then run it as a "safety check" (guardrails, no big harm) and say clearly it cannot confirm a 5% lift. Keep running to the planned end.
- Does a bigger sample always help? Yes for power, but not for bias. If the bug is in assignment or logging, more users do not fix it.
- Could you cut the 12 days? CUPED with a pre-period covariate of correlation 0.5 cuts variance by 25% (1 - 0.5^2), which cuts the days by about the same share. Book 1 Part 10, Q5 explains the inputs.
**Common mistakes:** Quoting n for 80% power but forgetting that the same 3 days is also the stopping rule. Ignoring the weekly cycle. Using the pooled traffic number as users when visitors repeat. Agreeing to a short test and then reading a non-significant result as "no effect".

### Q13 ⭐⭐⭐ 🟡 A price change was launched in one city only. Orders per user per week in that city rose from 2.0 to 2.3 (+15% relative to its own baseline), while in five comparison cities the average rose from 2.0 to 2.2 (+10%) over the same weeks. Explain what effect you would estimate, what you assume, and how you would check the assumption.
**Asked at:** Causal-inference and when-you-cannot-randomize material (an Interview Query causal-inference guide on diff-in-diff and synthetic control, Codemia 'explain difference-in-differences' practice pages, NBER working paper 25532 on synthetic difference-in-differences); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would estimate the effect by difference-in-differences: the treated city rose by 0.3 orders and the comparison cities by 0.2, so the price change effect is about +0.1 orders per user per week, +5% of the 2.0 baseline, not +15%, and it holds only if the city would have moved like the others without the change.
**Clarifying questions:**
- How many weeks of history do I have before the launch? I need many pre-weeks to test whether the cities moved together.
- Why was this city chosen? If it was picked because it was weak or strong (or had a local event), the comparison is not fair.
- Were comparison cities touched by anything else (competitor promo, weather, a holiday) in the same weeks? Any shock hitting only one side breaks the design.
- Can customers cross cities or see the new price from outside (spillover)? That contaminates the comparison cities.
- What is the outcome I care about: orders, revenue or margin? A price change moves the price per order, so orders alone can mislead.
**Approach:**
1. Compute the DiD: (2.3 - 2.0) - (2.2 - 2.0) = 0.1 orders per user per week. Relative to the 2.0 baseline that is +5%. The raw +15% mixes the price effect with a market lift of +10% that the comparison cities show.
2. State the key assumption: parallel trends (without the change, the treated city would have moved by +0.2 like the others). It cannot be proven, only checked. Book 1 Part 10, Q28 (Explain difference-in-differences) covers the assumption.
3. Check it: plot weekly orders for the treated city and the comparison average for 8 or more pre-weeks; estimate the pre-period gap slope; run an event-study (leads should be about zero).
4. Placebo test: pretend each comparison city was the treated one and compute its DiD. If the real DiD is not extreme against these, it is not convincing. With 1 treated city and 5 others the smallest permutation p-value is 1/6.
5. Improve the comparison: reweight or choose comparison cities that match on pre-trend (synthetic control, Book 1 Part 10, Q49), and check robustness to dropping one city at a time.
6. Report the estimate with uncertainty and a plain caveat: this is quasi-experimental, so it is weaker than a randomised test.
**Metrics:**
- DiD = (treated post mean - treated pre mean) - (comparison post mean - comparison pre mean), orders per user per week, users counted in the same way in all weeks.
- Relative effect = DiD / treated pre mean (here 0.1 / 2.0).
- Pre-trend slope of the gap (treated minus comparison) per week; should be close to zero.
- Guardrails: revenue per user, margin per order, cancellations. Price changes can raise orders and still lose money.
**Risks:**
- Parallel trends fails (the city was already growing faster). The simulation below shows the estimate then overstates a true 0.10 as about 0.17.
- One treated unit means very wide uncertainty; ordinary standard errors are too small.
- Spillovers and other local events in the same weeks.
- A price rise or fall also changes who orders: the mix shifts, so orders per user can hide a loss of high-value users.
**What the interviewer scores:**
- Strong: gets +0.1 (+5%) and says why +15% is wrong. Weak: reports +15% or +5% without a reason.
- Strong: names parallel trends and shows how to check (pre-trends, placebo). Weak: says "it is causal because there is a control group".
- Strong: asks why the city was picked. Weak: ignores selection.
- Strong: says what a randomised geo test would add. Weak: only repeats the formula.
**Example:** Illustrative numbers from the prompt. Treated city 2.0 to 2.3 (+0.3). Comparison average 2.0 to 2.2 (+0.2). DiD = 0.1 orders, +5% of 2.0. If the treated city had already been growing 0.01 orders more per week than the others before launch, part of that 0.1 is trend, not price.
- Weak answer: "Orders rose 15%, so the price change worked."
- Strong answer: "Comparison cities rose 10% on their own, so the price effect is about 5 points, and I need the pre-trends and a placebo before I believe it."
**Code:**
```python
# Q13: difference-in-differences for a one-city price change (illustrative numbers)
import numpy as np

# 1) The arithmetic from the prompt
pre_t, post_t = 2.0, 2.3
pre_c, post_c = 2.0, 2.2
did = (post_t - pre_t) - (post_c - pre_c)
print(f"naive before/after in treated city: {(post_t - pre_t) / pre_t:+.0%}")
print(f"DiD = {did:.2f} orders per user per week = {did / pre_t:+.1%} of the baseline")
assert abs(did - 0.1) < 1e-9 and abs(did / pre_t - 0.05) < 1e-9

# 2) Simulated weekly panel: 8 pre weeks, 4 post weeks, 1 treated + 5 comparison cities
rng = np.random.default_rng(13)
weeks, pre_w = 12, 8
trend = np.linspace(0, 0.2, weeks)           # shared market trend (+0.2 over 12 weeks)

def panel(extra_slope_treated=0.0, true_effect=0.10, noise=0.03):
    cities = []
    for k in range(6):
        y = 2.0 + trend + rng.normal(0, noise, weeks)
        if k == 0:
            y = y + np.linspace(0, extra_slope_treated, weeks)
            y[pre_w:] += true_effect
        cities.append(y)
    return np.array(cities)

def did_est(Y, treated=0):
    ctrl = [i for i in range(len(Y)) if i != treated]
    t = Y[treated, pre_w:].mean() - Y[treated, :pre_w].mean()
    c = Y[ctrl, pre_w:].mean() - Y[ctrl, :pre_w].mean()
    return t - c

def pretrend_gap(Y, treated=0):
    """slope of (treated - mean control) over the pre weeks, per week"""
    ctrl = [i for i in range(len(Y)) if i != treated]
    gap = Y[treated, :pre_w] - Y[ctrl, :pre_w].mean(axis=0)
    return np.polyfit(np.arange(pre_w), gap, 1)[0]

# parallel trends hold
ests, slopes = [], []
for _ in range(2000):
    Y = panel(); ests.append(did_est(Y)); slopes.append(pretrend_gap(Y))
print(f"parallel trends: DiD mean {np.mean(ests):.3f} (truth 0.100), sd {np.std(ests):.3f}, pre-trend slope sd {np.std(slopes):.4f}")
assert abs(np.mean(ests) - 0.10) < 0.005

# treated city was already growing faster (violation)
ests2, slopes2 = [], []
for _ in range(2000):
    Y = panel(extra_slope_treated=0.12); ests2.append(did_est(Y)); slopes2.append(pretrend_gap(Y))
print(f"trend violated:   DiD mean {np.mean(ests2):.3f} (truth 0.100), pre-trend slope mean {np.mean(slopes2):.4f} per week")
assert np.mean(ests2) > 0.15 and np.mean(slopes2) > 0.005

# 3) Placebo (permutation) inference with ONE treated city: pretend each comparison city was treated
Y = panel()
real = did_est(Y, 0)
placebo = [did_est(Y, k) for k in range(1, 6)]
print(f"real DiD {real:.3f}; placebo DiDs {np.round(placebo, 3)}")
rank = 1 + sum(abs(p) >= abs(real) for p in placebo)
print(f"rank of real among 6 = {rank}; smallest possible permutation p = 1/6 = {1/6:.3f}")
assert rank == 1
print("all asserts passed")
```
**Output (my run):**
```text
naive before/after in treated city: +15%
DiD = 0.10 orders per user per week = +5.0% of the baseline
parallel trends: DiD mean 0.100 (truth 0.100), sd 0.020, pre-trend slope sd 0.0050
trend violated:   DiD mean 0.166 (truth 0.100), pre-trend slope mean 0.0108 per week
real DiD 0.111; placebo DiDs [-0.002 -0.023 -0.025 -0.021 -0.04 ]
rank of real among 6 = 1; smallest possible permutation p = 1/6 = 0.167
all asserts passed
```
**Follow-ups:**
- What if the pre-trends differ? Add a city-specific trend or use synthetic control weights fitted on the pre-period; if the fit is poor, say the data cannot answer the question. Book 1 Part 10, Q19 (You cannot randomize) lists the options.
- How would you get proper confidence intervals? Placebo or permutation across cities, or a bootstrap over cities with many comparison units; a normal t-interval on one treated city is not reliable.
- Would you rather randomise? Yes: randomise by city or by time slice if the business can. Here it was already launched.
**Common mistakes:** Quoting the before-after change as the effect. Skipping the pre-trend check. Calling a single-city study "significant" with a plain t-test. Using a comparison city that was also affected (for example by a rival's move). Mixing +10% and +5 points in the same sentence.

### Q14 ⭐⭐⭐ 🟡 After a release, treatment shows 4% fewer add-to-cart events than control (relative to control), yet backend order counts are equal in the two arms. The release also renamed the add-to-cart event in the Android client, and Android is 45% of users. Explain how you diagnose this and what you do with the experiment.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
**Say this first (1 line):** Equal backend orders with 4% fewer add-to-cart events, right after an Android event rename, points to a logging bug and not to user behaviour, so I would cut by platform and app version, and I would not read the experiment on that event until it is fixed.
**Clarifying questions:**
- Which event name does the experiment dashboard count, and did the rename ship to both arms or only to treatment? A rename that only the treatment build has makes the old-name query miss events.
- Are backend orders (server side) independent of the client events? Yes means they are my ground truth; if both come from the client, I have no check.
- Which app versions carry the rename, and what share of Android users is on them? That sizes the loss.
- Did anything else change in the release (UI, button placement) that could really reduce add-to-cart? I still must rule out a real effect.
- Is there a server-side add-to-cart record (cart table)? It lets me count the truth without the client.
**Approach:**
1. Do not argue about the -4% yet. Test the funnel on a different data source: orders equal, so the end of the funnel did not change.
2. Cut the -4% by platform: if iOS and web are about 0% and Android carries all of it, the cause is Android. Illustrative arithmetic: if Android is 45% of events and carries the whole drop, then 4% / 0.45 = 8.9% of Android events are missing.
3. Cut by app version and event name: count the old and the new event name in each arm and version. The sum of both names should match the control count.
4. Check the funnel ratio: orders per add-to-cart event should be flat. A jump on Android in treatment (0.50 to 0.55 in my run) says the denominator lost events, not that users became better buyers.
5. Check the assignment: SRM and platform mix per arm should be fine (they are in my run), so the split is not the problem.
6. Decide: fix the event mapping, backfill from raw logs or server data if possible, then recompute. If the data cannot be recovered, re-run the affected cohort or exclude add-to-cart as a metric and read the test on backend orders. Book 1 Part 10, Q53 (How would you debug an experiment platform whose results look wrong) lists the platform checks.
**Metrics:**
- Add-to-cart events per user = add-to-cart events / assigned users, by platform and arm.
- Orders per user from the backend (server side), the ground truth.
- Funnel ratio = orders / add-to-cart events, by platform and arm.
- Guardrails: SRM p-value, share of events with an unknown event name, crash rate.
**Risks:**
- Treating the -4% as a real harm and killing a fine feature.
- Treating it as a pure bug and ignoring a real small drop that is hidden by equal orders (orders could be equal by noise; with a small sample "equal" is not proof).
- Fixing the pipeline mid-test without recording the date: the metric then has two regimes.
- Equal orders do not prove the add-to-cart behaviour is unchanged: users may add less and still order by other paths.
**What the interviewer scores:**
- Strong: uses a trusted second source (backend orders) to see the inconsistency. Weak: accepts the dashboard.
- Strong: segments by platform and version and does the 4 / 0.45 arithmetic. Weak: guesses.
- Strong: separates "what is the data issue" from "what is the decision" and says what to do with the test. Weak: only debugs.
- Strong: asks for instrumentation checks before launch (A/A, event contract tests). Weak: no prevention.
**Example:** Illustrative numbers. Control logs 1,000,000 add-to-cart events; treatment logs 960,000 (-4%). Orders: 300,000 in both arms. Android is 45% of events. If iOS and web are unchanged, Android lost 40,000 of 450,000 events, which is 8.9%. The orders-per-event ratio on Android moves from 0.50 to 0.55 while iOS and web stay at 0.50, which is the footprint of a missing denominator.
- Weak answer: "Treatment hurts add-to-cart by 4%, so we should not ship."
- Strong answer: "Orders did not move and the drop sits in Android after a rename. I think it is lost events. I will confirm by platform and version, fix the mapping, and read the test on orders."
**Code:**
```python
# Q14: -4% add-to-cart events but equal orders: a logging bug on Android? (illustrative simulation)
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

rng = np.random.default_rng(14)
n_per_arm = 2_000_000
android_share = 0.45
atc_per_user = 0.60          # add-to-cart events per user per week (same on all platforms)
order_rate = 0.30            # orders per user per week (from the backend, same in both arms)
lost_android_atc = 0.04 / android_share   # share of Android ATC events that stop being logged in treatment

print(f"implied Android ATC loss if iOS/web are clean: 0.04 / 0.45 = {lost_android_atc:.1%}")
assert abs(lost_android_atc - 0.0889) < 0.0005

rows = []
for arm in ("control", "treatment"):
    plat = rng.random(n_per_arm) < android_share
    atc_true = rng.poisson(atc_per_user, n_per_arm)
    orders = rng.poisson(order_rate, n_per_arm)
    logged = atc_true.copy()
    if arm == "treatment":      # renamed event is not picked up for part of Android events
        logged = np.where(plat, rng.binomial(atc_true, 1 - lost_android_atc), atc_true)
    rows.append(pd.DataFrame({"arm": arm, "android": plat, "atc": logged, "orders": orders}))
df = pd.concat(rows, ignore_index=True)

# 1) top line
g = df.groupby("arm")[["atc", "orders"]].sum()
print("top line ATC change :", f"{g.loc['treatment','atc'] / g.loc['control','atc'] - 1:+.2%}")
print("top line order change:", f"{g.loc['treatment','orders'] / g.loc['control','orders'] - 1:+.2%}")

# 2) cut by platform
p = df.groupby(["android", "arm"])[["atc", "orders"]].sum().unstack()
for plat, name in ((False, "iOS/web"), (True, "Android")):
    a = p.loc[plat, ("atc", "treatment")] / p.loc[plat, ("atc", "control")] - 1
    o = p.loc[plat, ("orders", "treatment")] / p.loc[plat, ("orders", "control")] - 1
    print(f"{name:8} ATC {a:+.2%}   orders {o:+.2%}")

# 3) funnel ratio orders per ATC event: jumps only where logging broke
ratio = (df.groupby(["android", "arm"])["orders"].sum() / df.groupby(["android", "arm"])["atc"].sum()).unstack()
print("orders per ATC event\n", ratio.round(3))

# 4) user split by platform and arm is fine (no SRM on platform mix)
ct = pd.crosstab(df["arm"], df["android"])
print("platform mix p-value:", round(chi2_contingency(ct)[1], 3))

# checks on the numbers quoted in the text
top = g.loc['treatment','atc'] / g.loc['control','atc'] - 1
assert -0.045 < top < -0.035
ord_chg = g.loc['treatment','orders'] / g.loc['control','orders'] - 1
assert abs(ord_chg) < 0.005
ios_chg = p.loc[False, ("atc","treatment")] / p.loc[False, ("atc","control")] - 1
and_chg = p.loc[True, ("atc","treatment")] / p.loc[True, ("atc","control")] - 1
assert abs(ios_chg) < 0.005 and -0.11 < and_chg < -0.07
assert ratio.loc[True, "treatment"] > 1.07 * ratio.loc[True, "control"]
print("all asserts passed")
```
**Output (my run):**
```text
implied Android ATC loss if iOS/web are clean: 0.04 / 0.45 = 8.9%
top line ATC change : -4.00%
top line order change: -0.21%
iOS/web  ATC -0.09%   orders -0.31%
Android  ATC -8.79%   orders -0.10%
orders per ATC event
 arm      control  treatment
android                    
False      0.500      0.499
True       0.501      0.549
platform mix p-value: 0.792
all asserts passed
```
**Follow-ups:**
- How do you prevent this? Contract tests on event names, an A/A run after every client release, and alerts when an event count per user moves more than expected in a non-experiment.
- What if the renamed event also changes the meaning (not just the name)? Then the metric is not comparable across arms and needs a new definition before any readout.
- Can I still use the test? Yes for backend metrics. Use the client metric only after the mapping is fixed and the history is rebuilt.
**Common mistakes:** Reporting the -4% to the product manager before checking the pipeline. Looking only at the top line. Dropping Android and calling the test clean, without saying what share of users that removes. Forgetting to ask whether the rename shipped to both arms.

### Q15 ⭐⭐⭐ 🟡 A test on 2,000,000 users per arm shows revenue per user up 0.4% relative to control, with a 95% confidence interval of +0.1% to +0.7%. Shipping costs 3 engineer-months and adds a feature to maintain, and the product manager says 'it is significant, so ship'. Explain how you make the decision.
**Asked at:** Guardrail and ship-decision material (a Dataford 'primary vs guardrail metrics' page, a Spotify Confidence guardrail-metric glossary and blog post, PracHub analytics-and-experimentation question pages, a Dataford 'non significant test PM wants launch' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Significant only means the lift is probably not zero; I decide by comparing the whole interval, +0.1% to +0.7%, with the break-even lift that pays for 3 engineer-months and the upkeep, and in my illustrative case the point estimate clears break-even but the low end does not.
**Clarifying questions:**
- What is the revenue base the 0.4% applies to (all users, one market, one surface)? The gain in money is lift times that base.
- What is the full cost: the 3 engineer-months, the upkeep, the opportunity cost of what else the team would build? Break-even needs all of it.
- Is the feature reversible and cheap to turn off? If yes, I am happier to ship on a thinner margin.
- Was this the only test or one of many tried versions? The winner's curse (the best of many looks too good) shrinks the estimate.
- Does revenue per user come with guardrails (refunds, retention, latency)? A small revenue gain can hide a long-term cost.
**Approach:**
1. Agree that the result is significant: the interval excludes 0 (z about 2.6, p about 0.009). Then say that is not the decision.
2. Convert the lift into money with the base: lift x annual revenue. Convert the cost into the same unit and divide to get the break-even lift.
3. Compare the interval with break-even: all above means ship; all below means do not; straddling means judge by risk, reversibility and cost of waiting.
4. Shrink the estimate for the winner's curse, and for a one-time novelty effect. Book 1 Part 10, Q15 (Statistical vs practical significance) gives the reading of the interval; Book 1 Part 10, Q54 covers the winner's curse.
5. Options when it straddles: ship with a holdout (a small group stays on the old version) to measure the real long-run lift, run longer to narrow the interval, or reduce the cost (a cheaper version).
6. Write down the decision rule before the readout next time.
**Metrics:**
- Relative lift = (revenue per user in treatment / revenue per user in control) - 1, over the full test period, same users in both denominators.
- Annual gain = lift x annual revenue of the affected users; net = gain - yearly cost.
- Break-even lift = yearly cost / annual revenue of the affected users.
- Probability the true lift exceeds break-even (a rough normal approximation) and expected net value.
- Guardrails: refunds, support contacts, retention, latency.
**Risks:**
- Heavy-tailed revenue: a few large buyers can produce the lift; check winsorized and per-user medians.
- The test base is not the rollout base (only some users were eligible).
- Maintenance cost is underestimated, so break-even is too low.
- Waiting for certainty has a cost too: each month of delay forgoes the expected gain.
**What the interviewer scores:**
- Strong: separates significance from size and from value. Weak: "p is small so ship" or "0.4% is tiny so no".
- Strong: builds a break-even from invented but explicit numbers and uses the interval. Weak: uses only the point estimate.
- Strong: mentions shrinkage, reversibility and a holdout. Weak: only says "run longer".
- Strong: gives a decision and its condition ("ship if the cost is under X"). Weak: ends with "it depends".
**Example:** Illustrative numbers. 10 million users, 100 units revenue per user per month: annual revenue 12,000 million units. Yearly cost 40 million units gives a break-even lift of 0.333%. Gains: low end 12 million (net -28 million), point 48 million (net +8 million), high end 84 million (net +44 million). The probability that the true lift beats break-even is about 67%. With a skeptical prior (most ideas are about 0 plus or minus 0.3%), the shrunk estimate is 0.317%, just under break-even.
- Weak answer: "It is significant, so ship."
- Strong answer: "The lift is real but small. It clears break-even only on the point estimate, so I would ship only if it is cheap to keep or ship with a holdout and re-measure."
**Code:**
```python
# Q15: statistically significant is not the same as worth shipping (illustrative numbers)
import numpy as np
from scipy.stats import norm

lift, lo, hi = 0.004, 0.001, 0.007          # relative lift on revenue per user and its 95% CI
se = (hi - lo) / (2 * 1.96)
z = lift / se
p = 2 * norm.sf(z)
print(f"implied SE = {se:.4%} relative, z = {z:.2f}, p = {p:.4f}")
assert abs(se - 0.0015306) < 1e-6 and 0.005 < p < 0.01          # significant, as the PM says

# Business case (all inventive units): 10M users, 100 units revenue per user per month
users, rev_pm = 10_000_000, 100.0
annual_rev = users * rev_pm * 12
cost_per_year = 40_000_000                  # build + upkeep, in the same units; finance supplies the real figure
breakeven = cost_per_year / annual_rev
print(f"annual revenue {annual_rev:,.0f}; cost {cost_per_year:,.0f}/yr; break-even lift = {breakeven:.3%}")
assert abs(breakeven - 4e7 / 1.2e10) < 1e-12

for name, l in (("low", lo), ("point", lift), ("high", hi)):
    print(f"{name:5}: lift {l:.2%} -> gain {l * annual_rev:,.0f} units/yr, net {l * annual_rev - cost_per_year:,.0f}")
assert lo * annual_rev - cost_per_year < 0 < lift * annual_rev - cost_per_year

# rough probability the true lift clears break-even (normal approximation around the estimate, flat prior)
p_clear = norm.sf((breakeven - lift) / se)
print(f"P(true lift > break-even) ~ {p_clear:.0%}")
assert 0.6 < p_clear < 0.7

# shrinkage for the winner's curse: if most ideas have lift ~ 0 +- 0.3%, the posterior mean is lower
prior_sd = 0.003
post_mean = lift * prior_sd**2 / (prior_sd**2 + se**2)
print(f"posterior mean with a N(0, 0.3%) prior = {post_mean:.3%}")
assert post_mean < lift

# how much longer would we need to cut the interval width in half? 4x the users
print("users needed for half-width CI: 4x ->", 4 * 2_000_000, "per arm")
assert abs(se / 2 - np.sqrt(se**2 / 4)) < 1e-12
print("all asserts passed")
```
**Output (my run):**
```text
implied SE = 0.1531% relative, z = 2.61, p = 0.0090
annual revenue 12,000,000,000; cost 40,000,000/yr; break-even lift = 0.333%
low  : lift 0.10% -> gain 12,000,000 units/yr, net -28,000,000
point: lift 0.40% -> gain 48,000,000 units/yr, net 8,000,000
high : lift 0.70% -> gain 84,000,000 units/yr, net 44,000,000
P(true lift > break-even) ~ 67%
posterior mean with a N(0, 0.3%) prior = 0.317%
users needed for half-width CI: 4x -> 8000000 per arm
all asserts passed
```
**Follow-ups:**
- What if the cost is half? Break-even drops to 0.167%; then the point estimate and most of the interval clear it, and I would ship.
- How do you narrow the interval? Variance reduction (CUPED) or more users: half the width needs about four times the users.
- What if the 3 engineer-months are already spent? Then only the upkeep matters for the decision (sunk cost); I would still count it.
**Common mistakes:** Mixing statistical and practical significance. Using the upper end of the interval as the expected gain. Ignoring maintenance. Forgetting the break-even depends on the base the lift applies to.

### Q16 ⭐⭐⭐ 🔴 A team looks at the experiment every day for 14 days and stops the first time p < 0.05, and an A/A simulation with that rule declares a 'winner' in roughly one run in five. Explain why, what you change in the process, and how you handle the business demand to be able to stop early.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Checking daily and stopping at the first p below 0.05 gives a false winner in about one run in five (22% in my simulation) when nothing is different, because each look is another chance to cross the line; the fix is to fix the end date, or to use sequential boundaries that spend the 5% error budget across the looks.
**Clarifying questions:**
- Why does the business want to stop early: to ship a winner sooner, or to stop a harmful test? The first needs a boundary for wins; the second needs a guardrail rule.
- How many looks do they really need (daily, weekly)? Fewer looks cost less alpha.
- Is a wrong win costly or cheap to undo? It sets how strict the early boundary should be.
- Does the platform support sequential or always-valid p-values? If yes, use them; if no, plan the looks in advance.
- Is the metric stable by day of week? Early looks on partial weeks are biased.
**Approach:**
1. Explain why in one line: p-values are valid for one pre-planned look. With 14 looks the chance that at least one crosses 1.96 under no effect is about 22%, not 5%.
2. Show it: run an A/A simulation with the same stopping rule (my run below). A demo convinces a manager faster than theory. Book 1 Part 10, Q7 (the PM wants to stop after 3 days) has the basic argument.
3. Process fix A: fix the sample size and the end date before the start; look at guardrails daily but read the primary metric only at the end.
4. Process fix B, when early stopping is a real need: pre-register the number of looks and use group-sequential boundaries. A constant boundary needs |z| above about 2.62 at every look; an O'Brien-Fleming-style boundary is very strict early (about 7.9 on day 1) and about 2.11 on day 14.
5. Or use an always-valid method (mixture sequential probability ratio test, SPRT). It keeps the error rate at any stopping time, at some cost in power.
6. Tell the business what they get: early stop for large effects or clear harm, and a clean decision date otherwise.
**Metrics:**
- False positive rate under A/A = runs that declare a winner at any look / total A/A runs.
- Overall alpha of a sequential design = chance that any look crosses its boundary under no effect (target 5%).
- Power = chance of declaring a win when the true effect exists, with early stopping allowed.
- Average sample number (users used on average) to show the early-stopping benefit.
**Risks:**
- Peeking at secondary metrics and picking one is the same problem (see Q4).
- A win declared early overstates the effect (winner's curse); report a shrunk estimate.
- Boundaries assume the looks are planned; unplanned extra looks break them.
- Early days are not representative (weekday mix, novelty).
**What the interviewer scores:**
- Strong: gives the reason (multiple looks, correlated tests) and a number near 20%. Weak: "peeking is bad" with no number.
- Strong: proposes both a process rule and a statistical fix. Weak: only statistical or only "do not look".
- Strong: respects the business need (early stop for harm or big wins). Weak: says "never stop early".
- Strong: runs or describes the A/A simulation. Weak: only recalls Bonferroni (Bonferroni is too conservative for correlated looks).
**Example:** Illustrative numbers. 500 users per arm per day, 14 days, no true difference. One look on day 14: 5.0% false wins. Stop at the first p below 0.05 across 14 daily looks: 21.8% (about 1 in 4.6). The share of runs that first cross on day 1 is 5.1%, on day 2 about 3.2%, and so on down to about 0.6% on day 14. With the constant boundary of 2.62 the overall error is back to 5%. The price of the O'Brien-Fleming-style rule is small: for a true effect of 0.04 sd, power is 0.64 with early stopping allowed against 0.66 for the single day-14 test.
- Weak answer: "The p-value is 0.04 on day 6 so it is significant; ship."
- Strong answer: "With 14 daily looks, that rule gives a false winner about once in five A/A runs. I would pre-set the end date, or use a boundary that spends alpha across looks."
**Code:**
```python
# Q16: daily peeking in an A/A test, and a fix with group-sequential boundaries (simulation)
import numpy as np
from scipy.stats import norm

rng = np.random.default_rng(16)
K, reps, per_day = 14, 100_000, 500          # 14 daily looks, 500 users per arm per day
z95 = norm.ppf(0.975)

# A/A: both arms have the same distribution. Look k uses all data up to day k.
# the sum of 500 N(0,1) values is N(0, 500), so draw each day's arm total directly (same statistics, much faster)
d = rng.normal(0, np.sqrt(per_day), (reps, K, 2))
cum = d.cumsum(axis=1)                       # (reps, K, 2) running sums per arm
n_k = per_day * np.arange(1, K + 1)
diff = cum[:, :, 1] / n_k[None, :] - cum[:, :, 0] / n_k[None, :]
z = diff / np.sqrt(2 / n_k[None, :])

single = np.mean(np.abs(z[:, -1]) > z95)
naive = np.mean((np.abs(z) > z95).any(axis=1))
print(f"one look at day 14: false positive rate = {single:.3f}")
print(f"stop at first p<0.05 over 14 daily looks: {naive:.3f}  (about 1 in {1/naive:.1f})")
assert abs(single - 0.05) < 0.005 and 0.18 < naive < 0.28

# when do the false wins occur?
first = np.where((np.abs(z) > z95).any(axis=1), (np.abs(z) > z95).argmax(axis=1) + 1, 0)
print("share of false wins by first day (1..14):", np.round(np.bincount(first, minlength=15)[1:] / reps, 3))

# Fix 1: one constant (Pocock-style) boundary for all 14 looks
def alpha_for(boundary):
    return np.mean((np.abs(z) > boundary[None, :]).any(axis=1))

lo_c, hi_c = 2.0, 3.5
for _ in range(30):
    mid = (lo_c + hi_c) / 2
    if alpha_for(np.full(K, mid)) > 0.05: lo_c = mid
    else: hi_c = mid
c_poc = hi_c
# Fix 2: O'Brien-Fleming-style boundary c*sqrt(K/k): strict early, near 1.96 at the end
lo_c, hi_c = 1.5, 3.0
for _ in range(30):
    mid = (lo_c + hi_c) / 2
    if alpha_for(mid * np.sqrt(K / np.arange(1, K + 1))) > 0.05: lo_c = mid
    else: hi_c = mid
c_obf = hi_c
bound_obf = c_obf * np.sqrt(K / np.arange(1, K + 1))
print(f"constant boundary |z| > {c_poc:.2f} at every look -> overall alpha {alpha_for(np.full(K, c_poc)):.3f}")
print(f"OBF-style: c = {c_obf:.2f}; |z| bounds day 1 {bound_obf[0]:.2f}, day 7 {bound_obf[6]:.2f}, day 14 {bound_obf[-1]:.2f} -> overall alpha {alpha_for(bound_obf):.3f}")
assert 2.5 < c_poc < 2.9 and abs(alpha_for(np.full(K, c_poc)) - 0.05) < 0.006
assert bound_obf[-1] < 2.2 and bound_obf[0] > 6

# Power cost of the fix: true effect 0.04 sd, 14 looks, compare fixed-sample test at day 14
eff = 0.04
d2 = rng.normal(0, np.sqrt(per_day), (20_000, K, 2)); d2[:, :, 1] += eff * per_day
cum2 = d2.cumsum(axis=1)
diff2 = cum2[:, :, 1] / n_k[None, :] - cum2[:, :, 0] / n_k[None, :]
z2 = diff2 / np.sqrt(2 / n_k[None, :])
pw_fixed = np.mean(z2[:, -1] > z95)
pw_obf = np.mean((z2 > bound_obf[None, :]).any(axis=1))
print(f"power, effect 0.04 sd: fixed day-14 test {pw_fixed:.2f}; OBF with early stopping allowed {pw_obf:.2f}")
assert pw_obf < pw_fixed and pw_fixed - pw_obf < 0.1
print("all asserts passed")
```
**Output (my run):**
```text
one look at day 14: false positive rate = 0.050
stop at first p<0.05 over 14 daily looks: 0.218  (about 1 in 4.6)
share of false wins by first day (1..14): [0.051 0.032 0.024 0.019 0.015 0.013 0.012 0.01  0.009 0.009 0.007 0.007
 0.006 0.006]
constant boundary |z| > 2.62 at every look -> overall alpha 0.050
OBF-style: c = 2.11; |z| bounds day 1 7.89, day 7 2.98, day 14 2.11 -> overall alpha 0.050
power, effect 0.04 sd: fixed day-14 test 0.66; OBF with early stopping allowed 0.64
all asserts passed
```
**Follow-ups:**
- Is Bonferroni over 14 looks right? It is valid but too strict because looks are positively correlated (the same data keeps being reused). Group-sequential boundaries are tighter.
- Can a Bayesian look as often as they like? Not for free. A posterior-probability stopping rule also inflates false wins unless it is calibrated; check it with an A/A simulation.
- What about stopping for harm? Use a one-sided guardrail rule with its own boundary; it spends a small part of the error budget.
**Common mistakes:** Saying "it is just 5% per look so fine". Applying Bonferroni blindly. Changing the end date after seeing the data. Reporting the raw estimate after an early stop without shrinkage.

### Q17 ⭐⭐⭐ 🔴 A test with no overall effect (+0.3% relative to control, not significant) is sliced into 40 segments by country, device and tenure, and one segment, new Android users in one country, shows +9% relative with p = 0.01. If none of the 40 segment effects were real, the chance that at least one reaches p <= 0.01 would be about 33%. The product manager wants to launch for that segment, so explain what you do.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would not launch on one segment out of 40: with no real effects anywhere, about 33% of experiments show at least one segment at p of 0.01 or below, and the +9% is the best of 40 noisy estimates, so I treat it as a hypothesis to confirm with a fresh test.
**Clarifying questions:**
- Were the 40 segments (and the cut by country, device and tenure) planned before the test or chosen after the result? Only planned cuts have a fair error rate.
- How many cuts did the team look at in total, including those not reported? The real number is usually larger than 40.
- Is there a reason to expect this segment to differ (a bug on that device, a local feature, a language issue)? A mechanism makes the claim stronger; none makes it weaker.
- How big is the segment (users, revenue)? A small segment gives a noisy and also small win.
- Is it cheap to launch to only that segment and keep a holdout? That changes the risk.
**Approach:**
1. State the base rate: 40 independent chances at the 1% level give 1 - 0.99^40 = 33% for at least one hit. (Segments overlap, so the true chance differs a little; the message is the same.)
2. Apply a correction and see what happens: Bonferroni needs p at or below 0.05 / 40 = 0.00125; Benjamini-Hochberg (BH) for the smallest p needs the same 0.00125. The segment at p = 0.01 passes neither. Book 1 Part 10, Q9 (the multiple-testing problem and Bonferroni, BH) has the methods.
3. Read the interval, not the p: a +9% estimate with p = 0.01 has a standard error of about 3.5%, so its 95% CI is about +2% to +16%, and the best of 40 is biased upward (winner's curse).
4. Ask whether the segment effect really differs from the rest: run an interaction test (does the treatment effect vary by this segment?) rather than a test inside the segment alone. Book 1 Part 10, Q47 (heterogeneous treatment effects) covers the danger of post-hoc subgroups.
5. Confirm: pre-register this one segment and run a new test on fresh traffic, or keep a holdout inside a segment launch.
6. Tell the product manager the cost and the date: a confirmation takes N days, and it protects a launch that may do nothing.
**Metrics:**
- Segment effect = (metric per user in treatment / metric per user in control) - 1, inside the segment; users in segment arm as denominator.
- Family-wise error rate (chance of any false hit across the 40) and false discovery rate (share of hits that are false).
- Adjusted p-value (Bonferroni: p x 40, capped at 1; here 0.4).
- Replication estimate on new data: the number I trust.
**Risks:**
- Subgroup hunting after the result (the garden of forking paths): the number of looks is larger than the reported 40.
- A segment that is a truly broken experience is real, but the estimate is then still noisy.
- Selection and winner's curse make the launch decision look better than it is.
- Launching on an unproven segment starts a story ("it works on Android in country X") that is hard to retire.
**What the interviewer scores:**
- Strong: computes 33% and the corrected thresholds. Weak: "it is significant at 0.01".
- Strong: separates exploration from confirmation and proposes the confirmatory test. Weak: refuses with no path forward.
- Strong: mentions winner's curse and the interaction test. Weak: applies Bonferroni only.
- Strong: proposes a low-regret launch (segment holdout). Weak: either launches or kills.
**Example:** Illustrative numbers. 40 segments, no real effect anywhere. The chance of at least one at p of 0.01 or below is 33.1% (simulated: 33.1%). Bonferroni threshold 0.00125, adjusted p for the hit 0.4. In a simulation where 5 of 40 segments have a real +2% and the rest are 0 (standard error 3.5%), the best-looking segment shows +8.0% on average, its true effect is +0.6% on average, and it is a truly null segment 68% of the time. Re-tested on fresh data it shows +0.6%.
- Weak answer: "New Android users in that country is up 9% at p = 0.01, so launch there."
- Strong answer: "One in three flat tests shows such a segment. I would confirm it with a new test on that segment alone, then launch."
**Code:**
```python
# Q17: one 'winning' segment out of 40 after a flat overall test (simulation, illustrative numbers)
import numpy as np
from scipy.stats import norm

rng = np.random.default_rng(17)
m, alpha1 = 40, 0.01
print(f"P(at least one of {m} null segments has p <= {alpha1}) = 1 - 0.99^{m} = {1 - 0.99**m:.3f}")
assert abs((1 - 0.99**m) - 0.331) < 0.001

# Simulate: every segment has a true effect of exactly 0; z ~ N(0,1) in each segment
reps = 200_000
z = rng.standard_normal((reps, m))
p = 2 * norm.sf(np.abs(z))
any_001 = np.mean((p <= alpha1).any(axis=1))
print(f"simulated: {any_001:.3f} of null experiments show at least one segment with p <= 0.01")
assert abs(any_001 - 0.331) < 0.005

# What corrections say about p = 0.01 when it is the smallest of 40
bonf = 0.05 / m
print(f"Bonferroni threshold 0.05/{m} = {bonf:.5f}; p = 0.01 passes? {0.01 <= bonf}")
# Benjamini-Hochberg: smallest p is compared with 0.05 * 1/40
bh = 0.05 * 1 / m
print(f"BH threshold for rank 1 = {bh:.5f}; p = 0.01 passes? {0.01 <= bh}")
assert 0.01 > bonf and 0.01 > bh

# A segment with +9% and p = 0.01 has an SE of about 9% / 2.576
se = 0.09 / norm.isf(0.005)
print(f"SE implied for the segment = {se:.1%} relative; its 95% CI is {0.09 - 1.96*se:+.1%} to {0.09 + 1.96*se:+.1%}")
assert 0.034 < se < 0.036

# Winner's curse: 5 of 40 segments have a real +2%, others 0, SE 3.5%. Pick the segment with the best estimate.
se_seg, true = 0.035, np.zeros(m); true[:5] = 0.02
est = true + se_seg * rng.standard_normal((reps, m))
best = est.argmax(axis=1)
sel_est = est[np.arange(reps), best]
sel_true = true[best]
print(f"best segment: mean estimate {sel_est.mean():+.1%}, mean true effect {sel_true.mean():+.2%}, picked a truly null segment {np.mean(sel_true == 0):.0%} of the time")
assert sel_est.mean() > 0.07 and sel_true.mean() < 0.01 and 0.6 < np.mean(sel_true == 0) < 0.75

# Replication on fresh data for the chosen segment (a confirmatory test with a new sample)
new = true[best] + se_seg * rng.standard_normal(reps)
print(f"replication estimate of the chosen segments: {new.mean():+.2%} (the first-look estimate was {sel_est.mean():+.1%})")
assert new.mean() < 0.01
# Chance that a truly null chosen segment passes a one-sided replication at 5%
print("pass rate of a replication at one-sided 5% for chosen segments:", f"{np.mean(new / se_seg > norm.isf(0.05)):.1%}")
print("all asserts passed")
```
**Output (my run):**
```text
P(at least one of 40 null segments has p <= 0.01) = 1 - 0.99^40 = 0.331
simulated: 0.331 of null experiments show at least one segment with p <= 0.01
Bonferroni threshold 0.05/40 = 0.00125; p = 0.01 passes? False
BH threshold for rank 1 = 0.00125; p = 0.01 passes? False
SE implied for the segment = 3.5% relative; its 95% CI is +2.2% to +15.8%
best segment: mean estimate +8.0%, mean true effect +0.64%, picked a truly null segment 68% of the time
replication estimate of the chosen segments: +0.63% (the first-look estimate was +8.0%)
pass rate of a replication at one-sided 5% for chosen segments: 7.9%
all asserts passed
```
**Follow-ups:**
- What if the segment had a clear reason to benefit (a device-specific fix)? Then the prior is higher, the claim is a planned hypothesis, and I would still confirm, with a smaller, faster test.
- What if the team wants a rule for subgroup claims? Pre-register a short list of segments, test the interaction, correct for the list size, and mark everything else as exploratory.
- Does the overall flat result mean no segment matters? No; it means no average effect. Segments can offset each other, but find that with planned analysis, not a scan.
**Common mistakes:** Using the 1% level inside the segment and ignoring the 40 chances. Confusing "significant in the segment" with "different from the other segments". Reporting the unshrunk effect as the expected launch gain. Forgetting that the real number of looks was larger.

### Q18 ⭐⭐⭐ 🔴 A test meant to split 1,000,000 users 50/50 has 495,000 in treatment and 505,000 in control. The treatment build crashes at launch on some older phones so those sessions never log events, treatment shows engagement per logged user up 2%, and the product manager says a 1% imbalance is small enough to ignore. Explain what is wrong and what the 2% means.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** A 495,000 versus 505,000 split is a sample ratio mismatch (chi-square 100, p about 1e-23), not a small imbalance; the build that crashes removes users from treatment who are not random, so the +2% per logged user is a survivor effect, and it cannot be read as the feature's effect.
**Clarifying questions:**
- How many users were assigned in each arm according to the assignment service (not the event logs)? The gap between assigned and logged counts the lost users.
- Which phones and OS versions crash, and how do those users behave in control (engagement, spend)? It tells me the direction of the bias.
- Do the crashed users come back (after an update) or are they gone for good? Gone means a real harm of the feature, not only a measurement issue.
- Is the split exactly 50/50 by design? An SRM check is against the planned ratio.
- Can I get a server-side measure for these users (logins, orders)? It lets me measure them without the client logs.
**Approach:**
1. Compute the SRM test: expected 500,000 each, observed 495,000 and 505,000. Chi-square = 5,000^2 / 500,000 x 2 = 100, p about 1e-23. A random split would almost never do this.
2. Say what it means: the arms no longer hold the same kind of people. Treatment lost users who crash, so the comparison is between survivors in treatment and everyone in control. The estimate is biased and the usual p-values are not valid. Book 1 Part 10, Q6 (What is a Sample Ratio Mismatch (SRM)?) lists the causes and tests.
3. Bound the bias with a quick calculation: if f of the treatment arm is missing and the missing users engage at a share r of the average, the survivor mean is (1 - f r) / (1 - f) times the arm mean. With f about 2% and r near 0, the inflation can be about +2%, the same size as the reported lift.
4. Confirm the cause: count users by device model and OS version in each arm; the missing ones should sit in the older phones. The 1% imbalance is that 1 point of the split; the size of the lost group is about 2% of the treatment arm.
5. Do what the data allows: analyse on the assignment log (all users assigned, intention-to-treat) using server-side outcomes; or compare only the unaffected devices (by pre-defined device filter in both arms); or fix the crash and re-run.
6. Tell the manager: the +2% is not a result, the crash is a real product bug that harms some users, and the test restarts after the fix.
**Metrics:**
- SRM chi-square = sum over arms of (observed - expected)^2 / expected; p-value from a chi-square with 1 degree of freedom.
- Lost share = (assigned - logged) / assigned in treatment.
- Engagement per assigned user (all assigned users in the denominator) from server-side data; compare with engagement per logged user.
- Guardrails: crash-free sessions, device-model mix per arm, app-store rating.
**Risks:**
- Reading the result on logged users only: survivors look better.
- Dropping the affected devices from only one arm and not the other.
- Fixing the crash mid-test and mixing two regimes.
- Assuming the bias goes up: it depends on whether the lost users are heavy or light users. Here they are older-phone users, who typically engage less in this illustration, but check it in control.
**What the interviewer scores:**
- Strong: computes the SRM test and rejects "1% is small". Weak: "50.5% versus 49.5% is close enough".
- Strong: explains the mechanism (non-random loss, survivor bias) and bounds the effect. Weak: lists causes without linking to the 2%.
- Strong: distinguishes the measurement problem from the real product harm. Weak: only data cleaning.
- Strong: gives a path (analyse on assignment, fix, re-run). Weak: stops at "invalid".
**Example:** Illustrative numbers. Assume 505,000 users were assigned to each arm and 10,000 treatment users never log (1.98% of the arm). If the true effect is zero and the lost users engage at 5% of normal, the logged-user lift comes out at about +2.15% in my simulation; the upper limit with lost users at 0 engagement is +2.02% in expectation (the simulated number can sit slightly above it because of sampling noise, about 0.15 points). If only 5,000 were missing of 500,000 each, the limit would be +1.01%, so the 2% needs the larger loss.
- Weak answer: "The imbalance is only 1%, and treatment is up 2%, so ship."
- Strong answer: "That split is not random. The lost users are the ones the build crashes on. The 2% is mostly who remains. I would analyse on all assigned users with server-side data and fix the crash first."
**Code:**
```python
# Q18: SRM from a crash on older phones and the '+2% per logged user' (illustrative simulation)
import numpy as np
from scipy.stats import chisquare

# 1) SRM test on the observed counts
obs = np.array([495_000, 505_000])
exp = np.array([500_000, 500_000])
chi2, p = chisquare(obs, exp)
print(f"chi-square = {chi2:.0f}, p = {p:.1e}")
assert round(chi2) == 100 and p < 1e-20

# 2) Largest bias that dropping f of the arm can create: survivors vs the whole arm
#    survivor mean / whole-arm mean = (1 - f*r)/(1 - f), where r = mean of dropped users / overall mean
assigned_c = 505_000
logged_t = 495_000
f = (assigned_c - logged_t) / assigned_c       # assumes both arms were assigned 505,000
print(f"share of treatment users missing (if assigned 505,000 each): {f:.2%}")
print(f"maximum possible inflation (dropped users engage 0): {f/(1-f):+.2%}")
assert abs(f - 0.0198) < 0.0001 and abs(f/(1-f) - 0.0202) < 0.0002
f_small = 5_000 / 500_000                       # if each arm was assigned 500,000
print(f"if only 5,000 were missing of 500,000: max inflation {f_small/(1-f_small):+.2%}")
assert f_small / (1 - f_small) < 0.0102

# 3) Simulation: true treatment effect is ZERO; dropped users are older-phone users who engage less
rng = np.random.default_rng(18)
n = 505_000
def make_arm(drop):
    old = rng.random(n) < 0.0198                       # older phones
    base = rng.gamma(2.0, 5.0, n)                      # engagement per user, mean 10
    eng = np.where(old, base * 0.05, base)             # older-phone users engage at 5% of normal
    keep = ~(old & drop)                               # in treatment their sessions never log
    return eng, keep
ec, kc = make_arm(False)
et, kt = make_arm(True)
print(f"logged users: control {kc.sum():,}, treatment {kt.sum():,}")
naive = et[kt].mean() / ec[kc].mean() - 1
itt = et.mean() / ec.mean() - 1     # all assigned users, missing sessions counted as the engagement they have (0 if lost)
et_itt = np.where(kt, et, 0.0)
itt_zero = et_itt.mean() / ec.mean() - 1
print(f"naive per logged user lift = {naive:+.2%} (true effect 0)")
print(f"analysis on ALL assigned users, lost users counted as zero: {itt_zero:+.2%}")
se_rel = np.sqrt(et[kt].var()/kt.sum() + ec[kc].var()/kc.sum()) / ec[kc].mean()
print(f"sampling noise (1 SE) of that lift = {se_rel:.2%}")
assert se_rel < 0.002
assert 0.015 < naive < 0.022 and abs(itt_zero) < 0.01
print("all asserts passed")
```
**Output (my run):**
```text
chi-square = 100, p = 1.5e-23
share of treatment users missing (if assigned 505,000 each): 1.98%
maximum possible inflation (dropped users engage 0): +2.02%
if only 5,000 were missing of 500,000: max inflation +1.01%
logged users: control 505,000, treatment 495,073
naive per logged user lift = +2.15% (true effect 0)
analysis on ALL assigned users, lost users counted as zero: +0.14%
sampling noise (1 SE) of that lift = 0.15%
all asserts passed
```
**Follow-ups:**
- Would reweighting the survivors fix it? Only if the lost users are like the survivors given observed device features; the crash selects on something unobserved too (how much they use the app). Reweighting is a sensitivity check, not a fix.
- How do you catch this earlier? An automatic SRM alert on day 1 and a crash-rate guardrail in both arms.
- Can the effect be bounded without the lost users? Yes, with worst-case or trimming bounds: assume the lost users would have engaged at the lowest and highest plausible level and report the range.
**Common mistakes:** Treating the SRM as a rounding issue. Computing engagement per logged user. Dropping older phones from treatment only. Not telling the product team about the crash.

### Q19 ⭐⭐ 🟢 An A/A test across 40 metrics shows 3 metrics with p < 0.05, and an engineer says the experimentation platform is broken. If every metric had no true difference and the tests were independent, about 2 of 40 would cross 5% by chance. Explain how you decide whether the platform is broken and what else you check.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Three hits out of 40 in one A/A test is normal: I expect 2, and 3 or more happens about 32% of the time, so I would not call the platform broken from one run; I would look at the p-value distribution over many A/A runs.
**Clarifying questions:**
- How many A/A tests have we run, and is this the first one? One run gives almost no information about a 5% rate.
- Are the 3 metrics related to each other (clicks, sessions, pageviews)? Related metrics hit together, so it counts as one event, not three.
- Are the same 3 metrics flagged in repeated A/A runs? A repeat points to a bug, a random hit does not.
- Is the unit of analysis equal to the unit of randomization (user in both)? A mismatch inflates false positives.
- Does the A/A pass the SRM check? A bad split would show up there first.
**Approach:**
1. Do the arithmetic: 40 x 0.05 = 2 expected hits. With independent null metrics, 3 or more hits has probability about 32% (binomial).
2. Run many A/A tests (hundreds, using replays of past traffic with random splits). Collect the p-values of each metric. For a healthy platform they are about uniform from 0 to 1, and about 5% fall below 0.05. Book 1 Part 10, Q21 (What is A/A testing and why would you run one?) explains the purpose.
3. Check the same metrics across runs: if the same 3 keep failing, look at their variance calculation (ratio metrics, clustering by user, heavy tails).
4. Check the pipeline basics: SRM, assignment hashing, a unit mismatch (page views analysed as if independent), bot filtering, double logging.
5. Decide: not broken if the rate over many runs is about 5% and p-values are uniform; broken if the false positive rate is well above 5% (for example 17% when the standard error is understated by 30%).
6. Fix the process: use a multiple-metrics policy (one primary, a few guardrails, correction) so a random hit does not drive a decision.
**Metrics:**
- False positive rate per metric = A/A runs with p below 0.05 / total A/A runs; should be about 0.05.
- Uniformity of p-values: Kolmogorov-Smirnov test against the uniform distribution, or a histogram.
- Hits per run: mean should be about 2 for 40 metrics, with the spread depending on correlation between the metrics.
- Guardrail: SRM p-value in each run.
**Risks:**
- Over-reading one run in either direction (either "platform broken" or "platform fine" from a single run).
- Correlated metrics: the average number of hits is still 2, but runs have either 0 hits or clumps; with correlation 0.9, 81% of runs show 0 hits.
- Re-running A/A until it passes is the same trap as peeking.
- An A/A on a quiet week does not test seasonal or heavy-tailed behaviour.
**What the interviewer scores:**
- Strong: computes 2 expected and about 32% for 3 or more. Weak: says "3 is more than 2, so something is wrong".
- Strong: proposes many A/As and p-value uniformity. Weak: proposes to "run another one" only.
- Strong: mentions correlated metrics and the unit mismatch. Weak: only multiple testing.
- Strong: says what would prove a bug (rate far above 5%, repeated same metrics). Weak: no criterion.
**Example:** Illustrative numbers. 40 independent null metrics at 5%: expected 2 hits, P(0 hits) 12.9%, P(exactly 3) 18.5%, P(3 or more) 32.3%. If metrics are correlated at 0.9, P(0 hits) is about 81% and P(3 or more) about 12%, yet the mean is still 2. A broken variance estimate (SE 30% too small) gives a false positive rate of about 17% per metric.
- Weak answer: "Three of 40 failed, the platform is broken."
- Strong answer: "Two are expected, and three or more shows up about a third of the time. I will run a few hundred A/As and check the p-value histogram and the SRM before I say anything."
**Code:**
```python
# Q19: A/A test with 40 metrics: 3 hits at 5%. Is the platform broken? (simulation)
import numpy as np
from scipy.stats import binom, kstest, ttest_ind

m, a = 40, 0.05
print(f"expected hits by chance = {m * a:.1f}")
p_ge3 = binom.sf(2, m, a)
print(f"P(3 or more hits among 40 independent null metrics) = {p_ge3:.3f}")
print(f"P(exactly 3) = {binom.pmf(3, m, a):.3f}; P(0 hits) = {binom.pmf(0, m, a):.3f}")
assert abs(m * a - 2.0) < 1e-12 and 0.31 < p_ge3 < 0.33

# One A/A run is weak evidence. Run many A/A tests on one metric: p-values should be uniform.
rng = np.random.default_rng(19)
pvals = np.array([ttest_ind(rng.normal(10, 3, 2000), rng.normal(10, 3, 2000)).pvalue for _ in range(3000)])
ks = kstest(pvals, "uniform")
print(f"3000 A/A runs, one metric: false positive rate {np.mean(pvals < 0.05):.3f}; KS test vs uniform p = {ks.pvalue:.2f}")
assert abs(np.mean(pvals < 0.05) - 0.05) < 0.015 and ks.pvalue > 0.01

# Correlated metrics: hits come in clumps (clicks, sessions, pageviews move together)
def hits(corr, reps=4000):
    cov = np.full((m, m), corr); np.fill_diagonal(cov, 1)
    L = np.linalg.cholesky(cov)
    z = rng.standard_normal((reps, m)) @ L.T
    return (np.abs(z) > 1.96).sum(axis=1)
for c in (0.0, 0.5, 0.9):
    h = hits(c)
    print(f"corr {c}: mean hits {h.mean():.2f}, P(>=3) {np.mean(h >= 3):.3f}, P(0 hits) {np.mean(h == 0):.3f}")
h0, h9 = hits(0.0), hits(0.9)
assert abs(h0.mean() - 2.0) < 0.1 and abs(h9.mean() - 2.0) < 0.2 and np.mean(h9 == 0) > np.mean(h0 == 0)

# A faulty platform shows up in repeated runs: a broken variance estimate (SE too small by 30%) gives too many hits
bad = np.mean(np.abs(rng.standard_normal(200_000) / 0.7) > 1.96)
print(f"if the SE were understated by 30%, the false positive rate would be {bad:.3f} (not 0.05)")
assert bad > 0.15
from scipy.stats import norm
n_needed = (norm.isf(0.025) * np.sqrt(0.05 * 0.95) + norm.isf(0.2) * np.sqrt(0.07 * 0.93)) ** 2 / 0.02 ** 2
print(f"run-metric pairs to tell a 5% rate from 7% (one-sample, 80% power): {n_needed:,.0f}")
assert 950 < n_needed < 1100
print("all asserts passed")
```
**Output (my run):**
```text
expected hits by chance = 2.0
P(3 or more hits among 40 independent null metrics) = 0.323
P(exactly 3) = 0.185; P(0 hits) = 0.129
3000 A/A runs, one metric: false positive rate 0.052; KS test vs uniform p = 0.10
corr 0.0: mean hits 2.00, P(>=3) 0.318, P(0 hits) 0.125
corr 0.5: mean hits 1.99, P(>=3) 0.230, P(0 hits) 0.427
corr 0.9: mean hits 2.08, P(>=3) 0.123, P(0 hits) 0.812
if the SE were understated by 30%, the false positive rate would be 0.169 (not 0.05)
run-metric pairs to tell a 5% rate from 7% (one-sample, 80% power): 1,030
all asserts passed
```
**Follow-ups:**
- How many A/A runs are enough? To tell 5% from 7% with a margin you need around a thousand run-metric pairs; use the platform's replay of past traffic to get them cheaply.
- Why do A/A tests sometimes fail on ratio metrics? The standard error ignores that impressions of one user are correlated; the fix is the delta method or analysis at user level (see Q8).
- Should we correct 40 metrics? Pick one primary metric for the decision and treat the others as guardrails or exploratory.
**Common mistakes:** Reading three hits as a bug. Re-running until the A/A is clean. Forgetting that correlated metrics hit together. Not checking SRM first.

### Q20 ⭐⭐ 🟢 Treatment revenue is 1,060,000 against 1,000,000 for control (+6% relative to control) with 100,000 users per arm. Twelve treatment accounts with automated behaviour (thousands of page views a day) contribute 30,000 of the treatment revenue, and without them the lift is +3% relative. Explain how you decide on filtering, what you report, and how you keep such accounts out of future tests.
**Asked at:** Bot and outlier contamination material (Algolia engineering and docs pages on outliers in A/B tests, a Peakhour post on bots corrupting A/B data; the latter is vendor marketing); mostly practitioner pages, so scenario is partly editor-designed; search snippets only, not opened
**Say this first (1 line):** Twelve accounts out of 100,000 produce 30,000 of the treatment revenue, so the honest lift is +3%, not +6%; I would remove them with a rule that does not look at the revenue or the arm, report both numbers, and put bot filtering in the platform before any test starts.
**Clarifying questions:**
- How were the 12 accounts identified (page views per day, no human signals, an IP range)? The rule must not depend on revenue or on the arm.
- How many similar accounts are in control? If none, the arms were not equal in bots, which is itself odd (12 of 12 bots in treatment by chance is about 0.02%).
- Did these accounts pay real money (resellers, power users, partners) or is it automated traffic with test payments? Real heavy buyers are not bots and belong in the data.
- Are the 12 accounts used on purpose by the business (an API partner)? Then they need their own segment.
- Did the treatment change something that bots exploit (a price bug, a coupon)? Then the bots are part of the finding.
**Approach:**
1. Check the arithmetic: (1,060,000 - 30,000) / 1,000,000 = +3.0%, so half the headline lift comes from 12 accounts (2,500 each, against a normal mean of 10).
2. Look at control with the same rule: how many accounts exceed the threshold? If the arms differ in bots, find the entry path (a campaign, a referral link). Assigned-at-random bots should be about equal across arms.
3. Define the filter by behaviour that does not use the outcome: page views per day above a high threshold, no mouse or touch events, headless user agents, repeated identical sessions. Apply it identically to both arms before looking at the result.
4. Report both: raw lift (+6%) and filtered lift (+3%) with the number of removed accounts (12) and why. Do not hide the raw one. Book 1 Part 10, Q25 (How do you handle outliers and heavy-tailed metrics?) covers winsorizing and trimming as a second line of defence.
5. Add a robustness check that needs no labels: winsorize revenue at a high percentile (99.9th) and compare. In my run it gives about +3.2%.
6. Fix the platform: a standard traffic filter before assignment or before analysis, an alert when top accounts hold a large share of a metric, and a test-by-test review of the top 20 accounts.
**Metrics:**
- Revenue per assigned user = total revenue / assigned accounts, per arm, before and after filtering.
- Share of arm revenue held by the top 12 accounts (30,000 / 1,060,000 = 2.8% of the treatment revenue, and 100% of the 3 points of excess lift).
- Filter precision and recall: flagged accounts that are bots / flagged; bots caught / known bots (check on a labelled sample).
- Guardrails: number of filtered accounts per arm (should be about equal), conversion rate among normal users.
**Risks:**
- Filtering on revenue or on the result is p-hacking: it picks the outliers that favour the answer.
- Dropping genuine heavy buyers removes the real tail and changes who the result is about.
- A rule built after seeing the result may fit that result; fix the rule in the platform and apply it in advance.
- The 12 accounts might respond to treatment in a way that matters (a pricing bug); then investigate.
**What the interviewer scores:**
- Strong: does the +3% arithmetic and says half the lift is bots. Weak: "remove outliers" with no rule.
- Strong: a pre-specified behavioural rule, applied to both arms, and both numbers reported. Weak: removes the top 12 by revenue.
- Strong: asks why bots landed unevenly across arms. Weak: ignores it.
- Strong: proposes a long-term control (a platform filter and alerts). Weak: only fixes this test.
**Example:** Illustrative numbers. Control 1,000,000; treatment 1,060,000 (+6%). Twelve accounts have 2,500 each (30,000). Without them treatment is 1,030,000 (+3.0%). The page-view rule "more than 1,000 a day" flags all 12 bots and 0 of 200,000 normal accounts in my simulation. If 12 bots had landed at random, all 12 landing in treatment has probability 0.00024.
- Weak answer: "Plus 6%, significant, ship."
- Strong answer: "Half of that is 12 automated accounts. Filtered, the lift is 3%, and I will report both and fix the filter before the next test."
**Code:**
```python
# Q20: 12 automated accounts create half of a +6% lift (illustrative simulation built to match the prompt)
import numpy as np
from scipy.stats import ttest_ind, binom

rng = np.random.default_rng(20)
n = 100_000
# normal users: heavy-tailed revenue, rescaled so control total is exactly 1,000,000
ctrl = rng.lognormal(0, 1.2, n); ctrl *= 1_000_000 / ctrl.sum()
base = rng.lognormal(0, 1.2, n)
treat_real = base * (1_030_000 / base.sum())         # genuine users: +3% in total
bots = np.full(12, 2_500.0)                          # 12 accounts, 30,000 in total
treat = np.concatenate([treat_real, bots])           # 100,012 accounts in the treatment arm
is_bot = np.r_[np.zeros(n, bool), np.ones(12, bool)]

print(f"control total {ctrl.sum():,.0f}; treatment total {treat.sum():,.0f}; bots {bots.sum():,.0f}")
print(f"lift with bots    : {treat.sum() / ctrl.sum() - 1:+.1%}")
print(f"lift without bots : {treat[~is_bot].sum() / ctrl.sum() - 1:+.1%}")
assert round(treat.sum()) == 1_060_000 and abs(treat.sum() / ctrl.sum() - 1.06) < 1e-9
assert abs(treat[~is_bot].sum() / ctrl.sum() - 1.03) < 1e-9

def report(label, t, c):
    r = ttest_ind(t, c, equal_var=False)
    print(f"{label:28} lift {t.mean() / c.mean() - 1:+.2%}  Welch p = {r.pvalue:.4f}")
    return r.pvalue
p_all = report("all accounts", treat, ctrl)
p_clean = report("bots removed", treat[~is_bot], ctrl)

# Winsorize at the 99.9th percentile of the pooled data (no bot labels needed)
cap = np.quantile(np.r_[ctrl, treat], 0.999)
report("winsorized at p99.9", np.minimum(treat, cap), np.minimum(ctrl, cap))
print(f"cap = {cap:.1f} vs a bot's revenue 2,500 and a normal mean of 10")

# a behaviour rule: page views per day (bots: thousands; normal users: a few dozen at most)
views_normal = rng.poisson(8, 2 * n)
views_bots = rng.integers(2_000, 5_000, 12)
rule = 1_000
print(f"rule 'page views/day > {rule}': flags {np.sum(views_bots > rule)} of 12 bots and {np.sum(views_normal > rule)} of {2*n:,} normal accounts")
assert np.sum(views_bots > rule) == 12 and np.sum(views_normal > rule) == 0

# if 12 bots had landed at random in the arms, how likely are all 12 in treatment?
print(f"P(all 12 bots land in treatment by chance) = {binom.pmf(12, 12, 0.5):.5f}")
assert abs(binom.pmf(12, 12, 0.5) - 0.5**12) < 1e-12
print("all asserts passed")
```
**Output (my run):**
```text
control total 1,000,000; treatment total 1,060,000; bots 30,000
lift with bots    : +6.0%
lift without bots : +3.0%
all accounts                 lift +5.99%  Welch p = 0.0000
bots removed                 lift +3.00%  Welch p = 0.0002
winsorized at p99.9          lift +3.16%  Welch p = 0.0000
cap = 206.8 vs a bot's revenue 2,500 and a normal mean of 10
rule 'page views/day > 1000': flags 12 of 12 bots and 0 of 200,000 normal accounts
P(all 12 bots land in treatment by chance) = 0.00024
all asserts passed
```
**Follow-ups:**
- What if you cannot identify bots with confidence? Use trimmed or winsorized metrics as the primary analysis for revenue, and report the raw one as a sensitivity check.
- Should you also drop them from control? Yes, apply the same rule to both arms; dropping only from one arm creates its own imbalance.
- Does removing 12 of 100,000 accounts need an SRM check? The counts should still be close to the split; if filtered counts differ between arms, that is a signal of non-random bot traffic.
**Common mistakes:** Filtering on the outcome. Dropping bots from treatment only. Not reporting the raw result. Treating a power user as a bot. Not asking how bots got into one arm.

### Q21 ⭐⭐ 🟢 A page gets 4,000 users per arm per month with baseline conversion of 2.0%, and the product manager wants to detect a 5% relative lift (0.1 points absolute). That needs about 315,000 users per arm, or roughly 79 months at this traffic. Explain what you tell the manager and what alternatives exist.
**Asked at:** Underpowered-test and MDE material (a Towards Data Science 'what to do when an A/B test result is not significant' article, a Dataford 'non significant test PM wants launch' page, a HackerNoon 'running A/B tests you can't measure' post, a Statsig power-analysis page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** A 5% lift at a 2% baseline needs about 315,000 users per arm, which is 79 months at 4,000 per arm per month, so I would say a classic A/B test cannot answer this question; I would show what the traffic can detect and offer a bigger lift, a more frequent metric, variance reduction, more pages, or a no-test decision.
**Clarifying questions:**
- Is a 5% relative lift really the smallest worth having, or is it a habit? If a 20% lift is the only one that matters, the test needs about 21,000 per arm (5 months).
- What does the page cost to change and to undo? A cheap, reversible change can go with a lower bar.
- Is there a more frequent metric that moves before conversion (click on the offer, add-to-cart)? Is it a good proxy for the 2% conversion?
- Are there other pages or markets with the same change? Pooling traffic shortens the time.
- Is there pre-period data per user? It enables variance reduction.
**Approach:**
1. Check the numbers: n = 315,000 per arm for 2.0% to 2.1% with 80% power and a two-sided 5% level; 315,000 / 4,000 = 79 months.
2. Turn it around for the manager: what can we detect? At 4,000 per arm the minimum detectable lift is 44% relative after 1 month, 25% after 3 months, 18% after 6, 13% after 12 months. Book 1 Part 10, Q14 (What do you do when the A/B test result is statistically insignificant?) explains why a flat result here would prove nothing.
3. List the options with their cost: (a) a bigger target lift (20% needs 5.3 months), (b) a sensitive upstream metric (20% baseline click rate: 6.4 months for a 5% lift), (c) CUPED (a correlation of 0.7 with the pre-period metric cuts months from 79 to 40), (d) apply the same change to 10 similar pages (7.9 months), (e) relax the error rates (one-sided 10% still needs 45 months).
4. Or do not A/B it: ship by design judgement, user research, or a quasi-experiment on a larger scope if the change is cheap and the downside is small.
5. If you ship without a test, monitor with a guardrail and a holdout to catch harm.
6. Write the decision down: "we cannot measure a 5% lift on this page; we chose X".
**Metrics:**
- Conversion = visitors who convert / visitors assigned; the sample size uses its variance p(1 - p).
- MDE (relative) = (1.96 + 0.84) x sqrt(2 p (1 - p) / n) / p.
- Months to run = n per arm / users per arm per month.
- Guardrails for a no-test launch: conversion on the page, error rate, page speed, complaint rate.
**Risks:**
- Running the test for 2 months and reading "not significant" as "no effect".
- A proxy metric that does not carry over to conversion.
- Pooling dissimilar pages hides differences.
- Lowering the power or the confidence silently so the number looks smaller.
**What the interviewer scores:**
- Strong: states the sample size, converts it into months and into MDE. Weak: just "run longer".
- Strong: offers several workable options and the cost of each. Weak: one option only.
- Strong: is willing to say "do not test, decide on judgement" with a safety net. Weak: insists on testing.
- Strong: keeps the manager's goal (a decision) in view. Weak: lectures.
**Example:** Illustrative numbers. 2.0% baseline, 5% lift: 315,000 per arm, 79 months. With CUPED at 0.7: variance x 0.51, so 161,000 per arm, 40 months. With a click metric at 20%: 25,600 per arm, 6.4 months. 21,100 per arm detects a 20% lift in 5.3 months.
- Weak answer: "Run it for 75 months."
- Strong answer: "This traffic can detect a 25% lift in 3 months, not 5%. I propose either a different metric, pooling pages, or shipping with a holdout and monitoring."
**Code:**
```python
# Q21: a test that needs 75 months: what can this traffic detect? (illustrative numbers)
import numpy as np
from scipy.stats import norm

za, zb = norm.ppf(0.975), norm.ppf(0.80)
def n_per_arm(p1, rel_lift, alpha_z=za, power_z=zb):
    p2 = p1 * (1 + rel_lift); pbar = (p1 + p2) / 2
    return (alpha_z * np.sqrt(2 * pbar * (1 - pbar)) + power_z * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2

n = n_per_arm(0.02, 0.05)
monthly = 4_000
print(f"n per arm for 2.0% -> 2.1%: {n:,.0f}; months at {monthly:,}/arm/month = {n / monthly:.0f}")
print(f"the prompt's round figures: 300,000 / 4,000 = {300_000 / monthly:.0f} months")
assert 310_000 < n < 320_000 and 77 < n / monthly < 80 and 300_000 / monthly == 75

def mde_rel(p1, n):
    se = np.sqrt(2 * p1 * (1 - p1) / n)
    return (za + zb) * se / p1
print("\nwhat the traffic can detect (relative MDE at baseline 2.0%):")
for months in (1, 3, 6, 12, 24):
    print(f"  {months:>2} months ({months * monthly:>6,} per arm): MDE = {mde_rel(0.02, months * monthly):.0%}")
assert 0.40 < mde_rel(0.02, 4_000) < 0.46 and 0.12 < mde_rel(0.02, 48_000) < 0.14

# Option A: CUPED with a pre-period covariate (variance x (1 - rho^2)); sample size scales with variance
for rho in (0.3, 0.5, 0.7):
    print(f"CUPED rho {rho}: n = {n * (1 - rho**2):,.0f} per arm, {n * (1 - rho**2) / monthly:.0f} months")
assert abs(n * (1 - 0.7**2) / monthly - 0.51 * n / monthly) < 1e-9

# Option B: a more frequent upstream metric, for example click on the offer at 20% baseline with the same 5% lift
n_up = n_per_arm(0.20, 0.05)
print(f"upstream metric, 20% baseline, 5% lift: n = {n_up:,.0f} per arm, {n_up / monthly:.1f} months")
assert 24_000 < n_up < 27_000

# Option C: accept a larger lift as the target, or a one-sided 10% test
n_big = n_per_arm(0.02, 0.20)
print(f"target 20% relative lift: n = {n_big:,.0f} per arm, {n_big / monthly:.1f} months")
n_one = n_per_arm(0.02, 0.05, alpha_z=norm.ppf(0.90), power_z=norm.ppf(0.80))
print(f"one-sided alpha 0.10 (z = 1.28), 5% lift: n = {n_one:,.0f} per arm, {n_one / monthly:.0f} months")
assert 20_000 < n_big < 22_000 and n_one < n
# Option D: pooling more pages (same change on 10 similar pages) multiplies traffic
print(f"same change on 10 similar pages: {n / (10 * monthly):.1f} months")
print("all asserts passed")
```
**Output (my run):**
```text
n per arm for 2.0% -> 2.1%: 315,206; months at 4,000/arm/month = 79
the prompt's round figures: 300,000 / 4,000 = 75 months

what the traffic can detect (relative MDE at baseline 2.0%):
   1 months ( 4,000 per arm): MDE = 44%
   3 months (12,000 per arm): MDE = 25%
   6 months (24,000 per arm): MDE = 18%
  12 months (48,000 per arm): MDE = 13%
  24 months (96,000 per arm): MDE = 9%
CUPED rho 0.3: n = 286,837 per arm, 72 months
CUPED rho 0.5: n = 236,404 per arm, 59 months
CUPED rho 0.7: n = 160,755 per arm, 40 months
upstream metric, 20% baseline, 5% lift: n = 25,582 per arm, 6.4 months
target 20% relative lift: n = 21,108 per arm, 5.3 months
one-sided alpha 0.10 (z = 1.28), 5% lift: n = 181,033 per arm, 45 months
same change on 10 similar pages: 7.9 months
all asserts passed
```
**Follow-ups:**
- Why not use a Bayesian test to get an answer sooner? The data have the same information; a Bayesian posterior will simply be wide. It helps express uncertainty, not remove it.
- Can sequential testing stop sooner? It can stop early when the true effect is much larger than planned; for a true 5% lift it needs about the same data or a little more, so it does not remove the problem.
- When would you accept a weaker design? When the change is cheap, reversible, and a loss would be small; then use a holdout and a guardrail.
**Common mistakes:** Saying "just wait". Lowering the power quietly. Using an upstream metric without checking it predicts conversion. Treating a non-significant small test as proof that the change is safe.

### Q22 ⭐⭐ 🟢 A food-delivery test ran Tuesday to Thursday (3 days) on 60,000 users per arm and shows a significant lift in orders per user. Weekend days account for about 40% of weekly orders and come with a different mix of customers. Explain whether three days is enough and how you choose the duration.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Three weekday days are not enough: they cover only 36% of weekly orders and none of the weekend, which is 40% of orders and a different crowd, so I would run whole weeks (at least 1, usually 2) and choose the length from the sample size and the weekly cycle.
**Clarifying questions:**
- Which days count as "weekend" here (Sat and Sun, or Fri evening to Sun)? The window must cover all of the heavy days.
- Does the treatment effect differ between weekday and weekend customers (office lunch versus family dinner)? It decides how much the missing days matter.
- Are the 60,000 users per arm the same people for the whole window, and how often does one user order? It affects how many users I need versus how many days.
- Is there a delay in the outcome (cancellations, refunds, repeat orders)? The measurement window extends past the last day.
- Are there events in the window (a holiday, a cricket match, rain, a promotion)? They distort a short window.
**Approach:**
1. Say what the 3 days represent: Tuesday to Thursday, 36% of weekly orders (3 x 12%). The result is valid for weekday customers, not for the week.
2. Check by simulation or past data whether weekday and weekend effects can differ. In my illustration: +5% on weekdays and -3% on weekends gives +5.15% for Tue-Thu only, but the true full-week effect is 0.6 x 5% + 0.4 x (-3%) = +1.8%.
3. Choose the duration: whole weeks, so each day of the week appears equally in both arms; at least one full cycle, usually two to see whether the effect fades (novelty) and to cover paydays or events. Book 1 Part 10, Q5 (How do you decide how long to run an experiment and how many users you need?) has the inputs.
4. Compute the sample size from the variance of orders per user and the smallest lift that matters. In my run the full-week CV is 0.91, so 60,000 users per arm detect about 1.5% relative at 80% power.
5. Read the result by day type as a secondary (pre-planned) cut: weekday and weekend, and say if the signs differ.
6. If a 3-day read is needed urgently, give it as "weekday read: +5% (significant); weekend not yet measured".
**Metrics:**
- Orders per user = orders in the window / users assigned, over the same full window in both arms.
- Weekday versus weekend lift: orders per user in weekday days and weekend days separately, pre-planned.
- Weighted lift = sum over day types of (share of orders x lift): 0.60 x 5% + 0.40 x (-3%) = 1.8% in my illustration.
- Guardrails: cancellation rate, delivery time, order value.
**Risks:**
- Generalising a weekday result to the whole week (the lift can even change sign).
- A short window makes the result sensitive to one-off events.
- Novelty: the first days are not the steady state.
- Weekly customers who order only on the weekend are never exposed in a Tue-Thu window; the metric per user then dilutes unevenly.
**What the interviewer scores:**
- Strong: spots that the sample covers 36% of orders and no weekend, and that the mix differs. Weak: "60,000 users is plenty".
- Strong: uses whole weeks and ties duration to sample size. Weak: picks a round number of days.
- Strong: plans the weekday/weekend cut and explains the weighted result. Weak: ignores heterogeneity.
- Strong: gives the manager an interim statement with limits. Weak: refuses to say anything.
**Example:** Illustrative numbers. Weekly orders: Mon to Fri 12% each, Sat and Sun 20% each, so the weekend is 40% and Tue-Thu is 36%. Treatment effect +5% on weekdays and -3% on weekends. The full-week effect is 0.60 x 5% + 0.40 x (-3%) = +1.8%. In my run, Tue-Thu only shows +5.15% (p below 0.0001), the weekend alone shows -3.91%, and the full week shows +1.25% (p = 0.018), which is within noise of +1.8% (standard error 0.53 points).
- Weak answer: "Significant at 60,000 per arm, so ship."
- Strong answer: "That is a weekday read. The weekend is 40% of orders and may go the other way. I will run two full weeks and report weekday and weekend separately."
**Code:**
```python
# Q22: is Tue-Thu enough for a food-delivery test? (simulation, illustrative numbers)
import numpy as np
from scipy.stats import ttest_ind

rng = np.random.default_rng(22)
n = 60_000
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
share = np.array([0.12, 0.12, 0.12, 0.12, 0.12, 0.20, 0.20])   # Sat + Sun = 40% of weekly orders
assert abs(share.sum() - 1) < 1e-12 and abs(share[5:].sum() - 0.40) < 1e-12
effect = np.array([0.05] * 5 + [-0.03] * 2)                   # weekday customers like it (+5%), weekend customers do not (-3%)

weekly_mean = 3.0                                              # orders per user per week (invented)
taste = rng.gamma(2.0, 0.5, size=(2 * n,))                      # user-level heterogeneity, mean 1
arm = np.r_[np.zeros(n, int), np.ones(n, int)]
lam = weekly_mean * taste[:, None] * share[None, :] * (1 + effect[None, :] * arm[:, None])
orders = rng.poisson(lam)                                      # users x 7 days, one week

def lift(cols, label):
    y = orders[:, cols].sum(axis=1)
    t, c = y[arm == 1], y[arm == 0]
    r = ttest_ind(t, c, equal_var=False)
    print(f"{label:22} lift {t.mean() / c.mean() - 1:+.2%}  p = {r.pvalue:.4f}  (orders/user/week-part: {c.mean():.3f} -> {t.mean():.3f})")
    return t.mean() / c.mean() - 1

l_tt = lift([1, 2, 3], "Tue-Thu only")
l_wk = lift(list(range(7)), "full week")
l_we = lift([5, 6], "weekend only")
true_week = (share * effect).sum()
print(f"true full-week effect = 0.12*5*0.05 + 0.40*(-0.03) = {true_week:+.2%}")
assert abs(true_week - 0.018) < 1e-12
assert l_tt > 0.03 and abs(l_wk - 0.018) < 0.01 and l_we < 0

# Tue-Thu covers only 36% of weekly orders
print(f"Tue-Thu share of weekly orders = {share[1:4].sum():.0%}")
assert abs(share[1:4].sum() - 0.36) < 1e-12

# Precision of the full-week readout: relative MDE for orders per user with 60,000 users per arm
y = orders.sum(axis=1)
cv_week = y[arm == 0].std() / y[arm == 0].mean()
mde_week = 2.8 * cv_week * np.sqrt(2 / n)
se_week = cv_week * np.sqrt(2 / n)
print(f"CV of weekly orders per user = {cv_week:.2f}; SE of the relative lift = {se_week:.2%}; MDE = {mde_week:.2%}")
n_need = 2 * (2.8 * cv_week / true_week) ** 2
print(f"the true weekly effect (+1.80%) is {true_week / mde_week:.1f}x the MDE; users per arm for 80% power at +1.8%: about {n_need:,.0f}")
assert 35_000 < n_need < 45_000
assert 0.01 < mde_week < 0.02 and true_week > 0
print("all asserts passed")
```
**Output (my run):**
```text
Tue-Thu only           lift +5.15%  p = 0.0000  (orders/user/week-part: 1.082 -> 1.138)
full week              lift +1.25%  p = 0.0183  (orders/user/week-part: 3.011 -> 3.049)
weekend only           lift -3.91%  p = 0.0000  (orders/user/week-part: 1.207 -> 1.160)
true full-week effect = 0.12*5*0.05 + 0.40*(-0.03) = +1.80%
Tue-Thu share of weekly orders = 36%
CV of weekly orders per user = 0.91; SE of the relative lift = 0.53%; MDE = 1.47%
the true weekly effect (+1.80%) is 1.2x the MDE; users per arm for 80% power at +1.8%: about 40,288
all asserts passed
```
**Follow-ups:**
- Why not just reweight the Tue-Thu data to the week? Reweighting fixes the order mix, not the unmeasured weekend behaviour; if the weekend customers react differently, you need their data.
- Is one week enough? It covers the cycle once; I prefer two for the novelty check and for the variance across weeks, unless the sample size says one is enough and the stakes are low.
- What if the weekend effect is negative and the weekday effect positive? Report both, compute the weighted effect, and consider a targeted launch (weekday-only treatment) with its own test.
**Common mistakes:** Reading a weekday result as a weekly one. Stopping at a round number of days. Forgetting delayed outcomes. Cutting by weekday afterwards without planning it.

### Q23 ⭐⭐ 🟢 A test compares one control with 4 treatment variants, each tested against control at the 5% level, and variant C wins with p = 0.03 while the other three are not significant. A Bonferroni threshold for 4 comparisons would be 0.0125. Explain how the extra variants change your read of C and what you recommend.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Four variants mean four chances to be fooled, so p = 0.03 on C is a lead, not a win; I would not ship on it, I would confirm C in a clean follow-up unless C was my one pre-declared hypothesis.

**Clarifying questions:**
- Was C the single pre-registered comparison, or were all four equal candidates? If only C was declared, 0.05 is fair for C.
- Is this one primary metric, or did we also look at several metrics? More looks, more false wins.
- What is the cost of shipping a dud and of waiting two weeks? That sets how strict I need to be.
- How big is C's lift and its interval? A tiny lift near the noise floor is the classic winner's curse.
- Can I re-run C against control alone? A fresh test is the cleanest fix.

**Approach:**
1. Count the comparisons: 4 variants against control is 4 tests, plus any extra metrics.
2. Compute the family-wise error: if each test runs at 5%, the chance that at least one of 4 shows p < 0.05 by luck is 1 - 0.95^4 = 18.5% (independent tests).
3. Apply a correction: Bonferroni threshold 0.05 / 4 = 0.0125. C has p = 0.03, so it does not pass. Holm gives the same answer here (smallest p must beat 0.0125).
4. Read the size, not only the p-value: the best of four is biased upward (winner's curse), so shrink the estimate.
5. Recommend: do not call C a winner yet. Run a confirmation test of C against control (pre-registered, fresh traffic), sized for a smaller lift than the one observed. Ship early only if C is cheap, safe and reversible.
6. For next time: pre-register the primary comparison or use a correction from the start (Book 1 Part 10 Q9 covers the multiple-testing theory).

**Metrics:**
- Per-variant lift = conversion(variant) - conversion(control), with a 95% interval. Denominator: users assigned to each arm.
- Family-wise error rate (FWER) = P(at least one false positive) = 1 - (1 - 0.05)^4 = 0.1855 for independent tests.
- Corrected threshold = 0.05 / 4 = 0.0125 (Bonferroni).
- Guardrails: SRM check on all five arms, and the guardrail metrics, before any lift is read.

**Risks:**
- Treating "the others are not significant" as proof that C is special. Chance alone often produces one winner.
- Over-correcting: Bonferroni is conservative when tests share a control, so a real lift can be missed. The answer is a bigger confirmation test, not a lower bar forever.
- Splitting traffic five ways cuts sample per arm, so every comparison is weaker than a simple A/B.
- Reporting C's observed lift as the expected lift in production.

**What the interviewer scores:**
- Strong: counts the comparisons and states 1 - 0.95^4 and 0.0125 unprompted. Weak: "p is 0.03, below 0.05, ship".
- Strong: separates "is there an effect" (corrected p) from "how big" (shrunk estimate, winner's curse). Weak: quotes the raw lift.
- Strong: gives a practical next step (confirm test, pre-register). Weak: says only "use Bonferroni" and stops.
- Strong: notes that a single declared hypothesis changes the answer. Weak: treats every test as the same.

**Example:** illustrative numbers. Control 10% conversion, 5,000 users per arm, variants A to D. C shows 11.2% (p = 0.03). The other three are within noise.
- Weak: "C beat control at p = 0.03, ship C."
- Strong: "With four variants there is an 18.5% chance of some false win. C misses the 0.0125 bar. I would re-test C alone, and expect a lift smaller than 1.2 points."
- In my run (simulation below), when all four variants are identical to control, at least one shows p < 0.05 in 16.0% of experiments (less than 18.5% because the four tests share one control and so are positively correlated). Only 4.6% pass 0.0125. When all four have the same tiny true lift (+0.20 points), the best significant variant is reported at +0.75 points, about 3.7 times too big. A null winner re-tested alone passes again only 4.8% of the time.

**Code:**
```python
# Q23: 4 variants vs one control, winner at p=0.03 (illustrative simulation, seeded)
import numpy as np
from scipy import stats

rng = np.random.default_rng(23)
K, ALPHA = 4, 0.05
print("Bonferroni threshold:", ALPHA / K, "; family-wise error if each test is run at 5%:", round(1 - 0.95**K, 4))
assert abs(ALPHA / K - 0.0125) < 1e-12 and abs((1 - 0.95**K) - 0.1855) < 1e-3

# Holm with the prompt's p-values: C = 0.03, the other three are above 0.05 (use 0.06, 0.20, 0.50)
p = np.array([0.03, 0.06, 0.20, 0.50])
order = np.argsort(p)
holm_ok = [p[i] <= ALPHA / (K - rank) for rank, i in enumerate(order)]
print("Holm: smallest p 0.03 vs threshold", ALPHA / K, "->", "reject" if holm_ok[0] else "do not reject")
assert not holm_ok[0]

# 1) all four variants are truly identical to control: how often does at least one 'win'?
n, base, reps = 5000, 0.10, 20000
ctrl = rng.binomial(n, base, reps) / n
var = rng.binomial(n, base, (reps, K)) / n
se = np.sqrt(2 * base * (1 - base) / n)
z = (var - ctrl[:, None]) / se
pv = 2 * (1 - stats.norm.cdf(np.abs(z)))
any5 = (pv.min(axis=1) < ALPHA).mean()
anyb = (pv.min(axis=1) < ALPHA / K).mean()
print(f"all-null sims: P(any variant p<0.05)={any5:.3f}  P(any p<0.0125)={anyb:.3f}")
assert 0.14 < any5 < 0.185 and 0.04 < anyb < 0.05   # below 18.55% / 5%: the four tests share one control, so they are positively correlated

# 2) winner's curse: every variant has the SAME small true lift (+0.2 points on a 10% base), best significant one is reported
n2, true = 20000, 0.002
c2 = rng.binomial(n2, base, reps) / n2
v2 = rng.binomial(n2, base + true, (reps, K)) / n2
se2 = np.sqrt(2 * base * (1 - base) / n2)
d2 = v2 - c2[:, None]
p2 = 2 * (1 - stats.norm.cdf(np.abs(d2 / se2)))
best = d2.argmax(axis=1)
sel = p2[np.arange(reps), best] < ALPHA
est = d2[np.arange(reps), best][sel].mean()
print(f"true lift {true*100:.2f} pts; mean estimate of the best significant variant {est*100:.2f} pts (n={sel.sum()} of {reps} sims)")
assert est > 1.5 * true

# 3) a fresh confirmation test of a null winner: only 5% pass again
conf = rng.binomial(n, base, (reps, 2))
zc = (conf[:, 1] - conf[:, 0]) / n / se
print("null winner re-tested alone, P(p<0.05 again) =", round((np.abs(zc) > 1.96).mean(), 3))
assert abs((np.abs(zc) > 1.96).mean() - 0.05) < 0.01
```

**Output (my run):**
```text
Bonferroni threshold: 0.0125 ; family-wise error if each test is run at 5%: 0.1855
Holm: smallest p 0.03 vs threshold 0.0125 -> do not reject
all-null sims: P(any variant p<0.05)=0.160  P(any p<0.0125)=0.046
true lift 0.20 pts; mean estimate of the best significant variant 0.75 pts (n=5358 of 20000 sims)
null winner re-tested alone, P(p<0.05 again) = 0.048
```

**Follow-ups:**
- What if C had been the only variant declared in advance? Then 0.03 against 0.05 is a fair single test, and I would still check the guardrails and the lift size.
- What about Holm or Benjamini-Hochberg? Holm is uniformly less conservative than Bonferroni with the same FWER guarantee; BH controls the false discovery rate and suits screening many ideas, not a ship decision.
- Does the shared control matter? Yes. The four comparisons are correlated, so Bonferroni is a little conservative (the simulation shows 16.0% rather than 18.5%).

**Common mistakes:** Calling the one significant variant a winner. Dividing 0.05 by 4 and then ignoring the size of the effect. Forgetting the winner's curse. Dropping the other three variants from the story. Using a correction after the fact on only the metrics that look good.

### Q24 ⭐⭐ 🟢 A product manager randomizes each page view independently to the old or new checkout design, so one user can see both designs in one session, and reports 5.2% conversion per page view for new against 5.0% for old (+4% relative). Explain what is wrong with this randomization unit and how you would fix it.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Randomizing each page view lets one person see both designs, so the groups are mixed, the effect leaks across views, and the standard errors are wrong; I would randomize by user, keep them in one arm, and analyse per user.

**Clarifying questions:**
- Is conversion measured per page view or per user or session? A user-level outcome copied onto many view rows is the worst case for the standard error.
- How many views does a typical user have in a session? That decides how bad the mixing is.
- Can I identify the user (login or stable cookie) before the first checkout page? I need a stable ID to assign on.
- Does seeing one design change how people behave on the next view (learning, trust, confusion)? That is carryover.
- Do we also need to compare across sessions or devices? That picks user ID over session or cookie.

**Approach:**
1. Name the problem: the unit of randomization (page view) is smaller than the unit of behaviour (the person making a purchase). One user sits in both arms.
2. Three consequences. (a) Carryover: what a person saw earlier changes what they do now, so control views are not pure control. (b) Dependence: views from one person are correlated, so a test that treats views as independent understates the noise. (c) Heavy users count many times, so the metric is weighted by activity.
3. Fix the design: hash a stable user ID to an arm, so the same person always sees the same design (Book 1 Part 10 Q4 covers choosing the unit).
4. Fix the analysis: one row per user, conversion = purchased at least once (or revenue per user). Denominator = users assigned, including those who never reached checkout, or a triggered denominator defined the same way in both arms.
5. If the design is already run, treat the +4% as unreliable. At best re-analyse with user-clustered standard errors, but the carryover bias cannot be repaired afterward, so re-run.
6. Check SRM at the user level.

**Metrics:**
- Primary: users who purchased / users assigned, per arm. Not conversions / page views.
- Secondary: revenue per user.
- Guardrails: SRM on users, page latency, error rate.
- Report the lift with a user-level confidence interval.

**Risks:**
- Carryover shrinks the true difference, so a page-view test can show a smaller (or oddly signed) effect than the real one.
- Standard errors are too small if the same user's outcome appears on many rows.
- Different designs on consecutive pages can confuse users (checkout steps that do not match) and hurt both arms.
- Weighting by views overweights people who reload a lot.

**What the interviewer scores:**
- Strong: says "unit of randomization should match the unit of the outcome and of the behaviour". Weak: "page views are a big sample, so it is good".
- Strong: lists carryover and dependence as two separate problems. Weak: names only one.
- Strong: proposes user-level assignment and a user-level analysis. Weak: only suggests a bigger test.
- Strong: notes that the 5.2% versus 5.0% cannot be trusted either way. Weak: argues about whether +4% is big.

**Example:** illustrative numbers. 400,000 users, each with 1 to 8 page views. True effect: once a user has seen the new design, conversion is +1.0 point (5% to 6%), whichever design the current view shows.
- Weak: "5.2 against 5.0 is +4%, the new design wins."
- Strong: "The unit is wrong. Randomize by user, then analyse per user."
- In my run, user-level randomization recovers +1.04 points (truth 1.00). Page-view randomization gives only +0.36 points, because after the first new view the control views are partly treated. If the user's session outcome is copied onto every view row, the naive standard error is 0.016 points but the true user-level one is 0.034 points, 2.12 times bigger.

**Code:**
```python
# Q24: page-view randomization vs user randomization (illustrative simulation, seeded)
import numpy as np

rng = np.random.default_rng(24)
print("relative lift quoted:", round(5.2 / 5.0 - 1, 3))
assert abs(5.2 / 5.0 - 1 - 0.04) < 1e-9

U = 400000
views = rng.integers(1, 9, U)                  # 1..8 page views per user
uid = np.repeat(np.arange(U), views)
pos = np.arange(len(uid)) - np.repeat(np.cumsum(views) - views, views)   # 0-based view index inside the user
base, delta = 0.05, 0.01                       # true effect of 'having seen new': +1 point

def lift(arm):
    # carryover: a user who has seen the new design at or before this view keeps the benefit, whichever design this view shows
    first_new = np.minimum.reduceat(np.where(arm == 1, pos, 99), np.cumsum(views) - views)
    seen = pos >= first_new[uid]
    y = rng.random(len(uid)) < base + delta * seen
    return y[arm == 1].mean() - y[arm == 0].mean()

est_view = lift(rng.integers(0, 2, len(uid)))
est_user = lift(rng.integers(0, 2, U)[uid])
print(f"estimated lift in points: page-view randomization {est_view*100:.2f}; user randomization {est_user*100:.2f}; truth 1.00")
assert abs(est_user - 0.01) < 0.002 and est_view < 0.7 * est_user

# SE problem: if the metric is 'user converted in the session' copied onto every view row, the rows are clones.
conv = rng.random(U) < 0.05
y_row = conv[uid].astype(float)
se_naive = np.sqrt(y_row.var() / len(y_row))
se_user = np.sqrt(conv.var() / U)
print(f"rows={len(y_row)}, users={U}: naive SE {se_naive*100:.3f} pts vs user-level SE {se_user*100:.3f} pts; true SE is {se_user/se_naive:.2f}x bigger")
assert se_user / se_naive > 1.5
```

**Output (my run):**
```text
relative lift quoted: 0.04
estimated lift in points: page-view randomization 0.36; user randomization 1.04; truth 1.00
rows=1800735, users=400000: naive SE 0.016 pts vs user-level SE 0.034 pts; true SE is 2.12x bigger
```

**Follow-ups:**
- Is page-view randomization ever fine? Yes, for effects that act only on that single view, no memory, and an outcome measured per view (for example a ranking test on one results page with independent requests). Checkout is a journey, so no.
- What if users are anonymous? Use the best stable ID (device cookie, with the cross-device problem in Q25), and keep the assignment sticky for the whole test.
- Can I fix it with clustered standard errors? That fixes the noise estimate, not the carryover bias.

**Common mistakes:** Calling +4% relative a big win without a user-level view. Using views as the denominator. Treating a big sample of views as a big sample of independent evidence. Fixing the standard errors and keeping the leaky design. Letting a user flip designs mid-session.

### Q25 ⭐⭐ 🟡 A test was randomized by device cookie, and 50,000 of 1,000,000 users (5%) turn out to appear in both arms because they use two devices. Treatment shows +2% relative lift among all users. Explain which way this contamination biases the result, how to measure it and what you would do about the readout.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Contamination usually biases the lift toward zero, so +2% is probably a floor; I would link the identities, measure the effect on one-device users only, and report both numbers with the reason.

**Clarifying questions:**
- How did we find the 50,000? Only logged-in users can be linked across devices, so unlinked cross-device users may remain. Why it matters: the true contamination could be bigger than 5%.
- Is the outcome measured per user (revenue, retention) or per device? Per user means a mixed user's outcome lands in both arms.
- Does the feature change behaviour that carries across devices (price, recommendations, habit) or only the device screen? Carryover decides whether bias is large.
- Is the 5% of all 1,000,000 users? Then it is 50,000 / 525,000 = 9.5% of each arm's population (475,000 one-device users plus the 50,000 in both), which matters for the size of the dilution.
- Can I still re-assign by user ID? If yes, rerun the test cleanly.

**Approach:**
1. Direction. A mixed user is exposed to treatment on one device. Their behaviour on the other device is partly changed too. So the control arm contains treated behaviour and the contrast shrinks: bias toward zero in the usual case. A real effect is understated, not overstated.
2. Size. If mixed users show the treated outcome in both arms, the observed difference is about the clean effect times (one-device users per arm) / (users per arm) = 475,000 / 525,000 = 0.905. So 2% observed implies roughly 2.2% clean.
3. Measure. Link devices by login or hashed email. Mark users as treatment-only, control-only, both. Compare treatment-only with control-only. Check that the mixed users are not odd (heavy users, high spenders): compare pre-period metrics.
4. Dose-response. Among mixed users, compare those whose treatment exposure was heavy with light exposure; a gradient confirms leakage.
5. Readout. Report the primary result as the one-device comparison (clean) with a note that mixed users were excluded by a pre-defined rule, and give the all-users number as the conservative lower bound. Do not simply drop users without saying so.
6. Fix going forward. Randomize on a user ID (hash of account ID) with the device as a nested attribute (Book 1 Part 10 Q4).

**Metrics:**
- Contamination rate = users seen in both arms / all users = 50,000 / 1,000,000 = 5% (9.5% of each arm).
- Clean lift = mean(treatment-only users) / mean(control-only users) - 1.
- All-users lift = mean(treatment arm, including mixed) / mean(control arm, including mixed) - 1.
- Guardrails: SRM per arm after linking; pre-period balance between treatment-only and control-only.

**Risks:**
- Unlinked cross-device users remain in the "clean" group, so the clean number is still a lower bound.
- Excluding mixed users changes the population (heavier users are more often multi-device). The lift for single-device users may not match the lift for everybody.
- The effect may not carry across devices (screen-specific change). Then contamination is harmless and the direction argument above does not apply.
- Negative interaction (confusion from seeing two designs) could push in either direction.

**What the interviewer scores:**
- Strong: gives a direction and an assumption behind it (toward zero if the effect carries across devices). Weak: "it adds noise".
- Strong: quantifies the dilution (0.905, so 2.0% becomes 2.2%). Weak: stays qualitative.
- Strong: proposes identity linking and a clean-versus-all readout. Weak: only "rerun with user ID".
- Strong: notices unlinked users and population change when excluding. Weak: treats the clean estimate as final.

**Example:** illustrative numbers. 1,000,000 users: 950,000 one-device users split 475,000 and 475,000, plus 50,000 in both arms. Revenue per user 10, SD 5, true effect +2.2%.
- Weak: "Contamination is only 5%, ignore it."
- Strong: "It is 9.5% of each arm. The mixed users sit at the treated level in both arms, so the observed lift is 0.905 of the clean one. I report clean and all-users, and rerun by user ID."
- In my run, the all-users lift is 1.91%, the one-device-only lift 2.11% (true 2.20%; the gap is sampling noise of about 0.1 points), and observed over clean is 0.903, matching 475,000 / 525,000 = 0.905. And 2% / 0.905 = 2.21%.

**Code:**
```python
# Q25: 50,000 of 1,000,000 users sit in both arms (illustrative simulation, seeded)
import numpy as np

rng = np.random.default_rng(25)
N, MIX = 1_000_000, 50_000
pure = N - MIX                                   # 950,000 users on one device only
T_pure = C_pure = pure // 2                      # 475,000 each
print("mixed users as a share of all users:", MIX / N, "; as a share of each arm:", round(MIX / (T_pure + MIX), 4))
assert abs(MIX / (T_pure + MIX) - 0.0952) < 1e-3

mu, sd, tau = 10.0, 5.0, 0.022                    # revenue per user; true effect +2.2%
# model: a mixed user has ONE outcome (own behaviour, exposed to treatment on one device), counted in both arms
y_tp = rng.normal(mu * (1 + tau), sd, T_pure)
y_cp = rng.normal(mu, sd, C_pure)
y_mix = rng.normal(mu * (1 + tau), sd, MIX)      # exposed, so they show the treated level in BOTH arms
mean_T = np.concatenate([y_tp, y_mix]).mean()
mean_C = np.concatenate([y_cp, y_mix]).mean()
obs = mean_T / mean_C - 1
clean = y_tp.mean() / y_cp.mean() - 1
print(f"all-users lift {obs*100:.2f}%; clean lift (pure users only) {clean*100:.2f}%; true {tau*100:.2f}%")
# diluted lift is roughly tau * 475/525
print("dilution factor 475,000/525,000 =", round(T_pure / (T_pure + MIX), 4), "; observed/clean =", round(obs / clean, 3))
assert abs(obs / clean - T_pure / (T_pure + MIX)) < 0.02
assert obs < clean

# the plain-text rule of thumb in the answer: 2% observed implies about 2.2% clean
print("2% / 0.905 =", round(2 / (T_pure / (T_pure + MIX)), 2))
assert abs(2 / (T_pure / (T_pure + MIX)) - 2.21) < 0.01
```

**Output (my run):**
```text
mixed users as a share of all users: 0.05 ; as a share of each arm: 0.0952
all-users lift 1.91%; clean lift (pure users only) 2.11%; true 2.20%
dilution factor 475,000/525,000 = 0.9048 ; observed/clean = 0.903
2% / 0.905 = 2.21
```

**Follow-ups:**
- Could contamination make the lift look bigger? Only if the mixed users are a different, higher-spending group and enter one arm's metric but not the other's, or if exposure to both designs creates a cross-device interaction. Under the plain carryover story it shrinks.
- Can I scale the observed lift up by 1/0.905? As a sensitivity bound, yes, labelled as an assumption. The measured clean lift is the better number.
- How do I prevent it? Assign on account ID where possible, and keep the assignment sticky across devices.

**Common mistakes:** Saying "5%, negligible" without computing the share per arm. Dropping the linked users silently. Assuming the bias is always toward zero without stating why. Forgetting that unlinked users remain. Reporting a scaled-up number as if it were measured.

### Q26 ⭐⭐ 🟡 A ride-hailing app randomizes riders 50/50 for a discount, and treated riders take 5.5 rides per week against 5.0 for control (+10% relative to control). Pickup wait time for control riders rose from 4.0 to 4.4 minutes (+10% relative) compared with the pre-period, because treated riders absorb drivers. Explain what the measured lift represents and how you design a market-level readout.
**Asked at:** Marketplace, interference and switchback material (Dataford 'interference in marketplace experiments', 'marketplace experiment with interference' and 'choose switchback for marketplace dispatch' pages, a DoorDash careers blog post, an arXiv 2022 paper on switchbacks and interference bias, a Statsig marketplace-experimentation page); company practice is described only as the snippets reported it; search snippets only, not opened
**Say this first (1 line):** The +10% is a rider-versus-rider comparison inside a shared pool of drivers, so it overstates what a full rollout would give; I would run a market-level design and read total rides, wait time and driver-side outcomes.

**Clarifying questions:**
- Is driver supply roughly fixed in the short run? If supply is elastic (drivers log on for the discount), the gap is smaller.
- Who pays for the discount (platform, driver, rider)? That changes driver behaviour and the profit metric.
- Did the control riders' rides change, or only their wait? The prompt says wait rose from 4.0 to 4.4 minutes, so control riders are worse off than the pre-period.
- How many markets (cities or zones) can I randomize, and are they independent? That decides market-level power.
- What is the business decision: launch to everyone, or optimise the discount size? That sets the estimand.

**Approach:**
1. State what +10% means. It is the difference between a treated rider and a control rider in the same market. Treated riders took driver time that control riders no longer got, so the control group is pushed down (wait +10%). The difference mixes the direct effect of the discount with harm to the control group. It is not the effect of giving everybody the discount.
2. Name the violation: stable unit treatment value assumption (SUTVA) fails because treated and control riders compete for the same drivers (Book 1 Part 10 Q12).
3. Say what the rollout effect would be: if drivers are the bottleneck, total rides are capped by supply. In a toy model with supply of 5.25 rides per rider-week, user-level A/B reads +10% but full rollout gives +5%.
4. Design the market-level readout. Randomize whole markets (cities, or zones with buffers) to discount or no discount, ideally pairs matched on size and pre-trend. Or use a switchback (alternate the whole market in time blocks; see Book 1 Part 10 Q29) or a geo test (Book 1 Part 10 Q44).
5. Analyse at the market (or market-week) level: total completed rides per rider, wait time, cancellations, driver earnings per hour, driver hours, plus platform margin after the discount.
6. Compare the user-level number and the market-level number. The gap is the size of the interference.

**Metrics:**
- Completed rides per active rider per week = completed rides / riders in the market that week (market level).
- Median and 90th-percentile pickup wait time per market-week.
- Driver utilisation and driver earnings per hour.
- Margin per ride after discount.
- Guardrails: cancellation rate, rider retention, surge or price changes.

**Risks:**
- Few markets means low power and a noisy readout.
- Markets are not independent if drivers move between them. Use buffers or keep neighbours in the same arm.
- Short-run supply is fixed, but in the long run drivers may join, so the long-run effect may differ from the test.
- Discount effects may fade or grow once riders learn about it (novelty).

**What the interviewer scores:**
- Strong: explains that the 10% is partly a transfer from the control group. Weak: "10% lift, launch it".
- Strong: gives a mechanism with supply constraints and a rough bound on the rollout effect. Weak: "interference exists".
- Strong: picks a market-level unit and a metric set that includes the driver side. Weak: only a longer test.
- Strong: uses the gap as a diagnostic. Weak: discards the A/B entirely.

**Example:** illustrative toy model. Without the discount, a rider requests 5.0 rides a week; with it, 5.5. City supply serves 5.25 rides per rider-week.
- Weak: "Treated riders take 10% more rides, so the discount adds 10% to rides."
- Strong: "In a mixed market, +10% is true for the comparison. If everybody gets the discount, demand is 5.5 but supply serves 5.25, so total rides rise 5%, and waits get worse."
- In my run (400,000 riders, Poisson requests, random rationing): the user-level A/B reads treated 5.50 against control 5.00 rides, +9.8%. The full rollout gives 5.25 rides per rider, +5.0%. A market-level design (20 markets, 10 discounted) reads 5.25 against 5.00, +5.0%, matching the rollout. In this toy the user-level A/B overstates the rollout effect about 2.0 times. The prompt's arithmetic is right: 5.5 / 5.0 = +10%, 4.4 / 4.0 = +10%.

**Code:**
```python
# Q26: ride-hailing discount, shared driver supply (illustrative toy model, seeded)
import numpy as np

rng = np.random.default_rng(26)
print("prompt arithmetic: rides", round(5.5 / 5.0 - 1, 3), " wait", round(4.4 / 4.0 - 1, 3))
assert abs(5.5 / 5.0 - 1 - 0.10) < 1e-9 and abs(4.4 / 4.0 - 1 - 0.10) < 1e-9

CAP_PER_RIDER = 5.25     # driver supply: rides per rider-week the whole city can serve (assumption)
BASE, DISC = 5.0, 5.5    # weekly ride requests per rider without / with the discount

def week(n, treated_share, cap_per_rider):
    """n riders in one market; requests ~ Poisson; supply is shared and rationed at random."""
    treated = rng.random(n) < treated_share
    req = rng.poisson(np.where(treated, DISC, BASE))
    cap = int(cap_per_rider * n)
    total = req.sum()
    keep = min(1.0, cap / total)                     # each request is served with the same probability
    served = rng.binomial(req, keep)
    return treated, served

# 1) user-level A/B in one market, 50/50 treated: supply covers total demand (5.25 per rider on average)
t, s = week(400_000, 0.5, CAP_PER_RIDER)
ab = s[t].mean() / s[~t].mean() - 1
print(f"user-level A/B lift: treated {s[t].mean():.2f} vs control {s[~t].mean():.2f} rides -> {ab*100:.1f}%")
assert abs(ab - 0.10) < 0.02

# 2) full rollout: everybody treated, same supply
t, s = week(400_000, 1.0, CAP_PER_RIDER)
roll = s.mean() / BASE - 1
print(f"full rollout: {s.mean():.2f} rides per rider vs 5.00 without discount -> {roll*100:.1f}% (supply caps it)")
assert 0.03 < roll < 0.07

# 3) market-level design: 20 markets, 10 get the discount for everyone, 10 do not; supply scales with market size
res = []
for m in range(20):
    treated_market = m % 2 == 0
    t, s = week(40_000, 1.0 if treated_market else 0.0, CAP_PER_RIDER)
    res.append((treated_market, s.mean()))
tm = np.mean([r for k, r in res if k]); cm = np.mean([r for k, r in res if not k])
print(f"market-level readout: treated markets {tm:.2f} vs control markets {cm:.2f} -> {(tm/cm-1)*100:.1f}%")
assert abs((tm / cm - 1) - roll) < 0.02
print("so the user-level A/B overstates the rollout effect by about", round(ab / roll, 1), "x in this toy")
```

**Output (my run):**
```text
prompt arithmetic: rides 0.1  wait 0.1
user-level A/B lift: treated 5.50 vs control 5.00 rides -> 9.8%
full rollout: 5.25 rides per rider vs 5.00 without discount -> 5.0% (supply caps it)
market-level readout: treated markets 5.25 vs control markets 5.00 -> 5.0%
so the user-level A/B overstates the rollout effect by about 2.0 x in this toy
```

**Follow-ups:**
- Is the user-level test useless? No: it measures the direct response of a rider to the discount, which is an input to the market model. It just must not be presented as the rollout effect.
- What if supply is flexible? Then drivers respond (log on more), the gap shrinks, and the market-level test shows by how much.
- What would you tell the finance team? A range: the user-level +10% as an upper bound, the market-level figure as the planning number, margin after the discount.

**Common mistakes:** Quoting +10% as the rollout effect. Looking only at the rider side. Ignoring that control wait time moved. Randomizing neighbouring zones that share drivers and calling them independent. Forgetting the cost of the discount in the decision.

### Q27 ⭐⭐ 🟡 A social app wants to test a feed change with graph-cluster randomization, using clusters of about 50 users with an intra-cluster correlation of 0.02, and the user-level design needed 100,000 users per arm. The design effect is 1 + (50 - 1) x 0.02 = 1.98. Explain what this means for sample size, how cluster size trades bias against variance, and what you would do if traffic is limited.
**Asked at:** Marketplace, interference and switchback material (Dataford 'interference in marketplace experiments', 'marketplace experiment with interference' and 'choose switchback for marketplace dispatch' pages, a DoorDash careers blog post, an arXiv 2022 paper on switchbacks and interference bias, a Statsig marketplace-experimentation page); company practice is described only as the snippets reported it; search snippets only, not opened
**Say this first (1 line):** A design effect of 1.98 means I need about twice the users, 198,000 per arm instead of 100,000, because a cluster of 50 users carries only about 25 users' worth of information; I would pick the smallest cluster that still contains most friend links.

**Clarifying questions:**
- Where does the ICC of 0.02 come from (the metric, the clusters, a past test)? ICC depends on the metric and the clustering, so I must use the one for this metric and these clusters.
- Are clusters all about 50, or very uneven? Unequal sizes make the design effect larger than 1.98.
- What share of friend links cross clusters? That is the leftover interference bias.
- Is traffic really limited, or is the limit the test duration? Time can buy sample.
- What is the smallest lift worth detecting? That sets the sample need.

**Approach:**
1. Compute it. Design effect = 1 + (m - 1) x ICC = 1 + 49 x 0.02 = 1.98. Users needed per arm = 100,000 x 1.98 = 198,000, which is 198,000 / 50 = 3,960 clusters per arm. The "effective" sample of 198,000 users is 100,000.
2. Explain it in plain words: users in a cluster look alike, so the 50th user adds less than a fresh independent user would.
3. The trade-off. Bigger clusters keep more friend links inside the same arm, so less leakage (interference bias), but the design effect rises with m. Smaller clusters do the opposite. In my toy friend graph a cluster of 10 cuts 55% of links and has a design effect of 1.18; size 50 cuts 11% and costs 1.98; size 200 cuts 2.8% but costs 4.98.
4. Choose the smallest cluster size where the cut share is tolerable, and use a modularity-based graph clustering so clusters are real communities. A true social graph is more clusterable than my ring toy.
5. If traffic is limited: (a) accept a larger minimum detectable effect, which grows with sqrt(1.98) = 1.41; (b) use CUPED with pre-period activity to shrink variance; (c) stratify or pair clusters on size and baseline activity; (d) run longer; (e) measure a more sensitive metric; (f) use ego-network or other designs if clusters are too leaky. Book 1 Part 10 Q51 covers the cluster theory.
6. Analyse at the cluster level (cluster means) or with cluster-robust standard errors. Do not treat users as independent.

**Metrics:**
- Design effect = 1 + (m - 1) x ICC, with m the average cluster size (use the unequal-size version if sizes vary a lot).
- Required users per arm = users per arm for an independent design x design effect.
- Cluster cut share = friend links between clusters / all links.
- Guardrails: SRM at the cluster level, covariate balance of cluster size and baseline activity between arms.

**Risks:**
- Under-estimating the ICC. A larger ICC drives the design effect up quickly.
- Unequal cluster sizes: one giant cluster dominates the arm.
- Residual leakage across cut links still biases the effect toward zero.
- Treating the 198,000 users as 198,000 independent users in the analysis, which gives false confidence.

**What the interviewer scores:**
- Strong: computes 198,000 and 3,960 clusters, and says the information is about the same as 100,000 independent users. Weak: repeats the formula only.
- Strong: explains cluster size as a bias versus variance dial. Weak: says "use bigger clusters" without cost.
- Strong: lists practical levers when traffic is limited (MDE, CUPED, pairing, time). Weak: "get more traffic".
- Strong: says to analyse at the cluster level. Weak: ignores the dependence.

**Example:** illustrative numbers. Independent design: 100,000 users per arm. Clusters of 50, ICC 0.02.
- Weak: "We need 100,000 users per arm, and clusters just make it a little noisier."
- Strong: "DE = 1.98, so 198,000 users per arm, 3,960 clusters per arm. If I only have 100,000 per arm, my MDE is 1.41 times larger."
- In my run, simulated clusters of 50 with ICC 0.02 give a variance ratio of 2.05 against independent users (formula 1.98; sampling noise). In the toy ring graph, going from cluster size 10 to 400 cuts links from 55% to 1.4% while the design effect goes from 1.18 to 8.98.

**Code:**
```python
# Q27: cluster randomization, design effect and the cluster-size trade-off (illustrative, seeded)
import numpy as np

rng = np.random.default_rng(27)
m, rho = 50, 0.02
de = 1 + (m - 1) * rho
print("design effect:", de, "; users per arm needed:", 100_000 * de, "; clusters per arm:", 100_000 * de / m)
assert abs(de - 1.98) < 1e-9 and abs(100_000 * de - 198_000) < 1e-6

# check by simulation: variance of a mean over clusters with ICC 0.02 versus independent users
n_clusters, reps = 400, 4000
sd_between, sd_within = np.sqrt(rho), np.sqrt(1 - rho)
means = np.empty(reps)
for r in range(reps):
    cl = rng.normal(0, sd_between, (n_clusters, 1)) + rng.normal(0, sd_within, (n_clusters, m))
    means[r] = cl.mean()
var_cluster = means.var()
var_iid = 1 / (n_clusters * m)
print(f"simulated variance ratio (clustered / independent) = {var_cluster/var_iid:.2f}")
assert abs(var_cluster / var_iid - de) < 0.15
print("MDE grows by sqrt(DE) =", round(np.sqrt(de), 3))

# trade-off: ring-lattice 'friend graph' (each user linked to 10 neighbours on each side), contiguous clusters
k = 10
print("cluster size | edges cut (share) | design effect")
cuts = {}
for size in (10, 25, 50, 100, 200, 400):
    cut = 0; tot = 0
    for d in range(1, k + 1):                    # edge from i to i+d crosses a boundary if i%size + d >= size
        i = np.arange(size)
        cut += (i + d >= size).sum() / size; tot += 1
    cuts[size] = cut / tot
    print(f"{size:12d} | {cuts[size]:.3f}             | {1 + (size - 1) * rho:.2f}")
assert cuts[400] < cuts[50] < cuts[10] and 1 + 399 * rho > 1 + 49 * rho
```

**Output (my run):**
```text
design effect: 1.98 ; users per arm needed: 198000.0 ; clusters per arm: 3960.0
simulated variance ratio (clustered / independent) = 2.05
MDE grows by sqrt(DE) = 1.407
cluster size | edges cut (share) | design effect
          10 | 0.550             | 1.18
          25 | 0.220             | 1.48
          50 | 0.110             | 1.98
         100 | 0.055             | 2.98
         200 | 0.028             | 4.98
         400 | 0.014             | 8.98
```

**Follow-ups:**
- What if clusters differ in size? Use 1 + ((CV^2 + 1) x mean size - 1) x ICC, where CV is the coefficient of variation of cluster sizes; it is larger than 1.98.
- What if I cannot afford the sample? Test a bigger effect, accept a lower power, or pick a design with less leakage cost, such as a market or geo test.
- How do I report? The effect, the cluster-robust interval, the cut-edge share and the assumption that the leakage is small.

**Common mistakes:** Using 1.98 on the wrong base (applying it to clusters rather than users). Taking the ICC from another metric. Analysing at user level. Choosing the cluster size only on variance, or only on leakage. Ignoring uneven cluster sizes.

### Q28 ⭐⭐ 🟡 A delivery marketplace runs a switchback test on dispatch logic, flipping the whole market between old and new every 30 minutes for 14 days (672 periods, 336 per arm), with about 900 deliveries per period. An analyst computes a z-test on all 604,800 deliveries as if independent. Explain the right analysis unit, the carryover and time-of-day issues, and how you would randomize the periods.
**Asked at:** Marketplace, interference and switchback material (Dataford 'interference in marketplace experiments', 'marketplace experiment with interference' and 'choose switchback for marketplace dispatch' pages, a DoorDash careers blog post, an arXiv 2022 paper on switchbacks and interference bias, a Statsig marketplace-experimentation page); company practice is described only as the snippets reported it; search snippets only, not opened
**Say this first (1 line):** The analysis unit is the time period, not the delivery: I have 672 periods, 336 per arm, not 604,800 independent orders; I would randomize the periods inside each day, analyse period-level with time-of-day controls, and drop or test for carryover.

**Clarifying questions:**
- Is the whole market flipped (one arm at a time), so there are no two arms live in the same period? That is the switchback premise.
- How long does the effect of a dispatch rule linger (couriers repositioning, queue backlog)? That sets period length and burn-in.
- Is demand strongly tied to time of day and day of week? That drives the randomization blocks and the controls.
- What are the primary metrics (delivery time, cost per delivery, orders completed)? They must be defined per period.
- Can the market be treated as one unit? If several markets exist, I can add them for more power.

**Approach:**
1. Analysis unit. The treatment varies by period, and all 900 deliveries in a period share the same market conditions (weather, demand surge, courier supply). So the deliveries are not independent. The sample size is closer to 672 period means than to 604,800 orders (Book 1 Part 10 Q29 covers switchback pitfalls).
2. Test at period level. Compute the average outcome per period (or a ratio of sums), remove the time-of-day pattern, and compare arms. One safe way is a difference per day, then a t-test over 14 days; another is a period-level regression with time-of-day fixed effects and standard errors that allow serial correlation (HAC) or a randomization test.
3. Randomization. Do not use strict alternation. Randomize within each day (24 new, 24 old out of 48 slots), or within day-of-week by slot blocks, so each hour of day appears in both arms. Fix the schedule in advance.
4. Carryover. Switching leaves traces in the next period. Options: longer periods, a burn-in (discard the first 5 to 10 minutes of each period for the metric), or add the previous period's arm to the model. With random assignment the plain contrast estimates the direct effect but misses the lingering part.
5. Time of day. Use slot-of-day and day-of-week controls so peak periods do not decide the result.
6. Report with an interval from the period-level analysis, plus the carryover check.

**Metrics:**
- Period mean delivery time = total delivery minutes in the period / deliveries completed in the period (or a ratio-of-sums at day level).
- Effect = mean over new periods - mean over old periods (after removing the slot-of-day mean).
- Effective n = 672 periods, 336 per arm; not 604,800.
- Guardrails: order volume per period, cancellations, courier hours (carryover or demand shifts).

**Risks:**
- Carryover: the effect at the start of a period is partly from the previous arm.
- Time-of-day confounding if the schedule is not balanced.
- Strict alternation can alias with any half-hour rhythm in demand (orders bunch just after the hour and half hour).
- Serial correlation between neighbouring periods understates noise further.
- Novelty or learning for couriers when they notice the rule flips.

**What the interviewer scores:**
- Strong: says the unit is the period and that the effective sample is hundreds, not hundreds of thousands. Weak: reports a tiny p-value from 604,800 orders.
- Strong: gives a randomization scheme with blocks by time of day. Weak: "alternate old, new, old, new".
- Strong: names carryover and gives a fix (burn-in, longer periods, lag term). Weak: ignores it.
- Strong: controls for time of day and uses an inference method that respects the correlation. Weak: plain z-test.

**Example:** illustrative numbers. 14 days x 48 half-hour periods = 672 periods; 672 x 900 = 604,800 deliveries. One delivery has SD 12 minutes; a market-wide shock per period has SD 1.5 minutes.
- Weak: "z-test on 604,800 deliveries, p tiny, new dispatch wins."
- Strong: "The 604,800 are 672 correlated period means. I randomize 24 of 48 periods each day, remove time-of-day, and test over 14 daily differences."
- In my run with NO true effect, the order-level z-test claims a significant result in 76.0% of experiments (it should be 5%). The day-level period test is at 4.9%. Strict alternation reads +1.000 minute when the truth is zero (it is aliased with the half-hour rhythm) while day-level random assignment reads +0.005. With carryover of half the effect into the next period, the random switchback reads -0.99 for a direct effect of -1.0, while a full rollout would give -1.5.

**Code:**
```python
# Q28: switchback, 672 half-hour periods, ~900 deliveries each (illustrative simulation, seeded)
import numpy as np

rng = np.random.default_rng(28)
P, PER_DAY, DELIV = 672, 48, 900
print("periods:", P, "deliveries:", P * DELIV, "periods per arm:", P // 2)
assert P == 14 * 48 and P * DELIV == 604_800

slot = np.arange(P) % PER_DAY                    # half-hour slot of the day
tod = 3.0 * np.sin(2 * np.pi * slot / PER_DAY)   # time-of-day pattern in delivery minutes (peak and off-peak)
SD_ORDER, SD_SHOCK, PHI = 12.0, 1.5, 0.6         # SD of one delivery; SD of a market-wide period shock; shock persistence

def shocks():
    e = np.zeros(P); e[0] = rng.normal(0, SD_SHOCK)
    for t in range(1, P): e[t] = PHI * e[t - 1] + rng.normal(0, SD_SHOCK * np.sqrt(1 - PHI**2))
    return e

def assign_day():                               # random 24/24 split of the 48 periods inside each day
    a = np.zeros(P, int)
    for d in range(14):
        a[d * PER_DAY + rng.permutation(PER_DAY)[:PER_DAY // 2]] = 1
    return a
alt = np.tile([0, 1], P // 2)                    # strict A,B,A,B...

PAR = 1.0 * (slot % 2)                           # a half-hour rhythm: e.g. orders bunch just after the hour/half-hour

def test(assign, effect=0.0):
    y = tod + PAR + shocks() + effect * assign + rng.normal(0, SD_ORDER / np.sqrt(DELIV), P)   # period mean minutes
    diff = y[assign == 1].mean() - y[assign == 0].mean()
    se_naive = SD_ORDER * np.sqrt(2 / (DELIV * P / 2))                      # z-test treating 604,800 orders as independent
    # right unit: the period; remove the slot-of-day mean, then use one difference per day (14 days) and a t-test
    ys = y.reshape(14, PER_DAY); a2 = assign.reshape(14, PER_DAY)
    res = ys - ys.mean(axis=0)
    dday = np.array([res[d][a2[d] == 1].mean() - res[d][a2[d] == 0].mean() for d in range(14)])
    t = dday.mean() / (dday.std(ddof=1) / np.sqrt(14))
    return diff, abs(diff / se_naive) > 1.96, abs(t) > 2.160                # 2.160 = t critical, 13 df

# a) under NO effect: false-positive rate of the naive order-level z-test vs the day-level period test
R = 1500
fp = np.array([test(assign_day())[1:] for _ in range(R)]).mean(axis=0)
print(f"false positives, no effect: order-level z-test {fp[0]:.3f}; day-level period test {fp[1]:.3f}")
assert fp[0] > 0.15 and 0.02 < fp[1] < 0.09
print(f"naive SE {SD_ORDER*np.sqrt(2/(DELIV*P/2)):.4f} min for the arm difference")

# b) strict alternation is aliased with any half-hour rhythm; random assignment is not
d_alt = np.array([test(alt)[0] for _ in range(300)])
d_blk = np.array([test(assign_day())[0] for _ in range(300)])
print(f"no effect, mean estimated difference: alternation {d_alt.mean():+.3f} min; day-random {d_blk.mean():+.3f} min")
assert abs(d_alt.mean()) > 0.8 and abs(d_blk.mean()) < 0.1

# c) carryover: each period keeps a share phi of the previous period's effect
tau, phi = -1.0, 0.5
est = []
for _ in range(600):
    a = assign_day()
    prev = np.r_[0, a[:-1]]
    y = tod + PAR + shocks() + tau * (a + phi * prev) + rng.normal(0, SD_ORDER / np.sqrt(DELIV), P)
    est.append(y[a == 1].mean() - y[a == 0].mean())
print(f"carryover test: true direct effect {tau}, full-rollout effect {tau*(1+phi)}, switchback estimate {np.mean(est):+.2f}")
assert abs(np.mean(est) - tau) < 0.15
```

**Output (my run):**
```text
periods: 672 deliveries: 604800 periods per arm: 336
false positives, no effect: order-level z-test 0.760; day-level period test 0.049
naive SE 0.0309 min for the arm difference
no effect, mean estimated difference: alternation +1.000 min; day-random +0.005 min
carryover test: true direct effect -1.0, full-rollout effect -1.5, switchback estimate -0.99
```

**Follow-ups:**
- How many periods do I need? Power depends on the period-level SD, not the number of orders. Use pilot period variances; more periods or more markets help, more orders per period barely do.
- Why not randomize by courier or order? Orders and couriers share the same dispatch pool, so the rule changes everyone's options (interference); that is why we flip the market.
- Does randomization remove the need for time-of-day controls? It protects against bias, but blocking and controls reduce noise.

**Common mistakes:** Treating deliveries as independent. Strict alternation. Ignoring carryover. Letting the first minutes of a period count. Using a pooled z-test and reporting p < 0.0001. Not checking that each hour of day appears in both arms.

### Q29 ⭐⭐ 🟡 A brand campaign is tested by randomizing 20 regions 10/10, and the largest region, with 30% of total revenue (the other 19 hold about 3.7% each), landed in treatment. Explain what this does to the readout, how you would balance and analyse a geo experiment, and what you tell the marketing lead.
**Asked at:** Marketplace, interference and switchback material (Dataford 'interference in marketplace experiments', 'marketplace experiment with interference' and 'choose switchback for marketplace dispatch' pages, a DoorDash careers blog post, an arXiv 2022 paper on switchbacks and interference bias, a Statsig marketplace-experimentation page); company practice is described only as the snippets reported it; search snippets only, not opened
**Say this first (1 line):** With one region holding 30% of revenue, a 10/10 split can be badly lopsided and that single region dominates the result; I would not compare levels, I would measure each region against its own history, balance the design, and tell marketing the test can only detect a large lift.

**Clarifying questions:**
- What outcome does the campaign target (revenue, new customers, brand search)? It sets the metric and the lag.
- Do I have 1 to 2 years of weekly history per region? Pre-period data is what lets me adjust and balance.
- Can people cross region borders (online sales, travel)? That leaks the campaign into control.
- Is the big region special (the capital, a different mix)? If it is unlike the others, it may need its own test.
- How big a lift would marketing consider worth the spend? That sets whether 20 regions can answer at all.

**Approach:**
1. Say what happened. Treated regions hold 30% + 9 x 3.68% = 63.2% of baseline revenue, control 36.8%. A level comparison (treated revenue against control revenue) would show +71% even if the campaign did nothing. That is why we never compare levels.
2. Change the metric to change versus the region's own pre-period (difference-in-differences, or a synthetic-control and time-series model for the treated group). Book 1 Part 10 Q44 covers geo experiments.
3. Balance the design (before launch, if possible). Pre-specify a rule: match regions on pre-period revenue and trend, or run the big region as its own case, or leave it out and randomize the other 19. Draw many random splits and pick one that meets a balance threshold (re-randomization), then keep the record.
4. Quantify noise. Each region is one data point, so with 20 regions the standard error is large. Use randomization inference (re-draw assignments), or a block bootstrap over weeks.
5. Tell marketing the truth: this design answers "is the effect large?". In my simulation with 5% weekly noise per region the smallest detectable lift is about 4%, so a true 2% lift would likely be inconclusive.
6. If the run has already started with the big region treated: analyse change versus history, report the big-region and the other-nine effects separately, and flag that the 30% region is one observation.

**Metrics:**
- Regional revenue change = (post-period revenue / pre-period revenue) per region, aggregated as treated sum over control sum.
- Lift = ratio of ratios - 1 (treated change relative to control change).
- Baseline balance = treated share of pre-period revenue (target near 50%).
- Guardrails: spillover (sales near borders), margin per order, pre-trend parallelism.

**Risks:**
- Level comparison misread as an effect (the +71% above).
- One region carries 30% of the weight; its idiosyncratic noise passes straight into the result.
- Few units: wide intervals, low power.
- Spillover across regions and national campaigns running at the same time.
- Pre-trends that diverge between treated and control.

**What the interviewer scores:**
- Strong: computes the baseline imbalance (63.2 against 36.8) and says why levels cannot be compared. Weak: "randomization balances everything".
- Strong: picks difference-in-differences or synthetic control with a placebo check. Weak: simple difference of means.
- Strong: admits low power with 20 units and says what effect size could be seen. Weak: promises a precise ROI.
- Strong: discusses leaving out or isolating the big region. Weak: ignores the weights.

**Example:** illustrative numbers. 20 regions: one at 30% of revenue and 19 at 3.68% each (sum 100%). Weekly noise 5% per region, 8 pre-weeks, 4 post-weeks, true campaign effect +2% in treated regions.
- Weak: "Treated regions sold more than control, so the campaign worked."
- Strong: "Treated regions were bigger to begin with. I compare each region with its own history, and with 20 regions I can only see lifts of about 4% or more."
- In my run: with the big region in treatment, treated regions hold 63.2% of baseline revenue; a level comparison reads +74.8% when the truth is +2%; the change-versus-history estimate reads +1.99%. Across random 10/10 splits, the big region is in treatment 51% of the time, treated baseline share ranges 36% to 64%, and the change-versus-history estimate has SD 1.87 points. Leaving the big region out (9 against 9 of the rest) keeps the share at 49% to 51% and reduces the SD to 1.45 points; the detectable lift is still about 4.1%.

**Code:**
```python
# Q29: 20 regions, one holds 30% of revenue (illustrative simulation, seeded)
import numpy as np

rng = np.random.default_rng(29)
share = np.r_[0.30, np.full(19, 0.70 / 19)]
print("other 19 regions each:", round(0.70 / 19 * 100, 2), "% (19 x 3.7 = 70.3 so the prompt's 3.7 is rounded)")
assert abs(share.sum() - 1) < 1e-12

PRE, POST, SD, LIFT = 8, 4, 0.05, 0.02           # weeks; weekly noise 5% per region; true campaign lift +2% in treated regions
def one(assign):
    mult = np.where(assign == 1, 1 + LIFT, 1.0)      # assign: 1 treated, 0 control, -1 left out
    pre = share[:, None] * (1 + rng.normal(0, SD, (20, PRE)))
    post = share[:, None] * mult[:, None] * (1 + rng.normal(0, SD, (20, POST)))
    T, C = assign == 1, assign == 0
    naive = post[T].sum() / post[C].sum() - 1                                    # compare post-period levels
    did = (post[T].sum() / pre[T].sum() * PRE / POST) / (post[C].sum() / pre[C].sum() * PRE / POST) - 1   # change vs own history
    return naive, did, pre[T].sum() / pre[T | C].sum()

# the actual draw in the prompt: big region (index 0) landed in treatment, 9 of the other 19 join it
a = np.zeros(20, int); a[0] = 1; a[1 + rng.permutation(19)[:9]] = 1
base_share = share[a == 1].sum()
print(f"treated regions hold {base_share*100:.1f}% of revenue before the test (control {100-base_share*100:.1f}%)")
assert abs(base_share - (0.30 + 9 * 0.70 / 19)) < 1e-9 and base_share > 0.6
print("lift if no effect existed would be read as", round(base_share / (1 - base_share) - 1, 3), "by a naive level comparison")

R = 4000
out = np.array([one(a) for _ in range(R)])
print(f"this assignment, true lift +2.0%: naive level comparison {out[:,0].mean()*100:+.1f}% ; change-vs-own-history {out[:,1].mean()*100:+.2f}% (sd {out[:,1].std()*100:.2f})")
assert out[:, 0].mean() > 0.5 and abs(out[:, 1].mean() - LIFT) < 0.005

# all random 10/10 assignments: how often does the big region land in treatment, and how lopsided is the baseline?
res = []
for _ in range(R):
    g = np.zeros(20, int); g[rng.permutation(20)[:10]] = 1
    res.append((g[0], share[g == 1].sum()))
res = np.array(res)
print(f"big region in treatment in {res[:,0].mean()*100:.0f}% of random splits; baseline share of treated regions ranges {res[:,1].min()*100:.0f}% to {res[:,1].max()*100:.0f}%")
# options: random 10/10; or run the big region on its own and randomize the other 19 (9 treated, 9 control, 1 spare)
def rand():
    g = np.zeros(20, int); g[rng.permutation(20)[:10]] = 1
    return g
def without_big():
    g = -np.ones(20, int); idx = 1 + rng.permutation(19)
    g[idx[:9]] = 1; g[idx[9:18]] = 0
    return g
sds = {}
for name, f in (("random 10/10", rand), ("big region left out", without_big)):
    d = np.array([one(f()) for _ in range(3000)])
    sds[name] = d[:, 1].std()
    print(f"{name:19s}: treated share of baseline revenue {d[:,2].min()*100:.0f}%-{d[:,2].max()*100:.0f}%; estimate mean {d[:,1].mean()*100:+.2f}%, sd {d[:,1].std()*100:.2f} points")
assert sds["big region left out"] < sds["random 10/10"]
sd_b = sds["big region left out"]
print(f"smallest lift detectable with about 80% power is 2.8 x sd = {2.8*sd_b*100:.1f}% , so a true +2% would not be detected either way")
assert 2.8 * sd_b > LIFT
```

**Output (my run):**
```text
other 19 regions each: 3.68 % (19 x 3.7 = 70.3 so the prompt's 3.7 is rounded)
treated regions hold 63.2% of revenue before the test (control 36.8%)
lift if no effect existed would be read as 0.714 by a naive level comparison
this assignment, true lift +2.0%: naive level comparison +74.8% ; change-vs-own-history +1.99% (sd 1.85)
big region in treatment in 51% of random splits; baseline share of treated regions ranges 37% to 63%
random 10/10       : treated share of baseline revenue 36%-64%; estimate mean +2.03%, sd 1.87 points
big region left out: treated share of baseline revenue 49%-51%; estimate mean +1.98%, sd 1.45 points
smallest lift detectable with about 80% power is 2.8 x sd = 4.1% , so a true +2% would not be detected either way
```

**Follow-ups:**
- Could I pair regions by size? With one region at 30% there is no partner of similar size, so pairing cannot balance it; in my simulation pairing was no better than random. Isolate or exclude it.
- What about synthetic control for the big region? It can work if other regions' history reproduces the big region well; check pre-period fit and run placebo tests on untreated regions.
- Is the prompt's "about 3.7% each" exact? 19 x 3.7 = 70.3, so the true value is 70/19 = 3.68%; rounding only.

**Common mistakes:** Comparing treated and control totals. Believing random assignment guarantees balance with 20 units. Using user-level standard errors on region data. Forgetting spillover. Promising a precise ROI from 20 data points.

### Q30 ⭐⭐ 🟡 In a UI redesign, existing users show sessions per day falling from 10.0 to 9.7 in week 1 (-3% relative to control), while new users (20% of traffic) show +4% relative. Explain how you separate a primacy effect from a real harm, how you test it, and how long you would run the experiment.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would plot the effect against days since each user's first exposure, not calendar day; if the existing users' drop shrinks toward zero while new users stay positive, it is primacy, and if it stays flat near -3%, it is real harm; I would run at least until the weekly effect stabilises, normally 3 to 4 weeks.

**Clarifying questions:**
- What do "10.0 to 9.7" and "-3% relative to control" refer to: treatment against control in week 1? I read it as treatment 9.7 against control 10.0 among existing users. Why it matters: a before-and-after drop in treatment alone would not be an experiment result.
- Are new users randomized too and how are they defined (first visit during the test)? New users have no habit to disrupt.
- Are sessions per day the primary metric, or is it retention and revenue? A drop in sessions can come with a gain in session quality.
- How strong is the weekly cycle (weekday versus weekend)? It sets the minimum run length.
- Is the redesign reversible? That sets how much risk we accept while waiting.

**Approach:**
1. Frame the two stories. Primacy: habits are disrupted at first, then people adapt and the effect moves toward the steady-state. Real harm: the effect stays negative. New-user effect is a clue: no old habits to break, so +4% suggests the design itself is fine for fresh users (Book 1 Part 10 Q8 covers novelty and primacy).
2. Plot the effect by days since first exposure (each user's own day 1, 2, 3...), with intervals, for existing users and for new users separately. Calendar-day plots mix users at different stages.
3. Test the trend. Fit a line (or an exponential) to the daily effect over exposure days; a significantly rising slope toward zero supports primacy, a flat line supports harm.
4. Cross-check with cohorts: users first exposed in week 1 against those first exposed in week 2 (if rolled in gradually), and with heavy versus light users.
5. Decide the duration from the data. Minimum: two full weekly cycles. Then continue until the weekly effect has stopped changing (for example two successive weekly estimates agree within the interval). A common rule of thumb is 3 to 4 weeks; the answer is a stopping rule, not a fixed number.
6. Pre-register the readout week and the metric so that I am not choosing the favourable week afterwards.

**Metrics:**
- Daily effect for existing users = mean sessions per user per day (treatment) / mean (control) - 1, by day since first exposure.
- Weekly effect = the same, averaged within exposure-week.
- Trend = slope of the daily effect against exposure day, with a confidence interval.
- Guardrails: retention (users active in week 2 / week 1), time per session, revenue per user.

**Risks:**
- Calling any early dip "primacy" and shipping a harmful change.
- The new-user lift may come from who arrives (a different population) rather than from the design.
- Blending: with 20% new users and 80% existing, the blended effect is 0.8 x (-3) + 0.2 x 4 = -1.6% (assuming equal baselines), which hides both stories.
- A fading negative can also be users leaving (survivor bias): check retention.
- Weekly cycle: a window that is not a whole number of weeks.

**What the interviewer scores:**
- Strong: uses exposure-day alignment and separates new from existing users. Weak: looks at calendar days or the blended number.
- Strong: states what each story predicts (slope rising versus flat). Weak: "wait and see".
- Strong: gives a stopping rule tied to data and the weekly cycle. Weak: "run for two weeks" with no reason.
- Strong: notes retention and survivor bias. Weak: ignores who stays.

**Example:** illustrative numbers. Story A (primacy): existing users start at -6% and the effect fades toward -0.5% with a time constant of 4.5 days, so the week-1 average is -3%. Story B (real harm): constant -3%. 40,000 users per arm, 10 sessions per day, SD 6.
- Weak: "Existing users dropped 3% in week 1, kill the redesign."
- Strong: "Week 1 is the same -3% under both stories. I plot by exposure day: Story A has weekly effects -2.9%, -0.8%, -0.4%, -0.8% and a significant rising slope; Story B stays near -3%."
- In my run, Story A: weekly effect -2.86, -0.82, -0.36, -0.77 (%), slope over days 1 to 14 +0.0286 sessions per day (p < 0.001). Story B: -3.3, -2.9, -2.88, -2.95, slope +0.0027 (p = 0.35). The blended week-1 figure is -1.6%. A single week of data for 3% needs only about 6,272 users per arm, so sample is not the problem; the time axis is.

**Code:**
```python
# Q30: existing users -3% in week 1, new users +4%: primacy or real harm? (illustrative simulation, seeded)
import numpy as np
from scipy import stats, optimize

rng = np.random.default_rng(30)
print("prompt: 10.0 -> 9.7 is", round(9.7 / 10.0 - 1, 3), "; blended week-1 effect if both groups have the same baseline:", round(0.8 * -3 + 0.2 * 4, 2), "%")
assert abs(9.7 / 10.0 - 1 + 0.03) < 1e-9 and abs(0.8 * -3 + 0.2 * 4 - -1.6) < 1e-9

# Story A (primacy): effect on existing users starts at -6% and fades with time constant tau days towards -0.5%
e0, einf = -0.06, -0.005
days = np.arange(1, 8)
f = lambda tau: np.mean(einf + (e0 - einf) * np.exp(-days / tau)) - (-0.03)
tau = optimize.brentq(f, 0.5, 50)
print(f"tau chosen so the week-1 average is -3%: {tau:.2f} days")
assert abs(f(tau)) < 1e-9
eff_A = lambda d: einf + (e0 - einf) * np.exp(-d / tau)
eff_B = lambda d: np.full_like(d, -0.03, dtype=float)       # Story B (real harm): constant -3%

def daily_effects(eff, n=40000, D=28, base=10.0, sd=6.0):
    """per-day difference in mean sessions per user between arms, with simulation noise."""
    d = np.arange(1, D + 1)
    se = sd * np.sqrt(2 / n)
    return d, base * eff(d) + rng.normal(0, se, D), se

def slope_test(d, y):
    r = stats.linregress(d[:14], y[:14])               # use first 14 exposure days
    return r.slope, r.pvalue
for name, eff in (("A primacy", eff_A), ("B real harm", eff_B)):
    d, y, se = daily_effects(eff)
    s, p = slope_test(d, y)
    wk = [y[i:i + 7].mean() / 10 * 100 for i in (0, 7, 14, 21)]
    print(f"{name:11s}: weekly effect % = {[round(float(w),2) for w in wk]}; slope over days 1-14 = {s:+.4f} sessions/day (p={p:.3f})")
    if name.startswith("A"): wkA, pA = wk, p
    else: wkB, pB = wk, p
assert wkA[0] < -2.5 and wkA[3] > -1.0 and pA < 0.05 and abs(wkB[3] + 3) < 1 and pB > 0.05
# new users have no habit to disrupt: their effect is a cleaner read of the steady state
print("blended week-1 effect with a 20% new-user share is read at", round(0.8 * -3 + 0.2 * 4, 1), "% while the steady state may differ")
n_need = 2 * (1.96 + 0.84) ** 2 * 6.0 ** 2 / 0.3 ** 2
print(f"users per arm to see a 3% (0.3 sessions) drop in ONE week's per-user average if sd is 6: about {n_need:,.0f}; we have 40,000, so the weekly readings above are well powered")
assert 6000 < n_need < 6600
```

**Output (my run):**
```text
prompt: 10.0 -> 9.7 is -0.03 ; blended week-1 effect if both groups have the same baseline: -1.6 %
tau chosen so the week-1 average is -3%: 4.52 days
A primacy  : weekly effect % = [-2.86, -0.82, -0.36, -0.77]; slope over days 1-14 = +0.0286 sessions/day (p=0.000)
B real harm: weekly effect % = [-3.3, -2.9, -2.88, -2.95]; slope over days 1-14 = +0.0027 sessions/day (p=0.346)
blended week-1 effect with a 20% new-user share is read at -1.6 % while the steady state may differ
users per arm to see a 3% (0.3 sessions) drop in ONE week's per-user average if sd is 6: about 6,272; we have 40,000, so the weekly readings above are well powered
```

**Follow-ups:**
- What if both new and existing users fade? That is a novelty effect on the positive side; do not extrapolate the +4%.
- Can I speed it up? Compare with a second, later-started cohort (staggered rollout) or analyse only the later exposure days with a pre-specified window.
- What if the dip stays but revenue rises? Make the decision on the pre-agreed primary metric and guardrails, and report the trade.

**Common mistakes:** Averaging all days into one number. Plotting by calendar day. Declaring "novelty" with no slope test. Stopping at the first significant reading. Ignoring the 20% new users. Not saying how long and why.

### Q31 ⭐⭐ 🟡 Revenue per user averages 20, with the top 0.1% of users contributing 25% of revenue, and a t-test shows treatment up 3% relative to control with p = 0.2 and a confidence interval wider than the effect. Explain your options for heavy-tailed metrics, what each trades away and how you would report the result.
**Asked at:** Bot and outlier contamination material (Algolia engineering and docs pages on outliers in A/B tests, a Peakhour post on bots corrupting A/B data; the latter is vendor marketing); mostly practitioner pages, so scenario is partly editor-designed; search snippets only, not opened
**Say this first (1 line):** A few whales dominate the variance, so +3% with p = 0.2 means "unknown", not "no effect"; I would use a pre-registered cap, CUPED and a longer run, and report the capped and uncapped estimates side by side.

**Clarifying questions:**
- Are the top 0.1% real customers or bots, test accounts and fraud? Bots are removed, real whales are kept (cap or model them).
- Is the metric revenue per user over a fixed window, and is there pre-period revenue per user? A pre-period metric enables CUPED.
- Does the business care about total revenue (whales matter) or typical user value? That picks the estimand.
- Did the treatment plausibly change whale behaviour (for example a bulk-purchase feature)? Then capping hides the effect.
- Was the cap or transformation fixed before looking? A cap chosen after peeking is a fishing step.

**Approach:**
1. First check the data: remove bots and duplicates, look at the top 20 users per arm. One account can swing the mean (Book 1 Part 10 Q25 covers outliers and heavy tails).
2. Options, with what each trades away:
   - Winsorize or cap at a fixed percentile (for example p99.9, set before looking). Cuts variance sharply; changes the estimand to "revenue up to the cap", so real whale gains are partly thrown away.
   - Log or other transform (log(1 + x)). Stable, but it tests a ratio-like quantity, not the average revenue the business cares about.
   - Rank test (Mann-Whitney). Robust, but it answers "is one distribution shifted", not "how many rupees".
   - CUPED: subtract the part of revenue predicted by pre-period revenue. Keeps the estimand and cuts variance; needs a pre-period and works only as well as the correlation.
   - Bootstrap for the interval. Honest about shape, does not shrink variance.
   - Two-part model (probability of buying x amount if buying) or conversion plus average order value. Explains where the effect comes from.
   - More users or more time. Always valid, slow.
3. Choose one primary rule in advance (for example capped revenue with CUPED) and keep the uncapped mean as a sensitivity result.
4. Report: effect with interval for the capped primary, the uncapped estimate with its wider interval, and the plain statement "we cannot rule out 0% or a few percent".

**Metrics:**
- Revenue per user = total revenue in the window / users assigned (include zeros).
- Capped revenue per user = sum(min(revenue, cap)) / users assigned, with cap = pooled p99.9 fixed beforehand.
- CUPED-adjusted metric = Y - theta x (X_pre - mean(X_pre)), theta = cov(Y, X_pre) / var(X_pre).
- Guardrails: share of revenue above the cap per arm, number of whales per arm (SRM-like check on the tail), refund rate.

**Risks:**
- Capping biases the lift down if the treatment raises whale spend.
- A cap chosen after seeing the result.
- Few whales per arm: random imbalance in the number of whales decides the result.
- Winsorizing within each arm separately (different caps) biases the comparison.
- Transforming then converting back to rupees without care.

**What the interviewer scores:**
- Strong: names several options and says what each gives up. Weak: "remove outliers" with no reasoning.
- Strong: separates bots (remove) from real whales (cap or model). Weak: deletes all the top users.
- Strong: commits to a rule in advance and reports a sensitivity result. Weak: picks whichever method gives p < 0.05.
- Strong: says "p = 0.2 means we do not know" and gives the interval. Weak: "no effect".

**Example:** illustrative numbers. Population: 80% spend nothing, 19.9% are ordinary buyers, 0.1% are whales. Mean revenue 20; top 0.1% hold 24.7% of revenue. True effect +3% on everybody's spend; 100,000 users per arm, 300 simulated tests.
- Weak: "p = 0.2, so there is no effect; drop it."
- Strong: "The test cannot see a 3% effect with this tail. Capped and CUPED versions give more power; I report both with intervals and plan a longer run."
- In my run the share of top 0.1% matches the prompt (24.7% against about 25%, mean 20.0). Power at +3%: raw mean 0.11, capped at p99.9 0.40, CUPED 0.18, log(1+x) 0.16. Estimated lift: raw 3.72% (SD 5.80 across tests), capped 2.82% (SD 1.70), CUPED 3.32% (SD 3.51). The cap gives lower variance but reads a bit under 3% because spend above the cap is discarded.

**Code:**
```python
# Q31: heavy-tailed revenue per user (illustrative simulation, seeded)
import numpy as np
from scipy import stats

rng = np.random.default_rng(31)
def population(n):
    """80% buy nothing, 19.9% ordinary buyers (lognormal), 0.1% whales (lognormal, very large)."""
    kind = rng.choice(3, n, p=[0.80, 0.199, 0.001])
    lvl = np.where(kind == 1, rng.lognormal(np.log(55), 0.8, n), np.where(kind == 2, rng.lognormal(np.log(3650), 0.8, n), 0.0))
    return lvl
big = population(4_000_000)
srt = np.sort(big)[::-1]
top_share = srt[:4000].sum() / big.sum()
print(f"mean revenue per user {big.mean():.1f}; top 0.1% of users hold {top_share*100:.1f}% of revenue; p99.9 = {np.quantile(big, .999):.0f}")
assert abs(big.mean() - 20) < 2 and abs(top_share - 0.25) < 0.04

N, REPS, LIFT = 100_000, 300, 0.03
def trial():
    L0 = population(2 * N)                           # each user's spend level
    pre = L0 * rng.gamma(4, 0.25, 2 * N)              # pre-period revenue, correlated with post
    post = L0 * rng.gamma(4, 0.25, 2 * N)
    arm = np.r_[np.zeros(N, int), np.ones(N, int)]
    post = post * (1 + LIFT * arm)
    cap = np.quantile(post, 0.999)                   # cap set from pooled data, blind to arm
    res = {}
    for name, y in (("raw mean", post), ("capped at p99.9", np.minimum(post, cap))):
        d = y[arm == 1].mean() - y[arm == 0].mean()
        se = np.sqrt(y[arm == 1].var(ddof=1) / N + y[arm == 0].var(ddof=1) / N)
        res[name] = (d / y[arm == 0].mean(), abs(d / se) > 1.96)
    th = np.cov(post, pre)[0, 1] / pre.var()          # CUPED
    adj = post - th * (pre - pre.mean())
    d = adj[arm == 1].mean() - adj[arm == 0].mean()
    se = np.sqrt(adj[arm == 1].var(ddof=1) / N + adj[arm == 0].var(ddof=1) / N)
    res["CUPED (pre revenue)"] = (d / adj[arm == 0].mean(), abs(d / se) > 1.96)
    res["log(1+x)"] = (None, abs(stats.ttest_ind(np.log1p(post[arm == 1]), np.log1p(post[arm == 0])).statistic) > 1.96)
    return res
R = [trial() for _ in range(REPS)]
print(f"true effect +3% on every user's revenue, {N:,} users per arm, {REPS} simulated tests")
print(f"{'method':22s} {'power':>6s} {'mean est. lift':>15s} {'sd of est.':>11s}")
pw = {}
for k in R[0]:
    power = np.mean([r[k][1] for r in R])
    pw[k] = power
    if R[0][k][0] is None:
        print(f"{k:22s} {power:6.2f} {'(log scale)':>15s}"); continue
    e = np.array([r[k][0] for r in R])
    print(f"{k:22s} {power:6.2f} {e.mean()*100:14.2f}% {e.std()*100:10.2f}")
assert pw["CUPED (pre revenue)"] > pw["raw mean"]
assert pw["raw mean"] < 0.3 and pw["capped at p99.9"] > pw["raw mean"]
print("capped lift is read lower than the true +3% because whales' extra spend above the cap is thrown away: the cap changes the estimand")
```

**Output (my run):**
```text
mean revenue per user 20.0; top 0.1% of users hold 24.7% of revenue; p99.9 = 843
true effect +3% on every user's revenue, 100,000 users per arm, 300 simulated tests
method                  power  mean est. lift  sd of est.
raw mean                 0.11           3.72%       5.80
capped at p99.9          0.40           2.82%       1.70
CUPED (pre revenue)      0.18           3.32%       3.51
log(1+x)                 0.16     (log scale)
capped lift is read lower than the true +3% because whales' extra spend above the cap is thrown away: the cap changes the estimand
```

**Follow-ups:**
- Is p = 0.2 evidence of no effect? No. The interval is wider than the effect; the test is underpowered for a 3% change.
- When is a rank test right? When the question is "do typical users spend more", not "how much total revenue".
- Which cap percentile? A pre-registered, stable one (p99 to p99.9); show sensitivity to the cap.

**Common mistakes:** Deleting the top users after seeing the result. Different caps per arm. Reporting the capped number as the revenue lift without saying so. Treating p = 0.2 as proof of no effect. Ignoring CUPED. Forgetting to exclude bots first.

### Q32 ⭐⭐ 🟡 A settings-page feature is seen by only 8% of users, and across all assigned users revenue per user is up 0.1% relative to control, not significant. Among users who reach the page, the lift is +1.25% relative. Explain how you analyse a test with low exposure, what the triggering rule must satisfy, and what you report.
**Asked at:** Underpowered-test and MDE material (a Towards Data Science 'what to do when an A/B test result is not significant' article, a Dataford 'non significant test PM wants launch' page, a HackerNoon 'running A/B tests you can't measure' post, a Statsig power-analysis page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would analyse the triggered users, those who actually reached the page, with a trigger rule defined the same way in both arms, and report both the diluted all-users number and the triggered number; the triggered +1.25% is a statement about the 8%, not the whole base.

**Clarifying questions:**
- Can I log "would have reached the page" in the control arm too (a counterfactual trigger)? Without it, the triggered comparison is not like with like.
- Does the feature change the chance of reaching the page (a new link, a prompt)? If yes, triggering is itself an outcome and the clean analysis is all users.
- Is the 0.1% across all assigned users measured over the whole population, with the same variance? It decides the power calculation.
- Will the 8% share stay stable after launch? The business impact is the lift times the exposed share.
- What decision hangs on it? A small, cheap feature can ship on a triggered result; a risky one needs more.

**Approach:**
1. Check the arithmetic: 8% of users x 1.25% = 0.1% overall. So the two numbers agree, if the non-reaching users are unaffected.
2. Explain the dilution. The ITT (intention-to-treat, all assigned users) is the honest business number, but 92% of users add noise and zero effect. The diluted effect is 12.5 times smaller (0.1% against 1.25%), so the all-users test needs 156 times as many users as the triggered test needs triggered users (12.5 squared). Because only 8% of assigned users trigger, the net cost is 156 x 0.08 = 12.5 times as many assigned users.
3. Triggered analysis. Compare users who reached the page in treatment against users who would have reached it in control. Requirements for the trigger: (a) defined on behaviour before the treatment difference appears; (b) logged in both arms by the same rule; (c) not influenced by the treatment; (d) all triggered users counted, including those who then did not use the feature.
4. Check for symmetry: the triggered share should be about equal in both arms (a built-in SRM check on triggered users).
5. Report: the ITT (+0.1%, not significant), the triggered lift (+1.25% with interval), the triggered share (8%) and the implied revenue impact.
6. If a counterfactual trigger cannot be logged, use ITT and plan a bigger or longer test, or use CUPED to cut variance (Book 1 Part 10 Q1 lists the sample-size steps).

**Metrics:**
- ITT lift = mean(revenue per user, all treatment-assigned) / mean(all control-assigned) - 1. Denominator: all assigned users.
- Triggered lift = mean(revenue, triggered treatment users) / mean(revenue, triggered control users) - 1.
- Triggered share = triggered users / assigned users, per arm (should match).
- Guardrails: SRM at the assigned level and at the triggered level.

**Risks:**
- Asymmetric trigger: in treatment you count users who clicked the new setting, in control you count everybody. Engaged users self-select and produce a huge fake lift.
- A trigger that the feature itself changes (a prompt that sends more users to the page).
- Reading +1.25% as the effect on all users.
- Multiplying 1.25% by the 8% and ignoring how much the share might change.

**What the interviewer scores:**
- Strong: connects 1.25% x 8% = 0.1% and explains dilution. Weak: "not significant, so no effect".
- Strong: lists the trigger rules (symmetric, pre-treatment, unaffected by treatment). Weak: "filter to users who used the feature".
- Strong: quantifies the sample saving. Weak: "triggered is better".
- Strong: reports both ITT and triggered. Weak: only the number that looks better.

**Example:** illustrative numbers. Revenue per user 20, SD 20. Triggered lift +1.25% means +0.25 per triggered user; ITT +0.1% means +0.02 per assigned user.
- Weak: "Across all users it is +0.1%, not significant, drop it."
- Strong: "Only 8% can feel it. For the triggered 8% the effect is +1.25%, and a triggered analysis needs about 100,000 triggered users per arm for 80% power."
- In my run: 80% power needs 100,466 triggered users per arm (1,255,821 assigned) for the triggered analysis against 15,697,759 per arm for the all-users analysis, a ratio of 12.5. With 1.25 million assigned users per arm, power is 0.13 for all users and 0.80 for triggered-only. If the feature does nothing but the trigger is asymmetric (treatment counts only the most engaged 8%, control counts everybody), the test reads +329%; a symmetric trigger reads -1.4%.

**Code:**
```python
# Q32: 8% exposure, diluted ITT vs triggered analysis (illustrative simulation, seeded)
import numpy as np
from scipy import stats

rng = np.random.default_rng(32)
SHARE, ITT_REL, MU, SD = 0.08, 0.001, 20.0, 20.0
print("triggered lift implied by the prompt:", ITT_REL / SHARE * 100, "%")
assert abs(ITT_REL / SHARE - 0.0125) < 1e-12

z = stats.norm.ppf(0.975) + stats.norm.ppf(0.80)
n_trig = 2 * z**2 * SD**2 / (MU * 0.0125) ** 2
n_itt = 2 * z**2 * SD**2 / (MU * 0.001) ** 2
print(f"users per arm for 80% power: triggered analysis {n_trig:,.0f} triggered (= {n_trig/SHARE:,.0f} assigned); all-users analysis {n_itt:,.0f}; ratio {n_itt/(n_trig/SHARE):.2f}")
assert abs(n_itt / n_trig - 1 / SHARE**2) < 1e-6

# simulate 2,000 tests with 1.25M assigned users per arm; group means drawn from their exact sampling distribution
N, R = 1_250_000, 2000
def one():
    k_t, k_c = rng.binomial(N, SHARE, 2)                       # triggered users per arm
    # triggered users: control mean MU, treatment mean MU*1.0125; the other users: MU in both arms
    t_trig = rng.normal(MU * 1.0125, SD / np.sqrt(k_t)); c_trig = rng.normal(MU, SD / np.sqrt(k_c))
    t_non = rng.normal(MU, SD / np.sqrt(N - k_t)); c_non = rng.normal(MU, SD / np.sqrt(N - k_c))
    t_all = (k_t * t_trig + (N - k_t) * t_non) / N; c_all = (k_c * c_trig + (N - k_c) * c_non) / N
    se_all = SD * np.sqrt(2 / N); se_trig = SD * np.sqrt(1 / k_t + 1 / k_c)
    return (t_all - c_all) / se_all, (t_trig - c_trig) / se_trig
zs = np.array([one() for _ in range(R)])
pw = (np.abs(zs) > 1.96).mean(axis=0)
print(f"power with 1.25M assigned per arm: all-users {pw[0]:.2f}; triggered-only {pw[1]:.2f}")
assert pw[0] < 0.2 and 0.7 < pw[1] < 0.9

# the trigger rule must be symmetric. Feature does NOTHING here. Spend ~ heavy-tailed; 'treatment users who clicked the new setting' are engaged users.
M = 400_000
spend_t = rng.lognormal(2.5, 1.0, M); spend_c = rng.lognormal(2.5, 1.0, M)
asym = spend_t[spend_t > np.quantile(spend_t, 1 - SHARE)].mean() / spend_c.mean() - 1                 # treated: 'engaged', control: everybody
sym = spend_t[rng.random(M) < SHARE].mean() / spend_c[rng.random(M) < SHARE].mean() - 1               # same rule on both arms (would-have-reached)
print(f"no true effect: asymmetric trigger reads {asym*100:+.0f}%; symmetric trigger reads {sym*100:+.1f}%")
assert asym > 1.0 and abs(sym) < 0.05
```

**Output (my run):**
```text
triggered lift implied by the prompt: 1.25 %
users per arm for 80% power: triggered analysis 100,466 triggered (= 1,255,821 assigned); all-users analysis 15,697,759; ratio 12.50
power with 1.25M assigned per arm: all-users 0.13; triggered-only 0.80
no true effect: asymmetric trigger reads +329%; symmetric trigger reads -1.4%
```

**Follow-ups:**
- Why is the ratio 12.5? The all-users test needs 156 times the triggered count (12.5 squared): 156 x 100,466 = 15.7 million assigned. The triggered test needs 100,466 / 0.08 = 1.26 million assigned. 15.7 / 1.26 = 12.5 (my run: 15,697,759 against 1,255,821).
- What if I cannot log control triggers? Use the all-users test, or CUPED, or run longer; do not substitute "users who used the feature".
- Does 1.25% scale to the whole base? Only for users who reach the page; effect on others is assumed zero.

**Common mistakes:** Filtering to feature users (selection). Using the triggered number as a company-wide lift. Hiding the ITT result. Changing the trigger after seeing results. Not checking the triggered share per arm.

### Q33 ⭐⭐ 🟡 A team shipped 12 experiments over a year, each measured at about +1% on revenue, so adding them up gives about 12.7% (1.01 to the power 12). A long-term holdout group kept on the year-start experience shows +5.5% relative. Explain why the two differ and how you would report cumulative impact.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
**Say this first (1 line):** The holdout is the better number: individual tests overstate their lifts (winner's curse, novelty), the launches overlap and cannibalise each other, so 12 x +1% does not add up to 12.7%; I would report the holdout with its interval and treat the sum as an upper bound.

**Clarifying questions:**
- How big is the holdout and how long has it been held (users, months)? That gives the holdout's own interval.
- Was the holdout clean (same users all year, no leakage, same logging)? A leaky holdout understates the effect.
- How were the 12 experiments chosen: the significant ones out of how many run? That sizes the winner's curse.
- Which metric: revenue per user, and over what window? The tests may have used a shorter window than the holdout.
- Did anything else change for everybody (pricing, seasonality, marketing)? The holdout is exposed to it too, so those drop out of the difference.

**Approach:**
1. Check the arithmetic: 1.01^12 = 1.1268, so 12.7% if effects compound. In log points 12 x ln(1.01) = 0.1194 against ln(1.055) = 0.0535: the holdout shows only 45% of the promise.
2. Reasons for the gap, in order:
   - Winner's curse: we ship the tests that came out significant, and their measured lifts are inflated by selection. Shipped tests measure about +1% while their true lifts are lower.
   - Novelty and decay: a two-week test captures a peak that fades. The holdout measures the long run.
   - Overlap and cannibalisation: two features that both nudge the same checkout step do not add; the second one has less room.
   - Interference and interaction: tests run on the same users at the same time, so lifts are measured against different baselines.
   - Different measurement: window, population, metric definition.
3. Do not try to split the gap by arithmetic. Say what is plausible and measure what you can: re-run a few launches as reverse tests (holdback) to estimate decay.
4. Report the cumulative impact as the holdout estimate with its interval (the primary number) and the sum of individual tests as a ceiling. Present the realisation ratio (holdout / sum) so the next year's plan uses a discount.
5. Process fixes: confirm big winners with a second test, track long-term holdouts for every quarter, keep a ledger of shipped lifts, apply shrinkage to new results (Book 1 Part 10 Q24 explains long-term holdouts).

**Metrics:**
- Cumulative lift = mean revenue per user (shipped experience) / mean revenue per user (holdout) - 1, same window and same population.
- Naive sum = product of (1 + measured lift) over shipped experiments - 1 = 1.01^12 - 1.
- Realisation ratio = log(1 + holdout lift) / sum of log(1 + individual lifts) = 0.0535 / 0.1194.
- Guardrails: holdout is a random user slice, same logging, no leakage, SRM against the intended share.

**Risks:**
- A holdout that is too small gives a wide interval. With 5% of users the interval is still narrow here (see example).
- Holdout users who leak into the new experience (shared accounts, other devices).
- Holdout users get a worse product for a year (cost, fairness, user churn).
- Treating the gap as proof that tests are useless. They are still valid for direction, not for magnitude.
- Compounding assumption: not all effects multiply.

**What the interviewer scores:**
- Strong: checks 1.01^12 = 12.7% and names winner's curse, novelty and overlap as separate causes. Weak: "the holdout is probably wrong".
- Strong: says which number to report and why (holdout with CI, sum as ceiling). Weak: reports 12.7%.
- Strong: gives the holdout's interval. Weak: treats 5.5% as exact.
- Strong: proposes process changes (confirm winners, shrinkage, rotating holdouts). Weak: stops at the diagnosis.

**Example:** illustrative numbers. 600 candidate ideas, true lifts average +0.30% with SD 0.45%, tests with SE 0.30%, ship the significant ones.
- Weak: "12 launches at +1% each, so we added 12.7% revenue."
- Strong: "The holdout says 5.5% (95% interval about 4.6 to 6.4). The sum is a ceiling because of selection, decay and overlap; the realisation is about 45% in log terms."
- In my run: of 600 ideas, 195 are shipped; their average measured lift is 0.91% but their average true lift is 0.71%. An illustrative chain (0.71% true, 75% remains after novelty, 90% after overlap) gives 0.478% per launch and 5.9% over twelve, in the range of the holdout. The decomposition is invented, only to show that plausible discounts can explain the gap. With a 5% holdout (500,000 users) the +5.5% has SE 0.44 points, interval about 4.6% to 6.4%, so 12.7% is far outside it.

**Code:**
```python
# Q33: 12 shipped +1% experiments vs a +5.5% holdout (illustrative simulation, seeded)
import numpy as np

rng = np.random.default_rng(33)
print("compounded sum of twelve +1%:", round(1.01**12 - 1, 4), "; log-points:", round(12 * np.log(1.01), 4), "vs holdout", round(np.log(1.055), 4))
assert abs(1.01**12 - 1 - 0.1268) < 5e-4
print(f"holdout shows {np.log(1.055)/(12*np.log(1.01))*100:.0f}% of the compounded promise")

# Reason 1: winner's curse. 600 candidate ideas, true lifts mostly small; each test has noise; ship only significant wins.
K, SE = 600, 0.003
true = rng.normal(0.0030, 0.0045, K)
meas = true + rng.normal(0, SE, K)
ship = meas / SE > 1.96
print(f"shipped {ship.sum()} of {K}: average MEASURED lift {meas[ship].mean()*100:.2f}%, average TRUE lift {true[ship].mean()*100:.2f}%")
assert meas[ship].mean() > true[ship].mean() + 0.001 and 0.008 < meas[ship].mean() < 0.012

# Reason 2 and 3 (illustrative factors, to be measured not assumed): novelty fades; overlapping tests cannibalise each other.
true_each = true[ship].mean(); persist = 0.75; overlap = 0.90
per = true_each * persist * overlap
cum = (1 + per) ** 12 - 1
print(f"illustrative chain: {true_each*100:.2f}% true x {persist} still there after novelty x {overlap} after overlap = {per*100:.3f}% each; twelve compounded = {cum*100:.1f}%")
assert 0.045 < cum < 0.065

# Reason 4: the holdout has its own noise. 5% holdout of 10M users, revenue per user CV = 3
N_H, N_L, CV = 500_000, 9_500_000, 3.0
se_rel = CV * np.sqrt(1 / N_H + 1 / N_L)
lo, hi = 1.055 - 1.96 * se_rel * 1.055, 1.055 + 1.96 * se_rel * 1.055
print(f"holdout 5.5% has SE {se_rel*100:.2f} points; 95% CI about {100*(lo-1):.1f}% to {100*(hi-1):.1f}%; 12.7% is far outside")
assert hi - 1 < 0.08
```

**Output (my run):**
```text
compounded sum of twelve +1%: 0.1268 ; log-points: 0.1194 vs holdout 0.0535
holdout shows 45% of the compounded promise
shipped 195 of 600: average MEASURED lift 0.91%, average TRUE lift 0.71%
illustrative chain: 0.71% true x 0.75 still there after novelty x 0.9 after overlap = 0.478% each; twelve compounded = 5.9%
holdout 5.5% has SE 0.44 points; 95% CI about 4.6% to 6.4%; 12.7% is far outside
```

**Follow-ups:**
- Which number goes on the company slide? The holdout figure with its interval, and the footnote that it is measured against the year-start experience.
- Is the holdout always right? It has its own noise and leakage risk. It is the best available estimate of the cumulative effect, not a perfect one.
- How do I stop the gap next year? Confirm winners with a second test, shrink estimates, run shorter holdbacks to measure decay, and avoid stacking tests on the same funnel step.

**Common mistakes:** Adding or compounding test lifts and calling it the annual impact. Believing a decomposition built by arithmetic. Using a tiny holdout. Not stating the holdout's interval. Forgetting that the holdout is a cost to users. Ignoring the order and overlap of launches.

### Q34 ⭐⭐ 🟡 A growth team wants a bandit rather than an A/B test to choose among 6 email subject lines for 600,000 recipients over 2 weeks, and then wants to claim a causal lift for next quarter's plan. Explain when a bandit is right, what you lose for inference and what you recommend.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
**Say this first (1 line):** A bandit is right when the goal is to earn opens during the campaign, not to learn a clean number, and here the team wants both, so I would run a bandit for the send and keep a small fixed-allocation slice (and a no-email holdout) for the causal claim.

**Clarifying questions:**
- What is the goal: maximise opens this fortnight, or learn which line to reuse next quarter? Why: the first is a bandit problem, the second is an estimation problem, and they pull in opposite directions.
- What does "causal lift" mean: line against line, or email against no email? Why: randomized lines answer the first, only a holdout answers the second.
- Can the result be read within the fortnight, or is the open delayed? Why: a bandit needs fast feedback to update; opens mostly arrive in the first day or two, which suits batches.
- Does the best line change by day or segment (a sale day, a weekday)? Why: a bandit chases a moving target and an estimate of "the" lift would not be stable.
- Is open rate the real goal, or purchases from the email? Why: opens can be inflated by privacy-proxy pre-fetching, so I would pick the outcome before the test.

**Approach:**
1. Decide the purpose. Pure "send the best line to as many people as possible, now": bandit. "Tell next quarter's plan how much this lifts revenue": A/B plus holdout.
2. If a bandit: send in daily batches (14 here), allocate each batch by Thompson sampling (draw a plausible rate for each line from its Beta posterior, send more to the line that wins most draws), and keep a floor (say 5% each) so no line is starved.
3. Log the allocation probability for every send. Randomization is still real, but the probabilities change by batch, so analyse with batch-stratified or inverse-probability weights, not a plain pooled rate.
4. Reserve a fixed slice (for example 10% of recipients, split equally over the 6 lines) that is never touched by the bandit. This slice gives clean estimates of every line.
5. Reserve a holdout that gets no email (or last quarter's default line). Only this answers "lift against what we would have done anyway".
6. Report the effect as an interval from the fixed slice, and the opens earned by the bandit as a separate, descriptive number.

**Metrics:**
- Primary for the bandit: open rate = opens / delivered emails (or click rate; pick one before the test).
- Regret = opens if every send had used the best line - opens actually earned.
- Estimate quality: width of the 95% interval for each line's rate and for line-minus-line gaps.
- Guardrails: unsubscribe rate = unsubscribes / delivered, spam-complaint rate, and revenue per recipient, per line.

**Risks:**
- Naive pooled rates from a bandit are biased: a line with an unlucky start gets fewer sends and its estimate stays noisy and low.
- Weak lines get little data, so "line 1 versus line 2" is poorly measured.
- Opens are a proxy; the best-opening line may sell less (a clickbait line raises unsubscribes).
- Taking the best-looking line's rate as next quarter's lift mixes in luck (winner's curse) and changes in audience and season.

**What the interviewer scores:**
- Strong: separates "earn while learning" from "learn", and says what each design gives up.
- Strong: names the bias and the need for allocation probabilities or a fixed slice for inference.
- Strong: asks "lift against what" and brings in a holdout.
- Weak: "bandits are always better because they waste fewer sends."
- Weak: reads the final pooled rate of the winner as the causal lift.

**Example:** (illustrative numbers) Six lines with true open rates 10.0% to 12.0% in 0.4-point steps, 600,000 recipients. Fixed A/B sends 100,000 to each line; the standard error of a gap between two lines is about 0.14 points. Thompson sampling in 14 daily batches earns about 5,300 more opens (8%) than the fixed split and sends only about 7,200 emails to the worst line. Its error on the gap between the two weakest lines is about four times larger. Weak answer: "use a bandit, it wastes fewer sends, and tell finance the winner's rate is the lift." Strong answer: "bandit for the send, a fixed slice and a no-email holdout for the number we plan on."

**Code:**
```python
# Q34: bandit vs fixed A/B for 6 subject lines. Illustrative numbers, seeded.
import numpy as np

N, K, BATCHES = 600_000, 6, 14
rates = np.array([0.100, 0.104, 0.108, 0.112, 0.116, 0.120])   # invented true open rates
assert N // K == 100_000
se_pair = np.sqrt(2 * 0.11 * 0.89 / 100_000)
print(f"fixed A/B: 100,000 per line, SE of a difference ~ {se_pair*100:.2f} points")
assert abs(se_pair - 0.00140) < 1e-4

def run_fixed(rng):
    n = np.full(K, N // K)
    s = rng.binomial(n, rates)
    return n, s

def run_ts(rng):
    n = np.zeros(K); s = np.zeros(K)
    per = N // BATCHES
    for b in range(BATCHES):
        if b == 0:
            share = np.full(K, 1 / K)
        else:
            draws = rng.beta(1 + s, 1 + n - s, size=(2000, K))
            share = np.bincount(draws.argmax(1), minlength=K) / 2000
        send = rng.multinomial(per, share)
        s += rng.binomial(send, rates); n += send
    return n, s

R = 300
rng = np.random.default_rng(34)
res = {}
for name, f in [("fixed", run_fixed), ("thompson", run_ts)]:
    clicks, best, diff_err, win_bias, worst_n = [], [], [], [], []
    for _ in range(R):
        n, s = f(rng)
        clicks.append(s.sum()); est = s / np.maximum(n, 1)
        w = est.argmax(); best.append(w == K - 1)
        win_bias.append(est[w] - rates[w])
        # error on the gap between the two lines with the lowest rates (smallest sample under a bandit)
        diff_err.append(abs((est[1] - est[0]) - (rates[1] - rates[0])))
        worst_n.append(n[0])
    res[name] = dict(clicks=np.mean(clicks), best=np.mean(best), bias=np.mean(win_bias),
                     gap_err=np.mean(diff_err), n_worst=np.mean(worst_n))
    r = res[name]
    print(f"{name:9s} opens={r['clicks']:9.0f} picked_true_best={r['best']:.0%} "
          f"bias_of_winner_estimate={r['bias']*100:+.3f} pts  abs_err_on_gap(line1-line0)={r['gap_err']*100:.3f} pts  sends_to_worst_line={r['n_worst']:.0f}")

best_possible = N * rates.max()
print("opens if every send used the best line:", int(best_possible))
assert res["thompson"]["clicks"] > res["fixed"]["clicks"]
assert res["thompson"]["n_worst"] < 0.5 * res["fixed"]["n_worst"]
assert res["thompson"]["gap_err"] > res["fixed"]["gap_err"]
extra = res["thompson"]["clicks"] - res["fixed"]["clicks"]
print(f"extra opens from the bandit: {extra:.0f} ({extra/res['fixed']['clicks']:.1%})")
```

**Output (my run):**
```text
fixed A/B: 100,000 per line, SE of a difference ~ 0.14 points
fixed     opens=    65992 picked_true_best=100% bias_of_winner_estimate=-0.007 pts  abs_err_on_gap(line1-line0)=0.103 pts  sends_to_worst_line=100000
thompson  opens=    71333 picked_true_best=100% bias_of_winner_estimate=-0.001 pts  abs_err_on_gap(line1-line0)=0.425 pts  sends_to_worst_line=7196
opens if every send used the best line: 72000
extra opens from the bandit: 5341 (8.1%)
```
The bandit picks the best line every time in this easy case (a 2-point spread over 600,000 sends), so the cost shows up as precision on the weak lines, not as a wrong winner. With closer lines or a shifting best line it can also pick wrongly.

**Follow-ups:**
- Why not just estimate lift from the bandit's data? You can, with batch or inverse-probability weights, but the weak lines stay poorly measured and an adaptive design changes the usual p-value rules. A fixed slice is simpler. See Book 1 Part 10 Q41 (multi-armed bandit).
- Could a contextual bandit help? Yes if the best line differs by segment, but then the estimate is per segment and needs even more data.

**Common mistakes:** Calling the bandit's pooled rate a causal lift. Forgetting there is no no-email control. Letting the bandit starve a line completely. Judging on opens when the business outcome is purchases. Using one number for next quarter without noting season and audience change.

### Q35 ⭐⭐ 🟡 A search ranking change raises click-through per query by 5% relative to control but raises queries per session by 8% (users reformulating) and leaves purchases per session flat. Explain how you interpret these conflicting metrics and what additional metric or cut you would build before deciding.
**Asked at:** Guardrail and ship-decision material (a Dataford 'primary vs guardrail metrics' page, a Spotify Confidence guardrail-metric glossary and blog post, PracHub analytics-and-experimentation question pages, a Dataford 'non significant test PM wants launch' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** CTR per query rose because the number of queries (the denominator) rose for the wrong reason, so I do not read it as a win; I decide on a per-session outcome (purchases or successful sessions) and build a "queries to success" view.

**Clarifying questions:**
- Is "reformulating" confirmed from logs (a second query within seconds, with an edited string) or is it a guess? Why: the whole story depends on whether extra queries are retries or genuine new intent.
- What is the business goal of search: purchases, revenue, or satisfaction? Why: it picks the primary metric.
- How wide is the interval on purchases per session? Why: "flat" can hide a real effect of a few percent either way.
- Does the change alter which results sit at the top (a ranking change) or only the snippets? Why: it tells me whether more clicks could mean better results or just more attempts.
- Are there human-rated relevance scores or a satisfaction survey I can add? Why: they separate "found it faster" from "needed more tries".

**Approach:**
1. Do the arithmetic. Clicks per session = CTR per query x queries per session = 1.05 x 1.08 = 1.134, so clicks per session are up about 13%, while purchases per session are flat. More clicks, same purchases.
2. Name the trap. CTR per query is a ratio. If users have to ask more times, the denominator grows. A higher CTR per query alongside more queries per session is the signature of retries, not of better results.
3. Pick the unit of decision: the session (or the user), because a purchase journey spans queries. Primary metric: purchases (or successful sessions) per session.
4. Build the missing metrics: reformulation rate, queries until first click or purchase, share of sessions with 3+ queries, abandonment (no click) rate, and time to first click.
5. Cut by query type (navigational, specific product, broad) and by new versus returning users. A ranking change may help broad queries and hurt specific ones.
6. Get an independent quality signal: a human-rated relevance sample, or a short "did you find it?" prompt.
7. Decide. If purchases per session are flat with a tight interval, queries per purchase go up and satisfaction is not better, then do not ship on CTR; consider iterating on the ranking.

**Metrics:**
- Primary: purchases per session = purchase count / sessions (or successful-session rate = sessions with a purchase or a long click / sessions).
- Diagnostic: reformulation rate = queries that follow another query within a short window with an edited string / all queries; queries per purchase = queries / purchases.
- Guardrails: zero-result rate, abandonment rate, latency, revenue per session.
- Ratio metrics get a delta-method or user-level interval; do not use the plain binomial formula on queries.

**Risks:**
- Optimising CTR per query rewards making the first result less satisfying (more retries, more clicks).
- A flat purchase result may still hide a few-percent change: the interval is the evidence, not the word "flat".
- Retries can be a good sign in discovery search (users exploring). Query type matters.
- Position and presentation changes alter clicks without changing relevance.

**What the interviewer scores:**
- Strong: multiplies the metrics (1.05 x 1.08 = 1.134) and spots the changing denominator.
- Strong: chooses a session or user outcome, then adds "queries to success" and a relevance check.
- Strong: asks for the interval on the flat metric.
- Weak: "CTR is up, queries are up, ship it" or "queries are up so it is bad" without checking the data.
- Weak: treats all three metrics as equally important.

**Example:** (illustrative numbers) Control: 2.00 queries per session, CTR 30.0% per query, 5.0% of sessions buy. Treatment: 2.16 queries, CTR 31.5%, 5.0% buy. In the code, clicks per session go from 0.60 to 0.68 (+13%), purchases per session differ by +0.08 points with an interval of -1.0% to +4.4% relative, queries per purchase go from 40.8 to 43.2, and the share of sessions with 3 or more queries goes from 26% to 32%. Weak answer: "CTR rose 5%, so ranking is better." Strong answer: "CTR per query rose because queries rose; purchases per session are flat, so I would not call it a win until queries-to-success and relevance agree."

**Code:**
```python
# Q35: CTR/query +5%, queries/session +8%, purchases/session flat. Illustrative, seeded.
import numpy as np
from scipy import stats

print("clicks per session ratio =", round(1.05 * 1.08, 3))
assert round(1.05 * 1.08, 3) == 1.134      # +13.4% clicks per session implied

rng = np.random.default_rng(35)
S = 200_000                                  # sessions per arm
def arm(q_mean, ctr, p_buy):
    q = rng.poisson(q_mean - 1, S) + 1       # queries per session (>=1)
    clicks = rng.binomial(q, ctr)
    buy = rng.random(S) < p_buy              # purchase does not depend on arm by construction
    first_click = (clicks > 0)
    return q, clicks, buy, first_click
qc, cc, bc, fc = arm(2.00, 0.300, 0.050)
qt, ct, bt, ft = arm(2.16, 0.315, 0.050)

print(f"queries/session  C {qc.mean():.3f}  T {qt.mean():.3f}  ({qt.mean()/qc.mean()-1:+.1%})")
ctr_c, ctr_t = cc.sum()/qc.sum(), ct.sum()/qt.sum()
print(f"CTR per query    C {ctr_c:.4f}  T {ctr_t:.4f}  ({ctr_t/ctr_c-1:+.1%})")
print(f"clicks/session   C {cc.mean():.3f}  T {ct.mean():.3f}  ({ct.mean()/cc.mean()-1:+.1%})")
assert abs(qt.mean()/qc.mean() - 1.08) < 0.01 and abs(ctr_t/ctr_c - 1.05) < 0.02

d = bt.mean() - bc.mean()
se = np.sqrt(bt.var()/S + bc.var()/S)
lo, hi = d - 1.96*se, d + 1.96*se
print(f"purchases/session diff {d*100:+.2f} pts, 95% CI [{lo*100:+.2f}, {hi*100:+.2f}] pts  = [{lo/0.05:+.1%}, {hi/0.05:+.1%}] relative")
assert lo < 0 < hi                           # flat: cannot reject zero
print(f"width of CI: +/-{1.96*se/0.05:.1%} relative -> a flat result rules out only effects bigger than that")
# extra cut: queries needed per purchase, and share of sessions with 3+ queries
print(f"queries per purchase  C {qc.sum()/bc.sum():.1f}  T {qt.sum()/bt.sum():.1f}")
print(f"sessions with 3+ queries  C {np.mean(qc>=3):.1%}  T {np.mean(qt>=3):.1%}")
assert np.mean(qt >= 3) > np.mean(qc >= 3)
```

**Output (my run):**
```text
clicks per session ratio = 1.134
queries/session  C 2.000  T 2.155  (+7.7%)
CTR per query    C 0.2999  T 0.3149  (+5.0%)
clicks/session   C 0.600  T 0.679  (+13.1%)
purchases/session diff +0.08 pts, 95% CI [-0.05, +0.22] pts  = [-1.0%, +4.4%] relative
width of CI: +/-2.7% relative -> a flat result rules out only effects bigger than that
queries per purchase  C 40.8  T 43.2
sessions with 3+ queries  C 26.4%  T 32.1%
```
In this simulation the purchase probability is identical by construction, so the "flat" is built in. The simulation shows the arithmetic and the interval width, not what real users do.

**Follow-ups:**
- What if purchases per session were up 1% but not significant? Report the interval, say the effect is small and unproven, and decide on cost and risk. See the Part 4 question on a flat result (Q5) in this part for how to read a CI that includes both zero and a useful effect.
- Why per session and not per query? A purchase belongs to a journey, and retries are part of the journey. See Book 1 Part 10 Q27 (ratio metrics, per-session versus per-user).

**Common mistakes:** Reading CTR per query as quality. Ignoring that the denominator moved. Calling "flat" "no effect". Using a binomial interval on queries from the same user. Judging a ranking change without a query-type cut.

### Q36 ⭐⭐ 🟡 A support assistant with a new model raises the share of conversations resolved without a human from 60% to 63% (3 points absolute, 5% relative to control) in a user-level test, but the same user can get different answers to the same question on a retry. Explain how nondeterminism affects the design, which unit you randomize and what you measure besides resolution.
**Asked at:** AI-era experiment material (an Atlan 2026 guide to A/B testing LLM applications, tianpan.co 2026 posts on non-deterministic AI features, an efficientlyconnected.com post on nondeterminism); practitioner posts rather than confirmed interview banks, an emerging theme; search snippets only, not opened
**Say this first (1 line):** Randomize by user, because the same user retrying must stay on one model, then analyse at user level (or with user-clustered errors), since conversations from one user are not independent and the same prompt can give different answers.

**Clarifying questions:**
- How is "resolved without a human" defined: user did not ask for an agent, did not contact again within 7 days, or confirmed by the user? Why: a reply that ends the chat is not the same as a solved problem.
- How many conversations does one user have in the test window? Why: it sets the design effect and the sample size.
- Can the model be made less random (temperature, fixed seed) and is it? Why: it tells me whether the noise is in the design or in the product.
- Do users share accounts or devices (a household, a company seat)? Why: it may need account-level randomization.
- What does a bad answer cost (refund, wrong advice, a complaint)? Why: it sets the guardrails.

**Approach:**
1. Arithmetic first: 60% to 63% is +3 percentage points, +5% relative to control. Say both.
2. Choose the unit. Randomize by user (or account): the same person must not see model A on Monday and model B on retry, or the arms contaminate each other and trust drops. Per-conversation randomization is wrong for this reason.
3. Accept that the model is random. Two things vary: between users (some users have easier problems) and within a user (the same question can resolve or not). Neither makes the test invalid; it makes the variance larger than a coin-flip formula says.
4. Analyse with the user as the unit: mean resolution per user, compare users. Or use conversation data with user-clustered standard errors. Do not treat every conversation as independent.
5. Size the test on users: independent-conversation sample size is about 4,100 per arm for this lift; with 4 conversations per user and intra-user correlation 0.2 the design effect is 1 + 3 x 0.2 = 1.6, so plan for roughly 1.6 times as many conversations, or count users accordingly.
6. Measure more than resolution (below), and sample conversations for human review of correctness.

**Metrics:**
- Primary: resolution rate per user = conversations resolved without a human / conversations, averaged over users (or total resolved / total conversations with user-clustered SE).
- Quality: human-audited correctness on a random sample (not on resolved ones only), hallucination or policy-violation rate.
- Guardrails: re-contact within 7 days of a "resolved" conversation, escalation rate, CSAT, latency (p95), cost per conversation.
- Stability: share of repeated identical questions with a different outcome.

**Risks:**
- "Resolved" can rise because users give up (they stop asking). The re-contact metric catches this.
- Treating conversations as independent gives intervals that are too narrow and p-values that are too small.
- A user who retries may be the unhappy case; excluding retries hides the problem.
- Model changes or provider updates in the middle of the test change the treatment.

**What the interviewer scores:**
- Strong: user-level randomization with a reason, and clustered or user-level analysis.
- Strong: separates between-user and within-user randomness and does the design-effect arithmetic.
- Strong: adds a quality and a re-contact metric instead of resolution alone.
- Weak: "LLM is non-deterministic so A/B tests do not work."
- Weak: randomizes per conversation or per message.

**Example:** (illustrative numbers) 3,000 users per arm, 4 conversations each, true resolution 60% versus 63%, intra-user correlation 0.2. In the simulated run the observed gap is 2.7 points; the naive standard error (all 12,000 conversations independent) is 0.63 points, the user-level one is 0.80 points, and the implied design effect is about 1.6. So the naive z of 4.4 falls to 3.5. Weak answer: "12,000 conversations per arm, so the 3 points are certain." Strong answer: "users are the unit; 3,000 users is the real sample size, and I check re-contact before believing resolution."

**Code:**
```python
# Q36: LLM support assistant, 60% -> 63% resolved. Nondeterminism, unit, clustering. Illustrative, seeded.
import numpy as np
from scipy import stats

p0, p1 = 0.60, 0.63
print(f"absolute {100*(p1-p0):.0f} points, relative {(p1/p0-1):.0%}")
assert round(p1 - p0, 2) == 0.03 and round(p1 / p0 - 1, 2) == 0.05

# sample size per arm if every conversation were independent (two-sided 5%, 80% power)
za, zb = stats.norm.ppf(0.975), stats.norm.ppf(0.80)
pbar = (p0 + p1) / 2
n_ind = 2 * pbar * (1 - pbar) * (za + zb) ** 2 / (p1 - p0) ** 2
print(f"independent conversations needed per arm: {n_ind:,.0f}")
assert 4000 < n_ind < 4400

# users have a personal resolve-propensity, and the same user retries: conversations in a user are correlated
rng = np.random.default_rng(36)
U, M = 3000, 4                      # users per arm, conversations per user
def arm(p, icc=0.2):
    a = p * (1 - icc) / icc; b = (1 - p) * (1 - icc) / icc       # Beta with intra-user correlation icc
    pu = rng.beta(a, b, U)
    y = rng.binomial(1, pu[:, None], (U, M))
    return y
yc, yt = arm(p0), arm(p1)
rc, rt = yc.mean(), yt.mean()
# naive: treat all U*M conversations as independent
se_naive = np.sqrt(rc*(1-rc)/(U*M) + rt*(1-rt)/(U*M))
# user-level: mean per user, compare users
uc, ut = yc.mean(1), yt.mean(1)
se_user = np.sqrt(uc.var(ddof=1)/U + ut.var(ddof=1)/U)
d = rt - rc
deff = (se_user / se_naive) ** 2
print(f"observed diff {d*100:+.2f} pts; naive SE {se_naive*100:.2f} pts; user-level SE {se_user*100:.2f} pts; design effect ~ {deff:.2f}")
print(f"naive z = {d/se_naive:.2f}   user-level z = {d/se_user:.2f}")
assert se_user > 1.2 * se_naive          # clustering widens the interval
rho = (deff - 1) / (M - 1)
print(f"implied intra-user correlation {rho:.2f} (built in: 0.20)")
assert 0.1 < rho < 0.3

# how much of the "same user, different answer" noise exists: same question, 5 retries, answer is right with prob q
q = 0.63
agree = q**2 + (1-q)**2
print(f"if retries were independent draws, two tries at the same question give the same outcome {agree:.0%} of the time when p(resolve)={q}")
assert round(agree, 2) == 0.53
```

**Output (my run):**
```text
absolute 3 points, relative 5%
independent conversations needed per arm: 4,130
observed diff +2.74 pts; naive SE 0.63 pts; user-level SE 0.80 pts; design effect ~ 1.62
naive z = 4.38   user-level z = 3.45
implied intra-user correlation 0.21 (built in: 0.20)
if retries were independent draws, two tries at the same question give the same outcome 53% of the time when p(resolve)=0.63
```
The intra-user correlation and the 4 conversations per user are invented. The point is the direction and size of the correction, which depends on your real data.

**Follow-ups:**
- Could you set temperature to 0 to remove the noise? It lowers within-prompt randomness but does not make the test unnecessary, and it changes the product you ship. Test the setting you will ship. See Book 1 Part 10 Q55 (non-deterministic treatment).
- What about a user who only has one conversation? They count once; the clustering matters for users with several.

**Common mistakes:** Per-conversation randomization. Intervals computed as if all conversations were independent. Reporting resolution alone. Excluding users who retried. Ignoring that "resolved" can mean "gave up".

### Q37 ⭐⭐ 🟡 An LLM judge prefers the new model in 620 of 1,000 offline pairs (62%), but humans agree with the judge on only 71% of 200 audited pairs, and the new model's answers are 35% longer. Explain how you validate the judge, what the 62% really tells you and how it connects to the online test.
**Asked at:** AI-era experiment material (an Atlan 2026 guide to A/B testing LLM applications, tianpan.co 2026 posts on non-deterministic AI features, an efficientlyconnected.com post on nondeterminism); practitioner posts rather than confirmed interview banks, an emerging theme; search snippets only, not opened
**Say this first (1 line):** The 62% is a judge's win rate on offline pairs, and with 71% agreement with humans and a 35% length gap it is weak evidence of better quality, so I validate the judge first and let only the online test decide.

**Clarifying questions:**
- How were the 200 audited pairs chosen: random, or the ones the judge was unsure about? Why: a biased audit gives biased agreement.
- Are the 1,000 pairs on the same prompts for both models and in random A/B order? Why: position bias in the judge would favour one slot.
- What does the judge see: only the answers, or also model names, and is it the same family as the new model? Why: judges often prefer their own style (self-preference).
- Were ties possible? Why: forcing a winner on tied pairs adds noise.
- What is the online decision this feeds: ship, or just pick which candidate to test? Why: a screening use needs less proof than a ship decision.

**Approach:**
1. Say what 62% is. 620 of 1,000 pairs means the judge preferred the new answer in 62% of pairs; the interval from sampling noise alone is about 59% to 65%. It says nothing about whether the judge is right.
2. Measure judge quality on the human-audited pairs. Agreement 71% is not very high for a two-answer choice; where the two sides are about equally likely, chance agreement is already about 50%, so Cohen's kappa is the better figure (about 0.42 in my invented table).
3. Break the audit down: where does the judge disagree with humans, and does the disagreement correlate with length, with answer position, or with style?
4. Correct the headline for judge error. If the judge says "new" in 80% of the cases where humans say "new" and 38% where humans say "old", the error-corrected human-preference rate is about 57%, with a wide interval (about 40% to 74%) that includes 50%.
5. Control length: compare at matched length, or add a length-penalised judge, or use pairwise comparisons where the judge is told not to reward length. Swap the order of the two answers and average.
6. Use the judge as a screen, not a verdict. Ship decisions come from the online test, with the judge as a monitoring metric whose link to online outcomes is checked.

**Metrics:**
- Judge win rate = pairs where the judge prefers new / pairs judged (62%), with an interval.
- Agreement = pairs where judge and human agree / audited pairs (71%); kappa = (agreement - chance agreement) / (1 - chance agreement).
- Per-slice agreement (by length bucket, position, topic).
- Online: task success, re-contact, CSAT, cost, latency; correlation between offline judge score and online outcome across past experiments.

**Risks:**
- Length bias: longer answers look more complete to a judge; 35% longer is a red flag.
- Self-preference when the judge shares a model family with one candidate.
- Position bias (the first answer wins too often).
- A small audit (200 pairs) gives a wide interval on agreement, about 64% to 77%.
- Optimising for the judge makes the judge a worse measure (it becomes the target).

**What the interviewer scores:**
- Strong: separates "the judge's win rate" from "truth", and quantifies judge error with an audit.
- Strong: names length, position and self-preference bias, and a control for each.
- Strong: connects to the online test and says offline only screens.
- Weak: "62% win rate, ship."
- Weak: "71% agreement is fine" with no chance-correction.

**Example:** (illustrative numbers) The invented audit has 80 pairs where both say new, 38 where the judge says new and humans say old, 20 where the judge says old and humans say new, 62 where both say old. Agreement is 142/200 = 71%, kappa 0.42. Correcting 62% for those error rates gives about 57%, interval 40% to 74%. A second simulation shows a judge that adds a small length bonus gives a 58% win rate at exactly equal quality, and 71% with a larger bonus. Weak answer: "the judge likes the new model 62% of the time, so it is better." Strong answer: "the judge is only moderately reliable and length-biased; the corrected preference could be near 50%, so I run the online test."

**Code:**
```python
# Q37: LLM judge 620/1000, humans agree on 71% of 200 audited pairs, new answers 35% longer. Illustrative, seeded.
import numpy as np
from scipy import stats

n, w = 1000, 620
assert w / n == 0.62
def wilson(k, n, z=1.96):
    p = k / n; c = (p + z*z/(2*n)) / (1 + z*z/n)
    h = z * np.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    return c - h, c + h
lo, hi = wilson(w, n)
print(f"judge win rate 62.0%, 95% CI [{lo:.1%}, {hi:.1%}] (sampling noise only)")
assert 0.58 < lo < 0.60 and 0.64 < hi < 0.66

# invented audit table of 200 pairs: judge says new wins (Jn) / old wins (Jo); human says new (Hn) / old (Ho)
Jn_Hn, Jn_Ho, Jo_Hn, Jo_Ho = 80, 38, 20, 62
assert Jn_Hn + Jn_Ho + Jo_Hn + Jo_Ho == 200
agree = (Jn_Hn + Jo_Ho) / 200
print(f"agreement {agree:.0%}")
assert agree == 0.71
po = agree
pj = (Jn_Hn + Jn_Ho) / 200; ph = (Jn_Hn + Jo_Hn) / 200
pe = pj * ph + (1 - pj) * (1 - ph)
kappa = (po - pe) / (1 - pe)
print(f"Cohen kappa {kappa:.2f}")
tpr = Jn_Hn / (Jn_Hn + Jo_Hn)       # P(judge says new | human says new)
fpr = Jn_Ho / (Jn_Ho + Jo_Ho)       # P(judge says new | human says old)
print(f"judge says 'new' when humans say new: {tpr:.0%}; when humans say old: {fpr:.0%}")
# correct the 62% for judge error (Rogan-Gladen), bootstrap over the audit
def corrected(j, tpr, fpr): return (j - fpr) / (tpr - fpr)
h_hat = corrected(0.62, tpr, fpr)
print(f"error-corrected human-preference rate ~ {h_hat:.1%}")
rng = np.random.default_rng(37)
cells = np.array([Jn_Hn, Jn_Ho, Jo_Hn, Jo_Ho]); hs = []
for _ in range(4000):
    a, b, c, d = rng.multinomial(200, cells / 200)
    t, f = a / max(a + c, 1), b / max(b + d, 1)
    j = rng.binomial(n, 0.62) / n
    if t - f > 0.1: hs.append(corrected(j, t, f))
ci = np.percentile(hs, [2.5, 97.5])
print(f"bootstrap 95% interval for the corrected rate: [{ci[0]:.1%}, {ci[1]:.1%}]")
assert ci[0] < 0.5 < ci[1]   # the interval reaches 50%: no preference not ruled out
# length bias: a judge that adds a bonus for length prefers longer answers even at equal quality
rng = np.random.default_rng(371)
quality_diff = rng.normal(0, 1, 100_000)          # new minus old, true mean 0
for bonus in (0.0, 0.3, 0.8):
    wins = np.mean(quality_diff + bonus + rng.normal(0, 1, 100_000) > 0)
    print(f"true quality equal, judge length bonus {bonus:.1f} -> judge win rate {wins:.1%}")
```

**Output (my run):**
```text
judge win rate 62.0%, 95% CI [59.0%, 65.0%] (sampling noise only)
agreement 71%
Cohen kappa 0.42
judge says 'new' when humans say new: 80%; when humans say old: 38%
error-corrected human-preference rate ~ 57.1%
bootstrap 95% interval for the corrected rate: [40.1%, 73.9%]
true quality equal, judge length bonus 0.0 -> judge win rate 50.1%
true quality equal, judge length bonus 0.3 -> judge win rate 58.3%
true quality equal, judge length bonus 0.8 -> judge win rate 71.5%
```
The audit table, the length bonus and the noise scale are invented for illustration. The correction formula assumes the judge's error rates are the same on the 1,000 pairs as on the audited 200.

**Follow-ups:**
- How big should the audit be? Big enough that the agreement interval is narrow relative to the decision, and stratified by length and topic; 200 pairs gives about plus or minus 6 points. See Book 1 Part 10 Q56 (validating an LLM judge).
- What if humans also disagree with each other? Then agreement with any single human is capped; measure human-human agreement first.

**Common mistakes:** Treating the judge as ground truth. Quoting raw agreement without chance correction. Ignoring length and position. Using the same model family as judge and candidate. Skipping the online test because the offline number is "significant".

### Q38 ⭐⭐ 🟡 An LLM feature raises satisfaction by 2 points but also raises 95th-percentile latency from 1.4 to 3.1 seconds and cost per query from 0.002 to 0.012 dollars (6 times). Explain how you frame the ship decision, which guardrails and budgets you set and what you propose as the next experiment.
**Asked at:** AI-era experiment material (an Atlan 2026 guide to A/B testing LLM applications, tianpan.co 2026 posts on non-deterministic AI features, an efficientlyconnected.com post on nondeterminism); practitioner posts rather than confirmed interview banks, an emerging theme; search snippets only, not opened
**Say this first (1 line):** A 2-point satisfaction gain is worth shipping only if it pays for a 6 times cost and a slower tail, so I turn the guardrails into budgets, test a routed version that keeps most of the gain, and decide on value per query minus cost per query.

**Clarifying questions:**
- How is satisfaction measured and what is its interval? Why: +2 points may be inside the noise, and it may be measured only on users who answered a survey.
- What does one satisfaction point do for the business (retention, conversion, fewer escalations)? Why: it is the only way to compare 2 points with 0.010 dollars per query.
- What is the latency budget (p95 where users give up, for example)? Why: a tail of 3.1 seconds may cross a drop-off threshold.
- Is the cost of the feature on the margin of this product, or does it scale with usage? Why: 6 times cost on millions of queries is a budget line.
- Which queries gained the most: all, or a hard subset? Why: it decides if routing can keep the gain.

**Approach:**
1. Do the arithmetic: cost 0.012 / 0.002 = 6 times; p95 latency 3.1 / 1.4 = 2.2 times. Say the +2 points has to be paid for twice.
2. Check the benefit is real: interval on satisfaction, effect on a harder outcome (task success, return rate), not only a survey.
3. Convert to money per user: extra cost per query x queries per user. With 20 queries per user per month (invented) that is 0.20 dollars, so the 2 points must be worth at least 0.10 dollars per point per user-month to break even.
4. Set budgets as guardrails before deciding: p95 latency (say at most 2.0 s), p99, timeout rate, cost per query (say at most 0.006 dollars), and a per-user cost cap. A guardrail is a bound with a decision attached, not a dashboard.
5. Look at where the cost and the tail come from. A slow path used for a minority of queries can raise p95 while the median barely moves.
6. Propose the next experiment: a routed arm (cheap model by default, large model for hard queries), a cached or shorter-answer arm, and a streaming display so users see text early. Compare satisfaction, p95, and cost per query against the budgets.
7. Ship only an arm inside the budgets; if none, decide explicitly whether the value covers the cost.

**Metrics:**
- Primary: satisfaction score (or task success), mean difference with interval.
- Latency: p50, p95, p99 and timeout rate of end-to-end time, per arm.
- Cost per query = total model spend / queries; cost per successful task = spend / successes.
- Net value per user = (value of satisfaction gain) - (extra cost per user).
- Guardrails: abandonment after slow responses, error rate, escalation rate.

**Risks:**
- Percentiles are not additive; compare them with a bootstrap or quantile interval, not by subtracting group averages.
- Satisfaction from a survey is biased to people who answer.
- The cost increase can grow with usage (longer conversations) beyond the test period.
- A novelty effect can make the 2 points shrink later.

**What the interviewer scores:**
- Strong: converts the quality gain to money and sets budgets before deciding.
- Strong: treats p95, not the mean, as the latency guardrail and asks where the tail comes from.
- Strong: proposes a routed or cheaper variant as the next test instead of a yes/no.
- Weak: "satisfaction went up so ship" or "6 times cost, so no".
- Weak: no numbers on break-even.

**Example:** (illustrative numbers) 20 queries per user per month. Extra cost is 0.010 x 20 = 0.20 dollars per user-month, so each of the 2 points must be worth about 0.10 dollars per user-month. In the code, a slow path used on 8% of queries lifts p95 from about 1.4 s to about 3.1 s while the median moves only from 0.80 s to 0.94 s. If only 30% of queries go to the large model, the blended cost is 0.005 dollars (2.5 times), and the next test checks whether it keeps most of the 2 points. Weak answer: "users are happier, ship it." Strong answer: "the gain is worth shipping only if it clears 0.20 dollars per user and a 2 s p95, so I test a routed version."

**Code:**
```python
# Q38: satisfaction +2 points, p95 latency 1.4 -> 3.1 s, cost 0.002 -> 0.012 dollars. Illustrative, seeded.
import numpy as np

print("cost multiple:", 0.012 / 0.002, " p95 multiple:", round(3.1 / 1.4, 2))
assert round(0.012 / 0.002, 6) == 6.0 and round(3.1 / 1.4, 2) == 2.21

# break-even: extra cost per user-month vs value of +2 satisfaction points (value per point is a made-up input)
q_per_user = 20                      # queries per user per month (invented)
extra_cost = (0.012 - 0.002) * q_per_user
print(f"extra cost per user-month: {extra_cost:.2f} dollars")
assert abs(extra_cost - 0.20) < 1e-9
need_per_point = extra_cost / 2
print(f"the 2 points must be worth at least {need_per_point:.2f} dollars per point per user-month to break even")

# latency: where does a p95 jump come from? a slow path for a minority of queries
rng = np.random.default_rng(38)
n = 200_000
old = rng.lognormal(np.log(0.8), 0.35, n)
slow = rng.random(n) < 0.08                         # 8% of queries go through a slow reasoning path
new = np.where(slow, rng.lognormal(np.log(3.3), 0.25, n), rng.lognormal(np.log(0.9), 0.35, n))
for name, x in (("old", old), ("new", new)):
    print(f"{name}: p50 {np.percentile(x,50):.2f}s  p95 {np.percentile(x,95):.2f}s  mean {x.mean():.2f}s")
assert np.percentile(new, 95) > 2 * np.percentile(old, 95)
assert np.percentile(new, 50) < 1.3 * np.percentile(old, 50)

# routing: send only hard queries to the expensive model
cheap, dear = 0.002, 0.012
for share in (1.0, 0.5, 0.3, 0.2):
    blended = share * dear + (1 - share) * cheap
    print(f"share of queries on the large model {share:.0%}: blended cost {blended:.4f} dollars ({blended/cheap:.1f}x)")
assert abs((0.3 * dear + 0.7 * cheap) - 0.005) < 1e-12
```

**Output (my run):**
```text
cost multiple: 6.0  p95 multiple: 2.21
extra cost per user-month: 0.20 dollars
the 2 points must be worth at least 0.10 dollars per point per user-month to break even
old: p50 0.80s  p95 1.42s  mean 0.85s
new: p50 0.94s  p95 3.06s  mean 1.15s
share of queries on the large model 100%: blended cost 0.0120 dollars (6.0x)
share of queries on the large model 50%: blended cost 0.0070 dollars (3.5x)
share of queries on the large model 30%: blended cost 0.0050 dollars (2.5x)
share of queries on the large model 20%: blended cost 0.0040 dollars (2.0x)
```
The latency mixture and the value per point are invented. The routed 2.5 times figure is blended arithmetic; whether routing keeps the gain is exactly what the next experiment must measure.

**Follow-ups:**
- Who decides the budget? Product and finance own the cost line, engineering the latency line, the data scientist writes the break-even and the experiment; the budget is agreed before the result.
- What if the gain is only for hard queries? Route those to the large model and keep the cheap path elsewhere.

**Common mistakes:** Deciding on satisfaction alone. Comparing mean latency when users feel the tail. Ignoring cost until finance asks. Treating a guardrail as a suggestion. Shipping without testing a cheaper variant.

### Q39 ⭐⭐ 🔴 A booking platform gave a pricing tool to a random half of 10,000 hosts, and treated listings average 10.8 bookings a month against 10.0 for control listings (+8% relative to control). Guest demand in each city is roughly fixed, so the two groups compete for the same bookings. Explain what the +8% measures, what the market-level effect could be and how you design a test to estimate it.
**Asked at:** Marketplace, interference and switchback material (Dataford 'interference in marketplace experiments', 'marketplace experiment with interference' and 'choose switchback for marketplace dispatch' pages, a DoorDash careers blog post, an arXiv 2022 paper on switchbacks and interference bias, a Statsig marketplace-experimentation page); company practice is described only as the snippets reported it; search snippets only, not opened
**Say this first (1 line):** The +8% compares treated listings with control listings that lost the bookings the treated ones won, so it measures a share gain, and the effect on the whole market could be near zero; I would randomize whole cities, not hosts.

**Clarifying questions:**
- How fixed is demand: does a cheaper or better-priced listing bring in new guests, or only move them? Why: it decides whether the market effect is zero or a fraction of +8%.
- What does the tool do (lower prices, smarter prices)? Why: lower prices can grow demand, smarter prices may only reshuffle it.
- Do the 10,000 hosts sit in a few cities or many? Why: the number of independent markets is the real sample size.
- What is the outcome that matters: bookings, revenue, host earnings, guest satisfaction? Why: a booking at a lower price can be worth less.
- Is there a month or more of pre-launch data per city? Why: it lets me remove city-to-city differences.

**Approach:**
1. Say what +8% is. Treated 10.8 versus control 10.0 is +8% relative to control. If demand is fixed, the market average is the same with everyone treated, and with no-one treated: (5,000 x 10.8 + 5,000 x 10.0) / 10,000 = 10.4. Treated gained 0.4 over that average and control lost 0.4. The 0.8 gap is redistribution.
2. Name the problem: interference. A host's outcome depends on other hosts' assignment (they share guests), so the usual assumption that one unit's outcome does not depend on another's fails.
3. Set the estimand: the global effect, bookings per listing when all listings use the tool versus when none do.
4. Design: randomize at the market level (whole cities), treated cities versus control cities; add a pre-period to adjust each city for its own baseline. A middle path is mixed saturation: cities at 0%, 50% and 100% of hosts treated, which also shows how much of the host-level gap is competition.
5. Accept the cost: only a few dozen independent units, so the interval is wide; use the pre-period (a difference-in-differences or regression adjustment), pair similar cities, and run long enough.
6. Report both: the host-level gap (what a host sees) and the market-level effect (what the platform gets), and say which one the decision depends on.

**Metrics:**
- Primary (market level): bookings per listing = bookings in the city / active listings in the city, compared with the city's own pre-period.
- Also: revenue per listing, guest-side conversion, prices and occupancy, share of bookings going to treated listings within a mixed city.
- Guardrails: guest satisfaction, cancellation rate, host churn in control.
- Host-level gap = treated bookings per listing / control bookings per listing - 1 (+8% here); it is not the market effect.

**Risks:**
- Reading +8% as the platform's gain: it can overstate the market effect up to fully.
- Few clusters give a low-power test; with 40 cities and no pre-period the interval can be tens of percent wide.
- Cities differ in size and season; assignment must be balanced on those.
- Spillover across nearby cities (guests searching in two towns) can leak.

**What the interviewer scores:**
- Strong: does the "fixed pie" arithmetic (10.4) and says the +8% is mostly redistribution if demand is fixed.
- Strong: proposes cluster (city) randomization, mixed saturation, and a pre-period adjustment, and notes the power cost.
- Strong: separates the host view from the platform view.
- Weak: "randomization makes the +8% causal, so it is the effect."
- Weak: proposes more hosts as the fix, which does not remove interference.

**Example:** (illustrative numbers) In the code, 40 cities of 250 listings, guests split by attractiveness, treated listings 8% more attractive. Host-level randomization shows about +8% whether total demand is fixed (true market effect 0%) or grows a little (elasticity 0.25, true market effect +1.9%). City-level randomization with each city compared to its own pre-period recovers 0.0% and +1.9%, with a standard deviation of about 0.9 points across assignments; without the pre-period the standard deviation is about 10 points, which is useless. Weak answer: "10.8 versus 10.0 is +8%, ship." Strong answer: "that is the host-vs-host gap; I would test at city level against each city's own history."

**Code:**
```python
# Q39: host-level pricing tool in a market with roughly fixed guest demand. Illustrative, seeded.
import numpy as np

print("relative lift:", round(10.8 / 10.0 - 1, 3))
assert round(10.8 / 10.0 - 1, 3) == 0.08
tot = 5000 * 10.8 + 5000 * 10.0
print("if demand is fixed, everyone-treated or nobody-treated average =", tot / 10_000)
assert tot / 10_000 == 10.4            # market average bookings per listing is 10.4 either way
print(f"treated gain over market average {10.8-10.4:+.1f}, control loss {10.0-10.4:+.1f}: the gap of 0.8 is all redistribution")

rng = np.random.default_rng(39)
C, N_PER = 40, 250                      # 40 cities, 250 listings each = 10,000 hosts
gamma = np.log(1.08)                    # treated listings are 8% more attractive to guests

def city_bookings(frac_treated, eps, Dper, treated_mask):
    """Guests split across listings in proportion to attractiveness w; city demand grows with mean w**eps."""
    w = np.where(treated_mask, np.exp(gamma), 1.0)
    D = Dper * N_PER * (w.mean() ** eps)
    return rng.poisson(D * w / w.sum())

def host_level(eps):
    diffs = []
    for _ in range(30):
        c = []; t = []
        for _ in range(C):
            m = np.zeros(N_PER, bool); m[: N_PER // 2] = True
            b = city_bookings(0.5, eps, 10.4 * rng.lognormal(0, 0.3), m)
            t.append(b[m].mean()); c.append(b[~m].mean())
        diffs.append(np.mean(t) / np.mean(c) - 1)
    return np.mean(diffs)

def city_level(eps, reps=400):
    est, adj = [], []
    for _ in range(reps):
        treated_city = rng.permutation(C) < C // 2
        tt, cc, tt2, cc2 = [], [], [], []
        for i in range(C):
            Dper = 10.4 * rng.lognormal(0, 0.3)
            m = np.full(N_PER, bool(treated_city[i]))
            b = city_bookings(1.0, eps, Dper, m)
            pre = rng.poisson(Dper * N_PER) / N_PER          # same city, month before launch
            (tt if treated_city[i] else cc).append(b.mean())
            (tt2 if treated_city[i] else cc2).append(b.mean() / pre)
        est.append(np.mean(tt) / np.mean(cc) - 1)
        adj.append(np.mean(tt2) / np.mean(cc2) - 1)
    return np.mean(est), np.std(est), np.mean(adj), np.std(adj)

for eps in (0.0, 0.25):
    h = host_level(eps)
    m, s, ma, sa = city_level(eps)
    print(f"demand elasticity {eps}: host-level estimate {h:+.1%};  city-level estimate {m:+.1%} (sd {s:.1%});  city-level vs own pre-period {ma:+.1%} (sd {sa:.1%})")
    assert sa < s / 3
    assert abs(ma - (1.08 ** eps - 1)) < 0.01
    if eps == 0.0:
        assert abs(h - 0.08) < 0.01 and abs(m) < 0.03
    else:
        assert abs(h - 0.08) < 0.01 and 0.0 < m < 0.06      # true market effect is 1.08**0.25 - 1
print("true market effect with elasticity 0.25:", f"{1.08**0.25-1:+.1%}")
```

**Output (my run):**
```text
relative lift: 0.08
if demand is fixed, everyone-treated or nobody-treated average = 10.4
treated gain over market average +0.4, control loss -0.4: the gap of 0.8 is all redistribution
demand elasticity 0.0: host-level estimate +8.2%;  city-level estimate +0.9% (sd 10.0%);  city-level vs own pre-period -0.0% (sd 0.9%)
demand elasticity 0.25: host-level estimate +8.1%;  city-level estimate +3.6% (sd 10.3%);  city-level vs own pre-period +1.9% (sd 0.9%)
true market effect with elasticity 0.25: +1.9%
```
The elasticity, the city-demand spread and the Poisson booking noise are invented, so the numbers show the pattern (host-level gap versus market effect, and why the pre-period matters), not a real platform.

**Follow-ups:**
- Why not just use a bigger sample of hosts? More hosts shrink noise but not the bias from competition. See Book 1 Part 10 Q37 (marketplace experiments) and Q29 in this part (regional randomization with one dominant region).
- Is host-level ever fine? Yes when the market is large and the treated share is small, so each host barely affects the others, or when the question is about the host's own outcome.

**Common mistakes:** Reporting the host gap as the platform effect. Adding hosts instead of changing the unit. Ignoring that cities are the real sample size. Skipping pre-period adjustment. Forgetting guest-side outcomes.

### Q40 ⭐⭐ 🔴 Treatment raises sessions per user by 10% relative to control and lowers revenue per session by 4% relative to control, and the team reports 'revenue per session is down, so the test failed'. Revenue per user is therefore up about 5.6% relative to control (1.10 x 0.96 = 1.056). Explain which metric should drive the decision, why the ratio misleads here and what else you check.
**Asked at:** Ratio-metric, delta-method and variance-reduction material (Spotify Confidence ratio-metric RFP and variance-reduction docs, MetricGate CUPED and delta-method pages, a TechPrep '66 Variance Reduction Interview Questions' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Revenue per session fell only because sessions per user rose, so I decide on revenue per user (the product of the two), and I check that the extra sessions are real value and not low-quality traffic.

**Clarifying questions:**
- Why do sessions rise: notifications, a redesign that splits one visit into two, or real extra use? Why: split visits inflate sessions without adding value.
- Is the 5.6% revenue per user an interval or a point, and is it significant? Why: the arithmetic is only as good as its error bars.
- What was the agreed primary metric before the test? Why: switching metric after seeing the result is a bias.
- What costs go with extra sessions (support, servers, refunds)? Why: revenue is not margin.
- Does retention or return-rate change in the following weeks? Why: more sessions today may mean fewer later.

**Approach:**
1. Check the arithmetic: 1.10 x 0.96 = 1.056, so revenue per user is up 5.6%. This works as an identity when "revenue per session" is total revenue divided by total sessions (ratio of sums) and "per user" is the average over users.
2. Name the issue: revenue per session is a ratio whose denominator moves with treatment. If treatment adds sessions that are worth less than the average one, the ratio falls even when total revenue rises. Here the extra sessions bring about 1.11 per session against 2.01 for the average (in my code).
3. Pick the decision metric: revenue per user, the unit that was randomized, with the interval (about +3.5% to +7.2% in my run). Revenue per session becomes a diagnostic.
4. Analyse properly: ratio metrics with the delta method, or user-level totals. Do not treat sessions as independent rows.
5. Check quality of the extra sessions: are they bounces, accidental, double sessions after a redesign? Look at session length, conversion per session, and the share of sessions with revenue.
6. Check guardrails and the future: refund rate, cost to serve, 7-day and 28-day return rate, and revenue per user in later weeks.
7. Decide: if revenue per user is up with a clear interval, guardrails hold and the extra sessions are not artefacts, call the test a success and explain the metric move.

**Metrics:**
- Primary: revenue per user = total revenue / users in arm, mean difference with 95% interval.
- Decomposition: sessions per user = sessions / users; revenue per session = total revenue / total sessions (ratio of sums). Relative effects multiply: (1+a)(1+b) - 1.
- Guardrails: refund rate, cost per user, return rate in later weeks, session length distribution.

**Risks:**
- Mean of per-user ratios is a different quantity from the ratio of sums (-4.6% versus -3.9% in my run); say which one you report.
- Revenue is heavy-tailed; a few big spenders can swing the user-level mean.
- More sessions can come from a worse experience (users come back because the first visit failed).
- A ratio's denominator is itself an outcome, so conditioning on sessions (analysing only users with sessions) is biased.

**What the interviewer scores:**
- Strong: multiplies the effects, picks the randomization unit's metric, and explains the denominator effect.
- Strong: checks whether the extra sessions are valuable, and what happens later.
- Strong: mentions the delta method for the ratio's interval.
- Weak: "revenue per session is down, the test failed."
- Weak: "revenue per user is up so everything is fine" with no guardrail check.

**Example:** (illustrative numbers) 100,000 users per arm. Control: 5.0 sessions and 2.00 revenue per session, so 10 per user. Treatment: +10% sessions, -4% per session, about 10.56 per user. The code gives sessions per user +9.7%, revenue per session -3.9%, revenue per user +5.4% with an interval of +3.5% to +7.2%, and the extra sessions bring about 1.11 each. Weak answer: "per-session revenue fell, it failed." Strong answer: "the rate fell because the denominator grew; per user, which is what we randomized, it is up and I would check the extra sessions are real."

**Code:**
```python
# Q40: sessions/user +10%, revenue/session -4%, revenue/user +5.6%. Illustrative, seeded.
import numpy as np

print("1.10 x 0.96 =", round(1.10 * 0.96, 3))
assert round(1.10 * 0.96, 3) == 1.056

rng = np.random.default_rng(40)
U = 100_000
def arm(mean_sessions, rev_per_session):
    # users differ in activity (gamma), sessions ~ Poisson; each session's revenue is zero-inflated and skewed
    act = rng.gamma(2.0, mean_sessions / 2.0, U)
    s = rng.poisson(act)
    rev = np.array([0.0] * U)
    tot = s.sum()
    per = np.where(rng.random(tot) < 0.1, rng.exponential(rev_per_session * 10, tot), 0.0)
    idx = np.repeat(np.arange(U), s)
    rev = np.bincount(idx, weights=per, minlength=U)
    return s, rev
sc, rc = arm(5.0, 2.00)
st, rt = arm(5.5, 1.92)

spu = st.mean() / sc.mean() - 1
rps = (rt.sum() / st.sum()) / (rc.sum() / sc.sum()) - 1
rpu = rt.mean() / rc.mean() - 1
print(f"sessions/user {spu:+.1%}   revenue/session (ratio of sums) {rps:+.1%}   revenue/user {rpu:+.1%}")
assert abs(spu - 0.10) < 0.02 and abs(rps + 0.04) < 0.03
# identity: revenue/user = sessions/user x revenue/session when the ratio is a ratio of sums
assert abs((1 + rpu) - (1 + spu) * (1 + rps)) < 1e-9

# interval for revenue per user: difference in means, user is the unit
d = rt.mean() - rc.mean()
se = np.sqrt(rt.var(ddof=1) / U + rc.var(ddof=1) / U)
print(f"revenue/user diff {d:.3f}, 95% CI [{d-1.96*se:.3f}, {d+1.96*se:.3f}]  = [{(d-1.96*se)/rc.mean():+.1%}, {(d+1.96*se)/rc.mean():+.1%}] relative")
assert d - 1.96 * se > 0
# delta-method SE of the ratio-of-sums revenue/session vs naive per-session SE
def ratio_se(num, den):
    r = num.sum() / den.sum(); m = den.mean()
    z = (num - r * den) / m
    return r, np.sqrt(z.var(ddof=1) / len(num))
rr, se_delta = ratio_se(rc, sc)
# naive: treat sessions as independent draws: need per-session values
print(f"control revenue/session {rr:.3f}, delta-method SE {se_delta:.4f}")
# mean of per-user ratios is a different quantity
mask_c, mask_t = sc > 0, st > 0
mor_c = (rc[mask_c] / sc[mask_c]).mean(); mor_t = (rt[mask_t] / st[mask_t]).mean()
print(f"mean of per-user ratios: {mor_t/mor_c-1:+.1%} (a different number from the ratio of sums {rps:+.1%})")
# a mix-shift check: the extra sessions are lower value than the existing ones
extra_sessions = st.sum() - sc.sum(); extra_rev = rt.sum() - rc.sum()
print(f"extra sessions {extra_sessions:,.0f}, extra revenue {extra_rev:,.0f} -> {extra_rev/extra_sessions:.2f} per extra session vs {rc.sum()/sc.sum():.2f} existing average")
assert extra_rev > 0
```

**Output (my run):**
```text
1.10 x 0.96 = 1.056
sessions/user +9.7%   revenue/session (ratio of sums) -3.9%   revenue/user +5.4%
revenue/user diff 0.540, 95% CI [0.351, 0.728]  = [+3.5%, +7.2%] relative
control revenue/session 2.012, delta-method SE 0.0124
mean of per-user ratios: -4.6% (a different number from the ratio of sums -3.9%)
extra sessions 48,470, extra revenue 53,961 -> 1.11 per extra session vs 2.01 existing average
```
The simulated effects (about +9.7%, -3.9%, +5.4%) differ a little from the prompt's round figures because of sampling noise; the identity (1 + a)(1 + b) = 1 + c is exact for ratio of sums and is asserted in the code.

**Follow-ups:**
- When would revenue per session be the right metric? When the question is about monetization of an unchanged amount of traffic, for example ad load, and sessions do not move. See Book 1 Part 10 Q27 (ratio metrics) and Q8 in this part (CTR as clicks over impressions).
- What if the interval on revenue per user includes zero? Then I cannot claim a gain; I would look at power and run longer, not choose the favourable ratio.

**Common mistakes:** Judging on a ratio whose denominator is also moved by treatment. Computing the interval with sessions as independent. Mixing ratio of sums and mean of ratios. Declaring success without guardrails. Dropping users with zero sessions.

### Q41 ⭐⭐ 🔴 A product launched in one country, and 15 other countries are available as donors. With 8 pre-launch weeks the synthetic-control fit has an average error of 1.5% of weekly revenue, and the post-launch gap is +2.5% of weekly revenue. Explain how you judge whether +2.5% is real using placebo tests, and what could invalidate the donor pool.
**Asked at:** Causal-inference and when-you-cannot-randomize material (an Interview Query causal-inference guide on diff-in-diff and synthetic control, Codemia 'explain difference-in-differences' practice pages, NBER working paper 25532 on synthetic difference-in-differences); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** A +2.5% gap on a fit that is off by 1.5% in normal weeks is not convincing by itself; I would run the same method on every donor country as a fake launch, and with only 16 countries the best p-value I can ever get is 1/16 = 6.25%.

**Clarifying questions:**
- How many post-launch weeks, and did anything else change in that country (a price move, a holiday, a competitor)? Why: synthetic control assumes only the launch differs.
- What outcome and what scale: weekly revenue, and how noisy is it week to week? Why: it sets the size of a normal gap.
- Which of the 15 donors are similar (same region, same product maturity)? Why: a donor pool that is unlike the launch country gives a poor counterfactual.
- Could any donor be affected by the launch (shared users, shared supply, cross-border spillover)? Why: contaminated donors bias the gap.
- Is the launch country special (the first market, chosen because it looked promising)? Why: selection makes the pre-trend a poor guide.

**Approach:**
1. Frame the question: gap = launch country minus its synthetic version (a weighted mix of donors that tracks the launch country before launch). The weights are non-negative and sum to 1.
2. Put the gap in context: 1.5% is the average miss in the pre period, so +2.5% is only about 1.7 times a normal miss. That is thin.
3. Run placebo tests in space: pretend each donor was the launch country, build a synthetic version for it from the other countries, and compute its post-launch gap. If many placebos show gaps as large as +2.5%, the launch result is not special.
4. Use a ratio that adjusts for fit: post-launch RMSPE (root mean squared prediction error) divided by pre-launch RMSPE. Rank the launch country among the 16 countries.
5. Read the rank honestly: the placebo p-value is rank / 16. Even rank 1 gives 0.0625; so with 16 units I can say "most extreme of 16", not "p < 0.05".
6. Run placebos in time too (pretend the launch was 4 weeks earlier), check leave-one-out donor weights, and vary the pre period.
7. Look at the donor pool: remove donors with big weights one at a time and see if the gap holds.

**Metrics:**
- Gap = (actual - synthetic) / pre-launch mean of the launch country's revenue (+2.5% here), by week and averaged.
- Pre-RMSPE = square root of the mean of squared pre-launch gaps (the 1.5% fit error).
- Ratio = post-RMSPE / pre-RMSPE; placebo p-value = (number of units with ratio at least the launch country's) / 16.
- Guardrails: donor weights (no single donor above, say, 50%), pre-period length (8 weeks is short), stability of the gap across leave-one-out fits.

**Risks:**
- With 8 pre-weeks and 15 donors the weights can overfit noise (more donors than weeks), which makes the pre fit look good and the post gap a poor guide.
- A good pre-fit does not prove the donors keep tracking after launch.
- Spillover from the launch country into donors biases the gap in an unknown direction.
- A few-unit permutation test has low power: a true effect can fail to stand out.

**What the interviewer scores:**
- Strong: compares the gap with the pre-fit error and runs placebos on every donor.
- Strong: knows the smallest p-value (1/16) and says what the test can and cannot show.
- Strong: lists donor-pool failure modes (spillover, dissimilar donors, overfit weights).
- Weak: "the gap is positive, so the launch worked."
- Weak: quotes a p-value below 0.0625 from a 16-unit permutation test.

**Example:** (illustrative numbers) In the simulation, 16 countries, 8 pre weeks and 8 post weeks, a +2.5% effect added to the launch country, weekly noise chosen so the launch country's pre-fit error is 1.5%. The estimated post gap is +1.7%, the launch country's ratio ranks 14th of 16 (placebo p = 0.875), and the largest placebo gap is 7.3%. Over 80 simulated worlds, the launch country has the top ratio in 10% of worlds when the true effect is +2.5% and also in 10% when it is zero. So this design cannot tell a real +2.5% from nothing. Weak answer: "+2.5% is a positive lift, ship." Strong answer: "the gap is smaller than normal placebo gaps; I would not claim it, and I would add pre-weeks, donors or a regional split."

**Code:**
```python
# Q41: synthetic control, 1 treated + 15 donors, 8 pre weeks, placebo-in-space test. Illustrative, seeded.
import numpy as np
from scipy.optimize import minimize

U, PRE, POST = 16, 8, 8
print("smallest possible placebo p-value with 16 units: 1/16 =", round(1 / 16, 4))
assert round(1 / 16, 4) == 0.0625          # cannot reach 0.05 however large the gap

def synth_gap(Y, i, pre):
    """Fit non-negative weights summing to 1 on the other units, return gap series (unit i minus synthetic), in % of own level."""
    others = [j for j in range(Y.shape[0]) if j != i]
    X = Y[others][:, :pre].T; y = Y[i, :pre]
    k = len(others)
    f = lambda w: np.sum((X @ w - y) ** 2)
    res = minimize(f, np.full(k, 1 / k), method="SLSQP", bounds=[(0, 1)] * k,
                   constraints={"type": "eq", "fun": lambda w: w.sum() - 1}, options={"maxiter": 200})
    w = res.x
    return (Y[i] - w @ Y[others]) / Y[i, :pre].mean()

def one_world(rng, effect):
    t = np.arange(PRE + POST)
    common = 100 * (1 + 0.004 * t + 0.02 * np.sin(t / 2.0))
    load1 = rng.normal(0, 1, U); load2 = rng.normal(0, 1, U)
    f2 = np.cumsum(rng.normal(0, 0.6, PRE + POST))
    Y = common[None, :] * (1 + 0.04 * load1[:, None] * (t[None, :] - 4) / 8 + 0.01 * load2[:, None] * f2[None, :] / 2)
    Y = Y * (1 + rng.normal(0, 0.022, Y.shape))            # weekly noise
    Y[0, PRE:] *= (1 + effect)                                # unit 0 is the launch country
    return Y

def ratios(Y):
    out = []
    for i in range(U):
        g = synth_gap(Y, i, PRE)
        pre = np.sqrt(np.mean(g[:PRE] ** 2)); post = np.sqrt(np.mean(g[PRE:] ** 2))
        out.append((pre, post, post / pre, g[PRE:].mean()))
    return np.array(out)

rng = np.random.default_rng(41)
Y = one_world(rng, 0.025)
r = ratios(Y)
rank = int((r[:, 2] >= r[0, 2]).sum())
print(f"launch country: pre-RMSPE {r[0,0]*100:.2f}%  mean post gap {r[0,3]*100:+.2f}%  post/pre ratio {r[0,2]:.1f}")
print(f"placebo countries: median pre-RMSPE {np.median(r[1:,0])*100:.2f}%, largest |mean post gap| {np.abs(r[1:,3]).max()*100:.2f}%")
print(f"rank of the launch ratio among 16: {rank}  -> placebo p = {rank}/16 = {rank/16:.3f}")
assert rank / 16 >= 0.0625

# how often would a real +2.5% effect even rank first, and how often does a zero effect rank first? (80 worlds each)
for eff in (0.025, 0.0):
    firsts = 0; sims = 80; gaps = []
    for s in range(sims):
        rr = ratios(one_world(np.random.default_rng(1000 + s), eff))
        firsts += int(rr[0, 2] >= rr[1:, 2].max()); gaps.append(rr[0, 3])
    print(f"true effect {eff:+.1%}: launch country has the top ratio in {firsts}/{sims} worlds ({firsts/sims:.0%}); mean estimated gap {np.mean(gaps)*100:+.2f}%")
    if eff == 0.0:
        assert firsts / sims < 0.2             # near 1/16 = 6%
```

**Output (my run):**
```text
smallest possible placebo p-value with 16 units: 1/16 = 0.0625
launch country: pre-RMSPE 1.51%  mean post gap +1.67%  post/pre ratio 1.7
placebo countries: median pre-RMSPE 1.55%, largest |mean post gap| 7.33%
rank of the launch ratio among 16: 14  -> placebo p = 14/16 = 0.875
true effect +2.5%: launch country has the top ratio in 8/80 worlds (10%); mean estimated gap +2.69%
true effect +0.0%: launch country has the top ratio in 8/80 worlds (10%); mean estimated gap +0.14%
```
The data-generating process (factor loadings, noise level) is invented and was tuned only so the pre-fit error is near 1.5%. The low power is a property of this simulated world; real data could be easier or harder. With 80 worlds, the 10% figures are noisy (about plus or minus 3 points).

**Follow-ups:**
- How could you get more power? More pre-weeks, more donors (regions inside countries), a longer post period, or a design like difference-in-differences with several launch markets. See Book 1 Part 10 Q49 (synthetic control) and Q28 (difference-in-differences) for the method.
- Is the placebo p-value a real p-value? It is a permutation-style rank test; it is valid if the launch country is exchangeable with the donors, which is a strong assumption.

**Common mistakes:** Reporting a gap without a pre-fit error. Skipping the placebo runs. Claiming p < 0.05 from 16 units. Letting one donor carry the weights. Forgetting spillover to donors and other launches at the same time.

### Q42 ⭐⭐ 🔴 A teammate uses sessions during the first 3 days of the experiment as the CUPED covariate because it correlates 0.9 with the outcome (28-day sessions), and the adjusted confidence interval is much tighter. Treatment changes early sessions. Explain what is wrong, which direction the bias goes and what a valid covariate would be.
**Asked at:** Ratio-metric, delta-method and variance-reduction material (Spotify Confidence ratio-metric RFP and variance-reduction docs, MetricGate CUPED and delta-method pages, a TechPrep '66 Variance Reduction Interview Questions' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The covariate is measured after treatment started and treatment changes it, so CUPED subtracts part of the real effect, pulls the estimate toward zero here, and makes the wrong answer look more certain; use pre-experiment data.

**Clarifying questions:**
- Is the 3-day window counted from each user's first exposure, and is exposure the same time as assignment? Why: even "early" data after exposure is affected by treatment.
- What is the outcome: 28-day sessions per user? Why: it fixes which pre-period metric is the matching covariate.
- Do all users have pre-experiment history? Why: new users have no pre-period data; they need a separate rule (the mean).
- Does the treatment effect on early sessions go the same way as on 28-day sessions? Why: it decides the direction of the bias.
- Is the adjusted analysis the pre-registered one? Why: picking the analysis that gives the tighter interval after seeing data is another bias.

**Approach:**
1. Recall the rule: CUPED adjusts the outcome with a covariate that is fixed before treatment, so it is independent of assignment. The adjusted outcome is Y - theta x (X - mean of X), with theta = cov(Y, X) / var(X).
2. Show why the teammate's covariate breaks it. Early sessions X are caused partly by treatment. The adjustment subtracts theta x (the treatment effect on X) from the effect on Y. With a high correlation, theta is near 1, so the adjusted effect is roughly the effect on Y minus the effect on early sessions.
3. Direction: here treatment raises both early and 28-day sessions, so the estimate is pulled toward zero (an understated effect). If treatment lowered early sessions but raised long-run ones, the effect would be overstated. In general the sign is (effect on Y) minus theta x (effect on X).
4. Why the interval looks better: the correlation of 0.9 shrinks the variance by 1 - 0.9^2 = 0.19, so the standard error is about 44% of the original. A narrow interval around a biased number means the confidence interval misses the truth most of the time.
5. Fix: use the same metric in the 28 days before the experiment (or 1 to 4 weeks, tested for correlation) as the covariate, and fix the choice before launch.
6. Check: compare the adjusted and unadjusted estimates; they should agree up to noise. A big gap between them is a red flag. Also test that the covariate is balanced across arms (it should be, for a pre-experiment covariate).

**Metrics:**
- Primary: 28-day sessions per user, with the CUPED-adjusted difference and its interval.
- Variance reduction = 1 - (SE adjusted / SE unadjusted)^2, about rho^2 for one covariate.
- Check: adjusted minus unadjusted point estimate, and covariate balance between arms.
- Guardrail: coverage in an A/A test (should be about 95%).

**Risks:**
- Post-treatment covariates (anything measured after assignment that treatment can move) break CUPED, and so does any covariate that is a proxy for the outcome.
- Early-days data can include novelty, so the early effect and the 28-day effect can differ in sign.
- Too many covariates can overfit with small samples.
- Dropping users without history changes the population.

**What the interviewer scores:**
- Strong: names the rule (covariate fixed before assignment) and explains why 0.9 correlation is not enough.
- Strong: gives the direction with reasoning (effect on Y minus theta x effect on X) and the fix.
- Strong: notes the tight interval is what makes it dangerous.
- Weak: "a higher correlation is always better."
- Weak: says the estimate stays unbiased because randomization protects it.

**Example:** (illustrative numbers) 50,000 users per arm in the code. True effect on 28-day sessions +2.0. Treatment also raises 3-day sessions by 1.5. Unadjusted estimate 1.99 (SE 0.19, interval covers the truth in 95% of runs). CUPED with early sessions: 0.62 (SE 0.07), and the interval covers the truth in 0% of runs. CUPED with pre-experiment sessions: 2.00 (SE 0.07), coverage 94%. Weak answer: "correlation 0.9 gives the biggest variance reduction." Strong answer: "that covariate is post-treatment; I would use the 28 days before launch and compare with the unadjusted number."

**Code:**
```python
# Q42: CUPED with a post-treatment covariate (first 3 days of the experiment). Illustrative, seeded.
import numpy as np

rho = 0.9
print("variance kept with covariate correlation 0.9:", round(1 - rho**2, 2), " -> SE shrinks to", round(np.sqrt(1 - rho**2), 2), "of its size")
assert round(1 - rho**2, 2) == 0.19 and round(np.sqrt(1 - rho**2), 2) == 0.44

rng = np.random.default_rng(42)
n = 50_000
TAU_Y, TAU_X = 2.0, 1.5     # true effect on 28-day sessions; treatment also raises early (3-day) sessions by 1.5

def sim(n, reps):
    out = {"naive": [], "bad": [], "good": []}
    se = {"naive": [], "bad": [], "good": []}
    for _ in range(reps):
        T = rng.integers(0, 2, n)
        L = rng.normal(100, 20, n)                           # latent engagement
        pre = L + rng.normal(0, 6, n)                        # sessions in the 28 days BEFORE the test
        early = L + rng.normal(0, 6, n) + TAU_X * T          # sessions in the first 3 days (post-treatment)
        Y = L + rng.normal(0, 6, n) + TAU_Y * T              # 28-day sessions
        for name, x in (("naive", None), ("bad", early), ("good", pre)):
            if x is None:
                a, b = Y[T == 1], Y[T == 0]
                est = a.mean() - b.mean(); s = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
            else:
                th = np.cov(Y, x)[0, 1] / x.var(ddof=1)      # pooled theta, the standard CUPED recipe
                Z = Y - th * (x - x.mean())
                a, b = Z[T == 1], Z[T == 0]
                est = a.mean() - b.mean(); s = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
            out[name].append(est); se[name].append(s)
    return {k: (np.mean(v), np.mean(se[k]), np.mean([abs(e - TAU_Y) < 1.96 * s for e, s in zip(v, se[k])])) for k, v in out.items()}

res = sim(n, 100)
Tt = rng.integers(0, 2, n); L = rng.normal(100, 20, n)
print("corr(early, 28-day) in the simulation ~",
      round(np.corrcoef(L + rng.normal(0, 6, n), L + rng.normal(0, 6, n))[0, 1], 2))
print(f"true effect on 28-day sessions: {TAU_Y}")
for k, (m, s, cov) in res.items():
    print(f"{k:6s} mean estimate {m:5.2f}   mean SE {s:.3f}   95% CI covers the truth in {cov:.0%} of runs")
assert abs(res["naive"][0] - TAU_Y) < 0.1 and abs(res["good"][0] - TAU_Y) < 0.1
assert res["bad"][0] < TAU_Y - 0.8                           # biased toward zero
assert res["bad"][1] < res["naive"][1] and res["good"][1] < res["naive"][1]
assert res["bad"][2] < 0.5 and res["naive"][2] > 0.9
```

**Output (my run):**
```text
variance kept with covariate correlation 0.9: 0.19  -> SE shrinks to 0.44 of its size
corr(early, 28-day) in the simulation ~ 0.92
true effect on 28-day sessions: 2.0
naive  mean estimate  1.99   mean SE 0.187   95% CI covers the truth in 95% of runs
bad    mean estimate  0.62   mean SE 0.074   95% CI covers the truth in 0% of runs
good   mean estimate  2.00   mean SE 0.074   95% CI covers the truth in 94% of runs
```
The latent-engagement model and noise sizes are invented. The bias formula (effect on Y minus theta times effect on X, with theta close to 0.9 in this setup) is what the output confirms: 2.0 - about 0.9 x 1.5 is about 0.65, and the run gives 0.62.

**Follow-ups:**
- Can I use first-3-days data at all? As a segmentation or novelty diagnostic, yes; as a CUPED covariate, no. See Q9 in this part (CUPED with pre-experiment spend).
- What if the pre-period is short for new users? Use pre-period data where it exists, and for users without it use a constant (the mean) with an indicator, so they get no adjustment.

**Common mistakes:** Choosing the covariate by correlation alone. Using data from after assignment. Not comparing adjusted and unadjusted estimates. Trusting a narrower interval as proof the method worked. Not A/A testing the pipeline.

### Q43 ⭐⭐ 🔴 In an experiment with 50,000 users per arm the overall split is exactly 50/50, so the SRM check passes. By platform, control has 20,000 iOS and 30,000 Android users while treatment has 16,000 iOS and 34,000 Android users. Explain what this means, why the overall check missed it, and what you do with the result.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The overall split is exactly 50/50, but the platform mix is 40% iOS in control and 32% in treatment, which is a very large sample-ratio mismatch inside platforms, so the experiment is broken and I would not read any result until I find the cause.

**Clarifying questions:**
- Was assignment designed to be 50/50 within each platform, or only overall? Why: it decides what the expected counts are in each cell.
- Where does a user get counted: at assignment, or at the first event after exposure? Why: counting on the first event lets a platform-specific crash or logging gap remove users from one arm.
- Did the treatment ship in a different app version, or a different build for iOS? Why: a version split is a common cause.
- Any exclusion rules (bots, eligibility filters) applied after assignment? Why: a filter that treats the arms or platforms differently creates the imbalance.

**Approach:**
1. Compute the check per platform, not just overall. iOS: 20,000 versus 16,000 has an expected 18,000 in each arm, chi-square = 444. Android: 30,000 versus 34,000, expected 32,000, chi-square = 250. Overall: 50,000 versus 50,000, chi-square = 0.
2. Explain why the overall test passed. The iOS shortfall in treatment (4,000) is exactly offset by an Android surplus (4,000), so the totals match. The SRM check on the total only sees the total. A check on a mix (platform by arm) sees the problem: chi-square about 694.
3. Treat the equality of totals as a coincidence or a symptom, not as comfort. Possible causes: iOS users in treatment are being dropped (crash, slow load, a missing event), or are being reassigned or shown on another platform, or an eligibility filter works differently by arm.
4. Quantify what it does: if iOS converts at 8% and Android at 4% in both arms and treatment does nothing, pooled conversion is 5.60% versus 5.28%, a fake drop of 0.32 points (5.7% relative), with z of about -2.2 at 50,000 per arm (it would grow with sample size). The mix shift alone makes the test look like a loser.
5. Investigate: trace the funnel per platform (assignment, exposure, first event), compare app versions, look at crash and error logs, check the assignment service by platform, and look for a bucketing change.
6. Decide: do not ship on this data. If the cause is a logging or exposure bug, fix and rerun. A within-platform comparison can be shown as a diagnostic, but it is only valid if the missing users are missing at random, which I cannot assume.

**Metrics:**
- SRM per cell = (observed - expected)^2 / expected, summed over arms, with p-value from chi-square (1 degree of freedom per two-arm cell). Use a strict threshold (for example p < 0.001) because it is a check run on many tests and many segments.
- Platform share per arm = users on the platform / users in the arm (40% versus 32% for iOS).
- Guardrails: assignment-to-exposure rate per platform and arm; crash rate; app version mix per arm.

**Risks:**
- Reweighting to the control mix hides the problem and only fixes the part you can see.
- The missing iOS users in treatment are likely not a random sample (the ones who crash or leave early), so even within iOS the arms are not comparable.
- Running SRM checks on many segments produces false alarms; use a strict threshold and look at the size of the gap, not only the p-value.
- Totals that match can create false confidence in dashboards that only check the total.

**What the interviewer scores:**
- Strong: runs the check by segment and explains why the total hid it (offsetting gaps).
- Strong: shows what the mix shift does to the metric with numbers.
- Strong: refuses to ship, finds the cause, reruns if needed.
- Weak: "SRM passed, so the test is valid."
- Weak: reweights and reports the result as if fixed.

**Example:** (illustrative numbers, from the prompt) iOS 20,000 versus 16,000: chi-square 444. Android 30,000 versus 34,000: chi-square 250. Total 50,000 versus 50,000: chi-square 0. With conversion 8% iOS and 4% Android in both arms, control pools to 5.60% and treatment to 5.28%. Weak answer: "overall split is exactly 50/50 so there is no SRM." Strong answer: "the platform mix differs by 8 points; that is a broken assignment or logging path, and the pooled result is not trustworthy."

**Code:**
```python
# Q43: overall 50/50 passes SRM but iOS and Android are lopsided. Illustrative, seeded.
import numpy as np
from scipy import stats

ctl = {"iOS": 20_000, "Android": 30_000}
trt = {"iOS": 16_000, "Android": 34_000}
nc, nt = sum(ctl.values()), sum(trt.values())
print("users per arm: control", nc, " treatment", nt)
assert nc == 50_000 and nt == 50_000

def srm(c, t):
    exp = (c + t) / 2
    chi = (c - exp) ** 2 / exp + (t - exp) ** 2 / exp
    return chi, stats.chi2.sf(chi, 1)

print("overall: chi2 = %.1f p = %.3f" % srm(nc, nt))
for p in ctl:
    chi, pv = srm(ctl[p], trt[p])
    print(f"{p}: {ctl[p]} vs {trt[p]}  chi2 = {chi:.1f}  p = {pv:.2e}")
assert srm(nc, nt)[0] == 0
assert round(srm(20_000, 16_000)[0], 1) == 444.4 and round(srm(30_000, 34_000)[0], 1) == 250.0

# the real question: is platform mix the same in the two arms?
table = np.array([[20_000, 30_000], [16_000, 34_000]])
chi, p, dof, _ = stats.chi2_contingency(table, correction=False)
print(f"platform x arm independence: chi2 = {chi:.1f}, dof {dof}, p = {p:.1e}; iOS share control {20/50:.0%} vs treatment {16/50:.0%}")
assert round(chi, 1) == 694.4

# what it does to the pooled metric even if treatment does nothing: iOS converts 8%, Android 4% in BOTH arms
rate = {"iOS": 0.08, "Android": 0.04}
pc = sum(ctl[k] * rate[k] for k in ctl) / nc
pt = sum(trt[k] * rate[k] for k in trt) / nt
print(f"true effect 0, pooled conversion control {pc:.2%} vs treatment {pt:.2%}: fake change {pt-pc:+.2%} points ({pt/pc-1:+.1%} relative)")
assert round(pc, 4) == 0.056 and round(pt, 4) == 0.0528
se = np.sqrt(pc*(1-pc)/nc + pt*(1-pt)/nt)
print(f"z for that fake change = {(pt-pc)/se:.1f}")
assert 2.0 < abs((pt - pc) / se) < 2.5
# a platform-adjusted comparison (stratified) removes the compositional part
```

**Output (my run):**
```text
users per arm: control 50000  treatment 50000
overall: chi2 = 0.0 p = 1.000
iOS: 20000 vs 16000  chi2 = 444.4  p = 1.17e-98
Android: 30000 vs 34000  chi2 = 250.0  p = 2.60e-56
platform x arm independence: chi2 = 694.4, dof 1, p = 4.8e-153; iOS share control 40% vs treatment 32%
true effect 0, pooled conversion control 5.60% vs treatment 5.28%: fake change -0.32% points (-5.7% relative)
z for that fake change = -2.2
```
The conversion rates are invented. The SRM numbers come straight from the prompt's counts.

**Follow-ups:**
- Could this be allowed if the product behaves differently by platform? No: assignment happens before the product shows anything, so the arms should have the same platform mix. If only exposed users are counted, a platform-specific exposure change can cause it, and then the metric must be reported with the exposure rule. See Q1 in this part (an SRM on 52,000 versus 48,000) and Book 1 Part 10 Q6 (what SRM is).
- How many segments should I check? The ones that could differ by arm (platform, country, app version, new versus returning), with a strict threshold.

**Common mistakes:** Checking SRM on the total only. Reweighting instead of finding the cause. Treating a tiny p-value as the only information. Ignoring the sign and size of the imbalance. Shipping while the cause is unknown.

### Q44 ⭐ 🟡 A team ran 8 variants of a landing page against one control, picked the best (+4% conversion relative to control, p = 0.02) and shipped it, and a follow-up re-test of that variant alone shows +1.5% relative. Explain the winner's curse, how to estimate the true effect of the chosen variant and how you would design such tests.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
**Say this first (1 line):** Picking the best of 8 noisy results selects the lucky one, so +4% overstates the true effect, and a fresh re-test of +1.5% is the honest number; I would shrink the estimate, confirm on new data, and use a multiple-comparison method next time.

**Clarifying questions:**
- Was p = 0.02 corrected for 8 variants, or is it the raw p-value for the winner against control? Why: raw means it is nearly worthless as evidence after selection.
- Was the choice of variants and metric fixed before the test? Why: post-hoc picking adds more selection.
- How large was the re-test and how long? Why: its interval tells me whether +1.5% differs from +4% or from zero.
- Was the re-test on a similar period and audience? Why: seasonal or novelty differences also move the estimate.
- What is the cost of a wrong ship here (a page the team must maintain, a brand change)? Why: it sets how much evidence I need.

**Approach:**
1. Explain the winner's curse. Each estimate is true effect plus noise. The largest of 8 estimates tends to carry a big positive noise term, so the selected variant's estimate is biased upward. The more variants and the noisier each one, the larger the bias.
2. Do the arithmetic on the evidence. +4% at p = 0.02 means a standard error of about 1.7% (z = 2.33). The p-value for the best of 8 should be adjusted: 8 x 0.02 = 0.16 (Bonferroni), and with 8 true nulls the chance of at least one p below 0.05 is 1 - 0.95^8 = 34%. So "p = 0.02" does not clear the bar.
3. Read the re-test. +1.5% with the same standard error has an interval from about -1.9% to +4.9%, and the difference from +4% is about 1.0 standard errors. The two results are consistent with a modest true effect and luck in the first.
4. Estimate the true effect of the chosen variant: use the fresh re-test (unbiased because the variant was chosen before it), or shrink the first-round estimates toward the average of all 8 (empirical Bayes) and combine with the re-test.
5. Decide on the new estimate and its interval: is +1.5% (interval -1.9% to +4.9%) enough for the cost? Probably continue the re-test or collect more data.
6. Design next time: fewer, better variants; a multiple-comparison correction against a shared control (Dunnett or Holm); split the data (choose the winner on part of the traffic, confirm on the rest); pre-registered primary metric; and report shrunk estimates for all variants.

**Metrics:**
- Per variant: relative lift = (conversion variant / conversion control) - 1, with its interval.
- Family-wise error rate = probability of at least one false win across the 8 comparisons (34% unadjusted at 0.05, about 5% with Bonferroni at 0.05/8).
- Winner's-curse bias = mean (estimate of the selected variant - its true effect); in my simulation about +1.8 points.
- Guardrails: confirm on a fresh sample; track the live lift after launch.

**Risks:**
- Shipping on the selected estimate and planning revenue around +4%.
- Shrinkage needs a prior; with only 8 variants the estimated spread is itself noisy.
- A re-test run right after the first one can have its own novelty or seasonality.
- Correcting for 8 comparisons costs power: some true winners are missed.

**What the interviewer scores:**
- Strong: explains selection bias in plain words and shows the p-value is not valid after picking the max.
- Strong: gives a way to estimate the true effect (fresh re-test, shrinkage) with numbers.
- Strong: proposes a design change (correction, split-sample confirm, fewer variants).
- Weak: "the re-test is just noise, the first test was bigger."
- Weak: "regression to the mean" with no mechanism or fix.

**Example:** (illustrative numbers) 5% baseline conversion, about 128,000 users per arm gives a standard error of 1.7% on the relative lift. Simulation: true effects spread as N(0, 1.5%) across 8 variants. The selected winner's average estimate is +3.3% but its average true effect is +1.4%, an overstatement of +1.8 points; among winners whose estimate is near +4%, the mean true effect is +1.8%. Shrinking toward the group mean removes the bias (average error -0.1 points) and reduces the root mean squared error from 2.3% to 1.5%. A fresh test of the chosen variant is unbiased (+1.4%). Weak answer: "+4% with p = 0.02, ship and plan for 4%." Strong answer: "plan for about 1.5%, and confirm on fresh traffic."

**Code:**
```python
# Q44: 8 variants vs control, best looks +4% (p = 0.02), re-test says +1.5%. Illustrative, seeded.
import numpy as np
from scipy import stats

base = 0.05
z = stats.norm.isf(0.02 / 2)
se_rel = 0.04 / z                                  # SE of the relative lift implied by +4% at p = 0.02
n_arm = 2 * base * (1 - base) / (se_rel * base) ** 2
print(f"+4% at p = 0.02 implies z = {z:.2f}, SE of relative lift {se_rel:.2%}, about {n_arm:,.0f} users per arm")
assert abs(z - 2.326) < 0.01 and 120_000 < n_arm < 135_000
print(f"Bonferroni p for 8 variants: {min(1, 0.02*8):.2f};  chance of >= 1 p<0.05 among 8 true nulls: {1-0.95**8:.1%}")
assert round(0.02 * 8, 2) == 0.16 and round(1 - 0.95 ** 8, 3) == 0.337
# does the re-test contradict the first estimate?
dz = (0.04 - 0.015) / np.sqrt(2) / se_rel
print(f"re-test +1.5% with the same SE: z for the difference {dz:.2f}; the re-test 95% CI is [{(0.015-1.96*se_rel):+.1%}, {(0.015+1.96*se_rel):+.1%}]")
assert dz < 1.5

rng = np.random.default_rng(44)
R, K, TAU = 20_000, 8, 0.015                        # true relative effects ~ N(0, 1.5%)
true = rng.normal(0, TAU, (R, K))
est = true + rng.normal(0, se_rel, (R, K))
best = est.argmax(1); idx = np.arange(R)
w_est, w_true = est[idx, best], true[idx, best]
print(f"winner: mean estimate {w_est.mean():+.2%}, mean true effect {w_true.mean():+.2%}, overstatement {w_est.mean()-w_true.mean():+.2%}")
assert w_est.mean() > w_true.mean() + 0.01
# winners that look like ours
sel = (w_est > 0.035) & (w_est < 0.045)
print(f"winners with estimate near +4%: {sel.sum()}; their mean true effect {w_true[sel].mean():+.2%}")
assert 0.0 < w_true[sel].mean() < 0.025
# empirical-Bayes shrinkage: prior variance from the 8 estimates in each experiment
shr_err, raw_err = [], []
for r in range(R):
    e = est[r]; v = max(e.var(ddof=1) - se_rel ** 2, 1e-8)
    b = v / (v + se_rel ** 2)
    post = e.mean() + b * (e - e.mean())
    shr_err.append(post[best[r]] - true[r, best[r]]); raw_err.append(e[best[r]] - true[r, best[r]])
print(f"mean error of winner: raw {np.mean(raw_err):+.2%}, shrunk {np.mean(shr_err):+.2%};  RMSE raw {np.sqrt(np.mean(np.square(raw_err))):.2%} vs shrunk {np.sqrt(np.mean(np.square(shr_err))):.2%}")
assert abs(np.mean(shr_err)) < abs(np.mean(raw_err)) / 2
# share of experiments in which the winner's re-test is >= 0 and its fresh estimate vs truth
fresh = true[idx, best] + rng.normal(0, se_rel, R)
print(f"fresh re-test of the winner: mean {fresh.mean():+.2%} (unbiased for its true effect {w_true.mean():+.2%})")
assert abs(fresh.mean() - w_true.mean()) < 0.001
```

**Output (my run):**
```text
+4% at p = 0.02 implies z = 2.33, SE of relative lift 1.72%, about 128,532 users per arm
Bonferroni p for 8 variants: 0.16;  chance of >= 1 p<0.05 among 8 true nulls: 33.7%
re-test +1.5% with the same SE: z for the difference 1.03; the re-test 95% CI is [-1.9%, +4.9%]
winner: mean estimate +3.26%, mean true effect +1.42%, overstatement +1.84%
winners with estimate near +4%: 4504; their mean true effect +1.75%
mean error of winner: raw +1.84%, shrunk -0.08%;  RMSE raw 2.30% vs shrunk 1.48%
fresh re-test of the winner: mean +1.41% (unbiased for its true effect +1.42%)
```
The spread of true effects (1.5%) is invented; with a wider or narrower spread the overstatement changes. The empirical-Bayes step uses only the 8 estimates in each simulated test, as a team would have.

**Follow-ups:**
- Why is the re-test unbiased? The variant was chosen before the re-test data existed, so the noise in the new data is independent of the choice. See Q23 in this part (one control with 4 variants) and Book 1 Part 10 Q9 (multiple testing).
- Does this apply to dashboards with many metrics? Yes, picking the one metric that moved has the same selection bias.

**Common mistakes:** Treating the selected variant's p-value as if it were the only test. Planning on the first estimate. Using more variants to "find a winner". Not confirming on fresh data. Calling the gap between +4% and +1.5% a real decline in effect.

### Q45 ⭐ 🟡 Two experiments run at once on the same users, one changing the recommendation carousel and one changing the carousel's layout, each randomized 50/50 independently, so 25% of users receive both treatments. Each is analysed alone and the combined group looks worse than either. Explain interaction effects, how to detect them and how platforms avoid them.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
**Say this first (1 line):** Each test alone is not wrong, it is answering a different question. The effect of A depends on whether B is on, so I read the four cells, test the A x B interaction, and then fix it with layers or by not running the two at once.

**Clarifying questions:**
- Do the two changes touch the same surface (carousel contents and carousel layout do)? If yes, I expect an interaction before I look at data.
- Is the "combined looks worse" number the 25% cell, with a decent sample? A small cell is noise until proven otherwise.
- Do both experiments use independent hashing, or one shared salt? A shared salt breaks the 25% cells (see the hash-salt question later in this part, Q54).
- Is the primary metric the same in both tests? If it is, the two readouts are fighting over the same number.
- Can one test wait? If yes, the cheapest fix is sequencing, not statistics.

**Approach:**
1. Say what interaction means: the effect of A is different when B is on. Effects are not additive.
2. Look at the four cells: neither, A only, B only, both. Each is about 25% of users, so the cells are big and cheap to compare.
3. Test it. Fit `y ~ A + B + A:B`. The A:B coefficient is the interaction. It is `both - A only - B only + neither`.
4. Note what each single-experiment readout actually is. "A alone" averages over B being on half the time, so it reads `a + 0.5 x interaction`. It is a blend, not the pure effect.
5. Decide. If the interaction is large and negative, do not ship both. Pick the best cell. Ship it, then re-test the other change on top of it.
6. Prevent it. Use layers (mutually exclusive buckets for experiments that touch the same surface) and keep orthogonal hashing for experiments that do not. Book 1 Part 10 Q48 (interaction effects between concurrent experiments) covers the platform theory.

**Metrics:**
- Cell mean = metric total in the cell / users in the cell.
- Interaction = mean(both) - mean(A only) - mean(B only) + mean(neither).
- Standard error of the interaction is twice the standard error of a marginal main effect with equal cells (computed below), so it needs about four times the users.
- Guardrails: the same guardrails as each experiment, read per cell. A guardrail can break only in the both-on cell.

**Risks:**
- Low power for the interaction. Absence of a significant interaction is not proof of none (power in the code: about 42% for a small interaction).
- Looking at many interactions across many experiments is a multiple-testing problem. Test the pairs that touch the same surface.
- Mutual exclusion splits traffic, so each test runs on half the users and takes longer.
- Shipping A and B together because "both won alone" is the real damage.

**What the interviewer scores:**
- Strong: states the interaction as a difference of differences, and says why the single readouts mislead.
- Strong: gives a platform fix (layers, exclusion, pre-launch overlap check) and names the cost, which is traffic.
- Weak: "run them one after the other" with nothing about detection.
- Weak: calls the combined cell worse and stops, with no test and no decision.

**Example:** Illustrative mean minutes per user: neither 100, A only 103, B only 103, both 98. Interaction = 98 - 103 - 103 + 100 = -8. "A alone" reads (103 + 98)/2 - (100 + 103)/2 = -1.0. So each test alone shows about -1 minute, although each one helps by +3 when the other is off.
- Weak answer: "Both lose, kill both." Strong answer: "The cells say each helps alone and clashes together, so I ship the better single one and re-test the second on top of it."

**Code:**
```python
# Q45: two overlapping experiments with an interaction (illustrative simulation)
import numpy as np
from scipy import stats
rng = np.random.default_rng(45)
N = 400_000
a = rng.random(N) < 0.5            # experiment A: carousel algorithm
b = rng.random(N) < 0.5            # experiment B: carousel layout (independent hash)
print("share in each cell (A,B):", {k: round(float(np.mean((a == k[0]) & (b == k[1]))), 3) for k in [(0,0),(1,0),(0,1),(1,1)]})
assert abs(np.mean(a & b) - 0.25) < 0.005
# illustrative mean minutes per user: each change alone helps, together they clash
base, ea, eb, inter = 100.0, 3.0, 3.0, -8.0
mu = base + ea * a + eb * b + inter * (a & b)
y = mu + rng.normal(0, 40, N)
cell = {k: y[(a == k[0]) & (b == k[1])] for k in [(0,0),(1,0),(0,1),(1,1)]}
for k, v in cell.items(): print("cell", k, "mean", round(float(v.mean()), 2), "n", len(v))
assert cell[(1,1)].mean() < cell[(1,0)].mean() and cell[(1,1)].mean() < cell[(0,1)].mean()
# each experiment analysed alone (ignores the other, averages over it)
for name, g in [("A alone", a), ("B alone", b)]:
    d = y[g].mean() - y[~g].mean(); se = np.sqrt(y[g].var()/g.sum() + y[~g].var()/(~g).sum())
    print(name, "estimate", round(float(d), 2), "+/-", round(1.96*se, 2))
    assert abs(d - (ea + inter/2)) < 1.0          # a + half the interaction = 3 - 4 = -1
# 2x2 regression with interaction term
X = np.column_stack([np.ones(N), a, b, a & b]).astype(float)
beta, *_ = np.linalg.lstsq(X, y, rcond=None)
res = y - X @ beta; s2 = res @ res / (N - 4)
se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
print("main A", round(beta[1], 2), "main B", round(beta[2], 2), "interaction", round(beta[3], 2), "SE int", round(se[3], 2), "SE A", round(se[1], 2))
assert abs(beta[3] - inter) < 4 * se[3] and abs(beta[3]/se[3]) > 5
se_marg = np.sqrt(y[a].var()/a.sum() + y[~a].var()/(~a).sum())
print("interaction SE / marginal main-effect SE:", round(se[3]/se_marg, 2))   # 2 with equal cells
assert 1.8 < se[3]/se_marg < 2.2
# how often is a smaller interaction (-2) detected at this size? power by simulation
def power(inter_true, n, reps=300):
    hit = 0
    for _ in range(reps):
        a_ = rng.random(n) < .5; b_ = rng.random(n) < .5
        y_ = 100 + 3*a_ + 3*b_ + inter_true*(a_ & b_) + rng.normal(0, 40, n)
        X_ = np.column_stack([np.ones(n), a_, b_, a_ & b_]).astype(float)
        be, *_ = np.linalg.lstsq(X_, y_, rcond=None); r = y_ - X_@be
        s = np.sqrt((r@r/(n-4)) * np.linalg.inv(X_.T@X_)[3,3]); hit += abs(be[3]/s) > 1.96
    return hit/reps
p_small = power(-2.0, 20_000)
print("power to detect interaction -2 with 20,000 users:", p_small)
assert 0.25 < p_small < 0.6
```

**Output (my run):**
```text
share in each cell (A,B): {(0, 0): 0.25, (1, 0): 0.251, (0, 1): 0.25, (1, 1): 0.25}
cell (0, 0) mean 99.82 n 99863
cell (1, 0) mean 102.96 n 100217
cell (0, 1) mean 102.93 n 99919
cell (1, 1) mean 98.03 n 100001
A alone estimate -0.88 +/- 0.25
B alone estimate -0.91 +/- 0.25
main A 3.14 main B 3.11 interaction -8.03 SE int 0.25 SE A 0.18
interaction SE / marginal main-effect SE: 2.0
power to detect interaction -2 with 20,000 users: 0.4166666666666667
```

**Follow-ups:**
- How do platforms avoid it? Layers: experiments on the same surface share one layer and get disjoint user buckets. Experiments on unrelated surfaces sit in different layers with independent hashes. Also an automatic overlap warning at launch.
- Can you always keep the 25% cells? Yes, if hashing is independent. You also get the interaction test for free, which exclusion throws away.
- What if the interaction is small? Then reading each test alone is fine. Say how small you can rule out, not just "not significant".

**Common mistakes:** Treating the single readouts as the pure effects. Ignoring the 25% cell. Using the same hash salt in both experiments. Testing the interaction with the power of a main effect. Shipping both because each won on its own.

### Q46 ⭐ 🟡 In a redirect test, 100,000 users are assigned to each arm, but only 93,000 treatment users are logged as arriving on the new page against 100,000 in control. Treatment conversion among logged users is higher. Explain why this is a sample-ratio problem of a specific kind, what bias results and how you would recover a valid estimate.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The assignment split is 100,000 to 100,000, so a normal SRM check passes. The mismatch is between assigned and logged users in treatment only, which is differential attrition. The 93,000 are a selected group, so I compare everyone assigned, not everyone logged.

**Clarifying questions:**
- Where is "arrived" logged: client-side on the new page, or server-side at the redirect? Client logging loses users who bounce or have slow connections.
- Is assignment logged before the redirect, on the server? If yes, I can analyse by assignment (intent to treat). If no, I have a harder problem.
- What is the redirect mechanism, and what is its failure rate (blocked scripts, slow pages, ad blockers)? It tells me who the 7,000 are.
- Is the conversion event logged on the new page too? Then lost users also lose their conversions, and the metric itself is biased.
- Did control pass through any redirect? In a clean design control redirects to the old page too, so both arms pay the same loss.

**Approach:**
1. Name the problem. 93,000 / 100,000 is a 7% loss in treatment only. The chi-square against an even 96,500 / 96,500 split is about 254, far beyond chance. It is a sample-ratio problem of the kind "differential logging after assignment", not a bucketing bug.
2. Say why the bias is real. Users who drop in a redirect are rarely random. They are slower, on weaker devices or networks, or more impatient, and those users often convert less. Dropping them lifts the treatment average even with zero effect.
3. Recover the valid estimate. Analyse by assignment: all 100,000 vs all 100,000, using the assignment log. This is intent to treat. It is unbiased but diluted by the 7%.
4. If you need the effect on people who actually saw the page, scale ITT by the arrival rate only if arrival depends on assignment alone (an instrumental-variables view). State the assumption.
5. If assignment was not logged, use bounds. Lee bounds trim the control group by the lost share (monotone loss assumed). Report the range, not a point.
6. Fix the pipe. Log assignment on the server, make control take the same redirect, and alert on assigned-versus-logged ratio per arm.

**Metrics:**
- Arrival rate per arm = users logged on the page / users assigned. Here 93,000 / 100,000 = 93% vs 100%.
- ITT lift = conversions among all assigned in treatment / assigned - same for control.
- Guardrails: arrival rate gap (alert above, say, 0.5 point), page-load time p95, bounce rate.

**Risks:**
- ITT is diluted: with a real effect, it shrinks toward zero by the arrival rate.
- Lee bounds are wide when the loss is 7% and the outcome is a rare event (see the code).
- Selection could go either way. Fast users may be lost, not slow ones. Do not assume the direction.
- A "fix" like dropping the same share of control at random does not remove the selection.

**What the interviewer scores:**
- Strong: separates the assignment split (fine) from the logged split (broken), and names differential attrition.
- Strong: lands on ITT by assignment plus a fix to the logging.
- Weak: "run the SRM test and drop the test", or "just use the logged users since they saw the page".
- Weak: proposes reweighting without saying what it assumes.

**Example:** Illustrative simulation with a true effect of zero. 86% of users are fast and convert at 10%; 14% are slow and convert at 2%. Half of the slow users in treatment never log arrival (about 7,000 users). Naive logged-only lift: about +0.67 points. ITT: about +0.14 points (noise around zero). The naive lift is created by the lost users alone.
- Weak answer: "Treatment conversion is higher among logged users, ship." Strong answer: "Logged users are a filtered group, the filter is correlated with conversion, so I compare all 100,000 to all 100,000."

**Code:**
```python
# Q46: redirect test, differential logging, zero true effect (illustrative simulation)
import numpy as np
from scipy import stats
rng = np.random.default_rng(46)
n = 100_000
chi = (93_000-96_500)**2/96_500 + (100_000-96_500)**2/96_500
print("chi-square logged treatment vs control (expected 96,500 each):", round(chi, 1), "p =", stats.chi2.sf(chi, 1))
assert 253 < chi < 255
# users have a speed type; slow users convert less and are the ones whose redirect fails
slow = rng.random(2*n) < 0.14
arm = np.r_[np.zeros(n, bool), np.ones(n, bool)]       # False control, True treatment
conv = rng.random(2*n) < np.where(slow, 0.02, 0.10)    # NO treatment effect at all
lost = arm & slow & (rng.random(2*n) < 0.5)            # half of slow treatment users never log the arrival
logged = ~lost
print("logged control", int((logged & ~arm).sum()), "logged treatment", int((logged & arm).sum()))
assert 91_500 < (logged & arm).sum() < 94_500
naive = conv[logged & arm].mean() - conv[~arm].mean()
itt = conv[arm].mean() - conv[~arm].mean()
print("naive (logged only) lift:", round(naive*100, 3), "points   ITT (everyone assigned):", round(itt*100, 3), "points")
assert naive > 0.003 and abs(itt) < 0.003
# Lee bounds: trim the control group by the lost share (monotone loss assumed)
q = ((~arm).sum() - (logged & arm).sum()) / (~arm).sum()      # share to trim
c = np.sort(conv[~arm].astype(float))
k = int(round(q * len(c)))
tmean = conv[logged & arm].mean()
upper = tmean - c[: len(c) - k].mean()    # drop the highest control outcomes: control mean falls, effect rises
lower = tmean - c[k:].mean()              # drop the lowest control outcomes: control mean rises, effect falls
print("trim share", round(q, 3), "Lee bounds on effect among always-logged:", round(lower*100, 3), "to", round(upper*100, 3), "points")
assert abs(lower) < 0.003 and upper > 0.05      # lower bound is near the true zero (up to noise); upper bound is very wide
# ITT needs treatment arrival to be measured by ASSIGNMENT: join conversion to the assignment log, not to the landing-page log
```

**Output (my run):**
```text
chi-square logged treatment vs control (expected 96,500 each): 253.9 p = 3.692155186011113e-57
logged control 100000 logged treatment 92947
naive (logged only) lift: 0.668 points   ITT (everyone assigned): 0.137 points
trim share 0.071 Lee bounds on effect among always-logged: 0.005 to 7.594 points
```

**Follow-ups:**
- Why not just add an SRM check on the logged counts? You should, it is what caught this. But it only detects. The fix is analysing by assignment.
- What if the 7% are genuinely worse users in a way the new page causes (a slower page)? Then the loss is itself an effect of treatment, and ITT correctly counts it as a harm.
- Why are the Lee bounds so wide here? Trimming 7% of a group where the outcome is rare moves the mean a lot. The bounds say what the data can support, which is not much.

**Common mistakes:** Running the SRM test on assigned counts only and declaring all good. Analysing logged users. "Fixing" by reweighting without a stated assumption. Not logging assignment on the server. Letting only the treatment arm go through a redirect.

### Q47 ⭐ 🟡 A Bayesian dashboard shows 'probability treatment is best' at 96% on day 5 of a planned 14-day test, and the team wants to stop. Explain whether peeking is still a problem under a Bayesian readout, what the 96% depends on and how you would set a stopping rule.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Peeking is still a problem. A Bayesian posterior is valid at any time, but stopping the moment it crosses 96% turns it into a rule that fires on noise often, so I fix a stopping rule in advance and wait for the planned sample.

**Clarifying questions:**
- What prior does the dashboard use, and is it the same for every test? The 96% is a function of the prior as much as the data.
- Is "best" the chance treatment beats control by any amount? That says nothing about size. I want the chance it beats the minimum effect that matters.
- Was the stopping rule written down before the test, and does it include a minimum duration? Day 5 is not a whole week, so weekday effects are not covered.
- How many users have been seen by day 5 against the plan? A small sample with a flat prior can give a high number on a small gap.
- What is the cost of shipping a loser versus waiting 9 more days? It sets the threshold.

**Approach:**
1. Say what the 96% is: the posterior chance that treatment's rate is above control's, given this prior and this likelihood and the data so far. It is not the chance the test will still say so at day 14.
2. Show why stopping on it is risky. In an A/A test (no true difference) the 96% line is crossed at some daily look in about 16% of runs, although at one fixed look it is crossed in about 4% (computed below).
3. Say what is true in the Bayesian defence. If the prior is correct, the posterior is still a coherent belief after stopping. But the prior is rarely the real distribution of effects, and the business cares about how often it ships a dud.
4. Set the rule before the test: minimum run of full weeks, a decision on expected loss (what I lose, on average, if I pick treatment and I am wrong) below a small bound, and a probability that the lift exceeds the minimum worthwhile effect, not zero.
5. Check the rule's false-ship rate by simulation under no effect, with the daily looks you will actually take.
6. If the team must stop early, use an always-valid design (group-sequential or mixture sequential), not the dashboard number.

**Metrics:**
- P(best) = posterior P(p_treatment > p_control) = share of posterior draws where treatment is higher.
- Expected loss of shipping = average of max(p_control - p_treatment, 0) over posterior draws.
- False-ship rate = share of A/A tests where the rule says ship.
- Guardrails: sample ratio, weekday coverage, a guardrail metric that must not fall.

**Risks:**
- A flat prior is not neutral on a rate; it acts strongly when the sample is small.
- A lift that is "probably above zero" can be too small to matter.
- Early peeks pick up novelty effects.
- A strict stopping rule slows learning. Pay for that with a smaller number of tests, not weaker rules.

**What the interviewer scores:**
- Strong: says posterior validity and error-rate control are different things, and puts a number on the false-stop rate.
- Strong: asks about the prior, the effect-size threshold and the week structure.
- Weak: "Bayesian means you can stop any time."
- Weak: "Bayesian is wrong, use p-values" without a rule.

**Example:** Illustrative A/A simulation: 5,000 users per arm per day, 5% baseline, no true effect. Fraction of tests where P(best) is at least 96%: day 5 only 3.9%, day 14 only 3.8%, at any daily look 16.3%. With a real +4% relative lift, stopping at the first 96% reads "win" in 63% of tests, but a day-14 decision reads "win" in 47.9%: the stopping rule catches more wins and more false ones. A rule that needs 99% at day 7 or day 14 only fires 1.8% of the time under no effect.
- Weak answer: "96% is above 95%, ship." Strong answer: "96% at day 5 depends on the prior and a partial week. I keep the 14 days, read expected loss, and set the rule from a simulation of false ships."

**Code:**
```python
# Q47: Bayesian "probability treatment is best" under daily peeking (illustrative simulation)
import numpy as np
from scipy import stats
rng = np.random.default_rng(47)
DAYS, PER_DAY, P0 = 14, 5_000, 0.05          # users per arm per day, baseline conversion
def look_probs(true_lift, sims=4000):
    pc = np.full(sims, P0); pt = pc * (1 + true_lift)
    cc = rng.binomial(PER_DAY, pc[:, None], (sims, DAYS)).cumsum(1)
    ct = rng.binomial(PER_DAY, pt[:, None], (sims, DAYS)).cumsum(1)
    n = PER_DAY * np.arange(1, DAYS + 1)
    # Beta(1,1) posteriors, normal approximation to P(p_t > p_c)
    mc, mt = (cc + 1) / (n + 2), (ct + 1) / (n + 2)
    vc, vt = mc * (1 - mc) / (n + 3), mt * (1 - mt) / (n + 3)
    return stats.norm.cdf((mt - mc) / np.sqrt(vc + vt))
# check the approximation against exact beta draws on one case
c, t, n = 250, 300, 5000
d = rng.beta(t + 1, n - t + 1, 400_000) > rng.beta(c + 1, n - c + 1, 400_000)
mc, mt = (c+1)/(n+2), (t+1)/(n+2)
approx = stats.norm.cdf((mt-mc)/np.sqrt(mc*(1-mc)/(n+3)+mt*(1-mt)/(n+3)))
print("exact vs normal-approx P(best):", round(float(d.mean()), 4), round(float(approx), 4)); assert abs(d.mean()-approx) < 0.005
null = look_probs(0.0)
ever96 = (null >= 0.96).any(1).mean()
day5 = (null[:, 4] >= 0.96).mean()
last = (null[:, -1] >= 0.96).mean()
print("A/A tests: P(best)>=96% on day 5:", round(day5, 3), "| at the planned end (day 14):", round(last, 3), "| at ANY daily look:", round(ever96, 3))
assert ever96 > 2 * last and ever96 > 0.09
# the same rule with a real +4% relative lift
alt = look_probs(0.04)
print("true +4% lift: stop-at-96% on some day 1-13 and call it a win:", round((alt[:, :13] >= .96).any(1).mean(), 3), "| win at day 14:", round((alt[:, -1] >= .96).mean(), 3))
# stopping rule that waits for whole weeks, needs P(best) high AND expected loss small
n5 = PER_DAY * 5
print("day-5 sample per arm:", n5, " day-14:", PER_DAY * 14)
safer = ((null[:, 6] >= 0.99) | (null[:, 13] >= 0.99)).mean()
print("A/A tests that cross 99% at day 7 or day 14 only:", round(safer, 3))
assert safer < ever96
```

**Output (my run):**
```text
exact vs normal-approx P(best): 0.986 0.9857
A/A tests: P(best)>=96% on day 5: 0.039 | at the planned end (day 14): 0.038 | at ANY daily look: 0.163
true +4% lift: stop-at-96% on some day 1-13 and call it a win: 0.63 | win at day 14: 0.479
day-5 sample per arm: 25000  day-14: 70000
A/A tests that cross 99% at day 7 or day 14 only: 0.018
```

**Follow-ups:**
- Is sequential testing a frequentist idea only? No. There are Bayesian sequential rules too, but they need their error rates checked by simulation. See Book 1 Part 10 Q7 (the PM wants to stop the test after 3 days) for the classic peeking case.
- What about 99%? It is fewer false stops, not zero. The number is only meaningful with a stated prior and rule.
- Which readout do I show the PM? Expected loss and the probability the lift is above the minimum worthwhile effect, with a "decision at day 14" date.

**Common mistakes:** Treating the posterior as immune to peeking. Reading P(best) as effect size. Stopping at a partial week. Using a flat prior without noticing it. Tuning the threshold after seeing the data.

### Q48 ⭐ 🟡 A retention offer was piloted in the 100 stores with the weakest sales last quarter, and their sales rose 12% relative to their own previous quarter while the all-store average rose 2%. Explain regression to the mean, why the 12% overstates the offer's effect and how you would redo the pilot.
**Asked at:** Causal-inference and when-you-cannot-randomize material (an Interview Query causal-inference guide on diff-in-diff and synthetic control, Codemia 'explain difference-in-differences' practice pages, NBER working paper 25532 on synthetic difference-in-differences); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** If you pick the stores with the worst last quarter, many of them were unlucky, and unlucky quarters bounce back by themselves. The 12% is mostly that bounce, so I would redo the pilot with random assignment among comparable weak stores.

**Clarifying questions:**
- How was "weakest" defined: one quarter of sales, or a longer average? One bad quarter selects the most luck.
- Was there anything else different for those stores (seasonal, a local event, a closure)? A cause other than luck is a different story.
- How noisy is a store's sales from quarter to quarter, relative to the gap between stores? That sets the size of the bounce.
- Did the offer cost anything and what lift would pay for it? The break-even lift decides how precise the redo must be.
- Is the sales figure for the same stores each quarter? Closed stores dropping out would add survivorship.

**Approach:**
1. Explain regression to the mean in one line. Sales = stable level + one-off luck. A store in the bottom 100 is selected for bad luck, and next quarter its luck averages out, so it rises with no help.
2. Name the benchmark that is wrong. The all-store average (+2%) is the wrong comparison, because it was not selected on a bad quarter.
3. Show what to compare against: the weak stores that did not get the offer. If you cannot get them now, estimate the bounce from history: how much did the bottom 100 of past quarters rise without any program?
4. Redo the pilot: take the 200 weakest, randomly give the offer to 100 and not to the other 100. Both groups have the same selection, so the bounce cancels in the difference.
5. If randomizing is not possible, use matched weak stores as a control and a difference-in-differences read, with several pre-quarters to check trends.
6. Size the redo for the small effect you want to detect. Store sales are noisy, so 100 vs 100 detects only large effects (see the code).

**Metrics:**
- Naive change = sales next quarter / sales last quarter - 1, for the pilot stores.
- Bounce = the same change for the weakest stores that did not get the offer.
- Offer effect = change in treated stores - change in comparable untreated stores.
- Guardrails: margin after the offer cost, store closures, a check that the control stores are not receiving a similar program.

**Risks:**
- The bounce size depends on how noisy the quarters are; it is not a constant.
- Matching on last quarter alone repeats the same trap if you match to stores that were not selected on it.
- Selecting on the outcome in the redo (only stores that did badly) is fine, as long as assignment is random inside the group.
- A small randomized redo can come out negative by chance (see the spread below).

**What the interviewer scores:**
- Strong: explains luck plus selection, shows the right comparison, and fixes the design with randomization inside the weak group.
- Strong: can say how big the bounce might be and how to estimate it from history.
- Weak: "12% is better than 2%, so the offer works."
- Weak: "Compare to the all-store average" or "use a bigger sample" without fixing the selection.

**Example:** Illustrative simulation of 1,000 stores with no offer at all: all stores rise 2.2% (market growth); the 100 weakest last quarter rise 10.9% by luck alone. With a true offer effect of only +1.5%, the pilot reads +12.6%. A randomized redo among the 200 weakest recovers the truth on average (about +1.5%), but one run of 100 vs 100 has a spread of about 2.5 points.
- Weak answer: "The offer lifted sales 12%." Strong answer: "About 11 of the 12 points would have come anyway; the offer is worth maybe 1 to 2 points, and I need a random control to say which."

**Code:**
```python
# Q48: regression to the mean in a "weakest 100 stores" pilot (illustrative simulation)
import numpy as np
rng = np.random.default_rng(48)
SIG, GROW = 0.115, 1.02                              # one-off luck sd, market-wide growth
S = 1000                                          # all stores
level = rng.lognormal(np.log(100), 0.20, S)       # each store's stable sales level
q0 = level * rng.lognormal(0, SIG, S)            # last quarter = level x one-off luck
q1 = GROW * level * rng.lognormal(0, SIG, S)     # next quarter, NO offer anywhere
weakest = np.argsort(q0)[:100]
chg = lambda idx: q1[idx].sum() / q0[idx].sum() - 1
print("no offer anywhere. all stores:", round(100*chg(np.arange(S)), 1), "%  weakest 100:", round(100*chg(weakest), 1), "%")
assert chg(weakest) > 0.08 and 0.0 < chg(np.arange(S)) < 0.04
# the pilot: true offer effect is only +1.5%
TRUE = 0.015
q1_pilot = q1.copy(); q1_pilot[weakest] *= 1 + TRUE
naive = q1_pilot[weakest].sum() / q0[weakest].sum() - 1
print("pilot reads", round(100*naive, 1), "% for the 100 weakest, true offer effect is", 100*TRUE, "%")
assert 0.09 < naive < 0.15
# redo: take the 200 weakest, randomly give the offer to 100 of them
reps, est = 2000, []
for _ in range(reps):
    lvl = rng.lognormal(np.log(100), 0.20, S)
    a = lvl * rng.lognormal(0, SIG, S); b = GROW * lvl * rng.lognormal(0, SIG, S)
    weak = np.argsort(a)[:200]; perm = rng.permutation(weak); tr, ct = perm[:100], perm[100:]
    b = b.copy(); b[tr] *= 1 + TRUE
    est.append((b[tr].sum()/a[tr].sum()) - (b[ct].sum()/a[ct].sum()))
est = np.array(est)
print("randomised among the 200 weakest: mean estimate", round(100*est.mean(), 2), "% (truth 1.5%), sd across reruns", round(100*est.std(), 2), "%")
assert abs(est.mean() - TRUE) < 0.004
```

**Output (my run):**
```text
no offer anywhere. all stores: 2.2 %  weakest 100: 10.9 %
pilot reads 12.6 % for the 100 weakest, true offer effect is 1.5 %
randomised among the 200 weakest: mean estimate 1.55 % (truth 1.5%), sd across reruns 2.48 %
```

**Follow-ups:**
- How do I estimate the bounce without a new pilot? Compare the bottom 100 of earlier quarters with no program; that bounce is your null.
- What if the offer has a real effect and the bounce is zero? Then the 12% would be right. The point is that you cannot know without a control.
- Is this the same as the winner's curse? It is the same selection idea in a different place. See Q44 earlier in this part.

**Common mistakes:** Comparing to the all-store average. Selecting on one noisy quarter. Not keeping a randomized or matched control. Declaring a result from 100 stores with a 2.5 point spread. Forgetting the closed stores.

### Q49 ⭐ 🟡 An LLM judge from the same model family as the treatment prefers treatment in 1,160 of 2,000 pairs (58%), while humans on 300 pairs prefer it 51% of the time. Explain self-preference and other judge biases, how you test for them and how you use the judge in an experiment.
**Asked at:** AI-era experiment material (an Atlan 2026 guide to A/B testing LLM applications, tianpan.co 2026 posts on non-deterministic AI features, an efficientlyconnected.com post on nondeterminism); practitioner posts rather than confirmed interview banks, an emerging theme; search snippets only, not opened
**Say this first (1 line):** A judge from the same family as the treatment tends to prefer its own style, and 58% from the judge against 51% from humans is a gap of 7 points that I treat as bias until a different judge and the human labels say otherwise. I use the judge to screen, and humans decide the close calls.

**Clarifying questions:**
- Are the 300 human pairs a random subset of the 2,000, with the judge's verdict on the same pairs? If not, I cannot compare like with like.
- Were pairs shown in random order, and were ties excluded? Position bias and ties change the 58%.
- Who rated the human pairs, how many raters, and what was their agreement? A noisy human label limits what the judge can be checked against.
- Does the treatment output come from the judge's own model family? That is the self-preference risk.
- What decision depends on this: ship, or just triage? It sets how strict I am.

**Approach:**
1. Check the numbers. 1,160 / 2,000 = 58.0%, with a 95% interval of about 55.8% to 60.2%. Humans: 153 / 300 = 51%, interval about 45.3% to 56.7%, which includes 50%. The difference is 7 points, z about 2.3, p about 0.02.
2. Name the biases: self-preference (likes text that looks like its own), position bias (favours the first or second slot), length bias (longer looks better), style or format bias. Book 1 Part 10 Q56 (validating an LLM-as-judge metric) owns the theory.
3. Test each. Swap order and compare the two win rates for position. Add a different-family judge for self-preference. Regress the verdict on length difference.
4. Calibrate on humans. On the 300 labelled pairs compute agreement and chance-corrected agreement (kappa), sensitivity and specificity against the human label.
5. Use the judge in the experiment only as a screen: both orders, a cross-family panel, a fixed rubric, and a human audit sample (including pairs the judge scored near 50%).
6. Make the decision on the primary behavioural metric and on the human-audited sample. The judge never decides alone.

**Metrics:**
- Judge win rate = treatment wins / (treatment wins + control wins), ties reported separately.
- Position effect = win rate with treatment first - win rate with treatment second.
- Cohen's kappa = (agreement - chance agreement) / (1 - chance agreement).
- Self-preference gap = same-family judge win rate - cross-family judge win rate on the same pairs.
- Guardrails: judge drift across dates, human audit sample size.

**Risks:**
- Averaging over both orders removes position bias but not self-preference.
- A cross-family judge has its own biases, so use two or three.
- 300 human pairs give a wide interval (about plus or minus 5.7 points). Do not over-read a small gap.
- Tuning the rubric until judge and humans agree can overfit the 300.

**What the interviewer scores:**
- Strong: checks the arithmetic and the intervals, then lists the biases and a test for each.
- Strong: treats the judge as a calibrated instrument with a human audit, not as ground truth.
- Weak: "58% means treatment is better" or "the judge is biased, discard it".
- Weak: more human labels is the only suggestion, with no cheaper checks.

**Example:** Illustrative simulation: real quality edge is tiny. The same-family judge adds a self bonus and a position bonus. Treatment in slot A wins 61.0%, in slot B 55.4%, average 58.2%. A cross-family judge averaged over both orders gives 50.7%, humans 49.9%. So about 7.5 of the 8.3 points over humans are bias. On a 300-pair human sample the same-family judge shows kappa near 0.06 with humans.
- Weak answer: "The judge says 58%, ship." Strong answer: "The judge is not independent of the treatment. I swap order, add a different-family judge, and check 300 human pairs before I trust any of it."

**Code:**
```python
# Q49: LLM judge vs humans, self-preference (illustrative)
import numpy as np
from scipy import stats
rng = np.random.default_rng(49)
print("judge win rate:", 1160/2000, " humans:", round(153/300, 3))
assert 1160/2000 == 0.58 and round(0.51*300) == 153
se_j = np.sqrt(.58*.42/2000); se_h = np.sqrt(.51*.49/300)
print("judge 95% CI:", round(.58-1.96*se_j, 3), round(.58+1.96*se_j, 3), "| human 95% CI:", round(.51-1.96*se_h, 3), round(.51+1.96*se_h, 3))
z = (.58-.51)/np.sqrt(se_j**2 + se_h**2); print("two-sample z", round(z, 2), "p =", round(2*stats.norm.sf(z), 3))
assert 0.45 < .51-1.96*se_h < 0.46 and .51+1.96*se_h > .5
# simulate a judge with real signal + self-preference + position bias; humans see only quality
N = 20_000
quality = rng.normal(0.05, 1.0, N)                    # treatment's true quality edge per pair (tiny)
human_p = 1/(1+np.exp(-0.2*quality))
human = rng.random(N) < human_p
def judge(self_bonus, pos_bonus, swap):
    # swap=True means treatment is shown second; position bias favours slot A
    pos = -pos_bonus if swap else pos_bonus
    p = 1/(1+np.exp(-(0.9*quality + self_bonus + pos)))
    return rng.random(N) < p
j1 = judge(0.35, 0.15, swap=False); j2 = judge(0.35, 0.15, swap=True)
both = (j1 & j2)                                        # treatment wins in BOTH orders
print("judge treatment win, treatment in slot A:", round(j1.mean(), 3), " slot B:", round(j2.mean(), 3))
print("average over both orders:", round((j1.mean() + j2.mean())/2, 3))
cross = judge(0.0, 0.15, swap=False); cross2 = judge(0.0, 0.15, swap=True)
print("cross-family judge (no self bonus), averaged over orders:", round((cross.mean()+cross2.mean())/2, 3), "| human:", round(human.mean(), 3))
assert j1.mean() > j2.mean()                           # position bias visible
assert (j1.mean()+j2.mean())/2 - (cross.mean()+cross2.mean())/2 > 0.05
# calibrate on 300 human-labelled pairs: use judge order-averaged verdict; check agreement
idx = rng.choice(N, 300, replace=False)
jv = j1[idx]                                          # the judge's single verdict, treatment shown first
hv = human[idx]
agree = (jv == hv).mean(); pe = jv.mean()*hv.mean() + (1-jv.mean())*(1-hv.mean())
print("raw agreement", round(agree, 3), "Cohen kappa", round((agree-pe)/(1-pe), 3))
assert (agree-pe)/(1-pe) < 0.4
```

**Output (my run):**
```text
judge win rate: 0.58  humans: 0.51
judge 95% CI: 0.558 0.602 | human 95% CI: 0.453 0.567
two-sample z 2.27 p = 0.023
judge treatment win, treatment in slot A: 0.61  slot B: 0.554
average over both orders: 0.582
cross-family judge (no self bonus), averaged over orders: 0.507 | human: 0.499
raw agreement 0.527 Cohen kappa 0.061
```

**Follow-ups:**
- Why not just use humans? Cost and speed. Use the judge to prioritise and humans to audit.
- Can you correct the judge's win rate using the human sample? Sometimes, with sensitivity and specificity from the labelled pairs, but only if the judge behaves the same outside that sample.
- Does swapping order fix self-preference? No. It fixes position only.

**Common mistakes:** Reading the judge's win rate as the user's win rate. Not swapping order. Judging with the same family that wrote the treatment. Comparing 2,000 judged pairs to 300 human pairs without checking they are the same kind of pair. Relying on raw agreement instead of kappa.

### Q50 ⭐ 🔴 A ranking team says a user-level A/B test would need 6 weeks to detect a 0.5% relative lift in clicks, and proposes interleaving to get a result in 1 week. Explain why interleaving is more sensitive, what it cannot measure and when you would still run the A/B test.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
**Say this first (1 line):** Interleaving shows both rankers to the same user in one list, so each user is their own control and the huge differences between users cancel out. That is why it needs far fewer users, but it only measures preference between rankers, not the lift in a business metric.

**Clarifying questions:**
- How different are the two rankers? Interleaving works when both produce comparable lists; if they differ in format or slate size it breaks down.
- What is the lift metric in the A/B test, and what does the 0.5% mean in clicks per user? I need the baseline noise.
- Is the decision "which ranker is better at ranking" or "what is the effect on revenue and retention"? They need different tools.
- Does the page have one list, or several slots and modules? Interleaving needs a single ranked list to merge.
- Can the platform log which ranker contributed each clicked item? Without that, nothing can be credited.

**Approach:**
1. Explain how it works: merge the two rankers' lists (for example team-draft: take turns picking the best item not yet shown), remember which ranker each item came from, and credit a click to that ranker.
2. Explain why it is more sensitive. In an A/B test the two arms contain different people, and people differ a lot in how much they click. That spread is the noise. In interleaving, the comparison happens inside each user, so the spread between users drops out. Only the within-user difference is left.
3. Put a number on it. In my illustration the A/B test needs between about 1.5 and 7.6 times more users depending on how uneven users are (computed below). The prompt's 6x (6 weeks versus 1 week) is realistic only when users are very uneven; I would measure the ratio on my own logs before promising a week.
4. Say what it cannot measure. Absolute lift in a business metric (a preference win rate does not translate to a % lift); effects that depend on the whole page (latency, diversity, revenue per session); anything about long-term behaviour; effects that need one ranker to be used consistently.
5. Use it as a filter. Interleave many candidate rankers quickly, send the winner to a full A/B test for the business metric.
6. Still run the A/B test when the ship decision is about revenue, retention or latency, when the change is not a ranking change, or when the interleaved list would look odd to users.

**Metrics:**
- Per user: d = clicks credited to B - clicks credited to A. Preference = sum of d / total credited clicks, or the share of users with d > 0.
- A/B metric = clicks per user (or CTR), difference in means with a confidence interval.
- Sample-size ratio = users needed for the A/B test / users needed for interleaving at the same power.
- Guardrails: latency, position bias in the interleaving method, agreement between interleaving and past A/B results.

**Risks:**
- Interleaving can be biased by the merge method (position bias favours the ranker with the first slot) unless the order is randomized.
- It measures preference between two rankers shown together. A ranker that wins in a mix may not win alone.
- The interleaved page is not a product users will see. It cannot test layout or latency.
- A high sensitivity can flag very small differences that do not matter. Set a minimum worthwhile win rate.

**What the interviewer scores:**
- Strong: explains within-user comparison and variance, and gives a number or a mechanism for the speed-up.
- Strong: lists what it cannot measure and keeps an A/B test for the business decision.
- Weak: "it is faster because it is smarter" with no variance argument.
- Weak: "replace A/B testing with interleaving".

**Example:** Illustrative: users have 2 clicks on average, very uneven (some click a lot, many click zero), ranker B adds 0.5% more clicks. A/B test needs about 2,404,000 users per arm (4.8 million total). Interleaving needs about 630,000 users. Ratio 7.6. With even users the ratio is only 1.5.
- Weak answer: "Interleaving is just more efficient, switch to it." Strong answer: "It cancels between-user noise, so I use it to pick the best ranker in a week, and I run the A/B test to size the business lift."

**Code:**
```python
# Q50: why interleaving needs far fewer users than a user-level A/B test (illustrative simulation)
import numpy as np
from scipy import stats
rng = np.random.default_rng(50)
LIFT = 0.005                                         # ranker B gets 0.5% more clicks than A
def users(n, shape):
    return rng.gamma(shape, 2.0 / shape, n)          # mean 2 clicks per user, heavy between-user spread
def ab_p(n, shape):
    lam = users(2*n, shape); arm = np.r_[np.zeros(n, bool), np.ones(n, bool)]
    y = rng.poisson(lam * np.where(arm, 1 + LIFT, 1.0))
    return stats.ttest_ind(y[arm], y[~arm], equal_var=False).pvalue
def il_p(n, shape):
    lam = users(n, shape); clicks = rng.poisson(lam)            # every user sees the interleaved list
    pB = (1 + LIFT) / (2 + LIFT)                                 # share of clicks that land on B's items
    d = 2 * rng.binomial(clicks, pB) - clicks                    # per-user (B clicks - A clicks)
    return stats.ttest_1samp(d, 0).pvalue
def power(f, n, shape, reps=400):
    return np.mean([f(n, shape) < 0.05 for _ in range(reps)])
for shape in (4.0, 0.3):
    # analytic users needed for 80% power, from variances
    mean, var_lam = 2.0, 4.0 / shape
    n_ab = 2 * (1.96 + 0.84)**2 * (var_lam + mean) / (LIFT * mean)**2          # per arm, Poisson mixture variance
    pB = (1 + LIFT) / (2 + LIFT); mu_d = mean * (2*pB - 1); var_d = mean * (1 - (2*pB-1)**2) + (2*pB-1)**2 * var_lam
    n_il = (1.96 + 0.84)**2 * var_d / mu_d**2                                    # total users, one group
    print(f"between-user spread shape={shape}: A/B needs {n_ab:,.0f} per arm ({2*n_ab:,.0f} total); interleaving {n_il:,.0f} users; ratio {2*n_ab/n_il:.1f}x")
    if shape == 0.3: ratio_heavy = 2*n_ab/n_il
    if shape == 4.0: ratio_light = 2*n_ab/n_il
assert ratio_heavy > ratio_light > 1.4
# check by simulation at the interleaving sample size
pa, pi = power(ab_p, 315_000, 0.3, 100), power(il_p, 630_000, 0.3, 100)
print("simulated power with the SAME 630,000 users (heavy-tailed): A/B 315,000 per arm =", pa, "| interleaving =", pi)
assert pi > 0.7 and pa < 0.3
```

**Output (my run):**
```text
between-user spread shape=4.0: A/B needs 470,400 per arm (940,800 total); interleaving 630,338 users; ratio 1.5x
between-user spread shape=0.3: A/B needs 2,404,267 per arm (4,808,533 total); interleaving 630,362 users; ratio 7.6x
simulated power with the SAME 630,000 users (heavy-tailed): A/B 315,000 per arm = 0.18 | interleaving = 0.78
```

**Follow-ups:**
- Can you convert a preference win rate to a lift? Not directly. Calibrate with past experiments that ran both ways, and say how wide the conversion is.
- What if only one slot is ranked? Then interleaving has little to merge. Use A/B.
- Book 1 Part 10 Q50 (how an interleaving experiment works and why it is more sensitive) has the theory; here I would stress the decision.

**Common mistakes:** Claiming a fixed speed-up. Not randomizing which ranker goes first. Using interleaving for non-ranking changes. Treating the preference win rate as revenue lift. Skipping the final A/B test.

### Q51 ⭐ 🔴 Leadership wants ship decisions after 7 days, but the target is 90-day retention, and across 60 past experiments the 7-day retention lift correlates 0.5 with the 90-day lift. Explain how you would build and validate a surrogate metric, what the 0.5 allows you to say and what long-term safeguards you keep.
**Asked at:** Guardrail and ship-decision material (a Dataford 'primary vs guardrail metrics' page, a Spotify Confidence guardrail-metric glossary and blog post, PracHub analytics-and-experimentation question pages, a Dataford 'non significant test PM wants launch' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** A correlation of 0.5 between 7-day and 90-day lifts is useful but weak: it means the 7-day number points the right way about two times in three, and it explains about a quarter of the variation, so I use it as one input with an uncertainty band, and I keep long-term holdouts to check.

**Clarifying questions:**
- What are the 60 experiments: lifts per experiment (one point each), or user-level data? The correlation is across experiments, so each point has measurement noise.
- Are the 60 similar in type to the new one? A surrogate learned on ranking tests may fail on pricing tests.
- How noisy were the 90-day lifts? Noise in either lift lowers the observed correlation below the true one.
- What does a wrong ship cost compared with waiting 90 days? It sets how much certainty I need.
- Are there known mechanisms (for example, habit formation) that link early use to retention? A causal story strengthens a statistical link.

**Approach:**
1. Say what 0.5 gives. R squared is 0.25, so the 7-day lift explains a quarter of the variation in 90-day lift. The 95% interval for r with 60 points is about 0.28 to 0.67 (Fisher z).
2. Say what it allows. The sign agrees in about 2 of 3 experiments (arccos formula for two normal variables). A 7-day lift one standard deviation above average predicts a 90-day lift of 0.5 sd with residual sd 0.87, so the chance the true 90-day lift is positive is about 72%.
3. Say what it does not allow. It does not say the 7-day metric causes the 90-day outcome, and it does not transfer to a new type of change.
4. Build the surrogate properly. Use experiment-level data (lift on 7-day metrics versus lift on 90-day retention), try a few early metrics and combine them, and fit with leave-one-out validation.
5. Validate out of sample: report leave-one-out R squared (lower than 0.25 in my run), calibration of the predicted interval, and the share of past decisions the surrogate would have gotten right.
6. Keep safeguards: ship on a prediction band, not a point; keep a long-term holdout for 90 days; tell the team how many past surrogate "ships" later turned out wrong; and for risky or irreversible changes wait.

**Metrics:**
- Surrogate lift = the 7-day retention lift (treatment minus control, same cohort definition).
- Target lift = 90-day retention lift for the same experiment.
- Correlation r across experiments; R squared; leave-one-out R squared.
- Decision accuracy = share of past experiments where surrogate and target agree on sign. Guardrails: holdout retention at 90 days, share of surrogate ships later reversed.

**Risks:**
- Measurement noise makes the observed r smaller than the true r (0.7 true gave 0.42 observed in my run), so the true link may be better, but you cannot assume that.
- Only 60 points: the observed r would move between about 0.33 and 0.65 on a rerun with new experiments.
- Surrogates break when a change works on the surrogate without working on the goal (a notification that lifts day-7 opens but annoys users later).
- Using the surrogate to pick winners selects experiments that game it (Goodhart effect).

**What the interviewer scores:**
- Strong: computes what 0.5 means (R squared, interval, sign agreement, a probability of a positive lift) rather than calling it "strong" or "weak".
- Strong: separates statistical association from causal surrogacy and keeps a holdout.
- Weak: "0.5 is moderate, so we can use 7-day."
- Weak: waits 90 days for everything, or ships on 7-day with no check.

**Example:** Illustrative: across 60 experiments r = 0.5. A new test shows a 7-day lift that is one standard deviation above the average 7-day lift. The model predicts 0.5 sd for the 90-day lift with residual sd 0.87. P(90-day lift above zero) = Phi(0.5 / 0.866) = 0.72. So about 3 in 10 such "wins" would be real losers. For a cheap, reversible change that is acceptable; for a pricing change it is not.
- Weak answer: "0.5 correlation, so 7-day is a good proxy." Strong answer: "0.5 gives me a 72% chance the 90-day lift is positive at one sd. I ship the reversible ones on that and hold out 5% to confirm at 90 days."

**Code:**
```python
# Q51: what a 0.5 correlation between 7-day and 90-day lifts across 60 experiments allows (illustrative)
import numpy as np
from scipy import stats
rng = np.random.default_rng(51)
r, n = 0.5, 60
z = np.arctanh(r); se = 1/np.sqrt(n-3)
lo, hi = np.tanh(z-1.96*se), np.tanh(z+1.96*se)
print("r =", r, " 95% CI via Fisher z:", round(lo, 2), "to", round(hi, 2), " R^2 =", r**2)
assert 0.27 < lo < 0.29 and 0.66 < hi < 0.68
print("p-value of r=0.5, n=60:", stats.t.sf(r*np.sqrt((n-2)/(1-r**2)), n-2)*2)
agree = 1 - np.arccos(r)/np.pi
print("P(7-day and 90-day lifts have the same sign), bivariate normal:", round(agree, 3))
assert abs(agree - 2/3) < 1e-9
# a 7-day lift one standard deviation above average
s1 = 1.0
pred_mean = r*s1; resid_sd = np.sqrt(1 - r**2)
p_pos = stats.norm.cdf(pred_mean/resid_sd)
print("given a 7-day lift of +1 sd: predicted 90-day lift", pred_mean, "sd, residual sd", round(resid_sd, 3), "-> P(90-day lift > 0) =", round(p_pos, 3))
assert 0.71 < p_pos < 0.73
# measurement noise: observed r is lower than the true r between the real effects
true_r, k = 0.7, 4000
t7, t90 = rng.multivariate_normal([0, 0], [[1, true_r], [true_r, 1]], k).T
o7 = t7 + rng.normal(0, 0.8, k); o90 = t90 + rng.normal(0, 0.8, k)   # each experiment's lift is measured with noise
print("true r between real effects", true_r, "-> observed r between measured lifts", round(np.corrcoef(o7, o90)[0, 1], 3))
assert np.corrcoef(o7, o90)[0, 1] < 0.5
# spread of observed r with 60 experiments (what luck alone does)
rs = []
for _ in range(2000):
    x, y = rng.multivariate_normal([0, 0], [[1, .5], [.5, 1]], 60).T; rs.append(np.corrcoef(x, y)[0, 1])
print("same true r=0.5, rerun with 60 new experiments: observed r in", np.round(np.percentile(rs, [5, 95]), 2), "(5th-95th pct)")
# leave-one-out prediction error of the surrogate on 60 experiments
x, y = rng.multivariate_normal([0, 0], [[1, .5], [.5, 1]], 60).T
pred = np.array([np.polyval(np.polyfit(np.delete(x, i), np.delete(y, i), 1), x[i]) for i in range(60)])
print("leave-one-out R^2 (honest out-of-sample):", round(1 - ((y-pred)**2).sum()/((y-y.mean())**2).sum(), 3))
```

**Output (my run):**
```text
r = 0.5  95% CI via Fisher z: 0.28 to 0.67  R^2 = 0.25
p-value of r=0.5, n=60: 4.7489326275419496e-05
P(7-day and 90-day lifts have the same sign), bivariate normal: 0.667
given a 7-day lift of +1 sd: predicted 90-day lift 0.5 sd, residual sd 0.866 -> P(90-day lift > 0) = 0.718
true r between real effects 0.7 -> observed r between measured lifts 0.423
same true r=0.5, rerun with 60 new experiments: observed r in [0.33 0.65] (5th-95th pct)
leave-one-out R^2 (honest out-of-sample): 0.154
```

**Follow-ups:**
- How would I strengthen the surrogate? Combine several early metrics, use a longer window (day 28), and add a mechanism metric. Test on experiments held out by type.
- What if leadership wants a yes or no? Give the probability and the cost of being wrong, and propose reversible launch with a holdout. See Book 1 Part 10 Q40 (running experiments for long-term outcomes) for the theory.
- Can I pool users from all experiments? Not for this question. The unit is the experiment, since the decision is per experiment.

**Common mistakes:** Calling r = 0.5 strong. Ignoring that each lift is noisy. Fitting and testing on the same 60. Treating correlation as surrogacy. Dropping the long-term holdout once the surrogate exists.

### Q52 ⭐ 🔴 An ad-auction change is tested by randomizing advertisers 50/50, but treated and control advertisers bid for the same impressions and draw on shared budgets. Explain the interference, the bias in the naive comparison and how a budget-split or auction-level design would help.
**Asked at:** Marketplace, interference and switchback material (Dataford 'interference in marketplace experiments', 'marketplace experiment with interference' and 'choose switchback for marketplace dispatch' pages, a DoorDash careers blog post, an arXiv 2022 paper on switchbacks and interference bias, a Statsig marketplace-experimentation page); company practice is described only as the snippets reported it; search snippets only, not opened
**Say this first (1 line):** Randomizing advertisers breaks the assumption that one advertiser's result does not depend on what others are doing. Treated and control advertisers fight for the same impressions and the same money, so the naive gap measures how treated advertisers take from control ones, not what happens when the change is live for everyone.

**Clarifying questions:**
- What exactly changes: bidding, ranking, pricing, or the auction rule? Rule changes touch everyone; bid changes touch only the treated.
- Do budgets bind (do advertisers run out), and is spend paced across the day? Binding budgets make advertisers compete across time as well.
- What is the launch decision: the change for all advertisers, or an opt-in tool for some? It tells me which counterfactual I need (everyone treated versus nobody).
- Which metric: advertiser value, platform revenue, or user experience? Revenue and advertiser value can move in opposite directions.
- Can we split traffic at the auction level and split budgets? That is the design that fixes it, and it needs engineering.

**Approach:**
1. Name the interference. Treated advertisers change their bids, win impressions that control advertisers would have won, and change prices that control advertisers pay. Shared budgets pass the effect across time: spending more early leaves less later, for treated and control.
2. Say what the naive comparison measures: treated versus control inside one mixed market. The business question is all-treated versus all-control. These can differ in size and even in sign.
3. Show it with a toy auction (below): the true all-versus-none effect is -12.1% on advertiser value, the naive advertiser-level comparison says -43.5%, and control advertisers gain 28.5% from the treated ones' mistakes.
4. Use a design where the unit of randomization contains the competition. Auction-level split: each impression is randomly sent to a "treatment" or "control" marketplace, and every advertiser's budget is split between the two. Each arm then behaves like a market with all-treated or all-control participants.
5. Alternatives: budget-split with pacing, cluster by advertiser group or by vertical, geo or time switchbacks, and a final ramp at the market level.
6. Check the design: split-budget spend should match the original budgets, bid landscape should look alike in both arms, and an A/A test on the split must show about zero.

**Metrics:**
- Advertiser value = sum of the value of impressions won (conversions or clicks weighted by value).
- Platform revenue = total spend on the arm's impressions.
- Effect = metric in the all-treated arm / metric in the all-control arm - 1.
- Guardrails: budget exhaustion time, price per click, advertiser churn, user-facing relevance.

**Risks:**
- Splitting budgets halves each arm's budget, which changes how often budgets bind. State it.
- Auction-level split has to be fine enough that the two arms see the same traffic mix.
- Learning systems (bidding agents) adapt slowly; a short split test may miss the long-run effect.
- Interference is not only in the bias, it also depends on the share of treated. Report results at the arm's share.

**What the interviewer scores:**
- Strong: states the all-treated versus all-control question and shows the naive gap is not that.
- Strong: proposes a design that makes competition internal to each arm (auction-level split, budget split) and says what it costs.
- Weak: "randomize advertisers and use more data".
- Weak: says the bias is always an overstatement; the direction depends on the setup.

**Example:** Illustrative toy second-price auction: 40 advertisers, 20,000 impressions, budgets that bind, treatment = bids 25% higher. All-treated versus all-control: value -12.1%, spend about 0%. Advertiser-level 50/50 split: treated advertisers show -43.5% (range -45.3% to -42.0% across 8 random splits), and control advertisers see +28.5% versus a world where nobody was treated. Auction-level split with half budgets per arm: -12.2%.
- Weak answer: "Treated advertisers lost 43%, kill it." Strong answer: "That number is mixed-market. The correct comparison is all versus none, which my split-budget design puts at about -12%."

**Code:**
```python
# Q52: advertiser-level randomization in a shared auction with shared budgets (illustrative simulation)
import numpy as np
rng = np.random.default_rng(52)
ADV, IMP, BUD = 40, 20_000, 520.0           # advertisers, impressions, budget each (budget binds)
def run(boost, seed=0):
    """second-price auction per impression; boost[i] multiplies advertiser i's bid; a spent budget stops bidding."""
    r = np.random.default_rng(seed)
    val = r.lognormal(0, 0.5, (IMP, ADV)) * r.lognormal(0, 0.3, ADV)      # value per impression
    wins = np.zeros(ADV); value = np.zeros(ADV); spend = np.zeros(ADV)
    budget = np.full(ADV, BUD)
    for t in range(IMP):
        bid = val[t] * boost; bid = np.where(spend < budget, bid, 0.0)
        top = np.argsort(bid)[-2:]
        i, price = top[1], bid[top[0]]
        if bid[i] <= 0: continue
        wins[i] += 1; value[i] += val[t, i]; spend[i] += price
    return wins, value, spend
B = 1.25
ctrl_all = run(np.ones(ADV), seed=1)
trt_all = run(np.full(ADV, B), seed=1)
truth = (trt_all[1].sum() - ctrl_all[1].sum()) / ctrl_all[1].sum()
truth_spend = (trt_all[2].sum() - ctrl_all[2].sum()) / ctrl_all[2].sum()
print("TRUTH (everyone vs nobody boosted): value delivered", f"{100*truth:+.1f}%", " spend", f"{100*truth_spend:+.1f}%")
# advertiser-randomised: half the advertisers boosted, same marketplace
naive = []; spill = []
for s in range(8):
    arm = rng.permutation(ADV) < ADV // 2
    w, v, sp = run(np.where(arm, B, 1.0), seed=1)
    naive.append(v[arm].mean() / v[~arm].mean() - 1)
    spill.append(v[~arm].sum() / ctrl_all[1][~arm].sum() - 1)   # control advertisers vs the same advertisers in the all-control world
print("NAIVE (advertiser-level 50/50): value per advertiser treated vs control", f"{100*np.mean(naive):+.1f}%", "(range", f"{100*min(naive):+.1f}% to {100*max(naive):+.1f}%)")
print("SPILLOVER: control advertisers' own value vs the all-control world:", f"{100*np.mean(spill):+.1f}%", "(SUTVA says this would be 0)")
assert np.mean(spill) > 0.1
# auction-level split: each impression is randomly given to a 'boosted' or 'plain' mini-marketplace with half budgets
r = np.random.default_rng(1); val = r.lognormal(0, 0.5, (IMP, ADV)) * r.lognormal(0, 0.3, ADV)
side = rng.random(IMP) < 0.5
def mini(mask, boost):
    v = np.zeros(ADV); spend = np.zeros(ADV); bud = BUD / 2
    for t in np.where(mask)[0]:
        bid = np.where(spend < bud, val[t] * boost, 0.0); top = np.argsort(bid)[-2:]
        i, p = top[1], bid[top[0]]
        if bid[i] <= 0: continue
        v[i] += val[t, i]; spend[i] += p
    return v, spend
vt, st = mini(side, B); vc, sc = mini(~side, 1.0)
est = vt.sum() / vc.sum() - 1
print("AUCTION-LEVEL split with half budgets in each arm: value", f"{100*est:+.1f}%", "(truth", f"{100*truth:+.1f}%)")
assert abs(np.mean(naive) - truth) > 0.15 and np.mean(naive) < truth
assert abs(est - truth) < 0.05
```

**Output (my run):**
```text
TRUTH (everyone vs nobody boosted): value delivered -12.1%  spend -0.0%
NAIVE (advertiser-level 50/50): value per advertiser treated vs control -43.5% (range -45.3% to -42.0%)
SPILLOVER: control advertisers' own value vs the all-control world: +28.5% (SUTVA says this would be 0)
AUCTION-LEVEL split with half budgets in each arm: value -12.2% (truth -12.1%)
```

**Follow-ups:**
- Why does the toy show a loss from bidding higher? In a second-price auction with budgets that bind, higher bids buy impressions at higher prices against rivals who bid less, so the same money buys less value. The size is specific to my toy.
- Is the bias always upward? No. Here the naive effect is more negative than the truth. Direction depends on the mechanism.
- When is advertiser-level randomization acceptable? When each advertiser is small relative to the market and budgets do not bind.

**Common mistakes:** Treating advertisers as independent. Splitting traffic without splitting budgets. Reporting the mixed-market gap as the launch effect. Ignoring spillover to control. Forgetting that platform revenue and advertiser value can disagree.

### Q53 ⭐ 🔴 Two weeks into a 4-week test of an LLM feature, the provider silently updated the underlying model, and a fixed 500-prompt regression suite run on the treatment path shows its pass rate moving from 82% to 87% (+5 points absolute) between week 2 and week 3. Explain how you detect and handle a mid-test change in the treatment and what you would pin or log in advance.
**Asked at:** AI-era experiment material (an Atlan 2026 guide to A/B testing LLM applications, tianpan.co 2026 posts on non-deterministic AI features, an efficientlyconnected.com post on nondeterminism); practitioner posts rather than confirmed interview banks, an emerging theme; search snippets only, not opened
**Say this first (1 line):** The treatment changed under my feet, so the test no longer has one treatment. I split the data at the update date, report each period separately, stop pooling the weeks, and from now on I pin the model version and log it on every request.

**Clarifying questions:**
- How do I know the update date: a provider notice, a version string in responses, or only the suite shift? An exact timestamp lets me split the data cleanly.
- Does the control arm use the same provider and model, or a fixed non-LLM path? If control also changed, a difference-in-differences read is still valid.
- Is the 500-prompt suite fixed and scored by the same method each time, and is it run once a week or daily? A single run per week has no noise estimate.
- Which metrics in the experiment moved at the same date (task success, latency, cost per request)? I look for a break in all of them, not just the suite.
- Can I pin a dated model version now and restart? That decides between salvage and rerun.

**Approach:**
1. Check the numbers. 82% of 500 is 410 passes, 87% is 435, so 25 more prompts pass. Unpaired z is about 2.2 (p about 0.03). Paired on the same prompts (illustrative: 45 fixed, 20 broken) gives McNemar p about 0.003. So the shift is probably real, but one weekly run has no noise estimate.
2. Get the noise floor. Rerun the suite many times on a fixed model. In my simulation two reruns differ by up to about 3.6 points at 95%, so a 5 point move is outside noise but not by a wide margin.
3. Confirm with the experiment's own data. Look for a break at the update time in the treatment-minus-control gap, latency and cost.
4. Split the analysis: pre-update period and post-update period, each with its own treatment-minus-control effect. Do not average them into one number.
5. Decide: if the post-update model is the one you will ship, the post-update period is the evidence, and it is shorter, so extend the test. If the effect changed sign or size, say so.
6. Prevent: pin a dated model version, log model version and prompt version on every request, run the regression suite daily, alert on version-string changes, and write a rule in the test plan that a change in treatment ends the readout window.

**Metrics:**
- Suite pass rate = prompts passed / 500, with several runs per period.
- Period effect = treatment mean - control mean within each period.
- Break check = difference in effect between periods, with a confidence interval.
- Guardrails: latency, cost per request, refusal rate, version-string counts.

**Risks:**
- Pooled averages mix two treatments. Illustrative: effect 0 in weeks 1-2 and +4 points in weeks 3-4 pools to +2.4 points, which describes neither model.
- The update may change style and cost as well as accuracy.
- Users may adapt (novelty) at the same time and confound the break.
- Pinning only works if the provider supports dated versions; otherwise rerun the suite on a schedule.

**What the interviewer scores:**
- Strong: treats the update as a change in the treatment, splits the periods, and gives a way to detect it (version logs, suite, break test).
- Strong: asks for the noise floor before reading 5 points.
- Weak: "average over the 4 weeks" or "restart" with no detection plan.
- Weak: assumes the suite shift is proof of a user-facing change.

**Example:** Illustrative weekly treatment-minus-control gaps (25,000 users per arm per week, baseline 30%): +0.45, 0.00, +4.30, +4.90 points. The pooled estimate is +2.41 points; the pre-update weeks give +0.23, the post-update weeks +4.60.
- Weak answer: "Four-week result is +2.4, ship." Strong answer: "That is a blend of two models. The current model shows about +4.6, from two weeks of data, so I extend the test on a pinned version."

**Code:**
```python
# Q53: provider silently updates the model two weeks into a 4-week test (illustrative)
import numpy as np
from scipy import stats
rng = np.random.default_rng(53)
print("500 prompts: 82% =", round(.82*500), "passes, 87% =", round(.87*500), "passes, difference", round(.87*500)-round(.82*500), "prompts")
assert round(.82*500) == 410 and round(.87*500) == 435
# unpaired two-proportion z (ignores that it is the same 500 prompts)
se = np.sqrt(.82*.18/500 + .87*.13/500); z = .05/se
print("unpaired z", round(z, 2), "p =", round(2*stats.norm.sf(z), 3))
# paired view: same prompts. Illustrative split of the 25 net gains: 45 fixed, 20 broken
fixed, broken = 45, 20
assert fixed - broken == 25
mc = stats.binomtest(fixed, fixed+broken, 0.5)
print("McNemar exact (45 fixed vs 20 broken): p =", round(mc.pvalue, 4))
# noise floor: same model, same suite, rerun with sampling temperature (each prompt passes with its own prob)
p_i = np.clip(rng.beta(1.2, 0.3, 500), 0, 1); p_i *= 0.82 / p_i.mean(); p_i = np.clip(p_i, 0, 1)
runs = np.array([rng.binomial(1, p_i).mean() for _ in range(2000)])
print("rerun noise on the SAME model: mean", round(runs.mean(), 3), "sd", round(runs.std(), 4), "-> 95% of reruns within +/-", round(1.96*runs.std()*np.sqrt(2), 3), "of each other")
assert 0.8 < runs.mean() < 0.84
# what the update does to the experiment readout: effect 0 in weeks 1-2, +4 points in weeks 3-4, control unchanged
N = 25_000                                    # users per arm per week
def week(eff):
    c = rng.binomial(N, 0.300)/N; t = rng.binomial(N, 0.300 + eff)/N; return t - c
effs = [week(0.0) for _ in (1, 2)] + [week(0.04) for _ in (3, 4)]
print("weekly treatment-minus-control (points):", [round(100*e, 2) for e in effs])
pooled = np.mean(effs)
print("pooled 4-week estimate:", round(100*pooled, 2), "points  | pre-update weeks:", round(100*np.mean(effs[:2]), 2), "| post-update weeks:", round(100*np.mean(effs[2:]), 2))
assert abs(np.mean(effs[:2])) < 0.01 and np.mean(effs[2:]) > 0.03 and 0.01 < pooled < 0.03
```

**Output (my run):**
```text
500 prompts: 82% = 410 passes, 87% = 435 passes, difference 25 prompts
unpaired z 2.19 p = 0.029
McNemar exact (45 fixed vs 20 broken): p = 0.0026
rerun noise on the SAME model: mean 0.815 sd 0.0129 -> 95% of reruns within +/- 0.036 of each other
weekly treatment-minus-control (points): [0.45, 0.0, 4.3, 4.9]
pooled 4-week estimate: 2.41 points  | pre-update weeks: 0.23 | post-update weeks: 4.6
```

**Follow-ups:**
- Why a fixed suite on the treatment path? It is a canary for model changes independent of user behaviour. Book 1 Part 10 Q55 (a test where the treatment is non-deterministic or changes mid-test) has the theory.
- What if the update made things worse? Same method: split, report the post-update effect, and decide on that. Roll back if the guardrails fail.
- Can I still use the first two weeks? Yes, as the evidence for the old model; they do not answer the question about the new one.

**Common mistakes:** Pooling across the update. Reading one weekly suite run as a precise number. Not logging the model version. Assuming control is unaffected without checking. Not extending the test on the new version.

### Q54 ⭐ 🔴 Two experiments reuse the same hash salt, so of 100,000 users, 45,000 are in treatment of both, 5,000 in treatment of A only, 5,000 in treatment of B only and 45,000 in control of both. Each experiment looks balanced on its own. Explain how this contaminates both results, how you detect a bucketing collision and what you do with the readouts.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
**Say this first (1 line):** Balanced is not the same as independent. With a shared salt the two experiments put almost the same users in treatment, so each readout contains the other experiment's effect, and I treat both readouts as contaminated until bucketing is fixed or I separate the effects from the four cells.

**Clarifying questions:**
- Are both experiments supposed to use independent hashing? If one platform rule says "same salt on purpose" (for example, nested tests), the story changes.
- Why are 10,000 users in a different state in A and B? Different allocation, a later ramp, or exclusions can explain a small gap even with a shared salt.
- Are the effects of A and B likely to add, or do they touch the same surface? It affects what I can recover.
- How long have they run, and can I restart with a new salt? Restarting is the clean answer.
- Has a decision already been made from these results? That sets how urgent the correction is.

**Approach:**
1. Check the arithmetic. Treatment of A is 45,000 + 5,000 = 50,000 and treatment of B is 5,000 + 45,000 = 50,000, so each is 50/50 and passes a normal SRM check.
2. Check independence. Independent assignment would give 25,000 users in each of the four cells. A chi-square test of A against B is about 64,000, and the correlation of the two flags is 0.8. P(B treated | A treated) = 90%, against 10% when A is control.
3. Explain the contamination. A user in A treatment is almost always in B treatment too. So A's naive readout is a + 0.8 b, and B's is b + 0.8 a, where a and b are the true effects (if effects add).
4. Detect the problem in general: run a cross-tab of every pair of concurrent experiments, run an A/A test on a pair of salts, compare hash outputs for correlation, and add a launch check that rejects reused salts.
5. Recover what you can. The two small cells (5,000 users each) separate the effects; fit `y ~ A + B` (and the interaction if there is a reason). Intervals are wider.
6. Fix and decide. Treat the old readouts as invalid for decisions, re-hash with new salts (or restart), and use the regression estimates only as a hint.

**Metrics:**
- Cell counts for each A x B combination; expected = row total x column total / grand total.
- Phi correlation of the two assignment flags = (n11 n00 - n10 n01) / sqrt(product of the four margins).
- Naive effect = mean(treated) - mean(control) for each experiment.
- Guardrails: SRM per experiment, pairwise overlap table per layer.

**Risks:**
- The joint regression assumes effects add. An interaction cannot be separated without more data in the small cells.
- The "A only" and "B only" cells may not be random (they may be users at a bucket boundary).
- Both experiments may have shipped decisions already.
- Rehashing mid-test mixes assignments; restart cleanly.

**What the interviewer scores:**
- Strong: spots that each is 50/50 yet jointly dependent, and quantifies it (0.8 correlation, a + 0.8 b).
- Strong: gives a detection method for the platform, not just for this case, and a recovery with its cost.
- Weak: "each experiment is balanced, so the results are fine".
- Weak: says to ignore the overlap because the effects are small.

**Example:** Illustrative effects: A adds 1.0, B adds 2.0, noise sd 10, 100,000 users in the stated cells. Naive A reads 2.67 +/- 0.12 (true 1.0, formula 1.0 + 0.8 x 2.0 = 2.6). Naive B reads 2.82 +/- 0.12 (true 2.0, formula 2.0 + 0.8 x 1.0 = 2.8). A joint regression gives A 1.14 +/- 0.21 and B 1.91 +/- 0.21: close to truth, with an interval about 1.7 times wider than the naive one.
- Weak answer: "Both are 50/50, so both are fine." Strong answer: "A and B are 80% correlated, so each readout carries the other's effect. I fit both flags together, and I re-salt before the next test."

**Code:**
```python
# Q54: two experiments sharing a hash salt (illustrative simulation of the stated counts)
import numpy as np
from scipy import stats
rng = np.random.default_rng(54)
# stated counts
tab = np.array([[45_000, 5_000],      # row A control:   B control 45,000 | B treatment 5,000 (B only)
                [5_000, 45_000]])     # row A treatment: B control 5,000 (A only) | B treatment 45,000 (both)
assert tab.sum() == 100_000 and tab[1].sum() == 50_000 and tab[:, 1].sum() == 50_000     # each looks 50/50 alone
chi2, p, *_ = stats.chi2_contingency(tab, correction=False)
phi = (tab[0,0]*tab[1,1] - tab[0,1]*tab[1,0]) / np.sqrt(tab.sum(0).prod() * tab.sum(1).prod())
print("independent assignment would give 25,000 per cell. chi-square", round(chi2, 0), "p =", p, " phi =", round(phi, 2))
assert abs(phi - 0.8) < 1e-9
print("P(B treated | A treated) =", tab[1,1]/tab[1].sum(), " P(B treated | A control) =", tab[0,1]/tab[0].sum())
# build users and outcomes: true effects A=+1.0, B=+2.0 (additive), noise sd 10
cells = np.repeat([0, 1, 2, 3], [45_000, 5_000, 5_000, 45_000])        # 0 ctrl/ctrl, 1 B only, 2 A only, 3 both
a = np.isin(cells, [2, 3]); b = np.isin(cells, [1, 3])
y = 50 + 1.0*a + 2.0*b + rng.normal(0, 10, 100_000)
def diff(g):
    d = y[g].mean() - y[~g].mean(); se = np.sqrt(y[g].var()/g.sum() + y[~g].var()/(~g).sum()); return d, 1.96*se
print("naive readout A: %.2f +/- %.2f (true 1.0)   naive readout B: %.2f +/- %.2f (true 2.0)" % (*diff(a), *diff(b)))
assert abs(diff(a)[0] - (1.0 + 0.8*2.0)) < 0.5 and abs(diff(b)[0] - (2.0 + 0.8*1.0)) < 0.5      # a + 0.8 b, b + 0.8 a
# recover with the 2x2 cells (regression on both flags)
X = np.column_stack([np.ones(len(y)), a, b]).astype(float)
beta, *_ = np.linalg.lstsq(X, y, rcond=None); r = y - X@beta
se = np.sqrt(np.diag((r@r/(len(y)-3)) * np.linalg.inv(X.T@X)))
print("joint regression: A %.2f +/- %.2f, B %.2f +/- %.2f" % (beta[1], 1.96*se[1], beta[2], 1.96*se[2]))
assert abs(beta[1]-1.0) < 2*1.96*se[1] and abs(beta[2]-2.0) < 2*1.96*se[2]
print("CI width of A, naive vs joint:", round(2*diff(a)[1], 2), "vs", round(2*1.96*se[1], 2))
```

**Output (my run):**
```text
independent assignment would give 25,000 per cell. chi-square 64000.0 p = 0.0  phi = 0.8
P(B treated | A treated) = 0.9  P(B treated | A control) = 0.1
naive readout A: 2.67 +/- 0.12 (true 1.0)   naive readout B: 2.82 +/- 0.12 (true 2.0)
joint regression: A 1.14 +/- 0.21, B 1.91 +/- 0.21
CI width of A, naive vs joint: 0.25 vs 0.41
```

**Follow-ups:**
- Does this show up in a standard SRM check? No. SRM checks each experiment's split, which is fine here.
- How do platforms avoid it? A unique salt per experiment, layers for mutual exclusion, and an automated overlap check at launch. See Book 1 Part 10 Q53 (debugging an experiment platform that gives wrong results) for the theory.
- If the effects are tiny, can I ignore it? Only after the cross-tab and a regression show it is tiny. The gap is largest when one effect is big.

**Common mistakes:** Running only an SRM check. Reading each experiment alone. Reusing a salt to "save" a bucket. Fixing it by reweighting without a model. Shipping on the contaminated readouts.

### Q55 ⭐ 🔴 An uplift model ranks 1,000,000 users, the top 20% (200,000) get a coupon, and the team compares their conversion to the other 800,000 who got none and reports +15% relative. Explain why this does not validate the model, and how you would design a randomized evaluation with holdouts and an uplift curve.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
**Say this first (1 line):** The coupon group was picked by the model, so it differs from the rest before any coupon is sent. To validate an uplift model I need random assignment of the coupon, with holdouts, and I look at the incremental conversions by score, not at who converts.

**Clarifying questions:**
- What does the model score: probability of converting, or the increase in probability from a coupon? A propensity model picks people who buy anyway.
- Did the 800,000 get no coupon for a reason (suppressed, or ineligible)? That is more selection.
- What is the coupon cost and the margin per conversion? Uplift only matters if the incremental conversions pay for the discount.
- Is there any past randomized coupon data? It is the cheapest way to train and check an uplift model.
- Can we hold out part of the top 20%? That is the core of the redesign.

**Approach:**
1. Say why it fails. The top 20% were chosen by the model; the other 80% were not. If the model ranks people by how likely they are to buy, the top group converts more with no coupon at all. A +15% gap is exactly what a model with zero uplift can produce. It can also hide a real uplift, if the model picks people with lower baseline. The direction is not knowable from this comparison.
2. Define the right quantity: uplift = conversion with the coupon - conversion without it, for the same kind of user. Only randomization gives the "without" group.
3. Design the evaluation. Draw a random sample (or use a holdout across the whole base), score everyone, and randomly give or withhold the coupon, independent of the score. Within each score decile compare treated with untreated.
4. Draw the uplift curve (Qini-style): sort by score, and plot cumulative incremental conversions as more of the base is targeted. A good model rises fast; a propensity model with no uplift is flat.
5. In production keep a random holdout inside the targeted group (for example 10% of the top 200,000) and a small random holdout in the rest. This gives a live check of both the incremental effect and the ranking.
6. Decide with money: incremental conversions x margin - coupon cost for the group targeted, and pick the cutoff where it turns negative. Book 1 Part 10 Q34 (how to evaluate an uplift model offline and online) covers the theory.

**Metrics:**
- Uplift (decile) = treated conversion rate - control conversion rate, within the decile.
- Incremental conversions at depth k = sum of uplift x decile size over the top deciles.
- Naive relative gap = conversion(top, coupon) / conversion(rest, no coupon) - 1.
- Guardrails: coupon cost per incremental conversion, margin, holdout size and balance check.

**Risks:**
- Withholding coupons from a holdout costs some sales. Size it (below: 10% of the top group).
- Uplift by decile is noisy at small sizes; use enough users per decile or smooth the curve.
- Customers can learn about coupons; long-term effects (waiting for a coupon) are not in a one-week read.
- Training and evaluating on the same randomized data overfits. Hold out part.

**What the interviewer scores:**
- Strong: says why the naive gap is confounded, and that it can overstate or understate.
- Strong: gives a randomized design with holdouts and defines the uplift curve and a money cutoff.
- Weak: "compare top 20% to the rest, but control for covariates".
- Weak: judges the model by conversion rate or AUC.

**Example:** Illustrative: 1,000,000 users; the top 20% convert at 5.75% and the rest at 5.0% with no coupon at all. Giving the top group a coupon that does nothing still yields +15% relative (simulated: +15.8%). With a randomized 400,000-user sample, uplift by decile is +2.10 points in the top decile, about +0.9 in deciles 8 and 7, and about zero below. Incremental conversions: about 2,100 per million for the top decile, about 4,000 for the top three, and the curve flattens after that.
- Weak answer: "Conversion is 15% higher in the group we targeted, the model works." Strong answer: "That gap is there without the coupon. I randomize the coupon inside score bands and read the uplift curve."

**Code:**
```python
# Q55: uplift model "validated" by comparing treated top 20% with untreated rest (illustrative simulation)
import numpy as np
rng = np.random.default_rng(55)
N = 1_000_000; TOP = 200_000
print("naive claim from stated counts: top 20% =", TOP, " rest =", N - TOP)
# Scenario 1: the model really ranks by who buys anyway (propensity), true coupon uplift is ZERO for everyone
score = rng.random(N); top = np.zeros(N, bool); top[np.argsort(-score)[:TOP]] = True
base = np.where(top, 0.0575, 0.05)              # top users already convert a bit more
conv = rng.random(N) < base                      # coupon changes nothing
naive = conv[top].mean() / conv[~top].mean() - 1
print("coupon has NO effect, yet naive comparison reads", f"{100*naive:+.1f}%", " (top converts", round(conv[top].mean(), 4), "vs rest", round(conv[~top].mean(), 4), ")")
assert abs(naive - 0.15) < 0.02
# Scenario 2: randomised evaluation sample. Model has real uplift signal: uplift rises with score decile
M = 400_000
sc = rng.random(M); dec = np.minimum((sc * 10).astype(int), 9)          # decile 9 = model's top
base = 0.05 + 0.002 * (9 - dec)                        # high-score users are NOT the highest-baseline here
uplift = np.where(dec == 9, 0.020, np.where(dec == 8, 0.012, np.where(dec == 7, 0.006, 0.0)))
treat = rng.random(M) < 0.5                            # coupon assigned by coin flip, ignoring the score
y = rng.random(M) < base + uplift * treat
print("decile | n | treated conv | control conv | uplift (pts)")
up = []
for d in range(9, -1, -1):
    m = dec == d; t, c = y[m & treat].mean(), y[m & ~treat].mean(); up.append(t - c)
    print(f"{d:>6} | {m.sum():>6} | {t:.4f} | {c:.4f} | {100*(t-c):+.2f}")
# uplift (Qini-style) curve: cumulative incremental conversions if we treat the top k deciles
inc = []
tot = 0.0
for d in range(9, -1, -1):
    m = dec == d
    n_t, n_c = (m & treat).sum(), (m & ~treat).sum()
    tot += (y[m & treat].sum() / n_t - y[m & ~treat].sum() / n_c) * m.sum()
    inc.append(tot)
print("incremental conversions per 1,000,000 users if we treat top k deciles (scaled):",
      [round(v * 1_000_000 / M) for v in inc])
assert up[0] > up[2] > 0.0 and up[0] > 0.012 and abs(up[5]) < 0.006
# hold-out sizing: top 20% (200,000) with 10% randomly held out
n_h = 20_000; n_t = 180_000; p = 0.0575
se = np.sqrt(p*(1-p)*(1/n_t + 1/n_h))
print("SE of treated-minus-holdout with a 10% holdout of the top 200,000:", round(100*se, 3), "points -> detectable effect at 80% power about", round(100*2.8*se, 2), "points")
assert 0.0015 < se < 0.002
```

**Output (my run):**
```text
naive claim from stated counts: top 20% = 200000  rest = 800000
coupon has NO effect, yet naive comparison reads +15.8%  (top converts 0.0575 vs rest 0.0496 )
decile | n | treated conv | control conv | uplift (pts)
     9 |  39985 | 0.0718 | 0.0508 | +2.10
     8 |  39939 | 0.0622 | 0.0529 | +0.93
     7 |  39901 | 0.0618 | 0.0523 | +0.94
     6 |  40158 | 0.0548 | 0.0557 | -0.09
     5 |  40231 | 0.0595 | 0.0568 | +0.27
     4 |  39984 | 0.0612 | 0.0607 | +0.05
     3 |  39900 | 0.0626 | 0.0614 | +0.12
     2 |  39845 | 0.0637 | 0.0630 | +0.08
     1 |  39949 | 0.0652 | 0.0656 | -0.05
     0 |  40108 | 0.0684 | 0.0707 | -0.24
incremental conversions per 1,000,000 users if we treat top k deciles (scaled): [2098, 3023, 3964, 3877, 4151, 4204, 4328, 4406, 4358, 4122]
SE of treated-minus-holdout with a 10% holdout of the top 200,000: 0.174 points -> detectable effect at 80% power about 0.49 points
```

**Follow-ups:**
- How big a holdout? With a 10% random holdout in the top 200,000 the standard error of the difference is about 0.17 points, so effects around 0.5 points are detectable at 80% power.
- Can I fit the uplift model on the non-randomized data? Only with strong assumptions (no hidden confounders). Randomized data is safer.
- What is an uplift curve versus a gains curve? A gains curve counts conversions; an uplift curve counts incremental conversions, which is the thing the coupon pays for.

**Common mistakes:** Comparing targeted with untargeted. Judging an uplift model by conversion. Giving everyone in the top group the coupon with no holdout. Ignoring coupon cost. Reading small deciles as precise.

