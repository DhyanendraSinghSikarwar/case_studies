# Book 6 — Part 6: Stakeholder Conflicts and Trade-off Decisions

**Topic:** Scenario-based "you and a stakeholder disagree, or two good options conflict; what do you do" questions for Data Scientist, Product Analyst and ML Engineer loops: a launch date the model cannot meet, business distrust of findings, accuracy versus latency versus cost versus interpretability, speed versus rigour under a deadline, ethics, fairness and privacy pushback, pressure to inflate or cherry-pick metrics, vague or shifting requirements, disagreeing with a senior person or an executive, saying no with data, backlog prioritisation, build versus buy politics, explaining a model to executives or regulators, owning a failed model or a wrong analysis, cross-team dependencies, resourcing disagreements, engineering versus data-science tension on productionising, ML versus rules baselines, dashboard versus model requests, black-box explanation demands, and AI-era twists (an LLM for everything, hallucination-risk acceptance, vendor API versus self-hosting, reviewing AI-written analysis).

**Target:** 45  |  **Actual:** 45 (⭐⭐⭐ 15, ⭐⭐ 20, ⭐ 10)  |  **Date:** 2026-10-30  |  **Status:** Complete (answers merged, checked, reviewed)

**Scope note:** this part keeps to trade-off decisions and stakeholder conflicts inside data-science and ML work, with numbers where a cost of delay, a threshold or an expected value can be computed. Generic behavioural scripts (conflict with a coworker, a time you failed, leadership stories) belong to Book 9 and are not repeated here; experiment theory belongs to Book 1 Part 10 and Book 6 Part 4, business case maths to Book 6 Part 5, and model degradation to Book 6 Part 2. Wave B answers should cross-reference those only by checked headings. All numbers in the prompts are invented illustrative numbers in one unnamed currency unit, not data from any company; every percentage names its base in the prompt, and every arithmetic claim in a prompt is checked in scratch/B6P06_wavea/qs.py. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part06_sources.md). Searches returned Dataford, PracHub, codemia and Yardstick stakeholder-conflict and pushback prompt pages, trade-off guides, prioritisation and saying-no pages, ethics and explainability material, productionising pages and 2026 vendor and CTO posts on LLM build versus buy. Most results were user-contributed prompt pages or general guidance with few model answers; none tied a scenario to a verified employer round, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

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

### Q10 ⭐⭐⭐ 🟡 The head of engineering wants to build a forecasting system in house, while finance wants to buy a vendor tool, and each side says the other is hiding costs. The build costs 900 up front plus 150 a year to maintain, and the vendor charges 400 a year, in thousands of one unit. Compute the 3-year cost of each, the break-even horizon, and the non-cost questions you would raise before recommending.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing
**Say this first (1 line):** Over 3 years build costs 1,350 and the vendor 1,200, so the vendor is cheaper by 150 and break-even is 3.6 years; but both sides' hidden-cost claims move that number, so I would price the hidden costs before recommending.

**Clarifying questions:**
- What does the forecast feed, and how bad is a miss? It decides whether control and accuracy matter more than cost.
- Is 150 a year only cloud and licences, or does it include the people who maintain it? Maintenance is where build budgets usually leak.
- Does the vendor price rise each year, and what do integration and exit cost? Finance's "hidden cost" claim lives here.
- How long is the planning horizon and what discount rate does finance use? Break-even at 3.6 years only matters if we keep the tool 4 years or more.
- Can we pilot the vendor on one product line? A pilot turns an opinion fight into evidence.

**Approach:**
1. Compute the plain numbers. Build: 900 + 3 x 150 = 1,350. Vendor: 3 x 400 = 1,200. Break-even: 900 / (400 - 150) = 3.6 years.
2. Say what they mean. Vendor wins until year 3.6; after that build wins, if the numbers hold.
3. Test each side's hidden-cost claim. If maintenance is 250 a year, break-even moves to 6 years. If the vendor raises price 10% a year, vendor 3-year cost is 1,324 and it flips to dearer than build in year 4.
4. Add the time value of money (illustrative 10%): present cost of build 1,273 versus vendor 995.
5. Then raise the non-cost questions: time to first forecast, accuracy on our data, control and customisation, data security and residency, vendor lock-in and exit, staff to maintain, and the cost of being wrong.
6. Recommend a decision rule, not a winner: buy and pilot if time-to-value and a 3-year horizon matter; build if the forecast is core, customisation is needed and we plan 5+ years.

**Metrics:**
- 3-year total cost of ownership = up-front + annual cost x 3 (all in thousands of one unit).
- Break-even horizon (years) = up-front cost / (vendor annual - build annual).
- Present cost = sum of discounted cash flows at the stated rate.
- Guardrails: forecast error (WAPE) on a common holdout, time to first usable forecast, and incident count.

**Risks:**
- Break-even assumes costs are flat. Real build maintenance and vendor prices both drift.
- The cost numbers ignore the benefit: a more accurate forecast can be worth far more than 150.
- Politics: each side owns one number. Do not let the cheaper number decide a strategic question.
- Build estimates are usually optimistic; the 900 is a forecast too.

**What the interviewer scores:**
- Strong: gets 1,350, 1,200 and 3.6, and says vendor is cheaper over 3 years. Weak: says "build is cheaper long term" without computing.
- Strong: tests both hidden-cost claims with numbers. Weak: argues from opinion.
- Strong: raises accuracy, speed, control, lock-in and staffing. Weak: cost only.
- Strong: proposes a pilot or decision rule that both sides accept. Weak: picks a side.

**Example:** (illustrative numbers, thousands) Year by year: build 1,050 / 1,200 / 1,350 / 1,500; vendor 400 / 800 / 1,200 / 1,600. They cross between years 3 and 4 (at 3.6). Weak answer: "Build, it is cheaper in the long run." Strong answer: "Over three years the vendor is cheaper by 150. Break-even is 3.6 years, and if maintenance is really 250 it is 6 years. I would pilot the vendor for accuracy on our data, and ask finance and engineering to agree the maintenance and price-escalation assumptions in writing."

**Code:**
```python
# Q10: build vs buy (thousands of one unit, illustrative)
build_up, build_yr, vendor_yr = 900, 150, 400
b3 = build_up + 3 * build_yr
v3 = 3 * vendor_yr
be = build_up / (vendor_yr - build_yr)          # years where cumulative costs meet
print("3-year build", b3, "vendor", v3, "vendor cheaper by", b3 - v3)
print("break-even years", be)
assert (b3, v3, be) == (1350, 1200, 3.6)

# sensitivity 1: maintenance really 250 a year (the 'hidden cost' finance fears)
be_hi = build_up / (vendor_yr - 250)
print("break-even if maintenance 250:", be_hi)
assert be_hi == 6.0
# sensitivity 2: vendor raises price 10% a year (the 'hidden cost' engineering fears)
def cum_vendor(y, esc=0.10):
    return sum(vendor_yr * (1 + esc) ** k for k in range(y))
def cum_build(y):
    return build_up + build_yr * y
for y in range(1, 6):
    print("year", y, "build", cum_build(y), "vendor+10%/yr", round(cum_vendor(y), 1))
assert round(cum_vendor(3), 1) == 1324.0 and cum_vendor(3) < cum_build(3)
assert cum_vendor(4) > cum_build(4)             # flips in year 4
# sensitivity 3: discount at 10%, upfront at t0, annual costs at year end
r = 0.10
ann = sum(1 / (1 + r) ** t for t in (1, 2, 3))
pv_b = build_up + build_yr * ann
pv_v = vendor_yr * ann
print("PV build", round(pv_b, 1), "PV vendor", round(pv_v, 1))
assert round(pv_b, 1) == 1273.0 and round(pv_v, 1) == 994.7
```

**Output (my run):**
```text
3-year build 1350 vendor 1200 vendor cheaper by 150
break-even years 3.6
break-even if maintenance 250: 6.0
year 1 build 1050 vendor+10%/yr 400.0
year 2 build 1200 vendor+10%/yr 840.0
year 3 build 1350 vendor+10%/yr 1324.0
year 4 build 1500 vendor+10%/yr 1856.4
year 5 build 1650 vendor+10%/yr 2442.0
PV build 1273.0 PV vendor 994.7
```

**Follow-ups:**
- What if the vendor is 20% more accurate? Then the forecast benefit probably dwarfs 150; measure it on a holdout.
- What if we expect to stay 6 years? Build wins on cost (900 + 900 = 1,800 against 2,400), if maintenance stays at 150.

**Common mistakes:**
- Comparing only 3-year totals and ignoring break-even.
- Treating the build estimate as certain.
- Ignoring non-cost factors such as lock-in and speed.
- Taking a side before pricing the hidden costs.

### Q11 ⭐⭐⭐ 🟡 A business owner says he cannot trust a model unless you tell him the exact rule behind each score. For one customer the churn probability is 17%, against a 10% base rate, and SHAP-style contributions are +6, +3 and -2 percentage points from three features. Show how you would explain this score, and say what you would not claim about the explanation.
**Asked at:** Explainability material (hirevire explainability pre-screening questions, fluxforce and other compliance-oriented pages on SHAP for regulators and model-risk guidance, a SHAP error-review workflow page); mostly vendor and practitioner pages rather than interview banks; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would say: this customer's risk is 17% against a 10% average; two features push it up by 6 and 3 points, one pulls it down by 2, and the net is plus 7; and I would not call these causes or rules.

**Clarifying questions:**
- What decision does he make from the score (call, discount, nothing)? The explanation should serve that action.
- Does he want a rule, or a reason he can check? A rule is a different model class (a scorecard or tree), so ask what he really needs.
- Are the three features ones he understands and can verify? An explanation in unreadable feature names is no explanation.
- Is there a regulator or customer who will see the reason? That raises the bar for stability and wording.
- How accurate is the score, calibrated or not? 17% is only meaningful if it is calibrated.

**Approach:**
1. Start with the base rate: "Out of 100 similar customers, about 10 leave."
2. Give the arithmetic: 10 + 6 + 3 - 2 = 17. The attributions add up to the gap between this customer and the average.
3. Translate each feature into plain words: "Long gap since last order: +6. Fewer logins: +3. On an annual plan: -2." (names invented)
4. Say what the numbers are: how this model arrived at this score, relative to an average customer.
5. Say what they are not: not the cause of churn, not an exact rule, not a promise that changing a feature changes the outcome.
6. Offer what he can trust instead of a rule: calibration (of customers scored near 17%, about 17 in 100 leave), a holdout result, and a simple surrogate (short rule list) clearly labelled as approximate.

**Metrics:**
- Local additivity check: base + sum(contributions) = score (10 + 7 = 17).
- Calibration: among customers scored 15-19%, observed churn rate.
- Explanation stability: share of customers whose top-3 features stay the same under retraining (guardrail).
- Surrogate fidelity if a rule list is offered: share of customers where the rule list and the model agree on the high/low call.

**Risks:**
- SHAP-style values explain the model, not the world. A feature with +6 is not a cause.
- With feature correlation or interactions, the contribution is not what happens if you change that feature (the code shows 0.15 attributed but a 0.25 change).
- Contributions depend on the baseline chosen and on the model; they can shift on retraining.
- Over-promising "exact rule" language invites a challenge you cannot meet.

**What the interviewer scores:**
- Strong: base rate, arithmetic (17 = 10 + 6 + 3 - 2), plain-language features. Weak: shows a bar chart without saying what it means.
- Strong: says what the explanation does not claim (cause, rule, counterfactual). Weak: "this is why he will leave."
- Strong: offers calibration and a holdout as the basis for trust. Weak: argues the model is too complex to explain.
- Strong: asks what decision it feeds. Weak: jumps to tooling.

**Example:** (illustrative numbers) Weak: "The model says 17% because feature 1 matters most." Strong: "Typical customers leave about 10% of the time. This one is 17%: seven points higher. About six points come from the long gap since the last order, three from fewer logins, and the annual plan takes two off. That tells us what the model is reacting to; it does not prove the gap causes churn. When we score customers near 17%, roughly 17 in 100 really left last quarter, and that is the evidence I would ask you to trust."

**Code:**
```python
# Q11: explaining one churn score (illustrative; percentage points)
base = 10.0
contrib = {"feature_1": +6.0, "feature_2": +3.0, "feature_3": -2.0}
score = base + sum(contrib.values())
print("base", base, "sum of contributions", sum(contrib.values()), "score", score)
assert sum(contrib.values()) == 7.0 and score == 17.0
# additivity check: dropping the largest contributor
print("score if feature_1 contribution were zero:", score - contrib["feature_1"])
assert score - contrib["feature_1"] == 11.0
# relative framing
print("risk ratio vs base:", round(score / base, 2))
assert round(score / base, 2) == 1.7
# What additivity does NOT say: removing feature_1 from the real model need not give 11.
# Tiny interaction example: p = 0.10 + 0.05*a + 0.05*b + 0.20*a*b with a=b=1 -> 0.40.
# Shapley split of the interaction is even, so a and b each get 0.05 + 0.10 = 0.15, base 0.10.
def f(a, b): return 0.10 + 0.05 * a + 0.05 * b + 0.20 * a * b
phi_a = 0.5 * ((f(1, 0) - f(0, 0)) + (f(1, 1) - f(0, 1)))
phi_b = 0.5 * ((f(0, 1) - f(0, 0)) + (f(1, 1) - f(1, 0)))
print("Shapley a", round(phi_a, 3), "b", round(phi_b, 3), "sum + base", round(f(0, 0) + phi_a + phi_b, 3))
assert abs(f(0, 0) + phi_a + phi_b - f(1, 1)) < 1e-12
print("but setting a to 0 changes p by", round(f(1, 1) - f(0, 1), 3), "not", round(phi_a, 3))
assert abs((f(1, 1) - f(0, 1)) - 0.25) < 1e-12 and abs(phi_a - 0.15) < 1e-12
```

**Output (my run):**
```text
base 10.0 sum of contributions 7.0 score 17.0
score if feature_1 contribution were zero: 11.0
risk ratio vs base: 1.7
Shapley a 0.15 b 0.15 sum + base 0.4
but setting a to 0 changes p by 0.25 not 0.15
```

**Follow-ups:**
- He insists on exact rules. Then offer a simpler, transparent model or a rule list and show the accuracy you give up; do not pretend the complex model has rules.
- Can I use the contributions to choose a retention offer? Only as a hint; test the offer in an experiment.

**Common mistakes:**
- Calling attributions causes.
- Quoting contributions without the base rate.
- Showing a chart with technical feature names.
- Promising that the explanation will not change on retraining.

### Q12 ⭐⭐⭐ 🟡 Four stakeholders each want a data-science project, and the team has 10 weeks of capacity. Project A is worth 280 (in thousands of one unit) and takes 6 weeks, B is worth 200 and takes 2, C is worth 150 and takes 3 and D is worth 120 and takes 5. Rank them by value per week, then find the best combination that fits in 10 weeks, and say how you tell the losers.
**Asked at:** Prioritisation and saying-no prompt pages (many Dataford pages on prioritising competing stakeholder requests, a codemia page on saying no to a request, a Towards Data Science stakeholder-management article on declining requests and agreeing a start-now versus later list); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** By value per week the order is B (100), C (50), A (46.7), D (24), but the best 10-week plan is A plus B at 480 using 8 weeks, which beats the ratio-greedy B, C and D at 470.

**Clarifying questions:**
- Are the values comparable and how sure are they? A value of 280 from a sponsor's guess is not the same as one from a measured baseline.
- Can a project be split or phased? A half-A in 3 weeks might change the answer.
- Are the 10 weeks the whole team's, or are there skill limits? Capacity by skill matters.
- Is there a deadline or dependency (a regulatory project, or one that unlocks another)? That overrides ratios.
- Do I keep slack for support and meetings? If real capacity is 8 weeks, the answer changes.

**Approach:**
1. Value per week: A 280/6 = 46.7, B 200/2 = 100, C 150/3 = 50, D 120/5 = 24. Rank B, C, A, D.
2. Greedy by ratio: B (2) + C (3) = 5 weeks; A needs 6, does not fit; D (5) fits. Total 10 weeks, value 470.
3. Check all combinations (only 15, so enumerate): A + B = 8 weeks, value 480. That is best. A + C is 430; B + C + D is 470.
4. Note the 2 spare weeks. Use them for a small item, support, or slack. C needs 3, so it does not fit.
5. Recommend A + B now, C and D on a dated later list.
6. Tell the losers early, with the reason and a re-entry date; see below.

**Metrics:**
- Value per week = estimated value / estimated weeks.
- Plan value = sum of values of chosen projects, subject to total weeks at most 10.
- Guardrails: confidence in each estimate, slack (weeks spare), dependencies.

**Risks:**
- Value and effort are estimates; a 20% overrun on A (7.2 weeks) leaves B still fitting but the 2-week slack gone.
- Ratio ranking is only a heuristic, as the 470 versus 480 shows.
- Whoever shouts loudest tends to win unless the scoring is shared.
- Telling losers late damages trust more than telling them "no".

**What the interviewer scores:**
- Strong: correct ratios and the point that greedy-by-ratio is not optimal. Weak: picks the top three ratios and stops.
- Strong: checks combinations and names the 2 spare weeks. Weak: ignores capacity left over.
- Strong: communicates the decision with criteria and a re-entry date. Weak: silent or vague "maybe later".
- Strong: asks about uncertainty and dependencies. Weak: treats the numbers as exact.

**Example:** (illustrative) Weak: "B, C and A are the top three, so we do those." That is 11 weeks and does not fit. Strong, to the owner of C: "C is a good project, 50 value per week. This quarter we chose A and B because together they deliver 480 against 470 for the alternative and fit in 8 weeks. C goes first on next quarter's list; if you can show its value is higher than 150, or that it can be done in 2 weeks, I will rescore it."

**Code:**
```python
from itertools import combinations
P = {"A": (280, 6), "B": (200, 2), "C": (150, 3), "D": (120, 5)}   # value (thousands), weeks
cap = 10
ratio = {k: v / w for k, (v, w) in P.items()}
rank = sorted(ratio, key=ratio.get, reverse=True)
print("value per week:", {k: round(ratio[k], 1) for k in rank}, "rank", rank)
assert rank == ["B", "C", "A", "D"] and round(ratio["A"], 1) == 46.7
# greedy by ratio
used = val = 0; picked = []
for k in rank:
    if used + P[k][1] <= cap:
        used += P[k][1]; val += P[k][0]; picked.append(k)
print("greedy by ratio:", picked, "weeks", used, "value", val)
assert (picked, used, val) == (["B", "C", "D"], 10, 470)
# exhaustive search
best = (0, ())
for r in range(1, 5):
    for c in combinations(P, r):
        w = sum(P[k][1] for k in c); v = sum(P[k][0] for k in c)
        if w <= cap and v > best[0]: best = (v, c)
        if w <= cap: print(" ", "+".join(c), "weeks", w, "value", v)
print("best:", best)
assert best == (480, ("A", "B")) and sum(P[k][1] for k in best[1]) == 8
print("spare weeks with best:", cap - 8, "-> C (3 weeks) does not fit; value lost to greedy:", 480 - 470)
```

**Output (my run):**
```text
value per week: {'B': 100.0, 'C': 50.0, 'A': 46.7, 'D': 24.0} rank ['B', 'C', 'A', 'D']
greedy by ratio: ['B', 'C', 'D'] weeks 10 value 470
  A weeks 6 value 280
  B weeks 2 value 200
  C weeks 3 value 150
  D weeks 5 value 120
  A+B weeks 8 value 480
  A+C weeks 9 value 430
  B+C weeks 5 value 350
  B+D weeks 7 value 320
  C+D weeks 8 value 270
  B+C+D weeks 10 value 470
best: (480, ('A', 'B'))
spare weeks with best: 2 -> C (3 weeks) does not fit; value lost to greedy: 10
```

**Follow-ups:**
- What if A slips by 3 weeks? A + B then takes 11 and does not fit; I would cut scope on A or drop to B + C + D (470).
- How do you tell D's owner? Lowest value per week (24); offer a smaller version or a self-serve alternative.

**Common mistakes:**
- Ranking by value alone.
- Stopping at greedy and calling it optimal.
- Forgetting support and meeting time.
- Saying "later" with no date.

### Q13 ⭐⭐⭐ 🔴 A loan model approves 60% of applicants in group A and 42% in group B, a ratio of 0.7 against a four-fifths style screening heuristic of 0.8. The business head says the gap simply reflects different repayment risk and wants to ship this week. How do you test his claim, what options do you put on the table, and when do you escalate?
**Asked at:** Ethics and fairness material (Yardstick data-ethics question page asking how bias was handled without disrupting the business, a University of Virginia online-ethics case on whether to keep a sensitive attribute in a model, a Data Science Newsletter ethics page, pre-screening pages on unethical data requests); practitioner pages rather than a confirmed interview bank; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The ratio is 42 / 60 = 0.70, below the 0.8 guideline, so I would not ship this week on assertion; I would test his claim by comparing approvals and defaults within risk bands, and escalate if the gap is not explained.

**Clarifying questions:**
- Which law and policy govern this product, and who owns fair-lending review? The 0.8 four-fifths figure is a screening heuristic borrowed from employment selection, not a lending test; the compliance team decides which test applies (check with legal).
- What defines groups A and B, and is the attribute used by the model or only known later? It decides whether you can measure at all.
- How many applicants per group, and what is the repayment history? Small samples make the ratio noisy.
- Which features drive the score, and are any proxies for the group (location, device, surname-based)? Proxies can hide the problem.
- What is the cost of delay versus the cost of a bad launch? It sets how hard to push back on "this week".

**Approach:**
1. Confirm the arithmetic and the noise: 0.42 / 0.60 = 0.70. With 10,000 applicants each (illustrative) the 18-point gap is far outside sampling error, so it is real, not noise.
2. Test his claim: "different repayment risk" is a testable hypothesis. Compare within risk bands (or score deciles), both approval rates and actual default rates, by group.
3. Read the result. If approvals are equal within each band and the risk mix differs, the gap is explained (code World 1). If B is approved less than A in the same band with the same default rate, it is not explained (World 2). Both worlds give the same 0.70 headline.
4. Put options on the table: ship as is with documented justification (only if explained), remove or constrain proxy features, adjust thresholds by band, or search for a less discriminatory alternative model and compare accuracy loss; or a limited launch with monitoring.
5. Set the escalation trigger in advance: escalate to compliance or model-risk now if the gap is unexplained after the band analysis, or if a proxy feature is found, or if he insists on shipping over an unresolved flag.
6. Document everything: the test, the alternatives considered and the decision owner.

**Metrics:**
- Impact ratio = approval rate of group B / approval rate of group A (0.42 / 0.60 = 0.70).
- Within-band approval ratio, per band, B over A; and default rate per band per group (calibration by group).
- Mix-standardised ratio = approval rate B would have with A's risk mix / A's approval rate.
- Guardrails: accuracy cost of each alternative (AUC, default rate), and approval volume.

**Risks:**
- Using the ratio alone: a ratio above 0.8 is not proof of fairness either.
- "Risk" measured by the model's own score is circular; use observed defaults.
- Defaults are only observed for approved applicants (selection bias), so the evidence for rejected ones is thin.
- Dropping a sensitive attribute does not remove the gap if proxies remain.
- Shipping quietly and fixing later: the legal and reputational cost can far exceed a week's delay.

**What the interviewer scores:**
- Strong: turns his claim into a test (within-band approvals and defaults). Weak: argues about fairness in the abstract.
- Strong: lists concrete options with costs, including less discriminatory alternatives. Weak: "just drop the feature".
- Strong: names escalation triggers and the right owner (compliance, model risk). Weak: either ships silently or refuses outright.
- Strong: hedges the legal test and asks compliance. Weak: states the four-fifths rule as the lending law.

**Example:** (illustrative) Weak: "The ratio is 0.7, so we cannot ship." Or: "He says it's risk, so fine." Strong: "I agree it could be risk, so let's check. If B applicants approved are as likely to repay as A applicants in each band, we have an explanation. If B is approved less in the same band, it is not risk. I will have the band table by Wednesday; if it is unexplained I will take it to compliance before any launch, and meanwhile propose a limited launch on the bands where the gap is zero."

**Code:**
```python
import math
# headline: approval rates and impact ratio
ra, rb = 0.60, 0.42
print("impact ratio", round(rb / ra, 2))
assert round(rb / ra, 2) == 0.70 and rb / ra < 0.8
# is the gap beyond noise? invented n = 10,000 applicants per group
n = 10_000
se = math.sqrt(ra * (1 - ra) / n + rb * (1 - rb) / n)
z = (ra - rb) / se
print("gap 18 pts, z =", round(z, 1))
assert z > 25
# Test of the business head's claim: compare approval WITHIN risk bands (invented).
# policy approves 90% / 50% / 10% of low / mid / high risk bands, same for both groups
rate = {"low": 0.9, "mid": 0.5, "high": 0.1}
mixA = {"low": 0.50, "mid": 0.25, "high": 0.25}
mixB = {"low": 0.25, "mid": 0.30, "high": 0.45}
def overall(mix, adj=1.0):
    return sum(mix[b] * rate[b] * adj for b in mix)
oA, oB = overall(mixA), overall(mixB)
print("World 1 (explained by mix): A", round(oA, 3), "B", round(oB, 3), "ratio", round(oB / oA, 2))
assert round(oA, 3) == 0.60 and round(oB, 3) == 0.42
# standardise B to A's mix: if equal within bands, ratio is 1.0
std = overall(mixA)
print("World 1 mix-standardised ratio:", round(std / oA, 2))
assert std / oA == 1.0
# World 2: B gets only 70% of the approval rate A gets in EVERY band, same risk mix as A
oB2 = overall(mixA, 0.70)
print("World 2 (not explained): B with A's own mix:", round(oB2, 3), "ratio", round(oB2 / oA, 2))
assert round(oB2 / oA, 2) == 0.70
# Same 0.70 headline from two different worlds: only the within-band comparison tells them apart.
# If risk is real, defaults should match the score: observed default per band should be equal across groups.
```

