### Q1 ⭐⭐⭐ 🟢 A test meant to split 100,000 users 50/50 ended with 52,000 in control and 48,000 in treatment. Treatment shows conversion of 5.0% against 4.8% for control (0.2 percentage points absolute, about 4% relative to control's 4.8%) with p = 0.03, and the product manager wants to ship today. Explain what you check first and what you tell the manager.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I do not ship today, because a 52,000 / 48,000 split of a 50/50 test is a sample ratio mismatch (SRM, the arm sizes do not match the design), so the assignment or logging is broken and the 0.2-point gap cannot be trusted.

**Clarifying questions:**
- Was the intended split exactly 50/50, and did it change mid-test? A ramp or a config change makes a ratio mismatch expected, not a bug.
- Are the counts users assigned or users who triggered or loaded the page? Losing users after assignment (crash, slow load, redirect) is the classic SRM cause.
- Is the mismatch the same every day? A constant mismatch points to a code path. A one-day jump points to a deployment or an outage.
- Does the split differ by platform, country or browser? It tells me where the loss happens.
- How was the p-value of 0.03 computed (which test, which counts)? I want to reproduce it before I defend or reject it (see the prompt note below).

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
- "The effect is small, so the bias is small" is wrong. A 2,000-user hole can wipe out a 0.2-point gap.
- Fixing the ratio by deleting users from the bigger arm just hides the bug.
- Pressure to ship because the p-value looks good.

**What the interviewer scores:**
- Strong: names SRM first and runs the chi-square before reading any lift. Weak: starts discussing whether 4% relative is big enough.
- Strong: gives a list of causes and a way to localise them (by day, platform, path). Weak: "rerun the test" with no diagnosis.
- Strong: explains why the gap is untrustworthy (differential loss, selection). Weak: "the sample is still big, so it is fine."
- Strong: tells the manager something clear and non-blocking: what I will do and by when. Weak: a lecture on p-values.

**Example:** (illustrative numbers) The design is 50,000 per arm. Observed is 52,000 control and 48,000 treatment: chi-square = 2 x 2,000^2 / 50,000 = 160. Now suppose a bug dropped 2,000 treated users who convert at only 1% (slow-device users). Add them back and treatment is (2,400 + 20) / 50,000 = 4.84%, against control 4.80%: the gap shrinks from 0.20 to 0.04 points. Weak answer: "p = 0.03, 4% lift, ship it." Strong answer: "SRM fails at p near 1e-36, so I do not read the lift until I find where 4,000 users went."

**Prompt note (Q1):** the prompt says treatment 5.0% against control 4.8% gives p = 0.03. Recomputed from the stated counts (2,400 of 48,000 against 2,496 of 52,000), the two-sided p is 0.143 and the one-sided p is 0.072. So the p = 0.03 does not follow from these numbers. The answer does not change (SRM comes first), but I would tell the manager that even ignoring SRM the gap is not significant.

**Code:**
```python
import numpy as np
from scipy import stats

# Illustrative numbers from the prompt
n_c, n_t = 52_000, 48_000
x_c, x_t = round(0.048 * n_c), round(0.050 * n_t)   # conversions: 2496 and 2400

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
print(f"z = {z:.2f}, two-sided p = {p_two:.3f}, one-sided p = {stats.norm.sf(z):.3f}")
assert p_two > 0.10          # the prompt's p = 0.03 does NOT follow from these counts

# 3) Chance that a fair 50/50 split ever looks like 52,000 / 48,000
print("P(|diff| >= 2000 under fair split) =", 2 * stats.binom.cdf(48_000, 100_000, 0.5))

# 4) Why the SRM matters. The treatment arm is 2,000 short of 50,000. Suppose those 2,000
#    were low converters (illustrative: 1.0%) dropped by a bug. Treatment with them restored:
lost = 2_000
rate_full = (x_t + lost * 0.01) / (n_t + lost)
gap = rate_full - p_c
print(f"treatment rate with the 2,000 restored: {rate_full:.4f}; gap to control: {gap*100:.2f} points")
assert abs(gap) < 0.0005     # the 0.2-point gap shrinks to about 0.04 points
```

**Output (my run):**
```text
SRM chi2 = 160.0  p = 1.1314837902433038e-36
conversion control 0.0480, treatment 0.0500, diff 0.0020
z = 1.46, two-sided p = 0.143, one-sided p = 0.072
P(|diff| >= 2000 under fair split) = 1.1530938666727834e-36
treatment rate with the 2,000 restored: 0.0484; gap to control: 0.04 points
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

### Q8 ⭐⭐⭐ 🟡 A team measures click-through rate as total clicks divided by total impressions and runs a two-proportion z-test over 2,000,000 impressions per arm, getting p < 0.001 for a lift from 4.00% to 4.05%. Those impressions come from only 100,000 users per arm (20 per user on average), and the user-level analysis gives p = 0.12. Explain why the two disagree and how you would analyse the metric properly.
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
2. Measure the inflation: with intra-user correlation rho and 20 impressions per user, the variance inflates by the design effect 1 + (m - 1) x rho. A user-level p of 0.12 against a pooled p near 0.011 implies a design effect of about 2.7 (rho about 0.09), see Code.
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

**Example:** (illustrative numbers) 100,000 users per arm, 20 impressions each. Control 4.00%, treatment 4.05%: the pooled z-test gives z = 2.54, p = 0.011. A user-level p of 0.12 means z = 1.55, so the variance is (2.54 / 1.55)^2 = 2.7 times larger than the pooled test assumed. With rho = 0.09, that matches 1 + 19 x 0.088. Weak answer: "p < 0.001, ship it." Strong answer: "The pooled test pretends that impressions are independent. At user level, it is not significant."

**Prompt note (Q8):** the prompt says the pooled impression-level test gives p < 0.001. For 4.00% against 4.05% on 2,000,000 impressions per arm the pooled two-proportion z-test gives z = 2.54 and p = 0.011, not below 0.001. The conclusion is unchanged (the pooled p is too small and the user-level p = 0.12 is the right one), but the quoted pooled p is wrong.

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
assert 0.005 < p_naive < 0.02            # NOT p < 0.001 as the prompt says

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
- Treating "p < 0.001" with millions of rows as strong evidence.
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
