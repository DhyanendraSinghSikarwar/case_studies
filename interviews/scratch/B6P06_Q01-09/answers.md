### Q1 ⭐⭐⭐ 🟢 A product manager has promised leadership a launch in 6 weeks, but your model needs 10 weeks to reach the quality bar. A rules baseline can ship in week 6 and captures 60,000 of the 100,000 weekly lift the full model would bring, and swapping in the full model would then slip to week 12. Compute cumulative lift by the end of week 12 for waiting and for the baseline-first plan, and say how you would present the choice to the PM.
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** By the end of week 12 the baseline-first plan has 360,000 of cumulative lift against 200,000 for waiting, a 160,000 lead that never closes, so I would ship the baseline in week 6 and tell the PM the full model follows.

**Clarifying questions:**
- Is "lift" counted per full week after launch? That fixes the arithmetic (weeks 7-12 for the baseline, weeks 11-12 for waiting).
- Is the week-12 swap date firm, or could it slip again? If it slips, the baseline plan's lead shrinks.
- What does the PM's promise to leadership actually say: a date, or a capability? A date can be met with a smaller scope.
- Is the rules baseline safe to ship (no harm, easy to roll back)? A baseline that can hurt customers changes the answer.
- Why does the swap cost 2 extra weeks (migration, A/B re-test)? Maybe the swap can be planned in parallel.

**Approach:**
1. Put numbers on both plans: waiting gives 100,000 x 2 weeks = 200,000; baseline-first gives 60,000 x 6 weeks = 360,000.
2. Check the long run: after week 12 both earn 100,000 a week, so the 160,000 lead stays.
3. Stress it: the baseline needs only about 33,333 a week to tie at week 12; if the swap slipped to week 16 the two plans would be level.
4. Define the quality bar the baseline must clear (guardrails), and what "full model replaces baseline" needs (a test, not a date).
5. Offer the PM three options in one table: wait, baseline-first, or a reduced-scope model. Recommend one and say what would change my mind.
6. Agree the message to leadership: "launch in week 6, the better model in week 12".

**Metrics:**
- Cumulative lift by week T = sum over live weeks of weekly lift (numerator: lift units; denominator: none, a running total).
- Guardrails for the baseline: error rate, complaint rate and any harm metric agreed before launch.
- Swap readiness: full model beats the baseline in a holdout by the agreed margin.

**Risks:**
- The 60,000 captured by the baseline is an estimate; if it is wrong the plan changes (break-even about 33,333).
- Two launches mean two sets of operations (monitoring, support).
- Leadership may remember only the baseline and never fund the full model.
- Counting the baseline's lift before it is proven in production.

**What the interviewer scores:**
- Strong: computes both totals and the break-even, and notes the lead persists. Weak: "ship the baseline, it is faster" with no numbers.
- Strong: frames it as options with a recommendation for the PM. Weak: argues model quality against the PM.
- Strong: protects the PM's promise (a date) while being honest about capability. Weak: either refuses the date or hides the gap.
- Strong: names what would flip the decision. Weak: no sensitivity.

**Example:** (illustrative numbers) Waiting: 2 live weeks x 100,000 = 200,000. Baseline-first: 6 live weeks x 60,000 = 360,000. Weak answer: "The model is not ready, so we cannot launch in 6 weeks." Strong answer: "We can hit week 6 with a rules version that gets 60% of the benefit. By week 12 that is 360,000 against 200,000 if we wait, and the full model still lands in week 12. If you would rather hold the date for the full model, that costs about 160,000 of lift by week 12."

**Code:**
```python
# Q1: cumulative lift by end of week 12 (illustrative numbers; lift counted per full week after launch)
full, base = 100_000, 60_000          # weekly lift: full model, rules baseline
wait = full * (12 - 10)               # full model live after week 10 -> weeks 11, 12
plan = base * (12 - 6)                # baseline live after week 6 -> weeks 7..12; swap lands in week 12, full from week 13
print("wait for full model:", wait)
print("baseline first     :", plan, " difference:", plan - wait)
assert wait == 200_000 and plan == 360_000 and plan - wait == 160_000

# long run: after week 12 both earn 100k a week, so the 160k lead stays
for wk in (12, 16, 20):
    w = full * (wk - 10)
    p = base * 6 + full * (wk - 12)
    print(f"week {wk}: wait {w:,} vs baseline-first {p:,}  (lead {p-w:,})")
    assert p - w == 160_000

# how weak can the baseline be before waiting wins at week 12?
be = wait / 6
print(f"break-even baseline lift per week: {be:,.0f}")
assert round(be) == 33_333
# if the swap slips a further 4 weeks (to week 16) the baseline plan still leads at week 16?
p16 = base * (16 - 6)
w16 = full * (16 - 10)
print("swap slips to week 16: baseline-first at wk16", p16, "vs wait", w16)
assert p16 == 600_000 and w16 == 600_000   # exactly level at week 16
```

**Output (my run):**
```text
wait for full model: 200000
baseline first     : 360000  difference: 160000
week 12: wait 200,000 vs baseline-first 360,000  (lead 160,000)
week 16: wait 600,000 vs baseline-first 760,000  (lead 160,000)
week 20: wait 1,000,000 vs baseline-first 1,160,000  (lead 160,000)
break-even baseline lift per week: 33,333
swap slips to week 16: baseline-first at wk16 600000 vs wait 600000
```

**Follow-ups:**
- What if the baseline captured only 30,000? Then 6 x 30,000 = 180,000 < 200,000, so waiting wins at week 12 (break-even about 33,333).
- What if the PM insists on the full model for week 6? Say the risk in numbers, offer a staged reveal, and write down that the quality bar was the choice.

**Common mistakes:**
- Counting the swap as free (here it costs 2 extra weeks).
- Counting launch week as a full week of lift.
- Presenting only a recommendation, not the options.