**Output (my run):**
```text
impact ratio 0.7
gap 18 pts, z = 25.9
World 1 (explained by mix): A 0.6 B 0.42 ratio 0.7
World 1 mix-standardised ratio: 1.0
World 2 (not explained): B with A's own mix: 0.42 ratio 0.7
```

**Follow-ups:**
- What if the gap is explained by mix? Document it, still check proxies, and monitor monthly.
- What if fixing it costs accuracy? Quantify it (for example approvals and defaults at the same volume) and let the risk owner decide with the numbers.

**Common mistakes:**
- Treating 0.8 as a legal line for lending.
- Accepting "different risk" without a within-band test.
- Removing the attribute and declaring victory.
- Escalating with no analysis, or never escalating.

### Q14 ⭐⭐⭐ 🔴 Your demand model forecast 118,000 units for a month in which 100,000 were sold, and, if supply ordered to the forecast, the 18,000 excess units cost up to 25 each in markdowns and holding (450,000 at most). The supply-chain head is angry and asks in front of the group who approved the model. Say what you do in the first hour, the first week and the next quarter, including how you own your part.
**Asked at:** Project-conflict prompts (PracHub pages on ML project milestones, scope and conflict, on stakeholder conflict under a compressed delivery timeline and on cross-functional pushback on an analysis; one is tagged to a large marketplace and one to a social platform on the page, unverified); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would not defend or hide; in the first hour I would say "the forecast was 18% high, that cost up to 450,000, I own the model's part, and I will bring a root cause in a week."

**Clarifying questions:**
- Did supply order exactly to the forecast, or add a buffer or cut? The 450,000 only holds if all 18,000 excess units were bought on the forecast alone.
- Who approved the model and the decision to order to the point forecast? It sets shared ownership without pointing fingers.
- Is this one bad month or a pattern? One miss of +18% is only meaningful against the model's history.
- Can the excess be sold later or returned? That reduces the real cost.
- What did the old method forecast? The right comparison is the alternative, not perfection.

**Approach:**
1. First hour: stay calm and factual. Confirm the numbers (118,000 against 100,000 is +18,000, or 18% over actual; at 25 each, up to 450,000). Say what you know and do not know. Own your part: "the forecast was mine; the error is mine to explain." Do not argue about who approved it in front of the group; offer to walk through the approval trail afterwards. Ask supply to hold further orders based on the old number while you check.
2. First week: root cause. Compare forecast and actual by product, region and week; check for data issues, a promo that was cancelled, a price change, stockouts that hid true demand, or a model bug. Compare with the old method and with the model's error history. Share a one-page note with supply: what happened, the cost range, what changes.
3. First week: agree interim controls with supply: forecast ranges instead of a point, a human review of large moves, a weekly bias check.
4. Next quarter: change the design. Report bias and error by segment, forecast intervals, and order using the cost ratio of under versus over-stock (code: if a shortage costs 40 and an excess 25 (invented), order at the 61.5th percentile of demand, not the average). Set an agreed alert when bias exceeds a threshold. Review the approval process: who signs off and on what evidence.
5. Close the loop: show supply the before and after error, and invite them into the next review.

**Metrics:**
- Bias (MPE) = (forecast - actual) / actual = +18%.
- WAPE = sum of absolute errors / sum of actuals, by segment.
- Cost of error = excess units x 25 = 450,000 (upper bound), plus lost margin on shortages.
- Guardrails: bias over the last 12 months, share of months outside the agreed band, service level.

**Risks:**
- Taking all the blame, or none. Both lose trust.
- The 450,000 is at most the cost (it holds only if supply ordered to the forecast); quoting it as the actual loss in a heated room overstates it, and shortage costs sit on top.
- Fixing one month by over-correcting, which flips the error to shortages.
- Public blame leaves supply and data science working apart.

**What the interviewer scores:**
- Strong: calm, factual, owns the model's part, defers root cause to a dated review. Weak: defensive, or grovelling with no plan.
- Strong: separates what the model did from how supply used it. Weak: blames supply's ordering.
- Strong: concrete first-hour, first-week and quarter actions. Weak: "I would do a post-mortem."
- Strong: uses the history to say whether it is a pattern. Weak: reacts to a single month.

**Example:** (illustrative) Weak: "That was the approved process, supply ordered what we gave them." Strong: "The forecast was 18% above actual, up to 450,000 of excess. That is on the model. I'll bring the root cause on Friday and a proposal to give you a range and a bias alert, so you are not ordering to one number. Can we also look at how much of the excess was actually bought?"

**Code:**
```python
import numpy as np
fc, act, unit = 118_000, 100_000, 25
excess = fc - act
cost = excess * unit
print("excess units", excess, "cost", cost)
assert excess == 18_000 and cost == 450_000
print("error vs actual", excess / act, "| as share of forecast", round(excess / fc, 4))
assert excess / act == 0.18 and round(excess / fc, 4) == 0.1525
# the 450,000 is an UPPER bound: it assumes every forecast unit was bought and none recovered
for share in (1.0, 0.6, 0.3):
    print(f"if supply bought {share:.0%} of the forecast excess: cost", int(cost * share))
assert int(cost * 0.6) == 270_000
# one month is one data point: compare with invented history of monthly % errors (seeded)
rng = np.random.default_rng(6)
hist = rng.normal(2, 8, 24)                    # model's past errors in % vs actual (illustrative)
base = rng.normal(0, 12, 24)                   # old method's past errors in %
print("model mean error %.1f%%, sd %.1f%%; old method sd %.1f%%" % (hist.mean(), hist.std(ddof=1), base.std(ddof=1)))
z = (18 - hist.mean()) / hist.std(ddof=1)
print("this month's +18%% is %.1f sd from the model's own history" % z)
assert z > 1.5
# asymmetric cost check: with 25 per excess unit and (invented) 40 lost margin per short unit,
# the cost-minimising quantile of demand is 40/(40+25)
q = 40 / (40 + 25)
print("order at demand quantile", round(q, 3))
assert round(q, 3) == 0.615
```

**Output (my run):**
```text
excess units 18000 cost 450000
error vs actual 0.18 | as share of forecast 0.1525
if supply bought 100% of the forecast excess: cost 450000
if supply bought 60% of the forecast excess: cost 270000
if supply bought 30% of the forecast excess: cost 135000
model mean error 4.6%, sd 8.6%; old method sd 11.1%
this month's +18% is 1.6 sd from the model's own history
order at demand quantile 0.615
```

**Follow-ups:**
- What if the root cause is supply ignoring the range? Say so with data in the review, privately first, and fix the process, not the person.
- What if the model was fine and demand was unusual? Show it with the segment breakdown and still add the interval and alert.

**Common mistakes:**
- Defending the model in the meeting.
- Quoting 450,000 without saying it assumes everything was ordered.
- Blaming the approver.
- Promising it will never happen again.

### Q15 ⭐⭐⭐ 🔴 Leadership wants an LLM agent to answer every internal analytics question, and a pilot sample was 94% correct, which at 500,000 monthly questions projects 30,000 wrong answers. A wrong answer costs about 20 in rework or bad decisions, so that projects to 600,000 a month. How do you push back constructively, and where would you accept the risk versus add review?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to AI-era build-versus-buy and hallucination-risk material (2026 vendor and CTO-guide pages such as ThirstySprout and TKMX AI on API versus self-host and LLM cost, an InfoQ LLM-adoption article); no interview page for the leadership-pressure framing was found
**Say this first (1 line):** 94% of 500,000 questions is 30,000 wrong answers, about 600,000 a month at 20 each, so I would not say no to the agent; I would say yes by tier: accept the risk where wrong answers are cheap and add review where they are costly.

**Clarifying questions:**
- How was the 94% measured: on how many questions, who judged "correct", and were they a typical mix? A 94% on easy questions says little about hard ones.
- What does a wrong answer cost in each type of question? A flat 20 hides the few that cost much more.
- What is the human baseline? Analysts also answer wrongly; the fair comparison is the agent against today.
- Can users tell when an answer is wrong, and can they see the query or source? Visible work cuts the damage.
- What does the leadership goal really want: speed, coverage or cost saving? It sets what we can trade.

**Approach:**
1. Do the arithmetic and respect the sample: 500,000 x 6% = 30,000; x 20 = 600,000. If the pilot was a sample (say 500 questions) the 94% could be 91.6% to 95.8%, so monthly wrong answers could be about 21,000 to 42,000. Measure before scaling.
2. Compare with the baseline: what does today's process cost in errors and in wait time? The aim is better than today, not zero error.
3. Segment by stakes. Illustrative split: 350,000 exploratory questions at 4% wrong costing 5 each; 100,000 routine reporting at 6% costing 20; 50,000 decision, finance or external-facing at 20% costing 41. That reproduces 30,000 wrong and 600,000, but 410,000 of the cost sits in 10% of the questions.
4. Accept the risk in the low-stakes tier with visible sources and a "flag wrong" button. Add review (a human, or verified query templates) in the high-stakes tier. In the example, review at 3 each with 80% catch saves 328,000 and costs 150,000, net 178,000 a month (all invented).
5. Pushback script: yes to the vision, here is the pilot extension, the tiers, the metrics, and the date we would widen coverage.
6. Monitor weekly: sampled accuracy by tier, user flags, rework cost, and escalate if any tier crosses its threshold.

**Metrics:**
- Accuracy = correct answers / answers audited, by tier, with a confidence interval.
- Expected monthly error cost = sum over tiers of (questions x error rate x cost per error).
- Review net benefit = (error cost avoided) - (review cost).
- Guardrails: share of answers with a visible source, user-flag rate, time to answer.

**Risks:**
- A single average accuracy hides the dangerous tail.
- Graders may be lenient or model-based; the 94% may be inflated.
- Reviewers rubber-stamp when volume is high, so measure review quality.
- Cost per error is an estimate; the bad cases (a wrong number in a board deck) are not 20.
- The 30,000 and 600,000 are projections from a pilot sample, so they carry the sample's uncertainty and any bias in which questions were piloted.

**What the interviewer scores:**
- Strong: correct arithmetic, then asks how 94% was measured and gives an interval. Weak: accepts or rejects 94%.
- Strong: tiers by stakes with an explicit review economics. Weak: "review everything" or "ship everything".
- Strong: frames it as a yes with controls, tied to the leader's goal. Weak: a flat no.
- Strong: proposes monitoring and a widening gate. Weak: no plan after launch.

**Example:** (illustrative) Weak: "LLMs hallucinate, it is too risky." Strong: "I agree we should do this. 94% means about 30,000 wrong a month, about 600,000, but 410,000 of that sits in the 50,000 decision-critical questions. I propose we let the agent answer everything exploratory with sources, and route the decision-critical tier through verified queries or a quick review. In my estimate that cuts the monthly cost from 600,000 to about 422,000 and I will report the real numbers after four weeks."

**Code:**
```python
import math
vol, acc, cost = 500_000, 0.94, 20
wrong = round(vol * (1 - acc))
print("wrong", wrong, "cost", wrong * cost)
assert wrong == 30_000 and wrong * cost == 600_000
# how sure is 94%? if the pilot sampled 500 questions (invented), Wilson 95% interval
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h
lo, hi = wilson(470, 500)
print("Wilson for 470/500: %.3f - %.3f" % (lo, hi))
print("monthly wrong at those bounds:", round(vol * (1 - hi)), "-", round(vol * (1 - lo)))
assert 0.91 < lo < 0.92 and 0.95 < hi < 0.96
# segments (invented): the average hides where the cost sits
seg = {  # name: (questions, error rate, cost per wrong answer)
    "exploratory": (350_000, 0.04, 5),
    "routine reporting": (100_000, 0.06, 20),
    "decision / finance / external": (50_000, 0.20, 41),
}
tw = tc = 0
for k, (q, e, c) in seg.items():
    w = round(q * e); tw += w; tc += w * c
    print(f"{k:32s} wrong {w:6d} cost {w*c:8d}")
print("total wrong", tw, "total cost", tc)
assert tw == 30_000 and tc == 600_000
# review the high-stakes tier only: 3 per review (invented), catches 80% of its errors (invented)
q, e, c = seg["decision / finance / external"]
review_cost = q * 3
saved = 0.8 * round(q * e) * c
net = saved - review_cost
print("review cost", review_cost, "saved", saved, "net", net, "| residual monthly cost", tc - saved + review_cost)
assert review_cost == 150_000 and saved == 328_000 and net == 178_000
```

**Output (my run):**
```text
wrong 30000 cost 600000
Wilson for 470/500: 0.916 - 0.958
monthly wrong at those bounds: 21174 - 42181
exploratory                      wrong  14000 cost    70000
routine reporting                wrong   6000 cost   120000
decision / finance / external    wrong  10000 cost   410000
total wrong 30000 total cost 600000
review cost 150000 saved 328000.0 net 178000.0 | residual monthly cost 422000.0
```

**Follow-ups:**
- Leadership says review kills the speed benefit. Review only the top tier, and show that exploratory answers stay instant.
- How do you improve accuracy? Use a governed semantic layer or verified metric definitions, and ask for a clarification when the question is ambiguous.

**Common mistakes:**
- Accepting a headline accuracy with no sample size.
- Using one cost per error for all questions.
- Saying no instead of offering a tiered yes.
- Forgetting to compare with human accuracy.

### Q16 ⭐⭐ 🟢 A marketing manager asks you for a churn model, but when you ask what decision it feeds she says she wants to see weekly churn by plan and region. A dashboard would take 2 weeks and a model about 10, five times as long. How do you handle the request, and when would you still build the model?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing
**Say this first (1 line):** She asked for a model but described a dashboard, so I would deliver the weekly churn by plan and region in 2 weeks instead of 10, and build the model once she names a decision and an action it would change.

**Clarifying questions:**
- What will you do differently when you see churn go up in a region? If the answer is "nothing yet", it is a reporting need.
- Is there an intervention (offer, call, price change) and what does it cost per customer? A model only earns money where there is a cost-bearing action to target.
- What does "churn" mean here (cancelled, inactive 30 days, did not renew)? The dashboard needs one agreed definition either way.
- Who will use the output weekly, and who owns the action? No owner, no model.
- Is there a deadline for a decision? It tells me whether the 2-week dashboard unblocks it.

**Approach:**
1. Restate the need: "You want to see where churn is moving each week." That is a dashboard: 2 weeks against 10, five times faster.
2. Agree the churn definition and cut (plan, region); ship the first version in 2 weeks and learn what she looks at.
3. Use it to find the decision. If a segment clearly stands out, a rule may be enough.
4. Build the model when three things hold: an action exists, contacting everyone is too costly or too weak, and a few customers hold most of the churn (targeting has value). Example: blanket offers lose 80,000 a month; a model that finds 40% of churners in the top 10% nets 28,000 (invented).
5. Say what the model costs her: 8 extra weeks, and a team that will not do other work.
6. Write down the trigger that starts the model project, so it is a plan, not a refusal.

**Metrics:**
- Weekly churn rate = customers who churned in week / customers active at start of week, by plan and region.
- For the model case: net value = churners x capture x save rate x value of save - contacts x cost per contact.
- Lift of the top decile = share of churners in the top 10% / 10%.
- Guardrails: dashboard usage (weekly views), time to first answer.

**Risks:**
- Building the model first: 10 weeks on something that feeds no decision.
- A dashboard that nobody opens; fix by asking what she will do with it.
- Churn definition disputes will eat the 2 weeks.
- The model's value is highly sensitive to the save rate (at 5% it loses money in the example).

**What the interviewer scores:**
- Strong: asks about the decision and finds that the need is a dashboard. Weak: builds what was named.
- Strong: gives conditions that justify the model with numbers. Weak: "dashboards are enough" with no condition.
- Strong: keeps the relationship: quick delivery, a path to the model. Weak: lectures her on the difference.
- Strong: notes the 5x effort difference. Weak: ignores cost of delay.

**Example:** (illustrative) Weak: "A model takes 10 weeks, I will start it." Or: "That is not a model request, please re-submit." Strong: "I can give you weekly churn by plan and region in two weeks. Once you see it, if there's an offer you could target at a small group, I will build the model, which takes ten weeks, and in my estimate it nets about 28,000 a month if the offer saves one in five customers. Does that sound right?"

**Code:**
```python
# Q16: dashboard first, model only when a decision needs it (illustrative)
dash_w, model_w = 2, 10
print("model/dashboard effort ratio", model_w / dash_w, "extra weeks", model_w - dash_w)
assert model_w / dash_w == 5
# when would a model pay? invented: 100,000 customers, 3% churn a month, offer costs 2 per contact,
# 20% of churners contacted are saved, a saved customer is worth 200
cust, churn, offer_cost, save_rate, value = 100_000, 0.03, 2, 0.20, 200
churners = cust * churn
# no model: contact everyone
blanket_cost = cust * offer_cost
blanket_gain = churners * save_rate * value
print("blanket: cost", blanket_cost, "gain", blanket_gain, "net", blanket_gain - blanket_cost)
assert (blanket_cost, blanket_gain) == (200_000, 120_000)
# a model whose top 10% holds 40% of churners (lift 4)
top, capture = 0.10, 0.40
m_cost = cust * top * offer_cost
m_gain = churners * capture * save_rate * value
print("model top 10%: cost", m_cost, "gain", m_gain, "net", m_gain - m_cost)
assert (m_cost, m_gain) == (20_000, 48_000)
# the dashboard alone changes nothing unless someone acts on the segment; model net per month 28,000
net = m_gain - m_cost
print("model net per month", net)
assert net == 28_000
# if offer only works at 5% save rate, the model does not pay
m_gain_low = churners * capture * 0.05 * value
print("at 5% save rate: gain", m_gain_low, "net", m_gain_low - m_cost)
assert m_gain_low - m_cost < 0
```

**Output (my run):**
```text
model/dashboard effort ratio 5.0 extra weeks 8
blanket: cost 200000 gain 120000.0 net -80000.0
model top 10%: cost 20000.0 gain 48000.0 net 28000.0
model net per month 28000.0
at 5% save rate: gain 12000.0 net -8000.0
```

**Follow-ups:**
- She still wants the model. Agree the decision and the success measure, then run the dashboard in parallel as the first deliverable.
- When is a rule enough? When one or two segments hold most of the churn and a simple cut is as good as a score.

**Common mistakes:**
- Taking the request at face value.
- Saying no to the model without saying when yes.
- Building a dashboard with no defined churn.
- Ignoring that the value depends on the intervention.

### Q17 ⭐⭐ 🟢 The operations team defends a rule set that catches 60% of 2,000 monthly fraud cases, and your model catches 75% at the same 10% review rate. Each caught case saves 150, so the model catches 300 more cases for 45,000 a month. The ops lead worries about losing control of decisions, so how do you win him over without overselling?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing
**Say this first (1 line):** The model catches 1,500 of 2,000 against 1,200 for the rules, 300 more cases worth 45,000 a month at the same review rate; I would win him over by keeping him in control, not by selling the number.

**Clarifying questions:**
- How are "fraud cases" confirmed, and could the rules have shaped which cases get labelled? Rules-caught cases are more likely to be confirmed, which flatters the rules, but model-only catches may go unlabelled.
- Do the model's 1,500 include most of the rules' 1,200? Overlap decides whether it can replace or only add to the rules.
- What is the review capacity and cost per review? The 10% review rate is fixed; a layered design needs more.
- What worries him: wrong blocks, loss of accountability, or his team's role? The pitch depends on it.
- Who is accountable for a miss: ops or the model owner? It decides who gets override rights.

**Approach:**
1. Do the arithmetic: 60% x 2,000 = 1,200; 75% x 2,000 = 1,500; 300 more at 150 = 45,000.
2. Be honest about what 300 means: it is net. With an invented overlap of 1,000, the model finds 500 the rules miss and misses 200 the rules catch (net 300). Dropping the rules gives away 30,000 a month in cases only they catch.
3. Offer a combined design: model scores, rules remain as a rule layer for known patterns, ops keeps the threshold and an override with a reason code. In the example that union is 1,700 cases (extra 75,000), if review capacity allows.
4. Run in shadow mode for a period, both systems side by side, scoring against confirmed cases. Agree the success measure and the stopping rule beforehand, with him.
5. Give him control levers: he sets review threshold within a band, sees reason codes for each score, can add rules, and gets a weekly report of disagreements.
6. Do not oversell: say the 75% is measured on past cases, will drift, and fraudsters adapt; ask him to help catch the drift.

**Metrics:**
- Recall (fraud caught) = confirmed fraud cases caught / all confirmed fraud cases, at a fixed review rate of 10%.
- Net incremental cases = model-only catches - rules-only catches (500 - 200 = 300 in the example).
- Saving = cases x 150, minus review and false-positive friction costs.
- Guardrails: precision of reviews, customer complaints on false blocks, override rate and its accuracy.

**Risks:**
- The 75% versus 60% is on historical labels; rules may have biased which cases got labelled.
- Fraudsters adapt; the model decays and needs monitoring.
- Selling "45,000" as certain: if the real number is lower he will not trust the next one.
- Taking decisions away: ops becomes passive and stops spotting new patterns.
- Cost of false blocks is missing from the 45,000.

**What the interviewer scores:**
- Strong: correct 300 and 45,000, and shows overlap (net, not gross). Weak: repeats the headline.
- Strong: gives him real control (thresholds, overrides, rules layer, shadow). Weak: "the model is better, trust it."
- Strong: admits limits and plans monitoring. Weak: oversells.
- Strong: asks about label bias. Weak: ignores how fraud is labelled.

**Example:** (illustrative) Weak: "The model is 15 points better, it will save 45,000 a month, you should switch." Strong: "At the same 10% review rate the model catches 300 more cases than the rules on last year's data, worth about 45,000 a month, before false-block costs. It also misses some that your rules catch, about 200 in my estimate, so I want to keep your rules on top. For the first quarter it will run in shadow, you set the threshold, and you can override any score with a reason that we will review together."

**Code:**
```python
import math
cases, rule_rate, model_rate, save = 2000, 0.60, 0.75, 150
rule_c, model_c = round(cases * rule_rate), round(cases * model_rate)
extra = model_c - rule_c
print("rules catch", rule_c, "model catches", model_c, "extra", extra, "saving", extra * save)
assert (rule_c, model_c, extra, extra * save) == (1200, 1500, 300, 45_000)
# the 300 is net: it hides overlap. Invented overlap: 1,000 caught by both
both = 1000
rules_only, model_only = rule_c - both, model_c - both
union = both + rules_only + model_only
print("rules-only", rules_only, "model-only", model_only, "net", model_only - rules_only, "union", union)
assert (rules_only, model_only, union) == (200, 500, 1700)
print("model alone loses", rules_only, "cases rules catch =", rules_only * save, "per month")
print("extra saving if ops keeps rules as a layer on top (needs spare review capacity):", (union - rule_c) * save)
assert (union - rule_c) * save == 75_000
# sampling error on 75% of 2,000 and a paired comparison
lo = model_rate - 1.96 * math.sqrt(model_rate * (1 - model_rate) / cases)
hi = model_rate + 1.96 * math.sqrt(model_rate * (1 - model_rate) / cases)
print("95%% interval on model recall: %.3f - %.3f" % (lo, hi))
# McNemar-style on discordant pairs (200 vs 500)
chi = (model_only - rules_only) ** 2 / (model_only + rules_only)
print("discordant-pair chi-square", round(chi, 1))
assert round(chi, 1) == 128.6
```

**Output (my run):**
```text
rules catch 1200 model catches 1500 extra 300 saving 45000
rules-only 200 model-only 500 net 300 union 1700
model alone loses 200 cases rules catch = 30000 per month
extra saving if ops keeps rules as a layer on top (needs spare review capacity): 75000
95% interval on model recall: 0.731 - 0.769
discordant-pair chi-square 128.6
```

**Follow-ups:**
- He asks what happens when the model is wrong. Overrides are logged and reviewed weekly; a rollback to the rules is one switch.
- Is the difference significant? On these invented discordant counts, 500 against 200 gives a chi-square of 128.6, far beyond noise; real data should be tested the same way.

**Common mistakes:**
- Quoting net gain as if it were all new fraud.
- Dropping the rules.
- Ignoring label bias.
- Treating ops as an obstacle instead of a source of fraud knowledge.

### Q18 ⭐⭐ 🟢 Your launch is in 4 weeks, but the one feature your model needs is owned by a data-engineering team whose backlog is 6 weeks long. A proxy feature gives an AUC of 0.77 against 0.80 with the real feature and 0.74 without either. What do you ask the other team, and which launch plan do you propose?
**Asked at:** Project-conflict prompts (PracHub pages on ML project milestones, scope and conflict, on stakeholder conflict under a compressed delivery timeline and on cross-functional pushback on an analysis; one is tagged to a large marketplace and one to a social platform on the page, unverified); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would launch in week 4 with the proxy feature (AUC 0.77, half of the possible lift) and ask the data-engineering team for a minimal version of the real feature, so we swap it in around week 7 and lose nothing if they slip.

**Clarifying questions to the other team:**
- What is the smallest useful version of the feature, for example a daily batch extract or a table with only our key, rather than the full pipeline? A reduced scope may fit before week 4 or in week 5 to 6.
- What exactly is in the 6-week backlog and what is ahead of us? It shows whether a slot swap or a shared sprint is realistic.
- Is the feature point-in-time correct (what we would have known at scoring time)? A feature that leaks the future gives a false 0.80.
- Can we help (write the SQL, test, document, on-call)? Offering capacity makes the ask easier to grant.
- What is the owner's SLA, schema-change process and quality check once it is live? We need to depend on it safely.

