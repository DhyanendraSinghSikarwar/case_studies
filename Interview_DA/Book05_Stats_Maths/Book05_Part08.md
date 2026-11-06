# Book 5 — Statistics & Maths for Data Analysts | Part 8: A/B Testing for Analysts 🟡🔴

**Target:** 40 questions | **Actual:** 43 questions
**Scope:** A/B testing as a data analyst uses it: hypotheses, design, metrics, sample size and power, significance, common pitfalls (peeking, SRM, novelty) and how to explain results.

### Q1 ⭐⭐⭐ 🟢 What is A/B testing? Explain it to a non-technical manager.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you explain an experiment in plain words without jargon?
**Say this in the interview:** "An A/B test is a fair comparison. We split people at random into two groups, show one group the current version (A) and the other the new version (B), and then compare one agreed result, such as how many people complete a purchase. Because the split is random, any real difference can be credited to the change."
**Explain simply:**
- It is like testing a new interview-reminder email: half of candidates get the old email, half get the new one, at the same time.
- Running both at the same time matters; comparing "this month vs last month" would mix in festivals, hiring seasons and other changes.
- We still need statistics, because two random groups will never match exactly. The test tells us whether the gap is bigger than normal random wobble.
**Worked example:** Version A converts 200 of 2,000 visitors (10%) and version B converts 240 of 2,000 (12%). B looks better; the test (see Q8) checks whether 2 points is more than luck.
**Likely follow-ups:**
1. *Is it only for websites?* No; any change you can apply to one random group and not another, such as an HR message, works.
2. *Why not just ask people which version they prefer?* What people say and what they do often differ; the test measures behaviour.
**Common mistakes:** Comparing before vs after and calling it an A/B test; running the two versions on different days; not deciding the success metric before starting.

### Q2 ⭐⭐⭐ 🟢 What are the control group and the treatment group in an A/B test?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Basic vocabulary, and that you know the control is the fair baseline.
**Say this in the interview:** "The control group sees the current experience and the treatment group sees the change. Everything else is kept the same, so the control tells us what would have happened anyway."
**Explain simply:**
- Control (also called A or baseline): no change. Treatment (also called B or variant): gets the new thing.
- The control is what lets us say "the change caused this" rather than "this happened by itself".
- Both groups should be the same size where possible, run over the same dates, and be measured the same way.
**Worked example:** HR sends a new reminder SMS to 400 interview candidates (treatment) and the usual email only to another 400 (control). If no-shows are 16% vs 22.5% (see Q14), the control's 22.5% is the "normal" level we compare against.
**Likely follow-ups:**
1. *Can the control receive nothing at all?* Yes, if "nothing" is the real current state, for example no reminder.
2. *What if the control group also changes over time?* That is fine; both change together, which is why we compare them rather than compare to the past.
**Common mistakes:** Treating "control" as a group that gets a bad experience (it is simply the current one); letting people choose their group.

### Q3 ⭐⭐⭐ 🟢 Why do we randomly assign users to the control and treatment groups?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand confounding (hidden differences between groups)?
**Say this in the interview:** "Random assignment makes the two groups alike on average, including things I cannot see or measure. So the only systematic difference between them is the change I made."
**Explain simply:**
- Without randomisation, groups differ for other reasons (a confounder is a hidden factor that affects both the group and the result).
- Example: employees who choose to join a wellness programme are probably already more engaged. Comparing them with non-joiners overstates the programme's effect (this is called selection bias).
- Randomisation does not make groups identical in every sample, just fair in the long run; the p-value accounts for that leftover chance.
**Worked example:** Suppose 1,000 employees; the engaged 200 volunteer for the programme and 2 of them leave (1%), while 16 of the other 800 leave (2%). The programme looks great, but the engaged were already less likely to leave. A coin-flip split would put engaged people in both groups equally.
**Likely follow-ups:**
1. *How do you check randomisation worked?* Compare group sizes (see SRM, Q29) and key traits such as device, region or tenure.
2. *What if you cannot randomise?* See Q43 for quasi-experiments.
**Common mistakes:** Assigning by "first half of the day" or by region and calling it random; letting users self-select.

### Q4 ⭐⭐⭐ 🟢 What are the null and alternative hypotheses in an A/B test? Give an example.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you state the testing logic correctly?
**Say this in the interview:** "The null hypothesis says the change has no effect: the two conversion rates are really equal. The alternative says they differ. I start by assuming the null and ask how surprising my data would be if it were true."
**Explain simply:**
- Null hypothesis (H0): no real difference; any gap is random chance.
- Alternative hypothesis (H1): there is a real difference (two-sided) or B is higher (one-sided; see Q21).
- We never "prove" H1; we either reject H0 (the data is too surprising under H0) or fail to reject it.
**Formula in plain words:** H0: conversion rate of B minus conversion rate of A equals zero. In symbols: H0: p_B - p_A = 0, H1: p_B - p_A ≠ 0.
**Worked example:** Checkout test. H0: the new button and the old button have the same true conversion rate. H1: the two true rates differ. Data: 10% vs 12%; the p-value of 0.043 (Q8) says such a gap would show up about 4% of the time if H0 were true, so we reject H0 at the 5% level.
**Likely follow-ups:**
1. *Why not set H1 as "B is better"?* You can (one-sided), but only if a drop would lead to the same decision as no change.
**Common mistakes:** Saying "we accept the null" when p is high (we only failed to find evidence); writing hypotheses after seeing the data.

### Q5 ⭐⭐⭐ 🟡 How would you design an A/B test end to end for a new website checkout page?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you structure a whole experiment, not only run a formula?
**Say this in the interview:** "I follow a fixed order: goal and hypothesis, metrics, who and how to randomise, sample size and duration, launch checks, analysis, decision. I decide all of it before looking at results."
**Explain simply:**
1. **Hypothesis:** "A shorter one-page checkout will raise the share of visitors who complete a purchase."
2. **Metrics:** primary metric = checkout completion rate; guardrails = refund rate, payment failures, page load time (Q6, Q17).
3. **Unit and split:** randomise by user (logged-in id or cookie) 50/50 (Q23, Q34), only users who reach checkout.
4. **Sample size:** from baseline rate, smallest lift worth detecting, 5% significance, 80% power (Q10). Convert to days using daily traffic, then round up to whole weeks (Q18).
5. **Pre-launch checks:** confirm tracking works; an A/A test if the setup is new (Q31).
6. **During the test:** monitor for bugs and the split ratio (SRM, Q29), but do not stop early on a good p-value (Q11).
7. **Analysis:** test the primary metric, give the confidence interval (Q20), check guardrails, then decide and document.
**Worked example:** Baseline completion 10%, aim to detect 10% to 12%: about 3,839 users per group, 7,678 total (see Q10). With 1,000 checkout visitors a day that is about 8 days, so run 14 days (two full weeks).
**Likely follow-ups:**
1. *What if the result is flat?* See Q25.
**Common mistakes:** Skipping the sample-size step; changing the metric after seeing results; testing on all visitors instead of those who actually see checkout (dilutes the effect).

### Q6 ⭐⭐⭐ 🟡 How do you choose the primary metric and the guardrail metrics for an A/B test?
**Asked at:** commonly asked (no company-specific report found); the sources note guardrail and metric questions as a recurring pattern in product-analyst style rounds.
**What the interviewer is checking:** Do you link the metric to the business goal and protect against harm?
**Say this in the interview:** "The primary metric is the one number that decides success, tied directly to what the change is meant to improve. Guardrails are things that must not get worse, such as refunds or speed. I fix both before launch."
**Explain simply:**
- Good primary metric: tied to the goal, sensitive enough to move in the test period, measurable per user, hard to game. Pick one; many "primary" metrics create the multiple-comparisons problem (Q22).
- Guardrail metric: a safety check, for example cancellations, complaints, load time, unsubscribe rate.
- Avoid vanity metrics (clicks, page views) when the real goal is revenue or retention; if the true goal is slow (annual retention), use a faster proxy that is known to predict it.
**Worked example (HR):** Test a new job-application form. Primary: applications completed per visitor. Guardrails: share of applicants who meet the minimum criteria (quality), time to complete, and form errors. If completions rise but qualified share falls, the form simply attracted more unsuitable applicants.
**Likely follow-ups:**
1. *How many guardrails?* A handful (3 to 5) that really matter.
**Common mistakes:** Picking the metric after seeing which one moved; choosing a metric the change cannot plausibly affect; no guardrails at all.

### Q7 ⭐⭐⭐ 🟡 What does the p-value mean in an A/B test result, and what does it not mean?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** The most-misquoted idea in statistics; do you state it correctly?
**Say this in the interview:** "The p-value is the chance of seeing a difference at least this large if the change actually did nothing. It is not the probability that the change works."
**Explain simply:**
- Small p-value: our data would be unusual in a "no effect" world, so we doubt the "no effect" idea.
- The usual cut-off (significance level, alpha) is 0.05, a convention not a law.
- It does NOT mean: "95% chance B is better", "the effect is big", or "the result will repeat".
- It says nothing about size: with huge traffic, a tiny useless lift can have a tiny p-value.
**Worked example:** A 10% vs 12% test with 2,000 per group gives p = 0.043. Meaning: if A and B truly converted the same, a gap this big would appear about 4.3 times in 100 experiments. Not meaning: "there is a 95.7% chance B is better".
**Excel / Python:**
```python
from scipy import stats

# Number of visitors and conversions for each version
visitors_per_version = 2000
conversions_a = 200
conversions_b = 240

# Pooled rate: expected rate for both versions if nothing really differs
pooled_rate = (conversions_a + conversions_b) / (2 * visitors_per_version)

# Standard error: typical random wobble in the gap between two rates
standard_error = (pooled_rate * (1 - pooled_rate) * 2 / visitors_per_version) ** 0.5

# z-score: how many wobbles apart the two rates are
z_score = (conversions_b / visitors_per_version - conversions_a / visitors_per_version) / standard_error

# Two-sided p-value from the normal curve
p_value = 2 * stats.norm.sf(abs(z_score))
print("z-score:", round(z_score, 3))
print("p-value:", round(p_value, 4))
```
Output: `z-score: 2.021`, `p-value: 0.0432`. The gap is about 2 wobbles wide, which would happen roughly 4% of the time by luck alone.
**Likely follow-ups:**
1. *What does p = 0.5 mean?* The data is very ordinary under "no effect"; it does not prove there is no effect.
**Common mistakes:** "p = 0.03 means 97% sure"; treating p = 0.049 and p = 0.051 as completely different; ignoring effect size.

### Q8 ⭐⭐⭐ 🟡 Version A converted 200 of 2,000 visitors and version B converted 240 of 2,000. Is B really better? Walk through the test.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you run a two-proportion z-test and interpret it honestly?
**Say this in the interview:** "B converts at 12% vs 10%, a 2-point gap. The two-proportion z-test gives p about 0.043, so it is significant at 5%, but only just. The confidence interval runs from about 0.06 to 3.9 points, so the true lift could be tiny. I'd call it promising, and check cost, guardrails and whether to confirm with more data."
**Explain simply:**
- Step 1, hypotheses: H0 no difference, H1 a difference.
- Step 2, rates: A = 200/2000 = 10%, B = 240/2000 = 12%.
- Step 3, pooled rate (assume no difference, so combine): 440/4000 = 11%.
- Step 4, standard error (random wobble of the gap) about 0.0099.
- Step 5, z = 0.02 / 0.0099 = 2.02; p = 0.043.
- Step 6, interval: 2 points ± 1.96 × 0.0099 gives about 0.06 to 3.94 points.
**Formula in plain words:** z = (rate B minus rate A) divided by the standard error of the gap. Symbols: z = (p_B - p_A) / sqrt(p(1-p)(1/n_A + 1/n_B)), where p is the pooled rate.
**Excel / Python:**
```python
import math
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest

# Raw counts
visitors_a, conversions_a = 2000, 200
visitors_b, conversions_b = 2000, 240

# Conversion rate of each version
rate_a = conversions_a / visitors_a
rate_b = conversions_b / visitors_b

# Pooled rate and standard error under "no difference"
pooled_rate = (conversions_a + conversions_b) / (visitors_a + visitors_b)
standard_error = math.sqrt(pooled_rate * (1 - pooled_rate) * (1 / visitors_a + 1 / visitors_b))

# z-score and two-sided p-value
z_score = (rate_b - rate_a) / standard_error
p_value = 2 * stats.norm.sf(abs(z_score))

# 95% confidence interval for the gap (each rate has its own spread here)
standard_error_gap = math.sqrt(rate_a * (1 - rate_a) / visitors_a + rate_b * (1 - rate_b) / visitors_b)
gap = rate_b - rate_a
lower_limit = gap - 1.96 * standard_error_gap
upper_limit = gap + 1.96 * standard_error_gap

print("pooled rate:", pooled_rate)
print("standard error:", round(standard_error, 5))
print("z-score:", round(z_score, 3), " p-value:", round(p_value, 4))
print("95% CI for gap (points):", round(lower_limit * 100, 2), "to", round(upper_limit * 100, 2))

# Cross-check with a ready-made library function
z_check, p_check = proportions_ztest([conversions_b, conversions_a], [visitors_b, visitors_a])
print("library check:", round(z_check, 3), round(p_check, 4))
```
Output: pooled rate `0.11`, standard error `0.00989`, `z-score: 2.021  p-value: 0.0432`, interval `0.06 to 3.94` points, library check `2.021 0.0432`. Significant, but the low end of the interval is almost zero.
Excel (version 2010+; not run in Excel here): put pooled rate in B1 `=(200+240)/4000`, standard error in B2 `=SQRT(B1*(1-B1)*(1/2000+1/2000))`, z in B3 `=(240/2000-200/2000)/B2` (returns 2.02), p-value in B4 `=2*(1-NORM.S.DIST(ABS(B3),TRUE))` (returns 0.043).
**Likely follow-ups:**
1. *Is B "really" better?* Probably, but the evidence is modest; p = 0.043 is near the cut-off and power was only about 52% (Q15).
**Common mistakes:** Saying "B is 20% better, so yes" without a test; quoting p without the interval; forgetting the sample was small for this effect.