### Q2 ⭐⭐⭐ 🟢 A sales VP says your lead-scoring model is useless because ten leads he personally knows are strong scored in the bottom half. In your holdout the top-scored decile converts at 18% against 6% for all leads, which is 3 times the average. How do you respond in the meeting, and what do you offer to rebuild his trust?
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would not argue; I would agree his ten leads matter, show that the top decile converts at 3 times the average on holdout data, and offer to test the model against his judgement on leads we have not looked at yet.

**Clarifying questions:**
- How did he pick the ten leads, and how many strong leads does he know? Ten out of hundreds is a selected sample, not a test.
- What does "strong" mean to him (closed, big deal, good fit)? The model may predict a different outcome.
- What does sales do with the score (call order, routing)? The score only has to rank well enough for that use.
- Are those ten leads in my training data, and were they scored before or after the outcome was known? It could be a data issue.
- Is the score visible to reps with no explanation? Unexplained scores lose trust fast.

**Approach:**
1. Acknowledge first: "Those ten matter. Let's look at them together."
2. Look at the ten leads for real: what features drive each score? Maybe a data gap (missing field) is the cause, which I can fix.
3. Show the aggregate evidence in his terms: top decile 18% versus 6% overall is 3 times; it holds 30% of all conversions in 10% of the leads (illustrative holdout of 10,000 leads).
4. Explain why ten misses do not contradict that: a model can rank well and still miss many individual leads. With 200 known strong leads and 15% in the bottom half, about 30 misses are expected (illustrative).
5. Offer a blind test: he picks strong and weak leads before seeing scores; we compare on the next 8 weeks of outcomes.
6. Agree a feedback loop: reps flag misses, I review monthly, and the model changes if a pattern appears.

**Metrics:**
- Decile conversion = converted leads in the decile / leads in the decile. Lift = decile rate / overall rate (18% / 6% = 3).
- Capture rate of the top decile = conversions in top decile / all conversions (30%).
- Recall of "strong" leads in the top half (for his definition).
- Guardrail: conversion of the middle deciles (no collapse), rep-reported misses.

**Risks:**
- Defending the model too hard turns it into a fight about status.
- The ten leads may reveal a real blind spot (new segment, stale data).
- Holdout lift can shrink in production if the population shifted.
- Overselling the lift: 3 times the average is a ranking statement, not a promise for each lead.

**What the interviewer scores:**
- Strong: empathy first, then evidence, then a test he can design. Weak: "the data says you are wrong."
- Strong: explains selection bias in plain words. Weak: quotes AUC to a sales VP.
- Strong: checks his cases for a real defect. Weak: assumes the model is right.
- Strong: offers a lasting feedback loop. Weak: one meeting, no follow-up.

**Example:** (illustrative numbers) Holdout of 10,000 leads: 600 convert (6%). Top decile: 1,000 leads, 180 convert (18%), that is 30% of all conversions. The other 9,000 convert at 4.7%. Weak answer: "Ten leads is anecdotal, the model is validated." Strong answer: "Let's pull up those ten leads together. Across 10,000 holdout leads the top tenth converts at 18% against 6% overall. A model like that still misses some strong leads, so I would like your list of fifty you are sure about, and we score them before we look."

**Code:**
```python
import math
from scipy import stats
# holdout (illustrative): 10,000 leads, overall conversion 6%, top decile 18%
n, top_n = 10_000, 1_000
conv_all, conv_top = 0.06 * n, 0.18 * top_n
lift = 0.18 / 0.06
share = conv_top / conv_all
print(f"lift {lift:.1f}x; top decile holds {share:.0%} of all conversions")
assert lift == 3.0 and round(conv_all) == 600 and round(conv_top) == 180 and round(share, 2) == 0.30

# is 18% vs 6% noise? 180 of 1,000 vs the other 420 of 9,000
p_rest = (600 - 180) / 9000
z = (0.18 - p_rest) / math.sqrt(0.18*0.82/1000 + p_rest*(1-p_rest)/9000)
print(f"rest-of-leads rate {p_rest:.3%}, z = {z:.1f}")
assert round(p_rest, 4) == 0.0467 and z > 10

# his ten leads: assume (illustrative) 15% of truly strong leads sit in the bottom half
miss = 0.15
known = 200                       # strong leads he can name over a year
print(f"expected misses among {known} strong leads: {known*miss:.0f}")
assert known * miss == 30
# chance that ten random strong leads are ALL in bottom half if model is decent
p10 = miss ** 10
print(f"P(10 random strong leads all in bottom half) = {p10:.2e}")
assert p10 < 1e-8
# but he can pick the 10 worst of 200: expected bottom-half count is 30, so ten is easy
assert stats.binom.sf(9, known, miss) > 0.999
print("P(at least 10 bottom-half leads among 200) > 0.999")
```

**Output (my run):**
```text
lift 3.0x; top decile holds 30% of all conversions
rest-of-leads rate 4.667%, z = 10.8
expected misses among 200 strong leads: 30
P(10 random strong leads all in bottom half) = 5.77e-09
P(at least 10 bottom-half leads among 200) > 0.999
```

**Follow-ups:**
- What if the ten leads reveal a real pattern? Fix it, say so, and show before and after on the same holdout.
- What if he still refuses the score? Run the blind test and let the outcome decide; keep the score advisory meanwhile.

**Common mistakes:**
- Treating anecdotes as worthless instead of checking them.
- Quoting statistical jargon instead of one clear lift number.
- Forgetting that the 15% miss rate is an assumption I would measure.