**Approach:**
1. Size the gap. Launch is week 4, the backlog is 6 weeks, so the feature arrives 2 weeks late, and with a week to integrate it is live at week 7.
2. Know what each option is worth: AUC 0.74 (neither), 0.77 (proxy), 0.80 (real). The proxy gives (0.77 - 0.74) / (0.80 - 0.74) = 50% of the available lift.
3. Compare plans over 12 weeks with a stated assumption: weekly value proportional to AUC - 0.5, full model worth 100 a week (invented). Wait for real: 500. Proxy at week 4 then real at week 7: 770. Launch with neither, then real: 740. Proxy adds 30 over launching bare, and 270 over waiting.
4. Propose: launch the proxy version in week 4 behind a feature flag, with monitoring and a written exit plan; log the inputs the real feature would use so the model can be retrained on it as soon as it lands.
5. Ask the other team for a dated, scoped commitment and make the dependency visible to the sponsor, rather than hoping.
6. Define a go/no-go rule: launch only if the proxy model meets the agreed minimum (a guardrail metric, not AUC alone) on a recent holdout.

**Metrics:**
- AUC for each variant on the same recent holdout; the difference with its interval (an AUC of 0.77 on 5,000 positives and 5,000 negatives has a standard error of about 0.005, so 0.77 versus 0.80 is a real gap, but 0.77 versus 0.74 depends on the same sample and pairing).
- Business metric at the decision threshold (precision at the review capacity, or cost saved), because AUC is not money.
- Weeks live x weekly value, as in the 12-week comparison.
- Guardrails: proxy feature coverage and freshness, drift, and the date the real feature lands.

**Risks:**
- The proxy can rely on data that will not exist in production in the same form; check point-in-time availability.
- AUC differences hide differences at the operating threshold.
- The temporary version becomes permanent if no one owns the swap date.
- Pushing the other team could damage a relationship we need again; make a small ask and offer help.
- The value-versus-AUC line is an assumption; if a model at 0.74 is below the business bar, launching bare is not an option.

**What the interviewer scores:**
- Strong: clear numbers on gap (2 weeks, live week 7), half the lift, and a staged plan. Weak: "just wait" or "just ship".
- Strong: specific asks of the other team (minimal scope, date, help, point-in-time). Weak: "escalate to their manager."
- Strong: states the assumptions behind the value comparison. Weak: treats AUC as value.
- Strong: sets a launch guardrail and an owner for the swap. Weak: leaves it open-ended.

**Example:** (illustrative) Weak: "The data team is too slow, let's go with the proxy forever." Strong: "Can you give us a daily extract of just the 3 columns we need by week 5? We'll write and test the SQL and take the on-call for it. We launch week 4 on the proxy at AUC 0.77, which gives half of the improvement, and retrain on your feature the week it lands, expected around week 7."

**Code:**
```python
# Q18: launch plan under a 4-week deadline (illustrative value model)
launch_w, backlog_w, integ_w = 4, 6, 1
auc = {"none": 0.74, "proxy": 0.77, "real": 0.80}
print("gap to real feature:", backlog_w - launch_w, "weeks (+", integ_w, "week to integrate) -> real live at week", backlog_w + integ_w)
assert backlog_w - launch_w == 2
# share of the possible lift (0.74 -> 0.80) the proxy gives
share = (auc["proxy"] - auc["none"]) / (auc["real"] - auc["none"])
print("proxy delivers", round(share, 2), "of the AUC lift")
assert round(share, 2) == 0.50
# assumption: weekly value proportional to (AUC - 0.5); full model worth 100/week (invented)
def v(a): return 100 * (a - 0.5) / (auc["real"] - 0.5)
for k in auc: print(" weekly value", k, round(v(auc[k]), 1))
H = 12   # horizon in weeks
# plan A: wait for real feature, launch week 7
A = (H - (backlog_w + integ_w)) * v(auc["real"])
# plan B: launch proxy week 4, swap in real at week 7
B = (backlog_w + integ_w - launch_w) * v(auc["proxy"]) + (H - (backlog_w + integ_w)) * v(auc["real"])
# plan C: launch week 4 with neither
C = (backlog_w + integ_w - launch_w) * v(auc["none"]) + (H - (backlog_w + integ_w)) * v(auc["real"])
print("12-week value: A wait", round(A), "| B proxy then real", round(B), "| C no feature then real", round(C))
assert round(A) == 500 and round(B) == 770 and round(C) == 740
# AUC differences are noisy: if two AUCs are from 5,000 positives and negatives each, SE about 0.004
import math
n1 = n0 = 5000; a = 0.77
q1, q2 = a / (2 - a), 2 * a * a / (1 + a)
se = math.sqrt((a * (1 - a) + (n1 - 1) * (q1 - a * a) + (n0 - 1) * (q2 - a * a)) / (n1 * n0))
print("approx SE of one AUC at 0.77, 5,000+5,000:", round(se, 4))
assert se < 0.01
```

**Output (my run):**
```text
gap to real feature: 2 weeks (+ 1 week to integrate) -> real live at week 7
proxy delivers 0.5 of the AUC lift
 weekly value none 80.0
 weekly value proxy 90.0
 weekly value real 100.0
12-week value: A wait 500 | B proxy then real 770 | C no feature then real 740
approx SE of one AUC at 0.77, 5,000+5,000: 0.0047
```

**Follow-ups:**
- They refuse a slot. Then the proxy stays, and I log the real feature's would-be inputs from another source so the retrain is quick.
- What if the proxy model is below the quality bar? Delay the launch, or launch to a small share of traffic, and say clearly what the bar is.

**Common mistakes:**
- Treating AUC as business value.
- Asking the other team for the whole feature instead of a minimal version.
- No date or owner for replacing the proxy.
- Not checking whether the proxy leaks information.

### Q19 ⭐⭐ 🟡 An engineering manager says your notebook cannot go to production, and wants to rewrite it before launch. The nightly scoring of 2,000,000 rows takes 5 hours today (400,000 rows an hour) against a 2-hour limit, which needs 1,000,000 rows an hour. How do you handle the disagreement over who does what, and what do you agree before any rewrite starts?
**Asked at:** Productionising prompt pages (several Dataford pages on moving a model from a notebook to production and collaborating with a data engineer, a Martin Fowler article against running notebooks in production, PyData talks on the notebook-to-production friction); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The job needs a 2.5x speedup (400,000 to 1,000,000 rows an hour), so before anyone rewrites anything we profile, agree a written target with a parity test, and split the work by who owns what.

**Clarifying questions:**
- Is 2 hours a hard limit (downstream jobs wait) or a target? It sets how much margin I aim for.
- Does the manager want a rewrite for speed, or for reliability, testing and monitoring? Those are different goals and the fix differs.
- Who will own the job on call after launch? Ownership decides who writes the code.
- Is the launch date fixed? It decides whether I ship a quick fix first and rewrite later.
- Which part of the 5 hours is feature building, model scoring, or I/O? Without a profile, "rewrite" is a guess.

**Approach:**
1. Agree the facts first: 2,000,000 rows in 5 hours is 400,000 rows an hour; 2 hours needs 1,000,000. That is 2.5x.
2. Say the manager is partly right: notebooks are hard to test, schedule and monitor. Do not defend the notebook as such.
3. Profile for one day. Find where the 5 hours go.
4. Use Amdahl's law: if only half the time is in code I can speed up, the best case is 2.5 hours, so a rewrite of that half cannot pass.
5. Agree acceptance criteria in writing before work starts: runtime under 1.6 hours on full data (20% margin), scores match the notebook within a tolerance on a frozen sample, memory cap, failure and retry behaviour.
6. Split ownership: I own model logic, feature definitions and the parity test; engineering owns the pipeline, scheduling, packaging and monitoring. Both sign the interface (input table, output table, schema).
7. Sequence it: quick wins first (vectorise, batch, parallelise, cache features), then the rewrite of whatever is still too slow. Put a review date on it.

**Metrics:**
- Throughput = rows scored / hours of wall-clock time. Target at least 1,000,000 rows an hour, aim for 1,250,000.
- Parity = share of rows where |new score - notebook score| is within tolerance. Target 100%, with the tolerance written down.
- Guardrails: peak memory, failed-run rate, cost of the compute, time to recover after a failure.

**Risks:**
- A rewrite silently changes the model (a different fill value, a different rounding). Scores drift and nobody notices. The parity test is the guard.
- Rewriting without profiling can fix the wrong 30% of the time.
- Two owners means no owner: unclear who gets the page at 3 a.m.
- Launch slips while the argument continues.

**What the interviewer scores:**
- Strong: converts the argument into numbers and a written acceptance test. Weak: "my notebook works, tell them to run it."
- Strong: concedes what the manager gets right (testability, ops) and keeps ownership of model logic. Weak: wins or loses the argument.
- Strong: asks for a profile and uses Amdahl's law. Weak: "rewrite everything in Spark."
- Strong: names the parity check and the on-call owner. Weak: no one says who owns the job after launch.

**Example:** (illustrative numbers) Profile says 70% of the 5 hours is feature building that vectorising can make 10x faster. New runtime = 5 x (0.30 + 0.70/10) = 1.85 hours. That passes 2 hours but not the 1.6-hour margin, so we also parallelise scoring. If the profile had said 50%, the best case is 2.5 hours and a rewrite of that part alone cannot pass. Weak answer: "The notebook is fine, the engineers are overreacting." Strong answer: "You are right that this cannot run as is. We need 2.5x. Give me a day to profile, then let us write down the runtime target and a score-matching test, and I will own the model code while your team owns the pipeline."

**Code:**
```python
rows, hours_now, hours_limit = 2_000_000, 5.0, 2.0
now_rate = rows / hours_now
need_rate = rows / hours_limit
speedup = need_rate / now_rate
print(f"now {now_rate:,.0f} rows/h, need {need_rate:,.0f} rows/h, speedup needed {speedup:.2f}x")
assert now_rate == 400_000 and need_rate == 1_000_000 and abs(speedup - 2.5) < 1e-12
# Amdahl: a share f of the 5 hours is optimisable by factor s (illustrative profile)
def runtime(f, s):
    return hours_now * ((1 - f) + f / s)
print("share f  speedup s  runtime(h)  meets 2h?  meets 1.6h (20% margin)?")
for f, s in [(0.5, 10), (0.7, 10), (0.7, 3), (0.9, 4), (0.9, 100)]:
    t = runtime(f, s)
    print(f"{f:7.0%}  {s:8d}  {t:10.2f}  {str(t <= 2.0):9}  {t <= 1.6}")
assert abs(runtime(0.7, 10) - 1.85) < 1e-9 and runtime(0.7, 10) <= 2.0
assert runtime(0.5, 10) > 2.0          # half the time is untouchable: ceiling is 2.5 h
assert abs(runtime(0.5, 1e9) - 2.5) < 1e-6
# smallest share that must be optimised (10x) to reach 1.6 h
f_need = (1 - 1.6 / hours_now) / (1 - 1 / 10)
print(f"with a 10x fix, at least {f_need:.1%} of runtime must be in the part you fix to hit 1.6 h")
assert abs(f_need - 0.7556) < 1e-3
# parity gate: a rewrite is accepted only if scores match the notebook
import numpy as np
rng = np.random.default_rng(7)
old = rng.random(100_000)
new = old + rng.normal(0, 1e-9, old.shape)      # a faithful rewrite
bad = old.copy(); bad[:500] += 0.2              # a rewrite with a bug in 0.5% of rows
tol = 1e-6
print("faithful rewrite max diff", f"{np.abs(old-new).max():.1e}", "| buggy rewrite rows off:", int((np.abs(old-bad) > tol).sum()))
assert np.abs(old - new).max() < tol and int((np.abs(old - bad) > tol).sum()) == 500
```

**Output (my run):**
```text
now 400,000 rows/h, need 1,000,000 rows/h, speedup needed 2.50x
share f  speedup s  runtime(h)  meets 2h?  meets 1.6h (20% margin)?
    50%        10        2.75  False      False
    70%        10        1.85  True       False
    70%         3        2.67  False      False
    90%         4        1.62  True       False
    90%       100        0.54  True       True
with a 10x fix, at least 75.6% of runtime must be in the part you fix to hit 1.6 h
faithful rewrite max diff 4.5e-09 | buggy rewrite rows off: 500
```

**Follow-ups:**
- The manager insists on a full rewrite anyway. Agree it, but keep the parity test and a date, and ship the optimised notebook step as the fallback.
- What if the profile shows the model itself is the slow part? Then the options are a smaller model, batching, or more hardware, which is a model trade-off for both sides.
- How do you keep the rewrite from drifting later? Share one feature definition, run parity on a sample every release.

**Common mistakes:**
- Arguing for or against notebooks in general.
- Starting a rewrite with no profile and no target.
- Forgetting a margin: 1.99 hours passes today and fails the first time data grows.
- Leaving the owner after launch unnamed.

### Q20 ⭐⭐ 🟡 Your manager must cut the data-science team from 6 people to 4 while requests keep growing. Each person has 10 person-weeks a quarter, 20% of which goes on meetings and support, so capacity falls from 48 to 32 person-weeks against a backlog of 72. How do you make the case for resourcing, and what do you offer to drop or defer?
**Asked at:** Prioritisation and saying-no prompt pages (many Dataford pages on prioritising competing stakeholder requests, a codemia page on saying no to a request, a Towards Data Science stakeholder-management article on declining requests and agreeing a start-now versus later list); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Capacity drops from 48 to 32 person-weeks against a backlog of 72, so we can cover 44% of it; I would show the gap, propose a ranked keep and defer list, and ask the manager to choose the cut openly.

**Clarifying questions:**
- Is 4 people final, or is it negotiable if I show lost value? It tells me whether I am making a case or planning.
- Who decides priorities across requesters (a steering group or the manager)? The defer list needs an owner.
- Which requests have hard deadlines (regulatory, launch)? Those stay regardless of value score.
- Is the 20% meeting and support overhead fixed, or can it be cut? It is a lever worth 2 person-weeks per person.
- How is value measured (revenue, cost saved, risk)? I need one common scale to rank.

**Approach:**
1. Do the arithmetic: 6 people x 10 x 0.8 = 48; 4 x 10 x 0.8 = 32. Backlog 72. Coverage 66.7% before, 44.4% after. Unfunded work grows from 24 to 40 person-weeks.
2. Note the backlog was already not fully covered with 6 people: this is a bigger squeeze, not a new problem.
3. Score every item: person-weeks, value, deadline, risk of not doing it.
4. Rank by value per person-week as a first pass, then override for hard deadlines. Choose the set that fits in 32.
5. Offer three trades: drop low-value work, defer to next quarter, and reduce overhead (support rota, office hours) from 20% to 15%, giving 34 weeks.
6. Show the cost of the cut: value lost, named projects and requesters. Let the manager and stakeholders choose.
7. Agree a review point: if requests still grow, revisit.

**Metrics:**
- Capacity = people x weeks x (1 - overhead). Coverage = capacity / backlog.
- Value per person-week = value score / person-weeks, for ranking only.
- Guardrails: share of capacity on deadline-bound work; number of requesters with nothing delivered.

**Risks:**
- Value scores are opinions; a fixed ranking can be gamed.
- Cutting overhead often means less support, and the work comes back as ad-hoc asks.
- Greedy ranking is not optimal when items are lumpy (see the code, where I use brute force).
- Treating 48 as a number the team can hit with no slack.

**What the interviewer scores:**
- Strong: gets 48, 32, 72, 44% and 40 weeks of gap right. Weak: "we will just work harder."
- Strong: brings a ranked keep and defer list. Weak: only says "we need more people."
- Strong: shows the cost of each cut to the manager in business terms. Weak: argues in terms of team morale only.
- Strong: leaves the final trade to the person who owns priorities. Weak: decides alone, or refuses.

**Example:** (illustrative numbers) Eight items with person-weeks 10, 8, 6, 12, 9, 14, 7, 6 (total 72) and value scores. The best set that fits 32 weeks keeps churn refresh, pricing analysis, fraud rules review and experiment platform fixes, with value 265 of 415 (64%) using 32 weeks, 44% of the work. Deferred: ad-hoc bundle, self-serve dashboard, forecasting model, LLM pilot. Weak answer: "Four people can do the same work if we prioritise." Strong answer: "With four of us we have 32 weeks against 72 asked for. Here are the four projects that give 64% of the value; here are the four I suggest we defer; here is what each deferral costs."

**Code:**
```python
from itertools import combinations
weeks_each, overhead = 10, 0.20
cap6 = 6 * weeks_each * (1 - overhead)
cap4 = 4 * weeks_each * (1 - overhead)
backlog = 72
print(f"capacity 6 people {cap6:.0f}, 4 people {cap4:.0f}, backlog {backlog}")
print(f"coverage: 6 people {cap6/backlog:.1%}, 4 people {cap4/backlog:.1%}; unfunded weeks: {backlog-cap6:.0f} -> {backlog-cap4:.0f}")
assert cap6 == 48 and cap4 == 32 and abs(cap6/backlog - 2/3) < 1e-12 and abs(cap4/backlog - 4/9) < 1e-12
assert backlog - cap6 == 24 and backlog - cap4 == 40
# overhead lever: cutting meetings/support from 20% to 15% with 4 people
cap4_lean = 4 * weeks_each * 0.85
print(f"4 people at 15% overhead: {cap4_lean:.0f} weeks")
assert abs(cap4_lean - 34) < 1e-9
# illustrative backlog: (name, person-weeks, value score) ; weeks sum to 72
items = [("churn model refresh", 10, 90), ("ad-hoc asks (bundle)", 8, 25), ("pricing analysis", 6, 60),
         ("self-serve dashboard", 12, 55), ("fraud rules review", 9, 70), ("new forecasting model", 14, 50),
         ("experiment platform fixes", 7, 45), ("LLM pilot", 6, 20)]
assert sum(w for _, w, _ in items) == 72
best = (0, None)
for r in range(len(items) + 1):
    for c in combinations(items, r):
        w = sum(x[1] for x in c); v = sum(x[2] for x in c)
        if w <= cap4 and v > best[0]:
            best = (v, c)
v4, chosen = best
total_v = sum(v for _, _, v in items)
print(f"best set for 32 weeks: value {v4} of {total_v} ({v4/total_v:.0%}), weeks {sum(x[1] for x in chosen)}")
print("keep :", [n for n, _, _ in chosen])
print("defer:", [n for n, _, _ in items if n not in [c[0] for c in chosen]])
assert sum(x[1] for x in chosen) <= 32
# value per week is only a heuristic; show it
for n, w, v in sorted(items, key=lambda x: -x[2]/x[1]):
    print(f"  {n:28s} {w:3d} wk  value {v:3d}  value/wk {v/w:5.2f}")
```

**Output (my run):**
```text
capacity 6 people 48, 4 people 32, backlog 72
coverage: 6 people 66.7%, 4 people 44.4%; unfunded weeks: 24 -> 40
4 people at 15% overhead: 34 weeks
best set for 32 weeks: value 265 of 415 (64%), weeks 32
keep : ['churn model refresh', 'pricing analysis', 'fraud rules review', 'experiment platform fixes']
defer: ['ad-hoc asks (bundle)', 'self-serve dashboard', 'new forecasting model', 'LLM pilot']
  pricing analysis               6 wk  value  60  value/wk 10.00
  churn model refresh           10 wk  value  90  value/wk  9.00
  fraud rules review             9 wk  value  70  value/wk  7.78
  experiment platform fixes      7 wk  value  45  value/wk  6.43
  self-serve dashboard          12 wk  value  55  value/wk  4.58
  new forecasting model         14 wk  value  50  value/wk  3.57
  LLM pilot                      6 wk  value  20  value/wk  3.33
  ad-hoc asks (bundle)           8 wk  value  25  value/wk  3.12
```

**Follow-ups:**
- The manager says "do all 72 anyway." Quality or deadlines slip; ask which one you may drop and write it down.
- Could automation help? Yes, for repeat asks (a self-serve dashboard), but it costs 12 weeks up front here, so it does not help this quarter.
- What if value scores are disputed? Use a rubric (money, risk, deadline) and have requesters score each other's items.

**Common mistakes:**
- Forgetting the 20% overhead and quoting 40 weeks.
- Giving only a plea for headcount with no numbers.
- Ranking only by value, so big items eat the budget.
- Silently dropping work instead of making the defer list visible.

### Q21 ⭐⭐ 🟡 Product wants to launch an LLM summariser after an evaluation of 400 summaries found 12 with an unsupported claim, a 3% rate. The product lead says that is good enough, and the legal team has not been asked. How do you frame the uncertainty around the 3%, and how do you get a risk decision from the right owner?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to AI-era build-versus-buy and hallucination-risk material (2026 vendor and CTO-guide pages such as ThirstySprout and TKMX AI on API versus self-host and LLM cost, an InfoQ LLM-adoption article); no interview page for the leadership-pressure framing was found
**Say this first (1 line):** 12 of 400 is 3% observed, but with 95% confidence the true rate could be anywhere from about 1.7% to 5.2%, and whether that is acceptable is a risk decision for legal and the product owner, not something I or the product lead can wave through.

**Clarifying questions:**
- What counts as an "unsupported claim", and how severe are they (a wrong date versus a wrong medical or financial statement)? Severity matters more than rate.
- How were the 400 chosen (random, or easy documents)? A biased sample makes the 3% meaningless.
- Who reads the summary and what do they do with it? A summary that triggers a decision carries more risk.
- What is the volume per month? It turns a rate into a count of bad summaries.
- Is there a human review, citation display or disclaimer in the product? Mitigations change the acceptable rate.

**Approach:**
1. State the point estimate: 12 / 400 = 3.0%.
2. Give the uncertainty: Wilson 95% interval 1.72% to 5.17% (the exact method gives 1.56% to 5.18%).
3. Turn it into counts: at an illustrative 100,000 summaries a month, about 3,000 bad, plausible range 1,700 to 5,200.
4. Say what the sample cannot show: it cannot prove the rate is under 4%. About 1,440 summaries would be needed if the true rate is 3%.
5. Break it down by severity and by document type; a 3% mix of trivial and harmful errors is not one number.
6. Name the decision owner: product owns the benefit, legal and risk own the exposure. Write a one-page memo with rate, interval, example failures, mitigations and a clear ask: approve, approve with conditions, or decline.
7. Offer conditions: citations next to claims, human review for high-risk content, a monitored sample each week, a rollback trigger.

**Metrics:**
- Unsupported-claim rate = summaries with at least one unsupported claim / summaries evaluated. Define per summary, and also per claim.
- Wilson 95% interval for that proportion.
- Guardrails: severity-weighted error rate, user complaint rate, share of summaries reviewed by a human.

**Risks:**
- "3%" sounds small and anchors the room; 3,000 bad summaries a month may not.
- Labelers disagree on what is supported; agreement should be measured.
- The evaluation set differs from live traffic.
- Launching with legal unaware creates a trust problem later even if nothing breaks.

**What the interviewer scores:**
- Strong: gives an interval and converts it into counts. Weak: quotes 3% as a fact.
- Strong: routes the decision to the owner with a written ask. Weak: either agrees with the lead or blocks alone.
- Strong: separates severity from rate. Weak: treats all errors alike.
- Strong: proposes conditions and a rollback trigger. Weak: a flat yes or no.

**Example:** (illustrative numbers) 12 of 400, interval 1.72% to 5.17%. Weak answer: "3% is low, good enough." Or: "No, I do not trust it." Strong answer: "The observed rate is 3%, and it could plausibly be 1.7% to 5.2%. At our volume that is roughly 1,700 to 5,200 bad summaries a month. I cannot say if that is acceptable, legal can. Here is a one-page memo; I suggest launch with citations and weekly sampling."

**Code:**
```python
import math
from scipy import stats
k, n = 12, 400
p = k / n
z = 1.959963984540054
den = 1 + z*z/n
centre = (p + z*z/(2*n)) / den
half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / den
lo, hi = centre - half, centre + half
cp_lo = stats.beta.ppf(0.025, k, n-k+1); cp_hi = stats.beta.ppf(0.975, k+1, n-k)
print(f"observed {p:.1%}; Wilson 95% {lo:.2%} to {hi:.2%}; exact (Clopper-Pearson) {cp_lo:.2%} to {cp_hi:.2%}")
assert abs(p - 0.03) < 1e-12 and 0.016 < lo < 0.018 and 0.051 < hi < 0.053
# what the interval means at an illustrative volume of 100,000 summaries a month
vol = 100_000
print(f"at {vol:,} summaries a month: expected {p*vol:,.0f} bad, plausible range {lo*vol:,.0f} to {hi*vol:,.0f}")
assert round(p*vol) == 3000
# can this sample prove the rate is under a 4% ceiling? upper bound 5.2% says no
print("upper bound under 4%?", hi < 0.04)
assert not (hi < 0.04)
# sample size so a 3% observed rate has a Wilson upper bound under 4%
def upper(k, n):
    pp = k/n; d = 1 + z*z/n
    return (pp + z*z/(2*n))/d + z*math.sqrt(pp*(1-pp)/n + z*z/(4*n*n))/d
nn = 400
while upper(round(0.03*nn), nn) >= 0.04: nn += 10
print(f"if the true rate stays 3%, about {nn} summaries are needed for an upper bound below 4%")
assert upper(round(0.03*nn), nn) < 0.04 and nn > 1000
```

