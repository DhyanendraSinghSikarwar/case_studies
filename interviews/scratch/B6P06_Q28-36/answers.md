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