### Q9 ⭐⭐⭐ 🟡 An A/B test shows a 2% lift with a p-value of 0.03. Would you ship the change?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you separate statistical significance from practical importance and risk?
**Say this in the interview:** "Not automatically. First I'd clarify whether 2% is relative or absolute, then look at the confidence interval, guardrails, the cost of shipping, and whether the test ran its planned length. Significance says the lift is probably not zero; it does not say it is worth it."
**Explain simply:**
- Ask: is the lift 2 percentage points, or 2% relative (10% to 10.2%)? These are very different (Q13).
- Look at the interval: p = 0.03 means the 95% interval just excludes zero, so the true lift may be much smaller.
- Check guardrails, segments for obvious breakage, novelty (Q19), and that the test was not stopped early (Q11).
- Weigh benefit against cost: engineering effort, complexity, user experience.
**Worked example:** If 2% is relative on a 10% baseline (10.0% to 10.2%) and p = 0.03, the test must have had about 213,800 visitors per group, and the 95% interval is roughly 0.02 to 0.38 points. With 1,000,000 visitors a month and Rs 500 per order, 0.2 points extra is 2,000 orders, about Rs 10,00,000 a month; worth shipping if cheap, not if it needs months of engineering. If instead 2% is 2 points, about 2,300 per group suffices and it is a bigger, rarer win.
**Excel / Python:**
```python
from scipy import stats

# Lift described as a 2% RELATIVE gain on a 10% baseline
baseline_rate = 0.10
variant_rate = 0.102
p_value = 0.03

# z-score implied by that p-value, and the standard error that goes with it
z_score = stats.norm.isf(p_value / 2)
standard_error = (variant_rate - baseline_rate) / z_score

# Visitors per group needed to get such a small standard error
variance_sum = baseline_rate * (1 - baseline_rate) + variant_rate * (1 - variant_rate)
visitors_per_group = variance_sum / standard_error ** 2

# 95% interval for the gap, in percentage points
lower_limit = (variant_rate - baseline_rate - 1.96 * standard_error) * 100
upper_limit = (variant_rate - baseline_rate + 1.96 * standard_error) * 100

print("z-score:", round(z_score, 3))
print("visitors per group:", round(visitors_per_group))
print("95% interval (points):", round(lower_limit, 3), "to", round(upper_limit, 3))
```
Output: `z-score: 2.17`, `visitors per group: 213797`, `95% interval (points): 0.019 to 0.381`. A tiny effect can be "significant" with big traffic; decide on business value.
**Likely follow-ups:**
1. *And if p were 0.20?* Not significant; we cannot rule out chance, so no evidence to ship on this data alone (Q25).
**Common mistakes:** Equating "significant" with "important"; not asking about relative vs absolute; ignoring cost.

### Q10 ⭐⭐⭐ 🟡 How do you calculate the sample size needed for an A/B test?
**Asked at:** commonly asked (no company-specific report found); sample size, MDE and power are a recurring topic in the prep sources.
**What the interviewer is checking:** Do you know the four inputs and how each moves the answer?
**Say this in the interview:** "I need four things: the baseline rate, the smallest lift worth detecting (MDE), the significance level (usually 5%) and the power (usually 80%). A formula or calculator then gives users per group. Smaller lifts need many more users."
**Explain simply:**
- Baseline rate: what control converts at today.
- MDE (minimum detectable effect): the smallest lift that would change a decision (Q16).
- Significance level (alpha) 0.05: tolerated false-alarm rate (Q12).
- Power 0.80: chance of catching a real effect of that size (Q15).
- Halving the MDE roughly quadruples the sample, because the effect is squared in the formula.
**Formula in plain words:** users per group = (z for alpha + z for power) squared, times (sum of the two groups' p(1-p)), divided by (difference in rates) squared. Symbols: n = (z_(α/2) + z_β)^2 × [p1(1-p1) + p2(1-p2)] / (p2 - p1)^2.
**Worked example:** Baseline 10%, want to detect 12%: n is about 3,839 per group (7,678 total). Detecting 11% instead needs about 14,749 per group.
**Excel / Python:**
```python
import math
from scipy import stats

# Inputs
baseline_rate = 0.10
target_rate = 0.12
significance_level = 0.05
power = 0.80

# z-values: 1.96 for 5% two-sided, 0.84 for 80% power
z_alpha = stats.norm.ppf(1 - significance_level / 2)
z_power = stats.norm.ppf(power)

# Combined spread of the two rates, and the gap we want to detect
variance_sum = baseline_rate * (1 - baseline_rate) + target_rate * (1 - target_rate)
gap = target_rate - baseline_rate

# Visitors needed per group (round up)
visitors_per_group = (z_alpha + z_power) ** 2 * variance_sum / gap ** 2
print("z for alpha:", round(z_alpha, 3), " z for power:", round(z_power, 3))
print("visitors per group:", math.ceil(visitors_per_group))

# Same calculation for a smaller 1-point gap (10% to 11%)
small_gap = 0.01
small_variance_sum = 0.10 * 0.90 + 0.11 * 0.89
small_gap_sample = (z_alpha + z_power) ** 2 * small_variance_sum / small_gap ** 2
print("visitors per group for 10% to 11%:", math.ceil(small_gap_sample))
```
Output: `z for alpha: 1.96  z for power: 0.842`, `visitors per group: 3839`, `visitors per group for 10% to 11%: 14749`. Library `statsmodels` (NormalIndPower) gives about 3,835, a tiny difference from using a different effect-size formula. In plain words: about 3,839 visitors in each version, so roughly 7,700 in total.
Excel (2010+; not run in Excel here): `=ROUNDUP((NORM.S.INV(0.975)+NORM.S.INV(0.8))^2*(0.1*0.9+0.12*0.88)/(0.02)^2,0)` should return 3,839 (same formula as the Python code).
**Likely follow-ups:**
1. *How long will it take?* Divide total users by daily eligible traffic, then round up to full weeks (Q18).
**Common mistakes:** Using total instead of per-group sample size; picking an MDE just to fit the available traffic; forgetting to use only eligible users.

### Q11 ⭐⭐⭐ 🟡 Why should you not stop an A/B test the moment the result turns significant (the peeking problem)?
**Asked at:** commonly asked (no company-specific report found); peeking appears in the prep sources as a standard pitfall.
**What the interviewer is checking:** Do you understand that repeated looks inflate false positives?
**Say this in the interview:** "A p-value is only valid for one planned look. If I check daily and stop when it dips below 0.05, I give chance many opportunities to produce a 'win', so my real false-alarm rate is far above 5%."
**Explain simply:**
- Early in a test, results swing wildly; a random wobble can cross p < 0.05 and then drift back.
- Each extra look is another chance for a false alarm, like re-rolling dice until you get a six.
- Fixes: decide sample size and end date in advance and look only then, or use sequential methods designed for repeated looks (Q42).
**Worked example:** I simulated 5,000 A/A tests (both versions truly 10%, 2,000 users each) and checked after every 200 users. Stopping at the first p < 0.05 gave a "winner" 18.6% of the time; checking only at the end gave 5.6% (about the promised 5%).
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Fixed seed so the result reproduces; 5,000 pretend experiments
random_generator = np.random.default_rng(42)
number_of_experiments = 5000
visitors_per_group = 2000

# Both groups truly convert at 10%, so any "win" is a false alarm
true_rate = 0.10

# Look at the results after 200, 400, ... 2000 users per group
look_points = list(range(200, 2001, 200))

false_alarms_peeking = 0
false_alarms_final_only = 0

for experiment in range(number_of_experiments):
    # Simulate every visitor's outcome for both groups
    group_a = random_generator.random(visitors_per_group) < true_rate
    group_b = random_generator.random(visitors_per_group) < true_rate
    stopped_early = False
    for users_so_far in look_points:
        conversions_a = group_a[:users_so_far].sum()
        conversions_b = group_b[:users_so_far].sum()
        pooled_rate = (conversions_a + conversions_b) / (2 * users_so_far)
        if pooled_rate == 0:
            continue
        standard_error = np.sqrt(pooled_rate * (1 - pooled_rate) * 2 / users_so_far)
        z_score = (conversions_b - conversions_a) / users_so_far / standard_error
        p_value = 2 * stats.norm.sf(abs(z_score))
        # A peeker would stop and declare a win the first time p is below 0.05
        if p_value < 0.05:
            stopped_early = True
        # Someone who looks only once, at the end
        if users_so_far == visitors_per_group and p_value < 0.05:
            false_alarms_final_only += 1
    if stopped_early:
        false_alarms_peeking += 1

print("peeking 10 times:", false_alarms_peeking / number_of_experiments)
print("single look at end:", false_alarms_final_only / number_of_experiments)
```
Output: `peeking 10 times: 0.1864`, `single look at end: 0.0556`. Peeking turned a 5% false-alarm rate into nearly 19%. In plain words: if we stop at the first lucky look, almost one in five do-nothing changes gets called a win. (The 0.0556 is a little above 5% only because of simulation noise.)
**Likely follow-ups:**
1. *Can I monitor at all?* Yes, for bugs and the split ratio; just do not decide the winner from early p-values.
**Common mistakes:** "It hit 95% so we can stop"; extending a test because it is "almost significant".

### Q12 ⭐⭐⭐ 🟡 What are Type I and Type II errors in the context of an A/B test?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you name both errors and link them to alpha and power?
**Say this in the interview:** "Type I is a false alarm: we ship a change that does nothing. Type II is a miss: we throw away a change that really works. Alpha controls Type I; power (1 minus the Type II rate) controls Type II."
**Explain simply:**
- Type I error (false positive): declare a winner when there is no real difference; probability = alpha, usually 5%.
- Type II error (false negative): see no significant result although a real effect exists; probability = beta, usually 20%.
- Power = 1 - beta. Bigger samples reduce Type II without raising Type I.
- Which hurts more depends on cost: a risky, expensive launch fears Type I; a cheap idea with big upside fears Type II.
**Worked example:** I simulated 5,000 tests with 2,000 users per group. When both versions were truly 10%, 4.9% came out "significant" (Type I rate, matching the 5% promise). When B was truly 12%, 46.8% of tests missed it (Type II), so power was only about 53%.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Fixed seed so the result reproduces; 5,000 pretend tests per world
random_generator = np.random.default_rng(7)
number_of_tests = 5000
visitors_per_group = 2000

# Two-proportion z-test at the 5% level: True means "looks significant"
def is_significant(conversions_a, conversions_b, visitors):
    pooled_rate = (conversions_a + conversions_b) / (2 * visitors)
    standard_error = np.sqrt(pooled_rate * (1 - pooled_rate) * 2 / visitors)
    z_score = (conversions_b - conversions_a) / visitors / standard_error
    return 2 * stats.norm.sf(abs(z_score)) < 0.05

false_alarms = 0
missed_wins = 0
for test in range(number_of_tests):
    # World 1: no real difference (10% vs 10%); a significant result is a false alarm
    conversions_a = random_generator.binomial(visitors_per_group, 0.10)
    conversions_b = random_generator.binomial(visitors_per_group, 0.10)
    if is_significant(conversions_a, conversions_b, visitors_per_group):
        false_alarms += 1
    # World 2: real difference (10% vs 12%); a non-significant result is a miss
    conversions_a = random_generator.binomial(visitors_per_group, 0.10)
    conversions_b = random_generator.binomial(visitors_per_group, 0.12)
    if not is_significant(conversions_a, conversions_b, visitors_per_group):
        missed_wins += 1

print("Type I rate (false alarms):", false_alarms / number_of_tests)
print("Type II rate (missed real win):", missed_wins / number_of_tests)
```
Output: `Type I rate (false alarms): 0.049`, `Type II rate (missed real win): 0.4676`. In plain words: with 2,000 users per group, about 1 in 20 do-nothing changes is wrongly called a win, and nearly half of real 2-point wins are missed.
**Likely follow-ups:**
1. *Can you reduce both at once?* Yes, only with more data (or lower variance, Q41).
**Common mistakes:** Mixing up which is which; thinking p < 0.05 means a 5% chance the result is wrong.

### Q13 ⭐⭐ 🟢 How do you calculate absolute lift and relative lift of a conversion rate, and why do both matter?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Precision with percentages, a classic source of misleading claims.
**Say this in the interview:** "Absolute lift is new rate minus old rate, in percentage points. Relative lift is that difference divided by the old rate. I report both, because a 20% relative lift can be a tiny absolute change."
**Explain simply:**
- Percentage points are differences between two percentages; percent change is relative to the starting value.
- Relative lift sounds big on small baselines; absolute lift shows how many extra people it really is.
**Formula in plain words:** absolute lift = treatment rate minus control rate; relative lift = absolute lift divided by control rate.
**Worked example:** Control 10% (200/2000), treatment 12% (240/2000): absolute lift 2.0 points, relative lift 20%. On a small baseline, 1.0% to 1.2% is also a 20% relative lift but only 0.2 points.
**Excel / Python:**
```python
# Conversion rates of the two groups
control_rate = 200 / 2000
treatment_rate = 240 / 2000

# Absolute lift in percentage points, relative lift in percent
absolute_lift_points = (treatment_rate - control_rate) * 100
relative_lift_percent = (treatment_rate - control_rate) / control_rate * 100

print("absolute lift (points):", round(absolute_lift_points, 2))
print("relative lift (%):", round(relative_lift_percent, 1))
```
Output: `absolute lift (points): 2.0`, `relative lift (%): 20.0`. Excel: with control rate in A1 (0.10) and treatment in B1 (0.12), absolute `=(B1-A1)*100` returns 2; relative `=(B1-A1)/A1` returns 20% when formatted as a percentage. In plain words: 2 extra buyers in every 100 visitors, which is a one-fifth improvement on the old rate.
**Likely follow-ups:**
1. *Which do you report to executives?* Both, plus the expected extra orders or hires.
**Common mistakes:** Saying "up 2%" when you mean 2 points; reporting only the bigger-sounding relative number.

### Q14 ⭐⭐ 🟢 Tell me about an A/B test you ran or analysed. What was the result and what happened next?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Real experience, structured storytelling, and honest interpretation.
**Say this in the interview:** "Use your own real project. If you have not run one, say so plainly and describe a realistic case you designed or analysed (a course, a self-made dataset, or a proposed HR test), then walk through it in the same structure. Never invent a business result you did not produce."
**Explain simply:** Use this structure: (1) the problem and hypothesis, (2) metric and guardrail, (3) design: groups, split, duration, sample size, (4) result with numbers and interval, (5) decision and what happened after, (6) one lesson learned.
**Worked example (illustrative template, not a real case):** "I proposed testing a new reminder SMS to reduce interview no-shows. 400 candidates got the usual email, 400 got the SMS plus email. No-shows were 22.5% (90 of 400) vs 16.0% (64 of 400): 6.5 points lower, about 29% relative reduction, z = -2.33, p = 0.020, 95% interval -11.9 to -1.1 points. Recruiter workload (guardrail) did not change. We rolled the SMS out to all candidates and tracked no-shows for two months to confirm the effect held (it can shrink, see Q37)."
**Excel / Python:**
```python
import math
from scipy import stats

# Counts for this illustrative HR test
candidates_per_group = 400
no_shows_control = 90
no_shows_reminder = 64

# No-show rate in each group and the gap
rate_control = no_shows_control / candidates_per_group
rate_reminder = no_shows_reminder / candidates_per_group
gap = rate_reminder - rate_control

# Z-test using the pooled rate
pooled_rate = (no_shows_control + no_shows_reminder) / (2 * candidates_per_group)
standard_error = math.sqrt(pooled_rate * (1 - pooled_rate) * 2 / candidates_per_group)
z_score = gap / standard_error
p_value = 2 * stats.norm.sf(abs(z_score))

# 95% confidence interval for the gap
standard_error_gap = math.sqrt(rate_control * (1 - rate_control) / candidates_per_group
                               + rate_reminder * (1 - rate_reminder) / candidates_per_group)
lower_limit = gap - 1.96 * standard_error_gap
upper_limit = gap + 1.96 * standard_error_gap

print("rates:", rate_control, rate_reminder)
print("gap (points):", round(gap * 100, 1), " relative change (%):", round(gap / rate_control * 100, 1))
print("z:", round(z_score, 2), " p:", round(p_value, 4))
print("95% CI (points):", round(lower_limit * 100, 1), "to", round(upper_limit * 100, 1))
```
Output: `rates: 0.225 0.16`, `gap (points): -6.5  relative change (%): -28.9`, `z: -2.33  p: 0.0197`, `95% CI (points): -11.9 to -1.1`. In plain words: the reminder cut no-shows by about 6.5 points, and the whole interval is below zero, so the drop is unlikely to be luck.
**Likely follow-ups:**
1. *What would you do differently?* Pre-register the sample size, check SRM, and follow up on long-term effect.
**Common mistakes:** Presenting only the win; no numbers; claiming outcomes you cannot back up; skipping what happened after the test.

### Q15 ⭐⭐ 🟡 What is statistical power, and why is 80% the usual target?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand power as the chance of detecting a real effect, and the cost trade-off?
**Say this in the interview:** "Power is the probability that the test will come out significant when the effect is real. 80% means we accept a 1-in-5 chance of missing a true effect of the size we planned for. It is a convention balancing certainty against the extra users and time that higher power costs."
**Explain simply:**
- Power = 1 - Type II error rate (Q12). Four levers: sample size, effect size, baseline noise, alpha.
- An underpowered test often ends "not significant" even when the idea works, so the result is inconclusive, not negative.
- 80% is a convention (alongside alpha 5%, so a miss is treated as four times less bad than a false alarm), not a law; riskier or costlier decisions justify 90%.
**Worked example:** Detecting 10% to 12% at 5% significance: 50% power needs 1,879 per group, 80% needs 3,839, 90% needs 5,139, 95% needs 6,355. The Q8 test with 2,000 per group had power of only about 52.5%.
**Excel / Python:**
```python
import math
from scipy import stats
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# Inputs: 10% now, 12% hoped for, 5% two-sided significance
baseline_rate = 0.10
target_rate = 0.12
z_alpha = stats.norm.ppf(1 - 0.05 / 2)

# Combined spread of the two rates, and the gap we want to detect
variance_sum = baseline_rate * (1 - baseline_rate) + target_rate * (1 - target_rate)
gap = target_rate - baseline_rate

# Visitors per group needed at different power levels
for power in (0.5, 0.8, 0.9, 0.95):
    z_power = stats.norm.ppf(power)
    visitors_per_group = (z_alpha + z_power) ** 2 * variance_sum / gap ** 2
    print("power", power, "-> visitors per group:", math.ceil(visitors_per_group))

# Power actually achieved with 2,000 visitors per group
effect_size = proportion_effectsize(target_rate, baseline_rate)
achieved_power = NormalIndPower().solve_power(effect_size, nobs1=2000, alpha=0.05, ratio=1)
print("power with 2,000 per group:", round(achieved_power, 3))
```
Output: `power 0.5 -> 1879`, `power 0.8 -> 3839`, `power 0.9 -> 5139`, `power 0.95 -> 6355`, `power with 2,000 per group: 0.525`. Going from 80% to 95% power costs about 65% more users.
**Likely follow-ups:**
1. *Do you calculate power after the test?* Better before; "post-hoc power" from the observed effect adds nothing beyond the p-value.
**Common mistakes:** Thinking power is the probability the result is correct; reading a non-significant underpowered test as "no effect".

### Q16 ⭐⭐ 🟡 What is the Minimum Detectable Effect (MDE), and how does it change the required sample size?
**Asked at:** commonly asked (no company-specific report found); sample size and MDE are a recurring A/B topic in the prep sources (Statsig, MetricGate; vendor blogs, not read in full).
**What the interviewer is checking:** Do you know that the MDE is chosen before the test and that small effects need far more people?
**Say this in the interview:** "The MDE is the smallest improvement that would actually matter to the business, and that I want my test to be able to catch. Halve the MDE and the sample size roughly quadruples, so I set it with the business before the test, not after."
**Explain simply:**
- *Minimum Detectable Effect*: the smallest real change you want the test to reliably spot (for example, conversion going from 10% to 11%).
- It is a planning choice, not a result. It comes from business value: "what lift is worth the cost of shipping?"
- Tiny differences hide inside random noise, so spotting them needs many more people.
- Sample size depends on the square of the MDE: half the MDE, about four times the people.
**Formula in plain words:** Visitors per group = (z for 5% significance + z for 80% power) squared, times the combined spread of both rates, divided by the MDE squared. In symbols: n = (z_alpha + z_power)^2 x [p1(1-p1) + p2(1-p2)] / MDE^2, with z_alpha = 1.96 and z_power = 0.84.
**Worked example:** Baseline conversion is 10%. To detect +2 points you need about 3,839 per group; +1 point needs 14,749; +0.5 point needs 57,760.
**Excel / Python:**
```python
import math
from scipy import stats

# Sample size per group for a conversion-rate test (two-sided 5%, 80% power)
def visitors_per_group(baseline_rate, mde_points):
    new_rate = baseline_rate + mde_points
    z_alpha = stats.norm.ppf(1 - 0.05 / 2)   # 1.96
    z_power = stats.norm.ppf(0.80)           # 0.84
    spread = baseline_rate * (1 - baseline_rate) + new_rate * (1 - new_rate)
    return math.ceil((z_alpha + z_power) ** 2 * spread / mde_points ** 2)

# Try three different MDEs on a 10% baseline
for mde_points in [0.02, 0.01, 0.005]:
    print(f"MDE {mde_points:.3f} -> {visitors_per_group(0.10, mde_points):,} per group")
```
Output:
```
MDE 0.020 -> 3,839 per group
MDE 0.010 -> 14,749 per group
MDE 0.005 -> 57,760 per group
```
Halving the MDE from 1 point to 0.5 point multiplies the people needed by about 3.9.
**Likely follow-ups:** 1) *Is MDE the same as the observed effect?* No: MDE is planned beforehand, the observed effect is what you measure. 2) *How do you pick it?* From the business value of the change and the traffic you can afford.
**Common mistakes:** Picking a tiny MDE "to be safe" and ending with a test that runs for months; setting the MDE after seeing the result; confusing absolute points with relative percent.

