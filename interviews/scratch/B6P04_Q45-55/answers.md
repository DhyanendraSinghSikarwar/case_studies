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