**Output (my run):**
```text
observed 3.0%; Wilson 95% 1.72% to 5.17%; exact (Clopper-Pearson) 1.56% to 5.18%
at 100,000 summaries a month: expected 3,000 bad, plausible range 1,724 to 5,170
upper bound under 4%? False
if the true rate stays 3%, about 1440 summaries are needed for an upper bound below 4%
```

**Follow-ups:**
- Would more samples shrink the interval? Yes, roughly with the square root of n; 4x the sample halves the width.
- What if they only agree to launch for low-risk content? Good; define low-risk in writing and route the rest to review.
- Is zero errors achievable? Not by evaluation: even 0 of 400 leaves an Wilson upper bound of about 0.95% (the rule of three gives 3 / 400 = 0.75%).

**Common mistakes:**
- Treating the observed rate as the true rate.
- Using the normal approximation at small counts without noting it.
- Letting the person who wants the launch decide the risk.
- Counting errors but not their severity.

### Q22 ⭐⭐ 🟡 The platform team wants to self-host an open model, and you favour a vendor API for a feature that uses 3,000 million tokens a month. The API costs 0.60 per million tokens (1,800 a month) and self-hosting costs about 6,000 a month in fixed infrastructure. Compute the break-even volume, and say what other factors you would put in front of both sides.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to AI-era build-versus-buy and hallucination-risk material (2026 vendor and CTO-guide pages such as ThirstySprout and TKMX AI on API versus self-host and LLM cost, an InfoQ LLM-adoption article); no interview page for the leadership-pressure framing was found
**Say this first (1 line):** Break-even is 10,000 million tokens a month, 3.3 times today's 3,000, so on cost alone the API is cheaper now by 4,200 a month; but I would put cost, quality, latency, data rules and people cost in front of both sides before deciding.

**Clarifying questions:**
- Does the 6,000 include engineers to run it, on-call, and spare capacity for peaks? Hidden people cost is the usual gap.
- How fast will volume grow, and is it spiky? Fixed capacity must cover peaks.
- Are there data-residency or confidentiality rules that rule out sending text to a vendor? That can decide it outright.
- Does the open model meet the quality bar on our own evaluation set? Cost is irrelevant if it does not.
- Is the API price per million tokens one rate, or different for input and output? The blend changes break-even.

**Approach:**
1. Compute the API bill: 3,000 x 0.60 = 1,800 a month.
2. Break-even volume = fixed cost / price = 6,000 / 0.60 = 10,000 million tokens.
3. Compare to today: 3.33x. At 10% monthly growth we reach it in about 13 months.
4. Show sensitivity: if API price halves to 0.30, break-even doubles to 20,000. If the true self-host cost is 9,000 or 12,000 it is 15,000 or 20,000.
5. List non-cost factors: quality on our task, latency, uptime and rate limits, data control, vendor lock-in and price changes, team time and skill, speed of switching later.
6. Propose a cheap, reversible path: start with the API behind a thin interface so we can swap models; run a self-host pilot on a small share to measure real cost and quality; set a trigger (e.g., sustained volume above 70% of break-even) to revisit.
7. Frame it as a joint decision with the platform team, not me against them.

**Metrics:**
- Monthly cost = price per million tokens x millions of tokens (API) versus fixed cost (self-host).
- Break-even volume = fixed monthly cost / API price per million.
- Guardrails: task quality score on our eval set, p95 latency, error and rate-limit rate, engineer-hours per month.

**Risks:**
- The 6,000 is probably an underestimate once staff time is included.
- API prices have fallen over time; a trend reverses break-even assumptions (illustrative).
- Self-host utilisation is rarely 100%; idle capacity wastes the fixed cost.
- Locking into one vendor makes later switching costly.

**What the interviewer scores:**
- Strong: gets 1,800 and 10,000 and says 3.3x today. Weak: arithmetic error or no break-even.
- Strong: names non-cost factors and the hidden people cost. Weak: only compares the two bills.
- Strong: proposes a reversible, measurable path with a trigger. Weak: a permanent winner declared.
- Strong: treats the platform team as a partner. Weak: frames it as winning an argument.

**Example:** (illustrative numbers) API 1,800 a month versus 6,000 self-host; over 12 months at 10% growth the API totals about 38,500 versus 72,000. Weak answer: "API is cheaper, case closed." Strong answer: "On today's volume the API is cheaper by 4,200 a month, and break-even is 10,000 million tokens, more than three times today. I would still run a small self-host pilot and fix a trigger to revisit, because quality, data rules and growth could change the answer."

**Code:**
```python
import math
api_per_m, fixed = 0.60, 6000.0
volume = 3000.0                       # million tokens a month
api_now = api_per_m * volume
be = fixed / api_per_m
print(f"API bill now {api_now:,.0f}; self-host fixed {fixed:,.0f}; break-even {be:,.0f} million tokens a month ({be/volume:.2f}x today)")
assert abs(api_now - 1800) < 1e-9 and abs(be - 10000) < 1e-9
print(f"at today's volume the API is cheaper by {fixed - api_now:,.0f} a month")
assert fixed - api_now == 4200
# sensitivity of break-even to API price and to the self-host bill (illustrative scenarios)
for price, fx in [(0.60, 6000), (0.30, 6000), (0.60, 9000), (0.60, 12000)]:
    print(f"  price {price:.2f}, self-host {fx:,}: break-even {fx/price:,.0f}M tokens")
assert 6000/0.30 == 20000 and abs(9000/0.60 - 15000) < 1e-9
# how long to grow into break-even at an illustrative 10% monthly growth
months = math.log(be/volume) / math.log(1.10)
print(f"months to reach break-even at 10% monthly growth: {months:.1f} -> {math.ceil(months)}")
assert math.ceil(months) == 13
# cumulative cost over 12 months at 10% growth
api_tot = sum(api_per_m*volume*1.1**m for m in range(12)); self_tot = fixed*12
print(f"12-month totals at 10% growth: API {api_tot:,.0f} vs self-host {self_tot:,.0f}")
assert api_tot < self_tot
```

**Output (my run):**
```text
API bill now 1,800; self-host fixed 6,000; break-even 10,000 million tokens a month (3.33x today)
at today's volume the API is cheaper by 4,200 a month
  price 0.60, self-host 6,000: break-even 10,000M tokens
  price 0.30, self-host 6,000: break-even 20,000M tokens
  price 0.60, self-host 9,000: break-even 15,000M tokens
  price 0.60, self-host 12,000: break-even 20,000M tokens
months to reach break-even at 10% monthly growth: 12.6 -> 13
12-month totals at 10% growth: API 38,492 vs self-host 72,000
```

**Follow-ups:**
- What if volume doubles every quarter? Then we reach break-even in under a year; plan the pilot now.
- What if input and output tokens are priced differently? Use the blended price from the real traffic mix.
- Would a smaller vendor model change it? Possibly; re-run the quality test, since a cheaper model shifts the break-even.

**Common mistakes:**
- Forgetting staff and on-call cost in the self-host number.
- Comparing at today's volume only.
- Mixing "million" and "billion" tokens.
- Deciding on cost without a quality test on our own data.

### Q23 ⭐⭐ 🟡 A junior analyst sends you an LLM-written summary saying revenue rose 12%, from 1,000,000 to 1,120,000, and the team is excited. Active users also rose 12%, from 50,000 to 56,000. Review the claim, and explain how you give feedback on the process rather than just the number.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to AI-era build-versus-buy and hallucination-risk material (2026 vendor and CTO-guide pages such as ThirstySprout and TKMX AI on API versus self-host and LLM cost, an InfoQ LLM-adoption article); no interview page for the leadership-pressure framing was found
**Say this first (1 line):** The arithmetic is right, revenue and users both rose 12%, but that means revenue per user stayed flat at 20.00, so the growth came entirely from more users, not better monetisation; and I would check the numbers against the source, not the summary.

**Clarifying questions:**
- Which query or table produced 1,000,000 and 1,120,000, and what period? I want to recompute them myself.
- How are "active users" and "revenue" defined (gross or net, refunds, time zone)? Definitions can move both numbers.
- Is this month versus last month, or year over year? Seasonality changes the story.
- Did the LLM see the data, or was it given the numbers typed in by hand? A model can mis-copy figures.

**Approach:**
1. Recompute: 1,120,000 / 1,000,000 = +12.0%; 56,000 / 50,000 = +12.0%.
2. Decompose: revenue per user is 20.00 in both periods. Change of 120,000 = 6,000 extra users x 20.00 = 120,000 from users, 0 from price or mix.
3. Say what the headline does not show: it hides segment mix. Totals can move the same while new users spend less and old users spend more (illustrative: 1,112,000 from a different mix).
4. Check the source: rerun the query, compare to the dashboard, look at the trend and not just two points.
5. Give process feedback in private, kindly: ask them to paste the query, to list definitions, to recompute numbers independently of the LLM, and to add "what could make this wrong".
6. Praise what was good (it is correct, it is clear) so the feedback is about method.
7. Offer a short checklist for LLM-assisted analysis: every number traced to a query, one sentence on what is not known, a second person checks the top claim.

**Metrics:**
- Growth % = new / old - 1 for revenue and users.
- Revenue per active user = revenue / active users.
- Decomposition: users effect = change in users x old revenue per user; per-user effect = change in revenue per user x new users.
- Guardrails: retention, refunds, share of revenue from new users.

**Risks:**
- The LLM can be fluent and wrong; a correct sentence this time proves nothing about next time.
- Same percentage growth is read as "healthy" while revenue per user is flat.
- Public feedback in front of an excited team can make a junior stop sharing.

**What the interviewer scores:**
- Strong: spots that revenue per user is flat and decomposes it. Weak: confirms "12% is right" and stops.
- Strong: checks the source and definitions. Weak: trusts the LLM text.
- Strong: gives feedback on the process with a checklist. Weak: only corrects the number or criticises the tool.
- Strong: handles the junior with care. Weak: embarrasses them or ignores it.

**Example:** (illustrative numbers) Revenue 1,000,000 to 1,120,000 and users 50,000 to 56,000. Revenue per user 20.00 to 20.00. Weak answer: "Looks right, great, send it." Strong answer: "The numbers recompute, nice. One thing to add: revenue per user did not move, so it is all user growth. Can you paste the query, and next time add one line on what this does not show?"

**Code:**
```python
rev0, rev1 = 1_000_000, 1_120_000
u0, u1 = 50_000, 56_000
g_rev, g_u = rev1/rev0 - 1, u1/u0 - 1
a0, a1 = rev0/u0, rev1/u1
print(f"revenue {g_rev:+.1%}, users {g_u:+.1%}, revenue per user {a0:.2f} -> {a1:.2f} ({a1/a0-1:+.1%})")
assert abs(g_rev - 0.12) < 1e-12 and abs(g_u - 0.12) < 1e-12 and a0 == a1 == 20.0
# decomposition: revenue change = users effect (at old ARPU) + ARPU effect (on new users)
users_effect = (u1 - u0) * a0
arpu_effect = (a1 - a0) * u1
print(f"change {rev1-rev0:,}: from more users {users_effect:,.0f}, from higher revenue per user {arpu_effect:,.0f}")
assert users_effect + arpu_effect == rev1 - rev0 == 120_000 and arpu_effect == 0
# what if rounding hid a mix change? same totals can hide two segments moving opposite ways (illustrative)
seg0 = {"old users": (40_000, 22.0), "new users": (10_000, 12.0)}
seg1 = {"old users": (40_000, 22.0), "new users": (16_000, 14.5)}
r0 = sum(u*a for u, a in seg0.values()); r1 = sum(u*a for u, a in seg1.values())
print(f"segment illustration: revenue {r0:,.0f} -> {r1:,.0f} ({r1/r0-1:+.1%}), users {50000} -> {56000}")
assert r0 == 1_000_000 and r1 == 1_112_000
```

**Output (my run):**
```text
revenue +12.0%, users +12.0%, revenue per user 20.00 -> 20.00 (+0.0%)
change 120,000: from more users 120,000, from higher revenue per user 0
segment illustration: revenue 1,000,000 -> 1,112,000 (+11.2%), users 50000 -> 56000
```

**Follow-ups:**
- Should we ban LLM summaries? No; allow them with a rule that every number links to a query.
- What if the user growth is mostly low-value users? Break down revenue per user by cohort before celebrating.
- How do you review faster? A template with query link, definitions, and a "not shown" line.

**Common mistakes:**
- Checking the percentage but not the base numbers.
- Reading "both +12%" as proof of healthy monetisation.
- Giving feedback in a group channel.
- Blaming the tool instead of fixing the process.

### Q24 ⭐⭐ 🟡 A compliance officer asks you to show why the credit model declined a specific applicant, but she distrusts SHAP because two retrains gave different top reasons for the same person. The model has 40 features and some are strongly correlated. How do you explain what the reasons mean, and what do you change to make them more stable?
**Asked at:** Explainability material (hirevire explainability pre-screening questions, fluxforce and other compliance-oriented pages on SHAP for regulators and model-risk guidance, a SHAP error-review workflow page); mostly vendor and practitioner pages rather than interview banks; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** SHAP reasons are only stable if the model is; with correlated features the credit is shared arbitrarily among near-duplicates, so I would explain reasons at the level of feature groups and stabilise the model, not claim a single feature is "the" reason.

**Clarifying questions:**
- What kind of model is it (linear, trees, neural net)? It changes how the explanation is computed.
- Which features are strongly correlated (income and credit limit, for example)? Those are the ones that swap places.
- What does the regulator or policy require: top reasons, adverse-action codes, or a full explanation? That defines the deliverable.
- What baseline does the SHAP use? A different background population gives different values.
- Do retrains use a fixed seed and the same data window? Part of the instability may be avoidable noise.

**Approach:**
1. Explain what a SHAP value means: a share of the gap between this applicant's score and the average score, given a baseline and a model. It is not a causal statement.
2. Explain the instability: when two features carry the same signal, a retrain can put the weight on either. The model prediction barely changes, but the reasons do.
3. Reproduce it: retrain on bootstrap samples and count how often the top reason changes for the same applicant.
4. Group correlated features (income-related, delinquency-related) and report reasons per group; sum SHAP within each group.
5. Make the model more stable: remove or combine near-duplicate features, constrain or regularise, fix seeds and data windows, and average SHAP over several retrains or bootstrap models.
6. Add a stability test to model validation: top-reason agreement across retrains with a threshold (for example, 90% for the top group).
7. Give the compliance officer a short document: what the reasons mean, what they do not mean, and the stability results.

**Metrics:**
- Top-reason agreement = retrains where the applicant's top reason equals the most common top reason / retrains.
- Number of distinct top reasons across retrains.
- Guardrails: AUC (or KS) stays within tolerance after grouping and pruning; share of applicants with a stable top reason.

**Risks:**
- Presenting a SHAP number as the cause of the decline.
- Pruning features to look stable can cost accuracy; check it.
- Group labels chosen after seeing the results invite bias; define groups from correlation clusters in advance.
- The baseline choice changes SHAP; document it.

**What the interviewer scores:**
- Strong: names correlation as the cause and shows it with a repeat-retrain test. Weak: "SHAP is the industry standard, trust it."
- Strong: offers group-level reasons and stability thresholds. Weak: only says "use a simpler model."
- Strong: explains meaning and limits in plain words for compliance. Weak: jargon.
- Strong: takes the officer's distrust as a valid finding. Weak: defends the tool.

**Example:** (illustrative simulation) 40 features in 10 groups of 4, within-group correlation about 0.9, 40 bootstrap retrains of a logistic model, one fixed applicant. Single-feature top reasons: 5 different features across retrains, the most common in 52% of retrains. At group level: 1 group in 100% of retrains. Weak answer: "The top reason is feature 6." Strong answer: "The decline is driven by the delinquency group; within that group the features are near-duplicates, so which one ranks first changes between retrains. We report the group."

**Code:**
```python
import numpy as np
rng = np.random.default_rng(24)
G, per, n = 10, 4, 3000                     # 10 groups of 4 correlated features = 40 features
def make(m):
    f = rng.normal(size=(m, G))
    X = np.repeat(f, per, axis=1) * np.sqrt(0.9) + rng.normal(size=(m, G*per)) * np.sqrt(0.1)  # within-group corr 0.9
    return X, f
beta_g = np.array([1.0, -0.8, 0.6, 0.5, -0.4, 0.3, 0.2, 0.1, 0.1, 0.05])
X, f = make(n)
y = (rng.random(n) < 1/(1+np.exp(-(f@beta_g - 0.5)))).astype(float)
def fit(X, y, lam=1e-3):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1])
    for _ in range(25):
        p = 1/(1+np.exp(-Xb@w)); g = Xb.T@(p-y) + lam*np.r_[0, w[1:]]
        H = (Xb.T*(p*(1-p)))@Xb + lam*np.diag(np.r_[0, np.ones(len(w)-1)])
        w = w - np.linalg.solve(H, g)
    return w[1:]
x_app = np.zeros(G*per); x_app[:] = np.repeat(np.array([0.2, 1.5, 0.3, -0.3, 0.9, 0.4, -0.2, 0.3, 0.1, 0.0]), per) # one applicant
retrains, top1, topg = 40, [], []
for r in range(retrains):
    idx = rng.integers(0, n, n)
    w = fit(X[idx], y[idx])
    mu = X[idx].mean(0)
    shap = w * (x_app - mu)              # exact SHAP in log-odds for a linear model with independent-feature baseline
    top1.append(int(np.argmax(-shap)))   # biggest push toward decline (lowest score)
    topg.append(int(np.argmax(-shap.reshape(G, per).sum(1))))
def modal_share(v): return max(np.bincount(v)) / len(v)
print(f"distinct top reasons across {retrains} retrains: single features {len(set(top1))}, groups {len(set(topg))}")
print(f"most common top reason appears in: single feature {modal_share(top1):.0%} of retrains, group {modal_share(topg):.0%}")
assert len(set(top1)) > len(set(topg))
assert modal_share(topg) > modal_share(top1)
```

**Output (my run):**
```text
distinct top reasons across 40 retrains: single features 5, groups 1
most common top reason appears in: single feature 52% of retrains, group 100%
```

**Follow-ups:**
- Why not just drop correlated features? You can, but you may lose signal and need to re-validate; grouping costs nothing in accuracy.
- Does this apply to tree models? Yes; trees pick one of two correlated features at each split, so reasons shift between retrains.
- Is SHAP wrong then? No, it answers a model question; the instability is in the model's use of redundant features. This simulation uses a linear model, where SHAP is exact, so the effect is not an artefact of approximation.

**Common mistakes:**
- Treating feature contribution as causal ("if she earned more she would be approved").
- Not fixing the baseline.
- Comparing one retrain to another without a stability metric.
- Hiding instability from compliance.

### Q25 ⭐⭐ 🟡 The CEO asks why the churn model's precision is only 30 percent. It flags 1,000 customers, 300 of whom really churn, out of 100,000 customers with a 5% churn rate (5,000 churners), so recall is 6%. How do you explain these numbers to him, and what do you recommend he use them for?
**Asked at:** Metric-definition and persuasion prompt pages (a 2026 data-analyst hiring guide naming a defended metric definition as a standard question, Yardstick persuasion and courage question pages for data scientists, Dataford pages on stakeholders disputing your findings); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Of 1,000 customers we flag, 300 churn, that is 30% precision against a 5% base rate, so the list is 6 times better than random; recall is 6% because we only contact 1,000 of 5,000 churners, and the right question is whether the offer pays at that precision.

**Clarifying questions:**
- What action follows a flag (call, discount, nothing)? The cost per contact sets the useful precision.
- What is a retained customer worth, and how often does the offer actually save one? Needed for break-even.
- Why 1,000 flagged: a capacity limit, or a threshold? It explains the low recall.
- Churn is defined over what window? "5% churn" means little without it.

**Approach:**
1. Say the definitions in one sentence each. Precision: of those we flag, how many really churn: 300 / 1,000 = 30%. Recall: of all who churn, how many we flag: 300 / 5,000 = 6%.
2. Give the baseline: 5% of customers churn, so picking at random gives 50 per 1,000. We find 300. That is 6x lift.
3. Explain why recall is low: we chose to flag only 1,000. Even a perfect list of 1,000 would give 20% recall.
4. Move from accuracy to money: with an illustrative cost of 5 per contact, 20% save rate and 100 value per saved customer, break-even precision is 5 / (0.2 x 100) = 25%. We are at 30%, so net +1,000; random would lose 4,000.
5. Recommend use: target the retention offer to the top-scored list, not a mass campaign; widen the list only while marginal precision stays above break-even.
6. Recommend measuring with a holdout: leave some flagged customers untreated to measure the real save rate.
7. Do not call the model "wrong": 30% precision is expected when the base rate is 5%.

**Metrics:**
- Precision = true churners among flagged / flagged = 300 / 1,000.
- Recall = true churners among flagged / all churners = 300 / 5,000.
- Lift = precision / base rate = 0.30 / 0.05.
- Net value = churners flagged x save rate x value - flagged x cost per contact.
- Guardrail: offer cost per customer, complaint rate, holdout save rate.

**Risks:**
- A CEO may hear "30%" and think "wrong 70% of the time". The 70% still costs only the contact fee.
- The save rate (20% here) is an assumption; if it is 10%, break-even precision becomes 50% and the plan loses money.
- Churn that the model flags may be customers who would stay anyway; only a holdout shows the effect.

**What the interviewer scores:**
- Strong: explains precision, recall, and lift in plain words and gets 30%, 6%, 6x. Weak: apologises for 30%.
- Strong: links precision to break-even economics. Weak: stays on metrics only.
- Strong: proposes a holdout to measure causal benefit. Weak: assumes flagged equals saved.
- Strong: short, calm, CEO language. Weak: formulas and jargon.

**Example:** (illustrative numbers) 100,000 customers, 5,000 churners, 1,000 flagged, 300 churn. Weak answer: "Precision is low, we need a better model." Strong answer: "Out of 1,000 we call, 300 would have left, that is six times better than picking at random. We call only 1,000, so we reach 6% of leavers. At our offer cost, anything above 25% precision pays, so I recommend we use it for targeted offers and test with a holdout."

**Code:**
```python
cust, churners, flagged, tp = 100_000, 5_000, 1_000, 300
base = churners / cust
prec, rec = tp / flagged, tp / churners
lift = prec / base
print(f"base rate {base:.1%}, precision {prec:.0%}, recall {rec:.0%}, lift {lift:.1f}x")
assert base == 0.05 and prec == 0.30 and abs(rec - 0.06) < 1e-12 and abs(lift - 6) < 1e-9
# random pick of 1,000 customers would catch
rand_tp = flagged * base
print(f"a random 1,000 would contain {rand_tp:.0f} churners; the model finds {tp}")
assert rand_tp == 50
# illustrative economics: offer costs 5, saves 20% of churners reached, a saved customer is worth 100
cost, save, value = 5.0, 0.20, 100.0
be_prec = cost / (save * value)
net_model = tp*save*value - flagged*cost
net_rand = rand_tp*save*value - flagged*cost
print(f"break-even precision {be_prec:.0%}; net value: model {net_model:,.0f}, random {net_rand:,.0f}")
assert abs(be_prec - 0.25) < 1e-12 and net_model == 1000 and net_rand == -4000
# recall is capped by capacity: even a perfect list of 1,000 would reach 1,000/5,000
print(f"max recall with 1,000 contacts: {flagged/churners:.0%}")
assert flagged/churners == 0.20
```

**Output (my run):**
```text
base rate 5.0%, precision 30%, recall 6%, lift 6.0x
a random 1,000 would contain 50 churners; the model finds 300
break-even precision 25%; net value: model 1,000, random -4,000
max recall with 1,000 contacts: 20%
```

**Follow-ups:**
- How do we raise recall? Flag more customers; precision falls, so check the marginal break-even.
- Is the prompt's 6% recall correct? Yes: 300 / 5,000 = 6%.
- Should we use AUC with him? Not first; money and lift are easier to explain.

**Common mistakes:**
- Mixing up precision and recall.
- Judging precision without the base rate.
- Ignoring the cost per contact.
- Claiming the 300 were "saved".

### Q26 ⭐⭐ 🟡 A PM has used three churn target definitions in one 20-day sprint, 30, then 60, then 90 days of inactivity, and each relabel-and-retrain costs you 3 days. The 9 days are 45% of the sprint (6 days, 30%, if the first build was planned work). What do you do about it, and how do you stop it happening again?
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would show the PM that each definition change costs 3 days of a 20-day sprint, ask for one churn definition agreed in writing with the decision owner, and make my pipeline cheap to relabel so a later change does not cost days.

**Clarifying questions:**
- What decision will the model drive, and over what time window does the business act? The definition should follow the action, not taste.
- Who owns the definition, the PM or a business lead? One named owner prevents repeats.
- Is 30 versus 90 days a real disagreement among stakeholders, or exploration? It tells me whether to mediate or to just parametrise.
- Is the sprint end date fixed? It decides what I trade off.

**Approach:**
1. Do the arithmetic: 3 relabel-and-retrain cycles x 3 days = 9 days = 45% of 20.
2. Split the cost honestly: three definitions, each cycle 3 days. If the first build was planned work, the avoidable loss is 6 days (30%); the full 9 days (45%) is the total spent.
3. Do not blame the PM: show the cost privately, then a one-slide compare of 30, 60, 90 on the same data: churn rate, share who return later, and what each means for the intervention.
4. Propose a decision rule: pick the window that matches how long the retention action takes to work, or where reactivation drops off.
5. Make labels parametric: one pass builds the inactivity gap, and labels for 30, 60 and 90 are columns. A new definition then costs about half a day, not 3 (illustrative).
6. Set change control: a definition change after sprint planning needs the owner's sign-off and shows its cost; otherwise it waits for the next sprint.
7. Record the definition in a one-page spec with a version number.