### Q17 ⭐⭐ 🟡 What is a guardrail metric, and what do you do when the primary metric improves but a guardrail metric gets worse?
**Asked at:** commonly asked (no company-specific report found); guardrails appear in the Amplitude and PracHub A/B lists (snippet level).
**What the interviewer is checking:** Can you weigh a win against a hidden cost instead of shipping on the headline number?
**Say this in the interview:** "A guardrail is a metric I must not damage while chasing the primary one, like refunds, page speed or complaints. If the primary improves but a guardrail worsens significantly, I do not ship automatically; I quantify the trade-off in money or customer harm and take it to the decision makers."
**Explain simply:**
- *Primary metric*: the one number the test is built to move (conversion).
- *Guardrail metric*: a safety check (refund rate, cancellations, load time, unsubscribe rate). It is not the goal, but a big fall means the win is not real.
- Decide guardrails and their acceptable limits before launch, so nobody argues afterwards.
- If a guardrail fails: check it is real (significant, not a logging bug), size the cost, then choose: fix and retest, ship to a small share, or drop.
**Worked example:** 20,000 visitors per group. Conversion rises from 10.0% to 10.6% (p = 0.048), but refunds rise from 4.0% to 4.6% (p = 0.003). The gain is real but small, and the refund damage is clearer, so I would not ship as is.
**Excel / Python:**
```python
import math
from scipy import stats

# Two-sided z-test for a difference between two rates
def compare_rates(events_a, visitors_a, events_b, visitors_b):
    rate_a = events_a / visitors_a
    rate_b = events_b / visitors_b
    pooled_rate = (events_a + events_b) / (visitors_a + visitors_b)
    standard_error = math.sqrt(pooled_rate * (1 - pooled_rate) * (1 / visitors_a + 1 / visitors_b))
    z_score = (rate_b - rate_a) / standard_error
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
    return round(rate_b - rate_a, 4), float(round(p_value, 4))

# Primary metric: conversion 10.0% -> 10.6%
print("Conversion change, p:", compare_rates(2000, 20000, 2120, 20000))
# Guardrail: refund rate 4.0% -> 4.6%
print("Refund change, p:   ", compare_rates(800, 20000, 920, 20000))
```
Output:
```
Conversion change, p: (0.006, 0.0484)
Refund change, p:    (0.006, 0.0031)
```
Both rates moved by 0.6 points, but the refund move is much more convincing statistically.
**Likely follow-ups:** 1) *Does every metric need a significance test?* Guardrails are often checked for "no meaningful harm" rather than for a win. 2) *Who decides?* The product owner, with your quantified trade-off.
**Common mistakes:** Defining guardrails after seeing the data; ignoring a guardrail because the primary is significant; forgetting that a guardrail can be underpowered, so "not significant" is not "safe".

### Q18 ⭐⭐ 🟡 How long should an A/B test run, and why should it usually cover full weeks?
**Asked at:** commonly asked (no company-specific report found); duration and sample size are a recurring A/B topic in the prep sources (PracHub listing, snippet level).
**What the interviewer is checking:** Do you connect duration to sample size and to weekly behaviour patterns?
**Say this in the interview:** "I work out the sample size first, divide by daily traffic to get the minimum days, then round up to full weeks (often one to three, never less than one), because behaviour differs between weekdays and weekends. I fix that length in advance and do not stop early."
**Explain simply:**
- Minimum days = total people needed divided by people entering the test per day.
- People behave differently by day: job applications may peak on Mondays, food orders on weekends. A test of 3 weekdays sees a biased picture.
- Full weeks give every weekday equal weight in both groups.
- Do not run too long either: cookies expire, seasons change, and the novelty effect (Q19) needs time to fade.
**Worked example:** Need 14,749 per group, so 29,498 in total. At 1,500 visitors a day that is 20 days, rounded up to 21 days (three full weeks).
**Excel / Python:**
```python
import math

# Visitors needed per group (from the sample size formula)
visitors_per_group = 14749
total_visitors_needed = visitors_per_group * 2
daily_visitors_in_test = 1500

# Days needed, then rounded up to whole weeks
days_needed = math.ceil(total_visitors_needed / daily_visitors_in_test)
days_rounded_to_full_weeks = math.ceil(days_needed / 7) * 7
print("Days needed:", days_needed)
print("Run for (full weeks):", days_rounded_to_full_weeks, "days")
```
Output:
```
Days needed: 20
Run for (full weeks): 21 days
```
Twenty days is not a whole number of weeks, so we add one day to finish on a complete third week.
**Likely follow-ups:** 1) *What if you hit the sample size in 3 days?* Still run at least a full week to cover the weekly cycle. 2) *What if there is a holiday?* Avoid it or extend the test.
**Common mistakes:** Stopping when the result looks good; ending mid-week; running far longer than planned "to be sure" and letting outside events creep in.

