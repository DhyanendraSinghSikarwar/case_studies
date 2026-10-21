# Book 1 - Part 10: A/B Testing, Causal Inference & Experimentation (Question List)

**Topic:** experiment design, metrics, randomization units, SRM, novelty, interference, multiple testing, peeking, switchback, DiD, propensity scores, IV, RDD, uplift, observational vs experimental, ambiguous results, GenAI experimentation.
**Target:** 50  |  **Actual:** 56  (3-star 19, 2-star 27, 1-star 10)  |  **Date:** 2026-10-20
**Scope note:** power/sample-size derivations, sequential testing, CUPED, variance reduction and Bayesian stats are owned by Parts 13-14; questions here are interview-use level only.
**Status:** Phase 1 (questions only, answers pending).

> Dedupe pass: removed 2 cross-part duplicate(s); renumbered Q1–Q56.
---

### Q1 ⭐⭐⭐ 🟢 Walk me through how you would design an A/B test end to end (hypothesis, metrics, unit, sample size, duration, decision rule).
**Asked at:** Product cos, Flipkart, Swiggy, Spotify, Booking, Zalando, GCCs
**Say this first (1 line):** I write down the decision first, then pick the hypothesis, metrics, randomization unit, sample size and duration, and fix the decision rule before launch, not after seeing data.

**Then explain:**
1. **Hypothesis and decision:** "Showing delivery ETA on the cart page will raise checkout conversion by at least 2% relative." Also state what we do if it wins, loses or is flat.
2. **Metrics:** one primary (conversion), a few guardrails (latency, cancellations, refunds, revenue per user), and some diagnostic secondaries.
3. **Unit:** usually user (logged-in id), so a person sees one experience. Analysis unit should match the randomization unit.
4. **Sample size:** from baseline rate, minimum detectable effect (MDE, the smallest lift worth detecting), alpha (5%) and power (80%). Then duration = users needed / eligible traffic per day, rounded up to full weeks to cover weekday/weekend cycles.
5. **Pre-launch checks:** A/A or logging check, 50/50 split, SRM check once live.
6. **Decision rule (written down):** two-sided test at 5%, no peeking-based stopping, ship if primary is positive and CI lower bound is above the practical threshold and no guardrail is breached.
7. **After:** read CI, check segments only as exploration, document, decide on rollout and a holdout.

**Example:** Baseline conversion 10%, MDE 5% relative (10% to 10.5%) needs about 58k users per arm. At 20k eligible users a day that is about 6 days, so I run 14 days (two full weekly cycles).

**Follow-ups:**
- *What if traffic is low?* Raise the MDE, use a more sensitive metric, use variance reduction (CUPED, Part 13), or run longer.
- *Why full weeks?* Behaviour differs by weekday; stopping mid-week biases the sample.

**Common mistakes:** choosing metrics after seeing results, no MDE, stopping when p crosses 0.05, randomizing by session but analysing by user, skipping guardrails.

### Q2 ⭐⭐⭐ 🟢 What is an A/B test and when should you NOT run one?
**Asked at:** Product cos, Amazon, Microsoft IDC, Booking
**Say this first (1 line):** An A/B test randomly splits users into control and treatment so any difference in outcome can be attributed to the change; I would not run one when randomization is impossible, traffic is too small, the effect is obvious or harmful, or the cost of the test is bigger than the decision.

**Then explain:**
- Randomization makes the groups comparable on everything, seen and unseen, so a difference is causal.
- **Do not run it when:**
  - Traffic is too low to detect a meaningful effect in a reasonable time (use qualitative research or a bigger-MDE decision).
  - It is a legal, security or bug fix: just ship it.
  - Ethics or fairness issues (denying a safety feature, discriminatory pricing).
  - The outcome is long-term and slow (brand, trust): need holdouts or quasi-experiments instead.
  - Strong interference (network effects) makes user-level split invalid.
  - One-off events (a launch, a rebrand) that cannot be split.
  - Novelty-driven or very small changes where the engineering cost exceeds the value.

**Example:** A new payment-page bug fix: ship. A new recommendation widget on a high-traffic page: test. A city-wide delivery fee change where drivers are shared: user-level A/B is biased, use geo or switchback.

**Follow-ups:**
- *What do you do instead?* Quasi-experiments (diff-in-diff, synthetic control), user research, or pre/post with caution.

**Common mistakes:** saying "always test everything", forgetting power, ignoring interference, treating a test as proof of long-term effect.

### Q3 ⭐⭐⭐ 🟢 How do you choose the primary metric, guardrail metrics and secondary metrics for an experiment? Give an example.
**Asked at:** Spotify, Zalando, Swiggy, Flipkart, PhonePe
**Say this first (1 line):** The primary metric is the one number that decides ship or no-ship and should reflect the goal of the change; guardrails protect things we must not hurt; secondary metrics help explain why.

**Then explain:**

| Type | Role | Properties |
|---|---|---|
| Primary | decision | one metric, sensitive, tied to the hypothesis, measurable in the test window |
| Guardrail | safety | latency, crash rate, cancellations, refunds, support tickets, revenue per user |
| Secondary / diagnostic | explanation | funnel steps, clicks, time on page |

- A good primary is sensitive (moves quickly), directional, and not easily gamed. Often a proxy for the long-term goal (for example 7-day orders instead of yearly LTV).
- Guardrails have non-inferiority thresholds ("cancellation rate must not rise by more than 0.2 pp").
- More metrics means more false positives, so only the primary decides; others are corrected or treated as exploratory.

**Example (food delivery, new "reorder" button):** primary = orders per user in 14 days; guardrails = delivery time, cancellation rate, average order value, app crashes; secondary = reorder-button clicks, search usage.

**Follow-ups:**
- *Primary conflicts with guardrail?* Guardrail breach beats a primary win unless leadership accepts the trade-off explicitly (see Q13).
- *Why not clicks as primary?* Clicks are easy to inflate and may not mean value.

**Common mistakes:** several "primary" metrics, picking the metric after seeing results, only vanity metrics, no guardrails.

### Q4 ⭐⭐⭐ 🟢 What is the randomization unit? How do you choose between user-, session-, device-, request- and cluster-level randomization?
**Asked at:** Booking, Spotify, Uber-style marketplaces, Amazon
**Say this first (1 line):** The randomization unit is the thing I assign to a variant; I pick the unit that matches how the metric is defined and that stops one unit's treatment from leaking into another.

**Then explain:**

| Unit | Use when | Risk |
|---|---|---|
| User (logged-in id) | most product features, long-term metrics | cross-device users if id missing |
| Device / cookie | logged-out traffic | same person on two devices sees both variants |
| Session | quick UI tweaks with no memory | same user sees both, inconsistent experience, correlated sessions |
| Request | stateless services like ranking latency, ad serving | no user consistency, metrics need care |
| Cluster / geo / time | network effects, marketplaces, shared supply | few units, low power, higher variance |

- Rule: analysis unit should equal randomization unit, otherwise standard errors are wrong (see Q27).
- Assign by hashing the unit id with an experiment salt so assignment is sticky and reproducible.

**Example:** A new search ranker: randomize by user so a customer gets a consistent experience across days. A new driver-dispatch rule: randomize by city-hour (switchback) because riders share the same drivers.

**Follow-ups:**
- *Why not session level for retention?* The same user would be in both arms and retention is a user metric.
- *Why not always cluster?* Fewer units means much lower power.

**Common mistakes:** randomize by session but compute per-user metrics, ignore logged-out/cross-device leakage, cluster randomization analysed as if individual.

### Q5 ⭐⭐⭐ 🟢 How do you decide how long to run an experiment and how many users you need? (interview-level: which inputs drive sample size; derivations are in Part 13)
**Asked at:** All product cos, Zalando, Swiggy, Flipkart
**Say this first (1 line):** Sample size depends on four inputs: baseline rate (or variance), the minimum effect I care about, alpha and power; duration is then users needed divided by daily eligible traffic, rounded up to whole weeks.

**Then explain:**
- **Smaller MDE means much more data:** n grows with 1/MDE squared, so halving the detectable lift needs about 4x users.
- **Higher variance or a baseline nearer 50% needs more users.** Noisy metrics like revenue need far more than conversion.
- **Stricter alpha or higher power needs more users** (5% and 80% are the usual defaults).
- **Duration:** at least one, ideally two full weekly cycles, plus enough time to see novelty wear off. Never end early because the result "looks significant".
- Splitting traffic across more variants or segments lowers per-arm traffic, so time goes up.

**Example:** Baseline 10%, MDE 5% relative, alpha 0.05, power 0.8 gives about 57.8k users per arm.

**Code:**
```python
import numpy as np
from scipy.stats import norm

def n_per_arm(p, mde_rel, alpha=0.05, power=0.8):
    p2 = p * (1 + mde_rel); pbar = (p + p2) / 2
    za, zb = norm.ppf(1 - alpha / 2), norm.ppf(power)
    return int(np.ceil(2 * pbar * (1 - pbar) * (za + zb) ** 2 / (p2 - p) ** 2))

n = n_per_arm(0.10, 0.05)
print(n, "per arm;", "days at 20k users/day total:", np.ceil(2 * n / 20000))
# 57764 per arm; days at 20k users/day total: 6.0
```

**Follow-ups:**
- *Not enough traffic?* Accept a bigger MDE, use variance reduction (CUPED), pick a more sensitive metric, or run longer.
- *Why round to weeks?* Weekday/weekend behaviour differs.

**Common mistakes:** no MDE ("just run until significant"), computing power after the fact, ignoring the weekly cycle, forgetting that eligible traffic (not total traffic) sets the clock.

### Q6 ⭐⭐⭐ 🟡 What is a Sample Ratio Mismatch (SRM)? How do you detect it and what are the common causes?
**Asked at:** Microsoft, Spotify, Booking, Zalando, product cos
**Say this first (1 line):** SRM means the observed split of users between arms differs from the planned split by more than chance allows; it signals a broken experiment, so I do not trust the results until it is explained.

**Then explain:**
- **Detect:** chi-square goodness-of-fit test of observed counts vs planned ratio. Use a strict threshold (p < 0.001) because it is a health check run on every test.
- **Common causes:**
  - Bug in assignment or bucketing (hash collisions, bad salt).
  - Logging loss that differs by arm (treatment page is slower so the event is not fired before the user leaves).
  - Bots or filters applied after assignment that hit arms differently.
  - Redirects in one arm, crashes in one arm, caching.
  - Triggering/exposure logic that differs between arms; users joining or leaving on different timelines.
- **Action:** stop, find the root cause, fix and rerun. Do not "adjust" the numbers.

**Example:** Planned 50/50, observed 50,600 vs 49,000 users.

**Code:**
```python
from scipy.stats import chisquare
obs = [50_600, 49_000]
stat, p = chisquare(obs, f_exp=[sum(obs) / 2] * 2)
print(round(stat, 1), p)   # 25.7  3.98e-07  -> SRM, investigate
```
A 1.6% gap (1,600 users out of 99,600) looks small but p is about 4e-7, so it is not luck.

**Follow-ups:**
- *Can you still analyse it?* Segment by platform/country/browser to find where the mismatch lives, but results are unreliable until the cause is fixed.
- *Why strict threshold?* Many tests run daily, so p < 0.05 would raise false alarms constantly.

**Common mistakes:** ignoring a "small" mismatch, running SRM only on the final day, using a t-test on counts, trying to reweight to fix it.

### Q7 ⭐⭐⭐ 🟡 The A/B test shows a significant lift but the PM wants to stop the test after 3 days. What is wrong with peeking and what do you do?
**Asked at:** Product cos, Zalando, Swiggy, Amazon
**Say this first (1 line):** Checking the p-value repeatedly and stopping the first time it dips below 0.05 inflates false positives far above 5%, so I would not stop at day 3 unless the test was designed for sequential monitoring.

**Then explain:**
- A fixed-horizon test guarantees 5% false positives only if you look once, at the planned sample size.
- Early data is noisy: p-values wander, so some day will cross 0.05 by chance.
- Day 3 also misses the weekly cycle and novelty effects.
- **What I do:**
  - Explain to the PM with a number: simulation below shows daily peeking turns 5% into over 20%.
  - Offer sequential methods (alpha-spending, group-sequential, always-valid p-values, Part 14) if early stopping is a real business need.
  - Allow early stopping for harm (guardrail breach), with pre-set rules.
  - Otherwise wait for the planned duration.

**Example:** Two identical arms (no true effect), 14 daily looks.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
sims, days, n = 2000, 14, 500            # users per arm per day, NO true effect
fp = 0
for _ in range(sims):
    ca = rng.binomial(n, 0.1, days).cumsum(); cb = rng.binomial(n, 0.1, days).cumsum()
    N = n * np.arange(1, days + 1)
    pa, pb, pp = ca / N, cb / N, (ca + cb) / (2 * N)
    z = (pb - pa) / np.sqrt(2 * pp * (1 - pp) / N)
    fp += (np.abs(z) > 1.96).any()