### Q3 ⭐⭐⭐ 🟢 A bank's compliance team wants a logistic regression with reason codes for loan declines, while the data scientist prefers a gradient-boosted model. At a fixed 60% approval rate on 50,000 applications (30,000 approved), the logistic model approves loans with a 4.0% default rate and the boosted model 3.6%, and each default costs 2,500. Compute the defaults and loss avoided by the boosted model and say how you would settle the disagreement.
**Asked at:** Trade-off prompt pages (Dataford pages on accuracy versus interpretability and on accuracy versus latency and resource constraints, an Interview Query 2026 ML engineer guide that advises reasoning about interpretability versus performance and latency versus accuracy, Hyring and other 2026 guides that mention latency budgets and quantization); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** At a 60% approval rate the boosted model avoids 120 defaults, worth 300,000 at 2,500 each, but that gap has a wide error range and compliance needs reason codes, so I would run a bounded comparison rather than pick a side.

**Clarifying questions:**
- Are the 4.0% and 3.6% default rates from the same holdout and the same applicants? A paired comparison is much tighter.
- What exactly does compliance require (reason codes per decline, monotonic features, stability)? A boosted model can meet some of it with constraints.
- Is the 300,000 per year or per cohort? It sets what an extra cost is worth paying.
- Is there a regulator or model-risk sign-off timeline? A long approval can erase the benefit.
- Does interest income differ between the two approved sets? Loss avoided is not profit.

**Approach:**
1. Compute the gap: 30,000 x 4.0% = 1,200 defaults versus 30,000 x 3.6% = 1,080; difference 120; times 2,500 = 300,000.
2. Put an error range on it: an unpaired 95% interval for 0.4 percentage points is about 0.09 to 0.71, so 70,000 to 530,000.
3. Price the other side: what does compliance cost for the boosted model (explanation tooling, validation) and for the logistic (nothing extra)?
4. Offer middle options: logistic with binned features and interactions; or boosted with monotonic constraints and a reason-code method.
5. Compare on one page: loss avoided, cost, regulatory risk, time to approve.
6. Settle with a pre-agreed rule: e.g. if the boosted model's paired gain holds above a threshold and reason codes pass compliance review, adopt it; otherwise logistic.

**Metrics:**
- Default rate at fixed approval rate = defaults among approved / approved applicants.
- Loss avoided = (default rate difference) x approved count x cost per default.
- Guardrails: reason-code stability, fairness gaps by group, score drift.

**Risks:**
- 120 fewer defaults is an estimate with a wide range.
- The boosted model's reason codes may be unstable between retrains.
- A fixed 60% approval rate hides how the models differ in who gets approved.
- Choosing on loss alone ignores adverse-action notice duties.

**What the interviewer scores:**
- Strong: gets 1,200, 1,080, 120, 300,000 and adds an error range. Weak: states the gain as certain.
- Strong: treats compliance as a constraint to satisfy, not a nuisance. Weak: "the boosted model is better, full stop."
- Strong: proposes a middle option and a decision rule. Weak: picks a winner without a test.
- Strong: asks the cost of explanation. Weak: ignores it.

**Example:** (illustrative numbers) Logistic: 1,200 defaults; boosted: 1,080; saving 120 x 2,500 = 300,000. Weak answer: "Boosted wins by 300,000, so we use it." Strong answer: "On this holdout boosted saves about 300,000, but the range runs from roughly 70,000 to 530,000. If we can meet the reason-code requirement for under that, I would take it; otherwise I would try a stronger logistic first."

**Code:**
```python
import math
apps, appr = 50_000, 30_000
assert appr == apps * 0.6
d_lr, d_gb = appr * 0.040, appr * 0.036
avoided = d_lr - d_gb
loss = avoided * 2500
print(f"defaults: logistic {d_lr:.0f}, boosted {d_gb:.0f}, fewer {avoided:.0f}, loss avoided {loss:,.0f}")
assert (round(d_lr), round(d_gb), round(avoided), round(loss)) == (1200, 1080, 120, 300000)
# is a 0.4pp gap real on 30,000 approvals? (unpaired, conservative)
se = math.sqrt(.04*.96/appr + .036*.964/appr)
lo, hi = 0.004 - 1.96*se, 0.004 + 1.96*se
print(f"gap 0.40pp, 95% CI ({lo*100:.2f}, {hi*100:.2f}) pp -> loss avoided range {lo*appr*2500:,.0f} to {hi*appr*2500:,.0f}")
assert 0.0008 < lo < 0.001 and 0.0070 < hi < 0.0072
# break-even: yearly cost of the explanation layer that would erase the saving
print("break-even extra cost of keeping boosted model compliant:", f"{loss:,.0f}")
assert loss == 300_000
# a middle option capturing half the gap (e.g. logistic with binned features)
half = loss / 2
print("middle option capturing half the gap:", f"{half:,.0f}")
assert half == 150_000
```

**Output (my run):**
```text
defaults: logistic 1200, boosted 1080, fewer 120, loss avoided 300,000
gap 0.40pp, 95% CI (0.09, 0.71) pp -> loss avoided range 70,529 to 529,471
break-even extra cost of keeping boosted model compliant: 300,000
middle option capturing half the gap: 150,000
```

**Follow-ups:**
- Would you use SHAP for reason codes? Possibly, but compliance must accept it and the codes must be stable; I would validate that with them.
- What if compliance simply refuses? Then the logistic wins and I improve it with feature work.

**Common mistakes:**
- Calling 300,000 profit rather than avoided loss.
- Ignoring uncertainty on a 0.4 point difference.
- Treating compliance as an opponent.