### Q19 ⭐⭐ 🟡 What are the novelty effect and the primacy effect in an A/B test?
**Asked at:** commonly asked (no company-specific report found); novelty effect is named in the Amplitude pitfalls list (snippet level).
**What the interviewer is checking:** Do you know early results may not reflect long-run behaviour?
**Say this in the interview:** "Novelty effect: people click on something new just because it is new, so the lift fades. Primacy effect is the opposite: people are used to the old way, so a better design looks worse at first until they adapt. I check the daily lift over time and run long enough for it to settle."
**Explain simply:**
- *Novelty effect*: a temporary boost because something is new and shiny.
- *Primacy effect* (also called change aversion): a temporary dip because existing users are used to the old version.
- Both mean the first days are not typical; the lift you care about is the one after things settle.
- Check: plot the daily lift, or compare new users (no habit) with returning users.
**Worked example:** Made-up daily lift for 14 days starts at 12 points and decays to 1 point. The first 3 days average 10, the last 7 days average 1.14, and the full 14 days average 3.79. Reading only the first days would hugely overstate the benefit.
**Excel / Python:**
```python
# Made-up daily lift (percentage points) for 14 days of a test
daily_lift_points = [12, 10, 8, 6, 4, 3, 2, 2, 1, 1, 1, 1, 1, 1]

first_three_days = daily_lift_points[:3]
last_seven_days = daily_lift_points[-7:]

print("Average lift, first 3 days:", sum(first_three_days) / len(first_three_days))
print("Average lift, last 7 days:", round(sum(last_seven_days) / len(last_seven_days), 2))
print("Average lift, all 14 days:", round(sum(daily_lift_points) / len(daily_lift_points), 2))
```
Output:
```
Average lift, first 3 days: 10.0
Average lift, last 7 days: 1.14
Average lift, all 14 days: 3.79
```
The lift shrinks over time, which is the classic novelty pattern.
**Likely follow-ups:** 1) *How do you separate the two?* Compare new vs returning users, and look at the trend. 2) *Which should you trust?* The settled, later-period effect.
**Common mistakes:** Calling a test after 2 days of high lift; mixing up the two effects; assuming every lift is permanent.

### Q20 ⭐⭐ 🟡 How do you read a confidence interval for the lift in an A/B test?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you use the interval to judge both significance and business size, not only the p-value?
**Say this in the interview:** "The 95% confidence interval is the range of lifts that fit the data. If it excludes zero, the result is significant; and its width tells me how precise we are. I compare the whole range with the smallest lift that matters to the business."
**Explain simply:**
- *Confidence interval (CI)*: a range built from the data so that, in the long run, 95% of such ranges contain the true value.
- Interval entirely above 0: B is better. Contains 0: we cannot rule out no difference. Entirely below 0: B is worse.
- A wide interval means a noisy, imprecise estimate. A narrow one means a precise estimate.
- It does not mean "95% chance the true value is in this range" in the strict sense; say "we are 95% confident, by the method".
**Formula in plain words:** Lift plus or minus 1.96 times the standard error. The *standard error* is how much the lift would wobble by chance. In symbols: (pB - pA) +/- 1.96 x sqrt[pA(1-pA)/nA + pB(1-pB)/nB].
**Worked example:** A converted 200/2,000 (10%), B 240/2,000 (12%). Lift is 2.0 points, 95% CI 0.06 to 3.94 points, or 0.6% to 39.4% relative. Significant, but barely: the true lift could be almost nothing or quite large.
**Excel / Python:**
```python
import math

# Version A: 200 of 2,000 converted; version B: 240 of 2,000
rate_a = 200 / 2000
rate_b = 240 / 2000
absolute_lift = rate_b - rate_a

# Standard error of the difference (how much it wobbles by chance)
standard_error = math.sqrt(rate_a * (1 - rate_a) / 2000 + rate_b * (1 - rate_b) / 2000)

# 95% confidence interval = lift plus or minus 1.96 standard errors
lower_end = absolute_lift - 1.96 * standard_error
upper_end = absolute_lift + 1.96 * standard_error

print(f"Lift: {absolute_lift:.4f}")
print(f"95% CI: {lower_end:.4f} to {upper_end:.4f}")
print(f"In relative terms: {lower_end / rate_a:.1%} to {upper_end / rate_a:.1%}")
```
Output:
```
Lift: 0.0200
95% CI: 0.0006 to 0.0394
In relative terms: 0.6% to 39.4%
```
The interval just clears zero, so the result is borderline significant and very imprecise.
**Likely follow-ups:** 1) *CI vs p-value?* The CI shows the size and the uncertainty; the p-value gives only one yes/no signal. 2) *Does 95% CI mean 95% of data lies inside?* No, it is about the true lift, not individual users.
**Common mistakes:** Saying "95% probability the true value is inside"; ignoring the lower end when it is near zero; mixing absolute points and relative percent.

### Q21 ⭐⭐ 🟡 When do you use a one-tailed test and when a two-tailed test in an A/B test?
**Asked at:** commonly asked (no company-specific report found); one-sided vs two-sided is a recurring pattern in the PracHub listing (snippet level).
**What the interviewer is checking:** Do you know the default is two-tailed and why one-tailed can be abused?
**Say this in the interview:** "I default to two-tailed, because I care if the change is worse as well as better. A one-tailed test is only fair if I decided before the test that I only act on one direction, and a harmful direction truly does not matter, which is rare."
**Explain simply:**
- *Two-tailed*: tests "is B different from A, up or down?"
- *One-tailed*: tests only "is B better than A?" and ignores the other direction.
- For the same data, the one-tailed p-value is half the two-tailed one. That makes it tempting to switch after the fact, which is cheating.
- A one-tailed test cannot flag a harmful change, which is the very thing a test should catch.
**Worked example:** Test A 200/2,000 vs B 240/2,000. Two-tailed p = 0.0432; one-tailed p = 0.0216. If the data had given a two-tailed p of 0.06, a switch to one-tailed would produce 0.03 and a false "win".
**Excel / Python:**
```python
from statsmodels.stats.proportion import proportions_ztest

converted = [200, 240]
visitors = [2000, 2000]

# Two-tailed: is B different from A in either direction?
z_score, p_two_tailed = proportions_ztest(converted, visitors)
# One-tailed: is B larger than A? (A is listed first, so test "smaller")
z_score, p_one_tailed = proportions_ztest(converted, visitors, alternative="smaller")

print("z-score:", round(z_score, 3))
print("Two-tailed p:", round(p_two_tailed, 4))
print("One-tailed p:", round(p_one_tailed, 4))
```
Output:
```
z-score: -2.021
Two-tailed p: 0.0432
One-tailed p: 0.0216
```
The z-score is negative only because A is listed first; the one-tailed p-value is exactly half the two-tailed one.
**Likely follow-ups:** 1) *Does Excel have both?* Yes: `NORM.S.DIST` gives one tail; double it for two tails. 2) *When is one-tailed fine?* Non-inferiority style tests, decided in advance.
**Common mistakes:** Choosing one-tailed after seeing the data; thinking it gives "more power" for free; ignoring a significant drop.

### Q22 ⭐⭐ 🟡 What is the multiple comparisons problem when you test many variants or many metrics, and how do you handle it?
**Asked at:** commonly asked (no company-specific report found); multiple comparisons is a recurring A/B topic in the PracHub listing (snippet level).
**What the interviewer is checking:** Do you know that more tests mean more false alarms, and can you name a fix?
**Say this in the interview:** "Every test at 5% has a 5% chance of a false alarm, so with many metrics or variants one will probably look significant by luck. I name one primary metric in advance, and for the rest I tighten the threshold with Bonferroni or control the false discovery rate."
**Explain simply:**
- Check 20 metrics at 5% each and the chance of at least one false "winner" is about 64%, not 5%.
- Fixes: pick one primary metric beforehand; use a stricter cut-off (*Bonferroni*: divide 5% by the number of tests); or use the *false discovery rate* (Benjamini-Hochberg) when you accept a few false leads.
- Treat unplanned significant findings as ideas to retest, not as results.
- Same issue with A/B/C/D variants and with slicing by segments.
**Formula in plain words:** Chance of at least one false alarm = 1 minus (1 minus 0.05) to the power of the number of tests. Bonferroni threshold = 0.05 divided by the number of tests.
**Worked example:** 20 metrics: 1 - 0.95^20 = 0.642. Bonferroni threshold is 0.0025. I also simulated 20,000 experiments where nothing is truly different (20 independent p-values each): 64.0% had at least one p below 0.05, but only 5.0% did when using the 0.0025 cut-off.
**Excel / Python:**
```python
import numpy as np

# Chance of at least one false alarm if 20 metrics are all tested at 5%
number_of_metrics = 20
chance_of_a_false_alarm = 1 - (1 - 0.05) ** number_of_metrics
print("Chance of at least one false alarm:", round(chance_of_a_false_alarm, 3))

# Bonferroni: divide the 5% allowance among the 20 tests
bonferroni_threshold = 0.05 / number_of_metrics
print("Bonferroni threshold per metric:", bonferroni_threshold)

# Simulate 20,000 experiments with no real effect; when nothing is real, each p-value is a random number between 0 and 1
random_generator = np.random.default_rng(11)
p_values = random_generator.random((20000, 20))
smallest_p_per_experiment = p_values.min(axis=1)

# Share of experiments with at least one "significant" metric, with and without the Bonferroni cut-off
print("Simulated, cut-off 0.05:", (smallest_p_per_experiment < 0.05).mean())
print("Simulated, cut-off 0.0025:", (smallest_p_per_experiment < 0.0025).mean())
```
Output:
```
Chance of at least one false alarm: 0.642
Bonferroni threshold per metric: 0.0025
Simulated, cut-off 0.05: 0.64045
Simulated, cut-off 0.0025: 0.0495
```
In plain words: testing 20 metrics at 5% almost always hands you a fake winner; the stricter cut-off brings the false-alarm rate back to about 5%.
Excel: `=1-(1-0.05)^20` returns 0.642 (not run in Excel here; same arithmetic).
**Likely follow-ups:** 1) *Is Bonferroni too strict?* Yes, with many tests it loses power; false discovery rate is gentler. 2) *Does one primary metric solve it?* For the main decision, yes.
**Common mistakes:** Reporting the one "significant" metric out of twenty; adjusting only after seeing results; treating segment slices as free.

### Q23 ⭐⭐ 🟡 What should be the unit of randomisation in an A/B test: user, session, cookie or device?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand consistency of experience and independence of observations?
**Say this in the interview:** "Usually the user, using a logged-in ID, so one person always sees the same version and I can count each person once. Sessions or cookies break if the same person is placed in both groups. I pick the unit to match how I will analyse and how the feature is experienced."
**Explain simply:**
- *Unit of randomisation*: the thing that gets a coin-flip assignment (person, session, device).
- Per session: the same person may see version A today and B tomorrow, which is confusing and muddies results.
- Per cookie or device: one person with a phone and a laptop can land in both groups.
- Per user ID: best consistency, but needs login. Sometimes you go bigger (a city, a store, an office) when users influence each other.
- Analyse at the same level you randomise, or the p-values are too optimistic.
**Worked example:** Hiring portal test by employee ID. A fixed scrambling (hash) of the ID plus the test name gives a stable, repeatable assignment.
**Excel / Python:**
```python
import hashlib

# Assign each employee to a group using a fixed "scrambling" of their ID
employee_ids = ["E1001", "E1002", "E1003", "E1004", "E1005", "E1006"]
for employee_id in employee_ids:
    text_to_scramble = "holiday_test" + employee_id
    scrambled_number = int(hashlib.md5(text_to_scramble.encode()).hexdigest(), 16)
    group = "treatment" if scrambled_number % 2 == 1 else "control"
    print(employee_id, group)
```
Output:
```
E1001 treatment
E1002 treatment
E1003 control
E1004 treatment
E1005 treatment
E1006 treatment
```
The same ID always gives the same group; over thousands of IDs the split would be close to 50/50 (this tiny list is not).
**Likely follow-ups:** 1) *Why include the test name?* So different tests get independent splits. 2) *When randomise by group of users?* When users affect each other (Q38).
**Common mistakes:** Randomising per session then counting users; ignoring one person on several devices; analysing sessions as if they were independent.