**Metrics:**
- Sprint days lost = number of cycles x days per cycle; share = lost days / sprint days.
- Churn rate by definition = customers with inactivity at least d days / customers.
- Guardrail: time to relabel and retrain, number of definition versions per sprint.

**Risks:**
- Hiding the cost leaves the PM unaware that it hurts.
- Saying no outright makes the PM an opponent; they may be reacting to executives.
- Locking a definition too early may lock a poor one; keep the version history.

**What the interviewer scores:**
- Strong: quantifies the cost and separates total from avoidable days. Weak: complains the PM is indecisive.
- Strong: fixes the process (single owner, spec, change control, parametric labels). Weak: just absorbs the changes.
- Strong: gives the PM a data comparison to decide with. Weak: argues from preference.
- Strong: calm, collaborative tone. Weak: escalates immediately.

**Example:** (illustrative numbers) A simulated gap table gives churn rates of 42.0% at 30 days, 18.6% at 60 and 9.7% at 90, so the three definitions are three different targets, not tweaks. Weak answer: "I keep changing the label whenever you ask." Strong answer: "Each definition costs me 3 days; the three cycles are 9 days, 45% of the sprint, and 6 days (30%) of that was avoidable. Here is how 30, 60 and 90 compare. Can we pick one by Friday and write it down? I will also make the label a parameter so a later change takes half a day."

**Code:**
```python
import numpy as np
sprint, per_change, changes = 20, 3, 3
lost = per_change * changes
print(f"total: {changes} relabel-and-retrain cycles x {per_change} days = {lost} days = {lost/sprint:.0%} of {sprint}")
assert lost == 9 and lost/sprint == 0.45
# three definitions; if the first build was planned work anyway, only two cycles are avoidable
avoidable = per_change * 2
print(f"if the first definition was planned work, avoidable loss = {avoidable} days = {avoidable/sprint:.0%}")
assert avoidable == 6 and avoidable/sprint == 0.30
# build once, label many: one pass over a gap table gives all three labels (illustrative simulation)
rng = np.random.default_rng(26)
gap = rng.lognormal(mean=3.2, sigma=1.0, size=100_000)   # days of inactivity at snapshot, illustrative
rates = {d: float((gap >= d).mean()) for d in (30, 60, 90)}
print({d: f"{r:.1%}" for d, r in rates.items()})
assert rates[30] > rates[60] > rates[90]
# change control: each extra definition requested after the sprint plan costs 3 days; a parametrised label costs 0.5 day
param_cost = 0.5
print(f"three definitions with a parametrised label: {3*param_cost} days instead of {lost}")
assert 3*param_cost == 1.5
```

**Output (my run):**
```text
total: 3 relabel-and-retrain cycles x 3 days = 9 days = 45% of 20
if the first definition was planned work, avoidable loss = 6 days = 30%
{30: '42.0%', 60: '18.6%', 90: '9.7%'}
three definitions with a parametrised label: 1.5 days instead of 9
```

**Follow-ups:**
- What if the PM still changes it? Apply change control: it goes into the next sprint unless the owner accepts the cost.
- Which definition do you recommend? The one where most returners have returned (reactivation curve flattens), and that matches the action window.
- Is the loss 9 days or 6? 9 days is the total spent on three cycles; 6 days (30%) is the avoidable part if the first build was planned work.

**Common mistakes:**
- Counting the original build as lost time.
- Complaining without a number or a fix.
- Treating the definition as a technical choice rather than a business one.
- Retraining before the definition is agreed in writing.

### Q27 ⭐⭐ 🟡 Marketing wants to use customers' location history in a propensity model, which would add 0.4 percentage points of conversion across 1,000,000 customers, or 4,000 extra conversions worth 20 each (80,000). The privacy team says the consent terms do not cover this use. How do you weigh the 80,000 against the risk, and what do you propose?
**Asked at:** Ethics and fairness material (Yardstick data-ethics question page asking how bias was handled without disrupting the business, a University of Virginia online-ethics case on whether to keep a sensitive attribute in a model, a Data Science Newsletter ethics page, pre-screening pages on unethical data requests); practitioner pages rather than a confirmed interview bank; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The 80,000 is real but the consent terms do not cover this use, so I would not weigh it as a simple expected value; I would take it to privacy and legal as their decision, and propose a lawful route that keeps part of the gain.

**Clarifying questions:**
- What exactly do the consent terms say, and which law applies? Privacy decides, and I should not guess.
- Over what period is the 80,000, and how was the 0.4 point lift measured? A single estimate has an interval.
- What would a breach or complaint cost (fine, remediation, trust)? Needed for any trade-off.
- Which already-consented signals (city from billing address, app usage) could stand in?
- Could we ask customers for fresh opt-in? Yes or no changes the plan.

**Approach:**
1. Check the number: 1,000,000 x 0.4% = 4,000 conversions x 20 = 80,000.
2. Put uncertainty on it: with an illustrative test of 100,000 per arm at 5% base conversion, 0.4 point has a 95% interval of 0.21 to 0.59, so 41,800 to 118,200.
3. State the break-even: gain / loss = probability at which the gain is cancelled. With an illustrative 2,000,000 downside, 4%; with 10,000,000, 0.8%. A small chance of a large loss cancels the gain.
4. Say the key point: this is not only expected value. Using data beyond consent can be a legal violation and a trust problem. Privacy and legal own that decision; I do not trade it off alone.
5. Propose options: (a) do not use location history now; (b) run a consent campaign for opt-in, which at an illustrative 25% opt-in keeps 20,000; (c) use coarser, already-consented features, at an illustrative half the lift, 40,000; (d) pilot only on consented customers.
6. Give marketing a date and a plan, so the answer is "not this way, but this way".
7. Document the decision and the owner.

**Metrics:**
- Gain = customers x lift x value per conversion = 1,000,000 x 0.004 x 20.
- Break-even probability = gain / loss.
- Guardrails: opt-in rate, complaint and unsubscribe rate, share of features with documented consent.

**Risks:**
- Treating a fine as a cost of doing business.
- A model trained on location may leak into other products later; deletion and audit become hard.
- The coarser feature may carry little of the lift; test before promising.
- Marketing feels blocked and goes around the process.

**What the interviewer scores:**
- Strong: gets 80,000 right and shows its uncertainty and break-even. Weak: dismisses it or accepts it.
- Strong: sends the decision to privacy and legal with options. Weak: decides alone either way.
- Strong: offers lawful alternatives with numbers. Weak: only says no.
- Strong: respects the business goal. Weak: lectures on ethics.

**Example:** (illustrative numbers) Gain 80,000. If a breach would cost 2,000,000, the plan breaks even at a 4% chance. Opt-in at 25% leaves 20,000; coarse features at half the lift leave 40,000. Weak answer: "80,000 is a lot, the risk is small, let us do it." Or: "No, privacy said no." Strong answer: "The gain is 80,000, maybe 40,000 to 118,000. The consent does not cover it, so that is privacy's call. Here are two routes that keep 20,000 to 40,000 without that risk."

**Code:**
```python
cust, lift_pp, value = 1_000_000, 0.4, 20
extra = cust * lift_pp / 100
gain = extra * value
print(f"extra conversions {extra:,.0f}, gain {gain:,.0f}")
assert extra == 4000 and gain == 80_000
# break-even: how likely/large must the downside be to cancel the gain? (loss figure is illustrative)
for loss in (500_000, 2_000_000, 10_000_000):
    print(f"  if loss on a breach is {loss:,}: break-even probability {gain/loss:.1%}")
assert abs(80_000/2_000_000 - 0.04) < 1e-12
# uncertainty in the lift: illustrative test with 100,000 per arm, base conversion 5%
import math
se = math.sqrt(2*0.05*0.95/100_000)
lo, hi = lift_pp/100 - 1.96*se, lift_pp/100 + 1.96*se
print(f"lift 0.40pp, 95% CI {lo*100:.2f}pp to {hi*100:.2f}pp -> gain {lo*cust*value:,.0f} to {hi*cust*value:,.0f}")
assert 0.20 < lo*100 < 0.22 and 0.58 < hi*100 < 0.60
# legal options (illustrative rates)
optin = 0.25
consent_gain = cust*optin*lift_pp/100*value
coarse_gain = 0.5*gain
print(f"opt-in route at {optin:.0%} consent: {consent_gain:,.0f}; coarse region-level feature at half the lift: {coarse_gain:,.0f}")
assert consent_gain == 20_000 and coarse_gain == 40_000
```

**Output (my run):**
```text
extra conversions 4,000, gain 80,000
  if loss on a breach is 500,000: break-even probability 16.0%
  if loss on a breach is 2,000,000: break-even probability 4.0%
  if loss on a breach is 10,000,000: break-even probability 0.8%
lift 0.40pp, 95% CI 0.21pp to 0.59pp -> gain 41,793 to 118,207
opt-in route at 25% consent: 20,000; coarse region-level feature at half the lift: 40,000
```

**Follow-ups:**
- What if legal says it is fine? Then use it with data minimisation, retention limits and a monitored guardrail.
- What if the lift is only half of 0.4? The case shrinks to 40,000, and the break-even loss falls to 40,000 / probability.
- Should I still build the model? Yes, on consented data first.

**Common mistakes:**
- Netting a legal violation against revenue as if it were a cost line.
- Quoting the lift as exact.
- Saying no with no alternative.
- Leaving the decision undocumented.

### Q28 ⭐⭐ 🟡 A team ran a test with five metrics and wants to headline whichever one is significant. With five independent metrics and no true effect, the chance of at least one significant result at the 5% level is 1 - 0.95^5, about 22.6%. How do you push back, and what do you agree with them before the next test?
**Asked at:** Metric-definition and persuasion prompt pages (a 2026 data-analyst hiring guide naming a defended metric definition as a standard question, Yardstick persuasion and courage question pages for data scientists, Dataford pages on stakeholders disputing your findings); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The 22.6% is right, so one "win" out of five metrics is close to what chance alone gives, and I would agree one primary metric and a correction rule before the next test.

**Clarifying questions:**
- Which metric did the team name as primary before the test? If none, the test has no confirmatory result, only leads.
- Are the five metrics correlated? Correlated metrics make the true chance of a false hit lower than 22.6%, but never zero.
- What is the p-value of the "winner"? 0.04 among five is weak, 0.0004 is not.
- Does the winning metric make product sense with the change? A story that fits is better than a random hit.
- What decision hangs on this? A reversible UI tweak needs less proof than a pricing change.

**Approach:**
1. Agree with the arithmetic first: 1 - 0.95^5 = 22.6%. Say it kindly: "this is the cost of looking five times, not a mistake by you."
2. Reframe the result: it is a hypothesis, not a win. Report all five with their intervals.
3. Offer a repair that costs little: Bonferroni at 0.05/5 = 0.01 per metric, or Holm, which is never worse. Check the winner against 0.01 now.
4. Agree before the next test, in writing: one primary metric, two or three guardrails, the alpha, the sample size, the stop date, and that other metrics are labelled exploratory.
5. Offer a confirmation run on the winning metric alone. One pre-registered test has a 5% false-alarm rate again.
6. Pointer: Book 1 Part 10, Q9 covers Bonferroni and BH in detail.

**Metrics:**
- Family-wise error rate = P(at least one false positive among the m tests) = 1 - (1 - alpha)^m.
- Per-metric level after Bonferroni = alpha / m. Here 0.01.
- Primary metric: one number, defined with numerator, denominator and window before launch.
- Guardrails: metrics that must not get worse, tested one-sided with a margin, not used to declare a win.

**Risks:**
- Bonferroni costs power. Moving from 0.05 to 0.01 needs about 1.5 times the sample for the same power ((2.58+0.84)^2 / (1.96+0.84)^2 = 1.49).
- The team feels accused and stops asking you. Keep it about the process.
- A real effect on a secondary metric gets dropped. Keep it as a lead for the next test.

**What the interviewer scores:**
- Strong: states the 22.6% and what to do about it (one primary metric, correction, confirmation). Weak: "p-hacking is bad" with no alternative.
- Strong: gives the team a rule for the next test. Weak: only criticises this one.
- Strong: respectful tone and a face-saving path. Weak: lecture.
- Strong: notes correlation and power cost. Weak: applies Bonferroni mechanically.

**Example:** (illustrative numbers) Five metrics, p = 0.030, 0.20, 0.45, 0.60, 0.80. The first is "significant" at 5% but fails 0.01 and fails Holm (0.030 > 0.05/5 = 0.01). Weak answer: "You cannot headline that, it is p-hacking." Strong answer: "With five metrics there is a 22.6% chance of at least one false hit, so this one at 0.03 is a lead, not a result. Let us pick one primary metric together, write the rule down, and rerun on that metric alone. If it holds, you headline it with full confidence."

**Code:**
```python
# Illustrative: five metrics, no true effect. Multiple-comparison arithmetic plus a seeded simulation.
import numpy as np
m, alpha = 5, 0.05
fwer = 1 - (1 - alpha) ** m
print(f"P(at least one p<0.05 | 5 independent nulls) = {fwer:.4f}")
assert round(fwer, 3) == 0.226
bonf = alpha / m
sidak = 1 - (1 - alpha) ** (1 / m)
print(f"Bonferroni per-metric level {bonf:.4f}, Sidak {sidak:.5f}")
assert bonf == 0.01 and round(sidak, 5) == 0.01021
print(f"FWER with Bonferroni 0.01 each: {1-(1-bonf)**m:.4f}")
assert 1 - (1 - bonf) ** m < alpha
rng = np.random.default_rng(28)
sims = rng.uniform(size=(200_000, m))          # p-values are uniform under the null
any_sig = (sims < alpha).any(axis=1).mean()
any_bonf = (sims < bonf).any(axis=1).mean()
print(f"simulated: raw {any_sig:.3f}, Bonferroni {any_bonf:.3f}")
assert abs(any_sig - 0.226) < 0.005 and abs(any_bonf - 0.049) < 0.004
# What the team saw: smallest of five p-values. Its median under the null:
minp = sims.min(axis=1)
print(f"median of the smallest p-value under the null: {np.median(minp):.3f}")
assert abs(np.median(minp) - (1 - 0.5 ** (1 / 5))) < 0.003
# Holm on an example: p = 0.030, 0.20, 0.45, 0.60, 0.80 (one 'win' at 0.03)
p = np.array([0.030, 0.20, 0.45, 0.60, 0.80])
order = np.argsort(p)
holm_ok = [p[i] <= alpha / (m - k) for k, i in enumerate(order)]
holm_ok = [bool(x) for x in holm_ok]
print("Holm rejects:", holm_ok)
assert not any(holm_ok)
```

**Output (my run):**
```text
P(at least one p<0.05 | 5 independent nulls) = 0.2262
Bonferroni per-metric level 0.0100, Sidak 0.01021
FWER with Bonferroni 0.01 each: 0.0490
simulated: raw 0.228, Bonferroni 0.049
median of the smallest p-value under the null: 0.129
Holm rejects: [False, False, False, False, False]
```

**Follow-ups:**
- What if metrics are correlated? The false-hit chance is below 22.6%; use a permutation test or Holm, which stay valid.
- What if leadership wants the story anyway? Show the result as "directional, to be confirmed" with the confirmation date.

**Common mistakes:**
- Saying the result is wrong. It may be right; it is just not confirmed.
- Using Bonferroni on guardrails, which hides harms.
- Forgetting that picking the best of five makes the winner's effect size look bigger than it is.

### Q29 ⭐⭐ 🟡 The CEO believes the holiday campaign drove sales, which were 23 million against 20 million a year earlier, up 15%. Comparison regions that did not get the campaign grew 11%, so the expected figure is 22.2 million and the campaign accounts for 0.8 million. How do you tell her that the campaign was worth much less than she thinks?
**Asked at:** Metric-definition and persuasion prompt pages (a 2026 data-analyst hiring guide naming a defended metric definition as a standard question, Yardstick persuasion and courage question pages for data scientists, Dataford pages on stakeholders disputing your findings); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Sales did grow 15%, but regions without the campaign grew 11%, so only about 0.8 of the 3 million extra, a bit over a quarter, is the campaign.

**Clarifying questions:**
- How were campaign regions chosen? If they were the strongest markets, the comparison is unfair.
- Did the campaign regions and comparison regions grow alike in earlier years? Parallel trends are the whole argument.
- Is 23 million revenue or margin, and what did the campaign cost? Worth is about profit, not sales.
- Could the campaign spill over to comparison regions (national ads, online)? That would hide some effect.
- Was there pull-forward, with a dip in January? Then even 0.8 is too high.

**Approach:**
1. Start with what she is right about: sales are up 3 million, 15%. Do not open with "you are wrong."
2. Show the counterfactual: 20 x 1.11 = 22.2 is what we expect without the campaign. 23 - 22.2 = 0.8.
3. Put it as a picture: 3.0 total, 2.2 would have happened anyway, 0.8 is the campaign. 26.7%.
4. Give a range, not a point: comparison growth of 9% to 13% gives 1.2 to 0.4.
5. Connect to money: 0.8 million at a 30% margin is 0.24, below an invented 0.5 cost. State this is illustrative.
6. Offer what keeps the campaign: it may still help brand or retention; propose a holdout region next season.

**Metrics:**
- Incremental sales = actual in treated regions - last year x (1 + comparison growth).
- Share credited = incremental / (this year - last year).
- Incremental profit = incremental x margin - campaign cost. ROI = that / cost.
- Guardrails: pre-period fit between treated and comparison regions, and a January dip check.

**Risks:**
- Comparison regions are not twins, so the 0.8 is uncertain.
- Spillover understates the lift.
- She hears "marketing failed" and tunes out. Frame as "what we learn for next year."

**What the interviewer scores:**
- Strong: recomputes 22.2 and 0.8, gives a range. Weak: repeats the number without uncertainty.
- Strong: leads with agreement, then evidence, then a proposal. Weak: opens by contradicting the CEO.
- Strong: moves from sales to profit. Weak: stays on revenue.
- Strong: proposes a holdout for next time. Weak: leaves it as an argument.

**Example:** (illustrative numbers, millions) Last year 20, this year 23, comparison growth 11%. Weak: "Your 15% is wrong, most of it is not the campaign." Strong: "Sales are up 3 million and that is good news. Regions with no campaign also grew 11%, so we would have reached about 22.2 anyway. The campaign added about 0.8, with a range of 0.4 to 1.2. Next season let us hold out two regions so we can measure it cleanly."

**Code:**
```python
# Illustrative numbers, million. Difference-in-differences style counterfactual.
last, this = 20.0, 23.0
growth_all = this / last - 1
comp = 0.11
expected = last * (1 + comp)
lift = this - expected
print(f"raw growth {growth_all:.1%}, expected {expected:.1f}, campaign {lift:.2f}")
assert round(growth_all, 2) == 0.15 and round(expected, 1) == 22.2 and round(lift, 2) == 0.80
raw_gain = this - last                    # what the CEO credits
share = lift / raw_gain
print(f"CEO credits {raw_gain:.1f}; campaign share {share:.1%}; the other {raw_gain-lift:.1f} would have happened anyway")
assert raw_gain == 3.0 and round(share, 3) == 0.267
# Sensitivity: the comparison growth is itself uncertain.
for g in (0.09, 0.11, 0.13):
    print(f"comparison growth {g:.0%}: campaign = {this - last*(1+g):.2f}")
assert round(this - last*1.09, 2) == 1.20 and round(this - last*1.13, 2) == 0.40
# Break-even growth where the campaign is worth nothing, and where the CEO is right
print("campaign = 0 if comparison grew", f"{this/last-1:.0%}")
# Does it pay? Illustrative cost 0.5 and 30% margin on the incremental sales.
margin, cost = 0.30, 0.5
print(f"incremental margin {lift*margin:.2f} vs cost {cost}: net {lift*margin-cost:.2f}")
assert round(lift*margin - cost, 2) == -0.26
print(f"CEO view of margin: {raw_gain*margin:.2f} vs cost {cost}: net {raw_gain*margin-cost:.2f}")
assert round(raw_gain*margin - cost, 2) == 0.40
```

**Output (my run):**
```text
raw growth 15.0%, expected 22.2, campaign 0.80
CEO credits 3.0; campaign share 26.7%; the other 2.2 would have happened anyway
comparison growth 9%: campaign = 1.20
comparison growth 11%: campaign = 0.80
comparison growth 13%: campaign = 0.40
campaign = 0 if comparison grew 15%
incremental margin 0.24 vs cost 0.5: net -0.26
CEO view of margin: 0.90 vs cost 0.5: net 0.40
```

**Follow-ups:**
- What if comparison regions grew 15%? Then the campaign added nothing. The CEO's reading holds only if comparison growth is near zero.
- Can you run a better test? Yes, geo holdout with matched pre-trends, same as a difference-in-differences design.

**Common mistakes:**
- Treating last year as the baseline.
- Reporting 0.8 as exact.
- Judging the campaign on revenue, not margin after cost.
- Making the CEO feel foolish.

### Q30 ⭐⭐ 🟡 After launch, a model drifts and nobody knows who gets paged: engineering says it is a data-science issue and data science says it is an infrastructure issue. The model has already run for 9 days with a degraded input feed. How do you settle ownership, and what do you propose for alerts and on-call?
**Asked at:** Productionising prompt pages (several Dataford pages on moving a model from a notebook to production and collaborating with a data engineer, a Martin Fowler article against running notebooks in production, PyData talks on the notebook-to-production friction); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Ownership goes by what broke, with one named first responder on every alert, so a 9-day silent failure cannot happen again.

**Clarifying questions:**
- What exactly degraded: the input feed, the pipeline, or the model? Different owner for each.
- Who detected it after 9 days, and how? That shows the missing alert.
- Is there a written service level (freshness, quality, latency) for the feed? Without one, nobody is wrong.
- What did 9 days cost in decisions made? It sizes the urgency and the postmortem.
- Who is on call now in each team, and are they willing to carry a model page?

**Approach:**
1. Stop the blame: today, fix the feed or fall back to the last good model or rules. Business first.
2. Postmortem, blameless: timeline of the 9 days, why no alert fired, who could have seen it.
3. Split ownership by layer: feed freshness and nulls go to the data engineering on-call; serving, latency and errors go to platform; score drift and quality go to the model owner (data science); business KPI to the product owner.
4. One rule: the first page goes to the owner of the layer where the alert fires; a short written escalation path handles the cross-over, with a 30-minute handover window.
5. Alerts: feed null rate and freshness, input drift, score distribution, delayed-label quality. Page on two consecutive breaches; ticket for slower signals.
6. Write a runbook per alert: what it means, first check, fallback, who to wake.
7. Review monthly, count pages and false alarms, and prune.

**Metrics:**
- Time to detect = alert time - failure start. Time to acknowledge, time to mitigate.
- Alert precision = real incidents / pages. Aim to keep pages tolerable (illustrative: under 2 per week per person).
- Coverage = share of model inputs and outputs with an alert.
- Guardrails: pages per on-call shift, number of alerts with no runbook.

**Risks:**
- Alert fatigue if thresholds are tight.
- Data science on call for infrastructure things they cannot fix.
- Ownership on paper but no authority to fix the feed. Give each owner a lever.
- A second team doing the same thing twice.

**What the interviewer scores:**
- Strong: separates fix-now from settle-ownership. Weak: starts with an org chart.
- Strong: ownership by layer with one first responder. Weak: "both teams share it."
- Strong: concrete alerts and an escalation path. Weak: "add monitoring."
- Strong: blameless, with detection time as the metric. Weak: finds a culprit.

**Example:** (illustrative numbers) 9 days is 216 hours. A daily check that pages after two breaches finds it in 48 hours; an hourly check finds it in 2. Weak answer: "Engineering owns the pipeline, we own the model, so talk to them." Strong answer: "Whoever sees the alert first gets paged. A feed null-rate alert goes to data engineering, a score-drift alert goes to us, and each has a runbook. Today I will switch to the last good model while we fix the feed, then we hold a blameless review."

**Code:**
```python
# Illustrative: how long a degraded feed runs under different alert setups. 9 days = 216 hours.
days = 9
hours = days * 24
assert hours == 216
# Alert on feed null-rate, checked every N hours, pages after 2 consecutive breaches.
def detect_hours(check_every, breaches=2):
    return check_every * breaches
for name, every in (("no alert (found by a user)", None), ("daily check", 24), ("hourly check", 1), ("15-min check", 0.25)):
    if every is None:
        h = hours
    else:
        h = detect_hours(every)
    print(f"{name:28} detected after {h:6.2f} h, bad hours avoided {hours-h:6.2f} of {hours}")
assert detect_hours(1) == 2 and detect_hours(24) == 48
# Illustrative cost: 4,000 decisions per day, 3% extra wrong decisions while degraded, 20 per wrong decision
decisions_per_day, extra_wrong, cost = 4000, 0.03, 20
per_day = decisions_per_day * extra_wrong * cost
print(f"cost per degraded day {per_day:.0f}; 9 days {per_day*9:.0f}; 2 hours {per_day*2/24:.0f}")
assert per_day == 2400 and per_day * 9 == 21600 and round(per_day * 2 / 24) == 200
# Ownership table: first page goes to the owner of the thing that broke
owners = {"input feed null/late": "data-eng on-call", "serving latency/errors": "platform on-call",
          "score or label drift, quality": "model owner (DS)", "business KPI off": "product owner"}
for k, v in owners.items(): print(f"{k:32} -> {v}")
assert len(owners) == 4
```

**Output (my run):**
```text
no alert (found by a user)   detected after 216.00 h, bad hours avoided   0.00 of 216
daily check                  detected after  48.00 h, bad hours avoided 168.00 of 216
hourly check                 detected after   2.00 h, bad hours avoided 214.00 of 216
15-min check                 detected after   0.50 h, bad hours avoided 215.50 of 216
cost per degraded day 2400; 9 days 21600; 2 hours 200
input feed null/late             -> data-eng on-call
serving latency/errors           -> platform on-call
score or label drift, quality    -> model owner (DS)
business KPI off                 -> product owner
```