### Q4 ⭐⭐⭐ 🟡 A ranking model A gives +1.2% relative click-through over model B, but its p95 latency is 80 ms against 25 ms for B and the product budget is 50 ms. A past latency test showed each extra 10 ms costs 0.3% of relative conversions, linear over this range. Compute the net effect of choosing A, assuming the click-through gain passes through to conversions one for one, and explain how you would decide with the ML lead and the product owner.
**Asked at:** Trade-off prompt pages (Dataford pages on accuracy versus interpretability and on accuracy versus latency and resource constraints, an Interview Query 2026 ML engineer guide that advises reasoning about interpretability versus performance and latency versus accuracy, Hyring and other 2026 guides that mention latency budgets and quantization); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Assuming the click-through gain passes through to conversions one for one, model A gives +1.2% CTR but its 55 ms of extra latency costs 1.65% of conversions, so the net is about -0.45% and it also breaks the 50 ms budget; I would not ship A as is.

**Clarifying questions:**
- Is one-for-one pass-through from click-through to conversions a fair assumption? The main case assumes it; if only part passes through, A looks worse (sensitivity below).
- Is the latency test valid up to 80 ms and for p95, not the mean? The linear range and the percentile matter.
- Is the 50 ms budget a hard SLO or a target? A hard limit decides it regardless of the net.
- Can A be made faster (distillation, caching, fewer candidates)? That is the real way forward.
- Do all users see the slow path or only the tail? It changes how the penalty applies.

**Approach:**
1. State the assumption: the +1.2% click-through gain passes through to conversions one for one. Latency gap: 80 - 25 = 55 ms. Penalty: 55 / 10 x 0.3% = 1.65%.
2. Net: +1.2% - 1.65% = -0.45% (about -0.47% compounded).
3. Find A's break-even latency: 1.2 / 0.3 x 10 = 40 ms above B, so 65 ms.
4. Check the budget: 80 ms is 30 ms over 50 ms, so it fails regardless of the net.
5. Ask what A would earn at 50 ms: 1.2% - 0.75% = +0.45%. Ask the ML lead if it is reachable.
6. Decide with the product owner: ship B, give A an optimisation sprint with a target of 50 ms, then run an online A/B test with latency as a guardrail.

**Metrics:**
- Relative CTR change = (CTR_A - CTR_B) / CTR_B.
- Relative conversion change = (conv - conv_B) / conv_B; latency penalty = 0.3% per 10 ms.
- Guardrails: p95 latency, timeouts, conversion.

**Risks:**
- Linear latency cost may not extend to 80 ms (it is often steeper).
- One-for-one pass-through is an assumption: clicks can rise without sales (sensitivity: at 60% pass-through the net is -0.93%).
- Offline CTR is not an online result.
- Applying a mean-latency effect to a p95 number.

**What the interviewer scores:**
- Strong: net -0.45% with the budget breach called out separately. Weak: "A has higher CTR, ship it."
- Strong: states the pass-through and linear-range assumptions. Weak: takes the numbers at face value.
- Strong: gives a path (optimise A to 50 ms, then test). Weak: a binary choice.
- Strong: involves both the ML lead and the product owner in the decision rule. Weak: decides alone.

**Example:** (illustrative numbers) A at 80 ms: +1.2% - 1.65% = -0.45%. A at 50 ms: +1.2% - 0.75% = +0.45%. Weak answer: "A is 1.2% better, take A." Strong answer: "A loses about half a percent net and breaks the 50 ms budget. If we can get A to 50 ms it is worth about +0.45%, so I would give the team one sprint for that and A/B test it."

**Code:**
```python
extra_ms = 80 - 25
pen = extra_ms / 10 * 0.3
print(f"extra latency {extra_ms} ms -> conversion penalty {pen:.2f}%")
assert extra_ms == 55 and round(pen, 2) == 1.65
net_add = 1.2 - pen
net_mul = (1.012 * (1 - pen/100) - 1) * 100
print(f"net (additive) {net_add:+.2f}%, net (compounded) {net_mul:+.2f}%")
assert round(net_add, 2) == -0.45 and round(net_mul, 2) == -0.47
# break-even latency for A
be_ms = 25 + 1.2 / 0.3 * 10
print(f"A breaks even at p95 {be_ms:.0f} ms")
assert be_ms == 65
# A tuned down to the 50 ms budget, keeping its CTR gain
net_50 = 1.2 - (50 - 25) / 10 * 0.3
print(f"A at 50 ms: {net_50:+.2f}%")
assert round(net_50, 2) == 0.45
# if only 60% of the CTR gain turns into conversions (illustrative pass-through)
net_pt = 0.6 * 1.2 - pen
print(f"with 60% CTR pass-through: {net_pt:+.2f}%")
assert round(net_pt, 2) == -0.93
```

**Output (my run):**
```text
extra latency 55 ms -> conversion penalty 1.65%
net (additive) -0.45%, net (compounded) -0.47%
A breaks even at p95 65 ms
A at 50 ms: +0.45%
with 60% CTR pass-through: -0.93%
```

**Follow-ups:**
- What if A is exactly 65 ms? Break-even on this arithmetic, but it still breaks the budget, so no.
- What if only 60% of the CTR gain reaches conversions? Net -0.93%, so A is worse.

**Common mistakes:**
- Adding a CTR percentage to a conversion percentage without stating the pass-through assumption.
- Charging only the 30 ms above budget instead of the 55 ms above B.
- Forgetting the latency test range.

### Q5 ⭐⭐⭐ 🟡 The CEO wants a revenue number for Friday's board deck, but you have just found that 3% of 200,000 order rows (6,000 rows) are duplicates, and cleaning and re-running takes two more days. The average order is 50, so gross revenue as currently computed is 10,000,000. What do you tell the CEO's chief of staff, and what exactly do you send by Friday?
**Asked at:** Project-conflict prompts (PracHub pages on ML project milestones, scope and conflict, on stakeholder conflict under a compressed delivery timeline and on cross-functional pushback on an analysis; one is tagged to a large marketplace and one to a social platform on the page, unverified); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would tell the chief of staff that the current figure of 10,000,000 is overstated by about 300,000, send the corrected 9,700,000 on Friday clearly labelled provisional with a range, and promise the final figure on a named date.

