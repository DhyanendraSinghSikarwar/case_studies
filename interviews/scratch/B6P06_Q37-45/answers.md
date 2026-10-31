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
