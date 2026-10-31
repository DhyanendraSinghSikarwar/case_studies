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
- Which law and policy govern this product, and who owns fair-lending review? The four-fifths rule is an employment-selection guideline often borrowed as a screening heuristic; for lending, the compliance team decides which test applies (check with legal).
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
- The 450,000 is an upper bound; quoting it as fact in a heated room can be wrong in either direction.
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
- The prompt's 94% sounds like a measured result on 500,000 questions; it is more likely a pilot rate projected to that volume.

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