**Clarifying questions:**
- Are the 6,000 rows exact duplicates (same order id), or similar rows? Only true duplicates should be removed.
- Is the board deck number gross revenue before refunds? The definition must match the deck.
- Does the average order value of the duplicated rows equal 50? If not, the 300,000 changes.
- Can the board accept "approximately" with a footnote? Some boards prefer a later exact number.
- Who else already holds the 10,000,000 figure? Wrong numbers travel fast.

**Approach:**
1. Size the problem: 6,000 x 50 = 300,000, which is 3.0% of reported revenue and 3.09% of the corrected number.
2. Tell the chief of staff at once, in one message: what is wrong, how big, what I will send.
3. Do a fast partial check: confirm the duplicate rule on a sample so I can say how sure I am.
4. By Friday send: 9.7 million as the best estimate, a range from 9.7 to 10.0 million depending on how many flagged rows prove to be real duplicates, and the date for the final.
5. Run the full clean and re-run over the next two days; send the final with a short note on what changed.
6. Afterwards add a duplicate check to the pipeline so it does not recur.

**Metrics:**
- Overstatement = duplicate rows x average order = 6,000 x 50 = 300,000.
- Overstatement percentage = 300,000 / 10,000,000 = 3.0% of reported; versus the corrected 9,700,000 it is 3.09%.
- Guardrail: row counts before and after the dedupe, and a reconciliation to the finance ledger.

**Risks:**
- Deleting rows that are real repeat orders.
- Sending the old number to protect the schedule.
- Sending a new number with no explanation, which damages trust in every later number.
- An exact figure on Friday that later changes again.

**What the interviewer scores:**
- Strong: tells them early, quantifies, and sends something usable by Friday. Weak: waits two days silently, or sends the wrong number.
- Strong: gives a labelled range, not false precision. Weak: a single number with no caveat.
- Strong: explains the cause and prevention. Weak: just the fix.
- Strong: keeps the message short for an executive reader. Weak: a long technical thread.

**Example:** (illustrative numbers) 200,000 rows x 50 = 10,000,000; remove 6,000 duplicates: 194,000 x 50 = 9,700,000. Weak answer: "I need until Sunday, I cannot give you a number." Strong answer: "The number we had is about 3% too high. Use 9.7 million for the deck, marked provisional; the true figure is between 9.7 and 10.0 million, and you will have the final on Sunday."

**Code:**
```python
rows, dup, avg = 200_000, 6_000, 50
rep = rows * avg
true = (rows - dup) * avg
print(f"reported {rep:,}; overstated by {dup*avg:,}; corrected {true:,}")
assert rep == 10_000_000 and dup*avg == 300_000 and true == 9_700_000
print(f"overstatement vs reported {dup/rows:.2%}, vs corrected {dup*avg/true:.2%}")
assert round(dup/rows, 4) == 0.03 and round(dup*avg/true, 4) == 0.0309
# range to send: if only some flagged rows are true duplicates
for share in (1.0, 0.5, 0.0):
    print(f"if {share:.0%} of flagged rows are real duplicates: {rep - share*dup*avg:,.0f}")
assert rep - 0.5*dup*avg == 9_850_000
```

**Output (my run):**
```text
reported 10,000,000; overstated by 300,000; corrected 9,700,000
overstatement vs reported 3.00%, vs corrected 3.09%
if 100% of flagged rows are real duplicates: 9,700,000
if 50% of flagged rows are real duplicates: 9,850,000
if 0% of flagged rows are real duplicates: 10,000,000
```

**Follow-ups:**
- What if the board deck cannot say provisional? Send 9.7 million with a footnote that it is subject to final reconciliation, and tell the chief of staff of the exposure.
- What if a duplicate is really a customer re-order? That is why the rule is checked on a sample first.

**Common mistakes:**
- Saying the error is 3% of the corrected number (it is 3.09%).
- Sending the uncorrected figure to meet Friday.
- Staying quiet until the fix is done.

### Q6 ⭐⭐⭐ 🟡 A PM asks you to report the new onboarding's conversion using only logged-in visitors, which gives 3.5%, rather than all visitors, which gives 2.0%. Of 400,000 visitors 40% were logged in, and the 2.0% is across all of them. Work out the conversion for logged-out visitors and explain how you handle the request without damaging the relationship.
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Logged-out conversion is 1.0% (2,400 of 240,000), so I would report all visitors at 2.0% as the headline, show the logged-in 3.5% as a labelled segment, and explain why to the PM.

**Clarifying questions:**
- What did the old onboarding convert for logged-in visitors? The fair comparison is the same segment before and after.
- Does the new onboarding reach logged-out visitors at all? If not, the all-visitor rate is diluted by people who never saw it.
- What does the PM need the number for (a review, a bonus, a decision)? The need shapes the honest alternative.
- Is logged-in status itself affected by the change? If so, filtering on it is biased.
- Is the 3.5% for the same period as the 2.0%? Mixed periods mislead.

**Approach:**
1. Work out the missing segment: 400,000 x 40% = 160,000 logged-in, with 5,600 conversions; all visitors give 8,000 conversions, so logged-out gives 2,400 of 240,000 = 1.0%.
2. Check: 0.4 x 3.5% + 0.6 x 1.0% = 2.0%.
3. Meet the PM privately: "Logged-in looks great at 3.5%. If we report only that, someone will ask about the other 60%."
4. Offer a better framing: headline 2.0% for all visitors, then a table with both segments and the comparison to the old flow for each.
5. Show the real opportunity: logged-out is 1.0% on 240,000 visitors, the biggest room to grow.
6. If asked again to hide it, state that the full number goes in the doc, and escalate only if the misleading version is going to a decision-maker.

