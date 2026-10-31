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

### Q26 ⭐⭐ 🟡 A PM has changed the churn target definition three times in one 20-day sprint, from 30 to 60 to 90 days of inactivity, and each change costs you 3 days of relabelling and retraining. The 9 lost days are 45% of the sprint. What do you do about it, and how do you stop it happening again?
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would show the PM that each definition change costs 3 days of a 20-day sprint, ask for one churn definition agreed in writing with the decision owner, and make my pipeline cheap to relabel so a later change does not cost days.

**Clarifying questions:**
- What decision will the model drive, and over what time window does the business act? The definition should follow the action, not taste.
- Who owns the definition, the PM or a business lead? One named owner prevents repeats.
- Is 30 versus 90 days a real disagreement among stakeholders, or exploration? It tells me whether to mediate or to just parametrise.
- Is the sprint end date fixed? It decides what I trade off.

**Approach:**
1. Do the arithmetic: 3 relabel-and-retrain cycles x 3 days = 9 days = 45% of 20.
2. Note a precision point: 30 to 60 to 90 is three definitions but two changes. If the first was planned work, the avoidable loss is 6 days (30%). Say 9 only if all three are counted as cost.
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
- Strong: quantifies the cost and corrects the count honestly. Weak: complains the PM is indecisive.
- Strong: fixes the process (single owner, spec, change control, parametric labels). Weak: just absorbs the changes.
- Strong: gives the PM a data comparison to decide with. Weak: argues from preference.
- Strong: calm, collaborative tone. Weak: escalates immediately.

**Example:** (illustrative numbers) A simulated gap table gives churn rates of 42.0% at 30 days, 18.6% at 60 and 9.7% at 90, so the three definitions are three different targets, not tweaks. Weak answer: "I keep changing the label whenever you ask." Strong answer: "Each change costs me 3 days, 45% of the sprint if we count all three. Here is how 30, 60 and 90 compare. Can we pick one by Friday and write it down? I will also make the label a parameter so a later change takes half a day."

**Code:**
```python
import numpy as np
sprint, per_change, changes = 20, 3, 3
lost = per_change * changes
print(f"as stated: {changes} relabel-and-retrain cycles x {per_change} days = {lost} days = {lost/sprint:.0%} of {sprint}")
assert lost == 9 and lost/sprint == 0.45
# 30 -> 60 -> 90 is three definitions but two changes; if the first build was needed anyway
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
as stated: 3 relabel-and-retrain cycles x 3 days = 9 days = 45% of 20
if the first definition was planned work, avoidable loss = 6 days = 30%
{30: '42.0%', 60: '18.6%', 90: '9.7%'}
three definitions with a parametrised label: 1.5 days instead of 9
```

**Follow-ups:**
- What if the PM still changes it? Apply change control: it goes into the next sprint unless the owner accepts the cost.
- Which definition do you recommend? The one where most returners have returned (reactivation curve flattens), and that matches the action window.
- Prompt wording: is "changed it three times" right? No, see the note: two changes, three definitions.

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
