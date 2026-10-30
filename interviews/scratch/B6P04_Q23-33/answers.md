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
2. Explain the dilution. The ITT (intention-to-treat, all assigned users) is the honest business number but 92% of users add noise and zero effect. Power for the diluted effect is about 1 / 0.08^2 = 156 times worse per user than for the 8% alone, adjusted for shares: for the same power the all-users test needs 12.5 times as many assigned users as the triggered test needs triggered users divided by 0.08.
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
- Why is the ratio 12.5? The effect is 12.5 times smaller diluted, so the sample needed per user is 156 times larger, but the triggered test only has 8% of users, so the net ratio on assigned users is 1 / 0.08 = 12.5 (the noise from non-triggered users is the same size as signal there).
- What if I cannot log control triggers? Use the all-users test, or CUPED, or run longer; do not substitute "users who used the feature".
- Does 1.25% scale to the whole base? Only for users who reach the page; effect on others is assumed zero.

**Common mistakes:** Filtering to feature users (selection). Using the triggered number as a company-wide lift. Hiding the ITT result. Changing the trigger after seeing results. Not checking the triggered share per arm.