### Q24 ⭐⭐ 🟡 Which statistical test would you use to compare conversion rate, and which to compare average revenue per user?
**Asked at:** commonly asked (no company-specific report found); test choice (z vs t) is in the Interview Query topic list (snippet level).
**What the interviewer is checking:** Do you match the test to the type of data (yes/no vs amount)?
**Say this in the interview:** "Conversion is a yes/no outcome, so I use a two-proportion z-test (or chi-square). Revenue per user is a number, so I use a t-test, usually Welch's, which does not assume equal spread. Because revenue is skewed with many zeros, I also check with a bootstrap (re-sampling the data many times to see how much the gap wobbles) or a Mann-Whitney test, and look at outliers."
**Explain simply:**
- Yes/no per person (converted, left the company): compare two proportions with a z-test or chi-square.
- Amount per person (revenue, salary): compare two averages with a t-test; *Welch's* version is the safe default.
- Money data is lopsided: most people spend 0, a few spend a lot. Big samples make the t-test still reasonable, but check outliers.
- Mann-Whitney compares overall ranking, not exactly the average, so say what you are testing.
**Worked example:** Made-up data, 5,000 visitors per group, conversion about 10% vs 11.5%. Buyers 490 vs 618 (z-test p = 0.000045). Revenue per visitor Rs 55.74 vs Rs 72.13 (Welch p = 0.003).
**Excel / Python:**
```python
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest

rng = np.random.default_rng(7)

# Made-up data: 5,000 visitors per group, conversion 10% vs 11.5%
converted_a = rng.binomial(1, 0.10, 5000)
converted_b = rng.binomial(1, 0.115, 5000)

# Conversion rate (yes/no): two-proportion z-test
z_score, p_conversion = proportions_ztest(
    [converted_a.sum(), converted_b.sum()], [5000, 5000])
print("Buyers A and B:", converted_a.sum(), converted_b.sum())
print("Conversion p-value:", round(p_conversion, 6))

# Revenue per visitor: zero for non-buyers, skewed amounts for buyers
def make_revenue(converted):
    revenue = np.zeros(len(converted))
    buyers = converted == 1
    revenue[buyers] = rng.lognormal(np.log(400), 0.8, buyers.sum())
    return revenue

revenue_a = make_revenue(converted_a)
revenue_b = make_revenue(converted_b)

# Welch t-test (does not assume equal spread in the two groups)
t_result = stats.ttest_ind(revenue_b, revenue_a, equal_var=False)
print("Avg revenue per visitor A, B:", round(revenue_a.mean(), 2), round(revenue_b.mean(), 2))
print("Revenue p-value:", round(t_result.pvalue, 4))
```
Output:
```
Buyers A and B: 490 618
Conversion p-value: 4.5e-05
Avg revenue per visitor A, B: 55.74 72.13
Revenue p-value: 0.003
```
Both tests point the same way here. The data is simulated, only to show the method.
**Likely follow-ups:** 1) *z or t for conversion?* z for proportions; with huge samples they agree. 2) *Why not a plain t-test on 0/1 data?* It works roughly, but the z-test is the natural fit.
**Common mistakes:** Using a t-test on counts of people who converted; ignoring huge outliers in revenue; testing revenue per buyer instead of per visitor and forgetting who is counted.

### Q25 ⭐⭐ 🟡 A test shows no statistically significant difference. What do you conclude and what do you recommend?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know "not significant" is not "no effect"?
**Say this in the interview:** "I do not say the change has no effect. I say we found no evidence of a difference of the size we could detect. I look at the confidence interval and the power: if the interval rules out any meaningful lift, we stop; if it is wide, the test was too small and I recommend more data or a bigger change."
**Explain simply:**
- *Absence of evidence is not evidence of absence.* A small test may simply be too weak (low *power*, Q15).
- Look at the confidence interval. Narrow around 0: truly no important effect. Wide, spanning useful values: inconclusive.
- Check the test ran its planned size and had no bugs (Q29).
- Then recommend: do not ship for the lift; ship only if there is another reason (cost saving, simplicity); or retest with more traffic or a bolder variant.
**Worked example:** A converted 100/1,000, B 112/1,000. Lift 1.2 points, p = 0.38, 95% CI from -1.5 to +3.9 points. The interval includes both a harm and a useful gain, so the test is inconclusive. Detecting a 1.2-point lift on a 10% base would need about 10,327 people per group.
**Excel / Python:**
```python
import math

# 100 of 1,000 vs 112 of 1,000 converted, and the gap between the rates
rate_a, rate_b = 100 / 1000, 112 / 1000
lift = rate_b - rate_a

# Standard error of the gap, then the 95% interval
standard_error = math.sqrt(rate_a * (1 - rate_a) / 1000 + rate_b * (1 - rate_b) / 1000)
print(f"Lift: {lift:.3f}")
print(f"95% CI: {lift - 1.96 * standard_error:.3f} to {lift + 1.96 * standard_error:.3f}")
```
Output:
```
Lift: 0.012
95% CI: -0.015 to 0.039
```
The range is wide, so we have learned little; this is "inconclusive", not "no effect".
**Likely follow-ups:** 1) *Would you extend the test?* Only if planned for; extending because it is not significant is a form of peeking (Q11). 2) *What next?* Retest with a proper power calculation.
**Common mistakes:** Declaring "no effect"; extending until it becomes significant; ignoring the interval.

### Q26 ⭐⭐ 🟡 A test shows a lift in click-through rate but no change in revenue. What could explain it?
**Asked at:** commonly asked (no company-specific report found); "CTR up but revenue flat" is listed on DataInterview (snippet level, not read in full).
**What the interviewer is checking:** Can you reason through a funnel instead of trusting one metric?
**Say this in the interview:** "More clicks without more revenue means the extra clicks are low-quality, or something later in the funnel got worse. I would break the funnel into steps, check who is clicking, check for clickbait-style design, and check data and timing issues."
**Explain simply:**
- *Click-through rate (CTR)*: clicks divided by views. It is an early step, not the goal.
- Possible reasons: curiosity clicks from people who never intended to buy; a misleading button; slower page after the click; a different price shown later; sales delayed beyond the test window; or revenue is noisy and the test is too small to see a change.
- Check orders per click, revenue per visitor, and results by new vs returning users.
- Revenue is a better primary metric when it is what the business wants; CTR is a diagnostic.
**Worked example:** Per 10,000 visitors, clicks go 300 to 360 (CTR 3.0% to 3.6%), but orders stay at 90. Orders per click fall from 0.30 to 0.25 and orders per visitor stay at 0.009. The extra 60 clicks produced nothing.
**Excel / Python:**
```python
# Made-up funnel for 10,000 visitors per group
visitors = 10000
clicks_control, clicks_treatment = 300, 360
orders_control, orders_treatment = 90, 90

print("CTR:", clicks_control / visitors, "->", clicks_treatment / visitors)
print("Orders per click:", orders_control / clicks_control, "->", orders_treatment / clicks_treatment)
print("Orders per visitor:", orders_control / visitors, "->", orders_treatment / visitors)
```
Output:
```
CTR: 0.03 -> 0.036
Orders per click: 0.3 -> 0.25
Orders per visitor: 0.009 -> 0.009
```
More people click but fewer of them buy, so the headline CTR win does not turn into money.
**Likely follow-ups:** 1) *Would you ship?* Not for the CTR alone. 2) *What if revenue is just noisy?* Check the power for revenue; it needs a larger sample than CTR.
**Common mistakes:** Celebrating CTR; not checking power for the revenue metric; forgetting orders can lag behind clicks.

### Q27 ⭐⭐ 🟡 HR wants to test whether a new reminder message reduces interview no-shows. How would you set up the A/B test?
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured practice scenario.
**What the interviewer is checking:** Can you apply the full design to a real HR problem: metric, unit, size, risks?
**Say this in the interview:** "Unit is the candidate; I randomly give half the old reminder and half the new one. Primary metric is no-show rate; guardrails are reschedule and cancellation rates and the candidate experience. I work out the sample size first, fix the end date, and check the split."
**Explain simply:**
- Hypothesis: the new message lowers the no-show rate. Null: it makes no difference.
- Randomise each candidate (by candidate ID) when the interview is booked, so the groups are alike.
- Define the metric: *no-show* means did not attend and gave no notice before the slot (write it down).
- Baseline: look at past no-show rate (say 25%). MDE: a drop to 20% is worth having.
- Risks: recruiters knowing which message was sent; candidates sharing messages; different slots or roles in each group; small hiring volumes mean a long test.
**Worked example:** Baseline 25%, aim for 20%: need 1,091 candidates per group (2,182 in total). If only 100 interviews are booked per week, that is about 22 weeks, so either accept a larger MDE (25% to 15% needs 248 per group) or run it across more roles and locations.
**Excel / Python:**
```python
import math
from scipy import stats

# Candidates per group to detect a drop in no-shows from 25% to 20%
baseline_no_show = 0.25
target_no_show = 0.20

# z-values for 5% two-sided significance and 80% power
z_alpha = stats.norm.ppf(0.975)
z_power = stats.norm.ppf(0.80)

# Combined spread of the two rates, then candidates per group (rounded up)
spread = baseline_no_show * (1 - baseline_no_show) + target_no_show * (1 - target_no_show)
candidates_per_group = math.ceil((z_alpha + z_power) ** 2 * spread / (baseline_no_show - target_no_show) ** 2)
print("Candidates per group:", candidates_per_group)
print("Total candidates:", candidates_per_group * 2)
```
Output:
```
Candidates per group: 1091
Total candidates: 2182
```
So the test needs about 2,200 booked interviews in total, a real planning constraint for HR.
**Likely follow-ups:** 1) *Which test at the end?* Two-proportion z-test on no-show rates. 2) *What if only one office is involved?* Result applies to that office; say so.
**Common mistakes:** Letting recruiters choose who gets which message; not defining "no-show"; ignoring that the test may take months at HR volumes.

### Q28 ⭐⭐ 🟡 Swiggy wants to test free delivery on orders above Rs 199. Which metrics would you track and what could go wrong?
**Asked at:** Swiggy-style metric question; no verified Swiggy report of this question (the Swiggy DA guide in the sources was seen only as a search snippet).
**What the interviewer is checking:** Can you pick a primary metric, guardrails and risks for a pricing change?
**Say this in the interview:** "The aim is more orders and bigger baskets, but free delivery costs money. So the primary metric is profit per user (or contribution margin), with orders per user and average order value as drivers, and guardrails like delivery time, customer complaints and cancellations. I would split users randomly and watch for people just topping up to Rs 199."
**Explain simply:**
- Primary: contribution per user (orders x margin after delivery cost and the fee waived). Order count alone can rise while profit falls.
- Supporting: orders per user, average order value (AOV), share of orders just above Rs 199, new vs repeat users.
- Guardrails: delivery time, rider load, cancellations, complaints, discount cost.
- What can go wrong: a loss-making win (more orders but less profit); users order smaller meals just to cross Rs 199 or merge orders; riders overloaded; some restaurants or cities behave differently; the effect fades after the offer is new (Q19).
- Randomise by user, not by order, so one person gets one consistent rule.
**Worked example:** Per 1,000 users, made-up numbers: orders rise 10% (400 to 440). Margin before the fee is Rs 35 an order. In control every order pays a Rs 30 fee; in treatment the fee is charged only on the 40% of orders below Rs 199. Total profit falls from Rs 26,000 to Rs 20,680, so the "winner" on orders loses money.
**Excel / Python:**
```python
# Made-up numbers per 1,000 users in each group
orders_control, orders_treatment = 400, 440
margin_per_order_before_fee = 35      # Rs, after food and delivery costs
free_share_treatment = 0.60           # share of orders now above Rs 199
fee_when_charged = 30                 # Rs

profit_control = orders_control * (margin_per_order_before_fee + fee_when_charged)
fee_per_order_treatment = (1 - free_share_treatment) * fee_when_charged
profit_treatment = orders_treatment * (margin_per_order_before_fee + fee_per_order_treatment)

print("Orders: +", round((orders_treatment / orders_control - 1) * 100), "%")
print("Total profit control, treatment (Rs):", profit_control, profit_treatment)
```
Output:
```
Orders: + 10 %
Total profit control, treatment (Rs): 26000 20680.0
```
The numbers are invented to show why the primary metric should be profit, not orders.
**Likely follow-ups:** 1) *Would you launch on a small city first?* Yes, as a pilot. 2) *Long-term effect?* Track repeat ordering for weeks, since habit may add value later.
**Common mistakes:** Choosing orders as the only metric; ignoring the cost of the waived fee; no guardrails for delivery time.

### Q29 ⭐⭐ 🔴 What is a Sample Ratio Mismatch (SRM), how do you detect it, and what do you do if you find one?
**Asked at:** commonly asked (no company-specific report found); SRM is in the Interview Query and Dataford lists (titles/snippets only).
**What the interviewer is checking:** Do you validate the experiment itself before reading the result?
**Say this in the interview:** "SRM means the split of users is not what we planned, for example 50.5k versus 49k in a 50/50 test. I check it with a chi-square test against the planned ratio. If it fails, the results cannot be trusted, so I find the cause (assignment or logging bug) and fix and rerun, not just analyse."
**Explain simply:**
- *Sample ratio mismatch*: the group sizes differ from the planned ratio by more than chance allows.
- Chance alone makes small wobbles (50,100 vs 49,900 is fine) but a big gap signals a bug: bot filtering applied to one group, a slower page losing users, a redirect failing, or a faulty assignment.
- Detect with a *chi-square test* comparing actual counts with the planned split. Many teams alarm at p below 0.001 (from memory, unverified).
- If found: pause the read-out, investigate, fix, rerun. Do not "adjust" the numbers.
**Worked example:** Planned 50/50. Seen 50,500 vs 49,000: chi-square 22.61, p = 0.000002, a clear mismatch. Seen 50,100 vs 49,900: chi-square 0.4, p = 0.53, fine.
**Excel / Python:**
```python
from scipy import stats

# Planned 50/50 split; we actually saw 50,500 vs 49,000 users
users_seen = [50500, 49000]
result = stats.chisquare(users_seen)   # compares to an even split by default
print("Chi-square:", round(result.statistic, 2))
print("p-value:", result.pvalue)
```
Output:
```
Chi-square: 22.61
p-value: 1.9813263332735096e-06
```
A p-value this tiny means the split cannot be chance, so the experiment is broken until proven otherwise. In Excel: `=CHISQ.TEST(actual_range, expected_range)` (2010+; not run here).
**Likely follow-ups:** 1) *Why not trust the lift if it is positive?* The users in the two groups are no longer comparable. 2) *Common causes?* Bot filtering, redirects, logging that fails in one version.
**Common mistakes:** Reading the lift without checking the split; dismissing a 1.5% gap on large traffic as "close enough"; using a 0.05 alarm and drowning in false alarms.