print("false positive rate with daily peeking:", fp / sims)   # about 0.22
```

**Follow-ups:**
- *Can I ever peek?* Yes, with a sequential design or alpha-spending; or monitor only SRM/guardrails.
- *Why not just use a lower alpha?* It helps but a fixed lower alpha at every look is crude; proper spending is better.

**Common mistakes:** "it is already significant, why wait", peeking at several metrics, thinking Bayesian posteriors are immune to stopping rules without a defined decision rule.

### Q8 ⭐⭐⭐ 🟡 What is the novelty effect and the primacy effect? How do you detect them and what do you do about them?
**Asked at:** Zalando, Spotify, Booking, product cos
**Say this first (1 line):** Novelty effect is a short-term lift because users are curious about something new; primacy effect is the opposite, a short-term dip because users are used to the old way and need time to adapt.

**Then explain:**
- Both mean the early effect is not the steady-state effect I want to ship on.
- **Detect:**
  - Plot the daily lift (or lift by days since first exposure). Decaying lift suggests novelty; rising lift suggests primacy.
  - Compare new users vs existing users: novelty and primacy mostly hit existing users, new users have no old habit.
  - Look at repeat-engagement metrics versus first-click metrics.
- **Handle:**
  - Run longer and judge on the stable later period.
  - Use only users first exposed late, or analyse by exposure-day cohort.
  - Keep a long-term holdout after launch.
  - Be wary of big UI changes (banners, redesigns) which are classic novelty cases.

**Example (illustrative numbers):** A bright "new" badge on recommendations lifts clicks +8% on days 1-2 but only +1% by day 10; shipping on the 2-day number would overstate the gain.

**Follow-ups:**
- *Is it just noise?* Check that the daily trend is monotone and the confidence bands separate.
- *New users show a lift too?* Then it is likely a real effect, not novelty.

**Common mistakes:** averaging the whole window and calling it steady state, ignoring existing-vs-new split, confusing day-of-week patterns with novelty decay.

### Q9 ⭐⭐⭐ 🟡 You track 20 metrics (or 10 variants) in one test and one is significant at p=0.04. What is the multiple-testing problem and how do you handle it (Bonferroni, BH/FDR)?
**Asked at:** Zalando, Amazon, Flipkart, product cos
**Say this first (1 line):** With many comparisons the chance of at least one false positive grows fast (20 tests at 5% gives about 64%), so one p=0.04 among 20 metrics is weak evidence; I correct with Bonferroni (strict, controls any false positive) or Benjamini-Hochberg (controls the share of false discoveries).

**Then explain:**
- **Family-wise error rate (FWER):** probability of at least one false positive. Bonferroni: test each at alpha/m, or multiply p by m. Simple, conservative, loses power.
- **False discovery rate (FDR):** expected fraction of "discoveries" that are false. BH: sort p-values, find the largest k with p(k) <= (k/m)*alpha, reject the first k. More power; good for exploratory many-metric analysis.
- **Best fix first:** pre-register one primary metric; treat the rest as secondary/exploratory. Use Bonferroni/Holm for a small confirmatory set, BH for large screens.
- For many variants vs one control, also Dunnett or Bonferroni.

**Example / Code:** ten p-values, alpha 0.05.
```python
import numpy as np
from statsmodels.stats.multitest import multipletests
p = np.array([0.001, 0.008, 0.012, 0.04, 0.2, 0.35, 0.5, 0.6, 0.7, 0.9])
for m in ["bonferroni", "fdr_bh"]:
    r = multipletests(p, alpha=0.05, method=m)
    print(m, r[0].sum(), np.round(r[1][:4], 3))
# bonferroni 1 [0.01 0.08 0.12 0.4]   -> only the first survives
# fdr_bh     3 [0.01 0.04 0.04 0.1]   -> three survive
print(1 - 0.95 ** 20)   # 0.64
```
The p=0.04 result does not survive either method.

**Follow-ups:**
- *Do guardrails need correction?* Usually not corrected the same way: missing a real harm is worse, so use looser thresholds there.
- *Bonferroni vs BH?* Bonferroni for decisions where any false claim is costly; BH for screening.

**Common mistakes:** celebrating the one significant metric, correcting only after seeing which metric "won", using Bonferroni on hundreds of correlated metrics, forgetting segment cuts also count as comparisons.

### Q10 ⭐⭐⭐ 🟡 What is Simpson's paradox? Give an A/B-test example where the variant wins overall but loses in every segment.
**Asked at:** FAANG-style loops, product cos
**Say this first (1 line):** Simpson's paradox is when a trend that holds in every subgroup reverses when the groups are combined, because the groups are unequal in size and in baseline rate; in an A/B test it usually means the arms have a different mix of users.

**Then explain:**
- A hidden variable (device, country, new vs old user) affects both group mix and outcome.
- In a clean randomized test the mix is balanced, so the paradox should not appear. If it does, suspect SRM, a bug, or a triggered/filtered population.
- Which view is right? Decide using the causal story: if the segment is a confounder or mix issue, trust the segment-level (or reweighted) result.
- Fix: stratify or standardize to a common mix; check balance of segments across arms.

**Example (conversion):** Variant B loses in both segments but wins overall because B got mostly high-converting desktop users.

| Segment | A | B |
|---|---|---|
| Mobile | 400/4000 = 10.0% | 95/1000 = 9.5% |
| Desktop | 300/1000 = 30.0% | 1140/4000 = 28.5% |
| Overall | 700/5000 = 14.0% | 1235/5000 = 24.7% |

**Code:**
```python
import pandas as pd
d = pd.DataFrame({"seg": ["mobile", "mobile", "desktop", "desktop"],
                  "arm": ["A", "B", "A", "B"],
                  "users": [4000, 1000, 1000, 4000],
                  "conv": [400, 95, 300, 1140]})
