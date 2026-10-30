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