### Q30 ⭐⭐ 🔴 You have too little traffic to reach the required sample size. What are your options?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you trade off honestly instead of running an underpowered test?
**Say this in the interview:** "I have a few levers: accept a larger MDE, so I test a bolder change; run longer; use a more sensitive metric or reduce variance (for example CUPED); pool more traffic; or move away from an A/B test, using before and after methods with care. What I avoid is running a weak test and treating a non-significant result as 'no effect'."
**Explain simply:**
- Larger MDE: only detect big effects. Test bolder changes, not tiny tweaks.
- Longer: more days, but with a limit (novelty, seasonality).
- Better metric: a metric with less noise, or earlier in the funnel (use as a signal with care).
- *Variance reduction* (CUPED, uses past behaviour to cut noise) can cut sample need by about 30% when the past metric is predictive (here assumed 30%, made-up).
- Looser threshold (10% significance) or a one-tailed test, only if agreed beforehand and the risk is low (Q21).
- Else: use judgement, qualitative research, or a quasi-experiment (Q43).
**Worked example:** Baseline 10%, 400 visitors a day in total. Detecting +1 point needs 14,749 per group, 74 days. Detecting +2 points needs 3,839, 20 days; +3 points needs 1,772, 9 days. With a 30% variance cut, +1 point needs about 10,325 per group.
**Excel / Python:**
```python
import math
from scipy import stats

daily_visitors = 400   # both groups together

def total_days(baseline_rate, mde_points):
    new_rate = baseline_rate + mde_points
    z_total = stats.norm.ppf(0.975) + stats.norm.ppf(0.80)
    spread = baseline_rate * (1 - baseline_rate) + new_rate * (1 - new_rate)
    visitors_per_group = math.ceil(z_total ** 2 * spread / mde_points ** 2)
    return visitors_per_group, math.ceil(2 * visitors_per_group / daily_visitors)

for mde_points in [0.01, 0.02, 0.03]:
    visitors_per_group, days = total_days(0.10, mde_points)
    print(f"MDE {mde_points:.2f}: {visitors_per_group:,} per group, {days} days")
```
Output:
```
MDE 0.01: 14,749 per group, 74 days
MDE 0.02: 3,839 per group, 20 days
MDE 0.03: 1,772 per group, 9 days
```
Aiming for bigger effects makes the test feasible in weeks, not months.
**Likely follow-ups:** 1) *Can you just reduce power to 70%?* Possible, but you accept more missed real effects. 2) *What is the cost of an underpowered test?* False reassurance and wasted effort.
**Common mistakes:** Running anyway and concluding "no impact"; lowering the bar silently after seeing results; chasing tiny effects with tiny traffic.

### Q31 ⭐ 🟢 What is the difference between an A/B test and an A/A test, and why run an A/A test?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that an A/A test is a health check of the testing system, not a test of an idea?
**Say this in the interview:** "In an A/B test the two groups see different versions. In an A/A test both groups see the exact same version. I run it to check that my setup is trustworthy: the split is fair, the tracking is correct, and the test only cries 'significant' about 5% of the time when there is truly no difference."
**Explain simply:**
- Because both groups are identical, any difference is pure luck. A healthy system should show "significant" in only about 5% of A/A tests (that is what the 5% significance level promises).
- If it shows far more (say 15%), something is broken: faulty randomisation, double-counted events, or the wrong statistical test.
- It also catches Sample Ratio Mismatch (a 50/50 split that does not come out 50/50) and tracking bugs before a real idea is judged on bad plumbing.
- Cost: it uses traffic and time without learning anything about a product idea, so teams usually run it when a new experiment platform or new metric is introduced, not for every test.
**Worked example:** Both groups see the same checkout page, true conversion 10%, 2,000 visitors per group. I simulate 2,000 such A/A tests.
**Excel / Python:**
```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

# Both groups get the SAME experience, true conversion is 10% in each
random_generator = np.random.default_rng(42)
visitors_per_group = 2000
true_conversion_rate = 0.10
number_of_aa_tests = 2000
false_alarms = 0

for test_number in range(number_of_aa_tests):
    # Simulate conversions in each group
    conversions_group_1 = random_generator.binomial(visitors_per_group, true_conversion_rate)
    conversions_group_2 = random_generator.binomial(visitors_per_group, true_conversion_rate)

    # Two-proportion z-test between the two identical groups
    z_score, p_value = proportions_ztest(
        [conversions_group_1, conversions_group_2],
        [visitors_per_group, visitors_per_group])

    # Count how often the test wrongly says "different"
    if p_value < 0.05:
        false_alarms = false_alarms + 1

print("Share of A/A tests that looked significant:", false_alarms / number_of_aa_tests)
```
Output: `Share of A/A tests that looked significant: 0.047`. About 5% as promised, so this setup is healthy.
**Likely follow-ups:** 1) *Do you run an A/A before every test?* No, only when the platform, metric or logging is new or suspected. 2) *What if an A/A comes out significant once?* That is normal 1 time in 20; repeat or check many A/A runs.
**Common mistakes:** Calling one significant A/A result a bug (it happens 5% of the time by design); skipping the check of the group sizes.

### Q32 ⭐ 🟡 What is the difference between an A/B test, an A/B/n test and a multivariate test?
**Asked at:** commonly asked (no company-specific report found); "A/B/n" is listed among recurring topics on prep sites (topic list only, pages not read in full).
**What the interviewer is checking:** Can you tell apart "several versions of one thing" from "combinations of several things", and do you know the traffic cost?
**Say this in the interview:** "An A/B test compares one control with one new version. An A/B/n test compares one control with several new versions of the same element. A multivariate test changes several elements at once and tests every combination, so it can tell me which element and which combination works, but it needs much more traffic."
**Explain simply:**
- A/B: 2 groups, one question ("is the new page better?").
- A/B/n: 3 or more groups, for example the control plus 2 or 3 button designs. More comparisons means a higher chance of a fluke, so I tighten the significance cut-off (Bonferroni: divide 0.05 by the number of comparisons).
- Multivariate: for example 2 headlines x 3 button colours = 6 combinations ("cells"), each needing its own full sample.
- Rule of thumb: every extra group costs sample size, so use A/B/n or multivariate only with lots of traffic.
**Worked example:** Baseline 10%, I want to detect 12%, power 80%. Computed below.
**Excel / Python:**
```python
import math
from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.power import NormalIndPower

# Current conversion 10%, smallest lift we care about is 10% -> 12%
baseline_rate = 0.10
target_rate = 0.12
effect_size = proportion_effectsize(target_rate, baseline_rate)
power_calculator = NormalIndPower()

# Plain A/B test: one comparison, alpha 0.05
users_ab = power_calculator.solve_power(effect_size, alpha=0.05, power=0.8)

# A/B/n with control + 2 new versions: 2 comparisons, Bonferroni alpha = 0.05 / 2
users_abn_3_arms = power_calculator.solve_power(effect_size, alpha=0.05 / 2, power=0.8)

# A/B/n with control + 3 new versions: 3 comparisons, alpha = 0.05 / 3
users_abn_4_arms = power_calculator.solve_power(effect_size, alpha=0.05 / 3, power=0.8)

print("A/B, users per group:", math.ceil(users_ab), "| total:", 2 * math.ceil(users_ab))
print("A/B/n, 3 arms, users per arm:", math.ceil(users_abn_3_arms), "| total:", 3 * math.ceil(users_abn_3_arms))
print("A/B/n, 4 arms, users per arm:", math.ceil(users_abn_4_arms), "| total:", 4 * math.ceil(users_abn_4_arms))
```
Output: `A/B, users per group: 3835 | total: 7670`, `A/B/n, 3 arms, users per arm: 4644 | total: 13932`, `A/B/n, 4 arms, users per arm: 5115 | total: 20460`. Going from 2 to 4 groups nearly triples the traffic. A 2x3 multivariate test (6 cells) needs about 6 x 3,835 = 23,010 users at the plain alpha, more with a correction.
**Likely follow-ups:** 1) *Why not just run several A/B tests?* Same fluke risk, and you cannot see interactions. 2) *When is multivariate worth it?* Only with high traffic and when elements may interact.
**Common mistakes:** Picking the best of many variants at plain 0.05; ignoring the traffic cost.

### Q33 ⭐ 🟡 How should outliers, such as a few very large orders, be handled when comparing revenue between groups?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that a few huge values can swing an average and that you must choose a robust method before looking at the result?
**Say this in the interview:** "First I check whether the outliers are errors or real big customers. Real ones I keep but tame, usually by capping (winsorising) at a high percentile, or by using a method that does not depend on extremes, like a rank test or a bootstrap. I decide the rule before the test starts so I am not picking whatever gives the nicer answer."
**Explain simply:**
- The mean is dragged by extremes: three bulk orders can move the group average by Rs 150.
- Capping (winsorising): replace anything above a high cut-off (say the 99.5th percentile) with the cut-off value.
- Rank test (Mann-Whitney): compares ordering, not size, so extremes matter little (but it answers "does one group tend to be higher?", not "is the mean higher?").
- Also consider a log transform or a bootstrap (re-sampling the data many times to see how much the difference wobbles).
- Never delete outliers just because they hurt your result; document the rule.
**Worked example:** Two groups of 1,000 orders with no real difference. Group B gets three bulk orders (Rs 60,000, 45,000, 52,000).
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Simulate order values (Rs) for two groups with no real difference
random_generator = np.random.default_rng(4)
orders_a = random_generator.lognormal(mean=6.0, sigma=0.5, size=1000).round(0)
orders_b = random_generator.lognormal(mean=6.0, sigma=0.5, size=1000).round(0)

# Add three huge bulk orders to group B only
orders_b[0] = 60000
orders_b[1] = 45000
orders_b[2] = 52000

# Compare plain averages and medians
print("Mean A:", round(orders_a.mean(), 1), "| Mean B:", round(orders_b.mean(), 1))
print("Median A:", np.median(orders_a), "| Median B:", np.median(orders_b))

# Welch t-test on raw values
p_raw = stats.ttest_ind(orders_b, orders_a, equal_var=False).pvalue
print("p-value, raw means:", round(p_raw, 3))

# Cap (winsorise) every order at the 99.5th percentile of all orders
all_orders = np.concatenate([orders_a, orders_b])
cap_value = np.percentile(all_orders, 99.5)
capped_a = np.minimum(orders_a, cap_value)
capped_b = np.minimum(orders_b, cap_value)
p_capped = stats.ttest_ind(capped_b, capped_a, equal_var=False).pvalue
print("Cap at Rs", round(cap_value, 1), "| capped means:", round(capped_a.mean(), 1), round(capped_b.mean(), 1))
print("p-value, capped:", round(p_capped, 3))

# Rank-based test that ignores how huge the biggest orders are
p_rank = stats.mannwhitneyu(orders_b, orders_a).pvalue
print("p-value, Mann-Whitney:", round(p_rank, 3))
```
Output: means Rs 455.6 vs 614.5 (but medians 399.0 vs 408.5), raw p = 0.081, capped means 455.4 vs 461.1 with p = 0.586, Mann-Whitney p = 0.473. The whole "Rs 159 gap" came from three orders; once tamed, it disappears.
**Likely follow-ups:** 1) *Is capping cheating?* Not if the rule is fixed in advance and applied to both groups. 2) *When are big orders the point?* If the business cares about revenue from whales, report both capped and uncapped.
**Common mistakes:** Removing outliers only from the group that looks bad; using plain t-test on heavy-tailed data and reporting a fluke as a win.

### Q34 ⭐ 🟡 Can you run an A/B test with an uneven split such as 90/10, and what are the trade-offs?
**Asked at:** commonly asked (no company-specific report found); related to the "60/40 split" bug question listed on prep sites (title only).
**What the interviewer is checking:** Do you know uneven splits are valid but statistically less efficient, and when they are useful?
**Say this in the interview:** "Yes, it is valid as long as assignment is random. The trade-off is that the test takes longer, because the small group limits the precision. I would use 90/10 when the change is risky and I want to limit damage, then ramp up to 50/50 if the early signs are safe."
**Explain simply:**
- The precision of the comparison is set mostly by the smaller group, so 90/10 needs far more total users than 50/50.
- Benefit: only 10% of users are exposed to a possibly bad change (risk control, safe rollout).
- A 50/50 split is the fastest way to reach a given power.
- If the split drifts from the planned ratio, that is a Sample Ratio Mismatch (SRM), a bug signal.
**Worked example:** Baseline 10%, detect 12%, power 80%, 1,000 visitors per day.
**Excel / Python:**
```python
import math
from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.power import NormalIndPower

# Baseline 10%, want to detect 12%
effect_size = proportion_effectsize(0.12, 0.10)
power_calculator = NormalIndPower()
daily_visitors = 1000

# 50/50 split: ratio = treatment size / control size = 1
control_5050 = power_calculator.solve_power(effect_size, alpha=0.05, power=0.8, ratio=1)
total_5050 = control_5050 * 2

# 90/10 split: only 10% see the new version, so treatment = control / 9
control_9010 = power_calculator.solve_power(effect_size, alpha=0.05, power=0.8, ratio=1 / 9)
treatment_9010 = control_9010 / 9
total_9010 = control_9010 + treatment_9010