d["rate"] = d.conv / d.users
print(d)
t = d.groupby("arm")[["users", "conv"]].sum()
print(t.conv / t.users)     # A 0.140, B 0.247
```

**Follow-ups:**
- *In a real A/B test, how could this happen?* Broken randomization (SRM), a bug sending desktop to B, or analysing only a post-assignment subset.
- *Which number do you report?* The stratified/reweighted one, after fixing the mix problem.

**Common mistakes:** trusting the pooled number, "averaging the segment rates", not checking whether segments are balanced across arms.

### Q11 ⭐⭐⭐ 🟡 Explain correlation vs causation. How would you establish causality for the claim 'users who use feature X retain better'?
**Asked at:** Spotify, Booking, product cos, Swiggy
**Say this first (1 line):** Correlation means two things move together; causation means changing one changes the other; "feature users retain better" is likely correlation because engaged users choose to use the feature, so I would run a randomized test to establish causality.

**Then explain:**
- **Why correlation misleads:** confounding (engaged users do everything more), reverse causation (retained users have more time to find the feature), selection bias.
- **Best way:** randomize exposure to the feature (A/B test, or an encouragement design nudging some users to try it) and compare retention of all assigned users (intent-to-treat).
- **If you cannot randomize:** diff-in-diff, propensity matching, IV (a randomized nudge), regression discontinuity, always stating assumptions.
- **Check:** pre-period engagement balance between users and non-users; dose-response; placebo outcomes.

**Example:** Users who use "playlists" retain 20% better. Randomly prompt half of eligible new users to create a playlist; if the prompted group retains better overall, the feature (via its prompt) has a causal effect. If not, it was just a marker of engaged users.

**Follow-ups:**
- *What if the feature is already used by everyone engaged?* Use an encouragement test plus IV to estimate the effect on those moved by the nudge.
- *Would controlling for past activity be enough?* It reduces bias but cannot rule out unmeasured confounders.

**Common mistakes:** saying "adjust for covariates and it is causal", concluding causation from cohort comparison, forgetting reverse causality.

### Q12 ⭐⭐⭐ 🟡 Explain network effects / interference (SUTVA violation). How do you run experiments on a social product or a two-sided marketplace?
**Asked at:** Uber, Swiggy, Zomato, Booking, Spotify, LinkedIn-style
**Say this first (1 line):** Interference means one user's treatment affects another user's outcome, which breaks SUTVA (the assumption that each unit's outcome depends only on its own assignment); on social or two-sided products I change the randomization unit to clusters, geos or time blocks.

**Then explain:**
- **Why it matters:** in a naive test, treated users take supply or influence control users, so the measured difference is biased (often overstated, or understated, depending on the mechanism).
- **Social network:** friends in different arms; fix with graph-cluster randomization (ego clusters).
- **Marketplace:** a better rider-pricing algorithm may just steal drivers from control. Options: geo/city randomization, switchback by time, budget-split designs, or two-sided randomization.
- **Trade-off:** clusters mean fewer independent units, less power, and need cluster-aware standard errors.
- **Diagnose:** compare results at user level vs cluster level; if estimates differ a lot, interference is present.

**Example:** Uber testing a new dispatch rule: 50% of riders in the same city get it. Treated riders get closer drivers, control riders get further ones, so the gap exaggerates the true effect. Switching the unit to city-hour switchback measures the real system-wide change.

**Follow-ups:**
- *Is the user-level result biased up or down?* Depends; with competition for shared supply it usually overstates the benefit.
- *Alternatives to experiments?* Synthetic control or geo matched markets.

**Common mistakes:** ignoring interference in marketplaces, analysing cluster experiments as if users were independent, using too few clusters.

### Q13 ⭐⭐⭐ 🟡 The test shows the primary metric up but revenue (or a guardrail) down or flat. How do you interpret and decide?
**Asked at:** Product cos, Swiggy, Flipkart, Zalando
**Say this first (1 line):** I do not ship on the primary metric alone: I check whether the guardrail drop is real, size the trade-off in money or long-term value, and decide against the pre-agreed decision rule.

**Then explain:**
1. **Is the guardrail drop real?** Look at its confidence interval, not just the point estimate, and whether the metric is noisy (revenue is heavy-tailed).
2. **Understand the mechanism:** funnel breakdown. Maybe more orders but smaller baskets, or discounts driving volume.
3. **Segments:** is the harm concentrated (new users, one city)? Could ship to the segment that benefits.
4. **Quantify:** convert both to a common unit, e.g. contribution margin per user.
5. **Long-term view:** will a short-term engagement gain cost retention or trust later?
6. **Decision:** if guardrail breach is real and large, do not ship (or iterate). If flat, ship only if the primary win is worth the complexity. Escalate with numbers if it is a business trade-off.

**Example:** New coupon banner: orders +4%, but revenue per user flat because coupon cost eats margin. Net profit per user is lower, so no ship; test a smaller discount.

**Follow-ups:**
- *Primary up, guardrail CI includes zero?* Inconclusive on the guardrail; check power for the guardrail or extend.
- *Who decides?* The pre-registered rule; trade-offs are a product/finance call, I provide the numbers.

**Common mistakes:** celebrating the primary, ignoring guardrail uncertainty, cherry-picking a segment after the fact, not converting to common units.

### Q14 ⭐⭐⭐ 🟡 What do you do when the A/B test result is statistically insignificant? Can you conclude there is no effect?
**Asked at:** Product cos, GCCs, Amazon
**Say this first (1 line):** No, an insignificant result means "no evidence of an effect at this sample size", not "no effect"; I look at the confidence interval to see what effects are still possible.

**Then explain:**
- Absence of evidence is not evidence of absence, especially if the test was underpowered.
- **Read the CI:**
  - If the CI is narrow around zero and excludes any effect I care about, I can say "no meaningful effect" (equivalence reasoning, TOST).
  - If the CI is wide, the test is inconclusive.
- **Next steps:** check power and MDE, check data quality and SRM, check exposure (was the feature really seen?), segment analysis only as hypothesis generation, consider extending only if the extension was pre-planned.
- **Business decision:** if the change is cheap and the CI rules out harm, ship for other reasons (simplicity, consistency); otherwise drop or redesign.

**Example (code):** 10.0% vs 10.2% with 20,000 per arm.
```python
import numpy as np
from scipy.stats import norm
p1, p2, n = 0.100, 0.102, 20000
se = np.sqrt(p1 * (1 - p1) / n + p2 * (1 - p2) / n); d = p2 - p1
print(round(d - 1.96 * se, 4), round(d + 1.96 * se, 4), round(2 * (1 - norm.cdf(d / se)), 2))
# -0.0039  0.0079  0.51
```
The CI runs from -0.4 pp to +0.8 pp, so a +0.8 pp gain (8% relative) is still possible; the test is inconclusive, not negative.

**Follow-ups:**
- *Can I just run it longer?* Only with a pre-planned or sequential design; otherwise it is peeking.
- *How to prove "no effect"?* Equivalence test with a pre-set margin.

**Common mistakes:** "p > 0.05 so no effect", slicing segments until something is significant, calling an underpowered test a failure of the idea.

### Q15 ⭐⭐⭐ 🟡 Statistical vs practical significance: how do you read the confidence interval of the lift and make a ship / no-ship call?
**Asked at:** Amazon, Spotify, Zalando, Flipkart
**Say this first (1 line):** Statistical significance says the effect is probably not zero; practical significance says it is big enough to matter; I read the whole confidence interval against a pre-defined minimum worthwhile effect and the cost of shipping.

**Then explain:**

| CI of lift vs threshold | Call |
|---|---|
| Entire CI above the practical threshold | Ship |
| CI above zero but straddles the threshold | Significant but maybe too small: weigh cost, risk, maybe iterate |
| CI includes zero, narrow, inside +/- threshold | Effectively no effect: do not ship for the metric |
| CI includes zero, wide | Inconclusive: more data or redesign |
| CI entirely below zero | Harm: do not ship |

- With huge samples, tiny effects become "significant" (+0.01% is real but worthless).
- Convert lift to money or users: +0.3 pp conversion on 10M monthly users is real revenue, even though the percent looks small.
- Remember winner's curse: the observed lift of a winner tends to be overstated (Q54).

**Example:** Lift +1.2% with 95% CI [+0.3%, +2.1%], practical threshold +1%. Significant, but the lower end is below the threshold; with low engineering cost I ship and keep a holdout, with high cost I would not.

**Follow-ups:**
- *Why CI instead of p-value?* It shows size and uncertainty, not only "is it zero".
- *Where does the threshold come from?* Cost of build/maintain, opportunity cost, business target, set before the test.

**Common mistakes:** shipping anything with p < 0.05, reporting only the point estimate, no pre-set threshold, ignoring cost.

### Q16 ⭐⭐⭐ 🟡 A metric (conversion, orders) dropped after a launch. How would you investigate whether it is real, caused by the launch, or a data issue?
**Asked at:** Swiggy, Flipkart, PhonePe, Amazon, Meta-style
**Say this first (1 line):** I first check if the drop is a data or tracking problem, then whether it is real, then decompose where it comes from, and finally link it to the launch with timing and a control or holdout.

**Then explain:**
1. **Data issue?** Check logging/pipeline changes, event counts, tracking SDK versions, delayed data, dashboard definitions, bots, outages.
2. **Real vs noise:** compare to normal day-to-day variation and the same weekday in past weeks; seasonality, holidays, sale events, competitor actions.
3. **Decompose:** by platform, app version, city, new vs returning, acquisition channel, funnel step (traffic x conversion x basket). Find the segment that explains most of the drop.
4. **Link to launch:**
   - Did the drop start exactly at rollout (staged rollout lets you compare exposed vs not)?
   - Was there a holdout or A/B? If yes, read it.
   - If not, diff-in-diff or synthetic control against unaffected regions.
5. **Act:** roll back or reduce rollout if guardrails are hit; fix tracking if data issue; document root cause.

**Example:** Orders fell 6% on Tuesday. Android-only, version 5.2, checkout step. Release 5.2 shipped Tuesday with a payment SDK change: real and caused by the launch; roll back.

**Follow-ups:**
- *No experiment exists?* Use staged-rollout timing, quasi-experiments, and server logs to verify.
- *Drop is the same everywhere?* Look for external causes (outage, holiday, pricing, competition).

**Common mistakes:** jumping to the launch as the cause, not checking tracking first, looking only at aggregates, ignoring seasonality.

### Q17 ⭐⭐⭐ 🟡 AI-era: How would you A/B test an LLM-powered feature (chatbot, summarisation, copilot)? Which metrics (task success, edit/retry rate, latency, token cost, LLM-judge score) and which randomization unit?
**Asked at:** GenAI product teams, Microsoft IDC, Amazon, Spotify, Zalando, Indian product cos
**Say this first (1 line):** I A/B test an LLM feature like any other, randomizing by user, but with a metric set that covers task success and user behaviour, quality (human or validated LLM-judge), latency and cost, and extra care for non-deterministic output.

**Then explain:**
- **Unit:** user (or conversation/org for copilots where teams share context). Not request-level, because a user would get inconsistent behaviour and carryover.
- **Primary:** task success or a downstream outcome (ticket resolved without human, summary accepted, code suggestion accepted and retained).
- **Behavioural signals:** edit rate, retry/regenerate rate, thumbs, abandonment, escalation to human, 7-day return use.
- **Quality:** LLM-judge scores and periodic human review as supporting evidence only (validate the judge first, Q56).
- **Guardrails:** latency (p95), token cost per task, error/refusal rate, safety/toxicity flags, hallucination reports.
- **Pitfalls:**
  - Output varies per call, so more noise; need more samples or repeated measures.
  - Novelty effect is large for chat features.
  - Silent model/provider updates (Q55) change treatment mid-test; log model version.
  - Cost and latency may offset quality gains: report cost per successful task.

**Example:** Support chatbot v2 vs v1: primary = resolution without human handover; guardrails = CSAT, p95 latency, cost per resolved ticket; randomize by customer id for 3 weeks.

**Follow-ups:**
- *Offline eval looks great but A/B flat?* See Q45.
- *Edit rate as success?* Ambiguous (could mean engagement or poor output); pair with acceptance and retention.

**Common mistakes:** relying on LLM-judge alone, request-level randomization, ignoring cost and latency, not pinning model version.

### Q18 ⭐⭐⭐ 🟡 Observational vs experimental data: what are confounders and how do you control for them? When would you trust an observational estimate?
**Asked at:** Product cos, Spotify, Booking, Microsoft IDC
**Say this first (1 line):** A confounder is a variable that influences both who gets the treatment and the outcome, creating a fake or distorted association; randomization removes confounding, while observational data needs adjustment and strong assumptions.

**Then explain:**
- **Experiment:** random assignment makes treatment independent of everything else, so groups are comparable on average.
- **Observational:** people self-select. Heavy users adopt the feature and also retain, so naive comparison overstates impact.
- **Control for confounders:** regression adjustment, stratification, matching, propensity-score weighting, doubly robust estimators, diff-in-diff for time-invariant confounders.
- **Limits:** can only adjust for measured confounders; unmeasured ones still bias. Do not control for colliders or mediators.
- **When I trust an observational estimate:**
  - Rich pre-treatment covariates that plausibly capture selection.
  - Good overlap between treated and control.
  - Sensitivity analysis shows conclusions survive a moderate hidden confounder.
  - Placebo/negative-control tests pass.
  - It agrees with any available experimental benchmark.

**Example:** Users of the "premium" tab spend more. Past spend and tenure drive both premium-tab use and spending; adjusting for them shrinks the effect a lot, and the remainder is still not guaranteed causal.

**Follow-ups:**
- *Is adding more covariates always better?* No: adjusting for post-treatment variables or colliders introduces bias.
- *Best fallback if you cannot randomize?* Natural experiments (rollout timing, thresholds, instruments).

**Common mistakes:** saying regression "proves causality", adjusting for mediators, ignoring overlap, not checking balance after adjustment.

### Q19 ⭐⭐⭐ 🔴 You cannot randomize (e.g., a pricing change, a regional launch). What are your options for estimating the causal effect?
**Asked at:** Booking, Spotify, Swiggy, Uber, Zalando, Amazon
**Say this first (1 line):** I use a quasi-experiment: pick the method that matches how the change was rolled out, such as diff-in-diff, synthetic control, regression discontinuity or instrumental variables, and state the assumption each one needs.

**Then explain:**

| Situation | Method | Key assumption |
|---|---|---|
| Treated and untreated regions, before/after data | Difference-in-differences | Parallel trends |
| One treated unit (a city) and many controls | Synthetic control | Weighted controls track the treated unit pre-launch |
| Eligibility cut-off (score, age, price threshold) | Regression discontinuity | No manipulation around the cut-off, units just on each side are comparable |
| Random nudge affects adoption | Instrumental variables | Relevance and exclusion |
| Self-selected adopters, rich covariates | Propensity matching/weighting | No unmeasured confounding, overlap |
| Phased rollout | Staggered DiD / event study | No anticipation, valid trends |

- Also consider geo experiments or switchbacks if you can still randomize at a coarser level.
- Always do placebo and robustness checks, and be honest about uncertainty.

**Example:** Swiggy raises delivery fees in Pune only. Use similar cities (Nagpur, Surat) as controls; DiD on orders per user before/after, check pre-trends, and cluster standard errors by city.

**Follow-ups:**
- *Only one treated city?* Synthetic control, with permutation-based inference.
- *Which is most credible?* Whichever has the most defensible assumption; RDD and good IVs are usually the most convincing.

**Common mistakes:** simple before/after (confounded by time), picking controls that already trend differently, not clustering standard errors, no placebo checks.

### Q20 ⭐⭐ 🟢 Which statistical test do you use for conversion-rate metrics vs continuous metrics like revenue per user? Explain the two-proportion z-test setup.
**Asked at:** Product cos, GCCs, Amazon India
**Say this first (1 line):** For a conversion rate (a yes/no metric) I use a two-proportion z-test; for continuous metrics like revenue per user I use Welch's t-test (or a bootstrap if the data is very skewed).

**Then explain:**
- **Two-proportion z-test:** H0: p_A = p_B. Pooled rate p = (x_A + x_B) / (n_A + n_B). z = (p_B - p_A) / sqrt(p(1-p)(1/n_A + 1/n_B)). Large samples make the normal approximation fine.
- **Welch t-test:** compares means without assuming equal variance. With large n, the CLT makes it fine even if revenue is skewed, but extreme outliers hurt power (see Q25).
- CI for the difference uses the unpooled standard error.
- Also: chi-square for 2x2 is equivalent to the z-test; use Fisher's exact test for tiny counts.
- Many revenue-per-user metrics are mostly zeros with a heavy tail; consider the t-test on the user-level mean plus capping.

**Example / Code:** 1,000 of 10,000 vs 1,100 of 10,000 convert.
```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import ttest_ind
z, p = proportions_ztest([1000, 1100], [10000, 10000])
print(round(z, 2), round(p, 3))                 # -2.31  0.021
rng = np.random.default_rng(1)
a = rng.lognormal(3, 1, 5000); b = rng.lognormal(3.03, 1, 5000)
print(ttest_ind(b, a, equal_var=False).pvalue)   # revenue-like metric, Welch
```
Conversion moved from 10.0% to 11.0%, p about 0.02: significant at 5%.

**Follow-ups:**
- *Why not a t-test on binary data?* Works with large n, but z-test is the natural test for proportions.
- *Why Welch?* Variances in the two arms are rarely equal.

**Common mistakes:** unpaired tests where users repeat, using the rate-of-sessions instead of user-level data, ignoring skew, one-sided tests chosen after seeing the data.

### Q21 ⭐⭐ 🟢 What is A/A testing and why would you run one?
**Asked at:** Microsoft, Booking, Zalando, product cos
**Say this first (1 line):** An A/A test splits users into two groups that get the identical experience; I run it to check that my experiment system is healthy: about 5% of tests should come out significant at alpha 0.05 and no SRM should appear.

**Then explain:**
- **What it validates:** randomization, logging, metric computation, variance estimates, and the statistical test.
- **Expected outcome:** p-values roughly uniform between 0 and 1; false positive rate about equal to alpha.
- **If it fails:** too many significant results means underestimated variance (e.g. correlated sessions treated as independent), bucketing bias, or a pipeline bug.
- **Uses:** pre-launch platform check, baseline variance estimate for power, and comparing variance-reduction methods.
- **Cost:** it uses traffic and time, so teams run continuous A/A in the background rather than per-test.

**Example:** before launching a new experiment platform, a team runs 1,000 A/A tests. If about 50 come out significant at 5%, the system is healthy; if 120 do, the variance is underestimated and they fix the pipeline first.

**Code:** simulate 2,000 A/A tests with no true difference.
```python
import numpy as np
from scipy.stats import ttest_ind
rng = np.random.default_rng(0)
ps = [ttest_ind(rng.normal(0, 1, 500), rng.normal(0, 1, 500)).pvalue for _ in range(2000)]
print(np.mean(np.array(ps) < 0.05), round(np.mean(ps), 2))   # 0.052  0.51
```
A healthy system gives about 5% rejections and a mean p near 0.5.

**Follow-ups:**
- *What if A/A rejects 12% of the time?* Standard errors are too small, probably unit mismatch or dependent observations.
- *Is A/A different from A/A/B?* A/A/B runs a spare control inside a real test as a continuous sanity check.

**Common mistakes:** running one A/A and judging a single p-value, treating A/A as pointless, forgetting to check SRM in it.

### Q22 ⭐⭐ 🟢 Compare how you would test a feature with 5 variants (A/B/n): what changes in analysis, sample size and decision?
**Asked at:** Zalando, product cos
**Say this first (1 line):** With five variants I need more total traffic, a correction for multiple comparisons, and a plan up front for how to pick the winner.

**Then explain:**
- **Overall test first:** ANOVA / chi-square across all arms (is anything different?), then compare each variant with control.
- **Multiple comparisons:** 4 treatment-vs-control tests, so use Dunnett (best for many-vs-control), Bonferroni (alpha/4 = 1.25%) or Holm. Without this, false positive risk is about 1 - 0.95^4 = 18.5%.
- **Sample size:** each arm needs the n of a normal A/B at the stricter alpha, so total traffic is about 5 arms x a bigger n (about 3.5x a plain two-arm test); at the same daily traffic the test runs roughly 3-4x longer.
- **Decision:** pick the best variant using a pre-set rule, then confirm the winner (ideally a follow-up A/B vs control) because the best of five is inflated by winner's curse.
- Alternatives if traffic is tight: fewer variants, sequential elimination, or a bandit.

**Example:** Five email subject lines, baseline 5% open rate. At Bonferroni alpha = 0.0125 (two-sided) and 80% power, each arm needs about 42% more users than at 0.05 (z-values: (2.50 + 0.84)^2 / (1.96 + 0.84)^2 = 11.2 / 7.8), and there are 2.5x as many arms (5 vs 2), so total traffic is about 3.5x.

**Follow-ups:**
- *Is control the same size as others?* Often give control a larger share (about sqrt(k) times) to maximize power for many-vs-control.
- *Is the top variant significantly better than the second?* Probably not; only compare it with control unless planned.

**Common mistakes:** running several A/Bs against control at 5% each, declaring the top performer without correction, no confirmation run.

### Q23 ⭐⭐ 🟢 A product manager says 'the cohort that used the feature has 30% higher retention, so ship it to everyone.' Respond.
**Asked at:** Product cos, Swiggy, Flipkart, Booking
**Say this first (1 line):** That comparison is not causal, because users who chose the feature are probably already more engaged; I would not ship on it but would validate with a randomized test or a careful quasi-experiment.

**Then explain:**
- **Selection bias:** people who adopt a feature are not random; motivated, power users self-select, so retention differs even without the feature.
- **Reverse causation:** retained users have more time to discover features.
- **What I would do:**
  1. Check pre-feature behaviour: were adopters already higher-retention?
  2. Run an A/B test or a randomized nudge/rollout (intent-to-treat on everyone assigned).
  3. If impossible, compare adopters with matched non-adopters on pre-period activity, or use DiD.
  4. Estimate the size and cost, then decide.
- **Tone with the PM:** the feature may well be good; I just want to know how much, because 30% is probably an overestimate.

**Example (illustrative numbers):** Adopters had 70% 30-day retention vs 54% for others (30% relative gain). Matching on prior 30-day activity shrinks the gap to 6%. A randomized rollout then shows +3%.

**Follow-ups:**
- *PM says there is no time for a test.* A staged rollout with a 10% holdout is cheap and gives a causal read.
- *Is the cohort result useless?* It is a hypothesis generator, not proof.

**Common mistakes:** agreeing because "the data says so", dismissing it without proposing an alternative, not mentioning the holdout compromise.

### Q24 ⭐⭐ 🟡 What is a holdout / long-term holdout group and why would a company keep one?
**Asked at:** Booking, Spotify, Amazon, ads and growth teams
**Say this first (1 line):** A holdout is a small group of users kept on the old experience (or without a feature or campaign) after launch, so the company can keep measuring the real, long-term incremental impact.

**Then explain:**
- **Why:** short tests miss slow effects (novelty fading, retention, fatigue, habit building), and tests are run one at a time while the product changes everywhere.
- **Types:** per-feature holdout (a few %), a "universal holdout" (a slice of users that gets no launches for a quarter or year), and ad/marketing holdouts to measure incrementality.
- **Benefits:** long-term effect, cumulative impact of many launches (Q54), a sanity check that dashboards reflect real gains, regression detection.
- **Costs:** some users get a worse experience, revenue left on the table, engineering complexity, and holdout size must be big enough for power.
- **Hygiene:** random, sticky assignment; monitor SRM; define an end date; avoid contamination from other channels.

**Example (illustrative numbers):** Notifications team keeps 1% of users on the old ranking for six months. After a year of launches, holdout retention is 3% below the main population: that 3% is the verified cumulative lift.

**Follow-ups:**
- *How big?* Enough to detect the smallest long-term effect you care about, often 1-5%.
- *Ethical concern?* Avoid holding out safety fixes or critical features.

**Common mistakes:** too small to be useful, never ending the holdout, treating it as free, forgetting to log exposure.

### Q25 ⭐⭐ 🟡 How do you handle outliers and heavy-tailed metrics (revenue, watch time) in an A/B test?
**Asked at:** Flipkart, Swiggy, Amazon, Spotify
**Say this first (1 line):** Heavy-tailed metrics make means noisy and tests underpowered, so I cap (winsorize) at a pre-set percentile, transform (log), use robust or bootstrap methods, or use variance reduction, while checking that I am still measuring what the business cares about.

**Then explain:**
- **Why it hurts:** a few whale users dominate the mean and the variance, so a single huge order can swing the result.
- **Options:**
  - **Winsorize/cap** at a percentile (e.g. 99.9th) computed on pooled data and applied equally to both arms; reduces variance with small bias.
  - **Log or log1p transform:** analyses relative changes; good for multiplicative effects but changes the question (geometric vs arithmetic mean).
  - **Bootstrap or trimmed means; median/quantile metrics** (e.g. p90 latency).
  - **Convert to a binary metric** (spent above X) as a secondary view.
  - **CUPED** (pre-period covariate) to cut variance.
- **Do not drop outliers after seeing results.** Set the rule before launch. Investigate real vs fraud/bot outliers separately.
- Remember capping changes the estimand: if whales drive revenue, report both capped and uncapped.

**Example / Code:** no true effect, but three 200k orders land in treatment.
```python
import numpy as np
from scipy.stats import ttest_ind
rng = np.random.default_rng(0)
a = rng.lognormal(3, 1, 20000)
b = rng.lognormal(3, 1, 20000)
b[:3] = 200_000
cap = np.quantile(np.r_[a, b], 0.999)
for name, (x, y) in {"raw": (a, b), "capped": (np.minimum(a, cap), np.minimum(b, cap)),
                     "log1p": (np.log1p(a), np.log1p(b))}.items():
    print(name, round(y.mean() - x.mean(), 2), round(ttest_ind(y, x, equal_var=False).pvalue, 3))