**Metrics:**
- Conversion = converters / visitors, for each segment and overall, with the same time window.
- Segment weights: 40% logged-in, 60% logged-out.
- Guardrail: the old flow's conversion for each segment.

**Risks:**
- A selected subset looks better because logged-in users are already more engaged.
- A reader may assume 3.5% is the rate for everyone.
- Damaging trust with the PM if I make it a confrontation.
- Cutting by a post-treatment variable creates bias.

**What the interviewer scores:**
- Strong: gets 1.0% quickly and verifies it. Weak: cannot split the average.
- Strong: gives the PM a constructive alternative (segment table). Weak: flat refusal or silent compliance.
- Strong: explains why the filter is misleading in one sentence. Weak: lectures on statistics.
- Strong: knows when to escalate. Weak: never or immediately.

**Example:** (illustrative numbers) 400,000 visitors; logged-in 160,000 at 3.5% = 5,600; all at 2.0% = 8,000; logged-out 2,400 / 240,000 = 1.0%. Weak answer: "No, I will not report that." Strong answer: "I can put 3.5% in the deck, as the logged-in segment next to the 2.0% overall and the old flow's rate, so nobody can say we hid anything."

**Code:**
```python
visitors = 400_000
li = visitors * 0.40
lo = visitors - li
conv_all = visitors * 0.02
conv_li = li * 0.035
conv_lo = conv_all - conv_li
print(f"logged-in {li:,.0f} -> {conv_li:,.0f}; logged-out {lo:,.0f} -> {conv_lo:,.0f} = {conv_lo/lo:.2%}")
assert (li, lo, round(conv_all), round(conv_li), round(conv_lo)) == (160000, 240000, 8000, 5600, 2400)
assert abs(conv_lo/lo - 0.01) < 1e-12
# weighted average check
assert abs(0.4*0.035 + 0.6*0.01 - 0.02) < 1e-12
# headline comparison needs the same segment in the old flow
print(f"logged-in rate is {0.035/0.01:.1f}x the logged-out rate")
assert round(0.035/0.01, 1) == 3.5
```

**Output (my run):**
```text
logged-in 160,000 -> 5,600; logged-out 240,000 -> 2,400 = 1.00%
logged-in rate is 3.5x the logged-out rate
```

**Follow-ups:**
- What if the PM insists on the 3.5% alone? I say I will include the full figure in the written doc and explain why.
- Is it ever fine to report logged-in only? Yes, if the product is for logged-in users only, and the label says so.

**Common mistakes:**
- Averaging 3.5% and 2.0% instead of solving for the missing segment.
- Making the PM feel accused.
- Forgetting to compare against the old flow for the same segment.

### Q7 ⭐⭐⭐ 🟡 A director says she wants an AI that tells the team which customers are unhappy, with no definition of unhappy, no decision attached and a vague deadline of next quarter. You have one analyst and one engineer available. How do you turn the request into something you can build and measure, and what do you refuse to start until it is agreed?
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would not start building until there is a definition of unhappy, a named decision and owner, and a date for a first version; with one analyst and one engineer I would offer a 4-week pilot on a simple list, not "an AI".

**Clarifying questions:**
- Who acts on the list, and what do they do (call, discount, escalate)? No action means no value.
- How many customers can the team act on each week? Capacity sets the size of the list.
- What would unhappy look like in past data (churn, complaint, low rating)? It gives us a label.
- What is a good outcome in numbers (saves, lower churn)? It gives us a target.
- What does "next quarter" mean: a demo, a pilot or a rollout? Scope depends on it.

**Approach:**
1. Turn "unhappy" into a testable label: for example churned within 90 days, or a complaint within 30 days. Agree it in writing with the director.
2. Attach a decision: weekly list of N customers for the success team to contact, with an owner.
3. Size it: the capacity and break-even precision (see the code: 40 per call, 600 per save, 30% save rate gives 22.2% break-even precision, about 2.8 times the 8% base rate).
4. Start with the analyst on a rules and simple-model baseline; the engineer builds the data feed and the weekly delivery.
5. Run a pilot for 4 weeks with a holdout of customers not contacted, to measure real saves.
6. Review at week 4 and decide whether to invest in a better model.

**Metrics:**
- Precision at K = customers on the list who became unhappy (by the agreed label) / K.
- Save rate = saved among contacted / contacted, versus a holdout group.
- Guardrails: contact fatigue, complaint rate, cost per call.

**Risks:**
- Building something nobody acts on.
- A label that moves later ("unhappy" redefined).
- Capacity of the success team, not the model, is the real bottleneck.
- A deadline promise made before scope.

**What the interviewer scores:**
- Strong: names what to refuse (no label, no decision, no owner) and what to build now. Weak: starts modelling immediately.
- Strong: connects the model to capacity and break-even. Weak: talks only about algorithms.
- Strong: proposes a small first deliverable inside the quarter. Weak: promises the full AI.
- Strong: keeps the director on side with a clear one-page agreement. Weak: pushes back with a long list of objections.

**Example:** (illustrative numbers) 5,000 customers, 8% unhappy (about 400), 60 calls a week. A call costs 40, a save is worth 600 and 30% of contacted unhappy customers are saved: break-even precision 40 / (600 x 0.30) = 22.2%; at 40% precision the weekly net is 1,920. Weak answer: "Sure, we will build an AI to detect unhappy customers." Strong answer: "Give me a label, an owner and a weekly capacity by Friday. In 4 weeks you will get a list, a holdout test, and a number for whether it pays."

