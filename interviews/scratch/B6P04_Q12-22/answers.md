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
**Say this first (1 line):** A 5% lift at a 2% baseline needs about 315,000 users per arm, which is 79 months at 4,000 per arm per month (the prompt's 300,000 and 75 months are round figures), so I would say a classic A/B test cannot answer this question; I would show what the traffic can detect and offer a bigger lift, a more frequent metric, variance reduction, more pages, or a no-test decision.
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