# raw 30.54 0.078 | capped 0.40 0.334 | log1p -0.0 0.775
```
Three outliers create a +30 gap in the raw mean (which is close to significant); capping brings it back to noise.

**Follow-ups:**
- *Is capping biased?* Slightly, but the variance drop is usually worth it; choose the cap before the test.
- *Revenue per user vs conversion?* Run conversion as a robust companion metric.

**Common mistakes:** removing outliers post hoc, different caps per arm, ignoring bots/fraud, using the median when the business cares about the mean.

### Q26 ⭐⭐ 🟡 How do you measure the effect when only some assigned users actually received the treatment? (intent-to-treat vs per-protocol, non-compliance, triggered analysis)
**Asked at:** Microsoft, Booking, Spotify, ads teams
**Say this first (1 line):** I report the intent-to-treat (ITT) effect, which compares everyone as assigned, and if I need the effect on people who actually got the treatment I scale ITT by the compliance rate (the CACE, complier average causal effect) or analyse only triggered users in both arms.

**Then explain:**
- **ITT:** compare by assignment, ignore whether treatment was received. It keeps the randomization intact and is the unbiased effect of the policy of offering the treatment, but is diluted by non-compliance.
- **Per-protocol (compare those who got it vs not):** biased, because compliers differ from non-compliers.
- **CACE (Wald/IV estimator):** CACE = ITT / (share exposed in treatment - share exposed in control). Assumes assignment only works through exposure (exclusion), monotonicity (no defiers).
- **Triggered analysis:** only include users who reached the point where the feature would show, in both arms (counterfactual trigger logged in control). Removes dilution from users who never saw the change and improves power.

**Example / Code:** only 30% see the new feature.
```python
import numpy as np
rng = np.random.default_rng(0)
n = 200000; z = rng.integers(0, 2, n)        # random assignment
comp = rng.random(n) < 0.3                    # would use the feature if offered
d = z * comp                                  # actually exposed
y = rng.normal(10, 3, n) + 0.5 * d            # true effect of exposure = 0.5
itt = y[z == 1].mean() - y[z == 0].mean()
share = d[z == 1].mean() - d[z == 0].mean()
print(round(itt, 3), round(share, 3), round(itt / share, 3))   # 0.163 0.299 0.546
```
ITT is 0.16 (diluted), exposure share 0.30, so CACE is about 0.55 (true value 0.5, with sampling noise).

**Follow-ups:**
- *Which do you report to leadership?* ITT for "should we launch the offer", CACE/triggered for "how good is the feature for people who use it".
- *Why not just filter to exposed users?* Selection bias unless filtered symmetrically with a counterfactual trigger.

**Common mistakes:** analysing only exposed users in treatment vs all in control, mixing ITT and CACE, no counterfactual logging in control.

### Q27 ⭐⭐ 🟡 Ratio metrics (CTR, revenue per session) and per-session vs per-user analysis: what goes wrong with the variance and how do you fix it (delta method)?
**Asked at:** Booking, Microsoft, Amazon, Spotify
**Say this first (1 line):** For a ratio like CTR or revenue per session, the sessions of one user are correlated and the denominator is random, so the simple binomial/session-level standard error is too small; I use the delta method (or analyse at the randomization unit) to get the right variance.

**Then explain:**
- **Problem:** users are randomized, but metric = sum(clicks) / sum(sessions). Treating each session as independent ignores that one user has many correlated sessions, so false positives rise.
- **Per-user analysis:** compute a user-level metric (clicks per user) and t-test it. Simple and valid, but answers a slightly different question (average of per-user rates vs the pooled ratio).
- **Delta method:** for ratio R = mean(C)/mean(S) over n users,
  Var(R) approx (1/n) * [Var(C)/mean(S)^2 - 2*mean(C)*Cov(C,S)/mean(S)^3 + mean(C)^2*Var(S)/mean(S)^4].
  Compute the SE for each arm, then test the difference.
- Alternatives: bootstrap by user, or linearization (turn the ratio into a per-user variable and use a t-test).

**Example:** a search team randomises 5,000 users; each user has about 6 sessions, and heavy users click far more than light users. Treating the ~30,000 sessions as independent gives a CTR standard error of 0.0019, but the correct user-level (delta method) value is 0.0027, so naive p-values would be overconfident. (Simulated data in the code below.)

**Code:** users have different click propensities.
```python
import numpy as np
rng = np.random.default_rng(0)
U = 5000
sess = rng.poisson(5, U) + 1
p_user = np.clip(rng.beta(1, 9, U) * (sess / 6), 0, 1)
clicks = rng.binomial(sess, p_user)
ctr = clicks.sum() / sess.sum()
n, mc, ms = U, clicks.mean(), sess.mean()
var = (clicks.var(ddof=1) / ms**2
       - 2 * mc * np.cov(clicks, sess)[0, 1] / ms**3
       + mc**2 * sess.var(ddof=1) / ms**4) / n
se_delta = np.sqrt(var)
se_naive = np.sqrt(ctr * (1 - ctr) / sess.sum())
print(f"CTR={ctr:.4f} delta SE={se_delta:.5f} naive SE={se_naive:.5f}")
# CTR=0.1174 delta SE=0.00265 naive SE=0.00186
```
The naive SE is about 30% too small, so naive p-values would be overconfident.

**Follow-ups:**
- *Why not just randomize by session?* Then session is the unit and the naive SE is valid, but user experience is inconsistent (Q4).
- *Alternative to delta?* User-level bootstrap.

**Common mistakes:** treating sessions as independent, mixing per-user and pooled definitions, ignoring the covariance term.

### Q28 ⭐⭐ 🟡 Explain difference-in-differences. What is the parallel-trends assumption and how do you test it?
**Asked at:** Booking, Spotify, Swiggy, Uber, Zalando, Amazon
**Say this first (1 line):** Difference-in-differences compares the before-to-after change in the treated group with the before-to-after change in a control group, so common time effects cancel out; it needs parallel trends, meaning the treated group would have moved like the control group without the treatment.

**Then explain:**
- **Estimate:** DiD = (treated_post - treated_pre) - (control_post - control_pre). In regression: y = a + b*treated + c*post + d*(treated x post); d is the effect.
- **Parallel trends:** cannot be proven, only checked:
  - Plot pre-period trends for both groups.
  - Test pre-period differences in slope (event-study leads should be near zero).
  - Placebo tests (fake treatment date, fake treated unit).
  - Other assumptions: no anticipation, no spillover into control, stable composition.
- **Inference:** cluster standard errors at the unit level (city); with few clusters use wild bootstrap.
- **Caveat:** staggered rollouts with heterogeneous effects can bias two-way fixed effects, use modern estimators (Callaway-Sant'Anna).

**Example / Code:** 40 cities, 20 treated, true effect 5, common trend +2 per period.
```python
import numpy as np, pandas as pd, statsmodels.formula.api as smf
rng = np.random.default_rng(0)
rows = []
for city in range(40):
    treated = city < 20; base = rng.normal(100, 5)
    for t in range(12):
        post = t >= 6
        y = base + 2 * t + (5 if treated and post else 0) + rng.normal(0, 2)
        rows.append((city, int(treated), int(post), t, y))