**Follow-ups:**
- What if the cause is unclear at 2 a.m.? The first responder owns the incident and calls the other side; nobody argues about cause until it is mitigated.
- Should data scientists be on call? For model quality, yes, with a business-hours target; for infrastructure, no.

**Common mistakes:**
- Settling who is guilty rather than who is paged.
- Alerting on everything.
- No fallback model, so mitigation is slow.
- Treating 9 days as an unlucky event instead of a missing alert.

### Q31 ⭐⭐ 🟡 Removing a postal-code feature cuts AUC from 0.80 to 0.78 but shrinks the approval-rate gap between two groups from 18 points to 6, a 12-point or two-thirds reduction. The credit-risk head only cares about AUC. How do you present the trade-off, and who should decide?
**Asked at:** Ethics and fairness material (Yardstick data-ethics question page asking how bias was handled without disrupting the business, a University of Virginia online-ethics case on whether to keep a sensitive attribute in a model, a Data Science Newsletter ethics page, pre-screening pages on unethical data requests); practitioner pages rather than a confirmed interview bank; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would show the trade-off in business and fairness numbers side by side, and say that the decision belongs to credit risk with compliance and legal, not to me alone.

**Clarifying questions:**
- Is the group gap in approvals, or after controlling for risk? A raw gap is a flag, not proof of unfairness.
- Does the postal code stand in for a protected attribute here? That is a legal question, so ask compliance.
- Are there other proxies left? Removing one feature may not fix the cause.
- What is the real cost of 0.02 AUC at the approval rate the bank uses? AUC is not money.
- What do regulators and internal policy require on fairness?

**Approach:**
1. Check the numbers: the gap drops 18 to 6 points, 12 points, two-thirds. AUC drops 0.02, 2.5% relative. Both are right.
2. Convert AUC to money. At a 60% approval rate with a 10% base default rate (illustrative, binormal), bad rate among approved goes from 3.43% to 3.87%, 0.44 points, about 266 extra defaults on 60,000 approvals.
3. Put both on one slide: cost of the AUC loss in rupees versus what the gap reduction means in legal and reputation risk.
4. Offer more options than yes/no: keep the feature but use a fairness constraint; replace it with a cleaner variable; adjust thresholds by policy only if the law allows.
5. Name the decision-makers: credit-risk head decides risk appetite, compliance and legal decide what is allowed, a senior committee signs off. I give recommendation and evidence.
6. Plan a follow-up: monitor the gap and the bad rate monthly.

**Metrics:**
- AUC (ranking) and bad rate among approved at the operating approval rate.
- Approval-rate gap = approval rate of group A - group B, in points. Also an equal-opportunity gap (approval among truly good borrowers).
- Expected loss = approved x bad rate x loss per default.
- Guardrails: calibration by group, and the share of applicants who change decision.

**Risks:**
- Dropping one feature rarely removes all proxy effects.
- Fairness fixes may be required by law, so this is not only a profit choice.
- Credit head sees fairness as a cost; legal sees AUC as a detail. Both need the same table.
- Group labels may not be legally usable to measure the gap. Check.

**What the interviewer scores:**
- Strong: translates AUC into default and money. Weak: argues AUC against fairness in the abstract.
- Strong: says who decides and why. Weak: "I would decide" or "the business decides."
- Strong: offers options beyond remove or keep. Weak: binary.
- Strong: careful with the claim that a gap means bias. Weak: assumes it does.

**Example:** (illustrative numbers) Gap 18 to 6 points. Bad rate 3.43% to 3.87%. Weak answer: "AUC fell only 0.02, so remove it." Strong answer: "The change costs about 0.44 points of bad rate, roughly 266 extra defaults per 60,000 approvals, and it cuts the approval gap by two-thirds. I will bring both to you and compliance, with two other options, and we decide together."

**Code:**
```python
# Illustrative. Translate AUC 0.80 vs 0.78 into bad rate among approved, and the fairness gap arithmetic.
from statistics import NormalDist
N = NormalDist()
gap0, gap1 = 18, 6
print("gap cut", gap0 - gap1, "points =", f"{(gap0-gap1)/gap0:.1%}")
assert gap0 - gap1 == 12 and round((gap0 - gap1) / gap0, 3) == 0.667
print("AUC drop", round(0.80 - 0.78, 2), "=", f"{0.02/0.80:.1%} relative")
assert round(0.02 / 0.80, 3) == 0.025
# Binormal: goods ~ N(0,1), bads ~ N(-d,1), AUC = Phi(d/sqrt2). Base default rate 10%, approve 60% of applicants.
def bad_rate_approved(auc, base=0.10, approve=0.60):
    d = 2 ** 0.5 * N.inv_cdf(auc)
    lo, hi = -10.0, 10.0
    for _ in range(100):                       # find cutoff c so that 60% score above c
        c = (lo + hi) / 2
        share = (1 - base) * (1 - N.cdf(c)) + base * (1 - N.cdf(c + d))
        if share > approve: lo = c
        else: hi = c
    bad_in = base * (1 - N.cdf(c + d))
    return bad_in / ((1 - base) * (1 - N.cdf(c)) + bad_in)
b80, b78 = bad_rate_approved(0.80), bad_rate_approved(0.78)
print(f"bad rate among approved: AUC 0.80 {b80:.2%}, AUC 0.78 {b78:.2%}, diff {100*(b78-b80):.2f} points")
assert round(b80, 4) == 0.0343 and round(b78, 4) == 0.0387, (b80, b78)
# Cost on 100,000 applicants, 60,000 approved, loss 2,000 per default (illustrative)
approved, loss = 60_000, 2000
extra_defaults = approved * (b78 - b80)
print(f"extra defaults {extra_defaults:.0f}, extra loss {extra_defaults*loss:,.0f}")
assert round(extra_defaults) == 266
```

**Output (my run):**
```text
gap cut 12 points = 66.7%
AUC drop 0.02 = 2.5% relative
bad rate among approved: AUC 0.80 3.43%, AUC 0.78 3.87%, diff 0.44 points
extra defaults 266, extra loss 532,675
```

**Follow-ups:**
- What if compliance says the feature must go regardless? Then the cost is a constraint, and I look for replacement features.
- What if the gap is explained by risk? Then it is a monitoring item and policy, not a data-science call.

**Common mistakes:**
- Equating a smaller gap with fairness.
- Reporting AUC without a money translation.
- Deciding alone.
- Forgetting other proxies for the same attribute.

### Q32 ⭐⭐ 🟡 The growth team wants the feed model that maximises clicks, while the content team wants a model with more diverse creators. The diverse model costs 0.8% relative click-through (4.0% to 3.968%) and raises the share of impressions to small creators. How do you frame this for both teams, and what would you test?
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would frame it as a price: 0.8% relative clicks, which is 0.032 points, for more reach to small creators, and I would test it for weeks, with creator and user retention as well as clicks.

**Clarifying questions:**
- What is the goal behind clicks? Revenue and retention are what growth really wants.
- What does the content team mean by diversity, and how is it measured? Share of impressions to small creators, number of creators reached?
- How big is the small-creator gain? The prompt gives the cost only, so I would ask for it.
- Is the click loss from users liking the content less, or from slower discovery? It decides if it improves.
- How many users and impressions are available, and for how long can we run?

**Approach:**
1. Restate the numbers: 4.0% to 3.968% is 0.8% relative, 0.032 points, 320 clicks per million impressions.
2. Make the two goals one table: clicks, small-creator share (illustrative 12% to 15%, +25% relative), creator retention, user retention.
3. Reframe for growth: clicks are short term; a creator who leaves reduces supply later. For content: the cost is real and bounded.
4. Test it as three arms: current model, diverse model, and maybe a blend with a weight on diversity. Randomise users.
5. Size it: seeing a 0.8% relative CTR change needs about 5.9 million impressions per arm (alpha 5%, power 80%), roughly 3 weeks at 100,000 users per arm with 20 impressions each per week (illustrative). Cluster by user, so be more careful.
6. Pre-agree the decision rule: ship if the click loss is under an agreed limit and creator or user retention is not worse, and the gain in small-creator share is at least a set size.
7. Plan a long-run holdout to see creator behaviour change over months.

**Metrics:**
- CTR = clicks / impressions, per user then averaged. Relative change = (CTR_diverse - CTR_current) / CTR_current.
- Small-creator impression share = impressions of small creators / all impressions.
- Creator 28-day retention, user 28-day retention and session length as guardrails.
- Diversity: number of distinct creators shown per user per week.

**Risks:**
- Short tests miss creator-side effects, which take weeks.
- Impressions are not independent within a user; naive tests are too confident.
- "Small creator" definition gamed by the model.
- The loss of 0.8% may be larger for new users.

**What the interviewer scores:**
- Strong: converts to absolute and per-million, and sizes the test. Weak: "run an A/B test."
- Strong: puts both goals in a common table with a decision rule. Weak: picks a side.
- Strong: thinks about long-run creator supply. Weak: only clicks.
- Strong: neutral language for both teams. Weak: sides with growth.

**Example:** (illustrative numbers) Weak: "Clicks matter most, keep the click model." Strong: "The diverse model costs 320 clicks per million impressions and raises small-creator share from 12% to 15% in our sketch. I would run three arms for about three weeks, watch creator retention, and agree beforehand that we ship if the click cost stays under 1% and retention does not fall."

**Code:**
```python
# Illustrative. Relative vs absolute CTR cost and the sample size needed to see it.
from statistics import NormalDist
N = NormalDist()
p0, rel = 0.040, 0.008
p1 = p0 * (1 - rel)
print(f"CTR {p0:.4%} -> {p1:.4%}; absolute drop {100*(p0-p1):.3f} points")
assert round(p1, 5) == 0.03968 and round(100 * (p0 - p1), 3) == 0.032
def n_per_arm(p, delta, alpha=0.05, power=0.80):
    z = N.inv_cdf(1 - alpha / 2) + N.inv_cdf(power)
    return 2 * p * (1 - p) * z * z / delta ** 2
n = n_per_arm(p0, p0 - p1)
print(f"impressions per arm to detect a 0.8% relative CTR change: {n:,.0f}")
assert 5.5e6 < n < 6.3e6
# at 20 impressions per user per week, one arm of 100,000 users per week
users_week = 100_000 * 20
print(f"weeks of 100k users/arm at 20 impressions/user/week: {n/users_week:.1f}")
assert 2.5 < n / users_week < 3.5
# Small-creator share (illustrative 12% -> 15% of impressions): what does a creator-side gain look like?
share0, share1 = 0.12, 0.15
print(f"small-creator impression share {share0:.0%} -> {share1:.0%}, +{(share1/share0-1):.0%} relative")
assert round(share1 / share0 - 1, 2) == 0.25
# Clicks cost per 1,000,000 impressions
print("clicks lost per 1M impressions:", round(1e6 * (p0 - p1)))
assert round(1e6 * (p0 - p1)) == 320
```

**Output (my run):**
```text
CTR 4.0000% -> 3.9680%; absolute drop 0.032 points
impressions per arm to detect a 0.8% relative CTR change: 5,886,660
weeks of 100k users/arm at 20 impressions/user/week: 2.9
small-creator impression share 12% -> 15%, +25% relative
clicks lost per 1M impressions: 320
```

**Follow-ups:**
- What if the diverse model also raises retention? Then it dominates and the argument is over.
- What if clicks fall 3%? Then try a blend with a small diversity weight and measure again.

**Common mistakes:**
- Calling 0.8% negligible without sizing.
- Randomising impressions, not users.
- Measuring diversity only by the model's own definition.
- Declaring a winner after one week.

### Q33 ⭐⭐ 🟡 Finance reports 4.2 million active users and the product team reports 3.6 million, a gap of 0.6 million or 14.3% of the finance figure, and each insists its number is right. The definitions differ on what counts as active and on how bots are treated. How do you resolve it in the room, and what do you change so it does not recur?
**Asked at:** Metric-definition and persuasion prompt pages (a 2026 data-analyst hiring guide naming a defended metric definition as a standard question, Yardstick persuasion and courage question pages for data scientists, Dataford pages on stakeholders disputing your findings); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Both numbers may be right for different definitions, so I would build a bridge from 4.2 to 3.6 in the room and then publish one named definition per use.

**Clarifying questions:**
- What is each team's exact definition of active (event, window, login or action)? That is most of the gap.
- How does each treat bots, test accounts and duplicates? That is the rest.
- What is each number used for (billing, board, product health)? Different uses can have different definitions.
- Who owns the user table, and are both teams reading the same source? A pipeline difference can add a third gap.
- Has the gap been stable over time? A growing gap points to a bot or logging change.

**Approach:**
1. Do not vote on whose number is right. Say: "let us find where the 0.6 million goes."
2. Write both definitions side by side.
3. Build a bridge: start at finance 4.2, remove bots, remove login-only users, remove test accounts, land on 3.6. Illustrative: 0.25 + 0.30 + 0.05 = 0.60.
4. Check the bridge sums to the gap, with nothing left unexplained. A leftover means a data issue.
5. Agree names: for example "Billable users" (finance) and "Engaged users" (product). Use each for its job; show the bridge.
6. Fix the cause: a metric dictionary with one owner, one SQL definition in a shared layer, a change log, and a monthly reconciliation check.

**Metrics:**
- Gap = finance - product = 0.6 million. As a share: 0.6/4.2 = 14.3% of finance, 0.6/3.6 = 16.7% of product.
- Bridge items: each removal as a number and a share of the gap; unexplained residual should be zero.
- Reconciliation drift: gap each month, alert on a change above a limit.
- Guardrail: both numbers refresh from the same raw table and date.

**Risks:**
- Each side hears "your number is wrong." Keep both defensible.
- One definition forced on both uses breaks billing or product work.
- The dictionary gets stale without an owner.
- Bot handling is a moving target; document the rule and the date.

**What the interviewer scores:**
- Strong: builds a bridge and shows it adds up. Weak: picks a side or averages.
- Strong: proposes named definitions per use. Weak: "we need one number" with no process.
- Strong: handles the room calmly. Weak: debates in the meeting.
- Strong: a durable fix (dictionary, owner, check). Weak: a one-off email.

**Example:** (illustrative numbers, millions) 4.2 less 0.25 bots is 3.95; less 0.30 login-only is 3.65; less 0.05 test accounts is 3.60. Weak: "Let us use the average, 3.9." Strong: "Here is the bridge: 0.25 bots, 0.30 login-only, 0.05 test accounts, which is exactly 0.6. Both numbers are right for their definitions. I propose we call them Billable and Engaged users and keep one definition file."

**Code:**
```python
# Illustrative bridge from 4.2M (finance) to 3.6M (product), millions.
fin, prod = 4.2, 3.6
gap = fin - prod
print(f"gap {gap:.1f}M = {gap/fin:.1%} of finance, {gap/prod:.1%} of product")
assert round(gap, 1) == 0.6 and round(gap / fin, 3) == 0.143 and round(gap / prod, 3) == 0.167
# Invented bridge: finance = any login in 30 days incl. bots; product = >=1 meaningful action, bots excluded.
bridge = [("bots and automated traffic", 0.25), ("login only, no meaningful action", 0.30), ("test and internal accounts", 0.05)]
run = fin
for name, v in bridge:
    run = round(run - v, 2)
    print(f"{name:36} -{v:.2f}  -> {run:.2f}")
assert run == prod and round(sum(v for _, v in bridge), 2) == round(gap, 2)
# Which number for which job (illustrative rule)
print("billing/seats -> finance definition; engagement -> product definition; both labelled with names")
# Cost of ambiguity: if growth is 5% on each series the absolute change differs
print("5% growth:", round(fin * 0.05, 2), "vs", round(prod * 0.05, 2), "million users")
assert round(fin * .05, 2) == 0.21 and round(prod * .05, 2) == 0.18
```

**Output (my run):**
```text
gap 0.6M = 14.3% of finance, 16.7% of product
bots and automated traffic           -0.25  -> 3.95
login only, no meaningful action     -0.30  -> 3.65
test and internal accounts           -0.05  -> 3.60
billing/seats -> finance definition; engagement -> product definition; both labelled with names
5% growth: 0.21 vs 0.18 million users
```

**Follow-ups:**
- What if the bridge leaves 0.1 unexplained? Treat it as a data defect and trace it to rows before presenting.
- Which number goes to the board? Whichever the board metric is defined as, labelled, with the other shown as a footnote.

**Common mistakes:**
- Averaging the two numbers.
- Saying 14.3% without saying of what (finance figure).
- Fixing it with one meeting and no owner.
- Letting a number be used for a job it was not defined for.

### Q34 ⭐⭐ 🟡 The sales VP asks you to raise the quarterly forecast from the model's 10.5 million to the target of 12 million, a 1.5 million or 14.3% uplift on the model figure. He says the sales team will hit it with effort. How do you respond, and how would you represent the model, the target and the risk gap in the deck?
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I will not change the model number, because a target is a goal and a forecast is an estimate, but I will show the target and the gap next to it so he can plan to close it.

**Clarifying questions:**
- Is 12 million a commitment to the board or an internal stretch? It changes how risky it is to publish a lower number.
- What did the model's error look like in past quarters? That sets how wide the range should be.
- What does sales plan to do differently (new deals, price, headcount) that the model has not seen?
- What is the pipeline today versus the same point last quarter? That is the evidence for his claim.
- Who uses the forecast (hiring, inventory, cash)? Over-forecasting has a cost for them.

**Approach:**
1. Acknowledge: "I want 12 to happen, and I can show what it takes."
2. Check the numbers: 12 - 10.5 = 1.5, which is 14.3% of the model figure.
3. Quantify risk: with an illustrative backtest error of sd 0.8, P10 to P90 is 9.47 to 11.53, so 12 is 1.88 sd above, about a 3% chance by the model alone.
4. Ask what must be true: how many extra deals or what conversion lift gives 1.5 million. Get sales to name them.
5. Deck design: three clearly labelled items: "Model forecast 10.5 (80% range 9.5-11.5)", "Target 12", "Gap 1.5, needs these actions". Add a commit level, for example P20 of 9.8.
6. Offer a scenario "model plus named initiatives" if he can show evidence for them, and a weekly tracker against both lines.

**Metrics:**
- Forecast error = (actual - forecast) / forecast; track MAPE and interval coverage (does 80% contain the actual 80% of the time).
- P(actual >= target) from the predictive distribution.
- Gap to target = target - forecast, and required weekly run-rate to close it.
- Guardrail: forecast bias over time, so the model is not quietly over or under.

**Risks:**
- Inflated forecast drives over-hiring or inventory, and the miss comes back to you.
- If you refuse flatly, he goes round you.
- The backtest error may be too optimistic, so the 3% is a floor on risk, not an exact number.
- Naming "sandbagging" in a deck sours the relationship; say "risk gap."

**What the interviewer scores:**
- Strong: keeps the forecast honest and offers a way to represent the target. Weak: gives in, or refuses without alternatives.
- Strong: quantifies the gap and the chance. Weak: "that is unrealistic."
- Strong: asks what must be true. Weak: debates optimism.
- Strong: clear deck with three labelled numbers. Weak: one blended number.

**Example:** (illustrative numbers) Model 10.5, range 9.5 to 11.5, target 12. Weak: "Fine, I will put 12 in the model." Strong: "The model says 10.5 with a likely range of 9.5 to 11.5. Twelve is a stretch target, about 3% likely on the model alone. Let me show a bridge of what sales would need to do to get the extra 1.5, and we will track both lines each week."

**Code:**
```python
# Illustrative: model forecast 10.5M, target 12M, assumed forecast error sd 0.8M (from a backtest, invented).
from statistics import NormalDist
model, target, sd = 10.5, 12.0, 0.8
uplift = target - model
print(f"gap {uplift:.1f}M = {uplift/model:.1%} of the model figure, {uplift/target:.1%} of target")
assert uplift == 1.5 and round(uplift / model, 3) == 0.143 and round(uplift / target, 3) == 0.125
N = NormalDist(model, sd)
p_hit = 1 - N.cdf(target)
p10, p90 = N.inv_cdf(0.10), N.inv_cdf(0.90)
print(f"P10 {p10:.2f}  P50 {model:.2f}  P90 {p90:.2f}  P(actual >= 12) = {p_hit:.1%}")
assert round(p10, 2) == 9.47 and round(p90, 2) == 11.53 and 0.02 < p_hit < 0.04
# z-score of the target
print("target is", round(uplift / sd, 2), "standard deviations above the model")
assert round(uplift / sd, 2) == 1.88
# What would make 12 a P50? Needed pipeline uplift on the base: 14.3% across the board.
# Illustrative commit/stretch view: commit at P20, stretch = target.
p20 = N.inv_cdf(0.20)
print(f"commit (P20) {p20:.2f}, model {model}, target {target}, risk gap to target {target-model:.1f}")
assert round(p20, 2) == 9.83
# If sales really lift by 5% of the model (an upside scenario), P(hit)
up = model * 1.05
print(f"model +5% -> {up:.2f}; P(>=12) = {1-NormalDist(up, sd).cdf(target):.1%}")
assert round(up, 2) == 11.03
```

**Output (my run):**
```text
gap 1.5M = 14.3% of the model figure, 12.5% of target
P10 9.47  P50 10.50  P90 11.53  P(actual >= 12) = 3.0%
target is 1.88 standard deviations above the model
commit (P20) 9.83, model 10.5, target 12.0, risk gap to target 1.5
model +5% -> 11.03; P(>=12) = 11.1%
```

**Follow-ups:**
- What if he insists on 12 in the forecast? Escalate to the shared owner of the forecast process; label the figure "target" and keep the model's own.
- What if the pipeline really is up? Then it belongs in the model as a feature, tested on past quarters.

**Common mistakes:**
- Editing the model output to please.
- Showing a point forecast with no range.
- Treating the 1.5 as only "effort".
- Presenting target and forecast as one line.

### Q35 ⭐⭐ 🔴 Your new model shows an AUC gain of 0.03 offline, but the online A/B test is flat after 3 weeks with a confidence interval that includes zero. The PM wants to ship anyway because of the roadmap, and you would rather stop. How do you handle the disagreement, and what do you check before you decide?
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** A flat test with an interval around zero says we cannot prove the gain, so I would check whether the test could have seen it and what shipping costs, then decide with the PM on numbers.

**Clarifying questions:**
- How big was the sample and what is the interval? The prompt gives neither. A wide interval means the test cannot tell.
- What effect was the test sized to detect? If the minimum detectable effect is bigger than a plausible gain, "flat" is uninformative.
- Is the A/B metric the same thing the offline AUC predicts? Ranking quality is not always the business metric.
- Did the experiment pass the sample-ratio check and run cleanly? A broken split makes everything moot.
- What does shipping cost (maintenance, latency, risk of a rollback) and what does delay cost the roadmap?

**Approach:**
1. Check the test: sample ratio, logging, exposure, and that the model served was the one evaluated.
2. Check power. Illustrative: 200,000 users per arm, 5.0% baseline. The standard error of the difference is 0.069 points; the minimum detectable effect at 80% power is 0.19 points (3.9% relative). Observed +0.03, interval [-0.11, +0.17].
3. Read it correctly: the data rule out a gain above 0.17 points and a loss beyond 0.11; they do not prove zero.
4. Check the offline-online gap: leakage in offline data, a changed population, metric mismatch, a novelty or fatigue effect, and segments set in advance.
5. Put money on it: +0.17 is worth about 660,000 a month and -0.11 costs about 420,000 on 1 million users at 400 per conversion (illustrative). The interval is two-sided, so the choice depends on maintenance cost and how reversible it is.
6. Offer options: run longer (four times the sample halves the interval: half-width 0.14 to 0.07), ship to a small share with a rollback trigger, or stop.
7. Agree a rule with the PM: "we ship if the lower bound is above minus X, or if the roadmap value of shipping is worth the downside", written in advance.

**Metrics:**
- Primary online metric difference with 95% interval; MDE = (z_alpha/2 + z_power) x SE.
- Sample ratio mismatch p-value.
- Offline AUC for reference, never as the launch criterion.
- Guardrails: latency, complaints, revenue per user, rollback rate.

**Risks:**
- Peeking after three weeks and extending until it turns significant inflates false positives. Set the extension length before looking.
- Shipping on the roadmap case gives a team a cost with no benefit.
- Stopping loses a real small gain of 0.1 points.
- Segment hunting after a flat result.

**What the interviewer scores:**
- Strong: asks about sample, interval and MDE. Weak: "flat means no effect" or "offline is better."
- Strong: checks test validity and the offline-online gap. Weak: argues by instinct.
- Strong: frames the disagreement as an explicit decision rule with costs. Weak: wins or loses on seniority.
- Strong: gives a middle path (small rollout, extension with pre-set length). Weak: ship or stop only.

**Example:** (illustrative numbers) 200,000 per arm, result +0.03 points with interval [-0.11, +0.17]. Weak: "AUC improved by 0.03, so ship it." Or: "It is flat, so kill it." Strong: "The test could only detect a lift of 0.19 points, so it cannot rule out a small gain. I propose extending for a pre-set period or a 10% rollout with a rollback trigger, and we agree now what we will do at each outcome."