print("50/50 total users:", math.ceil(total_5050), "| days:", round(total_5050 / daily_visitors, 1))
print("90/10 total users:", math.ceil(total_9010), "| days:", round(total_9010 / daily_visitors, 1))
print("90/10 treatment group size:", math.ceil(treatment_9010))
```
Output: `50/50 total users: 7670 | days: 7.7`, `90/10 total users: 21304 | days: 21.3`, `90/10 treatment group size: 2131`. The 90/10 split needs about 2.8 times the traffic.
**Likely follow-ups:** 1) *Does an uneven split bias the result?* No, only reduces precision. 2) *Can I change the split mid-test?* Avoid it; it mixes time effects with group effects (Simpson's paradox risk).
**Common mistakes:** Assuming uneven means invalid; not recomputing the sample size for the ratio.

### Q35 ⭐ 🟡 When should you not run an A/B test?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Mature judgement: you know A/B testing is a tool, not a ritual.
**Say this in the interview:** "I would not run one when there is too little traffic to reach a useful sample size, when the answer is obvious or legally required, when randomising is impossible or unethical, when the effect takes months to show up, or when users would affect each other. In those cases I use other evidence: a before-after comparison with a comparison group, qualitative research, or just a decision."
**Explain simply:**
- Too small: an HR test on 40 candidates a month cannot detect anything but giant effects.
- Obvious or mandatory: fixing a bug, a legal compliance change, a security patch.
- Cannot randomise: pay-band changes for existing staff (unfair and people talk).
- Long-term outcomes: "does onboarding improve 1-year retention?" would take a year, so choose a proxy or use observational methods.
- Interference: users influence each other (marketplaces, social features).
- Cost of the test exceeds the value of the decision.
**Worked example:** A site gets 150 visitors a day at the page; baseline conversion 10%, we want to detect 12%.
**Excel / Python:**
```python
import math
from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.power import NormalIndPower

# Small site: 150 visitors reach the page per day
daily_visitors = 150
effect_size = proportion_effectsize(0.12, 0.10)
users_per_group = NormalIndPower().solve_power(effect_size, alpha=0.05, power=0.8)
total_users_needed = 2 * math.ceil(users_per_group)
days_needed = total_users_needed / daily_visitors

print("Total users needed:", total_users_needed)
print("Days needed at 150 visitors a day:", round(days_needed, 1))
```
Output: `Total users needed: 7670`, `Days needed at 150 visitors a day: 51.1`. Seven weeks for one small question: probably not worth it.
**Likely follow-ups:** 1) *What would you do instead?* Pre-post with a control group, user interviews, or a bigger bolder change. 2) *Is a test ever required?* Not required, but wise when the change is risky and reversible.
**Common mistakes:** Treating every decision as a test; running a test that cannot possibly detect the effect.

### Q36 ⭐ 🔴 Why is slicing an A/B test result into many segments after the test dangerous?
**Asked at:** commonly asked (no company-specific report found); the multiple comparisons theme is listed on prep sites (titles only).
**What the interviewer is checking:** Do you understand that every extra look at the data is another chance for a fluke?
**Say this in the interview:** "If I slice the result by 20 segments (device, city, new vs old users and so on), the chance that at least one shows 'significant' purely by luck is about 64%. So a lone winning segment found after the fact is not evidence. I would treat it as an idea for a follow-up test, and plan important segments before the test starts."
**Explain simply:**
- Each test has a 5% false alarm rate. With 20 independent looks, the chance of at least one false alarm is 1 minus 0.95 to the power 20.
- Segments are also smaller, so they are noisy and swing widely.
- Fixes: pre-register a few segments of interest; adjust the cut-off (Bonferroni: 0.05 divided by number of looks); report all slices, not only the winners; confirm in a new test.
- This is sometimes called "p-hacking" or "the garden of forking paths".
**Formula in plain words:** Chance of at least one false alarm = 1 minus (1 minus alpha) raised to the number of tests. Here 1 - 0.95^20.
**Worked example:** Test with NO real effect, sliced into 20 segments of 300 users per arm. I check by calculation and by simulation.
**Excel / Python:** Excel check: `=1-0.95^20` returns 0.642 (any version; not run in Excel here).
```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

# Chance of at least one false alarm across 20 segments (no real effect anywhere)
number_of_segments = 20
chance_one_false_alarm = 1 - 0.95 ** number_of_segments
print("Calculated chance of >=1 false alarm:", round(chance_one_false_alarm, 3))

# Simulate: 2000 experiments with NO real effect, each sliced into 20 segments
random_generator = np.random.default_rng(1)
users_per_segment = 300
experiments_with_a_false_alarm = 0
number_of_experiments = 2000

for experiment in range(number_of_experiments):
    found_one = False
    for segment in range(number_of_segments):
        conversions_control = random_generator.binomial(users_per_segment, 0.10)
        conversions_treatment = random_generator.binomial(users_per_segment, 0.10)
        both_zero = conversions_control + conversions_treatment == 0
        if both_zero:
            continue
        z_score, p_value = proportions_ztest(
            [conversions_control, conversions_treatment],
            [users_per_segment, users_per_segment])
        if p_value < 0.05:
            found_one = True
            break
    if found_one:
        experiments_with_a_false_alarm = experiments_with_a_false_alarm + 1

print("Simulated share with >=1 'significant' segment:", experiments_with_a_false_alarm / number_of_experiments)
```
Output: `Calculated chance of >=1 false alarm: 0.642` and `Simulated share with >=1 'significant' segment: 0.644`. In plain words: with 20 slices and no real effect, about two experiments in three will still show a fake "winning" segment.
**Likely follow-ups:** 1) *Is segment analysis never allowed?* It is allowed for exploration; label it so and confirm later. 2) *What is Bonferroni?* Divide alpha by the number of looks (0.05/20 = 0.0025).
**Common mistakes:** Reporting only the segment that "won"; forgetting that small segments have wide uncertainty.

### Q37 ⭐ 🔴 What is the winner's curse, and why does a launched lift often turn out smaller than the test showed?
**Asked at:** commonly asked (no company-specific report found); the idea is discussed in Kohavi-style experimentation material (known only from summaries, not read in full).
**What the interviewer is checking:** Do you see that picking the best of many noisy results selects for good luck?
**Say this in the interview:** "Every measured lift is true effect plus luck. If I pick the winner out of many variants, or stop at a lucky peak, I tend to pick the one with the best luck, so its measured lift overstates the truth. After launch the luck does not repeat, so the real lift is smaller. It is called regression to the mean."
**Explain simply:**
- Tests with small samples are noisy; the noise is as big as the effect.
- Choosing the maximum among many noisy numbers is biased upward.
- Other causes: peeking and stopping early on a high, novelty effect fading, and segments chosen after the fact.
- Remedies: bigger samples, fewer variants, a confirmation (holdout) test, and shrinking the expected lift when forecasting.
**Worked example:** 20 variants whose true lifts are tiny (average 0, spread 0.3 points); each measured with noise of 0.5 points. I repeat the whole process 5,000 times and always pick the best-looking variant.
**Excel / Python:**
```python
import numpy as np

# 20 variants tested; true lifts are small (average 0%, spread 0.3 percentage points)
# Each test measures its lift with noise (spread 0.5 percentage points)
random_generator = np.random.default_rng(3)
number_of_variants = 20
number_of_repeats = 5000
winner_measured_lifts = []
winner_true_lifts = []

for repeat in range(number_of_repeats):
    # The real (unknown) lift of each variant
    true_lifts = random_generator.normal(0.0, 0.3, number_of_variants)
    # What the experiment measures = truth + random noise
    measured_lifts = true_lifts + random_generator.normal(0.0, 0.5, number_of_variants)
    # Pick the variant that looks best, as a team would
    best_variant = measured_lifts.argmax()
    winner_measured_lifts.append(measured_lifts[best_variant])
    winner_true_lifts.append(true_lifts[best_variant])

print("Average measured lift of the winner:", round(np.mean(winner_measured_lifts), 2))
print("Average TRUE lift of the winner:", round(np.mean(winner_true_lifts), 2))
```
Output: `Average measured lift of the winner: 1.09`, `Average TRUE lift of the winner: 0.28`. The winner looked about four times better than it really was.
**Likely follow-ups:** 1) *How to forecast the launch impact?* Use the confidence interval's lower half, or discount the lift; confirm with a holdout. 2) *Does a single A/B test suffer too?* Less so, but peeking and a significance filter still inflate "winning" results.
**Common mistakes:** Promising the full tested lift to finance; running many variants and quoting the best one.

### Q38 ⭐ 🔴 What are network effects or interference between users, and how do they break an A/B test?
**Asked at:** commonly asked (no company-specific report found); network effects/interference appears as a recurring topic on aggregator pages (PracHub, Dataford; titles only).
**What the interviewer is checking:** Do you know the key assumption that one user's outcome does not depend on others' group, and what to do when it fails?
**Say this in the interview:** "A/B tests assume users do not affect each other. In a marketplace, a social app or a delivery service, they do: treated users can use up shared stock or drivers, or influence friends in the control group. Then the test result does not match what happens when everyone gets the change. I would randomise in clusters (whole cities or friend groups), or by time, rather than by individual."
**Explain simply:**
- Interference (also called spillover or SUTVA violation, "stable unit treatment value assumption"): my result depends on who else is treated.
- Examples: a discount draws limited delivery slots toward treated users, starving control; a feature spreads by word of mouth to control users; an HR wellness challenge where teammates join in.
- Effect: the measured gap can be too large (control hurt) or too small (control contaminated).
- Fixes: cluster randomisation (assign whole cities, teams or networks), switchback tests (alternate the whole market on and off over time periods), or geo experiments.
**Worked example:** A shared stock of 100 delivery slots; 1,000 users order with probability 8% normally and 12% with the new offer. In the test, half get the offer; at launch, everyone does.
**Excel / Python:**
```python
# Delivery slots are limited to 100 in total
available_slots = 100

# Test world: 500 users get the offer (12%), 500 do not (8%)
treatment_orders = 500 * 0.12
control_orders = 500 * 0.08
measured_lift = treatment_orders / control_orders - 1

# Launch world: all 1000 users get the offer, but supply caps orders at 100
launch_orders = min(1000 * 0.12, available_slots)
old_orders = 1000 * 0.08
real_lift = launch_orders / old_orders - 1

print("Orders in test, treatment vs control:", treatment_orders, "vs", control_orders)
print("Measured lift in test:", round(measured_lift, 2))
print("Real lift at launch:", round(real_lift, 2))
```
Output: `Orders in test, treatment vs control: 60.0 vs 40.0`, `Measured lift in test: 0.5`, `Real lift at launch: 0.25`. The test promised +50%, but supply limits reality to +25%. (This is a simplified toy model, not real data.)
**Likely follow-ups:** 1) *What is a switchback test?* Switch the whole market between versions in alternating time blocks. 2) *Can you detect interference?* Compare results across clusters with different treated shares.
**Common mistakes:** Ignoring shared resources; randomising individuals in a social product.

### Q39 ⭐ 🔴 How do you analyse a ratio metric such as click-through rate when users have different numbers of sessions?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you realise sessions from the same user are not independent, so the naive formula understates uncertainty?
**Say this in the interview:** "The randomisation unit is the user, but the click-through rate (CTR, clicks divided by sessions) is counted per session. Sessions from one user are related, so treating each session as independent makes my error bars too narrow and creates false wins. I use the delta method, which calculates the variance from user-level numbers, or I bootstrap by user, or I analyse a per-user metric."
**Explain simply:**
- Ratio metric: total clicks divided by total sessions, where both numerator and denominator vary per user.
- Heavy users contribute many sessions and share the same click habit, so sessions are correlated.
- Naive test: treats every session as a separate coin flip, so the standard error is too small and false alarms rise above 5%.
- Delta method: a formula that approximates the variance of a ratio from user-level data. Alternatives: user-level bootstrap, or per-user averages (each user counts equally, which answers a slightly different question).
**Formula in plain words:** For each user, residual = clicks minus (overall CTR x sessions). Variance of CTR = variance of residuals / (number of users x average sessions squared).
**Worked example:** An A/A simulation: 500 users per group, sessions about 4 per user, each user with their own click habit. I count how often each method wrongly says "significant".
**Excel / Python:**
```python
import numpy as np

def ctr_and_variance(clicks_per_user, sessions_per_user):
    """Return overall CTR and its variance using the delta method."""
    number_of_users = len(clicks_per_user)
    # Overall CTR = total clicks / total sessions
    overall_ctr = clicks_per_user.sum() / sessions_per_user.sum()
    # Each user's "residual": clicks minus what the overall CTR predicts, scaled by average sessions
    residual_per_user = (clicks_per_user - overall_ctr * sessions_per_user) / sessions_per_user.mean()
    # Variance of the CTR, based on variation between USERS
    variance_of_ctr = residual_per_user.var(ddof=1) / number_of_users
    return overall_ctr, variance_of_ctr

# A/A simulation: same behaviour in both groups, but users differ a lot in click habit
random_generator = np.random.default_rng(5)
number_of_tests = 1000
users_per_group = 500
naive_false_alarms = 0
delta_false_alarms = 0