**Code:**
```python
# Illustrative: once a decision exists, capacity and economics define what to build
customers, unhappy_rate = 5_000, 0.08
calls_per_week = 60                 # CSM capacity (illustrative)
cost_call, value_save, save_rate = 40, 600, 0.30
be_prec = cost_call / (value_save * save_rate)
print(f"unhappy customers ~ {customers*unhappy_rate:.0f}; break-even precision of the call list = {be_prec:.1%}")
assert customers*unhappy_rate == 400 and round(be_prec, 3) == 0.222
# random list precision = base rate; model needs lift over base
print(f"lift needed over random at top-{calls_per_week}: {be_prec/unhappy_rate:.2f}x")
assert round(be_prec/unhappy_rate, 2) == 2.78
# value per week at precision 40%
for prec in (0.08, be_prec, 0.40):
    v = round(calls_per_week * (prec * value_save * save_rate - cost_call), 6) + 0.0
    print(f"precision {prec:.1%}: net per week {v:,.0f}")
assert round(60*(0.4*600*0.3-40)) == 1920
```

**Output (my run):**
```text
unhappy customers ~ 400; break-even precision of the call list = 22.2%
lift needed over random at top-60: 2.78x
precision 8.0%: net per week -1,536
precision 22.2%: net per week 0
precision 40.0%: net per week 1,920
```

**Follow-ups:**
- What if she will not define unhappy? I propose two candidate definitions, show the customers each picks, and let her choose.
- What if the pilot fails? Then we stop with a clear number, which is a result.

**Common mistakes:**
- Agreeing to the deadline before the scope.
- Skipping the holdout, so saves cannot be measured.
- Optimising a model before the team can act on its output.

### Q8 ⭐⭐⭐ 🟡 Your tech lead wants a deep model for a routing task, but your gradient-boosted baseline reaches an AUC of 0.84 against 0.86 for his model. His model would cost 12,000 a month to serve and the baseline 1,500, a difference of 10,500 a month or 126,000 a year. How do you disagree with him in the design review, and what evidence would change your mind?
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** An AUC gain of 0.02 would have to be worth at least 10,500 a month, or 126,000 a year, so I would ask for that conversion in decision terms before agreeing to the deep model.

**Clarifying questions:**
- What is a wrong routing worth (cost per misroute)? It converts AUC into money.
- Is the 0.02 AUC difference stable (confidence interval, same holdout, same period)? Small gaps are often noise.
- What are the latency, maintenance and monitoring costs beyond serving? They add to the deep model's cost.
- Does the deep model have headroom (more data, retraining)? If it does, the gap may grow.
- Who maintains it, and is there the skill on the team? The cost of ownership matters.

**Approach:**
1. Agree the facts: 12,000 - 1,500 = 10,500 a month; x 12 = 126,000 a year.
2. Convert AUC to the business metric at the operating threshold, not overall: how many misroutes does 0.86 avoid compared with 0.84?
3. Break-even: at 4 per misroute (illustrative) and 1,000,000 tasks a month, the deep model must avoid 2,625 misroutes, a 0.26% reduction in error rate.
4. Compare it with the measured reduction on a holdout, with a paired bootstrap interval on the difference.
5. Say what would change my mind: a measured gain above break-even, with a confidence interval that stays above it, plus acceptable latency and monitoring.
6. Propose a cheap next step: a shadow run of both models for 2 weeks.

**Metrics:**
- Net benefit per month = (misroutes avoided x cost per misroute) - 10,500.
- AUC difference with a paired bootstrap interval (same examples).
- Guardrails: p95 latency, drift alerts, retraining effort.

**Risks:**
- AUC is rank quality; the decision may depend on one threshold or a segment.
- The deep model's accuracy may degrade faster under drift.
- Arguing from taste, not evidence, makes it a status contest.
- Being proved wrong is fine; hiding the numbers is not.

**What the interviewer scores:**
- Strong: converts AUC into money and gives the break-even. Weak: "simple models are better."
- Strong: respects his idea and asks what evidence would settle it. Weak: dismisses it.
- Strong: proposes a time-boxed test. Weak: waits for the design review to decide.
- Strong: includes total cost of ownership. Weak: only serving cost.

**Example:** (illustrative numbers) At 4 per misroute and 1,000,000 tasks a month, 10,500 buys 2,625 misroutes, or 0.263% of tasks. If the deep model avoids 4,000 misroutes it earns 16,000 - 10,500 = 5,500 a month; if 1,000 it loses 6,500. Weak answer: "I do not think we need a deep model, the baseline is good enough." Strong answer: "I like the idea. It needs to avoid about 2,600 misroutes a month to pay for itself. Can we shadow both for two weeks and look at that number?"

**Code:**
```python
cost_dl, cost_gb = 12_000, 1_500
month = cost_dl - cost_gb
print("extra serving cost:", month, "a month,", month*12, "a year")
assert month == 10_500 and month*12 == 126_000
# misroute reduction needed to pay for it (illustrative volumes and cost)
tasks, cost_mis = 1_000_000, 4.0
need = month / cost_mis
print(f"need {need:,.0f} fewer misroutes a month = {need/tasks:.3%} of {tasks:,} tasks")
assert need == 2625 and round(need/tasks, 5) == 0.00263
# with a different cost per misroute
for c in (1.0, 4.0, 20.0):
    print(f"cost per misroute {c}: need {month/c/tasks:.3%} error-rate reduction")
assert round(month/20/tasks, 6) == 0.000525
```

**Output (my run):**
```text
extra serving cost: 10500 a month, 126000 a year
need 2,625 fewer misroutes a month = 0.263% of 1,000,000 tasks
cost per misroute 1.0: need 1.050% error-rate reduction
cost per misroute 4.0: need 0.263% error-rate reduction
cost per misroute 20.0: need 0.052% error-rate reduction
```