**Code:**
```python
# Illustrative: flat A/B after 3 weeks. 200,000 users per arm, baseline conversion 5.0%.
from statistics import NormalDist
N = NormalDist()
n, p = 200_000, 0.050
se = (2 * p * (1 - p) / n) ** 0.5
z = N.inv_cdf(0.975) + N.inv_cdf(0.80)
mde = z * se
print(f"se of difference {100*se:.3f} pts; MDE (80% power) {100*mde:.2f} pts = {mde/p:.1%} relative")
assert round(100 * se, 3) == 0.069 and round(100 * mde, 2) == 0.19
# Observed: +0.03 pts (illustrative). CI:
obs = 0.0003
lo, hi = obs - 1.96 * se, obs + 1.96 * se
print(f"observed +{100*obs:.2f} pts, 95% CI [{100*lo:.2f}, {100*hi:.2f}] pts")
assert lo < 0 < hi and round(100 * hi, 2) == 0.17
# The test cannot rule out a +0.17 pt gain, nor a -0.11 pt loss. Value of each: 1M orders-able users, 400 per conversion (illustrative)
users, value = 1_000_000, 400
print("value of +0.17 pts on 1M users/month:", f"{hi*users*value:,.0f}", "; of -0.11 pts:", f"{lo*users*value:,.0f}")
assert round(hi * users * value, -3) == 660_000 and round(lo * users * value, -3) == -420_000
# How long to halve the CI? Quadruple the sample.
n2 = 4 * n
se2 = (2 * p * (1 - p) / n2) ** 0.5
print(f"4x sample ({n2:,}/arm) -> CI half-width {100*1.96*se2:.2f} pts (was {100*1.96*se:.2f})")
assert round(1.96 * se2 * 100, 2) == 0.07
# Ship cost vs run-on cost, expected value with a prior belief. P(real +0.1 pt)=0.3, else 0; ship cost 20,000/month.
gain_if_real = 0.001 * users * value
ev = 0.3 * gain_if_real
print(f"gain if real {gain_if_real:,.0f}/month; EV {ev:,.0f}/month vs maintenance 20,000")
assert gain_if_real == 400_000 and ev == 120_000
```

**Output (my run):**
```text
se of difference 0.069 pts; MDE (80% power) 0.19 pts = 3.9% relative
observed +0.03 pts, 95% CI [-0.11, 0.17] pts
value of +0.17 pts on 1M users/month: 660,335 ; of -0.11 pts: -420,335
4x sample (800,000/arm) -> CI half-width 0.07 pts (was 0.14)
gain if real 400,000/month; EV 120,000/month vs maintenance 20,000
```

**Follow-ups:**
- What if the interval is very narrow around zero? Then the gain is truly small and the model does not earn its upkeep.
- What if the PM has a strategic reason? Take it as a cost of the decision, written down, with a rollback trigger.

**Common mistakes:**
- Reading "not significant" as "no effect".
- Extending the test until it wins.
- Using offline AUC as proof of business value.
- Making it a contest of opinion.

### Q36 ⭐ 🟢 A stakeholder sets a target of 99% accuracy for a model on an event with a 1% base rate. A model that predicts no event for everyone already scores 99%. How do you reset the target without making the stakeholder feel foolish?
**Asked at:** Metric-definition and persuasion prompt pages (a 2026 data-analyst hiring guide naming a defended metric definition as a standard question, Yardstick persuasion and courage question pages for data scientists, Dataford pages on stakeholders disputing your findings); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Accuracy at a 1% event rate can be 99% for a model that catches nothing, so I would help set a target on how many events we catch and how clean the alerts are.

**Clarifying questions:**
- What happens when we miss an event, and what happens when we raise a false alarm? That gives the cost of each error.
- How many alerts can the team handle each day? It caps false alarms.
- Is the 1% rate stable? If it changes, precision changes with it.
- What does the stakeholder mean by 99%: "almost never wrong"? Start from that wish.
- Is there a rule or manual process today to beat?

**Approach:**
1. Respect the instinct: 99% sounds right because it is a good grade in most settings.
2. Show the baseline in one line: "a model that says no event for everyone scores 99% and catches none." Frame it as a well-known trap, not their mistake.
3. Ask the business question: "of 1,000 real events, how many must we catch, and how many false alerts can we afford?"
4. Convert to targets: recall (share of events caught) and precision (share of alerts that are real), or precision at the number of alerts the team can review.
5. Anchor on a baseline: compare with the rules or manual flag rate; and lift over the 1% base rate.
6. Write the target: for example "catch at least 70% of events with at least 50% of alerts real" (illustrative), and keep accuracy as a sanity check.
7. Pointer: Book 1 Part 3, Q1 explains why accuracy misleads on imbalanced data.

**Metrics:**
- Recall = TP / (TP + FN). Precision = TP / (TP + FP). Accuracy = (TP + TN) / total, reported but not targeted.
- Lift = precision / base rate.
- Expected value = TP x benefit - flags x review cost.
- Guardrails: alert volume per day, recall by segment.

**Risks:**
- Precision falls if the base rate falls.
- Targeting recall alone floods the team with alerts.
- The stakeholder feels corrected in front of others. Have the conversation privately first.
- A new target that no one understands gets ignored.

**What the interviewer scores:**
- Strong: gives the do-nothing baseline in numbers, then a replacement target. Weak: "accuracy is bad."
- Strong: asks about costs and capacity. Weak: picks F1 without asking.
- Strong: tone that protects the stakeholder. Weak: lecture.
- Strong: keeps a number in the target so it stays testable. Weak: "it depends."

**Example:** (illustrative numbers) 100,000 cases, 1,000 events. Predict-none: accuracy 0.99, recall 0. A model with 700 true alerts and 700 false alerts: accuracy 0.99, recall 0.70, precision 0.50, 50 times the base rate. Weak: "99% accuracy is a bad target." Strong: "Good news: a model that never alerts already scores 99, so accuracy cannot tell us if we are helping. Can we agree on catching at least 70% of real events, with half of alerts real? Then we can see the real gain."

**Code:**
```python
# Illustrative: 100,000 cases, 1% base rate.
N, base = 100_000, 0.01
pos = int(N * base); neg = N - pos
assert pos == 1000 and neg == 99_000
def report(name, tp, fp):
    fn, tn = pos - tp, neg - fp
    acc = (tp + tn) / N
    rec = tp / pos
    prec = tp / (tp + fp) if tp + fp else float("nan")
    print(f"{name:22} TP {tp:4} FP {fp:5} FN {fn:4} acc {acc:.3f} recall {rec:.2f} precision {prec:.2f}")
    return acc, rec, prec
a0, r0, _ = report("predict none", 0, 0)
a1, r1, p1 = report("model (700 TP, 700 FP)", 700, 700)
assert a0 == 0.99 and r0 == 0 and a1 == 0.99 and r1 == 0.70 and p1 == 0.50
# lift over base rate
print("precision lift over base rate:", p1 / base)
assert round(p1 / base) == 50
# Cost-based view: review costs 5 per flag, a caught event saves 200, a missed one costs 200 (illustrative)
def value(tp, fp, review=5, save=200):
    return tp * save - (tp + fp) * review
print("value none:", value(0, 0), " value model:", value(700, 700), " 'perfect 99% acc' that flags 100 only:", value(100, 0))
assert value(700, 700) == 700 * 200 - 1400 * 5 == 133_000
```

**Output (my run):**
```text
predict none           TP    0 FP     0 FN 1000 acc 0.990 recall 0.00 precision nan
model (700 TP, 700 FP) TP  700 FP   700 FN  300 acc 0.990 recall 0.70 precision 0.50
precision lift over base rate: 50.0
value none: 0  value model: 133000  'perfect 99% acc' that flags 100 only: 19500
```

**Follow-ups:**
- What if the stakeholder insists on one number? Use precision at a fixed alert volume, or expected value in money.
- What if the base rate drifts? Re-compute precision and set the alert threshold again.

**Common mistakes:**
- Saying "99% accuracy is impossible."
- Targeting recall with no precision limit.
- Forgetting the base rate when quoting precision.
- Correcting the stakeholder in public.

### Q37 ⭐ 🟡 The model-risk team wants three more weeks of validation, and each week of delay costs about 25,000 in lost benefit, so 75,000 in total. The business head wants to skip some of the checks. How do you work with both, and what could you offer to shorten the review safely?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing
**Say this first (1 line):** Both of them are protecting something real: the delay costs 75,000 (3 weeks x 25,000, illustrative), but a shipped defect can cost far more, so I offer a risk-ranked, shorter review plus a capped launch instead of picking a side.

**Clarifying questions:**
- Which checks are still open, and which are the ones that catch the worst failures? Why: not all checks carry equal risk, so I can rank them.
- Is the 25,000 a week lost benefit or deferred benefit, and does it scale with traffic? Why: if it scales with exposure, a capped launch captures part of it.
- What does a serious defect cost, and who owns that loss? Why: this sets the break-even failure probability.
- Is model-risk's three weeks calendar time or effort, and can parts run in parallel? Why: parallel work shortens the clock.
- Who signs off, and is there a rollback or kill switch? Why: a safe launch needs a reversible one.

**Approach:**
1. Say the delay cost out loud with the model-risk lead and the business head together: 75,000 for 3 weeks.
2. Ask model-risk to rank the remaining checks by what harm they prevent. Keep the top ones non-negotiable.
3. Offer to speed up their work: hand over data, code, and documentation up front, and run checks in parallel.
4. Propose a staged launch: one week of the critical checks, then a 20% exposure launch with monitoring and a rollback trigger, remaining checks finishing in parallel.
5. Tell the business head which checks I will not skip, and why, in terms of loss.
6. Write the decision, owners and rollback thresholds in one page that both sign.

**Metrics:** Cost of delay = weekly benefit x weeks not live. Capped launch captures weekly benefit x exposure share x weeks live. Break-even defect probability = delay cost / loss if a defect ships. Guardrails: defect found in monitoring within the cap, rollback time, share of high-risk checks completed before any launch.

**Risks:**
- A capped launch can still harm the 20% who see it. Pick low-stakes exposure first.
- Model-risk may feel I am going around them. Always give them a veto on the critical checks.
- "Lost benefit" may just be deferred, which makes delay cheaper than it looks.

**What the interviewer scores:**
- Strong: quantifies both sides, ranks checks by risk, offers staging with rollback, keeps model-risk independent.
- Strong: speaks to each party's actual concern.
- Weak: "I would escalate", or "I would skip the low-value checks" without saying how they are chosen.
- Weak: treats model-risk as an obstacle.

**Example:** Illustrative numbers: 25,000 a week, 3 weeks, 75,000. Option B: 1 week of critical checks, then 20% launch for 2 weeks. Benefit captured is 25,000 x 20% x 2 = 10,000, so net delay cost is 65,000. Skipping checks is justified only if the extra defect risk times the loss is below 75,000. With a 1,000,000 loss, break-even is 7.5%, and a 10-point rise in risk is 100,000 expected loss.
- Weak: "We cannot skip checks, that is policy." / "Just ship, three weeks is too long."
- Strong: "The delay costs 75,000. I would not skip the checks that catch the worst failures, but I can get you live on 20% of traffic after week one with a rollback trigger, while the rest finishes."

**Code:**
```python
# Q37: cost of delay versus expected loss from skipped checks (all numbers illustrative)
weekly_benefit = 25_000
weeks = 3
full_delay = weekly_benefit * weeks
assert full_delay == 75_000

# Option B: shorter, risk-ranked review: 1 week, then a capped launch (20% of traffic) for 2 weeks
review_weeks = 1
cap = 0.20
benefit_during_cap = weekly_benefit * cap * (weeks - review_weeks)
cost_B = full_delay - benefit_during_cap        # benefit not captured vs launching on day 0 ... in the 3-week window
assert benefit_during_cap == 10_000 and cost_B == 65_000

# Option C: skip checks. Break-even failure probability for an assumed loss if a defect ships
loss_if_defect = 1_000_000                       # illustrative
breakeven_p = full_delay / loss_if_defect
assert abs(breakeven_p - 0.075) < 1e-12
# if skipping raises the chance of shipping a serious defect by 10 points, expected loss:
extra_p = 0.10
exp_loss = extra_p * loss_if_defect
assert exp_loss == 100_000 and exp_loss > full_delay

print("A: full 3-week review, delay cost =", full_delay)
print("B: 1-week review + 20% capped launch, benefit captured =", benefit_during_cap, "net delay cost =", cost_B)
print("C: skip checks, break-even extra defect probability =", f"{breakeven_p:.1%}", "for loss", loss_if_defect)
print("   if skipping adds 10 points of defect risk, expected loss =", exp_loss, ">", full_delay)
```

**Output (my run):**
```text
A: full 3-week review, delay cost = 75000
B: 1-week review + 20% capped launch, benefit captured = 10000.0 net delay cost = 65000.0
C: skip checks, break-even extra defect probability = 7.5% for loss 1000000
   if skipping adds 10 points of defect risk, expected loss = 100000.0 > 75000
```

**Follow-ups:**
- What if model-risk refuses a staged launch? Respect it, show the numbers to the shared sponsor, and ask them to decide with both views on one page.
- What if the business head insists on skipping everything? Say which skipped check I would be unwilling to own, and escalate that item only.

**Common mistakes:** Calling the delay cost a reason to skip checks. Siding with whoever is more senior. Offering a launch with no rollback. Never quantifying the downside.

### Q38 ⭐ 🟡 Two data-science teams in different divisions built competing churn models, and each reports a slightly different AUC on its own data, 0.82 and 0.83. Executives want one model, and both team leads are defensive. How do you run a fair comparison, and how do you handle the politics?
**Asked at:** Project-conflict prompts (PracHub pages on ML project milestones, scope and conflict, on stakeholder conflict under a compressed delivery timeline and on cross-functional pushback on an analysis; one is tagged to a large marketplace and one to a social platform on the page, unverified); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** An AUC of 0.82 on one team's data and 0.83 on another's cannot be compared, so I propose one shared holdout, scored by a neutral party with both teams agreeing the rules first.

**Clarifying questions:**
- What decision will the model drive (who is contacted, what is offered)? Why: it sets the metric, for example lift at a contact budget instead of AUC.
- Do the two teams define churn the same way (window, label, population)? Why: different definitions make AUC meaningless to compare.
- Can both models score the same recent customers? Why: a common out-of-time holdout is the fair test.
- What are cost, latency and maintenance for each? Why: if they tie on accuracy, these decide.
- Who has the authority to pick one? Why: the process needs a decision owner agreed in advance.

**Approach:**
1. Agree the rules with both leads before anyone sees results: label definition, population, time split, metric, and tie-break rules.
2. Build one holdout neither team trained on, from a later time window than all training data.
3. Both teams submit scores. A third person computes the metrics.
4. Report AUC plus the business metric (for example churners caught in the top 10%), with a paired bootstrap interval on the gap.
5. If the gap is inside the noise, decide on cost, simplicity, explainability and ownership, or blend them.
6. Give both teams credit in the readout. Keep the best features and ideas of each.

**Metrics:** AUC on the shared holdout = probability a random churner scores above a random non-churner. Gap CI = percentile interval of the paired AUC difference over bootstrap resamples. Business metric = churners in the top 10% of scores / all churners. Guardrails: same label definition, no tuning on the holdout, calibration check if scores drive offers.

**Risks:**
- Each team's data has a different population, so its AUC reflects its own mix.
- A holdout one team helped build looks rigged. Use a neutral owner.
- Declaring a winner on a 0.01 gap that is noise.

**What the interviewer scores:**
- Strong: agrees rules before results, uses a shared out-of-time holdout, shows a paired interval, and treats the politics as a process problem.
- Strong: recommends a blend or a cost-based tie-break when the gap is noise.
- Weak: "pick the higher AUC", or ignores the people involved.

**Example:** Illustrative: on a shared test set of 5,000 customers with 479 churners, A scores 0.823 and B 0.831, gap 0.008, 95% interval [-0.005, 0.021]. That includes zero, so I do not declare a winner on accuracy.
- Weak: "0.83 beats 0.82, so team B wins."
- Strong: "Those numbers come from different data. On one shared holdout the gap is under a point and the interval includes zero, so let us decide on cost and maintainability and keep the best parts of both."

**Code:**
```python
# Q38: are AUC 0.82 and 0.83 distinguishable on ONE shared test set? (simulated, illustrative)
import numpy as np
rng = np.random.default_rng(38)
n, prev = 5000, 0.10
y = (rng.random(n) < prev).astype(int)

def auc(y, s):
    r = s.argsort().argsort() + 1.0
    npos = y.sum(); nneg = len(y) - npos
    return (r[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg)

# two correlated models (share a latent signal), A a bit weaker than B
shared = rng.normal(size=n)                       # noise both models see
a = 1.38 * y + 0.9 * shared + np.sqrt(1 - 0.81) * rng.normal(size=n)
b = 1.43 * y + 0.9 * shared + np.sqrt(1 - 0.81) * rng.normal(size=n)
auc_a, auc_b = auc(y, a), auc(y, b)
diffs = []
idx_all = np.arange(n)
for _ in range(1000):
    i = rng.choice(idx_all, n)
    if y[i].sum() in (0, n): continue
    diffs.append(auc(y[i], b[i]) - auc(y[i], a[i]))
lo, hi = np.percentile(diffs, [2.5, 97.5])
print(f"positives in test set = {int(y.sum())}")
print(f"AUC A = {auc_a:.3f}, AUC B = {auc_b:.3f}, observed gap = {auc_b-auc_a:.3f}")
print(f"paired bootstrap 95% CI for gap = [{lo:.3f}, {hi:.3f}]")
assert y.sum() > 400
assert 0 < auc_b - auc_a < 0.03
assert (hi - lo) > 0.005       # interval has real width
print("CI includes 0:", lo <= 0 <= hi)
```

**Output (my run):**
```text
positives in test set = 479
AUC A = 0.823, AUC B = 0.831, observed gap = 0.008
paired bootstrap 95% CI for gap = [-0.005, 0.021]
CI includes 0: True
```

**Follow-ups:**
- How big a gap would count? One whose interval excludes zero and that moves the business metric enough to matter, agreed before the test.
- What if the teams refuse the shared holdout? Ask the sponsor to mandate it, and offer them a say in its design.

**Common mistakes:** Comparing numbers from different datasets. Letting one team build the test. Choosing on AUC alone. Embarrassing the losing team publicly.

### Q39 ⭐ 🟡 The CFO asks the data-science team to justify its cost of 1.8 million a year. The team has claimed benefits of 3.0 million, but 40% of that is also claimed by other initiatives, so only 1.8 million is solely attributable. How do you present the return honestly, and what do you say about work whose value is hard to measure?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing
**Say this first (1 line):** I would show a range, not one number: the claimed 3.0 million, the sole-attribution floor of 1.8 million, and a shared-credit view in between, because on the floor the team only breaks even against its 1.8 million cost.

**Clarifying questions:**
- How was each benefit measured (experiment, before and after, estimate)? Why: this sets how much the CFO should trust it.
- Which initiatives share the 40%, and do they also claim the same dollars? Why: double counting is the CFO's real worry.
- Is the 1.8 million cost fully loaded? Why: ROI changes with the cost base.
- Is the benefit recurring or one-off? Why: it decides the multi-year return.
- What does the CFO need: justify or decide on headcount? Why: it shapes the answer.

**Approach:**
1. Start with the honest floor: 60% of 3.0 million is 1.8 million, equal to cost, so net 0 on a sole-credit basis.
2. Show a middle case: sole plus half the shared pool is 2.4 million, net 0.6 million, ROI 33%.
3. Show the claimed 3.0 million as the upper bound, labelled as including shared credit.
4. Agree an attribution rule with finance and the other initiatives so the total across all claims is at most 100%.
5. For hard-to-measure work, list it separately with proxies and a clear label: decisions made faster, risks avoided, no dollar value invented.
6. Ask for the decision that follows: fund, grow or refocus, with next year's measurement plan.

**Metrics:** ROI = (attributed benefit - cost) / cost. Sole benefit = claimed x (1 - shared share). Guardrail: sum of credits across initiatives is at most 100% of the measured benefit; each benefit tagged measured or estimated.

**Risks:**
- Defending the 3.0 million loses the CFO's trust when double counting is found.
- Showing only the floor undervalues enabling work.
- Inventing a dollar value for hard-to-measure work.

**What the interviewer scores:**
- Strong: gives a range, shows the arithmetic, volunteers the weakness, and states what is unmeasured.
- Strong: proposes a shared attribution rule.
- Weak: defends the largest number or hides the shared 40%.

**Example:** Illustrative: claimed 3,000,000; shared 40% is 1,200,000; sole 1,800,000; cost 1,800,000.
- Weak: "We return 3.0 million on 1.8 million, a 67% return."
- Strong: "On benefits only we can claim alone, we break even. With half credit for the shared 1.2 million it is 2.4 million, a 33% return. Here is how we measured each."

**Code:**
```python
# Q39: honest ROI range for a 1.8M/yr team (illustrative)
cost = 1_800_000
claimed = 3_000_000
shared_share = 0.40
shared = claimed * shared_share
sole = claimed - shared
assert abs(shared - 1_200_000) < 1e-6 and abs(sole - 1_800_000) < 1e-6
def roi(b): return (b - cost) / cost
rows = [("claimed (everything)", claimed),
        ("sole only (floor)", sole),
        ("sole + half of shared", sole + 0.5 * shared)]
for name, b in rows:
    print(f"{name:24} benefit {b:>10,.0f}  net {b-cost:>10,.0f}  ROI {roi(b):6.1%}")
assert roi(claimed) > 0.66 and roi(claimed) < 0.67
assert roi(sole) == 0
assert abs(roi(sole + 0.5 * shared) - 1/3) < 1e-9
# how much of the shared 1.2M must we be credited to reach 25% ROI?
need = cost * 1.25 - sole
print(f"credit needed from shared pool for 25% ROI = {need:,.0f} of {shared:,.0f} ({need/shared:.0%})")
assert abs(need - 450_000) < 1e-6
```

**Output (my run):**
```text
claimed (everything)     benefit  3,000,000  net  1,200,000  ROI  66.7%
sole only (floor)        benefit  1,800,000  net          0  ROI   0.0%
sole + half of shared    benefit  2,400,000  net    600,000  ROI  33.3%
credit needed from shared pool for 25% ROI = 450,000 of 1,200,000 (38%)
```

**Follow-ups:**
- What about work with no measurable value? Say it is unmeasured, give leading indicators, and do not defend it with a made-up number.
- How would you improve next year? Pre-register measurement for each project.

**Common mistakes:** Double counting. Hiding the shared pool. Presenting cost per head without outcomes. Quantifying everything by guesswork.

### Q40 ⭐ 🟡 Leadership proposes replacing the analytics team's routine requests with an LLM text-to-SQL tool. On a test of 200 representative questions it answered 148 correctly (74%), and the business says it needs 95% for unsupervised use. How do you present the result, and what hybrid arrangement would you suggest?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to AI-era build-versus-buy and hallucination-risk material (2026 vendor and CTO-guide pages such as ThirstySprout and TKMX AI on API versus self-host and LLM cost, an InfoQ LLM-adoption article); no interview page for the leadership-pressure framing was found
**Say this first (1 line):** 148 of 200 is 74%, with a 95% interval of roughly 67% to 80%, so it is clearly below the 95% bar for unsupervised use, but it may be good enough for a hybrid where the tool drafts and a human checks.

**Clarifying questions:**
- What does a wrong answer cost (a bad decision, or a mild rework)? Why: it sets the acceptable error rate per question type.
- How were the 200 questions sampled, and who judged "correct"? Why: a biased test misleads either way.
- What types of questions fail? Why: errors are concentrated, which makes routing possible.
- Is there a certified semantic layer or metric definitions the tool can use? Why: it usually raises accuracy a lot.
- Who reviews outputs and how fast? Why: it sets whether supervised use is affordable.

**Approach:**
1. Present 74% with its interval, and translate it: 26 wrong answers per 100 questions versus 5 allowed at 95%.
2. Break results down by question type. Show where it is strong and weak.
3. Propose tiers: (a) unsupervised for simple questions on certified metrics once a tier is proven at 95% or better with a large enough sample, (b) tool drafts SQL and an analyst reviews for the rest, (c) humans own open-ended and high-stakes questions.
4. Add guardrails: show the generated SQL, log every query, spot-check a weekly sample, and re-test on new questions.
5. Define the promotion rule: a tier goes unsupervised only when its lower confidence bound reaches the target.
6. Report the time saved honestly, net of review time.

**Metrics:** Accuracy = correct answers / questions tested. 95% Wilson interval for a proportion. Per tier accuracy. Review time per question. Guardrail: wrong-answer rate on the weekly audit sample.

**Risks:**
- Confident wrong answers get used without anyone noticing.
- A test set that is easier than real traffic.
- Proving 95% needs enough samples: with zero errors, 73 straight correct answers are needed before the lower bound reaches 95%.

**What the interviewer scores:**
- Strong: interval, error translation, tiers, promotion rule.
- Strong: neither dismisses nor oversells the tool.
- Weak: "74% is too low, no", or "it will improve, roll it out".

**Example:** Illustrative split that adds to 148 of 200: simple certified-metric questions 114 of 120 (95.0%, interval 89.5% to 97.7%), open-ended questions 34 of 80 (42.5%). So only the simple tier is near the bar and still unproven.
- Weak: "74 percent is not good enough, so we keep the analytics team as is."
- Strong: "74% overall hides a 95% tier and a 43% tier. Let the tool serve the first tier with SQL shown and audited, draft for the second, and keep humans on the rest."