df = pd.DataFrame(rows, columns=["city", "treated", "post", "t", "y"])
m = smf.ols("y ~ treated*post", df).fit(cov_type="cluster", cov_kwds={"groups": df.city})
print(m.params["treated:post"].round(2), m.bse["treated:post"].round(2))     # 4.95 0.36
pre = df[df.post == 0]
m2 = smf.ols("y ~ treated*t", pre).fit(cov_type="cluster", cov_kwds={"groups": pre.city})
print(m2.params["treated:t"].round(3), m2.pvalues["treated:t"].round(2))     # -0.041 0.8
```
DiD recovers about 5; the pre-trend slope difference is near zero (p = 0.8), supporting parallel trends.

**Follow-ups:**
- *Parallel trends fails?* Use synthetic control, add covariates/trends carefully, or change control group.
- *Passing a pre-trend test proves it?* No, it only fails to reject; low power is possible.

**Common mistakes:** simple pre/post comparison, not clustering errors, controls that were affected by the treatment, over-trusting the pre-trend p-value.

### Q29 ⭐⭐ 🟡 What is a switchback (time-based) experiment? When is it used and what are its pitfalls (carryover, time-of-day effects)?
**Asked at:** Uber, DoorDash-style, Swiggy, Zomato, Booking
**Say this first (1 line):** A switchback flips the whole system (a city or region) between treatment and control over alternating time windows, then compares the windows; we use it when users can't be split cleanly because they share supply, like drivers or riders.

**Then explain:**
- **When:** marketplaces and network effects where user-level randomisation leaks (dispatch, surge pricing, ETA models). The unit of randomisation is a region x time-window, not a user.
- **How:** randomise the treatment order per region (not a fixed A-B-A-B), pick a window length, analyse window-level outcomes with region and hour-of-week effects.
- **Window length trade-off:** short windows give more samples but more carryover; long windows reduce carryover but give fewer units and more exposure to time trends.
- **Pitfalls:**
  - Carryover: queues, driver positions and surge state from window 1 leak into window 2. Fix: drop a burn-in period at the start of each window, or use longer windows.
  - Time-of-day and weekday effects: balance the schedule so each arm gets the same hours; add time fixed effects.
  - Few effective units, so low power; cluster errors by region.
  - Not usable for changes users notice and remember (a new UI).

**Example:** dispatch algorithm in 10 cities, 2-hour windows, randomised per city. Compare mean delivery time per window after dropping the first 15 minutes of each window.

**Follow-ups:**
- *How do you analyse it?* Regression of window metric on treatment with region and hour-of-week fixed effects and clustered errors, or randomisation inference by permuting the schedule.
- *Why not pre/post?* Time trends and events get confounded with the launch; switchback interleaves treatment with time.

**Common mistakes:** strictly alternating schedule that lines up with hour-of-day, ignoring carryover, treating each order as independent.

### Q30 ⭐⭐ 🟡 Explain propensity score matching / weighting. When would you use it and how do you check it worked (balance, overlap)?
**Asked at:** Product cos, healthcare and fintech GCCs, Spotify
**Say this first (1 line):** A propensity score is the probability of getting the treatment given covariates; we match or weight people on it so treated and untreated groups look alike on observed features, then compare outcomes.

**Then explain:**
- **Use when:** you can't randomise (a loyalty programme, a feature users opted into) and you believe you measured the confounders.
- **Steps:** fit a model for P(treated | X) (logistic or GBM), then either:
  - Matching: pair each treated unit with a nearest untreated unit (caliper to avoid bad matches).
  - IPW: weight treated by 1/e, controls by 1/(1-e); estimates the ATE. Trim extreme weights.
- **Check it worked:**
  - Balance: standardised mean difference (SMD) of every covariate after weighting; aim for below 0.1.
  - Overlap: plot propensity histograms by group; no overlap means no valid comparison there (positivity).
  - Effective sample size after weighting.
- **Limit:** only fixes observed confounding. Unobserved confounders still bias it; run a sensitivity analysis (Rosenbaum bounds, E-value).

**Example / Code:** one confounder x drives both treatment and outcome; true effect is 2.
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
rng = np.random.default_rng(0); n = 20000
x = rng.normal(size=n); t = rng.binomial(1, 1/(1+np.exp(-1.5*x)))
y = 2*t + 3*x + rng.normal(size=n)
print("naive", round(y[t==1].mean() - y[t==0].mean(), 2))               # 5.17
e = LogisticRegression().fit(x[:, None], t).predict_proba(x[:, None])[:, 1]
w = np.where(t == 1, 1/e, 1/(1-e))
ate = np.average(y[t==1], weights=w[t==1]) - np.average(y[t==0], weights=w[t==0])
print("ipw", round(ate, 2))                                             # 2.07
def smd(x, t, w):
    d = np.average(x[t==1], weights=w[t==1]) - np.average(x[t==0], weights=w[t==0])
    return d / np.sqrt((x[t==1].var() + x[t==0].var()) / 2)
print(round(smd(x, t, np.ones(n)), 2), round(smd(x, t, w), 2))          # 1.26 0.03
```
Naive gap is 5.17, IPW gets 2.07, and the SMD drops from 1.26 to 0.03.

**Follow-ups:**
- *Matching vs weighting?* Matching is intuitive but throws data away; IPW uses everyone but is noisy with extreme scores.
- *Does a good propensity model AUC mean good?* No; very high AUC means poor overlap. You want balance, not prediction.

**Common mistakes:** checking the model's AUC instead of covariate balance, including post-treatment variables, ignoring overlap, believing it handles hidden confounders.

### Q31 ⭐⭐ 🟡 What is Instrumental Variables (IV)? Explain the relevance and exclusion assumptions with an example.
**Asked at:** Booking, Spotify, Amazon, research-leaning DS roles
**Say this first (1 line):** IV uses a variable that nudges the treatment but affects the outcome only through the treatment, so you can get a causal effect even when treatment is confounded.

**Then explain:**
- **Setup:** instrument Z, treatment D, outcome Y, hidden confounder U.
- **Relevance:** Z must really move D (check first-stage F-statistic, rule of thumb above 10).
- **Exclusion:** Z affects Y only through D. Untestable, you argue it from domain knowledge.
- **Independence:** Z is as good as random (not related to U).
- **Monotonicity:** nobody does the opposite of what Z pushes.
- **Estimate:** Wald = (effect of Z on Y) / (effect of Z on D); 2SLS does this with covariates. It gives the LATE: the effect for compliers (people whose treatment changes with Z).
- **Common tech example:** random encouragement (a nudge email) as instrument for feature adoption, since users who adopt a feature are self-selected.

**Example / Code:** true effect is 2; hidden U drives both adoption and outcome; Z is a randomised nudge.
```python
import numpy as np
rng = np.random.default_rng(0); n = 50000
u = rng.normal(size=n); z = rng.binomial(1, .5, n)
d = (0.8*z + u + rng.normal(size=n) > 0.5).astype(float)
y = 2*d + 2*u + rng.normal(size=n)
print("ols", round(np.polyfit(d, y, 1)[0], 2))                                    # 4.17
wald = (y[z==1].mean() - y[z==0].mean()) / (d[z==1].mean() - d[z==0].mean())
print("iv", round(wald, 2))                                                       # 1.96
```
OLS says 4.17 (confounded); IV recovers about 2.

**Follow-ups:**
- *Weak instrument?* Estimates become very noisy and biased towards OLS; report the first-stage F.
- *Is the estimate the ATE?* No, LATE for compliers.

**Common mistakes:** an instrument that also affects Y directly, treating exclusion as testable, ignoring weak first stage, forgetting that IV answers a complier-only question.

### Q32 ⭐⭐ 🟡 Explain Regression Discontinuity Design with an example. What are its assumptions and limits?
**Asked at:** Booking, Spotify, fintech lending teams, Amazon
**Say this first (1 line):** RDD exploits a sharp cutoff rule (score above 700 gets the loan) and compares units just above and just below the cutoff, who are nearly identical, so the jump in outcome is the causal effect.

**Then explain:**
- **Idea:** near the threshold, assignment is almost random, because nobody can precisely control their score.
- **Estimate:** fit local linear regressions on each side within a bandwidth h; the effect is the gap at the cutoff. Bandwidth chosen by data-driven rules (Imbens-Kalyanaraman, CCT).
- **Assumptions and checks:**
  - No manipulation of the running variable: density test (McCrary) for bunching at the cutoff.
  - Covariates are smooth through the cutoff (balance test).
  - Outcome would be continuous without treatment.
  - Robustness to bandwidth and polynomial order.
- **Limits:** gives a local effect only at the cutoff (not for people far away); needs a lot of data near the cutoff; fuzzy RDD (cutoff only raises treatment probability) is an IV problem.

**Example / Code:** credit-line increase for score >= 0; true jump 3.
```python
import numpy as np
rng = np.random.default_rng(0); n = 50000
x = rng.uniform(-1, 1, n); t = (x >= 0)
y = 1 + 1.5*x + 3*t + rng.normal(size=n)
m = np.abs(x) < 0.2
X = np.c_[np.ones(m.sum()), t[m], x[m], x[m]*t[m]]
print(round(np.linalg.lstsq(X, y[m], rcond=None)[0][1], 2))   # 3.01
```

**Follow-ups:**
- *Why not use everyone with a big polynomial?* High-order polynomials behave badly at the edge; local linear is preferred.
- *Fuzzy RDD?* Use the cutoff as an instrument for actual treatment.

**Common mistakes:** ignoring score manipulation (agents nudging scores over the line), too wide a bandwidth, claiming the effect applies to everyone.

### Q33 ⭐⭐ 🟡 What is uplift modelling? How is it different from a normal propensity/response model?
**Asked at:** Flipkart, Swiggy, PhonePe, fintech, marketing DS
**Say this first (1 line):** An uplift model predicts the incremental effect of an action on each person, P(buy | treated) minus P(buy | not treated), while a response model only predicts who is likely to buy.

**Then explain:**
- Four kinds of customers: persuadables (act only if treated), sure things (buy anyway), lost causes, sleeping dogs (treatment hurts). We want persuadables; a response model happily targets sure things and wastes budget.
- **Data:** needs randomised (or well-controlled) treatment and control groups.
- **Methods:** two-model/T-learner (fit treated and control models, subtract), S-learner, X-learner, class-transformation trick, uplift trees / causal forests.
- **Output use:** target customers whose uplift times value exceeds cost of the offer.
- **Challenge:** uplift is a difference of two noisy things, so the signal is small and the targets are never observed for one person.

**Example:** coupon campaign. Response model scores a loyal customer 0.9 (will buy anyway). Uplift is 0.01, so skip them and save the coupon.

**Follow-ups:**
- *Why can't you just predict uplift directly?* You never see both outcomes for one person, so there is no per-person label.
- *Sleeping dogs?* Negative uplift users; suppress the offer for them.

**Common mistakes:** training on observational data without randomisation, evaluating with AUC (it measures response, not uplift), ignoring offer cost.

### Q34 ⭐⭐ 🟡 How do you evaluate an uplift model offline (Qini curve, AUUC) and online?
**Asked at:** Marketing DS, fintech, Swiggy, Flipkart
**Say this first (1 line):** Rank customers by predicted uplift, then plot cumulative incremental conversions as we treat more of them (Qini curve); a good model gets most of the gain early, and AUUC/Qini coefficient is the area between the curve and the random line.

**Then explain:**
- **Qini curve:** sort by score; at each cut-off k, Qini(k) = (treated conversions) - (control conversions) x (n_treated / n_control) in the top k. Compare against a random-targeting diagonal.
- **AUUC:** area under the uplift curve; Qini coefficient is the area above random. Higher is better. Always compute on held-out data from a randomised test.
- **Why not AUC:** there is no per-user label for uplift, so standard metrics don't apply.
- **Online:**
  - Randomise users into: model-targeted, random or control; or a holdout.
  - Compare incremental conversions per rupee spent (not just conversion).
  - Check whether the top-decile uplift predicted offline appears in the real test.

**Example / Code:** randomised data where only x0 > 0 users respond (true uplift +0.15, else -0.05); T-learner with GBM.
```python
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier as G
rng = np.random.default_rng(0); n = 40000
x = rng.normal(size=(n, 2)); t = rng.binomial(1, .5, n)
tau = 0.2*(x[:, 0] > 0) - 0.05
y = rng.binomial(1, np.clip(0.2 + tau*t, 0, 1))
tr = np.arange(n) < n//2; te = ~tr
f = lambda m: G(n_estimators=100, max_depth=3, random_state=0).fit(x[tr & m], y[tr & m])
m1, m0 = f(t == 1), f(t == 0)
s = m1.predict_proba(x[te])[:, 1] - m0.predict_proba(x[te])[:, 1]
def qini(score):
    o = np.argsort(-score); yy, tt = y[te][o], t[te][o]
    cT, cC = np.cumsum(yy*tt), np.cumsum(yy*(1-tt))
    nT, nC = np.cumsum(tt), np.cumsum(1-tt)
    return cT - cC*nT/np.maximum(nC, 1)
q, qr = qini(s), qini(rng.normal(size=te.sum()))
print(round(q.max(), 1), round(q[-1], 1), round(q.mean(), 1), round(qr.mean(), 1))  # 780.2 553.6 542.1 270.4
```
The model curve peaks at 780 incremental conversions (by treating about half the users) versus 554 when treating everyone, since the negative-uplift group is excluded; its mean height (AUUC-style) is 542 versus 270 for random.

**Follow-ups:**
- *Why does the curve go down at the end?* We are treating sleeping dogs, whose uplift is negative.
- *Offline looks good, online weak?* Check for non-randomised training data, overfitting to noise, and drift.

**Common mistakes:** evaluating on training data, using AUC, forgetting to adjust for unequal treated/control sizes, no online validation.

### Q35 ⭐⭐ 🟡 Explain Average Treatment Effect (ATE), CATE and the potential-outcomes framework. What is the fundamental problem of causal inference?
**Asked at:** Spotify, Booking, Amazon, causal-leaning DS roles
**Say this first (1 line):** Every person has two potential outcomes, Y(1) if treated and Y(0) if not; the treatment effect is their difference, but we only ever see one of them, which is the fundamental problem of causal inference.

**Then explain:**
- **Individual effect:** tau_i = Y_i(1) - Y_i(0). Never observed for anyone.
- **ATE:** E[Y(1) - Y(0)], the average over the population.
- **CATE:** E[Y(1) - Y(0) | X = x], the average effect for a subgroup, such as new users in India.
- **ATT:** effect on those who actually got treated.
- **Why randomisation works:** it makes treated and control groups comparable, so E[Y|T=1] - E[Y|T=0] equals the ATE.
- **Without randomisation:** observed difference = ATE + selection bias; we need assumptions (Q36) to fix it.

**Example / Code:** a tiny table of what is seen versus unseen.

| User | Y(1) | Y(0) | Treated | Observed |
|---|---|---|---|---|
| A | 1 | 0 | yes | 1 (Y(0) hidden) |
| B | 1 | 1 | no | 1 (Y(1) hidden) |
| C | 0 | 0 | yes | 0 |

True ATE = (1 + 0 + 0)/3 = 0.33, but nobody observes both columns.

**Follow-ups:**
- *How do we get around it?* Randomise, or assume conditional exchangeability given covariates.
- *Why CATE matters?* Personalisation, who to target (Q47, Q52).

**Common mistakes:** confusing association with causation, mixing up ATE and ATT, thinking a good prediction model gives a causal effect.