**Follow-ups:**
- What if the value per misroute is 20? The break-even drops to 0.05%, so the deep model likely pays.
- What if he still insists after the shadow test shows no gain? Record the decision and the metric to revisit; disagree and commit.

**Common mistakes:**
- Quoting 0.02 AUC as "small" or "large" without a decision value.
- Counting only serving cost.
- Forgetting the confidence interval.

### Q9 ⭐⭐⭐ 🟡 A PM wants a personalised experience for a segment of 800 users a week, which gives 400 per arm, with baseline conversion of 5%, and expects a 0.5 percentage point lift. The standard error of the difference in a single week's conversion is about 1.5 percentage points. Say no with data, and propose what you would do instead.
**Asked at:** Prioritisation and saying-no prompt pages (many Dataford pages on prioritising competing stakeholder requests, a codemia page on saying no to a request, a Towards Data Science stakeholder-management article on declining requests and agreeing a start-now versus later list); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** With 400 users per arm a week and a 5% baseline, a 0.5 point lift is about a third of one standard error (power about 6%), so a weekly test cannot see it; the sample needed is about 31,000 per arm, or roughly 78 weeks.

**Clarifying questions:**
- Is the 0.5 point lift based on evidence or a hope? If it is a guess, the true effect could be smaller.
- Is the personalisation cheap and reversible? Then a launch with monitoring may be reasonable.
- Are the 800 users a week unique, and can we widen the segment? More users shrink the wait.
- Is there a faster metric (click, add to cart) tied to conversion? A higher-rate metric needs fewer users.
- What is the cost of building and running it? It sets how much proof we need.

**Approach:**
1. State the arithmetic: SE of the difference = sqrt(2 x 0.05 x 0.95 / 400) = 1.54 points, so 0.5 points is only 0.32 SE.
2. Power at that size is about 6.2% per week, close to the false-positive rate.
3. Sample size for 80% power: about 31,231 per arm; at 400 per arm per week that is about 78 weeks.
4. Minimum detectable effect: 4.3 points in one week, 2.2 in 4 weeks, 1.2 in 12 weeks; so only a big lift is testable.
5. Offer alternatives: widen the segment, use a higher-rate proxy metric with a validated link, use variance reduction, or test on a pooled population and look at the segment as a subgroup.
6. If it is cheap and safe, ship with monitoring and a pre-agreed rollback instead of claiming proof.

**Metrics:**
- Conversion = converters / users in the arm; effect = treatment rate - control rate.
- Power = P(reject null | true effect 0.5 points); MDE at 80% power.
- Guardrails: conversion of the broader population, complaints.

**Risks:**
- An underpowered test gives a noisy answer that can be read as proof either way.
- Running for 78 weeks lets the world change under the test.
- A proxy metric may not translate to conversion.
- Saying only "no" loses the PM; offer a plan.

**What the interviewer scores:**
- Strong: computes SE, power, sample size and weeks. Weak: "the sample is too small" without numbers.
- Strong: says what we can do instead. Weak: a bare refusal.
- Strong: distinguishes "cannot prove" from "should not do." Weak: treats it as the same.
- Strong: keeps the PM as a partner. Weak: sounds like a gatekeeper.

**Example:** (illustrative numbers) 400 per arm, 5.0% versus 5.5%: SE 1.54 points, power 6%. Weak answer: "No, we do not have enough sample." Strong answer: "Each week we can only see a lift of 4 points or more; yours is 0.5. To prove it we would need about 31,000 per arm, which is 78 weeks. What I can do is widen the segment, use click-through as an early signal, or ship it cheaply with a rollback."

**Code:**
```python
import math
from scipy import stats
n, p0, d = 400, 0.05, 0.005
se = math.sqrt(2*p0*(1-p0)/n)
print(f"SE of difference {se*100:.2f} pp; effect/SE = {d/se:.2f}")
assert abs(se - 0.0154) < 1e-4 and round(d/se, 2) == 0.32
z = stats.norm.isf(0.025)
power = stats.norm.sf(z - d/se) + stats.norm.cdf(-z - d/se)
print(f"power per week at n=400 per arm: {power:.1%}")
assert 0.05 < power < 0.07
# sample size for 80% power, 5.0% vs 5.5%
p1 = p0 + d
var = p0*(1-p0) + p1*(1-p1)
need = (z + stats.norm.isf(0.2))**2 * var / d**2
weeks = need / n
print(f"per arm needed: {math.ceil(need):,}; weeks at 400 per arm per week: {weeks:.0f}")
assert math.ceil(need) == 31_231 and round(weeks) == 78
# smallest detectable effect (80% power) at 4 weeks and 12 weeks
for w in (1, 4, 12):
    s = math.sqrt(2*p0*(1-p0)/(n*w))
    print(f"{w} weeks: MDE {(z + stats.norm.isf(0.2))*s*100:.1f} pp")
assert round((z + stats.norm.isf(0.2))*math.sqrt(2*p0*(1-p0)/n)*100, 1) == 4.3
```

**Output (my run):**
```text
SE of difference 1.54 pp; effect/SE = 0.32
power per week at n=400 per arm: 6.2%
per arm needed: 31,231; weeks at 400 per arm per week: 78
1 weeks: MDE 4.3 pp
4 weeks: MDE 2.2 pp
12 weeks: MDE 1.2 pp
```

**Follow-ups:**
- What if the segment grew to 8,000 a week? Then 4,000 per arm gives about 8 weeks, which is plausible. (see Book 6 Part 4, Q12 for a worked sample-size answer; its heading starts "Baseline conversion is 5.0%")
- Can sequential testing help? It lets us stop early for large effects but does not change the sample needed for a small one.

**Common mistakes:**
- Saying "not significant" instead of "cannot detect an effect this size."
- Using the wrong variance (one arm instead of the difference).
- Running a weekly test and peeking.
