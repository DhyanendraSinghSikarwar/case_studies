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