**Code:**
```python
# Q40: what does 148/200 really say? Wilson interval + routing example (illustrative)
from math import sqrt
def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
k, n = 148, 200
lo, hi = wilson(k, n)
print(f"overall {k}/{n} = {k/n:.0%}, 95% Wilson CI [{lo:.3f}, {hi:.3f}]")
assert k / n == 0.74 and hi < 0.95            # even the top of the interval misses 95%
print("wrong answers per 1,000 questions: tool", round(1000*(1-k/n)), "vs target", round(1000*0.05))
# by tier (invented split that adds up to 148/200)
simple_k, simple_n = 114, 120
hard_k, hard_n = 34, 80
assert simple_k + hard_k == k and simple_n + hard_n == n
for name, kk, nn in [("simple/certified-metric", simple_k, simple_n), ("open-ended", hard_k, hard_n)]:
    l, h = wilson(kk, nn)
    print(f"{name:24} {kk}/{nn} = {kk/nn:.1%}  CI [{l:.3f}, {h:.3f}]")
# how many all-correct trials would prove >=95% lower bound? smallest n with 0 errors
m = 1
while wilson(m, m)[0] < 0.95: m += 1
print("smallest all-correct run whose lower bound reaches 95% =", m)
assert wilson(m, m)[0] >= 0.95 > wilson(m-1, m-1)[0]
```

**Output (my run):**
```text
overall 148/200 = 74%, 95% Wilson CI [0.675, 0.796]
wrong answers per 1,000 questions: tool 260 vs target 50
simple/certified-metric  114/120 = 95.0%  CI [0.895, 0.977]
open-ended               34/80 = 42.5%  CI [0.323, 0.534]
smallest all-correct run whose lower bound reaches 95% = 73
```

**Follow-ups:**
- Would more prompt work fix it? Maybe, but re-test on fresh questions, not the same 200.
- What does the analytics team do afterwards? See Q45 of this part.

**Common mistakes:** Quoting 74% without an interval. Averaging over question types. Testing on the questions used to tune prompts. Skipping an audit after launch.

### Q41 ⭐ 🟡 A VP asks you in a planning meeting to commit to a 90% accuracy figure before anyone has looked at the data. You have not seen label quality, class balance or the baseline yet. What do you say in the meeting, and what do you commit to instead?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing
**Say this first (1 line):** I cannot honestly promise 90% yet, because accuracy means nothing without the baseline and label quality, so I commit to a two-week discovery with a stated date for a target and a range.

**Clarifying questions:**
- What decision does the model drive and what do errors cost? Why: accuracy may be the wrong metric.
- What is the positive rate? Why: at 10% a model that says "no" always gets 90%.
- How are labels produced and how noisy are they? Why: noise caps measurable accuracy.
- What is today's baseline (rules, human)? Why: a target should be relative to it.
- When is the figure needed and for what purpose? Why: a date for the estimate may be all they need.

**Approach:**
1. In the meeting: "I want to hit a number we can defend, and I have not seen the data. I will give you a target and a range by a specific date."
2. Explain with one example: if only 10% are positive, a model that never flags anything scores 90%.
3. Commit to a short discovery: label audit, class balance, baseline, and a first simple model.
4. Propose the metric tied to the decision (for example recall at a review budget) and agree what "good" means.
5. Deliver the estimate with a range and the assumptions that would move it.
6. Put the agreed target, and the conditions for revisiting it, in writing.

**Metrics:** Baseline accuracy = max(p, 1-p) for positive rate p. Lift over baseline. Label noise ceiling: with 8% wrong labels a perfect model measures about 92%. Guardrail: report the metric on a time-split holdout.

**Risks:**
- Saying "no" with no alternative sounds obstructive.
- A target made up in the room becomes a promise.
- Discovery with no end date.

**What the interviewer scores:**
- Strong: refuses to commit politely, explains in one example, commits to a date and a process.
- Weak: caves to 90%, or lectures about accuracy.

**Example:** Illustrative: at positive rates of 1%, 5%, 10%, 50%, 90% the always-majority baseline is 99%, 95%, 90%, 50%, 90%. A perfect model scored against labels with 8% errors measures about 92%.
- Weak: "Sure, we will aim for 90%." / "Accuracy is a bad metric."
- Strong: "I will give you a committed target and range in two weeks, after I check labels and the baseline. If the positive rate is near 10%, 90% is what doing nothing scores."

**Code:**
```python
# Q41: why a bare 90% accuracy number means nothing before baseline and label quality
import numpy as np
print("majority-class baseline accuracy by positive rate:")
for p in (0.01, 0.05, 0.10, 0.50, 0.90):
    base = max(p, 1 - p)
    print(f"  positive rate {p:>4.0%} -> baseline {base:.0%}")
assert max(0.10, 0.90) == 0.90          # at 10% prevalence the 'no' model already scores 90%
assert max(0.90, 0.10) == 0.90
# label noise ceiling: a perfect model scored against labels that are 8% wrong
rng = np.random.default_rng(41)
n = 100_000
truth = rng.random(n) < 0.3
flip = rng.random(n) < 0.08
labels = truth ^ flip
perfect_pred = truth
acc = (perfect_pred == labels).mean()
print(f"perfect model vs labels with 8% noise: measured accuracy = {acc:.3f}")
assert abs(acc - 0.92) < 0.005
```

**Output (my run):**
```text
majority-class baseline accuracy by positive rate:
  positive rate   1% -> baseline 99%
  positive rate   5% -> baseline 95%
  positive rate  10% -> baseline 90%
  positive rate  50% -> baseline 50%
  positive rate  90% -> baseline 90%
perfect model vs labels with 8% noise: measured accuracy = 0.919
```

**Follow-ups:**
- What if the VP insists? Offer a conditional: "90% if labels and baseline look like X; I will tell you at the two-week review if not."
- Is it ever fine to give a rough number early? Yes, as a labelled range with assumptions.

**Common mistakes:** Committing without data. Refusing with no date. Using jargon in the meeting. Forgetting the decision metric.

### Q42 ⭐ 🔴 You discover that a model presented to leadership last quarter had a leakage bug, and the reported AUC of 0.91 is closer to 0.78 once fixed. Decisions have been made on it and the senior sponsor would rather leave it quiet. What do you do and say, and in what order?
**Asked at:** Ethics and fairness material (Yardstick data-ethics question page asking how bias was handled without disrupting the business, a University of Virginia online-ethics case on whether to keep a sensitive attribute in a model, a Data Science Newsletter ethics page, pre-screening pages on unethical data requests); practitioner pages rather than a confirmed interview bank; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would verify the bug, tell the sponsor myself and privately first, then correct the record with everyone who relied on the 0.91, because staying quiet is not an option.

**Clarifying questions:**
- Is the bug confirmed by someone independent of me? Why: I need to be sure before raising it.
- Which decisions used the model and what did they commit (money, customers)? Why: sets urgency.
- Is the model still live? Why: ongoing harm requires acting immediately.
- Are there reporting, audit or regulatory duties? Why: they decide who must be told.
- Who is the sponsor's boss or the model-risk contact? Why: I need an escalation route.

**Approach:**
1. Reproduce: fix the leak, re-run, and have a peer confirm 0.78.
2. Size the impact: what the real number means for the decisions made.
3. Go to the sponsor first, privately, with the fix, the impact and a proposed correction plan. Present it as a problem we solve together.
4. Ask for the correction to go out within days, with the sponsor presenting it.
5. If the sponsor still refuses, escalate to the model-risk or governance owner and tell the sponsor I am doing so. Do not go around silently.
6. Fix the process: add a leakage check and a second reviewer before any future presentation.

**Metrics:** AUC before and after the fix; positives caught in the top 10% before versus after; decisions affected; time from discovery to correction. Guardrail: written record of who was told and when.

**Risks:**
- Career risk. A late discovery by someone else is worse.
- Blaming the original author instead of the process.
- Corrections that omit the consequence for decisions.

**What the interviewer scores:**
- Strong: verifies first, goes to the sponsor first with a plan, corrects the record, escalates if needed, fixes the process.
- Weak: stays quiet, or goes straight to leadership over the sponsor.

**Example:** Illustrative binormal model with 10% positives. At AUC 0.91 reviewing the top 10% of customers catches about 58%; at 0.78 about 36%. Per 100,000 customers that is 5,844 promised versus 3,551 real, a shortfall of 2,292.
- Weak: "It is only a few points, it is probably fine."
- Strong: "I found a leakage bug. The real AUC is 0.78, not 0.91, and it changes how many customers we catch. I want us to tell leadership this week and I have a plan."

**Code:**
```python
# Q42: what the leaked AUC would have promised vs the real one (binormal model, illustrative)
from scipy.stats import norm
def d_prime(auc): return 2**0.5 * norm.ppf(auc)
def prec_recall_top(auc, prev, frac):
    d = d_prime(auc)
    # find threshold c so that flagged share = frac: prev*(1-Phi(c-d)) + (1-prev)*(1-Phi(c)) = frac
    lo, hi = -10, 10
    for _ in range(200):
        c = (lo + hi) / 2
        share = prev * norm.sf(c - d) + (1 - prev) * norm.sf(c)
        if share > frac: lo = c
        else: hi = c
    tp = prev * norm.sf(c - d)
    return tp / frac, tp / prev
prev, frac = 0.10, 0.10
for auc in (0.91, 0.78):
    p, r = prec_recall_top(auc, prev, frac)
    print(f"AUC {auc}: reviewing top 10% of customers -> precision {p:.1%}, recall {r:.1%}")
p91, r91 = prec_recall_top(0.91, prev, frac)
p78, r78 = prec_recall_top(0.78, prev, frac)
assert p91 > p78 and r91 > r78
cust = 100_000
print("per 100,000 customers, positives caught in the top 10%:",
      round(cust*prev*r91), "promised vs", round(cust*prev*r78), "real")
print("shortfall =", round(cust*prev*(r91-r78)), "positives")
```

**Output (my run):**
```text
AUC 0.91: reviewing top 10% of customers -> precision 58.4%, recall 58.4%
AUC 0.78: reviewing top 10% of customers -> precision 35.5%, recall 35.5%
per 100,000 customers, positives caught in the top 10%: 5844 promised vs 3551 real
shortfall = 2292 positives
```

**Follow-ups:**
- What if the sponsor threatens you? Keep a written record, use the governance route.
- How do you prevent it? Temporal splits, a leakage review, a second reviewer. Book 1 Part 03 has the thresholding material, and Book 1 Part 01 has the leakage question: "What is data leakage? Give 4 real examples (target, preprocessing, temporal, group) and how you would detect it."

**Common mistakes:** Waiting for a better moment. Going public before the sponsor. Hiding the impact. Fixing silently and swapping the number.

### Q43 ⭐ 🔴 You are asked to retire a legacy scorecard that a powerful VP relies on, because your new model has an AUC 0.02 higher on a holdout, with a paired bootstrap interval that excludes zero. The VP's team built the scorecard and fears losing visibility and influence. How do you plan the transition, and what do you do if the VP refuses?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing
**Say this first (1 line):** I would make the VP a co-owner of the transition: run the model in parallel, keep what the VP values visible, and only retire the scorecard against exit criteria both of us agreed, with the sponsor deciding if we cannot agree.

**Clarifying questions:**
- What does the VP actually use the scorecard for (decisions, reports, team status)? Why: that is what I must preserve.
- Does the 0.02 AUC gap hold on a fresh holdout, with a paired bootstrap interval that excludes zero? Why: a gap that may be noise is a weak reason to retire anything.
- What does 0.02 mean in the business metric? Why: the VP will respond to catches, not AUC.
- Who decides retirement and what rules apply (model risk, regulator)? Why: sets the authority path.
- Can the scorecard's reasoning be explained to the same level by the model? Why: loss of explainability is a legitimate objection.

**Approach:**
1. Listen to the VP first. Name what the scorecard gives them.
2. Show evidence: gap with interval and the extra positives caught at the operating point.
3. Run both in parallel for an agreed period (for example one or two quarters).
4. Preserve visibility: the VP's team owns the dashboards and the review of the new model, with the scorecard reasons shown as features.
5. Write exit criteria: gap holds, no segment is worse, explainability accepted. Retire when they are met.
6. If the VP refuses, escalate to the shared sponsor with the evidence and the offer of a longer parallel run. Do not go around the VP.

**Metrics:** AUC gap with paired bootstrap interval; positives caught in the top 10% (old vs new); segment-level gaps; adoption of the new dashboards. Guardrails: no segment degrades, explanations available.

**Risks:**
- Winning the argument and losing the relationship.
- A gap that shrinks out of time.
- Loss of reasons that the scorecard gave in plain language.

**What the interviewer scores:**
- Strong: empathy, evidence in business terms, parallel run, shared ownership, clean escalation.
- Weak: "the numbers are better, retire it", or quietly going to the VP's boss.

**Example:** Illustrative simulation of 20,000 customers with 1,999 positives: old AUC 0.776, new 0.796, gap 0.020, interval [0.014, 0.028], which excludes zero. In the top 10% the old scorecard catches 683 and the new model 737, an extra 54.
- Weak: "Your scorecard is out of date, we are switching on Monday."
- Strong: "Your team built the scorecard that set the standard. In parallel, the model catches 54 more per 20,000. Let us run both for a quarter, and your team keeps the review and the dashboards."

**Code:**
```python
# Q43: is "2 AUC points better" proven, and what does it buy? (simulated, illustrative)
import numpy as np
rng = np.random.default_rng(43)
n, prev = 20_000, 0.10
y = (rng.random(n) < prev).astype(int)
def auc(y, s):
    r = s.argsort().argsort() + 1.0
    npos = y.sum(); nneg = len(y) - npos
    return (r[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg)
shared = rng.normal(size=n)
old = 1.04 * y + 0.9 * shared + np.sqrt(0.19) * rng.normal(size=n)   # about 0.77
new = 1.14 * y + 0.9 * shared + np.sqrt(0.19) * rng.normal(size=n)   # about 0.80
a_old, a_new = auc(y, old), auc(y, new)
diffs = []
for _ in range(500):
    i = rng.integers(0, n, n)
    diffs.append(auc(y[i], new[i]) - auc(y[i], old[i]))
lo, hi = np.percentile(diffs, [2.5, 97.5])
print(f"old AUC {a_old:.3f}, new AUC {a_new:.3f}, gap {a_new-a_old:.3f}, 95% CI [{lo:.3f}, {hi:.3f}]")
assert 0.015 < a_new - a_old < 0.05 and lo > 0
# business translation: positives caught when the team reviews the top 10% of scores
k = int(0.10 * n)
def caught(s): return int(y[np.argsort(-s)[:k]].sum())
c_old, c_new = caught(old), caught(new)
print(f"positives total {int(y.sum())}; caught in top 10%: old {c_old}, new {c_new}, extra {c_new-c_old}")
assert c_new > c_old
# a 0.02 AUC claim only holds up if the interval is clear of zero and the extra catches matter
```

**Output (my run):**
```text
old AUC 0.776, new AUC 0.796, gap 0.020, 95% CI [0.014, 0.028]
positives total 1999; caught in top 10%: old 683, new 737, extra 54
```

**Follow-ups:**
- What if the parallel run shows no gain? Then keep the scorecard. That is a valid outcome.
- What if the VP is right on one segment? Use the scorecard there or fix the model.

**Common mistakes:** Treating it as technical only. Quoting AUC to a business owner. Ambushing the VP in a meeting. Retiring without exit criteria.

### Q44 ⭐ 🔴 Legal, growth and trust-and-safety each want a different moderation threshold on 100,000 items with 2,000 true violations. Threshold X gives 60% recall at 80% precision and threshold Y gives 75% recall at 75% precision, and a missed violation costs 50 against 5 for a wrongly flagged item. Compute the cost of each, and say how you would get the three groups to agree.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing
**Say this first (1 line):** At the stated 50-to-5 costs, threshold Y costs 27,500 and threshold X 41,500, so Y wins unless a miss costs less than two thirds of a false flag, and I would get the three groups to agree on the cost matrix first.

**Clarifying questions:**
- Where do the 50 and 5 come from, and does Legal see harm in wrongful flags that 5 understates? Why: if a false flag costs more than a miss, the choice flips.
- What is the human review capacity? Why: Y flags 2,000 items versus 1,500 for X.
- Can action be tiered (auto remove, review, leave)? Why: tiers beat one threshold.
- Are precision and recall measured on a fresh labelled sample, and how big? Why: errors in them move the cost.
- Who decides if the groups still disagree? Why: needs an owner.

**Approach:**
1. Compute: X catches 1,200 of 2,000, misses 800, flags 1,500 (1,200 / 0.8), so 300 are false. Y catches 1,500, misses 500, flags 2,000, so 500 are false.
2. Cost = misses x 50 + false flags x 5. X is 800 x 50 + 300 x 5 = 41,500. Y is 500 x 50 + 500 x 5 = 27,500. Y is cheaper by 14,000.
3. Compute the break-even miss-to-false-flag cost ratio: 200 extra false flags buy 300 fewer misses, so ratio 200 / 300 = 0.667.
4. Get Legal, growth and trust-and-safety to agree one cost matrix, with a range for each team's view.
5. Run sensitivity: if a false flag cost 100 and a miss 50 (ratio 0.5), X costs 70,000 and Y 75,000, so X wins.
6. Offer a tiered policy: high score auto-actioned, middle band to review, within capacity.

**Metrics:** Cost = FN x 50 + FP x 5. FN = positives x (1 - recall). FP = TP / precision - TP. Review load = flagged items. Guardrails: review capacity, appeal rate on wrongful flags.

**Risks:**
- Unmodelled costs: user harm, appeals, legal exposure.
- Precision and recall measured on small samples.
- Each team optimising its own number.

**What the interviewer scores:**
- Strong: correct arithmetic, break-even ratio, capacity check, a decision process.
- Weak: arithmetic errors, or picking by who shouts loudest.

**Example:** X: TP 1,200, FN 800, flagged 1,500, FP 300, cost 40,000 + 1,500 = 41,500. Y: TP 1,500, FN 500, flagged 2,000, FP 500, cost 25,000 + 2,500 = 27,500. The 100,000 total items does not enter the cost.
- Weak: "X has higher precision so X is better."
- Strong: "Y costs 14,000 less. It only loses if a miss costs under two thirds of a false flag. Let us agree the cost matrix and our review capacity."

**Code:**
```python
# Q44: cost of thresholds X and Y (prompt numbers)
pos = 2000
cost_fn, cost_fp = 50, 5
def cost(recall, precision, rnd=False):
    tp = recall * pos
    fn = pos - tp
    flagged = tp / precision
    fp = flagged - tp
    if rnd: fn, fp, flagged = round(fn), round(fp), round(flagged)
    return fn, fp, flagged, fn * cost_fn + fp * cost_fp
for name, r, p in (("X", 0.60, 0.80), ("Y", 0.75, 0.75)):
    fn, fp, fl, c = cost(r, p)
    print(f"{name}: FN {fn:.0f}, FP {fp:.2f}, flagged {fl:.2f}, cost {c:,.2f}")
cx, cy = cost(0.6, 0.8)[3], cost(0.75, 0.75)[3]
assert cost(0.6, 0.8)[:3] == (800, 300, 1500) and cx == 41_500
assert cost(0.75, 0.75)[:3] == (500, 500, 2000) and cy == 27_500
print(f"Y is cheaper by {cx-cy:,.0f}")
# break-even miss:false-flag cost ratio r (FP cost fixed at 5)
fnx, fpx, _, _ = cost(0.6, 0.8); fny, fpy, _, _ = cost(0.75, 0.75)
r = (fpy - fpx) / (fnx - fny)
print(f"break-even FN:FP cost ratio = {r:.3f} (prompt ratio is 10)")
assert abs(r - 2/3) < 1e-9 and 50 / 5 > r
print("review load: X flags", round(cost(0.6,0.8)[2]), "items, Y flags", round(cost(0.75,0.75)[2]))
# sensitivity: if a false flag cost 100 and a miss 50 (ratio 0.5), X wins
def total(fn, fp, cfn, cfp): return fn*cfn + fp*cfp
assert total(800, 300, 50, 100) == 70_000 and total(500, 500, 50, 100) == 75_000
print("false flag 100, miss 50: X", total(800,300,50,100), "Y", total(500,500,50,100))
```

**Output (my run):**
```text
X: FN 800, FP 300.00, flagged 1500.00, cost 41,500.00
Y: FN 500, FP 500.00, flagged 2000.00, cost 27,500.00
Y is cheaper by 14,000
break-even FN:FP cost ratio = 0.667 (prompt ratio is 10)
review load: X flags 1500 items, Y flags 2000
false flag 100, miss 50: X 70000 Y 75000
```

**Follow-ups:**
- What if Legal says a false flag costs 100 against a miss of 50? Then X costs 70,000 and Y 75,000, so X wins.
- Could a third threshold be better? Possibly. Sweep the curve, and see Book 1 Part 03, Q41: "Derive the Bayes-optimal threshold for a given cost matrix and explain why it needs calibrated probabilities."

**Common mistakes:** Using the 100,000 in the cost. Ignoring review capacity. Using one cost for all groups. Presenting a winner without sensitivity.

### Q45 ⭐ 🔴 Leadership says agentic AI will make the data-science team unnecessary within a year and asks for a plan to cut its scope. You believe parts of that are right and parts are risky. How do you frame the team's value, and which tasks do you volunteer to automate and which do you defend?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to AI-era build-versus-buy and hallucination-risk material (2026 vendor and CTO-guide pages such as ThirstySprout and TKMX AI on API versus self-host and LLM cost, an InfoQ LLM-adoption article); no interview page for the leadership-pressure framing was found
**Say this first (1 line):** I agree that routine query answering and boilerplate should be automated, so I volunteer those, and I defend the work that decides what to measure and whether results can be trusted, because unsupervised AI answers are still wrong too often.

**Clarifying questions:**
- What outcome does leadership want: cost, speed, or fewer requests queued? Why: automation can serve each differently.
- What share of team time is routine versus judgement? Why: sizes the real saving.
- What does a wrong answer cost in these workflows? Why: it sets how much review is needed.
- What accuracy have the tools shown on our tasks? Why: Q40 of this part shows a 74% text-to-SQL result, well below a 95% bar.
- Who is accountable when an automated answer is wrong? Why: accountability is the part that stays human.

**Approach:**
1. Agree with the premise where it is right: much routine work will be automated.
2. Volunteer a list: routine query answering on certified metrics, dashboard refreshes, boilerplate code, first-draft EDA and documentation.
3. Quantify net savings after review: for example 213.75 of 1,000 hours a month (21%).
4. Defend: problem framing, metric definitions, experiment and causal design, validation and monitoring of models, data quality, and being accountable for decisions.
5. Propose a one-year plan: automate in tiers, measure error, promote a task only when its measured accuracy meets the bar.
6. Reframe the team as the owner of quality and decisions, with AI as a tool.

**Metrics:** Net hours freed = hours x automated share x (1 - review overhead). Error rate of automated outputs on an audit sample. Time to answer. Guardrails: wrong-answer rate, incidents from unreviewed output.

**Risks:**
- Cutting the review layer and shipping confident wrong answers.
- Sounding defensive, which reads as protecting jobs.
- Losing the people who define metrics and catch errors.

**What the interviewer scores:**
- Strong: concedes what is true, offers a concrete automation list with numbers, defends specific tasks with reasons, uses evidence.
- Weak: "AI cannot do what we do", or giving up the whole scope.

**Example:** Illustrative mix of 1,000 hours: routine queries 350, boilerplate 150, design and causal work 250, modelling and validation 200, advice 50. Automate 60% of routine and 50% of boilerplate with a 25% review overhead: net saved 157.5 + 56.25 = 213.75 hours, 21.4%. Half the work remains: judgement and accountability.
- Weak: "Agents cannot replace data scientists."
- Strong: "I would automate the routine query and boilerplate work, which frees about a fifth of our time after review. I would keep metric design, experiments and validation, because the tool is wrong 26 times in 100 on our test."

**Code:**
```python
# Q45: capacity freed by automating routine work, net of review time (illustrative)
team_hours = 1000                       # analyst/DS hours per month
mix = {"routine queries and refreshes": 0.35, "boilerplate code, EDA, docs": 0.15,
       "metric definitions, experiment design, causal reads": 0.25,
       "model building, validation, monitoring": 0.20, "stakeholder advice": 0.05}
assert abs(sum(mix.values()) - 1) < 1e-9
auto_share = {"routine queries and refreshes": 0.60, "boilerplate code, EDA, docs": 0.50}
review_overhead = 0.25                  # reviewing AI output costs 25% of the time it replaces
freed = 0
for k, s in auto_share.items():
    h = team_hours * mix[k]
    saved = h * s * (1 - review_overhead)
    print(f"{k:34} {h:>5.0f} h, automate {s:.0%}, net saved {saved:6.1f} h")
    freed += saved
print(f"net hours freed = {freed:.1f} of {team_hours} = {freed/team_hours:.1%}")
assert abs(freed - (210*0.75 + 75*0.75)) < 1e-9 and abs(freed - 213.75) < 1e-9
# not 'team unnecessary': the defended work is the share that stays
defended = sum(v for k, v in mix.items() if k not in auto_share)
print(f"work not automated away: {defended:.0%} of the mix")
assert abs(defended - 0.50) < 1e-9
# reality check on unsupervised accuracy (see Q40): 74% right means 26 wrong in 100
print("wrong answers per 100 at 74% accuracy:", 100 - 74)
```

**Output (my run):**
```text
routine queries and refreshes        350 h, automate 60%, net saved  157.5 h
boilerplate code, EDA, docs          150 h, automate 50%, net saved   56.2 h
net hours freed = 213.8 of 1000 = 21.4%
work not automated away: 50% of the mix
wrong answers per 100 at 74% accuracy: 26
```

**Follow-ups:**
- What if the tools improve fast? Re-test quarterly and promote tasks as they pass.
- How do you show value? Decisions improved and errors prevented, with measured examples.

**Common mistakes:** Denying the change. Offering to cut without a plan. Citing no numbers. Treating review as free.