for test_number in range(number_of_tests):
    # Sessions per user (at least 1) and each user's own click habit
    sessions_a = random_generator.poisson(3, users_per_group) + 1
    sessions_b = random_generator.poisson(3, users_per_group) + 1
    habit_a = random_generator.beta(1, 9, users_per_group)
    habit_b = random_generator.beta(1, 9, users_per_group)
    clicks_a = random_generator.binomial(sessions_a, habit_a)
    clicks_b = random_generator.binomial(sessions_b, habit_b)

    ctr_a, variance_a = ctr_and_variance(clicks_a, sessions_a)
    ctr_b, variance_b = ctr_and_variance(clicks_b, sessions_b)
    gap = ctr_b - ctr_a

    # Correct way: z-score using user-level variance (delta method)
    z_delta = gap / np.sqrt(variance_a + variance_b)

    # Naive way: treat every session as an independent coin flip
    naive_se = np.sqrt(ctr_a * (1 - ctr_a) / sessions_a.sum() + ctr_b * (1 - ctr_b) / sessions_b.sum())
    z_naive = gap / naive_se

    if abs(z_delta) > 1.96:
        delta_false_alarms = delta_false_alarms + 1
    if abs(z_naive) > 1.96:
        naive_false_alarms = naive_false_alarms + 1

print("False alarm rate, naive session-level test:", naive_false_alarms / number_of_tests)
print("False alarm rate, delta method:", delta_false_alarms / number_of_tests)
```
Output: `False alarm rate, naive session-level test: 0.094`, `False alarm rate, delta method: 0.062`. Naive nearly doubles the promised 5%; the delta method is much closer (the small remaining excess is simulation noise and small samples).
**Likely follow-ups:** 1) *Why not average each user's own CTR?* You can, but light users then count as much as heavy ones; that is a different question. 2) *Simplest safe option?* Bootstrap by user.
**Common mistakes:** Using a session-level proportion test; randomising by user but analysing by session.

### Q40 ⭐ 🔴 What is the difference between frequentist and Bayesian A/B testing?
**Asked at:** commonly asked (no company-specific report found); "Bayesian vs frequentist" is listed among topics on Interview Query (topic list only, page not read in full).
**What the interviewer is checking:** Can you explain both approaches in plain words, including what each result number means?
**Say this in the interview:** "Frequentist testing asks: if there were truly no difference, how surprising is my data? That gives a p-value. Bayesian testing asks directly: given my data and what I believed before, how likely is it that B is better, and by how much? Bayesian output is easier for managers to read, but it depends on the prior belief, and both approaches still need good design."
**Explain simply:**
- Frequentist: fixed sample size decided up front; results are a p-value and a confidence interval. A p-value is not the probability B is better.
- Bayesian: start with a prior (belief before data, often "flat"), update with data to get a posterior, from which you read "chance B beats A" and a credible interval (a range holding the lift with 95% probability).
- Bayesian is not magic: it does not remove peeking-style concerns entirely, and a strongly chosen prior changes the answer.
- In practice with big samples and a flat prior both approaches give similar decisions.
**Worked example:** A converted 200 of 2,000; B converted 240 of 2,000.
**Excel / Python:**
```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

# Data: A converted 200 of 2000, B converted 240 of 2000
# Start with a flat prior Beta(1,1); posterior = Beta(1 + converted, 1 + not converted)
random_generator = np.random.default_rng(2)
draws_a = random_generator.beta(1 + 200, 1 + 1800, 200000)
draws_b = random_generator.beta(1 + 240, 1 + 1760, 200000)

# Share of draws where B's conversion rate beats A's
probability_b_better = (draws_b > draws_a).mean()
lift_draws = draws_b - draws_a
lower, upper = np.percentile(lift_draws, [2.5, 97.5])

# Frequentist answer for comparison
z_score, p_value = proportions_ztest([240, 200], [2000, 2000])

print("Bayesian: chance B is better than A:", round(probability_b_better, 3))
print("Bayesian: 95% credible range for lift (pp):", round(lower * 100, 2), "to", round(upper * 100, 2))
print("Frequentist p-value:", round(p_value, 3))
```
Output: `Bayesian: chance B is better than A: 0.979`, `95% credible range for lift (pp): 0.07 to 3.94`, `Frequentist p-value: 0.043`. Same story: B is probably better, but the lift could be tiny.
**Likely follow-ups:** 1) *Which is better?* Neither always; pick one, fix the rules before the test, and explain results clearly. 2) *What is a prior?* Your starting belief expressed as a distribution.
**Common mistakes:** Saying a p-value of 0.043 means a 95.7% chance B is better; thinking Bayesian lets you peek with no consequences.

### Q41 ⭐ 🔴 What is CUPED or variance reduction, and why does it help?
**Asked at:** commonly asked (no company-specific report found); an advanced topic, likely only in experimentation-heavy product-analytics roles (from memory, unverified).
**What the interviewer is checking:** Do you understand that using pre-experiment data removes predictable noise and speeds up tests?
**Say this in the interview:** "CUPED (Controlled-experiment Using Pre-Experiment Data) adjusts each user's outcome by what we would have expected from their behaviour before the test. A customer who spent a lot last month will probably spend a lot this month regardless of my change, so that part is noise. Removing it shrinks the variance, so the test reaches a clear answer with fewer users or less time."
**Explain simply:**
- Variance reduction: make results less noisy without more data.
- Adjusted outcome = outcome minus theta x (pre-experiment value minus its average). Theta is the slope of outcome versus pre-experiment value.
- It only works when the pre-experiment metric is correlated with the outcome. The variance falls by about the correlation squared.
- The pre-period data must be measured before the test starts, so it cannot be affected by the change.
- It does not change the true effect, it just measures it more sharply.
**Formula in plain words:** Adjusted value = actual value minus theta x (that person's pre-test value minus the average pre-test value). Variance kept ≈ 1 minus correlation squared.
**Worked example:** 4,000 customers; last month's spend predicts this month's spend (correlation about 0.83).
**Excel / Python:**
```python
import numpy as np

# 4000 customers: spend last month (pre) and this month (post); treatment adds about Rs 8
random_generator = np.random.default_rng(8)
users_per_group = 2000
spend_before = random_generator.normal(500, 120, 2 * users_per_group)
spend_after = 0.7 * spend_before + random_generator.normal(150, 60, 2 * users_per_group)
is_treatment = np.array([0] * users_per_group + [1] * users_per_group)
spend_after = spend_after + is_treatment * 8

def difference_and_error(values):
    control_values = values[is_treatment == 0]
    treatment_values = values[is_treatment == 1]
    difference = treatment_values.mean() - control_values.mean()
    std_error = np.sqrt(control_values.var(ddof=1) / users_per_group + treatment_values.var(ddof=1) / users_per_group)
    return difference, std_error

# Plain comparison
plain_difference, plain_error = difference_and_error(spend_after)

# CUPED: remove the part of spend explained by pre-experiment spend
theta = np.cov(spend_after, spend_before)[0, 1] / spend_before.var(ddof=1)
adjusted_spend = spend_after - theta * (spend_before - spend_before.mean())
cuped_difference, cuped_error = difference_and_error(adjusted_spend)

correlation = np.corrcoef(spend_after, spend_before)[0, 1]
print("Correlation before/after:", round(correlation, 2))
print("Plain: difference", round(plain_difference, 1), "| standard error", round(plain_error, 2))
print("CUPED: difference", round(cuped_difference, 1), "| standard error", round(cuped_error, 2))
print("Variance kept:", round(adjusted_spend.var() / spend_after.var(), 2))
```
Output: `Correlation before/after: 0.83`, `Plain: difference 10.6 | standard error 3.34`, `CUPED: difference 6.5 | standard error 1.86`, `Variance kept: 0.31` (matches 1 - 0.83^2). The error bar shrank by about 45%; the true effect I built in is Rs 8, and the plain estimate was off by chance (10.6) more than the adjusted one (6.5).
**Likely follow-ups:** 1) *Does it work for new users?* No; it needs pre-period history. 2) *Is it the same as regression adjustment?* It is a special case of adding a pre-test covariate.
**Common mistakes:** Using a covariate measured after the test started; expecting big gains when the pre-period metric is barely correlated.

### Q42 ⭐ 🔴 What is sequential testing, and how does it differ from fixed-horizon testing?
**Asked at:** commonly asked (no company-specific report found); peeking questions are listed on prep aggregators (titles only), sequential methods are the standard answer.
**What the interviewer is checking:** Do you know there is a statistically valid way to look at results early?
**Say this in the interview:** "Fixed-horizon testing fixes the sample size in advance and gives one valid look, at the end. Sequential testing plans several looks and uses stricter cut-offs, so I can stop early for a clear win or loss while keeping the false-alarm rate at 5%. It is the correct fix for the peeking problem."
**Explain simply:**
- Fixed horizon: decide sample size and end date up front, do not make decisions before.
- Sequential: use a "spending" plan for the 5% false alarm budget across planned looks (Pocock: same stricter cut-off at each look; O'Brien-Fleming: very strict early, relaxed late; or "always valid" methods like mSPRT).
- Gain: can stop early when the effect is big or clearly harmful, saving time and protecting users.
- Cost: slightly more users in the worst case, and extra complexity; analysis tools must support it.
**Worked example:** An A/A experiment checked at 5 looks (every 400 users per group), 20,000 simulated repeats.
**Excel / Python:**
```python
import numpy as np

# 20000 A/A experiments (no real effect), checked at 5 equally spaced looks
random_generator = np.random.default_rng(21)
number_of_experiments = 20000
number_of_looks = 5
users_per_look = 400
fixed_false_alarms = 0
peeking_false_alarms = 0
adjusted_false_alarms = 0

for experiment in range(number_of_experiments):
    control_values = random_generator.normal(0, 1, number_of_looks * users_per_look)
    treatment_values = random_generator.normal(0, 1, number_of_looks * users_per_look)

    z_scores = []
    for look in range(1, number_of_looks + 1):
        users_so_far = look * users_per_look
        gap = treatment_values[:users_so_far].mean() - control_values[:users_so_far].mean()
        z_scores.append(gap / np.sqrt(2 / users_so_far))
    z_scores = np.array(z_scores)

    # Fixed horizon: look once, at the end, with the usual 1.96 cut-off
    if abs(z_scores[-1]) > 1.96:
        fixed_false_alarms = fixed_false_alarms + 1
    # Peeking: stop the first time ANY look crosses 1.96
    if (np.abs(z_scores) > 1.96).any():
        peeking_false_alarms = peeking_false_alarms + 1
    # Sequential (Pocock-style): stricter cut-off 2.413 at every look
    if (np.abs(z_scores) > 2.413).any():
        adjusted_false_alarms = adjusted_false_alarms + 1

print("Fixed horizon false alarms:", fixed_false_alarms / number_of_experiments)
print("Peeking at 1.96:", peeking_false_alarms / number_of_experiments)
print("Sequential, cut-off 2.413:", adjusted_false_alarms / number_of_experiments)
```
Output: `Fixed horizon false alarms: 0.0511`, `Peeking at 1.96: 0.13775`, `Sequential, cut-off 2.413: 0.04905`. Peeking nearly triples the false alarms; the stricter cut-off restores 5%. (2.413 is the standard Pocock value for 5 looks at 5%, taken as known, and confirmed by this simulation.)
**Likely follow-ups:** 1) *Does sequential testing let me peek daily?* Only as many times as planned, or with an always-valid method. 2) *Is it the same as Bayesian stopping?* No; it is still frequentist, with controlled false alarms.
**Common mistakes:** Peeking using the ordinary 1.96 cut-off; changing the number of looks after seeing data.

### Q43 ⭐ 🔴 How would you measure the impact of a change when randomisation is not possible?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the main quasi-experimental methods and their assumptions, and are you honest about their weakness compared with a randomised test?
**Say this in the interview:** "I look for a fair comparison group. The most common method is difference-in-differences: compare the change over time in the affected group with the change in a similar unaffected group. Other options are matching, synthetic control, regression discontinuity (a cut-off rule) and interrupted time series. All are weaker than randomisation because they rest on assumptions I must check and state."
**Explain simply:**
- Why not just before versus after? Other things change over time (season, hiring cycles), so the gap is not clearly caused by the change.
- Difference-in-differences (DiD): effect = change in treated group minus change in comparison group. Key assumption: both would have moved in parallel without the change ("parallel trends"), which I check with earlier periods.
- Matching: compare treated with look-alike people on key traits; only controls for what I measure.
- Synthetic control: build a weighted blend of other units that tracks the treated unit before the change.
- Regression discontinuity: compare people just above and just below an eligibility cut-off.
**Worked example:** HR rolls a new interview-reminder process to the Hyderabad office only. Average no-show rate: Hyderabad 22% before and 15% after; other offices 21% before and 19% after.
**Excel / Python:** Excel check: with before and after rates in B2:C3, `=(C2-B2)-(C3-B3)` (any version; not run in Excel here).
```python
# Average no-show rate (%) in the office that got the new process (pilot) vs others
pilot_before = 22.0
pilot_after = 15.0
other_before = 21.0
other_after = 19.0

# Change in each group
pilot_change = pilot_after - pilot_before
other_change = other_after - other_before

# Difference-in-differences: pilot's change minus what happened anyway
effect_estimate = pilot_change - other_change

print("Pilot change:", pilot_change, "points")
print("Other offices change:", other_change, "points")
print("Estimated effect of the change:", effect_estimate, "points")
```
Output: `Pilot change: -7.0 points`, `Other offices change: -2.0 points`, `Estimated effect of the change: -5.0 points`. Without the comparison I would have wrongly credited the process with 7 points.
**Likely follow-ups:** 1) *How do you check parallel trends?* Plot several periods before the change; the lines should move together. 2) *Can you prove causation?* No, only make it more credible; say so.
**Common mistakes:** Simple before-after comparison; choosing a comparison group that was already trending differently; presenting the result as certain.