### Q36 ⭐⭐ 🟡 What assumptions are needed to estimate causal effects from observational data (SUTVA, unconfoundedness, positivity)?
**Asked at:** Spotify, Booking, Microsoft IDC
**Say this first (1 line):** To get causal effects from observational data we need SUTVA (no interference, one version of treatment), unconfoundedness (no hidden confounders once we control X) and positivity (everyone had a chance of either treatment).

**Then explain:**
| Assumption | Meaning | Breaks when |
|---|---|---|
| SUTVA | My outcome depends only on my own treatment; treatment is well defined | Network effects, marketplace sharing, "treatment" has many versions |
| Unconfoundedness (ignorability) | Given X, treatment is as good as random | Unmeasured motivation, intent, severity |
| Positivity (overlap) | 0 < P(T=1 given X) < 1 for all X | A segment always or never gets treated |
| Consistency | Observed outcome equals the potential outcome of the treatment received | Vaguely defined treatment |

- **Checks:** overlap plots (checkable), balance (checkable), negative-control outcomes and placebo tests, sensitivity analysis (E-value) for hidden confounding. SUTVA and unconfoundedness can't be proven.
- **Also:** don't adjust for post-treatment variables or colliders.

**Example:** a premium-membership effect on spend. Heavy spenders self-select into membership (unconfoundedness violated); there are no members among inactive users (positivity violated for them).

**Follow-ups:**
- *What if positivity fails?* Restrict to the overlap region and say the estimate applies only there.
- *Can you test unconfoundedness?* No; you can only probe it with sensitivity analysis and negative controls.

**Common mistakes:** "controlling for everything", including mediators or colliders, ignoring overlap, forgetting interference in marketplaces.

### Q37 ⭐⭐ 🟡 How would you design an experiment for a marketplace where both buyers/riders and sellers/drivers are affected (a new pricing or dispatch algorithm)?
**Asked at:** Uber, Swiggy, Zomato, Flipkart, Ola, Booking
**Say this first (1 line):** In a two-sided marketplace, naive user-level A/B is biased because treated and control users compete for the same drivers or inventory, so I randomise at a coarser level (city/time via switchback, or clusters) and measure both sides plus system-level metrics.

**Then explain:**
- **Requirements:** define success on both sides and guardrails (rider ETA, driver earnings, cancellations, platform margin).
- **Why the naive test fails:** if treated riders get faster pickups, control riders get slower ones (interference), so the measured lift is inflated or distorted.
- **Designs:**
  - Switchback by (city x time window) for dispatch and pricing.
  - Geo/cluster randomisation or matched markets, with synthetic control for analysis.
  - Two-sided randomisation (randomise buyers and sellers independently) to estimate the interference.
  - Budget-split or a small market-level holdout for long-run effects.
- **Analysis:** cluster-robust errors, few units so use permutation tests or CUPED-style variance reduction; check SRM per market.
- **Trade-offs:** lower power vs lower bias. Accept longer, noisier tests.

**Example:** new dispatch algorithm for Swiggy. Randomise 30-minute windows within each city; primary metric is delivery time and completed orders per rider-hour; guardrails are rider idle time and order cancellations.

**Follow-ups:**
- *Why not just rider-level A/B?* Riders are shared, so control gets fewer of them; the effect is biased.
- *How long?* Enough windows per city to cover weekday/weekend cycles.

**Common mistakes:** one-sided metrics, assuming SUTVA, ignoring carryover, declaring win on short-term buyer metrics while sellers or drivers get hurt.

### Q38 ⭐⭐ 🟡 How would you test a new recommendation or ranking algorithm online? Which metrics and what pitfalls (position bias, interleaving)?
**Asked at:** Spotify, Flipkart, Zalando, Netflix-style, Booking
**Say this first (1 line):** Run an A/B (and often interleaving first), judge it on engagement and downstream value metrics with guardrails, and watch for position bias, novelty effects and feedback loops.

**Then explain:**
- **Offline first:** NDCG/recall on logged data, but logs are biased by the old ranker, so offline wins don't always hold online (use counterfactual/IPS estimates with care).
- **Online ladder:** interleaving (fast, sensitive; see Q50) then a user-level A/B for the final decision.
- **Metrics:** primary is a value metric (conversion, listening time, orders), not raw CTR; secondary: diversity, catalogue coverage, latency; guardrails: returns, complaints, revenue per session.
- **Pitfalls:**
  - Position bias: items shown at the top get clicks regardless of quality; use position-aware metrics or interleaving.
  - Novelty/primacy effects: new rankings get curiosity clicks, so run at least 1-2 weeks and check effect over time.
  - Feedback loops and cold start: the new model changes the data it will train on later.
  - Clickbait: CTR rises while satisfaction falls; pair with long-term metrics.
  - Interference when shared inventory (limited stock) is competed for.

**Example:** Flipkart tests a new search ranker. Interleave for 2 days, A/B for 2 weeks; primary is orders per search session, guardrails are cancellations and latency p95.

**Follow-ups:**
- *Offline NDCG up, online flat?* Training data bias, metric mismatch, or position bias in labels.
- *Why not just CTR?* It rewards clickbait and is affected by position.

**Common mistakes:** stopping early on a novelty bump, optimising CTR only, ignoring latency, treating item clicks as independent samples when users are the randomisation unit.

### Q39 ⭐⭐ 🟡 How would you A/B test a price change or discount? What are the risks (cannibalization, fairness, price anchoring)?
**Asked at:** Flipkart, Swiggy, Booking, Zalando, Amazon
**Say this first (1 line):** I randomise users (or markets) to price arms, measure revenue and profit per user rather than conversion alone, and guard against cannibalisation, fairness and anchoring effects.

**Then explain:**
- **Primary metric:** profit (or revenue) per visitor, because a lower price raises conversion and lowers margin; conversion alone misleads.
- **Design:**
  - Randomise at user level when users can't see one another's prices; use geo or time-based designs when they can (leakage, screenshots, social media).
  - Keep users on one price for the whole test (consistency).
  - Long enough to capture repeat purchases and pull-forward demand.
- **Risks:**
  - Cannibalisation: discount on product A steals sales from B, so measure category-level or basket-level outcomes.
  - Pull-forward: discount brings purchases earlier, followed by a dip.
  - Fairness/legal: charging different customers different prices can harm trust and can break consumer laws; test by segments of time or geography carefully, and avoid sensitive attributes.
  - Anchoring: a user who saw a high price reference then sees a lower one, or the discount trains customers to wait for deals.
  - Long-term: brand perception, churn.
- **Alternatives:** conjoint/survey, price elasticity models from observational data, or a holdout.

**Example:** Swiggy tests a Rs 20 delivery fee reduction. Primary metric: contribution margin per user over 4 weeks; guardrails: order frequency after the test and fee-sensitive segment churn.

**Follow-ups:**
- *Elasticity estimate?* Log-log regression of quantity on price from randomised arms.
- *Users compare prices?* Use geo/time randomisation instead.

**Common mistakes:** celebrating higher conversion while profit drops, short test windows, ignoring cross-product effects and fairness.

### Q40 ⭐⭐ 🟡 How do you run experiments for a feature with a long-term outcome (retention, LTV) when you cannot wait months? (surrogate metrics, holdouts)
**Asked at:** Spotify, Booking, Netflix-style, Swiggy
**Say this first (1 line):** I don't wait months; I predict the long-term outcome from short-term surrogate metrics validated on past experiments, and keep a long-term holdout to confirm the real effect.

**Then explain:**
- **Surrogate index:** pick early signals (week-2 activity, number of sessions, feature depth) that historically predict 90-day retention or LTV; combine into one predicted-long-term score and use it as the test metric.
- **Validate the surrogate:** it must capture the treatment effect on the long-term outcome (surrogacy condition). Check on many past experiments: does the effect on the surrogate predict the effect on retention?
- **Holdouts:** keep a small percentage (1-5%) of users in control for months after launch to measure real cumulative effect.
- **Other tools:** cohort-based reads as they mature, extrapolating survival curves, and Bayesian priors on long-term effect.
- **Risks:** surrogates can be gamed (a notification boosts clicks but not retention), distribution shift in a new feature, and novelty fade.

**Example (hypothetical numbers):** a new onboarding flow. Short-term metric: completed 3 key actions in the first week. Historically, effect on that metric explains most of the effect on 90-day retention (checked across 40 past tests). Ship, but keep a 2% holdout for 90 days.

**Follow-ups:**
- *Surrogate says up, holdout later says flat?* Trust the holdout and fix the surrogate.
- *What if no history?* Run longer on a smaller sample, use mechanism reasoning, and be more conservative.

**Common mistakes:** using an unvalidated proxy (clicks), forgetting novelty decay, ending the holdout early.

### Q41 ⭐⭐ 🟡 What is a multi-armed bandit? When would you prefer it to a classic A/B test and what do you lose?
**Asked at:** Booking, Spotify, Zalando, ad-tech
**Say this first (1 line):** A multi-armed bandit is a method that shifts traffic to the better-looking variant while the test runs; I prefer it when the cost of a bad arm is high and the horizon is short, and I lose clean inference and unbiased estimates.

**Then explain:**
- **Idea:** balance exploration (learn) and exploitation (earn). Algorithms: epsilon-greedy, UCB, Thompson sampling (sample each arm's success rate from its posterior, pick the max).
- **Prefer bandits when:** many variants (headlines, banners), short-lived content (news, promos), low cost of switching, goal is maximise reward not understand effect.
- **Prefer A/B when:** you need a precise effect estimate and p-values, long-term effects, multiple metrics and guardrails, or rewards are delayed.
- **What you lose:**
  - Uneven allocation gives noisier estimates for the losing arms and biased naive means.
  - Hard with delayed outcomes (retention) and with non-stationary behaviour (day-of-week).
  - Harder to read guardrails and secondary metrics.

**Example / Code:** two arms, 10% and 12% true conversion, 20,000 users.
```python
import numpy as np
rng = np.random.default_rng(0); p = np.array([0.10, 0.12])
a = np.ones(2); b = np.ones(2); pulls = np.zeros(2)
for _ in range(20000):
    k = np.argmax(rng.beta(a, b)); r = rng.random() < p[k]
    a[k] += r; b[k] += 1 - r; pulls[k] += 1
print(pulls, int(a.sum() - 2))     # [ 3157. 16843.] 2294
```
Thompson gives 2,294 conversions versus about 2,200 from a 50/50 split, and sends 84% of traffic to the better arm.

**Follow-ups:**
- *Contextual bandit?* Picks the arm using user features; needs logging propensities to evaluate offline.
- *Regret?* Reward lost compared to always picking the best arm.

**Common mistakes:** using bandits for decisions that need long-term metrics, forgetting seasonality, treating bandit-arm averages as unbiased.

### Q42 ⭐⭐ 🟡 Explain selection bias and survivorship bias with experiment or observational examples.
**Asked at:** Product cos, GCCs, FAANG-style
**Say this first (1 line):** Selection bias is when the people in your data were chosen in a way related to the outcome; survivorship bias is the special case where you only see the ones who "survived" a filter.

**Then explain:**
- **Selection bias examples:**
  - Comparing users who adopted a feature with non-adopters (motivated users adopt).
  - Surveys with only responders; opt-in trials.
  - Experiments: excluding users who left before exposure, or analysing only users who logged in after assignment, which can break randomisation (differential attrition).
- **Survivorship bias examples:**
  - Average lifetime or spend of "current customers" (churned ones are gone).
  - Analysing only successful loans or funded start-ups.
  - Planes with bullet holes (WWII): armour where the surviving planes were not hit.
- **Fixes:**
  - Randomise when possible; analyse by intention-to-treat (everyone assigned).
  - Include the dropped/churned units; use survival analysis for censoring.
  - Model selection explicitly (propensity weighting, Heckman) or restrict conclusions.

**Example:** "Users who use search spend 3x more, so push search." Heavy buyers search more; the effect is selection. Randomise a search nudge to test it.

**Follow-ups:**
- *How to catch selection in an A/B test?* SRM check and compare attrition rates between arms.
- *Selection vs confounding?* Confounding is a shared cause of treatment and outcome; selection arises when analysis conditions on a variable affected by both.

**Common mistakes:** analysing only active users post-treatment, comparing opt-in groups, forgetting churned units.

### Q43 ⭐⭐ 🟡 A marketing campaign has already run. How do you estimate its incrementality?
**Asked at:** Swiggy, Flipkart, PhonePe, Zalando, Amazon India
**Say this first (1 line):** I need a counterfactual for what would have happened without the campaign, which I build from a holdout if one exists, otherwise from geo/time comparisons (DiD, synthetic control) or careful observational adjustment.

**Then explain (ordered by credibility):**
1. **Randomised holdout / ghost ads:** best case. Compare converted rate between exposed and held-out; incrementality = (treated rate - control rate) / treated rate.
2. **Geo experiments:** campaign ran in some cities only; compare with matched or synthetic-control cities (Q44, Q49).
3. **Difference-in-differences:** before/after for exposed versus similar unexposed users (Q28).
4. **Observational modelling:** propensity matching/weighting on pre-campaign behaviour (Q30) or time-series models (Bayesian structural time series, CausalImpact).
- **Pitfalls:** attributing all conversions after exposure (last-touch attribution counts sure-things), targeting bias (the campaign targeted likely buyers), spillover, and seasonality.
- **Report:** incremental conversions, incremental revenue, iROAS = incremental revenue / spend, with confidence interval.

**Example:** campaign sent to 1M users, no holdout. 5% converted. Matched untreated users with similar history convert at 4.2%. Incrementality about 0.8 points, so 8,000 incremental conversions, not 50,000. If each conversion is worth Rs 400 and spend was Rs 20 lakh, iROAS = 32 lakh / 20 lakh = 1.6.

**Follow-ups:**
- *Nothing comparable exists?* Say the effect isn't identifiable and give bounds / sensitivity analysis; recommend a holdout next time.
- *How to plan next time?* Always keep a randomised holdout.

**Common mistakes:** counting all post-exposure conversions, comparing exposed to unexposed without adjustment, ignoring seasonality.

### Q44 ⭐⭐ 🟡 How would you design and read a geo / city-level experiment when user-level randomization is not possible? (synthetic control, matched markets)
**Asked at:** Swiggy, Uber, Booking, Spotify, ad measurement teams
**Say this first (1 line):** When I can't randomise users, I randomise (or select) whole geographies, match or synthesise comparable control geos from pre-period data, and read the post-period gap as the effect.

**Then explain:**
- **Design:**
  - Unit = city/DMA. Choose geos so spillover is small (commuter areas bleed).
  - Matched markets: pair treated and control geos on pre-period trend and size, then randomise within pairs. Few units, so pair them.
  - Pre-period of enough length (e.g. 8-12 weeks) to fit well; pre-register the analysis.
  - Run power analysis by simulating on historical data (placebo tests).
- **Analysis:**
  - DiD or synthetic control (a weighted blend of control geos that tracks the treated geo before launch; Q49).
  - Time-series approach: Bayesian structural time series (CausalImpact).
  - Inference: permutation/placebo over control geos, not usual standard errors.
- **Pitfalls:** few units means low power, spillover between geos, local events (festival in one city), a poor pre-fit (discard if it's bad), and external-validity limits.

**Example (hypothetical numbers):** test a brand campaign in 6 cities vs 6 matched cities for 4 weeks. The synthetic control for each treated city fits within 2% before launch; the average post-launch gap is +4.1% orders; the placebo test on untreated cities shows gaps within +/-1.5%, so the effect is distinguishable.

**Follow-ups:**
- *How do you size it?* Use historical data, simulate fake lifts, see detection rate.
- *Few geos, how to get a p-value?* Permutation: compare the treated gap against gaps from placebo geos.

**Common mistakes:** choosing "interesting" test cities (selection), no pre-period validation, ignoring spillover, treating daily rows within a city as independent.

### Q45 ⭐⭐ 🟡 AI-era: Offline LLM evals look better but the online A/B shows no gain or a drop. How do you reconcile and decide?
**Asked at:** GenAI product teams, Microsoft IDC, product cos
**Say this first (1 line):** I assume the offline eval is measuring the wrong thing or on the wrong data until proven otherwise, so I debug the gap between the eval and real usage, and let the online result win the decision.

**Then explain:**
- **Why they diverge:**
  - Eval set doesn't match production queries (distribution shift, too clean, stale).
  - Metric mismatch: judged quality (LLM-as-judge, benchmark) is not user value (task completion, retention, edit rate).
  - Judge bias: LLM judge prefers longer or its own style.
  - Hidden costs: latency, tone, refusals, formatting breaking the UI.
  - Online issues: novelty, low power, SRM/logging bugs, segment effects hiding a win and a loss.
- **Steps:**
  1. Verify the experiment (sample ratio, logging, power).
  2. Slice: by query type, language, segment; the average can hide a win in one and a loss in another.
  3. Read samples manually: look at disagreements between offline and online.
  4. Check offline metric against human judgments and online outcomes on past launches (calibration).
  5. Build better evals from sampled production traffic.
- **Decision:** ship on online guardrails and user-value metrics; if flat and costly, don't ship; if flat and cheaper, could ship as cost win.

**Example:** new model scores +3 points on helpfulness offline, but task-completion is flat and latency rose 400ms. Slice shows gains on long queries and loss on short ones; users abandon from latency. Route short queries to the old model.

**Follow-ups:**
- *Is offline eval useless then?* No, it's a cheap filter; it just needs to be validated against online.
- *Flat result is underpowered?* Compute minimum detectable effect first.

**Common mistakes:** trusting the offline score, shipping on a benchmark win, ignoring latency and cost, not slicing.

### Q46 ⭐⭐ 🟡 AI-era: How would you measure the causal impact of AI-assistant adoption on productivity when users self-select into using it?
**Asked at:** Microsoft IDC, GCCs, research-leaning DS roles
**Say this first (1 line):** Adopters differ from non-adopters (they are more motivated and skilled), so I need a design that breaks self-selection: a randomised rollout or encouragement if possible, otherwise DiD or matching on pre-adoption productivity.

**Then explain:**
- **Best:** staggered or randomised access (phased rollout by team), or randomised encouragement as an instrument (IV, Q31): effect of adoption for those nudged.
- **If adoption has already happened:**
  - DiD / event study around each person's adoption date, compared with similar not-yet-adopters (staggered adoption; use modern estimators).
  - Matching/weighting on pre-adoption productivity, tenure, role, team.
  - Synthetic control at team level.
- **Metrics:** output (merged PRs weighted by complexity, tickets closed, time to resolution) plus quality (defects, rework, review comments) so speed is not bought with quality.
- **Pitfalls:** pre-trends (high performers adopt sooner), spillovers inside teams (help each other), Hawthorne effect, metric gaming, changes in the work mix, and measuring time spent rather than outcomes.

**Example:** 2,000 engineers; Copilot-style tool rolled out to teams in 4 waves, randomised order. Compare PR cycle time and defect rate across waves; late-wave teams are the control for early-wave ones.

**Follow-ups:**
- *Can't randomise?* Event-study with pre-trend checks plus matching, and be explicit about hidden confounding.
- *Heterogeneity?* Gains often larger for juniors; estimate CATE by tenure.

**Common mistakes:** comparing users to non-users, measuring usage as productivity, using only speed metrics, not checking pre-trends.

### Q47 ⭐ 🟡 Explain heterogeneous treatment effects: how do you find which segments benefit, and what are the dangers of post-hoc subgroup analysis?
**Asked at:** Spotify, Booking, Amazon, marketing DS
**Say this first (1 line):** Heterogeneous treatment effects mean the effect differs across people; I find segments with pre-specified subgroups or CATE models, and treat post-hoc slicing as hypothesis generation, not proof.

**Then explain:**
- **Find HTE:**
  - Pre-specified subgroups (new vs returning, platform, country) with interaction test: y ~ T * segment.
  - ML approaches: causal forests, meta-learners (T/X-learner), uplift trees (Q52).
  - Evaluate with held-out data: do predicted high-effect users really show a larger effect (Qini, calibration by bins)?
- **Dangers of post-hoc slicing:**
  - Multiple comparisons: with 20 segments, there is a ~64% chance (1 - 0.95^20) that at least one looks significant by luck.
  - Each subgroup is smaller, so estimates are noisy and, when selected for being large, inflated (winner's curse; Q54).
  - Story-telling: any pattern can be explained afterwards.
- **Safeguards:** pre-register segments, correct for multiple testing (Bonferroni, Benjamini-Hochberg), shrinkage, sample splitting, and confirm in a follow-up experiment.

**Example / Code:** no true effect at all, 20 random subgroups, 1,000 simulated experiments.
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(0); hits = 0
for _ in range(1000):
    y = rng.normal(size=2000); t = rng.integers(0, 2, 2000); g = rng.integers(0, 20, 2000)
    ps = [stats.ttest_ind(y[(g==k)&(t==1)], y[(g==k)&(t==0)]).pvalue for k in range(20)]
    hits += min(ps) < 0.05
print(hits / 1000)       # 0.626
```
In 62.6% of null experiments, some subgroup looks "significant".

**Follow-ups:**
- *How would you trust a segment finding?* Pre-registered or replicated in a new holdout experiment.
- *Does the overall effect matter?* Yes; first check the average, then explore.

**Common mistakes:** reporting only the best segment, no correction, acting on tiny subgroups, treating subgroup differences as causal for the segment definition.

### Q48 ⭐ 🟡 What are interaction effects between concurrent experiments and how do mature platforms avoid them (layers, orthogonal hashing)?
**Asked at:** Google-style, Booking, Spotify, Microsoft
**Say this first (1 line):** Interaction effects happen when two concurrent experiments change each other's effect (the combined result is not the sum); mature platforms avoid them with layers/domains and independent hashing so overlapping tests stay balanced, and keep conflicting tests in the same layer so a user is in only one.

**Then explain:**
- **Orthogonal (independent) randomisation:** hash user id with a different salt per experiment, so assignment in experiment A is independent of B. Then each arm of A has the same share of B's arms, and B's effect averages out of A's estimate (only works if there is no interaction).
- **Layers / mutually exclusive domains:** experiments that touch the same surface (same page, same ranking model) go in one layer; a user is in at most one of them. Different layers are independent.
- **Detect interactions:** run the 2x2 analysis (A x B) for suspicious pairs; test the interaction term; monitor via platform alerts.
- **Pitfalls:** same salt across tests (perfect correlation), reusing a salt from an old experiment (carryover), one experiment's bug breaking another's metrics.

**Example / Code:** same salt gives 50% overlap; different salts give 25% (independent).
```python
import numpy as np, hashlib
def bucket(uid, salt): return int(hashlib.md5(f"{salt}:{uid}".encode()).hexdigest(), 16) % 100
a1 = np.array([bucket(i, "expA") < 50 for i in range(100000)])
a2 = np.array([bucket(i, "expA") < 50 for i in range(100000)])   # same salt
b  = np.array([bucket(i, "expB") < 50 for i in range(100000)])   # different salt
print((a1 & a2).mean(), round((a1 & b).mean(), 3))               # 0.50142 0.249
```

**Follow-ups:**
- *Why not just mutually exclusive for everything?* Traffic gets split thin, so each test has less power.
- *When do interactions matter?* When both change the same UX or model (ranker and its UI).

**Common mistakes:** reusing one hash salt, ignoring same-surface conflicts, assuming independence means no interaction (it only keeps estimates unbiased on average if the effects are additive).

### Q49 ⭐ 🔴 Explain synthetic control. How is it different from difference-in-differences?
**Asked at:** Booking, Spotify, Uber, research-leaning DS roles
**Say this first (1 line):** Synthetic control builds a weighted mix of untreated units that matched the treated unit before the intervention, and uses it as the counterfactual; DiD instead assumes one simple parallel-trend with equal-weighted controls.

**Then explain:**
- **Method:** pick weights w >= 0, sum to 1, on control units to minimise pre-period gap between treated unit and the weighted controls. After launch, effect = treated - synthetic.
- **Versus DiD:**

| | DiD | Synthetic control |
|---|---|---|
| Control | Chosen group, equal weights | Data-driven weighted blend |
| Assumption | Parallel trends | Pre-period fit implies a good counterfactual |
| Best for | Many treated and controls | One or few treated units (a country, a city) |
| Inference | Clustered SEs | Placebo/permutation tests |

- **Checks:** good pre-period fit (RMSE small), placebo tests on controls, leave-one-out of donors, ratio of post to pre error.
- **Limits:** needs a long pre-period and a donor pool that spans the treated unit (no extrapolation outside the convex hull); bad fit means no answer.

**Example / Code:** one treated unit, 20 donors, 30 pre and 10 post periods, true effect 2.
```python
import numpy as np
from scipy import optimize
rng = np.random.default_rng(0)
T0, T1, J = 30, 10, 20
f = np.cumsum(rng.normal(size=T0 + T1)); load = rng.uniform(0.5, 1.5, J)
Y0 = np.outer(f, load) + rng.normal(0, .3, (T0 + T1, J))
yt = 0.9*f + rng.normal(0, .3, T0 + T1); yt[T0:] += 2.0
res = optimize.minimize(lambda w: ((yt[:T0] - Y0[:T0] @ w)**2).sum(), np.ones(J)/J,
                        bounds=[(0, 1)]*J, constraints={'type': 'eq', 'fun': lambda w: w.sum() - 1})
gap = yt - Y0 @ res.x
print(round(np.sqrt((gap[:T0]**2).mean()), 2), round(gap[T0:].mean(), 2))   # 0.17 1.99
```
Pre-period RMSE is 0.17 and the post-period gap is 1.99 against a true effect of 2.

**Follow-ups:**
- *Why non-negative weights summing to 1?* Avoids extrapolation and keeps the result interpretable.
- *Augmented / synthetic DiD?* Combine both to reduce bias when fit is imperfect.

**Common mistakes:** poor pre-fit but trusting the result, picking donors affected by the treatment, no placebo inference.

### Q50 ⭐ 🔴 How does an interleaving experiment work and why is it more sensitive than A/B for ranking?
**Asked at:** Spotify, Booking, search and recsys teams
**Say this first (1 line):** Interleaving shows each user one merged list mixing results from both rankers and counts which ranker's results get clicked; because each user compares both rankers directly, it needs far fewer users than A/B.

**Then explain:**
- **How:** Team-draft interleaving: rankers A and B take turns "drafting" their next best item (coin flip for who goes first each round), skipping duplicates. A click credits the ranker that supplied the item. The ranker with more credited clicks wins that user's session; aggregate win rates across users.
- **Why more sensitive:** within-user comparison removes between-user variance (some users click a lot, some don't). A/B must compare separate groups whose noise swamps small ranking differences.
- **Limits:**
  - Measures preference, not magnitude (no revenue/retention lift).
  - Only for ranking where results can be merged; not for UI changes or latency.
  - Hard for multi-page flows or purchase metrics; needs an A/B final check.
- **Use:** fast screening of many candidate rankers, then A/B for the winner.

**Example (toy simulation, assumptions in the code):** ranker B is about 1 point of CTR better than A. With 2,000 users per arm, A/B detects it only about 26% of the time (power). Interleaving 2,000 users, where 53% of clicks go to B, detects it in about 99% of runs. The exact numbers depend on the assumed user-to-user variation; the point is the gap in sensitivity, not the figures.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
n, Q, sims = 2000, 10, 300        # users, queries per user, simulated experiments
hit_ab = hit_il = 0
for _ in range(sims):
    # A/B: 2,000 users per arm, each with their own click propensity; ranker B is 1 pt better on average
    qa = rng.beta(1.5, 3.5, n); qb = rng.beta(1.5, 3.5, n)
    ca = rng.binomial(Q, qa) / Q; cb = rng.binomial(Q, np.clip(qb + 0.01, 0, 1)) / Q
    hit_ab += stats.ttest_ind(cb, ca, equal_var=False).pvalue < 0.05
    # Interleaving: 2,000 users see a merged list; 53% of clicks are credited to the better ranker B
    q = rng.beta(1.5, 3.5, n)
    clicks = rng.binomial(Q, np.clip(q + 0.005, 0, 1))
    b_wins = rng.binomial(clicks, 0.53)
    d = (2 * b_wins - clicks) / Q      # per-user (B credits - A credits)
    hit_il += stats.ttest_1samp(d, 0).pvalue < 0.05
print("A/B power", hit_ab / sims, "interleaving power", hit_il / sims)   # 0.26  0.993
```

**Follow-ups:**
- *Position bias?* Team-draft randomises who goes first to remove it.
- *Can interleaving say how much revenue changes?* No, calibrate it against past A/B results.

**Common mistakes:** thinking it replaces A/B for launch decisions, using it on non-rank changes, not randomising draft order.

### Q51 ⭐ 🔴 How do you handle interference with cluster-randomised or graph-cluster experiments? What is the bias-variance tradeoff of cluster size?
**Asked at:** LinkedIn-style, Uber, Spotify, Swiggy
**Say this first (1 line):** With interference (my treatment affects my friends), I randomise whole clusters of connected users so most of a user's neighbours share their assignment; bigger clusters reduce bias but give fewer units and so more variance.

**Then explain:**
- **Problem:** in a social graph, treated users change control users' behaviour (spillover), which biases the usual A/B difference.
- **Cluster randomisation:** partition the graph (community detection like Louvain, balanced partitioning) into clusters, randomise at cluster level; analyse with cluster-robust errors.
- **Bias-variance:**
  - Small clusters: many units, high power, but edges cut between clusters, so spillover remains (biased towards zero).
  - Large clusters: little spillover, but few units, high variance and imbalance.
  - Choose by simulation on the real graph.
- **Alternatives:** ego-cluster designs, two-sided randomisation to estimate the spillover, exposure mappings (estimate effect by fraction of treated neighbours), switchback/geo for marketplaces.
- **Fix variance:** CUPED/covariate adjustment, ratio of cluster sizes, stratify clusters on size and past activity.

**Example:** a new sharing feature on a messaging app. Partition users into ~5,000 communities; randomise communities. The fraction of friend edges crossing clusters tells you remaining contamination.

**Follow-ups:**
- *How to know interference exists?* Compare outcomes of control users with many vs few treated neighbours under cluster design.
- *Why not just user-level?* The estimate shows direct effect only, and the true launch effect with everyone treated will be higher or lower.

**Common mistakes:** analysing at user level with unadjusted errors, clusters of wildly unequal size, ignoring edges cut between clusters.

### Q52 ⭐ 🔴 Explain double machine learning, causal forests and meta-learners (S-, T-, X-learner) at a high level. When would you use them?
**Asked at:** Research-leaning DS, Booking, Amazon, Uber
**Say this first (1 line):** These are methods for estimating how the causal effect varies across people (CATE): meta-learners reuse any ML model, double ML removes confounding by residualising, and causal forests split on effect differences directly.

**Then explain:**
- **S-learner:** one model with treatment as a feature; effect = difference between predictions with T=1 and T=0. Simple, but may ignore T when the effect is small.
- **T-learner:** two models (treated and control), subtract. Flexible, but noisy if the groups are small or unbalanced.
- **X-learner:** T-learner, then impute individual effects using the other group's model and fit second-stage models; blend with propensity. Better when treated and control sizes are very different.
- **Double ML (DML):** fit nuisance models E[Y|X] and E[T|X] with cross-fitting, regress outcome residuals on treatment residuals; gives effect (ATE or CATE) robust to flexible nuisance models. Good for observational data with many controls.
- **Causal forest:** trees split to maximise effect heterogeneity; honest estimation (separate samples for splitting and estimating), gives confidence intervals (grf, EconML).
- **Use:** personalisation, targeting offers, finding who benefits. For observational data, still needs unconfoundedness.

**Example / Code:** partially linear model with confounded treatment; true effect 2.
```python
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor as R
from sklearn.model_selection import cross_val_predict
rng = np.random.default_rng(0); n = 5000
X = rng.normal(size=(n, 3)); t = X[:, 0] + rng.normal(size=n)
y = 2*t + 3*X[:, 0] + np.sin(X[:, 1]) + rng.normal(size=n)
print("naive", round(np.polyfit(t, y, 1)[0], 2))
ry = y - cross_val_predict(R(random_state=0), X, y, cv=5)
rt = t - cross_val_predict(R(random_state=0), X, t, cv=5)
print("dml", round((rt @ ry) / (rt @ rt), 2))   # 2.0
```
Naive slope is 3.53 (confounded); DML gives 2.00, the true effect.

**Follow-ups:**
- *Which meta-learner first?* T-learner for a quick baseline in randomised data; X-learner when treated group is small.
- *Why cross-fitting?* Avoids overfitting bias from using the same data to fit nuisances and estimate the effect.

**Common mistakes:** applying them to confounded data with no adjustment, no held-out validation (Qini, calibration), over-trusting individual predictions.

### Q53 ⭐ 🔴 How would you debug an experiment platform whose results look wrong (SRM, logging loss, bucketing collisions, carryover between experiments)?
**Asked at:** Microsoft, Booking, Spotify, Netflix-style
**Say this first (1 line):** I debug top-down: first check the sample ratio (SRM), then logging and exposure, then bucketing and overlap with other experiments, then the metric and analysis code.

**Then explain:**
- **SRM (sample ratio mismatch):** if assignment should be 50/50 and you see 50,500 vs 49,000, a chi-square test gives p about 2e-6. Results are untrustworthy until explained. Causes: bot filtering after exposure, redirect losses, crashes in one arm, assignment logic bug.
- **Logging loss:** the treatment may drop events (a heavier page logs less); compare event rates per user and client versions between arms.
- **Bucketing collisions:** reused hash salt, hash not uniform, same user in correlated experiments, users switching ids (logged-out to logged-in), shared devices.
- **Carryover:** users previously in an experiment on the same surface; re-randomise with a new salt or add a washout.
- **Analysis:** wrong unit (analysing by event, randomising by user), outlier users, metric definitions changed, bots, peeking.
- **Tools:** A/A tests (should give ~5% false positives, uniform p-values), segment SRM checks (by platform, country, day), dashboards for data freshness.

**Example / Code:**
```python
from scipy import stats
print(stats.chisquare([50500, 49000], [49750, 49750]).pvalue)   # 1.98e-06
```
**Follow-ups:**
- *SRM only in iOS?* Likely a client bug or redirect in that arm; segment and fix, don't just exclude.
- *A/A shows 15% significant?* Variance is underestimated (wrong unit or correlated data).

**Common mistakes:** ignoring a small SRM, "fixing" it by filtering, analysing at the wrong unit, trusting a result before an A/A sanity check.

### Q54 ⭐ 🔴 How do you quantify the cumulative impact of many launched experiments (the sum of wins exceeds the real lift)? What is the winner's curse?
**Asked at:** Booking, Spotify, Zalando, growth teams
**Say this first (1 line):** The sum of reported wins overshoots reality because we ship winners selected for looking good, and part of "looking good" is luck (winner's curse); I fix it with shrinkage, replication, and a holdout that measures the cumulative effect.

**Then explain:**
- **Winner's curse:** among many noisy estimates, the ones that pass significance are biased upward; the true effect is smaller (regression to the mean).
- **Other reasons for the gap:** effects overlap (two features boost the same metric), novelty decay, interactions, metric shifting, cannibalisation among features.
- **Fixes:**
  - Re-run or replicate the winners; shrink estimates towards a prior fit across all experiments (empirical Bayes).
  - Long-term holdout: keep a small set of users without a quarter's launches and compare.
  - Report cumulative lift from the holdout, not the sum of experiment lifts.
  - Pre-register, apply multiple-testing corrections.

**Example / Code:** 1,000 experiments, true effects mostly tiny (sd 0.2), measurement noise 0.5.
```python
import numpy as np
rng = np.random.default_rng(0)
true = rng.normal(0, 0.2, 1000); est = true + rng.normal(0, 0.5, 1000)
sig = est / 0.5 > 1.96
print(sig.sum(), round(est[sig].mean(), 2), round(true[sig].mean(), 2))   # 36 1.17 0.17
```
Among the 36 "significant" winners, the average reported lift is 1.17 but the real average is 0.17.

**Follow-ups:**
- *How would you shrink?* Posterior mean = prior mean + (tau^2/(tau^2 + se^2)) * (estimate - prior mean).
- *Cost of long holdouts?* Some lost revenue, but it's the only unbiased cumulative measure.

**Common mistakes:** summing lifts, reporting only winners, no replication, no holdout.

### Q55 ⭐ 🔴 AI-era: How do you handle a test where the treatment is non-deterministic or changes mid-test (LLM feature, silent provider model updates)?
**Asked at:** GenAI product teams, AI-era loops
**Say this first (1 line):** I treat the treatment as a moving target: pin and log the model version, sample multiple outputs per prompt, analyse at user level with enough volume, and stop or restart the test when the provider changes the model.

**Then explain:**
- **Non-determinism:** the same prompt can give different answers; this adds variance. Fix temperature where possible, log seeds and the full prompt, and measure the metric over many users, not a few outputs.
- **Mid-test model changes (silent provider updates):**
  - Pin the model version (snapshot) in the API; if the provider silently updates, treat it as a new treatment.
  - Log model identifier, system fingerprint, prompt template version for every call.
  - Monitor for drift: run a fixed canary set daily and alert on score changes.
  - If treatment changed mid-test, split analysis into before/after segments, or restart; don't pool.
- **Also fix:** control prompts should have the same infrastructure, latency and tooling so only the model or prompt differs.
- **Metrics:** use outcome metrics (task success, user ratings), plus validated LLM-judge scores (Q56) with confidence intervals; check heterogeneity by prompt type.

**Example:** testing a new assistant prompt. After day 6 the provider upgrades the base model; canary score jumps 4 points in both arms. Declare the day-6 boundary, analyse each period separately, and check that the treatment effect is stable across periods before pooling.

**Follow-ups:**
- *Can't pin the version?* Randomise at the user level, include time fixed effects, and compare arms concurrently (both arms get the same drift).
- *Variance too high?* More samples, repeated measures per user, CUPED on pre-period usage.

**Common mistakes:** assuming model is stable, no version logging, mixing periods, sampling a few outputs and treating them as independent.

### Q56 ⭐ 🔴 AI-era: How do you validate an LLM-as-judge metric before using it as an experiment outcome (bias, agreement with humans, variance)?
**Asked at:** GenAI teams, AI-era loops
**Say this first (1 line):** Before an LLM judge becomes a metric, I check it against human labels (agreement and calibration), test it for known biases, measure its own variance, and keep a periodic human audit.

**Then explain:**
- **Agreement with humans:** collect a human-labelled sample (stratified across topics and difficulty), with multiple raters. Compute Cohen's kappa or Krippendorff's alpha judge-vs-human, compare with human-vs-human; the judge should be about as consistent as humans.
- **Biases to test:**
  - Position bias: swap A/B order; does the verdict change?
  - Verbosity bias: does it prefer longer answers? Control for length.
  - Self-preference: does the judge favour its own model family?
  - Style/format bias.
- **Variance:** re-run the judge on the same item (temperature 0 and a few samples); measure test-retest agreement; use a rubric and structured output.
- **Metric validity:** does the judge score move when you inject known-worse answers? Does it correlate with online outcomes (user satisfaction) on past tests?
- **In the experiment:** report a confidence interval including judge noise, use the same judge, prompt and version in both arms, and recalibrate with human labels on a sample (prediction-powered inference).

**Example / Code:** 200 items; a human and a judge each label good (1) or bad (0).
```python
import numpy as np
from sklearn.metrics import cohen_kappa_score
rng = np.random.default_rng(0)
human = rng.binomial(1, 0.6, 200)
judge = np.where(rng.random(200) < 0.85, human, 1 - human)    # judge agrees 85% of the time
print(round(cohen_kappa_score(human, judge), 2))   # 0.7
```
Kappa is 0.70, i.e. substantial agreement (humans would normally be compared the same way).

**Follow-ups:**
- *Judge says better but humans disagree?* Don't ship on it; fix the rubric and re-validate.
- *Why swap order?* To measure and cancel position bias.

**Common mistakes:** using the judge without human validation, ignoring length bias, one judge call per item with no variance estimate, judge and generator from the same model family.
